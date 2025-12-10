import uuid

from django.test import TestCase
from eccr.neo4j_driver import get_driver
from eccr.repositories.competency_repo import get_competency, list_competencies
from eccr.repositories.framework_repo import (
    get_framework_with_competencies,
    list_frameworks,
)
from eccr.repositories.workrole_repo import list_workroles


class RepositoryTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        driver = get_driver()
        # Insert a small subgraph for tests (namespaced by a test tag)
        cls.test_tag = str(uuid.uuid4())[:8]
        with driver.session() as session:
            # Purge existing nodes for deterministic test results
            session.execute_write(
                lambda tx: tx.run("MATCH (n:Framework) DETACH DELETE n")
            )
            session.execute_write(
                lambda tx: tx.run("MATCH (n:Competency) DETACH DELETE n")
            )
            session.execute_write(
                lambda tx: tx.run("MATCH (n:WorkRole) DETACH DELETE n")
            )
            session.execute_write(
                lambda tx, tag: tx.run(
                    """
                    CREATE (f:Framework {id:$f_id,name:$f_name,description:'Test Framework', authoritative_source:'Source', resource_association:[], association:'', PROFILE:[]})
                    WITH f
                    CREATE (c:Job:Competency {id:$c_id,name:$c_name,description:'Desc',competency_statement:[],competency_framework:[],resource_association:[],reference_code:'R',competency_level:'L',type_label:'TL',type_uri:'URI',ksat_type:'',PROFILE:[],domain:'Test'})
                    CREATE (f)-[:HAS_SUBFRAMEWORK]->(c)
                    CREATE (w:WorkRole:Competency:AdvancedWorkRole {id:$w_id,name:$w_name,description:'WR',NISTID:'N',authoritativeSource:'AS',resourceAssociation:[],competencyDefinition:[],classification:'CL',markings:[],LocationName:'Loc',JobSalary:'100',JobTravelCode:'JTC',PromotionPotential:'P',careerpathway:[],type_uri:'uri',PROFILE:[],domain:'WR'})
                    """,
                    f_id=f"fw-{cls.test_tag}",
                    f_name=f"Framework {cls.test_tag}",
                    c_id=f"comp-{cls.test_tag}",
                    c_name=f"Competency {cls.test_tag}",
                    w_id=f"wr-{cls.test_tag}",
                    w_name=f"WorkRole {cls.test_tag}",
                ),
                cls.test_tag,
            )

    @classmethod
    def tearDownClass(cls):
        driver = get_driver()
        with driver.session() as session:
            session.execute_write(
                lambda tx, tag: tx.run(
                    """
                    MATCH (n) WHERE n.id IN [$f,$c,$w] DETACH DELETE n
                    """,
                    f=f"fw-{cls.test_tag}",
                    c=f"comp-{cls.test_tag}",
                    w=f"wr-{cls.test_tag}",
                ),
                cls.test_tag,
            )
        super().tearDownClass()

    def test_list_competencies(self):
        data = list_competencies(limit=5, skip=0)
        assert "results" in data and "total" in data
        assert any(r["name"].startswith("Competency") for r in data["results"])

    def test_get_competency(self):
        comp = get_competency(f"comp-{self.test_tag}")
        assert comp is not None
        assert comp["id"] == f"comp-{self.test_tag}"

    def test_list_frameworks_and_competency_count(self):
        data = list_frameworks(limit=5, skip=0)
        assert "results" in data
        target = next(
            (f for f in data["results"] if f["id"] == f"fw-{self.test_tag}"), None
        )
        assert target is not None
        assert (
            target.get("subframework_count") == 0
        )  # No subframeworks in our test data

    def test_framework_with_competencies(self):
        fw = get_framework_with_competencies(f"fw-{self.test_tag}")
        assert fw is not None
        assert fw["framework"]["id"] == f"fw-{self.test_tag}"
        assert fw["competencies"] and fw["competencies"][0]["id"].startswith("comp-")

    def test_list_workroles(self):
        data = list_workroles(limit=5, skip=0)
        assert any(r["id"] == f"wr-{self.test_tag}" for r in data["results"])
