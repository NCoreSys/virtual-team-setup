# 📚 CATÁLOGO MAESTRO — Templates de Especificación UI/UX

> **Versión:** 2.0  
> **Última actualización:** 2026-03-07  
> **Total de templates:** 14 + 1 Guía

---

## 🎯 Propósito

Este catálogo define los templates disponibles para especificar pantallas, flujos y componentes UI/UX. Cada pantalla debe usar **1 template principal** y puede referenciar templates adicionales como **anexos**.

---

## 📋 Reglas de uso

| Regla | Descripción |
|-------|-------------|
| **1 pantalla = 1 template principal** | Elegir el template que mejor describe la función principal |
| **Anexos para complejidad** | Form, DataGrid, Wizard, Modal se agregan como anexos cuando están embebidos |
| **UXStates es transversal** | Referenciar, no duplicar estados en cada spec |
| **Particularidades al final** | Excepciones en sección dedicada, no modificar estructura base |

---

## 🏷️ Convenciones de ID

| Tipo | Prefijo | Ejemplo |
|------|---------|---------|
| AppScreen | `screen-` | `screen-01-home-dashboard` |
| Landing | `lp-` | `lp-01-homepage` |
| Form | `form-` | `form-01-user-registration` |
| Wizard | `wiz-` | `wiz-01-onboarding` |
| UXStates | `uxstates-` | `uxstates-01-global` |
| DataGrid | `grid-` | `grid-01-users-list` |
| DashboardKPI | `dash-` | `dash-01-analytics` |
| EntityDetail | `detail-` | `detail-01-order-view` |
| AdminRBAC | `admin-` | `admin-01-roles-permissions` |
| ModalOverlay | `overlay-` | `overlay-01-confirm-delete` |
| Checkout | `pay-` | `pay-01-subscription` |
| ContentSEO | `seo-` | `seo-01-blog-article` |
| Notification | `notif-` | `notif-01-system-alerts` |
| SemanticSearch | `search-` | `search-01-kb-semantic` |

---

## 📊 Templates por prioridad

### P1 — Core (MVP)

Templates fundamentales para cualquier aplicación.

| # | Template | Archivo | Uso | Secciones núcleo |
|---|----------|---------|-----|------------------|
| 1 | **AppScreen** | `TEMPLATE_BASE_Spec_AppScreen_v2.md` | Pantalla de aplicación genérica | §5 Component Inventory |
| 2 | **Landing** | `TEMPLATE_BASE_Spec_Landing_v2.md` | Landing pages de conversión | §4 Estructura narrativa, §8 SEO |
| 3 | **Form** | `TEMPLATE_BASE_Spec_Form_v2.md` | Formularios (standalone o anexo) | §5 Field Inventory |
| 4 | **Wizard** | `TEMPLATE_BASE_Spec_Wizard_v2.md` | Flujos multi-paso | §4 Step Map |
| 5 | **UXStates** | `TEMPLATE_BASE_Spec_UXStates_v2.md` | Estados UI transversales | §2 Taxonomía de estados |

### P2 — Enterprise/Scale

Templates para aplicaciones empresariales y funcionalidades avanzadas.

| # | Template | Archivo | Uso | Secciones núcleo |
|---|----------|---------|-----|------------------|
| 6 | **DataGrid** | `TEMPLATE_BASE_Spec_DataGrid_v2.md` | Tablas de datos con acciones | §5 Column Inventory, §6 RBAC Matrix |
| 7 | **DashboardKPI** | `TEMPLATE_BASE_Spec_DashboardKPI_v2.md` | Dashboards analíticos | §4 KPI Dictionary |
| 8 | **EntityDetail** | `TEMPLATE_BASE_Spec_EntityDetail_v2.md` | Vista detalle de entidades | §4.2 State Machine, §7 Section Inventory |
| 9 | **AdminRBAC** | `TEMPLATE_BASE_Spec_AdminRBAC_v2.md` | Administración de roles/permisos | §4 Role Catalog, §5 Permission Catalog, §6 RBAC Matrix |
| 10 | **ModalOverlay** | `TEMPLATE_BASE_Spec_ModalOverlay_v2.md` | Modales, drawers, bottom sheets | §5 Overlay Inventory, §10 A11Y |
| 11 | **Notification** | `TEMPLATE_BASE_Spec_Notification_v2.md` | Sistema de notificaciones | §4 Catálogo de notificaciones, §6 Templates |
| 12 | **SemanticSearch** | `TEMPLATE_BASE_Spec_SemanticSearch_v2.md` | Búsqueda vectorial/IA | §3 Modelo embeddings, §5 Resultados, §7 Performance metrics |

### P3 — Conditional

Templates para casos de uso específicos.

| # | Template | Archivo | Uso | Secciones núcleo |
|---|----------|---------|-----|------------------|
| 13 | **Checkout** | `TEMPLATE_BASE_Spec_Checkout_v2.md` | Flujos de pago/suscripción | §4 Product Catalog, §5 Pricing, §10 Error handling |
| 14 | **ContentSEO** | `TEMPLATE_BASE_Spec_ContentSEO_v2.md` | Páginas de contenido/SEO | §4 Estructura contenido, §6 SEO metadata |

### Guías de referencia

| # | Documento | Archivo | Uso |
|---|-----------|---------|-----|
| 15 | **Design Tokens Checklist** | `GUIA_Design_Tokens_Checklist.md` | Checklist de tokens para Design System |

---

## 🔀 Matriz de selección

### ¿Qué template usar?

```
¿Es una pantalla de aplicación?
├─ ¿Tiene tabla de datos como elemento principal? → DataGrid
├─ ¿Muestra KPIs y gráficos? → DashboardKPI
├─ ¿Muestra detalle de una entidad con estados? → EntityDetail
├─ ¿Es administración de usuarios/roles? → AdminRBAC
├─ ¿Es búsqueda con IA/vectores? → SemanticSearch
└─ ¿Es pantalla genérica? → AppScreen

¿Es un flujo multi-paso?
├─ ¿Es proceso de pago? → Checkout
└─ ¿Es otro flujo? → Wizard

¿Es una landing page de conversión? → Landing

¿Es una página de contenido/blog/docs? → ContentSEO

¿Es un modal, drawer o bottom sheet? → ModalOverlay (usualmente como anexo)

¿Es un formulario standalone? → Form (usualmente como anexo)

¿Es configuración de notificaciones? → Notification
```

### Combinaciones frecuentes

| Pantalla | Template principal | Anexos |
|----------|-------------------|--------|
| Lista de usuarios con modal de edición | DataGrid | ModalOverlay + Form |
| Detalle de orden con acciones | EntityDetail | ModalOverlay |
| Checkout de suscripción | Checkout | Form (billing) |
| Landing con formulario de registro | Landing | Form |
| Dashboard con drill-down | DashboardKPI | ModalOverlay |
| Admin de roles con wizard de creación | AdminRBAC | Wizard + Form |
| Búsqueda IA con detalle de resultado | SemanticSearch | EntityDetail |
| App con sistema de notificaciones | — | Notification (transversal) |

---

## ✅ Marcadores estándar

Todos los templates v2.0 usan estos marcadores:

| Marcador | Significado |
|----------|-------------|
| `[OBL]` | Obligatorio — siempre completar |
| `[OPC]` | Opcional — completar si aplica |
| `[COND]` | Condicional — completar si se cumple condición |
| `{{PLACEHOLDER}}` | Reemplazar con valor específico |
| `[Elegir: A / B / C]` | Seleccionar una opción |

---

## 📁 Estructura de archivos

```
/templates/
├── P1-Core/
│   ├── TEMPLATE_BASE_Spec_AppScreen_v2.md
│   ├── TEMPLATE_BASE_Spec_Landing_v2.md
│   ├── TEMPLATE_BASE_Spec_Form_v2.md
│   ├── TEMPLATE_BASE_Spec_Wizard_v2.md
│   └── TEMPLATE_BASE_Spec_UXStates_v2.md
├── P2-Enterprise/
│   ├── TEMPLATE_BASE_Spec_DataGrid_v2.md
│   ├── TEMPLATE_BASE_Spec_DashboardKPI_v2.md
│   ├── TEMPLATE_BASE_Spec_EntityDetail_v2.md
│   ├── TEMPLATE_BASE_Spec_AdminRBAC_v2.md
│   ├── TEMPLATE_BASE_Spec_ModalOverlay_v2.md
│   ├── TEMPLATE_BASE_Spec_Notification_v2.md
│   └── TEMPLATE_BASE_Spec_SemanticSearch_v2.md
├── P3-Conditional/
│   ├── TEMPLATE_BASE_Spec_Checkout_v2.md
│   └── TEMPLATE_BASE_Spec_ContentSEO_v2.md
└── Guias/
    └── GUIA_Design_Tokens_Checklist.md
```

---

## 🔄 Changelog

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 2.0 | 2026-03-07 | Estandarización completa: marcadores [OBL]/[OPC]/[COND], placeholders, guía operativa para agentes, firmas de aprobación. Agregados: Notification (P2), SemanticSearch (P2), Design Tokens Guide. |
| 1.0 | — | Versión inicial con 12 templates |

---

> **Fin del catálogo**
