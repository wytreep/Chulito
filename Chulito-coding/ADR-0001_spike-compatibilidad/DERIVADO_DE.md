# Este código sale de estos documentos

| Documento origen | Ruta |
|---|---|
| ADR-0001 (baseline Node, TypeScript, NestJS) | `Chulito-document/03-arquitectura-decisiones/adr/` |
| Plan y evidencia del spike TBD-8 | `Chulito-document/03-arquitectura-decisiones/spikes/TBD-8_compatibilidad/` |

## Qué cubre

La matriz de versiones del ADR-0001: instalación limpia, build, typecheck, pruebas unitarias y e2e, smoke de runtime y `npm audit`.

## Qué NO hace

- No es el backend de producción: es un harness desechable.
- La prueba con PostgreSQL real no se ha ejecutado.

## Cómo verificarlo

Con Node 24.22.0 o 22.23.3: `npx --yes npm@11.19.1 ci` y `npx --yes npm@11.19.1 run verify`. En Windows, ejecutar desde Git Bash o WSL (los scripts son de bash).
