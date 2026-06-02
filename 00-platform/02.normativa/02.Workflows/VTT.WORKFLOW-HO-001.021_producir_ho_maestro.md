# VTT.WORKFLOW-HO-001.021 — Producir HO Maestro PM → PJM

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-HO-001.021` |
| **Pertenece a** | `VTT.PROTOCOL-HO-001` §5.5.1 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-06-01 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | PM |
| **Tipo** | [PROCESO] sub-procedimiento orquestador de FASE 5 |

---

## 1. Propósito

PM orquesta la producción del HO Maestro consolidando el upstream técnico completo en un documento que el PJM consume sin necesidad de regresar a preguntar.

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `implementation_plan` | array<path> | FASE 4 | sí | 10 subsecciones del 3B.9 (.md + .json) |
| `routing_index` | path | WORKFLOW-017 | sí | 3B.9.10 completo |
| `paquete_trazabilidad` | path | WORKFLOW-013 | sí | Validación cross-rol consolidada |
| `paquete_3b` | array<path> | FASE 2 | sí | Los 8 docs fundacionales |
| `spec_path` | path | FASE 1 | sí | SPEC del bloque |
| `operativo_proyecto` | path | configuración | sí | UUIDs del equipo |

---

## 3. Precondiciones

- FASE 4 cerrada con 3B.9 v1.4 + Routing Index 100%.
- PAQUETE_TRAZABILIDAD firmado.
- PM tiene acceso a OPERATIVO del proyecto.

---

## 4. Reglas del Workflow

- **R1:** Sin Routing Index 100% → DEVOLVER al TL (gate duro `RULE-HO-001`).
- **R2:** Sin pendientes P0 abiertos → continuar.
- **R3:** Separación matemática del HO obligatoria (R6 del Protocol).
- **R4:** No inventar contenido técnico — todo se cita desde docs upstream.
- **R5:** No duplicar SPECs completas — se referencian, no se inlinean.

---

## 5. Pasos

### Paso 1 — PM ejecuta validación inicial

→ invoca **`VTT.WORKFLOW-HO-001.023_validar_gate_routing_index`**

Si falla → DEVOLVER al TL.

### Paso 2 — PM extrae datos del paquete técnico

Lee subsecciones del 3B.9 + paquete_3b + PAQUETE_TRAZABILIDAD para identificar:
- Contexto del bloque (de 3B.1)
- Alcance incluido/excluido (de SPEC + 3B.9.1)
- Decisiones cerradas D-XX-NN (de 3B.6)
- Módulos, sprints, owners, roles (de 3B.9.9 + 3B.9.3)
- Estimaciones (de 3B.9.6)
- Critical path (de 3B.9.4)
- Paralelismo (de 3B.9.7)
- Gates (de 3B.8)
- Dependencias (de 3B.9.3 4 dimensiones)
- Riesgos (de 3B.9.6)
- Contingencias (de PAQUETE_TRAZABILIDAD)
- Pendientes (de PAQUETE_TRAZABILIDAD)
- Diferidos (de 3B.9.3 ❌ + ⚪ diferidos)
- Reglas de escalación

### Paso 3 — PM clasifica pendientes según severidad

| Tipo | Regla |
|---|---|
| P0 | Impide emitir HO. Resolver antes de continuar. |
| GATE | No impide HO pero bloquea gate futuro. Anotar owner + momento. |
| DIFERIDO | Fuera de alcance actual. Mover a backlog de bloque siguiente. |

Si hay P0 abierto → suspender workflow, regresar a FASE 4 o anterior según la naturaleza.

### Paso 4 — PM aplica regla de separación matemática

Mantiene separados:
- Baseline funcional
- Distribución DB interna
- DevOps OPER
- TL Review (horas)
- AR Audit (horas)
- QA (horas)
- Buffers
- Diferidos

### Paso 5 — PM redacta HO Maestro

→ invoca **`VTT.WORKFLOW-HO-001.022_redactar_secciones_ho_maestro`**

### Paso 6 — PM verifica condición de emisión

| Condición | Estado |
|---|---|
| No hay P0 | ✅ |
| GATE tienen owner y momento | ✅ |
| Diferidos separados | ✅ |
| Routing Index referenciado en §5 | ✅ |
| Sin SPECs duplicadas | ✅ |
| Sin contenido técnico inventado | ✅ |

Si TODAS las condiciones se cumplen → emitir HO.

### Paso 7 — PM ejecuta REVMA sobre HO Maestro

→ invoca **`VTT.WORKFLOW-HO-001.001_ciclo_revma`** (puede ser opcional según política — algunos PMs auto-revisan)

### Paso 8 — PM firma HO Maestro

Documento: `HO_PM_PJM_<BLOQUE>_IMPLEMENTACION_v1.0.md`.

### Paso 9 — PM entrega paquete completo al PJM

→ invoca **`VTT.SKILL-COMMENT-001`**

Paquete entregado al PJM:
1. HO Maestro
2. 3B.9 completo (10 subsecciones .md + .json)
3. Routing Index
4. Metodologías obligatorias (5)
5. Templates obligatorios
6. Guías cross-sprint (3)

---

## 6. Outputs

| Output | Tipo | Destino |
|---|---|---|
| `HO_PM_PJM_<BLOQUE>_IMPLEMENTACION_v1.0.md` | archivo .md | `_project-management/Fases/<BLOQUE>/` |
| Notificación al PJM | comentario formal | VTT |

---

## 7. Validación

- 13-17 secciones presentes según template.
- Routing Index referenciado en §5 con ejemplo concreto.
- Separación matemática aplicada.
- Sin contenido inventado (todo cita upstream).
- Sin SPECs duplicadas.
- Firma PM presente.
- PJM acusó recibo.

---

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| Routing Index incompleto | No se aplicó gate duro | DEVOLVER al TL, no parchear |
| HO contiene contenido inventado | Atajo | Citar desde docs upstream |
| Suma de horas no cuadra | Violación separación matemática | Re-aplicar regla, separar correctamente |
| P0 abierto y HO emitido | Violación R2 | Cancelar emisión, resolver P0 |
| SPEC entera inlineada | Violación R5 | Sustituir por referencia |

---

## 9. Skills invocadas

- `VTT.WORKFLOW-HO-001.022` (redactar secciones)
- `VTT.WORKFLOW-HO-001.023` (gate Routing Index)
- `VTT.WORKFLOW-HO-001.001` (REVMA)
- `VTT.SKILL-COMMENT-001`
- `VTT.SKILL-ATTACH-001`

---

**Documento:** `VTT.WORKFLOW-HO-001.021_producir_ho_maestro.md`
**Versión:** 1.0.0
**Fecha:** 2026-06-01
