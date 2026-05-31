# HANDOFF PJM — ADDENDUM V4.5: Ejecución, Registro e Integración UX

| Campo | Valor |
|-------|-------|
| **Documento** | HANDOFF_PJM_ADDENDUM_V4.5.md |
| **Versión** | 1.0 |
| **Fecha** | 2026-04-12 |
| **De** | PM (Martin Rivas) |
| **Para** | PJM |
| **Referencia** | ADDENDUM_EJECUCION_REGISTRO_INTEGRACION_V4.5.md |
| **Estado** | ✅ LISTO PARA EJECUCIÓN |

---

## 1. RESUMEN EJECUTIVO

| Métrica | Valor |
|---------|-------|
| ALTER tables | 1 |
| Endpoints nuevos | 3 |
| Pantallas FE | 53 |
| Componentes FE | 51 |
| Horas BE | 10h |
| Horas FE | 130h |
| **Total** | **140h** |

---

## 2. DECISIONES PM CONGELADAS

| # | Decisión | Resolución |
|---|----------|------------|
| D-40 | Campo status en TaskDevlogEntry | ✅ Agregar |
| D-41 | Gate bloquea task_in_review | ✅ Sí, 422 si hay critical/high pending |
| D-42 | Estados de status | ✅ pending, acknowledged, in_progress, resolved, deferred, wont_fix |

---

## 3. SPRINT S12-A: ALTER + GATE (BE)

**Responsable:** DB Engineer + BE Engineer  
**Horas:** 10h  
**Dependencias:** Ninguna

### 3.1 Tareas

| # | Tarea | Rol | Horas | Entregable |
|---|-------|-----|-------|------------|
| 1 | ALTER task_devlog_entries ADD status | DB | 2h | Migración SQL |
| 2 | PATCH /api/devlog-entries/:id/status | BE | 2h | Endpoint |
| 3 | GET /api/tasks/:taskId/review-gate | BE | 3h | Endpoint |
| 4 | Integrar gate con TaskService.updateStatus() | BE | 3h | 422 en task_in_review |

### 3.2 Migración SQL

```sql
-- Archivo: 20260412000001_add_status_to_devlog_entries.sql

ALTER TABLE task_devlog_entries 
ADD COLUMN status VARCHAR(50) DEFAULT 'pending';

-- Backfill
UPDATE task_devlog_entries 
SET status = 'resolved' 
WHERE resolved_at IS NOT NULL;

UPDATE task_devlog_entries 
SET status = 'deferred' 
WHERE deferred_to_phase_id IS NOT NULL AND resolved_at IS NULL;
```

### 3.3 Schema Prisma

```prisma
model TaskDevlogEntry {
  // ... campos existentes ...
  status String @default("pending") // NUEVO
  // ... resto igual ...
}
```

### 3.4 Endpoints

| Método | Ruta | Request | Response |
|--------|------|---------|----------|
| PATCH | /api/devlog-entries/:id/status | `{ status, resolution? }` | Entry actualizado |
| GET | /api/tasks/:taskId/review-gate | — | `{ canProceedToReview, blockers[], warnings[], summary }` |
| GET | /api/sprints/:sprintId/devlog-summary | — | Resumen por status/severity |

### 3.5 Lógica del Gate

```typescript
// TaskService.updateStatus()
if (newStatus === 'task_in_review') {
  const entries = await prisma.taskDevlogEntry.findMany({
    where: { 
      taskId,
      severity: { in: ['critical', 'high'] },
      status: 'pending'
    }
  });
  
  if (entries.length > 0) {
    throw new HttpException({
      statusCode: 422,
      message: 'Cannot proceed to review - pending critical/high entries',
      blockers: entries
    }, 422);
  }
}
```

---

## 4. SPRINT S12-B: INTEGRACIÓN FE

**Responsable:** FE Engineer + DL  
**Horas:** 130h  
**Dependencias:** S12-A completado

### 4.1 Fases

| Fase | Módulos | Pantallas | Componentes | Horas |
|------|---------|-----------|-------------|-------|
| 1 | A: Admin + J: Navegación | 14 | 6 | 26h |
| 2 | B: Releases + C: Trackables | 14 | 13 | 34h |
| 3 | D: Criterios + E: Devlog | 10 | 14 | 26h |
| 4 | F: Documents + G: Compliance | 8 | 11 | 22h |
| 5 | H: Signatures + I: Wizard | 7 | 7 | 22h |

### 4.2 Módulo A: Admin Catálogos (20h)

| # | Pantalla | Ruta |
|---|----------|------|
| A1 | Admin Dashboard | /admin |
| A2 | Catálogo Tipos de Proyecto | /admin/project-types |
| A3 | Catálogo Fases | /admin/phases |
| A4 | Catálogo Deliverables | /admin/deliverables |
| A5 | Catálogo Trackable Types | /admin/trackable-types |
| A6 | Flow Templates | /admin/flow-templates |
| A7 | Flow Template Detail | /admin/flow-templates/:id |
| A8 | Catálogo Criteria Types | /admin/criteria-types |
| A9 | Catálogo Devlog Categories | /admin/devlog-categories |
| A10 | Catálogo Link Types | /admin/link-types |
| A11 | Catálogo Living Doc Sources | /admin/living-doc-sources |

### 4.3 Módulo B: Releases/Sprints (16h)

| # | Pantalla | Ruta |
|---|----------|------|
| B1 | Lista de Releases | /projects/:id/releases |
| B2 | Detalle Release | /projects/:id/releases/:releaseId |
| B3 | Crear Release | /projects/:id/releases/new |
| B4 | Editar Release | /projects/:id/releases/:releaseId/edit |
| B5 | Lista de Sprints | /projects/:id/releases/:releaseId/sprints |
| B6 | Detalle Sprint | /projects/:id/sprints/:sprintId |
| B7 | Crear Sprint | /projects/:id/releases/:releaseId/sprints/new |
| B8 | Board del Sprint | /projects/:id/sprints/:sprintId/board |

### 4.4 Módulo C: Trackables (18h)

| # | Pantalla | Ruta |
|---|----------|------|
| C1 | Lista Trackable Items | /projects/:id/trackables |
| C2 | Detalle Trackable | /projects/:id/trackables/:itemId |
| C3 | Crear Trackable | /projects/:id/trackables/new |
| C4 | Matriz de Trazabilidad | /projects/:id/traceability |
| C5 | Deferred Items | /projects/:id/trackables/deferred |
| C6 | Links de Trackable | /projects/:id/trackables/:itemId/links |

### 4.5 Módulo D: Criterios (12h)

| # | Pantalla | Ruta |
|---|----------|------|
| D1 | Lista Criterios | /projects/:id/criteria |
| D2 | Detalle Criterio | /projects/:id/criteria/:criteriaId |
| D3 | Crear Criterio | /projects/:id/criteria/new |
| D4 | Fulfillment por Tarea | /tasks/:id/fulfillment |
| D5 | Cobertura de Criterios | /projects/:id/criteria-coverage |

### 4.6 Módulo E: Devlog/Gate (14h)

| # | Pantalla | Ruta |
|---|----------|------|
| E1 | Devlog de Tarea | /tasks/:id/devlog |
| E2 | Crear Entry | Modal |
| E3 | Resolver Entry | Modal |
| E4 | Review Gate Tarea | /tasks/:id/review-gate |
| E5 | Devlog Sprint | /sprints/:id/devlog |

**Componentes:**
- DevlogEntryCard
- DevlogEntryForm
- StatusBadge
- SeverityBadge
- CategoryFilter
- GateStatus
- ResolveForm
- DevlogSummary

### 4.7 Módulo F: Documents (14h)

| # | Pantalla | Ruta |
|---|----------|------|
| F1 | Explorador de Docs | /projects/:id/documents |
| F2 | Detalle Documento | /projects/:id/documents/:docId |
| F3 | Crear Documento | /projects/:id/documents/new |
| F4 | Configurar Living Doc | /projects/:id/documents/:docId/sources |
| F5 | Document Impacts | /tasks/:id/document-impacts |

### 4.8 Módulo G: Compliance (8h)

| # | Pantalla | Ruta |
|---|----------|------|
| G1 | Lista Compliance Checks | /admin/compliance-checks |
| G2 | Compliance de Tarea | /tasks/:id/compliance |
| G3 | Compliance del Sprint | /sprints/:id/compliance |

### 4.9 Módulo H: Signatures (12h)

| # | Pantalla | Ruta |
|---|----------|------|
| H1 | Firmas de Fase | /phases/:id/approvals |
| H2 | Firmas de Sprint | /sprints/:id/approvals |
| H3 | Firmas de Release | /releases/:id/approvals |
| H4 | Findings de Tarea | /tasks/:id/findings |
| H5 | Hardcode Check | /tasks/:id/hardcode-check |

### 4.10 Módulo I: Project Wizard (10h)

| # | Pantalla | Ruta |
|---|----------|------|
| I1 | Integrar Wizard al flujo | /projects/new/step/:step |
| I2 | Integrar Settings al menú | /projects/:id/settings/:tab |

### 4.11 Módulo J: Navegación (6h)

| # | Tarea |
|---|-------|
| J1 | Actualizar Sidebar con nuevas rutas |
| J2 | Agregar rutas al router |
| J3 | Breadcrumbs para nuevas pantallas |

---

## 5. NAVEGACIÓN FINAL

```
SIDEBAR
├── [+ Nuevo Proyecto] → /projects/new/step/1
│
├── 📁 {Proyecto}
│   ├── 📋 Overview
│   ├── 📦 Releases → /projects/:id/releases
│   ├── 🎯 Trackables → /projects/:id/trackables
│   ├── ✅ Criterios → /projects/:id/criteria
│   ├── 📄 Documentos → /projects/:id/documents
│   ├── 📊 Trazabilidad → /projects/:id/traceability
│   └── ⚙️ Settings → /projects/:id/settings
│
├── 📋 Tasks
│   └── {Task}
│       ├── 📝 Devlog → /tasks/:id/devlog
│       ├── 🚦 Review Gate → /tasks/:id/review-gate
│       └── ...
│
└── ⚙️ Admin
    ├── Catálogos → /admin
    └── Compliance → /admin/compliance-checks
```

---

## 6. SECUENCIA DE EJECUCIÓN

```
SEMANA 1:
├── DB: ALTER task_devlog_entries (2h)
├── BE: Endpoints status + gate (8h)
└── FE: Inicia Fase 1 (Admin + Nav)

SEMANA 2:
└── FE: Fase 1 completa + Inicia Fase 2

SEMANA 3:
└── FE: Fase 2 completa (Releases + Trackables)

SEMANA 4:
└── FE: Fase 3 completa (Criterios + Devlog)

SEMANA 5:
└── FE: Fase 4 completa (Documents + Compliance)

SEMANA 6:
├── FE: Fase 5 completa (Signatures + Wizard)
└── QA: Testing integración
```

---

## 7. CRITERIOS DE ACEPTACIÓN

| # | Criterio |
|---|----------|
| CA-01 | ALTER task_devlog_entries con campo status aplicado |
| CA-02 | PATCH /devlog-entries/:id/status funciona |
| CA-03 | GET /tasks/:id/review-gate retorna blockers |
| CA-04 | TaskService.updateStatus() retorna 422 si hay critical/high pending |
| CA-05 | 53 pantallas FE implementadas y navegables |
| CA-06 | Sidebar actualizado con nuevas rutas |
| CA-07 | Wizard de proyecto integrado al flujo |

---

## 8. HANDOFFS A GENERAR

| Rol | Documento | Contenido |
|-----|-----------|-----------|
| DB | BRIEF_DB_S12A.md | Migración SQL |
| BE | BRIEF_BE_S12A.md | Endpoints + gate logic |
| FE | BRIEF_FE_S12B.md | Pantallas + componentes |
| DL | BRIEF_DL_S12B.md | Wireframes + diseño |
| QA | BRIEF_QA_S12.md | Test plan |

---

## 9. FIRMA

| Rol | Firma | Fecha |
|-----|-------|-------|
| PM | ✅ Aprobado | 2026-04-12 |
| PJM | ⬜ Pendiente | |

---

**Documento:** HANDOFF_PJM_ADDENDUM_V4.5.md  
**Versión:** 1.0  
**Fecha:** 2026-04-12

---

**PM — Martin Rivas**  
CEO/Founder — Virtual Teams Tracking
