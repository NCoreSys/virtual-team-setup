# SOP-TRK-01 — Proceso de Seguimiento con Features VTT V4 en Memory Service

**Versión:** 2.0  
**Fecha:** 2026-05-12  
**Autor:** TL Memory Service — `92225290-6b6b-4c1f-a940-dcb4262507aa`  
**Aplica a:** TL, SA, PM, BE, QA, DO — cualquier rol que trabaje con Trackable Items en VTT  
**Propósito:** Definir el proceso operativo para usar las features de VTT V4 que reemplazan el control estático en documentos .md y .json, con base en lo que ya existe en el sistema.

---

## 1. Estado actual — Lo que ya existe en VTT

Antes de registrar cualquier cosa nueva, verificar qué ya está. Al 2026-05-12, el sistema tiene **210 Trackable Items** creados en fases anteriores:

| Tipo | Cantidad | Ejemplos de códigos | Estado predominante |
|------|----------|--------------------|--------------------|
| `rf` | 29 | RF-001..RF-032 | `ti_draft` |
| `rf` (aprobados Fase 0) | 20 | DEF-001..DEF-013, DEF-UX-01..08 | `ti_approved` |
| `rnf` | 33 | NFR-PERF-01..06, NFR-SEC-01..07, NFR-AVAIL-01..05 | `ti_draft` |
| `rnf` (aprobados) | 1 | NFR-SEC-07, DEF-003 | `ti_approved` |
| `adr` | 27 | ADR-SA-001..006, ADR-UX-01..21 | `ti_draft` |
| `assumption` | 16 | AS-001..010, HYP-001..006 | `ti_draft` |
| `business_rule` | 23 | BR-001..023 | `ti_draft` |
| `constraint` | 6 | CON-UX-01..06 | `ti_draft` |
| `use_case` | 22 | UC-001..022 | `ti_draft` |
| `user_story` | 33 | US-001..033 | `ti_draft` |
| **TOTAL** | **210** | | |

**Regla crítica:** El TL NO crea items nuevos si ya existen. Primero consulta la lista anterior y usa los IDs existentes para linkear a tareas. Solo crea items nuevos para gaps identificados (por ejemplo, ADRs técnicos de 3B.6 que aún no están en VTT).

**Gap identificado:** Los ADRs técnicos del área de backend (ADR-SA-001..006) están, pero los 43 ADRs de arquitectura de Memory Service (D-MEM-01..43, documentados en 3B.6) probablemente necesitan revisión para confirmar si están todos registrados.

---

## 2. Qué features de VTT V4 aplican para Memory Service

De las 12 features descritas en `MANUAL_FEATURES_VTT_V4.md`, estas son las que el TL y los agentes deben usar activamente:

| Feature | Aplica en MS | Cuándo | Rol principal |
|---------|-------------|--------|---------------|
| **Trackable Items** | ✅ Sí — 210 ya existen | Al asignar tareas: linkear items existentes | TL |
| **Acceptance Criteria** | ✅ Sí | Al crear cada assignment | TL |
| **Fulfillment de CA** | ✅ Sí | Al completar cada tarea | Agente ejecutor |
| **Links entre tareas** | ✅ Sí | Al crear tareas (depends_on, implements) | TL, PJM |
| **Review Gate** | ✅ Sí | Automático al mover a `task_in_review` | Sistema + Agente |
| **Deferred Scope** | ✅ Sí | Para los 8 ❌ de 3B.9.3 | TL |
| **Devlog Entries** | ✅ Sí — ya en uso | Durante ejecución de tarea | Agente ejecutor |
| **Firmas (Stage → Sprint → Release)** | ✅ Sí | Al cerrar stages y sprints | Agente, TL, AR, QA |
| **Hardcode Check** | ✅ Sí | Al completar tareas con código | BE, DO |
| **Document Impacts** | ⚠️ Parcial | Al modificar documentos existentes | Todos |
| **Living Documents** | ❌ No en R1 | Requiere hooks en CI/CD — planificado R2 | — |

---

## 3. El flujo corregido: el TL actúa tarea por tarea

**Corrección v2.0:** El TL no linkea items en batch antes de que existan las tareas. Lo hace cuando genera cada assignment. El proceso es incremental:

```
[PJM crea tarea en VTT] ← desde 3B.9.3_task_breakdown.md
        │
        ▼
[TL genera ASSIGNMENT] ← proceso normal (SKL-TASK-02)
        │
        ▼
[TL lee la tarea y determina qué items trackeable aplican]
  Pregunta: ¿qué RFs, RNFs, ADRs, BRs, UCs implementa esta tarea?
        │
        ▼
[TL linkea los items existentes a la tarea] ← usando IDs de §1
  POST /api/trackable-items/{item_id}/tasks  {"taskId": task_id}
        │
        ▼
[TL define Acceptance Criteria para la tarea] ← derivados de los items linkeados
  POST /api/tasks/{task_id}/criteria
        │
        ▼
[TL agrega links de tarea de dependencia] ← depends_on, blocks
  (ya parte del flujo de creación de tarea)
        │
        ▼
[TL entrega el ASSIGNMENT al agente] ← con lista de items linkeados y CAs
        │
        ▼
[Agente ejecuta, marca CAs, verifica Review Gate]
        │
        ▼
[TL revisa → aprueba → cierra items cuando corresponde]
```

---

## 4. Tabla de mapeo: qué items aplican por tipo de tarea

Esta tabla guía al TL al momento de asignar cada tarea. Para cada tipo de deliverable de Fase 4, los items más comunes a linkear:

### 4.1 Tareas de Backend (subfase 4.3 — API Endpoints, Services, Middlewares)

| Tarea de ejemplo | RFs a linkear | NFRs a linkear | ADRs a linkear | BRs a linkear |
|-----------------|--------------|----------------|----------------|---------------|
| 4.3.1 API Endpoints (POST /memories) | RF-001, RF-002 | NFR-PERF-01, NFR-SEC-01 | ADR-SA-001, ADR-SA-006 | BR-001, BR-002 |
| 4.3.1 API Endpoints (GET /context) | RF-003, RF-004 | NFR-PERF-01 (<500ms), NFR-PERF-02 | ADR-SA-003 | BR-003 |
| 4.3.7 Auth Middleware | — | NFR-SEC-01, NFR-SEC-02, NFR-SEC-03 | ADR-SA-004 | BR-015 |
| 4.3.2 Services Layer | RF-001..RF-010 (según service) | NFR-PERF-01..03, NFR-SCAL-01 | ADR-SA-001..006 | BR-001..015 |

**Fuente para determinar qué RFs cubre cada endpoint:** `phases/03-design/deliverables/api-design/3B.4.2_endpoints_list.md`

### 4.2 Tareas de Base de Datos (subfase 4.2)

| Tarea | Items a linkear |
|-------|----------------|
| 4.2.1 Schema Migration | NFR-PERF-04 (índices), ADR-SA-002 (PostgreSQL), BR-001..010 |
| 4.2.5 Performance Indexes | NFR-PERF-01, NFR-PERF-04, NFR-SCAL-01 |

### 4.3 Tareas de Testing (Fase 5)

| Tarea | Items a linkear |
|-------|----------------|
| 5.7.2 Load Tests | NFR-PERF-01 (<500ms) ← este es el que CIERRA el NFR |
| 5.1.x Unit Tests | Los RFs específicos del módulo testeado |
| 5.10.x Security Tests | NFR-SEC-01..06 |

### 4.4 Tareas de Deploy (Fase 6)

| Tarea | Items a linkear |
|-------|----------------|
| 6.3.1 Staging Deploy | NFR-AVAIL-01, NFR-AVAIL-02 |
| 6.5.1 Production Deploy | NFR-AVAIL-01..05, NFR-SCAL-01..02 |

### 4.5 User Stories y Use Cases

Los US-001..033 y UC-001..022 se linkean principalmente a tareas de Frontend (subfase 4.4) y a tareas de E2E Testing (5.6.x). El TL los incluye en el assignment del agente FE para que sepa exactamente qué flujo de usuario implementa.

---

## 5. Acceptance Criteria: derivados de los Trackable Items linkeados

Cuando el TL linkea items a una tarea, los CA de esa tarea se derivan directamente de esos items:

**Patrón:** Un RF linkeado → al menos un CA funcional que verifica su implementación.

```
RF-001: "El sistema permite registrar memorias con contenido, agentId y sessionId"
  → CA-1: El endpoint POST /memories acepta {content, agentId, sessionId} (functional, required: true)
  → CA-2: Retorna 400 si content está vacío (functional, required: true)
  → CA-3: Memory queda persistida en BD con embedding generado (technical, required: true)

NFR-PERF-01: "GET /context responde en <500ms P95"
  → CA en tarea 5.7.2: P95 < 500ms con 100 concurrent requests en staging (performance, required: true)

ADR-SA-004: "Usar X-Service-Key para autenticación"
  → CA en tarea 4.3.7: Requests sin X-Service-Key retornan 401 (security, required: true)
  → CA en tarea 4.3.7: Service Key inválida retorna 401 (security, required: true)

BR-015: "Solo agentes autenticados pueden acceder a /api/*"
  → CA en tarea 4.3.7: Middleware bloquea todos los endpoints sin header válido (functional, required: true)
```

### 5.1 Cómo crear el CA en VTT

```bash
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/criteria" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"title\": \"El endpoint POST /memories acepta {content, agentId, sessionId}\",
    \"description\": \"Verificar con test de integración. Ver RF-001.\",
    \"type\": \"functional\",
    \"required\": true
  }"
```

**Tipos válidos:** `functional` | `technical` | `security` | `performance` | `ux`

### 5.2 CA por nivel

| Nivel | Qué contiene | Quién lo define |
|-------|-------------|-----------------|
| Proyecto | Estándares globales: LOGIC.md, Swagger, no console.log, AppError | PM/TL al inicio del proyecto |
| Fase 4 | Compilación TS strict, unit tests >80%, devlog por decisión técnica | TL al arrancar Fase 4 |
| Fase 5 | Tests en CI/CD, evidencia en staging, bugs como Trackable Items | TL al arrancar Fase 5 |
| Fase 6 | Smoke tests post-deploy, monitoreo activo, rollback probado | TL al arrancar Fase 6 |
| Tarea | CA específicos derivados de los Trackable Items linkeados | TL al generar assignment |

---

## 6. Fulfillment: el agente reporta evidencia

Al completar la implementación, el agente marca cada CA:

```bash
# CA cumplido:
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/criteria/$CA_ID/fulfill" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"status\": \"met\",
    \"notes\": \"Verificado en test/integration/memories.spec.ts:45. PR #67. Response time P95=380ms en staging con Artillery.\"
  }"

# CA no cumplido:
curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/criteria/$CA_ID/fulfill" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"status\": \"not_met\",
    \"notes\": \"P95 = 620ms > 500ms. Requiere optimización de query de vector search. Devlog entry RISK-001 creado.\"
  }"
```

**Regla de evidencia:** La nota de fulfillment debe incluir AL MENOS UNO de: número de PR, nombre de archivo de test, número de línea, output de comando de prueba.

---

## 7. Review Gate: el sistema valida antes de pasar a revisión

Cuando el agente intenta mover la tarea a `task_in_review`, el Review Gate verifica automáticamente:

1. ¿Hay devlog entries con severity `critical` o `high` sin resolver? → 🔴 BLOQUEADO
2. ¿Hay CA `required: true` sin marcar? → 🔴 BLOQUEADO

```bash
# Verificar antes de mover:
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/review-gate" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

Si hay 🔴, el agente debe:
- Para devlog entry blocker/critical: resolver el problema técnico, luego marcar el entry como resuelto
- Para CA no marcado: implementar lo que falta o marcar `not_met` con justificación

---

## 8. Hardcode Check: aplica a todas las tareas con código (Fase 4, 6)

Antes de mover cualquier tarea de BE/DO a `task_in_review`, el agente ejecuta el Hardcode Check:

**Qué detecta:**

| Patrón | Severidad | Ejemplo en Memory Service |
|--------|-----------|--------------------------|
| UUID hardcodeado | HIGH | `agentId = "92225290-..."` en código |
| URL hardcodeada | CRITICAL | `fetch("http://77.42.88.106:3000")` en código |
| Service Key inline | CRITICAL | `serviceKey = "hBCGEKm41..."` |
| Timeout magic number | MEDIUM | `setTimeout(fn, 450)` sin constante nombrada |
| Status hardcodeado | HIGH | `status: "active"` en vez de usar enum |

**Proceso:**
1. Tarea → Hardcode Check → pegar fragmento de código relevante → Ejecutar análisis
2. Por cada finding: Corregir (si válido) / Marcar falso positivo con justificación / Crear bug trackeable
3. Findings CRITICAL o HIGH no resueltos → bloquean el Review Gate

---

## 9. Firmas: cierre formal de stages, sprints y releases

Las firmas en cascada son el mecanismo de cierre formal que reemplaza el "marcar como completado en el .md".

### 9.1 Firma de Stage (cada agente firma sus propias tareas)

**Cuándo:** Cuando el agente tiene TODAS sus tareas del stage en `task_completed`

**Pre-condiciones:**
- Todas las tareas en `completed` ✅
- Todos los CA marcados (met/not_met) ✅
- No hay devlog entries critical/high pendientes ✅
- Hardcode check ejecutado (si aplica) ✅

### 9.2 Firma de Sprint (TL, AR, QA)

**Cuándo:** Cuando TODOS los stages del sprint están firmados

**Quiénes firman:**
- TL: obligatorio (validación técnica general)
- AR: obligatorio (code review, consistencia arquitectónica)
- QA: obligatorio (tests passing, cobertura)
- DL: solo si hubo tareas FE/UX en el sprint

**Pre-condiciones adicionales:**
- Integration tests pasaron ✅
- No hay bugs blocker abiertos ✅
- Documentación actualizada ✅

### 9.3 Firma de Release (PM + TL)

**Cuándo:** Cuando todos los sprints del release están firmados

**Implica:** El PM firma que el release cumple con los criterios de aceptación a nivel de producto.

### 9.4 Relación entre Firmas y Trackable Items

La firma de sprint es también el momento para hacer el **cierre masivo de Trackable Items**:

```
Sprint firmado → TL revisa dashboard de TIs
                → Identifica RFs con todas sus tareas en task_approved
                → Cierra esos RFs (ti_approved)
                → Idem para RNFs con evidencia de testing
```

```bash
# Cerrar un RF:
curl -s -X PATCH "$VTT_BASE_URL/api/trackable-items/$ITEM_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"statusCode\": \"ti_approved\"}"
```

---

## 10. Deferred Scope: los 8 ❌ de 3B.9.3

Los deliverables marcados ❌ en la tabla maestra de estimaciones deben registrarse como Deferred Scope para que queden visibles en el backlog de R2:

| Deliverable ❌ | Razón | Defer a |
|----------------|-------|---------|
| 4.2.7 Stored Procedures | Sin lógica DB compleja en R1 — ADR-SA-002 | R2 |
| 4.2.8 Views | Sin reporting queries en R1 — ADR-SA-002 | R2 |
| 4.5.4 OAuth Integrations | X-Service-Key en R1 — 3B.4.6 | R2 |
| 6.1.5 Load Balancer | Un servidor en R1 — ADR-SA-005 | R2 |
| 6.1.7 MinIO Object Storage | Filesystem bind mount en R1 — ADR-SA-003 | R2 |
| 7.2.2 Ticket/Issue System | Solo logs en R1 — ADR-SA-006 | R2 |
| 7.4.3 A/B Testing | Sin experimentación en R1 | R2 |
| 7.6.3 Auto-scaling | Hetzner fijo en R1 — ADR-SA-005 | R2 |

```python
TL_ID = "92225290-6b6b-4c1f-a940-dcb4262507aa"
R1_RELEASE_ID = "92664a70-8812-4468-abc5-6b3f63d7ef54"

# Para cada ❌ que tenga un Trackable Item en VTT:
# Paso 1: aprobar
api_call(f"{BASE_URL}/api/trackable-items/{item_id}", {"statusCode": "ti_approved"}, method="PATCH")

# Paso 2: deferir
api_call(f"{BASE_URL}/api/trackable-items/{item_id}/defer", {
    "targetType": "release",
    "targetReleaseId": R1_RELEASE_ID,
    "reason": "[Deferred to R2] No aplica en R1. Ver ADR correspondiente.",
    "deferredBy": TL_ID
})
```

---

## 11. Document Impacts: qué documentos afecta cada tarea

Al completar cada tarea, el agente registra qué documentos modificó. Esto mantiene la trazabilidad entre código y documentación:

```bash
POST /api/tasks/{task_id}/impacts
{
  "documentId": "...",   # ID del documento en VTT si es Living Document
  "type": "added|modified|removed|referenced",
  "description": "Agregué schema de memories.ts a la guía de BD"
}
```

**Cuándo aplica en Memory Service:**
- BE modifica un endpoint → impacta OpenAPI spec
- DB modifica schema → impacta ERD y guía de migraciones
- QA genera reporte de load test → impacta NFR-PERF-01 evidencia

---

## 12. Proceso resumido: lo que hace el TL con cada assignment

```
Al generar un ASSIGNMENT para tarea MS-XXX:

1. LEER 3B.4.2 (endpoints) para identificar qué RFs cubre esta tarea
2. CONSULTAR lista de 210 TIs existentes → identificar los que aplican
3. LINKEAR items existentes a la tarea (NO crear nuevos si ya existen)
   → POST /api/trackable-items/{item_id}/tasks {"taskId": "MS-XXX"}
4. DEFINIR CAs derivados de los items linkeados
   → 1 CA por cada RF/NFR/BR importante
5. INCLUIR en el ASSIGNMENT:
   → Sección "Trackable Items linkeados: RF-001, NFR-PERF-01, ADR-SA-004"
   → Sección "Acceptance Criteria: [lista de CAs con evidencia esperada]"
   → Instrucción: "Al completar, marcar cada CA con evidencia concreta"
   → Instrucción: "Verificar Review Gate antes de mover a task_in_review"
   → Instrucción: "Ejecutar Hardcode Check si es tarea de código"

Al revisar la tarea (task_in_review):

6. VERIFICAR fulfillment: evidencia suficiente en cada CA
7. APROBAR tarea si CA cumplidos
8. REVISAR si algún RF tiene ahora todas sus tareas aprobadas → cerrar RF
9. Al cierre de sprint: firmar sprint + dashboard de TIs → cerrar los completados
```

---

## 13. Referencia rápida de API calls

```python
BASE_URL = "http://77.42.88.106:3000"
PROJECT_ID = "d0fc276d-e764-4a83-96e9-d65f086ed803"
R1_RELEASE_ID = "92664a70-8812-4468-abc5-6b3f63d7ef54"
TL_ID = "92225290-6b6b-4c1f-a940-dcb4262507aa"

# Listar TIs existentes (para no duplicar)
GET /api/projects/{PROJECT_ID}/trackable-items?limit=200

# Linkear TI a tarea
POST /api/trackable-items/{item_id}/tasks  {"taskId": "MS-XXX"}

# Crear CA en tarea
POST /api/tasks/{task_id}/criteria
{"title": "...", "type": "functional", "required": true}

# Reportar fulfillment
POST /api/tasks/{task_id}/criteria/{ca_id}/fulfill
{"status": "met|not_met", "notes": "Evidencia concreta..."}

# Verificar Review Gate
GET /api/tasks/{task_id}/review-gate

# Dashboard TIs pendientes
GET /api/projects/{PROJECT_ID}/trackable-items?status=pending&type=rf

# Cerrar TI
PATCH /api/trackable-items/{item_id}  {"statusCode": "ti_approved"}

# Deferir TI a R2
POST /api/trackable-items/{item_id}/defer
{"targetType": "release", "targetReleaseId": "...", "reason": "...", "deferredBy": "..."}
```

---

**Documento:** SOP-TRK-01_trackable_items_workflow.md | **Versión:** 2.0 | **Fecha:** 2026-05-12  
**Relacionado con:** SOP-EST-01, SOP-VEL-01, MANUAL_TRACKABLE_ITEMS_VTT.md, MANUAL_FEATURES_VTT_V4.md  
**Correcciones v2.0:** (1) Incorpora inventario real de 210 TIs existentes. (2) Flujo tarea-por-tarea al generar assignment, no batch. (3) Agrega Hardcode Check, Firmas en cascada y Document Impacts.
