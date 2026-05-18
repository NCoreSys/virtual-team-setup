# 🪟 TEMPLATE BASE — SPEC MODAL / DRAWER / OVERLAY

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

- ✅ **Modal de confirmación** (especialmente destructivas)
- ✅ **Modal de edición rápida** (sin salir de contexto)
- ✅ **Drawer con formulario** o contenido contextual
- ✅ **Bottom sheet** en mobile
- ✅ **Overlay crítico** que requiere documentación de accesibilidad
- ❌ Flujo multi-paso complejo → usar Wizard
- ❌ Página completa de edición → usar EntityDetail o AppScreen
- ❌ Tooltip simple → no requiere spec

---

# ESPECIFICACIÓN DE MODAL / DRAWER / OVERLAY

---

## 0) Metadatos del documento [OBL]

> **Activación:** Siempre obligatorio.

| Campo | Valor |
|-------|-------|
| **Nombre del documento** | Spec_Overlay_{{NOMBRE_OVERLAY}}_{{VERSION}} |
| **Proyecto** | {{NOMBRE_PROYECTO}} |
| **Módulo / Feature** | {{NOMBRE_MODULO}} |
| **Overlay** | {{NOMBRE_OVERLAY}} |
| **Tipo** | [Elegir: Modal / Drawer / Bottom Sheet / Popover / Dialog] |
| **ID técnico** | `overlay-{{NUM}}-{{SLUG}}` (ej: `overlay-01-edit-item`) |
| **Invocado desde** | {{PANTALLAS_ORIGEN}} |
| **Versión** | {{VERSION}} |
| **Estado** | [Elegir: Draft / Review / Approved / Deprecated] |
| **Prioridad** | [Elegir: Crítica / Alta / Media / Baja] |
| **Fecha** | {{FECHA_YYYY-MM-DD}} |
| **Owner (PM/PO)** | {{NOMBRE_OWNER}} |
| **UX/UI Owner** | {{NOMBRE_UX}} |
| **Tech Lead** | {{NOMBRE_TECH}} |
| **QA Owner** | {{NOMBRE_QA}} |

---

## 1) Propósito del overlay [OBL]

> **Activación:** Siempre obligatorio.

### 1.1 Descripción general [OBL]

Este overlay permite a **{{TIPO_USUARIO}}** realizar **{{ACCION}}** sin abandonar la pantalla origen.

| Campo | Valor |
|-------|-------|
| **Acción principal** | {{ACCION}} (ej: Editar item, Confirmar eliminación, Crear nuevo) |
| **Contexto** | {{CONTEXTO}} (ej: Desde grid de productos, Desde detalle de orden) |
| **Naturaleza** | [Elegir: Tarea rápida / Confirmación / Formulario / Información] |

### 1.2 Objetivo de negocio [OBL]

1. {{OBJETIVO_1}} (ej: Reducir fricción en ediciones rápidas)
2. {{OBJETIVO_2}} (ej: Prevenir errores en acciones destructivas)
3. {{OBJETIVO_3}} (ej: Mantener contexto del usuario)

### 1.3 Objetivo UX [OBL]

- Foco en la tarea específica
- Claridad sobre qué va a cambiar
- Cerrar/volver sin perder contexto de la pantalla origen

---

## 2) Alcance (Scope) [OBL]

> **Activación:** Siempre obligatorio.

### 2.1 Incluye (In Scope) [OBL]

- {{INCLUYE_1}} (ej: Contenido del overlay)
- {{INCLUYE_2}} (ej: Acciones confirm/cancel)
- {{INCLUYE_3}} (ej: Validaciones si hay form)
- {{INCLUYE_4}} (ej: Estados loading/error/success)
- {{INCLUYE_5}} (ej: Focus trap y accesibilidad)

### 2.2 No incluye (Out of Scope) [OBL]

- {{EXCLUYE_1}} (ej: Navegación completa — usar Wizard si se requiere)
- {{EXCLUYE_2}}

### 2.3 Dependencias [OBL]

| Tipo | Dependencia | Estado | Owner |
|------|-------------|--------|-------|
| API | {{ENDPOINT}} | [Pendiente/Listo] | {{OWNER}} |
| RBAC | {{PERMISO}} | [Pendiente/Listo] | {{OWNER}} |
| Design System | {{COMPONENTE}} | [Pendiente/Listo] | {{OWNER}} |

---

## 3) Disparadores (Entry Triggers) [OBL]

> **Activación:** Siempre obligatorio.

### 3.1 Tabla de triggers [OBL]

| Trigger ID | Tipo | Origen | Elemento UI | Condición | Parámetros |
|------------|------|--------|-------------|-----------|------------|
| `trig-01` | Click botón | {{PANTALLA}} | CTA "{{LABEL}}" | {{CONDICION}} | `mode`, `entity_id` |
| `trig-02` | Row action | {{GRID}} | Menu "{{LABEL}}" | {{CONDICION}} | `entity_id`, `row_data` |
| `trig-03` | Keyboard | {{PANTALLA}} | Shortcut `{{KEY}}` | Focus en elemento | — |
| `trig-{{N}}` | {{TIPO}} | {{ORIGEN}} | {{UI}} | {{CONDICION}} | {{PARAMS}} |

### 3.2 Parámetros de entrada [OBL]

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `entity_id` | string | [Sí/No] | ID de la entidad a editar/ver |
| `mode` | enum | Sí | [create/edit/view/confirm] |
| `context` | object | No | Datos adicionales (filtros, tab activo) |
| `{{PARAM}}` | {{TIPO}} | {{REQ}} | {{DESCRIPCION}} |

### 3.3 Precondiciones [OBL]

| Precondición | Validación | Si no cumple |
|--------------|------------|--------------|
| Usuario autenticado | Session válida | Redirect a login |
| Permiso requerido | RBAC check | Botón no visible o disabled |
| Entidad existe | API check | Error 404 |
| {{PRECONDICION}} | {{VALIDACION}} | {{FALLBACK}} |

---

## 4) Layout del overlay [OBL]

> **Activación:** Siempre obligatorio.

### 4.1 Tipo de overlay [OBL]

| Tipo | Cuándo usar | Seleccionado |
|------|-------------|--------------|
| **Modal centrado** | Tareas focalizadas, confirmaciones | ☐ |
| **Drawer lateral** | Edición con contexto visible, panels | ☐ |
| **Bottom sheet** | Mobile, acciones rápidas | ☐ |
| **Full-screen modal** | Formularios largos en mobile | ☐ |

### 4.2 Anatomía [OBL]

```
┌─────────────────────────────────────────┐
│  HEADER                            [✕]  │
│  Título + Subtítulo (opcional)          │
├─────────────────────────────────────────┤
│                                         │
│  BODY (scrollable)                      │
│  - Contenido principal                  │
│  - Formulario / Información / Lista     │
│                                         │
├─────────────────────────────────────────┤
│  FOOTER (sticky)                        │
│  [Cancel]                    [Primary]  │
└─────────────────────────────────────────┘
```

### 4.3 Dimensiones [OBL]

| Breakpoint | Tamaño | Comportamiento |
|------------|--------|----------------|
| Mobile | Full-screen o Bottom sheet | 100% width |
| Tablet | {{TAMAÑO}} (ej: 600px) | Centrado |
| Desktop | {{TAMAÑO}} (ej: 480px / 640px / 800px) | Centrado |

| Propiedad | Valor |
|-----------|-------|
| Max height | {{VALOR}} (ej: 90vh) |
| Min height | {{VALOR}} (ej: 200px) |
| Border radius | {{VALOR}} |
| Shadow | {{TOKEN}} |

### 4.4 Scroll behavior [OBL]

| Zona | Comportamiento |
|------|----------------|
| Header | Fixed (no scroll) |
| Body | Scroll interno si contenido excede |
| Footer | Fixed (no scroll) |
| Background | Scroll bloqueado |

---

## 5) Contenido y componentes (Overlay Inventory) [OBL] — **SECCIÓN NÚCLEO**

> **Activación:** Siempre obligatorio.

### 5.1 Estructura del overlay [OBL]

| Zona | Componente | Contenido | Datos | Estados |
|------|------------|-----------|-------|---------|
| Header | Title | {{TITULO}} | — | — |
| Header | Subtitle | {{SUBTITULO}} (opcional) | — | — |
| Header | Close button | ✕ | — | — |
| Body | {{COMPONENTE_1}} | {{CONTENIDO}} | {{FUENTE}} | loading/error |
| Body | {{COMPONENTE_2}} | {{CONTENIDO}} | {{FUENTE}} | loading/error |
| Footer | Cancel button | "{{LABEL}}" | — | — |
| Footer | Primary button | "{{LABEL}}" | — | disabled/loading |

### 5.2 Detalle de componentes [OBL]

#### Header [OBL]

| Elemento | Valor |
|----------|-------|
| Título | {{TITULO}} (ej: "Editar producto", "Confirmar eliminación") |
| Subtítulo | {{SUBTITULO}} (ej: nombre de entidad, contexto) |
| Icono | {{ICONO}} (opcional) |
| Close button | Sí (✕) |
| Status badge | {{STATUS}} (si aplica) |

#### Body [OBL]

| Componente | Tipo | Descripción |
|------------|------|-------------|
| {{COMPONENTE}} | [Form / DataList / Summary / Warning / Custom] | {{DESCRIPCION}} |

> Si el body contiene un **Form**, referenciar: `TEMPLATE_BASE_Spec_Form`

#### Footer [OBL]

| Botón | Label | Tipo | Posición | Comportamiento |
|-------|-------|------|----------|----------------|
| Cancel | "{{LABEL}}" | Secondary | Izquierda | Cierra overlay |
| Primary | "{{LABEL}}" | Primary / Danger | Derecha | Ejecuta acción |
| Secondary action | "{{LABEL}}" | Tertiary | {{POS}} | {{COMPORTAMIENTO}} |

---

## 6) Modos (Modes) [OBL]

> **Activación:** Siempre obligatorio.

### 6.1 Modos soportados [OBL]

| Modo | Descripción | Habilitado |
|------|-------------|------------|
| `create` | Crear nueva entidad | ☐ |
| `edit` | Editar entidad existente | ☐ |
| `view` | Ver detalle (solo lectura) | ☐ |
| `confirm` | Confirmar acción (especialmente destructiva) | ☐ |
| `{{MODO}}` | {{DESCRIPCION}} | ☐ |

### 6.2 Diferencias por modo [OBL]

| Elemento | `create` | `edit` | `view` | `confirm` |
|----------|----------|--------|--------|-----------|
| Título | "Crear {{ENTIDAD}}" | "Editar {{ENTIDAD}}" | "Ver {{ENTIDAD}}" | "{{ACCION_CONFIRM}}" |
| Campos editables | Todos | Todos (menos ID) | Ninguno | — |
| Primary CTA | "Crear" | "Guardar" | "Cerrar" | "{{CTA_CONFIRM}}" |
| CTA tipo | Primary | Primary | Secondary | Danger |
| Validaciones | Sí | Sí | No | No |
| Preload data | No | Sí | Sí | Sí (resumen) |

### 6.3 Modo confirm (destructivo) [COND]

> **Activación:** Incluir si hay acciones destructivas.

| Campo | Valor |
|-------|-------|
| Título | "{{TITULO_CONFIRM}}" (ej: "¿Eliminar este item?") |
| Mensaje | "{{MENSAJE}}" (ej: "Esta acción no se puede deshacer.") |
| Info de la entidad | {{INFO}} (nombre, ID, datos relevantes) |
| CTA Confirm | "{{LABEL}}" (ej: "Eliminar") |
| CTA Cancel | "Cancelar" |
| Typing confirmation | [Sí: escribir "{{TEXTO}}" / No] |

---

## 7) Acciones (CTAs) y reglas [OBL]

> **Activación:** Siempre obligatorio.

### 7.1 Acciones principales [OBL]

| Acción | Label | Tipo | Rol mínimo | Confirmación | Resultado | Errores |
|--------|-------|------|------------|--------------|-----------|---------|
| `save` | "Guardar" | Primary | {{ROL}} | No | Persiste + cierra | 400, 409, 500 |
| `create` | "Crear" | Primary | {{ROL}} | No | Crea + cierra | 400, 409, 500 |
| `delete` | "Eliminar" | Danger | {{ROL}} | Sí (modal anidado o typing) | Elimina + cierra | 403, 404, 409 |
| `cancel` | "Cancelar" | Secondary | — | [Si hay cambios] | Cierra sin guardar | — |
| `{{ACTION}}` | "{{LABEL}}" | {{TIPO}} | {{ROL}} | Sí/No | {{RESULTADO}} | {{ERRORES}} |

### 7.2 Habilitación de botones [OBL]

| Condición | Estado del botón primary |
|-----------|--------------------------|
| Form inválido | Disabled |
| Submit en progreso | Loading (spinner) + disabled |
| Error de validación | Enabled (mostrar errores) |
| Sin cambios (edit mode) | Disabled o enabled (según UX) |

### 7.3 Loading lock [OBL]

| Durante submit | Comportamiento |
|----------------|----------------|
| Primary CTA | Spinner + disabled |
| Cancel CTA | Disabled |
| Close (✕) | Disabled |
| Click outside | Bloqueado |
| ESC | Bloqueado |

---

## 8) Cierre del overlay (Exit Rules) [OBL]

> **Activación:** Siempre obligatorio.

### 8.1 Métodos de cierre [OBL]

| Método | Habilitado | Condiciones |
|--------|------------|-------------|
| Close button (✕) | Sí | No durante submit |
| ESC key | Sí/No | No durante submit, no si hay cambios sin guardar |
| Click outside (backdrop) | Sí/No | No durante submit, no si hay cambios |
| Cancel button | Sí | No durante submit |
| Success auto-close | Sí/No | Después de acción exitosa |

### 8.2 Reglas de cierre con cambios [OBL]

| Escenario | Comportamiento |
|-----------|----------------|
| Sin cambios | Cierra inmediatamente |
| Con cambios sin guardar | Warning "¿Descartar cambios?" |
| Durante submit | Bloquear todos los métodos de cierre |

#### Dialog de discard [COND]

```
┌─────────────────────────────────────┐
│  ¿Descartar cambios?                │
│                                     │
│  Los cambios no guardados se        │
│  perderán.                          │
│                                     │
│  [Seguir editando]  [Descartar]     │
└─────────────────────────────────────┘
```

### 8.3 Estado al cerrar [OBL]

| Escenario | Comportamiento en pantalla origen |
|-----------|-----------------------------------|
| Cancel/Discard | Sin cambios |
| Success (create) | Agregar item a lista / refetch |
| Success (edit) | Actualizar item en lista / refetch |
| Success (delete) | Remover item de lista / refetch |

| Preservar | Sí/No |
|-----------|-------|
| Scroll position | Sí |
| Filtros activos | Sí |
| Selección | [Mantener / Limpiar] |
| Tab activo | Sí |
---

*...Continuación de Parte 1 (Secciones 0-8)*

---

## 9) Estados (UX States) [OBL]

> **Activación:** Siempre obligatorio. Referencia: `UXStates_Pack_{{PROYECTO}}`

### 9.1 Estados del overlay [OBL]

| Estado | Trigger | UI |
|--------|---------|-----|
| `loading_initial` | Abriendo + cargando datos | Skeleton en body |
| `ready` | Datos cargados | Contenido visible |
| `submitting` | Acción en progreso | Spinner en CTA, inputs disabled |
| `success` | Acción exitosa | Toast + auto-close (o mensaje inline) |
| `error_load` | Error al cargar datos | Error state en body + retry |
| `error_submit` | Error al enviar | Toast error + form habilitado |
| `error_validation` | Validación fallida | Errores inline en campos |

### 9.2 Estados de botones [OBL]

| Botón | Default | Submitting | Disabled | Error |
|-------|---------|------------|----------|-------|
| Primary | Enabled | Spinner + "Guardando..." | Grayed out | Enabled |
| Cancel | Enabled | Disabled | — | Enabled |
| Close (✕) | Visible | Disabled | — | Visible |

### 9.3 Feedback post-acción [OBL]

| Resultado | Feedback | Comportamiento |
|-----------|----------|----------------|
| Success | Toast "{{MENSAJE}}" | Auto-close en {{TIEMPO}}s |
| Error 400 | Toast error + errores inline | Mantener abierto |
| Error 409 | Toast "{{MENSAJE_CONFLICTO}}" | Mantener abierto |
| Error 500 | Toast "Error del servidor" + retry | Mantener abierto |

---

## 10) Accesibilidad (A11Y) [OBL] — **CRÍTICO**

> **Activación:** Siempre obligatorio. Esta sección es crítica para overlays.

### 10.1 Focus trap [OBL]

| Requisito | Implementación |
|-----------|----------------|
| Focus inicial | [Elegir: Primer campo / Close button / Primary CTA] |
| Tab cycling | Solo dentro del overlay |
| Shift+Tab | Ciclo reverso dentro del overlay |
| Focus on close | Return focus al elemento trigger |

### 10.2 Keyboard navigation [OBL]

| Tecla | Acción |
|-------|--------|
| Tab | Siguiente elemento focusable |
| Shift+Tab | Elemento anterior |
| ESC | Cerrar (si permitido) |
| Enter | Activar elemento focused / Submit form |
| Space | Activar botones/checkboxes |

### 10.3 ARIA attributes [OBL]

| Atributo | Valor | Elemento |
|----------|-------|----------|
| `role` | `dialog` o `alertdialog` (si destructivo) | Container |
| `aria-modal` | `true` | Container |
| `aria-labelledby` | ID del título | Container |
| `aria-describedby` | ID de descripción (si aplica) | Container |
| `aria-label` | "Cerrar" | Close button |

### 10.4 Screen readers [OBL]

| Evento | Anuncio |
|--------|---------|
| Overlay abre | Título del dialog |
| Error de validación | Mensaje de error |
| Submitting | "Guardando..." |
| Success | "{{ENTIDAD}} guardado correctamente" |
| Overlay cierra | Focus en trigger, no anuncio especial |

### 10.5 Checklist de accesibilidad [OBL]

- [ ] Focus trap implementado
- [ ] Focus inicial correcto
- [ ] Return focus al cerrar
- [ ] ESC funciona (si permitido)
- [ ] `role="dialog"` o `role="alertdialog"`
- [ ] `aria-modal="true"`
- [ ] `aria-labelledby` apunta al título
- [ ] Botones tienen labels claros
- [ ] Errores anunciados

---

## 11) Responsive [OBL]

> **Activación:** Siempre obligatorio.

### 11.1 Comportamiento por breakpoint [OBL]

| Breakpoint | Tipo de overlay | Tamaño | Posición |
|------------|-----------------|--------|----------|
| Mobile (<768px) | [Full-screen / Bottom sheet] | 100% width | [Center / Bottom] |
| Tablet (768-1024px) | Modal | {{WIDTH}} | Center |
| Desktop (>1024px) | Modal | {{WIDTH}} | Center |

### 11.2 Adaptaciones mobile [OBL]

| Elemento | Desktop | Mobile |
|----------|---------|--------|
| Close button | Top-right ✕ | Top-right ✕ o swipe down |
| Footer | Inline | Sticky bottom |
| Form fields | Side labels | Stacked labels |
| Buttons | Side by side | [Stacked / Side by side] |

### 11.3 Bottom sheet behavior [COND]

> **Activación:** Incluir si se usa bottom sheet en mobile.

| Comportamiento | Implementación |
|----------------|----------------|
| Drag handle | Visible en top |
| Swipe down | Cierra (con confirmación si hay cambios) |
| Snap points | {{PUNTOS}} (ej: 50%, 90%) |
| Keyboard open | Sheet sube para mostrar input |

---

## 12) Datos, APIs e integraciones [OBL]

> **Activación:** Siempre obligatorio.

### 12.1 Endpoints [OBL]

| Endpoint | Método | Uso | Auth |
|----------|--------|-----|------|
| `GET {{ENDPOINT}}/:id` | GET | Preload data (edit/view) | Sí |
| `POST {{ENDPOINT}}` | POST | Create | Sí |
| `PATCH {{ENDPOINT}}/:id` | PATCH | Update | Sí |
| `DELETE {{ENDPOINT}}/:id` | DELETE | Delete | Sí |

### 12.2 Request payload [OBL]

```json
{
  "{{CAMPO_1}}": "{{VALOR}}",
  "{{CAMPO_2}}": "{{VALOR}}"
}
```

### 12.3 Response handling [OBL]

| Código | Significado | UI |
|--------|-------------|-----|
| 200/201 | Éxito | Toast success + close |
| 400 | Validación fallida | Errores inline |
| 403 | Sin permisos | Toast error |
| 404 | Entidad no encontrada | Error state |
| 409 | Conflicto | Toast error con explicación |
| 422 | Regla de negocio | Toast error con explicación |
| 500 | Error servidor | Toast error + retry |

### 12.4 Optimistic updates [OPC]

| Habilitado | Comportamiento |
|------------|----------------|
| Sí | Actualizar UI inmediatamente, rollback si error |
| No | Esperar respuesta del servidor |

---

## 13) Analytics / Instrumentación [OBL]

> **Activación:** Siempre obligatorio.

### 13.1 Eventos [OBL]

| Evento | Trigger | Payload |
|--------|---------|---------|
| `overlay_open` | Overlay visible | `overlay_id, mode, source_screen, entity_id, trigger_type` |
| `overlay_close` | Overlay cerrado | `overlay_id, mode, close_method, had_changes` |
| `overlay_submit` | Click en primary CTA | `overlay_id, mode, entity_id` |
| `overlay_success` | Acción exitosa | `overlay_id, mode, entity_id, duration_ms` |
| `overlay_error` | Error mostrado | `overlay_id, mode, error_type, error_code` |
| `overlay_discard` | Cambios descartados | `overlay_id, mode` |
| `overlay_validation_error` | Validación fallida | `overlay_id, field_ids` |

### 13.2 Métricas derivadas [OBL]

| Métrica | Cálculo |
|---------|---------|
| Completion rate | `overlay_success / overlay_open` |
| Abandon rate | `overlay_discard / overlay_open` |
| Error rate | `overlay_error / overlay_submit` |
| Time to complete | `overlay_success.timestamp - overlay_open.timestamp` |

---

## 14) QA / Casos de prueba [OBL]

> **Activación:** Siempre obligatorio.

### 14.1 Casos de apertura/cierre [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TO-01 | Abrir desde trigger | Overlay visible + focus correcto |
| TO-02 | Cerrar con ✕ | Overlay cierra + focus en trigger |
| TO-03 | Cerrar con ESC | Overlay cierra (si permitido) |
| TO-04 | Cerrar con click outside | Overlay cierra (si permitido) |
| TO-05 | Cerrar con Cancel | Overlay cierra |

### 14.2 Casos de focus trap [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TF-01 | Tab en último elemento | Focus va al primero |
| TF-02 | Shift+Tab en primero | Focus va al último |
| TF-03 | Click fuera del overlay | Focus permanece dentro |

### 14.3 Casos de submit [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TS-01 | Submit válido | Success + cierra |
| TS-02 | Submit con error 400 | Errores inline + no cierra |
| TS-03 | Submit con error 500 | Toast error + retry |
| TS-04 | Submit durante loading | Bloqueado |

### 14.4 Casos de discard [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TD-01 | Cerrar sin cambios | Cierra inmediatamente |
| TD-02 | Cerrar con cambios | Warning "¿Descartar?" |
| TD-03 | Confirmar discard | Cierra sin guardar |
| TD-04 | Cancelar discard | Vuelve al overlay |

### 14.5 Casos de responsive [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TR-01 | Mobile portrait | [Full-screen / Bottom sheet] |
| TR-02 | Tablet | Modal centrado |
| TR-03 | Resize durante overlay abierto | Adapta correctamente |

---

## 15) Riesgos, supuestos y decisiones [OBL]

> **Activación:** Siempre obligatorio.

### 15.1 Riesgos identificados [OBL]

| ID | Riesgo | Probabilidad | Impacto | Mitigación |
|----|--------|--------------|---------|------------|
| R-01 | Focus trap no funciona | Baja | Alto | Testing A11Y automatizado |
| R-02 | Pérdida de datos en discard | Media | Medio | Warning claro |
| R-03 | {{RIESGO}} | {{PROB}} | {{IMPACTO}} | {{MITIGACION}} |

### 15.2 Supuestos [OBL]

| ID | Supuesto | Validado |
|----|----------|----------|
| S-01 | Design system tiene componente modal | Sí/No |
| S-02 | API soporta operaciones necesarias | Sí/No |
| S-03 | {{SUPUESTO}} | Sí/No |

### 15.3 Decisiones pendientes [OBL]

| ID | Tema | Decisión | Responsable | Fecha |
|----|------|----------|-------------|-------|
| D-01 | Click outside cierra | {{DECISION}} | UX | {{FECHA}} |
| D-02 | Auto-close on success | {{DECISION}} | UX | {{FECHA}} |
| D-03 | ESC con cambios | {{DECISION}} | UX | {{FECHA}} |

---

## 16) Checklist de aprobación [OBL]

> **Activación:** Siempre obligatorio.

### 16.1 Especificación [OBL]

- [ ] Triggers definidos (§3)
- [ ] Layout y tamaños definidos (§4)
- [ ] Overlay Inventory completo (§5)
- [ ] Modos documentados (§6)
- [ ] Acciones y CTAs definidos (§7)
- [ ] Reglas de cierre definidas (§8)

### 16.2 Accesibilidad [OBL] — **CRÍTICO**

- [ ] Focus trap especificado
- [ ] Focus inicial definido
- [ ] Return focus definido
- [ ] ARIA attributes listados
- [ ] Keyboard navigation documentada

### 16.3 UX/Técnica [OBL]

- [ ] Estados definidos (§9)
- [ ] Responsive especificado (§11)
- [ ] APIs documentadas (§12)
- [ ] Analytics instrumentado (§13)

### 16.4 QA [OBL]

- [ ] Casos de prueba documentados
- [ ] Casos de A11Y incluidos

### 16.5 Firmas de aprobación [OBL]

| Rol | Nombre | Fecha | Status |
|-----|--------|-------|--------|
| PM/PO | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| UX/UI | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| Tech Lead | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| QA | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |

---

## 17) Particularidades del proyecto [OPC]

> **Activación:** Usar para configuraciones específicas.

### 17.1 Excepciones al estándar

| Sección | Excepción | Justificación |
|---------|-----------|---------------|
| {{SECCION}} | {{EXCEPCION}} | {{JUSTIFICACION}} |

### 17.2 Notas adicionales

{{NOTAS}}

---

## 📋 ANEXOS RELACIONADOS

> Marcar los anexos que aplican:

- [ ] **Form** → Si el body contiene formulario (usar TEMPLATE_BASE_Spec_Form)
- [ ] **UXStates** → Referencia a estándar global
- [ ] **AdminRBAC** → Si hay permisos complejos

---

## 🔁 GUÍA OPERATIVA PARA AGENTES

### Cómo usar este template:

1. **Copiar** el template
2. **Definir tipo** de overlay (Modal/Drawer/Sheet)
3. **Completar §5** (Overlay Inventory) — sección núcleo
4. **Completar §10** (Accesibilidad) — crítico para overlays
5. **Reemplazar** placeholders `{{...}}`
6. **Validar** con checklist (§16)

### Secciones núcleo (mínimo viable):

- §0 Metadatos
- §1 Propósito
- §3 Triggers
- §4 Layout
- §5 **Overlay Inventory** ← NÚCLEO
- §6 Modos
- §7 Acciones
- §8 Reglas de cierre
- §9 Estados
- §10 **Accesibilidad** ← CRÍTICO
- §13 Analytics
- §16 Checklist

### Validación cruzada:

- Cada modo en §6 debe tener diferencias documentadas
- Cada acción en §7 debe tener comportamiento de error
- Cada método de cierre en §8 debe tener condiciones
- Focus trap debe estar completo en §10
- Return focus debe estar definido

### Red flags a evitar:

- ❌ Overlay sin focus trap
- ❌ Sin return focus al cerrar
- ❌ Sin warning para cambios no guardados
- ❌ Click outside cierra sin considerar cambios
- ❌ Sin loading state durante submit
- ❌ Overlay muy largo que requiere mucho scroll (considerar Wizard)
- ❌ Sin comportamiento mobile definido

---

> **Fin del template**  
> **Versión:** 2.0  
> **Última actualización:** {{FECHA_ACTUALIZACION}}
