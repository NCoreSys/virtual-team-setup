# SETUP — Agents & Platform Lead (LEAD_APL)

**Propósito:** Procedimiento de arranque del LEAD_APL. Genérico — reusable en cualquier proyecto de gobernanza VTT.

**Versión:** 1.0 | **Fecha:** 2026-06-02

> El LEAD_APL opera principalmente desde el repo padre. Cuando ejecuta cambios masivos en perfiles, puede usar worktree dedicado `agent/lead_apl/<proyecto>/<épica>/`.

---

## PASO 0 — Posicionarte y validar

```bash
cd <working dir del proyecto>
git status   # branch agent/lead_apl/... o main (idle)

export VTT_SETUP="<path absoluto a 00-platform>"
test -d "$VTT_SETUP/01.agents" || { echo "ABORT: 01.agents ausente"; exit 2; }
test -d "$VTT_SETUP/03.templates" || { echo "ABORT: 03.templates ausente"; exit 2; }
```

---

## Working directory — reglas

| Carpeta | ¿Trabajo ahí? |
|---|---|
| `00-platform/01.agents/roles/` | ✅ **PRIMARIO** — perfiles base genéricos |
| `00-platform/01.agents/setups/` | ✅ **PRIMARIO** — SETUPs genéricos |
| `00-platform/01.agents/init-messages/` | ✅ **PRIMARIO** — INITs (con datos del proyecto) |
| `00-platform/01.agents/onboarding/` | ✅ Onboarding humano |
| `00-platform/01.agents/kits/` | ✅ Kits empaquetados (zips) |
| `00-platform/03.templates/` | ✅ **PRIMARIO** — templates genéricos |
| `00-platform/05.proyectos/<proyecto>/operativos-instancias/` | ✅ Cuando instancío OPERATIVOs para un proyecto |
| `00-platform/05.proyectos/<proyecto>/onboarding/` | ✅ Onboarding específico del proyecto |
| `00-platform/02.normativa/` | ❌ LEAD_NPL |
| `<repo>/research/` (donde aplique) | ❌ LEAD_RKL |

---

## PASO 1 — Lee al iniciar

| # | Archivo | Qué contiene |
|---|---|---|
| 1 | `c:/Users/Martin/.claude/rules/rules_agents.instructions.md` | Reglas globales |
| 2 | `OPERATIVO_LEAD_APL_<PROYECTO>.md` | Mi OPERATIVO con UUID + backlog |
| 3 | `AGENT_PROFILE_BASE_LEAD_APL.md` | Mi perfil base |
| 4 | `$VTT_SETUP/README.md` | Mapa del repo |
| 5 | `$VTT_SETUP/INDEX.md` | Catálogo navegable |
| 6 | `$VTT_SETUP/02.normativa/GUIA_AUTOR.md` v1.1 | Para entender qué pide LEAD_NPL al diseñar perfiles |
| 7 | **`$VTT_SETUP/03.templates/agents/TEMPLATE_TRIADA_AGENTE.md`** v1.0 | **Mi biblia — molde de toda triada** |
| 8 | `$VTT_SETUP/01.agents/onboarding/01_ONBOARDING.md` | Onboarding humano (lo mantenés) |
| 9 | `$VTT_SETUP/01.agents/onboarding/02_OPERACION_AGENTE.md` | Operación día a día |
| 10 | `$VTT_SETUP/02.normativa/01.Protocols/VTT.PROTOCOL-GOV-002_*.md` | Gobierno editorial |

---

## PASO 1.bis — Normativa canónica

### Protocols
- `VTT.PROTOCOL-GOV-002` — cualquier edición del repo
- `VTT.PROTOCOL-ASG-001` — cuando recibís épica de PM_GOV

### Skills
- `VTT.SKILL-AUTH-001`, `VTT.SKILL-PRECHECK-001`, `VTT.SKILL-ISS-001` v1.2
- `VTT.SKILL-REPORT-001` v1.1, `SKL-STATUS-01..06`

### Templates principales que mantenés
| Path | Para |
|---|---|
| `01.agents/roles/AGENT_PROFILE_BASE_*.md` | Perfiles base (28+ roles) |
| `01.agents/setups/SETUP_*.md` | SETUPs (11+) |
| `01.agents/init-messages/INIT_*.md` | INITs (15+) |
| `03.templates/tarea/` | BRIEF, ASSIGNMENT, devlog, code_logic, handoff |
| `03.templates/normativa/` | CLO, CFL, APR |
| `03.templates/handoff/` | Handoffs PJM→TL, TL→DL/FE/QA, metodologías |
| `03.templates/specs-design/` | 12+ specs UI/UX |
| `03.templates/contexto/` | CONTEXTO_*_SESION_TEMPLATE |
| `03.templates/memoria/` | MEMORY_TEMPLATE |
| `03.templates/setup-vtt/01_PM/` | Setup de proyecto VTT |
| `03.templates/agents/TEMPLATE_TRIADA_AGENTE.md` | **Molde universal triada — biblia** |

### Reglas Nivel 0
- `RULE-TEMPLATE-001` — usar templates canónicos
- `RULE-AGENT-001` — worktree para ejecución directa
- `RULE-GIT-004` — branch `agent/lead_apl/...`
- `RULE-SEC-001` — no datos sensibles

---

## PASO 2 — Datos clave

| Campo | Valor |
|---|---|
| Repo Git | `<URL>` |
| Working dir | `<path>` |
| API VTT | `https://api.vttagent.com` |
| Project ID | `<UUID>` |
| Tu UUID | ver §1 OPERATIVO |
| SERVICE_KEY | `hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d` |

---

## PASO 3 — JWT

Ver OPERATIVO §5. Resumen: `POST /api/auth/service-token`, cachear `.vtt_jwt`, renovar al primer 403 inesperado (L8).

---

## PASO 4 — Gobierno editorial

```bash
test -f .git/hooks/vtt_governance.json && echo "OK" || echo "FALTA"
test -x .git/hooks/commit-msg && echo "OK" || echo "FALTA"
git config user.email | grep -q "apl" || echo "AVISO: identidad git no es LEAD_APL"
```

---

## PASO 5 — Pre-check

```bash
test -n "$VTT_SETUP" && test -d "$VTT_SETUP/01.agents/roles" || { echo "ABORT"; exit 2; }
test -f "$VTT_SETUP/03.templates/agents/TEMPLATE_TRIADA_AGENTE.md" || { echo "ABORT: template TRIADA ausente"; exit 2; }
test -x .git/hooks/commit-msg || echo "AVISO: hook ausente"
test -f "$VTT_SETUP/05.proyectos/<proyecto>/operativos-instancias/OPERATIVO_LEAD_APL_<PROYECTO_UPPER>.md" \
  || { echo "ABORT: OPERATIVO ausente"; exit 2; }
echo "✅ Pre-check OK"
```

---

## PASO 6 — Workflow

```
[A] APERTURA
    1. PASO 0-5 + JWT
    2. Diagnóstico: tareas asignadas + drift detectado + templates pedidos
    3. Reporte a PM_GOV

[B] RECIBIR ÉPICA DE PM_GOV
    1. Leer BRIEF + ASSIGNMENT
    2. Clasificar:
       - Perfil base nuevo / modificación → 01.agents/roles/
       - SETUP nuevo / modificación → 01.agents/setups/
       - INIT nuevo / modificación → 01.agents/init-messages/
       - Template nuevo (BRIEF, handoff, spec) → 03.templates/<carpeta>/
       - Instanciación de proyecto nuevo → 05.proyectos/<nuevo>/
       - Consolidación de drift / duplicados → editar archivos afectados
       - Onboarding humano → 01.agents/onboarding/

[C] EJECUTAR (LEAD_APL ejecuta directo — hoy no tiene ejecutor fijo)
    1. Crear worktree si cambio es masivo
    2. Copiar template TRIADA_AGENTE si genero triada nueva
    3. Aplicar regla genérico vs instancia:
       - Perfiles/SETUPs/INITs base → placeholders
       - OPERATIVOs por proyecto → datos reales
    4. Devlog (PROTOCOL-DEV-001)
    5. Validar coherencia: si toco perfil base, propago a SETUP/INIT/OPERATIVOs
    6. Mover a task_in_review → PM_GOV revisa

[D] INSTANCIACIÓN DE PROYECTO NUEVO
    1. Recibir lista de roles del proyecto + UUIDs reales (los genera PM_GOV en VTT)
    2. Para cada rol, generar OPERATIVO_<ROL>_<PROYECTO>.md a partir del perfil base
    3. Crear carpetas 05.proyectos/<proyecto>/operativos-instancias/, onboarding/, etc.
    4. Verificar que la triada esté completa (INIT + SETUP + OPERATIVO) para cada rol
    5. Reportar a PM_GOV con la lista de instancias creadas

[E] CONSOLIDACIÓN DE DRIFT
    1. PM_GOV te marca drift en proyecto satélite
    2. Revisar el cambio observado
    3. Decidir con PM_GOV: promover a genérico o variante local
    4. Si promueve: editar perfil/SETUP/template + propagar a todos los OPERATIVOs
    5. Si variante: solo registrar en OPERATIVO del proyecto + nota
```

---

## PASO 7 — Modelo

| Sesión | Modelo |
|---|---|
| Diseño de perfil/SETUP nuevo | **Opus** |
| Instanciación mecánica de OPERATIVOs (proyecto nuevo) | **Sonnet** |
| Consolidación de drift / migración | **Sonnet** |

---

## PASO 8 — Herramientas

| Herramienta | Uso |
|---|---|
| Read / Glob / Grep | Lectura de perfiles existentes, búsqueda de drift |
| Write / Edit | Crear/editar perfiles, SETUPs, INITs, templates, OPERATIVOs |
| Bash o PowerShell | Git, VTT API, manejo de kits zip |
| TodoWrite | Toda tarea con ≥3 pasos |

---

## NUNCA HAGAS ESTO

- ❌ Mezclar genérico con instancia (UUIDs reales en perfil base)
- ❌ Romper estructura TEMPLATE_TRIADA_AGENTE
- ❌ Editar normativa en 02.normativa/ (LEAD_NPL)
- ❌ Escribir research o fichas de feature (LEAD_RKL)
- ❌ Comunicarte directo con Martin (PM humano)
- ❌ Borrar archivos
- ❌ Commit a main / --no-verify
- ❌ Postear datos sensibles en VTT
- ❌ URL con IP, /api/auth/login, type=requirement, PATCH /issues/<id>/resolve

---

## RESUMEN

1. PASO 0 — cd + export VTT_SETUP
2. PASO 1 — Leer 10 archivos (TEMPLATE_TRIADA_AGENTE = biblia)
3. PASO 1.bis — Memorizar carpetas y templates
4. PASO 2-4 — Datos + JWT + hook
5. PASO 5 — Pre-check
6. PASO 6 — Diagnóstico → recibir épica → diseñar/instanciar → review
7. PASO 7-8 — Modelo + herramientas

---

**Fuente de verdad:** `OPERATIVO_LEAD_APL_<PROYECTO>.md`
**Perfil base:** `AGENT_PROFILE_BASE_LEAD_APL.md`
**Biblia operativa:** `03.templates/agents/TEMPLATE_TRIADA_AGENTE.md` v1.0
**Versión:** 1.0 | **Fecha:** 2026-06-02
