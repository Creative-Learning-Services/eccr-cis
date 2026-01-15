import json

from django.http import Http404
from neomodel import db
from rest_framework import filters, status
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveUpdateAPIView)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from competencies.models import DjangoDomain, GenericNode, NeoDomain
from competencies.serializers import DynamicNodeSerializer, SpoofedSerializer
from competencies.utils.graph_utils import CustomPagination, LazyNeoQuery


class NodeCreation(CreateAPIView):
    """
    Create Nodes
    """

    serializer_class = DynamicNodeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class DomainList(ListAPIView):
    """
    List Domains available
    """

    queryset = DjangoDomain.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        return Response(
            json.dumps([n.name for n in NeoDomain.nodes.all()]),
            status=status.HTTP_200_OK,
        )


class DomainSubGraphList(ListAPIView):
    """
    List objects connected to chosen Domain
    """

    pagination_class = CustomPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = SpoofedSerializer

    # add fields to be searched on in the query
    search_fields = [
        "metadata_key",
        "metadata_key_hash",
        "provider_name",
        "unique_record_identifier",
    ]

    def get_queryset(self):
        """override queryset to filter using provider_id"""

        # get domain from provider, will be a human readable name
        provider_id = self.kwargs["provider_id"]

        # add any fields we need to search
        if "fields" in self.request.GET and self.request.GET.get("fields")\
                is not None:
            self.search_fields += (
                self.request.GET.get("fields").replace(".", "__").split(",")
            )

        # get the domain based on the name
        nd = NeoDomain.nodes.get(name=provider_id)
        # setup the base query for objects under the domain
        queryset = LazyNeoQuery(
            nd, "MATCH (:NeoDomain {uuid: $self_uuid})-[r:HOLDS]->(n)"
        )
        # figure out how to support slicing and filtering
        queryset.add_param({"self_uuid": nd.uuid})

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
            """
            MATCH (d:NeoDomain {name: $domain_name})-[:HOLDS]->
            (n{uuid: $node_id})
            RETURN n
            LIMIT 1
            """,
            {
                "domain_name": self.kwargs["provider_id"],
                "node_id": self.kwargs["experience_id"],
            },
        )[0]

        if not query_resp:
            raise Http404

        # add attributes
        node = GenericNode(query_resp[0][0].items())

        # get relationships
        query_resp = db.cypher_query(
            """
            MATCH (:NeoDomain {name: $domain_name})-[:HOLDS]->
            ({uuid: $node_id})-[r]->(m)
            RETURN r, m
            """,
            {
                "domain_name": self.kwargs["provider_id"],
                "node_id": self.kwargs["experience_id"],
            },
        )[0]
        # add relationships to uuid
        for rel, _ in query_resp:
            node._add_attr(
                rel.type, rel.end_node["uuid"])  # pylint: disable=W0212
        return node
