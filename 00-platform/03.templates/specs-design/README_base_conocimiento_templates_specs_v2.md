# 📘 README — Base de Conocimiento: Templates de Especificación UI/UX

> **Versión:** 2.0  
> **Última actualización:** 2026-03-07  
> **Propósito:** Guía de uso para agentes IA y equipos de producto

---

## 🎯 ¿Qué es esta base de conocimiento?

Esta base de conocimiento contiene **templates estandarizados** para especificar pantallas, flujos y componentes UI/UX. Está diseñada para ser usada por:

- **Agentes IA** que generan especificaciones automáticamente
- **Product Managers** que documentan requerimientos
- **Diseñadores UX** que especifican interacciones
- **Desarrolladores** que implementan funcionalidades

---

## 📋 Contenido

### Templates de especificación (14 templates)

| Prioridad | Templates | Descripción |
|-----------|-----------|-------------|
| **P1 Core** | AppScreen, Landing, Form, Wizard, UXStates | Fundamentales para cualquier app |
| **P2 Enterprise** | DataGrid, DashboardKPI, EntityDetail, AdminRBAC, ModalOverlay, Notification, SemanticSearch | Funcionalidades empresariales y IA |
| **P3 Conditional** | Checkout, ContentSEO | Casos de uso específicos |

### Documentos de referencia

| Documento | Descripción |
|-----------|-------------|
| **Catálogo Maestro** | Índice de templates con reglas de selección |
| **Guía Design Tokens** | Checklist de tokens para Design System |
| **Este README** | Guía de uso general |
| **Índice** | Navegación rápida a todos los documentos |

---

## 🏷️ Convenciones

### Marcadores de obligatoriedad

Todos los templates usan estos marcadores para indicar qué secciones completar:

| Marcador | Significado | Acción |
|----------|-------------|--------|
| `[OBL]` | **Obligatorio** | Siempre completar |
| `[OPC]` | **Opcional** | Completar si aplica al proyecto |
| `[COND]` | **Condicional** | Completar solo si se cumple la condición indicada |

### Placeholders

| Formato | Significado | Ejemplo |
|---------|-------------|---------|
| `{{NOMBRE}}` | Reemplazar con valor | `{{NOMBRE_PROYECTO}}` → "Mi App" |
| `[Elegir: A / B / C]` | Seleccionar una opción | `[Elegir: Draft / Review / Approved]` |
| `{{NUM}}` | Reemplazar con número | `{{NUM}}` → "5" |
| `{{FECHA}}` | Reemplazar con fecha | `{{FECHA_YYYY-MM-DD}}` → "2026-03-07" |

### IDs técnicos

Cada pantalla/spec debe tener un ID único con el prefijo correspondiente:

| Template | Prefijo | Ejemplo |
|----------|---------|---------|
| AppScreen | `screen-` | `screen-01-home-dashboard` |
| Landing | `lp-` | `lp-01-homepage` |
| Form | `form-` | `form-01-registration` |
| Wizard | `wiz-` | `wiz-01-onboarding` |
| DataGrid | `grid-` | `grid-01-users-list` |
| DashboardKPI | `dash-` | `dash-01-analytics` |
| EntityDetail | `detail-` | `detail-01-order-view` |
| AdminRBAC | `admin-` | `admin-01-roles` |
| ModalOverlay | `overlay-` | `overlay-01-confirm` |
| Checkout | `pay-` | `pay-01-subscribe` |
| ContentSEO | `seo-` | `seo-01-blog` |
| Notification | `notif-` | `notif-01-system` |
| SemanticSearch | `search-` | `search-01-kb` |
| UXStates | `uxstates-` | `uxstates-01-global` |

---

## 🚀 Cómo usar los templates

### Para agentes IA

1. **Identificar el tipo de pantalla** usando la matriz de selección del Catálogo Maestro
2. **Copiar el template correspondiente**
3. **Leer la sección "Guía de uso"** al inicio del template
4. **Completar secciones núcleo** primero (marcadas en cada template)
5. **Reemplazar todos los `{{PLACEHOLDER}}`**
6. **Omitir secciones `[COND]`** si no aplica la condición
7. **Validar con checklist** al final del template
8. **Agregar particularidades** en la sección dedicada si hay excepciones

### Para humanos

1. Consultar el **Catálogo Maestro** para elegir el template correcto
2. Descargar el template desde el índice
3. Completar las secciones obligatorias
4. Revisar con el equipo antes de aprobar
5. Usar el checklist de aprobación al final

---

## 📐 Estructura de cada template

Todos los templates v2.0 siguen esta estructura:

```
# TÍTULO DEL TEMPLATE

## 🔖 GUÍA DE USO
- Marcadores de obligatoriedad
- Cuándo usar / cuándo NO usar

## ESPECIFICACIÓN
- §0 Metadatos [OBL]
- §1 Propósito [OBL]
- §2 Alcance [OBL]
- ... (secciones específicas del template)
- §N-2 Riesgos y decisiones [OBL]
- §N-1 Checklist de aprobación [OBL]
- §N Particularidades [OPC]

## 📋 ANEXOS RELACIONADOS

## 🔁 GUÍA OPERATIVA PARA AGENTES
- Cómo usar este template
- Secciones núcleo (mínimo viable)
- Validación cruzada
- Red flags a evitar
```

---

## ⚠️ Reglas importantes

### 1 pantalla = 1 template principal

Cada pantalla usa UN template principal. Si tiene componentes complejos embebidos (formularios, modales, grids), estos se agregan como **anexos**.

**Ejemplo:** Una pantalla de lista de usuarios con modal de edición:
- Template principal: `DataGrid`
- Anexo 1: `ModalOverlay`
- Anexo 2: `Form`

### UXStates es transversal

No duplicar estados en cada spec. El template `UXStates` define la taxonomía global de estados (loading, empty, error, etc.) y los demás templates lo **referencian**.

### Particularidades al final

Si hay excepciones a la estructura estándar, documentarlas en la sección "Particularidades del proyecto" sin modificar las secciones base.

### Checklist antes de aprobar

Cada template tiene un checklist de aprobación. No marcar como "Approved" hasta completar todos los items y obtener firmas.

---

## 🔗 Anexos comunes por template

| Template principal | Anexos frecuentes |
|-------------------|-------------------|
| AppScreen | Form, ModalOverlay, DataGrid |
| Landing | Form |
| EntityDetail | ModalOverlay, Form |
| DataGrid | ModalOverlay, Form |
| AdminRBAC | Wizard, Form, ModalOverlay |
| Checkout | Form (billing) |
| DashboardKPI | ModalOverlay (drill-down) |
| SemanticSearch | EntityDetail (resultado detalle) |

---

## 📊 Validación cruzada

Al completar un spec, verificar consistencia entre secciones:

| Validación | Descripción |
|------------|-------------|
| **Componentes ↔ Spec** | Cada componente en el inventario debe tener especificación |
| **Roles ↔ Acciones** | Cada acción debe tener permisos definidos |
| **Estados ↔ UI** | Cada estado debe tener diseño de UI |
| **Analytics ↔ Interacciones** | Cada interacción clave debe tener evento |
| **QA ↔ Features** | Cada feature debe tener caso de prueba |

---

## 🚫 Red flags globales

Evitar estos errores comunes:

| Red flag | Problema |
|----------|----------|
| ❌ Sin secciones núcleo | Spec incompleto |
| ❌ Placeholders sin reemplazar | `{{NOMBRE}}` en documento final |
| ❌ Sin checklist de aprobación | No se puede validar completitud |
| ❌ Estados duplicados (no referenciar UXStates) | Inconsistencia entre pantallas |
| ❌ Sin analytics | No se puede medir |
| ❌ Sin casos de QA | No se puede testear |
| ❌ Modificar estructura base | Usar Particularidades en su lugar |

---

## 📁 Estructura de carpetas recomendada

```
/proyecto/
├── specs/
│   ├── screens/
│   │   ├── screen-01-home.md
│   │   ├── screen-02-profile.md
│   │   └── ...
│   ├── flows/
│   │   ├── wiz-01-onboarding.md
│   │   └── pay-01-checkout.md
│   ├── components/
│   │   ├── form-01-login.md
│   │   └── overlay-01-confirm.md
│   └── transversal/
│       ├── uxstates-01-global.md
│       └── notif-01-system.md
├── design/
│   └── design-tokens.md
└── index.md
```

---

## 🔄 Versionamiento

| Versión del template | Cuándo actualizar |
|---------------------|-------------------|
| Mismo template, nueva versión del spec | Incrementar versión del documento (`v1.0` → `v1.1`) |
| Cambios mayores en el spec | Incrementar versión mayor (`v1.x` → `v2.0`) |
| Template base actualizado | Los specs existentes NO se actualizan automáticamente |

---

## 📞 Soporte

Si encuentras gaps en los templates o necesitas un template nuevo:

1. Documentar el caso de uso no cubierto
2. Proponer estructura básica
3. Revisar con el equipo
4. Agregar al catálogo maestro

---

> **Fin del README**  
> **Versión:** 2.0
