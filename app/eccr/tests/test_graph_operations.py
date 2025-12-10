import json
from unittest.mock import MagicMock, patch

import pytest
from django.test import TestCase
from eccr.utils.validation import PayloadValidator, SchemaValidationError
from rest_framework import status
from rest_framework.test import APIClient


class PayloadValidatorTests(TestCase):
    """Test cases for PayloadValidator"""

    def setUp(self):
        self.validator = PayloadValidator()

    def test_validate_create_nodes_payload_success(self):
        """Test successful validation of create_nodes payload"""
        payload = {
            "operation": "create_nodes",
            "description": "Test creation",
            "nodes": [
                {
                    "label": "DCWFFramework",
                    "properties": {"id": "DCWFF-001", "name": "Test Framework"},
                }
            ],
        }

        # Should not raise any exception
        try:
            self.validator.validate_create_nodes_payload(payload)
        except SchemaValidationError:
            self.fail(
                "validate_create_nodes_payload raised SchemaValidationError unexpectedly"
            )

    def test_validate_create_nodes_payload_missing_operation(self):
        """Test validation failure for missing operation field"""
        payload = {"description": "Test creation", "nodes": []}

        with self.assertRaises(SchemaValidationError) as context:
            self.validator.validate_create_nodes_payload(payload)

        self.assertIn("Missing required fields", str(context.exception))

    def test_validate_create_nodes_payload_wrong_operation(self):
        """Test validation failure for wrong operation type"""
        payload = {"operation": "wrong_operation", "nodes": []}

        with self.assertRaises(SchemaValidationError) as context:
            self.validator.validate_create_nodes_payload(payload)

        self.assertIn("Operation must be 'create_nodes'", str(context.exception))

    def test_validate_create_nodes_payload_empty_nodes(self):
        """Test validation failure for empty nodes list"""
        payload = {"operation": "create_nodes", "nodes": []}

        with self.assertRaises(SchemaValidationError) as context:
            self.validator.validate_create_nodes_payload(payload)

        self.assertIn("must be a non-empty list", str(context.exception))

    def test_validate_create_relationship_payload_success(self):
        """Test successful validation of create_relationship payload"""
        payload = {
            "operation": "create_relationship",
            "source_node": {
                "label": "AdvancedWorkRole",
                "properties": {
                    "id": "AdvancedWorkRole-103",
                    "name": "Senior Cybersecurity Architect",
                },
            },
            "destination_node": {
                "label": "KsatsKnowledge",
                "properties": {
                    "id": "KSAT-107",
                    "name": "Enterprise Architecture Frameworks",
                },
            },
            "relationship": {"edge_label": "REQUIRES", "properties": {}},
        }

        try:
            self.validator.validate_create_relationship_payload(payload)
        except SchemaValidationError:
            self.fail(
                "validate_create_relationship_payload raised SchemaValidationError unexpectedly"
            )

    def test_validate_create_relationship_to_existing_payload_success(self):
        """Test successful validation of create_relationship_to_existing payload"""
        payload = {
            "operation": "create_relationship_to_existing",
            "new_node": {
                "label": "KsatsAbility",
                "properties": {
                    "id": "KSAT-108",
                    "name": "Threat Intelligence Analysis",
                },
            },
            "existing_node_reference": {
                "label": "Job",
                "lookup_method": "by_id",
                "lookup_value": "WR-AN-EX-001",
            },
            "relationship": {
                "edge_label": "SUPPORTS",
                "direction": "from_existing_to_new",
            },
        }

        try:
            self.validator.validate_create_relationship_to_existing_payload(payload)
        except SchemaValidationError:
            self.fail(
                "validate_create_relationship_to_existing_payload raised SchemaValidationError unexpectedly"
            )


class GraphOperationsAPITests(TestCase):
    """Test cases for Graph Operations API endpoints"""

    def setUp(self):
        self.client = APIClient()

    @patch("eccr.services.graph_service.graph_service.create_nodes")
    def test_create_nodes_endpoint_success(self, mock_create_nodes):
        """Test successful node creation via API"""
        mock_create_nodes.return_value = {
            "operation": "create_nodes",
            "status": "success",
            "nodes_created": 1,
            "node_ids": ["DCWFF-002"],
        }

        payload = {
            "operation": "create_nodes",
            "description": "Create test nodes",
            "nodes": [
                {
                    "label": "DCWFFramework",
                    "properties": {"id": "DCWFF-002", "name": "Test Framework"},
                }
            ],
        }

        response = self.client.post("/api/nodes/", data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["nodes_created"], 1)
        mock_create_nodes.assert_called_once_with(payload)

    @patch("eccr.services.graph_service.graph_service.create_relationship")
    def test_create_relationship_endpoint_success(self, mock_create_relationship):
        """Test successful relationship creation via API"""
        mock_create_relationship.return_value = {
            "operation": "create_relationship",
            "status": "success",
            "source_node_id": "AdvancedWorkRole-103",
            "destination_node_id": "KSAT-107",
        }

        payload = {
            "operation": "create_relationship",
            "source_node": {
                "label": "AdvancedWorkRole",
                "properties": {
                    "id": "AdvancedWorkRole-103",
                    "name": "Senior Cybersecurity Architect",
                },
            },
            "destination_node": {
                "label": "KsatsKnowledge",
                "properties": {
                    "id": "KSAT-107",
                    "name": "Enterprise Architecture Frameworks",
                },
            },
            "relationship": {"edge_label": "REQUIRES"},
        }

        response = self.client.post("/api/relationships/", data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "success")
        mock_create_relationship.assert_called_once_with(payload)

    @patch("eccr.services.graph_service.graph_service.create_relationship_to_existing")
    def test_create_relationship_to_existing_endpoint_success(self, mock_create_rel):
        """Test successful relationship to existing node creation via API"""
        mock_create_rel.return_value = {
            "operation": "create_relationship_to_existing",
            "status": "success",
            "new_node_id": "KSAT-108",
        }

        payload = {
            "operation": "create_relationship_to_existing",
            "new_node": {
                "label": "KsatsAbility",
                "properties": {
                    "id": "KSAT-108",
                    "name": "Threat Intelligence Analysis",
                },
            },
            "existing_node_reference": {
                "label": "Job",
                "lookup_method": "by_id",
                "lookup_value": "WR-AN-EX-001",
            },
            "relationship": {"edge_label": "SUPPORTS"},
        }

        response = self.client.post(
            "/api/relationships/existing/", data=payload, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "success")
        mock_create_rel.assert_called_once_with(payload)

    def test_create_nodes_endpoint_validation_error(self):
        """Test API endpoint returns 400 for validation errors"""
        payload = {"operation": "wrong_operation", "nodes": []}

        response = self.client.post("/api/nodes/", data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Validation Error")

    @patch("eccr.neo4j_driver.get_driver")
    def test_health_endpoint_success(self, mock_get_driver):
        """Test health endpoint when database is accessible"""
        mock_driver = MagicMock()
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_record = MagicMock()

        mock_get_driver.return_value = mock_driver
        mock_driver.session.return_value.__enter__.return_value = mock_session
        mock_session.run.return_value = mock_result
        mock_result.single.return_value = mock_record
        mock_record.__getitem__.return_value = 1

        response = self.client.get("/api/health/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "healthy")

    @patch("eccr.neo4j_driver.get_driver")
    def test_health_endpoint_failure(self, mock_get_driver):
        """Test health endpoint when database is not accessible"""
        mock_get_driver.side_effect = Exception("Connection failed")

        response = self.client.get("/api/health/")

        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertEqual(response.data["status"], "unhealthy")
