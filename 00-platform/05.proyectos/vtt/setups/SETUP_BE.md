# SETUP — Backend Engineer (BE) | VTT

**Propósito:** Procedimiento de arranque del BE (cubre BE #1 y BE #2).

**Trabajamos con git worktrees** (VTT.PROTOCOL-WT-001) — tu working directory es **el worktree que te asigne el TL en la tarea**.

---

## PASO 0 — Identificar tu worktree asignado

El TL te asigna el worktree en el comentario de la tarea o en el ASSIGNMENT. Worktrees disponibles:

| Worktree | Path |
|----------|------|
| `vtt-espacio-1` | `virtual-teams-tracking/.vtt/worktrees/vtt-espacio-1` (TL coordinación) |
| `vtt-espacio-2` | `virtual-teams-tracking/.vtt/worktrees/vtt-espacio-2` |
| `vtt-espacio-3` | `virtual-teams-tracking/.vtt/worktrees/vtt-espacio-3` |
| `vtt-espacio-4` | `virtual-teams-tracking/.vtt/worktrees/vtt-espacio-4` |

> ⚠️ El TL te dice cuál usar. NUNCA elijas por tu cuenta.

```bash
cd c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking/.vtt/worktrees/<vtt-espacio-N>
```

---

## Working directory — reglas

| Carpeta | ¿Puedo trabajar ahí? |
|---------|----------------------|
| `<MI_WORKTREE>` | ✅ PRIMARIO |
| Repo base `virtual-teams-tracking/` | ❌ PROHIBIDO |
| Otros worktrees | ❌ PROHIBIDO |
| `virtual-teams-setup/` | ❌ Solo lectura (normativa) |

---

## PASO 1 — Lee al iniciar

### Normativa (paths absolutos desde virtual-teams-setup/)

| # | Archivo | Qué contiene |
|---|---|---|
| 1 | `c:/Users/Martin/.claude/rules/rules_agents.instructions.md` | Reglas globales VTT |
| 2 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/05.proyectos/vtt/Proyect_data.md` | UUIDs equipo + SERVICE_KEY + paths |
| 3 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/05.proyectos/vtt/operativos-instancias/OPERATIVO_BE.md` | Tu OPERATIVO específico |
| 4 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-WT-001_gobernanza_worktrees.md` | **Worktrees** — sos AGENTE EJECUTOR, sí usás worktree (la parte que te corresponde: §5.2 apertura sesión, §5.4 casos especiales, §5.4.5 cleanup al cerrar) |
| 5 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-MAN-001_gobernanza_manifest.md` | **Manifest** — la parte que te corresponde: §5.2 leer execution_manifest ANTES de tocar código, §5.3 generar task_manifest v1.0 al cerrar |
| 6 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/02.Workflows/VTT.WORKFLOW-WT-001.002_apertura_sesion_diaria.md` | Cómo arrancás sesión en tu worktree |
| 7 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/02.Workflows/VTT.WORKFLOW-MAN-001.002_leer_execution_manifest.md` | Cómo leés tu execution_manifest |
| 8 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/02.Workflows/VTT.WORKFLOW-MAN-001.003_generar_task_manifest_v10.md` | Cómo generás task_manifest v1.0 al cerrar |
| 9 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/03.Skills/precheck/VTT.SKILL-PRECHECK-001_validar_entorno_inicio_tarea.md` | Pre-check obligatorio (5 checks) antes de empezar |
| 10 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/03.Skills/manifest/VTT.SKILL-EXM-001_execution_manifest.md` | Skill para leer execution_manifest |
| 11 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/03.Skills/manifest/VTT.SKILL-MAN-001_task_manifest.md` | Skill para generar task_manifest v1.0 |
| 12 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/03.Skills/report/VTT.SKILL-REPORT-001_entrega_tarea.md` | **REPORT v1.1** — entrega de tarea. Path canónico `knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>_REPORT.md` (MISMA carpeta que el manifest, NO `knowledge/agent-tasks/reports/` que es legacy) |

> ⚠️ **NO leas el PROTOCOL-ASG-001 completo (47 pasos / 6 fases).** Ese es del TL. Vos solo ejecutás tu fase de agente — los Workflows + Skills de arriba cubren lo tuyo.

### Operativa (en tu worktree de tarea)

| # | Archivo |
|---|---|
| 12 | Tu BRIEF (attachment) |
| 13 | Tu ASSIGNMENT (attachment) |
| 14 | Tu execution_manifest en `.vtt/manifests/<TASK_ID>.execution.json` |
| 15 | `backend/prisma/schema.prisma` (read-only — base del schema) |
| 16 | `backend/src/routes/` (endpoints existentes) |
| 17 | `backend/src/services/` (services existentes para reutilizar patrones) |

---

## PASO 2 — Datos clave

| Campo | Valor |
|-------|-------|
| UUID #1 | `8834830b-578f-46be-933b-0abcbbc5da99` |
| UUID #2 | `008cacfc-d0cb-41d2-8628-def9571f8c77` |
| Project ID | `d837bcd5-3f10-4e19-a418-344a1eef98ad` |
| API URL | `https://api.vttagent.com`  (NO `:3000` — VTT-870 cerró el puerto) |
| SERVICE_KEY | viene de `BE_SERVICE_KEY` del `.env` local (NUNCA hardcodear en repo — rotada VTT-957) |
| Swagger | `https://api.vttagent.com/api-docs` |

---

## PASO 3 — JWT + tareas asignadas

```bash
# Cargar BE_SERVICE_KEY del .env local (NUNCA hardcodear)
source .env  # debe definir BE_SERVICE_KEY

TOKEN=$(curl -sk -X POST https://api.vttagent.com/api/auth/service-token \
  -H "Content-Type: application/json" \
  -d "{\"userId\":\"<TU_UUID>\",\"serviceKey\":\"$BE_SERVICE_KEY\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['token'])")

curl -H "Authorization: Bearer $TOKEN" "https://api.vttagent.com/api/tasks?assigneeId=<TU_UUID>"
```

---

## PASO 4 — DIAGNÓSTICO obligatorio del worktree

```bash
git branch --show-current
git status
git stash list
git fetch origin
git log --oneline @{u}..HEAD 2>/dev/null
```

**6 estados** (A/B/C/D/E/F) — ver `SETUP_TL_EXECUTOR.md` §PASO 4.2.

- ✅ A/B → continuar (sync con main + crear branch)
- ✅ C → tu tarea en curso
- ⚠️ D → archivos extraños (excepto dinámicos del sistema) → STOP + reportar
- 🛑 E → branch de otra tarea → STOP + reportar al TL
- 🛑 F → stash sin label → STOP + reportar

### Archivos dinámicos del sistema (es normal verlos modificados):
- `knowledge/agent-tasks/agents-status.json`
- `knowledge/agent-tasks/notifications.txt`
- `.claude/settings.json`

---

## PASO 5 — Workflow de 12 pasos

Ver `OPERATIVO_BE.md` §7 — pasos 0-12 con curls y comandos.

Resumen:
```
0. git checkout main && git pull && git checkout -b feature/[TASK_ID]
1. PATCH status → in_progress
2-3. Leer brief + ASSIGNMENT + archivos de referencia
4. Verificar entorno (npm run dev OK, BD accesible)
5. Implementar siguiendo patrón Router → Service → Prisma
6. Crear .LOGIC.md por cada archivo
7. Probar localmente (curl real con 200)
8. Testing manual (edge cases, errors)
9. Development Log
10. Commit + push
11. PR a main con gh CLI
12. Subir attachments (devlog, code_logic) + comentario + PATCH status → in_review
```

---

## NUNCA HAGAS ESTO

- ❌ NUNCA modificar `backend/prisma/schema.prisma` (es del DB)
- ❌ NUNCA modificar `docker-compose.yml` / `.env` / `nginx.conf` (es del DO)
- ❌ NUNCA modificar `frontend/` (es del FE)
- ❌ NUNCA inventar campos del schema — verificar contra schema.prisma
- ❌ NUNCA inventar endpoints — verificar contra routes/
- ❌ NUNCA mockear datos — crear issue si faltan
- ❌ NUNCA commit directo a main
- ❌ NUNCA PR a develop — siempre main
- ❌ NUNCA dejar console.log de debug
- ❌ NUNCA endpoint sin try-catch ni Swagger JSDoc inline
- ❌ NUNCA usar PATCH /status para on_hold — usar PUT /on-hold (ERR-006)
- ❌ Comentarios con `!` en bash → ERR-002 → usar Python urllib

---

## R-AGENTE-WT-01 — Cleanup al cerrar

Ver `SETUP_TL_EXECUTOR.md` §R-AGENTE-WT-01 — árbol completo.

**Regla de oro:** ante duda → commit + push. NUNCA dejar trabajo local sin pushear.

Pasos resumidos:
1. `git status` → decidir por tipo de archivo (commit+push default / ignorar dinámicos / discard tests / stash+reportar excepción)
2. `git stash list` → debe estar vacío (excepción documentada en devlog observation)
3. `git log @{u}..HEAD` → debe estar vacío (todo pusheado)
4. `git checkout wt-<vtt-espacio-N>` (branch idle)
5. RECIÉN AHORA → PATCH status → task_in_review

---

## RESUMEN

1. Worktree asignado por el TL → cd ahí
2. Lee normativa + ASSIGNMENT + brief
3. JWT + listar tareas
4. DIAGNÓSTICO worktree (6 estados)
5. Workflow 12 pasos
6. Cleanup R-AGENTE-WT-01 antes de in_review

**Fuente de verdad:** `OPERATIVO_BE.md`
**Versión:** 1.1 | **Fecha:** 2026-06-03

> **Cambio v1.1 (2026-06-03):** URL `:3000` → `https://api.vttagent.com` (VTT-870). SERVICE_KEY hardcoded → `BE_SERVICE_KEY` del `.env` (rotada VTT-957). Agregado item 12 SKILL-REPORT-001 con path canónico `knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>_REPORT.md` (legacy `knowledge/agent-tasks/reports/` deprecado).
