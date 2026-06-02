# VTT.WORKFLOW-HO-001.020 — Emitir JSON Canónico del Task Breakdown

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-HO-001.020` |
| **Pertenece a** | `VTT.PROTOCOL-HO-001` §5.4.7 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-06-01 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | TL |
| **Tipo** | [PROCESO] sub-procedimiento de FASE 4 (caso específico de WORKFLOW-019) |

---

## 1. Propósito

Caso especializado de WORKFLOW-019 enfocado en el Task Breakdown — la subsección más crítica del 3B.9 para downstream (HO Maestro + paquete operativo + materialización futura).

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `task_breakdown_md` | path | WORKFLOW-014 o WORKFLOW-015 | sí | Archivo .md del Task Breakdown |
| `schema_task_breakdown` | path | configuración | sí | JSON Schema validador |

---

## 3. Precondiciones

- `task_breakdown_md` existe con versión declarada.
- Schema validador disponible.

---

## 4. Reglas del Workflow

- **R1:** JSON incluye TODAS las 4 dimensiones de dependencia.
- **R2:** Campos `_raw` (string original tal como aparece en el .md) son OPCIONALES y solo para auditoría.
- **R3:** Sistema VTT consume campos parseados (arrays, no strings).
- **R4:** `dep_technical` debe ser array de Task IDs válidos (existentes en el mismo Task Breakdown).
- **R5:** `external_blockers` debe ser array de strings con autor entre paréntesis.

---

## 5. Pasos

### Paso 1 — TL parsea tabla maestra del Task Breakdown .md

Por cada fila de tabla → objeto JSON con schema canónico:

```json
{
  "task_id": "TSK-S02-R1-01",
  "sprint": "S02",
  "nodo": "R1",
  "modulo": "RBAC",
  "titulo": "Organization.ownerId + OrganizationMember + migración R1",
  "owner": "DB",
  "rol": "DB",
  "esfuerzo": "3h",
  "esfuerzo_horas": 3,
  "complejidad": "MEDIUM",
  "aplica": "✅",

  "dep_technical": ["TSK-S01-A1-01"],
  "dep_role": ["db_engineer"],
  "gate_release": "GATE-S02",
  "external_blockers": [],

  "criterio_aceptacion": "...",
  "evidencia": "...",
  "archivos_afectados": ["prisma/schema.prisma", "migrations/m-r1.sql"],
  "spec_source": "3B.3 v1.2",
  "seccion": "§3.5",
  "adr_decision": "D-RBAC-10",
  "control_sec": "SEC-C-21, SEC-C-59",
  "migracion": "M-R1",
  "entregable": "Migración R1"
}
```

### Paso 2 — TL valida cada objeto contra schema

Validación de schema verifica:
- Campos requeridos presentes.
- Tipos correctos (string, array, number, etc.).
- Enums respetados (`aplica` ∈ {✅, ⚪, ❌}, `complejidad` ∈ {LOW, MEDIUM, HIGH, VERY HIGH}).

### Paso 3 — TL valida referencias internas

Por cada Task ID en `dep_technical`:
- Verifica que ese Task ID existe en el mismo Task Breakdown.
- Si no existe → error.

### Paso 4 — TL valida convenciones críticas

- Ningún `dep_technical` contiene frase "S0X cerrado" (`RULE-DEP-001`).
- Todos los `external_blockers` tienen autor entre paréntesis (`RULE-DEP-003`).
- Cada `gate_release` referencia un gate definido en plan de rollout (3B.8).

### Paso 5 — TL escribe `task_breakdown_<version>.json`

Path: paralelo al .md con misma versión.

### Paso 6 — TL ejecuta diff con .md

Verifica que .json tiene misma cantidad de tareas que el .md.

---

## 6. Outputs

| Output | Tipo | Destino |
|---|---|---|
| `3B.9.3_TASK_BREAKDOWN_<version>.json` | archivo .json | mismo lugar que .md |

---

## 7. Validación

- JSON pasa schema validator.
- Referencias internas válidas (todos los Task IDs en `dep_technical` existen).
- Convenciones críticas respetadas (R3, R4, R5).
- Misma cantidad de tareas que el .md.

---

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| `dep_technical` referencia Task ID inexistente | Error de tipeo o tarea eliminada del .md | Verificar contra .md, corregir |
| `external_blocker` sin autor | Violación R5 | Agregar autor entre paréntesis |
| `S0X cerrado` en `dep_technical` | Violación R4 + `RULE-DEP-001` | Mover a `gate_release` |
| Schema validation falla | Campo faltante o tipo equivocado | Completar .md, regenerar |

---

## 9. Skills invocadas

- (Skill de parseo .md → JSON a definir)
- (Skill de validación JSON Schema a definir)
- `VTT.SKILL-ATTACH-001`

---

**Documento:** `VTT.WORKFLOW-HO-001.020_emitir_json_task_breakdown.md`
**Versión:** 1.0.0
**Fecha:** 2026-06-01
