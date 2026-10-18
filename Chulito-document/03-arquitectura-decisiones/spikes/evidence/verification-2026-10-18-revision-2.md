# Registro de verificación — TBD-8 / ADR-0001 — **revisión 2**

**Fecha de ejecución:** 18 de octubre de 2026 (zona Cali, UTC−05:00).
**Matriz reproducida:** `Chulito-coding/ADR-0001_spike-compatibilidad/scripts/run-node-matrix.sh`; lockfile `Chulito-coding/ADR-0001_spike-compatibilidad/package-lock.json`; npm 11.19.1.
**Estado:** reemplaza a [`verification-2026-10-18.md`](verification-2026-10-18.md) (revisión 1), que se conserva como registro histórico.

## Qué cambió frente a la revisión 1

- `@types/node` 24.19.2 → **22.20.5** (se compila contra la línea mínima soportada, Node 22).
- Vitest 4.1.12 → **5.0.5** y `@vitest/coverage-v8` 4.1.12 → **5.0.5**: se adoptó la línea vigente, también parcheada frente a GHSA-82fw-gwwq-j7x9.
- Se agregaron `oxlint` 1.88.0 y `prettier` 3.9.10 y las puertas `lint` y `format:check`, ahora incluidas en `verify`.
- `engines` fija también `npm ^11.19.1`; `scripts/run-postgres-smoke.sh` invoca `npm@11.19.1` como los demás scripts.
- Postinstall de `@scarf/scarf` **denegado** (`"allowScripts": { "@scarf/scarf": false }` en `package.json`).
- `strictPropertyInitialization` se retiró de `tsconfig.json` (queda `strict` completo, como declara el ADR).
- `evidence/registry-metadata.json` se regeneró: 25 registros con los pins de la revisión 2.
- El log del `ERESOLVE` de TypeScript 7 quedó archivado en [`ts7-eresolve.log`](ts7-eresolve.log).

## Resultado por runtime

| Runtime | `npm ci` | Build Nest | Typecheck | `oxlint` | `prettier --check` | Unitarias | E2E | Runtime smoke | `npm audit` |
|---|---|---|---|---|---|---|---|---|---|
| Node 24.22.0 | OK | OK | OK | OK | OK | 2/2 | 3/3 | OK; health y OpenAPI en loopback | 0 vulnerabilidades |
| Node 22.23.3 | OK | OK | OK | OK | OK | 2/2 | 3/3 | OK; health y OpenAPI en loopback | 0 vulnerabilidades |

El runtime smoke ejecuta el `dist/main.js` compilado bajo la versión activa de Node y comprueba que `GET /api/health` devuelve `{"service":"chulito-api","status":"ok","synthetic":true}` y que `/api/docs-json` se sirve con dos rutas OpenAPI.

## Compatibilidad negativa

Una resolución independiente y desechable con TypeScript 7.0.2 y `ts-jest@29.4.15` terminó con `ERESOLVE`, citando el peer `typescript >=4.3 <7` de ts-jest (log en [`ts7-eresolve.log`](ts7-eresolve.log)). No se alteró el lockfile del spike. El `@nestjs/swagger@12.0.2` fijado declara `^5.5.0 || ^6.0.0`, no TypeScript 7.

## Seguridad y limitaciones

- La única dependencia con script de instalación es `@scarf/scarf` (telemetría, transitiva de `swagger-ui-dist`); su postinstall quedó denegado por política y `npm install-scripts ls` no reporta scripts sin revisar.
- Docker no está disponible (el daemon no respondió) y no se usó `psql`; **la conexión PostgreSQL real sigue sin ejecutarse**. El procedimiento Compose reproducible queda en `scripts/run-postgres-smoke.sh`.
- La matriz valida el conjunto fijado, las versiones exactas probadas y el estado del registro en esta fecha; no valida cada patch permitido por `engines`, la nube de despliegue ni el resto del backend.
- En Windows los scripts `.sh` y la matriz son bash: se ejecutan desde Git Bash o WSL, o se corren los pasos equivalentes con `npx --yes npm@11.19.1` a mano (como en este registro).
- El harness contiene datos sintéticos; S-0.1 es un escenario simulado, no resultados de entrevistas.

## Comandos de reproducción

Desde `Chulito-coding/ADR-0001_spike-compatibilidad/` con nvm:

```bash
./scripts/run-node-matrix.sh
```

Instalación limpia con npm 11.19.1, build, typecheck, `oxlint`, `prettier --check`, unitarias, e2e, runtime smoke y `npm audit` bajo ambos parches.
