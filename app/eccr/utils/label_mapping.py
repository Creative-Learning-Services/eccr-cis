import json
import os
from typing import Any, Dict, List, Optional, Tuple

from django.conf import settings


class LabelMappingManager:
    """Manages node label mappings for two-label pattern creation"""

    def __init__(self):
        self.config_path = os.path.join(
            settings.BASE_DIR, "eccr", "schemas", "label_mapping_config.json"
        )
        self._config = None
        self._load_config()

    def _load_config(self):
        """Load the label mapping configuration"""
        try:
            with open(self.config_path, "r") as f:
                self._config = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Label mapping configuration not found: {self.config_path}"
            )
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in label mapping configuration: {e}")

    def get_labels_for_single_label(self, single_label: str) -> List[str]:
        """
        Get the list of labels for a given single label input from REST payload.
        Maps single label to [specific_label, superset_label] pattern.

        Args:
            single_label: The single label from REST payload (e.g., 'DCWFFramework', 'Job', etc.)

        Returns:
            List of labels to apply to the node in order [specific, superset]
        """
        if not self._config:
            return [single_label]  # Fallback to single label

        mapping = self._config.get("specific_type_mappings", {}).get(single_label)
        if not mapping:
            return [single_label]  # Fallback to single label

        specific_label = mapping["specific_label"]
        superset_label = mapping["superset_label"]

        # Return in order: specific_label, superset_label (as seen in cypher: DCWFFramework:Framework)
        # Only add superset if it's different from specific
        if specific_label == superset_label:
            return [specific_label]
        else:
            return [specific_label, superset_label]

    def get_schema_file_for_single_label(self, single_label: str) -> Optional[str]:
        """
        Get the schema file for a given single label

        Args:
            single_label: The single label from REST payload

        Returns:
            Schema filename or None if not found
        """
        if not self._config:
            return None

        mapping = self._config.get("specific_type_mappings", {}).get(single_label)
        return mapping.get("schema_file") if mapping else None

    def get_superset_label_for_single_label(self, single_label: str) -> str:
        """
        Get the superset label for a given single label

        Args:
            single_label: The single label from REST payload

        Returns:
            Superset label (e.g., 'Framework', 'Competency')
        """
        if not self._config:
            return single_label

        mapping = self._config.get("specific_type_mappings", {}).get(single_label)
        return mapping.get("superset_label", single_label) if mapping else single_label

    def get_specific_label_for_single_label(self, single_label: str) -> str:
        """
        Get the specific label for a given single label

        Args:
            single_label: The single label from REST payload

        Returns:
            Specific label (same as input in most cases)
        """
        if not self._config:
            return single_label

        mapping = self._config.get("specific_type_mappings", {}).get(single_label)
        return mapping.get("specific_label", single_label) if mapping else single_label

    def is_valid_single_label(self, single_label: str) -> bool:
        """
        Check if a single label is valid

        Args:
            single_label: The single label to validate

        Returns:
            True if valid, False otherwise
        """
        if not self._config:
            return True  # Allow all if config not available

        return single_label in self._config.get("specific_type_mappings", {})

    def get_available_single_labels(self) -> List[str]:
        """
        Get all available single labels

        Returns:
            List of available single labels
        """
        if not self._config:
            return []

        return list(self._config.get("specific_type_mappings", {}).keys())

    def get_single_labels_for_superset_label(self, superset_label: str) -> List[str]:
        """
        Get all single labels that belong to a superset label

        Args:
            superset_label: Superset label (e.g., 'Framework', 'Competency')

        Returns:
            List of single labels
        """
        if not self._config:
            return []

        single_labels = []
        for single_label, mapping in self._config.get(
            "specific_type_mappings", {}
        ).items():
            if mapping.get("superset_label") == superset_label:
                single_labels.append(single_label)

        return single_labels


# Global instance
label_mapping_manager = LabelMappingManager()
