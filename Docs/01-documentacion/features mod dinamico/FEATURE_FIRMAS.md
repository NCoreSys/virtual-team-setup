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

### ¿Dónde se configura?

| Lugar | Cuándo | Qué se configura |
|-------|--------|------------------|
| **Wizard** (paso de config) | Al crear proyecto | Config global de firmas |
| **Settings del proyecto** | Después de crear | Editar config global |
| **Handoff del release/sprint** | Al planificar | Firmantes específicos |

### Configuración global (Proyecto)

```json
{
  "signaturesConfig": {
    "enabled": true,
    "levels": {
      "task": {
        "enabled": false,
        "requiredForTypes": ["development", "bugfix"]
      },
      "delivery": {
        "enabled": true,
        "requireReviewer": true
      },
      "sprint": {
        "enabled": true,
        "requiredSigners": ["TL", "AR", "QA"]
      },
      "phase": {
        "enabled": true,
        "usePhaseDefaults": true
      },
      "release": {
        "enabled": true,
        "requiredSigners": ["PJM", "PM"],
        "externalApprovalRequired": false
      }
    }
  }
}
```

### Configuración por fase (Catálogo)

En `phase_catalog` o al configurar proyecto:

```json
{
  "phaseCode": "development",
  "signatureConfig": {
    "enabled": true,
    "defaultSigners": ["TL", "AR", "QA"],
    "requiredSigners": ["TL", "QA"]
  }
}
```

### ¿Se puede editar después de crear?

| Situación | ¿Se puede editar? | ¿Quién puede? |
|-----------|-------------------|---------------|
| No hay firmas aún | ✅ Sí | Usuario (humano) |
| Ya hay firmas | ❌ No | — |
| Sprint en curso sin firmas | ✅ Sí | Usuario (humano) |

**Regla importante:** Solo el **usuario humano** puede modificar la configuración de firmas. Los agentes NO pueden modificarla para evitar que se auto-aprueben.

### ¿Qué pasa si no se configura en el wizard?

Se usan los **defaults del template de flujo** seleccionado:

| Template | Firmas default |
|----------|----------------|
| SDLC-Scrum | Habilitadas (sprint, release) |
| Kanban | Deshabilitadas |
| Waterfall | Habilitadas (fase, release) |
| Custom | Usuario debe configurar |

---

## 5. FLUJO OPERATIVO

### 5.0 NIVELES DE FIRMA

El sistema soporta **5 niveles de firma**, cada uno configurable de manera independiente:

```
NIVEL 1: TAREA
├── Firmante: Agente ejecutor
├── Qué valida: "Terminé mi trabajo"
└── Configurable: Sí, por tipo de tarea

NIVEL 2: ENTREGABLE (Delivery)
├── Firmantes: Agentes que contribuyeron + Revisor (TL/SA)
├── Qué valida: "El entregable está completo"
└── Configurable: Sí, por tipo de entregable

NIVEL 3: SPRINT
├── Firmantes: Revisores (TL, AR, QA, DL si aplica)
├── Qué valida: Code review, integration, tests
└── Configurable: Sí, por sprint

NIVEL 4: FASE
├── Firmantes: Según fase (SA para Analysis, TL para Development, etc.)
├── Qué valida: "La fase está completa"
└── Configurable: Sí, por fase en catálogo

NIVEL 5: RELEASE
├── Firmantes: PJM, PM, Stakeholders
├── Qué valida: "Listo para producción"
└── Configurable: Sí, por release
```

### 5.1 TIPOS DE FIRMANTES

| Tipo | Roles | Qué pueden firmar |
|------|-------|-------------------|
| **Ejecutores** | DB, BE, FE, QA-Agent, etc. | Su propia tarea, su contribución a entregable |
| **Revisores** | TL, SA, AR, DL | Sprint, Fase, Entregables |
| **Aprobadores** | PM, PJM, PO, Stakeholders | Release, Proyecto |

### 5.2 ¿CÓMO SE DETERMINAN LOS FIRMANTES?

Los firmantes se definen en **3 lugares**:

| Lugar | Cuándo se define | Qué define |
|-------|------------------|------------|
| **Catálogo de fases** | Al configurar proyecto | Firmantes default por tipo de fase |
| **Handoff del release/sprint** | Al planificar trabajo | Firmantes específicos para ese trabajo |
| **Usuarios del proyecto** | Al asignar equipo | Nivel de autoridad de cada usuario |

#### Algoritmo de cálculo de firmantes:

```
1. Obtener usuarios asignados al proyecto
2. Por cada usuario, obtener su nivel de autoridad
3. Filtrar según la fase/sprint/entregable
4. Cruzar con firmantes requeridos del catálogo
5. Resultado: lista de firmantes para ese nivel
```

#### Ejemplo en Handoff:

```markdown
## FIRMANTES SPRINT S05

### Nivel: Stage/Fase
| Fase | Firmantes Requeridos |
|------|---------------------|
| Analysis | SA (obligatorio), AR (opcional) |
| Development | TL (obligatorio), AR (obligatorio) |
| Testing | QA (obligatorio) |

### Nivel: Sprint
| Rol | Usuario | Obligatorio |
|-----|---------|-------------|
| TL | @juan-tl | ✅ |
| AR | @maria-ar | ✅ |
| QA | @pedro-qa | ✅ |

### Nivel: Release
| Rol | Usuario | Obligatorio |
|-----|---------|-------------|
| PJM | @pjm-agent | ✅ |
| PM | @martin | ✅ |
```

---

### 5.3 NIVEL 1: FIRMA DE TAREA

#### ¿Qué es?

El agente ejecutor firma que completó su tarea.

#### Actores

El **agente asignado** a la tarea.

#### ¿Cuándo aplica?

- Configurable por tipo de tarea
- Default: aplica a tareas de desarrollo/código
- No aplica: tareas de análisis, documentación (configurable)

#### Paso a paso

```
PASO 1: Agente completa la tarea
─────────────────────────────────────────────────
Status cambia a "completed"

PASO 2: Sistema verifica si tarea requiere firma
─────────────────────────────────────────────────
Según configuración del tipo de tarea.

PASO 3: Si requiere firma, agente firma
─────────────────────────────────────────────────
POST /api/tasks/:taskId/sign

PASO 4: Tarea queda firmada
─────────────────────────────────────────────────
Se registra: quién, cuándo
```

#### Request

```
POST /api/tasks/:taskId/sign
```

```json
{
  "comments": "Implementación completa. PR #125 mergeado."
}
```

---

### 5.4 NIVEL 2: FIRMA DE ENTREGABLE (Delivery)

#### ¿Qué es?

Firma que valida que un entregable está completo.

#### Actores

- **Agentes** que contribuyeron al entregable
- **Revisor** (TL o SA según fase)

#### ¿Cuándo aplica?

Configurable por tipo de entregable en catálogo.

#### Paso a paso

```
PASO 1: Todas las tareas del entregable completadas
─────────────────────────────────────────────────
Sistema detecta que el delivery está listo.

PASO 2: Agentes que contribuyeron firman
─────────────────────────────────────────────────
Cada agente firma su participación.

PASO 3: Revisor firma
─────────────────────────────────────────────────
TL o SA revisa y firma el entregable.

PASO 4: Entregable cerrado
─────────────────────────────────────────────────
Se registra: firmantes, timestamps
```

#### Request

```
POST /api/deliveries/:deliveryId/sign
```

---

### 5.5 NIVEL 3: FIRMA DE SPRINT

#### ¿Qué es?

Firma que valida que el sprint está completo y revisado.

#### Actores

| Rol | Obligatorio | Qué valida |
|-----|-------------|------------|
| TL | ✅ Sí | Code review, integration |
| AR | ✅ Sí | Arquitectura, ADRs |
| QA | ✅ Sí | Tests, bugs |
| DL | Solo si hubo FE | UX, diseño |

#### Paso a paso

(Se mantiene el flujo actual documentado)

---

### 5.6 NIVEL 4: FIRMA DE FASE

#### ¿Qué es?

Firma que valida que una fase del proyecto está completa.

#### Actores

Depende de la fase (definido en `phase_catalog`):

| Fase | Firmantes Default |
|------|-------------------|
| Planning | PM |
| Requirements | PM, SA |
| Analysis | SA, AR |
| UX Design | DL, AR |
| Technical Design | AR, TL |
| Development | TL, AR, QA |
| Testing | QA, TL |
| Deployment | TL, DevOps |
| Operations | TL, PM |

#### ¿Cuándo aplica?

- Cuando todos los sprints de esa fase están completos
- O cuando la fase no usa sprints (ej: Kanban)

#### Paso a paso

```
PASO 1: Todos los entregables/sprints de la fase completados
─────────────────────────────────────────────────────────────
Sistema detecta que la fase puede cerrarse.

PASO 2: Firmantes de la fase revisan
─────────────────────────────────────────────────────────────
Según catálogo de la fase.

PASO 3: Firmantes firman
─────────────────────────────────────────────────────────────
POST /api/phases/:phaseId/sign

PASO 4: Fase cerrada
─────────────────────────────────────────────────────────────
Se registra, siguiente fase puede iniciar formalmente.
```

#### Request

```
POST /api/phases/:phaseId/sign
```

---

### 5.7 NIVEL 5: FIRMA DE RELEASE

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

| Situación | ¿Puedes continuar trabajando? |
|-----------|-----------------------------|
| Sprint 5 no firmado, quieres empezar Sprint 6 | ✅ SÍ |
| Release MVP no firmado, quieres trabajar en V2.0 | ✅ SÍ |
| Fase Analysis no firmada, quieres empezar Development | ✅ SÍ |
| Entregable no firmado, quieres crear otro | ✅ SÍ |
| Tu compañero no firmó su tarea | ✅ SÍ |

### ¿Qué SÍ requiere firmas para proceder?

| Situación | Requiere firma |
|-----------|----------------|
| Cerrar **formalmente** un sprint | ✅ Sí |
| Cerrar **formalmente** un release | ✅ Sí |
| Deploy a producción (si config lo requiere) | ✅ Sí |
| Métricas de cierre | ✅ Sí |
| Generar reportes de auditoría | ✅ Sí |

### ¿Qué pasa si nunca firmamos?

- El trabajo sigue normalmente
- No tienes cierre formal
- No tienes audit trail
- No puedes generar reportes de cierre
- Si algo falla, no hay registro de quién validó

### Configuración por nivel

Cada nivel puede configurarse como:

| Opción | Comportamiento |
|--------|----------------|
| `enabled: true` | Firma requerida para cierre formal |
| `enabled: false` | No se requiere firma, cierre automático |
| `optional: true` | Firma disponible pero no requerida |

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

## 13. INTEGRACIÓN CON DoD/DoR

### Relación Firmas ↔ Criterios

Las firmas dependen del sistema de criterios:

| Nivel de firma | Prerequisito de criterios |
|----------------|--------------------------|
| **Tarea** | Todos los DoD deben estar `verified` |
| **Stage** | Todas las tareas del agente con DoD `verified` |
| **Sprint** | Todos los stages firmados + validaciones TL/AR/QA |
| **Release** | Todos los sprints firmados |

### Flujo integrado

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     FLUJO: DoD → FIRMA                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  TAREA                                                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 1. Agente completa trabajo                                          │   │
│  │ 2. Agente reporta DoD (fulfillmentStatus = "reported")             │   │
│  │ 3. TL verifica DoD (fulfillmentStatus = "verified")                │   │
│  │ 4. Tarea → completed                                                │   │
│  │ 5. Agente puede firmar su tarea (si firma de tarea habilitada)     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              │                                              │
│                              ▼                                              │
│  STAGE                                                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Requisito: Todas las tareas del agente en "completed"              │   │
│  │            con DoD "verified"                                       │   │
│  │                                                                     │   │
│  │ → Agente puede firmar stage                                        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              │                                              │
│                              ▼                                              │
│  SPRINT                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Requisito: Todos los stages firmados                               │   │
│  │                                                                     │   │
│  │ → TL/AR/QA pueden firmar sprint                                    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Validación al firmar

Cuando un agente intenta firmar su stage, el sistema verifica:

```typescript
async signStage(sprintId: string, phaseCode: string, agentId: string) {
  // 1. Obtener tareas del agente en este stage
  const tasks = await this.getAgentTasksInStage(sprintId, phaseCode, agentId);
  
  // 2. Verificar que todas están completed
  const notCompleted = tasks.filter(t => t.status !== 'completed');
  if (notCompleted.length > 0) {
    throw new Error('Tasks not completed: ' + notCompleted.map(t => t.code));
  }
  
  // 3. Verificar que todos los DoD están verified
  for (const task of tasks) {
    const dodCriteria = await this.getCriteria(task.id, { type: 'dod' });
    const notVerified = dodCriteria.filter(c => 
      c.isApplicable && c.fulfillmentStatus !== 'verified'
    );
    if (notVerified.length > 0) {
      throw new Error(`Task ${task.code} has unverified DoD: ${notVerified.map(c => c.code)}`);
    }
  }
  
  // 4. Proceder con firma
  return this.createStageApproval(sprintId, phaseCode, agentId);
}
```

### Configuración

| Config | Descripción | Default |
|--------|-------------|---------|
| `requireDoDForStageSign` | ¿Exigir DoD verified para firmar stage? | `true` |
| `requireDoDForSprintSign` | ¿Exigir todas las tareas con DoD verified? | `true` |

---

## 14. FAQ

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
