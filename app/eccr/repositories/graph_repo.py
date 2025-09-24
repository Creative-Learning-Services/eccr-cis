from typing import Dict, Any, List, Optional, Tuple
import logging
from eccr.neo4j_driver import get_driver

logger = logging.getLogger(__name__)


def build_cypher_properties(properties: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    """
    Build Cypher property string and parameters from a properties dictionary

    Args:
        properties: Dictionary of node properties

    Returns:
        Tuple of (property_string, parameters_dict)
    """
    if not properties:
        return "", {}

    # Create parameter placeholders
    prop_parts = []
    params = {}

    for key, value in properties.items():
        param_key = f"prop_{key}"
        prop_parts.append(f"{key}: ${param_key}")
        params[param_key] = value

    property_string = "{" + ", ".join(prop_parts) + "}"
    return property_string, params


def create_nodes_batch(nodes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Create multiple nodes in a batch operation

    Args:
        nodes: List of node dictionaries with 'label' and 'properties'

    Returns:
        Dictionary with operation results
    """
    driver = get_driver()

    with driver.session() as session:
        created_nodes = []

        # Create each node individually for better error handling
        for node in nodes:
            label = node["label"]
            properties = node["properties"]

            prop_string, params = build_cypher_properties(properties)

            cypher = f"""
            CREATE (n:{label} {prop_string})
            RETURN n
            """

            result = session.run(cypher, **params)
            record = result.single()

            if record:
                created_node = dict(record["n"])
                created_nodes.append({"label": label, "properties": created_node})
                logger.info(
                    f"Created {label} node with id: {properties.get('id', 'unknown')}"
                )
            else:
                raise Exception(f"Failed to create {label} node")

    return {"nodes_created": len(created_nodes), "nodes": created_nodes}


def create_node_with_relationship(
    source_node: Dict[str, Any],
    destination_node: Dict[str, Any],
    relationship: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Create two nodes and a relationship between them

    Args:
        source_node: Source node dictionary
        destination_node: Destination node dictionary
        relationship: Relationship dictionary

    Returns:
        Dictionary with operation results
    """
    driver = get_driver()

    with driver.session() as session:
        # Extract data
        source_label = source_node["label"]
        source_props = source_node["properties"]
        dest_label = destination_node["label"]
        dest_props = destination_node["properties"]
        edge_label = relationship["edge_label"]
        rel_props = relationship.get("properties", {})

        # Build property strings
        source_prop_string, source_params = build_cypher_properties(source_props)
        dest_prop_string, dest_params = build_cypher_properties(dest_props)
        rel_prop_string, rel_params = build_cypher_properties(rel_props)

        # Combine all parameters with prefixes to avoid conflicts
        all_params = {}
        for key, value in source_params.items():
            all_params[f"source_{key}"] = value
        for key, value in dest_params.items():
            all_params[f"dest_{key}"] = value
        for key, value in rel_params.items():
            all_params[f"rel_{key}"] = value

        # Update property strings with prefixed parameters
        source_prop_string = source_prop_string.replace("$prop_", "$source_prop_")
        dest_prop_string = dest_prop_string.replace("$prop_", "$dest_prop_")
        rel_prop_string = rel_prop_string.replace("$prop_", "$rel_prop_")

        # Build Cypher query
        cypher = f"""
        CREATE (source:{source_label} {source_prop_string})
        CREATE (dest:{dest_label} {dest_prop_string})
        CREATE (source)-[r:{edge_label} {rel_prop_string}]->(dest)
        RETURN source, dest, r
        """

        result = session.run(cypher, **all_params)
        record = result.single()

        if record:
            created_source = dict(record["source"])
            created_dest = dict(record["dest"])
            created_rel = dict(record["r"])

            logger.info(
                f"Created nodes and relationship: {source_label} -[{edge_label}]-> {dest_label}"
            )

            return {
                "source_node": {"label": source_label, "properties": created_source},
                "destination_node": {"label": dest_label, "properties": created_dest},
                "relationship": {"type": edge_label, "properties": created_rel},
            }
        else:
            raise Exception("Failed to create nodes and relationship")


def find_existing_node(
    label: str, lookup_method: str, lookup_value: str
) -> Optional[Dict[str, Any]]:
    """
    Find an existing node in the graph

    Args:
        label: Node label
        lookup_method: How to find the node ('by_id' or 'by_property')
        lookup_value: Value to search for

    Returns:
        Node dictionary if found, None otherwise
    """
    driver = get_driver()

    with driver.session() as session:
        if lookup_method == "by_id":
            cypher = f"MATCH (n:{label} {{id: $lookup_value}}) RETURN n LIMIT 1"
        elif lookup_method == "by_property":
            # For now, assume searching by 'name' property
            # This could be extended to support arbitrary properties
            cypher = f"MATCH (n:{label} {{name: $lookup_value}}) RETURN n LIMIT 1"
        else:
            raise ValueError(f"Unsupported lookup method: {lookup_method}")

        result = session.run(cypher, lookup_value=lookup_value)
        record = result.single()

        if record:
            return {"label": label, "properties": dict(record["n"])}
        return None


def create_node_and_relate_to_existing(
    new_node: Dict[str, Any],
    existing_node_ref: Dict[str, Any],
    relationship: Dict[str, Any],
    validation_config: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """
    Create a new node and relate it to an existing node

    Args:
        new_node: New node dictionary
        existing_node_ref: Reference to existing node
        relationship: Relationship dictionary
        validation_config: Validation configuration

    Returns:
        Dictionary with operation results
    """
    driver = get_driver()
    validation_config = validation_config or {}

    with driver.session() as session:
        # Extract data
        new_label = new_node["label"]
        new_props = new_node["properties"]
        existing_label = existing_node_ref["label"]
        lookup_method = existing_node_ref["lookup_method"]
        lookup_value = existing_node_ref["lookup_value"]
        edge_label = relationship["edge_label"]
        rel_props = relationship.get("properties", {})
        direction = relationship.get("direction", "from_existing_to_new")

        # Build property strings
        new_prop_string, new_params = build_cypher_properties(new_props)
        rel_prop_string, rel_params = build_cypher_properties(rel_props)

        # Combine parameters with prefixes
        all_params = {"lookup_value": lookup_value}
        for key, value in new_params.items():
            all_params[f"new_{key}"] = value
        for key, value in rel_params.items():
            all_params[f"rel_{key}"] = value

        # Update property strings with prefixed parameters
        new_prop_string = new_prop_string.replace("$prop_", "$new_prop_")
        rel_prop_string = rel_prop_string.replace("$prop_", "$rel_prop_")

        # Build lookup condition
        if lookup_method == "by_id":
            lookup_condition = f"existing.id = $lookup_value"
        elif lookup_method == "by_property":
            lookup_condition = f"existing.name = $lookup_value"
        else:
            raise ValueError(f"Unsupported lookup method: {lookup_method}")

        # Build relationship direction
        if direction == "from_existing_to_new":
            rel_pattern = f"(existing)-[r:{edge_label} {rel_prop_string}]->(new_node)"
        elif direction == "from_new_to_existing":
            rel_pattern = f"(new_node)-[r:{edge_label} {rel_prop_string}]->(existing)"
        else:
            # Default to from existing to new
            rel_pattern = f"(existing)-[r:{edge_label} {rel_prop_string}]->(new_node)"

        # Build Cypher query
        cypher = f"""
        MATCH (existing:{existing_label}) WHERE {lookup_condition}
        CREATE (new_node:{new_label} {new_prop_string})
        CREATE {rel_pattern}
        RETURN existing, new_node, r
        """

        result = session.run(cypher, **all_params)
        record = result.single()

        if record:
            existing_node = dict(record["existing"])
            created_new_node = dict(record["new_node"])
            created_rel = dict(record["r"])

            logger.info(
                f"Created {new_label} node and related to existing {existing_label}"
            )

            return {
                "new_node": {"label": new_label, "properties": created_new_node},
                "existing_node": {"label": existing_label, "properties": existing_node},
                "relationship": {
                    "type": edge_label,
                    "properties": created_rel,
                    "direction": direction,
                },
            }
        else:
            raise Exception(
                f"Failed to create relationship - existing node not found or creation failed"
            )
