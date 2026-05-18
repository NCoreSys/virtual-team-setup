# ÍNDICE — Templates del Proceso Cierre PM → Handoff PJM

**Versión:** 1.0
**Fecha:** 2026-04-22
**Proceso asociado:** [`09_PROCESO_CIERRE_PM_HANDOFF_PJM.md`](../../standard/09_PROCESO_CIERRE_PM_HANDOFF_PJM.md)
**Caso validado con:** Memory Service R1

---

## Propósito

Esta carpeta contiene los **7 templates** que materializan el proceso estandarizado de entrega PM → PJM. Cualquier PM que necesite cerrar un proyecto y entregarlo operativamente al PJM debe usarlos en el orden definido por el proceso §4.

---

## Mapeo Proceso → Templates

| Paso del proceso (09) | Template a usar | Salida |
|-----------------------|-----------------|--------|
| 1. Leer análisis de feature | — (solo lectura) | Entendimiento consolidado |
| 2. Cerrar docs PM (freeze) | — (marcar docs existentes) | Docs en estado FINAL |
| **3. Filtrar deliverables** | [`TEMPLATE_FASES_APLICABLES_V1.0.md`](TEMPLATE_FASES_APLICABLES_V1.0.md) | `FASES_APLICABLES_<proyecto>.md` |
| **4. Definir iniciación** | [`TEMPLATE_PRE_HANDOFF_INICIACION_V1.0.md`](TEMPLATE_PRE_HANDOFF_INICIACION_V1.0.md) | `PRE_HANDOFF_INICIACION_<proyecto>.md` |
| **5. Consolidar plan maestro** | [`TEMPLATE_CONSOLIDADO_V1.0.md`](TEMPLATE_CONSOLIDADO_V1.0.md) | `CONSOLIDADO_<proyecto>.md` |
| **6. Generar Cierre + Handoff** | [`TEMPLATE_CIERRE_PM_HANDOFF_PJM_V1.0.md`](TEMPLATE_CIERRE_PM_HANDOFF_PJM_V1.0.md) | `CIERRE_PM_HANDOFF_PJM_<proyecto>.md` |
| **7. Generar Task Index Seed** | [`TEMPLATE_TASK_INDEX_SEED_V1.0.md`](TEMPLATE_TASK_INDEX_SEED_V1.0.md) | `TASK_INDEX_SEED_<proyecto>.md` |
| **8. Generar script ejecutable** | [`TEMPLATE_create_vtt_script_V1.0.py`](TEMPLATE_create_vtt_script_V1.0.py) | `create_<proyecto>_vtt.py` |
| **9. Generar HO de ejecución** | [`TEMPLATE_HO_PJM_CARGA_VTT_V1.0.md`](TEMPLATE_HO_PJM_CARGA_VTT_V1.0.md) | `HO_PJM_CARGA_VTT_<proyecto>.md` |

---

## Reglas generales de uso

### 1. Placeholders

Todos los templates usan `<<PLACEHOLDER>>` como marca de reemplazo. Al copiar:

```bash
sed -i 's/<<PROYECTO>>/Memory Service/g' CIERRE_PM_HANDOFF_PJM_Memory_Service.md
```

Placeholders comunes:
- `<<PROYECTO>>` / `<<NOMBRE_PROYECTO>>` — nombre del proyecto
- `<<CODIGO>>` / `<<CODIGO_3_LETRAS>>` — código corto (ej: MEM)
- `<<N>>` — número (tareas, horas, etc.)
- `<<UUID_*>>` — UUIDs reales del proyecto
- `<<YYYY-MM-DD>>` — fecha de emisión
- `<<vX.Y>>` — versión de doc

### 2. Orden de generación

Los templates se generan en el orden del proceso (3 → 9). Cada uno depende del anterior:

```
TEMPLATE_FASES_APLICABLES
        ↓
TEMPLATE_PRE_HANDOFF_INICIACION
        ↓
TEMPLATE_CONSOLIDADO  ──┐
                        ↓
        TEMPLATE_CIERRE_PM_HANDOFF_PJM (principal)
                        ↓
        TEMPLATE_TASK_INDEX_SEED
                        ↓
        TEMPLATE_create_vtt_script.py
                        ↓
        TEMPLATE_HO_PJM_CARGA_VTT (entrega final al PJM)
```

### 3. Gates de calidad

Cada paso tiene gate definido en el proceso §4. **No avanzar al siguiente template sin cerrar el gate del anterior**.

### 4. Referencias a archivos

Los templates incluyen al final:
- `Template source: <nombre del template>`
- `Proceso asociado: 09_PROCESO_CIERRE_PM_HANDOFF_PJM.md (paso X)`

**Preservar estas referencias** en los docs generados para trazabilidad.

---

## Templates descriptivos

### 1. TEMPLATE_FASES_APLICABLES_V1.0.md

**Input:** catálogo SDLC de 438 deliverables + contexto del proyecto
**Output:** filtro de deliverables aplicables con razones de exclusión
**Tamaño típico del output:** 400-800 líneas

### 2. TEMPLATE_PRE_HANDOFF_INICIACION_V1.0.md

**Input:** filtro + necesidades operativas (VTT, repo, VM, team, tooling)
**Output:** 20-30 sub-tareas operativas en 7 categorías (A-G)
**Tamaño típico del output:** 300-500 líneas

### 3. TEMPLATE_CONSOLIDADO_V1.0.md

**Input:** fases aplicables + iniciación + listado de tareas VTT
**Output:** plan maestro con iniciación + fases SDLC + tareas reemplazando deliverables 4-7
**Tamaño típico del output:** 700-1200 líneas

### 4. TEMPLATE_CIERRE_PM_HANDOFF_PJM_V1.0.md  (⭐ PRINCIPAL)

**Input:** todos los outputs anteriores
**Output:** documento formal de cierre PM + handoff operativo en formato V4.2
**Tamaño típico del output:** 600-900 líneas

Este es el documento más importante — es el que el PJM recibe oficialmente.

### 5. TEMPLATE_TASK_INDEX_SEED_V1.0.md

**Input:** UUIDs reales + descripciones detalladas de tareas
**Output:** seed con todos los campos VTT (title, description, priorityId, etc.)
**Tamaño típico del output:** 800-1500 líneas (depende de número de tareas)

Contiene las **descripciones 150-2000 chars** de cada tarea y los **UUIDs globales**.

### 6. TEMPLATE_create_vtt_script_V1.0.py

**Input:** seed completo
**Output:** script Python ejecutable que crea todo en VTT
**Tamaño típico del output:** 500-800 líneas

Secuencia de 6 POSTs: Project → Phases → Deliveries → Tasks → Assignments → Dependencies.

### 7. TEMPLATE_HO_PJM_CARGA_VTT_V1.0.md

**Input:** script listo + seed cerrado
**Output:** HO dirigido al PJM con instrucciones de ejecución
**Tamaño típico del output:** 200-300 líneas

Incluye: prerrequisitos, proceso de ejecución, verificación post, rollback.

---

## Caso de validación: Memory Service R1

Los 7 templates fueron validados generando los siguientes artefactos exitosamente el 2026-04-22:

| Template | Artefacto generado | Ubicación |
|----------|--------------------|-----------|
| FASES_APLICABLES | `FASES_APLICABLES_MEMORY_SERVICE.md` | `Release2.0/01-PM/` |
| PRE_HANDOFF_INICIACION | `PRE_HANDOFF_INICIACION_MEMORY_SERVICE.md` | `Release2.0/01-PM/` |
| CONSOLIDADO | `CONSOLIDADO_MEMORY_SERVICE_R1.md` | `Release2.0/01-PM/` |
| CIERRE_PM_HANDOFF_PJM | `CIERRE_PM_HANDOFF_PJM_MEMORY_SERVICE_R1.md` | `Release2.0/01-PM/` |
| TASK_INDEX_SEED | `TASK_INDEX_SEED_MEMORY_SERVICE.md` | `Release2.0/01-PM/` |
| create_vtt_script.py | `create_memory_service_vtt.py` | `Release2.0/scripts/` |
| HO_PJM_CARGA_VTT | `HO_PJM_CARGA_VTT_MEMORY_SERVICE.md` | `Release2.0/01-PM/` |

El script ejecutó correctamente y creó: 1 Project + 10 Phases + 65 Deliveries + 116 Tasks + 15 Dependencies.

---

## Errores comunes a evitar

Ver `09_PROCESO_CIERRE_PM_HANDOFF_PJM.md §7` para la lista completa. Los principales:

1. **Hardcodear UUIDs stale** — usar siempre source of truth actualizado
2. **`complexity: "medium"`** — debe ser MAYÚSCULAS `"MEDIUM"`
3. **`assignedTo`** — se ignora, usar `assignedToId`
4. **No mapear tarea → deliverables** — causa retrabajo por ambigüedad
5. **1 HO por rol** — correcto: 1 HO por fase
6. **Usar wizard de creación** — usar POST separados
7. **Mezclar subfases con deliverables** — son unidades distintas

---

## Mantenimiento de templates

### Cuándo actualizar

- Cuando se descubre un patrón recurrente en proyectos
- Cuando cambian los endpoints del sistema VTT
- Cuando se agregan nuevos gates de calidad
- Cuando se detecta un error común no documentado

### Cómo actualizar

1. Incrementar versión del template (V1.0 → V1.1 → V2.0)
2. Documentar cambios en el header del template
3. Actualizar este índice con la nueva versión
4. Mantener el template anterior por 1 release antes de borrarlo

---

## Historial de versiones

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0 | 2026-04-22 | Versión inicial. 7 templates generados a partir del caso Memory Service R1. |

---

**Ubicación:** `memory-service-project/00-platform/templates/Handoff_proceso/`

**Proceso asociado:** [`09_PROCESO_CIERRE_PM_HANDOFF_PJM.md`](../../standard/09_PROCESO_CIERRE_PM_HANDOFF_PJM.md)
