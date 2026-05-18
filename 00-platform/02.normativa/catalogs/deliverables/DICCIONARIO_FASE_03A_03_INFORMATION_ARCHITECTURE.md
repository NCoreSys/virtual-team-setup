# DICCIONARIO DE DELIVERABLES — FASE 3A.3: INFORMATION ARCHITECTURE

**Versión:** 1.1  
**Fecha:** 2026-05-14  
**Fase:** 3A — Design UX/UI  
**Subfase:** 3A.3 — Information Architecture  
**Total deliverables:** 8  
**Responsable de subfase:** UX Designer  
**Aprueba:** Design Lead

---

## Contexto de la subfase

Information Architecture (IA) define cómo se organiza, estructura y etiqueta el contenido del producto para que los usuarios encuentren lo que buscan y entiendan dónde están. Es el esqueleto invisible del producto: el usuario no "ve" la IA, pero la experimenta cada vez que navega, busca, o se pierde. Una buena IA hace que todo sea intuitivo; una mala IA produce usuarios frustrados que no encuentran nada.

**Prerequisitos de subfase:**
- Personas definidas (3A.2) — mental models de los usuarios
- User Research (3A.1) — cómo organizan la información actualmente
- Use Cases (2.3) — funcionalidades a organizar

**Entrega de subfase:**
- Estructura de información completa: sitemap, navegación, taxonomía, y URL structure

---

### 3A.3.1 Site Map

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.3 Information Architecture |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Diagrama |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Una vez + actualizaciones por feature nueva |

**Perfil de ejecución:** Requiere capacidad de organizar jerárquicamente las secciones y páginas del producto de forma lógica y alineada al mental model del usuario.  
En VTT: un agente puede generar el sitemap en Mermaid o como diagrama de árbol a partir de la lista de pantallas derivada de los use cases. Es bastante delegable. Necesita brief con: lista de secciones/módulos del producto, jerarquía de páginas, y relaciones entre secciones.

**Qué es:** Diagrama jerárquico que muestra todas las páginas/pantallas del producto organizadas en secciones, con sus relaciones padre-hijo. Muestra la estructura completa del producto de un vistazo: cuántas secciones principales hay, cuántos niveles de profundidad, y qué contiene cada sección.

**Para qué sirve:** Es el mapa del producto. Permite al equipo ver la estructura completa antes de diseñar pantallas individuales. Detecta problemas temprano: secciones huérfanas, jerarquía demasiado profunda (>3 niveles), secciones desbalanceadas (una con 20 páginas y otra con 2). También es la base para la navegación y la URL structure.

**Inputs requeridos:**
- `2.3.3` Use Case List — funcionalidades a organizar
- `3A.2.3` Primary Persona — mental model del usuario principal
- `3A.1.9` Behavioral Patterns — cómo los usuarios organizan mentalmente la información
- `3A.3.6` Card Sorting Results — organización validada por usuarios

**Dependencias (predecessors):**
- `2.3.3` Use Case List *(obligatorio)* — funcionalidades a incluir
- `3A.2.3` Primary Persona *(obligatorio)* — mental model del usuario
- `3A.3.6` Card Sorting Results *(recomendado)* — organización validada

**Habilita (successors):**
- `3A.3.2` Navigation Structure — navegación derivada del sitemap
- `3A.3.7` Menu Structure — menús basados en la jerarquía
- `3A.3.8` URL Structure — URLs derivadas del sitemap
- `3A.4.1` Wireframe Document — pantallas a wireframear

**Audiencia:**
- **UX Designer** — estructura del producto
- **UI Designer** — pantallas a diseñar
- **Frontend Developer** — rutas a implementar
- **Product Owner** — validación de scope visual
- **Content Writer** — estructura de contenido

**Secciones esperadas:**
1. Diagrama de sitemap (tree diagram)
2. Leyenda (página, sección, modal, external link)
3. Niveles de profundidad por sección
4. Páginas condicionales (por rol, por estado)
5. Tabla complementaria (página, sección padre, acceso: público/autenticado/admin)

**Criterio de completitud:**
- [ ] Todas las pantallas del producto representadas
- [ ] Jerarquía máxima de 3 niveles (idealmente)
- [ ] Secciones principales alineadas al mental model del usuario
- [ ] Páginas de sistema incluidas (login, register, 404, settings)
- [ ] Leyenda incluida
- [ ] Validado contra use cases (cada use case tiene sus pantallas)

**Anti-patrones:**
- ❌ **Sitemap de la organización:** Organizar el producto por departamentos internos ("Ventas", "RRHH") en vez del mental model del usuario.
- ❌ **Más de 3 niveles:** Settings > Account > Security > Privacy > Cookies — demasiado profundo, el usuario se pierde.
- ❌ **Sin páginas de sistema:** Olvidar login, register, 404, error, loading — no son features pero son pantallas.
- ❌ **Sitemap = menú:** El sitemap es más que el menú — incluye páginas de detalle, modals, y flujos que no aparecen en la nav.

**Template:** `phases/03-design/deliverables/site-map.mmd` *(pendiente)*

---

### 3A.3.2 Navigation Structure

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.3 Information Architecture |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Diagrama |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5-1 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere entendimiento de tipos de navegación y cuándo usar cada uno (global nav, local nav, utility nav, breadcrumbs).  
En VTT: un agente puede documentar la estructura de navegación a partir del sitemap. Es bastante delegable. Necesita brief con: sitemap, tipo de navegación elegida (sidebar, top bar, bottom tabs), y plataforma (web, mobile, ambas).

**Qué es:** Definición de cómo se navega el producto: navegación global (siempre visible), navegación local (contextual a la sección), navegación de utilidad (settings, profile, help), breadcrumbs, y shortcuts. Define qué aparece en cada nivel de navegación y cómo se conectan las secciones.

**Para qué sirve:** El sitemap dice qué páginas existen. La navigation structure dice cómo se llega a ellas. Un producto con 50 páginas y mala navegación es un laberinto. La estructura de navegación asegura que el usuario siempre sabe: dónde está, cómo llegó, y a dónde puede ir.

**Inputs requeridos:**
- `3A.3.1` Site Map — estructura a navegar
- `3A.2.3` Primary Persona — patrones de navegación preferidos
- Plataforma target (web, mobile, ambas)

**Dependencias (predecessors):**
- `3A.3.1` Site Map *(obligatorio)*

**Habilita (successors):**
- `3A.3.3` Navigation Patterns — patrones de UI elegidos
- `3A.3.7` Menu Structure — menús como implementación
- `3A.4.1` Wireframe Document — navegación en wireframes

**Audiencia:**
- **UX Designer** — diseño de navegación
- **UI Designer** — componentes de navegación
- **Frontend Developer** — routing implementación

**Secciones esperadas:**
1. Navegación global (ítems siempre visibles)
2. Navegación local (ítems por sección)
3. Navegación de utilidad (profile, settings, help, notifications)
4. Breadcrumbs (reglas de generación)
5. Shortcuts / Quick actions
6. Diferencias mobile vs desktop
7. Diagrama de flujo de navegación

**Criterio de completitud:**
- [ ] Navegación global definida (5-7 ítems max)
- [ ] Navegación local definida por sección
- [ ] Breadcrumbs rules definidas
- [ ] Mobile navigation definida (bottom tabs, hamburger, etc.)
- [ ] Cada página alcanzable en máximo 3 clicks

**Anti-patrones:**
- ❌ **10+ ítems en nav global:** Demasiadas opciones — el usuario no escanea más de 7±2 ítems.
- ❌ **Hamburger menu en desktop:** Oculta la navegación — no hay razón de ocultar en pantallas amplias.
- ❌ **Sin breadcrumbs:** En jerarquías de 3+ niveles, el usuario no sabe cómo regresar.
- ❌ **Navegación inconsistente:** La nav cambia entre secciones — el usuario re-aprende cada vez.

**Template:** `phases/03-design/deliverables/navigation-structure.md` *(pendiente)*

---

### 3A.3.3 Navigation Patterns

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.3 Information Architecture |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Documento (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere conocimiento de UI patterns de navegación y sus trade-offs por plataforma.  
En VTT: un agente puede documentar los navigation patterns elegidos con justificación y referencia visual. Es altamente delegable. Necesita brief con: plataformas target, complejidad del producto, y patrones elegidos por el UX Designer.

**Qué es:** Documento que define qué patrones de UI se usan para la navegación: sidebar (fixed/collapsible), top navigation bar, bottom tabs (mobile), hamburger menu, tab bar, drawer, breadcrumbs, pagination, infinite scroll, etc. Para cada patrón: dónde se usa, justificación, y referencia visual.

**Para qué sirve:** Estandariza la navegación del producto. Sin definir los patterns, cada pantalla inventa su propia navegación: una usa tabs, otra usa sidebar, otra usa bottom tabs — inconsistencia que confunde al usuario.

**Inputs requeridos:**
- `3A.3.2` Navigation Structure — estructura a implementar con patterns
- Plataforma target y device considerations
- Best practices de la plataforma (Material Design, HIG)

**Dependencias (predecessors):**
- `3A.3.2` Navigation Structure *(obligatorio)*

**Habilita (successors):**
- `3A.4.1` Wireframe Document — patterns aplicados en wireframes
- `3A.7.8` Pattern Library — patterns de navegación incluidos
- `4.4.3` Layouts — layouts implementan los patterns

**Audiencia:**
- **UX/UI Designer** — referencia de qué patterns usar
- **Frontend Developer** — componentes de navegación a implementar

**Secciones esperadas:**
1. Patterns seleccionados (tabla: pattern, dónde se usa, plataforma, justificación)
2. Referencia visual por pattern (screenshot o mockup)
3. Responsive behavior (cómo cambia la nav entre breakpoints)
4. Patterns descartados (y por qué)
5. Accessibility considerations (keyboard nav, screen readers)

**Criterio de completitud:**
- [ ] Pattern de navegación global definido (sidebar/topbar/bottom tabs)
- [ ] Pattern de navegación local definido
- [ ] Responsive behavior documentado
- [ ] Justificación por pattern
- [ ] Accessibility considerada

**Anti-patrones:**
- ❌ **Mezclar patterns incompatibles:** Sidebar + bottom tabs + hamburger simultáneamente — sobrecarga de opciones.
- ❌ **Pattern trendy sin justificación:** Usar gesture navigation porque "es moderno" sin evaluar si el usuario lo entiende.
- ❌ **Ignorar platform conventions:** Usar bottom tabs en web desktop o sidebar en mobile — contra las expectativas.

**Template:** `phases/03-design/deliverables/navigation-patterns.md` *(pendiente)*

---

### 3A.3.4 Content Inventory

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.3 Information Architecture |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Designer / Content Writer |
| **Aprueba** | Design Lead |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez + actualizaciones |

**Perfil de ejecución:** Requiere atención al detalle para inventariar todo el contenido del producto.  
En VTT: un agente puede generar el inventario de contenido a partir de los use cases y el sitemap. Es altamente delegable. Necesita brief con: sitemap, tipos de contenido por sección, y fuentes de contenido.

**Qué es:** Inventario exhaustivo de todo el contenido del producto: textos, imágenes, videos, formularios, datos dinámicos, mensajes de error, emails, notificaciones, y ayuda contextual. Para cada pieza: tipo, ubicación, fuente (estático vs dinámico), responsable de creación, y status.

**Para qué sirve:** Identifica todo el contenido que necesita ser creado, curado, o migrado antes del lanzamiento. Sin inventario, el equipo descubre faltantes tarde: "¿quién escribe los emails transaccionales?", "¿de dónde viene el texto de onboarding?", "¿necesitamos traducir esto?".

**Inputs requeridos:**
- `3A.3.1` Site Map — páginas que contienen contenido
- `2.3.4` Detailed Use Cases — contenido dinámico requerido

**Dependencias (predecessors):**
- `3A.3.1` Site Map *(obligatorio)*

**Habilita (successors):**
- `3A.3.5` Taxonomy — categorización del contenido
- `3A.4.7` Wireframe Annotations — contenido en wireframes
- Content creation pipeline

**Audiencia:**
- **Content Writer** — qué contenido crear
- **UX Designer** — qué contenido diseñar
- **Product Owner** — validación de contenido requerido

**Secciones esperadas:**
1. Tabla de inventario (página, tipo de contenido, estático/dinámico, fuente, responsable, status)
2. Contenido estático (copy de UI, legal, ayuda, marketing)
3. Contenido dinámico (datos de usuario, feeds, generado)
4. Mensajes del sistema (errores, confirmaciones, vacío, loading)
5. Emails y notificaciones (transaccionales, marketing)
6. Multimedia (imágenes, iconos, videos, ilustraciones)
7. Contenido pendiente de creación (gap analysis)

**Criterio de completitud:**
- [ ] Todas las páginas del sitemap cubiertas
- [ ] Contenido estático y dinámico diferenciado
- [ ] Mensajes del sistema inventariados
- [ ] Emails transaccionales listados
- [ ] Gap analysis (qué falta crear)
- [ ] Responsable asignado por pieza de contenido

**Anti-patrones:**
- ❌ **"Lorem ipsum everywhere":** Diseñar con placeholder text — nadie piensa en el contenido real hasta que es tarde.
- ❌ **Olvidar mensajes de sistema:** Empty states, errores, confirmaciones no inventariados — se improvisan en desarrollo.
- ❌ **Sin emails transaccionales:** Nadie piensa en el email de "confirma tu cuenta" hasta 2 días antes del launch.

**Template:** `phases/03-design/deliverables/content-inventory.md` *(pendiente)*

---

### 3A.3.5 Taxonomy

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.3 Information Architecture |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Diagrama |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5-1 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere capacidad de crear sistemas de clasificación que sean lógicos para los usuarios.  
En VTT: un agente puede generar taxonomías a partir del content inventory y los card sorting results. Es bastante delegable. Necesita brief con: contenido a categorizar, card sorting results, y business glossary.

**Qué es:** Sistema de clasificación y categorización del contenido del producto: categorías, subcategorías, tags, labels, y sus relaciones jerárquicas y asociativas. Define cómo se organiza el contenido para búsqueda, filtrado, y navegación. Incluye vocabulario controlado (qué términos se usan y cuáles se evitan).

**Para qué sirve:** Si el producto tiene artículos, productos, proyectos, o cualquier contenido categorizable, la taxonomía define cómo se clasifica. Sin taxonomía, cada persona etiqueta diferente: uno pone "Urgente", otro "Prioridad Alta", otro "Critical" — el filtrado no funciona.

**Inputs requeridos:**
- `3A.3.4` Content Inventory — contenido a categorizar
- `3A.3.6` Card Sorting Results — organización validada por usuarios
- `2.5.7` Business Glossary — vocabulario estandarizado

**Dependencias (predecessors):**
- `3A.3.4` Content Inventory *(obligatorio)*
- `3A.3.6` Card Sorting Results *(recomendado)*

**Habilita (successors):**
- `3A.3.7` Menu Structure — categorías como ítems de menú
- `3B.3.5` Data Dictionary — taxonomía reflejada en la BD
- `4.4.1` Components — filtros y categorías en UI

**Audiencia:**
- **UX Designer** — organización del contenido
- **Content Writer** — vocabulario controlado
- **Backend Developer** — categorías como enums/tablas en BD

**Secciones esperadas:**
1. Diagrama de taxonomía (tree o faceted)
2. Categorías principales con definición
3. Subcategorías por categoría
4. Tags / labels (taxonomía plana complementaria)
5. Vocabulario controlado (término preferido, sinónimos, términos evitados)
6. Reglas de categorización (cómo decidir dónde va algo)

**Criterio de completitud:**
- [ ] Categorías principales definidas
- [ ] Jerarquía coherente (no más de 3 niveles)
- [ ] Vocabulario controlado documentado
- [ ] Validada con card sorting (si se realizó)
- [ ] Reglas de categorización documentadas

**Anti-patrones:**
- ❌ **Taxonomía del experto:** Categorías que solo el equipo interno entiende — los usuarios usan vocabulario diferente.
- ❌ **Categorías solapadas:** "Reportes" y "Informes" como categorías separadas — confusión garantizada.
- ❌ **Taxonomía rígida:** Solo jerárquica sin tags — limita la búsqueda facetada.

**Template:** `phases/03-design/deliverables/taxonomy.md` *(pendiente)*

---

### 3A.3.6 Card Sorting Results

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.3 Information Architecture |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Researcher / UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Informe (MD/PDF) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días (ejecución + análisis) |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere conocimiento de card sorting (abierto vs cerrado, presencial vs remoto) y análisis de dendrogramas y similarity matrices.  
En VTT: un agente puede analizar los resultados de card sorting (similarity matrices, dendrogramas) y generar el reporte. NO puede facilitar las sesiones de card sorting. Necesita brief con: datos exportados de la herramienta (Optimal Workshop, UXtweak), tipo de card sorting, y número de participantes.

**Qué es:** Resultados del ejercicio de card sorting con usuarios: cómo agruparon y etiquetaron las piezas de contenido/funcionalidad del producto. Incluye: similarity matrix (qué items se agrupan juntos con más frecuencia), dendrograma (clustering jerárquico), categorías emergentes (en card sorting abierto), y agreement rate (en card sorting cerrado).

**Para qué sirve:** Valida la IA con datos de usuarios reales. En lugar de que el UX Designer organice basándose en su intuición, los usuarios dicen cómo ELLOS organizan la información. El card sorting revela mental models que el equipo no anticipó ("los usuarios agrupan 'facturación' con 'clientes', no con 'finanzas'").

**Inputs requeridos:**
- Lista de items/cards (funcionalidades, páginas, o contenido)
- `3A.2.3` Primary Persona — perfil de participantes
- Herramienta de card sorting (Optimal Workshop, UXtweak, Miro)
- Al menos 15 participantes (para significancia estadística)

**Dependencias (predecessors):**
- `3A.3.4` Content Inventory *(obligatorio)* — items para las cards
- `3A.2.3` Primary Persona *(obligatorio)* — perfil de participantes

**Habilita (successors):**
- `3A.3.1` Site Map — estructura validada
- `3A.3.5` Taxonomy — categorías validadas
- `3A.3.7` Menu Structure — menú basado en agrupación del usuario

**Audiencia:**
- **UX Designer** — IA informada por datos
- **Design Lead** — validación

**Secciones esperadas:**
1. Metodología (abierto/cerrado, herramienta, participantes)
2. Similarity matrix (qué items se agrupan juntos)
3. Dendrograma (clustering jerárquico)
4. Categorías emergentes (en abierto) o agreement rate (en cerrado)
5. Hallazgos principales (agrupaciones sorprendentes, items difíciles de categorizar)
6. Recomendaciones para IA

**Criterio de completitud:**
- [ ] Al menos 15 participantes
- [ ] Similarity matrix generada
- [ ] Hallazgos documentados
- [ ] Recomendaciones para IA derivadas
- [ ] Items difíciles de categorizar identificados

**Anti-patrones:**
- ❌ **Card sorting con el equipo interno:** Los desarrolladores no son los usuarios — su mental model es diferente.
- ❌ **5 participantes:** Muestra insuficiente para card sorting cuantitativo — mínimo 15 para patrones estadísticos.
- ❌ **Ignorar los resultados:** Hacer card sorting y después organizar como quería el UX Designer de todas formas.

**Template:** `phases/03-design/deliverables/card-sorting-results.md` *(pendiente)*

---

### 3A.3.7 Menu Structure

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.3 Information Architecture |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Diagrama |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere capacidad de traducir la navigation structure en menús concretos con labels claros.  
En VTT: un agente puede generar la estructura de menús a partir de la navigation structure y el sitemap. Es altamente delegable. Necesita brief con: navigation structure, sitemap, y roles del sistema (menú puede variar por rol).

**Qué es:** Definición detallada de los menús del producto: menú principal (items, orden, icons, submenús), menús secundarios, menú de usuario (profile, settings, logout), y menús contextuales (right-click, action menus). Para cada menú: items, labels, iconos, y variaciones por rol de usuario.

**Para qué sirve:** Traduce la navigation structure abstracta en la implementación concreta que el usuario ve. Define los labels exactos de cada item (importa: "Proyectos" vs "Mis Proyectos" vs "Projects" cambia la expectativa del usuario). También define variaciones por rol (admin ve más items que user).

**Inputs requeridos:**
- `3A.3.2` Navigation Structure — estructura a implementar
- `3A.3.1` Site Map — páginas accesibles desde menú
- `3A.3.5` Taxonomy — labels y categorías
- `2.5.5` Authorization Rules — ítems por rol

**Dependencias (predecessors):**
- `3A.3.2` Navigation Structure *(obligatorio)*
- `3A.3.1` Site Map *(obligatorio)*

**Habilita (successors):**
- `3A.4.1` Wireframe Document — menú en wireframes
- `3A.7.8` Pattern Library — menú como pattern
- `4.4.3` Layouts — componente de menú implementado

**Audiencia:**
- **UX/UI Designer** — diseño de menús
- **Frontend Developer** — implementación de menús
- **QA Engineer** — verificación de menú por rol

**Secciones esperadas:**
1. Menú principal (items, orden, icons, submenús, links)
2. Menú de usuario (profile, settings, logout)
3. Menús por rol (tabla: item × rol = visible/oculto)
4. Menús contextuales (acciones por entidad)
5. Labels y tooltips
6. Responsive behavior (cómo se colapsa el menú en mobile)

**Criterio de completitud:**
- [ ] Menú principal definido con items y orden
- [ ] Variaciones por rol documentadas
- [ ] Labels definitivos (no placeholders)
- [ ] Iconos asignados a ítems principales
- [ ] Responsive behavior definido

**Anti-patrones:**
- ❌ **Menú de 15 items:** Demasiados — agrupar en submenús o priorizar.
- ❌ **Labels ambiguos:** "Gestión" puede significar 10 cosas diferentes — ser específico.
- ❌ **Menú igual para todos los roles:** Admin y user ven lo mismo — confuso para el user, inseguro para el admin.
- ❌ **Sin iconos:** En mobile, menús text-only son difíciles de escanear.

**Template:** `phases/03-design/deliverables/menu-structure.md` *(pendiente)*

---

### 3A.3.8 URL Structure

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.3 Information Architecture |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Designer / Frontend Developer |
| **Aprueba** | Design Lead |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere conocimiento de URL design: slugs, nested routes, query parameters, y SEO considerations.  
En VTT: un agente puede generar la URL structure completa a partir del sitemap y las naming conventions. Es altamente delegable. Necesita brief con: sitemap, naming conventions (kebab-case), y si hay consideraciones de SEO.

**Qué es:** Tabla que define la URL de cada página/pantalla del producto: path, parámetros dinámicos (`:id`, `:slug`), query parameters, y relación con el sitemap. Las URLs deben ser legibles, predecibles, y reflejar la jerarquía de la IA.

**Para qué sirve:** URLs bien diseñadas son navegación en sí mismas: `/projects/123/tasks` le dice al usuario dónde está. URLs también afectan SEO, shareability (compartir un link que tiene sentido), y bookmarking. Definir URLs antes de implementar evita refactoring costoso.

**Inputs requeridos:**
- `3A.3.1` Site Map — páginas a mapear
- `3B.2.5` Naming Conventions — convención de URLs (kebab-case)
- `3B.4.2` Endpoints List — alineación con API routes (si aplica)

**Dependencias (predecessors):**
- `3A.3.1` Site Map *(obligatorio)*

**Habilita (successors):**
- `4.4.4` Routing — implementación de rutas frontend
- `3B.4.2` Endpoints List — consistencia con API paths
- SEO strategy — URLs optimizadas

**Audiencia:**
- **Frontend Developer** — implementación de routing
- **UX Designer** — URLs como parte de la IA
- **SEO** — URLs optimizadas para buscadores

**Secciones esperadas:**
1. Tabla de URLs (page, path, params, query params, auth required)
2. Convenciones (kebab-case, plural resources, max depth)
3. Parámetros dinámicos (`:id`, `:slug`)
4. Query parameters estándar (tab, filter, sort, page)
5. Redirects (URLs legacy si hay migración)
6. URLs públicas vs autenticadas

**Criterio de completitud:**
- [ ] Todas las páginas del sitemap tienen URL definida
- [ ] Convención de naming consistente (kebab-case)
- [ ] Parámetros dinámicos documentados
- [ ] Max profundidad razonable (3-4 segments max)
- [ ] URLs legibles y predecibles

**Anti-patrones:**
- ❌ **URLs con IDs numéricos expuestos:** `/users/47382` — expone conteo de usuarios y es enumerable.
- ❌ **URLs ilegibles:** `/app/m/2/v/detail?ref=abc123` — el usuario no puede inferir dónde está.
- ❌ **Inconsistencia de casing:** `/user-profile`, `/userSettings`, `/User_Dashboard` — 3 convenciones en una app.
- ❌ **URLs demasiado profundas:** `/org/team/project/sprint/task/subtask/comment` — 7 niveles es excesivo.

**Template:** `phases/03-design/deliverables/url-structure.md` *(pendiente)*

---

## Tabla resumen de ejecutores — Fase 3A.3 Information Architecture

| Deliverable | Responsable | Ejecuta | Delegable VTT |
|-------------|-------------|---------|---------------|
| 3A.3.1 Site Map | UX Designer | UX Designer | ✅ — puede generar sitemap en Mermaid desde use cases y estructura |
| 3A.3.2 Navigation Structure | UX Designer | UX Designer | ✅ — puede documentar estructura de navegación |
| 3A.3.3 Navigation Patterns | UX Designer | UX Designer | ✅ — puede documentar patterns con justificación |
| 3A.3.4 Content Inventory | UX Designer | UX Designer / Content Writer | ✅ — puede generar inventario desde sitemap y use cases |
| 3A.3.5 Taxonomy | UX Designer | UX Designer | ✅ — puede generar taxonomía desde content inventory |
| 3A.3.6 Card Sorting Results | UX Designer | UX Researcher | 🔶 Parcial — puede analizar datos, no puede facilitar sesiones |
| 3A.3.7 Menu Structure | UX Designer | UX Designer | ✅ — puede generar estructura de menús desde navigation |
| 3A.3.8 URL Structure | UX Designer | UX Designer / Frontend Dev | ✅ — puede generar URL structure desde sitemap |

---

## Siguiente archivo

**Próximo:** `DICCIONARIO_FASE_03A_04_WIREFRAMES.md` — 9 deliverables (3A.4.1 a 3A.4.9)
