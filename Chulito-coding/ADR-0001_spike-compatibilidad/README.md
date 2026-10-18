# Chulito TBD-8 compatibility spike

This is a disposable compatibility harness generated with the official NestJS CLI 12.0.8 and then reduced to a synthetic health/validation API. It is not the Chulito product backend, does not ingest payment notices, and does not use S-0.1 as field evidence.

## Candidate toolchain

- Node.js 24.22.0 (LTS candidate); Node.js 22.23.3 is the secondary LTS line tested.
- npm 11.19.1 is pinned as the reproducibility tool for install, scripts and audits.
- NestJS core/common/platform/testing 12.1.3; CLI 12.0.8; schematics 12.0.7.
- TypeScript 6.0.3; ESM (`nodenext`) and Vitest 5.0.5 (`@vitest/coverage-v8` 5.0.5) from the Nest CLI 12 template.
- `@types/node` 22.20.5: the project type-checks against the minimum supported LTS line (Node 22), not against the running patch.
- `@nestjs/config` 12.0.1, `@nestjs/swagger` 12.0.2, `class-validator` 0.15.1 and `class-transformer` 0.5.1.
- `oxlint` 1.88.0 and `prettier` 3.9.10 back the `lint` and `format:check` scripts.
- PostgreSQL driver `pg` 8.23.1 is compile-checked. The SRS has not selected an ORM or approved a database integration.

All direct versions are exact pins and `package-lock.json` is the reproducibility authority. The accepted Node range in this harness is `^22.22.3 || ^24.15.0`: it is **narrower** than what the tools declare (`@nestjs/cli@12.0.8` asks for Node `>= 20.11`; `@nestjs/schematics@12.0.7` asks for `^22.22.3 || ^24.15.0 || >=26.0.0`) and was chosen by the tested matrix, leaving Node 26 (Current, not LTS) out until it is proven. `engines` also pins `npm ^11.19.1`. The matrix runner executes npm 11.19.1 even if the installed Node distribution bundles another npm patch.

## Install, build and test

Run the complete clean matrix from this directory:

```bash
./scripts/run-node-matrix.sh
```

It selects Node 24.22.0 and 22.23.3 through nvm, uses npm 11.19.1 for `ci`, build, typecheck, unit tests, e2e tests, process startup smoke and `audit`, and fails on the first unsuccessful command. For one runtime only, use `nvm use 24.22.0` (or `22.23.3`), then `npx --yes npm@11.19.1 ci` and `npx --yes npm@11.19.1 run verify`.

`verify` exercises the Nest production build, TypeScript typecheck, `oxlint`, `prettier --check`, two unit tests, three HTTP e2e tests (health JSON, request validation and generated `/api/docs-json`), and starts `dist/main.js` to exercise the ESM runtime over loopback. No service needs to listen on a public interface.

### Windows

The `scripts/*.sh` files and the nvm matrix are bash-based; on Windows run them from Git Bash or WSL, or run the equivalent `npx --yes npm@11.19.1` steps (`ci`, `run build`, `run typecheck`, `run lint`, `run format:check`, `test`, `run test:e2e`, `run test:runtime`, `audit`) manually as this record did. `run-node-matrix.sh` sources `$NVM_DIR/nvm.sh`, so it targets nvm.sh environments.

### Install-script policy

`@scarf/scarf@1.4.0` arrives transitively through `@nestjs/swagger` → `swagger-ui-dist` and declares a `postinstall` (`node ./report.js`). Its install script is explicitly denied via the `"allowScripts": { "@scarf/scarf": false }` entry in `package.json`; npm 11.19.1 would otherwise report it as "not covered by allowScripts".

## Optional PostgreSQL test

Docker and `psql` were unavailable in the recorded environment, so this step was not executed. If Docker Compose is installed, run:

```bash
./scripts/run-postgres-smoke.sh
```

The script creates a disposable local PostgreSQL 16 container on loopback port 54329, runs a parameterized query through `pg`, then removes the container and volume. The credentials in `postgres/compose.yaml` are local test-only placeholders and must never be reused outside this isolated spike. Without Docker, set `DATABASE_URL` to a disposable PostgreSQL database and run `npx --yes npm@11.19.1 run test:postgres`.

This checks the `pg` client/Node connection path only. It does not select TypeORM, Prisma, Drizzle, migrations, connection pooling policy for production, or a Chulito database schema.

## Evidence

See `../../Chulito-document/03-arquitectura-decisiones/adr/ADR-0001.md`, `../../Chulito-document/03-arquitectura-decisiones/spikes/evidence/sources.md`, `../../Chulito-document/03-arquitectura-decisiones/spikes/evidence/registry-metadata.json`, `../../Chulito-document/03-arquitectura-decisiones/spikes/evidence/verification-2026-10-18.md` and `../../Chulito-document/03-arquitectura-decisiones/spikes/evidence/verification-2026-10-18-revision-2.md` for the decision record and dated snapshots/results.
