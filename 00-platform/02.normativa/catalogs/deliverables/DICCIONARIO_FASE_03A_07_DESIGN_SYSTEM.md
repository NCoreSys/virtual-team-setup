# DICCIONARIO DE DELIVERABLES — FASE 3A.7: DESIGN SYSTEM

**Versión:** 1.0  
**Fecha:** 2026-05-14  
**Fase:** 3A — Design UX/UI  
**Subfase:** 3A.7 — Design System  
**Total deliverables:** 10  
**Responsable de subfase:** UI Designer  
**Aprueba:** Design Lead

---

## Contexto de la subfase

El Design System es el sistema nervioso visual del producto. Define los building blocks reutilizables (tokens, colores, tipografía, componentes) que garantizan consistencia visual y aceleran tanto el diseño como el desarrollo frontend. Sin un Design System, cada pantalla se convierte en una decisión ad-hoc, multiplicando inconsistencias y deuda de diseño.

**Prerequisitos de subfase:**
- Mockups aprobados (3A.5)
- Prototipo validado (3A.6)
- Identidad visual definida (si existe branding previo)

**Entrega de subfase:**
- Sistema de diseño documentado, versionado y consumible por desarrollo

---

### 3A.7.1 Design Tokens

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.7 Design System |
| **Responsable** | UI Designer |
| **Ejecuta** | UI Designer / Frontend Developer |
| **Aprueba** | Design Lead |
| **Formato** | JSON / Figma Variables |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 2-3 días |
| **Frecuencia** | Una vez + actualizaciones por sprint |

**Perfil de ejecución:** Requiere conocimiento de design tokens (naming conventions, estructura jerárquica, formatos de exportación). Debe entender la relación entre tokens semánticos y primitivos.  
En VTT: un agente puede generar el JSON de tokens a partir de la paleta de colores, tipografía y spacing ya definidos en mockups. Necesita brief con: paleta aprobada, escala tipográfica, sistema de spacing, y convención de naming (e.g., `color.primary.500`, `spacing.md`). NO puede decidir valores estéticos — esos vienen del UI Designer.

**Qué es:** Archivo estructurado (JSON, YAML o Figma Variables) que define las variables atómicas del sistema de diseño: colores, tamaños de fuente, espaciados, radios de borde, sombras, breakpoints y duraciones de animación. Son los "átomos" del design system — valores abstractos con nombres semánticos que se referencian en lugar de usar valores hardcoded.

**Para qué sirve:** Garantiza una fuente única de verdad (single source of truth) para todos los valores visuales. Permite cambiar un color primario en un solo lugar y que se propague a todo el producto. Habilita tematización (light/dark mode, white-labeling) y asegura que diseño y código usen exactamente los mismos valores.

**Inputs requeridos:**
- `3A.5.1` UI Mockups Complete — valores visuales extraídos de los diseños aprobados
- `3A.7.2` Color Palette — paleta de colores definida
- `3A.7.3` Typography Scale — escala tipográfica definida
- `3A.7.4` Spacing System — sistema de espaciado definido
- Decisión de formato de exportación (JSON, CSS custom properties, Tailwind config)

**Dependencias (predecessors):**
- `3A.5.1` UI Mockups Complete *(obligatorio)* — los mockups contienen los valores que se extraen
- `3A.7.2` Color Palette *(obligatorio)* — colores como tokens primitivos
- `3A.7.3` Typography Scale *(obligatorio)* — tipografía tokenizada
- `3A.7.4` Spacing System *(obligatorio)* — espaciado tokenizado

**Habilita (successors):**
- `3A.7.6` Component Library — los componentes consumen tokens
- `3A.9.4` CSS Variables — exportación directa de tokens a CSS
- `4.4.8` Styles — desarrollo frontend consume tokens
- `4.4.1` Components — componentes React referencian tokens

**Audiencia:**
- **UI Designer** — para mantener consistencia en nuevos diseños
- **Frontend Developer** — para implementar estilos consumiendo tokens en lugar de valores hardcoded
- **Design Lead** — para auditar consistencia del sistema visual
- **Tech Lead** — para validar que los tokens son implementables

**Secciones esperadas:**
1. Convención de naming (estructura jerárquica: primitivos → semánticos → componente)
2. Tokens de color (primitivos y semánticos)
3. Tokens de tipografía (font-family, font-size, font-weight, line-height)
4. Tokens de espaciado (scale: 4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px)
5. Tokens de bordes (radius, width)
6. Tokens de sombras (elevation levels)
7. Tokens de breakpoints (mobile, tablet, desktop, wide)
8. Tokens de animación (duration, easing)
9. Formato de exportación y consumo

**Criterio de completitud:**
- [ ] Todos los valores visuales de los mockups están tokenizados
- [ ] Naming convention documentada y consistente
- [ ] Tokens primitivos y semánticos diferenciados
- [ ] Archivo JSON/YAML válido y parseable
- [ ] Al menos un formato de exportación definido (CSS vars, Tailwind, etc.)
- [ ] Tokens cubren: colores, tipografía, espaciado, bordes, sombras, breakpoints

**Anti-patrones:**
- ❌ **Tokens sin semántica:** Usar nombres como `blue-500` en lugar de `color-primary` — acopla el token al valor visual en vez de al uso.
- ❌ **Tokens incompletos:** Tokenizar colores pero dejar tipografía y spacing hardcoded — inconsistencia parcial.
- ❌ **Token sprawl:** Crear 47 variantes de gris cuando se usan 5 — complejidad innecesaria que nadie mantiene.
- ❌ **Sin jerarquía:** Mezclar tokens primitivos con semánticos sin estructura — imposible hacer tematización.

**Template:** `phases/03-design/deliverables/design-tokens.json` *(pendiente)*

---

### 3A.7.2 Color Palette

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.7 Design System |
| **Responsable** | UI Designer |
| **Ejecuta** | UI Designer |
| **Aprueba** | Design Lead |
| **Formato** | Figma |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Una vez + refinamientos menores |

**Perfil de ejecución:** Requiere ojo de diseñador con conocimiento de teoría del color, accesibilidad (contraste WCAG AA/AAA), y experiencia en sistemas de color escalables (shade scales).  
En VTT: un agente puede validar contraste de accesibilidad de pares de colores y generar shade scales algorítmicamente (HSL manipulation). NO puede tomar decisiones estéticas de paleta — eso requiere juicio humano del UI Designer. Necesita brief con: colores de marca, colores primario/secundario elegidos, y requisito de nivel WCAG.

**Qué es:** Definición completa de todos los colores del producto, organizada en categorías: colores primarios, secundarios, neutros, semánticos (success, warning, error, info), y sus escalas de intensidad (50-900). Incluye los valores hexadecimales, RGB y HSL de cada color.

**Para qué sirve:** Establece el vocabulario cromático del producto. Evita que cada diseñador o developer invente tonos ad-hoc. Garantiza accesibilidad al pre-validar contrastes. Permite tematización coherente (dark mode).

**Inputs requeridos:**
- `3A.5.1` UI Mockups Complete — colores usados en diseños aprobados
- Brand guidelines existentes (si aplica)
- Requisitos de accesibilidad (WCAG AA mínimo)

**Dependencias (predecessors):**
- `3A.5.1` UI Mockups Complete *(obligatorio)* — colores validados visualmente
- `3A.7.9` Brand Guidelines *(recomendado)* — si existe branding previo, la paleta debe alinearse

**Habilita (successors):**
- `3A.7.1` Design Tokens — colores se convierten en tokens
- `3A.7.6` Component Library — componentes usan la paleta
- `3A.7.8` Pattern Library — patrones referencian colores semánticos
- `3A.5.9` Dark Mode — paleta dark derivada de la paleta light

**Audiencia:**
- **UI Designer** — referencia para todo diseño nuevo
- **Frontend Developer** — implementación exacta de colores
- **Design Lead** — aprobación de identidad visual
- **QA Engineer** — verificación de implementación vs diseño

**Secciones esperadas:**
1. Colores primarios (con shade scale 50-900)
2. Colores secundarios (con shade scale)
3. Colores neutros / grises (con shade scale)
4. Colores semánticos (success, warning, error, info)
5. Colores de superficie (background, card, overlay)
6. Colores de texto (primary, secondary, disabled, inverse)
7. Tabla de contraste WCAG (pares validados)
8. Guía de uso (cuándo usar cada color)
9. Paleta dark mode (si aplica)

**Criterio de completitud:**
- [ ] Colores primarios, secundarios y neutros definidos con shade scales
- [ ] Colores semánticos definidos (success, warning, error, info)
- [ ] Todos los pares texto/fondo cumplen WCAG AA (4.5:1 para texto normal)
- [ ] Valores en hex, RGB y HSL documentados
- [ ] Guía de uso por categoría
- [ ] Paleta exportada en Figma como estilos/variables

**Anti-patrones:**
- ❌ **Paleta sin contraste validado:** Colores bonitos que no pasan WCAG — accesibilidad es requisito, no nice-to-have.
- ❌ **Colores sin escala:** Solo definir `primary` sin shade scale (50-900) — imposible generar estados hover, active, disabled.
- ❌ **Semánticos iguales a primarios:** Usar el mismo azul para `primary` y para `info` — confunde el significado del color.
- ❌ **Demasiados colores:** 12 colores semánticos cuando 4 bastan — complejidad que nadie recuerda.

**Template:** `phases/03-design/deliverables/color-palette.md` *(pendiente)*

---

### 3A.7.3 Typography Scale

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.7 Design System |
| **Responsable** | UI Designer |
| **Ejecuta** | UI Designer |
| **Aprueba** | Design Lead |
| **Formato** | Figma |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere conocimiento de tipografía digital: escalas modulares, legibilidad en pantalla, line-height óptimos, font pairing, y licenciamiento de fuentes.  
En VTT: un agente puede generar una escala tipográfica matemática (e.g., ratio 1.25 Major Third) a partir de un tamaño base y generar los CSS correspondientes. NO puede elegir las fuentes ni juzgar legibilidad estética. Necesita brief con: fuentes elegidas (nombre, peso), tamaño base, ratio de escala, y plataforma target (web, mobile, ambas).

**Qué es:** Definición de la jerarquía tipográfica del producto: fuentes seleccionadas (font-family), escala de tamaños (font-size), pesos (font-weight), alturas de línea (line-height), y espaciado entre letras (letter-spacing). Organizada por roles semánticos: display, heading (h1-h6), body, caption, overline, button, etc.

**Para qué sirve:** Establece jerarquía visual clara para que el usuario distinga títulos de cuerpo de texto de captions sin esfuerzo cognitivo. Garantiza legibilidad en todas las plataformas. Evita la proliferación de tamaños arbitrarios.

**Inputs requeridos:**
- `3A.5.1` UI Mockups Complete — tipografía usada en diseños
- `3A.7.9` Brand Guidelines — fuentes de marca (si existen)
- Requisitos de plataforma (web, iOS, Android)
- Licencias de fuentes verificadas

**Dependencias (predecessors):**
- `3A.5.1` UI Mockups Complete *(obligatorio)* — tipografía validada visualmente
- `3A.7.9` Brand Guidelines *(recomendado)* — fuentes de marca

**Habilita (successors):**
- `3A.7.1` Design Tokens — tipografía tokenizada
- `3A.7.6` Component Library — componentes usan la escala
- `3A.7.7` Component Documentation — documentación referencia la escala
- `4.4.8` Styles — frontend implementa la escala

**Audiencia:**
- **UI Designer** — referencia obligatoria para todo texto nuevo
- **Frontend Developer** — implementación de clases tipográficas
- **Content Writer** — sabe qué niveles de heading usar
- **Design Lead** — validación de jerarquía visual

**Secciones esperadas:**
1. Fuentes seleccionadas (nombre, peso disponible, fallbacks, licencia)
2. Escala de tamaños (con ratio matemático si aplica)
3. Roles tipográficos (display, h1-h6, subtitle, body1, body2, caption, overline, button)
4. Line-height por nivel
5. Letter-spacing por nivel
6. Font-weight mapping (regular, medium, semibold, bold)
7. Reglas de uso (cuándo usar cada nivel)
8. Consideraciones responsive (ajustes mobile vs desktop)
9. Fuentes de fallback y loading strategy (FOUT/FOIT)

**Criterio de completitud:**
- [ ] Fuentes primaria y secundaria definidas con fallbacks
- [ ] Escala de al menos 8 niveles (display, h1-h6, body, caption)
- [ ] Line-height definido para cada nivel
- [ ] Reglas de uso documentadas
- [ ] Licencias de fuentes verificadas
- [ ] Consideraciones responsive documentadas
- [ ] Estilos creados en Figma

**Anti-patrones:**
- ❌ **Demasiadas fuentes:** 4+ font-families distintas — aumenta tiempo de carga y rompe cohesión visual.
- ❌ **Escala sin ratio:** Tamaños arbitrarios (13px, 17px, 21px) sin lógica matemática — difícil de mantener y recordar.
- ❌ **Line-height fijo:** Usar `line-height: 1.5` para todo — headings necesitan menos, body necesita más.
- ❌ **Sin fallbacks:** No definir font-stack de fallback — FOUT agresivo cuando la fuente no carga.

**Template:** `phases/03-design/deliverables/typography-scale.md` *(pendiente)*

---

### 3A.7.4 Spacing System

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.7 Design System |
| **Responsable** | UI Designer |
| **Ejecuta** | UI Designer |
| **Aprueba** | Design Lead |
| **Formato** | Figma |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere entendimiento de grids, espaciado consistente, y la relación entre densidad de información y usabilidad.  
En VTT: un agente puede generar una escala de spacing basada en un valor base (e.g., 4px o 8px) y documentarla. También puede auditar mockups para verificar que usan valores de la escala. NO puede decidir la densidad visual apropiada para el producto. Necesita brief con: unidad base de spacing, factor de escala, y nivel de densidad deseado (compact, comfortable, spacious).

**Qué es:** Sistema de espaciado basado en una unidad base (generalmente 4px u 8px) que define los valores permitidos para padding, margin, gap y layout spacing. Incluye una escala nombrada (xs, sm, md, lg, xl, 2xl, etc.) o numérica (space-1, space-2, etc.) que cubre desde micro-espaciado (4px) hasta macro-espaciado (64px+).

**Para qué sirve:** Elimina decisiones arbitrarias de spacing ("¿pongo 13px o 15px de padding?"). Crea ritmo visual consistente. Garantiza que los elementos mantienen proporciones armónicas en todo el producto. Facilita la implementación frontend (valores predecibles, no magic numbers).

**Inputs requeridos:**
- `3A.5.1` UI Mockups Complete — spacing patterns observados en diseños
- `3A.4.9` Responsive Breakpoints — cómo cambia el spacing en diferentes viewports
- Decisión de unidad base (4px vs 8px)

**Dependencias (predecessors):**
- `3A.5.1` UI Mockups Complete *(obligatorio)* — spacing validado visualmente
- `3A.4.9` Responsive Breakpoints *(recomendado)* — ajustes responsive del spacing

**Habilita (successors):**
- `3A.7.1` Design Tokens — spacing tokenizado
- `3A.7.6` Component Library — componentes usan spacing del sistema
- `4.4.8` Styles — frontend usa spacing scale (e.g., Tailwind spacing)

**Audiencia:**
- **UI Designer** — referencia para todo layout nuevo
- **Frontend Developer** — valores exactos de spacing a implementar
- **Design Lead** — validación de ritmo visual

**Secciones esperadas:**
1. Unidad base y ratio de escala
2. Escala completa de spacing (nombre, valor en px, valor en rem)
3. Reglas de uso por contexto (inline spacing, stack spacing, inset padding, section spacing)
4. Grid system (columnas, gutters, margins)
5. Consideraciones responsive (cómo cambia spacing por breakpoint)
6. Ejemplos visuales de aplicación

**Criterio de completitud:**
- [ ] Unidad base definida (4px u 8px)
- [ ] Escala de al menos 8 niveles documentada
- [ ] Nombres semánticos asignados (xs a 3xl o equivalente)
- [ ] Reglas de uso por contexto documentadas
- [ ] Grid system definido (columnas, gutters)
- [ ] Valores disponibles en Figma como variables/estilos

**Anti-patrones:**
- ❌ **Spacing arbitrario:** Valores como 7px, 13px, 22px que no pertenecen a ninguna escala — imposible de mantener consistente.
- ❌ **Escala demasiado granular:** 20 niveles de spacing cuando 8-10 cubren todo — análisis parálisis.
- ❌ **Sin reglas de contexto:** La escala existe pero nadie sabe cuándo usar `md` vs `lg` — la escala no se adopta.
- ❌ **Spacing fijo sin responsive:** Mismo spacing en mobile y desktop — demasiado espacio en mobile, poco en desktop.

**Template:** `phases/03-design/deliverables/spacing-system.md` *(pendiente)*

---

### 3A.7.5 Icon Library

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.7 Design System |
| **Responsable** | UI Designer |
| **Ejecuta** | UI Designer |
| **Aprueba** | Design Lead |
| **Formato** | Figma / SVG |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 2-3 días |
| **Frecuencia** | Una vez + adiciones incrementales |

**Perfil de ejecución:** Requiere habilidades de diseño de iconos o curación de icon sets existentes. Debe entender exportación SVG optimizada, tamaños de grid, y consistencia estilística.  
En VTT: un agente puede inventariar los iconos usados en los mockups, organizarlos por categoría, y optimizar SVGs (SVGO). También puede generar el archivo de exportación. NO puede diseñar iconos custom ni juzgar consistencia estilística. Necesita brief con: icon set base elegido (Lucide, Heroicons, Phosphor, custom), tamaño de grid (24x24, 20x20), stroke width, y lista de iconos necesarios por pantalla.

**Qué es:** Colección organizada y estandarizada de todos los iconos utilizados en el producto. Puede ser un icon set existente (Lucide, Heroicons, Material Icons) customizado, o una biblioteca custom. Incluye los archivos SVG optimizados, organizados por categoría, en tamaños estándar, con naming convention consistente.

**Para qué sirve:** Centraliza los iconos para evitar inconsistencias (un dev usa un ícono de Font Awesome, otro usa uno de Material). Garantiza consistencia visual (mismo stroke width, mismo grid, mismo estilo). Facilita la implementación frontend (un solo paquete de iconos).

**Inputs requeridos:**
- `3A.5.1` UI Mockups Complete — iconos usados en diseños
- Decisión de icon set base (existente vs custom)
- Grid size y stroke width definidos

**Dependencias (predecessors):**
- `3A.5.1` UI Mockups Complete *(obligatorio)* — inventario de iconos necesarios
- `3A.7.2` Color Palette *(recomendado)* — colores aplicados a iconos
- `3A.7.4` Spacing System *(recomendado)* — tamaños de icono alineados al spacing

**Habilita (successors):**
- `3A.7.6` Component Library — componentes que incluyen iconos
- `3A.7.10` Asset Library — iconos como parte de assets exportables
- `3A.9.3` Asset Export — SVGs listos para desarrollo
- `4.4.1` Components — componentes React consumen iconos

**Audiencia:**
- **UI Designer** — referencia para usar iconos existentes y solicitar nuevos
- **Frontend Developer** — importación e implementación de iconos
- **Design Lead** — validación de consistencia visual

**Secciones esperadas:**
1. Icon set base seleccionado y justificación
2. Grid y tamaños estándar (16px, 20px, 24px, 32px)
3. Stroke width y estilo (outline, filled, duotone)
4. Naming convention de iconos
5. Catálogo por categoría (navigation, action, status, content, social)
6. Guía de uso (cuándo usar ícono solo vs ícono + label)
7. Instrucciones de exportación SVG
8. Proceso para agregar nuevos iconos

**Criterio de completitud:**
- [ ] Todos los iconos de mockups incluidos en la biblioteca
- [ ] Estilo visual consistente (mismo stroke width, grid, estilo)
- [ ] SVGs optimizados (SVGO o equivalente)
- [ ] Naming convention aplicada a todos los iconos
- [ ] Catálogo organizado por categoría
- [ ] Exportables en al menos un formato (SVG components, sprite, font)
- [ ] Proceso de adición de nuevos iconos documentado

**Anti-patrones:**
- ❌ **Mix de icon sets:** Mezclar Heroicons con Font Awesome con Material — estilos incompatibles, inconsistencia visual.
- ❌ **SVGs sin optimizar:** Iconos con metadata innecesaria, paths redundantes — peso excesivo.
- ❌ **Sin naming convention:** `icon1.svg`, `boton-cerrar.svg`, `CloseBtn.svg` — imposible buscar y mantener.
- ❌ **Iconos sin tamaño estándar:** Iconos de 18px, 22px, 26px — no alineados al spacing system.

**Template:** `phases/03-design/deliverables/icon-library/` *(pendiente)*

---

### 3A.7.6 Component Library

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.7 Design System |
| **Responsable** | UI Designer |
| **Ejecuta** | UI Designer |
| **Aprueba** | Design Lead |
| **Formato** | Figma |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 5-8 días |
| **Frecuencia** | Una vez + evolución continua |

**Perfil de ejecución:** Requiere dominio avanzado de Figma (auto-layout, variants, component properties, slots) y entendimiento de anatomía de componentes UI. Es el deliverable más complejo del Design System.  
En VTT: un agente puede generar la documentación de la component library y crear inventarios de componentes a partir de mockups. NO puede construir los componentes en Figma — eso requiere trabajo manual del UI Designer. Puede generar el mapping de componentes de diseño a componentes de código. Necesita brief con: lista de componentes identificados, estados requeridos por componente, y prioridad de construcción.

**Qué es:** Biblioteca de componentes de UI reutilizables construidos en Figma con variants, auto-layout y component properties. Incluye todos los componentes identificados en los mockups: botones, inputs, cards, modals, dropdowns, tables, navigation, etc. Cada componente tiene todas sus variantes (size, state, type) como Figma variants.

**Para qué sirve:** Es la "fábrica" de piezas UI. Permite construir pantallas nuevas ensamblando componentes existentes en lugar de diseñar desde cero. Reduce tiempo de diseño de nuevas features en 60-80%. Garantiza consistencia pixel-perfect. Es la referencia autoritativa para el desarrollo frontend.

**Inputs requeridos:**
- `3A.5.1` UI Mockups Complete — componentes extraídos de diseños aprobados
- `3A.7.1` Design Tokens — tokens consumidos por componentes
- `3A.7.2` Color Palette — colores de componentes
- `3A.7.3` Typography Scale — tipografía de componentes
- `3A.7.4` Spacing System — padding/margin de componentes
- `3A.7.5` Icon Library — iconos usados en componentes
- `3A.5.5` Component States — estados hover, active, disabled, error, loading

**Dependencias (predecessors):**
- `3A.5.1` UI Mockups Complete *(obligatorio)*
- `3A.5.5` Component States *(obligatorio)* — define todos los estados
- `3A.7.1` Design Tokens *(obligatorio)* — componentes consumen tokens
- `3A.7.2` Color Palette *(obligatorio)*
- `3A.7.3` Typography Scale *(obligatorio)*
- `3A.7.4` Spacing System *(obligatorio)*
- `3A.7.5` Icon Library *(obligatorio)*

**Habilita (successors):**
- `3A.7.7` Component Documentation — documentación de cada componente
- `3A.7.8` Pattern Library — patrones compuestos por componentes
- `3A.9.1` Handoff Document — referencia de componentes para devs
- `3A.9.2` Specs Export — specs exportadas de componentes
- `4.4.1` Components — implementación React de los componentes
- `4.4.12` Storybook — stories basadas en variantes de Figma

**Audiencia:**
- **UI Designer** — uso diario para diseñar nuevas pantallas
- **Frontend Developer** — referencia autoritativa para implementación
- **Design Lead** — auditoría de calidad y consistencia
- **Product Manager** — entender qué building blocks existen
- **QA Engineer** — verificación visual de componentes implementados

**Secciones esperadas:**
1. Inventario de componentes (tabla: nombre, categoría, prioridad)
2. Categorías (primitives, forms, navigation, feedback, data display, layout, overlay)
3. Anatomía por componente (partes, slots, props)
4. Variantes por componente (size: sm/md/lg, variant: primary/secondary/ghost, state: default/hover/active/disabled/error/loading)
5. Auto-layout y responsive behavior
6. Figma component properties configuradas
7. Naming convention en Figma (e.g., `Button / Primary / Medium / Default`)

**Criterio de completitud:**
- [ ] Todos los componentes de mockups extraídos y componentizados
- [ ] Cada componente tiene todas sus variantes como Figma variants
- [ ] Auto-layout aplicado en todos los componentes
- [ ] Component properties configuradas (boolean, text, instance swap)
- [ ] Naming convention consistente en toda la biblioteca
- [ ] Componentes usan tokens (Figma variables) — no valores hardcoded
- [ ] Estados hover, active, disabled, error, loading para componentes interactivos

**Anti-patrones:**
- ❌ **Componentes sin variants:** Cada estado es un componente separado en vez de una variant — imposible de mantener.
- ❌ **Valores hardcoded:** Componentes con `#3B82F6` en vez de `color/primary/500` — cambiar el primario requiere editar cada componente.
- ❌ **Sin auto-layout:** Componentes con posicionamiento absoluto — se rompen al cambiar contenido.
- ❌ **Naming inconsistente:** `btn-primary`, `Button/Main`, `PrimaryBtn` — no se encuentra nada.
- ❌ **Overengineering:** 47 variantes de un botón cuando el producto usa 6 — esfuerzo desperdiciado.

**Template:** `phases/03-design/deliverables/component-library/` *(pendiente)*

---

### 3A.7.7 Component Documentation

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.7 Design System |
| **Responsable** | UI Designer |
| **Ejecuta** | UI Designer / Technical Writer |
| **Aprueba** | Design Lead |
| **Formato** | Documento (MD/Notion/Storybook) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 3-5 días |
| **Frecuencia** | Una vez + actualizaciones por componente nuevo |

**Perfil de ejecución:** Requiere capacidad de escritura técnica clara y conocimiento de los componentes. Debe ser comprensible tanto para diseñadores como para developers.  
En VTT: un agente puede generar la documentación de cada componente a partir de la component library de Figma: describir props, variantes, estados, uso correcto e incorrecto, y generar tablas de API. Es un deliverable altamente delegable. Necesita brief con: lista de componentes, acceso a la Figma library, y guía de tono/formato de la documentación.

**Qué es:** Documentación detallada de cada componente de la library. Para cada componente: descripción, cuándo usarlo, cuándo NO usarlo, props/variantes disponibles, ejemplos de uso, guidelines de accesibilidad, y relación con otros componentes. Puede vivir en un sitio de documentación (Storybook, Notion, docsite) o como documento markdown.

**Para qué sirve:** La component library sin documentación es una caja de herramientas sin manual. La documentación responde "¿cuándo uso un Dialog vs un Drawer?", "¿qué variant de botón uso para acciones destructivas?". Reduce preguntas repetitivas y decisiones inconsistentes.

**Inputs requeridos:**
- `3A.7.6` Component Library — componentes a documentar
- `3A.7.1` Design Tokens — tokens referenciados por componentes
- `3A.5.5` Component States — estados documentados
- Guidelines de accesibilidad (WCAG)

**Dependencias (predecessors):**
- `3A.7.6` Component Library *(obligatorio)* — componentes construidos antes de documentar
- `3A.7.1` Design Tokens *(recomendado)* — referencia de tokens en docs

**Habilita (successors):**
- `3A.9.1` Handoff Document — referencia de componentes para handoff
- `4.4.1` Components — devs consultan docs al implementar
- `4.4.12` Storybook — stories alineadas a la documentación de diseño

**Audiencia:**
- **Frontend Developer** — referencia primaria al implementar componentes
- **UI Designer** — guía de uso correcto de componentes existentes
- **QA Engineer** — criterio de aceptación visual por componente
- **New team members** — onboarding al design system

**Secciones esperadas (por componente):**
1. Nombre y descripción
2. Cuándo usar / Cuándo NO usar
3. Anatomía (partes del componente con labels)
4. Props / Variantes (tabla: prop, tipo, valores, default)
5. Estados (default, hover, active, focus, disabled, error, loading)
6. Ejemplos de uso (Do / Don't con capturas)
7. Guidelines de accesibilidad (ARIA roles, keyboard nav)
8. Componentes relacionados
9. Changelog (cambios por versión)

**Criterio de completitud:**
- [ ] Todos los componentes de la library documentados
- [ ] Cada doc tiene: descripción, cuándo usar, props, estados, Do/Don't
- [ ] Guidelines de accesibilidad incluidas por componente
- [ ] Ejemplos visuales (screenshots o embeds de Figma)
- [ ] Formato consistente en todas las docs de componentes

**Anti-patrones:**
- ❌ **Docs sin Do/Don't:** Solo describir el componente sin mostrar uso correcto vs incorrecto — se usa mal.
- ❌ **Docs desactualizadas:** Documentación de v1 cuando la library va en v3 — peor que no tener docs.
- ❌ **Docs solo para diseñadores:** Lenguaje de Figma que los devs no entienden — no es consumible cross-equipo.
- ❌ **Docs genéricas:** Copiar docs de Material UI en lugar de documentar el comportamiento específico del proyecto.

**Template:** `phases/03-design/deliverables/component-documentation.md` *(pendiente)*

---

### 3A.7.8 Pattern Library

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.7 Design System |
| **Responsable** | UI Designer |
| **Ejecuta** | UX Designer / UI Designer |
| **Aprueba** | Design Lead |
| **Formato** | Figma |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 3-4 días |
| **Frecuencia** | Una vez + adiciones por feature nueva |

**Perfil de ejecución:** Requiere pensamiento de diseño a nivel de patrón: no componentes individuales sino combinaciones recurrentes que resuelven problemas de UX comunes. Necesita experiencia en UX patterns (forms, search, data tables, empty states, onboarding).  
En VTT: un agente puede inventariar los patterns recurrentes de los mockups y documentar su estructura (qué componentes componen cada pattern). NO puede diseñar patterns nuevos ni decidir cuál es la mejor solución UX para un problema. Necesita brief con: lista de patterns identificados en mockups, contexto de uso de cada uno, y componentes involucrados.

**Qué es:** Colección de patrones de UI recurrentes: combinaciones de componentes que resuelven problemas de diseño comunes. Ejemplos: form patterns (inline validation, multi-step), data table patterns (filterable, sortable, paginated), search patterns (autocomplete, filtered), navigation patterns (breadcrumbs + tabs), empty state patterns, error page patterns, loading patterns.

**Para qué sirve:** Los componentes son letras; los patterns son palabras. Un pattern dice "así se construye un formulario de búsqueda con filtros" usando componentes del system. Evita reinventar soluciones a problemas ya resueltos. Acelera el diseño de features nuevas que siguen patterns existentes.

**Inputs requeridos:**
- `3A.5.1` UI Mockups Complete — patterns extraídos de diseños
- `3A.7.6` Component Library — componentes que componen los patterns
- `3A.3.3` Navigation Patterns — patterns de navegación ya definidos
- `2.6.1` User Flow Diagrams — flujos que los patterns implementan

**Dependencias (predecessors):**
- `3A.7.6` Component Library *(obligatorio)* — patterns se construyen con componentes
- `3A.5.1` UI Mockups Complete *(obligatorio)* — patterns extraídos de diseños
- `3A.3.3` Navigation Patterns *(recomendado)* — patterns de navegación

**Habilita (successors):**
- `3A.7.7` Component Documentation — docs referencian patterns
- `3A.9.1` Handoff Document — patterns como referencia para devs
- `4.4.2` Pages — pages implementan patterns

**Audiencia:**
- **UI Designer** — referencia para diseñar pantallas nuevas con patterns probados
- **UX Designer** — validar que los patterns resuelven los problemas de UX correctamente
- **Frontend Developer** — entender la estructura de secciones complejas
- **Product Manager** — saber qué patterns existen al definir features nuevas

**Secciones esperadas:**
1. Catálogo de patterns (tabla: nombre, categoría, componentes involucrados)
2. Form patterns (inline validation, multi-step, conditional fields)
3. Data display patterns (table, list, grid, detail view)
4. Search & filter patterns (search bar, faceted filters, active filters)
5. Navigation patterns (sidebar, tabs, breadcrumbs, pagination)
6. Feedback patterns (toast, alert, empty state, error page)
7. Layout patterns (dashboard, settings page, detail page)
8. Por cada pattern: descripción, cuándo usar, estructura, ejemplo visual

**Criterio de completitud:**
- [ ] Todos los patterns recurrentes de los mockups identificados y documentados
- [ ] Cada pattern muestra qué componentes usa
- [ ] Ejemplos visuales de cada pattern
- [ ] Guía de cuándo usar cada pattern
- [ ] Patterns construidos con componentes de la library (no ad-hoc)

**Anti-patrones:**
- ❌ **Confundir componentes con patterns:** Un botón es un componente; un "form con submit y cancel" es un pattern — niveles diferentes de abstracción.
- ❌ **Patterns sin contexto:** Documentar el pattern sin explicar cuándo usarlo vs alternativas — se elige arbitrariamente.
- ❌ **Patterns con componentes ad-hoc:** Un pattern que usa componentes que no están en la library — rompe el sistema.
- ❌ **Sin variantes:** Un solo pattern de formulario para formularios de 3 campos y de 30 — escalas distintas requieren patterns distintos.

**Template:** `phases/03-design/deliverables/pattern-library/` *(pendiente)*

---

### 3A.7.9 Brand Guidelines

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.7 Design System |
| **Responsable** | UI Designer |
| **Ejecuta** | UI Designer / Brand Designer |
| **Aprueba** | Design Lead |
| **Formato** | PDF |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 2-3 días |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere sensibilidad de branding: tono de voz visual, personalidad de marca, y cómo se traduce a decisiones de UI. Idealmente un Brand Designer, pero en equipos pequeños el UI Designer asume el rol.  
En VTT: un agente puede compilar y estructurar las Brand Guidelines a partir de inputs existentes (logo files, paleta, tipografía, tono de voz definido). Puede generar el documento PDF estructurado. NO puede tomar decisiones de identidad de marca — esas son decisiones creativas humanas. Necesita brief con: logo y variantes, paleta de marca, fuentes, tono de voz, y valores de marca definidos.

**Qué es:** Documento que define la identidad visual de la marca del producto: uso del logo (variantes, clear space, tamaño mínimo, usos incorrectos), paleta de marca, tipografía de marca, tono de voz, personalidad visual, fotografía/ilustración style, y reglas de aplicación. Es la "constitución" visual del producto.

**Para qué sirve:** Garantiza que todo output visual (UI, marketing, docs, presentaciones) sea coherente con la identidad de marca. Evita que cada persona interprete la marca a su manera. Es especialmente importante cuando hay múltiples diseñadores o agencias externas.

**Inputs requeridos:**
- Logo y variantes (si existen)
- `3A.7.2` Color Palette — paleta de marca
- `3A.7.3` Typography Scale — fuentes de marca
- Decisiones de brand voice/personality (del PO o marketing)

**Dependencias (predecessors):**
- `0.4.2` UVP Statement *(recomendado)* — propuesta de valor informa personalidad de marca
- `0.4.4` Target Customer Profile *(recomendado)* — audiencia informa tono visual
- `3A.7.2` Color Palette *(obligatorio)* — colores de la marca
- `3A.7.3` Typography Scale *(obligatorio)* — tipografía de la marca

**Habilita (successors):**
- `3A.7.1` Design Tokens — tokens alineados a brand
- `3A.7.6` Component Library — componentes siguen brand guidelines
- `3A.7.10` Asset Library — assets de marca exportables

**Audiencia:**
- **UI Designer** — referencia para todo diseño visual
- **Marketing** — aplicación de marca en materiales
- **Product Owner** — validación de identidad de marca
- **Agencias externas** — guía para producir materiales alineados

**Secciones esperadas:**
1. Logo (variantes, clear space, tamaño mínimo, usos incorrectos)
2. Paleta de marca (primarios, secundarios, aplicación)
3. Tipografía de marca (fuentes, jerarquía, reglas)
4. Tono de voz (personalidad, do/don't de copy)
5. Iconografía y estilo de ilustración
6. Fotografía / imagery style
7. Layouts y composición
8. Aplicaciones (tarjetas, presentaciones, emails)
9. Do / Don't visuales con ejemplos

**Criterio de completitud:**
- [ ] Logo documentado con variantes, clear space y usos incorrectos
- [ ] Paleta de marca con reglas de aplicación
- [ ] Tipografía de marca con jerarquía
- [ ] Tono de voz definido con ejemplos
- [ ] Al menos 5 ejemplos de Do / Don't
- [ ] Formato PDF exportable y compartible

**Anti-patrones:**
- ❌ **Brand guidelines sin Do/Don't:** Solo mostrar lo correcto sin advertir lo incorrecto — la gente comete los mismos errores.
- ❌ **Guidelines demasiado vagas:** "Usamos azul" sin especificar qué azul, cuándo, y cómo — no guía nada.
- ❌ **Desconectadas del Design System:** Brand guidelines que definen una paleta diferente a los design tokens — dos fuentes de verdad conflictivas.
- ❌ **Sin reglas de logo:** El logo se estira, se pone sobre fondos inadecuados, se modifica — sin restricciones documentadas.

**Template:** `phases/03-design/deliverables/brand-guidelines.pdf` *(pendiente)*

---

### 3A.7.10 Asset Library

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.7 Design System |
| **Responsable** | UI Designer |
| **Ejecuta** | UI Designer |
| **Aprueba** | Design Lead |
| **Formato** | Figma / Folder |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Una vez + adiciones continuas |

**Perfil de ejecución:** Requiere organización meticulosa y conocimiento de formatos de exportación (SVG, PNG 1x/2x/3x, WebP, PDF). Trabajo operativo más que creativo.  
En VTT: un agente puede organizar assets existentes, optimizar imágenes (compresión, resize), generar las exportaciones en múltiples formatos y resoluciones, y crear el catálogo/índice. Es un deliverable altamente delegable. Necesita brief con: lista de assets requeridos, formatos de exportación por tipo, y estructura de carpetas.

**Qué es:** Repositorio centralizado y organizado de todos los assets visuales del producto: logos (en todos los formatos y variantes), iconos exportados, ilustraciones, fotografías de producto, imágenes de placeholder, favicons, app icons, social media assets, y cualquier otro recurso gráfico necesario para desarrollo y marketing.

**Para qué sirve:** Evita que los developers busquen assets en chats, emails o carpetas personales. Garantiza que se usen las versiones correctas y optimizadas. Centraliza todo el material visual para acceso rápido por cualquier miembro del equipo.

**Inputs requeridos:**
- `3A.7.5` Icon Library — iconos exportados
- `3A.7.9` Brand Guidelines — logo y variantes
- `3A.5.1` UI Mockups Complete — assets usados en diseños
- Fotografías / ilustraciones del producto

**Dependencias (predecessors):**
- `3A.7.5` Icon Library *(obligatorio)* — iconos como assets
- `3A.7.9` Brand Guidelines *(obligatorio)* — logo y assets de marca
- `3A.5.1` UI Mockups Complete *(obligatorio)* — assets usados en diseños

**Habilita (successors):**
- `3A.9.3` Asset Export — assets listos para handoff a desarrollo
- `4.4.1` Components — frontend consume assets
- `4.4.8` Styles — imágenes y recursos referenciados

**Audiencia:**
- **Frontend Developer** — descarga de assets para implementación
- **UI Designer** — referencia de assets disponibles
- **Marketing** — acceso a assets de marca
- **DevOps** — favicons, app icons para deploy

**Secciones esperadas:**
1. Estructura de carpetas del asset library
2. Catálogo de assets (tabla: nombre, categoría, formatos disponibles, tamaño)
3. Logo / variantes (SVG, PNG 1x/2x/3x, dark/light)
4. Favicons y app icons (todos los tamaños requeridos)
5. Iconos exportados (SVG, PNG si necesario)
6. Ilustraciones / imágenes de producto
7. Placeholders (avatar default, image placeholder, empty state illustrations)
8. Social media assets (OG images, share cards)
9. Guía de formatos (cuándo usar SVG vs PNG vs WebP)
10. Naming convention de archivos

**Criterio de completitud:**
- [ ] Todos los assets de mockups exportados y organizados
- [ ] Logo en SVG + PNG (1x, 2x, 3x) en variantes light/dark
- [ ] Favicons generados (16x16, 32x32, apple-touch-icon, etc.)
- [ ] Iconos exportados en SVG optimizado
- [ ] Naming convention consistente
- [ ] Estructura de carpetas documentada
- [ ] Todos los assets optimizados (compresión sin pérdida visible)

**Anti-patrones:**
- ❌ **Assets sin optimizar:** PNGs de 2MB que deberían ser SVGs de 3KB — performance kill.
- ❌ **Sin naming convention:** `logo_final_v3_FINAL(2).png` — caos.
- ❌ **Assets dispersos:** Algunos en Figma, otros en Google Drive, otros en Slack — nadie encuentra nada.
- ❌ **Sin versiones múltiples:** Solo el logo en PNG sin SVG ni variantes de resolución — insuficiente para todas las plataformas.
- ❌ **Sin placeholders:** No tener avatar default, empty state illustrations — los devs usan placeholders feos temporales que se vuelven permanentes.

**Template:** `phases/03-design/deliverables/asset-library/` *(pendiente)*

---

## Tabla resumen de ejecutores — Fase 3A.7 Design System

| Deliverable | Responsable | Ejecuta | Delegable VTT |
|-------------|-------------|---------|---------------|
| 3A.7.1 Design Tokens | UI Designer | UI Designer / Frontend Developer | 🔶 Parcial — puede generar JSON de tokens a partir de valores dados, no puede decidir valores |
| 3A.7.2 Color Palette | UI Designer | UI Designer | ❌ — decisiones estéticas y de accesibilidad requieren juicio humano |
| 3A.7.3 Typography Scale | UI Designer | UI Designer | 🔶 Parcial — puede generar escala matemática, no puede elegir fuentes |
| 3A.7.4 Spacing System | UI Designer | UI Designer | 🔶 Parcial — puede generar escala y documentar, no puede decidir densidad visual |
| 3A.7.5 Icon Library | UI Designer | UI Designer | 🔶 Parcial — puede inventariar, organizar y optimizar SVGs, no puede diseñar iconos |
| 3A.7.6 Component Library | UI Designer | UI Designer | ❌ — requiere trabajo manual en Figma con variants y auto-layout |
| 3A.7.7 Component Documentation | UI Designer | UI Designer / Technical Writer | ✅ — altamente delegable, puede generar docs completas a partir de la library |
| 3A.7.8 Pattern Library | UI Designer | UX Designer / UI Designer | 🔶 Parcial — puede inventariar y documentar patterns, no puede diseñarlos |
| 3A.7.9 Brand Guidelines | UI Designer | UI Designer / Brand Designer | 🔶 Parcial — puede compilar y estructurar el PDF, no puede tomar decisiones de marca |
| 3A.7.10 Asset Library | UI Designer | UI Designer | ✅ — altamente delegable: organizar, optimizar, catalogar y exportar assets |

---

## Siguiente archivo

**Próximo:** `DICCIONARIO_FASE_03A_08_USABILITY_TESTING.md` — 7 deliverables (3A.8.1 a 3A.8.7)
