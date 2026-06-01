# Development Log — VTS-002 — Fix items_detected hardcoded en VTT.SCRIPT-MAN-001

| Campo | Valor |
|---|---|
| **Task** | VTS-002 |
| **Fecha** | 2026-06-01 |
| **Agente** | Coordinator (`51af43cf-8939-4a6f-99ee-31238cfd6894`) |
| **Proyecto** | VTS (Virtual Teams Setup) |
| **Phase** | NORM |
| **Sprint** | S01 |
| **Branch** | `feature/VTS-001-002-003` (consolidado con VTS-001 y VTS-003 — fixes al mismo script) |
| **Origen del bug** | TL Reviewer VTT en review de v1.4 |

---

## 1. Resumen ejecutivo

`items_detected_for_tl_review` estaba **hardcoded a `[]`** en `build_v10()` línea ~509 del script `VTT.SCRIPT-MAN-001_gen_task_manifest.py`. Aunque el REPORT del agente tuviera contenido bajo `### Items detectados para trackeo`, el campo del manifest siempre quedaba vacío. Fix v1.5: usar el helper nuevo `_extract_list_items(report_sections.get("items_detected"))`.

---

## 2. Descripción del bug

### 2.1 Síntoma

El campo `items_detected_for_tl_review` del manifest v1.0 siempre se generaba como `[]` sin importar lo que dijera el REPORT. El TL al revisar la tarea no veía los items que el agente quería que el TL trackeara.

### 2.2 Causa raíz

Línea ~509 de `build_v10()`:

```python
"items_detected_for_tl_review": [],
```

Hardcoded a array vacío. Probablemente era un placeholder durante el desarrollo inicial del script que nunca se conectó al parser de `report_sections`.

### 2.3 Impacto

- Items críticos que el agente detectaba durante la ejecución y quería que el TL trackeara se perdían silenciosamente
- El TL no tenía evidencia estructurada de hallazgos secundarios del agente
- Otro caso de "datos del REPORT que se evaporan en el JSON final" — patrón similar al bug VTT-870 resuelto en v1.4

### 2.4 Detección

TL Reviewer VTT detectó el bug al revisar v1.4 (la tarea VTS-001 fue su test de regresión). Reportado en VTS-002.

---

## 3. Fix aplicado

### 3.1 Cambio

```python
# v1.4 (buggy — hardcoded)
"items_detected_for_tl_review": [],

# v1.5 (fixed)
"items_detected_for_tl_review": _extract_list_items(report_sections.get("items_detected")),
```

### 3.2 Refactor asociado

Se introdujo el helper `_extract_list_items(section_text)` que acepta múltiples formatos (bullets, numerados, párrafos) y excluye headings. Ver devlog de VTS-003 para detalle del helper.

---

## 4. Pruebas realizadas

Las pruebas del helper `_extract_list_items` cubren 13 casos (ver devlog VTS-003). Específicamente para `items_detected`:

```python
# Test del campo en aislamiento
section = '- Item A detectado\n- Item B para track\n- Item C revisar'
result = _extract_list_items(section)
# Esperado: ['Item A detectado', 'Item B para track', 'Item C revisar']
assert len(result) == 3
```

Con REPORT real que tenga la sección `### Items detectados para trackeo:` con contenido, el manifest ahora refleja los items.

---

## 5. Archivos modificados

| Path | Cambio | Líneas afectadas |
|---|---|---|
| `00-platform/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py` | Header v1.4 → v1.5 + helper `_extract_list_items` + fix línea ~509 | ~10, ~228, ~509 |
| `knowledge/code-logic/scripts/manifest/VTT.SCRIPT-MAN-001.LOGIC.md` | Actualizado con D-MAN-005 + nueva sección §2.2.bis + historial v1.5 | varias |
| `knowledge/development-log/2026-06-01_VTS-002_fix-items-detected-hardcoded.md` | Este devlog | nuevo |
| `knowledge/agent-tasks/briefs/BRIEF_VTS-002_fix-items-detected-hardcoded.md` | BRIEF de la tarea | nuevo |
| `knowledge/agent-tasks/assignments/ASSIGNMENT_VTS-002_fix-items-detected-hardcoded.md` | ASSIGNMENT de la tarea | nuevo |

---

## 6. Decisiones técnicas

### 6.1 Refactor compartido con VTS-003

VTS-002 y VTS-003 comparten el helper `_extract_list_items`. La introducción del helper se justifica con VTS-003 (que necesitaba parser más complejo). VTS-002 simplemente lo consume. Por eso ambos devlogs se referencian.

### 6.2 Sin migración del manifest histórico

Los manifests v1.0 ya generados con `items_detected_for_tl_review: []` quedan así. No los regenero (decisión idéntica a VTS-001).

### 6.3 Otros campos potencialmente afectados

Investigué si hay otros campos del manifest que también estén hardcoded a `[]` o similar. Encontré:

- `living_documents_declared_no_change: []` — hardcoded, pero esto es por diseño (el agente declara explícitamente en otro lado)
- `tech_debt_for_r2: []` — hardcoded, también por diseño

Decisión: NO tocar esos en este fix. Si el TL detecta que también deberían leer del REPORT → tarea separada.

---

## 7. Commit message a usar

Ver §10 del devlog VTS-003 (commit consolidado para VTS-002 + VTS-003).

---

## 8. Referencias

- **Bug paralelo:** VTS-003 (mismo PR, mismo bump v1.5)
- **Origen review:** TL Reviewer VTT al revisar v1.4
- **Helper introducido:** `_extract_list_items` (ver devlog VTS-003)
- **Decisiones registradas:** D-MAN-005, D-MAN-007 en CODE_LOGIC §4
