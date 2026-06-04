# SETUP — Product Owner (PO) | VTT

**Propósito:** Procedimiento de arranque del PO.

---

## PASO 0 — Worktree

```bash
cd c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking/.vtt/worktrees/vtt-espacio-1
```

> El PO no escribe código de producción. Usás el worktree para hacer UAT en el codebase real y editar `_project-management/PO/roadmap.md`.

---

## PASO 1 — Lee al iniciar

| # | Archivo |
|---|---------|
| 1 | `c:/Users/Martin/.claude/rules/rules_agents.instructions.md` |
| 2 | `00-platform/05.proyectos/vtt/Proyect_data.md` |
| 3 | `00-platform/05.proyectos/vtt/operativos-instancias/OPERATIVO_PO.md` |
| 4 | `_project-management/Fases/01 Bloque uno/R2.0/` (SPECs vigentes) |
| 5 | `_project-management/PO/roadmap.md` (si existe) |

---

## PASO 2 — Datos clave

| Campo | Valor |
|-------|-------|
| UUID | `4128b577-eec1-4bc2-a595-42bd6b43db5e` |
| Email | `product.owner@vtt.ai` |
| Project ID | `d837bcd5-3f10-4e19-a418-344a1eef98ad` |

---

## PASO 3 — JWT + listar backlog

```bash
TOKEN=...
# User Stories activas
curl -H "Authorization: Bearer $TOKEN" "http://77.42.88.106:3000/api/projects/d837bcd5-3f10-4e19-a418-344a1eef98ad/trackable-items?typeCode=USER_STORY"

# Tareas completed para UAT
curl -H "Authorization: Bearer $TOKEN" "http://77.42.88.106:3000/api/tasks?status=task_completed"
```

---

## PASO 4 — Diagnóstico del worktree

Mismo árbol de 6 estados (A/B/C/D/E/F) — ver `SETUP_TL_EXECUTOR.md` §PASO 4.

---

## PASO 5 — Workflow del PO

```
BACKLOG GROOMING:
1. Revisar User Stories abiertas
2. Priorizar con PM
3. Refinar acceptance criteria
4. POST /trackable-items typeCode=USER_STORY (si nuevas)
5. Vincular a tareas técnicas: POST /trackable-items/{id}/tasks

UAT:
1. Leer User Story vinculada
2. Probar funcionalidad como usuario final
3. Decisión: PO-ACCEPT / PO-REJECT (solo comentario, NO cambiar status)
4. PM decide APR-PM final

DIFERIR:
POST /trackable-items/{id}/defer body: {reason, targetType, targetSprintId}
```

---

## NUNCA HAGAS ESTO

- ❌ NUNCA cambiar status de tareas
- ❌ NUNCA aprobar terminalmente
- ❌ NUNCA priorizar fuera de la visión del PM
- ❌ NUNCA cambiar scope sin escalar
- ❌ Acceptance criteria ambiguos
- ❌ UAT como dev — siempre como usuario final
- ❌ Cancelar User Stories (es del PM) — diferir es OK

---

## R-AGENTE-WT-01

Si editaste `_project-management/PO/roadmap.md`:
```bash
git add _project-management/PO/
git commit -m "docs(po): actualización roadmap"
git push
git checkout wt-vtt-espacio-1
```

---

**Fuente de verdad:** `OPERATIVO_PO.md`
**Versión:** 1.0 | **Fecha:** 2026-05-29
