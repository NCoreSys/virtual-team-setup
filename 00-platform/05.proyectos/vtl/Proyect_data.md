# Datos del Proyecto VTL (VTT Agent Landing)

| Campo | Valor |
|---|---|
| **Proyecto** | VTT Agent Landing Page |
| **Project Key** | `VTTL` |
| **Project UUID** | `7e460b63-a3b0-4ce5-9d21-b88cf38748e1` |
| **Repo** | https://github.com/prompt-ai-studio/Virtual-teams-landing-page.git (creado 2026-06-05, branch `main` activa — supersedes ADR-LAND-04 original que decía `NCoreSys/vttagent-landing`) |
| **Repo local** | `c:/Users/Martin/Documents/virtual-teams/Virtual-teams-landing-page/` |
| **Branch principal** | `main` |
| **URL producción** | https://vttagent.com (Nginx en VM Hetzner 77.42.88.106) |
| **Backend VTT (API tracking)** | https://api.vttagent.com |
| **Backend landing (early access endpoint)** | https://api.vttagent.com/api/early-access (montado sobre backend VTT existente — ADR-LAND-01) |
| **Swagger VTT** | https://api.vttagent.com/api-docs |
| **PM** | Martin Rivas — `pm@vtt.com` (humano admin, gestiona VTT principal y VTL) |
| **TL** | Claude (Tech Lead) — `tech.lead@vtt-landing.ai` |
| **Última actualización** | 2026-06-05 |
| **Verificado contra API** | Sí — `POST /api/projects` 2026-06-05 (creado por PO con bypass `platform_super_admin`) |
| **Origen** | Proyecto creado vía API el 2026-06-05T05:08:11Z. Tropicalizado de `vtt/` v1.0 (2026-05-29). |

> ⚠️ **VTL no es VTT.** Es un proyecto distinto en la misma plataforma. Comparten el backend VTT y la service key, pero el equipo, los UUIDs, el flujo y el contexto son independientes. NUNCA mezclar tareas/dependencias/contextos entre VTT y VTL.

---

## 1. Equipo VTL — Emails y UUIDs

> Todos los emails terminan en `@vtt-landing.ai`. Los UUIDs son distintos a los del equipo VTT.

### Coordinación y Gestión

| Rol | Nombre | Email | UUID |
|---|---|---|---|
| **TL** Tech Lead (coordinador del bloque técnico) | Claude (Tech Lead) | `tech.lead@vtt-landing.ai` | `e47a98e4-57ea-453f-8164-5aeb5fac0d06` |
| **PJM** Project Manager | Project Manager | `project.manager@vtt-landing.ai` | `9fe5d1db-15bc-4ff4-ac9a-880958146f53` |
| **PM** Product Manager | Product Manager | `product.manager@vtt-landing.ai` | `fbed7a92-fc3f-49c7-8d50-28e5ccf2734c` |
| **ProgM** Program Manager | Program Manager | `program.manager@vtt-landing.ai` | `f220fa38-5e49-4931-b1d8-1a954ffcb699` |
| **PO** Product Owner ⭐ creador del proyecto | Product Owner | `product.owner@vtt-landing.ai` | `fb3662a1-23fa-4f62-a23b-d2e14dd1ff29` |

> ⭐ El PO tiene capability `workspaces.create` (via membership `tenant_admin` + bypass `platform_super_admin`). Es el único rol del equipo VTL con permiso para crear/eliminar proyectos via API.

### Desarrollo

| Rol | Nombre | Email | UUID |
|---|---|---|---|
| **BE** Backend API Specialist #1 | Backend API Specialist | `backend.dev@vtt-landing.ai` | `a2e44984-929c-4453-a8c2-01815d0a74be` |
| **BE2** Backend API Specialist #2 | Backend API Specialist #2 | `backend.dev2@vtt-landing.ai` | `57da2365-bc11-422f-8915-6139a2957019` |
| **DB** Database Engineer | Database Engineer | `db.engineer@vtt-landing.ai` | `3360c720-9357-4a4c-9b2a-95088ab4197b` |
| **INF / DO** DevOps Engineer (Infra + VM Admin) | DevOps Engineer | `devops@vtt-landing.ai` | `56107eb4-bd15-426f-958f-3d9f7099b007` |
| **FE** Frontend Dev #1 | Frontend Dev #1 | `frontend.dev1@vtt-landing.ai` | `ea466308-4d6b-4cb7-a423-1f1074ec9861` |
| **FE2** Frontend Dev #2 | Frontend Dev #2 | `frontend.dev2@vtt-landing.ai` | `4506f68b-9fd7-4a4d-a223-aa6a795edbc7` |
| **AA** Asset Agent (rol nuevo VTL — produce SVGs/favicons/screenshots) | Asset Agent | `asset.agent@vtt-landing.ai` | `3ed05c2b-01b4-4424-af28-891bae29d063` |
| **MOT** Motion Agent (rol nuevo VTL — implementa GSAP) | Motion Agent | `motion.agent@vtt-landing.ai` | `cce1da50-be81-4fcb-a173-84af95f10dc1` |

> 🆕 **AA y MOT son roles nuevos creados específicamente para VTL.** No existen en el equipo VTT principal. AA opera bajo dirección del DL (produce íconos/logos/favicons/screenshots optimizados, sin tomar decisiones de diseño). MOT implementa la timeline GSAP de 38s de la demo y la MicroDemo del hero. Ambos tienen `role=frontend_dev` en el catálogo de roles VTT por compatibilidad RBAC.

### Análisis y QA

| Rol | Nombre | Email | UUID |
|---|---|---|---|
| **SA** Systems Analyst | Systems Analyst | `systems.analyst@vtt-landing.ai` | `1137661e-f2b2-41ad-9728-bdb8e00bb674` |
| **QA** QA Engineer #1 | QA Engineer | `qa.engineer@vtt-landing.ai` | `111fb749-31b8-4eca-ae76-0e8628d6b407` |
| **QA2** QA Engineer #2 | QA Engineer #2 | `qa.engineer2@vtt-landing.ai` | `795f8bef-71e2-42fd-83a7-3334099256d5` |
| **AR** Auditor Reviewer (Architect) | Auditor Reviewer | `auditor.reviewer@vtt-landing.ai` | `aec481d2-85c0-40e1-ad04-48f07f76114b` |
| **IR** Integration Reviewer | Integration Reviewer | `integration.reviewer@vtt-landing.ai` | `d62c5658-6b51-455e-8bf1-3e9d71c0c64f` |
| **IA** Integration Auditor | Integration Auditor | `integration.auditor@vtt-landing.ai` | `d825e4d6-76ea-4ecf-9bde-6bf992f52a2a` |

### Diseño

| Rol | Nombre | Email | UUID |
|---|---|---|---|
| **DL** Design Lead | Design Lead | `design.lead@vtt-landing.ai` | `625ef947-84ab-47e4-8c8e-05cdd2de9079` |
| **UX** UX Designer | UX Designer | `ux.designer@vtt-landing.ai` | `ffdc410f-3649-4ee6-b0e3-9b38475332eb` |

### Sistema

| Rol | Nombre | Email | UUID |
|---|---|---|---|
| **System** | System | `system@vtt-landing.ai` | `a1362e33-a868-4972-9389-669cbe3b28b5` |

---

## 2. Service Key

```
La SERVICE_KEY vive en c:/Users/Martin/Documents/virtual-teams/Virtual-teams-landing-page/.env
bajo la variable VTT_TL_SERVICE_KEY.
```

> ⚠️ **NUNCA hardcodear la service key en este archivo, en código, ni en comentarios de VTT.** Leerla del `.env` con `source .env` o equivalente y referenciarla como `$VTT_TL_SERVICE_KEY` (o `$BE_SERVICE_KEY` en docs heredados).
>
> **Importante:** el nombre `VTT_TL_SERVICE_KEY` es histórico. La key es **genérica del proyecto VTL** — autentica a cualquier UUID del equipo VTL (TL, PO, BE, etc.) vía `POST /api/auth/service-token` (body: `{userId, serviceKey}`). Token válido 30 días.

---

## 3. UUIDs de Status (Task lifecycle)

> Heredados del backend VTT — comunes a todos los proyectos.

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
- **Astro 5** (SSG, partial hydration) + **React islands** para interactividad
- **TypeScript strict**
- **Tailwind CSS 4** + CSS custom properties (design tokens) + **CSS Modules** (demo)
- **GSAP 3 + ScrollTrigger** (dynamic import — solo §6 cuando entra al viewport — NFR-05)
- Fuentes **self-hosted** (Instrument Sans + Inter + JetBrains Mono — ADR-LAND-03)
- Plausible analytics (cookieless)

### Backend (early access endpoint)
- **Express endpoint en backend VTT existente** (NO Supabase — ADR-LAND-01)
- **Prisma + PostgreSQL 16** (tabla `early_access_leads`)
- **Cloudflare Turnstile** (spam protection invisible)
- **Resend** (notificación email al equipo por cada lead)

### Infra / Deploy
- **Nginx en VM Hetzner 77.42.88.106** (NO Vercel — ADR-LAND-02)
- **GitHub Actions** → rsync SSH
- Dominio: `vttagent.com`

### Repo
- **Independiente** (`prompt-ai-studio/Virtual-teams-landing-page` — supersedes ADR-LAND-04 que decía `NCoreSys/vttagent-landing`)

---

## 6. Modelo de dos repos — Normativa vs Operativa

> **Regla:** El agente VTL consulta documentos de DOS repos según la naturaleza del documento.

### Repo `virtual-teams-setup/` — Normativa

| Categoría | Path canónico |
|-----------|---------------|
| Datos del equipo VTL (este archivo) | `00-platform/05.proyectos/vtl/Proyect_data.md` |
| Operativos por rol | `00-platform/05.proyectos/vtl/operativos-instancias/` |
| Init messages por rol | `00-platform/05.proyectos/vtl/init-messages/` |
| Setups por rol | `00-platform/05.proyectos/vtl/setups/` |
| Perfiles base genéricos | `00-platform/01.agents/roles/` |
| **Protocols** (procesos completos) | `00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-*.md` ← compartidos con VTT |
| **Reglas Nivel 0** | `00-platform/02.normativa/00.Rules/rules_catalog.json` ← compartido con VTT |
| **Skills** (capacidades reusables) | `00-platform/02.normativa/03.Skills/` ← compartidas con VTT |
| **Scripts canónicos** | `00-platform/02.normativa/04.Scripts/` ← compartidos con VTT |
| Templates BRIEF / ASSIGNMENT / devlog / code_logic | `00-platform/03.templates/tarea/` |
| Templates Handoff / Methodologies | `00-platform/03.templates/handoff/` |
| Templates Specs UI/UX | `00-platform/03.templates/specs-design/` |
| Guías operativas | `00-platform/04.docs-soporte/guias-operativas/` |

### Repo `Virtual-teams-landing-page/` — Operativa

| Categoría | Path |
|-----------|------|
| Specs aprobados (9 docs LPDR a Growth) | `docs/Specs/` |
| Handoffs por sprint (PJM→TL) | `docs/Sprints/HANDOFF_TL_S0X.md` |
| Closures por sprint | `docs/Sprints/CLOSURE_S0X.md` |
| Setup del bloque | `docs/Sprints/SETUP_BLOQUE_LANDING.md` |
| Contexto del bloque (IDs reales VTT) | `docs/Sprints/CONTEXTO_BLOQUE_LANDING.md` |
| HO maestro PJM→TL | `docs/Sprints/HO_PJM_TL_LANDING.md` |
| Material de planning + perfiles AA/MOT | `docs/Planning files/` |
| Material referencial técnico | `knowledge/Docs/` |
| Briefs y assignments por tarea | `knowledge/agent-tasks/briefs/` y `/assignments/` |
| Development logs | `knowledge/development-log/` |
| Code logic | `knowledge/code-logic/` |
| **Task manifests** (canónico v1.1) | `knowledge/task-manifests/<phase>/<sprint>/` |
| .env (VTT_TL_SERVICE_KEY) | `.env` (NO commitear) |
| Project ID persistido | `.vtl_project_id` (NO commitear) |
| JWT TL persistido | `.vtl_jwt` (NO commitear) |

### Regla de decisión rápida

```
¿El documento es genérico/reutilizable entre proyectos?
  SÍ → virtual-teams-setup/00-platform/...
  NO → Virtual-teams-landing-page/...

¿Es estado vivo del trabajo en curso?
  SÍ → Virtual-teams-landing-page/
  NO (es plantilla, perfil, regla, proceso) → virtual-teams-setup/
```

---

## 7. Worktrees del proyecto VTL (PROTOCOL-WT-001 v1.1.0)

**VTL SÍ usa worktrees por equipo.** Aunque es un proyecto de tamaño medio (263.5h, 75 tareas, 6 sprints), sin worktrees los agentes se pisarían trabajando en paralelo sobre el mismo repo (incidentes documentados PROC-COORD-01 / vtt-setup 2026-06-02).

### 7.1 Mapeo de 5 equipos VTL

| Equipo | Roles | Worktree path | Branch idle | Repo base | Sprints activos |
|---|---|---|---|---|---|
| **infra** | INF (DO) | `.vtt/worktrees/vttl-team-infra/` | `wt-vttl-team-infra` | `Virtual-teams-landing-page/` | S00, S05 |
| **design** | DL + AA (AA bajo dirección DL — HO §6.5) | `.vtt/worktrees/vttl-team-design/` | `wt-vttl-team-design` | `Virtual-teams-landing-page/` | S00 (DL+AA) + S01-S04 (DL Design Review) |
| **frontend** | FE + MOT (ambos tocan `src/components/demo/`) | `.vtt/worktrees/vttl-team-frontend/` | `wt-vttl-team-frontend` | `Virtual-teams-landing-page/` | S01-S04 (FE) + S03-S04 (MOT) |
| **qa** | QA | `.vtt/worktrees/vttl-team-qa/` | `wt-vttl-team-qa` | `Virtual-teams-landing-page/` | S05 |
| **backend** | BE | `.vtt/worktrees/vttl-team-backend/` | `wt-vttl-team-backend` | `virtual-teams-tracking/` (ADR-LAND-01) | S00 |

> **Total: 5 worktrees.** El TL Reviewer NO ocupa worktree (opera en clon padre — `PROTOCOL-WT-001 §7.bis`).

### 7.2 Reglas operativas

- **El TL VTL es administrador único** de los worktrees: los crea (setup inicial), los asigna en cada ASSIGNMENT (`worktreePath` del execution_manifest), valida disciplina al cerrar, hace cleanup post-aprobación, recrea si se corrompen, cleanup masivo al cerrar el bloque (ver `OPERATIVO_TL_REVIEWER.md §16`).
- **Los agentes NUNCA crean/eliminan worktrees** por su cuenta — solo trabajan en el asignado.
- **Coordinación intra-equipo:** solo UN agente del mismo equipo en `task_in_progress` por vez. Equipos `design` (DL+AA) y `frontend` (FE+MOT) necesitan esta coordinación.
- **Worktrees auxiliares temporales:** si dos agentes del mismo equipo necesitan paralelo real → crear `vttl-team-<equipo>-aux-NN` con `PROTOCOL-WT-001 §5.4.5`.
- **Branch idle** (`wt-vttl-team-*`) NUNCA se mergea a main — solo sirve para que el worktree no quede detached.
- `.vtt/` está en `.gitignore` — los worktrees son infra local, NO se commitean.

### 7.3 Convivencia con worktrees de VTT principal

El repo `virtual-teams-tracking/` también aloja los worktrees del proyecto VTT principal (`vtt-espacio-1..5`). El worktree `vttl-team-backend` convive con ellos:

```
virtual-teams-tracking/.vtt/worktrees/
├── vtt-espacio-1..5/      ← VTT principal (otro equipo, otro proyecto)
└── vttl-team-backend/      ← VTL backend (este proyecto)
```

> El BE de VTL **SOLO** trabaja en `vttl-team-backend`. NUNCA entra a `vtt-espacio-*`.

---

## 8. Estructura del proyecto VTL

### Jerarquía VTT planificada (a crear en setup post-tropicalización)

```
Project (VTTL) — 7e460b63-a3b0-4ce5-9d21-b88cf38748e1
  └── Release (v1.0 Landing)
        └── Sprints (S00-S05) — 6 sprints, ~14 días c/u (sprintEnabled=true, sprintDuration=14)
              └── Deliveries (1 por sprint × cadena de rol)
                    └── Tasks (75 nodos: 73 tareas + SETUP-BLOQUE-LANDING + CIERRE-BLOQUE-LANDING)
```

### Roles activos por sprint (HO PJM→TL §5)

| Sprint | Horas | Roles activos | Foco |
|---|---|---|---|
| **S00** | 67.5h | TL, INF, DL, AA, BE | Infra + Assets + Backend + Mockups |
| **S01** | 43h | TL, DL (DR), FE | Foundation Astro + 11 secciones estáticas |
| **S02** | 38h | TL, DL (DR), FE | Interactivos (tabs, form, TaskCard) + demo base |
| **S03** | 49h ⚡ CRITICAL PATH | TL, DL (DR), FE, MOT | GSAP timeline 38s + ensamblaje demo |
| **S04** | 38h | TL, DL (DR), FE, MOT | MicroDemo + ensamblaje + analytics + login |
| **S05** | 28h | TL, INF, QA, PM | QA + Deploy + Post-launch |

---

## 9. Carga de contexto del agente VTL

### Capa 1 — Auto-cargado en cada sesión
- `MEMORY.md` (auto-memory del proyecto VTL, si existe)
- `rules_agents.instructions.md` (reglas globales transversales — comunes a VTT+VTL)
- `OPERATIVO_<ROL>.md` (perfil del rol activo)

### Capa 2 — El agente lee manualmente al iniciar

**Normativa (virtual-teams-setup):**
- `00-platform/05.proyectos/vtl/Proyect_data.md` — este archivo
- `00-platform/05.proyectos/vtl/operativos-instancias/OPERATIVO_<MI_ROL>.md`
- `00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-*.md` (ASG-001 para TL; WT-001, MAN-001, DEV-001 para ejecutores)
- `00-platform/02.normativa/03.Skills/precheck/VTT.SKILL-PRECHECK-001_*.md`

**Operativa (Virtual-teams-landing-page):**
- `docs/Sprints/HANDOFF_TL_S0X.md` (TL al planificar)
- `docs/Sprints/CONTEXTO_BLOQUE_LANDING.md` (estado del bloque)
- `docs/Specs/<spec relevante>` (segun rol — ver §10 abajo)
- `GET /api/tasks?assigneeId=<UUID_AGENTE>` — mis tareas asignadas

### Capa 3 — Específico por tarea (attachments VTT)
- `BRIEF_<TASK_ID>_*.md` (attachment de la tarea — el TL lo escribe)
- `ASSIGNMENT_<TASK_ID>_*.md` (attachment de la tarea — el TL lo escribe)
- Mensaje del agente (comentario en la tarea con curls de status y datos)
- **Specs relevantes** adjuntados como `fileType=brief` adicional

---

## 10. Specs por rol (qué adjuntar a tareas de cada agente)

| Rol | Specs obligatorias | Specs referenciales |
|---|---|---|
| **DL** Design Lead | 00 LPDR, 01 UX Narrative, 03 Wireframe, 05 Visual/UI | 02 Demo Sim, 06 Motion |
| **AA** Asset Agent | 05 Visual/UI §I1, 08 Growth §3.2 (favicon) | 04 Copy §2/§3/§7/§8, 00 LPDR §17.9 |
| **MOT** Motion Agent | 06 Motion Spec, 02 Demo Sim | 05 Visual/UI §B2, 07 Technical §3 |
| **FE** Frontend | 07 Technical Spec, 03 Wireframe, 04 Copy, 05 Visual/UI, 06 Motion | Todas las demás como referencia |
| **BE** Backend | 07 Technical §1.4, §7, ADR-LAND-01/09 | — |
| **INF** DevOps | 3B.8 Infrastructure Plan, ADR-LAND-02 | 07 Technical §8 |
| **QA** QA | Todas las specs (validación contra spec) | 08 Growth §1.6, §2.2 |
| **TL** Tech Lead | Todas (coordina y revisa todo) | — |

---

## 11. Diferencias con VTT principal y Memory Service

VTL es un proyecto **distinto** dentro de la misma plataforma. Particularidades:

| Aspecto | VTT principal | VTL (este proyecto) | Memory Service |
|---|---|---|---|
| Project Key | `VTT` | `VTTL` | `MS` |
| Email domain | `@vtt.ai` / `@vtt.com` | `@vtt-landing.ai` | varía |
| Worktrees por equipo | Sí (5 espacios genéricos) | **Sí (5 worktrees fijos por equipo VTL)** — ver §7 | Sí (por rol) |
| Sprints | 14 días | 14 días | 14 días |
| Bloque actual | Bloque 1.A R2.0 | v1.0 Landing | Fase 1A+ |
| Roles únicos | TL, PM, BE, DB, DO, FE, QA, AR, IR, DL, UX, SA, PJM, ProgM, PO, PdM, IA | + **AA** + **MOT** (rol nuevo VTL) | + CIA, MRA, PSA, FA, SEC, SRE, TW, QAA, PTE, UXR |

---

## 12. Comandos rápidos

### Obtener JWT (cualquier UUID del equipo VTL)

```bash
cd c:/Users/Martin/Documents/virtual-teams/Virtual-teams-landing-page
set -a && . ./.env && set +a

python3 -c "
import urllib.request, json, os
req = urllib.request.Request(
    'https://api.vttagent.com/api/auth/service-token',
    data=json.dumps({'userId': '<TU_UUID>', 'serviceKey': os.environ['VTT_TL_SERVICE_KEY']}).encode(),
    headers={'Content-Type': 'application/json'}, method='POST')
with urllib.request.urlopen(req) as r:
    print(json.loads(r.read())['data']['token'])
" > .vtl_jwt
```

### Validar usuarios del sistema VTL

```bash
TOKEN=$(cat .vtl_jwt)
curl -s -H "Authorization: Bearer $TOKEN" "https://api.vttagent.com/api/users?limit=100" \
  | python3 -m json.tool | grep -E '(vtt-landing|id)'
```

### Obtener tareas del proyecto VTL

```bash
TOKEN=$(cat .vtl_jwt)
PROJECT_ID=$(cat .vtl_project_id)
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.vttagent.com/api/tasks?projectId=$PROJECT_ID&limit=200" | python3 -m json.tool
```

---

## 13. Capability — `workspaces.create`

**Solo el PO** (`fb3662a1-23fa-4f62-a23b-d2e14dd1ff29`) tiene esta capability vía:
- Membership en organización `d147a8fb-372f-40d9-9390-db404dd1d0f3` con role `tenant_admin`
- Bypass `platform_super_admin` en el lookup del JWT

Resto del equipo (TL, PM, BE, etc.) tiene capabilities operativas estándar (`tasks.create`, `tracking.manage_workflows`, etc.) pero **NO puede crear/eliminar proyectos**.

Si en algún momento se necesita crear otro proyecto o bloque, debe usar el JWT del PO.

---

## 14. Validación

Para revalidar este documento contra el sistema:

```bash
# 1. Listar usuarios @vtt-landing.ai
TOKEN=$(cat .vtl_jwt)
curl -s -H "Authorization: Bearer $TOKEN" "https://api.vttagent.com/api/users?limit=200" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); users=d.get('data',{}).get('data',[]); print('\n'.join(f\"{u.get('role',''):20} {u['email']:40} {u['id']}\" for u in users if '@vtt-landing.ai' in u.get('email','')))"

# 2. Verificar que el proyecto VTTL existe
curl -s -H "Authorization: Bearer $TOKEN" "https://api.vttagent.com/api/projects" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); ps=d.get('data',{}).get('data',[]); print('\n'.join(f\"{p['key']:8} {p['name']:40} {p['id']}\" for p in ps if isinstance(p, dict)))"
```

---

## 15. Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-06-05 | Versión inicial. Tropicalizado de `vtt/Proyect_data.md` v1.0 (2026-05-28). Cambios principales: (1) Project UUID nuevo (`7e460b63-...`, key `VTTL` por límite 6 chars del API). (2) Equipo VTL con 22 UUIDs distintos del equipo VTT (mismos roles + 2 nuevos AA/MOT específicos para landing). (3) Email domain `@vtt-landing.ai`. (4) Stack landing-específico (Astro+React+GSAP+Nginx Hetzner, NO Vercel ni Supabase). (5) Modelo SIN worktrees (proyecto chico). (6) Service key referenciada del `.env` (NUNCA hardcoded). (7) Bypass `platform_super_admin` documentado para creación del proyecto. (8) Specs aprobadas (9 docs LPDR→Growth) listadas con asignación por rol. |
| 1.1 | 2026-06-05 | **Supersede del nombre del repo** (ADR-LAND-04 original). Cambio: `NCoreSys/vttagent-landing` → `prompt-ai-studio/Virtual-teams-landing-page`. Razón: el repo se creó en la org `prompt-ai-studio` (donde el TL tiene scope `repo`+`workflow` via gh CLI) y se conservó el nombre del directorio local existente (`Virtual-teams-landing-page`) para no romper paths absolutos en docs y scripts. Repo activo desde 2026-06-05T13:48:17Z con primer commit `32b34b7` (79 archivos, branch `main`). Actualizado en 6 archivos `vtl/` (Proyect_data, INDEX, INIT_DO, SETUP_DO, SETUP_TL_REVIEWER, OPERATIVO_DO) + 10 archivos `docs/` del repo landing (HO_PJM, HANDOFF_TL_S00, CLOSURE_S00, SETUP_BLOQUE_LANDING, 4 Planning files, 07 Technical ADDENDUM, HO_PM_PJM). |
| **1.2** | **2026-06-05** | **Reincorporación de worktrees por equipo (`PROTOCOL-WT-001 v1.1.0`).** Razón: la v1.0 había excluido worktrees argumentando "proyecto chico", pero sin worktrees los agentes se pisarían trabajando en paralelo (incidentes PROC-COORD-01 / vtt-setup 2026-06-02 confirmaron el patrón). Cambios: (1) **§7 reescrito completo:** "VTL NO usa worktrees" → "VTL SÍ usa worktrees por equipo" con mapeo de 5 equipos (infra/design/frontend/qa en repo landing + backend en `virtual-teams-tracking`), reglas operativas (TL administrador único, agentes nunca crean worktrees, coordinación intra-equipo 1 agente por vez, worktrees auxiliares temporales para paralelo real, branch idle nunca se mergea), convivencia con worktrees de VTT principal. (2) §11 tabla comparativa: "Worktrees por equipo: NO modelo liviano" → "Sí (5 worktrees fijos)". (3) Equipos definidos: `infra` (INF), `design` (DL+AA, AA bajo dirección DL HO §6.5), `frontend` (FE+MOT, ambos tocan `src/components/demo/`), `qa` (QA solo S05), `backend` (BE en `virtual-teams-tracking/` por ADR-LAND-01). (4) Actualizado también en todos los 15 perfiles (3 docs × 5 roles): TL Reviewer (§16 nueva, admin completa), DL Reviewer (§8.bis worktree workflow), DO (§8.bis), AA (§8.bis), BE (§8.bis con convivencia con worktrees VTT principal). |

---

**Mantenedor:** TL VTL (Claude — `tech.lead@vtt-landing.ai`)
**Cambios:** vía PR al repo `virtual-teams-setup/` (cuando esté en git)
**Origen:** tropicalización del `vtt/Proyect_data.md` v1.0 (2026-05-28)
