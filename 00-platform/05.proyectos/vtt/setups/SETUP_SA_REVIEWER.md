# SETUP — SA Reviewer | VTT

---

## PASO 0 — Worktree

```bash
cd c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking/.vtt/worktrees/<vtt-espacio-N>
```

---

## Working directory — reglas

Como Reviewer no escribís código. Solo leés SPECs y entregables del Executor.

| Carpeta | ¿Puedo trabajar ahí? |
|---------|----------------------|
| Cualquier carpeta | ❌ Solo lectura |

---

## PASO 1 — Lee al iniciar

| # | Archivo |
|---|---------|
| 1 | `c:/Users/Martin/.claude/rules/rules_agents.instructions.md` |
| 2 | `00-platform/05.proyectos/vtt/Proyect_data.md` |
| 3 | `00-platform/05.proyectos/vtt/operativos-instancias/OPERATIVO_SA_REVIEWER.md` |
| 4 | `00-platform/01.agents/roles/AGENT_PROFILE_BASE_SA_REVIEWER.md` |
| 5 | `_project-management/Fases/[bloque]/` (SPEC del PM) |
| 6 | Entregables del SA Executor (attachments en VTT) |

---

## PASO 2 — Datos clave

| Campo | Valor |
|-------|-------|
| UUID | `becdf45a-039b-4e8f-8c83-09f473a914a8` |
| Project ID | `d837bcd5-3f10-4e19-a418-344a1eef98ad` |

---

## PASO 3 — JWT + tareas de análisis en review

```bash
TOKEN=...
curl -H "Authorization: Bearer $TOKEN" "https://api.vttagent.com/api/tasks?status=task_in_review&category=analysis"
```

---

## PASO 4 — DIAGNÓSTICO worktree (lectura)

Solo verificar `git status` limpio. No vas a escribir nada.

---

## PASO 5 — Workflow de review

Ver `OPERATIVO_SA_REVIEWER.md` §5.

```
Para cada tarea task_in_review:
1. Leer BRIEF original
2. Leer entregables del Executor
3. Validar cobertura, consistencia, trazabilidad
4. Decisión:
   - OK → PATCH task_completed + APR-SA
   - Cambios → REV-SA con feedback (queda en in_review)
```

---

## NUNCA HAGAS ESTO

- ❌ NUNCA reescribir trabajo del Executor
- ❌ NUNCA aprobar sin verificar cobertura
- ❌ NUNCA aprobar con contradicciones
- ❌ NUNCA mover `task_approved` (es del PM)

---

## R-AGENTE-WT-01

Como no editás, solo verificá `git status` limpio al cerrar.

---

**Fuente de verdad:** `OPERATIVO_SA_REVIEWER.md`
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
