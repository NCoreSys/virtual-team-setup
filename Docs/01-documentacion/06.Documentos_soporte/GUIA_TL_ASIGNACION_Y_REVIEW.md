# GUÍA TL — Asignación de Tareas y Review Completo

**Versión:** 1.0  
**Fecha:** 2026-05-20  
**Proyecto:** Memory Service  
**Rol:** Tech Lead (TL Reviewer + TL Ejecutor)

---

## DATOS DEL PROYECTO

| Campo | Valor |
|---|---|
| PROJECT_ID | `d0fc276d-e764-4a83-96e9-d65f086ed803` |
| PROJECT_KEY | `MS` |
| API_BASE | `http://77.42.88.106:3000` |
| SERVICE_KEY | `hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d` |
| TL UUID | `92225290-6b6b-4c1f-a940-dcb4262507aa` |
| Phase Development ID | `c5f9f305-de20-4d09-b939-39a84654362c` |

### UUIDs de Equipo

| Rol | UUID | Email |
|---|---|---|
| TL | `92225290-6b6b-4c1f-a940-dcb4262507aa` | tl@memory-service.vtt.ai |
| BE | `ebbe3cee-abed-4b3b-860d-0a81f632b08a` | backend@memory-service.vtt.ai |
| DB | `6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7` | database@memory-service.vtt.ai |
| AR | `e9403c25-c1f8-4b64-b2ef-f447d53115e2` | ar@memory-service.vtt.ai |
| QA | `613c9538-658c-45fe-a6d7-c1ea9ff04b78` | qa@memory-service.vtt.ai |
| DO | `322e3745-9756-4a7c-af11-44b33edef44d` | devops@memory-service.vtt.ai |
| FE | `d23c9cd9-a156-433b-8900-94add5488eec` | frontend@memory-service.vtt.ai |

### UUIDs de Status

| Status | UUID |
|---|---|
| task_pending | `335fd9c6-f0d6-4966-a6ea-f518c78bc422` |
| task_in_progress | `2a76888a-e595-4cfc-ac4c-a3ae5087ef56` |
| task_in_review | `1ec975a5-7581-4a1a-ab8f-51b1a7ef868d` |
| task_completed | `aa5ceb90-5209-42a2-b874-a8cbee597a97` |
| task_on_hold | `c62eb334-b7bc-4c9f-af85-a5666c262aaa` |

### Priority IDs

| Prioridad | UUID |
|---|---|
| low | (verificar en VTT) |
| medium | `d0b619ef-27e7-42d8-8879-41030a602eed` |
| high | `1a617554-6319-4c56-826f-8ef49a0ff9cc` |

---

## PARTE 1 — ASIGNAR TAREA (16 pasos — PROCESO_ASIGNACION_TAREAS_v3.md)

### Paso 1 — Obtener JWT

```bash
TOKEN=$(python3 -c "
import urllib.request, json, sys
req = urllib.request.Request(
    'http://77.42.88.106:3000/api/auth/service-token',
    data=json.dumps({'userId': '92225290-6b6b-4c1f-a940-dcb4262507aa', 'serviceKey': 'hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d'}).encode(),
    headers={'Content-Type': 'application/json'}, method='POST')
with urllib.request.urlopen(req) as r:
    sys.stdout.write(json.loads(r.read())['data']['token'])
")
```

### Paso 2 — Crear tarea en VTT (si no existe)

```bash
curl -s -X POST "http://77.42.88.106:3000/api/phases/{PHASE_ID}/tasks" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "...",
    "description": "max 2000 chars",
    "priorityId": "<uuid>",
    "statusId": "335fd9c6-f0d6-4966-a6ea-f518c78bc422",
    "assignedToId": "<uuid_agente>",
    "assignedBy": "92225290-6b6b-4c1f-a940-dcb4262507aa",
    "category": "development",
    "complexity": "MEDIUM",
    "estimatedHours": 3,
    "createdBy": "92225290-6b6b-4c1f-a940-dcb4262507aa"
  }'
```

> **Gotcha:** usar `assignedToId` — `assigneeId` es ignorado silenciosamente.

### Paso 3 — Verificar dependencias

```bash
curl -s "http://77.42.88.106:3000/api/tasks/MS-XXX" -H "Authorization: Bearer $TOKEN" | python3 -c "
import sys,json; d=json.load(sys.stdin)['data']
print('isBlocked:', d.get('isBlocked'))
for dep in d.get('dependencies',[]): print(' DEP:', dep['task']['id'], dep['task']['status']['code'])
"
```

Si `isBlocked: True` → NO asignar. Esperar deps.

### Paso 4A — Verificar schema.prisma (OBLIGATORIO para tareas con Prisma)

> **Lección MS-303/305/310:** Nunca generar ASSIGNMENT con modelos Prisma sin leer el schema real.

```bash
# Leer schema real del worktree
cat c:/Users/Martin/Documents/virtual-teams/memory-service/.vtt/worktrees/backend-db/prisma/schema.prisma
```

**Modelos reales:** `SourceCatalog`, `ConversationTypeCatalog`, `ConversationStatusCatalog`, `WorkTypeCatalog`, `BlockTypeCatalog`, `MessageTypeCatalog`, `MessageStatusCatalog`, `PlatformCatalog`, `TopicCatalog`, `PriorityCatalog`

**NO existen:** `ModelCatalog`, `TurnRoleCatalog`, `ParticipantRoleCatalog`, `EntityTypeCatalog`

### Paso 5 — Generar ASSIGNMENT

Archivo: `knowledge/agent-tasks/assignments/ASSIGNMENT_MS-XXX_nombre.md`

Secciones obligatorias:
1. Objetivo + alcance
2. DOCUMENTOS DE REFERENCIA OBLIGATORIOS (rutas exactas)
3. Archivos a crear/modificar
4. Implementación detallada
5. Criterios de Aceptación (CAs)
6. Workflow del agente (pasos numerados)
7. Hardcode Check
8. **REPORTE al TL** — incluir instrucción de guardar como .md y mostrar en pantalla

**Instrucción de reporte OBLIGATORIA al final del ASSIGNMENT:**
```markdown
## REPORTE al TL

Al completar:
1. Guardar reporte como: `knowledge/agent-tasks/reports/04-development/<SPRINT>/MS-XXX_REPORT.md`
2. Mostrar el reporte completo en pantalla (cat del archivo)
3. Postearlo como comment en VTT (formato SKL-REPORT-01, 16 secciones)
```

### Paso 6 — Subir ASSIGNMENT a VTT

```bash
curl -s -X POST "http://77.42.88.106:3000/api/tasks/MS-XXX/attachments" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@knowledge/agent-tasks/assignments/ASSIGNMENT_MS-XXX_nombre.md" \
  -F "fileType=assignment" \
  -F "uploadedById=92225290-6b6b-4c1f-a940-dcb4262507aa"
```

### Paso 7 — Crear CAs en VTT

```bash
curl -s -X POST "http://77.42.88.106:3000/api/tasks/MS-XXX/criteria" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "CA-01: ...", "criteriaTypeCode": "acceptance", "required": true}'
```

> **Gotcha:** campo es `criteriaTypeCode`, NO `type`.

### Paso 8 — Generar y postear mensaje al agente

```bash
cd c:/Users/Martin/Documents/virtual-teams/memory-service/.vtt/worktrees/project-tl
python3 scripts/gen_mensaje.py MS-XXX --post
```

Si falla por >5000 chars → postear versión corta manualmente con Python.

**El mensaje SIEMPRE debe incluir:**
- Working directory del agente
- Lista de CAs con IDs
- Comandos JWT, in_progress, in_review
- UUID del agente
- Instrucción de guardar reporte como .md y mostrar en pantalla

---

## PARTE 2 — REVISAR TAREA (PROCESO_CIERRE_TAREA_v2.md)

### Paso 1 — Verificar review gate

```bash
curl -s "http://77.42.88.106:3000/api/tasks/MS-XXX/review-gate" -H "Authorization: Bearer $TOKEN" | python3 -c "
import sys,json; d=json.load(sys.stdin)['data']
print('canProceed:', d.get('canProceedToReview'))
print('blockers:', d.get('blockers',[]))
"
```

Debe ser `canProceedToReview: true` — si no, NO proceder.

### Paso 2 — Verificar CAs

```bash
curl -s "http://77.42.88.106:3000/api/tasks/MS-XXX/criteria" -H "Authorization: Bearer $TOKEN" | python3 -c "
import sys,json
for c in json.load(sys.stdin).get('data',[]): print(c['id'][:8], '|', c.get('status'), '|', c.get('title','')[:60])
"
```

Todos deben estar en `met`.

### Paso 3 — Verificar PR en GitHub

```bash
gh pr view <N> --repo NCoreSys/memory-service-backend --json state,mergeable,files
```

- `state: OPEN`
- `mergeable: MERGEABLE`
- Files solo del scope de la tarea

### Paso 4 — Modelo Dinámico (SKL-DYNAMIC-MODEL-01)

#### 4.1 Crear TIs detectados por el agente

```bash
curl -s -X POST "http://77.42.88.106:3000/api/projects/d0fc276d-e764-4a83-96e9-d65f086ed803/trackable-items" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "DEBT-XXX-NN",
    "title": "[DEFER R2] titulo",
    "description": "[Deferred to R2] descripcion",
    "typeCode": "tech_debt",
    "statusCode": "ti_draft",
    "createdById": "92225290-6b6b-4c1f-a940-dcb4262507aa"
  }'

# Vincular a la tarea
curl -s -X POST "http://77.42.88.106:3000/api/trackable-items/<TI_ID>/tasks" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"taskId":"MS-XXX","linkType":"related_to"}'
```

> **Gotcha:** `process_improvement` NO válido → usar `tech_debt` + marker `[PROCESS]`

#### 4.2 Agregar evidencias a TIs

```bash
curl -s -X POST "http://77.42.88.106:3000/api/trackable-items/<TI_ID>/evidence" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "link",
    "title": "[MS-XXX] [S2] descripcion corta",
    "url": "https://github.com/NCoreSys/memory-service-backend/pull/N",
    "description": "[TASK:MS-XXX] [SPRINT:S2] descripcion completa",
    "createdById": "92225290-6b6b-4c1f-a940-dcb4262507aa"
  }'
```

> **Gotcha:** endpoint singular `/evidence` (NO `/evidences`). Type enum: `document|link|test_result|screenshot` (NO `pr`).

#### 4.3 Resolver devlog entries

```bash
# Listar pendientes
curl -s "http://77.42.88.106:3000/api/tasks/MS-XXX/devlog" -H "Authorization: Bearer $TOKEN" | python3 -c "
import sys,json
for e in json.load(sys.stdin).get('data',[]): 
    if e.get('status')!='resolved': print(e['id'][:8], e.get('title','')[:60])
"

# Resolver cada uno
curl -s -X PATCH "http://77.42.88.106:3000/api/tasks/MS-XXX/devlog/<ENTRY_ID>/status" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "resolved", "resolution": "Revisado por TL durante cierre MS-XXX. <accion tomada>"}'
```

> **Gotcha:** `resolution` es REQUERIDO cuando status=`resolved`. Sin él → 400.

### Paso 5 — Postear APR-TL comment

```bash
curl -s -X POST "http://77.42.88.106:3000/api/tasks/MS-XXX/comments" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "### CODE REVIEW PASS — MS-XXX\n\n**CAs**: CA-01 ✅ CA-02 ✅\n**Devlog**: N entries\n**Review Gate**: passed\n**PR #N**: aprobado para merge", "userId": "92225290-6b6b-4c1f-a940-dcb4262507aa"}'
```

> **Gotcha:** máx 5000 chars. Dividir si excede.

### Paso 6 — Mover a task_completed

```bash
curl -s -X PATCH "http://77.42.88.106:3000/api/tasks/MS-XXX/status" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"statusId": "aa5ceb90-5209-42a2-b874-a8cbee597a97", "changedBy": "92225290-6b6b-4c1f-a940-dcb4262507aa"}'
```

---

## PARTE 3 — PROCESO DE BUGS / ISSUES

Cuando un agente reporta un bug o discrepancia:

1. **Agente** crea issue en su tarea (`POST /api/tasks/MS-XXX/issues`) → tarea queda en `task_on_hold`
2. **TL** crea tarea derivada (`POST /api/phases/{PHASE_ID}/tasks`)
3. **TL** genera ASSIGNMENT + CAs + mensaje completo para la tarea derivada
4. **TL** liga el issue a la tarea derivada:
   ```bash
   curl -s -X PUT "http://77.42.88.106:3000/api/issues/{ISSUE_ID}" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"resolvedByTaskId": "MS-YYY"}'
   ```
5. **Agente** ejecuta la tarea derivada y la completa (entrega normal)
6. **TL** revisa la tarea derivada → la mueve a `task_completed`
7. El sistema levanta automáticamente el hold de la tarea padre (MS-XXX)
8. **Agente** retoma MS-XXX

> **NUNCA:** fix ad-hoc, modificar código de tareas ya completadas sin pasar por este flujo.

---

## PARTE 4 — GOTCHAS CRÍTICOS DE VTT

| # | Problema | Solución |
|---|---|---|
| 1 | `assigneeId` ignorado | Usar `assignedToId` al crear tarea |
| 2 | `criteriaTypeCode` no `type` | Para crear CAs |
| 3 | Crear tarea: `POST /api/phases/{id}/tasks` | NO `POST /api/tasks` |
| 4 | Comments máx 5000 chars | Dividir o subir como attachment |
| 5 | `resolution` requerido en devlog resolve | Sin él → 400 |
| 6 | Evidence endpoint: `/evidence` (singular) | NO `/evidences` |
| 7 | Evidence type enum | `link|document|test_result|screenshot` (NO `pr`) |
| 8 | `process_improvement` NO válido | Usar `tech_debt` + marker `[PROCESS]` |
| 9 | Resolver issue: `PUT /api/issues/{id}` | NO `PATCH /api/tasks/:id/issues/:id` |
| 10 | Hold se levanta automático | Cuando `resolvedByTaskId` tarea pasa a `task_completed` |
| 11 | gen_mensaje.py genera >5000 chars | Postear versión corta manualmente |
| 12 | `assignedTo` no persiste via PATCH | Usar `assignedToId` al crear la tarea |

---

## PARTE 5 — REGLAS CRÍTICAS

1. **TL nunca mueve tareas a `task_in_progress`** — solo los agentes lo hacen
2. **No asignar tarea con `isBlocked: true`** — esperar deps
3. **Leer `prisma/schema.prisma` real** antes de generar ASSIGNMENT con modelos Prisma
4. **Todo ASSIGNMENT debe terminar con instrucción de reporte** — guardar .md + mostrar en pantalla + postear en VTT
5. **Bugs siguen el proceso formal** — nunca fix ad-hoc
6. **Comments `message` + `userId`** — NUNCA `content` + `authorId`
7. **Attachments requieren `uploadedById`** — sin él → 400
8. **Modelo dinámico al cerrar** — TIs + evidencias + devlog resolve, no opcional
9. **gen_mensaje.py siempre con `--post`** — si falla por chars, postear manualmente

---

## PARTE 6 — SCRIPTS DE USO FRECUENTE

### Ver tareas en review

```bash
curl -s "http://77.42.88.106:3000/api/tasks?projectId=d0fc276d-e764-4a83-96e9-d65f086ed803&status=task_in_review" \
  -H "Authorization: Bearer $TOKEN" | python3 -c "
import sys,json
for t in json.load(sys.stdin).get('data',[]): print(t['id'], '-', t['title'][:50])
"
```

### Ver estado general del proyecto

```bash
curl -s "http://77.42.88.106:3000/api/tasks?projectId=d0fc276d-e764-4a83-96e9-d65f086ed803" \
  -H "Authorization: Bearer $TOKEN" | python3 -c "
import sys,json
from collections import Counter
tasks = json.load(sys.stdin).get('data',[])
cnt = Counter(t['status']['code'] for t in tasks)
for s,n in sorted(cnt.items()): print(f'  {s}: {n}')
"
```

### Generar mensaje al agente

```bash
cd c:/Users/Martin/Documents/virtual-teams/memory-service/.vtt/worktrees/project-tl
python3 scripts/gen_mensaje.py MS-XXX --post
```

---

**Documentos relacionados:**
- `00-agent-setup/06.Documentos_soporte/PROCESO_ASIGNACION_TAREAS_v3.md`
- `00-agent-setup/06.Documentos_soporte/PROCESO_CIERRE_TAREA_v2.md`
- `.claude/agents/OPERATIVO_TL_MEMORY-SERVICE.md`
- `knowledge/platform-feedback/VTT_PLATFORM_GAPS_2026-05-13.md`
- `C:\Users\Martin\.claude\projects\...\memory\MEMORY.md`
