import json
import os
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch


class GraphOperationsIntegrationTests(TestCase):
    """Integration tests using the actual payload examples"""

    def setUp(self):
        self.client = APIClient()
        self.test_data_dir = os.path.join(os.path.dirname(__file__), "data")

    def load_test_payload(self, filename):
        """Load test payload from JSON file"""
        filepath = os.path.join(self.test_data_dir, filename)
        with open(filepath, "r") as f:
            return json.load(f)

    @patch("eccr.repositories.graph_repo.get_driver")
    def test_create_nodes_only_payload(self, mock_get_driver):
        """Test the create_nodes_only.json payload"""
        # Mock Neo4j driver
        mock_driver = self._setup_mock_driver(mock_get_driver)

        payload = self.load_test_payload("create_nodes_only.json")

        response = self.client.post("/api/nodes/", data=payload, format="json")

        # Should return 201 Created on success
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["operation"], "create_nodes")
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["nodes_created"], 4)  # 4 nodes in the test file

    @patch("eccr.repositories.graph_repo.get_driver")
    def test_create_node_to_node_relationship_payload(self, mock_get_driver):
        """Test the create_node_to_node_relationship.json payload"""
        # Mock Neo4j driver
        mock_driver = self._setup_mock_driver(mock_get_driver)

        payload = self.load_test_payload("create_node_to_node_relationship.json")

        response = self.client.post("/api/relationships/", data=payload, format="json")

        # Should return 201 Created on success
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["operation"], "create_relationship")
        self.assertEqual(response.data["status"], "success")
        self.assertIn("source_node_id", response.data)
        self.assertIn("destination_node_id", response.data)

    @patch("eccr.repositories.graph_repo.get_driver")
    @patch("eccr.repositories.graph_repo.find_existing_node")
    def test_create_node_relate_to_existing_payload(
        self, mock_find_existing, mock_get_driver
    ):
        """Test the create_node_relate_to_existing.json payload"""
        # Mock Neo4j driver
        mock_driver = self._setup_mock_driver(mock_get_driver)

        # Mock existing node found
        mock_find_existing.return_value = {
            "label": "Job",
            "properties": {"id": "WR-AN-EX-001", "name": "Exploitation Analyst"},
        }

        payload = self.load_test_payload("create_node_relate_to_existing.json")

        response = self.client.post(
            "/api/relationships/existing/", data=payload, format="json"
        )

        # Should return 201 Created on success
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["operation"], "create_relationship_to_existing")
        self.assertEqual(response.data["status"], "success")
        self.assertIn("new_node_id", response.data)
        self.assertIn("existing_node_reference", response.data)

    def test_create_nodes_validation_error(self):
        """Test validation error with invalid payload"""
        invalid_payload = {
            "operation": "create_nodes",
            "nodes": [
                {
                    "label": "InvalidLabel",  # No schema for this label
                    "properties": {"id": "test-001"},
                }
            ],
        }

        response = self.client.post("/api/nodes/", data=invalid_payload, format="json")

        # Should return 400 Bad Request for validation error
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Validation Error")
        # Check that validation errors contain information about invalid schema
        self.assertIn("errors", response.data)
        error_text = str(response.data["errors"])
        self.assertIn("No schema found", error_text)

    def test_missing_required_fields(self):
        """Test validation error for missing required fields"""
        invalid_payload = {
            "operation": "create_nodes"
            # Missing 'nodes' field
        }

        response = self.client.post("/api/nodes/", data=invalid_payload, format="json")

        # Should return 400 Bad Request for validation error
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Validation Error")
        self.assertIn("Missing required fields", response.data["message"])

    def _setup_mock_driver(self, mock_get_driver):
        """Setup a mock Neo4j driver for testing"""
        from unittest.mock import MagicMock

        mock_driver = MagicMock()
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_record = MagicMock()

        # Setup the mock chain
        mock_get_driver.return_value = mock_driver
        mock_driver.session.return_value.__enter__.return_value = mock_session
        mock_session.run.return_value = mock_result
        mock_result.single.return_value = mock_record

        # Mock node properties to be returned
        mock_record.__getitem__.side_effect = lambda key: {
            "n": {"id": "test-id", "name": "Test Node"},
            "source": {"id": "source-id", "name": "Source Node"},
            "dest": {"id": "dest-id", "name": "Dest Node"},
            "existing": {"id": "existing-id", "name": "Existing Node"},
            "new_node": {"id": "new-id", "name": "New Node"},
            "r": {"type": "TEST_RELATIONSHIP"},
        }.get(key, {})

        return mock_driver
