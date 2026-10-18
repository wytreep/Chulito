# CONFIRMA — Síntesis documental de línea base operativa

**Consolidación de hallazgos de trabajo, visión, requisitos y decisiones · Fase 0**

| Campo | Valor |
|---|---|
| Código | CNF-SD-001 |
| Versión | SD-0.2 |
| Fecha | 13 de octubre de 2026 |
| Estado | Base operativa adoptada para planificación y diseño; sujeta a correcciones del responsable |
| Proyecto | Confirma (nombre provisional) |
| Documentos base | PRD v0.3; SRS v0.1; Guía de entrevistas v0.1; S-0.1 como base de trabajo |
| Uso | Interno — borrador de trabajo |

> **Recomendación ejecutiva.** Adoptar S-0.1 como base operativa de esta iteración. La señal prioritaria es un negocio pequeño con empleados que necesita confirmar pagos sin exponer la cuenta del dueño y cuadrar varios emisores. Reencuadrar el MVP alrededor de confirmación compartida y libro diario; mantener el fraude como función secundaria. Avanzar con una vertical slice técnica usando eventos sintéticos mientras se resuelven captura, emisores, trazabilidad y privacidad.

> **Límite decisional.** Los valores de S-0.1 se aceptan para priorizar decisiones internas de producto, pero no se extrapolan como estimación de mercado ni como métricas de uso del producto. El responsable puede corregir cualquier dato asumido.

> **Alcance de la síntesis.** Usa los registros de S-0.1 como premisas de trabajo para esta fase, conserva su trazabilidad y actualiza la recomendación de avance; no reemplaza el PRD ni el SRS.

<!-- PAGEBREAK -->

## Control y resumen ejecutivo

Para esta iteración, S-0.1 se adopta como **base operativa aceptada por el responsable del proyecto**. Su distribución de trabajo es n=16: cinco tiendas de barrio, cuatro negocios de comida/domicilios, cuatro vendedores por redes y tres cajeros/empleados. Las señales que orientan la prioridad son 14/16 con pagos digitales semanales, 9/16 que aceptan pantallazos, 8/16 con un caso concreto de comprobante falso o dudoso, 10/16 con cierre manual de 20–40 minutos y 11/16 preocupados por dar acceso al correo. En los negocios con empleados, 6 de 7 describen llamadas al dueño o uso compartido del teléfono para confirmar.

La decisión que se adopta del informe es **replantear el alcance, no cambiar de proyecto**. El usuario prioritario es el negocio pequeño con empleados y varios emisores; la propuesta central pasa a ser confirmación compartida para el cajero y libro diario multiemisor. La detección de pantallazos falsos queda como función secundaria: los emisores ya cubren parte del problema y el cierre manual/visibilidad de pagos parece ofrecer una oportunidad más transversal. La preocupación por el acceso al correo favorece explorar primero un mecanismo controlado por el usuario, como el reenvío selectivo, antes que el acceso completo.

El trabajo puede continuar sin esperar nuevas entrevistas: primero se reconcilian PRD v0.3 y SRS v0.1; en paralelo se prueba la ingestión desacoplada y una vertical slice con eventos sintéticos. Se mantienen como puertas antes de captura real el canal autorizado, los emisores iniciales, las muestras utilizables, la política de retención y la revisión legal.

### Decisión recomendada

1. Adoptar para el diseño actual el segmento de negocio pequeño con empleados y varios medios de pago; no priorizar al vendedor individual en el MVP.
2. Centrar la primera versión en vista del cajero sin acceso a la cuenta del dueño, confirmación del pago recibido y libro diario unificado; tratar el fraude como complemento.
3. Priorizar una captura controlada por el usuario y evaluar reenvío de mensajes antes de acceso completo al correo; cerrar la opción mediante un ADR y revisión de privacidad/plataforma.
4. Avanzar con esquema canónico, idempotencia y flujo de conciliación usando datos sintéticos; corregir la trazabilidad SRS v0.1 ↔ PRD v0.3 antes de declarar línea base técnica.

**Estado de la base:** los hallazgos de S-0.1 se usan para tomar decisiones internas y quedan abiertos a correcciones del responsable; el archivo fuente se conserva como referencia.

## Contenido

1. Alcance y método de esta síntesis — p. 3  
2. Base documental y estado de la información — p. 3  
3. Comprensión consolidada del producto — p. 3  
4. Señales de S-0.1 y métricas de producto — p. 4  
5. Convergencia de requisitos y trazabilidad — p. 5  
6. Registro de decisiones pendientes — p. 6  
7. Riesgos y dependencias — p. 7  
8. Plan de avance con la línea base S-0.1 — p. 7  
9. Criterios de preparación y salida — p. 8  
10. Inconsistencias que conviene corregir — p. 9  
11. Conclusión — p. 9  
12. Fuentes documentales — p. 9

<!-- PAGEBREAK -->

## 1. Alcance y método de esta síntesis

Esta revisión consolida los documentos del proyecto y adopta los hallazgos y la recomendación de S-0.1 como base operativa de diseño, según la instrucción del responsable. Las cifras se usan para priorizar segmento, propuesta de valor y trabajo técnico de la siguiente iteración. No se introduce investigación externa ni se modifican los archivos PRD/SRS fuente.

El informe mantiene trazabilidad explícita a S-0.1 y usa sus valores dentro del alcance del proyecto; no los extrapola a todo el mercado ni los confunde con métricas de un producto en producción. Si el responsable corrige un registro, cifra o interpretación, se actualiza esta línea base y sus decisiones derivadas.

**Regla de lectura:** “base operativa” significa que los valores se aceptan para orientar la planificación actual. Los objetivos de producto (por ejemplo, latencia, reducción del tiempo de cuadre o falsos positivos) siguen siendo metas de diseño/piloto, no resultados observados de Confirma.

## 2. Base documental y estado de la información

| Fuente | Aporte a la síntesis | Estado y uso |
|---|---|---|
| [D1] PRD CNF-PRD-001, v0.3 (12-oct-2026) | Visión, público, alcance MVP, metas candidatas, requisitos, riesgos y decisiones. | Referencia vigente de producto; ajustar el énfasis de alcance con la decisión de reencuadre de S-0.1. |
| [D2] SRS CNF-SRS-001, v0.1 | Requisitos de software, reglas, criterios, interfaces, datos, trazabilidad y TBD. | Borrador derivado del PRD v0.2; reconciliarlo con el PRD v0.3 antes de baselinar. |
| [D3] Guía CNF-GEI-001, v0.1 | Hipótesis H1–H6, preguntas, perfiles, consentimiento y criterios. | Protocolo disponible si se decide ampliar o renovar la validación; no bloquea el avance técnico de esta iteración. |
| [D4] Informe CNF-HAL-001-S, S-0.1 | Distribución n=16, señales por hipótesis, prioridades y decisión de reencuadrar. | Base operativa aceptada por el responsable para esta iteración. Se conserva su procedencia y se aplica dentro del proyecto, sin extrapolación estadística. |

El conjunto de valores aceptado identifica un segmento prioritario y consecuencias de producto suficientes para orientar el próximo prototipo. La selección del canal/emisores y las decisiones de privacidad, datos y requisitos siguen abiertas.

## 3. Comprensión consolidada del producto

### 3.1 Propuesta de valor operativa

Confirma ayuda a un negocio pequeño con empleados a confirmar pagos digitales desde notificaciones del emisor, mostrar el estado al cajero sin exponer la cuenta financiera del dueño y reunir los movimientos de varios emisores en un libro diario. El registro debe distinguir confirmado, pendiente, dudoso y no reconocido; una coincidencia insuficiente no debe convertirse en confirmación automática.

### 3.2 Perfil prioritario y composición de la base

| Perfil incluido en S-0.1 | n | Prioridad de trabajo | Necesidad principal |
|---|---:|---|---|
| Tienda de barrio | 5 | Alta si tiene empleados y varios medios | El cajero ve el pago y el dueño puede cuadrar el día. |
| Negocio de comida/domicilios | 4 | Alta si tiene empleados y varios medios | Confirmación rápida durante la fila/entrega y registro diario. |
| Vendedor por redes/emprendedor | 4 | Media | Verificación rápida; no es el foco inicial de MVP. |
| Cajero/empleado | 3 | Rol usuario, no segmento comprador | Consultar la confirmación sin acceder a la cuenta del dueño. |
| **Total de registros de trabajo** | **16** | — | Distribución descrita en S-0.1. |

En el subgrupo de negocios con empleados, 6 de 7 describen que el cajero llama al dueño o comparte su teléfono; las alertas llegan al dueño. Esta señal respalda diseñar primero el acceso delegado del cajero, con permisos mínimos. El perfil que cobra solo y casi exclusivamente por QR queda en prioridad baja; el vendedor por redes permanece como posible segmento posterior.

### 3.3 Problema y alternativas actuales

El cierre es una señal de valor tan importante como la confirmación en caja: 10/16 reúnen varias aplicaciones y un cuaderno, con una duración estimada en S-0.1 de 20–40 minutos por noche. El problema de comprobantes falsos existe en la base de trabajo, pero no parece ser el dolor principal: 8/16 describen un caso reciente; varios ya usan verificadores/alertas, y 5/16 dicen que el verificador de Nequi les basta.

Tres de 16 tienen parlante de pagos. Se valora el aviso audible, pero no resuelve el historial ni el cuadre multiemisor y depende de un proveedor. La comparación inicial a mantener en la investigación de alternativas incluye verificador de Nequi, alertas de Bancolombia, Bre-B y parlantes; confirmar disponibilidad y cobertura antes de decidir integración o posicionamiento.

### 3.4 Límites del MVP

**Incluido como dirección:** negocio con empleados; roles dueño/cajero; confirmación del pago desde una fuente controlada; vista de confirmaciones para el cajero; libro diario de los emisores habilitados; conciliación básica; discrepancias para revisión; auditoría.

**Fuera del alcance inicial:** custodiar o mover dinero; sustituir POS/facturación; integraciones bancarias oficiales; aplicación móvil dedicada; reportes semanales/exportación; alertas por patrones sospechosos; y convertir la detección de pantallazos en el valor principal. La interfaz puede probarse antes de cerrar los detalles del canal real de captura.

## 4. Señales de S-0.1 y métricas de producto

### 4.1 Base operativa por hipótesis

| ID | Resultado de trabajo en S-0.1 (n=16) | Implicación adoptada para diseño |
|---|---|---|
| H1 — Frecuencia | 14/16 reciben pagos digitales cada semana; la proporción descrita va de 20 % a 60 % de las ventas. | Priorizar un flujo de pago frecuente y varios emisores, sin extrapolar el rango a todo el mercado. |
| H2 — Pantallazos | 9/16 aceptan pantallazos, especialmente en transferencias por número/llave; con QR suelen mirar la notificación. | Confirmar desde la notificación recibida; fraude de pantallazo como función secundaria, no como único valor. |
| H3 — Casos dudosos | 8/16 relatan un caso concreto de comprobante falso o dudoso en los últimos seis meses. | Mantener señalización/revisión, pero centrar el MVP en confirmación compartida y cuadre. |
| H4 — Coste | Montos típicos pequeños y un caso grande; el coste principal descrito es el tiempo y la tensión de verificar mientras hay fila. | Medir tiempo de caja y cierre; no priorizar el valor únicamente por pérdidas monetarias. |
| H5 — Soluciones actuales | 11/16 revisan la app o llaman al dueño; 5/16 consideran suficiente el verificador de Nequi. | Diseñar una vista delegada para el cajero y diferenciar el libro multiemisor de los verificadores existentes. |
| H6 — Prueba/privacidad | 7/16 dicen que probarían un piloto; 11/16 expresan preocupación por dar acceso al correo. | Preferir captura bajo control del usuario y probar primero reenvío selectivo frente a acceso total. |

### 4.2 Otras señales accionables

| Señal de trabajo | Dato de S-0.1 | Consecuencia |
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

Los valores de arriba se separan en dos categorías: señales de trabajo de S-0.1 aceptadas para priorización, y metas técnicas/comerciales aún no medidas en un producto operativo.

## 5. Convergencia de requisitos y trazabilidad

### 5.1 Requisitos de producto en lenguaje común

| PRD v0.3 | Resultado candidato | Desarrollo en el SRS v0.1 |
|---|---|---|
| RF-01 | Recibir notificaciones mediante el canal aprobado y normalizar solo campos disponibles. | SRS-F-10–14; SRS-F-15 añade estado de captura y debe trazarse explícitamente. |
| RF-02 | Evitar pagos duplicados al reprocesar una notificación. | SRS-F-13 y NFR-04. |
| RF-03 | El cajero consulta el estado del cobro sin acceso a la cuenta financiera del dueño. | SRS-F-20, F-23 y permisos de F-04. |
| RF-04 | Asociar un cobro esperado con un pago recibido. | SRS-F-21, F-22 y regla SRS-RN-03 [HIP/TBD-3]. |
| RF-05 | Mantener el libro diario unificado de los emisores habilitados por negocio. | SRS-F-30, F-31; F-32 (CSV) queda posterior al MVP. |
| RF-06 | Aislar los datos de cada negocio. | Correspondencia más directa: SRS-F-05 y SRS-NFR-06. |
| RF-07 | Crear y revocar cajeros con permisos limitados. | SRS-F-03 y F-04; F-01/F-02 son capacidades de alta/autenticación que requieren una traza de producto explícita. |
| RF-08 | Señalar discrepancias para revisión, sin convertirlas en confirmación automática. | SRS-F-24 y F-25. |

Esta tabla es una **propuesta de reconciliación**, no una edición de los documentos. La matriz existente del SRS asocia RF-06 también con SRS-F-01/F-02, aunque en el PRD v0.3 RF-06 significa aislamiento de negocios. Antes de baselinar, corregir esa traza y asignar un origen claro a alta de negocio/autenticación (SRS-F-01/F-02), estado de captura (F-15), alertas y requisitos técnicos añadidos.

### 5.2 Requisitos transversales y decisiones técnicas

El PRD v0.3 define como requisitos de calidad candidatos el aislamiento entre negocios, la minimización y revisión del tratamiento de datos personales (incluida la Ley 1581 de 2012), la recuperación ante fallos sin pérdida/duplicación y la auditoría de acciones sensibles. El SRS los desarrolla mediante cifrado, retención pendiente, TLS, Argon2id, un subconjunto aplicable de OWASP ASVS nivel 2, límites de tasa, registros sin datos sensibles, pruebas de aislamiento y despliegue reproducible.

El SRS también propone REST/OpenAPI 3.1, un canal de tiempo real por definir en ADR, contenedores y dependencias fijadas. Deben conservarse como propuestas técnicas sujetas a decisión; no todos son requisitos de producto aprobados. La referencia del SRS a que el servicio estaría fuera de regulación de pagos por no custodiar ni mover dinero es un supuesto por revisar: no tratarlo como conclusión legal. La revisión jurídica prevista en TBD-6 debe preceder al piloto con datos reales.

## 6. Registro de decisiones pendientes

| Prioridad | Decisión o vacío | Qué bloquea | Salida necesaria |
|---|---|---|---|
| Decisión de producto | Reencuadrar, no pivotar: negocio con empleados; confirmación compartida y libro diario; fraude secundario. | Posicionamiento, historias y orden del backlog. | Reflejarlo explícitamente en la próxima revisión del PRD y en criterios del MVP. |
| P0 | Canal de captura (PRD Q1 / SRS TBD-1): reenvío selectivo, lectura limitada u otra opción controlada. S-0.1 favorece evitar acceso total al correo. | Arquitectura de ingestión, permisos, retención y confianza. | Spike comparativo + ADR; evaluar primero reenvío selectivo, sin dar por resuelto el soporte/plataforma. |
| P0 | Emisores del MVP (Q2 / TBD-2). Alternativas nombradas: Nequi, alertas Bancolombia, Bre-B, parlantes. | Parsers y cobertura real. | Seleccionar un conjunto acotado según uso prioritario, viabilidad y muestras autorizadas. |
| P0 | Flujo de conciliación (Q3 / TBD-3): monto, hora, referencia, ventana y estados. | Confirmación errónea, falsos positivos y casos dudosos. | Tabla de reglas/escenarios; confirmar si los 10 minutos por defecto aplican. |
| P0 | Reconciliación PRD v0.3 ↔ SRS v0.1. | Línea base verificable y asignación de desarrollo. | Matriz actualizada de requisitos, origen, estado, prioridad y prueba; actualizar referencia de PRD v0.2. |
| P0 | Retención/eliminación (SRS TBD-4), aplicabilidad legal (TBD-6/NFR-13) y privacidad. | Uso de datos reales y piloto. | Revisar minimización, acceso, borrado, auditoría y aspectos legales en Colombia antes de captura real. |
| P1 | Catálogo de permisos dueño/cajero (RF-07). | RBAC y pruebas de aislamiento. | Matriz rol × acción; revocación, sesiones y datos visibles. |
| P1 | Muestras para parsers (PRD R3 / SRS A3). | Declarar soporte efectivo de emisores. | Obtener muestras autorizadas/anónimas; mientras tanto, usar fixtures sintéticos. |
| P2 | Canal de alertas al dueño (SRS TBD-5). | Gestión de mensajes no reconocidos/errores. | Definir canal; se puede simular en el prototipo. |
| P2 | Precio/modelo de uso (PRD Q4). | Alcance comercial del piloto. | Posponer hasta medir adopción y valor de la propuesta priorizada. |
| No bloqueante ahora | Validación adicional con campo y muestra de la guía. | Aumentaría confianza y permitiría corregir la base. | No detener la vertical slice; si se programa, actualizar n y criterios de la guía antes de recoger nuevos datos. |

## 7. Riesgos y dependencias

| Riesgo | Nivel de atención | Mitigación para avanzar ahora |
|---|---|---|
| La distribución n=16 es de conveniencia y puede no representar a todos los comercios. | Medio; limita extrapolación, no bloquea diseño de esta iteración. | Usarla para priorizar el perfil indicado; no convertir porcentajes en tamaño de mercado. Actualizar si el responsable corrige datos o se incorpora evidencia nueva. |
| El canal de captura no está definido y podría tener restricciones de plataforma. | Alto; PRD RK3 / Q1. | Separar adaptador del dominio; probar opciones con datos sintéticos y emitir ADR antes de integración. |
| Privacidad y reticencia a dar acceso al correo (11/16 en S-0.1). | Alto; PRD RK4 / SRS NFR-07. | Priorizar reenvío/consentimiento granular; no pedir acceso total por defecto; minimizar y no registrar contenido sensible. |
| Los formatos de notificación cambian. | Alto impacto; PRD RK2. | Parsers aislados/versionados, fixtures, cola de no reconocidos y alertas. |
| Muestras reales podrían no estar disponibles o no ser utilizables. | Dependencia abierta; PRD R3 / SRS A3. | Definir esquema canónico y fixtures; no declarar cobertura real hasta probar muestras autorizadas. |
| Alcance excesivo para un solo desarrollador. | Alto; PRD RK5/SRS. | Vertical slice pequeña; mantener reportes, CSV y aplicación móvil fuera del MVP inicial. |
| Los emisores pueden mejorar verificadores/notificaciones. | Medio/alto; PRD RK6. | Verificar la cobertura actual antes de decidir; diferenciar Confirma por visibilidad entre roles y cuadre multiemisor. |
| Supuesto regulatorio del SRS podría ser incorrecto o incompleto. | Alto antes de piloto. | Revisión legal local; no inferir una exención únicamente porque el producto no custodie fondos. |

## 8. Plan de avance con la línea base S-0.1

### Frente A — Confirmar alcance y trazabilidad

1. Adoptar como dirección de producto el negocio con empleados y varios emisores; promesa central: cajero confirma sin cuenta del dueño + libro diario; fraude secundario.
2. Actualizar la próxima revisión del PRD con esta prioridad, los datos de trabajo n=16, el hallazgo de privacidad y la preferencia por captura controlada.
3. Reconciliar RF/RNF del PRD v0.3 con el SRS v0.1; marcar los requisitos técnicos que necesitan aprobación y corregir RF-06.

**Salida:** alcance del MVP priorizado y matriz PRD–SRS consistente.

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

Para el piloto, elegir emisor(es), conseguir muestras autorizadas/anonimizadas, fijar línea base del cuadre, acordar retención/borrado, completar revisión legal y definir soporte/incidentes. La guía de entrevistas puede usarse más adelante para comprobar o corregir la base; no es condición previa para la prueba técnica actual.

**Salida:** puertas y criterios de piloto definidos. Si entran datos de campo nuevos, registrar diferencias respecto de S-0.1 y actualizar la línea base antes de cambiar prioridades.

## 9. Criterios de preparación y salida

### Listo para iniciar desarrollo limitado

- S-0.1 adoptado como base operativa de esta iteración; PRD v0.3 como referencia de producto y SRS v0.1 pendiente de reconciliación.
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

## 10. Inconsistencias que conviene corregir

1. **Versión de origen del SRS:** el control y la introducción del SRS v0.1 dicen que deriva del PRD v0.2; existe un PRD v0.3 más reciente. Actualizar la relación de origen y revisar cambios, no cambiar solo la etiqueta de versión.
2. **RF-06:** en PRD v0.3 significa aislamiento de datos. La matriz SRS existente incluye bajo ese ID alta/autenticación (F-01/F-02) además de aislamiento. Reasignar o crear trazas de producto para esas funciones base.
3. **Requisitos técnicos añadidos:** confirmar que SRS-F-14/F-15, NFR-01–13, interfaces y decisiones de despliegue trazan a un requisito, riesgo o restricción vigente; identificar cuáles son decisiones del desarrollador y cuáles necesitan aprobación del dueño del producto.
4. **Muestras y criterios:** S-0.1 aporta n=16 como base operativa para esta fase; la guía v0.1 conserva un protocolo para cinco entrevistas. No bloquear el prototipo por esa diferencia. Si se recoge una muestra nueva, definir de antemano el tamaño, los perfiles y los criterios para no mezclar bases ni umbrales.
5. **Muestras reales:** el PRD depende de muestras autorizadas y anonimizadas; el SRS A3 lo expresa como supuesto. No aparece un conjunto de muestras en el material consultado; tratar su disponibilidad como dependencia abierta.
6. **Regulación:** el SRS NFR-13 plantea una exención como supuesto. Mantenerla como pregunta legal y no usarla para justificar el piloto.
7. **Panorama de alternativas:** el PRD fecha su comparación a 11-oct-2026 y advierte que las fuentes no se verificaron en páginas completas. Confirmar funciones actuales antes de tomar decisiones de posicionamiento.

## 11. Conclusión

Con la base operativa de S-0.1, la decisión de trabajo es **replantear el alcance, no cambiar de proyecto**. El foco será el negocio pequeño con empleados y varios emisores; la primera propuesta de valor es dar al cajero confirmación confiable sin exponer la cuenta del dueño y reducir el cuadre manual con un libro diario. Los pantallazos falsos siguen siendo un problema a atender, pero no serán el eje del MVP.

El equipo puede avanzar desde ahora con la trazabilidad PRD–SRS, un ADR de captura y una vertical slice basada en eventos sintéticos. La integración real queda condicionada a elección de emisor/canal, muestras autorizadas, reglas de conciliación, retención y revisión legal. Nuevas entrevistas pueden corregir o ampliar esta base, pero no son un bloqueo para el desarrollo limitado de esta iteración.

**Siguiente paso recomendado:** crear el backlog y los criterios de aceptación del MVP reencuadrado; en paralelo corregir la matriz de trazabilidad SRS v0.1 y ejecutar el spike que compare una vía de captura controlada, con prioridad inicial al reenvío selectivo frente al acceso completo al correo.

## 12. Fuentes documentales

- **[D1]** *Documento de requisitos del producto (PRD)*, CNF-PRD-001, v0.3, 12 de octubre de 2026. Archivo: `PRD_Confirma_v0.3_ISO29148.pdf`.
- **[D2]** *Especificación de requisitos de software (SRS)*, CNF-SRS-001, v0.1. Archivo: `SRS_Confirma_v0.1_29148_estructura_alineada.pdf` y su DOCX editable. El contenido declara derivación del PRD v0.2.
- **[D3]** *Guía de entrevistas de validación*, CNF-GEI-001, v0.1, 11 de octubre de 2026. Archivo: `Guia_Entrevistas_Confirma_v0.1_IEEE.pdf`.
- **[D4]** *Informe de síntesis de investigación — Hallazgos de descubrimiento*, CNF-HAL-001-S, S-0.1. Archivo: `Informe_Sintesis_Investigacion_Confirma_S-0.1.pdf`. Base operativa adoptada por el responsable para decisiones de esta iteración; los valores se conservan con su fuente y se usan para priorización interna, no como proyección de mercado.

**Nota metodológica:** la mención de ISO/IEC/IEEE 29148 en PRD y SRS describe una alineación estructural/metodológica seleccionada. No es certificación ni declaración formal de conformidad con la norma.
