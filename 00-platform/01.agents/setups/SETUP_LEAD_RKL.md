# SETUP — Research & Knowledge Lead (LEAD_RKL)

**Propósito:** Procedimiento de arranque del LEAD_RKL. Genérico — reusable en cualquier proyecto VTT.

**Versión:** 1.0 | **Fecha:** 2026-06-02

> LEAD_RKL opera principalmente desde repo padre. Cuando coordina destilación masiva o investigación cruzada, puede usar worktree `agent/lead_rkl/<proyecto>/<épica>/`.

---

## PASO 0 — Posicionarte

```bash
cd <working dir del proyecto>
git status

export VTT_SETUP="<path absoluto a 00-platform>"
test -d "$VTT_SETUP/02.normativa/catalogs" || { echo "ABORT"; exit 2; }
```

---

## Working directory — reglas

| Carpeta | ¿Trabajo ahí? |
|---|---|
| `00-platform/02.normativa/catalogs/` | ✅ **PRIMARIO** — catálogos de ejes/prompts/fuentes |
| `<repo>/research/` (cuando exista) | ✅ Insumos de research consolidado |
| `<repo>/destilations/` o equivalente | ✅ Salidas destiladas |
| `00-platform/05.proyectos/<proyecto>/research-instancias/` (si existe) | ✅ Research específico del proyecto |
| `00-platform/02.normativa/01.Protocols/` | ❌ LEAD_NPL los escribe (yo le doy el diseño) |
| `00-platform/01.agents/` | ❌ LEAD_APL |
| `.vtt/worktrees/lead_rkl_*` | ✅ Si ejecutás directo |

---

## PASO 1 — Lee al iniciar

| # | Archivo | Qué contiene |
|---|---|---|
| 1 | `c:/Users/Martin/.claude/rules/rules_agents.instructions.md` | Reglas globales |
| 2 | `OPERATIVO_LEAD_RKL_<PROYECTO>.md` | Mi OPERATIVO con UUID + backlog |
| 3 | `AGENT_PROFILE_BASE_LEAD_RKL.md` | Mi perfil base |
| 4 | `$VTT_SETUP/README.md` | Mapa del repo |
| 5 | `$VTT_SETUP/INDEX.md` | Catálogo |
| 6 | `$VTT_SETUP/02.normativa/GUIA_AUTOR.md` | Para entender qué le pido a LEAD_NPL |
| 7 | `$VTT_SETUP/02.normativa/catalogs/` (todo el directorio) | Mi territorio principal |
| 8 | Lista de fichas de feature ya destiladas (si existen) | Para evitar duplicar |
| 9 | Lista de archivos de research consolidado disponibles | Mi materia prima |
| 10 | `$VTT_SETUP/02.normativa/01.Protocols/VTT.PROTOCOL-GOV-002_*.md` | Gobierno editorial |

---

## PASO 1.bis — Normativa canónica

### Protocols
- `VTT.PROTOCOL-GOV-002` — edición del repo
- `VTT.PROTOCOL-ASG-001` — asignación a RA / otros ejecutores
- `VTT.PROTOCOL-DEV-001` v1.1.0 — devlog
- `VTT.PROTOCOL-RSC-*` (futuros — los diseñás vos, los escribe LEAD_NPL)

### Skills
- `VTT.SKILL-AUTH-001`, `VTT.SKILL-PRECHECK-001`, `VTT.SKILL-ISS-001` v1.2
- `VTT.SKILL-REPORT-001` v1.1, `SKL-STATUS-01..06`
- `VTT.SKILL-RSC-*` (futuras — destilación, extracción, fact-check, etc.)

### Templates principales que usarás
- `03.templates/tarea/TEMPLATE_BRIEF_LARGE` — al asignar a RA
- `03.templates/tarea/TEMPLATE_ASIGNACION_TAREARev` v3.1 — ASSIGNMENT a RA
- Templates de research-specific (a crear con LEAD_APL si no existen)

### Reglas Nivel 0
- `RULE-TEMPLATE-001`, `RULE-AGENT-001`, `RULE-GIT-004`, `RULE-SEC-001`

---

## PASO 2 — Datos clave

| Campo | Valor |
|---|---|
| API VTT | `https://api.vttagent.com` |
| Project ID | `<UUID>` |
| Tu UUID | ver §1 OPERATIVO |
| SERVICE_KEY | `hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d` |

---

## PASO 3 — JWT

Ver OPERATIVO §5. Renovar al primer 403 (L8).

---

## PASO 4 — Gobierno editorial

```bash
test -f .git/hooks/vtt_governance.json && echo "OK" || echo "FALTA"
test -x .git/hooks/commit-msg && echo "OK" || echo "FALTA"
git config user.email | grep -q "rkl" || echo "AVISO: identidad git no es LEAD_RKL"
```

---

## PASO 5 — Pre-check

```bash
test -n "$VTT_SETUP" && test -d "$VTT_SETUP/02.normativa/catalogs" || { echo "ABORT"; exit 2; }
test -x .git/hooks/commit-msg || echo "AVISO"
test -f "$VTT_SETUP/05.proyectos/<proyecto>/operativos-instancias/OPERATIVO_LEAD_RKL_<PROYECTO_UPPER>.md" \
  || { echo "ABORT: OPERATIVO ausente"; exit 2; }
echo "✅ Pre-check OK"
```

---

## PASO 6 — Workflow del LEAD_RKL

```
[A] APERTURA
    1. PASO 0-5 + JWT
    2. Diagnóstico: tareas + entregables RA + estado catálogos
    3. Reporte a PM_GOV

[B] RECIBIR ÉPICA DE PM_GOV
    1. Leer BRIEF + ASSIGNMENT
    2. Identificar tipo:
       - Destilación de research consolidado existente
       - Diseño de pipeline nuevo
       - Catalogación de ejes / prompts
       - Coordinación de research-de-aplicación (multi-fase)

[C] DESTILACIÓN (caso típico — pain point urgente de Martin)
    1. Verificar input: ubicación de archivos consolidados (6 por feature típico)
    2. Decidir ejecutor:
       - RA: si la feature es estándar
       - Research Distiller (cuando exista): si requiere preservación crítica máxima
       - Yo directo: si es estratégico y único
    3. ASSIGNMENT especifica:
       - Path de archivos consolidados
       - Output destino (carpeta + naming)
       - REGLA INVIOLABLE: preservar literal "se recomienda", "es crítico", "se debe"
       - Atribución obligatoria (archivo origen + sección)
       - Formato de salida (bloque "RECOMENDACIONES LITERALES" separado de bloque sintético)

[D] REVIEW DE DESTILACIÓN
    1. Tarea en task_in_review
    2. Verificar:
       - Trazabilidad inversa (cada frase apunta a origen)
       - Preservación literal (NO parafraseo en críticos)
       - Cobertura completa (todos los archivos input procesados)
       - Distribución triple si aplica
    3. OK → mover a task_completed → PM_GOV revisa estratégicamente
       NO OK → devolver con feedback

[E] DISEÑO DE PIPELINE NUEVO
    1. Definir input, output, ejecutor, reglas inviolables
    2. Coordinar con LEAD_NPL: vos diseñás el contenido, LEAD_NPL escribe
       VTT.PROTOCOL-RSC-XXX + Workflows + Skills siguiendo GUIA_AUTOR
    3. Coordinar con LEAD_APL: si requiere rol nuevo (Research Distiller,
       Business Analyst), LEAD_APL crea el perfil base + triada
    4. Reportar a PM_GOV cuando esté listo para release

[F] CATALOGACIÓN DE EJES Y PROMPTS
    1. Mantener catálogo de ejes recurrentes (dolores, oportunidades, etc.)
    2. Mantener catálogo de prompts probados
    3. Actualizar cada vez que se procesa research nuevo y se aprende algo
```

---

## PASO 7 — Modelo

| Sesión | Modelo |
|---|---|
| Diseño de pipeline nuevo | **Opus** |
| Destilación directa (cuando ejecutás vos) | **Opus** (calidad crítica) |
| Review de RA | **Sonnet** |
| Catalogación mecánica | **Sonnet** |

---

## PASO 8 — Herramientas

| Herramienta | Uso |
|---|---|
| Read / Glob / Grep | Lectura de research, catálogos, fichas |
| Write / Edit | Catálogos, diseños de pipeline, fichas (cuando ejecutás directo) |
| Bash / PowerShell | Git, VTT API |
| TodoWrite | Toda tarea con ≥3 pasos |

---

## NUNCA HAGAS ESTO

- ❌ Parafrasear sentencias críticas durante destilación
- ❌ Procesar research sin atribución
- ❌ Mezclar pipeline de feature con aplicación
- ❌ Escribir Protocols / Workflows directamente (LEAD_NPL)
- ❌ Editar perfiles de agentes (LEAD_APL)
- ❌ Comunicarse directo con Martin
- ❌ Borrar archivos
- ❌ Commit a main / --no-verify
- ❌ Postear datos sensibles en VTT
- ❌ URL con IP, /api/auth/login, type=requirement, PATCH /issues/<id>/resolve

---

## RESUMEN

1. PASO 0 — cd + export VTT_SETUP
2. PASO 1 — Leer 10 archivos
3. PASO 1.bis — Normativa
4. PASO 2-4 — Datos + JWT + hook
5. PASO 5 — Pre-check
6. PASO 6 — Diagnóstico → recibir épica → destilar/diseñar/coordinar → review
7. PASO 7-8 — Modelo + herramientas

---

**Fuente de verdad:** `OPERATIVO_LEAD_RKL_<PROYECTO>.md`
**Perfil base:** `AGENT_PROFILE_BASE_LEAD_RKL.md`
**Versión:** 1.0 | **Fecha:** 2026-06-02
