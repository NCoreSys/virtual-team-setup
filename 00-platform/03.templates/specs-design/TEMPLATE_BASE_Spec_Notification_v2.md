# 🔔 TEMPLATE BASE — SPEC NOTIFICATION SYSTEM (Push/In-App/Email/SMS)

> **Versión:** 2.0 (Estandarizada para agentes)  
> **Tipo:** P2 — Enterprise/Scale  
> **Última actualización:** {{FECHA_ACTUALIZACION}}

---

## 🔖 GUÍA DE USO DEL TEMPLATE

### Marcadores de obligatoriedad

| Marcador | Significado | Regla |
|----------|-------------|-------|
| `[OBL]` | **Obligatorio** | Siempre debe completarse |
| `[OPC]` | **Opcional** | Completar si aplica al proyecto |
| `[COND]` | **Condicional** | Completar solo si se cumple la condición indicada |

### Cuándo usar este template

- ✅ **Notificaciones push** (mobile/web)
- ✅ **Notificaciones in-app** (banners, badges, toasts)
- ✅ **Emails transaccionales** (confirmaciones, alertas)
- ✅ **SMS/WhatsApp** transaccionales
- ✅ **Centro de notificaciones** (notification center)
- ✅ **Preferencias de usuario** (opt-in/out)
- ❌ Email marketing/newsletters → sistema de marketing separado
- ❌ Toasts de feedback inmediato → cubierto en UXStates

---

# ESPECIFICACIÓN DE SISTEMA DE NOTIFICACIONES

---

## 0) Metadatos del documento [OBL]

> **Activación:** Siempre obligatorio.

| Campo | Valor |
|-------|-------|
| **Nombre del documento** | Spec_Notifications_{{NOMBRE_PROYECTO}}_{{VERSION}} |
| **Proyecto** | {{NOMBRE_PROYECTO}} |
| **Alcance** | [Elegir: Global (todo el producto) / Módulo específico] |
| **ID técnico** | `notif-{{NUM}}-{{SLUG}}` (ej: `notif-01-global`) |
| **Versión** | {{VERSION}} |
| **Estado** | [Elegir: Draft / Review / Approved / Deprecated] |
| **Prioridad** | [Elegir: Crítica / Alta / Media / Baja] |
| **Fecha** | {{FECHA_YYYY-MM-DD}} |
| **Owner (PM/PO)** | {{NOMBRE_OWNER}} |
| **UX/UI Owner** | {{NOMBRE_UX}} |
| **Tech Lead** | {{NOMBRE_TECH}} |
| **QA Owner** | {{NOMBRE_QA}} |

---

## 1) Propósito del sistema de notificaciones [OBL]

> **Activación:** Siempre obligatorio.

### 1.1 Descripción general [OBL]

Este documento define el sistema de notificaciones del producto, incluyendo todos los canales, triggers, templates y preferencias de usuario.

| Campo | Valor |
|-------|-------|
| **Objetivo principal** | [Elegir: Engagement / Transaccional / Alertas / Mixto] |
| **Canales habilitados** | {{CANALES}} (ej: Push, In-app, Email, SMS) |
| **Volumen estimado** | {{VOLUMEN}} notificaciones/día |

### 1.2 Objetivo de negocio [OBL]

1. {{OBJETIVO_1}} (ej: Aumentar engagement y retención)
2. {{OBJETIVO_2}} (ej: Informar sobre eventos críticos)
3. {{OBJETIVO_3}} (ej: Reducir fricción en flujos)
4. {{OBJETIVO_4}} (ej: Cumplimiento regulatorio)

### 1.3 Objetivo UX [OBL]

- Notificaciones relevantes y oportunas
- No interrumpir innecesariamente
- Control total del usuario sobre preferencias
- Claridad en el mensaje y acción esperada

### 1.4 KPIs [OBL]

| Métrica | Valor objetivo | Canal |
|---------|----------------|-------|
| Delivery rate | > {{VALOR}}% | Push |
| Open rate | > {{VALOR}}% | Push, Email |
| CTR | > {{VALOR}}% | Todos |
| Opt-out rate | < {{VALOR}}% | Todos |
| Time to action | < {{VALOR}}min | Críticas |

---

## 2) Alcance (Scope) [OBL]

> **Activación:** Siempre obligatorio.

### 2.1 Incluye (In Scope) [OBL]

- {{INCLUYE_1}} (ej: Catálogo de notificaciones)
- {{INCLUYE_2}} (ej: Templates por canal)
- {{INCLUYE_3}} (ej: Triggers y condiciones)
- {{INCLUYE_4}} (ej: Preferencias de usuario)
- {{INCLUYE_5}} (ej: Centro de notificaciones)
- {{INCLUYE_6}} (ej: Analytics)

### 2.2 No incluye (Out of Scope) [OBL]

- {{EXCLUYE_1}} (ej: Email marketing/newsletters)
- {{EXCLUYE_2}} (ej: Notificaciones internas entre admins)

### 2.3 Dependencias [OBL]

| Tipo | Dependencia | Estado | Owner |
|------|-------------|--------|-------|
| Push provider | {{PROVIDER}} (ej: Firebase, OneSignal) | [Pendiente/Listo] | {{OWNER}} |
| Email provider | {{PROVIDER}} (ej: SendGrid, SES) | [Pendiente/Listo] | {{OWNER}} |
| SMS provider | {{PROVIDER}} (ej: Twilio) | [Pendiente/Listo] | {{OWNER}} |
| User preferences | {{SISTEMA}} | [Pendiente/Listo] | {{OWNER}} |

---

## 3) Canales de notificación [OBL]

> **Activación:** Siempre obligatorio.

### 3.1 Canales habilitados [OBL]

| Canal | Habilitado | Provider | Opt-in requerido | Fallback |
|-------|------------|----------|------------------|----------|
| **Push mobile** | Sí/No | {{PROVIDER}} | Sí (OS level) | In-app |
| **Push web** | Sí/No | {{PROVIDER}} | Sí (browser) | Email |
| **In-app banner** | Sí/No | Interno | No | — |
| **In-app badge** | Sí/No | Interno | No | — |
| **Notification center** | Sí/No | Interno | No | — |
| **Email** | Sí/No | {{PROVIDER}} | Sí (registro) | — |
| **SMS** | Sí/No | {{PROVIDER}} | Sí (explícito) | Email |
| **WhatsApp** | Sí/No | {{PROVIDER}} | Sí (explícito) | SMS |

### 3.2 Prioridad de canales [OBL]

| Prioridad | Uso | Canales | Ejemplo |
|-----------|-----|---------|---------|
| **Crítica** | Requiere acción inmediata | Push + SMS + Email | Seguridad, pagos fallidos |
| **Alta** | Importante, tiempo sensible | Push + Email | Pedido enviado, mensaje nuevo |
| **Media** | Informativo, puede esperar | In-app + Email | Actualizaciones, tips |
| **Baja** | Nice to have | In-app only | Sugerencias, engagement |

### 3.3 Reglas de canal [OBL]

| Regla | Implementación |
|-------|----------------|
| Horario permitido | {{HORARIO}} (ej: 8am-10pm hora local) |
| Quiet hours | {{HORARIO}} (ej: 10pm-8am, excepto críticas) |
| Rate limiting | Max {{NUM}} notificaciones/día por usuario |
| Deduplicación | No repetir misma notificación en {{TIEMPO}} |
| Fallback automático | Si push falla → {{FALLBACK}} |

---

## 4) Catálogo de notificaciones [OBL] — **SECCIÓN NÚCLEO**

> **Activación:** Siempre obligatorio. Esta es la sección más importante.

### 4.1 Tabla de notificaciones [OBL]

| Notif ID | Nombre | Categoría | Trigger | Canales | Prioridad | Configurable |
|----------|--------|-----------|---------|---------|-----------|--------------|
| `notif-001` | Bienvenida | Onboarding | Registro completado | Email + In-app | Alta | No |
| `notif-002` | Verificar email | Seguridad | Registro | Email | Crítica | No |
| `notif-003` | Pedido confirmado | Transaccional | Pago exitoso | Push + Email | Alta | Sí |
| `notif-004` | Pedido enviado | Transaccional | Cambio estado | Push + Email | Alta | Sí |
| `notif-005` | Mensaje nuevo | Social | Mensaje recibido | Push + In-app | Alta | Sí |
| `notif-006` | Pago fallido | Billing | Error de pago | Push + Email + SMS | Crítica | No |
| `notif-007` | Recordatorio carrito | Engagement | Abandono 24h | Push + Email | Media | Sí |
| `notif-008` | Producto favorito disponible | Engagement | Stock update | Push | Media | Sí |
| `{{NOTIF_ID}}` | {{NOMBRE}} | {{CATEGORIA}} | {{TRIGGER}} | {{CANALES}} | {{PRIORIDAD}} | Sí/No |

### 4.2 Categorías de notificaciones [OBL]

| Categoría | Descripción | Configurable por usuario |
|-----------|-------------|--------------------------|
| **Seguridad** | Login, password, 2FA | No (siempre activo) |
| **Transaccional** | Pedidos, pagos, envíos | Parcial (canal sí, recibir no) |
| **Social** | Mensajes, follows, likes | Sí |
| **Engagement** | Recordatorios, sugerencias | Sí |
| **Marketing** | Promos, ofertas | Sí (opt-in explícito) |
| **Sistema** | Mantenimiento, actualizaciones | No |

---

## 5) Detalle por notificación [OBL]

> **Activación:** Completar para cada notificación crítica.

### 5.1 Template de especificación [OBL]

#### Notificación: {{NOMBRE_NOTIFICACION}}

| Campo | Valor |
|-------|-------|
| **Notif ID** | `notif-{{NUM}}` |
| **Nombre interno** | {{NOMBRE}} |
| **Categoría** | {{CATEGORIA}} |
| **Prioridad** | [Crítica / Alta / Media / Baja] |
| **Configurable** | Sí/No |

**Trigger:**

| Campo | Valor |
|-------|-------|
| Evento | {{EVENTO}} |
| Condiciones | {{CONDICIONES}} |
| Delay | {{DELAY}} (ej: inmediato, 24h después) |
| Frecuencia | {{FRECUENCIA}} (ej: una vez, cada vez, max 1/día) |

**Canales y contenido:**

| Canal | Activo | Template ID |
|-------|--------|-------------|
| Push | Sí/No | `push-{{ID}}` |
| Email | Sí/No | `email-{{ID}}` |
| SMS | Sí/No | `sms-{{ID}}` |
| In-app | Sí/No | `inapp-{{ID}}` |

**Variables disponibles:**

| Variable | Tipo | Ejemplo |
|----------|------|---------|
| `{{user.name}}` | string | "María" |
| `{{order.id}}` | string | "#12345" |
| `{{order.total}}` | currency | "$99.00" |
| `{{product.name}}` | string | "Producto X" |
| `{{action_url}}` | URL | "https://..." |

---

## 6) Templates de contenido [OBL]

> **Activación:** Siempre obligatorio.

### 6.1 Push notifications [OBL]

| Template ID | Título | Body | Acción | Deep link |
|-------------|--------|------|--------|-----------|
| `push-001` | "¡Bienvenido, {{user.name}}!" | "Tu cuenta está lista. Explora ahora." | Abrir app | `app://home` |
| `push-003` | "Pedido confirmado ✓" | "Tu pedido {{order.id}} está en proceso." | Ver pedido | `app://orders/{{order.id}}` |
| `push-004` | "¡Tu pedido va en camino! 📦" | "{{order.id}} fue enviado. Llegará el {{delivery.date}}." | Rastrear | `app://tracking/{{order.id}}` |
| `push-{{ID}}` | "{{TITULO}}" | "{{BODY}}" | {{ACCION}} | `{{DEEPLINK}}` |

**Reglas de push:**

| Regla | Valor |
|-------|-------|
| Título max | 50 caracteres |
| Body max | 100 caracteres |
| Imagen | Opcional, 2:1 ratio |
| Acción | 1 CTA principal |

### 6.2 Email templates [OBL]

| Template ID | Subject | Preheader | CTA | Tipo |
|-------------|---------|-----------|-----|------|
| `email-001` | "Bienvenido a {{app.name}}, {{user.name}}" | "Tu cuenta está lista para usar" | "Explorar ahora" | Transactional |
| `email-002` | "Verifica tu email" | "Confirma tu cuenta para continuar" | "Verificar email" | Transactional |
| `email-003` | "Pedido {{order.id}} confirmado" | "Gracias por tu compra" | "Ver pedido" | Transactional |
| `email-{{ID}}` | "{{SUBJECT}}" | "{{PREHEADER}}" | "{{CTA}}" | {{TIPO}} |

**Reglas de email:**

| Regla | Valor |
|-------|-------|
| Subject max | 60 caracteres |
| Preheader max | 100 caracteres |
| From name | {{FROM_NAME}} |
| From email | {{FROM_EMAIL}} |
| Reply-to | {{REPLY_TO}} |
| Unsubscribe | Obligatorio (link en footer) |

### 6.3 SMS templates [COND]

> **Activación:** Incluir si se usa SMS.

| Template ID | Mensaje | Caracteres |
|-------------|---------|------------|
| `sms-006` | "{{app.name}}: Tu pago falló. Actualiza tu método: {{short_url}}" | 80 |
| `sms-{{ID}}` | "{{MENSAJE}}" | {{NUM}} |

**Reglas de SMS:**

| Regla | Valor |
|-------|-------|
| Max caracteres | 160 (1 SMS) o 306 (2 SMS) |
| Incluir opt-out | "Reply STOP to unsubscribe" |
| Short URLs | Usar acortador |

### 6.4 In-app notifications [OBL]

| Template ID | Tipo | Título | Body | CTA | Dismissable |
|-------------|------|--------|------|-----|-------------|
| `inapp-001` | Banner | "¡Bienvenido!" | "Completa tu perfil para empezar" | "Completar" | Sí |
| `inapp-005` | Badge + List item | "{{sender.name}}" | "{{message.preview}}" | Abrir chat | — |
| `inapp-{{ID}}` | {{TIPO}} | "{{TITULO}}" | "{{BODY}}" | "{{CTA}}" | Sí/No |

**Tipos de in-app:**

| Tipo | Uso | Persistencia |
|------|-----|--------------|
| Banner (top) | Alertas importantes | Hasta dismiss |
| Toast | Confirmaciones rápidas | Auto-dismiss 5s |
| Badge | Contador de pendientes | Hasta leer |
| List item | Notification center | Hasta leer/borrar |
| Modal | Críticas, requieren acción | Hasta acción |

---

## 7) Preferencias de usuario [OBL]

> **Activación:** Siempre obligatorio.

### 7.1 Estructura de preferencias [OBL]

| Categoría | Push | Email | SMS | Default | Editable |
|-----------|------|-------|-----|---------|----------|
| Seguridad | ✓ (locked) | ✓ (locked) | ✓ (locked) | On | No |
| Transaccional | ✓ | ✓ | ✗ | On | Canal sí |
| Social | ✓ | ✓ | ✗ | On | Sí |
| Engagement | ✓ | ✓ | ✗ | On | Sí |
| Marketing | ✗ | ✗ | ✗ | Off | Sí (opt-in) |

### 7.2 UI de preferencias [OBL]

| Sección | Controles |
|---------|-----------|
| Global | Master toggle "Pausar todas" |
| Por categoría | Toggle on/off |
| Por canal | Toggle por canal dentro de categoría |
| Quiet hours | Time picker inicio/fin |
| Frecuencia | [Todas / Resumen diario / Resumen semanal] |

### 7.3 Reglas de preferencias [OBL]

| Regla | Implementación |
|-------|----------------|
| Seguridad siempre activo | No se puede desactivar |
| Transaccional requerido | Se puede cambiar canal, no desactivar |
| Unsubscribe desde email | Un click, sin login requerido |
| Cambios aplicados | Inmediatamente |
| Sync cross-device | Sí |
---

*...Continuación de Parte 1 (Secciones 0-7)*

---

## 8) Notification Center (In-App) [COND]

> **Activación:** Incluir si el producto tiene centro de notificaciones.

### 8.1 Estructura del notification center [COND]

| Elemento | Implementación |
|----------|----------------|
| Acceso | Icono campana en header |
| Badge counter | Número de no leídas |
| Posición | [Drawer / Page / Modal] |
| Agrupación | [Por fecha / Por categoría / Sin agrupar] |

### 8.2 Funcionalidades [COND]

| Funcionalidad | Habilitada |
|---------------|------------|
| Marcar como leída | Sí |
| Marcar todas como leídas | Sí |
| Eliminar notificación | Sí/No |
| Eliminar todas | Sí/No |
| Filtrar por categoría | Sí/No |
| Buscar | Sí/No |

### 8.3 Retención [COND]

| Regla | Valor |
|-------|-------|
| Días de retención | {{DIAS}} días |
| Máximo notificaciones | {{NUM}} |
| Comportamiento al exceder | Eliminar más antiguas |

---

## 9) Lógica de envío [OBL]

> **Activación:** Siempre obligatorio.

### 9.1 Reglas de deduplicación [OBL]

| Regla | Implementación |
|-------|----------------|
| Misma notificación | No repetir en {{TIEMPO}} |
| Mismo trigger | Agrupar si ocurre {{NUM}} veces en {{TIEMPO}} |
| Batch | "Tienes {{count}} mensajes nuevos" |

### 9.2 Reglas de timing [OBL]

| Regla | Implementación |
|-------|----------------|
| Inmediatas | Seguridad, transaccionales críticas |
| Con delay | Engagement (esperar {{TIEMPO}} antes de enviar) |
| Scheduled | Marketing (hora óptima por timezone) |
| Quiet hours | No enviar {{HORARIO}}, excepto críticas |

### 9.3 Rate limiting [OBL]

| Límite | Valor |
|--------|-------|
| Por usuario/día | Max {{NUM}} notificaciones |
| Por usuario/hora | Max {{NUM}} notificaciones |
| Por categoría/día | Max {{NUM}} por categoría |
| Burst protection | Max {{NUM}} en {{TIEMPO}} |

### 9.4 Fallback y retry [OBL]

| Escenario | Comportamiento |
|-----------|----------------|
| Push falla | Retry {{NUM}} veces, luego fallback a {{CANAL}} |
| Email bounces | Marcar email inválido, no reintentar |
| SMS falla | Retry {{NUM}} veces |
| Usuario offline | Queue hasta {{TIEMPO}}, luego descartar/email |

---

## 10) Estados y tracking [OBL]

> **Activación:** Siempre obligatorio.

### 10.1 Estados de notificación [OBL]

| Estado | Descripción | Aplica a |
|--------|-------------|----------|
| `pending` | En cola para envío | Todos |
| `sent` | Enviada al provider | Todos |
| `delivered` | Confirmada entrega | Push, SMS |
| `opened` | Usuario abrió | Push, Email |
| `clicked` | Usuario hizo click en CTA | Todos |
| `dismissed` | Usuario descartó | Push, In-app |
| `failed` | Error de envío | Todos |
| `bounced` | Email rebotado | Email |
| `unsubscribed` | Usuario se dio de baja | Email, SMS |

### 10.2 Tracking por canal [OBL]

| Canal | Métricas tracked |
|-------|------------------|
| Push | sent, delivered, opened, clicked, dismissed |
| Email | sent, delivered, opened, clicked, bounced, unsubscribed |
| SMS | sent, delivered, clicked, unsubscribed |
| In-app | shown, clicked, dismissed |

---

## 11) APIs y datos [OBL]

> **Activación:** Siempre obligatorio.

### 11.1 Endpoints [OBL]

| Endpoint | Método | Uso | Auth |
|----------|--------|-----|------|
| `GET /notifications` | GET | Lista de notificaciones del usuario | User |
| `GET /notifications/unread-count` | GET | Contador de no leídas | User |
| `PATCH /notifications/:id/read` | PATCH | Marcar como leída | User |
| `POST /notifications/read-all` | POST | Marcar todas como leídas | User |
| `DELETE /notifications/:id` | DELETE | Eliminar notificación | User |
| `GET /notifications/preferences` | GET | Preferencias del usuario | User |
| `PATCH /notifications/preferences` | PATCH | Actualizar preferencias | User |
| `POST /notifications/send` | POST | Enviar notificación (interno) | Service |

### 11.2 Payload de notificación [OBL]

```json
{
  "id": "notif-uuid",
  "type": "notif-003",
  "category": "transactional",
  "title": "Pedido confirmado ✓",
  "body": "Tu pedido #12345 está en proceso.",
  "data": {
    "order_id": "12345",
    "action_url": "app://orders/12345"
  },
  "channels": ["push", "email"],
  "priority": "high",
  "created_at": "2025-01-15T10:30:00Z",
  "read_at": null,
  "clicked_at": null
}
```

### 11.3 Webhooks [COND]

| Evento | Payload | Uso |
|--------|---------|-----|
| `notification.delivered` | notif_id, channel, timestamp | Analytics |
| `notification.opened` | notif_id, channel, timestamp | Analytics |
| `notification.clicked` | notif_id, channel, action, timestamp | Analytics |
| `notification.failed` | notif_id, channel, error, timestamp | Alerting |

---

## 12) Estados UX [OBL]

> **Activación:** Siempre obligatorio. Referencia: `UXStates_Pack_{{PROYECTO}}`

### 12.1 Estados del notification center [OBL]

| Estado | UI |
|--------|-----|
| Loading | Skeleton de lista |
| Empty | "No tienes notificaciones" + ilustración |
| Error | "Error al cargar" + retry |
| Loaded | Lista de notificaciones |

### 12.2 Estados de preferencias [OBL]

| Estado | UI |
|--------|-----|
| Loading | Skeleton de toggles |
| Saving | Spinner en toggle cambiado |
| Saved | Toast "Preferencias guardadas" |
| Error | Toast error + retry |

---

## 13) Accesibilidad (A11Y) [OBL]

> **Activación:** Siempre obligatorio.

### 13.1 Notification center [OBL]

| Requisito | Implementación |
|-----------|----------------|
| Badge anunciado | "{{N}} notificaciones sin leer" |
| Lista navegable | Arrow keys |
| Acciones | Keyboard accessible |
| Focus | Focus en primera notificación al abrir |

### 13.2 Push/In-app [OBL]

| Requisito | Implementación |
|-----------|----------------|
| No depender solo de sonido | Vibración + visual |
| Dismissable | Swipe o botón X |
| Alto contraste | Texto legible |

---

## 14) Analytics / Instrumentación [OBL]

> **Activación:** Siempre obligatorio.

### 14.1 Eventos [OBL]

| Evento | Trigger | Payload |
|--------|---------|---------|
| `notification_sent` | Notificación enviada | `notif_id, type, channel, user_id` |
| `notification_delivered` | Confirmación de entrega | `notif_id, channel, latency_ms` |
| `notification_opened` | Usuario abrió | `notif_id, channel, time_to_open_ms` |
| `notification_clicked` | Click en CTA | `notif_id, channel, action` |
| `notification_dismissed` | Usuario descartó | `notif_id, channel` |
| `notification_failed` | Error de envío | `notif_id, channel, error_code` |
| `notification_center_opened` | Abrió notification center | `unread_count` |
| `preferences_updated` | Cambió preferencias | `category, channel, new_value` |
| `unsubscribed` | Opt-out | `channel, category, source` |

### 14.2 Métricas derivadas [OBL]

| Métrica | Cálculo |
|---------|---------|
| Delivery rate | `delivered / sent` |
| Open rate | `opened / delivered` |
| CTR | `clicked / opened` |
| Dismiss rate | `dismissed / delivered` |
| Opt-out rate | `unsubscribed / total_users` |
| Time to open | `avg(opened.timestamp - sent.timestamp)` |

---

## 15) QA / Casos de prueba [OBL]

> **Activación:** Siempre obligatorio.

### 15.1 Casos de envío [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TN-01 | Trigger de notificación | Notificación enviada a canales correctos |
| TN-02 | Preferencias respetadas | No enviar a canal desactivado |
| TN-03 | Quiet hours | No enviar durante quiet hours (excepto críticas) |
| TN-04 | Rate limiting | Bloquear si excede límite |
| TN-05 | Deduplicación | No duplicar en ventana de tiempo |

### 15.2 Casos de canales [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TC-01 | Push con app cerrada | Notificación recibida |
| TC-02 | Push click | Abre deep link correcto |
| TC-03 | Email delivery | Email recibido, formateado correctamente |
| TC-04 | Email unsubscribe | 1-click, sin login |
| TC-05 | In-app badge | Contador actualizado |

### 15.3 Casos de preferencias [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TP-01 | Toggle categoría off | No recibir notificaciones de esa categoría |
| TP-02 | Toggle canal off | No recibir en ese canal |
| TP-03 | Seguridad locked | No se puede desactivar |
| TP-04 | Sync cross-device | Preferencias aplicadas en todos los dispositivos |

---

## 16) Riesgos, supuestos y decisiones [OBL]

> **Activación:** Siempre obligatorio.

### 16.1 Riesgos [OBL]

| ID | Riesgo | Probabilidad | Impacto | Mitigación |
|----|--------|--------------|---------|------------|
| R-01 | Spam percibido | Media | Alto | Rate limiting, preferencias |
| R-02 | Push no entregados | Media | Medio | Fallback a email |
| R-03 | Email en spam | Media | Alto | SPF/DKIM, sender reputation |
| R-04 | Opt-out masivo | Baja | Alto | Segmentación, relevancia |

### 16.2 Supuestos [OBL]

| ID | Supuesto | Validado |
|----|----------|----------|
| S-01 | Providers seleccionados | Sí/No |
| S-02 | Templates de email aprobados | Sí/No |
| S-03 | Deep links configurados | Sí/No |

### 16.3 Decisiones pendientes [OBL]

| ID | Tema | Decisión | Responsable | Fecha |
|----|------|----------|-------------|-------|
| D-01 | Provider de push | {{DECISION}} | Tech | {{FECHA}} |
| D-02 | Rate limits finales | {{DECISION}} | PM + Tech | {{FECHA}} |
| D-03 | Quiet hours default | {{DECISION}} | UX | {{FECHA}} |

---

## 17) Checklist de aprobación [OBL]

### 17.1 Catálogo [OBL]

- [ ] Catálogo de notificaciones completo (§4)
- [ ] Templates por canal definidos (§6)
- [ ] Preferencias estructuradas (§7)

### 17.2 Técnica [OBL]

- [ ] Providers configurados
- [ ] APIs documentadas (§11)
- [ ] Rate limiting definido (§9)
- [ ] Fallbacks configurados

### 17.3 UX [OBL]

- [ ] Notification center especificado (si aplica)
- [ ] Estados definidos (§12)
- [ ] Accesibilidad validada (§13)

### 17.4 QA/Analytics [OBL]

- [ ] Casos de prueba documentados
- [ ] Analytics instrumentado (§14)

### 17.5 Firmas de aprobación [OBL]

| Rol | Nombre | Fecha | Status |
|-----|--------|-------|--------|
| PM/PO | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| UX/UI | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| Tech Lead | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| QA | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |

---

## 18) Particularidades del proyecto [OPC]

### 18.1 Notificaciones custom

| Notif ID | Particularidad |
|----------|----------------|
| {{ID}} | {{PARTICULARIDAD}} |

### 18.2 Excepciones al estándar

| Sección | Excepción | Justificación |
|---------|-----------|---------------|
| {{SECCION}} | {{EXCEPCION}} | {{JUSTIFICACION}} |

---

## 📋 ANEXOS RELACIONADOS

- [ ] **UXStates** → Estados de notification center
- [ ] **AdminRBAC** → Configuración de notificaciones por admin
- [ ] **Form** → UI de preferencias

---

## 🔁 GUÍA OPERATIVA PARA AGENTES

### Cómo usar este template:

1. **Copiar** el template
2. **Completar §4** (Catálogo de notificaciones) — sección núcleo
3. **Definir §6** (Templates de contenido)
4. **Configurar §7** (Preferencias)
5. **Validar** con checklist (§17)

### Secciones núcleo (mínimo viable):

- §0 Metadatos
- §3 Canales
- §4 **Catálogo de notificaciones** ← NÚCLEO
- §5 Detalle por notificación
- §6 Templates de contenido
- §7 Preferencias
- §9 Lógica de envío
- §14 Analytics
- §17 Checklist

### Validación cruzada:

- Cada notificación en §4 debe tener templates en §6
- Cada categoría en §4.2 debe tener regla en §7
- Cada canal en §3 debe tener provider
- Rate limits deben ser consistentes con UX

### Red flags a evitar:

- ❌ Notificaciones sin categoría clara
- ❌ Sin rate limiting (spam)
- ❌ Sin preferencias de usuario
- ❌ Seguridad desactivable
- ❌ Sin fallback cuando canal falla
- ❌ Sin unsubscribe en emails
- ❌ Sin quiet hours

---

> **Fin del template**  
> **Versión:** 2.0  
> **Última actualización:** {{FECHA_ACTUALIZACION}}
