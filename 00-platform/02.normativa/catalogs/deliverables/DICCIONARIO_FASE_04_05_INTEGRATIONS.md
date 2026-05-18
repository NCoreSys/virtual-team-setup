# DICCIONARIO DE DELIVERABLES — FASE 4.5: INTEGRATIONS

**Versión:** 1.0  
**Fecha:** 2026-05-14  
**Fase:** 4 — Development  
**Subfase:** 4.5 — Integrations  
**Total deliverables:** 9  
**Responsable de subfase:** Backend Developer  
**Aprueba:** Solution Architect

---

## Contexto de la subfase

Integrations implementa la conexión del sistema con servicios externos: payment gateways, email providers, auth providers, storage, analytics, y cualquier API de terceros. Las integraciones son los puntos más frágiles del sistema — donde nuestro código toca código ajeno con SLAs, rate limits, y formatos diferentes. Cada integración requiere error handling, retry logic, y fallback strategy.

**Prerequisitos de subfase:**
- Integration Points documentados (3B.1.6)
- Integration Flows diagramados (3B.5.5)
- Backend Services implementados (4.3.2)

**Entrega de subfase:**
- Todas las integraciones con servicios externos implementadas, testeadas, y con error handling robusto

---

### 4.5.1 Integration Code

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.5 Integrations |
| **Responsable** | Backend Developer |
| **Ejecuta** | Backend Developer |
| **Aprueba** | Solution Architect |
| **Formato** | TypeScript |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 3-5 días (por integración) |
| **Frecuencia** | Por integración |

**Perfil de ejecución:** Requiere leer y entender documentación de APIs de terceros, implementar auth (OAuth, API keys), y manejar responses/errors del servicio externo.  
En VTT: un agente puede generar scaffolding de integración (client, auth, error mapping) desde la documentación de la API externa. La lógica de mapping de datos y edge cases requiere developer. Necesita brief con: API docs del servicio, integration points doc, y data mapping.

**Qué es:** Código que implementa la conexión con cada servicio externo: HTTP client configurado, autenticación con el servicio (API key, OAuth, JWT), request formatting (transformar datos al formato del servicio), response parsing (transformar response al formato interno), y error mapping (traducir errores del servicio a errores internos).

**Para qué sirve:** Cada servicio externo tiene su propia API, su propio formato, y sus propias reglas. El integration code encapsula esa complejidad: el resto del backend llama `paymentService.charge(amount)` sin saber que detrás hay un POST a Stripe con headers específicos, idempotency keys, y webhook verification.

**Inputs requeridos:**
- `3B.1.6` Integration Points — spec de cada integración
- `3B.5.5` Integration Flows — sequence diagrams
- Documentación de la API del servicio externo
- Credenciales de sandbox/test environment

**Dependencias (predecessors):**
- `3B.1.6` Integration Points *(obligatorio)*
- `3B.5.5` Integration Flows *(obligatorio)*
- `4.3.2` Services *(obligatorio)* — services que orquestan integraciones

**Habilita (successors):**
- `4.5.6` Integration Tests — tests de integraciones
- `4.5.7` Integration Docs — documentación
- Funcionalidades que dependen de servicios externos

**Audiencia:**
- **Backend Developer** — implementación y mantenimiento
- **Solution Architect** — validación de approach
- **DevOps Lead** — credentials y networking

**Secciones esperadas:**
1. Client por servicio externo (src/integrations/stripe/, src/integrations/sendgrid/)
2. Auth configuration (API key, OAuth tokens)
3. Request builders (transform internal data → external format)
4. Response parsers (transform external response → internal format)
5. Error mappers (external error → internal AppError)
6. Configuration (URLs, timeouts, retry policies)

**Criterio de completitud:**
- [ ] Client implementado y funcional contra sandbox
- [ ] Auth configurada (credentials en secrets, no en código)
- [ ] Data mapping bidireccional (interno ↔ externo)
- [ ] Error mapping completo (cada error del servicio → error interno)
- [ ] Timeouts configurados
- [ ] Logging de requests/responses (sin credentials)
- [ ] Tests contra sandbox o mocks

**Anti-patrones:**
- ❌ **Credentials hardcoded:** API key en el código — va en secrets management.
- ❌ **Sin timeout:** Request que espera infinitamente si el servicio no responde.
- ❌ **Sin error mapping:** Error de Stripe raw en el response al usuario — confuso e inseguro.
- ❌ **Acoplamiento directo:** Service llama a Stripe directamente sin abstraction — imposible de mockear y cambiar de provider.
- ❌ **Sin logging:** Integración falla y no hay logs de qué request se envió — debugging imposible.

**Template:** `phases/04-development/deliverables/integrations/` *(pendiente)*

---

### 4.5.2 API Clients

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.5 Integrations |
| **Responsable** | Backend Developer |
| **Ejecuta** | Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | TypeScript |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Incluido en 4.5.1 |
| **Frecuencia** | Por servicio externo |

**Perfil de ejecución:** Requiere implementar HTTP clients tipados para cada servicio externo.  
En VTT: un agente puede generar API clients tipados desde la documentación del servicio. Es bastante delegable.

**Qué es:** HTTP clients tipados para cada API externa: instancia de Axios/fetch pre-configurada con base URL del servicio, auth headers, request/response interceptors, y types TypeScript para cada endpoint del servicio. Encapsulan la comunicación HTTP raw.

**Para qué sirve:** Separa la comunicación HTTP (cómo hablar con el servicio) de la lógica de integración (qué hacer con los datos). Permite cambiar de HTTP library sin tocar la lógica. Centraliza configuración (base URL, timeout, retries) por servicio.

**Inputs requeridos:**
- Documentación de API del servicio externo
- `3B.1.6` Integration Points — config por servicio

**Dependencias (predecessors):**
- `3B.1.6` Integration Points *(obligatorio)*

**Habilita (successors):**
- `4.5.1` Integration Code — clients usados por integration code

**Audiencia:**
- **Backend Developer** — uso en integraciones

**Secciones esperadas:**
1. Client class/module por servicio externo
2. Base URL y auth pre-configurados
3. Request/response types del servicio
4. Interceptors (logging, error transform)

**Criterio de completitud:**
- [ ] Client por servicio externo implementado
- [ ] Types para request/response del servicio
- [ ] Auth pre-configurada
- [ ] Timeout y retry configurados
- [ ] Logging de requests (sin credentials)

**Anti-patrones:**
- ❌ **fetch() raw:** Sin client, cada call construye URL y headers manualmente.
- ❌ **Sin types:** Response del servicio es `any` — no type safety.
- ❌ **Client genérico para todo:** Un client para Stripe, SendGrid, y S3 — configs muy diferentes.

**Template:** `phases/04-development/deliverables/api-clients/` *(pendiente)*

---

### 4.5.3 Webhooks

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.5 Integrations |
| **Responsable** | Backend Developer |
| **Ejecuta** | Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | TypeScript |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Por servicio con webhooks |

**Perfil de ejecución:** Requiere implementar webhook handlers: signature verification, idempotency, y async processing.  
En VTT: un agente puede generar webhook handlers con signature verification. Es bastante delegable.

**Qué es:** Endpoints que reciben callbacks/webhooks de servicios externos: Stripe payment events, SendGrid email delivery status, GitHub push events, etc. Cada webhook handler: verifica la firma/signature (autenticidad), parsea el payload, procesa el evento (idempotentemente), y retorna 200 rápido (procesamiento pesado va a un worker).

**Para qué sirve:** Muchos servicios externos comunican resultados via webhooks (push) en vez de que nuestro sistema pregunte (poll). Stripe notifica "el pago se confirmó" via webhook — si no lo procesamos, no sabemos que el pago se completó.

**Inputs requeridos:**
- `3B.5.5` Integration Flows — webhook flows diseñados
- Documentación de webhooks del servicio
- Webhook secret para signature verification

**Dependencias (predecessors):**
- `3B.5.5` Integration Flows *(obligatorio)*
- `4.3.1` API Endpoints *(obligatorio)* — endpoint de webhook

**Habilita (successors):**
- Procesamiento de eventos externos en tiempo real
- `4.5.6` Integration Tests — tests de webhooks

**Audiencia:**
- **Backend Developer** — implementación
- **DevOps Lead** — endpoint público, networking

**Secciones esperadas:**
1. Webhook endpoints (POST /webhooks/stripe, POST /webhooks/sendgrid)
2. Signature verification por servicio
3. Event type routing (switch por event type)
4. Idempotency (no procesar el mismo event 2 veces)
5. Async processing (enqueue → respond 200 → process in worker)
6. Logging de webhooks recibidos

**Criterio de completitud:**
- [ ] Endpoint por servicio con webhooks
- [ ] Signature verification implementada (rechazar webhooks no firmados)
- [ ] Idempotency key (event ID almacenado, skip si duplicado)
- [ ] Response 200 inmediata (procesamiento async)
- [ ] Event types principales manejados
- [ ] Logging de webhook receipt y processing result

**Anti-patrones:**
- ❌ **Sin signature verification:** Cualquiera puede enviar un POST fake — security hole.
- ❌ **Procesamiento síncrono lento:** Webhook que procesa 10 segundos → servicio reintenta → duplicados.
- ❌ **Sin idempotency:** Procesar el mismo webhook 2 veces → cobro duplicado o email duplicado.
- ❌ **Sin logging:** Webhook falla silenciosamente — no hay forma de saber qué pasó.

**Template:** `phases/04-development/deliverables/webhooks/` *(pendiente)*

---

### 4.5.4 OAuth Integrations

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.5 Integrations |
| **Responsable** | Backend Developer |
| **Ejecuta** | Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | TypeScript |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días por provider |
| **Frecuencia** | Por OAuth provider |

**Perfil de ejecución:** Requiere implementar OAuth 2.0 flows: authorization code, PKCE, token exchange.  
En VTT: un agente puede generar OAuth flow implementation. Es bastante delegable si el framework tiene soporte (Passport.js, NextAuth).

**Qué es:** Implementación de OAuth 2.0 para social login (Google, GitHub, Microsoft) y/o API authorization: redirect to provider, callback handler, token exchange, user info retrieval, account linking (crear o vincular cuenta interna), y token storage.

**Para qué sirve:** OAuth permite "Login con Google" y acceso a APIs que requieren autorización del usuario (Google Calendar, GitHub repos). Sin OAuth correcto, los tokens se pierden, el refresh falla, o el account linking crea duplicados.

**Inputs requeridos:**
- `3B.4.6` Authentication Spec — social login flows
- OAuth provider configuration (client ID, secret, scopes)
- `4.3.2` Services — user service para account create/link

**Dependencias (predecessors):**
- `3B.4.6` Authentication Spec *(obligatorio)*
- `4.3.2` Services *(obligatorio)* — user management

**Habilita (successors):**
- Social login funcional
- API integrations que requieren OAuth

**Audiencia:**
- **Backend Developer** — implementación
- **Frontend Developer** — botones de social login
- **Security Engineer** — validación de OAuth security

**Secciones esperadas:**
1. Provider configuration (client ID, secret, redirect URI, scopes)
2. Authorization redirect endpoint
3. Callback handler (token exchange, user info)
4. Account linking logic (create new or link existing)
5. Token storage (refresh tokens encrypted)
6. Error handling (denied, expired, invalid state)

**Criterio de completitud:**
- [ ] OAuth flow completo funcional por provider
- [ ] Account linking (nuevo usuario y usuario existente)
- [ ] Refresh token almacenado de forma segura
- [ ] Error handling (user denies, token expired)
- [ ] CSRF protection (state parameter)
- [ ] Tests del flow

**Anti-patrones:**
- ❌ **Sin state parameter:** CSRF vulnerable — siempre validar state.
- ❌ **Refresh token en plain text:** Debe estar encriptado en la BD.
- ❌ **Sin account linking:** Login con Google crea cuenta nueva aunque el email ya existe — duplicados.
- ❌ **Scopes excesivos:** Pedir acceso a todo cuando solo se necesita email — usuarios no confían.

**Template:** `phases/04-development/deliverables/oauth/` *(pendiente)*

---

### 4.5.5 Third-party SDKs

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.5 Integrations |
| **Responsable** | Backend Developer |
| **Ejecuta** | Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | Config |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5-1 día por SDK |
| **Frecuencia** | Por servicio |

**Perfil de ejecución:** Requiere instalar, configurar, y wrappear SDKs de terceros.  
En VTT: un agente puede generar SDK configuration y wrappers. Es bastante delegable.

**Qué es:** SDKs oficiales de servicios de terceros instalados y configurados: Stripe SDK, AWS SDK, Firebase Admin, SendGrid SDK, Sentry SDK, etc. Cada SDK: instalado como dependencia, configurado con credentials del .env, y wrapeado en un service interno (para no acoplar el código directamente al SDK).

**Para qué sirve:** Los SDKs oficiales son preferibles a HTTP raw porque: manejan auth automáticamente, tienen types incluidos, manejan retries y errors, y se actualizan con cambios de la API. Wrapearlos en un service interno permite cambiar de provider sin refactorizar todo el codebase.

**Inputs requeridos:**
- `3B.1.5` Technology Stack — SDKs necesarios
- `3B.1.6` Integration Points — servicios con SDK disponible
- Credenciales de cada servicio

**Dependencias (predecessors):**
- `3B.1.6` Integration Points *(obligatorio)*
- `4.1.3` Environment Variables *(obligatorio)* — credentials

**Habilita (successors):**
- `4.5.1` Integration Code — integration usa SDKs

**Audiencia:**
- **Backend Developer** — configuración y uso

**Secciones esperadas:**
1. SDK instalados (tabla: servicio, SDK, versión)
2. Configuration por SDK (initialized con env vars)
3. Service wrapper por SDK (StripeService wraps Stripe SDK)
4. Types exportados del SDK

**Criterio de completitud:**
- [ ] SDKs instalados y en dependencies (no devDependencies)
- [ ] Configuración vía env vars (no hardcoded)
- [ ] Wrapeados en service interno
- [ ] Versión fija en package.json (no `^` para SDKs de terceros)

**Anti-patrones:**
- ❌ **SDK sin wrapper:** `import Stripe from 'stripe'` en 15 archivos — acoplado, imposible de mockear.
- ❌ **SDK con `^latest`:** Actualización automática que rompe la integración.
- ❌ **Credentials en constructor:** `new Stripe('sk_test_abc')` — va en env var.

**Template:** `phases/04-development/deliverables/third-party-sdks/` *(pendiente)*

---

### 4.5.6 Integration Tests

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.5 Integrations |
| **Responsable** | Backend Developer |
| **Ejecuta** | Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | Jest |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Por integración |

**Perfil de ejecución:** Requiere testing con mocks de servicios externos (no contra producción).  
En VTT: un agente puede generar integration tests con mocks. Es bastante delegable.

**Qué es:** Tests que verifican que las integraciones funcionan correctamente: tests contra sandbox del servicio (si disponible) o contra mocks que simulan las responses del servicio. Cubren: happy path (pago exitoso), error paths (pago rechazado, timeout), y webhook processing.

**Para qué sirve:** Las integraciones son frágiles — el servicio externo puede cambiar su API, sus errors, o su behavior. Los tests detectan breaking changes temprano y verifican que el error handling funciona.

**Inputs requeridos:**
- `4.5.1` Integration Code — código a testear
- Sandbox credentials del servicio (si disponible)
- Mock responses del servicio

**Dependencias (predecessors):**
- `4.5.1` Integration Code *(obligatorio)*

**Habilita (successors):**
- Confianza en integraciones pre-deploy
- CI/CD gate

**Audiencia:**
- **Backend Developer** — escribe y mantiene
- **QA Engineer** — referencia de coverage

**Secciones esperadas:**
1. Tests contra sandbox (si disponible)
2. Tests con mocks (responses simuladas)
3. Tests de error handling (timeout, 500, rate limit)
4. Tests de webhook processing
5. Tests de retry logic

**Criterio de completitud:**
- [ ] Happy path testeado por integración
- [ ] Error paths testeados (timeout, server error, rate limit)
- [ ] Webhook processing testeado
- [ ] Retry logic testeada
- [ ] Tests no dependen de servicio externo real en CI (usar mocks)

**Anti-patrones:**
- ❌ **Tests contra producción:** Crear cargos reales en Stripe durante tests — usar sandbox o mocks.
- ❌ **Solo happy path:** Testear pago exitoso pero no pago rechazado.
- ❌ **Tests que dependen de connectivity:** CI falla porque el sandbox de Stripe está caído — usar mocks para CI.

**Template:** `phases/04-development/deliverables/integration-tests/` *(pendiente)*

---

### 4.5.7 Integration Docs

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.5 Integrations |
| **Responsable** | Backend Developer |
| **Ejecuta** | Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | MD |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día por integración |
| **Frecuencia** | Por integración |

**Perfil de ejecución:** Requiere documentar cómo funciona cada integración para futuros maintainers.  
En VTT: un agente puede generar documentación de integraciones. Es altamente delegable.

**Qué es:** Documentación por integración: qué servicio, para qué se usa, cómo está configurado, qué endpoints/webhooks se usan, cómo obtener credentials, cómo testear localmente (sandbox), y troubleshooting de problemas comunes. Es la guía para el developer que mantendrá esta integración en el futuro.

**Para qué sirve:** Las integraciones son las partes más difíciles de debuggear — el error puede estar en nuestro código, en el servicio, o en la red. La documentación reduce el tiempo de troubleshooting de horas a minutos.

**Inputs requeridos:**
- `4.5.1` Integration Code — implementación a documentar
- `3B.1.6` Integration Points — spec original

**Dependencias (predecessors):**
- `4.5.1` Integration Code *(obligatorio)*

**Habilita (successors):**
- Onboarding de developers nuevos
- Troubleshooting rápido

**Audiencia:**
- **Backend Developer** — mantenimiento
- **DevOps Lead** — credentials y networking
- **New developers** — onboarding

**Secciones esperadas:**
1. Overview por integración (servicio, propósito, endpoints usados)
2. Setup guide (cómo obtener credentials, configurar sandbox)
3. Cómo testear localmente
4. Webhook setup (URL, eventos suscritos)
5. Error handling y troubleshooting
6. Monitoring y alertas

**Criterio de completitud:**
- [ ] Documentación por integración
- [ ] Setup reproducible
- [ ] Troubleshooting de problemas comunes
- [ ] Probado por developer que no la implementó

**Anti-patrones:**
- ❌ **Sin docs de integración:** "Pregúntale a quien lo hizo" — esa persona se fue de la empresa.
- ❌ **Docs desactualizadas:** Documentación que referencia endpoints viejos del servicio.

**Template:** `phases/04-development/deliverables/integration-docs/` *(pendiente)*

---

### 4.5.8 Error Handling

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.5 Integrations |
| **Responsable** | Backend Developer |
| **Ejecuta** | Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | TypeScript |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Incluido en 4.5.1 |
| **Frecuencia** | Por integración |

**Perfil de ejecución:** Requiere manejar errors específicos de cada servicio externo y traducirlos a errores internos.  
En VTT: un agente puede generar error mapping por servicio. Es bastante delegable.

**Qué es:** Error handling específico para integraciones: mapear errores del servicio externo (Stripe: card_declined, insufficient_funds, rate_limit) a errores internos (PaymentDeclinedError, RateLimitError), implementar circuit breaker (si el servicio falla N veces consecutivas, dejar de intentar temporalmente), y fallback behavior (si el servicio de email falla, enqueue para retry).

**Para qué sirve:** Los errores de servicios externos son diferentes a los errores internos: tienen formatos diferentes, códigos diferentes, y requieren handling diferente (retry vs fail vs fallback). Sin error handling de integración, un error de Stripe se propaga como un 500 genérico — el usuario no sabe que su tarjeta fue rechazada.

**Inputs requeridos:**
- `4.5.1` Integration Code — errores a manejar
- Documentación de errores del servicio externo
- `3B.2.6` Error Handling Strategy — circuit breaker, fallback

**Dependencias (predecessors):**
- `4.5.1` Integration Code *(obligatorio)*
- `3B.2.6` Error Handling Strategy *(obligatorio)*

**Habilita (successors):**
- UX de errores de integración (mensajes claros al usuario)
- Resiliencia del sistema

**Audiencia:**
- **Backend Developer** — implementación
- **Frontend Developer** — error messages para UI

**Secciones esperadas:**
1. Error mapping por servicio (external error → internal error)
2. Circuit breaker configuration (threshold, timeout, half-open)
3. Fallback behavior por integración
4. User-facing error messages (no mensajes técnicos del servicio)
5. Logging de errores de integración (con request context)

**Criterio de completitud:**
- [ ] Error mapping completo por servicio
- [ ] Circuit breaker implementado para servicios críticos
- [ ] Fallback definido (qué pasa si el servicio está caído)
- [ ] Messages user-friendly (no "stripe_error_123")
- [ ] Logging con contexto (qué se envió, qué se recibió)

**Anti-patrones:**
- ❌ **Error raw del servicio al usuario:** "card_declined" de Stripe directo — el usuario no entiende.
- ❌ **Sin circuit breaker:** Servicio caído → 1000 requests fallidos → cascada de errores.
- ❌ **Catch genérico:** `catch(e) { throw new Error("Integration failed") }` — pierde el contexto del error.

**Template:** `phases/04-development/deliverables/integration-error-handling/` *(pendiente)*

---

### 4.5.9 Retry Logic

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.5 Integrations |
| **Responsable** | Backend Developer |
| **Ejecuta** | Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | TypeScript |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5-1 día |
| **Frecuencia** | Una vez (reutilizable) |

**Perfil de ejecución:** Requiere implementar retry con backoff exponencial y jitter.  
En VTT: un agente puede generar retry logic reutilizable. Es altamente delegable.

**Qué es:** Lógica de reintentos para llamadas a servicios externos que fallan por errores transientes (timeout, 503, rate limit): retry con exponential backoff (esperar 1s, 2s, 4s, 8s entre reintentos), jitter (variación aleatoria para evitar thundering herd), max retries configurables, y clasificación de errores retryable vs non-retryable (timeout sí, 400 no).

**Para qué sirve:** El 90% de los errores de red son transientes — un retry los resuelve. Sin retry, un timeout de 100ms se convierte en un error para el usuario. Con retry (3 intentos, backoff exponencial), el sistema se recupera automáticamente de la mayoría de errores de red.

**Inputs requeridos:**
- `3B.2.6` Error Handling Strategy — retry policy
- `4.5.1` Integration Code — integraciones que necesitan retry

**Dependencias (predecessors):**
- `3B.2.6` Error Handling Strategy *(obligatorio)*

**Habilita (successors):**
- Resiliencia de integraciones
- Reducción de errores transientes

**Audiencia:**
- **Backend Developer** — uso en integraciones

**Secciones esperadas:**
1. Retry utility function (genérica, reutilizable)
2. Exponential backoff implementation (baseDelay × 2^attempt)
3. Jitter (random variance to avoid thundering herd)
4. Retryable error classification (timeout, 503, 429 → retry; 400, 404 → don't retry)
5. Max retries configuration (default: 3)
6. Logging of retry attempts

**Criterio de completitud:**
- [ ] Retry utility reutilizable implementada
- [ ] Exponential backoff con jitter
- [ ] Clasificación de errores retryable vs non-retryable
- [ ] Max retries configurable
- [ ] Logging de cada retry attempt
- [ ] Tests de retry logic

**Anti-patrones:**
- ❌ **Retry sin backoff:** Reintentar inmediatamente N veces — DDos al servicio externo.
- ❌ **Retry de errores no-transientes:** Reintentar un 400 Bad Request — siempre va a fallar.
- ❌ **Sin max retries:** Loop infinito de retries — request timeout, resource leak.
- ❌ **Sin jitter:** Todos los clientes reintentan al mismo tiempo — thundering herd.
- ❌ **Sin logging:** No saber que hubo retries — oculta problemas de conectividad.

**Template:** `phases/04-development/deliverables/retry-logic/` *(pendiente)*

---

## Tabla resumen de ejecutores — Fase 4.5 Integrations

| Deliverable | Responsable | Ejecuta | Delegable VTT |
|-------------|-------------|---------|---------------|
| 4.5.1 Integration Code | Backend Developer | Backend Developer | 🔶 Parcial — scaffolding sí, data mapping complejo no |
| 4.5.2 API Clients | Backend Developer | Backend Developer | ✅ — puede generar typed clients desde API docs |
| 4.5.3 Webhooks | Backend Developer | Backend Developer | ✅ — puede generar handlers con signature verification |
| 4.5.4 OAuth Integrations | Backend Developer | Backend Developer | ✅ — puede generar OAuth flows con frameworks |
| 4.5.5 Third-party SDKs | Backend Developer | Backend Developer | ✅ — puede configurar y wrapear SDKs |
| 4.5.6 Integration Tests | Backend Developer | Backend Developer | ✅ — puede generar tests con mocks |
| 4.5.7 Integration Docs | Backend Developer | Backend Developer | ✅ — puede generar documentación completa |
| 4.5.8 Error Handling | Backend Developer | Backend Developer | ✅ — puede generar error mapping y circuit breaker |
| 4.5.9 Retry Logic | Backend Developer | Backend Developer | ✅ — puede generar retry utility reutilizable |

---

## Siguiente archivo

**Próximo:** `DICCIONARIO_FASE_04_06_UNIT_TESTS.md` — 7 deliverables (4.6.1 a 4.6.7)
