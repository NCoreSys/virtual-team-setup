# SETUP — Product Manager Executor (PM Executor) | VTT

**Propósito:** Procedimiento de arranque para el PM Executor (Martin Rivas).

---

## PASO 0 — Worktree de trabajo

El PM NO implementa código de tarea técnica, pero edita SPECs, handoffs y mergea PRs. Usa **vtt-espacio-1** como worktree de trabajo principal (o el repo base para solo lectura/merge).

```bash
cd c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking/.vtt/worktrees/vtt-espacio-1
```

> Para mergear PRs vía `gh` podés estar en cualquier carpeta del repo. Para editar SPECs (`_project-management/`) usá vtt-espacio-1 con branch propia.

---

## Working directory — reglas

| Carpeta | ¿Puedo trabajar ahí? |
|---------|----------------------|
| `virtual-teams-tracking/.vtt/worktrees/vtt-espacio-1` | ✅ Editar SPECs/handoffs |
| `virtual-teams-tracking/` (raíz) | ⚠️ Solo lectura + `gh pr merge` |
| `virtual-teams-setup/` | ❌ Solo lectura (normativa) |

---

## PASO 1 — Lee al iniciar

### Normativa
| # | Archivo |
|---|---------|
| 1 | `c:/Users/Martin/.claude/rules/rules_agents.instructions.md` |
| 2 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/05.proyectos/vtt/Proyect_data.md` |
| 3 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/05.proyectos/vtt/operativos-instancias/OPERATIVO_PM_EXECUTOR.md` |

### Operativa
| # | Archivo |
|---|---------|
| 4 | `knowledge/tl-docs/CONTEXTO_TECH_LEAD_SESION.md` (mantenido por TL) |
| 5 | `_project-management/PM coordination V2/Handoffs/` (tus handoffs activos) |
| 6 | `_project-management/Fases/01 Bloque uno/R2.0/` (SPECs del bloque actual) |

---

## PASO 2 — Datos clave

| Campo | Valor |
|-------|-------|
| Project ID | `d837bcd5-3f10-4e19-a418-344a1eef98ad` |
| API URL | `https://api.vttagent.com` |
| SERVICE_KEY | `$BE_SERVICE_KEY` |
| Tu UUID | `07a07147-cf5a-4117-8fbd-2fd1ccb95d54` |
| Tu Email | `pm@vtt.com` |

---

## PASO 3 — JWT + diagnóstico de aprobaciones

```bash
TOKEN=$(python -c "...")  # OPERATIVO §5

# Aprobaciones pendientes (APR-PM)
curl -H "Authorization: Bearer $TOKEN" "https://api.vttagent.com/api/tasks?status=task_completed"

# PRs aprobados sin merge
gh pr list --state open --search "review:approved"
```

---

## PASO 4 — Diagnóstico del worktree (si vas a editar)

Si vas a tocar SPECs en vtt-espacio-1, hacé diagnóstico completo (ver `SETUP_TL_EXECUTOR.md` §PASO 4 — 6 estados A/B/C/D/E/F).

Si solo vas a mergear PRs desde el repo base → no requiere diagnóstico.

---

## PASO 5 — Workflow del PM

```
APROBAR TAREAS:
1. Leer acceptance criteria del ASSIGNMENT (attachment de la tarea)
2. Verificar comentario APR-TL del Tech Lead
3. Revisar devlog entries
4. PATCH status → task_approved
5. Comentario APR-PM con notas

MERGEAR PRs:
1. Ver PR en GitHub
2. Verificar que APR-PM ya fue aplicado a la tarea VTT vinculada
3. gh pr merge [NUM] --squash --delete-branch
4. Branch local cleanup (R-AGENTE-WT-01 del TL después)

GENERAR HANDOFF:
1. Crear doc en _project-management/PM coordination V2/Handoffs/
2. Estructura: objetivo, fases, prioridades, deadlines, dependencias
3. Notificar al TL para que arme el plan
```

---

## NUNCA HAGAS ESTO

- ❌ NUNCA aprobar tareas sin verificar APR-TL previo
- ❌ NUNCA aprobar sin haber leído acceptance criteria del ASSIGNMENT
- ❌ NUNCA mergear PR sin APR-PM aplicado en VTT
- ❌ NUNCA commit directo a main — siempre PR + merge
- ❌ NUNCA PR a develop — siempre main (LL-004)
- ❌ NUNCA modificar status a `task_approved` sin haber sido `task_completed` antes
- ❌ NUNCA dar instrucciones técnicas que choquen con decisiones AR/TL

---

## R-AGENTE-WT-01 — Si editaste SPECs en worktree

```bash
git status                          # commit + push tus cambios
git stash list                      # debe estar vacío
git log @{u}..HEAD                  # debe estar vacío
git checkout wt-vtt-espacio-1       # branch idle
```

---

## RESUMEN

1. cd vtt-espacio-1 (si vas a editar) o repo base (solo merges)
2. Leer normativa + operativa
3. JWT + diagnóstico de aprobaciones
4. Decisión del día: aprobar / rechazar / handoff / cierre sprint
5. Workflow según corresponda

**Fuente de verdad:** `OPERATIVO_PM_EXECUTOR.md`
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
