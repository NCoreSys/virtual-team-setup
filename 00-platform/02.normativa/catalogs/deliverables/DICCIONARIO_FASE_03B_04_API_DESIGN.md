# DICCIONARIO DE DELIVERABLES — FASE 3B.4: API DESIGN

**Versión:** 1.0  
**Fecha:** 2026-05-14  
**Fase:** 3B — Design Technical  
**Subfase:** 3B.4 — API Design  
**Total deliverables:** 11  
**Responsable de subfase:** Tech Lead  
**Aprueba:** Solution Architect

---

## Contexto de la subfase

API Design define los contratos entre el frontend y el backend, entre servicios internos, y entre el sistema y consumidores externos. Un buen API design es el contrato más importante del proyecto: permite que frontend y backend se desarrollen en paralelo, que terceros integren con confianza, y que el sistema evolucione sin romper consumidores existentes. Las decisiones de API son difíciles de cambiar una vez que hay consumidores — hay que hacerlas bien desde el inicio.

**Prerequisitos de subfase:**
- Solution Architecture (3B.1) — contenedores y componentes definidos
- Database Design (3B.3) — entidades/resources identificadas
- Use Cases detallados (2.3.4) — operaciones que la API debe soportar

**Entrega de subfase:**
- Contratos de API completos, documentados, y testeables antes de escribir una línea de backend

---

### 3B.4.1 OpenAPI Spec

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.4 API Design |
| **Responsable** | Tech Lead |
| **Ejecuta** | Tech Lead / Backend Developer |
| **Aprueba** | Solution Architect |
| **Formato** | YAML/JSON (OpenAPI 3.0+) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 3-5 días |
| **Frecuencia** | Una vez + actualizaciones por sprint |

**Perfil de ejecución:** Requiere conocimiento de la especificación OpenAPI 3.0+, RESTful design principles, y experiencia en diseño de APIs consumibles. Debe entender schemas, references ($ref), security schemes, y response codes.  
En VTT: un agente puede generar el OpenAPI spec completo en YAML a partir de: lista de endpoints, request/response schemas, y reglas de autenticación. Es altamente delegable — es un formato estructurado y bien definido. Necesita brief con: lista de recursos (entities), operaciones CRUD por recurso, request/response examples, auth method, y reglas de paginación.

**Qué es:** Archivo de especificación formal de la API en formato OpenAPI 3.0+ (anteriormente Swagger). Define cada endpoint con: path, HTTP method, parameters (path, query, header), request body schema, response schemas por status code, security requirements, y tags de agrupación. Es un contrato machine-readable que genera documentación, SDKs, y mocks automáticamente.

**Para qué sirve:** Es el contrato entre frontend y backend. Con el OpenAPI spec, el frontend puede generar types/interfaces automáticamente, hacer mock de la API antes de que el backend exista, y validar responses. El backend implementa contra el contrato sin ambigüedad. Herramientas como Swagger UI generan documentación interactiva automática.

**Inputs requeridos:**
- `3B.4.2` Endpoints List — lista de endpoints a especificar
- `3B.4.3` Request/Response Examples — examples para incluir en el spec
- `3B.4.6` Authentication Spec — security schemes
- `3B.3.1` ERD Complete — entidades que se mapean a API resources
- `2.3.4` Detailed Use Cases — operaciones que la API soporta

**Dependencias (predecessors):**
- `3B.4.2` Endpoints List *(obligatorio)* — qué endpoints incluir
- `3B.3.1` ERD Complete *(obligatorio)* — schemas derivados del modelo de datos
- `3B.4.6` Authentication Spec *(obligatorio)* — security schemes del spec
- `2.3.4` Detailed Use Cases *(recomendado)* — operaciones de negocio

**Habilita (successors):**
- `3B.4.10` Postman Collection — generada desde el OpenAPI spec
- `4.3.3` API Routes — implementación directa del spec
- `4.4.1` Components — frontend genera types desde el spec
- `5.3.1` API Tests — tests de contrato basados en el spec
- Swagger UI — documentación auto-generada

**Audiencia:**
- **Backend Developer** — contrato a implementar
- **Frontend Developer** — contrato a consumir, auto-generación de types
- **QA Engineer** — base para API tests
- **External Integrators** — documentación de la API pública
- **Tech Lead** — revisión del diseño de API

**Secciones esperadas:**
1. Info (title, version, description, contact)
2. Servers (dev, staging, prod URLs)
3. Security Schemes (Bearer JWT, API Key, OAuth2)
4. Tags (agrupación lógica de endpoints)
5. Paths (cada endpoint con operations)
6. Schemas/Components (request/response models reutilizables)
7. Parameters compartidos (pagination, sorting, filtering)
8. Response schemas por status code (200, 201, 400, 401, 403, 404, 422, 500)
9. Examples por endpoint

**Criterio de completitud:**
- [ ] Todos los endpoints del proyecto especificados
- [ ] Request body schema para POST/PUT/PATCH
- [ ] Response schema para cada status code relevante
- [ ] Security requirements en endpoints que lo requieren
- [ ] Schemas reutilizables con $ref (no duplicados)
- [ ] Pagination parameters documentados
- [ ] Examples incluidos para endpoints principales
- [ ] Spec válido (pasa validación de OpenAPI linter)
- [ ] Swagger UI generado y navegable

**Anti-patrones:**
- ❌ **Spec generado post-facto:** Escribir el código primero y generar el spec después — pierde el propósito de contrato previo.
- ❌ **Schemas duplicados:** Definir UserResponse en cada endpoint en vez de usar $ref — mantenimiento imposible.
- ❌ **Sin examples:** Spec técnicamente correcto pero sin examples — el consumidor no sabe qué esperar.
- ❌ **Spec desactualizado:** API evoluciona pero el spec no — documentación engañosa, peor que no tener spec.
- ❌ **Over-specification:** Documentar headers internos, cookies de sesión, y detalles de implementación — el spec es el contrato público, no el detalle interno.

**Template:** `phases/03B-design-technical/deliverables/openapi-spec.yaml` *(pendiente)*

---

### 3B.4.2 Endpoints List

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.4 API Design |
| **Responsable** | Tech Lead |
| **Ejecuta** | Tech Lead / Backend Developer |
| **Aprueba** | Solution Architect |
| **Formato** | Tabla (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez + actualizaciones por feature |

**Perfil de ejecución:** Requiere entendimiento de REST conventions (resources, HTTP verbs, status codes) y capacidad de mapear use cases a endpoints.  
En VTT: un agente puede generar la lista completa de endpoints a partir de los use cases y el ERD: mapear cada entidad a un resource con CRUD operations, y cada use case a un endpoint custom si no encaja en CRUD. Es altamente delegable. Necesita brief con: lista de entidades/resources, operaciones por entidad, y use cases que requieren endpoints custom (acciones que no son CRUD).

**Qué es:** Tabla maestra de todos los endpoints de la API: path, HTTP method, descripción, resource, autenticación requerida, y roles autorizados. Es la vista panorámica de toda la superficie de la API antes de entrar al detalle del OpenAPI spec.

**Para qué sirve:** Permite revisar el diseño de la API de un vistazo: ¿están todos los use cases cubiertos?, ¿los paths siguen convenciones REST?, ¿la agrupación por resource es coherente?, ¿faltan endpoints para algún flujo? Es más rápido iterar sobre una tabla que sobre un YAML de 2000 líneas.

**Inputs requeridos:**
- `2.3.4` Detailed Use Cases — operaciones que la API debe soportar
- `3B.3.1` ERD Complete — entidades que se mapean a resources
- `3B.4.6` Authentication Spec — qué endpoints requieren auth
- `3B.4.7` Authorization Spec — qué roles acceden a qué endpoints

**Dependencias (predecessors):**
- `2.3.4` Detailed Use Cases *(obligatorio)* — funcionalidades a exponer
- `3B.3.1` ERD Complete *(obligatorio)* — resources derivados de entidades
- `2.5.5` Authorization Rules *(recomendado)* — permisos por endpoint

**Habilita (successors):**
- `3B.4.1` OpenAPI Spec — endpoints detallados en el spec
- `3B.4.3` Request/Response Examples — examples por endpoint
- `3B.4.10` Postman Collection — colección con todos los endpoints
- `3B.9.3` Task Breakdown — estimación por endpoint

**Audiencia:**
- **Tech Lead** — revisión del diseño de API
- **Backend Developer** — vista panorámica de qué implementar
- **Frontend Developer** — qué endpoints consumir
- **QA Engineer** — scope de testing de API

**Secciones esperadas:**
1. Tabla de endpoints (method, path, descripción, resource, auth, roles)
2. Agrupación por resource/tag
3. Endpoints CRUD estándar por resource
4. Endpoints custom (acciones que no son CRUD: `/users/:id/activate`, `/orders/:id/refund`)
5. Endpoints de sistema (health check, version, docs)
6. Conteo total de endpoints por resource y method
7. Endpoints públicos vs privados

**Criterio de completitud:**
- [ ] Todos los use cases tienen al menos un endpoint que los soporta
- [ ] Convención REST aplicada (plural resources, HTTP verbs correctos)
- [ ] Auth y roles indicados por endpoint
- [ ] Endpoints de sistema incluidos (health, version)
- [ ] No hay endpoints duplicados ni redundantes
- [ ] Naming consistente (kebab-case, plural resources)

**Anti-patrones:**
- ❌ **Verbos en paths:** `/getUsers`, `/createOrder`, `/deleteItem` — el HTTP method ya indica la acción.
- ❌ **Singular resources:** `/user` en vez de `/users` — convención REST es plural.
- ❌ **Demasiados custom endpoints:** 15 endpoints custom por resource cuando CRUD + filters cubren el 80% — over-engineering.
- ❌ **Sin endpoints de sistema:** No incluir health check — el load balancer no puede verificar si el servicio está vivo.
- ❌ **Inconsistencia de naming:** `/user-profiles`, `/orderItems`, `/product_categories` — 3 convenciones en un proyecto.

**Template:** `phases/03B-design-technical/deliverables/endpoints-list.md` *(pendiente)*

---

### 3B.4.3 Request/Response Examples

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.4 API Design |
| **Responsable** | Tech Lead |
| **Ejecuta** | Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | JSON |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Una vez + actualizaciones por endpoint nuevo |

**Perfil de ejecución:** Requiere entendimiento de la estructura de datos del dominio y capacidad de generar examples realistas. Debe cubrir happy path, errores de validación, y error responses.  
En VTT: un agente puede generar request/response examples completos a partir del ERD, endpoints list, y data dictionary. Puede producir examples para happy path, validation errors, not found, unauthorized, y otros error cases. Es altamente delegable. Necesita brief con: endpoints list, schemas del OpenAPI, y data dictionary para valores realistas.

**Qué es:** Colección de ejemplos concretos de request bodies y response bodies para cada endpoint principal. Para cada endpoint: al menos un example de request exitoso con su response, un example de validation error, y un example de error de negocio. Los examples usan datos realistas (no "string", "0", "test").

**Para qué sirve:** El schema dice que `email` es `string` con format `email` — el example muestra `"maria.garcia@example.com"`. Los examples son lo primero que lee un developer para entender cómo usar un endpoint. Son la base para Postman collections, mock servers, y test fixtures. Un endpoint sin examples es un endpoint que se implementa por prueba y error.

**Inputs requeridos:**
- `3B.4.2` Endpoints List — endpoints a ejemplificar
- `3B.3.5` Data Dictionary — campos y valores válidos
- `3B.4.5` Error Codes — error responses estándar
- `3B.4.4` Pagination Strategy — format de paginated responses

**Dependencias (predecessors):**
- `3B.4.2` Endpoints List *(obligatorio)* — qué endpoints ejemplificar
- `3B.3.5` Data Dictionary *(recomendado)* — valores realistas
- `3B.4.5` Error Codes *(recomendado)* — error response format

**Habilita (successors):**
- `3B.4.1` OpenAPI Spec — examples embebidos en el spec
- `3B.4.10` Postman Collection — examples como pre-filled bodies
- `5.3.1` API Tests — fixtures basados en examples
- Mock servers — generados desde examples

**Audiencia:**
- **Frontend Developer** — entiende la estructura de datos al consumir la API
- **Backend Developer** — referencia al implementar
- **QA Engineer** — test fixtures
- **External Integrators** — documentación práctica

**Secciones esperadas:**
1. Convención de examples (datos ficticios pero realistas, no "string" o "test")
2. Por cada endpoint principal:
   - Request example (headers + body)
   - Response 200/201 example (body completo)
   - Response 400 example (validation error)
   - Response 404 example (si aplica)
   - Response 422 example (business rule violation, si aplica)
3. Pagination response example
4. Error response format estándar

**Criterio de completitud:**
- [ ] Todos los endpoints CRUD principales tienen examples
- [ ] Endpoints custom tienen examples
- [ ] Datos realistas (nombres reales, emails con formato, fechas válidas)
- [ ] Al menos un error example por endpoint
- [ ] Pagination example incluido
- [ ] Error response sigue el formato estándar (3B.4.5)
- [ ] Examples son copy-pasteable en Postman para testing inmediato

**Anti-patrones:**
- ❌ **Datos placeholder:** `"name": "string"`, `"email": "string"` — no comunica nada.
- ❌ **Solo happy path:** Mostrar el response 200 pero nunca los errors — el frontend no sabe qué errores manejar.
- ❌ **Examples inconsistentes:** El request crea un `User` con `id: 1` pero el response muestra `id: 42` — confuso.
- ❌ **Sin headers:** Mostrar body sin incluir `Authorization: Bearer ...` ni `Content-Type` — incompleto.

**Template:** `phases/03B-design-technical/deliverables/request-response-examples.md` *(pendiente)*

---

### 3B.4.4 Pagination Strategy

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.4 API Design |
| **Responsable** | Tech Lead |
| **Ejecuta** | Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | Documento (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere entendimiento de los trade-offs entre offset-based, cursor-based, y keyset pagination, y cuándo usar cada uno.  
En VTT: un agente puede documentar la estrategia de pagination con formato de request/response, query parameters, y examples. Es altamente delegable. Necesita brief con: tipo de pagination elegido (offset vs cursor), page size defaults/max, y formato de metadata (total, hasMore, nextCursor).

**Qué es:** Documento que define cómo la API maneja la paginación de colecciones: tipo de paginación (offset-based, cursor-based, keyset), query parameters estándar (`page`, `limit`, `cursor`, `after`), formato del response metadata (`total`, `page`, `hasMore`, `nextCursor`), page sizes (default y máximo), y reglas de sorting.

**Para qué sirve:** Sin paginación estándar, cada endpoint implementa su propia versión: uno usa `?page=1&size=10`, otro `?offset=0&limit=10`, otro `?cursor=abc`. La estrategia unifica el approach para que frontend solo aprenda un patrón. También previene queries de millones de registros que tumban la BD.

**Inputs requeridos:**
- `3B.1.5` Technology Stack — ORM/framework puede condicionar el approach
- `3B.3.3` Table Specifications — volumen de datos por tabla
- `3B.4.2` Endpoints List — endpoints que retornan colecciones

**Dependencias (predecessors):**
- `3B.4.2` Endpoints List *(obligatorio)* — qué endpoints paginan
- `3B.3.3` Table Specifications *(recomendado)* — volumen esperado

**Habilita (successors):**
- `3B.4.1` OpenAPI Spec — pagination parameters y response format documentados
- `3B.4.3` Request/Response Examples — pagination examples
- `4.3.3` API Routes — implementación uniforme

**Audiencia:**
- **Frontend Developer** — cómo paginar las llamadas
- **Backend Developer** — implementación estándar
- **QA Engineer** — testing de pagination edge cases

**Secciones esperadas:**
1. Tipo de paginación elegido y justificación (offset vs cursor vs keyset)
2. Query parameters estándar (nombre, tipo, default, max)
3. Response metadata format (total, page, pageSize, hasMore, nextCursor)
4. Page size: default y máximo
5. Sorting parameters (`sort`, `order`)
6. Filtering parameters (convención: `?status=active&role=admin`)
7. Examples completos (request + response con metadata)
8. Edge cases (página vacía, última página, single result)

**Criterio de completitud:**
- [ ] Tipo de paginación definido con justificación
- [ ] Query parameters documentados con defaults
- [ ] Response metadata format definido
- [ ] Page size max definido (protección contra over-fetching)
- [ ] Sorting y filtering documentados
- [ ] Al menos un example completo
- [ ] Edge cases documentados

**Anti-patrones:**
- ❌ **Sin max page size:** Permitir `?limit=999999` — query de todo el dataset, BD colapsada.
- ❌ **Offset en datasets grandes:** Offset pagination con `OFFSET 1000000` — performance degradada exponencialmente.
- ❌ **Metadata inconsistente:** Un endpoint retorna `total`, otro `count`, otro ni siquiera lo incluye.
- ❌ **Sin sorting estándar:** Cada endpoint ordena diferente — frontend no puede predecir el comportamiento.

**Template:** `phases/03B-design-technical/deliverables/pagination-strategy.md` *(pendiente)*

---

### 3B.4.5 Error Codes

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.4 API Design |
| **Responsable** | Tech Lead |
| **Ejecuta** | Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | Tabla (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5-1 día |
| **Frecuencia** | Una vez + adiciones por feature |

**Perfil de ejecución:** Requiere entendimiento de HTTP status codes y capacidad de diseñar error codes de aplicación que sean informativos y accionables.  
En VTT: un agente puede generar la tabla completa de error codes con: HTTP status, application error code, message, description, y resolution. Es altamente delegable. Necesita brief con: categorías de errores del sistema, formato de error response deseado, y business rules que pueden fallar.

**Qué es:** Catálogo de todos los códigos de error que la API puede retornar: HTTP status codes utilizados, application-level error codes (e.g., `AUTH_001`, `VAL_002`, `BIZ_003`), mensajes de error estándar, y el formato uniforme del error response body. Cada error code tiene: código, HTTP status, mensaje, descripción para el developer, y acción sugerida.

**Para qué sirve:** El frontend necesita saber exactamente qué errores puede recibir y cómo manejar cada uno. Sin error codes estándar, el frontend hace `if (error.message.includes("not found"))` — frágil y no mantenible. Con error codes, puede hacer `if (error.code === "USER_NOT_FOUND")` — robusto y tipado.

**Inputs requeridos:**
- `3B.2.6` Error Handling Strategy — clasificación de errores
- `2.5.3` Validation Rules — validaciones que pueden fallar
- `2.5.1` Business Rules Document — reglas de negocio que pueden violarse
- `3B.4.2` Endpoints List — endpoints que generan errores

**Dependencias (predecessors):**
- `3B.2.6` Error Handling Strategy *(obligatorio)* — clasificación de errores
- `2.5.3` Validation Rules *(recomendado)* — validation errors
- `2.5.1` Business Rules Document *(recomendado)* — business errors

**Habilita (successors):**
- `3B.4.1` OpenAPI Spec — error responses documentados
- `3B.4.3` Request/Response Examples — error response examples
- `4.3.7` Middleware — error handler implementa los codes
- `4.4.1` Components — frontend maneja error codes específicos

**Audiencia:**
- **Frontend Developer** — manejo de errores específicos por code
- **Backend Developer** — implementación de error responses
- **QA Engineer** — verificación de error responses correctos
- **External Integrators** — documentación de errores de la API

**Secciones esperadas:**
1. Formato estándar del error response body (JSON schema)
2. HTTP status codes utilizados (tabla: code, cuándo se usa)
3. Error codes de validación (VAL_xxx)
4. Error codes de autenticación/autorización (AUTH_xxx)
5. Error codes de negocio (BIZ_xxx)
6. Error codes de infraestructura (SYS_xxx)
7. Convención de naming de error codes
8. Por cada error code: código, HTTP status, message, description, resolution
9. Mensajes de error i18n-ready (code estable, message localizable)

**Criterio de completitud:**
- [ ] Formato de error response definido (code, message, details, requestId)
- [ ] HTTP status codes documentados con criterio de uso
- [ ] Al menos 10 error codes de validación
- [ ] Error codes de auth definidos (invalid token, expired, forbidden)
- [ ] Error codes de negocio para reglas principales
- [ ] Convención de naming consistente
- [ ] Messages son user-friendly (no stack traces ni jerga técnica)

**Anti-patrones:**
- ❌ **Solo HTTP status codes:** Retornar 400 sin error code de aplicación — el frontend no sabe si es validación, formato, o lógica.
- ❌ **Mensajes técnicos al usuario:** "NullPointerException at line 47" — expone internals y no es accionable para el usuario.
- ❌ **Error codes inconsistentes:** `ERR001`, `auth_invalid`, `VALIDATION-FAIL` — 3 convenciones diferentes.
- ❌ **Sin requestId:** Error sin identificador para correlacionar con logs — imposible debuggear en producción.
- ❌ **Mensajes hardcoded en inglés:** No preparar para i18n — el error code es estable, el mensaje se localiza.

**Template:** `phases/03B-design-technical/deliverables/error-codes.md` *(pendiente)*

---

### 3B.4.6 Authentication Spec

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.4 API Design |
| **Responsable** | Tech Lead |
| **Ejecuta** | Backend Developer / Security Engineer |
| **Aprueba** | Solution Architect |
| **Formato** | Documento (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere conocimiento de autenticación web: JWT (access + refresh tokens), OAuth2 flows, session management, y token storage best practices. Debe entender los vectores de ataque (CSRF, XSS, token theft).  
En VTT: un agente puede documentar la especificación de autenticación completa: flujos de login/logout/refresh, JWT structure, token lifecycle, y storage recommendations. Puede generar diagramas de flujo de auth. NO puede tomar decisiones de seguridad críticas sin el Security Engineer. Necesita brief con: auth method elegido (JWT, session, OAuth2), token lifetimes, refresh strategy, y providers externos (Auth0, Firebase Auth, Cognito).

**Qué es:** Especificación completa del mecanismo de autenticación de la API: cómo se obtiene un token (login flow), qué contiene el token (claims), cuánto dura (lifetime), cómo se renueva (refresh flow), cómo se revoca (logout/blacklist), y cómo se transporta (header, cookie). Si se usa un provider externo (Auth0, Firebase Auth, Cognito), documenta la integración.

**Para qué sirve:** Frontend y backend deben implementar el mismo flujo de autenticación exactamente igual. Sin esta especificación, el frontend implementa refresh tokens de una forma y el backend de otra — loops de logout infinitos, tokens que no se renuevan, y sesiones zombie.

**Inputs requeridos:**
- `3B.1.5` Technology Stack — JWT library, auth provider
- `3B.7.2` Authentication Design — diseño de seguridad de auth
- `3B.4.2` Endpoints List — endpoints de auth (/login, /logout, /refresh)
- Requisitos de seguridad (MFA, social login, SSO)

**Dependencias (predecessors):**
- `3B.7.2` Authentication Design *(obligatorio)* — decisiones de seguridad de auth
- `3B.1.5` Technology Stack *(obligatorio)* — tools y providers
- `3B.4.2` Endpoints List *(recomendado)* — endpoints de auth

**Habilita (successors):**
- `3B.4.1` OpenAPI Spec — security schemes
- `3B.5.2` Auth Flow — sequence diagram de auth
- `4.3.4` Authentication Implementation — implementación del spec
- `4.4.1` Components — frontend auth flow (login form, token management)

**Audiencia:**
- **Frontend Developer** — implementación del auth flow en el cliente
- **Backend Developer** — implementación del auth en el servidor
- **Security Engineer** — validación de seguridad
- **QA Engineer** — testing de auth flows y edge cases

**Secciones esperadas:**
1. Auth method (JWT, session, OAuth2) con justificación
2. Login flow (request, response, token delivery)
3. Token structure (JWT claims: sub, iat, exp, roles, custom claims)
4. Token lifetimes (access token: 15min, refresh token: 7d, etc.)
5. Refresh flow (cómo renovar el access token)
6. Logout flow (token revocation, blacklist, client cleanup)
7. Token storage (httpOnly cookie vs localStorage — con justificación)
8. Token transport (Authorization header, cookie)
9. Multi-device sessions (si aplica)
10. Social login / SSO (si aplica)
11. MFA flow (si aplica)
12. Password reset flow
13. Error responses de auth (invalid credentials, expired token, revoked)

**Criterio de completitud:**
- [ ] Auth method definido con justificación
- [ ] Login, refresh, y logout flows documentados step-by-step
- [ ] Token structure con claims definidos
- [ ] Token lifetimes definidos (access, refresh)
- [ ] Token storage y transport definidos
- [ ] Password reset flow documentado
- [ ] Error responses de auth definidos
- [ ] Validado por Security Engineer

**Anti-patrones:**
- ❌ **Access tokens de larga vida:** JWT de 24h sin refresh — si se compromete, el atacante tiene acceso por 24h.
- ❌ **Refresh token en localStorage:** Susceptible a XSS — los refresh tokens van en httpOnly cookies.
- ❌ **Sin logout real:** "Logout" solo borra el token en el cliente pero el token sigue siendo válido — sesión zombie.
- ❌ **JWT sin expiración:** Tokens que nunca expiran — si se filtran, acceso permanente.
- ❌ **Credenciales en query params:** `/login?username=admin&password=123` — visibles en logs, browser history, y referrer headers.

**Template:** `phases/03B-design-technical/deliverables/authentication-spec.md` *(pendiente)*

---

### 3B.4.7 Authorization Spec

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.4 API Design |
| **Responsable** | Tech Lead |
| **Ejecuta** | Backend Developer / Security Engineer |
| **Aprueba** | Solution Architect |
| **Formato** | Documento (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Una vez + actualizaciones por nuevo rol/permiso |

**Perfil de ejecución:** Requiere entendimiento de modelos de autorización (RBAC, ABAC, PBAC) y capacidad de mapear roles y permisos a endpoints y resources específicos.  
En VTT: un agente puede generar la especificación de autorización completa: matriz rol-endpoint, definición de permisos, y middleware rules. Es altamente delegable. Necesita brief con: modelo de autorización elegido (RBAC/ABAC), roles definidos, permisos por rol, y endpoints list para mapear.

**Qué es:** Especificación del modelo de autorización: qué roles existen, qué permisos tiene cada rol, qué endpoints/resources puede acceder cada rol, y qué reglas de row-level security aplican (e.g., "un user solo puede ver sus propios orders"). Define si se usa RBAC (Role-Based), ABAC (Attribute-Based), o un híbrido.

**Para qué sirve:** Autenticación dice "quién eres", autorización dice "qué puedes hacer". Sin esta spec, los permisos se implementan ad-hoc: un endpoint checa `if (user.role === 'admin')`, otro no checa nada, otro checa el permiso incorrecto. La spec centraliza las reglas para implementación consistente.

**Inputs requeridos:**
- `2.5.5` Authorization Rules — reglas de autorización de negocio
- `3B.7.3` Authorization Design — diseño de seguridad de authz
- `3B.4.2` Endpoints List — endpoints a proteger
- `2.3.5` Actor Definitions — actores/roles del sistema

**Dependencias (predecessors):**
- `2.5.5` Authorization Rules *(obligatorio)* — reglas de negocio de permisos
- `3B.7.3` Authorization Design *(obligatorio)* — modelo RBAC/ABAC
- `3B.4.2` Endpoints List *(obligatorio)* — endpoints a proteger
- `2.3.5` Actor Definitions *(obligatorio)* — roles del sistema

**Habilita (successors):**
- `3B.4.1` OpenAPI Spec — security requirements por endpoint
- `4.3.4` Authentication Implementation — middleware de autorización
- `4.3.7` Middleware — guards/policies implementados
- `5.3.1` API Tests — tests de autorización por rol

**Audiencia:**
- **Backend Developer** — implementación de guards/policies
- **Frontend Developer** — UI condicional basada en permisos
- **Security Engineer** — validación del modelo
- **QA Engineer** — test matrix por rol
- **Product Owner** — validación de que los permisos reflejan el negocio

**Secciones esperadas:**
1. Modelo de autorización (RBAC/ABAC/híbrido) con justificación
2. Roles definidos (tabla: rol, descripción, permisos)
3. Permisos definidos (tabla: permiso, descripción, recursos afectados)
4. Matriz rol-permiso (tabla cruzada: rol × permiso = ✅/❌)
5. Matriz rol-endpoint (tabla: endpoint, roles autorizados)
6. Row-level security (reglas de "solo puede ver/editar lo suyo")
7. Reglas especiales (superadmin, owner, delegated permissions)
8. Herencia de roles (si aplica)
9. Implementation approach (middleware, decorator, policy, guard)
10. Default deny principle (todo está prohibido a menos que se autorice explícitamente)

**Criterio de completitud:**
- [ ] Todos los roles del sistema definidos
- [ ] Permisos granulares definidos (no solo "admin puede todo")
- [ ] Matriz rol-endpoint completa
- [ ] Row-level security documentado
- [ ] Default deny como principio
- [ ] Implementation approach definido
- [ ] Validado por Security Engineer
- [ ] Validado por Product Owner (los permisos reflejan el negocio)

**Anti-patrones:**
- ❌ **Solo 2 roles: admin y user:** Sin granularidad — o puedes todo o no puedes nada.
- ❌ **Hardcoded roles en código:** `if (role === 'admin')` en cada controller — no es un sistema de permisos, es spaghetti condicional.
- ❌ **Default allow:** Endpoints sin protección por defecto, y se agrega auth "cuando se acuerdan" — vulnerabilidades garantizadas.
- ❌ **Sin row-level security:** Un user puede ver/editar los datos de otro user porque nadie filtró por owner — data leak.
- ❌ **Permisos solo en backend:** El frontend no sabe qué permisos tiene el user — muestra botones que luego dan 403.

**Template:** `phases/03B-design-technical/deliverables/authorization-spec.md` *(pendiente)*

---

### 3B.4.8 Rate Limiting

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.4 API Design |
| **Responsable** | Tech Lead |
| **Ejecuta** | Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | Tabla (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez + ajustes post-producción |

**Perfil de ejecución:** Requiere entendimiento de rate limiting algorithms (fixed window, sliding window, token bucket, leaky bucket) y cómo proteger APIs de abuso sin afectar usuarios legítimos.  
En VTT: un agente puede documentar la estrategia de rate limiting con tabla de límites por endpoint/tier, headers de respuesta, y configuración. Es altamente delegable. Necesita brief con: tiers de usuarios (free, pro, enterprise), límites por tier, algoritmo elegido, y herramienta (Redis, API Gateway).

**Qué es:** Definición de los límites de uso de la API: requests por minuto/hora por IP, por usuario autenticado, o por API key. Incluye: algoritmo de rate limiting, límites por tier de usuario, headers de rate limit en responses (`X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`), y response cuando se excede el límite (429 Too Many Requests).

**Para qué sirve:** Sin rate limiting, un script malicioso o un bug en un cliente puede hacer 10,000 requests/segundo y tumbar la API. El rate limiting protege contra: DDoS, brute force attacks (login), scraping, y bugs en clientes que hacen polling agresivo. También permite diferenciar tiers de servicio (free: 100 req/min, pro: 1000 req/min).

**Inputs requeridos:**
- `3B.4.2` Endpoints List — endpoints a proteger
- `3B.1.5` Technology Stack — herramienta de rate limiting (Redis, API Gateway)
- `3B.8.6` Scaling Strategy — capacidad del sistema
- Requisitos de negocio (tiers, SLAs)

**Dependencias (predecessors):**
- `3B.4.2` Endpoints List *(obligatorio)* — endpoints a proteger
- `3B.1.5` Technology Stack *(obligatorio)* — herramienta

**Habilita (successors):**
- `3B.4.1` OpenAPI Spec — rate limit headers documentados
- `4.3.7` Middleware — rate limit middleware implementado
- `3B.7.1` Security Plan — rate limiting como control de seguridad

**Audiencia:**
- **Backend Developer** — implementación
- **Frontend Developer** — manejo de 429 responses
- **DevOps Lead** — configuración y monitoring
- **External Integrators** — límites que deben respetar

**Secciones esperadas:**
1. Algoritmo de rate limiting (fixed window, sliding window, token bucket)
2. Tabla de límites (endpoint o grupo, tier, requests/window, burst)
3. Límites especiales (login: más restrictivo, health: sin límite)
4. Headers de rate limit en responses
5. Response format de 429 Too Many Requests
6. Retry-After header
7. Rate limit por: IP, user, API key (cuál o combinación)
8. Almacenamiento de contadores (Redis, in-memory, API Gateway)
9. Excepciones (IPs whitelistadas, service accounts)

**Criterio de completitud:**
- [ ] Algoritmo elegido y justificado
- [ ] Límites definidos para endpoints principales
- [ ] Login/auth más restrictivo (protección brute force)
- [ ] Headers de rate limit documentados
- [ ] 429 response format definido con Retry-After
- [ ] Herramienta de rate limiting elegida
- [ ] Excepciones documentadas

**Anti-patrones:**
- ❌ **Sin rate limiting:** API abierta sin límites — un script puede tumbar el servicio.
- ❌ **Límites demasiado restrictivos:** 10 req/min para un dashboard que necesita 20 calls al cargar — UX rota para usuarios legítimos.
- ❌ **Sin headers:** El cliente no sabe cuántos requests le quedan — no puede hacer throttling proactivo.
- ❌ **Rate limit solo por IP:** En empresas con NAT, 1000 usuarios comparten una IP — todos bloqueados por uno.
- ❌ **Login sin rate limit específico:** Permite brute force de credenciales — security hole.

**Template:** `phases/03B-design-technical/deliverables/rate-limiting.md` *(pendiente)*

---

### 3B.4.9 Versioning Strategy

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.4 API Design |
| **Responsable** | Tech Lead |
| **Ejecuta** | Tech Lead |
| **Aprueba** | Solution Architect |
| **Formato** | Documento (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere entendimiento de API evolution, backward compatibility, y los trade-offs entre URL versioning, header versioning, y query parameter versioning.  
En VTT: un agente puede documentar la estrategia de versionado basándose en las mejores prácticas de la industria. Es altamente delegable. Necesita brief con: approach elegido (URL path, header, query param), policy de breaking changes, y deprecation timeline.

**Qué es:** Documento que define cómo se versiona la API para evolucionar sin romper clientes existentes: dónde va el version (URL path `/v1/`, header `API-Version`, query param `?v=1`), qué constituye un breaking change, cuál es la política de deprecation (cuánto tiempo se mantienen versiones antiguas), y cómo se comunican los cambios.

**Para qué sirve:** Las APIs evolucionan. Sin versionado, un cambio en el response schema rompe todos los clientes existentes. Con versionado, los clientes pueden migrar a su ritmo mientras se mantiene backward compatibility. La estrategia define las reglas del juego antes de que sea necesario versionar.

**Inputs requeridos:**
- `3B.1.1` Architecture Document — contexto técnico
- Requisitos de backward compatibility
- Número esperado de consumidores de la API

**Dependencias (predecessors):**
- `3B.4.2` Endpoints List *(obligatorio)* — endpoints que se versionan
- `3B.1.1` Architecture Document *(recomendado)* — contexto

**Habilita (successors):**
- `3B.4.1` OpenAPI Spec — versioning reflejado en server URLs y paths
- `3B.4.11` API Guidelines — reglas de evolución de la API
- Todo el desarrollo futuro de la API

**Audiencia:**
- **Tech Lead** — enforcement de la política
- **Backend Developer** — implementación de versiones
- **Frontend Developer** — manejo de versiones al consumir
- **External Integrators** — expectativa de estabilidad

**Secciones esperadas:**
1. Approach de versioning (URL path, header, query) con justificación
2. Formato de versión (v1, v2 — major only; o semver para APIs internas)
3. Definición de breaking change (qué cambios requieren nueva versión)
4. Non-breaking changes (qué cambios son backward compatible)
5. Deprecation policy (timeline: anuncio → sunset → removal)
6. Communication de cambios (changelog, deprecation headers, email)
7. Maintenance de versiones antiguas (cuántas versiones en paralelo)
8. Migration guides (cómo se documenta la migración entre versiones)

**Criterio de completitud:**
- [ ] Approach de versioning definido
- [ ] Breaking vs non-breaking changes definidos con ejemplos
- [ ] Deprecation policy con timeline
- [ ] Communication plan para cambios
- [ ] Máximo de versiones en paralelo definido
- [ ] Policy aprobada por stakeholders

**Anti-patrones:**
- ❌ **Sin versioning:** Cambios breaking directos sin versión — rompe clientes existentes.
- ❌ **Versioning pero sin deprecation:** v1, v2, v3, v4 todas mantenidas eternamente — costo de mantenimiento exponencial.
- ❌ **Breaking changes sin comunicar:** Cambiar el response schema sin avisar — clientes se rompen por sorpresa.
- ❌ **Demasiadas versiones por cambios menores:** Nueva versión por agregar un campo opcional — over-versioning, un campo nuevo es non-breaking.

**Template:** `phases/03B-design-technical/deliverables/versioning-strategy.md` *(pendiente)*

---

### 3B.4.10 Postman Collection

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.4 API Design |
| **Responsable** | Tech Lead |
| **Ejecuta** | Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | JSON (Postman v2.1) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5-1 día |
| **Frecuencia** | Una vez + actualizaciones por endpoint nuevo |

**Perfil de ejecución:** Requiere experiencia con Postman: collections, environments, variables, pre-request scripts, y test scripts. Debe saber organizar requests de forma navegable.  
En VTT: un agente puede generar la Postman collection completa desde el OpenAPI spec (importación automática) o manualmente desde la endpoints list con request/response examples pre-populated. Es altamente delegable. Necesita brief con: OpenAPI spec o endpoints list, base URL por environment, y auth tokens de test.

**Qué es:** Archivo JSON de Postman Collection que contiene todos los endpoints de la API organizados por resource, con request bodies pre-populated, variables de environment (base URL, auth token), y opcionalmente test scripts que validan responses. Incluye environments (dev, staging, prod) con variables por environment.

**Para qué sirve:** Permite a cualquier developer o QA testear la API con un click — sin tener que construir requests manualmente. Es la herramienta de testing manual más usada. También sirve como documentación interactiva (Postman genera docs desde la collection) y como base para automation con Newman (CLI de Postman).

**Inputs requeridos:**
- `3B.4.1` OpenAPI Spec — generación automática de la collection
- `3B.4.2` Endpoints List — endpoints a incluir
- `3B.4.3` Request/Response Examples — bodies pre-populated
- `3B.4.6` Authentication Spec — auth setup en Postman

**Dependencias (predecessors):**
- `3B.4.1` OpenAPI Spec *(obligatorio)* — fuente para generación
- `3B.4.3` Request/Response Examples *(obligatorio)* — bodies pre-populated
- `3B.4.6` Authentication Spec *(obligatorio)* — auth configurada en la collection

**Habilita (successors):**
- `5.3.1` API Tests — base para automation con Newman
- `4.3.3` API Routes — developers verifican implementación contra collection
- Testing manual durante desarrollo

**Audiencia:**
- **Backend Developer** — testing manual durante desarrollo
- **Frontend Developer** — exploración de la API
- **QA Engineer** — testing manual y automatizado
- **External Integrators** — exploración y testing

**Secciones esperadas:**
1. Collection con requests organizados por resource/folder
2. Environments (dev, staging, prod) con variables
3. Auth configurada (Bearer token, auto-refresh si posible)
4. Request bodies con examples realistas
5. Pre-request scripts para auth token refresh (si aplica)
6. Test scripts básicos (status code check, schema validation)
7. Variables de collection ({{baseUrl}}, {{authToken}}, {{userId}})
8. README en la collection con instrucciones de uso

**Criterio de completitud:**
- [ ] Todos los endpoints de la API incluidos
- [ ] Organizados por resource en folders
- [ ] Request bodies con datos realistas (no vacíos)
- [ ] Al menos 2 environments (dev, staging)
- [ ] Auth configurada y funcional
- [ ] Collection importable sin errores
- [ ] Instrucciones de setup documentadas

**Anti-patrones:**
- ❌ **Collection sin environments:** URLs hardcoded — hay que cambiar manualmente para cada environment.
- ❌ **Requests sin bodies:** Endpoints POST/PUT vacíos — el developer tiene que inventar el body.
- ❌ **Sin auth configurada:** Cada request requiere copiar/pegar el token manualmente — tedioso y error-prone.
- ❌ **Collection desactualizada:** Endpoints que ya no existen, schemas que cambiaron — collection engañosa.
- ❌ **Sin organización:** 50 requests en una lista plana sin folders — imposible de navegar.

**Template:** `phases/03B-design-technical/deliverables/postman-collection.json` *(pendiente)*

---

### 3B.4.11 API Guidelines

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.4 API Design |
| **Responsable** | Tech Lead |
| **Ejecuta** | Tech Lead |
| **Aprueba** | Solution Architect |
| **Formato** | Documento (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere experiencia en API design y opiniones formadas sobre convenciones RESTful, response formats, y consistency rules.  
En VTT: un agente puede generar las API guidelines basándose en guías de industria (Google API Design Guide, Microsoft REST API Guidelines, Zalando RESTful API Guidelines) customizadas al proyecto. Es altamente delegable. Necesita brief con: guía base a adoptar, customizaciones del proyecto, y decisiones de estilo ya tomadas (naming, pagination, error format).

**Qué es:** Documento que define las convenciones y estándares para diseñar endpoints de la API. Es el "coding standards" pero para APIs: naming conventions de paths, uso de HTTP methods, formato de responses, manejo de relaciones, bulk operations, filtering, sorting, embedding/expanding, y HATEOAS (si aplica). Garantiza que nuevos endpoints se diseñan de forma consistente.

**Para qué sirve:** Sin guidelines, cada developer diseña endpoints con su propio estilo. Las guidelines garantizan que un developer que sabe usar 5 endpoints puede usar los 50 restantes sin aprender convenciones nuevas. Es especialmente importante cuando la API es pública o tiene múltiples developers contribuyendo.

**Inputs requeridos:**
- `3B.4.4` Pagination Strategy — incluida en guidelines
- `3B.4.5` Error Codes — incluida en guidelines
- `3B.4.8` Rate Limiting — incluida en guidelines
- `3B.4.9` Versioning Strategy — incluida en guidelines
- `3B.2.5` Naming Conventions — naming de endpoints
- Guía base (Google, Microsoft, Zalando)

**Dependencias (predecessors):**
- `3B.4.4` Pagination Strategy *(obligatorio)* — sección de guidelines
- `3B.4.5` Error Codes *(obligatorio)* — sección de guidelines
- `3B.4.9` Versioning Strategy *(obligatorio)* — sección de guidelines
- `3B.2.5` Naming Conventions *(obligatorio)* — naming de API paths

**Habilita (successors):**
- Todos los futuros endpoints del proyecto — se diseñan siguiendo las guidelines
- `4.3.3` API Routes — implementación consistente
- API review process — criterios de revisión de nuevos endpoints

**Audiencia:**
- **Backend Developer** — referencia al diseñar nuevos endpoints
- **Tech Lead** — criterios de API review
- **Frontend Developer** — expectativa de consistencia
- **External Integrators** — convenciones de la API documentadas

**Secciones esperadas:**
1. Guía base adoptada y scope de customización
2. URL design (resource naming, nesting, max depth)
3. HTTP methods (cuándo GET/POST/PUT/PATCH/DELETE)
4. Request format (Content-Type, encoding, max body size)
5. Response format (envelope vs flat, casing: camelCase)
6. Status codes (tabla: code, cuándo se usa)
7. Pagination (referencia a 3B.4.4)
8. Filtering y sorting (query params conventions)
9. Error responses (referencia a 3B.4.5)
10. Versioning (referencia a 3B.4.9)
11. Rate limiting (referencia a 3B.4.8)
12. Relations (embedding, expanding, include params)
13. Bulk operations (batch endpoints, format)
14. Idempotency (idempotency keys para POST)
15. CORS policy
16. Do / Don't examples

**Criterio de completitud:**
- [ ] Convenciones de URL, methods, y response format documentadas
- [ ] Todas las secciones referenciadas (pagination, errors, versioning, rate limit)
- [ ] Do / Don't examples para cada convención principal
- [ ] Guía base referenciada
- [ ] CORS policy definida
- [ ] Idempotency rules definidas
- [ ] Validado por Solution Architect

**Anti-patrones:**
- ❌ **Guidelines que nadie lee:** 50 páginas de teoría REST — debe ser conciso y con examples.
- ❌ **Guidelines sin enforcement:** Reglas que no se revisan en PRs — se ignoran gradualmente.
- ❌ **Copiar guidelines de otro proyecto sin adaptar:** Guidelines de una API pública para una API interna — contextos diferentes.
- ❌ **Sin Do/Don't:** Solo reglas abstractas sin examples concretos — cada developer interpreta diferente.
- ❌ **Guidelines que contradicen los deliverables anteriores:** API Guidelines dice offset pagination pero Pagination Strategy dice cursor — inconsistencia.

**Template:** `phases/03B-design-technical/deliverables/api-guidelines.md` *(pendiente)*

---

## Tabla resumen de ejecutores — Fase 3B.4 API Design

| Deliverable | Responsable | Ejecuta | Delegable VTT |
|-------------|-------------|---------|---------------|
| 3B.4.1 OpenAPI Spec | Tech Lead | Tech Lead / Backend Developer | ✅ — puede generar spec completo en YAML desde endpoints y schemas |
| 3B.4.2 Endpoints List | Tech Lead | Tech Lead / Backend Developer | ✅ — puede mapear use cases y entidades a endpoints REST |
| 3B.4.3 Request/Response Examples | Tech Lead | Backend Developer | ✅ — puede generar examples realistas desde schemas y data dictionary |
| 3B.4.4 Pagination Strategy | Tech Lead | Backend Developer | ✅ — puede documentar estrategia completa con examples |
| 3B.4.5 Error Codes | Tech Lead | Backend Developer | ✅ — puede generar catálogo completo de error codes |
| 3B.4.6 Authentication Spec | Tech Lead | Backend Developer / Security Engineer | 🔶 Parcial — puede documentar spec, pero decisiones de seguridad requieren Security Engineer |
| 3B.4.7 Authorization Spec | Tech Lead | Backend Developer / Security Engineer | 🔶 Parcial — puede generar matrices rol-permiso, pero model choice requiere juicio |
| 3B.4.8 Rate Limiting | Tech Lead | Backend Developer | ✅ — puede documentar estrategia completa |
| 3B.4.9 Versioning Strategy | Tech Lead | Tech Lead | ✅ — puede documentar estrategia basada en mejores prácticas |
| 3B.4.10 Postman Collection | Tech Lead | Backend Developer | ✅ — puede generar collection completa desde OpenAPI spec |
| 3B.4.11 API Guidelines | Tech Lead | Tech Lead | ✅ — puede generar guidelines basadas en guías de industria |

---

## Siguiente archivo

**Próximo:** `DICCIONARIO_FASE_03B_05_SEQUENCE_DIAGRAMS.md` — 6 deliverables (3B.5.1 a 3B.5.6)
