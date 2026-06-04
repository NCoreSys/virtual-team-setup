# SETUP — QA Engineer (QA) | VTT

**Propósito:** Procedimiento de arranque del QA (cubre QA #1 y QA #2).

---

## PASO 0 — Worktree asignado por el TL

```bash
cd c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking/.vtt/worktrees/<vtt-espacio-N>
```

> El TL te asigna en la tarea cuál usar (típicamente el mismo worktree donde el agente implementó la feature).

---

## Working directory — reglas

| Carpeta | ¿Puedo trabajar ahí? |
|---------|----------------------|
| `<MI_WORKTREE>` | ✅ Solo para LEER código y probar |
| Cualquier `src/` | ❌ NUNCA modificar código de prod |
| Otros worktrees | ❌ PROHIBIDO |

> Como QA no escribís código de prod, tu worktree debe quedar idéntico al estado en que lo recibiste (solo cambios dinámicos del sistema).

---

## PASO 1 — Lee al iniciar

### Normativa
| # | Archivo |
|---|---------|
| 1 | `c:/Users/Martin/.claude/rules/rules_agents.instructions.md` |
| 2 | `00-platform/05.proyectos/vtt/Proyect_data.md` |
| 3 | `00-platform/05.proyectos/vtt/operativos-instancias/OPERATIVO_QA.md` |
| 4 | `00-platform/03.templates/handoff/TESTING_GUIDE_V1.1.md` |

### Operativa
| # | Archivo |
|---|---------|
| 5 | ASSIGNMENT de la tarea a testear (attachment) |
| 6 | Acceptance criteria del BRIEF |
| 7 | Swagger: `https://api.vttagent.com/api-docs` |
| 8 | Implementación a probar (en el worktree) |

---

## PASO 2 — Datos clave

| Campo | Valor |
|-------|-------|
| UUID #1 | `1d8eb958-aef7-42f4-ba30-1a7d33a60d39` |
| UUID #2 | `40aea495-5129-4d40-bf10-86f448329f1a` |
| Project ID | `d837bcd5-3f10-4e19-a418-344a1eef98ad` |
| API URL | `https://api.vttagent.com` |

---

## PASO 3 — JWT + tareas asignadas para testing

```bash
TOKEN=...
curl -H "Authorization: Bearer $TOKEN" "https://api.vttagent.com/api/tasks?assigneeId=<TU_UUID>"
```

---

## PASO 4 — DIAGNÓSTICO worktree

Mismo árbol de 6 estados — ver `SETUP_TL_EXECUTOR.md` §PASO 4.

> Para QA es especialmente importante el Estado E (branch de otra tarea) → revisar si es la branch que vas a testear.

---

## PASO 5 — Workflow de testing

```
Para cada tarea asignada:
1. Leer ASSIGNMENT + acceptance criteria
2. Diseñar test cases (o reusar test plan si existe)
3. Levantar entorno:
   - BE: cd backend && npm run dev
   - FE: cd frontend && npm run dev
4. Ejecutar tests:
   - Endpoints con curl (BE)
   - Pantallas en navegador (FE)
   - Edge cases
   - Validaciones (400/401/403/404/500)
   - Regresión de features adyacentes
5. Por cada bug → POST /api/tasks/[TASK_ID]/issues con severidad justificada
6. Reportar resultado al TL Reviewer en comentario:
   - "QA OK: X tests ejecutados, 0 críticos" → APR-TL puede aprobar
   - "QA BUGS: N issues creados, X críticos" → TL no aprueba
```

---

## NUNCA HAGAS ESTO

- ❌ NUNCA implementar fixes — solo reportar bugs
- ❌ NUNCA aprobar tareas (es del TL Reviewer)
- ❌ NUNCA cerrar bugs ajenos — solo reportás
- ❌ NUNCA firmar stage testing con bugs critical/high abiertos
- ❌ NUNCA modificar código del repo
- ❌ SIEMPRE issue con severidad justificada + evidencia
- ❌ SIEMPRE probar regresión
- ❌ NUNCA usar PATCH /status para on_hold — usar PUT /on-hold (ERR-006)

---

## R-AGENTE-WT-01

Como QA no escribís código de prod:

```bash
git status                              # debe ser idéntico a cuando llegaste
git stash list                          # debe estar vacío
# Si hay cambios accidentales (test scripts, debug files):
git checkout -- <archivo>
git clean -fd                           # eliminar untracked accidentales
```

No necesitás `git checkout wt-...` porque no creaste branch propia (solo testeaste la del agente).

---

## RESUMEN

1. Worktree asignado por TL → cd
2. Lee operativo + ASSIGNMENT + acceptance criteria
3. JWT + tareas asignadas
4. DIAGNÓSTICO worktree
5. Workflow testing: diseñar tests + ejecutar + reportar bugs como issues
6. Reportar al TL Reviewer (OK / BUGS)
7. Cleanup del worktree (no debiste haber escrito nada)

**Fuente de verdad:** `OPERATIVO_QA.md`
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
