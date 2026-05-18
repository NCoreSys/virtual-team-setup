# 🔍 TEMPLATE BASE — SPEC SEMANTIC SEARCH (Búsqueda Vectorial/IA)

> **Versión:** 2.0 (Estandarizada para agentes)  
> **Tipo:** P2 — Enterprise/Scale (AI-powered)  
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

- ✅ **Búsqueda semántica** con embeddings vectoriales
- ✅ **Búsqueda por similitud** (cosine, dot product)
- ✅ **RAG interfaces** (Retrieval Augmented Generation)
- ✅ **Knowledge base search** con relevance scoring
- ✅ **Búsqueda híbrida** (keyword + semantic)
- ✅ **Búsqueda de imágenes** por descripción
- ❌ Búsqueda keyword tradicional → usar DataGrid con filtros
- ❌ Autocomplete simple → usar componente en AppScreen
- ❌ Filtros sin relevance scoring → usar DataGrid

---

# ESPECIFICACIÓN DE BÚSQUEDA SEMÁNTICA

---

## 0) Metadatos del documento [OBL]

> **Activación:** Siempre obligatorio.

| Campo | Valor |
|-------|-------|
| **Nombre del documento** | Spec_SemanticSearch_{{NOMBRE}}_{{VERSION}} |
| **Proyecto** | {{NOMBRE_PROYECTO}} |
| **Módulo / Feature** | {{MODULO}} |
| **Búsqueda** | {{NOMBRE_BUSQUEDA}} |
| **ID técnico** | `search-{{NUM}}-{{SLUG}}` (ej: `search-01-kb-semantic`) |
| **Ruta** | {{RUTA}} (ej: `/search`, `/kb/search`) |
| **Versión** | {{VERSION}} |
| **Estado** | [Elegir: Draft / Review / Approved / Deprecated] |
| **Prioridad** | [Elegir: Crítica / Alta / Media / Baja] |
| **Fecha** | {{FECHA_YYYY-MM-DD}} |
| **Owner (PM/PO)** | {{NOMBRE_OWNER}} |
| **AI/ML Owner** | {{NOMBRE_ML}} |
| **UX/UI Owner** | {{NOMBRE_UX}} |
| **Tech Lead** | {{NOMBRE_TECH}} |
| **QA Owner** | {{NOMBRE_QA}} |

---

## 1) Propósito de la búsqueda [OBL]

> **Activación:** Siempre obligatorio.

### 1.1 Descripción general [OBL]

Esta búsqueda permite a **{{TIPO_USUARIO}}** encontrar **{{TIPO_CONTENIDO}}** usando búsqueda semántica basada en embeddings vectoriales.

| Campo | Valor |
|-------|-------|
| **Tipo de búsqueda** | [Elegir: Semántica pura / Híbrida (keyword + semantic) / Multi-modal] |
| **Contenido indexado** | {{CONTENIDO}} (ej: documentos, productos, imágenes, código) |
| **Volumen del índice** | {{NUM}} documentos/items |

### 1.2 Objetivo de negocio [OBL]

1. {{OBJETIVO_1}} (ej: Encontrar contenido relevante por intención, no solo keywords)
2. {{OBJETIVO_2}} (ej: Reducir "búsquedas sin resultados")
3. {{OBJETIVO_3}} (ej: Descubrir contenido relacionado semánticamente)

### 1.3 Objetivo UX [OBL]

- Resultados relevantes sin requerir keywords exactos
- Transparencia en el scoring (por qué este resultado)
- Performance rápida (<500ms percibido)
- Feedback claro cuando no hay resultados relevantes

### 1.4 KPIs [OBL]

| Métrica | Valor objetivo | Valor crítico |
|---------|----------------|---------------|
| MRR (Mean Reciprocal Rank) | > {{VALOR}} | < {{VALOR}} |
| Precision@K (K={{NUM}}) | > {{VALOR}}% | < {{VALOR}}% |
| Click-through rate | > {{VALOR}}% | < {{VALOR}}% |
| Zero-result rate | < {{VALOR}}% | > {{VALOR}}% |
| Query latency (p95) | < {{VALOR}}ms | > {{VALOR}}ms |
| User satisfaction | > {{VALOR}}/5 | < {{VALOR}}/5 |

---

## 2) Alcance (Scope) [OBL]

> **Activación:** Siempre obligatorio.

### 2.1 Incluye (In Scope) [OBL]

- {{INCLUYE_1}} (ej: Búsqueda semántica por texto natural)
- {{INCLUYE_2}} (ej: Relevance scoring con visualización)
- {{INCLUYE_3}} (ej: Filtros por categoría/tipo/calidad)
- {{INCLUYE_4}} (ej: Match highlighting)
- {{INCLUYE_5}} (ej: Performance metrics visibles)

### 2.2 No incluye (Out of Scope) [OBL]

- {{EXCLUYE_1}}
- {{EXCLUYE_2}}

### 2.3 Dependencias [OBL]

| Tipo | Dependencia | Estado | Owner |
|------|-------------|--------|-------|
| Embedding model | {{MODELO}} (ej: bge-small-en-v1.5, text-embedding-3-small) | [Pendiente/Listo] | {{OWNER}} |
| Vector DB | {{DB}} (ej: Pinecone, Weaviate, Qdrant, pgvector) | [Pendiente/Listo] | {{OWNER}} |
| Index pipeline | {{PIPELINE}} | [Pendiente/Listo] | {{OWNER}} |
| Content source | {{FUENTE}} | [Pendiente/Listo] | {{OWNER}} |

---

## 3) Modelo de embeddings y vectores [OBL] — **SECCIÓN NÚCLEO**

> **Activación:** Siempre obligatorio. Define la configuración técnica de IA.

### 3.1 Modelo de embeddings [OBL]

| Campo | Valor |
|-------|-------|
| **Modelo** | {{MODELO}} (ej: `bge-small-en-v1.5`, `text-embedding-3-small`) |
| **Provider** | [Elegir: OpenAI / Cohere / HuggingFace / Self-hosted] |
| **Dimensiones** | {{NUM}} dims (ej: 384, 1536) |
| **Max tokens** | {{NUM}} tokens |
| **Idiomas soportados** | {{IDIOMAS}} |

### 3.2 Vector database [OBL]

| Campo | Valor |
|-------|-------|
| **Base de datos** | {{DB}} |
| **Índice** | [Elegir: HNSW / IVF / Flat / Annoy] |
| **Métrica de similitud** | [Elegir: Cosine / Dot product / Euclidean] |
| **Parámetros del índice** | {{PARAMS}} (ej: `ef_construction=200, M=16`) |

### 3.3 Chunking strategy [OBL]

| Campo | Valor |
|-------|-------|
| **Estrategia** | [Elegir: Fixed size / Semantic / Sentence / Paragraph] |
| **Chunk size** | {{NUM}} tokens/caracteres |
| **Overlap** | {{NUM}} tokens/caracteres |
| **Metadata por chunk** | {{METADATA}} (ej: doc_id, section, page) |

### 3.4 Campos indexados [OBL]

| Campo | Tipo | Vectorizado | Filtrable | Peso |
|-------|------|-------------|-----------|------|
| `title` | string | Sí | No | {{PESO}} |
| `content` | text | Sí | No | {{PESO}} |
| `summary` | text | Sí | No | {{PESO}} |
| `category` | enum | No | Sí | — |
| `tags` | array | No | Sí | — |
| `quality_score` | float | No | Sí | — |
| `{{CAMPO}}` | {{TIPO}} | Sí/No | Sí/No | {{PESO}} |

---

## 4) Query y retrieval [OBL]

> **Activación:** Siempre obligatorio.

### 4.1 Proceso de query [OBL]

```
User Query → [Preprocesamiento] → [Embedding] → [Vector Search] → [Reranking] → [Resultados]
```

| Paso | Descripción | Latencia objetivo |
|------|-------------|-------------------|
| Preprocesamiento | Normalizar, expandir query | < {{MS}}ms |
| Embedding | Generar vector de query | < {{MS}}ms |
| Vector search | Buscar en índice | < {{MS}}ms |
| Reranking | Reordenar por relevancia | < {{MS}}ms |
| Total | End-to-end | < {{MS}}ms |

### 4.2 Parámetros de búsqueda [OBL]

| Parámetro | Valor default | Configurable | Descripción |
|-----------|---------------|--------------|-------------|
| `top_k` | {{NUM}} | Sí/No | Número de resultados a recuperar |
| `min_score` | {{VALOR}} | Sí/No | Score mínimo de relevancia |
| `rerank` | true/false | Sí/No | Aplicar reranking |
| `hybrid_alpha` | {{VALOR}} | Sí/No | Peso keyword vs semantic (si híbrido) |

### 4.3 Búsqueda híbrida [COND]

> **Activación:** Incluir si se usa búsqueda híbrida (keyword + semantic).

| Campo | Valor |
|-------|-------|
| **Keyword search** | [BM25 / Full-text / Elasticsearch] |
| **Fusión** | [Elegir: RRF / Linear / Weighted] |
| **Alpha (semantic weight)** | {{VALOR}} (0 = solo keyword, 1 = solo semantic) |

### 4.4 Reranking [COND]

> **Activación:** Incluir si se usa reranker.

| Campo | Valor |
|-------|-------|
| **Modelo reranker** | {{MODELO}} (ej: `bge-reranker-base`, `cohere-rerank`) |
| **Top N para rerank** | {{NUM}} |
| **Score threshold** | {{VALOR}} |

---

## 5) Resultados de búsqueda [OBL] — **SECCIÓN NÚCLEO**

> **Activación:** Siempre obligatorio.

### 5.1 Estructura de resultado [OBL]

| Campo | Tipo | Descripción | Visible |
|-------|------|-------------|---------|
| `id` | string | ID del documento | No |
| `title` | string | Título del resultado | Sí |
| `excerpt` | string | Fragmento con highlights | Sí |
| `url` / `deep_link` | string | Link al detalle | Sí |
| `relevance_score` | float (0-1) | Score de similitud | Sí |
| `quality_score` | float (0-1) | Score de calidad del doc | Sí/No |
| `match_fields` | array | Campos donde hubo match | Sí |
| `category` | string | Categoría/tipo | Sí |
| `tags` | array | Tags del documento | Sí |
| `thumbnail` | string | Imagen preview | Sí/No |
| `metadata` | object | Metadata adicional | Parcial |

### 5.2 Visualización del relevance score [OBL]

| Rango | Label | Color | Descripción |
|-------|-------|-------|-------------|
| 90-100% | "Alta relevancia" | Verde | Match muy fuerte |
| 75-89% | "Buena relevancia" | Azul/Verde claro | Match bueno |
| 60-74% | "Relevancia media" | Amarillo | Match parcial |
| < 60% | "Baja relevancia" | Gris | Match débil (o no mostrar) |

| Elemento visual | Implementación |
|-----------------|----------------|
| Badge con % | "📊 94% relevancia" |
| Barra de progreso | Barra con fill proporcional |
| Estrellas | ★★★★☆ |
| Tooltip | "Similitud coseno: 0.94" |

### 5.3 Match highlighting [OBL]

| Campo | Valor |
|-------|-------|
| Tag de highlight | `<em>` o `<mark>` |
| Contexto alrededor | {{NUM}} caracteres |
| Max highlights por resultado | {{NUM}} |
| Campos con highlight | {{CAMPOS}} |

### 5.4 Match fields ("Match en:") [OBL]

| Campo | Valor |
|-------|-------|
| Mostrar campos | Sí |
| Formato | "Match en: **title**, **content**" |
| Máximo campos | {{NUM}} |

---

## 6) UI de búsqueda [OBL]

> **Activación:** Siempre obligatorio.

### 6.1 Estructura de la página [OBL]

```
┌─────────────────────────────────────────────────────┐
│  SEARCH HERO                                        │
│  [Título] [Descripción]                             │
│  [═══════════════════════════════] [🔍 Buscar]     │
│  Filtros: [Categoría ▼] [Tipo ▼] [Quality mín: __] │
├─────────────────────────────────────────────────────┤
│  RESULTS HEADER                                     │
│  12 resultados para "query" · query: 23ms · search: 4ms │
├─────────────────────────────────────────────────────┤
│  RESULT CARD 1                              [Ver →] │
│  [Thumb] [Title] [Domain]     [📊 94% relevancia]  │
│          [Tags] [Quality: 0.95]                     │
│          Match en: title, content                   │
│          Excerpt with <em>highlights</em>...        │
├─────────────────────────────────────────────────────┤
│  RESULT CARD 2                              [Ver →] │
│  ...                                                │
├─────────────────────────────────────────────────────┤
│  PAGINATION / LOAD MORE                             │
├─────────────────────────────────────────────────────┤
│  TECH NOTE                                          │
│  Modelo: bge-small-en-v1.5 · Índice: HNSW          │
└─────────────────────────────────────────────────────┘
```

### 6.2 Search input [OBL]

| Campo | Valor |
|-------|-------|
| Placeholder | "{{PLACEHOLDER}}" (ej: "Describe lo que buscas...") |
| Autocomplete | Sí/No |
| Suggestions | Sí/No |
| Example queries | Sí/No |
| Voice input | Sí/No |
| Min caracteres | {{NUM}} |
| Debounce | {{MS}}ms |

### 6.3 Filtros [OBL]

| Filter ID | Label | Tipo | Opciones | Default | Server-side |
|-----------|-------|------|----------|---------|-------------|
| `category` | Categoría | Dropdown | {{OPCIONES}} | All | Sí |
| `type` | Tipo | Dropdown | {{OPCIONES}} | All | Sí |
| `min_quality` | Quality mín | Number input | 0-1 | {{DEFAULT}} | Sí |
| `min_relevance` | Relevancia mín | Number input | 0-1 | {{DEFAULT}} | Sí |
| `date_range` | Fecha | Date range | — | All time | Sí |
| `{{FILTER}}` | {{LABEL}} | {{TIPO}} | {{OPCIONES}} | {{DEFAULT}} | Sí/No |

### 6.4 Results list [OBL]

| Campo | Valor |
|-------|-------|
| Layout | [List / Grid / Cards] |
| Items por página | {{NUM}} |
| Paginación | [Numbered / Load more / Infinite scroll] |
| Ordenamiento | [Relevance / Date / Quality / Custom] |
| Default sort | Relevance (score desc) |

---

## 7) Performance metrics (visible) [OBL]

> **Activación:** Siempre obligatorio para búsqueda semántica.

### 7.1 Métricas a mostrar [OBL]

| Métrica | Label | Formato | Visible por default |
|---------|-------|---------|---------------------|
| `query_time_ms` | "query" | "23ms" | Sí |
| `search_time_ms` | "search" | "4ms" | Sí |
| `total_results` | — | "12 resultados" | Sí |
| `model` | "Modelo" | "bge-small-en-v1.5" | [Admin only / Todos] |
| `index_type` | "Índice" | "HNSW" | [Admin only / Todos] |

### 7.2 Performance badge [OBL]

```
query: 23ms · search: 4ms
```

| Campo | Valor |
|-------|-------|
| Posición | Results header |
| Formato | "query: {{X}}ms · search: {{Y}}ms" |
| Tooltip | Breakdown detallado |

### 7.3 Tech note (footer) [OPC]

| Campo | Valor |
|-------|-------|
| Contenido | "Búsqueda vectorial con modelo {{MODEL}} ({{DIMS}} dims) · índice {{INDEX}}" |
| Visible para | [Todos / Admins / Debug mode] |
---

*...Continuación de Parte 1 (Secciones 0-7)*

---

## 8) Filtros y facetas [OBL]

> **Activación:** Siempre obligatorio.

### 8.1 Filtros pre-búsqueda [OBL]

| Filter ID | Label | Tipo | Server-side | Afecta embedding |
|-----------|-------|------|-------------|------------------|
| `category` | Categoría | Dropdown | Sí | No (metadata filter) |
| `type` | Tipo | Dropdown | Sí | No |
| `min_quality` | Quality mín | Number | Sí | No |
| `date_from` | Desde | Date | Sí | No |
| `status` | Estado | Dropdown | Sí | No |

### 8.2 Filtros post-búsqueda [OPC]

| Filter ID | Label | Descripción |
|-----------|-------|-------------|
| `min_relevance` | Relevancia mín | Filtrar resultados con score < X |
| `hide_duplicates` | Ocultar similares | Agrupar resultados muy similares |

### 8.3 Facetas dinámicas [COND]

> **Activación:** Incluir si se muestran conteos por faceta.

| Faceta | Mostrar conteo | Actualizar en tiempo real |
|--------|----------------|---------------------------|
| Categoría | Sí | Sí |
| Tags | Sí | Sí |
| Tipo | Sí | Sí |

---

## 9) Estados de la búsqueda [OBL]

> **Activación:** Siempre obligatorio. Referencia: `UXStates_Pack_{{PROYECTO}}`

### 9.1 Estados principales [OBL]

| Estado | Trigger | UI |
|--------|---------|-----|
| `idle` | Página cargada, sin query | Search box vacío, suggestions/examples |
| `typing` | Usuario escribiendo | Debounce activo, autocomplete |
| `searching` | Query enviada | Skeleton results, spinner |
| `results` | Resultados recibidos | Lista de resultados |
| `no_results` | 0 resultados | Empty state con sugerencias |
| `error` | Error en búsqueda | Error message + retry |
| `partial_error` | Algunos resultados fallaron | Resultados parciales + warning |

### 9.2 Empty state ("Sin resultados") [OBL]

| Elemento | Contenido |
|----------|-----------|
| Ilustración | {{ILUSTRACION}} |
| Título | "No encontramos resultados para '{{query}}'" |
| Sugerencias | Revisar ortografía, usar términos más generales, quitar filtros |
| Queries sugeridas | Basadas en historial o populares |
| CTA | "Limpiar filtros" / "Ver todo" |

### 9.3 Loading state [OBL]

| Elemento | Implementación |
|----------|----------------|
| Search input | Disabled durante búsqueda |
| Results area | Skeleton de {{NUM}} cards |
| Progress | [Spinner / Progress bar / Shimmer] |
| Cancelable | Sí/No |

---

## 10) Accesibilidad (A11Y) [OBL]

> **Activación:** Siempre obligatorio.

### 10.1 Search input [OBL]

| Requisito | Implementación |
|-----------|----------------|
| Label | `aria-label="Búsqueda semántica"` |
| Role | `role="searchbox"` |
| Autocomplete | `aria-autocomplete="list"` si aplica |
| Live region | Anunciar "Buscando..." y "X resultados encontrados" |

### 10.2 Results [OBL]

| Requisito | Implementación |
|-----------|----------------|
| Results count | `aria-live="polite"` para anunciar conteo |
| Result items | `role="article"` o lista semántica |
| Relevance score | Texto alternativo "94% de relevancia" |
| Keyboard nav | Arrow keys para navegar resultados |

### 10.3 Filtros [OBL]

| Requisito | Implementación |
|-----------|----------------|
| Labels | Asociados a cada control |
| Estado activo | Anunciar filtros aplicados |
| Clear filters | Accesible por keyboard |

---

## 11) Analytics / Instrumentación [OBL]

> **Activación:** Siempre obligatorio.

### 11.1 Eventos [OBL]

| Evento | Trigger | Payload |
|--------|---------|---------|
| `search_initiated` | Query enviada | `query, filters, user_id` |
| `search_completed` | Resultados recibidos | `query, results_count, latency_ms, model` |
| `search_no_results` | 0 resultados | `query, filters` |
| `search_error` | Error | `query, error_code` |
| `result_clicked` | Click en resultado | `query, result_id, position, relevance_score` |
| `result_viewed` | Resultado visible (viewport) | `query, result_id, position` |
| `filter_applied` | Filtro cambiado | `filter_id, value, results_count` |
| `filter_cleared` | Filtros limpiados | `previous_filters` |
| `query_refined` | Query modificada | `original_query, new_query` |
| `pagination` | Cambio de página | `query, page, results_count` |

### 11.2 Métricas de relevancia [OBL]

| Métrica | Cálculo | Objetivo |
|---------|---------|----------|
| MRR | Mean Reciprocal Rank | > {{VALOR}} |
| Precision@5 | Clicks en top 5 / búsquedas | > {{VALOR}}% |
| CTR | Clicks / Impresiones | > {{VALOR}}% |
| Zero-result rate | Búsquedas sin resultados / Total | < {{VALOR}}% |
| Abandonment rate | Búsquedas sin click / Total | < {{VALOR}}% |
| Avg position clicked | Posición promedio del click | < {{VALOR}} |

### 11.3 Feedback explícito [COND]

> **Activación:** Incluir si hay sistema de feedback.

| Mecanismo | Implementación |
|-----------|----------------|
| Thumbs up/down | Por resultado |
| "No es relevante" | Flag por resultado |
| "Falta algo" | Feedback global |

---

## 12) API y datos [OBL]

> **Activación:** Siempre obligatorio.

### 12.1 Endpoint de búsqueda [OBL]

| Campo | Valor |
|-------|-------|
| **Endpoint** | `POST /api/search/semantic` |
| **Auth** | {{AUTH_TYPE}} |
| **Rate limit** | {{LIMIT}} requests/min |

### 12.2 Request payload [OBL]

```json
{
  "query": "dark theme dashboard with charts",
  "filters": {
    "category": "fintech",
    "min_quality": 0.7,
    "status": "active"
  },
  "options": {
    "top_k": 20,
    "min_score": 0.5,
    "include_metadata": true,
    "highlight": true
  }
}
```

### 12.3 Response payload [OBL]

```json
{
  "results": [
    {
      "id": "doc-123",
      "title": "Stripe Dashboard",
      "excerpt": "<em>Dark mode dashboard</em> with purple accents...",
      "url": "/kb/doc-123",
      "relevance_score": 0.94,
      "quality_score": 0.95,
      "match_fields": ["token_inventory", "design_observations"],
      "category": "fintech",
      "tags": ["dashboard", "dark-theme"],
      "thumbnail": "https://..."
    }
  ],
  "meta": {
    "total": 12,
    "query_ms": 23,
    "search_ms": 4,
    "model": "bge-small-en-v1.5",
    "index": "hnsw"
  }
}
```

### 12.4 Error responses [OBL]

| Error code | Descripción | HTTP status |
|------------|-------------|-------------|
| `QUERY_TOO_SHORT` | Query muy corta | 400 |
| `QUERY_TOO_LONG` | Query excede límite | 400 |
| `INDEX_UNAVAILABLE` | Índice no disponible | 503 |
| `EMBEDDING_FAILED` | Error generando embedding | 500 |
| `SEARCH_TIMEOUT` | Búsqueda timeout | 504 |
| `RATE_LIMITED` | Rate limit excedido | 429 |

---

## 13) Performance [OBL]

> **Activación:** Siempre obligatorio.

### 13.1 Objetivos de latencia [OBL]

| Fase | Objetivo (p50) | Objetivo (p95) | Crítico |
|------|----------------|----------------|---------|
| Embedding generation | < {{MS}}ms | < {{MS}}ms | > {{MS}}ms |
| Vector search | < {{MS}}ms | < {{MS}}ms | > {{MS}}ms |
| Reranking | < {{MS}}ms | < {{MS}}ms | > {{MS}}ms |
| Total (server) | < {{MS}}ms | < {{MS}}ms | > {{MS}}ms |
| Total (perceived) | < {{MS}}ms | < {{MS}}ms | > {{MS}}ms |

### 13.2 Estrategias de optimización [OBL]

| Estrategia | Implementación |
|------------|----------------|
| Caching de embeddings | Cache queries frecuentes |
| Approximate search | HNSW vs exact search |
| Pre-filtering | Filtrar antes de search vectorial |
| Pagination | No cargar todos los resultados |
| Debounce | {{MS}}ms antes de buscar |

---

## 14) QA / Casos de prueba [OBL]

> **Activación:** Siempre obligatorio.

### 14.1 Casos de búsqueda [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TS-01 | Query simple | Resultados relevantes ordenados por score |
| TS-02 | Query semántica (sinónimos) | Encuentra resultados sin keyword exacta |
| TS-03 | Query larga (párrafo) | Funciona correctamente |
| TS-04 | Query vacía | No dispara búsqueda |
| TS-05 | Query sin resultados | Empty state con sugerencias |

### 14.2 Casos de filtros [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TF-01 | Filtro por categoría | Solo resultados de esa categoría |
| TF-02 | Filtro por quality mín | Solo resultados >= threshold |
| TF-03 | Múltiples filtros | Combinación AND correcta |
| TF-04 | Limpiar filtros | Reset a estado inicial |

### 14.3 Casos de performance [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TP-01 | Query típica | < {{MS}}ms |
| TP-02 | Query con filtros | < {{MS}}ms |
| TP-03 | Concurrent queries | Sin degradación |
| TP-04 | Large result set | Paginación funciona |

### 14.4 Casos de relevancia [OBL]

| ID | Query test | Resultado esperado en top 3 | Score mínimo |
|----|------------|----------------------------|--------------|
| TR-01 | "{{QUERY_1}}" | {{DOC_ESPERADO}} | > {{SCORE}} |
| TR-02 | "{{QUERY_2}}" | {{DOC_ESPERADO}} | > {{SCORE}} |
| TR-03 | "{{QUERY_3}}" | {{DOC_ESPERADO}} | > {{SCORE}} |

---

## 15) Riesgos, supuestos y decisiones [OBL]

> **Activación:** Siempre obligatorio.

### 15.1 Riesgos [OBL]

| ID | Riesgo | Probabilidad | Impacto | Mitigación |
|----|--------|--------------|---------|------------|
| R-01 | Relevancia baja | Media | Alto | Reranking, feedback loop |
| R-02 | Latencia alta | Media | Alto | Caching, approximate search |
| R-03 | Costos de embeddings | Media | Medio | Caching, modelo local |
| R-04 | Index stale | Media | Medio | Pipeline de actualización |

### 15.2 Supuestos [OBL]

| ID | Supuesto | Validado |
|----|----------|----------|
| S-01 | Modelo de embeddings seleccionado | Sí/No |
| S-02 | Vector DB configurado | Sí/No |
| S-03 | Pipeline de indexación funcional | Sí/No |

### 15.3 Decisiones pendientes [OBL]

| ID | Tema | Decisión | Responsable | Fecha |
|----|------|----------|-------------|-------|
| D-01 | Modelo de embeddings | {{DECISION}} | ML/Tech | {{FECHA}} |
| D-02 | Vector DB | {{DECISION}} | Tech | {{FECHA}} |
| D-03 | Hybrid vs semantic puro | {{DECISION}} | PM/ML | {{FECHA}} |

---

## 16) Checklist de aprobación [OBL]

### 16.1 Modelo y datos [OBL]

- [ ] Modelo de embeddings seleccionado (§3)
- [ ] Vector DB configurado
- [ ] Pipeline de indexación funcional
- [ ] Campos indexados definidos

### 16.2 UX [OBL]

- [ ] UI de búsqueda especificada (§6)
- [ ] Relevance score visualization definida (§5)
- [ ] Estados definidos (§9)
- [ ] Empty states diseñados

### 16.3 Performance [OBL]

- [ ] Objetivos de latencia definidos (§13)
- [ ] Caching strategy
- [ ] Métricas visibles configuradas (§7)

### 16.4 QA/Analytics [OBL]

- [ ] Casos de prueba documentados
- [ ] Casos de relevancia definidos (§14.4)
- [ ] Analytics instrumentado (§11)

### 16.5 Firmas de aprobación [OBL]

| Rol | Nombre | Fecha | Status |
|-----|--------|-------|--------|
| PM/PO | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| AI/ML Owner | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| UX/UI | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| Tech Lead | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| QA | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |

---

## 17) Particularidades del proyecto [OPC]

### 17.1 Excepciones al estándar

| Sección | Excepción | Justificación |
|---------|-----------|---------------|
| {{SECCION}} | {{EXCEPCION}} | {{JUSTIFICACION}} |

---

## 📋 ANEXOS RELACIONADOS

- [ ] **DataGrid** → Si resultados se muestran en grid con acciones
- [ ] **EntityDetail** → Para detalle de cada resultado
- [ ] **UXStates** → Estados de búsqueda

---

## 🔁 GUÍA OPERATIVA PARA AGENTES

### Cómo usar este template:

1. **Copiar** el template
2. **Completar §3** (Modelo de embeddings) — sección núcleo
3. **Completar §5** (Estructura de resultados) — sección núcleo
4. **Definir §7** (Performance metrics visibles)
5. **Documentar §14.4** (Casos de relevancia) — crítico para QA
6. **Validar** con ML Owner

### Secciones núcleo (mínimo viable):

- §0 Metadatos
- §3 **Modelo de embeddings y vectores** ← NÚCLEO
- §4 Query y retrieval
- §5 **Resultados de búsqueda** ← NÚCLEO
- §6 UI de búsqueda
- §7 **Performance metrics** ← CRÍTICO
- §9 Estados
- §12 API
- §14 QA (especialmente §14.4 casos de relevancia)
- §16 Checklist

### Validación cruzada:

- Modelo en §3 debe coincidir con tech note en §7
- Campos en §3.4 deben aparecer en match_fields de §5
- Latencias en §13 deben ser alcanzables con config de §3
- Casos de relevancia (§14.4) deben validarse con datos reales

### Red flags a evitar:

- ❌ Sin modelo de embeddings definido
- ❌ Sin métricas de performance visibles
- ❌ Sin empty state para "sin resultados"
- ❌ Sin visualización de relevance score
- ❌ Sin casos de prueba de relevancia
- ❌ Sin caching strategy (costos de API)
- ❌ Sin feedback loop para mejorar relevancia

---

> **Fin del template**  
> **Versión:** 2.0  
> **Última actualización:** {{FECHA_ACTUALIZACION}}
