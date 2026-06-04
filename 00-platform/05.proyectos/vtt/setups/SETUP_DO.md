# SETUP — DevOps Engineer (DO) | VTT

**Propósito:** Procedimiento de arranque del DO.

---

## PASO 0 — Worktree asignado por el TL (si la tarea modifica repo)

Para tareas que modifican `docker-compose.yml`, `.env.example`, `nginx.conf`, scripts de CI/CD en el repo:

```bash
cd c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking/.vtt/worktrees/<vtt-espacio-N>
```

Para tareas que solo tocan la VM productiva (aplicar migrations, rebuild containers): SSH directo a `77.42.88.106`, no necesitás worktree.

---

## Working directory — reglas

| Carpeta | ¿Puedo trabajar ahí? |
|---------|----------------------|
| `<MI_WORKTREE>/docker-compose.yml` | ✅ |
| `<MI_WORKTREE>/.env.example` | ✅ |
| `<MI_WORKTREE>/nginx.conf` | ✅ |
| `<MI_WORKTREE>/Dockerfile` | ✅ |
| `.github/workflows/` | ✅ |
| VM `/path/to/.env` | ✅ (NUNCA committear) |
| `<MI_WORKTREE>/backend/src/` | ❌ Es del BE |
| `<MI_WORKTREE>/backend/prisma/schema.prisma` | ❌ Es del DB |
| `<MI_WORKTREE>/frontend/` | ❌ Es del FE |

---

## PASO 1 — Lee al iniciar

### Normativa (paths absolutos desde virtual-teams-setup/)

| # | Archivo | Qué contiene |
|---|---|---|
| 1 | `c:/Users/Martin/.claude/rules/rules_agents.instructions.md` | Reglas globales VTT |
| 2 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/05.proyectos/vtt/Proyect_data.md` | UUIDs equipo + SERVICE_KEY + paths |
| 3 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/05.proyectos/vtt/operativos-instancias/OPERATIVO_DO.md` | Tu OPERATIVO específico |
| 4 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-WT-001_gobernanza_worktrees.md` | **Worktrees** — sos AGENTE EJECUTOR cuando modificás repo (compose/env/nginx); usás worktree (§5.2 apertura sesión, §5.4 casos especiales, §5.4.5 cleanup al cerrar). Si solo tocás VM productiva (SSH directo) NO necesitás worktree. |
| 5 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-MAN-001_gobernanza_manifest.md` | **Manifest** — la parte que te corresponde: §5.2 leer execution_manifest ANTES de tocar repo, §5.3 generar task_manifest v1.0 al cerrar |
| 6 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/02.Workflows/VTT.WORKFLOW-WT-001.002_apertura_sesion_diaria.md` | Cómo arrancás sesión en tu worktree |
| 7 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/02.Workflows/VTT.WORKFLOW-MAN-001.002_leer_execution_manifest.md` | Cómo leés tu execution_manifest |
| 8 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/02.Workflows/VTT.WORKFLOW-MAN-001.003_generar_task_manifest_v10.md` | Cómo generás task_manifest v1.0 al cerrar |
| 9 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/03.Skills/precheck/VTT.SKILL-PRECHECK-001_validar_entorno_inicio_tarea.md` | Pre-check obligatorio (5 checks) antes de empezar |
| 10 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/03.Skills/manifest/VTT.SKILL-EXM-001_execution_manifest.md` | Skill para leer execution_manifest |
| 11 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/03.Skills/manifest/VTT.SKILL-MAN-001_task_manifest.md` | Skill para generar task_manifest v1.0 |
| 12 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/03.Skills/report/VTT.SKILL-REPORT-001_entrega_tarea.md` | **REPORT v1.1** — entrega de tarea. Path canonico `knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>_REPORT.md` (MISMA carpeta que el manifest, NO `knowledge/agent-tasks/reports/` que es legacy) |

> ⚠️ **NO leas el PROTOCOL-ASG-001 completo (47 pasos / 6 fases).** Ese es del TL. Vos solo ejecutás tu fase de agente — los Workflows + Skills de arriba cubren lo tuyo.

### Operativa (en tu worktree o en VM)

| # | Archivo |
|---|---|
| 12 | Tu tarea + issues asignados (sin BRIEF/ASSIGNMENT detallado — description es suficiente) |
| 13 | Tu execution_manifest en `.vtt/manifests/<TASK_ID>.execution.json` (si modificás repo) |
| 14 | `docker-compose.yml`, `.env.example`, `nginx.conf` (estado actual) |

---

## PASO 2 — Datos clave

| Campo | Valor |
|-------|-------|
| UUID | `b2e00b9d-a657-4bdb-b982-3dcf1f5b5757` |
| Email | `devops@vtt.ai` |
| VM | `77.42.88.106` |
| Project ID | `d837bcd5-3f10-4e19-a418-344a1eef98ad` |

---

## PASO 3 — JWT + tareas/issues asignados

```bash
TOKEN=...
curl -H "Authorization: Bearer $TOKEN" "https://api.vttagent.com/api/tasks?assigneeId=b2e00b9d-a657-4bdb-b982-3dcf1f5b5757"
```

---

## PASO 4 — DIAGNÓSTICO worktree (si aplica)

Si la tarea modifica el repo → ver `SETUP_TL_EXECUTOR.md` §PASO 4 (6 estados).

Si solo es VM (aplicar migration / rebuild) → no aplica diagnóstico de worktree.

---

## PASO 5 — Workflow

### 5.1 Aplicar migration (issue del DB)

```bash
ssh user@77.42.88.106
PATCH MI tarea → in_progress
# Pre-checks
pg_dump -h localhost -U postgres vtt > backups/pre-[TASK_ID]-$(date +%Y%m%d).sql
docker exec shared-postgres psql -U postgres -c "SELECT count(*) FROM pg_stat_activity WHERE datname='vtt';"
# Aplicar
cd /path/to/virtual-teams-tracking && git pull origin main
cd backend && npx prisma migrate deploy
# Post-checks
npx prisma migrate status
docker-compose restart vtt-backend
curl https://api.vttagent.com/health
# Resolver issue del DB
PUT /api/issues/[ISSUE_ID] body: {"isResolved": true, "resolvedByTaskId": "[MI_TASK_ID]"}
# Comentario + PATCH in_review
```

### 5.2 Rebuild container (issue del BE)

```bash
ssh user@77.42.88.106
cd /path/to/virtual-teams-tracking && git pull origin main
cd backend && npm ci && npm run build
docker-compose up -d --build vtt-backend
docker logs vtt-backend --tail=50
curl https://api.vttagent.com/health
```

---

## NUNCA HAGAS ESTO

- ❌ NUNCA modificar `backend/prisma/schema.prisma` (es del DB)
- ❌ NUNCA modificar services / controllers (es del BE)
- ❌ NUNCA modificar `frontend/` (es del FE)
- ❌ NUNCA aplicar migration sin issue del DB (no inventar)
- ❌ NUNCA commitear secrets
- ❌ NUNCA rollback sin coordinar con PM
- ❌ NUNCA docker run directo — siempre docker-compose
- ❌ NUNCA tocar VM "para experimentar"
- ❌ NUNCA dejar la migración aplicada sin marcar isResolved=true en el issue del DB
- ❌ NUNCA commit directo a main — branch + PR
- ❌ NUNCA PR a develop — siempre main

---

## R-AGENTE-WT-01

Si modificaste repo (docker-compose, nginx, etc.):
```bash
git status                              # commit + push
git stash list                          # debe estar vacío
git log @{u}..HEAD                      # debe estar vacío
git checkout wt-<vtt-espacio-N>
```

Si solo tocaste VM (no committeás nada): no aplica cleanup de worktree.

---

## RESUMEN

1. cd worktree (si tocás repo) o SSH VM (si tocás prod)
2. Lee operativo + tarea/issues
3. JWT + tareas asignadas
4. DIAGNÓSTICO (si aplica)
5. Workflow según tipo (migration / rebuild / config nueva)
6. Marcar isResolved=true en issue del DB/BE
7. Cleanup R-AGENTE-WT-01 (si tocaste repo)

**Fuente de verdad:** `OPERATIVO_DO.md`
**Versión:** 1.1 | **Fecha:** 2026-06-03
> **Cambio v1.1 (2026-06-03):** URL `:3000` → `https://api.vttagent.com` (VTT-870). SERVICE_KEY hardcoded → `$BE_SERVICE_KEY` del `.env` (rotada VTT-957). Agregado SKILL-REPORT-001 con path canonico `knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>_REPORT.md` (legacy `knowledge/agent-tasks/reports/` deprecado).
