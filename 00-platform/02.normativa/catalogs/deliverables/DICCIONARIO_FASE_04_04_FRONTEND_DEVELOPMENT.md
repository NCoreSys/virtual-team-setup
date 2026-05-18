# DICCIONARIO DE DELIVERABLES — FASE 4.4: FRONTEND DEVELOPMENT

**Versión:** 1.0  
**Fecha:** 2026-05-14  
**Fase:** 4 — Development  
**Subfase:** 4.4 — Frontend Development  
**Total deliverables:** 15  
**Responsable de subfase:** Frontend Developer  
**Aprueba:** Tech Lead

---

## Contexto de la subfase

Frontend Development implementa la interfaz de usuario: los componentes React, páginas, layouts, hooks, state management, y estilos que el usuario ve e interactúa. Traduce los mockups de Figma (3A.5) en código funcional pixel-perfect, consumiendo la API del backend (4.3) y aplicando el Design System (3A.7). Es la capa visible del producto.

**Prerequisitos de subfase:**
- Design Handoff (3A.9) — mockups, specs, assets, y CSS variables
- API Endpoints (4.3.1) — backend implementado (o al menos contrato OpenAPI)
- Environment Setup (4.1) — ambiente listo

**Entrega de subfase:**
- Frontend completo: componentes, páginas, routing, state, estilos, tests, accesibilidad, y responsive

---

### 4.4.1 Components

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.4 Frontend Development |
| **Responsable** | Frontend Developer |
| **Ejecuta** | Frontend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | TSX (React) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 5-10 días (continuo) |
| **Frecuencia** | Por sprint |

**Perfil de ejecución:** Requiere dominio de React (functional components, hooks, composition), TypeScript, y Figma-to-code translation.  
En VTT: un agente puede generar componentes React desde mockups y design system specs: estructura JSX, props interface, estados, y estilos base. Componentes con lógica interactiva compleja requieren developer. Necesita brief con: mockup del componente, props esperadas, estados, y design tokens.

**Qué es:** Componentes React reutilizables que implementan el Component Library de Figma (3A.7.6): Button, Input, Select, Card, Modal, Table, Toast, etc. Cada componente tiene: props tipadas (TypeScript interface), todos los estados (hover, active, disabled, error, loading), responsive behavior, y accesibilidad (ARIA). Se organizan por categoría (primitives, forms, feedback, layout, navigation).

**Para qué sirve:** Los componentes son los building blocks del frontend — las páginas se construyen ensamblándolos. Un componente bien hecho se implementa una vez y se usa 50 veces. Garantiza consistencia visual (todos los botones son iguales) y reduce tiempo de desarrollo de features nuevas.

**Inputs requeridos:**
- `3A.7.6` Component Library — referencia visual (Figma)
- `3A.7.7` Component Documentation — specs de cada componente
- `3A.9.2` Specs Export — medidas exactas
- `3A.9.4` CSS Variables — tokens como CSS vars
- `3A.5.5` Component States — estados visuales

**Dependencias (predecessors):**
- `3A.7.6` Component Library *(obligatorio)* — referencia visual
- `3A.9.4` CSS Variables *(obligatorio)* — design tokens
- `3A.9.2` Specs Export *(obligatorio)* — specs exactas

**Habilita (successors):**
- `4.4.2` Pages — pages usan componentes
- `4.4.11` Component Tests — tests de componentes
- `4.4.12` Storybook — stories de componentes

**Audiencia:**
- **Frontend Developer** — usa y extiende componentes
- **UI Designer** — valida implementación vs Figma
- **QA Engineer** — verifica visual y funcional

**Secciones esperadas:**
1. Componentes primitivos (Button, Input, Select, Checkbox, Radio, Toggle, Badge, Avatar)
2. Componentes de formulario (Form, FormField, DatePicker, FileUpload)
3. Componentes de feedback (Toast, Alert, Modal, Dialog, Tooltip, Popover)
4. Componentes de datos (Table, List, Card, Pagination, EmptyState)
5. Componentes de navegación (Navbar, Sidebar, Tabs, Breadcrumbs, Menu)
6. Componentes de layout (Container, Grid, Stack, Divider)
7. Props interfaces (TypeScript) por componente
8. Variants (size, variant, state) por componente

**Criterio de completitud:**
- [ ] Todos los componentes del Component Library de Figma implementados
- [ ] Props tipadas con TypeScript interface
- [ ] Todos los estados implementados (hover, active, disabled, error, loading)
- [ ] CSS variables consumidas (no colores hardcoded)
- [ ] Accesibilidad: ARIA labels, keyboard navigation, focus visible
- [ ] Responsive behavior implementado
- [ ] Cada componente tiene al menos 1 test
- [ ] Visual match con Figma (pixel-perfect en componentes críticos)

**Anti-patrones:**
- ❌ **Componentes sin props interface:** `props: any` — pierde type safety y autocompletado.
- ❌ **Estilos hardcoded:** `color: #3B82F6` en vez de `var(--color-primary-500)` — no respeta design system.
- ❌ **Sin estados:** Botón sin hover, input sin error state — interfaz "muerta".
- ❌ **Componentes no-composables:** Modal que hardcodea su contenido — no reutilizable.
- ❌ **Sin accesibilidad:** Button sin role, input sin label, modal sin focus trap — inutilizable para usuarios de screen reader.

**Template:** `phases/04-development/deliverables/components/` *(pendiente)*

---

### 4.4.2 Pages

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.4 Frontend Development |
| **Responsable** | Frontend Developer |
| **Ejecuta** | Frontend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | TSX (React) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 5-10 días (continuo) |
| **Frecuencia** | Por sprint |

**Perfil de ejecución:** Requiere ensamblar componentes en páginas completas, conectar con API, y manejar estados de página (loading, error, empty).  
En VTT: un agente puede generar scaffolding de páginas: layout, data fetching, estados, y componentes ensamblados. Lógica de interacción compleja requiere developer.

**Qué es:** Páginas/vistas completas del producto que ensamblan componentes en layouts funcionales: Dashboard, UserList, OrderDetail, Settings, Profile, etc. Cada page: conecta con la API (data fetching), maneja estados (loading, error, empty, data), y renderiza componentes con datos reales.

**Para qué sirve:** Los componentes son ladrillos; las pages son habitaciones. Una page orquesta: fetch data → show loading → render components with data → handle errors. Es donde el producto cobra vida con datos reales.

**Inputs requeridos:**
- `3A.5.1` UI Mockups Complete — referencia visual de cada página
- `4.4.1` Components — componentes a ensamblar
- `4.4.6` API Client — conexión con backend
- `4.4.5` State Management — estado de la app
- `3A.9.1` Handoff Document — comportamiento por página

**Dependencias (predecessors):**
- `4.4.1` Components *(obligatorio)* — building blocks
- `4.4.6` API Client *(obligatorio)* — data fetching
- `4.4.3` Layouts *(obligatorio)* — layout wrapper

**Habilita (successors):**
- `4.4.10` Unit Tests FE — tests de pages
- `5.4.1` E2E Tests — tests end-to-end por page/flow
- Producto funcional visible

**Audiencia:**
- **Frontend Developer** — implementación
- **UI Designer** — validación visual
- **QA Engineer** — testing funcional
- **Product Owner** — validación de funcionalidad

**Secciones esperadas:**
1. Page por ruta del sitemap (src/pages/ o src/app/)
2. Data fetching (React Query, SWR, o server components)
3. Loading states por page
4. Error states por page
5. Empty states por page
6. Page-level state management
7. SEO metadata (title, description) si aplica

**Criterio de completitud:**
- [ ] Todas las pantallas del sitemap implementadas
- [ ] Data fetching funcional (conecta con API real)
- [ ] Loading, error, y empty states implementados
- [ ] Responsive en desktop y mobile
- [ ] Match visual con mockups
- [ ] Navigation entre pages funcional

**Anti-patrones:**
- ❌ **Fat pages:** Toda la lógica en la page — extraer a hooks y components.
- ❌ **Sin loading state:** Page en blanco mientras carga — parece rota.
- ❌ **Sin error handling:** API falla → pantalla blanca — debe mostrar error state.
- ❌ **Data fetching en useEffect manual:** Sin cache, sin retry, sin dedup — usar React Query/SWR.

**Template:** `phases/04-development/deliverables/pages/` *(pendiente)*

---

### 4.4.3 Layouts

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.4 Frontend Development |
| **Responsable** | Frontend Developer |
| **Ejecuta** | Frontend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | TSX |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere implementar layouts responsive con navegación, sidebar, y content area.  
En VTT: un agente puede generar layouts desde los wireframes y navigation structure. Es bastante delegable.

**Qué es:** Componentes de layout reutilizables que definen la estructura macro de las páginas: MainLayout (navbar + sidebar + content area), AuthLayout (centrado para login/register), DashboardLayout (sidebar collapsible + header + content), y FullWidthLayout (sin sidebar). Cada layout incluye navegación, responsive behavior, y slots para content.

**Para qué sirve:** Los layouts evitan repetir navbar + sidebar en cada page. Una page solo define su contenido; el layout provee la estructura envolvente. Cambiar la navegación se hace en un solo lugar (el layout), no en 30 pages.

**Inputs requeridos:**
- `3A.3.2` Navigation Structure — navegación del layout
- `3A.3.3` Navigation Patterns — patterns de nav (sidebar, topbar)
- `3A.4.9` Responsive Breakpoints — responsive del layout
- `3A.9.5` Redlines — medidas del layout

**Dependencias (predecessors):**
- `3A.3.2` Navigation Structure *(obligatorio)*
- `4.4.1` Components *(obligatorio)* — Navbar, Sidebar como componentes

**Habilita (successors):**
- `4.4.2` Pages — pages usan layouts
- `4.4.15` Responsive Implementation — layouts responsive

**Audiencia:**
- **Frontend Developer** — estructura base de cada page

**Secciones esperadas:**
1. MainLayout (authenticated pages)
2. AuthLayout (login, register, forgot password)
3. Variantes de layout (con/sin sidebar, full-width)
4. Responsive behavior (sidebar collapse, hamburger menu)
5. Slot/children pattern para content area

**Criterio de completitud:**
- [ ] Layout para pages autenticadas (con nav)
- [ ] Layout para pages de auth (sin nav, centrado)
- [ ] Sidebar collapsible en mobile
- [ ] Responsive funcional en todos los breakpoints
- [ ] Navigation funcional (routing)

**Anti-patrones:**
- ❌ **Navbar duplicado en cada page:** Copy-paste de nav en 30 pages — mantenimiento imposible.
- ❌ **Layout no responsive:** Sidebar fijo en mobile — content area de 100px.
- ❌ **Layout sin slots:** Layout que hardcodea content — no reutilizable.

**Template:** `phases/04-development/deliverables/layouts/` *(pendiente)*

---

### 4.4.4 Hooks

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.4 Frontend Development |
| **Responsable** | Frontend Developer |
| **Ejecuta** | Frontend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | TypeScript |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Continuo |
| **Frecuencia** | Por feature |

**Perfil de ejecución:** Requiere dominio de React hooks patterns: custom hooks, composition, y separation of concerns.  
En VTT: un agente puede generar custom hooks comunes (useDebounce, useLocalStorage, usePagination, useAuth). Es bastante delegable.

**Qué es:** Custom React hooks que encapsulan lógica reutilizable: data fetching hooks (useUsers, useOrders), UI hooks (useDebounce, useMediaQuery, useClickOutside), auth hooks (useAuth, usePermissions), form hooks (useForm), y business logic hooks. Cada hook es testeable, tipado, y documentado.

**Para qué sirve:** Los hooks extraen lógica de los componentes para reutilización. En lugar de que 5 componentes implementen debounce, hay un `useDebounce()` que todos usan. Los hooks son el mecanismo de React para separar lógica de UI.

**Inputs requeridos:**
- `4.4.6` API Client — hooks de data fetching wrappean el client
- `4.4.5` State Management — hooks acceden al store
- Necesidades recurrentes durante desarrollo

**Dependencias (predecessors):**
- `4.4.6` API Client *(recomendado)* — para data fetching hooks
- `4.4.5` State Management *(recomendado)* — para state hooks

**Habilita (successors):**
- `4.4.2` Pages — pages usan hooks
- `4.4.1` Components — components usan hooks
- `4.4.10` Unit Tests FE — tests de hooks

**Audiencia:**
- **Frontend Developer** — uso diario

**Secciones esperadas:**
1. Data hooks (useUsers, useCreateUser, useUpdateOrder) — wrapping React Query
2. Auth hooks (useAuth, useCurrentUser, usePermissions, useRequireAuth)
3. UI hooks (useDebounce, useMediaQuery, useClickOutside, useLocalStorage)
4. Form hooks (useForm wrapping react-hook-form, o custom)
5. Business hooks (useCart, useNotifications, useSearch)

**Criterio de completitud:**
- [ ] Hooks de data fetching para cada entidad principal
- [ ] Hook de auth funcional (useAuth, useCurrentUser)
- [ ] UI hooks comunes implementados (debounce, media query)
- [ ] Cada hook tipado con TypeScript (input types, return types)
- [ ] Cada hook tiene unit test
- [ ] Documentados con JSDoc

**Anti-patrones:**
- ❌ **Lógica en componentes:** useEffect + fetch + setState en cada componente — extraer a custom hook.
- ❌ **Hooks sin types:** `useAuth()` retorna `any` — pierde type safety.
- ❌ **Hooks con side effects ocultos:** Hook que muta global state sin que el nombre lo indique.
- ❌ **Over-abstraction:** Custom hook para cada useState — no todo justifica un hook.

**Template:** `phases/04-development/deliverables/hooks/` *(pendiente)*

---

### 4.4.5 State Management

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.4 Frontend Development |
| **Responsable** | Frontend Developer |
| **Ejecuta** | Frontend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | TypeScript |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Una vez + evolución |

**Perfil de ejecución:** Requiere diseño de state architecture: qué es server state (React Query) vs client state (Zustand/Redux), y cómo estructurar stores.  
En VTT: un agente puede generar store configuration y slices/atoms. Es bastante delegable.

**Qué es:** Configuración y estructura del state management del frontend: client state store (Zustand, Redux Toolkit, Jotai) para UI state (sidebar open, modal visible, theme preference), y server state management (React Query, SWR) para API data (cache, refetch, optimistic updates). Incluye la estructura de stores/slices.

**Para qué sirve:** Sin state management, el state se pasa por props a través de 8 niveles de componentes (prop drilling) o se duplica en múltiples lugares. Un store centralizado permite que cualquier componente acceda al state que necesita sin drilling.

**Inputs requeridos:**
- `3B.1.5` Technology Stack — library elegida (Zustand, Redux, Jotai)
- Necesidades de state del producto (qué state es global vs local)

**Dependencias (predecessors):**
- `3B.1.5` Technology Stack *(obligatorio)* — library elegida

**Habilita (successors):**
- `4.4.2` Pages — pages acceden al store
- `4.4.4` Hooks — hooks wrappean store access
- `4.4.10` Unit Tests FE — tests de store

**Audiencia:**
- **Frontend Developer** — configuración y uso

**Secciones esperadas:**
1. Store configuration (Zustand create, Redux configureStore)
2. Slices/atoms por dominio (authSlice, uiSlice, notificationsSlice)
3. Server state (React Query client configuration, cache policies)
4. Selectors/derived state
5. Actions/mutations

**Criterio de completitud:**
- [ ] Client state store configurado
- [ ] Server state (React Query/SWR) configurado con cache policies
- [ ] Slices para auth, UI, y business state
- [ ] TypeScript types para todo el state
- [ ] DevTools configurados (React Query Devtools, Redux Devtools)
- [ ] Tests de store

**Anti-patrones:**
- ❌ **Todo en global state:** El color de un input en global store — solo state compartido es global.
- ❌ **Server state en client store:** Guardar API responses en Redux — React Query lo maneja mejor (cache, refetch, dedup).
- ❌ **Prop drilling como alternativa:** Pasar state por 8 niveles de props — store o context lo resuelve.
- ❌ **Store sin types:** `state: any` — pierde autocompletado y detección de errores.

**Template:** `phases/04-development/deliverables/state-management/` *(pendiente)*

---

### 4.4.6 API Client

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.4 Frontend Development |
| **Responsable** | Frontend Developer |
| **Ejecuta** | Frontend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | TypeScript |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez + por endpoint |

**Perfil de ejecución:** Requiere configurar HTTP client (Axios/fetch) con interceptors, auth, y error handling.  
En VTT: un agente puede generar API client completo con types desde el OpenAPI spec. Es altamente delegable.

**Qué es:** Módulo que encapsula todas las llamadas HTTP al backend: instancia de Axios/fetch configurada con base URL, auth interceptor (attach JWT), error interceptor (handle 401 → refresh token, handle network errors), request/response types (generados desde OpenAPI), y funciones por endpoint (`api.users.getById(id)`, `api.orders.create(data)`).

**Para qué sirve:** Centraliza la comunicación con el backend. En lugar de que cada componente haga `fetch('/api/users')` con su propia configuración, hay un client que maneja auth, errors, retries, y tipos automáticamente. Cambiar la base URL o agregar un header se hace en un solo lugar.

**Inputs requeridos:**
- `3B.4.1` OpenAPI Spec — types auto-generados
- `3B.4.6` Authentication Spec — auth token handling
- `4.3.1` API Endpoints — endpoints a consumir

**Dependencias (predecessors):**
- `3B.4.1` OpenAPI Spec *(obligatorio)* — types
- `3B.4.6` Authentication Spec *(obligatorio)* — auth handling

**Habilita (successors):**
- `4.4.4` Hooks — data fetching hooks wrappean API client
- `4.4.2` Pages — pages consumen API vía hooks/client

**Audiencia:**
- **Frontend Developer** — interfaz con el backend

**Secciones esperadas:**
1. HTTP client instance (Axios/fetch con config base)
2. Auth interceptor (attach Bearer token, handle 401 → refresh)
3. Error interceptor (transform errors to AppError, handle network errors)
4. Request/Response types (generados o manuales, tipados)
5. API functions por resource (`api.users.*`, `api.orders.*`)
6. Configuration (base URL from env, timeout, retries)

**Criterio de completitud:**
- [ ] HTTP client configurado con base URL, timeout
- [ ] Auth interceptor funcional (attach token, refresh on 401)
- [ ] Error handling estándar (network, timeout, API errors)
- [ ] Types para request/response de cada endpoint
- [ ] Funciones de API por resource
- [ ] Configurable por environment (dev/staging/prod URL)

**Anti-patrones:**
- ❌ **fetch() raw en cada componente:** Sin config compartida, sin auth, sin error handling — duplicación masiva.
- ❌ **Sin interceptor de auth:** Cada call agrega `Authorization: Bearer` manualmente — se olvida y falla.
- ❌ **Sin types:** `response.data` es `any` — pierde toda la type safety del frontend.
- ❌ **Sin error handling:** Network error → unhandled promise rejection → crash silencioso.

**Template:** `phases/04-development/deliverables/api-client/` *(pendiente)*

---

### 4.4.7 Types/Interfaces

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.4 Frontend Development |
| **Responsable** | Frontend Developer |
| **Ejecuta** | Frontend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | TypeScript |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día + continuo |
| **Frecuencia** | Continua |

**Perfil de ejecución:** Requiere TypeScript avanzado: generics, utility types, discriminated unions.  
En VTT: un agente puede generar types desde OpenAPI spec o Prisma client. Es altamente delegable.

**Qué es:** Definiciones TypeScript compartidas del frontend: types de entidades (User, Order, Product), types de API (CreateUserInput, OrderListResponse), types de UI (ButtonVariant, ModalProps, FormState), y utility types (Paginated<T>, ApiResponse<T>). Organizadas en archivos `.d.ts` o `types.ts`.

**Para qué sirve:** TypeScript sin types definidos es JavaScript con pasos extra. Los types dan: autocompletado, detección de errores en compile time, documentación inline, y refactoring seguro. Un type cambia → TypeScript muestra todos los archivos que necesitan actualización.

**Inputs requeridos:**
- `3B.4.1` OpenAPI Spec — API types
- `4.3.5` DTOs/Schemas — schemas del backend
- `4.4.1` Components — component prop types

**Dependencias (predecessors):**
- `3B.4.1` OpenAPI Spec *(obligatorio)* — API contracts

**Habilita (successors):**
- Todo el código frontend — type safety

**Audiencia:**
- **Frontend Developer** — type safety

**Secciones esperadas:**
1. Entity types (`src/types/entities/` — User, Order, Product)
2. API types (`src/types/api/` — requests, responses, errors)
3. UI types (`src/types/ui/` — component props, form state, theme)
4. Utility types (`src/types/utils/` — Paginated<T>, Nullable<T>)
5. Enum types (status, roles, etc.)

**Criterio de completitud:**
- [ ] Types para todas las entidades del dominio
- [ ] Types para API request/response
- [ ] No hay `any` en el codebase (eslint: no-explicit-any)
- [ ] Types exportados y reutilizados (no duplicados)
- [ ] Alineados con los types del backend

**Anti-patrones:**
- ❌ **`any` everywhere:** Derrota el propósito de TypeScript.
- ❌ **Types duplicados:** Frontend y backend definen User diferente — desincronización.
- ❌ **Inline types:** `props: { name: string; age: number }` en cada componente — no reutilizable.
- ❌ **Over-typing:** Type para cada string literal — burocracia sin beneficio.

**Template:** `phases/04-development/deliverables/types/` *(pendiente)*

---

### 4.4.8 Styles

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.4 Frontend Development |
| **Responsable** | Frontend Developer |
| **Ejecuta** | Frontend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | CSS / Tailwind |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Continuo |
| **Frecuencia** | Por componente |

**Perfil de ejecución:** Requiere dominio del approach de styling elegido (Tailwind, CSS Modules, styled-components).  
En VTT: un agente puede generar estilos Tailwind o CSS desde design tokens y specs. Es bastante delegable.

**Qué es:** Implementación de estilos del frontend: CSS variables globales (design tokens), configuración de Tailwind (theme extend con tokens), estilos base (reset, typography, animations), y estilos por componente (CSS Modules, Tailwind classes, o styled-components). Todo consumiendo los design tokens de 3A.9.4.

**Para qué sirve:** Los estilos traducen el design system de Figma a CSS que el browser renderiza. Sin estilos sistematizados, cada componente tiene su propio `padding: 13px; color: #3478af` — inconsistente, no mantenible, y desconectado del design system.

**Inputs requeridos:**
- `3A.9.4` CSS Variables — design tokens en CSS
- `3A.7.1` Design Tokens — valores de referencia
- `3A.9.2` Specs Export — medidas exactas
- `3B.1.5` Technology Stack — approach de styling

**Dependencias (predecessors):**
- `3A.9.4` CSS Variables *(obligatorio)* — tokens
- `3B.1.5` Technology Stack *(obligatorio)* — approach

**Habilita (successors):**
- `4.4.1` Components — componentes consumen estilos
- `4.4.15` Responsive Implementation — media queries

**Audiencia:**
- **Frontend Developer** — styling
- **UI Designer** — validación visual

**Secciones esperadas:**
1. CSS variables globales (`:root { --color-primary: ... }`)
2. Tailwind config (theme.extend con design tokens)
3. Base styles (reset, body, typography defaults)
4. Animation classes/keyframes
5. Utility classes custom (si aplica)
6. Dark mode styles (si aplica)

**Criterio de completitud:**
- [ ] Design tokens implementados como CSS variables
- [ ] Tailwind configurado con tokens (o equivalent approach)
- [ ] Base styles aplicados (reset, typography)
- [ ] No hay colores/spacing hardcoded — todo via tokens
- [ ] Dark mode funcional (si aplica)
- [ ] Animations definidas (transitions, keyframes)

**Anti-patrones:**
- ❌ **Colores hardcoded:** `bg-[#3B82F6]` en Tailwind — usar `bg-primary-500`.
- ❌ **Estilos inline:** `style={{ padding: '13px' }}` — no mantenible, no responsive.
- ❌ **CSS global sin scope:** Estilos que aplican a todo por accidente — usar CSS Modules o scoping.
- ❌ **!important:** Señal de CSS mal estructurado — refactorizar la especificidad.

**Template:** `phases/04-development/deliverables/styles/` *(pendiente)*

---

### 4.4.9 Utils

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.4 Frontend Development |
| **Responsable** | Frontend Developer |
| **Ejecuta** | Frontend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | TypeScript |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Continuo |
| **Frecuencia** | Continua |

**Perfil de ejecución:** Requiere identificar lógica reutilizable del frontend.  
En VTT: un agente puede generar utils comunes del frontend. Es altamente delegable.

**Qué es:** Funciones utilitarias del frontend: formateo (formatDate, formatCurrency, formatNumber), validación (isEmail, isURL), transformación (camelToSnake, slugify), DOM helpers (classNames/clsx, copyToClipboard), y storage helpers (getFromLocalStorage con parsing seguro).

**Para qué sirve:** Misma razón que backend utils (4.3.8) — evitar duplicación de lógica repetitiva en el frontend.

**Inputs requeridos:**
- Necesidades recurrentes durante desarrollo frontend

**Dependencias (predecessors):**
- `3B.2.1` Folder Structure *(obligatorio)* — dónde viven

**Habilita (successors):**
- Todo el código frontend los consume

**Audiencia:**
- **Frontend Developer** — uso diario

**Secciones esperadas:**
1. Format utils (date, currency, number, fileSize)
2. Validation utils (email, URL, phone)
3. String utils (truncate, capitalize, slugify)
4. DOM utils (classNames, copyToClipboard, scrollTo)
5. Storage utils (localStorage wrapper con error handling)

**Criterio de completitud:**
- [ ] Funciones puras y testeadas
- [ ] No duplican funcionalidad de libraries (date-fns, lodash)
- [ ] JSDoc documentados
- [ ] Unit tests por util

**Anti-patrones:**
- ❌ **Reinventar date-fns:** `formatDate()` custom de 50 líneas — usar la library.
- ❌ **Utils con side effects:** Función que modifica el DOM inesperadamente.
- ❌ **Sin tests:** Bug en `formatCurrency()` se propaga a toda la app.

**Template:** `phases/04-development/deliverables/frontend-utils/` *(pendiente)*

---

### 4.4.10 Unit Tests FE

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.4 Frontend Development |
| **Responsable** | Frontend Developer |
| **Ejecuta** | Frontend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | Jest / Vitest |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Continuo (30% del tiempo dev) |
| **Frecuencia** | Por feature |

**Perfil de ejecución:** Requiere testing de React: renderizado, user interactions, hooks, y async behavior.  
En VTT: un agente puede generar tests de hooks y utils. Tests de componentes con interacciones complejas requieren developer.

**Qué es:** Tests unitarios del frontend: tests de hooks custom (useAuth, useDebounce), tests de utils (formatDate, slugify), y tests de lógica de componentes aislada (state transitions, conditional rendering). No incluye component rendering tests (esos son 4.4.11).

**Para qué sirve:** Verifican que la lógica del frontend funciona correctamente de forma aislada, sin renderizar componentes ni conectar con la API.

**Inputs requeridos:**
- `4.4.4` Hooks — hooks a testear
- `4.4.9` Utils — utils a testear

**Dependencias (predecessors):**
- `4.4.4` Hooks *(obligatorio)* — código a testear
- `4.4.9` Utils *(obligatorio)* — código a testear

**Habilita (successors):**
- `4.6.3` Test Coverage Report — coverage medido

**Audiencia:**
- **Frontend Developer** — escribe y mantiene tests

**Secciones esperadas:**
1. Tests de hooks (setup renderHook, verify state changes)
2. Tests de utils (input → output, edge cases)
3. Tests de store/state (actions, reducers, selectors)

**Criterio de completitud:**
- [ ] Hooks custom testeados
- [ ] Utils testeados con edge cases
- [ ] State management testeado
- [ ] Coverage ≥80%
- [ ] Tests pasan en CI sin flakiness

**Anti-patrones:**
- ❌ **Tests que testean React:** Testing que `useState` funciona — eso ya lo testea React.
- ❌ **Tests de implementación:** Verificar que se llamó `setState(5)` en vez de verificar que el output es 5.

**Template:** `phases/04-development/deliverables/unit-tests-fe/` *(pendiente)*

---

### 4.4.11 Component Tests

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.4 Frontend Development |
| **Responsable** | Frontend Developer |
| **Ejecuta** | Frontend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | Testing Library |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Continuo |
| **Frecuencia** | Por componente |

**Perfil de ejecución:** Requiere React Testing Library: render, user events, queries, y assertions.  
En VTT: un agente puede generar component tests. Es bastante delegable para componentes estándar.

**Qué es:** Tests de componentes React con Testing Library: renderizar el componente, simular interacciones de usuario (click, type, select), y verificar que el output visual y funcional es correcto. Testing desde la perspectiva del usuario ("el botón muestra 'Submit'", "al clickear aparece el modal") — no desde la perspectiva de implementación.

**Para qué sirve:** Verifican que los componentes funcionan como el usuario espera: se renderizan correctamente, responden a interacciones, y muestran el contenido correcto. Detectan regresiones visuales y funcionales antes de que lleguen a QA.

**Inputs requeridos:**
- `4.4.1` Components — componentes a testear
- `4.4.2` Pages — pages a testear

**Dependencias (predecessors):**
- `4.4.1` Components *(obligatorio)*

**Habilita (successors):**
- `4.6.3` Test Coverage Report — coverage

**Audiencia:**
- **Frontend Developer** — escribe y mantiene

**Secciones esperadas:**
1. Tests de componentes primitivos (Button renders, handles click)
2. Tests de form components (validates input, shows error)
3. Tests de pages (renders data, handles loading/error)
4. User event simulation (click, type, select, keyboard)

**Criterio de completitud:**
- [ ] Componentes críticos testeados (forms, modals, tables)
- [ ] User interactions simuladas (click, type, select)
- [ ] Accessibility queries usadas (getByRole, getByLabelText — no getByTestId)
- [ ] Async behavior testeado (loading → data, loading → error)
- [ ] Coverage ≥80% de componentes

**Anti-patrones:**
- ❌ **getByTestId para todo:** Testing Library promueve queries accesibles — usar getByRole, getByText.
- ❌ **Snapshot tests como única estrategia:** Snapshots se auto-aprueban y no testean comportamiento.
- ❌ **Tests de implementación:** `expect(setState).toHaveBeenCalled()` — testear output, no implementation.

**Template:** `phases/04-development/deliverables/component-tests/` *(pendiente)*

---

### 4.4.12 Storybook

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.4 Frontend Development |
| **Responsable** | Frontend Developer |
| **Ejecuta** | Frontend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | Storybook |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 2-3 días + continuo |
| **Frecuencia** | Por componente |

**Perfil de ejecución:** Requiere configurar Storybook y crear stories por componente.  
En VTT: un agente puede generar stories desde las component props interfaces. Es altamente delegable.

**Qué es:** Storybook configurado con stories para cada componente: cada story muestra el componente en un estado/variante específica (Button/Primary/Large, Input/Error/Disabled, Modal/Open). Funciona como catálogo visual interactivo de todos los componentes del design system implementados.

**Para qué sirve:** Storybook es el "showroom" de componentes: permite visualizar, interactuar, y testear cada componente de forma aislada (sin necesitar la app completa). Es la referencia para UI Designer (valida implementación vs Figma), para QA (pruebas visuales), y para nuevos developers (catálogo de componentes disponibles).

**Inputs requeridos:**
- `4.4.1` Components — componentes a documentar
- `3A.7.7` Component Documentation — specs a comparar

**Dependencias (predecessors):**
- `4.4.1` Components *(obligatorio)*

**Habilita (successors):**
- Visual regression testing (Chromatic)
- UI review por Design Lead

**Audiencia:**
- **UI Designer** — validación visual
- **Frontend Developer** — catálogo de componentes
- **QA Engineer** — testing visual
- **New developers** — descubrir componentes existentes

**Secciones esperadas:**
1. Storybook configurado y accesible
2. Stories por componente (todas las variantes)
3. Controls/args configurados (props editables interactivamente)
4. Docs page por componente (auto-generada desde props)
5. Stories organizadas por categoría (Primitives, Forms, Feedback, etc.)

**Criterio de completitud:**
- [ ] Storybook configurado y corriendo
- [ ] Cada componente tiene al menos 1 story
- [ ] Variantes principales como stories separadas
- [ ] Controls configurados para props editables
- [ ] Organización por categoría
- [ ] Accesible por todo el equipo (deployed o local)

**Anti-patrones:**
- ❌ **Storybook desactualizado:** Componentes nuevos sin stories — el catálogo no refleja la realidad.
- ❌ **Una story por componente:** Solo el default state — pierde el valor de ver variantes.
- ❌ **Sin controls:** No poder editar props interactivamente — pierde interactividad.

**Template:** `phases/04-development/deliverables/storybook/` *(pendiente)*

---

### 4.4.13 Frontend README

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.4 Frontend Development |
| **Responsable** | Frontend Developer |
| **Ejecuta** | Frontend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | README.md |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez + actualizaciones |

**Perfil de ejecución:** Requiere documentación técnica del frontend.  
En VTT: un agente puede generar el README. Es altamente delegable.

**Qué es:** README específico del frontend: estructura de carpetas, cómo correr, cómo testear, cómo agregar componentes/pages nuevas, convenciones de styling, y guía de contribución frontend-specific.

**Para qué sirve:** Onboarding de developers nuevos al frontend. Un developer que conoce React lee este README y entiende las convenciones específicas del proyecto.

**Inputs requeridos:**
- Frontend implementado (4.4.1-4.4.12)
- `3B.2.1` Folder Structure — estructura

**Dependencias (predecessors):**
- Frontend implementado

**Habilita (successors):**
- Onboarding de developers

**Audiencia:**
- **Frontend Developer** — referencia y onboarding

**Secciones esperadas:**
1. Folder structure con descripción
2. Cómo agregar un componente nuevo (step-by-step)
3. Cómo agregar una page nueva
4. Convenciones de styling
5. Testing guide
6. Storybook guide

**Criterio de completitud:**
- [ ] Estructura documentada
- [ ] "How to" para componente y page nuevos
- [ ] Convenciones documentadas
- [ ] Probado por developer que no lo escribió

**Anti-patrones:**
- ❌ **README genérico:** "Frontend built with React" — sin valor.
- ❌ **Sin how-to:** Documenta qué hay pero no cómo contribuir.

**Template:** `phases/04-development/deliverables/frontend-readme.md` *(pendiente)*

---

### 4.4.14 Accessibility

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.4 Frontend Development |
| **Responsable** | Frontend Developer |
| **Ejecuta** | Frontend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | ARIA (en código) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Continuo (incluido en cada componente) |
| **Frecuencia** | Continua |

**Perfil de ejecución:** Requiere conocimiento de WCAG 2.1 AA, ARIA roles, keyboard navigation, y screen reader behavior.  
En VTT: un agente puede agregar ARIA attributes, roles, y keyboard handlers a componentes existentes. Es bastante delegable.

**Qué es:** Implementación de accesibilidad en el frontend: ARIA roles y labels en componentes interactivos, keyboard navigation (Tab, Enter, Escape, Arrow keys), focus management (focus trap en modals, focus visible), color contrast (WCAG AA: 4.5:1), y semantic HTML (headings hierarchy, landmarks, alt text).

**Para qué sirve:** Accesibilidad no es opcional — es un requisito legal en muchas jurisdicciones (ADA, EAA) y una buena práctica de UX. Un producto no accesible excluye a usuarios con discapacidades visuales, motoras, o cognitivas. WCAG AA es el estándar mínimo.

**Inputs requeridos:**
- `3A.7.7` Component Documentation — a11y specs por componente
- WCAG 2.1 AA guidelines
- `4.4.1` Components — componentes a hacer accesibles

**Dependencias (predecessors):**
- `4.4.1` Components *(obligatorio)* — componentes implementados

**Habilita (successors):**
- `5.9.1` Accessibility Testing — testing de a11y
- Compliance con WCAG 2.1 AA

**Audiencia:**
- **Frontend Developer** — implementación
- **QA Engineer** — testing de a11y
- **Compliance** — evidencia de accesibilidad

**Secciones esperadas:**
1. ARIA roles y labels en componentes interactivos
2. Keyboard navigation implementada (Tab order, Enter/Escape handlers)
3. Focus management (focus trap, focus visible, skip links)
4. Semantic HTML (headings h1-h6, nav, main, aside, footer)
5. Alt text en imágenes
6. Color contrast verificado (≥4.5:1 para texto normal)
7. Screen reader testing results

**Criterio de completitud:**
- [ ] Todos los componentes interactivos tienen ARIA labels
- [ ] Keyboard navigation funcional (Tab through all interactive elements)
- [ ] Focus visible en todos los interactive elements
- [ ] Focus trap en modals y drawers
- [ ] Semantic HTML (landmarks, headings)
- [ ] Color contrast ≥4.5:1 (WCAG AA)
- [ ] axe-core lint plugin configurado (0 violations)
- [ ] Screen reader testing básico (VoiceOver/NVDA)

**Anti-patrones:**
- ❌ **div como button:** `<div onClick={}>` sin role="button", sin keyboard handler — inaccessible.
- ❌ **Sin focus visible:** Outline removed (`outline: none`) sin alternativa — keyboard users no saben dónde están.
- ❌ **Imágenes sin alt:** Screen reader dice "image" sin descripción.
- ❌ **a11y como afterthought:** "Lo agregamos después del launch" — después nunca llega.

**Template:** `phases/04-development/deliverables/accessibility/` *(pendiente)*

---

### 4.4.15 Responsive Implementation

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.4 Frontend Development |
| **Responsable** | Frontend Developer |
| **Ejecuta** | Frontend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | CSS |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Continuo (incluido en cada componente/page) |
| **Frecuencia** | Continua |

**Perfil de ejecución:** Requiere implementar media queries, flex/grid layouts responsive, y testing en múltiples viewports.  
En VTT: un agente puede generar responsive CSS/Tailwind desde los responsive breakpoints y variantes. Es bastante delegable.

**Qué es:** Implementación responsive del frontend: media queries (o Tailwind responsive prefixes), layouts que se adaptan entre breakpoints (sidebar collapse, column reflow, element hide/show), touch targets en mobile (44px+), y viewport-specific behavior (scroll, navigation, typography scale).

**Para qué sirve:** El producto debe funcionar en desktop (1440px), laptop (1280px), tablet (768px), y mobile (375px). Sin responsive implementation, el desktop design se ve roto en mobile — texto cortado, botones fuera de pantalla, layouts solapados.

**Inputs requeridos:**
- `3A.4.9` Responsive Breakpoints — breakpoints definidos
- `3A.5.10` Responsive Variants — variantes visuales por breakpoint
- `3A.9.5` Redlines — medidas por breakpoint

**Dependencias (predecessors):**
- `3A.4.9` Responsive Breakpoints *(obligatorio)*
- `3A.5.10` Responsive Variants *(obligatorio)*
- `4.4.1` Components *(obligatorio)* — componentes a hacer responsive
- `4.4.3` Layouts *(obligatorio)* — layouts responsive

**Habilita (successors):**
- `5.4.2` Cross-browser Testing — testing en múltiples devices
- Producto funcional en todos los viewports

**Audiencia:**
- **Frontend Developer** — implementación
- **QA Engineer** — testing en múltiples viewports
- **UI Designer** — validación visual por breakpoint

**Secciones esperadas:**
1. Breakpoints implementados (Tailwind config o CSS media queries)
2. Layout responsive (sidebar collapse, grid reflow)
3. Typography responsive (font-size adjustments si aplica)
4. Component responsive (table → card list en mobile, tabs → accordion)
5. Navigation responsive (topbar → hamburger, sidebar → drawer)
6. Touch targets ≥44px en mobile
7. Viewport meta tag configurado

**Criterio de completitud:**
- [ ] Funcional en desktop (1280px+), tablet (768px), mobile (375px)
- [ ] Sidebar collapsa en mobile
- [ ] Navigation mobile funcional (hamburger/bottom tabs)
- [ ] Touch targets ≥44px en mobile
- [ ] No hay horizontal scroll en ningún breakpoint
- [ ] Texto legible en todos los breakpoints (no cortado, no overflow)
- [ ] Testeado en device real o emulator

**Anti-patrones:**
- ❌ **Solo desktop:** "El mobile ya lo hacemos" — nunca se hace bien después.
- ❌ **Media queries ad-hoc:** `@media (max-width: 847px)` — usar los breakpoints definidos.
- ❌ **Horizontal scroll en mobile:** Contenido que se sale del viewport — UX rota.
- ❌ **Text overflow sin handling:** Títulos largos que desbordan containers — usar truncate o wrap.

**Template:** `phases/04-development/deliverables/responsive/` *(pendiente)*

---

## Tabla resumen de ejecutores — Fase 4.4 Frontend Development

| Deliverable | Responsable | Ejecuta | Delegable VTT |
|-------------|-------------|---------|---------------|
| 4.4.1 Components | Frontend Developer | Frontend Developer | 🔶 Parcial — scaffolding sí, lógica interactiva compleja no |
| 4.4.2 Pages | Frontend Developer | Frontend Developer | 🔶 Parcial — scaffolding sí, data flow complejo no |
| 4.4.3 Layouts | Frontend Developer | Frontend Developer | ✅ — puede generar layouts desde wireframes |
| 4.4.4 Hooks | Frontend Developer | Frontend Developer | ✅ — puede generar hooks comunes |
| 4.4.5 State Management | Frontend Developer | Frontend Developer | ✅ — puede generar store config y slices |
| 4.4.6 API Client | Frontend Developer | Frontend Developer | ✅ — puede generar desde OpenAPI spec |
| 4.4.7 Types/Interfaces | Frontend Developer | Frontend Developer | ✅ — puede generar desde OpenAPI/Prisma |
| 4.4.8 Styles | Frontend Developer | Frontend Developer | ✅ — puede generar desde design tokens |
| 4.4.9 Utils | Frontend Developer | Frontend Developer | ✅ — puede generar utils comunes |
| 4.4.10 Unit Tests FE | Frontend Developer | Frontend Developer | 🔶 Parcial — tests de utils sí, tests de lógica compleja no |
| 4.4.11 Component Tests | Frontend Developer | Frontend Developer | 🔶 Parcial — tests estándar sí, interacciones complejas no |
| 4.4.12 Storybook | Frontend Developer | Frontend Developer | ✅ — puede generar stories desde props |
| 4.4.13 Frontend README | Frontend Developer | Frontend Developer | ✅ — puede generar README completo |
| 4.4.14 Accessibility | Frontend Developer | Frontend Developer | ✅ — puede agregar ARIA y keyboard handlers |
| 4.4.15 Responsive Implementation | Frontend Developer | Frontend Developer | ✅ — puede generar responsive CSS desde breakpoints |

---

## Siguiente archivo

**Próximo:** `DICCIONARIO_FASE_04_05_INTEGRATIONS.md` — 9 deliverables (4.5.1 a 4.5.9)
