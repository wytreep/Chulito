# ADR-0001: Baseline compatible de Node.js, TypeScript y NestJS

- **Estado:** Propuesto; requiere aprobación del responsable técnico del producto.
- **Fecha:** 18 de octubre de 2026.
- **Decisores:** pendiente de confirmación.
- **Contexto del producto:** Chulito, referido por el prefijo histórico `CNF-` en algunos identificadores documentales.
- **Trazabilidad:** SRS Chulito v0.4, TBD-8.
- **Evidencia:** [fuentes y restricciones](../spikes/TBD-8_compatibilidad/evidence/sources.md), [snapshot npm](../spikes/TBD-8_compatibilidad/evidence/registry-metadata.json), [registro de verificación](../spikes/TBD-8_compatibilidad/evidence/verification-2026-10-18.md), [verificación revisión 2](../spikes/TBD-8_compatibilidad/evidence/verification-2026-10-18-revision-2.md), [harness](../../../Chulito-coding/ADR-0001_spike-compatibilidad/README.md).

## Contexto

Antes de iniciar la implementación backend se requiere comprobar que las versiones de Node.js, TypeScript, NestJS, módulos ESM, runner de pruebas y dependencias de validación/documentación resuelvan entre sí desde npm, compilen y ejecuten pruebas bajo las líneas LTS elegidas. La matriz es específica al conjunto fijado en el lockfile y al 18-oct-2026; no sustituye pruebas del sistema completo.

El spike usa un harness desechable con un health endpoint y un endpoint echo con payload sintético. No ingiere notificaciones, no se conecta a Nequi/Daviplata, no accede a cuentas ni usa datos de usuarios. S-0.1 es un escenario simulado, no resultados de entrevistas realizadas; no aporta evidencia para esta decisión técnica.

## Decisión propuesta

1. **Runtime de referencia:** Node.js 24 LTS, parche probado `24.22.0`, para desarrollo, CI y despliegues nuevos mientras la línea siga en soporte LTS y la plataforma de destino la soporte.
2. **Compatibilidad secundaria:** mantener CI y desarrollo compatibles con Node.js 22 LTS, parche probado `22.23.3`, mientras la línea siga en soporte y exista necesidad de despliegue en Node 22.
3. **Rango de herramientas:** restringir el repositorio a `^22.22.3 || ^24.15.0` (`package.json`). Ese rango es **más estrecho** que el que declaran las herramientas: `@nestjs/cli@12.0.8` solo exige Node `>= 20.11` y `@nestjs/schematics@12.0.7` declara `^22.22.3 || ^24.15.0 || >=26.0.0`. Se eligió deliberadamente por la matriz efectivamente probada (Node 24.22.0 y 22.23.3) y deja fuera Node 26 (Current, no LTS) hasta que se pruebe. Los parches probados no prueban automáticamente cada parche dentro de esos rangos; CI debe ejecutarse en ambos parches LTS y actualizar la matriz cuando cambie el parche de referencia.
4. **Framework:** NestJS 12.1.3 para `@nestjs/common`, `@nestjs/core`, `@nestjs/platform-express` y `@nestjs/testing`; CLI 12.0.8 y schematics 12.0.7.
5. **Lenguaje y módulos:** TypeScript 6.0.3 y ESM con `module`/`moduleResolution` `NodeNext`. Mantener `strict`, `isolatedModules`, decoradores y `emitDecoratorMetadata` habilitados en la configuración base.
6. **Pruebas:** utilizar Vitest 5.0.5 (con `@vitest/coverage-v8` 5.0.5) sobre Vite 8.3.4 y Supertest 7.3.1 para pruebas unitarias y HTTP/e2e. La plantilla oficial ESM de Nest CLI 12 genera Vitest; no se recomienda añadir Jest/ts-jest en este baseline sin un requerimiento concreto. La versión inicial Vitest 4.1.2 se descartó tras `npm audit` identificar GHSA-82fw-gwwq-j7x9 (rango vulnerable `>=2.1.0 <4.1.11`). La revisión 2 adoptó la línea vigente 5.0.5, también parcheada, tras pasar la matriz en Node 24.22.0 y 22.23.3; la auditoría del lockfile fue cero.
7. **Dependencias de integración usadas en el harness:** `@nestjs/config` 12.0.1, `@nestjs/swagger` 12.0.2, `class-validator` 0.15.1, `class-transformer` 0.5.1 y `pg` 8.23.1.
8. **Reproducibilidad:** fijar versiones directas exactas, conservar `package-lock.json`, usar `npm ci`, exigir engines (`engine-strict=true`, con `node` y `npm` en `package.json`) y adoptar npm 11.19.1 como versión de referencia del spike. Todos los scripts del repositorio invocan `npm@11.19.1` explícitamente en lugar de depender del npm que traiga el runtime de Node.
9. **Persistencia:** no decidir PostgreSQL como arquitectura de datos ni seleccionar ORM a partir de este ADR. `pg` compila y sus tipos se chequean, pero no hubo Docker ni `psql` disponibles, así que no se ejecutó una conexión real. La prueba opcional PostgreSQL 16 queda como procedimiento reproducible para ejecutar en un entorno con Docker.
10. **Puertas de calidad y scripts:** denegar el postinstall de telemetría de `@scarf/scarf` (`npm install-scripts deny @scarf/scarf`, que llega por `swagger-ui-dist`) y ejecutar `oxlint` y `prettier --check` como scripts del harness (`lint`, `format:check`) dentro de `verify`.
11. **Tipos de Node:** fijar `@types/node` 22.20.5, la línea mínima soportada, para que el typecheck no acepte API que no exista en Node 22.

## Evidencia y resultado

El registro consultado fue `https://registry.npmjs.org/`; la documentación de Node y Nest se vincula en [`../spikes/TBD-8_compatibilidad/evidence/sources.md`](../spikes/TBD-8_compatibilidad/evidence/sources.md). La metadata exacta de los paquetes directos del harness (25 registros) se capturó en [`../spikes/TBD-8_compatibilidad/evidence/registry-metadata.json`](../spikes/TBD-8_compatibilidad/evidence/registry-metadata.json).

La verificación limpia se ejecutó con `npm ci` en Node `24.22.0` y `22.23.3`, ambos usando npm `11.19.1`. En cada runtime pasó la compilación de Nest, `tsc --noEmit`, `oxlint`, `prettier --check`, dos pruebas unitarias, tres pruebas e2e (health, validación y documento OpenAPI), el arranque del `dist/main.js` y el smoke HTTP contra loopback. `npm audit` informó cero vulnerabilidades en ambas ejecuciones. Los detalles de comandos y contadores están en [`../spikes/TBD-8_compatibilidad/evidence/verification-2026-10-18-revision-2.md`](../spikes/TBD-8_compatibilidad/evidence/verification-2026-10-18-revision-2.md) (que reemplaza a [`../spikes/TBD-8_compatibilidad/evidence/verification-2026-10-18.md`](../spikes/TBD-8_compatibilidad/evidence/verification-2026-10-18.md)).

Se rechazó una prueba de resolución con TypeScript `7.0.2`: npm devolvió `ERESOLVE` por el peer range de `ts-jest@29.4.15` (`typescript >=4.3 <7`); además, el `@nestjs/swagger@12.0.2` fijado declara soporte hasta TypeScript 6. Esto respalda no adelantar el major sin una actualización explícita de peers y nueva matriz. La rama de prueba TypeScript 7 no forma parte del `package-lock.json` del harness; el log quedó archivado en [`../spikes/TBD-8_compatibilidad/evidence/ts7-eresolve.log`](../spikes/TBD-8_compatibilidad/evidence/ts7-eresolve.log).

La **revisión 2** (18-oct-2026) ajustó `@types/node` a 22.20.5, adoptó Vitest 5.0.5, añadió las puertas `oxlint` y `prettier --check`, fijó `engines.npm` y denegó el postinstall de `@scarf/scarf`. Volvió a correr la matriz completa en Node `24.22.0` y `22.23.3` con cero fallos y cero vulnerabilidades; los detalles están en [`../spikes/TBD-8_compatibilidad/evidence/verification-2026-10-18-revision-2.md`](../spikes/TBD-8_compatibilidad/evidence/verification-2026-10-18-revision-2.md), que reemplaza a la revisión 1.

## Alternativas consideradas

| Alternativa | Evaluación | Resultado |
|---|---|---|
| Node 24 LTS primario y Node 22 LTS secundario | Ambas líneas son LTS según el registro oficial consultado y pasan el mismo harness con su parche probado. | Recomendada en esta propuesta. |
| Node 26 Current | No era LTS en la fecha de consulta; no se probó. | No usar como baseline de producción todavía; revaluar al cambiar su estado y tras añadirlo a CI. |
| NestJS 11 | Documentación disponible y Node 20+, pero no se ejecutó matriz; elegirlo no aporta evidencia de compatibilidad al proyecto actual. | No seleccionado; reabrir si NestJS 12 queda incompatible con despliegue o dependencias. |
| CommonJS + Jest/ts-jest | Ecosistema conocido, pero difiere del scaffold oficial ESM de Nest CLI 12 y no fue el camino probado. | No seleccionado; no declarar compatible a partir de este spike. |
| TypeScript 7 | El ensayo de resolución falló por peer dependency de ts-jest y la versión de Swagger fijada no lo declara compatible. | Rechazado para este baseline; reabrir tras alineación de peers y pruebas. |
| PostgreSQL/ORM específico | No hubo servicio PostgreSQL disponible y el proyecto no seleccionó ORM. | Fuera de la decisión de este ADR. |

## Consecuencias

- Desarrollo y CI deberán usar Node 24 como línea principal y probar además Node 22 mientras se requiera compatibilidad. En Windows, `verify.sh`, la matriz y el smoke de PostgreSQL son bash: se ejecutan desde Git Bash o WSL, o se corren los pasos equivalentes con `npx --yes npm@11.19.1` a mano.
- El typecheck compila contra `@types/node` 22 (línea mínima soportada); si se adopta Node 24 de forma exclusiva habrá que reevaluar ese pin.
- La única dependencia con script de instalación es `@scarf/scarf` (telemetría, transitiva de `swagger-ui-dist`), y su postinstall queda denegado por política.
- Un cambio de versión mayor de Node, Nest, TypeScript, Vite o Vitest requiere actualizar lockfile y volver a ejecutar el workflow completo, no solo actualizar rangos.
- La plantilla comprobada aporta ESM, validación de DTO y OpenAPI, pero todavía no define módulos de dominio, autenticación, autorización, colas, almacenamiento, persistencia ni captura de notificaciones.
- El soporte de PostgreSQL queda desconocido a nivel de conexión real hasta ejecutar el smoke en un host con Docker/PostgreSQL.
- La decisión no cierra TBD-1 (canal de captura), TBD-2 (emisores), TBD-6 (asesoría legal), TBD-7 (validación real del segmento) ni TBD-9 (port de la vertical slice Python a TypeScript).

## Riesgos y acciones siguientes

1. Ejecutar `./scripts/run-postgres-smoke.sh` cuando haya Docker Compose disponible; anotar versión real de PostgreSQL y resultado.
2. Obtener aprobación técnica de este ADR antes de convertirlo en baseline oficial del producto.
3. Integrar la matriz Node 22/24 y `npm audit` en CI; fijar una política de actualización de dependencias y revisión periódica de advisories.
4. Completar TBD-9 como trabajo separado y usar la vertical slice Python como especificación ejecutable, no como backend de producción.
5. Mantener visible TBD-7: las decisiones de segmento, alcance y prioridad requieren evidencia de personas/comercios reales; la validación técnica no las resuelve.

## Reproducción

Desde `Chulito-coding/ADR-0001_spike-compatibilidad/`, con nvm y acceso a npm:

```bash
./scripts/run-node-matrix.sh
```

La matriz reinstala dependencias mediante `npm ci`, compila, tipa, ejecuta `oxlint` y `prettier --check`, corre tests unitarios/e2e, inicia el artefacto compilado en loopback y ejecuta auditoría para cada parche fijado. Para la parte PostgreSQL no ejecutada, consultar la sección correspondiente del README del harness.

## Historial

| Fecha | Cambio |
|---|---|
| 2026-10-18 | ADR inicial, propuesto, basado en spike ejecutado en Node 22/24. |
| 2026-10-18 | Revisión 2: `@types/node` 22.20.5, Vitest 5.0.5, `oxlint`/`prettier`, `engines.npm`, postinstall de `@scarf/scarf` denegado y matriz repetida con cero fallos. La revisión 1 de la evidencia queda reemplazada. Estado sigue **Propuesto**. |