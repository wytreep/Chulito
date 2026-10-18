# Este código sale de estos documentos

| Documento origen | Ruta |
|---|---|
| SRS v0.4 (criterios Gherkin §4, modelo de datos §8) | `Chulito-document/02-requisitos/srs/` |
| ST-01 v0.3 (canales y modelo canónico) | `Chulito-document/03-arquitectura-decisiones/spikes/` |

## Qué cubre

SRS-F-10 a F-14, F-22 a F-24 y SRS-NFR-04 como especificación ejecutable, con datos sintéticos.

## Qué NO hace

- No es el backend de producción: está en Python y el objetivo es NestJS/TypeScript (TBD-9).
- No usa muestras reales ni se conecta a ningún canal.

## Nota de nombres

El módulo se renombró de `confirma_vertical_slice.py` (nombre anterior del proyecto) a `chulito_vertical_slice.py`; `run_demo.py` y `tests/` importan el nombre nuevo. El `.docx` de ST-01 v0.3 conserva la mención histórica al nombre anterior al describir la ejecución de esa revisión.
