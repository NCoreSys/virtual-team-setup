# 🧾 TEMPLATE BASE — SPEC FORM (Formularios Simple/Complex)

> **Versión:** 2.0 (Estandarizada para agentes)  
> **Tipo:** P1 — Core  
> **Última actualización:** {{FECHA_ACTUALIZACION}}

---

## 🔖 GUÍA DE USO DEL TEMPLATE

### Marcadores de obligatoriedad

| Marcador | Significado | Regla |
|----------|-------------|-------|
| `[OBL]` | **Obligatorio** | Siempre debe completarse |
| `[OPC]` | **Opcional** | Completar si aplica al proyecto |
| `[COND]` | **Condicional** | Completar solo si se cumple la condición indicada |

### Placeholders

- `{{NOMBRE}}` → Reemplazar con valor específico del proyecto
- `[Elegir: opción1 / opción2]` → Seleccionar una opción
- `[Listar...]` → Agregar items según aplique

### Cuándo usar este template

- ✅ Formulario con **3+ campos** y lógica de validación
- ✅ Formulario crítico para conversión o flujo de negocio
- ✅ Formulario con integraciones (CRM, API, webhook)
- ❌ Formulario trivial (1-2 campos simples) → documentar inline en template principal

---

# ESPECIFICACIÓN DE FORMULARIO

---

## 0) Metadatos del documento [OBL]

> **Activación:** Siempre obligatorio.

| Campo | Valor |
|-------|-------|
| **Nombre del documento** | Spec_Form_{{NOMBRE_FORM}}_{{VERSION}} |
| **Proyecto** | {{NOMBRE_PROYECTO}} |
| **Módulo / Feature** | {{NOMBRE_MODULO}} |
| **Formulario** | {{NOMBRE_FORM}} |
| **ID técnico** | `form-{{NUM}}-{{SLUG}}` (ej: `form-01-profile-update`) |
| **Contexto** | [Elegir: AppScreen / Landing / Wizard Step / Modal / Admin / Standalone] |
| **Versión** | {{VERSION}} |
| **Estado** | [Elegir: Draft / Review / Approved / Deprecated] |
| **Prioridad** | [Elegir: Crítica / Alta / Media / Baja] |
| **Fecha** | {{FECHA_YYYY-MM-DD}} |
| **Owner (PM/PO/Growth)** | {{NOMBRE_OWNER}} |
| **UX/UI Owner** | {{NOMBRE_UX}} |
| **Tech Lead** | {{NOMBRE_TECH}} |
| **QA Owner** | {{NOMBRE_QA}} |
| **Legal/Compliance** | {{NOMBRE_LEGAL}} (si aplica) |

---

## 1) Propósito del formulario [OBL]

> **Activación:** Siempre obligatorio.

### 1.1 Descripción general [OBL]

Este formulario permite a **{{TIPO_USUARIO}}** realizar **{{ACCION}}**.

| Campo | Valor |
|-------|-------|
| **Pantalla/flujo donde vive** | {{PANTALLA_O_FLUJO}} |
| **Objetivo principal** | {{OBJETIVO}} |
| **Tipo de formulario** | [Elegir: Captura lead / Registro / Actualización perfil / Crear entidad / Configuración / Checkout / Contacto / Otro] |

### 1.2 Objetivo de negocio [OBL]

1. {{OBJETIVO_NEGOCIO_1}}
2. {{OBJETIVO_NEGOCIO_2}}

### 1.3 Objetivo UX [OBL]

- Reducir fricción (mínimos campos necesarios)
- Minimizar errores (validación clara)
- Aumentar completion rate
- Claridad en validaciones y feedback

### 1.4 KPIs [OBL]

| Métrica | Valor objetivo | Valor crítico |
|---------|----------------|---------------|
| Form start rate | {{VALOR}} | < {{VALOR}} |
| Completion rate | {{VALOR}} | < {{VALOR}} |
| Drop-off rate | {{VALOR}} | > {{VALOR}} |
| Tiempo promedio de llenado | {{VALOR}} | > {{VALOR}} |
| Errores por sesión | {{VALOR}} | > {{VALOR}} |

---

## 2) Alcance (Scope) [OBL]

> **Activación:** Siempre obligatorio.

### 2.1 Incluye (In Scope) [OBL]

- {{INCLUYE_1}} (ej: Campos de input + validación)
- {{INCLUYE_2}} (ej: Submit + estados)
- {{INCLUYE_3}} (ej: Integración con {{SISTEMA}})
- {{INCLUYE_4}} (ej: Persistencia de borrador)

### 2.2 No incluye (Out of Scope) [OBL]

- {{EXCLUYE_1}}
- {{EXCLUYE_2}}

### 2.3 Dependencias [OBL]

| Tipo | Dependencia | Estado | Owner |
|------|-------------|--------|-------|
| API | {{ENDPOINT}} | [Pendiente/Listo] | {{OWNER}} |
| CRM | {{SISTEMA}} | [Pendiente/Listo] | {{OWNER}} |
| Auth | {{SISTEMA_AUTH}} | [Pendiente/Listo] | {{OWNER}} |
| Componentes UI | {{COMPONENTES}} | [Pendiente/Listo] | {{OWNER}} |

---

## 3) Usuarios, roles y permisos [COND]

> **Activación:** Incluir si hay múltiples roles con permisos diferenciados. Si es formulario público sin roles, omitir.

### 3.1 Matriz de permisos [COND]

| Rol | Puede ver | Puede editar | Puede enviar | Restricciones |
|-----|-----------|--------------|--------------|---------------|
| {{ROL_1}} | ✅/❌ | ✅/❌ | ✅/❌ | {{RESTRICCION}} |
| {{ROL_2}} | ✅/❌ | ✅/❌ | ✅/❌ | {{RESTRICCION}} |
| {{ROL_ADMIN}} | ✅ | ✅ | ✅ | — |

### 3.2 Reglas de campos por rol [COND]

| Campo | Visible para | Editable para | Notas |
|-------|--------------|---------------|-------|
| {{CAMPO}} | {{ROLES}} | {{ROLES}} | {{NOTAS}} |

---

## 4) Contexto de uso (Journey) [OBL]

> **Activación:** Siempre obligatorio.

### 4.1 Punto de entrada [OBL]

| Origen | Trigger | Contexto |
|--------|---------|----------|
| {{ORIGEN_1}} | {{TRIGGER}} (ej: Click botón CTA) | {{CONTEXTO}} |
| {{ORIGEN_2}} | {{TRIGGER}} | {{CONTEXTO}} |

### 4.2 Punto de salida [OBL]

| Resultado | Destino | Comportamiento |
|-----------|---------|----------------|
| Success | {{DESTINO}} | [Thank-you page / Modal close / Next step / Inline message] |
| Cancel | {{DESTINO}} | [Back / Close / Discard confirmation] |
| Error | {{DESTINO}} | [Inline retry / Error page] |

### 4.3 Flujo principal (Happy Path) [OBL]

```
1. Usuario llega al formulario desde {{ORIGEN}}
2. Sistema muestra formulario en estado idle
3. Usuario completa campos
4. Sistema valida en tiempo real (si aplica)
5. Usuario hace submit
6. Sistema valida y envía
7. Sistema muestra confirmación de éxito
8. Usuario continúa a {{DESTINO}}
```

### 4.4 Flujos alternos [OBL]

| Flujo | Trigger | Comportamiento |
|-------|---------|----------------|
| Abandono | Usuario cierra/navega | {{COMPORTAMIENTO}} |
| Error de validación | Campo inválido | Mostrar error inline, focus en campo |
| Error de red | Sin conexión | {{COMPORTAMIENTO}} |
| Error de backend | API falla | {{COMPORTAMIENTO}} |
| Duplicado | Usuario/email ya existe | {{COMPORTAMIENTO}} |
| Timeout | Respuesta lenta | {{COMPORTAMIENTO}} |

---

## 5) Inventario de campos (Field Inventory) [OBL] — **SECCIÓN NÚCLEO**

> **Activación:** Siempre obligatorio. Esta es la sección más importante del template.

### 5.1 Tabla de campos [OBL]

| Orden | Field ID | Label | Tipo | Requerido | Validación | Dependencia | Default | Placeholder | Error message |
|------:|----------|-------|------|-----------|------------|-------------|---------|-------------|---------------|
| 1 | `{{FIELD_ID}}` | {{LABEL}} | [text/email/tel/number/select/checkbox/radio/textarea/date/file] | Sí/No | {{REGLA}} | {{DEPENDENCIA}} | {{DEFAULT}} | {{PLACEHOLDER}} | {{ERROR}} |
| 2 | `{{FIELD_ID}}` | {{LABEL}} | {{TIPO}} | Sí/No | {{REGLA}} | {{DEPENDENCIA}} | {{DEFAULT}} | {{PLACEHOLDER}} | {{ERROR}} |
| 3 | `{{FIELD_ID}}` | {{LABEL}} | {{TIPO}} | Sí/No | {{REGLA}} | {{DEPENDENCIA}} | {{DEFAULT}} | {{PLACEHOLDER}} | {{ERROR}} |

### 5.2 Detalle de validaciones por campo [OBL]

| Field ID | Regla | Valor | Mensaje de error |
|----------|-------|-------|------------------|
| `email` | Formato | RFC 5322 | "Ingresa un email válido" |
| `email` | Único | Async check | "Este email ya está registrado" |
| `phone` | Regex | `{{REGEX}}` | "Formato de teléfono inválido" |
| `password` | Min length | 8 | "Mínimo 8 caracteres" |
| `password` | Pattern | 1 mayúscula, 1 número | "Debe incluir mayúscula y número" |
| `{{FIELD}}` | {{REGLA}} | {{VALOR}} | {{MENSAJE}} |

### 5.3 Reglas de dependencia entre campos [COND]

> **Activación:** Incluir si hay campos condicionales.

| Campo dependiente | Condición | Comportamiento |
|-------------------|-----------|----------------|
| `{{CAMPO_B}}` | `{{CAMPO_A}}` = `{{VALOR}}` | Mostrar / Habilitar |
| `{{CAMPO_C}}` | `{{CAMPO_A}}` = `{{VALOR}}` | Ocultar / Deshabilitar |
| `{{CAMPO_D}}` | Calculado de `{{CAMPO_E}}` | Auto-fill |

### 5.4 Reglas de navegación [OBL]

| Comportamiento | Implementación |
|----------------|----------------|
| Orden de tab | Secuencial según orden de tabla |
| Enter en campo | [Elegir: Next field / Submit / Nada] |
| Submit habilitado | Cuando: {{CONDICION}} |

---

## 6) Validaciones (Client + Server) [OBL]

> **Activación:** Siempre obligatorio.

### 6.1 Validación client-side [OBL]

| Momento | Comportamiento |
|---------|----------------|
| On blur | Validar campo individual |
| On change | [Elegir: Validar inmediato / Limpiar error previo / Nada] |
| On submit | Validar todos los campos |

### 6.2 Validación server-side [OBL]

| Validación | Endpoint | Momento |
|------------|----------|---------|
| Email único | `{{ENDPOINT}}` | [On blur / On submit] |
| {{VALIDACION}} | `{{ENDPOINT}}` | {{MOMENTO}} |

### 6.3 Manejo de errores [OBL]

| Tipo de error | Ubicación | Comportamiento |
|---------------|-----------|----------------|
| Error de campo | Inline (debajo del campo) | Mostrar mensaje + highlight |
| Error summary | [Arriba del form / No aplica] | Lista de errores con links |
| Focus automático | Primer campo con error | Scroll + focus |

### 6.4 Sanitización [OBL]

| Campo | Sanitización |
|-------|--------------|
| Todos los textos | Trim whitespace |
| Email | Lowercase |
| Teléfono | Strip non-numeric (excepto +) |
| {{CAMPO}} | {{SANITIZACION}} |

---

## 7) Comportamiento del formulario [OBL]

> **Activación:** Siempre obligatorio.

### 7.1 Estados del formulario [OBL]

| Estado | Descripción | UI |
|--------|-------------|-----|
| `idle` | Formulario vacío, listo para input | Campos habilitados |
| `editing` | Usuario está ingresando datos | Campos habilitados |
| `validating` | Validación async en progreso | Spinner en campo |
| `submitting` | Enviando al servidor | Botón loading, campos disabled |
| `success` | Envío exitoso | Mensaje de confirmación |
| `error` | Error en envío | Mensaje de error + retry |

### 7.2 Submit behavior [OBL]

| Comportamiento | Implementación |
|----------------|----------------|
| Prevención doble submit | Disable button al click |
| Debounce | {{VALOR}}ms (si aplica) |
| Loading indicator | Spinner en botón + texto "Enviando..." |
| Timeout | {{VALOR}}s → mostrar retry |

### 7.3 Persistencia [COND]

> **Activación:** Incluir si el form guarda borradores o tiene autosave.

| Comportamiento | Implementación | Storage |
|----------------|----------------|---------|
| Guardar borrador | {{TRIGGER}} | [localStorage / sessionStorage / Backend] |
| Autosave | Cada {{INTERVALO}} o on blur | {{STORAGE}} |
| Restauración | Al volver a la página | Precargar valores |
| Expiración | {{DURACION}} | Limpiar después de X tiempo |

### 7.4 Cancel / Close behavior [OBL]

| Escenario | Comportamiento |
|-----------|----------------|
| Form sin cambios | Cerrar sin confirmación |
| Form con cambios | [Elegir: Confirmación modal / Guardar borrador / Descartar silencioso] |
| Mensaje de confirmación | "{{MENSAJE}}" |

---

## 8) Integraciones y datos [OBL]

> **Activación:** Siempre obligatorio si hay backend.

### 8.1 Endpoints [OBL]

| Endpoint | Método | Uso | Autenticación | Rate limit |
|----------|--------|-----|---------------|------------|
| `{{ENDPOINT_SUBMIT}}` | POST | Enviar formulario | [Sí/No] | {{LIMITE}} |
| `{{ENDPOINT_VALIDATE}}` | GET/POST | Validación async | [Sí/No] | {{LIMITE}} |
| `{{ENDPOINT_PREFILL}}` | GET | Precargar datos | [Sí/No] | {{LIMITE}} |

### 8.2 Payload de envío [OBL]

```json
{
  "{{FIELD_1}}": "{{VALUE}}",
  "{{FIELD_2}}": "{{VALUE}}",
  "metadata": {
    "user_id": "{{USER_ID}}",
    "timestamp": "{{ISO_DATE}}",
    "source": "{{SOURCE}}",
    "utm_campaign": "{{UTM}}"
  }
}
```

### 8.3 Respuestas esperadas [OBL]

| Código | Significado | Acción en UI |
|--------|-------------|--------------|
| 200/201 | Éxito | Mostrar success state |
| 400 | Validación fallida | Mostrar errores por campo |
| 409 | Duplicado | Mostrar mensaje específico |
| 422 | Datos inválidos | Mostrar errores |
| 429 | Rate limit | Mostrar "Intenta más tarde" |
| 500 | Error servidor | Mostrar error genérico + retry |

### 8.4 Anti-spam / Seguridad [COND]

> **Activación:** Incluir para formularios públicos (leads, contacto, registro).

| Mecanismo | Implementación |
|-----------|----------------|
| Honeypot | Campo oculto `{{CAMPO}}` |
| CAPTCHA | [reCAPTCHA v3 / hCaptcha / Ninguno] |
| Rate limiting | {{LIMITE}} requests por IP |
| Deduplicación | Por email en últimas {{HORAS}}h |

---

## 9) UI Specs (Visual) [OBL]

> **Activación:** Siempre obligatorio.

### 9.1 Layout [OBL]

| Propiedad | Valor |
|-----------|-------|
| Columnas | [Elegir: 1 columna / 2 columnas / Mixto] |
| Ancho máximo | {{VALOR}} |
| Spacing vertical entre campos | {{VALOR}} |
| Agrupaciones/secciones | {{DESCRIPCION}} |

### 9.2 Componentes UI por tipo de campo [OBL]

| Tipo de campo | Componente | Variante |
|---------------|------------|----------|
| text | Input | Default |
| email | Input | type="email" |
| tel | Input | type="tel" + máscara |
| select | [Select / Dropdown / Combobox] | {{VARIANTE}} |
| checkbox | Checkbox | {{VARIANTE}} |
| radio | Radio Group | {{VARIANTE}} |
| textarea | Textarea | {{VARIANTE}} |
| date | [Date Picker / Input date] | {{VARIANTE}} |
| file | File Upload | {{VARIANTE}} |

### 9.3 Anatomía de campo [OBL]

```
┌─────────────────────────────────────┐
│ Label *                    (Helper) │
├─────────────────────────────────────┤
│ [  Placeholder text...           ] │
├─────────────────────────────────────┤
│ ⚠️ Error message                    │
└─────────────────────────────────────┘
```

| Elemento | Obligatorio | Notas |
|----------|-------------|-------|
| Label | Sí | Siempre visible |
| Required indicator (*) | Si es requerido | Asterisco o texto |
| Placeholder | Opcional | No reemplaza label |
| Helper text | Opcional | Instrucciones de formato |
| Error message | Cuando hay error | Reemplaza helper |

---

## 10) Accesibilidad (A11Y) [OBL]

> **Activación:** Siempre obligatorio.

### 10.1 Estructura semántica [OBL]

| Requisito | Implementación |
|-----------|----------------|
| `<form>` wrapper | Sí |
| `<label>` por campo | `<label for="{{ID}}">` |
| Campos requeridos | `aria-required="true"` + indicador visual |
| Helper text | `aria-describedby="{{ID}}-helper"` |
| Error messages | `aria-describedby="{{ID}}-error"` + `aria-invalid="true"` |

### 10.2 Navegación por teclado [OBL]

| Tecla | Acción |
|-------|--------|
| Tab | Mover al siguiente campo |
| Shift + Tab | Mover al campo anterior |
| Enter | [Submit form / Next field] — según contexto |
| Space | Toggle checkbox/radio |
| Arrow keys | Navegar opciones en select/radio |
| Escape | Cerrar dropdown/modal |

### 10.3 Screen readers [OBL]

| Evento | Anuncio |
|--------|---------|
| Focus en campo | Label + helper text |
| Error en campo | Label + "inválido" + mensaje de error |
| Submit exitoso | "Formulario enviado correctamente" |
| Submit fallido | "Error al enviar, {{N}} campos con error" |

### 10.4 Touch targets [OBL]

- **Tamaño mínimo:** 44x44px para inputs y botones
- **Spacing mínimo:** 8px entre elementos interactivos

---

## 11) Responsive [OBL]

> **Activación:** Siempre obligatorio.

### 11.1 Breakpoints [OBL]

| Breakpoint | Layout | Notas |
|------------|--------|-------|
| Mobile (320-767) | 1 columna | Campos full-width |
| Tablet (768-1023) | 1-2 columnas | Según complejidad |
| Desktop (1024+) | 1-2 columnas | Max-width contenido |

### 11.2 Comportamiento mobile [OBL]

| Elemento | Comportamiento mobile |
|----------|----------------------|
| Teclado | Tipo apropiado (email, tel, number) |
| Botón submit | Full-width o sticky bottom |
| Selects | Native picker o custom |
| Date picker | Native o custom |
| Autocomplete | `autocomplete` attribute |

---

## 12) Copy y microcopy [OBL]

> **Activación:** Siempre obligatorio.

### 12.1 Textos del formulario [OBL]

| Elemento | Copy | Notas |
|----------|------|-------|
| Título del form | {{COPY}} | H2 o superior |
| Subtítulo/descripción | {{COPY}} | Opcional |
| CTA submit | {{COPY}} | Verbo de acción |
| CTA secundario | {{COPY}} | Si hay cancel/back |

### 12.2 Mensajes de estado [OBL]

| Estado | Mensaje | Tono |
|--------|---------|------|
| Éxito | "{{MENSAJE}}" | Positivo, confirmatorio |
| Error genérico | "{{MENSAJE}}" | Empático, accionable |
| Error de red | "{{MENSAJE}}" | Claro, con retry |
| Campos requeridos | "Este campo es requerido" | Directo |

### 12.3 Labels y placeholders [OBL]

| Campo | Label | Placeholder | Helper text |
|-------|-------|-------------|-------------|
| {{CAMPO}} | {{LABEL}} | {{PLACEHOLDER}} | {{HELPER}} |

---

## 13) Analytics / Instrumentación [OBL]

> **Activación:** Siempre obligatorio.

### 13.1 Eventos [OBL]

| Evento | Trigger | Payload |
|--------|---------|---------|
| `form_view` | Form visible | `form_id, screen_id, user_role` |
| `form_start` | Primer foco en campo | `form_id, first_field` |
| `field_focus` | Foco en campo | `form_id, field_id` |
| `field_blur` | Blur de campo | `form_id, field_id, has_value, has_error` |
| `field_error` | Error de validación | `form_id, field_id, error_type` |
| `form_submit` | Click en submit | `form_id, fields_completed` |
| `form_success` | Respuesta exitosa | `form_id, response_time_ms` |
| `form_failure` | Error en submit | `form_id, error_type, error_code` |
| `form_abandon` | Salir sin completar | `form_id, last_field, fields_completed` |

### 13.2 Métricas derivadas [OPC]

| Métrica | Cálculo |
|---------|---------|
| Completion rate | `form_success / form_start` |
| Drop-off por campo | `field_blur sin form_success` |
| Error rate | `field_error / field_blur` |
| Tiempo de llenado | `form_success.timestamp - form_start.timestamp` |

---

## 14) QA / Casos de prueba [OBL]

> **Activación:** Siempre obligatorio.

### 14.1 Casos funcionales [OBL]

| ID | Caso | Resultado esperado | Prioridad |
|----|------|-------------------|-----------|
| TF-01 | Submit con todos los campos válidos | Success + redirect/message | Crítica |
| TF-02 | Submit con campo requerido vacío | Error inline en campo | Crítica |
| TF-03 | Submit con formato inválido | Error específico de validación | Crítica |
| TF-04 | Validación async (email único) | Error si duplicado | Alta |
| TF-05 | Retry después de error de red | Reenvío exitoso | Alta |
| TF-06 | Doble click en submit | Solo un envío | Alta |

### 14.2 Casos de accesibilidad [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TA-01 | Navegación completa con Tab | Todos los campos alcanzables |
| TA-02 | Labels anunciados por screen reader | Correcto |
| TA-03 | Errores anunciados | aria-invalid + mensaje leído |
| TA-04 | Submit con Enter | Funciona desde cualquier campo |

### 14.3 Casos responsive [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TR-01 | Mobile 320px | Layout 1 columna, sin overflow |
| TR-02 | Teclado mobile email | Teclado con @ visible |
| TR-03 | Teclado mobile teléfono | Teclado numérico |

### 14.4 Casos de error [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TE-01 | Sin conexión | Mensaje de error + retry |
| TE-02 | Timeout de API | Mensaje + retry |
| TE-03 | Error 500 | Mensaje genérico + soporte |
| TE-04 | Rate limit | Mensaje "intenta más tarde" |

---

## 15) Riesgos, supuestos y decisiones [OBL]

> **Activación:** Siempre obligatorio.

### 15.1 Riesgos identificados [OBL]

| ID | Riesgo | Probabilidad | Impacto | Mitigación |
|----|--------|--------------|---------|------------|
| R-01 | {{RIESGO}} | [Alta/Media/Baja] | [Alto/Medio/Bajo] | {{MITIGACION}} |

### 15.2 Supuestos [OBL]

| ID | Supuesto | Validado |
|----|----------|----------|
| S-01 | API disponible y estable | Sí/No |
| S-02 | Reglas de validación confirmadas | Sí/No |
| S-03 | {{SUPUESTO}} | Sí/No |

### 15.3 Decisiones pendientes [OBL]

| ID | Tema | Decisión | Responsable | Fecha |
|----|------|----------|-------------|-------|
| D-01 | Campos mínimos requeridos | {{DECISION}} | {{RESPONSABLE}} | {{FECHA}} |
| D-02 | Mensajes de error | {{DECISION}} | {{RESPONSABLE}} | {{FECHA}} |

---

## 16) Checklist de aprobación [OBL]

> **Activación:** Siempre obligatorio.

### 16.1 Especificación [OBL]

- [ ] Field Inventory completo (tabla §5)
- [ ] Validaciones documentadas (client + server)
- [ ] Estados del form definidos
- [ ] Integraciones/endpoints mapeados

### 16.2 UX [OBL]

- [ ] Copy de labels y errores definido
- [ ] Estados de éxito/error diseñados
- [ ] Responsive especificado
- [ ] Accesibilidad mínima definida

### 16.3 Técnica [OBL]

- [ ] Contrato de API definido
- [ ] Validaciones server confirmadas
- [ ] Seguridad (si aplica: CAPTCHA, rate limit)

### 16.4 QA [OBL]

- [ ] Casos de prueba documentados
- [ ] Analytics instrumentado

### 16.5 Firmas de aprobación [OBL]

| Rol | Nombre | Fecha | Status |
|-----|--------|-------|--------|
| PM/PO | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| UX/UI | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| Tech Lead | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| QA | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |

---

## 17) Particularidades del proyecto [OPC]

> **Activación:** Usar para excepciones o customizaciones específicas.

### 17.1 Excepciones al estándar

| Sección | Excepción | Justificación | Aprobado por |
|---------|-----------|---------------|--------------|
| {{SECCION}} | {{EXCEPCION}} | {{JUSTIFICACION}} | {{APROBADOR}} |

### 17.2 Notas adicionales

{{NOTAS}}

---

## 📋 ANEXOS RELACIONADOS

> Este template Form típicamente es **anexo de** otros templates:

- [ ] **AppScreen** → Form dentro de pantalla de producto
- [ ] **Landing** → Form de captura de leads
- [ ] **Wizard** → Form por cada step
- [ ] **Modal** → Form en overlay
- [ ] **AdminRBAC** → Form con permisos complejos

---

## 🔁 GUÍA OPERATIVA PARA AGENTES

### Cómo usar este template:

1. **Copiar** el template
2. **Completar §5 primero** (Field Inventory) — es la sección núcleo
3. **Reemplazar** placeholders `{{...}}`
4. **Omitir** secciones `[OPC]` o `[COND]` si no aplican
5. **Validar** con checklist (§16)

### Secciones núcleo (mínimo viable):

- §0 Metadatos
- §1 Propósito
- §4 Journey
- §5 **Field Inventory** ← CRÍTICO
- §6 Validaciones
- §7 Estados
- §8 Integraciones
- §10 Accesibilidad
- §12 Copy
- §13 Analytics
- §16 Checklist

### Validación cruzada:

- Cada campo en §5 debe tener validación en §6
- Cada campo en §5 debe tener error message
- Cada estado en §7 debe tener copy en §12
- Cada evento en §13 debe tener caso de prueba en §14

### Red flags a evitar:

- ❌ Form sin Field Inventory
- ❌ Validaciones solo client-side
- ❌ Sin mensajes de error definidos
- ❌ Sin estado de loading/submitting
- ❌ Sin manejo de errores de red

---

> **Fin del template**  
> **Versión:** 2.0  
> **Última actualización:** {{FECHA_ACTUALIZACION}}
