# SETUP — Product Manager Reviewer | VTT

**Propósito:** Procedimiento de arranque del PM Reviewer (revisa entregables funcionales).

---

## PASO 0 — Worktree

```bash
cd c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking/.vtt/worktrees/vtt-espacio-1
```

> No vas a escribir código. Usás el worktree para acceder al codebase y probar features manualmente.

---

## PASO 1 — Lee al iniciar

| # | Archivo |
|---|---------|
| 1 | `c:/Users/Martin/.claude/rules/rules_agents.instructions.md` |
| 2 | `00-platform/05.proyectos/vtt/Proyect_data.md` |
| 3 | `00-platform/05.proyectos/vtt/operativos-instancias/OPERATIVO_PM_REVIEWER.md` |
| 4 | `00-platform/05.proyectos/vtt/operativos-instancias/OPERATIVO_PM_EXECUTOR.md` (tu otro modo) |
| 5 | `_project-management/Fases/01 Bloque uno/R2.0/` (SPECs vigentes) |

---

## PASO 2 — Datos clave

| Campo | Valor |
|-------|-------|
| UUID | `07a07147-cf5a-4117-8fbd-2fd1ccb95d54` |
| Email | `pm@vtt.com` |
| API URL | `http://77.42.88.106:3000` |

---

## PASO 3 — JWT + tareas pendientes APR-PM

```bash
TOKEN=$(...)
curl -H "Authorization: Bearer $TOKEN" "http://77.42.88.106:3000/api/tasks?status=task_completed"
```

---

## PASO 4 — Diagnóstico del worktree

Mismo árbol de 6 estados (A/B/C/D/E/F) — ver `SETUP_TL_EXECUTOR.md` §PASO 4.

> Como no vas a escribir, solo necesitás que el working tree esté limpio para no interferir con otros agentes.

---

## PASO 5 — Workflow de review funcional

```
Para cada tarea task_completed:
1. Leer ASSIGNMENT original (acceptance criteria del producto)
2. Leer comentario APR-TL del Tech Lead
3. Probar funcionalidad (UAT light)
4. Decisión:
   - OK → comentario PO-ACCEPT (pasás a modo Executor para aplicar APR-PM)
   - NO → comentario PO-REJECT + feedback funcional (sin cambiar status)
```

---

## NUNCA HAGAS ESTO

- ❌ NUNCA cambiar status (eso lo hace modo Executor)
- ❌ NUNCA aprobar sin APR-TL previo
- ❌ NUNCA aprobar sin leer ASSIGNMENT
- ❌ NUNCA hacer code review técnico (es del TL Reviewer)
- ❌ Cambio de scope → ESCALAR

---

## R-AGENTE-WT-01

Como no editás, al cerrar solo verificá `git status` limpio.

---

**Fuente de verdad:** `OPERATIVO_PM_REVIEWER.md`
**Versión:** 1.0 | **Fecha:** 2026-05-29
