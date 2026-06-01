# VTT.SKILL-STATUS-007 — Mantener dashboard SPRINT_STATUS_SX.md del TL

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-STATUS-007` |
| **Categoría** | STATUS (Sprint dashboard del TL) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-31 |
| **Aplica a** | TL Reviewer durante FASE 3 del sprint |
| **Tokens estimados** | ~140 |
| **Cuándo se usa** | `WORKFLOW-ASG-001.028` / `CARD-EXE-009` |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `sprint` | string | sí | ej. S03 |
| `sprint_status_path` | path | sí | |
| `trigger_event` | enum | sí | |
| `sprint_id` | UUID | sí | sprint en VTT |
| `tl_name` | string | opcional | |

`trigger_event` ∈ {`task_in_progress_started`, `task_in_review_received`, `task_approved`, `task_on_hold_authorized`, `issue_created`, `blocker_detected`, `daily_sync`, `manual_update`}

## Precondición

- `SPRINT_STATUS_<sprint>.md` existe (creado en setup del sprint)
- TL con write access al repo

## Variables del entorno

- `$VTT_TOKEN`, `$VTT_SETUP`

## Reglas

- R1 Actualizar al MOMENTO del evento, no batchear
- R2 Estructura canónica obligatoria 7 secciones
- R3 NO duplicar info de VTT — referenciar links
- R4 Commit con mensaje `chore(sprint): SPRINT_STATUS_<sprint>.md — <trigger_event>`
- R5 Cross-reference con TASK_TRACKING (sprint actual = fuente)
- R6 NO se firma, NO bloquea cierre del sprint

## Ejecución

```bash
python $VTT_SETUP/02.normativa/04.Scripts/status/SCRIPT-STATUS-003_update_sprint_status.py \
  --sprint "$SPRINT" \
  --status-path "$SPRINT_STATUS_PATH" \
  --trigger-event "$TRIGGER_EVENT" \
  --sprint-id "$SPRINT_ID" \
  --tl-name "$TL_NAME"
```

Script:
1. Consulta VTT (tasks/issues/devlog del sprint)
2. Genera §1-§5 desde datos VTT
3. Preserva §6 (próximos pasos manual del TL)
4. Agrega entry §7 Historial

## Validación

- Markdown válido
- Secciones §1-§7 presentes
- Commit successful

## Error común

- Discrepancia con TASK_TRACKING → SPRINT_STATUS es fuente (R5)
- Conflict en git push → `git pull --rebase` + reintentar
- §6 perdida → verificar versión del script (preserva manual)

## Scripts invocados

- `SCRIPT-STATUS-003_update_sprint_status.py` (mismo número, distinto target)

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-31 | Versión inicial. Dashboard operativo TL (vivo). NO confundir con SKILL-STATUS-003 (task_completed). |
