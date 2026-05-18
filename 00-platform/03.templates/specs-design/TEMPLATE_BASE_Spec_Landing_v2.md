# 📘 TEMPLATE BASE — SPEC LANDING PAGE (Marketing/Conversion/SEO)

> **Versión:** 2.0 (Estandarizada para agentes)  
> **Tipo:** P1 — Core  
> **Última actualización:** {{FECHA_ACTUALIZACION}}

---

## 🔖 GUÍA DE USO DEL TEMPLATE

### Marcadores de obligatoriedad

| Marcador | Significado | Regla |
|----------|-------------|-------|
| `[OBL]` | **Obligatorio** | Siempre debe completarse |
| `[OPC]` | **Opcional** | Completar si aplica al proyecto |
| `[COND]` | **Condicional** | Completar solo si se cumple la condición indicada |

### Placeholders

- `{{NOMBRE}}` → Reemplazar con valor específico del proyecto
- `[Elegir: opción1 / opción2]` → Seleccionar una opción
- `[Listar...]` → Agregar items según aplique

### Reglas de activación

Cada sección indica cuándo debe incluirse. Si no aplica, **omitir la sección completa** (no dejar vacía).

---

# ESPECIFICACIÓN DE LANDING PAGE

---

## 0) Metadatos del documento [OBL]

> **Activación:** Siempre obligatorio.

| Campo | Valor |
|-------|-------|
| **Nombre del documento** | Spec_LP_{{NOMBRE_LANDING}}_{{VERSION}} |
| **Proyecto** | {{NOMBRE_PROYECTO}} |
| **Campaña / Iniciativa** | {{NOMBRE_CAMPAÑA}} |
| **Landing Page** | {{NOMBRE_LANDING}} |
| **ID técnico** | `lp-{{NUM}}-{{SLUG}}` (ej: `lp-01-main-acquisition`) |
| **Versión** | {{VERSION}} (ej: v1.0) |
| **Estado** | [Elegir: Draft / Review / Approved / Live / Deprecated] |
| **Prioridad** | [Elegir: Crítica / Alta / Media / Baja] |
| **Tipo** | [Elegir: Web / Responsive / Mobile-first] |
| **Fecha** | {{FECHA_YYYY-MM-DD}} |
| **Owner (Marketing/PM)** | {{NOMBRE_MARKETING}} |
| **UX/UI Owner** | {{NOMBRE_UX}} |
| **Copy Owner** | {{NOMBRE_COPY}} |
| **Growth / Performance Owner** | {{NOMBRE_GROWTH}} |
| **Tech Lead** | {{NOMBRE_TECH}} |
| **QA Owner** | {{NOMBRE_QA}} |

---

## 1) Propósito de la landing [OBL]

> **Activación:** Siempre obligatorio.

### 1.1 Descripción general [OBL]

Esta landing page está diseñada para **{{AUDIENCIA_OBJETIVO}}** con el fin de **{{OBJETIVO_PRINCIPAL}}**.

| Campo | Valor |
|-------|-------|
| **Función en el funnel** | [Elegir: TOFU / MOFU / BOFU / Retargeting / Remarketing / Branded] |
| **Canales de tráfico** | [Elegir múltiples: Ads / SEO / Email / Social / Afiliados / Directo] |

### 1.2 Objetivo de negocio [OBL]

1. {{OBJETIVO_NEGOCIO_1}}
2. {{OBJETIVO_NEGOCIO_2}}
3. {{OBJETIVO_NEGOCIO_3}}

### 1.3 Objetivos de conversión [OBL]

| Tipo | Conversión | CTA | Prioridad |
|------|------------|-----|-----------|
| **Principal** | {{CONVERSION_PRINCIPAL}} (ej: Lead, Demo, Registro) | {{CTA_PRINCIPAL}} | Crítica |
| **Secundaria** | {{CONVERSION_SECUNDARIA}} (ej: Newsletter, Video play) | {{CTA_SECUNDARIO}} | Alta |
| **Micro** | {{MICRO_CONVERSION}} (ej: Scroll, Click pricing) | — | Media |

### 1.4 KPIs / Métricas objetivo [OBL]

| Métrica | Valor objetivo | Valor crítico (alerta) |
|---------|----------------|------------------------|
| CVR principal | {{VALOR}} | < {{VALOR_CRITICO}} |
| CTR CTA principal | {{VALOR}} | < {{VALOR_CRITICO}} |
| CPL / CPA | {{VALOR}} | > {{VALOR_CRITICO}} |
| Bounce rate | {{VALOR}} | > {{VALOR_CRITICO}} |
| Scroll depth (75%) | {{VALOR}} | < {{VALOR_CRITICO}} |
| Form completion rate | {{VALOR}} | < {{VALOR_CRITICO}} |
| Tiempo en página | {{VALOR}} | < {{VALOR_CRITICO}} |

---

## 2) Alcance (Scope) [OBL]

> **Activación:** Siempre obligatorio.

### 2.1 Incluye (In Scope) [OBL]

- {{INCLUYE_1}} (ej: Hero + propuesta de valor)
- {{INCLUYE_2}} (ej: Bloques de beneficios)
- {{INCLUYE_3}} (ej: Prueba social / testimonials)
- {{INCLUYE_4}} (ej: Formulario + integración CRM)
- {{INCLUYE_5}} (ej: SEO técnico básico)
- {{INCLUYE_6}} (ej: Analytics y tracking)

### 2.2 No incluye (Out of Scope) [OBL]

- {{EXCLUYE_1}}
- {{EXCLUYE_2}}
- {{EXCLUYE_3}}

### 2.3 Dependencias [OBL]

| Tipo | Dependencia | Estado | Owner | Fecha límite |
|------|-------------|--------|-------|--------------|
| Diseño | {{DEPENDENCIA}} | [Pendiente/En progreso/Listo] | {{OWNER}} | {{FECHA}} |
| Copy | {{DEPENDENCIA}} | [Pendiente/En progreso/Listo] | {{OWNER}} | {{FECHA}} |
| Integración | {{DEPENDENCIA}} | [Pendiente/En progreso/Listo] | {{OWNER}} | {{FECHA}} |
| Assets | {{DEPENDENCIA}} | [Pendiente/En progreso/Listo] | {{OWNER}} | {{FECHA}} |
| Legal | {{DEPENDENCIA}} | [Pendiente/En progreso/Listo] | {{OWNER}} | {{FECHA}} |

---

## 3) Audiencia y segmentación [OBL]

> **Activación:** Siempre obligatorio para landing pages.

### 3.1 Audiencia primaria [OBL]

| Campo | Valor |
|-------|-------|
| **Perfil** | {{PERFIL_PRIMARIO}} |
| **Necesidad / dolor principal** | {{DOLOR_PRINCIPAL}} |
| **Nivel de awareness** | [Elegir: Unaware / Problem-aware / Solution-aware / Product-aware / Most-aware] |
| **Intención** | [Elegir: Informacional / Navegacional / Transaccional] |

### 3.2 Audiencia secundaria [OPC]

| Campo | Valor |
|-------|-------|
| **Perfil** | {{PERFIL_SECUNDARIO}} |
| **Uso de la landing** | {{USO}} |

### 3.3 Variantes por segmento [COND]

> **Activación:** Incluir si hay variantes de landing por segmento.

| Segmento | Cambio en copy | Cambio en oferta | Cambio visual | Cambio CTA | URL |
|----------|----------------|------------------|---------------|------------|-----|
| {{SEGMENTO_1}} | {{CAMBIO}} | {{CAMBIO}} | {{CAMBIO}} | {{CAMBIO}} | {{URL}} |
| {{SEGMENTO_2}} | {{CAMBIO}} | {{CAMBIO}} | {{CAMBIO}} | {{CAMBIO}} | {{URL}} |

### 3.4 Fuentes de tráfico [OBL]

| Fuente | % estimado | UTM source | Notas |
|--------|------------|------------|-------|
| Google Ads | {{%}} | `google` | {{NOTAS}} |
| Meta Ads | {{%}} | `facebook` | {{NOTAS}} |
| LinkedIn Ads | {{%}} | `linkedin` | {{NOTAS}} |
| SEO orgánico | {{%}} | `organic` | {{NOTAS}} |
| Email | {{%}} | `email` | {{NOTAS}} |
| Directo/Referral | {{%}} | `direct` | {{NOTAS}} |

---

## 4) Journey de conversión [OBL]

> **Activación:** Siempre obligatorio.

### 4.1 Entry points [OBL]

| Origen | URL / Parámetros | Contexto del usuario |
|--------|------------------|---------------------|
| {{ORIGEN_1}} | `{{URL}}?utm_source={{SOURCE}}` | {{CONTEXTO}} |
| {{ORIGEN_2}} | `{{URL}}?utm_source={{SOURCE}}` | {{CONTEXTO}} |

### 4.2 Scroll Journey (narrativa de persuasión) [OBL]

```
1. Usuario aterriza → ve HERO (3-5 seg para captar atención)
2. Entiende PROPUESTA DE VALOR (headline + subheadline)
3. Revisa BENEFICIOS / DIFERENCIADORES
4. Valida CONFIANZA (logos, testimonios, casos)
5. Llega a CTA / FORMULARIO
6. Convierte o realiza micro-conversión
```

### 4.3 CTA Journey [OBL]

| Ubicación | CTA presente | Comportamiento | Prioridad |
|-----------|--------------|----------------|-----------|
| Above the fold | Sí/No | {{COMPORTAMIENTO}} | Crítica |
| Post-beneficios | Sí/No | {{COMPORTAMIENTO}} | Alta |
| Post-proof | Sí/No | {{COMPORTAMIENTO}} | Alta |
| Final de página | Sí/No | {{COMPORTAMIENTO}} | Crítica |
| Sticky (mobile) | Sí/No | {{COMPORTAMIENTO}} | Media |

### 4.4 Flujos alternos [OPC]

| Flujo | Descripción | Comportamiento esperado |
|-------|-------------|------------------------|
| Scanner | Usuario solo lee títulos | Headlines deben ser auto-explicativos |
| High-intent | Click CTA inmediato | CTA above fold funcional |
| Need-proof | Necesita validación social | Scroll hasta testimonios |
| Form abandonment | Abandona formulario | {{COMPORTAMIENTO}} |
| Validation error | Error en campos | {{COMPORTAMIENTO}} |

---

## 5) Estructura narrativa de la landing [OBL]

> **Activación:** Siempre obligatorio. Define el orden de bloques y lógica de persuasión.

### 5.1 Mapa de secciones [OBL]

| Orden | Sección | Objetivo | Prioridad | Obligatoria | Objeción que resuelve |
|-------|---------|----------|-----------|-------------|----------------------|
| 1 | Hero | Captar atención + CTA | Crítica | Sí | — |
| 2 | Problema | Crear relevancia | Alta | [Sí/No] | "¿Esto es para mí?" |
| 3 | Solución | Explicar propuesta | Crítica | Sí | "¿Qué ofreces?" |
| 4 | Beneficios | Mostrar valor | Alta | Sí | "¿Por qué me importa?" |
| 5 | Cómo funciona | Reducir fricción | Media | [Sí/No] | "¿Es complicado?" |
| 6 | Proof / Social | Construir confianza | Alta | Sí | "¿Puedo confiar?" |
| 7 | Pricing/Oferta | Clarificar inversión | [Alta/Media] | [Sí/No] | "¿Cuánto cuesta?" |
| 8 | FAQ | Resolver objeciones | Media | [Sí/No] | Objeciones específicas |
| 9 | CTA final | Convertir | Crítica | Sí | — |
| 10 | Footer legal | Cumplimiento | Alta | Sí | — |

### 5.2 Detalle por bloque [OBL]

> Repetir para cada bloque crítico.

#### Bloque: {{NOMBRE_BLOQUE}}

| Campo | Valor |
|-------|-------|
| **Mensaje clave** | {{MENSAJE}} |
| **Acción esperada del usuario** | {{ACCION}} |
| **Objeción que resuelve** | {{OBJECION}} |
| **KPI asociado** | {{KPI}} |
| **Componentes incluidos** | {{COMPONENTES}} |

---

## 6) Inventario de componentes UI [OBL]

> **Activación:** Siempre obligatorio.

### 6.1 Lista de componentes [OBL]

| ID | Nombre | Tipo | Reutilizable | Prioridad | Fuente | Estado |
|----|--------|------|--------------|-----------|--------|--------|
| `cmp-01` | Hero Section | Section | No | Crítica | Custom | {{ESTADO}} |
| `cmp-02` | CTA Button Primary | Button | Sí | Crítica | DS | {{ESTADO}} |
| `cmp-03` | Lead Form | Form | Sí | Crítica | Shared | {{ESTADO}} |
| `cmp-04` | Benefit Card | Card | Sí | Alta | Shared | {{ESTADO}} |
| `cmp-05` | Testimonial Card | Card | Sí | Alta | Shared | {{ESTADO}} |
| `cmp-06` | Logo Bar | Section | Sí | Alta | Shared | {{ESTADO}} |
| `cmp-07` | FAQ Accordion | Accordion | Sí | Media | Shared | {{ESTADO}} |
| `cmp-08` | Sticky CTA | CTA Bar | Sí | Media | Nuevo | {{ESTADO}} |

### 6.2 Jerarquía visual [OBL]

| Nivel | Componentes | Justificación |
|-------|-------------|---------------|
| **Primario** | Hero + CTA principal | Primera impresión, conversión |
| **Secundario** | Beneficios, Proof, Oferta | Argumentación |
| **Terciario** | FAQ, Detalles, Disclaimers | Soporte |

### 6.3 Componentes condicionales [OPC]

| Componente | Condición para mostrar |
|------------|------------------------|
| Video demo | Solo desktop / campaña específica |
| Countdown | Solo campañas con fecha límite |
| Sticky CTA | Solo mobile |
| Pricing block | Solo tráfico high-intent |
| Chat widget | Solo horario laboral |

---

## 7) Especificación por componente [OBL]

> **Activación:** Repetir por cada componente crítico (Hero, CTA, Form, Testimonial, FAQ).

---

### 7.X {{NOMBRE_COMPONENTE}} [OBL por componente crítico]

#### a) Identificación [OBL]

| Campo | Valor |
|-------|-------|
| **ID** | `cmp-{{NUM}}` |
| **Nombre técnico** | `{{slug-componente}}` |
| **Tipo** | [Elegir: Button / Form / Card / Banner / Accordion / Section / Modal] |
| **Reutilizable** | Sí / No |
| **Owner** | [Elegir: Design System / Frontend / Growth Team] |

#### b) Propósito [OBL]

{{DESCRIPCION_FUNCION_EN_CONVERSION}}

#### c) Estructura interna [OBL]

| Elemento | Requerido | Contenido/Fuente | Fallback |
|----------|-----------|------------------|----------|
| Headline | Sí/No | {{CONTENIDO}} | {{FALLBACK}} |
| Subheadline | Sí/No | {{CONTENIDO}} | {{FALLBACK}} |
| Visual (imagen/video) | Sí/No | {{CONTENIDO}} | {{FALLBACK}} |
| CTA | Sí/No | {{CONTENIDO}} | {{FALLBACK}} |
| Trust signal | Sí/No | {{CONTENIDO}} | {{FALLBACK}} |
| Legal note | Sí/No | {{CONTENIDO}} | {{FALLBACK}} |

#### d) Variantes [OPC]

| Variante | Cuándo aplica | Diferencias |
|----------|---------------|-------------|
| Default | {{CONDICION}} | — |
| Mobile | {{CONDICION}} | {{DIFERENCIAS}} |
| Desktop | {{CONDICION}} | {{DIFERENCIAS}} |
| Campaign A/B | {{CONDICION}} | {{DIFERENCIAS}} |
| Segment variant | {{CONDICION}} | {{DIFERENCIAS}} |

#### e) Estados [OBL]

| Estado | Apariencia | Trigger |
|--------|------------|---------|
| `default` | {{DESCRIPCION}} | Estado inicial |
| `hover` | {{DESCRIPCION}} | Mouse over |
| `focus` | {{DESCRIPCION}} | Foco teclado |
| `loading` | {{DESCRIPCION}} | Procesando |
| `success` | {{DESCRIPCION}} | Conversión exitosa |
| `error` | {{DESCRIPCION}} | Error en acción |
| `disabled` | {{DESCRIPCION}} | No disponible |

#### f) Reglas de comportamiento [OBL]

| Evento | Comportamiento | Notas |
|--------|----------------|-------|
| Click CTA | {{COMPORTAMIENTO}} | {{NOTAS}} |
| Submit form | {{COMPORTAMIENTO}} | {{NOTAS}} |
| Validation error | {{COMPORTAMIENTO}} | {{NOTAS}} |
| Integration fail | {{COMPORTAMIENTO}} | {{NOTAS}} |
| Usuario ya convirtió | {{COMPORTAMIENTO}} | {{NOTAS}} |

#### g) Specs visuales (UI) [OPC]

| Propiedad | Valor | Token |
|-----------|-------|-------|
| Width | {{VALOR}} | {{TOKEN}} |
| Height | {{VALOR}} | {{TOKEN}} |
| Padding | {{VALOR}} | {{TOKEN}} |
| Border radius | {{VALOR}} | {{TOKEN}} |
| Shadow | {{VALOR}} | {{TOKEN}} |
| Typography | {{VALOR}} | {{TOKEN}} |
| Color | {{VALOR}} | {{TOKEN}} |

#### h) Responsive [OPC]

| Breakpoint | Comportamiento |
|------------|----------------|
| Mobile (320-767) | {{COMPORTAMIENTO}} |
| Tablet (768-1023) | {{COMPORTAMIENTO}} |
| Desktop (1024+) | {{COMPORTAMIENTO}} |

#### i) Accesibilidad (A11Y) [OBL]

| Requisito | Implementación |
|-----------|----------------|
| `aria-label` | {{VALOR}} |
| Tab order | {{POSICION}} |
| Keyboard support | {{TECLAS}} |
| Touch target | Mínimo 44x44px |
| Contrast | WCAG AA (4.5:1) |
| Error messages | Accesibles vía `aria-describedby` |

#### j) Analytics [OBL]

| Evento | Trigger | Payload |
|--------|---------|---------|
| `{{EVENTO_VIEW}}` | Visible en viewport | `page_id, component_id, campaign_id` |
| `{{EVENTO_CLICK}}` | Click/tap | `page_id, component_id, position, utm_*` |
| `{{EVENTO_SUBMIT}}` | Form submit | `page_id, form_id, campaign_id` |
| `{{EVENTO_ERROR}}` | Error | `page_id, error_type, field` |

---

## 8) Layout y estructura de página [OBL]

> **Activación:** Siempre obligatorio.

### 8.1 Estructura general [OBL]

```
┌─────────────────────────────────────┐
│       HEADER (si aplica)            │
├─────────────────────────────────────┤
│            HERO SECTION             │
├─────────────────────────────────────┤
│       BLOQUES NARRATIVOS            │
│  (Beneficios / Proof / Cómo func.)  │
├─────────────────────────────────────┤
│        FORMULARIO / CTA             │
├─────────────────────────────────────┤
│              FAQ                    │
├─────────────────────────────────────┤
│          FOOTER LEGAL               │
└─────────────────────────────────────┘
│ OVERLAYS: Modal, Toast, Cookie      │
└─────────────────────────────────────┘
```

### 8.2 Grid / Layout system [OBL]

| Propiedad | Valor |
|-----------|-------|
| Tipo de layout | [Elegir: Flex / Grid / Mixto] |
| Columnas | {{NUM_COLUMNAS}} |
| Gap | {{VALOR}} |
| Max width | {{VALOR}} |
| Container padding | {{VALOR}} |

### 8.3 Jerarquía de zonas [OBL]

| Zona | Prioridad | Above fold | Sticky |
|------|-----------|------------|--------|
| Header | Media | Sí | Sí/No |
| Hero | Crítica | Sí | No |
| Bloques narrativos | Alta | No | No |
| Form/CTA | Crítica | Sí (CTA) / No (form) | No |
| FAQ | Media | No | No |
| Footer | Alta | No | No |

---

## 9) Navegación [OBL]

> **Activación:** Siempre obligatorio.

### 9.1 URL y rutas [OBL]

| Campo | Valor |
|-------|-------|
| URL principal | `{{URL}}` |
| URL con UTMs | `{{URL}}?utm_source={{SOURCE}}&utm_medium={{MEDIUM}}&utm_campaign={{CAMPAIGN}}` |
| Canonical | `{{URL_CANONICAL}}` |
| Thank-you page | `{{URL_THANKYOU}}` |
| Redirect post-conversion | `{{URL_REDIRECT}}` |

### 9.2 Navegación interna [OPC]

| Elemento | Destino | Tipo |
|----------|---------|------|
| Logo | {{DESTINO}} | [Link externo / Anchor / Ninguno] |
| Nav links (si hay) | {{DESTINO}} | [Anchor / Externo] |
| CTA principal | {{DESTINO}} | [Anchor a form / Modal / Redirect] |
| Footer links | {{DESTINO}} | [Externo] |

### 9.3 Comportamiento post-conversión [OBL]

| Escenario | Comportamiento |
|-----------|----------------|
| Form success | [Elegir: Thank-you page / Inline success / Modal / Redirect externo] |
| Form error | [Elegir: Inline error / Toast / Modal] |
| Duplicate lead | {{COMPORTAMIENTO}} |

---

## 10) Formulario e integraciones [OBL]

> **Activación:** Siempre obligatorio para landings con captura de leads.

### 10.1 Campos del formulario [OBL]

| Campo | Tipo | Requerido | Validación | Placeholder | Error message |
|-------|------|-----------|------------|-------------|---------------|
| {{CAMPO_1}} | [text/email/tel/select] | Sí/No | {{REGLA}} | {{PLACEHOLDER}} | {{ERROR}} |
| {{CAMPO_2}} | [text/email/tel/select] | Sí/No | {{REGLA}} | {{PLACEHOLDER}} | {{ERROR}} |
| {{CAMPO_3}} | [text/email/tel/select] | Sí/No | {{REGLA}} | {{PLACEHOLDER}} | {{ERROR}} |
| Consent | checkbox | Sí | checked | — | {{ERROR}} |

### 10.2 Integraciones [OBL]

| Sistema | Tipo | Endpoint/Config | Campos mapeados | Owner |
|---------|------|-----------------|-----------------|-------|
| {{CRM}} | [API/Webhook/Native] | {{ENDPOINT}} | {{CAMPOS}} | {{OWNER}} |
| {{EMAIL_PLATFORM}} | [API/Webhook/Native] | {{ENDPOINT}} | {{CAMPOS}} | {{OWNER}} |
| {{ANALYTICS}} | [Tag/Pixel] | {{CONFIG}} | {{EVENTOS}} | {{OWNER}} |

### 10.3 Flujo de datos [OBL]

```
Form Submit → Validación frontend → Envío a backend/integración
           → Success: Thank-you + tracking event
           → Error: Mensaje inline + retry
```

### 10.4 Fallbacks [OBL]

| Escenario | Fallback |
|-----------|----------|
| CRM no disponible | {{FALLBACK}} |
| Timeout | {{FALLBACK}} |
| Error de validación backend | {{FALLBACK}} |

---

## 11) Reglas de negocio / conversión [OBL]

> **Activación:** Siempre obligatorio.

### 11.1 Reglas de conversión [OBL]

| ID | Regla | Componentes afectados |
|----|-------|----------------------|
| BR-01 | {{REGLA}} | {{COMPONENTES}} |
| BR-02 | {{REGLA}} | {{COMPONENTES}} |

### 11.2 Reglas de visibilidad [OPC]

| Elemento | Condición para mostrar | Condición para ocultar |
|----------|------------------------|------------------------|
| {{ELEMENTO}} | {{CONDICION}} | {{CONDICION}} |

### 11.3 Reglas de oferta [COND]

> **Activación:** Incluir si hay ofertas, descuentos o condiciones especiales.

| Oferta | Condición | Vigencia | Restricciones |
|--------|-----------|----------|---------------|
| {{OFERTA}} | {{CONDICION}} | {{VIGENCIA}} | {{RESTRICCIONES}} |

---

## 12) Estados de página [OBL]

> **Activación:** Siempre obligatorio.

### 12.1 Loading [OBL]

| Elemento | Tipo de loading | Duración máx | Fallback |
|----------|-----------------|--------------|----------|
| Página inicial | {{TIPO}} | {{DURACION}} | {{FALLBACK}} |
| Form submit | {{TIPO}} | {{DURACION}} | {{FALLBACK}} |
| Assets (imágenes) | {{TIPO}} | {{DURACION}} | {{FALLBACK}} |

### 12.2 Error States [OBL]

| Tipo | Mensaje | CTA | Comportamiento |
|------|---------|-----|----------------|
| Error de red | {{MENSAJE}} | {{CTA}} | {{COMPORTAMIENTO}} |
| Error de form | {{MENSAJE}} | {{CTA}} | {{COMPORTAMIENTO}} |
| Error de integración | {{MENSAJE}} | {{CTA}} | {{COMPORTAMIENTO}} |
| Página no encontrada | {{MENSAJE}} | {{CTA}} | {{COMPORTAMIENTO}} |

### 12.3 Success States [OBL]

| Conversión | Mensaje | Siguiente paso | Tracking |
|------------|---------|----------------|----------|
| Lead capturado | {{MENSAJE}} | {{SIGUIENTE}} | `form_success` |
| Micro-conversión | {{MENSAJE}} | {{SIGUIENTE}} | `{{EVENTO}}` |

---

## 13) Accesibilidad (A11Y) [OBL]

> **Activación:** Siempre obligatorio.

### 13.1 Estándar aplicable [OBL]

- **Nivel objetivo:** WCAG 2.1 AA
- **Contraste mínimo:** 4.5:1 (texto normal), 3:1 (texto grande)
- **Focus visible:** Obligatorio

### 13.2 Formulario accesible [OBL]

| Requisito | Implementación |
|-----------|----------------|
| Labels asociados | `<label for="">` en cada input |
| Errores accesibles | `aria-describedby` vinculado al mensaje |
| Instrucciones de formato | Texto visible + `aria-describedby` |
| Anuncios dinámicos | `aria-live="polite"` para feedback |

### 13.3 Navegación por teclado [OBL]

| Elemento | Tecla | Acción |
|----------|-------|--------|
| Tab | Tab/Shift+Tab | Navegar elementos |
| CTAs | Enter/Space | Activar |
| Acordeones | Enter/Space | Expandir/colapsar |
| Modales | Escape | Cerrar |

### 13.4 Touch targets [OBL]

- **Tamaño mínimo:** 44x44px
- **Espaciado mínimo:** 8px

---

## 14) Responsive [OBL]

> **Activación:** Siempre obligatorio.

### 14.1 Breakpoints [OBL]

| Nombre | Rango | Prioridad |
|--------|-------|-----------|
| Mobile | 320–767px | Primaria (mobile-first) |
| Tablet | 768–1023px | Secundaria |
| Desktop | 1024–1439px | Primaria |
| Large Desktop | 1440px+ | Secundaria |

### 14.2 Cambios por breakpoint [OBL]

| Elemento | Mobile | Tablet | Desktop |
|----------|--------|--------|---------|
| Hero layout | Stack vertical | Mixto | 2 columnas |
| Formulario | 1 columna | 1-2 columnas | 2 columnas |
| Benefit cards | 1 columna | 2 columnas | 3-4 columnas |
| Sticky CTA | Visible | Opcional | Oculto |
| FAQ | Acordeón | Acordeón | Acordeón/Grid |

### 14.3 Comportamientos especiales [OPC]

| Comportamiento | Breakpoints | Descripción |
|----------------|-------------|-------------|
| Sticky CTA | Mobile | {{DESCRIPCION}} |
| Hero video | Desktop only | {{DESCRIPCION}} |
| Lazy loading | Todos | {{DESCRIPCION}} |

---

## 15) Design System / Tokens [OPC]

> **Activación:** Incluir si hay design system. Si no, omitir.

### 15.1 Tokens de color [OPC]

| Uso | Token | Valor |
|-----|-------|-------|
| Primary CTA | `--color-primary` | {{VALOR}} |
| Background | `--color-bg` | {{VALOR}} |
| Text | `--color-text` | {{VALOR}} |
| Success | `--color-success` | {{VALOR}} |
| Error | `--color-error` | {{VALOR}} |

### 15.2 Tipografía [OPC]

| Uso | Token | Valor |
|-----|-------|-------|
| Hero headline | `--font-hero` | {{VALOR}} |
| Section headline | `--font-h2` | {{VALOR}} |
| Body | `--font-body` | {{VALOR}} |
| CTA | `--font-cta` | {{VALOR}} |

---

## 16) Copy, mensajería y SEO [OBL]

> **Activación:** Siempre obligatorio para landing pages.

### 16.1 Propuesta de valor [OBL]

| Campo | Copy | Variante A/B |
|-------|------|--------------|
| **H1 (Headline)** | {{COPY}} | {{VARIANTE}} |
| **Subheadline** | {{COPY}} | {{VARIANTE}} |
| **Mensaje clave** | {{COPY}} | — |
| **Objeción principal** | {{OBJECION}} | — |

### 16.2 Copy por sección [OBL]

| Sección | Objetivo | Copy | Variante A/B |
|---------|----------|------|--------------|
| Hero | Captar atención | {{COPY}} | {{VARIANTE}} |
| Beneficios | Mostrar valor | {{COPY}} | {{VARIANTE}} |
| Proof | Generar confianza | {{COPY}} | {{VARIANTE}} |
| CTA final | Convertir | {{COPY}} | {{VARIANTE}} |

### 16.3 Microcopy de formulario [OBL]

| Elemento | Copy |
|----------|------|
| Placeholder email | {{COPY}} |
| Label teléfono | {{COPY}} |
| Error email inválido | {{COPY}} |
| Error campo requerido | {{COPY}} |
| Texto de consentimiento | {{COPY}} |
| Mensaje de éxito | {{COPY}} |

### 16.4 SEO Metadata [OBL]

| Campo | Valor | Caracteres |
|-------|-------|------------|
| SEO Title | {{VALOR}} | {{NUM}}/60 |
| Meta Description | {{VALOR}} | {{NUM}}/160 |
| H1 | {{VALOR}} | — |
| Canonical | {{URL}} | — |
| Indexación | [Elegir: index,follow / noindex,nofollow] | — |
| Open Graph Title | {{VALOR}} | — |
| OG Description | {{VALOR}} | — |
| OG Image | {{URL_IMAGEN}} | — |
| Schema markup | [Elegir: FAQ / Organization / Product / Service / WebPage] | — |

---

## 17) Analytics, tracking y atribución [OBL]

> **Activación:** Siempre obligatorio.

### 17.1 Eventos de página [OBL]

| Evento | Trigger | Payload |
|--------|---------|---------|
| `page_view` | Carga de página | `page_id, utm_*, referrer` |
| `scroll_depth` | 25/50/75/90% | `page_id, depth, time_on_page` |
| `time_on_page` | Intervalos | `page_id, seconds` |

### 17.2 Eventos de conversión [OBL]

| Evento | Trigger | Payload | Plataformas |
|--------|---------|---------|-------------|
| `cta_click` | Click CTA | `page_id, cta_id, position, utm_*` | GA4, Meta, LinkedIn |
| `form_start` | Primer foco | `page_id, form_id` | GA4 |
| `form_submit` | Submit | `page_id, form_id, utm_*` | GA4, Meta, LinkedIn |
| `form_success` | Respuesta OK | `page_id, lead_type` | GA4, Meta, LinkedIn, Ads |
| `form_error` | Error | `page_id, error_type, field` | GA4 |

### 17.3 Captura de atribución [OBL]

| Parámetro | Captura | Storage | Envío a CRM |
|-----------|---------|---------|-------------|
| `utm_source` | URL | Cookie/Session | Sí |
| `utm_medium` | URL | Cookie/Session | Sí |
| `utm_campaign` | URL | Cookie/Session | Sí |
| `utm_content` | URL | Cookie/Session | Sí |
| `utm_term` | URL | Cookie/Session | Sí |
| `gclid` | URL | Cookie | Sí |
| `fbclid` | URL | Cookie | Sí |

### 17.4 Pixels y tags [OBL]

| Plataforma | Evento | Trigger | Consentimiento requerido |
|------------|--------|---------|--------------------------|
| GA4 | `page_view` | Page load | Sí/No |
| GA4 | `generate_lead` | Form success | Sí/No |
| Meta Pixel | `PageView` | Page load | Sí |
| Meta Pixel | `Lead` | Form success | Sí |
| LinkedIn | `conversion` | Form success | Sí |
| Google Ads | `conversion` | Form success | Sí |

---

## 18) Performance web [OBL]

> **Activación:** Siempre obligatorio para landing pages (impacta conversión).

### 18.1 Objetivos Core Web Vitals [OBL]

| Métrica | Objetivo | Crítico si excede |
|---------|----------|-------------------|
| LCP (Largest Contentful Paint) | < 2.5s | > 4s |
| INP (Interaction to Next Paint) | < 200ms | > 500ms |
| CLS (Cumulative Layout Shift) | < 0.1 | > 0.25 |
| TTFB (Time to First Byte) | < 800ms | > 1.8s |
| Peso total página | < {{VALOR}}KB | > {{VALOR}}KB |

### 18.2 Estrategias de optimización [OBL]

| Estrategia | Aplica a | Implementación |
|------------|----------|----------------|
| Imágenes WebP/AVIF | Todas las imágenes | {{IMPLEMENTACION}} |
| Lazy loading | Below fold | `loading="lazy"` |
| Preload críticos | Hero, fonts | `<link rel="preload">` |
| Third-party async | Scripts no críticos | `async` / `defer` |
| Fonts optimizadas | Todas | `font-display: swap` |

### 18.3 Riesgos de performance [OPC]

| Riesgo | Impacto | Mitigación |
|--------|---------|------------|
| Video hero pesado | LCP alto | {{MITIGACION}} |
| Muchos trackers | INP alto | {{MITIGACION}} |
| Imágenes sin optimizar | LCP + peso | {{MITIGACION}} |
| Widgets externos | Blocking | {{MITIGACION}} |

---

## 19) QA / Casos de prueba [OBL]

> **Activación:** Siempre obligatorio.

### 19.1 Casos funcionales [OBL]

| ID | Caso | Resultado esperado | Prioridad |
|----|------|-------------------|-----------|
| TF-01 | CTA principal navega a form/ancla | {{RESULTADO}} | Crítica |
| TF-02 | Form valida campos requeridos | {{RESULTADO}} | Crítica |
| TF-03 | Form envía datos a CRM | {{RESULTADO}} | Crítica |
| TF-04 | Thank-you page se muestra | {{RESULTADO}} | Crítica |
| TF-05 | UTMs persisten en formulario | {{RESULTADO}} | Alta |

### 19.2 Casos visuales [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TV-01 | Hero above the fold (mobile) | Visible completo |
| TV-02 | Responsive en breakpoints | Sin roturas |
| TV-03 | Estados hover/focus visibles | Feedback visual |

### 19.3 Casos de tracking [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TT-01 | `page_view` dispara al cargar | Evento en GA4 |
| TT-02 | `cta_click` con payload correcto | UTMs presentes |
| TT-03 | `form_success` dispara conversión | Evento en todas las plataformas |
| TT-04 | Pixels respetan consentimiento | No disparan sin consent |

### 19.4 Casos de error [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TE-01 | Sin conexión a red | Mensaje de error amigable |
| TE-02 | CRM timeout | Fallback + mensaje |
| TE-03 | Campo inválido | Error inline específico |

### 19.5 Casos de accesibilidad [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TA-01 | Navegación con teclado | Todos los CTAs alcanzables |
| TA-02 | Focus visible | Outline claro |
| TA-03 | Form con screen reader | Labels anunciados |
| TA-04 | Contraste WCAG AA | Aprobado |

---

## 20) Riesgos, supuestos y decisiones [OBL]

> **Activación:** Siempre obligatorio.

### 20.1 Riesgos identificados [OBL]

| ID | Riesgo | Probabilidad | Impacto | Mitigación | Owner |
|----|--------|--------------|---------|------------|-------|
| R-01 | {{RIESGO}} | [Alta/Media/Baja] | [Alto/Medio/Bajo] | {{MITIGACION}} | {{OWNER}} |

### 20.2 Supuestos [OBL]

| ID | Supuesto | Validado | Fecha |
|----|----------|----------|-------|
| S-01 | {{SUPUESTO}} | Sí/No | {{FECHA}} |

### 20.3 Decisiones pendientes [OBL]

| ID | Tema | Decisión | Responsable | Fecha límite |
|----|------|----------|-------------|--------------|
| D-01 | CTA copy | {{DECISION}} | {{RESPONSABLE}} | {{FECHA}} |
| D-02 | Campos de form | {{DECISION}} | {{RESPONSABLE}} | {{FECHA}} |
| D-03 | Proof autorizado | {{DECISION}} | {{RESPONSABLE}} | {{FECHA}} |

---

## 21) Checklist de aprobación (Go / No-Go Launch) [OBL]

> **Activación:** Siempre obligatorio. Última validación antes de lanzar.

### 21.1 Marketing / Growth [OBL]

- [ ] Objetivo de conversión definido
- [ ] Mensajería aprobada
- [ ] CTAs definidos (principal + secundario)
- [ ] KPIs objetivo establecidos
- [ ] Audiencia y segmentos definidos

### 21.2 UX/UI [OBL]

- [ ] Estructura narrativa definida
- [ ] Componentes inventariados
- [ ] Responsive validado en breakpoints
- [ ] Accesibilidad mínima validada
- [ ] Estados (loading/error/success) definidos

### 21.3 Técnica [OBL]

- [ ] Formulario funcional + integraciones
- [ ] SEO metadata configurado
- [ ] URLs y canonical definidos
- [ ] Performance dentro de objetivos (LCP < 2.5s)

### 21.4 Analytics [OBL]

- [ ] Tracking configurado (GA4, pixels)
- [ ] Eventos de conversión definidos
- [ ] UTMs capturados y enviados a CRM
- [ ] Dashboards/reportes listos

### 21.5 Legal / Compliance [COND]

> **Activación:** Incluir si aplica regulación (GDPR, etc.)

- [ ] Aviso de privacidad enlazado
- [ ] Consentimiento de datos
- [ ] Disclaimers de oferta
- [ ] CMP / Cookie banner

### 21.6 Firmas de aprobación [OBL]

| Rol | Nombre | Fecha | Status |
|-----|--------|-------|--------|
| Marketing/Growth | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| UX/UI | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| Tech Lead | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| Analytics | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| QA | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| Legal | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado/N/A] |

---

## 22) Particularidades del proyecto [OPC]

> **Activación:** Usar para excepciones o customizaciones específicas que no encajan en secciones estándar.

### 22.1 Excepciones al estándar

| Sección afectada | Excepción | Justificación | Aprobado por |
|------------------|-----------|---------------|--------------|
| {{SECCION}} | {{EXCEPCION}} | {{JUSTIFICACION}} | {{APROBADOR}} |

### 22.2 Customizaciones específicas

{{DESCRIPCION_CUSTOMIZACIONES}}

### 22.3 Notas para el equipo

{{NOTAS_ADICIONALES}}

---

## 📋 ANEXOS REQUERIDOS

> Marcar los anexos que aplican a esta landing:

- [ ] **Anexo Form** → Si el formulario es complejo (usar TEMPLATE_BASE_Spec_Form)
- [ ] **Anexo UXStates** → Referencia a estándar global (usar TEMPLATE_BASE_Spec_UXStates)
- [ ] **Anexo ModalOverlay** → Si hay modales críticos (usar TEMPLATE_BASE_Spec_ModalOverlay)

---

## 🔁 GUÍA OPERATIVA PARA AGENTES

### Cómo usar este template:

1. **Copiar** el template completo
2. **Reemplazar** todos los `{{PLACEHOLDER}}` con valores específicos
3. **Seleccionar** opciones en `[Elegir: ...]`
4. **Omitir** secciones `[OPC]` o `[COND]` si no aplican
5. **Repetir** sección 7 por cada componente crítico
6. **Validar** con checklist (sección 21) antes de lanzar

### Secciones núcleo (mínimo viable para launch):

- §0 Metadatos
- §1 Propósito + conversión
- §2 Scope
- §4 Journey de conversión
- §5 Estructura narrativa
- §6 Inventario de componentes
- §7 Specs de componentes críticos (Hero, Form, CTA)
- §10 Formulario e integraciones
- §12 Estados
- §16 Copy + SEO
- §17 Analytics/Tracking
- §18 Performance
- §21 Checklist

### Diferencias clave vs AppScreen:

| Aspecto | Landing | AppScreen |
|---------|---------|-----------|
| Foco | Conversión única | Funcionalidad múltiple |
| Audiencia | Externa (campañas) | Usuarios autenticados |
| Tracking | UTMs, pixels, atribución | Analytics de producto |
| SEO | Crítico | Secundario |
| Performance | Core Web Vitals estrictos | Importante pero flexible |

### Validación cruzada:

- Cada bloque en §5 debe tener componentes en §6
- Cada campo de form en §10 debe tener error en §12
- Cada evento en §17 debe tener caso de prueba en §19.3
- Cada CTA debe tener tracking asociado

---

> **Fin del template**  
> **Versión:** 2.0  
> **Última actualización:** {{FECHA_ACTUALIZACION}}
