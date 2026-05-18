# OPERATIVO — Tech Lead | Memory Service

**Proyecto:** Memory Service (independiente de VTT)
**Rol:** Tech Lead (TL)
**Repo:** `c:\Users\Martin\Documents\virtual-teams\memory-service\`
**Última actualización:** 2026-04-21

---

## 1. IDENTIDAD DEL AGENTE

| Dato | Valor |
|------|-------|
| **Rol** | Tech Lead |
| **UUID** | `92225290-6b6b-4c1f-a940-dcb4262507aa` |
| **Email** | tl@memory-service.vtt.ai |
| **Proyecto ID** | `d0fc276d-e764-4a83-96e9-d65f086ed803` |
| **Project Key** | MS |

---

## 2. BACKEND VTT (Source of Truth de tareas)

| Dato | Valor |
|------|-------|
| **API URL** | `http://77.42.88.106:3000` |
| **SERVICE_KEY** | leer de `$MEM_VTT_SERVICE_KEY` (NO hardcodear en docs versionados — ver HO_ACTUALIZAR_TAREAS_VTT.md §1) |
| **Auth** | JWT vía `POST /api/auth/service-token` con SERVICE_KEY + UUID → response `.data.token` |

### Phase IDs del proyecto Memory Service (10 fases, 116 tareas, 381h)

| Order | Fase | Phase UUID | Tareas | Horas |
|-------|------|-----------|--------|-------|
| 1 | Project Setup | `83f56bad-7e60-4ffa-bc19-9c0f9ba097a1` | MEM-001..005 | 11h |
| 2 | Discovery | `3ee3a429-f836-45ea-afde-1753c78db9ac` | MEM-006..009 | 9h |
| 3 | Planning | `a0dcfb69-b862-4784-b8c9-5aad233dfb9d` | MEM-010..017 | 23h |
| 4 | Analysis | `26ecb1f6-1eb8-494f-930e-7e173c4ee559` | MEM-018..025 | 41h |
| 5 | Design UX/UI | `2c8f0f2f-992a-46e5-b80f-9739180c2532` | MEM-026..038 | 35h |
| 6 | Design Technical | `5f452a38-6cc6-4bbc-a8d5-1f50da2562af` | MEM-039..047 | 45h |
| 7 | Development | `c2804591-b21c-4340-9065-59fd23e14b63` | MEM-048..093 | 116h |
| 8 | Testing | `7ab83ed0-2238-4241-a915-8a957144d63e` | MEM-094..103 | 60h |
| 9 | Deploy | `137d3082-f280-48da-81e7-abd3c1789f63` | MEM-104..110 | 26h |
| 10 | Operations | `2ffc2179-2376-4197-93d1-56a878cd976e` | MEM-111..116 | 15h |

### Priority IDs

| Prioridad | UUID |
|-----------|------|
| medium | `d0b619ef-27e7-42d8-8879-41030a602eed` |
| high | `1a617554-6319-4c56-826f-8ef49a0ff9cc` |

### API Gotchas confirmados (HO v2.1)

| # | Gotcha | Implicación |
|---|--------|-------------|
| 1 | `POST /api/phases/:id/tasks` ignora `assigneeId` | Usar PATCH posterior |
| 2 | POST/PATCH task aceptan `deliveryId` pero NO lo persisten | GET task no devuelve `deliveryId` — documentado como issue pendiente |
| 3 | `POST /api/projects` ignora `deliverables[]` | Deliveries creadas por endpoint dedicado |
| 4 | Naming inconsistente POST `/deliverables` vs GET `/deliveries` | No afecta operación actual |

---

## 3. EQUIPO DEL PROYECTO (12 roles)

| Sigla | Rol | UUID |
|-------|-----|------|
| PM  | Product Manager | `350831b2-e1ae-4dbe-b2eb-7e023ec2e103` |
| PJM | Project Manager | `0ff63a29-0bc0-465a-b9bd-5f71476bc91d` |
| **TL**  | **Tech Lead (YO)** | `92225290-6b6b-4c1f-a940-dcb4262507aa` |
| SA  | System Architect | `0c128e3b-db3b-4e31-b107-0379b5791233` |
| AR  | Architect | `e9403c25-c1f8-4b64-b2ef-f447d53115e2` |
| BE  | Backend Engineer | `ebbe3cee-abed-4b3b-860d-0a81f632b08a` |
| DB  | Database Engineer | `6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7` |
| FE  | Frontend Engineer | `d23c9cd9-a156-433b-8900-94add5488eec` |
| UX  | UX Engineer | `a75a1dae-754a-4b6f-a3ff-db8d51f6a91b` |
| DL  | Design Lead | `b3a09269-cded-468c-a475-15a48f203cb0` |
| QA  | QA Engineer | `613c9538-658c-45fe-a6d7-c1ea9ff04b78` |
| DO  | DevOps | `322e3745-9756-4a7c-af11-44b33edef44d` |

---

## 4. AUTH — Obtener JWT token

### Script Python (recomendado)

```python
import os, requests

API_URL = "http://77.42.88.106:3000"
TL_UUID = "92225290-6b6b-4c1f-a940-dcb4262507aa"
SERVICE_KEY = os.environ["MEM_VTT_SERVICE_KEY"]  # NO hardcodear

resp = requests.post(
    f"{API_URL}/api/auth/service-token",
    json={"userId": TL_UUID, "serviceKey": SERVICE_KEY},
    timeout=10,
)
resp.raise_for_status()
TOKEN = resp.json()["data"]["token"]
print(TOKEN)
```

### curl

```bash
curl -s -X POST http://77.42.88.106:3000/api/auth/service-token \
  -H "Content-Type: application/json" \
  -d "{\"userId\":\"92225290-6b6b-4c1f-a940-dcb4262507aa\",\"serviceKey\":\"$MEM_VTT_SERVICE_KEY\"}" \
  | jq -r .data.token
```

Guarda el resultado como `$TOKEN` y reúsalo en todos los requests posteriores.

---

## 5. COMANDOS DE ARRANQUE (ejecutar al iniciar sesión)

### 5.1 Listar mis tareas asignadas

```bash
curl -s "$API_URL/api/tasks?assigneeId=$TL_UUID" \
  -H "Authorization: Bearer $TOKEN" | jq '.[] | {id, title, status, priority}'
```

### 5.2 Tareas `task_in_review` del proyecto (pendientes de mi review)

```bash
curl -s "$API_URL/api/tasks?projectId=d0fc276d-e764-4a83-96e9-d65f086ed803&status=task_in_review" \
  -H "Authorization: Bearer $TOKEN" | jq '.[] | {id, title, assigneeId}'
```

### 5.3 Tareas `task_on_hold` del proyecto (blockers a conocer)

```bash
curl -s "$API_URL/api/tasks?projectId=d0fc276d-e764-4a83-96e9-d65f086ed803&status=task_on_hold" \
  -H "Authorization: Bearer $TOKEN" | jq '.[] | {id, title, blockedReason}'
```

### 5.4 Estado global del proyecto (todas las tareas)

```bash
curl -s "$API_URL/api/tasks?projectId=d0fc276d-e764-4a83-96e9-d65f086ed803" \
  -H "Authorization: Bearer $TOKEN" | jq 'group_by(.status) | map({status: .[0].status, count: length})'
```

---

## 6. CAMBIOS DE STATUS (uso frecuente)

Estados VTT: `pending` → `task_assigned` → `task_in_progress` → `task_in_review` → `task_completed` (happy path).
Estados de excepción: `task_on_hold`, `task_rejected`, `task_cancelled`.

### Aprobar tarea después de code review

```bash
curl -s -X PATCH "$API_URL/api/tasks/{TASK_ID}/status" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status":"task_completed","reviewerId":"92225290-6b6b-4c1f-a940-dcb4262507aa","comment":"Approved por TL: <razón>"}'
```

### Rechazar tarea (pedir cambios)

```bash
curl -s -X PATCH "$API_URL/api/tasks/{TASK_ID}/status" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status":"task_rejected","reviewerId":"92225290-6b6b-4c1f-a940-dcb4262507aa","comment":"Rechazada: <razón + qué arreglar>"}'
```

### Crear tarea nueva (FASE 1 — planificación)

```bash
curl -s -X POST "$API_URL/api/phases/{PHASE_UUID}/tasks" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "nombre descriptivo",
    "priorityId": "d0b619ef-27e7-42d8-8879-41030a602eed",
    "complexity": "HIGH",
    "category": "development",
    "type": "feature",
    "estimatedHours": 3,
    "assigneeId": "<UUID del ejecutor>"
  }'
```

**Valores válidos:**
- `complexity`: LOW | MEDIUM | HIGH
- `category`: development | design | testing | documentation | review | bugfix | deployment
- `type`: feature | bug | research | documentation | chore

---

## 7. FUENTES DE VERDAD DEL PROYECTO

| Documento | Ruta | Uso |
|-----------|------|-----|
| **SPEC** (v1.9) | `memory-service-project/Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` | Contrato técnico final, 43 decisiones cerradas |
| **Plan sprints** | `memory-service-project/Release2.0/PJM/HO_PJM_PLAN_SPRINTS_MEMORY_SERVICE.md` | 52 tareas, calendario, owners |
| **Addendum integración** | `memory-service-project/Release2.0/01-PM/ADDENDUM_INTEGRACION_MEMORY_SERVICE_v1.1.md` | Contratos con Runtime v1.1 y Prompt Builder v1.3 |
| **TL Review previa** | `memory-service-project/Release2.0/04-TL/TL_REVIEW_SPEC_MEMORY_SERVICE_v1.md` | Observaciones TL-01..TL-N que originaron D-MEM-43 y otras |
| **AR Review** | `memory-service-project/Release2.0/02-AR/AR_REVIEW_SPEC_MEMORY_SERVICE_v1.md` | Arquitectura aprobada |
| **DB Review** | `memory-service-project/Release2.0/03-DB/DB_REVIEW_SPEC_MEMORY_SERVICE_v1.md` | Schema aprobado |
| **Dónde depositar entregables** | `memory-service-project/00-platform/06.Skills/file-structure/SKL-STRUCTURE-01_ubicar-entregable.md` | Rutas correctas por fase |

**Regla:** en caso de conflicto entre documentos → **SPEC v1.9** manda.
**Regla:** Antes de crear cualquier entregable → consultar SKL-STRUCTURE-01.

---

## 8. PROCESO DE CODE REVIEW (resumen)

Cuando una tarea entra en `task_in_review` y yo soy el reviewer:

1. **Leer el ASSIGNMENT original** (lo escribí yo) para recordar qué se pedía.
2. **Ver el PR** en GitHub / branch `feature/[TASK_ID]`.
3. **Verificar entregables obligatorios** (ver `rules_agents.instructions.md §3`):
   - Código funcional (compila + corre localmente)
   - `.LOGIC.md` por cada archivo creado/modificado
   - Development Log en `knowledge/development-log/YYYY-MM-DD_[TASK_ID]_*.md`
   - Commit con `Co-Authored-By` + `Refs: #TASK_ID`
   - Swagger docs (si hay endpoints)
4. **Verificar contrato contra SPEC v1.9** (sección correspondiente).
5. **Decisión:**
   - OK → PATCH status `task_completed` + comentario con razón
   - Cambios menores → PATCH `task_rejected` con lista puntual
   - Bloqueante técnico → Escalar a PM, crear ISSUE si es dato faltante

---

## 9. ESCALACIÓN

| Situación | A quién escalar |
|-----------|-----------------|
| Conflicto entre SPEC y realidad técnica | PM (Martin Rivas) |
| Recurso (agente) no disponible | PJM |
| Falta de datos → crear ISSUE | PM + dejar tarea en `task_on_hold` |
| Cambio de alcance propuesto por ejecutor | PM (no aceptar sin su OK) |
| Integración con Hook Manager VTT (S06) | PM + PJM juntos |

---

## 10. NUNCA HACER COMO TL

- ❌ Implementar código directamente (rol es planear + revisar, no ejecutar)
- ❌ Aprobar tarea sin `.LOGIC.md` o sin Development Log
- ❌ Aceptar mock data — exigir ISSUE + `task_on_hold`
- ❌ Hardcodear UUIDs en ASSIGNMENTS — referenciar este archivo
- ❌ Reabrir decisiones D-MEM-01 a D-MEM-43 (están cerradas)
- ❌ Hacer merge a main (solo Coordinador / PM)

---

**Fuente de verdad operativa:** este archivo.
**Si algo de acá está desactualizado:** avisar a PM y actualizar antes de operar.
