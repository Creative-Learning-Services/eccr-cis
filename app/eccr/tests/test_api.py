import uuid

from django.test import TestCase
from django.urls import reverse
from eccr.neo4j_driver import get_driver
from rest_framework.test import APIClient


class APITests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tag = uuid.uuid4().hex[:8]
        cls.f_id = f"DCWFF-{cls.tag}"
        cls.job_id = f"WR-JOB-{cls.tag}"
        cls.awr_id = f"AdvancedWorkRole-{cls.tag}"
        cls.ksat_id = f"KSAT-{cls.tag}"
        print(f"Creating test entities with tag: {cls.tag}")
        print(f"Framework ID: {cls.f_id}")
        print(f"Job Competency ID: {cls.job_id}")
        driver = get_driver()
        with driver.session() as session:
            # Purge existing nodes for deterministic test behavior (WARNING:
            # destructive; acceptable in test environment)
            session.execute_write(
                lambda tx: tx.run("MATCH (n:Framework) DETACH DELETE n")
            )
            session.execute_write(
                lambda tx: tx.run("MATCH (n:Competency) DETACH DELETE n")
            )
            session.execute_write(
                lambda tx, params: tx.run(
                    """
                    CREATE (f:DCWFFramework:Framework {
                        id: $f_id,
                        name: $f_name,
                        description: 'Test DCWF Framework',
                        authoritativeSource: 'https://test.mil/dcwf-framework',
                        competencyDefinition: ['CD-TEST-001'],
                        PROFILE: ['Framework', 'DCWFFramework'],
                        domain: 'DCWF',
                        conformsTo: 'SCD 1.0'
                    })

                    CREATE (job:Job:Competency {
                        id: $job_id,
                        name: $job_name,
                        description: 'Test Job Competency',
                        competencyStatement: 'Test job competency statement',
                        type: 'Job',
                        typeURI: 'https://ksat.nist.gov/Job',
                        PROFILE: ['job', 'competency'],
                        domain: 'DCWF',
                        conformsTo: 'SCD 1.0'
                    })

                    CREATE (awr:AdvancedWorkRole:Competency {
                        id: $awr_id,
                        name: $awr_name,
                        description: 'Test Advanced Work Role',
                        competencyStatement: 'Test advanced work role competency',
                        type: 'Advanced Work Role',
                        typeURI: 'https://ksat.nist.gov/AdvancedWorkRole',
                        NISTID: ['NIST-TEST'],
                        DCWFID: ['TEST-AWR'],
                        PROFILE: ['work role', 'competency'],
                        domain: 'DCWF',
                        conformsTo: 'SCD 1.0'
                    })

                    CREATE (ksat:KSATSSkill:Competency {
                        id: $ksat_id,
                        name: $ksat_name,
                        description: 'Test KSAT Skill',
                        competencyStatement: 'Test KSAT skill competency',
                        type: 'Skill',
                        typeURI: 'https://ksat.nist.gov/KSAT/Skill',
                        NISTID: ['NIST-TEST'],
                        DCWFID: ['TEST-KSAT'],
                        PROFILE: ['ksats', 'competency', 'skill'],
                        domain: 'DCWF',
                        conformsTo: 'SCD 1.0'
                    })

                    // Create relationships matching init.cypher structure
                    CREATE (job)-[:REQUIRES]->(awr)
                    CREATE (awr)-[:REQUIRES_COMPETENCY]->(ksat)
                    """,
                    **params,
                ),
                {
                    "f_id": cls.f_id,
                    "f_name": f"Test DCWF Framework {cls.tag}",
                    "job_id": cls.job_id,
                    "job_name": f"Test Job {cls.tag}",
                    "awr_id": cls.awr_id,
                    "awr_name": f"Test Advanced Work Role {cls.tag}",
                    "ksat_id": cls.ksat_id,
                    "ksat_name": f"Test KSAT Skill {cls.tag}",
                },
            )
            print(f"Test entities created successfully")

            # Verify entities were created
            frameworks = session.run("MATCH (f:Framework) RETURN f.id, f.name").data()
            competencies = session.run(
                "MATCH (c:Competency) RETURN c.id, c.name"
            ).data()
            print(f"Created frameworks: {frameworks}")
            print(f"Created competencies: {competencies}")

    @classmethod
    def tearDownClass(cls):
        driver = get_driver()
        with driver.session() as session:
            session.execute_write(
                lambda tx, params: tx.run(
                    """
                    MATCH (n) WHERE n.id IN [$f_id, $job_id, $awr_id, $ksat_id]
                    DETACH DELETE n
                    """,
                    **params,
                ),
                {
                    "f_id": cls.f_id,
                    "job_id": cls.job_id,
                    "awr_id": cls.awr_id,
                    "ksat_id": cls.ksat_id,
                },
            )
        super().tearDownClass()

    def test_competency_list(self):
        resp = self.client.get("/api/competencies/?limit=5")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("results", resp.json())

    def test_competency_detail(self):
        """Test retrieving a single Job competency"""
        print(f"Testing competency detail for ID: {self.job_id}")
        resp = self.client.get(f"/api/competencies/{self.job_id}/")
        print(f"Response status: {resp.status_code}")
        if resp.status_code != 200:
            print(f"Response content: {resp.content}")
        self.assertEqual(resp.status_code, 200)

        data = resp.json()
        self.assertEqual(data["id"], self.job_id)
        self.assertEqual(data["type_label"], "Job")
        self.assertEqual(data["domain"], "DCWF")
        self.assertEqual(data["conformsTo"], "SCD 1.0")

    def test_framework_list(self):
        resp = self.client.get("/api/frameworks/?limit=5")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()["results"]
        self.assertTrue(any(f["id"] == self.f_id for f in data))

    def test_framework_with_competencies(self):
        resp = self.client.get(f"/api/frameworks/{self.f_id}/competencies/")
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertEqual(body["framework"]["id"], self.f_id)
        # Note: Framework hierarchy changed - competencies are now attached to jobs, not directly to frameworks
        # This test may need adjustment based on the API's handling of the new
        # structure

    def test_workrole_list_and_detail(self):
        # Test work role list endpoint
        list_resp = self.client.get("/api/workroles/?limit=5")
        self.assertEqual(list_resp.status_code, 200)

        # Test work role detail endpoint
        detail_resp = self.client.get(f"/api/workroles/{self.awr_id}/")
        self.assertEqual(detail_resp.status_code, 200)
        data = detail_resp.json()
        self.assertEqual(data["id"], self.awr_id)
        self.assertEqual(data["domain"], "DCWF")
        self.assertEqual(data["type_label"], "Advanced Work Role")

    def test_workrole_competency_detail(self):
        """Test retrieving a work role competency"""
        resp = self.client.get(f"/api/competencies/{self.awr_id}/")
        self.assertEqual(resp.status_code, 200)

        data = resp.json()
        self.assertEqual(data["id"], self.awr_id)
        self.assertEqual(data["type_label"], "Advanced Work Role")
        self.assertEqual(data["domain"], "DCWF")
        self.assertEqual(data["conformsTo"], "SCD 1.0")

    def test_ksat_competency_detail(self):
        """Test retrieving a KSAT competency"""
        resp = self.client.get(f"/api/competencies/{self.ksat_id}/")
        self.assertEqual(resp.status_code, 200)

        data = resp.json()
        self.assertEqual(data["id"], self.ksat_id)
        self.assertEqual(data["type_label"], "Skill")
        self.assertEqual(data["domain"], "DCWF")
        self.assertEqual(data["conformsTo"], "SCD 1.0")

    def test_framework_hierarchy(self):
        # Test that DCWF framework exists
        resp = self.client.get(f"/api/frameworks/{self.f_id}/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["id"], self.f_id)
        self.assertEqual(data.get("domain"), "DCWF")
        self.assertEqual(data.get("conformsTo"), "SCD 1.0")
