# Fuentes oficiales consultadas — canales de captura de Confirma

**Fecha de consulta:** 13 de octubre de 2026  
**Uso:** insumo para el spike técnico de selección de canal. Las notas distinguen hechos publicados de conclusiones de diseño.

## Android: escucha de notificaciones

1. **Android Developers, `NotificationListenerService` API reference**  
   URL: <https://developer.android.com/reference/android/service/notification/NotificationListenerService>  
   La referencia describe el servicio como receptor de llamadas del sistema cuando se publican, retiran o cambia la clasificación de notificaciones. Para extenderlo, la aplicación debe declarar el servicio en el manifiesto con `android.permission.BIND_NOTIFICATION_LISTENER_SERVICE` y un intent filter con `android.service.notification.NotificationListenerService`. La implementación debe esperar a `onListenerConnected()` antes de operar. La documentación también registra limitaciones de listeners en dispositivos de baja RAM con Android Q o anterior y de listeners en perfiles de trabajo.

2. **Android Developers, `Settings.ACTION_NOTIFICATION_LISTENER_SETTINGS`**  
   URL: <https://developer.android.com/reference/android/provider/Settings#ACTION_NOTIFICATION_LISTENER_SETTINGS>  
   La acción abre los ajustes de acceso de listeners de notificaciones (añadida en API 22). En la práctica del producto, la captura necesita que la persona usuaria habilite el listener desde esos ajustes; el prototipo debe comprobar la experiencia y el comportamiento en las versiones/dispositivos objetivo. La concesión no debe presentarse como automática.

**Implicación de diseño:** Android puede cubrir notificaciones emitidas por apps instaladas, no solo correo, pero exige un componente Android y una autorización de acceso de notificaciones en el dispositivo. El listener es una capacidad a nivel del sistema; se debe aplicar allowlist de paquetes en el dispositivo, minimizar contenido recolectado y medir revocación, reinicios y restricciones de fabricante. La referencia no garantiza que los emisores concretos de Confirma publiquen los campos requeridos en sus notificaciones.

## Gmail: lectura por API y reenvío selectivo

3. **Google for Developers, `Choose Gmail API scopes`**  
   URL: <https://developers.google.com/workspace/gmail/api/auth/scopes>  
   La tabla clasifica `https://www.googleapis.com/auth/gmail.readonly` como scope restringido y lo describe como acceso para ver mensajes y configuración del correo. Google indica que los scopes restringidos requieren verificación OAuth; si los datos de scopes restringidos se almacenan en servidores o se transmiten, debe realizarse una evaluación de seguridad. La política recomienda pedir el scope menos amplio posible.

4. **Gmail Help, `Automatically forward Gmail messages to another account`**  
   URL: <https://support.google.com/mail/answer/10957?hl=en>  
   Gmail permite reenviar todos los mensajes o solo los que coinciden con criterios de filtros. Al agregar una dirección de reenvío se envía un enlace de verificación a esa dirección. Para reenviar mensajes seleccionados, se desactiva el reenvío global y se configura un filtro con la acción `Forward it`.

**Implicación de diseño:** leer una cuenta Gmail mediante OAuth desde Confirma representa una carga de autorización y verificación elevada para el MVP. El reenvío mediante filtro puede limitar los correos enviados al servicio y evita que Confirma lea el buzón mediante un scope API, pero conserva una transferencia de contenido, requiere configuración/verificación por la persona dueña y aplica principalmente si el emisor notifica por correo. No elimina las obligaciones de privacidad, retención ni seguridad.

## Conclusión provisional (no es ADR de decisión final)

- La vertical slice no debe depender todavía de un canal real: debe aceptar envelopes sintéticos de varios adaptadores y validar el contrato canónico, conciliación e idempotencia.
- Para una prueba real posterior, comparar **reenvío de correo filtrado** con **listener Android de allowlist** en un spike acotado; no implementar lectura amplia de Gmail como primera alternativa.
- No elegir definitivamente hasta completar pruebas con muestras autorizadas/anonimizadas de los emisores prioritarios, medir carga de configuración y revisar el tratamiento de datos. Esta recomendación aplica como decisión técnica de la iteración y puede corregirse con nuevas indicaciones del responsable.
