# 🎨 GUÍA DE DESIGN TOKENS — Checklist de Definición

> **Versión:** 1.0  
> **Tipo:** Guía de referencia (no es template de spec)  
> **Propósito:** Checklist de qué tokens debe definir un Design System para estandarizar el proceso

---

## 📋 ¿Qué es esta guía?

Esta guía **NO es un template para llenar**, sino un **checklist de referencia** que define qué elementos debe contener un Design System completo.

**Uso:**
- Verificar que el Design System del proyecto esté completo
- Identificar gaps en la definición de tokens
- Estandarizar la estructura de tokens entre proyectos

---

## 1) Colores (Color Tokens)

### 1.1 Colores primitivos [OBL]

| Categoría | Tokens a definir | Ejemplo |
|-----------|------------------|---------|
| **Escala de grises** | `gray-50` a `gray-900` | 10 valores |
| **Color primario** | `primary-50` a `primary-900` | 10 valores |
| **Color secundario** | `secondary-50` a `secondary-900` | 10 valores |
| **Colores de acento** | `accent-1`, `accent-2`, etc. | Según marca |

### 1.2 Colores semánticos [OBL]

| Token | Uso | Debe incluir |
|-------|-----|--------------|
| `color-success` | Estados exitosos | Default, hover, active, bg, text |
| `color-warning` | Advertencias | Default, hover, active, bg, text |
| `color-error` | Errores | Default, hover, active, bg, text |
| `color-info` | Información | Default, hover, active, bg, text |

### 1.3 Colores de superficie [OBL]

| Token | Uso |
|-------|-----|
| `color-bg-primary` | Fondo principal |
| `color-bg-secondary` | Fondo secundario |
| `color-bg-tertiary` | Fondo terciario |
| `color-bg-inverse` | Fondo invertido (dark) |
| `color-bg-overlay` | Overlay/backdrop |
| `color-bg-disabled` | Estados disabled |

### 1.4 Colores de texto [OBL]

| Token | Uso |
|-------|-----|
| `color-text-primary` | Texto principal |
| `color-text-secondary` | Texto secundario |
| `color-text-tertiary` | Texto terciario/placeholder |
| `color-text-inverse` | Texto sobre fondos oscuros |
| `color-text-disabled` | Texto disabled |
| `color-text-link` | Links |
| `color-text-link-hover` | Links hover |

### 1.5 Colores de borde [OBL]

| Token | Uso |
|-------|-----|
| `color-border-default` | Bordes normales |
| `color-border-subtle` | Bordes sutiles |
| `color-border-strong` | Bordes prominentes |
| `color-border-focus` | Focus rings |
| `color-border-error` | Bordes de error |

### 1.6 Dark mode [COND]

| Requisito | Descripción |
|-----------|-------------|
| Tokens duplicados | Cada token debe tener versión light y dark |
| Naming convention | `--color-bg-primary` funciona en ambos modos |
| CSS variables | Usar custom properties para swap |

---

## 2) Tipografía (Typography Tokens)

### 2.1 Font families [OBL]

| Token | Uso | Fallbacks |
|-------|-----|-----------|
| `font-family-sans` | UI, body text | System fonts |
| `font-family-serif` | Editorial (si aplica) | Georgia, serif |
| `font-family-mono` | Código | Monospace |

### 2.2 Font sizes [OBL]

| Token | Valor típico | Uso |
|-------|--------------|-----|
| `font-size-xs` | 12px | Labels pequeños |
| `font-size-sm` | 14px | Texto secundario |
| `font-size-base` | 16px | Body text |
| `font-size-lg` | 18px | Body grande |
| `font-size-xl` | 20px | Subtítulos |
| `font-size-2xl` | 24px | H4 |
| `font-size-3xl` | 30px | H3 |
| `font-size-4xl` | 36px | H2 |
| `font-size-5xl` | 48px | H1 |
| `font-size-6xl` | 60px | Display |

### 2.3 Font weights [OBL]

| Token | Valor | Uso |
|-------|-------|-----|
| `font-weight-normal` | 400 | Body text |
| `font-weight-medium` | 500 | Emphasis |
| `font-weight-semibold` | 600 | Headings |
| `font-weight-bold` | 700 | Strong emphasis |

### 2.4 Line heights [OBL]

| Token | Valor | Uso |
|-------|-------|-----|
| `line-height-none` | 1 | Single line |
| `line-height-tight` | 1.25 | Headings |
| `line-height-normal` | 1.5 | Body text |
| `line-height-relaxed` | 1.75 | Long form |

### 2.5 Letter spacing [OBL]

| Token | Valor | Uso |
|-------|-------|-----|
| `letter-spacing-tighter` | -0.05em | Display text |
| `letter-spacing-tight` | -0.025em | Headings |
| `letter-spacing-normal` | 0 | Body |
| `letter-spacing-wide` | 0.025em | Uppercase |
| `letter-spacing-wider` | 0.05em | Labels |

### 2.6 Text styles compuestos [OBL]

| Token | Composición |
|-------|-------------|
| `text-style-h1` | size-5xl, weight-bold, line-tight |
| `text-style-h2` | size-4xl, weight-semibold, line-tight |
| `text-style-h3` | size-3xl, weight-semibold, line-tight |
| `text-style-h4` | size-2xl, weight-semibold, line-normal |
| `text-style-body` | size-base, weight-normal, line-normal |
| `text-style-body-sm` | size-sm, weight-normal, line-normal |
| `text-style-caption` | size-xs, weight-normal, line-normal |
| `text-style-button` | size-sm, weight-medium, line-none |
| `text-style-label` | size-xs, weight-medium, line-none, spacing-wide |

---

## 3) Espaciado (Spacing Tokens)

### 3.1 Escala de spacing [OBL]

| Token | Valor | Uso típico |
|-------|-------|------------|
| `space-0` | 0 | Reset |
| `space-1` | 4px | Mínimo |
| `space-2` | 8px | Tight |
| `space-3` | 12px | Compact |
| `space-4` | 16px | Default |
| `space-5` | 20px | Comfortable |
| `space-6` | 24px | Relaxed |
| `space-8` | 32px | Sections |
| `space-10` | 40px | Large gaps |
| `space-12` | 48px | Section dividers |
| `space-16` | 64px | Page sections |
| `space-20` | 80px | Major sections |
| `space-24` | 96px | Hero spacing |

### 3.2 Spacing semánticos [OPC]

| Token | Uso |
|-------|-----|
| `space-component-gap` | Gap entre elementos de componente |
| `space-section-gap` | Gap entre secciones |
| `space-page-margin` | Márgenes de página |
| `space-card-padding` | Padding de cards |
| `space-input-padding-x` | Padding horizontal de inputs |
| `space-input-padding-y` | Padding vertical de inputs |
| `space-button-padding-x` | Padding horizontal de botones |
| `space-button-padding-y` | Padding vertical de botones |

---

## 4) Tamaños (Size Tokens)

### 4.1 Tamaños de componentes [OBL]

| Token | Uso | Valores típicos |
|-------|-----|-----------------|
| `size-button-sm` | Botón pequeño | height: 32px |
| `size-button-md` | Botón mediano | height: 40px |
| `size-button-lg` | Botón grande | height: 48px |
| `size-input-sm` | Input pequeño | height: 32px |
| `size-input-md` | Input mediano | height: 40px |
| `size-input-lg` | Input grande | height: 48px |
| `size-avatar-sm` | Avatar pequeño | 24px |
| `size-avatar-md` | Avatar mediano | 40px |
| `size-avatar-lg` | Avatar grande | 64px |
| `size-icon-sm` | Icono pequeño | 16px |
| `size-icon-md` | Icono mediano | 24px |
| `size-icon-lg` | Icono grande | 32px |

### 4.2 Tamaños de layout [OBL]

| Token | Uso | Valor típico |
|-------|-----|--------------|
| `size-sidebar` | Ancho de sidebar | 280px |
| `size-header` | Altura de header | 64px |
| `size-footer` | Altura de footer | 80px |
| `size-modal-sm` | Modal pequeño | 400px |
| `size-modal-md` | Modal mediano | 600px |
| `size-modal-lg` | Modal grande | 800px |
| `size-container-sm` | Container pequeño | 640px |
| `size-container-md` | Container mediano | 768px |
| `size-container-lg` | Container grande | 1024px |
| `size-container-xl` | Container extra grande | 1280px |

---

## 5) Bordes (Border Tokens)

### 5.1 Border radius [OBL]

| Token | Valor | Uso |
|-------|-------|-----|
| `radius-none` | 0 | Sin radius |
| `radius-sm` | 4px | Subtle |
| `radius-md` | 8px | Default |
| `radius-lg` | 12px | Cards |
| `radius-xl` | 16px | Modals |
| `radius-2xl` | 24px | Large cards |
| `radius-full` | 9999px | Pills, avatares |

### 5.2 Border width [OBL]

| Token | Valor | Uso |
|-------|-------|-----|
| `border-width-0` | 0 | Sin borde |
| `border-width-1` | 1px | Default |
| `border-width-2` | 2px | Emphasis |
| `border-width-4` | 4px | Strong |

---

## 6) Sombras (Shadow Tokens)

### 6.1 Elevation shadows [OBL]

| Token | Uso | Valor típico |
|-------|-----|--------------|
| `shadow-none` | Sin sombra | none |
| `shadow-sm` | Sutil | 0 1px 2px rgba(0,0,0,0.05) |
| `shadow-md` | Cards | 0 4px 6px rgba(0,0,0,0.1) |
| `shadow-lg` | Dropdowns | 0 10px 15px rgba(0,0,0,0.1) |
| `shadow-xl` | Modals | 0 20px 25px rgba(0,0,0,0.15) |
| `shadow-2xl` | Popovers | 0 25px 50px rgba(0,0,0,0.25) |
| `shadow-inner` | Inset | inset 0 2px 4px rgba(0,0,0,0.05) |

### 6.2 Focus shadows [OBL]

| Token | Uso |
|-------|-----|
| `shadow-focus` | Focus ring default |
| `shadow-focus-error` | Focus ring en error |

---

## 7) Transiciones y animaciones (Motion Tokens)

### 7.1 Durations [OBL]

| Token | Valor | Uso |
|-------|-------|-----|
| `duration-instant` | 0ms | Ninguna |
| `duration-fast` | 100ms | Micro-interactions |
| `duration-normal` | 200ms | Default |
| `duration-slow` | 300ms | Modals, drawers |
| `duration-slower` | 500ms | Page transitions |

### 7.2 Easing [OBL]

| Token | Valor | Uso |
|-------|-------|-----|
| `ease-linear` | linear | Progress bars |
| `ease-in` | cubic-bezier(0.4, 0, 1, 1) | Exit |
| `ease-out` | cubic-bezier(0, 0, 0.2, 1) | Enter |
| `ease-in-out` | cubic-bezier(0.4, 0, 0.2, 1) | Default |

### 7.3 Transitions compuestas [OBL]

| Token | Composición |
|-------|-------------|
| `transition-colors` | color duration-normal ease-in-out |
| `transition-opacity` | opacity duration-normal ease-in-out |
| `transition-transform` | transform duration-normal ease-out |
| `transition-all` | all duration-normal ease-in-out |

---

## 8) Z-Index (Layer Tokens)

### 8.1 Z-index scale [OBL]

| Token | Valor | Uso |
|-------|-------|-----|
| `z-base` | 0 | Contenido normal |
| `z-dropdown` | 1000 | Dropdowns |
| `z-sticky` | 1100 | Sticky headers |
| `z-fixed` | 1200 | Fixed elements |
| `z-drawer` | 1300 | Drawers |
| `z-modal` | 1400 | Modals |
| `z-popover` | 1500 | Popovers |
| `z-tooltip` | 1600 | Tooltips |
| `z-toast` | 1700 | Toasts |

---

## 9) Breakpoints (Responsive Tokens)

### 9.1 Breakpoint scale [OBL]

| Token | Valor | Uso |
|-------|-------|-----|
| `breakpoint-sm` | 640px | Mobile landscape |
| `breakpoint-md` | 768px | Tablet |
| `breakpoint-lg` | 1024px | Desktop |
| `breakpoint-xl` | 1280px | Large desktop |
| `breakpoint-2xl` | 1536px | Extra large |

---

## 10) Otros tokens [OPC]

### 10.1 Opacity [OPC]

| Token | Valor | Uso |
|-------|-------|-----|
| `opacity-0` | 0 | Invisible |
| `opacity-25` | 0.25 | Muy sutil |
| `opacity-50` | 0.5 | Medio |
| `opacity-75` | 0.75 | Visible |
| `opacity-100` | 1 | Full |

### 10.2 Aspect ratios [OPC]

| Token | Valor | Uso |
|-------|-------|-----|
| `aspect-square` | 1/1 | Avatares |
| `aspect-video` | 16/9 | Videos |
| `aspect-photo` | 4/3 | Fotos |

---

## ✅ Checklist de completitud

### Tokens mínimos requeridos

- [ ] **Colores**
  - [ ] Primitivos (escala de cada color)
  - [ ] Semánticos (success, error, warning, info)
  - [ ] Superficie (backgrounds)
  - [ ] Texto
  - [ ] Bordes

- [ ] **Tipografía**
  - [ ] Font families
  - [ ] Font sizes (escala completa)
  - [ ] Font weights
  - [ ] Line heights
  - [ ] Text styles compuestos

- [ ] **Espaciado**
  - [ ] Escala de spacing (4px base)
  - [ ] Espaciado semántico (opcional pero recomendado)

- [ ] **Tamaños**
  - [ ] Componentes (botones, inputs, avatares, iconos)
  - [ ] Layout (containers, modals, sidebar)

- [ ] **Bordes**
  - [ ] Border radius
  - [ ] Border width

- [ ] **Sombras**
  - [ ] Elevation scale
  - [ ] Focus shadows

- [ ] **Motion**
  - [ ] Durations
  - [ ] Easing functions
  - [ ] Transitions compuestas

- [ ] **Z-Index**
  - [ ] Layer scale

- [ ] **Breakpoints**
  - [ ] Responsive scale

### Documentación requerida

- [ ] Naming convention documentada
- [ ] Formato de tokens (CSS vars, JSON, etc.)
- [ ] Guía de uso por categoría
- [ ] Ejemplos de aplicación
- [ ] Proceso de actualización

---

## 📝 Notas de implementación

### Formatos de tokens

| Formato | Uso | Ejemplo |
|---------|-----|---------|
| **CSS Custom Properties** | Web | `--color-primary: #e8796e` |
| **JSON** | Design tools, multi-platform | `{ "color": { "primary": "#e8796e" } }` |
| **SCSS Variables** | Build-time | `$color-primary: #e8796e` |
| **Figma Variables** | Design | Variable en Figma |

### Herramientas recomendadas

| Herramienta | Uso |
|-------------|-----|
| **Style Dictionary** | Transformar tokens a múltiples formatos |
| **Tokens Studio** | Plugin de Figma para tokens |
| **Figma Variables** | Variables nativas de Figma |
| **Tailwind Config** | Tokens en Tailwind CSS |

---

> **Fin de la guía**  
> **Versión:** 1.0
