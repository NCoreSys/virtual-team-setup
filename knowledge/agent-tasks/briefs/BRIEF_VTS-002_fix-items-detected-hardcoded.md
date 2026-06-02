# BRIEF — VTS-002 — Fix items_detected hardcoded en VTT.SCRIPT-MAN-001

| Campo | Valor |
|---|---|
| **Task ID** | VTS-002 |
| **Título** | [FIX-NORM] VTT.SCRIPT-MAN-001 v1.5 — items_detected_for_tl_review hardcoded a [] |
| **Proyecto** | VTS |
| **Phase** | NORM |
| **Sprint** | S01 |
| **Asignado a** | Coordinator (`51af43cf-...`) |
| **Creado por** | TL Reviewer VTT (`abdff0db-...`) |
| **Tipo** | bugfix |
| **Prioridad** | high |
| **Complejidad** | LOW |
| **Estimación** | 0.5h |

---

## 1. Objetivo

Conectar el campo `items_detected_for_tl_review` del manifest v1.0 al parser de secciones del REPORT. Hoy está hardcoded a `[]` ignorando el contenido del REPORT.

## 2. Contexto

### 2.1 Bug

Línea ~509 de `build_v10()`:
```python
"items_detected_for_tl_review": [],  # ← hardcoded, ignora report_sections["items_detected"]
```

### 2.2 Por qué importa

Items críticos que el agente detecta y quiere que el TL trackee se pierden silenciosamente. El TL no ve evidencia estructurada de hallazgos secundarios del agente.

### 2.3 Origen

TL Reviewer VTT al revisar v1.4 (tarea VTS-001). Reportado en VTS-002.

## 3. Alcance

### SÍ

- Reemplazar el `[]` hardcoded por llamada al helper `_extract_list_items(report_sections.get("items_detected"))`
- El helper se introduce en VTS-003 (mismo PR consolidado)
- Bumpear script v1.4 → v1.5 (consolidado con VTS-003)
- Actualizar CODE_LOGIC + devlog

### NO

- No tocar otros campos hardcoded por diseño (`living_documents_declared_no_change`, `tech_debt_for_r2`)
- No refactorizar `findings`, `adrs`, `derived_tasks` aún (queda como mejora futura)
- No regenerar manifests históricos

## 4. Criterios de aceptación

### DoD (12)

1. Script ejecuta sin error
2. Cambio probado con REPORT con `items_detected` con contenido
3. CODE_LOGIC.md actualizado (D-MAN-005)
4. Development Log creado
5. Sin devlog entries críticos/altos pendientes
6. Sin console.log/print debug
7. Manejo de errores OK
8. Sin TODOs sin explicación
9. Sin código comentado innecesario
10. Sin hardcoded paths/UUIDs/secrets
11. Commit message formato VTT
12. PR a `main`

### Integración (2)

13. `items_detected_for_tl_review` ahora contiene los items del REPORT cuando los hay
14. Si la sección `items_detected` NO existe en el REPORT → campo queda como `[]` (igual que antes — sin regresión)

### Acceptance específicos (3)

15. Línea ~509 cambia de `"items_detected_for_tl_review": []` a llamada al helper
16. Test con REPORT que tenga `### Items detectados para trackeo` con bullets devuelve items NO vacíos
17. Changelog v1.5 documenta el fix con referencia a VTS-002

## 5. Cómo probar

```bash
# Verificar fix en código
grep -n 'items_detected_for_tl_review' 00-platform/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py
# Debe matchear: _extract_list_items(report_sections.get("items_detected"))

# Test del helper
python -c "
import importlib.util
spec = importlib.util.spec_from_file_location('m', '00-platform/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
print(m._extract_list_items('- Item A\n- Item B'))
# Esperado: ['Item A', 'Item B']
"
```

## 6. Referencias

- **Bug paralelo:** VTS-003 (mismo PR, mismo bump v1.5)
- **Origen review:** TL Reviewer VTT al revisar v1.4
- **Decisión:** D-MAN-005 en CODE_LOGIC §4
