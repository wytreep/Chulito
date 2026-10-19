# Chulito-coding

Código derivado de los documentos. **El nombre de cada carpeta indica de dónde sale**: `<ID del documento origen>_<qué es>`.

| Carpeta | Sale de | Qué es | Estado |
|---|---|---|---|
| `ST-01_prototipo-python/` | ST-01 v0.3 y SRS v0.4 (§4 y §8) | Especificación ejecutable en Python | 12 pruebas reportadas; verificadas en una sesión anterior |
| `ADR-0001_spike-compatibilidad/` | ADR-0001 | Harness NestJS/TypeScript para probar la matriz de versiones | Verificado en Node 24.22.0 y 22.23.3; PostgreSQL sin ejecutar |
| `SRS-v0.4_mockup-ui/` | SRS v0.4 (pantallas y UC-01 a UC-06) | Mockup HTML con datos sintéticos | Completo: `Chulito_Mockup_v0.4.html` junto a `DERIVADO_DE.md` |

Cada carpeta contiene `DERIVADO_DE.md`. La del harness también incluye `tools/capture_registry_metadata.py`, que genera el snapshot de metadata de npm. Cuando empiece el backend de producción (TBD-9) irá en una carpeta nueva, por ejemplo `SRS-v1.0_api-nestjs/`, con su propio `DERIVADO_DE.md`.
