# DECISIONES — Criteria System: Gaps Q1-Q7
## Respuestas del SA a las preguntas del PM sobre el modelo de DoD/DoR/AC

**Solicitado por:** PM Memory Service
**Respondido por:** SA Ejecutor (`0c128e3b-db3b-4e31-b107-0379b5791233`)
**Fecha:** 2026-05-06
**Estado:** Pendiente aprobación PM + AR
**Referencia:** PROPUESTA_CRITERIA_TRAZABILIDAD_VTT.md

---

## Contexto

El análisis de MS-024 (Acceptance Criteria) produjo 144 criterios mapeados al modelo VTT V4. Al evaluar la implementación, el PM identificó 7 gaps de diseño (G1-G7) que se traducen en 7 preguntas (Q1-Q7). Este documento formaliza las respuestas del SA para que no se pierdan en el chat.

---

## Q1 — ¿DoD item se puede desactivar por tarea individual?

**Gap:** G1 — ¿Qué pasa si un DoD item no aplica a una tarea específica?

**Decisión:** Sí, solo PM/TL pueden desactivar un DoD item en una tarea específica.

**Justificación:** Si cualquier rol desactiva, el DoD se erosiona. Si nadie puede, hay fricción cuando un criterio genuinamente no aplica (ej: DOD-BE-07 "Idempotencia verificada" no aplica a un endpoint GET de solo lectura).

**Modelo de datos:**

```
task_criteria (tabla existente, campos nuevos)
├── isApplicable: Boolean (default: true)
├── disabledReason: String? (obligatorio si isApplicable=false)
└── disabledBy: UUID? (FK → users, solo PM/TL)
```

**Reglas:**
- Default: todos los DoD items aplican (`isApplicable=true`)
- Solo roles PM o TL pueden cambiar `isApplicable` a `false`
- Al desactivar, `disabledReason` es obligatorio (trazabilidad)
- Items desactivados no se evalúan en el review gate
- Items desactivados siguen visibles en la tarea (no se borran) con indicador visual

---

## Q2 — ¿Quién puede modificar templates DoD/DoR?

**Gap:** G2 — Roles autorizados para CRUD de templates.

**Decisión:** PM + AR gestionan templates de proyecto. Admin VTT gestiona templates globales.

**Justificación:** Los templates son el estándar de calidad. El PM los gestiona desde perspectiva de proceso, el AR los valida desde perspectiva técnica. El Admin controla los globales para garantizar consistencia entre proyectos.

**Matriz de permisos:**

| Operación | Template global | Template de proyecto |
|-----------|----------------|---------------------|
| Crear | Admin VTT | PM, AR |
| Editar | Admin VTT | PM, AR |
| Desactivar | Admin VTT | PM |
| Ver | Todos | Todos los miembros del proyecto |

**Implementación:** Validación de rol en los endpoints CRUD de `criteria_template`. El campo `scope` (global/project) determina qué permisos aplican.

---

## Q3 — ¿Gherkin AC son editables post-aprobación?

**Gap:** G3 — Mutabilidad de AC una vez aprobados.

**Decisión:** Solo agregar, no modificar. Los AC originales se congelan; se pueden agregar nuevos y deprecar existentes.

**Justificación:** Si son completamente editables, se pierde trazabilidad del contrato SA→QA. Si son inmutables, no se puede corregir un error. El punto medio: congelar originales, permitir agregar, deprecar con historial.

**Modelo de datos:**

```
task_criteria.acStatus: Enum
├── "active"                — AC original, vigente
├── "deprecated"            — AC reemplazado (no se evalúa, queda como historial)
├── "added_post_approval"   — AC agregado después de aprobación
└── "superseded_by"         — UUID del AC que lo reemplaza (si deprecated)
```

**Reglas:**
- AC con `acStatus=active` no se puede editar (campos description, code congelados)
- Para corregir un AC: deprecar el original (`acStatus=deprecated`, `supersededBy=nuevo_id`) y crear uno nuevo (`acStatus=added_post_approval`)
- Los AC `deprecated` no cuentan en el review gate pero son visibles en historial
- Solo SA Reviewer o PM pueden deprecar un AC
- Cualquier rol autorizado puede agregar AC nuevos post-aprobación

**Ejemplo de flujo:**

```
1. AC-US-001-1 (active) — "Import exitoso retorna HTTP 201"
2. QA descubre que debería ser HTTP 200 (por idempotencia)
3. SA depreca AC-US-001-1 → acStatus=deprecated, supersededBy=AC-US-001-1b
4. SA crea AC-US-001-1b (added_post_approval) — "Import exitoso retorna HTTP 200"
5. Historial preservado: AC-US-001-1 → deprecated → AC-US-001-1b
```

---

## Q4 — ¿Cambio en template DoD afecta tareas existentes?

**Gap:** G4 — Versionamiento de templates.

**Decisión:** Configurable por el PM al momento de modificar el template.

**Justificación:** Retroactivo puro es peligroso (puede romper tareas en progreso). Solo nuevas es insuficiente (si descubrís un DoD crítico faltante, querés que aplique). La solución es que el PM decide el alcance del cambio.

**Opciones al modificar template:**

| applyTo | Descripción | Cuándo usarlo |
|---------|-------------|---------------|
| `new_only` | Solo tareas creadas después del cambio | Refinamiento menor, mejora incremental |
| `pending` | Tareas en pending/ready que aún no empezaron | DoD crítico descubierto, tareas no iniciadas |
| `all_active` | Todas las tareas excepto completed/approved | Corrección de error en DoD existente |

**Modelo de datos:**

```
criteria_template_history
├── id: UUID (PK)
├── templateId: UUID (FK → criteria_template)
├── previousDescription: String
├── newDescription: String
├── applyTo: Enum("new_only", "pending", "all_active")
├── changedBy: UUID (FK → users)
├── changedAt: DateTime
└── reason: String
```

**Reglas:**
- Default: `new_only` (menos riesgo)
- `all_active` requiere confirmación explícita (campo `confirmed: true` en el request)
- Cada cambio queda en `criteria_template_history` con before/after
- Si `applyTo=pending`, el sistema busca tareas con `status IN (task_pending, task_defined)` y agrega/actualiza el criterio
- Si `applyTo=all_active`, excluye `task_completed` y `task_approved`

---

## Q5 — ¿Quién marca fulfillment de DoD?

**Gap:** G5 — El SA dice "DoD checklist" pero no quién lo marca.

**Decisión:** Flujo dual — agente reporta, TL/reviewer verifica.

**Justificación:** Si solo el agente marca, se auto-certifica sin validación. Si solo TL marca, se crea bottleneck. El flujo dual: el agente aporta evidencia, el reviewer valida.

**Modelo de datos:**

```
task_criteria.fulfillmentStatus: Enum
├── "pending"    — criterio aún no evaluado
├── "reported"   — agente ejecutor reporta cumplimiento con evidencia
├── "verified"   — TL/reviewer confirma que se cumple
└── "rejected"   — TL/reviewer rechaza con comentario
```

```
task_criteria_fulfillment (tabla nueva o campos en task_criteria)
├── reportedBy: UUID? — agente que reportó
├── reportedAt: DateTime?
├── reportEvidence: String? — evidencia del agente
├── verifiedBy: UUID? — reviewer que verificó
├── verifiedAt: DateTime?
├── verificationComment: String? — comentario del reviewer
└── rejectionReason: String? — razón si rejected
```

**Flujo:**

```
Agente ejecutor termina su trabajo
  │
  ├─ Marca cada DoD item como "reported" con evidencia
  │  POST /api/tasks/:id/criteria/:criteriaId/fulfill
  │  { "status": "reported", "evidence": "Endpoint probado con curl, screenshot adjunto" }
  │
  ├─ Mueve tarea a task_in_review
  │
  └─ TL/Reviewer revisa:
     │
     ├─ Si todo OK → marca como "verified"
     │  POST /api/tasks/:id/criteria/:criteriaId/verify
     │  { "status": "verified", "comment": "Confirmado" }
     │
     └─ Si falla → marca como "rejected"
        POST /api/tasks/:id/criteria/:criteriaId/verify
        { "status": "rejected", "reason": "Test unitario no cubre edge case X" }
        → Tarea vuelve a task_in_progress para corrección
```

**Reglas de transición de tarea:**
- Para mover a `task_in_review`: todos los DoD items deben estar en `reported` (mínimo)
- Para mover a `task_completed`: todos los DoD items deben estar en `verified`
- Si algún DoD queda en `rejected`: tarea no puede pasar a `task_completed`

---

## Q6 — ¿Test Scenarios son criterios o entidad separada?

**Gap:** G6 — Naturaleza de los Test Scenarios en el modelo.

**Decisión:** Criterios en tarea QA, con campos extendidos de testing.

**Justificación:** Los Test Scenarios ya tienen todo lo que necesitan del modelo de criteria (code, description, status, fulfillment). Crear una entidad separada duplica funcionalidad. Lo que sí necesitan son campos adicionales para capturar resultado de ejecución.

**Campos extendidos para criteria de tipo testing:**

```
task_criteria (campos adicionales, nullable, solo aplican a testing)
├── testResult: Enum?("pass", "fail", "blocked", "skipped")
├── executedAt: DateTime?
├── executedBy: UUID?
├── evidence: String? — link a screenshot, log, video
├── defectId: UUID? (FK → trackable_items WHERE typeCode='bug') — si fail, link al bug
└── executionNotes: String?
```

**Flujo QA:**

```
1. SA crea Test Scenarios como criteria tipo "functional" en tarea QA
2. QA ejecuta cada escenario
3. QA registra resultado:
   POST /api/tasks/:taskId/criteria/:criteriaId/fulfill
   {
     "status": "met",          // o "not_met"
     "testResult": "pass",     // o "fail", "blocked"
     "evidence": "logs/TS-01-5-race.log",
     "executedAt": "2026-05-20T10:00:00Z"
   }
4. Si fail → QA crea Bug como trackable item y vincula:
   { "defectId": "uuid-del-bug" }
```

**R2 (si se necesita):** Si el volumen de testing crece, se puede crear una entidad `test_execution` separada que vincule a criteria. Pero para R1, los campos extendidos en criteria son suficientes.

---

## Q7 — ¿projectTypeCode de Memory Service?

**Gap:** G7 — Determina qué templates globales hereda.

**Decisión:** `software`.

**Justificación:** Memory Service es un microservicio Node.js + TypeScript + PostgreSQL. Es un proyecto de software estándar. La distinción microservicio vs monolito vs librería no afecta los DoD/DoR (todos necesitan "compila TS", "tests pasan", "PR creado").

**Implicación:** Memory Service hereda todos los templates globales con `projectTypeCode=software`. Los templates específicos del proyecto (BR-006 "máquina de estados", BR-007 "idempotencia") se agregan como scope=project.

**Si en el futuro** hay diferencias reales entre tipos de proyectos software (ej: un proyecto Python tiene DoD diferentes a uno TypeScript), se puede subdividir el catálogo: `software-node`, `software-python`. Hoy no es necesario.

---

## Resumen de Decisiones

| Q | Decisión | Impacto en BD |
|---|----------|---------------|
| Q1 | PM/TL desactivan DoD por tarea con reason | `isApplicable`, `disabledReason`, `disabledBy` en task_criteria |
| Q2 | PM+AR proyecto, Admin global | Permisos por rol en CRUD template |
| Q3 | Solo agregar, no modificar. Deprecar con historial | `acStatus`, `supersededBy` en task_criteria |
| Q4 | Configurable: new_only / pending / all_active | `criteria_template_history` tabla nueva |
| Q5 | Agente reporta → TL verifica | `fulfillmentStatus` (reported/verified/rejected), campos de fulfillment |
| Q6 | Criterios en tarea QA con campos de testing | `testResult`, `executedAt`, `evidence`, `defectId` en task_criteria |
| Q7 | `software` | Sin cambios — ya existe |

---

## Impacto Acumulado en el Modelo

### Campos nuevos en `task_criteria` (tabla existente)

```
task_criteria
├── ... (campos existentes)
├── isApplicable: Boolean (default: true)          — Q1
├── disabledReason: String?                         — Q1
├── disabledBy: UUID?                               — Q1
├── acStatus: Enum (active/deprecated/added_post_approval) — Q3
├── supersededBy: UUID?                             — Q3
├── fulfillmentStatus: Enum (pending/reported/verified/rejected) — Q5
├── reportedBy: UUID?                               — Q5
├── reportedAt: DateTime?                           — Q5
├── reportEvidence: String?                         — Q5
├── verifiedBy: UUID?                               — Q5
├── verifiedAt: DateTime?                           — Q5
├── verificationComment: String?                    — Q5
├── rejectionReason: String?                        — Q5
├── testResult: Enum?(pass/fail/blocked/skipped)    — Q6
├── executedAt: DateTime?                           — Q6
├── executedBy: UUID?                               — Q6
├── evidence: String?                               — Q6
├── defectId: UUID?                                 — Q6
└── executionNotes: String?                         — Q6
```

### Tablas nuevas

```
criteria_template              — P1 (propuesta anterior)
criteria_template_history      — Q4
```

### Estimación de esfuerzo adicional (sobre las 30-34h de la propuesta anterior)

| Decisión | Esfuerzo adicional |
|----------|-------------------|
| Q1 (isApplicable) | +2h (migration + validación) |
| Q3 (acStatus + deprecation) | +4h (lógica de deprecation + historial) |
| Q4 (template history) | +4h (tabla + lógica de applyTo) |
| Q5 (fulfillment dual) | +6h (flujo reported→verified, validación en transiciones) |
| Q6 (campos testing) | +3h (migration + endpoints de test execution) |
| **Total adicional** | **+19h** |

### Esfuerzo total (propuesta + decisiones)

| Bloque | Horas |
|--------|-------|
| P1-P4 (propuesta original) | 30-34h |
| Q1-Q6 (decisiones de gaps) | +19h |
| **Total** | **49-53h** |

---

## Próximo Paso

Estas decisiones necesitan aprobación del PM y validación técnica del AR/TL antes de implementarse. Una vez aprobadas, el TL puede crear las tareas de implementación en VTT para el proyecto VTT (no Memory Service — estas mejoras son al sistema VTT mismo).

---

**Documento:** DECISIONES_CRITERIA_SYSTEM_Q1-Q7.md
**Versión:** 1.0
**Fecha:** 2026-05-06
**Para:** PM, AR, TL
