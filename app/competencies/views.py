import json

from django.core.paginator import Paginator
from django.utils.functional import cached_property
from neomodel import db
from rest_framework import filters, pagination, status
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from competencies.models import DjangoDomain, NeoDomain
from competencies.serializers import (DjangoDomainSerializer,
                                      DynamicNodeSerializer, SpoofedSerializer)

# Create your views here.


class LazyNeoQuery():
    """
    Class for setting up Neo4j queries in a lazy way
    """

    def __init__(self):
        """
        Setup object
        """
        pass

    @cached_property
    @db.read_transaction
    def count(self):
        """
        get the count
        """
        pass

    def filter(self, filter):
        """
        add filters to a query
        """
        pass

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
            qs = self._chain()
            if k.start is not None:
                start = int(k.start)
            else:
                start = None
            if k.stop is not None:
                stop = int(k.stop)
            else:
                stop = None
            qs.query.set_limits(start, stop)
            return list(qs)[:: k.step] if k.step else qs

        qs = self._chain()
        qs.query.set_limits(k, k + 1)
        qs._fetch_all()
        return qs._result_cache[0]


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

        def queryset(): return None
        queryset.query = "MATCH (p)-[r:WITHIN]->(:NeoDomain {element_id_property: $self}) "
        queryset.count = queryset.query + 'RETURN count(*)'
        queryset.obj = NeoDomain.nodes.get(name=provider_id)
        # figure out how to support slicing and filtering

        return queryset

    def filter_queryset(self, queryset):
        """override search filter to filter using ?search=value1 value2..."""

        filter_backends = (filters.SearchFilter,)

        for backend in list(filter_backends):
            queryset = backend().filter_queryset(self.request, queryset,
                                                 view=self)
        return queryset


class GenericNodeEndpoint(RetrieveUpdateAPIView):
    """
    Get or update a Node
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = DynamicNodeSerializer

    def get_object(self):
        return NeoDomain.nodes.get(name=self.kwargs['provider_id']).\
            within.get(uid=self.kwargs['experience_id'])
        within.get(uid=self.kwargs['experience_id'])
