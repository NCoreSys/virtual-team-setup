# 📘 TEMPLATE BASE — ESPECIFICACIÓN FUNCIONAL + UI/UX (Reusable)

## 0) Metadatos del documento

**Nombre del documento:** Especificación Funcional + UI/UX  
**Proyecto:** `[Nombre del proyecto]`  
**Módulo / Feature:** `[Nombre del módulo]`  
**Pantalla / Vista:** `[Nombre de pantalla]`  
**ID técnico:** `[ej. nav-01-home-feed]`  
**Versión:** `[v1.0]`  
**Estado:** `[Draft / Review / Approved / Deprecated]`  
**Prioridad:** `[Crítica / Alta / Media / Baja]`  
**Tipo:** `[Mobile / Web / Responsive / Desktop / Tablet]`  
**Fecha:** `[YYYY-MM-DD]`  
**Owner (PM/PO):** `[Nombre]`  
**UX/UI Owner:** `[Nombre]`  
**Tech Lead:** `[Nombre]`  
**QA Owner:** `[Nombre]`

---

## 1) Propósito de la pantalla / módulo

### 1.1 Descripción general
Explica **qué hace** esta pantalla/módulo y por qué existe.

**Template:**
- Esta pantalla/módulo permite a `[tipo de usuario]` realizar `[acción principal]`.
- Su función dentro del sistema es `[rol dentro del flujo general]`.
- Se considera `[MVP / fase 2 / enterprise-only / admin-only]`.

### 1.2 Objetivo de negocio
- `[Objetivo de negocio #1]`
- `[Objetivo de negocio #2]`
- `[Objetivo de negocio #3]`

### 1.3 Objetivo UX
- `[Objetivo UX #1: reducir fricción / discovery / conversión / confianza]`
- `[Objetivo UX #2]`
- `[Objetivo UX #3]`

### 1.4 KPIs / Métricas objetivo
- **CTR esperado:** `[ ]`
- **Tiempo promedio en pantalla:** `[ ]`
- **Tasa de conversión:** `[ ]`
- **Errores UX tolerables:** `[ ]`
- **Retención / retorno:** `[ ]`

---

## 2) Alcance (Scope)

### 2.1 Incluye (In Scope)
- `[Funcionalidad A]`
- `[Funcionalidad B]`
- `[Funcionalidad C]`

### 2.2 No incluye (Out of Scope)
- `[Funcionalidad no incluida #1]`
- `[Integración futura #2]`
- `[Feature opcional #3]`

### 2.3 Dependencias
- `[API / microservicio / auth / permisos / feature flags / data source]`
- `[Módulo previo requerido]`
- `[Componente compartido del design system]`

---

## 3) Usuarios, roles y permisos

### 3.1 Roles involucrados
| Rol | Puede ver | Puede interactuar | Puede editar | Puede aprobar | Restricciones |
|---|---|---|---|---|---|
| `[Rol 1]` | ✅ | ✅ | ✅ | ❌ | `[restricción]` |
| `[Rol 2]` | ✅ | ✅ | ❌ | ❌ | `[restricción]` |
| `[Admin]` | ✅ | ✅ | ✅ | ✅ | `[si aplica]` |

### 3.2 Tipo de usuario objetivo (UX)
- `[Usuario primario]`
- `[Usuario secundario]`
- `[Usuario ocasional]`

### 3.3 Consideraciones por rol
- ¿Cambia la UI por rol?
- ¿Cambia la data visible?
- ¿Cambia la navegación?
- ¿Cambia el copy / CTA?

---

## 4) Contexto dentro del flujo (Journey)

### 4.1 Punto de entrada
¿Desde dónde llega el usuario?

- `[Login]`
- `[Dashboard]`
- `[Notificación]`
- `[Deep link]`
- `[Búsqueda]`
- `[Menu lateral]`

### 4.2 Punto de salida
¿A dónde puede ir desde aquí?

- `[Pantalla destino 1]`
- `[Pantalla destino 2]`
- `[Detalle / checkout / profile / etc.]`

### 4.3 Flujo principal (Happy Path)
Describe el flujo principal paso a paso.

1. Usuario entra desde `[origen]`
2. Visualiza `[contenido clave]`
3. Interactúa con `[componente principal]`
4. Selecciona `[elemento]`
5. Sistema responde con `[resultado]`
6. Usuario continúa a `[siguiente pantalla]`

### 4.4 Flujos alternos / secundarios
- Flujo de búsqueda rápida
- Flujo de filtro
- Flujo sin resultados
- Flujo con error
- Flujo de regreso / cancelación

---

## 5) Inventario de componentes UI (Screen Inventory)

> Esta sección es clave para reutilizar specs en cualquier proyecto.

### 5.1 Lista de componentes de la pantalla
| ID componente | Nombre | Tipo | Reutilizable | Prioridad | Fuente |
|---|---|---|---|---|---|
| `cmp-01` | `[Search Bar]` | Input | Sí | Alta | Design System |
| `cmp-02` | `[Product Card]` | Card | Sí | Crítica | Shared |
| `cmp-03` | `[Bottom Nav]` | Navigation | Sí | Crítica | Shared |
| `cmp-04` | `[Filter Chip]` | Chip | Sí | Media | Nuevo |

### 5.2 Jerarquía visual
- **Primario:** `[CTA / contenido principal]`
- **Secundario:** `[lista / filtros / cards]`
- **Terciario:** `[metadata / labels / hints]`

### 5.3 Componentes obligatorios vs opcionales
- **Obligatorios:** `[ ]`
- **Opcionales:** `[ ]`
- **Condicionales por estado/rol:** `[ ]`

---

## 6) Especificación detallada por componente (Reusable Section)

> Repetir esta subsección por cada componente importante.

## 6.X `[Nombre del componente]`

### a) Identificación
- **ID:** `[cmp-xx]`
- **Nombre técnico:** `[ej. product-card]`
- **Tipo:** `[Card / Input / Button / Modal / Tab / List]`
- **Reutilizable:** `[Sí/No]`
- **Owner:** `[DS / Frontend / Feature team]`

### b) Propósito del componente
¿Para qué sirve dentro de esta pantalla?

### c) Contenido / estructura interna
Lista de elementos que contiene:
- `[Título]`
- `[Subtítulo]`
- `[Imagen/Icono]`
- `[Precio/Badge/Estado]`
- `[CTA]`

### d) Variantes
- `[Default]`
- `[Compact]`
- `[Expanded]`
- `[Mobile]`
- `[Desktop]`
- `[Read-only]`
- `[Admin variant]`

### e) Estados visuales / funcionales
- `default`
- `hover` (si aplica)
- `focus`
- `pressed`
- `disabled`
- `loading`
- `empty`
- `error`
- `selected`
- `active`

### f) Reglas de comportamiento
- ¿Qué pasa al hacer click?
- ¿Qué pasa si no hay data?
- ¿Qué pasa si hay texto largo?
- ¿Qué pasa si falla la imagen?
- ¿Qué pasa si el usuario no tiene permisos?

### g) Especificaciones visuales (UI)
- **Width:** `[ ]`
- **Height:** `[ ]`
- **Padding:** `[ ]`
- **Gap:** `[ ]`
- **Border radius:** `[ ]`
- **Shadow:** `[ ]`
- **Typography:** `[ ]`
- **Color tokens:** `[ ]`

### h) Especificaciones responsive
- **Mobile:** `[comportamiento]`
- **Tablet:** `[comportamiento]`
- **Desktop:** `[comportamiento]`

### i) Accesibilidad (A11Y)
- `aria-label`: `[ ]`
- orden de tabulación: `[ ]`
- soporte teclado: `[ ]`
- target táctil mínimo: `44px` (si aplica)
- contraste: `WCAG AA`
- lector de pantalla: `[texto anunciado]`

### j) Eventos de analytics (si aplica)
- `component_view`
- `component_click`
- `cta_click`
- `error_shown`

Payload ejemplo:
- `screen_id`
- `component_id`
- `user_role`
- `item_id`
- `position`
- `source`

---

## 7) Layout y estructura de pantalla

### 7.1 Estructura general
Define la arquitectura visual de la pantalla:

- **Header / Top bar**
- **Zona de filtros**
- **Contenido principal**
- **Sidebar (si aplica)**
- **Footer / Bottom nav**
- **Overlays (modal, drawer, toast)**

### 7.2 Grid / layout system
- **Tipo de layout:** `[Flex / Grid / Mixto]`
- **Columnas:** `[2 / 4 / 12]`
- **Gap:** `[ ]`
- **Max width:** `[ ]`
- **Container padding:** `[ ]`

### 7.3 Jerarquía de zonas
| Zona | Descripción | Prioridad | Sticky | Scroll |
|---|---|---|---|---|
| Header | `[ ]` | Alta | Sí/No | No |
| Sidebar | `[ ]` | Media | Sí/No | Sí/No |
| Main Content | `[ ]` | Crítica | No | Sí |
| Footer/Nav | `[ ]` | Alta | Sí/No | No |

---

## 8) Navegación y comportamiento

### 8.1 Rutas / navegación real
- **Ruta actual:** `[ej. /dashboard/home]`
- **Ruta técnica interna:** `[si aplica]`
- **Deep links soportados:** `[ ]`
- **Parámetros de URL:** `[ ]`

### 8.2 Acciones de navegación
| Acción | Trigger | Destino | Tipo |
|---|---|---|---|
| Click CTA principal | botón | `/x/y` | Push |
| Click card | tarjeta | `/product/:id` | Push |
| Back | back nav | pantalla anterior | Pop |

### 8.3 Persistencia de estado
- ¿Se recuerda scroll?
- ¿Se recuerdan filtros?
- ¿Se recuerda tab activa?
- ¿Se recupera estado al volver?

---

## 9) Datos y contratos (Data + API Mapping)

### 9.1 Fuentes de datos
- `[API REST / GraphQL / local cache / feature flag / mock data]`

### 9.2 Endpoints relacionados
| Endpoint | Método | Uso en pantalla | Prioridad | Cache |
|---|---|---|---|---|
| `/api/...` | GET | cargar listado | Alta | 5 min |
| `/api/...` | POST | acción usuario | Alta | No |
| `/api/...` | GET | metadata/filtros | Media | 1 h |

### 9.3 Datos requeridos por componente
| Componente | Campo | Tipo | Requerido | Fallback |
|---|---|---|---|---|
| Product Card | `title` | string | Sí | `"Sin título"` |
| Product Card | `imageUrl` | string | No | placeholder |
| Product Card | `price` | number | Sí | ocultar bloque |

### 9.4 Reglas de validación de datos
- Campos obligatorios
- Límites de longitud
- Formato de moneda / fecha
- Sanitización de texto
- Manejo de nulos

### 9.5 Estrategia de cache / refresh
- TTL por endpoint
- invalidación por evento
- fallback local
- skeleton loading
- stale-while-revalidate (si aplica)

---

## 10) Reglas de negocio (Business Rules)

### 10.1 Reglas funcionales
- `[Regla 1]`
- `[Regla 2]`
- `[Regla 3]`

### 10.2 Reglas por rol/permisos
- `[Ej. usuarios guest no pueden ver precios]`
- `[Ej. admin ve controles extra]`

### 10.3 Reglas de prioridad / ordenamiento
- ¿Cómo se ordena el contenido?
- ¿Qué pesa más: recencia, relevancia, personalización, inventario, score?

### 10.4 Reglas de visibilidad condicional
- Mostrar componente solo si `[condición]`
- Ocultar CTA si `[condición]`
- Cambiar copy si `[condición]`

---

## 11) Estados de pantalla (Screen States)

### 11.1 Loading
- Skeletons visibles
- Duración mínima (si aplica)
- Indicadores de progreso
- UI bloqueada / parcial

### 11.2 Empty State
- Mensaje principal
- Explicación breve
- CTA de recuperación
- Ilustración/ícono (si aplica)

### 11.3 Error State
- Error de red
- Error servidor
- Error permisos
- Error de datos incompletos
- CTA: reintentar / soporte / volver

### 11.4 Success / Feedback
- Toast
- Banner
- Inline confirmation
- Estado persistente

---

## 12) Accesibilidad (A11Y) — sección obligatoria

### 12.1 Requisitos mínimos
- WCAG 2.1 AA
- Contraste mínimo 4.5:1 (texto normal)
- Focus visible
- Soporte teclado
- Labels descriptivos

### 12.2 Navegación por teclado
- Orden de tab
- traps en modales
- enter/space en botones
- escape en overlays
- shortcuts (si aplica)

### 12.3 Lectores de pantalla
- nombres accesibles
- descripción de iconos
- anuncios de errores/success
- textos alternativos de imágenes

### 12.4 Touch targets (mobile/tablet)
- mínimo `44x44px`

---

## 13) Responsive / Adaptabilidad

### 13.1 Breakpoints oficiales del proyecto
- **Mobile:** `[320–767]`
- **Tablet:** `[768–1023]`
- **Desktop:** `[1024–1439]`
- **Large Desktop:** `[1440+]`

### 13.2 Cambios por breakpoint
| Elemento | Mobile | Tablet | Desktop |
|---|---|---|---|
| Grid principal | 1–2 cols | 2–3 cols | 4+ cols |
| Sidebar | oculto/drawer | opcional | visible |
| CTA labels | compactos | normal | completo |

### 13.3 Comportamiento responsive especial
- reflow de cards
- truncado de texto
- sticky nav
- collapses / accordions
- drawer vs sidebar

---

## 14) Design System / Tokens (si aplica)

### 14.1 Colores (tokens)
- `--color-primary`
- `--color-secondary`
- `--color-bg`
- `--color-surface`
- `--color-text`
- `--color-border`
- `--color-success`
- `--color-warning`
- `--color-error`

### 14.2 Tipografía
- familia
- escala tipográfica
- pesos
- line-height
- reglas de truncado

### 14.3 Espaciado
- scale (`4,8,12,16,24,32...`)
- padding estándar
- gaps estándar

### 14.4 Radio / sombras / motion
- radius scale
- shadow levels
- durations
- easing

---

## 15) Copy UX / Contenido

### 15.1 Tono y estilo
- `[Profesional / cercano / experto / enterprise / playful]`

### 15.2 Textos clave
| Elemento | Copy actual | Variante A | Variante B | Notas |
|---|---|---|---|---|
| Título pantalla | `[ ]` | `[ ]` | `[ ]` | |
| CTA principal | `[ ]` | `[ ]` | `[ ]` | |
| Empty state | `[ ]` | `[ ]` | `[ ]` | |

### 15.3 Reglas de microcopy
- evitar ambigüedad
- usar verbos de acción
- mensajes de error accionables
- consistencia terminológica

---

## 16) Analytics / Instrumentación (obligatorio para producto)

### 16.1 Eventos de pantalla
- `screen_view`
- `screen_loaded`
- `screen_error`

### 16.2 Eventos de interacción
| Evento | Trigger | Payload mínimo |
|---|---|---|
| `search_started` | foco/click en buscador | `screen_id, source` |
| `item_clicked` | click card | `item_id, position, screen_id` |
| `filter_applied` | aplicar filtro | `filter_type, value` |

### 16.3 Métricas derivadas
- CTR por bloque
- tiempo hasta primera acción
- abandono por error
- conversión por entry point

---

## 17) Performance / Calidad técnica

### 17.1 Objetivos de performance
- Tiempo de carga inicial
- LCP (web)
- TTI / INP (web)
- FPS (animaciones)
- peso máximo de assets

### 17.2 Estrategias
- lazy loading
- code splitting
- caching
- placeholders/skeletons
- compresión de imágenes

### 17.3 Riesgos técnicos
- dependencia API lenta
- imágenes pesadas
- listas extensas
- rendering cost en móviles de gama baja

---

## 18) QA / Casos de prueba (base reusable)

### 18.1 Casos funcionales
- carga correcta de datos
- navegación a destinos correctos
- acciones por rol
- validaciones de negocio

### 18.2 Casos visuales
- alignment
- spacing
- truncado
- responsive
- estados hover/focus/disabled

### 18.3 Casos de error
- sin red
- API 500
- timeout
- payload incompleto
- permisos insuficientes

### 18.4 Casos de accesibilidad
- tab order
- focus visible
- lector de pantalla
- contraste
- touch targets

---

## 19) Riesgos, supuestos y decisiones abiertas

### 19.1 Riesgos
- `[riesgo 1]`
- `[riesgo 2]`

### 19.2 Supuestos
- `[supuesto 1]`
- `[supuesto 2]`

### 19.3 Decisiones pendientes
| Tema | Decisión pendiente | Responsable | Fecha |
|---|---|---|---|
| `[ej. ordenamiento]` | definir algoritmo | PM + Data | `[ ]` |
| `[ej. permisos]` | validar matriz final | Security/Backend | `[ ]` |

---

## 20) Checklist de aprobación (Go / No-Go)

### 20.1 Producto / UX
- [ ] Objetivo de pantalla claro
- [ ] Flujos documentados
- [ ] Componentes inventariados
- [ ] Copy base validado

### 20.2 Técnica
- [ ] APIs mapeadas
- [ ] Contratos definidos
- [ ] Reglas de negocio confirmadas
- [ ] Riesgos identificados

### 20.3 Calidad
- [ ] Estados (loading/empty/error) definidos
- [ ] Responsive definido
- [ ] Accesibilidad mínima definida
- [ ] Analytics definido

### 20.4 Aprobación final
- **PM/PO:** `[ ]`
- **UX/UI:** `[ ]`
- **Tech Lead:** `[ ]`
- **QA:** `[ ]`

---

## 🔁 Cómo reutilizar este documento (regla operativa)

Usa este template como **esqueleto fijo** y solo cambia:
1. Metadatos
2. Objetivo del módulo/pantalla
3. Inventario de componentes
4. Reglas de negocio
5. APIs / data mapping
6. Eventos de analytics
7. Riesgos y decisiones pendientes

👉 El resto queda como estándar corporativo.

---

## ✅ Versión mínima (MVP rápido)

- 0) Metadatos
- 1) Propósito
- 2) Scope
- 4) Flujo
- 5) Inventario de componentes
- 6) Specs por componente (solo críticos)
- 8) Navegación
- 9) APIs / Datos
- 10) Reglas de negocio
- 11) Estados
- 12) Accesibilidad
- 16) Analytics
- 20) Checklist

