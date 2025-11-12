import json
import typing

from django.core.paginator import Paginator
from django.http import Http404
from django.utils.functional import cached_property
from neomodel import db
from neomodel.sync_.core import StructuredNode
from rest_framework import filters, pagination, status
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from competencies.models import DjangoDomain, NeoDomain
from competencies.serializers import DynamicNodeSerializer, SpoofedSerializer

# Create your views here.


class GenericNode():
    """
    Class to store generic attributes and relationships
    """

    def __init__(self, items: typing.ItemsView[str, typing.Any]):
        self.__attributes = set()
        for k, v in items:
            self._add_attr(k, v)

    def _attributes(self, k):
        self.__attributes.add(k)

    def _add_attr(self, k, v):
        if hasattr(self, k):
            curr = getattr(self, k)
            if isinstance(curr, list):
                curr.append(v)
            else:
                setattr(self, k, [curr, v])
        else:
            setattr(self, k, v)
        self._attributes(k)

    def __repr__(self):
        return str({k: getattr(self, k) for k in self.__attributes})


class LazyNeoQuery():
    """
    Class for setting up Neo4j queries in a lazy way
    """
    # Pretty much a copy of how QuerySets work
    # currently not a subclass of QuerySets as content diverges so much
    # but this might change in the future

    def __init__(self, obj: StructuredNode, query: str, order: str = "n.uuid"):
        """
        Setup object
        """
        self._object = obj
        self._chain = query
        self._filters = set()
        self._args = {}
        self._order = order
        self._skip = None
        self._limit = None
        self._result_cache = None

    @property
    def order(self):
        """
        return formatted order
        """
        if not self._order:
            return ""
        return f"ORDER BY {self._order}"

    @property
    def skip(self):
        """
        return formatted skip
        """
        if not self._skip:
            return ""
        return f"SKIP {self._skip}"

    @property
    def limit(self):
        """
        return formatted limit
        """
        if not self._limit:
            return ""
        return f"LIMIT {self._limit}"

    @cached_property
    @db.read_transaction
    def count(self) -> int:
        """
        get the count
        """
        if self._result_cache is not None:
            return len(self._result_cache)
        return self._object.cypher('\n'.join([
            self._chain,
            self._get_filter_clause(),
            'RETURN count(*)',
            self.skip,
            self.limit]),
            self._args)[0][0][0]

    def filter(self, filter_str: str, param: dict):
        """
        add filters to a query
        """
        self._filters.add(filter_str)
        self._args.update(param)

    def _get_filter_clause(self):
        """
        Format the WHERE clause for the filter query
        """
        if not self._filters:
            return ""
        return "WHERE " + " OR ".join(self._filters)

    def _resolve_query(self):
        if self._result_cache is not None:
            return len(self._result_cache)
        self._result_cache = self._object.cypher('\n'.join([
            self._chain,
            self._get_filter_clause(),
            'RETURN n',
            self.order,
            self.skip,
            self.limit]),
            self._args)[0]
        return self._result_cache

    @db.read_transaction
    def __getitem__(self, k):
        """Retrieve an item or slice from the set of results."""
        if not isinstance(k, (int, slice)):
            raise TypeError(
                f"LazyNeoQuery indices must be integers or slices, not {type(k).__name__}."
            )
        if (isinstance(k, int) and k < 0) or (
            isinstance(k, slice)
            and (
                (k.start is not None and k.start < 0)
                or (k.stop is not None and k.stop < 0)
            )
        ):
            raise ValueError("Negative indexing is not supported.")

        if self._result_cache is not None:
            return self._result_cache[k]

        if isinstance(k, slice):
            if k.start is not None:
                self._skip = int(k.start)
            if k.stop is not None:
                self._limit = int(k.stop) - self._skip if self._skip else 0
            return list(self._resolve_query())[:: k.step] if k.step else self._resolve_query()

        self._skip = int(k)
        self._limit = 1
        self._resolve_query()
        return self._result_cache[0]


class CustomPaginator(Paginator):

    @cached_property
    def count(self):
        """Return the total number of objects, across all pages."""
        return self.object_list.count


class CustomPagination(pagination.PageNumberPagination):
    """custom pagination to add page_size from api. For example:

    http://api.example.org/accounts/?page=4
    http://api.example.org/accounts/?page=4&page_size=100"""

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50
    django_paginator_class = CustomPaginator

    # def paginate_queryset(self, queryset, request, view=None):
    #     return super().paginate_queryset(queryset, request, view)


class DomainList(ListAPIView):
    """
    List Domains available
    """
    queryset = DjangoDomain.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        return Response(
            json.dumps(
                [n.name for n in NeoDomain.nodes.all()]
            ),
            status=status.HTTP_200_OK)


class DomainSubGraphList(ListAPIView):
    """
    List objects connected to chosen Domain
    """
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = SpoofedSerializer

    # add fields to be searched on in the query
    search_fields = ['metadata_key',
                     'metadata_key_hash', 'provider_name',
                     'unique_record_identifier']

    def get_queryset(self):
        """override queryset to filter using provider_id"""

        provider_id = self.kwargs['provider_id']
        if 'fields' in self.request.GET and\
                self.request.GET.get('fields') is not None:
            self.search_fields += self.request.GET.get('fields').\
                replace('.', '__').split(',')

        queryset = LazyNeoQuery(
            NeoDomain.nodes.get(name=provider_id),
            "MATCH (:NeoDomain {element_id_property: $self})-[r:HOLDS]->(n)")
        # figure out how to support slicing and filtering

        return queryset

    def filter_queryset(self, queryset: LazyNeoQuery):
        """override search filter to filter using ?search=value1 value2..."""

        # get search terms
        values = filters.SearchFilter().get_search_terms(self.request)

        # if no search, don't filter
        if not values:
            return queryset

        # add filters for each field and value pair
        for pos, value in enumerate(values):
            for field in self.search_fields:
                queryset.filter(f"n.{field} = ${pos}", {pos: value})

        return queryset


class GenericNodeEndpoint(RetrieveUpdateAPIView):
    """
    Get or update a Node
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = DynamicNodeSerializer

    def get_object(self):
        # get base object in case no relationships
        query_resp = db.cypher_query(
            '''
            MATCH (d:NeoDomain {name: $domain_name})-[:HOLDS]->(n{uuid: $node_id})
            RETURN n
            LIMIT 1
            ''',
            {
                'domain_name': self.kwargs['provider_id'],
                'node_id': self.kwargs['experience_id'],
            })[0]

        if not query_resp:
            raise Http404

        # add attributes
        node = GenericNode(query_resp[0][0].items())

        # get relationships
        query_resp = db.cypher_query(
            '''
            MATCH (:NeoDomain {name: $domain_name})-[:HOLDS]->({uuid: $node_id})-[r]->(m)
            RETURN r, m
            ''',
            {
                'domain_name': self.kwargs['provider_id'],
                'node_id': self.kwargs['experience_id'],
            })[0]
        # add relationships to uuid
        for rel, _ in query_resp:
            node._add_attr(  # pylint: disable=W0212
                rel.type, rel.end_node['uuid'])
        return node
