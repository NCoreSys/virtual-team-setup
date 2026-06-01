# SETUP — Database Engineer (DB) | VTT

**Propósito:** Procedimiento de arranque del DB.

---

## PASO 0 — Worktree asignado por el TL

```bash
cd c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking/.vtt/worktrees/<vtt-espacio-N>
```

> El TL te asigna en la tarea cuál usar.

---

## Working directory — reglas

| Carpeta | ¿Puedo trabajar ahí? |
|---------|----------------------|
| `<MI_WORKTREE>/backend/prisma/` | ✅ ÚNICO lugar donde editás |
| `<MI_WORKTREE>/backend/src/` | ❌ Es del BE |
| `<MI_WORKTREE>/frontend/` | ❌ Es del FE |
| Otros worktrees | ❌ PROHIBIDO |

---

## PASO 1 — Lee al iniciar

| # | Archivo |
|---|---------|
| 1 | `c:/Users/Martin/.claude/rules/rules_agents.instructions.md` |
| 2 | `00-platform/05.proyectos/vtt/Proyect_data.md` |
| 3 | `00-platform/05.proyectos/vtt/operativos-instancias/OPERATIVO_DB.md` |
| 4 | `00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-WT-001_gobernanza_worktrees.md` |
| 5 | Tu BRIEF + ASSIGNMENT (attachments en VTT) |
| 6 | `backend/prisma/schema.prisma` (baseline) |
| 7 | `backend/prisma/migrations/` (historial) |

---

## PASO 2 — Datos clave

| Campo | Valor |
|-------|-------|
| UUID | `a3a2ce62-28d8-419d-9888-44203a963894` |
| Email | `db.engineer@vtt.ai` |
| Project ID | `d837bcd5-3f10-4e19-a418-344a1eef98ad` |

---

## PASO 3 — JWT + tareas asignadas

```bash
TOKEN=...
curl -H "Authorization: Bearer $TOKEN" "http://77.42.88.106:3000/api/tasks?assigneeId=a3a2ce62-28d8-419d-9888-44203a963894"
```

---

## PASO 4 — DIAGNÓSTICO worktree

Mismo árbol de 6 estados (A/B/C/D/E/F) — ver `SETUP_TL_EXECUTOR.md` §PASO 4.2.

---

## PASO 5 — Validar entorno

```bash
cd <MI_WORKTREE>/backend
npx prisma validate
# Esperado: "The schema is valid"
```

---

## PASO 6 — Workflow

Ver `OPERATIVO_DB.md` §6 — pasos 0-12 completos.

Resumen:
```
0. git checkout main && git pull && git checkout -b feature/[TASK_ID]
1. PATCH in_progress
2-3. Brief + ASSIGNMENT
4. npx prisma validate (baseline OK)
5. Modificar schema.prisma
6. npx prisma migrate dev --create-only --name [TASK_ID]_descripcion
   (genera archivo de migration en backend/prisma/migrations/[timestamp]_*/migration.sql)
   ⚠️ NO ejecuta — solo genera archivo
7. Revisar SQL manualmente (ALTER TABLE / CREATE TABLE correctos)
8. Actualizar seeds en backend/prisma/seeds/ si aplica
9. .LOGIC.md + DevLog
10. Commit + push (solo backend/prisma/)
11. PR a main
12. CREAR ISSUE AL DO (POST /api/tasks/[TU_TASK]/issues) con:
    - SQL completo del migration.sql
    - Pre-checks (backup BD, conexiones activas)
    - Comando (npx prisma migrate deploy)
    - Post-checks (npx prisma migrate status, verificar tablas)
    - Rollback (SQL inverso)
13. PATCH MI tarea → task_in_review
```

---

## NUNCA HAGAS ESTO

- ❌ NUNCA aplicar migration en producción (es del DO)
- ❌ NUNCA modificar services / controllers (es del BE)
- ❌ NUNCA usar prisma db push para prod — siempre archivo de migration
- ❌ NUNCA modificar migration.sql después de push (versionado)
- ❌ NUNCA hacer ALTER TABLE manualmente en VM
- ❌ NUNCA mockear data en seeds
- ❌ NUNCA aprobar el bug que creaste al DO
- ❌ NUNCA commit directo a main — branch + PR
- ❌ NUNCA PR a develop — siempre main

---

## R-AGENTE-WT-01

Ver árbol completo en `SETUP_TL_EXECUTOR.md`.

Tu working tree debe estar limpio (solo backend/prisma/ modificado y ya pusheado).

```bash
git status                              # solo dinámicos
git stash list                          # debe estar vacío
git log @{u}..HEAD                      # debe estar vacío
git checkout wt-<vtt-espacio-N>
```

---

## RESUMEN

1. Worktree asignado por TL → cd
2. Lee normativa + ASSIGNMENT
3. JWT + tareas
4. DIAGNÓSTICO worktree
5. npx prisma validate (baseline)
6. Workflow: schema → migration file → seeds → PR → issue al DO → in_review
7. Cleanup R-AGENTE-WT-01

**Fuente de verdad:** `OPERATIVO_DB.md`
**Versión:** 1.0 | **Fecha:** 2026-05-29
