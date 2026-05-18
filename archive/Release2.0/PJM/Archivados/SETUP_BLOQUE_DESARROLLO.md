# SETUP: Bloque Desarrollo — Memory Service

**Documento:** SETUP_BLOQUE_DESARROLLO.md  
**De:** PJM-Agent  
**Para:** TL (Tech Lead)  
**Fecha:** 2026-04-21  
**Versión:** 1.0  
**Estado:** 📋 READY PARA EJECUTAR

---

## 0. QUÉ ES ESTE DOCUMENTO

Este documento es tu instrucción de setup. Tu trabajo como TL **antes de ejecutar cualquier sprint** es crear en VTT toda la estructura de tareas atómicas para el bloque de Desarrollo (Phase 5 Design UX/UI + Phase 7 Development), configurar las dependencias y generar el CONTEXTO.

**No empieces a codear ni asignar código a nadie hasta que este setup esté completo.**

Flujo:
```
1. Leer este documento completo
2. Crear tarea SETUP-BLOQUE-DEV en VTT (gate)
3. Crear TODAS las tareas atómicas de Phase 5 + Phase 7
4. Configurar dependencias
5. Crear tareas de CIERRE por sprint + CIERRE-BLOQUE
6. Generar CONTEXTO_BLOQUE_DESARROLLO.md con todos los IDs
7. Marcar SETUP-BLOQUE-DEV como task_completed
8. Notificar al PJM
```

**Solo cuando el setup esté completo los sprints pueden iniciar.**

---

## 1. CONTEXTO DEL PROYECTO

| Dato | Valor |
|------|-------|
| Project ID | `51e169f7-8a23-4628-8b78-04864b633ac7` |
| API URL | `http://77.42.88.106:3000` |
| Tu UUID (TL) | `92225290-6b6b-4c1f-a940-dcb4262507aa` |
| SERVICE_KEY | En `/root/memory-service/.env` en la VM |

### Autenticación

```python
import urllib.request, json, os

BASE_URL = "http://77.42.88.106:3000"
TL_ID    = "92225290-6b6b-4c1f-a940-dcb4262507aa"
SK       = os.environ.get("MEM_VTT_SERVICE_KEY")  # export MEM_VTT_SERVICE_KEY="..."

r = urllib.request.urlopen(urllib.request.Request(
    BASE_URL + "/api/auth/service-token",
    data=json.dumps({"userId": TL_ID, "serviceKey": SK}).encode(),
    headers={"Content-Type": "application/json"}, method="POST"))
TOKEN = json.loads(r.read())["data"]["token"]
HEADERS = {"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"}
```

---

## 2. FASES DONDE SE CREAN LAS TAREAS

| Fase | Phase UUID | Tareas |
|------|-----------|--------|
| Phase 5: Design UX/UI | `2c8f0f2f-992a-46e5-b80f-9739180c2532` | Todas las tareas DL |
| Phase 7: Development | `c2804591-b21c-4340-9065-59fd23e14b63` | Todas las tareas DB, BE, FE, QA, DO, TL reviews |

> **Nota sobre los 116 MEM-XXX:** Esos ítems son deliverables de control (nivel de entrega), NO tareas atómicas. Tu trabajo es crear las tareas atómicas NUEVAS en las fases. No toques ni modifiques los MEM-XXX existentes — son hitos del PM.

---

## 3. AGENTES Y UUIDs

| Sigla | UUID |
|-------|------|
| TL | `92225290-6b6b-4c1f-a940-dcb4262507aa` |
| DB | `6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7` |
| BE | `ebbe3cee-abed-4b3b-860d-0a81f632b08a` |
| FE | `d23c9cd9-a156-433b-8900-94add5488eec` |
| QA | `613c9538-658c-45fe-a6d7-c1ea9ff04b78` |
| DO | `322e3745-9756-4a7c-af11-44b33edef44d` |
| DL | `b3a09269-cded-468c-a475-15a48f203cb0` |
| AR | `e9403c25-c1f8-4b64-b2ef-f447d53115e2` |

### Prioridades

| Nombre | UUID |
|--------|------|
| high | `1a617554-6319-4c56-826f-8ef49a0ff9cc` |
| medium | `d0b619ef-27e7-42d8-8879-41030a602eed` |

---

## 4. PASO 1 — CREAR TAREA SETUP-BLOQUE-DEV (GATE)

Esta tarea es el nodo ORIGEN. Todas las primeras tareas de cada sprint dependen de ella.

**Crear en Phase 7 (Development):**

```json
{
  "title": "SETUP-BLOQUE-DEV: Estructura de tareas atómicas creada",
  "priorityId": "1a617554-6319-4c56-826f-8ef49a0ff9cc",
  "complexity": "LOW",
  "category": "documentation",
  "estimatedHours": 2,
  "description": "Gate de inicio: todas las tareas del bloque Development creadas con dependencias configuradas"
}
```

**Guardar el UUID que retorna — es SETUP_ID, lo necesitas para las dependencias.**

---

## 5. PASO 2 — CREAR TAREAS PHASE 5: DESIGN UX/UI (11 tareas DL)

Phase UUID: `2c8f0f2f-992a-46e5-b80f-9739180c2532`

> Las tareas DL van en Phase 5. Al crear, NO incluir `assigneeId` (bug VTT — ignorado en POST). Asignar después con PATCH.

### Sprint S-DL-01 (orden 1-3)

| ID local | title | estimatedHours | complexity | category |
|----------|-------|---------------|-----------|----------|
| DL-S01-01 | Design System tokens (colores, tipografía, espaciado) | 3 | MEDIUM | design |
| DL-S01-02 | Wireframes Dashboard (stats, actividad reciente) | 4 | HIGH | design |
| DL-S01-03 | Wireframes Agent Timeline (cronología conversaciones) | 3 | MEDIUM | design |

### Sprint S-DL-02 (orden 4-5)

| ID local | title | estimatedHours | complexity | category |
|----------|-------|---------------|-----------|----------|
| DL-S02-01 | Wireframes Conversation Viewer modo TASK | 4 | HIGH | design |
| DL-S02-02 | Wireframes Conversation Viewer modo REVIEW | 4 | HIGH | design |

### Sprint S-DL-03 (orden 6-9)

| ID local | title | estimatedHours | complexity | category |
|----------|-------|---------------|-----------|----------|
| DL-S03-01 | Wireframes Import Manual | 2 | MEDIUM | design |
| DL-S03-02 | Wireframes Cost Reports (proyecto y agente) | 2 | MEDIUM | design |
| DL-S03-03 | Wireframes Lista/Búsqueda conversaciones | 2 | MEDIUM | design |
| DL-S03-04 | Wireframes Health page | 1 | LOW | design |

### Sprint S-DL-04 + APR-DL (orden 10-12)

| ID local | title | estimatedHours | complexity | category |
|----------|-------|---------------|-----------|----------|
| DL-S04-01 | Documento UX Spec completo (9 pantallas, estados, flows) | 2 | MEDIUM | documentation |
| DL-S04-02 | Handoff a FE (assets exportados, specs, tokens) | 1 | LOW | documentation |
| APR-DL | APR-DL: Aprobación Design Handoff — FE puede iniciar | 1 | LOW | review |

**Después de crear las 12 tareas, asignar con PATCH:**
- DL-S01-01 a DL-S04-02 → `assigneeId: b3a09269-cded-468c-a475-15a48f203cb0` (DL)
- APR-DL → `assigneeId: 92225290-6b6b-4c1f-a940-dcb4262507aa` (TL)

---

## 6. PASO 3 — CREAR TAREAS PHASE 7: DEVELOPMENT (52 tareas + gate tasks)

Phase UUID: `c2804591-b21c-4340-9065-59fd23e14b63`

### 6.1 Sprint MEM-S01: Schema + Seeds (9h total)

| ID local | title | estimatedHours | complexity | category | assignee |
|----------|-------|---------------|-----------|----------|---------|
| MEM-DB-001 | Crear schema Prisma completo (19 tablas, 10 catálogos) | 3 | HIGH | development | DB |
| MEM-DB-002 | Migraciones + partial indexes (SQL manual) | 2 | MEDIUM | development | DB |
| MEM-DB-003 | Seed catálogos (sources, statuses, topics, workTypes) | 1 | LOW | development | DB |
| MEM-BE-001 | Setup proyecto Express + estructura carpetas | 2 | MEDIUM | development | BE |
| MEM-BE-002 | Catalog cache en startup (prefetch para evitar N+1) | 1 | LOW | development | BE |
| TL-S01-REV | Code Review PRs MEM-S01 (schema + setup) | 1 | MEDIUM | review | TL |
| CIERRE-S01 | CIERRE-S01: Sprint Schema+Seeds completado | 1 | LOW | review | TL |

### 6.2 Sprint MEM-S02: Import + Timeline (12h total)

| ID local | title | estimatedHours | complexity | category | assignee |
|----------|-------|---------------|-----------|----------|---------|
| MEM-BE-003 | POST /api/conversations/import (source CLAUDE_SDK, idempotencia P2002) | 4 | HIGH | development | BE |
| MEM-BE-004 | Parser JSONL + validación + externalSessionId format | 2 | MEDIUM | development | BE |
| MEM-BE-005 | Clasificación por reglas (topics por keywords, workType por agentRole) | 3 | HIGH | development | BE |
| MEM-BE-006 | GET /api/agents/:agentId/timeline | 2 | MEDIUM | development | BE |
| MEM-BE-007 | Storage contenido completo en filesystem + contentPreview en BD | 1 | LOW | development | BE |
| TL-S02-REV | Code Review PRs MEM-S02 (import + timeline) | 1 | MEDIUM | review | TL |
| CIERRE-S02 | CIERRE-S02: Sprint Import+Timeline completado | 1 | LOW | review | TL |

### 6.3 Sprint MEM-S03: Content + Context <500ms (12h total)

| ID local | title | estimatedHours | complexity | category | assignee |
|----------|-------|---------------|-----------|----------|---------|
| MEM-BE-008 | GET /api/conversations/:id/content (messages parseados) | 2 | MEDIUM | development | BE |
| MEM-BE-009 | GET /api/context (JSON estructurado, fail-fast, sin transformar) | 4 | HIGH | development | BE |
| MEM-BE-010 | Optimización <500ms con índices parciales + prefetch statusId | 2 | HIGH | development | BE |
| MEM-QA-001 | Tests rendimiento GET /context (10/100/1000 convs, 50 concurrent) | 2 | MEDIUM | testing | QA |
| MEM-QA-002 | Tests unitarios import + clasificación | 2 | MEDIUM | testing | QA |
| TL-S03-REV | Code Review PRs MEM-S03 (context + performance) | 1 | MEDIUM | review | TL |
| CIERRE-S03 | CIERRE-S03: Sprint Content+Context completado | 1 | LOW | review | TL |

### 6.4 Sprint MEM-S04: Adapters + Cleanup (12h total)

| ID local | title | estimatedHours | complexity | category | assignee |
|----------|-------|---------------|-----------|----------|---------|
| MEM-BE-011 | POST /api/conversations/import-review (prefetch catalogs) | 3 | MEDIUM | development | BE |
| MEM-BE-012 | Adapter Claude Web (JSON export de claude.ai) | 2 | MEDIUM | development | BE |
| MEM-BE-013 | Adapter ChatGPT (JSON export) | 2 | MEDIUM | development | BE |
| MEM-BE-014 | Cleanup job por statusId (catch delega siempre, max 3 retries) | 2 | MEDIUM | development | BE |
| MEM-BE-015 | Retry logic con log de acciones | 1 | LOW | development | BE |
| MEM-BE-016 | Tests unitarios cada adapter + cleanup logic | 2 | MEDIUM | testing | BE |
| TL-S04-REV | Code Review PRs MEM-S04 (adapters + cleanup) | 1 | MEDIUM | review | TL |
| CIERRE-S04 | CIERRE-S04: Sprint Adapters+Cleanup completado | 1 | LOW | review | TL |

### 6.5 Sprint MEM-S05: Lista + Cost + Dashboard (11h total)

| ID local | title | estimatedHours | complexity | category | assignee |
|----------|-------|---------------|-----------|----------|---------|
| MEM-BE-017 | GET /api/conversations (lista, filtros, paginación) | 2 | MEDIUM | development | BE |
| MEM-BE-018 | GET /api/projects/:id/cost-report (sumas tokens + costos 6 decimales) | 2 | MEDIUM | development | BE |
| MEM-BE-019 | GET /api/agents/:id/cost-report (breakdown por workType) | 2 | MEDIUM | development | BE |
| MEM-BE-020 | GET /api/dashboard (stats globales + actividad reciente) | 2 | MEDIUM | development | BE |
| MEM-BE-021 | POST /api/conversations/upload (import manual) | 2 | MEDIUM | development | BE |
| MEM-BE-022 | GET /health (BD, storage, cache status) | 1 | LOW | development | BE |
| TL-S05-REV | Code Review PRs MEM-S05 (lista + cost + dashboard) | 1 | MEDIUM | review | TL |
| CIERRE-S05 | CIERRE-S05: Sprint Lista+Cost+Dashboard completado | 1 | LOW | review | TL |

### 6.6 Sprint MEM-S06: Docker + Integration (14h total)

| ID local | title | estimatedHours | complexity | category | assignee |
|----------|-------|---------------|-----------|----------|---------|
| MEM-DO-001 | Dockerfile + docker-compose.yml (puerto 3002/3003) | 2 | MEDIUM | deployment | DO |
| MEM-DO-002 | Deploy a VM Hetzner 77.42.88.106 | 2 | MEDIUM | deployment | DO |
| MEM-DO-003 | Configuración nginx/traefik reverse proxy | 1 | LOW | deployment | DO |
| MEM-BE-023 | Integración Hook Manager VTT (externalSessionId={run_id}:r{N}:{role}) | 4 | HIGH | development | BE |
| MEM-QA-003 | Tests E2E flujo completo SDK→import→context | 3 | HIGH | testing | QA |
| MEM-QA-004 | Tests integración Runtime v1.1 (platformRefs, source CLAUDE_SDK) | 2 | MEDIUM | testing | QA |
| TL-S06-REV | Code Review PRs MEM-S06 (docker + integration) | 1 | MEDIUM | review | TL |
| AR-S06-AUD | Integration Audit final BE (AR revisa arquitectura implementada) | 2 | MEDIUM | review | AR |
| CIERRE-S06 | CIERRE-S06: BE Backend completo — gate para UI | 1 | LOW | review | TL |

### 6.7 Sprint UI-01: Setup + Timeline + Viewer TASK (16h total)

> ⚠️ **GATE DOBLE**: Esta tarea no puede empezar hasta que CIERRE-S06 + APR-DL estén completados.

| ID local | title | estimatedHours | complexity | category | assignee |
|----------|-------|---------------|-----------|----------|---------|
| MEM-FE-001 | Setup React + Vite + TailwindCSS | 2 | MEDIUM | development | FE |
| MEM-FE-002 | Configuración API client (base URL, interceptors) | 1 | LOW | development | FE |
| MEM-FE-003 | Agent Timeline component (cronología de conversaciones) | 5 | HIGH | development | FE |
| MEM-FE-004 | Conversation Viewer modo TASK (mensajes + metadata) | 6 | HIGH | development | FE |
| MEM-FE-005 | Routing + layout base (nav, sidebar, breadcrumbs) | 2 | MEDIUM | development | FE |
| TL-UI01-REV | Code Review PRs UI-01 | 1 | MEDIUM | review | TL |
| DL-UI01-REV | DL Review UI-01 vs wireframes | 2 | MEDIUM | review | DL |
| CIERRE-UI01 | CIERRE-UI01: Sprint Setup+Timeline+Viewer completado | 1 | LOW | review | TL |

### 6.8 Sprint UI-02: Dashboard + Cost + Import (12h total)

| ID local | title | estimatedHours | complexity | category | assignee |
|----------|-------|---------------|-----------|----------|---------|
| MEM-FE-006 | Dashboard page (stats, gráficas, actividad reciente) | 4 | HIGH | development | FE |
| MEM-FE-007 | Cost Report Proyecto page (tabla + breakdown) | 4 | MEDIUM | development | FE |
| MEM-FE-008 | Import Manual page (upload + preview + submit) | 4 | MEDIUM | development | FE |
| TL-UI02-REV | Code Review PRs UI-02 | 1 | MEDIUM | review | TL |
| DL-UI02-REV | DL Review UI-02 vs wireframes | 2 | MEDIUM | review | DL |
| CIERRE-UI02 | CIERRE-UI02: Sprint Dashboard+Cost+Import completado | 1 | LOW | review | TL |

### 6.9 Sprint UI-03: Viewer REVIEW + Lista (10h total)

| ID local | title | estimatedHours | complexity | category | assignee |
|----------|-------|---------------|-----------|----------|---------|
| MEM-FE-009 | Conversation Viewer modo REVIEW (anotaciones, diff) | 5 | HIGH | development | FE |
| MEM-FE-010 | Lista conversaciones + búsqueda + filtros avanzados | 5 | HIGH | development | FE |
| TL-UI03-REV | Code Review PRs UI-03 | 1 | MEDIUM | review | TL |
| DL-UI03-REV | DL Review UI-03 vs wireframes | 2 | MEDIUM | review | DL |
| CIERRE-UI03 | CIERRE-UI03: Sprint Viewer+Lista completado | 1 | LOW | review | TL |

### 6.10 Sprint UI-04: Cost Agente + Health + Estados (8h total)

| ID local | title | estimatedHours | complexity | category | assignee |
|----------|-------|---------------|-----------|----------|---------|
| MEM-FE-011 | Cost Report Agente page | 3 | MEDIUM | development | FE |
| MEM-FE-012 | Health page (estado BD, storage, servicios) | 2 | LOW | development | FE |
| MEM-FE-013 | Estados globales: loading, empty, error (componentes reutilizables) | 3 | MEDIUM | development | FE |
| TL-UI04-REV | Code Review PRs UI-04 | 1 | MEDIUM | review | TL |
| DL-UI04-REV | DL Review UI-04 vs wireframes | 2 | MEDIUM | review | DL |
| APR-QA-UI | APR-QA: Todas las pruebas QA UI aprobadas | 1 | LOW | review | QA |
| CIERRE-UI04 | CIERRE-UI04: Sprint UI-04 + QA aprobado | 1 | LOW | review | TL |

### 6.11 Tarea de Cierre Final

| ID local | title | estimatedHours | complexity | category | assignee |
|----------|-------|---------------|-----------|----------|---------|
| CIERRE-BLOQUE-DEV | CIERRE-BLOQUE-DEV: Desarrollo completo — entrega al PM | 1 | LOW | review | TL |

**Total de tareas a crear: 12 (Phase 5) + ~75 (Phase 7) ≈ 87 tareas atómicas**

---

## 7. PASO 4 — DEPENDENCIAS

### 7.1 Grafo de dependencias (leer antes de crear)

Reglas de METODOLOGIA_SETUP_PLAN_VTT:
- 1 solo nodo ORIGEN (SETUP-BLOQUE-DEV)
- 0 nodos huérfanos ni hojas excepto SETUP (origen) y CIERRE-BLOQUE-DEV (final)
- CIERRE de cada sprint → habilita el siguiente sprint

```
SETUP-BLOQUE-DEV (ORIGEN)
    │
    ├──► Phase 5 DL track (paralelo con BE)
    │    DL-S01-01 ──► DL-S01-02
    │              ──► DL-S01-03
    │    DL-S01-02 ──► DL-S02-01 ──► DL-S03-01 ──► DL-S04-01 ──► APR-DL
    │    DL-S01-03 ──► DL-S02-02 ──► DL-S03-02 ──► DL-S04-02 ──► APR-DL
    │                              ──► DL-S03-03 ──► APR-DL
    │                              ──► DL-S03-04 ──► APR-DL
    │
    ├──► MEM-DB-001 ──► MEM-DB-002 ──► MEM-DB-003
    │                                       │
    │    MEM-DB-001 ──► MEM-BE-001 ──► MEM-BE-002
    │                                       │
    │    MEM-DB-003 + MEM-BE-002 ──► TL-S01-REV ──► CIERRE-S01
    │
    CIERRE-S01 ──► MEM-BE-003 ──► MEM-BE-004
    │                         ──► MEM-BE-005 ──► MEM-BE-006
    │                                              ──► MEM-BE-007 ──► TL-S02-REV ──► CIERRE-S02
    │
    CIERRE-S02 ──► MEM-BE-008 ──► MEM-BE-009 ──► MEM-BE-010 ──► MEM-QA-001
    │                                                          ──► MEM-QA-002
    │    MEM-QA-001 + MEM-QA-002 + MEM-BE-010 ──► TL-S03-REV ──► CIERRE-S03
    │
    CIERRE-S03 ──► MEM-BE-011 ──► MEM-BE-012 ──► MEM-BE-016
    │                         ──► MEM-BE-013 ──► MEM-BE-016
    │                         ──► MEM-BE-014 ──► MEM-BE-015 ──► MEM-BE-016
    │    MEM-BE-016 ──► TL-S04-REV ──► CIERRE-S04
    │
    CIERRE-S04 ──► MEM-BE-017 ──► MEM-BE-018
    │                         ──► MEM-BE-019
    │                         ──► MEM-BE-020
    │                         ──► MEM-BE-021
    │                         ──► MEM-BE-022
    │    MEM-BE-022 + MEM-BE-021 + MEM-BE-020 ──► TL-S05-REV ──► CIERRE-S05
    │
    CIERRE-S05 ──► MEM-DO-001 ──► MEM-DO-002 ──► MEM-DO-003
    │          ──► MEM-BE-023
    │          ──► MEM-QA-003 ──► MEM-QA-004
    │    MEM-DO-003 + MEM-BE-023 + MEM-QA-004 ──► TL-S06-REV ──► AR-S06-AUD ──► CIERRE-S06
    │
    CIERRE-S06 + APR-DL ──► MEM-FE-001 ──► MEM-FE-002
    │                                   ──► MEM-FE-005
    │                    MEM-FE-001 ──► MEM-FE-003 ──► MEM-FE-004 ──► TL-UI01-REV
    │                    TL-UI01-REV + MEM-FE-004 ──► DL-UI01-REV ──► CIERRE-UI01
    │
    CIERRE-UI01 ──► MEM-FE-006 ──► MEM-FE-007
    │                           ──► MEM-FE-008
    │    MEM-FE-008 ──► TL-UI02-REV ──► DL-UI02-REV ──► CIERRE-UI02
    │
    CIERRE-UI02 ──► MEM-FE-009 ──► MEM-FE-010
    │    MEM-FE-010 ──► TL-UI03-REV ──► DL-UI03-REV ──► CIERRE-UI03
    │
    CIERRE-UI03 ──► MEM-FE-011 ──► MEM-FE-012
    │                           ──► MEM-FE-013
    │    MEM-FE-013 + MEM-FE-012 ──► TL-UI04-REV ──► DL-UI04-REV ──► APR-QA-UI ──► CIERRE-UI04
    │
    CIERRE-S06 + CIERRE-UI04 ──► CIERRE-BLOQUE-DEV (FINAL)
```

### 7.2 Cómo crear dependencias vía API

```python
def add_dependency(task_id, depends_on_task_id):
    """task_id DEPENDE de depends_on_task_id (finish-to-start)"""
    body = {"dependsOnTaskId": depends_on_task_id}
    req = urllib.request.Request(
        f"{BASE_URL}/api/tasks/{task_id}/dependencies",
        data=json.dumps(body).encode(),
        headers=HEADERS, method="POST")
    try:
        r = urllib.request.urlopen(req)
        print(f"  OK dep: {task_id} → {depends_on_task_id}")
    except Exception as e:
        print(f"  ERROR dep: {task_id} → {depends_on_task_id}: {e}")
```

---

## 8. PASO 5 — VERIFICAR GRAFO (AUDITORÍA)

Después de crear todas las dependencias, ejecutar este script para verificar 0 huérfanos y 0 hojas:

```python
import time

def get_deps(token, task_id):
    req = urllib.request.Request(
        f"{BASE_URL}/api/tasks/{task_id}/dependencies",
        headers={"Authorization": f"Bearer {token}"}, method="GET")
    try:
        with urllib.request.urlopen(req) as r:
            raw = json.loads(r.read())
            return raw if isinstance(raw, list) else raw.get("data", raw.get("dependencies", []))
    except:
        return []

def audit_graph(task_ids, final_id, origin_id):
    depended_upon = set()
    has_incoming = set()
    for tid in task_ids:
        deps = get_deps(TOKEN, tid)
        for d in deps:
            dep_on = (d.get("dependsOnTaskId") or
                      d.get("dependsOnTask", {}).get("id") or "")
            if dep_on:
                depended_upon.add(dep_on)
                has_incoming.add(tid)
        time.sleep(0.05)

    leaves   = [t for t in task_ids if t not in depended_upon and t != final_id]
    orphans  = [t for t in task_ids if t not in has_incoming and t != origin_id]

    print(f"Leaves  (sin salida):  {len(leaves)}")
    for t in leaves: print(f"  LEAF:   {t}")
    print(f"Orphans (sin entrada): {len(orphans)}")
    for t in orphans: print(f"  ORPHAN: {t}")
    if not leaves and not orphans:
        print("GRAPH OK — 0 hojas, 0 huérfanos")
```

**Criterio de aceptación: 0 hojas, 0 huérfanos** (excepto tareas canceladas).

---

## 9. PASO 6 — ASIGNAR AGENTES (PATCH)

Después de crear todas las tareas y verificar el grafo, asignar agentes via PATCH:

```python
def patch_task(task_id, assignee_id):
    body = {"assigneeId": assignee_id}
    req = urllib.request.Request(
        f"{BASE_URL}/api/tasks/{task_id}",
        data=json.dumps(body).encode(),
        headers=HEADERS, method="PATCH")
    urllib.request.urlopen(req)
    print(f"  PATCH assignee OK: {task_id}")
```

Asignar según la columna `assignee` de las tablas en §5 y §6.

---

## 10. PASO 7 — GENERAR CONTEXTO_BLOQUE_DESARROLLO.md

Al terminar el setup, generar este archivo con todos los UUIDs reales de VTT:

**Ubicación:** `memory-service-project/Release2.0/PJM/CONTEXTO_BLOQUE_DESARROLLO.md`

```markdown
# CONTEXTO: Bloque Desarrollo — Memory Service

## 1. IDs del Proyecto

| Entidad | ID |
|---------|----|
| Proyecto | 51e169f7-8a23-4628-8b78-04864b633ac7 |
| Phase 5 Design UX/UI | 2c8f0f2f-992a-46e5-b80f-9739180c2532 |
| Phase 7 Development | c2804591-b21c-4340-9065-59fd23e14b63 |

## 2. IDs de Tareas Gate

| Tarea | ID VTT |
|-------|--------|
| SETUP-BLOQUE-DEV | [UUID] |
| APR-DL | [UUID] |
| CIERRE-S01 | [UUID] |
| CIERRE-S02 | [UUID] |
| CIERRE-S03 | [UUID] |
| CIERRE-S04 | [UUID] |
| CIERRE-S05 | [UUID] |
| CIERRE-S06 | [UUID] |
| CIERRE-UI01 | [UUID] |
| CIERRE-UI02 | [UUID] |
| CIERRE-UI03 | [UUID] |
| CIERRE-UI04 | [UUID] |
| CIERRE-BLOQUE-DEV | [UUID] |

## 3. IDs de Tareas Atómicas

[Tabla completa: ID local → UUID VTT, para CADA una de las 87 tareas]

## 4. Agentes Asignados

[Tabla rol → UUID]
```

Este documento es la referencia que todos los agentes usarán durante la ejecución.

---

## 11. PASO 8 — MARCAR SETUP COMO COMPLETO Y NOTIFICAR

Cuando el setup esté terminado (grafo validado, agentes asignados, CONTEXTO generado):

```python
# Marcar SETUP-BLOQUE-DEV como task_completed
body = {"status": "task_completed"}
req = urllib.request.Request(
    f"{BASE_URL}/api/tasks/{SETUP_ID}/status",
    data=json.dumps(body).encode(),
    headers=HEADERS, method="PATCH")
urllib.request.urlopen(req)
```

**Notificar al PJM con el siguiente formato:**

```
## Setup Completado: Bloque Desarrollo

SETUP-BLOQUE-DEV: [UUID] → task_completed

Tareas creadas:
- Phase 5 (DL): 12 tareas
- Phase 7 (BE + DB + FE + QA + DO + reviews): XX tareas

CONTEXTO_BLOQUE_DESARROLLO.md generado en: Release2.0/PJM/

Grafo auditado: 0 hojas, 0 huérfanos.

Siguiente paso: iniciar MEM-S01 (DB puede arrancar).
```

---

## 12. CHECKLIST COMPLETO TL

### Prerrequisitos
- [ ] Leí METODOLOGIA_SETUP_FASE.md
- [ ] Leí METODOLOGIA_SETUP_PLAN_VTT.md
- [ ] Acceso a VTT verificado (GET /api/health retorna 200)
- [ ] SERVICE_KEY exportada como env var

### Estructura
- [ ] SETUP-BLOQUE-DEV creado en Phase 7 → guardé UUID como SETUP_ID
- [ ] 12 tareas DL creadas en Phase 5
- [ ] ~75 tareas DB/BE/FE/QA/DO/TL/AR creadas en Phase 7

### Asignaciones
- [ ] Todos los agentes asignados via PATCH (DL, DB, BE, FE, QA, DO, TL, AR)

### Dependencias
- [ ] Dependencias creadas según grafo §7.1
- [ ] SETUP-BLOQUE-DEV es dependencia de MEM-DB-001 y DL-S01-01
- [ ] APR-DL es dependencia de MEM-FE-001 (junto con CIERRE-S06)
- [ ] Cada CIERRE-SXX habilita el siguiente sprint
- [ ] CIERRE-BLOQUE-DEV depende de CIERRE-S06 y CIERRE-UI04

### Auditoría
- [ ] Script audit_graph ejecutado → 0 hojas, 0 huérfanos

### Documentación
- [ ] CONTEXTO_BLOQUE_DESARROLLO.md generado con todos los IDs
- [ ] SETUP-BLOQUE-DEV marcado como task_completed

### Notificación
- [ ] PJM notificado con el formato de §11

---

## 13. GOTCHAS API VTT (RECORDATORIO)

| Gotcha | Acción |
|--------|--------|
| `POST /api/phases/{id}/tasks` ignora `assigneeId` | Crear task primero, luego PATCH con assigneeId |
| `POST task` con `deliveryId` no persiste en GET | No preocuparse por linkear tasks a deliveries — son planos a nivel fase |
| `PUT /api/phases/{id}` ignora `order` | Usar PATCH /phases/reorder si necesitas reordenar |
| Response GET phases: `resp["data"]["data"]` | Doble data en el response |

---

## 14. DOCUMENTOS DE REFERENCIA

| Documento | Ubicación | Para qué |
|-----------|-----------|----------|
| `HO_PJM_PLAN_SPRINTS_MEMORY_SERVICE.md` | `Release2.0/PJM/` | Lista completa de tareas por sprint con horas |
| `SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` | `Release2.0/01-PM/` | Detalles técnicos de cada tarea |
| `HANDOFF_PJM_SPRINT_SETUP_VTT.md` | `Release2.0/PJM/` | State actual VTT (Phase UUIDs, Agent UUIDs) |
| `HANDOFF_TL_SPRINT_MEM-S01.md` | `Release2.0/PJM/` | Brief técnico para ejecutar MEM-S01 (post-setup) |
| `METODOLOGIA_SETUP_FASE.md` | `00-agent-setup/templates/Handoff_proceso/` | Metodología de setup (leer antes) |
| `METODOLOGIA_SETUP_PLAN_VTT.md` | `00-agent-setup/templates/Handoff_proceso/` | Reglas del grafo de dependencias |

---

## 15. HISTORIAL

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | 2026-04-21 | PJM-Agent | Setup del bloque Development completo |

---

**FIN DEL SETUP BLOQUE DESARROLLO**
