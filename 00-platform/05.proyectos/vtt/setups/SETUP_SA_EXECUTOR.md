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
curl -H "Authorization: Bearer $TOKEN" "https://api.vttagent.com/api/tasks?assigneeId=becdf45a-039b-4e8f-8c83-09f473a914a8"
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
