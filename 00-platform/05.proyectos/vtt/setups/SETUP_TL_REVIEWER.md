# SETUP — Tech Lead Reviewer (TL-R / Coordinador) | VTT

**Propósito:** Procedimiento de arranque para el TL Reviewer del proyecto VTT.

**REGLA CRÍTICA (`VTT.PROTOCOL-WT-001 v1.1` §2):** El TL Reviewer **NO usa worktrees**. Los worktrees son SOLO para agentes ejecutores. Yo opero directamente en el **repo padre `virtual-teams-tracking/`** en modo lectura/auditoría. Si necesito modificar código → asigno tarea al TL Executor (sesión separada, mismo UUID), él trabaja en su worktree.

---

## PASO 0 — Posicionarte en el repo padre

```bash
cd c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking
git fetch origin
git checkout main && git pull --ff-only origin main
```

> Trabajás sobre `main` actualizado. Para revisar el PR de un agente, hacés checkout temporal de su branch (PASO 4) sin tocar los worktrees del agente.

---

## Working directory — reglas

| Carpeta | ¿Puedo trabajar ahí? |
|---------|----------------------|
| `virtual-teams-tracking/` (raíz, repo padre) | ✅ **PRIMARIO** — lectura, audit, checkout temporal de PRs |
| `virtual-teams-tracking/.vtt/manifests/` | ✅ **AUXILIAR** — generar manifest v1.5 al cerrar review |
| `virtual-teams-tracking/.vtt/worktrees/vtt-espacio-*` | ❌ **PROHIBIDO** — son de los Executors. NO `cd` ahí ni hacer checkout |
| `virtual-teams-setup/` | ❌ **PROHIBIDO para edición** — repo normativa (solo lectura como referencia) |

---

## PASO 1 — Lee estos archivos al iniciar (paths absolutos)

### Normativa (repo `virtual-teams-setup/`)

| # | Archivo | Qué contiene |
|---|---------|--------------|
| 1 | `c:/Users/Martin/.claude/rules/rules_agents.instructions.md` | Reglas globales VTT |
| 2 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/05.proyectos/vtt/Proyect_data.md` | UUIDs + service key + paths |
| 3 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/05.proyectos/vtt/operativos-instancias/OPERATIVO_TL_REVIEWER.md` | Tu OPERATIVO |
| 4 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-WT-001_gobernanza_worktrees.md` | Worktrees v1.1 — **Reviewers NO usan worktrees** |
| 5 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-ASG-001_ciclo_asignacion_tarea.md` | **Ciclo asignación + cierre canónico (47 pasos, 6 fases)** — reemplaza `_pending-migration/PROCESO_ASIGNACION_TAREAS.md` |
| 6 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-DEV-001_ciclo_devlog_entry.md` | Lifecycle devlog en review (FASE 3) |
| 7 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-MAN-001_gobernanza_manifest.md` | Manifest v1.0 (agente) / v1.5 (TL al cerrar) |
| 8 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/03.Skills/precheck/VTT.SKILL-PRECHECK-001_validar_entorno_inicio_tarea.md` | Pre-check de entorno al iniciar sesión |
| 9 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/03.Skills/report/VTT.SKILL-REPORT-001_entrega_tarea.md` | Formato canónico del reporte v1.1 |

### Operativa (repo `virtual-teams-tracking/`)

| # | Archivo | Qué contiene |
|---|---------|--------------|
| 6 | `knowledge/tl-docs/CONTEXTO_TECH_LEAD_SESION.md` | Estado actual del sprint |

---

## PASO 2 — Datos clave del proyecto VTT

| Campo | Valor |
|-------|-------|
| Project ID | `d837bcd5-3f10-4e19-a418-344a1eef98ad` |
| Project Key | VTT |
| API URL | `https://api.vttagent.com` |
| SERVICE_KEY | `$BE_SERVICE_KEY` |
| Tu UUID | `abdff0db-ad0b-4a0c-99f5-c898d18bd2d8` |
| Tu Email | `tech.lead@vtt.ai` |

---

## PASO 3 — JWT + diagnóstico del sprint

```bash
# Obtener JWT (en OPERATIVO §5)
TOKEN=$(curl ...)

# Diagnóstico inicial
curl -H "Authorization: Bearer $TOKEN" "https://api.vttagent.com/api/tasks?status=task_in_review"
curl -H "Authorization: Bearer $TOKEN" "https://api.vttagent.com/api/tasks?status=task_on_hold"
curl -H "Authorization: Bearer $TOKEN" "https://api.vttagent.com/api/tasks?status=task_pending"
```

Reportar al PM (formato §8 del OPERATIVO).

---

## PASO 4 — Revisar PR de un agente (sin worktree)

Cuando una tarea pasa a `task_in_review`, hacés checkout temporal de su branch **en el repo padre** (NO en worktrees):

```bash
cd c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking

# 1. Sincronizar
git fetch origin

# 2. Checkout temporal de la branch del PR (sin tocar worktrees del agente)
git checkout feature/<TASK_ID>
# o si el PR está en otra rama: git checkout -b review-<TASK_ID> origin/<branch_del_pr>

# 3. Revisar: leer código, ejecutar curl al endpoint, validar criterios
# ...

# 4. Volver a main al terminar
git checkout main
git pull --ff-only origin main
```

**5 verificaciones obligatorias antes de PASS (PROTOCOL-ASG-001 §5.5):**

1. Review gate verde (`GET /api/tasks/<id>/review-gate` → `canProceedToReview: true`)
2. Criterios met (DoD 12/12 + integración 2/2 + acceptance según brief)
3. Manifest v1.0 commiteado al PR (`<TASK_ID>.json` + `.manifest.md` + `_REPORT.md` en `knowledge/task-manifests/<phase>/<sprint>/`)
4. Devlog en estado terminal (`PROTOCOL-DEV-001` §FASE 3 — todos los entries en resolved/wont_fix/deferred)
5. Reporte en path canónico v1.1 (`knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>_REPORT.md`, NO en `agent-tasks/reports/`)

---

## PASO 5 — Asignar tarea a un agente ejecutor

Cuando preparás un ASSIGNMENT para un agente ejecutor, **vos asignás el worktree** que usa (vos NO ocupás ninguno):

```
Worktrees disponibles para Executors:
- vtt-espacio-1 (agente)
- vtt-espacio-2 (agente)
- vtt-espacio-3 (agente)
- vtt-espacio-4 (agente)
- vtt-espacio-5 (agente)
```

Reglas:
- 1 agente = 1 worktree por tarea
- NO asignar 2 agentes al mismo worktree simultáneamente
- Verificá disponibilidad: `git -C virtual-teams-tracking worktree list` + confirmar que el worktree elegido está idle
- **El TL Reviewer NO ocupa worktree** (`VTT.PROTOCOL-WT-001 v1.1` §2). Los 5 worktrees son 100% para Executors.

Documentá en el ASSIGNMENT (sección "Worktree asignado") y en el mensaje al agente.

---

## NUNCA HAGAS ESTO

- ❌ NUNCA aprobar terminalmente (`task_approved`) — es del PM
- ❌ NUNCA mergear PRs — es del PM
- ❌ NUNCA implementar código de prod en modo Reviewer — usá modo Executor
- ❌ NUNCA asignar 2 agentes al mismo worktree en simultáneo
- ❌ NUNCA escribir ASSIGNMENT desde memoria — verificar contra código real
- ❌ NUNCA aprobar sin review gate verde + criterios met
- ❌ NUNCA firmar stage con findings critical/high abiertos
- ❌ NUNCA spawnar sub-agente TL — actuá directo

---

## R-AGENTE-WT-01 — Cleanup al cambiar de worktree

Si rotás entre worktrees durante la sesión (revisar PR del agente en vtt-espacio-2, después volver a vtt-espacio-1):

1. Antes de dejar un worktree, `git status` debe estar limpio (excepto dinámicos)
2. NO commitear cambios en branches de otros agentes
3. Volver siempre a `vtt-espacio-1` para coordinación

---

## RESUMEN

1. **PASO 0** — cd a vtt-espacio-1
2. **PASO 1** — Leer normativa + operativa
3. **PASO 2** — Datos clave
4. **PASO 3** — JWT + diagnóstico sprint
5. **PASO 4** — Diagnóstico worktree (6 estados)
6. **PASO 5** — Al asignar tareas, elegir worktree libre para cada agente

**Fuente de verdad:** `OPERATIVO_TL_REVIEWER.md`
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
