# MANUAL DE FEATURES VTT V4
## Guía para Agentes y Usuarios

**Versión:** 2.0  
**Fecha:** 2026-05-06  
**Audiencia:** Agentes AI, TL, PM, usuarios del sistema

---

## ÍNDICE

1. [Criterios de Aceptación (AC, DoD, DoR)](#1-criterios-de-aceptación)
2. [Fulfillment de Criterios](#2-fulfillment-de-criterios)
3. [Devlog Entries](#3-devlog-entries)
4. [Links entre Tareas](#4-links-entre-tareas)
5. [Document Impacts](#5-document-impacts)
6. [Review Gate](#6-review-gate)
7. [Living Documents](#7-living-documents)
8. [Trackable Items](#8-trackable-items)
9. [Deferred Scope](#9-deferred-scope)
10. [Hardcode Check](#10-hardcode-check)
11. [Firmas y Aprobaciones](#11-firmas-y-aprobaciones)
12. [Releases y Sprints](#12-releases-y-sprints)
13. [Task Types](#13-task-types)

---

## 1. CRITERIOS DE ACEPTACIÓN

### ¿Qué es?
Sistema integral de criterios que define las condiciones de éxito. Incluye tres tipos:

| Tipo | Código | Propósito |
|------|--------|-----------|
| **AC (Acceptance Criteria)** | AC-US-XXX-N | Criterios funcionales de la User Story |
| **DoD (Definition of Done)** | DOD-XX-NN | Checklist de completitud por tipo de tarea |
| **DoR (Definition of Ready)** | DOR-NN | Precondiciones para iniciar |

### ¿Para qué sirve?
- **DoR** — Valida que puedes empezar (¿tienes todo lo necesario?)
- **DoD** — Valida que terminaste bien (¿cumple los estándares?)
- **AC** — Valida que funciona (¿hace lo que debería?)

### ¿Cómo se usa?

**Al crear una tarea:**
1. El sistema hereda automáticamente DoD y DoR según el `taskTypeCode`
2. PM/TL agregan AC específicos de la User Story

**Al iniciar la tarea:**
1. Sistema verifica DoR
2. Si hay DoR pendientes → bloqueado (puedes hacer override con justificación)

**Al terminar la tarea:**
1. Agente reporta cada DoD como "cumplido" con evidencia
2. TL verifica cada DoD
3. Cuando todos están "verified" → puedes mover a completed

### Ejemplo completo

Tarea: "Implementar endpoint POST /users" (taskTypeCode: backend)

**DoR heredado automáticamente:**
- [ ] DOR-01: ASSIGNMENT leído completamente
- [ ] DOR-02: Dependencias en task_completed
- [ ] DOR-08: Rama Git creada
- ... (14 items)

**DoD heredado automáticamente:**
- [ ] DOD-BE-01: Código compila sin errores TypeScript
- [ ] DOD-BE-02: Validación Zod implementada
- [ ] DOD-BE-03: Tests unitarios pasan
- ... (12 items)

**AC agregados por PM:**
- [ ] AC-US-001-1: Given JSONL válido, When POST /import, Then HTTP 201
- [ ] AC-US-001-2: Given email duplicado, Then HTTP 409

### Tipos de criterios

| Tipo | Cuándo usarlo |
|------|---------------|
| `functional` | Comportamiento esperado (AC) |
| `technical` | Requisito de implementación |
| `security` | Requisitos de seguridad |
| `performance` | Requisitos de rendimiento |
| `dod` | Definition of Done |
| `dor` | Definition of Ready |

---

## 2. FULFILLMENT DE CRITERIOS

### ¿Qué es?
El registro de cumplimiento. Tiene dos niveles: **reportar** (agente) y **verificar** (TL/QA).

### Flujo de fulfillment

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  ESTADO: pending                                            │
│     │                                                       │
│     ▼  Agente completa y reporta                           │
│                                                             │
│  ESTADO: reported                                           │
│     │   (reportedBy, reportedAt, evidence)                 │
│     │                                                       │
│     ▼  TL/QA revisa                                        │
│     │                                                       │
│     ├─► ESTADO: verified  (aprobado)                       │
│     │   (verifiedBy, verifiedAt)                           │
│     │                                                       │
│     └─► ESTADO: rejected  (rechazado)                      │
│         (rejectionReason)                                   │
│         → Tarea vuelve a in_progress                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### ¿Cómo se usa?

**Como agente:**

1. Terminas tu trabajo
2. Vas a la tarea → Tab "Criteria"
3. Por cada criterio DoD/AC:
   - Click en [Report as Met]
   - Agrega evidencia: "Implementado en PR #125, test en línea 45"
4. Mueves tarea a `in_review`

**Como TL/QA:**

1. Revisas los criterios reportados
2. Por cada uno:
   - Click en [Verify] si está bien
   - Click en [Reject] con razón si no está bien
3. Si todos verificados → tarea puede ir a `completed`

### Estados

| Estado | Significado | Quién lo pone |
|--------|-------------|---------------|
| `pending` | No evaluado | Sistema |
| `reported` | Agente dice que cumplió | Agente |
| `verified` | TL confirma que cumplió | TL/QA |
| `rejected` | TL rechaza, hay que corregir | TL/QA |

### Desactivar criterio que no aplica

Si un DoD no aplica a tu tarea (ej: DOD-BE-07 "Idempotencia" en un endpoint GET):

1. Pide a PM/TL que lo desactive
2. PM/TL hace: PATCH con `isApplicable: false` y `disabledReason: "..."`
3. El criterio no cuenta en validaciones pero queda visible
| `not_met` | No cumplido |

---

## 3. DEVLOG ENTRIES

### ¿Qué es?
Entradas de registro que documentan lo que pasa durante la ejecución de una tarea.

### ¿Para qué sirve?
- Captura decisiones tomadas sobre la marcha
- Documenta problemas encontrados
- Registra deuda técnica para después
- Crea historial de lo que pasó

### ¿Cómo se usa?

Durante tu trabajo, cada vez que:
- Tomes una decisión técnica → registra una entrada tipo `decision`
- Encuentres algo que bloquea → registra un `blocker`
- Identifiques deuda técnica → registra `tech_debt`
- Hagas una observación de testing → registra `testing_note`
- Detectes un riesgo → registra `risk`

### Categorías

| Categoría | Cuándo usarla | ¿Usa severidad? |
|-----------|---------------|-----------------|
| `decision` | Tomaste una decisión técnica | No |
| `blocker` | Algo te impide avanzar | Sí |
| `tech_debt` | Identificaste algo que mejorar después | Sí |
| `testing_note` | Resultado de prueba o verificación | Sí |
| `risk` | Identificaste un riesgo potencial | Sí |
| `issue` | Observación o inconsistencia (NO bugs) | Sí |

### Severidad

| Severidad | Significado | ¿Bloquea cierre? |
|-----------|-------------|------------------|
| `critical` | Impide que el sistema funcione | ✅ SÍ |
| `high` | Problema serio que debe resolverse | ✅ SÍ |
| `medium` | Debería resolverse pero no urgente | ❌ NO |
| `low` | Nice to have | ❌ NO |

### Ejemplo

Estás implementando un endpoint y decides usar UUID en lugar de auto-increment:

```
Categoría: decision
Título: Usar UUID v4 para IDs de usuario
Descripción: Por consistencia con el resto del sistema y para evitar 
             exposición de secuencias en la API.
```

### ⚠️ IMPORTANTE

**Los bugs NO van en devlog.** Los bugs tienen su propio proceso separado.

---

## 4. LINKS ENTRE TAREAS

### ¿Qué es?
Conexiones entre tareas que indican dependencias o relaciones.

### ¿Para qué sirve?
- Saber qué tareas debes esperar antes de empezar
- Ver qué tareas estás bloqueando
- Encontrar tareas relacionadas

### ¿Cómo se usa?

Al crear o actualizar una tarea, agregas links:

1. Vas a la tarea → Tab "Links"
2. Click [+ Nuevo Link]
3. Seleccionas tipo de relación
4. Buscas la tarea relacionada

### Tipos de links

| Tipo | Significado | Ejemplo |
|------|-------------|---------|
| `depends_on` | Esta tarea necesita que otra termine primero | "POST /users" depende de "Crear modelo User" |
| `blocks` | Esta tarea impide que otra avance | "Migración DB" bloquea "Deploy a producción" |
| `related_to` | Tareas relacionadas sin dependencia | "POST /users" relacionada con "GET /users/:id" |
| `implements` | Esta tarea implementa un requerimiento | "POST /users" implementa "RF-001" |

### Ejemplo visual

```
VTT-420: Crear modelo User
         │
         └── depends_on ──┐
                          │
                          ▼
VTT-423: POST /users ────blocks───► VTT-430: POST /auth/login
         │
         └── related_to ──► VTT-425: GET /users/:id
```

---

## 5. DOCUMENT IMPACTS

### ¿Qué es?
Registro de qué documentos afecta tu trabajo en una tarea.

### ¿Para qué sirve?
- Saber qué documentación actualizar
- Rastrear cambios en documentos
- Mantener documentación sincronizada con código

### ¿Cómo se usa?

Al terminar tu trabajo:

1. Vas a la tarea → Tab "Impacts"
2. Click [+ Nuevo Impacto]
3. Seleccionas el documento afectado
4. Indicas tipo de impacto y descripción

### Tipos de impacto

| Tipo | Significado |
|------|-------------|
| `added` | Creaste un documento nuevo |
| `modified` | Modificaste un documento existente |
| `removed` | Eliminaste un documento |
| `referenced` | Solo referenciaste, sin cambios |

### Ejemplo

Implementaste un nuevo endpoint:

```
Documento: API Reference - Users Module
Tipo: modified
Descripción: Agregué documentación del endpoint POST /users
```

---

## 6. REVIEW GATE

### ¿Qué es?
Una verificación automática antes de que una tarea pueda pasar a revisión.

### ¿Para qué sirve?
- Evita que tareas incompletas lleguen a QA
- Asegura que problemas críticos se resuelvan antes de avanzar
- Reduce retrabajo

### ¿Cómo funciona?

Cuando intentas pasar una tarea a "In Review":

1. El sistema verifica:
   - ¿Hay devlog entries con severidad `critical` o `high` pendientes?
   - ¿Hay criterios obligatorios sin cumplir?

2. Si hay problemas → **BLOQUEADO** (error 422)
3. Si todo está bien → La tarea avanza

### ¿Qué hacer si estás bloqueado?

1. Abre el Review Gate (badge 🔴 en la tarea)
2. Ve la lista de blockers
3. Resuelve cada uno:
   - **Devlog entry:** Márcalo como resuelto o diferido
   - **Criterio:** Márcalo como cumplido

4. Intenta avanzar de nuevo

### Estados del badge

| Badge | Significado |
|-------|-------------|
| 🔴 | No puede avanzar - hay blockers |
| 🟢 | Puede avanzar - todo resuelto |

---

## 7. LIVING DOCUMENTS

### ¿Qué es?
Documentos que se actualizan automáticamente desde el código.

### ¿Para qué sirve?
- Mantener documentación siempre actualizada
- Evitar documentación desactualizada
- Reducir trabajo manual de documentar

### Tipos de living documents

| Tipo | Fuente | Qué genera |
|------|--------|------------|
| Schema | `prisma/schema.prisma` | Documentación de modelos de datos |
| API | `swagger/openapi.json` | Documentación de endpoints |

### ¿Cómo funciona?

1. Haces cambios en el código (ej: agregas modelo en schema.prisma)
2. El sistema detecta el cambio
3. El documento asociado se actualiza automáticamente

### Ejemplo

Agregas un nuevo modelo `Payment` en schema.prisma:

```prisma
model Payment {
  id        String   @id
  amount    Decimal
  status    String
  createdAt DateTime
}
```

El documento "Database Schema" se actualiza solo para incluir este modelo.

---

## 8. TRACKABLE ITEMS

### ¿Qué es?
Items que necesitan seguimiento a lo largo del proyecto.

### ¿Para qué sirve?
- Rastrear requerimientos hasta su implementación
- Documentar decisiones arquitectónicas (ADRs)
- Seguir KPIs y riesgos

### Tipos de trackable items

| Tipo | Código | Ejemplo |
|------|--------|---------|
| Requerimiento Funcional | RF | RF-001: Usuario puede registrarse |
| Requerimiento No Funcional | RNF | RNF-001: API responde en < 200ms |
| Architecture Decision Record | ADR | ADR-001: Usar PostgreSQL |
| Key Performance Indicator | KPI | KPI-001: Tasa de conversión |
| Riesgo | RISK | RISK-001: Dependencia de API externa |

### ¿Cómo se usa?

1. PM/AR crea el trackable item
2. Se vincula a las tareas que lo implementan
3. Se agregan evidencias cuando se completa
4. Se puede ver la matriz de trazabilidad

### ADRs de proceso

Para decisiones de **cómo trabajamos** (no de código), usa ADR con prefijo `PROC`:

```
ADR-PROC-001: Estructura de carpetas .vtt/
ADR-PROC-002: Composición de equipos por repo
```

### ¿Dónde van las decisiones tomadas durante una tarea?

| Tipo de decisión | Dónde va |
|------------------|----------|
| Decisión de código/arquitectura que afecta todo el proyecto | Trackable Item (ADR) |
| Decisión local durante ejecución de tarea | Devlog entry (decision) |
| Decisión de proceso/metodología | Trackable Item (ADR-PROC-XXX) |

---

## 9. DEFERRED SCOPE

### ¿Qué es?
Sistema para registrar scope que se decide posponer a una fase o release futuro.

### ¿Para qué sirve?
- No perder features que se posponen
- Tener visibilidad de qué quedó pendiente
- Planificar releases futuros

### ¿Cómo se usa?

1. Durante análisis o desarrollo, identificas algo que no entra en este release
2. Creas un registro de "deferred scope"
3. Indicas a qué fase/release se pospone
4. El item queda visible en el backlog futuro

### Estados

| Estado | Significado |
|--------|-------------|
| `deferral_pending` | Pendiente de programar |
| `deferral_scheduled` | Programado para sprint/release futuro |
| `deferral_completed` | Ya se implementó |
| `deferral_cancelled` | Se canceló, no se hará |

### Ejemplo

Durante desarrollo de MVP, identificas que "exportar a PDF" no es crítico:

```
Item: Exportar reportes a PDF
Status: deferral_scheduled
Target: Release V2.0
Reason: No es crítico para MVP, requiere librería adicional
```

---

## 10. HARDCODE CHECK

### ¿Qué es?
Sistema para detectar datos "quemados" en el código que deberían venir de configuración.

### ¿Para qué sirve?
- Evitar datos hardcodeados en producción
- Detectar credenciales expuestas
- Mantener código configurable

### ¿Cómo se usa?

**Modo actual (manual):**

1. Vas a la tarea → Hardcode Check
2. Pegas el código a revisar
3. Click "Ejecutar análisis"
4. Ves los findings

**Modo futuro (automático):**

1. Haces PR
2. Sistema escanea automáticamente
3. Si hay findings críticos, la tarea no puede avanzar

### ¿Qué detecta?

| Patrón | Severidad | Ejemplo malo |
|--------|-----------|--------------|
| UUID hardcodeado | HIGH | `userId = "550e8400-..."` |
| URL hardcodeada | CRITICAL | `fetch("http://localhost:3000")` |
| Credenciales inline | CRITICAL | `apiKey = "sk-abc123"` |
| Magic numbers | MEDIUM | `setTimeout(fn, 86400000)` |
| Status hardcodeado | HIGH | `status: "active"` |

### ¿Qué hacer con un finding?

| Opción | Cuándo usarla |
|--------|---------------|
| **Corregir** | El finding es válido, corrige el código |
| **Falso positivo** | Es intencional (ej: constante documentada) — aprueba con justificación |
| **Generar bug** | No puedes corregirlo ahora — crea bug para fix posterior |

---

## 11. FIRMAS Y APROBACIONES

### ¿Qué es?
Sistema de firmas en cascada para cerrar fases, sprints y releases.

### ¿Para qué sirve?
- Asegurar que cada etapa fue revisada
- Documentar quién aprobó qué
- Crear audit trail

---

### NIVEL 1: FIRMA DE STAGE (Fase dentro de Sprint)

#### ¿Qué es un Stage?
Un stage es una **fase específica dentro de un sprint**. Por ejemplo, si el Sprint 5 tiene tareas de Development y Testing, hay dos stages: `S05-Development` y `S05-Testing`.

#### ¿Quién firma?
Los **agentes que ejecutaron tareas** en ese stage.

#### ¿Cuándo se puede firmar?
Cuando **TODAS** las tareas del agente en ese stage están en `completed`.

#### Criterios para firmar Stage:

| # | Criterio | Obligatorio |
|---|----------|-------------|
| 1 | Todas mis tareas en status `completed` | ✅ |
| 2 | Todos los criterios de aceptación marcados | ✅ |
| 3 | No hay devlog entries `critical`/`high` pendientes | ✅ |
| 4 | Hardcode check ejecutado (si aplica) | ✅ |

#### Proceso paso a paso:

```
1. Agente completa todas sus tareas del stage
        │
        ▼
2. Agente verifica:
   ☐ ¿Todas mis tareas están en "completed"?
   ☐ ¿Marqué todos los criterios de aceptación?
   ☐ ¿Resolví todos los devlog entries críticos?
        │
        ▼
3. Agente va a: Sprint → Stage → [Firmar Stage]
        │
        ▼
4. Sistema valida automáticamente los criterios
        │
        ├── Si falla → Muestra qué falta
        │
        └── Si pasa → Stage firmado
                │
                ▼
5. Se registra:
   - Quién firmó
   - Cuándo firmó
   - Tareas incluidas
```

#### Ejemplo:

```
Sprint: S05-Trazabilidad
Stage: Development

Agente: BE-Agent
Tareas:
  ✅ VTT-350: Implementar TaskDevlogEntry (completed)
  ✅ VTT-351: Implementar AcceptanceCriteria (completed)
  ✅ VTT-352: Implementar TaskCriteriaFulfillment (completed)

BE-Agent puede firmar el stage Development.
```

#### ¿Qué pasa si otro agente no ha terminado?

Cada agente firma **sus propias tareas**. No necesitas esperar a otros agentes del mismo stage. El stage completo se considera "firmado" cuando **todos los agentes** que tienen tareas ahí han firmado.

---

### NIVEL 2: FIRMA DE SPRINT

#### ¿Quién firma?
- **TL** (Team Lead) — obligatorio
- **AR** (Architect) — obligatorio
- **QA** — obligatorio
- **DL** (Designer) — solo si hubo tareas de FE/UX

#### ¿Cuándo se puede firmar?
Cuando **TODOS los stages** del sprint están firmados por todos sus agentes.

#### Criterios para firmar Sprint:

| # | Criterio | Validado por | Obligatorio |
|---|----------|--------------|-------------|
| 1 | Todos los stages firmados | Sistema | ✅ |
| 2 | Code review completado | AR | ✅ |
| 3 | Integration tests pasaron | TL | ✅ |
| 4 | QA tests pasaron | QA | ✅ |
| 5 | No hay bugs blocker abiertos | Sistema | ✅ |
| 6 | Hardcode check pasó | Sistema | ✅ |
| 7 | Documentación actualizada | AR | Recomendado |

#### Proceso paso a paso:

```
1. Todos los stages del sprint están firmados
        │
        ▼
2. Sistema notifica a TL/AR/QA que pueden firmar
        │
        ▼
3. Cada firmante revisa:
   
   AR revisa:
   ☐ Code review de todos los PRs
   ☐ Arquitectura consistente
   ☐ ADRs documentados
   
   TL revisa:
   ☐ Integration tests pasan
   ☐ No hay blockers pendientes
   ☐ Scope completado
   
   QA revisa:
   ☐ Test cases ejecutados
   ☐ Bugs críticos resueltos
   ☐ Regresiones verificadas
        │
        ▼
4. Cada firmante va a: Sprint → [Firmar Sprint]
        │
        ▼
5. Cada firmante marca sus validaciones:
   ☑ codeReviewPassed: true
   ☑ integrationPassed: true
   ☑ testsPassed: true
   ☑ hardcodeCheckPassed: true
        │
        ▼
6. Sistema registra firma con timestamp
        │
        ▼
7. Cuando TODOS firmaron → Sprint cerrado
```

#### Campos de la firma de Sprint:

```json
{
  "sprintId": "uuid",
  "signedBy": "uuid-del-firmante",
  "role": "TL",
  "signedAt": "2026-04-12T10:00:00Z",
  "validations": {
    "codeReviewPassed": true,
    "integrationPassed": true,
    "testsPassed": true,
    "hardcodeCheckPassed": true
  },
  "comments": "Todo verificado. PRs #120-#125 revisados."
}
```

#### Delegación de firma:

Si TL no está disponible, puede **delegar** su firma a otro rol senior:

```json
{
  "signedBy": "uuid-ar",
  "delegatedBy": "uuid-tl",
  "delegationReason": "TL de vacaciones, AR asume responsabilidad",
  "delegatedAt": "2026-04-12T09:00:00Z"
}
```

**Regla:** Delegación solo permitida en Sprint y Release, NO en Stage.

---

### NIVEL 3: FIRMA DE RELEASE

#### ¿Quién firma?
- **PJM** (Project Manager Agent) — obligatorio
- **PM** (Product Manager / Martin) — obligatorio
- **Stakeholders externos** — opcional, si `externalApprovalRequired = true`

#### ¿Cuándo se puede firmar?
Cuando **TODOS los sprints** del release están firmados.

#### Criterios para firmar Release:

| # | Criterio | Validado por | Obligatorio |
|---|----------|--------------|-------------|
| 1 | Todos los sprints firmados | Sistema | ✅ |
| 2 | Deployment a staging exitoso | DevOps/TL | ✅ |
| 3 | Smoke tests en staging pasaron | QA | ✅ |
| 4 | Release notes documentados | PJM | ✅ |
| 5 | Rollback plan definido | TL | ✅ |
| 6 | Aprobación de stakeholders | PM | Si aplica |

#### Proceso paso a paso:

```
1. Todos los sprints del release están firmados
        │
        ▼
2. PJM prepara:
   ☐ Release notes
   ☐ Lista de cambios
   ☐ Breaking changes (si hay)
   ☐ Instrucciones de deployment
        │
        ▼
3. Deploy a staging
        │
        ▼
4. QA ejecuta smoke tests en staging
        │
        ▼
5. Si todo OK:
   - PJM firma
   - PM firma
   - (Stakeholders firman si aplica)
        │
        ▼
6. Release cerrado → Listo para producción
```

#### Campos de la firma de Release:

```json
{
  "releaseId": "uuid",
  "signedBy": "uuid-pm",
  "role": "PM",
  "signedAt": "2026-04-12T14:00:00Z",
  "approvalType": "full_approval",
  "comments": "Release aprobado para producción. Deploy programado para 2026-04-13 06:00 UTC."
}
```

---

### RESUMEN DE FLUJO COMPLETO

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        FLUJO DE FIRMAS                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  STAGE (por cada fase del sprint)                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ BE-Agent firma ───┐                                                 │   │
│  │ FE-Agent firma ───┼──► Stage Development firmado                   │   │
│  │ DB-Agent firma ───┘                                                 │   │
│  │                                                                     │   │
│  │ QA-Agent firma ──────► Stage Testing firmado                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                           │                                                 │
│                           ▼                                                 │
│  SPRINT                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Todos los stages firmados                                          │   │
│  │         │                                                           │   │
│  │         ▼                                                           │   │
│  │ TL firma (code review, integration) ───┐                           │   │
│  │ AR firma (arquitectura, ADRs) ─────────┼──► Sprint firmado         │   │
│  │ QA firma (tests, bugs) ────────────────┤                           │   │
│  │ DL firma (si hubo FE) ─────────────────┘                           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                           │                                                 │
│                           ▼                                                 │
│  RELEASE                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Todos los sprints firmados                                          │   │
│  │         │                                                           │   │
│  │         ▼                                                           │   │
│  │ Deploy a staging ──► Smoke tests ──► OK                            │   │
│  │         │                                                           │   │
│  │         ▼                                                           │   │
│  │ PJM firma (release notes) ─────────┐                               │   │
│  │ PM firma (aprobación final) ───────┼──► Release cerrado            │   │
│  │ Stakeholders (si aplica) ──────────┘                               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                           │                                                 │
│                           ▼                                                 │
│                    🚀 PRODUCCIÓN                                            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### BLOQUEOS

| Nivel | No puedes firmar si... |
|-------|------------------------|
| Stage | Tienes tareas no completadas |
| Stage | Hay criterios de aceptación pendientes |
| Stage | Hay devlog entries `critical`/`high` pendientes |
| Sprint | Hay stages sin firmar |
| Sprint | Hay bugs blocker abiertos |
| Sprint | Code review no completado |
| Release | Hay sprints sin firmar |
| Release | Smoke tests no pasaron |

---

### IRREVERSIBILIDAD

**Las firmas son irreversibles.**

- Una vez firmado, no se puede "desfirmar"
- Si se encuentra un problema después de firmar → va a **proceso de bugs/support**
- El bug se resuelve en un **sprint futuro**, no se reabre el firmado

---

### TABLAS EN BASE DE DATOS

| Tabla | Nivel | Campos clave |
|-------|-------|--------------|
| `stage_approvals` | Stage | sprintId, phaseCode, signedBy, signedAt |
| `sprint_approvals` | Sprint | sprintId, signedBy, role, validations, delegatedBy |
| `release_approvals` | Release | releaseId, signedBy, role, approvalType |

---

## 12. RELEASES Y SPRINTS

### ¿Qué es?

**Release:** Una versión del proyecto (MVP, V2.0, V3.0)

**Sprint:** Una iteración de tiempo dentro de un release (Sprint 1, Sprint 2)

### ¿Para qué sirve?
- Organizar el trabajo en ciclos
- Planificar entregas
- Medir progreso

### ¿Cuándo usar sprints?

| Metodología | ¿Usa sprints? |
|-------------|---------------|
| Scrum | ✅ Sí (típico 2 semanas) |
| Kanban | ❌ No |
| Waterfall | ❌ No |
| Hybrid | Opcional |

### Jerarquía

```
PROYECTO: VTT
    │
    ├── RELEASE: MVP
    │       ├── Sprint 1
    │       ├── Sprint 2
    │       └── Sprint 3
    │
    ├── RELEASE: V2.0
    │       ├── Sprint 4
    │       └── Sprint 5
    │
    └── RELEASE: V3.0
            └── ...
```

### Reglas importantes

1. **Releases son lineales** — MVP se completa antes de V2.0
2. **No crees proyecto nuevo para cada versión** — crea un RELEASE
3. **Sprints son opcionales** — solo si la metodología los requiere

---

## RESUMEN: ¿QUÉ USAR CUÁNDO?

| Situación | Feature a usar |
|-----------|----------------|
| Quiero saber qué debe cumplir mi tarea | Criterios de Aceptación |
| Terminé y quiero marcar qué cumplí | Fulfillment |
| Tomé una decisión durante mi trabajo | Devlog entry (decision) |
| Algo me bloquea | Devlog entry (blocker) |
| Encontré algo que mejorar después | Devlog entry (tech_debt) |
| Mi tarea depende de otra | Link (depends_on) |
| Modifiqué documentación | Document Impact |
| No puedo pasar a review | Revisar Review Gate |
| Quiero que la documentación se auto-actualice | Living Document |
| Debo rastrear un requerimiento | Trackable Item (RF) |
| Tomé una decisión arquitectónica importante | Trackable Item (ADR) |
| Decidimos cómo vamos a trabajar | Trackable Item (ADR-PROC) |
| Algo se pospone a futuro | Deferred Scope |
| Quiero verificar que no tengo datos hardcodeados | Hardcode Check |
| Terminé mi fase/sprint | Firma |

---

## 13. TASK TYPES

### ¿Qué es?
Clasificación de tareas por tipo de trabajo. Determina qué DoD se hereda automáticamente.

### Tipos disponibles

| taskTypeCode | Nombre | DoD heredado | Cuándo usar |
|--------------|--------|--------------|-------------|
| `backend` | Backend Development | DOD-BE (12 items) | Endpoints, servicios, lógica |
| `frontend` | Frontend Development | DOD-FE (9 items) | Componentes UI, vistas |
| `database` | Database | DOD-BE | Schema, migrations, seeds |
| `documentation` | Documentation / Analysis | DOD-DOC (8 items) | Documentos, análisis, specs |
| `testing` | QA Testing | DOD-QA (6 items) | Tests, validación |
| `devops` | Infrastructure / DevOps | DOD-BE subset | Docker, CI/CD, deployment |
| `design` | Design | DOD-DL | Wireframes, design system |
| `research` | Research | Ninguno | Investigación, spikes, PoC |
| `meeting` | Meeting | Ninguno | Reuniones, ceremonies |

### ¿Cómo funciona?

**Automático:** Al crear una tarea, el sistema infiere el taskTypeCode del rol del asignado:

| Rol asignado | taskTypeCode inferido |
|--------------|----------------------|
| BE-Agent | `backend` |
| FE-Agent | `frontend` |
| SA, AR | `documentation` |
| QA | `testing` |
| DL | `design` |

**Manual:** PM/TL puede cambiar el taskTypeCode si el inferido no es correcto.

### Ejemplo

```
PM crea tarea y asigna a BE-Agent
    │
    ▼
Sistema infiere: taskTypeCode = "backend"
    │
    ▼
Sistema hereda:
  - 14 criterios DOR (Definition of Ready)
  - 12 criterios DOD-BE (Definition of Done Backend)
    │
    ▼
Tarea lista con 26 criterios automáticamente
```

### Cambiar taskTypeCode

Si la tarea fue asignada al agente incorrecto:

1. PM/TL edita la tarea
2. Cambia `taskTypeCode` de "backend" a "documentation"
3. Sistema pregunta: "Los DoD cambiarán. ¿Confirmar?"
4. PM confirma
5. Se eliminan DOD-BE, se agregan DOD-DOC

---

## ERRORES COMUNES

| Error | Corrección |
|-------|------------|
| Poner bugs en devlog | Los bugs tienen proceso separado |
| Crear proyecto nuevo para cada versión | Crear RELEASE dentro del proyecto |
| No registrar decisiones | Usar devlog entry tipo "decision" |
| Ignorar criterios de aceptación | Revisarlos ANTES de empezar |
| Intentar avanzar con blockers | Resolver primero, luego avanzar |
| No vincular tareas dependientes | Crear links de dependencia |
| Olvidar impactos en documentos | Registrar qué docs modificaste |
| Iniciar tarea sin cumplir DoR | Verificar DoR primero o pedir override |
| Marcar DoD sin evidencia | Siempre incluir evidencia (PR, test, etc.) |
| No esperar verificación de TL | DoD debe estar "verified", no solo "reported" |

---

**Documento:** MANUAL_FEATURES_VTT_V4.md  
**Versión:** 2.0  
**Fecha:** 2026-05-06
