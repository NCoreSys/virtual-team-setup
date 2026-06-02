# TEMPLATE: EXTRACT por archivo consolidado

> **Cómo usar:** copia este template a `EXTRACT_<feature>_<bloque>.md` (ej. `EXTRACT_hook-manager_HM-01.md`). Procesa UN consolidado por archivo. Borra este bloque de instrucciones antes de entregar.
>
> **Quién lo produce:** Research Analyst (RA) en el paso 1 del pipeline.
> **Input:** 1 archivo `CONSOLIDADO_<feature>-<bloque>.md`.
> **Output:** 1 archivo EXTRACT con todas las recomendaciones extraídas línea-por-línea.
> **Política:** preservar citas literales en recomendaciones `[CRÍTICO]`. NUNCA parafrasear críticos. Cada ítem con `Impacto: Alto|Medio|Bajo` obligatorio.
>
> **Referencias:**
> - `AGENT_PROFILE_BASE_RA.md` §4 (los 8 marcadores)
> - `VTT.SKILL-RA-001_extract_recommendations.md`
> - Origen del feature: el `PLAN_INVESTIGACION_*.md` correspondiente

---

# EXTRACT — <CONSOLIDADO_NAME>

## Metadata

| Campo | Valor |
|---|---|
| **Feature** | <ej. Hook Manager R2.0> |
| **Bloque** | <ej. HM-01> |
| **Archivo origen** | <path absoluto o relativo al repo origen> |
| **Líneas analizadas** | <N líneas del consolidado> |
| **Fuentes consolidadas** | <ej. ChatGPT V1, ChatGPT V2, Claude, Gemini, Perplexity (5)> |
| **Fecha extracto** | YYYY-MM-DD |
| **Procesado por** | Research Analyst (UUID) |
| **Versión EXTRACT** | 1.0 |

---

## 1. Resumen del consolidado (1 párrafo)

<2-4 oraciones que capturan la conclusión central del CONSOLIDADO. Si el consolidado tiene un §Resumen Ejecutivo, sintetizarlo. NO inventar — solo recoger.>

---

## 2. Recomendaciones — agrupadas por criticidad

> Los 8 marcadores están definidos en `AGENT_PROFILE_BASE_RA.md` §4.
> **Impacto** es campo separado (Alto/Medio/Bajo).
> **Cita literal** entre comillas en `[CRÍTICO]` — NUNCA parafrasear.

### 🔴 [CRÍTICO] — debe hacerse así o el sistema falla

| # | Cita literal | Origen § | Impacto | Convergencia | Contexto / Acción esperada |
|---|---|---|---|---|---|
| 1 | "<cita literal del consolidado>" | §2.1 | Alto | [4/4] | <una línea de qué hay que hacer> |
| 2 | "<...>" | §3.2 | Alto | [3/4] | <...> |

### 🟠 [RECOMENDADO] — fuerte recomendación con justificación

| # | Cita o paráfrasis breve | Origen § | Impacto | Convergencia | Justificación |
|---|---|---|---|---|---|
| 1 | <...> | §2.5 | Medio | [4/4] | <por qué los modelos lo recomiendan> |

### 🟡 [OPCIONAL] — mejora pero no esencial

| # | Recomendación | Origen § | Impacto | Convergencia |
|---|---|---|---|---|
| 1 | <...> | §4.1 | Bajo | [2/4] |

### ⚫ [ANTI-PATRÓN] — NO hacer X (explícito)

| # | Cita literal | Origen § | Impacto | Por qué NO |
|---|---|---|---|---|
| 1 | "<cita>" | §5.3 | Alto | <consecuencia explícita del consolidado> |

### 🔵 [DECISIÓN-CONFIRMADA] — lo que VTT/proyecto ya hizo bien

| # | Decisión confirmada | Origen § | Impacto | Modelos que confirman |
|---|---|---|---|---|
| 1 | <decisión actual del proyecto> | §2.3 | Alto | [4/4] |

### 🟣 [GAP-DETECTADO] — algo que NO contemplamos

| # | Gap | Origen § | Impacto | Acción sugerida |
|---|---|---|---|---|
| 1 | <descripción del gap> | §3.7 | Medio | <acción que el PM debe evaluar> |

### 🟢 [VENTAJA-COMPETITIVA] — diferenciador propietario

| # | Ventaja | Origen § | Impacto | Por qué es diferenciador |
|---|---|---|---|---|
| 1 | <ej. FSM dual taskStatus/hookStatus> | §2.3 | Alto | <ningún framework comercial lo implementa nativo> |

### 🟤 [DIVERGENCIA] — agentes contradicen

| # | Tema | Postura A | Postura B | Modelos por cada postura | Impacto si se elige mal |
|---|---|---|---|---|---|
| 1 | <ej. Restate vs Temporal> | Restate prioritario | Temporal prioritario | A: ChatGPT, Gemini / B: Claude, Perplexity | Medio |

---

## 3. Dependencias detectadas

> Recomendaciones que tienen orden obligatorio entre sí ("para hacer X primero Y") o requieren prerequisito.

| # | Recomendación dependiente | Depende de | Razón |
|---|---|---|---|
| 1 | "Adoptar event-driven como principal" | "Polling como fallback funcional" | <consolidado §X.Y dice "migrar paulatinamente"> |
| 2 | <recomendación B> | <recomendación A> | <cita o explicación del orden> |

---

## 4. Datos duros (números, benchmarks, umbrales, precios)

| # | Métrica | Valor | Fuente (modelo o paper citado en consolidado) | Contexto |
|---|---|---|---|---|
| 1 | Throughput target hooks/s | 1500 | ChatGPT citando benchmark Temporal | Bajo carga sostenida 1h |
| 2 | Latencia p99 dispatch | <200ms | Claude | SLA propuesto |

> **Política:** NO promediar datos de fuentes distintas. Reportar cada dato con su fuente.

---

## 5. Conflictos no resueltos (requieren validación PM)

> Diferentes de divergencias: aquí los modelos NO se ponen de acuerdo y el PM debe decidir.

| # | Tema | Resumen del conflicto | Postura mayoritaria | Postura minoritaria | Recomendación del RA |
|---|---|---|---|---|---|
| 1 | <ej. Adoptar MCP como standard ya o esperar 6 meses> | <2 modelos dicen ya, 2 dicen esperar> | "Ya" (Gemini, Claude) | "Esperar" (ChatGPT, Perplexity) | DECISIÓN PENDIENTE PM |

---

## 6. Subpreguntas del prompt original — cobertura

> El PROMPT_INVESTIGACION_<feature>_<bloque> tiene N subpreguntas. Verificar cuáles tienen respuesta consolidada.

| # | Subpregunta del prompt original | ¿Respuesta consolidada? | Donde |
|---|---|---|---|
| 1 | ¿Qué orquestadores existen en producción? | ✅ | §2 |
| 2 | ¿Cómo orquestan los productos de coding AI? | ✅ | §3 |
| 3 | <subpregunta N> | ⚠️ Parcial / ❌ Sin cobertura | <§ o "no cubierto"> |

---

## 7. Trazabilidad inversa

Para que el implementador pueda volver al texto original:

| Cita / Recomendación | CONSOLIDADO § | Modelo que más profundiza |
|---|---|---|
| "Hook Manager como control plane propietario" | §2.1 | Claude (3 párrafos de razonamiento) |
| <recomendación X> | §Y.Z | <modelo Q> |

---

## 8. Resumen estadístico del extracto

| Categoría | Conteo |
|---|---|
| 🔴 CRÍTICO | <N> |
| 🟠 RECOMENDADO | <N> |
| 🟡 OPCIONAL | <N> |
| ⚫ ANTI-PATRÓN | <N> |
| 🔵 DECISIÓN-CONFIRMADA | <N> |
| 🟣 GAP-DETECTADO | <N> |
| 🟢 VENTAJA-COMPETITIVA | <N> |
| 🟤 DIVERGENCIA | <N> |
| Dependencias | <N> |
| Datos duros | <N> |
| Conflictos pendientes PM | <N> |

---

## 9. Notas del RA

<Observaciones del Research Analyst sobre la calidad del consolidado, dificultades de extracción, sugerencias para el FEATURE_SPEC. Honesto — si el consolidado es débil en algún área, declararlo.>

---

**EXTRACT producido siguiendo `TEMPLATE_EXTRACT_PER_FILE.md` v1.0 (2026-06-02).**
