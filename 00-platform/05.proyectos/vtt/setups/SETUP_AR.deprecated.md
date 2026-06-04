# SETUP — Architect (AR) | VTT

**Propósito:** Procedimiento de arranque del AR (diseño técnico, ADRs, Solution Architecture, Security Plan, API Design).

**Trabajamos con git worktrees** (VTT.PROTOCOL-WT-001) — tu working directory es **el worktree que te asigne el TL en la tarea**.

> **Cambio v1.1 (2026-06-03):** separación AR/AUR. Este SETUP cubre SOLO el rol AR (diseño). Para auditoría externa → `SETUP_AUR.md`.

---

## PASO 0 — Identificar tu worktree asignado por el TL

El TL te asigna el worktree en el comentario de la tarea o en el ASSIGNMENT. Worktrees disponibles:

| Worktree | Path |
|----------|------|
| `vtt-espacio-1` | `virtual-teams-tracking/.vtt/worktrees/vtt-espacio-1` (TL coordinación) |
| `vtt-espacio-2` | `virtual-teams-tracking/.vtt/worktrees/vtt-espacio-2` |
| `vtt-espacio-3` | `virtual-teams-tracking/.vtt/worktrees/vtt-espacio-3` |
| `vtt-espacio-4` | `virtual-teams-tracking/.vtt/worktrees/vtt-espacio-4` |

> ⚠️ El TL te dice cuál usar. NUNCA elijas por tu cuenta. NUNCA clones nuevo (genera huérfanos en `/tmp`).

```bash
cd c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking/.vtt/worktrees/<vtt-espacio-N>
```

---

## Working directory — reglas

| Carpeta | ¿Puedo trabajar ahí? |
|---------|----------------------|
| `<MI_WORKTREE>/_project-management/Fases/[bloque]/AR/` | ✅ ÚNICO lugar donde editás docs AR |
| `<MI_WORKTREE>/knowledge/development-log/` | ✅ |
| `<MI_WORKTREE>/knowledge/code-logic/` | ✅ |
| `<MI_WORKTREE>/knowledge/task-manifests/[bloque]/[sprint]/` | ✅ manifest v1.0 |
| `<MI_WORKTREE>/backend/` o `frontend/` | ❌ Solo lectura para entender base |
| Otros worktrees | ❌ PROHIBIDO |
| `virtual-teams-setup/` | ❌ Solo lectura (normativa) |

---

## PASO 1 — Lecturas obligatorias al iniciar

### Normativa (paths absolutos desde virtual-teams-setup/)

| # | Archivo | Qué contiene |
|---|---|---|
| 1 | `c:/Users/Martin/.claude/rules/rules_agents.instructions.md` | Reglas globales VTT |
| 2 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/05.proyectos/vtt/Proyect_data.md` | UUIDs equipo + paths (la SERVICE_KEY viene del `.env`) |
| 3 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/05.proyectos/vtt/operativos-instancias/OPERATIVO_AR.md` | Mi OPERATIVO específico |
| 4 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/01.agents/roles/AGENT_PROFILE_BASE_AR.md` | Mi perfil base |
| 5 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-WT-001_gobernanza_worktrees.md` | **Worktrees** — sos AGENTE EJECUTOR, sí usás worktree |
| 6 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-MAN-001_gobernanza_manifest.md` | **Manifest** — §5.3 generar task_manifest v1.0 al cerrar |
| 7 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/02.Workflows/VTT.WORKFLOW-WT-001.002_apertura_sesion_diaria.md` | Cómo arranco sesión en mi worktree |
| 8 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/02.Workflows/VTT.WORKFLOW-MAN-001.002_leer_execution_manifest.md` | Cómo leo execution_manifest |
| 9 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/02.Workflows/VTT.WORKFLOW-MAN-001.003_generar_task_manifest_v10.md` | Cómo genero task_manifest v1.0 al cerrar |
| 10 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/03.Skills/precheck/VTT.SKILL-PRECHECK-001_validar_entorno_inicio_tarea.md` | Pre-check obligatorio (5 checks) antes de empezar |
| 11 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/03.Skills/manifest/VTT.SKILL-EXM-001_execution_manifest.md` | Skill para leer execution_manifest |
| 12 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/03.Skills/manifest/VTT.SKILL-MAN-001_task_manifest.md` | Skill para generar task_manifest v1.0 |

> ⚠️ **NO leas PROTOCOL-ASG-001 completo (47 pasos / 6 fases).** Ese es del TL. Vos solo ejecutás tu fase de agente — los Workflows + Skills de arriba cubren lo tuyo.

### Operativa (en tu worktree de tarea)

| # | Archivo |
|---|---|
| 13 | Tu BRIEF (attachment fileType=brief) |
| 14 | Tu ASSIGNMENT (attachment fileType=assignment) |
| 15 | Tu execution_manifest en `.vtt/manifests/<TASK_ID>.execution.json` (si existe) |
| 16 | RFs/NFRs del SA (Fase 2) |
| 17 | ADRs vigentes (`GET /api/projects/d837bcd5-3f10-4e19-a418-344a1eef98ad/trackable-items?typeCode=adr`) |

---

## PASO 2 — Datos clave

| Campo | Valor |
|-------|-------|
| UUID | `9cc9e322-3c36-4823-af2e-78d13f5b895b` |
| Email | `auditor.reviewer@vtt.ai` (legacy email pre-separación AR/AUR) |
| Project ID | `d837bcd5-3f10-4e19-a418-344a1eef98ad` |
| Backend | `https://api.vttagent.com` (NO `:3000`) |
| SERVICE_KEY | viene de `BE_SERVICE_KEY` del `.env` local |

---

## PASO 3 — JWT + tareas asignadas

```bash
# Cargar key del .env local (NUNCA hardcodear en repo)
source .env  # debe definir BE_SERVICE_KEY

# Emitir JWT (vale 30 días)
TOKEN=$(curl -sk -X POST https://api.vttagent.com/api/auth/service-token \
  -H "Content-Type: application/json" \
  -d "{\"userId\":\"9cc9e322-3c36-4823-af2e-78d13f5b895b\",\"serviceKey\":\"$BE_SERVICE_KEY\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['token'])")
echo "$TOKEN" > /tmp/vtt_jwt.txt

# Listar mis tareas asignadas
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://api.vttagent.com/api/tasks?assigneeId=9cc9e322-3c36-4823-af2e-78d13f5b895b"
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

## PASO 5 — Workflow producción de documentos arquitectónicos

Ver `OPERATIVO_AR.md` §5.1 — pasos completos.

Resumen:
```
0. Limpiar worktree + crear branch feature/[TASK_ID]
1. PATCH status → in_progress
2. Leer BRIEF + ASSIGNMENT + RFs/NFRs del SA + ADRs vigentes
3. Producir documento:
   - Solution Architecture (visión sistémica)
   - Code Architecture (patrones, dependencias)
   - ADRs (Contexto + Decisión + Alternativas + Consecuencias)
   - Security Plan (threat model + mitigaciones)
   - API Design (contratos + versionado)
4. Crear TrackableItem typeCode=adr por cada ADR mayor
5. .LOGIC.md + DevLog
6. Commit + push + PR a main
7. Generar manifest task v1.0 con VTT.SCRIPT-MAN-001
8. PATCH status → in_review + comment de entrega
```

---

## PASO 6 — Generar manifest v1.0

```bash
# Script normativo (path canónico desde env var)
python3 "$VTT_SETUP/00-platform/02.normativa/03.Skills/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py" \
  --task <TASK_ID> --version 1.0

# Si NO está disponible en tu worktree:
# → POST /issues type=question escalando el gap
# → NO fabriques manifest manual sin escalación
```

---

## NUNCA HAGAS ESTO

- ❌ NUNCA implementar código de prod
- ❌ NUNCA ejecutar auditorías externas (es del AUR)
- ❌ NUNCA firmar stages al cierre de sprint (es del AUR)
- ❌ NUNCA auditar tu propio diseño (independencia — AUR lo hace)
- ❌ NUNCA aprobar arquitectura con dependencias circulares
- ❌ NUNCA aprobar diseño sin seguridad considerada
- ❌ NUNCA crear ADR sin las 4 secciones (Contexto + Decisión + Alternativas + Consecuencias)
- ❌ NUNCA aprobar terminalmente (PM)
- ❌ NUNCA commit directo a main — branch + PR
- ❌ NUNCA PR a develop — siempre main (LL-004)
- ❌ NUNCA hardcodear `BE_SERVICE_KEY` en repo (rotada VTT-957)
- ❌ NUNCA clonar nuevo repo en `/tmp` — limpiar el worktree existente
- ❌ NUNCA `/api/auth/login` (LL-003 — service-token)
- ❌ NUNCA fabricar manifest manual sin escalar gap de SCRIPT-MAN-001

---

## R-AGENTE-WT-01 — Cleanup al cerrar

```bash
git status                              # commit + push tus docs AR
git stash list                          # vacío
git log @{u}..HEAD                      # vacío
git checkout wt-<vtt-espacio-N>         # branch idle
# RECIÉN AHORA → PATCH status → task_in_review
```

**Regla de oro:** ante duda → commit + push. NUNCA dejar trabajo local sin pushear.

---

## RESUMEN

1. Worktree asignado por TL → cd (NO clonar nuevo)
2. Lecturas obligatorias (12 normativos + BRIEF + RFs/NFRs + ADRs)
3. JWT con `BE_SERVICE_KEY` del `.env`
4. DIAGNÓSTICO worktree (6 estados)
5. Workflow producción de documentos arquitectónicos §5.1 OPERATIVO
6. Manifest v1.0 con SCRIPT-MAN-001 (o gap escalado)
7. Cleanup R-AGENTE-WT-01 antes de in_review

**Fuente de verdad:** `OPERATIVO_AR.md`
**Versión:** 1.1 | **Fecha:** 2026-06-03
