# TEMPLATE: Mensaje de Asignación de Tarea

| Campo | Valor |
|---|---|
| **Versión** | 2.2 |
| **Fecha** | 2026-05-22 |
| **Aplica a** | TL Asignador (lo genera) → Agente ejecutor (lo recibe en VTT como comment) |
| **Reemplaza** | v2.1 (sin Paso 0 Pre-check obligatorio) |
| **Reglas aplicables** | `RULE-SCRIPT-001` (path canónico), `RULE-TEMPLATE-001` (lectura formal del template), `RULE-AGENT-001` (worktree dedicado) |
| **Skills referenciadas** | `VTT.SKILL-PRECHECK-001` (Paso 0), `VTT.SKILL-REPORT-001` (Paso 4 al cerrar) |

---

## Cómo usar este template

1. Copiar el bloque ` ``` ` de abajo
2. Reemplazar todos los placeholders `{{VAR}}` con los datos reales de la tarea
3. **Elegir UNA** de las 2 variantes de §Working Directory (con worktree o sin worktree) y borrar la otra
4. Pegar como comment en VTT al asignar al agente

> El mensaje **NO duplica instrucciones** de Protocols/Workflows. Solo apunta al setup. Si el agente necesita detalle → abre los archivos del setup referenciados.

---

```markdown
Hola {{ROL_NOMBRE}},

Tienes tarea nueva asignada: **{{TASK_ID}}** ({{TITULO}}).
Sprint: {{SPRINT}} | Phase: {{PHASE}}

═══════════════════════════════════════════════════════════════════════
WORKING DIRECTORY
═══════════════════════════════════════════════════════════════════════

<!-- VARIANTE A — Proyecto CON worktrees por rol (.vtt/worktrees/ existe) -->
<!-- Borrar esta variante si el proyecto NO usa worktrees -->

Tu cwd fijo (worktree por rol): `{{PROJECT_ROOT}}/.vtt/worktrees/{{REPO}}-{{ROL_LOWER}}/`

Reglas:
- Trabajas SIEMPRE en este directorio (todas tus tareas, hoy y mañana)
- Cada tarea = nueva branch dentro del MISMO worktree
- NUNCA hagas `git checkout` en el clon base
- NUNCA hagas cd a otro worktree de otro rol
- Tu `.env` y `node_modules` viven aquí (no en el clon base)

Workspace VSCode dedicado:
`{{PROJECT_ROOT}}/.vtt/workspaces/{{REPO}}-{{ROL_LOWER}}.code-workspace`

Execution manifest (lee ANTES de empezar):
`{{PROJECT_ROOT}}/.vtt/manifests/{{TASK_ID}}.execution.json`

Puerto npm asignado (si aplica): `PORT={{PORT}}`

<!-- VARIANTE B — Proyecto SIN worktrees (clon directo) -->
<!-- Borrar esta variante si el proyecto SÍ usa worktrees -->

Tu cwd: `{{PROJECT_ROOT}}/`

Reglas:
- Un solo working tree del proyecto (no hay multi-rol simultáneo)
- Cada tarea = nueva branch desde main
- No hay execution_manifest por tarea (solo aplica a proyectos con worktrees)

<!-- FIN — fin de las 2 variantes -->

Paso 0-A — **PRE-CHECK OBLIGATORIO** (POLÍTICA v2.2 — `VTT.SKILL-PRECHECK-001`):

Antes de tocar nada, validar el entorno. Si CUALQUIER check falla → DETENER la tarea y reportar al TL.

```bash
# Check 1 — $VTT_SETUP exportado y existe
test -n "$VTT_SETUP" && test -d "$VTT_SETUP/02.normativa" || { echo "ABORT: \$VTT_SETUP inválido"; exit 2; }

# Check 2 — Scripts canónicos existen en $VTT_SETUP (al menos MAN-001)
test -f "$VTT_SETUP/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py" \
  || { echo "ABORT: SCRIPT-MAN-001 no existe en \$VTT_SETUP — actualizar virtual-teams-setup"; exit 2; }

# Check 3 — NO copias locales prohibidas en worktree (RULE-SCRIPT-001)
ROGUE=$(find . -maxdepth 4 -type f \( -name "VTT.SCRIPT-MAN-*.py" -o -name "VTT.SCRIPT-EXM-*.py" -o -name "VTT.SCRIPT-MSG-*.py" \) 2>/dev/null)
test -z "$ROGUE" || { echo "ABORT: copias locales detectadas (RULE-SCRIPT-001):\n$ROGUE"; exit 2; }

# Check 4 — $TOKEN responde 200 (validar al final, después de SKILL-AUTH-001)

echo "✅ Pre-check OK — entorno listo"
```

> **Política:** si el pre-check falla, NO continuar. Postear comment en la tarea VTT con el error y dejar la tarea en `task_on_hold` o `task_pending`. Ver `$VTT_SETUP/02.normativa/03.Skills/precheck/VTT.SKILL-PRECHECK-001_validar_entorno_inicio_tarea.md` para los 5 checks completos.

Paso 0-B — Comandos git al arrancar la tarea:
```bash
cd {{CWD_DEL_AGENTE}}      # path que corresponde según variante elegida arriba
git status                  # debe estar limpio
git fetch origin
git checkout main && git pull origin main
git checkout -b feature/{{TASK_ID}} origin/main
```

═══════════════════════════════════════════════════════════════════════
NORMATIVA DE REFERENCIA (Source of Truth)
═══════════════════════════════════════════════════════════════════════

Variable de entorno: `$VTT_SETUP={{VTT_SETUP_PATH}}`

Lectura obligatoria (en orden) — abre cada archivo SOLO cuando lo necesites:

1. Tu OPERATIVO local:
   `.claude/agents/OPERATIVO_{{ROL}}_{{PROYECTO}}.md`

2. ASSIGNMENT y BRIEF de la tarea (locales):
   - `knowledge/agent-tasks/assignments/{{PHASE}}/{{SPRINT}}/ASSIGNMENT_{{TASK_ID}}_{{SLUG}}.md`
   - `knowledge/agent-tasks/briefs/{{PHASE}}/{{SPRINT}}/BRIEF_{{TASK_ID}}_{{SLUG}}.md`

3. Workflow del agente (al cerrar la tarea — genera manifest v1.0):
   `$VTT_SETUP/02.normativa/02.Workflows/VTT.WORKFLOW-MAN-001.003_generar_task_manifest_v10.md`

4. Convenciones de filesystem (si dudas dónde dejar entregables):
   `$VTT_SETUP/02.normativa/00_CONVENCIONES_FILESYSTEM.md`

5. Convenciones de branch Git:
   `$VTT_SETUP/02.normativa/00_REGISTRO_ACRONIMOS.md` §3.bis

Consulta bajo demanda (solo si encuentras algo no cubierto):
- `$VTT_SETUP/02.normativa/01.Protocols/VTT.PROTOCOL-MAN-001_gobernanza_manifest.md` (gobernanza completa del manifest)
- `$VTT_SETUP/02.normativa/01.Protocols/VTT.PROTOCOL-ASG-001_ciclo_asignacion_tarea.md` (ciclo end-to-end)
- `$VTT_SETUP/02.normativa/03.Skills/manifest/VTT.SKILL-MAN-001_task_manifest.md` (esquema v1.2 completo)

═══════════════════════════════════════════════════════════════════════
CRITERIOS DE ACEPTACIÓN
═══════════════════════════════════════════════════════════════════════

{{LISTA_CAs}}

(Cada CA con su `id` UUID — el agente reporta con `PATCH /api/tasks/{{TASK_ID}}/criteria/<id>` `{status:"met", evidence:"..."}`)

═══════════════════════════════════════════════════════════════════════
COMANDOS VTT — JWT, status, devlog
═══════════════════════════════════════════════════════════════════════

Paso 0 — Obtener JWT:
```bash
TOKEN=$(python -c "
import urllib.request, json, sys
req = urllib.request.Request(
    'http://77.42.88.106:3000/api/auth/service-token',
    data=json.dumps({'userId': '{{AGENT_UUID}}', 'serviceKey': '{{SERVICE_KEY}}'}).encode(),
    headers={'Content-Type': 'application/json'}, method='POST')
with urllib.request.urlopen(req) as r:
    sys.stdout.write(json.loads(r.read())['data']['token'])
")
export TOKEN
```

Paso 1 — Mover a in_progress:
```bash
curl -s -X PATCH http://77.42.88.106:3000/api/tasks/{{TASK_ID}}/status \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"statusId": "2a76888a-e595-4cfc-ac4c-a3ae5087ef56", "changedBy": "{{AGENT_UUID}}"}'
```

Durante la tarea — Registrar devlog entries (1 entry):
```bash
# Endpoint SINGULAR /devlog para 1 entry — payload directo SIN wrapper
curl -s -X POST "http://77.42.88.106:3000/api/tasks/{{TASK_ID}}/devlog" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"categoryCode": "decision", "title": "<descripcion>", "description": "<contexto del por qué — OBLIGATORIO>", "severity": "low", "reportedBy": "{{AGENT_UUID}}"}'

# Para varias entries en batch usar /devlog-entries (plural) CON wrapper {"entries":[...]}
```

> Ver `VTT.SKILL-DEV-001` (decision) y `VTT.SKILL-DEV-002` (observation) — `description` es obligatorio (caso MS-333: entries sin description tuvieron que ser borradas).

Al completar — Reportar CAs:
```bash
curl -s -X PATCH "http://77.42.88.106:3000/api/tasks/{{TASK_ID}}/criteria/<CRITERIA_ID>" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"status": "met", "evidence": "<evidencia concreta>"}'
```

═══════════════════════════════════════════════════════════════════════
ENTREGABLES AL CERRAR (en este orden — AL FINAL)
═══════════════════════════════════════════════════════════════════════

1. Verifica review gate `canProceedToReview: true`
2. Sube devlog: `POST /attachments fileType=devlog`
3. Sube code_logic: `POST /attachments fileType=code_logic` (uno por archivo de código)
4. **Lee la skill VTT.SKILL-REPORT-001 ANTES de generar el reporte** (POLÍTICA v2.1 — I1):
   `$VTT_SETUP/02.normativa/03.Skills/report/VTT.SKILL-REPORT-001_entrega_tarea.md`
   El reporte sigue la estructura formal de esa skill (16 secciones obligatorias).
5. **Genera el reporte local en la MISMA carpeta del manifest** (POLÍTICA v2.1 — I2):
   `knowledge/task-manifests/{{PHASE}}/{{SPRINT}}/{{TASK_ID}}_REPORT.md`
   > **Ubicación obligatoria:** la misma carpeta donde `VTT.SCRIPT-MAN-001` escribe el JSON + manifest.md. NO usar `knowledge/agent-tasks/reports/...` (path deprecado en v2.1).
6. **Muestra el reporte RENDERIZADO en pantalla** (POLÍTICA v2.1 — I3):
   El agente DEBE renderizar el markdown como bloque visualizable (NO ejecutar `cat`).
   Razón: el TL/PM revisa el reporte visualmente antes del PASS — headings, tablas y listas formateadas. `cat` muestra texto plano sin formato.
7. Postea comment SKL-REPORT-01 (extracto del reporte) → guarda el `comment_id`
8. Mueve status a `task_in_review`
9. Crea PR en GitHub
10. **Genera Task Manifest v1.0** con script oficial (path canónico RULE-SCRIPT-001):
    ```bash
    python $VTT_SETUP/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py \
      --task-id {{TASK_ID}} \
      --version 1.0 \
      --agent-uuid {{AGENT_UUID}} \
      --report-path knowledge/task-manifests/{{PHASE}}/{{SPRINT}}/{{TASK_ID}}_REPORT.md \
      --phase {{PHASE}} \
      --sprint {{SPRINT}} \
      --upload
    ```
    > **PROHIBIDO** invocar copias locales del script en `scripts/manifest/` del worktree (RULE-SCRIPT-001 v1.0).
11. **Commitea el manifest al MISMO PR de la tarea** (Paso 12 obligatorio):
    ```bash
    git add knowledge/task-manifests/{{PHASE}}/{{SPRINT}}/{{TASK_ID}}.json
    git add knowledge/task-manifests/{{PHASE}}/{{SPRINT}}/{{TASK_ID}}.manifest.md
    git add knowledge/task-manifests/{{PHASE}}/{{SPRINT}}/{{TASK_ID}}_REPORT.md
    git commit -m "[{{TASK_ID}}] manifest v1.0 — agent delivery"
    git push origin feature/{{TASK_ID}}
    ```

═══════════════════════════════════════════════════════════════════════
DATOS DEL SISTEMA
═══════════════════════════════════════════════════════════════════════

- **Tu user ID:** `{{AGENT_UUID}}`
- **Tu rol:** {{ROL_NOMBRE}} ({{ROL}})
- **Status in_progress:** `2a76888a-e595-4cfc-ac4c-a3ae5087ef56`
- **Status in_review:** `1ec975a5-7581-4a1a-ab8f-51b1a7ef868d`
- **Backend VTT:** http://77.42.88.106:3000
- **Service Key:** {{SERVICE_KEY}}
- **Project root:** {{PROJECT_ROOT}}
- **$VTT_SETUP:** {{VTT_SETUP_PATH}}

═══════════════════════════════════════════════════════════════════════
QUE PASA DESPUES (FYI — no requiere acción del agente)
═══════════════════════════════════════════════════════════════════════

Una vez tu v1.0 esté subido + PR creado con el manifest commiteado:

1. TL revisa tu PR en GitHub (incluye el manifest v1.0 commiteado)
2. TL aprueba PR del agente → merge a main
3. TL ejecuta script v1.5 (`--version 1.5`) que SOBREESCRIBE tu manifest local con enriquecimiento (review.tl_review + dynamic_model_actions)
4. TL crea branch `tl/{{TASK_ID}}-close` con PR a main (FASE 4.5 del PROTOCOL-ASG-001)
5. PM aprueba PR del TL

Tu manifest v1.0 queda preservado como historial:
- En VTT como attachment original
- En git como commit en la branch `feature/{{TASK_ID}}` (ya mergeada)

═══════════════════════════════════════════════════════════════════════

Estimación: {{ESTIM_HORAS}}h

Reportar al TL al completar con el formato del ASSIGNMENT §REPORTE.

Atentamente,
Tech Lead {{PROYECTO_CORTO}}
```

---

## Placeholders — referencia rápida

| Placeholder | Ejemplo | Origen |
|---|---|---|
| `{{ROL_NOMBRE}}` | Backend Engineer | Operativo del agente |
| `{{ROL}}` | BE | Operativo del agente |
| `{{ROL_LOWER}}` | be | Lowercase del rol |
| `{{TASK_ID}}` | MS-293 | VTT |
| `{{TITULO}}` | [4.3.14] Error Handling | VTT task.title |
| `{{SPRINT}}` | S01 | VTT task.sprint.name |
| `{{PHASE}}` | 04-development | Convención del proyecto |
| `{{SLUG}}` | error-handling | Snake-case del título |
| `{{PROJECT_ROOT}}` | c:/.../memory-service-project | Path del repo de la tarea |
| `{{REPO}}` | backend | Nombre del repo (si el proyecto es multi-repo) |
| `{{CWD_DEL_AGENTE}}` | `{{PROJECT_ROOT}}/.vtt/worktrees/backend-be/` (variante A) o `{{PROJECT_ROOT}}` (variante B) | Computado |
| `{{VTT_SETUP_PATH}}` | c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform | Source of Truth |
| `{{AGENT_UUID}}` | ebbe3cee-abed-4b3b-860d-0a81f632b08a | VTT user.id |
| `{{SERVICE_KEY}}` | hBCGEKm41BijI6jJ... | Configuración del proyecto |
| `{{PORT}}` | 3013 | Asignado por rol (solo si proyecto usa worktrees) |
| `{{PROYECTO}}` | MEMORY-SERVICE | Nombre del proyecto en mayúsculas |
| `{{PROYECTO_CORTO}}` | Memory Service | Display name |
| `{{ESTIM_HORAS}}` | 4 | VTT task.estimatedHours |
| `{{LISTA_CAs}}` | Tabla `- CA-XX (uuid): título` | Generada de VTT |

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | (legacy) | Versión original. Paths hardcodeados. Sin commit del manifest al PR. Sin referencia al setup. |
| 2.0 | 2026-05-18 | **Refactor completo.** Variante única con sección Working Directory condicional (A=worktrees, B=sin worktrees). Apunta a `$VTT_SETUP` para Source of Truth (no duplica Protocols). Paso 12 nuevo: commit del manifest al PR. Sección "Qué pasa después" explica FASE 4.5 del TL. Comando explícito de `gen_task_manifest.py` con flags correctos. Referencia `00_CONVENCIONES_FILESYSTEM.md` y `00_REGISTRO_ACRONIMOS.md §3.bis`. |
| 2.1 | 2026-05-22 | **OLA 1 cierre del sub-sistema MSG.** Fix de bugs heredados + 3 instrucciones del PM para entrega: **(I1)** El agente debe LEER `VTT.SKILL-REPORT-001` antes de generar el reporte (Paso 4 explícito). **(I2)** Ubicación obligatoria del reporte = misma carpeta del JSON del manifest (`knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>_REPORT.md`) — NO `knowledge/agent-tasks/reports/...` (deprecado). **(I3)** El agente DEBE renderizar el reporte en pantalla, prohibido `cat` (Paso 6). **Fixes heredados de v2.0:** (a) endpoint devlog era `/devlog-entries` sin wrapper → causaba HTTP 400 (caso MS-333). Ahora `/devlog` singular para 1 entry con `description` obligatorio. (b) `description` se documenta como obligatorio. (c) Reportes ahora se commitean al PR con el manifest (paso 11). (d) Aplica `RULE-SCRIPT-001` (path canónico, prohibido copias locales) y `RULE-TEMPLATE-001`. Origen: drift entre `MENSAJE_MS-290.md` y `MENSAJE_MS-333.md`. |
| 2.2 | 2026-05-22 | **Paso 0 Pre-check obligatorio.** Antes de tocar código, el agente DEBE ejecutar 4 checks (VTT_SETUP existe, scripts canónicos presentes, NO copias locales prohibidas, TOKEN válido). Si falla → tarea en hold + comment al TL. Reemplaza el Paso 0 anterior (que era solo `git`). Nuevo Paso 0-A (pre-check) + Paso 0-B (git). Origen: validación end-to-end del refactor MSG-001 + skill VTT.SKILL-PRECHECK-001 creada. Asegura cumplimiento operativo de RULE-SCRIPT-001 desde el primer minuto del agente. |
