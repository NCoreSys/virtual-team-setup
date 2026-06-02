# VTT.WORKFLOW-HO-001.019 — Producir JSON Sincronizado con .md

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-HO-001.019` |
| **Pertenece a** | `VTT.PROTOCOL-HO-001` §5.4.1, §5.4.7 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-06-01 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | TL (productor del .md) |
| **Tipo** | [PROCESO] sub-procedimiento de sincronización |

---

## 1. Propósito

Workflow genérico que produce/actualiza el archivo .json a partir del .md cuando se actualiza una subsección del 3B.9.x. Garantiza la convención de doble output sincronizado de FASE 4.

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `md_path` | path | producido por WORKFLOW-014/015/016/017 | sí | Archivo .md actualizado |
| `schema_objetivo` | enum | tipo de subsección | sí | `task_breakdown` / `routing_index` / `wbs` / etc. |

---

## 3. Precondiciones

- Archivo .md existe en disco con versión declarada.
- Schema correspondiente está definido (ver Anexos C y D del Protocol).

---

## 4. Reglas del Workflow

- **R1:** Ambos archivos (.md y .json) llevan misma versión.
- **R2:** JSON es derivado del .md — si hay conflicto, el .md gana (es la fuente humana).
- **R3:** Si .md cambia → re-ejecutar este workflow inmediatamente para mantener sincronización.
- **R4:** Validar JSON contra schema antes de cerrar.

---

## 5. Pasos

### Paso 1 — TL identifica schema objetivo

Según el archivo .md a sincronizar:
- `3B.9.3` → schema `task_breakdown`
- `3B.9.10` → schema `routing_index`
- `3B.9.4` → schema `dependency_map`
- ... etc.

### Paso 2 — TL parsea contenido del .md a estructura

Por cada fila de tabla o sección estructurable del .md → estructura JSON.

Ejemplo para Task Breakdown:
- Cada fila de tabla → objeto JSON.
- Campos: `task_id`, `sprint`, `modulo`, `titulo`, `owner`, `rol`, `esfuerzo`, `dep_technical`, `dep_role`, `gate_release`, `external_blockers`, `criterio_aceptacion`, `evidencia`, `archivos_afectados`, `spec_source`, `seccion`, `adr_decision`.

### Paso 3 — TL valida JSON contra schema

JSON debe pasar validación de schema (campos requeridos presentes, tipos correctos).

Si falla validación → corregir .md (puede tener campo faltante o mal formateado), regenerar.

### Paso 4 — TL escribe archivo .json al mismo path con misma versión

Path: `<basename>.json` paralelo al `.md`.

Versión declarada coincide con la del .md.

### Paso 5 — TL ejecuta diff de validación

Verifica que ambos archivos representan misma información (todas las filas del .md están en .json, sin duplicados ni omisiones).

Si diff falla → corregir antes de cerrar.

---

## 6. Outputs

| Output | Tipo | Destino |
|---|---|---|
| `<basename>.json` | archivo .json | mismo path que .md |

---

## 7. Validación

- .json existe con misma versión que .md.
- Pasa validación contra schema.
- Diff con .md no muestra omisiones ni duplicados.

---

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| JSON no pasa validación de schema | Campo requerido faltante en .md | Corregir .md primero |
| Versiones .md y .json desincronizadas | Edición de uno sin el otro | Re-ejecutar workflow |
| Fila de .md no aparece en .json | Parseo incompleto | Revisar parser, regenerar |
| JSON tiene filas que no están en .md | Datos residuales | Regenerar desde cero |

---

## 9. Skills invocadas

- (Skill de transformación .md → .json a definir en bloque de Skills)
- `VTT.SKILL-ATTACH-001`

---

**Documento:** `VTT.WORKFLOW-HO-001.019_producir_json_sincronizado.md`
**Versión:** 1.0.0
**Fecha:** 2026-06-01
