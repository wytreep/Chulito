# Plan de pruebas

**Chulito — confirmación compartida de pagos y libro diario para negocios pequeños**

> **BORRADOR (v0.1).** Plan de pruebas de la **Fase 0 (diseño)**. No se ha ejecutado ninguna prueba de este plan: el backend de producción no existe (TBD-9) y la captura real sigue pendiente (TBD-1). Los resultados que se registren en el futuro deben indicar versión, entorno, fixtures y fecha.

| Campo | Valor |
|---|---|
| Versión | 0.1 (borrador) |
| Fecha | 4 de noviembre de 2026 |
| Estado | Borrador — pendiente de revisión |
| Documento fuente | SRS v0.4 (CNF-SRS-001) |
| Historias | `02-requisitos/historias-usuario/historias-usuario.md` |
| Seguridad | `06-seguridad-privacidad/modelo-amenazas-stride.md` |
| Alcance | MVP en diseño; sin canal real ni datos reales |

## 1. Propósito

Definir **qué se prueba, cómo se prueba y con qué evidencia se acepta** cada requisito del SRS v0.4, de forma que:

1. cada `SRS-F-xx`, `SRS-NFR-xx` y `SRS-RN-xx` tenga al menos un caso de prueba asociado;
2. las mitigaciones del modelo STRIDE tengan una prueba de seguridad verificable;
3. la definición de terminado sea objetiva y no dependa de una impresión.

## 2. Alcance

**Incluye:** cuentas y roles, aislamiento multi-tenant, captura y normalización, idempotencia, emparejamiento, estados del cobro, libro diario, auditoría, consentimiento, exportación, requisitos no funcionales y pruebas derivadas de STRIDE.

**No incluye:**

- pruebas con bancos o billeteras reales (TBD-1, TBD-2);
- pruebas de penetración externas;
- certificación de cumplimiento legal (TBD-6);
- rendimiento con volúmenes de producción (no hay línea base);
- aplicación móvil nativa (no existe).

## 3. Referencias

| Documento | Uso |
|---|---|
| SRS v0.4 | Requisitos, criterios de aceptación y transiciones T-01…T-08 |
| PRD v0.4 | Trazabilidad de producto |
| `historias-usuario.md` | Criterios por historia |
| `modelo-amenazas-stride.md` | Amenazas y mitigaciones |
| `06-seguridad-privacidad/` | Política de datos, cookies y términos |
| ADR-0001 | Stack previsto (NestJS/TypeScript) y toolchain |
| Prototipo Python | Especificación ejecutable, **no** producción |

## 4. Estrategia

### 4.1 Niveles

| Nivel | Qué verifica | Herramienta prevista | Cuándo |
|---|---|---|---|
| Unitario | Parsers, reglas de emparejamiento, cálculos, validaciones | Vitest (stack objetivo) / `unittest` (prototipo) | Cada cambio |
| Integración | API, base de datos, colas, auditoría, aislamiento | Vitest + contenedores | Cada integración |
| Contrato | OpenAPI 3.1, códigos de error de canal | Esquema + pruebas de contrato | Cada cambio de API |
| Extremo a extremo | Registro → cobro → pago → libro | Playwright (propuesta) | Antes de cada entrega |
| No funcional | Latencia, capacidad, recuperación, seguridad | k6 o equivalente (propuesta) | Por hito |
| Manual | Usabilidad, textos legales, accesibilidad | Guion de revisión | Antes de piloto |

### 4.2 Pirámide

- **Base:** unitarias de parsers y reglas (rápidas, deterministas, sin red).
- **Medio:** integración de pipeline, aislamiento y auditoría.
- **Cima:** pocas pruebas E2E de los flujos US-01, US-03, US-04 y US-06.

### 4.3 Datos de prueba

1. **Solo sintéticos.** Nunca datos reales de personas, bancos ni negocios.
2. **Fixtures de comprobantes** con montos, referencias y fechas inventadas, versionados en el repositorio de código (sin PII).
3. **Dos tenants** (A y B) con usuarios de cada rol para probar aislamiento.
4. **Reloj controlado** para ventanas de emparejamiento, `occurred_at`, `received_at` y cierre diario en `America/Bogota`.
5. **Adaptador simulado** que pueda: entregar, duplicar, retrasar, perder y caerse.

## 5. Entornos

| Entorno | Uso | Datos | Estado |
|---|---|---|---|
| Local | Unitarias e integración | Sintéticos | Disponible para el prototipo Python |
| CI | Verificación automática | Sintéticos | Previsto en ADR-0001 |
| Staging | E2E y NFR | Sintéticos | **No existe** (TBD-9) |
| Piloto | Validación controlada | Reales, con autorización | **No habilitado** (TBD-1, TBD-6, TBD-7) |

## 6. Casos funcionales

| ID | Caso | Resultado esperado | Nivel |
|---|---|---|---|
| TP-F-01 | Registrar negocio y dueño con datos válidos | Se crea tenant y cuenta; el dueño inicia sesión | E2E |
| TP-F-02 | Sesión inactiva supera el tiempo configurado | La sesión se cierra y exige autenticación | Integración |
| TP-F-03 | Dueño crea, lista y revoca cajero | El cajero queda creado y, al revocar, sus solicitudes posteriores se rechazan | Integración |
| TP-F-04 | Cajero intenta ver configuración, credenciales o consentimientos | Se rechaza y no se filtra información | Integración |
| TP-F-05 | Cajero de A solicita pagos, auditoría y exportación de B | Se rechaza sin revelar si B existe | Integración |
| TP-F-10 | Habilitar captura sin consentimiento vigente | La captura no se activa y se explica el motivo | Integración |
| TP-F-11 | Captura con consentimiento y adaptador caído | Estado **degradado**, intentos y error registrados; no se crea pago | Integración |
| TP-F-12 | Mensaje de emisor identificable y mensaje desconocido | El primero va a su parser; el segundo se conserva como **no reconocido** | Unitario |
| TP-F-13 | Normalizar monto, fecha, emisor, referencia y tipo | Campos normalizados; `occurred_at` y `received_at` separados | Unitario |
| TP-F-14 | Reenviar el mismo mensaje con igual huella | Un solo pago y un solo registro; la repetición queda trazada | Integración |
| TP-F-15 | Mensaje sin parser reconocible | Se conserva, se avisa si hay consentimiento y **no** se crea pago | Integración |
| TP-F-16 | Señal de pérdida o retraso del canal | Brecha potencial por tenant/canal; sin pago sintético | Integración |
| TP-F-20 | Pago llega con la vista del cajero abierta | Aparece en vivo con estado correcto y sin duplicar | E2E |
| TP-F-21 | Registrar cobro con monto 0 o negativo | Se rechaza con mensaje claro; no crea cobro | Unitario |
| TP-F-22 | Cobro de 25.000 COP y pago compatible dentro de la ventana | Pasa a **Confirmado**; trazas correlacionadas | Integración |
| TP-F-23 | Recorrer los cuatro estados del cobro | Solo se permiten las transiciones T-01…T-08 | Integración |
| TP-F-24 | Cobro 25.000 COP y pago 2.500 COP dentro de ventana | Pago **Dudoso**, cobro **Pendiente** | Integración |
| TP-F-25 | Dueño resuelve un dudoso | Pasa a **Confirmado**, se audita y el pago original no cambia | Integración |
| TP-F-30 | Libro diario con pagos de dos emisores | Agrupa por negocio y fecha; separa `occurred_at` y `received_at` | Integración |
| TP-F-31 | Cierre del día con diferencias | Totales por emisor y cajero; diferencias correctas en `America/Bogota` | Integración |
| TP-F-32 | Dueño exporta CSV y JSON con filtros | Solo datos de su tenant, con auditoría | Integración |
| TP-F-40 | Ejecutar altas/bajas de cajeros, resoluciones, consentimientos y exportaciones | Cada acción genera evento de auditoría inmutable | Integración |
| TP-F-41 | Dueño solicita eliminación de datos | Se audita alcance, resultado y límites de respaldo | Integración |

## 7. Casos de requisitos no funcionales

| ID | Caso | Resultado esperado | Nivel |
|---|---|---|---|
| TP-NFR-01 | Medir 200 eventos elegibles en 3 sesiones | p95 ≤ 10 s de `received_at` a render; reporte por canal y emisor con p50, p95, p99, n y exclusiones | NFR |
| TP-NFR-02 | Carga de 20 negocios y 50 notificaciones/min | No degrada TP-NFR-01; sin pérdida ni duplicados | NFR |
| TP-NFR-03 | Medir disponibilidad mensual en piloto | Se reporta el valor observado; **no** se declara cumplimiento contractual | Operación |
| TP-NFR-04 | Caída y recuperación de un componente | Reanuda desde almacenamiento duradero, deduplica por huella y no pierde ni duplica | Integración |
| TP-NFR-05 | Revisar autenticación, TLS, secretos y hashing | Argon2id, TLS en todo el tráfico, secretos fuera del repositorio, subconjunto ASVS L2 | Seguridad |
| TP-NFR-06 | Suite automática de aislamiento | Ningún negocio accede a datos de otro, incluidos mensajes, consentimientos y auditoría | Integración |
| TP-NFR-07 | Revisar minimización, cifrado y retención | Solo campos necesarios; original cifrado; retención según TBD-4 | Inspección |
| TP-NFR-08 | Superar límites de tasa en API y recepción | Se bloquea o encola según política, sin afectar a otros tenants | NFR |
| TP-NFR-09 | Medir cobertura de cada parser | Cada parser es módulo independiente con ≥ 80 % de cobertura | Unitario |
| TP-NFR-10 | Cajero confirma un cobro en celular | Máximo 3 interacciones; interfaz en español y usable | Manual |
| TP-NFR-11 | Revisar logs, métricas y trazas | Sin datos sensibles, con correlación, salud, canal, reintentos y brechas | Inspección |
| TP-NFR-12 | Despliegue reproducible en contenedor | Versiones fijadas según ADR-0001 | Integración |
| TP-NFR-13 | Revisar el supuesto regulatorio | Dictamen legal documentado; sin afirmar cumplimiento | Inspección |

## 8. Casos derivados de STRIDE

| ID | Amenaza | Caso | Resultado esperado |
|---|---|---|---|
| TP-SEC-01 | S-01 toma de cuenta | Credential stuffing y bloqueo progresivo | Bloqueo y alerta; no revela si la cuenta existe |
| TP-SEC-02 | S-03 robo de sesión | Revisar cookies `HttpOnly`, `Secure`, `SameSite`, CSRF y revocación | Sesión protegida y revocable por dispositivo |
| TP-SEC-03 | T-01/T-02 comprobante alterado o reutilizado | Alterar monto y reenviar el mismo comprobante | Se marca dudoso o se deduplica; no se concilia dos veces |
| TP-SEC-04 | T-06 inyección en la extracción | Texto del comprobante con instrucciones o JSON malformado | Se trata como dato; esquema estricto; no ejecuta acciones |
| TP-SEC-05 | D-02/E-04 archivo malicioso | PDF corrupto, macro o archivo sobredimensionado | Se rechaza o aísla; no afecta el servicio |
| TP-SEC-06 | E-03 SSRF | Comprobante con enlaces internos o metadatos del proveedor | No se siguen enlaces; se bloquea el destino |
| TP-SEC-07 | I-03 datos en logs | Buscar PII en logs y trazas | Sin cuerpos de correo ni comprobantes completos |
| TP-SEC-08 | I-01 fuga entre negocios | Cambiar identificadores en la URL y el cuerpo | Rechazo sin filtrar existencia |
| TP-SEC-09 | D-01/D-03 inundación | Ráfaga de correos y llamadas a la API | Cuotas y límites activos; servicio estable |
| TP-SEC-10 | I-05 exfiltración | Descarga masiva con una cuenta comprometida | Detección de volumen anómalo y alerta |

## 9. Matriz de trazabilidad

| Requisito | Casos |
|---|---|
| SRS-F-01 | TP-F-01 |
| SRS-F-02 | TP-F-02, TP-SEC-02 |
| SRS-F-03 | TP-F-03 |
| SRS-F-04 | TP-F-04 |
| SRS-F-05 | TP-F-05, TP-NFR-06, TP-SEC-08 |
| SRS-F-10 | TP-F-10, TP-F-11 |
| SRS-F-11 | TP-F-12 |
| SRS-F-12 | TP-F-13 |
| SRS-F-13 | TP-F-14 |
| SRS-F-14 | TP-F-15 |
| SRS-F-15 | TP-F-16, TP-SEC-09 |
| SRS-F-20 | TP-F-20 |
| SRS-F-21 | TP-F-21 |
| SRS-F-22 | TP-F-22 |
| SRS-F-23 | TP-F-23 |
| SRS-F-24 | TP-F-24, TP-SEC-03 |
| SRS-F-25 | TP-F-25 |
| SRS-F-30 | TP-F-30 |
| SRS-F-31 | TP-F-31 |
| SRS-F-32 | TP-F-32 |
| SRS-F-40 | TP-F-40 |
| SRS-F-41 | TP-F-41 |
| SRS-NFR-01 | TP-NFR-01 |
| SRS-NFR-02 | TP-NFR-02 |
| SRS-NFR-03 | TP-NFR-03 |
| SRS-NFR-04 | TP-NFR-04, TP-F-14 |
| SRS-NFR-05 | TP-NFR-05, TP-SEC-01, TP-SEC-02 |
| SRS-NFR-06 | TP-NFR-06, TP-F-05 |
| SRS-NFR-07 | TP-NFR-07, TP-SEC-07 |
| SRS-NFR-08 | TP-NFR-08, TP-SEC-09 |
| SRS-NFR-09 | TP-NFR-09 |
| SRS-NFR-10 | TP-NFR-10 |
| SRS-NFR-11 | TP-NFR-11 |
| SRS-NFR-12 | TP-NFR-12 |
| SRS-NFR-13 | TP-NFR-13 |
| SRS-RN-01 | TP-F-30, TP-F-31, TP-F-05 |
| SRS-RN-02 | TP-F-22, TP-F-23 |
| SRS-RN-03 | TP-F-22, TP-F-24 |
| SRS-RN-04 | TP-F-25, TP-F-40 |
| SRS-RN-05 | TP-F-04 |
| SRS-RN-06 | TP-F-31 |

## 10. Evidencia y gestión de defectos

1. Cada ejecución registra: fecha, entorno, versión del código y del parser, fixtures usados, resultado y responsable.
2. Los resultados se guardan como evidencia en `07-calidad-pruebas/evidencia/` (texto o enlace; los binarios van fuera del repositorio).
3. Un defecto se clasifica por severidad:

| Severidad | Criterio | Efecto |
|---|---|---|
| Crítica | Pérdida o duplicación de pagos, fuga entre negocios, ejecución remota | Bloquea la entrega |
| Alta | Estado incorrecto, consentimiento no respetado, auditoría ausente | Bloquea el hito |
| Media | Error de cálculo con corrección manual, mensaje confuso | Se corrige en el hito |
| Baja | Texto, formato o mejora menor | Se planifica |

4. Ningún defecto crítico o alto puede quedar abierto para declarar un hito terminado.

## 11. Criterios de salida

### 11.1 Fase 0 (diseño)

- Todos los requisitos del SRS tienen al menos un caso asociado.
- Las historias US-01…US-08 tienen criterios verificables.
- El modelo STRIDE tiene pruebas de seguridad propuestas.
- **No se exige ejecución:** el código de producción no existe.

### 11.2 MVP

- 100 % de los casos de prioridad Alta ejecutados.
- ≥ 95 % en verde; el resto con defecto clasificado y aceptado.
- 0 defectos críticos o altos abiertos.
- TP-NFR-01 ejecutado con la muestra mínima o con una desviación documentada.
- TP-NFR-06 (aislamiento) al 100 %.
- Auditoría verificada en todos los flujos sensibles.

### 11.3 Piloto

- Casos de prioridad Alta y Media ejecutados.
- Pruebas con fixtures autorizados y anonimizados (TBD-2).
- Revisión legal de textos y retención (TBD-6).
- Plan de respuesta a incidentes probado.

## 12. Definición de terminado por fase

| Fase | Se considera terminada cuando |
|---|---|
| Requisitos | SRS, historias y criterios están aprobados y trazados |
| Diseño técnico | ADR aprobado y modelo STRIDE revisado sobre la arquitectura |
| Implementación | Casos unitarios e integración en verde en CI |
| Entrega | Casos E2E y NFR en verde; evidencia registrada |
| Piloto | Criterios de salida de piloto cumplidos y revisión legal cerrada |

## 13. Riesgos y bloqueos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Sin canal real (TBD-1) | No se puede validar latencia ni captura real | Adaptador simulado y fixtures; declarar límite |
| Sin muestras de emisores (TBD-2) | Parsers no representativos | Fixtures sintéticos y revisión al obtener muestras |
| Sin backend (TBD-9) | No hay E2E ni NFR ejecutables | Probar el prototipo Python y el harness; no presentarlos como producción |
| Ventana de 10 min provisional (TBD-3) | Casos de borde mal calibrados | Parametrizar la ventana |
| Retención sin aprobar (TBD-4) | Pruebas de borrado sin base legal | Marcar como propuesta |
| Revisión legal pendiente (TBD-6) | Textos y consentimiento sin validar | No ejecutar con datos reales |

## 14. Control de cambios

Toda modificación de este plan incrementa la versión y se registra en `CHANGELOG.md`. Los resultados de ejecución no se escriben aquí: van en `evidencia/` con su propia fecha y versión.
