# Proceso de Asignación de Tareas - Tech Lead · Memory Service

**Fecha:** 2026-05-01
**Versión:** 2.0 — Modelo Dinámico V4
**Proyecto:** Memory Service (R1)

---

## Documentos Base (LEER SIEMPRE)

| # | Documento | Propósito |
|---|-----------|-----------|
| 1 | `.claude/agents/OPERATIVO_TL_MEMORY-SERVICE.md` | Rol del TL, UUIDs del equipo, credenciales |
| 2 | `00-platform/05.Templates/05.Proyecto/02.Genericos/TEMPLATE_ASIGNACION_TAREARev.md` | Template assignments (v3.0) |
| 3 | `knowledge/GUIA_AGENTES_MODELO_DINAMICO_V4.md` | Referencia completa endpoints V4 |
| 4 | `.claude/rules/PROJECT_RULES.md` | Reglas operativas del proyecto |
| 5 | `Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` | Fuente de verdad funcional |

---

## Datos del Proyecto

| Campo | Valor |
|-------|-------|
| VTT_BASE_URL | `http://77.42.88.106:3000` |
| PROJECT_ID | `d0fc276d-e764-4a83-96e9-d65f086ed803` |
| PROJECT_KEY | `MS` |
| SERVICE_KEY | `hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d` |
| Tech Lead UUID | `92225290-6b6b-4c1f-a940-dcb4262507aa` |

---

## Equipo

| Rol | UUID | Email |
|-----|------|-------|
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

## Las Dos Fases del Proceso (LL-005)

### FASE 1 — Planificación (al recibir handoff del PM)
- Leer handoff del PM: features, fechas, dependencias
- Generar plan del sprint con oleadas y bloqueantes
- Crear tareas en VTT vía API
- Generar BRIEFs y subirlos como attachments
- **No requiere leer código** — es planificación de alto nivel

### FASE 2 — Asignación (al momento de asignar una tarea)
- Escribir ASSIGNMENT con información actualizada desde el código real
- Completar `API/RECURSOS DISPONIBLES` desde routes/ y schemas reales — NO desde el handoff
- Subir ASSIGNMENT como attachment y asignar al agente

---

## Flujo Completo

### Paso 1: Recibir Handoff del PM
- Leer SPEC v1.9 para contexto funcional
- Analizar dependencias y definir oleadas

### Paso 2: Crear Tareas y BRIEFs (FASE 1)

```bash
# Crear tarea — token TL requerido
curl -s -X POST "http://77.42.88.106:3000/api/phases/{phaseId}/tasks" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "string",
    "description": "string (max 2000 chars)",
    "priorityId": "UUID",
    "statusId": "335fd9c6-f0d6-4966-a6ea-f518c78bc422",
    "assignedToId": "UUID_AGENTE",
    "assignedBy": "92225290-6b6b-4c1f-a940-dcb4262507aa",
    "category": "development",
    "complexity": "MEDIUM",
    "createdBy": "92225290-6b6b-4c1f-a940-dcb4262507aa"
  }'

# Subir BRIEF
curl -s -X POST "http://77.42.88.106:3000/api/tasks/MS-XXX/attachments" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@ruta/BRIEF_MS-XXX_nombre.md" \
  -F "fileType=brief" \
  -F "uploadedById=92225290-6b6b-4c1f-a940-dcb4262507aa"
```

### Paso 3: Generar Assignment (FASE 2)

Usar: `TEMPLATE_ASIGNACION_TAREARev.md` (v3.0)
Ubicación: `knowledge/agent-tasks/assignments/ASSIGNMENT_MS-XXX_nombre.md`

Además de los 8 elementos estándar, en Memory Service verificar:
- ADR-001: repo correcto del agente (memory-service-backend, memory-service-frontend, etc.)
- SPEC v1.9: sección relevante para la tarea
- Si toca API Memory Service: puerto 3002, no 3000

```bash
# Subir ASSIGNMENT
curl -s -X POST "http://77.42.88.106:3000/api/tasks/MS-XXX/attachments" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@ruta/ASSIGNMENT_MS-XXX_nombre.md" \
  -F "fileType=assignment" \
  -F "uploadedById=92225290-6b6b-4c1f-a940-dcb4262507aa"
```

### Paso 4: Asignar Tarea

```bash
curl -s -X PATCH "http://77.42.88.106:3000/api/tasks/MS-XXX" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"assigneeId": "UUID_AGENTE"}'
```

### Paso 5: Mensaje al Agente

```
Tienes tarea nueva asignada: MS-XXX — [Título].

1. Lee el ASSIGNMENT: knowledge/agent-tasks/assignments/ASSIGNMENT_MS-XXX_nombre.md
2. Lee el BRIEF: knowledge/agent-tasks/briefs/BRIEF_MS-XXX_nombre.md
3. Lee las reglas: .claude/rules/PROJECT_RULES.md
4. Lee tu OPERATIVO: .claude/agents/OPERATIVO_[ROL]_MEMORY-SERVICE.md

--- INDICACIONES DEL SISTEMA ---

0) Obtén tu JWT (ejecutar PRIMERO):
python3 -c "
import urllib.request, json, sys
req = urllib.request.Request(
    'http://77.42.88.106:3000/api/auth/service-token',
    data=json.dumps({'userId':'[UUID_AGENTE]','serviceKey':'hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d'}).encode(),
    headers={'Content-Type':'application/json'}, method='POST')
with urllib.request.urlopen(req) as r:
    sys.stdout.write(json.loads(r.read())['data']['token'])
"
Guarda como TOKEN=<resultado> — válido 30 días.

a) Mueve MS-XXX a in_progress:
curl -s -X PATCH http://77.42.88.106:3000/api/tasks/MS-XXX/status \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"statusId":"2a76888a-e595-4cfc-ac4c-a3ae5087ef56","changedBy":"[UUID_AGENTE]"}'

b) Trabaja la tarea siguiendo el workflow del assignment (12 pasos).

c) Durante la tarea — registra en VTT:
   Decisiones: POST http://77.42.88.106:3000/api/tasks/MS-XXX/devlog-entries
   body: {"categoryCode":"decision","severity":null,"title":"...","reportedBy":"[UUID_AGENTE]"}
   
   Blockers: POST http://77.42.88.106:3000/api/tasks/MS-XXX/devlog-entries
   body: {"categoryCode":"blocker","severity":"high","title":"...","reportedBy":"[UUID_AGENTE]"}
   
   CAs cumplidos: POST http://77.42.88.106:3000/api/tasks/MS-XXX/criteria/[criteriaId]/fulfill
   body: {"status":"met","evidence":"descripción de evidencia"}

d) ANTES de in_review — sube entregables:
   curl -s -X POST "http://77.42.88.106:3000/api/tasks/MS-XXX/attachments" \
     -H "Authorization: Bearer $TOKEN" \
     -F "file=@knowledge/development-log/YYYY-MM-DD_MS-XXX_slug.md" \
     -F "fileType=devlog" -F "uploadedById=[UUID_AGENTE]"
   
   curl -s -X POST "http://77.42.88.106:3000/api/tasks/MS-XXX/attachments" \
     -H "Authorization: Bearer $TOKEN" \
     -F "file=@knowledge/code-logic/[espejo]/archivo.LOGIC.md" \
     -F "fileType=code_logic" -F "uploadedById=[UUID_AGENTE]"

e) Verifica el review gate:
curl -s "http://77.42.88.106:3000/api/tasks/MS-XXX/review-gate" -H "Authorization: Bearer $TOKEN"
→ Si canProceedToReview = false → resolver entries critical/high primero.

f) Mueve MS-XXX a in_review:
curl -s -X PATCH http://77.42.88.106:3000/api/tasks/MS-XXX/status \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"statusId":"1ec975a5-7581-4a1a-ab8f-51b1a7ef868d","changedBy":"[UUID_AGENTE]"}'

g) Pega tu reporte de entrega (formato SKL-REPORT-01) como comentario en esta tarea:
curl -s -X POST http://77.42.88.106:3000/api/tasks/MS-XXX/comments \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"message": "[REPORTE_ENTREGA]", "userId": "[UUID_AGENTE]"}'

Datos del sistema:
- Tu UUID: [UUID_AGENTE]
- SERVICE_KEY: hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d
- VTT_BASE_URL: http://77.42.88.106:3000
- Swagger VTT: http://77.42.88.106:3000/api-docs
- Swagger Memory API: http://[host]:3002/api-docs
```

---

## Comandos del TL para Review

```python
# Obtener token TL
import urllib.request, json

req = urllib.request.Request(
    'http://77.42.88.106:3000/api/auth/service-token',
    data=json.dumps({
        'userId': '92225290-6b6b-4c1f-a940-dcb4262507aa',
        'serviceKey': 'hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d'
    }).encode(),
    headers={'Content-Type': 'application/json'}, method='POST')
with urllib.request.urlopen(req) as r:
    token = json.loads(r.read())['data']['token']

# Mover a completed
req2 = urllib.request.Request(
    'http://77.42.88.106:3000/api/tasks/MS-XXX/status',
    data=json.dumps({
        'statusId': 'aa5ceb90-5209-42a2-b874-a8cbee597a97',
        'changedBy': '92225290-6b6b-4c1f-a940-dcb4262507aa'
    }).encode(),
    headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token},
    method='PATCH')
with urllib.request.urlopen(req2) as r2:
    print(json.loads(r2.read()))
```

```bash
# Comentario APR-TL
curl -s -X POST "http://77.42.88.106:3000/api/tasks/MS-XXX/comments" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"message": "APR-TL: revisión técnica aprobada. [Notas]", "userId": "92225290-6b6b-4c1f-a940-dcb4262507aa"}'

# Review gate
curl -s "http://77.42.88.106:3000/api/tasks/MS-XXX/review-gate" -H "Authorization: Bearer $TOKEN"

# Devlog entries pendientes
curl -s "http://77.42.88.106:3000/api/tasks/MS-XXX/devlog-entries?status=pending" -H "Authorization: Bearer $TOKEN"

# CAs fulfill
curl -s "http://77.42.88.106:3000/api/tasks/MS-XXX/criteria-fulfillments" -H "Authorization: Bearer $TOKEN"
```

---

## UUIDs de Status

| Status | UUID |
|--------|------|
| task_created | `0e54089b-296a-4d80-bcd3-80a7a71f1696` |
| task_pending | `335fd9c6-f0d6-4966-a6ea-f518c78bc422` |
| task_in_progress | `2a76888a-e595-4cfc-ac4c-a3ae5087ef56` |
| task_in_review | `1ec975a5-7581-4a1a-ab8f-51b1a7ef868d` |
| task_completed | `aa5ceb90-5209-42a2-b874-a8cbee597a97` |
| task_approved | `b9ca4951-6e14-4d82-b1d8-440793bbaf47` |
| task_on_hold | `c62eb334-b7bc-4c9f-af85-a5666c262aaa` |

---

## Reglas Críticas

1. **UNA tarea a la vez** — regla LL-001 del proyecto
2. **BRIEF = adjunto al crear. ASSIGNMENT = adjunto al asignar.**
3. **Review gate limpio antes de in_review** — obligatorio, no saltar
4. **Devlog entries obligatorios** — decisiones, blockers, ADRs durante la tarea
5. **CAs con fulfill en VTT** — no solo en el reporte escrito
6. **on-hold via PUT /on-hold con x-user-id** — NUNCA PATCH /status
7. **Comentarios: `message` + `userId`** — NUNCA `content` + `authorId`
8. **Attachments: `uploadedById` obligatorio** — sin él → 400
9. **ADR-001:** cada agente trabaja en su repo correspondiente con su PAT
10. **SPEC v1.9** es la fuente de verdad funcional — cualquier cambio requiere ADR

---

## Changelog

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 2.0 | 2026-05-01 | Customización Memory Service. Modelo Dinámico V4: review-gate en flujo, devlog entries obligatorios, CAs fulfill, TrackableItems. Mensaje al agente con pasos c/d/e/f/g y URLs reales. Comandos TL con UUID real. |
| 1.4 | 2026-03-19 | Versión base — LL-005, dos fases, template desde artefactos |
