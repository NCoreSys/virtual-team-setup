# DICCIONARIO DE DELIVERABLES — FASE 3A.4: WIREFRAMES

**Versión:** 1.1  
**Fecha:** 2026-05-14  
**Fase:** 3A — Design UX/UI  
**Subfase:** 3A.4 — Wireframes  
**Total deliverables:** 9  
**Responsable de subfase:** UX Designer  
**Aprueba:** Design Lead

---

## Contexto de la subfase

Wireframes son el blueprint del producto: definen la estructura, layout y jerarquía de contenido de cada pantalla SIN diseño visual (sin colores, sin tipografía final, sin imágenes reales). Son el equivalente arquitectónico de los planos de una casa — muestran dónde va cada habitación antes de elegir los muebles. Iterar en wireframes es 10x más barato que iterar en mockups de alta fidelidad.

**Prerequisitos de subfase:**
- Information Architecture (3A.3) — estructura de navegación y sitemap
- Personas (3A.2) — para quién se diseña
- Use Cases (2.3) — funcionalidades a diseñar

**Entrega de subfase:**
- Wireframes de todas las pantallas del producto, en versiones desktop y mobile, con flujos conectados y anotaciones

---

### 3A.4.1 Wireframe Document

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.4 Wireframes |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | PDF |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día (compilación) |
| **Frecuencia** | Una vez + actualizaciones |

**Perfil de ejecución:** Requiere capacidad de organizar y presentar wireframes de forma navegable con contexto por pantalla.  
En VTT: un agente puede generar el documento contenedor que organiza todos los wireframes con índice, contexto por flujo, y anotaciones. NO puede crear los wireframes visuales. Necesita brief con: lista de wireframes creados, flujos, y notas del UX Designer.

**Qué es:** Documento consolidado que presenta todos los wireframes del proyecto organizados por flujo/módulo: índice de pantallas, contexto narrativo por flujo, wireframes embebidos o linkeados, y anotaciones de comportamiento. Es la entrega formal de wireframes para review.

**Para qué sirve:** Organiza los wireframes dispersos en Figma en un documento presentable y navegable. Permite al Design Lead y al Product Owner revisar los wireframes con contexto, no como frames aislados. Incluye la narrativa de por qué cada pantalla existe y qué decisiones de UX se tomaron.

**Inputs requeridos:**
- `3A.4.2` a `3A.4.9` — todos los wireframes individuales
- `3A.3.1` Site Map — estructura del producto
- `2.3.4` Detailed Use Cases — flujos implementados

**Dependencias (predecessors):**
- `3A.4.2` Low-Fi Wireframes *(obligatorio)*
- `3A.4.3` Mid-Fi Wireframes *(obligatorio)*
- `3A.3.1` Site Map *(obligatorio)* — estructura del producto

**Habilita (successors):**
- `3A.5.1` UI Mockups Complete — mockups basados en wireframes aprobados
- Review y aprobación de Design Lead y Product Owner

**Audiencia:**
- **Design Lead** — review y aprobación
- **Product Owner** — validación de que los flujos son correctos
- **UI Designer** — base para mockups
- **Frontend Developer** — preview de la estructura

**Secciones esperadas:**
1. Índice de pantallas (tabla: nombre, flujo, versión desktop/mobile, status)
2. Por cada flujo: contexto, user story referenciada, wireframes en secuencia
3. Anotaciones de comportamiento (interacciones, condicionales, edge cases)
4. Decisiones de UX documentadas (por qué esta estructura y no otra)
5. Preguntas abiertas / decisiones pendientes

**Criterio de completitud:**
- [ ] Todas las pantallas del sitemap wireframeadas
- [ ] Organizado por flujo/módulo
- [ ] Anotaciones incluidas
- [ ] Versiones desktop y mobile representadas
- [ ] Revisado por Design Lead

**Anti-patrones:**
- ❌ **"Mira el Figma":** Enviar un link de Figma sin contexto no es un entregable — es una delegación de navegación al reviewer.
- ❌ **Wireframes sin flujo:** Pantallas aisladas sin mostrar cómo se conectan — pierde el journey del usuario.
- ❌ **Sin anotaciones:** Wireframes que solo muestran layout sin explicar comportamiento — ambiguos.

**Template:** `phases/03-design/deliverables/wireframe-document.md` *(pendiente)*

---

### 3A.4.2 Low-Fi Wireframes

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.4 Wireframes |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Sketches (papel/Balsamiq/Excalidraw) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Una vez (fase exploratoria) |

**Perfil de ejecución:** Requiere pensamiento de layout y capacidad de explorar múltiples opciones rápidamente sin invertir en detalle.  
En VTT: un agente NO puede crear wireframes visuales de baja fidelidad. Puede describir textualmente la estructura de cada pantalla (qué elementos, en qué orden, qué jerarquía) como input para el UX Designer. Necesita brief con: pantallas a wireframear y contenido/funcionalidad de cada una.

**Qué es:** Wireframes rápidos y deliberadamente "feos": sketches en papel, Balsamiq, o Excalidraw que exploran la estructura y layout de las pantallas sin preocuparse por detalles. Son borradores para explorar opciones: "¿la nav va arriba o al lado?", "¿el formulario va en modal o en página?", "¿la lista muestra 3 o 5 campos?". Se hacen múltiples versiones por pantalla.

**Para qué sirve:** Permiten explorar e iterar 10x más rápido que wireframes detallados. Si el layout no funciona, se descarta y se hace otro en 5 minutos — no en 2 horas. Son la herramienta de pensamiento del UX Designer, no un entregable final. Se usan para alinear rápidamente con el equipo antes de invertir en detalle.

**Inputs requeridos:**
- `3A.3.1` Site Map — pantallas a wireframear
- `3A.3.2` Navigation Structure — navegación a incluir
- `2.3.4` Detailed Use Cases — funcionalidad por pantalla
- `3A.2.3` Primary Persona — diseño orientado al usuario principal

**Dependencias (predecessors):**
- `3A.3.1` Site Map *(obligatorio)* — pantallas identificadas
- `3A.3.2` Navigation Structure *(obligatorio)* — navegación definida

**Habilita (successors):**
- `3A.4.3` Mid-Fi Wireframes — versión refinada del layout elegido
- Decisiones rápidas de layout con stakeholders

**Audiencia:**
- **UX Designer** — herramienta de exploración propia
- **Design Lead** — review rápido de opciones
- **Product Owner** — feedback temprano de estructura

**Secciones esperadas:**
1. Sketches de pantallas principales (2-3 opciones por pantalla clave)
2. Anotaciones rápidas (qué elemento es qué)
3. Flujos básicos (cómo se conectan las pantallas)
4. Decisiones de layout tomadas (qué opción se eligió y por qué)

**Criterio de completitud:**
- [ ] Pantallas principales exploradas (al menos los 3-5 flujos principales)
- [ ] Múltiples opciones para pantallas clave
- [ ] Feedback del Design Lead/PO obtenido
- [ ] Decisiones de layout documentadas
- [ ] Listas para refinar en mid-fi

**Anti-patrones:**
- ❌ **Low-fi demasiado detallados:** Si parecen mockups, se invirtió demasiado tiempo — el punto es ser rápido y descartable.
- ❌ **Una sola opción:** Solo un layout por pantalla — no se exploró el espacio de diseño.
- ❌ **Saltarse low-fi:** Ir directo a mid-fi o mockups — se pierde la exploración rápida y se compromete con el primer layout.

**Template:** `phases/03-design/deliverables/low-fi-wireframes/` *(pendiente)*

---

### 3A.4.3 Mid-Fi Wireframes

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.4 Wireframes |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Figma |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 3-5 días |
| **Frecuencia** | Una vez + iteraciones |

**Perfil de ejecución:** Requiere dominio de Figma y capacidad de traducir los low-fi sketches en wireframes limpios con proporciones correctas, texto real (no lorem ipsum), y componentes reutilizables.  
En VTT: un agente NO puede crear wireframes en Figma. Puede generar las especificaciones textuales detalladas de cada pantalla (qué elementos, orden, contenido placeholder, comportamiento) como brief para el UX Designer. Necesita brief con: low-fi wireframes aprobados y contenido real disponible.

**Qué es:** Wireframes en Figma con proporciones reales, tipografía genérica (no la final), grises para jerarquía visual, texto real (o realistic placeholder), y componentes básicos reutilizables. Son suficientemente detallados para que un stakeholder no-diseñador entienda la pantalla, pero suficientemente abstractos para no distraer con decisiones visuales.

**Para qué sirve:** Son el entregable principal de wireframing: aprobados estos, se pasa a mockups. Definen la estructura final de cada pantalla con suficiente detalle para que el UI Designer sepa qué elementos diseñar y el PO pueda validar que el flujo es correcto. Son la "especificación de estructura" del producto.

**Inputs requeridos:**
- `3A.4.2` Low-Fi Wireframes — layout elegido
- `3A.3.7` Menu Structure — navegación
- `3A.3.4` Content Inventory — contenido a incluir
- `2.3.4` Detailed Use Cases — funcionalidad por pantalla

**Dependencias (predecessors):**
- `3A.4.2` Low-Fi Wireframes *(obligatorio)* — layout aprobado
- `3A.3.2` Navigation Structure *(obligatorio)* — navegación
- `3A.3.4` Content Inventory *(recomendado)* — contenido real

**Habilita (successors):**
- `3A.4.4` Desktop Wireframes — wireframes desktop derivados
- `3A.4.5` Mobile Wireframes — wireframes mobile derivados
- `3A.4.7` Wireframe Annotations — anotaciones sobre mid-fi
- `3A.4.8` Wireframe Flows — flujos conectados
- `3A.5.1` UI Mockups Complete — base para mockups

**Audiencia:**
- **Design Lead** — aprobación de estructura
- **Product Owner** — validación de flujos
- **UI Designer** — base para mockups
- **Frontend Developer** — preview de componentes

**Secciones esperadas:**
1. Wireframes por pantalla en Figma (frames organizados por flujo)
2. Componentes wireframe reutilizables (button, input, card, table wireframe)
3. Texto real o realistic placeholder (no lorem ipsum)
4. Jerarquía visual con grises (heading, body, secondary text)
5. Interacciones básicas indicadas (qué es clickeable)

**Criterio de completitud:**
- [ ] Todas las pantallas del sitemap wireframeadas
- [ ] Texto real o realistic placeholder (no lorem ipsum)
- [ ] Componentes wireframe reutilizables creados
- [ ] Jerarquía visual clara (heading > body > secondary)
- [ ] Navegación incluida en todas las pantallas
- [ ] Aprobados por Design Lead

**Anti-patrones:**
- ❌ **Lorem ipsum:** Texto placeholder genérico no revela problemas de contenido (texto demasiado largo, labels ambiguos).
- ❌ **Wireframes demasiado bonitos:** Si parecen mockups, el PO da feedback visual en vez de estructural — se pierde el punto.
- ❌ **Sin componentes reutilizables:** Cada pantalla tiene su propio "botón" ad-hoc — inconsistencia y más trabajo.
- ❌ **Solo desktop:** Wireframear solo desktop y "ya luego hacemos el mobile" — el mobile afterthought siempre sale mal.

**Template:** `phases/03-design/deliverables/mid-fi-wireframes.figma` *(pendiente)*

---

### 3A.4.4 Desktop Wireframes

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.4 Wireframes |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Figma |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Incluido en 3A.4.3 |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere diseño para viewport de 1280px+ con consideraciones de wide screen y content width.  
En VTT: un agente NO puede crear wireframes en Figma. Puede especificar la estructura por pantalla textualmente.

**Qué es:** Versión desktop de los mid-fi wireframes, diseñada para viewports de 1280px+ (laptop/desktop). Incluye layout con sidebar o topbar navigation, content area con max-width apropiado, y aprovechamiento del espacio horizontal (multi-column layouts, side panels).

**Para qué sirve:** Desktop es generalmente donde se diseña primero para apps B2B/SaaS (desktop-first) o donde se adapta después para apps consumer (mobile-first). Los wireframes desktop definen el layout con más espacio disponible, que luego se comprime/reorganiza para mobile.

**Inputs requeridos:**
- `3A.4.3` Mid-Fi Wireframes — base
- `3A.3.2` Navigation Structure — nav desktop (sidebar/topbar)
- `3A.4.9` Responsive Breakpoints — breakpoint desktop definido

**Dependencias (predecessors):**
- `3A.4.3` Mid-Fi Wireframes *(obligatorio)*

**Habilita (successors):**
- `3A.5.2` Desktop Mockups — mockups desktop basados en wireframes
- `3A.4.8` Wireframe Flows — flujos desktop

**Audiencia:**
- **UI Designer** — base para desktop mockups
- **Frontend Developer** — estructura desktop

**Secciones esperadas:**
1. Wireframes de todas las pantallas en viewport desktop (1280px+)
2. Layout patterns aplicados (sidebar + content, topbar + content, full-width)
3. Content max-width definido
4. Multi-column layouts donde aplique

**Criterio de completitud:**
- [ ] Todas las pantallas en versión desktop
- [ ] Navigation desktop incluida (sidebar/topbar)
- [ ] Content max-width consistente
- [ ] Layout aprovecha el espacio horizontal

**Anti-patrones:**
- ❌ **Content full-width:** Texto que se estira a 1920px — ilegible, el ojo se pierde.
- ❌ **Ignorar wide screens:** Diseñar para 1280px y no considerar 1920px+ — layout se rompe.

**Template:** `phases/03-design/deliverables/desktop-wireframes.figma` *(pendiente)*

---

### 3A.4.5 Mobile Wireframes

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.4 Wireframes |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Figma |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 2-3 días |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere diseño mobile-aware: thumb zones, touch targets (44px min), single-column layouts, y priorización de contenido para viewport limitado.  
En VTT: un agente NO puede crear wireframes en Figma. Puede especificar qué cambia entre desktop y mobile por pantalla.

**Qué es:** Versión mobile de los wireframes, diseñada para viewports de 375px (iPhone) y 360px (Android). Reimagina cada pantalla desktop para mobile: single-column layout, navegación colapsada (hamburger/bottom tabs), touch-friendly targets, y contenido priorizado (qué se muestra, qué se oculta, qué se reordena).

**Para qué sirve:** Mobile no es "desktop comprimido" — es un rediseño de la experiencia para un contexto diferente (pantalla chica, touch, una mano, distracciones, conectividad variable). Los wireframes mobile aseguran que la experiencia mobile es first-class, no un afterthought.

**Inputs requeridos:**
- `3A.4.3` Mid-Fi Wireframes — estructura base
- `3A.3.3` Navigation Patterns — navegación mobile (bottom tabs, hamburger)
- `3A.4.9` Responsive Breakpoints — breakpoints mobile
- Mobile platform guidelines (Material Design, HIG)

**Dependencias (predecessors):**
- `3A.4.3` Mid-Fi Wireframes *(obligatorio)*
- `3A.3.3` Navigation Patterns *(obligatorio)* — nav mobile definida

**Habilita (successors):**
- `3A.5.3` Mobile Mockups — mockups mobile
- `3A.4.8` Wireframe Flows — flujos mobile

**Audiencia:**
- **UI Designer** — base para mobile mockups
- **Frontend Developer** — estructura responsive

**Secciones esperadas:**
1. Wireframes de pantallas principales en viewport mobile (375px)
2. Navegación mobile (bottom tabs, hamburger, drawer)
3. Adaptaciones de layout (qué cambia vs desktop: reorder, hide, collapse)
4. Touch targets (44px minimum)
5. Gestures (swipe, pull-to-refresh) si aplican

**Criterio de completitud:**
- [ ] Pantallas principales en versión mobile
- [ ] Navegación mobile implementada
- [ ] Touch targets de 44px+ mínimo
- [ ] Contenido priorizado (qué se muestra, qué se colapsa)
- [ ] Adaptaciones documentadas (diff vs desktop)

**Anti-patrones:**
- ❌ **Shrink desktop:** Comprimir la pantalla desktop a 375px sin rediseñar — ilegible e inutilizable.
- ❌ **Touch targets de 20px:** Botones y links demasiado pequeños — imposible tocar con precisión.
- ❌ **Toda la info visible:** Mostrar todo lo del desktop en mobile — overload de información.
- ❌ **Mobile afterthought:** "Ya después hacemos el mobile responsive" — siempre sale mal.

**Template:** `phases/03-design/deliverables/mobile-wireframes.figma` *(pendiente)*

---

### 3A.4.6 Tablet Wireframes

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.4 Wireframes |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Figma |
| **Obligatorio** | ⚪ Opcional |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere entendimiento de tablet como viewport intermedio: ni desktop ni mobile, con sus propios patterns (split view, master-detail).  
En VTT: un agente NO puede crear wireframes en Figma. Puede especificar adaptaciones tablet.

**Qué es:** Versión tablet de los wireframes (768px-1024px), si el producto necesita soporte tablet explícito. Los tablets tienen viewport intermedio que permite layouts de 2 columnas pero con touch interface. Patterns específicos: split view (master-detail), panel lateral, y landscape/portrait considerations.

**Para qué sirve:** Si una porción significativa de usuarios usa tablet (educación, retail, field work), los wireframes tablet aseguran que la experiencia no es "ni desktop ni mobile" sino optimizada para tablet. Si el uso tablet es marginal, los breakpoints responsive cubren lo básico.

**Inputs requeridos:**
- `3A.4.4` Desktop Wireframes — layout desktop como referencia
- `3A.4.5` Mobile Wireframes — layout mobile como referencia
- Analytics de uso por device (si disponible)

**Dependencias (predecessors):**
- `3A.4.4` Desktop Wireframes *(obligatorio)*
- `3A.4.5` Mobile Wireframes *(obligatorio)*

**Habilita (successors):**
- `3A.5.4` Tablet Mockups — mockups tablet

**Audiencia:**
- **UI Designer** — base para tablet mockups
- **Frontend Developer** — breakpoints intermedios

**Secciones esperadas:**
1. Wireframes de pantallas principales en viewport tablet (768px/1024px)
2. Adaptaciones de layout (split view, 2-column, panel lateral)
3. Touch targets mantenidos (44px+)
4. Landscape vs portrait considerations

**Criterio de completitud:**
- [ ] Pantallas principales en versión tablet
- [ ] Adaptaciones documentadas (diff vs desktop y mobile)
- [ ] Landscape y portrait considerados
- [ ] Touch targets mantenidos

**Anti-patrones:**
- ❌ **Tablet = desktop chico:** Solo encoger el desktop sin aprovechar patterns tablet (split view, panels).
- ❌ **Tablet wireframes sin justificación:** Hacer wireframes tablet cuando el 1% de usuarios usa tablet — esfuerzo desperdiciado.

**Template:** `phases/03-design/deliverables/tablet-wireframes.figma` *(pendiente)*

---

### 3A.4.7 Wireframe Annotations

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.4 Wireframes |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | En wireframes (Figma) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere capacidad de anticipar las preguntas del UI Designer, developer, y PO, y responderlas con anotaciones.  
En VTT: un agente puede generar el contenido de las anotaciones a partir de los use cases, business rules, y decisiones de UX. Es altamente delegable como texto. Necesita brief con: wireframes, comportamientos interactivos, y reglas de negocio por pantalla.

**Qué es:** Anotaciones superpuestas en los wireframes que explican el comportamiento que no es visible en la imagen estática: qué pasa al hacer click, qué validaciones aplican, qué datos son dinámicos, qué cambia según el estado del usuario, edge cases (formulario vacío, lista sin resultados), y links a use cases/business rules relevantes.

**Para qué sirve:** Un wireframe sin anotaciones es ambiguo: "¿este botón va a una nueva página o abre un modal?", "¿qué pasa si el usuario no ha completado el perfil?", "¿esta lista es paginada o infinite scroll?". Las anotaciones responden estas preguntas antes de que se pregunten.

**Inputs requeridos:**
- `3A.4.3` Mid-Fi Wireframes — wireframes a anotar
- `2.3.4` Detailed Use Cases — comportamiento por pantalla
- `2.5.1` Business Rules Document — reglas que afectan la UI
- `2.5.3` Validation Rules — validaciones en formularios

**Dependencias (predecessors):**
- `3A.4.3` Mid-Fi Wireframes *(obligatorio)*
- `2.3.4` Detailed Use Cases *(obligatorio)*

**Habilita (successors):**
- `3A.5.1` UI Mockups Complete — comportamiento documentado para mockups
- `3A.9.1` Handoff Document — anotaciones se heredan al handoff
- `4.4.1` Components — developers entienden el comportamiento

**Audiencia:**
- **UI Designer** — comportamiento a diseñar visualmente
- **Frontend Developer** — comportamiento a implementar
- **QA Engineer** — criterios de aceptación visual

**Secciones esperadas:**
1. Anotaciones de interacción (click → modal/page/action)
2. Anotaciones de validación (campos requeridos, formatos, mensajes de error)
3. Anotaciones de estado (logueado/no logueado, vacío/con datos, loading)
4. Anotaciones de contenido dinámico (de dónde vienen los datos)
5. Anotaciones de edge cases (0 resultados, overflow de texto, max items)
6. Referencias cruzadas (link a use case, business rule)

**Criterio de completitud:**
- [ ] Todas las pantallas con interacciones tienen anotaciones
- [ ] Comportamiento de cada elemento interactivo documentado
- [ ] Edge cases principales cubiertos (vacío, error, loading)
- [ ] Validaciones de formularios anotadas
- [ ] Referencias a use cases incluidas

**Anti-patrones:**
- ❌ **Wireframes sin anotaciones:** Cada persona interpreta el comportamiento diferente — ambigüedad garantizada.
- ❌ **Anotaciones obvias:** "Este es un botón" — anotar solo lo que no es evidente visualmente.
- ❌ **Demasiadas anotaciones:** Wireframe ilegible por la cantidad de notas — priorizar lo importante.

**Template:** `phases/03-design/deliverables/wireframe-annotations.md` *(pendiente)*

---

### 3A.4.8 Wireframe Flows

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.4 Wireframes |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Figma |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere capacidad de conectar wireframes en secuencias que representan user journeys completos.  
En VTT: un agente NO puede crear flows en Figma. Puede listar la secuencia de pantallas por flujo como especificación para el UX Designer. Necesita brief con: use cases y wireframes creados.

**Qué es:** Wireframes conectados con flechas que muestran la secuencia de pantallas que el usuario recorre para completar un flujo completo: registro, crear un proyecto, hacer una compra, etc. Muestra la progresión desde la pantalla inicial hasta el resultado final, incluyendo decisiones (bifurcaciones) y estados intermedios.

**Para qué sirve:** Los wireframes individuales muestran pantallas; los flows muestran journeys. Un PO puede ver el flujo completo de registro y decir "faltan 2 pantallas" o "este paso es innecesario" — feedback que no es posible mirando pantallas aisladas.

**Inputs requeridos:**
- `3A.4.3` Mid-Fi Wireframes — pantallas a conectar
- `2.6.1` User Flow Diagrams — flujos definidos
- `2.6.2` Happy Path Flows — secuencias principales

**Dependencias (predecessors):**
- `3A.4.3` Mid-Fi Wireframes *(obligatorio)*
- `2.6.1` User Flow Diagrams *(obligatorio)* — flujos de referencia

**Habilita (successors):**
- `3A.6.1` Interactive Prototype — prototipo basado en flujos
- `3A.8.2` Test Script — flujos como base de tareas de testing
- `3A.5.1` UI Mockups Complete — flujos a mockupear

**Audiencia:**
- **Design Lead** — review de journey completo
- **Product Owner** — validación de flujos
- **QA Engineer** — test scenarios

**Secciones esperadas:**
1. Flujo por user journey principal (wireframes conectados con flechas)
2. Decisiones / bifurcaciones (qué pasa si sí/no)
3. Estados intermedios (loading, confirmación, success)
4. Error paths (qué pantalla se muestra si algo falla)
5. Entry y exit points de cada flujo

**Criterio de completitud:**
- [ ] Los 3-5 flujos principales conectados
- [ ] Happy path completo por flujo
- [ ] Al menos 1 error path por flujo principal
- [ ] Decisiones/bifurcaciones documentadas
- [ ] Entry y exit points claros

**Anti-patrones:**
- ❌ **Solo happy path:** No mostrar qué pasa cuando algo falla — el developer inventa.
- ❌ **Flujos lineales sin decisiones:** Todo flujo real tiene bifurcaciones — si no se muestran, no se diseñaron.
- ❌ **Flujos de 15 pantallas:** Demasiados pasos — señal de que el flujo necesita simplificación.

**Template:** `phases/03-design/deliverables/wireframe-flows.figma` *(pendiente)*

---

### 3A.4.9 Responsive Breakpoints

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.4 Wireframes |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Designer / Frontend Developer |
| **Aprueba** | Design Lead |
| **Formato** | Documento (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere conocimiento de responsive design y cómo los breakpoints afectan el layout.  
En VTT: un agente puede documentar los breakpoints estándar y las reglas de adaptación por breakpoint. Es altamente delegable. Necesita brief con: plataformas target, framework CSS (Tailwind breakpoints, Bootstrap), y decisiones de layout mobile vs desktop.

**Qué es:** Documento que define los breakpoints responsive del producto: a qué anchos de pantalla cambia el layout (mobile: 375px, tablet: 768px, desktop: 1024px, wide: 1440px), y qué cambia en cada breakpoint (navegación, columnas, spacing, visibilidad de elementos, tamaños de fuente).

**Para qué sirve:** Sin breakpoints definidos, el frontend developer inventa cuándo colapsar la sidebar, cuándo cambiar de 3 columnas a 1, cuándo ocultar elementos. Los breakpoints estándar + las reglas de adaptación aseguran que el responsive es predecible y consistente en todo el producto.

**Inputs requeridos:**
- `3A.4.4` Desktop Wireframes — layout desktop
- `3A.4.5` Mobile Wireframes — layout mobile
- Framework CSS elegido (Tailwind, Bootstrap — breakpoints estándar)

**Dependencias (predecessors):**
- `3A.4.4` Desktop Wireframes *(obligatorio)*
- `3A.4.5` Mobile Wireframes *(obligatorio)*

**Habilita (successors):**
- `3A.5.10` Responsive Variants — mockups por breakpoint
- `3A.7.4` Spacing System — spacing responsive
- `3A.9.5` Redlines — medidas por breakpoint
- `4.4.15` Responsive Implementation — implementación frontend

**Audiencia:**
- **Frontend Developer** — breakpoints exactos a implementar
- **UI Designer** — diseñar para cada breakpoint
- **QA Engineer** — testing en cada breakpoint

**Secciones esperadas:**
1. Tabla de breakpoints (nombre, min-width, max-width, uso)
2. Reglas de adaptación por breakpoint (qué cambia: nav, columns, spacing, font-size)
3. Approach (mobile-first vs desktop-first)
4. Container max-widths por breakpoint
5. Elementos que se ocultan/muestran por breakpoint
6. Typography scale adjustments (si cambian por breakpoint)

**Criterio de completitud:**
- [ ] Al menos 3 breakpoints definidos (mobile, tablet, desktop)
- [ ] Reglas de adaptación documentadas por breakpoint
- [ ] Approach (mobile-first/desktop-first) definido
- [ ] Container widths definidos
- [ ] Consistente con framework CSS elegido

**Anti-patrones:**
- ❌ **Breakpoints arbitrarios:** 500px, 850px, 1100px — no estándar, difícil de recordar. Usar los del framework.
- ❌ **Solo 2 breakpoints:** Mobile y desktop sin tablet — experiencia rota en tablets.
- ❌ **Breakpoints sin reglas:** Definir los px pero no qué cambia — el developer adivina.
- ❌ **Responsive = esconder cosas:** Solo ocultar elementos en mobile en vez de reorganizar — la información sigue siendo necesaria.

**Template:** `phases/03-design/deliverables/responsive-breakpoints.md` *(pendiente)*

---

## Tabla resumen de ejecutores — Fase 3A.4 Wireframes

| Deliverable | Responsable | Ejecuta | Delegable VTT |
|-------------|-------------|---------|---------------|
| 3A.4.1 Wireframe Document | UX Designer | UX Designer | 🔶 Parcial — puede generar documento contenedor, no los wireframes |
| 3A.4.2 Low-Fi Wireframes | UX Designer | UX Designer | ❌ — trabajo visual exploratorio manual |
| 3A.4.3 Mid-Fi Wireframes | UX Designer | UX Designer | ❌ — trabajo visual en Figma |
| 3A.4.4 Desktop Wireframes | UX Designer | UX Designer | ❌ — trabajo visual en Figma |
| 3A.4.5 Mobile Wireframes | UX Designer | UX Designer | ❌ — trabajo visual en Figma |
| 3A.4.6 Tablet Wireframes | UX Designer | UX Designer | ❌ — trabajo visual en Figma |
| 3A.4.7 Wireframe Annotations | UX Designer | UX Designer | ✅ — puede generar contenido de anotaciones desde use cases |
| 3A.4.8 Wireframe Flows | UX Designer | UX Designer | ❌ — trabajo visual en Figma |
| 3A.4.9 Responsive Breakpoints | UX Designer | UX Designer / Frontend Dev | ✅ — puede documentar breakpoints y reglas de adaptación |

---

## Siguiente archivo

**Próximo:** `DICCIONARIO_FASE_03A_05_MOCKUPS.md` — 10 deliverables (3A.5.1 a 3A.5.10)
