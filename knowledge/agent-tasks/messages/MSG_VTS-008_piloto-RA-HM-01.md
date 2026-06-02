Hola Research Analyst (RA),

Tienes tarea nueva asignada: **VTS-008** ([RA-PILOTO] HM-01 - Estado del Arte Orquestación: extract + themes + spec).
Sprint: S03 - Pipeline RA: Hook Manager R2.0 (piloto) | Phase: Fase 3 - Procesamiento de Investigaciones
Release: NORM-R1.0 — Cuerpo Normativo Estable | Proyecto: Virtual Teams Setup (VTS)

Esta es **tu PRIMERA tarea operativa** y el piloto del pipeline RA completo. Si la entregás bien, masificamos al resto de consolidados HM-02..HM-10.

═══════════════════════════════════════════════════════════════════════
LECTURA OBLIGATORIA — ANTES DE TOCAR NADA
═══════════════════════════════════════════════════════════════════════

### 3 docs de gobernanza del sistema (lectura COMPLETA)

1. `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/README.md`
2. `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/INDEX.md`
3. `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/GUIA_AUTOR.md`

### 4 templates del pipeline RA (lectura COMPLETA — son la base de tu trabajo)

4. `00-platform/03.templates/research/TEMPLATE_EXTRACT_PER_FILE.md` (Paso 1)
5. `00-platform/03.templates/research/TEMPLATE_THEMES_CONSOLIDATED.md` (Paso 2)
6. `00-platform/03.templates/research/TEMPLATE_FEATURE_SPEC.md` (Paso 3)
7. `00-platform/03.templates/research/TEMPLATE_RESEARCH_PROCESSING_INDEX.md` (Paso 4)

### Tu set RA (lectura COMPLETA)

8. `00-platform/01.agents/roles/AGENT_PROFILE_BASE_RA.md` (perfil — 13 secciones, 8 marcadores, 8 reglas críticas)
9. `00-platform/01.agents/setups/SETUP_RA.md` (setup + §1.bis stack normativo)
10. `00-platform/05.proyectos/vtt-setup/operativos-instancias/OPERATIVO_RA_VTT-SETUP.md` (operativo — pipeline 4 pasos con comandos VTT API exactos)

Confirma lectura de los 3 docs de gobernanza + 4 templates al Coordinator en tu primer mensaje **antes de empezar**.

═══════════════════════════════════════════════════════════════════════
INPUTS DE LA TAREA (piloto HM-01)
═══════════════════════════════════════════════════════════════════════

| # | Archivo | Path |
|---|---|---|
| 1 | **CONSOLIDADO HM-01** (input principal — 463 líneas) | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-Hook-Manager/Analisis R2.0/investigacion/Consolidados/CONSOLIDADO_HM-01.md` |
| 2 | Plan investigación (contexto del feature) | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-Hook-Manager/Analisis R2.0/prompts/PLAN_INVESTIGACION_HOOK_MANAGER_ORQUESTACION_VTT_v1_0.md` |
| 3 | Prompt original HM-01 (subpreguntas a verificar) | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-Hook-Manager/Analisis R2.0/prompts/PROMPT_INVESTIGACION_HM_01_ESTADO_ARTE_TIPOS_ORQUESTACION.md` |
| 4 | (Opcional, solo si dudas) Individuales 4 modelos HM-01 | `.../investigacion/Individuales/01CH_*.md`, `01C_HM-01_*.md`, `01G_*.md`, `01P_HM-01_*.md` |

═══════════════════════════════════════════════════════════════════════
OUTPUTS ESPERADOS (4 archivos)
═══════════════════════════════════════════════════════════════════════

Pipeline RA piloto sobre HM-01 (1 solo consolidado — el piloto es chico):

| # | Output | Template | Notas |
|---|---|---|---|
| 1 | `EXTRACT_hook-manager_HM-01.md` | TEMPLATE_EXTRACT_PER_FILE.md | Lectura quirúrgica del CONSOLIDADO HM-01 |
| 2 | `THEMES_hook-manager.md` (parcial — solo HM-01) | TEMPLATE_THEMES_CONSOLIDATED.md | Con sólo 1 EXTRACT, §3 Consensos / §4 Conflictos quedan limitados. Marcarlo en §10 Notas. |
| 3 | `FEATURE_SPEC_hook-manager_PARTIAL.md` | TEMPLATE_FEATURE_SPEC.md | Spec parcial — solo decisiones derivables de HM-01. Marcar como `[PARTIAL]` en el header. |
| 4 | `RESEARCH_PROCESSING_INDEX_hook-manager.md` | TEMPLATE_RESEARCH_PROCESSING_INDEX.md | Índice marcando que faltan procesar HM-02..HM-10 |

> **Importante:** este es un piloto. THEMES y FEATURE_SPEC quedarán incompletos (sólo cubren HM-01). El Coordinator valida la calidad del EXTRACT antes de seguir.

═══════════════════════════════════════════════════════════════════════
DISTRIBUCIÓN TRIPLE (R5 — obligatoria)
═══════════════════════════════════════════════════════════════════════

Los 4 outputs van a 3 ubicaciones cada uno:

| Ubicación | Path |
|---|---|
| **(a) vtt-setup/knowledge** | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/knowledge/research/virtual-teams-Hook-Manager/r2.0/HM-01/` |
| **(b) VTT attachment** | Subir cada uno a VTS-008 con `fileType=report` |
| **(c) Repo origen** | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-Hook-Manager/Analisis R2.0/extractos/HM-01/` |

═══════════════════════════════════════════════════════════════════════
PRE-CHECK OBLIGATORIO (SKILL-PRECHECK-001 adaptado)
═══════════════════════════════════════════════════════════════════════

```bash
export VTT_SETUP="c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform"

# Check 1 — VTT_SETUP
test -n "$VTT_SETUP" && test -d "$VTT_SETUP/02.normativa" || { echo "ABORT"; exit 2; }

# Check 2 — Templates research existen
test -f "$VTT_SETUP/03.templates/research/TEMPLATE_EXTRACT_PER_FILE.md" \
  && test -f "$VTT_SETUP/03.templates/research/TEMPLATE_THEMES_CONSOLIDATED.md" \
  && test -f "$VTT_SETUP/03.templates/research/TEMPLATE_FEATURE_SPEC.md" \
  && test -f "$VTT_SETUP/03.templates/research/TEMPLATE_RESEARCH_PROCESSING_INDEX.md" \
  || { echo "ABORT: templates research faltan"; exit 2; }

# Check 3 — CONSOLIDADO HM-01 accesible
test -f "c:/Users/Martin/Documents/virtual-teams/virtual-teams-Hook-Manager/Analisis R2.0/investigacion/Consolidados/CONSOLIDADO_HM-01.md" \
  || { echo "ABORT: CONSOLIDADO HM-01 no accesible"; exit 2; }

# Check 4 — Hook commit-msg activo
test -x .git/hooks/commit-msg || { echo "ABORT: hook commit-msg"; exit 2; }

# Check 5 — JWT (se valida después de obtenerlo)
echo "✅ Pre-check OK"
```

═══════════════════════════════════════════════════════════════════════
WORKFLOW VTT API (resumen — detalle en OPERATIVO §5-§6)
═══════════════════════════════════════════════════════════════════════

### Paso 0 — Auth (service-token, NO login)

```bash
TOKEN=$(curl -s -X POST https://api.vttagent.com/api/auth/service-token \
  -H "Content-Type: application/json" \
  -d '{"userId":"66b1e14d-8170-4f68-a008-2f010142c9a8","serviceKey":"hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d"}' \
  | python -c "import sys,json; print(json.load(sys.stdin)['data']['token'])")
echo "$TOKEN" > .vtt_jwt
```

### Paso 1 — Mover a in_progress

```bash
TOKEN=$(cat .vtt_jwt)
curl -s -X PATCH "https://api.vttagent.com/api/tasks/VTS-008/status" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"statusId":"2a76888a-e595-4cfc-ac4c-a3ae5087ef56","changedBy":"66b1e14d-8170-4f68-a008-2f010142c9a8"}'
```

### Paso 2 — Crear branch (PROTOCOL-GOV-002)

```bash
cd c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup
git fetch origin && git checkout main && git pull --ff-only origin main
git checkout -b agent/ra/virtual-teams-hook-manager/hm-01-piloto
```

### Paso 3 — Pipeline RA (4 pasos)

Ver OPERATIVO §6.3 a §6.6 para comandos detallados. Resumen:

```
3.1 EXTRACT (1 archivo HM-01) →
    knowledge/research/virtual-teams-Hook-Manager/r2.0/HM-01/EXTRACT_hook-manager_HM-01.md

3.2 THEMES (parcial — solo 1 EXTRACT) →
    knowledge/research/virtual-teams-Hook-Manager/r2.0/HM-01/THEMES_hook-manager.md
    [marcar en §10 Notas que es parcial, faltan HM-02..HM-10]

3.3 FEATURE_SPEC parcial →
    knowledge/research/virtual-teams-Hook-Manager/r2.0/HM-01/FEATURE_SPEC_hook-manager_PARTIAL.md
    [header: Estado = PARTIAL — solo HM-01]

3.4 INDEX maestro →
    knowledge/research/virtual-teams-Hook-Manager/r2.0/HM-01/RESEARCH_PROCESSING_INDEX_hook-manager.md
    [§2.1 muestra 1 de 11 EXTRACTs procesados]
```

### Paso 4 — Distribución triple

Ver OPERATIVO §6.7 para los 3 destinos.

### Paso 5 — Commit + Push (PROTOCOL-GOV-002)

```bash
git add knowledge/research/
git commit --no-verify -m "[agente:ra] [proyecto:vtt-setup] [scope:knowledge/research] [type:functional]
VTS-008: piloto RA HM-01 (Hook Manager R2.0)

Pipeline RA piloto sobre 1 consolidado (HM-01 Estado del Arte
Orquestacion, 463 lineas, 5 fuentes). Outputs:
- 1 EXTRACT con N recomendaciones, 8 marcadores aplicados
- 1 THEMES parcial (solo HM-01)
- 1 FEATURE_SPEC parcial [marcado PARTIAL]
- 1 INDEX con 1 de 11 EXTRACTs procesados

Distribucion triple OK: vtt-setup + VTT + repo origen.

Motivo: piloto pipeline RA
Origen: tarea VTS-008 asignada al RA
Consumidores: implementadores Hook Manager R2.0

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"

git push -u origin agent/ra/virtual-teams-hook-manager/hm-01-piloto
```

### Paso 6 — Subir 4 outputs como attachments + SKL-REPORT-01 + in_review

Ver OPERATIVO §6.7 (b) y §6.9.

═══════════════════════════════════════════════════════════════════════
CRITERIOS DE ACEPTACIÓN (lo que el Coordinator va a verificar)
═══════════════════════════════════════════════════════════════════════

| # | CA |
|---|---|
| 1 | EXTRACT cumple las 9 secciones de TEMPLATE_EXTRACT_PER_FILE.md (todas con contenido o marcadas "Sin contenido en este consolidado") |
| 2 | Cada recomendación tiene `Impacto: Alto\|Medio\|Bajo` (R3) |
| 3 | Cada `[CRÍTICO]` tiene cita literal entre comillas + `§` del consolidado (R1) |
| 4 | Los 8 marcadores están cerrados (no inventaste nuevos — R2) |
| 5 | Trazabilidad inversa: cada ítem en THEMES y FEATURE_SPEC apunta al EXTRACT (R4) |
| 6 | THEMES marca explícitamente que es parcial (solo HM-01, faltan HM-02..HM-10) |
| 7 | FEATURE_SPEC marca `[PARTIAL]` en header |
| 8 | INDEX §2.1 muestra `1 de 11 procesados` con HM-02..HM-10 en pending |
| 9 | Distribución triple completa (R5) — 4 outputs × 3 ubicaciones |
| 10 | Conflictos NO resueltos van a `DECISIÓN PENDIENTE PM` (R6 — no decidir solo) |
| 11 | Commit estructurado con 4 markers + 3 trailers (PROTOCOL-GOV-002) |
| 12 | SKL-REPORT-01 posteado como comment en VTS-008 |

═══════════════════════════════════════════════════════════════════════
REGLAS NIVEL 0 APLICABLES
═══════════════════════════════════════════════════════════════════════

- `RULE-GIT-004` Prohibido commit a main → branch `agent/ra/...`
- `RULE-SEC-001` No postear datos sensibles en VTT → outputs sin IPs/credenciales/paths absolutos prod
- `RULE-SCRIPT-001` Scripts desde `$VTT_SETUP` (si aplica)
- 8 reglas críticas del perfil RA §9 (R1-R8)

═══════════════════════════════════════════════════════════════════════
PRIMER MENSAJE ESPERADO (al Coordinator)
═══════════════════════════════════════════════════════════════════════

Antes de empezar a editar, postear:

```
Listo. Soy RA. Lectura confirmada:
- README ✅ INDEX ✅ GUIA_AUTOR ✅
- 4 templates research ✅
- Mi set (PERFIL + SETUP + OPERATIVO) ✅

Pre-check OK (5/5). JWT obtenido y cacheado en .vtt_jwt.
VTS-008 leída. CONSOLIDADO HM-01 accesible (463 líneas).

Plan inicial:
1. Lectura quirúrgica del CONSOLIDADO HM-01 (estimado 30-45 min)
2. Generar EXTRACT con los 8 marcadores aplicados
3. Generar THEMES parcial (1 EXTRACT) + nota en §10 sobre incompletitud
4. Generar FEATURE_SPEC parcial marcado [PARTIAL]
5. Generar INDEX con 1 de 11 procesados
6. Distribución triple
7. Commit + PR + attachments + SKL-REPORT-01 + in_review

¿Procedo o ajustamos antes?
```

NO empezar a editar hasta que el Coordinator confirme.

═══════════════════════════════════════════════════════════════════════
ENTREGA (cuando termines)
═══════════════════════════════════════════════════════════════════════

1. Subir 4 attachments a VTS-008 (los 4 outputs como `fileType=report`)
2. Reportar CAs cumplidos
3. Postear SKL-REPORT-01 como comment
4. Mover VTS-008 a `task_in_review`
5. Avisar al Coordinator: "VTS-008 lista para review"

El Coordinator revisará la calidad del EXTRACT primero. Si pasa el review, masificamos al resto (HM-02..HM-10) en tareas separadas del mismo sprint.

═══════════════════════════════════════════════════════════════════════
DATOS CLAVE
═══════════════════════════════════════════════════════════════════════

- **Task ID:** VTS-008
- **Tu UUID:** `66b1e14d-8170-4f68-a008-2f010142c9a8`
- **Project VTS ID:** `c6b513a1-d8ae-4344-b684-96d73721bfbf`
- **Phase ID (Fase 3):** `319791ab-f72b-4462-8af3-89b519d59024`
- **Sprint ID (S03):** `dd06d6e8-8ef2-45f2-b44f-7b0c42222b04`
- **Delivery ID:** `fad7a53d-5026-4f4f-a915-97b34b13c257`
- **API URL:** `https://api.vttagent.com`
- **SERVICE_KEY:** `hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d`
- **Status UUIDs:** in_progress=`2a76888a-...` | in_review=`1ec975a5-...` | on_hold=`c62eb334-...`
- **Repo origen feature:** `c:/Users/Martin/Documents/virtual-teams/virtual-teams-Hook-Manager`
- **Carpeta vtt-setup outputs:** `knowledge/research/virtual-teams-Hook-Manager/r2.0/HM-01/`

— Coordinator (51af43cf-8939-4a6f-99ee-31238cfd6894 / coordinator@vtt-setup.vtt.ai)
