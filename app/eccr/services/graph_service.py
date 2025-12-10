import logging
from typing import Any, Dict, List, Optional

from eccr.repositories.graph_repo import (
    create_node_and_relate_to_existing,
    create_node_with_relationship,
    create_nodes_batch,
    find_existing_node,
)
from eccr.utils.validation import PayloadValidator, SchemaValidationError

logger = logging.getLogger(__name__)


class GraphOperationError(Exception):
    """Custom exception for graph operation errors"""

    pass


class GraphService:
    """Service layer for graph operations"""

    def __init__(self):
        self.validator = PayloadValidator()

    def create_nodes(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create multiple nodes without relationships

        Args:
            payload: Dictionary containing operation data

        Returns:
            Dictionary with operation results

        Raises:
            SchemaValidationError: If payload validation fails
            GraphOperationError: If graph operation fails
        """
        try:
            # Validate payload
            self.validator.validate_create_nodes_payload(payload)

            # Extract nodes
            nodes = payload["nodes"]

            logger.info(f"Creating {len(nodes)} nodes")

            # Create nodes in Neo4j
            result = create_nodes_batch(nodes)

            logger.info(f"Successfully created {len(nodes)} nodes")

            return {
                "operation": "create_nodes",
                "status": "success",
                "nodes_created": len(nodes),
                "node_ids": [node["properties"]["id"] for node in nodes],
                "details": result,
            }

        except SchemaValidationError:
            raise
        except Exception as e:
            logger.error(f"Error creating nodes: {str(e)}")
            raise GraphOperationError(f"Failed to create nodes: {str(e)}")

    def create_relationship(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create two new nodes with a relationship between them

        Args:
            payload: Dictionary containing operation data

        Returns:
            Dictionary with operation results

        Raises:
            SchemaValidationError: If payload validation fails
            GraphOperationError: If graph operation fails
        """
        try:
            # Validate payload
            self.validator.validate_create_relationship_payload(payload)

            # Extract data
            source_node = payload["source_node"]
            destination_node = payload["destination_node"]
            relationship = payload["relationship"]

            logger.info(
                f"Creating relationship from {source_node['label']} to {destination_node['label']}"
            )

            # Create nodes and relationship in Neo4j
            result = create_node_with_relationship(
                source_node, destination_node, relationship
            )

            logger.info(f"Successfully created nodes and relationship")

            return {
                "operation": "create_relationship",
                "status": "success",
                "source_node_id": source_node["properties"]["id"],
                "destination_node_id": destination_node["properties"]["id"],
                "relationship_type": relationship["edge_label"],
                "details": result,
            }

        except SchemaValidationError:
            raise
        except Exception as e:
            logger.error(f"Error creating relationship: {str(e)}")
            raise GraphOperationError(f"Failed to create relationship: {str(e)}")

    def create_relationship_to_existing(
        self, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a new node and relate it to an existing node

        Args:
            payload: Dictionary containing operation data

        Returns:
            Dictionary with operation results

        Raises:
            SchemaValidationError: If payload validation fails
            GraphOperationError: If graph operation fails
        """
        try:
            # Validate payload
            self.validator.validate_create_relationship_to_existing_payload(payload)

            # Extract data
            new_node = payload["new_node"]
            existing_node_ref = payload["existing_node_reference"]
            relationship = payload["relationship"]
            validation_config = payload.get("validation", {})

            logger.info(
                f"Creating new {new_node['label']} node and relating to existing {existing_node_ref['label']}"
            )

            # Check if existing node exists
            if validation_config.get("check_existing_node", True):
                existing_node = find_existing_node(
                    existing_node_ref["label"],
                    existing_node_ref["lookup_method"],
                    existing_node_ref["lookup_value"],
                )

                if not existing_node and validation_config.get(
                    "fail_if_not_exists", True
                ):
                    raise GraphOperationError(
                        f"Existing node not found: {existing_node_ref['label']} "
                        f"with {existing_node_ref['lookup_method']} = {existing_node_ref['lookup_value']}"
                    )

            # Create new node and relationship
            result = create_node_and_relate_to_existing(
                new_node, existing_node_ref, relationship, validation_config
            )

            logger.info(
                f"Successfully created new node and relationship to existing node"
            )

            return {
                "operation": "create_relationship_to_existing",
                "status": "success",
                "new_node_id": new_node["properties"]["id"],
                "existing_node_reference": existing_node_ref,
                "relationship_type": relationship["edge_label"],
                "details": result,
            }

        except SchemaValidationError:
            raise
        except Exception as e:
            logger.error(f"Error creating relationship to existing node: {str(e)}")
            raise GraphOperationError(
                f"Failed to create relationship to existing node: {str(e)}"
            )


# Convenience instance
graph_service = GraphService()
