# HANDOFF — Fase 5: Testing · Memory Service

| Campo | Valor |
|-------|-------|
| **Documento** | HO_FASE_5_TESTING_MEMORY_SERVICE.md |
| **Versión** | 1.0 |
| **Fecha** | 2026-04-22 |
| **De** | PJM — `0ff63a29-0bc0-465a-b9bd-5f71476bc91d` |
| **Para** | QA — `613c9538-658c-45fe-a6d7-c1ea9ff04b78` |
| **CC** | TL — `92225290-6b6b-4c1f-a940-dcb4262507aa` · AR — `e9403c25-c1f8-4b64-b2ef-f447d53115e2` · PM — `350831b2-e1ae-4dbe-b2eb-7e023ec2e103` · BE — `ebbe3cee-abed-4b3b-860d-0a81f632b08a` |
| **Rol líder** | QA |
| **Proyecto** | Memory Service |
| **Fase VTT** | Testing (Phase order 8) |
| **Estado** | ✅ APROBADO — listo para ejecución |

---

## RESUMEN EJECUTIVO

Esta fase valida **la calidad total del sistema** antes del deploy a producción. Tiene 10 tareas VTT (MEM-094..103), 60h totales, distribuidas en 10 VTT Deliveries. Incluye performance testing del SLA contractual `<500ms`.

**Roles activos:** QA · AR · PM · BE  
**Líder de seguimiento:** QA  
**Criterio de entrada:** Gate Development cerrado (MEM-093 `task_completed`)  
**Criterio de salida:** MEM-103 `task_completed` + todos los SLAs verificados + UAT aprobado por PM

---

## 1. ARQUITECTURA DE LA FASE

```
╔══════════════════════════════════════════════════════════════╗
║   GATE DE ENTRADA: MEM-093 task_completed                    ║
║   (Development completo — todos los 11 endpoints + UI)       ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║   DELIVERY 1: Test Planning                                  ║
║   └─ MEM-094  Test Planning        QA   4h  MED             ║
║                                                              ║
║   DELIVERY 2: Test Cases                                     ║
║   └─ MEM-095  Test Cases completos QA   8h  MED             ║
║                                                              ║
║   DELIVERY 3: Test Environment                               ║
║   └─ MEM-096  Test Environment     DO   4h  MED             ║
║                                                              ║
║   DELIVERY 4: Functional Testing                             ║
║   └─ MEM-097  Functional Testing   QA   8h  MED             ║
║                                                              ║
║   DELIVERY 5: Integration Testing                            ║
║   └─ MEM-098  Integration Testing  QA   6h  MED             ║
║                                                              ║
║   DELIVERY 6: E2E Testing                                    ║
║   └─ MEM-099  E2E Testing          QA   8h  MED             ║
║                                                              ║
║   DELIVERY 7: Performance Testing                            ║
║   └─ MEM-100  Performance Testing  QA   6h  CRITICAL        ║
║                                                              ║
║   DELIVERY 8: Security Testing                               ║
║   └─ MEM-101  Security Testing     AR   4h  HIGH            ║
║                                                              ║
║   DELIVERY 9: UAT                                            ║
║   └─ MEM-102  UAT                  PM   4h  MED             ║
║                                                              ║
║   DELIVERY 10: Bug Fixes                                     ║
║   └─ MEM-103  Bug Fixes            BE   8h  MED             ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║   GATE DE SALIDA: MEM-103 completed + SLAs OK + UAT aprobado ║
║   → Habilita Fase 6 Deploy (MEM-104)                         ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 2. DEPENDENCIAS INTERNAS

```
MEM-093 (Development gate)
    │
    ▼
MEM-094 (Test Planning)
    │
    ├──────────────────────────────────► MEM-095 (Test Cases)
    │                                          │
    └──────────────────────────────────► MEM-096 (Test Environment)
                                               │
                              ┌────────────────┴─────────────────────┐
                              ▼                                       ▼
                        MEM-097 (Functional)                   MEM-098 (Integration)
                              │                                       │
                              └─────────────────────┬────────────────┘
                                                    ▼
                                              MEM-099 (E2E)
                                                    │
                                    ┌───────────────┴───────────────┐
                                    ▼                               ▼
                             MEM-100 (Performance)         MEM-101 (Security)
                                    │                               │
                                    └───────────────┬───────────────┘
                                                    ▼
                                              MEM-102 (UAT)
                                                    │
                                                    ▼
                                              MEM-103 (Bug Fixes)
```

---

## 3. TAREAS VTT — DETALLE

### MEM-094 · Test Planning

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-094 |
| **Rol** | QA (`613c9538-658c-45fe-a6d7-c1ea9ff04b78`) |
| **Delivery** | Test Planning |
| **Horas** | 4h |
| **Prioridad** | MEDIUM |
| **Complejidad** | MEDIUM |
| **Categoría** | testing |

**Descripción:** Definir la estrategia de testing del Memory Service:
- Plan de pruebas: objetivos, alcance, criterios de entrada/salida por tipo de test.
- Tipos de testing definidos: Functional, Integration, E2E, Performance (SLA <500ms), Security (OWASP).
- Herramientas seleccionadas: Jest/Vitest (unit/functional), Supertest (API integration), k6 (performance), OWASP ZAP o Playwright (security/E2E).
- Entornos de prueba: local, staging.
- Responsabilidades por tipo de test.
- Métricas de calidad: cobertura mínima por capa, criterios de pass/fail.

---

### MEM-095 · Test Cases Completos

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-095 |
| **Rol** | QA (`613c9538-658c-45fe-a6d7-c1ea9ff04b78`) |
| **Delivery** | Test Cases |
| **Horas** | 8h |
| **Prioridad** | MEDIUM |
| **Complejidad** | HIGH |
| **Categoría** | testing |

**Descripción:** Crear el inventario completo de casos de prueba:
- Test cases para los 11 endpoints: happy path, error cases, edge cases.
- Test cases de idempotencia (import con misma [sourceId, externalSessionId] → ALREADY_INDEXED).
- Test cases de performance: GET /context con 100 conv × 10 agentes × 5 proyectos.
- Test cases de estado: PENDING → PROCESSING → IMPORTED/ERROR transiciones.
- Test cases UI: cada pantalla con estados empty/loading/error/success.
- Mapeo de test cases a User Stories del backlog (para traceability).

---

### MEM-096 · Test Environment Setup

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-096 |
| **Rol** | DO (`322e3745-9756-4a7c-af11-44b33edef44d`) |
| **Delivery** | Test Environment |
| **Horas** | 4h |
| **Prioridad** | MEDIUM |
| **Complejidad** | MEDIUM |
| **Categoría** | testing |

**Descripción:** Configurar el entorno de testing:
- BD de test aislada (memory_service_test) con seed fresh por test suite.
- Storage de test en directorio temporal.
- Variables de entorno para test (`.env.test`).
- Scripts: `npm run test`, `npm run test:integration`, `npm run test:e2e`, `npm run test:perf`.
- CI pipeline integrado con los test suites.
- Mock del Hook Manager para tests de integración.

---

### MEM-097 · Functional Testing

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-097 |
| **Rol** | QA (`613c9538-658c-45fe-a6d7-c1ea9ff04b78`) |
| **Delivery** | Functional Testing |
| **Horas** | 8h |
| **Prioridad** | MEDIUM |
| **Complejidad** | HIGH |
| **Categoría** | testing |

**Descripción:** Ejecutar pruebas funcionales de todos los endpoints:
- POST /import: 4 fuentes (CLAUDE_SDK, CLAUDE_WEB, CHATGPT, VTT_CHANNEL), idempotencia, validación Zod.
- POST /import-review: multi-agente, primaryAgentId=NULL, ConversationParticipant persistido.
- POST /upload: sin SERVICE_KEY, auto-detección de fuente, delegación al flujo interno.
- GET /content: parseo desde storage, sin query BD.
- GET /context: filtrado projectId obligatorio, SLA deferido a Performance Testing.
- GET /agents/:id/timeline: paginación cursor, filtros.
- GET /conversations: filtros múltiples combinados.
- GET /projects/:id/cost-report y GET /agents/:id/cost-report: cálculo costo USD correcto.
- GET /dashboard/stats: totales y métricas agregadas.
- GET /health: BD + storage + Redis checks.

---

### MEM-098 · Integration Testing

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-098 |
| **Rol** | QA (`613c9538-658c-45fe-a6d7-c1ea9ff04b78`) |
| **Delivery** | Integration Testing |
| **Horas** | 6h |
| **Prioridad** | MEDIUM |
| **Complejidad** | HIGH |
| **Categoría** | testing |

**Descripción:** Probar las integraciones entre componentes internos y externos:
- BE ↔ BD Prisma: queries, transacciones, constraints únicos.
- BE ↔ Storage filesystem: save() TASK y saveReview() REVIEW.
- BE ↔ Redis catalog cache: hit/miss, invalidación.
- Cleanup cron ↔ BD: detección STALE >10min, retry ≤3, transición a ERROR tras max retries.
- Mock Hook Manager → POST /import: verifica SERVICE_KEY, persistencia, idempotencia.
- Mock Prompt Builder → GET /context: verifica estructura JSON, filtrado projectId, latencia.

---

### MEM-099 · E2E Testing

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-099 |
| **Rol** | QA (`613c9538-658c-45fe-a6d7-c1ea9ff04b78`) |
| **Delivery** | E2E Testing |
| **Horas** | 8h |
| **Prioridad** | MEDIUM |
| **Complejidad** | HIGH |
| **Categoría** | testing |

**Descripción:** Pruebas end-to-end del sistema completo:
- Flujo completo import → contexto: importar conv → consultar /context → verificar respuesta.
- Flujo UI completo: abrir Timeline, seleccionar conversación, ver Viewer, navegar a Cost Report.
- Flujo import manual UI: drag & drop archivo JSON → progress → success → aparece en lista.
- Flujo health monitoring: verificar pantalla Health refleja estado real de servicios.
- Pruebas cross-browser: Chrome + Firefox (desktop).

---

### MEM-100 · Performance Testing

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-100 |
| **Rol** | QA (`613c9538-658c-45fe-a6d7-c1ea9ff04b78`) |
| **Delivery** | Performance Testing |
| **Horas** | 6h |
| **Prioridad** | **CRITICAL** |
| **Complejidad** | HIGH |
| **Categoría** | testing |

**Descripción:** Validar el SLA contractual `<500ms` p95 para GET /context:
- Benchmark k6 con 100 conversaciones × 10 agentes × 5 proyectos (dataset representativo).
- Métricas: p50, p95, p99, max latencia. Objetivo: p95 < 500ms.
- Prueba de carga: 50 usuarios concurrentes durante 5 minutos.
- Prueba de stress: identificar punto de quiebre.
- Prueba de throughput: import de 1000 conversaciones en batch.
- Reporte con gráficos de percentiles. Si p95 > 500ms → **tarea rechazada, escalar a TL**.

> 🚨 Si este test falla el criterio `p95 <500ms`, NO se puede avanzar a Deploy. TL debe revisar implementación MEM-059.

---

### MEM-101 · Security Testing

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-101 |
| **Rol** | AR (`e9403c25-c1f8-4b64-b2ef-f447d53115e2`) |
| **Delivery** | Security Testing |
| **Horas** | 4h |
| **Prioridad** | HIGH |
| **Complejidad** | HIGH |
| **Categoría** | testing |

**Descripción:** Validar el plan de seguridad del Memory Service:
- Prueba de autenticación: endpoints con SERVICE_KEY incorrecta/ausente → 401.
- Prueba de POST /upload sin key → debe aceptar (excepción documentada).
- Validación Zod: enviar payloads malformados → 400 con mensaje correcto.
- Headers de seguridad: verificar helmet headers en responses.
- OWASP básico: SQL injection attempt (protegido por Prisma), XSS en strings (sanitización).
- Rate limiting: verificar que se activa tras umbral definido.
- SERVICE_KEY no expuesta en logs ni responses.

---

### MEM-102 · UAT

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-102 |
| **Rol** | PM (`350831b2-e1ae-4dbe-b2eb-7e023ec2e103`) |
| **Delivery** | UAT |
| **Horas** | 4h |
| **Prioridad** | MEDIUM |
| **Complejidad** | MEDIUM |
| **Categoría** | testing |

**Descripción:** User Acceptance Testing del sistema completo:
- PM realiza pruebas de aceptación desde la perspectiva de usuario final.
- Validar que los AC de las User Stories se cumplen (DoD verificado).
- Recorrer la UI: Dashboard → Timeline → Conversation Viewer → Cost Report → Health.
- Importar una conversación manualmente vía UI y verificar que aparece en lista y viewer.
- Verificar Cost Report: cifras de costo USD coherentes.
- Aprobar o rechazar con feedback específico por pantalla/endpoint.
- Sign-off formal del PM para habilitar Deploy.

---

### MEM-103 · Bug Fixes

| Campo | Valor |
|-------|-------|
| **VTT ID** | MS-103 |
| **Rol** | BE (`ebbe3cee-abed-4b3b-860d-0a81f632b08a`) |
| **Delivery** | Bug Fixes |
| **Horas** | 8h |
| **Prioridad** | MEDIUM |
| **Complejidad** | HIGH |
| **Categoría** | bugfix |

**Descripción:** Corrección de bugs encontrados en MEM-097..102. Buffer de 8h para:
- Bugs críticos bloqueantes del deploy.
- Bugs de rendimiento (si MEM-100 identifica bottlenecks).
- Bugs de seguridad (si MEM-101 identifica vulnerabilidades).
- Bugs de UAT (si MEM-102 reporta issues).
- Cada bug fix documentado en Development Log.

---

## 4. RESUMEN DE TAREAS

| VTT ID | Título | Rol | h | Cmplx | Pri |
|--------|--------|-----|--:|-------|:---:|
| MS-094 | Test Planning | QA | 4 | MEDIUM | M |
| MS-095 | Test Cases completos | QA | 8 | HIGH | M |
| MS-096 | Test Environment setup | DO | 4 | MEDIUM | M |
| MS-097 | Functional Testing | QA | 8 | HIGH | M |
| MS-098 | Integration Testing | QA | 6 | HIGH | M |
| MS-099 | E2E Testing | QA | 8 | HIGH | M |
| MS-100 | Performance Testing | QA | 6 | HIGH | **C** |
| MS-101 | Security Testing | AR | 4 | HIGH | **H** |
| MS-102 | UAT | PM | 4 | MEDIUM | M |
| MS-103 | Bug Fixes | BE | 8 | HIGH | M |
| **TOTAL** | | | **60h** | | |

---

## 5. CRITERIO CRÍTICO DE SALIDA

```
[ ] MEM-094 task_completed — Test Plan aprobado por TL
[ ] MEM-095 task_completed — Test Cases completos (11 endpoints + UI)
[ ] MEM-096 task_completed — Entorno test configurado + CI integrado
[ ] MEM-097 task_completed — Functional: 11 endpoints pasan todos los test cases
[ ] MEM-098 task_completed — Integration: BE↔BD↔Storage↔Redis OK
[ ] MEM-099 task_completed — E2E: flujos completos import→context + UI OK
[ ] MEM-100 task_completed — Performance: GET /context p95 <500ms VERIFICADO 🚨
[ ] MEM-101 task_completed — Security: SERVICE_KEY + OWASP básico OK
[ ] MEM-102 task_completed — UAT: PM sign-off formal
[ ] MEM-103 task_completed — Bug Fixes: 0 bugs críticos abiertos
[ ] MEM-104 desbloqueado en VTT (Fase Deploy arranca)
```

---

## 6. ESCALACIÓN

| Bloqueo | Escalar a |
|---------|-----------|
| Performance p95 >500ms en GET /context | TL + AR (revisar MEM-059) |
| Vulnerability de seguridad crítica | AR + PM |
| Bug bloqueante en endpoint crítico | TL + BE |
| PM rechaza UAT — feedback UI | DL + FE |

---

## 7. FIRMAS

| Rol | Nombre | Firma | Fecha |
|-----|--------|-------|-------|
| **PJM (emite)** | PJM Agent | ✅ EMITIDO | 2026-04-22 |
| **QA (recibe y lidera)** | QA Agent | ⬜ Pendiente acuse | — |
| **PM (UAT + sign-off)** | Martin Rivas | ⬜ Pendiente UAT | — |

---

## 8. REFERENCIAS

- `TASK_INDEX_SEED_MEMORY_SERVICE.md` v2.1 — §4.8 Testing tasks
- `HO_FASE_4_DEVELOPMENT_MEMORY_SERVICE.md` — Gate previo + descripción de endpoints
- `SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` — SLA <500ms, validaciones Zod, AMB-07
- `VTT_UUIDS_MEMORY_SERVICE.json` — UUIDs tareas MS-094..103

---

**Documento:** HO_FASE_5_TESTING_MEMORY_SERVICE.md  
**Versión:** 1.0  
**Estado:** ✅ EMITIDO — Pendiente sign-off QA y PM  
**Fecha:** 2026-04-22

---

**PJM — Memory Service**  
Virtual Teams Tracking
