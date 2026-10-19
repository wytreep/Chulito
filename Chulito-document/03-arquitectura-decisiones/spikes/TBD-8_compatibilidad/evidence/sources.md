# Fuentes oficiales y evidencia del registro

**Consulta:** 17 de octubre de 2026 (hora de Cali, UTC−05:00; capturas npm en JSON asociadas a la ejecución local).
**Registro usado:** `https://registry.npmjs.org/`.

## Evidencia oficial

1. Node.js publica su calendario y estado de ramas en [Node.js Releases](https://nodejs.org/en/about/previous-releases). En la consulta, Node 24 (Krypton) y Node 22 (Jod) aparecen como LTS; Node 26 figura como Current. Node.js recomienda Active/Maintenance LTS para aplicaciones de producción. El spike por eso instala y prueba 24.22.0 como candidata y 22.23.3 como línea secundaria, y no recomienda Node 26 como runtime de producción.
2. La [guía de migración de NestJS 12](https://docs.nestjs.com/migration-guide) documenta los mínimos diferenciados: para ejecutar una aplicación NestJS 12 con CommonJS, Node 20.19+ o 22.12+; para CLI/schematics, Node 22.22.3+, 24.15+ o 26+. La guía también indica que ESM es una opción de proyecto, que la plantilla ESM usa Vitest y que `@nestjs/testing` no depende del runner.
3. La [guía de migración de NestJS 11](https://docs.nestjs.com/v11/migration-guide) establece Node 20+ como requisito de NestJS 11 y recomienda la última LTS. Se conserva como contexto de la rama anterior, no como candidata elegida.
4. La [documentación de testing de NestJS](https://docs.nestjs.com/fundamentals/testing) describe el uso de `@nestjs/testing` y Supertest para pruebas HTTP de extremo a extremo.

## Consultas del registro npm

Los valores vigentes y el JSON de `version`, `engines`, `peerDependencies` y `dependencies` de los paquetes directos del harness se guardan en `registry-metadata.json`; la restricción de `ts-jest` (que no es dependencia directa) queda respaldada por el log archivado de su resolución fallida. La consulta inicial encontró las siguientes restricciones que influyen en la matriz:

- `@nestjs/schematics@12.0.7` requiere Node `^22.22.3 || ^24.15.0 || >=26.0.0` y TypeScript `>=6.0.0`.
- `@nestjs/swagger@12.0.2` requiere NestJS 12 y acepta TypeScript `^5.5.0 || ^6.0.0`; no declara TypeScript 7 como compatible.
- `ts-jest@29.4.15` admite Jest 29/30 y TypeScript `>=4.3 <7`; el log de la resolución fallida con TypeScript 7.0.2 se archivó en [`evidence/ts7-eresolve.log`](ts7-eresolve.log). Nest CLI v12 genera ESM + Vitest por defecto en esta plantilla, por lo que la combinación ejecutada se valida con ese runner.
- Nest CLI `12.0.8` declara TypeScript `~6.0.2` como dependencia; la aplicación se prueba con TypeScript `6.0.3`, que satisface ese rango.
- La instalación inicial con Vitest `4.1.2` reportó la asesoría moderada [GHSA-82fw-gwwq-j7x9](https://github.com/advisories/GHSA-82fw-gwwq-j7x9), con rango vulnerable `>=2.1.0 <4.1.11`. Se fijó `vitest` y `@vitest/coverage-v8` en `4.1.12` antes de ejecutar la verificación final; la revisión corregida debe terminar con cero hallazgos npm audit.

La existencia de una versión en npm no demuestra por sí sola compatibilidad. La evidencia de compatibilidad son `npm ci`, compilación, pruebas y arranque de la aplicación ejecutados con el lockfile y el runtime registrados.
