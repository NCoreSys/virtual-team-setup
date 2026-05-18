# 📰 TEMPLATE BASE — SPEC CONTENT / CMS / SEO PAGE

> **Versión:** 2.0 (Estandarizada para agentes)  
> **Tipo:** P3 — Conditional  
> **Última actualización:** {{FECHA_ACTUALIZACION}}

---

## 🔖 GUÍA DE USO DEL TEMPLATE

### Marcadores de obligatoriedad

| Marcador | Significado | Regla |
|----------|-------------|-------|
| `[OBL]` | **Obligatorio** | Siempre debe completarse |
| `[OPC]` | **Opcional** | Completar si aplica al proyecto |
| `[COND]` | **Condicional** | Completar solo si se cumple la condición indicada |

### Cuándo usar este template

- ✅ **Blog posts** y artículos
- ✅ **Help Center** y documentación
- ✅ **Knowledge Base** (FAQ, guías)
- ✅ **Páginas legales** (Terms, Privacy, etc.)
- ✅ **About / Company pages**
- ✅ Cualquier página con **objetivo SEO orgánico**
- ❌ Landing page de conversión → usar TEMPLATE_BASE_Spec_Landing
- ❌ Pantalla de app interna → usar TEMPLATE_BASE_Spec_AppScreen
- ❌ Entity detail (producto, orden) → usar TEMPLATE_BASE_Spec_EntityDetail

---

# ESPECIFICACIÓN DE CONTENT / CMS / SEO PAGE

---

## 0) Metadatos del documento [OBL]

> **Activación:** Siempre obligatorio.

| Campo | Valor |
|-------|-------|
| **Nombre del documento** | Spec_Content_{{NOMBRE_PAGINA}}_{{VERSION}} |
| **Proyecto** | {{NOMBRE_PROYECTO}} |
| **Tipo de página** | [Elegir: Blog / Help Center / Docs / Legal / About / Knowledge Base / FAQ] |
| **Página** | {{NOMBRE_PAGINA}} |
| **ID técnico** | `seo-{{NUM}}-{{SLUG}}` (ej: `seo-01-help-article`) |
| **Ruta** | {{RUTA}} (ej: `/blog/:slug`, `/help/:category/:slug`) |
| **Fuente** | [Elegir: CMS / Markdown / Headless CMS / Hardcoded] |
| **Versión** | {{VERSION}} |
| **Estado** | [Elegir: Draft / Review / Approved / Deprecated] |
| **Prioridad** | [Elegir: Crítica / Alta / Media / Baja] |
| **Fecha** | {{FECHA_YYYY-MM-DD}} |
| **Owner (Content/PM)** | {{NOMBRE_CONTENT}} |
| **SEO Owner** | {{NOMBRE_SEO}} |
| **UX/UI Owner** | {{NOMBRE_UX}} |
| **Tech Lead** | {{NOMBRE_TECH}} |
| **QA Owner** | {{NOMBRE_QA}} |
| **Legal (si aplica)** | {{NOMBRE_LEGAL}} |

---

## 1) Propósito de la página [OBL]

> **Activación:** Siempre obligatorio.

### 1.1 Descripción general [OBL]

Esta página provee **{{TIPO_CONTENIDO}}** para **{{AUDIENCIA}}**.

| Campo | Valor |
|-------|-------|
| **Tipo de contenido** | [Elegir: Información / Educación / Soporte / Legal / Branding] |
| **Objetivo principal** | [Elegir: SEO orgánico / Reducción de tickets / Educación / Compliance / Brand awareness] |
| **Audiencia** | {{AUDIENCIA}} |

### 1.2 Objetivo de negocio [OBL]

1. {{OBJETIVO_1}} (ej: Tráfico orgánico)
2. {{OBJETIVO_2}} (ej: Autoridad E-E-A-T)
3. {{OBJETIVO_3}} (ej: Reducción de tickets de soporte)
4. {{OBJETIVO_4}} (ej: Cumplimiento legal)

### 1.3 Objetivo UX [OBL]

- Lectura clara y scannable
- Navegación fácil (TOC, breadcrumbs)
- Confiabilidad (autor, fecha, fuentes)
- Performance excelente (Core Web Vitals)

### 1.4 KPIs [OBL]

| Métrica | Valor objetivo |
|---------|----------------|
| Organic sessions | {{VALOR}}/mes |
| CTR en SERP | > {{VALOR}}% |
| Scroll depth (75%+) | > {{VALOR}}% |
| Time on page | > {{VALOR}}s |
| Bounce rate | < {{VALOR}}% |
| Conversion assist | {{VALOR}}% |

---

## 2) Alcance (Scope) [OBL]

> **Activación:** Siempre obligatorio.

### 2.1 Incluye (In Scope) [OBL]

- {{INCLUYE_1}} (ej: Estructura de contenido)
- {{INCLUYE_2}} (ej: Componentes editoriales - TOC, callouts, code blocks)
- {{INCLUYE_3}} (ej: SEO metadata completo)
- {{INCLUYE_4}} (ej: Schema markup)
- {{INCLUYE_5}} (ej: Enlaces internos/externos)

### 2.2 No incluye (Out of Scope) [OBL]

- {{EXCLUYE_1}} (ej: Formularios de conversión — usar Landing)
- {{EXCLUYE_2}} (ej: Checkout)

### 2.3 Dependencias [OBL]

| Tipo | Dependencia | Estado | Owner |
|------|-------------|--------|-------|
| CMS | {{CMS}} (ej: Contentful, Sanity, WordPress) | [Pendiente/Listo] | {{OWNER}} |
| Search | {{SEARCH}} (ej: Algolia, interno) | [Pendiente/Listo] | {{OWNER}} |
| Analytics | {{ANALYTICS}} | [Pendiente/Listo] | {{OWNER}} |
| CDN/Images | {{CDN}} | [Pendiente/Listo] | {{OWNER}} |

---

## 3) Audiencia e intención de búsqueda [OBL]

> **Activación:** Siempre obligatorio.

### 3.1 Audiencia [OBL]

| Campo | Valor |
|-------|-------|
| **Audiencia primaria** | {{AUDIENCIA}} |
| **Audiencia secundaria** | {{AUDIENCIA}} (opcional) |
| **Nivel de conocimiento** | [Elegir: Principiante / Intermedio / Avanzado] |
| **Contexto de llegada** | [Elegir: Búsqueda orgánica / Link interno / Referral / Social] |

### 3.2 Intención de búsqueda [OBL]

| Tipo | Aplica | Keywords ejemplo |
|------|--------|------------------|
| **Informacional** | Sí/No | "qué es...", "cómo funciona..." |
| **Navegacional** | Sí/No | "[marca] ayuda", "[marca] docs" |
| **Transaccional** | Sí/No | "comprar...", "precio..." |
| **Investigación comercial** | Sí/No | "mejor...", "comparativa..." |

### 3.3 Keywords target [OBL]

| Keyword | Volumen | Dificultad | Intención | Prioridad |
|---------|---------|------------|-----------|-----------|
| {{KEYWORD_1}} | {{VOL}} | {{DIF}} | {{INTENCION}} | Alta |
| {{KEYWORD_2}} | {{VOL}} | {{DIF}} | {{INTENCION}} | Media |
| {{KEYWORD_LSI}} | {{VOL}} | {{DIF}} | {{INTENCION}} | Baja |

### 3.4 Etapa del funnel [OBL]

| Etapa | Descripción | Aplica |
|-------|-------------|--------|
| TOFU (Awareness) | Descubrimiento del problema | ☐ |
| MOFU (Consideration) | Evaluando soluciones | ☐ |
| BOFU (Decision) | Listo para actuar | ☐ |

---

## 4) Estructura del contenido [OBL] — **SECCIÓN NÚCLEO**

> **Activación:** Siempre obligatorio.

### 4.1 Outline del contenido [OBL]

| Orden | Bloque | Heading | Objetivo | Formato | Palabras aprox |
|------:|--------|---------|----------|---------|---------------:|
| 1 | Título | H1 | Tema principal + keyword | Heading | — |
| 2 | Intro | — | Contexto, hook, promesa | Paragraph | {{NUM}} |
| 3 | TOC | — | Navegación rápida | Component | — |
| 4 | Sección 1 | H2 | {{OBJETIVO}} | H2 + body | {{NUM}} |
| 5 | Sección 2 | H2 | {{OBJETIVO}} | H2 + body | {{NUM}} |
| 6 | Subsección | H3 | {{OBJETIVO}} | H3 + body | {{NUM}} |
| 7 | FAQ | H2 | Preguntas comunes | Accordion | {{NUM}} |
| 8 | Conclusión | H2 | Resumen + siguiente paso | Paragraph | {{NUM}} |
| 9 | CTA | — | Conversión | Banner/Button | — |
| 10 | Related | — | Mantener en sitio | Links | — |

### 4.2 Reglas editoriales [OBL]

| Regla | Valor |
|-------|-------|
| Tono | [Elegir: Formal / Casual / Técnico / Amigable] |
| Longitud objetivo | {{NUM}} palabras |
| Máximo nivel de heading | H3 (no usar H4+) |
| Párrafos | Máximo {{NUM}} líneas |
| Listas | Usar cuando hay 3+ items |
| Imágenes | Alt text descriptivo obligatorio |
| Enlaces internos | Mínimo {{NUM}} por artículo |
| Enlaces externos | Solo a fuentes confiables, `rel="nofollow"` si aplica |

### 4.3 Jerarquía de headings [OBL]

```
H1: Título principal (1 por página)
├── H2: Sección principal 1
│   ├── H3: Subsección 1.1
│   └── H3: Subsección 1.2
├── H2: Sección principal 2
│   └── H3: Subsección 2.1
├── H2: FAQ
└── H2: Conclusión
```

---

## 5) Componentes editoriales [OBL]

> **Activación:** Siempre obligatorio.

### 5.1 Inventario de componentes [OBL]

| Componente | Uso | Reglas | A11Y |
|------------|-----|--------|------|
| **Table of Contents (TOC)** | Navegación rápida | Sticky sidebar o inline | Links con anchors |
| **Callout/Alert** | Destacar info importante | Tipos: info, warning, tip, danger | Contraste, no solo color |
| **Code block** | Mostrar código | Syntax highlighting | `<pre><code>` |
| **Table** | Datos tabulares | Responsive | `<th scope>` |
| **Quote/Blockquote** | Citas | Atribución | `<blockquote cite>` |
| **Image** | Visual | Alt text obligatorio | `alt`, `loading="lazy"` |
| **Video embed** | Contenido multimedia | Thumbnail + play | Transcripción |
| **Accordion/FAQ** | Preguntas | Expandible | `aria-expanded` |
| **CTA Banner** | Conversión | Destacado | Botón accesible |
| **Author box** | E-E-A-T | Avatar + bio | — |
| **Related articles** | Retención | 3-5 artículos | Links descriptivos |

### 5.2 Detalle de componentes críticos [OBL]

#### Table of Contents (TOC) [COND]

> **Activación:** Incluir para artículos largos (>1000 palabras).

| Campo | Valor |
|-------|-------|
| Posición | [Inline después de intro / Sticky sidebar] |
| Niveles incluidos | H2, H3 |
| Collapsible | Sí/No |
| Highlight active | Sí (en scroll) |

#### Callouts [OBL]

| Tipo | Icono | Color | Uso |
|------|-------|-------|-----|
| Info | ℹ️ | Azul | Información adicional |
| Tip | 💡 | Verde | Consejo útil |
| Warning | ⚠️ | Amarillo | Advertencia |
| Danger | 🚫 | Rojo | Alerta crítica |

#### Author box [COND]

> **Activación:** Incluir para E-E-A-T (blog, docs con expertise).

| Campo | Valor |
|-------|-------|
| Avatar | Imagen del autor |
| Nombre | Nombre completo |
| Rol/Título | Posición o expertise |
| Bio | 1-2 líneas |
| Link | Perfil o LinkedIn |

---

## 6) SEO (Metadata) [OBL] — **SECCIÓN NÚCLEO**

> **Activación:** Siempre obligatorio.

### 6.1 Metadata básico [OBL]

| Campo | Valor | Caracteres |
|-------|-------|------------|
| **SEO Title** | {{TITULO_SEO}} | 50-60 |
| **Meta Description** | {{META_DESCRIPCION}} | 150-160 |
| **URL Slug** | {{SLUG}} | Corto, con keyword |
| **Canonical** | {{URL_CANONICAL}} | URL absoluta |
| **Robots** | [index, follow] / [noindex, nofollow] | — |
| **Language** | {{LANG}} (ej: es-MX, en-US) | — |

### 6.2 Open Graph (OG) [OBL]

| Campo | Valor |
|-------|-------|
| `og:title` | {{OG_TITLE}} |
| `og:description` | {{OG_DESCRIPTION}} |
| `og:image` | {{OG_IMAGE_URL}} (1200x630px) |
| `og:type` | [article / website] |
| `og:url` | {{URL}} |
| `og:site_name` | {{SITE_NAME}} |

### 6.3 Twitter Cards [OBL]

| Campo | Valor |
|-------|-------|
| `twitter:card` | [summary_large_image / summary] |
| `twitter:title` | {{TWITTER_TITLE}} |
| `twitter:description` | {{TWITTER_DESCRIPTION}} |
| `twitter:image` | {{TWITTER_IMAGE_URL}} |

### 6.4 Estructura semántica [OBL]

| Requisito | Implementación |
|-----------|----------------|
| 1 solo H1 | ✅ Obligatorio |
| H2/H3 jerárquicos | ✅ Sin saltar niveles |
| Párrafos cortos | ✅ Máximo 3-4 líneas |
| Listas para enumerar | ✅ `<ul>`, `<ol>` |
| Links descriptivos | ✅ No "click aquí" |

### 6.5 Internal linking [OBL]

| Tipo | Implementación |
|------|----------------|
| Links en contenido | {{NUM}} mínimo por artículo |
| Anchor text | Descriptivo, con keyword si natural |
| Related articles | {{NUM}} al final |
| Breadcrumbs | [Sí / No] |
| Pillar/Cluster | {{ESTRATEGIA}} |

### 6.6 Schema markup [OBL]

| Schema | Aplica | Campos requeridos |
|--------|--------|-------------------|
| `Article` | Blog posts | headline, author, datePublished, image |
| `FAQPage` | Páginas con FAQ | mainEntity (questions) |
| `HowTo` | Tutoriales | step, name, text |
| `BreadcrumbList` | Navegación | itemListElement |
| `Organization` | About page | name, logo, url |
| `WebPage` | Genérico | name, description |

#### Ejemplo de schema Article [OBL]

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{{TITULO}}",
  "author": {
    "@type": "Person",
    "name": "{{AUTOR}}"
  },
  "datePublished": "{{FECHA_PUBLICACION}}",
  "dateModified": "{{FECHA_MODIFICACION}}",
  "image": "{{URL_IMAGEN}}",
  "publisher": {
    "@type": "Organization",
    "name": "{{PUBLISHER}}",
    "logo": "{{LOGO_URL}}"
  }
}
```

---

## 7) Datos y CMS [OBL]

> **Activación:** Siempre obligatorio.

### 7.1 Campos del CMS [OBL]

| Campo | Tipo | Requerido | Uso |
|-------|------|-----------|-----|
| `title` | string | Sí | H1 |
| `slug` | string | Sí | URL |
| `seo_title` | string | Sí | Meta title |
| `meta_description` | string | Sí | Meta description |
| `body` | richtext | Sí | Contenido principal |
| `excerpt` | string | No | Preview en listados |
| `featured_image` | image | Sí | OG image, hero |
| `author` | reference | [Sí/No] | E-E-A-T |
| `category` | reference | [Sí/No] | Organización |
| `tags` | array | No | Filtrado |
| `published_at` | datetime | Sí | Fecha de publicación |
| `updated_at` | datetime | Sí | Freshness |
| `status` | enum | Sí | draft/published/archived |
| `{{CAMPO}}` | {{TIPO}} | Sí/No | {{USO}} |

### 7.2 Validaciones del CMS [OBL]

| Campo | Validación |
|-------|------------|
| `slug` | Único, lowercase, sin espacios |
| `seo_title` | Max 60 caracteres |
| `meta_description` | Max 160 caracteres |
| `featured_image` | Min 1200x630px |
| `body` | No vacío |

### 7.3 Preview y publish workflow [OPC]

| Estado | Comportamiento |
|--------|----------------|
| Draft | Solo visible en preview |
| Scheduled | Publicará en fecha programada |
| Published | Visible públicamente |
| Archived | No visible, no indexado |
---

*...Continuación de Parte 1 (Secciones 0-7)*

---

## 8) Navegación [OBL]

> **Activación:** Siempre obligatorio.

### 8.1 Estructura de URLs [OBL]

| Tipo de página | Patrón de URL |
|----------------|---------------|
| Blog post | `/blog/{{slug}}` |
| Help article | `/help/{{category}}/{{slug}}` |
| Docs | `/docs/{{version}}/{{section}}/{{slug}}` |
| Legal | `/legal/{{slug}}` |

### 8.2 Breadcrumbs [OBL]

```
Home > Blog > Categoría > Título del artículo
```

### 8.3 Artículos relacionados [OBL]

| Campo | Valor |
|-------|-------|
| Cantidad | {{NUM}} artículos |
| Lógica | [Mismo category / Tags / Manual] |
| Posición | [Sidebar / Fin del artículo] |

### 8.4 Búsqueda interna [COND]

| Campo | Valor |
|-------|-------|
| Search provider | {{PROVIDER}} |
| Campos indexados | title, body, tags |

---

## 9) Estados (UX States) [OBL]

> **Activación:** Siempre obligatorio. Referencia: `UXStates_Pack_{{PROYECTO}}`

| Estado | Trigger | UI |
|--------|---------|-----|
| `loading` | Cargando contenido | Skeleton |
| `loaded` | Contenido listo | Artículo completo |
| `error_404` | Slug no encontrado | Error + search |
| `error_500` | Error servidor | Error + retry |

---

## 10) Accesibilidad (A11Y) [OBL]

### 10.1 Headings [OBL]

- Jerarquía correcta (H1 → H2 → H3)
- 1 solo H1 por página
- Descriptivos

### 10.2 Imágenes [OBL]

- Alt text obligatorio
- Decorativas: `alt=""`

### 10.3 Links [OBL]

- Texto descriptivo
- Links externos: `target="_blank" rel="noopener"`
- Focus visible

### 10.4 Contenido [OBL]

- Contraste WCAG AA
- Font size mínimo 16px
- Line height 1.5+

---

## 11) Performance [OBL]

### 11.1 Core Web Vitals [OBL]

| Métrica | Objetivo | Crítico |
|---------|----------|---------|
| LCP | < 2.5s | > 4s |
| INP | < 200ms | > 500ms |
| CLS | < 0.1 | > 0.25 |

### 11.2 Optimizaciones [OBL]

| Estrategia | Implementación |
|------------|----------------|
| Images | `loading="lazy"`, WebP, responsive |
| Fonts | Preload, font-display: swap |
| CSS | Critical CSS inline |
| JS | Defer non-critical |
| Third-party | Minimizar scripts externos |

---

## 12) Analytics / Instrumentación [OBL]

### 12.1 Eventos [OBL]

| Evento | Trigger | Payload |
|--------|---------|---------|
| `content_view` | Página visible | `content_id, slug, category, author` |
| `scroll_depth` | 25%, 50%, 75%, 100% | `content_id, depth` |
| `toc_click` | Click en TOC | `content_id, anchor` |
| `cta_click` | Click en CTA | `content_id, cta_id` |
| `related_click` | Click en relacionado | `content_id, related_id` |
| `search_used` | Búsqueda interna | `query, results_count` |
| `copy_code` | Copiar code block | `content_id, code_index` |

### 12.2 Métricas SEO [OBL]

| Métrica | Fuente |
|---------|--------|
| Organic sessions | GA4 |
| Impressions/Clicks | Search Console |
| Average position | Search Console |
| CTR | Search Console |

---

## 13) QA / Casos de prueba [OBL]

### 13.1 Casos de contenido [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TC-01 | Render de artículo | Contenido completo visible |
| TC-02 | Headings correctos | H1 único, jerarquía correcta |
| TC-03 | Imágenes con alt | Todas tienen alt text |
| TC-04 | Links funcionan | No broken links |

### 13.2 Casos de SEO [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TS-01 | Meta title | Presente, <60 chars |
| TS-02 | Meta description | Presente, <160 chars |
| TS-03 | Canonical | URL correcta |
| TS-04 | Schema markup | Válido en testing tool |
| TS-05 | OG tags | Todos presentes |

### 13.3 Casos de performance [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TP-01 | LCP | < 2.5s |
| TP-02 | CLS | < 0.1 |
| TP-03 | Images lazy load | Correcto |

### 13.4 Casos de accesibilidad [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TA-01 | Keyboard navigation | TOC, links navegables |
| TA-02 | Screen reader | Headings anunciados |
| TA-03 | Contraste | WCAG AA |

---

## 14) Riesgos, supuestos y decisiones [OBL]

### 14.1 Riesgos [OBL]

| ID | Riesgo | Probabilidad | Impacto | Mitigación |
|----|--------|--------------|---------|------------|
| R-01 | Duplicate content | Media | Alto | Canonicals |
| R-02 | Thin content | Media | Medio | Min word count |
| R-03 | Broken links | Alta | Medio | Link checker |

### 14.2 Supuestos [OBL]

| ID | Supuesto | Validado |
|----|----------|----------|
| S-01 | CMS soporta campos requeridos | Sí/No |
| S-02 | Schema markup implementable | Sí/No |

### 14.3 Decisiones pendientes [OBL]

| ID | Tema | Decisión | Responsable | Fecha |
|----|------|----------|-------------|-------|
| D-01 | CMS seleccionado | {{DECISION}} | Tech | {{FECHA}} |
| D-02 | Schema types | {{DECISION}} | SEO | {{FECHA}} |

---

## 15) Checklist de aprobación [OBL]

### 15.1 Contenido [OBL]

- [ ] Outline definido (§4)
- [ ] Componentes editoriales especificados (§5)
- [ ] Campos CMS definidos (§7)

### 15.2 SEO [OBL]

- [ ] Metadata completo (§6)
- [ ] Schema markup definido
- [ ] Internal linking strategy
- [ ] URL structure definida

### 15.3 Técnica [OBL]

- [ ] Performance targets definidos
- [ ] Accesibilidad validada
- [ ] Analytics instrumentado

### 15.4 QA [OBL]

- [ ] Casos de prueba documentados

### 15.5 Firmas de aprobación [OBL]

| Rol | Nombre | Fecha | Status |
|-----|--------|-------|--------|
| Content/PM | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| SEO Owner | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| UX/UI | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| Tech Lead | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| QA | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |

---

## 16) Particularidades del proyecto [OPC]

### 16.1 Excepciones al estándar

| Sección | Excepción | Justificación |
|---------|-----------|---------------|
| {{SECCION}} | {{EXCEPCION}} | {{JUSTIFICACION}} |

---

## 📋 ANEXOS RELACIONADOS

- [ ] **UXStates** → Referencia a estándar global
- [ ] **Form** → Si hay formularios de suscripción/contacto

---

## 🔁 GUÍA OPERATIVA PARA AGENTES

### Cómo usar este template:

1. **Copiar** el template
2. **Completar §4** (Estructura del contenido) — sección núcleo
3. **Completar §6** (SEO metadata) — sección núcleo
4. **Definir §7** (Campos CMS)
5. **Validar** con SEO Owner

### Secciones núcleo (mínimo viable):

- §0 Metadatos
- §3 Audiencia e intención
- §4 **Estructura del contenido** ← NÚCLEO
- §5 Componentes editoriales
- §6 **SEO metadata** ← NÚCLEO
- §7 Campos CMS
- §11 Performance
- §12 Analytics
- §15 Checklist

### Validación cruzada:

- Cada heading en §4 debe seguir jerarquía
- Keywords en §3 deben aparecer en §6 (title, description)
- Schema en §6.6 debe coincidir con tipo de página
- Campos CMS en §7 deben soportar metadata de §6

### Red flags a evitar:

- ❌ Sin keyword research
- ❌ Meta title > 60 caracteres
- ❌ Meta description > 160 caracteres
- ❌ Sin schema markup
- ❌ Headings saltados (H1 → H3)
- ❌ Imágenes sin alt text
- ❌ Sin canonical
- ❌ Sin breadcrumbs

---

> **Fin del template**  
> **Versión:** 2.0  
> **Última actualización:** {{FECHA_ACTUALIZACION}}
