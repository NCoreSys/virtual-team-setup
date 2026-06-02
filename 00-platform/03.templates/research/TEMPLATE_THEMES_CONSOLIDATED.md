# TEMPLATE: THEMES — Cruce temático multi-archivo

> **Cómo usar:** copia este template a `THEMES_<feature>.md`. Cruza los N EXTRACTs de una misma feature por dominio. Borra este bloque antes de entregar.
>
> **Quién lo produce:** Research Analyst (RA) en el paso 2 del pipeline.
> **Input:** N archivos `EXTRACT_<feature>_<bloque>.md`.
> **Output:** 1 archivo THEMES con recomendaciones agrupadas por dominio + consensos cross-extracto + conflictos cross-extracto.
>
> **Referencias:**
> - `AGENT_PROFILE_BASE_RA.md` §3.2 (responsabilidades de consolidación temática)
> - `VTT.SKILL-RA-002_consolidate_themes.md`

---

# THEMES — <Feature>

## Metadata

| Campo | Valor |
|---|---|
| **Feature** | <ej. Hook Manager R2.0> |
| **Extractos consolidados** | <N> (lista abajo en §1) |
| **Fecha consolidación temática** | YYYY-MM-DD |
| **Procesado por** | RA (UUID) |
| **Versión THEMES** | 1.0 |

---

## 1. Inputs procesados

| # | Bloque | EXTRACT | Recomendaciones críticas | GAPs | Conflictos pendientes |
|---|---|---|---|---|---|
| 1 | HM-01 | `EXTRACT_hook-manager_HM-01.md` | 8 | 1 | 0 |
| 2 | HM-02 | `EXTRACT_hook-manager_HM-02.md` | 5 | 3 | 1 |
| ... | | | | | |
| **Total** | | | **<suma>** | **<suma>** | **<suma>** |

---

## 2. Recomendaciones agrupadas por dominio

### 2.1 Arquitectura

> Recomendaciones sobre estructura del sistema, decisiones de patrón, arquitectura macro.

| # | Recomendación | Marcador | Impacto | Aparece en extractos | Convergencia cross-extracto |
|---|---|---|---|---|---|
| 1 | "Hook Manager como control plane propietario" | 🟢 [VENTAJA-COMPETITIVA] | Alto | HM-01, HM-03, HM-04 | [3/N extractos lo mencionan] |
| 2 | FSM dual taskStatus/hookStatus | 🔵 [DECISIÓN-CONFIRMADA] | Alto | HM-01, HM-05 | [2/N] |

### 2.2 Tecnología (stack / herramientas)

| # | Recomendación | Marcador | Impacto | Aparece en | Convergencia |
|---|---|---|---|---|---|
| 1 | Adoptar Restate, Inngest o Temporal para durable execution | 🟠 [RECOMENDADO] | Alto | HM-01, HM-04, HM-05, HM-06 | [4/N] |

### 2.3 Migración (orden, pasos, fallback)

| # | Recomendación | Marcador | Impacto | Aparece en | Convergencia |
|---|---|---|---|---|---|
| 1 | "Polling → event-driven (con polling como fallback)" | 🔴 [CRÍTICO] | Alto | HM-01, HM-06 | [2/N] |

### 2.4 Seguridad / Governance

| # | Recomendación | Marcador | Impacto | Aparece en | Convergencia |
|---|---|---|---|---|---|

### 2.5 Performance / Escalabilidad

### 2.6 Observabilidad / Monitoreo

### 2.7 Human-in-the-loop / Aprobaciones

### 2.8 Costos / Model Routing

### 2.9 Otros dominios detectados

> Si los extractos cubren dominios no listados arriba, agregalos como subsección 2.X.

---

## 3. Consensos cross-extracto

> Recomendaciones que aparecen en **3+ extractos** de la misma feature. Son los señales más fuertes para el FEATURE_SPEC.

| # | Recomendación | Marcador | Impacto | Extractos donde aparece | Cita representativa |
|---|---|---|---|---|---|
| 1 | "Mantener Hook Manager como control plane propietario" | 🟢 [VENTAJA-COMPETITIVA] [CONVERGENCIA 4/4] | Alto | HM-01, HM-03, HM-04, HM-08 (4 de N) | "ningún framework del mercado implementa la combinación completa que VTT necesita" |

---

## 4. Conflictos cross-extracto

> Recomendaciones que aparecen en DOS o más extractos pero **contradicen entre sí**. Diferentes de las divergencias dentro de un extracto.

| # | Tema | Postura A (extractos) | Postura B (extractos) | Severidad del conflicto | Recomendación del RA |
|---|---|---|---|---|---|
| 1 | <ej. Orden de adopción Restate vs Temporal> | HM-04 (Restate primero), HM-05 (Restate) | HM-06 (Temporal primero), HM-07 (Temporal) | Alto (decisión arquitectónica) | DECISIÓN PENDIENTE PM |

---

## 5. Dependencias cross-feature (orden de implementación)

> "Para hacer X (bloque A) primero hay que resolver Y (bloque B)". Detectadas cruzando los EXTRACTs.

```
Orden sugerido de implementación (preliminar):

1. <bloque/feature 1>  — sin dependencias
2. <bloque/feature 2>  — depende de 1 (razón: <cita>)
3. <bloque/feature 3>  — depende de 1, 2
4. ...
```

Tabla de dependencias explícitas:

| Item dependiente | Depende de | Razón | Origen (extractos) |
|---|---|---|---|
| <feature B> | <feature A> | "X requiere Y antes" | HM-03, HM-07 |

---

## 6. GAPs cross-feature consolidados

> GAPs detectados que aparecen en varios extractos = problemas reales que VTT debe atender.

| # | GAP | Aparece en | Impacto | Acción sugerida (RA → escalar a PM) |
|---|---|---|---|---|
| 1 | "VTT no tiene mecanismo de detección de Sybil agents" | HM-02, HM-08 | Medio | Crear tarea de research adicional o tarea de implementación |

---

## 7. Datos duros consolidados

> Números, umbrales, benchmarks que aparecen en múltiples extractos. Si dos extractos contradicen el mismo dato → conflicto en §4.

| Métrica | Valor consensuado | Rangos por fuente | Confianza |
|---|---|---|---|
| Throughput hooks/s target | 1500 | ChatGPT: 1500 / Claude: 2000 | Media (rango 1500-2000) |
| Latencia p99 dispatch | <200ms | Convergente en HM-01, HM-04, HM-05 | Alta |

---

## 8. Decisiones pendientes para el PM

> Resumen de conflictos + GAPs que el PM debe revisar antes de generar el FEATURE_SPEC final.

| # | Decisión pendiente | Origen (§THEMES) | Opciones | Recomendación RA |
|---|---|---|---|---|
| 1 | <decisión> | §4.1 | A / B / C | <opción que el RA ve más sólida basado en evidencia, sin decidir> |

---

## 9. Resumen estadístico cross-extractos

| Categoría | Conteo cross-extractos |
|---|---|
| Recomendaciones CRÍTICAS únicas | <N> |
| Recomendaciones por dominio | Arquitectura: N, Tecnología: N, ... |
| Consensos (3+ extractos coinciden) | <N> |
| Conflictos cross-extracto | <N> |
| GAPs consolidados | <N> |
| Decisiones pendientes PM | <N> |
| Dependencias cross-feature | <N> |

---

## 10. Notas del RA

<Observaciones sobre el cruce: dominios que dominan, dominios subcubiertos, calidad agregada de la investigación, sugerencias para el FEATURE_SPEC.>

---

**THEMES producido siguiendo `TEMPLATE_THEMES_CONSOLIDATED.md` v1.0 (2026-06-02).**
