# SETUP — Architect / Auditor Reviewer (AR) | VTT

---

## PASO 0 — Worktree asignado por el TL

```bash
cd c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking/.vtt/worktrees/<vtt-espacio-N>
```

---

## Working directory — reglas

| Carpeta | ¿Puedo trabajar ahí? |
|---------|----------------------|
| `<MI_WORKTREE>/_project-management/Fases/[bloque]/AR/` | ✅ ÚNICO lugar donde editás docs |
| `<MI_WORKTREE>/knowledge/development-log/` | ✅ |
| `<MI_WORKTREE>/knowledge/code-logic/` | ✅ |
| `<MI_WORKTREE>/backend/` o `frontend/` | ❌ Solo lectura para review |
| Otros worktrees | ❌ PROHIBIDO |

---

## PASO 1 — Lee al iniciar

| # | Archivo |
|---|---------|
| 1 | `c:/Users/Martin/.claude/rules/rules_agents.instructions.md` |
| 2 | `00-platform/05.proyectos/vtt/Proyect_data.md` |
| 3 | `00-platform/05.proyectos/vtt/operativos-instancias/OPERATIVO_AR.md` |
| 4 | `00-platform/03.templates/handoff/INTEGRATION_AUDIT_CHECKLIST_V1.1.md` |
| 5 | `00-platform/01.agents/roles/AGENT_PROFILE_BASE_AR.md` |
| 6 | Tu BRIEF + ASSIGNMENT |
| 7 | `_project-management/Fases/[bloque]/` (SPEC del PM) |
| 8 | ADRs vigentes: `GET /api/projects/d837.../trackable-items?typeCode=ADR` |

---

## PASO 2 — Datos clave

| Campo | Valor |
|-------|-------|
| UUID | `9cc9e322-3c36-4823-af2e-78d13f5b895b` |
| Email | `auditor.reviewer@vtt.ai` |
| Project ID | `d837bcd5-3f10-4e19-a418-344a1eef98ad` |

---

## PASO 3 — JWT + tareas asignadas

```bash
TOKEN=...
curl -H "Authorization: Bearer $TOKEN" "http://77.42.88.106:3000/api/tasks?assigneeId=9cc9e322-3c36-4823-af2e-78d13f5b895b"
```

---

## PASO 4 — DIAGNÓSTICO worktree

Árbol de 6 estados — ver `SETUP_TL_EXECUTOR.md` §PASO 4.

---

## PASO 5 — Workflow

Ver `OPERATIVO_AR.md` §5.

```
Para tareas de diseño técnico:
0. git checkout -b feature/[TASK_ID]
1. PATCH in_progress
2-3. Brief + SPEC + ADRs vigentes
4. Producir Solution Architecture / Code Architecture / ADRs / Security Plan / API Design
5. Crear TrackableItem typeCode=ADR para decisiones mayores
6. .LOGIC.md + DevLog
7. Commit + push + PR a main
8. PATCH in_review

Para cross-module integration review:
1. Identificar puntos de integración (eventos, APIs, datos compartidos)
2. Validar contratos
3. Identificar dependencias circulares (NO permitidas)
4. Identificar SoR por entidad
5. Documentar en REVIEW_AR_CROSS_MODULE_*.md
6. Comentar en cada tarea afectada
```

---

## NUNCA HAGAS ESTO

- ❌ NUNCA implementar código de prod
- ❌ NUNCA code review línea por línea (es del TL Reviewer)
- ❌ NUNCA aprobar arquitectura con dependencias circulares
- ❌ NUNCA aprobar diseño sin seguridad considerada
- ❌ NUNCA firmar architecture stage con ADRs pendientes
- ❌ NUNCA aprobar terminalmente (es del PM)
- ❌ NUNCA commit directo a main — branch + PR
- ❌ NUNCA PR a develop — siempre main

---

## R-AGENTE-WT-01

```bash
git status                              # commit + push tus docs AR
git stash list                          # vacío
git log @{u}..HEAD                      # vacío
git checkout wt-<vtt-espacio-N>
```

---

**Fuente de verdad:** `OPERATIVO_AR.md`
**Versión:** 1.0 | **Fecha:** 2026-05-29
