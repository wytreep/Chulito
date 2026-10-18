# Chulito — entrega documental y técnica corregida

**Fecha:** 17 de octubre de 2026  
**Estado:** paquete de trabajo; requisitos, decisiones de producto y stack pendientes de revisión/aprobación.

> **S-0.1 es un escenario simulado, no resultados de entrevistas realizadas.** Las cifras y perfiles son ficticios; no son evidencia de campo, mercado, preferencias ni validación del segmento o alcance del MVP.

## Qué contiene

- **Síntesis Documental SD-0.3:** fuente Markdown, Word editable y PDF. Reemplaza la presentación de S-0.1 como “base operativa” por un supuesto de trabajo explícitamente simulado. Las decisiones de segmento/alcance quedan sujetas a entrevistas reales.
- **SRS v0.3:** Word editable y PDF, derivado del PRD v0.3, con aviso metodológico explícito, historial de corrección y TBD para validación real, compatibilidad del stack (ADR-0001) y port de la vertical slice a TypeScript/NestJS.
- **Spike técnico ST-01 v0.2:** Markdown, Word editable y PDF. Corrige el conteo a **12/12 pruebas**, describe el código Python como especificación ejecutable y separa el spike de canales del spike de compatibilidad Node.js/TypeScript/NestJS, todavía no ejecutado.
- **Código y fixtures sintéticos:** prototipo Python, pruebas automatizadas, ejemplo de eventos y demo reproducible.
- **Trazabilidad y contexto:** PRD v0.3, guía de entrevistas v0.1, informe S-0.1 y fuentes oficiales de captura.
- **Aclaración del PRD:** se incluye un anexo editorial Word/PDF con la cláusula explícita y una copia compuesta del PDF del PRD con ese anexo al frente. El PDF fuente original se conserva intacto por separado; el anexo no crea una revisión nueva del PRD.

## Validación técnica reproducible

Desde `spike/` ejecutar:

```bash
python3 -m unittest discover -s tests -v
python3 run_demo.py
```

Resultado al 17-oct-2026: **12 pruebas aprobadas**. La demo usa exclusivamente datos sintéticos y produce una identidad canónica de pago a partir de dos observaciones de canal.

## Límites y pendientes

Las pruebas no acreditan integraciones reales, cobertura de emisores ni preferencias de usuarios. Las entrevistas no bloquean el trabajo técnico con datos sintéticos, pero sí son necesarias para validar problema, segmento y alcance antes de baselinar el MVP o iniciar un piloto. El código actual está en Python; el port y las pruebas equivalentes en TypeScript/NestJS están pendientes. El spike de compatibilidad previsto para ADR-0001 no se ha ejecutado y es distinto del ST-01, que cubre canales de captura.

El PRD v0.3 disponible en el workspace original es PDF. No se encontró un DOCX fuente del PRD, por lo que este paquete conserva el PDF original y no fabrica una reconstrucción editable potencialmente infiel. El anexo de aclaración sí incluye DOCX editable y PDF, pero no sustituye el texto editable del PRD. Las revisiones SD-0.3, SRS v0.3 y ST-01 v0.2 sí incluyen fuente editable cuando aplica, DOCX y PDF.

## Archivos principales

- `documentos/Sintesis_Documental_Chulito_SD-0.3.md` / `.docx` / `.pdf`
- `documentos/SRS_Chulito_v0.3_29148_alineacion_estructural.docx` / `.pdf`
- `documentos/Spike_Tecnico_Chulito_ST-01_v0.2.md` / `.docx` / `.pdf`
- `referencias/PRD_Chulito_v0.3_ISO29148.pdf`
- `referencias/PRD_Chulito_v0.3_ISO29148_original.pdf` (copia fuente intacta)
- `referencias/PRD_Chulito_v0.3_paquete_con_aviso.pdf` (anexo editorial al frente + fuente original)
- `referencias/Aclaracion_Metodologica_PRD_v0.3.docx` / `.pdf`
- `referencias/Informe_Hallazgos_Chulito_S-0.1_Escenario_Simulado.pdf`
- `spike/README.md`, código, pruebas, fixtures y referencias oficiales
- `scripts/` contiene los generadores y el actualizador SRS usados para las revisiones.
