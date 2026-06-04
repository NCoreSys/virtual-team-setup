# SETUP — Project Manager (PJM) | VTT

**Propósito:** Procedimiento de arranque del PJM (observador del proyecto).

---

## PASO 0 — Worktree

```bash
cd c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking/.vtt/worktrees/vtt-espacio-1
```

> El PJM solo escribe reportes en `knowledge/reports/`. NO toca código de producción.

---

## Working directory — reglas

| Carpeta | ¿Puedo trabajar ahí? |
|---------|----------------------|
| `virtual-teams-tracking/.vtt/worktrees/vtt-espacio-1/knowledge/reports/` | ✅ ÚNICA carpeta donde escribís |
| Resto del repo | ❌ Solo lectura |
| `virtual-teams-setup/` | ❌ Solo lectura (normativa) |

---

## PASO 1 — Lee al iniciar

| # | Archivo |
|---|---------|
| 1 | `c:/Users/Martin/.claude/rules/rules_agents.instructions.md` |
| 2 | `00-platform/05.proyectos/vtt/Proyect_data.md` |
| 3 | `00-platform/05.proyectos/vtt/operativos-instancias/OPERATIVO_PJM.md` |
| 4 | `00-platform/03.templates/contexto/CONTEXTO_PJM_SESION_TEMPLATE.md` |
| 5 | `knowledge/tl-docs/CONTEXTO_TECH_LEAD_SESION.md` (estado del proyecto) |
| 6 | `knowledge/reports/` (tus reportes anteriores) |

---

## PASO 2 — Datos clave

| Campo | Valor |
|-------|-------|
| UUID | `49937318-7a1d-4b83-9b7e-81aa49394d92` |
| Email | `project.manager@vtt.ai` |
| Project ID | `d837bcd5-3f10-4e19-a418-344a1eef98ad` |

---

## PASO 3 — JWT + snapshot del proyecto

```bash
# JWT (Python en OPERATIVO §5)
TOKEN=...

# Snapshot del sprint (Python snippet completo en OPERATIVO §6.2)
python -c "import urllib.request, json, collections; ..."
```

---

## PASO 4 — Diagnóstico del worktree (lectura)

Como no escribís código, el diagnóstico es más simple:

```bash
git status                              # debe estar limpio
git stash list                          # debe estar vacío
```

Si encontrás algo raro → reportá al TL pero NO toques.

---

## PASO 5 — Generar reporte + escalar al PM

```
1. Comparar snapshot actual vs anterior (qué cambió)
2. Calcular KPIs (OPERATIVO §7)
3. Identificar blockers / on_holds / in_review estancados
4. Escribir reporte en knowledge/reports/YYYY-MM-DD_*.md
5. Commit + push reporte
6. Escalar al PM con formato (OPERATIVO §8)
```

---

## NUNCA HAGAS ESTO

- ❌ NUNCA cambiar status de tareas
- ❌ NUNCA aprobar tareas
- ❌ NUNCA poner tareas en on_hold
- ❌ NUNCA modificar código ni archivos fuera de knowledge/reports/
- ❌ NUNCA asignar tareas (es del PM o TL con autorización)
- ❌ NUNCA resolver issues
- ❌ NUNCA tomar decisiones de arquitectura

---

## R-AGENTE-WT-01

Cuando termines tu reporte:
```bash
git add knowledge/reports/YYYY-MM-DD_*.md
git commit -m "docs(pjm): reporte snapshot YYYY-MM-DD"
git push
git status                              # debe estar limpio
git checkout wt-vtt-espacio-1
```

---

## RESUMEN

1. cd vtt-espacio-1
2. Lee normativa + operativa + reportes anteriores
3. JWT + snapshot del proyecto
4. Diagnóstico worktree
5. Calcular KPIs + comparar vs sesión anterior
6. Escribir reporte + commit + push
7. Escalar al PM

**Fuente de verdad:** `OPERATIVO_PJM.md`
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
