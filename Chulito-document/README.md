# Chulito-document

Documentos del proyecto. Se numera por tipo; dentro de cada carpeta va la **versión vigente** y, junto a cada `.docx`, su `.pdf` generado desde él. Aquí solo se versionan los archivos de texto (índices, ADR, planes, evidencia y estos READMEs); los binarios (`*.docx`, `*.pdf` y `*.zip`) se guardan **fuera del repositorio**, en `C:\dev\Chulito_documentos\`, con la misma ruta relativa. Las entregas previas al paquete v0.4 se conservan como `.zip` en `_archivo/`, junto a la carpeta `versiones-anteriores/`.

| Carpeta | Contenido | Estado |
|---|---|---|
| `00-control/` | Índice de versiones, trazabilidad requisito → código → prueba, lista de correcciones abiertas | Activa |
| `01-investigacion/` | Guía de entrevistas, evidencia documental y el informe S-0.1 (escenario simulado) | Activa |
| `02-requisitos/` | PRD, SRS e historias de usuario | PRD y SRS activos; historias pendientes |
| `03-arquitectura-decisiones/` | ADR, informes y evidencia de spikes (una carpeta por spike), C4, modelo de datos y API | ADR-0001 propuesto; el resto pendiente |
| `04-sintesis/` | Síntesis documental | Activa |
| `05-operacion/` | Entregas con manifiesto SHA256 y futuros runbooks | Activa |
| `06-seguridad-privacidad/` | Modelo de amenazas (STRIDE), política de datos, Ley 1581 | Pendiente |
| `07-calidad-pruebas/` | Plan de pruebas y definición de terminado | Pendiente |
| `_archivo/` | Zips originales de entregas previas y documentos Word iniciales | Solo lectura |

Convención de nombres: `<Tipo>_<Proyecto>_v<MAYOR>.<MENOR>_<detalle>.<ext>`. Mayor = cambia alcance o requisitos; menor = precisiones.
