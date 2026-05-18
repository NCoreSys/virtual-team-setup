# Proceso de Asignación + Cierre de Tareas — Tech Lead · Memory Service v3

**Versión:** 3.1
**Fecha:** 2026-05-14
**Reemplaza:** `PROCESO_ASIGNACION_TAREAS.md` v2.0
**Cambios v2 → v3:** 16 pasos del ciclo completo (vs 13 antes), modelo dinámico al cerrar, automatización del mensaje al agente con `scripts/gen_mensaje.py`, manifest al final del workflow, gotchas reales de VTT documentados.

---

## Documentos Base (LEER SIEMPRE)

| # | Documento | Propósito |
|---|-----------|-----------|
| 1 | `.claude/agents/OPERATIVO_TL_MEMORY-SERVICE.md` | Operativo del TL Ejecutor |
| 2 | `.claude/agents/OPERATIVO_TL_REVIEWER.md` v3.2 | Operativo del TL Reviewer |
| 3 | `00-platform/05.Templates/05.Proyecto/02.Genericos/TEMPLATE_ASIGNACION_TAREARev.md` | Template assignments (v3) |
| 4 | `00-platform/06.Documentos_soporte/PROCESO_CIERRE_TAREA_v2.md` | Workflow cierre con modelo dinámico |
| 5 | `00-platform/06.Skills/CATALOGO_SKILLS_MEMORY_SERVICE.md` v1.3 | Catálogo de skills (34 skills) |
| 6 | `Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` | Fuente de verdad funcional |
| 7 | `.claude/rules/MAPA_DEPENDENCIAS_ENTREGABLES.md` | Inputs obligatorios por tarea |
| 8 | `knowledge/platform-feedback/VTT_PLATFORM_GAPS_2026-05-13.md` | Gaps conocidos del backend VTT |

---

## Datos del Proyecto

| Campo | Valor |
|---|---|
| VTT_BASE_URL | `http://77.42.88.106:3000` |
| PROJECT_ID | `d0fc276d-e764-4a83-96e9-d65f086ed803` |
| PROJECT_KEY | `MS` |
| SERVICE_KEY | env `$MEM_VTT_SERVICE_KEY` |
| Tech Lead UUID | `92225290-6b6b-4c1f-a940-dcb4262507aa` |

## Equipo

| Rol | UUID | Email |
|---|---|---|
| PM | `350831b2-e1ae-4dbe-b2eb-7e023ec2e103` | `pm@memory-service.vtt.ai` |
| Tech Lead | `92225290-6b6b-4c1f-a940-dcb4262507aa` | `memory-service.tl@vtt.ai` |
| PJM | `0ff63a29-0bc0-465a-b9bd-5f71476bc91d` | `pjm@memory-service.vtt.ai` |
| Backend | `ebbe3cee-abed-4b3b-860d-0a81f632b08a` | `memory-service.be@vtt.ai` |
| DB | `6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7` | `memory-service.db@vtt.ai` |
| Frontend | `d23c9cd9-a156-433b-8900-94add5488eec` | `memory-service.fe@vtt.ai` |
| QA | `613c9538-658c-45fe-a6d7-c1ea9ff04b78` | `memory-service.qa@vtt.ai` |
| DevOps | `322e3745-9756-4a7c-af11-44b33edef44d` | `memory-service.devops@vtt.ai` |
| Design Lead | `b3a09269-cded-468c-a475-15a48f203cb0` | `memory-service.dl@vtt.ai` |
| UX | `a75a1dae-754a-4b6f-a3ff-db8d51f6a91b` | `memory-service.ux@vtt.ai` |
| AR | `e9403c25-c1f8-4b64-b2ef-f447d53115e2` | `ar@memory-service.vtt.ai` |
| SA | `0c128e3b-db3b-4e31-b107-0379b5791233` | `sa@memory-service.vtt.ai` |

---

## Las Tres Fases del Ciclo

```
FASE 1 — Planificación (TL Ejecutor)
   Pasos 1-3: crear tarea, brief, dependencias

FASE 2 — Asignación (TL Ejecutor)
   Pasos 4-7: análisis de dependencias, assignment, CAs/TIs, mensaje al agente

FASE 3 — Cierre (TL Reviewer)
   Pasos 8-16: verificación + modelo dinámico + APR-TL + manifest
```

---

## CICLO COMPLETO — 16 PASOS

### FASE 1 — Planificación

#### Paso 1 — Leer Handoff del PM y SPEC

- Leer SPEC v1.9 para contexto funcional
- Leer MAPA_DEPENDENCIAS_ENTREGABLES para identificar inputs obligatorios
- Analizar dependencias y definir oleadas del sprint

#### Paso 2 — Crear Tarea en VTT

```bash
TOKEN=$(curl -s -X POST $BASE/api/auth/service-token \
  -H "Content-Type: application/json" \
  -d "{\"userId\":\"92225290-...\",\"serviceKey\":\"$MEM_VTT_SERVICE_KEY\"}" \
  | jq -r '.data.token')

curl -s -X POST "$BASE/api/phases/{phaseId}/tasks" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{
    "title": "...",
    "description": "max 2000 chars",
    "priorityId": "<uuid>",
    "statusId": "335fd9c6-f0d6-4966-a6ea-f518c78bc422",
    "assignedToId": "<uuid_agente>",      # NO assigneeId — silently ignored
    "assignedBy": "92225290-...",
    "category": "development",
    "complexity": "MEDIUM",
    "createdBy": "92225290-..."
  }'
```

**Gotcha:** `assignedToId` correcto. `assigneeId` es ignorado silenciosamente.

#### Paso 3 — Crear y Subir BRIEF

Ubicación local: `knowledge/agent-tasks/briefs/[fase]/[sprint]/BRIEF_MS-XXX_<nombre>.md`

```bash
curl -s -X POST "$BASE/api/tasks/MS-XXX/attachments" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@knowledge/agent-tasks/briefs/04-development/S01/BRIEF_MS-XXX_nombre.md" \
  -F "fileType=brief" \
  -F "uploadedById=92225290-..."
```

---

### FASE 2 — Asignación

#### Paso 4 — Análisis de Dependencias de Datos

**Regla absoluta:** No generar ASSIGNMENT sin completar primero el Análisis de Dependencias.

Ver `PROCESO_ANALISIS_DEPENDENCIAS_ASSIGNMENT.md`:

```
[ ] Identifiqué qué documentos fuente necesita el agente
[ ] Tracé cada dependencia a su ruta exacta
[ ] Verifiqué que los documentos existen y están aprobados
[ ] El ASSIGNMENT referenciará rutas exactas en "DOCUMENTOS DE REFERENCIA OBLIGATORIOS"
```

**Lección MS-029..035:** Un assignment sin trazado de dependencias = el agente trabaja en el vacío (perdió ~1M tokens en regeneración).

#### Paso 5 — Generar ASSIGNMENT

Ubicación local: `knowledge/agent-tasks/assignments/[fase]/[sprint]/ASSIGNMENT_MS-XXX_<nombre>.md`

Usar `TEMPLATE_ASIGNACION_TAREARev.md` v3. Secciones obligatorias:
- §1 Objetivo + alcance
- §2 DOCUMENTOS DE REFERENCIA OBLIGATORIOS (rutas exactas)
- §3 Acceptance Criteria (a crear en VTT en Paso 6)
- §4 TrackableItems a vincular (implements / related_to)
- §5 Living Documents impactados (declarar incluso si "sin cambios")
- §6 Workflow del agente (15 pasos del agente)
- §7 Hardcode Check (criterios y comandos)
- §8 Tech debts e items detectados — **sección obligatoria** para que el agente la rellene en SKL-REPORT-01

**Subir ASSIGNMENT:**
```bash
curl -s -X POST "$BASE/api/tasks/MS-XXX/attachments" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@knowledge/agent-tasks/assignments/.../ASSIGNMENT_MS-XXX_nombre.md" \
  -F "fileType=assignment" \
  -F "uploadedById=92225290-..."
```

#### Paso 6 — Crear Acceptance Criteria en VTT

```bash
curl -s -X POST "$BASE/api/tasks/MS-XXX/criteria" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{
    "title": "CA-01: ...",
    "description": "...",
    "criteriaTypeCode": "acceptance",    # NO type
    "required": true
  }'
```

**Gotcha:** campo es `criteriaTypeCode`, NO `type`. Endpoint es `/criteria`, NO `/acceptance-criteria`.

#### Paso 7 — Vincular TrackableItems + Generar Mensaje al Agente

**Vincular TIs:**
```bash
curl -s -X POST "$BASE/api/trackable-items/<TI_UUID>/tasks" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"taskId":"MS-XXX","linkType":"implements"}'   # o "related_to"
```

#### Paso 7b — Crear execution_manifest de la tarea (NUEVO v3.1)

> Aplica desde adopción de worktrees por rol (`GUIA_WORKTREES_MEMORY_SERVICE.md`).
> Declara qué agente, qué worktree, qué archivos puede tocar. El agente lo lee al arrancar.

```bash
# Copiar template y editar
cp .vtt/manifests/_template.execution.json .vtt/manifests/MS-XXX.execution.json

# Editar:
#  - taskId, title
#  - agents[].agentUuid del rol
#  - agents[].branch = feature/MS-XXX
#  - agents[].assignedWorkdir = .vtt/worktrees/<repo>-<rol-lower>
#  - agents[].allowedPaths (del BRIEF §3 Inputs y §4 Deliverables)
#  - agents[].deniedPaths (.env*, .vtt/**, node_modules/**)
#  - agents[].expectedOutputs (paths de reports/diffs)

# Validar JSON
python -m json.tool .vtt/manifests/MS-XXX.execution.json
```

Ver detalle: `GUIA_ASIGNACION_TAREA_TL_EJECUTOR.md` Paso 8.5.

#### Paso 8 — Generar Mensaje al Agente (SKL-MESSAGE-01)

```bash
python scripts/gen_mensaje.py MS-XXX --post
```

El script:
- Publica el mensaje como comment en VTT
- Inyecta cwd del worktree según rol del agente
- Inyecta path del `.code-workspace` para que el usuario abra la ventana
- Comandos de arranque (JWT + branch creation + status)
- Referencia al execution_manifest creado en Paso 7b

También guarda en `knowledge/agent-tasks/messages/04-development/S01/MENSAJE_MS-XXX.md`.

---

### FASE 3 — Cierre (TL Reviewer)

> **Documento detallado:** `PROCESO_CIERRE_TAREA_v2.md`
> A continuación, el resumen integrado en este proceso.

#### Paso 8 — Verificar Review Gate

```bash
curl -s "$BASE/api/tasks/MS-XXX/review-gate" -H "Authorization: Bearer $TOKEN"
```

Esperado: `canProceedToReview: true`, `blockers: []`.

#### Paso 9 — Verificar Acceptance Criteria

```bash
curl -s "$BASE/api/tasks/MS-XXX/criteria" -H "Authorization: Bearer $TOKEN" | \
  jq '.data | map(select(.status != "met"))'
```

Esperado: array vacío (todas met).

#### Paso 10 — Verificar Attachments

```bash
curl -s "$BASE/api/tasks/MS-XXX/attachments" -H "Authorization: Bearer $TOKEN" | \
  jq '.data | group_by(.fileType) | map({type: .[0].fileType, count: length})'
```

Esperado: brief, assignment, devlog, code_logic (o placeholder), manifest.

#### Paso 11 — Verificar PRs en GitHub

```bash
gh pr view <N> --repo NCoreSys/memory-service-backend --json state,mergeable,url
gh pr view <N> --repo NCoreSys/memory-service-project --json state,mergeable,url
```

Esperado: state=OPEN, mergeable=MERGEABLE.

#### Paso 12 — **APLICAR SKL-DYNAMIC-MODEL-01** (NUEVO en v3)

> **Skill operativa:** `00-platform/06.Skills/dynamic-model/SKL-DYNAMIC-MODEL-01_cierre-modelo-dinamico.md`

##### 12.1 — Crear TIs detectados por el agente

Del reporte SKL-REPORT-01 sección "Tech debts detectados" y "Items detectados para trackeo":

```bash
curl -s -X POST "$BASE/api/projects/$PROJECT_ID/trackable-items" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{
    "code": "DEBT-XXX-NN",
    "title": "[DEFER R2] <titulo>",
    "description": "[Deferred to R2] <descripcion>",
    "typeCode": "tech_debt",            # software acepta solo tech_debt para improvements
    "statusCode": "ti_draft",
    "createdById": "92225290-..."
  }'

# Vincular a la tarea
curl -s -X POST "$BASE/api/trackable-items/<TI_ID>/tasks" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"taskId":"MS-XXX","linkType":"related_to"}'
```

**Constraints:**
- `process_improvement` NO válido → `tech_debt` + `[PROCESS]` marker
- Status `ti_deferred` NO existe → marker `[DEFER R2]` textual
- Endpoint `/defer` NO existe → no llamar

##### 12.2 — Agregar evidencias a TIs vinculadas (heredadas + nuevas)

Por cada TI vinculada × cada PR:

```bash
curl -s -X POST "$BASE/api/trackable-items/<TI_ID>/evidence" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{
    "type": "link",                        # enum: document|link|test_result|screenshot
    "title": "[MS-XXX] [S1] <descripcion corta>",
    "url": "https://github.com/.../pull/N",
    "description": "[TASK:MS-XXX] [SPRINT:S1] <descripcion completa>",
    "createdById": "92225290-..."
  }'
```

**Gotchas:**
- Endpoint singular `/evidence` (NO `/evidences`)
- Enum `type`: no acepta `pr` (usar `link`)
- DELETE no existe → cuidar formato

**Formato OBLIGATORIO de marker:**
- title: `[MS-XXX] [SX] ...`
- description: `[TASK:MS-XXX] [SPRINT:SX] ...`
- url: PR específico

##### 12.3 — Resolver devlog entries

```bash
# Listar entries pendientes
curl -s "$BASE/api/tasks/MS-XXX/devlog" -H "Authorization: Bearer $TOKEN" | \
  jq '.data[] | select(.status != "resolved") | {id, title}'

# Resolver cada uno
curl -s -X PATCH "$BASE/api/tasks/MS-XXX/devlog/<ENTRY_ID>/status" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{
    "status": "resolved",
    "resolution": "Revisado por TL durante cierre MS-XXX. ..."
  }'
```

**Gotcha:** `resolution` es REQUERIDO cuando status=`resolved` o `wont_fix`. Sin él → 400.

#### Paso 13 — APR-TL Comment

```bash
curl -s -X POST "$BASE/api/tasks/MS-XXX/comments" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{
    "message": "## APR-TL: MS-XXX aprobado...\n[...con sección Acciones aplicadas al cerrar (modelo dinámico)]",
    "userId": "92225290-..."
  }'
```

Máximo 5000 chars. Si excede, dividir en 2 comments o subir como attachment.

#### Paso 14 — Status → task_completed

```bash
curl -s -X PATCH "$BASE/api/tasks/MS-XXX/status" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{
    "statusId": "aa5ceb90-5209-42a2-b874-a8cbee597a97",
    "changedBy": "92225290-...",
    "reason": "APR-TL: aprobado tras code review + modelo dinamico aplicado"
  }'
```

#### Paso 15 — **Aplicar SKL-MANIFEST-01** (AL FINAL — crítico)

> **Skill operativa:** `00-platform/06.Skills/manifest/SKL-MANIFEST-01_generar-manifest.md`
>
> **Regla crítica:** El manifest se genera **DESPUÉS** de attachments + status + dynamic model. Si se genera antes, quedan campos null en `delivery` (lección PROC-MANIFEST-01).

Generar/actualizar `knowledge/task-manifests/[fase]/[sprint]/MS-XXX.json` con:

```json
{
  "task": { ... },
  "brief": { ... },
  "assignment": { ... },
  "agent_message": { ... },
  "delivery": {
    "skl_report_01_full": "<reporte literal del agente>",
    "deliverables_actual": [...],
    "vtt_attachments": { ... },
    "criteria_results": [...],
    "criteria_summary": { ... },
    "devlog_summary": { ... },
    "hardcode_check": { ... },
    "trackable_items_actual": { ... },
    "living_documents_declared_no_change": [...],
    "tech_debt_for_r2": [...],
    "dynamic_model_actions": {
      "new_tis_created": [...],
      "evidences_added": [...],
      "devlog_resolved_count": N,
      "note_defer_endpoint_missing": "...",
      "note_typecode_constraint": "..."
    },
    "how_to_verify": [...],
    "git": { ... }
  },
  "review": {
    "tl_review": {
      "verdict": "approved",
      "verifications": { "dynamic_model_applied": true, ... },
      ...
    }
  },
  "indexes": { ... }
}
```

Subir como attachment `fileType=manifest`.

#### Paso 16 — Validación Final + Notificación PM

```bash
# Validar todo
curl -s "$BASE/api/tasks/MS-XXX" -H "Authorization: Bearer $TOKEN" | jq '.data.status.code'
# task_completed

curl -s "$BASE/api/tasks/MS-XXX/devlog" -H "Authorization: Bearer $TOKEN" | \
  jq '.data | map(select(.status != "resolved")) | length'
# 0

# Notificar PM (comment o canal externo)
```

PM hace aprobación terminal: `status → task_approved`.

---

## Gotchas de VTT (consolidados — actualizado 2026-05-13)

| # | Concepto | Detalle |
|---|---|---|
| 1 | `assignedToId` no `assigneeId` | Backend ignora silenciosamente assigneeId |
| 2 | `criteriaTypeCode` no `type` | Para CAs; endpoint `/criteria` no `/acceptance-criteria` |
| 3 | `PUT /deliveries` no PATCH | El template decía PATCH (era incorrecto) |
| 4 | JSON requiere wrapper `.md` | Backend whitelist no incluye `application/json` |
| 5 | Comments ≤ 5000 chars | Dividir o adjuntar archivo |
| 6 | Severity en devlog es enum no nullable | Usar `"low"` mínimo |
| 7 | GET `/devlog` (singular), POST `/devlog-entries` (plural) | Verbos opuestos |
| 8 | Review Gate exige code_logic | Incluso documentation/deployment → placeholder N/A |
| 9 | `/document-impacts` inaccesible al DO | Workaround: devlog observation |
| 10 | TI create scoped a project | `POST /api/projects/:id/trackable-items` |
| 11 | Evidence endpoint singular `/evidence` | NO `/evidences` |
| 12 | Evidence enum type | `document\|link\|test_result\|screenshot` (NO `pr`) |
| 13 | Devlog resolve necesita `resolution` | Cuando status=resolved/wont_fix |
| 14 | `/defer` NO existe | Marker `[DEFER R2]` textual |
| 15 | `process_improvement` NO válido software | Usar `tech_debt` + `[PROCESS]` marker |
| 16 | DELETE evidence NO existe | Cuidar formato al crear |
| 17 | `GET /tasks/:id/trackable-items` NO existe | Iterar TIs del proyecto |
| 18 | Manifest al final | Generar AFTER attachments + status + dynamic_model |

---

## UUIDs de Status

| Status | UUID |
|---|---|
| task_created | `0e54089b-296a-4d80-bcd3-80a7a71f1696` |
| task_pending | `335fd9c6-f0d6-4966-a6ea-f518c78bc422` |
| task_in_progress | `2a76888a-e595-4cfc-ac4c-a3ae5087ef56` |
| task_in_review | `1ec975a5-7581-4a1a-ab8f-51b1a7ef868d` |
| task_completed | `aa5ceb90-5209-42a2-b874-a8cbee597a97` |
| task_approved | `b9ca4951-6e14-4d82-b1d8-440793bbaf47` |
| task_on_hold | `c62eb334-b7bc-4c9f-af85-a5666c262aaa` |

---

## Reglas Críticas

1. **UNA tarea a la vez** — regla LL-001
2. **BRIEF = adjunto al crear. ASSIGNMENT = adjunto al asignar.**
3. **Review gate limpio antes de in_review** — obligatorio
4. **CAs con fulfill en VTT** — no solo en reporte
5. **Comentarios: `message` + `userId`** — NUNCA `content` + `authorId`
6. **Attachments: `uploadedById` obligatorio** — sin él 400
7. **Modelo dinámico al cerrar (Paso 12)** — TIs + evidencias + devlog resolve, no opcional
8. **Manifest al FINAL (Paso 15)** — después de attachments + status
9. **SPEC v1.9** fuente de verdad funcional — cambios requieren ADR

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 2.0 | 2026-05-01 | Customización Memory Service. Modelo Dinámico V4: review-gate, devlog, CAs fulfill, TrackableItems |
| 3.0 | 2026-05-13 | Ciclo completo 16 pasos: FASE 1 + FASE 2 + FASE 3 (cierre). Modelo dinámico al cerrar (Paso 12, SKL-DYNAMIC-MODEL-01). Mensaje automatizado con `scripts/gen_mensaje.py`. Manifest al FINAL (Paso 15, SKL-MANIFEST-01). 18 gotchas de VTT documentados. Lecciones MS-283/284/285. |
| **3.1** | **2026-05-14** | **Paso 7b NUEVO: crear execution_manifest. Worktrees por rol (cierra PROC-COORD-01). Renumeración: Paso 8 (mensaje) era 8, ahora consolida 7→8. Referencias a `GUIA_WORKTREES_MEMORY_SERVICE.md`.** |
