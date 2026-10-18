#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
NVM_SH="${NVM_DIR:-$HOME/.nvm}/nvm.sh"
if [[ ! -f "$NVM_SH" ]]; then
  echo "nvm not found at $NVM_SH; install the exact Node versions listed in .nvmrc and README first." >&2
  exit 2
fi
# shellcheck disable=SC1090
source "$NVM_SH"
cd "$ROOT"

for version in 24.22.0 22.23.3; do
  echo "=== Node $version / npm 11.19.1 ==="
  nvm use "$version"
  node --version
  npx --yes npm@11.19.1 --version
  npx --yes npm@11.19.1 ci
  npx --yes npm@11.19.1 run verify
  npx --yes npm@11.19.1 audit
done
