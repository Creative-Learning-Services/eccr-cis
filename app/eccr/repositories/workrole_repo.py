from typing import Any, Dict, Optional

from eccr.neo4j_driver import get_driver

WORKROLE_RETURN = (
    "w.id as id, w.name as name, w.description as description, w.NISTID as NISTID, "
    "w.type as type_label, w.typeURI as type_uri, w.DCWFID as DCWFID, "
    "w.competencyStatement as competency_statement, w.domain as domain, "
    "w.PROFILE as PROFILE, w.conformsTo as conformsTo"
)


def record_to_dict(record) -> Dict[str, Any]:
    return {k: record.get(k) for k in record.keys()}


def list_workroles(limit: int = 5, skip: int = 0) -> Dict[str, Any]:
    # Query WorkRole competency types (AdvancedWorkRole, IntermediateWorkRole,
    # BasicWorkRole)
    cypher = f"""
    MATCH (w:Competency)
    WHERE w:AdvancedWorkRole OR w:IntermediateWorkRole OR w:BasicWorkRole
    RETURN {WORKROLE_RETURN}
    ORDER BY w.name
    SKIP $skip LIMIT $limit
    """

    count_cypher = """
    MATCH (w:Competency)
    WHERE w:AdvancedWorkRole OR w:IntermediateWorkRole OR w:BasicWorkRole
    RETURN count(w) as total
    """
    driver = get_driver()
    with driver.session() as session:
        total = session.run(count_cypher).single()["total"]
        results = session.run(cypher, skip=skip, limit=limit)
        data = [record_to_dict(r) for r in results]
        return {"results": data, "total": total}


def get_workrole(workrole_id: str) -> Optional[Dict[str, Any]]:
    cypher = f"""
    MATCH (w:Competency {{id: $workrole_id}})
    WHERE w:AdvancedWorkRole OR w:IntermediateWorkRole OR w:BasicWorkRole
    RETURN {WORKROLE_RETURN}
    LIMIT 1
    """
    driver = get_driver()
    with driver.session() as session:
        rec = session.run(cypher, workrole_id=workrole_id).single()
        return record_to_dict(rec) if rec else None
