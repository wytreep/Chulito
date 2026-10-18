# Chulito — entrega documental v0.4

**Fecha:** 17 de octubre de 2026  
**Estado:** borradores integrados, pendientes de revisión y aprobación formal.  
**Identidad documental:** los códigos `CNF-*` se conservan como prefijo histórico de Confirma para no romper la trazabilidad; la marca visible vigente es **Chulito**.

> **S-0.1 es un escenario simulado, no resultados de entrevistas realizadas.** Sus 16 registros, perfiles y proporciones son ficticios. No son evidencia de campo, no estiman el mercado y no justifican decisiones de segmento, prioridad o alcance.

## Documentos vigentes

| Artefacto | Versión | Editable | Lectura |
|---|---:|---|---|
| PRD de visión y alcance, con comparación de alternativas y registro de evidencia | v0.4 | [DOCX](PRD/Chulito_PRD_v0.4_2026-10-17.docx) | [PDF](PRD/Chulito_PRD_v0.4_2026-10-17.pdf) |
| Especificación de requisitos de software, estructura alineada con ISO/IEC/IEEE 29148:2018 | v0.4 | [DOCX](SRS/SRS_Chulito_v0.4_29148_alineacion_estructural.docx) | [PDF](SRS/SRS_Chulito_v0.4_29148_alineacion_estructural.pdf) |
| Síntesis documental reconciliada con PRD/SRS v0.4 | SD-0.4 | [DOCX](Sintesis/Sintesis_Documental_Chulito_SD-0.4.docx) | [PDF](Sintesis/Sintesis_Documental_Chulito_SD-0.4.pdf) |
| Guía de entrevistas con consentimiento y privacidad reforzados | v0.2 | [DOCX](Investigacion/Chulito_01_Guia_de_Entrevistas_v0.2.docx) | [PDF](Investigacion/Chulito_01_Guia_de_Entrevistas_v0.2.pdf) |
| Informe S-0.1, explícitamente rotulado como escenario simulado | revisión v0.2 | [DOCX](Investigacion/Chulito_03_Hallazgos_S-0.1_ESCENARIO_SIMULADO_revision_v0.2.docx) | [PDF](Investigacion/Chulito_03_Hallazgos_S-0.1_ESCENARIO_SIMULADO_revision_v0.2.pdf) |
| Spike de canales y modelo canónico | ST-01 v0.3 | [DOCX](Spike/Spike_Tecnico_Chulito_ST-01_v0.3.docx) | [PDF](Spike/Spike_Tecnico_Chulito_ST-01_v0.3.pdf) |

Cada documento tiene una sola versión editable vigente en este paquete. Los PDF se generaron desde sus respectivos DOCX.

## Posicionamiento, evidencia y límites

El PRD contrasta Nequi Negocios, Kuadra, Cajero y Bre-B usando páginas públicas de producto, proveedor o entidad oficial, con fecha y nivel de evidencia. Bre-B se trata como infraestructura interoperable, no como una aplicación competidora. La comparación no afirma paridad funcional ni demuestra demanda por Chulito; el posicionamiento multiemisor con rol de cajero es una hipótesis que debe probarse con personas usuarias reales.

La guía v0.2 sirve para entrevistas futuras: participar es voluntario, el permiso de grabación se solicita por separado, las personas pueden retirarse y no se deben recopilar credenciales ni datos reales de clientes. La guía no convierte S-0.1 en entrevistas.

## Estado técnico y decisiones abiertas

- **TBD-1:** canal de captura pendiente de prueba autorizada y ADR.
- **TBD-2:** emisores y muestras reales autorizadas pendientes; no se afirma cobertura de Nequi, Daviplata ni otros emisores.
- **TBD-3:** ventana de conciliación de 10 minutos provisional, sujeta a validación con flujos reales.
- **TBD-4:** retención propuesta —cuerpo original cifrado hasta 7 días y campos normalizados 12 meses—, sujeta a asesoría legal; no es una conclusión de cumplimiento.
- **TBD-5:** dirección de producto v0.4: avisos in-app y correo; SMS y push fuera del MVP. Requiere consentimiento y pruebas de entrega.
- **TBD-6:** revisión legal local pendiente antes del piloto.
- **TBD-7:** entrevistas reales para validar problema, segmento y alcance pendientes; bloquean baselining y piloto, no las pruebas sintéticas.
- **TBD-8:** spike de compatibilidad Node.js/TypeScript/NestJS y dependencias no ejecutado; debe producir ADR-0001.
- **TBD-9:** port de la especificación Python a TypeScript/NestJS pendiente.

La mención de alineación estructural con ISO/IEC/IEEE 29148:2018 no constituye certificación ni declaración formal de conformidad.

## Prototipo sintético

El código de `Prototipo/` es una especificación ejecutable de referencia, no el backend de producción. No hace llamadas de red ni integra Gmail, Android, Nequi, Daviplata o APIs bancarias. Los datos son fixtures inventados. La suite tiene 12 pruebas; se verificó con:

```bash
cd Prototipo
python3 -m unittest discover -s tests -v
python3 run_demo.py
```

La ejecución incluida en esta entrega produjo 12/12 pruebas aprobadas y una demo con `synthetic_only: true`, dos observaciones sintéticas y un pago canónico. Esto no valida formatos de emisores reales, compatibilidad del stack, preferencia de usuarios, desempeño en producción ni cumplimiento legal.
