# VTT.CARD-ISS-004 — TL decide acción del Issue (4 opciones)

| Campo | Valor |
|---|---|
| **Código** | `VTT.CARD-ISS-004` |
| **Tipo** | `CARD-std` |
| **Versión** | 1.0 |
| **Aplica cuando** | `task.phase = execution AND agent.role = TL` |
| **Requiere Cards previas** | `CARD-ISS-003` |
| **Pertenece a** | WORKFLOW-ASG-001.037 |
| **Tokens estimados** | ~1,350 |

---

## 4 opciones (mutuamente excluyentes)

### Opción A — `create_corrective_task`

**Cuándo:** critical con downstream, conflicto TI vigente, bug reproducible, scope creep.

```bash
# El TL escribe ASSIGNMENT.md + lista de CAs a mano (no automatizable)

python $VTT_SETUP/02.normativa/04.Scripts/task/SCRIPT-TASK-001_create_corrective.py \
  --source-issue-id "$ISSUE_ID" \
  --parent-task-id "$PARENT_TASK_ID" \
  --assignment-md "$ASSIGNMENT_PATH" \
  --cas-json "$CAS_PATH" \
  --assignee-role "<BE|FE|...>" \
  --sprint "$S"
```

El script crea tarea hija + asigna agente + sube ASSIGNMENT + crea CAs + dependency `blocks` parent → child.

Issue queda en `pending_corrective`. La correctiva sigue el ciclo completo del PROTOCOL (**recursión**). Cuando correctiva → `task_approved`, sistema VTT cierra Issue + auto-resume parent.

### Opción B — `resolve_inline`

**Cuándo:** fix NO requiere salir de `allowedPaths`, NO cambia scope, ≤1h.

```bash
# Comment con instrucciones específicas al agente
curl -X POST "$VTT_BASE_URL/api/tasks/<PARENT_TASK_ID>/comments" \
  -H "Authorization: Bearer $VTT_TOKEN" \
  -d '{
    "comment": "Resolver inline:\n1. <Paso 1>\n2. <Paso 2>\nNo cambiar scope. Reportar cuando esté.",
    "authorId": "<TL_UUID>"
  }'

# Cerrar Issue
curl -X PATCH "$VTT_BASE_URL/api/issues/<ISSUE_ID>" \
  -H "Authorization: Bearer $VTT_TOKEN" \
  -d '{"status":"resolved","resolution":"Resuelto inline — ver comment en tarea"}'
```

Auto-resume dispara → parent vuelve a `task_in_progress`.

### Opción C — `accept_workaround` + tech_debt

**Cuándo:** workaround menor aceptable, requiere tracking para sprint futuro.

```bash
# 1. Crear TI tech_debt
curl -X POST "$VTT_BASE_URL/api/projects/<PROJECT_ID>/trackable-items" \
  -H "Authorization: Bearer $VTT_TOKEN" \
  -d '{
    "typeCode":"tech_debt",
    "title":"Workaround aceptado: <síntoma> (ISS-<ID>)",
    "description":"<descripción + por qué se acepta + qué resolver en futuro>",
    "priority":"medium",
    "statusCode":"ti_draft"
  }'

# 2. Vincular al próximo sprint
curl -X POST "$VTT_BASE_URL/api/sprints/<NEXT_SPRINT_ID>/trackable-items" \
  -d '{"trackableItemId":"<TI_ID>"}'

# 3. Instrucciones al agente + cerrar Issue (PATCH issue status=resolved)
```

> ⚠️ **TI tech_debt OBLIGATORIO.** NO se acepta workaround sin tracking.

### Opción D — `reject_issue`

**Cuándo:** Issue mal reportado, no es bloqueante, agente puede continuar.

```bash
# Justificación clara
curl -X POST "$VTT_BASE_URL/api/issues/<ISSUE_ID>/comments" \
  -d '{"comment":"Issue rechazado.\nRazón: <justificación específica>\nAcción: continuar con ASSIGNMENT original.","authorId":"<TL_UUID>"}'

# Cerrar como wont_fix
curl -X PATCH "$VTT_BASE_URL/api/issues/<ISSUE_ID>" \
  -d '{"status":"wont_fix","resolution":"<justificación>"}'
```

Auto-resume dispara.

## Status final del Issue por opción

| Opción | Issue status final |
|---|---|
| A `create_corrective_task` | `pending_corrective` (cierra cuando correctiva aprueba) |
| B `resolve_inline` | `resolved` |
| C `accept_workaround` | `resolved` |
| D `reject_issue` | `wont_fix` |

## Auto-resume

Sistema VTT auto-resume el parent task en **B, C, D**. En **A**, espera la aprobación de la correctiva.

## Final (común) — Actualizar SPRINT_STATUS

Invocar **CARD-EXE-009** con `trigger_event=issue_resolved`.

## Si falla

| Síntoma | Acción |
|---|---|
| `resolve_inline` requiere salir de allowedPaths | Cambiar a Opción A (correctiva) |
| `accept_workaround` sin TI creado | Crear TI post-facto + vincular sprint |
| Auto-resume no dispara | Verificar `task.onHoldIssueId` apunta al Issue resuelto |
| Tarea correctiva sin `sourceIssueId` | PATCH /tasks/:id con campo |

## Output

Acción ejecutada + Issue cerrado con status correspondiente + agente notificado + SPRINT_STATUS actualizado. Auto-resume dispara (B/C/D) o espera (A).
