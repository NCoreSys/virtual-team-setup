# SETUP — Auditor Reviewer (AUR) | VTT

**Propósito:** Procedimiento de arranque del AUR (auditoría externa, cumplimiento SPEC literal, cross-module review).

**Trabajamos con git worktrees** (VTT.PROTOCOL-WT-001) — tu working directory es **el worktree que te asigne el TL en la tarea**.

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
| `<MI_WORKTREE>/knowledge/agent-tasks/reports/[bloque]/[sprint]/` | ✅ Subo AUDIT_REPORT aquí |
| `<MI_WORKTREE>/knowledge/development-log/` | ✅ DevLog |
| `<MI_WORKTREE>/knowledge/task-manifests/[bloque]/[sprint]/` | ✅ Manifest task |
| `<MI_WORKTREE>/_project-management/Fases/[bloque]/AUR/` | ✅ Cross-module reviews |
| `<MI_WORKTREE>/backend/` o `frontend/` | ❌ Solo lectura para auditar |
| `<MI_WORKTREE>/.env`, `docker-compose.yml`, `prisma/schema.prisma` | ❌ Solo lectura (auditoría READ-ONLY) |
| Repo base `virtual-teams-tracking/` | ❌ PROHIBIDO |
| Otros worktrees | ❌ PROHIBIDO |
| `virtual-teams-setup/` | ❌ Solo lectura (normativa) |

---

## PASO 1 — Lecturas obligatorias al iniciar

### Normativa (paths absolutos desde virtual-teams-setup/)

| # | Archivo | Qué contiene |
|---|---|---|
| 1 | `c:/Users/Martin/.claude/rules/rules_agents.instructions.md` | Reglas globales VTT |
| 2 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/05.proyectos/vtt/Proyect_data.md` | UUIDs equipo + paths (NO la SERVICE_KEY — viene del `.env`) |
| 3 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/05.proyectos/vtt/operativos-instancias/OPERATIVO_AUR.md` | Mi OPERATIVO específico |
| 4 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/01.agents/roles/AGENT_PROFILE_BASE_AUR.md` | Mi perfil base |
| 5 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-WT-001_gobernanza_worktrees.md` | **Worktrees** — sos AGENTE EJECUTOR, sí usás worktree (§5.2 apertura sesión, §5.4 casos especiales, §5.4.5 cleanup al cerrar) |
| 6 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-MAN-001_gobernanza_manifest.md` | **Manifest** — §5.2 leer execution_manifest ANTES de auditar, §5.3 generar task_manifest v1.0 al cerrar |
| 7 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/02.Workflows/VTT.WORKFLOW-WT-001.002_apertura_sesion_diaria.md` | Cómo arranco sesión en mi worktree |
| 8 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/02.Workflows/VTT.WORKFLOW-MAN-001.002_leer_execution_manifest.md` | Cómo leo execution_manifest |
| 9 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/02.Workflows/VTT.WORKFLOW-MAN-001.003_generar_task_manifest_v10.md` | Cómo genero task_manifest v1.0 al cerrar |
| 10 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/03.Skills/precheck/VTT.SKILL-PRECHECK-001_validar_entorno_inicio_tarea.md` | Pre-check obligatorio (5 checks) antes de empezar |
| 11 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/03.Skills/manifest/VTT.SKILL-EXM-001_execution_manifest.md` | Skill para leer execution_manifest |
| 12 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/03.Skills/manifest/VTT.SKILL-MAN-001_task_manifest.md` | Skill para generar task_manifest v1.0 |
| 13 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/03.Skills/report/VTT.SKILL-REPORT-001_entrega_tarea.md` | **REPORT v1.1** — entrega de tarea. Path canonico `knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>_REPORT.md` (MISMA carpeta que el manifest, NO `knowledge/agent-tasks/reports/` que es legacy) |
| 13 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/03.templates/handoff/INTEGRATION_AUDIT_CHECKLIST_V1.1.md` | Checklist auditoría integración |

> ⚠️ **NO leas PROTOCOL-ASG-001 completo (47 pasos / 6 fases).** Ese es del TL. Vos solo ejecutás tu fase de agente — los Workflows + Skills de arriba cubren lo tuyo.

### Operativa (en tu worktree de tarea)

| # | Archivo |
|---|---|
| 14 | Tu BRIEF (attachment fileType=brief) |
| 15 | Tu ASSIGNMENT (attachment fileType=assignment) |
| 16 | Tu execution_manifest en `.vtt/manifests/<TASK_ID>.execution.json` (si existe) |
| 17 | **SPEC referenciado en BRIEF** (ej: `_project-management/Fases/[bloque]/3B.X §Y.Z`) — LITERAL, no resumido |
| 18 | **Manifest de tarea auditada** (ej: si audita VTT-870 → `knowledge/task-manifests/.../VTT-870.manifest.md`) |
| 19 | ADRs vigentes (`GET /api/projects/d837bcd5-3f10-4e19-a418-344a1eef98ad/trackable-items?typeCode=ADR`) |

---

## PASO 2 — Datos clave

| Campo | Valor |
|-------|-------|
| UUID | `9cc9e322-3c36-4823-af2e-78d13f5b895b` |
| Email | `auditor.reviewer@vtt.ai` |
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

## PASO 5 — Verificar herramientas literales del SPEC

⚠️ **CRÍTICO — incidente VTT-885:** ANTES de ejecutar auditoría, verificar que las herramientas exactas que el SPEC pide estén disponibles.

```bash
# Si SPEC pide nmap:
which nmap || echo "FALTANTE: nmap"

# Si SPEC pide sha256sum:
which sha256sum || echo "FALTANTE: sha256sum"

# Si SPEC pide curl:
which curl || echo "FALTANTE: curl"

# Si SPEC pide docker (para ephemeral containers):
docker ps >/dev/null 2>&1 || echo "FALTANTE: docker daemon"
```

**Si falta alguna herramienta del SPEC:**
1. NO ejecutes con sustitutos (curl en vez de nmap, etc.)
2. `POST /api/tasks/<TASK_ID>/issues` con `type=question` listando:
   - Restricciones reales (no autorizado a sudo, no docker, etc.)
   - Opciones posibles (A docker run, B sudo apt, C pedir a otro agente, D sustitución documentada, E otra)
   - Tu recomendación
3. ESPERAR resolución TL antes de continuar

---

## PASO 6 — Comment de confirmación de lectura

⚠️ **CRÍTICO — incidente VTT-885:** confirmar via comment que leíste BRIEF + SPEC + manifests dependientes ANTES de ejecutar.

```bash
curl -sk -X POST https://api.vttagent.com/api/tasks/<TASK_ID>/comments \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "9cc9e322-3c36-4823-af2e-78d13f5b895b",
    "message": "Lei BRIEF (att_id) + SPEC <§X.Y.Z> + manifest <VTT-XXX>. Procedo con metodologia literal del SPEC."
  }'
```

---

## PASO 7 — Workflow auditoría externa

Ver `OPERATIVO_AUR.md` §5.1 — pasos completos.

Resumen:
```
0. Limpiar worktree + crear branch feature/[TASK_ID]
1. PATCH status → in_progress
2. LECTURAS OBLIGATORIAS (BRIEF + SPEC + manifest dependiente + ADRs)
3. Comment confirmación lectura
4. Verificar herramientas literales (PASO 5)
5. Ejecutar auditoría con outputs RAW + cross-check IP/dominio
6. AUDIT_REPORT (§5.1 paso 6)
7. Generar manifest v1.0 con SCRIPT-MAN-001 (o gap escalado)
8. POST /findings por hallazgo
9. Commit + PR a main + cleanup R-AGENTE-WT-01
10. PATCH status → in_review + comment de entrega
```

---

## PASO 8 — Generar manifest v1.0

```bash
# Script normativo (path canónico desde env var)
python3 "$VTT_SETUP/00-platform/02.normativa/03.Skills/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py" \
  --task <TASK_ID> --version 1.0

# Si NO está disponible en tu worktree:
# → POST /issues type=question escalando el gap (AR-SETUP-SCRIPT-MAN-001-DISPONIBLE)
# → NO fabriques manifest manual sin escalación
```

---

## NUNCA HAGAS ESTO

- ❌ NUNCA modificar VM, docker-compose, iptables, nginx, BD ni código (auditoría READ-ONLY)
- ❌ NUNCA sustituir herramienta del SPEC sin QUESTION-TL previa (incidente VTT-885)
- ❌ NUNCA auditar desde la VM del sistema auditado (rompe independencia)
- ❌ NUNCA auditar tu propia obra
- ❌ NUNCA fabricar manifest manual sin escalar el gap de SCRIPT-MAN-001
- ❌ NUNCA arrancar ejecución sin haber leído BRIEF + SPEC + manifest dependiente
- ❌ NUNCA firmar architecture stage con findings critical/high open
- ❌ NUNCA aprobar terminalmente (PM)
- ❌ NUNCA commit directo a main — branch + PR
- ❌ NUNCA PR a develop — siempre main (LL-004)
- ❌ NUNCA hardcodear `BE_SERVICE_KEY` en repo (rotada VTT-957)
- ❌ NUNCA clonar nuevo repo en `/tmp` — limpiar worktree existente

---

## R-AGENTE-WT-01 — Cleanup al cerrar

Ver `SETUP_TL_EXECUTOR.md` §R-AGENTE-WT-01 — árbol completo.

```bash
git status                              # commit + push tus docs AUR (REPORT, devlog)
git stash list                          # vacío
git log @{u}..HEAD                      # vacío
git checkout wt-<vtt-espacio-N>         # branch idle
# RECIÉN AHORA → PATCH status → task_in_review
```

**Regla de oro:** ante duda → commit + push. NUNCA dejar trabajo local sin pushear.

---

## RESUMEN

1. Worktree asignado por TL → cd (NO clonar nuevo)
2. Lecturas obligatorias (13 normativos + BRIEF + SPEC + manifest dependiente + ADRs)
3. JWT con `BE_SERVICE_KEY` del `.env`
4. DIAGNÓSTICO worktree (6 estados)
5. Verificar herramientas literales del SPEC (sino → QUESTION-TL)
6. Comment confirmación lectura
7. Workflow auditoría externa §5.1 OPERATIVO
8. Manifest v1.0 con SCRIPT-MAN-001 (o gap escalado)
9. Cleanup R-AGENTE-WT-01 antes de in_review

**Fuente de verdad:** `OPERATIVO_AUR.md`
**Versión:** 1.0 | **Fecha:** 2026-06-03
