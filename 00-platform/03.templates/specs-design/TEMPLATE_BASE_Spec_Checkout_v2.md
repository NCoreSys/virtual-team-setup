# 💳 TEMPLATE BASE — SPEC CHECKOUT / PAGOS / SUSCRIPCIÓN

> **Versión:** 2.0 (Estandarizada para agentes)  
> **Tipo:** P3 — Conditional  
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

- ✅ **Flujo de compra** de productos o servicios
- ✅ **Suscripciones** (SaaS, membresías)
- ✅ **Upgrades/Downgrades** de planes
- ✅ **Pagos únicos** (one-time purchase)
- ✅ **Checkout e-commerce**
- ❌ Carrito de compras sin pago → usar AppScreen
- ❌ Billing portal (gestión post-compra) → usar EntityDetail

---

# ESPECIFICACIÓN DE CHECKOUT / PAGOS

---

## 0) Metadatos del documento [OBL]

> **Activación:** Siempre obligatorio.

| Campo | Valor |
|-------|-------|
| **Nombre del documento** | Spec_Checkout_{{NOMBRE_FLUJO}}_{{VERSION}} |
| **Proyecto** | {{NOMBRE_PROYECTO}} |
| **Módulo / Feature** | {{MODULO}} (ej: Checkout, Billing, Subscription) |
| **Flujo** | [Elegir: Compra única / Suscripción / Upgrade / Renewal / Downgrade] |
| **ID técnico** | `pay-{{NUM}}-{{SLUG}}` (ej: `pay-01-subscribe-pro`) |
| **Ruta(s)** | {{RUTAS}} (ej: `/checkout`, `/billing/upgrade`) |
| **Contexto** | [Elegir: Standalone / Landing → Checkout / App → Upgrade] |
| **Versión** | {{VERSION}} |
| **Estado** | [Elegir: Draft / Review / Approved / Deprecated] |
| **Prioridad** | [Elegir: Crítica / Alta / Media / Baja] |
| **Fecha** | {{FECHA_YYYY-MM-DD}} |
| **Owner (PM/PO/Growth)** | {{NOMBRE_OWNER}} |
| **UX/UI Owner** | {{NOMBRE_UX}} |
| **Tech Lead** | {{NOMBRE_TECH}} |
| **Finance/Legal Owner** | {{NOMBRE_FINANCE}} |
| **QA Owner** | {{NOMBRE_QA}} |

---

## 1) Propósito del checkout [OBL]

> **Activación:** Siempre obligatorio.

### 1.1 Descripción general [OBL]

Este flujo permite a **{{TIPO_USUARIO}}** completar **{{TIPO_COMPRA}}** de **{{PRODUCTO_PLAN}}**.

| Campo | Valor |
|-------|-------|
| **Tipo de transacción** | [Elegir: Compra única / Suscripción recurrente / Upgrade / Trial → Paid] |
| **Producto/Plan** | {{PRODUCTO}} |
| **Criticidad** | Alta (involucra dinero) |

### 1.2 Objetivo de negocio [OBL]

1. {{OBJETIVO_1}} (ej: Maximizar conversión de checkout)
2. {{OBJETIVO_2}} (ej: Reducir tasa de fallas de pago)
3. {{OBJETIVO_3}} (ej: Minimizar chargebacks)
4. {{OBJETIVO_4}} (ej: Cumplimiento fiscal/legal)

### 1.3 Objetivo UX [OBL]

- Claridad del precio total (sin sorpresas)
- Confianza y seguridad percibida
- Manejo de errores accionable
- Fricción mínima (menos pasos posibles)

### 1.4 KPIs [OBL]

| Métrica | Valor objetivo | Valor crítico |
|---------|----------------|---------------|
| Conversion rate (checkout started → success) | > {{VALOR}}% | < {{VALOR}}% |
| Payment failure rate | < {{VALOR}}% | > {{VALOR}}% |
| Drop-off por step | < {{VALOR}}% por step | > {{VALOR}}% |
| Time to complete | < {{VALOR}}s | > {{VALOR}}s |
| Refund rate | < {{VALOR}}% | > {{VALOR}}% |

---

## 2) Alcance (Scope) [OBL]

> **Activación:** Siempre obligatorio.

### 2.1 Incluye (In Scope) [OBL]

- {{INCLUYE_1}} (ej: Selección de plan/producto)
- {{INCLUYE_2}} (ej: Resumen de compra con breakdown)
- {{INCLUYE_3}} (ej: Captura de método de pago)
- {{INCLUYE_4}} (ej: Cálculo de impuestos y descuentos)
- {{INCLUYE_5}} (ej: Confirmación y receipt)
- {{INCLUYE_6}} (ej: Manejo de errores y retry)

### 2.2 No incluye (Out of Scope) [OBL]

- {{EXCLUYE_1}} (ej: Disputas/chargebacks workflow)
- {{EXCLUYE_2}} (ej: Billing portal post-compra)

### 2.3 Dependencias [OBL]

| Tipo | Dependencia | Estado | Owner |
|------|-------------|--------|-------|
| Payment Provider | {{PROVIDER}} (ej: Stripe, Adyen, MercadoPago) | [Pendiente/Listo] | {{OWNER}} |
| Pricing Service | {{SERVICIO}} | [Pendiente/Listo] | {{OWNER}} |
| Tax Service | {{SERVICIO}} | [Pendiente/Listo] | {{OWNER}} |
| Antifraud | {{SERVICIO}} | [Pendiente/Listo] | {{OWNER}} |
| Email/Receipts | {{SERVICIO}} | [Pendiente/Listo] | {{OWNER}} |

---

## 3) Usuarios, roles y permisos [OBL]

> **Activación:** Siempre obligatorio.

### 3.1 Matriz de permisos [OBL]

| Rol | Puede comprar | Ver pricing | Ver invoices | Admin billing | Cancelar/Refund |
|-----|---------------|-------------|--------------|---------------|-----------------|
| {{ROL_USER}} | ✅ | ✅ | ✅/❌ | ❌ | ❌ |
| {{ROL_ADMIN}} | ✅ | ✅ | ✅ | ✅ | ✅ |
| {{ROL_GUEST}} | ✅/❌ | ✅ | ❌ | ❌ | ❌ |

### 3.2 Reglas de compra [OBL]

| Regla | Implementación |
|-------|----------------|
| Autenticación requerida | [Sí / No / Opcional (guest checkout)] |
| Email verificado | [Sí / No] |
| Límite de compras | {{LIMITE}} |
| País/región permitido | {{PAISES}} |

---

## 4) Oferta y catálogo (Product/Plan Catalog) [OBL] — **SECCIÓN NÚCLEO**

> **Activación:** Siempre obligatorio.

### 4.1 Catálogo de productos/planes [OBL]

| SKU/Plan ID | Nombre | Tipo | Periodicidad | Precio base | Moneda | Trial | Límites/Features | Notas |
|-------------|--------|------|--------------|------------:|--------|-------|------------------|-------|
| `plan-free` | Free | subscription | — | 0 | {{MONEDA}} | — | {{LIMITES}} | Default |
| `plan-pro` | Pro | subscription | monthly | {{PRECIO}} | {{MONEDA}} | {{TRIAL_DIAS}}d | {{LIMITES}} | Popular |
| `plan-pro-annual` | Pro Annual | subscription | annual | {{PRECIO}} | {{MONEDA}} | {{TRIAL_DIAS}}d | {{LIMITES}} | Descuento |
| `plan-enterprise` | Enterprise | subscription | annual | Custom | {{MONEDA}} | — | {{LIMITES}} | Contact sales |
| `addon-{{ID}}` | {{NOMBRE}} | one-time | — | {{PRECIO}} | {{MONEDA}} | — | {{LIMITES}} | {{NOTAS}} |
| `{{SKU}}` | {{NOMBRE}} | {{TIPO}} | {{PERIODO}} | {{PRECIO}} | {{MONEDA}} | {{TRIAL}} | {{LIMITES}} | {{NOTAS}} |

### 4.2 Reglas de elegibilidad [OBL]

| Transición | Permitida | Reglas |
|------------|-----------|--------|
| Free → Pro | Sí | — |
| Pro Monthly → Pro Annual | Sí | Prorrateado |
| Pro → Enterprise | Sí | Contact sales |
| Pro → Free (downgrade) | Sí/No | {{REGLAS}} |
| Trial → Paid | Sí | Auto al terminar trial |
| {{TRANSICION}} | Sí/No | {{REGLAS}} |

### 4.3 Restricciones geográficas [COND]

> **Activación:** Incluir si hay restricciones por país.

| Plan/Producto | Países permitidos | Países bloqueados |
|---------------|-------------------|-------------------|
| {{PLAN}} | {{PAISES}} | {{PAISES}} |

---

## 5) Pricing, impuestos y descuentos [OBL] — **SECCIÓN NÚCLEO**

> **Activación:** Siempre obligatorio.

### 5.1 Componentes del precio [OBL]

| Componente | Descripción | Cálculo |
|------------|-------------|---------|
| Subtotal | Precio base del plan/producto | `plan.price` |
| Descuento | Cupón o promo aplicada | `- coupon.amount` |
| Impuestos | IVA/VAT/Sales tax | `+ (subtotal - descuento) * tax_rate` |
| Fees | Cargos adicionales (si aplica) | `+ fee.amount` |
| **Total** | Monto a cobrar | `subtotal - descuento + impuestos + fees` |

### 5.2 Reglas fiscales [OBL]

| País/Región | Impuesto | Tasa | Incluido en precio | Factura requerida |
|-------------|----------|------|--------------------|-------------------|
| {{PAIS}} | {{TIPO}} (ej: IVA) | {{TASA}}% | Sí/No | Sí/No |
| {{PAIS}} | {{TIPO}} | {{TASA}}% | Sí/No | Sí/No |

### 5.3 Datos fiscales requeridos [COND]

> **Activación:** Incluir si se requiere facturación.

| Dato | Requerido | Validación |
|------|-----------|------------|
| Nombre/Razón social | Sí | — |
| RFC/Tax ID | Sí/No | {{REGEX}} |
| Dirección | Sí | — |
| Código postal | Sí | {{REGEX}} |
| {{DATO}} | Sí/No | {{VALIDACION}} |

### 5.4 Cupones y promociones [COND]

> **Activación:** Incluir si hay sistema de cupones.

| Coupon ID | Nombre | Tipo | Valor | Aplica a | Condiciones | Expira | Stackable |
|-----------|--------|------|-------|----------|-------------|--------|-----------|
| `WELCOME10` | Bienvenida | Porcentaje | -10% | Todos | Primera compra | {{FECHA}} | No |
| `ANNUAL20` | Descuento anual | Porcentaje | -20% | Planes anuales | — | — | No |
| `{{ID}}` | {{NOMBRE}} | {{TIPO}} | {{VALOR}} | {{APLICA}} | {{CONDICIONES}} | {{EXPIRA}} | Sí/No |

### 5.5 Reglas de display [OBL]

| Regla | Implementación |
|-------|----------------|
| Mostrar breakdown | Sí (subtotal, descuento, impuestos, total) |
| Moneda | Detectar por país o permitir selección |
| Formato de precio | {{FORMATO}} (ej: $1,234.56 MXN) |
| Redondeo | {{REGLA}} (ej: 2 decimales) |
| Precio tachado (original) | Sí si hay descuento |

---

## 6) Flujo del checkout (Journey) [OBL]

> **Activación:** Siempre obligatorio.

### 6.1 Estructura del flujo [OBL]

| Tipo | Cuándo usar | Seleccionado |
|------|-------------|--------------|
| **Single page** | Checkout simple, pocos campos | ☐ |
| **Multi-step (Wizard)** | Checkout complejo, múltiples secciones | ☐ |
| **Embedded** | Checkout dentro de otra página | ☐ |

### 6.2 Mapa de pasos [OBL]

| Paso | Nombre | Objetivo | Inputs | Output | Validaciones | Skippable |
|-----:|--------|----------|--------|--------|--------------|-----------|
| 1 | Plan | Seleccionar plan | Radio/Cards | `plan_id` | Requerido | No |
| 2 | Billing | Datos de facturación | Form | `billing_profile` | Format, required | [Si ya existe] |
| 3 | Payment | Método de pago | Card/Wallet | `payment_method` | Card valid, 3DS | No |
| 4 | Review | Confirmar compra | — | `order` | — | No |
| {{N}} | {{NOMBRE}} | {{OBJETIVO}} | {{INPUTS}} | {{OUTPUT}} | {{VALIDACIONES}} | Sí/No |

### 6.3 Entry points [OBL]

| Entry point | Origen | Parámetros | Comportamiento |
|-------------|--------|------------|----------------|
| Pricing page | `/pricing` | `plan_id` | Pre-selecciona plan |
| Upgrade CTA | App | `plan_id`, `current_plan` | Muestra upgrade |
| Landing | `/landing` | `coupon` | Aplica cupón |
| {{ENTRY}} | {{ORIGEN}} | {{PARAMS}} | {{COMPORTAMIENTO}} |

### 6.4 Exit points [OBL]

| Resultado | Destino | Comportamiento |
|-----------|---------|----------------|
| Success | `/checkout/success` o `/dashboard` | Acceso habilitado |
| Cancel | Página anterior | Sin cambios |
| Abandon | — | Recovery email (opcional) |

---

## 7) Métodos de pago [OBL]

> **Activación:** Siempre obligatorio.

### 7.1 Métodos soportados [OBL]

| Método | Habilitado | Países | Provider | Notas |
|--------|------------|--------|----------|-------|
| Tarjeta de crédito | ✅ | Global | {{PROVIDER}} | Visa, MC, Amex |
| Tarjeta de débito | ✅ | Global | {{PROVIDER}} | — |
| Apple Pay | Sí/No | {{PAISES}} | {{PROVIDER}} | Safari, iOS |
| Google Pay | Sí/No | {{PAISES}} | {{PROVIDER}} | Chrome, Android |
| PayPal | Sí/No | {{PAISES}} | PayPal | — |
| OXXO/SPEI | Sí/No | México | {{PROVIDER}} | Cash/Transfer |
| Invoice/Net terms | Sí/No | Enterprise | — | Aprobación requerida |
| {{METODO}} | Sí/No | {{PAISES}} | {{PROVIDER}} | {{NOTAS}} |

### 7.2 Reglas por método [OBL]

| Método | Monto mínimo | Monto máximo | Requiere 3DS | Tiempo de confirmación |
|--------|--------------|--------------|--------------|------------------------|
| Tarjeta | {{MIN}} | {{MAX}} | Sí/No | Inmediato |
| OXXO | {{MIN}} | {{MAX}} | No | 24-72h |
| {{METODO}} | {{MIN}} | {{MAX}} | Sí/No | {{TIEMPO}} |

### 7.3 UI de captura de pago [OBL]

| Elemento | Implementación |
|----------|----------------|
| Card number | Input masked (•••• •••• •••• 1234) |
| Expiry | MM/YY |
| CVC | 3-4 dígitos, masked |
| Cardholder name | Texto |
| Billing address | [Completo / Solo país / ZIP] |
| Save card | Checkbox (para futuras compras) |

---

## 8) Seguridad, antifraude y cumplimiento [OBL]

> **Activación:** Siempre obligatorio.

### 8.1 PCI Compliance [OBL]

| Requisito | Implementación |
|-----------|----------------|
| Nivel de PCI | SAQ-A (hosted fields / redirect) |
| Tokenización | Sí — nunca almacenar datos de tarjeta |
| Hosted fields | [Stripe Elements / Adyen Components / etc.] |

### 8.2 3D Secure [COND]

> **Activación:** Incluir si se usa 3DS.

| Configuración | Valor |
|---------------|-------|
| Versión | 3DS2 |
| Trigger | [Siempre / Solo si banco requiere / Por monto] |
| Fallback si falla | [Permitir sin 3DS / Rechazar] |
| UI | [Redirect / Modal / Inline] |

### 8.3 Antifraude [COND]

> **Activación:** Incluir si hay sistema antifraude.

| Medida | Implementación |
|--------|----------------|
| Radar/Fraud detection | {{SERVICIO}} |
| Rate limiting | {{LIMITE}} intentos por IP/usuario |
| Velocity checks | {{REGLAS}} |
| Manual review | [Para montos > {{VALOR}} / Scores altos] |

### 8.4 Cumplimiento legal [OBL]

| Requisito | Implementación |
|-----------|----------------|
| Términos y condiciones | Checkbox antes de pagar |
| Política de cancelación | Visible en checkout |
| Derecho de retiro | {{DIAS}} días (si aplica) |
| GDPR/Privacidad | Link a política |
---

*...Continuación de Parte 1 (Secciones 0-8)*

---

## 9) Confirmación, recibos e invoices [OBL]

> **Activación:** Siempre obligatorio.

### 9.1 Pantalla de éxito [OBL]

| Elemento | Contenido |
|----------|-----------|
| Título | "¡Pago exitoso!" / "Bienvenido a {{PLAN}}" |
| Número de orden | `#{{ORDER_ID}}` |
| Resumen de compra | Plan, precio, periodo |
| Próximos pasos | {{PASOS}} (ej: "Ya puedes acceder a...") |
| CTA principal | "Ir a {{DESTINO}}" |
| CTA secundario | "Ver recibo" / "Descargar factura" |

### 9.2 Email de confirmación [OBL]

| Campo | Valor |
|-------|-------|
| Trigger | Inmediato post-pago exitoso |
| Subject | "{{SUBJECT}}" (ej: "Confirmación de tu compra") |
| Contenido | Resumen de compra, número de orden, link a factura |
| Reply-to | {{EMAIL}} |

### 9.3 Recibo/Invoice [OBL]

| Elemento | Incluido |
|----------|----------|
| Número de factura | Sí |
| Fecha | Sí |
| Datos del comprador | Sí |
| Datos del vendedor | Sí |
| Breakdown de precio | Sí |
| Impuestos desglosados | Sí |
| Método de pago (últimos 4 dígitos) | Sí |
| Descarga PDF | Sí |
| Acceso en billing portal | Sí |

---

## 10) Estados y error handling [OBL] — **CRÍTICO**

> **Activación:** Siempre obligatorio. El manejo de errores en pagos es crítico.

### 10.1 Estados del checkout [OBL]

| Estado | Trigger | UI |
|--------|---------|-----|
| `idle` | Página cargada | Form listo |
| `loading` | Cargando datos (planes, precios) | Skeleton |
| `validating` | Validando campos | Inline validation |
| `processing` | Enviando pago | Spinner + "Procesando pago..." |
| `awaiting_3ds` | Esperando 3DS | Modal/redirect 3DS |
| `awaiting_confirmation` | Pago async (OXXO, transfer) | Instrucciones |
| `success` | Pago exitoso | Success page |
| `failed` | Pago fallido | Error + opciones |

### 10.2 Tipos de error y handling [OBL]

| Error | Código | Mensaje usuario | Acción | Retry |
|-------|--------|-----------------|--------|-------|
| Tarjeta declinada | `card_declined` | "Tu tarjeta fue declinada. Intenta con otra." | Cambiar método | Sí |
| Fondos insuficientes | `insufficient_funds` | "Fondos insuficientes. Intenta con otra tarjeta." | Cambiar método | Sí |
| Tarjeta expirada | `expired_card` | "Tu tarjeta está expirada." | Actualizar datos | Sí |
| CVC inválido | `incorrect_cvc` | "El código de seguridad es incorrecto." | Corregir CVC | Sí |
| 3DS fallido | `3ds_failed` | "No pudimos verificar tu identidad. Intenta de nuevo." | Reintentar | Sí |
| 3DS abandonado | `3ds_abandoned` | "Verificación cancelada." | Reintentar | Sí |
| Timeout | `timeout` | "El proceso tardó demasiado. Intenta de nuevo." | Reintentar | Sí |
| Proveedor caído | `provider_unavailable` | "Problemas técnicos. Intenta en unos minutos." | Esperar + retry | Sí |
| Precio cambió | `price_mismatch` | "El precio ha cambiado. Revisa el nuevo total." | Refrescar | Sí |
| Cupón inválido | `coupon_invalid` | "Este cupón no es válido o ha expirado." | Quitar cupón | — |
| Cupón no aplicable | `coupon_not_applicable` | "Este cupón no aplica para este plan." | Quitar cupón | — |
| Fraud detected | `fraud_suspected` | "No pudimos procesar tu pago. Contacta soporte." | Contactar soporte | No |
| {{ERROR}} | `{{CODE}}` | "{{MENSAJE}}" | {{ACCION}} | Sí/No |

### 10.3 Reglas de retry [OBL]

| Regla | Implementación |
|-------|----------------|
| Preservar datos del form | Sí (no perder lo ingresado) |
| Permitir cambiar método | Sí |
| Límite de reintentos | {{LIMITE}} por sesión |
| Backoff | {{TIEMPO}} entre reintentos |
| Link a soporte | Visible después de {{N}} fallos |

### 10.4 Recovery de abandoned checkout [OPC]

| Mecanismo | Trigger | Acción |
|-----------|---------|--------|
| Email recovery | {{TIEMPO}} después de abandon | Email con link al checkout |
| Notificación in-app | Próximo login | Banner recordatorio |

---

## 11) Accesibilidad (A11Y) [OBL]

> **Activación:** Siempre obligatorio.

### 11.1 Formularios de pago [OBL]

| Requisito | Implementación |
|-----------|----------------|
| Labels asociados | `<label for="">` en todos los inputs |
| Error messages | `aria-describedby` + `aria-invalid` |
| Required fields | `aria-required="true"` |
| Autocomplete | `autocomplete="cc-number"` etc. |

### 11.2 Estados y feedback [OBL]

| Evento | Anuncio |
|--------|---------|
| Validación error | Error leído por screen reader |
| Processing | "Procesando pago, por favor espera" |
| Success | "Pago completado exitosamente" |
| Failure | Error + opciones |

### 11.3 Navegación [OBL]

| Requisito | Implementación |
|-----------|----------------|
| Tab order | Lógico (campos → botón) |
| Focus visible | En todos los elementos |
| Skip links | Si hay header/nav |

---

## 12) Analytics / Instrumentación [OBL]

> **Activación:** Siempre obligatorio.

### 12.1 Eventos [OBL]

| Evento | Trigger | Payload |
|--------|---------|---------|
| `checkout_view` | Página visible | `entry_point, plan_id, user_id` |
| `checkout_step_view` | Step visible | `step_number, step_name` |
| `checkout_step_complete` | Step completado | `step_number, step_name, duration_ms` |
| `plan_selected` | Selección de plan | `plan_id, plan_price, currency` |
| `coupon_applied` | Cupón aplicado | `coupon_id, discount_amount` |
| `coupon_failed` | Cupón rechazado | `coupon_id, error_code` |
| `payment_method_selected` | Método seleccionado | `method_type` |
| `checkout_submit` | Click en pagar | `plan_id, total, currency, payment_method` |
| `checkout_processing` | Pago en proceso | `plan_id` |
| `checkout_success` | Pago exitoso | `plan_id, order_id, total, currency, payment_method` |
| `checkout_failed` | Pago fallido | `plan_id, error_code, error_message` |
| `checkout_abandon` | Salida sin completar | `step_number, had_interaction` |
| `checkout_retry` | Reintento de pago | `attempt_number, previous_error` |

### 12.2 Métricas de funnel [OBL]

| Métrica | Cálculo |
|---------|---------|
| Checkout conversion rate | `checkout_success / checkout_view` |
| Step completion rate | `step_N_complete / step_N_view` |
| Drop-off rate por step | `1 - step_completion_rate` |
| Payment success rate | `checkout_success / checkout_submit` |
| Average time to complete | `avg(success.timestamp - view.timestamp)` |
| Retry rate | `checkout_retry / checkout_failed` |
| Recovery rate | `success_after_abandon / checkout_abandon` |

### 12.3 Revenue tracking [OBL]

| Evento | Datos |
|--------|-------|
| `purchase` (GA4/Meta) | `transaction_id, value, currency, items` |
| `subscription_start` | `plan_id, mrr, currency` |

---

## 13) Performance [OBL]

> **Activación:** Siempre obligatorio.

### 13.1 Objetivos [OBL]

| Métrica | Objetivo | Crítico |
|---------|----------|---------|
| Page load (LCP) | < {{VALOR}}s | > {{VALOR}}s |
| Time to interactive | < {{VALOR}}s | > {{VALOR}}s |
| Payment processing | < {{VALOR}}s (p95) | > {{VALOR}}s |

### 13.2 Estrategias [OBL]

| Estrategia | Implementación |
|------------|----------------|
| Minimizar scripts terceros | Solo payment provider |
| Lazy load payment form | Cargar después de step anterior |
| Preload pricing | Cache o prefetch |
| No bloquear UI durante processing | Spinner + mensajes |
| Manejar latencia del provider | Timeout + retry UI |

---

## 14) Responsive [OBL]

> **Activación:** Siempre obligatorio.

### 14.1 Comportamiento por breakpoint [OBL]

| Breakpoint | Layout |
|------------|--------|
| Mobile | Single column, sticky CTA |
| Tablet | Single column o 2 columns |
| Desktop | 2 columns (form + summary) |

### 14.2 Elementos sticky [OBL]

| Elemento | Mobile | Desktop |
|----------|--------|---------|
| Order summary | Colapsable arriba | Sticky sidebar |
| CTA "Pagar" | Sticky bottom | Inline |

---

## 15) QA / Casos de prueba [OBL]

> **Activación:** Siempre obligatorio.

### 15.1 Casos de pago [OBL]

| ID | Caso | Resultado esperado | Prioridad |
|----|------|-------------------|-----------|
| TP-01 | Pago exitoso con tarjeta | Success page + email | Crítica |
| TP-02 | Pago con 3DS exitoso | 3DS + success | Crítica |
| TP-03 | Tarjeta declinada | Error + retry | Crítica |
| TP-04 | 3DS fallido | Error + retry | Alta |
| TP-05 | Timeout de proveedor | Error + retry | Alta |
| TP-06 | Wallet (Apple/Google Pay) | Success | Alta |

### 15.2 Casos de pricing [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TC-01 | Cupón válido aplicado | Descuento reflejado |
| TC-02 | Cupón inválido | Error mensaje |
| TC-03 | Impuestos por país | Cálculo correcto |
| TC-04 | Cambio de plan mid-checkout | Precio actualizado |

### 15.3 Casos de edge [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TE-01 | Doble submit | Bloquear segundo |
| TE-02 | Back button durante processing | Warning o bloquear |
| TE-03 | Sesión expira | Redirect a login |
| TE-04 | Precio cambia durante checkout | Notificar + actualizar |

### 15.4 Casos de accesibilidad [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TA-01 | Completar checkout con keyboard | Funcional |
| TA-02 | Screen reader en errores | Errores anunciados |
| TA-03 | Autocomplete de tarjeta | Funcional |

---

## 16) Riesgos, supuestos y decisiones [OBL]

> **Activación:** Siempre obligatorio.

### 16.1 Riesgos identificados [OBL]

| ID | Riesgo | Probabilidad | Impacto | Mitigación |
|----|--------|--------------|---------|------------|
| R-01 | Proveedor de pagos caído | Baja | Crítico | Fallback, monitoreo |
| R-02 | Fraude/chargebacks | Media | Alto | Antifraude, 3DS |
| R-03 | Errores fiscales | Media | Alto | Tax service, testing |
| R-04 | {{RIESGO}} | {{PROB}} | {{IMPACTO}} | {{MITIGACION}} |

### 16.2 Supuestos [OBL]

| ID | Supuesto | Validado |
|----|----------|----------|
| S-01 | Proveedor de pagos seleccionado | Sí/No |
| S-02 | Estructura de pricing definida | Sí/No |
| S-03 | Requisitos fiscales claros | Sí/No |
| S-04 | {{SUPUESTO}} | Sí/No |

### 16.3 Decisiones pendientes [OBL]

| ID | Tema | Decisión | Responsable | Fecha |
|----|------|----------|-------------|-------|
| D-01 | Proveedor de pagos | {{DECISION}} | Tech + Finance | {{FECHA}} |
| D-02 | Impuestos por país | {{DECISION}} | Finance + Legal | {{FECHA}} |
| D-03 | Guest checkout | {{DECISION}} | PM + UX | {{FECHA}} |

---

## 17) Checklist de aprobación [OBL]

> **Activación:** Siempre obligatorio.

### 17.1 Producto [OBL]

- [ ] Catálogo de planes definido (§4)
- [ ] Pricing y taxes definidos (§5)
- [ ] Flujo de checkout mapeado (§6)
- [ ] Métodos de pago definidos (§7)

### 17.2 Seguridad/Legal [OBL]

- [ ] PCI compliance verificado
- [ ] 3DS configurado (si aplica)
- [ ] Términos y condiciones aprobados
- [ ] Política de cancelación definida

### 17.3 UX/Técnica [OBL]

- [ ] Error handling completo (§10)
- [ ] Success page y emails definidos (§9)
- [ ] Responsive especificado
- [ ] Accesibilidad validada

### 17.4 QA/Analytics [OBL]

- [ ] Casos de prueba documentados
- [ ] Funnel analytics configurado
- [ ] Revenue tracking implementado

### 17.5 Firmas de aprobación [OBL]

| Rol | Nombre | Fecha | Status |
|-----|--------|-------|--------|
| PM/PO/Growth | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| UX/UI | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| Tech Lead | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| Finance/Legal | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| QA | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |

---

## 18) Particularidades del proyecto [OPC]

> **Activación:** Usar para configuraciones específicas.

### 18.1 Excepciones al estándar

| Sección | Excepción | Justificación |
|---------|-----------|---------------|
| {{SECCION}} | {{EXCEPCION}} | {{JUSTIFICACION}} |

### 18.2 Notas adicionales

{{NOTAS}}

---

## 📋 ANEXOS RELACIONADOS

> Marcar los anexos que aplican:

- [ ] **Wizard** → Si checkout es multi-step (usar TEMPLATE_BASE_Spec_Wizard)
- [ ] **Form** → Para formularios de billing/payment
- [ ] **UXStates** → Referencia a estándar global

---

## 🔁 GUÍA OPERATIVA PARA AGENTES

### Cómo usar este template:

1. **Copiar** el template
2. **Completar §4** (Product Catalog) y **§5** (Pricing) — secciones núcleo
3. **Definir §7** (Métodos de pago) con el proveedor
4. **Completar §10** (Error handling) — crítico para pagos
5. **Reemplazar** placeholders `{{...}}`
6. **Validar** con Finance/Legal antes de lanzar

### Secciones núcleo (mínimo viable):

- §0 Metadatos
- §1 Propósito
- §4 **Product/Plan Catalog** ← NÚCLEO
- §5 **Pricing, taxes, descuentos** ← NÚCLEO
- §6 Flujo
- §7 Métodos de pago
- §8 Seguridad
- §9 Confirmación
- §10 **Error handling** ← CRÍTICO
- §12 Analytics
- §17 Checklist

### Validación cruzada:

- Cada plan en §4 debe tener precio en §5
- Cada método de pago en §7 debe tener reglas
- Cada error en §10 debe tener mensaje y acción
- El funnel en §12 debe cubrir todos los steps de §6

### Red flags a evitar:

- ❌ Checkout sin catálogo de errores detallado
- ❌ Sin 3DS en pagos con tarjeta
- ❌ Sin breakdown de precio (solo total)
- ❌ Sin preservar datos en retry
- ❌ Sin límite de reintentos
- ❌ Sin validación de Finance/Legal
- ❌ Sin funnel analytics

---

> **Fin del template**  
> **Versión:** 2.0  
> **Última actualización:** {{FECHA_ACTUALIZACION}}
