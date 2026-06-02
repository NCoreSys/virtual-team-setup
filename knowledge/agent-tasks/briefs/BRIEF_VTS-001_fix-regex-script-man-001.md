# BRIEF — VTS-001 — Fix regex VTT.SCRIPT-MAN-001 v1.4

| Campo | Valor |
|---|---|
| **Task ID** | VTS-001 |
| **Título** | [FIX-NORM] VTT.SCRIPT-MAN-001 v1.4 — regex acepta `:` final en headings (bug VTT-870) |
| **Proyecto** | VTS (Virtual Teams Setup) |
| **Phase** | NORM (Normativa y Gobierno Editorial) |
| **Sprint** | S01 |
| **Asignado a** | Coordinator (`51af43cf-8939-4a6f-99ee-31238cfd6894`) |
| **Creado por** | TL Reviewer VTT (`abdff0db-ad0b-4a0c-99f5-c898d18bd2d8`) |
| **Tipo** | bugfix |
| **Prioridad** | high |
| **Complejidad** | LOW |
| **Estimación** | 1h |

---

## 1. Objetivo

Asentar formalmente el fix del regex de `parse_report_sections()` en `VTT.SCRIPT-MAN-001_gen_task_manifest.py`. El bug causaba que 6 de 12 secciones narrativas del REPORT (findings, adrs, derived_tasks, notes, items_detected, how_to_verify) se perdieran silenciosamente en los manifests v1.0/v1.5 cuando los headings tenían `:` final.

---

## 2. Contexto

### 2.1 Origen del bug

- **Reportado por:** TL Reviewer VTT en tarea VTT-870 (proyecto VTT)
- **Devlog improvement:** id `b428d19d` (consultar VTT-870 para id exacto si aplica)
- **Detección:** TL Reviewer revisó manifest v1.0 entregado por agente y notó que findings/adrs/notes/items_detected/derived_tasks/how_to_verify quedaron como `"N/A"` o `[]` aunque el REPORT sí los tenía con contenido

### 2.2 Causa raíz

`VTT.SCRIPT-MAN-001_gen_task_manifest.py` línea 207:

```python
pattern_md = rf"(?:^|\n)#{{1,3}}\s+{re.escape(alias)}\s*\n(.*?)(?=\n#{{1,3}}\s+|\Z)"
```

El `\s*\n` después del alias NO toleraba `:` final. Heading `### Findings:` (con dos puntos) no matcheaba → sección `None` → caía a default.

### 2.3 Por qué importa

- Manifest v1.0 es la entrada del agente al cerrar tarea
- Manifest v1.5 es la entrada del TL al aprobar tarea
- Ambos son auditables y se preservan en VTT como attachments + en git como tracking files
- Si 6 de 12 secciones quedan vacías sin alerta → trazabilidad rota → análisis cross-tarea fallido

---

## 3. Alcance

### 3.1 Lo que se hace

- Modificar regex `pattern_md` línea ~207 para aceptar `:?` opcional
- Modificar regex `pattern_line` (fallback) para homogeneidad
- Bumpear header del script v1.3 → v1.4
- Agregar entrada changelog v1.4
- Crear CODE_LOGIC.md del script
- Crear Development Log
- Commit estructurado + push + PR

### 3.2 Lo que NO se hace

- Reprocesar manifests históricos generados con v1.3 buggy (los datos viejos quedan como están)
- Migrar el script a otro nivel (sigue siendo Script, no Skill)
- Refactorizar otras partes del script no relacionadas con `parse_report_sections`
- Agregar tests unitarios formales (queda como deuda técnica derivada)

---

## 4. Criterios de aceptación

### 4.1 DoD (12 obligatorios)

1. Script ejecuta sin error con Python 3.12+
2. Cambio probado con REPORT mixto (4 secciones con `:` + 4 sin `:`)
3. CODE_LOGIC.md creado/actualizado para el script
4. Development Log creado en `knowledge/development-log/`
5. Sin devlog entries críticos/altos pendientes al cerrar
6. Sin `console.log` / `print` de debug
7. Manejo de errores con try-catch donde aplica (regex no necesita try)
8. Sin TODOs sin explicación
9. Sin código comentado innecesario
10. Sin hardcoded paths/UUIDs/secrets
11. Commit message con formato VTT (`[agente:coord] [proyecto:vtt-setup] ...`)
12. PR creado a `main` con `gh pr create`

### 4.2 Integración (2)

13. Manifests generados con headings SIN `:` (estilo v1.3) siguen funcionando (cero regresión)
14. Manifests generados con headings CON `:` ahora extraen las 6 secciones críticas (findings, adrs, derived_tasks, notes, items_detected, how_to_verify)

### 4.3 Acceptance específicos del bug (3)

15. Regex `pattern_md` línea ~207 acepta `:?` opcional antes del `\s*\n`
16. Test inline con REPORT mixto (8 secciones, 4 con `:` y 4 sin `:`) imprime las 8 secciones con contenido NO vacío
17. Changelog v1.4 en el header del script con referencia explícita a VTT-870

---

## 5. Cómo probar

### 5.1 Test inline (regex aislado)

```bash
python -c "
import re
report = '''### Findings:
- Finding A
'''
p = r'(?:^|\n)#{1,3}\s+Findings\s*:?\s*\n(.*?)(?=\n#{1,3}\s+|\Z)'
m = re.search(p, report, re.DOTALL | re.IGNORECASE)
print('OK' if m and m.group(1).strip() else 'FAIL')
"
# Esperado: OK
```

### 5.2 Verificar versión y changelog del script

```bash
grep "Version: 1.4" 00-platform/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py
grep "VTT-870" 00-platform/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py
# Ambos deben matchear
```

### 5.3 Verificar que el fix está en el regex

```bash
grep '{re.escape(alias)}.s.\*:?' 00-platform/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py
# Debe matchear el pattern_md y pattern_line con :? opcional
```

---

## 6. Referencias

- **Origen:** VTT-870 (proyecto VTT) — devlog `b428d19d` o equivalente
- **Script afectado:** `00-platform/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py`
- **Protocol relacionado:** `VTT.PROTOCOL-MAN-001_gobernanza_manifest.md`
- **Skill relacionada:** `VTT.SKILL-MAN-001_task_manifest.md`
