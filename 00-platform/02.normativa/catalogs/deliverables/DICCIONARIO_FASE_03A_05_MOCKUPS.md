# DICCIONARIO DE DELIVERABLES — FASE 3A.5: MOCKUPS / UI DESIGN

**Versión:** 1.1  
**Fecha:** 2026-05-14  
**Fase:** 3A — Design UX/UI  
**Subfase:** 3A.5 — Mockups / UI Design  
**Total deliverables:** 10  
**Responsable de subfase:** UI Designer  
**Aprueba:** Design Lead

---

## Contexto de la subfase

Mockups son el diseño visual de alta fidelidad: la versión "final" de cada pantalla con colores, tipografía, iconos, imágenes, y todos los detalles visuales. Es lo que el usuario verá. Los mockups transforman los wireframes grises en interfaces visualmente pulidas y emocionalmente resonantes. Son la referencia pixel-perfect para el desarrollo frontend.

**Prerequisitos de subfase:**
- Wireframes aprobados (3A.4) — estructura validada
- Personas (3A.2) — contexto visual (profesional, casual, premium)
- Identidad visual / branding (si existe)

**Entrega de subfase:**
- Mockups de alta fidelidad de todas las pantallas en todas las plataformas, incluyendo todos los estados

---

### 3A.5.1 UI Mockups Complete

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.5 Mockups |
| **Responsable** | UI Designer |
| **Ejecuta** | UI Designer |
| **Aprueba** | Design Lead |
| **Formato** | Figma |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 5-10 días |
| **Frecuencia** | Una vez + iteraciones post-testing |

**Perfil de ejecución:** Requiere dominio avanzado de UI design: color theory, tipografía, espaciado, composición, y Figma (auto-layout, components, styles).  
En VTT: un agente NO puede crear mockups visuales. Puede generar especificaciones detalladas (qué componentes usar, qué colores, qué tipografía, qué spacing) como brief para el UI Designer. Necesita brief con: wireframes aprobados, brand guidelines, y design system (si existe).

**Qué es:** Conjunto completo de mockups de alta fidelidad de todas las pantallas del producto en Figma: versión desktop, mobile, y tablet (si aplica). Incluye todos los estados (default, hover, active, disabled, error, loading, empty). Es la representación visual final del producto tal como lo verá el usuario.

**Para qué sirve:** Son la fuente de verdad visual para el desarrollo frontend. Cada pixel, color, tipografía, y espaciado que el developer implementa sale de aquí. También son la herramienta de comunicación con stakeholders: "así va a verse el producto". Y son la base para el prototipo interactivo y las pruebas de usabilidad.

**Inputs requeridos:**
- `3A.4.3` Mid-Fi Wireframes — estructura aprobada
- `3A.4.7` Wireframe Annotations — comportamientos
- `3A.7.2` Color Palette — paleta de colores (si ya existe)
- `3A.7.3` Typography Scale — tipografía (si ya existe)
- Brand guidelines existentes (si aplica)

**Dependencias (predecessors):**
- `3A.4.3` Mid-Fi Wireframes *(obligatorio)* — estructura aprobada
- `3A.4.7` Wireframe Annotations *(obligatorio)* — comportamientos

**Habilita (successors):**
- `3A.5.2` a `3A.5.10` — versiones específicas derivadas
- `3A.6.1` Interactive Prototype — prototipo basado en mockups
- `3A.7.1` Design Tokens — tokens extraídos de mockups
- `3A.7.6` Component Library — componentes extraídos
- `3A.8.1` Usability Test Plan — mockups como objeto de test
- `3A.9.1` Handoff Document — mockups como entregable a dev

**Audiencia:**
- **Design Lead** — aprobación visual
- **Product Owner** — validación de que "así se ve"
- **Frontend Developer** — referencia pixel-perfect
- **QA Engineer** — referencia visual para testing
- **Marketing** — screenshots para materiales

**Secciones esperadas:**
1. Mockups organizados por flujo/módulo en Figma
2. Versiones desktop, mobile, tablet
3. Estados por pantalla (default, hover, active, disabled, error, loading, empty)
4. Componentes reutilizables con variants
5. Figma styles aplicados (colors, typography, effects)
6. Auto-layout en todos los componentes

**Criterio de completitud:**
- [ ] Todas las pantallas del sitemap mockeadas en alta fidelidad
- [ ] Versiones desktop y mobile para todas las pantallas principales
- [ ] Todos los estados diseñados (ver 3A.5.5 a 3A.5.8)
- [ ] Componentes reutilizables creados
- [ ] Figma styles/variables aplicados (no colores hardcoded)
- [ ] Auto-layout aplicado
- [ ] Aprobados por Design Lead

**Anti-patrones:**
- ❌ **Mockups sin wireframes:** Ir directo a alta fidelidad sin validar estructura — costoso de iterar.
- ❌ **Inconsistencia visual:** Cada pantalla tiene botones diferentes, tipografía diferente — sin design system.
- ❌ **Solo estado default:** Diseñar cómo se ve "cuando todo va bien" pero no error, empty, loading — el dev inventa.
- ❌ **Colores hardcoded:** Usar hex values directos en vez de Figma styles — imposible de cambiar globalmente.

**Template:** `phases/03-design/deliverables/ui-mockups.figma` *(pendiente)*

---

### 3A.5.2 Desktop Mockups

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.5 Mockups |
| **Responsable** | UI Designer |
| **Ejecuta** | UI Designer |
| **Aprueba** | Design Lead |
| **Formato** | Figma/PNG |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Incluido en 3A.5.1 |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere diseño visual para viewport desktop con aprovechamiento de espacio.  
En VTT: un agente NO puede crear mockups. Puede verificar que todas las pantallas tienen versión desktop.

**Qué es:** Versión desktop de todos los mockups: diseño visual completo para viewports de 1280px+, con navegación desktop (sidebar/topbar), layouts multi-columna, y aprovechamiento del espacio horizontal.

**Para qué sirve:** Es la versión "completa" del producto con todo el espacio disponible. Para apps B2B/SaaS, desktop es frecuentemente la experiencia primaria. Los desktop mockups son la referencia principal para el desarrollo frontend desktop.

**Inputs requeridos:**
- `3A.5.1` UI Mockups Complete — parte del conjunto
- `3A.4.4` Desktop Wireframes — estructura desktop aprobada

**Dependencias (predecessors):**
- `3A.4.4` Desktop Wireframes *(obligatorio)*

**Habilita (successors):**
- `3A.6.1` Interactive Prototype — prototipo desktop
- `3A.9.2` Specs Export — specs desktop

**Audiencia:**
- **Frontend Developer** — implementación desktop
- **QA Engineer** — referencia visual desktop

**Secciones esperadas:**
1. Todas las pantallas en viewport desktop (1280px / 1440px)
2. Content area con max-width
3. Navegación desktop completa
4. Layout patterns aplicados

**Criterio de completitud:**
- [ ] Todas las pantallas en versión desktop
- [ ] Navegación desktop incluida
- [ ] Content max-width consistente
- [ ] Calidad pixel-perfect

**Anti-patrones:**
- ❌ **Solo una resolución:** Diseñar para 1440px sin considerar 1280px ni 1920px.
- ❌ **Content sin max-width:** Texto que se estira al 100% del viewport — ilegible en widescreen.

**Template:** `phases/03-design/deliverables/desktop-mockups.figma` *(pendiente)*

---

### 3A.5.3 Mobile Mockups

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.5 Mockups |
| **Responsable** | UI Designer |
| **Ejecuta** | UI Designer |
| **Aprueba** | Design Lead |
| **Formato** | Figma/PNG |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 3-5 días |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere diseño mobile-native: thumb zones, touch targets, platform conventions.  
En VTT: un agente NO puede crear mockups. Puede verificar completitud y documentar diferencias vs desktop.

**Qué es:** Versión mobile de todos los mockups: diseño visual completo para viewports de 375px (iPhone) y 360px (Android), con navegación mobile, single-column layouts, y touch-friendly design.

**Para qué sirve:** Mobile es frecuentemente el 60%+ del tráfico consumer. Los mockups mobile aseguran una experiencia nativa y no un "desktop comprimido". Son la referencia para implementación responsive o app mobile.

**Inputs requeridos:**
- `3A.5.1` UI Mockups Complete — parte del conjunto
- `3A.4.5` Mobile Wireframes — estructura mobile aprobada

**Dependencias (predecessors):**
- `3A.4.5` Mobile Wireframes *(obligatorio)*

**Habilita (successors):**
- `3A.6.1` Interactive Prototype — prototipo mobile
- `3A.9.2` Specs Export — specs mobile

**Audiencia:**
- **Frontend Developer** — implementación responsive/mobile
- **QA Engineer** — testing mobile

**Secciones esperadas:**
1. Todas las pantallas principales en viewport mobile (375px)
2. Navegación mobile (bottom tabs/hamburger)
3. Touch targets (44px+)
4. Adaptaciones vs desktop documentadas

**Criterio de completitud:**
- [ ] Pantallas principales en versión mobile
- [ ] Navegación mobile implementada
- [ ] Touch targets ≥ 44px
- [ ] Diseño mobile-native (no desktop comprimido)

**Anti-patrones:**
- ❌ **Desktop shrink:** Comprimir el desktop sin rediseñar.
- ❌ **Touch targets diminutos:** Botones de 24px — frustración táctil.
- ❌ **Sin bottom safe area:** Ignorar la safe area del iPhone (home indicator).

**Template:** `phases/03-design/deliverables/mobile-mockups.figma` *(pendiente)*

---

### 3A.5.4 Tablet Mockups

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.5 Mockups |
| **Responsable** | UI Designer |
| **Ejecuta** | UI Designer |
| **Aprueba** | Design Lead |
| **Formato** | Figma/PNG |
| **Obligatorio** | ⚪ Opcional |
| **Esfuerzo típico** | 2-3 días |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere diseño para viewport intermedio con patterns tablet (split view, panels).  
En VTT: un agente NO puede crear mockups. Solo si el proyecto requiere soporte tablet explícito.

**Qué es:** Versión tablet de los mockups (768px-1024px), si el proyecto lo requiere. Diseño optimizado para el viewport intermedio con patterns como split view, master-detail, y panel lateral.

**Para qué sirve:** Si una porción significativa de usuarios usa tablet. Si no, el responsive entre mobile y desktop suele cubrir tablet adecuadamente sin mockups explícitos.

**Inputs requeridos:**
- `3A.4.6` Tablet Wireframes — estructura tablet aprobada
- Analytics de uso por device

**Dependencias (predecessors):**
- `3A.4.6` Tablet Wireframes *(obligatorio)*

**Habilita (successors):**
- `3A.9.2` Specs Export — specs tablet

**Audiencia:**
- **Frontend Developer** — breakpoints tablet
- **QA Engineer** — testing tablet

**Secciones esperadas:**
1. Pantallas principales en viewport tablet
2. Adaptaciones vs desktop y mobile
3. Landscape y portrait

**Criterio de completitud:**
- [ ] Pantallas principales en versión tablet
- [ ] Landscape y portrait considerados
- [ ] Justificación de necesidad tablet

**Anti-patrones:**
- ❌ **Tablet mockups sin justificación:** Esfuerzo sin data de uso tablet.

**Template:** `phases/03-design/deliverables/tablet-mockups.figma` *(pendiente)*

---

### 3A.5.5 Component States

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.5 Mockups |
| **Responsable** | UI Designer |
| **Ejecuta** | UI Designer |
| **Aprueba** | Design Lead |
| **Formato** | Figma |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 2-3 días |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere diseño de micro-estados: hover, active, focus, disabled, error, loading por componente interactivo.  
En VTT: un agente NO puede diseñar states visualmente. Puede listar qué states necesita cada componente como checklist.

**Qué es:** Diseño visual de todos los estados de cada componente interactivo: default, hover, active/pressed, focus (keyboard), disabled, error, loading, y selected. Para buttons, inputs, checkboxes, dropdowns, cards, links, tabs, y cualquier elemento con el que el usuario interactúa.

**Para qué sirve:** Una interfaz profesional responde visualmente a cada interacción del usuario. Sin states, los botones no cambian al hover, los inputs no muestran error, los disabled no se diferencian — la interfaz se siente "muerta". Los states dan feedback visual que confirma "tu acción fue recibida".

**Inputs requeridos:**
- `3A.5.1` UI Mockups Complete — componentes a diseñar states
- `3A.7.2` Color Palette — colores de estados
- Accessibility guidelines (focus visible, contrast)

**Dependencias (predecessors):**
- `3A.5.1` UI Mockups Complete *(obligatorio)*

**Habilita (successors):**
- `3A.7.6` Component Library — variants de states
- `3A.9.2` Specs Export — specs de states
- `4.4.1` Components — implementación de states CSS

**Audiencia:**
- **Frontend Developer** — implementación CSS de cada state
- **QA Engineer** — verificación de states

**Secciones esperadas:**
1. State matrix (tabla: componente × state = diseñado ✅/❌)
2. Diseño visual de cada state por componente
3. Transiciones entre states (duración, easing)
4. Focus state visible (WCAG: focus must be visible for keyboard nav)
5. Disabled state rules (opacity, pointer-events, cursor)

**Criterio de completitud:**
- [ ] Todos los componentes interactivos tienen: default, hover, active, focus, disabled
- [ ] Inputs tienen: default, focus, filled, error, disabled
- [ ] Focus state visible para keyboard navigation (accessibility)
- [ ] States diseñados como Figma variants
- [ ] Transiciones documentadas

**Anti-patrones:**
- ❌ **Sin hover state:** Botones que no cambian al pasar el cursor — se siente roto.
- ❌ **Sin focus state:** Usuarios de keyboard no pueden ver dónde están — accessibility fail.
- ❌ **Disabled = invisible:** Disabled tan sutil que parece activo — el usuario lo clickea y no pasa nada.
- ❌ **States inconsistentes:** Hover del botón es darker pero hover del link es underline — falta sistema.

**Template:** `phases/03-design/deliverables/component-states.figma` *(pendiente)*

---

### 3A.5.6 Empty States

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.5 Mockups |
| **Responsable** | UI Designer |
| **Ejecuta** | UI Designer |
| **Aprueba** | Design Lead |
| **Formato** | Figma |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere diseño de estados vacíos con ilustración, copy motivador, y CTA.  
En VTT: un agente puede redactar el copy de empty states y sugerir la estructura (ilustración + título + descripción + CTA). NO puede diseñar las ilustraciones. Necesita brief con: pantallas con empty states y acciones disponibles para el usuario.

**Qué es:** Diseño de lo que ve el usuario cuando una sección no tiene datos: lista vacía, dashboard sin proyectos, inbox sin mensajes, búsqueda sin resultados. Cada empty state tiene: ilustración, título explicativo, descripción breve, y CTA (Call to Action) para guiar al usuario a "llenar" la sección.

**Para qué sirve:** Empty states son la primera experiencia del usuario nuevo — es el primer screen que ve. Un empty state bien diseñado educa ("así se ve cuando tengas proyectos"), motiva ("crea tu primer proyecto"), y guía (CTA claro). Un empty state vacío o genérico desorienta y frustra.

**Inputs requeridos:**
- `3A.5.1` UI Mockups Complete — pantallas con posibles estados vacíos
- `3A.3.4` Content Inventory — contenido de empty states
- Copy del empty state (título, descripción, CTA)

**Dependencias (predecessors):**
- `3A.5.1` UI Mockups Complete *(obligatorio)*

**Habilita (successors):**
- `3A.7.8` Pattern Library — empty state como pattern
- `4.4.1` Components — empty state components

**Audiencia:**
- **Frontend Developer** — implementación
- **Content Writer** — copy de empty states
- **QA Engineer** — verificación de empty states

**Secciones esperadas:**
1. Inventario de pantallas con empty state (tabla: pantalla, contexto, CTA)
2. Diseño por empty state (ilustración + title + description + CTA button)
3. Copy definitivo por empty state
4. Variantes (first-time user vs returning user con datos borrados)

**Criterio de completitud:**
- [ ] Todas las pantallas con listas/datos tienen empty state diseñado
- [ ] Cada empty state tiene: ilustración, título, descripción, CTA
- [ ] Copy finalizado (no placeholder)
- [ ] CTA funcional (no "Haz algo" sino "Crear primer proyecto")

**Anti-patrones:**
- ❌ **"No hay datos":** Empty state que solo dice "No hay resultados" — no guía, no motiva.
- ❌ **Sin CTA:** Empty state informativo pero sin acción — ¿y ahora qué hago?
- ❌ **Empty states no diseñados:** El developer pone un texto gris centrado — se siente abandonado.

**Template:** `phases/03-design/deliverables/empty-states.figma` *(pendiente)*

---

### 3A.5.7 Error States

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.5 Mockups |
| **Responsable** | UI Designer |
| **Ejecuta** | UI Designer |
| **Aprueba** | Design Lead |
| **Formato** | Figma |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere diseño de estados de error claros, no-culpabilizantes, y accionables.  
En VTT: un agente puede redactar copy de error states y definir la estructura visual. NO puede diseñar en Figma. Necesita brief con: tipos de errores del sistema y acciones de recovery.

**Qué es:** Diseño de cómo se presentan los errores al usuario: errores de validación inline (campo por campo), errores de formulario (summary), errores de página (404, 500, 403), errores de red (offline), y errores de negocio ("no puedes hacer esto porque X"). Cada error tiene: indicador visual (color, icono), mensaje claro, y acción de recovery.

**Para qué sirve:** Los errores son inevitables. Un error bien diseñado dice: qué salió mal (en lenguaje humano), por qué (contexto), y qué hacer al respecto (recovery action). Un error mal diseñado dice "Error 500" — el usuario no sabe qué pasó ni qué hacer.

**Inputs requeridos:**
- `3A.5.1` UI Mockups Complete — pantallas con posibles errores
- `3B.4.5` Error Codes — tipos de errores del sistema
- `2.5.3` Validation Rules — validaciones que pueden fallar

**Dependencias (predecessors):**
- `3A.5.1` UI Mockups Complete *(obligatorio)*

**Habilita (successors):**
- `3A.7.8` Pattern Library — error patterns
- `4.4.1` Components — error components
- `3B.2.6` Error Handling Strategy — visual alignment

**Audiencia:**
- **Frontend Developer** — implementación de error UI
- **Content Writer** — copy de mensajes de error
- **QA Engineer** — verificación de error states

**Secciones esperadas:**
1. Error inline (validación de campo: posición, color, mensaje)
2. Error de formulario (toast/banner summary)
3. Error pages (404, 500, 403, offline)
4. Error de negocio (operación no permitida)
5. Copy de cada error (claro, no-técnico, accionable)
6. Recovery actions por tipo de error

**Criterio de completitud:**
- [ ] Error inline diseñado (campo + mensaje)
- [ ] Error pages diseñadas (404, 500, 403)
- [ ] Copy de errores finalizado (no-técnico, accionable)
- [ ] Recovery action por tipo de error
- [ ] Consistencia visual con el design system

**Anti-patrones:**
- ❌ **"An error occurred":** Mensaje genérico sin contexto ni acción — inútil.
- ❌ **Error culpabilizante:** "Has introducido un email incorrecto" → mejor "El formato de email no es válido. Ejemplo: tu@email.com".
- ❌ **Stack traces al usuario:** Información técnica que asusta y no ayuda.
- ❌ **Error sin recovery:** El usuario ve el error pero no sabe cómo arreglarlo.

**Template:** `phases/03-design/deliverables/error-states.figma` *(pendiente)*

---

### 3A.5.8 Loading States

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.5 Mockups |
| **Responsable** | UI Designer |
| **Ejecuta** | UI Designer |
| **Aprueba** | Design Lead |
| **Formato** | Figma |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5-1 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere diseño de estados de carga: skeletons, spinners, progress bars, y optimistic UI.  
En VTT: un agente puede especificar qué tipo de loading usar por pantalla. NO puede diseñar visualmente. Necesita brief con: pantallas con carga de datos y tipo de loading preferido.

**Qué es:** Diseño de lo que ve el usuario mientras el contenido carga: skeleton screens (placeholders animados que imitan el layout), spinners (indicador genérico de carga), progress bars (para operaciones con porcentaje conocido), y optimistic UI (mostrar el resultado antes de confirmar con el server).

**Para qué sirve:** Si una pantalla tarda 2 segundos sin loading state, el usuario piensa que está rota. El loading state comunica "estoy trabajando, espérame". Los skeleton screens son preferidos porque dan sensación de velocidad (perceived performance) al mostrar la estructura del contenido antes de que lleguen los datos.

**Inputs requeridos:**
- `3A.5.1` UI Mockups Complete — pantallas que cargan datos
- Decisión de loading pattern (skeleton, spinner, progress)

**Dependencias (predecessors):**
- `3A.5.1` UI Mockups Complete *(obligatorio)*

**Habilita (successors):**
- `3A.7.8` Pattern Library — loading patterns
- `4.4.1` Components — loading components

**Audiencia:**
- **Frontend Developer** — implementación de loading states
- **QA Engineer** — verificación de loading states

**Secciones esperadas:**
1. Loading patterns elegidos por contexto (skeleton, spinner, progress, optimistic)
2. Skeleton screens para pantallas principales
3. Spinner design y placement
4. Progress bar para operaciones largas
5. Reglas de uso (cuándo skeleton vs spinner vs progress)

**Criterio de completitud:**
- [ ] Loading pattern definido por tipo de contenido
- [ ] Skeleton screens diseñados para pantallas principales
- [ ] Spinner global diseñado
- [ ] Reglas de uso documentadas
- [ ] Consistencia visual

**Anti-patrones:**
- ❌ **Spinner everywhere:** Spinner genérico para todo — pierde la oportunidad de skeleton screens que dan mejor perceived performance.
- ❌ **Sin loading state:** Pantalla en blanco mientras carga — parece rota.
- ❌ **Loading bloqueante:** Spinner que bloquea toda la UI — solo bloquear lo que está cargando.

**Template:** `phases/03-design/deliverables/loading-states.figma` *(pendiente)*

---

### 3A.5.9 Dark Mode

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.5 Mockups |
| **Responsable** | UI Designer |
| **Ejecuta** | UI Designer |
| **Aprueba** | Design Lead |
| **Formato** | Figma |
| **Obligatorio** | ⚪ Opcional |
| **Esfuerzo típico** | 2-3 días |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere conocimiento de dark mode design: colores invertidos correctamente, contraste en dark backgrounds, y elevation con sombras/opacidad.  
En VTT: un agente puede generar la paleta dark mode derivada de la paleta light. NO puede diseñar las pantallas. Necesita brief con: color palette light y reglas de inversión.

**Qué es:** Versión dark mode del producto: paleta de colores invertida (backgrounds oscuros, texto claro), con ajustes de contraste, elevation (superficies con diferentes niveles de gris oscuro), e imágenes/iconos adaptados. No es simplemente "invertir colores" — requiere diseño deliberado para legibilidad y estética en fondos oscuros.

**Para qué sirve:** Dark mode reduce fatiga visual en ambientes oscuros, ahorra batería en pantallas OLED, y es preferido por un % significativo de usuarios. Si el producto se usa extensivamente (SaaS, productividad), dark mode es un diferenciador de UX.

**Inputs requeridos:**
- `3A.5.1` UI Mockups Complete — versión light a adaptar
- `3A.7.2` Color Palette — paleta dark derivada
- `3A.7.1` Design Tokens — tokens con tema dark

**Dependencias (predecessors):**
- `3A.5.1` UI Mockups Complete *(obligatorio)*
- `3A.7.2` Color Palette *(obligatorio)* — paleta dark definida

**Habilita (successors):**
- `3A.7.1` Design Tokens — tokens dark theme
- `3A.9.4` CSS Variables — dark mode CSS variables

**Audiencia:**
- **UI Designer** — referencia dark mode
- **Frontend Developer** — implementación dark theme

**Secciones esperadas:**
1. Paleta dark mode (surface colors por elevation level)
2. Mockups de pantallas principales en dark mode
3. Reglas de adaptación (qué cambia, qué no)
4. Imágenes/iconos en dark mode
5. Contraste verificado (WCAG)

**Criterio de completitud:**
- [ ] Paleta dark definida
- [ ] Pantallas principales en dark mode
- [ ] Contraste WCAG AA en dark mode
- [ ] Elevation levels con tonos de gris diferentes
- [ ] Toggle light/dark diseñado

**Anti-patrones:**
- ❌ **Invertir colores:** `background: black; color: white` — no funciona para elementos de color, sombras, ni imágenes.
- ❌ **Pure black background:** `#000000` es harsh — usar dark grays (`#121212`, `#1E1E1E`).
- ❌ **Sin verificar contraste:** Texto gris claro sobre gris oscuro — ilegible.

**Template:** `phases/03-design/deliverables/dark-mode.figma` *(pendiente)*

---

### 3A.5.10 Responsive Variants

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.5 Mockups |
| **Responsable** | UI Designer |
| **Ejecuta** | UI Designer |
| **Aprueba** | Design Lead |
| **Formato** | Figma |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Incluido en desktop + mobile |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere diseño responsive: cómo los mockups se adaptan entre breakpoints.  
En VTT: un agente NO puede crear las variantes responsive. Puede documentar las diferencias entre breakpoints como tabla.

**Qué es:** Vista consolidada de cómo cada pantalla principal se adapta entre breakpoints: qué cambia entre desktop → tablet → mobile (columnas, navegación, visibilidad de elementos, reordenamiento). Puede ser side-by-side comparisons en Figma o una tabla de adaptaciones.

**Para qué sirve:** Los mockups desktop y mobile muestran los extremos. Las responsive variants muestran la transición: "a 768px la sidebar se colapsa", "a 640px las 3 columnas pasan a 1", "a 480px el header se simplifica". Es la referencia para que el frontend implementa responsive correctamente.

**Inputs requeridos:**
- `3A.5.2` Desktop Mockups — extremo desktop
- `3A.5.3` Mobile Mockups — extremo mobile
- `3A.4.9` Responsive Breakpoints — breakpoints definidos

**Dependencias (predecessors):**
- `3A.5.2` Desktop Mockups *(obligatorio)*
- `3A.5.3` Mobile Mockups *(obligatorio)*
- `3A.4.9` Responsive Breakpoints *(obligatorio)*

**Habilita (successors):**
- `3A.9.1` Handoff Document — responsive behavior documentado
- `3A.9.5` Redlines — medidas por breakpoint
- `4.4.15` Responsive Implementation — implementación

**Audiencia:**
- **Frontend Developer** — implementación responsive
- **QA Engineer** — testing en cada breakpoint

**Secciones esperadas:**
1. Side-by-side: desktop | tablet | mobile por pantalla principal
2. Tabla de adaptaciones (breakpoint, qué cambia)
3. Notas de reordenamiento (qué elementos cambian de posición)
4. Elementos que se ocultan/muestran por breakpoint

**Criterio de completitud:**
- [ ] Pantallas principales con vista en al menos 2 breakpoints
- [ ] Diferencias entre breakpoints documentadas
- [ ] Consistente con 3A.4.9 Responsive Breakpoints

**Anti-patrones:**
- ❌ **Solo desktop y mobile sin intermedio:** El frontend adivina qué pasa a 768px.
- ❌ **Responsive = ocultar:** Solo esconder cosas en mobile en vez de reorganizar — pierde funcionalidad.

**Template:** `phases/03-design/deliverables/responsive-variants.figma` *(pendiente)*

---

## Tabla resumen de ejecutores — Fase 3A.5 Mockups

| Deliverable | Responsable | Ejecuta | Delegable VTT |
|-------------|-------------|---------|---------------|
| 3A.5.1 UI Mockups Complete | UI Designer | UI Designer | ❌ — trabajo visual en Figma |
| 3A.5.2 Desktop Mockups | UI Designer | UI Designer | ❌ — trabajo visual en Figma |
| 3A.5.3 Mobile Mockups | UI Designer | UI Designer | ❌ — trabajo visual en Figma |
| 3A.5.4 Tablet Mockups | UI Designer | UI Designer | ❌ — trabajo visual en Figma |
| 3A.5.5 Component States | UI Designer | UI Designer | ❌ — trabajo visual en Figma |
| 3A.5.6 Empty States | UI Designer | UI Designer | 🔶 Parcial — puede redactar copy, no puede diseñar ilustraciones |
| 3A.5.7 Error States | UI Designer | UI Designer | 🔶 Parcial — puede redactar copy de errores y definir estructura |
| 3A.5.8 Loading States | UI Designer | UI Designer | 🔶 Parcial — puede especificar loading pattern por pantalla |
| 3A.5.9 Dark Mode | UI Designer | UI Designer | 🔶 Parcial — puede generar paleta dark derivada |
| 3A.5.10 Responsive Variants | UI Designer | UI Designer | ❌ — trabajo visual en Figma |

---

## Siguiente archivo

**Próximo:** `DICCIONARIO_FASE_03A_06_PROTOTYPES.md` — 6 deliverables (3A.6.1 a 3A.6.6)
