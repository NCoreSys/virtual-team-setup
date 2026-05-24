# CIERRE PM + HANDOFF OPERATIVO PJM — VTT MODELO DINÁMICO V4

| Campo | Valor |
|-------|-------|
| **Documento** | CIERRE_PM_HANDOFF_PJM_MODELO_DINAMICO_V4.2.md |
| **Versión** | 4.2.0 |
| **Fecha** | 2026-03-30 |
| **Fase SDLC** | 02-Analysis → Cierre |
| **Autor** | PM (Martin Rivas) |
| **Destinatario** | PJM (Project Manager) |
| **Estado** | ✅ CERRADO — Listo para ejecución |

---

## PARTE I: CIERRE PM DEL ANÁLISIS

### 1. DOCUMENTOS CONSUMIDOS

| # | Documento | Versión | Autor | Estado |
|---|-----------|---------|-------|--------|
| 1 | SPEC_FUNCIONAL_MODELO_DINAMICO_V4_CONSOLIDADO.md | 1.1.0 | SA-Agent | ✅ Base final |
| 2 | AR_ANALISIS_VTT_MODELO_DINAMICO_V4.3.md | 4.3.0 | AR | ✅ Cerrado |
| 3 | AR_ADDENDUM_DEFERRED_SCOPE_TRACKING_V2.md | 2.0 | AR | ✅ Integrado |
| 4 | REPORTE_REVISION_DB_MODELO_DINAMICO_V4.md | 1.0 | DB Engineer | ✅ Aprobado con obs |
| 5 | REPORTE_REVISION_DB_ADDENDUM_DEFERRED_SCOPE_V2.md | 1.0 | DB Engineer | ✅ Aprobado con correcciones |
| 6 | REPORTE_REVISION_TL_MODELO_DINAMICO_V4.md | 1.0.0 | TL-Agent | ✅ Aprobado |
| 7 | REPORTE_REVISION_BE_MODELO_DINAMICO_V4.md | 1.0 | BE Engineer | ✅ Aprobado con obs |

### 2. DECISIONES PM FINALES (D-01 a D-17)

Todas las decisiones están **CONGELADAS**. No se reabren.

#### Decisiones Base V4 (D-01 a D-12)

| # | Decisión | Estado |
|---|----------|--------|
| D-01 | `deliveries` ya existe y se **EXTIENDE** (ALTER, no CREATE) | ✅ FROZEN |
| D-02 | MVP mantiene relación **1:N** con `Task.deliveryId` (no N:M) | ✅ FROZEN |
| D-03 | Tabla documental objetivo es `project_documents`; `documents` queda legacy | ✅ FROZEN |
| D-04 | `document_index` referencia `project_documents.id` | ✅ FROZEN |
| D-05 | `DocumentIndex.projectDocumentId` es **PK única** (sin `id` separado) | ✅ FROZEN |
| D-06 | `changeControl` = `fixed \| controlled \| dynamic` | ✅ FROZEN |
| D-07 | BD es fuente de verdad; FileSystem es espejo **BD → FS** unidireccional | ✅ FROZEN |
| D-08 | Backend VTT es **escritor único**; Knowledge Service solo consulta | ✅ FROZEN |
| D-09 | Living Docs MVP = solo **Schema + API Endpoints** | ✅ FROZEN |
| D-10 | Indexación **post-commit asíncrona** con reintento + endpoint `/reindex` | ✅ FROZEN |
| D-11 | **Extender servicios existentes**: `delivery.service.ts`, `projectDocuments.service.ts`, `project.service.ts`, `phase.service.ts` | ✅ FROZEN |
| D-12 | Usar nombres reales Prisma: `prisma.deliveries` (no `prisma.delivery`) | ✅ FROZEN |

#### Decisiones Addendum Deferred Scope (D-13 a D-17)

| # | Decisión | Estado |
|---|----------|--------|
| D-13 | Addendum Deferred Scope entra como **Sprint 4-B** | ✅ FROZEN |
| D-14 | `TrackableItemDeferral.id` usa `@default(uuid())` (no `cuid()`) | ✅ FROZEN |
| D-15 | Status codes proceso `deferral` con prefijo: `deferral_pending`, `deferral_scheduled`, `deferral_completed`, `deferral_cancelled` | ✅ FROZEN |
| D-16 | FK `trackableItemId` con `onDelete: Cascade` (no `Restrict`) | ✅ FROZEN |
| D-17 | `cancel` **entra al MVP** (no diferido a R2) | ✅ FROZEN |

### 3. CORRECCIONES INCORPORADAS

Todas las correcciones de los reportes DB/TL/BE han sido incorporadas a la especificación final:

| Origen | Código | Corrección |
|--------|--------|------------|
| DB V4 | DB-C001 | `Deliveries` se extiende vía ALTER |
| DB V4 | DB-C002 | Tabla objetivo = `project_documents` |
| DB V4 | DB-C003 | `changeControl` = fixed/controlled/dynamic |
| DB V4 | DB-M002 | MVP mantiene 1:N Task↔Delivery |
| DB V4 | DB-M004 | `projectDocumentId` como PK única |
| DB ADD | ADD-C001 | PK usa `uuid()` no `cuid()` |
| DB ADD | ADD-C002 | Status codes con prefijo `deferral_` |
| DB ADD | ADD-C003 | Compliance query usa estados terminales reales |
| DB ADD | ADD-C004 | `onDelete: Cascade` en FK trackableItemId |
| DB ADD | ADD-M001 | Modelo real es `Deliveries` (plural) |
| TL | TL-OBS-01 | Equivalencias Prisma en brief |
| TL | TL-OBS-02 | Endpoint `/reindex` + startup check |
| TL | TL-OBS-03 | Volume `/knowledge/` en docker-compose |
| TL | TL-OBS-05 | `gen_random_uuid()::text` en seeds |
| BE | CONFLICT-BE-01 | `prisma.deliveries` (no `prisma.delivery`) |
| BE | CONFLICT-BE-02 | Extender servicios, no crear nuevos |

### 4. LIMITACIONES MVP DOCUMENTADAS

| Limitación | Descripción | Resolución |
|------------|-------------|------------|
| LIM-01 | `PhaseService.canClose()` solo cubre deferrals de tipo `phase` | V2 extenderá a sprint/delivery |
| LIM-02 | Living Docs solo Schema + API Endpoints | V2 agregará Catálogos, Services, Validators |
| LIM-03 | Sync unidireccional BD → FS | V2 evaluará sync bidireccional si se requiere |
| LIM-04 | `TrackableItemTask.status` usa texto libre | V2 integrará a StatusCatalog |

### 5. VEREDICTO PM

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║   ✅ ANÁLISIS CERRADO — APROBADO PARA EJECUCIÓN                          ║
║                                                                           ║
║   17 decisiones PM congeladas (D-01 a D-17)                              ║
║   16 correcciones incorporadas de DB/TL/BE                               ║
║   4 limitaciones MVP documentadas                                         ║
║   0 bloqueos pendientes                                                   ║
║   0 inconsistencias abiertas                                              ║
║                                                                           ║
║   Tablas nuevas: 17 (incluyendo trackable_item_deferrals)                ║
║   Tablas modificadas: 4 (projects, phases, tasks, project_documents)      ║
║   Tablas extendidas: 1 (deliveries)                                       ║
║   Endpoints nuevos: 32                                                    ║
║                                                                           ║
║   El paquete está listo para bajada operativa a TL vía PJM.              ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

---

## PARTE II: HANDOFF OPERATIVO PARA PJM

### 6. ALCANCE FINAL MVP

#### 6.1 Tablas Nuevas (17)

| Sprint DB | Tabla | Dependencias |
|-----------|-------|--------------|
| S01 | `project_type_catalog` | — |
| S01 | `phase_catalog` | — |
| S01 | `deliverable_catalog` | — |
| S01 | `trackable_type_catalog` | `project_type_catalog` |
| S02 | `flow_template_catalog` | `project_type_catalog` |
| S02 | `flow_phase_config` | `flow_template_catalog`, `phase_catalog` |
| S02 | `phase_deliverable_config` | `flow_phase_config`, `deliverable_catalog` |
| S03 | `releases` | `projects`, `status_catalog` |
| S03 | `sprints` | `releases`, `status_catalog` |
| S04 | `trackable_items` | `projects`, `trackable_type_catalog`, `status_catalog` |
| S04 | `trackable_item_tasks` | `trackable_items`, `tasks` |
| S04 | `trackable_item_evidences` | `trackable_items` |
| **S04-B** | `trackable_item_deferrals` | `trackable_items`, `status_catalog`, `releases`, `sprints`, `deliveries` |
| S05 | `project_folders` | `projects` |
| S06 | `living_document_configs` | `projects` |
| S06 | `document_index` | `project_documents` |
| S07 | `compliance_checks` | `projects` |

#### 6.2 Tablas Modificadas (ALTER)

| Sprint DB | Tabla | Campos Nuevos |
|-----------|-------|---------------|
| S03 | `projects` | `projectTypeCode`, `flowTemplateId`, `sprintEnabled`, `sprintDuration`, `fsSyncStatus`, `fsSyncAt`, `fsSyncErrors` |
| S03 | `phases` | `releaseId`, `phaseCode`, `type` |
| S03 | `tasks` | `sprintId` |
| S03 | `deliveries` | `code`, `deliverableCode`, `sprintId`, `dueDate`, `completedAt` |
| S06 | `project_documents` | `folderId`, `phaseCode`, `sprintId`, `deliveryId`, `trackableItemId`, `documentType`, `isLivingDocument`, `lastSyncAt`, `syncStatus`, `autoUpdateSource`, `changeControl`, `lockedAt`, `lockedBy` |

#### 6.3 Seeds StatusCatalog

| Sprint DB | Proceso | Códigos |
|-----------|---------|---------|
| S03 | `release` | `release_planned`, `release_active`, `release_completed`, `release_cancelled` |
| S03 | `sprint` | `sprint_planned`, `sprint_active`, `sprint_completed` |
| S04 | `trackable_item` | `ti_draft`, `ti_approved`, `ti_in_progress`, `ti_implemented`, `ti_verified`, `ti_failed` |
| S04-B | `deferral` | `deferral_pending`, `deferral_scheduled`, `deferral_completed`, `deferral_cancelled` |

#### 6.4 Diferido a V2

| Componente | Razón |
|------------|-------|
| Relación N:M Task ↔ Delivery (`DeliveryTasks`) | MVP usa 1:N existente |
| Living Docs: Catálogos, Services, Validators | Requiere parsing de código |
| Triggers `daily`/`weekly` para Living Docs | Requiere cron job |
| Sync bidireccional FS → BD | Complejidad alta |
| `canClose()` para deferrals sprint/delivery | MVP solo cubre phase |
| Dashboard de items huérfanos | UI feature |
| Alertas automáticas | Notificaciones |

---

### 7. SECUENCIA DE SPRINTS

#### 7.1 Sprints DB (ejecuta DB Engineer)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ FASE A: CATÁLOGOS BASE                                                  │
├─────────────────────────────────────────────────────────────────────────┤
│ DB-S01  │ 7 tablas catálogo                        │ ~8h   │ Riesgo: ⬜ │
│ DB-S02  │ 3 tablas flujo                           │ ~6h   │ Riesgo: ⬜ │
├─────────────────────────────────────────────────────────────────────────┤
│ FASE B: INSTANCIAS                                                      │
├─────────────────────────────────────────────────────────────────────────┤
│ DB-S03  │ releases, sprints + ALTER 4 tablas       │ ~8h   │ Riesgo: 🟡 │
│         │ + seed StatusCatalog (release, sprint)   │       │            │
├─────────────────────────────────────────────────────────────────────────┤
│ FASE C: TRACKING                                                        │
├─────────────────────────────────────────────────────────────────────────┤
│ DB-S04  │ trackable_items, _tasks, _evidences      │ ~6h   │ Riesgo: ⬜ │
│         │ + seed StatusCatalog (trackable_item)    │       │            │
│ DB-S04-B│ trackable_item_deferrals                 │ ~4h   │ Riesgo: ⬜ │
│         │ + seed StatusCatalog (deferral)          │       │            │
├─────────────────────────────────────────────────────────────────────────┤
│ FASE D: DOCUMENTOS                                                      │
├─────────────────────────────────────────────────────────────────────────┤
│ DB-S05  │ project_folders                          │ ~4h   │ Riesgo: ⬜ │
│ DB-S06  │ living_document_configs, document_index  │ ~6h   │ Riesgo: 🟡 │
│         │ + ALTER project_documents (+13 campos)   │       │            │
│         │ + backfill document_index                │       │            │
├─────────────────────────────────────────────────────────────────────────┤
│ FASE E: COMPLIANCE                                                      │
├─────────────────────────────────────────────────────────────────────────┤
│ DB-S07  │ compliance_checks                        │ ~3h   │ Riesgo: ⬜ │
└─────────────────────────────────────────────────────────────────────────┘

TOTAL DB: ~45h (7.5 sprints si sprint = 1 día)
```

#### 7.2 Sprints BE (ejecuta BE Engineer)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ BE SPRINTS                                                              │
├─────────────────────────────────────────────────────────────────────────┤
│ BE-S1   │ Extender projectDocuments.service.ts     │ ~8h   │ Post DB-S03│
│         │ Crear IndexerService + /reindex          │       │            │
│         │ Extender delivery.service.ts             │       │            │
├─────────────────────────────────────────────────────────────────────────┤
│ BE-S2   │ Crear ProjectFolderService + routes      │ ~6h   │ Post DB-S05│
├─────────────────────────────────────────────────────────────────────────┤
│ BE-S3   │ Crear ReleaseService + SprintService     │ ~8h   │ Post DB-S03│
│         │ + routes /api/releases, /api/sprints     │       │            │
├─────────────────────────────────────────────────────────────────────────┤
│ BE-S4   │ Crear TrackableItemService               │ ~10h  │ Post DB-S04│
│         │ + routes /api/trackable-items            │       │            │
│         │ + /tasks, /evidence                      │       │            │
├─────────────────────────────────────────────────────────────────────────┤
│ BE-S4-B │ Crear TrackableItemDeferralService       │ ~6h   │ Post DB-S04-B│
│         │ + endpoints: defer, schedule, cancel, list│      │            │
│         │ + integrar PhaseService.canClose()       │       │            │
├─────────────────────────────────────────────────────────────────────────┤
│ BE-S5   │ Crear LivingDocService + SyncService     │ ~8h   │ Post DB-S06│
│         │ + routes /api/living-docs                │       │            │
│         │ + /api/projects/:id/sync-filesystem      │       │            │
├─────────────────────────────────────────────────────────────────────────┤
│ BE-S6   │ Crear ComplianceService                  │ ~6h   │ Post DB-S07│
│         │ + routes /api/compliance-checks          │       │            │
└─────────────────────────────────────────────────────────────────────────┘

TOTAL BE: ~52h (8.5 sprints si sprint = 1 día)
```

#### 7.3 Paralelismo Permitido

```
SEMANA 1:
  DB: S01 → S02 (catálogos + flujos)
  DevOps: Configurar volume /knowledge/ + verificar Dockerfile

SEMANA 2:
  DB: S03 (releases, sprints, ALTERs)
  BE: S1 (IndexerService, extender servicios) ← inicia cuando DB-S03 termine

SEMANA 3:
  DB: S04 + S04-B (tracking + deferrals)
  BE: S3 (ReleaseService, SprintService)

SEMANA 4:
  DB: S05 + S06 (folders, docs)
  BE: S4 + S4-B (TrackableItem + Deferrals)

SEMANA 5:
  DB: S07 (compliance)
  BE: S2 + S5 (Folders, LivingDocs, Sync)

SEMANA 6:
  BE: S6 (Compliance)
  QA: Integración completa
```

---

### 8. DEPENDENCIAS POR ROL

#### 8.1 DB Engineer

| Prerequisito | Momento | Responsable |
|--------------|---------|-------------|
| Verificar constraint `@unique` en `StatusCatalog.code` | Antes de DB-S03 | DB |
| Usar `gen_random_uuid()::text` en todos los seeds | Todos los sprints | DB |
| Usar comillas en columnas camelCase en SQL raw | Todos los sprints | DB |
| Backfill `document_index` post-migración | Después de DB-S06 | DB |

#### 8.2 BE Engineer

| Prerequisito | Momento | Responsable |
|--------------|---------|-------------|
| Usar `prisma.deliveries` (no `prisma.delivery`) | Todos los sprints | BE |
| **EXTENDER** `delivery.service.ts`, `projectDocuments.service.ts` | BE-S1 | BE |
| Implementar startup check en IndexerService | BE-S1 | BE |
| `JSON.stringify` para `fsSyncErrors: Json?` | BE-S1 | BE |
| Verificar `prisma/schema.prisma` en contenedor | BE-S5 | BE/DevOps |

#### 8.3 DevOps

| Prerequisito | Momento | Responsable |
|--------------|---------|-------------|
| Agregar bind mount `/knowledge/` en docker-compose.yml | **Antes de BE-S5** | DevOps |
| Verificar `COPY prisma ./prisma` en Dockerfile | **Antes de BE-S5** | DevOps |

```yaml
# docker-compose.yml — cambio requerido
vtt-backend:
  volumes:
    - ./knowledge:/app/knowledge
```

#### 8.4 QA

| Prerequisito | Momento | Responsable |
|--------------|---------|-------------|
| Backward compatibility de endpoints existentes | Cada sprint BE | QA |
| Validar que campos nuevos son nullable | DB-S03, DB-S06 | QA |
| Validar integración deferrals + PhaseService.canClose() | Post BE-S4-B | QA |

---

### 9. ENDPOINTS MVP (32 TOTAL)

| # | Ruta | Métodos | Sprint BE |
|---|------|---------|-----------|
| 1 | `/api/releases` | GET, POST | BE-S3 |
| 2 | `/api/releases/:id` | GET, PATCH, DELETE | BE-S3 |
| 3 | `/api/releases/:id/sprints` | GET, POST | BE-S3 |
| 4 | `/api/sprints/:id` | GET, PATCH, DELETE | BE-S3 |
| 5 | `/api/phases/:id/deliveries` | GET, POST | BE-S1 |
| 6 | `/api/deliveries/:id` | GET, PATCH, DELETE | BE-S1 |
| 7 | `/api/project-folders` | GET, POST | BE-S2 |
| 8 | `/api/project-folders/:id` | GET, PATCH, DELETE | BE-S2 |
| 9 | `/api/project-folders/:id/move` | POST | BE-S2 |
| 10 | `/api/trackable-items` | GET, POST | BE-S4 |
| 11 | `/api/trackable-items/:id` | GET, PATCH, DELETE | BE-S4 |
| 12 | `/api/trackable-items/:id/tasks` | POST, DELETE | BE-S4 |
| 13 | `/api/trackable-items/:id/evidence` | POST | BE-S4 |
| 14 | `/api/trackable-items/:id/defer` | POST | BE-S4-B |
| 15 | `/api/deferrals/:id/schedule` | PATCH | BE-S4-B |
| 16 | `/api/deferrals/:id/cancel` | PATCH | BE-S4-B |
| 17 | `/api/projects/:id/deferrals` | GET | BE-S4-B |
| 18 | `/api/living-docs` | GET | BE-S5 |
| 19 | `/api/living-docs/:type/regenerate` | POST | BE-S5 |
| 20 | `/api/projects/:id/sync-filesystem` | POST | BE-S5 |
| 21 | `/api/projects/:id/reindex` | POST | BE-S1 |
| 22 | `/api/compliance-checks` | GET, POST | BE-S6 |
| 23 | `/api/compliance-checks/:id` | GET | BE-S6 |
| 24-32 | Catálogos (GET only) | GET | BE-S1 |

---

### 10. RIESGOS Y MITIGACIONES

| # | Riesgo | Prob. | Impacto | Mitigación |
|---|--------|-------|---------|------------|
| R1 | Migración rompe datos existentes | Baja | Alto | Campos nullable + backup obligatorio + rollback scripts |
| R2 | IndexerService pierde eventos | Media | Medio | Startup check + cola reintento + `/reindex` |
| R3 | Volume `/knowledge/` no configurado | Media | Alto | **DevOps prerequisito antes de BE-S5** |
| R4 | `prisma/schema.prisma` no en contenedor | Media | Medio | Verificar Dockerfile |
| R5 | BE usa nombres Prisma incorrectos | Alta | Bajo | Tabla de equivalencias en SPEC |
| R6 | BE crea servicios nuevos en vez de extender | Alta | Medio | D-11 y D-12 explícitos |
| R7 | Scope amplio (17 tablas, 32 endpoints) | Media | Alto | Sprints rollback-able |
| R8 | `fsSyncErrors: Json?` rompe serialización | Media | Bajo | `JSON.stringify` explícito |
| R9 | `canClose()` no cubre deferrals sprint/delivery | Media | Bajo | **Limitación documentada (LIM-01)** |
| R10 | StatusCatalog.code colisión | Baja | Medio | Prefijo `deferral_` aplicado |

---

### 11. CHECKLIST PJM ANTES DE INICIAR

```
PREREQUISITOS OBLIGATORIOS:
[ ] Backup de BD de producción
[ ] DevOps confirma volume /knowledge/ configurado
[ ] DevOps confirma COPY prisma ./prisma en Dockerfile
[ ] DB Engineer confirma constraint @unique en StatusCatalog.code
[ ] TL confirma lectura de SPEC_FUNCIONAL v1.1 + este handoff

ASIGNACIÓN DE TAREAS:
[ ] DB Engineer recibe: SPEC v1.1 + scripts migración AR V4.3
[ ] BE Engineer recibe: SPEC v1.1 + servicios a extender + endpoints
[ ] QA recibe: matriz de endpoints + criterios de aceptación
[ ] DevOps recibe: prerequisitos de infraestructura

DOCUMENTOS DE REFERENCIA:
[ ] SPEC_FUNCIONAL_MODELO_DINAMICO_V4_CONSOLIDADO_v1.1.md
[ ] AR_ANALISIS_VTT_MODELO_DINAMICO_V4.3.md (scripts migración sección 8)
[ ] Este documento (CIERRE_PM_HANDOFF_PJM_MODELO_DINAMICO_V4.2.md)
```

---

### 12. CRITERIO DE ÉXITO

El feature VTT Modelo Dinámico V4 se considera **COMPLETADO** cuando:

1. ✅ Las 17 tablas nuevas existen en producción
2. ✅ Las 4 tablas modificadas tienen los campos nuevos
3. ✅ Los 32 endpoints responden correctamente
4. ✅ `PhaseService.canClose()` integra validación de deferrals (solo phase)
5. ✅ IndexerService indexa documentos post-upload
6. ✅ LivingDocService regenera Schema y API Endpoints
7. ✅ SyncService escribe estructura en `/knowledge/`
8. ✅ Backward compatibility verificada (endpoints existentes no rotos)

---

### 13. FIRMAS

| Rol | Nombre | Firma | Fecha |
|-----|--------|-------|-------|
| PM | Martin Rivas | ✅ APROBADO | 2026-03-30 |
| PJM | (pendiente) | ⬜ | |
| TL | (pendiente) | ⬜ | |
| DB Engineer | (pendiente) | ⬜ | |
| BE Engineer | (pendiente) | ⬜ | |
| DevOps | (pendiente) | ⬜ | |
| QA | (pendiente) | ⬜ | |

---

**Documento:** CIERRE_PM_HANDOFF_PJM_MODELO_DINAMICO_V4.2.md  
**Versión:** 4.2.0  
**Estado:** ✅ CERRADO — Listo para ejecución  
**Fecha:** 2026-03-30

---

**PM — Martin Rivas**  
CEO/Founder — Virtual Teams Tracking
