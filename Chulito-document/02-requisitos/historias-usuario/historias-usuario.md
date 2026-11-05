# Historias de usuario

**Chulito — confirmación compartida de pagos y libro diario para negocios pequeños**

> **BORRADOR (v0.1).** Historias derivadas del SRS v0.4. No son evidencia de entrevistas: el escenario S-0.1 es simulado. Los criterios de aceptación son verificables, pero **no se han ejecutado**. Sujetas a revisión de producto antes de baselinar el MVP.

| Campo | Valor |
|---|---|
| Versión | 0.1 (borrador) |
| Fecha | 4 de noviembre de 2026 |
| Estado | Borrador — pendiente de revisión de producto |
| Fuente | SRS v0.4 (`SRS-F-xx`, `SRS-NFR-xx`, `SRS-RN-xx`, US-01…US-08) |
| Origen | PRD CNF-PRD-001 v0.4 |
| Alcance | MVP en diseño; el backend de producción no existe (TBD-9) |

## 1. Convenciones

- **Prioridad:** Alta (MVP), Media (MVP deseable), Baja (después del MVP).
- **Trazas:** cada historia cita los IDs del SRS y del PRD que implementa.
- **Criterios:** formato Dado / Cuando / Entonces, verificables con el plan de pruebas (`07-calidad-pruebas/plan-pruebas.md`).
- **Roles:** Dueño, Cajero, Operador técnico y Titular de los datos, según el SRS §2.3.
- **Estado de implementación:** ninguna historia está implementada. El prototipo Python es una especificación ejecutable, no producción.

## 2. Roles y objetivos

| Rol | Objetivo principal | Lo que no puede hacer |
|---|---|---|
| Dueño | Controlar el negocio, sus cajeros, la captura y los datos | Acceder a datos de otro negocio |
| Cajero | Registrar cobros y ver los pagos de su negocio | Ver credenciales, configuración de captura ni exportar |
| Operador técnico | Operar el servicio y ver métricas | Ver el contenido de los pagos |
| Titular de los datos | Otorgar o revocar consentimiento y pedir sus datos | Exportar datos de otro titular |

## 3. Historias

### US-01 — Registrar negocio y cajero

**Como** dueño, **quiero** registrar mi negocio y crear cajeros, **para** separar responsabilidades sin compartir mis credenciales.

| Campo | Valor |
|---|---|
| Prioridad | Alta |
| Trazas SRS | `SRS-F-01`, `SRS-F-02`, `SRS-F-03`, `SRS-F-04`, `SRS-F-05`, `SRS-RN-05` |
| Trazas PRD | §7.1, RF-06, RF-07 |

**Criterios de aceptación**

1. **Dado** un visitante sin cuenta, **cuando** registra un negocio y su cuenta de dueño con datos válidos, **entonces** se crea el negocio (tenant), la cuenta queda asociada a él y puede iniciar sesión.
2. **Dado** un dueño autenticado, **cuando** crea un cajero, **entonces** el cajero recibe acceso limitado a ver pagos de su negocio y registrar cobros esperados, y no ve credenciales, consentimientos administrativos ni configuración de captura.
3. **Dado** un cajero con sesión activa, **cuando** el dueño revoca su cuenta, **entonces** las solicitudes posteriores de esa cuenta se rechazan.
4. **Dado** un cajero del negocio A, **cuando** solicita pagos, auditoría o exportaciones del negocio B, **entonces** la solicitud se rechaza sin revelar si B existe.
5. **Dado** un usuario inactivo, **cuando** supera el tiempo configurado, **entonces** la sesión se cierra y debe autenticarse de nuevo.

**Notas**

- El registro debe explicar en la interfaz que Chulito no custodia ni mueve fondos.
- La verificación de correo y la política de contraseñas se definen en el ADR de seguridad y en el SRS `SRS-NFR-05`.

### US-02 — Otorgar y revocar consentimiento

**Como** dueño, **quiero** habilitar o revocar explícitamente la captura y los avisos, **para** controlar el tratamiento de los datos de mi negocio.

| Campo | Valor |
|---|---|
| Prioridad | Alta |
| Trazas SRS | `SRS-F-10`, `SRS-F-40`, `SRS-NFR-07` |
| Trazas PRD | RF-01, RNF-02, RNF-04 |

**Criterios de aceptación**

1. **Dado** un negocio sin consentimiento de captura, **cuando** intenta habilitar la captura, **entonces** el sistema exige leer el alcance y aceptar el texto vigente antes de activarla.
2. **Dado** un consentimiento otorgado, **cuando** se registra, **entonces** quedan guardados tenant, actor, alcance, versión del texto, fecha y hora, y estado.
3. **Dado** un consentimiento vigente, **cuando** el titular lo revoca, **entonces** la revocación queda auditada y no se inician nuevas capturas ni avisos dentro del alcance revocado.
4. **Dado** un consentimiento revocado, **cuando** existen datos anteriores, **entonces** siguen sujetos a la retención y a las solicitudes de eliminación, y la interfaz lo explica.
5. **Dado** el flujo de captura, **cuando** el dueño lo activa, **entonces** puede otorgar captura y avisos por separado.

### US-03 — Registrar un cobro y ver el pago en vivo

**Como** cajero, **quiero** registrar un cobro esperado y ver el pago en vivo, **para** confirmar la venta sin salir de la pantalla.

| Campo | Valor |
|---|---|
| Prioridad | Alta |
| Trazas SRS | `SRS-F-20`, `SRS-F-21`, `SRS-F-22`, `SRS-F-23`, `SRS-RN-02`, `SRS-RN-03` |
| Trazas PRD | RF-03, RF-04 |

**Criterios de aceptación**

1. **Dado** un cajero autenticado, **cuando** registra un cobro con monto mayor que cero y referencia opcional, **entonces** el cobro queda en estado **Pendiente**.
2. **Dado** un cobro de 25.000 COP creado hace 2 minutos, **cuando** llega un pago de 25.000 COP con referencia coincidente dentro de la ventana, **entonces** el cobro pasa a **Confirmado** y se muestra al cajero.
3. **Dado** un pago confirmado, **cuando** se renderiza en la vista del cajero, **entonces** el p95 desde `received_at` hasta el render es ≤ 10 s (`SRS-NFR-01`).
4. **Dado** un canal caído, **cuando** el cajero mira la pantalla, **entonces** ve el estado del canal y no aparece un pago inventado.
5. **Dado** un pago que ya emparejó un cobro, **cuando** llega otro cobro, **entonces** no se reutiliza el mismo pago (`SRS-RN-02`).

### US-04 — Distinguir un pago dudoso o tardío

**Como** cajero, **quiero** distinguir un pago dudoso o tardío de uno confirmado, **para** no afirmar una confirmación incorrecta.

| Campo | Valor |
|---|---|
| Prioridad | Alta |
| Trazas SRS | `SRS-F-23`, `SRS-F-24`, `SRS-F-25`, `SRS-RN-03`, `SRS-RN-04` |
| Trazas PRD | RF-08 |

**Criterios de aceptación**

1. **Dado** un cobro de 25.000 COP, **cuando** llega un pago de 2.500 COP dentro de la ventana, **entonces** el pago queda **Dudoso** y el cobro sigue **Pendiente**.
2. **Dado** un evento con `occurred_at` anterior y `received_at` posterior a la ventana, **cuando** se procesa, **entonces** se conservan ambos tiempos y se marca tardío o dudoso según la regla, sin presentarlo como confirmado.
3. **Dado** un cobro **Dudoso**, **cuando** el dueño lo resuelve manualmente, **entonces** queda **Confirmado**, se agrega un evento de auditoría y el pago original no se modifica.
4. **Dado** un pago dudoso, **cuando** se muestra en la interfaz, **entonces** la interfaz no usa la expresión «pago recibido» ni sugiere una confirmación que no existe.
5. **Dado** un usuario sin rol de dueño, **cuando** intenta resolver un dudoso, **entonces** la acción se rechaza.

### US-05 — Ver el estado del canal y las brechas potenciales

**Como** dueño, **quiero** ver si el canal está caído, retrasado o con reintentos, **para** investigar una brecha sin que el sistema invente pagos.

| Campo | Valor |
|---|---|
| Prioridad | Media |
| Trazas SRS | `SRS-F-14`, `SRS-F-15`, `SRS-NFR-04`, `SRS-NFR-11` |
| Trazas PRD | RF-01, RF-02, RK2, RK3 |

**Criterios de aceptación**

1. **Dado** un negocio con captura habilitada, **cuando** el dueño abre el panel, **entonces** ve la última captura del adaptador, el estado del canal, los errores recientes y los reintentos.
2. **Dado** un canal sin conexión, **cuando** el envío no puede confirmarse, **entonces** el estado pasa a **degradado**, se registran intentos y error, se reintenta con espera creciente y no se crea un pago.
3. **Dado** una señal observable de pérdida o retraso, **cuando** se detecta, **entonces** se registra una **brecha potencial** por tenant y canal, se reintenta o escala y se avisa si hay consentimiento.
4. **Dado** un mensaje que ningún parser reconoce, **cuando** se recibe, **entonces** se conserva como **no reconocido**, se avisa al dueño si corresponde y no se convierte en pago.
5. **Dado** una brecha potencial, **cuando** se muestra, **entonces** la interfaz aclara que no equivale a un pago perdido confirmado.

### US-06 — Libro diario y exportación de datos propios

**Como** dueño, **quiero** un libro diario y una exportación estructurada de mis datos, **para** revisar operaciones y ejercer control del tenant.

| Campo | Valor |
|---|---|
| Prioridad | Alta (libro), Baja (exportación) |
| Trazas SRS | `SRS-F-30`, `SRS-F-31`, `SRS-F-32`, `SRS-F-41`, `SRS-RN-01`, `SRS-RN-06` |
| Trazas PRD | RF-05, RNF-02 |

**Criterios de aceptación**

1. **Dado** un negocio con pagos de varios emisores, **cuando** el dueño consulta el libro diario, **entonces** ve los pagos del día agrupados por negocio y fecha, con `occurred_at` y `received_at` diferenciados cuando ambos existen.
2. **Dado** el cierre del día, **cuando** se genera, **entonces** incluye totales por emisor y por cajero, las diferencias frente a los cobros esperados y usa la zona `America/Bogota`.
3. **Dado** un pago de otro negocio, **cuando** se calcula el cierre, **entonces** no aparece en los totales (`SRS-RN-01`).
4. **Dado** un dueño autenticado, **cuando** exporta CSV o JSON con filtros de fecha, **entonces** obtiene solo datos de su tenant, con auditoría de la exportación.
5. **Dado** un cajero o un tenant ajeno, **cuando** intenta exportar, **entonces** la solicitud se rechaza.
6. **Dado** una brecha potencial, **cuando** se calculan los totales, **entonces** no se suma como pago.

### US-07 — Medir el tiempo de captura a render

**Como** operador técnico, **quiero** medir el tiempo desde la captura del adaptador hasta el render, **para** reportar `SRS-NFR-01` por canal y emisor sin incluir latencia anterior.

| Campo | Valor |
|---|---|
| Prioridad | Media |
| Trazas SRS | `SRS-NFR-01`, `SRS-NFR-11` |
| Trazas PRD | Métricas del PRD |

**Criterios de aceptación**

1. **Dado** un evento aceptado por el adaptador, **cuando** se renderiza en la vista del cajero, **entonces** existe un identificador de correlación que une adaptador, emisor, evento, procesamiento y render.
2. **Dado** un conjunto de al menos 200 eventos elegibles en 3 sesiones, **cuando** se calcula la métrica, **entonces** se reportan p50, p95, p99, n, pérdidas, duplicados y exclusiones por canal y emisor.
3. **Dado** un evento con `occurred_at`, **cuando** se mide, **entonces** `occurred_at` se reporta por separado y no se usa como inicio de la medición.
4. **Dado** un mensaje rechazado antes de la captura o sin ruta observable al render, **cuando** se calcula la muestra, **entonces** se excluye y la exclusión queda documentada.

### US-08 — Recibir avisos de brecha

**Como** dueño, **quiero** recibir avisos de brecha por canales aprobados, **para** actuar a tiempo, con consentimiento y sin SMS ni push en el MVP.

| Campo | Valor |
|---|---|
| Prioridad | Media |
| Trazas SRS | `SRS-F-15`, `SRS-F-40`, `SRS-NFR-07` |
| Trazas PRD | RK2, RK3, RNF-02 |

**Criterios de aceptación**

1. **Dado** consentimiento de aviso vigente, **cuando** se detecta una brecha, **entonces** se muestra dentro de la aplicación y se envía por correo electrónico.
2. **Dado** un consentimiento revocado, **cuando** se detecta una brecha, **entonces** no se envían nuevos avisos dentro del alcance revocado.
3. **Dado** un aviso de brecha, **cuando** se genera, **entonces** describe señal, tenant, canal, marcas de tiempo, intentos y estado, y no afirma que existió un pago.
4. **Dado** el MVP, **cuando** se configura el canal, **entonces** SMS y push no están disponibles.
5. **Dado** un aviso enviado, **cuando** se consulta la auditoría, **entonces** el envío queda registrado.

## 4. Matriz de trazabilidad

| Historia | Requisitos SRS | Prioridad |
|---|---|---|
| US-01 | F-01, F-02, F-03, F-04, F-05, RN-05 | Alta |
| US-02 | F-10, F-40, NFR-07 | Alta |
| US-03 | F-20, F-21, F-22, F-23, RN-02, RN-03, NFR-01 | Alta |
| US-04 | F-23, F-24, F-25, RN-03, RN-04 | Alta |
| US-05 | F-14, F-15, NFR-04, NFR-11 | Media |
| US-06 | F-30, F-31, F-32, F-41, RN-01, RN-06 | Alta / Baja |
| US-07 | NFR-01, NFR-11 | Media |
| US-08 | F-15, F-40, NFR-07 | Media |

## 5. Fuera de alcance de estas historias

- Integraciones oficiales con bancos o billeteras (no existen en el MVP; TBD-1 y TBD-2).
- Custodia o movimiento de fondos.
- Facturación electrónica, punto de venta o nómina.
- Notificaciones por SMS o push.
- Aplicación móvil nativa.
- Analítica de producto y cookies no esenciales (ver `06-seguridad-privacidad/politica-cookies.md`).

## 6. Pendientes que afectan la aceptación

| Pendiente | Efecto sobre las historias |
|---|---|
| TBD-1 vía de captura | US-03, US-05, US-08 no pueden probarse de extremo a extremo con un canal real |
| TBD-2 emisores y muestras | US-03 y US-05 dependen de fixtures autorizados |
| TBD-3 ventana de emparejamiento | US-03 y US-04 usan 10 minutos provisionales |
| TBD-4 retención | US-02 y US-06 dependen de los plazos definitivos |
| TBD-6 revisión legal | US-02, US-06 y US-08 dependen de los textos aprobados |
| TBD-9 port a TypeScript | Ninguna historia es implementación de producción todavía |

## 7. Definición de terminado

Una historia se considera terminada cuando:

1. cumple todos sus criterios de aceptación con pruebas automatizadas o evidencia de inspección;
2. tiene trazabilidad a los IDs del SRS y al caso de prueba correspondiente del plan;
3. no introduce datos reales ni secretos;
4. actualiza el SRS si cambia el alcance;
5. pasa la revisión de seguridad aplicable del modelo STRIDE.

El detalle operativo está en `07-calidad-pruebas/plan-pruebas.md`.
