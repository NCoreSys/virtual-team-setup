# 📊 TEMPLATE BASE — SPEC DATA GRID (Tabla Enterprise)

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

- ✅ Tabla con **filtros, sort, paginación** avanzados
- ✅ Tabla con **acciones por fila y/o bulk actions**
- ✅ Tabla con **export/import** de datos
- ✅ Tabla con **RBAC** (columnas/acciones por rol)
- ✅ Tabla con **virtualización** para grandes volúmenes
- ❌ Lista simple de cards → usar AppScreen
- ❌ Tabla decorativa sin interacción → usar AppScreen

---

# ESPECIFICACIÓN DE DATA GRID / TABLA ENTERPRISE

---

## 0) Metadatos del documento [OBL]

> **Activación:** Siempre obligatorio.

| Campo | Valor |
|-------|-------|
| **Nombre del documento** | Spec_DataGrid_{{NOMBRE_GRID}}_{{VERSION}} |
| **Proyecto** | {{NOMBRE_PROYECTO}} |
| **Módulo / Feature** | {{NOMBRE_MODULO}} |
| **Pantalla/Sección** | {{PANTALLA_DONDE_VIVE}} |
| **Data Grid** | {{NOMBRE_GRID}} |
| **ID técnico** | `grid-{{NUM}}-{{SLUG}}` (ej: `grid-01-inventory-main`) |
| **Contexto** | [Elegir: AppScreen / DashboardKPI / Admin / EntityDetail] |
| **Versión** | {{VERSION}} |
| **Estado** | [Elegir: Draft / Review / Approved / Deprecated] |
| **Prioridad** | [Elegir: Crítica / Alta / Media / Baja] |
| **Fecha** | {{FECHA_YYYY-MM-DD}} |
| **Owner (PM/PO)** | {{NOMBRE_OWNER}} |
| **UX/UI Owner** | {{NOMBRE_UX}} |
| **Tech Lead** | {{NOMBRE_TECH}} |
| **Data/BI Owner** | {{NOMBRE_DATA}} (si aplica) |
| **QA Owner** | {{NOMBRE_QA}} |

---

## 1) Propósito del Data Grid [OBL]

> **Activación:** Siempre obligatorio.

### 1.1 Descripción general [OBL]

Este data grid permite a **{{TIPO_USUARIO}}** **ver, filtrar, ordenar y actuar** sobre **{{ENTIDAD}}**.

| Campo | Valor |
|-------|-------|
| **Entidad principal** | {{ENTIDAD}} (ej: Orders, Inventory, Tickets, Customers) |
| **Operación principal** | [Elegir: Monitoreo / Gestión / Auditoría / Análisis / Planeación] |
| **Frecuencia de uso** | [Elegir: Continuo / Diario / Semanal / Ad-hoc] |

### 1.2 Objetivo de negocio [OBL]

1. {{OBJETIVO_NEGOCIO_1}} (ej: Visibilidad operativa en tiempo real)
2. {{OBJETIVO_NEGOCIO_2}} (ej: Reducción de tiempos de análisis)
3. {{OBJETIVO_NEGOCIO_3}} (ej: Control y acciones masivas)

### 1.3 Objetivo UX [OBL]

- Descubrimiento rápido de información
- Precisión y control sobre los datos
- Reducir carga cognitiva
- Performance con datasets grandes

### 1.4 KPIs [OBL]

| Métrica | Valor objetivo | Valor crítico |
|---------|----------------|---------------|
| Tiempo a primera acción | < {{VALOR}}s | > {{VALOR}}s |
| Uso de filtros (% sesiones) | {{VALOR}}% | < {{VALOR}}% |
| Export rate | {{VALOR}}% | — |
| Errores por acción | < {{VALOR}}% | > {{VALOR}}% |
| Tiempo de carga (p95) | < {{VALOR}}s | > {{VALOR}}s |

---

## 2) Alcance (Scope) [OBL]

> **Activación:** Siempre obligatorio.

### 2.1 Incluye (In Scope) [OBL]

- {{INCLUYE_1}} (ej: Columnas, filas, formatos)
- {{INCLUYE_2}} (ej: Filtros, sort, búsqueda)
- {{INCLUYE_3}} (ej: Paginación/virtualización)
- {{INCLUYE_4}} (ej: Selección single/multi)
- {{INCLUYE_5}} (ej: Acciones por fila y masivas)
- {{INCLUYE_6}} (ej: Export CSV/XLSX)

### 2.2 No incluye (Out of Scope) [OBL]

- {{EXCLUYE_1}}
- {{EXCLUYE_2}}

### 2.3 Dependencias [OBL]

| Tipo | Dependencia | Estado | Owner |
|------|-------------|--------|-------|
| API List | `{{ENDPOINT_LIST}}` | [Pendiente/Listo] | {{OWNER}} |
| API Export | `{{ENDPOINT_EXPORT}}` | [Pendiente/Listo] | {{OWNER}} |
| RBAC | {{SISTEMA_PERMISOS}} | [Pendiente/Listo] | {{OWNER}} |
| Feature Flag | {{FLAG}} | [Activo/Inactivo] | {{OWNER}} |

---

## 3) Usuarios, roles y permisos (RBAC) [OBL]

> **Activación:** Siempre obligatorio para DataGrids enterprise.

### 3.1 Matriz de permisos por acción [OBL]

| Rol | Ver tabla | Ver cols sensibles | Filtrar | Ordenar | Exportar | Acciones fila | Bulk actions | Editar | Aprobar |
|-----|-----------|-------------------|---------|---------|----------|---------------|--------------|--------|---------|
| {{ROL_1}} | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |
| {{ROL_2}} | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |
| {{ROL_ADMIN}} | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

### 3.2 Reglas de visibilidad por rol [COND]

| Elemento | Regla | Roles afectados |
|----------|-------|-----------------|
| Columnas sensibles | {{REGLA}} | {{ROLES}} |
| Filas por scope | {{REGLA}} (ej: solo su tenant/región) | {{ROLES}} |
| Acciones específicas | {{REGLA}} | {{ROLES}} |

### 3.3 Audit de acceso [COND]

> **Activación:** Incluir si hay datos sensibles o requisitos de compliance.

| Evento auditado | Datos capturados |
|-----------------|------------------|
| Vista de columna sensible | user_id, column_id, timestamp |
| Export de datos | user_id, filters, row_count, timestamp |
| Acción sobre fila | user_id, action, row_id, timestamp |

---

## 4) Definición del dataset [OBL]

> **Activación:** Siempre obligatorio.

### 4.1 Entidad principal [OBL]

| Campo | Valor |
|-------|-------|
| **Entidad** | {{ENTIDAD}} |
| **Primary Key** | `{{PRIMARY_KEY}}` |
| **Sistema fuente** | {{SISTEMA}} |
| **Tabla/Colección** | {{TABLA}} |

### 4.2 Volumen esperado [OBL]

| Métrica | Valor |
|---------|-------|
| Filas típicas | {{VALOR}} |
| Filas p95 | {{VALOR}} |
| Filas máximo | {{VALOR}} |
| Crecimiento mensual | {{VALOR}}% |

### 4.3 Refresh y latencia [OBL]

| Métrica | Valor |
|---------|-------|
| Frecuencia de refresh | [Elegir: Real-time / Near real-time / Cada X min / Manual] |
| Latencia de datos | {{VALOR}} |
| Load time p50 | < {{VALOR}}s |
| Load time p95 | < {{VALOR}}s |

---

## 5) Columnas (Column Inventory) [OBL] — **SECCIÓN NÚCLEO**

> **Activación:** Siempre obligatorio. Esta es la sección más importante del template.

### 5.1 Tabla de columnas [OBL]

| # | Column ID | Header | Tipo | Formato | Visible default | Ocultable | Sortable | Filterable | Width | Align | Sensible |
|--:|-----------|--------|------|---------|-----------------|-----------|----------|------------|-------|-------|----------|
| 1 | `{{COL_ID}}` | {{HEADER}} | [string/number/currency/date/enum/boolean] | {{FORMATO}} | Sí/No | Sí/No | Sí/No | Sí/No | {{WIDTH}}px | [left/center/right] | Sí/No |
| 2 | `{{COL_ID}}` | {{HEADER}} | {{TIPO}} | {{FORMATO}} | Sí/No | Sí/No | Sí/No | Sí/No | {{WIDTH}}px | {{ALIGN}} | Sí/No |
| 3 | `{{COL_ID}}` | {{HEADER}} | {{TIPO}} | {{FORMATO}} | Sí/No | Sí/No | Sí/No | Sí/No | {{WIDTH}}px | {{ALIGN}} | Sí/No |

### 5.2 Reglas de formato [OBL]

| Tipo | Formato | Ejemplo |
|------|---------|---------|
| Currency | {{FORMATO}} | $1,234.56 MXN |
| Date | {{FORMATO}} | DD/MM/YYYY HH:mm |
| Number | {{FORMATO}} | 1,234.56 |
| Percentage | {{FORMATO}} | 12.5% |
| Enum/Status | Badge con color | `active` → green badge |
| Boolean | [Checkbox / Yes-No / Icon] | ✓ / ✗ |

### 5.3 Columnas calculadas [COND]

> **Activación:** Incluir si hay columnas derivadas.

| Column ID | Fórmula | Fuente | Recalcula |
|-----------|---------|--------|-----------|
| `{{COL_ID}}` | {{FORMULA}} | {{FUENTE}} | [On load / On demand] |

### 5.4 Columnas sensibles [COND]

> **Activación:** Incluir si hay datos PII o confidenciales.

| Column ID | Tipo de dato | Mask para roles | Roles con acceso full |
|-----------|--------------|-----------------|----------------------|
| `{{COL_ID}}` | {{TIPO}} (ej: PII, Financiero) | {{MASK}} (ej: ****1234) | {{ROLES}} |

### 5.5 Columna de acciones [OBL]

| Posición | Sticky | Acciones disponibles |
|----------|--------|---------------------|
| [Primera / Última] | Sí/No | {{ACCIONES}} |

---

## 6) Filtrado, búsqueda y ordenamiento [OBL]

> **Activación:** Siempre obligatorio.

### 6.1 Búsqueda global [OBL]

| Campo | Valor |
|-------|-------|
| Habilitada | Sí/No |
| Campos incluidos | {{CAMPOS}} |
| Min caracteres | {{NUM}} |
| Debounce | {{MS}}ms |
| Server-side | Sí/No |

### 6.2 Filtros [OBL]

| Filter ID | Campo(s) | Tipo UI | Opciones/Rango | Default | Persistente | Server-side |
|-----------|----------|---------|----------------|---------|-------------|-------------|
| `{{FILTER_ID}}` | `{{CAMPO}}` | [Dropdown/Multi-select/Date range/Number range/Text] | {{OPCIONES}} | {{DEFAULT}} | Sí/No | Sí/No |
| `{{FILTER_ID}}` | `{{CAMPO}}` | {{TIPO}} | {{OPCIONES}} | {{DEFAULT}} | Sí/No | Sí/No |

### 6.3 Filtros predefinidos (Quick filters) [OPC]

| Filter preset | Nombre | Filtros aplicados |
|---------------|--------|-------------------|
| `{{PRESET_ID}}` | {{NOMBRE}} | {{FILTROS}} |

### 6.4 Ordenamiento (Sort) [OBL]

| Campo | Valor |
|-------|-------|
| Multi-sort | Sí/No |
| Default sort | `{{COLUMNA}}` {{ASC/DESC}} |
| Tie-breaker | `{{COLUMNA}}` |
| Server-side | Sí/No |

### 6.5 Persistencia de filtros [OPC]

| Mecanismo | Implementación |
|-----------|----------------|
| URL params | `?filter_status=active&sort=created_at` |
| localStorage | Por usuario |
| Server (saved views) | Guardado con nombre |

---

## 7) Paginación / Virtualización [OBL]

> **Activación:** Siempre obligatorio.

### 7.1 Estrategia seleccionada [OBL]

| Estrategia | Cuándo usar | Seleccionada |
|------------|-------------|--------------|
| **Paginación server-side** | Datasets grandes, control preciso | ☐ |
| **Paginación client-side** | Datasets pequeños (<1000 filas) | ☐ |
| **Virtualización (windowing)** | Scroll infinito, UX fluida | ☐ |
| **Infinite scroll** | Mobile, feeds | ☐ |

### 7.2 Configuración de paginación [COND]

> **Activación:** Incluir si se usa paginación.

| Campo | Valor |
|-------|-------|
| Page size options | {{OPTIONS}} (ej: [10, 25, 50, 100]) |
| Default page size | {{DEFAULT}} |
| Max page size | {{MAX}} |
| Show total count | Sí/No |
| Show page selector | Sí/No |

### 7.3 Configuración de virtualización [COND]

> **Activación:** Incluir si se usa virtualización.

| Campo | Valor |
|-------|-------|
| Row height | {{HEIGHT}}px |
| Overscan | {{ROWS}} filas |
| Buffer | {{ROWS}} filas |

### 7.4 Infinite scroll [COND]

> **Activación:** Incluir si se usa infinite scroll.

| Campo | Valor |
|-------|-------|
| Trigger threshold | {{PX}}px del bottom |
| Loading indicator | Spinner / Skeleton rows |
| Batch size | {{ROWS}} filas |

---

## 8) Selección y acciones [OBL]

> **Activación:** Siempre obligatorio.

### 8.1 Selección de filas [OBL]

| Campo | Valor |
|-------|-------|
| Tipo de selección | [Elegir: None / Single / Multi] |
| Select all (page) | Sí/No |
| Select all (query) | Sí/No |
| Checkbox column | Sí/No |
| Click en fila selecciona | Sí/No |

### 8.2 Acciones por fila (Row actions) [OBL]

| Acción | Label | Icono | Rol mínimo | Confirmación | Resultado | Errores |
|--------|-------|-------|------------|--------------|-----------|---------|
| `view` | Ver | 👁 | {{ROL}} | No | Navega a detalle | 404 |
| `edit` | Editar | ✏️ | {{ROL}} | No | Abre modal/page | 403, 409 |
| `delete` | Eliminar | 🗑 | {{ROL}} | Sí (destructiva) | Elimina fila | 403, 409 |
| `{{ACTION}}` | {{LABEL}} | {{ICON}} | {{ROL}} | Sí/No | {{RESULTADO}} | {{ERRORES}} |

### 8.3 Acciones masivas (Bulk actions) [COND]

> **Activación:** Incluir si hay acciones sobre múltiples filas.

| Acción | Label | Aplica a | Límite | Confirmación | Async | Audit |
|--------|-------|----------|--------|--------------|-------|-------|
| `export` | Exportar | Selección / Query | {{LIMITE}} | Sí/No | Sí | Sí |
| `bulk_update` | Actualizar | Selección | {{LIMITE}} | Sí | Sí/No | Sí |
| `bulk_delete` | Eliminar | Selección | {{LIMITE}} | Sí (destructiva) | Sí/No | Sí |
| `{{ACTION}}` | {{LABEL}} | {{APLICA}} | {{LIMITE}} | Sí/No | Sí/No | Sí/No |

### 8.4 Confirmaciones destructivas [OBL]

| Acción | Mensaje de confirmación | CTA confirmar | CTA cancelar |
|--------|------------------------|---------------|--------------|
| Delete single | "{{MENSAJE}}" | "Eliminar" | "Cancelar" |
| Bulk delete | "{{MENSAJE}} ({{N}} items)" | "Eliminar todos" | "Cancelar" |
| `{{ACTION}}` | "{{MENSAJE}}" | {{CTA}} | {{CTA}} |

---

## 9) Export / Import [COND]

> **Activación:** Incluir si el grid soporta export/import.

### 9.1 Export [COND]

| Campo | Valor |
|-------|-------|
| Formatos | [CSV / XLSX / PDF] |
| Scope | [Selección / Página actual / Query completa] |
| Columnas exportadas | [Visibles / Todas / Seleccionables] |
| Generación | [Síncrona / Asíncrona] |
| Notificación | [Descarga directa / Email / In-app notification] |
| Límite de filas | {{LIMITE}} |

### 9.2 Import [COND]

| Campo | Valor |
|-------|-------|
| Formatos | [CSV / XLSX] |
| Plantilla disponible | Sí/No |
| Validaciones | {{VALIDACIONES}} |
| Preview antes de importar | Sí/No |
| Rollback disponible | Sí/No |
| Límite de filas | {{LIMITE}} |

---

## 10) Estados (UX States) [OBL]

> **Activación:** Siempre obligatorio. Referencia: `UXStates_Pack_{{PROYECTO}}`

### 10.1 Estados aplicables [OBL]

| Estado | Contexto | UI |
|--------|----------|-----|
| `loading_initial` | Carga inicial | Skeleton de filas |
| `loading_partial` | Filtro/sort/paginación | Overlay o skeleton |
| `empty_no_results` | Query sin resultados | Empty state con limpiar filtros |
| `empty_first_time` | Sin datos en sistema | Empty state con CTA crear |
| `error_network` | Sin conexión | Error con retry |
| `error_server_5xx` | Error de API | Error con retry |
| `success_action` | Acción completada | Toast |
| `error_action` | Acción fallida | Toast error |

### 10.2 Loading de tabla [OBL]

| Tipo | Implementación |
|------|----------------|
| Inicial | {{NUM}} skeleton rows |
| Paginación | [Overlay / Skeleton / Spinner] |
| Acción | Spinner en botón |

---

## 11) Accesibilidad (A11Y) [OBL]

> **Activación:** Siempre obligatorio.

### 11.1 Estructura semántica [OBL]

| Requisito | Implementación |
|-----------|----------------|
| Elemento | `<table>` con `role="grid"` o equivalente |
| Headers | `<th>` con `scope="col"` |
| Celdas | `<td>` o `role="gridcell"` |
| Caption | Título descriptivo de la tabla |

### 11.2 Navegación por teclado [OBL]

| Tecla | Acción |
|-------|--------|
| Tab | Entrar/salir de la tabla |
| Arrow keys | Navegar celdas |
| Enter | Activar acción / Expandir fila |
| Space | Seleccionar fila (si checkbox) |
| Home/End | Primera/última celda de fila |
| Ctrl+Home/End | Primera/última celda de tabla |

### 11.3 Screen readers [OBL]

| Elemento | Anuncio |
|----------|---------|
| Header de columna | Nombre + sortable/sorted |
| Celda | Valor + header asociado |
| Fila seleccionada | "Seleccionada" |
| Acciones | Label descriptivo |

### 11.4 Focus visible [OBL]

- Focus outline en celda activa
- Focus en controles (filtros, botones)
- Skip link para saltar tabla (si muy grande)

---

## 12) Performance [OBL]

> **Activación:** Siempre obligatorio para DataGrids enterprise.

### 12.1 Objetivos [OBL]

| Métrica | Objetivo | Crítico |
|---------|----------|---------|
| Initial load (p50) | < {{VALOR}}s | > {{VALOR}}s |
| Initial load (p95) | < {{VALOR}}s | > {{VALOR}}s |
| Filter/sort response | < {{VALOR}}ms | > {{VALOR}}ms |
| Scroll FPS | > 30fps | < 20fps |
| Action latency | < {{VALOR}}ms | > {{VALOR}}ms |

### 12.2 Estrategias de optimización [OBL]

| Estrategia | Aplica | Implementación |
|------------|--------|----------------|
| Virtualización | Sí/No | {{IMPLEMENTACION}} |
| Server-side filter/sort | Sí/No | {{IMPLEMENTACION}} |
| Debounce en búsqueda | Sí/No | {{MS}}ms |
| Caché de queries | Sí/No | {{TTL}} |
| Lazy load de columnas | Sí/No | {{COLUMNAS}} |
| Prefetch de páginas | Sí/No | {{PAGINAS}} |

### 12.3 Riesgos de performance [OPC]

| Riesgo | Impacto | Mitigación |
|--------|---------|------------|
| Demasiadas columnas (>20) | Render lento | Column picker, lazy columns |
| Heavy cell renders | Scroll lento | Memoization, virtualization |
| Filtros costosos | Latencia | Server-side, índices |
| Export grande | Timeout | Async export, límites |

---

## 13) Analytics / Instrumentación [OBL]

> **Activación:** Siempre obligatorio.

### 13.1 Eventos [OBL]

| Evento | Trigger | Payload |
|--------|---------|---------|
| `grid_view` | Grid visible | `grid_id, screen_id, user_role, row_count` |
| `grid_filter_applied` | Filtro cambiado | `grid_id, filter_id, filter_value` |
| `grid_filter_cleared` | Filtros limpiados | `grid_id` |
| `grid_sort_applied` | Sort cambiado | `grid_id, column_id, direction` |
| `grid_search` | Búsqueda ejecutada | `grid_id, query_length, results_count` |
| `grid_page_changed` | Cambio de página | `grid_id, page, page_size` |
| `grid_row_selected` | Fila seleccionada | `grid_id, row_id, selected_count` |
| `grid_row_action` | Acción en fila | `grid_id, action, row_id` |
| `grid_bulk_action` | Acción masiva | `grid_id, action, selected_count` |
| `grid_export_requested` | Export iniciado | `grid_id, format, row_count` |
| `grid_export_completed` | Export listo | `grid_id, format, duration_ms` |
| `grid_error` | Error mostrado | `grid_id, error_type, context` |

### 13.2 Métricas derivadas [OBL]

| Métrica | Cálculo |
|---------|---------|
| Filter usage rate | `sessions con filter / total sessions` |
| Export rate | `exports / grid_views` |
| Action completion rate | `action_success / action_initiated` |
| Time to first action | `first_action.timestamp - grid_view.timestamp` |

---

## 14) QA / Casos de prueba [OBL]

> **Activación:** Siempre obligatorio.

### 14.1 Casos funcionales [OBL]

| ID | Caso | Resultado esperado | Prioridad |
|----|------|-------------------|-----------|
| TF-01 | Sort por columna | Orden correcto, indicador visible | Crítica |
| TF-02 | Filtro aplicado | Filas filtradas, count actualizado | Crítica |
| TF-03 | Búsqueda global | Resultados correctos | Alta |
| TF-04 | Paginación | Navegación correcta, datos consistentes | Crítica |
| TF-05 | Selección múltiple | Checkbox funcional, count correcto | Alta |
| TF-06 | Acción por fila | Acción ejecutada, feedback mostrado | Crítica |
| TF-07 | Bulk action | Acción aplicada a todos, feedback | Alta |
| TF-08 | Export | Archivo generado con datos correctos | Alta |

### 14.2 Casos de seguridad/RBAC [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TS-01 | Columna sensible oculta por rol | No visible para rol sin permiso |
| TS-02 | Acción bloqueada por rol | Botón disabled o no visible |
| TS-03 | Export bloqueado por rol | Opción no disponible |

### 14.3 Casos de performance [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TP-01 | Carga inicial con {{N}} filas | < {{TIEMPO}}s |
| TP-02 | Scroll con {{N}} filas | Smooth (>30fps) |
| TP-03 | Filtro en dataset grande | < {{TIEMPO}}s |

### 14.4 Casos de accesibilidad [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TA-01 | Navegación con teclado | Todas las celdas alcanzables |
| TA-02 | Sort anunciado | Screen reader lee estado |
| TA-03 | Acciones accesibles | Todas activables con teclado |

---

## 15) Riesgos, supuestos y decisiones [OBL]

> **Activación:** Siempre obligatorio.

### 15.1 Riesgos identificados [OBL]

| ID | Riesgo | Probabilidad | Impacto | Mitigación |
|----|--------|--------------|---------|------------|
| R-01 | Performance con volumen alto | [Alta/Media/Baja] | Alto | Virtualización, server-side |
| R-02 | Permisos mal configurados | [Alta/Media/Baja] | Alto | Tests RBAC, audit |
| R-03 | {{RIESGO}} | {{PROB}} | {{IMPACTO}} | {{MITIGACION}} |

### 15.2 Supuestos [OBL]

| ID | Supuesto | Validado |
|----|----------|----------|
| S-01 | API soporta filtros server-side | Sí/No |
| S-02 | API soporta paginación | Sí/No |
| S-03 | {{SUPUESTO}} | Sí/No |

### 15.3 Decisiones pendientes [OBL]

| ID | Tema | Decisión | Responsable | Fecha |
|----|------|----------|-------------|-------|
| D-01 | Paginación vs virtualización | {{DECISION}} | {{RESPONSABLE}} | {{FECHA}} |
| D-02 | Columnas default visibles | {{DECISION}} | {{RESPONSABLE}} | {{FECHA}} |
| D-03 | Límite de export | {{DECISION}} | {{RESPONSABLE}} | {{FECHA}} |

---

## 16) Checklist de aprobación [OBL]

> **Activación:** Siempre obligatorio.

### 16.1 Especificación [OBL]

- [ ] Column Inventory completo (§5)
- [ ] Filtros y sort definidos (§6)
- [ ] Estrategia paginación/virtualización (§7)
- [ ] Acciones row y bulk definidas (§8)
- [ ] Export/Import especificado (si aplica)

### 16.2 Seguridad [OBL]

- [ ] RBAC por columna y acción
- [ ] Columnas sensibles identificadas
- [ ] Audit log definido (si aplica)

### 16.3 UX/Performance [OBL]

- [ ] Estados definidos (loading/empty/error)
- [ ] Objetivos de performance establecidos
- [ ] Accesibilidad definida

### 16.4 QA [OBL]

- [ ] Casos de prueba documentados
- [ ] Analytics instrumentado

### 16.5 Firmas de aprobación [OBL]

| Rol | Nombre | Fecha | Status |
|-----|--------|-------|--------|
| PM/PO | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| UX/UI | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| Tech Lead | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| Data/BI | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado/N/A] |
| QA | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |

---

## 17) Particularidades del proyecto [OPC]

> **Activación:** Usar para configuraciones custom o excepciones.

### 17.1 Excepciones al estándar

| Sección | Excepción | Justificación | Aprobado por |
|---------|-----------|---------------|--------------|
| {{SECCION}} | {{EXCEPCION}} | {{JUSTIFICACION}} | {{APROBADOR}} |

### 17.2 Notas adicionales

{{NOTAS}}

---

## 📋 ANEXOS RELACIONADOS

> Marcar los anexos que aplican:

- [ ] **AdminRBAC** → Si hay permisos complejos (usar TEMPLATE_BASE_Spec_AdminRBAC)
- [ ] **UXStates** → Referencia a estándar global
- [ ] **ModalOverlay** → Si acciones abren modales complejos

---

## 🔁 GUÍA OPERATIVA PARA AGENTES

### Cómo usar este template:

1. **Copiar** el template
2. **Completar §5 primero** (Column Inventory) — es la sección núcleo
3. **Definir §3** (RBAC) — crítico para enterprise
4. **Reemplazar** placeholders `{{...}}`
5. **Omitir** secciones `[COND]` si no aplican
6. **Validar** con checklist (§16)

### Secciones núcleo (mínimo viable):

- §0 Metadatos
- §1 Propósito
- §3 RBAC
- §4 Dataset
- §5 **Column Inventory** ← CRÍTICO
- §6 Filtros y sort
- §7 Paginación
- §8 Acciones
- §10 Estados
- §11 Accesibilidad
- §13 Analytics
- §16 Checklist

### Validación cruzada:

- Cada columna en §5 con `Filterable=Sí` debe tener filtro en §6
- Cada columna en §5 con `Sensible=Sí` debe tener regla en §5.4
- Cada acción en §8 debe tener permiso en §3
- Cada acción destructiva debe tener confirmación en §8.4
- Cada estado en §10 debe referenciar UXStates Pack

### Red flags a evitar:

- ❌ Grid sin Column Inventory
- ❌ Columnas sensibles sin RBAC
- ❌ Acciones destructivas sin confirmación
- ❌ Sin estrategia de paginación/virtualización
- ❌ Sin objetivos de performance
- ❌ >20 columnas sin column picker

---

> **Fin del template**  
> **Versión:** 2.0  
> **Última actualización:** {{FECHA_ACTUALIZACION}}
