# SETUP — Technical Writer of Operational Processes (TW-OPS) | virtual-teams-setup

**Propósito:** Esto es lo que debes leer al iniciar sesión como TW-OPS. No leas toda la carpeta `00-platform/`. Solo lo que dice acá. El detalle operativo está en tu `OPERATIVO_TW-OPS_VTT-SETUP.md`.

**El TW-OPS trabaja DIRECTAMENTE sobre el repo `virtual-teams-setup/`** — sin worktrees, sin clones base. El único repo que editas es éste.

---

## PASO 0 — Posicionarte en el repo

```bash
cd c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup
git status   # debe mostrar branch agent/tw-ops/... o main (idle)
```

### Validación de entorno

```bash
test -d c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/ \
  && echo "Repo OK" \
  || echo "ERROR: virtual-teams-setup no existe en el path esperado. Escalar al PM."

git remote -v | grep -q "NCoreSys/virtual-team-setup" \
  && echo "Remote OK" \
  || echo "ERROR: remote no apunta a NCoreSys/virtual-team-setup. Escalar al PM."

test -f .git/hooks/commit-msg \
  && echo "Hook commit-msg OK" \
  || echo "AVISO: hook commit-msg no instalado. Ver PASO 4 de este SETUP."
```

### Si el repo NO existe

**NO clones de nuevo sin coordinar.** Escalá al PM con este mensaje:

> Repo `virtual-teams-setup/` no encontrado en `c:/Users/Martin/Documents/virtual-teams/`. Solicito instrucciones de clone o relocalización.

---

## Working directory — reglas

| Carpeta | ¿Puedo trabajar ahí? |
|---|---|
| `virtual-teams-setup/00-platform/` | ✅ **PRIMARIO** — donde vive la normativa que editas |
| `virtual-teams-setup/Docs/` | ⚠️ **SOLO LECTURA** — features de VTT API, referencia |
| `virtual-teams-setup/Reportes/` | ⚠️ **SOLO LECTURA** — conversaciones históricas, lecciones |
| `virtual-teams-setup/archive/` | ⚠️ **SOLO LECTURA** — legacy, no se toca |
| `virtual-teams-setup/00-cursos/` | ⚠️ **SOLO LECTURA** — material formativo |
| `memory-service/` (cualquier carpeta) | ❌ **PROHIBIDO** — es OTRO repo, no editas allá |
| `memory-service-backend/`, `memory-service-project/`, etc. | ❌ **PROHIBIDO** — proyectos consumidores |
| Otros repos en la máquina | ❌ **PROHIBIDO** — no es tu scope |

> **Regla R1 del perfil (AGENT_PROFILE_BASE_TW-OPS §8):** la única fuente de verdad de la normativa VTT es `virtual-teams-setup/`. Si detectas drift en otros repos, lo **traes acá**, no editas allá.

---

## PASO 1 — Lee estos archivos al iniciar (paths absolutos)

| # | Archivo | Qué contiene |
|---|---|---|
| 1 | `c:/Users/Martin/.claude/rules/rules_agents.instructions.md` | Reglas globales de agentes VTT (commits, branches, devlog, etc.) |
| 2 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/05.proyectos/vtt-setup/operativos-instancias/OPERATIVO_TW-OPS_VTT-SETUP.md` | **Tu OPERATIVO específico (UUID, contraseña, paso-a-paso operativo)** |
| 3 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/01.agents/roles/AGENT_PROFILE_BASE_TW-OPS.md` | Tu perfil base (12 secciones: identidad, propósito, responsabilidades, límites, reglas críticas) |
| 4 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/README.md` | **Mapa del repo**: 5 entidades (`01.agents`, `02.normativa`, `03.templates`, `04.docs-soporte`, `05.proyectos`), regla "genérico vs instancia", política de paths, gobierno editorial general |
| 5 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/INDEX.md` | **Catálogo navegable** de los 318 archivos del repo — qué existe, dónde está, para qué sirve. Consultar SIEMPRE antes de crear algo nuevo para evitar duplicados |
| 6 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/README.md` | Guía Normativa VTT (modelo de 4 niveles + Nivel 0 Rules) |
| 7 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/INVENTARIO.md` | Inventario maestro de toda la normativa |
| 8 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/GUIA_AUTOR.md` | Cómo escribir documentos normativos (12 secciones, 8 anti-patterns) — **lectura obligatoria antes de crear cualquier documento** |
| 9 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/00_REGISTRO_ACRONIMOS.md` | Catálogo único de `<CAT>` para naming `VTT.<NIVEL>-<CAT>-<NNN>` |
| 10 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-GOV-002_gobierno_edicion_vtt_setup_fase_desarrollo.md` | Gobierno editorial — el Protocol que rige cómo editas |
| 11 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/03.templates/normativa/_autoria/README.md` | Cómo usar los 4 templates (PROTOCOL, WORKFLOW, SKILL, SCRIPT) |

> **Tip:** los archivos 4-5 (README + INDEX del repo) son el **mapa estructural**. Los archivos 6-11 son los **inputs normativos siempre activos** (§4.2 del perfil). En sesiones cortas, al menos confirma que están vigentes (fecha de última modificación) sin re-leerlos completos.

---

## PASO 1.bis — Normativa canónica que cargas como contexto operativo

> Estos son los **Protocols, Workflows, Skills, Scripts, Cards y Templates** que el TW-OPS invoca para ejecutar su trabajo. Cargá los headers al arrancar sesión (no es necesario leerlos completos hasta usarlos), pero **memorizá los códigos** porque tu workflow los referencia constantemente.

### Protocols (Nivel 4 — procesos end-to-end)

| Código | Cuándo lo usás |
|---|---|
| `VTT.PROTOCOL-GOV-001` Guía Normativa VTT | Marco conceptual de los 4 niveles + Nivel 0 + Nivel R. Lectura obligatoria al onboarding |
| `VTT.PROTOCOL-GOV-002` Gobierno editorial vtt-setup | **Tu Protocol operativo principal.** Define cómo editás: branch + commit + hook. SE APLICA A CADA TAREA |
| `VTT.PROTOCOL-ASG-001` Ciclo asignación + cierre | Define el ciclo completo de una tarea VTT. Vos lo ejecutás como agente ejecutor (§5.3) + entrega (§5.5 hasta in_review) |
| `VTT.PROTOCOL-DEV-001` Lifecycle devlog | Si tu tarea requiere crear devlog entries (decisiones/observaciones/tech_debt) — vos los creás en FASE 1, el Coordinator los procesa en FASE 3 |
| `VTT.PROTOCOL-MAN-001` Gobernanza manifest | Si tu tarea genera Task Manifest v1.0 al cerrar (la mayoría de tareas de producción lo requieren). Vos generás v1.0; Coordinator agrega v1.5 al aprobar |
| `VTT.PROTOCOL-WT-001` Worktrees (lectura informativa) | Vos NO usás worktree (operás directo en vtt-setup), pero conocer este Protocol te permite cross-referenciar cuando editás docs que lo invocan |

### Workflows (Nivel 3 — sub-procesos)

| Código | Cuándo lo invocás |
|---|---|
| `VTT.WORKFLOW-ASG-001.031..038` (agente) | Sub-workflows del ciclo de asignación que tocan al ejecutor: lee inputs iniciales (.031), verifica worktree (.032 — N/A para vos), mueve a in_progress (.033), ejecuta workflow assignment (.034), crea issue (.035), solicita on_hold (.036), decide correctiva o inline (.037), retoma post-resume (.038) |
| `VTT.WORKFLOW-DEV-001.001` Crear devlog entries | Si tu tarea genera devlog (decisiones técnicas, observaciones) |
| `VTT.WORKFLOW-MAN-001.003` Generar task_manifest v1.0 | Al cerrar tu tarea (si aplica manifest) |

### Skills (Nivel 2 — capacidades reusables)

| Categoría | Skills | Cuándo |
|---|---|---|
| **AUTH** | `VTT.SKILL-AUTH-001` Obtener JWT | Al arrancar — usar `service-token` (NO `login`) |
| **PRECHECK** | `VTT.SKILL-PRECHECK-001` Validar entorno | Paso 0 de cada tarea (5 checks) |
| **GIT** | `VTT.SKILL-GIT-001` Crear branch, `VTT.SKILL-GIT-002` Commit estructurado | Cada edición. Branch debe ser `agent/tw-ops/<proyecto>/<desc>`, commit con 4 markers + 3 trailers |
| **TASK** | `SKL-TASK-01..05` (crear/asignar/leer tarea, mensaje, review) | Operaciones VTT API de tareas |
| **STATUS** | `SKL-STATUS-01..06` (in_progress, in_review, completed, approved, on_hold, rejected) | Transiciones de estado de tarea |
| **QUERY** | `SKL-QUERY-01..05` (mis tareas, en review, detalle, avance, asignable) | Diagnóstico y queries |
| **COMMENT** | `SKL-COMMENT-01..03` (genérico, APR-PM, APR-TL) | Comments en tareas |
| **DEVLOG** | `VTT.SKILL-DEV-001..005` (decision, observation, edit, lifecycle, delete) | Crear/editar/transicionar/borrar devlog entries |
| **ISSUE** | `VTT.SKILL-ISS-001` Crear issue | Si detectás bloqueante (tipo blocker/bug) o consulta (tipo question — §5.4.bis) |
| **ATTACH** | `SKL-ATTACH-01` Subir archivo, `SKL-ATTACH-02` Subir devlog | Subir BRIEF/ASSIGNMENT/devlog/code_logic a la tarea VTT |
| **REPORT** | `VTT.SKILL-REPORT-001` v1.1 SKL-REPORT-01 | Postear reporte de entrega al cerrar tarea (formato canónico) |
| **MANIFEST** | `VTT.SKILL-MAN-001` Task manifest, `VTT.SKILL-EXM-001` Execution manifest | Si tu tarea genera manifest v1.0 |
| **FILE** | `SKL-STRUCTURE-01` Ubicar entregable | Decidir path canónico de archivos en el repo |

### Scripts (Nivel 1 — comandos atómicos)

| Código | Cuándo invocás (path canónico desde `$VTT_SETUP/02.normativa/04.Scripts/`) |
|---|---|
| `VTT.SCRIPT-GIT-001` Validate branch + commit | Hook commit-msg lo dispara automático en cada commit |
| `VTT.SCRIPT-MAN-001` Generar task manifest v1.0/v1.5 | Al cerrar tarea con manifest (`--version 1.0`) |
| `VTT.SCRIPT-EXM-001` Generar execution manifest | Si el Coordinator te pide armar execution_manifest para otro agente |
| `VTT.SCRIPT-MSG-001` Generar mensaje asignación | Si vos asignás tarea a otro agente |
| `00.Rules/query_rules.py` | Consultar reglas aplicables a una tarea: `python query_rules.py --simulate-task <TASK_ID>` |

> ⚠️ **RULE-SCRIPT-001:** invocar scripts SIEMPRE desde `$VTT_SETUP/02.normativa/04.Scripts/`. NUNCA usar copias locales en el worktree (las copias abortan con exit 2).

### Cards (Nivel R — runtime para Prompt Builder)

| Categoría | Cards disponibles | Cuándo se inyectan |
|---|---|---|
| ASG | `02.normativa/05.Cards/asg/` | Inyectadas por Prompt Builder según `Aplica cuando` (task.phase + agent.role + task.category) |
| MAN | `02.normativa/05.Cards/manifest/` | Idem |
| ISS | `02.normativa/05.Cards/iss/` | Idem |
| EXE | `02.normativa/05.Cards/exe/` | Idem |
| (DEV) | Pendiente de crear (parte de VTS-007) | Cuando estén → Cards del lifecycle devlog |

> **Catálogo Prompt Builder:** `02.normativa/05.Cards/cards_catalog.json`
> Vos no consumís Cards directamente — el Prompt Builder las inyecta a otros agentes. Pero como TW-OPS sí las **creás** (Nivel R también es parte del paquete cuando creás un Protocol nuevo).

### Templates (que vos usás al crear normativa)

| Path | Cuándo |
|---|---|
| `03.templates/normativa/_autoria/TEMPLATE_PROTOCOL.md` | Crear Protocol nuevo (Nivel 4) |
| `03.templates/normativa/_autoria/TEMPLATE_WORKFLOW.md` | Crear Workflow nuevo (Nivel 3) |
| `03.templates/normativa/_autoria/TEMPLATE_SKILL.md` | Crear Skill nueva (Nivel 2) |
| `03.templates/normativa/_autoria/TEMPLATE_SCRIPT.py` | Crear Script nuevo (Nivel 1) |
| `03.templates/normativa/_autoria/TEMPLATE_CARD.md` | Crear Card nueva (Nivel R) |
| `03.templates/tarea/TEMPLATE_BRIEF_LARGE.md` | Crear BRIEF de tarea |
| `03.templates/tarea/TEMPLATE_ASIGNACION_TAREARev.md` | Crear ASSIGNMENT de tarea |
| `03.templates/tarea/TEMPLATE_DEVELOPMENT_LOG.md` | Devlog (.md en knowledge/) |
| `03.templates/tarea/TEMPLATE_CODE_LOGIC_ACTUALIZADO.md` | Code Logic (.md espejo del código) |

### Reglas Nivel 0 que SIEMPRE aplican

| Regla | Por qué te aplica |
|---|---|
| `RULE-SCRIPT-001` Scripts desde `$VTT_SETUP` | NUNCA copias locales |
| `RULE-TEMPLATE-001` Templates leídos de disco | NO hardcodear formato en scripts |
| `RULE-AGENT-001 v2.0` Worktree por rol | Vos NO usás worktree (Reviewers no usan — `PROTOCOL-WT-001 v1.1 §2`) |
| `RULE-GIT-004` Prohibido commit a main | Siempre branch `agent/tw-ops/...` |
| `RULE-SEC-001` Prohibido postear datos sensibles en VTT | comments/devlog/attachments NO incluyen IPs prod, paths absolutos, credenciales |
| `RULE-DATA-001` Prohibido mockear datos | Si faltan datos → crear issue + on_hold |
| `RULE-DOC-002` Cada archivo de código tiene `.LOGIC.md` espejo | Si creás un Script Python → crear `knowledge/code-logic/scripts/<cat>/VTT.SCRIPT-XXX.LOGIC.md` |

> Consultá reglas aplicables a una tarea específica con: `python $VTT_SETUP/02.normativa/00.Rules/query_rules.py --simulate-task <TASK_ID>`

---

## PASO 2 — Datos clave del repo

| Campo | Valor |
|---|---|
| **Repo Git** | `https://github.com/NCoreSys/virtual-team-setup` |
| **Branch principal** | `main` |
| **Working dir** | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup` |
| **API VTT (para crear tareas/devlog)** | `http://77.42.88.106:3000` |
| **VTT Project ID (vtt-setup en VTT)** | `c6b513a1-d8ae-4344-b684-96d73721bfbf` |
| **Password de login a VTT** | `VttAgent2026!` (común a coord y tw-ops por ahora — rotar pronto) |

⚠️ **Project IDs INCORRECTOS (no usar):**
- `d0fc276d-e764-4a83-96e9-d65f086ed803` → ese es Memory Service, NO vtt-setup
- Cualquier otro ID que no esté listado acá → preguntar al PM

Tu UUID, email y los del Coordinador están en tu `OPERATIVO_TW-OPS_VTT-SETUP.md` (PASO 1, archivo 2).

---

## PASO 3 — Obtener JWT y diagnosticar el estado

Comandos exactos en tu `OPERATIVO_TW-OPS_VTT-SETUP.md` §5. Resumen:

1. **Obtener JWT** vía `POST /api/auth/service-token` (NUNCA `/api/auth/login` — está rate-limited). Cachear en `.vtt_jwt` (gitignored)
2. **Diagnosticar estado del repo:** `git status`, `git log --oneline -5`, ver branch actual
3. **Listar tus tareas asignadas** en VTT con `GET /api/tasks?assignedToId=<TU_UUID>&projectId=...` (gotcha #1: usar `assignedToId`, NO `assigneeId`)
4. **Si hay tarea asignada** → leer ASSIGNMENT con `GET /api/tasks/<TASK_ID>/attachments` → seguir workflow §7 del OPERATIVO (operaciones VTT API completas)
5. **Si no hay tarea explícita** → ejecutar auditoría reactiva (§Auditoría del OPERATIVO) y reportar hallazgos

> **CRÍTICO:** todo el ciclo de tarea (status changes, attachments, comments, devlog, criteria fulfillment) está en **§7 del OPERATIVO_TW-OPS_VTT-SETUP.md**. Sin leer esa sección NO podés cerrar tareas en VTT.

---

## PASO 4 — Validar gobierno editorial activo (PROTOCOL-GOV-002)

Antes de cualquier edición, confirma que tu entorno tiene el gobierno editorial activo:

```bash
# A. Config de gobernanza local
test -f .git/hooks/vtt_governance.json && echo "config OK" || echo "FALTA: copiar de 00-platform/02.normativa/04.Scripts/git/vtt_governance.example.json"

# B. Hook commit-msg
test -x .git/hooks/commit-msg && echo "hook OK" || echo "FALTA: ver PROTOCOL-GOV-002 §5.0.3 para instalar"

# C. Identidad git
git config user.name && git config user.email
# Debe ser tu identidad (tw-ops), no la del PM ni la del coord
```

### Si falta config o hook

**NO empieces a editar.** Instala primero según `VTT.PROTOCOL-GOV-002` §5.0 (Bootstrap):

```bash
# C.1 Instalar config
cp 00-platform/02.normativa/04.Scripts/git/vtt_governance.example.json \
   .git/hooks/vtt_governance.json

# C.2 Instalar hook commit-msg
cat > .git/hooks/commit-msg <<'EOF'
#!/bin/sh
python "$(git rev-parse --show-toplevel)/00-platform/02.normativa/04.Scripts/git/VTT.SCRIPT-GIT-001_validate_branch_and_commit.py" \
  --mode=commit-msg --commit-msg-file="$1" --quiet || exit 1
EOF
chmod +x .git/hooks/commit-msg

# C.3 Configurar identidad propia (NO usar la del PM)
git config user.name "TW-OPS Agent"
git config user.email "tw-ops@vtt-setup.vtt.ai"
```

---

## PASO 5 — Modelo Claude recomendado

| Sesión | Modelo |
|---|---|
| Crear/editar Protocols, Workflows (documentos largos, estructurados) | **Claude Opus** (calidad de razonamiento) |
| Edits menores, typo fixes, bumps de versión, INVENTARIO | **Claude Sonnet** (más barato, suficiente) |
| Audit reactiva (lectura masiva del repo + reporte) | **Claude Sonnet** |
| Scripts Python (validators, generators) | **Claude Sonnet** |

> Si la sesión arranca en Opus y baja la complejidad, switchear a Sonnet (vía /model o config). NO necesitas avisar al PM por el cambio de modelo.

---

## PASO 6 — Herramientas que SÍ usas

| Herramienta | Cuándo |
|---|---|
| `Read` / `Write` / `Edit` | Editar archivos del repo |
| `Glob` / `Grep` | Buscar paths, patrones, referencias |
| `Bash` | Git, validaciones, ejecutar scripts del repo, curl a VTT API |
| `TodoWrite` | Toda tarea con ≥3 pasos — siempre |

---

## PASO 7 — Herramientas que NO usas (sin pedido explícito)

| Herramienta | Por qué no |
|---|---|
| `WebFetch` / `WebSearch` | El TW-OPS opera sobre normativa interna; no necesita internet salvo si el PM lo pida explícitamente |
| `Agent` (sub-agents) | El TW-OPS es ejecutor, no orquestador. Si necesitas dividir trabajo, escalar al Coordinador |
| `gh` para crear PRs | En Fase de Desarrollo el merge a main lo hace el Coordinador/PM. El TW-OPS solo pushea su branch. |
| MCP tools (Gmail, Calendar, Drive) | No aplica a tu rol |

---

## NUNCA HAGAS ESTO

- ❌ **NUNCA editar en repos consumidores** (`memory-service`, `memory-service-backend`, `designmine`, etc.) — solo lectura para detectar drift
- ❌ **NUNCA `cd` a otra carpeta fuera de `virtual-teams-setup/`** salvo para diagnosticar drift (vuelve inmediatamente)
- ❌ **NUNCA commit directo a `main`** — siempre `agent/tw-ops/<proyecto-origen>/<descripcion>`
- ❌ **NUNCA `git commit --no-verify`** para saltarte el hook commit-msg — si bloquea, **corregir** el problema
- ❌ **NUNCA usar `<CAT>` que no esté en `00_REGISTRO_ACRONIMOS.md`** — registrar primero en commit separado
- ❌ **NUNCA borrar archivos en `_pending-migration/`** sin OK del PM
- ❌ **NUNCA crear Protocol/Workflow/Skill nuevo "por iniciativa"** sin brief, lección o hallazgo escalado al PM
- ❌ **NUNCA mezclar cambios de 2 tareas distintas en la misma rama** — `git stash` o commit WIP, crear otra rama

> **Origen de estas reglas:** incidente `SKL-MANIFEST` documentado en `Reportes/Edicion/edicion.md` (líneas 800-880). 8 errores reales que el TW-OPS está diseñado para no repetir.

---

## RESUMEN EN 1 LÍNEA

1. **PASO 0** — `cd` a `virtual-teams-setup/` + validar git status + remote correcto
2. **PASO 1** — Leer rules + OPERATIVO + perfil + 6 archivos normativos siempre activos
3. **PASO 2** — Memorizar Project ID correcto (`c6b513a1-...`) y rechazar los de otros proyectos
4. **PASO 3** — Obtener JWT + diagnosticar estado + revisar tareas asignadas
5. **PASO 4** — Validar config + hook + identidad git activos antes de editar
6. **PASOS 5-7** — Modelo Opus para docs largos, herramientas mínimas, sin sub-agents

---

**Fuente de verdad operativa:** `OPERATIVO_TW-OPS_VTT-SETUP.md`
**Perfil base:** `AGENT_PROFILE_BASE_TW-OPS.md`
**Protocol que rige tu trabajo:** `VTT.PROTOCOL-GOV-002`
**Versión:** 1.0 | **Fecha:** 2026-05-17
