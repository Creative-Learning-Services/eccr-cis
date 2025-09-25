from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
import logging
from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
    inline_serializer,
)
from rest_framework import serializers

from eccr.services.graph_service import graph_service, GraphOperationError
from eccr.utils.validation import SchemaValidationError
from eccr.exceptions import GraphExceptionHandler

logger = logging.getLogger(__name__)


class BaseGraphView(GenericAPIView):
    """Base view for graph operations with common error handling"""

    parser_classes = [JSONParser]

    def handle_exceptions(self, e: Exception) -> Response:
        """Delegate exception handling to the custom exception handler"""
        return GraphExceptionHandler.handle_exceptions(e)


class CreateNodesView(BaseGraphView):
    """
    Create multiple nodes without relationships
    """

    @extend_schema(
        tags=["Graph Operations - Nodes"],
        summary="Create Nodes",
        description="Create multiple nodes in the Neo4j graph database with specified labels and properties",
        request=inline_serializer(
            name="CreateNodesRequest",
            fields={
                "operation": serializers.CharField(default="create_nodes"),
                "nodes": serializers.ListField(
                    child=serializers.DictField(
                        child=serializers.JSONField(),
                        help_text="Node object with 'label' and 'properties' keys",
                    ),
                    help_text="List of nodes to create",
                ),
            },
        ),
        examples=[
            OpenApiExample(
                "Create DCWF Framework Nodes",
                value={
                    "operation": "create_nodes",
                    "nodes": [
                        {
                            "label": "DCWFFramework",
                            "properties": {
                                "id": "DCWFF-001",
                                "name": "Cyber Defense Framework",
                                "description": "Framework for cyber defense competencies",
                                "version": "1.0",
                            },
                        },
                        {
                            "label": "DCWFFramework",
                            "properties": {
                                "id": "DCWFF-002",
                                "name": "Incident Response Framework",
                                "description": "Framework for incident response procedures",
                            },
                        },
                    ],
                },
            )
        ],
        responses={
            201: OpenApiResponse(
                description="Nodes created successfully",
                examples=[
                    OpenApiExample(
                        "Success Response",
                        value={
                            "operation": "create_nodes",
                            "status": "success",
                            "nodes_created": 2,
                            "node_ids": ["DCWFF-001", "DCWFF-002"],
                            "details": {
                                "nodes_created": 2,
                                "nodes": [
                                    {
                                        "label": "DCWFFramework",
                                        "properties": {"id": "DCWFF-001"},
                                    },
                                    {
                                        "label": "DCWFFramework",
                                        "properties": {"id": "DCWFF-002"},
                                    },
                                ],
                            },
                        },
                    )
                ],
            ),
            400: OpenApiResponse(description="Validation error"),
            422: OpenApiResponse(description="Graph operation error"),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    def post(self, request):
        """
        Create multiple nodes in the graph

        Expected payload format:
        {
            "operation": "create_nodes",
            "nodes": [
                {
                    "label": "NodeLabel",
                    "properties": { ... }
                },
                ...
            ]
        }
        """
        try:
            payload = request.data
            result = graph_service.create_nodes(payload)

            return Response(result, status=status.HTTP_201_CREATED)

        except Exception as e:
            return self.handle_exceptions(e)


class CreateRelationshipView(BaseGraphView):
    """
    Create two new nodes with a relationship between them
    """

    @extend_schema(
        tags=["Graph Operations - Relationships"],
        summary="Create Nodes with Relationship",
        description="""Create two new nodes and establish a relationship between them in a single operation.
        
        This endpoint is useful when you need to create two related entities simultaneously,
        such as linking a work role to a required competency.
        
        Use Cases:
        • Create a work role and link it to a required skill
        • Create a framework and associate it with a competency
        • Establish dependencies between new entities""",
        request=inline_serializer(
            name="CreateRelationshipRequest",
            fields={
                "operation": serializers.CharField(default="create_relationship"),
                "source_node": serializers.DictField(
                    child=serializers.JSONField(),
                    help_text="Source node with 'label' and 'properties'",
                ),
                "destination_node": serializers.DictField(
                    child=serializers.JSONField(),
                    help_text="Destination node with 'label' and 'properties'",
                ),
                "relationship": serializers.DictField(
                    child=serializers.JSONField(),
                    help_text="Relationship with 'edge_label' and 'properties'",
                ),
            },
        ),
        examples=[
            OpenApiExample(
                "Work Role to Competency",
                summary="Link a work role to a required competency",
                value={
                    "operation": "create_relationship",
                    "source_node": {
                        "label": "AdvancedWorkRole",
                        "properties": {
                            "id": "AWR-SEC-001",
                            "name": "Senior Security Analyst",
                            "description": "Advanced cybersecurity analysis role",
                        },
                    },
                    "destination_node": {
                        "label": "KsatsKnowledge",
                        "properties": {
                            "id": "K-001",
                            "name": "Network Security Protocols",
                            "description": "Knowledge of network security protocols",
                        },
                    },
                    "relationship": {
                        "edge_label": "REQUIRES",
                        "properties": {"importance": "critical", "level": "expert"},
                    },
                },
            )
        ],
        responses={
            201: OpenApiResponse(
                description="Nodes and relationship created successfully"
            ),
            400: OpenApiResponse(description="Validation error"),
            422: OpenApiResponse(description="Graph operation error"),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    def post(self, request):
        """
        Create two nodes and a relationship between them

        Expected payload format:
        {
            "operation": "create_relationship",
            "source_node": {
                "label": "SourceLabel",
                "properties": { ... }
            },
            "destination_node": {
                "label": "DestLabel",
                "properties": { ... }
            },
            "relationship": {
                "edge_label": "RELATIONSHIP_TYPE",
                "properties": { ... }
            }
        }
        """
        try:
            payload = request.data
            result = graph_service.create_relationship(payload)

            return Response(result, status=status.HTTP_201_CREATED)

        except Exception as e:
            return self.handle_exceptions(e)


class CreateRelationshipToExistingView(BaseGraphView):
    """
    Create a new node and relate it to an existing node
    """

    @extend_schema(
        tags=["Graph Operations - Relationships"],
        summary="Create Node and Link to Existing",
        description="""Create a new node and establish a relationship with an existing node in the graph.
        
        This endpoint is useful when you want to add new entities that relate to 
        existing ones, such as adding a new skill to an existing work role.
        
        Use Cases:
        • Add new competencies to existing work roles
        • Link new frameworks to existing organizational structures
        • Create dependencies with existing entities""",
        request=inline_serializer(
            name="CreateRelationshipToExistingRequest",
            fields={
                "operation": serializers.CharField(
                    default="create_relationship_to_existing"
                ),
                "new_node": serializers.DictField(
                    child=serializers.JSONField(),
                    help_text="New node to create with 'label' and 'properties'",
                ),
                "existing_node_reference": serializers.DictField(
                    child=serializers.JSONField(),
                    help_text="Reference to existing node with lookup information",
                ),
                "relationship": serializers.DictField(
                    child=serializers.JSONField(),
                    help_text="Relationship definition with direction and properties",
                ),
            },
        ),
        examples=[
            OpenApiExample(
                "Add Skill to Existing Role",
                summary="Create new skill and link to existing work role",
                value={
                    "operation": "create_relationship_to_existing",
                    "new_node": {
                        "label": "KsatsSkill",
                        "properties": {
                            "id": "S-CYBER-001",
                            "name": "Threat Detection",
                            "description": "Ability to detect cybersecurity threats",
                        },
                    },
                    "existing_node_reference": {
                        "label": "Job",
                        "lookup_method": "by_id",
                        "lookup_value": "WR-AN-EX-001",
                    },
                    "relationship": {
                        "edge_label": "REQUIRES",
                        "direction": "from_existing_to_new",
                        "properties": {"proficiency_level": "intermediate"},
                    },
                },
            )
        ],
        responses={
            201: OpenApiResponse(description="Node created and linked successfully"),
            400: OpenApiResponse(description="Validation error"),
            404: OpenApiResponse(description="Existing node not found"),
            422: OpenApiResponse(description="Graph operation error"),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    def post(self, request):
        """
        Create a new node and relate it to an existing node

        Expected payload format:
        {
            "operation": "create_relationship_to_existing",
            "new_node": {
                "label": "NewNodeLabel",
                "properties": { ... }
            },
            "existing_node_reference": {
                "label": "ExistingLabel",
                "lookup_method": "by_id|by_property",
                "lookup_value": "...",
            },
            "relationship": {
                "edge_label": "RELATIONSHIP_TYPE",
                "direction": "from_existing_to_new|from_new_to_existing",
                "properties": { ... }
            },
            "validation": {
                "check_existing_node": true,
                "fail_if_not_exists": true,
                "create_if_duplicate": false
            }
        }
        """
        try:
            payload = request.data
            result = graph_service.create_relationship_to_existing(payload)

            return Response(result, status=status.HTTP_201_CREATED)

        except Exception as e:
            return self.handle_exceptions(e)


class GraphHealthView(GenericAPIView):
    """
    Check the health of the graph database connection
    """

    @extend_schema(
        tags=["System Health"],
        summary="Graph Database Health Check",
        description="""Check the connectivity and health of the Neo4j graph database.
        
        This endpoint performs a simple connectivity test to ensure the graph database
        is accessible and responding to queries.
        
        Use Cases:
        • System monitoring and health checks
        • Troubleshooting database connectivity issues
        • Automated health monitoring for CI/CD pipelines""",
        responses={
            200: OpenApiResponse(
                description="Database is healthy and accessible",
                examples=[
                    OpenApiExample(
                        "Healthy Response",
                        value={
                            "status": "healthy",
                            "database": "neo4j",
                            "message": "Graph database connection successful",
                        },
                    )
                ],
            ),
            503: OpenApiResponse(
                description="Database is not accessible",
                examples=[
                    OpenApiExample(
                        "Unhealthy Response",
                        value={
                            "status": "unhealthy",
                            "database": "neo4j",
                            "error": "Connection failed: Unable to connect to database",
                        },
                    )
                ],
            ),
        },
    )
    def get(self, request):
        """Check graph database connectivity"""
        try:
            from eccr.neo4j_driver import get_driver

            driver = get_driver()
            with driver.session() as session:
                result = session.run("RETURN 1 as health_check")
                record = result.single()

                if record and record["health_check"] == 1:
                    return Response(
                        {
                            "status": "healthy",
                            "database": "connected",
                            "timestamp": (
                                str(logger._cache.keys())
                                if hasattr(logger, "_cache")
                                else "unknown"
                            ),
                        }
                    )
                else:
                    return Response(
                        {"status": "unhealthy", "database": "connection_failed"},
                        status=status.HTTP_503_SERVICE_UNAVAILABLE,
                    )

        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return Response(
                {"status": "unhealthy", "database": "error", "error": str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
