# VTT.SKILL-ISS-003 — Decidir acción del Issue (TL)

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-ISS-003` |
| **Categoría** | ISS (Issue Lifecycle) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-31 |
| **Aplica a** | TL Reviewer post `SKILL-ISS-002` |
| **Tokens estimados** | ~150 |
| **Cuándo se usa** | `WORKFLOW-ASG-001.037` / `CARD-ISS-004` |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `issue_id` | UUID | sí | |
| `tl_id` | UUID | sí | |
| `action` | enum | sí | A/B/C/D |
| `instructions_for_agent` | string | opcional | (B, C) |
| `rejection_reason` | string | requerido si D | |
| `corrective_task_id` | UUID | requerido si A | |
| `tech_debt_ti_id` | UUID | requerido si C | |

## Precondición

- `SKILL-ISS-002` ejecutado
- Si S1/S2: PM consultado

## Variables del entorno

- `$VTT_TOKEN`

## Reglas

- R1 4 opciones mutuamente excluyentes
- R2 `create_corrective_task` si: critical+downstream, conflicto TI, bug reproducible
- R3 `resolve_inline` solo si NO requiere salir de allowedPaths
- R4 `accept_workaround` REQUIERE TI tech_debt
- R5 `reject_issue` REQUIERE justificación
- R6 Status final: `pending_corrective` (A) / `resolved` (B,C) / `wont_fix` (D)

## Ejecución

```bash
python $VTT_SETUP/02.normativa/04.Scripts/issue/SCRIPT-ISSUE-003_resolve_issue.py \
  --issue-id "$ISSUE_ID" \
  --action "$ACTION" \
  --tl-id "$TL_UUID" \
  [--instructions "$INSTRUCTIONS"] \
  [--rejection-reason "$REJECTION_REASON"] \
  [--corrective-task-id "$CORRECTIVE_TASK_ID"] \
  [--tech-debt-ti-id "$TECH_DEBT_TI_ID"]
```

## Validación

- Issue cerrado con status correspondiente
- Agente notificado
- Auto-resume preparado (B/C/D)

## Error común

- `resolve_inline` requiere salir allowedPaths → cambiar a A
- `accept_workaround` sin TI → crear TI post-facto
- Auto-resume no dispara → verificar onHoldIssueId

## Scripts invocados

- `SCRIPT-ISSUE-003_resolve_issue.py`
- `SCRIPT-TASK-001_create_corrective.py` (Opción A)

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-31 | Versión inicial. 4 opciones con sub-flujos. |
