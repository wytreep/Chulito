# Cambios por entrega

## Sin publicar
- Documentos legales en **borrador v0.1** en `06-seguridad-privacidad/`: política de tratamiento de datos, aviso de privacidad y autorización de tratamiento. Texto en el repositorio y PDF en `C:\dev\Chulito_documentos\`. Sujetos a revisión legal (TBD-6); no usar con datos reales.
- Modelo de amenazas **STRIDE v0.1** en `06-seguridad-privacidad/modelo-amenazas-stride.md`: activos, actores, amenazas S/T/R/I/D/E, amenazas propias del dominio (comprobantes duplicados o de otro negocio), controles por capa y 14 requisitos de seguridad derivados. Borrador de diseño: el backend (TBD-9) aún no existe y la trazabilidad al SRS queda pendiente.
- Términos y condiciones del servicio en **borrador v0.1** (`06-seguridad-privacidad/terminos-y-condiciones.md`): aceptación, descripción del servicio, límites explícitos (no es entidad financiera, no mueve dinero, no certifica el pago ni la identidad del pagador), uso aceptable, datos de terceros, licencia, disponibilidad, responsabilidad, terminación y ley aplicable (Colombia). Pendiente: precio, plan y revisión legal (TBD-6).
- Política de cookies en **borrador v0.1** (`06-seguridad-privacidad/politica-cookies.md`): tipos de cookies, inventario previsto, consentimiento opt-in para las no esenciales y administración desde el navegador. El frontend no existe aún (TBD-9): la tabla debe reemplazarse con el inventario real.
- Historias de usuario **v0.1** (`02-requisitos/historias-usuario/historias-usuario.md`): US-01 a US-08 derivadas del SRS v0.4, con criterios Dado/Cuando/Entonces, roles, matriz de trazabilidad y dependencias de los TBD.
- Plan de pruebas **v0.1** (`07-calidad-pruebas/plan-pruebas.md`): estrategia por niveles, datos sintéticos, 23 casos funcionales, 13 no funcionales, 10 de seguridad derivados de STRIDE, matriz requisito → caso y criterios de salida por fase. Sin pruebas ejecutadas.
- Modelo **C4 v0.1** (`03-arquitectura-decisiones/c4/modelo-c4.md`): contexto, contenedores, componentes de API y worker, flujo de captura, límites de confianza, despliegue propuesto y decisiones aún abiertas (cola, ORM, tiempo real, nube, TBD-1). Diagramas Mermaid renderizados a SVG para el PDF.
- El repositorio guarda solo texto (`.md`) y código. Los binarios (`*.docx`, `*.pdf` y `*.zip`) viven **fuera** del repositorio, en `C:\dev\Chulito_documentos\`, con la misma ruta relativa; aquí quedan la estructura, los READMEs y un `.gitkeep` por carpeta. Se ignoran esos formatos en `.gitignore` para no reincorporarlos por accidente.
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
