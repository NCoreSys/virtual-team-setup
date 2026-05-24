# VTT.SKILL-MAN-001 — Task Manifest (Generar / Validar / Subir)

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-MAN-001` |
| **Categoría** | MAN (Manifest) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-17 |
| **Aplica a** | Agente ejecutor (v1.0) + TL Reviewer (v1.5) |
| **Tokens estimados** | ~250 |
| **Cuándo se usa** | Al cierre de tarea: agente genera v1.0 (paso final de su workflow), TL genera v1.5 (paso final del cierre) |
| **Schema soportado** | v1.2 |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `action` | enum | sí | Una de: `fetch_vtt_data` / `parse_report` / `add_operations_block` / `compose` / `validate` / `save_local` / `upload` / `download_v10` / `enrich_to_v15` / `add_dynamic_actions` / `add_tl_review` |
| `task_id` | string (MS-XXX) | sí | ID externo de la tarea |
| `version` | enum (`1.0` / `1.5`) | sí | Instance version a generar |
| `agent_uuid` | uuid | sí (v1.0) | UUID del agente ejecutor (para v1.0) o TL Reviewer (para v1.5) |
| `report_path` | path | sí (v1.0) | Solo para v1.0 — ruta al reporte SKL-REPORT-01 local |
| `phase` | string | sí | Ej. `04-development` — para path local del manifest |
| `sprint` | string | sí | Ej. `S01` |
| `v10_attachment_id` | uuid | sí (v1.5) | Solo para v1.5 — para descargar v1.0 del agente |
| `dynamic_actions_data` | dict | sí (v1.5) | Datos del Modelo Dinámico aplicado por el TL |
| `verifications_data` | dict | sí (v1.5) | Los 6+2 flags de `review.tl_review.verifications` |
| `apr_tl_comment_id` | uuid | sí (v1.5) | Comment APR-TL posteado por el TL |

> **Regla contractual:** Los inputs son fijos. Si parecen insuficientes para un caso particular, NO es que la Skill esté mal — es que el Workflow está mal definido y debe pasar los datos extras como parte de los dicts existentes.

---

## Precondición

- JWT válido obtenido (`SKL-AUTH-01`)
- Para v1.0: las 8 precondiciones de `WORKFLOW-MAN-001.003 §3` cumplidas
- Para v1.5: las 11 precondiciones de `WORKFLOW-MAN-001.004 §3` cumplidas
- Existe `02.normativa/04.Scripts/manifest/schema_v1.2.json` (schema validable) — opcional pero recomendado para validar formalmente

---

## Variables del entorno

```bash
$TOKEN              # JWT (de SKL-AUTH-01)
$VTT_BASE_URL       # Base URL backend (default http://77.42.88.106:3000)
$AGENT_UUID         # UUID del actor que invoca (agente o TL)
$PROJECT_ID         # UUID del proyecto en VTT
```

> Política: los UUIDs específicos del task (taskId, attachmentIds) son **inputs**, no env vars.

---

## Esquema v1.2 — referencia completa

> El schema completo vive como JSON Schema validable en `02.normativa/04.Scripts/manifest/schema_v1.2.json` (a generarse junto con el script).
> Esta sección documenta la estructura **conceptual**. Para implementar, usar el JSON Schema.

### Bloques top-level

```
{
  "schema_version": "1.2",                        // SIEMPRE "1.2"
  "manifest_id": "MS-XXX",                        // == task_id
  "generated_at": "<ISO timestamp UTC>",
  "generated_by": "<UUID del actor>",             // agent_uuid para v1.0, tl_uuid para v1.5
  "generation_note": "...",                       // breve nota explicativa
  "last_updated": "<ISO timestamp>",
  "last_updated_block": "...",                    // qué bloque se modificó por última vez

  "task": { ... },                                // metadata de la tarea
  "brief": { ... },                               // attachment del brief
  "assignment": { ... },                          // attachment del assignment
  "agent_message": { ... },                       // metadata del mensaje al agente

  "delivery": { ... },                            // GRAN bloque — qué entregó el agente
  "review": { ... },                              // review.tl_review (v1.5) + review.pm_approval (v2.0 futuro)
  "indexes": { ... }                              // campos derivados para queries de IMPROVE-002
}
```

### Bloque `task`

```json
{
  "id": "MS-XXX",
  "title": "...",
  "sprint": { "id": "<uuid>", "name": "S1 - ..." },
  "stage": "development|design|testing|deployment",
  "assignee": { "id": "<UUID>", "role": "BE|DB|FE|...", "email": "..." },
  "estimated_hours": <N>,
  "actual_hours": <N>,
  "complexity": "LOW|MEDIUM|HIGH",
  "category": "development|deployment|documentation|testing|design|devops|operation|sql_migration|rollback|smoke_test|config_change|restart_service",
  "sdlc_catalog_id": "4.X.Y",
  "current_status": "task_in_review (v1.0) | task_completed (v1.5)",
  "dependencies_upstream": [...]
}
```

### Bloque `delivery` (campos clave)

```json
{
  "delivered_at": "<ISO>",
  "delivered_by": "<AGENT_UUID>",
  "vtt_report_comment_id": "<uuid>",
  "report_file_path": "knowledge/agent-tasks/reports/<phase>/<sprint>/<TASK_ID>_REPORT.md",

  "what_was_done": "Texto narrativo corto (~80 palabras max) — campo más consultado",

  "deliverables_actual": [
    { "path": "...", "state": "created|modified", "what": "qué se hizo en este archivo" }
  ],

  "development_log_path": "...",
  "code_logic_files": ["..."],
  "code_logic_attachment_strategy": { "placeholder_uploaded": false, "placeholder_attachment_id": null, "reason": "..." },

  "vtt_attachments": {
    "brief_id": "<uuid>", "assignment_id": "<uuid>",
    "devlog_id": "<uuid>", "code_logic_ids": ["<uuid>"]
  },

  "criteria_results": [
    { "id": "<uuid>", "title": "CA-XX: ...", "status": "met", "criteriaTypeCode": "technical" }
  ],
  "criteria_summary": { "total": N, "met": N, "not_met": 0, "pending": 0 },

  "devlog_entries": [
    { "category": "decision|blocker|tech_debt|finding|observation",
      "severity": "low|medium|high|critical",
      "title": "...",
      "status": "pending|resolved|wont_fix" }
  ],
  "devlog_summary": { "total": N, "by_category": {...}, "all_resolved_by_tl": false },

  "findings": "Texto narrativo o N/A",
  "adrs_taken": "Texto narrativo o N/A",
  "derived_tasks": "Texto narrativo o N/A",
  "notes": "Texto narrativo o N/A",

  "hardcode_check": { "executed": true, "findings_total": N, "findings_critical_high": 0, "false_positives_justified": N },
  "tests": { "framework": "Jest|Vitest|N/A", "tests_passing": N, "coverage_stmts": N.NN, "threshold_met": true },

  "trackable_items_actual": {
    "implements": [{ "code": "RF-XXX", "uuid": "<uuid>" }],
    "related_to": [{ "code": "AS-001", "uuid": "<uuid>" }]
  },

  "living_documents_declared_no_change": ["LD-XX"],

  "tech_debt_for_r2": [
    { "code_suggested": "DEBT-XXX-NN", "ti_id": "<uuid o null en v1.0>", "title": "...", "urgency": "low" }
  ],

  "items_detected_for_tl_review": [
    { "type_suggested": "tech_debt", "code_suggested": "DEBT-XXX-NN", "description": "...", "urgency": "baja" }
  ],

  "how_to_verify": ["curl ...", "npm test"],

  "review_gate": {
    "canProceedToReview": true, "entries_total": N, "resolved": N, "warnings": N
  },

  "git": {
    "branch": "feature/MS-XXX",
    "base_branch": "main",
    "pr_number": N,
    "pr_url": "https://github.com/NCoreSys/.../pull/N",
    "commit_sha": "<sha>",
    "commit_message": "<tipo>(<repo>) [MS-XXX]: ..."
  },

  "operations": { ... },              // SOLO si task.category ∈ [deployment,devops,...] — ver §Bloque operations

  "dynamic_model_actions": { ... }    // SOLO en v1.5 — agregado por TL
}
```

### Bloque `delivery.operations` (DevOps)

```json
{
  "type": "sql_migration|deploy|rollback|config_change|smoke_test|restart_service",
  "executed_at": "<ISO>",
  "executed_by": "<UUID>",
  "environment": "production|staging|local",
  "sql_applied": "<SQL ejecutado, si aplica>",
  "commands_applied": ["..."],
  "pre_checks": [{ "check": "...", "result": "..." }],
  "post_checks_passed": true,
  "post_checks_details": [{ "check": "...", "result": "..." }],
  "issue_resolved": "<uuid o null>",
  "rollback_plan": "...",
  "rejection_history": "<texto si es re-entrega>"
}
```

### Bloque `review.tl_review` (v1.5)

```json
{
  "reviewer_uuid": "<TL_UUID>",
  "verdict": "approved|rejected",
  "reviewed_at": "<ISO>",
  "moved_to_completed_at": "<ISO>",
  "comment_id": "<apr_tl_comment_id>",
  "findings": [],
  "verifications": {
    "review_gate_verified": true,
    "criteria_evidence_verified": true,
    "living_docs_verified": true,
    "hardcode_check_verified": true,
    "deliverables_match_assignment": true,
    "dynamic_model_applied": true,
    "worktree_discipline_verified": true,
    "allowed_paths_respected": true
  },
  "notes": "..."
}
```

### Bloque `delivery.dynamic_model_actions` (v1.5)

```json
{
  "new_tis_created": [{ "code": "DEBT-XXX-NN", "id": "<uuid>", "linked_as": "..." }],
  "evidences_added": [{ "ti_code": "...", "ti_id": "<uuid>", "type": "link", "title": "[MS-XXX] [SX] ..." }],
  "devlog_resolved_count": N,
  "devlog_wont_fix_count": N,
  "notes": "...",
  "note_defer_endpoint_missing": "...",
  "note_typecode_constraint": "..."
}
```

### Bloque `indexes`

Campos derivados que IMPROVE-002 indexa para queries SQL rápidas:

```json
{
  "implements_codes": [...],
  "related_to_codes": [...],
  "deliverables_paths": [...],         // espejo de delivery.deliverables_actual[].path
  "tech_debt_count": N,
  "criteria_met_ratio": "N/N",
  "devlog_entries_count": N,
  "devlog_resolved_count": N,
  "files_created_count": N
}
```

---

## Mapeo SKL-REPORT-01 → manifest (v1.0)

| Sección del reporte | Campo del manifest | Tipo |
|---|---|---|
| `Lo que se hizo:` | `delivery.what_was_done` | string ≤80 palabras |
| `Código:` (bullets de archivos) | `delivery.deliverables_actual[]` | array `{path, state, what}` |
| `Development Log:` | `delivery.development_log_path` | string (solo path) |
| `Code Logic:` | `delivery.code_logic_files[]` | array strings (paths) |
| `Criterios de aceptación:` (tabla) | `delivery.criteria_results[]` + `criteria_summary` | array + summary |
| `Devlog entries registrados en VTT:` | `delivery.devlog_entries[]` + `devlog_summary` | array estructurado + summary |
| `Findings / Deuda técnica:` | `delivery.findings` | string |
| `ADRs tomados:` | `delivery.adrs_taken` | string |
| `TrackableItems creados o vinculados:` | `delivery.trackable_items_actual` | objeto |
| `Items detectados para trackeo:` | `delivery.items_detected_for_tl_review[]` | array |
| `Tareas derivadas generadas:` | `delivery.derived_tasks` | string |
| `Cómo verificar:` | `delivery.how_to_verify[]` | array strings |
| `Notas:` | `delivery.notes` | string |
| `Review gate al entregar:` | `delivery.review_gate` | objeto |
| `Commit:` | `delivery.git.{commit_sha, commit_message}` | strings |
| `PR:` | `delivery.git.{pr_url, pr_number}` | string + number |

---

## Ejecución

La Skill orquesta `VTT.SCRIPT-MAN-001` (`gen_task_manifest.py`) con la `action` correspondiente:

### v1.0 (agente)

```bash
# Acción atómica: el script hace fetch_vtt_data + parse_report + compose + validate + save_local + upload
python 02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py \
  --task-id "$TASK_ID" \
  --version "1.0" \
  --agent-uuid "$AGENT_UUID" \
  --report-path "knowledge/agent-tasks/reports/$PHASE/$SPRINT/${TASK_ID}_REPORT.md" \
  --phase "$PHASE" \
  --sprint "$SPRINT" \
  --upload
```

### v1.5 (TL)

```bash
python 02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py \
  --task-id "$TASK_ID" \
  --version "1.5" \
  --tl-uuid "$TL_UUID" \
  --v10-attachment-id "$V10_ATTACHMENT_ID" \
  --apr-tl-comment-id "$APR_TL_COMMENT_ID" \
  --dynamic-actions-json "/tmp/${TASK_ID}_dynamic_actions.json" \
  --verifications-json "/tmp/${TASK_ID}_verifications.json" \
  --phase "$PHASE" \
  --sprint "$SPRINT" \
  --upload
```

Output del script: stdout JSON con `{success, attachment_id, manifest_path, validation_errors}`.

---

## Validación

### Pre-upload (en el script)

El script aborta antes de subir si:

| Check | Falla si |
|---|---|
| Schema | `schema_version != "1.2"` |
| `what_was_done` | vacío o < 20 chars |
| `deliverables_actual` | array vacío o algún elemento sin `what` |
| `report_file_path` | archivo no existe en disco |
| `vtt_report_comment_id` | null en v1.0 |
| `vtt_attachments.devlog_id` | null en v1.0 |
| `review_gate.canProceedToReview` | false |
| `git.pr_url` | null sin `git.note` explicativo |
| `indexes.deliverables_paths` | no espeja `deliverables_actual[].path` |
| `review.tl_review` (en v1.0) | poblado por error |
| DevOps task | `delivery.operations` falta |
| `review.tl_review.verdict` (en v1.5) | null o vacío |
| `verifications.*` (en v1.5) | alguno `false` |

### Post-upload

```bash
# Manifest subido como fileType=manifest
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/attachments" -H "Authorization: Bearer $TOKEN" | \
  jq '[.data[] | select(.fileType=="manifest")] | length'
# v1.0: esperado >= 1; v1.5: esperado >= 2

# Para v1.5: el último uploaded por TL
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/attachments" -H "Authorization: Bearer $TOKEN" | \
  jq '[.data[] | select(.fileType=="manifest" and .uploadedBy=="'$TL_UUID'")] | length >= 1'
```

---

## Error común

| Error | Causa probable | Solución |
|---|---|---|
| `HTTP 400 fileType invalid` | Subiendo JSON puro | Wrappear en `.md` antes de upload |
| `HTTP 401 Unauthorized` | TOKEN expirado | Renovar con `SKL-AUTH-01` |
| `HTTP 413 Payload too large` | Manifest > 5MB | Revisar — manifest no debe exceder 200KB; si pasa, hay texto largo embebido |
| `Validation error: what_was_done empty` | Parser no encontró sección en el reporte | Verificar formato del reporte — headings correctos |
| `Validation error: deliverables_actual[0].what missing` | Bullet del reporte sin descripción | Cada archivo en sección `Código:` debe tener `path - descripción` |
| `Validation error: devlog mismatch` | `devlog_entries.length != devlog_summary.total` | Sincronizar antes de subir |
| `IndexError parsing report` | Reporte mal formado | Pedir al agente regenerar reporte |

---

## Scripts invocados

- `VTT.SCRIPT-MAN-001_gen_task_manifest.py` — único script (atómico, ~300 líneas) que ejecuta TODAS las acciones según `--version` y flags

> Sin Scripts adicionales — la Skill delega TODA la lógica al script. La Skill solo describe contratos.

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-17 | Versión inicial. Skill normativa que reemplaza al borrador legacy `SKL-MANIFEST-01_generar-manifest.md` (`_pending-migration/manifest/`). Consolida v1.0 (agente) y v1.5 (TL) en una sola Skill con dispatch por `--version`. Schema fijo en v1.2. |
| 1.1 | 2026-05-18 | Script `VTT.SCRIPT-MAN-001` bumpeado a v1.1 con 7 fixes detectados en producción (caso VTT-721): parser de paths con guiones, normalización de `category` objeto→string, re-indexación en v1.5, fallback shape para `task.sprint/stage/category`, campo comment `body→message`, `uploadedById` en multipart, endpoint individual attachment correcto (`/api/attachments/<id>/file`). Contrato de Skill sin cambios. |
| 1.2 | 2026-05-18 | Script bumpeado a v1.2 (un solo par de archivos local sin sufijo `.v1.5`) + v1.3 (Bug #8 detectado en validación VTT-718): `build_v15()` ahora consolida en `delivery.trackable_items_actual.related_to` todos los TIs del modelo dinámico — tanto `new_tis_created` (TIs nuevos del TL) como `evidences_added` (TIs evidenciados, ya existentes). Antes solo agregaba los nuevos, dejando `tech_debt_count=0` y `related_to_codes=[]` cuando el TL solo evidenciaba TIs existentes. Caso real: VTT-718 con 21 TIs evidenciados. Contrato de Skill sin cambios. |

> **Política de versionado:**
> - v1, v2, v3... — bumpear por cambio de contrato (inputs/outputs) o de comportamiento mayor
> - Mejoras internas sin cambio de contrato → misma versión, actualizar fecha
