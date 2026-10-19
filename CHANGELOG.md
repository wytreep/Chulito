# Cambios por entrega

## Sin publicar
- Estructura definitiva del repositorio: `Chulito-document/` por tipo y `Chulito-coding/` por documento de origen, con `.gitkeep` en las carpetas todavía vacías.
- `spikes/` reorganizado en una carpeta por spike (`ST-01_canales/`, `TBD-8_compatibilidad/` con `README.md`, `evidence/` y `plan/`). El ADR vive en `adr/ADR-0001_baseline-node-typescript-nestjs.md` y `capture_registry_metadata.py` en `Chulito-coding/ADR-0001_spike-compatibilidad/tools/`.
- `_archivo/` conserva solo los dos `.zip` de entregas previas —sin descomprimir— y estrena `versiones-anteriores/` (v0.1 y v0.2, más los PDF sueltos de la guía v0.1 y el PRD v0.3). `Fuentes_Oficiales_Captura_2026-10-13.md` se rescató a `01-investigacion/evidencia-documental/`.
- `05-operacion/entregas/` guarda los zips congelados de `entrega-v0.4_2026-10-17` y `entrega-adr0001-r1_2026-10-18`.
- ADR-0001 **revisión 2**: `@types/node` 22.20.5, Vitest 5.0.5, `oxlint`/`prettier` con `format:check`, `engines.npm`, postinstall de `@scarf/scarf` denegado y matriz repetida en Node 24.22.0 y 22.23.3 (evidencia en `Chulito-document/03-arquitectura-decisiones/spikes/TBD-8_compatibilidad/evidence/verification-2026-10-18-revision-2.md`).
- Prototipo Python: el módulo del prototipo es `chulito_vertical_slice.py`, con sus imports en `run_demo.py` y `tests/`.
- Mockup de UI `Chulito_Mockup_v0.4.html` ubicado en `Chulito-coding/SRS-v0.4_mockup-ui/`, junto a su `DERIVADO_DE.md`.
- Nombre del proyecto unificado a **Chulito** en nombres de archivo y carpeta y en el texto de la documentación.

## entrega-v0.4 (2026-10-17)
- PRD v0.4, SRS v0.4, síntesis SD-0.4, guía de entrevistas v0.2, informe S-0.1 (escenario simulado), ST-01 v0.3 y prototipo Python.

## adr-0001-r1 (2026-10-18)
- ADR-0001 propuesto con harness de compatibilidad (Node 24.22.0 y 22.23.3).
