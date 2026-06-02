Hola Technical Writer of Operational Processes (TW-OPS),

Tienes tarea nueva asignada: **VTS-007** ([AUDIT-NORM] PROTOCOL-DEV-001: auditar y completar paquete (5 niveles + integración ASG-001)).
Sprint: S01 - Setup ciclo + backlog inicial | Phase: Fase 2 - Desarrollo de Protocolos
Release: NORM-R1.0 — Cuerpo Normativo Estable | Proyecto: Virtual Teams Setup (VTS)

═══════════════════════════════════════════════════════════════════════
LECTURA OBLIGATORIA — ANTES DE TOCAR NADA
═══════════════════════════════════════════════════════════════════════

Lee EN ORDEN y COMPLETOS los 3 documentos de gobernanza del sistema:

1. `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/README.md`
   → Mapa del repo (5 entidades), regla genérico vs instancia, política de paths

2. `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/INDEX.md`
   → Catálogo navegable de los 318+ archivos. Consultar SIEMPRE antes de crear algo nuevo.

3. `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/GUIA_AUTOR.md`
   → Cómo se crean documentos normativos: árbol de decisión de nivel, 8 anti-patterns,
     checklist por nivel, workflow del autor en 10 pasos. ES TU MANUAL.

Después lee tu SETUP §1.bis (que tiene tu stack normativo completo: Protocols/Workflows/
Skills/Scripts/Cards/Templates/Reglas que invocás) y tu OPERATIVO §7 (operaciones VTT API).

Confirma lectura de los 3 docs de gobernanza al Coordinator en tu primer mensaje antes de empezar.

═══════════════════════════════════════════════════════════════════════
WORKING DIRECTORY (sin worktree — operás directo en vtt-setup)
═══════════════════════════════════════════════════════════════════════

Tu cwd: `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/`

Reglas:
- Operás DIRECTAMENTE en virtual-teams-setup/ (NO usás worktrees — los worktrees son para
  agentes ejecutores de proyectos de código como BE/FE/DB; vos sos editor de normativa)
- Cada tarea = nueva branch desde main con formato `agent/tw-ops/<proyecto-origen>/<desc>`
- Tu Protocol de gobierno editorial es `VTT.PROTOCOL-GOV-002`
- Tu hook commit-msg DEBE estar activo (validates branch + commit format)

Variable de entorno obligatoria al arrancar:
```bash
export VTT_SETUP="c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform"
test -d "$VTT_SETUP/02.normativa" || { echo "ABORT: \$VTT_SETUP inválido"; exit 2; }
```

═══════════════════════════════════════════════════════════════════════
PRE-CHECK OBLIGATORIO — antes de empezar la tarea (VTT.SKILL-PRECHECK-001)
═══════════════════════════════════════════════════════════════════════

```bash
# Check 1 — $VTT_SETUP existe
test -n "$VTT_SETUP" && test -d "$VTT_SETUP/02.normativa" || { echo "ABORT"; exit 2; }

# Check 2 — Scripts canónicos presentes
test -f "$VTT_SETUP/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py" \
  || { echo "ABORT: SCRIPT-MAN-001 ausente"; exit 2; }

# Check 3 — NO copias locales (RULE-SCRIPT-001)
ROGUE=$(find . -maxdepth 4 -type f \( -name "VTT.SCRIPT-MAN-*.py" -o -name "VTT.SCRIPT-MSG-*.py" \) 2>/dev/null)
test -z "$ROGUE" || { echo "ABORT: copias locales detectadas"; exit 2; }

# Check 4 — Hook commit-msg activo (PROTOCOL-GOV-002)
test -x .git/hooks/commit-msg || { echo "ABORT: hook commit-msg no instalado — ver PROTOCOL-GOV-002 §5.0"; exit 2; }

# Check 5 — Identidad git
git config user.email | grep -q "tw-ops" || { echo "AVISO: git config user.email no es tw-ops"; }

echo "✅ Pre-check OK"
```

═══════════════════════════════════════════════════════════════════════
OBJETIVO DE LA TAREA — VTS-007
═══════════════════════════════════════════════════════════════════════

Auditar el paquete normativo del **Devlog Lifecycle** (PROTOCOL-DEV-001) y completar gaps
en los 5 niveles del modelo VTT (Protocol + Workflow + Skill + Script + Card).

### Inputs

| # | Archivo | Por qué |
|---|---|---|
| 1 | `Docs/01-documentacion/features mod dinamico/FEATURE_DEVLOG_LIFECYCLE.md` | Feature origen v1.0 (2026-05-21) — la spec funcional |
| 2 | `00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-DEV-001_ciclo_devlog_entry.md` | Protocol existente v1.0.0 — base a auditar |
| 3 | `00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-ASG-001_ciclo_asignacion_tarea.md` | Para verificar integración con FASE 1/3/4 del DEV-001 |
| 4 | `00-platform/02.normativa/03.Skills/dev/` (5 skills existentes: DEV-001..005) | Inventario de Skills DEV |
| 5 | `00-platform/02.normativa/05.Cards/README.md` + `cards_catalog.json` | Modelo de Cards Nivel R + template `TEMPLATE_CARD.md` |
| 6 | `00-platform/02.normativa/GUIA_AUTOR.md` | Tu manual de autor — checklist por nivel |
| 7 | `00-platform/02.normativa/00_REGISTRO_ACRONIMOS.md` | Verificar que `DEV` está activo (lo está) |

### Hallazgos preliminares (lo que el Coordinator ya detectó — vos confirmás y completás)

| Nivel | Estado preliminar | Acción esperada |
|---|---|---|
| **Protocol** DEV-001 | ✅ v1.0.0 existe | Auditar contra FEATURE + ASG-001 → si hay gaps → bump v1.1.0 |
| **Workflows** DEV-001.001/.002/.003 | ❌ NO existen en disco | Crear los 3 siguiendo `TEMPLATE_WORKFLOW.md` |
| **Skills** DEV-001..005 | ✅ Existen | Auditar alineamiento con Protocol |
| **Skills** DEV-006/007/008 | ⚠️ Mencionadas pero faltan | Verificar si se necesitan o eliminar referencias |
| **Scripts** DEV | ❌ Carpeta no existe | Evaluar si aplica algún script atómico DEV; si no → documentar por qué |
| **Cards** DEV (Nivel R) | ❌ No hay `05.Cards/dev/` | Crear las Cards aplicables siguiendo `TEMPLATE_CARD.md` (presupuesto mini/std/large según contenido) |
| **Integración ASG-001** | A verificar | FASE 1 DEV ↔ ASG §5.3 / FASE 3 DEV ↔ ASG §5.5 / FASE 4 DEV ↔ ASG §5.6 |
| **Cross-link bidireccional** | ❌ FEATURE no apunta al Protocol | Actualizar FEATURE_DEVLOG_LIFECYCLE.md con pointer al PROTOCOL-DEV-001 |

### Outputs esperados (al cerrar la tarea)

1. **Reporte de auditoría** detallando diff FEATURE vs PROTOCOL vs Workflows vs Skills (qué falta)
2. **Protocol bumpeado** (v1.0.0 → v1.1.0) si hay gaps detectados
3. **3 Workflows DEV-001.001/.002/.003** creados siguiendo el template
4. **Skills faltantes** (006/007/008 si aplican) creadas O documentar por qué se eliminan
5. **Carpeta `05.Cards/dev/`** con las Cards aplicables del lifecycle
6. **FEATURE_DEVLOG_LIFECYCLE.md** actualizado con cross-link al Protocol
7. **INVENTARIO.md + REGISTRO_ACRONIMOS.md** actualizados con lo nuevo

═══════════════════════════════════════════════════════════════════════
CRITERIOS DE ACEPTACIÓN
═══════════════════════════════════════════════════════════════════════

La tarea VTS-007 tiene los CAs cargados en VTT como `criteriaIds`. Cada uno se reporta con:

```bash
curl -s -X PATCH "https://api.vttagent.com/api/tasks/VTS-007/criteria/<CRITERION_ID>" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"fulfillmentStatus": "met", "evidence": "<descripción + path/sha>", "fulfilledBy": "fe1b589c-7cf2-4779-82d4-b7ae536536ce"}'
```

Listar criterios cargados:
```bash
curl -s "https://api.vttagent.com/api/tasks/VTS-007/criteria" -H "Authorization: Bearer $TOKEN"
```

═══════════════════════════════════════════════════════════════════════
WORKFLOW VTT API — COMANDOS (resumen — detalle completo en OPERATIVO §7)
═══════════════════════════════════════════════════════════════════════

### Paso 0 — Auth (usa service-token, NO login — está rate-limited)

```bash
TOKEN=$(curl -s -X POST https://api.vttagent.com/api/auth/service-token \
  -H "Content-Type: application/json" \
  -d '{"userId":"fe1b589c-7cf2-4779-82d4-b7ae536536ce","serviceKey":"hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d"}' \
  | python -c "import sys,json; print(json.load(sys.stdin)['data']['token'])")
echo "$TOKEN" > .vtt_jwt   # cachear para no repetir auth
```

### Paso 1 — Mover a in_progress

```bash
TOKEN=$(cat .vtt_jwt)
curl -s -X PATCH "https://api.vttagent.com/api/tasks/VTS-007/status" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"statusId":"2a76888a-e595-4cfc-ac4c-a3ae5087ef56","changedBy":"fe1b589c-7cf2-4779-82d4-b7ae536536ce"}'
```

### Paso 2-N — Durante la tarea: devlog entries de decisiones

```bash
# Ejemplo: decisión técnica
curl -s -X POST "https://api.vttagent.com/api/tasks/VTS-007/devlog" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"categoryCode":"decision","title":"<desc>","description":"<contexto + por qué>","reportedBy":"fe1b589c-7cf2-4779-82d4-b7ae536536ce"}'
```

### Paso final — Subir attachments, reportar CAs, postear SKL-REPORT-01, mover a in_review

Ver OPERATIVO §7.6 (attachments), §7.5 (criteria), §7.7 (comment), §7.8 (in_review).

═══════════════════════════════════════════════════════════════════════
NORMATIVA DE REFERENCIA (Source of Truth para esta tarea)
═══════════════════════════════════════════════════════════════════════

| Documento | Por qué |
|---|---|
| `$VTT_SETUP/02.normativa/GUIA_AUTOR.md` | Tu manual de autor — DECIDIR nivel, naming, checklist |
| `$VTT_SETUP/02.normativa/00_REGISTRO_ACRONIMOS.md` | `DEV` ya está activo. Verificar antes de cualquier coding nuevo |
| `$VTT_SETUP/03.templates/normativa/_autoria/TEMPLATE_PROTOCOL.md` | Si bumpeás Protocol DEV-001 |
| `$VTT_SETUP/03.templates/normativa/_autoria/TEMPLATE_WORKFLOW.md` | Crear DEV-001.001/.002/.003 |
| `$VTT_SETUP/03.templates/normativa/_autoria/TEMPLATE_SKILL.md` | Si creás DEV-006/007/008 |
| `$VTT_SETUP/03.templates/normativa/_autoria/TEMPLATE_SCRIPT.py` | Si decidís crear script DEV |
| `$VTT_SETUP/03.templates/normativa/_autoria/TEMPLATE_CARD.md` | Crear Cards Nivel R del lifecycle |
| `$VTT_SETUP/02.normativa/01.Protocols/VTT.PROTOCOL-GOV-002_*.md` | Cómo editás (branch + commit + hook) |
| `$VTT_SETUP/02.normativa/01.Protocols/VTT.PROTOCOL-ASG-001_*.md` §5.3/§5.5/§5.6 | Para verificar integración con DEV-001 |
| `$VTT_SETUP/02.normativa/01.Protocols/VTT.PROTOCOL-DEV-001_*.md` | El Protocol existente a auditar |

═══════════════════════════════════════════════════════════════════════
REGLAS NIVEL 0 APLICABLES
═══════════════════════════════════════════════════════════════════════

| Regla | Por qué aplica a esta tarea |
|---|---|
| `RULE-AUTHOR-001` Antes de crear: leer GUIA_AUTOR + REGISTRO_ACRONIMOS | Toda creación de Protocol/Workflow/Skill/Script/Card |
| `RULE-TEMPLATE-001` Usar templates de `_autoria/` | NO inventar estructura |
| `RULE-SCRIPT-001` Si creás Script: invocación desde `$VTT_SETUP` | NUNCA copias locales |
| `RULE-GIT-004` Prohibido commit a main | Branch `agent/tw-ops/vtt-setup/audit-protocol-dev-001` (o similar) |
| `RULE-SEC-001` No postear datos sensibles en VTT | Comments/devlog/attachments sin IPs/credenciales/paths absolutos prod |
| `RULE-DOC-002` Cada archivo de código tiene `.LOGIC.md` | Si creás Script DEV → crear CODE_LOGIC.md |

Para más reglas: `python $VTT_SETUP/02.normativa/00.Rules/query_rules.py --simulate-task VTS-007`

═══════════════════════════════════════════════════════════════════════
PRIMER MENSAJE ESPERADO (al Coordinator)
═══════════════════════════════════════════════════════════════════════

Antes de empezar a editar, postear al Coordinator (en mi ventana de chat o como comment en VTS-007):

```
Listo. Soy TW-OPS. Lectura de gobernanza confirmada:
- README ✅
- INDEX ✅
- GUIA_AUTOR ✅

Pre-check OK (5/5 checks). $VTT_SETUP exportado y válido. JWT obtenido.

Tarea VTS-007 leída. Plan inicial:
1. <Tu plan en 3-5 bullets — qué vas a auditar primero, en qué orden,
   qué outputs esperás generar>

¿Procedo o ajustamos antes?
```

NO empezar a editar hasta que el Coordinator confirme.

═══════════════════════════════════════════════════════════════════════
ENTREGA (cuando termines)
═══════════════════════════════════════════════════════════════════════

1. Subir 4 attachments a VTS-007: BRIEF + ASSIGNMENT + devlog + code_logic (si creaste script)
2. Reportar CAs cumplidos con `PATCH /criteria/<id>`
3. Postear SKL-REPORT-01 como comment (formato en `VTT.SKILL-REPORT-001` v1.1)
4. Mover VTS-007 a `task_in_review` (statusId `1ec975a5-...`)
5. Avisar al Coordinator en chat: "VTS-007 lista para review"

El Coordinator revisará siguiendo las 5 verificaciones del INIT_TL_REVIEWER §FASE 3 antes de
aprobar y mover a `task_completed`.

═══════════════════════════════════════════════════════════════════════
DATOS CLAVE
═══════════════════════════════════════════════════════════════════════

- **Task ID:** VTS-007
- **Tu UUID:** `fe1b589c-7cf2-4779-82d4-b7ae536536ce`
- **Proyecto VTS ID:** `c6b513a1-d8ae-4344-b684-96d73721bfbf`
- **Phase ID (Fase 2):** `67045d1f-b0d7-4990-b96b-31cd8232cb32`
- **Sprint ID (S01):** `ae661ec0-0a83-44fa-84d3-23643799641a`
- **Delivery ID:** `0346fbf4-0137-4b2e-a850-adb5ec50f5fe`
- **API URL:** `https://api.vttagent.com`
- **Status UUIDs:** in_progress=`2a76888a-...` | in_review=`1ec975a5-...` | completed=`aa5ceb90-...` | on_hold=`c62eb334-...`
- **Priority UUIDs:** high=`1a617554-...` | medium=`d0b619ef-...` | low=`95f2e731-...`

— Coordinator (51af43cf-8939-4a6f-99ee-31238cfd6894 / coordinator@vtt-setup.vtt.ai)
