import json
import os
from typing import Dict, Any, List, Optional
from jsonschema import validate, ValidationError, RefResolver
from django.conf import settings


class SchemaValidationError(Exception):
    """Custom exception for schema validation errors"""

    def __init__(self, message: str, errors: List[str] = None):
        super().__init__(message)
        self.errors = errors or []


class NodeSchemaValidator:
    """Validates node data against JSON schemas"""

    def __init__(self):
        self.schemas_dir = os.path.join(settings.BASE_DIR, "eccr", "schemas")
        self._schema_cache = {}
        self._resolver = None
        self._load_schemas()

    def _load_schemas(self):
        """Load all schema files into cache"""
        if not os.path.exists(self.schemas_dir):
            raise FileNotFoundError(f"Schemas directory not found: {self.schemas_dir}")

        for filename in os.listdir(self.schemas_dir):
            if filename.endswith(".json"):
                schema_path = os.path.join(self.schemas_dir, filename)
                with open(schema_path, "r") as f:
                    schema = json.load(f)
                    self._schema_cache[filename] = schema

        # Create resolver for reference resolution
        self._resolver = RefResolver(
            base_uri=f"file://{self.schemas_dir}/", referrer={}
        )

    def get_schema_for_label(self, label: str) -> Optional[Dict[str, Any]]:
        """Get schema for a given node label"""
        # Map node labels to schema files
        label_to_schema = {
            "DcwfFramework": "dcwf_framework_node_profile.json",
            "Job": "job_node_profile.json",
            "AdvancedWorkRole": "advanced_work_role_node_profile.json",
            "BasicWorkRole": "basic_work_role_node_profile.json",
            "IntermediateWorkRole": "intermediate_work_role_node_profile.json",
            "KsatsAbility": "ksats_ability_node_profile.json",
            "KsatsKnowledge": "ksats_knowledge_node_profile.json",
            "KsatsSkill": "ksats_skill_node_profile.json",
            "KsatsTask": "ksats_task_node_profile.json",
            "DcwfCompetency": "dcwf_competency_node_profile.json",
            "Competency": "competency_node_profile.json",
            "Framework": "framework_node_profile.json",
            "FunctionalCommunity": "functional_community_node_profile.json",
            "WorkforceElement": "workforce_element_node_profile.json",
        }

        schema_file = label_to_schema.get(label)
        if schema_file and schema_file in self._schema_cache:
            return self._schema_cache[schema_file]
        return None

    def validate_node(self, node_data: Dict[str, Any]) -> None:
        """
        Validate a single node against its schema

        Args:
            node_data: Dictionary containing 'label' and 'properties' keys

        Raises:
            SchemaValidationError: If validation fails
        """
        if "label" not in node_data:
            raise SchemaValidationError("Node data must contain 'label' field")

        label = node_data["label"]
        schema = self.get_schema_for_label(label)

        if not schema:
            raise SchemaValidationError(f"No schema found for node label: {label}")

        try:
            validate(instance=node_data, schema=schema, resolver=self._resolver)
        except ValidationError as e:
            raise SchemaValidationError(
                f"Validation failed for {label} node: {e.message}", [str(e)]
            )

    def validate_nodes(self, nodes: List[Dict[str, Any]]) -> None:
        """
        Validate multiple nodes

        Args:
            nodes: List of node dictionaries

        Raises:
            SchemaValidationError: If any validation fails
        """
        errors = []

        for i, node in enumerate(nodes):
            try:
                self.validate_node(node)
            except SchemaValidationError as e:
                # If the exception has specific error details, use them
                # Otherwise, use the main exception message
                if e.errors:
                    errors.extend([f"Node {i+1}: {error}" for error in e.errors])
                else:
                    errors.append(f"Node {i+1}: {str(e)}")

        if errors:
            raise SchemaValidationError("Multiple validation errors", errors)


class PayloadValidator:
    """Validates operation payloads"""

    def __init__(self):
        self.node_validator = NodeSchemaValidator()

    def validate_create_nodes_payload(self, payload: Dict[str, Any]) -> None:
        """Validate create_nodes operation payload"""
        required_fields = ["operation", "nodes"]
        self._check_required_fields(payload, required_fields)

        if payload["operation"] != "create_nodes":
            raise SchemaValidationError("Operation must be 'create_nodes'")

        if not isinstance(payload["nodes"], list) or len(payload["nodes"]) == 0:
            raise SchemaValidationError("'nodes' must be a non-empty list")

        # Validate each node against its schema
        self.node_validator.validate_nodes(payload["nodes"])

    def validate_create_relationship_payload(self, payload: Dict[str, Any]) -> None:
        """Validate create_relationship operation payload"""
        required_fields = [
            "operation",
            "source_node",
            "destination_node",
            "relationship",
        ]
        self._check_required_fields(payload, required_fields)

        if payload["operation"] != "create_relationship":
            raise SchemaValidationError("Operation must be 'create_relationship'")

        # Validate both nodes
        self.node_validator.validate_node(payload["source_node"])
        self.node_validator.validate_node(payload["destination_node"])

        # Validate relationship structure
        self._validate_relationship(payload["relationship"])

    def validate_create_relationship_to_existing_payload(
        self, payload: Dict[str, Any]
    ) -> None:
        """Validate create_relationship_to_existing operation payload"""
        required_fields = [
            "operation",
            "new_node",
            "existing_node_reference",
            "relationship",
        ]
        self._check_required_fields(payload, required_fields)

        if payload["operation"] != "create_relationship_to_existing":
            raise SchemaValidationError(
                "Operation must be 'create_relationship_to_existing'"
            )

        # Validate new node
        self.node_validator.validate_node(payload["new_node"])

        # Validate existing node reference
        self._validate_existing_node_reference(payload["existing_node_reference"])

        # Validate relationship structure
        self._validate_relationship(payload["relationship"])

    def _check_required_fields(
        self, payload: Dict[str, Any], required_fields: List[str]
    ) -> None:
        """Check if all required fields are present"""
        missing_fields = [field for field in required_fields if field not in payload]
        if missing_fields:
            raise SchemaValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )

    def _validate_relationship(self, relationship: Dict[str, Any]) -> None:
        """Validate relationship structure"""
        if "edge_label" not in relationship:
            raise SchemaValidationError("Relationship must contain 'edge_label'")

        if (
            not isinstance(relationship["edge_label"], str)
            or not relationship["edge_label"].strip()
        ):
            raise SchemaValidationError("'edge_label' must be a non-empty string")

        # Validate direction if present
        if "direction" in relationship:
            valid_directions = [
                "from_source_to_destination",
                "from_destination_to_source",
                "from_existing_to_new",
                "from_new_to_existing",
            ]
            if relationship["direction"] not in valid_directions:
                raise SchemaValidationError(
                    f"Invalid direction. Must be one of: {', '.join(valid_directions)}"
                )

    def _validate_existing_node_reference(self, reference: Dict[str, Any]) -> None:
        """Validate existing node reference structure"""
        required_fields = ["label", "lookup_method", "lookup_value"]
        self._check_required_fields(reference, required_fields)

        valid_lookup_methods = ["by_id", "by_property"]
        if reference["lookup_method"] not in valid_lookup_methods:
            raise SchemaValidationError(
                f"Invalid lookup_method. Must be one of: {', '.join(valid_lookup_methods)}"
            )
