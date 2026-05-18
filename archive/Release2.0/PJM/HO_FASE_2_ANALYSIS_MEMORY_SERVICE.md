# HANDOFF — Fase 2: Analysis · Memory Service

| Campo | Valor |
|-------|-------|
| **Documento** | HO_FASE_2_ANALYSIS_MEMORY_SERVICE.md |
| **Versión** | 1.0 |
| **Fecha** | 2026-04-22 |
| **De** | PJM — `0ff63a29-0bc0-465a-b9bd-5f71476bc91d` |
| **Para** | SA — `0c128e3b-db3b-4e31-b107-0379b5791233` |
| **CC** | PM — `350831b2-e1ae-4dbe-b2eb-7e023ec2e103` · UX — `a75a1dae-754a-4b6f-a3ff-db8d51f6a91b` |
| **Rol líder** | SA (Solution Analyst) |
| **Proyecto** | Memory Service |
| **Fase VTT** | Analysis (Phase order 4) |
| **Estado** | ✅ APROBADO — listo para ejecución |

---

## RESUMEN EJECUTIVO

Esta fase traduce la visión y el scope a **requisitos formales y modelos de comportamiento** antes de entrar en diseño. Tiene 8 tareas VTT (MEM-018..025), 41h totales, y produce 43 deliverables SDLC distribuidos en 8 VTT Deliveries.

**Roles activos:** SA · AR · UX  
**Líder de seguimiento:** SA  
**Criterio de entrada:** Gate Planning cerrado (MEM-017 `task_completed`)  
**Criterio de salida:** MEM-025 `task_completed` + sign-off SA en todos los 2.1.* al 2.8.*

---

## 1. ARQUITECTURA DE LA FASE

```
╔══════════════════════════════════════════════════════╗
║   GATE DE ENTRADA: MEM-017 task_completed            ║
║   (Budget & Resources cerrado — Planning OK)         ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║   DELIVERY 1: Functional Requirements (VTT)          ║
║   └─ MEM-018  Functional Requirements  SA  6h  MED  ║
║                                                      ║
║   DELIVERY 2: Non-Functional Requirements (VTT)      ║
║   └─ MEM-019  Non-Functional Req.      AR  4h  MED  ║
║                                                      ║
║   DELIVERY 3: Use Cases (VTT)                        ║
║   └─ MEM-020  Use Cases                SA  5h  MED  ║
║                                                      ║
║   DELIVERY 4: User Stories (VTT)                     ║
║   └─ MEM-021  User Stories             SA  8h  MED  ║
║                                                      ║
║   DELIVERY 5: Business Rules (VTT)                   ║
║   └─ MEM-022  Business Rules           SA  4h  MED  ║
║                                                      ║
║   DELIVERY 6: User Flows (VTT)                       ║
║   └─ MEM-023  User Flows               UX  4h  MED  ║
║                                                      ║
║   DELIVERY 7: Acceptance Criteria (VTT)              ║
║   └─ MEM-024  Acceptance Criteria      SA  6h  MED  ║
║                                                      ║
║   DELIVERY 8: Traceability Matrix (VTT)              ║
║   └─ MEM-025  Traceability Matrix      SA  4h  MED  ║
║                                                      ║
╠══════════════════════════════════════════════════════╣
║   GATE DE SALIDA: 8/8 tasks completed + 43 docs      ║
║   → Habilita Fase 3A Design UX/UI                    ║
╚══════════════════════════════════════════════════════╝
```

---

## 2. DEPENDENCIAS INTERNAS

```
MEM-017 (Planning gate)
    │
    ▼
MEM-018 (Functional Requirements)
    │
    ├─────────────────────────────────────────────────► MEM-019 (NFR)
    │
    └─────────────────────────────────────────────────► MEM-020 (Use Cases)
                                                              │
                                                    ┌─────────┴──────────┐
                                                    ▼                    ▼
                                              MEM-021 (Stories)    MEM-022 (BizRules)
                                                    │
                                                    └────────────────────► MEM-023 (User Flows)
                                                                                │
                                                                                ▼
                                                                          MEM-024 (AC)
                                                                                │
                                                                                ▼
                                                                          MEM-025 (Traceability)
```

**Notas de ejecución:**
- MEM-018 (FR) es el punto de partida obligatorio — define los 11 endpoints R1
- MEM-019 (NFR) puede arrancar en paralelo con MEM-020 una vez MEM-018 completado
- MEM-021 y MEM-022 pueden trabajarse en paralelo después de MEM-020
- MEM-023 (User Flows, UX) puede arrancar en paralelo con MEM-021/022
- MEM-024 requiere MEM-021 (necesita las Stories para escribir AC en Gherkin)
- MEM-025 cierra la fase: consolida trazabilidad RF→US→Test

---

## 3. TAREAS VTT — DETALLE

### MEM-018 · Functional Requirements

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-018 |
| **Rol** | SA (`0c128e3b-db3b-4e31-b107-0379b5791233`) |
| **Delivery** | Functional Requirements |
| **Horas** | 6h |
| **Prioridad** | MEDIUM |
| **Complejidad** | HIGH |
| **Categoría** | documentation |

**Descripción:** Autorar el SRS (Software Requirements Specification) del Memory Service:
- `2.1.1 SRS Document` — Documento maestro de requisitos funcionales.
- `2.1.2 Requirements List (RF-XXX)` — Lista completa sobre los 11 endpoints R1: POST /import, POST /import-review, POST /upload, GET /content, GET /context, GET /agents/:id/timeline, GET /conversations, GET /projects/:id/cost-report, GET /agents/:id/cost-report, GET /dashboard/stats, GET /health.
- `2.1.3 MoSCoW Prioritization` — Must/Should/Could/Won't de cada RF.
- `2.1.4 Feature List` — Agrupación de RFs por feature (Import, Context, Timeline, Cost, Dashboard, Health).
- `2.1.5 Functional Decomposition` — Árbol de funcionalidades por módulo.
- `2.1.6 Requirements Approval` — Sign-off formal de los requisitos funcionales.

**Entregables SDLC:** 2.1.1 · 2.1.2 · 2.1.3 · 2.1.4 · 2.1.5 · 2.1.6

---

### MEM-019 · Non-Functional Requirements

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-019 |
| **Rol** | AR (`e9403c25-c1f8-4b64-b2ef-f447d53115e2`) |
| **Delivery** | Non-Functional Requirements |
| **Horas** | 4h |
| **Prioridad** | MEDIUM |
| **Complejidad** | HIGH |
| **Categoría** | documentation |

**Descripción:** Autorar los requisitos no funcionales del sistema:
- `2.2.1 NFR Document` — Marco general de NFRs y su importancia para Memory Service.
- `2.2.2 Performance NFRs` — Incluye obligatoriamente el SLA contractual `<500ms` p95 para GET /context. Benchmarks con k6.
- `2.2.3 Security NFRs` — SERVICE_KEY autenticación, OWASP Top 10, validación Zod, headers de seguridad.
- `2.2.4 Scalability NFRs` — Límites de carga (conversaciones, agentes concurrentes), estrategia de escala horizontal.
- `2.2.5 Availability NFRs` — Uptime objetivo, RTO/RPO, plan de DR para servidor único Hetzner.
- `2.2.6 Usability NFRs` — Criterios de usabilidad de la UI: tiempo de carga < 2s, responsive desktop.

**Entregables SDLC:** 2.2.1 · 2.2.2 · 2.2.3 · 2.2.4 · 2.2.5 · 2.2.6

---

### MEM-020 · Use Cases

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-020 |
| **Rol** | SA (`0c128e3b-db3b-4e31-b107-0379b5791233`) |
| **Delivery** | Use Cases |
| **Horas** | 5h |
| **Prioridad** | MEDIUM |
| **Complejidad** | MEDIUM |
| **Categoría** | documentation |

**Descripción:** Autorar el modelo de casos de uso del Memory Service:
- `2.3.1 Use Case Document` — Marco y descripción general del modelo.
- `2.3.2 UML Use Case Diagram` — Diagrama con actores (Agent, PB, Hook Manager, Admin, UI User) y casos de uso principales.
- `2.3.3 Use Case List` — Inventario completo de casos de uso (mínimo UC-001..UC-020).
- `2.3.4 Detailed Use Cases` — Descripción completa de casos críticos: UC-Import (4 fuentes), UC-Context (<500ms), UC-Timeline, UC-Cost, UC-Upload.
- `2.3.5 Actor Definitions` — Definición y responsabilidades de cada actor del sistema.
- `2.3.6 Use Case Relationships` — Include, extend, generalización entre casos de uso.

**Entregables SDLC:** 2.3.1 · 2.3.2 · 2.3.3 · 2.3.4 · 2.3.5 · 2.3.6

---

### MEM-021 · User Stories

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-021 |
| **Rol** | SA (`0c128e3b-db3b-4e31-b107-0379b5791233`) |
| **Delivery** | User Stories |
| **Horas** | 8h |
| **Prioridad** | MEDIUM |
| **Complejidad** | HIGH |
| **Categoría** | documentation |

**Descripción:** Autorar el backlog completo de historias de usuario:
- `2.4.1 Product Backlog` — Backlog priorizado con todas las US del R1.
- `2.4.2 User Stories` — Historias en formato "Como [rol], quiero [acción], para [beneficio]". Mínimo 30 US cubriendo los 11 endpoints + UI.
- `2.4.3 Story Map` — Mapa visual de stories agrupadas por actividad de usuario.
- `2.4.4 Epics` — Agrupación de US en épicas (Import, Memory Context, Cost Tracking, UI Dashboard, Operations).
- `2.4.5 Story Estimation` — Story points por US usando escala Fibonacci.
- `2.4.6 Sprint Assignment` — Asignación de US a sprints S01..S06 y UI-01..UI-04.

**Entregables SDLC:** 2.4.1 · 2.4.2 · 2.4.3 · 2.4.4 · 2.4.5 · 2.4.6

---

### MEM-022 · Business Rules

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-022 |
| **Rol** | SA (`0c128e3b-db3b-4e31-b107-0379b5791233`) |
| **Delivery** | Business Rules |
| **Horas** | 4h |
| **Prioridad** | MEDIUM |
| **Complejidad** | HIGH |
| **Categoría** | documentation |

**Descripción:** Autorar el catálogo completo de reglas de negocio:
- `2.5.1 Business Rules Document` — Marco general de reglas y su enforcement.
- `2.5.2 Rules List (BR-XXX)` — Inventario completo de reglas de negocio numeradas.
- `2.5.3 Validation Rules` — Reglas de validación Zod por endpoint. Descripciones < 2000 chars, UUIDs válidos, enums correctos.
- `2.5.4 Calculation Rules` — Cálculo de costo USD por tokens: `inputTokens * inputCostPer1k / 1000 + outputTokens * outputCostPer1k / 1000`. Solo SDK con costo real.
- `2.5.5 Authorization Rules` — SERVICE_KEY obligatoria en headers. Reglas de acceso por endpoint.
- `2.5.6 State Transition Rules` — PENDING → PROCESSING → IMPORTED/ERROR. AMB-07: catch no mueve a ERROR, delega a cleanup cron 5min.
- `2.5.7 Business Glossary` — Glosario de términos de dominio (conversation, turn, block, agent session, context window, etc.).

**Entregables SDLC:** 2.5.1 · 2.5.2 · 2.5.3 · 2.5.4 · 2.5.5 · 2.5.6 · 2.5.7

---

### MEM-023 · User Flows

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-023 |
| **Rol** | UX (`a75a1dae-754a-4b6f-a3ff-db8d51f6a91b`) |
| **Delivery** | User Flows |
| **Horas** | 4h |
| **Prioridad** | MEDIUM |
| **Complejidad** | MEDIUM |
| **Categoría** | design |

**Descripción:** Autorar los flujos de usuario de la interfaz Memory Service:
- `2.6.1 User Flow Diagrams` — Diagramas de flujo de todas las pantallas UI (Dashboard, Timeline, Viewer, Import, Cost, Health).
- `2.6.2 Happy Path Flows` — Flujos principales sin errores para cada caso de uso UI.
- `2.6.3 Error Flows` — Qué ve el usuario cuando hay error en import, timeout context, health falla.
- `2.6.4 Edge Case Flows` — Conversación vacía, agente sin cost data, lista sin resultados.
- `2.6.5 User Journey Maps` — Jornada completa del TL consultando contexto, y del PM revisando costos.
- `2.6.6 Task Flows` — Flujos orientados a tareas: "Ver Timeline de agente", "Importar conversación manual", "Ver Cost Report proyecto".
- `2.6.7 Navigation Map` — Mapa de navegación entre pantallas de la UI.

**Entregables SDLC:** 2.6.1 · 2.6.2 · 2.6.3 · 2.6.4 · 2.6.5 · 2.6.6 · 2.6.7

---

### MEM-024 · Acceptance Criteria

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-024 |
| **Rol** | SA (`0c128e3b-db3b-4e31-b107-0379b5791233`) |
| **Delivery** | Acceptance Criteria |
| **Horas** | 6h |
| **Prioridad** | MEDIUM |
| **Complejidad** | HIGH |
| **Categoría** | documentation |

**Descripción:** Autorar los criterios de aceptación formales del proyecto:
- `2.7.1 Acceptance Criteria Document` — Marco general y metodología (BDD/Gherkin).
- `2.7.2 AC en formato Gherkin` — Given/When/Then por cada User Story del backlog (mínimo 30 US → 30 AC sets).
- `2.7.3 Definition of Done (DoD)` — Checklist que toda tarea debe cumplir antes de `task_completed`: código compila, tests pasan, docs creadas, Swagger actualizado.
- `2.7.4 Definition of Ready (DoR)` — Checklist que toda tarea debe cumplir antes de `task_in_progress`: ASSIGNMENT leído, dependencias `task_completed`, entorno disponible.
- `2.7.5 Test Scenarios` — Escenarios de prueba por feature (import idempotencia, context <500ms, cleanup cron, health checks).

**Entregables SDLC:** 2.7.1 · 2.7.2 · 2.7.3 · 2.7.4 · 2.7.5

---

### MEM-025 · Traceability Matrix

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-025 |
| **Rol** | SA (`0c128e3b-db3b-4e31-b107-0379b5791233`) |
| **Delivery** | Traceability Matrix |
| **Horas** | 4h |
| **Prioridad** | MEDIUM |
| **Complejidad** | MEDIUM |
| **Categoría** | documentation |

**Descripción:** Autorar la matriz de trazabilidad del proyecto:
- `2.8.1 Traceability Matrix` — Matriz completa RF → US → AC → Test Cases (futura).
- `2.8.2 RF → US Mapping` — Cada requisito funcional trazado a sus User Stories.
- `2.8.3 US → Test Cases Mapping` — Cada User Story trazada a sus escenarios de prueba (anticipado para Fase Testing).
- `2.8.4 Coverage Report` — Informe de cobertura: qué porcentaje de RFs tienen US, AC y Test Cases asociados.

**Entregables SDLC:** 2.8.1 · 2.8.2 · 2.8.3 · 2.8.4

---

## 4. RESUMEN DE TAREAS

| VTT ID | Título | Rol | h | Cmplx | Pri | Delivery |
|--------|--------|-----|--:|-------|:---:|----------|
| MS-018 | Functional Requirements | SA | 6 | HIGH | M | Functional Requirements |
| MS-019 | Non-Functional Requirements | AR | 4 | HIGH | M | Non-Functional Requirements |
| MS-020 | Use Cases | SA | 5 | MEDIUM | M | Use Cases |
| MS-021 | User Stories | SA | 8 | HIGH | M | User Stories |
| MS-022 | Business Rules | SA | 4 | HIGH | M | Business Rules |
| MS-023 | User Flows | UX | 4 | MEDIUM | M | User Flows |
| MS-024 | Acceptance Criteria | SA | 6 | HIGH | M | Acceptance Criteria |
| MS-025 | Traceability Matrix | SA | 4 | MEDIUM | M | Traceability Matrix |
| **TOTAL** | | | **41h** | | | **8 Deliveries** |

---

## 5. DELIVERABLES SDLC PRODUCIDOS

| VTT Delivery | Docs SDLC | Tarea |
|-------------|-----------|-------|
| Functional Requirements | 2.1.1, 2.1.2, 2.1.3, 2.1.4, 2.1.5, 2.1.6 | MEM-018 |
| Non-Functional Requirements | 2.2.1, 2.2.2, 2.2.3, 2.2.4, 2.2.5, 2.2.6 | MEM-019 |
| Use Cases | 2.3.1, 2.3.2, 2.3.3, 2.3.4, 2.3.5, 2.3.6 | MEM-020 |
| User Stories | 2.4.1, 2.4.2, 2.4.3, 2.4.4, 2.4.5, 2.4.6 | MEM-021 |
| Business Rules | 2.5.1, 2.5.2, 2.5.3, 2.5.4, 2.5.5, 2.5.6, 2.5.7 | MEM-022 |
| User Flows | 2.6.1, 2.6.2, 2.6.3, 2.6.4, 2.6.5, 2.6.6, 2.6.7 | MEM-023 |
| Acceptance Criteria | 2.7.1, 2.7.2, 2.7.3, 2.7.4, 2.7.5 | MEM-024 |
| Traceability Matrix | 2.8.1, 2.8.2, 2.8.3, 2.8.4 | MEM-025 |

**Total SDLC:** 43 documentos en 8 VTT Deliveries

---

## 6. USUARIOS VTT ACTIVOS EN ESTA FASE

| Rol | Email | UUID |
|-----|-------|------|
| SA | sa@memory-service.vtt.ai | `0c128e3b-db3b-4e31-b107-0379b5791233` |
| AR | ar@memory-service.vtt.ai | `e9403c25-c1f8-4b64-b2ef-f447d53115e2` |
| UX | ux@memory-service.vtt.ai | `a75a1dae-754a-4b6f-a3ff-db8d51f6a91b` |
| PM | pm@memory-service.vtt.ai | `350831b2-e1ae-4dbe-b2eb-7e023ec2e103` |

---

## 7. GATE DE SALIDA — CRITERIOS DE COMPLETITUD

```
[ ] MEM-018 task_completed — SRS + RF-XXX lista + MoSCoW + Feature List
[ ] MEM-019 task_completed — NFR Performance (<500ms) + Security + Scalability
[ ] MEM-020 task_completed — UML Use Cases + Detailed (Import, Context, Timeline, Cost)
[ ] MEM-021 task_completed — Product Backlog ≥30 US + Story Map + Sprint Assignment
[ ] MEM-022 task_completed — BR-XXX + State Transitions + Calculation Rules
[ ] MEM-023 task_completed — User Flows (7 pantallas) + Journey Maps + Navigation
[ ] MEM-024 task_completed — Gherkin AC por cada US + DoD + DoR + Test Scenarios
[ ] MEM-025 task_completed — Traceability Matrix RF→US→AC completa
[ ] SA sign-off en todos los 2.1.* al 2.8.* (43 docs)
[ ] MEM-026 desbloqueado en VTT (Fase 3A Design UX/UI arranca)
```

---

## 8. RESTRICCIONES Y NOTAS CLAVE

1. **11 endpoints R1 son el scope fijo:** El SRS debe documentar exactamente estos endpoints. Cualquier nuevo endpoint debe pasar por change request con PM.
2. **<500ms es contractual:** MEM-019 debe documentar este NFR con criterio de aceptación medible. Los tests de performance (MEM-061) validarán este SLA en Fase Development.
3. **Idempotencia de import:** La regla `@@unique([sourceId, externalSessionId])` debe estar en el Business Rules (2.5.2) y en los AC (2.7.2).
4. **AMB-07 documentado:** La decisión de que el catch no mueve status a ERROR (delega a cleanup cron 5min) debe aparecer en Business Rules 2.5.6 y en los Gherkin AC.
5. **UX produce User Flows (MEM-023):** El SA y UX deben coordinar para que los flows UX sean consistentes con los Use Cases del SA.

---

## 9. ESCALACIÓN

| Bloqueo | Escalar a |
|---------|-----------|
| Ambigüedad en requisitos funcionales | PM |
| NFRs de performance (cómo medir <500ms) | TL + AR |
| Decisiones de diseño UI en User Flows | DL |
| Ambigüedad en Business Rules técnicas | TL + BE |

---

## 10. FIRMAS

| Rol | Nombre | Firma | Fecha |
|-----|--------|-------|-------|
| **PJM (emite)** | PJM Agent | ✅ EMITIDO | 2026-04-22 |
| **SA (recibe y lidera)** | SA Agent | ⬜ Pendiente acuse | — |
| **PM (valida)** | Martin Rivas | ⬜ Pendiente sign-off | — |

---

## 11. REFERENCIAS

- `TASK_INDEX_SEED_MEMORY_SERVICE.md` v2.1 — §4.4 Analysis tasks
- `SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` — §2 Analysis / Requirements
- `ADDENDUM_INTEGRACION_MEMORY_SERVICE_v1.1.md` — AMB-07, integraciones Hook Manager
- `HO_FASE_1_PLANNING_MEMORY_SERVICE.md` — Gate previo (Scope 1.2.2 y 1.2.3 son input)
- `VTT_UUIDS_MEMORY_SERVICE.json` — UUIDs de tareas MS-018..025

---

**Documento:** HO_FASE_2_ANALYSIS_MEMORY_SERVICE.md  
**Versión:** 1.0  
**Estado:** ✅ EMITIDO — Pendiente sign-off SA y PM  
**Fecha:** 2026-04-22  

---

**PJM — Memory Service**  
Virtual Teams Tracking
