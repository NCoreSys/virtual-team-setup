# SETUP: Sprint S3 — Features BE + FE Start

**Documento:** SETUP_S3.md
**Versión:** 1.0
**De:** PJM-Agent
**Para:** TL (Tech Lead)
**Fecha:** 2026-05-12
**Sprint:** S3 — Features BE + FE Start
**Propósito:** Instrucciones para crear estructura y tareas del Sprint S3 en VTT

---

## 0. RESUMEN EJECUTIVO

Al completar este setup:

- ✅ Sprint S3 creado en VTT (vinculado a Release R1)
- ✅ 4 Deliveries creados y vinculados a Sprint S3
- ✅ 18 tareas creadas y asociadas (13 deliverables + 1 TL + 4 validación/cierre)
- ✅ Dependencias configuradas (cross-sprint con S2 + intra-sprint)

**Primer sprint con Frontend.** BE expone endpoints, FE arranca foundation.

**Tiempo estimado:** 1.5 horas
**Prerrequisito:** Sprint S2 completado (CIERRE-S2 = task_completed ✅)

---

## 1. PRERREQUISITOS

| # | Prerrequisito | Estado |
|---|---------------|--------|
| 1 | Sprint S2 cerrado (APR-S2 completado) | ⬜ |
| 2 | RELEASE_ID y CONTEXTO_S2.md disponibles | ⬜ |
| 3 | IDs de tareas S2 para dependencias cross-sprint | ⬜ |
| 4 | HANDOFF_TL_S3.md y CLOSURE_S3.md disponibles | ⬜ |

---

## 2. CONSTANTES DE SESIÓN

```python
import urllib.request, json, time, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://77.42.88.106:3000"
PROJECT_ID = "d0fc276d-e764-4a83-96e9-d65f086ed803"
PHASE_DEV = "c5f9f305-de20-4d09-b939-39a84654362c"

# Auth
req = urllib.request.Request(
    f'{BASE_URL}/api/auth/service-token',
    data=json.dumps({
        'userId': '92225290-6b6b-4c1f-a940-dcb4262507aa',
        'serviceKey': 'hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d'
    }).encode(),
    headers={'Content-Type': 'application/json'}, method='POST')
TOKEN = json.loads(urllib.request.urlopen(req).read())['data']['token']
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

# Agentes
TL = "92225290-6b6b-4c1f-a940-dcb4262507aa"
BE = "ebbe3cee-abed-4b3b-860d-0a81f632b08a"
FE = "d23c9cd9-a156-433b-8900-94add5488eec"
AR = "e9403c25-c1f8-4b64-b2ef-f447d53115e2"
DL = "b3a09269-cded-468c-a475-15a48f203cb0"
PM_ID = "350831b2-e1ae-4dbe-b2eb-7e023ec2e103"

PRI_HIGH = "1a617554-6319-4c56-826f-8ef49a0ff9cc"
PRI_MED  = "d0b619ef-27e7-42d8-8879-41030a602eed"

# === RECUPERAR DE CONTEXTO_S2 ===
RELEASE_ID = "________________________________"
T_4_3_2_S2  = "________________________________"  # [4.3.2] Services (S2)
T_4_3_7_S2  = "________________________________"  # [4.3.7] Middlewares (S2)
T_4_2_5_S2  = "________________________________"  # [4.2.5] Indexes (S2)
CIERRE_S2   = "________________________________"
```

---

## 3. PASO 1: CREAR SPRINT S3

```python
body = {
    "number": 3,
    "name": "S3 — Features BE + FE Start",
    "goal": "POST /import e2e OK, JSONL procesado, estado IMPORTED en BD, FE foundation desplegada",
    "startDate": "2026-06-29T00:00:00Z",
    "endDate": "2026-07-12T00:00:00Z"
}
req = urllib.request.Request(
    f'{BASE_URL}/api/releases/{RELEASE_ID}/sprints',
    data=json.dumps(body).encode(), headers=HEADERS, method='POST')
SPRINT_S3_ID = json.loads(urllib.request.urlopen(req).read())['data']['id']
print(f"SPRINT_S3_ID: {SPRINT_S3_ID}")
```

**Registrar:**
```
SPRINT_S3_ID: ________________________________
```

---

## 4. PASO 2: CREAR TAREA SETUP

```python
body = {
    "title": "SETUP-S3: Setup Sprint 3 — Features BE + FE Start",
    "description": "Configuración del Sprint S3. Primer sprint con FE.",
    "assigneeId": TL, "estimatedHours": 1, "priorityId": PRI_MED,
    "complexity": "LOW", "category": "documentation"
}
req = urllib.request.Request(f'{BASE_URL}/api/phases/{PHASE_DEV}/tasks',
    data=json.dumps(body).encode(), headers=HEADERS, method='POST')
SETUP_S3 = json.loads(urllib.request.urlopen(req).read())['data']['id']
print(f"SETUP_S3: {SETUP_S3}")
```

**Registrar:**
```
SETUP_S3: ________________________________
```

---

## 5. PASO 3: CREAR 4 DELIVERIES

```python
def create_delivery(name, order):
    body = {"phaseId": PHASE_DEV, "name": name, "order": order, "createdBy": TL}
    req = urllib.request.Request(f'{BASE_URL}/api/deliveries',
        data=json.dumps(body).encode(), headers=HEADERS, method='POST')
    return json.loads(urllib.request.urlopen(req).read())['data']['id']

DEL_BE_S3  = create_delivery("BE-S3: Endpoints + Integrations + Worker", 1)
DEL_FE_S3  = create_delivery("FE-S3: Foundation (Components + Hooks + State)", 2)
DEL_TL_S3  = create_delivery("TL-S3: Reviews + SLA Check", 3)
DEL_REV_S3 = create_delivery("REV-S3: Validación + Cierre", 4)

print(f"DEL_BE_S3:  {DEL_BE_S3}")
print(f"DEL_FE_S3:  {DEL_FE_S3}")
print(f"DEL_TL_S3:  {DEL_TL_S3}")
print(f"DEL_REV_S3: {DEL_REV_S3}")
```

**Registrar:**
```
DEL_BE_S3:  ________________________________
DEL_FE_S3:  ________________________________
DEL_TL_S3:  ________________________________
DEL_REV_S3: ________________________________
```

---

## 6. PASO 4: VINCULAR DELIVERIES AL SPRINT S3

```python
for d in [DEL_BE_S3, DEL_FE_S3, DEL_TL_S3, DEL_REV_S3]:
    body = {"sprintId": SPRINT_S3_ID}
    req = urllib.request.Request(f'{BASE_URL}/api/deliveries/{d}',
        data=json.dumps(body).encode(), headers=HEADERS, method='PATCH')
    urllib.request.urlopen(req)
    time.sleep(0.05)
print("Deliveries vinculados a Sprint S3 ✅")
```

---

## 7. PASO 5: CREAR TAREAS BE (Endpoints + Integrations + Worker)

```python
tasks_be = [
    ("4.3.1", "API Endpoints — 11 endpoints", 13, "HIGH",
     "4.3.2 Services (S2), 4.3.7 Middlewares (S2), 4.2.5 Indexes (S2)\nDetalle: 11 endpoints de 3B.4.2. GET /context con SLA <500ms via Promise.race"),
    ("4.3.6", "Workers — Cleanup Job", 8, "HIGH",
     "4.3.2 Services (S2)\nDetalle: node-cron cada 5min, retry ≤3, PENDING/PROCESSING stuck >10min → retry → ERROR"),
    ("4.5.1", "Integration Code — 3 integraciones", 8, "HIGH",
     "4.3.2 Services (S2)\nDetalle: Runtime v1.1 → POST /import, PB v1.3 → GET /context, Hook Manager → POST /import-review"),
    ("4.5.2", "API Clients (consumidores)", 5, "MEDIUM",
     "4.5.1\nDetalle: Clientes HTTP para consumidores externos de Memory Service"),
    ("4.5.3", "Webhooks — POST /api/import-review", 5, "MEDIUM",
     "4.5.1\nDetalle: Webhook para VTT_CHANNEL vía Hook Manager"),
    ("4.5.5", "Third-party SDKs — ioredis, node-cron, multer", 3, "LOW",
     "SETUP-S3\nDetalle: Dependencias npm: ioredis 5.x, node-cron, multer para file upload"),
]

be_ids = {}
for cat_id, name, hours, complexity, deps in tasks_be:
    pri = PRI_HIGH if complexity in ("HIGH", "VERY HIGH") else PRI_MED
    body = {
        "title": f"[{cat_id}] {name}",
        "description": f"Deliverable: {name} (ID catálogo: {cat_id})\nSprint: S3\nRol: BE\nEstimación: {hours}h / {hours} SP\nComplejidad: {complexity}\nDependencias: {deps}",
        "assigneeId": BE, "estimatedHours": hours, "priorityId": pri,
        "complexity": "HIGH" if complexity == "VERY HIGH" else complexity,
        "category": "development"
    }
    req = urllib.request.Request(f'{BASE_URL}/api/phases/{PHASE_DEV}/tasks',
        data=json.dumps(body).encode(), headers=HEADERS, method='POST')
    be_ids[cat_id] = json.loads(urllib.request.urlopen(req).read())['data']['id']
    print(f"T_{cat_id}: {be_ids[cat_id]}")
    time.sleep(0.1)

T_4_3_1 = be_ids["4.3.1"]
T_4_3_6 = be_ids["4.3.6"]
T_4_5_1 = be_ids["4.5.1"]
T_4_5_2 = be_ids["4.5.2"]
T_4_5_3 = be_ids["4.5.3"]
T_4_5_5 = be_ids["4.5.5"]
```

**Registrar:**
```
T_4_3_1: ________________________________
T_4_3_6: ________________________________
T_4_5_1: ________________________________
T_4_5_2: ________________________________
T_4_5_3: ________________________________
T_4_5_5: ________________________________
```

---

## 8. PASO 6: CREAR TAREAS FE (Foundation)

```python
tasks_fe = [
    ("4.4.1", "Components — shared + layout shell + nav", 8, "HIGH",
     "Design Handoff (fases 5-6 completadas ✅)\nDetalle: Componentes base: AppShell, Sidebar, Header, Card, Table, Badge, Button, StatusIndicator"),
    ("4.4.3", "Layouts", 3, "LOW",
     "4.4.1\nDetalle: MainLayout con sidebar + content area, AuthLayout (si aplica)"),
    ("4.4.4", "Hooks — useConversations, useContext, useCosts", 5, "MEDIUM",
     "4.4.6\nDetalle: Custom hooks para data fetching con estados loading/error/data"),
    ("4.4.5", "State Management", 5, "MEDIUM",
     "4.4.1\nDetalle: React Context para global state (no Redux en R1). Contexts: AuthContext, FilterContext"),
    ("4.4.6", "API Client FE", 5, "MEDIUM",
     "4.4.7\nDetalle: fetch wrapper con X-Service-Key header, error handling, base URL config"),
    ("4.4.7", "Types/Interfaces — @NCoreSys/api-types", 3, "LOW",
     "SETUP-S3\nDetalle: Shared types package entre backend y frontend"),
    ("4.4.8", "Styles — Tailwind setup", 3, "LOW",
     "SETUP-S3\nDetalle: Tailwind CSS 3.x config con design tokens del design system"),
]

fe_ids = {}
for cat_id, name, hours, complexity, deps in tasks_fe:
    pri = PRI_HIGH if complexity in ("HIGH", "VERY HIGH") else PRI_MED
    body = {
        "title": f"[{cat_id}] {name}",
        "description": f"Deliverable: {name} (ID catálogo: {cat_id})\nSprint: S3\nRol: FE\nEstimación: {hours}h / {hours} SP\nComplejidad: {complexity}\nDependencias: {deps}",
        "assigneeId": FE, "estimatedHours": hours, "priorityId": pri,
        "complexity": complexity, "category": "development"
    }
    req = urllib.request.Request(f'{BASE_URL}/api/phases/{PHASE_DEV}/tasks',
        data=json.dumps(body).encode(), headers=HEADERS, method='POST')
    fe_ids[cat_id] = json.loads(urllib.request.urlopen(req).read())['data']['id']
    print(f"T_{cat_id}: {fe_ids[cat_id]}")
    time.sleep(0.1)

T_4_4_1 = fe_ids["4.4.1"]
T_4_4_3 = fe_ids["4.4.3"]
T_4_4_4 = fe_ids["4.4.4"]
T_4_4_5 = fe_ids["4.4.5"]
T_4_4_6 = fe_ids["4.4.6"]
T_4_4_7 = fe_ids["4.4.7"]
T_4_4_8 = fe_ids["4.4.8"]
```

**Registrar:**
```
T_4_4_1: ________________________________
T_4_4_3: ________________________________
T_4_4_4: ________________________________
T_4_4_5: ________________________________
T_4_4_6: ________________________________
T_4_4_7: ________________________________
T_4_4_8: ________________________________
```

---

## 9. PASO 7: CREAR TAREAS TL + VALIDACIÓN + CIERRE + APR

```python
# TL-S3-REV
body = {
    "title": "TL-S3-REV: Reviews + SLA Check Preliminar Sprint S3",
    "description": "Revisar PRs BE y FE. Verificar GET /context <500ms en dev local. Primer check de SLA.",
    "assigneeId": TL, "estimatedHours": 3, "priorityId": PRI_MED,
    "complexity": "MEDIUM", "category": "review"
}
req = urllib.request.Request(f'{BASE_URL}/api/phases/{PHASE_DEV}/tasks',
    data=json.dumps(body).encode(), headers=HEADERS, method='POST')
TL_S3_REV = json.loads(urllib.request.urlopen(req).read())['data']['id']
print(f"TL_S3_REV: {TL_S3_REV}")
time.sleep(0.1)

# AR-S3
body = {
    "title": "AR-S3: Integration Audit Sprint S3",
    "description": "Auditar: 11 endpoints vs 3B.4.2, integrations vs 3B.1.6, FE foundation vs 3B.2.1.",
    "assigneeId": AR, "estimatedHours": 3, "priorityId": PRI_MED,
    "complexity": "MEDIUM", "category": "review"
}
req = urllib.request.Request(f'{BASE_URL}/api/phases/{PHASE_DEV}/tasks',
    data=json.dumps(body).encode(), headers=HEADERS, method='POST')
AR_S3 = json.loads(urllib.request.urlopen(req).read())['data']['id']
print(f"AR_S3: {AR_S3}")
time.sleep(0.1)

# DL-S3-REV (FE foundation review)
body = {
    "title": "DL-S3-REV: Visual Review FE Foundation Sprint S3",
    "description": "DL revisa componentes base, Tailwind tokens, layout shell. Foundation visual — no páginas.",
    "assigneeId": DL, "estimatedHours": 2, "priorityId": PRI_MED,
    "complexity": "LOW", "category": "review"
}
req = urllib.request.Request(f'{BASE_URL}/api/phases/{PHASE_DEV}/tasks',
    data=json.dumps(body).encode(), headers=HEADERS, method='POST')
DL_S3_REV = json.loads(urllib.request.urlopen(req).read())['data']['id']
print(f"DL_S3_REV: {DL_S3_REV}")
time.sleep(0.1)

# CIERRE-S3
body = {
    "title": "CIERRE-S3: Cierre Sprint 3 — Features BE + FE Start",
    "description": "Cierre formal S3. Requiere firmas TL + AR + DL. Usar CLOSURE_S3.md.",
    "assigneeId": TL, "estimatedHours": 2, "priorityId": PRI_HIGH,
    "complexity": "MEDIUM", "category": "review"
}
req = urllib.request.Request(f'{BASE_URL}/api/phases/{PHASE_DEV}/tasks',
    data=json.dumps(body).encode(), headers=HEADERS, method='POST')
CIERRE_S3 = json.loads(urllib.request.urlopen(req).read())['data']['id']
print(f"CIERRE_S3: {CIERRE_S3}")
time.sleep(0.1)

# APR-S3
body = {
    "title": "APR-S3: Aprobación final Sprint S3",
    "description": "Aprobación PM tras firmas TL + AR + DL y verificación M3.",
    "assigneeId": PM_ID, "estimatedHours": 1, "priorityId": PRI_HIGH,
    "complexity": "LOW", "category": "review"
}
req = urllib.request.Request(f'{BASE_URL}/api/phases/{PHASE_DEV}/tasks',
    data=json.dumps(body).encode(), headers=HEADERS, method='POST')
APR_S3 = json.loads(urllib.request.urlopen(req).read())['data']['id']
print(f"APR_S3: {APR_S3}")
```

**Registrar:**
```
TL_S3_REV: ________________________________
AR_S3:     ________________________________
DL_S3_REV: ________________________________
CIERRE_S3: ________________________________
APR_S3:    ________________________________
```

---

## 10. PASO 8: ASOCIAR TAREAS A DELIVERIES

```python
def assign_task_to_delivery(delivery_id, task_id):
    body = {"assignedBy": TL}
    req = urllib.request.Request(
        f'{BASE_URL}/api/deliveries/{delivery_id}/tasks/{task_id}',
        data=json.dumps(body).encode(), headers=HEADERS, method='POST')
    urllib.request.urlopen(req)
    time.sleep(0.05)

# BE (6 tareas) → DEL_BE_S3
for t in [T_4_3_1, T_4_3_6, T_4_5_1, T_4_5_2, T_4_5_3, T_4_5_5]:
    assign_task_to_delivery(DEL_BE_S3, t)
print("BE → DEL_BE_S3 ✅")

# FE (7 tareas) → DEL_FE_S3
for t in [T_4_4_1, T_4_4_3, T_4_4_4, T_4_4_5, T_4_4_6, T_4_4_7, T_4_4_8]:
    assign_task_to_delivery(DEL_FE_S3, t)
print("FE → DEL_FE_S3 ✅")

# TL (1 tarea) → DEL_TL_S3
assign_task_to_delivery(DEL_TL_S3, TL_S3_REV)
print("TL → DEL_TL_S3 ✅")

# REV (4 tareas + SETUP) → DEL_REV_S3
for t in [AR_S3, DL_S3_REV, CIERRE_S3, APR_S3, SETUP_S3]:
    assign_task_to_delivery(DEL_REV_S3, t)
print("REV → DEL_REV_S3 ✅")

print("Todas las tareas asociadas a Deliveries ✅")
```

---

## 11. PASO 9: REGISTRAR DEPENDENCIAS

```python
def add_dep(task_id, depends_on_id):
    body = {"dependsOnTaskId": depends_on_id}
    req = urllib.request.Request(f'{BASE_URL}/api/tasks/{task_id}/dependencies',
        data=json.dumps(body).encode(), headers=HEADERS, method='POST')
    urllib.request.urlopen(req)
    time.sleep(0.05)

print("Registrando dependencias S3...")

# === CROSS-SPRINT: S2 → S3 ===
add_dep(SETUP_S3, CIERRE_S2)

# === BE chain ===
add_dep(T_4_3_1, T_4_3_2_S2)     # Endpoints ← Services (S2)
add_dep(T_4_3_1, T_4_3_7_S2)     # Endpoints ← Middlewares (S2)
add_dep(T_4_3_1, T_4_2_5_S2)     # Endpoints ← Indexes (S2) — GET /context necesita indexes
add_dep(T_4_3_6, T_4_3_2_S2)     # Cleanup Job ← Services (S2)
add_dep(T_4_5_1, T_4_3_2_S2)     # Integration Code ← Services (S2)
add_dep(T_4_5_2, T_4_5_1)        # API Clients ← Integration Code
add_dep(T_4_5_3, T_4_5_1)        # Webhooks ← Integration Code
add_dep(T_4_5_5, SETUP_S3)       # SDKs ← SETUP (npm install)

# === FE chain ===
add_dep(T_4_4_7, SETUP_S3)       # Types ← SETUP
add_dep(T_4_4_8, SETUP_S3)       # Styles ← SETUP
add_dep(T_4_4_1, T_4_4_8)        # Components ← Styles (Tailwind tokens necesarios)
add_dep(T_4_4_3, T_4_4_1)        # Layouts ← Components
add_dep(T_4_4_6, T_4_4_7)        # API Client ← Types
add_dep(T_4_4_4, T_4_4_6)        # Hooks ← API Client (fetch wrapper)
add_dep(T_4_4_5, T_4_4_1)        # State Management ← Components

# === Validación chain ===
add_dep(TL_S3_REV, T_4_3_1)      # TL Review ← Endpoints (última BE crítica)
add_dep(TL_S3_REV, T_4_3_6)      # TL Review ← Cleanup Job
add_dep(TL_S3_REV, T_4_5_2)      # TL Review ← API Clients
add_dep(TL_S3_REV, T_4_5_3)      # TL Review ← Webhooks
add_dep(TL_S3_REV, T_4_4_4)      # TL Review ← Hooks (última FE)
add_dep(TL_S3_REV, T_4_4_5)      # TL Review ← State Management
add_dep(DL_S3_REV, T_4_4_1)      # DL Review ← Components
add_dep(DL_S3_REV, T_4_4_3)      # DL Review ← Layouts
add_dep(DL_S3_REV, T_4_4_8)      # DL Review ← Styles
add_dep(AR_S3, TL_S3_REV)        # AR ← TL Review
add_dep(CIERRE_S3, AR_S3)        # CIERRE ← AR
add_dep(CIERRE_S3, DL_S3_REV)    # CIERRE ← DL Review
add_dep(APR_S3, CIERRE_S3)       # APR ← CIERRE

print("Dependencias S3 registradas ✅")
```

---

## 12. PASO 10: GENERAR CONTEXTO

```markdown
# CONTEXTO: Sprint S3 — Features BE + FE Start

**Generado por:** TL-Agent
**Fecha:** [FECHA]

## 1. Estructura VTT

| Entidad | ID |
|---------|-----|
| Release R1 | {RELEASE_ID} |
| Sprint S3 | {SPRINT_S3_ID} |

## 2. Deliveries

| Delivery | ID |
|----------|-----|
| BE-S3: Endpoints + Integrations + Worker | {DEL_BE_S3} |
| FE-S3: Foundation | {DEL_FE_S3} |
| TL-S3: Reviews + SLA Check | {DEL_TL_S3} |
| REV-S3: Validación + Cierre | {DEL_REV_S3} |

## 3. Tareas

| ID Cat | Título | VTT ID | Rol | Horas | Delivery |
|--------|--------|--------|:---:|:-----:|----------|
| 4.3.1 | API Endpoints | {T_4_3_1} | BE | 13 | DEL_BE_S3 |
| 4.3.6 | Workers — Cleanup Job | {T_4_3_6} | BE | 8 | DEL_BE_S3 |
| 4.5.1 | Integration Code | {T_4_5_1} | BE | 8 | DEL_BE_S3 |
| 4.5.2 | API Clients | {T_4_5_2} | BE | 5 | DEL_BE_S3 |
| 4.5.3 | Webhooks | {T_4_5_3} | BE | 5 | DEL_BE_S3 |
| 4.5.5 | Third-party SDKs | {T_4_5_5} | BE | 3 | DEL_BE_S3 |
| 4.4.1 | Components | {T_4_4_1} | FE | 8 | DEL_FE_S3 |
| 4.4.3 | Layouts | {T_4_4_3} | FE | 3 | DEL_FE_S3 |
| 4.4.4 | Hooks | {T_4_4_4} | FE | 5 | DEL_FE_S3 |
| 4.4.5 | State Management | {T_4_4_5} | FE | 5 | DEL_FE_S3 |
| 4.4.6 | API Client FE | {T_4_4_6} | FE | 5 | DEL_FE_S3 |
| 4.4.7 | Types/Interfaces | {T_4_4_7} | FE | 3 | DEL_FE_S3 |
| 4.4.8 | Styles | {T_4_4_8} | FE | 3 | DEL_FE_S3 |
| — | TL Reviews + SLA Check | {TL_S3_REV} | TL | 3 | DEL_TL_S3 |
| — | AR Audit | {AR_S3} | AR | 3 | DEL_REV_S3 |
| — | DL Visual Review | {DL_S3_REV} | DL | 2 | DEL_REV_S3 |
| — | CIERRE-S3 | {CIERRE_S3} | TL | 2 | DEL_REV_S3 |
| — | APR-S3 | {APR_S3} | PM | 1 | DEL_REV_S3 |

## 4. Resumen

| Categoría | Tareas | Horas |
|-----------|:------:|:-----:|
| BE (Endpoints+Integrations+Worker) | 6 | 42h |
| FE (Foundation) | 7 | 32h |
| TL (Reviews) | 1 | 3h |
| Validación + Cierre + APR | 4 | 8h |
| **Total** | **18** | **85h** |
```

---

## 13. CHECKLIST DE VERIFICACIÓN

```markdown
## Setup S3 — Verificación Final

### Estructura VTT
[ ] Sprint S3 creado y vinculado a R1
[ ] 4 Deliveries creados y vinculados a Sprint S3

### Tareas BE (6) → DEL_BE_S3
[ ] [4.3.1] API Endpoints
[ ] [4.3.6] Workers — Cleanup Job
[ ] [4.5.1] Integration Code
[ ] [4.5.2] API Clients
[ ] [4.5.3] Webhooks
[ ] [4.5.5] Third-party SDKs

### Tareas FE (7) → DEL_FE_S3
[ ] [4.4.1] Components
[ ] [4.4.3] Layouts
[ ] [4.4.4] Hooks
[ ] [4.4.5] State Management
[ ] [4.4.6] API Client FE
[ ] [4.4.7] Types/Interfaces
[ ] [4.4.8] Styles

### Validación (5) → DEL_TL_S3 + DEL_REV_S3
[ ] TL-S3-REV
[ ] AR-S3
[ ] DL-S3-REV
[ ] CIERRE-S3
[ ] APR-S3

### Dependencias cross-sprint
[ ] SETUP-S3 ← CIERRE-S2
[ ] 4.3.1 ← 4.3.2 + 4.3.7 + 4.2.5 (S2)
[ ] 4.3.6, 4.5.1 ← 4.3.2 (S2)

### Dependencias intra-sprint
[ ] BE: 4.5.1 → 4.5.2, 4.5.3
[ ] FE: 4.4.8 → 4.4.1 → 4.4.3, 4.4.5; 4.4.7 → 4.4.6 → 4.4.4
[ ] Val: BE+FE → TL; FE visual → DL; TL+DL → AR → CIERRE → APR

### Documentación
[ ] CONTEXTO_S3.md generado
[ ] Agentes notificados (BE + FE)
```

---

**FIN DEL SETUP S3**
