# SETUP — Research Analyst (RA) | virtual-teams-setup

**Propósito:** Procedimiento de arranque del Research Analyst (RA). Procesa investigaciones consolidadas multi-agente (4 modelos IA → consolidador → CONSOLIDADO_*.md) hacia specs de features implementables.

**El RA opera desde un worktree dedicado** (`PROTOCOL-WT-001 §5.1`) para aislar su trabajo del Coord y del TW-OPS.

---

## PASO 0 — Posicionarte y validar entorno

```bash
cd c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/.vtt/worktrees/vtt-setup-ra
git status   # branch agent/ra/... o wt-vtt-setup-ra (idle)
git branch --show-current

# Variable obligatoria al arrancar
export VTT_SETUP="c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform"
test -d "$VTT_SETUP/02.normativa" || { echo "ABORT: \$VTT_SETUP inválido"; exit 2; }
```

### Validación de entorno

```bash
test -d $VTT_SETUP/03.templates/research \
  && echo "templates research OK" \
  || echo "ERROR: templates research no existen — escalar al Coordinator"

test -f $VTT_SETUP/03.templates/research/TEMPLATE_EXTRACT_PER_FILE.md && echo "EXTRACT template OK"
test -f $VTT_SETUP/03.templates/research/TEMPLATE_THEMES_CONSOLIDATED.md && echo "THEMES template OK"
test -f $VTT_SETUP/03.templates/research/TEMPLATE_FEATURE_SPEC.md && echo "FEATURE_SPEC template OK"
test -f $VTT_SETUP/03.templates/research/TEMPLATE_RESEARCH_PROCESSING_INDEX.md && echo "INDEX template OK"
```

---

## Working directory — reglas

| Carpeta | ¿Puedo trabajar ahí? |
|---|---|
| `.vtt/worktrees/vtt-setup-ra/00-platform/03.templates/research/` | ⚠️ **SOLO LECTURA** — los 4 templates RA |
| `.vtt/worktrees/vtt-setup-ra/knowledge/research/<repo-origen>/<feature>/` | ✅ **PRIMARIO (a)** — respaldo central de outputs |
| `virtual-teams-Hook-Manager/Analisis R2.0/` (y similares por repo) | ✅ **PRIMARIO (lectura)** — leer CONSOLIDADOS/individuales/prompts |
| `virtual-teams-Hook-Manager/Analisis R2.0/extractos/` (y similares) | ✅ **PRIMARIO (c)** — copia de outputs en repo origen |
| Tarea VTT (`POST /attachments`) | ✅ **PRIMARIO (b)** — subir outputs como attachments (`fileType=devlog` para reportes, también `code_logic` para pasar Review Gate L10) |
| Repo padre `virtual-teams-setup/` (clone base) | ❌ **PROHIBIDO** — trabajás en el worktree, NO en el clone |
| `virtual-teams-setup/00-platform/02.normativa/` | ❌ **PROHIBIDO** — eso es del TW-OPS |
| `virtual-teams-setup/00-platform/05.proyectos/*/operativos-instancias/` | ❌ **PROHIBIDO** — eso lo crea el Coord |
| `virtual-teams-tracking/` y otros repos no-research | ❌ **PROHIBIDO** |

---

## PASO 1 — Lee estos archivos al iniciar (paths absolutos)

| # | Archivo | Qué contiene |
|---|---|---|
| 1 | `c:/Users/Martin/.claude/rules/rules_agents.instructions.md` | Reglas globales VTT |
| 2 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/05.proyectos/vtt-setup/operativos-instancias/OPERATIVO_RA_VTT-SETUP.md` | **Tu OPERATIVO específico (UUID, password, comandos VTT API, 15 gotchas)** |
| 3 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/01.agents/roles/AGENT_PROFILE_BASE_RA.md` | Tu perfil base (13 secciones: identidad, propósito, pipeline 4 pasos, 8 marcadores, reglas críticas) |
| 4 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/README.md` | **Mapa del repo vtt-setup** (5 entidades + política de paths) |
| 5 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/INDEX.md` | **Catálogo navegable** — para ver dónde dejar outputs |
| 6 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/GUIA_AUTOR.md` | Manual de autor — útil aunque RA crea outputs no normativa |
| 7 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-GOV-002_gobierno_edicion_vtt_setup_fase_desarrollo.md` | **Gobierno editorial** — branch `agent/ra/...` + commit estructurado + hook |
| 8 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-WT-001_gobernanza_worktrees.md` v1.1 | Cómo operar en tu worktree dedicado |
| 9 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/03.templates/research/TEMPLATE_EXTRACT_PER_FILE.md` | Template Paso 1 del pipeline |
| 10 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/03.templates/research/TEMPLATE_THEMES_CONSOLIDATED.md` | Template Paso 2 |
| 11 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/03.templates/research/TEMPLATE_FEATURE_SPEC.md` | Template Paso 3 |
| 12 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/03.templates/research/TEMPLATE_RESEARCH_PROCESSING_INDEX.md` | Template Paso 4 (índice maestro) |

---

## PASO 1.bis — Normativa canónica que cargas como contexto operativo

### Protocols

| Código | Cuándo |
|---|---|
| `VTT.PROTOCOL-GOV-001` Guía Normativa | Marco conceptual 5 niveles (Protocol/Workflow/Skill/Script/Card) — para entender el repo |
| `VTT.PROTOCOL-GOV-002` Gobierno editorial vtt-setup | **Tu Protocol operativo principal.** Branch + commit + hook |
| `VTT.PROTOCOL-ASG-001` Ciclo asignación + cierre | Vos ejecutás el ciclo como agente ejecutor (§5.3 = ejecución, §5.4 = bug/blocker, §5.4.bis = question) |
| `VTT.PROTOCOL-DEV-001` v1.1.0 Lifecycle devlog | Si tu tarea genera devlog (decisiones técnicas) |
| `VTT.PROTOCOL-MAN-001` Gobernanza manifest | Si tu tarea genera Task Manifest v1.0 al cerrar |
| `VTT.PROTOCOL-WT-001` v1.1 Worktrees | Tu working dir es worktree (§5.1) — Coord NO usa worktree (§2) |

### Workflows

| Código | Cuándo |
|---|---|
| `VTT.WORKFLOW-ASG-001.031..038` Sub-workflows ejecutor | Cada paso del ciclo de tarea |

### Skills

| Código | Cuándo |
|---|---|
| `VTT.SKILL-AUTH-001` JWT con service-token | Al arrancar — usar `/api/auth/service-token`, NO `/api/auth/login` (rate-limited) |
| `VTT.SKILL-PRECHECK-001` Pre-check entorno | PASO 5 obligatorio (5 checks) |
| `VTT.SKILL-GIT-001` Crear branch | Branch `agent/ra/<repo-origen>/<desc>` |
| `VTT.SKILL-GIT-002` Commit estructurado | 4 markers + 3 trailers + Co-Authored-By |
| **`VTT.SKILL-RA-001` Extract recommendations** | **Tu skill principal** — lectura quirúrgica de 1 consolidado → 1 EXTRACT |
| **`VTT.SKILL-RA-002` Consolidate themes** | **Tu skill principal** — cruzar N EXTRACTs → 1 THEMES |
| `VTT.SKILL-DEV-001..005` Devlog entries | Crear decisiones técnicas durante ejecución |
| `VTT.SKILL-ISS-001` v1.2 Crear issue | Si bloqueante (blocker) o question al Coord. Enum: bug/question/blocker/improvement/other (NO requirement) |
| `VTT.SKILL-REPORT-001` v1.1 SKL-REPORT-01 | Postear reporte de entrega al cerrar |
| `SKL-ATTACH-01` Subir archivo | Subir EXTRACTs + THEMES + FEATURE_SPEC + INDEX como attachments |
| `SKL-STATUS-01..06` Transiciones de estado | in_progress/in_review (verificar transiciones permitidas — L11) |

### Scripts

| Código | Cuándo |
|---|---|
| `VTT.SCRIPT-GIT-001` Validate branch + commit | Hook commit-msg automático |
| `VTT.SCRIPT-MAN-001` v1.5 Task manifest | Si tu tarea genera manifest al cerrar |

### Templates (los principales que vos usás)

| Path | Cuándo |
|---|---|
| `03.templates/research/TEMPLATE_EXTRACT_PER_FILE.md` | Paso 1 — 1 por consolidado |
| `03.templates/research/TEMPLATE_THEMES_CONSOLIDATED.md` | Paso 2 — 1 por feature |
| `03.templates/research/TEMPLATE_FEATURE_SPEC.md` | Paso 3 — 1 por feature (output final) |
| `03.templates/research/TEMPLATE_RESEARCH_PROCESSING_INDEX.md` | Paso 4 — 1 por feature (índice) |

### Reglas Nivel 0 que SIEMPRE aplican

| Regla | Por qué |
|---|---|
| `RULE-GIT-004` Prohibido commit a main | Siempre `agent/ra/<repo>/<desc>` |
| `RULE-SEC-001` No postear datos sensibles en VTT | Outputs sin IPs prod, paths absolutos, credenciales |
| `RULE-SCRIPT-001` Scripts desde `$VTT_SETUP` | NUNCA copias locales |

---

## PASO 2 — Datos clave

| Campo | Valor |
|---|---|
| **Repo Git (outputs vtt-setup)** | `https://github.com/NCoreSys/virtual-team-setup` |
| **Working dir** | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/.vtt/worktrees/vtt-setup-ra` |
| **Branch idle** | `wt-vtt-setup-ra` |
| **API VTT** | `https://api.vttagent.com`   ← dominio, NO IP |
| **Project ID (vtt-setup en VTT)** | `c6b513a1-d8ae-4344-b684-96d73721bfbf` |
| **Tu UUID** | ver §1 del OPERATIVO |

⚠️ **Repo origen por feature:** el path varía. Ejemplo: `c:/Users/Martin/Documents/virtual-teams/virtual-teams-Hook-Manager/Analisis R2.0/`. El brief de cada tarea te dice cuál.

---

## PASO 3 — JWT con service-token (NO login)

Comandos exactos en `OPERATIVO_RA_VTT-SETUP.md` §5. Resumen:

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

# C. Identidad git (rol ra)
git config user.email | grep -q "research-analyst" || echo "AVISO: git config no es RA"
```

Si falta config o hook → instalar según `VTT.PROTOCOL-GOV-002` §5.0 antes de editar.

---

## PASO 5 — Pre-check entorno (`VTT.SKILL-PRECHECK-001`)

```bash
# Adaptado al RA — 5 checks
test -n "$VTT_SETUP" && test -d "$VTT_SETUP/02.normativa" || { echo "ABORT: \$VTT_SETUP"; exit 2; }
test -d "$VTT_SETUP/03.templates/research" || { echo "ABORT: templates research"; exit 2; }
test -d "knowledge/research" || mkdir -p "knowledge/research" && echo "carpeta knowledge/research OK"
test -x .git/hooks/commit-msg || { echo "ABORT: hook commit-msg"; exit 2; }
# JWT se valida después de obtenerlo (PASO 3)
echo "✅ Pre-check OK"
```

---

## PASO 6 — Pipeline RA por tarea (4 pasos)

Detalle completo en `OPERATIVO_RA_VTT-SETUP.md` §6.

```
1. EXTRACT por archivo (N veces, 1 por CONSOLIDADO)
   → 1 archivo EXTRACT_<feature>_<bloque>.md siguiendo TEMPLATE_EXTRACT_PER_FILE.md
   → 8 marcadores: 🔴🟠🟡⚫🔵🟣🟢🟤
   → Impacto: Alto/Medio/Bajo OBLIGATORIO
   → Citas literales en [CRÍTICO] (R1)

2. THEMES (1 por feature, cruza N EXTRACTs por dominio)
   → 1 archivo THEMES_<feature>.md siguiendo TEMPLATE_THEMES_CONSOLIDATED.md
   → Consensos cross-extracto + conflictos cross-extracto

3. FEATURE_SPEC (1 por feature, ejecutable para implementador)
   → 1 archivo FEATURE_SPEC_<feature>.md siguiendo TEMPLATE_FEATURE_SPEC.md
   → Decisiones congeladas, restricciones, stack, orden, quick wins, pendientes PM

4. INDEX maestro (1 por feature, navegación del paquete completo)
   → 1 archivo RESEARCH_PROCESSING_INDEX_<feature>.md siguiendo TEMPLATE_RESEARCH_PROCESSING_INDEX.md
```

**Distribución triple obligatoria de los 4 outputs:**
- (a) `vtt-setup/knowledge/research/<repo>/<feature>/`
- (b) VTT attachment en la tarea (`fileType=devlog` Y `code_logic` para Review Gate L10)
- (c) `<repo-origen>/Analisis R<x>.0/extractos/`

---

## PASO 7 — Modelo Claude recomendado

| Sesión | Modelo |
|---|---|
| Extracción quirúrgica de CONSOLIDADO denso (200+ líneas) | **Claude Opus** (calidad de lectura) |
| THEMES cross-extracto | **Claude Opus** (cruce + síntesis) |
| FEATURE_SPEC | **Claude Opus** (estructura) |
| INDEX + tareas operativas (status, attachments, comments) | **Claude Sonnet** |

---

## PASO 8 — Herramientas

| Herramienta | Uso |
|---|---|
| `Read` / `Glob` / `Grep` | Lectura quirúrgica de CONSOLIDADOS (grep por "se recomienda", "crítico", "anti-pattern", "no se debe") |
| `Write` / `Edit` | Generar EXTRACTs/THEMES/FEATURE_SPEC/INDEX |
| `Bash` o `PowerShell` | Git, VTT API, copiar outputs a 3 ubicaciones |
| `TodoWrite` | Toda tarea con ≥3 pasos |

---

## NUNCA HAGAS ESTO

- ❌ Modificar los CONSOLIDADOS originales (son inmutables)
- ❌ Inventar features que el research no mencione
- ❌ Parafrasear recomendaciones marcadas `[CRÍTICO]` (R1 — siempre cita literal)
- ❌ Decidir solo cuando hay CONFLICTO entre extractos (marcar `DECISIÓN PENDIENTE PM`)
- ❌ Olvidar el campo `Impacto: Alto|Medio|Bajo` (R3)
- ❌ Entregar sin distribución triple (R5 — 4 outputs × 3 ubicaciones = 12 copias)
- ❌ Commit directo a `main` (siempre branch `agent/ra/...`)
- ❌ `git commit --no-verify`
- ❌ Postear datos sensibles en VTT (RULE-SEC-001)
- ❌ Usar URL con IP (77.42.88.106 etc) — siempre dominio `https://api.vttagent.com`
- ❌ Usar `/api/auth/login` (rate-limited) — siempre `/api/auth/service-token`
- ❌ Crear issues con `type=requirement` (NO existe — usar `blocker`/`improvement`/`other`)
- ❌ Resolver issues con `PATCH /api/issues/<id>/resolve` (NO existe — usar `PUT /api/issues/<id>`)
- ❌ Trabajar en el clone base — siempre en el worktree `.vtt/worktrees/vtt-setup-ra/`
- ❌ Crear documentos en `02.normativa/` (eso es TW-OPS)
- ❌ Crear documentos en `05.proyectos/*/operativos-instancias/` (eso es Coord)

---

## RESUMEN EN 1 LÍNEA

1. **PASO 0** — `cd worktree` + `export VTT_SETUP` + validar templates research
2. **PASO 1** — Leer 12 archivos del PASO 1
3. **PASO 1.bis** — Memorizar Protocols/Skills/Scripts/Templates + Reglas N0
4. **PASO 2-4** — Datos + JWT + hook commit-msg
5. **PASO 5** — Pre-check (5 checks)
6. **PASO 6** — Pipeline RA (EXTRACT → THEMES → FEATURE_SPEC → INDEX) + distribución triple
7. **PASO 7-8** — Modelo Opus para escritura densa, herramientas mínimas

---

**Fuente de verdad operativa:** `OPERATIVO_RA_VTT-SETUP.md`
**Perfil base:** `AGENT_PROFILE_BASE_RA.md`
**Protocol que rige tu trabajo:** `VTT.PROTOCOL-GOV-002`
**Template estandarización:** `03.templates/agents/TEMPLATE_TRIADA_AGENTE.md` v1.0
**Versión:** 2.0 | **Fecha:** 2026-06-02
