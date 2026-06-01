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

| # | Archivo |
|---|---------|
| 1 | `c:/Users/Martin/.claude/rules/rules_agents.instructions.md` |
| 2 | `00-platform/05.proyectos/vtt/Proyect_data.md` |
| 3 | `00-platform/05.proyectos/vtt/operativos-instancias/OPERATIVO_DO.md` |
| 4 | Tu tarea + issues asignados (sin BRIEF/ASSIGNMENT detallado — description es suficiente) |
| 5 | `docker-compose.yml`, `.env.example`, `nginx.conf` (estado actual) |

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
curl -H "Authorization: Bearer $TOKEN" "http://77.42.88.106:3000/api/tasks?assigneeId=b2e00b9d-a657-4bdb-b982-3dcf1f5b5757"
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
curl http://77.42.88.106:3000/health
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
curl http://77.42.88.106:3000/health
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
**Versión:** 1.0 | **Fecha:** 2026-05-29
