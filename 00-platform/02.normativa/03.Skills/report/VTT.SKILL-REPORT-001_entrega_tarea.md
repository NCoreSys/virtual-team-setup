# VTT.SKILL-REPORT-001 — Reporte de entrega de tarea (SKL-REPORT-01)

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-REPORT-001` |
| **Categoría** | REPORT |
| **Versión** | 1.1 |
| **Fecha** | 2026-05-22 |
| **Aplica a** | Todos los roles ejecutores (BE, DB, FE, QA, DO, DL, UX, AR, SA) |
| **Tokens estimados** | ~480 |
| **Cuándo se usa** | Al cerrar tarea — DESPUÉS de pasar review gate y mover a `task_in_review`. Es **precondición #2** del manifest v1.0 (PROTOCOL-MAN-001 §5.3) |
| **Reemplaza** | `SKL-REPORT-01_entrega-tarea.md` (legacy) |
| **Reglas aplicables** | I2 (reporte en carpeta del manifest), I3 (render obligatorio en pantalla) del template v2.1 |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `task_id` | string (MS-XXX) | sí | ID de la tarea |
| `task_name` | string | sí | Título humano de la tarea |
| `agent_uuid` | uuid | sí | UUID del agente que entrega |
| `phase` | string | sí | `04-development`, `03-design`, etc. |
| `sprint` | string | sí | `S01`, `S06-FIX-A`, etc. |
| `task_slug` | string | sí | Snake-case del título (para naming) |
| `report_data` | object | sí | Contenido del reporte (ver template abajo) |

---

## Precondición OBLIGATORIA

```bash
# Verificar review gate — NUNCA saltar este paso
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/review-gate" \
  -H "Authorization: Bearer $TOKEN" | python -m json.tool
```

Si `canProceedToReview = false`:

```bash
# Resolver cada blocker del devlog antes
curl -s -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/devlog/$ENTRY_ID/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"status": "resolved", "resolution": "Descripción de cómo se resolvió"}'
```

Solo cuando `canProceedToReview = true` → continuar con `VTT.SKILL-STATUS-002` y luego esta skill.

---

## Variables del entorno

```bash
$TOKEN
$VTT_BASE_URL              # http://77.42.88.106:3000
$AGENT_UUID
```

---

## Convención de paths (v1.1 — política I2 del template v2.1)

```
knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>_REPORT.md
```

> **El reporte vive en la MISMA carpeta que el JSON del manifest** (`<TASK_ID>.json` + `<TASK_ID>.manifest.md`). Esto permite que `VTT.SCRIPT-MAN-001` lo lea directamente y que el `git add` del Paso 12 capture los 3 archivos juntos.

### Ejemplos (v1.1)

- Memory Service: `knowledge/task-manifests/04-development/S01/MS-293_REPORT.md`
- VTT-tracking:   `knowledge/task-manifests/S06-FIX-A/VTT-705_REPORT.md`

### Path legacy (v1.0 — DEPRECADO)

`knowledge/agent-tasks/reports/<phase>/<sprint>/<TASK_ID>_REPORT.md` ya **NO se usa** desde v1.1. Si una tarea vieja tiene el reporte en ese path, dejarlo donde está (legacy), pero para tareas nuevas el path canónico es `knowledge/task-manifests/`.

---

## Template del reporte (sin truncar — archivo local)

> **Política:** todos los campos son obligatorios. Si no aplica, escribir literal `N/A` — nunca omitir sección. El parser de `VTT.SCRIPT-MAN-001` espera todas las secciones.

```markdown
## Entrega: <TASK_ID> — <TASK_NAME>

### Lo que se hizo:
<RESUMEN_TRABAJO>

### Código:
- `<ARCHIVO_1>` — <DESCRIPCION_1>
- `<ARCHIVO_2>` — <DESCRIPCION_2>

### Development Log:
`knowledge/development-log/<YYYY-MM-DD>_<TASK_ID>_<SLUG>.md`

### Code Logic:
- `knowledge/code-logic/<ARCHIVO_1>.LOGIC.md`
- `knowledge/code-logic/<ARCHIVO_2>.LOGIC.md`

### Criterios de aceptación:
| CA | Criterio | Resultado |
|----|----------|-----------|
| CA-1 | <CRITERIO_1> | ✅ / ❌ |
| CA-2 | <CRITERIO_2> | ✅ / ❌ |

### Devlog entries registrados en VTT:
| Categoría | Severidad | Título | Estado | Resolucion(descripcion) |
|-----------|-----------|--------|--------|--------|
| decision | low | <DECISION_TITULO> | resolved | resolucion |
| observation | low | <OBS_TITULO> | resolved |resolucion |

### Findings / Deuda técnica:
<FINDINGS o N/A>

### ADRs tomados:
<ADRS o N/A>

### TrackableItems creados o vinculados:
<TIS o N/A>

### Items detectados para trackeo (TL revisar):

| Tipo sugerido | Código sugerido | Descripción breve | ¿Retroactivo? | Urgencia |
|---|---|---|---|---|
| <tipo> | <código> | <descripción> | Sí / No | Alta / Media / Baja |

### Tareas derivadas generadas:
<TAREAS_DERIVADAS o N/A>

### Cómo verificar:
<PASOS_VERIFICACIÓN_O_QUERY>

### Notas:
<NOTAS o N/A>

### Review gate al entregar:
`canProceedToReview: true` — <N> entries totales, <N> resueltos, <N> warnings

### Commit:
`<COMMIT_TYPE> [<TASK_ID>]: <COMMIT_DESCRIPTION>`
SHA: `<COMMIT_SHA>`

### PR:
<PR_URL>
```

---

## Ejecución — flujo de 3 pasos

### Paso 1 — Generar reporte LOCAL completo (fuente de verdad)

```bash
# v1.1 — path canónico (misma carpeta que el JSON del manifest)
REPORT_PATH="knowledge/task-manifests/<PHASE>/<SPRINT>/<TASK_ID>_REPORT.md"

mkdir -p "$(dirname "$REPORT_PATH")"

# Generar el contenido siguiendo el template (16 secciones) y guardarlo
# El agente escribe el archivo con su tooling (Write tool, Edit, etc.).
# Política I2: el reporte vive en la MISMA carpeta del manifest JSON.
```

Este archivo contiene el reporte **COMPLETO sin truncar**. Es la fuente que `VTT.SCRIPT-MAN-001` lee para construir el manifest v1.0.

### Paso 1.bis — Render obligatorio en pantalla (POLÍTICA v1.1 — I3)

```
EL AGENTE DEBE MOSTRAR EL REPORTE COMO MARKDOWN RENDERIZADO EN PANTALLA.

NO ejecutar `cat $REPORT_PATH` — eso muestra texto plano sin formato.
```

**Cómo se cumple en Claude Code (y similar):**

- Embeber el contenido del reporte como **bloque markdown directo** en la respuesta del agente (entre triple-backtick si hace falta delimitar)
- El usuario debe poder leer: headings con jerarquía visual, tablas con bordes, listas con bullets, código en monospace
- Razón: el TL/PM revisa el reporte **visualmente** antes del PASS. Sin formato el reporte es ilegible.

**Anti-patrón (NO hacer):**

```bash
# ❌ MAL — muestra texto plano, el TL no puede revisar
cat "$REPORT_PATH"

# ❌ MAL — solo dice "está acá", el TL tiene que abrir el archivo manualmente
echo "Reporte en: $REPORT_PATH"
```

**Patrón correcto:**

> El agente, después de escribir el archivo `.md`, **escribe el contenido completo del reporte como markdown directo en su próximo mensaje al usuario**. El renderer del cliente (Claude Code, IDE plugin, etc.) lo muestra formateado.

### Paso 2 — Postear extracto como comment en VTT

VTT limita comments a **5000 chars**. El reporte completo suele exceder. Postear las primeras 8-10 líneas + link al archivo.

```bash
EXTRACTO=$(head -20 "$REPORT_PATH")

curl -s -X POST "$VTT_BASE_URL/api/tasks/$TASK_ID/comments" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "$(python -c "
import json
extracto = '''$EXTRACTO'''
msg = extracto + '\n\n**Reporte completo:** $REPORT_PATH'
print(json.dumps({'message': msg, 'userId': '$AGENT_UUID'}))
")"
```

**Capturar el `comment_id`** del response — se usa en `delivery.vtt_report_comment_id` del manifest v1.0.

```bash
REPORT_COMMENT_ID=$(curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/comments" -H "Authorization: Bearer $TOKEN" \
  | python -c "
import sys, json
cs = json.load(sys.stdin).get('data', [])
last = cs[-1] if cs else None
print(last.get('id', '') if last else '')
")
echo "REPORT_COMMENT_ID=$REPORT_COMMENT_ID"
```

### Paso 3 — `VTT.SCRIPT-MAN-001` lee el archivo (no el comment)

El script de manifest hace:

```python
# v1.1 — path canónico
report_path = f"knowledge/task-manifests/{phase}/{sprint}/{TASK_ID}_REPORT.md"
with open(report_path, 'r', encoding='utf-8') as f:
    content = f.read()
# Parsear secciones por regex de headings (## ...)
```

> **Por eso el reporte LOCAL es la fuente de verdad — no el comment.**

El agente invoca el script con el flag `--report-path` apuntando al nuevo path:

```bash
python $VTT_SETUP/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py \
  --task-id MS-XXX \
  --version 1.0 \
  --agent-uuid $AGENT_UUID \
  --report-path knowledge/task-manifests/$PHASE/$SPRINT/MS-XXX_REPORT.md \
  --phase $PHASE \
  --sprint $SPRINT \
  --upload
```

---

## Validación

```bash
# Check 1: archivo existe en el path v1.1 canónico
REPORT_PATH="knowledge/task-manifests/<PHASE>/<SPRINT>/<TASK_ID>_REPORT.md"
ls "$REPORT_PATH"
# Esperado: existe

# Check 1.bis (v1.1): no quedó por error en el path legacy
test ! -f "knowledge/agent-tasks/reports/<PHASE>/<SPRINT>/<TASK_ID>_REPORT.md"
# Esperado: el archivo NO existe en path legacy (si existe, fue a la ubicación vieja por error)

# Check 2: comment posteado
curl -s "$VTT_BASE_URL/api/tasks/$TASK_ID/comments" -H "Authorization: Bearer $TOKEN" \
  | python -c "
import sys, json
cs = json.load(sys.stdin).get('data', [])
report_comments = [c for c in cs if 'Entrega:' in (c.get('message') or '')]
print(f'report_comments: {len(report_comments)}')
"
# Esperado: >= 1

# Check 3: todas las secciones del template están en el reporte
SECTIONS="Lo que se hizo|Código|Development Log|Code Logic|Criterios de aceptación|Devlog entries|Findings|ADRs|TrackableItems|Items detectados|Tareas derivadas|Cómo verificar|Notas|Review gate|Commit|PR"
grep -E "^### ($SECTIONS)" "$REPORT_PATH" | wc -l
# Esperado: 16 (todas las secciones)

# Check 4 (v1.1 — I3): el agente mostró el reporte renderizado en su respuesta
# Validación manual: el TL/PM debe poder LEER el reporte sin abrir el archivo
# El agente debe haber embebido el contenido como markdown directo en su mensaje
```

---

## Reglas

| # | Regla |
|---|---|
| R1 | Todos los campos son obligatorios — usar `N/A` cuando no aplica |
| R2 | El reporte completo va SIEMPRE en archivo local — el comment es solo extracto |
| R3 | Si el comment excede 5000 chars → HTTP 400. Por eso el extracto |
| R4 | El archivo se commitea al PR (Paso 12 del workflow del agente) |
| R5 | `VTT.SCRIPT-MAN-001` espera las 16 secciones — no inventes ni omitas |
| **R6 (v1.1 — I2)** | **El reporte vive en `knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>_REPORT.md`** (misma carpeta que el JSON del manifest). Path legacy `knowledge/agent-tasks/reports/` está DEPRECADO. |
| **R7 (v1.1 — I3)** | **El agente DEBE renderizar el reporte en pantalla como markdown formateado** (NO `cat`). El TL/PM revisa visualmente antes del PASS. |

---

## Error común

| Error | Causa | Solución |
|---|---|---|
| Reporte incompleto | Saltar secciones | Usar template completo, `N/A` donde no aplique |
| Comment HTTP 400 | Excede 5000 chars | Usar extracto (primeras 8-10 líneas) |
| Manifest fail al parsear | Falta heading exacto | Respetar `### <Nombre>` literal del template |
| Reporte fuera del path estándar | Ruta inventada | Usar `knowledge/task-manifests/<phase>/<sprint>/...` (v1.1) |
| Reporte en path legacy `agent-tasks/reports/` | Convención v1.0 | Migrar a `task-manifests/` — el manifest v1.0 lo va a buscar ahí desde v1.1 |
| TL no puede revisar el reporte | Agente usó `cat` | Re-mostrar el reporte como markdown formateado en pantalla (R7) |
| `REPORT_COMMENT_ID` perdido | No capturó | Hacer GET después de POST como en §Paso 2 |

---

## Skills invocadas

- `VTT.SKILL-AUTH-001` — `$TOKEN`
- `VTT.SKILL-COMMENT-001` — para postear el extracto

---

## Skills que invocan ESTA

- Workflow del agente al cerrar tarea (paso final pre-manifest)
- `VTT.WORKFLOW-MAN-001.003 §3` (parser del report → manifest)

---

## Cuándo NO usar esta Skill

- **Si el review gate falla** — resolver entries pendientes primero
- **Si la tarea es del PJM (reporte ejecutivo)** — usar `VTT.SKILL-REPORT-002` en su lugar

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-19 | Versión inicial. Migración de `SKL-REPORT-01_entrega-tarea.md`. **Categoría cambió de `REPORT` a categoría VTT formal**. Mantiene las 16 secciones obligatorias. Cross-ref con `VTT.SCRIPT-MAN-001` (parser) y `00_CONVENCIONES_FILESYSTEM.md` (path estándar). Documentación explícita del flujo 3 pasos (archivo + extracto + parser). |
| 1.1 | 2026-05-22 | **OLA 1 cierre sub-sistema MSG — políticas I2/I3 del template v2.1.** Cambios: (1) **R6 nueva** — path canónico del reporte cambia de `knowledge/agent-tasks/reports/<phase>/<sprint>/` a `knowledge/task-manifests/<phase>/<sprint>/` (misma carpeta que el JSON del manifest — política I2). El path legacy queda deprecado. (2) **R7 nueva** — render obligatorio en pantalla (NO `cat`): el agente DEBE mostrar el reporte como markdown formateado para que el TL/PM lo revise visualmente (política I3). Agregado Paso 1.bis con anti-patrones (`cat`, `echo`) y patrón correcto. (3) Cross-ref actualizado con template v2.1, SKILL-PRECHECK-001, RULE-SCRIPT-001, RULE-TEMPLATE-001. Origen: drift MS-290 vs MS-333. |
