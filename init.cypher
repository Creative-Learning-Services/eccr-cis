// Create DCWF Framework Hierarchy
CREATE
  (DCWFF1:DCWFFramework:Framework
    {
      id: "DCWFF-001",
      name: "DoD Cyber Workforce Framework",
      description:
        "Department of Defense's standardized system for describing and managing its cyber-related personnel, serving as a common lexicon of work roles, tasks, and necessary knowledge, skills, and abilities",
      authoritativeSource: "https://public.cyber.mil/dcwf-framework",
      competencyDefinition: ["CD-EXPL-001", "CD-INTEL-002", "CD-VULN-003"],
      PROFILE: ["Framework", "DCWFFramework"],
      domain: "DCWF",
      conformsTo: "SCD 1.0"
    })

CREATE
  (FC1:FunctionalCommunity:Framework
    {
      id: "DCWF-FC1",
      name: "Cyberspace Information Technology (IT) Workforce",
      description:
        "Personnel who design, build, configure, operate, and maintain IT, networks, and capabilities.",
      authoritativeSource:
        "https://public.cyber.mil/dcwf-functional-community/cyberspace_it_workforce",
      competencyDefinition: ["CD-TECH-001", "CD-CUST-002", "CD-SOFT-004"],
      PROFILE: ["Framework", "FunctionalCommunity"],
      domain: "DCWF",
      conformsTo: "SCD 1.0"
    })

CREATE
  (wr1:WorkForceElement:Framework
    {
      id: "DCWF-FC1-CE",
      name: "Cyberspace Enablers",
      description:
        "A broad element focusing on personnel who enable cyberspace operations.",
      authoritativeSource:
        "https://public.cyber.mil/dcwf-workforce-element/cyber_enabler",
      competencyDefinition: ["CD-SEC-005", "CD-DEV-001", "CD-RSCH-002"],
      PROFILE: ["Framework", "WorkForceElement"],
      domain: "DCWF",
      conformsTo: "SCD 1.0"
    })

// Create Job Competency Nodes
CREATE
  (job1:Job:Competency
    {
      id: "WR-AN-EX-001",
      name: "Exploitation Analyst",
      description:
        "Partners with cyberspace operations customers to identify access and collection gaps that can be satisfied through cyberspace exploitation.",
      competencyStatement: "Job of Exploitation Analyst within DCWF",
      isSupportedBy: ["RA-CYBER-001", "RA-INTEL-003"],
      type: "Job",
      typeURI: "https://ksat.nist.gov/Job",
      markings: ["UNCLASSIFIED"],
      LocationName: "Washington, DC",
      JobSalary: "GS-12/13",
      JobTravelCode: "25% Travel",
      PromotionPotential: "GS-14",
      careerpathway: ["CP-INTEL-001", "CP-CYBER-003"],
      AssessmentRubric: "https://rubrics.cyber/exploitation_analyst",
      NISTID: ["NIST-SP-800-181"],
      DCWFID: ["DCWF-101"],
      PROFILE: ["job", "competency"],
      domain: "DCWF",
      conformsTo: "SCD 1.0"
    })

CREATE
  (job2:Job:Competency
    {
      id: "WR-OM-TS-001",
      name: "Technical Support Specialist",
      description:
        "Provides technical support to customers who need assistance utilizing client level hardware and software in accordance with established organizational processes.",
      competencyStatement: "Job of Technical Support Specialist within DCWF",
      isSupportedBy: ["RA-TECH-002", "RA-SUPP-001"],
      type: "Job",
      typeURI: "https://ksat.nist.gov/Job",
      markings: ["UNCLASSIFIED"],
      LocationName: "San Antonio, TX",
      JobSalary: "GS-9/11",
      JobTravelCode: "10% Travel",
      PromotionPotential: "GS-12",
      careerpathway: ["CP-IT-001", "CP-SECOPS-002"],
      AssessmentRubric: "https://rubrics.cyber/technical_support_specialist",
      NISTID: ["NIST-SP-800-181"],
      DCWFID: ["DCWF-102"],
      PROFILE: ["job", "competency"],
      domain: "DCWF",
      conformsTo: "SCD 1.0"
    })

// Create Work Role Competency Hierarchy
CREATE
  (awr1:AdvancedWorkRole:Competency
    {
      id: "AdvancedWorkRole-102",
      name: "Advanced Technical Support Specialist",
      description:
        "Diagnoses, resolves, and identifies enhancements resulting from complex or novel incidents.",
      competencyStatement:
        "Can diagnosis, resolve, and indentify enhancements resulting from complex or novel incidents",
      isSupportedBy: ["RA-CYBER-001", "RA-INTEL-003"],
      type: "Advanced Work Role",
      typeURI: "https://ksat.nist.gov/AdvancedWorkRole",
      AssessmentRubric: "https://rubrics.cyber/technicalsupportspecialist",
      NISTID: ["NIST-SP-800-181"],
      DCWFID: ["411"],
      PROFILE: ["work role", "competency"],
      domain: "DCWF",
      conformsTo: "SCD 1.0"
    })

CREATE
  (iwr1:IntermediateWorkRole:Competency
    {
      id: "IntermediateWorkRole-102",
      name: "Intermediate Technical Support Specialist",
      description:
        "Diagnoses and resolves customer-reported system incidents, problems, and events independently.",
      competencyStatement:
        "Can supervise diagnosis of system incidents, problems, and events",
      isSupportedBy: ["RA-CYBER-001", "RA-INTEL-003"],
      type: "Intermediate Work Role",
      typeURI: "https://ksat.nist.gov/IntermediateWorkRole",
      AssessmentRubric: "https://rubrics.cyber/technicalsupportspecialist",
      NISTID: ["NIST-SP-800-181"],
      DCWFID: ["411"],
      PROFILE: ["workRole", "competency"],
      domain: "DCWF",
      conformsTo: "SCD 1.0"
    })

CREATE
  (bwr1:BasicWorkRole:Competency
    {
      id: "BasicWorkRole-102",
      name: "Basic Technical Support Specialist",
      description:
        "Supports the diagnosis of customer-reported system incidents, problems, and events under supervision.",
      competencyStatement:
        "Can supervise diagnosis of system incidents, problems, and events while supervised",
      isSupportedBy: ["RA-CYBER-001", "RA-INTEL-003"],
      type: "Basic Work Role",
      typeURI: "https://ksat.nist.gov/BasicWorkRole",
      AssessmentRubric: "https://rubrics.cyber/technicalsupportspecialist",
      NISTID: ["NIST-SP-800-181"],
      DCWFID: ["411"],
      PROFILE: ["work role", "competency"],
      domain: "DCWF",
      conformsTo: "SCD 1.0"
    })

// Create framework hierarchy relationships
CREATE (DCWFF1)-[:HAS_SUBFRAMEWORK]->(FC1)
CREATE (FC1)-[:HAS_SUBFRAMEWORK]->(wr1)

// Create work role hierarchy requires relationships
CREATE (awr1)-[:REQUIRES]->(iwr1)
CREATE (iwr1)-[:REQUIRES]->(bwr1);

// Create KSAT Competency nodes with proper typing

CREATE
  (ksat3:KSATSTask:Competency
    {
      id: "KSAT-103",
      name: "Incident Response Coordination",
      description:
        "Task of coordinating and managing cyber incident response activities.",
      competencyStatement:
        "Can coordinate and manage cyber incident response activities",
      type: "Task",
      typeURI: "https://ksat.nist.gov/KSAT/Task",
      AssessmentRubric: "https://rubrics.cyber/ksat-103",
      Owner: "NIST",
      NISTID: ["NIST-SP-800-181"],
      DCWFID: ["DCWF-103"],
      PROFILE: ["ksats", "competency", "task"],
      domain: "DCWF",
      conformsTo: "SCD 1.0"
    })

CREATE
  (ksat5:KSATSAbility:Competency
    {
      id: "KSAT-105",
      name: "Security Policy Development",
      description:
        "Ability to develop and implement cybersecurity policies and standards.",
      competencyStatement:
        "Can develop and implement cybersecurity policies and standards",
      type: "Ability",
      typeURI: "https://ksat.nist.gov/KSAT/Ability",
      AssessmentRubric: "https://rubrics.cyber/ksat-105",
      Owner: "NIST",
      NISTID: ["NIST-SP-800-181"],
      DCWFID: ["DCWF-105"],
      PROFILE: ["ksats", "competency"],
      domain: "DCWF",
      conformsTo: "SCD 1.0"
    })

CREATE
  (ksat4:KSATSSkill:Competency
    {
      id: "KSAT-104",
      name: "Vulnerability Assessment",
      description:
        "Skill in conducting vulnerability assessments of systems and networks.",
      competencyStatement:
        "Can conduct vulnerability assessments of systems and networks",
      type: "Skill",
      typeURI: "https://ksat.nist.gov/KSAT/Skill",
      AssessmentRubric: "https://rubrics.cyber/ksat-104",
      Owner: "NIST",
      NISTID: ["NIST-SP-800-181"],
      DCWFID: ["DCWF-104"],
      PROFILE: ["ksats", "competency", "skill"],
      domain: "DCWF",
      conformsTo: "SCD 1.0"
    })

CREATE
  (ksat6:KSATSKnowledge:Competency
    {
      id: "KSAT-106",
      name: "Vulnerability Assessment Knowledge",
      description:
        "Knowledge in conducting vulnerability assessments of systems and networks.",
      competencyStatement:
        "Understands conducting vulnerability assessments of systems and networks",
      type: "Knowledge",
      typeURI: "https://ksat.nist.gov/KSAT/Knowledge",
      AssessmentRubric: "https://rubrics.cyber/ksat-106",
      Owner: "NIST",
      NISTID: ["NIST-SP-800-181"],
      DCWFID: ["DCWF-106"],
      PROFILE: ["ksats", "competency", "knowledge"],
      domain: "DCWF",
      conformsTo: "SCD 1.0"
    })

// Create KSAT type relationships (Task > Ability > Knowledge + Skill)
CREATE (ksat3)-[:REQUIRES]->(ksat5)
CREATE (ksat5)-[:REQUIRES]->(ksat4)
CREATE (ksat5)-[:REQUIRES]->(ksat6);

// Create relationships between Job:Competency nodes and KSAT:Competency nodes

MATCH
  (job1:Job:Competency {id: "WR-AN-EX-001"}),
  (ksat3:KSATSTask:Competency {id: "KSAT-103"})
CREATE (job1)-[:INCLUDES_KSATS]->(ksat3);

MATCH
  (job2:Job:Competency {id: "WR-OM-TS-001"}),
  (ksat4:KSATSSkill:Competency {id: "KSAT-104"})
CREATE (job2)-[:INCLUDES_KSATS]->(ksat4);

// Functional Community nodes are now handled as Framework level entities above

// Updated Job and Work Role relationships

MATCH
  (job1:Job:Competency {id: "WR-AN-EX-001"}),
  (awr1:AdvancedWorkRole:Competency {id: "AdvancedWorkRole-102"})
CREATE (job1)-[:REQUIRES]->(awr1);

MATCH
  (job2:Job:Competency {id: "WR-OM-TS-001"}),
  (iwr1:IntermediateWorkRole:Competency {id: "IntermediateWorkRole-102"})
CREATE (job2)-[:REQUIRES]->(iwr1);

// WorkforceElement nodes are now handled as Framework level entities above

// Create 5 DCWFCompetency:Competency nodes using the CompetencyDefinition schema

CREATE
  (dcwf1:DCWFCompetency:Competency
    {
      id: "DCWF-COMP-001",
      name: "Network Security Monitoring",
      description:
        "Ability to monitor, detect, and respond to network security threats.",
      competencyStatement:
        "Can identify and respond to network-based threats using monitoring tools.",
      resourceAssociation: ["https://resources.cyber/dcwf1"],
      competencyFramework: ["https://frameworks.cyber/dcwf"],
      referenceCode: "NSM-001",
      competencyLevel: "Advanced",
      typeLabel: "Technical",
      typeUri: "https://types.cyber/technical",
      PROFILE: ["DCWFCompetency", "Competency"],
      domain: "DCWF"
    })

CREATE
  (dcwf2:DCWFCompetency:Competency
    {
      id: "DCWF-COMP-002",
      name: "Incident Response Management",
      description:
        "Ability to manage and coordinate response to cybersecurity incidents.",
      competencyStatement:
        "Can lead and coordinate incident response activities.",
      resourceAssociation: ["https://resources.cyber/dcwf2"],
      competencyFramework: ["https://frameworks.cyber/dcwf"],
      referenceCode: "IRM-002",
      competencyLevel: "Expert",
      typeLabel: "Management",
      typeUri: "https://types.cyber/management",
      PROFILE: ["DCWFCompetency", "Competency"],
      domain: "DCWF"
    })

CREATE
  (dcwf3:DCWFCompetency:Competency
    {
      id: "DCWF-COMP-003",
      name: "Vulnerability Assessment",
      description:
        "Ability to assess and report vulnerabilities in systems and networks.",
      competencyStatement:
        "Can conduct vulnerability assessments and recommend mitigations.",
      resourceAssociation: ["https://resources.cyber/dcwf3"],
      competencyFramework: ["https://frameworks.cyber/dcwf"],
      referenceCode: "VA-003",
      competencyLevel: "Intermediate",
      typeLabel: "Technical",
      typeUri: "https://types.cyber/technical",
      PROFILE: ["DCWFCompetency", "Competency"],
      domain: "DCWF"
    })

CREATE
  (dcwf4:DCWFCompetency:Competency
    {
      id: "DCWF-COMP-004",
      name: "Cybersecurity Policy Development",
      description:
        "Ability to develop and implement cybersecurity policies and standards.",
      competencyStatement:
        "Can create and maintain cybersecurity policies for an organization.",
      resourceAssociation: ["https://resources.cyber/dcwf4"],
      competencyFramework: ["https://frameworks.cyber/dcwf"],
      referenceCode: "CPD-004",
      competencyLevel: "Advanced",
      typeLabel: "Policy",
      typeUri: "https://types.cyber/policy",
      PROFILE: ["DCWFCompetency", "Competency"],
      domain: "DCWF"
    })

CREATE
  (dcwf5:DCWFCompetency:Competency
    {
      id: "DCWF-COMP-005",
      name: "Risk Management",
      description:
        "Ability to identify, assess, and mitigate cybersecurity risks.",
      competencyStatement:
        "Can perform risk assessments and develop mitigation strategies.",
      resourceAssociation: ["https://resources.cyber/dcwf5"],
      competencyFramework: ["https://frameworks.cyber/dcwf"],
      referenceCode: "RM-005",
      competencyLevel: "Expert",
      typeLabel: "Management",
      typeUri: "https://types.cyber/management",
      PROFILE: ["DCWFCompetency", "Competency"],
      domain: "DCWF"
    });

// Create REQUIRES_COMPETENCY relationships between KSATS:Competency and DCWFCompetency:Competency

MATCH
  (ksat1:KSATS:Competency {id: "KSAT-101"}),
  (dcwf1:DCWFCompetency:Competency {id: "DCWF-COMP-001"})
CREATE (ksat1)-[:REQUIRES_COMPETENCY]->(dcwf1);

MATCH
  (ksat2:KSATS:Competency {id: "KSAT-102"}),
  (dcwf2:DCWFCompetency:Competency {id: "DCWF-COMP-002"})
CREATE (ksat2)-[:REQUIRES_COMPETENCY]->(dcwf2);

MATCH
  (ksat3:KSATS:Competency {id: "KSAT-103"}),
  (dcwf3:DCWFCompetency:Competency {id: "DCWF-COMP-003"})
CREATE (ksat3)-[:REQUIRES_COMPETENCY]->(dcwf3);

MATCH
  (ksat4:KSATS:Competency {id: "KSAT-104"}),
  (dcwf4:DCWFCompetency:Competency {id: "DCWF-COMP-004"})
CREATE (ksat4)-[:REQUIRES_COMPETENCY]->(dcwf4);

MATCH
  (ksat5:KSATS:Competency {id: "KSAT-105"}),
  (dcwf5:DCWFCompetency:Competency {id: "DCWF-COMP-005"})
CREATE (ksat5)-[:REQUIRES_COMPETENCY]->(dcwf5);

// DOTE Domain Instance Sample Dataset

// Create the Framework node
CREATE
  (f:Framework
    {
      id: "comp_framework_1",
      name: "Operating Environment and System Design",
      authoritative_source: "https://us.gov/DoD_T&E_Framework.doc",
      description:
        "Understand and communicate joint warfighting concepts, CONEMP/CONOPS and TTP for DoD systems, including but not limited to the CONOP/CONEMP, TTP, and capabilities of opposing forces. Contextualize DoD system design requirements with respect to the operational mission and the intended operating environment.",
      start_date: datetime("2024-01-01T00:00:00Z"),
      end_date: datetime("2025-12-31T23:59:59Z"),
      PROFILE: "DOT&E"
    })

// Create Competency 1.1 - Mission
CREATE
  (c1:Competency:DoteKsat
    {
      id: "comp_1_1",
      name: "Mission Understanding",
      description:
        "Understands and communicates CONEMP/CONOPS, TTP, and how (Services, Joint) units/forces equipped with DoD system are intended to contribute to the warfighter's/joint force mission. Considers DoD systems in the context of kill-webs, mission threads and other operationally relevant and realistic system-of-system mission scenarios.",
      competency_statement:
        "Understands and communicates CONEMP/CONOPS, TTP, and warfighter mission contribution",
      competency_framework: "comp_framework_1",
      resource_association: "https://us.gov/courses/Mission_Planning_Systems",
      type_label: "Knowledge",
      type_uri: "http://competency.dod.mil/knowledge",
      PROFILE: "KSAT",
      ksat_type: "Knowledge"
    })

// The rest of the Competencies can follow the model above
// Create Competency 1.2 - COIs
CREATE
  (c2:Competency:DoteKsat
    {
      id: "comp_1_2",
      name: "Conditions of Interest (COIs)",
      description:
        "Understands COIs that the DoD system is intended to address. This includes but is not limited to fundamental operational factors and levels that might affect COIs including but not limited to terrain, climate, vegetation, opposing forces to support the development of mission scenarios in all domain or multi domain operations.",
      competency_statement:
        "Understands COIs and operational factors affecting DoD systems",
      competency_framework: "Operating Environment and System Design",
      resource_association: "Environmental_Assessment_Tools",
      type_label: "COIs",
      type_uri: "http://competency.dod.mil/cois",
      PROFILE: "KSAT",
      ksat_type: "Knowledge"
    })

// Create Competency 1.3 - DoD System
CREATE
  (c3:Competency:DoteKsat
    {
      id: "comp_1_3",
      name: "DoD System Understanding",
      description:
        "Understands the DoD systems and its mission critical function including but not limited to sub-components, components, sub-systems, and systems design features critical to operational effectiveness, suitability, survivability, and lethality.",
      competency_statement:
        "Understands DoD systems architecture and mission critical functions",
      competency_framework: "Operating Environment and System Design",
      resource_association: "Systems_Architecture_Documentation",
      type_label: "DoD System",
      type_uri: "http://competency.dod.mil/system",
      PROFILE: "KSAT",
      ksat_type: "Knowledge"
    })

// Create Competency 1.4 - User
CREATE
  (c4:Competency:DoteKsat
    {
      id: "comp_1_4",
      name: "User Mission and Training",
      description:
        "Understands the user mission/training and how the user will use and operate the DoD systems. Understands the human-system interface, workload demands, usability, situational awareness requirements, training process and requirements.",
      competency_statement:
        "Understands user operations and human-system interface requirements",
      competency_framework: "Operating Environment and System Design",
      resource_association: "Human_Factors_Engineering",
      type_label: "User",
      type_uri: "http://competency.dod.mil/user",
      PROFILE: "KSAT",
      ksat_type: "Skill"
    })

// Create Competency 1.5 - Opposing Forces
CREATE
  (c5:Competency:DoteKsat
    {
      id: "comp_1_5",
      name: "Opposing Forces Understanding",
      description:
        "In coordination with the Intelligence Community, maintains operational understanding, awareness and expertise of the adversary CONEMP/CONOPS, TTP, threat and target landscape that have, will, or currently impact DoD system(s) in the intended theater of operations. Understands the kinetic and non-kinetic threat and targets laydown, density, distribution, capabilities, effects for the intended DoD system area of operation, including but not limited to the most relevant, proliferated and stressing threats and targets to the DoD system.",
      competency_statement:
        "Maintains operational understanding of adversary capabilities and threat landscape",
      competency_framework: "Operating Environment and System Design",
      resource_association: "Intelligence_Community_Resources",
      type_label: "Opposing Forces",
      type_uri: "http://competency.dod.mil/threats",
      PROFILE: "KSAT",
      ksat_type: "Ability"
    })

// Create HAS_COMPETENCY relationships
CREATE (f)-[:HAS_COMPETENCY]->(c1)

CREATE (f)-[:HAS_COMPETENCY]->(c2)

CREATE (f)-[:HAS_COMPETENCY]->(c3)

CREATE (f)-[:HAS_COMPETENCY]->(c4)

CREATE (f)-[:HAS_COMPETENCY]->(c5)

// Create Framework #2
CREATE
  (f2:Framework
    {
      id: "comp_framework_2",
      name: "Acquisition and Requirements Process",
      authoritative_source: "DoD T&E Framework",
      resource_association: "DoD_Acquisition_System",
      description:
        "Understand the acquisition strategy and the relevant acquisition and program decisions for each of the adaptive acquisition framework pathways. Understand and maximize the contracting process for the benefit of meeting OT&E and LFT&E objectives. Understand and inform the technical and operational requirements.",
      start_date: datetime("2024-01-01T00:00:00Z"),
      end_date: datetime("2025-12-31T23:59:59Z"),
      association: "DoD_Acquisition_Process",
      PROFILE: "DOT&E"
    })

// Create Competency 2.1 - Acquisition Strategy
CREATE
  (c21:Competency:DoteKsat
    {
      id: "comp_2_1",
      name: "Acquisition Strategy",
      description:
        "Understands the intent of the acquisition strategy. Considers the details of the acquisition strategy in the context of the development of TEMP or T&E strategy, and OT&E and LFT&E plans.",
      competency_statement:
        "Understands acquisition strategy intent and its application to T&E planning",
      competency_framework: "Acquisition and Requirements Process",
      resource_association: "Acquisition_Strategy_Documentation",
      type_label: "Acquisition Strategy",
      type_uri: "http://competency.dod.mil/acquisition_strategy",
      PROFILE: "KSAT",
      ksat_type: "Knowledge"
    })

// Create Competency 2.2 - Acquisition Pathway
CREATE
  (c22:Competency:DoteKsat
    {
      id: "comp_2_2",
      name: "Acquisition Pathway",
      description:
        "Understands the acquisition policy for each of the acquisition pathways. Considers the acquisition and program decisions in identifying the appropriate test data and M&S results needed to inform those decisions, given the maturity of the DoD system.",
      competency_statement:
        "Understands acquisition pathways and appropriate test data requirements",
      competency_framework: "Acquisition and Requirements Process",
      resource_association: "Adaptive_Acquisition_Framework",
      type_label: "Acquisition Pathway",
      type_uri: "http://competency.dod.mil/acquisition_pathway",
      PROFILE: "KSAT",
      ksat_type: "Knowledge"
    })

// Create Competency 2.3 - Acquisition Management
CREATE
  (c23:Competency:DoteKsat
    {
      id: "comp_2_3",
      name: "Acquisition Management",
      description:
        "Understands the acquisition process and the roles and responsibilities of the program manager, the test and evaluation working-level integrated product team or integrated test team, and the roles and responsibilities of the operational test agencies and the LFT&E organizations. Has the building coalitions and leadership skills to influence the acquisition management for the benefit of meeting OT&E and LFT&E objectives.",
      competency_statement:
        "Understands acquisition roles and demonstrates leadership skills to influence management",
      competency_framework: "Acquisition and Requirements Process",
      resource_association: "Acquisition_Management_Systems",
      type_label: "Acquisition Management",
      type_uri: "http://competency.dod.mil/acquisition_management",
      PROFILE: "KSAT",
      ksat_type: "Ability"
    })

// Create Competency 2.4 - Contracting
CREATE
  (c24:Competency:DoteKsat
    {
      id: "comp_2_4",
      name: "Contracting",
      description:
        "Understands when and how to define OT&E and LFT&E requirements to inform requests for proposals and acquisition contracts, and secure access to required contractor-generated data, tools, support, test articles, and expertise.",
      competency_statement:
        "Understands contracting processes for T&E requirements and data access",
      competency_framework: "Acquisition and Requirements Process",
      resource_association: "Contracting_Systems",
      type_label: "Contracting",
      type_uri: "http://competency.dod.mil/contracting",
      PROFILE: "KSAT",
      ksat_type: "Skill"
    })

// Create Competency 2.5 - Requirements
CREATE
  (c25:Competency:DoteKsat
    {
      id: "comp_2_5",
      name: "Requirements",
      description:
        "Understands and supports the role of the DOT&E as an advisor to the Joint Requirements Oversight Council on matters within DOT&E authority and expertise. Informs and influences the requirements development process so the technical and operational requirements are measurable, testable, justifiable, achievable, and relevant to the operational mission.",
      competency_statement:
        "Supports DOT&E advisory role and influences requirements development",
      competency_framework: "Acquisition and Requirements Process",
      resource_association: "JROC_Requirements_Process",
      type_label: "Requirements",
      type_uri: "http://competency.dod.mil/requirements",
      PROFILE: "KSAT",
      ksat_type: "Ability"
    })

// Create HAS_COMPETENCY relationships
CREATE (f2)-[:HAS_COMPETENCY]->(c21)

CREATE (f2)-[:HAS_COMPETENCY]->(c22)

CREATE (f2)-[:HAS_COMPETENCY]->(c23)

CREATE (f2)-[:HAS_COMPETENCY]->(c24)

CREATE (f2)-[:HAS_COMPETENCY]->(c25)

// Create Framework #3
CREATE
  (f3:Framework
    {
      id: "comp_framework_3",
      name: "Policy Development and Implementation",
      authoritative_source: "DoD T&E Framework",
      resource_association: "DoD_Policy_Systems",
      description:
        "Understand, implement, and promulgate relevant DoD and T&E policies and guidance. Support DOT&E strategic initiatives intended to update existing and establish new policy for OT&E and LFT&E.",
      start_date: datetime("2024-01-01T00:00:00Z"),
      end_date: datetime("2025-12-31T23:59:59Z"),
      association: "DoD_Policy_Development",
      PROFILE: "DOT&E"
    })

// Create Competency 3.1 - Policy Compliance
CREATE
  (c31:Competency:DoteKsat
    {
      id: "comp_3_1",
      name: "Policy Compliance",
      description:
        "Understands, implements, and ensures compliance with DoD policy for OT&E and LFT&E for programs on the T&E Oversight List for OT&E and LFT&E.",
      competency_statement:
        "Understands, implements, and ensures DoD policy compliance for T&E programs",
      competency_framework: "Policy Development and Implementation",
      resource_association: "DoD_Policy_Database",
      type_label: "Policy Compliance",
      type_uri: "http://competency.dod.mil/policy_compliance",
      PROFILE: "KSAT",
      ksat_type: "Knowledge"
    })

// Create Competency 3.2 - Policy Development
CREATE
  (c32:Competency:DoteKsat
    {
      id: "comp_3_2",
      name: "Policy Development",
      description:
        "Identifies policy and guidance gaps or challenges and offers solutions to the DOT&E strategy and policy development team in accordance with DOT&E standard operating procedures.",
      competency_statement:
        "Identifies policy gaps and offers solutions to DOT&E policy development team",
      competency_framework: "Policy Development and Implementation",
      resource_association: "Policy_Development_SOPs",
      type_label: "Policy Development",
      type_uri: "http://competency.dod.mil/policy_development",
      PROFILE: "KSAT",
      ksat_type: "Ability"
    })

// Create Competency 3.3 - Policy Adoption
CREATE
  (c33:Competency:DoteKsat
    {
      id: "comp_3_3",
      name: "Policy Adoption",
      description:
        "Offers use cases and opportunities within the program to pilot new policy and guidance initiatives. Drafts language for new policy and guidance as demonstrated with use cases.",
      competency_statement:
        "Offers use cases for piloting new policy and drafts policy language",
      competency_framework: "Policy Development and Implementation",
      resource_association: "Policy_Pilot_Programs",
      type_label: "Policy Adoption",
      type_uri: "http://competency.dod.mil/policy_adoption",
      PROFILE: "KSAT",
      ksat_type: "Skill"
    })

// Create Competency 3.4 - Policy Awareness
CREATE
  (c34:Competency:DoteKsat
    {
      id: "comp_3_4",
      name: "Policy Awareness",
      description:
        "Understands and keeps up-to-date on local, national, and international policies and trends that affect the organization and shape stakeholders' views; is aware of the organization's impact on the external environment. Understands and keeps-up-to-date on new and developing policy governing T&E of next-generation technology and emerging threats.",
      competency_statement:
        "Maintains awareness of policy trends and emerging technology T&E policy",
      competency_framework: "Policy Development and Implementation",
      resource_association: "Policy_Intelligence_Systems",
      type_label: "Policy Awareness",
      type_uri: "http://competency.dod.mil/policy_awareness",
      PROFILE: "KSAT",
      ksat_type: "Knowledge"
    })

// Create HAS_COMPETENCY relationships
CREATE (f3)-[:HAS_COMPETENCY]->(c31)

CREATE (f3)-[:HAS_COMPETENCY]->(c32)

CREATE (f3)-[:HAS_COMPETENCY]->(c33)

CREATE (f3)-[:HAS_COMPETENCY]->(c34)

// Create Framework #4
CREATE
  (f4:Framework
    {
      id: "comp_framework_4",
      name: "Test Planning, Execution, and Evaluation",
      authoritative_source: "DoD T&E Framework",
      resource_association: "DoD_Test_Evaluation_Systems",
      description:
        "Evaluate the adequacy and compliance of TEMPs, T&E strategies, OT&E, and LFT&E plans with DoD policy for OT&E and LFT&E. Observe test events and analyze results of T&E to evaluate operational effectiveness, operational suitability, survivability, and lethality with scientific rigor.",
      start_date: datetime("2024-01-01T00:00:00Z"),
      end_date: datetime("2025-12-31T23:59:59Z"),
      association: "DoD_Test_Evaluation",
      PROFILE: "DOT&E"
    })

// Create Competency 4.1 - Science and Technology
CREATE
  (c41:Competency:DoteKsat
    {
      id: "comp_4_1",
      name: "Science and Technology",
      description:
        "Understands and applies the latest advances in science (e.g., design of experiments, statistical inference methods, big data analytics) and technology (e.g., M&S, digital engineering, digital tools, data management tools, modern predictive analytics tools using AI and machine learning, other automation and AI-enabled tools) to optimize planning, execution, analysis, and reporting of integrated T&E, OT&E, and LFT&E across the acquisition life cycle.",
      competency_statement:
        "Applies latest science and technology advances to optimize T&E across acquisition lifecycle",
      competency_framework: "Test Planning, Execution, and Evaluation",
      resource_association: "Science_Technology_Tools",
      type_label: "Science and Technology",
      type_uri: "http://competency.dod.mil/science_technology",
      PROFILE: "KSAT",
      ksat_type: "Ability"
    })

// Create Competency 4.2 - Risk Assessment
CREATE
  (c42:Competency:DoteKsat
    {
      id: "comp_4_2",
      name: "Risk Assessment",
      description:
        "Understands and/or executes risk-based level of test assessment and mission-based risk assessments needed to inform OT&E and LFT&E scope tailored to the acquisition strategy. Identifies how the operational and live fire test strategies map to IDSK to integrate T&E data and independent OT&E and LFT&E data and M&S results needed to appropriately inform the acquisition and program decisions.",
      competency_statement:
        "Executes risk-based assessments and maps test strategies to IDSK for acquisition decisions",
      competency_framework: "Test Planning, Execution, and Evaluation",
      resource_association: "Risk_Assessment_Tools",
      type_label: "Risk Assessment",
      type_uri: "http://competency.dod.mil/risk_assessment",
      PROFILE: "KSAT",
      ksat_type: "Skill"
    })

// Create Competency 4.3 - TEMP/T&E Strategy Development
CREATE
  (c43:Competency:DoteKsat
    {
      id: "comp_4_3",
      name: "TEMP/T&E Strategy Development",
      description:
        "Understands and implements DoD policy for TEMP/T&E strategy to help codify an agreement between the DoD system program manager and T&E stakeholders. Has the knowledge to help outline and justify the focus and scope of OT&E and LFT&E activities required to evaluate the operational effectiveness, suitability, survivability, and lethality (as applicable) of DoD systems as they mature across the acquisition life cycle.",
      competency_statement:
        "Implements TEMP/T&E strategy policy and justifies OT&E and LFT&E scope",
      competency_framework: "Test Planning, Execution, and Evaluation",
      resource_association: "TEMP_Development_Tools",
      type_label: "TEMP/T&E Strategy Development",
      type_uri: "http://competency.dod.mil/temp_strategy",
      PROFILE: "KSAT",
      ksat_type: "Knowledge"
    })

// Create Competency 4.4 - Test and M&S V&V Plan Development
CREATE
  (c44:Competency:DoteKsat
    {
      id: "comp_4_4",
      name: "Test and M&S V&V Plan Development",
      description:
        "Support the development of OT&E, LFT&E, and M&S plans using applied mathematics, statistics, inference methods, or related science-based test and analysis methods. Ensure test and M&S plans include operationally relevant conditions, information about the order of test event execution and test data collection, cost estimate, and relevant operating instructions that may impact test outcomes.",
      competency_statement:
        "Develops science-based test and M&S V&V plans with operationally relevant conditions",
      competency_framework: "Test Planning, Execution, and Evaluation",
      resource_association: "Test_Planning_Tools",
      type_label: "Test and M&S V&V Plan Development",
      type_uri: "http://competency.dod.mil/test_plan_development",
      PROFILE: "KSAT",
      ksat_type: "Skill"
    })

// Create Competency 4.5 - Execution
CREATE
  (c45:Competency:DoteKsat
    {
      id: "comp_4_5",
      name: "Execution",
      description:
        "Ensures execution of tests and data collection in accordance with DoD policy for OT&E and LFT&E, approved test, M&S, and M&S V&V plans. Understands and confirms requirements of an approved test or M&S plan are satisfied by the end of an OT&E, LFT&E, or M&S event.",
      competency_statement:
        "Ensures test execution compliance and confirms plan requirement satisfaction",
      competency_framework: "Test Planning, Execution, and Evaluation",
      resource_association: "Test_Execution_Systems",
      type_label: "Execution",
      type_uri: "http://competency.dod.mil/test_execution",
      PROFILE: "KSAT",
      ksat_type: "Skill"
    })

// Create Competency 4.6 - Evaluation
CREATE
  (c46:Competency:DoteKsat
    {
      id: "comp_4_6",
      name: "Evaluation",
      description:
        "Understands and uses digital tools, applied mathematics, statistics, inference methods, and other science-based analytical methods to independently analyze all relevant test data and M&S results in as real-time as possible to inform the existing and next phase of test.",
      competency_statement:
        "Uses science-based analytical methods for real-time test data analysis",
      competency_framework: "Test Planning, Execution, and Evaluation",
      resource_association: "Data_Analysis_Tools",
      type_label: "Evaluation",
      type_uri: "http://competency.dod.mil/test_evaluation",
      PROFILE: "KSAT",
      ksat_type: "Ability"
    })

// Create HAS_COMPETENCY relationships
CREATE (f4)-[:HAS_COMPETENCY]->(c41)

CREATE (f4)-[:HAS_COMPETENCY]->(c42)

CREATE (f4)-[:HAS_COMPETENCY]->(c43)

CREATE (f4)-[:HAS_COMPETENCY]->(c44)

CREATE (f4)-[:HAS_COMPETENCY]->(c45)

CREATE (f4)-[:HAS_COMPETENCY]->(c46)

// Create Framework #4A
CREATE
  (f4a:Framework
    {
      id: "comp_framework_4a",
      name: "Data Management and Reporting",
      authoritative_source: "DoD T&E Framework",
      resource_association: "DoD_Data_Management_Systems",
      description:
        "Manage the data and information gathered during testing and assess data collection methodologies and tools to improve the testing process, and clearly articulate highly technical results of OT&E and LFT&E test to Congress and other stakeholders.",
      start_date: datetime("2024-01-01T00:00:00Z"),
      end_date: datetime("2025-12-31T23:59:59Z"),
      association: "DoD_Data_Management",
      PROFILE: "DOT&E"
    })

// Create Competency 4A.1 - T&E Data Strategy and Management
CREATE
  (c4a1:Competency:DoteKsat
    {
      id: "comp_4a_1",
      name: "T&E Data Strategy and Management",
      description:
        "Understands the DoD data management strategy, policy and guidance and ensures that acquisition programs have an adequate data management strategy and plan to maximize the use of contractor and developmental test and evaluation data and other program artifacts in support of OT&E and LFT&E planning, execution, analysis, and reporting. Ensures DOT&E access to all program relevant data to increase OT&E and LFT&E efficiency and effectiveness.",
      competency_statement:
        "Understands DoD data management strategy and ensures adequate program data management plans",
      competency_framework: "Data Management and Reporting",
      resource_association: "DoD_Data_Strategy_Systems",
      type_label: "T&E Data Strategy and Management",
      type_uri: "http://competency.dod.mil/data_strategy",
      PROFILE: "KSAT",
      ksat_type: "Knowledge"
    })

// Create Competency 4A.2 - DOT&E Data and Knowledge Management
CREATE
  (c4a2:Competency:DoteKsat
    {
      id: "comp_4a_2",
      name: "DOT&E Data and Knowledge Management",
      description:
        "Store the data and M&S results throughout the OT&E and LFT&E planning, preparation, execution, analysis, and evaluation phases, in accordance with the DOT&E data management plan. Develop and deliver OT&E and LFT&E reports on test adequacy, preliminary or final evaluation of operational effectiveness, suitability, survivability, and lethality, and actionable recommendations in accordance with the policy for OT&E and LFT&E, and DOT&E reporting guidance.",
      competency_statement:
        "Manages DOT&E data storage and develops comprehensive T&E evaluation reports",
      competency_framework: "Data Management and Reporting",
      resource_association: "DOT&E_Data_Management_Platform",
      type_label: "DOT&E Data and Knowledge Management",
      type_uri: "http://competency.dod.mil/dote_data_management",
      PROFILE: "KSAT",
      ksat_type: "Skill"
    })

// Create Competency 4A.3 - Technical Writing and Reporting
CREATE
  (c4a3:Competency:DoteKsat
    {
      id: "comp_4a_3",
      name: "Technical Writing and Reporting",
      description:
        "Creates clear, concise, timely, and accurate technical T&E documentation (e.g., annual reports, Operational Assessments, emerging results briefs, Initial Operational Test reports) and follows the recommended structure in every report, and personally defends data, conclusions, and recommendations.",
      competency_statement:
        "Creates clear technical T&E documentation and defends conclusions and recommendations",
      competency_framework: "Data Management and Reporting",
      resource_association: "Technical_Writing_Tools",
      type_label: "Technical Writing and Reporting",
      type_uri: "http://competency.dod.mil/technical_writing",
      PROFILE: "KSAT",
      ksat_type: "Skill"
    })

// Create Competency 4A.4 - Communication
CREATE
  (c4a4:Competency:DoteKsat
    {
      id: "comp_4a_4",
      name: "Communication",
      description:
        "Applies knowledge of DoD acquisition system, science and technology-based test and evaluation, and concepts of operations for clear and convincing presentations of technical data, analysis, and evaluation tailored to the intended audience (Congress, DoD Senior leaders, and Warfighter).",
      competency_statement:
        "Delivers clear technical presentations tailored to diverse stakeholder audiences",
      competency_framework: "Data Management and Reporting",
      resource_association: "Presentation_Tools",
      type_label: "Communication",
      type_uri: "http://competency.dod.mil/technical_communication",
      PROFILE: "KSAT",
      ksat_type: "Ability"
    })

// Create Competency 4A.5 - Information Security
CREATE
  (c4a5:Competency:DoteKsat
    {
      id: "comp_4a_5",
      name: "Information Security",
      description:
        "Properly protects and safeguards classified information to prevent unauthorized disclosure by adhering to DoD Manual 5200.01, Volume 3 and Executive Order 13526, and specific acquisition program classification guidance manuals. Prevents, detects, and reports security incidents, security violations, and classified data spills and helps correct the causes of such occurrence.",
      competency_statement:
        "Protects classified information and prevents security incidents per DoD policy",
      competency_framework: "Data Management and Reporting",
      resource_association: "Information_Security_Systems",
      type_label: "Information Security",
      type_uri: "http://competency.dod.mil/information_security",
      PROFILE: "KSAT",
      ksat_type: "Knowledge"
    })

// Create HAS_COMPETENCY relationships
CREATE (f4a)-[:HAS_COMPETENCY]->(c4a1)

CREATE (f4a)-[:HAS_COMPETENCY]->(c4a2)

CREATE (f4a)-[:HAS_COMPETENCY]->(c4a3)

CREATE (f4a)-[:HAS_COMPETENCY]->(c4a4)

CREATE (f4a)-[:HAS_COMPETENCY]->(c4a5)

// Create Framework #4B
CREATE
  (f4b:Framework
    {
      id: "comp_framework_4b",
      name: "TEMP/T&E Strategy Development",
      authoritative_source: "DoD T&E Framework",
      resource_association: "DoD_TEMP_Systems",
      description:
        "Ensure compliance with DoD policy for TEMP/T&E Strategy. Help codify an agreement between the DoD system program manager and T&E stakeholders outlining and justifying the focus and scope of T&E activities required to evaluate the operational effectiveness, suitability, survivability, and lethality of DoD systems as they mature across the acquisition life cycle.",
      start_date: datetime("2024-01-01T00:00:00Z"),
      end_date: datetime("2025-12-31T23:59:59Z"),
      association: "DoD_TEMP_Strategy",
      PROFILE: "DOT&E"
    })

// Create Competency 4B.1 - IDSK
CREATE
  (c4b1:Competency:DoteKsat
    {
      id: "comp_4b_1",
      name: "IDSK",
      description:
        "Correctly identify and help efficiently codify qualified integrated T&E data and independent OT&E and LFT&E data and M&S results needed to appropriately inform the acquisition and program decisions; increase T&E efficiency; and support the evaluation of operational effectiveness, suitability, survivability, and lethality (as applicable) across the acquisition life cycle, in support of each acquisition decision.",
      competency_statement:
        "Identifies and codifies integrated T&E data to inform acquisition decisions",
      competency_framework: "TEMP/T&E Strategy Development",
      resource_association: "IDSK_Management_Systems",
      type_label: "IDSK",
      type_uri: "http://competency.dod.mil/idsk",
      PROFILE: "KSAT",
      ksat_type: "Skill"
    })

// Create Competency 4B.2 - OT&E
CREATE
  (c4b2:Competency:DoteKsat
    {
      id: "comp_4b_2",
      name: "OT&E",
      description:
        "Understands and implements DoD policy for OT&E. Considers measures, metrics, and statistical methods to maximize use of available data and design the OT&E to evaluate, with scientific rigor, the operational effectiveness and suitability of a production or fielding representative DoD systems in operationally relevant and representative contested, congested, and constrained environments while taking into equal consideration survivability and lethality effects (as applicable).",
      competency_statement:
        "Implements OT&E policy with scientific rigor in contested environments",
      competency_framework: "TEMP/T&E Strategy Development",
      resource_association: "OT&E_Planning_Systems",
      type_label: "OT&E",
      type_uri: "http://competency.dod.mil/ote",
      PROFILE: "KSAT",
      ksat_type: "Ability"
    })

// Create Competency 4B.3 - LFT&E
CREATE
  (c4b3:Competency:DoteKsat
    {
      id: "comp_4b_3",
      name: "LFT&E",
      description:
        "Understands and implements DoD policy for LFT&E. Considers measures, metrics, and statistical methods to maximize use of available data and design LFT&E to evaluate, with scientific rigor, realistic, full spectrum survivability and lethality (as applicable) of a combat-loaded system in operationally relevant and representative contested, congested, and constrained environments using live kinetic and non-kinetic threats and targets (or their surrogates) and their combined effects.",
      competency_statement:
        "Implements LFT&E policy with scientific rigor for survivability and lethality evaluation",
      competency_framework: "TEMP/T&E Strategy Development",
      resource_association: "LFT&E_Planning_Systems",
      type_label: "LFT&E",
      type_uri: "http://competency.dod.mil/lfte",
      PROFILE: "KSAT",
      ksat_type: "Ability"
    })

// Create Competency 4B.4 - M&S
CREATE
  (c4b4:Competency:DoteKsat
    {
      id: "comp_4b_4",
      name: "M&S",
      description:
        "Understands and implements DoD policy for M&S VV&A for OT&E and LFT&E. Understands and implements a scientifically rigorous verification, validation, and accreditation (VV&A) that includes uncertainty quantification of M&S results using statistical methods.",
      competency_statement:
        "Implements scientifically rigorous M&S VV&A with uncertainty quantification",
      competency_framework: "TEMP/T&E Strategy Development",
      resource_association: "M&S_VV&A_Systems",
      type_label: "M&S",
      type_uri: "http://competency.dod.mil/ms_vva",
      PROFILE: "KSAT",
      ksat_type: "Knowledge"
    })

// Create Competency 4B.5 - Resources
CREATE
  (c4b5:Competency:DoteKsat
    {
      id: "comp_4b_5",
      name: "Resources",
      description:
        "Develop an independent T&E Concept to inform the TEMP/T&E strategy and OT&E and LFT&E plans and identify T&E resources needed to implement the TEMP/T&E strategy. Identify T&E resources gaps and their effect on the adequacy of the TEMP/T&E strategy, OT&E and LFT&E plans. Inform and coordinate with the DOT&E Pillar 1 lead on T&E resources gaps and proposed solutions.",
      competency_statement:
        "Develops independent T&E concepts and identifies resource gaps for TEMP strategy",
      competency_framework: "TEMP/T&E Strategy Development",
      resource_association: "T&E_Resource_Management",
      type_label: "Resources",
      type_uri: "http://competency.dod.mil/te_resources",
      PROFILE: "KSAT",
      ksat_type: "Skill"
    })

// Create Competency 4B.6 - Cost
CREATE
  (c4b6:Competency:DoteKsat
    {
      id: "comp_4b_6",
      name: "Cost",
      description:
        "Provide an independent assessment of the cost of required OT&E, LFT&E and M&S including FUSL, alternate LFT&E strategy, and M&S VV&A to evaluate the TEMP/T&E strategy adequacy.",
      competency_statement:
        "Provides independent cost assessments for T&E strategy adequacy evaluation",
      competency_framework: "TEMP/T&E Strategy Development",
      resource_association: "Cost_Analysis_Tools",
      type_label: "Cost",
      type_uri: "http://competency.dod.mil/te_cost",
      PROFILE: "KSAT",
      ksat_type: "Skill"
    })

// Create HAS_COMPETENCY relationships
CREATE (f4b)-[:HAS_COMPETENCY]->(c4b1)

CREATE (f4b)-[:HAS_COMPETENCY]->(c4b2)

CREATE (f4b)-[:HAS_COMPETENCY]->(c4b3)

CREATE (f4b)-[:HAS_COMPETENCY]->(c4b4)

CREATE (f4b)-[:HAS_COMPETENCY]->(c4b5)

CREATE (f4b)-[:HAS_COMPETENCY]->(c4b6)

// Create Framework #4C
CREATE
  (f4c:Framework
    {
      id: "comp_framework_4c",
      name: "Modeling and Simulation VV&A",
      authoritative_source: "DoD T&E Framework",
      resource_association: "DoD_M&S_VV&A_Systems",
      description:
        "Understands and implements DoD policy for M&S VV&A for OT&E and LFT&E. Understands and implements a scientifically rigorous verification, validation, and accreditation (VV&A) that includes uncertainty quantification of M&S results using statistical methods.",
      start_date: datetime("2024-01-01T00:00:00Z"),
      end_date: datetime("2025-12-31T23:59:59Z"),
      association: "DoD_M&S_VV&A",
      PROFILE: "DOT&E"
    })

// Create Competency 4C.1 - M&S Intended Use
CREATE
  (c4c1:Competency:DoteKsat
    {
      id: "comp_4c_1",
      name: "M&S Intended Use",
      description:
        "Understands different types of M&S and how they support OT&E and LFT&E across the acquisition life cycle.",
      competency_statement:
        "Understands M&S types and their application to T&E across acquisition lifecycle",
      competency_framework: "Modeling and Simulation VV&A",
      resource_association: "M&S_Type_Classification",
      type_label: "M&S Intended Use",
      type_uri: "http://competency.dod.mil/ms_intended_use",
      PROFILE: "KSAT",
      ksat_type: "Knowledge"
    })

// Create Competency 4C.2 - M&S Capability Assessment
CREATE
  (c4c2:Competency:DoteKsat
    {
      id: "comp_4c_2",
      name: "M&S Capability Assessment",
      description:
        "Determines the feasibility and benefits of using M&S to support OT&E or LFT&E.",
      competency_statement:
        "Determines M&S feasibility and benefits for T&E support",
      competency_framework: "Modeling and Simulation VV&A",
      resource_association: "M&S_Assessment_Tools",
      type_label: "M&S Capability Assessment",
      type_uri: "http://competency.dod.mil/ms_capability_assessment",
      PROFILE: "KSAT",
      ksat_type: "Skill"
    })

// Create Competency 4C.3 - M&S Management
CREATE
  (c4c3:Competency:DoteKsat
    {
      id: "comp_4c_3",
      name: "M&S Management",
      description:
        "Understands the M&S management, including roles and responsibilities across organizations, and associated definitions such as modeling, simulation, verification, validation, accreditation, uncertainty quantification, etc.",
      competency_statement:
        "Understands M&S management roles and VV&A terminology",
      competency_framework: "Modeling and Simulation VV&A",
      resource_association: "M&S_Management_Framework",
      type_label: "M&S Management",
      type_uri: "http://competency.dod.mil/ms_management",
      PROFILE: "KSAT",
      ksat_type: "Knowledge"
    })

// Create Competency 4C.4 - M&S Requirements
CREATE
  (c4c4:Competency:DoteKsat
    {
      id: "comp_4c_4",
      name: "M&S Requirements",
      description:
        "Assesses the M&S, VV&A requirements, and acceptability criteria to meet OT&E or LFT&E objectives and ensure rigorous VV&A. Identifies M&S outputs and live data requirements, criteria for comparing M&S to live data, and quantitative methods of comparing data and calculating associated uncertainties in support of VV&A.",
      competency_statement:
        "Assesses M&S VV&A requirements and data comparison criteria",
      competency_framework: "Modeling and Simulation VV&A",
      resource_association: "M&S_Requirements_Tools",
      type_label: "M&S Requirements",
      type_uri: "http://competency.dod.mil/ms_requirements",
      PROFILE: "KSAT",
      ksat_type: "Skill"
    })

// Create Competency 4C.5 - M&S Planning and Analysis
CREATE
  (c4c5:Competency:DoteKsat
    {
      id: "comp_4c_5",
      name: "M&S Planning and Analysis",
      description:
        "Understands and applies statistical and other methods that can be useful for scoping and analyzing M&S outputs (e.g., design of experiments, uncertainty quantification, extrapolation, statistical modeling).",
      competency_statement:
        "Applies statistical methods for M&S output analysis and uncertainty quantification",
      competency_framework: "Modeling and Simulation VV&A",
      resource_association: "Statistical_Analysis_Tools",
      type_label: "M&S Planning and Analysis",
      type_uri: "http://competency.dod.mil/ms_planning_analysis",
      PROFILE: "KSAT",
      ksat_type: "Ability"
    })

// Create Competency 4C.6 - M&S Independent Review
CREATE
  (c4c6:Competency:DoteKsat
    {
      id: "comp_4c_6",
      name: "M&S Independent Review",
      description:
        "Supports the review process of M&S VV&A reports and independently analyzes the M&S V&V results for record to determine their use in supporting DOT&E's evaluation of operational effectiveness, suitability, survivability, and lethality (as applicable).",
      competency_statement:
        "Conducts independent M&S VV&A review and analysis for DOT&E evaluations",
      competency_framework: "Modeling and Simulation VV&A",
      resource_association: "M&S_Review_Framework",
      type_label: "M&S Independent Review",
      type_uri: "http://competency.dod.mil/ms_independent_review",
      PROFILE: "KSAT",
      ksat_type: "Ability"
    })

// Create Competency 4C.7 - M&S Evaluation
CREATE
  (c4c7:Competency:DoteKsat
    {
      id: "comp_4c_7",
      name: "M&S Evaluation",
      description:
        "Determines whether the test data collected using M&S tools are sufficient to adequately supplement data collected during OT or LFT to facilitate a credible evaluation of the system. Understands the risks of using unvalidated M&S.",
      competency_statement:
        "Evaluates M&S data sufficiency and understands unvalidated M&S risks",
      competency_framework: "Modeling and Simulation VV&A",
      resource_association: "M&S_Evaluation_Tools",
      type_label: "M&S Evaluation",
      type_uri: "http://competency.dod.mil/ms_evaluation",
      PROFILE: "KSAT",
      ksat_type: "Ability"
    })

// Create HAS_COMPETENCY relationships
CREATE (f4c)-[:HAS_COMPETENCY]->(c4c1)

CREATE (f4c)-[:HAS_COMPETENCY]->(c4c2)

CREATE (f4c)-[:HAS_COMPETENCY]->(c4c3)

CREATE (f4c)-[:HAS_COMPETENCY]->(c4c4)

CREATE (f4c)-[:HAS_COMPETENCY]->(c4c5)

CREATE (f4c)-[:HAS_COMPETENCY]->(c4c6)

CREATE (f4c)-[:HAS_COMPETENCY]->(c4c7)

// Create Framework #4D
CREATE
  (f4d:Framework
    {
      id: "comp_framework_4d",
      name: "Full Spectrum Survivability and Lethality",
      authoritative_source: "DoD T&E Framework",
      resource_association: "DoD_LFT&E_Systems",
      description:
        "Understands and implements DoD policy for LFT&E. Considers measures, metrics, and statistical methods to maximize use of available data and design LFT&E to evaluate, with scientific rigor, realistic, full spectrum survivability and lethality (as applicable) of a combat-loaded system in operationally relevant and representative contested, congested, and constrained environments using live kinetic and non-kinetic threats and targets (or their surrogates) and their combined effects.",
      start_date: datetime("2024-01-01T00:00:00Z"),
      end_date: datetime("2025-12-31T23:59:59Z"),
      association: "DoD_LFT&E",
      PROFILE: "DOT&E"
    })

// Create Competency 4D.1 - Full Spectrum Survivability Kill Chain
CREATE
  (c4d1:Competency:DoteKsat
    {
      id: "comp_4d_1",
      name: "Full Spectrum Survivability Kill Chain",
      description:
        "Understands measures, metrics, and methods to evaluate full spectrum survivability with scientific rigor in an operationally representative and relevant contested, congested, and constrained environment across the acquisition life cycle including operations and sustainment. Supports the evaluation of the DoD system survivability kill chain including: (1) susceptibility to attack or engagement, (2) vulnerability to attack evaluation of the effect of the vulnerability on operational effectiveness and suitability, (3) effect of the attack or engagement on user casualties, (4) recoverability from the attack, and (5) coordinated, full spectrum attack effects.",
      competency_statement:
        "Evaluates full spectrum survivability kill chain with scientific rigor across lifecycle",
      competency_framework: "Full Spectrum Survivability and Lethality",
      resource_association: "Survivability_Kill_Chain_Tools",
      type_label: "Full Spectrum Survivability Kill Chain",
      type_uri: "http://competency.dod.mil/survivability_kill_chain",
      PROFILE: "KSAT",
      ksat_type: "Ability"
    })

// Create Competency 4D.2 - Kinetic Threats T&E
CREATE
  (c4d2:Competency:DoteKsat
    {
      id: "comp_4d_2",
      name: "Kinetic Threats T&E",
      description:
        "Understands and applies susceptibility, vulnerability, user casualties (as applicable), recoverability and collateral damage to support survivability evaluation against kinetic threat effects (e.g., penetration (projectile, fragmentation), shock, blast, and fire effects on the DoD system or adversary target) in a contested kinetic threat environment.",
      competency_statement:
        "Applies survivability evaluation against kinetic threat effects in contested environment",
      competency_framework: "Full Spectrum Survivability and Lethality",
      resource_association: "Kinetic_Threat_Testing_Tools",
      type_label: "Kinetic Threats T&E",
      type_uri: "http://competency.dod.mil/kinetic_threats",
      PROFILE: "KSAT",
      ksat_type: "Skill"
    })

// Create Competency 4D.3 - Cyber T&E
CREATE
  (c4d3:Competency:DoteKsat
    {
      id: "comp_4d_3",
      name: "Cyber T&E",
      description:
        "Understands and applies susceptibility (prevent), vulnerability (mitigate), user casualties (as applicable), recoverability (recover) and collateral damage to support survivability evaluation against cyberattack (e.g., deny, degrade, disrupt, deceive, destroy, exploit, or influence, including cascading effects in the physical domains) in a contested and congested cyberspace.",
      competency_statement:
        "Applies survivability evaluation against cyberattacks in contested cyberspace",
      competency_framework: "Full Spectrum Survivability and Lethality",
      resource_association: "Cyber_Testing_Tools",
      type_label: "Cyber T&E",
      type_uri: "http://competency.dod.mil/cyber_te",
      PROFILE: "KSAT",
      ksat_type: "Skill"
    })

// Create Competency 4D.4 - EMSO T&E
CREATE
  (c4d4:Competency:DoteKsat
    {
      id: "comp_4d_4",
      name: "EMSO T&E",
      description:
        "Understands and applies susceptibility (prevent), vulnerability (mitigate), user casualties (as applicable), recoverability (recover) and collateral damage to support survivability evaluation against electromagnetic spectrum fires (e.g., deny, degrade, disrupt, deceive, destroy, exploit, or influence, including cascading effects in the physical domains) in a contested and congested, and constrained EMSO). Includes directed energy: electromagnetic attack or spectrum effects such as wideband radio frequency, lasers; and high-power microwaves.",
      competency_statement:
        "Applies survivability evaluation against electromagnetic spectrum fires and directed energy",
      competency_framework: "Full Spectrum Survivability and Lethality",
      resource_association: "EMSO_Testing_Tools",
      type_label: "EMSO T&E",
      type_uri: "http://competency.dod.mil/emso_te",
      PROFILE: "KSAT",
      ksat_type: "Skill"
    })

// Create Competency 4D.5 - CBRN T&E
CREATE
  (c4d5:Competency:DoteKsat
    {
      id: "comp_4d_5",
      name: "CBRN T&E",
      description:
        "Understands and applies susceptibility, vulnerability, user casualties, recoverability and collateral damage to support survivability evaluation against CBRN threats (e.g., chemical and biological agents or radioactive particles, electromagnetic pulse, blast, and thermal energy (nuclear events).",
      competency_statement:
        "Applies survivability evaluation against CBRN threats and nuclear effects",
      competency_framework: "Full Spectrum Survivability and Lethality",
      resource_association: "CBRN_Testing_Tools",
      type_label: "CBRN T&E",
      type_uri: "http://competency.dod.mil/cbrn_te",
      PROFILE: "KSAT",
      ksat_type: "Knowledge"
    })

// Create Competency 4D.6 - Lethality Kill Chain
CREATE
  (c4d6:Competency:DoteKsat
    {
      id: "comp_4d_6",
      name: "Lethality Kill Chain",
      description:
        "Understands measures, metrics, and methods required to support an evaluation of full spectrum lethality with scientific rigor in an operationally representative and relevant contested, congested, and constrained environment across the acquisition life cycle including operations and sustainment. Considers the adversary TTP and the adversary kill-chain; and will include but not be limited to: (1) offensive capability lethal mechanism, (2) offensive capabilities against operationally representative and realistic functional, physical, or information materials and targets, as fired from the host platform or the warfighter, (3) offensive capabilities in the presence of adversaries' susceptibility and vulnerability reduction effects, and (4) effect of an offensive attack on collateral damage.",
      competency_statement:
        "Evaluates full spectrum lethality kill chain with scientific rigor across lifecycle",
      competency_framework: "Full Spectrum Survivability and Lethality",
      resource_association: "Lethality_Kill_Chain_Tools",
      type_label: "Lethality Kill Chain",
      type_uri: "http://competency.dod.mil/lethality_kill_chain",
      PROFILE: "KSAT",
      ksat_type: "Ability"
    })

// Create HAS_COMPETENCY relationships
CREATE (f4d)-[:HAS_COMPETENCY]->(c4d1)

CREATE (f4d)-[:HAS_COMPETENCY]->(c4d2)

CREATE (f4d)-[:HAS_COMPETENCY]->(c4d3)

CREATE (f4d)-[:HAS_COMPETENCY]->(c4d4)

CREATE (f4d)-[:HAS_COMPETENCY]->(c4d5)

CREATE (f4d)-[:HAS_COMPETENCY]->(c4d6)

// Create Framework #5
CREATE
  (f5:Framework
    {
      id: "comp_framework_5",
      name: "Software",
      authoritative_source: "DoD T&E Framework",
      resource_association: "DoD_Software_T&E_Systems",
      description:
        "Understands and can implement DoD policy for OT&E and LFT&E of software intensive systems and software embedded in systems to evaluate, with scientific rigor, the operational effectiveness, suitability, survivability, and lethality (as applicable) of DoD systems in support of the delivery of each incremental capability.",
      start_date: datetime("2024-01-01T00:00:00Z"),
      end_date: datetime("2025-12-31T23:59:59Z"),
      association: "DoD_Software_T&E",
      PROFILE: "DOT&E"
    })

// Create Competency 5.1 - Mission Context
CREATE
  (c51:Competency:DoteKsat
    {
      id: "comp_5_1",
      name: "Mission Context",
      description:
        "Builds understanding of mission(s) the software will support, to scope the operational testing to those missions. Further builds understanding of deployment strategy, including training strategy, to align operational testing to the capabilities delivered.",
      competency_statement:
        "Builds mission understanding to scope operational testing and align with deployment strategy",
      competency_framework: "Software",
      resource_association: "Mission_Analysis_Tools",
      type_label: "Mission Context",
      type_uri: "http://competency.dod.mil/software_mission_context",
      PROFILE: "KSAT",
      ksat_type: "Knowledge"
    })

// Create Competency 5.2 - Software Development
CREATE
  (c52:Competency:DoteKsat
    {
      id: "comp_5_2",
      name: "Software Development",
      description:
        "Demonstrates an understanding of agile and DevSecOps methodologies and their associated terminologies for iterative software development. Further understands testing conducted throughout development. Identifies and understands limitations of testing conducted throughout the development for use in operational evaluations.",
      competency_statement:
        "Understands agile/DevSecOps methodologies and development testing limitations",
      competency_framework: "Software",
      resource_association: "DevSecOps_Tools",
      type_label: "Software Development",
      type_uri: "http://competency.dod.mil/software_development",
      PROFILE: "KSAT",
      ksat_type: "Knowledge"
    })

// Create Competency 5.3 - Risk Based Approach
CREATE
  (c53:Competency:DoteKsat
    {
      id: "comp_5_3",
      name: "Risk Based Approach",
      description:
        "Applies a risk-based approach to scoping OT&E and LFT&E. Demonstrates the ability to outline the processes, frequency, and approval process for operational tests. Advocates for independent operational testing to be conducted as needed.",
      competency_statement:
        "Applies risk-based approach to T&E scoping and advocates for independent testing",
      competency_framework: "Software",
      resource_association: "Risk_Assessment_Framework",
      type_label: "Risk Based Approach",
      type_uri: "http://competency.dod.mil/software_risk_approach",
      PROFILE: "KSAT",
      ksat_type: "Skill"
    })

// Create Competency 5.4 - OT&E and LFT&E of Software
CREATE
  (c54:Competency:DoteKsat
    {
      id: "comp_5_4",
      name: "OT&E and LFT&E of Software",
      description:
        "Demonstrates an understanding of the basic OT&E and LFT&E responsibilities for T&E of software intensive and software embedded in DoD systems or services acquired via the Defense Acquisition System. Understands and can develop an operational testing strategy that balances the OT&E/LFT&E of the system with the deployment rate of the system to inform decision makers on operational effectiveness, suitability, survivability, and lethality.",
      competency_statement:
        "Develops operational testing strategy balancing T&E with software deployment rate",
      competency_framework: "Software",
      resource_association: "Software_T&E_Strategy_Tools",
      type_label: "OT&E and LFT&E of Software",
      type_uri: "http://competency.dod.mil/software_ote_lfte",
      PROFILE: "KSAT",
      ksat_type: "Ability"
    })

// Create Competency 5.5 - Test Automation
CREATE
  (c55:Competency:DoteKsat
    {
      id: "comp_5_5",
      name: "Test Automation",
      description:
        "Understands test automation use cases and how automated test data is designed into systems to support planning and execution of functional, regression, performance, and survivability testing.",
      competency_statement:
        "Understands test automation use cases and automated test data design",
      competency_framework: "Software",
      resource_association: "Test_Automation_Tools",
      type_label: "Test Automation",
      type_uri: "http://competency.dod.mil/test_automation",
      PROFILE: "KSAT",
      ksat_type: "Skill"
    })

// Create Competency 5.6 - Support to Decisions
CREATE
  (c56:Competency:DoteKsat
    {
      id: "comp_5_6",
      name: "Support to Decisions",
      description:
        "Understands how the role of automated and manual Software T&E maintains cadence with software development decision points and acquisition decision points.",
      competency_statement:
        "Understands T&E cadence with software development and acquisition decision points",
      competency_framework: "Software",
      resource_association: "Decision_Support_Tools",
      type_label: "Support to Decisions",
      type_uri: "http://competency.dod.mil/software_decision_support",
      PROFILE: "KSAT",
      ksat_type: "Knowledge"
    })

// Create Competency 5.7 - Infrastructure
CREATE
  (c57:Competency:DoteKsat
    {
      id: "comp_5_7",
      name: "Infrastructure",
      description:
        "Develops an understanding of underlying hardware and software infrastructure, including differences that may affect the operational performance, and including interfacing systems, to scope testing for the system-of-systems, as applicable. Supports VV&A activities of the infrastructure to determine applicability of testing data to operational evaluations.",
      competency_statement:
        "Understands infrastructure impacts on performance and supports VV&A activities",
      competency_framework: "Software",
      resource_association: "Infrastructure_Analysis_Tools",
      type_label: "Infrastructure",
      type_uri: "http://competency.dod.mil/software_infrastructure",
      PROFILE: "KSAT",
      ksat_type: "Skill"
    })

// Create HAS_COMPETENCY relationships
CREATE (f5)-[:HAS_COMPETENCY]->(c51)

CREATE (f5)-[:HAS_COMPETENCY]->(c52)

CREATE (f5)-[:HAS_COMPETENCY]->(c53)

CREATE (f5)-[:HAS_COMPETENCY]->(c54)

CREATE (f5)-[:HAS_COMPETENCY]->(c55)

CREATE (f5)-[:HAS_COMPETENCY]->(c56)

CREATE (f5)-[:HAS_COMPETENCY]->(c57)

// Create Framework #6
CREATE
  (f6:Framework
    {
      id: "comp_framework_6",
      name: "Artificial Intelligence",
      authoritative_source: "DoD T&E Framework",
      resource_association: "DoD_AI_T&E_Systems",
      description:
        "Understand and implement DoD policy for OT&E and LFT&E of Artificial Intelligence (AI)-Based and Autonomous Systems. Understand aspects of AI such as tools, models, design, testing and evaluation protocols.",
      start_date: datetime("2024-01-01T00:00:00Z"),
      end_date: datetime("2025-12-31T23:59:59Z"),
      association: "DoD_AI_T&E",
      PROFILE: "DOT&E"
    })

// Create Competency 6.1 - AI Awareness
CREATE
  (c61:Competency:DoteKsat
    {
      id: "comp_6_1",
      name: "AI Awareness",
      description:
        "Understands how AI presents challenges as a subject of OT&E and LFT&E and how AI can enable future improvements in T&E effectiveness and efficiency.",
      competency_statement:
        "Understands AI challenges in T&E and potential for T&E improvements",
      competency_framework: "Artificial Intelligence",
      resource_association: "AI_T&E_Awareness_Tools",
      type_label: "AI Awareness",
      type_uri: "http://competency.dod.mil/ai_awareness",
      PROFILE: "KSAT",
      ksat_type: "Knowledge"
    })

// Create Competency 6.2 - AI T&E Policy and Ethics
CREATE
  (c62:Competency:DoteKsat
    {
      id: "comp_6_2",
      name: "AI T&E Policy and Ethics",
      description:
        "Understands the policy, law and ethical considerations in performing T&E on AI-enabled systems. Understands the five AI ethical principles (responsible, equitable, traceable, reliable, and governable) and how they can be measured during the evaluation of AI systems.",
      competency_statement:
        "Understands AI T&E policy, law, and ethical principles measurement",
      competency_framework: "Artificial Intelligence",
      resource_association: "AI_Ethics_Framework",
      type_label: "AI T&E Policy and Ethics",
      type_uri: "http://competency.dod.mil/ai_policy_ethics",
      PROFILE: "KSAT",
      ksat_type: "Knowledge"
    })

// Create Competency 6.3 - Dataset Relevancy
CREATE
  (c63:Competency:DoteKsat
    {
      id: "comp_6_3",
      name: "Dataset Relevancy",
      description:
        "Can distinguish between training, validation, and test datasets and can identify if the training dataset is operationally representative to ensure that AI model testing is more relevant to OT and LFT.",
      competency_statement:
        "Distinguishes dataset types and ensures operational representativeness for AI testing",
      competency_framework: "Artificial Intelligence",
      resource_association: "AI_Dataset_Analysis_Tools",
      type_label: "Dataset Relevancy",
      type_uri: "http://competency.dod.mil/ai_dataset_relevancy",
      PROFILE: "KSAT",
      ksat_type: "Skill"
    })

// Create Competency 6.4 - AI Planning
CREATE
  (c64:Competency:DoteKsat
    {
      id: "comp_6_4",
      name: "AI Planning",
      description:
        "Understands the requirements, screening characterization, designing factors, recording conditions, identifying constraints, test matrices for AI planning efforts, and demonstrates the ability to determine the confidence level and power of hypothesis tests.",
      competency_statement:
        "Understands AI planning requirements and demonstrates hypothesis testing capabilities",
      competency_framework: "Artificial Intelligence",
      resource_association: "AI_Planning_Tools",
      type_label: "AI Planning",
      type_uri: "http://competency.dod.mil/ai_planning",
      PROFILE: "KSAT",
      ksat_type: "Skill"
    })

// Create Competency 6.5 - AI Performance
CREATE
  (c65:Competency:DoteKsat
    {
      id: "comp_6_5",
      name: "AI Performance",
      description:
        "Demonstrates the ability to confirm that the information received from AI-enabled systems and data is accurate, precise, recallable, and robust.",
      competency_statement:
        "Confirms AI system information accuracy, precision, recallability, and robustness",
      competency_framework: "Artificial Intelligence",
      resource_association: "AI_Performance_Assessment_Tools",
      type_label: "AI Performance",
      type_uri: "http://competency.dod.mil/ai_performance",
      PROFILE: "KSAT",
      ksat_type: "Skill"
    })

// Create Competency 6.6 - Human-Machine Teaming
CREATE
  (c66:Competency:DoteKsat
    {
      id: "comp_6_6",
      name: "Human-Machine Teaming",
      description:
        "Understands human-machine science and test approaches that include cognitive and physiological assessments of human operators to inform system development. Understands the role of the human-machine evaluation strategy within the larger TEMP/T&E Strategy.",
      competency_statement:
        "Understands human-machine science and evaluation strategy within TEMP",
      competency_framework: "Artificial Intelligence",
      resource_association: "Human_Machine_Teaming_Tools",
      type_label: "Human-Machine Teaming",
      type_uri: "http://competency.dod.mil/human_machine_teaming",
      PROFILE: "KSAT",
      ksat_type: "Knowledge"
    })

// Create Competency 6.7 - AI Application
CREATE
  (c67:Competency:DoteKsat
    {
      id: "comp_6_7",
      name: "AI Application",
      description:
        "Understands the application of AI tools and systems; applies the processes, principles, and technologies inherent in DevSecOps; uses ML models and prediction methods for evaluating AI performance; communicates best practices for AI/ML T&E validation and verification to the T&E enterprise from the field, DoD Partners, academia, and industry; and leverages AI capabilities in designing tests and analyzing results.",
      competency_statement:
        "Applies AI tools, DevSecOps, and ML models while communicating best practices",
      competency_framework: "Artificial Intelligence",
      resource_association: "AI_Application_Framework",
      type_label: "AI Application",
      type_uri: "http://competency.dod.mil/ai_application",
      PROFILE: "KSAT",
      ksat_type: "Ability"
    })

// Create Competency 6.8 - AI Visualization
CREATE
  (c68:Competency:DoteKsat
    {
      id: "comp_6_8",
      name: "AI Visualization",
      description:
        "Demonstrates the ability to evaluate graphical representations of AI data and understands the importance of evaluating ML model performance through visualization tools for communicating the results to stakeholders.",
      competency_statement:
        "Evaluates AI data visualizations and ML model performance for stakeholder communication",
      competency_framework: "Artificial Intelligence",
      resource_association: "AI_Visualization_Tools",
      type_label: "AI Visualization",
      type_uri: "http://competency.dod.mil/ai_visualization",
      PROFILE: "KSAT",
      ksat_type: "Skill"
    })

// Create Competency 6.9 - AI Capabilities Assessment
CREATE
  (c69:Competency:DoteKsat
    {
      id: "comp_6_9",
      name: "AI Capabilities Assessment",
      description:
        "Understands AI tools and coding, can identify issues in ML models and common frameworks used to implement AI methods; recognizes potential use cases to integrate AI into T&E, and leverages AI capabilities in analyzing results.",
      competency_statement:
        "Understands AI tools, identifies ML model issues, and leverages AI for T&E integration",
      competency_framework: "Artificial Intelligence",
      resource_association: "AI_Capabilities_Assessment_Tools",
      type_label: "AI Capabilities Assessment",
      type_uri: "http://competency.dod.mil/ai_capabilities_assessment",
      PROFILE: "KSAT",
      ksat_type: "Ability"
    })

// Create HAS_COMPETENCY relationships
CREATE (f6)-[:HAS_COMPETENCY]->(c61)

CREATE (f6)-[:HAS_COMPETENCY]->(c62)

CREATE (f6)-[:HAS_COMPETENCY]->(c63)

CREATE (f6)-[:HAS_COMPETENCY]->(c64)

CREATE (f6)-[:HAS_COMPETENCY]->(c65)

CREATE (f6)-[:HAS_COMPETENCY]->(c66)

CREATE (f6)-[:HAS_COMPETENCY]->(c67)

CREATE (f6)-[:HAS_COMPETENCY]->(c68)

CREATE (f6)-[:HAS_COMPETENCY]->(c69)

// Create Framework #7
CREATE
  (f7:Framework
    {
      id: "comp_framework_7",
      name: "Leadership",
      authoritative_source: "DoD T&E Framework",
      resource_association: "DoD_Leadership_Development_Systems",
      description:
        "Demonstrate personal and professional attributes of effective leaders to lead change; lead people; deliver results; manage human capital, finances, and technology; and build coalitions.",
      start_date: datetime("2024-01-01T00:00:00Z"),
      end_date: datetime("2025-12-31T23:59:59Z"),
      association: "DoD_Leadership_Development",
      PROFILE: "DOT&E"
    })

// Create Competency 7.1 - Professional Ethics
CREATE
  (c71:Competency:DoteKsat
    {
      id: "comp_7_1",
      name: "Professional Ethics",
      description:
        "Understands the guidelines of professional and personal conduct of DOT&E ethical standards and provides clear direction and expectations when engaging with OTAs and LFT&E organizations to set and track against explicit and defensible positions throughout OT&E and LFT&E.",
      competency_statement:
        "Understands DOT&E ethical standards and provides clear direction to T&E organizations",
      competency_framework: "Leadership",
      resource_association: "Ethics_Guidelines_Framework",
      type_label: "Professional Ethics",
      type_uri: "http://competency.dod.mil/professional_ethics",
      PROFILE: "KSAT",
      ksat_type: "Knowledge"
    })

// Create Competency 7.2 - Collaboration and Partnerships
CREATE
  (c72:Competency:DoteKsat
    {
      id: "comp_7_2",
      name: "Collaboration and Partnerships",
      description:
        "Inspires and fosters collaboration, partnership, team commitment, and trust inside and outside of DOT&E. Facilitates cooperation and motivates team members to accomplish group goals.",
      competency_statement:
        "Inspires collaboration and partnership while motivating teams to accomplish goals",
      competency_framework: "Leadership",
      resource_association: "Collaboration_Tools",
      type_label: "Collaboration and Partnerships",
      type_uri: "http://competency.dod.mil/collaboration_partnerships",
      PROFILE: "KSAT",
      ksat_type: "Ability"
    })

// Create Competency 7.3 - Conflict Resolution
CREATE
  (c73:Competency:DoteKsat
    {
      id: "comp_7_3",
      name: "Conflict Resolution",
      description:
        "Engages with DOT&E leadership in advance, when necessary, to discuss notable test planning concerns and resolve potential issues and creates resolution channels for arbitrating test program issues/disagreements that cannot be resolved at the working level.",
      competency_statement:
        "Engages leadership to resolve test planning concerns and creates resolution channels",
      competency_framework: "Leadership",
      resource_association: "Conflict_Resolution_Framework",
      type_label: "Conflict Resolution",
      type_uri: "http://competency.dod.mil/conflict_resolution",
      PROFILE: "KSAT",
      ksat_type: "Skill"
    })

// Create Competency 7.4 - Creativity and Innovation
CREATE
  (c74:Competency:DoteKsat
    {
      id: "comp_7_4",
      name: "Creativity and Innovation",
      description:
        "Develops new insights into situations; questions conventional approaches; encourages new ideas and innovations; designs and implements new or cutting-edge programs/processes.",
      competency_statement:
        "Develops new insights, questions conventional approaches, and implements innovative programs",
      competency_framework: "Leadership",
      resource_association: "Innovation_Framework",
      type_label: "Creativity and Innovation",
      type_uri: "http://competency.dod.mil/creativity_innovation",
      PROFILE: "KSAT",
      ksat_type: "Ability"
    })

// Create Competency 7.5 - Strategic Thinking and Planning
CREATE
  (c75:Competency:DoteKsat
    {
      id: "comp_7_5",
      name: "Strategic Thinking and Planning",
      description:
        "Formulates objectives and priorities and implements plans consistent with long-term interests of the organization in a global environment and capitalizes on opportunities and manages risks.",
      competency_statement:
        "Formulates strategic objectives and implements long-term organizational plans",
      competency_framework: "Leadership",
      resource_association: "Strategic_Planning_Tools",
      type_label: "Strategic Thinking and Planning",
      type_uri: "http://competency.dod.mil/strategic_thinking_planning",
      PROFILE: "KSAT",
      ksat_type: "Ability"
    })

// Create Competency 7.6 - Workforce Development
CREATE
  (c76:Competency:DoteKsat
    {
      id: "comp_7_6",
      name: "Workforce Development",
      description:
        "Contributes to the design, development, and implementation of education and training programs to fill identified competency gaps in the workforce.",
      competency_statement:
        "Designs and implements education programs to address workforce competency gaps",
      competency_framework: "Leadership",
      resource_association: "Workforce_Development_Systems",
      type_label: "Workforce Development",
      type_uri: "http://competency.dod.mil/workforce_development",
      PROFILE: "KSAT",
      ksat_type: "Skill"
    })

// Create Competency 7.7 - Financial Management
CREATE
  (c77:Competency:DoteKsat
    {
      id: "comp_7_7",
      name: "Financial Management",
      description:
        "Understands the organization's financial processes and prepares, justifies, and administers the program budget and oversees procurement and contracting to achieve desired results. Monitors expenditures and uses cost-benefit thinking to set priorities.",
      competency_statement:
        "Manages organizational finances, budgets, and procurement with cost-benefit analysis",
      competency_framework: "Leadership",
      resource_association: "Financial_Management_Systems",
      type_label: "Financial Management",
      type_uri: "http://competency.dod.mil/financial_management",
      PROFILE: "KSAT",
      ksat_type: "Skill"
    })

// Create HAS_COMPETENCY relationships
CREATE (f7)-[:HAS_COMPETENCY]->(c71)

CREATE (f7)-[:HAS_COMPETENCY]->(c72)

CREATE (f7)-[:HAS_COMPETENCY]->(c73)

CREATE (f7)-[:HAS_COMPETENCY]->(c74)

CREATE (f7)-[:HAS_COMPETENCY]->(c75)

CREATE (f7)-[:HAS_COMPETENCY]->(c76)

CREATE (f7)-[:HAS_COMPETENCY]->(c77)