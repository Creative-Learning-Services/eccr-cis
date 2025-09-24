from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from eccr.serializers.competency import WorkRoleSerializer
from eccr.repositories.workrole_repo import list_workroles, get_workrole


class WorkRoleListView(GenericAPIView):
    serializer_class = WorkRoleSerializer

    @extend_schema(
        tags=["ECCR Data - Work Roles"],
        summary="List Work Roles",
        description="""
        Retrieve a paginated list of work roles
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
                description="List of work roles retrieved successfully"
            ),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    def get(self, request):
        try:
            limit = int(request.query_params.get("limit", 5))
            skip = int(request.query_params.get("skip", 0))
            repo_result = list_workroles(limit=limit, skip=skip)
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


class WorkRoleDetailView(GenericAPIView):
    serializer_class = WorkRoleSerializer

    def get(self, request, work_role_id):
        try:
            wr = get_workrole(work_role_id)
            if not wr:
                return Response(
                    {"error": "Work role not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = self.get_serializer(wr)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
