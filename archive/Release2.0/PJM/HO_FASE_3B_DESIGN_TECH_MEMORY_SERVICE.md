# HANDOFF — Fase 3B: Design Technical · Memory Service

| Campo | Valor |
|-------|-------|
| **Documento** | HO_FASE_3B_DESIGN_TECH_MEMORY_SERVICE.md |
| **Versión** | 1.0 |
| **Fecha** | 2026-04-22 |
| **De** | PJM — `0ff63a29-0bc0-465a-b9bd-5f71476bc91d` |
| **Para** | TL — `92225290-6b6b-4c1f-a940-dcb4262507aa` |
| **CC** | AR — `e9403c25-c1f8-4b64-b2ef-f447d53115e2` · DB — `6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7` · BE — `ebbe3cee-abed-4b3b-860d-0a81f632b08a` · DO — `322e3745-9756-4a7c-af11-44b33edef44d` |
| **Rol líder** | TL (Tech Lead) |
| **Proyecto** | Memory Service |
| **Fase VTT** | Design Technical (Phase order 6) |
| **Estado** | ✅ APROBADO — listo para ejecución |

---

## RESUMEN EJECUTIVO

Esta fase produce el **blueprint técnico completo** del Memory Service antes de que BE/DB/FE escriban una línea de código. Tiene 9 tareas VTT (MEM-039..047), 45h totales, y produce 63 documentos técnicos distribuidos en 9 VTT Deliveries.

**Roles activos:** AR · TL · DB · BE · DO  
**Líder de seguimiento:** TL  
**Criterio de entrada:** Gate Analysis cerrado (MEM-025 `task_completed`)  
**Criterio de salida:** MEM-047 `task_completed` + sign-off TL en todos los 3B.* deliverables

> Esta fase puede ejecutarse **en paralelo con Fase 3A Design UX/UI**. Ambas dependen del gate Analysis (MEM-025) y no tienen dependencia entre sí.

---

## 1. ARQUITECTURA DE LA FASE

```
╔══════════════════════════════════════════════════════════════╗
║   GATE DE ENTRADA: MEM-025 task_completed                    ║
║   (Traceability Matrix cerrada — Analysis OK)                ║
║   [puede ejecutarse en paralelo con Fase 3A Design UX/UI]   ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║   DELIVERY 1: Solution Architecture                          ║
║   └─ MEM-039  Solution Architecture   AR   6h  HIGH         ║
║                                                              ║
║   DELIVERY 2: Code Architecture                              ║
║   └─ MEM-040  Code Architecture       TL   4h  HIGH         ║
║                                                              ║
║   DELIVERY 3: Database Design                                ║
║   └─ MEM-041  Database Design         DB   6h  HIGH         ║
║                                                              ║
║   DELIVERY 4: API Design                                     ║
║   └─ MEM-042  API Design              BE   8h  HIGH         ║
║                                                              ║
║   DELIVERY 5: Sequence Diagrams                              ║
║   └─ MEM-043  Sequence Diagrams       AR   6h  HIGH         ║
║                                                              ║
║   DELIVERY 6: ADRs                                           ║
║   └─ MEM-044  ADRs                    TL   4h  MED          ║
║                                                              ║
║   DELIVERY 7: Security Plan                                  ║
║   └─ MEM-045  Security Plan           AR   4h  HIGH         ║
║                                                              ║
║   DELIVERY 8: Infrastructure Plan                            ║
║   └─ MEM-046  Infrastructure Plan     DO   4h  MED          ║
║                                                              ║
║   DELIVERY 9: Technical Estimates                            ║
║   └─ MEM-047  Technical Estimates     TL   3h  MED          ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║   GATE DE SALIDA: 9/9 tasks completed + 63 docs técnicos     ║
║   → Habilita Fase 4 Development (MEM-048)                   ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 2. DEPENDENCIAS INTERNAS

```
MEM-025 (Analysis gate)
    │
    ▼
MEM-039 (Solution Architecture) — AR — PUNTO DE PARTIDA
    │
    ├─────────────────────────────────────────────────────► MEM-040 (Code Arch — TL)
    │
    ├─────────────────────────────────────────────────────► MEM-041 (DB Design — DB)
    │
    ├─────────────────────────────────────────────────────► MEM-042 (API Design — BE)
    │
    ├─────────────────────────────────────────────────────► MEM-043 (Sequence Diagrams — AR)
    │
    ├─────────────────────────────────────────────────────► MEM-044 (ADRs — TL)
    │
    ├─────────────────────────────────────────────────────► MEM-045 (Security Plan — AR)
    │
    └─────────────────────────────────────────────────────► MEM-046 (Infra Plan — DO)
                                                                  │
                                            MEM-042 (API Design) ─┘
                                                                  │
                                                                  ▼
                                                           MEM-047 (Technical Estimates — TL)
```

**Notas de ejecución:**
- MEM-039 (Solution Architecture) es el punto de partida — define el marco para todo lo demás
- MEM-040..046 pueden ejecutarse en paralelo una vez MEM-039 completado
- MEM-047 (Estimates) debe esperar a MEM-042 (API Design finalizado para estimar esfuerzo real)
- AR lidera MEM-039, MEM-043 y MEM-045 — mayor carga en este rol

---

## 3. TAREAS VTT — DETALLE

### MEM-039 · Solution Architecture

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-039 |
| **Rol** | AR (`e9403c25-c1f8-4b64-b2ef-f447d53115e2`) |
| **Delivery** | Solution Architecture |
| **Horas** | 6h |
| **Prioridad** | MEDIUM |
| **Complejidad** | HIGH |
| **Categoría** | documentation |

**Descripción:** Autorar el documento de arquitectura de solución del Memory Service:
- `3B.1.1 Architecture Document` — Vista general de la arquitectura: componentes, responsabilidades, interacciones.
- `3B.1.2 C4 Level 1 (Context)` — Diagrama de contexto: Memory Service y sus relaciones con VTT Runtime, Prompt Builder, Hook Manager, UI, storage.
- `3B.1.3 C4 Level 2 (Container)` — Contenedores: API (Node/Express), BD (PostgreSQL), Storage (filesystem), Redis (cache).
- `3B.1.4 C4 Level 3 (Component)` — Componentes internos: controllers, services, adapters, jobs, middleware.
- `3B.1.5 Tech Stack` — Stack seleccionado con justificación: Node 20 + TypeScript + Express + Prisma + PostgreSQL + Redis.
- `3B.1.6 Integration Points` — Interfaces con sistemas externos: Hook Manager (POST /import), Prompt Builder (GET /context), VTT Runtime (POST /import con CLAUDE_SDK).
- `3B.1.7 Data Flow Diagram` — Flujo de datos de la importación y recuperación de contexto.

**Entregables SDLC:** 3B.1.1 · 3B.1.2 · 3B.1.3 · 3B.1.4 · 3B.1.5 · 3B.1.6 · 3B.1.7

---

### MEM-040 · Code Architecture

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-040 |
| **Rol** | TL (`92225290-6b6b-4c1f-a940-dcb4262507aa`) |
| **Delivery** | Code Architecture |
| **Horas** | 4h |
| **Prioridad** | MEDIUM |
| **Complejidad** | HIGH |
| **Categoría** | documentation |

**Descripción:** Autorar el blueprint de arquitectura de código:
- `3B.2.1 Folder Structure` — Estructura de carpetas: `src/` (routes, controllers, services, adapters, middleware, jobs, schemas, utils, config), `prisma/`, `knowledge/`, `docs/`.
- `3B.2.2 Coding Standards` — Convenciones de TypeScript estricto, naming (camelCase, PascalCase), imports, exports.
- `3B.2.3 Design Patterns` — Patrones usados: Repository, Adapter, Service Layer, Factory para adapters. Sin ORM para queries complejas (raw SQL con Prisma).
- `3B.2.4 Module Dependencies` — Grafo de dependencias entre módulos (qué importa qué).
- `3B.2.5 Naming Conventions` — Convenciones de nombres para archivos, clases, funciones, tipos, constantes.
- `3B.2.6 Error Handling Strategy` — Middleware de error centralizado. Zod para validación. MEM-ERR-* error codes. AMB-07: catch no mueve a ERROR.

**Entregables SDLC:** 3B.2.1 · 3B.2.2 · 3B.2.3 · 3B.2.4 · 3B.2.5 · 3B.2.6

---

### MEM-041 · Database Design

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-041 |
| **Rol** | DB (`6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7`) |
| **Delivery** | Database Design |
| **Horas** | 6h |
| **Prioridad** | MEDIUM |
| **Complejidad** | HIGH |
| **Categoría** | documentation |

**Descripción:** Autorar el diseño completo de la base de datos:
- `3B.3.1 ERD` — Diagrama Entidad-Relación de las 19 tablas principales + 10 tablas de catálogo.
- `3B.3.2 Prisma Schema` — Schema Prisma completo con constraints únicos: `@@unique([sourceId, externalSessionId])`, `@@unique([conversationId, turnIndex])`, `@@unique([turnId, blockIndex])`, `@@unique([conversationId, entityName])`.
- `3B.3.3 Table Specifications` — Especificación de cada tabla: columnas, tipos, constraints, índices, relaciones.
- `3B.3.4 Index Strategy` — Índices partial: `idx_conv_agent_time`, `idx_conv_task`. Índice GIN: `idx_conv_runtime_run` (ADDENDUM §5.3). Índice: `idx_block_filepath`.
- `3B.3.5 Data Dictionary` — Diccionario de datos: significado de cada campo en contexto del dominio.
- `3B.3.6 Migration Strategy` — Estrategia para migraciones: Prisma migrate deploy, partial_indexes.sql adicional.
- `3B.3.7 Seed Plan` — Plan de seeds: 10 catálogos con datos iniciales obligatorios.
- `3B.3.8 Backup Strategy` — Estrategia de backup para servidor único Hetzner.

**Entregables SDLC:** 3B.3.1 · 3B.3.2 · 3B.3.3 · 3B.3.4 · 3B.3.5 · 3B.3.6 · 3B.3.7 · 3B.3.8

---

### MEM-042 · API Design

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-042 |
| **Rol** | BE (`ebbe3cee-abed-4b3b-860d-0a81f632b08a`) |
| **Delivery** | API Design |
| **Horas** | 8h |
| **Prioridad** | MEDIUM |
| **Complejidad** | HIGH |
| **Categoría** | documentation |

**Descripción:** Autorar el diseño completo de la API del Memory Service:
- `3B.4.1 OpenAPI Spec` — Especificación OpenAPI 3.0 completa de los 11 endpoints R1.
- `3B.4.2 Endpoints Documentation` — Descripción detallada de cada endpoint: método, path, params, body, responses. Los 11 endpoints: POST /import, POST /import-review, POST /upload, GET /content, GET /context, GET /agents/:id/timeline, GET /conversations, GET /projects/:id/cost-report, GET /agents/:id/cost-report, GET /dashboard/stats, GET /health.
- `3B.4.3 Request/Response Examples` — Ejemplos reales de request y response por endpoint.
- `3B.4.4 Pagination Strategy` — Paginación cursor basada en `startedAt DESC` para lista y timeline.
- `3B.4.5 Error Codes (MEM-ERR-*)` — Catálogo de códigos de error propios: MEM-ERR-001..MEM-ERR-504.
- `3B.4.6 Authentication Design` — SERVICE_KEY en header `X-Service-Key`. Excepciones (POST /upload sin key).
- `3B.4.7 Authorization Design` — Reglas de acceso por endpoint según caller (Runtime, PB, Hook Manager, UI).
- `3B.4.8 Rate Limiting` — Límites de rate por endpoint y por caller.
- `3B.4.9 API Versioning` — Estrategia de versionado (sin versión en R1, preparar para v2).
- `3B.4.10 Postman Collection` — Colección Postman con todos los endpoints y ejemplos.
- `3B.4.11 API Guidelines` — Convenciones de la API: naming, casing, paginación, filtros, errores.

**Entregables SDLC:** 3B.4.1 · 3B.4.2 · 3B.4.3 · 3B.4.4 · 3B.4.5 · 3B.4.6 · 3B.4.7 · 3B.4.8 · 3B.4.9 · 3B.4.10 · 3B.4.11

---

### MEM-043 · Sequence Diagrams

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-043 |
| **Rol** | AR (`e9403c25-c1f8-4b64-b2ef-f447d53115e2`) |
| **Delivery** | Sequence Diagrams |
| **Horas** | 6h |
| **Prioridad** | MEDIUM |
| **Complejidad** | HIGH |
| **Categoría** | documentation |

**Descripción:** Autorar los diagramas de secuencia del sistema:
- `3B.5.1 Sequence Diagrams Document` — Marco y convenciones de los diagramas.
- `3B.5.2 Auth Flow` — Flujo de autenticación: cómo se valida SERVICE_KEY en cada request.
- `3B.5.3 Business Flows` — Flujos principales: Import (4 fuentes → adapters → BD → storage), Context (<500ms parallel queries), Cleanup cron (5min STALE→retry).
- `3B.5.4 Error Flows` — Qué pasa en cada punto de fallo: BD down, storage error, timeout context, adapter falla.
- `3B.5.5 Integration Flows` — Flujos de integración externa: Runtime → Hook Manager → Memory Service (import), Prompt Builder → Memory Service (GET /context), PJM cargando datos a VTT.
- `3B.5.6 Async Flows` — Flujos asíncronos: cleanup job, status transitions, import-review multi-agente.

**Entregables SDLC:** 3B.5.1 · 3B.5.2 · 3B.5.3 · 3B.5.4 · 3B.5.5 · 3B.5.6

---

### MEM-044 · ADRs

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-044 |
| **Rol** | TL (`92225290-6b6b-4c1f-a940-dcb4262507aa`) |
| **Delivery** | ADRs |
| **Horas** | 4h |
| **Prioridad** | MEDIUM |
| **Complejidad** | MEDIUM |
| **Categoría** | documentation |

**Descripción:** Formalizar las decisiones de arquitectura tomadas durante el diseño:
- `3B.6.1 ADR Template` — Plantilla estándar para los ADRs (contexto, decisión, consecuencias, estado).
- `3B.6.2 ADR Index` — Índice de los 48 ADRs: 43 decisiones D-MEM + 5 decisiones D-INT de integración.
- `3B.6.3 ADR Documents` — Documentos individuales para las decisiones más críticas (D-MEM-01 Prisma ORM, D-MEM-06 storage JSONL, D-MEM-35 cleanup cron, D-MEM-39 filtrado projectId, D-MEM-43 NO leer BD en /content, D-INT-01..05 integraciones).
- `3B.6.4 Decision Log` — Log cronológico de cuándo y por qué se tomó cada decisión.

**Entregables SDLC:** 3B.6.1 · 3B.6.2 · 3B.6.3 · 3B.6.4

---

### MEM-045 · Security Plan

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-045 |
| **Rol** | AR (`e9403c25-c1f8-4b64-b2ef-f447d53115e2`) |
| **Delivery** | Security Plan |
| **Horas** | 4h |
| **Prioridad** | MEDIUM |
| **Complejidad** | HIGH |
| **Categoría** | documentation |

**Descripción:** Autorar el plan de seguridad del sistema:
- `3B.7.1 Security Plan` — Marco general de seguridad del Memory Service.
- `3B.7.2 Authentication (SERVICE_KEY)` — Implementación y validación de SERVICE_KEY. Casos donde no se requiere (POST /upload público).
- `3B.7.3 Authorization` — Control de acceso por endpoint y por caller.
- `3B.7.4 Data Protection` — Qué datos son sensibles (tokens, conversaciones) y cómo se protegen.
- `3B.7.5 Encryption` — Datos en tránsito (HTTPS) y en reposo (si aplica).
- `3B.7.6 OWASP Compliance` — Mitigaciones para OWASP Top 10 en el contexto del Memory Service.
- `3B.7.7 Security Headers` — Headers HTTP de seguridad (helmet, CORS, CSP).
- `3B.7.8 Secrets Management` — Gestión de SERVICE_KEY y credenciales de BD en secrets de GitHub Actions.
- `3B.7.9 Input Validation` — Validación Zod en todos los endpoints. Sin SQL injection posible con Prisma.
- `3B.7.10 Security Logging` — Qué eventos de seguridad se loguean (auth failures, rate limit, etc.).
- `3B.7.11 Incident Response` — Qué hacer si se compromete la SERVICE_KEY o hay breach.

**Entregables SDLC:** 3B.7.1 · 3B.7.2 · 3B.7.3 · 3B.7.4 · 3B.7.5 · 3B.7.6 · 3B.7.7 · 3B.7.8 · 3B.7.9 · 3B.7.10 · 3B.7.11

---

### MEM-046 · Infrastructure Plan

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-046 |
| **Rol** | DO (`322e3745-9756-4a7c-af11-44b33edef44d`) |
| **Delivery** | Infrastructure Plan |
| **Horas** | 4h |
| **Prioridad** | MEDIUM |
| **Complejidad** | MEDIUM |
| **Categoría** | documentation |

**Descripción:** Autorar el plan de infraestructura del Memory Service:
- `3B.8.1 Infrastructure Plan` — Visión general de la infraestructura.
- `3B.8.2 Infrastructure Diagram` — Diagrama del servidor Hetzner (77.42.88.106): Docker containers, shared-network, shared-postgres, Redis, storage volume.
- `3B.8.3 Server Specifications` — Specs del servidor: CPU, RAM, disco, OS, Docker version.
- `3B.8.4 Network Configuration` — shared-network Docker, firewall reglas puertos 3002 (API) y 3003 (UI si aplica).
- `3B.8.5 Environment Matrix` — Variables de entorno por entorno (local, staging, production) con valores ejemplo.
- `3B.8.6 Scaling Strategy` — Cómo escalar en R1 (no HA) y qué se necesitaría para HA en R2.
- `3B.8.7 Backup Plan` — Estrategia de backup de BD y storage. Frecuencia, retención, restore procedure.
- `3B.8.8 Disaster Recovery` — Plan DR para servidor único: tiempo de recuperación estimado, pasos de restore.
- `3B.8.9 Infrastructure Cost` — Costo estimado de la infraestructura (ya pagado como parte de VTT).
- `3B.8.10 SLA Definition` — SLA del servicio: uptime objetivo, `<500ms` p95 GET /context.
- `3B.8.11 Monitoring Plan` — Qué se monitorea: latencia, errores, storage usage, BD connections.

**Entregables SDLC:** 3B.8.1 · 3B.8.2 · 3B.8.3 · 3B.8.4 · 3B.8.5 · 3B.8.6 · 3B.8.7 · 3B.8.8 · 3B.8.9 · 3B.8.10 · 3B.8.11

---

### MEM-047 · Technical Estimates

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-047 |
| **Rol** | TL (`92225290-6b6b-4c1f-a940-dcb4262507aa`) |
| **Delivery** | Technical Estimates |
| **Horas** | 3h |
| **Prioridad** | MEDIUM |
| **Complejidad** | MEDIUM |
| **Categoría** | documentation |

**Descripción:** Autorar las estimaciones técnicas del proyecto:
- `3B.9.1 Technical Estimates` — Estimación total: 381h distribuidas por fase y rol.
- `3B.9.2 Story Points` — Puntos de historia por US (calibrados con velocidad de referencia).
- `3B.9.3 Task Breakdown` — Desglose de horas por tarea en Development: S01(9h) + S02(12h) + S03(12h) + S04(12h) + S05(11h) + S06(14h) + UI-01..04.
- `3B.9.4 Effort Matrix` — Matriz de esfuerzo por rol × fase.
- `3B.9.5 Complexity Analysis` — Análisis de complejidad técnica: HIGH (MEM-059 GET /context <500ms, MEM-048 Schema 19 tablas, MEM-042 API 11 endpoints).
- `3B.9.6 Risk-Adjusted Estimates` — Estimaciones con buffer por riesgo (15% para integración Hook Manager, 20% para performance <500ms).
- `3B.9.7 Dependencies Map` — Mapa de las 78 dependencias registradas en VTT (15 críticas + 63 intra-fase).
- `3B.9.8 Team Velocity` — Velocidad estimada del equipo de agentes IA por sprint.
- `3B.9.9 Capacity Plan` — Capacidad disponible por rol durante el proyecto.

**Entregables SDLC:** 3B.9.1 · 3B.9.2 · 3B.9.3 · 3B.9.4 · 3B.9.5 · 3B.9.6 · 3B.9.7 · 3B.9.8 · 3B.9.9

---

## 4. RESUMEN DE TAREAS

| VTT ID | Título | Rol | h | Cmplx | Pri | Delivery |
|--------|--------|-----|--:|-------|:---:|----------|
| MS-039 | Solution Architecture | AR | 6 | HIGH | M | Solution Architecture |
| MS-040 | Code Architecture | TL | 4 | HIGH | M | Code Architecture |
| MS-041 | Database Design | DB | 6 | HIGH | M | Database Design |
| MS-042 | API Design | BE | 8 | HIGH | M | API Design |
| MS-043 | Sequence Diagrams | AR | 6 | HIGH | M | Sequence Diagrams |
| MS-044 | ADRs | TL | 4 | MEDIUM | M | ADRs |
| MS-045 | Security Plan | AR | 4 | HIGH | M | Security Plan |
| MS-046 | Infrastructure Plan | DO | 4 | MEDIUM | M | Infrastructure Plan |
| MS-047 | Technical Estimates | TL | 3 | MEDIUM | M | Technical Estimates |
| **TOTAL** | | | **45h** | | | **9 Deliveries** |

---

## 5. DELIVERABLES SDLC PRODUCIDOS

| VTT Delivery | Docs SDLC | Tarea |
|-------------|-----------|-------|
| Solution Architecture | 3B.1.1..3B.1.7 (7 docs) | MEM-039 |
| Code Architecture | 3B.2.1..3B.2.6 (6 docs) | MEM-040 |
| Database Design | 3B.3.1..3B.3.8 (8 docs) | MEM-041 |
| API Design | 3B.4.1..3B.4.11 (11 docs) | MEM-042 |
| Sequence Diagrams | 3B.5.1..3B.5.6 (6 docs) | MEM-043 |
| ADRs | 3B.6.1..3B.6.4 (4 docs + 48 ADRs) | MEM-044 |
| Security Plan | 3B.7.1..3B.7.11 (11 docs) | MEM-045 |
| Infrastructure Plan | 3B.8.1..3B.8.11 (11 docs) | MEM-046 |
| Technical Estimates | 3B.9.1..3B.9.9 (9 docs) | MEM-047 |

**Total SDLC:** 63 documentos + 48 ADRs individuales en 9 VTT Deliveries

---

## 6. USUARIOS VTT ACTIVOS EN ESTA FASE

| Rol | Email | UUID |
|-----|-------|------|
| AR | ar@memory-service.vtt.ai | `e9403c25-c1f8-4b64-b2ef-f447d53115e2` |
| TL | tl@memory-service.vtt.ai | `92225290-6b6b-4c1f-a940-dcb4262507aa` |
| DB | db@memory-service.vtt.ai | `6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7` |
| BE | be@memory-service.vtt.ai | `ebbe3cee-abed-4b3b-860d-0a81f632b08a` |
| DO | do@memory-service.vtt.ai | `322e3745-9756-4a7c-af11-44b33edef44d` |
| PM | pm@memory-service.vtt.ai | `350831b2-e1ae-4dbe-b2eb-7e023ec2e103` |

---

## 7. GATE DE SALIDA — CRITERIOS DE COMPLETITUD

```
[ ] MEM-039 task_completed — C4 L1/L2/L3 + Tech Stack + Integration Points + Data Flow
[ ] MEM-040 task_completed — Folder Structure + Coding Standards + Design Patterns + Error Handling
[ ] MEM-041 task_completed — ERD 19 tablas + Prisma Schema + Index Strategy + Seed Plan
[ ] MEM-042 task_completed — OpenAPI Spec 11 endpoints + Postman Collection + Error Codes MEM-ERR-*
[ ] MEM-043 task_completed — Sequence Diagrams (Import, Context, Cleanup, Integration flows)
[ ] MEM-044 task_completed — 48 ADRs formalizados (43 D-MEM + 5 D-INT)
[ ] MEM-045 task_completed — Security Plan + OWASP + SERVICE_KEY + Incident Response
[ ] MEM-046 task_completed — Infra Diagram Hetzner + DR Plan + SLA <500ms documentado
[ ] MEM-047 task_completed — 381h estimadas + Dependencies Map 78 deps + Risk-adjusted
[ ] TL sign-off en todos los 3B.* deliverables
[ ] MEM-048 desbloqueado en VTT (Fase 4 Development arranca)
```

---

## 8. RESTRICCIONES Y NOTAS CLAVE

1. **19 tablas + 10 catálogos:** MEM-041 debe diseñar exactamente este número de tablas. Cambios de schema requieren aprobación TL.
2. **11 endpoints R1 = scope fijo:** MEM-042 documenta solo estos 11. Cualquier nuevo endpoint es change request.
3. **48 ADRs:** El índice de D-MEM y D-INT del SPEC v1.9 debe formalizarse completamente en MEM-044. No inventar nuevas decisiones — documentar las ya tomadas.
4. **AMB-07 en Sequence Diagrams:** La decisión de catch sin mover a ERROR (delega a cleanup) debe aparecer en los Error Flows (MEM-043 3B.5.4).
5. **Parallel con Fase 3A:** Esta fase no depende de los wireframes UX. Puede ejecutarse completamente en paralelo con Design UX/UI.
6. **AR tiene la mayor carga:** 3 tareas (MEM-039, MEM-043, MEM-045) = 16h. Planificar entregas AR con TL.

---

## 9. ESCALACIÓN

| Bloqueo | Escalar a |
|---------|-----------|
| Conflicto en decisiones de arquitectura | PM + AR |
| Dudas sobre integraciones Hook Manager / Runtime | PM |
| Ambigüedad en schema BD (tabla vs columna) | TL + SA |
| Requisitos de seguridad adicionales | PM |
| Cambio en estimaciones (±20%) | PM + PJM |

---

## 10. FIRMAS

| Rol | Nombre | Firma | Fecha |
|-----|--------|-------|-------|
| **PJM (emite)** | PJM Agent | ✅ EMITIDO | 2026-04-22 |
| **TL (recibe y lidera)** | TL Agent | ⬜ Pendiente acuse | — |
| **AR (recibe)** | AR Agent | ⬜ Pendiente acuse | — |
| **PM (valida)** | Martin Rivas | ⬜ Pendiente sign-off | — |

---

## 11. REFERENCIAS

- `TASK_INDEX_SEED_MEMORY_SERVICE.md` v2.1 — §4.6 Design Technical tasks
- `SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` — §3B Design Technical + ADRs D-MEM-* y D-INT-*
- `ADDENDUM_INTEGRACION_MEMORY_SERVICE_v1.1.md` — §5 Partial indexes, integración hooks
- `HO_FASE_2_ANALYSIS_MEMORY_SERVICE.md` — Gate previo (FR, NFR, BizRules son inputs clave)
- `VTT_UUIDS_MEMORY_SERVICE.json` — UUIDs de tareas MS-039..047

---

**Documento:** HO_FASE_3B_DESIGN_TECH_MEMORY_SERVICE.md  
**Versión:** 1.0  
**Estado:** ✅ EMITIDO — Pendiente sign-off TL y PM  
**Fecha:** 2026-04-22  

---

**PJM — Memory Service**  
Virtual Teams Tracking
