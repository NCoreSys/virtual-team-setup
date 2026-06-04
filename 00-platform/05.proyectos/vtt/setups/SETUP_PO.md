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
curl -H "Authorization: Bearer $TOKEN" "https://api.vttagent.com/api/projects/d837bcd5-3f10-4e19-a418-344a1eef98ad/trackable-items?typeCode=USER_STORY"

# Tareas completed para UAT
curl -H "Authorization: Bearer $TOKEN" "https://api.vttagent.com/api/tasks?status=task_completed"
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

---

## ANEXO (v1.1) — Lecturas normativas obligatorias

> **Cambio v1.1 (2026-06-03):** este SETUP no tenía referencias a la normativa del manifest + worktrees + REPORT. Se agrega ahora como anexo para alinear con el resto de ejecutores. Antes de arrancar tu tarea, lee:

| # | Archivo | Qué contiene |
|---|---|---|
| N1 | `00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-WT-001_gobernanza_worktrees.md` | **Worktrees** — sos agente ejecutor, sí usás worktree (§5.2 apertura, §5.4 casos especiales, §5.4.5 cleanup) |
| N2 | `00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-MAN-001_gobernanza_manifest.md` | **Manifest** — §5.2 leer execution_manifest ANTES de tocar contenido, §5.3 generar task_manifest v1.0 al cerrar |
| N3 | `00-platform/02.normativa/02.Workflows/VTT.WORKFLOW-WT-001.002_apertura_sesion_diaria.md` | Cómo arrancás sesión en tu worktree |
| N4 | `00-platform/02.normativa/02.Workflows/VTT.WORKFLOW-MAN-001.002_leer_execution_manifest.md` | Cómo leés tu execution_manifest |
| N5 | `00-platform/02.normativa/02.Workflows/VTT.WORKFLOW-MAN-001.003_generar_task_manifest_v10.md` | Cómo generás task_manifest v1.0 al cerrar |
| N6 | `00-platform/02.normativa/03.Skills/precheck/VTT.SKILL-PRECHECK-001_validar_entorno_inicio_tarea.md` | Pre-check obligatorio (5 checks) antes de empezar |
| N7 | `00-platform/02.normativa/03.Skills/manifest/VTT.SKILL-EXM-001_execution_manifest.md` | Skill para leer execution_manifest |
| N8 | `00-platform/02.normativa/03.Skills/manifest/VTT.SKILL-MAN-001_task_manifest.md` | Skill para generar task_manifest v1.0 |
| N9 | `00-platform/02.normativa/03.Skills/report/VTT.SKILL-REPORT-001_entrega_tarea.md` | **REPORT v1.1** — entrega de tarea. Path canónico `knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>_REPORT.md` (MISMA carpeta que el manifest, NO `knowledge/agent-tasks/reports/` que es legacy) |

> ⚠️ **NO leas el PROTOCOL-ASG-001 completo (47 pasos / 6 fases).** Ese es del TL. Vos solo ejecutás tu fase de agente — los Workflows + Skills de arriba cubren lo tuyo.

### Path canónico del REPORT (v1.1)

```
knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>_REPORT.md
```

⚠️ El path legacy `knowledge/agent-tasks/reports/<phase>/<sprint>/` **NO se usa** desde v1.1. Si una tarea vieja tiene el REPORT ahí, dejarlo (legacy); para tareas nuevas el path canónico es `knowledge/task-manifests/`.

### Script normativo (para generar manifest v1.0 al cerrar)

```bash
python3 "$VTT_SETUP/00-platform/02.normativa/03.Skills/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py" \
  --task <TASK_ID> --version 1.0
```

Si SCRIPT-MAN-001 NO está disponible en tu worktree → `POST /issues type=question` escalando el gap. NO fabriques manifest manual sin escalación.

---

> **Cambio v1.1 (2026-06-03):** URL backend `:3000` → `https://api.vttagent.com` (VTT-870). SERVICE_KEY hardcoded → `$BE_SERVICE_KEY` del `.env` (rotada VTT-957). Anexo normativo agregado con PROTOCOL-MAN-001, PROTOCOL-WT-001, WORKFLOWs, SKILLs (PRECHECK, EXM, MAN, REPORT) — alineado al template BE/DB.
