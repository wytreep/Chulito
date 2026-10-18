# CONFIRMA — Síntesis documental y supuestos de trabajo

**Consolidación documental de visión, requisitos, supuestos y decisiones pendientes · Fase 0**

| Campo | Valor |
|---|---|
| Código | CNF-SD-001 |
| Versión | SD-0.3 |
| Fecha | 17 de octubre de 2026 |
| Estado | Borrador revisado; S-0.1 es un escenario simulado, no evidencia de campo |
| Proyecto | Chulito (nombre provisional) |
| Documentos base | PRD v0.3; SRS v0.3; Guía de entrevistas v0.1; S-0.1 (escenario simulado) |
| Uso | Interno — borrador de trabajo |

> **S-0.1 es un escenario simulado, no resultados de entrevistas realizadas.** Sus cifras son ficticias; no constituyen evidencia de campo ni validan segmento, problema, preferencias o alcance del MVP.

> **ADVERTENCIA DE EVIDENCIA — S-0.1 es un escenario simulado, no resultados de entrevistas realizadas.** Sus cifras y perfiles son ficticios; no representan participantes reales ni evidencia de mercado.

> **Recomendación ejecutiva.** Usar S-0.1 únicamente como supuesto de trabajo para explorar una dirección de diseño, no como validación de segmento o alcance. La hipótesis a validar es que un negocio pequeño con empleados necesita confirmar pagos sin exponer la cuenta del dueño y cuadrar varios emisores. Mantener como dirección provisional la confirmación compartida y el libro diario, con fraude como posible función secundaria. Puede continuar el prototipo técnico con eventos sintéticos; las decisiones de producto requieren evidencia real antes de baselinar el MVP o iniciar un piloto.

> **Límite decisional.** Los valores ficticios de S-0.1 no son entrevistas, no se presentan como evidencia ni se extrapolan como estimación de mercado o métricas de uso. Solo sirven para ensayar análisis y orientar preguntas de investigación; el responsable puede reemplazar o corregir las hipótesis.

> **Alcance de la síntesis.** Conserva trazabilidad al escenario simulado S-0.1 y lo trata como supuesto de trabajo explícito. No sustituye investigación de campo ni reemplaza el PRD o el SRS.

<!-- PAGEBREAK -->

## Control y resumen ejecutivo

S-0.1 es un **escenario simulado, no resultados de entrevistas realizadas**. Describe 16 registros ficticios (cinco tiendas de barrio, cuatro negocios de comida/domicilios, cuatro vendedores por redes y tres cajeros/empleados); sus proporciones —por ejemplo, 14/16, 9/16, 8/16, 10/16 y 11/16— son valores inventados para ejercitar el análisis, no observaciones empíricas. No se afirma que se haya entrevistado a personas o negocios. En esta revisión, estos datos solo generan hipótesis de producto que deben contrastarse con investigación real.

La interpretación del escenario propone **como hipótesis**, no como decisión validada, explorar un negocio pequeño con empleados y varios emisores, con confirmación compartida para el cajero y libro diario multiemisor. También plantea evaluar la detección de pantallazos como función secundaria y una vía de captura controlada por el usuario. El segmento, la prioridad del problema y el alcance del MVP siguen sin evidencia real y deben contrastarse antes de aprobar decisiones de producto.

El trabajo técnico acotado puede continuar con datos sintéticos sin esperar entrevistas. Esto no valida decisiones de producto: la selección del segmento y del alcance del MVP sigue pendiente de entrevistas reales. La trazabilidad PRD v0.3–SRS v0.3 ya fue actualizada; antes de captura real siguen siendo puertas el canal autorizado, los emisores iniciales, las muestras utilizables, la política de retención y la revisión legal.

### Decisión recomendada

1. Tratar como hipótesis de diseño —no decisión aprobada— el segmento de negocio pequeño con empleados y varios medios de pago; validar prioridad frente al vendedor individual con investigación real.
2. Evaluar una primera versión centrada en vista del cajero sin acceso a la cuenta del dueño, confirmación del pago recibido y libro diario unificado; validar alcance y prioridad antes de baselinar. El fraude queda como hipótesis de complemento.
3. Comparar captura controlada por el usuario y reenvío de mensajes frente a otras opciones; el escenario simulado no demuestra preferencias reales. Cerrar la opción mediante ADR y revisión de privacidad/plataforma.
4. Avanzar con esquema canónico, idempotencia y flujo de conciliación usando datos sintéticos. La trazabilidad SRS v0.3 ↔ PRD v0.3 fue actualizada; las decisiones de producto no quedan validadas por este trabajo técnico.

**Estado de la información:** S-0.1 es un escenario simulado y sus resultados no son evidencia de campo. Se conserva como supuesto de trabajo provisional para diseñar preguntas y ejemplos; reemplazarlo o actualizarlo con evidencia real.

## Contenido

1. Alcance y método de esta síntesis — p. 3  
2. Base documental y estado de la información — p. 3  
3. Comprensión consolidada del producto — p. 3  
4. Señales de S-0.1 y métricas de producto — p. 4  
5. Convergencia de requisitos y trazabilidad — p. 5  
6. Registro de decisiones pendientes — p. 6  
7. Riesgos y dependencias — p. 7  
8. Plan de avance: supuestos, validación y riesgos técnicos — p. 8  
9. Criterios de preparación y salida — p. 9  
10. Verificaciones realizadas y asuntos pendientes — p. 9  
11. Conclusión — p. 10  
12. Fuentes documentales — p. 10

<!-- PAGEBREAK -->

## 1. Alcance y método de esta síntesis

Esta revisión consolida los documentos del proyecto y trata S-0.1 como escenario simulado y supuesto de trabajo provisional, no como hallazgos de entrevistas. Sus cifras no validan segmento, propuesta de valor ni demanda. Se usan únicamente como material de ejemplo para definir preguntas y avanzar pruebas técnicas sintéticas. No se introduce investigación externa.

El informe mantiene trazabilidad a S-0.1 e identifica sus valores como ficticios. No son resultados de entrevistas, no deben presentarse como preferencias o métricas reales, ni extrapolarse al mercado. Cuando haya evidencia de campo, se registrará por separado y se revisarán las hipótesis y decisiones derivadas.

**Regla de lectura:** “supuesto de trabajo” significa una hipótesis explícita y provisional para orientar experimentos técnicos, no evidencia que confirme una necesidad o preferencia. Los objetivos de producto (por ejemplo, latencia, reducción del tiempo de cuadre o falsos positivos) siguen siendo metas, no resultados observados de Chulito.

## 2. Base documental y estado de la información

| Fuente | Aporte a la síntesis | Estado y uso |
|---|---|---|
| [D1] PRD CNF-PRD-001, v0.3 (12-oct-2026) | Visión, alcance candidato, metas, requisitos, riesgos y decisiones. | Referencia de producto; el propio PRD identifica S-0.1 como escenario de trabajo y requiere contrastar hipótesis con entrevistas reales. |
| [D2] SRS CNF-SRS-001, v0.3 | Requisitos de software, reglas, criterios, interfaces, datos, trazabilidad y TBD. | Borrador derivado del PRD v0.3; trazabilidad actualizada; pendiente de revisión y aprobación. |
| [D3] Guía CNF-GEI-001, v0.1 | Hipótesis H1–H6, preguntas, perfiles, consentimiento y criterios. | Protocolo para validar problema, segmento y alcance con entrevistas reales; estas no bloquean el spike técnico sintético. |
| [D4] Informe CNF-HAL-001-S, S-0.1 | Escenario simulado con 16 registros ficticios y conclusiones ilustrativas. | No son resultados de entrevistas ni evidencia de campo; se conserva solo como supuesto de trabajo para generar hipótesis. |

El escenario no identifica empíricamente un segmento prioritario ni valida consecuencias de producto. Puede orientar hipótesis para un prototipo técnico con datos sintéticos; segmento, alcance y valor siguen pendientes de validación con personas usuarias reales.

## 3. Comprensión consolidada del producto

### 3.1 Hipótesis de propuesta de valor

La hipótesis de valor por validar es que Chulito ayude a un negocio pequeño con empleados a confirmar pagos digitales desde notificaciones del emisor, mostrar el estado al cajero sin exponer la cuenta financiera del dueño y reunir movimientos de varios emisores en un libro diario. El comportamiento propuesto debe distinguir confirmado, pendiente, dudoso y no reconocido; una coincidencia insuficiente no debe convertirse en confirmación automática.

### 3.2 Perfil prioritario y composición de la base

| Perfil ficticio del escenario S-0.1 | n ficticio | Prioridad hipotética (por validar) | Necesidad hipotética |
|---|---:|---|---|
| Tienda de barrio | 5 | Alta si tiene empleados y varios medios | El cajero ve el pago y el dueño puede cuadrar el día. |
| Negocio de comida/domicilios | 4 | Alta si tiene empleados y varios medios | Confirmación rápida durante la fila/entrega y registro diario. |
| Vendedor por redes/emprendedor | 4 | Media | Verificación rápida; no es el foco inicial de MVP. |
| Cajero/empleado | 3 | Rol usuario, no segmento comprador | Consultar la confirmación sin acceder a la cuenta del dueño. |
| **Total de registros ficticios del escenario** | **16** | — | Distribución descrita en S-0.1. |

Dentro del escenario ficticio, 6 de 7 registros del subgrupo describen llamadas al dueño o uso compartido del teléfono. Esto genera una hipótesis para explorar —acceso delegado del cajero con permisos mínimos—, pero no demuestra una práctica observada. La prioridad relativa de perfiles también permanece sin validar.

### 3.3 Problema y alternativas actuales

El escenario simulado propone comparar el cierre manual y la confirmación en caja: incluye registros ficticios sobre uso de varias aplicaciones, duración estimada y comprobantes dudosos. Esas cifras no prueban incidencia, frecuencia ni prioridad del problema. Deben comprobarse con entrevistas reales antes de decidir el enfoque del MVP.

El escenario contiene tres registros ficticios con parlante de pagos y plantea preguntas sobre historial y cuadre multiemisor. La cobertura de alternativas (verificador de Nequi, alertas de Bancolombia, Bre-B y parlantes) requiere investigación independiente y actual antes de decidir integración o posicionamiento.

### 3.4 Límites del MVP

**Hipótesis de alcance a validar:** negocio con empleados; roles dueño/cajero; confirmación del pago desde una fuente controlada; vista de confirmaciones para el cajero; libro diario de los emisores habilitados; conciliación básica; discrepancias para revisión; auditoría.

**Fuera del alcance provisional:** custodiar o mover dinero; sustituir POS/facturación; integraciones bancarias oficiales; aplicación móvil dedicada; reportes semanales/exportación; alertas por patrones sospechosos. Este recorte es una hipótesis de trabajo que requiere validar con investigación y aprobación antes de baselinar el MVP.

## 4. Señales de S-0.1 y métricas de producto

### 4.1 Resultados ficticios del escenario simulado por hipótesis

| ID | Resultado ilustrativo de S-0.1 (16 registros ficticios) | Hipótesis a validar |
|---|---|---|
| H1 — Frecuencia | 14/16 reciben pagos digitales cada semana; la proporción descrita va de 20 % a 60 % de las ventas. | Priorizar un flujo de pago frecuente y varios emisores, sin extrapolar el rango a todo el mercado. |
| H2 — Pantallazos | 9/16 aceptan pantallazos, especialmente en transferencias por número/llave; con QR suelen mirar la notificación. | Confirmar desde la notificación recibida; fraude de pantallazo como función secundaria, no como único valor. |
| H3 — Casos dudosos | 8/16 relatan un caso concreto de comprobante falso o dudoso en los últimos seis meses. | Mantener señalización/revisión, pero centrar el MVP en confirmación compartida y cuadre. |
| H4 — Coste | Montos típicos pequeños y un caso grande; el coste principal descrito es el tiempo y la tensión de verificar mientras hay fila. | Medir tiempo de caja y cierre; no priorizar el valor únicamente por pérdidas monetarias. |
| H5 — Soluciones actuales | 11/16 revisan la app o llaman al dueño; 5/16 consideran suficiente el verificador de Nequi. | Diseñar una vista delegada para el cajero y diferenciar el libro multiemisor de los verificadores existentes. |
| H6 — Prueba/privacidad | 7/16 dicen que probarían un piloto; 11/16 expresan preocupación por dar acceso al correo. | Preferir captura bajo control del usuario y probar primero reenvío selectivo frente a acceso total. |

### 4.2 Otras señales accionables

| Dato ficticio del escenario | Valor ilustrativo de S-0.1 | Hipótesis a contrastar |
|---|---|---|
| Conciliación manual | 10/16 usan varias apps y un cuaderno; 20–40 min por noche según el escenario. | Incluir libro diario y establecer línea base de cuadre. |
| Visibilidad del cajero | 6 de 7 negocios con empleados llaman al dueño o comparten el celular; la alerta llega al dueño. | Rol de cajero de acceso limitado es central al MVP. |
| Parlantes de pago | 3/16 tienen uno; ayuda el aviso, pero no hay historial y no cuadra varios emisores. | Compararlos como alternativa parcial, no como sustituto del libro diario. |
| Segmentación | Tienda/comida con empleados: alta; vendedor por redes: media; vendedor solo presencial y casi todo QR: baja. | Orientar prototipo y piloto al perfil de alta prioridad. |

### 4.3 Metas del PRD/SRS que todavía requieren prueba

| Métrica | Meta candidata | Próxima definición/prueba |
|---|---|---|
| Cobros confirmados por cajero sin llamar al dueño | ≥80 % en piloto. | Definir denominador y capturar uso en la vertical slice/piloto. |
| Tiempo de cuadre | Reducción ≥50 % frente a línea base del negocio. | La referencia de 20–40 min de S-0.1 orienta el caso; medir línea base por negocio antes de afirmar reducción. |
| Falsos positivos | 0 en conjunto de pruebas manipuladas. | Definir casos, etiqueta y protocolo de prueba; no presentarlo como garantía. |
| Latencia | <10 s; el SRS pide 95 % de notificaciones bajo 10 s. | Acordar percentil, inicio/fin, canal y exclusiones. |
| Cobertura de parsers | ≥2 emisores en MVP. | Elegir emisores y obtener muestras autorizadas/anonimizadas. |
| Idempotencia | 0 duplicados al reprocesar. | Probar reintentos y claves de deduplicación con fixtures. |
| Uso piloto | ≥2 negocios con empleados durante una semana. | Acordar participantes, soporte y registro; 7/16 disposición declarada no equivale a uso real. |
| Capacidad y disponibilidad SRS | 20 negocios, 50 notificaciones/min, 99,5 % mensual (no contractual). | Validar carga, medición y objetivos de servicio antes de comprometerlos. |

Los valores de S-0.1 son cifras ficticias del escenario; las metas técnicas/comerciales son objetivos candidatos aún no medidos en un producto operativo. Ninguna categoría constituye evidencia de demanda real.

## 5. Convergencia de requisitos y trazabilidad

### 5.1 Requisitos de producto en lenguaje común y estado de validación

| PRD v0.3 | Resultado candidato | Desarrollo en el SRS v0.3 |
|---|---|---|
| RF-01 | Recibir notificaciones mediante el canal aprobado y normalizar solo campos disponibles. | SRS-F-10–14; SRS-F-15 se traza como derivado de RK2/RK3 en SRS v0.3. |
| RF-02 | Evitar pagos duplicados al reprocesar una notificación. | SRS-F-13 y NFR-04. |
| RF-03 | El cajero consulta el estado del cobro sin acceso a la cuenta financiera del dueño. | SRS-F-20, F-23 y permisos de F-04. |
| RF-04 | Asociar un cobro esperado con un pago recibido. | SRS-F-21, F-22 y regla SRS-RN-03 [HIP/TBD-3]. |
| RF-05 | Mantener el libro diario unificado de los emisores habilitados por negocio. | SRS-F-30, F-31; F-32 (CSV) queda posterior al MVP. |
| RF-06 | Aislar los datos de cada negocio. | Correspondencia más directa: SRS-F-05 y SRS-NFR-06. |
| RF-07 | Crear y revocar cajeros con permisos limitados. | SRS-F-03 y F-04; SRS-F-01/F-02 se registran como derivados de PRD §7.1 en SRS v0.3 y requieren aprobación. |
| RF-08 | Señalar discrepancias para revisión, sin convertirlas en confirmación automática. | SRS-F-24 y F-25. |

La trazabilidad del SRS v0.3 refleja PRD v0.3 y RF-06 como aislamiento de negocios. La matriz establece correspondencias documentales, no evidencia la validez de los requisitos ni de las decisiones de segmento/alcance. Alta de negocio/autenticación, estado de captura, alertas y requisitos técnicos derivados requieren revisión y aprobación antes de baselinar.

### 5.2 Requisitos transversales y decisiones técnicas

El PRD v0.3 define como requisitos de calidad candidatos el aislamiento entre negocios, la minimización y revisión del tratamiento de datos personales (incluida la Ley 1581 de 2012), la recuperación ante fallos sin pérdida/duplicación y la auditoría de acciones sensibles. El SRS los desarrolla mediante cifrado, retención pendiente, TLS, Argon2id, un subconjunto aplicable de OWASP ASVS nivel 2, límites de tasa, registros sin datos sensibles, pruebas de aislamiento y despliegue reproducible.

El SRS también propone REST/OpenAPI 3.1, un canal de tiempo real por definir en ADR, contenedores y dependencias fijadas. Deben conservarse como propuestas técnicas sujetas a decisión; no todos son requisitos de producto aprobados. La referencia del SRS a que el servicio estaría fuera de regulación de pagos por no custodiar ni mover dinero es un supuesto por revisar: no tratarlo como conclusión legal. La revisión jurídica prevista en TBD-6 debe preceder al piloto con datos reales.

## 6. Registro de decisiones pendientes

| Prioridad | Decisión o vacío | Qué bloquea | Salida necesaria |
|---|---|---|---|
| P0 — Validación de producto | Segmento y alcance del MVP (incluida prioridad entre cajero, libro diario y fraude). S-0.1 es simulado; no hay evidencia de entrevistas. | Posicionamiento, historias y orden del backlog aprobados. | Entrevistas reales con perfiles definidos, síntesis trazable y actualización/aprobación del PRD; no baselinar alcance con S-0.1. |
| P0 | Canal de captura (PRD Q1 / SRS TBD-1): reenvío selectivo, listener Android u otra opción controlada. S-0.1 no demuestra preferencias reales. | Arquitectura de ingestión, permisos, retención y confianza. | Spike comparativo + ADR; comparar alternativas sin priorizar por los datos simulados y sin dar por resuelto soporte/plataforma. |
| P0 técnico | Compatibilidad de versiones Node.js, TypeScript y NestJS para ADR-0001. ST-01 cubre canales, no compatibilidad del stack. | Fijación de versiones, toolchain, CI y dependencias. | Ejecutar spike de compatibilidad, registrar versiones probadas y aprobar ADR-0001. |
| P1 técnico | Portar la vertical slice Python a TypeScript/NestJS. El prototipo Python es especificación ejecutable, no código de producción. | Validación dentro del stack objetivo. | Traducir contrato/reglas/pruebas a TypeScript y mantener fixtures sintéticos; no promover Python a backend productivo. |
| P0 | Emisores del MVP (Q2 / TBD-2). Alternativas nombradas: Nequi, alertas Bancolombia, Bre-B, parlantes. | Parsers y cobertura real. | Validar uso/prioridad con usuarios reales; seleccionar un conjunto acotado según viabilidad y muestras autorizadas. |
| P0 | Flujo de conciliación (Q3 / TBD-3): monto, hora, referencia, ventana y estados. | Confirmación errónea, falsos positivos y casos dudosos. | Tabla de reglas/escenarios; confirmar si los 10 minutos por defecto aplican. |
| Completado documental, aprobación pendiente | Reconciliación inicial PRD v0.3 ↔ SRS v0.3. | Aprobación de requisitos y eventual baselining. | Revisión del responsable; la trazabilidad no valida las hipótesis de producto. |
| P0 | Retención/eliminación (SRS TBD-4), aplicabilidad legal (TBD-6/NFR-13) y privacidad. | Uso de datos reales y piloto. | Revisar minimización, acceso, borrado, auditoría y aspectos legales en Colombia antes de captura real. |
| P1 | Catálogo de permisos dueño/cajero (RF-07). | RBAC y pruebas de aislamiento. | Matriz rol × acción; revocación, sesiones y datos visibles. |
| P1 | Muestras para parsers (PRD R3 / SRS A3). | Declarar soporte efectivo de emisores. | Validar emisores prioritarios con usuarios reales y obtener muestras autorizadas/anónimas antes de integración real. |
| P2 | Canal de alertas al dueño (SRS TBD-5). | Gestión de mensajes no reconocidos/errores. | Definir canal; se puede simular en el prototipo. |
| P2 | Precio/modelo de uso (PRD Q4). | Alcance comercial del piloto. | Posponer hasta medir adopción y valor de la propuesta priorizada. |
| P0 producto / no bloquea spike técnico | Entrevistas reales y validación de segmento/alcance. | Decisiones de producto, MVP y piloto; no bloquea ejecutar pruebas técnicas con datos sintéticos. | Actualizar la guía, reclutar perfiles relevantes, documentar consentimiento y evidencia; revisar PRD antes de aprobar el MVP. |

## 7. Riesgos y dependencias

| Riesgo | Nivel de atención | Mitigación para avanzar ahora |
|---|---|---|
| S-0.1 presenta n=16 registros ficticios; no es muestra de conveniencia ni representa entrevistas. | Alto para decisiones de producto; no bloquea pruebas de software sintéticas. | No usar porcentajes para priorizar demanda/segmento. Validar con campo antes de fijar alcance, posicionamiento o piloto. |
| El canal de captura no está definido y podría tener restricciones de plataforma. | Alto; PRD RK3 / Q1. | Separar adaptador del dominio; probar opciones con datos sintéticos y emitir ADR antes de integración. |
| Privacidad y rechazo a acceso amplio al correo (hipótesis ilustrada por S-0.1; no evidencia real). | Alto; PRD RK4 / SRS NFR-07. | Tratar minimización y control del usuario como principios de diseño; validar preferencias y canal con usuarios reales. |
| Los formatos de notificación cambian. | Alto impacto; PRD RK2. | Parsers aislados/versionados, fixtures, cola de no reconocidos y alertas. |
| Muestras reales podrían no estar disponibles o no ser utilizables. | Dependencia abierta; PRD R3 / SRS A3. | Definir esquema canónico y fixtures; no declarar cobertura real hasta probar muestras autorizadas. |
| Alcance excesivo para un solo desarrollador. | Alto; PRD RK5/SRS. | Vertical slice pequeña; mantener reportes, CSV y aplicación móvil fuera del MVP inicial. |
| Los emisores pueden mejorar verificadores/notificaciones. | Medio/alto; PRD RK6. | Verificar la cobertura actual antes de decidir; diferenciar Chulito por visibilidad entre roles y cuadre multiemisor. |
| Supuesto regulatorio del SRS podría ser incorrecto o incompleto. | Alto antes de piloto. | Revisión legal local; no inferir una exención únicamente porque el producto no custodie fondos. |

## 8. Plan de avance: supuestos, validación y riesgos técnicos

### Frente A — Confirmar alcance y trazabilidad

1. Registrar como hipótesis a validar: negocio con empleados y varios emisores; explorar cajero sin cuenta del dueño + libro diario; no declararlo segmento/alcance confirmado.
2. Realizar entrevistas reales con perfiles priorizados; actualizar PRD con evidencia, hipótesis confirmadas/refutadas y decisiones de alcance. No presentar los 16 registros ficticios como datos de campo.
3. Revisar y aprobar trazabilidad PRD v0.3–SRS v0.3 y requisitos técnicos añadidos; la corrección documental de RF-06 ya está reflejada.

**Salida:** evidencia real y decisiones de producto registradas; matriz PRD–SRS revisada y aprobada antes de baselinar MVP.

### Frente B — Reducir riesgo de captura

1. Mantener la entrada detrás de una interfaz/adaptador, sin acoplarla a correo o Android.
2. Probar alternativas de captura con eventos sintéticos; priorizar la opción de menor acceso y comparar reenvío selectivo frente a lectura limitada.
3. Definir esquema canónico: negocio, emisor, monto, fecha/hora, referencia si existe, huella, estado de parseo y origen.
4. Decidir el canal con ADR que incluya permisos, límites de plataforma, revocación, privacidad y fallos.

**Salida:** prueba reproducible de alternativas y decisión documentada; sin afirmar integración productiva.

### Frente C — Construir una vertical slice del valor priorizado

Implementar en un entorno de prueba: dueño/cajero, cobro esperado, evento sintético de pago, emparejamiento explícito, vista del cajero, libro diario y auditoría. Probar idempotencia, campos ausentes, duplicados, mensajes no reconocidos, discrepancias y aislamiento multi-tenant. Mantener el estado “dudoso/no reconocido” para revisión humana.

**Salida:** demostración verificable de confirmación compartida + registro multiemisor con fixtures sintéticos.

### Frente D — Preparar el piloto, sin bloquear el prototipo

Para el piloto, primero validar segmento y alcance con investigación real; luego elegir emisor(es), conseguir muestras autorizadas/anonimizadas, fijar línea base del cuadre, acordar retención/borrado, completar revisión legal y definir soporte/incidentes. Las entrevistas no bloquean el spike técnico con datos sintéticos, pero sí son necesarias para confirmar decisiones de producto y preparar un piloto responsable.

**Salida:** puertas y criterios de piloto definidos. Registrar resultados de campo como evidencia nueva e independiente; contrastarlos con las hipótesis inspiradas en S-0.1 y revisar prioridades mediante decisión documentada.

## 9. Criterios de preparación y salida

### Listo para iniciar desarrollo limitado

- S-0.1 identificado como escenario simulado, no evidencia. PRD v0.3 y SRS v0.3 disponibles como documentos de trabajo; la aprobación de requisitos y la validación de producto siguen pendientes.
- Alcance de la vertical slice limitado a roles, evento sintético, idempotencia, emparejamiento explícito y libro diario.
- Fixtures sintéticos marcados como tales; ningún dato real o personal en repositorio, logs o capturas.
- Pruebas de aislamiento y revocación de cajero especificadas.

### Listo para comprometer captura de un emisor

- Canal elegido mediante ADR, restricciones revisadas y control del usuario descrito.
- Emisor elegido para el MVP y muestra autorizada/anónima disponible, o definición clara de qué campos no pueden comprobarse.
- Comportamiento de duplicado, campos ausentes, mensajes no reconocidos y discrepancias probado.
- Retención, borrado, acceso, auditoría y riesgos legales revisados.

### Listo para piloto

- Negocio(s) participantes, consentimiento, soporte y condiciones definidos.
- Métricas con línea base, denominadores y periodos acordados.
- Revisión legal/privacidad completada, amenazas principales mitigadas y política de incidentes/disposición de datos aprobada.
- Requisitos/criterios del PRD y SRS reconciliados y aprobados para el alcance del piloto.

## 10. Verificaciones realizadas y asuntos pendientes

1. **Origen y trazabilidad SRS:** SRS v0.3 declara PRD v0.3 como origen y RF-06 como aislamiento. La revisión y aprobación de la matriz completa siguen pendientes; la trazabilidad no valida las hipótesis de producto.
2. **Requisitos técnicos añadidos:** confirmar que SRS-F-14/F-15, NFR-01–13, interfaces y decisiones de despliegue trazan a un requisito, riesgo o restricción vigente, e identificar cuáles necesitan aprobación del dueño del producto.
3. **Compatibilidad del stack:** el spike Node.js/TypeScript/NestJS previsto para ADR-0001 no se ha ejecutado; ST-01 compara canales de captura y no lo sustituye.
4. **Implementación objetivo:** la vertical slice Python es especificación ejecutable con pruebas sintéticas; portar lógica y pruebas a TypeScript/NestJS está pendiente y Python no es el backend de producción.
5. **Validación de producto:** S-0.1 es un escenario simulado con 16 registros ficticios y no aporta evidencia de campo. Realizar entrevistas para decidir segmento y alcance; el prototipo técnico con datos sintéticos puede avanzar en paralelo, sin presentarlo como validación de producto.
6. **Muestras reales:** el PRD depende de muestras autorizadas y anonimizadas; el SRS A3 lo expresa como supuesto. No aparece un conjunto de muestras reales en el material consultado; tratar su disponibilidad como dependencia abierta.
7. **Regulación:** el SRS NFR-13 plantea una exención como supuesto. Mantenerla como pregunta legal y no usarla para justificar el piloto.
8. **Panorama de alternativas:** el PRD fecha su comparación a 11-oct-2026 y advierte que las fuentes no se verificaron en páginas completas. Confirmar funciones actuales antes de tomar decisiones de posicionamiento.

## 11. Conclusión

S-0.1 no permite concluir que se deba replantear el alcance: es un escenario simulado, no resultados de entrevistas. Como hipótesis para investigación, se propone explorar negocios pequeños con empleados y varios emisores, confirmación para el cajero y libro diario, manteniendo fraude como posible función secundaria. No fijar segmento ni MVP hasta contrastarlo con evidencia real y aprobar la decisión.

El equipo puede avanzar con pruebas técnicas basadas en eventos sintéticos. La integración real requiere elección de emisor/canal, muestras autorizadas, reglas de conciliación, retención y revisión legal. Las entrevistas reales no bloquean ese spike técnico, pero sí son necesarias para validar segmento, problema y alcance del MVP antes de baselinar producto o iniciar un piloto.

**Siguiente paso recomendado:** (1) planear entrevistas reales que validen problema, segmento y alcance; (2) completar el spike de compatibilidad de Node.js, TypeScript y NestJS previsto para ADR-0001; (3) portar la especificación ejecutable Python del ST-01 a TypeScript/NestJS; y (4) continuar pruebas de canales por separado, con muestras autorizadas. ST-01 compara canales y no sustituye el spike de compatibilidad del stack.

## 12. Fuentes documentales

- **[D1]** *Documento de requisitos del producto (PRD)*, CNF-PRD-001, v0.3, 12 de octubre de 2026. Archivo: `PRD_Chulito_v0.3_ISO29148.pdf`.
- **[D2]** *Especificación de requisitos de software (SRS)*, CNF-SRS-001, v0.3. Archivo: `SRS_Chulito_v0.3_29148_alineacion_estructural.pdf` y su DOCX editable. Derivado del PRD v0.3; pendiente de revisión y aprobación.
- **[D3]** *Guía de entrevistas de validación*, CNF-GEI-001, v0.1, 11 de octubre de 2026. Archivo: `Guia_Entrevistas_Chulito_v0.1_IEEE.pdf`.
- **[D4]** *Informe de síntesis de investigación — Hallazgos de descubrimiento*, CNF-HAL-001-S, S-0.1. Archivo: `Informe_Hallazgos_Chulito_S-0.1_Escenario_Simulado.pdf`. S-0.1 es un escenario simulado, no resultados de entrevistas realizadas. Las cifras son ficticias y solo se conservan como supuesto de trabajo; no son evidencia ni proyección de mercado.

**Nota metodológica:** la mención de ISO/IEC/IEEE 29148 en PRD y SRS describe una alineación estructural/metodológica seleccionada. No es certificación ni declaración formal de conformidad con la norma.
