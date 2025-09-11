#!/bin/bash
set -e

# Start Neo4j in the background to allow cypher-shell to connect
/startup/docker-entrypoint.sh neo4j &

# Wait for Neo4j to be ready
echo "Waiting for Neo4j to start..."
# Use a loop to wait for the server to be up
until cypher-shell "RETURN 1" > /dev/null 2>&1; do
  echo -n "."
  sleep 1
done

echo "\nNeo4j started. Running init.cypher..."
# Run the cypher script using cypher-shell
cypher-shell -f /var/lib/neo4j/init.cypher

echo "init.cypher script finished."

# Bring the Neo4j process to the foreground to keep the container running
wait