import requests
from competencies.models import Configuration
from django.core.cache import cache


def ldss_get():
    """Function to get LDSS configuration value"""
    conf = Configuration.objects.first()
    ldss_endpoint = conf.ldss_host
    if not ldss_endpoint.endswith("/"):
        ldss_endpoint = ldss_endpoint + "/"
    if not ldss_endpoint.endswith("api/"):
        ldss_endpoint = ldss_endpoint + "api/"
    return ldss_endpoint


def read_json_data(schema_ref):
    """get schema from ldss and ingest as dictionary values"""
    # check cache for schema
    cached_schema = cache.get(schema_ref)
    if cached_schema:
        return cached_schema

    # if not in cache, connect to api
    ldss_host = ldss_get()
    request_path = ldss_host
    if schema_ref.startswith("xss:"):
        request_path += "schemas/?iri=" + schema_ref
    else:
        request_path += "schemas/?name=" + schema_ref
    schema = requests.get(request_path, verify=True, timeout=3.0)
    json_content = schema.json()["schema"]

    # save schema to cache
    cache.add(schema_ref, json_content, timeout=10)
    return json_content
