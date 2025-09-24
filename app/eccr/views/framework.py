from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from eccr.serializers import FrameworkSerializer
from eccr.serializers.competency import CompetencySerializer
from eccr.repositories.framework_repo import (
    list_frameworks,
    get_framework,
    get_framework_with_competencies,
)


class FrameworkListView(GenericAPIView):
    serializer_class = FrameworkSerializer

    @extend_schema(
        tags=["ECCR Data - Frameworks"],
        summary="List Frameworks",
        description="""
        Retrieve a paginated list of cybersecurity frameworks.
        
        Includes DCWF (Data Center Workforce Framework) and other 
        industry-standard cybersecurity frameworks.
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
        ],
        responses={
            200: OpenApiResponse(
                description="List of frameworks retrieved successfully"
            ),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    def get(self, request):
        try:
            limit = int(request.query_params.get("limit", 5))
            skip = int(request.query_params.get("skip", 0))
            repo_result = list_frameworks(limit=limit, skip=skip)
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


class FrameworkDetailView(GenericAPIView):
    serializer_class = FrameworkSerializer

    def get(self, request, framework_id):
        try:
            fw = get_framework(framework_id)
            if not fw:
                return Response(
                    {"error": "Framework not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = self.get_serializer(fw)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class FrameworkWithCompetenciesView(GenericAPIView):
    serializer_class = FrameworkSerializer

    def get(self, request, framework_id):
        try:
            limit = int(request.query_params.get("competency_limit", 5))
            skip = int(request.query_params.get("competency_skip", 0))
            data = get_framework_with_competencies(framework_id, limit=limit, skip=skip)
            if not data:
                return Response(
                    {"error": "Framework not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            framework_serialized = self.get_serializer(data["framework"]).data
            competencies_serialized = [
                CompetencySerializer(c).data for c in data["competencies"]
            ]
            return Response(
                {
                    "framework": framework_serialized,
                    "competencies": competencies_serialized,
                    "competency_pagination": data["competency_pagination"],
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
