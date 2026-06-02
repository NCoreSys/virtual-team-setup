# Development Log — VTS-003 — Fix how_to_verify parser limitado en VTT.SCRIPT-MAN-001

| Campo | Valor |
|---|---|
| **Task** | VTS-003 |
| **Fecha** | 2026-06-01 |
| **Agente** | Coordinator (`51af43cf-8939-4a6f-99ee-31238cfd6894`) |
| **Proyecto** | VTS (Virtual Teams Setup) |
| **Phase** | NORM |
| **Sprint** | S01 |
| **Branch** | `feature/VTS-001-002-003` (consolidado con VTS-001 y VTS-002 — fixes al mismo script) |
| **Origen del bug** | TL Reviewer VTT en review de v1.4 |

---

## 1. Resumen ejecutivo

`how_to_verify` en `build_v10()` línea ~511 del script usaba un parser **limitado a bullets** (`-/*/+`). Si los pasos del REPORT estaban en formato **numerado** (`1.`, `2.`, `1)`) o como **párrafos sin viñeta**, se perdían silenciosamente. Fix v1.5: refactor a un helper `_extract_list_items` tolerante con múltiples formatos.

---

## 2. Descripción del bug

### 2.1 Síntoma

El campo `how_to_verify` del manifest v1.0 quedaba vacío o incompleto cuando el REPORT del agente usaba:
- Pasos numerados: `1. Ejecutar X`, `2. Verificar Y`
- Párrafos descriptivos sin viñeta
- Mezcla de formatos

Esto es común porque las guías paso-a-paso suelen ser numeradas (no con viñetas).

### 2.2 Causa raíz

Línea ~511 de `build_v10()`:

```python
"how_to_verify": [l.strip().lstrip("-*+ ") for l in (report_sections.get("how_to_verify") or "").split("\n") if l.strip().startswith(("-", "*", "+"))],
```

El predicado `l.strip().startswith(("-", "*", "+"))` filtra todo lo que no empiece con esos 3 chars. Las líneas numeradas (`1.`, `2.`) y los párrafos no matchean → se descartan.

### 2.3 Impacto

- Pasos críticos de validación que el agente documentaba quedaban fuera del manifest
- El TL al revisar no veía cómo probar lo que el agente entregó
- Pérdida silenciosa: el campo `how_to_verify` quedaba con menos items de los reales, sin alerta

### 2.4 Detección

TL Reviewer VTT detectó el bug al revisar v1.4. Reportado en VTS-003.

---

## 3. Fix aplicado

### 3.1 Refactor a helper

Se extrajo la lógica a un helper reusable `_extract_list_items(section_text)`:

```python
def _extract_list_items(section_text):
    """
    Extrae items de una seccion narrativa del REPORT como lista de strings.
    Acepta bullets (-/*/+), numerados (1./1)) y parrafos.
    Excluye headings markdown (#).
    Idempotente: None/empty → [].
    """
    if not section_text:
        return []
    import re as _re
    items = []
    for raw in section_text.split("\n"):
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#"):
            continue
        cleaned = _re.sub(r"^[-*+]\s+", "", line)
        cleaned = _re.sub(r"^\d+[.)]\s+", "", cleaned)
        if cleaned:
            items.append(cleaned)
    return items
```

### 3.2 Aplicación en `build_v10()`

```python
# v1.4 (buggy)
"how_to_verify": [l.strip().lstrip("-*+ ") for l in (report_sections.get("how_to_verify") or "").split("\n") if l.strip().startswith(("-", "*", "+"))],

# v1.5 (fixed)
"how_to_verify": _extract_list_items(report_sections.get("how_to_verify")),
```

### 3.3 Reutilización del helper

El mismo helper se usa también para `items_detected_for_tl_review` (VTS-002). Esto centraliza la lógica de parsing de listas y reduce duplicación.

---

## 4. Pruebas realizadas

### 4.1 Test inline — 13 casos cubiertos

```
OK  None input
OK  Empty string
OK  Only whitespace
OK  Bullets con -      → 3 items
OK  Bullets con *      → 2 items
OK  Bullets con +      → 2 items
OK  Numerados 1./2.    → 3 items
OK  Numerados 1)/2)    → 2 items
OK  Párrafos           → 2 items
OK  Mix de formatos    → 4 items
OK  Heading excluido   → 1 item (solo el bullet)
OK  Múltiples headings → 1 item
OK  Líneas vacías intercaladas → 2 items
```

**Resultado:** 13/13 OK. Cero regresión con respecto a v1.4 (bullets siguen funcionando).

### 4.2 Idempotencia

`_extract_list_items(None)` → `[]`
`_extract_list_items("")` → `[]`
`_extract_list_items("   ")` → `[]`

Sin excepciones. Comportamiento seguro ante secciones ausentes en el REPORT.

---

## 5. Archivos modificados

Idéntico a VTS-002 — ambos fixes están en el mismo commit (v1.5 del script):

| Path | Cambio |
|---|---|
| `00-platform/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py` | Header v1.4 → v1.5 + helper `_extract_list_items` + fix línea ~511 |
| `knowledge/code-logic/scripts/manifest/VTT.SCRIPT-MAN-001.LOGIC.md` | Actualizado con D-MAN-006, D-MAN-007 + §2.2.bis del helper |
| `knowledge/development-log/2026-06-01_VTS-003_fix-how-to-verify-parser-limitado.md` | Este devlog |
| `knowledge/agent-tasks/briefs/BRIEF_VTS-003_fix-how-to-verify-parser-limitado.md` | BRIEF de la tarea |
| `knowledge/agent-tasks/assignments/ASSIGNMENT_VTS-003_fix-how-to-verify-parser-limitado.md` | ASSIGNMENT |

---

## 6. Decisiones técnicas

### 6.1 Helper en vez de inline

Decisión D-MAN-007: introducir `_extract_list_items` como función helper en lugar de duplicar la lógica en cada campo. Razones:
- VTS-002 y VTS-003 necesitaban el mismo parser → DRY
- Tests centralizados (13 casos en una sola función)
- Si en el futuro `findings`, `adrs`, etc. necesitan el mismo tratamiento → migración trivial

### 6.2 Qué considera "ítem válido"

El helper considera ítem válido:
- Líneas con bullet (`-`, `*`, `+`) — limpia el prefijo
- Líneas numeradas (`1.`, `2)`, etc.) — limpia el prefijo
- Líneas sin prefijo pero con texto — las agrega tal cual (párrafos)

**No considera ítem válido:**
- Líneas vacías
- Headings markdown (`#`, `##`, `###`)
- Líneas con solo espacios

### 6.3 Riesgo de "demasiado tolerante"

Si el REPORT incluye texto narrativo NO estructurado bajo `### Como verificar`, el helper lo capturará como ítems (uno por línea). Esto puede inflar el campo con basura.

Mitigación: confiar en el formato del REPORT (los agentes deben estructurar la sección con bullets/numerados). Si el REPORT está mal estructurado, el problema es upstream — no del helper.

---

## 7. Cómo probar

```bash
# Test 1 — Bullets (regresión v1.4)
python -c "
import importlib.util
spec = importlib.util.spec_from_file_location('m', '00-platform/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
print(m._extract_list_items('- Paso A\n- Paso B'))
# Esperado: ['Paso A', 'Paso B']
"

# Test 2 — Numerados (fix v1.5)
python -c "
import importlib.util
spec = importlib.util.spec_from_file_location('m', '00-platform/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
print(m._extract_list_items('1. Ejecutar curl\n2. Verificar 200\n3. Revisar log'))
# Esperado: ['Ejecutar curl', 'Verificar 200', 'Revisar log']
"

# Test 3 — Idempotencia
python -c "
import importlib.util
spec = importlib.util.spec_from_file_location('m', '00-platform/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
print(m._extract_list_items(None))
print(m._extract_list_items(''))
# Esperado: [] y []
"
```

---

## 8. Commit message a usar (consolidado VTS-002 + VTS-003)

```
[agente:coord] [proyecto:vtt-setup] [scope:00-platform/02.normativa,knowledge] [type:functional]
VTS-002+003: items_detected ya no hardcoded + how_to_verify acepta multi-formato

VTT.SCRIPT-MAN-001 v1.4 -> v1.5. 2 bugs detectados por TL Reviewer VTT
en review de v1.4 (tarea VTS-001):

VTS-002: items_detected_for_tl_review estaba hardcoded a []. Ahora
extrae del REPORT con helper _extract_list_items.

VTS-003: how_to_verify parser solo capturaba bullets (-/*/+). Pasos
numerados (1./1)) y parrafos sin vineta se perdian. Ahora usa el
helper _extract_list_items que acepta los 3 formatos.

Refactor: nuevo helper _extract_list_items(section_text) que acepta
bullets, numerados y parrafos, excluye headings markdown. Tests:
13/13 OK. Cero regresion con respecto a v1.4.

Motivo: review TL de v1.4 sobre VTS-001
Origen: tareas VTS-002 y VTS-003 creadas por TL VTT
Consumidores: todos los proyectos VTT que generen manifests

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
```

---

## 9. Referencias

- **Bug paralelo:** VTS-002 (mismo PR, mismo bump v1.5)
- **Origen review:** TL Reviewer VTT al revisar v1.4 (tarea VTS-001)
- **Helper introducido:** `_extract_list_items` (compartido con VTS-002)
- **Decisiones registradas:** D-MAN-006, D-MAN-007 en CODE_LOGIC §4
