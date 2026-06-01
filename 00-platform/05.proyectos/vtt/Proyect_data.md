# Datos del Proyecto VTT (Virtual Teams Tracking)

| Campo | Valor |
|---|---|
| **Proyecto** | Virtual Teams Tracking (VTT) |
| **Project Key** | VTT |
| **Project UUID** | `d837bcd5-3f10-4e19-a418-344a1eef98ad` |
| **Repo** | https://github.com/NCoreSys/virtual-teams-tracking.git |
| **Branch principal** | `main` |
| **Backend (prod)** | http://77.42.88.106:3000 |
| **Swagger** | http://77.42.88.106:3000/api-docs |
| **PM** | Martin Rivas — `pm@vtt.com` |
| **TL** | Claude (Tech Lead) — `tech.lead@vtt.ai` |
| **Última actualización** | 2026-05-28 |
| **Verificado contra API** | Sí — `GET /api/users` 2026-05-28 |

---

## 1. Equipo VTT — Emails y UUIDs

### Coordinación y Gestión

| Rol | Nombre | Email | UUID |
|---|---|---|---|
| PM | Martin Rivas | `pm@vtt.com` | `07a07147-cf5a-4117-8fbd-2fd1ccb95d54` |
| Tech Lead | Claude (Tech Lead) | `tech.lead@vtt.ai` | `abdff0db-ad0b-4a0c-99f5-c898d18bd2d8` |
| PJM | Project Manager | `project.manager@vtt.ai` | `49937318-7a1d-4b83-9b7e-81aa49394d92` |
| PM (Product) | Product Manager | `product.manager@vtt.ai` | `07395164-eeb8-4ef8-9600-70f2f89c2b24` |
| Program Manager | Program Manager | `program.manager@vtt.ai` | `c6e012c7-de80-4d37-b375-f9a2d6abdec7` |
| PO | Product Owner | `product.owner@vtt.ai` | `4128b577-eec1-4bc2-a595-42bd6b43db5e` |

### Desarrollo

| Rol | Nombre | Email | UUID |
|---|---|---|---|
| Backend Engineer #1 | Backend API Specialist | `backend.dev@vtt.ai` | `8834830b-578f-46be-933b-0abcbbc5da99` |
| Backend Engineer #2 | Backend API Specialist #2 | `backend.dev2@vtt.ai` | `008cacfc-d0cb-41d2-8628-def9571f8c77` |
| Database Engineer | Database Engineer | `db.engineer@vtt.ai` | `a3a2ce62-28d8-419d-9888-44203a963894` |
| DevOps Engineer | DevOps Engineer | `devops@vtt.ai` | `b2e00b9d-a657-4bdb-b982-3dcf1f5b5757` |
| Frontend Dev #1 | Frontend Dev #1 | `frontend.dev1@vtt.ai` | `84ad0fbe-996d-4aa7-abf6-57d64d4671de` |
| Frontend Dev #2 | Frontend Dev #2 | `frontend.dev2@vtt.ai` | `9b8d927e-0013-4291-850d-bff968b37c84` |

### Análisis y QA

| Rol | Nombre | Email | UUID |
|---|---|---|---|
| Solution Analyst | Systems Analyst | `systems.analyst@vtt.ai` | `becdf45a-039b-4e8f-8c83-09f473a914a8` |
| QA Engineer #1 | QA Engineer | `qa.engineer@vtt.ai` | `1d8eb958-aef7-42f4-ba30-1a7d33a60d39` |
| QA Engineer #2 | QA Engineer #2 | `qa.engineer2@vtt.ai` | `40aea495-5129-4d40-bf10-86f448329f1a` |
| Architect (AR) | Auditor Reviewer | `auditor.reviewer@vtt.ai` | `9cc9e322-3c36-4823-af2e-78d13f5b895b` |
| Integration Reviewer | Integration Reviewer | `integration.reviewer@vtt.ai` | `fbef6ae6-ba0d-43ce-8cc1-2f28c9c6346d` |
| Integration Auditor | Integration Auditor | `integration.auditor@vtt.ai` | `f294a61d-ffcd-411f-9f24-3adcccae446b` |

### Diseño

| Rol | Nombre | Email | UUID |
|---|---|---|---|
| Design Lead | Design Lead | `design.lead@vtt.ai` | `ebf0f384-51ba-49f5-8e98-fa7569ce1d31` |
| UX Designer | UX Designer | `ux.designer@vtt.ai` | `ce8a2ace-21cb-44e9-978b-aa5f45977478` |

### Sistema

| Rol | Nombre | Email | UUID |
|---|---|---|---|
| System | System | `system@vtt.ai` | `5cbfc67f-50ba-4ece-910d-2011aa6241ac` |

---

## 2. Service Key

```
hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d
```

> Misma clave que memory-service. Se usa para obtener JWT vía `POST /api/auth/service-token` (body: `{userId, serviceKey}`). Token válido 30 días.

---

## 3. UUIDs de Status (Task lifecycle)

| Code | Name | UUID | Order |
|---|---|---|---|
| task_created | Created | `0e54089b-296a-4d80-bcd3-80a7a71f1696` | 1 |
| task_pending | Pending | `335fd9c6-f0d6-4966-a6ea-f518c78bc422` | 2 |
| task_in_progress | In Progress | `2a76888a-e595-4cfc-ac4c-a3ae5087ef56` | 3 |
| task_in_review | In Review | `1ec975a5-7581-4a1a-ab8f-51b1a7ef868d` | 4 |
| task_completed | Completed | `aa5ceb90-5209-42a2-b874-a8cbee597a97` | 5 |
| task_approved | Approved | `b9ca4951-6e14-4d82-b1d8-440793bbaf47` | 6 |
| task_blocked | Blocked | `c897cbd6-99b9-4640-a760-e0056384fae5` | 7 |
| task_on_hold | On Hold | `c62eb334-b7bc-4c9f-af85-a5666c262aaa` | 8 |
| task_rejected | Rejected | `eb264e77-4c1d-40d1-a3af-e6cd8f402205` | 9 |
| task_cancelled | Cancelled | `b9488db1-2969-43aa-b804-3fcb49f355a4` | 10 |

---

## 4. UUIDs de Prioridad

| Prioridad | UUID |
|---|---|
| critical | `90ec3df2-fac4-40fa-b2ce-29daf0f4956e` |
| high | `1a617554-6319-4c56-826f-8ef49a0ff9cc` |
| medium | `d0b619ef-27e7-42d8-8879-41030a602eed` |
| low | `95f2e731-41b9-4a7d-9a43-31f00a4ddd7e` |

---

## 5. Stack Técnico

### Frontend
- React 18 + TypeScript + Vite + TailwindCSS + Recharts
- Router: `frontend/src/router/index.tsx`
- Tokens: `frontend/src/index.css`
- Iconos: `lucide-react`
- Auth FE: `useAuth()` → `user.id`

### Backend
- Node.js + Express + TypeScript + Prisma ORM + PostgreSQL + MinIO
- Auth: JWT (obligatorio desde VTT-296 / LL-006)
- Middleware permisos: `authorization.middleware.ts`, `context.middleware.ts`

### Infra
- Docker: `vtt-backend`, `shared-postgres`
- VM: `http://77.42.88.106:3000`

---

## 6. Modelo de dos repos — Normativa vs Operativa

> **Regla:** El agente VTT consulta documentos de DOS repos según la naturaleza del documento.

### Repo `virtual-teams-setup/` — Normativa
**Cómo se hacen las cosas.** Genérico y reutilizable entre proyectos.

| Categoría | Path canónico |
|-----------|---------------|
| Datos del equipo VTT (este archivo) | `00-platform/05.proyectos/vtt/Proyect_data.md` |
| Operativos por rol | `00-platform/05.proyectos/vtt/operativos-instancias/` |
| Perfiles base genéricos | `00-platform/01.agents/roles/` |
| Setups / INIT genéricos | `00-platform/01.agents/setups/` + `00-platform/01.agents/init-messages/` |
| Protocols (procesos completos) | `00-platform/02.normativa/01.Protocols/` |
| Reglas Nivel 0 (catálogo de 47 reglas) | `00-platform/02.normativa/00.Rules/rules_catalog.json` |
| Skills (capacidades reusables) | `00-platform/02.normativa/03.Skills/` |
| Scripts canónicos | `00-platform/02.normativa/04.Scripts/` |
| Templates BRIEF / ASSIGNMENT / devlog / code_logic | `00-platform/03.templates/tarea/` |
| Templates Handoff / Methodologies | `00-platform/03.templates/handoff/` |
| Templates Specs UI/UX | `00-platform/03.templates/specs-design/` |
| Guías operativas | `00-platform/04.docs-soporte/guias-operativas/` |

### Repo `virtual-teams-tracking/` — Operativa
**Qué se está haciendo en VTT específicamente.** Datos vivos del trabajo en curso.

| Categoría | Path |
|-----------|------|
| Estado del proyecto / sprint | `knowledge/tl-docs/CONTEXTO_TECH_LEAD_SESION.md` |
| Procedimientos operativos agentes (a migrar) | `knowledge/PROCEDIMIENTOS_OPERATIVOS_AGENTES.md` |
| BRIEFs generados | `knowledge/agent-tasks/briefs/` |
| ASSIGNMENTs generados | `knowledge/agent-tasks/assignments/` |
| Development logs | `knowledge/development-log/` |
| Code logic (espejo de src/) | `knowledge/code-logic/` |
| HTMLs del UX | `knowledge/design/screens/` |
| Reportes del PJM | `knowledge/reports/` |
| SPECs y handoffs del PM | `_project-management/` |
| Schema BD | `backend/prisma/schema.prisma` |
| Migrations | `backend/prisma/migrations/` |
| Backend code | `backend/src/` |
| Frontend code | `frontend/src/` |

### Regla de decisión rápida

```
¿El documento es genérico/reutilizable entre proyectos?
  SÍ → virtual-teams-setup/00-platform/...
  NO → virtual-teams-tracking/...

¿Es estado vivo del trabajo en curso?
  SÍ → virtual-teams-tracking/
  NO (es plantilla, perfil, regla, proceso) → virtual-teams-setup/
```

---

## 7. Carga de contexto del agente

### Capa 1 — Auto-cargado en cada sesión
- `MEMORY.md` (auto-memory del proyecto VTT)
- `rules_agents.instructions.md` (reglas globales transversales)
- `OPERATIVO_<ROL>_VTT.md` (.claude/agents/...) — perfil del rol activo

### Capa 2 — El agente lee manualmente al iniciar

**Normativa (virtual-teams-setup):**
- `00-platform/05.proyectos/vtt/Proyect_data.md` — este archivo
- `00-platform/05.proyectos/vtt/operativos-instancias/OPERATIVO_<MI_ROL>.md` — mi operativo VTT
- `00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-ASG-001_*.md` — ciclo asignación
- `00-platform/01.agents/onboarding/01_ONBOARDING.md` + `02_OPERACION_AGENTE.md`

**Operativa (virtual-teams-tracking):**
- `knowledge/tl-docs/CONTEXTO_TECH_LEAD_SESION.md` (estado del sprint actual)
- `GET /api/tasks?assigneeId=<UUID_AGENTE>` — mis tareas asignadas

### Capa 3 — Específico por tarea (API VTT)
- `BRIEF_VTT-XXX_*.md` (attachment de la tarea)
- `ASSIGNMENT_VTT-XXX_*.md` (attachment de la tarea)
- Mensaje del agente (comentario en la tarea con curls de status y datos)

---

## 8. Comandos rápidos

### Obtener JWT (requerido para mutations desde VTT-296)

```bash
python3 -c "
import urllib.request, json, sys
req = urllib.request.Request(
    'http://77.42.88.106:3000/api/auth/service-token',
    data=json.dumps({'userId': 'UUID_AGENTE', 'serviceKey': 'hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d'}).encode(),
    headers={'Content-Type': 'application/json'}, method='POST')
with urllib.request.urlopen(req) as r:
    sys.stdout.write(json.loads(r.read())['data']['token'])
"
```

### Validar usuarios del sistema

```bash
curl -s "http://77.42.88.106:3000/api/users" | python3 -m json.tool
```

### Validar status disponibles

```bash
curl -s "http://77.42.88.106:3000/api/catalogs/status?process=task"
```

---

## 9. Diferencias con Memory Service

VTT y Memory Service son **proyectos distintos** dentro de la misma plataforma. Roles que existen en VTT pero NO en Memory Service:

- **Product Owner (PO)** — `product.owner@vtt.ai`
- **Program Manager** — `program.manager@vtt.ai`
- **Product Manager** (separado del PM coordinador) — `product.manager@vtt.ai`
- **Integration Auditor** (separado de Integration Reviewer) — `integration.auditor@vtt.ai`
- **Backend #2 / QA #2 / Frontend #2** — recursos duplicados por carga

Roles que existen en Memory Service pero NO en VTT (no creados todavía):

- CIA (Competitive Intelligence Analyst)
- MRA (Market Research Analyst)
- PSA (Product Strategy Analyst)
- FA (Financial Analyst)
- SEC (Security Engineer)
- SRE (Site Reliability Engineer)
- TW (Technical Writer)
- QAA (QA Automation)
- PTE (Performance Test Engineer)
- UXR (UX Researcher)

> Si VTT requiere alguno de estos roles, crear el usuario en el sistema antes de generar el `OPERATIVO_<ROL>_VTT.md` correspondiente.

---

## 10. Validación

Para revalidar este documento contra el sistema:

```bash
# 1. Listar usuarios @vtt.ai / @vtt.com
curl -s "http://77.42.88.106:3000/api/users" | \
  python3 -c "import sys,json; users=json.load(sys.stdin)['data']; print('\n'.join(f\"{u['role']:30} {u['email']:40} {u['id']}\" for u in users if '@vtt.ai' in u['email'] or '@vtt.com' in u['email']))"

# 2. Verificar que cada UUID de esta tabla existe
# (si un email cambia o un usuario se desactiva, actualizar este doc)
```

---

**Mantenedor:** TL VTT (Claude — `tech.lead@vtt.ai`)
**Cambios:** vía PR al repo `virtual-teams-setup/` (cuando esté en git)
