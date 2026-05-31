# DICCIONARIO DE DELIVERABLES — FASE 0: DISCOVERY

**Versión:** 1.1.0  
**Fecha:** 2026-05-14  
**Cambios vs V1.0:** Agregados campos "Ejecuta" y "Perfil de ejecución" en todos los deliverables  
**Total deliverables:** 22  
**Objetivo de fase:** Validar que el producto tiene sentido antes de invertir recursos.  
**Duración típica:** 1-4 semanas  
**Criterio de salida de fase:** Product Owner aprueba continuar.

---

## Nota sobre Responsable vs Ejecuta

| Rol | Significado |
|-----|-------------|
| **Responsable** | Dueño del resultado. Revisa, valida calidad, responde si sale mal. No necesariamente hace el trabajo. |
| **Ejecuta** | Hace el trabajo operativo. Puede ser el mismo responsable, un agente especializado, un analista o un externo. |
| **Aprueba** | Da el go/no-go final sobre el deliverable. |

El **Responsable** define el brief, supervisa la ejecución y valida la calidad del entregable. El **Ejecuta** produce el contenido. En VTT, el Ejecuta puede ser un agente especializado que recibe un brief del Responsable.

---

## Roles involucrados en esta fase

| Rol | Nivel | Participa en |
|-----|-------|-------------|
| Product Owner (PO) | ●●● Principal | Todas las subfases |
| Product Manager (PM) | ●●● Principal | 0.1, 0.2 |
| Systems Analyst (SA) | ● Participa | 0.1, 0.2, 0.3 |
| Design Lead | ● Participa | 0.2, 0.4 |
| UX Designer / Researcher | ● Participa | 0.2, 0.3, 0.4 |
| Research Agent (VTT) | ● Ejecutor | 0.1, 0.2 |

---

# 0.1 MARKET RESEARCH

**Responsable:** Product Manager  
**Aprueba:** Product Owner  
**Objetivo de subfase:** Entender el mercado, tamaño y tendencias antes de definir el producto.

---

### 0.1.1 Market Research Report

| Campo | Valor |
|-------|-------|
| **Fase** | 00-Discovery |
| **Subfase** | 0.1 Market Research |
| **Responsable** | Product Manager |
| **Ejecuta** | Research Agent / Systems Analyst |
| **Aprueba** | Product Owner |
| **Formato** | PDF/MD |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 3-5 días |
| **Frecuencia** | Una vez por proyecto |

**Perfil de ejecución:** Requiere habilidades de investigación de mercado, acceso a fuentes de datos de industria (Statista, reportes sectoriales, datos gubernamentales), y capacidad de síntesis analítica. En VTT: asignable a un agente SA con prompt de research de mercado, o a un Research Agent especializado. El PM elabora el brief con el mercado objetivo y las preguntas clave a responder.

**Qué es:** Documento consolidado que presenta el análisis completo del mercado donde operará el producto. Integra los hallazgos de tamaño de mercado, tendencias, segmentos y mercado objetivo en una narrativa coherente.

**Para qué sirve:** Es la base factual sobre la que se toman todas las decisiones de producto. Sin este documento, las decisiones de alcance, pricing y posicionamiento se basan en suposiciones. Permite al Product Owner decidir si el mercado justifica la inversión.

**Inputs requeridos:**
- Brief del PM con preguntas clave y mercado a investigar
- Fuentes de datos de mercado (reportes de industria, Statista, IBISWorld, fuentes gubernamentales)
- Datos internos de la organización si existen
- Entrevistas preliminares con stakeholders del negocio

**Dependencias (predecessors):**
- Ninguna — es uno de los primeros deliverables del proyecto
- Requiere contexto de negocio provisto por el Product Owner (briefing inicial)

**Habilita (successors):**
- `0.1.2` TAM/SAM/SOM — se alimenta de este reporte
- `0.1.4` Market Segments — derivado del análisis
- `0.2.1` Competitive Analysis Doc — necesita el contexto de mercado
- `0.3.1` Problem Statement — los pain points de mercado informan la definición del problema
- `1.2.1` Scope Statement — el tamaño de oportunidad influye en el alcance del MVP

**Audiencia:**
- **Product Owner** — para decidir si invertir en el producto
- **Product Manager** — como base para todas las decisiones de producto
- **Investors/Stakeholders** — para justificar la oportunidad
- **Design Lead** — para entender el contexto de los usuarios

**Secciones esperadas:**
1. Executive Summary (1 página máximo)
2. Metodología (fuentes de datos, fechas de recolección)
3. Tamaño de mercado (TAM/SAM/SOM cuantificado)
4. Tendencias de la industria (3-5 tendencias clave)
5. Segmentos de mercado identificados
6. Mercado objetivo seleccionado con justificación
7. Oportunidades y riesgos de mercado
8. Conclusiones y recomendación

**Criterio de completitud:**
- [ ] Datos de mercado provienen de al menos 3 fuentes verificables
- [ ] TAM/SAM/SOM están cuantificados en cifras concretas
- [ ] Al menos 3 tendencias de mercado identificadas con evidencia
- [ ] Segmentos de mercado definidos con criterios claros
- [ ] Mercado objetivo seleccionado con justificación basada en datos
- [ ] Product Owner ha revisado y aprobado

**Anti-patrones:**
- ❌ **Datos de una sola fuente:** Basar todo en un solo reporte. Se necesita triangulación.
- ❌ **Mercado inflado:** Usar el TAM como si fuera el mercado alcanzable.
- ❌ **Research sin conclusión:** Presentar datos sin decir qué significan para el producto.
- ❌ **Datos obsoletos:** Fuentes de más de 2 años en mercados dinámicos.

**Template:** `_pm/templates/TEMPLATE_MARKET_RESEARCH.md` *(pendiente)*

**Ejemplo de referencia:** Análisis de mercado EdTech LATAM para Forajido — TAM de transcripción educativa en español, segmentos por nivel educativo, tendencias de IA en educación.

---

### 0.1.2 TAM/SAM/SOM

| Campo | Valor |
|-------|-------|
| **Fase** | 00-Discovery |
| **Subfase** | 0.1 Market Research |
| **Responsable** | Product Manager |
| **Ejecuta** | Research Agent / Systems Analyst |
| **Aprueba** | Product Owner |
| **Formato** | Sección dentro de 0.1.1 |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Una vez + actualización anual |

**Perfil de ejecución:** Requiere capacidad de análisis cuantitativo y modelado financiero básico. Debe saber calcular top-down y bottom-up, y ser honesto con los supuestos. En VTT: asignable al mismo agente que ejecuta 0.1.1, ya que es una sección del Market Research. El PM debe proveer criterios de filtrado geográfico y de capacidad para el SAM/SOM.

**Qué es:** Cuantificación del mercado en tres niveles: Total Addressable Market (todo el mercado posible), Serviceable Addressable Market (lo alcanzable geográfica y técnicamente), y Serviceable Obtainable Market (lo que realistamente capturaremos en 1-3 años).

**Para qué sirve:** Dimensiona la oportunidad y fuerza honestidad sobre cuánto mercado realmente se puede capturar. El SOM es el número que importa para decisiones de inversión.

**Inputs requeridos:**
- Brief del PM con criterios de filtrado geográfico y de capacidad
- Datos de tamaño de industria (reportes, datos públicos)
- Información geográfica del alcance del producto
- Capacidad de la organización (equipo, presupuesto, channels)
- Datos de penetración de competidores si disponibles

**Dependencias (predecessors):**
- `0.1.1` Market Research Report — provee datos base

**Habilita (successors):**
- `0.4.1` Value Proposition Canvas
- `1.6.1` Budget Estimate
- `1.6.4` ROI Projection

**Audiencia:**
- **Product Owner** — decisión go/no-go
- **Investors** — retorno potencial
- **Program Manager** — dimensionar recursos

**Secciones esperadas:**
1. TAM — cifra + metodología de cálculo
2. SAM — cifra + criterios de filtrado
3. SOM — cifra + supuestos de penetración realistas
4. Visualización (funnel o tabla comparativa)
5. Fuentes y fecha de los datos

**Criterio de completitud:**
- [ ] Tres niveles cuantificados con cifras concretas
- [ ] Metodología de cálculo documentada
- [ ] SOM basado en supuestos explícitos
- [ ] Al menos 2 fuentes independientes

**Anti-patrones:**
- ❌ **SOM = SAM:** Asumir captura total del mercado servible.
- ❌ **TAM sin filtrar:** Citar mercado global cuando el producto es regional.
- ❌ **Bottom-up fantasioso:** "Si solo el 1% nos compra..." no es un plan.

**Template:** Incluido dentro de `TEMPLATE_MARKET_RESEARCH.md`

---

### 0.1.3 Market Trends

| Campo | Valor |
|-------|-------|
| **Fase** | 00-Discovery |
| **Subfase** | 0.1 Market Research |
| **Responsable** | Product Manager |
| **Ejecuta** | Research Agent / Systems Analyst |
| **Aprueba** | Product Owner |
| **Formato** | Sección dentro de 0.1.1 |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez + revisión semestral |

**Perfil de ejecución:** Requiere capacidad de monitoreo de industria, lectura de reportes especializados y síntesis de tendencias. Debe distinguir hype de tendencia real (con datos de adopción). En VTT: asignable al Research Agent con acceso a búsqueda web y fuentes de industria. El PM debe indicar el sector y horizonte temporal a investigar.

**Qué es:** Identificación de las 3-5 tendencias principales que transforman la industria. No predicciones — movimientos observables con datos.

**Para qué sirve:** Posicionar el producto a favor de las corrientes del mercado. Identifica ventanas de oportunidad temporales.

**Inputs requeridos:**
- Brief del PM con sector y horizonte temporal
- Reportes de industria recientes (últimos 12 meses)
- Publicaciones especializadas del sector
- Movimientos de competidores (funding, lanzamientos, pivots)
- Cambios regulatorios relevantes

**Dependencias (predecessors):**
- `0.1.1` Market Research Report

**Habilita (successors):**
- `0.2.6` Market Opportunities
- `0.3.4` Why Now
- `0.4.4` Target Customer Profile

**Audiencia:**
- **Product Owner** — validar timing
- **Product Manager** — alinear features con tendencias
- **Solution Architect** — anticipar necesidades tecnológicas

**Secciones esperadas:**
1. Lista de 3-5 tendencias, cada una con:
   - Descripción (1-2 párrafos)
   - Evidencia (datos, fuentes)
   - Impacto en el producto (positivo/negativo/neutral)
   - Horizonte temporal
2. Matriz de tendencias vs impacto en el producto

**Criterio de completitud:**
- [ ] Mínimo 3 tendencias identificadas
- [ ] Cada una tiene evidencia concreta
- [ ] Impacto en el producto documentado
- [ ] Fuentes citadas con fecha

**Anti-patrones:**
- ❌ **Tendencias genéricas:** "La IA está creciendo" no es un insight.
- ❌ **Confundir hype con tendencia:** Trending topic ≠ tendencia de mercado.
- ❌ **Solo tendencias favorables:** Omitir las que juegan en contra es sesgo.

**Template:** Incluido dentro de `TEMPLATE_MARKET_RESEARCH.md`

---

### 0.1.4 Market Segments

| Campo | Valor |
|-------|-------|
| **Fase** | 00-Discovery |
| **Subfase** | 0.1 Market Research |
| **Responsable** | Product Manager |
| **Ejecuta** | Research Agent / Systems Analyst / PM |
| **Aprueba** | Product Owner |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez + revisión por fase de crecimiento |

**Perfil de ejecución:** Requiere capacidad de análisis de datos demográficos y de comportamiento, y criterio para definir segmentación MECE. El PM puede ejecutar directamente si tiene los datos del Market Research, o delegar al SA/Research Agent la recopilación y proponer la segmentación para validación del PM. En VTT: el agente necesita los datos de 0.1.1 y 0.1.2 como input.

**Qué es:** Tabla que divide el mercado en segmentos homogéneos usando criterios definidos (demográficos, geográficos, por comportamiento, por necesidad). Cada segmento tiene tamaño estimado y atractivo relativo.

**Para qué sirve:** Obliga a elegir a QUIÉN le vendes primero. Informa MVP, pricing, canal y messaging.

**Inputs requeridos:**
- `0.1.1` Market Research Report
- `0.1.2` TAM/SAM/SOM — para dimensionar cada segmento
- Datos demográficos del mercado objetivo

**Dependencias (predecessors):**
- `0.1.1` Market Research Report
- `0.1.2` TAM/SAM/SOM

**Habilita (successors):**
- `0.1.5` Target Market
- `0.2.1` Competitive Analysis
- `0.4.4` Target Customer Profile

**Audiencia:**
- **Product Owner** — priorizar segmentos
- **Product Manager** — features por segmento
- **UX Designer** — personas por segmento

**Secciones esperadas:**

| Segmento | Tamaño | Dolor principal | Willingness to pay | Accesibilidad | Prioridad |
|----------|--------|----------------|-------------------|---------------|-----------|

Más justificación de criterios de segmentación y priorización.

**Criterio de completitud:**
- [ ] Mínimo 3 segmentos identificados
- [ ] Cada uno con tamaño estimado
- [ ] Criterios MECE
- [ ] Prioridad asignada con justificación

**Anti-patrones:**
- ❌ **Segmento "todos":** No es un segmento.
- ❌ **Solo demografía:** Comportamiento y necesidad segmentan mejor.
- ❌ **Sin tamaño:** Sin estimación no se puede priorizar.

**Template:** Incluido dentro de `TEMPLATE_MARKET_RESEARCH.md`

---

### 0.1.5 Target Market

| Campo | Valor |
|-------|-------|
| **Fase** | 00-Discovery |
| **Subfase** | 0.1 Market Research |
| **Responsable** | Product Manager |
| **Ejecuta** | Product Manager |
| **Aprueba** | Product Owner |
| **Formato** | Descripción |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Una vez + revisión por pivot |

**Perfil de ejecución:** Este deliverable es una decisión estratégica, no una tarea de investigación. El PM lo ejecuta directamente basándose en los datos de segmentación ya recopilados. No es delegable a un agente porque requiere juicio de negocio y alineamiento con el PO. En VTT: el PM redacta la selección y justificación; un agente puede formatear pero no decidir.

**Qué es:** Declaración concreta de a quién va dirigido el producto en su primera fase. Selección del segmento prioritario con justificación detallada.

**Para qué sirve:** Cierra la conversación de "¿a quién le vendemos?" Cada decisión de producto se evalúa contra este target.

**Inputs requeridos:**
- `0.1.4` Market Segments — lista priorizada
- `0.1.2` TAM/SAM/SOM — tamaño del segmento elegido
- Criterios de decisión del Product Owner

**Dependencias (predecessors):**
- `0.1.4` Market Segments *(obligatorio)*
- `0.1.2` TAM/SAM/SOM *(obligatorio)*

**Habilita (successors):**
- `0.2.1` Competitive Analysis
- `0.3.1` Problem Statement
- `0.3.2` User Pain Points
- `0.4.4` Target Customer Profile
- `1.2.4` MVP Definition

**Audiencia:**
- Todo el equipo — brújula del proyecto

**Secciones esperadas:**
1. Segmento seleccionado (nombre + descripción)
2. Justificación basada en datos
3. Tamaño del segmento (SOM)
4. Características clave
5. Canales de acceso
6. Segmentos descartados y por qué

**Criterio de completitud:**
- [ ] Un solo segmento elegido
- [ ] Justificación basada en datos
- [ ] Product Owner aprueba
- [ ] El equipo puede responder "¿para quién es?" en una frase

**Anti-patrones:**
- ❌ **Target múltiple:** 3 targets = 3 productos.
- ❌ **Target aspiracional:** Elegir el más sexy vs el más accesible.
- ❌ **Sin justificación:** "Porque conocemos el sector" es débil.

**Template:** Incluido dentro de `TEMPLATE_MARKET_RESEARCH.md`

---

# 0.2 COMPETITIVE ANALYSIS

**Responsable:** Product Manager  
**Aprueba:** Product Owner  
**Objetivo de subfase:** Conocer competidores, fortalezas, debilidades y gaps explotables.

---

### 0.2.1 Competitive Analysis Doc

| Campo | Valor |
|-------|-------|
| **Fase** | 00-Discovery |
| **Subfase** | 0.2 Competitive Analysis |
| **Responsable** | Product Manager |
| **Ejecuta** | Research Agent / Systems Analyst |
| **Aprueba** | Product Owner |
| **Formato** | PDF/MD |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 3-5 días |
| **Frecuencia** | Una vez + actualización trimestral |

**Perfil de ejecución:** Requiere capacidad de investigación competitiva, acceso a productos competidores (trials, demos), habilidad para sintetizar información de múltiples fuentes en una narrativa estratégica. En VTT: asignable a un Research Agent con capacidad de web search + un SA que pruebe los productos hands-on. El PM provee brief con el target market y los criterios de comparación.

**Qué es:** Documento consolidado del panorama competitivo. Integra lista de competidores, features, pricing, SWOT y oportunidades.

**Para qué sirve:** Evita construir algo que ya existe o competir frontalmente sin diferenciación. Revela gaps y debilidades capitalizables.

**Inputs requeridos:**
- Brief del PM con target market y criterios de comparación
- `0.1.5` Target Market
- Acceso a productos competidores (demos, trials)
- Reviews de usuarios (G2, Capterra, App Store)
- Información pública de competidores

**Dependencias (predecessors):**
- `0.1.5` Target Market *(obligatorio)*
- `0.1.1` Market Research Report *(recomendado)*

**Habilita (successors):**
- `0.2.3` Feature Comparison
- `0.2.6` Market Opportunities
- `0.4.1` Value Proposition Canvas
- `0.4.3` Key Differentiators
- `1.2.4` MVP Definition

**Audiencia:**
- **Product Owner** — posicionamiento
- **Product Manager** — priorización de features
- **Design Lead** — benchmark UX
- **Solution Architect** — benchmark técnico

**Secciones esperadas:**
1. Resumen del panorama competitivo
2. Lista de competidores directos e indirectos
3. Análisis detallado por competidor
4. Matriz comparativa de features
5. SWOT por competidor
6. Gaps y oportunidades
7. Posicionamiento recomendado

**Criterio de completitud:**
- [ ] Mínimo 3 directos y 2 indirectos analizados
- [ ] Fortalezas Y debilidades por competidor
- [ ] Gaps identificados con evidencia
- [ ] Posicionamiento recomendado

**Anti-patrones:**
- ❌ **"No tenemos competencia":** Siempre la hay.
- ❌ **Solo lo del sitio web:** Probar el producto revela los insights reales.
- ❌ **Solo directos:** Los indirectos son igual de importantes.
- ❌ **Sesgo de confirmación:** Buscar solo debilidades para justificar el proyecto.

**Template:** `_pm/templates/TEMPLATE_COMPETITIVE_ANALYSIS.md` *(pendiente)*

---

### 0.2.2 Competitor List

| Campo | Valor |
|-------|-------|
| **Fase** | 00-Discovery |
| **Subfase** | 0.2 Competitive Analysis |
| **Responsable** | Product Manager |
| **Ejecuta** | Research Agent |
| **Aprueba** | Product Owner |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Actualización trimestral |

**Perfil de ejecución:** Tarea de recopilación que requiere búsqueda sistemática en directorios (G2, Capterra, ProductHunt, Crunchbase) y App Stores. En VTT: ideal para un Research Agent con web search. El PM debe proveer el target market y criterios de qué cuenta como competidor directo vs indirecto.

**Qué es:** Tabla con todos los competidores directos e indirectos clasificados por tipo, con información clave.

**Para qué sirve:** Inventario base del que se derivan todos los análisis competitivos.

**Inputs requeridos:**
- Brief del PM con criterios directo/indirecto
- `0.1.5` Target Market
- Directorios (G2, Capterra, ProductHunt, Crunchbase)
- Input del Product Owner sobre competidores conocidos

**Dependencias (predecessors):**
- `0.1.5` Target Market *(obligatorio)*

**Habilita (successors):**
- `0.2.1` Competitive Analysis Doc
- `0.2.3` Feature Comparison
- `0.2.4` Pricing Comparison
- `0.2.5` SWOT Analysis
- `0.2.7` UX Benchmarking

**Audiencia:**
- **Product Manager** — referencia continua
- **Product Owner** — panorama rápido

**Secciones esperadas:**

| Competidor | Tipo | Producto | Target | Pricing | Funding | URL |
|-----------|------|----------|--------|---------|---------|-----|

**Criterio de completitud:**
- [ ] Mínimo 5 competidores (3 directos, 2 indirectos)
- [ ] Clasificación directo/indirecto
- [ ] Información verificable con URL

**Anti-patrones:**
- ❌ **Lista infinita:** Más de 15 diluye el análisis.
- ❌ **Solo los obvios:** Buscar por problema resuelto, no solo por categoría.

**Template:** Incluido dentro de `TEMPLATE_COMPETITIVE_ANALYSIS.md`

---

### 0.2.3 Feature Comparison

| Campo | Valor |
|-------|-------|
| **Fase** | 00-Discovery |
| **Subfase** | 0.2 Competitive Analysis |
| **Responsable** | Product Manager |
| **Ejecuta** | Systems Analyst + UX Designer |
| **Aprueba** | Product Owner |
| **Formato** | Tabla/Matriz |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 2 días |
| **Frecuencia** | Actualización trimestral |

**Perfil de ejecución:** Requiere prueba hands-on de los productos competidores — no basta con leer el sitio web. El SA evalúa funcionalidad y capacidades técnicas, el UX Designer evalúa la experiencia. En VTT: no es totalmente automatizable porque requiere interacción real con los productos. Un agente puede estructurar la matriz y pre-llenar con información pública, pero el testing hands-on lo hace un humano o un SA con acceso real.

**Qué es:** Matriz que compara features clave de cada competidor vs el producto planeado. Clasifica cada feature como table-stake, diferenciadora, nice-to-have u oportunidad.

**Para qué sirve:** Identifica qué es obligatorio, qué genera ventaja y dónde hay gaps.

**Inputs requeridos:**
- `0.2.2` Competitor List
- Acceso hands-on a productos competidores
- Reviews de usuarios con mención de features
- Brief del PM con lista de features a evaluar

**Dependencias (predecessors):**
- `0.2.2` Competitor List *(obligatorio)*

**Habilita (successors):**
- `0.2.6` Market Opportunities
- `0.4.3` Key Differentiators
- `1.2.4` MVP Definition
- `2.1.1` Functional Requirements

**Audiencia:**
- **Product Manager** — priorización
- **Product Owner** — diferenciación
- **Tech Lead** — complejidad técnica

**Criterio de completitud:**
- [ ] Mínimo 15 features comparadas
- [ ] Basado en prueba directa del producto
- [ ] Cada feature clasificada por categoría
- [ ] Al menos 2 features con ventaja clara

**Anti-patrones:**
- ❌ **Comparar marketing:** Lo que dice el sitio vs lo que hace el producto.
- ❌ **Sin priorización:** Features sin peso relativo es ruido.
- ❌ **Ganamos en todo:** Si eso pasa, el análisis es sesgado.

**Template:** Incluido dentro de `TEMPLATE_COMPETITIVE_ANALYSIS.md`

---

### 0.2.4 Pricing Comparison

| Campo | Valor |
|-------|-------|
| **Fase** | 00-Discovery |
| **Subfase** | 0.2 Competitive Analysis |
| **Responsable** | Product Manager |
| **Ejecuta** | Research Agent / Systems Analyst |
| **Aprueba** | Product Owner |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Actualización trimestral |

**Perfil de ejecución:** Tarea de recopilación y normalización de datos de pricing. Requiere acceso a páginas de pricing de competidores y capacidad de normalizar a unidad comparable. En VTT: asignable a Research Agent con web search. El PM debe definir la unidad de normalización (por usuario/mes, por transacción, etc.).

**Qué es:** Comparativa de modelos de pricing: cómo cobran, cuánto por tier, qué incluye cada plan, costo real por usuario/transacción.

**Para qué sirve:** Define el rango de precios aceptable en el mercado. Informa la estrategia de monetización.

**Inputs requeridos:**
- `0.2.2` Competitor List
- Páginas de pricing de competidores
- `0.2.3` Feature Comparison — correlacionar precio con features
- Brief del PM con unidad de normalización

**Dependencias (predecessors):**
- `0.2.2` Competitor List *(obligatorio)*
- `0.2.3` Feature Comparison *(recomendado)*

**Habilita (successors):**
- `1.6.1` Budget Estimate
- `1.6.4` ROI Projection
- `0.4.1` Value Proposition Canvas

**Audiencia:**
- **Product Owner** — modelo de monetización
- **Product Manager** — posicionar pricing

**Criterio de completitud:**
- [ ] Pricing de al menos 3 competidores
- [ ] Costo normalizado por unidad comparable
- [ ] Modelo recomendado con justificación

**Anti-patrones:**
- ❌ **Solo precio de lista:** Descuentos y free tiers cambian el costo real.
- ❌ **Manzanas con naranjas:** Normalizar a unidad comparable.

**Template:** Incluido dentro de `TEMPLATE_COMPETITIVE_ANALYSIS.md`

---

### 0.2.5 SWOT Analysis

| Campo | Valor |
|-------|-------|
| **Fase** | 00-Discovery |
| **Subfase** | 0.2 Competitive Analysis |
| **Responsable** | Product Manager |
| **Ejecuta** | Product Manager / Systems Analyst |
| **Aprueba** | Product Owner |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Actualización semestral |

**Perfil de ejecución:** Tarea de síntesis estratégica que combina datos de múltiples fuentes. El PM puede ejecutar directamente si ya tiene los inputs, o el SA puede proponer un draft que el PM refina. En VTT: un agente SA puede generar un primer draft basado en los datos de 0.2.2, 0.2.3 y reviews, pero el PM debe validar y agregar juicio estratégico.

**Qué es:** SWOT por cada competidor principal. Las debilidades = oportunidades del producto. Las fortalezas = barreras.

**Para qué sirve:** Informa estrategia de posicionamiento. Identifica vulnerabilidades de competidores.

**Inputs requeridos:**
- `0.2.2` Competitor List
- `0.2.3` Feature Comparison
- Reviews de usuarios (quejas = debilidades)
- Info de hiring, funding, noticias

**Dependencias (predecessors):**
- `0.2.2` Competitor List *(obligatorio)*
- `0.2.3` Feature Comparison *(recomendado)*

**Habilita (successors):**
- `0.2.6` Market Opportunities
- `0.4.3` Key Differentiators

**Criterio de completitud:**
- [ ] SWOT para al menos 3 competidores
- [ ] Cada cuadrante con mínimo 2 puntos concretos
- [ ] Debilidades validadas con evidencia

**Anti-patrones:**
- ❌ **SWOT genérico:** "Could improve UX" no es accionable.
- ❌ **Solo S y W:** Oportunidades y amenazas se olvidan frecuentemente.

**Template:** Incluido dentro de `TEMPLATE_COMPETITIVE_ANALYSIS.md`

---

### 0.2.6 Market Opportunities

| Campo | Valor |
|-------|-------|
| **Fase** | 00-Discovery |
| **Subfase** | 0.2 Competitive Analysis |
| **Responsable** | Product Manager |
| **Ejecuta** | Product Manager |
| **Aprueba** | Product Owner |
| **Formato** | Lista priorizada |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Actualización trimestral |

**Perfil de ejecución:** Tarea de síntesis final que integra todos los análisis previos en oportunidades accionables. Requiere visión completa de los deliverables anteriores y juicio estratégico. El PM lo ejecuta directamente — no es delegable porque requiere integrar múltiples inputs y tomar posición. En VTT: un agente puede listar los gaps encontrados en 0.2.3 y 0.2.5, pero la priorización y la declaración de oportunidad la hace el PM.

**Qué es:** Lista priorizada de oportunidades derivadas de gaps competitivos y tendencias. Puente entre análisis y acción.

**Para qué sirve:** Alimenta la propuesta de valor y la definición del MVP.

**Inputs requeridos:**
- `0.2.3` Feature Comparison — gaps de features
- `0.2.5` SWOT Analysis — debilidades de competidores
- `0.1.3` Market Trends
- `0.3.2` User Pain Points

**Dependencias (predecessors):**
- `0.2.3` Feature Comparison *(obligatorio)*
- `0.2.5` SWOT Analysis *(obligatorio)*
- `0.1.3` Market Trends *(recomendado)*

**Habilita (successors):**
- `0.4.1` Value Proposition Canvas
- `0.4.3` Key Differentiators
- `1.2.4` MVP Definition

**Criterio de completitud:**
- [ ] Mínimo 3 oportunidades identificadas
- [ ] Cada una con evidencia del gap
- [ ] Priorización por viabilidad + impacto
- [ ] Al menos 1 que ningún competidor cubre

**Anti-patrones:**
- ❌ **Sin evidencia:** "Creemos que hay oportunidad" sin datos.
- ❌ **Si nadie lo atacó, preguntar por qué:** Puede haber una razón.

**Template:** Incluido dentro de `TEMPLATE_COMPETITIVE_ANALYSIS.md`

---

### 0.2.7 UX Benchmarking

| Campo | Valor |
|-------|-------|
| **Fase** | 00-Discovery |
| **Subfase** | 0.2 Competitive Analysis |
| **Responsable** | Product Manager |
| **Ejecuta** | UX Designer / Design Lead |
| **Aprueba** | Product Owner |
| **Formato** | Report |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 2-3 días |
| **Frecuencia** | Una vez + actualización por release de competidor |

**Perfil de ejecución:** Requiere experiencia en evaluación de UX, capacidad de identificar patrones de interacción, y habilidad para documentar con capturas/grabaciones. No es tarea de research genérico — necesita ojo de diseñador. En VTT: el UX Designer o Design Lead ejecuta el hands-on testing. Un agente puede estructurar el reporte y recopilar screenshots públicos, pero la evaluación de flujos requiere un perfil de diseño.

**Qué es:** Benchmark práctico de la experiencia de usuario de competidores. Documenta flujos clave, puntos de fricción y patrones.

**Para qué sirve:** Copiar lo que funciona, evitar lo que no. Base de referencia para el equipo de diseño.

**Inputs requeridos:**
- Brief del PM con flujos clave a evaluar
- `0.2.2` Competitor List
- Acceso hands-on a productos competidores
- Herramienta de captura de pantalla/grabación

**Dependencias (predecessors):**
- `0.2.2` Competitor List *(obligatorio)*
- `0.2.3` Feature Comparison *(recomendado)*

**Habilita (successors):**
- `3A.1.1` UX Research Plan
- `3A.3.1` Wireframes
- `3A.4.1` UI Style Guide

**Criterio de completitud:**
- [ ] Mínimo 3 competidores evaluados hands-on
- [ ] Al menos 3 flujos clave por competidor
- [ ] Evidencia visual (screenshots/grabaciones)
- [ ] Patrones positivos Y negativos documentados

**Anti-patrones:**
- ❌ **Screenshot sin análisis:** Capturar sin explicar.
- ❌ **Solo estética:** Evaluar solo visual sin flujos ni fricción.
- ❌ **Sin contexto de usuario:** Evaluar desde el equipo, no desde el usuario.

**Template:** `_pm/templates/TEMPLATE_UX_BENCHMARKING.md` *(pendiente)*

---

# 0.3 PROBLEM DEFINITION

**Responsable:** Product Owner  
**Aprueba:** Product Owner  
**Objetivo de subfase:** Definir con precisión qué problema resuelve el producto.

---

### 0.3.1 Problem Statement

| Campo | Valor |
|-------|-------|
| **Fase** | 00-Discovery |
| **Subfase** | 0.3 Problem Definition |
| **Responsable** | Product Owner |
| **Ejecuta** | Product Owner (con input de PM y SA) |
| **Aprueba** | Product Owner |
| **Formato** | 1-2 párrafos |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez (si cambia, es un pivot) |

**Perfil de ejecución:** Este es el deliverable más personal del PO — es su visión del problema cristalizada en palabras. El PM y el SA pueden proveer datos e insights, pero la redacción final es del PO porque refleja su apuesta de negocio. En VTT: un agente puede proponer un draft basado en los datos de 0.1 y 0.2, pero el PO debe reescribirlo con su voz. No es delegable en su versión final.

**Qué es:** Declaración concisa del problema desde la perspectiva del usuario: quién lo tiene, cuál es, cuándo ocurre, qué impacto tiene. El artefacto más corto y más importante del SDLC.

**Para qué sirve:** Ancla del proyecto. Cada feature y decisión se evalúa contra esta declaración.

**Inputs requeridos:**
- `0.1.5` Target Market — para quién es el problema
- Datos de 0.1 y 0.2 — contexto de mercado y competencia
- Observación directa o entrevistas preliminares
- Experiencia del Product Owner en el dominio

**Dependencias (predecessors):**
- `0.1.5` Target Market *(obligatorio)*

**Habilita (successors):**
- `0.3.2` User Pain Points
- `0.3.3` Current Solutions
- `0.3.4` Why Now
- `0.4.1` Value Proposition Canvas
- `1.1.1` Vision Statement
- `1.2.1` Scope Statement
- `2.1.1` Functional Requirements

**Audiencia:**
- Todo el equipo — el "por qué existimos"

**Secciones esperadas:**
Formato recomendado:
> **[Usuarios]** experimentan **[problema]** cuando **[contexto]**. Esto resulta en **[impacto medible]**. Actualmente lo resuelven mediante **[alternativas]**, que son inadecuadas porque **[limitaciones]**.

**Criterio de completitud:**
- [ ] Identifica quién (específico, no genérico)
- [ ] Describe en términos del usuario (no de la solución)
- [ ] Cuantifica el impacto si es posible
- [ ] Cualquier persona del equipo puede parafrasearlo

**Anti-patrones:**
- ❌ **Solución disfrazada:** "No existe una app de X" no es el problema del usuario.
- ❌ **Demasiado amplio:** "La educación es deficiente" no es accionable.
- ❌ **Sin impacto medible:** Sin cuantificación, difícil justificar inversión.

**Template:** `_pm/templates/TEMPLATE_PROBLEM_DEFINITION.md` *(pendiente)*

---

### 0.3.2 User Pain Points

| Campo | Valor |
|-------|-------|
| **Fase** | 00-Discovery |
| **Subfase** | 0.3 Problem Definition |
| **Responsable** | Product Owner |
| **Ejecuta** | UX Researcher / Systems Analyst |
| **Aprueba** | Product Owner |
| **Formato** | Lista priorizada |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Una vez + post user research |

**Perfil de ejecución:** Requiere habilidades de entrevista con usuarios, análisis cualitativo y empatía para entender dolores reales (no los que el equipo asume). En VTT: asignable a un UX Researcher o SA con experiencia en discovery. El PO provee el Problem Statement y acceso a usuarios del target market. Un agente puede analizar reviews y quejas de competidores como fuente secundaria.

**Qué es:** Lista priorizada de dolores específicos del usuario. Cada pain point es una manifestación concreta del problema general.

**Para qué sirve:** Descompone el problema en piezas accionables. Cada pain point mapea a features.

**Inputs requeridos:**
- `0.3.1` Problem Statement
- Guía de entrevista preparada
- Acceso a usuarios del target market (5-10)
- Reviews y quejas de productos competidores

**Dependencias (predecessors):**
- `0.3.1` Problem Statement *(obligatorio)*
- `0.1.5` Target Market *(obligatorio)*

**Habilita (successors):**
- `0.3.5` Problem Validation
- `0.4.1` Value Proposition Canvas
- `2.1.1` Functional Requirements
- `3A.1.2` User Personas

**Criterio de completitud:**
- [ ] Mínimo 5 pain points
- [ ] Priorizados por severidad × frecuencia
- [ ] Al menos 3 validados con usuarios reales
- [ ] Escritos desde la perspectiva del usuario

**Anti-patrones:**
- ❌ **Inventados:** El equipo asume sin preguntar al usuario.
- ❌ **Feature requests:** "Necesito un botón" es feature; "pierdo 30 min copiando" es pain.
- ❌ **Solo funcionales:** Dolores emocionales también son válidos.

**Template:** Incluido dentro de `TEMPLATE_PROBLEM_DEFINITION.md`

---

### 0.3.3 Current Solutions

| Campo | Valor |
|-------|-------|
| **Fase** | 00-Discovery |
| **Subfase** | 0.3 Problem Definition |
| **Responsable** | Product Owner |
| **Ejecuta** | Systems Analyst / Research Agent |
| **Aprueba** | Product Owner |
| **Formato** | Lista |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere capacidad de mapear flujos de trabajo existentes — tanto soluciones formales (productos) como informales (workarounds, procesos manuales). El SA puede hacer este mapeo a partir de entrevistas con usuarios o de los datos de 0.3.2. En VTT: un agente SA puede documentar las soluciones formales (competidores ya listados en 0.2.2) y un Research Agent puede investigar workarounds mencionados en reviews/foros.

**Qué es:** Documentación de cómo los usuarios resuelven el problema HOY — con o sin tecnología.

**Para qué sirve:** La solución actual es la competencia real. El producto debe ser significativamente mejor que el workaround actual.

**Inputs requeridos:**
- `0.3.2` User Pain Points — revelan workarounds
- Entrevistas sobre flujos actuales
- `0.2.2` Competitor List — soluciones formales

**Dependencias (predecessors):**
- `0.3.1` Problem Statement *(obligatorio)*
- `0.3.2` User Pain Points *(recomendado)*

**Habilita (successors):**
- `0.4.1` Value Proposition Canvas
- `0.4.2` UVP Statement
- `1.2.4` MVP Definition

**Criterio de completitud:**
- [ ] Al menos 3 soluciones documentadas (incluyendo "no hacer nada")
- [ ] Pros y contras de cada una
- [ ] Gap entre solución actual y solución ideal

**Anti-patrones:**
- ❌ **Ignorar workarounds:** Spreadsheets y WhatsApp compiten con tu producto.
- ❌ **"No hay solución actual":** Siempre la hay.

**Template:** Incluido dentro de `TEMPLATE_PROBLEM_DEFINITION.md`

---

### 0.3.4 Why Now

| Campo | Valor |
|-------|-------|
| **Fase** | 00-Discovery |
| **Subfase** | 0.3 Problem Definition |
| **Responsable** | Product Owner |
| **Ejecuta** | Product Owner (con datos del PM) |
| **Aprueba** | Product Owner |
| **Formato** | 1 párrafo |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Al igual que el Problem Statement, este es un deliverable de juicio estratégico del PO. Los datos vienen de 0.1.3 Market Trends, pero la argumentación del timing es una decisión de negocio. En VTT: un agente puede compilar los cambios recientes relevantes del mercado, pero el PO articula por qué esos cambios crean la ventana de oportunidad.

**Qué es:** Argumentación de por qué este es el momento correcto para resolver el problema.

**Para qué sirve:** Responde: "Si existe hace años, ¿qué cambió?" Sin "why now" convincente, el timing es cuestionable.

**Inputs requeridos:**
- `0.1.3` Market Trends — cambios recientes
- Cambios tecnológicos, regulatorios, de comportamiento

**Dependencias (predecessors):**
- `0.3.1` Problem Statement *(obligatorio)*
- `0.1.3` Market Trends *(obligatorio)*

**Habilita (successors):**
- `0.4.1` Value Proposition Canvas
- `1.1.1` Vision Statement

**Criterio de completitud:**
- [ ] Al menos 2 cambios recientes concretos
- [ ] Explica por qué no era viable antes
- [ ] Convincente para alguien externo

**Anti-patrones:**
- ❌ **"La tecnología existe":** Necesita un hecho específico y reciente.
- ❌ **Sin urgencia:** Si funciona igual en 5 años, no hay "why now."

**Template:** Incluido dentro de `TEMPLATE_PROBLEM_DEFINITION.md`

---

### 0.3.5 Problem Validation

| Campo | Valor |
|-------|-------|
| **Fase** | 00-Discovery |
| **Subfase** | 0.3 Problem Definition |
| **Responsable** | Product Owner |
| **Ejecuta** | UX Researcher / Systems Analyst |
| **Aprueba** | Product Owner |
| **Formato** | Report |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 3-5 días |
| **Frecuencia** | Una vez (pre-inversión) |

**Perfil de ejecución:** Requiere habilidades de investigación cualitativa: diseño de guías de entrevista, conducción de entrevistas sin sesgo, análisis temático de hallazgos, y redacción de conclusiones basadas en evidencia. En VTT: asignable a UX Researcher o SA con experiencia en user research. Necesita acceso a usuarios reales del target market — esto no es automatizable con agentes porque requiere interacción humana real. Un agente puede diseñar la guía de entrevista y analizar las transcripciones post-entrevista.

**Qué es:** Reporte que valida el problema con usuarios reales. Gate de go/no-go más importante.

**Para qué sirve:** Hasta aquí todo es hipótesis. Este documento confirma o desmiente con datos reales.

**Inputs requeridos:**
- `0.3.1` Problem Statement — hipótesis a validar
- `0.3.2` User Pain Points — dolores a confirmar
- `0.1.5` Target Market — a quién entrevistar
- Acceso a 5-15 usuarios del mercado objetivo
- Guía de entrevista diseñada

**Dependencias (predecessors):**
- `0.3.1` Problem Statement *(obligatorio)*
- `0.3.2` User Pain Points *(obligatorio)*
- `0.1.5` Target Market *(obligatorio)*

**Habilita (successors):**
- `0.4.1` Value Proposition Canvas — basado en problema validado
- `1.2.4` MVP Definition
- Decisión go/no-go de fase 0

**Audiencia:**
- **Product Owner** — decisión go/no-go
- **Investors** — evidencia de que el problema existe
- Todo el equipo — confianza

**Secciones esperadas:**
1. Metodología (cuántos, quiénes, cómo)
2. Perfil de participantes (anonimizado)
3. Hallazgos clave agrupados por tema
4. Citas textuales representativas
5. Cuantificación del dolor
6. Pain points confirmados vs no confirmados
7. Insights inesperados
8. Conclusión go/no-go/pivot

**Criterio de completitud:**
- [ ] Mínimo 5 usuarios participaron
- [ ] Metodología documentada y reproducible
- [ ] Al menos 3 pain points confirmados
- [ ] Conclusión explícita go/no-go/pivot
- [ ] Product Owner tomó decisión basada en hallazgos

**Anti-patrones:**
- ❌ **Preguntas leading:** "¿No te gustaría...?" no valida.
- ❌ **Sample sesgado:** Solo amigos o believers.
- ❌ **Validación post-hoc:** Decidir construir y luego buscar confirmación.
- ❌ **Ignorar invalidación:** Si 4/5 dicen que no, eso es un hallazgo válido.

**Template:** `_pm/templates/TEMPLATE_PROBLEM_VALIDATION.md` *(pendiente)*

---

# 0.4 VALUE PROPOSITION

**Responsable:** Product Owner  
**Aprueba:** Product Owner  
**Objetivo de subfase:** Definir qué nos hace únicos y por qué el usuario nos elegiría.

---

### 0.4.1 Value Proposition Canvas

| Campo | Valor |
|-------|-------|
| **Fase** | 00-Discovery |
| **Subfase** | 0.4 Value Proposition |
| **Responsable** | Product Owner |
| **Ejecuta** | Product Owner + Product Manager (workshop) |
| **Aprueba** | Product Owner |
| **Formato** | Template (Canvas) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez + por pivot |

**Perfil de ejecución:** Se ejecuta idealmente como workshop colaborativo entre PO y PM, con input del Design Lead. Requiere capacidad de facilitación y síntesis. En VTT: un agente puede pre-llenar el canvas con los datos de 0.3.1, 0.3.2 y 0.2.6 como punto de partida, pero el mapeo pain→reliever y la priorización requieren juicio humano del PO y PM trabajando juntos.

**Qué es:** Framework de Strategyzer: perfil del cliente (jobs, pains, gains) vs propuesta de valor (products/services, pain relievers, gain creators).

**Para qué sirve:** Fuerza articulación explícita de cómo el producto crea valor, mapeado 1:1 contra dolores del usuario.

**Inputs requeridos:**
- `0.3.1` Problem Statement
- `0.3.2` User Pain Points — dolores validados
- `0.3.3` Current Solutions
- `0.2.6` Market Opportunities
- `0.3.5` Problem Validation

**Dependencias (predecessors):**
- `0.3.1` Problem Statement *(obligatorio)*
- `0.3.2` User Pain Points *(obligatorio)*
- `0.3.5` Problem Validation *(obligatorio)*

**Habilita (successors):**
- `0.4.2` UVP Statement
- `0.4.3` Key Differentiators
- `0.4.5` Value Hypothesis
- `1.2.4` MVP Definition
- `2.1.1` Functional Requirements

**Criterio de completitud:**
- [ ] Lado cliente: al menos 5 jobs, 5 pains, 5 gains
- [ ] Lado producto: al menos 3 pain relievers, 3 gain creators
- [ ] Cada reliever mapeado a un pain específico
- [ ] Basado en datos validados, no suposiciones

**Anti-patrones:**
- ❌ **Canvas genérico:** Frases tipo "mejorar experiencia" sin especificidad.
- ❌ **Solution-first:** Empezar por el producto y forzar los pains.
- ❌ **Canvas estático:** No actualizarlo con nueva información.

**Template:** `_pm/templates/TEMPLATE_VALUE_PROPOSITION_CANVAS.md` *(pendiente)*

---

### 0.4.2 UVP Statement

| Campo | Valor |
|-------|-------|
| **Fase** | 00-Discovery |
| **Subfase** | 0.4 Value Proposition |
| **Responsable** | Product Owner |
| **Ejecuta** | Product Owner |
| **Aprueba** | Product Owner |
| **Formato** | 1 frase |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Una vez + por pivot |

**Perfil de ejecución:** El PO lo escribe directamente — es la destilación máxima de su visión. En VTT: un agente puede proponer 3-5 opciones de UVP basado en el canvas, pero el PO selecciona y refina la versión final. La frase final debe salir de la cabeza del PO.

**Qué es:** Una frase que comunica la propuesta de valor única.

**Para qué sirve:** Fuerza claridad absoluta. Se usa en pitch, landing page, onboarding y como filtro de priorización.

**Inputs requeridos:**
- `0.4.1` Value Proposition Canvas
- `0.4.3` Key Differentiators

**Dependencias (predecessors):**
- `0.4.1` Value Proposition Canvas *(obligatorio)*

**Habilita (successors):**
- `1.1.1` Vision Statement
- Landing page, pitch deck

**Secciones esperadas:**
Formato: **[Producto]** ayuda a **[usuario]** a **[resultado]** mediante **[mecanismo diferenciador]**, a diferencia de **[alternativas]** que **[limitación]**.

**Criterio de completitud:**
- [ ] Una sola frase (máximo 2)
- [ ] Menciona usuario, beneficio y diferenciador
- [ ] Alguien externo entiende de qué se trata

**Anti-patrones:**
- ❌ **Feature como UVP:** "Usamos IA" → resultado: "Profesores recuperan 6 hrs."
- ❌ **Buzzword bingo:** "Plataforma innovadora disruptiva" no comunica nada.
- ❌ **Aplica a competidores:** Si reemplazas el nombre y funciona, no es única.

**Template:** Incluido dentro de `TEMPLATE_VALUE_PROPOSITION_CANVAS.md`

---

### 0.4.3 Key Differentiators

| Campo | Valor |
|-------|-------|
| **Fase** | 00-Discovery |
| **Subfase** | 0.4 Value Proposition |
| **Responsable** | Product Owner |
| **Ejecuta** | Product Owner + Product Manager |
| **Aprueba** | Product Owner |
| **Formato** | Lista (3-5 ítems) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Una vez + revisión trimestral |

**Perfil de ejecución:** Tarea de síntesis estratégica conjunta entre PO (visión de negocio) y PM (datos competitivos). Requiere combinar los insights del canvas con la feature comparison para identificar ventajas sostenibles. En VTT: un agente puede listar los gaps de 0.2.3 y proponer diferenciadores candidatos, pero la selección final (qué es realmente sostenible) es decisión PO+PM.

**Qué es:** 3-5 ventajas estratégicas sostenibles que diferencian al producto. No features — ventajas difíciles de copiar.

**Para qué sirve:** Define el "moat." Guía inversión de recursos y messaging.

**Inputs requeridos:**
- `0.4.1` Value Proposition Canvas
- `0.2.3` Feature Comparison
- `0.2.6` Market Opportunities
- `0.2.5` SWOT Analysis

**Dependencias (predecessors):**
- `0.4.1` Value Proposition Canvas *(obligatorio)*
- `0.2.3` Feature Comparison *(obligatorio)*

**Habilita (successors):**
- `0.4.2` UVP Statement
- `1.2.4` MVP Definition
- `3B.1.1` System Architecture

**Criterio de completitud:**
- [ ] 3-5 diferenciadores
- [ ] Cada uno verificable (métrica, no adjetivo)
- [ ] Cada uno con explicación de sostenibilidad
- [ ] Validados contra feature comparison

**Anti-patrones:**
- ❌ **"Mejor UX":** No es sostenible ni verificable.
- ❌ **Copiables:** Si se replica en 3 meses, no es moat.
- ❌ **Más de 5:** Si tienes 10, no tienes ninguno.

**Template:** Incluido dentro de `TEMPLATE_VALUE_PROPOSITION_CANVAS.md`

---

### 0.4.4 Target Customer Profile

| Campo | Valor |
|-------|-------|
| **Fase** | 00-Discovery |
| **Subfase** | 0.4 Value Proposition |
| **Responsable** | Product Owner |
| **Ejecuta** | UX Designer / UX Researcher |
| **Aprueba** | Product Owner |
| **Formato** | Descripción |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez + refinamiento post research |

**Perfil de ejecución:** Requiere habilidades de síntesis de research de usuarios en un perfil narrativo. El UX Designer/Researcher construye el perfil a partir de los datos de entrevistas y el target market. En VTT: un agente puede generar un primer draft del perfil basado en los datos de 0.1.5, 0.3.2 y 0.3.5, pero debe ser validado con el UX Designer y el PO para confirmar que refleja la realidad observada en las entrevistas.

**Qué es:** Perfil detallado del cliente ideal — demografía, comportamiento, motivaciones, frustraciones. Predecesor de User Personas.

**Para qué sirve:** Pone cara al usuario. "¿[María] necesita esto?" en vez de "¿el mercado necesita esto?"

**Inputs requeridos:**
- `0.1.5` Target Market
- `0.3.2` User Pain Points
- `0.3.5` Problem Validation
- Datos de entrevistas con usuarios

**Dependencias (predecessors):**
- `0.1.5` Target Market *(obligatorio)*
- `0.3.2` User Pain Points *(obligatorio)*

**Habilita (successors):**
- `3A.1.2` User Personas
- `3A.1.3` User Journey Maps
- `1.3.4` Communication Plan

**Secciones esperadas:**
1. Demographics (edad, rol, ubicación)
2. Contexto profesional
3. Objetivos
4. Frustraciones
5. Comportamiento digital
6. Criterios de decisión de compra
7. Quote representativa

**Criterio de completitud:**
- [ ] Basado en datos reales (entrevistas)
- [ ] Suficientemente específico para distinguir de otros perfiles
- [ ] El equipo puede responder "¿[perfil] haría X?" sin preguntar

**Anti-patrones:**
- ❌ **Aspiracional:** El cliente que quieres vs el que realmente comprará.
- ❌ **Solo demografía:** Comportamiento y motivaciones diferencian más.
- ❌ **Sin datos:** Perfil inventado sin hablar con usuarios.

**Template:** `_pm/templates/TEMPLATE_CUSTOMER_PROFILE.md` *(pendiente)*

---

### 0.4.5 Value Hypothesis

| Campo | Valor |
|-------|-------|
| **Fase** | 00-Discovery |
| **Subfase** | 0.4 Value Proposition |
| **Responsable** | Product Owner |
| **Ejecuta** | Product Owner + Product Manager |
| **Aprueba** | Product Owner |
| **Formato** | Lista |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Una vez + revisión post-MVP |

**Perfil de ejecución:** Requiere pensamiento científico: formular hipótesis falseables, definir métricas y umbrales, y diseñar cómo testear con el MVP. Es tarea conjunta PO+PM. En VTT: un agente puede proponer hipótesis candidatas derivadas del canvas (cada pain reliever es una hipótesis implícita), pero el PO y PM deben definir las métricas y umbrales porque eso determina qué significa éxito o fracaso.

**Qué es:** Lista de hipótesis testables sobre por qué el producto creará valor. Formato: "Creemos que [acción] resultará en [resultado] para [usuario]."

**Para qué sirve:** Transforma supuestos en hipótesis explícitas. El MVP se diseña para validarlas.

**Inputs requeridos:**
- `0.4.1` Value Proposition Canvas
- `0.3.5` Problem Validation
- `0.4.3` Key Differentiators

**Dependencias (predecessors):**
- `0.4.1` Value Proposition Canvas *(obligatorio)*
- `0.3.5` Problem Validation *(obligatorio)*

**Habilita (successors):**
- `1.2.4` MVP Definition
- `1.1.4` Success Metrics
- `5.x` Testing

**Secciones esperadas:**
3-7 hipótesis, cada una con:
1. Hipótesis ("Creemos que... resultará en... para...")
2. Métrica de validación
3. Umbral de éxito (número concreto)
4. Cómo se testea (qué parte del MVP)
5. Riesgo si es falsa

**Criterio de completitud:**
- [ ] 3-7 hipótesis documentadas
- [ ] Cada una falseable
- [ ] Cada una con métrica y umbral numérico
- [ ] Priorizadas por riesgo

**Anti-patrones:**
- ❌ **No falseable:** "El producto será útil" no se puede probar falsa.
- ❌ **Sin métrica:** Hipótesis sin medición es un deseo.
- ❌ **Solo seguras:** Las riesgosas son las que más necesitan validación.

**Template:** Incluido dentro de `TEMPLATE_VALUE_PROPOSITION_CANVAS.md`

---

# ÍNDICE DE DEPENDENCIAS — FASE 0

```
0.1.1 Market Research Report
  └─► 0.1.2, 0.1.3, 0.1.4, 0.2.1, 0.3.1, 1.2.1

0.1.2 TAM/SAM/SOM
  └─► 0.4.1, 1.6.1, 1.6.4

0.1.3 Market Trends
  └─► 0.2.6, 0.3.4, 0.4.4

0.1.4 Market Segments
  └─► 0.1.5, 0.2.1, 0.4.4

0.1.5 Target Market
  └─► 0.2.1, 0.2.2, 0.3.1, 0.3.2, 0.4.4, 1.2.4

0.2.1 Competitive Analysis Doc
  └─► 0.2.3, 0.2.6, 0.4.1, 0.4.3, 1.2.4

0.2.2 Competitor List
  └─► 0.2.1, 0.2.3, 0.2.4, 0.2.5, 0.2.7

0.2.3 Feature Comparison
  └─► 0.2.6, 0.4.3, 1.2.4, 2.1.1

0.2.4 Pricing Comparison
  └─► 1.6.1, 1.6.4, 0.4.1

0.2.5 SWOT Analysis
  └─► 0.2.6, 0.4.3

0.2.6 Market Opportunities
  └─► 0.4.1, 0.4.3, 1.2.4

0.2.7 UX Benchmarking
  └─► 3A.1.1, 3A.3.1, 3A.4.1

0.3.1 Problem Statement
  └─► 0.3.2, 0.3.3, 0.3.4, 0.4.1, 1.1.1, 1.2.1, 2.1.1

0.3.2 User Pain Points
  └─► 0.3.5, 0.4.1, 2.1.1, 3A.1.2

0.3.3 Current Solutions
  └─► 0.4.1, 0.4.2, 1.2.4

0.3.4 Why Now
  └─► 0.4.1, 1.1.1

0.3.5 Problem Validation
  └─► 0.4.1, 1.2.4, go/no-go gate

0.4.1 Value Proposition Canvas
  └─► 0.4.2, 0.4.3, 0.4.5, 1.2.4, 2.1.1

0.4.2 UVP Statement
  └─► 1.1.1, landing page, pitch deck

0.4.3 Key Differentiators
  └─► 0.4.2, 1.2.4, 3B.1.1

0.4.4 Target Customer Profile
  └─► 3A.1.2, 3A.1.3, 1.3.4

0.4.5 Value Hypothesis
  └─► 1.2.4, 1.1.4, 5.x
```

---

# RESUMEN DE EJECUTORES — FASE 0

| Deliverable | Responsable | Ejecuta | Delegable a agente VTT |
|-------------|-------------|---------|------------------------|
| 0.1.1 Market Research Report | PM | Research Agent / SA | ✅ Sí — con brief del PM |
| 0.1.2 TAM/SAM/SOM | PM | Research Agent / SA | ✅ Sí — con criterios de filtrado |
| 0.1.3 Market Trends | PM | Research Agent / SA | ✅ Sí — con sector y horizonte |
| 0.1.4 Market Segments | PM | Research Agent / SA / PM | 🔶 Parcial — recopila datos, PM prioriza |
| 0.1.5 Target Market | PM | PM | ❌ No — decisión estratégica |
| 0.2.1 Competitive Analysis Doc | PM | Research Agent / SA | ✅ Sí — con brief y target |
| 0.2.2 Competitor List | PM | Research Agent | ✅ Sí — recopilación pura |
| 0.2.3 Feature Comparison | PM | SA + UX Designer | 🔶 Parcial — matriz sí, hands-on testing no |
| 0.2.4 Pricing Comparison | PM | Research Agent / SA | ✅ Sí — recopilación + normalización |
| 0.2.5 SWOT Analysis | PM | PM / SA | 🔶 Parcial — draft sí, juicio estratégico no |
| 0.2.6 Market Opportunities | PM | PM | ❌ No — síntesis estratégica |
| 0.2.7 UX Benchmarking | PM | UX Designer / Design Lead | ❌ No — requiere evaluación hands-on |
| 0.3.1 Problem Statement | PO | PO (con input PM/SA) | 🔶 Parcial — draft sí, versión final no |
| 0.3.2 User Pain Points | PO | UX Researcher / SA | 🔶 Parcial — análisis de reviews sí, entrevistas no |
| 0.3.3 Current Solutions | PO | SA / Research Agent | ✅ Sí — mapeo de soluciones existentes |
| 0.3.4 Why Now | PO | PO (con datos del PM) | 🔶 Parcial — compilar datos sí, argumentar no |
| 0.3.5 Problem Validation | PO | UX Researcher / SA | 🔶 Parcial — guía y análisis sí, entrevistas no |
| 0.4.1 Value Proposition Canvas | PO | PO + PM (workshop) | 🔶 Parcial — pre-llenado sí, mapeo final no |
| 0.4.2 UVP Statement | PO | PO | ❌ No — destilación personal del PO |
| 0.4.3 Key Differentiators | PO | PO + PM | 🔶 Parcial — candidatos sí, selección no |
| 0.4.4 Target Customer Profile | PO | UX Designer / Researcher | ✅ Sí — con datos de entrevistas |
| 0.4.5 Value Hypothesis | PO | PO + PM | 🔶 Parcial — candidatos sí, métricas/umbrales no |

---

**Documento:** DICCIONARIO_FASE_00_DISCOVERY.md  
**Versión:** 1.1.0  
**Estado:** ✅ Listo para revisión  
**Siguiente:** DICCIONARIO_FASE_01_PLANNING.md
