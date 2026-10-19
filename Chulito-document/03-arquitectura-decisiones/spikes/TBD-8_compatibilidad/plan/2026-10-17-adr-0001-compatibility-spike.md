# Chulito TBD-8 Compatibility Spike Plan

> **For agentic workers:** Execute this plan in the isolated `chulito-tbd8-spike` repository; the user already selected direct implementation in the sandbox.

**Goal:** Validate a reproducible Node.js/TypeScript/NestJS dependency set for Chulito and produce ADR-0001 with verified commands, results, and explicit limits.

**Architecture:** Query the public npm registry and official Node/NestJS documentation, freeze exact package versions in a lockfile, scaffold a minimal Nest HTTP application, and run install/build/unit/e2e checks on supported Node LTS lines. Keep database selection separate; test the PostgreSQL client only if a local PostgreSQL service is available, otherwise include a runnable container script.

**Tech Stack:** Node.js 22 LTS and 24 LTS (exact patch releases resolved at execution), NestJS 12, TypeScript 6, Jest 30/ts-jest 29 or the Nest CLI v12 default test runner, npm lockfile, optional `pg`/PostgreSQL 16.

**Spec:** `Chulito-document/02-requisitos/srs/SRS_Chulito_v0.4_29148_alineacion_estructural.pdf`, TBD-8; entrega de referencia en `Chulito-document/05-operacion/entregas/entrega-v0.4_2026-10-17/README.md`.

## Global Constraints

- Do not modify the unrelated `univirtual` repository or replace the Python reference slice.
- Test only synthetic health/API data; no provider credentials, real payment records, or integrations.
- Use versions actually published in the npm registry and exact pins in the spike lockfile.
- Treat Node 24 LTS as the production candidate only if official release status and installed CLI floor both agree; Node 22 is a secondary compatibility line.
- Do not select an ORM or claim database compatibility unless a PostgreSQL-backed test is executed.
- Preserve S-0.1's status: simulated scenario, not field evidence.

## Review Focus

- Node patch releases below Nest CLI/schematics engine floors: verify both runtime and CLI scaffold floors.
- TypeScript major outside the Nest ecosystem peer ranges: inspect peer requirements and compile the actual app.
- Nest packages from mismatched majors: install all framework packages on one major and inspect the resolved dependency tree.
- ESM/CommonJS loader behavior: exercise the generated application, not only `tsc`.
- Jest/ts-jest interoperability: run unit and HTTP-level tests under the actual selected TypeScript version.
- PostgreSQL unavailable in the sandbox: provide a deterministic Compose + smoke-test command and state it was not executed.

---

## Task 1: Capture sources and the candidate matrix

**Files:** `evidence/registry-metadata.json`, `evidence/sources.md`, `ADR-0001_baseline-node-typescript-nestjs.md`.

- [x] Record retrieval timestamp and registry URL.
- [x] Capture exact versions, `engines`, and peer dependencies for the selected Nest/TypeScript/test/Swagger/config/pg packages in `evidence/registry-metadata.json`.
- [x] Record official Node release-status and Nest migration requirements with URLs.
- [x] Reject prerelease dist-tags unless an explicit compatibility experiment requires one. (Se fijaron solo versiones estables; ninguna dependencia quedó en un dist-tag `beta`, `rc` o `next`.)

## Task 2: Freeze the executable Nest candidate

**Files:** `package.json`, `package-lock.json`, `tsconfig.json`, `nest-cli.json`, `src/`, `test/`.

- [x] Resolve exact patch versions for Node 22/24 and install through nvm.
- [x] Generate and verify a minimal NestJS 12 ESM HTTP application with Vitest.
- [x] Include config, Swagger, validation and pg client dependencies; pg client is typechecked but not live-connected.
- [x] Run clean `npm ci`, build, typecheck, unit, HTTP e2e and compiled-process smoke on each Node line.
- [x] Run `npm ls`, inspect peers/engines, and run `npm audit`; did not use `--legacy-peer-deps`.

## Task 3: Check PostgreSQL availability and portability

**Files:** `postgres/compose.yaml`, `scripts/postgres-smoke.mjs`, `scripts/run-postgres-smoke.sh`.

- [x] Check Docker and local PostgreSQL availability; both Docker and `psql` were unavailable.
- [ ] Connect with `pg`, execute a parameterized query, and record PostgreSQL version; still pending (el entorno no tenía Docker ni `psql`; el script Compose queda listo pero sin ejecutar).
- [x] Leave an isolated Compose script for PostgreSQL 16 plus an environment-driven smoke test; do not claim integration passed.

## Task 4: Decide and record ADR-0001

**Files:** `ADR-0001.md`, `README.md`.

- [x] Recommend exact Node support policy, Nest/TypeScript/test-runner baseline and lockfile policy from results.
- [x] List evidence, failed experiment, unresolved choices (especially ORM/database), and reproduction commands.
- [x] Mark ADR as Proposed; distinguish executed tests from recommendations.

## Task 5: Verify and package

- [x] Re-run from clean install and all selected Node lines.
- [x] Verify health response, committed lockfile and ignored `node_modules`/build outputs.
- [x] Report exact passing checks, unavailable database check, and links in the root README.
