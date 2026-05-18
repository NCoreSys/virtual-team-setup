# 🗂️ TEMPLATE BASE — SPEC ENTITY DETAIL (Detalle de Entidad)

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

### Placeholders

- `{{NOMBRE}}` → Reemplazar con valor específico del proyecto
- `[Elegir: opción1 / opción2]` → Seleccionar una opción
- `[Listar...]` → Agregar items según aplique

### Cuándo usar este template

- ✅ Pantalla de **registro maestro** de una entidad
- ✅ Vista con **header resumen + tabs/secciones + acciones**
- ✅ Entidad con **state machine** (estados y transiciones)
- ✅ Vista con **timeline/activity log**
- ❌ Lista de entidades → usar DataGrid
- ❌ Página de contenido editorial → usar ContentSEO
- ❌ Dashboard con KPIs → usar DashboardKPI

---

# ESPECIFICACIÓN DE ENTITY DETAIL

---

## 0) Metadatos del documento [OBL]

> **Activación:** Siempre obligatorio.

| Campo | Valor |
|-------|-------|
| **Nombre del documento** | Spec_EntityDetail_{{NOMBRE_ENTIDAD}}_{{VERSION}} |
| **Proyecto** | {{NOMBRE_PROYECTO}} |
| **Módulo / Feature** | {{NOMBRE_MODULO}} |
| **Entidad** | {{NOMBRE_ENTIDAD}} (ej: Order, Product, Customer, Ticket, Asset, Case) |
| **Pantalla** | {{NOMBRE_PANTALLA}} |
| **ID técnico** | `detail-{{NUM}}-{{SLUG}}` (ej: `detail-01-order`) |
| **Ruta** | `{{RUTA}}` (ej: `/orders/:id`) |
| **Contexto** | [Elegir: AppScreen / Admin / Dashboard drill-down / CRM] |
| **Versión** | {{VERSION}} |
| **Estado** | [Elegir: Draft / Review / Approved / Deprecated] |
| **Prioridad** | [Elegir: Crítica / Alta / Media / Baja] |
| **Fecha** | {{FECHA_YYYY-MM-DD}} |
| **Owner (PM/PO)** | {{NOMBRE_OWNER}} |
| **UX/UI Owner** | {{NOMBRE_UX}} |
| **Tech Lead** | {{NOMBRE_TECH}} |
| **QA Owner** | {{NOMBRE_QA}} |

---

## 1) Propósito de la pantalla [OBL]

> **Activación:** Siempre obligatorio.

### 1.1 Descripción general [OBL]

Esta pantalla muestra el **registro maestro** de **{{ENTIDAD}}** y permite acciones contextuales.

| Campo | Valor |
|-------|-------|
| **Contenido principal** | Resumen + metadata + secciones/tabs + timeline |
| **Tipo de entidad** | {{TIPO}} (ej: transaccional, master data, documento) |
| **Frecuencia de acceso** | [Elegir: Alta / Media / Baja] |

### 1.2 Objetivo de negocio [OBL]

1. {{OBJETIVO_NEGOCIO_1}} (ej: Visibilidad completa del registro)
2. {{OBJETIVO_NEGOCIO_2}} (ej: Habilitar decisiones y acciones)
3. {{OBJETIVO_NEGOCIO_3}} (ej: Trazabilidad y auditoría)

### 1.3 Objetivo UX [OBL]

- Encontrar información crítica rápidamente
- Reducir saltos entre pantallas
- Acciones claras y seguras
- Contexto completo sin sobrecarga

### 1.4 KPIs [OBL]

| Métrica | Valor objetivo |
|---------|----------------|
| Tiempo a encontrar dato clave | < {{VALOR}}s |
| Acciones iniciadas desde detalle | {{VALOR}}% |
| Tasa de error en acciones | < {{VALOR}}% |
| Tab switch rate | {{VALOR}}% |

---

## 2) Alcance (Scope) [OBL]

> **Activación:** Siempre obligatorio.

### 2.1 Incluye (In Scope) [OBL]

- {{INCLUYE_1}} (ej: Header resumen con estado)
- {{INCLUYE_2}} (ej: Tabs/secciones de información)
- {{INCLUYE_3}} (ej: Acciones por estado)
- {{INCLUYE_4}} (ej: Links a entidades relacionadas)
- {{INCLUYE_5}} (ej: Timeline/activity log)

### 2.2 No incluye (Out of Scope) [OBL]

- {{EXCLUYE_1}}
- {{EXCLUYE_2}}

### 2.3 Dependencias [OBL]

| Tipo | Dependencia | Estado | Owner |
|------|-------------|--------|-------|
| API Detail | `{{ENDPOINT}}` | [Pendiente/Listo] | {{OWNER}} |
| API Actions | `{{ENDPOINT}}` | [Pendiente/Listo] | {{OWNER}} |
| RBAC | {{SISTEMA}} | [Pendiente/Listo] | {{OWNER}} |
| Related entities | {{ENTIDADES}} | [Pendiente/Listo] | {{OWNER}} |

---

## 3) Usuarios, roles y permisos [OBL]

> **Activación:** Siempre obligatorio.

### 3.1 Matriz de permisos [OBL]

| Rol | Ver detalle | Ver campos sensibles | Ejecutar acciones | Editar | Aprobar | Eliminar | Restricciones |
|-----|-------------|---------------------|-------------------|--------|---------|----------|---------------|
| {{ROL_VIEWER}} | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | Solo lectura |
| {{ROL_OPERATOR}} | ✅ | ✅/❌ | ✅ | ✅/❌ | ❌ | ❌ | {{RESTRICCION}} |
| {{ROL_ADMIN}} | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — |

### 3.2 Reglas de visibilidad por rol [COND]

| Elemento | Regla | Roles afectados |
|----------|-------|-----------------|
| Campos sensibles | {{REGLA}} | {{ROLES}} |
| Secciones específicas | {{REGLA}} | {{ROLES}} |
| Acciones | {{REGLA}} | {{ROLES}} |

---

## 4) Modelo de datos de la entidad [OBL]

> **Activación:** Siempre obligatorio.

### 4.1 Identidad [OBL]

| Campo | Valor |
|-------|-------|
| **Primary Key** | `{{PK}}` (ej: `id`, `order_id`) |
| **Display ID** | `{{DISPLAY_ID}}` (ej: `ORD-12345`) |
| **Claves secundarias** | {{CLAVES}} |

### 4.2 State machine [OBL]

| Estado | Descripción | Acciones permitidas | Transiciones posibles |
|--------|-------------|---------------------|----------------------|
| `{{ESTADO_1}}` | {{DESCRIPCION}} | {{ACCIONES}} | → {{ESTADOS}} |
| `{{ESTADO_2}}` | {{DESCRIPCION}} | {{ACCIONES}} | → {{ESTADOS}} |
| `{{ESTADO_3}}` | {{DESCRIPCION}} | {{ACCIONES}} | → {{ESTADOS}} |
| `{{ESTADO_FINAL}}` | {{DESCRIPCION}} | {{ACCIONES}} | Terminal |

### 4.3 Diagrama de estados [OPC]

```
[Draft] --submit--> [Pending Review]
                          |
            +-------------+-------------+
            |                           |
       approve                       reject
            |                           |
            v                           v
       [Approved] --cancel-->      [Rejected]
            |
       complete
            |
            v
       [Completed]
```

### 4.4 Campos críticos [OBL]

| Campo | Tipo | Descripción | Siempre visible |
|-------|------|-------------|-----------------|
| `id` | string | Identificador único | Sí |
| `status` | enum | Estado actual | Sí |
| `owner` | reference | Propietario/responsable | Sí |
| `created_at` | datetime | Fecha de creación | Sí |
| `updated_at` | datetime | Última modificación | Sí |
| `{{CAMPO}}` | {{TIPO}} | {{DESCRIPCION}} | Sí/No |

---

## 5) Layout y estructura [OBL]

> **Activación:** Siempre obligatorio.

### 5.1 Estructura de zonas [OBL]

```
┌─────────────────────────────────────────────────────┐
│  BREADCRUMBS (opcional)                             │
├─────────────────────────────────────────────────────┤
│  HEADER RESUMEN (sticky opcional)                   │
│  [Status] Título | Metadata | [Acciones primarias]  │
├─────────────────────────────────────────────────────┤
│  TABS / SECTIONS                                    │
│  [Tab 1] [Tab 2] [Tab 3] [Tab 4]                   │
├─────────────────────────┬───────────────────────────┤
│  CONTENIDO DEL TAB      │  PANEL LATERAL (opcional) │
│                         │  - Quick actions          │
│                         │  - Summary                │
│                         │  - Related entities       │
├─────────────────────────┴───────────────────────────┤
│  TIMELINE / ACTIVITY LOG (opcional)                 │
└─────────────────────────────────────────────────────┘
```

### 5.2 Jerarquía visual [OBL]

| Nivel | Contenido | Posición |
|-------|-----------|----------|
| **Primario** | Status + Título + Acciones críticas | Header (top) |
| **Secundario** | Datos principales por tab | Centro |
| **Terciario** | Historial, metadata secundaria | Abajo / Panel lateral |

### 5.3 Responsive [OBL]

| Breakpoint | Comportamiento |
|------------|----------------|
| Mobile | Header compacto, tabs en scroll/dropdown, sin panel lateral |
| Tablet | Header normal, tabs scroll, panel colapsable |
| Desktop | Layout completo con panel lateral |

---

## 6) Header de entidad (Summary Header) [OBL] — **SECCIÓN NÚCLEO**

> **Activación:** Siempre obligatorio.

### 6.1 Estructura del header [OBL]

```
┌─────────────────────────────────────────────────────────────┐
│ [←Back]                                              [⋮More]│
├─────────────────────────────────────────────────────────────┤
│ [🟢 Active]  Order #ORD-12345                               │
│ Customer: John Doe | Created: Jan 15, 2025 | Owner: Maria   │
├─────────────────────────────────────────────────────────────┤
│ [Edit]  [Approve]  [Cancel]                                 │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 Campos del header [OBL]

| Campo | Fuente | Formato | Posición | Tooltip | Sensible |
|-------|--------|---------|----------|---------|----------|
| `status` | API | Badge con color | Izquierda del título | {{TOOLTIP}} | No |
| `display_id` | API | String | Título principal | — | No |
| `{{CAMPO_1}}` | API | {{FORMATO}} | Metadata row | {{TOOLTIP}} | Sí/No |
| `{{CAMPO_2}}` | API | {{FORMATO}} | Metadata row | {{TOOLTIP}} | Sí/No |
| `{{CAMPO_3}}` | API | {{FORMATO}} | Metadata row | {{TOOLTIP}} | Sí/No |

### 6.3 Acciones del header [OBL]

| Acción | Label | Icono | Tipo | Rol mínimo | Estados válidos | Confirmación | Resultado |
|--------|-------|-------|------|------------|-----------------|--------------|-----------|
| `edit` | Editar | ✏️ | Primary | {{ROL}} | {{ESTADOS}} | No | Abre editor |
| `approve` | Aprobar | ✓ | Primary | {{ROL}} | {{ESTADOS}} | Sí | Cambia estado |
| `cancel` | Cancelar | ✗ | Danger | {{ROL}} | {{ESTADOS}} | Sí | Cambia estado |
| `{{ACTION}}` | {{LABEL}} | {{ICON}} | {{TIPO}} | {{ROL}} | {{ESTADOS}} | Sí/No | {{RESULTADO}} |

### 6.4 Comportamiento del header [OBL]

| Comportamiento | Valor |
|----------------|-------|
| Sticky on scroll | Sí/No |
| Compacto en mobile | Sí |
| Acciones en overflow menu (mobile) | Sí |

---

## 7) Secciones / Tabs (Section Inventory) [OBL] — **SECCIÓN NÚCLEO**

> **Activación:** Siempre obligatorio.

### 7.1 Tabla de secciones [OBL]

| Orden | Section ID | Nombre | Tipo | Objetivo | Componentes | Default visible | Roles |
|------:|------------|--------|------|----------|-------------|-----------------|-------|
| 1 | `sec-overview` | Overview | Tab | Vista general | Cards, key-value | Sí (default) | Todos |
| 2 | `sec-details` | Detalles | Tab | Info completa | Data list | Sí | Todos |
| 3 | `sec-related` | Relacionados | Tab | Entidades vinculadas | List + links | Sí | Todos |
| 4 | `sec-activity` | Actividad | Tab | Timeline | Timeline | Sí | {{ROLES}} |
| 5 | `sec-{{ID}}` | {{NOMBRE}} | {{TIPO}} | {{OBJETIVO}} | {{COMPONENTES}} | Sí/No | {{ROLES}} |

### 7.2 Detalle por sección [OBL]

> Repetir por cada sección crítica.

#### Sección: {{NOMBRE_SECCION}}

| Campo | Valor |
|-------|-------|
| **Section ID** | `sec-{{ID}}` |
| **Nombre** | {{NOMBRE}} |
| **Tipo** | [Tab / Section / Collapsible] |
| **Objetivo** | {{OBJETIVO}} |

| Componente | Tipo | Datos | Acciones |
|------------|------|-------|----------|
| {{COMPONENTE_1}} | {{TIPO}} | {{DATOS}} | {{ACCIONES}} |
| {{COMPONENTE_2}} | {{TIPO}} | {{DATOS}} | {{ACCIONES}} |

### 7.3 Reglas de visibilidad [COND]

| Sección | Condición para mostrar | Condición para ocultar |
|---------|------------------------|------------------------|
| `sec-{{ID}}` | {{CONDICION}} | {{CONDICION}} |

---

## 8) Componentes y patrones comunes [OBL]

> **Activación:** Siempre obligatorio.

### 8.1 Data lists (Key-Value pairs) [OBL]

| Comportamiento | Implementación |
|----------------|----------------|
| Layout | [Elegir: 1 columna / 2 columnas / Responsive] |
| Truncado | Ellipsis + tooltip |
| Empty value | "—" o "No especificado" |
| Copy to clipboard | Sí/No (en campos copiables) |
| Links | Campos con navegación |

### 8.2 Related entities [COND]

> **Activación:** Incluir si hay entidades relacionadas.

| Entidad relacionada | Relación | Display | Link | Quick actions |
|---------------------|----------|---------|------|---------------|
| {{ENTIDAD}} | {{RELACION}} (1:1, 1:N, N:M) | {{DISPLAY}} | {{LINK}} | {{ACCIONES}} |

### 8.3 Timeline / Activity log [COND]

> **Activación:** Incluir si hay historial de cambios.

| Campo | Valor |
|-------|-------|
| Eventos incluidos | {{EVENTOS}} (ej: status changes, comments, edits) |
| Ordenamiento | [Más reciente primero / Más antiguo primero] |
| Paginación | {{CONFIG}} |
| Expandible | Sí/No (ver diff) |

| Elemento del evento | Fuente |
|---------------------|--------|
| Tipo de evento | `event_type` |
| Usuario | `user` |
| Timestamp | `created_at` |
| Descripción | `description` |
| Diff (opcional) | `changes` |

---

## 9) Acciones contextuales [OBL]

> **Activación:** Siempre obligatorio.

### 9.1 Acciones por estado [OBL]

| Estado actual | Acciones disponibles | Requiere confirmación | Audit log |
|---------------|---------------------|----------------------|-----------|
| `{{ESTADO_1}}` | {{ACCIONES}} | {{CONFIRMACION}} | Sí/No |
| `{{ESTADO_2}}` | {{ACCIONES}} | {{CONFIRMACION}} | Sí/No |
| `{{ESTADO_3}}` | {{ACCIONES}} | {{CONFIRMACION}} | Sí/No |

### 9.2 Detalle de acciones [OBL]

| Acción | Trigger | Validaciones | Resultado | Error handling |
|--------|---------|--------------|-----------|----------------|
| `{{ACTION}}` | {{TRIGGER}} | {{VALIDACIONES}} | {{RESULTADO}} | {{ERRORES}} |

### 9.3 Acciones destructivas [OBL]

| Acción | Mensaje de confirmación | CTA confirmar | CTA cancelar | Requiere input |
|--------|------------------------|---------------|--------------|----------------|
| `delete` | "¿Eliminar {{ENTIDAD}}? Esta acción no se puede deshacer." | "Eliminar" | "Cancelar" | No |
| `cancel` | "{{MENSAJE}}" | {{CTA}} | {{CTA}} | [Sí: razón / No] |

### 9.4 Notificaciones post-acción [OPC]

| Acción | Notificación al usuario | Notificación a otros |
|--------|-------------------------|---------------------|
| `{{ACTION}}` | {{NOTIFICACION}} | {{NOTIFICACION}} |

---

## 10) Navegación y deep links [OBL]

> **Activación:** Siempre obligatorio.

### 10.1 Rutas [OBL]

| Tipo | Ruta | Parámetros |
|------|------|------------|
| Detalle | `{{BASE_PATH}}/:id` | `id` = entity ID |
| Tab específico | `{{BASE_PATH}}/:id?tab={{TAB}}` | `tab` = section ID |
| Con contexto | `{{BASE_PATH}}/:id?from={{SOURCE}}` | `from` = origen |

### 10.2 Navegación entrante [OBL]

| Origen | Comportamiento |
|--------|----------------|
| DataGrid (lista) | Tab default |
| Dashboard KPI | Tab relacionado con el drill-down |
| Search | Tab default |
| Notificación | Tab de actividad (si aplica) |
| Deep link externo | Tab especificado o default |

### 10.3 Navegación saliente [OBL]

| Destino | Trigger | Comportamiento |
|---------|---------|----------------|
| Back (lista) | Back button / breadcrumb | Preservar filtros |
| Related entity | Click en link | Nueva página o modal |
| Edit modal | Edit action | Modal o página |

---

## 11) Datos, APIs e integraciones [OBL]

> **Activación:** Siempre obligatorio.

### 11.1 Endpoints [OBL]

| Endpoint | Método | Uso | Auth | Cache |
|----------|--------|-----|------|-------|
| `GET {{BASE}}/{{ENTITY}}/:id` | GET | Cargar detalle | Sí | {{TTL}} |
| `PATCH {{BASE}}/{{ENTITY}}/:id` | PATCH | Actualizar campos | Sí | — |
| `POST {{BASE}}/{{ENTITY}}/:id/{{ACTION}}` | POST | Ejecutar acción | Sí | — |
| `GET {{BASE}}/{{ENTITY}}/:id/activity` | GET | Timeline | Sí | {{TTL}} |

### 11.2 Response de detalle [OBL]

```json
{
  "id": "{{ID}}",
  "status": "{{STATUS}}",
  "display_id": "{{DISPLAY_ID}}",
  "{{CAMPO}}": "{{VALOR}}",
  "related_entities": {
    "{{ENTIDAD}}": { "id": "...", "name": "..." }
  },
  "metadata": {
    "created_at": "{{ISO_DATE}}",
    "updated_at": "{{ISO_DATE}}",
    "created_by": { "id": "...", "name": "..." }
  }
}
```

### 11.3 Errores y handling [OBL]

| Código | Significado | UI |
|--------|-------------|-----|
| 200 | Éxito | Mostrar detalle |
| 404 | Entidad no encontrada | Error page "No encontrado" |
| 403 | Sin permisos | Error page "Sin acceso" |
| 409 | Conflicto (acción) | Toast error + mensaje |
| 500 | Error servidor | Error state + retry |

### 11.4 Refresh post-acción [OBL]

| Acción | Refresh behavior |
|--------|------------------|
| Status change | Refetch entity completo |
| Edit field | Optimistic update + refetch |
| Delete | Redirect a lista |

---

## 12) Estados (UX States) [OBL]

> **Activación:** Siempre obligatorio. Referencia: `UXStates_Pack_{{PROYECTO}}`

### 12.1 Estados de página [OBL]

| Estado | Trigger | UI |
|--------|---------|-----|
| `loading` | Carga inicial | Skeleton header + skeleton tabs |
| `error_404` | Entity not found | Error page con CTA "Volver a lista" |
| `error_403` | Sin permisos | Error page con CTA "Solicitar acceso" |
| `error_500` | Error de servidor | Error state con retry |

### 12.2 Estados de sección [OBL]

| Estado | Trigger | UI |
|--------|---------|-----|
| `loading` | Carga de tab | Skeleton del contenido |
| `empty` | Sección sin datos | Empty state contextual |
| `error` | Error de carga | Error inline con retry |

### 12.3 Estados de acción [OBL]

| Estado | Trigger | UI |
|--------|---------|-----|
| `loading` | Acción en progreso | Spinner en botón, disabled |
| `success` | Acción exitosa | Toast success |
| `error` | Acción fallida | Toast error + mensaje |

---

## 13) Accesibilidad (A11Y) [OBL]

> **Activación:** Siempre obligatorio.

### 13.1 Tabs accesibles [OBL]

| Requisito | Implementación |
|-----------|----------------|
| Role | `role="tablist"` + `role="tab"` + `role="tabpanel"` |
| Selection | `aria-selected="true"` en tab activo |
| Panel association | `aria-controls` + `aria-labelledby` |
| Keyboard | Arrow keys para navegar tabs |

### 13.2 Focus management [OBL]

| Evento | Comportamiento |
|--------|----------------|
| Cambio de tab | Focus en primer elemento del panel |
| Acción abre modal | Focus en modal |
| Modal cerrado | Return focus a trigger |
| Error de acción | Focus en mensaje de error |

### 13.3 Screen readers [OBL]

| Elemento | Anuncio |
|----------|---------|
| Status badge | "Estado: {{STATUS}}" |
| Tabs | "Tab {{N}} de {{TOTAL}}: {{NOMBRE}}" |
| Acciones | Label descriptivo de la acción |
| Timeline event | "{{FECHA}}: {{USUARIO}} - {{EVENTO}}" |

---

## 14) Responsive [OBL]

> **Activación:** Siempre obligatorio.

### 14.1 Breakpoints [OBL]

| Breakpoint | Header | Tabs | Panel lateral | Acciones |
|------------|--------|------|---------------|----------|
| Mobile | Compacto (2 líneas) | Scroll horizontal | Oculto | Overflow menu |
| Tablet | Normal | Scroll si necesario | Colapsable | Visible |
| Desktop | Completo | Todos visibles | Visible | Visible |

### 14.2 Comportamientos específicos [OBL]

| Elemento | Mobile | Desktop |
|----------|--------|---------|
| Metadata del header | Stack vertical | Inline |
| Acciones secundarias | En menú ⋮ | Visible |
| Related entities | Lista simple | Cards o tabla |
| Timeline | Compacta | Expandida |

---

## 15) Analytics / Instrumentación [OBL]

> **Activación:** Siempre obligatorio.

### 15.1 Eventos [OBL]

| Evento | Trigger | Payload |
|--------|---------|---------|
| `detail_view` | Página visible | `entity_type, entity_id, user_role, entry_point` |
| `detail_loaded` | Carga completa | `entity_type, entity_id, load_time_ms` |
| `tab_switch` | Cambio de tab | `entity_type, entity_id, from_tab, to_tab` |
| `action_initiated` | Click en acción | `entity_type, entity_id, action, current_status` |
| `action_confirmed` | Confirmación de acción | `entity_type, entity_id, action` |
| `action_completed` | Acción exitosa | `entity_type, entity_id, action, new_status` |
| `action_failed` | Acción fallida | `entity_type, entity_id, action, error_type` |
| `related_entity_click` | Click en entidad relacionada | `entity_type, entity_id, related_type, related_id` |
| `timeline_expand` | Expandir evento | `entity_type, entity_id, event_id` |
| `detail_error` | Error mostrado | `entity_type, entity_id, error_type` |

### 15.2 Métricas derivadas [OBL]

| Métrica | Cálculo |
|---------|---------|
| Time to first action | `action_initiated.timestamp - detail_view.timestamp` |
| Action success rate | `action_completed / action_initiated` |
| Tab engagement | `tab_switch count por sesión` |
| Related entity exploration | `related_entity_click / detail_view` |

---

## 16) QA / Casos de prueba [OBL]

> **Activación:** Siempre obligatorio.

### 16.1 Casos funcionales [OBL]

| ID | Caso | Resultado esperado | Prioridad |
|----|------|-------------------|-----------|
| TF-01 | Carga de detalle | Datos correctos en header y tabs | Crítica |
| TF-02 | Cambio de tab | Contenido correcto por tab | Alta |
| TF-03 | Acción por estado | Solo acciones válidas visibles | Crítica |
| TF-04 | Ejecutar acción con confirmación | Modal + resultado correcto | Alta |
| TF-05 | Link a entidad relacionada | Navegación correcta | Alta |
| TF-06 | Timeline carga eventos | Eventos ordenados correctamente | Media |

### 16.2 Casos de RBAC [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TR-01 | Viewer ve detalle | Solo lectura, sin acciones |
| TR-02 | Operator ve acciones | Acciones según permisos |
| TR-03 | Campo sensible oculto | Masked o no visible |
| TR-04 | Sección restringida | No visible para rol |

### 16.3 Casos de estados [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TS-01 | Entity not found (404) | Error page con back |
| TS-02 | Sin permisos (403) | Error page con solicitar |
| TS-03 | Tab sin datos | Empty state contextual |
| TS-04 | Acción falla | Toast error + no cambio |

### 16.4 Casos de accesibilidad [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TA-01 | Navegación de tabs con teclado | Arrow keys funcionan |
| TA-02 | Focus post-action | Focus correcto |
| TA-03 | Screen reader en header | Status y título anunciados |

---

## 17) Riesgos, supuestos y decisiones [OBL]

> **Activación:** Siempre obligatorio.

### 17.1 Riesgos identificados [OBL]

| ID | Riesgo | Probabilidad | Impacto | Mitigación |
|----|--------|--------------|---------|------------|
| R-01 | State machine incompleta | [Alta/Media/Baja] | Alto | Documentar todos los estados |
| R-02 | Campos sensibles expuestos | {{PROB}} | {{IMPACTO}} | RBAC + tests |
| R-03 | {{RIESGO}} | {{PROB}} | {{IMPACTO}} | {{MITIGACION}} |

### 17.2 Supuestos [OBL]

| ID | Supuesto | Validado |
|----|----------|----------|
| S-01 | API de detalle disponible | Sí/No |
| S-02 | State machine definida | Sí/No |
| S-03 | {{SUPUESTO}} | Sí/No |

### 17.3 Decisiones pendientes [OBL]

| ID | Tema | Decisión | Responsable | Fecha |
|----|------|----------|-------------|-------|
| D-01 | State machine final | {{DECISION}} | {{RESPONSABLE}} | {{FECHA}} |
| D-02 | Campos sensibles | {{DECISION}} | {{RESPONSABLE}} | {{FECHA}} |
| D-03 | Tabs a incluir | {{DECISION}} | {{RESPONSABLE}} | {{FECHA}} |

---

## 18) Checklist de aprobación [OBL]

> **Activación:** Siempre obligatorio.

### 18.1 Especificación [OBL]

- [ ] Header definido (§6)
- [ ] Section Inventory completo (§7)
- [ ] State machine documentada (§4.2)
- [ ] Acciones por estado definidas (§9)

### 18.2 Seguridad [OBL]

- [ ] RBAC por campo y acción
- [ ] Campos sensibles identificados
- [ ] Acciones destructivas con confirmación

### 18.3 UX [OBL]

- [ ] Estados definidos (loading/error/empty)
- [ ] Responsive especificado
- [ ] Accesibilidad definida

### 18.4 QA [OBL]

- [ ] Casos de prueba documentados
- [ ] Analytics instrumentado

### 18.5 Firmas de aprobación [OBL]

| Rol | Nombre | Fecha | Status |
|-----|--------|-------|--------|
| PM/PO | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| UX/UI | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| Tech Lead | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| QA | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |

---

## 19) Particularidades del proyecto [OPC]

> **Activación:** Usar para configuraciones específicas de esta entidad.

### 19.1 Excepciones al estándar

| Sección | Excepción | Justificación |
|---------|-----------|---------------|
| {{SECCION}} | {{EXCEPCION}} | {{JUSTIFICACION}} |

### 19.2 Notas adicionales

{{NOTAS}}

---

## 📋 ANEXOS RELACIONADOS

> Marcar los anexos que aplican:

- [ ] **AdminRBAC** → Si hay permisos complejos (usar TEMPLATE_BASE_Spec_AdminRBAC)
- [ ] **ModalOverlay** → Si acciones abren modales complejos
- [ ] **UXStates** → Referencia a estándar global
- [ ] **Form** → Si hay edición inline compleja

---

## 🔁 GUÍA OPERATIVA PARA AGENTES

### Cómo usar este template:

1. **Copiar** el template
2. **Completar §4.2** (State machine) — fundamental para acciones
3. **Completar §6** (Header) y **§7** (Sections) — secciones núcleo
4. **Mapear acciones** por estado en §9
5. **Reemplazar** placeholders `{{...}}`
6. **Validar** con checklist (§18)

### Secciones núcleo (mínimo viable):

- §0 Metadatos
- §1 Propósito
- §3 RBAC
- §4 **State machine** ← CRÍTICO
- §5 Layout
- §6 **Header** ← CRÍTICO
- §7 **Section Inventory** ← CRÍTICO
- §9 Acciones por estado
- §11 APIs
- §12 Estados
- §15 Analytics
- §18 Checklist

### Validación cruzada:

- Cada estado en §4.2 debe tener acciones en §9
- Cada sección en §7 debe tener componentes definidos
- Cada acción destructiva debe tener confirmación en §9.3
- Cada acción debe tener evento en §15
- Header y tabs deben tener behavior responsive en §14

### Red flags a evitar:

- ❌ Entity sin state machine clara
- ❌ Acciones sin validación de estado
- ❌ Campos sensibles sin RBAC
- ❌ Acciones destructivas sin confirmación
- ❌ Tabs sin lazy loading (performance)
- ❌ Timeline sin paginación (si hay muchos eventos)

---

> **Fin del template**  
> **Versión:** 2.0  
> **Última actualización:** {{FECHA_ACTUALIZACION}}
