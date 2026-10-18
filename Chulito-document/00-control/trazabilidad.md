# Trazabilidad requisito → código → prueba

| Requisito | Código | Prueba | Estado real |
|---|---|---|---|
| SRS-F-13, F-05, F-22, F-24, F-14, F-03 | `ST-01_prototipo-python/` | `tests/test_vertical_slice.py` | Especificación ejecutable en Python |
| SRS-F-02, F-04, F-20 a F-25, UC-01 a UC-06 | `SRS-v0.4_mockup-ui/` | Revisión visual | Prototipo sin backend |
| ADR-0001 (baseline) | `ADR-0001_spike-compatibilidad/` | `npm run verify` | Verificado en Node 24.22.0 y 22.23.3; PostgreSQL pendiente |
| TBD-9 (port a TypeScript) | — | — | Sin código de dominio en TypeScript todavía |
