# VTT.WORKFLOW-HO-001.030 — Producir INDEX_PAQUETE_OPERATIVO_<BLOQUE>

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-HO-001.030` |
| **Pertenece a** | `VTT.PROTOCOL-HO-001` §5.6.10 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-06-01 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | PJM |
| **Tipo** | [PROCESO] sub-procedimiento de cierre de FASE 6 |

---

## 1. Propósito

PJM produce el documento síntesis del bloque que indexa todos los sprints generados y sirve como punto de entrada del TL al paquete operativo completo. Es el último artefacto antes de entregar al TL.

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `paquete_operativo` | array<path> | WORKFLOWS 026-029 | sí | Todos los SETUP, HANDOFF, CLOSURE del bloque |
| `analisis_scope` | path | WORKFLOW-025 | sí | Roles activos y dependencias por sprint |
| `ho_maestro` | path | WORKFLOW-021 | sí | HO Maestro PM → PJM |

---

## 3. Precondiciones

- Todos los sprints del bloque tienen SETUP, CLOSURE y N handoffs producidos.
- Tareas de calidad inyectadas (WORKFLOW-029).

---

## 4. Reglas del Workflow

- **R1:** INDEX_PAQUETE_OPERATIVO es punto de entrada único del TL.
- **R2:** Lista TODOS los sprints del bloque, no solo los del primer ciclo.
- **R3:** Cita rutas exactas de cada documento producido.
- **R4:** Incluye orden de ejecución sugerido para el TL.

---

## 5. Pasos

### Paso 1 — PJM identifica todos los sprints del bloque

Lista de sprints según Capacity Plan (S00, S01, ..., S0N).

### Paso 2 — PJM produce sección "Resumen del Bloque"

- Nombre del bloque
- Total de sprints
- Roles activos por sprint (matriz)
- Total de horas estimadas del bloque
- Milestones del bloque

### Paso 3 — PJM produce sección "Documentos por Sprint"

Por cada sprint:
- SETUP_S[N].md (ruta)
- N handoffs por rol activo del sprint (rutas)
- CLOSURE_S[N].md (ruta)
- JSONs sincronizados

### Paso 4 — PJM produce sección "Orden de Ejecución del TL"

Secuencia sugerida:
```
1. Leer INDEX_PAQUETE_OPERATIVO (este doc)
2. Leer HO Maestro
3. Para S00:
   a. Ejecutar SETUP_S00.md (crea estructura VTT del sprint)
   b. Llenar CONTEXTO_S00.md con UUIDs reales devueltos
   c. Asignar tareas a agentes según HANDOFF_<ROL>_S00
4. Cuando S00 cierra (firma APR-S00):
   a. Pasar a S01
   ...
```

### Paso 5 — PJM produce sección "Tareas de Calidad Inyectadas"

Síntesis de tareas inyectadas por WORKFLOW-029 por familia y por sprint.

### Paso 6 — PJM produce sección "Metodologías y Guías de Referencia"

Lista de las 5 metodologías + 3 guías cross-sprint con rutas. Son inputs estables del TL durante toda la ejecución.

### Paso 7 — PJM produce sección "Gates de Release"

Tabla `GATE-S0X` → criterios → quién lo libera (DevOps + PM).

### Paso 8 — PJM produce sección "External Blockers Activos"

Lista de external_blockers del Task Breakdown que aún no se han resuelto.

PM debe monitorearlos y resolverlos antes de que se vuelvan críticos.

### Paso 9 — PJM produce INDEX_PAQUETE_OPERATIVO_<BLOQUE>.md

Documento síntesis completo.

### Paso 10 — PJM produce JSON sincronizado

→ invoca **`VTT.WORKFLOW-HO-001.019`**

### Paso 11 — PJM ejecuta REVMA sobre INDEX

→ invoca **`VTT.WORKFLOW-HO-001.001`** con SA o PM Revisor.

### Paso 12 — PJM presenta paquete operativo completo al PM

PJM envía mensaje al PM con:
- Ruta del INDEX
- Resumen del bloque
- Confirmación de que todos los sprints están documentados

→ invoca **`VTT.SKILL-COMMENT-001`**.

### Paso 13 — PM aprueba o pide ajustes

→ **[DECISIÓN]**
- **APROBADO** → continuar a Paso 14.
- **AJUSTES** → PJM aplica observaciones, vuelve a sprint específico (WORKFLOWS 026/027/028/029) según corresponda.

### Paso 14 — PJM entrega al TL

PJM redacta mensaje formal al TL con:
- Ruta del INDEX_PAQUETE_OPERATIVO
- Confirmación de paquete completo
- Recordatorio: `ASG-001` arranca cuando TL acuse recibo.

→ invoca **`VTT.SKILL-COMMENT-001`** al TL.

### Paso 15 — TL acusa recibo

TL confirma recepción del paquete completo y que no necesita aclaraciones.

→ invoca **`VTT.SKILL-COMMENT-001`** del TL al PJM/PM.

**FIN DE FASE 6 — FIN DEL PROTOCOL-HO-001.**

---

## 6. Outputs

| Output | Tipo | Destino |
|---|---|---|
| `INDEX_PAQUETE_OPERATIVO_<BLOQUE>.md` | archivo .md | `_project-management/Fases/<BLOQUE>/Sprints/` |
| `INDEX_PAQUETE_OPERATIVO_<BLOQUE>.json` | archivo .json sincronizado | mismo lugar |
| Acuse de recibo del TL | comentario formal | VTT |

---

## 7. Validación

- INDEX cubre 100% de sprints del bloque.
- Orden de ejecución del TL claro y ejecutable.
- Metodologías + guías referenciadas con rutas.
- Gates de release listados.
- External blockers activos identificados.
- PM aprobó.
- TL acusó recibo.

---

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| Falta sprint en INDEX | Olvido | Agregar |
| Rutas rotas | Edición posterior | Verificar antes de entregar |
| TL pregunta algo después del acuse | Paquete incompleto | Aceptar gap, agregar a próximo bloque |
| External blockers no listados | Olvido | Listar todos los activos |

---

## 9. Skills invocadas

- `VTT.WORKFLOW-HO-001.019` (sincronización JSON)
- `VTT.WORKFLOW-HO-001.001` (REVMA)
- `VTT.SKILL-COMMENT-001`
- `VTT.SKILL-ATTACH-001`

---

**Documento:** `VTT.WORKFLOW-HO-001.030_producir_index_paquete_operativo.md`
**Versión:** 1.0.0
**Fecha:** 2026-06-01
