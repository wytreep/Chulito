#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
compose=(docker compose -f postgres/compose.yaml)
cleanup() {
  "${compose[@]}" down --volumes --remove-orphans >/dev/null 2>&1 || true
}
trap cleanup EXIT

"${compose[@]}" up -d --wait db
DATABASE_URL='postgresql://chulito_spike:local_only_chulito_spike@127.0.0.1:54329/chulito_spike' \
  npx --yes npm@11.19.1 run test:postgres
