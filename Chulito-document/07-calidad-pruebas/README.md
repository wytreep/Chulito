# 07-calidad-pruebas

Plan de pruebas, criterios de aceptación ejecutables y definición de terminado por fase.

| Documento | Versión | Estado | Texto |
|---|---|---|---|
| Plan de pruebas | 0.1 | Borrador | `plan-pruebas.md` |

**No se ha ejecutado ninguna prueba de este plan.** El backend de producción no existe (TBD-9) y la captura real sigue pendiente (TBD-1). Los resultados futuros van en `evidencia/`, con fecha, entorno, versión y fixtures.

## Cobertura

- Casos funcionales `TP-F-xx` para cuentas, captura, emparejamiento, libro, auditoría y exportación.
- Casos no funcionales `TP-NFR-xx` para latencia, capacidad, recuperación, seguridad, usabilidad y portabilidad.
- Casos de seguridad `TP-SEC-xx` derivados del modelo STRIDE.
- Matriz requisito → caso para todos los `SRS-F`, `SRS-NFR` y `SRS-RN` del SRS v0.4.

## Evidencia

`evidencia/` guardará los registros de ejecución. Los binarios (capturas, reportes) se guardan fuera del repositorio, en `C:\dev\Chulito_documentos\Chulito-document\07-calidad-pruebas\`.
