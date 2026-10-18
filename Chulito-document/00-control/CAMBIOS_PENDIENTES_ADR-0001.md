# Correcciones del spike TBD-8 y ADR-0001

Base original: el paquete `Chulito_TBD8_ADR0001_2026-10-18.zip` **sin modificar**.
Cada punto fue comprobado contra ese paquete, el lockfile o el registro de npm el 2026-10-18.
Las rutas originales eran relativas a `chulito-api/`; el harness vive ahora en `Chulito-coding/ADR-0001_spike-compatibilidad/`.

**Estado: aplicado en la revisión 2 (2026-10-18).**

- A1–A6 aplicadas (tsconfig `strict`, `engines.npm`, npm fijado en el script de PostgreSQL, rutas relativas del plan, redacción de la decisión 3 del ADR, log del `ERESOLVE` archivado).
- B1: `@types/node` 22.20.5 (opción recomendada).
- B2: Vitest 5.0.5 adoptado tras pasar la matriz.
- B3: postinstall de `@scarf/scarf` denegado (`"allowScripts": { "@scarf/scarf": false }`).
- B4: se activaron `oxlint` y `prettier` con los scripts `lint` y `format:check` en `verify`.
- B5: `pg-pool.ts` marcado como NO INTEGRADO.
- B6: nota de Windows (Git Bash/WSL) en el README del harness y en el ADR.
- B7: casilla de dist-tags prerelease marcada con evidencia; la conexión PostgreSQL **sigue pendiente** (sin Docker/`psql`).
- Resultado: `evidence/verification-2026-10-18-revision-2.md` (Node 24.22.0 y 22.23.3, cero fallos, cero vulnerabilidades). El estado del ADR sigue **Propuesto**.

## A. Obligatorias (el documento y el código se contradicen)

| # | Archivo | Cambio | Por qué |
|---|---|---|---|
| A1 | `tsconfig.json` línea 20 | Borrar `"strictPropertyInitialization": false,` | El ADR (decisión 5) dice mantener `strict`; esta línea lo relaja |
| A2 | `package.json` → `engines` | Agregar `"npm": "^11.19.1"` junto a `node` | `packageManager` no impide usar npm 10 (el que trae Node 22.23.3); `engines.npm` sí lo detecta |
| A3 | `scripts/run-postgres-smoke.sh` línea 13 | `npm run test:postgres` → `npx --yes npm@11.19.1 run test:postgres` | Los otros scripts ya fijan npm; este no |
| A4 | `../docs/plans/2026-10-17-adr-0001-compatibility-spike.md` línea 11 | Cambiar `/home/ubuntu/Chulito_Entrega_v0.4_2026-10-17/...` por rutas relativas al repositorio | Es una ruta de otro entorno |
| A5 | `../ADR-0001.md` decisión 3 | Sustituir "alineado con los engines de Nest CLI 12/schematics" por: `@nestjs/cli@12.0.8` declara `>= 20.11`; `@nestjs/schematics@12.0.7` declara `^22.22.3 \|\| ^24.15.0 \|\| >=26.0.0`; el rango del repositorio es más estrecho (excluye 26) y se elige por la matriz probada | El texto actual no coincide con el snapshot del propio spike |
| A6 | `../evidence/sources.md` línea 19 | Archivar el log del `ERESOLVE` de TypeScript 7 (p. ej. `evidence/ts7-eresolve.log`) o añadir `ts-jest` a `registry-metadata.json` | La afirmación sobre `ts-jest@29.4.15` cita un snapshot que no lo contiene (0 coincidencias) |

## B. Decisiones tuyas (cada una cambia el ADR)

| # | Tema | Hallazgo verificado | Opciones |
|---|---|---|---|
| B1 | `@types/node` | El paquete fija `24.19.2` (dist-tag `old-version`; `latest` es 26.6.5) pero el baseline también soporta Node 22 | **Recomendada:** `22.20.5` (compilar contra la línea mínima). Alternativa: mantener 24.19.2 y declarar que la fila Node 22 compila contra tipos 24 |
| B2 | Vitest | Fijado en 4.1.12; `latest` es 5.0.5. Vitest 5.0.5 declara `node ^22.12.0 \|\| ^24.0.0 \|\| >=26.0.0` y `vite ^6.4.0 \|\| ^7.0.0 \|\| ^8.0.0`, compatibles con este baseline | Probar 5.0.5 con la matriz y adoptarlo, o dejar 4.1.12 y añadir Vitest 5 a "Alternativas consideradas" con el motivo real |
| B3 | `@scarf/scarf` | Llega por `swagger-ui-dist`; versión 1.4.0 con `postinstall: node ./report.js`. npm 11.19.1 lo reporta como "no cubierto por allowScripts" | Ejecutar `npm install-scripts deny @scarf/scarf`, comprobar dónde registra la política y documentarla en el ADR (Consecuencias/Seguridad) |
| B4 | Lint y formato | Existen `.oxlintrc.json` y `.prettierrc`, pero no hay `oxlint` ni `prettier` en dependencias ni scripts | O se agregan dependencias y scripts `lint` y `format:check` al `verify`, o se borran ambos archivos. No dejar a medias |
| B5 | `src/database/pg-pool.ts` | Código sin uso por diseño | Añadir cabecera "NO INTEGRADO" o quitarlo |
| B6 | Windows | `verify.sh` y la matriz usan bash y nvm de Unix | Documentar "usar Git Bash o WSL", o reescribir los scripts en Node (`.mjs`) |
| B7 | Plan del spike, líneas 40 y 57 | Dos casillas abiertas: rechazo de dist-tags prerelease y conexión real a PostgreSQL | Marcar solo lo que tenga evidencia; la prueba PostgreSQL sigue pendiente (no hay Docker aquí) |

## C. Qué NO hay que corregir

- **Permisos de los `.sh`:** el zip original ya los trae ejecutables (`-rwxr-xr-x`). Si en tu equipo pierden el permiso al commitear desde Windows: `git update-index --chmod=+x <ruta>/scripts/*.sh`.
- `@types/supertest 7.2.1` frente a `supertest 7.3.1`: desajuste de patch inofensivo.
- Dependencias opcionales no resueltas (`UNMET OPTIONAL`): normales.

## D. Verificación después de aplicar

1. Si cambiaste dependencias (B1, B2, B4): `npx --yes npm@11.19.1 install` y revisar el diff de `package-lock.json`.
2. Con Node **24.22.0** y luego **22.23.3**: `npx --yes npm@11.19.1 ci`, `... run verify` y `... audit`. Esperado: 0 fallos y 0 vulnerabilidades.
3. Guardar el resultado en `spikes/` como evidencia de la revisión 2 e indicar que la revisión 1 queda reemplazada.
4. Añadir fila de revisión en el historial del ADR. El estado sigue **Propuesto** hasta que lo apruebes.
