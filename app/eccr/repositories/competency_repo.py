from typing import Any, Dict, Optional

from eccr.neo4j_driver import get_driver

# Projection constants keep responses consistent
COMPETENCY_RETURN = (
    "n.id as id, n.name as name, n.description as description, "
    "n.competencyStatement as competency_statement, n.domain as domain, "
    "n.type as type_label, n.typeURI as type_uri, "
    "n.PROFILE as PROFILE, n.conformsTo as conformsTo"
)


def record_to_dict(record) -> Dict[str, Any]:
    """Convert a Neo4j record to a dictionary"""
    return {k: record.get(k) for k in record.keys()}


def list_competencies(
    limit: int = 20, skip: int = 0, filters: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    List competencies with optional filtering and pagination
    Args:
        limit: Maximum number of results to return
        skip: Number of results to skip (for pagination)
        filters: Optional dictionary of filters (e.g., name_contains, domain)
    """

    filters = filters or {}
    where_clauses = []
    params: Dict[str, Any] = {"limit": limit, "skip": skip}

    if name := filters.get("name_contains"):
        where_clauses.append("n.name CONTAINS $name_contains")
        params["name_contains"] = name
    if domain := filters.get("domain"):
        where_clauses.append("n.domain = $domain")
        params["domain"] = domain

    where_block = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""

    cypher = f"""
    MATCH (n:Competency)
    {where_block}
    RETURN {COMPETENCY_RETURN}
    ORDER BY n.name
    SKIP $skip LIMIT $limit
    """

    count_cypher = f"""
    MATCH (n:Competency)
    {where_block}
    RETURN count(n) as total
    """

    driver = get_driver()
    with driver.session() as session:
        total = session.run(count_cypher, **params).single()["total"]
        results = session.run(cypher, **params)
        data = [record_to_dict(r) for r in results]
        return {"results": data, "total": total}


def get_competency(competency_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a single competency by its unique identifier (id)
    Args:
        competency_id: Unique identifier of the competency
    """
    # Query all types of competency nodes (Job, WorkRole hierarchies, KSAT
    # types)
    cypher = f"""
    MATCH (n:Competency {{id: $competency_id}})
    RETURN {COMPETENCY_RETURN}
    LIMIT 1
    """
    driver = get_driver()
    with driver.session() as session:
        rec = session.run(cypher, competency_id=competency_id).single()
        return record_to_dict(rec) if rec else None
