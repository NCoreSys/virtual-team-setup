# ADDENDUM: Ejecución, Registro e Integración UX — V4.5

| Campo | Valor |
|-------|-------|
| **Documento** | ADDENDUM_EJECUCION_REGISTRO_INTEGRACION_V4.5.md |
| **Versión** | 1.0 |
| **Fecha** | 2026-04-12 |
| **Autor** | PM (Martin Rivas) |
| **Tipo** | Addendum — ALTER + UX |
| **Documento base** | SPEC_FUNCIONAL_MODELO_DINAMICO_V4_CONSOLIDADO_v1.4.3.md |
| **Estado** | ✅ APROBADO PM |

---

## 1. PROBLEMA

1. `TaskDevlogEntry` no tiene campo `status` — solo `resolvedAt` que no permite flujo completo
2. Las APIs V4 (S01-S11) están funcionando pero no hay UI para usarlas
3. No hay gate de revisión que bloquee tareas con entries critical/high pendientes

---

## 2. CAMBIOS EN MODELO DE DATOS

### 2.1 ALTER: TaskDevlogEntry

```prisma
model TaskDevlogEntry {
  // ... campos existentes ...
  
  // NUEVO CAMPO
  status String @default("pending") // pending | acknowledged | in_progress | resolved | deferred | wont_fix
  
  // ... resto igual ...
}
```

**Migración:**

```sql
ALTER TABLE task_devlog_entries 
ADD COLUMN status VARCHAR(50) DEFAULT 'pending';

-- Backfill: si resolvedAt no es null, status = 'resolved'
UPDATE task_devlog_entries 
SET status = 'resolved' 
WHERE resolved_at IS NOT NULL;

-- Backfill: si deferredToPhaseId no es null, status = 'deferred'
UPDATE task_devlog_entries 
SET status = 'deferred' 
WHERE deferred_to_phase_id IS NOT NULL AND resolved_at IS NULL;
```

### 2.2 Estados de TaskDevlogEntry

| status | Descripción | Quién cambia |
|--------|-------------|--------------|
| `pending` | Recién creado por agente | Agente |
| `acknowledged` | TL/PM lo vio | TL/PM |
| `in_progress` | Se está trabajando (tiene fixTaskId) | TL |
| `resolved` | Resuelto | TL/PM |
| `deferred` | Diferido a otra fase | TL/PM |
| `wont_fix` | No se va a resolver | TL/PM |

---

## 3. GATE DE REVISIÓN

### 3.1 Endpoint

```
GET /api/tasks/:taskId/review-gate
```

### 3.2 Response

```json
{
  "canProceedToReview": false,
  "blockers": [
    {
      "id": "uuid",
      "categoryCode": "blocker",
      "severity": "critical",
      "title": "Admin debe ejecutar migración",
      "status": "pending"
    }
  ],
  "warnings": [
    {
      "id": "uuid",
      "categoryCode": "tech_debt",
      "severity": "medium",
      "title": "Refactorizar TimeService"
    }
  ],
  "summary": {
    "total": 5,
    "pending": 2,
    "acknowledged": 1,
    "resolved": 2
  }
}
```

### 3.3 Lógica

```typescript
canProceedToReview = devlogEntries
  .filter(e => e.severity IN ('critical', 'high') && e.status === 'pending')
  .length === 0
```

### 3.4 Integración con Task Status

```typescript
// TaskService.updateStatus()
if (newStatus === 'task_in_review') {
  const gate = await this.getReviewGate(taskId);
  if (!gate.canProceedToReview) {
    throw new HttpException({
      statusCode: 422,
      message: 'Cannot proceed to review - pending critical/high entries',
      blockers: gate.blockers
    }, 422);
  }
}
```

---

## 4. ENDPOINTS NUEVOS/MODIFICADOS

### 4.1 Devlog Entries

| Método | Ruta | Descripción | Sprint |
|--------|------|-------------|--------|
| `PATCH` | `/api/devlog-entries/:id/status` | Cambiar status | S12-BE |
| `GET` | `/api/tasks/:taskId/review-gate` | Verificar gate | S12-BE |
| `GET` | `/api/sprints/:sprintId/devlog-summary` | Resumen del sprint | S12-BE |

### 4.2 Request/Response

**PATCH /api/devlog-entries/:id/status**

```json
// Request
{
  "status": "resolved",
  "resolution": "Migración ejecutada por Admin"
}

// Response
{
  "id": "uuid",
  "status": "resolved",
  "resolvedBy": "user-id",
  "resolvedAt": "2026-04-12T10:00:00Z",
  "resolution": "Migración ejecutada por Admin"
}
```

---

## 5. INTEGRACIÓN UX — SPRINT S12

### 5.1 Resumen

| Módulo | Pantallas | Componentes | Horas |
|--------|-----------|-------------|-------|
| A: Admin Catálogos | 11 | 6 | 20h |
| B: Releases/Sprints | 8 | 6 | 16h |
| C: Trackables | 6 | 7 | 18h |
| D: Criterios | 5 | 6 | 12h |
| E: Devlog/Gate | 5 | 8 | 14h |
| F: Documents | 5 | 7 | 14h |
| G: Compliance | 3 | 4 | 8h |
| H: Signatures | 5 | 7 | 12h |
| I: Project Wizard | 2 | — | 10h |
| J: Navegación | 3 | — | 6h |
| **TOTAL** | **53** | **51** | **130h** |

### 5.2 Módulo E: Devlog/Gate (Detalle)

#### Pantallas

| # | Pantalla | Ruta | Descripción |
|---|----------|------|-------------|
| E1 | Devlog de Tarea | `/tasks/:id/devlog` | Lista de entries con filtros |
| E2 | Crear Entry | Modal | Formulario nuevo entry |
| E3 | Resolver Entry | Modal | Cambiar status con resolución |
| E4 | Review Gate Tarea | `/tasks/:id/review-gate` | Ver blockers/warnings |
| E5 | Devlog Sprint | `/sprints/:id/devlog` | Consolidado del sprint |

#### Componentes

| # | Componente | Uso |
|---|------------|-----|
| CE1 | DevlogEntryCard | Tarjeta con severity badge y status |
| CE2 | DevlogEntryForm | Formulario crear entry |
| CE3 | StatusBadge | Badge pending/acknowledged/resolved/etc |
| CE4 | SeverityBadge | Badge critical/high/medium/low |
| CE5 | CategoryFilter | Filtro por categoría |
| CE6 | GateStatus | Indicador can/cannot proceed |
| CE7 | ResolveForm | Formulario resolver/diferir |
| CE8 | DevlogSummary | Resumen por status/severity |

#### Wireframe E1: Devlog de Tarea

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Task: VTT-367 - QA Sources/Impacts                      [Review Gate]  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│ [Filtros: Todos | Pending | Resolved] [Categoría ▼] [Severity ▼]       │
│                                                                         │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ 🔴 CRITICAL | blocker | PENDING                                     │ │
│ │ Admin debe ejecutar migrate resolve                                  │ │
│ │ Reportado: 2026-04-04 por QA-Agent                                  │ │
│ │ [Acknowledge] [Resolve] [Defer] [Create Fix Task]                    │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ 🟡 MEDIUM | tech_debt | ACKNOWLEDGED                                │ │
│ │ Refactorizar TimeService                                             │ │
│ │ Reportado: 2026-04-04 | Acknowledged: 2026-04-05 por TL             │ │
│ │ [Resolve] [Defer]                                                    │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ ✅ | decision | RESOLVED                                            │ │
│ │ Usar UTC para todos los cálculos                                     │ │
│ │ Resuelto: 2026-04-05 por TL                                          │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ [+ Nuevo Entry]                                                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### Wireframe E4: Review Gate

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Review Gate: VTT-367                                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │                                                                     │ │
│ │   ❌ NO PUEDE PASAR A REVIEW                                       │ │
│ │                                                                     │ │
│ │   1 entry critical/high pendiente                                   │ │
│ │                                                                     │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ BLOCKERS (resolver para continuar):                                    │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ 🔴 CRITICAL | blocker                                               │ │
│ │ Admin debe ejecutar migrate resolve                                  │ │
│ │ [Resolve] [Defer]                                                    │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ RESUMEN:                                                                │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Total: 5 | Pending: 1 | Acknowledged: 1 | Resolved: 3              │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 5.3 Resto de Módulos

Ver documento BRIEF_S12_INTEGRACION_FE_MODELO_DINAMICO_V4.md para detalle completo de:
- Módulo A: Admin Catálogos
- Módulo B: Releases/Sprints
- Módulo C: Trackables
- Módulo D: Criterios
- Módulo F: Documents
- Módulo G: Compliance
- Módulo H: Signatures
- Módulo I: Project Wizard
- Módulo J: Navegación

---

## 6. SPRINTS DE IMPLEMENTACIÓN

### 6.1 S12-A: ALTER + Gate (BE)

| Tarea | Descripción | Horas |
|-------|-------------|-------|
| DB-S12-A | ALTER task_devlog_entries + backfill | 2h |
| BE-S12-A1 | PATCH /devlog-entries/:id/status | 2h |
| BE-S12-A2 | GET /tasks/:id/review-gate | 3h |
| BE-S12-A3 | Integrar gate con TaskService.updateStatus() | 3h |
| **Total** | | **10h** |

### 6.2 S12-B: Integración FE

| Fase | Módulos | Horas |
|------|---------|-------|
| Fase 1 | A: Admin + J: Navegación | 26h |
| Fase 2 | B: Releases + C: Trackables | 34h |
| Fase 3 | D: Criterios + E: Devlog | 26h |
| Fase 4 | F: Documents + G: Compliance | 22h |
| Fase 5 | H: Signatures + I: Wizard | 22h |
| **Total** | | **130h** |

---

## 7. DECISIONES PM CONGELADAS

| # | Decisión | Resolución |
|---|----------|------------|
| D-40 | Campo status en TaskDevlogEntry | ✅ Agregar |
| D-41 | Gate bloquea task_in_review | ✅ Sí, 422 si hay critical/high pending |
| D-42 | Estados de status | ✅ pending, acknowledged, in_progress, resolved, deferred, wont_fix |

---

## 8. MÉTRICAS

| Métrica | Valor |
|---------|-------|
| Tablas ALTER | 1 (task_devlog_entries) |
| Endpoints nuevos | 3 |
| Pantallas FE | 53 |
| Componentes FE | 51 |
| Horas BE | 10h |
| Horas FE | 130h |
| **Total** | **140h** |

---

## 9. FIRMA

| Rol | Firma | Fecha |
|-----|-------|-------|
| PM | ✅ Aprobado | 2026-04-12 |

---

**Documento:** ADDENDUM_EJECUCION_REGISTRO_INTEGRACION_V4.5.md  
**Versión:** 1.0  
**Fecha:** 2026-04-12
