# CODE LOGIC — VTT.SCRIPT-MAN-001_gen_task_manifest.py

| Campo | Valor |
|---|---|
| **Archivo** | `00-platform/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py` |
| **Versión actual** | v1.5 (2026-06-01) |
| **Últimas tareas relacionadas** | VTS-001 (regex `:`), VTS-002 (items_detected hardcoded), VTS-003 (how_to_verify parser limitado) |
| **Origen** | VTT-870 + review de v1.4 por TL Reviewer VTT (VTS-002 / VTS-003) |

---

## 1. Propósito

Generar Task Manifest schema v1.2 desde un REPORT markdown del agente, y subirlo a VTT como attachment `fileType=manifest`. Cubre dos versiones del manifest:

- **v1.0** — generado por el agente al cerrar su tarea (campos del agente)
- **v1.5** — generado por el TL al aprobar (agrega `dynamic_actions`, `evidences_added`, related_to consolidado)

---

## 2. Componentes clave del flujo

### 2.1 `parse_report_sections(content)` — línea ~200

Función central que extrae las secciones narrativas del REPORT markdown y las convierte a un dict.

**Mecanismo:**
1. Itera sobre `REPORT_SECTIONS` (dict con `{section_key: [aliases]}` — ej. `findings: ["Findings", "Hallazgos", "Tech Findings"]`)
2. Para cada section_key, intenta cada alias
3. Construye un regex que matchea `## <alias>` o `### <alias>` y captura hasta el siguiente heading
4. Si matchea con el pattern markdown → usa esa captura
5. Fallback: pattern de línea no-markdown `Alias:` con `[A-Z][a-zA-Z\s]+:` como delimitador

**Bug VTT-870 (resuelto en v1.4):**

El regex original (v1.3 y anteriores) era:
```python
pattern_md = rf"(?:^|\n)#{{1,3}}\s+{re.escape(alias)}\s*\n(.*?)(?=\n#{{1,3}}\s+|\Z)"
```

El `\s*\n` final exigía que tras el alias hubiera espacios opcionales y un newline. NO aceptaba `:` final.

Resultado: heading como `### Findings:` (con dos puntos finales) NO matcheaba. La sección quedaba como `None`. En el JSON final caía a `"N/A"` o `[]`.

**Impacto:** 6 de 12 secciones del REPORT se perdían silenciosamente:
- `findings`
- `adrs`
- `derived_tasks`
- `notes`
- `items_detected`
- `how_to_verify`

**Fix v1.4 aplicado:**
```python
pattern_md = rf"(?:^|\n)#{{1,3}}\s+{re.escape(alias)}\s*:?\s*\n(.*?)(?=\n#{{1,3}}\s+|\Z)"
```

Se agregó `:?` opcional antes del `\s*\n`. Acepta:
- `### Findings\n...` (sin `:`)
- `### Findings:\n...` (con `:`)
- `### Findings :\n...` (con espacio antes del `:`)

El lookahead de corte (`\n#{1,3}\s+`) NO se tocó — sigue cortando la sección en el siguiente heading. Probado con REPORT mixto (8 secciones, 4 con `:` y 4 sin `:`) — todas parsean OK.

El pattern de fallback (`pattern_line`) también se homogeneizó a `\s*:?\s*\n` para consistencia.

### 2.2 `build_v10(args)` — manifest v1.0 del agente

Construye el JSON v1.0 con:
- Metadata de la tarea (id, title, status, sprint, phase)
- Indexes calculados (deliverables, devlog_summary, criteria_results)
- Devlog entries parseados del REPORT
- Trackable items declarados
- **Secciones narrativas (extraídas con `parse_report_sections`):** what_was_done, findings, adrs, derived_tasks, notes, items_detected, how_to_verify, deuda_tecnica, etc.

Si `parse_report_sections` devuelve `None` para una sección, el manifest cae al default (`"N/A"` o `[]` según el campo).

**Bug VTS-002 (resuelto en v1.5):** `items_detected_for_tl_review` estaba **hardcoded a `[]`** en línea ~509:
```python
"items_detected_for_tl_review": [],  # IGNORABA report_sections["items_detected"]
```
Aunque el REPORT incluyera contenido bajo `### Items detectados para trackeo`, NO se reflejaba en el manifest. Fix v1.5: cambiar a `_extract_list_items(report_sections.get("items_detected"))`.

**Bug VTS-003 (resuelto en v1.5):** `how_to_verify` usaba un **parser limitado** que solo capturaba líneas con viñetas `-/*/+`:
```python
"how_to_verify": [l.strip().lstrip("-*+ ") for l in (...).split("\n") if l.strip().startswith(("-", "*", "+"))],
```
Si los pasos del REPORT eran **numerados** (`1.`, `2)`) o **párrafos sin viñeta**, se perdían. Fix v1.5: refactor a helper `_extract_list_items` que acepta los 3 formatos.

### 2.2.bis `_extract_list_items(section_text)` — helper v1.5

Nuevo helper introducido en v1.5 para centralizar la extracción de listas desde secciones narrativas. Reemplaza el parser inline limitado.

**Acepta:**
- Líneas con viñeta: `- texto`, `* texto`, `+ texto`
- Líneas numeradas: `1. texto`, `2) texto`, `1) texto`
- Párrafos sin viñeta (líneas con texto que no son headings)

**Excluye:**
- Headings markdown (`#`, `##`, `###`)
- Líneas vacías
- Líneas con solo espacios

**Idempotente:** aplicado a `None` o `""` devuelve `[]` sin error.

**Tests:** 13/13 casos cubiertos (None/empty/whitespace/bullets/numerados/párrafos/mix/headings/líneas vacías intercaladas).

**Candidatos a usar el helper en el futuro:** además de `items_detected` y `how_to_verify`, también podrían refactorizarse a usar este helper: `findings`, `adrs`, `derived_tasks`, `deuda_tecnica`, `tis`. Queda como mejora derivada — por ahora solo se aplica donde había bug confirmado para minimizar superficie de cambio.

### 2.3 `build_v15(args, v10_doc, dynamic_actions)` — manifest v1.5 del TL

Toma el v1.0 existente y lo enriquece con:
- `dynamic_actions.new_tis_created` (TIs nuevos del TL)
- `dynamic_actions.evidences_added` (TIs evidenciados — nuevos o existentes)
- `related_to` consolidado desde ambas fuentes con dedup (fix v1.3 bug #8)
- `tech_debt_count` recalculado

### 2.4 `save_local(doc, task_id, phase, sprint)` y `upload_to_vtt(...)`

- `save_local` escribe a `knowledge/task-manifests/<phase>/<sprint>/<TASK_ID>.{json,manifest.md}` (sobrescribe el mismo par cada vez — v1.2 fix)
- `upload_to_vtt` hace multipart upload a `POST /api/tasks/:id/attachments` con `fileType=manifest` y `uploadedById`

---

## 3. Dependencias importantes

| Dependencia | Por qué |
|---|---|
| `re` (regex) | Parseo de secciones del REPORT (función crítica afectada por bug VTT-870) |
| `json` | Serialización del manifest |
| `urllib.request` | HTTP a VTT API |
| `pathlib` | Manejo de paths |
| `argparse` | CLI estándar (modo agente vs modo TL: `--version 1.0` o `--version 1.5`) |
| VTT API endpoints | `POST /api/tasks/:id/attachments` (multipart), `GET /api/tasks/:id` (lectura metadata) |
| Variables de entorno | `$TOKEN` (JWT), `$VTT_BASE_URL` (host) |

---

## 4. Decisiones de diseño históricas

| ID | Decisión | Versión |
|---|---|---|
| D-MAN-001 | El manifest se sobrescribe (`save_local`) — historial vive en VTT attachments + git log del PR | v1.2 |
| D-MAN-002 | Sin sufijo `.v1.5` en el nombre del archivo — la versión es metadata interna del JSON | v1.2 |
| D-MAN-003 | `build_v15` consolida `related_to` desde 2 fuentes con dedup (no solo `new_tis_created`) | v1.3 |
| D-MAN-004 | `parse_report_sections` acepta heading con `:` opcional final (regex `:?`) | v1.4 |
| D-MAN-005 | `items_detected_for_tl_review` lee del REPORT (antes `[]` hardcoded) | v1.5 |
| D-MAN-006 | `how_to_verify` usa parser tolerante (bullets + numerados + párrafos) | v1.5 |
| D-MAN-007 | Helper `_extract_list_items` reusable — centraliza la lógica de extracción de listas | v1.5 |

---

## 5. Pruebas realizadas para v1.4

### 5.1 Test inline (REPORT mixto con y sin `:`)

REPORT de prueba con 8 secciones:
- `## What was done` (sin `:`)
- `## Findings:` (con `:`)
- `### Deuda tecnica:` (con `:`)
- `### Items detected for TL:` (con `:`)
- `## Notes` (sin `:`)
- `### How to verify:` (con `:`)
- `## ADRs:` (con `:`)
- `## Derived tasks:` (con `:`)

**Resultado:** 8/8 secciones parsean correctamente. Cada una corta limpiamente en el siguiente heading sin contaminación.

### 5.2 Regresión

El pattern v1.4 (`:?` opcional) es **estrictamente más permisivo** que el v1.3. Cualquier heading que parseaba en v1.3 (sin `:`) sigue parseando en v1.4. Cero regresión.

---

## 6. Historial de cambios

| Versión | Fecha | Cambio principal |
|---|---|---|
| 1.0 | 2026-05-17 | Versión inicial. Parseo de REPORT + generación manifest v1.0 y v1.5 + upload a VTT. |
| 1.1 | 2026-05-18 | 7 bugs corregidos detectados en producción VTT-721 (parse_deliverables, devlog_entries[].category, indexes en v1.5, task.sprint/stage shape, comment.message vs body, multipart uploadedById, endpoint attachment individual). |
| 1.2 | 2026-05-18 | save_local sobrescribe el mismo par (`<TASK_ID>.{json,manifest.md}`) — sin sufijo .v1.5. |
| 1.3 | 2026-05-18 | Bug #8 VTT-718: build_v15 consolida `related_to` desde 2 fuentes con dedup. |
| 1.4 | 2026-05-31 | Bug VTT-870 / TL Reviewer VTT: parse_report_sections regex acepta `:` final en headings (`:?` opcional). 6 secciones del REPORT dejan de perderse silenciosamente. |
| **1.5** | **2026-06-01** | **VTS-002 + VTS-003 / TL Reviewer VTT (review de v1.4). (a) `items_detected_for_tl_review` dejó de estar hardcoded a `[]` — ahora extrae del REPORT. (b) `how_to_verify` ya no se limita a bullets `-/*/+` — acepta también numerados (`1.`, `2)`) y párrafos. Refactor: helper `_extract_list_items(section_text)` reusable. 13/13 tests OK.** |

---

## 7. Referencias

- **Tarea VTT actual:** VTS-001 (formaliza el fix v1.4)
- **Origen del bug:** VTT-870 + devlog `b428d19d` (proyecto VTT)
- **Templates de REPORT:** `03.templates/normativa/_autoria/` (los headings del REPORT del agente deben seguir el formato del template)
- **PROTOCOL relacionado:** `VTT.PROTOCOL-MAN-001_gobernanza_manifest.md` (gobernanza del manifest v1.0 y v1.5)
- **Skill relacionada:** `VTT.SKILL-MAN-001_task_manifest.md`
