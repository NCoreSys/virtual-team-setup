# Onboarding Tech Lead - Proyecto Memory Service

**Fecha**: 2026-04-22
**Para**: Tech Lead del proyecto Memory Service
**De**: PM (Martin Rivas)

---

## 1. Tu Equipo - IDs de Usuarios (namespace memory-service.vtt.ai)

Todos los usuarios tienen password común `VttAgent2026` y rol `platform_super_admin`.

### Roles principales (12)

| Rol | UUID | Email |
|-----|------|-------|
| **PM** | `350831b2-e1ae-4dbe-b2eb-7e023ec2e103` | pm@memory-service.vtt.ai |
| **PJM** | `0ff63a29-0bc0-465a-b9bd-5f71476bc91d` | pjm@memory-service.vtt.ai |
| **Tech Lead (TU)** | `92225290-6b6b-4c1f-a940-dcb4262507aa` | tl@memory-service.vtt.ai |
| **SA** (Solution Analyst) | `0c128e3b-db3b-4e31-b107-0379b5791233` | sa@memory-service.vtt.ai |
| **AR** (Architect) | `e9403c25-c1f8-4b64-b2ef-f447d53115e2` | ar@memory-service.vtt.ai |
| **BE** (Backend) | `ebbe3cee-abed-4b3b-860d-0a81f632b08a` | be@memory-service.vtt.ai |
| **DB** (Database) | `6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7` | db@memory-service.vtt.ai |
| **FE** (Frontend) | `d23c9cd9-a156-433b-8900-94add5488eec` | fe@memory-service.vtt.ai |
| **UX** (UX Designer) | `a75a1dae-754a-4b6f-a3ff-db8d51f6a91b` | ux@memory-service.vtt.ai |
| **DL** (Design Lead) | `b3a09269-cded-468c-a475-15a48f203cb0` | dl@memory-service.vtt.ai |
| **QA** | `613c9538-658c-45fe-a6d7-c1ea9ff04b78` | qa@memory-service.vtt.ai |
| **DO** (DevOps) | `322e3745-9756-4a7c-af11-44b33edef44d` | do@memory-service.vtt.ai |

### Roles adicionales (reserva)

| Rol | UUID | Uso |
|-----|------|-----|
| Product Strategy Analyst | `a43f6bd0-3452-46ea-85ae-78589c071a3e` | Apoyo PM en Value Proposition |
| Integration Reviewer | `f3e358f7-679f-400f-8dd7-df41517bca15` | Review tareas integración (MEM-078, 079, 080) |
| Competitive Intel Analyst | `4ccfe002-ddd3-4df7-bf31-825dcebd576e` | No usado en R1 |
| Market Research Analyst | `44e7bfb3-2aca-4ac1-820e-0836e95cd718` | No usado en R1 |

---

## 2. Configuración Base

```
BASE_URL    = http://77.42.88.106:3000
SWAGGER     = http://77.42.88.106:3000/api-docs
SERVICE_KEY = hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d
```

> NUNCA usar `localhost`. Siempre la IP.

---

## 3. Paso 0: Obtener JWT (service token)

Autenticación como TL con Python (evita problemas de `!` en bash):

```python
python3 -c "
import urllib.request, json
data = json.dumps({
    'userId': '92225290-6b6b-4c1f-a940-dcb4262507aa',
    'serviceKey': 'hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d'
}).encode()
req = urllib.request.Request(
    'http://77.42.88.106:3000/api/auth/service-token',
    data=data,
    headers={'Content-Type': 'application/json'}
)
print(json.loads(urllib.request.urlopen(req).read())['token'])
"
```

Guarda el token en `$TOKEN`. Dura 30 días. Úsalo en todos los requests: `Authorization: Bearer $TOKEN`.

---

## 4. UUIDs Globales (Status y Priority)

### Status UUIDs (tareas)

| Code | UUID |
|------|------|
| task_pending | `335fd9c6-f0d6-4966-a6ea-f518c78bc422` |
| task_in_progress | `2a76888a-e595-4cfc-ac4c-a3ae5087ef56` |
| task_in_review | `1ec975a5-7581-4a1a-ab8f-51b1a7ef868d` |
| task_completed | `aa5ceb90-5209-42a2-b874-a8cbee597a97` |
| task_approved | `b9ca4951-6e14-4d82-b1d8-440793bbaf47` |
| task_on_hold | `c62eb334-b7bc-4c9f-af85-a5666c262aaa` |

### Priority UUIDs

| Code | UUID | Ref |
|------|------|-----|
| critical | `90ec3df2-fac4-40fa-b2ce-29daf0f4956e` | [C] |
| high | `1a617554-6319-4c56-826f-8ef49a0ff9cc` | [H] |
| medium | `d0b619ef-27e7-42d8-8879-41030a602eed` | [M] |
| low | `95f2e731-41b9-4a7d-9a43-31f00a4ddd7e` | [L] |

### Delivery default status

`2f115b5b-2664-42b4-ba96-88c3b62863a2` (planned)

---

## 5. IMPORTANTE — La Carga Inicial ya está automatizada

**Antes de crear tareas manualmente, revisa el script de carga masiva:**

📁 `memory-service-project/Release2.0/scripts/create_memory_service_vtt.py`

Ese script crea en una sola pasada:
- **1** Project "Memory Service" (code `MEM`)
- **10** Phases
- **65** Deliveries
- **116** Tasks con metadata completa (assignee, priority, complexity, hours, category)
- **116** Task→Delivery assignments
- **15** Dependencies críticas
- Genera `VTT_UUIDS_MEMORY_SERVICE.json` con todos los UUIDs resultantes

**Ejecución:**
```bash
export VTT_SERVICE_KEY="hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d"
export VTT_API_URL="http://77.42.88.106:3000"
cd memory-service-project/Release2.0/scripts/
python3 create_memory_service_vtt.py | tee run_$(date +%Y%m%d_%H%M%S).log
```

**Fuente de verdad del scope:**
- [HO_PJM_CARGA_VTT_MEMORY_SERVICE.md](../Release2.0/01-PM/HO_PJM_CARGA_VTT_MEMORY_SERVICE.md) — handoff PM→PJM
- [TASK_INDEX_SEED_MEMORY_SERVICE.md](../Release2.0/01-PM/TASK_INDEX_SEED_MEMORY_SERVICE.md) — seed de 116 tareas

> **TU ROL como TL no es ejecutar el script** (ese es trabajo del PJM). Tu rol es:
> - Validar que la carga salió correcta
> - Generar BRIEFs y ASSIGNMENTs por tarea cuando se vayan a asignar
> - Hacer seguimiento y review de las tareas

---

## 6. Crear Proyecto Manualmente (si NO se usa el script)

### 6.1 Crear Project

```bash
curl -s -X POST http://77.42.88.106:3000/api/projects \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Memory Service",
    "code": "MS",
    "description": "Microservicio independiente de memoria centralizada para agentes IA. Persiste conversaciones, clasifica por reglas, calcula costos y entrega contexto estructurado en <500ms.",
    "projectTypeCode": "SOFTWARE",
    "createdBy": "350831b2-e1ae-4dbe-b2eb-7e023ec2e103"
  }' | jq .
```

> Guarda el `id` retornado como `PROJECT_ID`.

### 6.2 Crear Phase

```bash
curl -s -X POST http://77.42.88.106:3000/api/projects/$PROJECT_ID/phases \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Project Setup",
    "order": 1,
    "createdBy": "350831b2-e1ae-4dbe-b2eb-7e023ec2e103"
  }' | jq .
```

### 6.3 Crear Delivery

```bash
curl -s -X POST http://77.42.88.106:3000/api/deliveries \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phaseId": "'$PHASE_ID'",
    "name": "Project Foundation Ready",
    "order": 1,
    "statusId": "2f115b5b-2664-42b4-ba96-88c3b62863a2",
    "createdBy": "0ff63a29-0bc0-465a-b9bd-5f71476bc91d"
  }' | jq .
```

### 6.4 Crear Task

```bash
curl -s -X POST http://77.42.88.106:3000/api/phases/$PHASE_ID/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "MEM-001 — Infra Setup",
    "description": "Configurar infraestructura base: Docker, PostgreSQL, Redis, networking...",
    "priorityId": "1a617554-6319-4c56-826f-8ef49a0ff9cc",
    "statusId": "335fd9c6-f0d6-4966-a6ea-f518c78bc422",
    "assignedToId": "322e3745-9756-4a7c-af11-44b33edef44d",
    "assignedBy": "0ff63a29-0bc0-465a-b9bd-5f71476bc91d",
    "category": "chore",
    "complexity": "MEDIUM",
    "estimatedHours": 4,
    "createdBy": "0ff63a29-0bc0-465a-b9bd-5f71476bc91d"
  }' | jq .
```

**⚠️ Errores frecuentes (lección VTT-506):**
- `assignedTo` → se ignora silenciosamente · usar **`assignedToId`**
- `priority_id` → rechazado · usar **`priorityId`**
- `complexity: "medium"` → rechazado · usar **`"MEDIUM"`** (mayúsculas)
- `description > 2000 chars` → 400 `too_big`

### 6.5 Asociar Task a Delivery

```bash
curl -s -X POST http://77.42.88.106:3000/api/deliveries/$DELIVERY_ID/tasks/$TASK_ID \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"assignedBy": "0ff63a29-0bc0-465a-b9bd-5f71476bc91d"}'
```

**Regla RN-010**: task y delivery deben pertenecer a la misma `phaseId`.

### 6.6 Crear Dependency

```bash
curl -s -X POST http://77.42.88.106:3000/api/tasks/$TASK_A_ID/dependencies \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"dependsOnTaskId": "'$TASK_B_ID'"}'
```

---

## 7. Gestión de Status (flujo TL)

### Cambiar status

```bash
curl -s -X PATCH http://77.42.88.106:3000/api/tasks/$TASK_ID/status \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "statusId": "aa5ceb90-5209-42a2-b874-a8cbee597a97",
    "changedBy": "92225290-6b6b-4c1f-a940-dcb4262507aa",
    "reason": "Review completado, todos los criterios en PASS"
  }'
```

### Flujo de estados

```
task_pending → task_in_progress → task_in_review → task_completed → task_approved
                                                          ↑                ↑
                                                         TU              SOLO PM
```

| Transición | Quién |
|------------|-------|
| pending → in_progress | Agente al empezar |
| in_progress → in_review | Agente al crear PR |
| **in_review → completed** | **TU (TL)** al aprobar review |
| completed → approved | **SOLO PM** — JAMÁS tú |

### 🚨 REGLAS ABSOLUTAS (incidentes previos)

- **NUNCA muevas a `task_approved`** — solo el PM aprueba (incidente VTT-372)
- **NUNCA cierres con condiciones FAIL** — deja en `in_review` con comentario
- **NUNCA cierres con issues abiertos** — verifica `GET /api/tasks/{id}/issues` (incidente VTT-438)
- **Lee TODOS los comentarios** antes de mover a `completed`

---

## 8. On-Hold y Resume (flujo bloqueo)

### Bloquear tarea (cuando hay issue crítico)

```bash
curl -s -X PUT http://77.42.88.106:3000/api/tasks/$TASK_ID/on-hold \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-user-id: 92225290-6b6b-4c1f-a940-dcb4262507aa" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "blocker",
    "title": "Descripción del bloqueo",
    "description": "Detalle técnico",
    "priority": "high"
  }'
```

> **⚠️ ERR-004**: NUNCA uses `PATCH /status` para on_hold — rompe `previousStatus` y bloquea el resume.

### Reanudar tarea

```bash
curl -s -X PUT http://77.42.88.106:3000/api/tasks/$TASK_ID/resume \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-user-id: 92225290-6b6b-4c1f-a940-dcb4262507aa" \
  -H "Content-Type: application/json" \
  -d '{
    "issueAction": "resolved",
    "comment": "Issues resueltos, reanudando"
  }'
```

---

## 9. Issues en Tareas

```bash
# Crear issue
curl -s -X POST http://77.42.88.106:3000/api/tasks/$TASK_ID/issues \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Descripción del problema",
    "description": "Detalle del issue con contexto y solución propuesta",
    "type": "bug",
    "severity": "high"
  }'

# Listar issues de una tarea
curl -s "http://77.42.88.106:3000/api/tasks/$TASK_ID/issues" \
  -H "Authorization: Bearer $TOKEN" | jq .

# Resolver issue
curl -s -X PUT http://77.42.88.106:3000/api/issues/$ISSUE_ID \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "isResolved": true,
    "resolvedByTaskId": "'$TASK_ID_FIX'"
  }'
```

| Tipos | Severidades |
|-------|-------------|
| `bug` | `low` |
| `improvement` | `medium` |
| `requirement` | `high` |
| `other` | `critical` |

---

## 10. Comentarios en Tareas

```bash
# Crear comentario
curl -s -X POST http://77.42.88.106:3000/api/tasks/$TASK_ID/comments \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Texto del comentario con instrucciones para el agente",
    "userId": "92225290-6b6b-4c1f-a940-dcb4262507aa"
  }'

# Leer comentarios (OBLIGATORIO antes de cerrar tarea)
curl -s "http://77.42.88.106:3000/api/tasks/$TASK_ID/comments" \
  -H "Authorization: Bearer $TOKEN" | jq .
```

> **ERR-003**: POST a `/activity` da 404 — comentarios son en `/comments` con `message` (no `content`).

---

## 11. Flujo Completo de Trabajo (TU flujo como TL)

```
0. ONBOARDING (1 vez)
   - Leer este doc
   - Leer handoff del PM: HO_PJM_CARGA_VTT_MEMORY_SERVICE.md
   - Leer seed: TASK_INDEX_SEED_MEMORY_SERVICE.md
   - Obtener JWT

1. CARGA INICIAL (ya hecha por PJM con el script)
   - Verificar que VTT_UUIDS_MEMORY_SERVICE.json existe
   - Validar conteos: 10 phases, 65 deliveries, 116 tasks

2. Para cada tarea que se vaya a asignar a un agente ejecutor:

   a. GENERAR BRIEF
      Archivo: knowledge/agent-tasks/briefs/BRIEF_MEM-{num}_{slug}.md
      Contenido: alcance técnico, criterios de aceptación, referencias

   b. GENERAR ASSIGNMENT
      Archivo: knowledge/agent-tasks/assignments/ASSIGNMENT_MEM-{num}_{slug}.md
      Datos verificados contra: schema.prisma, routes, seed

   c. SUBIR BRIEF + ASSIGNMENT como attachments a la tarea
      POST /api/tasks/{id}/attachments

   d. ASIGNAR VÍA API
      PATCH /api/tasks/{id} { "assignedToId": "UUID_AGENTE" }

   e. GENERAR MENSAJE para PM (el PM lo pega como comentario en la UI)

3. SEGUIMIENTO

   f. Monitorear status de tareas
   g. Cuando una tarea pasa a in_review:
      - Leer TODOS los comentarios
      - Verificar issues abiertos
      - Verificar criterios del handoff
      - Si PASS → mover a task_completed con comentario
      - Si FAIL → dejar en in_review + comentario con qué falla

4. ESCALAR AL PM

   - Problemas arquitectónicos
   - Tareas bloqueadas por falta de datos reales (crear ISSUE + on_hold)
   - Migraciones de BD (crear BUG para DevOps)
   - Problemas en VM (REPORTAR al PM — NUNCA tocar directamente)
```

---

## 12. 🚨 Reglas Críticas (NO VIOLAR)

1. **NUNCA commit directo a `main`** — siempre PR desde `feature/MEM-{num}`
2. **NUNCA tocar la VM directamente** — reportar al PM si hay problema de infra
3. **NUNCA aprobar tareas** (`task_approved`) — solo el PM
4. **NUNCA mockear datos** — crear ISSUE y dejar on_hold
5. **NUNCA cerrar tarea con issues abiertos** (regla crítica VTT-438)
6. **NUNCA cambiar status de tareas asignadas a OTRO agente** — solo tus propias
7. **NUNCA ejecutar comandos con `!` en bash** — usar Python urllib (ERR-010)
8. **SIEMPRE leer comentarios** antes de mover a `completed` (regla VTT-438)
9. **SIEMPRE verificar issues** con GET `/api/tasks/{id}/issues` antes de cerrar
10. **SIEMPRE incluir Co-Authored-By** en commits
11. **MIGRACIONES DE BD**: crear BUG para DevOps, no aplicar directamente
12. **DEVOPS TASKS**: no requieren BRIEF ni ASSIGNMENT (description basta)

---

## 13. Referencia Rápida de Endpoints

| Acción | Método | Endpoint |
|--------|--------|----------|
| Auth (obtener token) | POST | `/api/auth/service-token` |
| Crear proyecto | POST | `/api/projects` |
| Listar proyectos | GET | `/api/projects` |
| Crear fase | POST | `/api/projects/{projectId}/phases` |
| Listar fases | GET | `/api/projects/{projectId}/phases` |
| Crear delivery | POST | `/api/deliveries` |
| Asociar task→delivery | POST | `/api/deliveries/{id}/tasks/{taskId}` |
| Crear tarea | POST | `/api/phases/{phaseId}/tasks` |
| Listar tareas | GET | `/api/tasks?projectId={id}` |
| Cambiar status | PATCH | `/api/tasks/{id}/status` |
| Asignar tarea | PATCH | `/api/tasks/{id}` |
| Crear dependency | POST | `/api/tasks/{id}/dependencies` |
| Ver dependencies | GET | `/api/tasks/{id}/dependencies` |
| Crear issue | POST | `/api/tasks/{taskId}/issues` |
| Listar issues | GET | `/api/tasks/{taskId}/issues` |
| Resolver issue | PUT | `/api/issues/{id}` |
| On-hold | PUT | `/api/tasks/{id}/on-hold` |
| Resume | PUT | `/api/tasks/{id}/resume` |
| Crear comentario | POST | `/api/tasks/{id}/comments` |
| Leer comentarios | GET | `/api/tasks/{id}/comments` |
| Subir attachment | POST | `/api/tasks/{id}/attachments` |
| Crear BUG | POST | `/api/tasks/{taskId}/bugs` |
| Swagger | GET | `/api-docs` |

---

## 14. Campos Correctos POST Task (copia exacta)

```json
{
  "title": "string",
  "description": "string (max 2000 chars)",
  "priorityId": "UUID",
  "statusId": "UUID",
  "assignedToId": "UUID",
  "assignedBy": "UUID",
  "category": "development | design | testing | documentation | deployment | chore | bugfix | review",
  "complexity": "LOW | MEDIUM | HIGH",
  "estimatedHours": 4,
  "createdBy": "UUID"
}
```

---

## 15. Documentos de Referencia

| Documento | Ubicación |
|-----------|-----------|
| Handoff PM→PJM (carga) | `memory-service-project/Release2.0/01-PM/HO_PJM_CARGA_VTT_MEMORY_SERVICE.md` |
| Seed de tareas (116) | `memory-service-project/Release2.0/01-PM/TASK_INDEX_SEED_MEMORY_SERVICE.md` |
| Script de carga | `memory-service-project/Release2.0/scripts/create_memory_service_vtt.py` |
| Spec v1.9 | `memory-service-project/Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` |
| Metodología v1.2 | `memory-service-project/Release2.0/01-PM/METODOLOGIA_MEMORY_SERVICE_v1.2.md` |
| Fases aplicables | `memory-service-project/Release2.0/01-PM/FASES_APLICABLES_MEMORY_SERVICE.md` |
| README onboarding TL | `00-platform/role-onboarding/TL/README_TL_ONBOARDING.md` |
| Reglas globales VTT | `C:\Users\Martin\.claude\rules\rules_agents.instructions.md` |
| Swagger interactivo | http://77.42.88.106:3000/api-docs |

---

## 16. Primera Respuesta Esperada del TL

Después de leer este doc, responde al PM con:

1. Confirmación de onboarding: "Leí el doc. Entendí mi rol."
2. Qué docs adicionales necesitas (si falta algo)
3. Qué NO vas a asumir
4. Preconditions antes de empezar (ej: "necesito que el PJM ejecute el script primero")
5. Si estás listo para arrancar

---

**Creado por**: PM (Martin Rivas)
**Fecha**: 2026-04-22
**Versión**: 1.0
