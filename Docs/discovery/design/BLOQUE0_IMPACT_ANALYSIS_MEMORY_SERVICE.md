# Análisis de Impacto — Specs Bloque 0 VTT en Memory Service

**Documento:** BLOQUE0_IMPACT_ANALYSIS_MEMORY_SERVICE.md  
**Versión:** 1.0  
**Fecha:** 2026-05-06  
**Autor:** SA Reviewer  
**Estado:** APROBADO — requiere acción antes de iniciar implementación

---

## Resumen Ejecutivo

Memory Service es la **primera feature de VTT**. Como tal, debe implementar desde cero los 4 estándares de plataforma definidos en el Bloque 0, que **no estaban incorporados** en los entregables del Analysis ni del Design Technical ya generados.

Este documento identifica el impacto en cada entregable del SDLC y define exactamente qué se requiere antes de que el equipo de desarrollo pueda comenzar la implementación.

| Spec Bloque 0 | Horas estimadas | Estado de incorporación |
|---------------|-----------------|------------------------|
| Seguridad Base | ~14h | ❌ No incorporada |
| Logs y Observabilidad | ~8h | ❌ No incorporada |
| Manejo de Errores | ~12h | ❌ No incorporada |
| Multitenant / RBAC | ~29h | ❌ No incorporada |
| **TOTAL** | **~63h** | |

---

## 1. SPEC_SEGURIDAD_BASE_v1.1

### Qué agrega al Memory Service

| Componente | Descripción |
|------------|-------------|
| `helmet()` | Headers HTTP de seguridad en Express |
| `apiLimiter` | Rate limiting 100 req/15min global |
| `authLimiter` | Rate limiting 5 req/15min en endpoints de auth |
| `validateBody / validateQuery / validateParams` | Middleware Zod para validación de entrada |
| `EncryptionService` | AES-256-GCM para datos sensibles en reposo |
| `env validation` | Zod schema para variables de entorno (JWT_SECRET ≥32 chars, ENCRYPTION_KEY 64 hex, ANTHROPIC_API_KEY starts 'sk-ant-') |
| `CORS` | Configuración por entorno (dev vs prod) |

### Impacto en Analysis

| Deliverable | Impacto | Acción requerida |
|-------------|---------|-----------------|
| **MS-018 — Functional Requirements** | RF nuevos: validación de inputs, rate limiting, encryption | Addendum: RF-SEC-001..RF-SEC-005 |
| **MS-019 — Non-Functional Requirements** | NFR nuevos: seguridad, rate limiting, encryption en reposo | Addendum: NFR-SEC-001..NFR-SEC-003 |
| **MS-022 — Business Rules** | Reglas nuevas: qué datos se encriptan, límites por entorno | Addendum: BR-SEC-001..BR-SEC-002 |
| **MS-024 — Acceptance Criteria** | AC específicos para validaciones Zod, rate limit, headers | Addendum por pantalla de Upload |
| **MS-025 — Traceability Matrix** | Nuevos RF/NFR deben trazarse hasta componentes | Addendum a la matriz |

### Impacto en Design Technical

| Deliverable | Impacto | Acción requerida |
|-------------|---------|-----------------|
| **MS-039 — Architecture Document** | Helmet, rate limiting y CORS son componentes middleware de la API | Incorporar capa middleware en arquitectura |
| **MS-042 — API Design** | Todos los endpoints deben documentar rate limits y headers de seguridad | Addendum con response headers, 429 responses |
| **MS-045 — Security Plan** | Este es el documento central donde vive la spec de seguridad base | Redactar completo basado en SPEC_SEGURIDAD_BASE |
| **MS-043 — Sequence Diagrams** | Agregar paso de middleware de seguridad en flujo de upload | Addendum diagrama |

### Impacto en Design UX/UI

| Deliverable | Impacto | Descripción |
|-------------|---------|-------------|
| **MS-029..035 — Wireframes** | Rate limit → la UI debe mostrar error 429 al usuario | Agregar estado de error por rate limit en Upload y Dashboard |

---

## 2. SPEC_LOGS_OBSERVABILIDAD_v1.1

### Qué agrega al Memory Service

| Componente | Descripción |
|------------|-------------|
| `Winston logger` | Dev: colorized console; Prod: JSON estructurado |
| `correlationId middleware` | Header `X-Correlation-ID` generado o reenviado por cada request |
| `X-Trace-ID` | Para requests originados desde Runtime/Bridge — habilita tracing E2E |
| `requestLoggerMiddleware` | Log automático de entrada/salida con duración |
| `createRequestLogger(RuntimeContext)` | Logger contextualizado con taskId, runtimeRunId, agentId |
| `loggedExternalCall` | Wrapper para llamadas a servicios externos con log de latencia |
| `sanitizeForLogging` | Redacción de password/token/secret/apiKey/authorization/cookie |

### Impacto en Analysis

| Deliverable | Impacto | Acción requerida |
|-------------|---------|-----------------|
| **MS-018 — Functional Requirements** | RF nuevos: correlationId en responses, trazabilidad de requests | Addendum: RF-LOG-001..RF-LOG-003 |
| **MS-019 — Non-Functional Requirements** | NFR nuevos: logging estructurado, correlationId, sanitización | Addendum: NFR-LOG-001..NFR-LOG-002 |
| **MS-022 — Business Rules** | BR nuevo: qué campos se sanitizan antes de loggear | Addendum: BR-LOG-001 |
| **MS-025 — Traceability Matrix** | RF-LOG trazados hasta componentes logging | Addendum a la matriz |

### Impacto en Design Technical

| Deliverable | Impacto | Acción requerida |
|-------------|---------|-----------------|
| **MS-039 — Architecture Document** | Logger y correlationId son componentes transversales de la API | Incorporar en arquitectura como cross-cutting concerns |
| **MS-041 — DB Design** | No aplica directamente (logging es en archivo/stdout) | Ninguna |
| **MS-042 — API Design** | Todos los responses deben incluir `X-Correlation-ID` header | Addendum: response headers estándar |
| **MS-043 — Sequence Diagrams** | Agregar correlationId en headers de todos los flujos | Addendum |
| **MS-044 — Observability / Monitoring** (si existe) | Este es el documento central para logs | Redactar |

### Impacto en Integraciones

**Crítico para Memory Service:** El Runtime v1.1 y el MCP Bridge son los principales consumidores de `GET /context`. Cuando ellos llaman al Memory Service deben incluir `X-Trace-ID`, y el Memory Service debe usarlo para correlacionar en sus logs. Esto afecta:
- MS-039 §Integraciones
- MS-042 §Headers de Request
- MS-046 §Integration Testing

---

## 3. SPEC_MANEJO_ERRORES_v1.1

### Qué agrega al Memory Service

| Componente | Descripción |
|------------|-------------|
| `ErrorCategory` | 8 categorías: VALIDATION/AUTH/AUTHZ/DOMAIN/RESOURCE/EXTERNAL/INFRA/INTERNAL |
| `AppError` | Clase con `isOperational` flag — separa errores esperados de bugs |
| `ERROR_CODES` | Catálogo de códigos únicos por categoría |
| `errorHandler middleware` | Global — diferencia operacional vs no-operacional, 500 vs error estructurado |
| `mapExternalError` | Prisma P2002/P2025/P2003, ZodError, JWT, timeout/connection |
| `withRetry` | 3 intentos, exponential backoff + jitter |
| `CircuitBreaker` | CLOSED/OPEN/HALF_OPEN — failureThreshold:5, resetTimeout:30s |

### Impacto en Analysis

| Deliverable | Impacto | Acción requerida |
|-------------|---------|-----------------|
| **MS-018 — Functional Requirements** | RF nuevos: respuestas de error estructuradas, circuit breaker | Addendum: RF-ERR-001..RF-ERR-004 |
| **MS-019 — Non-Functional Requirements** | NFR existente de disponibilidad 99.5% + circuit breaker + retry | Addendum: NFR-ERR-001..NFR-ERR-002 |
| **MS-022 — Business Rules** | BR nuevos: cuándo reintentar, qué errores son recuperables | Addendum: BR-ERR-001..BR-ERR-003 |
| **MS-024 — Acceptance Criteria** | AC: formato de error estructurado por endpoint, 503 cuando circuit open | Addendum por módulo |
| **MS-025 — Traceability Matrix** | RF-ERR trazados hasta componentes | Addendum |

### Impacto en Design Technical

| Deliverable | Impacto | Acción requerida |
|-------------|---------|-----------------|
| **MS-039 — Architecture Document** | errorHandler, CircuitBreaker, withRetry son componentes del API | Incorporar en architecture document |
| **MS-041 — DB Design** | Prisma errors (P2002, P2025, P2003) mapeados por mapExternalError | Documentar error codes esperados por entidad |
| **MS-042 — API Design** | Todos los endpoints deben documentar: responses 400/401/403/404/409/429/500/503, formato AppError | Addendum completo de error responses |
| **MS-043 — Sequence Diagrams** | Agregar flujos de retry y circuit breaker en secuencias de Upload y Query | Addendum diagramas |

### Impacto en Design UX/UI

| Deliverable | Impacto | Descripción |
|-------------|---------|-------------|
| **MS-029..035 — Wireframes** | Circuit breaker abierto → 503 Service Unavailable en la UI | Agregar estado "Sistema no disponible" en Dashboard y Health Status |
| **MS-035 — Health Status wireframe** | CircuitBreaker status (CLOSED/OPEN/HALF_OPEN) debería ser visible | Agregar indicadores de CircuitBreaker por servicio externo |

---

## 4. SPEC_MULTITENANT_RBAC_v1.3

### Qué agrega al Memory Service

| Componente | Descripción |
|------------|-------------|
| `authenticate middleware` | Valida JWT → genera `req.auth` (userId, tokenType, isHuman, isAgent) |
| `resolveAuthorizationContext` | Navega hasta org/workspace → genera `req.authz` |
| `requireCapability (RBAC)` | Evalúa capabilities por rol efectivo |
| `requirePolicy (ABAC)` | 9 policies basadas en contexto del recurso |
| `permissions.service` | RBAC con org privilege + workspace membership |
| `policy.service` | canReadWorkspaceResource, canUpdateTask, canTransitionTask, canApproveTask, canSubmitChangeRequest, canApproveSignature, canManageUsers, canExecuteImport, canConfigureApprovalFlow |
| `audit-decision.service` | Log de decisiones sensibles |
| `OrganizationMember` | Entidad formal con ownerId como fuente de verdad |
| `WorkspaceMember` | Membresía por workspace con roleId |

### Impacto en Analysis

| Deliverable | Impacto | Acción requerida |
|-------------|---------|-----------------|
| **MS-018 — Functional Requirements** | RF críticos nuevos: autenticación, autorización por workspace/org, upload solo para miembros, query respeta RBAC | Addendum: RF-RBAC-001..RF-RBAC-008 |
| **MS-019 — Non-Functional Requirements** | NFR nuevos: tiempo de resolución de contexto de autorización <50ms | Addendum: NFR-RBAC-001 |
| **MS-020 — Use Cases** | Todos los UC deben incluir actor con rol específico | Revisar UC-001..UCN y agregar precondición de autenticación |
| **MS-021 — User Stories** | US deben especificar roles: "Como workspace_member puedo...", "Como org_admin puedo..." | Addendum/revisión US-001..USN |
| **MS-022 — Business Rules** | BR nuevos: quién puede subir (workspace member), quién puede ver (workspace member), quién puede admin (org_admin/owner) | Addendum: BR-RBAC-001..BR-RBAC-005 |
| **MS-024 — Acceptance Criteria** | AC: 401 sin token, 403 sin capability, 404 si recurso no existe (no 403) | Addendum por módulo |
| **MS-025 — Traceability Matrix** | RF-RBAC trazados hasta middleware chain | Addendum |

### Impacto en Design Technical

| Deliverable | Impacto | Acción requerida |
|-------------|---------|-----------------|
| **MS-039 — Architecture Document** | Middleware chain completa: authenticate → resolveAuthzContext → requireCapability → requirePolicy | Reescribir sección middleware en arquitectura |
| **MS-041 — DB Design** | Agregar entidades: `User`, `Organization`, `OrganizationMember`, `Workspace`, `WorkspaceMember`, `Role`, `RoleCapability`, `Capability` | Addendum al DB Design — entidades de autorización |
| **MS-042 — API Design** | Todos los endpoints necesitan: header `Authorization: Bearer`, response 401/403 documentados, capabilities requeridas por endpoint | Reescribir sección de seguridad de cada endpoint |
| **MS-043 — Sequence Diagrams** | Agregar middleware chain en todos los flujos de ingesta y query | Addendum diagramas |
| **MS-045 — Security Plan** | RBAC y ABAC son el núcleo del security plan | Ampliar con sección de autorización |

### Impacto en Design UX/UI — CRÍTICO

| Deliverable | Impacto | Descripción |
|-------------|---------|-------------|
| **MS-027 — IA (Information Architecture)** | La IA debe estructurarse por workspace — cada usuario ve solo su contexto | Revisar jerarquía: Organization → Workspace → datos |
| **MS-028 — Design System** | Agregar componentes: RoleTag, PermissionGate, AuthGuard | Addendum al Component Library |
| **MS-029 — Dashboard wireframe** | Mostrar solo datos del workspace del usuario autenticado | Revisar |
| **MS-030 — Conversations List wireframe** | Filtrar por workspace membership | Revisar |
| **MS-031 — Conversation Viewer wireframe** | Acceso restringido por membership | Revisar |
| **MS-032 — Agent Timeline wireframe** | Restringido al workspace del usuario | Revisar |
| **MS-033 — Project Cost Report wireframe** | Solo visible para org_admin/owner o miembros del workspace | Revisar |
| **MS-034 — Agent Cost Report wireframe** | Ídem | Revisar |
| **MS-035 — Manual Upload wireframe** | Solo workspace_member puede subir (RF-RBAC) | Agregar estado 403/401 |
| **MS-036 — Health Status wireframe** | ¿Es visible para todos o solo org_admin? Definir | Decisión pendiente |
| **MS-026 — Personas** | Las personas deben representar roles RBAC: workspace_member, org_admin, org_owner | Revisar/extender personas |

---

## 5. Resumen Consolidado por Deliverable

### Analysis — Deliverables con Addendum requerido

| Deliverable | Addendums |
|-------------|-----------|
| **MS-018 FR** | RF-SEC (5), RF-LOG (3), RF-ERR (4), RF-RBAC (8) = **20 RF nuevos** |
| **MS-019 NFR** | NFR-SEC (3), NFR-LOG (2), NFR-ERR (2), NFR-RBAC (1) = **8 NFR nuevos** |
| **MS-020 Use Cases** | Revisar todos — agregar precondición de autenticación y roles |
| **MS-021 User Stories** | Revisar todas — especificar rol del actor en cada US |
| **MS-022 Business Rules** | BR-SEC (2), BR-LOG (1), BR-ERR (3), BR-RBAC (5) = **11 BR nuevos** |
| **MS-024 AC** | Addendum por módulo: errores 401/403/404/429/503 en todos los endpoints |
| **MS-025 Traceability** | Extender matriz con todas las nuevas RF/NFR → componentes |

### Design Technical — Deliverables con Addendum requerido

| Deliverable | Acción |
|-------------|--------|
| **MS-039 Architecture** | Agregar: middleware chain, cross-cutting concerns (logger, correlation), CircuitBreaker, RBAC entities |
| **MS-041 DB Design** | Agregar entidades de autorización: User, Organization, OrganizationMember, Workspace, WorkspaceMember, Role, RoleCapability, Capability |
| **MS-042 API Design** | Reescribir sección seguridad: auth headers, rate limit, error responses (400/401/403/404/429/503), capabilities por endpoint |
| **MS-043 Sequence Diagrams** | Agregar flujos: middleware chain, retry, circuit breaker |
| **MS-045 Security Plan** | Documento central — redactar completo con las 4 specs |

### Design UX/UI — Deliverables afectados

| Deliverable | Acción |
|-------------|--------|
| **MS-026 Personas** | Extender para incluir roles RBAC como eje de las personas |
| **MS-027 IA** | Revisar jerarquía para reflejar Organization → Workspace → datos |
| **MS-028 Design System** | Addendum: RoleTag, PermissionGate, estados de error 401/403 |
| **MS-029..035 Wireframes** | Revisar cada pantalla para RBAC + estados de error de seguridad |
| **MS-036 Health Status** | Definir política de visibilidad (todos vs org_admin) y añadir CircuitBreaker status |

---

## 6. Nuevas Tareas Requeridas

Las siguientes tareas DEBEN crearse y completarse **antes de iniciar el Development**:

### Addendums de Analysis (Fase 2 — Completar antes de Fase 4)

| Task ID sugerido | Título | Rol | Horas est. | Urgencia |
|-----------------|--------|-----|-----------|---------|
| MS-141 | Addendum FR — Bloque 0 (20 RF nuevos) | SA | 3h | 🔴 Crítico |
| MS-142 | Addendum NFR — Bloque 0 (8 NFR nuevos) | SA | 2h | 🔴 Crítico |
| MS-143 | Addendum Business Rules — Bloque 0 | SA | 2h | 🔴 Crítico |
| MS-144 | Addendum User Stories — RBAC roles | SA | 3h | 🔴 Crítico |
| MS-145 | Addendum Use Cases — autenticación/autorización | SA | 2h | 🟡 Alto |
| MS-146 | Addendum Acceptance Criteria — errores de seguridad | SA | 3h | 🟡 Alto |
| MS-147 | Actualizar Traceability Matrix — Bloque 0 | SA | 2h | 🟡 Alto |

### Addendums de Design Technical (Fase 3B — Completar durante o antes de Development)

| Task ID sugerido | Título | Rol | Horas est. | Urgencia |
|-----------------|--------|-----|-----------|---------|
| MS-148 | Addendum Architecture — middleware chain + RBAC entities | AR | 4h | 🔴 Crítico |
| MS-149 | Addendum DB Design — entidades de autorización (7 tablas) | DB | 4h | 🔴 Crítico |
| MS-150 | Addendum API Design — security headers, error responses, capabilities | BE/AR | 6h | 🔴 Crítico |
| MS-151 | Addendum Sequence Diagrams — middleware, retry, circuit breaker | AR | 3h | 🟡 Alto |
| MS-152 | Redactar Security Plan completo — MS-045 | AR/SA | 6h | 🔴 Crítico |

### Addendums de Design UX/UI (Fase 3A — Completar antes de Development)

| Task ID sugerido | Título | Rol | Horas est. | Urgencia |
|-----------------|--------|-----|-----------|---------|
| MS-153 | Addendum Personas — roles RBAC | UX | 2h | 🟡 Alto |
| MS-154 | Addendum IA — jerarquía Organization/Workspace | DL | 2h | 🟡 Alto |
| MS-155 | Addendum Design System — RoleTag, PermissionGate, estados error | DL | 2h | 🟡 Alto |
| MS-156 | Addendum Wireframes — RBAC + estados de error seguridad (8 pantallas) | DL | 4h | 🟡 Alto |

---

## 7. Decisiones Pendientes

Las siguientes decisiones deben tomarse **antes de iniciar los addendums**:

| # | Pregunta | Quien decide | Urgencia |
|---|----------|-------------|---------|
| 1 | ¿Memory Service usa su propio modelo de Org/Workspace/User, o comparte con VTT core? | PM + SA | 🔴 Crítico |
| 2 | ¿La UI del Memory Service requiere login propio (JWT) o usa token de servicio? | PM + AR | 🔴 Crítico |
| 3 | ¿Health Status es visible para todos los workspace members o solo para org_admin? | PM + DL | 🟡 Alto |
| 4 | ¿El CircuitBreaker status debe aparecer en la UI? Si sí, en qué pantalla | AR + DL | 🟡 Alto |
| 5 | ¿Las fuentes de ingesta (Claude CLI, ChatGPT, etc.) se autentican con service token o JWT? | AR + BE | 🔴 Crítico |

---

## 8. Estimación de Esfuerzo Total

| Categoría | Horas |
|-----------|-------|
| Addendums Analysis | 17h |
| Addendums Design Technical | 23h |
| Addendums Design UX/UI | 10h |
| Implementación Bloque 0 en Dev | 63h |
| **TOTAL adicional** | **113h** |

---

## 9. Recomendación SA

**No iniciar el Development (Fase 4) hasta que:**

1. Las 5 decisiones pendientes estén resueltas
2. Los addendums críticos de Analysis estén completos (MS-141, MS-142, MS-143, MS-144)
3. Los addendums críticos de Design Technical estén completos (MS-148, MS-149, MS-150, MS-152)

Los addendums no críticos (MS-145..147, MS-151, MS-153..156) pueden completarse en paralelo con el inicio del Development, pero deben estar terminados antes de que el equipo llegue al módulo que impactan.

**El AR (MS-039) puede continuar**, pero debe incorporar los cambios de middleware chain y RBAC entities de inmediato. Es preferible que el AR lea este documento antes de comenzar a redactar MS-039.

---

*Generado por: SA Reviewer — 2026-05-06*  
*Basado en: SPEC_SEGURIDAD_BASE_v1.1, SPEC_LOGS_OBSERVABILIDAD_v1.1, SPEC_MANEJO_ERRORES_v1.1, SPEC_MULTITENANT_RBAC_v1.3*
