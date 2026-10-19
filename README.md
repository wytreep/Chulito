# Chulito

Confirmación compartida de pagos y libro diario unificado para negocios pequeños en Colombia.
Repositorio de **documentación, decisiones de arquitectura y código de referencia** de un proyecto de portafolio en fase de diseño.

> **Avisos**
> - Los hallazgos S-0.1 son un **escenario simulado**; no son resultados de entrevistas realizadas y no validan el problema ni el alcance.
> - No hay datos reales en este repositorio. Todo dato de prueba es sintético.
> - El nombre *Chulito* está en verificación de dominio y marca. El prefijo `CNF-` de algunos códigos de documento es histórico (nombre anterior).

## Estructura

```
Chulito/                 Repositorio: solo texto (.md) y código
├── Chulito-document/    Estructura e índices de los documentos (fuente de verdad)
└── Chulito-coding/      Código derivado de los documentos (cada carpeta dice de cuál)
```

Cada carpeta de código incluye un `DERIVADO_DE.md` con el documento origen, los requisitos que cubre y lo que **no** está implementado.

## Dónde están los documentos

Los binarios (`*.docx`, `*.pdf` y `*.zip`) **no** se versionan aquí: se guardan fuera del repositorio, en `C:\dev\Chulito_documentos\`, con la **misma ruta relativa** que tendrían dentro (por ejemplo `Chulito_documentos\Chulito-document\02-requisitos\prd\Chulito_PRD_v0.4_2026-10-17.pdf`). El repositorio conserva la carpeta, su README y un `.gitkeep` como marcador de posición. Los archivos de texto (`.md`: índices, ADR, planes, evidencia) sí están aquí.

## Reglas

1. Un requisito vive en el SRS; una decisión técnica vive en un ADR. El código no los redefine.
2. Orden de cambio: primero el documento, luego el código.
3. Sin datos reales, sin secretos, sin `node_modules/` ni `dist/`.
4. Los documentos de escenario simulado no se citan como evidencia.

## Estado de la Fase 0

Pendientes abiertos (detalle en el SRS v0.4): TBD-1 captura, TBD-2 emisores, TBD-6 asesoría legal, TBD-7 validación real, TBD-8 ADR-0001 (en revisión), TBD-9 port a TypeScript.

## Cómo verificar

- Documentos: con `C:\dev\Chulito_documentos\` en su sitio, comparar `Chulito-document/05-operacion/entregas/*/MANIFEST_SHA256.txt` con los archivos (`Get-FileHash -Algorithm SHA256`).
- Spike: `cd Chulito-coding/ADR-0001_spike-compatibilidad && npx --yes npm@11.19.1 ci && npx --yes npm@11.19.1 run verify` bajo Node 24.22.0 o 22.23.3.
- Prototipo: `cd Chulito-coding/ST-01_prototipo-python && python -m unittest discover -s tests -v`.
