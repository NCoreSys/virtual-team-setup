# Guía — Task Manifest para agentes ejecutores

**Versión:** 4.0
**Fecha:** 2026-05-17
**Aplicable a:** BE, DB, FE, QA, DO, DL, UX, AR, SA (cualquier agente ejecutor)
**Complemento de:** `SKL-MANIFEST-01` (skill del TL Reviewer) y `SKL-REPORT-01` (skill del agente)
**Schema del manifest:** v1.2

**Changelog v3.1 → v4.0:**
- Guía reescrita como **documentación descriptiva** (qué, por qué, cuándo, reglas). El código de implementación vive en SKL-MANIFEST-01.
- Schema bump 1.1 → 1.2: ELIMINADO `delivery.skl_report_01_full` (contaminaba el JSON). REEMPLAZADO por campos separados, uno por sección del SKL-REPORT-01.
- Nueva sección: §Mapeo SKL-REPORT-01 → Manifest (qué sección del report alimenta qué campo del manifest).
- Nueva sección: §Por qué campos separados (motivación + IMPROVE-002).
- Eliminado snippet Python completo (movido a SKL-MANIFEST-01).
- Eliminado schema JSON completo (vive en SKL-MANIFEST-01 §Esquema v1.0).

---

## 1. ¿Qué es el manifest?

Un archivo JSON estructurado que captura **todo el ciclo de vida de una tarea** en un solo documento auditable: BRIEF, ASSIGNMENT, entrega del agente, decisiones, evidencias, review del TL.

**No es** un contenedor de texto narrativo largo. **Es un índice queryable** donde cada campo permite responder una pregunta operativa: ¿qué se hizo? ¿qué archivos se tocaron? ¿qué CAs pasaron? ¿qué deuda quedó pendiente? ¿quién aprobó?

**Vive en:**
- `knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>.json` (fuente local)
- Wrapper `.md` adjunto al mismo path (para subir a VTT — el backend no acepta JSON puro)
- VTT como attachment `fileType=manifest`

---

## 2. ¿Por qué campos separados (no un único `skl_report_01_full`)?

**Antes** (schema v1.0/v1.1, ahora deprecado): el manifest incluía un campo `skl_report_01_full` con el report completo embebido como texto. Resultado: cada manifest ~12K chars de texto duplicado, JSON contaminado, queries imposibles.

**Ahora** (schema v1.2): cada sección del SKL-REPORT-01 se mapea a un campo estructurado independiente. Resultado:

- Un agente futuro puede pedir los últimos 50 manifests y recibir ~12K **tokens útiles** (estructura navegable), no 600K de texto plano.
- Queries posibles: "todas las tareas que tocaron `foo.service.ts`", "todos los findings con severidad high en S6", "todas las tareas con tech_debt pendiente para R2".
- IMPROVE-002 (BD de manifests) puede indexar campos individuales en lugar de hacer `LIKE '%texto%'` sobre un blob.
- El reporte completo sigue existiendo como **archivo en disco** (`knowledge/agent-tasks/reports/...`) para lectura humana exhaustiva.

---

## 3. Quién hace qué con el manifest

| Versión INSTANCE | Quién | Cuándo | Contenido |
|---|---|---|---|
| **v1.0** | **Agente ejecutor (TÚ)** | Paso 15 de tu workflow — AL FINAL, después de attachments + status `task_in_review` + PRs + reporte SKL-REPORT-01 | Bloques `task`, `brief`, `assignment`, `agent_message`, `delivery` poblados con TU trabajo real. `review.tl_review = null`. |
| **v1.5** | TL Reviewer | Paso 14 del cierre | Lee tu v1.0 → agrega `delivery.dynamic_model_actions` + `review.tl_review` → sube como NUEVO attachment (no reemplaza) |
| v2.0 (futuro) | PM | Aprobación final | Agrega `review.pm_approval` |

**Tu rol como agente:** generar la v1.0 con `current_status: task_in_review` y subir como attachment `fileType=manifest`.

**No es opcional.** Es el entregable #7.5 obligatorio del ASSIGNMENT.

---

## 4. Regla crítica de orden — manifest AL FINAL

> Generar el manifest **DESPUÉS** de estos pasos. Si lo generas antes, quedan campos `null` en `delivery`.

```
Paso 14 del workflow del agente:
  [x] Reporte SKL-REPORT-01 guardado en archivo knowledge/agent-tasks/reports/<phase>/<sprint>/<TASK_ID>_REPORT.md
  [x] Extracto del reporte posteado como comment en VTT (8-10 líneas + link al archivo)
  [x] Devlog subido como attachment fileType=devlog
  [x] Code Logic subido (real o placeholder N/A) como attachment fileType=code_logic
  [x] Status moveado a task_in_review
  [x] PR(s) creado(s) con URL específica
  [x] Review Gate canProceedToReview=true

Paso 15:
  → Recolectar IDs reales de todo lo anterior desde VTT API
  → Extraer campos narrativos del reporte local
  → Construir <TASK_ID>.json con todos los bloques completos
  → Validar (ver §8)
  → Subir como attachment fileType=manifest
```

**Lección PROC-MANIFEST-01:** la primera versión de MS-284 tuvo 10+ campos null porque se generó prematuramente.

---

## 5. Mapeo SKL-REPORT-01 → Manifest (v1.2)

Cada sección del reporte que generas con SKL-REPORT-01 alimenta uno o más campos del manifest. Esta tabla es la fuente de verdad para que el JSON refleje el reporte sin duplicar texto en un solo blob.

| Sección del reporte (archivo local) | Campo(s) del manifest | Notas |
|---|---|---|
| `Lo que se hizo:` | `delivery.what_was_done` | Texto corto (~80 palabras max). Es el campo más consultado por agentes futuros. |
| `Código:` (lista de archivos con descripción) | `delivery.deliverables_actual[]` con `{path, state, what}` | `state` = created\|modified. `what` = descripción corta de qué se hizo en ese archivo (extraída del bullet). |
| `Development Log:` (path) | `delivery.development_log_path` | Solo el path; el archivo se lee on-demand. |
| `Code Logic:` (paths) | `delivery.code_logic_files[]` | Solo paths. |
| `Criterios de aceptación:` (tabla) | `delivery.criteria_results[]` + `delivery.criteria_summary` | Cada CA con su `id` (UUID de VTT), `title`, `status`, `criteriaTypeCode`. |
| `Devlog entries registrados en VTT:` (tabla) | `delivery.devlog_entries[]` + `delivery.devlog_summary` | Estructurado: `{category, severity, title, status}`. NO solo el summary. |
| `Findings / Deuda técnica:` | `delivery.findings` | Texto narrativo o `"N/A"`. |
| `ADRs tomados:` | `delivery.adrs_taken` | Texto narrativo o `"N/A"`. |
| `TrackableItems creados o vinculados:` | `delivery.trackable_items_actual.{implements, related_to}` | Cada TI con `{code, uuid}`. Espejar códigos en `indexes.implements_codes` y `indexes.related_to_codes`. |
| `Items detectados para trackeo (TL revisar):` | `delivery.items_detected_for_tl_review[]` | Cada item con `{type_suggested, code_suggested, description, urgency, retroactive}`. |
| `Tareas derivadas generadas:` | `delivery.derived_tasks` | Texto narrativo o `"N/A"`. |
| `Cómo verificar:` (lista de comandos) | `delivery.how_to_verify[]` | Array de strings. |
| `Notas:` | `delivery.notes` | Texto narrativo o `"N/A"`. |
| `Review gate al entregar:` | `delivery.review_gate` | Objeto `{canProceedToReview, entries_total, resolved, warnings}`. |
| `Commit:` | `delivery.git.commit_sha` + `delivery.git.commit_message` | SHA del commit + mensaje literal. |
| `PR:` | `delivery.git.pr_url` + `delivery.git.pr_number` | URL + número. |

**Adicionalmente** (no vienen del reporte sino de operaciones del workflow):

| Origen | Campo del manifest |
|---|---|
| Path del reporte local (puntero, no contenido) | `delivery.report_file_path` |
| ID del comment extracto en VTT | `delivery.vtt_report_comment_id` |
| IDs de attachments (brief, assignment, devlog, code_logic) | `delivery.vtt_attachments.*` |
| Resultado de SKL-HARDCODE-CHECK | `delivery.hardcode_check` |
| Resultado de tests (Jest/Vitest) | `delivery.tests` |
| Paths de archivos tocados (espejo de `deliverables_actual.path`) | `indexes.deliverables_paths` |

---

## 6. Reglas de validación

### Campos obligatorios (siempre)

- `schema_version` debe ser `"1.2"` para nuevos manifests
- `delivery.what_was_done` no puede estar vacío ni ser placeholder
- `delivery.deliverables_actual[]` debe tener al menos 1 entrada, y cada una debe tener `path`, `state` y `what`
- `delivery.devlog_entries[].length` debe coincidir con `delivery.devlog_summary.total`
- `indexes.deliverables_paths` debe espejar todos los `delivery.deliverables_actual[].path`

### Campos `null` con `note` (intencional)

Algunos bloques pueden ser `null` por convención cuando no aplican. En esos casos, agregar un campo `note` explicando POR QUÉ es null:

- `brief` y `assignment` pueden ser `null` en tareas DevOps/operación (no requieren brief)
- `delivery.git` puede ser `null` en tareas sin código (DevOps en producción)
- `delivery.tests` puede tener `framework: "N/A"` en tareas sin tests

### Tareas DevOps — bloque `delivery.operations` obligatorio

Si `task.category` ∈ `[deployment, devops, operation, sql_migration, rollback, smoke_test, config_change, restart_service]`, entonces `delivery.operations` es **obligatorio** (ver SKL-MANIFEST-01 §Bloque `delivery.operations`).

### Aborts del script

El script de generación debe abortar (no subir el manifest) si:

1. No existe el reporte local (`report_file_path`)
2. `what_was_done` queda vacío
3. Tarea DevOps sin `delivery.operations`
4. `brief`/`assignment`/`git` son `null` sin `note`

---

## 7. ¿Qué NO debe ir en el manifest?

- **El reporte completo embebido como texto** (eso es lo que `skl_report_01_full` hacía mal). Solo el path al archivo en `delivery.report_file_path`.
- **El contenido del development log** — solo el path en `delivery.development_log_path`.
- **El contenido de code logic** — solo los paths en `delivery.code_logic_files[]`.
- **El contenido del devlog** — solo entries estructurados con `{category, severity, title, status}` (sin la descripción larga).
- **El contenido del brief o assignment** — solo IDs de attachment + path.
- **Logs de ejecución, traces, outputs largos** — guardarlos como attachments separados con `fileType=log` si son relevantes.

Regla: **paths y IDs sí; contenidos largos no.** El manifest indexa, no almacena.

---

## 8. Checklist antes de subir

```
[ ] schema_version = "1.2"
[ ] task.id, task.title, task.sprint, task.current_status="task_in_review" presentes
[ ] brief y assignment tienen vtt_attachment_id (o note si es DevOps)
[ ] delivery.what_was_done es texto real (>20 caracteres)
[ ] delivery.deliverables_actual[] tiene al menos 1 entrada con {path, state, what}
[ ] delivery.report_file_path apunta al archivo del reporte local que existe en disco
[ ] delivery.vtt_report_comment_id tiene el ID del comment-extracto en VTT
[ ] delivery.vtt_attachments.devlog_id presente (devlog ya subido)
[ ] delivery.criteria_results[] coincide con CAs en VTT
[ ] delivery.devlog_entries[] estructurado (no solo summary)
[ ] delivery.review_gate.canProceedToReview = true
[ ] delivery.git tiene pr_url, pr_number, commit_sha, commit_message
[ ] indexes.deliverables_paths espeja delivery.deliverables_actual[].path
[ ] review.tl_review = null (es del TL, no lo toques)
[ ] Si task.category = deployment → delivery.operations completo
[ ] Si algún campo es null intencional → agregar note explicando
```

Para los comandos `jq` específicos de validación, ver SKL-MANIFEST-01 §Validación v1.0.

---

## 9. Ubicación de archivos

| Archivo | Ruta |
|---|---|
| Manifest JSON (fuente local) | `knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>.json` |
| Wrapper MD (para subir a VTT) | `knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>.manifest.md` |
| Reporte fuente del agente | `knowledge/agent-tasks/reports/<phase>/<sprint>/<TASK_ID>_REPORT.md` |
| Brief | `knowledge/agent-tasks/briefs/<phase>/<sprint>/BRIEF_<TASK_ID>_<slug>.md` |
| Assignment | `knowledge/agent-tasks/assignments/<phase>/<sprint>/ASSIGNMENT_<TASK_ID>_<slug>.md` |
| Development log | `knowledge/development-log/<YYYY-MM-DD>_<TASK_ID>_<slug>.md` |
| Code logic | `knowledge/code-logic/<modulo>/<TASK_ID>_<slug>.LOGIC.md` |

`<phase>` ejemplos: `04-development`, `05-testing`, `06-deploy`.
`<sprint>` ejemplos: `S01`, `S06-FIX-A`.

---

## 10. Documentos relacionados

- `SKL-MANIFEST-01_generar-manifest.md` — Skill con el esquema JSON completo, snippets de implementación y validaciones
- `SKL-REPORT-01_entrega-tarea.md` — Skill del reporte de entrega del agente (fuente de los campos narrativos)
- `SKL-DYNAMIC-MODEL-01_cierre-modelo-dinamico.md` — Skill que el TL ejecuta antes de la v1.5
- `GUIA_REVISION_TAREA_TL_REVIEWER.md` — Guía completa del TL Reviewer
- `PROCESO_CIERRE_TAREA_v2.md` — Workflow de cierre donde encaja el manifest
- `IMPROVE-002_bd_manifiestos_y_tis.md` — BD queryable que consume los campos separados del manifest
