from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from eccr.serializers.competency import CompetencySerializer
from eccr.repositories.competency_repo import list_competencies, get_competency


class CompetencyListView(GenericAPIView):
    serializer_class = CompetencySerializer

    @extend_schema(
        tags=["ECCR Data - Competencies"],
        summary="List Competencies",
        description="""
        Retrieve a paginated list of competencies from the ECCR system.
        
        Supports filtering by name and domain to help find specific competencies.
        """,
        parameters=[
            OpenApiParameter(
                name="limit",
                description="Number of results to return (default: 5)",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="skip",
                description="Number of results to skip for pagination (default: 0)",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="name_contains",
                description="Filter competencies by name containing this text",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="domain",
                description="Filter competencies by domain",
                required=False,
                type=str,
            ),
        ],
        responses={
            200: OpenApiResponse(
                description="List of competencies retrieved successfully"
            ),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    def get(self, request):
        try:
            limit = int(request.query_params.get("limit", 5))
            skip = int(request.query_params.get("skip", 0))
            filters = {
                k: v
                for k, v in {
                    "name_contains": request.query_params.get("name_contains"),
                    "domain": request.query_params.get("domain"),
                }.items()
                if v is not None and v != ""
            }
            repo_result = list_competencies(limit=limit, skip=skip, filters=filters)
            serializer = self.get_serializer(repo_result["results"], many=True)
            return Response(
                {
                    "results": serializer.data,
                    "total": repo_result["total"],
                    "limit": limit,
                    "skip": skip,
                }
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CompetencyDetailView(GenericAPIView):
    serializer_class = CompetencySerializer

    @extend_schema(
        tags=["ECCR Data - Competencies"],
        summary="Get Competency Details",
        description="""
        Retrieve detailed information about a specific competency by its ID.
        
        Returns comprehensive information about the competency including
        its properties and relationships.
        """,
        responses={
            200: OpenApiResponse(
                description="Competency details retrieved successfully"
            ),
            404: OpenApiResponse(description="Competency not found"),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    def get(self, request, id):
        try:
            comp = get_competency(id)
            if not comp:
                return Response(
                    {"error": "Competency not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = self.get_serializer(comp)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
