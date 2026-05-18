# DICCIONARIO DE DELIVERABLES — FASE 3B.1: SOLUTION ARCHITECTURE

**Versión:** 1.0  
**Fecha:** 2026-05-14  
**Fase:** 3B — Design Technical  
**Subfase:** 3B.1 — Solution Architecture  
**Total deliverables:** 7  
**Responsable de subfase:** Solution Architect  
**Aprueba:** Tech Lead

---

## Contexto de la subfase

Solution Architecture es la columna vertebral técnica del proyecto. Define la estructura macro del sistema: qué piezas existen, cómo se comunican, qué tecnologías las implementan, y cómo fluyen los datos entre ellas. Se utiliza el modelo C4 (Context, Container, Component) para documentar la arquitectura en niveles progresivos de detalle. Las decisiones que se toman aquí condicionan toda la fase de desarrollo.

**Prerequisitos de subfase:**
- Requisitos funcionales y no funcionales definidos (Fase 2)
- Use cases detallados (2.3)
- Design UX/UI en handoff o completado (3A.9)
- Constraints técnicos identificados (infra existente, integraciones obligatorias)

**Entrega de subfase:**
- Arquitectura documentada y aprobada, lista para derivar diseño de código, BD, APIs y seguridad

---

### 3B.1.1 Architecture Document

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.1 Solution Architecture |
| **Responsable** | Solution Architect |
| **Ejecuta** | Solution Architect |
| **Aprueba** | Tech Lead |
| **Formato** | MD/PDF |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 3-5 días |
| **Frecuencia** | Una vez + actualizaciones mayores |

**Perfil de ejecución:** Requiere experiencia senior en diseño de sistemas distribuidos, cloud architecture, y trade-offs técnicos (performance vs cost, consistency vs availability). Debe poder justificar cada decisión con razonamiento técnico.  
En VTT: un agente puede generar la estructura del documento, compilar diagramas en formato Mermaid/PlantUML, y documentar las decisiones ya tomadas por el Solution Architect. NO puede tomar decisiones arquitectónicas — esas requieren experiencia y juicio humano. Necesita brief con: requisitos no funcionales, constraints técnicos, integraciones requeridas, y decisiones de stack ya tomadas.

**Qué es:** Documento maestro de arquitectura que consolida todas las vistas del sistema: contexto, contenedores, componentes, decisiones tecnológicas, puntos de integración, y flujo de datos. Es el documento de referencia que cualquier developer nuevo lee para entender "cómo está construido el sistema" a nivel macro.

**Para qué sirve:** Proporciona la visión holística del sistema antes de que se escriba una línea de código. Garantiza que todos los stakeholders técnicos comparten la misma mental model del sistema. Sirve como referencia autoritativa para resolver disputas de diseño ("¿dónde va esta lógica?", "¿qué servicio maneja esto?").

**Inputs requeridos:**
- `2.3.4` Detailed Use Cases — requisitos funcionales que la arquitectura debe soportar
- `2.5.1` Business Rules Document — reglas que condicionan el diseño
- `1.2.2` In Scope — alcance que la arquitectura cubre
- `1.2.6` Assumptions — supuestos técnicos
- NFRs (performance, scalability, availability, security)
- Constraints de infraestructura existente

**Dependencias (predecessors):**
- `2.3.4` Detailed Use Cases *(obligatorio)* — requisitos funcionales
- `2.5.1` Business Rules Document *(obligatorio)* — reglas de negocio que afectan diseño
- `1.2.2` In Scope *(obligatorio)* — alcance del sistema
- `1.4.1` Risk Register *(recomendado)* — riesgos técnicos a mitigar en la arquitectura
- `3A.9.1` Handoff Document *(recomendado)* — contexto de lo que el frontend necesita

**Habilita (successors):**
- `3B.1.2` System Context Diagram — vista L1 derivada del documento
- `3B.1.3` Container Diagram — vista L2
- `3B.1.4` Component Diagram — vista L3
- `3B.1.5` Technology Stack — stack derivado de decisiones
- `3B.2.1` Folder Structure — estructura de código alineada a arquitectura
- `3B.3.1` ERD Complete — modelo de datos derivado de la arquitectura
- `3B.4.1` OpenAPI Spec — contratos de API entre componentes
- `3B.6.3` ADR Documents — decisiones documentadas

**Audiencia:**
- **Tech Lead** — validación y alineación con capacidades del equipo
- **Solution Architect** — documento propio de referencia
- **Backend Developer** — entiende la estructura macro del backend
- **Frontend Developer** — entiende qué APIs consumir y cómo
- **DevOps Lead** — entiende qué desplegar y cómo se conecta
- **Security Engineer** — identifica superficie de ataque
- **Product Manager** — entiende las implicaciones técnicas del scope

**Secciones esperadas:**
1. Executive Summary (resumen de la solución en 1 párrafo)
2. Drivers arquitectónicos (requisitos funcionales clave, NFRs, constraints)
3. Vista de contexto (C4 Level 1 — sistema y actores externos)
4. Vista de contenedores (C4 Level 2 — aplicaciones, bases de datos, servicios)
5. Vista de componentes (C4 Level 3 — módulos internos de cada contenedor)
6. Stack tecnológico (tabla con justificación)
7. Puntos de integración (sistemas externos, APIs de terceros)
8. Flujo de datos (cómo fluyen los datos principales a través del sistema)
9. Cross-cutting concerns (logging, monitoring, auth, error handling)
10. Decisiones arquitectónicas clave (resumen — detalle en ADRs)
11. Riesgos técnicos y mitigaciones
12. Glosario técnico

**Criterio de completitud:**
- [ ] Las 3 vistas C4 (context, container, component) incluidas
- [ ] Stack tecnológico definido con justificación por elección
- [ ] Puntos de integración documentados
- [ ] Flujo de datos para al menos los 3 flujos principales
- [ ] NFRs mapeados a decisiones arquitectónicas
- [ ] Cross-cutting concerns documentados
- [ ] Revisado y aprobado por Tech Lead
- [ ] Comprensible por un developer que no participó en la decisión

**Anti-patrones:**
- ❌ **Architecture Astronaut:** Sobre-diseñar con microservicios, event sourcing y CQRS para una app CRUD — la complejidad debe justificarse con los NFRs.
- ❌ **Documento de 80 páginas que nadie lee:** Si no es consumible, no es útil — el Architecture Document debe ser conciso y referencial.
- ❌ **Sin justificación de decisiones:** "Usamos PostgreSQL" sin explicar por qué no MySQL, MongoDB, o DynamoDB — las decisiones sin contexto se cuestionan eternamente.
- ❌ **Arquitectura desconectada de requisitos:** Diseñar la arquitectura sin referenciar los use cases y NFRs — se construye para problemas que no existen.

**Template:** `phases/03B-design-technical/deliverables/architecture-document.md` *(pendiente)*

---

### 3B.1.2 System Context Diagram

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.1 Solution Architecture |
| **Responsable** | Solution Architect |
| **Ejecuta** | Solution Architect |
| **Aprueba** | Tech Lead |
| **Formato** | Diagrama (Mermaid/PlantUML/Draw.io) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere visión sistémica: entender el sistema como una caja negra y mapear todas sus interacciones con el mundo exterior (usuarios, sistemas externos, APIs de terceros).  
En VTT: un agente puede generar el diagrama C4 Level 1 en Mermaid o PlantUML a partir de una descripción textual del Solution Architect. Es altamente delegable como tarea de diagramación. Necesita brief con: nombre del sistema, tipos de usuarios/actores, sistemas externos con los que interactúa, y dirección del flujo (quién llama a quién).

**Qué es:** Diagrama de alto nivel (C4 Level 1 — System Context) que muestra el sistema como una caja negra y sus relaciones con actores externos: usuarios (personas), sistemas upstream (que envían datos), sistemas downstream (que consumen datos), y servicios de terceros (payment gateways, email providers, etc.). Es el "zoom out" máximo.

**Para qué sirve:** Responde la pregunta más básica: "¿qué es el sistema y con quién interactúa?". Es la primera diapositiva de cualquier presentación técnica. Permite a stakeholders no-técnicos entender los boundaries del sistema sin detalles internos. Define claramente qué es "nuestro" y qué es "externo".

**Inputs requeridos:**
- `3B.1.1` Architecture Document — contexto del sistema
- `2.3.5` Actor Definitions — actores que interactúan con el sistema
- `1.2.2` In Scope — qué incluye el sistema
- Inventario de sistemas externos e integraciones

**Dependencias (predecessors):**
- `3B.1.1` Architecture Document *(obligatorio)* — define el contexto
- `2.3.5` Actor Definitions *(obligatorio)* — actores del diagrama
- `1.2.2` In Scope *(recomendado)* — boundaries del sistema

**Habilita (successors):**
- `3B.1.3` Container Diagram — zoom in del sistema
- `3B.1.6` Integration Points — detalle de cada integración
- `3B.7.1` Security Plan — superficie de ataque visible

**Audiencia:**
- **Todos los stakeholders** — es el diagrama más accesible
- **Product Owner** — entiende boundaries del sistema
- **Security Engineer** — identifica superficie de ataque
- **DevOps Lead** — entiende qué conectar

**Secciones esperadas:**
1. Diagrama C4 Level 1 (sistema central, actores, sistemas externos)
2. Leyenda (colores, formas, significado)
3. Descripción de cada actor externo
4. Descripción de cada sistema externo (qué hace, protocolo de comunicación)
5. Notas sobre dirección del flujo (request/response, push/pull, sync/async)

**Criterio de completitud:**
- [ ] Sistema central representado como una caja
- [ ] Todos los tipos de usuario/actor representados
- [ ] Todos los sistemas externos identificados
- [ ] Flechas con dirección y protocolo (REST, GraphQL, SMTP, webhook)
- [ ] Leyenda incluida
- [ ] Diagrama comprensible sin explicación verbal adicional

**Anti-patrones:**
- ❌ **Demasiado detalle:** Mostrar componentes internos en el diagrama de contexto — eso es Level 2/3, no Level 1.
- ❌ **Sistemas fantasma:** Incluir integraciones "que quizás usemos" — solo lo confirmado.
- ❌ **Sin flechas direccionales:** Cajas conectadas sin indicar quién llama a quién — ambiguo.
- ❌ **Diagrama sin leyenda:** Colores y formas sin explicación — cada persona interpreta diferente.

**Template:** `phases/03B-design-technical/deliverables/system-context-diagram.mmd` *(pendiente)*

---

### 3B.1.3 Container Diagram

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.1 Solution Architecture |
| **Responsable** | Solution Architect |
| **Ejecuta** | Solution Architect |
| **Aprueba** | Tech Lead |
| **Formato** | Diagrama (Mermaid/PlantUML/Draw.io) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez + actualizaciones si cambia la estructura |

**Perfil de ejecución:** Requiere experiencia en diseño de sistemas: debe entender las unidades de deployment (web app, API server, database, message queue, CDN) y cómo se comunican.  
En VTT: un agente puede generar el diagrama C4 Level 2 en Mermaid/PlantUML a partir del description del Solution Architect. Puede también generar variantes (con/sin CDN, con/sin queue). Necesita brief con: lista de contenedores (apps, DBs, queues, caches), tecnología de cada uno, protocolo de comunicación entre ellos, y qué actor accede a qué contenedor.

**Qué es:** Diagrama de nivel intermedio (C4 Level 2 — Container) que abre la caja negra del sistema y muestra sus contenedores principales: aplicaciones web/mobile, APIs, bases de datos, colas de mensajes, caches, CDNs, workers, y sus interacciones. Cada contenedor es una unidad de deployment independiente con su tecnología.

**Para qué sirve:** Responde "¿de qué piezas está hecho el sistema?". Cada contenedor será desplegado, mantenido y escalado independientemente. Este diagrama es la base para planificar el desarrollo (qué equipos trabajan en qué contenedores), la infraestructura (qué servidores/servicios cloud necesitamos), y la seguridad (qué comunicaciones proteger).

**Inputs requeridos:**
- `3B.1.1` Architecture Document — decisiones arquitectónicas
- `3B.1.2` System Context Diagram — actores y sistemas externos
- `3B.1.5` Technology Stack — tecnología por contenedor
- NFRs de performance, scalability, availability

**Dependencias (predecessors):**
- `3B.1.1` Architecture Document *(obligatorio)* — decisiones que definen los contenedores
- `3B.1.2` System Context Diagram *(obligatorio)* — contexto externo
- `3B.1.5` Technology Stack *(recomendado)* — tecnología etiquetada en cada contenedor

**Habilita (successors):**
- `3B.1.4` Component Diagram — zoom in de cada contenedor
- `3B.1.7` Data Flow Diagram — flujo de datos entre contenedores
- `3B.3.1` ERD Complete — diseño de cada base de datos
- `3B.4.1` OpenAPI Spec — contrato de cada API
- `3B.8.1` Infrastructure Plan — infra para cada contenedor
- `3B.8.2` Infrastructure Diagram — mapping contenedor → infra

**Audiencia:**
- **Tech Lead** — planificación de trabajo por contenedor
- **Backend Developer** — entiende qué API/servicio desarrolla
- **Frontend Developer** — entiende qué API consumir
- **DevOps Lead** — qué desplegar y cómo conectar
- **Security Engineer** — comunicaciones a proteger

**Secciones esperadas:**
1. Diagrama C4 Level 2 (todos los contenedores con tecnología etiquetada)
2. Leyenda (contenedor, database, message queue, external system)
3. Tabla de contenedores (nombre, tipo, tecnología, responsabilidad, owner)
4. Comunicaciones (tabla: origen → destino, protocolo, sync/async, autenticación)
5. Notas sobre escalamiento (qué contenedores son stateless/stateful)

**Criterio de completitud:**
- [ ] Todos los contenedores identificados y etiquetados con tecnología
- [ ] Bases de datos como contenedores separados (no dentro de la API)
- [ ] Protocolo de comunicación en cada flecha (HTTP/REST, gRPC, AMQP, WebSocket)
- [ ] Sync vs Async indicado en cada comunicación
- [ ] Tabla complementaria de contenedores con owner/responsable
- [ ] Consistente con el System Context Diagram (mismos actores y sistemas externos)

**Anti-patrones:**
- ❌ **Monolito no explicitado:** Tener un solo contenedor "Backend" sin diferenciar API de workers de schedulers — falsa simplicidad.
- ❌ **Microservicios prematuros:** 15 contenedores para un MVP que podría ser un monolito — complejidad operacional innecesaria.
- ❌ **Sin tecnología etiquetada:** Contenedores genéricos ("API", "DB") sin indicar la tecnología — no informa decisiones.
- ❌ **Comunicaciones implícitas:** "El frontend habla con el backend" sin indicar protocolo, auth, ni sync/async.

**Template:** `phases/03B-design-technical/deliverables/container-diagram.mmd` *(pendiente)*

---

### 3B.1.4 Component Diagram

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.1 Solution Architecture |
| **Responsable** | Solution Architect |
| **Ejecuta** | Solution Architect / Tech Lead |
| **Aprueba** | Tech Lead |
| **Formato** | Diagrama (Mermaid/PlantUML/Draw.io) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Una vez + actualizaciones si cambian los módulos |

**Perfil de ejecución:** Requiere conocimiento profundo del dominio del negocio y de patrones de diseño de software. Debe poder descomponer un contenedor en módulos lógicos cohesivos con responsabilidades claras.  
En VTT: un agente puede generar diagramas C4 Level 3 en Mermaid/PlantUML. Puede también proponer una descomposición modular basada en los bounded contexts del dominio y los use cases. Es parcialmente delegable. Necesita brief con: contenedor a descomponer, módulos/layers identificados, responsabilidad de cada módulo, y dependencias entre módulos.

**Qué es:** Diagrama de detalle (C4 Level 3 — Component) que abre un contenedor específico y muestra sus componentes/módulos internos: controllers, services, repositories, modules, libraries. Generalmente se hace un diagrama por contenedor principal (API backend, frontend app). Muestra cómo los módulos internos colaboran entre sí.

**Para qué sirve:** Responde "¿cómo está organizado internamente cada contenedor?". Es el puente entre la arquitectura (macro) y el código (micro). Define los boundaries de módulos que se traducirán en carpetas, namespaces, y paquetes del código. Permite a los developers entender la división de responsabilidades antes de escribir código.

**Inputs requeridos:**
- `3B.1.3` Container Diagram — contenedor a descomponer
- `2.3.4` Detailed Use Cases — funcionalidades que los componentes implementan
- `2.5.1` Business Rules Document — reglas que viven en cada componente
- `3B.2.3` Design Patterns — patrones que definen la estructura interna

**Dependencias (predecessors):**
- `3B.1.3` Container Diagram *(obligatorio)* — define los contenedores a descomponer
- `2.3.4` Detailed Use Cases *(obligatorio)* — funcionalidades a mapear a componentes
- `3B.2.3` Design Patterns *(recomendado)* — patterns que definen layers/modules

**Habilita (successors):**
- `3B.2.1` Folder Structure — carpetas alineadas a componentes
- `3B.2.4` Module Dependencies — dependencias formalizadas
- `3B.5.3` Main Business Flows — sequences entre componentes
- `4.3.1` Backend Modules — implementación directa de componentes

**Audiencia:**
- **Tech Lead** — validación de la descomposición modular
- **Backend Developer** — entiende qué módulo implementa y sus dependencias
- **Frontend Developer** — entiende la estructura del frontend
- **Solution Architect** — validación de la separación de concerns

**Secciones esperadas:**
1. Diagrama C4 Level 3 por contenedor principal
2. Leyenda (component, service, repository, controller, etc.)
3. Tabla de componentes (nombre, tipo, responsabilidad, interfaces que expone)
4. Dependencias entre componentes (qué componente llama a cuál)
5. Mapping componente → use cases que implementa
6. Notas sobre boundaries de transacción
7. Componentes cross-cutting (logging, auth middleware, error handler)

**Criterio de completitud:**
- [ ] Al menos un diagrama Level 3 por contenedor principal (backend API, frontend app)
- [ ] Cada componente tiene nombre, tipo y responsabilidad
- [ ] Dependencias entre componentes explicitadas con flechas
- [ ] Mapping a use cases documentado
- [ ] Cross-cutting concerns identificados
- [ ] Diagrama validado por Tech Lead como implementable

**Anti-patrones:**
- ❌ **Componente "God Module":** Un componente que hace todo — no hay separación de concerns real.
- ❌ **Demasiada granularidad:** 30 componentes en un API con 10 endpoints — sobre-ingeniería que no se mapea a código real.
- ❌ **Dependencias circulares:** A depende de B, B depende de C, C depende de A — señal de mala descomposición.
- ❌ **Sin mapping a funcionalidad:** Componentes que existen por "buena práctica" pero no implementan ningún use case — bloatware arquitectónico.

**Template:** `phases/03B-design-technical/deliverables/component-diagram.mmd` *(pendiente)*

---

### 3B.1.5 Technology Stack

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.1 Solution Architecture |
| **Responsable** | Solution Architect |
| **Ejecuta** | Solution Architect / Tech Lead |
| **Aprueba** | Tech Lead |
| **Formato** | Tabla (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere conocimiento amplio del ecosistema tecnológico: lenguajes, frameworks, bases de datos, servicios cloud, herramientas de CI/CD. Debe poder evaluar trade-offs entre opciones (learning curve, community, performance, cost, hiring pool).  
En VTT: un agente puede documentar el stack en formato tabla con justificación una vez que el Solution Architect ha tomado las decisiones. Puede también generar comparativas de opciones evaluadas (pros/cons matrix). NO puede elegir el stack — esa decisión depende de factores humanos (experiencia del equipo, hiring, budget). Necesita brief con: decisiones de stack tomadas, justificación de cada elección, y alternativas consideradas.

**Qué es:** Tabla completa de todas las tecnologías seleccionadas para el proyecto, organizada por capa: frontend (framework, state management, testing), backend (lenguaje, framework, ORM), base de datos (engine, cache), infraestructura (cloud, CI/CD, monitoring), y herramientas de desarrollo (IDE, linting, formatting). Para cada tecnología: nombre, versión, justificación de la elección.

**Para qué sirve:** Elimina ambigüedad sobre qué tecnologías usar. Evita que cada developer elija su propio stack ("yo prefiero Vue, tú prefieres React"). Documenta las versiones exactas para evitar incompatibilidades. La justificación de cada elección previene cuestionamientos futuros y facilita onboarding.

**Inputs requeridos:**
- `3B.1.1` Architecture Document — contexto técnico
- NFRs (performance, scalability, security)
- Skills del equipo de desarrollo
- Budget de infraestructura
- Requisitos de integraciones (SDKs disponibles por lenguaje)

**Dependencias (predecessors):**
- `3B.1.1` Architecture Document *(obligatorio)* — contexto de decisiones
- `1.2.6` Assumptions *(recomendado)* — supuestos sobre tecnología
- `1.4.1` Risk Register *(recomendado)* — riesgos técnicos que influyen en elección

**Habilita (successors):**
- `3B.1.3` Container Diagram — tecnología etiquetada en cada contenedor
- `3B.2.1` Folder Structure — estructura depende del framework
- `3B.2.2` Coding Standards — estándares dependen del lenguaje
- `3B.3.2` Schema Definition — ORM/query builder depende del stack
- `3B.6.3` ADR Documents — decisiones de stack como ADRs
- `4.1.1` Environment Setup — instalación del stack elegido

**Audiencia:**
- **Todo el equipo técnico** — referencia de qué usar
- **DevOps Lead** — qué instalar y configurar
- **Tech Lead** — validación de capacidades del equipo
- **Product Manager** — implicaciones de costo y timeline
- **HR/Recruiting** — perfiles técnicos a contratar

**Secciones esperadas:**
1. Tabla de stack por capa (frontend, backend, database, infra, dev tools)
2. Por cada tecnología: nombre, versión, categoría, justificación
3. Alternativas consideradas (tabla: opción, pros, cons, motivo de descarte)
4. Matriz de compatibilidad (versiones compatibles entre sí)
5. Requisitos de licenciamiento (costo, tipo de licencia)
6. Plan de actualización (qué versiones están en LTS, cuándo expira soporte)
7. Skills gap (qué tecnologías necesitan ramp-up del equipo)

**Criterio de completitud:**
- [ ] Todas las capas cubiertas (frontend, backend, DB, infra, dev tools)
- [ ] Versión específica para cada tecnología
- [ ] Justificación escrita para cada elección principal
- [ ] Alternativas consideradas documentadas para decisiones no obvias
- [ ] Licenciamiento verificado (ninguna sorpresa de costos)
- [ ] Skills gap identificado con plan de ramp-up
- [ ] Aprobado por Tech Lead

**Anti-patrones:**
- ❌ **Resume-Driven Development:** Elegir tecnologías porque son "cool" o "nuevas" y no porque resuelven el problema — el stack es para el producto, no para el CV.
- ❌ **Sin versiones:** "Usamos React" sin especificar versión — incompatibilidades garantizadas.
- ❌ **Stack sin justificación:** Tabla de tecnologías sin explicar por qué — cuestionamiento eterno.
- ❌ **Ignorar al equipo:** Elegir Rust cuando el equipo sabe Python — el ramp-up puede ser más caro que los beneficios.
- ❌ **Vendor lock-in no reconocido:** Elegir servicios propietarios de cloud sin documentar el costo de migración futura.

**Template:** `phases/03B-design-technical/deliverables/technology-stack.md` *(pendiente)*

---

### 3B.1.6 Integration Points

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.1 Solution Architecture |
| **Responsable** | Solution Architect |
| **Ejecuta** | Solution Architect / Backend Developer |
| **Aprueba** | Tech Lead |
| **Formato** | Diagrama + Documento |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Una vez + actualizaciones si se agregan integraciones |

**Perfil de ejecución:** Requiere experiencia en integración de sistemas: APIs REST, webhooks, OAuth, message queues, file transfers, SDKs de terceros. Debe entender los failure modes de cada tipo de integración.  
En VTT: un agente puede documentar cada punto de integración en el formato estándar una vez que el Solution Architect los identifica. Puede generar diagramas de integración, tablas de mapping de datos, y checklists de consideraciones por integración. Necesita brief con: lista de integraciones, protocolo de cada una, credenciales/auth requerido, formato de datos, y SLAs del proveedor externo.

**Qué es:** Documentación detallada de cada punto donde el sistema se conecta con sistemas externos: APIs de terceros (payment gateways, email services, auth providers), sistemas legacy, file feeds, webhooks entrantes, y cualquier otra interfaz externa. Para cada integración: protocolo, autenticación, formato de datos, rate limits, SLA, y plan de fallback.

**Para qué sirve:** Las integraciones son la fuente #1 de fallos en producción ("se cayó el servicio de pagos", "el webhook de Stripe dejó de llegar"). Documentar cada integración con sus failure modes y fallbacks antes de codificar reduce drasticamente los outages. También facilita el onboarding de developers nuevos que necesitan entender cómo conectar con cada servicio externo.

**Inputs requeridos:**
- `3B.1.2` System Context Diagram — sistemas externos identificados
- `2.3.4` Detailed Use Cases — funcionalidades que requieren integraciones
- Documentación de APIs de terceros
- Contratos/SLAs con proveedores externos

**Dependencias (predecessors):**
- `3B.1.2` System Context Diagram *(obligatorio)* — sistemas externos identificados
- `3B.1.1` Architecture Document *(obligatorio)* — contexto técnico
- `2.3.4` Detailed Use Cases *(recomendado)* — qué funcionalidades requieren integraciones

**Habilita (successors):**
- `3B.4.1` OpenAPI Spec — endpoints de integración documentados
- `3B.5.5` Integration Flows — sequence diagrams de cada integración
- `3B.7.1` Security Plan — seguridad de cada integración
- `4.3.6` Third Party Integrations — implementación de integraciones

**Audiencia:**
- **Backend Developer** — implementación de cada integración
- **Tech Lead** — evaluación de complejidad y riesgo
- **DevOps Lead** — configuración de networking, secrets, y monitoring
- **Security Engineer** — evaluación de seguridad de cada integración
- **QA Engineer** — estrategia de testing (mocks vs sandbox)

**Secciones esperadas:**
1. Inventario de integraciones (tabla: nombre, proveedor, tipo, criticidad)
2. Por cada integración:
   - Descripción y propósito
   - Protocolo (REST, GraphQL, SOAP, WebSocket, SFTP, SDK)
   - Autenticación (API key, OAuth2, JWT, mTLS)
   - Formato de datos (JSON, XML, CSV)
   - Rate limits y quotas
   - SLA del proveedor (uptime, latencia)
   - Data mapping (campos nuestros → campos del proveedor)
   - Error handling y retry strategy
   - Fallback plan (qué pasa si el servicio se cae)
   - Sandbox/test environment disponible
3. Diagrama de integraciones
4. Matriz de criticidad (qué integraciones son bloqueantes vs degradables)
5. Cronograma de setup (onboarding con cada proveedor)

**Criterio de completitud:**
- [ ] Todas las integraciones del System Context Diagram detalladas
- [ ] Protocolo y autenticación documentados para cada una
- [ ] Rate limits y SLA del proveedor registrados
- [ ] Fallback plan para integraciones críticas
- [ ] Sandbox/test environment identificado para cada integración
- [ ] Cronograma de setup con dependencias de onboarding
- [ ] Revisado por Security Engineer para consideraciones de seguridad

**Anti-patrones:**
- ❌ **"La API funciona, ya está":** No documentar rate limits, SLA, ni fallback — funciona hasta que no funciona.
- ❌ **Sin sandbox:** Desarrollar contra producción del proveedor — datos reales contaminados con pruebas.
- ❌ **Sin retry strategy:** Asumir que la API siempre responde — la primera vez que falle, el sistema se rompe en cascada.
- ❌ **Credenciales hardcoded:** Documentar API keys en el documento de integraciones — las credenciales van en secrets management, no en docs.
- ❌ **Sin data mapping:** "Les mandamos el objeto de usuario" sin especificar qué campos mapean a qué — errores de integración garantizados.

**Template:** `phases/03B-design-technical/deliverables/integration-points.md` *(pendiente)*

---

### 3B.1.7 Data Flow Diagram

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.1 Solution Architecture |
| **Responsable** | Solution Architect |
| **Ejecuta** | Solution Architect |
| **Aprueba** | Tech Lead |
| **Formato** | Diagrama (Mermaid/PlantUML/Draw.io) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez + actualizaciones si cambia el flujo |

**Perfil de ejecución:** Requiere entendimiento de cómo los datos se transforman y mueven a través del sistema: desde el input del usuario hasta el almacenamiento, procesamiento, y output. Debe poder diferenciar entre flujos sincrónicos y asincrónicos.  
En VTT: un agente puede generar DFDs en Mermaid a partir de una descripción textual de los flujos de datos. Puede producir diagramas de nivel 0 (contexto) y nivel 1 (procesos). Es altamente delegable. Necesita brief con: flujos de datos principales (user input → processing → storage → output), transformaciones de datos, y data stores involucrados.

**Qué es:** Diagrama que muestra cómo los datos principales (entidades del dominio) fluyen a través del sistema: desde su origen (user input, webhook, feed), pasando por procesamiento (validación, transformación, enriquecimiento), almacenamiento (database, cache, file storage), hasta su consumo (UI, reports, APIs, exports). Puede ser DFD clásico (procesos, data stores, flujos) o un diagrama de flujo personalizado.

**Para qué sirve:** Complementa los diagramas C4 con una vista centrada en los datos en lugar de las aplicaciones. Responde: "¿de dónde vienen los datos?", "¿dónde se almacenan?", "¿quién los consume?", "¿cómo se transforman?". Es especialmente útil para diseñar la capa de datos, planificar migraciones, y entender implicaciones de seguridad (¿dónde viven los datos sensibles?).

**Inputs requeridos:**
- `3B.1.3` Container Diagram — contenedores que procesan/almacenan datos
- `3B.1.6` Integration Points — fuentes y destinos externos de datos
- `2.3.4` Detailed Use Cases — flujos funcionales que generan datos
- `2.5.1` Business Rules Document — reglas que transforman datos

**Dependencias (predecessors):**
- `3B.1.3` Container Diagram *(obligatorio)* — contenedores de procesamiento y almacenamiento
- `3B.1.6` Integration Points *(obligatorio)* — fuentes externas de datos
- `2.3.4` Detailed Use Cases *(recomendado)* — flujos principales

**Habilita (successors):**
- `3B.3.1` ERD Complete — entidades identificadas en los flujos
- `3B.3.5` Data Dictionary — campos de datos documentados
- `3B.5.3` Main Business Flows — secuencias basadas en flujos de datos
- `3B.7.4` Data Protection Plan — datos sensibles identificados en los flujos
- `3B.8.7` Backup Strategy — data stores identificados

**Audiencia:**
- **Solution Architect** — validación de la coherencia del flujo
- **Database Engineer** — entiende qué datos almacenar y de dónde vienen
- **Backend Developer** — entiende las transformaciones de datos
- **Security Engineer** — identifica dónde viven datos sensibles (PII, PCI)
- **Data Engineer** — si hay pipeline de datos o ETL
- **Compliance** — flujo de datos personales para GDPR/CCPA

**Secciones esperadas:**
1. DFD Level 0 (contexto — sistema como proceso central con fuentes y destinos)
2. DFD Level 1 (procesos internos principales con data stores)
3. Por cada flujo principal:
   - Origen del dato (user, API, feed, scheduled)
   - Transformaciones (validación, normalización, enriquecimiento, cálculo)
   - Almacenamiento (qué DB, qué tabla, qué cache)
   - Consumo (UI, report, API response, export)
4. Datos sensibles marcados (PII, financieros, médicos)
5. Flujos sincrónicos vs asincrónicos diferenciados
6. Data retention (cuánto tiempo se guardan los datos)

**Criterio de completitud:**
- [ ] DFD cubre los 3-5 flujos de datos principales del sistema
- [ ] Origen, procesamiento, almacenamiento y consumo documentados por flujo
- [ ] Datos sensibles identificados y marcados
- [ ] Flujos sync vs async diferenciados
- [ ] Data stores identificados con tecnología (PostgreSQL, Redis, S3, etc.)
- [ ] Consistente con Container Diagram e Integration Points
- [ ] Revisado por Database Engineer y Security Engineer

**Anti-patrones:**
- ❌ **DFD sin data stores:** Mostrar procesos y flujos pero no dónde se almacenan los datos — falta la mitad de la historia.
- ❌ **Datos sensibles no marcados:** PII, datos financieros, o de salud fluyendo sin señalizar — compliance risk.
- ❌ **Solo happy path:** Documentar el flujo cuando todo sale bien pero no el flujo de errores, reintentos, o dead-letter queues.
- ❌ **DFD como organigrama:** Mostrar jerarquía de equipos en lugar de flujo de datos — confunde dos cosas distintas.

**Template:** `phases/03B-design-technical/deliverables/data-flow-diagram.mmd` *(pendiente)*

---

## Tabla resumen de ejecutores — Fase 3B.1 Solution Architecture

| Deliverable | Responsable | Ejecuta | Delegable VTT |
|-------------|-------------|---------|---------------|
| 3B.1.1 Architecture Document | Solution Architect | Solution Architect | 🔶 Parcial — puede estructurar y documentar decisiones ya tomadas, no puede tomarlas |
| 3B.1.2 System Context Diagram | Solution Architect | Solution Architect | ✅ — puede generar diagrama C4 L1 en Mermaid/PlantUML a partir de descripción |
| 3B.1.3 Container Diagram | Solution Architect | Solution Architect | ✅ — puede generar diagrama C4 L2 en Mermaid/PlantUML a partir de descripción |
| 3B.1.4 Component Diagram | Solution Architect | Solution Architect / Tech Lead | 🔶 Parcial — puede generar diagrama, pero descomposición modular requiere juicio |
| 3B.1.5 Technology Stack | Solution Architect | Solution Architect / Tech Lead | 🔶 Parcial — puede documentar y comparar opciones, no puede elegir el stack |
| 3B.1.6 Integration Points | Solution Architect | Solution Architect / Backend Developer | ✅ — puede documentar integraciones en formato estándar con toda la info |
| 3B.1.7 Data Flow Diagram | Solution Architect | Solution Architect | ✅ — puede generar DFDs en Mermaid a partir de descripción textual |

---

## Siguiente archivo

**Próximo:** `DICCIONARIO_FASE_03B_02_CODE_ARCHITECTURE.md` — 6 deliverables (3B.2.1 a 3B.2.6)
