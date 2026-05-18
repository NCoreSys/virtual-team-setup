# HANDOFF PJM: Plan de Sprints Memory Service en VTT

**De:** PM (Martin Rivas)
**Para:** PJM (pjm@memory-service.vtt.ai)
**Fecha:** 2026-04-19
**Prioridad:** P0 CRITICO
**Fuente:** HANDOFF_PJM_MEMORY_SERVICE_2026-04-15.md (plan aprobado 150h)

---

## 0. CONTEXTO

El analisis, spec tecnica y arquitectura estan COMPLETOS y aprobados:
- SPEC v1.9 consolidado con 43 decisiones cerradas (D-MEM-01 a D-MEM-43)
- Reviews aprobados: AR, DB, TL, SA
- Infraestructura provisionada: BD, storage, SERVICE_KEY, docker-compose

El proyecto ya existe en VTT con 9 fases y 68 deliverables (MEM-001 a MEM-068).

Tu tarea: crear las tareas de ejecucion (sprints) en VTT bajo los deliverables correctos por fase.

---

## 1. DATOS VTT

| Dato | Valor |
|------|-------|
| Project ID | a56a76e6-29bf-401e-a8ec-091882e383f7 |
| API URL | http://77.42.88.106:3000 |
| Tu UUID | 0ff63a29-0bc0-465a-b9bd-5f71476bc91d |
| SERVICE_KEY | hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d |

Phase 3A UUID: 340df4ef-24ae-4d65-96ce-45ccaea1e042
Phase 4 UUID:  7e003478-cd98-4953-ae79-676e864fb1f8

---

## 2. ESTRUCTURA CORRECTA POR FASE

Los sprints del HO original se separan en dos fases:

| Sprint HO original | Fase VTT | Deliverable VTT |
|-------------------|----------|-----------------|
| S-DL-01 (Design System + Dashboard wireframes) | PHASE 3A | MEM-019 Wireframes + MEM-021 Design System |
| S-DL-02 (Conversation Viewer wireframes) | PHASE 3A | MEM-019 Wireframes + MEM-020 Mockups |
| S-DL-03 (Import + Cost + Lista wireframes) | PHASE 3A | MEM-019 Wireframes |
| S-DL-04 (UX Spec + Handoff) | PHASE 3A | MEM-022 Design Handoff |
| S01 Schema + Seeds | PHASE 4 | MEM-032 |
| S02 Import + Timeline | PHASE 4 | MEM-033 |
| S03 Content + Context | PHASE 4 | MEM-034 |
| S04 Adapters + Cleanup | PHASE 4 | MEM-035 |
| S05 Lista + Cost + Dashboard | PHASE 4 | MEM-036 |
| S06 Docker + Integration | PHASE 4 | MEM-037 |
| S-UI-01 Setup + Timeline + Viewer | PHASE 4 | MEM-042 |
| S-UI-02 Dashboard + Cost + Import | PHASE 4 | MEM-043 |
| S-UI-03 Viewer REVIEW + Lista | PHASE 4 | MEM-044 |
| S-UI-04 Cost Agente + Health | PHASE 4 | MEM-045 |

Nota: MEM-038 a MEM-041 (DL deliverables en Phase 4) quedan como hitos de control.
Las tareas reales del DL van bajo Phase 3A.

---

## 3. AGENTES Y UUIDs

| Sigla | UUID |
|-------|------|
| PM | 350831b2-e1ae-4dbe-b2eb-7e023ec2e103 |
| PJM | 0ff63a29-0bc0-465a-b9bd-5f71476bc91d |
| TL | 92225290-6b6b-4c1f-a940-dcb4262507aa |
| BE | ebbe3cee-abed-4b3b-860d-0a81f632b08a |
| DB | 6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7 |
| FE | d23c9cd9-a156-433b-8900-94add5488eec |
| QA | 613c9538-658c-45fe-a6d7-c1ea9ff04b78 |
| DO | 322e3745-9756-4a7c-af11-44b33edef44d |
| DL | b3a09269-cded-468c-a475-15a48f203cb0 |

Prioridades VTT:
- medium: d0b619ef-27e7-42d8-8879-41030a602eed
- high:   1a617554-6319-4c56-826f-8ef49a0ff9cc

---

## 4. FASE 3A — Design UX/UI (DL, 28h)

Phase UUID: 340df4ef-24ae-4d65-96ce-45ccaea1e042

Las tareas DL van dentro de los deliverables MEM-019, MEM-020, MEM-021 y MEM-022.

### Sprint S-DL-01 (10h) dentro de MEM-019/MEM-021

| # | Titulo | Agente | Horas | Complexity | Category |
|---|--------|--------|-------|------------|----------|
| 1 | Design System tokens (colores, tipografia, espaciado) | DL | 3 | MEDIUM | design |
| 2 | Wireframes Dashboard (stats, actividad reciente) | DL | 4 | HIGH | design |
| 3 | Wireframes Agent Timeline (cronologia conversaciones) | DL | 3 | MEDIUM | design |

### Sprint S-DL-02 (8h) dentro de MEM-019/MEM-020

| # | Titulo | Agente | Horas | Complexity | Category |
|---|--------|--------|-------|------------|----------|
| 4 | Wireframes Conversation Viewer modo TASK | DL | 4 | HIGH | design |
| 5 | Wireframes Conversation Viewer modo REVIEW | DL | 4 | HIGH | design |

### Sprint S-DL-03 (7h) dentro de MEM-019

| # | Titulo | Agente | Horas | Complexity | Category |
|---|--------|--------|-------|------------|----------|
| 6 | Wireframes Import Manual | DL | 2 | MEDIUM | design |
| 7 | Wireframes Cost Reports (proyecto y agente) | DL | 2 | MEDIUM | design |
| 8 | Wireframes Lista/Busqueda conversaciones | DL | 2 | MEDIUM | design |
| 9 | Wireframes Health page | DL | 1 | LOW | design |

### Sprint S-DL-04 (3h) dentro de MEM-022

| # | Titulo | Agente | Horas | Complexity | Category |
|---|--------|--------|-------|------------|----------|
| 10 | Documento UX Spec completo (9 pantallas, estados, flows) | DL | 2 | MEDIUM | documentation |
| 11 | Handoff a FE (assets exportados, specs, tokens) | DL | 1 | LOW | documentation |

**TOTAL Phase 3A: 28h, 11 tareas**
**HITO: MEM-022 completado = FE puede iniciar**

---

## 5. FASE 4 — Development (BE + FE, 122h)

Phase UUID: 7e003478-cd98-4953-ae79-676e864fb1f8

### MEM-032: S01 — Schema + Seeds (9h) | DB + BE

| Tarea ID | Titulo | Agente | Horas | Complexity | Category |
|----------|--------|--------|-------|------------|----------|
| MEM-DB-001 | Crear schema Prisma completo (19 tablas, 10 catalogos) | DB | 3 | HIGH | development |
| MEM-DB-002 | Migraciones + partial indexes (SQL manual) | DB | 2 | MEDIUM | development |
| MEM-DB-003 | Seed catalogos (sources, statuses, topics, workTypes) | DB | 1 | LOW | development |
| MEM-BE-001 | Setup proyecto Express + estructura carpetas | BE | 2 | MEDIUM | development |
| MEM-BE-002 | Catalog cache en startup (prefetch para evitar N+1) | BE | 1 | LOW | development |

### MEM-033: S02 — Import + Timeline + Clasificacion (12h) | BE

| Tarea ID | Titulo | Agente | Horas | Complexity | Category |
|----------|--------|--------|-------|------------|----------|
| MEM-BE-003 | POST /api/conversations/import (source CLAUDE_SDK, idempotencia P2002) | BE | 4 | HIGH | development |
| MEM-BE-004 | Parser JSONL + validacion + externalSessionId format | BE | 2 | MEDIUM | development |
| MEM-BE-005 | Clasificacion por reglas (topics por keywords, workType por agentRole) | BE | 3 | HIGH | development |
| MEM-BE-006 | GET /api/agents/:agentId/timeline | BE | 2 | MEDIUM | development |
| MEM-BE-007 | Storage contenido completo en filesystem + contentPreview en BD | BE | 1 | LOW | development |

### MEM-034: S03 — Content + Context <500ms (12h) | BE + QA

| Tarea ID | Titulo | Agente | Horas | Complexity | Category |
|----------|--------|--------|-------|------------|----------|
| MEM-BE-008 | GET /api/conversations/:id/content (messages parseados) | BE | 2 | MEDIUM | development |
| MEM-BE-009 | GET /api/context (JSON estructurado, fail-fast, sin transformar) | BE | 4 | HIGH | development |
| MEM-BE-010 | Optimizacion <500ms con indices parciales + prefetch statusId | BE | 2 | HIGH | development |
| MEM-QA-001 | Tests rendimiento GET /context (10/100/1000 convs, 50 concurrent) | QA | 2 | MEDIUM | testing |
| MEM-QA-002 | Tests unitarios import + clasificacion | QA | 2 | MEDIUM | testing |

### MEM-035: S04 — Adapters + Cleanup (12h) | BE

| Tarea ID | Titulo | Agente | Horas | Complexity | Category |
|----------|--------|--------|-------|------------|----------|
| MEM-BE-011 | POST /api/conversations/import-review (prefetch catalogs) | BE | 3 | MEDIUM | development |
| MEM-BE-012 | Adapter Claude Web (JSON export de claude.ai) | BE | 2 | MEDIUM | development |
| MEM-BE-013 | Adapter ChatGPT (JSON export) | BE | 2 | MEDIUM | development |
| MEM-BE-014 | Cleanup job por statusId (catch delega siempre, max 3 retries) | BE | 2 | MEDIUM | development |
| MEM-BE-015 | Retry logic con log de acciones | BE | 1 | LOW | development |
| MEM-BE-016 | Tests unitarios cada adapter + cleanup logic | BE | 2 | MEDIUM | testing |

### MEM-036: S05 — Lista + Cost + Dashboard + Health (11h) | BE

| Tarea ID | Titulo | Agente | Horas | Complexity | Category |
|----------|--------|--------|-------|------------|----------|
| MEM-BE-017 | GET /api/conversations (lista, filtros, paginacion) | BE | 2 | MEDIUM | development |
| MEM-BE-018 | GET /api/projects/:id/cost-report (sumas tokens + costos 6 decimales) | BE | 2 | MEDIUM | development |
| MEM-BE-019 | GET /api/agents/:id/cost-report (breakdown por workType) | BE | 2 | MEDIUM | development |
| MEM-BE-020 | GET /api/dashboard (stats globales + actividad reciente) | BE | 2 | MEDIUM | development |
| MEM-BE-021 | POST /api/conversations/upload (import manual) | BE | 2 | MEDIUM | development |
| MEM-BE-022 | GET /health (BD, storage, cache status) | BE | 1 | LOW | development |

### MEM-037: S06 — Docker + Deploy + Integracion Hook Manager (14h) | DO + BE + QA

| Tarea ID | Titulo | Agente | Horas | Complexity | Category |
|----------|--------|--------|-------|------------|----------|
| MEM-DO-001 | Dockerfile + docker-compose.yml (puerto 3002/3003) | DO | 2 | MEDIUM | deployment |
| MEM-DO-002 | Deploy a VM Hetzner 77.42.88.106 | DO | 2 | MEDIUM | deployment |
| MEM-DO-003 | Configuracion nginx/traefik reverse proxy | DO | 1 | LOW | deployment |
| MEM-BE-023 | Integracion Hook Manager VTT (externalSessionId={run_id}:r{N}:{role}) | BE | 4 | HIGH | development |
| MEM-QA-003 | Tests E2E flujo completo SDK->import->context | QA | 3 | HIGH | testing |
| MEM-QA-004 | Tests integracion Runtime v1.1 (platformRefs, source CLAUDE_SDK) | QA | 2 | MEDIUM | testing |

### MEM-042: UI-01 — Setup + Timeline + Viewer TASK (16h) | FE

DEPENDENCIA CRITICA: MEM-022 Design Handoff debe estar COMPLETADO.

| Tarea ID | Titulo | Agente | Horas | Complexity | Category |
|----------|--------|--------|-------|------------|----------|
| MEM-FE-001 | Setup React + Vite + TailwindCSS | FE | 2 | MEDIUM | development |
| MEM-FE-002 | Configuracion API client (base URL, interceptors) | FE | 1 | LOW | development |
| MEM-FE-003 | Agent Timeline component (cronologia de conversaciones) | FE | 5 | HIGH | development |
| MEM-FE-004 | Conversation Viewer modo TASK (mensajes + metadata) | FE | 6 | HIGH | development |
| MEM-FE-005 | Routing + layout base (nav, sidebar, breadcrumbs) | FE | 2 | MEDIUM | development |

### MEM-043: UI-02 — Dashboard + Cost + Import (12h) | FE

| Tarea ID | Titulo | Agente | Horas | Complexity | Category |
|----------|--------|--------|-------|------------|----------|
| MEM-FE-006 | Dashboard page (stats, graficas, actividad reciente) | FE | 4 | HIGH | development |
| MEM-FE-007 | Cost Report Proyecto page (tabla + breakdown) | FE | 4 | MEDIUM | development |
| MEM-FE-008 | Import Manual page (upload + preview + submit) | FE | 4 | MEDIUM | development |

### MEM-044: UI-03 — Viewer REVIEW + Lista (10h) | FE

| Tarea ID | Titulo | Agente | Horas | Complexity | Category |
|----------|--------|--------|-------|------------|----------|
| MEM-FE-009 | Conversation Viewer modo REVIEW (anotaciones, diff) | FE | 5 | HIGH | development |
| MEM-FE-010 | Lista conversaciones + busqueda + filtros avanzados | FE | 5 | HIGH | development |

### MEM-045: UI-04 — Cost Agente + Health + Estados (8h) | FE

| Tarea ID | Titulo | Agente | Horas | Complexity | Category |
|----------|--------|--------|-------|------------|----------|
| MEM-FE-011 | Cost Report Agente page | FE | 3 | MEDIUM | development |
| MEM-FE-012 | Health page (estado BD, storage, servicios) | FE | 2 | LOW | development |
| MEM-FE-013 | Estados globales: loading, empty, error (componentes reutilizables) | FE | 3 | MEDIUM | development |

**TOTAL Phase 4: 122h, 39 tareas**

---

## 6. DEPENDENCIAS CRITICAS

S-DL-01 -> S-DL-02 -> S-DL-03 -> S-DL-04 [MEM-022 HITO]
                                              |
                              MEM-042 -> MEM-043 -> MEM-044 -> MEM-045

MEM-032 -> MEM-033 -> MEM-034 -> MEM-035 -> MEM-036 -> MEM-037

MEM-037 depende de Hook Manager VTT operativo.
FE no puede iniciar sin MEM-022 completado.
DL puede correr en paralelo con BE desde Sprint 2.

---

## 7. CALENDARIO

| Sprint | Fechas | Deliverables | Owner |
|--------|--------|--------------|-------|
| Sprint 2 | May 19 - Jun 01 | MEM-019/020/021 (DL-01,02,03) + MEM-032 (S01) | DL // DB+BE |
| Sprint 3 | Jun 02 - Jun 15 | MEM-022 (DL-04) + MEM-033/034 (S02,S03) | DL + BE+QA |
| Sprint 4 | Jun 16 - Jun 29 | MEM-035/036 (S04,S05) + MEM-042 (UI-01) | BE + FE |
| Sprint 5 | Jun 30 - Jul 13 | MEM-037 (S06) + MEM-043/044 (UI-02,03) | DO+BE+QA + FE |
| Sprint 6 | Jul 14 - Jul 27 | MEM-045 (UI-04) | FE |

---

## 8. RESUMEN DE HORAS

| Fase | Sprints | Tareas | Horas |
|------|---------|--------|-------|
| Phase 3A (DL) | S-DL-01 a S-DL-04 | 11 | 28h |
| Phase 4 BE | S01 a S06 | 28 | 76h |
| Phase 4 FE | UI-01 a UI-04 | 13 | 46h |
| TOTAL | 14 sprints | 52 tareas | 150h |

---

## 9. API PARA CREAR TAREAS

POST http://77.42.88.106:3000/api/phases/{PHASE_UUID}/tasks

Body:
{
  "title": "nombre de la tarea",
  "priorityId": "d0b619ef-27e7-42d8-8879-41030a602eed",
  "complexity": "HIGH",
  "category": "development",
  "type": "feature",
  "order": 1,
  "estimatedHours": 3,
  "assigneeId": "UUID-del-agente"
}

Valores validos:
- complexity: LOW | MEDIUM | HIGH
- category: development | design | testing | documentation | review | bugfix | deployment
- type: feature | bug | research | documentation | chore

---

## 10. CHECKLIST PJM

Phase 3A:
[ ] 1. Crear 3 tareas S-DL-01 bajo Phase 3A (order 1-3)
[ ] 2. Crear 2 tareas S-DL-02 bajo Phase 3A (order 4-5)
[ ] 3. Crear 4 tareas S-DL-03 bajo Phase 3A (order 6-9)
[ ] 4. Crear 2 tareas S-DL-04 bajo Phase 3A (order 10-11)

Phase 4:
[ ] 5. Crear 5 tareas MEM-032 bajo Phase 4
[ ] 6. Crear 5 tareas MEM-033 bajo Phase 4
[ ] 7. Crear 5 tareas MEM-034 bajo Phase 4
[ ] 8. Crear 6 tareas MEM-035 bajo Phase 4
[ ] 9. Crear 6 tareas MEM-036 bajo Phase 4
[ ] 10. Crear 6 tareas MEM-037 bajo Phase 4
[ ] 11. Crear 5 tareas MEM-042 bajo Phase 4
[ ] 12. Crear 3 tareas MEM-043 bajo Phase 4
[ ] 13. Crear 2 tareas MEM-044 bajo Phase 4
[ ] 14. Crear 3 tareas MEM-045 bajo Phase 4
[ ] 15. Verificar 52 tareas: GET /api/tasks?projectId=a56a76e6-29bf-401e-a8ec-091882e383f7
[ ] 16. Notificar al PM

---

## 11. DOCUMENTOS DE REFERENCIA

- Release2.0/01-PM/HANDOFF_PJM_MEMORY_SERVICE_2026-04-15.md (plan original aprobado)
- Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md (spec tecnica completa)
- Release2.0/02-AR/AR_REVIEW_SPEC_MEMORY_SERVICE_v1.md (arquitectura aprobada)
- Release2.0/03-DB/DB_REVIEW_SPEC_MEMORY_SERVICE_v1.md (DB schema aprobado)
- Release2.0/04-TL/TL_REVIEW_SPEC_MEMORY_SERVICE_v1.md (tech lead observaciones)
- Release2.0/PJM/SETUP_MEM.md (detalle tareas con IDs internos)
- Release2.0/PJM/CLOSURE_MEM_SPRINTS.md (templates cierre por sprint)

Estado: LISTO PARA EJECUTAR
