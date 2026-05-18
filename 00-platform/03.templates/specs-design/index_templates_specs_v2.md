# 📑 ÍNDICE — Templates de Especificación UI/UX v2.0

> **Última actualización:** 2026-03-07  
> **Total documentos:** 17

---

## 📘 Documentos de referencia

| Documento | Descripción | Link |
|-----------|-------------|------|
| 📚 **Catálogo Maestro** | Índice de templates, reglas de selección, matriz de decisión | [catalogo_maestro_templates_specs_uiux_v2.md](./catalogo_maestro_templates_specs_uiux_v2.md) |
| 📘 **README** | Guía de uso, convenciones, estructura | [README_base_conocimiento_templates_specs_v2.md](./README_base_conocimiento_templates_specs_v2.md) |
| 🎨 **Guía Design Tokens** | Checklist de tokens para Design System | [GUIA_Design_Tokens_Checklist.md](./GUIA_Design_Tokens_Checklist.md) |

---

## 🟢 P1 — Core (MVP)

Templates fundamentales para cualquier aplicación.

| # | Template | Descripción | Sección núcleo | Link |
|---|----------|-------------|----------------|------|
| 1 | 📱 **AppScreen** | Pantalla de aplicación genérica | §5 Component Inventory | [TEMPLATE_BASE_Spec_AppScreen_v2.md](./P1-Core/TEMPLATE_BASE_Spec_AppScreen_v2.md) |
| 2 | 🚀 **Landing** | Landing pages de conversión | §4 Estructura narrativa | [TEMPLATE_BASE_Spec_Landing_v2.md](./P1-Core/TEMPLATE_BASE_Spec_Landing_v2.md) |
| 3 | 📝 **Form** | Formularios (standalone o anexo) | §5 Field Inventory | [TEMPLATE_BASE_Spec_Form_v2.md](./P1-Core/TEMPLATE_BASE_Spec_Form_v2.md) |
| 4 | 🧙 **Wizard** | Flujos multi-paso | §4 Step Map | [TEMPLATE_BASE_Spec_Wizard_v2.md](./P1-Core/TEMPLATE_BASE_Spec_Wizard_v2.md) |
| 5 | 🔄 **UXStates** | Estados UI transversales | §2 Taxonomía de estados | [TEMPLATE_BASE_Spec_UXStates_v2.md](./P1-Core/TEMPLATE_BASE_Spec_UXStates_v2.md) |

---

## 🔵 P2 — Enterprise/Scale

Templates para aplicaciones empresariales y funcionalidades avanzadas.

| # | Template | Descripción | Sección núcleo | Link |
|---|----------|-------------|----------------|------|
| 6 | 📊 **DataGrid** | Tablas de datos con acciones | §5 Column Inventory | [TEMPLATE_BASE_Spec_DataGrid_v2.md](./P2-Enterprise/TEMPLATE_BASE_Spec_DataGrid_v2.md) |
| 7 | 📈 **DashboardKPI** | Dashboards analíticos | §4 KPI Dictionary | [TEMPLATE_BASE_Spec_DashboardKPI_v2.md](./P2-Enterprise/TEMPLATE_BASE_Spec_DashboardKPI_v2.md) |
| 8 | 📄 **EntityDetail** | Vista detalle de entidades | §4.2 State Machine | [TEMPLATE_BASE_Spec_EntityDetail_v2.md](./P2-Enterprise/TEMPLATE_BASE_Spec_EntityDetail_v2.md) |
| 9 | 🔐 **AdminRBAC** | Administración de roles/permisos | §4-6 Role/Permission/Matrix | [TEMPLATE_BASE_Spec_AdminRBAC_v2.md](./P2-Enterprise/TEMPLATE_BASE_Spec_AdminRBAC_v2.md) |
| 10 | 🪟 **ModalOverlay** | Modales, drawers, bottom sheets | §5 Overlay Inventory | [TEMPLATE_BASE_Spec_ModalOverlay_v2.md](./P2-Enterprise/TEMPLATE_BASE_Spec_ModalOverlay_v2.md) |
| 11 | 🔔 **Notification** | Sistema de notificaciones | §4 Catálogo de notificaciones | [TEMPLATE_BASE_Spec_Notification_v2.md](./P2-Enterprise/TEMPLATE_BASE_Spec_Notification_v2.md) |
| 12 | 🔍 **SemanticSearch** | Búsqueda vectorial/IA | §3 Modelo embeddings | [TEMPLATE_BASE_Spec_SemanticSearch_v2.md](./P2-Enterprise/TEMPLATE_BASE_Spec_SemanticSearch_v2.md) |

---

## 🟡 P3 — Conditional

Templates para casos de uso específicos.

| # | Template | Descripción | Sección núcleo | Link |
|---|----------|-------------|----------------|------|
| 13 | 💳 **Checkout** | Flujos de pago/suscripción | §4 Product Catalog, §5 Pricing | [TEMPLATE_BASE_Spec_Checkout_v2.md](./P3-Conditional/TEMPLATE_BASE_Spec_Checkout_v2.md) |
| 14 | 📰 **ContentSEO** | Páginas de contenido/SEO | §4 Estructura, §6 SEO | [TEMPLATE_BASE_Spec_ContentSEO_v2.md](./P3-Conditional/TEMPLATE_BASE_Spec_ContentSEO_v2.md) |

---

## 🗂️ Estructura de carpetas

```
templates/
├── index.md                           ← Este archivo
├── catalogo_maestro_v2.md
├── README_v2.md
├── GUIA_Design_Tokens_Checklist.md
│
├── P1-Core/
│   ├── TEMPLATE_BASE_Spec_AppScreen_v2.md
│   ├── TEMPLATE_BASE_Spec_Landing_v2.md
│   ├── TEMPLATE_BASE_Spec_Form_v2.md
│   ├── TEMPLATE_BASE_Spec_Wizard_v2.md
│   └── TEMPLATE_BASE_Spec_UXStates_v2.md
│
├── P2-Enterprise/
│   ├── TEMPLATE_BASE_Spec_DataGrid_v2.md
│   ├── TEMPLATE_BASE_Spec_DashboardKPI_v2.md
│   ├── TEMPLATE_BASE_Spec_EntityDetail_v2.md
│   ├── TEMPLATE_BASE_Spec_AdminRBAC_v2.md
│   ├── TEMPLATE_BASE_Spec_ModalOverlay_v2.md
│   ├── TEMPLATE_BASE_Spec_Notification_v2.md
│   └── TEMPLATE_BASE_Spec_SemanticSearch_v2.md
│
└── P3-Conditional/
    ├── TEMPLATE_BASE_Spec_Checkout_v2.md
    └── TEMPLATE_BASE_Spec_ContentSEO_v2.md
```

---

## ⚡ Selección rápida

### Por tipo de pantalla

| Necesito especificar... | Usar template |
|-------------------------|---------------|
| Pantalla genérica de app | AppScreen |
| Landing page de conversión | Landing |
| Formulario | Form |
| Flujo de varios pasos | Wizard |
| Lista/tabla de datos | DataGrid |
| Dashboard con métricas | DashboardKPI |
| Detalle de una entidad | EntityDetail |
| Admin de usuarios/roles | AdminRBAC |
| Modal o drawer | ModalOverlay |
| Checkout/pagos | Checkout |
| Blog/docs/contenido | ContentSEO |
| Sistema de notificaciones | Notification |
| Búsqueda con IA | SemanticSearch |
| Estados de UI globales | UXStates |

### Por funcionalidad IA

| Funcionalidad IA | Template |
|------------------|----------|
| Búsqueda semántica/vectorial | **SemanticSearch** |
| Recomendaciones | AppScreen + sección IA |
| Chatbot/Asistente | AppScreen + sección IA |
| Análisis predictivo | DashboardKPI |

---

## 📊 Resumen de cobertura

| Categoría | Templates | Cobertura |
|-----------|-----------|-----------|
| Pantallas de app | AppScreen, DataGrid, DashboardKPI, EntityDetail, AdminRBAC | ✅ Completa |
| Flujos | Wizard, Checkout | ✅ Completa |
| Componentes | Form, ModalOverlay | ✅ Completa |
| Marketing/Content | Landing, ContentSEO | ✅ Completa |
| Transversales | UXStates, Notification | ✅ Completa |
| IA/ML | SemanticSearch | ✅ Completa |
| Design System | Design Tokens Guide | ✅ Completa |

---

## 🔄 Changelog del índice

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 2.0 | 2026-03-07 | 14 templates v2.0 + 1 guía. Nuevos: Notification, SemanticSearch, Design Tokens. |
| 1.0 | — | 12 templates originales |

---

> **Fin del índice**
