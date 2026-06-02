# SETUP — Technical Writer of Operational Processes (TW-OPS) | virtual-teams-setup

**Propósito:** Procedimiento de arranque del TW-OPS. Crea/edita/audita normativa operativa (Protocols/Workflows/Skills/Scripts/Cards) del repo canónico VTT.

**El TW-OPS opera desde un worktree dedicado** (`PROTOCOL-WT-001 §5.1`) para aislar su trabajo del Coord y del RA.

---

## PASO 0 — Posicionarte y validar entorno

```bash
cd c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/.vtt/worktrees/vtt-setup-tw-ops
git status   # branch agent/tw-ops/... o wt-vtt-setup-tw-ops (idle)
git branch --show-current

# Variable obligatoria al arrancar
export VTT_SETUP="c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform"
test -d "$VTT_SETUP/02.normativa" || { echo "ABORT: \$VTT_SETUP inválido"; exit 2; }
```

### Validación de entorno

```bash
test -d $VTT_SETUP/02.normativa && echo "02.normativa OK" || echo "ERROR: 02.normativa no encontrado"
test -d $VTT_SETUP/02.normativa/01.Protocols && echo "Protocols OK"
test -d $VTT_SETUP/02.normativa/02.Workflows && echo "Workflows OK"
test -d $VTT_SETUP/02.normativa/03.Skills && echo "Skills OK"
test -d $VTT_SETUP/02.normativa/04.Scripts && echo "Scripts OK"
test -d $VTT_SETUP/02.normativa/05.Cards && echo "Cards OK"
test -f $VTT_SETUP/02.normativa/GUIA_AUTOR.md && echo "GUIA_AUTOR OK"
test -f $VTT_SETUP/02.normativa/INVENTARIO.md && echo "INVENTARIO OK"
```

---

## Working directory — reglas

| Carpeta | ¿Puedo trabajar ahí? |
|---|---|
| `.vtt/worktrees/vtt-setup-tw-ops/00-platform/02.normativa/` | ✅ **PRIMARIO** — TODA tu edición va acá |
| `.vtt/worktrees/vtt-setup-tw-ops/00-platform/02.normativa/_autoria/` | ✅ **PRIMARIO (lectura)** — templates de autoría |
| `.vtt/worktrees/vtt-setup-tw-ops/knowledge/agent-tasks/audits/` | ✅ **PRIMARIO (escritura)** — reportes de auditoría FASE B |
| `.vtt/worktrees/vtt-setup-tw-ops/knowledge/agent-tasks/messages/` | ✅ **PRIMARIO (lectura)** — MSG_VTS-XXX assignments |
| Tarea VTT (`POST /attachments`) | ✅ **PRIMARIO** — subir reportes audit como `code_logic` Y `devlog` (Review Gate L10) |
| Repo padre `virtual-teams-setup/` (clone base) | ❌ **PROHIBIDO** — trabajás en el worktree, NO en el clone |
| `00-platform/03.templates/research/` | ❌ **PROHIBIDO** — eso es del RA |
| `00-platform/05.proyectos/*/operativos-instancias/` | ❌ **PROHIBIDO** — eso lo crea el Coord (datos de identidad de cada agente) |

---

## PASO 1 — Lee estos archivos al iniciar (paths absolutos)

| # | Archivo | Qué contiene |
|---|---|---|
| 1 | `c:/Users/Martin/.claude/rules/rules_agents.instructions.md` | Reglas globales VTT |
| 2 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/05.proyectos/vtt-setup/operativos-instancias/OPERATIVO_TW-OPS_VTT-SETUP.md` | **Tu OPERATIVO específico (UUID, password, comandos VTT API, 15 gotchas)** |
| 3 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/01.agents/roles/AGENT_PROFILE_BASE_TW-OPS.md` | Tu perfil base (identidad, propósito, responsabilidades, inputs/outputs) |
| 4 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/README.md` | **Mapa del repo vtt-setup** (5 entidades + política de paths) |
| 5 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/INDEX.md` | **Catálogo navegable** — para detectar duplicados/drift |
| 6 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/GUIA_AUTOR.md` | **Tu biblia editorial** — checklist por nivel, naming, anti-patterns |
| 7 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/INVENTARIO.md` | Lista canónica de Protocols/Workflows/Skills/Scripts vigentes |
| 8 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/00_REGISTRO_ACRONIMOS.md` | Acrónimos `<CAT>` aprobados para naming |
| 9 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-GOV-002_gobierno_edicion_vtt_setup_fase_desarrollo.md` | **Gobierno editorial** — branch `agent/tw-ops/...` + commit estructurado + hook |
| 10 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-WT-001_gobernanza_worktrees.md` v1.1 | Cómo operar en tu worktree dedicado |

---

## PASO 1.bis — Normativa canónica que cargas como contexto operativo

### Protocols

| Código | Cuándo |
|---|---|
| `VTT.PROTOCOL-GOV-001` Guía Normativa | Marco conceptual 5 niveles (Protocol/Workflow/Skill/Script/Card) — base de TODO |
| `VTT.PROTOCOL-GOV-002` Gobierno editorial vtt-setup | **Tu Protocol operativo principal** — branch + commit + hook |
| `VTT.PROTOCOL-ASG-001` Ciclo asignación + cierre | Vos como ejecutor (§5.3 = ejecución, §5.4 = bug/blocker, §5.4.bis = question) |
| `VTT.PROTOCOL-DEV-001` v1.1.0 Lifecycle devlog | Si tu tarea genera devlog entries (decisiones técnicas) |
| `VTT.PROTOCOL-MAN-001` Gobernanza manifest | Si tu tarea genera Task Manifest v1.0 al cerrar |
| `VTT.PROTOCOL-WT-001` v1.1 Worktrees | Tu working dir es worktree (§5.1) — Coord NO usa worktree (§2) |

### Workflows

| Código | Cuándo |
|---|---|
| `VTT.WORKFLOW-ASG-001.031..038` Sub-workflows ejecutor | Cada paso del ciclo de tarea (leer inputs, ejecutar, entregar) |
| `VTT.WORKFLOW-DEV-001.001/.002/.003` Devlog entries | Crear/editar/cerrar entries devlog |

### Skills

| Código | Cuándo |
|---|---|
| `VTT.SKILL-AUTH-001` JWT con service-token | Al arrancar — usar `/api/auth/service-token`, NO `/api/auth/login` (rate-limited) |
| `VTT.SKILL-PRECHECK-001` Pre-check entorno | PASO 5 obligatorio (5 checks) |
| `VTT.SKILL-GIT-001` Crear branch | Branch `agent/tw-ops/vtt-setup/<desc>` |
| `VTT.SKILL-GIT-002` Commit estructurado | 4 markers + 3 trailers + Co-Authored-By |
| `VTT.SKILL-DEV-001..005` Devlog entries | Crear decisiones técnicas durante ejecución |
| `VTT.SKILL-ISS-001` v1.2 Crear issue | Si bloqueante (blocker) o question al Coord. Enum: bug/question/blocker/improvement/other (NO requirement) |
| `VTT.SKILL-REPORT-001` v1.1 SKL-REPORT-01 | Postear reporte de entrega al cerrar |
| `SKL-ATTACH-01` Subir archivo | Subir auditorías como `fileType=code_logic` Y `devlog` (Review Gate L10) |
| `SKL-STATUS-01..06` Transiciones de estado | in_progress/in_review (verificar transiciones permitidas — L11) |

### Scripts

| Código | Cuándo |
|---|---|
| `VTT.SCRIPT-GIT-001` Validate branch + commit | Hook commit-msg automático (instalado por PROTOCOL-GOV-002 §5.0) |
| `VTT.SCRIPT-MAN-001` v1.5 Task manifest | Si tu tarea genera manifest al cerrar |

### Templates de autoría (tu fuente para crear normativa nueva)

| Path | Cuándo |
|---|---|
| `02.normativa/_autoria/TEMPLATE_PROTOCOL.md` | Crear Protocol nuevo |
| `02.normativa/_autoria/TEMPLATE_WORKFLOW.md` | Crear Workflow nuevo |
| `02.normativa/_autoria/TEMPLATE_SKILL.md` | Crear Skill nueva |
| `02.normativa/_autoria/TEMPLATE_SCRIPT.md` | Crear Script nuevo |
| `02.normativa/_autoria/TEMPLATE_CARD.md` | Crear Card nueva |

### Reglas Nivel 0 que SIEMPRE aplican

| Regla | Por qué |
|---|---|
| `RULE-GIT-004` Prohibido commit a main | Siempre `agent/tw-ops/vtt-setup/<desc>` |
| `RULE-SEC-001` No postear datos sensibles en VTT | Auditorías SIN IPs prod / paths absolutos / credenciales |
| `RULE-SCRIPT-001` Scripts desde `$VTT_SETUP` | NUNCA copias locales del Script |

---

## PASO 2 — Datos clave

| Campo | Valor |
|---|---|
| **Repo Git** | `https://github.com/NCoreSys/virtual-team-setup` |
| **Working dir** | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/.vtt/worktrees/vtt-setup-tw-ops` |
| **Branch idle** | `wt-vtt-setup-tw-ops` |
| **API VTT** | `https://api.vttagent.com`   ← dominio, NO IP |
| **Project ID (vtt-setup en VTT)** | `c6b513a1-d8ae-4344-b684-96d73721bfbf` |
| **Tu UUID** | ver §1 del OPERATIVO |

---

## PASO 3 — JWT con service-token (NO login)

Comandos exactos en `OPERATIVO_TW-OPS_VTT-SETUP.md` §5. Resumen:

1. **Obtener JWT** vía `POST /api/auth/service-token` (NUNCA `/api/auth/login`). Cachear en `.vtt_jwt`.
2. **Si una operación API da 403 inesperado con "Missing capability"** — primero renovar JWT (las capabilities del JWT son snapshot del momento de emisión — L8 VTS-007). Si el token nuevo difiere del cacheado, reemplazar `.vtt_jwt`.
3. **Listar tareas asignadas** con `GET /api/tasks?assignedToId=<TU_UUID>&projectId=...` (gotcha #1: `assignedToId`, NO `assigneeId`).
4. **Leer ASSIGNMENT** de tu tarea (attachment con `fileType=assignment`).
5. **Reportar primera respuesta al Coordinator** con plan inicial antes de empezar.

---

## PASO 4 — Validar gobierno editorial activo

```bash
# A. Config gobernanza local
test -f .git/hooks/vtt_governance.json && echo "config OK" || echo "FALTA"

# B. Hook commit-msg
test -x .git/hooks/commit-msg && echo "hook OK" || echo "FALTA"

# C. Identidad git (rol tw-ops)
git config user.email | grep -q "tw-ops" || echo "AVISO: git config no es TW-OPS"
git config user.name | grep -qi "tw-ops\|technical writer" || echo "AVISO: git user.name no es TW-OPS"
```

Si falta config o hook → instalar según `VTT.PROTOCOL-GOV-002` §5.0 antes de editar.

---

## PASO 5 — Pre-check entorno (`VTT.SKILL-PRECHECK-001`)

```bash
# 5 checks obligatorios
test -n "$VTT_SETUP" && test -d "$VTT_SETUP/02.normativa" || { echo "ABORT: \$VTT_SETUP"; exit 2; }
test -d "$VTT_SETUP/_autoria" || test -d "$VTT_SETUP/02.normativa/_autoria" || { echo "ABORT: templates autoría"; exit 2; }
test -f "$VTT_SETUP/02.normativa/INVENTARIO.md" || { echo "ABORT: INVENTARIO"; exit 2; }
test -x .git/hooks/commit-msg || { echo "ABORT: hook commit-msg"; exit 2; }
# JWT se valida después de obtenerlo (PASO 3)
echo "✅ Pre-check OK"
```

---

## PASO 6 — Workflow TW-OPS (4 fases por tarea)

Detalle completo en `OPERATIVO_TW-OPS_VTT-SETUP.md` §6.

```
FASE A — Setup operativo (5-10 min)
  - Crear branch agent/tw-ops/vtt-setup/<desc> desde main
  - Verificar git identity + hook activo
  - Mover tarea a task_in_progress (precondición SKILL-STATUS-002)

FASE B — Auditoría read-only (1-3h)
  - Cross-walk FEATURE ↔ Protocol ↔ Workflows ↔ Skills ↔ Cards
  - Identificar gaps reales con evidencia (grep, file system check)
  - Identificar falsos positivos y DESCARTARLOS (no hacer "por las dudas")
  - Producir reporte AUDIT_<TASK_ID>_<DOMAIN>.md en knowledge/agent-tasks/audits/
  - Reportar plan al Coord ANTES de empezar FASE C

FASE C — Construcción (1-4h, depende del scope)
  - Commits SEPARADOS por type (functional vs structural — NUNCA mezclar)
  - Orden estricto: Protocol → Workflows → Skills → Cards → cross-links
  - Cada artefacto sigue template de _autoria/
  - Tokens medidos canónicamente chars/4 (GUIA_AUTOR §4.6)
  - Si Card mini >700 tokens → upgrade a CARD-std (no negociable)
  - Hook valida cada commit; si falla → fixear, NUNCA --no-verify

FASE D — Entrega
  - Push branch a origin
  - Subir reporte audit como attachment 2× (fileType=devlog Y fileType=code_logic — L10)
  - Postear SKL-REPORT-01 en la tarea (partir en N comments si supera ~5000 chars — L7)
  - Mover tarea task_in_progress → task_in_review (verificar transición permitida — L11)
  - Esperar review del Coord
```

---

## PASO 7 — Modelo Claude recomendado

| Sesión | Modelo |
|---|---|
| Auditoría FASE B (cross-walk denso, lectura quirúrgica) | **Claude Opus** (calidad de razonamiento) |
| FASE C construcción de Protocol/Workflows largos | **Claude Opus** (estructura editorial) |
| FASE A operativa + FASE D entrega (status, attachments, comments) | **Claude Sonnet** (rapidez en operaciones API) |

---

## PASO 8 — Herramientas

| Herramienta | Uso |
|---|---|
| `Read` / `Glob` / `Grep` | Lectura quirúrgica del repo (audit FASE B) — grep por patrones DEV-00X, INVOKE, etc. |
| `Write` / `Edit` | Generar Protocols/Workflows/Skills/Scripts/Cards |
| `Bash` o `PowerShell` | Git, VTT API, validaciones |
| `TodoWrite` | Toda tarea con ≥3 pasos (obligatorio en FASE C) |

---

## NUNCA HAGAS ESTO

- ❌ Editar normativa sin auditoría previa (FASE B obligatoria)
- ❌ Crear gaps "por las dudas" sin evidencia grep
- ❌ Mezclar functional + structural en mismo commit
- ❌ Commit directo a `main` (siempre branch `agent/tw-ops/vtt-setup/...`)
- ❌ `git commit --no-verify` (si el hook bloquea, fixear el problema)
- ❌ Postear datos sensibles en VTT (RULE-SEC-001)
- ❌ Usar URL con IP (77.42.88.106 etc) — siempre dominio `https://api.vttagent.com`
- ❌ Usar `/api/auth/login` (rate-limited) — siempre `/api/auth/service-token`
- ❌ Crear issues con `type=requirement` (NO existe — usar `blocker`/`improvement`/`other`)
- ❌ Resolver issues con `PATCH /api/issues/<id>/resolve` (NO existe — usar `PUT /api/issues/<id>`)
- ❌ Trabajar en el clone base — siempre en el worktree `.vtt/worktrees/vtt-setup-tw-ops/`
- ❌ Crear documentos en `03.templates/research/` (eso es RA)
- ❌ Crear documentos en `05.proyectos/*/operativos-instancias/` (eso es Coord)

---

## RESUMEN EN 1 LÍNEA

1. **PASO 0** — `cd worktree` + `export VTT_SETUP` + validar 02.normativa/
2. **PASO 1** — Leer 10 archivos del PASO 1
3. **PASO 1.bis** — Memorizar Protocols/Workflows/Skills/Scripts/Templates + Reglas N0
4. **PASO 2-4** — Datos + JWT + hook commit-msg
5. **PASO 5** — Pre-check (5 checks)
6. **PASO 6** — Workflow 4 fases (A setup / B audit / C construcción / D entrega)
7. **PASO 7-8** — Modelo Opus para FASE B/C, Sonnet para A/D

---

**Fuente de verdad operativa:** `OPERATIVO_TW-OPS_VTT-SETUP.md`
**Perfil base:** `AGENT_PROFILE_BASE_TW-OPS.md`
**Protocol que rige tu trabajo:** `VTT.PROTOCOL-GOV-002`
**Template estandarización:** `03.templates/agents/TEMPLATE_TRIADA_AGENTE.md` v1.0
**Versión:** 2.0 | **Fecha:** 2026-06-02
