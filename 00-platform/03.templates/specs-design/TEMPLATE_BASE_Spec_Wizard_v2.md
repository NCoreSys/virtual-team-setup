# 🧭 TEMPLATE BASE — SPEC WIZARD (Multi-step Flow / Onboarding)

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

- ✅ Flujo con **2+ pasos** secuenciales
- ✅ Requiere **guardado parcial** o persistencia entre pasos
- ✅ Tiene **validación por step** antes de avanzar
- ✅ Necesita trackear **drop-off por paso**
- ❌ Pantalla única con form simple → usar Form o AppScreen
- ❌ Tabs sin secuencia obligatoria → usar AppScreen

---

# ESPECIFICACIÓN DE WIZARD / FLUJO MULTI-STEP

---

## 0) Metadatos del documento [OBL]

> **Activación:** Siempre obligatorio.

| Campo | Valor |
|-------|-------|
| **Nombre del documento** | Spec_Wizard_{{NOMBRE_WIZARD}}_{{VERSION}} |
| **Proyecto** | {{NOMBRE_PROYECTO}} |
| **Módulo / Feature** | {{NOMBRE_MODULO}} |
| **Wizard / Flow** | {{NOMBRE_WIZARD}} |
| **ID técnico** | `wiz-{{NUM}}-{{SLUG}}` (ej: `wiz-01-onboarding`) |
| **Contexto** | [Elegir: Onboarding / Setup / Checkout / Registro / Creación de entidad / Admin / Compliance] |
| **Número de pasos** | {{NUM_PASOS}} |
| **Versión** | {{VERSION}} |
| **Estado** | [Elegir: Draft / Review / Approved / Deprecated] |
| **Prioridad** | [Elegir: Crítica / Alta / Media / Baja] |
| **Fecha** | {{FECHA_YYYY-MM-DD}} |
| **Owner (PM/PO/Growth)** | {{NOMBRE_OWNER}} |
| **UX/UI Owner** | {{NOMBRE_UX}} |
| **Tech Lead** | {{NOMBRE_TECH}} |
| **QA Owner** | {{NOMBRE_QA}} |

---

## 1) Propósito del flujo [OBL]

> **Activación:** Siempre obligatorio.

### 1.1 Descripción general [OBL]

Este wizard guía a **{{TIPO_USUARIO}}** para completar **{{OBJETIVO}}** en **{{NUM_PASOS}}** pasos.

| Campo | Valor |
|-------|-------|
| **Por qué es wizard (no pantalla única)** | {{JUSTIFICACION}} (ej: tarea compleja, requiere validación por etapas) |
| **Tiempo estimado de completar** | {{TIEMPO}} minutos |
| **Frecuencia de uso** | [Elegir: Una vez / Ocasional / Frecuente] |

### 1.2 Objetivo de negocio [OBL]

1. {{OBJETIVO_NEGOCIO_1}} (ej: Activación de usuarios, conversión, setup completo)
2. {{OBJETIVO_NEGOCIO_2}}

### 1.3 Objetivo UX [OBL]

- Reducir fricción en tarea compleja
- Dar transparencia del progreso
- Minimizar drop-off
- Permitir pausa y continuidad
- Guiar al usuario paso a paso

### 1.4 KPIs [OBL]

| Métrica | Valor objetivo | Valor crítico |
|---------|----------------|---------------|
| Start rate | {{VALOR}} | < {{VALOR}} |
| Completion rate | {{VALOR}} | < {{VALOR}} |
| Drop-off rate global | {{VALOR}} | > {{VALOR}} |
| Drop-off por paso (peor paso) | {{VALOR}} | > {{VALOR}} |
| Tiempo total promedio | {{VALOR}} | > {{VALOR}} |
| Errores por sesión | {{VALOR}} | > {{VALOR}} |

---

## 2) Alcance (Scope) [OBL]

> **Activación:** Siempre obligatorio.

### 2.1 Incluye (In Scope) [OBL]

- {{INCLUYE_1}} (ej: Estructura de pasos y navegación)
- {{INCLUYE_2}} (ej: Validaciones por paso)
- {{INCLUYE_3}} (ej: Persistencia de progreso)
- {{INCLUYE_4}} (ej: Manejo de abandono y recovery)

### 2.2 No incluye (Out of Scope) [OBL]

- {{EXCLUYE_1}}
- {{EXCLUYE_2}}

### 2.3 Dependencias [OBL]

| Tipo | Dependencia | Estado | Owner |
|------|-------------|--------|-------|
| Auth | {{SISTEMA_AUTH}} | [Pendiente/Listo] | {{OWNER}} |
| API | {{ENDPOINTS}} | [Pendiente/Listo] | {{OWNER}} |
| Feature Flag | {{FLAG}} | [Activo/Inactivo] | {{OWNER}} |
| Componentes UI | Stepper, Form components | [Pendiente/Listo] | {{OWNER}} |

---

## 3) Usuarios, roles y permisos [COND]

> **Activación:** Incluir si hay múltiples roles o el wizard cambia por rol.

### 3.1 Matriz de capacidades por rol [COND]

| Rol | Puede iniciar | Puede completar | Puede pausar | Puede editar pasos previos | Restricciones |
|-----|---------------|-----------------|--------------|---------------------------|---------------|
| {{ROL_1}} | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | {{RESTRICCION}} |
| {{ROL_2}} | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | {{RESTRICCION}} |
| {{ROL_ADMIN}} | ✅ | ✅ | ✅ | ✅ | — |

### 3.2 Variaciones por rol [COND]

| Elemento | Cambio por rol | Roles afectados |
|----------|----------------|-----------------|
| Pasos visibles | {{CAMBIO}} | {{ROLES}} |
| Campos editables | {{CAMBIO}} | {{ROLES}} |
| Pasos obligatorios | {{CAMBIO}} | {{ROLES}} |
| Aprobaciones requeridas | {{CAMBIO}} | {{ROLES}} |

---

## 4) Estructura del wizard (Mapa de pasos) [OBL] — **SECCIÓN NÚCLEO**

> **Activación:** Siempre obligatorio. Esta es la sección más importante del template.

### 4.1 Tabla de pasos [OBL]

| Paso # | Step ID | Nombre | Objetivo | Tipo | Inputs principales | Validación clave | Puede saltarse | Tiempo est. |
|-------:|---------|--------|----------|------|-------------------|------------------|----------------|-------------|
| 1 | `step-01` | {{NOMBRE}} | {{OBJETIVO}} | [Form/Selection/Upload/Review/Approval] | {{INPUTS}} | {{VALIDACION}} | Sí/No | {{TIEMPO}} |
| 2 | `step-02` | {{NOMBRE}} | {{OBJETIVO}} | {{TIPO}} | {{INPUTS}} | {{VALIDACION}} | Sí/No | {{TIEMPO}} |
| 3 | `step-03` | {{NOMBRE}} | {{OBJETIVO}} | {{TIPO}} | {{INPUTS}} | {{VALIDACION}} | Sí/No | {{TIEMPO}} |
| N | `step-final` | Confirmación | Revisar y confirmar | Review | Resumen | Todo válido | No | {{TIEMPO}} |

### 4.2 Tipos de pasos [OBL]

| Tipo | Descripción | Componentes típicos |
|------|-------------|---------------------|
| **Form** | Captura de datos | Inputs, selects, validación |
| **Selection** | Elegir opciones | Cards, radio groups, checkboxes |
| **Upload** | Subir archivos | File upload, preview, progress |
| **Review** | Confirmar información | Summary, edit links |
| **Approval** | Requiere aprobación | Status, approver info |
| **Info** | Solo informativo | Text, media, next button |

### 4.3 Reglas de progresión [OBL]

| Regla | Condición |
|-------|-----------|
| **Next habilitado** | {{CONDICION}} (ej: todos los campos requeridos válidos) |
| **Back permitido** | {{CONDICION}} (ej: siempre / solo si no hay commit) |
| **Skip permitido** | {{CONDICION}} (ej: paso marcado como opcional) |
| **Jump a paso futuro** | {{CONDICION}} (ej: nunca / solo si pasos previos completos) |
| **Jump a paso previo** | {{CONDICION}} (ej: siempre / con confirmación) |

### 4.4 Diagrama de flujo [OPC]

```
[Start] → [Step 1] → [Step 2] → [Step 3] → [Review] → [Complete]
              ↓           ↓           ↓
          [Abandon]   [Abandon]   [Abandon]
              ↓           ↓           ↓
          [Resume]    [Resume]    [Resume]
```

---

## 5) Navegación y control del flujo [OBL]

> **Activación:** Siempre obligatorio.

### 5.1 Controles de navegación [OBL]

| Control | Label | Comportamiento | Condición para mostrar |
|---------|-------|----------------|------------------------|
| **Next** | {{LABEL}} (ej: "Continuar") | Validar paso actual → avanzar | Siempre |
| **Back** | {{LABEL}} (ej: "Atrás") | Regresar sin perder datos | Paso > 1 |
| **Save & Exit** | {{LABEL}} | Guardar progreso → salir | {{CONDICION}} |
| **Cancel** | {{LABEL}} | Descartar → confirmar → salir | {{CONDICION}} |
| **Skip** | {{LABEL}} | Saltar paso opcional | Paso marcado skippable |

### 5.2 Stepper behavior [OBL]

| Comportamiento | Valor | Notas |
|----------------|-------|-------|
| Stepper visible | Sí/No | {{NOTAS}} |
| Stepper clickeable | Sí/No | {{NOTAS}} |
| Puede ir a pasos futuros | Sí/No | {{NOTAS}} |
| Puede regresar a pasos previos | Sí/No | {{NOTAS}} |
| Indicador de paso actual | {{TIPO}} | (número, barra, dots) |
| Indicador de pasos completados | {{TIPO}} | (checkmark, color) |
| Indicador de pasos con error | {{TIPO}} | (warning icon, color) |

### 5.3 Persistencia de estado [OBL]

| Tipo | Implementación | Notas |
|------|----------------|-------|
| Persistencia por sesión | [localStorage / sessionStorage / Memory] | {{NOTAS}} |
| Persistencia server | [Sí/No] — Endpoint: {{ENDPOINT}} | {{NOTAS}} |
| Autosave | [Por campo / Por paso / Al salir / No] | {{NOTAS}} |
| Restauración al volver | [Último paso / Desde inicio / Paso válido] | {{NOTAS}} |
| Expiración de draft | {{DURACION}} | {{NOTAS}} |

### 5.4 Manejo de abandono [OBL]

| Escenario | Comportamiento |
|-----------|----------------|
| Usuario intenta salir con cambios | [Elegir: Warning modal / Autosave / Descartar silencioso] |
| Mensaje de confirmación | "{{MENSAJE}}" |
| Recuperación de sesión abandonada | [Elegir: Prompt al volver / Automático / Manual desde lista] |
| Notificación de draft pendiente | [Elegir: Email / Push / In-app / Ninguno] |

---

## 6) Especificación por paso [OBL]

> **Activación:** Repetir por cada paso del wizard.

---

### 6.X Paso {{NUM}}: {{NOMBRE_PASO}} [OBL]

#### a) Identificación [OBL]

| Campo | Valor |
|-------|-------|
| **Step ID** | `step-{{NUM}}` |
| **Nombre** | {{NOMBRE}} |
| **Tipo** | [Elegir: Form / Selection / Upload / Review / Approval / Info] |
| **Obligatorio** | Sí/No |
| **Puede saltarse** | Sí/No |

#### b) Objetivo del paso [OBL]

{{DESCRIPCION_OBJETIVO}}

#### c) UI / Componentes [OBL]

| Componente | Tipo | Prioridad | Notas |
|------------|------|-----------|-------|
| {{COMPONENTE_1}} | {{TIPO}} | {{PRIORIDAD}} | {{NOTAS}} |
| {{COMPONENTE_2}} | {{TIPO}} | {{PRIORIDAD}} | {{NOTAS}} |

#### d) Campos / Inputs [COND: si tipo = Form]

> **Activación:** Incluir si el paso es de tipo Form. Referir a TEMPLATE_BASE_Spec_Form para detalle completo.

| Field ID | Label | Tipo | Requerido | Validación | Default |
|----------|-------|------|-----------|------------|---------|
| `{{FIELD}}` | {{LABEL}} | {{TIPO}} | Sí/No | {{VALIDACION}} | {{DEFAULT}} |

#### e) Opciones [COND: si tipo = Selection]

> **Activación:** Incluir si el paso es de tipo Selection.

| Option ID | Label | Descripción | Selección |
|-----------|-------|-------------|-----------|
| `{{OPTION}}` | {{LABEL}} | {{DESCRIPCION}} | [Single/Multiple] |

#### f) Validaciones [OBL]

| Validación | Momento | Mensaje de error |
|------------|---------|------------------|
| {{VALIDACION_1}} | [On blur / On next / Async] | {{MENSAJE}} |
| {{VALIDACION_2}} | {{MOMENTO}} | {{MENSAJE}} |

#### g) Estados del paso [OBL]

| Estado | Descripción | UI |
|--------|-------------|-----|
| `not_started` | Paso no alcanzado | Deshabilitado en stepper |
| `in_progress` | Paso actual | Activo |
| `completed` | Paso completado | Checkmark en stepper |
| `error` | Tiene errores | Warning en stepper |
| `skipped` | Paso saltado | Indicador de skip |

#### h) Reglas de navegación del paso [OBL]

| Regla | Condición |
|-------|-----------|
| Next habilitado | {{CONDICION}} |
| Back permitido | {{CONDICION}} |
| Skip permitido | {{CONDICION}} |

#### i) Datos / API [OPC]

| Endpoint | Método | Uso | Momento |
|----------|--------|-----|---------|
| `{{ENDPOINT}}` | GET | Precargar datos | Al entrar al paso |
| `{{ENDPOINT}}` | POST | Guardar paso | Al hacer Next |

#### j) Analytics [OBL]

| Evento | Trigger | Payload adicional |
|--------|---------|-------------------|
| `step_view` | Paso visible | `step_id, step_number` |
| `step_complete` | Next exitoso | `step_id, duration_ms` |
| `step_error` | Error de validación | `step_id, error_type, field` |
| `step_skip` | Usuario salta paso | `step_id` |
| `step_back` | Usuario regresa | `step_id, from_step` |

---

## 7) Datos, APIs e integraciones [OBL]

> **Activación:** Siempre obligatorio.

### 7.1 Endpoints por paso [OBL]

| Step ID | Endpoint | Método | Uso | Prioridad |
|---------|----------|--------|-----|-----------|
| Global | `{{ENDPOINT_INIT}}` | GET | Inicializar wizard | Crítica |
| `step-01` | `{{ENDPOINT}}` | POST | Guardar paso 1 | Alta |
| `step-02` | `{{ENDPOINT}}` | POST | Guardar paso 2 | Alta |
| Global | `{{ENDPOINT_COMPLETE}}` | POST | Finalizar wizard | Crítica |

### 7.2 Estrategia de guardado [OBL]

| Estrategia | Descripción | Cuándo usar |
|------------|-------------|-------------|
| **Por paso (commit incremental)** | Cada paso guarda al server | Wizards largos, datos críticos |
| **Al final (commit único)** | Todo se guarda al completar | Wizards cortos, datos no críticos |
| **Híbrido** | Algunos pasos guardan, otros no | Según criticidad del dato |

**Estrategia seleccionada:** [Elegir: Por paso / Al final / Híbrido]

### 7.3 Payload de wizard completo [OBL]

```json
{
  "wizard_id": "{{WIZARD_ID}}",
  "user_id": "{{USER_ID}}",
  "status": "completed",
  "steps": {
    "step-01": { "{{FIELD}}": "{{VALUE}}" },
    "step-02": { "{{FIELD}}": "{{VALUE}}" }
  },
  "metadata": {
    "started_at": "{{ISO_DATE}}",
    "completed_at": "{{ISO_DATE}}",
    "duration_ms": {{VALUE}}
  }
}
```

### 7.4 Respuestas y errores [OBL]

| Código | Significado | Acción en UI |
|--------|-------------|--------------|
| 200/201 | Éxito | Avanzar al siguiente paso |
| 400 | Validación fallida | Mostrar errores en paso |
| 409 | Conflicto (ej: duplicado) | Mensaje específico |
| 500 | Error servidor | Error global + retry |

---

## 8) Reglas de negocio [OBL]

> **Activación:** Siempre obligatorio.

### 8.1 Reglas globales del wizard [OBL]

| ID | Regla | Pasos afectados |
|----|-------|-----------------|
| BR-01 | {{REGLA}} | {{PASOS}} |
| BR-02 | {{REGLA}} | {{PASOS}} |

### 8.2 Reglas condicionales [OPC]

| Condición | Efecto en wizard |
|-----------|------------------|
| Usuario es {{SEGMENTO}} | {{EFECTO}} (ej: mostrar paso extra) |
| {{CONDICION}} | {{EFECTO}} |

### 8.3 Requisitos de compliance [COND]

> **Activación:** Incluir si hay requisitos legales o regulatorios.

| Requisito | Paso afectado | Implementación |
|-----------|---------------|----------------|
| {{REQUISITO}} | {{PASO}} | {{IMPLEMENTACION}} |

---

## 9) Estados globales del wizard [OBL]

> **Activación:** Siempre obligatorio.

### 9.1 Estados del wizard [OBL]

| Estado | Descripción | UI |
|--------|-------------|-----|
| `not_started` | Usuario no ha iniciado | CTA para iniciar |
| `in_progress` | En algún paso | Stepper + contenido del paso |
| `paused` | Guardado y abandonado | Opción de continuar |
| `completed` | Todos los pasos completados | Confirmación final |
| `expired` | Draft expirado | Mensaje + opción de reiniciar |
| `error` | Error irrecuperable | Mensaje + soporte |

### 9.2 Loading states [OBL]

| Contexto | Tipo de loading | UI |
|----------|-----------------|-----|
| Carga inicial del wizard | [Spinner / Skeleton] | {{DESCRIPCION}} |
| Transición entre pasos | [Spinner / Skeleton / Ninguno] | {{DESCRIPCION}} |
| Guardado de paso | [Inline spinner / Button loading] | {{DESCRIPCION}} |
| Finalización | [Spinner / Progress bar] | {{DESCRIPCION}} |

### 9.3 Error states [OBL]

| Tipo | Scope | Mensaje | CTA |
|------|-------|---------|-----|
| Error de campo | Campo individual | {{MENSAJE}} | Fix inline |
| Error de paso | Paso completo | {{MENSAJE}} | Fix + retry |
| Error de red | Global | {{MENSAJE}} | Retry |
| Error de servidor | Global | {{MENSAJE}} | Retry / Soporte |

### 9.4 Success / Completion [OBL]

| Elemento | Valor |
|----------|-------|
| Pantalla de confirmación | [Elegir: Inline / Redirect a thank-you / Modal] |
| Mensaje de éxito | "{{MENSAJE}}" |
| Siguiente acción | {{SIGUIENTE_ACCION}} |
| Redirect destino | {{URL_DESTINO}} |

---

## 10) Accesibilidad (A11Y) [OBL]

> **Activación:** Siempre obligatorio.

### 10.1 Stepper accesible [OBL]

| Requisito | Implementación |
|-----------|----------------|
| Role ARIA | `role="navigation"` + `aria-label="Progreso del formulario"` |
| Paso actual | `aria-current="step"` |
| Pasos completados | `aria-label` con estado |
| Anuncio de progreso | "Paso {{N}} de {{TOTAL}}: {{NOMBRE}}" |

### 10.2 Navegación por teclado [OBL]

| Tecla | Acción |
|-------|--------|
| Tab | Navegar campos dentro del paso |
| Enter | Submit paso / Activar botón |
| Escape | Cerrar modales de confirmación |

### 10.3 Focus management [OBL]

| Evento | Comportamiento de focus |
|--------|------------------------|
| Cambio de paso | Focus al título del nuevo paso |
| Error de validación | Focus al primer campo con error |
| Modal de confirmación | Focus trap dentro del modal |
| Cierre de modal | Return focus al trigger |

### 10.4 Screen readers [OBL]

| Evento | Anuncio |
|--------|---------|
| Entrada a paso | "Paso {{N}} de {{TOTAL}}: {{NOMBRE}}" |
| Completar paso | "Paso {{N}} completado, avanzando a paso {{N+1}}" |
| Error | "Error en paso {{N}}: {{DESCRIPCION}}" |
| Wizard completo | "Proceso completado exitosamente" |

---

## 11) Responsive [OBL]

> **Activación:** Siempre obligatorio.

### 11.1 Breakpoints [OBL]

| Breakpoint | Comportamiento stepper | Comportamiento contenido |
|------------|------------------------|--------------------------|
| Mobile (320-767) | [Compacto / Oculto / Dots] | 1 columna |
| Tablet (768-1023) | [Normal / Compacto] | 1-2 columnas |
| Desktop (1024+) | Normal con labels | 2 columnas si aplica |

### 11.2 Navegación mobile [OBL]

| Elemento | Comportamiento mobile |
|----------|----------------------|
| Botones Next/Back | [Elegir: Sticky bottom / Inline / Full-width] |
| Stepper | [Elegir: Top compacto / Hidden + progress bar / Dots] |
| Contenido | Scroll vertical, evitar horizontal |

---

## 12) Copy y microcopy [OBL]

> **Activación:** Siempre obligatorio.

### 12.1 Textos globales [OBL]

| Elemento | Copy | Notas |
|----------|------|-------|
| Título del wizard | {{COPY}} | H1 |
| Subtítulo/descripción | {{COPY}} | Opcional |
| Indicador de progreso | "Paso {{N}} de {{TOTAL}}" | — |

### 12.2 Botones de navegación [OBL]

| Botón | Copy default | Variante por paso |
|-------|--------------|-------------------|
| Next | {{COPY}} (ej: "Continuar") | {{VARIANTES}} |
| Back | {{COPY}} (ej: "Atrás") | — |
| Save & Exit | {{COPY}} | — |
| Cancel | {{COPY}} | — |
| Finish | {{COPY}} (ej: "Finalizar") | Último paso |

### 12.3 Mensajes de estado [OBL]

| Estado | Mensaje |
|--------|---------|
| Éxito final | "{{MENSAJE}}" |
| Error genérico | "{{MENSAJE}}" |
| Abandono warning | "{{MENSAJE}}" |
| Draft recuperado | "{{MENSAJE}}" |

---

## 13) Analytics / Instrumentación [OBL]

> **Activación:** Siempre obligatorio.

### 13.1 Eventos de wizard [OBL]

| Evento | Trigger | Payload |
|--------|---------|---------|
| `wizard_view` | Wizard cargado | `wizard_id, user_id, has_draft` |
| `wizard_start` | Primer paso iniciado | `wizard_id, entry_point` |
| `step_view` | Paso visible | `wizard_id, step_id, step_number` |
| `step_complete` | Paso completado | `wizard_id, step_id, duration_ms` |
| `step_error` | Error en paso | `wizard_id, step_id, error_type` |
| `step_back` | Regreso a paso anterior | `wizard_id, from_step, to_step` |
| `step_skip` | Paso saltado | `wizard_id, step_id` |
| `wizard_save_exit` | Guardar y salir | `wizard_id, last_step` |
| `wizard_abandon` | Abandono sin guardar | `wizard_id, last_step, time_spent` |
| `wizard_complete` | Wizard finalizado | `wizard_id, total_duration, steps_completed` |

### 13.2 Métricas derivadas [OBL]

| Métrica | Cálculo |
|---------|---------|
| Completion rate | `wizard_complete / wizard_start` |
| Drop-off rate por paso | `1 - (step_N_complete / step_N_view)` |
| Tiempo promedio | `avg(wizard_complete.total_duration)` |
| Paso con más abandono | `max(drop-off rate por paso)` |
| Recovery rate | `wizard_complete con draft / wizard_save_exit` |

---

## 14) Performance y riesgos técnicos [OPC]

> **Activación:** Incluir para wizards críticos o complejos.

### 14.1 Riesgos de performance [OPC]

| Riesgo | Impacto | Mitigación |
|--------|---------|------------|
| Demasiados pasos | Drop-off alto | Consolidar pasos, mostrar progreso claro |
| Validaciones async lentas | Frustración usuario | Loading states, optimistic UI |
| Guardado frecuente costoso | Latencia | Debounce, batch saves |
| Pérdida de progreso | Abandono | Autosave, recovery |
| Carga inicial pesada | Bounce | Lazy load por paso |

### 14.2 Objetivos de performance [OPC]

| Métrica | Objetivo |
|---------|----------|
| Carga inicial | < {{VALOR}}s |
| Transición entre pasos | < {{VALOR}}ms |
| Guardado de paso | < {{VALOR}}s |

---

## 15) QA / Casos de prueba [OBL]

> **Activación:** Siempre obligatorio.

### 15.1 Casos funcionales [OBL]

| ID | Caso | Resultado esperado | Prioridad |
|----|------|-------------------|-----------|
| TF-01 | Completar wizard happy path | Success + redirect | Crítica |
| TF-02 | Next con campos inválidos | Error inline, no avanza | Crítica |
| TF-03 | Back en paso 2+ | Regresa con datos intactos | Alta |
| TF-04 | Skip en paso opcional | Avanza sin validar | Alta |
| TF-05 | Save & Exit | Guarda draft, sale | Alta |
| TF-06 | Recuperar draft | Resume desde último paso | Alta |

### 15.2 Casos de error y recovery [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TE-01 | Sin conexión al guardar | Error + retry, no pierde datos |
| TE-02 | Timeout de API | Mensaje + retry |
| TE-03 | Sesión expirada | Redirect a login, preserva draft |
| TE-04 | Draft expirado | Mensaje + opción reiniciar |

### 15.3 Casos de accesibilidad [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TA-01 | Navegación con Tab | Todos los campos alcanzables |
| TA-02 | Stepper con screen reader | Anuncia paso actual y total |
| TA-03 | Focus al cambiar paso | Focus en título del nuevo paso |

### 15.4 Casos responsive [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TR-01 | Wizard en mobile 320px | Stepper compacto, contenido 1 col |
| TR-02 | Botones en mobile | Accesibles, touch target 44px |

---

## 16) Riesgos, supuestos y decisiones [OBL]

> **Activación:** Siempre obligatorio.

### 16.1 Riesgos identificados [OBL]

| ID | Riesgo | Probabilidad | Impacto | Mitigación |
|----|--------|--------------|---------|------------|
| R-01 | Drop-off alto en paso {{N}} | [Alta/Media/Baja] | Alto | {{MITIGACION}} |
| R-02 | {{RIESGO}} | {{PROB}} | {{IMPACTO}} | {{MITIGACION}} |

### 16.2 Supuestos [OBL]

| ID | Supuesto | Validado |
|----|----------|----------|
| S-01 | APIs disponibles y estables | Sí/No |
| S-02 | {{SUPUESTO}} | Sí/No |

### 16.3 Decisiones pendientes [OBL]

| ID | Tema | Decisión | Responsable | Fecha |
|----|------|----------|-------------|-------|
| D-01 | Número de pasos | {{DECISION}} | {{RESPONSABLE}} | {{FECHA}} |
| D-02 | Estrategia de guardado | {{DECISION}} | {{RESPONSABLE}} | {{FECHA}} |

---

## 17) Checklist de aprobación [OBL]

> **Activación:** Siempre obligatorio.

### 17.1 Especificación [OBL]

- [ ] Mapa de pasos completo (tabla §4)
- [ ] Cada paso especificado (§6)
- [ ] Reglas de progresión definidas
- [ ] Estrategia de persistencia definida

### 17.2 UX [OBL]

- [ ] Estados globales definidos
- [ ] Copy de navegación definido
- [ ] Responsive especificado
- [ ] Accesibilidad definida

### 17.3 Técnica [OBL]

- [ ] Endpoints mapeados
- [ ] Estrategia de guardado confirmada
- [ ] Manejo de errores definido

### 17.4 QA [OBL]

- [ ] Casos de prueba documentados
- [ ] Analytics instrumentado

### 17.5 Firmas de aprobación [OBL]

| Rol | Nombre | Fecha | Status |
|-----|--------|-------|--------|
| PM/PO | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| UX/UI | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| Tech Lead | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| QA | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |

---

## 18) Particularidades del proyecto [OPC]

> **Activación:** Usar para excepciones o customizaciones específicas.

### 18.1 Excepciones al estándar

| Sección | Excepción | Justificación | Aprobado por |
|---------|-----------|---------------|--------------|
| {{SECCION}} | {{EXCEPCION}} | {{JUSTIFICACION}} | {{APROBADOR}} |

### 18.2 Notas adicionales

{{NOTAS}}

---

## 📋 ANEXOS REQUERIDOS

> Marcar los anexos que aplican:

- [ ] **Anexo Form** → Para cada paso tipo Form con campos complejos (usar TEMPLATE_BASE_Spec_Form)
- [ ] **Anexo UXStates** → Referencia a estándar global de estados
- [ ] **Anexo AdminRBAC** → Si hay permisos complejos por rol

---

## 🔁 GUÍA OPERATIVA PARA AGENTES

### Cómo usar este template:

1. **Copiar** el template
2. **Completar §4 primero** (Mapa de pasos) — es la sección núcleo
3. **Repetir §6** por cada paso del wizard
4. **Reemplazar** placeholders `{{...}}`
5. **Omitir** secciones `[OPC]` o `[COND]` si no aplican
6. **Validar** con checklist (§17)

### Secciones núcleo (mínimo viable):

- §0 Metadatos
- §1 Propósito + KPIs
- §4 **Mapa de pasos** ← CRÍTICO
- §5 Navegación y persistencia
- §6 **Spec por cada paso** ← CRÍTICO
- §7 APIs
- §9 Estados globales
- §10 Accesibilidad
- §13 Analytics
- §17 Checklist

### Validación cruzada:

- Cada paso en §4 debe tener spec en §6
- Cada paso en §4 debe tener endpoint en §7 (si guarda)
- Cada paso debe tener evento en §13
- Reglas de progresión en §4.3 deben coincidir con §6.h

### Red flags a evitar:

- ❌ Wizard sin mapa de pasos
- ❌ Pasos sin objetivo claro
- ❌ Sin estrategia de persistencia
- ❌ Sin manejo de abandono
- ❌ Sin recovery de drafts
- ❌ Más de 7 pasos sin justificación

---

> **Fin del template**  
> **Versión:** 2.0  
> **Última actualización:** {{FECHA_ACTUALIZACION}}
