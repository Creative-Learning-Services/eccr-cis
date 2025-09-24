from typing import Dict, Any, Optional, List
from eccr.neo4j_driver import get_driver

# Projection constants keep responses consistent
FRAMEWORK_RETURN = (
    "f.id as id, f.name as name, f.description as description, "
    "f.authoritativeSource as authoritative_source, f.competencyDefinition as competency_definition, "
    "f.PROFILE as PROFILE, f.domain as domain, f.conformsTo as conformsTo"
)


def record_to_dict(record) -> Dict[str, Any]:
    """Convert a Neo4j record to a dictionary"""
    return {k: record.get(k) for k in record.keys()}


def list_frameworks(limit: int = 20, skip: int = 0) -> Dict[str, Any]:
    """
    List all frameworks with optional pagination.

    Args:
        limit: Maximum number of results to return
        skip: Number of results to skip (for pagination)
    """

    cypher = f"""
    MATCH (f:Framework)
    OPTIONAL MATCH (f)-[:HAS_SUBFRAMEWORK*]->(sub:Framework)
    WITH f, count(sub) as subframework_count
    RETURN {FRAMEWORK_RETURN}, subframework_count
    ORDER BY f.name
    SKIP $skip LIMIT $limit
    """

    count_cypher = """
    MATCH (f:Framework)
    RETURN count(f) as total
    """

    driver = get_driver()
    with driver.session() as session:
        total = session.run(count_cypher).single()["total"]
        results = session.run(cypher, skip=skip, limit=limit)
        data = [record_to_dict(r) for r in results]
        return {"results": data, "total": total}


def get_framework(framework_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a single framework by its unique identifier (id)
    Args:
        framework_id: Unique identifier of the framework
    """

    cypher = f"""
    MATCH (f:Framework {{id: $framework_id}})
    OPTIONAL MATCH (f)-[:HAS_SUBFRAMEWORK*]->(sub:Framework)
    WITH f, count(sub) as subframework_count
    RETURN {FRAMEWORK_RETURN}, subframework_count
    LIMIT 1
    """
    driver = get_driver()
    with driver.session() as session:
        rec = session.run(cypher, framework_id=framework_id).single()
        return record_to_dict(rec) if rec else None


def get_framework_with_competencies(
    framework_id: str, limit: int = 100, skip: int = 0
) -> Optional[Dict[str, Any]]:
    """
    retrieve a framework and its associated competencies with pagination
    Args:
        framework_id: Unique identifier of the framework
        limit: Maximum number of competencies to return
        skip: Number of competencies to skip (for pagination)
    """

    framework_cypher = f"""
    MATCH (f:Framework {{id: $framework_id}})
    RETURN {FRAMEWORK_RETURN}
    LIMIT 1
    """

    competencies_cypher = """
    MATCH (f:Framework {id: $framework_id})-[:HAS_SUBFRAMEWORK*]->(job:Job:Competency)
    RETURN job.id as id, job.name as name, job.description as description, 
           job.domain as domain, job.type as type_label
    ORDER BY job.name
    SKIP $skip LIMIT $limit
    """

    count_cypher = """
    MATCH (:Framework {id: $framework_id})-[:HAS_SUBFRAMEWORK*]->(job:Job:Competency)
    RETURN count(job) as total_competencies
    """

    driver = get_driver()
    with driver.session() as session:
        fw = session.run(framework_cypher, framework_id=framework_id).single()
        if not fw:
            return None
        fw_dict = record_to_dict(fw)
        total_competencies = session.run(
            count_cypher, framework_id=framework_id
        ).single()["total_competencies"]
        comps = session.run(
            competencies_cypher, framework_id=framework_id, skip=skip, limit=limit
        )
        comp_list = [record_to_dict(r) for r in comps]
        return {
            "framework": fw_dict,
            "competencies": comp_list,
            "competency_pagination": {
                "total": total_competencies,
                "limit": limit,
                "skip": skip,
            },
        }
