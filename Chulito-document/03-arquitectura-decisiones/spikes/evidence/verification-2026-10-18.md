# Registro de verificación — TBD-8 / ADR-0001

> **Revisión 1 (reemplazada).** Este registro queda superado por [`verification-2026-10-18-revision-2.md`](verification-2026-10-18-revision-2.md); se conserva como evidencia histórica.

**Fecha de ejecución:** 18 de octubre de 2026, zona Cali (UTC−05:00).
**Matriz reproducida:** `Chulito-coding/ADR-0001_spike-compatibilidad/scripts/run-node-matrix.sh`; lockfile `Chulito-coding/ADR-0001_spike-compatibilidad/package-lock.json`; npm 11.19.1.

## Resultado por runtime

| Runtime | Instalación limpia | Build Nest | Typecheck | Unitarias | E2E | Runtime smoke | npm audit |
|---|---|---|---|---:|---:|---|---|
| Node 24.22.0 | `npm ci` OK | OK | OK | 2/2 | 3/3 | OK; health y OpenAPI en loopback | 0 vulnerabilidades |
| Node 22.23.3 | `npm ci` OK | OK | OK | 2/2 | 3/3 | OK; health y OpenAPI en loopback | 0 vulnerabilidades |

El comando global terminó con código 0 en ambas filas. El runtime smoke ejecutó el `dist/main.js` construido bajo la versión activa de Node y comprobó que `GET /api/health` devuelve `{"service":"chulito-api","status":"ok","synthetic":true}` y que `/api/docs-json` se sirve con dos rutas OpenAPI.

Los tres casos e2e verifican: (1) health endpoint, (2) payload válido e inválido por ValidationPipe, y (3) especificación OpenAPI. Las unitarias verifican el servicio/controller sintéticos. El archivo `src/database/pg-pool.ts` se incluyó en build y typecheck, pero no se conectó a PostgreSQL.

## Compatibilidad negativa

Una resolución independiente y desechable con TypeScript 7.0.2, NestJS 12.1.3, Swagger 12.0.2 y ts-jest 29.4.15 terminó con `ERESOLVE`, citando el peer `typescript >=4.3 <7` de ts-jest. No se alteró el lockfile del spike con este ensayo. La metadata consultada también muestra que el Swagger fijado admite `^5.5.0 || ^6.0.0`, no TypeScript 7.

## Seguridad y limitaciones

- La primera revisión usó Vitest 4.1.2 y npm audit señaló la asesoría moderada GHSA-82fw-gwwq-j7x9. Se actualizó el runner y `@vitest/coverage-v8` a 4.1.12 antes de la matriz final; los audits posteriores a cada `npm ci` y los dos audits explícitos reportaron 0 vulnerabilidades.
- npm mostró un aviso no bloqueante de que `@scarf/scarf@1.4.0` tiene un script postinstall no cubierto por la política de aprobación de scripts. La instalación, build y pruebas continuaron correctamente; el aviso no se suprimió.
- Docker y `psql` no están disponibles en el entorno de ejecución. Por tanto, no se afirma que la conexión PostgreSQL ni el Compose funcionen aquí. Se dejó una prueba aislada reproducible en `Chulito-coding/ADR-0001_spike-compatibilidad/scripts/run-postgres-smoke.sh`.
- La matriz valida el conjunto fijado, las versiones exactas probadas y el estado del registro en esta fecha. No valida cada patch permitido por `engines`, disponibilidad en la nube de despliegue ni el resto del backend del producto.
- El harness contiene datos sintéticos; S-0.1 es un escenario simulado, no resultados de entrevistas realizadas.

## Comandos de reproducción

Desde `Chulito-coding/ADR-0001_spike-compatibilidad/` con nvm:

```bash
./scripts/run-node-matrix.sh
```

El script hace instalación limpia con npm 11.19.1, ejecuta build, typecheck, unitarias, e2e, runtime smoke y npm audit bajo ambos parches.
