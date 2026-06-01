# BRIEF — VTS-003 — Fix how_to_verify parser limitado

| Campo | Valor |
|---|---|
| **Task ID** | VTS-003 |
| **Título** | [FIX-NORM] VTT.SCRIPT-MAN-001 v1.5 — how_to_verify acepta bullets + numerados + párrafos |
| **Proyecto** | VTS |
| **Phase** | NORM |
| **Sprint** | S01 |
| **Asignado a** | Coordinator (`51af43cf-...`) |
| **Creado por** | TL Reviewer VTT (`abdff0db-...`) |
| **Tipo** | bugfix |
| **Prioridad** | high |
| **Complejidad** | LOW-MEDIUM (refactor a helper reusable) |
| **Estimación** | 1h |

---

## 1. Objetivo

Reemplazar el parser limitado de `how_to_verify` (línea ~511) por un helper más tolerante (`_extract_list_items`) que acepte bullets, numerados y párrafos. El helper queda reusable para otros campos.

## 2. Contexto

### 2.1 Bug

Línea ~511 de `build_v10()`:
```python
"how_to_verify": [l.strip().lstrip("-*+ ") for l in (...).split("\n") if l.strip().startswith(("-", "*", "+"))],
```

Solo captura líneas que empiezan con `-`, `*`, `+`. Pasos numerados (`1. Ejecutar X`, `2) Verificar Y`) y párrafos descriptivos se pierden.

### 2.2 Por qué importa

Las guías paso-a-paso suelen ser numeradas, no con viñetas. El TL al revisar no ve cómo probar lo que el agente entregó.

### 2.3 Origen

TL Reviewer VTT al revisar v1.4 (tarea VTS-001). Reportado en VTS-003.

## 3. Alcance

### SÍ

- Crear helper `_extract_list_items(section_text)` que acepta bullets + numerados + párrafos
- Reemplazar la lógica inline de `how_to_verify` por llamada al helper
- Compartir el helper con VTS-002 (`items_detected`)
- Bumpear script v1.4 → v1.5 (consolidado con VTS-002)
- Documentar el helper en CODE_LOGIC (§2.2.bis + D-MAN-006 y D-MAN-007)
- 13 tests del helper

### NO

- No refactorizar `findings`, `adrs`, `derived_tasks` a usar el helper aún (queda como mejora futura)
- No regenerar manifests históricos
- No cambiar el formato del REPORT (los agentes pueden seguir usando bullets si quieren)

## 4. Criterios de aceptación

### DoD (12)

1. Script ejecuta sin error
2. Cambio probado con 13 casos del helper
3. CODE_LOGIC.md actualizado (D-MAN-006, D-MAN-007 + §2.2.bis)
4. Development Log creado
5. Sin devlog entries críticos/altos pendientes
6. Sin console.log/print debug
7. Manejo de errores OK (helper idempotente con None/empty)
8. Sin TODOs sin explicación
9. Sin código comentado innecesario
10. Sin hardcoded paths/UUIDs/secrets
11. Commit message formato VTT
12. PR a `main`

### Integración (2)

13. Cero regresión: bullets (`-/*/+`) siguen extrayendo items igual que en v1.4
14. Pasos numerados y párrafos del REPORT ahora aparecen en `how_to_verify` del manifest

### Acceptance específicos (4)

15. Helper `_extract_list_items` existe en el script y maneja None/empty sin error
16. Helper acepta: bullets (`-`, `*`, `+`), numerados (`N.`, `N)`), párrafos sin viñeta
17. Helper excluye: headings markdown (`#`, `##`, `###`) y líneas vacías
18. 13/13 tests del helper pasan

## 5. Cómo probar

```bash
# Test 1 — Bullets (regresión v1.4)
python -c "
import importlib.util
spec = importlib.util.spec_from_file_location('m', '00-platform/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
assert m._extract_list_items('- A\n- B') == ['A', 'B']
print('OK bullets')
"

# Test 2 — Numerados (fix v1.5)
python -c "
import importlib.util
spec = importlib.util.spec_from_file_location('m', '00-platform/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
assert m._extract_list_items('1. Uno\n2. Dos') == ['Uno', 'Dos']
print('OK numerados')
"

# Test 3 — Mix
python -c "
import importlib.util
spec = importlib.util.spec_from_file_location('m', '00-platform/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
got = m._extract_list_items('- a\n1. b\nc\n* d')
assert got == ['a', 'b', 'c', 'd'], f'got {got}'
print('OK mix')
"

# Test 4 — Idempotencia
python -c "
import importlib.util
spec = importlib.util.spec_from_file_location('m', '00-platform/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
assert m._extract_list_items(None) == []
assert m._extract_list_items('') == []
print('OK idempotencia')
"
```

## 6. Referencias

- **Bug paralelo:** VTS-002 (mismo PR, mismo bump v1.5)
- **Helper introducido:** `_extract_list_items` (reutilizado por VTS-002)
- **Decisiones:** D-MAN-006 (parser tolerante), D-MAN-007 (helper reusable) en CODE_LOGIC §4
- **Origen review:** TL Reviewer VTT al revisar v1.4
