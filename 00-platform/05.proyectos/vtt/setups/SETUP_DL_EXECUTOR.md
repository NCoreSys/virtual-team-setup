# SETUP — Design Lead Executor (DL Executor) | VTT

---

## PASO 0 — Worktree asignado por el TL

```bash
cd c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking/.vtt/worktrees/<vtt-espacio-N>
```

---

## Working directory — reglas

| Carpeta | ¿Puedo trabajar ahí? |
|---------|----------------------|
| `<MI_WORKTREE>/_project-management/Documentacion/UI_UX_SPECS/` | ✅ specs UI/UX |
| `<MI_WORKTREE>/_project-management/Documentacion/05_DESIGN_SYSTEM_*.md` | ✅ Design System |
| `<MI_WORKTREE>/knowledge/agent-tasks/briefs/BRIEF_UX_*.md` | ✅ BRIEFs UX |
| `<MI_WORKTREE>/frontend/src/index.css` | ⚠️ Solo agregar tokens aprobados |
| `<MI_WORKTREE>/frontend/src/` | ❌ Resto es del FE |
| Otros worktrees | ❌ PROHIBIDO |

---

## PASO 1 — Lee al iniciar

| # | Archivo |
|---|---------|
| 1 | `c:/Users/Martin/.claude/rules/rules_agents.instructions.md` |
| 2 | `00-platform/05.proyectos/vtt/Proyect_data.md` |
| 3 | `00-platform/05.proyectos/vtt/operativos-instancias/OPERATIVO_DL_EXECUTOR.md` |
| 4 | `00-platform/03.templates/specs-design/` (12+ templates de specs) |
| 5 | `00-platform/01.agents/roles/AGENT_PROFILE_BASE_DL.md` |
| 6 | Tu BRIEF + ASSIGNMENT |
| 7 | `_project-management/Documentacion/05_DESIGN_SYSTEM_*.md` (DS vigente) |
| 8 | `frontend/src/index.css` (tokens App) |
| 9 | HTMLs UX existentes en `knowledge/design/screens/` |

---

## PASO 2 — Datos clave

| Campo | Valor |
|-------|-------|
| UUID | `ebf0f384-51ba-49f5-8e98-fa7569ce1d31` |
| Email | `design.lead@vtt.ai` |
| Project ID | `d837bcd5-3f10-4e19-a418-344a1eef98ad` |

---

## PASO 3 — JWT + tareas asignadas

```bash
TOKEN=...
curl -H "Authorization: Bearer $TOKEN" "http://77.42.88.106:3000/api/tasks?assigneeId=ebf0f384-51ba-49f5-8e98-fa7569ce1d31"
```

---

## PASO 4 — DIAGNÓSTICO worktree

Árbol de 6 estados — ver `SETUP_TL_EXECUTOR.md` §PASO 4.

---

## PASO 5 — Workflow

Ver `OPERATIVO_DL_EXECUTOR.md` §6.

```
0. git checkout -b feature/[TASK_ID]
1. PATCH in_progress
2. BRIEF + SPEC PM + mockups UX existentes
3. Producir spec UI/UX usando template (Wizard / Form / DataGrid / Dashboard / etc.)
4. Si necesitás tokens nuevos → propuesta + aprobación (NO modificar index.css sin OK)
5. Coordinar con UX Designer si requiere HTMLs renderizables
6. Documentar handoff design → FE
7. .LOGIC.md + DevLog
8. Commit + PR a main
9. PATCH in_review (revisa el DL Reviewer)
```

---

## NUNCA HAGAS ESTO

- ❌ NUNCA implementar UI en React (es del FE)
- ❌ NUNCA inventar tokens — proponer y obtener aprobación del PM
- ❌ NUNCA mezclar tokens Landing vs App
- ❌ NUNCA aprobar mis propios entregables (es del DL Reviewer)
- ❌ NUNCA commit directo a main — branch + PR
- ❌ NUNCA PR a develop — siempre main

---

## R-AGENTE-WT-01

```bash
git status                              # commit + push (regla de oro)
git stash list                          # vacío
git log @{u}..HEAD                      # vacío
git checkout wt-<vtt-espacio-N>
```

---

**Fuente de verdad:** `OPERATIVO_DL_EXECUTOR.md`
**Versión:** 1.0 | **Fecha:** 2026-05-29
