# Development Log — MS-017 · Budget & Resources

**Fecha:** 2026-05-05
**Tarea:** MS-017 — Budget & Resources
**Agente:** PM — Martin Rivas (`350831b2-e1ae-4dbe-b2eb-7e023ec2e103`)
**Repo:** memory-service-project
**Fase:** Planning (Phase 3)

---

## Resumen

Se produjeron los 5 documentos de presupuesto y recursos de Memory Service R1: Budget Estimate (402h en 10 fases), Cost Breakdown (12 roles, top 3: BE 70h, QA 64h, TL 52h), Resource Plan (matriz de presencia por fase + picos + critical path), ROI Analysis (4 dimensiones cuantificadas con datos reales de Discovery), y Budget Tracking (plantilla usable con S01-S06 + UI-01..04 y reglas de escalación).

---

## Archivos Creados

| Archivo | Descripción |
|---------|-------------|
| `docs/planning/budget/1.6.1_budget_estimate.md` | 402h en 10 fases + estimación de costo USD ($266-$776) |
| `docs/planning/budget/1.6.2_cost_breakdown.md` | 12 roles con horas estimadas y top 3 por carga |
| `docs/planning/budget/1.6.3_resource_plan.md` | Matriz de presencia + picos + roles en critical path |
| `docs/planning/budget/1.6.4_roi_analysis.md` | ROI en 4 dimensiones con datos reales de Discovery |
| `docs/planning/budget/1.6.5_budget_tracking.md` | Plantilla de seguimiento con reglas de escalación |

---

## Decisiones

**D1 — Total 402h (no 381h):** El brief cita 381h como cifra maestra del HO. La discrepancia se explica porque MS-121..145 (Project Setup expandido) añadieron 21h no contempladas originalmente. Se documenta la diferencia y se indica que esas 32h ya están consumidas.

**D2 — ROI en 4 dimensiones:** El brief pedía mínimo 3. Se añadió una 4a dimensión (Habilitación del Ecosistema) porque es el retorno más estratégico y no era redundante con las otras 3.

**D3 — Estimación de costo USD incluida en Budget Estimate:** El brief no lo pedía explícitamente pero los datos de Discovery ($0.82-$2.53/corrida) permitían una estimación creíble (~$266-$776 total). Se incluyó para darle contexto al ROI.

**D4 — Reglas de escalación en Budget Tracking:** Se definieron umbrales cuantitativos (±15% varianza) para que la plantilla sea accionable, no solo descriptiva.

---

## Criterios de Aceptación

| # | Criterio | Estado |
|---|----------|--------|
| CA-1 | Budget Estimate cubre 10 fases, total ~402h | ✅ |
| CA-2 | Cost Breakdown incluye 12 roles, sumas coherentes, top 3 identificados | ✅ BE/QA/TL |
| CA-3 | Resource Plan con presencia por fase, picos y roles críticos | ✅ |
| CA-4 | ROI usa datos reales de Discovery en 3+ dimensiones | ✅ 4 dimensiones |
| CA-5 | Budget Tracking con S01-S06 + UI-01..04 y columna varianza | ✅ |
| CA-6 | Coherente con Phase Breakdown y Sprint Calendar de MS-016 | ✅ |
| CA-7 | Sin TODOs ni secciones vacías | ✅ |

---

**Co-Authored-By:** Claude Sonnet 4.6 <noreply@anthropic.com>
