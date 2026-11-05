# Política de cookies

**Chulito — confirmación compartida de pagos y libro diario para negocios pequeños**

> **BORRADOR (v0.1).** Documento de trabajo para revisión legal (**TBD-6**). El frontend del producto todavía no está implementado (TBD-9): esta política describe el comportamiento **previsto** y debe completarse con el inventario real de cookies antes de publicar. No constituye asesoría jurídica.

| Campo | Valor |
|---|---|
| Versión | 0.1 (borrador) |
| Fecha | 4 de noviembre de 2026 |
| Estado | Borrador — revisión legal pendiente (TBD-6) |
| Responsable | [RAZÓN SOCIAL], NIT [NIT] |
| Entrada en vigencia | [FECHA] |
| Sitio | [URL] |

## 1. Qué son las cookies y tecnologías similares

Las cookies son archivos pequeños que un sitio web guarda en el navegador. Permiten recordar la sesión, proteger la cuenta y medir el uso del sitio. Chulito también puede usar **almacenamiento local** (`localStorage`, `sessionStorage`), **píxeles** y tecnologías equivalentes; esta política los cubre a todos.

## 2. Marco normativo

En Colombia no existe una ley específica de cookies. Se aplican las reglas de protección de datos personales:

- **Ley 1581 de 2012** y **Decreto 1377 de 2013** (compilado en el Decreto 1074 de 2015), cuando la cookie permite identificar o hacer identificable a una persona;
- las guías y conceptos de la **Superintendencia de Industria y Comercio (SIC)** sobre datos personales y canales digitales;
- la **Ley 1480 de 2011** (Estatuto del Consumidor), en materia de información veraz y suficiente.

Las cookies estrictamente necesarias para prestar el servicio no requieren consentimiento, porque sin ellas el servicio no funciona. Las demás sí.

## 3. Tipos de cookies según su finalidad

| Tipo | Para qué sirve | ¿Requiere consentimiento? |
|---|---|---|
| **Técnicas o necesarias** | Mantener la sesión, autenticar, prevenir fraude (CSRF), balancear carga y recordar el estado del formulario | No |
| **De preferencia** | Recordar idioma, zona horaria, filtros y opciones de la interfaz | Sí |
| **Analíticas** | Medir visitas, uso de funciones y errores, de forma agregada | Sí |
| **Publicitarias** | Mostrar o medir anuncios | Sí (Chulito no las prevé en el MVP) |

## 4. Cookies que Chulito prevé usar

> **Nota para TBD-9:** esta tabla es un inventario **previsto**, no implementado. Debe reemplazarse con los nombres, duraciones y proveedores reales antes de publicar el sitio.

| Nombre | Tipo | Finalidad | Duración | Proveedor | ¿Esencial? |
|---|---|---|---|---|---|
| `chulito_session` | Técnica | Mantener la sesión autenticada | Sesión | Chulito | Sí |
| `chulito_csrf` | Técnica | Proteger contra falsificación de peticiones | Sesión | Chulito | Sí |
| `chulito_prefs` | Preferencia | Recordar idioma y filtros | 12 meses | Chulito | No |
| `chulito_consent` | Técnica | Guardar la decisión sobre cookies | 12 meses | Chulito | Sí |
| `_ga`, `_ga_*` | Analítica | Medir uso del sitio (si se habilita) | 24 meses | [Proveedor] | No |

Si el sitio no habilita analítica, las cookies `_ga` no se instalan y la fila se elimina de esta tabla.

## 5. Consentimiento

1. Al entrar al sitio, Chulito muestra un aviso con tres opciones: **aceptar todas**, **rechazar las no esenciales** y **configurar**.
2. Las cookies no esenciales **no se instalan** hasta que la persona las acepte. El aviso no usa casillas premarcadas ni obliga a aceptar para continuar.
3. Rechazar las no esenciales no impide usar el servicio.
4. La decisión se guarda y se puede cambiar en cualquier momento desde **[ENLACE/CONFIGURACIÓN]** o borrando las cookies del navegador.
5. Chulito conserva registro de la decisión (fecha, hora, versión del aviso y opciones elegidas) como prueba de consentimiento.

## 6. Cómo administrar las cookies en el navegador

La mayoría de navegadores permiten ver, bloquear y eliminar cookies:

- **Chrome:** Configuración → Privacidad y seguridad → Cookies y otros datos de sitios.
- **Edge:** Configuración → Cookies y permisos del sitio.
- **Firefox:** Configuración → Privacidad y seguridad.
- **Safari:** Preferencias → Privacidad.

Bloquear las cookies técnicas puede impedir el inicio de sesión o el funcionamiento del servicio.

## 7. Terceros y transferencia de datos

Si se habilitan cookies analíticas o de terceros, el proveedor puede tratar datos técnicos (dirección IP, identificadores del navegador, páginas visitadas). Chulito:

1. solo contrata proveedores que ofrezcan garantías de seguridad y confidencialidad;
2. documenta el país de alojamiento y, si hay transferencia internacional, la causal aplicable conforme al artículo 26 de la Ley 1581 de 2012;
3. no usa cookies de terceros para publicidad comportamental en el MVP.

> **Nota para TBD-6:** confirmar el proveedor de analítica, el país de alojamiento y si se requiere autorización adicional para la transferencia.

## 8. Relación con la política de datos personales

El tratamiento de datos personales se rige por la **Política de tratamiento de datos personales** y el **Aviso de privacidad**, disponibles en [URL]. Esta política de cookies los complementa y no los sustituye.

## 9. Cambios y vigencia

Esta política rige desde [FECHA]. Si se añaden cookies o cambia su finalidad, se actualizará la tabla y se pedirá el consentimiento de nuevo cuando corresponda. La versión vigente estará publicada en [URL].

## 10. Contacto

Para preguntas sobre cookies o datos personales: **[privacidad@dominio]**.

## Anexo. Inventario técnico (a completar en TBD-9)

| Elemento | Dónde se guarda | Qué contiene | Retención |
|---|---|---|---|
| Sesión | Cookie `HttpOnly` / `Secure` | Identificador de sesión | Sesión o [N] horas |
| Preferencias | `localStorage` | Idioma, filtros | Hasta borrar |
| Consentimiento | Cookie | Versión del aviso y opciones | 12 meses |
| Analítica (si aplica) | Cookie de terceros | Identificador seudónimo | [N] meses |
