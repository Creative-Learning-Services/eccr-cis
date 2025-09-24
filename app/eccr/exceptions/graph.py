from rest_framework.response import Response
from rest_framework import status
import logging

from eccr.services.graph_service import GraphOperationError
from eccr.utils.validation import SchemaValidationError

logger = logging.getLogger(__name__)


class GraphExceptionHandler:
    """Custom exception handler for graph operations"""

    @staticmethod
    def handle_exceptions(e: Exception) -> Response:
        """Common exception handling for graph operations"""
        if isinstance(e, SchemaValidationError):
            logger.warning(f"Schema validation error: {e}")
            return Response(
                {
                    "error": "Validation Error",
                    "message": str(e),
                    "errors": getattr(e, "errors", []),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif isinstance(e, GraphOperationError):
            logger.error(f"Graph operation error: {e}")
            return Response(
                {"error": "Graph Operation Error", "message": str(e)},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        else:
            logger.error(f"Unexpected error: {e}")
            return Response(
                {
                    "error": "Internal Server Error",
                    "message": "An unexpected error occurred",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
