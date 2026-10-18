#!/usr/bin/env bash
# Re-run the Bruno proof: owned local API + collection + reports + CSV iterations + OpenAPI import + docs.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; OUT="${OUT:-/tmp/bruno-proof}"; mkdir -p "$OUT"
command -v bru >/dev/null || npm i -g @usebruno/cli@4.2.1
python3 "$HERE/server.py" 8787 & SRV=$!; trap 'kill $SRV' EXIT; sleep 1
cd "$HERE/collection"
bru run --env local --env-var password=demo --reporter-json "$OUT/run.json" --reporter-junit "$OUT/run.xml" --reporter-html "$OUT/run.html"
bru run 02-login.bru 04-create-item.bru --env local --env-var password=demo --csv-file-path ../items.csv --reporter-json "$OUT/csv.json"
if bru run 02-login.bru --env local --env-var password=wrong --bail >/dev/null 2>&1; then echo "gate FAILED to fail"; exit 1; else echo "failure gate OK (non-zero exit)"; fi
bru import openapi -s "$HERE/openapi.yaml" -o "$OUT/imported" -n "KOSIF from OpenAPI" --collection-format bru
bru docs generate -o "$OUT/docs.html" --all-envs
