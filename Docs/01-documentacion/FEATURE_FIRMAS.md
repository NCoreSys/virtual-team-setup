# FEATURE: FIRMAS Y APROBACIONES

| Campo | Valor |
|-------|-------|
| **Feature** | Firmas y Aprobaciones |
| **Versión** | 1.0 |
| **Fecha** | 2026-04-12 |
| **Sprint origen** | S08 |
| **Estado** | ✅ Implementado (BE/DB) |

---

## 1. QUÉ ES

Sistema de firmas en cascada para documentar formalmente que cada etapa del proyecto fue completada y revisada. Opera en tres niveles: Stage (fase dentro de sprint), Sprint, y Release.

---

## 2. PARA QUÉ SIRVE

- **Audit trail** — Registro de quién aprobó qué y cuándo
- **Accountability** — Cada rol tiene responsabilidad formal sobre su trabajo
- **Cierre formal** — Marca el fin de una etapa para efectos de métricas y reporting
- **Calidad** — Fuerza revisiones antes de cerrar

---

## 3. PRECONDICIONES

### Para que el sistema de firmas funcione, debe existir:

| Precondición | Tabla/Entidad | ¿Existe? |
|--------------|---------------|----------|
| Proyecto creado | `projects` | ✅ |
| Release creado | `releases` | ✅ |
| Sprint creado (si aplica) | `sprints` | ✅ |
| Tareas asignadas a fases | `tasks` con `phaseId` | ✅ |
| Usuarios/Agentes registrados | `users` | ✅ |
| Catálogo de fases | `phase_catalog` | ✅ |

### Seeds necesarios:

Ninguno específico para firmas. Las tablas de aprobación se llenan durante el uso.

---

## 4. CÓMO SE ACTIVA

### ¿Quién inicia el proceso de firmas?

**Nadie lo "inicia" explícitamente.** El proceso de firmas se activa automáticamente cuando:

| Nivel | Se activa cuando... |
|-------|---------------------|
| Stage | Un agente completa todas sus tareas en una fase del sprint |
| Sprint | Todos los stages del sprint están firmados |
| Release | Todos los sprints del release están firmados |

### ¿Hay que configurar algo?

**Al crear el proyecto/release/sprint:**

| Configuración | Dónde | Default |
|---------------|-------|---------|
| `sprintEnabled` | Proyecto | `true` para Scrum, `false` para Kanban |
| `externalApprovalRequired` | Release | `false` |
| `requiredSigners` | `flow_phase_config` | Según template de flujo |

---

## 5. FLUJO OPERATIVO

### 5.1 NIVEL 1: FIRMA DE STAGE

#### ¿Qué es un Stage?

Un stage = una **fase específica** dentro de un **sprint específico**.

Ejemplo: Sprint S05 tiene tareas en fase Development y fase Testing. Eso son 2 stages:
- `S05-development`
- `S05-testing`

#### Actores

Los **agentes que ejecutaron tareas** en ese stage.

#### Paso a paso

```
PASO 1: Agente completa su última tarea del stage
─────────────────────────────────────────────────
El agente termina de trabajar. Todas sus tareas en ese stage 
están en status "completed".

PASO 2: Agente verifica precondiciones
─────────────────────────────────────────────────
Antes de firmar, el agente verifica:

☐ ¿Todas MIS tareas en este stage están "completed"?
☐ ¿Marqué todos los criterios de aceptación?
☐ ¿Resolví todos los devlog entries critical/high?
☐ ¿Ejecuté hardcode check (si aplica a mis tareas)?

PASO 3: Agente solicita firmar
─────────────────────────────────────────────────
POST /api/sprints/:sprintId/stages/:phaseCode/sign

El sistema valida automáticamente las precondiciones.

PASO 4: Sistema responde
─────────────────────────────────────────────────
SI PASA:
  → Stage firmado para este agente
  → Se registra: quién, cuándo, qué tareas

SI FALLA:
  → Error 422 con detalle de qué falta
  → Agente corrige y reintenta
```

#### Request

```
POST /api/sprints/:sprintId/stages/:phaseCode/sign
```

```json
{
  "comments": "Todas las tareas de DB completadas. Migraciones aplicadas."
}
```

#### Response (éxito)

```json
{
  "id": "uuid-approval",
  "sprintId": "uuid-sprint",
  "phaseCode": "development",
  "signedBy": "uuid-db-agent",
  "signedAt": "2026-04-12T10:00:00Z",
  "tasksIncluded": [
    { "id": "uuid-task-1", "title": "Crear migración users" },
    { "id": "uuid-task-2", "title": "Crear migración payments" }
  ],
  "comments": "Todas las tareas de DB completadas. Migraciones aplicadas."
}
```

#### Response (error)

```json
{
  "statusCode": 422,
  "message": "Cannot sign stage - pending items",
  "errors": [
    {
      "type": "task_not_completed",
      "taskId": "uuid",
      "title": "Crear índices en payments",
      "currentStatus": "in_progress"
    },
    {
      "type": "devlog_pending",
      "entryId": "uuid",
      "severity": "critical",
      "title": "Esperando migración de Admin"
    }
  ]
}
```

#### ¿Cuándo está el stage completamente firmado?

Cuando **TODOS los agentes** que tienen tareas en ese stage han firmado.

```
Stage: S05-development

Agentes con tareas:
  ✅ DB-Agent: firmó
  ✅ BE-Agent: firmó
  ⬜ FE-Agent: pendiente

Estado del stage: PARCIALMENTE FIRMADO

Cuando FE-Agent firme → Estado: COMPLETAMENTE FIRMADO
```

---

### 5.2 NIVEL 2: FIRMA DE SPRINT

#### Actores

| Rol | Obligatorio | Qué valida |
|-----|-------------|------------|
| TL (Team Lead) | ✅ Sí | Code review, integration |
| AR (Architect) | ✅ Sí | Arquitectura, ADRs |
| QA | ✅ Sí | Tests, bugs |
| DL (Designer) | Solo si hubo FE | UX, diseño |

#### Paso a paso

```
PASO 1: Sistema detecta que todos los stages están firmados
─────────────────────────────────────────────────────────────
Automático. No requiere acción.

PASO 2: Sistema notifica a firmantes del sprint
─────────────────────────────────────────────────────────────
TL, AR, QA (y DL si aplica) reciben notificación de que 
pueden firmar el sprint.

PASO 3: Cada firmante hace su revisión
─────────────────────────────────────────────────────────────
TL revisa:
  ☐ Todos los PRs mergeados
  ☐ Integration tests pasan
  ☐ No hay blockers pendientes
  ☐ Scope del sprint completado

AR revisa:
  ☐ Code review de PRs
  ☐ Arquitectura consistente
  ☐ ADRs documentados (si hubo decisiones)
  ☐ No hay tech debt crítica

QA revisa:
  ☐ Test cases ejecutados
  ☐ Bugs críticos/high resueltos
  ☐ Regresiones verificadas
  ☐ Hardcode check pasó

DL revisa (si aplica):
  ☐ UI implementada según diseño
  ☐ UX consistente
  ☐ Responsive funciona

PASO 4: Cada firmante firma
─────────────────────────────────────────────────────────────
POST /api/sprints/:sprintId/sign

Cada uno firma independientemente. No hay orden obligatorio.

PASO 5: Sprint cerrado
─────────────────────────────────────────────────────────────
Cuando TODOS los firmantes requeridos han firmado:
  → Sprint status = "closed"
  → Sprint.closedAt = timestamp
  → Sprint.allApprovalsSigned = true
```

#### Request

```
POST /api/sprints/:sprintId/sign
```

```json
{
  "validations": {
    "codeReviewPassed": true,
    "integrationPassed": true,
    "testsPassed": true,
    "hardcodeCheckPassed": true
  },
  "comments": "PRs #120-#125 revisados. Integration tests OK."
}
```

#### Response (éxito)

```json
{
  "id": "uuid-approval",
  "sprintId": "uuid-sprint",
  "signedBy": "uuid-tl",
  "role": "TL",
  "signedAt": "2026-04-12T14:00:00Z",
  "validations": {
    "codeReviewPassed": true,
    "integrationPassed": true,
    "testsPassed": true,
    "hardcodeCheckPassed": true
  },
  "comments": "PRs #120-#125 revisados. Integration tests OK.",
  "sprintStatus": {
    "totalSignersRequired": 3,
    "signersSoFar": 2,
    "pending": ["QA"],
    "isClosed": false
  }
}
```

#### Delegación

Si TL no está disponible, puede delegar a AR:

```
POST /api/sprints/:sprintId/sign
```

```json
{
  "delegatedBy": "uuid-tl",
  "delegationReason": "TL de vacaciones. AR asume responsabilidad.",
  "validations": {
    "codeReviewPassed": true,
    "integrationPassed": true
  }
}
```

**Regla:** Solo se puede delegar en Sprint y Release, NO en Stage.

---

### 5.3 NIVEL 3: FIRMA DE RELEASE

#### Actores

| Rol | Obligatorio | Qué valida |
|-----|-------------|------------|
| PJM (Project Manager Agent) | ✅ Sí | Release notes, documentación |
| PM (Product Manager) | ✅ Sí | Aprobación final |
| Stakeholders externos | Solo si `externalApprovalRequired = true` | Aprobación de negocio |

#### Paso a paso

```
PASO 1: Sistema detecta que todos los sprints están firmados
─────────────────────────────────────────────────────────────
Automático. No requiere acción.

PASO 2: PJM prepara release
─────────────────────────────────────────────────────────────
PJM genera/verifica:
  ☐ Release notes completos
  ☐ Lista de cambios (changelog)
  ☐ Breaking changes documentados (si hay)
  ☐ Instrucciones de deployment
  ☐ Rollback plan

PASO 3: Deploy a staging
─────────────────────────────────────────────────────────────
TL/DevOps hace deploy a ambiente de staging.

PASO 4: QA ejecuta smoke tests en staging
─────────────────────────────────────────────────────────────
QA verifica que las funcionalidades críticas funcionan en staging.

PASO 5: Firmantes firman
─────────────────────────────────────────────────────────────
POST /api/releases/:releaseId/sign

Orden típico:
  1. PJM firma (release notes listos)
  2. PM firma (aprobación final)
  3. Stakeholders firman (si aplica)

PASO 6: Release cerrado
─────────────────────────────────────────────────────────────
Cuando TODOS los firmantes requeridos han firmado:
  → Release status = "closed"
  → Release.closedAt = timestamp
  → Release.allApprovalsSigned = true
  → Listo para deploy a producción
```

#### Request

```
POST /api/releases/:releaseId/sign
```

```json
{
  "approvalType": "full_approval",
  "comments": "Release V2.0 aprobado. Deploy programado para 2026-04-13 06:00 UTC."
}
```

#### Response (éxito)

```json
{
  "id": "uuid-approval",
  "releaseId": "uuid-release",
  "signedBy": "uuid-pm",
  "role": "PM",
  "signedAt": "2026-04-12T16:00:00Z",
  "approvalType": "full_approval",
  "comments": "Release V2.0 aprobado. Deploy programado para 2026-04-13 06:00 UTC.",
  "releaseStatus": {
    "totalSignersRequired": 2,
    "signersSoFar": 2,
    "pending": [],
    "isClosed": true
  }
}
```

---

## 6. CIERRE / COMPLETACIÓN

### ¿Cuándo se considera "cerrado" cada nivel?

| Nivel | Cerrado cuando... | Campo en BD |
|-------|-------------------|-------------|
| Stage | Todos los agentes del stage firmaron | Calculado: count de `stage_approvals` |
| Sprint | TL + AR + QA (+ DL) firmaron | `sprints.allApprovalsSigned = true` |
| Release | PJM + PM (+ stakeholders) firmaron | `releases.allApprovalsSigned = true` |

### ¿Qué pasa después de cerrar?

| Nivel | Después de cerrar... |
|-------|----------------------|
| Stage | Siguiente stage puede iniciarse (aunque ya podía) |
| Sprint | Sprint.closedAt se llena, métricas se calculan |
| Release | Listo para producción, Release.closedAt se llena |

---

## 7. ¿ES BLOQUEANTE?

### ¿Las firmas bloquean el trabajo?

**NO.** Las firmas son para **cierre formal**, no para bloquear desarrollo.

| Situación | ¿Puedes continuar? |
|-----------|--------------------|
| Sprint 5 no firmado, quieres empezar Sprint 6 | ✅ SÍ |
| Release MVP no firmado, quieres trabajar en V2.0 | ✅ SÍ |
| Stage Development no firmado, quieres empezar Testing | ✅ SÍ |
| Tu compañero no firmó su stage, quieres firmar el tuyo | ✅ SÍ |

### ¿Qué SÍ bloquean las firmas?

| Situación | Bloqueado |
|-----------|-----------|
| Cerrar formalmente un sprint | Requiere firmas |
| Cerrar formalmente un release | Requiere firmas |
| Deploy a producción (si el proceso lo requiere) | Requiere release firmado |
| Métricas de cierre de sprint | Requiere sprint cerrado |

### ¿Qué pasa si nunca firmamos?

- El trabajo sigue normalmente
- No tienes métricas formales de cierre
- No tienes audit trail de quién aprobó qué
- Si algo falla en producción, no hay registro de quién validó

---

## 8. RESPONSABLES

| Nivel | Responsable de iniciar | Responsable de firmar |
|-------|------------------------|----------------------|
| Stage | Automático (cuando agente completa tareas) | Cada agente sus tareas |
| Sprint | Automático (cuando stages completos) | TL, AR, QA, DL |
| Release | PJM prepara, automático cuando sprints completos | PJM, PM, stakeholders |

### Matriz de responsabilidad

| Acción | Agente | TL | AR | QA | DL | PJM | PM |
|--------|--------|----|----|----|----|-----|-----|
| Completar tareas | ✅ | | | | | | |
| Firmar stage | ✅ | | | | | | |
| Code review | | ✅ | ✅ | | | | |
| Firmar sprint | | ✅ | ✅ | ✅ | ✅* | | |
| Preparar release notes | | | | | | ✅ | |
| Firmar release | | | | | | ✅ | ✅ |
| Aprobar para producción | | | | | | | ✅ |

*DL solo si hubo tareas de FE/UX en el sprint.

---

## 9. ENDPOINTS

### Stage

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/sprints/:sprintId/stages/:phaseCode/sign` | Firmar stage |
| GET | `/api/sprints/:sprintId/stages` | Ver estado de todos los stages |
| GET | `/api/sprints/:sprintId/stages/:phaseCode/approvals` | Ver firmas de un stage |

### Sprint

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/sprints/:sprintId/sign` | Firmar sprint |
| GET | `/api/sprints/:sprintId/approvals` | Ver firmas del sprint |
| GET | `/api/sprints/:sprintId/sign-status` | Ver quién falta por firmar |

### Release

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/releases/:releaseId/sign` | Firmar release |
| GET | `/api/releases/:releaseId/approvals` | Ver firmas del release |
| GET | `/api/releases/:releaseId/sign-status` | Ver quién falta por firmar |

---

## 10. EJEMPLO COMPLETO

### Escenario

Sprint S05 "Trazabilidad" tiene:
- Fase Development: 3 agentes (DB, BE, FE)
- Fase Testing: 1 agente (QA)

### Flujo completo

```
DÍA 1-5: DESARROLLO
────────────────────────────────────────────────────────────
DB-Agent completa sus 2 tareas → status: completed
BE-Agent completa sus 4 tareas → status: completed
FE-Agent completa sus 3 tareas → status: completed

DÍA 5: FIRMAS DE STAGE DEVELOPMENT
────────────────────────────────────────────────────────────
DB-Agent:
  POST /api/sprints/S05/stages/development/sign
  → ✅ Firmado

BE-Agent:
  POST /api/sprints/S05/stages/development/sign
  → ✅ Firmado

FE-Agent:
  POST /api/sprints/S05/stages/development/sign
  → ❌ Error: devlog entry critical pendiente
  
FE-Agent resuelve el devlog entry, reintenta:
  POST /api/sprints/S05/stages/development/sign
  → ✅ Firmado

Stage Development: COMPLETAMENTE FIRMADO

DÍA 6-8: TESTING
────────────────────────────────────────────────────────────
QA-Agent ejecuta tests, reporta bugs, bugs se corrigen.
QA-Agent completa sus tareas → status: completed

DÍA 8: FIRMA DE STAGE TESTING
────────────────────────────────────────────────────────────
QA-Agent:
  POST /api/sprints/S05/stages/testing/sign
  → ✅ Firmado

Stage Testing: COMPLETAMENTE FIRMADO
Todos los stages firmados → Sistema notifica a TL/AR/QA

DÍA 9: FIRMAS DE SPRINT
────────────────────────────────────────────────────────────
TL revisa PRs, integration:
  POST /api/sprints/S05/sign
  {
    "validations": {
      "codeReviewPassed": true,
      "integrationPassed": true,
      "testsPassed": true,
      "hardcodeCheckPassed": true
    }
  }
  → ✅ Firmado (1/3)

AR revisa arquitectura:
  POST /api/sprints/S05/sign
  → ✅ Firmado (2/3)

QA confirma tests:
  POST /api/sprints/S05/sign
  → ✅ Firmado (3/3)

Sprint S05: CERRADO
  → closedAt = 2026-04-09T17:00:00Z
  → allApprovalsSigned = true

(Repetir para otros sprints del release...)

DÍA FINAL: FIRMA DE RELEASE
────────────────────────────────────────────────────────────
Todos los sprints del release MVP están firmados.

PJM:
  - Genera release notes
  - Verifica documentación
  POST /api/releases/MVP/sign
  → ✅ Firmado (1/2)

PM:
  - Revisa release notes
  - Aprueba para producción
  POST /api/releases/MVP/sign
  → ✅ Firmado (2/2)

Release MVP: CERRADO
  → closedAt = 2026-04-12T16:00:00Z
  → allApprovalsSigned = true
  → 🚀 LISTO PARA PRODUCCIÓN
```

---

## 11. TABLAS EN BASE DE DATOS

### stage_approvals

```sql
CREATE TABLE stage_approvals (
  id TEXT PRIMARY KEY,
  sprint_id TEXT NOT NULL REFERENCES sprints(id),
  phase_code TEXT NOT NULL,
  signed_by TEXT NOT NULL REFERENCES users(id),
  signed_at TIMESTAMP NOT NULL DEFAULT NOW(),
  tasks_included JSONB,
  comments TEXT,
  
  UNIQUE(sprint_id, phase_code, signed_by)
);
```

### sprint_approvals

```sql
CREATE TABLE sprint_approvals (
  id TEXT PRIMARY KEY,
  sprint_id TEXT NOT NULL REFERENCES sprints(id),
  signed_by TEXT NOT NULL REFERENCES users(id),
  role TEXT NOT NULL,
  signed_at TIMESTAMP NOT NULL DEFAULT NOW(),
  
  -- Validaciones
  code_review_passed BOOLEAN,
  integration_passed BOOLEAN,
  tests_passed BOOLEAN,
  hardcode_check_passed BOOLEAN,
  
  -- Delegación
  delegated_by TEXT REFERENCES users(id),
  delegation_reason TEXT,
  delegated_at TIMESTAMP,
  
  comments TEXT,
  
  UNIQUE(sprint_id, signed_by)
);
```

### release_approvals

```sql
CREATE TABLE release_approvals (
  id TEXT PRIMARY KEY,
  release_id TEXT NOT NULL REFERENCES releases(id),
  signed_by TEXT NOT NULL REFERENCES users(id),
  role TEXT NOT NULL,
  signed_at TIMESTAMP NOT NULL DEFAULT NOW(),
  approval_type TEXT DEFAULT 'full_approval',
  
  -- Delegación
  delegated_by TEXT REFERENCES users(id),
  delegation_reason TEXT,
  delegated_at TIMESTAMP,
  
  comments TEXT,
  
  UNIQUE(release_id, signed_by)
);
```

### Campos en sprints

```sql
ALTER TABLE sprints ADD COLUMN all_stages_signed BOOLEAN DEFAULT false;
ALTER TABLE sprints ADD COLUMN all_approvals_signed BOOLEAN DEFAULT false;
ALTER TABLE sprints ADD COLUMN closed_at TIMESTAMP;
ALTER TABLE sprints ADD COLUMN closed_by TEXT REFERENCES users(id);
```

### Campos en releases

```sql
ALTER TABLE releases ADD COLUMN all_approvals_signed BOOLEAN DEFAULT false;
ALTER TABLE releases ADD COLUMN closed_at TIMESTAMP;
ALTER TABLE releases ADD COLUMN closed_by TEXT REFERENCES users(id);
ALTER TABLE releases ADD COLUMN external_approval_required BOOLEAN DEFAULT false;
```

---

## 12. ERRORES COMUNES

| Error | Causa | Solución |
|-------|-------|----------|
| "Cannot sign stage - tasks not completed" | Tienes tareas en status != completed | Completa tus tareas primero |
| "Cannot sign stage - pending devlog entries" | Hay entries critical/high sin resolver | Resuelve o difiere los entries |
| "Cannot sign sprint - stages not complete" | Faltan firmas de stages | Espera que todos los agentes firmen |
| "Cannot sign sprint - missing signers" | No tienes permiso para firmar | Solo TL/AR/QA/DL pueden firmar sprint |
| "Sprint already closed" | Intentas firmar sprint ya cerrado | No se puede, las firmas son irreversibles |

---

## 13. FAQ

**¿Puedo desfirmar algo?**
No. Las firmas son irreversibles. Si hay un problema después de firmar, va a proceso de bugs.

**¿Qué pasa si TL no está disponible?**
Puede delegar a AR. La delegación queda registrada con razón.

**¿Puedo firmar el sprint si un agente no firmó su stage?**
No. Todos los stages deben estar completamente firmados primero.

**¿Las firmas bloquean mi trabajo?**
No. Puedes seguir trabajando en sprints/releases futuros sin esperar firmas.

**¿Qué pasa si nunca firmamos?**
El trabajo sigue, pero no tienes cierre formal ni audit trail.

---

**Documento:** FEATURE_FIRMAS.md  
**Versión:** 1.0  
**Fecha:** 2026-04-12
