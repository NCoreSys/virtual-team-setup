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
| API URL | `https://api.vttagent.com` |

---

## PASO 3 — JWT + tareas pendientes APR-PM

```bash
TOKEN=$(...)
curl -H "Authorization: Bearer $TOKEN" "https://api.vttagent.com/api/tasks?status=task_completed"
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

---

## ANEXO (v1.1) — Donde encontrar el REPORT del agente que revisas

> **Cambio v1.1 (2026-06-03):** path canónico del REPORT cambió en SKILL-REPORT-001 v1.1.

Cuando revisas una tarea entregada por un agente ejecutor (BE, DB, FE, DO, etc.), el `<TASK_ID>_REPORT.md` vive en:

```
knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>_REPORT.md
```

⚠️ **Path legacy DEPRECADO** (NO buscar ahí para tareas nuevas):
```
knowledge/agent-tasks/reports/<phase>/<sprint>/<TASK_ID>_REPORT.md
```

El REPORT está en la MISMA carpeta que el `<TASK_ID>.json` + `<TASK_ID>.manifest.md` (los 3 archivos del manifest viven juntos).

Referencia normativa:
- `00-platform/02.normativa/03.Skills/report/VTT.SKILL-REPORT-001_entrega_tarea.md` v1.1 (R6: path canónico) — explica el formato esperado del REPORT (14 secciones) y dónde vive.

Si una tarea vieja tiene el REPORT en el path legacy, dejarlo (legacy compatible). Para tareas nuevas exigir el path canónico al agente. Si el agente entregó en path legacy → rechazar review hasta que mueva al canónico.

---

> **Cambio v1.1 (2026-06-03):** URL backend `:3000` → `https://api.vttagent.com` (VTT-870). SERVICE_KEY hardcoded → `$BE_SERVICE_KEY` del `.env` (rotada VTT-957). Agregado anexo SKILL-REPORT-001 con path canónico — alineado con SETUPs ejecutores.
