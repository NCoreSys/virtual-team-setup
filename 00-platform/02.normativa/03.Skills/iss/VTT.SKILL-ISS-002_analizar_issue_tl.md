# VTT.SKILL-ISS-002 — Analizar Issue y clasificar severidad (TL)

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-ISS-002` |
| **Categoría** | ISS (Issue Lifecycle) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-31 |
| **Aplica a** | TL Reviewer al recibir notificación de Issue |
| **Tokens estimados** | ~140 |
| **Cuándo se usa** | `WORKFLOW-ASG-001.011` / `CARD-ISS-003` |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `issue_id` | UUID | sí | |
| `tl_id` | UUID | sí | |

## Precondición

- Issue en `status=open`
- Tarea origen en `task_on_hold`

## Variables del entorno

- `$VTT_TOKEN`

## Reglas

- R1 Clasificación S1-S4 obligatoria
- R2 Responder ≤24h o escalar PM
- R3 Leer Issue + tarea + devlog ANTES de clasificar
- R4 S1/S2 → consultar PM antes de decidir
- R5 Análisis como comment estructurado (auditoría)
- R6 Status Issue → `acknowledged` al iniciar análisis

## Ejecución

```bash
python $VTT_SETUP/02.normativa/04.Scripts/issue/SCRIPT-ISSUE-002_classify_severity.py \
  --issue-id "$ISSUE_ID" \
  --tl-id "$TL_UUID"
```

Script:
1. `PATCH /issues/<id>` → `status=acknowledged`
2. Consulta tarea + devlog
3. Aplica matriz severity × downstream → sugiere S1-S4
4. Devuelve análisis estructurado para que TL valide

## Validación

- Output con `severity_operational_suggested` ∈ {S1,S2,S3,S4}
- `requires_pm_consultation` bool

## Error común

- Issue no encontrado → verificar issueId
- Clasificación sin contexto → R3
- S1/S2 sin consulta PM → revertir + consultar

## Scripts invocados

- `SCRIPT-ISSUE-002_classify_severity.py`

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-31 | Versión inicial. Matriz S1-S4. |
