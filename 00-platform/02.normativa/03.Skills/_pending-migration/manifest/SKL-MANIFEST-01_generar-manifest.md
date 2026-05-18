# SKL-MANIFEST-01 — Generar/Actualizar Task Manifest

**Categoría:** MANIFEST
**Aplica a:** Agente ejecutor (v1.0) + TL Reviewer (v1.5)
**Versión:** 5.0
**Tokens estimados:** ~200
**Schema del manifest:** v1.2

**Versiones del manifest (instance):**
- **v1.0** — generada por el **agente ejecutor** al final de su workflow (paso 15)
- **v1.5** — generada por el **TL Reviewer** al cerrar la tarea (paso 14 del cierre)

**Changelog v4.1 → v5.0 (BREAKING):**
- ELIMINADO `delivery.skl_report_01_full` (contaminaba el JSON con texto duplicado de hasta 12K chars por manifest)
- ELIMINADO `delivery.skl_report_01_source`
- NUEVOS campos separados por sección del SKL-REPORT-01 (cada sección = un campo estructurado del manifest)
  - `delivery.what_was_done` (string corto)
  - `delivery.deliverables_actual[].what` (descripción por archivo — habilita query "tareas que tocaron archivo X")
  - `delivery.development_log_path` (puntero, no contenido)
  - `delivery.devlog_entries[]` (estructurado, no solo summary)
  - `delivery.findings`, `delivery.adrs_taken`, `delivery.derived_tasks`, `delivery.notes`
  - `delivery.review_gate` (objeto estructurado)
  - `delivery.git.commit_message`
- Motivo: el manifest es ÍNDICE, no contenedor. El report completo vive en el archivo de disco (auditoría humana). Campos separados permiten queries SQL precisas según IMPROVE-002.
- Schema bump 1.1 → 1.2 (campos nuevos en `delivery`)
- El comment de VTT sigue siendo extracto navegable (~8-10 líneas + link al archivo)

**Changelog v4.0 → v4.1:** (deprecado por v5.0)
- Lectura de `skl_report_01_full` desde archivo. Ya NO aplica — el campo se eliminó.

**Changelog v3.0 → v4.0:**
- Schema bump 1.0 → 1.1 (bloque opcional `delivery.operations` para tareas DevOps/operación)
- Convención: `brief.note`, `assignment.note`, `delivery.git.note` cuando son `null` intencional

---

## ⚠️ Regla crítica de orden

> **NUNCA generar el manifest prematuramente.** Va AL FINAL del workflow correspondiente.

| Quién | Generar manifest DESPUÉS de | Si lo generas antes |
|---|---|---|
| **Agente** | Paso 14 propio: attachments + status `task_in_review` + PR(s) + SKL-REPORT-01 (archivo en disco + comment en VTT) | Campos `null` en `delivery.what_was_done`, `vtt_attachments.devlog_id`, `git.pr_url` |
| **TL Reviewer** | Paso 13 propio: FASE B (TIs nuevos + evidencias + devlog resolved) + APR-TL + status `task_completed` | `review.tl_review.comment_id: null`, `delivery.dynamic_model_actions: missing` |

**Lección PROC-MANIFEST-01:** la primera versión de MS-284 tuvo 10+ campos null porque se generó prematuramente.

---

# PARTE A — Manifest v1.0 (rol: AGENTE EJECUTOR)

## Precondiciones (agente)

- Status de la tarea = `task_in_review`
- Reporte completo guardado en `knowledge/agent-tasks/reports/<phase>/<sprint>/<TASK_ID>_REPORT.md` (fuente para extraer campos)
- Comment extracto SKL-REPORT-01 posteado en VTT (8-10 líneas + link al archivo)
- Attachments subidos: devlog + code_logic (real o placeholder N/A)
- PRs creados en GitHub con URL específica
- CAs reportados con `PATCH /criteria/:cid` `{status:"met"}`

## Variables del agente

- `$TOKEN` — JWT del agente (SKL-AUTH-01)
- `$TASK_ID` — MS-XXX
- `$AGENT_UUID` — TU UUID
- `$PROJECT_ID` — UUID del proyecto

## Esquema v1.0 — lo que el agente genera

```json
{
  "schema_version": "1.2",
  "manifest_id": "MS-XXX",
  "generated_at": "<ISO timestamp>",
  "generated_by": "<AGENT_UUID>",
  "generation_note": "v1.0 generado por agente al cerrar workflow. TL Reviewer agregara review.tl_review en v1.5.",
  "last_updated": "<ISO timestamp>",
  "last_updated_block": "delivery",

  "task": {
    "id": "MS-XXX",
    "title": "...",
    "sprint": { "id": "<uuid>", "name": "S1 - ..." },
    "stage": "development",
    "assignee": { "id": "<AGENT_UUID>", "role": "..." },
    "estimated_hours": N,
    "actual_hours": N,
    "complexity": "LOW|MEDIUM|HIGH",
    "category": "development|deployment|documentation",
    "sdlc_catalog_id": "4.X.Y",
    "current_status": "task_in_review",
    "dependencies_upstream": [...]
  },

  "brief": {
    "vtt_attachment_id": "<uuid>",
    "file_path": "knowledge/agent-tasks/briefs/04-development/S01/BRIEF_MS-XXX_<slug>.md"
  },
  "assignment": {
    "vtt_attachment_id": "<uuid>",
    "file_path": "knowledge/agent-tasks/assignments/04-development/S01/ASSIGNMENT_MS-XXX_<slug>.md",
    "criteria_count": N
  },
  "agent_message": {
    "template_version": "3.0",
    "agent_role": "<rol>",
    "agent_uuid": "<AGENT_UUID>",
    "generated_by_script": "scripts/gen_mensaje.py"
  },

  "delivery": {
    "delivered_at": "<ISO timestamp>",
    "delivered_by": "<AGENT_UUID>",
    "vtt_report_comment_id": "<id del comment-extracto en VTT (max 5000 chars)>",
    "report_file_path": "knowledge/agent-tasks/reports/<phase>/<sprint>/<TASK_ID>_REPORT.md",

    "what_was_done": "Texto corto narrativo (max ~80 palabras) extraido de la seccion 'Lo que se hizo' del report.",

    "deliverables_actual": [
      {
        "path": "memory-service-backend/src/services/foo.service.ts",
        "state": "created|modified",
        "what": "Descripcion corta de que se hizo en este archivo (extraida de la lista 'Codigo' del report)"
      }
    ],

    "development_log_path": "knowledge/development-log/2026-MM-DD_<TASK_ID>_<slug>.md",
    "code_logic_files": [
      "memory-service-backend/knowledge/code-logic/.../X.LOGIC.md"
    ],
    "code_logic_attachment_strategy": {
      "placeholder_uploaded": false,
      "placeholder_attachment_id": null,
      "reason": "..."
    },

    "vtt_attachments": {
      "brief_id": "<uuid>",
      "assignment_id": "<uuid>",
      "devlog_id": "<uuid>",
      "code_logic_ids": ["<uuid>"]
    },

    "criteria_results": [
      { "id": "<uuid>", "title": "CA-XX: ...", "status": "met", "criteriaTypeCode": "technical" }
    ],
    "criteria_summary": { "total": N, "met": N, "not_met": 0, "pending": 0 },

    "devlog_entries": [
      { "category": "decision|blocker|tech_debt|finding|observation",
        "severity": "low|medium|high",
        "title": "...",
        "status": "pending|resolved" }
    ],
    "devlog_summary": { "total": N, "by_category": { "decision": N, "blocker": N }, "all_resolved_by_tl": false },

    "findings": "Texto narrativo o 'N/A'. Bugs nuevos, observaciones tecnicas, deuda detectada no critica.",
    "adrs_taken": "Texto narrativo o 'N/A'. ADRs nuevos creados o ADRs existentes aplicados.",
    "derived_tasks": "Texto narrativo o 'N/A'. Tareas nuevas generadas (ej: MS-XXX para DevOps).",
    "notes": "Texto narrativo o 'N/A'. Contexto relevante para el revisor: merge recovery, edge cases, limitaciones.",

    "hardcode_check": {
      "executed": true,
      "findings_total": N,
      "findings_critical_high": 0,
      "false_positives_justified": N
    },

    "tests": {
      "framework": "Jest|Vitest|N/A",
      "tests_passing": N,
      "coverage_stmts": N.NN,
      "threshold_met": true
    },

    "trackable_items_actual": {
      "implements": [{ "code": "RF-XXX", "uuid": "<uuid>" }],
      "related_to": [{ "code": "AS-001", "uuid": "<uuid>" }]
    },

    "living_documents_declared_no_change": ["LD-XX"],

    "tech_debt_for_r2": [
      { "code_suggested": "DEBT-XXX-NN", "title": "...", "urgency": "low", "retroactive": false }
    ],

    "items_detected_for_tl_review": [
      { "type_suggested": "tech_debt", "code_suggested": "DEBT-XXX-NN", "description": "...", "urgency": "baja" }
    ],

    "how_to_verify": ["curl ...", "cd <repo> && npm test"],

    "review_gate": {
      "canProceedToReview": true,
      "entries_total": N,
      "resolved": N,
      "warnings": N
    },

    "git": {
      "branch": "feature/MS-XXX",
      "base_branch": "main",
      "pr_number": N,
      "pr_url": "https://github.com/NCoreSys/.../pull/N",
      "commit_sha": "<sha>",
      "commit_message": "<tipo>(<repo>) [MS-XXX]: Descripcion breve"
    },

    "metrics": { "actual_hours": N, "deliverables_count": N, "tests_passing": N }
  },

  "review": {
    "tl_review": null,
    "pm_approval": null
  },

  "indexes": {
    "implements_codes": [...],
    "related_to_codes": [...],
    "deliverables_paths": ["memory-service-backend/src/services/foo.service.ts"],
    "tech_debt_count": N,
    "criteria_met_ratio": "N/N",
    "devlog_entries_count": N,
    "devlog_resolved_count": N,
    "files_created_count": N
  }
}
```

> `review.tl_review` queda en `null`. El TL lo poblará en v1.5.
> `delivery.dynamic_model_actions` NO se incluye en v1.0. El TL lo agrega en v1.5.

## Tareas DevOps / operación — bloque `delivery.operations` (schema v1.1+)

Aplica a tareas con `task.category` ∈ `[deployment, devops, operation, sql_migration, rollback, smoke_test, config_change, restart_service]`.

Estas tareas típicamente NO tienen BRIEF/ASSIGNMENT/PR. Convención:

### Campos null intencionales con `note`

```json
{
  "brief": {
    "vtt_attachment_id": null,
    "file_path": null,
    "note": "DevOps tasks NO requieren BRIEF — description de la tarea es suficiente"
  },
  "assignment": {
    "vtt_attachment_id": null,
    "file_path": null,
    "note": "DevOps tasks NO requieren ASSIGNMENT — description de la tarea es suficiente"
  },
  "delivery": {
    "git": {
      "branch": null,
      "base_branch": null,
      "pr_url": null,
      "note": "Tarea de operación en prod — sin PR/branch/commit. SQL ejecutado directo via psql."
    }
  }
}
```

### Bloque `delivery.operations` completo

```json
{
  "delivery": {
    "operations": {
      "type": "sql_migration | deploy | rollback | config_change | smoke_test | restart_service",
      "executed_at": "<ISO timestamp>",
      "executed_by": "<UUID>",
      "environment": "production | staging | local",

      "sql_applied": "<SQL ejecutado, si aplica>",
      "commands_applied": ["comando 1", "comando 2"],

      "pre_checks": [
        { "check": "descripcion del check", "result": "estado antes" }
      ],
      "post_checks_passed": true,
      "post_checks_details": [
        { "check": "validacion 1", "result": "OK / valor obtenido" },
        { "check": "validacion 2", "result": "OK / valor obtenido" }
      ],

      "issue_resolved": "<uuid del issue VTT, si aplica>",
      "rollback_plan": "Pasos para revertir si falla — opcional pero recomendado",
      "rejection_history": "Si es re-entrega: motivo del rechazo previo y fix aplicado"
    }
  }
}
```

### Campos obligatorios vs opcionales en `operations`

| Campo | Obligatorio | Cuándo |
|---|---|---|
| `type` | ✅ Sí (si el bloque existe) | Siempre |
| `executed_at` | ✅ Sí | Siempre |
| `executed_by` | ✅ Sí | Siempre |
| `environment` | ✅ Sí | Siempre |
| `post_checks_passed` | ✅ Sí | Siempre |
| `post_checks_details` | ✅ Sí | Siempre (probar que la operación tuvo éxito) |
| `sql_applied` | ❌ Opcional | Solo si hay SQL |
| `commands_applied` | ❌ Opcional | Solo si hay comandos shell relevantes |
| `pre_checks` | ❌ Opcional pero recomendado | Estado del sistema antes |
| `issue_resolved` | ❌ Opcional | Si cierra un issue VTT |
| `rollback_plan` | ❌ Opcional pero recomendado | Producción |
| `rejection_history` | ⚠️ Obligatorio si es re-entrega | Tarea rechazada previamente |

### Ejemplo real (VTT-720)

```json
{
  "schema_version": "1.2",
  "manifest_id": "VTT-720",
  "task": {
    "id": "VTT-720",
    "title": "[DevOps] VTT-705: Aplicar migración document_versions en producción",
    "stage": "deployment",
    "category": "deployment",
    "current_status": "task_in_review"
  },
  "delivery": {
    "what_was_done": "Se aplicó ALTER TABLE document_versions ALTER COLUMN createdById DROP NOT NULL en producción. Pre/post checks OK.",
    "operations": {
      "type": "sql_migration",
      "executed_at": "2026-05-17T04:00:00Z",
      "executed_by": "<DEVOPS_UUID>",
      "environment": "production",
      "sql_applied": "ALTER TABLE document_versions ALTER COLUMN \"createdById\" DROP NOT NULL;",
      "pre_checks": [
        { "check": "current nullable state", "result": "createdById | NO | text" }
      ],
      "post_checks_passed": true,
      "post_checks_details": [
        { "check": "nullable changed", "result": "createdById | YES" },
        { "check": "FK fk_document_versions_user intact", "result": "confdeltype=n (SET NULL)" },
        { "check": "test INSERT with NULL createdById", "result": "INSERT 0 1, ROLLBACK applied" }
      ],
      "issue_resolved": "6ea5990e-632a-4bc2-8141-ba404b29dff6",
      "rejection_history": "Primera entrega completada con createdById NOT NULL. TL detectó bug, rechazó y solicitó ALTER incremental."
    }
  }
}
```

## Construcción del manifest — referencia de implementación

El agente construye el JSON con su lenguaje/herramienta preferida. Reglas:

1. **Recolectar IDs reales desde VTT** (no hardcodear):
   - `GET /api/tasks/$TASK_ID` → metadata de la tarea
   - `GET /api/tasks/$TASK_ID/criteria` → CAs con sus IDs y status
   - `GET /api/tasks/$TASK_ID/devlog` → entries para llenar `devlog_entries[]`
   - `GET /api/tasks/$TASK_ID/attachments` → IDs de brief, assignment, devlog, code_logic
   - `GET /api/tasks/$TASK_ID/comments` → ID del comment SKL-REPORT-01 extracto

2. **Extraer campos narrativos del report local** (`knowledge/agent-tasks/reports/.../<TASK_ID>_REPORT.md`):
   - `what_was_done` ← sección "Lo que se hizo"
   - `deliverables_actual[].what` ← cada bullet de la sección "Código"
   - `findings`, `adrs_taken`, `derived_tasks`, `notes` ← secciones homónimas
   - `review_gate` ← sección "Review gate al entregar"

3. **Validar antes de subir**:
   - Si `task.category=deployment` y `delivery.operations` falta → ABORT
   - Si `brief.vtt_attachment_id=null` y `brief.note=null` → ABORT (debe explicar el null)
   - Si `delivery.what_was_done` está vacío → ABORT (es el campo más consultado)

4. **Wrappear JSON en `.md`** y subir como attachment `fileType=manifest` (VTT no acepta JSON puro como MIME).

5. **Guardar copia local** en `knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>.json` + wrapper `.md`.

## Validación v1.0 (agente)

```bash
# Manifest subido como fileType=manifest
curl -s "$BASE/api/tasks/$TASK_ID/attachments" -H "Authorization: Bearer $TOKEN" | \
  jq '.data | map(select(.fileType=="manifest")) | length'  # >=1

# Schema version correcto
jq '.schema_version' knowledge/task-manifests/04-development/S01/$TASK_ID.json
# Esperado: "1.2"

# Campos narrativos NO null
jq '.delivery.what_was_done != null and (.delivery.what_was_done | length) > 20' $TASK_ID.json  # true

# Deliverables tienen "what" (no solo path+state)
jq '.delivery.deliverables_actual | all(.what != null)' $TASK_ID.json  # true

# Devlog entries estructurados (no solo summary)
jq '.delivery.devlog_entries | length == .delivery.devlog_summary.total' $TASK_ID.json  # true

# Index deliverables_paths poblado (habilita query "tareas que tocaron X")
jq '.indexes.deliverables_paths | length > 0' $TASK_ID.json  # true

# Si es tarea DevOps: validar operations completo
CATEGORY=$(jq -r '.task.category' $TASK_ID.json)
if echo "$CATEGORY" | grep -qE 'deployment|devops|operation|sql_migration|rollback'; then
  jq '.delivery.operations | (.type != null and .executed_at != null and .post_checks_passed != null)' $TASK_ID.json
  # Esperado: true
fi

# Si brief/assignment/git son null, deben tener note
jq '.brief | if .vtt_attachment_id == null then .note != null else true end' $TASK_ID.json
jq '.assignment | if .vtt_attachment_id == null then .note != null else true end' $TASK_ID.json
jq '.delivery.git | if .pr_url == null then .note != null else true end' $TASK_ID.json
```

---

# PARTE B — Manifest v1.5 (rol: TL REVIEWER)

## Precondiciones (TL Reviewer)

- v1.0 del agente existe como attachment en VTT
- FASE B del cierre ejecutada:
  - TIs nuevos creados desde `items_detected_for_tl_review` del v1.0
  - Evidencias agregadas a TIs heredados y nuevos con marker `[TASK:MS-XXX]`
  - Devlog entries marcados `resolved`
- APR-TL comment posteado
- Status moveado a `task_completed`

## Qué cambia entre v1.0 y v1.5

| Cambio | Acción |
|---|---|
| `current_status` | `"task_in_review"` → `"task_completed"` |
| `last_updated` | timestamp actual |
| `last_updated_block` | `"delivery"` → `"review.tl_review + delivery.dynamic_model_actions"` |
| `generation_note` | agregar nota TL |
| `delivery.dynamic_model_actions` | **NUEVO bloque** (no estaba en v1.0) |
| `delivery.devlog_summary.all_resolved_by_tl` | `false` → `true` |
| `delivery.devlog_entries[].status` | actualizar a `resolved` los que el TL cerró |
| `delivery.trackable_items_actual.related_to` | agregar TIs nuevos creados por TL |
| `delivery.tech_debt_for_r2` | agregar `ti_id` real a cada item ahora que existe en VTT |
| `review.tl_review` | **NUEVO objeto** con verdict, verifications, notes |

## Esquema agregado en v1.5

```json
{
  "delivery": {
    "dynamic_model_actions": {
      "new_tis_created": [
        { "code": "DEBT-XXX-NN", "id": "<uuid>", "linked_as": "related_to MS-XXX" }
      ],
      "evidences_added": [
        { "ti_code": "NFR-SEC-XX", "type": "link", "title": "[MS-XXX] [SX] ..." }
      ],
      "devlog_resolved_count": N,
      "note_defer_endpoint_missing": "...",
      "note_typecode_constraint": "..."
    }
  },
  "review": {
    "tl_review": {
      "reviewer_uuid": "<TL_UUID>",
      "verdict": "approved",
      "reviewed_at": "<ISO timestamp>",
      "moved_to_completed_at": "<ISO timestamp>",
      "comment_id": "<id del APR-TL comment>",
      "findings": [],
      "verifications": {
        "review_gate_verified": true,
        "criteria_evidence_verified": true,
        "living_docs_verified": true,
        "hardcode_check_verified": true,
        "deliverables_match_assignment": true,
        "dynamic_model_applied": true
      },
      "notes": "Modelo dinamico aplicado: ..."
    },
    "pm_approval": { "approver_uuid": null, "approved_at": null, "comment_id": null }
  }
}
```

## Construcción v1.5 — referencia de implementación

1. Leer v1.0 del disco (el agente lo dejó).
2. Actualizar campos del cambio (ver tabla anterior).
3. Agregar `delivery.dynamic_model_actions` con datos de FASE B del cierre.
4. Agregar `review.tl_review` con verdict + verifications + notes.
5. Reescribir JSON local + wrappear `.md`.
6. Subir como **NUEVO** attachment `fileType=manifest` (VTT no permite reemplazar; el v1.0 queda como historial).

## Validación v1.5 (TL)

```bash
# Hay al menos 2 manifests (v1.0 del agente + v1.5 del TL)
curl -s "$BASE/api/tasks/$TASK_ID/attachments" -H "Authorization: Bearer $TOKEN" | \
  jq '.data | map(select(.fileType=="manifest")) | length'  # >=2

# v1.5 tiene review.tl_review poblado
jq '.review.tl_review.verdict' $TASK_ID.json  # "approved"

# dynamic_model_actions presente
jq '.delivery.dynamic_model_actions | keys' $TASK_ID.json
# incluye new_tis_created, evidences_added, devlog_resolved_count

# current_status correcto
jq '.task.current_status' $TASK_ID.json  # "task_completed"

# devlog_summary.all_resolved_by_tl=true
jq '.delivery.devlog_summary.all_resolved_by_tl' $TASK_ID.json  # true
```

---

## Versionado del manifest

### Versiones del INSTANCE (v1.0, v1.5, v2.0)

Es la versión del manifest individual de una tarea. Cambia cuando se actualizan bloques:

| Versión | Quién genera | Cambio |
|---|---|---|
| v1.0 | Agente | Entrega original — bloques task/brief/assignment/agent_message/delivery |
| v1.5 | TL Reviewer | Agrega review.tl_review + dynamic_model_actions; status → task_completed |
| v2.0 (futuro) | PM | Agrega review.pm_approval; status → task_approved |

### Versiones del SCHEMA (1.0, 1.1, 1.2)

Es la versión del schema JSON declarado en `schema_version`. Define qué campos existen:

| Schema | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-05-13 | Schema inicial — bloques base, sin operations |
| 1.1 | 2026-05-17 | Agrega bloque opcional `delivery.operations` (DevOps) + convención `note` en campos null intencionales |
| **1.2** | **2026-05-17** | **ELIMINA `skl_report_01_full` (basura). AGREGA campos separados por sección del SKL-REPORT-01: `what_was_done`, `deliverables_actual[].what`, `development_log_path`, `devlog_entries[]`, `findings`, `adrs_taken`, `derived_tasks`, `notes`, `review_gate`, `git.commit_message`. AGREGA `indexes.deliverables_paths` para queries de archivos tocados.** |

Actualizar `last_updated` y `last_updated_block` cada vez. Los manifests viejos NO se borran (no hay DELETE attachments) — quedan como historial.

---

## Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| Agente: `what_was_done: null` | No extrajo la sección del report local | Leer `report_file_path` y copiar literal la sección "Lo que se hizo" |
| Agente: `deliverables_actual[].what` faltante | Solo copió path+state | Cada deliverable debe tener `what` (descripción del bullet "Código" del report) |
| Agente: `devlog_entries: []` con `devlog_summary.total>0` | Solo llenó summary | Llenar también el array estructurado |
| Agente: `indexes.deliverables_paths: []` | No espejó deliverables_actual.path | Indexar todos los paths para queries de IMPROVE-002 |
| Agente: `vtt_attachments.devlog_id: null` | Devlog no subido como attachment antes del manifest | Verificar Paso 14 |
| Agente: incluyó `review.tl_review` poblado | Confusión de rol | Dejar `null`; es del TL |
| TL: `dynamic_model_actions: missing` | SKL-DYNAMIC-MODEL-01 no aplicada antes del manifest | Ejecutar FASE B del cierre antes |
| TL: `review.tl_review.comment_id: null` | APR-TL no posteado | Postear comment antes de generar v1.5 |
| 400 al subir manifest | JSON puro rechazado | Wrappear en `.md` con bloque ` ```json ` |
| Manifest reemplazado en vez de agregar | Confusión: VTT no permite reemplazar | Subir como NUEVO attachment; el viejo queda |
| Tarea DevOps sin `delivery.operations` | Falta trazabilidad de qué se ejecutó | Llenar bloque completo (schema v1.2) |
| `brief.vtt_attachment_id: null` sin `note` | Validador no sabe si es intencional o error | Agregar campo `note` explicando |
| `schema_version: "1.0"` o `"1.1"` con campos separados | Inconsistencia schema/contenido | Bumpear a `"1.2"` |
| Tarea re-entregada sin `rejection_history` | TL no sabe por qué se rechazó la primera vez | Agregar `operations.rejection_history` |
| Campo `skl_report_01_full` presente | Schema viejo (v1.0/v1.1) | Eliminar; reemplazar por campos separados v1.2 |

---

## Documentos relacionados

- `PROCESO_CIERRE_TAREA_v2.md` — Workflow donde se ejecuta v1.5
- `GUIA_MANIFEST_PARA_AGENTES.md` — Guía descriptiva del manifest (qué secciones, qué reglas)
- `SKL-REPORT-01_entrega-tarea.md` — Genera el report local del que se extraen los campos narrativos
- `GUIA_REVISION_TAREA_TL_REVIEWER.md` — Guía completa TL (rol v1.5)
- `SKL-DYNAMIC-MODEL-01_cierre-modelo-dinamico.md` — Skill que pobla `dynamic_model_actions`
- `IMPROVE-002_bd_manifiestos_y_tis.md` — BD de manifests queryable (consume estos campos separados)
- `OPERATIVO_TL_MEMORY-SERVICE.md` v4.0 — Operativo del rol unificado TL
