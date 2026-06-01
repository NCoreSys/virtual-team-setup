# VTT.WORKFLOW-ASG-001.028 — TL mantiene SPRINT_STATUS_SX.md

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-ASG-001.028` |
| **Pertenece a** | `VTT.PROTOCOL-ASG-001` §5.3.bis |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-05-31 |
| **Aplica a** | TL Reviewer durante FASE 3 |
| **Reglas Nivel 0** | `RULE-TEMPLATE-001`, `RULE-SCRIPT-001` |
| **CARD asociada** | `VTT.CARD-EXE-009` |

---

## 1. Propósito

Mantener `SPRINT_STATUS_<sprint>.md` (dashboard operativo del TL) **vivo durante toda la FASE 3**. Permite reanudar trabajo sin perder contexto entre sesiones.

**Diferencia con CIERRE:** SPRINT_STATUS = vivo. CIERRE = snapshot final firmado.

## 2. Inputs

| Input | Tipo | Descripción |
|---|---|---|
| `sprint` | string | ej. `S03` |
| `project_name` | string | |
| `sprint_status_path` | path | `knowledge/sprints/<sprint>/SPRINT_STATUS_<sprint>.md` |
| `trigger_event` | enum | evento que dispara update |
| `tasks_affected` | array | opcional |

`trigger_event` ∈ {`task_in_progress_started`, `task_in_review_received`, `task_approved`, `task_on_hold_authorized`, `issue_created`, `blocker_detected`, `daily_sync`, `manual_update`}

## 3. Precondiciones

- Sprint inicializado
- `SPRINT_STATUS_<sprint>.md` existe (creado por `WORKFLOW-ASG-001.027`)

## 4. Reglas

| # | Regla |
|---|---|
| R1 | Actualizar al MOMENTO del evento, no batchear |
| R2 | SPRINT_STATUS es operativo del TL — NO se firma, NO bloquea cierre |
| R3 | Estructura canónica obligatoria 7 secciones (§1-§7) |
| R4 | NO duplicar info de VTT — referenciar links |
| R5 | Commit `chore(sprint): SPRINT_STATUS_<sprint>.md — <trigger_event>` |
| R6 | Cross-reference con TASK_TRACKING global (sprint actual = fuente) |

## 5. Pasos

### Paso 1 — Detectar trigger_event

### Paso 2 — Consultar VTT
```bash
curl -s "$VTT_BASE_URL/api/sprints/<SPRINT_ID>/tasks?include=status,assignedTo"
curl -s "$VTT_BASE_URL/api/sprints/<SPRINT_ID>/issues?status=open,acknowledged"
curl -s "$VTT_BASE_URL/api/sprints/<SPRINT_ID>/devlog?severity=critical,high&status=pending"
```

### Paso 3 — Ejecutar script
```bash
python $VTT_SETUP/02.normativa/04.Scripts/status/SCRIPT-STATUS-003_update_sprint_status.py \
  --sprint "$SPRINT" \
  --status-path "$SPRINT_STATUS_PATH" \
  --trigger-event "$TRIGGER_EVENT" \
  --sprint-id "$SPRINT_ID" \
  --tl-name "<nombre>"
```

Script regenera §1-§5 desde VTT, preserva §6 (próximos pasos del TL — solo manual), agrega entry §7.

### Paso 4 — Estructura canónica (7 secciones)
1. Resumen sprint
2. Tareas por estado (🟢🟤🔵🟠🟡🔴)
3. Blockers activos
4. Issues abiertos
5. KPIs
6. Próximos pasos del TL (manual)
7. Historial de cambios

### Paso 5 — Cross-reference con TASK_TRACKING
Si discrepancia → SPRINT_STATUS es fuente del sprint actual.

### Paso 6 — Commit
```bash
git add $SPRINT_STATUS
git commit -m "chore(sprint): SPRINT_STATUS_<sprint>.md — <trigger_event>

- Tarea(s) afectada(s): <lista>

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
git push origin <branch_tl>
```

### Paso 7 — Notificar stakeholders (opcional)
Si `trigger_event in [blocker_detected, issue_created]` severity `critical` → comment al PM.

## 6. Outputs

| Output | Descripción |
|---|---|
| `sprint_status_path` | path |
| `sections_updated` | array |
| `commit_sha` | string |
| `discrepancies_with_tracking` | array (debe ser vacío) |

## 7. Validación

Commit successful + markdown válido + secciones §1-§7 presentes.

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| SPRINT_STATUS desactualizado | TL no actualizó al momento | Re-ejecutar `daily_sync` |
| Discrepancia con TASK_TRACKING | TT refleja otro sprint | SPRINT_STATUS es fuente (R6) |
| Conflict en git push | Otra sesión editó | `git pull --rebase` + reintentar |

## 9. Skills invocadas

- `SKILL-STATUS-003`, `SKILL-QUERY-001`

## 10. Scripts invocados

- `SCRIPT-STATUS-003_update_sprint_status.py`

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0.0 | 2026-05-31 | Versión inicial. Dashboard operativo TL (vivo), diferenciado de CIERRE (final). 7 secciones canónicas. |
