# VTT.WORKFLOW-ASG-001.037 — TL decide acción (correctiva/inline/workaround/reject)

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-ASG-001.037` |
| **Pertenece a** | `VTT.PROTOCOL-ASG-001` §5.4.4 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-05-31 |
| **Aplica a** | TL Reviewer post `.011` |
| **Reglas Nivel 0** | `RULE-SCRIPT-001` |
| **CARD asociada** | `VTT.CARD-ISS-004` |

---

## 1. Propósito

Formalizar las **4 opciones de resolución** del TL tras analizar Issue:
- A `create_corrective_task` — tarea hija con `sourceIssueId` (recursión PROTOCOL)
- B `resolve_inline` — agente arregla en misma tarea
- C `accept_workaround` + tech_debt — TI creado
- D `reject_issue` — Issue no aplica

## 2. Inputs

| Input | Tipo | Descripción |
|---|---|---|
| `issue_id` | UUID | |
| `tl_id` | UUID | |
| `action` | enum | A/B/C/D |
| `instructions_for_agent` | string | opcional (B, C) |
| `rejection_reason` | string | requerido si D |
| `corrective_task_id` | UUID | requerido si A |
| `tech_debt_ti_id` | UUID | requerido si C |

## 3. Precondiciones

- `.011` ejecutado (Issue clasificado)
- Si S1/S2: PM consultado
- Tarea origen en `task_on_hold`

## 4. Reglas

| # | Regla |
|---|---|
| R1 | 4 opciones mutuamente excluyentes |
| R2 | `create_corrective_task` si: critical+downstream, conflicto TI, bug reproducible |
| R3 | `resolve_inline` solo si NO requiere salir de allowedPaths NI cambio de scope |
| R4 | `accept_workaround` REQUIERE TI tech_debt creado y vinculado a sprint próximo |
| R5 | `reject_issue` REQUIERE justificación clara |
| R6 | Status final Issue: `pending_corrective` (A) / `resolved` (B,C) / `wont_fix` (D) |
| R7 | Notificar agente con instrucciones específicas |

## 5. Pasos

### OPCIÓN A — `create_corrective_task`

#### A.1 — TL escribe ASSIGNMENT correctivo (manual)

#### A.2 — Definir CAs (≥1 obligatorio)

#### A.3 — Ejecutar script
```bash
python $VTT_SETUP/02.normativa/04.Scripts/task/SCRIPT-TASK-001_create_corrective.py \
  --source-issue-id "$ISSUE_ID" \
  --parent-task-id "$PARENT_TASK_ID" \
  --assignment-md "$ASSIGNMENT_PATH" \
  --cas-json "$CAS_PATH" \
  --assignee-role "<BE|FE|...>" \
  --sprint "$S"
```

Script: crear tarea hija + asignar + subir ASSIGNMENT + crear CAs + dependency `blocks`.

#### A.4 — Notificar agente
Comment con link correctiva.

#### A.5 — Cerrar Issue como `pending_corrective`

---

### OPCIÓN B — `resolve_inline`

#### B.1 — Validar viable (R3)

#### B.2 — Comment con instrucciones específicas

#### B.3 — Cerrar Issue `resolved`

#### B.4 — Auto-resume dispara

---

### OPCIÓN C — `accept_workaround` + tech_debt

#### C.1 — Crear TI `tech_debt`
```bash
curl -X POST "$VTT_BASE_URL/api/projects/<PROJECT_ID>/trackable-items" \
  -d '{"typeCode":"tech_debt","title":"...","description":"...","priority":"medium","statusCode":"ti_draft"}'
```

#### C.2 — Vincular TI a sprint próximo

#### C.3 — Comment instrucciones workaround

#### C.4 — Cerrar Issue `resolved` con `resolution` que mencione el TI

---

### OPCIÓN D — `reject_issue`

#### D.1 — Justificación clara

#### D.2 — Cerrar Issue `wont_fix`

#### D.3 — Notificar agente

---

### Paso final (todas las opciones) — Actualizar SPRINT_STATUS

Invocar `WORKFLOW-ASG-001.028` con `trigger_event=issue_resolved`.

## 6. Outputs

| Output | Descripción |
|---|---|
| `action_executed` | A/B/C/D |
| `corrective_task_id` | si A |
| `tech_debt_ti_id` | si C |
| `issue_status_final` | `pending_corrective`/`resolved`/`wont_fix` |
| `auto_resume_will_trigger` | bool (true en B/C/D) |

## 7. Validación

Issue cerrado con status correspondiente + agente notificado + SPRINT_STATUS actualizado.

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| `resolve_inline` requiere salir allowedPaths | Mal evaluado | Cambiar a A |
| `accept_workaround` sin TI | Olvido | Crear TI post-facto |
| Auto-resume no dispara | onHoldIssueId mismatch | Verificar + forzar |
| Correctiva sin sourceIssueId | Falta flag | PATCH /tasks/:id |

## 9. Skills invocadas

- `SKILL-ISSUE-003`, `SKILL-TASK-001` (A), `SKILL-TRK-001` (C), `SKILL-COMMENT-001` (todas)

## 10. Scripts invocados

- `SCRIPT-ISSUE-003_resolve_issue.py`
- `SCRIPT-TASK-001_create_corrective.py` (A)

## 11. Sub-workflows invocados

- `WORKFLOW-ASG-001.028` (siempre, al final)
- Recursión a `PROTOCOL-ASG-001 §5.2` (Opción A)

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0.0 | 2026-05-31 | Versión inicial. 4 opciones mutuamente excluyentes con sub-flujos. Auto-resume en B/C/D. Recursión en A. |
