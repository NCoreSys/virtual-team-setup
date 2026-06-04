# SETUP — UX Designer (UX) | VTT

---

## PASO 0 — Worktree asignado por el TL

```bash
cd c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking/.vtt/worktrees/<vtt-espacio-N>
```

---

## Working directory — reglas

| Carpeta | ¿Puedo trabajar ahí? |
|---------|----------------------|
| `<MI_WORKTREE>/knowledge/design/screens/` | ✅ ÚNICO lugar donde editás |
| `<MI_WORKTREE>/knowledge/development-log/` | ✅ |
| `<MI_WORKTREE>/knowledge/code-logic/` | ✅ |
| `<MI_WORKTREE>/frontend/` | ❌ Es del FE |
| Otros worktrees | ❌ PROHIBIDO |

---

## PASO 1 — Lee al iniciar

| # | Archivo |
|---|---------|
| 1 | `c:/Users/Martin/.claude/rules/rules_agents.instructions.md` |
| 2 | `00-platform/05.proyectos/vtt/Proyect_data.md` |
| 3 | `00-platform/05.proyectos/vtt/operativos-instancias/OPERATIVO_UX.md` |
| 4 | `00-platform/03.templates/specs-design/` (templates de specs) |
| 5 | `00-platform/01.agents/roles/AGENT_PROFILE_BASE_UX.md` |
| 6 | Tu BRIEF UX (attachment, creado por DL) |
| 7 | `_project-management/Documentacion/05_DESIGN_SYSTEM_*.md` |
| 8 | `frontend/src/index.css` (tokens App) |
| 9 | HTMLs existentes en `knowledge/design/screens/` |

---

## PASO 2 — Datos clave

| Campo | Valor |
|-------|-------|
| UUID | `ce8a2ace-21cb-44e9-978b-aa5f45977478` |
| Email | `ux.designer@vtt.ai` |
| Project ID | `d837bcd5-3f10-4e19-a418-344a1eef98ad` |

---

## PASO 3 — JWT + tareas asignadas

```bash
TOKEN=...
curl -H "Authorization: Bearer $TOKEN" "http://77.42.88.106:3000/api/tasks?assigneeId=ce8a2ace-21cb-44e9-978b-aa5f45977478"
```

---

## PASO 4 — DIAGNÓSTICO worktree

Árbol de 6 estados — ver `SETUP_TL_EXECUTOR.md` §PASO 4.

---

## PASO 5 — Workflow

Ver `OPERATIVO_UX.md` §6.

```
0. git checkout -b feature/[TASK_ID]
1. PATCH in_progress
2. Leer BRIEF UX del DL
3. Generar HTML(s):
   - Estructura semántica (header/main/section)
   - Tokens del DS (no hex hardcoded)
   - Estados (loading/empty/error/success) cada uno con sección demarcada
   - Variantes responsive si BRIEF lo pide
   - Comentarios HTML explicando comportamientos interactivos
4. Probar en navegador (file://) — sin errores
5. .LOGIC.md con decisiones de diseño
6. DevLog
7. Commit + push + PR a main
8. Subir HTMLs + screenshots como attachments
9. PATCH in_review (revisa el DL Reviewer)
```

---

## NUNCA HAGAS ESTO

- ❌ NUNCA programar React/JS funcional — solo HTML+CSS
- ❌ NUNCA conectar APIs
- ❌ NUNCA hex hardcoded — siempre tokens del DS
- ❌ NUNCA mezclar tokens Landing vs App
- ❌ NUNCA inventar diseño sin BRIEF del DL — coordinar
- ❌ NUNCA aprobar mis pantallas (es del DL Reviewer)
- ❌ NUNCA commit directo a main — branch + PR
- ❌ NUNCA PR a develop — siempre main

---

## R-AGENTE-WT-01

```bash
git status                              # commit + push HTMLs
git stash list                          # vacío
git log @{u}..HEAD                      # vacío
git checkout wt-<vtt-espacio-N>
```

---

**Fuente de verdad:** `OPERATIVO_UX.md`
**Versión:** 1.0 | **Fecha:** 2026-05-29
