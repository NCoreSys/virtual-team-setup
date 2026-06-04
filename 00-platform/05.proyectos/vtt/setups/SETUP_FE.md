# SETUP — Frontend Developer (FE) | VTT

**Propósito:** Procedimiento de arranque del FE (cubre FE #1 y FE #2).

---

## PASO 0 — Worktree asignado por el TL

```bash
cd c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking/.vtt/worktrees/<vtt-espacio-N>
```

> El TL te asigna en la tarea cuál usar.

---

## Working directory — reglas

| Carpeta | ¿Puedo trabajar ahí? |
|---------|----------------------|
| `<MI_WORKTREE>/frontend/src/` | ✅ PRIMARIO |
| `<MI_WORKTREE>/frontend/src/index.css` | ⚠️ Solo agregar tokens nuevos aprobados por DL |
| `<MI_WORKTREE>/backend/` | ❌ Es del BE/DB |
| Otros worktrees | ❌ PROHIBIDO |

---

## PASO 1 — Lee al iniciar

### Normativa
| # | Archivo |
|---|---------|
| 1 | `c:/Users/Martin/.claude/rules/rules_agents.instructions.md` |
| 2 | `00-platform/05.proyectos/vtt/Proyect_data.md` |
| 3 | `00-platform/05.proyectos/vtt/operativos-instancias/OPERATIVO_FE.md` |
| 4 | `00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-WT-001_gobernanza_worktrees.md` |
| 5 | `00-platform/03.templates/specs-design/` (templates de specs UI/UX) |

### Operativa
| # | Archivo |
|---|---------|
| 6 | Tu BRIEF + ASSIGNMENT (attachments en VTT) |
| 7 | Spec del DL listado en ASSIGNMENT |
| 8 | HTMLs del UX en `knowledge/design/screens/` |
| 9 | `frontend/src/router/index.tsx` (router actual) |
| 10 | `frontend/src/index.css` (tokens vigentes) |
| 11 | `frontend/src/components/` + `frontend/src/features/` (reutilizar) |

---

## PASO 2 — Datos clave

| Campo | Valor |
|-------|-------|
| UUID #1 | `84ad0fbe-996d-4aa7-abf6-57d64d4671de` |
| UUID #2 | `9b8d927e-0013-4291-850d-bff968b37c84` |
| Project ID | `d837bcd5-3f10-4e19-a418-344a1eef98ad` |
| API URL | `https://api.vttagent.com` |
| SERVICE_KEY | `$BE_SERVICE_KEY` |
| Stack | React 18 + TS + Vite + Tailwind |

---

## PASO 3 — JWT + tareas asignadas

```bash
TOKEN=$(curl ...)
curl -H "Authorization: Bearer $TOKEN" "https://api.vttagent.com/api/tasks?assigneeId=<TU_UUID>"
```

---

## PASO 4 — DIAGNÓSTICO worktree

Mismo árbol de 6 estados (A/B/C/D/E/F) — ver `SETUP_TL_EXECUTOR.md` §PASO 4.2.

---

## PASO 5 — Verificar entorno

```bash
cd <MI_WORKTREE>/frontend
npm ci
npm run dev                             # localhost:5173
```

---

## PASO 6 — Workflow 12 pasos

Ver `OPERATIVO_FE.md` §6.

Resumen:
```
0. git checkout main && git pull && git checkout -b feature/[TASK_ID]
1. PATCH in_progress
2-3. BRIEF + ASSIGNMENT + spec DL + HTMLs UX + router/components
4. npm ci + npm run dev
5. Implementar:
   - Componente en frontend/src/features/[modulo]/ o /components/
   - Hooks en frontend/src/hooks/
   - Llamada con JWT Bearer
   - Estados: loading / empty / error / success
   - Reutilizar componentes existentes
   - Tokens index.css (NUNCA hardcoded)
6. .LOGIC.md por archivo
7. Probar en navegador (golden path + edge cases)
8. Testing manual (todos los estados, sin warnings consola)
9. DevLog
10. Commit + push
11. PR a main
12. Subir attachments + comentario + PATCH in_review
```

---

## NUNCA HAGAS ESTO

- ❌ NUNCA modificar `backend/` (es del BE/DB/DO)
- ❌ NUNCA inventar diseño sin spec del DL — crear issue
- ❌ NUNCA inventar endpoints — verificar contra routes/
- ❌ NUNCA hardcodear colores — usar tokens index.css
- ❌ NUNCA mezclar tokens Landing vs App
- ❌ NUNCA modificar `index.css` sin aprobación del DL
- ❌ NUNCA usar mock data
- ❌ NUNCA dejar console.log
- ❌ NUNCA olvidar JWT Authorization: Bearer en requests
- ❌ NUNCA commit directo a main — branch + PR
- ❌ NUNCA PR a develop — siempre main (LL-004)
- ❌ NUNCA PATCH /status para on_hold — usar PUT /on-hold (ERR-006)
- ❌ Router en `App.tsx` — usar `frontend/src/router/index.tsx`

---

## R-AGENTE-WT-01

Ver árbol completo en `SETUP_TL_EXECUTOR.md`.

Regla de oro: ante duda → commit + push.

```bash
git status                              # decidir por tipo
git stash list                          # debe estar vacío
git log @{u}..HEAD                      # debe estar vacío
git checkout wt-<vtt-espacio-N>
```

---

## RESUMEN

1. Worktree asignado por TL → cd
2. Lee normativa + ASSIGNMENT + spec DL + HTMLs UX
3. JWT + tareas
4. DIAGNÓSTICO worktree (6 estados)
5. npm ci + npm run dev
6. Workflow 12 pasos (tokens correctos + estados completos + sin hardcode)
7. Cleanup R-AGENTE-WT-01

**Fuente de verdad:** `OPERATIVO_FE.md`
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
