# HANDOFF: PJM — Sprint Setup en VTT (ESTADO REAL)

**De:** PM (Martin Rivas)
**Para:** PJM (pjm@memory-service.vtt.ai)
**Fecha:** 2026-04-21
**Prioridad:** P0 CRITICO
**Proyecto:** Memory Service — MEM
**Version:** 3.0 (estado real post-setup VTT)

---

## 0. ESTADO ACTUAL DEL PROYECTO EN VTT

**YA ESTA HECHO (no rehacer):**
- Proyecto `Memory Service` creado en VTT (key `MEM`, release `Release 1 MVP`)
- 10 fases creadas con UUIDs reales (ver seccion 2)
- 73 deliveries creadas y distribuidas correctamente (ver seccion 3)
- 116 tareas creadas con IDs sequenciales `MEM-001` a `MEM-116` (ver seccion 7)

**NO HECHO — tu trabajo como PJM:**
1. Validar mapeo task -> delivery (las tareas estan creadas a nivel de fase, el link a delivery debe validarse)
2. Asignar `assigneeId` a cada tarea (agente responsable)
3. Ajustar `estimatedHours`, `complexity`, `category` si difieren del plan
4. Confirmar calendario de sprints y fechas de entrega por delivery
5. Crear dependencias entre tareas (MEM-032 -> MEM-033 -> etc.)

**IMPORTANTE:** El proyecto viejo con ID `a56a76e6-29bf-401e-a8ec-091882e383f7` fue borrado. Usa el nuevo ID en seccion 1.

---

## 1. DATOS DEL PROYECTO EN VTT

| Dato | Valor |
|------|-------|
| **Project ID** | `51e169f7-8a23-4628-8b78-04864b633ac7` |
| Project Key | MEM |
| API URL | http://77.42.88.106:3000 |
| Tu usuario | pjm@memory-service.vtt.ai |
| Tu UUID | 0ff63a29-0bc0-465a-b9bd-5f71476bc91d |
| SERVICE_KEY | hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d |
| Inicio | 2026-04-21 |
| Fin | 2026-07-31 |
| Sprint | 2 semanas |

### Autenticacion

```python
import urllib.request, json

BASE_URL = "http://77.42.88.106:3000"
PJM_ID   = "0ff63a29-0bc0-465a-b9bd-5f71476bc91d"
SK       = "hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d"

r = urllib.request.urlopen(urllib.request.Request(
    BASE_URL + "/api/auth/service-token",
    data=json.dumps({"userId": PJM_ID, "serviceKey": SK}).encode(),
    headers={"Content-Type": "application/json"}, method="POST"))
TOKEN = json.loads(r.read())["data"]["token"]
HEADERS = {"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"}
```

Estructura completa (Project ID, Phase UUIDs, Delivery UUIDs) ya guardada en:
`c:/Users/Martin/Documents/virtual-teams/memory-service/mem_structure.json`

---

## 2. PHASE IDs REALES EN VTT

| Order | Fase | Phase UUID |
|-------|------|-----------|
| 1 | **Project Setup** | `83f56bad-7e60-4ffa-bc19-9c0f9ba097a1` |
| 2 | Discovery | `3ee3a429-f836-45ea-afde-1753c78db9ac` |
| 3 | Planning | `a0dcfb69-b862-4784-b8c9-5aad233dfb9d` |
| 4 | Analysis | `26ecb1f6-1eb8-494f-930e-7e173c4ee559` |
| 5 | Design UX/UI | `2c8f0f2f-992a-46e5-b80f-9739180c2532` |
| 6 | Design Technical | `5f452a38-6cc6-4bbc-a8d5-1f50da2562af` |
| 7 | Development | `c2804591-b21c-4340-9065-59fd23e14b63` |
| 8 | Testing | `7ab83ed0-2238-4241-a915-8a957144d63e` |
| 9 | Deploy | `137d3082-f280-48da-81e7-abd3c1789f63` |
| 10 | Operations | `2ffc2179-2376-4197-93d1-56a878cd976e` |

---

## 3. DELIVERIES EN VTT (73 total)

Los delivery names en VTT NO llevan el prefijo `MEM-XXX`. Los IDs son UUIDs reales del backend.

### Project Setup (1 delivery)

| UUID | Name |
|------|------|
| `020d7a9e-1dec-47e9-b157-c138a2754188` | Project Foundation Ready |

Nota: Antes habia 5 deliveries tipo-tarea. Se consolidaron en 1. Las 5 tareas (MEM-001 a MEM-005) quedan bajo esta delivery unica.

### Discovery (2 deliveries)

| UUID | Name |
|------|------|
| `7e062012-8dc3-41c8-9db6-587bd522fae5` | Problem Definition |
| `46747b7f-5aa2-4224-b2f8-c5b7aa2fc695` | Value Proposition |

### Planning (6 deliveries)

| UUID | Name |
|------|------|
| `1553a1bb-bbb6-4001-a1bd-e55604fddf5f` | Vision & Objectives |
| `aad0f343-e275-4016-b05d-ddc668da4540` | Scope |
| `d43385a3-2af5-4360-9360-9027f7e5fc05` | Stakeholders |
| `beb200d7-ec93-440b-8e2e-315641fb817b` | Risks |
| `d81d0a16-fb85-42df-9840-10cf953dbf2b` | Timeline |
| `26231124-d702-4fbf-becf-b804e14f53ff` | Budget & Resources |

### Analysis (8 deliveries)

| UUID | Name |
|------|------|
| `6ac31b6c-490b-49cc-aedf-9d0d6bd7cbbc` | Functional Requirements |
| `cb635bb1-fd85-4c94-acba-1207f72cb033` | Non-Functional Requirements |
| `a5ebe11c-4989-4107-9ec7-6c4b15b2cb01` | Use Cases |
| `0cc1246e-8a2e-4d0e-95c6-bad1cb44c9d8` | User Stories |
| `ab5cd01a-b1a7-46ac-8c7d-415af03018b4` | Business Rules |
| `93ff3616-9750-4d3a-bae3-3618be821da9` | User Flows |
| `65e3a6e2-9296-4dc1-9f05-0e1c13879332` | Acceptance Criteria |
| `5d38464a-a2da-482f-8db7-d6a9c86560fa` | Traceability Matrix |

### Design UX/UI (6 deliveries)

| UUID | Name |
|------|------|
| `64487f12-0696-4e24-b973-39da1e3e25fd` | Personas |
| `335688d7-bb95-4223-a79d-ed53ad1bdc46` | Information Architecture |
| `171bb08d-10f8-49ad-a7c7-7b592924e2b4` | Wireframes |
| `d0429a60-066c-49e4-99ca-a234b757924c` | Mockups UI Design |
| `c07dbe80-389b-4b39-aaf6-0eda69063b73` | Design System |
| `ae0a6c01-644b-4063-9230-7670955390c7` | Design Handoff |

### Design Technical (9 deliveries)

| UUID | Name |
|------|------|
| `45a98395-2b39-412d-86f8-c38619e65808` | Solution Architecture |
| `876c7e9a-e9c3-4859-825b-4f24c16db0d5` | Code Architecture |
| `042828c8-d1e0-470c-904b-3acfb3afdafc` | Database Design |
| `f30e7d4d-bd75-46d5-9b9e-35e4d2648182` | API Design |
| `e05c0252-260a-48cc-bd48-e84030bd2771` | Sequence Diagrams |
| `9a52a704-e7e5-4df4-93e7-0c01a9b12937` | Architecture Decision Records |
| `60745748-e84d-4ca1-af44-ee936a1e678b` | Security Plan |
| `bb4bd482-ba4a-4435-ad78-67bf55ad6717` | Infrastructure Plan |
| `dc564fd8-8b98-435d-8048-781f1fefa3f2` | Technical Estimates |

### Development (14 deliveries: 6 BE sprints + 4 DL control + 4 UI)

| UUID | Name |
|------|------|
| `cdf64298-78a3-41f0-81ca-c6cc620b0e6b` | S01: Schema + Seeds |
| `6225b7f9-1c53-4d15-bf58-28356f5c2abe` | S02: Import + Timeline |
| `07fc4bb5-0bea-4ca3-b220-ec72f07b0d7f` | S03: Content + Context |
| `307fde68-d46e-4d27-b214-5a7578248cd3` | S04: Adapters + Cleanup |
| `91d5b816-a2e5-40c0-922d-7680cfffc18c` | S05: Lista + Cost + Dashboard |
| `07af8788-bf9d-4f79-9fdc-9f9b6991e5f5` | S06: Docker + Integration |
| `6c73db76-8951-4b82-bf1d-80eb3a8f774c` | DL-01: Design System + Dashboard (control) |
| `a745ef6d-61f0-4c7c-9682-78a87340318e` | DL-02: Conversation Viewer (control) |
| `23635818-fbaa-4cd2-9807-a9c4e3a9ced8` | DL-03: Import + Cost + Health (control) |
| `7a0b451f-f139-45d5-8c76-a76fa1647ae8` | DL-04: UX Spec + Handoff (control) |
| `a68364fb-f3c4-4a83-a781-73c07740f98c` | UI-01: Setup + Timeline + Viewer |
| `0faec639-adc7-4b54-8473-341304d675a0` | UI-02: Dashboard + Cost + Import |
| `40ac1259-720c-4fdc-bd0e-5e8a3034ec63` | UI-03: Viewer REVIEW + Lista |
| `06c47e49-0d9f-496c-b929-5426bdf03176` | UI-04: Cost Agente + Health |

### Testing (10 deliveries)

| UUID | Name |
|------|------|
| `69ab8133-76be-4651-9005-bef9a065e765` | Test Planning |
| `4c1c3824-ab69-48cf-8e37-733182f2ce12` | Test Cases |
| `2c8fdfc2-58cd-4e8e-a635-ef6a6e37ec6d` | Test Environment |
| `05201e04-8833-4f55-acfd-3d2911c1a4e7` | Functional Testing |
| `9d59355e-ffbe-43df-9c6d-cc730ddbb6d1` | Integration Testing |
| `b9cdfc52-6d4f-4322-8490-5f96c6035c9d` | E2E Testing |
| `cdb3747f-6f7c-4297-aef3-41bdd61de9b2` | Performance Testing |
| `41f0bd77-2a8d-439f-a649-37b4f97b86dc` | Security Testing |
| `8bcc3f68-8a41-40c8-b7ea-f1797dbd5a68` | UAT |
| `a7ab2609-725b-428c-afed-dca2540e8c03` | Bug Fixes |

### Deploy (7 deliveries)

| UUID | Name |
|------|------|
| `94655325-9812-48b3-898a-941773d043da` | Infrastructure Setup |
| `718394eb-b86e-47f5-b50c-d9a9f958df1a` | CI/CD Configuration |
| `84efdaa0-dbe7-4513-99e9-0708739e9bf6` | Staging Deploy |
| `cf1bf126-039b-4c6d-b069-7f4e036116b3` | Smoke Testing |
| `76051806-a2b9-4ec9-b9f4-961523cc4b97` | Production Deploy |
| `57291868-e1e2-4b62-bee1-5f20d49ad5a6` | Post-Deploy Monitoring |
| `d28a5a78-829e-4ea0-86ec-eee556e181bd` | Rollback Plan |

### Operations (6 deliveries)

| UUID | Name |
|------|------|
| `02ff2c77-8ea9-424c-b0db-077b819541d0` | Monitoring |
| `dfd61eca-7194-4835-b25f-51f9956c63e6` | User Support |
| `813c2946-4bb8-4f77-a7c3-e24061842b4f` | Bug Fixes Operations |
| `8cdde41d-147f-4e2c-b234-0952d560b614` | Incremental Improvements |
| `a8a4df88-cb3b-4ff8-af95-e25c3883693e` | Security Updates |
| `fdcf5a75-25b2-46f4-b260-3429a8f9f41b` | Scaling |

---

## 4. AGENTES Y UUIDs

| Sigla | Email | UUID |
|-------|-------|------|
| PM | pm@memory-service.vtt.ai | 350831b2-e1ae-4dbe-b2eb-7e023ec2e103 |
| PJM | pjm@memory-service.vtt.ai | 0ff63a29-0bc0-465a-b9bd-5f71476bc91d |
| TL | tl@memory-service.vtt.ai | 92225290-6b6b-4c1f-a940-dcb4262507aa |
| BE | backend@memory-service.vtt.ai | ebbe3cee-abed-4b3b-860d-0a81f632b08a |
| DB | database@memory-service.vtt.ai | 6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7 |
| FE | frontend@memory-service.vtt.ai | d23c9cd9-a156-433b-8900-94add5488eec |
| QA | qa@memory-service.vtt.ai | 613c9538-658c-45fe-a6d7-c1ea9ff04b78 |
| DO | devops@memory-service.vtt.ai | 322e3745-9756-4a7c-af11-44b33edef44d |
| DL | design-lead@memory-service.vtt.ai | b3a09269-cded-468c-a475-15a48f203cb0 |
| UX | ux@memory-service.vtt.ai | a75a1dae-754a-4b6f-a3ff-db8d51f6a91b |
| SA | sa@memory-service.vtt.ai | 0c128e3b-db3b-4e31-b107-0379b5791233 |
| AR | ar@memory-service.vtt.ai | e9403c25-c1f8-4b64-b2ef-f447d53115e2 |

### Prioridades VTT confirmadas

| Prioridad | UUID |
|-----------|------|
| medium | `d0b619ef-27e7-42d8-8879-41030a602eed` |
| high | `1a617554-6319-4c56-826f-8ef49a0ff9cc` |
| critical | `90ec3df2-fac4-40fa-b2ce-29daf0f4956e` |

---

## 5. CALENDARIO DE SPRINTS

| Sprint | Fechas | Deliveries activas |
|--------|--------|-------------------|
| Pre-Sprint | Apr 21 - Apr 24 | Project Foundation Ready (11h) |
| Sprint 0 | Apr 21 - May 04 | Discovery (2) + Planning (6) |
| Sprint 1 | May 05 - May 18 | Analysis (8) + Design Technical (9) |
| Sprint 2 | May 19 - Jun 01 | Design UX/UI: Personas, IA, Wireframes + DL-01 control + S01 |
| Sprint 3 | Jun 02 - Jun 15 | Design UX/UI: Mockups + Design Handoff + DL-02/03/04 + S02/S03 |
| Sprint 4 | Jun 16 - Jun 29 | S04, S05 + UI-01 |
| Sprint 5 | Jun 30 - Jul 13 | S06 + UI-02/03 + Testing (Test Planning, Cases, Functional, Integration) |
| Sprint 6 | Jul 14 - Jul 27 | UI-04 + Testing restante + Deploy |
| Post-MVP | Jul 28 - Jul 31 | Operations (6) |

---

## 6. API — PATRONES CONFIRMADOS Y GOTCHAS

### 6.1 POST task (crea task en una fase)

```
POST http://77.42.88.106:3000/api/phases/{phaseUUID}/tasks
Authorization: Bearer {TOKEN}
Content-Type: application/json

{
  "title": "Nombre de la tarea",
  "priorityId": "d0b619ef-27e7-42d8-8879-41030a602eed",
  "complexity": "MEDIUM",
  "category": "documentation",
  "estimatedHours": 3,
  "description": "..."
}
```

**Valores validos:**
- complexity: `LOW | MEDIUM | HIGH`
- category: `development | design | testing | documentation | review | bugfix | deployment`

### 6.2 PATCH task (actualizar campos)

```
PATCH /api/tasks/{taskId}
{
  "assigneeId": "UUID-del-agente",
  "estimatedHours": 4,
  "complexity": "HIGH",
  "priorityId": "..."
}
```

### 6.3 GOTCHAS CONFIRMADOS (IMPORTANTE)

1. **`POST /api/projects` ignora `deliverables[]`**: el array de deliverables en el body es SILENCIOSAMENTE ignorado. Deliveries deben crearse por endpoint dedicado.
2. **POST y PATCH task aceptan `deliveryId` pero NO lo persisten**: `GET /api/tasks/:id` no devuelve `deliveryId` ni `deliverableId`. Las tareas aparecen flotando a nivel de fase en la UI. **Validar con el PM si este comportamiento es intencional o si hay otro mecanismo para link task-delivery.**
3. **`POST /api/phases/:id/tasks` ignora `assigneeId` en el body**: usa PATCH posterior para asignar.
4. **GET deliveries naming inconsistency**: el POST usa path `/deliverables` pero el GET usa path `/deliveries`:
   - POST: `POST /api/projects/{projectId}/phases/{phaseId}/deliverables`
   - GET lista: `GET /api/phases/{phaseId}/deliveries`
   - GET uno: `GET /api/deliveries/{id}`
   - DELETE: `DELETE /api/deliveries/{id}`

### 6.4 Patron confirmado POST+PATCH

```python
# Paso 1: crear task en fase
r = call("POST", f"/api/phases/{phase_id}/tasks", {
    "title": ..., "priorityId": ..., "complexity": ..., "category": ..., "estimatedHours": ...
})
task_id = r["data"]["id"]  # e.g. "MEM-042"

# Paso 2: asignar agente
call("PATCH", f"/api/tasks/{task_id}", {"assigneeId": BE_UUID})
```

---

## 7. TAREAS YA CREADAS EN VTT (116 total)

**Las 116 tareas YA ESTAN CREADAS** con IDs sequenciales `MEM-001` a `MEM-116`. Tu trabajo es:
- Validar que title/complexity/category/estimatedHours coinciden con el plan
- Asignar `assigneeId` a cada una
- Validar el link a delivery (ver gotcha en seccion 6.3)

### 7.0 Project Setup — Tareas MEM-001 a MEM-005 (5 tareas, 11h)

Delivery: `Project Foundation Ready` (`020d7a9e-1dec-47e9-b157-c138a2754188`)

| Task ID | Titulo | Agente | Horas | Complexity | Category |
|---------|--------|--------|-------|------------|----------|
| MEM-001 | Inicializar repo git + estructura de carpetas (/src, /prisma, /knowledge, /_project-management) | DO | 2 | MEDIUM | deployment |
| MEM-002 | Crear TASK_TRACKING.md local con las 116 tareas | PJM | 2 | LOW | documentation |
| MEM-003 | Copiar templates TEMPLATE_CODE_LOGIC.md y TEMPLATE_DEVELOPMENT_LOG.md | PJM | 1 | LOW | documentation |
| MEM-004 | Crear .env.example, .gitignore, docker-compose.yml base (Postgres local) | DO | 2 | MEDIUM | deployment |
| MEM-005 | Redactar briefs iniciales por tarea en /_project-management/briefs/ | PM | 4 | MEDIUM | documentation |

### 7.1 Discovery — Tareas MEM-006 a MEM-009 (4 tareas, 9h)

| Task ID | Titulo | Agente | Horas | Delivery target |
|---------|--------|--------|-------|----------------|
| MEM-006 | Definir problema central y pain points | SA | 3 | Problem Definition |
| MEM-007 | Entrevistas con stakeholders | PM | 2 | Problem Definition |
| MEM-008 | Redactar Value Proposition Canvas | SA | 3 | Value Proposition |
| MEM-009 | Validar propuesta con PM | PM | 1 | Value Proposition |

### 7.2 Planning — Tareas MEM-010 a MEM-017 (8 tareas, 23h)

| Task ID | Titulo | Agente | Horas | Delivery target |
|---------|--------|--------|-------|----------------|
| MEM-010 | Documentar Vision y Mission del proyecto | PM | 3 | Vision & Objectives |
| MEM-011 | Definir OKRs del MVP | PM | 2 | Vision & Objectives |
| MEM-012 | Definir In-Scope y Out-of-Scope | SA | 4 | Scope |
| MEM-013 | Mapa de stakeholders y RACI | PJM | 2 | Stakeholders |
| MEM-014 | Registro de riesgos y mitigaciones | PJM | 3 | Risks |
| MEM-015 | Roadmap y calendario de sprints | PJM | 4 | Timeline |
| MEM-016 | Estimacion de horas por rol | PJM | 3 | Timeline |
| MEM-017 | Definir presupuesto de computo | PM | 2 | Budget & Resources |

### 7.3 Analysis — Tareas MEM-018 a MEM-025 (8 tareas, 41h)

| Task ID | Titulo | Agente | Horas | Delivery target |
|---------|--------|--------|-------|----------------|
| MEM-018 | Levantamiento de Req. Funcionales | SA | 6 | Functional Requirements |
| MEM-019 | Req. No Funcionales (performance <500ms) | AR | 4 | Non-Functional Requirements |
| MEM-020 | Diagramas de Casos de Uso | SA | 5 | Use Cases |
| MEM-021 | Epics y User Stories (Gherkin) | SA | 8 | User Stories |
| MEM-022 | Reglas de Negocio (idempotencia, cleanup) | TL | 4 | Business Rules |
| MEM-023 | User Flows para cada actor | UX | 4 | User Flows |
| MEM-024 | Criterios de Aceptacion por US | SA | 6 | Acceptance Criteria |
| MEM-025 | Matriz de Trazabilidad US vs Req | SA | 4 | Traceability Matrix |

### 7.4 Design UX/UI — Tareas MEM-026 a MEM-038 (13 tareas, 35h)

| Task ID | Titulo | Agente | Horas | Delivery target |
|---------|--------|--------|-------|----------------|
| MEM-026 | Fichas de Personas (agentes + admin) | UX | 3 | Personas |
| MEM-027 | Sitemap y arquitectura de informacion | UX | 4 | Information Architecture |
| MEM-028 | Design System tokens (colores, tipografia, espaciado) | DL | 3 | Design System |
| MEM-029 | Wireframes Dashboard (stats, actividad reciente) | DL | 4 | Wireframes |
| MEM-030 | Wireframes Agent Timeline (cronologia conversaciones) | DL | 3 | Wireframes |
| MEM-031 | Wireframes Conversation Viewer modo TASK | DL | 4 | Wireframes / Mockups |
| MEM-032 | Wireframes Conversation Viewer modo REVIEW | DL | 4 | Wireframes / Mockups |
| MEM-033 | Wireframes Import Manual | DL | 2 | Wireframes |
| MEM-034 | Wireframes Cost Reports (proyecto y agente) | DL | 2 | Wireframes |
| MEM-035 | Wireframes Lista/Busqueda conversaciones | DL | 2 | Wireframes |
| MEM-036 | Wireframes Health page | DL | 1 | Wireframes |
| MEM-037 | Documento UX Spec completo (9 pantallas, estados, flows) | DL | 2 | Design Handoff |
| MEM-038 | Handoff a FE (assets exportados, specs, tokens) | DL | 1 | Design Handoff |

**HITO: MEM-038 completado = FE puede iniciar.**

### 7.5 Design Technical — Tareas MEM-039 a MEM-047 (9 tareas, 45h)

| Task ID | Titulo | Agente | Horas | Delivery target |
|---------|--------|--------|-------|----------------|
| MEM-039 | Diagrama de arquitectura de solucion | TL | 6 | Solution Architecture |
| MEM-040 | Estructura de carpetas y patrones | TL | 4 | Code Architecture |
| MEM-041 | Diseno de BD (tablas, indices, relaciones) | DB | 6 | Database Design |
| MEM-042 | OpenAPI Spec (todos los endpoints) | BE | 8 | API Design |
| MEM-043 | Diagramas de secuencia (flujos criticos) | AR | 6 | Sequence Diagrams |
| MEM-044 | ADRs (decisiones de arquitectura) | TL | 4 | Architecture Decision Records |
| MEM-045 | Plan de Seguridad (auth, secrets, RBAC) | AR | 4 | Security Plan |
| MEM-046 | Plan de Infraestructura (Hetzner, Docker) | DO | 4 | Infrastructure Plan |
| MEM-047 | Estimaciones tecnicas finales por sprint | TL | 3 | Technical Estimates |

### 7.6 Development — Tareas MEM-048 a MEM-093 (46 tareas, 116h)

#### MEM-048 a MEM-052 → delivery `S01: Schema + Seeds` (9h)
| Task ID | Titulo | Agente | Horas |
|---------|--------|--------|-------|
| MEM-048 | Crear schema Prisma completo (19 tablas, 10 catalogos) | DB | 3 |
| MEM-049 | Migraciones + partial indexes (SQL manual) | DB | 2 |
| MEM-050 | Seed catalogos (sources, statuses, topics, workTypes) | DB | 1 |
| MEM-051 | Setup proyecto Express + estructura carpetas | BE | 2 |
| MEM-052 | Catalog cache en startup (prefetch para evitar N+1) | BE | 1 |

#### MEM-053 a MEM-057 → delivery `S02: Import + Timeline` (12h)
| Task ID | Titulo | Agente | Horas |
|---------|--------|--------|-------|
| MEM-053 | POST /api/conversations/import (source CLAUDE_SDK, idempotencia P2002) | BE | 4 |
| MEM-054 | Parser JSONL + validacion + externalSessionId format | BE | 2 |
| MEM-055 | Clasificacion por reglas (topics por keywords, workType por agentRole) | BE | 3 |
| MEM-056 | GET /api/agents/:agentId/timeline | BE | 2 |
| MEM-057 | Storage contenido completo en filesystem + contentPreview en BD | BE | 1 |

#### MEM-058 a MEM-062 → delivery `S03: Content + Context` (12h)
| Task ID | Titulo | Agente | Horas |
|---------|--------|--------|-------|
| MEM-058 | GET /api/conversations/:id/content (messages parseados) | BE | 2 |
| MEM-059 | GET /api/context (JSON estructurado, fail-fast, sin transformar) | BE | 4 |
| MEM-060 | Optimizacion <500ms con indices parciales + prefetch statusId | BE | 2 |
| MEM-061 | Tests rendimiento GET /context (10/100/1000 convs, 50 concurrent) | QA | 2 |
| MEM-062 | Tests unitarios import + clasificacion | QA | 2 |

#### MEM-063 a MEM-068 → delivery `S04: Adapters + Cleanup` (12h)
| Task ID | Titulo | Agente | Horas |
|---------|--------|--------|-------|
| MEM-063 | POST /api/conversations/import-review (prefetch catalogs) | BE | 3 |
| MEM-064 | Adapter Claude Web (JSON export de claude.ai) | BE | 2 |
| MEM-065 | Adapter ChatGPT (JSON export) | BE | 2 |
| MEM-066 | Cleanup job por statusId (catch delega siempre, max 3 retries) | BE | 2 |
| MEM-067 | Retry logic con log de acciones | BE | 1 |
| MEM-068 | Tests unitarios cada adapter + cleanup logic | BE | 2 |

#### MEM-069 a MEM-074 → delivery `S05: Lista + Cost + Dashboard` (11h)
| Task ID | Titulo | Agente | Horas |
|---------|--------|--------|-------|
| MEM-069 | GET /api/conversations (lista, filtros, paginacion) | BE | 2 |
| MEM-070 | GET /api/projects/:id/cost-report (sumas tokens + costos 6 decimales) | BE | 2 |
| MEM-071 | GET /api/agents/:id/cost-report (breakdown por workType) | BE | 2 |
| MEM-072 | GET /api/dashboard (stats globales + actividad reciente) | BE | 2 |
| MEM-073 | POST /api/conversations/upload (import manual) | BE | 2 |
| MEM-074 | GET /health (BD, storage, cache status) | BE | 1 |

#### MEM-075 a MEM-080 → delivery `S06: Docker + Integration` (14h)
| Task ID | Titulo | Agente | Horas |
|---------|--------|--------|-------|
| MEM-075 | Dockerfile + docker-compose.yml (puerto 3002/3003) | DO | 2 |
| MEM-076 | Deploy a VM Hetzner 77.42.88.106 | DO | 2 |
| MEM-077 | Configuracion nginx/traefik reverse proxy | DO | 1 |
| MEM-078 | Integracion Hook Manager VTT (externalSessionId={run_id}:r{N}:{role}) | BE | 4 |
| MEM-079 | Tests E2E flujo completo SDK->import->context | QA | 3 |
| MEM-080 | Tests integracion Runtime v1.1 (platformRefs, source CLAUDE_SDK) | QA | 2 |

#### MEM-081 a MEM-085 → delivery `UI-01: Setup + Timeline + Viewer` (16h)
**DEPENDENCIA CRITICA: MEM-038 (Design Handoff) debe estar COMPLETADO.**

| Task ID | Titulo | Agente | Horas |
|---------|--------|--------|-------|
| MEM-081 | Setup React + Vite + TailwindCSS | FE | 2 |
| MEM-082 | Configuracion API client (base URL, interceptors) | FE | 1 |
| MEM-083 | Agent Timeline component (cronologia de conversaciones) | FE | 5 |
| MEM-084 | Conversation Viewer modo TASK (mensajes + metadata) | FE | 6 |
| MEM-085 | Routing + layout base (nav, sidebar, breadcrumbs) | FE | 2 |

#### MEM-086 a MEM-088 → delivery `UI-02: Dashboard + Cost + Import` (12h)
| Task ID | Titulo | Agente | Horas |
|---------|--------|--------|-------|
| MEM-086 | Dashboard page (stats, graficas, actividad reciente) | FE | 4 |
| MEM-087 | Cost Report Proyecto page (tabla + breakdown) | FE | 4 |
| MEM-088 | Import Manual page (upload + preview + submit) | FE | 4 |

#### MEM-089 a MEM-090 → delivery `UI-03: Viewer REVIEW + Lista` (10h)
| Task ID | Titulo | Agente | Horas |
|---------|--------|--------|-------|
| MEM-089 | Conversation Viewer modo REVIEW (anotaciones, diff) | FE | 5 |
| MEM-090 | Lista conversaciones + busqueda + filtros avanzados | FE | 5 |

#### MEM-091 a MEM-093 → delivery `UI-04: Cost Agente + Health` (8h)
| Task ID | Titulo | Agente | Horas |
|---------|--------|--------|-------|
| MEM-091 | Cost Report Agente page | FE | 3 |
| MEM-092 | Health page (estado BD, storage, servicios) | FE | 2 |
| MEM-093 | Estados globales: loading, empty, error (componentes reutilizables) | FE | 3 |

### 7.7 Testing — Tareas MEM-094 a MEM-103 (10 tareas, 60h)

| Task ID | Titulo | Agente | Horas | Delivery target |
|---------|--------|--------|-------|----------------|
| MEM-094 | Plan de pruebas completo | QA | 4 | Test Planning |
| MEM-095 | Casos de prueba funcionales | QA | 8 | Test Cases |
| MEM-096 | Configurar entorno QA en Hetzner | DO | 4 | Test Environment |
| MEM-097 | Ejecucion pruebas funcionales | QA | 8 | Functional Testing |
| MEM-098 | Pruebas de integracion Runtime | QA | 6 | Integration Testing |
| MEM-099 | Pruebas E2E flujo completo | QA | 8 | E2E Testing |
| MEM-100 | Pruebas de performance (<500ms) | QA | 6 | Performance Testing |
| MEM-101 | Pruebas de seguridad | AR | 4 | Security Testing |
| MEM-102 | UAT con usuarios clave | PM | 4 | UAT |
| MEM-103 | Correccion de bugs encontrados | BE | 8 | Bug Fixes |

### 7.8 Deploy — Tareas MEM-104 a MEM-110 (7 tareas, 26h)

| Task ID | Titulo | Agente | Horas | Delivery target |
|---------|--------|--------|-------|----------------|
| MEM-104 | Configurar VM Hetzner para produccion | DO | 4 | Infrastructure Setup |
| MEM-105 | Pipeline CI/CD (GitHub Actions) | DO | 6 | CI/CD Configuration |
| MEM-106 | Deploy a Staging y smoke tests | DO | 4 | Staging Deploy |
| MEM-107 | Smoke Testing en Staging | QA | 3 | Smoke Testing |
| MEM-108 | Deploy a Produccion (puerto 3002/3003) | DO | 4 | Production Deploy |
| MEM-109 | Configurar alertas y dashboards | DO | 3 | Post-Deploy Monitoring |
| MEM-110 | Documentar plan de rollback | TL | 2 | Rollback Plan |

### 7.9 Operations — Tareas MEM-111 a MEM-116 (6 tareas, 15h)

| Task ID | Titulo | Agente | Horas | Delivery target |
|---------|--------|--------|-------|----------------|
| MEM-111 | Configurar monitoreo continuo | DO | 3 | Monitoring |
| MEM-112 | Documentar soporte de usuarios | PM | 2 | User Support |
| MEM-113 | Proceso de gestion de bugs en produccion | TL | 2 | Bug Fixes Operations |
| MEM-114 | Roadmap de mejoras post-MVP | PM | 3 | Incremental Improvements |
| MEM-115 | Schedule de actualizaciones de seguridad | AR | 2 | Security Updates |
| MEM-116 | Plan de escalabilidad horizontal | AR | 3 | Scaling |

---

## 8. RESUMEN DE HORAS

| Fase | Tareas | Horas |
|------|--------|-------|
| Project Setup | 5 | 11 |
| Discovery | 4 | 9 |
| Planning | 8 | 23 |
| Analysis | 8 | 41 |
| Design UX/UI | 13 | 35 |
| Design Technical | 9 | 45 |
| Development | 46 | 116 |
| Testing | 10 | 60 |
| Deploy | 7 | 26 |
| Operations | 6 | 15 |
| **TOTAL** | **116** | **381** |

### Por rol

| Rol | Horas estimadas |
|-----|-----------------|
| PM | ~24h |
| PJM | ~15h |
| SA | ~36h |
| TL | ~25h |
| AR | ~23h |
| DB | ~12h |
| BE | ~74h |
| DL | ~28h |
| UX | ~11h |
| FE | ~46h |
| QA | ~54h |
| DO | ~33h |
| **TOTAL** | **~381h** |

---

## 9. DEPENDENCIAS CRITICAS

```
Phase 1 (Project Setup) -> Phase 2 (Discovery) -> Phase 3 (Planning) -> Phase 4 (Analysis)
                                                                              |
                                                                              v
                                     Phase 5 (Design UX/UI)  ==  Phase 6 (Design Technical)  [paralelo]
                                                 |
                                                 v
                                         MEM-038 (Design Handoff)  [HITO]
                                                 |
                                                 v
                      Phase 7 BE: MEM-048..052 -> MEM-053..057 -> MEM-058..062 -> MEM-063..068 -> MEM-069..074 -> MEM-075..080
                      Phase 7 FE: (desde MEM-038)                                  MEM-081..085 -> MEM-086..088 -> MEM-089..090 -> MEM-091..093
                                                 |
                                                 v
                                         Phase 8 (Testing)
                                                 |
                                                 v
                                         Phase 9 (Deploy)
                                                 |
                                                 v
                                        Phase 10 (Operations)
```

- MEM-078 depende de Hook Manager VTT operativo
- FE (MEM-081+) NO puede iniciar sin MEM-038 completado
- DL puede correr en paralelo con 3B y con MEM-048..057 de BE desde Sprint 2

---

## 10. CHECKLIST PJM (trabajo pendiente)

### Paso 1 — Validar creacion de tareas
- [ ] GET `/api/projects/51e169f7-8a23-4628-8b78-04864b633ac7` → `tasksCount = 116`
- [ ] Revisar que cada fase tenga las tareas correctas (cantidades en seccion 8)

### Paso 2 — Asignar agentes (PATCH assigneeId)
- [ ] Phase 1 Project Setup: MEM-001..005
- [ ] Phase 2 Discovery: MEM-006..009
- [ ] Phase 3 Planning: MEM-010..017
- [ ] Phase 4 Analysis: MEM-018..025
- [ ] Phase 5 Design UX/UI: MEM-026..038
- [ ] Phase 6 Design Technical: MEM-039..047
- [ ] Phase 7 Development: MEM-048..093
- [ ] Phase 8 Testing: MEM-094..103
- [ ] Phase 9 Deploy: MEM-104..110
- [ ] Phase 10 Operations: MEM-111..116

### Paso 3 — Validar mapeo task-delivery
- [ ] Confirmar con PM si el API actualmente NO soporta asignar task a delivery (GET task no devuelve deliveryId)
- [ ] Si se habilita: ejecutar PATCH `deliveryId` por cada task segun tabla seccion 7
- [ ] Si no: documentar como issue y mantener tareas a nivel de fase

### Paso 4 — Ajustar complexity/hours si difieren
- [ ] Comparar cada task con seccion 7 — si complexity/category/estimatedHours difiere, PATCH

### Paso 5 — Crear dependencias
- [ ] MEM-081 depende de MEM-038 (HITO)
- [ ] MEM-053 depende de MEM-048..052 (S02 depende de S01)
- [ ] MEM-058 depende de MEM-053..057 (S03 depende de S02)
- [ ] (etc. — ver seccion 9)

### Paso 6 — Calendario
- [ ] Confirmar fechas de Sprint 0..6 segun seccion 5
- [ ] Setear `startDate` / `endDate` por delivery si el API lo soporta

### Paso 7 — Reportar al PM
- [ ] Resumen de asignaciones
- [ ] Lista de issues encontrados (especialmente el del link task-delivery)
- [ ] Listo para kickoff

---

## 11. DOCUMENTOS DE REFERENCIA

- `Release2.0/01-PM/HANDOFF_PJM_MEMORY_SERVICE_2026-04-15.md` — Plan original aprobado 150h
- `Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` — Spec tecnica completa
- `Release2.0/02-AR/AR_REVIEW_SPEC_MEMORY_SERVICE_v1.md` — Arquitectura aprobada
- `Release2.0/03-DB/DB_REVIEW_SPEC_MEMORY_SERVICE_v1.md` — DB schema aprobado
- `Release2.0/04-TL/TL_REVIEW_SPEC_MEMORY_SERVICE_v1.md` — Tech lead observaciones
- `Release2.0/PJM/HO_PJM_PLAN_SPRINTS_MEMORY_SERVICE.md` — Detalle tareas ANALISIS
- `Release2.0/PJM/SETUP_MEM.md` — Detalle IDs internos Development
- `Release2.0/PJM/CLOSURE_MEM_SPRINTS.md` — Templates cierre por sprint
- `c:/Users/Martin/Documents/virtual-teams/memory-service/mem_structure.json` — UUIDs en vivo (project, phases, deliveries)
- `c:/Users/Martin/Documents/virtual-teams/memory-service/memory-service-project/00-agent-setup/operating-core/MANUAL_USUARIO_AGENTE_MODELO_DINAMICO_V4.md` — Manual agente con gotchas reales

---

**Estado:** Proyecto creado en VTT. Pendiente: asignar agentes, validar link task-delivery, crear dependencias.
**Siguiente:** PJM ejecuta checklist seccion 10 y reporta al PM.
