# DICCIONARIO DE DELIVERABLES — FASE 4.3: BACKEND DEVELOPMENT

**Versión:** 1.0  
**Fecha:** 2026-05-14  
**Fase:** 4 — Development  
**Subfase:** 4.3 — Backend Development  
**Total deliverables:** 15  
**Responsable de subfase:** Backend Developer  
**Aprueba:** Tech Lead

---

## Contexto de la subfase

Backend Development es el corazón de la implementación: APIs, servicios de negocio, modelos de datos, workers asíncronos, middlewares, y toda la lógica del lado del servidor. Es donde los requisitos funcionales, business rules, y diseño técnico se convierten en código ejecutable. Cada deliverable de esta subfase es un artefacto de código con tests, documentación, y error handling incluidos.

**Prerequisitos de subfase:**
- Environment Setup (4.1) — ambiente listo para codificar
- Database Implementation (4.2) — schema y models listos
- API Design (3B.4) — contratos de API definidos
- Design Patterns (3B.2.3) — patrones a seguir

**Entrega de subfase:**
- Backend completo: APIs implementadas, lógica de negocio, tests, y documentación

---

### 4.3.1 API Endpoints

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.3 Backend Development |
| **Responsable** | Backend Developer |
| **Ejecuta** | Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | TypeScript |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 5-10 días (continuo por sprint) |
| **Frecuencia** | Por sprint |

**Perfil de ejecución:** Requiere dominio del framework backend (NestJS, Express, Fastify), routing, request validation, y response formatting.  
En VTT: un agente puede generar scaffolding de endpoints (route, controller, validation schema) desde el OpenAPI spec. Puede generar CRUD completo. La lógica de negocio compleja requiere developer humano. Necesita brief con: OpenAPI spec, schemas de request/response, y business rules por endpoint.

**Qué es:** Implementación de todos los endpoints REST definidos en el OpenAPI spec (3B.4.1): routes, controllers, request validation (con Zod/class-validator), response serialization, y HTTP status codes correctos. Cada endpoint conecta request → validation → service → response.

**Para qué sirve:** Los endpoints son la interfaz del backend con el mundo exterior — el frontend, los integradores, y los clientes los consumen. Un endpoint bien implementado valida inputs, delega a services, maneja errores, y retorna responses consistentes según el contrato.

**Inputs requeridos:**
- `3B.4.1` OpenAPI Spec — contrato a implementar
- `3B.4.2` Endpoints List — lista de endpoints
- `3B.4.3` Request/Response Examples — examples de referencia
- `3B.4.5` Error Codes — error responses estándar
- `3B.2.3` Design Patterns — patterns de controller/route

**Dependencias (predecessors):**
- `3B.4.1` OpenAPI Spec *(obligatorio)* — contrato
- `4.2.1` Initial Migration *(obligatorio)* — BD lista
- `4.3.2` Services *(co-dependencia)* — controllers delegan a services
- `4.3.5` DTOs/Schemas *(co-dependencia)* — validation schemas

**Habilita (successors):**
- `4.4.6` API Client — frontend consume endpoints
- `4.3.9` Unit Tests BE — tests de controllers
- `4.3.10` Integration Tests — tests end-to-end de API
- `4.3.11` API Documentation — Swagger generado desde código
- `5.3.1` API Tests — QA tests de API

**Audiencia:**
- **Frontend Developer** — consume los endpoints
- **QA Engineer** — testea los endpoints
- **Tech Lead** — code review de implementación

**Secciones esperadas:**
1. Routes por resource (archivos `src/routes/` o `src/controllers/`)
2. Request validation schemas (Zod/class-validator por endpoint)
3. Response serialization (DTOs de response)
4. Error handling por endpoint (validation errors, not found, business errors)
5. Middleware aplicado (auth, rate limit, logging)

**Criterio de completitud:**
- [ ] Todos los endpoints del OpenAPI spec implementados
- [ ] Request validation funcional (invalid input → 400 con detalles)
- [ ] Response format consistente con el spec
- [ ] HTTP status codes correctos por caso (200, 201, 400, 401, 403, 404, 422, 500)
- [ ] Error handling estándar (error codes del catálogo)
- [ ] Cada endpoint tiene al menos 1 unit test
- [ ] Swagger/OpenAPI auto-generado desde decorators/annotations
- [ ] Code review aprobado

**Anti-patrones:**
- ❌ **Fat controllers:** Toda la lógica en el controller — debe delegar a services.
- ❌ **Sin validation:** Aceptar cualquier input y fallar en el service/DB — errores crípticos.
- ❌ **Inconsistencia de responses:** Un endpoint retorna `{ data: [...] }` y otro `{ results: [...] }` — sin estándar.
- ❌ **Catch genérico:** `catch(e) { res.status(500).send("Error") }` — pierde contexto del error.
- ❌ **Endpoint sin test:** "Funciona en Postman" no es un test — los tests automatizados previenen regresiones.

**Template:** `phases/04-development/deliverables/api-endpoints/` *(pendiente)*

---

### 4.3.2 Services

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.3 Backend Development |
| **Responsable** | Backend Developer |
| **Ejecuta** | Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | TypeScript |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 5-10 días (continuo por sprint) |
| **Frecuencia** | Por sprint |

**Perfil de ejecución:** Requiere entendimiento profundo de las business rules y capacidad de traducirlas a lógica de código limpio y testeable.  
En VTT: un agente puede generar scaffolding de services (interfaces, métodos CRUD base, dependency injection). La lógica de negocio compleja requiere developer humano. Necesita brief con: business rules por entidad, validation rules, y design patterns.

**Qué es:** Capa de servicios de negocio que contiene toda la lógica del dominio: validaciones de negocio, cálculos, orquestación de operaciones, y coordinación entre repositories. Los services son el "cerebro" del backend — los controllers solo rutean, los services deciden. Cada service encapsula la lógica de un bounded context o módulo.

**Para qué sirve:** Separa la lógica de negocio de la capa HTTP (controllers) y de la capa de datos (repositories). Esto permite: testear la lógica de negocio sin HTTP, reusar lógica entre endpoints diferentes, y cambiar la capa de datos sin tocar la lógica.

**Inputs requeridos:**
- `2.5.1` Business Rules Document — reglas a implementar
- `2.5.3` Validation Rules — validaciones de negocio
- `2.5.4` Calculation Rules — cálculos
- `3B.2.3` Design Patterns — Service Layer pattern
- `4.3.4` Repositories — acceso a datos

**Dependencias (predecessors):**
- `2.5.1` Business Rules Document *(obligatorio)* — lógica a implementar
- `4.3.4` Repositories *(co-dependencia)* — services usan repositories
- `4.3.3` Models *(obligatorio)* — entidades del dominio

**Habilita (successors):**
- `4.3.1` API Endpoints — controllers delegan a services
- `4.3.6` Workers — workers reusan services
- `4.3.9` Unit Tests BE — tests de lógica de negocio

**Audiencia:**
- **Backend Developer** — implementación y mantenimiento
- **Tech Lead** — code review de lógica de negocio

**Secciones esperadas:**
1. Service por módulo/entidad (archivos `src/services/`)
2. Interfaces de service (para dependency injection y testing)
3. Métodos de negocio (create, update, delete + custom operations)
4. Validaciones de negocio (reglas que no son solo formato)
5. Orquestación (operaciones que involucran múltiples repositories)
6. Error throwing (custom exceptions de negocio)

**Criterio de completitud:**
- [ ] Todas las business rules del documento implementadas
- [ ] Cada service tiene interface (para mocking en tests)
- [ ] Dependency injection configurada (no `new Repository()` directo)
- [ ] Custom exceptions para errores de negocio
- [ ] Cada método de service tiene unit test
- [ ] Sin acceso directo a DB (solo vía repositories)
- [ ] Code review aprobado

**Anti-patrones:**
- ❌ **Anemic services:** Services que solo pasan datos del controller al repository sin lógica — no justifican la capa.
- ❌ **God service:** Un service con 30 métodos y 2000 líneas — descomponer por responsabilidad.
- ❌ **Service accede a DB directo:** `prisma.user.findMany()` en el service — viola Repository pattern.
- ❌ **Sin dependency injection:** `new UserRepository()` hardcoded — imposible de mockear en tests.
- ❌ **Business rules en controller:** Validaciones de negocio en el controller — no reutilizable, no testeable aisladamente.

**Template:** `phases/04-development/deliverables/services/` *(pendiente)*

---

### 4.3.3 Models

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.3 Backend Development |
| **Responsable** | Backend Developer |
| **Ejecuta** | Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | Prisma / TypeScript |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Una vez + por migration |

**Perfil de ejecución:** Requiere dominio del ORM elegido (Prisma, TypeORM, Sequelize).  
En VTT: un agente puede generar models/entities completos desde el schema definition. Es altamente delegable. Necesita brief con: schema de BD y ORM elegido.

**Qué es:** Definición de modelos de datos en la capa de aplicación: entidades del ORM (Prisma schema, TypeORM entities, Sequelize models) que mapean tablas de BD a objetos TypeScript. Incluyen: campos, tipos, relaciones, validaciones de modelo, y hooks/callbacks (beforeCreate, afterUpdate).

**Para qué sirve:** Los models son el puente entre la BD y el código de aplicación. En lugar de escribir SQL raw, el developer trabaja con objetos tipados: `user.orders` en vez de `SELECT * FROM orders WHERE user_id = ?`. El ORM genera queries optimizadas y previene SQL injection.

**Inputs requeridos:**
- `3B.3.2` Schema Definition — schema a mapear
- `3B.3.1` ERD Complete — relaciones entre entidades
- `3B.1.5` Technology Stack — ORM elegido

**Dependencias (predecessors):**
- `4.2.1` Initial Migration *(obligatorio)* — schema en BD
- `3B.3.2` Schema Definition *(obligatorio)* — base del modelo

**Habilita (successors):**
- `4.3.4` Repositories — repositories usan models
- `4.3.2` Services — services trabajan con models
- `4.3.5` DTOs/Schemas — DTOs derivados de models

**Audiencia:**
- **Backend Developer** — interacción con BD vía models
- **Database Engineer** — validación de mapping correcto

**Secciones esperadas:**
1. Schema file (Prisma) o Entity files (TypeORM) en `src/models/` o `prisma/schema.prisma`
2. Relaciones definidas (hasMany, belongsTo, manyToMany)
3. Validaciones a nivel de modelo (si el ORM las soporta)
4. Hooks/callbacks (timestamps automáticos, soft delete)
5. Types generados (Prisma Client types)

**Criterio de completitud:**
- [ ] Todas las tablas del ERD mapeadas a models
- [ ] Relaciones correctas (1:1, 1:N, N:M)
- [ ] Types TypeScript generados y usables
- [ ] Soft delete configurado donde aplique
- [ ] Timestamps automáticos (created_at, updated_at)
- [ ] Validado contra el schema de BD (sin discrepancias)

**Anti-patrones:**
- ❌ **Models desincronizados con BD:** El model dice `email: string` pero la BD tiene `email: varchar(100) NOT NULL UNIQUE` — discrepancia.
- ❌ **Relaciones faltantes:** La BD tiene FK pero el model no define la relación — queries ineficientes con JOINs manuales.
- ❌ **Sin types generados:** Usar `any` en vez de los types del ORM — pierde type safety.

**Template:** `phases/04-development/deliverables/models/` *(pendiente)*

---

### 4.3.4 Repositories

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.3 Backend Development |
| **Responsable** | Backend Developer |
| **Ejecuta** | Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | TypeScript |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 2-3 días |
| **Frecuencia** | Por sprint |

**Perfil de ejecución:** Requiere implementación del Repository pattern: encapsular acceso a datos con interface tipada.  
En VTT: un agente puede generar repositories CRUD completos con interface. Es altamente delegable. Necesita brief con: models, queries frecuentes, y filtering/pagination patterns.

**Qué es:** Capa de acceso a datos que encapsula todas las queries a la BD: CRUD operations, queries custom (findByEmail, findActiveOrders), filtering, sorting, pagination, y transactions. Cada repository tiene una interface (para mocking) y una implementación (que usa el ORM).

**Para qué sirve:** Separa el "cómo se acceden los datos" del "qué se hace con los datos" (services). Permite cambiar de ORM o de BD sin tocar la lógica de negocio. Facilita testing: los tests de services mockean el repository interface en vez de necesitar una BD real.

**Inputs requeridos:**
- `4.3.3` Models — entidades a acceder
- `3B.2.3` Design Patterns — Repository pattern
- `3B.4.4` Pagination Strategy — implementación de paginación
- `3B.3.4` Index Strategy — queries optimizadas

**Dependencias (predecessors):**
- `4.3.3` Models *(obligatorio)* — entidades del ORM
- `3B.2.3` Design Patterns *(obligatorio)* — pattern a seguir

**Habilita (successors):**
- `4.3.2` Services — services consumen repositories
- `4.3.9` Unit Tests BE — repositories mockeables

**Audiencia:**
- **Backend Developer** — acceso a datos
- **Tech Lead** — code review de queries

**Secciones esperadas:**
1. Interface por repository (`IUserRepository`)
2. Implementación por repository (`UserRepository implements IUserRepository`)
3. Métodos CRUD base (findById, findAll, create, update, delete)
4. Métodos custom (findByEmail, findActiveByOrg)
5. Paginación y filtering implementados
6. Transaction support

**Criterio de completitud:**
- [ ] Interface + implementación por entidad principal
- [ ] CRUD base implementado
- [ ] Queries custom para los use cases principales
- [ ] Pagination implementada según 3B.4.4
- [ ] Soft delete implementado (donde aplique)
- [ ] Cada repository tiene unit test
- [ ] No hay queries raw sin justificación (usar ORM)

**Anti-patrones:**
- ❌ **Repository por tabla:** 30 repositories para 30 tablas — solo crear para entidades con lógica de acceso.
- ❌ **Queries N+1:** Loop que hace 1 query por item — usar includes/joins.
- ❌ **Sin interface:** Implementación directa sin interface — no mockeable.
- ❌ **Business logic en repository:** El repository calcula descuentos — eso va en el service.

**Template:** `phases/04-development/deliverables/repositories/` *(pendiente)*

---

### 4.3.5 DTOs/Schemas

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.3 Backend Development |
| **Responsable** | Backend Developer |
| **Ejecuta** | Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | Zod / TypeScript |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Por endpoint nuevo |

**Perfil de ejecución:** Requiere definir schemas de validación tipados que validen inputs y serialicen outputs.  
En VTT: un agente puede generar DTOs y Zod schemas desde el OpenAPI spec. Es altamente delegable. Necesita brief con: OpenAPI spec con request/response schemas.

**Qué es:** Data Transfer Objects y schemas de validación: Zod schemas (o class-validator) para validar request bodies, query params, y path params; y DTOs de response para serializar outputs (qué campos se exponen en la API, qué se oculta — nunca exponer password hash, internal IDs, etc.).

**Para qué sirve:** Los DTOs son el "firewall" entre la BD y la API: el model tiene 20 campos pero el DTO de response solo expone 12 (sin password, sin internal flags). Los schemas de request validan que el input cumple el formato ANTES de llegar al service — si el email no es válido, se rechaza en la capa de validación, no en el service.

**Inputs requeridos:**
- `3B.4.1` OpenAPI Spec — schemas de request/response
- `4.3.3` Models — campos del modelo
- `3B.7.9` Input Validation Rules — reglas de validación

**Dependencias (predecessors):**
- `3B.4.1` OpenAPI Spec *(obligatorio)* — schemas
- `4.3.3` Models *(obligatorio)* — campos base

**Habilita (successors):**
- `4.3.1` API Endpoints — controllers usan DTOs para validar
- `4.4.7` Types/Interfaces — frontend puede derivar types de los DTOs

**Audiencia:**
- **Backend Developer** — validación y serialización
- **Frontend Developer** — entiende qué enviar y qué recibir

**Secciones esperadas:**
1. Request schemas por endpoint (CreateUserInput, UpdateOrderInput)
2. Response DTOs por entidad (UserResponse, OrderListResponse)
3. Query param schemas (PaginationQuery, FilterQuery)
4. Shared schemas (DateRange, Pagination, SortOrder)
5. Validation error messages customizados

**Criterio de completitud:**
- [ ] Schema de validación para cada endpoint que recibe body
- [ ] DTO de response para cada entidad expuesta
- [ ] Campos sensibles excluidos de response DTOs (password, internal flags)
- [ ] Validation messages user-friendly (no "Expected string, received number")
- [ ] Types exportados para consumo del frontend
- [ ] Tests de validación (inputs válidos e inválidos)

**Anti-patrones:**
- ❌ **Exponer el modelo directo:** `res.json(user)` con password hash incluido — data leak.
- ❌ **Sin validación de input:** Aceptar cualquier body y fallar en la BD — errores crípticos.
- ❌ **DTOs duplicados:** Copiar los mismos campos en 5 DTOs diferentes — crear DTOs base y extender.
- ❌ **Mensajes de error técnicos:** "ZodError: Expected string, received undefined at path email" — no es user-friendly.

**Template:** `phases/04-development/deliverables/dtos/` *(pendiente)*

---

### 4.3.6 Workers

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.3 Backend Development |
| **Responsable** | Backend Developer |
| **Ejecuta** | Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | TypeScript |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 2-3 días |
| **Frecuencia** | Por feature que requiera async |

**Perfil de ejecución:** Requiere experiencia con procesamiento asíncrono: queues, consumers, retry logic, dead-letter queues.  
En VTT: un agente puede generar scaffolding de workers (consumer, producer, retry config). La lógica de procesamiento requiere developer. Necesita brief con: async flows (3B.5.6), queue tool, y error handling.

**Qué es:** Workers/Jobs que procesan tareas asíncronas fuera del request/response cycle: envío de emails, generación de reportes, procesamiento de archivos, sincronización de datos con servicios externos, y scheduled jobs (cron). Cada worker: consume de una queue, procesa, y reporta resultado.

**Para qué sirve:** Operaciones que toman más de 500ms no deben bloquear la API response. Los workers permiten: responder rápido al usuario ("tu reporte se está generando"), procesar en background, y reintentar si falla — sin que el usuario espere.

**Inputs requeridos:**
- `3B.5.6` Async Flows — flujos asíncronos diseñados
- `3B.1.5` Technology Stack — herramienta de queue (BullMQ, SQS)
- `3B.2.6` Error Handling Strategy — retry logic, DLQ

**Dependencias (predecessors):**
- `3B.5.6` Async Flows *(obligatorio)* — diseño de flujos async
- `4.3.2` Services *(obligatorio)* — workers reusan services

**Habilita (successors):**
- `4.3.9` Unit Tests BE — tests de workers
- `3B.8.11` Monitoring Strategy — monitoring de queues

**Audiencia:**
- **Backend Developer** — implementación y mantenimiento
- **DevOps Lead** — deployment y monitoring de workers

**Secciones esperadas:**
1. Producers (dónde se enqueue el job)
2. Consumers (workers que procesan)
3. Job definitions (nombre, payload schema, options)
4. Retry configuration (attempts, backoff, DLQ)
5. Scheduled jobs / Cron definitions
6. Monitoring/logging de jobs

**Criterio de completitud:**
- [ ] Cada flujo async del 3B.5.6 tiene su worker
- [ ] Retry logic implementada (con backoff exponencial)
- [ ] Dead-letter queue configurada para jobs que fallan después de N retries
- [ ] Jobs son idempotentes (procesar 2 veces no duplica resultado)
- [ ] Logging de inicio, fin, y error de cada job
- [ ] Scheduled jobs documentados (nombre, schedule, qué hace)
- [ ] Tests de workers

**Anti-patrones:**
- ❌ **Proceso async sin retry:** Si el email falla, se pierde — retry lo resuelve el 95% de las veces.
- ❌ **Jobs no idempotentes:** Procesar un job 2 veces envía 2 emails — el usuario recibe duplicados.
- ❌ **Sin DLQ:** Jobs que fallan se pierden silenciosamente — data loss invisible.
- ❌ **Workers sin monitoring:** "¿Está corriendo el worker de emails?" — nadie sabe.

**Template:** `phases/04-development/deliverables/workers/` *(pendiente)*

---

### 4.3.7 Middlewares

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.3 Backend Development |
| **Responsable** | Backend Developer |
| **Ejecuta** | Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | TypeScript |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Una vez + adiciones |

**Perfil de ejecución:** Requiere entendimiento del middleware pipeline del framework (request → middlewares → handler → response).  
En VTT: un agente puede generar middlewares estándar (auth, logging, error handler, rate limit, CORS). Es altamente delegable. Necesita brief con: auth spec, logging strategy, y security headers.

**Qué es:** Funciones middleware que interceptan requests antes/después del handler: authentication (validar JWT), authorization (verificar permisos), request logging, error handling global, rate limiting, CORS, security headers, request ID generation, y response time tracking.

**Para qué sirve:** Los middlewares implementan cross-cutting concerns que aplican a todos (o muchos) endpoints sin duplicar código en cada controller. Auth se verifica una vez en middleware, no en cada endpoint. Errors se manejan en un global handler, no en cada catch.

**Inputs requeridos:**
- `3B.4.6` Authentication Spec — auth middleware
- `3B.4.7` Authorization Spec — authz middleware
- `3B.2.6` Error Handling Strategy — error handler middleware
- `3B.4.8` Rate Limiting — rate limit middleware
- `3B.7.7` Security Headers — headers middleware
- `3B.7.10` Security Logging — logging middleware

**Dependencias (predecessors):**
- `3B.4.6` Authentication Spec *(obligatorio)*
- `3B.2.6` Error Handling Strategy *(obligatorio)*

**Habilita (successors):**
- `4.3.1` API Endpoints — endpoints usan middlewares
- `4.3.15` Logging — logging middleware implementado

**Audiencia:**
- **Backend Developer** — usa y extiende middlewares
- **Security Engineer** — valida auth y security middlewares
- **Tech Lead** — code review de middlewares críticos

**Secciones esperadas:**
1. Auth middleware (JWT validation, token extraction)
2. Authorization middleware (role/permission check)
3. Error handler middleware (global catch, formatting, logging)
4. Request logging middleware (method, path, status, duration)
5. Rate limiting middleware
6. CORS middleware
7. Security headers middleware
8. Request ID middleware (genera UUID por request para tracing)
9. Orden de middleware pipeline documentado

**Criterio de completitud:**
- [ ] Auth middleware funcional (JWT validation)
- [ ] Authorization middleware con role checking
- [ ] Global error handler que captura todas las excepciones
- [ ] Request logging con request ID
- [ ] Rate limiting configurado
- [ ] Security headers aplicados (CSP, HSTS, etc.)
- [ ] CORS configurado correctamente
- [ ] Orden de middleware pipeline correcto y documentado
- [ ] Tests de cada middleware

**Anti-patrones:**
- ❌ **Auth en cada controller:** `if (!req.user) return 401` duplicado en 30 endpoints — va en middleware.
- ❌ **Error handler que traga errores:** Catch que loggea pero retorna 200 — el cliente cree que todo salió bien.
- ❌ **Middleware order incorrecto:** Auth después de rate limit → usuarios no autenticados consumen rate limit de usuarios legítimos.
- ❌ **CORS `*` en producción:** Permite requests desde cualquier origen — security risk.

**Template:** `phases/04-development/deliverables/middlewares/` *(pendiente)*

---

### 4.3.8 Utils

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.3 Backend Development |
| **Responsable** | Backend Developer |
| **Ejecuta** | Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | TypeScript |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Continuo (por necesidad) |
| **Frecuencia** | Continua |

**Perfil de ejecución:** Requiere capacidad de identificar funcionalidad reutilizable y extraerla a utils.  
En VTT: un agente puede generar utils comunes (date formatting, slug generation, pagination helpers). Es altamente delegable.

**Qué es:** Funciones utilitarias reutilizables en el backend: formateo de fechas, generación de slugs, hashing, sanitización, pagination helpers, error factories, response formatters, y type guards. Son funciones puras (sin side effects) que se usan transversalmente.

**Para qué sirve:** Evita duplicación de lógica repetitiva. En lugar de que cada service tenga su propia función de formatear fechas, hay un `formatDate()` en utils que todos usan. Son las "herramientas" compartidas del codebase.

**Inputs requeridos:**
- Necesidades recurrentes durante el desarrollo
- `3B.2.5` Naming Conventions — naming de utils

**Dependencias (predecessors):**
- `3B.2.1` Folder Structure *(obligatorio)* — dónde viven los utils

**Habilita (successors):**
- Todo el código del backend los consume

**Audiencia:**
- **Backend Developer** — uso diario

**Secciones esperadas:**
1. Date utils (formatDate, parseDate, diffDays)
2. String utils (slugify, truncate, capitalize)
3. Crypto utils (hashPassword, generateToken, compareHash)
4. Pagination utils (calculateOffset, buildPaginationMeta)
5. Error utils (createAppError, isAppError)
6. Response utils (successResponse, errorResponse)
7. Type guards (isString, isNumber, isDefined)

**Criterio de completitud:**
- [ ] Funciones puras (sin side effects)
- [ ] Cada util tiene unit test
- [ ] Cada util tiene JSDoc/TSDoc
- [ ] No duplican funcionalidad de libraries existentes (lodash, date-fns)
- [ ] Carpeta `src/utils/` organizada por dominio

**Anti-patrones:**
- ❌ **Utils como cajón de sastre:** 50 funciones sin relación en un archivo — descomponer por dominio.
- ❌ **Reinventar lodash:** Escribir `deepClone()` custom cuando lodash lo hace — usar libraries probadas.
- ❌ **Utils con side effects:** `sendEmail()` en utils — eso es un service, no un util.
- ❌ **Utils sin tests:** "Es una función simple" — bugs en utils se propagan a todo el codebase.

**Template:** `phases/04-development/deliverables/utils/` *(pendiente)*

---

### 4.3.9 Unit Tests BE

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.3 Backend Development |
| **Responsable** | Backend Developer |
| **Ejecuta** | Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | Jest |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Continuo (30% del tiempo de dev) |
| **Frecuencia** | Por feature |

**Perfil de ejecución:** Requiere experiencia en testing: arrange-act-assert, mocking, fixtures, y test naming conventions.  
En VTT: un agente puede generar tests unitarios a partir de los services y su lógica. Es bastante delegable para tests de CRUD y validación. Tests de lógica compleja requieren developer.

**Qué es:** Tests unitarios del backend que verifican la lógica de cada unidad (service, util, middleware) de forma aislada: mockean dependencias (repositories, external services), testean happy path y error paths, y verifican que las business rules se aplican correctamente.

**Para qué sirve:** Los unit tests son la red de seguridad del código: si un refactor rompe una business rule, el test falla inmediatamente. Sin tests, los bugs se descubren en QA (caro) o en producción (muy caro). Coverage ≥80% es el target estándar.

**Inputs requeridos:**
- `4.3.2` Services — servicios a testear
- `4.3.8` Utils — utils a testear
- `4.3.7` Middlewares — middlewares a testear
- `4.6.5` Mock Factories — factories para test data

**Dependencias (predecessors):**
- `4.3.2` Services *(obligatorio)* — código a testear
- `4.6.5` Mock Factories *(recomendado)* — data de tests

**Habilita (successors):**
- `4.6.3` Test Coverage Report — coverage measurement
- `4.6.4` Coverage ≥80% — metric target
- CI/CD pipeline — tests como gate

**Audiencia:**
- **Backend Developer** — escribe y mantiene tests
- **Tech Lead** — verifica coverage y calidad de tests en code review

**Secciones esperadas:**
1. Tests por service (1 archivo de test por service)
2. Tests por util
3. Tests por middleware
4. Test fixtures y factories
5. Coverage report

**Criterio de completitud:**
- [ ] Cada service tiene tests (happy path + error paths)
- [ ] Cada util tiene tests
- [ ] Middlewares críticos testeados (auth, error handler)
- [ ] Coverage ≥80% de líneas
- [ ] Tests pasan en CI sin flakiness
- [ ] Naming convention: `describe('ServiceName')` → `it('should do X when Y')`
- [ ] Mocks correctos (no testear la BD en unit tests)

**Anti-patrones:**
- ❌ **Tests que testean el mock:** `expect(mockRepo.findById).toHaveBeenCalled()` sin verificar el resultado — testa la implementación, no el comportamiento.
- ❌ **Tests frágiles:** Cambian con cada refactor porque testean implementación interna.
- ❌ **Solo happy path:** 100% de tests son "create user succeeds" — ¿qué pasa cuando falla?
- ❌ **Tests lentos:** Unit tests que conectan a DB real — deben ser in-memory/mocked.
- ❌ **Coverage gaming:** Tests sin assertions solo para subir coverage — falsa seguridad.

**Template:** `phases/04-development/deliverables/unit-tests-be/` *(pendiente)*

---

### 4.3.10 Integration Tests

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.3 Backend Development |
| **Responsable** | Backend Developer |
| **Ejecuta** | Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | Jest / Supertest |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 2-3 días |
| **Frecuencia** | Por feature |

**Perfil de ejecución:** Requiere setup de test DB, request testing (Supertest), y manejo de test lifecycle (setup/teardown).  
En VTT: un agente puede generar integration tests desde el OpenAPI spec y request/response examples. Es bastante delegable.

**Qué es:** Tests que verifican flujos completos HTTP request → response contra una API corriendo con BD real (test DB): envían requests con Supertest, verifican status codes, response bodies, y side effects en la BD. Prueban que controllers + services + repositories + BD funcionan juntos correctamente.

**Para qué sirve:** Los unit tests verifican piezas aisladas; los integration tests verifican que las piezas encajan. Un service que pasa unit tests puede fallar en integración si el controller no le pasa los datos correctos o el repository tiene un bug en el query.

**Inputs requeridos:**
- `3B.4.3` Request/Response Examples — fixtures de request/response
- `4.3.1` API Endpoints — endpoints a testear
- `4.2.4` Test Data — datos para tests

**Dependencias (predecessors):**
- `4.3.1` API Endpoints *(obligatorio)* — endpoints implementados
- `4.2.4` Test Data *(obligatorio)* — datos en test DB

**Habilita (successors):**
- `5.3.1` API Tests — QA tests de API (basados en integration tests)
- CI/CD pipeline — integration tests como gate

**Audiencia:**
- **Backend Developer** — escribe y mantiene
- **QA Engineer** — referencia de coverage de API

**Secciones esperadas:**
1. Test setup (test DB, migrations, seed, app instance)
2. Tests por endpoint (request → response verification)
3. Tests de auth (con token, sin token, token expirado)
4. Tests de authorization (rol correcto, rol incorrecto)
5. Tests de validation (input inválido → 400)
6. Test teardown (cleanup de test data)

**Criterio de completitud:**
- [ ] Cada endpoint CRUD tiene integration test
- [ ] Happy path y error paths cubiertos
- [ ] Auth tests (con/sin token, expirado, forbidden)
- [ ] Validation tests (inputs inválidos)
- [ ] Tests aislados (no dependen de orden de ejecución)
- [ ] Test DB con setup/teardown limpio
- [ ] Pasan en CI consistentemente (no flaky)

**Anti-patrones:**
- ❌ **Tests que dependen de orden:** Test B falla si test A no corrió primero — tests deben ser independientes.
- ❌ **Test DB compartida:** Todos los tests usan la misma DB sin cleanup — data de un test contamina otro.
- ❌ **Tests contra producción:** Integration tests apuntando a la API real — peligroso y lento.
- ❌ **Solo happy path:** Testear POST /users con datos válidos pero no con email duplicado.

**Template:** `phases/04-development/deliverables/integration-tests/` *(pendiente)*

---

### 4.3.11 API Documentation

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.3 Backend Development |
| **Responsable** | Backend Developer |
| **Ejecuta** | Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | Swagger UI |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Incluido en implementación (auto-generado) |
| **Frecuencia** | Automática con cada deploy |

**Perfil de ejecución:** Requiere configurar auto-generación de docs desde decorators/annotations del framework.  
En VTT: un agente puede configurar Swagger/OpenAPI auto-generation. Es altamente delegable.

**Qué es:** Documentación interactiva de la API auto-generada desde el código: Swagger UI accesible en `/api/docs` que muestra todos los endpoints, schemas, examples, y permite hacer requests de prueba directamente desde el browser. Se genera automáticamente desde decorators (NestJS @ApiProperty) o annotations.

**Para qué sirve:** Documentación que siempre está actualizada porque se genera del código. Si se agrega un endpoint, aparece en Swagger automáticamente. Si se cambia un schema, se refleja. Es la documentación viva de la API.

**Inputs requeridos:**
- `4.3.1` API Endpoints — endpoints con decorators
- `4.3.5` DTOs/Schemas — schemas documentados
- Framework con soporte Swagger (NestJS, Fastify, Express)

**Dependencias (predecessors):**
- `4.3.1` API Endpoints *(obligatorio)*
- `4.3.5` DTOs/Schemas *(obligatorio)*

**Habilita (successors):**
- Frontend Developer consulta docs
- External Integrators consultan docs
- `3B.4.10` Postman Collection — puede importar desde Swagger

**Audiencia:**
- **Frontend Developer** — referencia de API
- **QA Engineer** — testing manual desde Swagger UI
- **External Integrators** — documentación de API pública

**Secciones esperadas:**
1. Swagger UI configurado en ruta `/api/docs`
2. Todos los endpoints con descripción
3. Request/response schemas documentados
4. Auth configuration en Swagger (Bearer token input)
5. Examples incluidos
6. Grouping por tags/modules

**Criterio de completitud:**
- [ ] Swagger UI accesible en `/api/docs`
- [ ] Todos los endpoints documentados
- [ ] Schemas de request/response completos
- [ ] Auth configurada (Authorize button funciona)
- [ ] Examples incluidos en endpoints principales
- [ ] Try it out funciona (requests reales desde Swagger)

**Anti-patrones:**
- ❌ **Docs manuales:** Documentación en un Markdown que nadie actualiza — se desincroniza del código.
- ❌ **Swagger en producción sin auth:** Cualquiera puede acceder y hacer requests — proteger con auth o desactivar en prod.
- ❌ **Schemas incompletos:** `@ApiProperty()` sin type ni description — docs auto-generadas pero inútiles.

**Template:** `phases/04-development/deliverables/api-docs-config.ts` *(pendiente)*

---

### 4.3.12 Postman Collection

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.3 Backend Development |
| **Responsable** | Backend Developer |
| **Ejecuta** | Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | JSON (Postman) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día (actualización) |
| **Frecuencia** | Por sprint |

**Perfil de ejecución:** Requiere Postman y actualización de la collection con nuevos endpoints.  
En VTT: un agente puede generar/actualizar Postman collection desde Swagger. Es altamente delegable.

**Qué es:** Actualización de la Postman Collection (3B.4.10) con los endpoints implementados: bodies con datos reales, auth pre-configurada, test scripts que validan responses, y environments actualizados. La collection evoluciona con cada sprint.

**Para qué sirve:** La collection diseñada en 3B.4.10 tenía datos de ejemplo. Ahora se actualiza con datos funcionales que realmente funcionan contra la API implementada. Es la herramienta de testing manual más usada por el equipo.

**Inputs requeridos:**
- `3B.4.10` Postman Collection — collection inicial
- `4.3.1` API Endpoints — endpoints implementados
- `4.3.11` API Documentation — puede importar desde Swagger

**Dependencias (predecessors):**
- `3B.4.10` Postman Collection *(obligatorio)* — base
- `4.3.1` API Endpoints *(obligatorio)*

**Habilita (successors):**
- Testing manual del equipo
- `5.3.1` API Tests — automation con Newman

**Audiencia:**
- **Todo el equipo técnico** — testing manual

**Secciones esperadas:**
1. Collection actualizada con endpoints implementados
2. Environments actualizados (dev, staging URLs reales)
3. Auth configurada y funcional
4. Request bodies con datos funcionales
5. Test scripts básicos por request

**Criterio de completitud:**
- [ ] Todos los endpoints implementados en la collection
- [ ] Requests funcionales (no errores 500)
- [ ] Auth funcional
- [ ] Environments configurados

**Anti-patrones:**
- ❌ **Collection desactualizada:** Endpoints que ya no existen, schemas que cambiaron.
- ❌ **Sin environments:** URLs hardcoded a localhost — no funciona para staging.

**Template:** `phases/04-development/deliverables/postman-collection.json` *(pendiente)*

---

### 4.3.13 Backend README

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.3 Backend Development |
| **Responsable** | Backend Developer |
| **Ejecuta** | Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | README.md |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez + actualizaciones |

**Perfil de ejecución:** Requiere documentación técnica clara del backend.  
En VTT: un agente puede generar el README del backend. Es altamente delegable.

**Qué es:** README específico del backend (si es un monorepo con `/backend/README.md` o el README principal si es repo separado): arquitectura del backend, estructura de carpetas, cómo correr, cómo testear, convenciones, y guía de contribución backend-specific.

**Para qué sirve:** Un developer nuevo al backend lee este README y entiende: cómo está organizado, qué patrones sigue, cómo agregar un endpoint nuevo, y cómo correr tests. Es el onboarding backend-specific.

**Inputs requeridos:**
- `3B.2.1` Folder Structure — estructura a documentar
- `3B.2.3` Design Patterns — patterns a documentar
- `4.1.2` Environment Setup Guide — referencia al setup

**Dependencias (predecessors):**
- Backend implementado (4.3.1-4.3.10)

**Habilita (successors):**
- Onboarding de developers nuevos al backend

**Audiencia:**
- **Backend Developer** — referencia y onboarding
- **New team members** — entrada al backend

**Secciones esperadas:**
1. Overview de arquitectura backend
2. Folder structure con descripción
3. Cómo agregar un nuevo endpoint (step-by-step)
4. Cómo agregar un nuevo service
5. Cómo correr tests
6. Patterns y convenciones
7. Debugging guide

**Criterio de completitud:**
- [ ] Estructura de carpetas documentada
- [ ] "How to add a new endpoint" step-by-step
- [ ] Cómo correr tests documentado
- [ ] Patterns documentados con ejemplos
- [ ] Probado por developer que no lo escribió

**Anti-patrones:**
- ❌ **README genérico:** "This is a backend" sin información útil.
- ❌ **README desactualizado:** Estructura de hace 3 meses que ya cambió.
- ❌ **Sin "how to":** Documenta qué hay pero no cómo contribuir — el developer sigue preguntando.

**Template:** `phases/04-development/deliverables/backend-readme.md` *(pendiente)*

---

### 4.3.14 Error Handling

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.3 Backend Development |
| **Responsable** | Backend Developer |
| **Ejecuta** | Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | TypeScript |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez + refinamientos |

**Perfil de ejecución:** Requiere implementar la Error Handling Strategy (3B.2.6) en código.  
En VTT: un agente puede generar la jerarquía de excepciones custom, el global error handler, y el error response formatter. Es altamente delegable.

**Qué es:** Implementación de la estrategia de error handling: jerarquía de excepciones custom (AppError → ValidationError, NotFoundError, BusinessRuleError, UnauthorizedError), global error handler middleware, error response formatter (formato estándar con code, message, details, requestId), y HTTP status code mapping.

**Para qué sirve:** Sin error handling estándar, cada endpoint maneja errores diferente: uno retorna `{ error: "bad" }`, otro `{ message: "fail", code: 500 }`. La implementación estandarizada garantiza que todos los errores tienen el mismo formato, los mismos campos, y el mismo nivel de información.

**Inputs requeridos:**
- `3B.2.6` Error Handling Strategy — diseño a implementar
- `3B.4.5` Error Codes — catálogo de error codes

**Dependencias (predecessors):**
- `3B.2.6` Error Handling Strategy *(obligatorio)*
- `3B.4.5` Error Codes *(obligatorio)*

**Habilita (successors):**
- `4.3.7` Middlewares — global error handler
- `4.3.1` API Endpoints — endpoints usan custom exceptions
- `4.3.2` Services — services throw custom exceptions

**Audiencia:**
- **Backend Developer** — usa custom exceptions
- **Frontend Developer** — consume error responses estándar

**Secciones esperadas:**
1. Base AppError class (code, message, statusCode, details)
2. Custom exceptions (ValidationError, NotFoundError, BusinessRuleError, etc.)
3. Global error handler middleware
4. Error response formatter
5. HTTP status code mapping (exception → status)
6. Error logging (qué se loggea, qué no)

**Criterio de completitud:**
- [ ] Jerarquía de excepciones implementada (mínimo 5 tipos)
- [ ] Global error handler captura todas las excepciones
- [ ] Error response tiene formato estándar (code, message, details, requestId)
- [ ] Stack traces NUNCA en responses (solo en logs)
- [ ] HTTP status codes correctos por tipo de error
- [ ] Tests de error handling

**Anti-patrones:**
- ❌ **throw new Error("something"):** Strings genéricos sin tipo — el handler no sabe qué status code retornar.
- ❌ **Stack trace en response:** Información interna expuesta al cliente.
- ❌ **500 para todo:** Validation error retorna 500 en vez de 400 — confunde al frontend.

**Template:** `phases/04-development/deliverables/error-handling/` *(pendiente)*

---

### 4.3.15 Logging

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.3 Backend Development |
| **Responsable** | Backend Developer |
| **Ejecuta** | Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | TypeScript |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5-1 día |
| **Frecuencia** | Una vez + refinamientos |

**Perfil de ejecución:** Requiere implementar structured logging con niveles, contexto, y formatos.  
En VTT: un agente puede configurar el logger (Winston, Pino) con formato estructurado. Es altamente delegable.

**Qué es:** Implementación del sistema de logging del backend: logger configurado (Winston, Pino), formato structured JSON, niveles de log (debug, info, warn, error), contexto automático (requestId, userId, method, path), y reglas de qué loggear en cada nivel. Incluye request logging middleware y application-level logging.

**Para qué sirve:** Los logs son la "caja negra" del sistema en producción. Cuando algo falla a las 3AM, los logs dicen qué pasó: qué request llegó, qué parámetros tenía, qué servicio falló, y con qué error. Sin logging structured, `console.log("error")` no dice nada útil.

**Inputs requeridos:**
- `3B.7.10` Security Logging — eventos de seguridad a loggear
- `3B.8.11` Monitoring Strategy — herramienta de log aggregation
- `3B.2.6` Error Handling Strategy — logging de errores

**Dependencias (predecessors):**
- `3B.7.10` Security Logging *(obligatorio)* — eventos a loggear
- `3B.8.11` Monitoring Strategy *(recomendado)* — formato y destino

**Habilita (successors):**
- `7.1.1` Monitoring Setup — logs como input de monitoring
- Debugging en producción
- Alerting basado en logs

**Audiencia:**
- **Backend Developer** — usa el logger
- **DevOps Lead** — configura log aggregation
- **Tech Lead** — verifica calidad de logging en code review

**Secciones esperadas:**
1. Logger configurado (Winston/Pino) con formato JSON structured
2. Log levels definidos (debug, info, warn, error) con reglas de uso
3. Request logging middleware (method, path, status, duration, requestId)
4. Application logging patterns (service operations, business events)
5. Security logging (auth events, authz failures)
6. Datos que NUNCA se loggean (passwords, tokens, PII sin masking)
7. Log destinations (stdout, file, log aggregation service)

**Criterio de completitud:**
- [ ] Logger structured JSON configurado
- [ ] Request logging automático en todos los endpoints
- [ ] Levels usados correctamente (info para operaciones normales, error para fallos)
- [ ] RequestId en todos los logs (para tracing)
- [ ] Passwords y tokens NUNCA loggeados
- [ ] Logs parseable por herramienta de aggregation (JSON format)
- [ ] Performance: logging no impacta latencia (async logging)

**Anti-patrones:**
- ❌ **console.log():** No es un logger — sin levels, sin formato, sin contexto.
- ❌ **Loggear passwords:** `log.info("Login", { email, password })` — credentials en plain text en logs.
- ❌ **Sin requestId:** Logs sin correlación — imposible seguir un request a través de múltiples services.
- ❌ **Log everything en debug:** Producción con debug level = logs de 100GB/día — costo y noise.
- ❌ **Logging síncrono:** `fs.writeFileSync()` en cada log — bloquea el event loop.

**Template:** `phases/04-development/deliverables/logging/` *(pendiente)*

---

## Tabla resumen de ejecutores — Fase 4.3 Backend Development

| Deliverable | Responsable | Ejecuta | Delegable VTT |
|-------------|-------------|---------|---------------|
| 4.3.1 API Endpoints | Backend Developer | Backend Developer | 🔶 Parcial — scaffolding CRUD sí, lógica custom no |
| 4.3.2 Services | Backend Developer | Backend Developer | 🔶 Parcial — scaffolding sí, business rules complejas no |
| 4.3.3 Models | Backend Developer | Backend Developer | ✅ — puede generar models desde schema |
| 4.3.4 Repositories | Backend Developer | Backend Developer | ✅ — puede generar CRUD repositories con interface |
| 4.3.5 DTOs/Schemas | Backend Developer | Backend Developer | ✅ — puede generar desde OpenAPI spec |
| 4.3.6 Workers | Backend Developer | Backend Developer | 🔶 Parcial — scaffolding sí, lógica de procesamiento no |
| 4.3.7 Middlewares | Backend Developer | Backend Developer | ✅ — puede generar middlewares estándar |
| 4.3.8 Utils | Backend Developer | Backend Developer | ✅ — puede generar utils comunes |
| 4.3.9 Unit Tests BE | Backend Developer | Backend Developer | 🔶 Parcial — puede generar tests de CRUD, tests de lógica compleja no |
| 4.3.10 Integration Tests | Backend Developer | Backend Developer | 🔶 Parcial — puede generar tests desde OpenAPI examples |
| 4.3.11 API Documentation | Backend Developer | Backend Developer | ✅ — puede configurar Swagger auto-generation |
| 4.3.12 Postman Collection | Backend Developer | Backend Developer | ✅ — puede actualizar desde Swagger |
| 4.3.13 Backend README | Backend Developer | Backend Developer | ✅ — puede generar README completo |
| 4.3.14 Error Handling | Backend Developer | Backend Developer | ✅ — puede implementar jerarquía de excepciones |
| 4.3.15 Logging | Backend Developer | Backend Developer | ✅ — puede configurar logger structured |

---

## Siguiente archivo

**Próximo:** `DICCIONARIO_FASE_04_04_FRONTEND_DEVELOPMENT.md` — 15 deliverables (4.4.1 a 4.4.15)
