# VTT.WORKFLOW-HO-001.007 — Producir 3B.1 Solution Architecture

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-HO-001.007` |
| **Pertenece a** | `VTT.PROTOCOL-HO-001` §5.2.3 (rol AR) |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-06-01 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | AR (productor primario), TL (co-productor) |
| **Tipo** | [PROCESO] sub-procedimiento de FASE 2 |

---

## 1. Propósito

Producir el documento 3B.1 Solution Architecture — raíz del paquete técnico fundacional. Define componentes, tech stack, integraciones y data flow del bloque. Es input obligatorio para todos los demás 3B.X.

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `spec_path` | path | FASE 1 aprobada | sí | SPEC del bloque |
| `metodologia_path` | path | FASE 1 aprobada | sí | METODOLOGIA del bloque |
| `docs_sinteticos` | array<path> | WORKFLOW-005 (si camino C) | no | Docs 3B sintéticos producidos |
| `docs_actuales` | array<path> | WORKFLOW-006 (si camino C) | no | Docs `3B.X_actual_*` |

---

## 3. Precondiciones

- FASE 1 completa con SPEC + METODOLOGIA aprobadas.
- Camino confirmado en DECISION_BLOQUE.
- AR está en cadena de roles.

---

## 4. Reglas del Workflow

- **R1:** 3B.1 NO contradice ninguna decisión cerrada de SPEC.
- **R2:** Diagramas C4 (L1, L2, L3) son obligatorios.
- **R3:** Tech stack se justifica contra requisitos NFR de SPEC.
- **R4:** Integraciones externas se documentan con contrato (input/output esperados).
- **R5:** En camino C, 3B.1 refleja el sistema completo (estado actual + delta de la feature), no solo lo nuevo.

---

## 5. Pasos

### Paso 1 — AR lee SPEC + METODOLOGIA aprobadas

AR identifica:
- Componentes lógicos requeridos
- Tech stack propuesto/restricciones
- Integraciones con sistemas externos
- Restricciones NFR (performance, security, scalability)

### Paso 2 — AR diseña arquitectura de solución

AR produce diagramas:
- C4 Nivel 1 — System Context (sistema en su entorno)
- C4 Nivel 2 — Container (componentes principales)
- C4 Nivel 3 — Component (zoom dentro de containers críticos)

### Paso 3 — AR documenta tech stack

Para cada componente, AR declara:
- Lenguaje + framework
- Librerías clave
- Justificación contra NFR (ej. "Node 20 + Express porque NFR-PERF-01 SLA <500ms y el equipo tiene velocity histórica con ese stack")

### Paso 4 — AR documenta integraciones

Por cada integración externa:
- Sistema con el que se integra
- Tipo de integración (REST sync, webhook async, event bus)
- Contrato (request/response)
- Manejo de fallos

### Paso 5 — AR ejecuta ciclo REVMA sobre 3B.1

→ invoca **`VTT.WORKFLOW-HO-001.001_ciclo_revma`** con (`documento=3B.1_SOLUTION_ARCHITECTURE.md`, `agente_generador=AR`, `contexto=[SPEC, METODOLOGIA]`)

### Paso 6 — AR firma 3B.1 cuando REVMA emite APROBADO

Documento queda versionado y disponible como input para 3B.2..3B.8.

---

## 6. Outputs

| Output | Tipo | Destino |
|---|---|---|
| `3B.1_SOLUTION_ARCHITECTURE.md` | archivo .md | `_project-management/Fases/<BLOQUE>/` |
| Diagramas C4 L1/L2/L3 | incluidos en .md (mermaid) o exportados | mismo lugar |

---

## 7. Validación

- 3B.1 contiene C4 L1, L2 y L3 (los 3 niveles).
- Tech stack justificado contra NFR.
- Integraciones con contrato declarado.
- Ciclo REVMA cerrado con APROBADO.
- Versionado correctamente.

---

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| 3B.1 contradice ADR existente en SPEC | No se leyó SPEC completa | Backfeed a FASE 1 o ajustar 3B.1 |
| Diagramas C4 incompletos | AR saltó niveles | Producir los 3 niveles antes de REVMA |
| Tech stack sin justificación | "Es lo que conocemos" | Justificar contra NFR específicos |
| 3 vueltas REVMA por temas cosméticos | PM Revisor mal calibrado | Cortar ciclo según R4 de WORKFLOW-001 |

---

## 9. Skills invocadas

- `VTT.WORKFLOW-HO-001.001` (REVMA — invocado en Paso 5)
- `VTT.SKILL-ATTACH-001` (subir al sistema)

---

**Documento:** `VTT.WORKFLOW-HO-001.007_producir_3b1_solution_architecture.md`
**Versión:** 1.0.0
**Fecha:** 2026-06-01
