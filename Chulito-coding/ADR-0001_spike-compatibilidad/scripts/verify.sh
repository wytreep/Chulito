#!/usr/bin/env bash
set -euo pipefail
NPM=(npx --yes npm@11.19.1)
"${NPM[@]}" --version
"${NPM[@]}" run build
"${NPM[@]}" run typecheck
"${NPM[@]}" run lint
"${NPM[@]}" run format:check
"${NPM[@]}" test
"${NPM[@]}" run test:e2e
"${NPM[@]}" run test:runtime
