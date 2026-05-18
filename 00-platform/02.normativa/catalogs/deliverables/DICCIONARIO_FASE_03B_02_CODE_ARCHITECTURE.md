# DICCIONARIO DE DELIVERABLES — FASE 3B.2: CODE ARCHITECTURE

**Versión:** 1.0  
**Fecha:** 2026-05-14  
**Fase:** 3B — Design Technical  
**Subfase:** 3B.2 — Code Architecture  
**Total deliverables:** 6  
**Responsable de subfase:** Tech Lead  
**Aprueba:** Solution Architect

---

## Contexto de la subfase

Code Architecture traduce las decisiones de Solution Architecture (3B.1) al nivel de código: cómo se organizan los archivos, qué estándares se siguen, qué patrones de diseño se usan, cómo se nombran las cosas, y cómo se manejan los errores. Es la diferencia entre un codebase navegable y mantenible, y un spaghetti code donde nadie encuentra nada. Estas decisiones se toman una vez y condicionan toda la vida del proyecto.

**Prerequisitos de subfase:**
- Solution Architecture definida (3B.1)
- Technology Stack elegido (3B.1.5)
- Equipo de desarrollo identificado (para adaptar estándares a su experiencia)

**Entrega de subfase:**
- Estándares de código, estructura de carpetas, patrones, y convenciones documentadas y listas para aplicar desde el primer commit

---

### 3B.2.1 Folder Structure

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.2 Code Architecture |
| **Responsable** | Tech Lead |
| **Ejecuta** | Tech Lead |
| **Aprueba** | Solution Architect |
| **Formato** | Documento (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5-1 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere experiencia con el framework elegido y sus convenciones de organización de código. Debe entender trade-offs entre feature-based vs layer-based organization y cómo escala cada approach.  
En VTT: un agente puede generar la folder structure completa con tree diagram y descripción de cada carpeta, basándose en el framework elegido y patrones estándar (e.g., Next.js app router, NestJS modules, Django apps). Es altamente delegable. Necesita brief con: framework/tech stack, approach de organización (feature-based vs layer-based), módulos/features del producto, y convenciones del equipo.

**Qué es:** Definición de la estructura de directorios del proyecto: cómo se organizan carpetas de código fuente, tests, configuración, assets, documentación, y scripts. Incluye el tree completo con descripción del propósito de cada directorio, y reglas sobre dónde va cada tipo de archivo.

**Para qué sirve:** Un developer nuevo debería poder navegar el codebase en 10 minutos leyendo este documento. Evita que cada developer invente su propia estructura ("yo pongo los helpers en /utils, yo en /lib, yo en /shared"). Garantiza que el codebase escala sin convertirse en un laberinto cuando crece de 10 a 200 archivos.

**Inputs requeridos:**
- `3B.1.5` Technology Stack — framework define la estructura base
- `3B.1.4` Component Diagram — módulos que se mapean a carpetas
- `3B.2.3` Design Patterns — patrones definen layers/estructura
- Convenciones del framework elegido (Next.js, NestJS, Django, etc.)

**Dependencias (predecessors):**
- `3B.1.5` Technology Stack *(obligatorio)* — framework condiciona la estructura
- `3B.1.4` Component Diagram *(obligatorio)* — módulos se mapean a carpetas
- `3B.2.3` Design Patterns *(recomendado)* — patterns definen layers

**Habilita (successors):**
- `4.1.2` Repository Setup — repo creado con la estructura definida
- `4.1.3` Project Scaffolding — scaffolding sigue la estructura
- `4.3.1` Backend Modules — developers saben dónde crear módulos
- `4.4.1` Components — developers saben dónde crear componentes

**Audiencia:**
- **Todo el equipo de desarrollo** — referencia diaria
- **Tech Lead** — enforcement de la estructura en code reviews
- **DevOps Lead** — paths de build, test, y deploy

**Secciones esperadas:**
1. Tree diagram completo del proyecto
2. Descripción de cada directorio raíz (src/, tests/, config/, docs/, scripts/)
3. Estructura del código fuente (src/) con subdirectorios por módulo o layer
4. Estructura de tests (mirror de src/ o colocated)
5. Reglas de organización (dónde van: componentes, servicios, utils, types, constants)
6. Archivos de configuración raíz (.env, tsconfig, eslint, prettier, docker)
7. Ejemplos de feature completa (cómo se ve un módulo/feature con todos sus archivos)
8. Reglas de lo que NO va en cada carpeta

**Criterio de completitud:**
- [ ] Tree diagram completo con al menos 3 niveles de profundidad
- [ ] Cada directorio tiene descripción de propósito
- [ ] Reglas claras de dónde va cada tipo de archivo
- [ ] Al menos un ejemplo de feature/módulo completo
- [ ] Estructura alineada al framework elegido
- [ ] Estructura soporta crecimiento (no se rompe al agregar features)
- [ ] Aprobado por Solution Architect

**Anti-patrones:**
- ❌ **Carpeta "utils" cajón de sastre:** `/utils` con 47 archivos sin relación — señal de falta de diseño modular.
- ❌ **Estructura ultra-profunda:** `src/modules/auth/services/implementations/v2/AuthService.ts` — 6 niveles es excesivo.
- ❌ **Estructura que no escala:** Funciona con 5 archivos, colapsa con 50 — no anticipó crecimiento.
- ❌ **Ignorar convenciones del framework:** Inventar estructura custom cuando el framework tiene una convención probada — confunde a developers con experiencia en el framework.

**Template:** `phases/03B-design-technical/deliverables/folder-structure.md` *(pendiente)*

---

### 3B.2.2 Coding Standards

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.2 Code Architecture |
| **Responsable** | Tech Lead |
| **Ejecuta** | Tech Lead |
| **Aprueba** | Solution Architect |
| **Formato** | Documento (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Una vez + refinamientos menores |

**Perfil de ejecución:** Requiere experiencia con el lenguaje/framework y opiniones formadas sobre readability, maintainability, y best practices. Debe balancear rigor con pragmatismo — estándares demasiado estrictos no se adoptan.  
En VTT: un agente puede generar un documento de coding standards basado en guías comunitarias (Airbnb JS, Google Python, etc.) customizado al stack del proyecto. Puede también generar las configuraciones de linting/formatting (ESLint, Prettier, Black). Es altamente delegable. Necesita brief con: lenguaje/framework, guía base a adoptar (Airbnb, Standard, Google), customizaciones del equipo, y nivel de strictness deseado.

**Qué es:** Documento que define las reglas de escritura de código: estilo (indentation, brackets, semicolons), convenciones (variable naming, function length, file size), patterns requeridos (inmutabilidad, functional vs OOP, error handling), y anti-patterns prohibidos. Incluye las configuraciones de herramientas de enforcement (ESLint, Prettier, Ruff, etc.).

**Para qué sirve:** Garantiza que todo el código del proyecto se lee como si lo hubiera escrito una sola persona. Elimina debates de estilo en code reviews ("¿tabs o spaces?" ya está decidido). Reduce bugs al prohibir patterns peligrosos (any, eval, implicit type coercion). Las herramientas de enforcement automatizan el compliance.

**Inputs requeridos:**
- `3B.1.5` Technology Stack — lenguaje y framework definen las reglas
- Guía de estilo base a adoptar (Airbnb, Google, Standard)
- Preferencias del equipo
- Configuración de CI/CD para enforcement

**Dependencias (predecessors):**
- `3B.1.5` Technology Stack *(obligatorio)* — lenguaje define las reglas aplicables
- `3B.2.5` Naming Conventions *(obligatorio)* — naming es parte de los standards

**Habilita (successors):**
- `4.1.3` Project Scaffolding — linting y formatting configurados desde el inicio
- `4.1.4` CI/CD Pipeline — linting como step del pipeline
- Todo el código del proyecto — developers aplican los standards

**Audiencia:**
- **Todo el equipo de desarrollo** — referencia diaria
- **Tech Lead** — enforcement en code reviews
- **QA Automation** — configuración de linting en CI

**Secciones esperadas:**
1. Guía base adoptada (e.g., "Airbnb JavaScript con customizaciones")
2. Reglas de estilo (indentation, line length, quotes, semicolons, trailing commas)
3. Reglas de naming (ver 3B.2.5 Naming Conventions — reference cruzada)
4. Reglas de funciones (max parameters, max lines, single responsibility)
5. Reglas de tipos (TypeScript strictness, avoid `any`, prefer interfaces)
6. Reglas de imports (order, aliases, absolute vs relative)
7. Reglas de comments (JSDoc, cuándo comentar, cuándo no)
8. Reglas de error handling (try/catch patterns, custom errors)
9. Reglas de testing (naming de tests, arrange-act-assert, mocking)
10. Patterns prohibidos (lista de anti-patterns con justificación)
11. Configuración de herramientas (ESLint config, Prettier config, pre-commit hooks)
12. Proceso de excepciones (cómo y cuándo se permite violar una regla)

**Criterio de completitud:**
- [ ] Guía base adoptada y customizaciones documentadas
- [ ] Configuración de ESLint/Prettier (o equivalente) incluida y funcional
- [ ] Pre-commit hooks configurados
- [ ] Reglas de funciones, tipos, imports, y comments documentadas
- [ ] Anti-patterns listados con justificación
- [ ] Proceso de excepciones definido (no es una ley inflexible)
- [ ] Validado con al menos 2 developers del equipo

**Anti-patrones:**
- ❌ **Standards sin tooling:** Reglas escritas que nadie enforce — se violan en el segundo commit.
- ❌ **Demasiadas reglas custom:** 200 reglas que nadie recuerda — adoptar una guía estándar y customizar mínimamente.
- ❌ **Standards religiosos:** Debates infinitos sobre tabs vs spaces — elegir y seguir adelante.
- ❌ **Sin excepciones:** Reglas absolutas sin proceso para excepciones justificadas — los developers buscan workarounds.
- ❌ **Standards copiados de otro proyecto:** Reglas de un proyecto Python en un proyecto TypeScript — no transferibles.

**Template:** `phases/03B-design-technical/deliverables/coding-standards.md` *(pendiente)*

---

### 3B.2.3 Design Patterns

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.2 Code Architecture |
| **Responsable** | Tech Lead |
| **Ejecuta** | Tech Lead / Solution Architect |
| **Aprueba** | Solution Architect |
| **Formato** | Documento (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Una vez + adiciones por feature compleja |

**Perfil de ejecución:** Requiere conocimiento profundo de patrones de diseño (GoF, enterprise patterns, domain-driven design) y juicio para elegir cuáles aplicar al contexto del proyecto. No todos los patterns son apropiados para todos los proyectos.  
En VTT: un agente puede documentar los design patterns seleccionados con ejemplos de código en el lenguaje del proyecto, diagramas UML, y justificación. Puede también generar code templates/snippets para cada pattern. NO puede decidir qué patterns usar — esa decisión requiere experiencia del Tech Lead. Necesita brief con: lista de patterns seleccionados, justificación, y contexto donde se aplican.

**Qué es:** Documento que define los design patterns que el equipo debe usar en el proyecto: patrones arquitectónicos (Repository, Service Layer, CQRS), patrones creacionales (Factory, Builder), patrones estructurales (Adapter, Decorator), y patrones de comportamiento (Strategy, Observer). Para cada pattern: cuándo usarlo, ejemplo de código en el stack del proyecto, y cuándo NO usarlo.

**Para qué sirve:** Estandariza cómo se resuelven problemas recurrentes de diseño de software. Sin esto, cada developer resuelve el mismo problema de forma diferente (uno usa Repository, otro consulta la DB directo en el controller, otro crea un helper). Los patterns crean vocabulario compartido: "eso es un Adapter" es más eficiente que explicar la solución completa.

**Inputs requeridos:**
- `3B.1.1` Architecture Document — decisiones arquitectónicas
- `3B.1.4` Component Diagram — estructura modular
- `3B.1.5` Technology Stack — patterns dependen del lenguaje/framework
- `2.3.4` Detailed Use Cases — complejidad de los casos de uso

**Dependencias (predecessors):**
- `3B.1.1` Architecture Document *(obligatorio)* — contexto arquitectónico
- `3B.1.4` Component Diagram *(obligatorio)* — estructura que los patterns implementan
- `3B.1.5` Technology Stack *(obligatorio)* — patterns dependen del lenguaje

**Habilita (successors):**
- `3B.2.1` Folder Structure — estructura refleja los layers de los patterns
- `3B.2.6` Error Handling Strategy — patterns de error handling
- `4.3.1` Backend Modules — developers implementan usando los patterns
- `4.4.1` Components — frontend patterns aplicados

**Audiencia:**
- **Todo el equipo de desarrollo** — referencia al implementar funcionalidad
- **Tech Lead** — enforcement en code reviews
- **Solution Architect** — validación de coherencia con la arquitectura

**Secciones esperadas:**
1. Patrones arquitectónicos (Repository, Service Layer, Unit of Work, CQRS)
2. Patrones creacionales seleccionados (Factory, Builder, Singleton justificado)
3. Patrones estructurales seleccionados (Adapter, Decorator, Facade)
4. Patrones de comportamiento seleccionados (Strategy, Observer, Command)
5. Por cada pattern:
   - Nombre y descripción breve
   - Cuándo usarlo (contexto y triggers)
   - Cuándo NO usarlo (over-engineering scenarios)
   - Ejemplo de código en el stack del proyecto
   - Diagrama UML simplificado
6. Patterns del framework (e.g., React patterns: hooks, compound components, render props)
7. Anti-patterns explícitamente prohibidos (God Object, Spaghetti, Anemic Domain Model)
8. Decision tree (guía para elegir qué pattern aplicar en cada situación)

**Criterio de completitud:**
- [ ] Al menos 5 patterns principales documentados con ejemplos de código
- [ ] Cada pattern tiene "cuándo usar" y "cuándo NO usar"
- [ ] Ejemplos de código en el lenguaje/framework del proyecto
- [ ] Anti-patterns documentados con justificación
- [ ] Decision tree o guía de selección incluida
- [ ] Validado por el equipo de desarrollo (no solo el Tech Lead)

**Anti-patrones:**
- ❌ **Pattern catalog genérico:** Copiar los 23 patterns de GoF sin filtrar cuáles aplican — nadie lee un catálogo de 23 patterns.
- ❌ **Patterns sin ejemplo en el stack:** Explicar Repository con Java cuando el proyecto es Python — no es consumible.
- ❌ **Pattern por Pattern's sake:** Usar Strategy pattern para una sola estrategia — over-engineering.
- ❌ **Sin "cuándo NO usar":** Solo documentar cuándo aplicar — los developers aplican el pattern everywhere.
- ❌ **Anemic Domain Model sin saberlo:** Definir Services que tienen toda la lógica y Entities que son solo data bags — anti-DDD accidental.

**Template:** `phases/03B-design-technical/deliverables/design-patterns.md` *(pendiente)*

---

### 3B.2.4 Module Dependencies

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.2 Code Architecture |
| **Responsable** | Tech Lead |
| **Ejecuta** | Tech Lead |
| **Aprueba** | Solution Architect |
| **Formato** | Diagrama |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5-1 día |
| **Frecuencia** | Una vez + actualizaciones cuando se agregan módulos |

**Perfil de ejecución:** Requiere capacidad de análisis de dependencias y entendimiento de acoplamiento vs cohesión. Debe poder identificar dependencias circulares y proponer soluciones.  
En VTT: un agente puede generar el diagrama de dependencias entre módulos en Mermaid a partir de la lista de módulos y sus relaciones. También puede analizar imports de un codebase existente y generar el diagrama automáticamente. Es altamente delegable. Necesita brief con: lista de módulos, qué módulo importa de cuál, y dirección permitida de dependencia (e.g., "services pueden importar repositories pero no al revés").

**Qué es:** Diagrama que muestra las dependencias entre módulos/packages del codebase: qué módulo importa de cuál, en qué dirección fluyen las dependencias, y cuáles son los módulos core vs periféricos. Incluye reglas de dependencia (e.g., "domain no depende de infrastructure", "controllers dependen de services, nunca al revés").

**Para qué sirve:** Previene dependencias circulares, god modules, y acoplamiento excesivo antes de que ocurran en el código. Las reglas de dependencia se pueden enforcar con herramientas (eslint-plugin-boundaries, NestJS module system). Visualizar dependencias ayuda a planificar el orden de desarrollo y los impactos de cambios.

**Inputs requeridos:**
- `3B.1.4` Component Diagram — componentes que se mapean a módulos
- `3B.2.1` Folder Structure — carpetas que representan módulos
- `3B.2.3` Design Patterns — layers que definen dirección de dependencia

**Dependencias (predecessors):**
- `3B.1.4` Component Diagram *(obligatorio)* — módulos identificados
- `3B.2.1` Folder Structure *(obligatorio)* — organización de módulos
- `3B.2.3` Design Patterns *(recomendado)* — layers definen reglas de dependencia

**Habilita (successors):**
- `3B.9.7` Dependencies Map — dependencias técnicas de tareas
- `4.1.3` Project Scaffolding — módulos creados con dependencias correctas
- `4.3.1` Backend Modules — implementación respetando dependencias

**Audiencia:**
- **Tech Lead** — enforcement de reglas de dependencia en code reviews
- **Backend Developer** — entiende qué puede importar y qué no
- **Frontend Developer** — entiende la estructura de dependencias del frontend
- **Solution Architect** — validación de separación de concerns

**Secciones esperadas:**
1. Diagrama de dependencias entre módulos (directed graph)
2. Leyenda (tipos de dependencia: directa, indirecta, opcional)
3. Reglas de dependencia (tabla: módulo, puede depender de, NO puede depender de)
4. Módulos core (sin dependencias externas — domain, shared)
5. Módulos periféricos (dependen de core — infrastructure, adapters)
6. Análisis de acoplamiento (módulos más acoplados, riesgos)
7. Estrategia para dependency inversion donde se necesite

**Criterio de completitud:**
- [ ] Todos los módulos del proyecto representados
- [ ] Dirección de dependencia clara en cada flecha
- [ ] Reglas de dependencia explícitas (qué puede importar de qué)
- [ ] Sin dependencias circulares
- [ ] Módulos core identificados
- [ ] Reglas enforceable con tooling (eslint-plugin-boundaries o similar)

**Anti-patrones:**
- ❌ **Dependencias circulares:** A → B → C → A — señal de boundaries mal definidos; se rompe al refactorizar.
- ❌ **God module:** Un módulo del que todos dependen y que depende de todos — cuello de botella para cambios.
- ❌ **Domain depende de infrastructure:** El modelo de dominio importa el ORM o el framework — inversión de dependencia violada.
- ❌ **Sin reglas explícitas:** "Cada quien importa lo que necesita" — en 3 meses, spaghetti de dependencias.

**Template:** `phases/03B-design-technical/deliverables/module-dependencies.mmd` *(pendiente)*

---

### 3B.2.5 Naming Conventions

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.2 Code Architecture |
| **Responsable** | Tech Lead |
| **Ejecuta** | Tech Lead |
| **Aprueba** | Solution Architect |
| **Formato** | Documento (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere conocimiento de convenciones del lenguaje (camelCase en JS, snake_case en Python, PascalCase en C#) y experiencia en naming semántico (nombres que comunican intención).  
En VTT: un agente puede generar el documento completo de naming conventions basándose en las convenciones del lenguaje/framework y customizaciones del equipo. Es altamente delegable. Necesita brief con: lenguaje/framework, convenciones base del ecosistema, y customizaciones específicas del proyecto (prefijos, sufijos, acrónimos).

**Qué es:** Documento que define las convenciones de nombres para todo en el codebase: archivos, carpetas, variables, funciones, clases, interfaces, tipos, constantes, enums, tablas de BD, columnas, endpoints de API, branches de Git, y commits. Para cada categoría: case style (camelCase, PascalCase, snake_case, kebab-case), prefijos/sufijos, y ejemplos.

**Para qué sirve:** Naming es comunicación. Un buen nombre elimina la necesidad de leer la implementación para entender qué hace algo. Las convenciones de naming consistentes hacen que el codebase se lea como un todo coherente y que la búsqueda (Cmd+Shift+F) funcione de forma predecible.

**Inputs requeridos:**
- `3B.1.5` Technology Stack — lenguaje define las convenciones base
- Convenciones del ecosistema (e.g., React: PascalCase para componentes)
- `2.5.7` Business Glossary — términos de dominio estandarizados

**Dependencias (predecessors):**
- `3B.1.5` Technology Stack *(obligatorio)* — lenguaje define las convenciones
- `2.5.7` Business Glossary *(recomendado)* — vocabulario de dominio estandarizado

**Habilita (successors):**
- `3B.2.2` Coding Standards — naming es parte de los standards
- `3B.3.3` Table Specifications — naming de tablas y columnas
- `3B.4.2` Endpoints List — naming de endpoints
- Todo el código del proyecto

**Audiencia:**
- **Todo el equipo de desarrollo** — referencia constante
- **Tech Lead** — enforcement en code reviews
- **Database Engineer** — naming de BD

**Secciones esperadas:**
1. Case styles overview (camelCase, PascalCase, snake_case, kebab-case, SCREAMING_CASE)
2. Archivos y carpetas (case, singular/plural, extensiones)
3. Variables y constantes (case, prefijos para boolean: is/has/should, constantes en SCREAMING_CASE)
4. Funciones y métodos (case, verbos de acción: get, set, create, update, delete, find, validate, format)
5. Clases, interfaces, tipos (case, prefijos/sufijos: IService, UserDTO, CreateUserInput)
6. Componentes React/Vue (PascalCase, naming semántico)
7. Tablas y columnas de BD (case, singular/plural, foreign keys, timestamps)
8. Endpoints de API (kebab-case, plural resources, nested resources)
9. Branches de Git (feature/, bugfix/, hotfix/, release/)
10. Commits (conventional commits: feat, fix, docs, refactor)
11. Variables de entorno (SCREAMING_CASE, prefijos por servicio)
12. Glosario de términos de dominio (término → nombre en código)

**Criterio de completitud:**
- [ ] Todas las categorías cubiertas (variables, funciones, clases, archivos, BD, API, Git)
- [ ] Case style definido para cada categoría
- [ ] Al menos 3 ejemplos por categoría (bueno, malo, corrección)
- [ ] Glosario de dominio incluido
- [ ] Alineado con convenciones del lenguaje/framework
- [ ] Configurable en linting donde sea posible

**Anti-patrones:**
- ❌ **Naming inconsistente:** `getUserById`, `fetch_user`, `findUser`, `loadUserData` para la misma operación — 4 convenciones en un proyecto.
- ❌ **Acrónimos ambiguos:** `usr`, `mgr`, `btn`, `dlg` — ahorra 3 caracteres pero pierde claridad.
- ❌ **Nombres genéricos:** `data`, `info`, `temp`, `result`, `item` — no comunican intención.
- ❌ **Hungarian notation en 2026:** `strName`, `intAge`, `boolIsActive` — el sistema de tipos ya comunica el tipo.
- ❌ **Inconsistencia entre layers:** `users` en la API, `user` en la BD, `Users` en el modelo, `UserEntity` en el DTO — ¿cuál es el canónico?

**Template:** `phases/03B-design-technical/deliverables/naming-conventions.md` *(pendiente)*

---

### 3B.2.6 Error Handling Strategy

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.2 Code Architecture |
| **Responsable** | Tech Lead |
| **Ejecuta** | Tech Lead / Backend Developer |
| **Aprueba** | Solution Architect |
| **Formato** | Documento (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere experiencia en error handling patterns: custom exceptions, error boundaries, global error handlers, structured logging de errores, y cómo comunicar errores al usuario final. Debe entender la diferencia entre errores operacionales (esperados) y errores programáticos (bugs).  
En VTT: un agente puede generar la estrategia de error handling con: jerarquía de custom exceptions, global error handler middleware, error response format (para API), error boundary patterns (para frontend), y logging templates. Es bastante delegable. Necesita brief con: stack tecnológico, formato de error response deseado, niveles de severidad, y herramienta de logging/monitoring.

**Qué es:** Documento que define cómo el sistema maneja errores en todas las capas: errores de validación (input inválido), errores de negocio (operación no permitida), errores de infraestructura (DB caída, servicio externo no disponible), y errores inesperados (bugs). Define: jerarquía de excepciones custom, formato estándar de error response, estrategia de logging, error boundaries en frontend, retry policies, y qué información mostrar al usuario vs qué loggear internamente.

**Para qué sirve:** Sin una estrategia, cada developer maneja errores a su manera: unos usan try/catch, otros ignoran errores, otros lanzan strings genéricos. El resultado es un sistema donde los errores se pierden, los logs son inútiles, y el usuario ve "Something went wrong" sin contexto. La estrategia estandariza el manejo para que los errores sean informativos, logueados, y manejados gracefully.

**Inputs requeridos:**
- `3B.1.5` Technology Stack — lenguaje y framework definen los mecanismos
- `3B.4.5` Error Codes — códigos de error estándar de la API
- `3B.7.10` Security Logging — qué errores tienen implicaciones de seguridad
- `3B.8.11` Monitoring Strategy — cómo se alertan errores

**Dependencias (predecessors):**
- `3B.1.5` Technology Stack *(obligatorio)* — mecanismos de error del lenguaje
- `3B.2.3` Design Patterns *(recomendado)* — patterns de error handling
- `3B.4.5` Error Codes *(recomendado)* — códigos estándar para API responses

**Habilita (successors):**
- `4.3.1` Backend Modules — developers implementan error handling estándar
- `4.4.1` Components — frontend error boundaries implementados
- `4.3.7` Middleware — error handling middleware
- `4.5.3` Error Handling Tests — tests de error handling

**Audiencia:**
- **Backend Developer** — implementación de error handling en services y controllers
- **Frontend Developer** — error boundaries y manejo de error responses
- **Tech Lead** — enforcement en code reviews
- **DevOps Lead** — configuración de alerting basado en errores
- **QA Engineer** — testing de escenarios de error

**Secciones esperadas:**
1. Clasificación de errores (operacionales vs programáticos, por severidad)
2. Jerarquía de excepciones custom (AppError → ValidationError, BusinessError, InfraError, etc.)
3. Formato estándar de error response API (code, message, details, requestId)
4. HTTP status codes mapping (qué error → qué status code)
5. Global error handler (middleware/interceptor pattern)
6. Error handling por capa (controller, service, repository, integration)
7. Frontend error handling (error boundaries, toast notifications, error pages)
8. Retry policies (qué errores reintentar, backoff strategy, max retries)
9. Logging de errores (qué loggear, nivel de severidad, structured logging format)
10. Error monitoring y alerting (thresholds, escalation)
11. Información al usuario (qué mostrar vs qué ocultar — nunca stack traces)
12. Dead-letter queues para errores en procesamiento asíncrono

**Criterio de completitud:**
- [ ] Clasificación de errores definida
- [ ] Jerarquía de excepciones custom con al menos 4 tipos
- [ ] Formato estándar de error response definido
- [ ] HTTP status codes mapeados a tipos de error
- [ ] Global error handler documentado con ejemplo de código
- [ ] Frontend error handling strategy definida
- [ ] Logging de errores con formato y niveles
- [ ] Retry policy para errores transientes
- [ ] Nunca se expone stack trace ni info sensible al usuario

**Anti-patrones:**
- ❌ **Catch-all silencioso:** `catch (e) { /* ignore */ }` — errores desaparecen, bugs se acumulan en silencio.
- ❌ **Error strings:** `throw "User not found"` en lugar de excepciones tipadas — imposible de manejar programáticamente.
- ❌ **Stack traces al usuario:** Error response con `stack: "Error at line 47 of UserService..."` — información sensible expuesta.
- ❌ **Un solo catch para todo:** Manejar ValidationError igual que DatabaseError — respuestas incorrectas y logging inadecuado.
- ❌ **Sin retry para errores transientes:** Network timeout = error fatal, cuando un retry lo resolvería.
- ❌ **Logs sin contexto:** `Error: something failed` sin requestId, userId, ni operación — imposible de diagnosticar.

**Template:** `phases/03B-design-technical/deliverables/error-handling-strategy.md` *(pendiente)*

---

## Tabla resumen de ejecutores — Fase 3B.2 Code Architecture

| Deliverable | Responsable | Ejecuta | Delegable VTT |
|-------------|-------------|---------|---------------|
| 3B.2.1 Folder Structure | Tech Lead | Tech Lead | ✅ — puede generar estructura completa basada en framework y módulos |
| 3B.2.2 Coding Standards | Tech Lead | Tech Lead | ✅ — puede generar documento y configuraciones de linting/formatting |
| 3B.2.3 Design Patterns | Tech Lead | Tech Lead / Solution Architect | 🔶 Parcial — puede documentar y ejemplificar patterns seleccionados, no puede elegirlos |
| 3B.2.4 Module Dependencies | Tech Lead | Tech Lead | ✅ — puede generar diagrama de dependencias en Mermaid |
| 3B.2.5 Naming Conventions | Tech Lead | Tech Lead | ✅ — puede generar documento completo basado en convenciones del ecosistema |
| 3B.2.6 Error Handling Strategy | Tech Lead | Tech Lead / Backend Developer | ✅ — puede generar estrategia completa con código de ejemplo |

---

## Siguiente archivo

**Próximo:** `DICCIONARIO_FASE_03B_03_DATABASE_DESIGN.md` — 8 deliverables (3B.3.1 a 3B.3.8)
