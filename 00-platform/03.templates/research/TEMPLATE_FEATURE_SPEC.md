# TEMPLATE: FEATURE SPEC — Output ejecutable para implementadores

> **Cómo usar:** copia este template a `FEATURE_SPEC_<feature>.md`. Este es el output FINAL que recibe el implementador (BE/FE/DB/DO del proyecto destino). Borra este bloque antes de entregar.
>
> **Quién lo produce:** Research Analyst (RA) en el paso 3 del pipeline.
> **Input:** 1 archivo `THEMES_<feature>.md` + N EXTRACTs (para trazabilidad inversa).
> **Output:** 1 archivo FEATURE_SPEC ejecutable con decisiones congeladas, restricciones, stack, orden, quick wins, decisiones pendientes.
>
> **Reglas:**
> - NO inventar features. Solo lo que THEMES + EXTRACTs dicen.
> - Cada ítem con trazabilidad inversa al EXTRACT y al CONSOLIDADO original.
> - Si hay CONFLICTO no resuelto → marcar `DECISIÓN PENDIENTE PM`, NO decidir solo.
>
> **Referencias:**
> - `AGENT_PROFILE_BASE_RA.md` §3.3 (responsabilidades del spec ejecutable)

---

# FEATURE SPEC — <Feature>

## Metadata

| Campo | Valor |
|---|---|
| **Feature** | <ej. Hook Manager R2.0> |
| **Versión** | 1.0 |
| **Fecha** | YYYY-MM-DD |
| **Autor** | Research Analyst (UUID) |
| **Fuentes** | <N CONSOLIDADOS + 1 THEMES> — lista abajo |
| **Proyecto destino** | <repo donde se implementa, ej. virtual-teams-Hook-Manager> |
| **Estado** | Borrador / Aprobado PM / En implementación |

---

## 1. Resumen ejecutivo (3-5 párrafos)

<Síntesis de lo que el feature debe hacer + decisiones centrales + restricciones críticas. Lo primero que el implementador lee.>

---

## 2. Decisiones congeladas

> Decisiones que el research consolidado considera **resueltas con alta confianza** y deben implementarse así. Cada una con su trazabilidad al consolidado.

| ID | Decisión | Fuente (extracto §) | Marcador | Impacto | Conf. |
|---|---|---|---|---|---|
| D-01 | Hook Manager como control plane propietario | HM-01 §2.1 [CONVERGENCIA 4/4] | 🟢 [VENTAJA-COMPETITIVA] | Alto | 5/5 |
| D-02 | FSM dual taskStatus/hookStatus | HM-01 §2.3 [CONVERGENCIA 5/5] | 🔵 [DECISIÓN-CONFIRMADA] | Alto | 5/5 |
| D-03 | <decisión congelada> | <fuente> | <marcador> | <impacto> | <conf> |

---

## 3. Restricciones duras (NO hacer)

> Lo que el research dice EXPLÍCITAMENTE que NO se debe hacer. Anti-patrones detectados.

| ID | Restricción | Fuente (extracto §) | Razón |
|---|---|---|---|
| R-01 | NO usar polling fijo de 5s | HM-06 §4.2 ⚫ [ANTI-PATRÓN] | "degrada throughput, usar adaptive backoff" |
| R-02 | NO reemplazar Hook Manager con framework genérico | HM-01 §2.1 | "ningún framework del mercado implementa la combinación completa" |

---

## 4. Stack tecnológico decidido

> Solo tecnologías donde el research converge o donde hay decisión congelada. Si hay conflicto sobre una tecnología, va a §8 (decisiones pendientes), NO acá.

| Capa | Tecnología | Razón (cita del research) | Fuente | Alternativas descartadas |
|---|---|---|---|---|
| Durabilidad | Restate | "tres candidatos: Restate, Inngest, Temporal. Restate aparece como primer voto en 3/4 extractos" | HM-04 §3.1, HM-05 §2.2 | Inngest (2do voto), Temporal (3er voto) |
| Stack base | TypeScript + Node 20 + PostgreSQL 16 + Prisma 5.22 | Ya decidido pre-research, confirmado por todos los extractos | - | - |
| ... | | | | |

---

## 5. Features con prioridad

> Lista priorizada de features a implementar. Cada una con justificación + dependencias + estimación gruesa.

### Feature 5.1 — <Nombre>

| Campo | Valor |
|---|---|
| **ID** | F-01 |
| **Prioridad** | P0 (CRÍTICA) / P1 / P2 |
| **Impacto** | Alto / Medio / Bajo |
| **Esfuerzo estimado** | <horas / días — del research si lo dice, sino "TBD"> |
| **Depende de** | Ninguna / F-XX |
| **Bloquea** | F-YY (si esta no se hace, F-YY no avanza) |
| **Trazabilidad** | EXTRACT HM-04 §2.3, THEMES §2.1 |

**Qué hace:**
<descripción 2-3 párrafos>

**Recomendaciones del research:**
- 🔴 [CRÍTICO] <cita literal con §>
- 🟠 [RECOMENDADO] <cita o paráfrasis>

**Restricciones aplicables:**
- R-XX, R-YY

**Decisiones congeladas que aplican:**
- D-XX, D-YY

### Feature 5.2 — <Nombre>

<repetir estructura>

---

## 6. Orden de implementación (dependencias)

```
Sprint 1:
  - F-01 — sin dependencias
  - F-03 — depende de F-01

Sprint 2:
  - F-02 — depende de F-01, F-03
  - F-05 — depende de F-02

Sprint 3:
  - F-04 — depende de F-02
  - F-06 — paralelo a F-04

Sprint 4:
  - F-07 — depende de F-04, F-05, F-06 (cierre del bloque)
```

---

## 7. Quick wins (alto impacto, bajo esfuerzo)

> Features que se pueden hacer pronto con poco esfuerzo y dan valor inmediato.

| # | Feature | Esfuerzo | Impacto | Razón quick win |
|---|---|---|---|---|
| 1 | <feature> | 2-4h | Alto | <por qué es quick win> |

---

## 8. Decisiones pendientes (requieren PM)

> Lo que el research dejó sin consenso. El RA NO decide — lista las opciones con evidencia.

| ID | Decisión pendiente | Opciones | Evidencia por opción | Recomendación RA |
|---|---|---|---|---|
| P-01 | <decisión> | A: <opción> / B: <opción> | A: 2 modelos lo soportan / B: 2 modelos lo soportan | <observación neutral del RA — NO decidir> |

---

## 9. Tech debt aceptado (consciente, postergado)

> Items donde el research recomienda Y, pero por scope/tiempo se aceptan en versión actual y se postergan.

| ID | Tech debt | Razón postergación | Impacto si no se hace | Plan futuro |
|---|---|---|---|---|
| TD-01 | <descripción> | <por qué se posterga ahora> | Medio | Sprint X / Release Y |

---

## 10. GAPs detectados que el PM debe atender

> Cosas que VTT no contemplaba antes del research y que ahora se sabe que faltan.

| ID | GAP | Fuente | Impacto si no se aborda | Acción sugerida |
|---|---|---|---|---|
| G-01 | <descripción del gap> | THEMES §6 [GAP-DETECTADO] | Alto | <acción concreta> |

---

## 11. Métricas de éxito (cómo sabremos que el feature funciona)

> Si el research consolidado define métricas, listarlas. Si no, RA propone y marca como `TBD-PM`.

| Métrica | Target | Fuente | Cómo medir |
|---|---|---|---|
| Throughput hooks/s | ≥1500 | HM-04 §4 datos duros | <herramienta/proceso> |
| Latencia p99 dispatch | <200ms | HM-01 §4 | <herramienta> |

---

## 12. Trazabilidad inversa

| Sección del FEATURE_SPEC | Fuente principal (THEMES + EXTRACTs) |
|---|---|
| §2 Decisiones congeladas | THEMES §3 (consensos cross-extracto) |
| §3 Restricciones | THEMES §2.X agrupado por ANTI-PATRÓN |
| §4 Stack | THEMES §2.2 (Tecnología) |
| §5 Features | EXTRACTs § individuales + THEMES §2 |
| §8 Pendientes PM | THEMES §4 (conflictos) + §8 (decisiones pendientes) |

---

## 13. Sign-off

| Rol | Firma | Fecha |
|---|---|---|
| Research Analyst | <UUID> | YYYY-MM-DD |
| Coordinator (review) | <UUID> | <esperando> |
| PM (aprobación) | <UUID> | <esperando> |

---

**FEATURE_SPEC producido siguiendo `TEMPLATE_FEATURE_SPEC.md` v1.0 (2026-06-02).**
