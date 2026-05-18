# Code Logic — Budget & Resources Documents (MS-017)

**Archivos:** `docs/planning/budget/1.6.1_budget_estimate.md`, `1.6.2_cost_breakdown.md`, `1.6.3_resource_plan.md`, `1.6.4_roi_analysis.md`, `1.6.5_budget_tracking.md`
**Tarea:** MS-017
**Autor:** PM (`350831b2-e1ae-4dbe-b2eb-7e023ec2e103`)
**Fecha:** 2026-05-05

---

## Propósito

5 documentos de planificación financiera y de recursos que cierran formalmente la fase Planning y habilitan MS-018 (Analysis).

## Contenido por documento

| Archivo | Contenido |
|---------|-----------|
| 1.6.1 Budget Estimate | 402h en 10 fases + estimación de costo USD ($266-$776) basada en datos reales de Discovery |
| 1.6.2 Cost Breakdown | 12 roles con horas estimadas. Top 3: BE (70h), QA (64h), TL (52h) |
| 1.6.3 Resource Plan | Matriz de presencia ●/○ por fase. Picos en Ph4 (5 roles) y Ph7 (4 roles). Critical path: BE, TL, DL, DB |
| 1.6.4 ROI Analysis | 4 dimensiones: reducción tokens ($162-$486/mes), eliminación arranque frío (~11h/sem), trazabilidad (~6.75h/sem), habilitación ecosistema |
| 1.6.5 Budget Tracking | Plantilla con tracking por fase + por sprint (S01-S06 + UI-01..04) + reglas de escalación ±15% |

## Decisiones de diseño

- Total 402h (no 381h del HO) — diferencia de 21h por expansión de Project Setup ya consumidas
- ROI en 4 dimensiones (brief pedía 3) — 4a dimensión estratégica no redundante
- Umbrales de escalación cuantitativos en Budget Tracking (±15%) para hacer la plantilla accionable

## Historial de cambios

| Fecha | Tarea | Autor | Cambio |
|-------|-------|-------|--------|
| 2026-05-05 | MS-017 | PM | Creación inicial — cierre de fase Planning |
