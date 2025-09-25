#!/usr/bin/env python3
"""
Demo script showing how to use the Graph Operations API endpoints

This script demonstrates how to call the three main endpoints:
1. Create nodes only
2. Create nodes with relationships
3. Create new node and relate to existing

Make sure your Django server is running before executing this script.
"""

import json
import requests
from typing import Dict, Any


# Base URL for your API (adjust as needed)
BASE_URL = "http://localhost:8000/api/v1"


def make_request(endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Make a POST request to the specified endpoint"""
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}

    print(f"\n🚀 Making request to: {url}")
    print(f"📦 Payload: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(url, json=payload, headers=headers)

        print(f"📈 Status Code: {response.status_code}")

        if response.status_code in [200, 201]:
            result = response.json()
            print(f"✅ Success: {json.dumps(result, indent=2)}")
            return result
        else:
            error = response.json() if response.content else {"error": "Unknown error"}
            print(f"❌ Error: {json.dumps(error, indent=2)}")
            return error

    except requests.exceptions.RequestException as e:
        print(f"🔥 Request failed: {e}")
        return {"error": str(e)}


def demo_create_nodes():
    """Demo: Create multiple nodes without relationships"""
    print("\n" + "=" * 60)
    print("DEMO 1: Create Nodes Only")
    print("=" * 60)

    payload = {
        "operation": "create_nodes",
        "description": "Demo: Create sample framework and competency nodes",
        "nodes": [
            {
                "label": "DCWFFramework",
                "properties": {
                    "id": "DCWFF-DEMO-001",
                    "name": "Demo DoD Cyber Workforce Framework",
                    "description": "Demo version of the Department of Defense's cyber workforce framework",
                    "authoritativeSource": "https://demo.cyber.mil/dcwf-framework",
                    "domain": "DCWF",
                    "conformsTo": "SCD 1.0",
                    "profile": ["Framework", "DCWFFramework"],
                },
            },
            {
                "label": "DCWFCompetency",
                "properties": {
                    "id": "DCWF-COMP-DEMO-001",
                    "name": "Demo Incident Response",
                    "description": "Demo competency for incident response coordination",
                    "competencyStatement": "Can lead incident response teams effectively",
                    "competencyLevel": "Expert",
                    "conformsTo": "SCD 1.0",
                    "profile": ["DCWFCompetency", "Competency"],
                },
            },
        ],
    }

    return make_request("/nodes/", payload)


def demo_create_relationship():
    """Demo: Create two nodes with a relationship"""
    print("\n" + "=" * 60)
    print("DEMO 2: Create Nodes with Relationship")
    print("=" * 60)

    payload = {
        "operation": "create_relationship",
        "description": "Demo: Create advanced work role and required knowledge with relationship",
        "source_node": {
            "label": "AdvancedWorkRole",
            "properties": {
                "id": "AWR-DEMO-001",
                "name": "Demo Senior Security Architect",
                "description": "Demo advanced work role for senior security architecture",
                "competencyStatement": "Can design enterprise security architectures",
                "type": "Advanced Work Role",
                "conformsTo": "SCD 1.0",
                "profile": ["work role", "competency"],
            },
        },
        "destination_node": {
            "label": "KsatsKnowledge",
            "properties": {
                "id": "KSAT-DEMO-001",
                "name": "Demo Security Architecture Principles",
                "description": "Demo knowledge of security architecture principles and frameworks",
                "competencyStatement": "Understands security architecture design principles",
                "type": "Knowledge",
                "Owner": "DEMO",
                "conformsTo": "SCD 1.0",
                "profile": ["ksats", "competency", "knowledge"],
            },
        },
        "relationship": {
            "edge_label": "REQUIRES",
            "properties": {
                "relationship_type": "competency_requirement",
                "priority": "high",
                "validation_status": "approved",
            },
        },
    }

    return make_request("/relationships/", payload)


def demo_create_relationship_to_existing():
    """Demo: Create new node and relate to existing (assumes Job node exists)"""
    print("\n" + "=" * 60)
    print("DEMO 3: Create Node and Relate to Existing")
    print("=" * 60)

    payload = {
        "operation": "create_relationship_to_existing",
        "description": "Demo: Create ability and relate to existing job",
        "new_node": {
            "label": "KsatsAbility",
            "properties": {
                "id": "KSAT-DEMO-ABILITY-001",
                "name": "Demo Threat Analysis",
                "description": "Demo ability to analyze cybersecurity threats",
                "competencyStatement": "Can analyze threat intelligence and produce reports",
                "type": "Ability",
                "Owner": "DEMO",
                "conformsTo": "SCD 1.0",
                "profile": ["ksats", "competency", "ability"],
            },
        },
        "existing_node_reference": {
            "label": "Job",
            "lookup_method": "by_id",
            "lookup_value": "WR-AN-EX-001",  # This should exist in your database
            "description": "Reference to existing Exploitation Analyst job",
        },
        "relationship": {
            "edge_label": "SUPPORTS",
            "direction": "from_existing_to_new",
            "properties": {
                "relationship_type": "job_ability_requirement",
                "criticality": "important",
                "validation_status": "pending_review",
            },
        },
        "validation": {
            "check_existing_node": True,
            "fail_if_not_exists": False,  # Don't fail if job doesn't exist
            "create_if_duplicate": False,
        },
    }

    return make_request("/relationships/existing/", payload)


def demo_health_check():
    """Demo: Check API and database health"""
    print("\n" + "=" * 60)
    print("DEMO: Health Check")
    print("=" * 60)

    url = f"{BASE_URL}/health/"

    try:
        response = requests.get(url)
        print(f"📈 Status Code: {response.status_code}")

        result = response.json()
        print(f"🏥 Health Status: {json.dumps(result, indent=2)}")

        return result

    except requests.exceptions.RequestException as e:
        print(f"🔥 Health check failed: {e}")
        return {"error": str(e)}


def main():
    """Run all demos"""
    print("🎯 Graph Operations API Demo")
    print("=" * 60)
    print("This demo will test all three graph operation endpoints")
    print("Make sure your Django server is running on localhost:8000")

    # Check health first
    health = demo_health_check()
    if health.get("status") != "healthy":
        print("\n❌ Database is not healthy. Please check your Neo4j connection.")
        return

    # Run demos
    results = []

    # Demo 1: Create nodes only
    result1 = demo_create_nodes()
    results.append(("Create Nodes", result1))

    # Demo 2: Create relationship between new nodes
    result2 = demo_create_relationship()
    results.append(("Create Relationship", result2))

    # Demo 3: Create node and relate to existing
    result3 = demo_create_relationship_to_existing()
    results.append(("Create Relationship to Existing", result3))

    # Summary
    print("\n" + "=" * 60)
    print("📊 DEMO SUMMARY")
    print("=" * 60)

    for demo_name, result in results:
        status = "✅ SUCCESS" if result.get("status") == "success" else "❌ FAILED"
        print(f"{demo_name}: {status}")
        if "error" in result:
            print(f"   Error: {result.get('message', result.get('error'))}")

    print("\n🎉 Demo completed!")


if __name__ == "__main__":
    main()
