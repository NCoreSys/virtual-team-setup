# 📈 TEMPLATE BASE — SPEC DASHBOARD KPI (Analytics)

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

- ✅ Dashboard con **KPIs definidos** y métricas de negocio
- ✅ Dashboard con **comparaciones temporales** (WoW, MoM, YoY)
- ✅ Dashboard con **drill-down** a detalle
- ✅ Dashboard **ejecutivo u operativo** con decisiones basadas en datos
- ❌ Dashboard solo de navegación sin métricas → usar AppScreen
- ❌ Página de reportes estáticos → usar ContentSEO

---

# ESPECIFICACIÓN DE DASHBOARD KPI / ANALYTICS

---

## 0) Metadatos del documento [OBL]

> **Activación:** Siempre obligatorio.

| Campo | Valor |
|-------|-------|
| **Nombre del documento** | Spec_Dashboard_{{NOMBRE_DASHBOARD}}_{{VERSION}} |
| **Proyecto** | {{NOMBRE_PROYECTO}} |
| **Módulo / Feature** | {{NOMBRE_MODULO}} |
| **Dashboard** | {{NOMBRE_DASHBOARD}} |
| **ID técnico** | `dash-{{NUM}}-{{SLUG}}` (ej: `dash-01-exec-overview`) |
| **Tipo de dashboard** | [Elegir: Ejecutivo / Operativo / Analítico / Control Tower] |
| **Versión** | {{VERSION}} |
| **Estado** | [Elegir: Draft / Review / Approved / Deprecated] |
| **Prioridad** | [Elegir: Crítica / Alta / Media / Baja] |
| **Fecha** | {{FECHA_YYYY-MM-DD}} |
| **Owner (PM/PO)** | {{NOMBRE_OWNER}} |
| **UX/UI Owner** | {{NOMBRE_UX}} |
| **Data/BI Owner** | {{NOMBRE_DATA}} |
| **Tech Lead** | {{NOMBRE_TECH}} |
| **QA Owner** | {{NOMBRE_QA}} |

---

## 1) Propósito del dashboard [OBL]

> **Activación:** Siempre obligatorio.

### 1.1 Descripción general [OBL]

Este dashboard permite a **{{TIPO_USUARIO}}** monitorear **{{AREA}}** mediante KPIs y visualizaciones.

| Campo | Valor |
|-------|-------|
| **Objetivo principal** | [Elegir: Decisiones ejecutivas / Operación diaria / Auditoría / Seguimiento de objetivos / Detección de anomalías] |
| **Frecuencia de uso** | [Elegir: Continuo / Diario / Semanal / Mensual / Ad-hoc] |
| **Audiencia principal** | {{AUDIENCIA}} |

### 1.2 Objetivo de negocio [OBL]

1. {{OBJETIVO_NEGOCIO_1}} (ej: Alinear equipos con metas)
2. {{OBJETIVO_NEGOCIO_2}} (ej: Detectar riesgos temprano)
3. {{OBJETIVO_NEGOCIO_3}} (ej: Priorizar acciones con datos)

### 1.3 Objetivo UX [OBL]

- Claridad y rapidez (insight en segundos)
- Comparabilidad (periodos, benchmarks)
- Drill-down consistente
- Evitar ambigüedad de definición

### 1.4 KPIs de producto (uso del dashboard) [OBL]

| Métrica | Valor objetivo |
|---------|----------------|
| Frecuencia de uso | {{VALOR}} veces/semana |
| Tiempo a primer insight | < {{VALOR}}s |
| Acciones iniciadas desde dashboard | {{VALOR}}% |
| Drill-down usage rate | {{VALOR}}% |

---

## 2) Alcance (Scope) [OBL]

> **Activación:** Siempre obligatorio.

### 2.1 Incluye (In Scope) [OBL]

- {{INCLUYE_1}} (ej: KPI cards con valores y deltas)
- {{INCLUYE_2}} (ej: Gráficos de tendencia)
- {{INCLUYE_3}} (ej: Filtros globales por periodo/segmento)
- {{INCLUYE_4}} (ej: Drill-down a detalle)
- {{INCLUYE_5}} (ej: Glosario/definiciones de métricas)

### 2.2 No incluye (Out of Scope) [OBL]

- {{EXCLUYE_1}}
- {{EXCLUYE_2}}

### 2.3 Dependencias [OBL]

| Tipo | Dependencia | Estado | Owner |
|------|-------------|--------|-------|
| Data source | {{FUENTE}} | [Pendiente/Listo] | {{OWNER}} |
| API | {{ENDPOINT}} | [Pendiente/Listo] | {{OWNER}} |
| Catálogo de métricas | {{CATALOGO}} | [Pendiente/Listo] | {{OWNER}} |
| Refresh pipeline | {{PIPELINE}} | [Pendiente/Listo] | {{OWNER}} |

---

## 3) Usuarios, roles y permisos [OBL]

> **Activación:** Siempre obligatorio para dashboards enterprise.

### 3.1 Matriz de permisos [OBL]

| Rol | Ver dashboard | Ver métricas sensibles | Ver drill-down | Exportar | Scope |
|-----|---------------|------------------------|----------------|----------|-------|
| {{ROL_1}} | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | {{SCOPE}} |
| {{ROL_2}} | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | {{SCOPE}} |
| {{ROL_ADMIN}} | ✅ | ✅ | ✅ | ✅ | Global |

### 3.2 Reglas de scope [COND]

> **Activación:** Incluir si hay filtrado de datos por rol.

| Rol | Filtro aplicado | Ejemplo |
|-----|-----------------|---------|
| {{ROL}} | {{FILTRO}} | Solo ve datos de su región/tenant |

### 3.3 Audit de acceso [COND]

> **Activación:** Incluir para métricas sensibles.

| Evento auditado | Datos capturados |
|-----------------|------------------|
| Vista de métrica sensible | user_id, kpi_id, timestamp |
| Export de datos | user_id, filters, timestamp |

---

## 4) Definiciones de métricas (KPI Dictionary) [OBL] — **SECCIÓN NÚCLEO**

> **Activación:** Siempre obligatorio. Esta sección evita discusiones futuras ("¿qué significa este número?").

### 4.1 Catálogo de KPIs [OBL]

| KPI ID | Nombre | Definición exacta | Fórmula | Unidad | Fuente de verdad | Granularidad | Refresh | Owner | Sensible |
|--------|--------|-------------------|---------|--------|------------------|--------------|---------|-------|----------|
| `kpi-01` | {{NOMBRE}} | {{DEFINICION}} | {{FORMULA}} | [%/$/MXN/#/ratio] | {{FUENTE}} | [hourly/daily/weekly] | {{REFRESH}} | {{OWNER}} | Sí/No |
| `kpi-02` | {{NOMBRE}} | {{DEFINICION}} | {{FORMULA}} | {{UNIDAD}} | {{FUENTE}} | {{GRANULARIDAD}} | {{REFRESH}} | {{OWNER}} | Sí/No |
| `kpi-03` | {{NOMBRE}} | {{DEFINICION}} | {{FORMULA}} | {{UNIDAD}} | {{FUENTE}} | {{GRANULARIDAD}} | {{REFRESH}} | {{OWNER}} | Sí/No |

### 4.2 Detalle por KPI [OBL]

> Repetir por cada KPI crítico.

#### KPI: {{NOMBRE_KPI}}

| Campo | Valor |
|-------|-------|
| **ID** | `kpi-{{NUM}}` |
| **Nombre display** | {{NOMBRE}} |
| **Definición de negocio** | {{DEFINICION_COMPLETA}} |
| **Fórmula** | `{{FORMULA}}` |
| **Unidad** | {{UNIDAD}} |
| **Fuente de verdad** | {{SISTEMA/TABLA}} |
| **Granularidad** | {{GRANULARIDAD}} |
| **Latencia de datos** | {{LATENCIA}} |
| **Objetivo/Target** | {{VALOR_OBJETIVO}} |
| **Umbral de alerta** | {{UMBRAL}} |
| **Comparación default** | [Elegir: vs periodo anterior / vs target / vs benchmark] |
| **Owner de definición** | {{OWNER}} |

### 4.3 Periodos oficiales [OBL]

| Campo | Valor |
|-------|-------|
| **Periodo default** | [Elegir: Last 7d / Last 30d / MTD / QTD / YTD / Custom] |
| **Periodos disponibles** | {{LISTA_PERIODOS}} |
| **Comparación default** | [Elegir: WoW / MoM / QoQ / YoY / vs Target] |
| **Timezone** | {{TIMEZONE}} |
| **Inicio de semana** | [Elegir: Lunes / Domingo] |
| **Cierre de mes** | {{DIA}} |

### 4.4 Reglas de formato y display [OBL]

| Tipo | Formato | Ejemplo |
|------|---------|---------|
| Porcentaje | {{FORMATO}} | 12.5% |
| Moneda | {{FORMATO}} | $1,234.56 MXN |
| Número grande | {{FORMATO}} | 1.2M, 45K |
| Decimales | {{REGLA}} | 2 decimales para %, 0 para counts |
| Delta positivo | {{FORMATO}} | ▲ +12.5% (verde) |
| Delta negativo | {{FORMATO}} | ▼ -8.3% (rojo) |
| Delta neutro | {{FORMATO}} | — 0% (gris) |

---

## 5) Layout del dashboard [OBL]

> **Activación:** Siempre obligatorio.

### 5.1 Estructura de zonas [OBL]

```
┌─────────────────────────────────────────────────────┐
│  HEADER: Título + Filtros globales + Data freshness │
├─────────────────────────────────────────────────────┤
│  KPI CARDS: Métricas principales (overview)         │
│  [KPI 1] [KPI 2] [KPI 3] [KPI 4]                    │
├─────────────────────────────────────────────────────┤
│  CHARTS: Tendencias y distribuciones                │
│  [Chart 1: Trend]        [Chart 2: Breakdown]       │
├─────────────────────────────────────────────────────┤
│  DETAIL: Tablas / Drill-down                        │
│  [DataGrid o Lista]                                 │
├─────────────────────────────────────────────────────┤
│  INSIGHTS/ALERTS (opcional)                         │
└─────────────────────────────────────────────────────┘
```

### 5.2 Jerarquía visual [OBL]

| Nivel | Contenido | Posición |
|-------|-----------|----------|
| **Primario** | KPIs críticos (North Star metrics) | Top, más grande |
| **Secundario** | Tendencias y breakdowns | Medio |
| **Terciario** | Detalle y drill-down | Abajo |

### 5.3 Responsive [OBL]

| Breakpoint | Layout |
|------------|--------|
| Mobile | KPI cards stack, charts full-width |
| Tablet | 2 columnas de cards, charts stack |
| Desktop | Grid completo, charts side-by-side |

---

## 6) Filtros globales [OBL]

> **Activación:** Siempre obligatorio.

### 6.1 Tabla de filtros [OBL]

| Filter ID | Label | Tipo | Opciones | Default | Persistente | Afecta |
|-----------|-------|------|----------|---------|-------------|--------|
| `date_range` | Periodo | Date range picker | {{OPCIONES}} | Last 30d | Sí | Todos |
| `comparison` | Comparar con | Dropdown | WoW, MoM, YoY, Target | MoM | Sí | KPIs con delta |
| `{{FILTER_ID}}` | {{LABEL}} | {{TIPO}} | {{OPCIONES}} | {{DEFAULT}} | Sí/No | {{WIDGETS}} |

### 6.2 Comportamiento de filtros [OBL]

| Comportamiento | Implementación |
|----------------|----------------|
| Aplicación | [Elegir: Automática / Con botón Apply] |
| Reset | Botón "Limpiar filtros" |
| Interdependencia | {{REGLAS}} (ej: región filtra ciudades) |

### 6.3 Persistencia y sharing [OPC]

| Mecanismo | Implementación |
|-----------|----------------|
| URL params | `?period=last_30d&region=mx` |
| localStorage | Guardar última selección |
| Saved views | Guardar combinación con nombre |
| Share link | Copiar URL con filtros |

---

## 7) Componentes del dashboard [OBL]

> **Activación:** Siempre obligatorio.

### 7.1 KPI Cards [OBL]

| Card ID | KPI | Posición | Tamaño | Drill-down |
|---------|-----|----------|--------|------------|
| `card-01` | `kpi-01` | Row 1, Col 1 | [Small/Medium/Large] | {{DESTINO}} |
| `card-02` | `kpi-02` | Row 1, Col 2 | {{TAMAÑO}} | {{DESTINO}} |

#### Anatomía de KPI Card [OBL]

```
┌─────────────────────────────┐
│ [ℹ️] Nombre del KPI         │ ← Header con tooltip
├─────────────────────────────┤
│      1,234.56               │ ← Valor principal
│      ▲ +12.5% vs MoM        │ ← Delta y comparación
│      Target: 1,500          │ ← Target (opcional)
└─────────────────────────────┘
```

| Elemento | Requerido | Interacción |
|----------|-----------|-------------|
| Nombre | Sí | — |
| Tooltip con definición | Sí | Hover/click en ℹ️ |
| Valor principal | Sí | — |
| Delta (cambio) | Sí | Color según dirección |
| Periodo de comparación | Sí | — |
| Target/Goal | Opcional | — |
| Sparkline | Opcional | — |
| Click → drill-down | Opcional | Navega a detalle |

### 7.2 Charts [OBL]

> Repetir por cada chart.

#### Chart: {{NOMBRE_CHART}}

| Campo | Valor |
|-------|-------|
| **Chart ID** | `chart-{{NUM}}` |
| **Tipo** | [Elegir: Line / Bar / Area / Pie / Donut / Stacked / Combo] |
| **KPIs mostrados** | {{KPIS}} |
| **Dimensión X** | {{DIMENSION}} (ej: date, category) |
| **Métrica Y** | {{METRICA}} |
| **Series** | {{SERIES}} (si hay múltiples líneas) |
| **Posición** | Row {{N}}, Col {{N}} |
| **Tamaño** | {{TAMAÑO}} |

| Interacción | Comportamiento |
|-------------|----------------|
| Hover | Tooltip con valores |
| Click en punto | {{COMPORTAMIENTO}} |
| Click en leyenda | Toggle serie |
| Drill-down | {{DESTINO}} |

| Estado | UI |
|--------|-----|
| Loading | Skeleton del chart |
| Empty | "Sin datos para este periodo" |
| Error | "Error al cargar" + retry |

### 7.3 Tabla de detalle [COND]

> **Activación:** Incluir si hay tabla de drill-down. Referencia: TEMPLATE_BASE_Spec_DataGrid.

| Campo | Valor |
|-------|-------|
| Referencia | `grid-{{ID}}` |
| Posición | {{POSICION}} |
| Relación con KPIs | Desglose de `{{KPI}}` |

### 7.4 Alerts / Insights [COND]

> **Activación:** Incluir si hay alertas automáticas o insights.

| Alert ID | Condición | Severidad | Mensaje | CTA |
|----------|-----------|-----------|---------|-----|
| `alert-01` | {{CONDICION}} | [Info/Warning/Critical] | {{MENSAJE}} | {{CTA}} |

---

## 8) Interacciones y drill-down [OBL]

> **Activación:** Siempre obligatorio.

### 8.1 Drill-down paths [OBL]

| Origen | Elemento clickeable | Destino | Tipo | Filtros aplicados |
|--------|---------------------|---------|------|-------------------|
| KPI Card | Card completa | {{DESTINO}} | [Modal/Page/Section] | {{FILTROS}} |
| Chart | Punto/barra | {{DESTINO}} | {{TIPO}} | Periodo del punto |
| Chart | Leyenda | Toggle serie | Inline | — |
| Tabla | Fila | Entity detail | Page | Entity ID |

### 8.2 Tooltips y definiciones [OBL]

| Elemento | Contenido del tooltip |
|----------|----------------------|
| KPI Card ℹ️ | Definición completa + fórmula + fuente |
| Chart punto | Valor + fecha + comparación |
| Chart serie | Nombre + valor actual |

### 8.3 Glosario / Help [OPC]

| Implementación | Ubicación |
|----------------|-----------|
| Tooltip inline | En cada KPI |
| Panel lateral | Botón "Definiciones" |
| Página separada | Link en header |

---

## 9) Datos, APIs y refresh [OBL]

> **Activación:** Siempre obligatorio.

### 9.1 Endpoints [OBL]

| Endpoint | Método | Uso | Params | Cache TTL |
|----------|--------|-----|--------|-----------|
| `{{ENDPOINT_KPIS}}` | GET | KPI values | period, filters | {{TTL}} |
| `{{ENDPOINT_CHARTS}}` | GET | Chart data | period, granularity | {{TTL}} |
| `{{ENDPOINT_EXPORT}}` | POST | Export data | format, filters | — |

### 9.2 Estrategia de carga [OBL]

| Estrategia | Implementación |
|------------|----------------|
| Carga inicial | [Elegir: Todo junto / KPIs primero, charts después / Paralelo] |
| Prioridad | KPIs > Charts > Detail |
| Lazy load | Charts bajo el fold |

### 9.3 Refresh y cache [OBL]

| Comportamiento | Configuración |
|----------------|---------------|
| Auto-refresh | [Elegir: Sí, cada {{INTERVALO}} / No] |
| Manual refresh | Botón en header |
| Stale-while-revalidate | Sí/No |
| Cache invalidation | {{TRIGGER}} |

### 9.4 Data freshness [OBL]

| Elemento | Implementación |
|----------|----------------|
| Indicador de frescura | "Última actualización: {{TIMESTAMP}}" |
| Datos retrasados | Warning banner si > {{UMBRAL}} |
| Gaps en series | [Elegir: Interpolar / Mostrar vacío / Indicador] |

---

## 10) Estados (UX States) [OBL]

> **Activación:** Siempre obligatorio. Referencia: `UXStates_Pack_{{PROYECTO}}`

### 10.1 Estados por componente [OBL]

| Componente | Loading | Empty | Error | Partial Error |
|------------|---------|-------|-------|---------------|
| Dashboard completo | Skeleton full | — | Error page | — |
| KPI Card | Skeleton card | "—" | "Error" + retry | Individual |
| Chart | Skeleton chart | "Sin datos" | "Error" + retry | Individual |
| Filtros | Disabled | — | — | — |

### 10.2 Comportamiento de errores parciales [OBL]

| Escenario | Comportamiento |
|-----------|----------------|
| 1 KPI falla | Mostrar error solo en ese KPI, resto funciona |
| 1 Chart falla | Mostrar error en chart, resto funciona |
| API principal falla | Error de página completa |

---

## 11) Accesibilidad (A11Y) [OBL]

> **Activación:** Siempre obligatorio.

### 11.1 Charts accesibles [OBL]

| Requisito | Implementación |
|-----------|----------------|
| Alternativa textual | Tabla de datos colapsable |
| Screen reader | Descripción del chart + resumen de datos |
| Colores | No depender solo de color, usar patrones |
| Contraste | WCAG AA para texto y líneas |

### 11.2 Navegación [OBL]

| Requisito | Implementación |
|-----------|----------------|
| Tab order | Lógico: filtros → KPIs → charts → detail |
| Focus visible | En todos los elementos interactivos |
| Skip links | Saltar a secciones principales |

### 11.3 Tooltips accesibles [OBL]

| Requisito | Implementación |
|-----------|----------------|
| Trigger | Hover + focus |
| Dismissable | Escape |
| Contenido | Readable por screen reader |

---

## 12) Performance [OBL]

> **Activación:** Siempre obligatorio.

### 12.1 Objetivos [OBL]

| Métrica | Objetivo | Crítico |
|---------|----------|---------|
| Initial load (KPIs visibles) | < {{VALOR}}s | > {{VALOR}}s |
| Full dashboard load | < {{VALOR}}s | > {{VALOR}}s |
| Filter response | < {{VALOR}}ms | > {{VALOR}}ms |
| Chart render | < {{VALOR}}ms | > {{VALOR}}ms |

### 12.2 Estrategias [OBL]

| Estrategia | Implementación |
|------------|----------------|
| Batch endpoints | Un request para múltiples KPIs |
| Lazy load charts | Cargar cuando visible en viewport |
| Limitar puntos en series | Max {{NUM}} puntos, agregar si más |
| Cache de queries | {{TTL}} |
| Prefetch | Precargar drill-down probable |

### 12.3 Riesgos [OPC]

| Riesgo | Impacto | Mitigación |
|--------|---------|------------|
| Demasiados KPIs | Render lento | Limitar a {{NUM}} visibles |
| Series muy largas | Chart lento | Agregar/downsampling |
| Filtros pesados | Latencia | Server-side, índices |

---

## 13) Analytics / Instrumentación [OBL]

> **Activación:** Siempre obligatorio.

### 13.1 Eventos [OBL]

| Evento | Trigger | Payload |
|--------|---------|---------|
| `dashboard_view` | Dashboard visible | `dashboard_id, user_role, filters` |
| `dashboard_loaded` | Carga completa | `dashboard_id, load_time_ms` |
| `kpi_tooltip_open` | Hover en ℹ️ | `dashboard_id, kpi_id` |
| `kpi_click` | Click en KPI card | `dashboard_id, kpi_id` |
| `filter_applied` | Cambio de filtro | `dashboard_id, filter_id, value` |
| `chart_interaction` | Interacción con chart | `dashboard_id, chart_id, interaction_type` |
| `drilldown_open` | Navegación a detalle | `dashboard_id, source, destination` |
| `dashboard_export` | Export iniciado | `dashboard_id, format` |
| `dashboard_error` | Error mostrado | `dashboard_id, error_type, component` |

### 13.2 Métricas derivadas [OBL]

| Métrica | Cálculo |
|---------|---------|
| Time to insight | `first_interaction.timestamp - dashboard_view.timestamp` |
| Drill-down rate | `drilldown_open / dashboard_view` |
| Filter usage | `sessions con filter / total sessions` |
| Error rate | `dashboard_error / dashboard_view` |

---

## 14) QA / Casos de prueba [OBL]

> **Activación:** Siempre obligatorio.

### 14.1 Casos de datos [OBL]

| ID | Caso | Resultado esperado | Prioridad |
|----|------|-------------------|-----------|
| TD-01 | KPIs muestran valores correctos | Match con fuente | Crítica |
| TD-02 | Fórmulas calculadas correctamente | Match con definición | Crítica |
| TD-03 | Deltas correctos vs periodo anterior | Cálculo correcto | Alta |
| TD-04 | Charts reflejan datos filtrados | Datos consistentes | Alta |

### 14.2 Casos funcionales [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TF-01 | Filtro por periodo | Todos los widgets se actualizan |
| TF-02 | Drill-down desde KPI | Navegación correcta |
| TF-03 | Tooltip muestra definición | Contenido completo |
| TF-04 | Export de datos | Archivo con datos correctos |

### 14.3 Casos de estados [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TS-01 | Periodo sin datos | Empty state en charts |
| TS-02 | Error de API | Error state con retry |
| TS-03 | Error parcial (1 KPI) | Solo ese KPI muestra error |

### 14.4 Casos de accesibilidad [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TA-01 | Navegación con teclado | Todos los elementos alcanzables |
| TA-02 | Chart con screen reader | Descripción + tabla alternativa |
| TA-03 | Tooltips accesibles | Activables con focus |

---

## 15) Riesgos, supuestos y decisiones [OBL]

> **Activación:** Siempre obligatorio.

### 15.1 Riesgos identificados [OBL]

| ID | Riesgo | Probabilidad | Impacto | Mitigación |
|----|--------|--------------|---------|------------|
| R-01 | Definiciones de KPI ambiguas | [Alta/Media/Baja] | Alto | Diccionario completo |
| R-02 | Datos no disponibles a tiempo | {{PROB}} | {{IMPACTO}} | {{MITIGACION}} |
| R-03 | {{RIESGO}} | {{PROB}} | {{IMPACTO}} | {{MITIGACION}} |

### 15.2 Supuestos [OBL]

| ID | Supuesto | Validado |
|----|----------|----------|
| S-01 | Fuentes de datos disponibles y confiables | Sí/No |
| S-02 | Definiciones de KPI aprobadas por negocio | Sí/No |
| S-03 | {{SUPUESTO}} | Sí/No |

### 15.3 Decisiones pendientes [OBL]

| ID | Tema | Decisión | Responsable | Fecha |
|----|------|----------|-------------|-------|
| D-01 | Definiciones finales de KPIs | {{DECISION}} | Data + Negocio | {{FECHA}} |
| D-02 | Fuente de verdad por métrica | {{DECISION}} | Data | {{FECHA}} |
| D-03 | Periodo default | {{DECISION}} | PM + UX | {{FECHA}} |

---

## 16) Checklist de aprobación [OBL]

> **Activación:** Siempre obligatorio.

### 16.1 Datos [OBL]

- [ ] KPI Dictionary completo (§4)
- [ ] Definiciones aprobadas por negocio
- [ ] Fuentes de verdad identificadas
- [ ] Fórmulas documentadas

### 16.2 UX [OBL]

- [ ] Layout definido
- [ ] Filtros especificados
- [ ] Drill-downs mapeados
- [ ] Estados (loading/empty/error) definidos

### 16.3 Técnica [OBL]

- [ ] Endpoints mapeados
- [ ] Estrategia de cache definida
- [ ] Performance objectives establecidos
- [ ] RBAC configurado

### 16.4 QA [OBL]

- [ ] Casos de prueba documentados
- [ ] Analytics instrumentado
- [ ] Accesibilidad validada

### 16.5 Firmas de aprobación [OBL]

| Rol | Nombre | Fecha | Status |
|-----|--------|-------|--------|
| PM/PO | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| UX/UI | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| Data/BI | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| Tech Lead | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| QA | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |

---

## 17) Particularidades del proyecto [OPC]

> **Activación:** Usar para KPIs custom o configuraciones específicas.

### 17.1 KPIs específicos del proyecto

| KPI ID | Particularidad | Notas |
|--------|----------------|-------|
| {{KPI_ID}} | {{PARTICULARIDAD}} | {{NOTAS}} |

### 17.2 Excepciones al estándar

| Sección | Excepción | Justificación |
|---------|-----------|---------------|
| {{SECCION}} | {{EXCEPCION}} | {{JUSTIFICACION}} |

---

## 📋 ANEXOS RELACIONADOS

> Marcar los anexos que aplican:

- [ ] **DataGrid** → Si hay tablas de drill-down (usar TEMPLATE_BASE_Spec_DataGrid)
- [ ] **UXStates** → Referencia a estándar global
- [ ] **AdminRBAC** → Si hay permisos complejos por métrica

---

## 🔁 GUÍA OPERATIVA PARA AGENTES

### Cómo usar este template:

1. **Copiar** el template
2. **Completar §4 primero** (KPI Dictionary) — es la sección núcleo
3. **Validar definiciones** con stakeholders de negocio
4. **Reemplazar** placeholders `{{...}}`
5. **Omitir** secciones `[COND]` si no aplican
6. **Validar** con checklist (§16)

### Secciones núcleo (mínimo viable):

- §0 Metadatos
- §1 Propósito
- §3 RBAC
- §4 **KPI Dictionary** ← CRÍTICO
- §5 Layout
- §6 Filtros
- §7 Componentes
- §8 Drill-down
- §9 APIs y refresh
- §10 Estados
- §13 Analytics
- §16 Checklist

### Validación cruzada:

- Cada KPI en §4 debe tener card en §7.1
- Cada KPI debe tener definición completa (no ambigua)
- Cada chart en §7.2 debe referenciar KPIs de §4
- Cada drill-down debe tener destino definido
- Cada componente debe tener estados en §10

### Red flags a evitar:

- ❌ Dashboard sin KPI Dictionary
- ❌ KPIs sin fórmula clara
- ❌ Métricas sin owner de definición
- ❌ Múltiples fuentes de verdad para mismo KPI
- ❌ Charts sin alternativa accesible
- ❌ >10 KPIs visibles simultáneamente (cognitive overload)

---

> **Fin del template**  
> **Versión:** 2.0  
> **Última actualización:** {{FECHA_ACTUALIZACION}}
