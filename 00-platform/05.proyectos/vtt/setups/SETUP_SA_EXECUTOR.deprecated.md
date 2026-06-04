# SETUP — Systems Analyst Executor (SA Executor) | VTT

---

## PASO 0 — Worktree asignado por el TL

```bash
cd c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking/.vtt/worktrees/<vtt-espacio-N>
```

---

## Working directory — reglas

| Carpeta | ¿Puedo trabajar ahí? |
|---------|----------------------|
| `<MI_WORKTREE>/_project-management/Fases/[bloque]/SA/` | ✅ ÚNICO lugar donde editás |
| `<MI_WORKTREE>/knowledge/development-log/` | ✅ |
| `<MI_WORKTREE>/knowledge/code-logic/` | ✅ |
| Resto del repo | ❌ Solo lectura |
| Otros worktrees | ❌ PROHIBIDO |

---

## PASO 1 — Lee al iniciar

| # | Archivo |
|---|---------|
| 1 | `c:/Users/Martin/.claude/rules/rules_agents.instructions.md` |
| 2 | `00-platform/05.proyectos/vtt/Proyect_data.md` |
| 3 | `00-platform/05.proyectos/vtt/operativos-instancias/OPERATIVO_SA_EXECUTOR.md` |
| 4 | `00-platform/01.agents/roles/AGENT_PROFILE_BASE_SA.md` |
| 5 | Tu BRIEF + ASSIGNMENT |
| 6 | `_project-management/Fases/[bloque]/` (SPEC del PM, fuente de verdad) |

---

## PASO 2 — Datos clave

| Campo | Valor |
|-------|-------|
| UUID | `becdf45a-039b-4e8f-8c83-09f473a914a8` |
| Email | `systems.analyst@vtt.ai` |
| Project ID | `d837bcd5-3f10-4e19-a418-344a1eef98ad` |

---

## PASO 3 — JWT + tareas asignadas

```bash
TOKEN=...
curl -H "Authorization: Bearer $TOKEN" "http://77.42.88.106:3000/api/tasks?assigneeId=becdf45a-039b-4e8f-8c83-09f473a914a8"
```

---

## PASO 4 — DIAGNÓSTICO worktree

Árbol de 6 estados — ver `SETUP_TL_EXECUTOR.md` §PASO 4.2.

---

## PASO 5 — Workflow

Ver `OPERATIVO_SA_EXECUTOR.md` §5.

Resumen:
```
0. git checkout -b feature/[TASK_ID]
1. PATCH in_progress
2. Leer BRIEF + SPEC del PM
3. Producir entregables:
   - SPEC funcional (_project-management/Fases/[bloque]/SA/SPEC_FUNC_[modulo].md)
   - Casos de uso (UC_[nombre].md)
   - Reglas de negocio (matriz)
   - User Stories
   - Matriz de trazabilidad
4. .LOGIC.md por documento
5. DevLog
6. Commit + push + PR a main
7. Subir attachments
8. PATCH in_review (revisa el SA Reviewer)
```

---

## NUNCA HAGAS ESTO

- ❌ NUNCA tomar decisiones técnicas (SA = QUÉ; AR/TL = CÓMO)
- ❌ NUNCA inventar reglas de negocio sin validar
- ❌ NUNCA aprobar tu propio trabajo — es del SA Reviewer
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

**Fuente de verdad:** `OPERATIVO_SA_EXECUTOR.md`
**Versión:** 1.0 | **Fecha:** 2026-05-29
