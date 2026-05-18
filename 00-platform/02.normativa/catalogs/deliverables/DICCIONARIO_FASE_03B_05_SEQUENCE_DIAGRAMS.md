# DICCIONARIO DE DELIVERABLES — FASE 3B.5: SEQUENCE DIAGRAMS

**Versión:** 1.0  
**Fecha:** 2026-05-14  
**Fase:** 3B — Design Technical  
**Subfase:** 3B.5 — Sequence Diagrams  
**Total deliverables:** 6  
**Responsable de subfase:** Solution Architect  
**Aprueba:** Tech Lead

---

## Contexto de la subfase

Los Sequence Diagrams muestran cómo los componentes del sistema interactúan en el tiempo para resolver un flujo específico. Mientras los diagramas C4 muestran estructura estática, los sequence diagrams muestran comportamiento dinámico: "cuando el usuario hace login, ¿qué llama a qué, en qué orden, y qué datos fluyen?". Son la traducción de los use cases a interacciones técnicas entre componentes.

**Prerequisitos de subfase:**
- Solution Architecture (3B.1) — componentes y contenedores definidos
- API Design (3B.4) — endpoints definidos
- Use Cases detallados (2.3.4) — flujos a diagramar

**Entrega de subfase:**
- Flujos principales, de autenticación, de error, de integración, y asíncronos documentados como sequence diagrams

---

### 3B.5.1 Sequence Diagrams Doc

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.5 Sequence Diagrams |
| **Responsable** | Solution Architect |
| **Ejecuta** | Solution Architect |
| **Aprueba** | Tech Lead |
| **Formato** | MD/PDF |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere capacidad de curar y organizar los diagramas de secuencia en un documento navegable con contexto para cada diagrama.  
En VTT: un agente puede generar el documento contenedor que organiza y contextualiza todos los sequence diagrams. Es altamente delegable. Necesita brief con: lista de diagramas a incluir, orden lógico, y contexto narrativo para cada uno.

**Qué es:** Documento contenedor que agrupa todos los sequence diagrams del proyecto con índice, contexto narrativo para cada diagrama, y convenciones utilizadas. No es un diagrama en sí, sino el documento que organiza todos los diagramas de las subfases 3B.5.2-3B.5.6.

**Para qué sirve:** Proporciona un punto de entrada único para consultar cualquier flujo del sistema. Sin este documento, los diagramas viven dispersos en archivos separados sin contexto. El documento agrega narrativa: "este flujo se activa cuando X, los participantes son Y, y el resultado esperado es Z".

**Inputs requeridos:**
- `3B.5.2` a `3B.5.6` — todos los sequence diagrams individuales
- `3B.1.3` Container Diagram — participantes de los diagramas
- `3B.1.4` Component Diagram — componentes que participan

**Dependencias (predecessors):**
- `3B.5.2` Auth Flow *(obligatorio)*
- `3B.5.3` Main Business Flows *(obligatorio)*
- `3B.5.4` Error Flows *(obligatorio)*
- `3B.5.5` Integration Flows *(obligatorio)*
- `3B.5.6` Async Flows *(obligatorio)*

**Habilita (successors):**
- `4.3.1` Backend Modules — developers consultan flujos al implementar
- `5.3.1` API Tests — flujos como base de test scenarios

**Audiencia:**
- **Todo el equipo técnico** — referencia de flujos
- **New team members** — onboarding técnico

**Secciones esperadas:**
1. Índice de diagramas (tabla: nombre, categoría, flujo, participantes)
2. Convenciones de diagramación (Mermaid syntax, colores, notas)
3. Auth Flow (3B.5.2) con contexto
4. Main Business Flows (3B.5.3) con contexto
5. Error Flows (3B.5.4) con contexto
6. Integration Flows (3B.5.5) con contexto
7. Async Flows (3B.5.6) con contexto
8. Cross-reference a use cases (qué use case implementa cada flujo)

**Criterio de completitud:**
- [ ] Todos los sequence diagrams incluidos y contextualizados
- [ ] Índice navegable
- [ ] Convenciones documentadas
- [ ] Cross-reference a use cases
- [ ] Documento navegable sin conocimiento previo

**Anti-patrones:**
- ❌ **Solo diagramas sin contexto:** Secuencias sin explicación de cuándo se activan y qué resultado producen.
- ❌ **Diagramas dispersos:** Cada diagrama en un archivo diferente sin índice central — imposible saber qué existe.
- ❌ **Sin convenciones:** Cada diagrama usa diferente notación y estilo — inconsistencia visual.

**Template:** `phases/03B-design-technical/deliverables/sequence-diagrams-doc.md` *(pendiente)*

---

### 3B.5.2 Auth Flow

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.5 Sequence Diagrams |
| **Responsable** | Solution Architect |
| **Ejecuta** | Solution Architect / Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | Mermaid |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere entendimiento de auth flows (login, token refresh, logout, password reset, social login) y cómo se implementan a nivel de componentes.  
En VTT: un agente puede generar los sequence diagrams de auth en Mermaid a partir de la Authentication Spec. Es altamente delegable. Necesita brief con: auth spec completa, participantes (browser, API, auth provider, DB), y variantes de flujo (login normal, social, MFA).

**Qué es:** Sequence diagram(s) que muestran los flujos completos de autenticación: login (credentials → token), token refresh (refresh token → new access token), logout (token revocation), password reset, y social login (si aplica). Muestra los participantes (Browser/App, API, Auth Provider, Database) y cada request/response con datos.

**Para qué sirve:** La autenticación es el flujo más complejo y más critical-path. Un error en la implementación = usuarios no pueden entrar. El sequence diagram asegura que frontend y backend implementan el mismo flujo exactamente. También es referencia para Security Engineer al auditar vulnerabilidades.

**Inputs requeridos:**
- `3B.4.6` Authentication Spec — flujos definidos
- `3B.1.3` Container Diagram — participantes
- `3B.1.6` Integration Points — auth providers externos

**Dependencias (predecessors):**
- `3B.4.6` Authentication Spec *(obligatorio)* — flujos a diagramar
- `3B.1.3` Container Diagram *(obligatorio)* — participantes

**Habilita (successors):**
- `3B.5.1` Sequence Diagrams Doc — incluido en el documento
- `4.3.4` Authentication Implementation — implementación directa
- `5.3.2` Auth Tests — test scenarios basados en el flujo

**Audiencia:**
- **Frontend Developer** — implementación del auth flow en el cliente
- **Backend Developer** — implementación del auth en el servidor
- **Security Engineer** — auditoría de seguridad del flujo

**Secciones esperadas:**
1. Login flow (credentials → validate → generate tokens → response)
2. Token refresh flow (refresh token → validate → new access token)
3. Logout flow (revoke → blacklist → cleanup)
4. Password reset flow (request → email → validate link → new password)
5. Social login flow (si aplica: redirect → callback → create/link account)
6. MFA flow (si aplica: first factor → challenge → second factor)
7. Error cases por flujo (invalid credentials, expired token, rate limited)

**Criterio de completitud:**
- [ ] Login, refresh, y logout diagramados
- [ ] Password reset diagramado
- [ ] Participantes correctos (alineados a Container Diagram)
- [ ] Request/response data indicados en cada flecha
- [ ] Error cases incluidos (alt/opt blocks)
- [ ] Consistente con Authentication Spec

**Anti-patrones:**
- ❌ **Solo happy path:** Login exitoso sin mostrar qué pasa con credenciales inválidas — el developer no implementa el error handling.
- ❌ **Participantes incorrectos:** El browser habla directo con la DB — saltarse capas que sí existen.
- ❌ **Sin datos en flechas:** Flechas que dicen "request" y "response" sin indicar qué datos viajan — no es útil.
- ❌ **Auth desconectado del spec:** El diagram muestra un flujo diferente al Authentication Spec — contradicción.

**Template:** `phases/03B-design-technical/deliverables/auth-flow.mmd` *(pendiente)*

---

### 3B.5.3 Main Business Flows

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.5 Sequence Diagrams |
| **Responsable** | Solution Architect |
| **Ejecuta** | Solution Architect / Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | Diagramas (Mermaid) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 2-3 días |
| **Frecuencia** | Una vez + nuevos diagramas por feature |

**Perfil de ejecución:** Requiere capacidad de traducir use cases de negocio en interacciones técnicas entre componentes. Debe entender el mapping entre funcionalidad de usuario y operaciones de backend.  
En VTT: un agente puede generar sequence diagrams de los flujos principales en Mermaid a partir de los use cases, API endpoints, y component diagram. Es bastante delegable. Necesita brief con: use cases a diagramar, endpoints involucrados, componentes del backend que participan, y business rules que afectan el flujo.

**Qué es:** Conjunto de sequence diagrams para los 3-7 flujos de negocio principales del sistema. Cada flujo muestra la interacción completa desde la acción del usuario hasta la respuesta, pasando por todos los componentes: UI → API Controller → Service → Repository → Database, incluyendo validaciones, business rules, y transformaciones.

**Para qué sirve:** Son el "blueprint" de la implementación. Un developer que debe implementar "crear una orden" lee este diagrama y sabe: qué controller recibe el request, qué service procesa la lógica, qué validaciones aplican, qué se guarda en qué tabla, y qué response retornar. Reduce las decisiones ad-hoc durante la codificación.

**Inputs requeridos:**
- `2.3.4` Detailed Use Cases — flujos a diagramar
- `3B.1.4` Component Diagram — componentes participantes
- `3B.4.2` Endpoints List — API calls en el flujo
- `2.5.1` Business Rules Document — reglas que aparecen en el flujo
- `3B.3.1` ERD Complete — tablas/entidades afectadas

**Dependencias (predecessors):**
- `2.3.4` Detailed Use Cases *(obligatorio)* — flujos fuente
- `3B.1.4` Component Diagram *(obligatorio)* — participantes
- `3B.4.2` Endpoints List *(obligatorio)* — API calls
- `2.5.1` Business Rules Document *(recomendado)* — validaciones en el flujo

**Habilita (successors):**
- `3B.5.1` Sequence Diagrams Doc — incluidos en el documento
- `4.3.1` Backend Modules — implementación basada en los flujos
- `5.1.1` Test Strategy — test scenarios derivados de flujos
- `5.3.1` API Tests — flujos como escenarios de test end-to-end

**Audiencia:**
- **Backend Developer** — blueprint de implementación
- **Frontend Developer** — entiende el flujo completo detrás de cada acción
- **QA Engineer** — test scenarios end-to-end
- **Tech Lead** — revisión de diseño

**Secciones esperadas:**
1. Lista de flujos diagramados (tabla: nombre, use case ref, complejidad)
2. Por cada flujo principal:
   - Contexto y trigger (qué acción del usuario inicia el flujo)
   - Sequence diagram en Mermaid
   - Participantes con su rol (Controller, Service, Repository, External)
   - Datos en cada interacción (request/response payloads simplificados)
   - Business rules aplicadas (notes en el diagrama)
   - Alternative paths (alt/opt blocks para variaciones)

**Criterio de completitud:**
- [ ] Los 3-5 flujos de negocio más importantes diagramados
- [ ] Cada diagrama tiene participantes alineados al Component Diagram
- [ ] Datos indicados en cada flecha (no solo "request"/"response")
- [ ] Business rules aparecen como notes o conditions
- [ ] Alternative paths incluidos (al menos 1 por flujo)
- [ ] Cross-reference a use case y endpoint

**Anti-patrones:**
- ❌ **Diagramas demasiado detallados:** Cada getter, setter, y log statement — nivel de código, no de diseño.
- ❌ **Diagramas sin alternative paths:** Solo el happy path — no documenta qué pasa cuando una validación falla.
- ❌ **Participantes genéricos:** "Backend" como un solo participante cuando hay Controller, Service, Repository — pierde el valor del diagrama.
- ❌ **Flujos triviales diagramados:** CRUD básico sin business rules no necesita sequence diagram — es overhead.

**Template:** `phases/03B-design-technical/deliverables/main-business-flows.mmd` *(pendiente)*

---

### 3B.5.4 Error Flows

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.5 Sequence Diagrams |
| **Responsable** | Solution Architect |
| **Ejecuta** | Solution Architect / Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | Diagramas (Mermaid) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere mentalidad defensiva: pensar en qué puede fallar en cada punto del flujo y cómo el sistema se recupera o degrada gracefully.  
En VTT: un agente puede generar error flow diagrams basándose en la Error Handling Strategy y los Main Business Flows. Puede identificar puntos de fallo en cada flujo y diagramar el comportamiento de error. Es bastante delegable. Necesita brief con: error handling strategy, puntos de fallo identificados, y comportamiento deseado (retry, fallback, graceful degradation).

**Qué es:** Sequence diagrams que muestran cómo el sistema maneja errores: qué pasa cuando una validación falla, cuando la BD no está disponible, cuando un servicio externo no responde, o cuando ocurre un error inesperado. Muestra el flujo desde el error hasta la respuesta al usuario, incluyendo logging, alerting, y recovery.

**Para qué sirve:** El happy path se implementa naturalmente. Los errores, no. Sin error flows explícitos, cada developer inventa su propio manejo de errores. Los diagramas de error aseguran que el sistema falla de forma consistente, informativa, y recuperable.

**Inputs requeridos:**
- `3B.2.6` Error Handling Strategy — clasificación y manejo de errores
- `3B.5.3` Main Business Flows — flujos donde insertar error handling
- `3B.4.5` Error Codes — responses de error estándar
- `3B.1.6` Integration Points — puntos de fallo externos

**Dependencias (predecessors):**
- `3B.2.6` Error Handling Strategy *(obligatorio)*
- `3B.5.3` Main Business Flows *(obligatorio)* — flujos base
- `3B.4.5` Error Codes *(recomendado)*

**Habilita (successors):**
- `3B.5.1` Sequence Diagrams Doc — incluidos
- `4.3.7` Middleware — error handling middleware
- `5.4.1` Error Handling Tests — scenarios de test

**Audiencia:**
- **Backend Developer** — implementación de error handling
- **Frontend Developer** — manejo de error responses
- **QA Engineer** — negative test scenarios
- **DevOps Lead** — alerting basado en errores

**Secciones esperadas:**
1. Validation error flow (input inválido → error response)
2. Business rule violation flow (operación no permitida → error response)
3. Database unavailable flow (DB down → retry → fallback → error response)
4. External service failure flow (timeout → retry → circuit breaker → fallback)
5. Unexpected error flow (unhandled exception → global handler → log → generic error response)
6. Rate limit exceeded flow (429 → retry-after header → client backoff)

**Criterio de completitud:**
- [ ] Al menos 4 tipos de error diagramados
- [ ] Logging y alerting incluidos en el flujo
- [ ] Retry logic diagramada donde aplica
- [ ] Error response final al usuario documentada
- [ ] Consistente con Error Handling Strategy

**Anti-patrones:**
- ❌ **Solo "return 500":** Error flow que termina en un 500 genérico sin logging ni contexto — imposible diagnosticar.
- ❌ **Sin retry para transientes:** Timeout del external service = error fatal, sin intentar retry.
- ❌ **Error flows que exponen internals:** El error response al usuario incluye stack trace o nombres de tablas.
- ❌ **No diagramar error flows:** "Los errores se manejan en el catch" — no es un diseño, es improvisación.

**Template:** `phases/03B-design-technical/deliverables/error-flows.mmd` *(pendiente)*

---

### 3B.5.5 Integration Flows

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.5 Sequence Diagrams |
| **Responsable** | Solution Architect |
| **Ejecuta** | Solution Architect / Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | Diagramas (Mermaid) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Una vez + nuevo diagrama por integración nueva |

**Perfil de ejecución:** Requiere conocimiento de los APIs/SDKs de los servicios externos y cómo se integran en la arquitectura del sistema.  
En VTT: un agente puede generar sequence diagrams de integración a partir de la documentación de Integration Points y la documentación de la API del servicio externo. Es bastante delegable. Necesita brief con: docs de la API del servicio externo, integration points doc, y componentes del sistema que participan.

**Qué es:** Sequence diagrams que muestran las interacciones del sistema con cada servicio externo: payment gateway (Stripe), email service (SendGrid), auth provider (Auth0), storage (S3), analytics (Segment), etc. Muestra el flujo completo: desde la acción interna que dispara la integración, pasando por la llamada al servicio, procesamiento de la respuesta, y manejo de errores/webhooks.

**Para qué sirve:** Las integraciones son las "fronteras" del sistema — donde nuestro código toca código ajeno. Son los puntos más propensos a errores (timeouts, cambios de API, rate limits). Diagramar cada integración previene implementaciones ad-hoc y asegura que se manejan todos los edge cases (especialmente webhooks entrantes y retries).

**Inputs requeridos:**
- `3B.1.6` Integration Points — integraciones documentadas
- `3B.1.3` Container Diagram — participantes
- Documentación de APIs de terceros
- `3B.5.4` Error Flows — error handling en integraciones

**Dependencias (predecessors):**
- `3B.1.6` Integration Points *(obligatorio)* — integraciones a diagramar
- `3B.1.3` Container Diagram *(obligatorio)* — participantes

**Habilita (successors):**
- `3B.5.1` Sequence Diagrams Doc — incluidos
- `4.3.6` Third Party Integrations — implementación directa
- `5.6.1` Integration Tests — test scenarios

**Audiencia:**
- **Backend Developer** — implementación de cada integración
- **DevOps Lead** — networking, secrets, y monitoring de integraciones
- **QA Engineer** — test scenarios con mocks de integraciones

**Secciones esperadas:**
1. Por cada integración externa:
   - Trigger (qué acción interna dispara la integración)
   - Flujo outbound (llamada al servicio externo)
   - Procesamiento de response
   - Webhook/callback handling (si aplica)
   - Error handling y retry
   - Data mapping (nuestro formato → formato del servicio)
2. Resumen de integraciones y sus patterns (sync, async, webhook)

**Criterio de completitud:**
- [ ] Cada integración del Integration Points document tiene un sequence diagram
- [ ] Flujo outbound y webhook/callback diagramados
- [ ] Error handling incluido (timeout, error response, retry)
- [ ] Data mapping indicado
- [ ] Consistente con Integration Points document

**Anti-patrones:**
- ❌ **Integración como caja negra:** Flecha que dice "call Stripe" sin mostrar qué endpoint, qué datos, ni qué manejar en la response.
- ❌ **Sin webhook flows:** Diagramar la llamada saliente pero no el webhook entrante — el developer no sabe cómo procesar callbacks.
- ❌ **Sin retry/error:** Asumir que la integración siempre funciona — el primer timeout rompe el flujo.

**Template:** `phases/03B-design-technical/deliverables/integration-flows.mmd` *(pendiente)*

---

### 3B.5.6 Async Flows

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.5 Sequence Diagrams |
| **Responsable** | Solution Architect |
| **Ejecuta** | Solution Architect / Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | Diagramas (Mermaid) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez + nuevos diagramas por worker nuevo |

**Perfil de ejecución:** Requiere entendimiento de procesamiento asíncrono: message queues (RabbitMQ, SQS, Redis), event-driven architecture, background workers, cron jobs, y eventual consistency.  
En VTT: un agente puede generar sequence diagrams de flujos asíncronos en Mermaid. Es altamente delegable. Necesita brief con: lista de procesos async (email sending, report generation, data sync), message queue/tool elegido, y failure handling (DLQ, retry).

**Qué es:** Sequence diagrams que muestran flujos de procesamiento asíncrono: tareas que no se ejecutan en el request/response cycle sino en background. Incluye: envío de emails, generación de reportes, procesamiento de archivos, sincronización de datos, scheduled jobs/cron, y event-driven workflows. Muestra: productor → queue → consumer → resultado.

**Para qué sirve:** Los flujos asíncronos son "invisibles" — no hay un request/response directo. Sin diagramas, nadie sabe: "¿quién produce el mensaje?", "¿qué consumer lo procesa?", "¿qué pasa si el consumer falla?", "¿hay dead-letter queue?". Los diagramas hacen visible lo invisible y aseguran que se diseña el error handling asíncrono.

**Inputs requeridos:**
- `3B.1.3` Container Diagram — queues, workers como contenedores
- `3B.1.7` Data Flow Diagram — flujos async identificados
- `3B.1.5` Technology Stack — herramienta de queue/messaging
- `3B.2.6` Error Handling Strategy — manejo de errores en async

**Dependencias (predecessors):**
- `3B.1.3` Container Diagram *(obligatorio)* — workers y queues
- `3B.1.7` Data Flow Diagram *(recomendado)* — flujos async
- `3B.1.5` Technology Stack *(obligatorio)* — herramienta de messaging

**Habilita (successors):**
- `3B.5.1` Sequence Diagrams Doc — incluidos
- `4.3.5` Background Jobs — implementación de workers
- `5.5.1` Async Tests — test scenarios
- `3B.8.11` Monitoring Strategy — monitoring de queues y workers

**Audiencia:**
- **Backend Developer** — implementación de producers y consumers
- **DevOps Lead** — deployment y monitoring de workers
- **Tech Lead** — validación de diseño async
- **QA Engineer** — testing de flujos async (más complejo que sync)

**Secciones esperadas:**
1. Por cada flujo asíncrono:
   - Trigger (qué evento produce el mensaje)
   - Producer (qué componente envía a la queue)
   - Message format (payload del mensaje)
   - Queue/Topic (nombre, tipo: FIFO, standard)
   - Consumer (qué worker procesa el mensaje)
   - Processing logic (qué hace el consumer)
   - Result (side effects: email enviado, report generado, dato actualizado)
   - Error handling (retry, DLQ, alerting)
2. Scheduled jobs / Cron (tabla: nombre, schedule, qué hace)
3. Dead-letter queue strategy
4. Idempotency considerations (mensajes duplicados)

**Criterio de completitud:**
- [ ] Todos los flujos async del sistema diagramados
- [ ] Producer, queue, y consumer identificados por flujo
- [ ] Message format documentado
- [ ] Error handling y DLQ incluidos
- [ ] Scheduled jobs/cron documentados
- [ ] Idempotency considerada (qué pasa si el mensaje se procesa 2 veces)

**Anti-patrones:**
- ❌ **Async sin error handling:** "Ponemos el email en la queue y ya" — ¿qué pasa si el email falla?
- ❌ **Sin dead-letter queue:** Mensajes que fallan se pierden silenciosamente — datos perdidos sin alerting.
- ❌ **Sin idempotency:** Procesamiento duplicado de un mensaje crea registros duplicados — data corruption.
- ❌ **Scheduled jobs no documentados:** Cron jobs "que alguien puso" sin documentación — nadie sabe qué hacen ni cuándo corren.

**Template:** `phases/03B-design-technical/deliverables/async-flows.mmd` *(pendiente)*

---

## Tabla resumen de ejecutores — Fase 3B.5 Sequence Diagrams

| Deliverable | Responsable | Ejecuta | Delegable VTT |
|-------------|-------------|---------|---------------|
| 3B.5.1 Sequence Diagrams Doc | Solution Architect | Solution Architect | ✅ — puede organizar y contextualizar todos los diagramas |
| 3B.5.2 Auth Flow | Solution Architect | Solution Architect / Backend Developer | ✅ — puede generar diagrams de auth en Mermaid desde Auth Spec |
| 3B.5.3 Main Business Flows | Solution Architect | Solution Architect / Backend Developer | 🔶 Parcial — puede generar diagramas pero traducir use cases a interacciones técnicas requiere juicio |
| 3B.5.4 Error Flows | Solution Architect | Solution Architect / Backend Developer | 🔶 Parcial — puede generar diagrams pero identificar failure modes requiere experiencia |
| 3B.5.5 Integration Flows | Solution Architect | Solution Architect / Backend Developer | ✅ — puede generar diagramas desde Integration Points y docs de API |
| 3B.5.6 Async Flows | Solution Architect | Solution Architect / Backend Developer | ✅ — puede generar diagramas de flujos async en Mermaid |

---

## Siguiente archivo

**Próximo:** `DICCIONARIO_FASE_03B_06_ADR.md` — 4 deliverables (3B.6.1 a 3B.6.4)
