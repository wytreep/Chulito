# Confirma — spike técnico de captura y vertical slice

**Revisión:** 0.2 · **Fecha:** 17 de octubre de 2026  
**Propósito:** reducir riesgo técnico de los canales de captura y probar con datos sintéticos el flujo `captura → normalización → idempotencia → conciliación`.

> **S-0.1 es un escenario simulado, no resultados de entrevistas realizadas.** Sus cifras no validan preferencias, segmento ni alcance del MVP. El PRD v0.3 también identifica S-0.1 como escenario de trabajo y pide contrastar sus supuestos con entrevistas reales.

## Resultado del spike de canales

Se compararon la lectura de Gmail mediante OAuth, el reenvío de correo con filtro y el listener Android. La evidencia y las referencias están en [Fuentes oficiales de captura](Fuentes_Oficiales_Captura_2026-10-13.md).

**Conclusión provisional:** no acoplar la vertical slice a un canal externo ni cerrar todavía la vía de captura. Para una prueba posterior, comparar reenvío filtrado (menos privilegio API, pero transferencia de contenido y configuración por el usuario) con listener Android (captura de notificaciones de apps, pero exige app Android y habilitación del listener). No usar lectura amplia de Gmail como primera alternativa del MVP. No priorizar canales por S-0.1; registrar la decisión mediante ADR tras validar cobertura con muestras autorizadas y revisar privacidad.

## Modelo canónico propuesto

### `CaptureEnvelope`

| Campo | Tipo | Obligatorio | Uso |
|---|---|---:|---|
| `tenant_id` | string/UUID | Sí | Contexto de aislamiento; nunca inferido del texto del mensaje. |
| `channel` | enum | Sí | `email_forward`, `android_listener` u otro adaptador futuro. |
| `source_event_id` | string nullable | No | ID estable proporcionado por el origen; se usa para reintentos del mismo evento. |
| `source_name` | string | Sí | Dirección remitente o paquete Android; metadato interno. |
| `title` | string | No | Asunto de correo o título de notificación. |
| `text` | string | Sí | Cuerpo/texto transitorio para el parser; su persistencia requiere cifrado y retención definidos. |
| `received_at_utc` | timestamp ISO 8601 UTC | Sí | Momento de recepción por el adaptador. |
| `payload_fingerprint` | SHA-256 | Derivado | Huella de contenido para trazabilidad y fallback de idempotencia. |

### `PaymentNotice` normalizado

`tenant_id`, `issuer`, `amount_cop` (monto en pesos colombianos como entero; sin punto de miles ni escalamiento por 100), `currency=COP`, `occurred_at_utc`, `reference` nullable, `operation_type`, `source_channel`, `source_event_id`, `received_at_utc`, `payload_fingerprint`. Los datos ausentes se mantienen como `null`; **no se inventan**.

En producción, separar la notificación cruda (cifrada, acceso restringido y retención explícita) del pago canónico. La vertical slice conserva solo huellas, metadatos mínimos y estado; no escribe los textos crudos en SQLite.

## Idempotencia: dos niveles

1. **Evento de captura/reintento:** clave por `tenant_id + channel + source_event_id`; si el origen no tiene ID estable, usar `tenant_id + channel + payload_fingerprint`. Repetir el mismo evento no ejecuta de nuevo la conciliación.
2. **Identidad de transacción:** clave por `tenant_id + issuer + reference` solo cuando se valide que la referencia es estable y suficientemente única para el emisor. Así, una misma transacción recibida por correo y Android no crea dos pagos. Sin referencia, el fallback es por canal y huella exacta; **no se deduplican canales distintos a ciegas**. Esto puede dejar un posible duplicado para revisión, pero reduce el riesgo de fusionar dos pagos legítimos.

## Regla conservadora de conciliación de la slice

- Una única coincidencia por negocio, monto, referencia y ventana de 10 minutos → `confirmed`.
- Más de una candidata o referencia ausente → `review`; no confirmar automáticamente.
- Si hay una candidata temporal con el mismo monto o referencia, pero el otro dato discrepa → `doubtful`; un cobro meramente cercano sin señales coincidentes queda sin asociación.
- Sin candidato del mismo negocio dentro de la ventana → `unmatched`.
- Sin parser compatible → `unparsed`, sin crear un pago.

La ventana de 10 minutos replica el valor provisional del SRS y debe permanecer configurable/por validar (TBD-3). No se hacen búsquedas de cobros de otros negocios.

## Ejecución

```bash
python3 -m unittest discover -s tests -v
python3 run_demo.py
```

Implementación: [`confirma_vertical_slice.py`](confirma_vertical_slice.py). Pruebas: [`tests/test_vertical_slice.py`](tests/test_vertical_slice.py). Fixtures de referencia: [`examples/synthetic_events.json`](examples/synthetic_events.json).

**Resultado verificado el 17-oct-2026:** 12/12 pruebas pasan; la demo procesa dos observaciones sintéticas (correo y Android) como un pago canónico. Esto verifica únicamente reglas del prototipo con fixtures inventados: no es evidencia de entrevistas, cobertura de emisores ni validación de mercado.

**Stack:** el prototipo está implementado en Python como especificación ejecutable, no como backend objetivo ni código de producción. El stack previsto es NestJS/TypeScript; falta portar la lógica y las pruebas. También está pendiente el spike de compatibilidad Node.js/TypeScript/NestJS/dependencias asociado a ADR-0001. Este ST-01 trata canales de captura y no ejecuta ni sustituye ese spike.

## Fuera de alcance y limitaciones conocidas

- Los dominios `.invalid`, los nombres de paquete `*.fixture.invalid`, el asunto y el texto son **datos inventados**; no representan formatos de Nequi, Daviplata ni bancos.
- No hay OAuth, app Android, recepción SMTP/HTTP, API pública, multiusuario real, cifrado, autorización ni persistencia productiva.
- La referencia de transacción no se ha validado como globalmente única por emisor. Si no se puede comprobar, se debe rebajar esa clave y usar revisión de posibles duplicados.
- El prototipo guarda un hash de mensajes no reconocidos, pero no implementa la retención de contenido crudo que pide el requisito derivado SRS-F-14. La implementación real debe resolver cifrado, acceso, aviso al dueño y retención antes de piloto.
- El código usa SQLite en memoria para hacer reproducibles las pruebas; no es una recomendación de motor productivo.

## Próximas decisiones

1. Validar con entrevistas reales el segmento, problema y alcance del MVP; las entrevistas no bloquean pruebas técnicas sintéticas, pero sí decisiones de producto y piloto.
2. Elegir emisores según uso real y viabilidad, y obtener muestras autorizadas/anónimas.
3. Ejecutar el spike de captura en un Android de prueba y con un buzón de prueba: latencia, campos disponibles, falsas conciliaciones, configuración y revocación.
4. Validar unicidad de referencias, zonas horarias y formatos de monto por emisor.
5. Definir política de retención/cifrado y permisos mínimos antes de almacenar contenido original.
6. Ejecutar por separado el spike de compatibilidad para ADR-0001 y fijar versiones.
7. Portar la especificación ejecutable y las pruebas a TypeScript/NestJS; registrar ADR de canal aparte.
