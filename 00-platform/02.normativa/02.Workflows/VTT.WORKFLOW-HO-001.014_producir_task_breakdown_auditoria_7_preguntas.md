# VTT.WORKFLOW-HO-001.014 — Producir Task Breakdown + Auditoría 7 Preguntas

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-HO-001.014` |
| **Pertenece a** | `VTT.PROTOCOL-HO-001` §5.4.3, §5.4.5 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-06-01 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | TL |
| **Tipo** | [PROCESO] sub-procedimiento pivote de FASE 4 |

---

## 1. Propósito

TL produce 3B.9.3 Task Breakdown v1.0 — el pivote único del Implementation Plan. Aplica el algoritmo canónico de 7 preguntas técnicas a cada `dep_technical` candidata para evitar bloqueos artificiales.

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `paquete_3b` | array<path> | FASE 2+3 | sí | Los 8 docs 3B + PAQUETE_TRAZABILIDAD |
| `spec_path` | path | FASE 1 | sí | SPEC |
| `analisis_fases_completo` | path | catálogo SDLC | sí | Catálogo 438 deliverables |
| `velocity_historica` | path | proyecto | no | Si existe, se usa para calibrar |
| `template_task_breakdown` | path | templates | sí | Template canónico |

---

## 3. Precondiciones

- FASE 3 cerrada con PAQUETE_TRAZABILIDAD firmado.
- TL tiene acceso a velocity histórica si existe.
- ANALISIS_FASES_COMPLETO disponible.

---

## 4. Reglas del Workflow

- **R1:** TL clasifica cada deliverable como ✅/⚪/❌ con justificación citable.
- **R2:** ❌ debe citar ADR o decisión SPEC que lo justifica.
- **R3:** Las 4 dimensiones de dependencia se declaran SIEMPRE (`dep_technical`, `dep_role`, `gate_release`, `external_blockers`).
- **R4:** Algoritmo de 7 preguntas se aplica a CADA `dep_technical` candidata (no batch, no aproximación).
- **R5:** Prohibido usar `S0X cerrado` en `dep_technical` (RULE-DEP-001).
- **R6:** External_blockers con autor responsable entre paréntesis (RULE-DEP-003).

---

## 5. Pasos

### Paso 1 — TL filtra catálogo SDLC vs scope del bloque

De los 438 deliverables del ANALISIS_FASES_COMPLETO:
- Por cada deliverable de Fase 4-7 (los 191 ejecutables): decide ✅/⚪/❌.
- ✅ aplica en R1, ⚪ opcional, ❌ no aplica con justificación.

### Paso 2 — TL estima cada deliverable ✅/⚪

Por cada deliverable activo:
- Horas estimadas
- SP equivalente (1 SP = 1h por defecto)
- Complejidad LOW/MEDIUM/HIGH/VERY HIGH
- Rol primario

Si `velocity_historica` disponible → calibra contra FV histórica del tipo de deliverable.

### Paso 3 — TL identifica candidatos a dependencia técnica

Por cada deliverable, lista candidatos a dependencia técnica (otros deliverables que parece que se necesitan antes).

### Paso 4 — TL aplica algoritmo de 7 preguntas a cada candidato

Por cada par (deliverable, candidato a dep):

| # | Pregunta | Evidencia |
|---|---|---|
| 1 | ¿Importa tipo/contrato del candidato? | `import`, interfaces |
| 2 | ¿Consume servicio/middleware/policy del candidato? | Llamada, uso en pipeline |
| 3 | ¿Modifica mismo archivo que el candidato? | Path en `archivos_afectados` |
| 4 | ¿Extiende schema con FK al entregable del candidato? | FK Prisma |
| 5 | ¿Depende del orden estricto de migraciones? | Cadena 3B.8 |
| 6 | ¿Consume seed del candidato? | Lookup contra filas seedadas |
| 7 | ¿Monta routes que requieren controllers del candidato? | `routes/index.ts` |

**Decisión:**
- Al menos un SÍ con evidencia → CONSERVAR en `dep_technical`.
- Todos NO → ELIMINAR (es continuidad-rol disfrazada, va a `dep_role`).
- Duda semántica → marcar PENDIENTE TL + documentar pregunta.

### Paso 5 — TL declara las 4 dimensiones por deliverable

| Campo | Contenido |
|---|---|
| `dep_technical` | array de Task IDs que pasaron el algoritmo |
| `dep_role` | array de roles (formato `db_engineer`, `be_auth_agent`, etc.) |
| `gate_release` | identificador del GATE de release (ej. `GATE-S03`) |
| `external_blockers` | array de strings con autor entre paréntesis |

### Paso 6 — TL declara campos de trazabilidad

Por cada deliverable:
- `criterio_aceptacion`
- `evidencia`
- `archivos_afectados`
- `spec_source` (referencia a 3B.X + sección)
- `adr_decision` (si aplica)
- `control_sec` (si aplica)
- `migracion` (si aplica)
- `entregable` (descripción del output esperado)

### Paso 7 — TL produce 3B.9.3 v1.0 en .md

Documento con tabla maestra de deliverables.

### Paso 8 — TL produce 3B.9.3 v1.0 en .json sincronizado

→ invoca **`VTT.WORKFLOW-HO-001.020_emitir_json_task_breakdown`** con (`md_path=3B.9.3_v1.0.md`)

### Paso 9 — TL ejecuta REVMA sobre 3B.9.3 v1.0

→ invoca **`VTT.WORKFLOW-HO-001.001_ciclo_revma`** con (`documento=3B.9.3_v1.0.md`, `agente_generador=TL`, `contexto=[paquete_3b, SPEC, PAQUETE_TRAZABILIDAD]`)

REVMA confirma corrección formal antes de pasar al ciclo iterativo PM/TL.

---

## 6. Outputs

| Output | Tipo | Destino |
|---|---|---|
| `3B.9.3_TASK_BREAKDOWN_v1.0.md` | archivo .md | `_project-management/Fases/<BLOQUE>/` |
| `3B.9.3_TASK_BREAKDOWN_v1.0.json` | archivo .json sincronizado | mismo lugar |

---

## 7. Validación

- Cada deliverable tiene clasificación ✅/⚪/❌.
- ❌ tienen justificación citable.
- Las 4 dimensiones declaradas en cada tarea.
- Algoritmo 7 preguntas aplicado (evidencia trazable).
- Cero `S0X cerrado` en `dep_technical`.
- External_blockers con autor entre paréntesis.
- .md y .json sincronizados.
- REVMA aprobado.

---

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| `dep_technical` incluye continuidad-rol (todas las preguntas NO) | No se aplicó algoritmo | Re-auditar, eliminar |
| ❌ sin justificación | Atajo | Citar ADR/SPEC |
| External_blocker sin autor | Olvido | Agregar `(PM)` o quien resuelve |
| Más de 5 deps por tarea | Tarea demasiado amplia | Considerar partir en sub-tareas |
| .json desincronizado con .md | Fallo manual | Re-ejecutar WORKFLOW-020 |

---

## 9. Skills invocadas

- `VTT.WORKFLOW-HO-001.020` (emitir JSON)
- `VTT.WORKFLOW-HO-001.001` (REVMA)
- `VTT.SKILL-ATTACH-001`

---

**Documento:** `VTT.WORKFLOW-HO-001.014_producir_task_breakdown_auditoria_7_preguntas.md`
**Versión:** 1.0.0
**Fecha:** 2026-06-01
