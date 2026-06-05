# INDEX — Proyecto VTL (VTT Agent Landing)

| Campo | Valor |
|---|---|
| Proyecto | VTT Agent Landing Page (VTL) |
| Project Key | `VTTL` |
| Project UUID | `7e460b63-a3b0-4ce5-9d21-b88cf38748e1` |
| Backend VTT | `https://api.vttagent.com` |
| URL producción | `https://vttagent.com` (Nginx en VM Hetzner) |
| Repo landing | `Virtual-teams-landing-page/` (remoto: `prompt-ai-studio/Virtual-teams-landing-page`) |
| Repo backend | `virtual-teams-tracking/` (mismo backend VTT existente — ADR-LAND-01) |
| PM | Martin Rivas — `pm@vtt.com` |
| TL | Claude (Tech Lead) — `tech.lead@vtt-landing.ai` |
| Sprints | 6 (S00 a S05), 263.5h funcionales, 75 nodos, ~148 dependencias |
| Versión | 1.0 |
| Fecha | 2026-06-05 |

> Índice navegable de los operativos del proyecto VTL. Tropicalizado de `vtt/INDEX.md` v1.0. **VTL es un proyecto distinto a VTT principal** — equipos y UUIDs separados, mismo backend VTT compartido.

---

## 1. Estructura del proyecto

```
05.proyectos/vtl/
├── Proyect_data.md             ← Datos maestros (UUIDs, paths, status, referencia service key)
├── INDEX.md                    ← Este archivo
├── operativos-instancias/      ← OPERATIVOS por rol (5 archivos para S00, faltan resto)
├── init-messages/              ← INIT por rol (5 archivos para S00)
└── setups/                     ← SETUP por rol (5 archivos para S00)
```

### Relación INIT → SETUP → OPERATIVO

```
1. INIT_<ROL>.md           ← System prompt corto al iniciar el agente (datos + reglas innegociables + ADRs aplicables)
        ↓ apunta a
2. SETUP_<ROL>.md          ← Procedimiento de arranque (working dir, JWT, archivos a leer, workflow por tarea)
        ↓ apunta a
3. OPERATIVO_<ROL>.md      ← Manual completo del rol (workflow, comandos, boundaries, reglas, equipo, fuentes)
```

---

## 2. Roles tropicalizados — Sprint S00 (esta tanda)

| Rol | Sigla | UUID | INIT | SETUP | OPERATIVO | Tareas S00 | Horas |
|-----|-------|------|------|-------|-----------|-----------|-------|
| **Tech Lead Reviewer** | TL | `e47a98e4-...` | [INIT](init-messages/INIT_TL_REVIEWER.md) | [SETUP](setups/SETUP_TL_REVIEWER.md) | [OPERATIVO](operativos-instancias/OPERATIVO_TL_REVIEWER.md) | Coordinación + TL-REVIEW-S00 + CIERRE-S00 | 3.5h |
| **Design Lead Reviewer** | DL | `625ef947-...` | [INIT](init-messages/INIT_DL_REVIEWER.md) | [SETUP](setups/SETUP_DL_REVIEWER.md) | [OPERATIVO](operativos-instancias/OPERATIVO_DL_REVIEWER.md) | DL-S00-01..08 (mockups, OG, login, demo frames) | 45h |
| **DevOps Engineer** | INF / DO | `56107eb4-...` | [INIT](init-messages/INIT_DO.md) | [SETUP](setups/SETUP_DO.md) | [OPERATIVO](operativos-instancias/OPERATIVO_DO.md) | INF-S00-01..06 (VM, Nginx, SSL, repo, CI) | 3.5h |
| **Asset Agent** 🆕 | AA | `3ed05c2b-...` | [INIT](init-messages/INIT_AA.md) | [SETUP](setups/SETUP_AA.md) | [OPERATIVO](operativos-instancias/OPERATIVO_AA.md) | AA-S00-01..04 (íconos, logos, favicon, screenshots) | 16h |
| **Backend Engineer** | BE | `a2e44984-...` | [INIT](init-messages/INIT_BE.md) | [SETUP](setups/SETUP_BE.md) | [OPERATIVO](operativos-instancias/OPERATIVO_BE.md) | BE-S00-01..03 (model + endpoint + integrations) | 10h |

> 🆕 **AA es un rol NUEVO específico de VTL** — no existe en VTT principal. Es operador gráfico bajo dirección del DL.

---

## 3. Roles pendientes (próximas tandas — al avanzar sprints)

| Rol | Sigla | UUID | Sprints | Cuándo tropicalizar |
|-----|-------|------|---------|---------------------|
| **Frontend Engineer** | FE | `ea466308-...` | S01-S04 | Antes de cerrar S00 (FE arranca S01) |
| **Motion Agent** 🆕 | MOT | `cce1da50-...` | S03-S04 | Antes de cerrar S02 (MOT arranca S03) |
| **QA Engineer** | QA | `111fb749-...` | S05 | Antes de cerrar S04 |
| **Product Manager** | PM (Martin humano) | `07a07147-...` | S05 (PM-S05-01..05) | Antes de cerrar S04 |

> 🆕 **MOT es un rol NUEVO específico de VTL** — implementa GSAP timeline 38s y MicroDemo.

**Otros roles del equipo VTL (22 UUIDs en `Proyect_data.md §1`)** que pueden activarse según necesidad:
- BE #2 backup (`57da2365-...`)
- DB (`3360c720-...`)
- FE #2 backup (`4506f68b-...`)
- QA #2 (`795f8bef-...`)
- SA (`1137661e-...`)
- UX (`ffdc410f-...`) — backup DL
- AR, IR, IA, PdM, ProgM, PJM, PO — no esperados en operación regular

---

## 4. Modelo Reviewer-only (VTL) vs Executor+Reviewer (VTT)

VTT principal desdobla algunos roles (TL Executor + TL Reviewer, DL Executor + DL Reviewer, etc.). **VTL usa modelo LIVIANO con solo Reviewer** para TL/DL:

| Rol | VTT principal | VTL |
|-----|---------------|-----|
| TL | TL_EXECUTOR + TL_REVIEWER (2 perfiles, mismo UUID) | **TL_REVIEWER único** (coordinador completo) |
| DL | DL_EXECUTOR + DL_REVIEWER (2 perfiles, mismo UUID) | **DL_REVIEWER único** (produce mockups + DR) |
| PM | PM_EXECUTOR + PM_REVIEWER | (Solo PM humano en S05) |
| SA | SA_EXECUTOR + SA_REVIEWER | (No activo regular) |

Razón: VTL es proyecto chico (75 tareas, 6 sprints) con modelo de validación liviano (HO PJM→TL §6.2).

---

## 5. Modelo de dos repos — Normativa vs Operativa

> El agente VTL consulta documentos de DOS repos según la naturaleza del documento.

### Repo `virtual-teams-setup/` — Normativa (compartida con VTT)

| Tipo | Path canónico |
|------|---------------|
| Datos del equipo VTL | `00-platform/05.proyectos/vtl/Proyect_data.md` |
| Operativos por rol | `00-platform/05.proyectos/vtl/operativos-instancias/` |
| Init messages | `00-platform/05.proyectos/vtl/init-messages/` |
| Setups por rol | `00-platform/05.proyectos/vtl/setups/` |
| Protocols (procesos) | `00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-*.md` ← compartidos con VTT |
| Reglas Nivel 0 | `00-platform/02.normativa/00.Rules/rules_catalog.json` ← compartido |
| Skills | `00-platform/02.normativa/03.Skills/` ← compartidas |
| Scripts canónicos | `00-platform/02.normativa/04.Scripts/` ← compartidos |
| Templates | `00-platform/03.templates/` ← compartidos |
| Guías operativas | `00-platform/04.docs-soporte/guias-operativas/` |

### Repo `Virtual-teams-landing-page/` — Operativa específica VTL

| Tipo | Path |
|------|------|
| **9 Specs aprobados** (LPDR + 8 más) | `docs/Specs/` |
| Handoffs por sprint | `docs/Sprints/HANDOFF_TL_S0X.md` |
| Closures por sprint | `docs/Sprints/CLOSURE_S0X.md` |
| HO maestro PJM→TL | `docs/Sprints/HO_PJM_TL_LANDING.md` |
| Setup del bloque (receta) | `docs/Sprints/SETUP_BLOQUE_LANDING.md` |
| Contexto del bloque (IDs reales) | `docs/Sprints/CONTEXTO_BLOQUE_LANDING.md` |
| Perfiles AA + MOT específicos | `docs/Planning files/PERFIL_*.md` |
| Material referencial | `knowledge/Docs/` |
| Briefs y assignments (que el TL escribe) | `knowledge/agent-tasks/briefs/` y `/assignments/` |
| Development logs | `knowledge/development-log/` |
| Code logic | `knowledge/code-logic/` |
| Task manifests v1.0/v1.5 | `knowledge/task-manifests/<phase>/<sprint>/` |
| `.env` (VTT_TL_SERVICE_KEY) | `.env` (NO commitear) |
| Project ID persistido | `.vtl_project_id` |
| JWT persistido | `.vtl_jwt` |

### Repo `virtual-teams-tracking/` — Backend VTT (donde implementa el BE de VTL)

| Tipo | Path |
|------|------|
| Schema Prisma (el BE agrega `EarlyAccessLead`) | `backend/prisma/schema.prisma` |
| Migrations (el BE agrega `add_early_access_lead`) | `backend/prisma/migrations/` |
| Routes (el BE agrega `early-access.routes.ts`) | `backend/src/routes/` |
| Services (el BE agrega `early-access.service.ts`) | `backend/src/services/` |
| Validators (el BE agrega `early-access.validator.ts`) | `backend/src/validators/` |
| `.env` backend (VTT_TL_SERVICE_KEY también vive aquí) | `.env` |

> El BE de VTL NO toca otros archivos del backend VTT — solo agrega 1 model + 1 router + 1 service + 1 validator (ADR-LAND-01).

---

## 6. Worktrees del proyecto VTL (PROTOCOL-WT-001 v1.1.0)

**VTL SÍ usa worktrees por equipo.** 5 worktrees fijos (uno por equipo VTL). Sin worktrees los agentes se pisarían trabajando en paralelo sobre el mismo repo.

| Equipo | Roles | Worktree path | Repo base |
|---|---|---|---|
| **infra** | INF (DO) | `.vtt/worktrees/vttl-team-infra/` | `Virtual-teams-landing-page/` |
| **design** | DL + AA | `.vtt/worktrees/vttl-team-design/` | `Virtual-teams-landing-page/` |
| **frontend** | FE + MOT | `.vtt/worktrees/vttl-team-frontend/` | `Virtual-teams-landing-page/` |
| **qa** | QA | `.vtt/worktrees/vttl-team-qa/` | `Virtual-teams-landing-page/` |
| **backend** | BE | `.vtt/worktrees/vttl-team-backend/` | `virtual-teams-tracking/` (ADR-LAND-01) |

- **TL Reviewer NO ocupa worktree** — opera en clon padre (`§7.bis`). SÍ administra los 5 worktrees (crea, asigna, valida disciplina, cleanup, recrea si se corrompen).
- **Cada agente ejecutor** trabaja en el worktree de SU equipo, creando `feature/<TASK_ID>` desde `main`.
- **Coordinación intra-equipo** (solo equipos `design` y `frontend` con 2 agentes): solo UN agente en `task_in_progress` por vez. Para paralelo real → worktree auxiliar temporal (`PROTOCOL-WT-001 §5.4.5`).
- Detalle completo: `Proyect_data.md §7` + `OPERATIVO_TL_REVIEWER.md §16`.

---

## 7. ADRs activos VTL (HO §9 — 16 ADRs vinculantes)

| ADR | Decisión | Roles afectados |
|---|---|---|
| ADR-LAND-01 | Backend VTT existente, no Supabase | BE, INF |
| ADR-LAND-02 | Nginx en VM, no Vercel | INF |
| ADR-LAND-03 | Fonts self-hosted (no Google Fonts CDN) | FE, DL |
| ADR-LAND-04 | Repo independiente `prompt-ai-studio/Virtual-teams-landing-page` (renombrado vs ADR original `NCoreSys/vttagent-landing` — ver Proyect_data §15 changelog) | INF |
| ADR-LAND-06 | Estados Completed/Approved/Release-ready = amber/blue/green | DL, FE, MOT |
| ADR-LAND-07 | Plan→Queue slide (no morph) | FE, MOT |
| ADR-LAND-08 | Spring easing PROHIBIDO en demo | MOT, FE |
| ADR-LAND-09 | Duplicate email → 200 (NO 409) | BE |
| ADR-LAND-10 | Warning suave email personal | BE, FE |
| ADR-LAND-11 | MobileMenu = client:load | FE |
| ADR-LAND-12 | SSL via Certbot Let's Encrypt | INF |
| ADR-LAND-13 | © 2026 Ncoresys en footer | FE |
| ADR-LAND-14 | Early access embebido (anchor §10, no página separada) | FE |
| ADR-LAND-15 | Autoplay off en mobile on scroll | FE, MOT |
| ADR-LAND-16 | DL + AA separados (DL conceptual, AA producción mecánica) | DL, AA |

Otros ADRs (incluido ADR-LAND-05) listados en `HO_PJM_TL_LANDING.md §9`.

---

## 8. Controles de seguridad VTL (HO §10 — 12 SEC-L)

| ID | Control | Sprint impl | Sprint verif | Responsable |
|---|---|---|---|---|
| SEC-L-01 | Rate limiting 5 req/min/IP | S00 | S05 | BE |
| SEC-L-02 | Turnstile server-side | S00 | S05 | BE |
| SEC-L-03 | No info leak duplicados | S00 | S05 | BE |
| SEC-L-04 | Validación Zod | S00 | S05 | BE |
| SEC-L-05 | CORS restrictivo | S00 | S05 | BE |
| SEC-L-06 | No PII en logs | S00 | S05 | BE |
| SEC-L-07 | HTTPS obligatorio | S00 | S05 | INF |
| SEC-L-08 | No directory listing | S00 | S05 | INF |
| SEC-L-09 | Security headers | S00 | S05 | INF |
| SEC-L-10 | No inline scripts no controlados | S01 | S05 | FE |
| SEC-L-11 | Input no renderizado como HTML | S02 | S05 | FE |
| SEC-L-12 | Turnstile site key para vttagent.com | S00 | S05 | INF |

---

## 9. Sprints y mapeo a roles activos (HO §5)

| Sprint | Horas | Tareas | Roles activos | Foco |
|---|---|---|---|---|
| **S00** | 67.5h | 23 (22 + CIERRE-S00) | TL, INF, DL, AA, BE | Infra + Assets + Backend + Mockups |
| **S01** | 43h | 15 (14 + CIERRE-S01) | TL, DL (DR), FE | Foundation Astro + 11 secciones estáticas |
| **S02** | 38h | 9 (8 + CIERRE-S02) | TL, DL (DR), FE | Interactivos + demo base |
| **S03** ⚡ | 49h | 9 (8 + CIERRE-S03) | TL, DL (DR), FE, **MOT** | GSAP timeline 38s + ensamblaje demo |
| **S04** | 38h | 9 (8 + CIERRE-S04) | TL, DL (DR), FE, MOT | MicroDemo + ensamblaje + analytics + login |
| **S05** | 28h | 10 (9 + CIERRE-S05) + CIERRE-BLOQUE | TL, INF, QA, PM | QA + Deploy + Post-launch |

Critical path = ~105h (demo: S02 deps → S03 GSAP → S04 ensamblaje).

---

## 10. Carga de contexto por agente (capas)

### Capa 1 — Auto-cargado en cada sesión
- `MEMORY.md` (auto-memory del proyecto VTL, si existe)
- `rules_agents.instructions.md` (reglas globales — comunes VTT+VTL)
- `OPERATIVO_<ROL>.md` (perfil del rol activo)

### Capa 2 — El agente lee manualmente al iniciar

**Normativa:**
- `00-platform/05.proyectos/vtl/Proyect_data.md`
- `00-platform/05.proyectos/vtl/operativos-instancias/OPERATIVO_<MI_ROL>.md`
- `00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-*.md` (ASG-001 para TL; MAN-001 para ejecutores)
- `00-platform/02.normativa/03.Skills/precheck/VTT.SKILL-PRECHECK-001_*.md`
- `00-platform/02.normativa/03.Skills/report/VTT.SKILL-REPORT-001_*.md`

**Operativa específica VTL:**
- `Virtual-teams-landing-page/docs/Sprints/HO_PJM_TL_LANDING.md` (TL)
- `Virtual-teams-landing-page/docs/Sprints/HANDOFF_TL_S0X.md` (todos en su sprint)
- `Virtual-teams-landing-page/docs/Specs/<spec relevante por rol>` (ver §11 abajo)
- `GET /api/tasks?assigneeId=<UUID_AGENTE>`

### Capa 3 — Específico por tarea (attachments VTT)
- `BRIEF_<TASK_ID>_*.md` (que el TL escribe)
- `ASSIGNMENT_<TASK_ID>_*.md` (que el TL escribe)
- **Specs relevantes** adjuntados como `fileType=brief` adicional

---

## 11. Specs aprobadas por rol (qué adjuntar a tareas)

| Rol | Specs obligatorias | Specs referenciales |
|---|---|---|
| **DL** | 00 LPDR, 01 UX Narrative, 03 Wireframe, 05 Visual/UI | 02 Demo Sim, 06 Motion |
| **AA** | 05 Visual/UI §I1, 08 Growth §3.2 (favicon), PERFIL_ASSET_AGENT | 04 Copy §2/§3/§7/§8, 00 LPDR §17.9 |
| **MOT** | 06 Motion Spec, 02 Demo Sim, PERFIL_MOTION_AGENT | 05 Visual/UI §B2, 07 Technical §3 |
| **FE** | 07 Technical, 03 Wireframe, 04 Copy, 05 Visual/UI, 06 Motion | Todas las demás como referencia |
| **BE** | 07 Technical §1.4 + §7, ADR-LAND-01/09 | — |
| **INF** | 3B.8 Infrastructure (si existe), ADR-LAND-02/12 | 07 Technical §8 |
| **QA** | Todas (validación contra spec) | 08 Growth §1.6, §2.2 |
| **TL** | Todas | — |

---

## 12. Validación

Para revalidar este índice contra el sistema:

```bash
cd c:/Users/Martin/Documents/virtual-teams/Virtual-teams-landing-page
set -a && . ./.env && set +a

# Listar usuarios VTL
TOKEN=$(cat .vtl_jwt)
curl -s -H "Authorization: Bearer $TOKEN" "https://api.vttagent.com/api/users?limit=200" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); users=d.get('data',{}).get('data',[]); print('\n'.join(f\"{u.get('role',''):20} {u['email']:40} {u['id']}\" for u in users if '@vtt-landing.ai' in u.get('email','')))"

# Verificar proyecto VTTL
curl -s -H "Authorization: Bearer $TOKEN" "https://api.vttagent.com/api/projects" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); ps=d.get('data',{}).get('data',[]); print('\n'.join(f\"{p['key']:8} {p['name']:40} {p['id']}\" for p in ps if isinstance(p, dict)))"
```

---

## 13. Pendientes (TODOs)

### Roles a tropicalizar en próximas tandas
- [ ] FE Frontend Engineer (antes de S01)
- [ ] MOT Motion Agent (antes de S03)
- [ ] QA Engineer (antes de S05)
- [ ] PM Executor (para tareas PM-S05-01..05)
- [ ] Otros backup roles si se activan (BE2, FE2, QA2, UX, DB)

### Estructura VTT a materializar (TL post-tropicalización)
- [ ] Release v1.0 Landing
- [ ] 6 Sprints S00-S05
- [ ] Phases SDLC (mínimo Development)
- [ ] Deliveries por sprint × cadena de rol
- [ ] 75 tareas (73 + SETUP-BLOQUE-LANDING + CIERRE-BLOQUE-LANDING)
- [ ] ~148 dependencias técnicas
- [ ] Project Plan MODO D (generatePlan)

---

## 14. Cómo invocar este operativo desde el agente

### Opción A — Path canónico
```
00-platform/05.proyectos/vtl/operativos-instancias/OPERATIVO_<ROL>.md
```

### Opción B — Symlink a `.claude/agents/` (si VTL adopta ese patrón)
Cuando aplique, los archivos de `.claude/agents/` pueden apuntar a estos via symlink o copia controlada.

---

## 15. Convenciones del proyecto VTL

| Aspecto | Convención |
|---------|------------|
| Branch principal | `main` (NUNCA `develop` — LL-004) |
| Commit format | `[<TASK_ID>] descripción` + Co-Authored-By + Refs |
| PR | siempre a `main` |
| Auth | JWT obligatorio (VTT-296 / LL-006) |
| Comentarios | campos `message` + `userId` (NO `content`/`authorId`) |
| On-hold | `PUT /on-hold` (NUNCA `PATCH /status` — ERR-006) |
| Sprint en tareas | vive en Delivery, NO en Task |
| Tech debt diferido | severity = medium/low (NUNCA high — bloquea gate) |
| Issues correctivos | crear tarea con `sourceIssueId` (NUNCA PUT manual) |
| Worktrees | NO se usan en VTL (proyecto chico) |
| Service key | `VTT_TL_SERVICE_KEY` del `.env` (NUNCA hardcodear) |

---

**Mantenedor:** TL VTL (Claude — `tech.lead@vtt-landing.ai`)
**Cambios:** vía PR al repo `virtual-teams-setup/`
**Versión:** 1.0 | **Fecha:** 2026-06-05
**Origen:** tropicalización de `vtt/INDEX.md` v1.0 (2026-05-29)
