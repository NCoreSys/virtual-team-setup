# TEMPLATE: INDEX maestro del paquete de research processing

> **Cómo usar:** copia este template a `RESEARCH_PROCESSING_INDEX_<feature>.md`. Es el índice navegable del paquete completo: inputs + outputs del RA. Borra este bloque antes de entregar.
>
> **Quién lo produce:** Research Analyst (RA) en el paso 4 del pipeline.
> **Propósito:** apuntar a todos los archivos del paquete (inputs y outputs) para que el implementador (o el PM al firmar) tenga un solo punto de entrada.

---

# RESEARCH PROCESSING INDEX — <Feature>

## Metadata

| Campo | Valor |
|---|---|
| **Feature** | <ej. Hook Manager R2.0> |
| **Repo origen** | <ej. virtual-teams-Hook-Manager> |
| **Versión investigación** | <ej. R2.0> |
| **Fecha procesamiento** | YYYY-MM-DD |
| **Procesado por** | Research Analyst (UUID) |
| **Estado** | En proceso / Listo para review / Aprobado PM |

---

## 1. Inputs procesados

### 1.1 Plan de investigación

| # | Archivo | Path origen | Descripción |
|---|---|---|---|
| 1 | `PLAN_INVESTIGACION_<feature>_v1_0.md` | `<repo>/Analisis Rx.0/prompts/` | Plan que define alcance + N prompts + 4 agentes |

### 1.2 Prompts (uno por bloque)

| # | Bloque | Prompt | Path |
|---|---|---|---|
| 1 | HM-01 | `PROMPT_INVESTIGACION_HM_01_ESTADO_ARTE_TIPOS_ORQUESTACION.md` | <path> |
| 2 | HM-02 | `PROMPT_INVESTIGACION_HM_02_DOLORES_ERRORES_RETOS.md` | <path> |
| ... | | | |

### 1.3 Individuales (4 modelos × N bloques)

| Bloque | Claude | ChatGPT | Gemini | Perplexity |
|---|---|---|---|---|
| HM-01 | `01C_HM-01_...md` | `01CH_...md` | `01G_...md` | `01P_HM-01_...md` |
| HM-02 | ... | ... | ... | ... |

> **Conteo:** N bloques × 4 modelos = <total> archivos individuales

### 1.4 Consolidados (uno por bloque)

| # | Bloque | Consolidado | Líneas | Procesado |
|---|---|---|---|---|
| 1 | HM-01 | `CONSOLIDADO_HM-01.md` | 463 | ✅ EXTRACT generado |
| 2 | HM-02 | `CONSOLIDADO_HM-02.md` | <N> | ✅ / ⏸ pending |
| ... | | | | |
| **Total** | | | | <N> de <N> procesados |

### 1.5 Perfil consolidador (referencia)

- `PERFIL_AGENTE_CONSOLIDADOR_4a1_<feature>.md` — perfil del agente que produjo los CONSOLIDADOS
- `PERFIL_AGENTE_CONSOLIDADOR_MAESTRO_<N>a1_<feature>.md` — perfil del consolidador maestro (si aplica)

---

## 2. Outputs del RA (este paquete)

### 2.1 EXTRACTs por archivo (paso 1)

| # | Bloque | Archivo | Status | Hallazgos críticos | Conflictos PM |
|---|---|---|---|---|---|
| 1 | HM-01 | `EXTRACT_<feature>_HM-01.md` | ✅ | <N> | <N> |
| 2 | HM-02 | `EXTRACT_<feature>_HM-02.md` | ⏸ pending | - | - |
| ... | | | | | |
| **Total** | | | <X de N> | <suma críticos> | <suma conflictos> |

### 2.2 THEMES consolidado (paso 2)

| Archivo | Status | Dominios cubiertos | Consensos cross-extracto |
|---|---|---|---|
| `THEMES_<feature>.md` | ⏸ pending (espera todos los EXTRACTs) | - | - |

### 2.3 FEATURE SPEC (paso 3)

| Archivo | Status | Features identificadas | Decisiones pendientes PM |
|---|---|---|---|
| `FEATURE_SPEC_<feature>.md` | ⏸ pending (espera THEMES) | - | - |

### 2.4 INDEX maestro (paso 4 — este archivo)

| Archivo | Versión |
|---|---|
| `RESEARCH_PROCESSING_INDEX_<feature>.md` | 1.0 |

---

## 3. Distribución (triple ubicación de outputs)

> Los 4 outputs se copian a las 3 ubicaciones (ver `AGENT_PROFILE_BASE_RA.md` §3.5).

| Output | (a) vtt-setup/knowledge | (b) VTT attachment | (c) Repo origen |
|---|---|---|---|
| N EXTRACTs | `knowledge/research/<repo>/<feature>/` | ✅ tarea VTS-XXX | `<repo>/Analisis Rx.0/extractos/` |
| THEMES | idem | ✅ | idem |
| FEATURE_SPEC | idem | ✅ | idem |
| INDEX (este) | idem | ✅ | idem |

---

## 4. Status global del paquete

| Etapa | Status | Fecha completado |
|---|---|---|
| Paso 1 — EXTRACTs (N archivos) | <X de N> | <fecha o "en progreso"> |
| Paso 2 — THEMES | ⏸ pending | - |
| Paso 3 — FEATURE_SPEC | ⏸ pending | - |
| Paso 4 — INDEX | ⏸ pending | - |
| Distribución triple | ⏸ pending | - |
| Review Coordinator | ⏸ pending | - |
| Sign-off PM | ⏸ pending | - |

---

## 5. Decisiones pendientes consolidadas (todas)

> Todas las `DECISIÓN PENDIENTE PM` detectadas en EXTRACTs + THEMES + FEATURE_SPEC, en un solo lugar para que el PM las revise.

| # | Origen (extracto/themes/spec) | Decisión pendiente | Opciones | Recomendación RA |
|---|---|---|---|---|
| 1 | EXTRACT HM-01 §5.1 | <decisión> | A / B | <neutral> |
| 2 | THEMES §4.1 | <conflicto cross-extracto> | A / B / C | <neutral> |
| 3 | FEATURE_SPEC §8 P-01 | <decisión final pendiente> | A / B | <neutral> |

---

## 6. GAPs detectados consolidados

| # | Origen | GAP | Impacto | Acción sugerida |
|---|---|---|---|---|
| 1 | EXTRACT HM-02 §2.6 | <gap> | Medio | <acción> |

---

## 7. Sign-off del paquete

| Rol | Firma | Fecha | Comentarios |
|---|---|---|---|
| Research Analyst | <UUID> | YYYY-MM-DD | Paquete completo, distribuido en las 3 ubicaciones |
| Coordinator (review) | | | |
| PM (aprobación final) | | | |

---

## 8. Cómo navegar este paquete

**Para el implementador (BE/FE/DB/DO):**
1. Lee `FEATURE_SPEC_<feature>.md` (es lo único obligatorio)
2. Si necesita más contexto de una decisión → ir al EXTRACT referenciado en la trazabilidad
3. Si quiere ver el consolidado completo → CONSOLIDADO original en repo origen

**Para el PM (al firmar):**
1. Lee §5 (Decisiones pendientes) y §6 (GAPs)
2. Decide cada pendiente
3. Firma §7

**Para el Coordinator (al revisar):**
1. Audita §4 (status global) — todo en ✅
2. Verifica trazabilidad inversa en 3-5 ítems aleatorios del FEATURE_SPEC
3. Confirma distribución triple en §3
4. Firma §7

---

**INDEX producido siguiendo `TEMPLATE_RESEARCH_PROCESSING_INDEX.md` v1.0 (2026-06-02).**
