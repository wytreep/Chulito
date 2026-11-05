# Modelo de amenazas (STRIDE)

**Chulito — confirmación compartida de pagos y libro diario para negocios pequeños**

> **BORRADOR (v0.1).** Modelo de amenazas de **diseño**: el backend de producción (TBD-9) todavía no existe. No sustituye una revisión de seguridad ni una prueba de penetración. Los riesgos son cualitativos y deben revisarse cuando haya arquitectura implementada.

| Campo | Valor |
|---|---|
| Versión | 0.1 (borrador) |
| Fecha | 4 de noviembre de 2026 |
| Estado | Borrador — sin revisión de seguridad externa |
| Alcance | MVP en diseño: captura de comprobantes, conciliación y libro diario |
| Fuera de alcance | Infraestructura del proveedor de nube, aplicación bancaria del usuario, dispositivos personales |

## 1. Supuestos

- El MVP recibe comprobantes por **reenvío de correo** o **carga manual**; no lee la banca del usuario ni pide credenciales bancarias.
- No se almacenan números completos de tarjeta ni claves bancarias.
- Los datos de prueba son sintéticos; no hay datos reales en el repositorio.
- El producto es **multi-negocio**: varias cuentas comparten la misma infraestructura.
- La verificación contra el banco emisor no está definida; el estado del pago se apoya en el comprobante y en reglas de conciliación.

## 2. Activos

| Activo | Por qué importa | Sensibilidad |
|---|---|---|
| Credenciales y sesiones | Dan acceso a todos los datos del negocio | Alta |
| Comprobantes y sus adjuntos | Contienen montos, referencias y datos de pagadores | Alta |
| Libro diario y conciliaciones | Son la fuente de verdad contable del negocio | Alta |
| Configuración de captura | Alias de reenvío, remitentes autorizados, reglas | Alta |
| Registros de auditoría | Prueban quién hizo qué | Alta |
| Tokens de integración | Acceso programático a la cuenta | Alta |
| Metadatos técnicos | IP, dispositivo, horarios, patrones de uso | Media |
| Reputación y disponibilidad | Afectan la confianza y el costo operativo | Media |

## 3. Actores y superficies de ataque

| Actor | Motivación | Superficie |
|---|---|---|
| Atacante externo | Fraude, robo de datos, extorsión | API web, correo de reenvío, adjuntos, autenticación |
| Persona usuaria maliciosa | Alterar montos, borrar deudas, espiar a otro negocio | API, cargas de archivos, consultas |
| Pagador | Disputar un pago o suplantar a otro | Comprobantes, referencias |
| Personal interno | Acceso indebido o error | Panel administrativo, base de datos, soporte |
| Proveedor o encargado | Fuga o indisponibilidad | Nube, correo, analítica |
| Contenido no confiable | Inyección, archivos maliciosos | Cuerpo del correo, PDF, imágenes, nombres de archivo |

## 4. Análisis STRIDE

Escala: probabilidad e impacto Alto / Medio / Bajo. El riesgo mostrado es el **residual** después de aplicar la mitigación propuesta.

### 4.1 Spoofing (suplantación)

| ID | Amenaza | Escenario | Mitigación | Riesgo |
|---|---|---|---|---|
| S-01 | Toma de cuenta | Credential stuffing o contraseña reutilizada | Verificación de correo, política de contraseñas, bloqueo progresivo, MFA opcional, detección de credenciales filtradas | Medio |
| S-02 | Suplantación del canal de reenvío | Un tercero conoce el alias y envía comprobantes falsos | Alias largo y no adivinable, rotación, remitentes autorizados, validación SPF/DKIM/DMARC y marcar lo no verificado | Alto |
| S-03 | Robo de sesión o token | XSS, dispositivo compartido o token en el navegador | Cookies HttpOnly, Secure y SameSite, rotación de tokens, cierre por inactividad, revocación por dispositivo | Medio |
| S-04 | Suplantación de soporte | Phishing que pide contraseña o código | Canal oficial único, nunca pedir secretos, avisos en la aplicación | Medio |
| S-05 | Suplantación de administrador | Cuenta interna compartida o sin MFA | Cuentas nominales, MFA obligatorio, mínimo privilegio | Alto |

### 4.2 Tampering (manipulación)

| ID | Amenaza | Escenario | Mitigación | Riesgo |
|---|---|---|---|---|
| T-01 | Comprobante alterado | Se edita el monto o la referencia antes de reenviarlo | Hash del original, extracción desde el adjunto, contraste de campos, marcar como dudoso cuando no cuadra | Alto |
| T-02 | Reutilización de un comprobante | Se reenvía el mismo pago para simular un segundo abono | Deduplicación por hash, emisor, referencia, monto y fecha; ventana temporal; registro de intentos | Alto |
| T-03 | Alteración del libro diario | Se edita o borra un asiento para ocultar un faltante | Libro append-only, correcciones por reversa, encadenamiento de hashes | Alto |
| T-04 | Alteración de registros de auditoría | Se borran huellas de una acción | Almacenamiento separado, append-only, sellado periódico y alertas | Medio |
| T-05 | Cambio de configuración de captura | Se añade un remitente o se cambia el alias | Doble confirmación, notificación al titular y historial de cambios | Medio |
| T-06 | Inyección en la extracción | El texto del comprobante intenta alterar el parser o el modelo | Tratar el contenido como datos, esquema de salida estricto, sin herramientas, límites de tamaño | Alto |

### 4.3 Repudiation (repudio)

| ID | Amenaza | Escenario | Mitigación | Riesgo |
|---|---|---|---|---|
| R-01 | El negocio niega un registro | Dice que no creó un cobro o no confirmó un pago | Registro con usuario, IP, fecha y hash; confirmaciones explícitas; auditoría | Medio |
| R-02 | El operador niega un acceso | Consultó datos sin justificación | Auditoría de accesos sensibles, mínimo privilegio, acceso de emergencia registrado | Medio |
| R-03 | El pagador niega el pago | Disputa la operación | Chulito no certifica el pago: muestra la evidencia y su estado; el negocio conserva el original | Medio |

### 4.4 Information disclosure (divulgación)

| ID | Amenaza | Escenario | Mitigación | Riesgo |
|---|---|---|---|---|
| I-01 | Fuga entre negocios | Un usuario consulta recursos de otro cambiando el identificador | Identificador de negocio obligatorio en cada consulta, autorización por recurso, pruebas de aislamiento | Alto |
| I-02 | Comprobantes expuestos | Enlaces públicos o almacenamiento mal configurado | Almacenamiento privado, enlaces firmados de corta vida, cifrado | Alto |
| I-03 | Datos personales en registros | Se guarda el cuerpo del correo o el comprobante completo en logs | Enmascaramiento, no registrar contenido, retención corta | Medio |
| I-04 | Fuga por copias de respaldo | Respaldo accesible o sin cifrar | Cifrado, acceso restringido y pruebas de restauración | Medio |
| I-05 | Exfiltración con cuenta comprometida | Descarga masiva de comprobantes | Detección de volumen anómalo, límites y alertas | Medio |
| I-06 | Enumeración | Se prueban correos o referencias para descubrir cuentas | Respuestas uniformes, límites de tasa | Bajo |

### 4.5 Denial of service (denegación)

| ID | Amenaza | Escenario | Mitigación | Riesgo |
|---|---|---|---|---|
| D-01 | Inundación de la bandeja | Correo basura al alias del negocio | Remitentes autorizados, cuotas por negocio, deduplicación temprana, cola con contrapresión | Medio |
| D-02 | Archivos abusivos | Adjuntos enormes o maliciosos | Límite de tamaño y tipo, antivirus, sandbox, cuotas | Medio |
| D-03 | Ataque a la API | Fuerza bruta o ráfagas | Límites de tasa, WAF, bloqueo adaptativo | Medio |
| D-04 | Costo por procesamiento | Extracción costosa repetida | Presupuesto por negocio, caché, degradación controlada | Medio |

### 4.6 Elevation of privilege (elevación)

| ID | Amenaza | Escenario | Mitigación | Riesgo |
|---|---|---|---|---|
| E-01 | Escalada a administrador | El cliente manipula roles o rutas | Autorización en el servidor, roles verificados, pruebas negativas | Alto |
| E-02 | Acceso de soporte sin control | Un agente ve datos de cualquier negocio | Roles separados, aprobación, registro y ventana temporal | Medio |
| E-03 | SSRF | El procesamiento sigue enlaces internos | No seguir enlaces externos, lista permitida, sandbox, bloquear metadatos del proveedor | Medio |
| E-04 | Ejecución por archivo malicioso | Parser vulnerable o macro | Sandbox, contenedor sin privilegios, antivirus, dependencias al día | Medio |

## 5. Amenazas propias del dominio

| ID | Amenaza | Por qué es crítica en Chulito | Mitigación |
|---|---|---|---|
| C-01 | Comprobante de otro negocio | Un usuario reenvía el comprobante de un tercero y lo concilia como propio | Validar destino del pago, marcar discrepancia y no conciliar automáticamente |
| C-02 | Pago ya conciliado en otro periodo | Se reintenta el mismo comprobante meses después | Deduplicación global por hash, emisor, referencia y monto |
| C-03 | Monto del texto distinto al del adjunto | El texto del correo dice una cifra y el PDF otra | Extraer del adjunto, comparar ambas fuentes y marcar dudoso |
| C-04 | Suplantación del nombre del pagador | El nombre no prueba la identidad | No usar el nombre como evidencia; usar referencia, monto, fecha y emisor |
| C-05 | Dependencia del correo | Si el canal se compromete, se compromete la captura | Segundo canal de verificación, alertas y revisión manual de casos dudosos |

## 6. Controles por capa

| Capa | Controles mínimos |
|---|---|
| Transporte | TLS, HSTS, certificados válidos, sin protocolos obsoletos |
| Identidad | Contraseñas robustas, MFA opcional (obligatoria para administración), recuperación segura, revocación de sesiones |
| Aplicación | Validación de entrada, autorización por recurso, CSRF, CSP, cabeceras seguras |
| Datos | Cifrado en tránsito y reposo, minimización, seudonimización, retención definida |
| Comprobantes | Sandbox, hash del original, deduplicación, esquema estricto de extracción |
| Operación | Auditoría inmutable, alertas, copias cifradas, gestión de secretos, parcheo |
| Proveedores | Contratos, revisión de seguridad y país de alojamiento documentado |

## 7. Requisitos de seguridad derivados

1. Toda consulta debe filtrar por el negocio autenticado; nunca por un identificador del cliente sin verificación.
2. Toda acción sensible debe quedar en un registro de auditoría append-only con usuario, fecha y resultado.
3. Todo comprobante debe deduplicarse antes de conciliar.
4. El correo recibido debe validarse con SPF, DKIM y DMARC cuando el emisor lo publique, y marcarse cuando no se pueda verificar.
5. El alias de reenvío debe ser largo, no adivinable y rotable por el usuario.
6. Debe haber límites de tasa y cuotas por negocio en API, cargas y procesamiento.
7. Los archivos deben procesarse en un entorno aislado y con antivirus.
8. Los datos deben cifrarse en tránsito y en reposo.
9. Los registros no deben contener cuerpos de correo ni comprobantes completos.
10. Debe detectarse el acceso o la descarga anómala y alertarse.
11. Las sesiones deben poder revocarse por dispositivo.
12. Las copias de respaldo deben estar cifradas y probarse con restauraciones periódicas.
13. Debe revisarse la superficie de dependencias en cada entrega.
14. Los cambios de configuración de captura deben quedar auditados y notificarse al titular.

## 8. Riesgos aceptados y límites

- **Verificación bancaria:** el MVP no confirma el pago contra el banco emisor; el estado se basa en el comprobante y en las reglas de conciliación. Esto debe explicarse en el producto y en los términos.
- **Identidad del pagador:** Chulito no certifica quién pagó; solo registra la evidencia disponible.
- **Canal de correo:** es el punto más débil de la captura. Requiere validación de remitente y revisión de casos dudosos.
- **Sin backend de producción:** este modelo describe el diseño; debe repetirse sobre la arquitectura real (TBD-9).
- **Trazabilidad al SRS:** las amenazas aún no están vinculadas a identificadores `SRS-NFR-xx`; esa trazabilidad queda pendiente.

## 9. Pruebas sugeridas

- Aislamiento entre dos negocios con identificadores cruzados.
- Reenvío duplicado del mismo comprobante y de un comprobante ya conciliado.
- Comprobante con monto alterado en el texto y en el adjunto.
- Envío desde un remitente no autorizado y desde un alias filtrado.
- Carga de archivos grandes, corruptos y con contenido malicioso.
- Inyección de instrucciones en el texto del comprobante.
- Límites de tasa y cuotas por negocio.
- Restauración de una copia de respaldo.
- Revisión de dependencias y de configuración de almacenamiento.

## 10. Estado y próximos pasos

- **Estado:** borrador de diseño, sin revisión de seguridad externa.
- **Próximo paso:** repetir el modelo sobre la arquitectura del backend (TBD-9) y trazar cada mitigación a un requisito del SRS.
- **Dependencia:** la revisión legal (TBD-6) y este modelo deben leerse juntos: varias amenazas son también obligaciones de la Ley 1581 de 2012.
