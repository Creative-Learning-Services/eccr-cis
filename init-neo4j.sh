#!/bin/bash
set -euo pipefail

AUTH_USER=${NEO4J_USERNAME:-neo4j}
AUTH_PASS=${NEO4J_PASSWORD:-neo4j}
AUTH_MODE=${NEO4J_AUTH:-none}
START_CMD="/startup/docker-entrypoint.sh neo4j"

MAX_RETRIES=30
SLEEP_SECONDS=1
WARN_AFTER=15
INIT_CYPHER=/var/lib/neo4j/init.cypher
SENTINEL=/data/.init_applied

echo "[neo4j-init] Starting Neo4j..."
${START_CMD} &

attempt=0
run_cypher() {
  local stmt="$1"
  if [[ "${AUTH_MODE}" == "none" ]]; then
    cypher-shell "${stmt}"
  else
    cypher-shell -u "${AUTH_USER}" -p "${AUTH_PASS}" "${stmt}"
  fi
}

while true; do
  if run_cypher "RETURN 1;" >/dev/null 2>&1; then
    echo "[neo4j-init] Database is available."
    break
  fi
  attempt=$((attempt+1))
  if [[ $attempt -eq $WARN_AFTER ]]; then
    echo "[neo4j-init][WARN] Still waiting. If this persists, password in data/dbms/auth.ini may not match NEO4J_PASSWORD."
  fi
  if [[ $attempt -ge $MAX_RETRIES ]]; then
    echo "[neo4j-init][ERROR] Gave up after ${MAX_RETRIES} attempts."
    echo "---- Neo4j recent log tail ----"
    tail -n 100 /logs/neo4j.log 2>/dev/null || true
    exit 1
  fi
  sleep "${SLEEP_SECONDS}"
done

if [[ -f "${INIT_CYPHER}" ]]; then
  if [[ ! -f "${SENTINEL}" ]]; then
    echo "[neo4j-init] Applying init.cypher... (auth mode: ${AUTH_MODE})"
    if [[ "${AUTH_MODE}" == "none" ]]; then
      if cypher-shell -f "${INIT_CYPHER}"; then
        touch "${SENTINEL}"
        echo "[neo4j-init] init.cypher applied successfully."
      else
        echo "[neo4j-init][ERROR] Failed to apply init.cypher."
        exit 1
      fi
    else
      if cypher-shell -u "${AUTH_USER}" -p "${AUTH_PASS}" -f "${INIT_CYPHER}"; then
        touch "${SENTINEL}"
        echo "[neo4j-init] init.cypher applied successfully."
      else
        echo "[neo4j-init][ERROR] Failed to apply init.cypher."
        exit 1
      fi
    fi
    echo "[neo4j-init] Backfilling missing uid properties where only id exists..."
    run_cypher 'MATCH (n) WHERE exists(n.id) AND n.uid IS NULL SET n.uid = n.id;' || echo "[neo4j-init][WARN] uid backfill failed"
  else
    echo "[neo4j-init] init.cypher already applied (marker present). Skipping."
  fi
else
  echo "[neo4j-init] No init.cypher found at ${INIT_CYPHER}; skipping."
fi

echo "[neo4j-init] Handing over control; keeping process in foreground."
wait