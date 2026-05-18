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

**Regla:** en caso de conflicto entre documentos → **SPEC v1.9** manda.

---

## 8. PROCESO DE CODE REVIEW (resumen)

> **Importante:** el code review formal lo ejecuta el **TL Reviewer** (`OPERATIVO_TL_REVIEWER.md v3.2`) siguiendo `PROCESO_CIERRE_TAREA_v2.md` (16 pasos). Si tú estás haciendo el review, sigue ese proceso.
>
> Resumen del flujo (FASE C de PROCESO_ASIGNACION_TAREAS_v3):

Cuando una tarea entra en `task_in_review`:

1. **Verificación (Pasos 8-11)** — Review Gate + CAs + attachments + PRs
2. **Aplicar modelo dinámico (Paso 12 — SKL-DYNAMIC-MODEL-01):**
   - Crear TIs detectados por el agente (`tech_debt` + `[DEFER R2]` marker)
   - Vincular TIs nuevos a la tarea (`related_to`)
   - Agregar evidencias a TIs vinculadas con marker `[TASK:MS-XXX] [SPRINT:SX]`
   - Resolver devlog entries con `resolution` requerido
3. **APR-TL comment (Paso 13)** — incluir sección "Acciones aplicadas al cerrar (modelo dinámico)"
4. **PATCH status → task_completed (Paso 14)**
5. **Generar manifest AL FINAL (Paso 15 — SKL-MANIFEST-01)** con bloque `delivery.dynamic_model_actions`
6. **Validación final (Paso 16)** — devlog resolved, evidencias con marker, manifest subido

**Decisiones posibles:**
- OK → seguir flujo (Pasos 12-16) → notificar PM para aprobación terminal
- Cambios menores → PATCH `task_rejected` con feedback puntual
- Bloqueante técnico → escalar a PM, crear ISSUE si es dato faltante

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

---

## Entregables OBLIGATORIOS antes de mover a in_review

Antes de `PATCH /status → in_review` debes haber subido y registrado:

1. **Devlog entries** registrados (decisiones, blockers, observaciones, tech_debt) — quedan en `pending`; el TL Reviewer los pondrá `resolved` al cerrar
2. **CAs reportados** con `PATCH /criteria/:cid` `{status:"met", evidence:"..."}` (todos los criteriaIds del assignment)
3. **TrackableItems heredados** vinculados según assignment (implements/related_to)
4. **Review Gate verde** (`GET /review-gate` → `canProceedToReview: true`)
5. **DevLog** subido como attachment (`fileType=devlog`)
6. **Code Logic** subido como attachment (`fileType=code_logic`) [o placeholder N/A si la tarea no produce código TS]
7. **Comentario de reporte (SKL-REPORT-01)** con secciones del modelo dinámico:
   - Tech debts detectados (TL los creará como TIs `[DEFER R2]`)
   - Items detectados para trackeo (TL revisar)
   - TrackableItems creados o vinculados (con UUIDs reales)
   - Devlog entries registrados (TL los marcará `resolved`)
   - PRs y commits (URLs específicas, no URL base)

> **NO generes manifest desde aquí.** El manifest lo genera el TL Reviewer al cerrar (Paso 15 — `SKL-MANIFEST-01`), después de attachments + status + dynamic_model.

### Verificar Review Gate (BLOQUEANTE)
```bash
curl -s "http://77.42.88.106:3000/api/tasks/MS-XXX/review-gate"   -H "Authorization: Bearer $TOKEN"
# Esperado: { "data": { "canProceedToReview": true } }
# Si false → resolver devlog entries critical/high pendientes primero
```

### Resolver devlog entry pendiente
```bash
curl -s -X PATCH "http://77.42.88.106:3000/api/tasks/MS-XXX/devlog/{entryId}/status"   -H "Authorization: Bearer $TOKEN"   -H "Content-Type: application/json"   -d '{"status":"resolved","resolution":"Cómo se resolvió"}'
```

### Reportar cumplimiento de CA
```bash
curl -s -X PATCH "http://77.42.88.106:3000/api/tasks/MS-XXX/criteria/{criteriaId}" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"status":"met","evidence":"PR #N o evidencia concreta"}'
```
> **Gotcha:** El endpoint real es `PATCH /criteria/:cid`. El `POST /fulfill` documentado en templates antiguos devuelve 404.

### Endpoints validados (Modelo Dinámico V4 + descubrimientos 2026-05-13)

| Endpoint | Uso | Notas |
|---|---|---|
| `POST /api/tasks/:taskId/devlog-entries` | Registrar entry | Plural en POST |
| `GET /api/tasks/:taskId/devlog` | Listar entries | Singular en GET |
| `PATCH /api/tasks/:taskId/devlog/:eid/status` | Resolver entry | `resolution` REQUERIDO si status=resolved/wont_fix |
| `GET /api/tasks/:taskId/review-gate` | Verificar gate | canProceedToReview boolean |
| `PATCH /api/tasks/:taskId/criteria/:cid` | Cumplir CA | NO `/fulfill` |
| `GET /api/tasks/:taskId/criteria` | Listar CAs | criteriaTypeCode (no `type`) |
| `POST /api/projects/:projectId/trackable-items` | Crear TI scoped | Software acepta solo `tech_debt` para improvements |
| `POST /api/trackable-items/:tiId/tasks` | Vincular TI a tarea | linkType: implements/related_to |
| `POST /api/trackable-items/:tiId/evidence` | Agregar evidencia | singular `/evidence`, enum: document/link/test_result/screenshot |
| `GET /api/trackable-items/:tiId/evidence` | Listar evidencias | |
| `GET /api/projects/:projectId/trackable-items?statusCode=&typeCode=` | Listar TIs | Filtros por query param |

### Gaps de feature en VTT (workarounds aplicados)

Ver `knowledge/platform-feedback/VTT_PLATFORM_GAPS_2026-05-13.md`:

| Gap | Workaround |
|---|---|
| `POST /trackable-items/:id/defer` NO existe | Marker `[DEFER R2]` en title+description |
| Status `ti_deferred` NO existe | TIs viven en `ti_draft` con marker |
| `typeCode=process_improvement` NO válido software | Usar `tech_debt` + `[PROCESS]` marker |
| `DELETE /trackable-item-evidences/:id` NO existe | Cuidar formato al crear; no se pueden corregir |
| Campo `taskId` en evidence NO existe | Marker `[TASK:MS-XXX] [SPRINT:SX]` en description |
| `GET /tasks/:id/trackable-items` NO existe | Iterar TIs del proyecto |

