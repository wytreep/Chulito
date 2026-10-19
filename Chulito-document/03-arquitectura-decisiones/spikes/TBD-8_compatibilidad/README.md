# Chulito — TBD-8 / ADR-0001

Este directorio contiene el spike aislado de compatibilidad de Node.js, TypeScript y NestJS solicitado para reducir riesgo antes del desarrollo del backend. No modifica el repositorio `univirtual` ni la vertical slice de referencia Python.

## Entregables

- [ADR-0001](../adr/ADR-0001_baseline-node-typescript-nestjs.md): decisión propuesta, trazabilidad, alternativas, consecuencias y límites.
- [Harness NestJS](../../../Chulito-coding/ADR-0001_spike-compatibilidad/README.md): fuentes, versiones, comandos y prueba PostgreSQL opcional.
- [Registro de verificación (revisión 2)](evidence/verification-2026-10-18-revision-2.md): salida resumida de la matriz Node 22/24 con `lint`/`format:check`, ERESOLVE de TypeScript 7 y límites observados. Reemplaza a la [revisión 1](evidence/verification-2026-10-18.md).
- [Fuentes](evidence/sources.md) y [snapshot de metadata npm](evidence/registry-metadata.json).
- [Plan del spike](plan/2026-10-17-adr-0001-compatibility-spike.md).

## Reproducir

Con nvm, npm 11.19.1 vía `npx` y acceso al registro npm:

```bash
cd Chulito-coding/ADR-0001_spike-compatibilidad
./scripts/run-node-matrix.sh
```

El proceso prueba instalación, compilación, tipos, unitarias, e2e, ejecución del artefacto compilado y `npm audit` en Node 24.22.0 y Node 22.23.3. La prueba de PostgreSQL no se ejecutó en el entorno donde se hizo el spike porque no había Docker/psql; el script local Compose queda disponible si se desea validarla.

## Estado

El resultado técnico sustenta una propuesta de baseline, pero ADR-0001 mantiene estado **Propuesto** hasta que el responsable técnico la apruebe. No selecciona ORM ni base de datos. Tampoco cierra TBD-1, TBD-2, TBD-6, TBD-7 ni TBD-9. En particular, S-0.1 es un escenario simulado y no evidencia de campo.
