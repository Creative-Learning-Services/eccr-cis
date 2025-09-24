import threading
import socket
from urllib.parse import urlparse
from neo4j import GraphDatabase
from django.conf import settings

_driver_lock = threading.Lock()
_driver = None


def get_driver():
    global _driver
    if _driver is None:
        with _driver_lock:
            if _driver is None:
                uri = getattr(settings, "NEO4J_BOLT_URI", None) or getattr(
                    settings, "NEOMODEL_NEO4J_BOLT_URL", None
                )
                # Fallback for local test runs executed outside Docker network: resolve 'neo4j' host
                try:
                    parsed = urlparse(uri)
                    host = parsed.hostname
                    port = parsed.port or 7687
                    if host == "neo4j":
                        try:
                            socket.getaddrinfo(host, port)
                        except socket.gaierror:
                            # Replace only the host portion once
                            uri = uri.replace("neo4j", "localhost", 1)
                except Exception:
                    # Non-fatal; keep original uri
                    pass
                user = getattr(settings, "NEO4J_USERNAME", "neo4j")
                password = getattr(settings, "NEO4J_PASSWORD", "")
                # Always attempt auth; if password blank and server has auth disabled it will be ignored.
                auth = (user, password) if password != "" else (user, None)
                _driver = GraphDatabase.driver(uri, auth=auth)
    return _driver


def close_driver():
    global _driver
    if _driver:
        _driver.close()
        _driver = None
