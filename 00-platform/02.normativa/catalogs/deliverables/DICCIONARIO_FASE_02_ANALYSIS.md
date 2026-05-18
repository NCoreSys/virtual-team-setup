# DICCIONARIO DE DELIVERABLES — FASE 2: ANALYSIS

**Versión:** 1.1.0  
**Fecha:** 2026-05-14  
**Total deliverables:** 47  
**Objetivo de fase:** Definir QUÉ debe hacer el sistema en detalle.  
**Duración típica:** 2-4 semanas  
**Criterio de salida de fase:** Product Owner aprueba requisitos completos.

---

## Roles involucrados en esta fase

| Rol | Nivel | Participa en |
|-----|-------|-------------|
| Product Manager (PM) | ●●● Principal | 2.4 |
| Systems Analyst (SA) | ●●● Principal | 2.1, 2.2, 2.3, 2.5, 2.8 |
| QA Lead | ●●● Principal | 2.7, 2.8 |
| Product Owner (PO) | ●● Activo | Aprueba en 2.1, 2.3, 2.4, 2.5, 2.7 |
| UX Designer | ●● Activo | 2.6 |
| Tech Lead (TL) | ● Participa | 2.2, 2.5 |

---

# 2.1 FUNCTIONAL REQUIREMENTS

**Responsable:** Systems Analyst  
**Aprueba:** Product Owner  
**Objetivo de subfase:** Documentar qué debe hacer el sistema.

---

### 2.1.1 SRS Document

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.1 Functional Requirements |
| **Responsable** | Systems Analyst |
| **Ejecuta** | Systems Analyst |
| **Aprueba** | Product Owner |
| **Formato** | PDF/MD |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 3-5 días |
| **Frecuencia** | Una vez + refinamiento por sprint |

**Perfil de ejecución:** El SA lo produce directamente — es su deliverable central. Requiere capacidad de traducir necesidades de negocio a especificaciones técnicas sin ambigüedad. En VTT: un agente SA puede generar un SRS completo a partir del MVP Definition, use cases y user stories, pero debe ser validado por el SA humano y aprobado por el PO.

**Qué es:** Software Requirements Specification — documento formal que describe TODAS las funcionalidades que el sistema debe tener. Es el contrato entre producto (qué quiere) y desarrollo (qué construye).

**Para qué sirve:** Elimina ambigüedad entre lo que el PO imagina y lo que el developer construye. Sin SRS, cada persona interpreta los requisitos a su manera.

**Inputs requeridos:**
- `1.2.4` MVP Definition — alcance de la primera versión
- `1.2.2` In-Scope — funcionalidades incluidas
- `0.3.2` User Pain Points — dolores a resolver
- `0.4.1` Value Proposition Canvas — valor a entregar
- Entrevistas con PO y PM para clarificar intención

**Dependencias (predecessors):**
- `1.2.4` MVP Definition *(obligatorio)*
- `1.2.2` In-Scope *(obligatorio)*
- `0.3.1` Problem Statement *(obligatorio)*

**Habilita (successors):**
- `2.1.2` Requirements List — lista derivada del SRS
- `2.1.3` Priority Matrix — priorización de requisitos
- `2.3.1` Use Case Document — use cases implementan los requisitos
- `3B.1.1` System Architecture — la arquitectura soporta los requisitos
- `5.1.1` Test Strategy — los tests validan los requisitos

**Audiencia:**
- **Tech Lead** — para planear la implementación
- **Developers** — para entender qué construir
- **QA Lead** — para diseñar tests
- **Product Owner** — para validar que se entendió

**Secciones esperadas:**
1. Introducción y propósito del sistema
2. Alcance del sistema
3. Requisitos funcionales organizados por módulo/feature
4. Requisitos de interfaz de usuario
5. Requisitos de interfaces externas (APIs, integraciones)
6. Requisitos de datos
7. Restricciones y supuestos
8. Glosario de términos

**Criterio de completitud:**
- [ ] Cada requisito es testable (se puede verificar si se cumple o no)
- [ ] Cada requisito es único (no hay duplicados)
- [ ] Cada requisito es trazable (tiene ID único RF-XXX)
- [ ] No hay requisitos contradictorios
- [ ] PO ha aprobado

**Anti-patrones:**
- ❌ **Requisitos ambiguos:** "El sistema debe ser rápido" no es testable. "El sistema debe responder en <2 segundos" sí.
- ❌ **Requisitos de solución:** "Usar React para el frontend" no es un requisito funcional — es una decisión de implementación.
- ❌ **SRS monolítico:** Mejor organizar por módulo/feature que un documento lineal de 100 páginas.

**Template:** `_pm/templates/TEMPLATE_SRS.md` *(pendiente)*

---

### 2.1.2 Requirements List

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.1 Functional Requirements |
| **Responsable** | Systems Analyst |
| **Ejecuta** | Systems Analyst |
| **Aprueba** | Product Owner |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Con el SRS |

**Perfil de ejecución:** SA lo extrae del SRS. En VTT: altamente automatizable — un agente puede extraer la lista de requisitos de cualquier SRS en formato tabla.

**Qué es:** Lista numerada (RF-001, RF-002...) de todos los requisitos funcionales con descripción breve, módulo y prioridad.

**Para qué sirve:** Vista rápida de todos los requisitos. Más fácil de revisar que el SRS completo. Se usa para tracking de cobertura.

**Inputs requeridos:**
- `2.1.1` SRS Document

**Dependencias (predecessors):**
- `2.1.1` SRS Document *(obligatorio)*

**Habilita (successors):**
- `2.1.3` Priority Matrix
- `2.8.1` Traceability Matrix — mapeo RF a todo lo demás

**Secciones esperadas:**

| ID | Requisito | Módulo | Prioridad | Estado |
|----|----------|--------|-----------|--------|
| RF-001 | Descripción | Módulo | Must/Should/Could/Won't | Draft/Aprobado |

**Criterio de completitud:**
- [ ] Cada requisito del SRS tiene entrada en la lista
- [ ] IDs únicos y secuenciales
- [ ] Prioridad asignada

**Template:** Incluido dentro de `TEMPLATE_SRS.md`

---

### 2.1.3 Priority Matrix

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.1 Functional Requirements |
| **Responsable** | Systems Analyst |
| **Ejecuta** | Systems Analyst + Product Manager |
| **Aprueba** | Product Owner |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Por sprint |

**Perfil de ejecución:** SA estructura la matriz, PM aporta la prioridad de negocio. En VTT: un agente puede categorizar requisitos usando MoSCoW si el PM provee criterios de priorización.

**Qué es:** Priorización de requisitos usando framework MoSCoW (Must have, Should have, Could have, Won't have this time).

**Para qué sirve:** Define qué se construye primero. Los "Must" entran en el MVP, los "Should" en la siguiente iteración.

**Inputs requeridos:**
- `2.1.2` Requirements List
- `1.2.4` MVP Definition — qué es "Must"
- Input del PM sobre valor de negocio
- Input del TL sobre complejidad técnica

**Dependencias (predecessors):**
- `2.1.2` Requirements List *(obligatorio)*

**Habilita (successors):**
- `2.4.1` Product Backlog — prioridad informa el backlog
- Sprint planning

**Criterio de completitud:**
- [ ] Todos los requisitos categorizados en MoSCoW
- [ ] "Must" es alcanzable en el timeline
- [ ] PO aprueba la categorización

**Anti-patrones:**
- ❌ **Todo es "Must":** Si todo es prioridad 1, nada es prioridad 1.
- ❌ **Priorización sin TL:** La complejidad técnica afecta la viabilidad de un "Must."

**Template:** Incluido dentro de `TEMPLATE_SRS.md`

---

### 2.1.4 Feature List

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.1 Functional Requirements |
| **Responsable** | Systems Analyst |
| **Ejecuta** | Systems Analyst + Product Manager |
| **Aprueba** | Product Owner |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Con el SRS |

**Perfil de ejecución:** SA agrupa los requisitos en features, PM valida que las features alineen con el producto. En VTT: un agente puede agrupar requisitos por módulo/feature automáticamente si el naming convention es consistente.

**Qué es:** Lista de features por módulo — agrupación lógica de requisitos en capacidades de usuario.

**Para qué sirve:** Puente entre requisitos técnicos (RF-XXX) y lenguaje de producto (features). El PM habla de features, el developer de requisitos.

**Inputs requeridos:**
- `2.1.2` Requirements List
- `1.2.2` In-Scope

**Dependencias (predecessors):**
- `2.1.2` Requirements List *(obligatorio)*

**Habilita (successors):**
- `2.1.5` Functional Decomposition
- `2.4.4` Epics — features se convierten en epics

**Criterio de completitud:**
- [ ] Cada requisito está asignado a una feature
- [ ] Cada feature tiene descripción clara para usuario no-técnico
- [ ] Organizadas por módulo

**Template:** Incluido dentro de `TEMPLATE_SRS.md`

---

### 2.1.5 Functional Decomposition

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.1 Functional Requirements |
| **Responsable** | Systems Analyst |
| **Ejecuta** | Systems Analyst |
| **Aprueba** | Product Owner |
| **Formato** | Diagrama |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Con el SRS |

**Perfil de ejecución:** SA produce el diagrama de descomposición. En VTT: un agente puede generar un diagrama de descomposición funcional en Mermaid a partir de la feature list y los módulos.

**Qué es:** Diagrama jerárquico que descompone el sistema en subsistemas → módulos → funciones → subfunciones.

**Para qué sirve:** Visualiza la estructura funcional completa del sistema. Permite verificar que no faltan funciones y que la organización es lógica.

**Inputs requeridos:**
- `2.1.4` Feature List
- `2.1.2` Requirements List

**Dependencias (predecessors):**
- `2.1.4` Feature List *(obligatorio)*

**Habilita (successors):**
- `3B.1.1` System Architecture — la descomposición funcional informa los componentes
- `2.4.4` Epics — los módulos pueden mapearse a epics

**Criterio de completitud:**
- [ ] Todos los módulos y features representados
- [ ] Máximo 3-4 niveles de profundidad
- [ ] No hay funciones huérfanas (sin módulo)

**Template:** Incluido dentro de `TEMPLATE_SRS.md`

---

### 2.1.6 Requirements Approval

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.1 Functional Requirements |
| **Responsable** | Systems Analyst |
| **Ejecuta** | Product Owner |
| **Aprueba** | Product Owner |
| **Formato** | Sign-off |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Una vez + por cambio formal |

**Perfil de ejecución:** El PO revisa y firma la aprobación. El SA facilita la revisión. En VTT: un agente puede preparar un resumen ejecutivo del SRS para facilitar la revisión del PO, pero la aprobación es acto humano.

**Qué es:** Aprobación formal de los requisitos por parte del Product Owner. Gate de control antes de proceder a diseño y desarrollo.

**Para qué sirve:** Establece un baseline de requisitos aprobados. Cualquier cambio posterior es un "change request" formal.

**Inputs requeridos:**
- `2.1.1` SRS Document completo
- `2.1.3` Priority Matrix aprobada

**Dependencias (predecessors):**
- `2.1.1` SRS Document *(obligatorio)*
- `2.1.3` Priority Matrix *(obligatorio)*

**Habilita (successors):**
- Inicio de Fase 3 (Design)
- `2.4.1` Product Backlog — baseline para crear stories

**Criterio de completitud:**
- [ ] PO ha revisado el SRS completo
- [ ] Sign-off documentado (fecha, nombre, firma o aprobación digital)
- [ ] Lista de observaciones resueltas

**Anti-patrones:**
- ❌ **Aprobación sin leer:** El PO debe entender lo que aprueba.
- ❌ **Aprobación verbal:** Debe quedar documentada.

**Template:** `_pm/templates/TEMPLATE_SIGNOFF.md` *(pendiente)*

---

# 2.2 NON-FUNCTIONAL REQUIREMENTS

**Responsable:** Systems Analyst  
**Aprueba:** Solution Architect  
**Objetivo de subfase:** Documentar requisitos de calidad del sistema.

---

### 2.2.1 NFR Document

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.2 Non-Functional Requirements |
| **Responsable** | Systems Analyst |
| **Ejecuta** | Systems Analyst + Solution Architect |
| **Aprueba** | Solution Architect |
| **Formato** | PDF/MD |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 2-3 días |
| **Frecuencia** | Una vez + por cambio de arquitectura |

**Perfil de ejecución:** SA define los NFRs con input del Solution Architect para viabilidad. En VTT: un agente puede proponer NFRs estándar por categoría (performance, seguridad, escalabilidad, disponibilidad, usabilidad), y el SA/Architect ajustan los targets al contexto del proyecto.

**Qué es:** Documento que define los requisitos de CALIDAD del sistema — no qué hace, sino qué tan bien lo hace.

**Para qué sirve:** Los NFRs determinan la arquitectura. Un sistema que debe soportar 10 usuarios es arquitectónicamente diferente de uno que debe soportar 10M. Sin NFRs, el arquitecto no puede tomar decisiones informadas.

**Inputs requeridos:**
- `2.1.1` SRS Document — los NFRs complementan los funcionales
- `0.4.5` Value Hypothesis — los targets de las hipótesis implican NFRs
- `0.1.2` TAM/SAM/SOM — dimensionar escalabilidad
- Expectativas del PO sobre calidad

**Dependencias (predecessors):**
- `2.1.1` SRS Document *(obligatorio)*

**Habilita (successors):**
- `2.2.2`-`2.2.6` — secciones detalladas por categoría
- `3B.1.1` System Architecture — los NFRs determinan la arquitectura
- `5.3.1` Performance Tests — tests validan los NFRs

**Audiencia:**
- **Solution Architect** — para diseñar la arquitectura
- **Tech Lead** — para decisiones de implementación
- **DevOps** — para dimensionar infraestructura
- **QA Lead** — para diseñar tests de calidad

**Secciones esperadas:**
1. Performance requirements (tiempos de respuesta, throughput)
2. Security requirements (autenticación, autorización, encriptación)
3. Scalability requirements (usuarios concurrentes, crecimiento)
4. Availability requirements (uptime, disaster recovery)
5. Usability requirements (accesibilidad, internacionalización)
6. Compliance requirements si aplica

**Criterio de completitud:**
- [ ] Cada NFR es medible (tiene un número, no "debe ser rápido")
- [ ] Priorizado (qué sacrificar si hay trade-off entre performance y seguridad)
- [ ] Solution Architect valida que los targets son alcanzables
- [ ] Alineado con el presupuesto de infraestructura

**Anti-patrones:**
- ❌ **NFRs vagos:** "Alta disponibilidad" no dice nada. "99.9% uptime excluyendo ventanas de mantenimiento" sí.
- ❌ **NFRs imposibles:** "0 segundos de downtime" no es alcanzable.
- ❌ **Ignorar NFRs hasta producción:** Los NFRs se definen ANTES de la arquitectura, no después del launch.

**Template:** `_pm/templates/TEMPLATE_NFR.md` *(pendiente)*

---

### 2.2.2 Performance Requirements

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.2 Non-Functional Requirements |
| **Responsable** | Systems Analyst |
| **Ejecuta** | Systems Analyst + Tech Lead |
| **Aprueba** | Solution Architect |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Con el NFR doc |

**Perfil de ejecución:** SA define targets, TL valida viabilidad técnica. En VTT: un agente puede proponer targets estándar por tipo de aplicación (web app: <2s page load, API: <200ms response, etc.).

**Qué es:** Requisitos específicos de rendimiento: tiempos de respuesta, throughput, tiempos de carga por tipo de operación.

**Para qué sirve:** Define la experiencia de velocidad del usuario y los SLAs técnicos.

**Inputs requeridos:**
- `2.2.1` NFR Document — sección de performance
- Benchmarks de competidores (de 0.2.7 UX Benchmarking)

**Dependencias (predecessors):** `2.2.1` NFR Document *(obligatorio)*

**Habilita (successors):** `5.3.1` Performance Tests, `3B.1.1` System Architecture

**Secciones esperadas:**

| Operación | Target | Condiciones | Medición |
|----------|--------|------------|---------|
| Page load | <2s | 3G connection | Lighthouse |
| API response | <200ms | p95 | APM tool |

**Criterio de completitud:**
- [ ] Targets por tipo de operación (lectura, escritura, búsqueda)
- [ ] Condiciones de medición definidas (percentil, red, dispositivo)
- [ ] TL confirma viabilidad

**Template:** Incluido dentro de `TEMPLATE_NFR.md`

---

### 2.2.3 Security Requirements

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.2 Non-Functional Requirements |
| **Responsable** | Systems Analyst |
| **Ejecuta** | Systems Analyst + Security Engineer (si existe) |
| **Aprueba** | Solution Architect |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Con el NFR doc |

**Perfil de ejecución:** SA define los requisitos de seguridad con input de Security Engineer si existe. En VTT: un agente puede proponer requisitos estándar (OWASP Top 10, autenticación, encriptación at-rest/in-transit, RBAC), pero la evaluación de amenazas específicas al contexto requiere expertise humano.

**Qué es:** Requisitos de seguridad del sistema: autenticación, autorización, encriptación, protección de datos, compliance.

**Para qué sirve:** Define el nivel de seguridad mínimo aceptable antes de construir. Retrofit de seguridad es 10x más caro que security-by-design.

**Inputs requeridos:**
- `2.2.1` NFR Document
- Regulaciones aplicables (GDPR, LGPD, etc.)
- Sensibilidad de los datos manejados

**Dependencias (predecessors):** `2.2.1` NFR Document *(obligatorio)*

**Habilita (successors):** `3B.1.1` System Architecture (security architecture), `5.6.1` Security Tests, `7.5.x` Security Updates

**Criterio de completitud:**
- [ ] Autenticación y autorización definidas
- [ ] Encriptación at-rest y in-transit especificada
- [ ] OWASP Top 10 cubierto
- [ ] Compliance regulatorio identificado

**Template:** Incluido dentro de `TEMPLATE_NFR.md`

---

### 2.2.4 Scalability Requirements

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.2 Non-Functional Requirements |
| **Responsable** | Systems Analyst |
| **Ejecuta** | Systems Analyst + Solution Architect |
| **Aprueba** | Solution Architect |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Con el NFR doc |

**Perfil de ejecución:** SA define targets basado en el SOM, Architect valida la estrategia de escalamiento. En VTT: un agente puede calcular requisitos de escalabilidad a partir del SOM y las proyecciones de adopción.

**Qué es:** Requisitos de crecimiento: usuarios concurrentes, volumen de datos, tráfico pico, y cómo debe escalar el sistema.

**Para qué sirve:** Evita el síndrome de "funciona para 10 usuarios pero se cae con 1000." Define cuándo escalar horizontalmente vs verticalmente.

**Inputs requeridos:**
- `0.1.2` TAM/SAM/SOM — proyección de usuarios
- `2.2.1` NFR Document

**Dependencias (predecessors):** `2.2.1` NFR Document *(obligatorio)*

**Habilita (successors):** `3B.5.1` Infrastructure Design, `7.6.x` Scaling

**Criterio de completitud:**
- [ ] Usuarios concurrentes target (año 1, año 2, año 3)
- [ ] Volumen de datos proyectado
- [ ] Estrategia de escalamiento (horizontal/vertical/auto)
- [ ] Dimensionado para SOM, no para TAM

**Anti-patrones:**
- ❌ **Diseñar para millones con SOM de cientos:** Over-engineering costoso.

**Template:** Incluido dentro de `TEMPLATE_NFR.md`

---

### 2.2.5 Availability Requirements

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.2 Non-Functional Requirements |
| **Responsable** | Systems Analyst |
| **Ejecuta** | Systems Analyst + DevOps |
| **Aprueba** | Solution Architect |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Con el NFR doc |

**Perfil de ejecución:** SA define el SLA target, DevOps valida la infraestructura necesaria. En VTT: un agente puede calcular el downtime permitido por nivel de SLA (99.9% = 8.7 hrs/año).

**Qué es:** Requisitos de disponibilidad: uptime target, RPO (Recovery Point Objective), RTO (Recovery Time Objective), ventanas de mantenimiento.

**Para qué sirve:** Define cuánto downtime es aceptable y qué tan rápido se debe recuperar de un fallo.

**Inputs requeridos:**
- `2.2.1` NFR Document
- Expectativas del PO sobre disponibilidad
- Costo de infraestructura por nivel de SLA

**Dependencias (predecessors):** `2.2.1` NFR Document *(obligatorio)*

**Habilita (successors):** `3B.5.1` Infrastructure Design, `6.7.1` Rollback Plan

**Criterio de completitud:**
- [ ] Uptime target definido (ej: 99.9%)
- [ ] RPO y RTO definidos
- [ ] Ventanas de mantenimiento acordadas
- [ ] Costo de infra validado contra el budget

**Template:** Incluido dentro de `TEMPLATE_NFR.md`

---

### 2.2.6 Usability Requirements

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.2 Non-Functional Requirements |
| **Responsable** | Systems Analyst |
| **Ejecuta** | UX Designer + Systems Analyst |
| **Aprueba** | Solution Architect |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Con el NFR doc |

**Perfil de ejecución:** UX Designer define requisitos de usabilidad y accesibilidad, SA los formaliza. En VTT: un agente puede listar requisitos estándar de accesibilidad (WCAG 2.1 AA) e internacionalización (i18n).

**Qué es:** Requisitos de usabilidad, accesibilidad (WCAG), internacionalización, y estándares de experiencia de usuario.

**Para qué sirve:** Asegura que el producto es usable por el mayor rango posible de usuarios, incluyendo aquellos con discapacidades.

**Inputs requeridos:**
- `2.2.1` NFR Document
- `0.4.4` Target Customer Profile — necesidades de usabilidad del perfil
- Regulaciones de accesibilidad aplicables

**Dependencias (predecessors):** `2.2.1` NFR Document *(obligatorio)*

**Habilita (successors):** `3A.4.x` Wireframes (accesibilidad), `5.4.x` Usability Tests

**Criterio de completitud:**
- [ ] Nivel de WCAG target definido
- [ ] Idiomas soportados definidos
- [ ] Dispositivos/navegadores target definidos
- [ ] Criterios de usabilidad medibles (ej: task completion rate >90%)

**Template:** Incluido dentro de `TEMPLATE_NFR.md`

---

# 2.3 USE CASES

**Responsable:** Systems Analyst  
**Aprueba:** Product Owner  
**Objetivo de subfase:** Documentar casos de uso del sistema.

---

### 2.3.1 Use Case Document

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.3 Use Cases |
| **Responsable** | Systems Analyst |
| **Ejecuta** | Systems Analyst |
| **Aprueba** | Product Owner |
| **Formato** | MD/PDF |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 3-5 días |
| **Frecuencia** | Una vez + por feature nueva |

**Perfil de ejecución:** SA lo produce directamente. En VTT: un agente SA puede generar use cases detallados a partir del SRS y las user stories, siguiendo templates estándar (precondiciones, flujo principal, flujos alternativos, postcondiciones). Es uno de los deliverables más automatizables de la fase.

**Qué es:** Documento completo de casos de uso que describe cómo los actores interactúan con el sistema para lograr objetivos específicos.

**Para qué sirve:** Traduce requisitos abstractos en escenarios concretos de interacción. Los developers entienden qué construir, los QAs entienden qué testear.

**Inputs requeridos:**
- `2.1.1` SRS Document — requisitos a cubrir
- `2.1.4` Feature List — features a documentar como use cases
- `0.4.4` Target Customer Profile — quién interactúa

**Dependencias (predecessors):**
- `2.1.1` SRS Document *(obligatorio)*

**Habilita (successors):**
- `2.3.2` Use Case Diagram
- `2.3.4` Detailed Use Cases
- `2.4.2` User Stories — stories se derivan de use cases
- `2.7.2` Criteria per Story
- `5.2.1` Test Cases — tests basados en use cases

**Criterio de completitud:**
- [ ] Cada feature del MVP tiene al menos 1 use case
- [ ] Cada use case tiene flujo principal y al menos 1 alternativo
- [ ] Precondiciones y postcondiciones definidas
- [ ] PO ha validado que los escenarios son correctos

**Anti-patrones:**
- ❌ **Solo happy path:** Los flujos alternativos y de error son donde vive la complejidad real.
- ❌ **Use cases de sistema, no de usuario:** "El sistema guarda en la DB" no es un use case. "El profesor sube una grabación" sí.

**Template:** `_pm/templates/TEMPLATE_USE_CASES.md` *(pendiente)*

---

### 2.3.2 Use Case Diagram

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.3 Use Cases |
| **Responsable** | Systems Analyst |
| **Ejecuta** | Systems Analyst |
| **Aprueba** | Product Owner |
| **Formato** | Diagrama UML |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Con el use case doc |

**Perfil de ejecución:** SA lo produce. En VTT: altamente automatizable — un agente puede generar diagramas UML de use cases en Mermaid a partir de 2.3.5 Actor Definitions y 2.3.3 Use Case List.

**Qué es:** Diagrama UML que muestra actores, use cases y sus relaciones (include, extend).

**Para qué sirve:** Vista rápida de quién hace qué con el sistema. Útil para validar cobertura con el PO.

**Inputs requeridos:**
- `2.3.1` Use Case Document
- `2.3.5` Actor Definitions

**Dependencias (predecessors):** `2.3.1` Use Case Document *(obligatorio)*

**Habilita (successors):** `2.3.6` Use Case Relationships

**Criterio de completitud:**
- [ ] Todos los actores representados
- [ ] Todos los use cases principales representados
- [ ] Relaciones include/extend correctas

**Template:** Incluido dentro de `TEMPLATE_USE_CASES.md`

---

### 2.3.3 Use Case List

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.3 Use Cases |
| **Responsable** | Systems Analyst |
| **Ejecuta** | Systems Analyst |
| **Aprueba** | Product Owner |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Con el use case doc |

**Perfil de ejecución:** SA lo extrae del documento. En VTT: automatizable desde 2.3.1.

**Qué es:** Lista numerada de todos los use cases con ID, nombre, actor principal, módulo y prioridad.

**Para qué sirve:** Índice rápido para tracking de cobertura y asignación a sprints.

**Inputs requeridos:** `2.3.1` Use Case Document

**Dependencias (predecessors):** `2.3.1` Use Case Document *(obligatorio)*

**Habilita (successors):** `2.8.1` Traceability Matrix

**Criterio de completitud:**
- [ ] Cada use case del documento tiene entrada
- [ ] IDs únicos (UC-001, UC-002...)

**Template:** Incluido dentro de `TEMPLATE_USE_CASES.md`

---

### 2.3.4 Detailed Use Cases

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.3 Use Cases |
| **Responsable** | Systems Analyst |
| **Ejecuta** | Systems Analyst |
| **Aprueba** | Product Owner |
| **Formato** | Template |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 2-3 días |
| **Frecuencia** | Con el use case doc |

**Perfil de ejecución:** SA escribe cada use case en detalle. En VTT: altamente automatizable — un agente SA puede generar use cases detallados con el formato estándar. Es de los deliverables donde más valor agrega un agente por volumen.

**Qué es:** Cada use case en formato detallado: precondiciones, trigger, flujo principal paso a paso, flujos alternativos, flujos de excepción, postcondiciones, reglas de negocio.

**Para qué sirve:** Es la especificación más cercana a lo que el developer implementa y lo que el QA testea.

**Inputs requeridos:**
- `2.3.1` Use Case Document
- `2.5.1` Business Rules — reglas que aplican en cada use case

**Dependencias (predecessors):** `2.3.1` Use Case Document *(obligatorio)*

**Habilita (successors):**
- `2.4.2` User Stories — cada use case genera 1+ stories
- `2.7.5` Test Scenarios — cada flujo es un test scenario
- `5.2.1` Test Cases

**Criterio de completitud:**
- [ ] Cada use case tiene precondiciones, flujo principal, al menos 1 alternativo, postcondiciones
- [ ] Reglas de negocio referenciadas por ID (BR-XXX)
- [ ] Flujos de excepción (qué pasa cuando falla)

**Template:** Incluido dentro de `TEMPLATE_USE_CASES.md`

---

### 2.3.5 Actor Definitions

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.3 Use Cases |
| **Responsable** | Systems Analyst |
| **Ejecuta** | Systems Analyst |
| **Aprueba** | Product Owner |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Con el use case doc |

**Perfil de ejecución:** SA define los actores. En VTT: un agente puede derivar actores del Target Customer Profile y los roles del sistema.

**Qué es:** Tabla que define cada actor del sistema: nombre, descripción, permisos, relación con otros actores.

**Para qué sirve:** Establece QUIÉN interactúa con el sistema y con qué nivel de acceso. Informa directamente el modelo de autorización.

**Inputs requeridos:**
- `0.4.4` Target Customer Profile
- `2.1.1` SRS Document

**Dependencias (predecessors):** `2.1.1` SRS Document *(obligatorio)*

**Habilita (successors):** `2.3.2` Use Case Diagram, `2.5.5` Authorization Rules

**Criterio de completitud:**
- [ ] Todos los actores humanos y de sistema identificados
- [ ] Permisos básicos por actor definidos
- [ ] Jerarquía de actores si existe

**Template:** Incluido dentro de `TEMPLATE_USE_CASES.md`

---

### 2.3.6 Use Case Relationships

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.3 Use Cases |
| **Responsable** | Systems Analyst |
| **Ejecuta** | Systems Analyst |
| **Aprueba** | Product Owner |
| **Formato** | Diagrama |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Con el use case doc |

**Perfil de ejecución:** SA lo produce. En VTT: automatizable desde el diagrama UML y los use cases detallados.

**Qué es:** Diagrama que muestra las relaciones include/extend entre use cases y las dependencias.

**Para qué sirve:** Identifica use cases reutilizables (include) y extensiones opcionales (extend). Informa la modularización del código.

**Inputs requeridos:** `2.3.2` Use Case Diagram, `2.3.4` Detailed Use Cases

**Dependencias (predecessors):** `2.3.2` Use Case Diagram *(obligatorio)*

**Habilita (successors):** `3B.1.1` System Architecture — modularización

**Criterio de completitud:**
- [ ] Relaciones include/extend correctamente identificadas
- [ ] Use cases comunes (login, notificación) como includes

**Template:** Incluido dentro de `TEMPLATE_USE_CASES.md`

---

# 2.4 USER STORIES

**Responsable:** Product Manager  
**Aprueba:** Product Owner  
**Objetivo de subfase:** Definir funcionalidades desde perspectiva del usuario.

---

### 2.4.1 Product Backlog

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.4 User Stories |
| **Responsable** | Product Manager |
| **Ejecuta** | Product Manager |
| **Aprueba** | Product Owner |
| **Formato** | Lista priorizada |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 2 días (inicial) |
| **Frecuencia** | Continua (refinement cada sprint) |

**Perfil de ejecución:** PM lo crea y mantiene. En VTT: un agente puede generar stories iniciales a partir de los use cases y requisitos, pero el PM las refina y prioriza.

**Qué es:** Lista priorizada de todas las user stories del producto, incluyendo las del MVP y las de fases futuras.

**Para qué sirve:** Es el "inventario" de trabajo de producto. El sprint planning selecciona stories del top del backlog.

**Inputs requeridos:**
- `2.3.4` Detailed Use Cases — cada use case genera stories
- `2.1.3` Priority Matrix — priorización
- `1.2.4` MVP Definition — qué stories son del MVP

**Dependencias (predecessors):**
- `2.3.1` Use Case Document *(obligatorio)*
- `2.1.6` Requirements Approval *(obligatorio)*

**Habilita (successors):**
- `2.4.2` User Stories — cada ítem se detalla
- `2.4.3` Story Map
- Sprint planning

**Criterio de completitud:**
- [ ] Todas las features del MVP tienen stories
- [ ] Priorizadas (top = próximo sprint)
- [ ] Estimadas (al menos las del próximo sprint)

**Template:** Herramienta de gestión (Jira, Linear, GitHub Issues)

---

### 2.4.2 User Stories

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.4 User Stories |
| **Responsable** | Product Manager |
| **Ejecuta** | Product Manager + Systems Analyst |
| **Aprueba** | Product Owner |
| **Formato** | Template |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 3-5 días (batch inicial) |
| **Frecuencia** | Continua (refinement) |

**Perfil de ejecución:** PM escribe las stories en lenguaje de usuario, SA agrega detalle técnico y criterios de aceptación. En VTT: un agente puede generar stories completas a partir de use cases en formato "As a [role], I want [goal], so that [benefit]" con acceptance criteria en Gherkin. Altamente automatizable.

**Qué es:** Historias de usuario completas en formato estándar con acceptance criteria, notas técnicas y dependencias.

**Para qué sirve:** Unidad de trabajo del equipo. Cada story es algo que se puede implementar, testear y entregar en un sprint.

**Inputs requeridos:**
- `2.4.1` Product Backlog
- `2.3.4` Detailed Use Cases
- `2.5.1` Business Rules
- `2.7.3` Definition of Done

**Dependencias (predecessors):**
- `2.4.1` Product Backlog *(obligatorio)*
- `2.3.4` Detailed Use Cases *(obligatorio)*

**Habilita (successors):**
- `2.4.5` Story Estimation
- `2.7.2` Criteria per Story
- Sprint planning → Development

**Criterio de completitud:**
- [ ] Formato: "As a [role], I want [goal], so that [benefit]"
- [ ] Acceptance criteria en formato Gherkin (Given/When/Then)
- [ ] Story cumple INVEST (Independent, Negotiable, Valuable, Estimable, Small, Testable)
- [ ] Aprobada por PO

**Anti-patrones:**
- ❌ **Story técnica:** "As a developer, I want to refactor the DB" no es user story — es tech debt.
- ❌ **Story épica:** Si no cabe en un sprint, es una epic, no una story.
- ❌ **Sin acceptance criteria:** Una story sin AC no se puede testear ni cerrar.

**Template:** `_pm/templates/TEMPLATE_USER_STORY.md` *(pendiente)*

---

### 2.4.3 Story Map

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.4 User Stories |
| **Responsable** | Product Manager |
| **Ejecuta** | Product Manager |
| **Aprueba** | Product Owner |
| **Formato** | Diagrama |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez + por release |

**Perfil de ejecución:** PM lo crea. En VTT: un agente puede generar una estructura inicial de story map agrupando stories por epic y flujo de usuario.

**Qué es:** Mapa visual que organiza las stories en dos dimensiones: horizontal (flujo del usuario) y vertical (prioridad/release).

**Para qué sirve:** Visualiza el producto completo y dónde cae la línea de MVP. Más intuitivo que una lista para entender el alcance.

**Inputs requeridos:**
- `2.4.1` Product Backlog
- `2.4.4` Epics
- `2.6.5` User Journey Maps

**Dependencias (predecessors):** `2.4.1` Product Backlog *(obligatorio)*

**Habilita (successors):** Release planning, sprint planning

**Criterio de completitud:**
- [ ] Todas las epics representadas
- [ ] Línea de MVP visible
- [ ] Flujo de usuario coherente de izquierda a derecha

**Template:** Herramienta visual (Miro, FigJam) o Mermaid

---

### 2.4.4 Epics

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.4 User Stories |
| **Responsable** | Product Manager |
| **Ejecuta** | Product Manager |
| **Aprueba** | Product Owner |
| **Formato** | Lista |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Con el backlog |

**Perfil de ejecución:** PM agrupa stories en epics. En VTT: un agente puede derivar epics de los módulos del feature list (2.1.4).

**Qué es:** Agrupación de user stories relacionadas en unidades temáticas más grandes (ej: "Autenticación", "Transcripción", "Dashboard").

**Para qué sirve:** Organización de alto nivel del backlog. Permite hablar de conjuntos de funcionalidad sin entrar en detalle.

**Inputs requeridos:** `2.4.1` Product Backlog, `2.1.4` Feature List

**Dependencias (predecessors):** `2.4.1` Product Backlog *(obligatorio)*

**Habilita (successors):** `2.4.3` Story Map, Release planning

**Criterio de completitud:**
- [ ] Cada story pertenece a una epic
- [ ] 5-15 epics típico para un MVP
- [ ] Nombre descriptivo por epic

**Template:** Herramienta de gestión

---

### 2.4.5 Story Estimation

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.4 User Stories |
| **Responsable** | Product Manager |
| **Ejecuta** | Tech Lead + Developers |
| **Aprueba** | Tech Lead |
| **Formato** | Columna en backlog |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días por sprint |
| **Frecuencia** | Por sprint (refinement) |

**Perfil de ejecución:** El equipo de desarrollo estima en story points durante el refinement. El PM facilita pero NO estima. En VTT: un agente puede proponer estimaciones iniciales basadas en complejidad técnica de los acceptance criteria, pero las estimaciones finales son del equipo de desarrollo.

**Qué es:** Estimación en story points de cada user story usando técnicas como planning poker.

**Para qué sirve:** Permite calcular velocidad del equipo y predecir cuántos sprints toma cada release.

**Inputs requeridos:**
- `2.4.2` User Stories con acceptance criteria
- Experiencia del equipo con stories similares

**Dependencias (predecessors):** `2.4.2` User Stories *(obligatorio)*

**Habilita (successors):** `2.4.6` Sprint Assignment, velocity tracking

**Criterio de completitud:**
- [ ] Stories del próximo sprint estimadas
- [ ] Equipo de desarrollo participó en la estimación (no solo el TL)
- [ ] Stories >13 puntos divididas en stories más pequeñas

**Anti-patrones:**
- ❌ **PM estima:** La estimación es del equipo que implementa.
- ❌ **Story points = horas:** Story points miden complejidad relativa, no tiempo.

**Template:** Herramienta de gestión

---

### 2.4.6 Sprint Assignment

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.4 User Stories |
| **Responsable** | Product Manager |
| **Ejecuta** | Product Manager + Tech Lead |
| **Aprueba** | Product Owner |
| **Formato** | Columna en backlog |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | En sprint planning |
| **Frecuencia** | Cada sprint |

**Perfil de ejecución:** PM prioriza qué stories entran, TL valida capacidad del equipo. En VTT: un agente puede proponer asignación basada en velocidad histórica y dependencias.

**Qué es:** Asignación de stories a sprints específicos basada en prioridad, dependencias y capacidad del equipo.

**Para qué sirve:** Convierte el backlog priorizado en un plan de ejecución sprint por sprint.

**Inputs requeridos:**
- `2.4.5` Story Estimation
- `1.5.4` Sprint Calendar
- Velocidad histórica del equipo

**Dependencias (predecessors):**
- `2.4.5` Story Estimation *(obligatorio)*
- `1.5.4` Sprint Calendar *(obligatorio)*

**Habilita (successors):** Sprint execution, handoffs a desarrollo

**Criterio de completitud:**
- [ ] Stories del próximo sprint asignadas
- [ ] Total de story points no excede velocidad del equipo
- [ ] Dependencias respetadas (no asignar story B antes que story A)

**Template:** Herramienta de gestión

---

# 2.5 BUSINESS RULES

**Responsable:** Systems Analyst  
**Aprueba:** Product Owner  
**Objetivo de subfase:** Documentar lógica y validaciones de negocio.

---

### 2.5.1 Business Rules Document

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.5 Business Rules |
| **Responsable** | Systems Analyst |
| **Ejecuta** | Systems Analyst |
| **Aprueba** | Product Owner |
| **Formato** | MD/PDF |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 2-3 días |
| **Frecuencia** | Una vez + por feature |

**Perfil de ejecución:** SA documenta las reglas a partir de entrevistas con PO/PM y los use cases. En VTT: un agente SA puede extraer reglas implícitas de los use cases detallados y proponerlas formalmente.

**Qué es:** Documento que define todas las reglas de negocio del sistema: validaciones, cálculos, permisos, transiciones de estado.

**Para qué sirve:** Centraliza la lógica de negocio. Cuando un developer pregunta "¿qué pasa si el usuario intenta X?", la respuesta está aquí.

**Inputs requeridos:**
- `2.1.1` SRS Document
- `2.3.4` Detailed Use Cases
- Entrevistas con PO/PM sobre reglas de negocio

**Dependencias (predecessors):**
- `2.1.1` SRS Document *(obligatorio)*
- `2.3.4` Detailed Use Cases *(recomendado)*

**Habilita (successors):**
- `2.5.2`-`2.5.7` — reglas detalladas por tipo
- `2.4.2` User Stories — stories referencian reglas (BR-XXX)
- `4.x` Development — developers implementan las reglas

**Criterio de completitud:**
- [ ] Cada regla tiene ID único (BR-XXX)
- [ ] Cada regla es no-ambigua y testable
- [ ] Reglas organizadas por tipo (validación, cálculo, autorización, estado)
- [ ] PO ha validado que las reglas son correctas

**Anti-patrones:**
- ❌ **Reglas implícitas:** Si la regla solo existe en la cabeza del PO, no existe.
- ❌ **Reglas en código sin documentar:** Primero documento, luego código.

**Template:** `_pm/templates/TEMPLATE_BUSINESS_RULES.md` *(pendiente)*

---

### 2.5.2 Rules List

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.5 Business Rules |
| **Responsable** | Systems Analyst |
| **Ejecuta** | Systems Analyst |
| **Aprueba** | Product Owner |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Con el BR doc |

**Perfil de ejecución:** SA extrae del documento. En VTT: automatizable.

**Qué es:** Lista numerada (BR-001, BR-002...) de todas las reglas de negocio con descripción breve y categoría.

**Inputs requeridos:** `2.5.1` Business Rules Document

**Dependencias (predecessors):** `2.5.1` Business Rules Document *(obligatorio)*

**Habilita (successors):** `2.8.1` Traceability Matrix

**Criterio de completitud:**
- [ ] Cada regla del documento tiene entrada
- [ ] IDs únicos y categoría asignada

**Template:** Incluido dentro de `TEMPLATE_BUSINESS_RULES.md`

---

### 2.5.3 Validation Rules

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.5 Business Rules |
| **Responsable** | Systems Analyst |
| **Ejecuta** | Systems Analyst |
| **Aprueba** | Product Owner |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Con el BR doc |

**Perfil de ejecución:** SA las define. En VTT: un agente puede generar validaciones estándar por tipo de dato (email, teléfono, fecha, rango numérico).

**Qué es:** Reglas de validación de datos de entrada: formatos, rangos, obligatoriedad, unicidad.

**Para qué sirve:** Define qué acepta y qué rechaza el sistema en cada campo/input.

**Inputs requeridos:** `2.5.1` Business Rules Document, `2.1.1` SRS Document

**Dependencias (predecessors):** `2.5.1` Business Rules Document *(obligatorio)*

**Habilita (successors):** `4.x` Frontend/Backend validation, `5.2.1` Test Cases

**Secciones esperadas:**

| Campo | Tipo | Obligatorio | Formato | Rango | Mensaje de error |
|-------|------|------------|---------|-------|-----------------|

**Criterio de completitud:**
- [ ] Cada campo de entrada del sistema tiene validaciones definidas
- [ ] Mensajes de error por cada validación

**Template:** Incluido dentro de `TEMPLATE_BUSINESS_RULES.md`

---

### 2.5.4 Calculation Rules

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.5 Business Rules |
| **Responsable** | Systems Analyst |
| **Ejecuta** | Systems Analyst |
| **Aprueba** | Product Owner |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Con el BR doc |

**Perfil de ejecución:** SA las define con input del PM/PO sobre la lógica de negocio. En VTT: un agente puede formalizar cálculos en fórmulas explícitas.

**Qué es:** Reglas de cálculo del sistema: fórmulas, transformaciones, agregaciones.

**Para qué sirve:** Centraliza la lógica de cálculo. Evita que cada developer implemente su propia versión de la misma fórmula.

**Inputs requeridos:** `2.5.1` Business Rules Document

**Dependencias (predecessors):** `2.5.1` Business Rules Document *(obligatorio)*

**Criterio de completitud:**
- [ ] Cada cálculo tiene fórmula explícita
- [ ] Inputs y outputs de cada cálculo definidos
- [ ] Casos edge (división por cero, null, desbordamiento) documentados

**Template:** Incluido dentro de `TEMPLATE_BUSINESS_RULES.md`

---

### 2.5.5 Authorization Rules

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.5 Business Rules |
| **Responsable** | Systems Analyst |
| **Ejecuta** | Systems Analyst |
| **Aprueba** | Product Owner |
| **Formato** | Matriz |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Con el BR doc |

**Perfil de ejecución:** SA la define a partir de los Actor Definitions (2.3.5). En VTT: un agente puede generar la matriz RBAC cruzando actores × operaciones × recursos.

**Qué es:** Matriz de autorización (RBAC): qué rol puede hacer qué operación sobre qué recurso.

**Para qué sirve:** Define formalmente los permisos del sistema antes de implementar. Evita agujeros de seguridad por permisos mal definidos.

**Inputs requeridos:**
- `2.3.5` Actor Definitions
- `2.5.1` Business Rules Document

**Dependencias (predecessors):**
- `2.3.5` Actor Definitions *(obligatorio)*
- `2.5.1` Business Rules Document *(obligatorio)*

**Habilita (successors):** `2.2.3` Security Requirements, `3B.1.1` System Architecture (security)

**Secciones esperadas:**

| Recurso | Operación | Admin | User | Guest |
|---------|----------|-------|------|-------|
| Transcripción | Crear | ✅ | ✅ | ❌ |
| Transcripción | Eliminar | ✅ | 🔶 Own | ❌ |

**Criterio de completitud:**
- [ ] Todos los actores × todas las operaciones × todos los recursos
- [ ] Principio de least privilege aplicado
- [ ] Operaciones sensibles (eliminar, admin) restringidas

**Template:** Incluido dentro de `TEMPLATE_BUSINESS_RULES.md`

---

### 2.5.6 State Transition Rules

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.5 Business Rules |
| **Responsable** | Systems Analyst |
| **Ejecuta** | Systems Analyst |
| **Aprueba** | Product Owner |
| **Formato** | Diagrama |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Con el BR doc |

**Perfil de ejecución:** SA las define y diagrama. En VTT: un agente puede generar diagramas de estado en Mermaid a partir de las entidades principales y sus estados posibles.

**Qué es:** Diagramas de estado que muestran los estados posibles de cada entidad principal y las transiciones permitidas entre estados.

**Para qué sirve:** Define la máquina de estados del sistema. Evita transiciones inválidas (ej: no puedes "publicar" algo que está "eliminado").

**Inputs requeridos:**
- `2.5.1` Business Rules Document
- `2.3.4` Detailed Use Cases — las acciones de los use cases son transiciones

**Dependencias (predecessors):** `2.5.1` Business Rules Document *(obligatorio)*

**Habilita (successors):** `4.x` Development — implementación de state machines

**Criterio de completitud:**
- [ ] Diagrama de estados para cada entidad principal
- [ ] Cada transición tiene trigger (qué la causa) y guard (qué condiciones deben cumplirse)
- [ ] Estados terminales identificados

**Template:** Incluido dentro de `TEMPLATE_BUSINESS_RULES.md`

---

### 2.5.7 Business Glossary

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.5 Business Rules |
| **Responsable** | Systems Analyst |
| **Ejecuta** | Systems Analyst |
| **Aprueba** | Product Owner |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Continua (se va enriqueciendo) |

**Perfil de ejecución:** SA lo mantiene. En VTT: un agente puede extraer términos de dominio de todos los documentos previos y proponerlos para el glosario.

**Qué es:** Glosario de términos de negocio con definición precisa. Cada término tiene una y solo una definición oficial.

**Para qué sirve:** Elimina ambigüedad. Cuando el PO dice "ISBN" y el developer entiende "EAN", el glosario resuelve: "ISBN = EAN = número de producto."

**Inputs requeridos:** Todos los documentos de fases 0, 1 y 2

**Dependencias (predecessors):** Ninguna directa — se construye progresivamente

**Habilita (successors):** Todos los documentos futuros — vocabulario estándar

**Criterio de completitud:**
- [ ] Cada término de dominio usado en la documentación tiene definición
- [ ] Sin sinónimos no documentados
- [ ] PO valida las definiciones

**Anti-patrones:**
- ❌ **Glosario genérico:** "API: Application Programming Interface" no agrega valor. "Transcripción: resultado textual del procesamiento de audio de una clase grabada" sí.

**Template:** Incluido dentro de `TEMPLATE_BUSINESS_RULES.md`

---

# 2.6 USER FLOWS

**Responsable:** UX Designer  
**Aprueba:** Design Lead  
**Objetivo de subfase:** Documentar los caminos que sigue el usuario.

---

### 2.6.1 User Flow Diagrams

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.6 User Flows |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Diagramas |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 2-3 días |
| **Frecuencia** | Una vez + por feature |

**Perfil de ejecución:** UX Designer los produce. En VTT: un agente puede generar user flows en Mermaid a partir de los use cases detallados, pero el UX Designer refina la experiencia (dónde poner confirmaciones, cómo manejar errores UX-wise).

**Qué es:** Diagramas que muestran los caminos que sigue el usuario dentro del producto para completar una tarea — incluyendo decisiones, errores y caminos alternativos.

**Para qué sirve:** Es el puente entre use cases (qué hace el usuario) y wireframes (cómo se ve). Los developers entienden la navegación, los QAs los caminos a testear.

**Inputs requeridos:**
- `2.3.4` Detailed Use Cases
- `2.3.5` Actor Definitions
- `0.4.4` Target Customer Profile

**Dependencias (predecessors):**
- `2.3.4` Detailed Use Cases *(obligatorio)*

**Habilita (successors):**
- `2.6.2`-`2.6.7` — flujos específicos
- `3A.4.x` Wireframes — los wireframes implementan los flujos
- `3A.3.1` Site Map — se deriva de los flujos

**Criterio de completitud:**
- [ ] Un flow por cada use case principal
- [ ] Happy path + al menos 1 error path por flow
- [ ] Cada decisión tiene todas sus salidas documentadas
- [ ] Consistente con los use cases

**Template:** `_pm/templates/TEMPLATE_USER_FLOWS.md` *(pendiente)*

---

### 2.6.2 Happy Path Flows

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.6 User Flows |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Diagrama |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Con user flows |

**Perfil de ejecución:** UX Designer los produce. En VTT: altamente automatizable — un agente genera el happy path directo del use case principal.

**Qué es:** Flujos del camino ideal — cuando todo sale bien, sin errores ni bifurcaciones.

**Para qué sirve:** El punto de partida del diseño y la primera cosa que se implementa y testea.

**Inputs requeridos:** `2.6.1` User Flow Diagrams

**Dependencias (predecessors):** `2.6.1` User Flow Diagrams *(obligatorio)*

**Habilita (successors):** `3A.4.x` Wireframes — se diseñan primero los happy paths

**Criterio de completitud:**
- [ ] Cada feature principal tiene happy path documentado
- [ ] Lineal (sin bifurcaciones — esas van en 2.6.3)
- [ ] Mínimo de pasos necesarios

**Template:** Incluido dentro de `TEMPLATE_USER_FLOWS.md`

---

### 2.6.3 Error Flows

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.6 User Flows |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Diagrama |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Con user flows |

**Perfil de ejecución:** UX Designer los define. En VTT: un agente puede generar los flujos de error a partir de los flujos alternativos de los use cases.

**Qué es:** Flujos que documentan qué ve el usuario cuando algo sale mal: validaciones fallidas, errores de servidor, timeouts, permisos denegados.

**Para qué sirve:** El 80% de la experiencia real del usuario son los estados de error y los edge cases, no el happy path.

**Inputs requeridos:**
- `2.6.1` User Flow Diagrams
- `2.5.3` Validation Rules — qué puede fallar

**Dependencias (predecessors):** `2.6.1` User Flow Diagrams *(obligatorio)*

**Habilita (successors):** `3A.5.7` Error States (UI), `5.2.1` Test Cases

**Criterio de completitud:**
- [ ] Cada happy path tiene al menos 2 error flows asociados
- [ ] Cada error tiene recovery path (cómo vuelve al happy path)
- [ ] Mensajes de error definidos (o referencia a 2.5.3)

**Template:** Incluido dentro de `TEMPLATE_USER_FLOWS.md`

---

### 2.6.4 Edge Cases

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.6 User Flows |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Designer + Systems Analyst |
| **Aprueba** | Design Lead |
| **Formato** | Lista |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Continua |

**Perfil de ejecución:** UX Designer identifica edge cases de experiencia, SA identifica edge cases técnicos. En VTT: un agente puede listar edge cases comunes por tipo de feature (formularios: campos vacíos, input extremo; listas: vacías, 1 ítem, 10K ítems; etc.).

**Qué es:** Lista de casos borde: situaciones inusuales pero posibles que el sistema debe manejar.

**Para qué sirve:** Los bugs más difíciles viven en los edge cases. Documentarlos antes de construir ahorra debugging costoso.

**Inputs requeridos:**
- `2.6.1`-`2.6.3` User/Happy/Error Flows
- `2.5.3` Validation Rules

**Dependencias (predecessors):** `2.6.1` User Flow Diagrams *(obligatorio)*

**Habilita (successors):** `5.2.1` Test Cases, `3A.5.6` Empty States (UI)

**Criterio de completitud:**
- [ ] Cada feature tiene edge cases documentados
- [ ] Incluye: datos vacíos, datos extremos, concurrencia, pérdida de conexión
- [ ] Cada edge case tiene comportamiento esperado definido

**Template:** Incluido dentro de `TEMPLATE_USER_FLOWS.md`

---

### 2.6.5 User Journey Maps

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.6 User Flows |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Diagrama |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Una vez + por persona |

**Perfil de ejecución:** UX Designer los produce. En VTT: un agente puede generar la estructura del journey map, pero las emociones y touchpoints requieren input de research real.

**Qué es:** Mapas de journey completos: experiencia end-to-end del usuario incluyendo acciones, pensamientos, emociones y touchpoints.

**Para qué sirve:** Va más allá de los flujos funcionales — incluye la experiencia emocional. Identifica momentos de frustración y de deleite.

**Inputs requeridos:**
- `0.4.4` Target Customer Profile
- `0.3.2` User Pain Points
- `2.6.1` User Flow Diagrams

**Dependencias (predecessors):**
- `2.6.1` User Flow Diagrams *(obligatorio)*
- `0.4.4` Target Customer Profile *(obligatorio)*

**Habilita (successors):** `3A.4.x` Wireframes, `2.4.3` Story Map

**Criterio de completitud:**
- [ ] Un journey por persona principal
- [ ] Incluye: fases, acciones, pensamientos, emociones, touchpoints, oportunidades
- [ ] Momentos de dolor y de deleite identificados

**Template:** `_pm/templates/TEMPLATE_JOURNEY_MAP.md` *(pendiente)*

---

### 2.6.6 Task Flows

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.6 User Flows |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Diagramas |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Con user flows |

**Perfil de ejecución:** UX Designer los produce. En VTT: automatizable a partir de use cases — cada use case es un task flow.

**Qué es:** Flujos de tareas específicas: cada tarea individual que el usuario puede realizar, desglosada en pasos atómicos.

**Para qué sirve:** Más granular que user flows. Cada task flow se convierte en una pantalla o sección de wireframe.

**Inputs requeridos:** `2.6.1` User Flow Diagrams, `2.3.4` Detailed Use Cases

**Dependencias (predecessors):** `2.6.1` User Flow Diagrams *(obligatorio)*

**Habilita (successors):** `3A.4.x` Wireframes

**Criterio de completitud:**
- [ ] Una task por cada acción atómica del usuario
- [ ] Pasos numerados secuencialmente
- [ ] Input y output de cada paso definido

**Template:** Incluido dentro de `TEMPLATE_USER_FLOWS.md`

---

### 2.6.7 Navigation Map

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.6 User Flows |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Diagrama |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Con user flows |

**Perfil de ejecución:** UX Designer lo produce. En VTT: un agente puede generar un navigation map en Mermaid a partir del site map y los user flows.

**Qué es:** Mapa de navegación del producto: cómo se conectan las pantallas y las secciones entre sí.

**Para qué sirve:** Define la estructura de navegación antes de diseñar. Informa el menú, los breadcrumbs, la navegación lateral, etc.

**Inputs requeridos:** `2.6.1` User Flow Diagrams, `2.1.4` Feature List

**Dependencias (predecessors):** `2.6.1` User Flow Diagrams *(obligatorio)*

**Habilita (successors):** `3A.3.1` Site Map, `3A.3.2` Navigation Structure

**Criterio de completitud:**
- [ ] Todas las pantallas/secciones del MVP representadas
- [ ] Conexiones de navegación completas
- [ ] Profundidad de navegación razonable (max 3-4 clicks a cualquier destino)

**Template:** Incluido dentro de `TEMPLATE_USER_FLOWS.md`

---

# 2.7 ACCEPTANCE CRITERIA

**Responsable:** QA Lead  
**Aprueba:** Product Owner  
**Objetivo de subfase:** Definir cómo se valida que algo está completo.

---

### 2.7.1 Acceptance Criteria Doc

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.7 Acceptance Criteria |
| **Responsable** | QA Lead |
| **Ejecuta** | QA Lead + Systems Analyst |
| **Aprueba** | Product Owner |
| **Formato** | MD/PDF |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 2 días |
| **Frecuencia** | Una vez + por sprint |

**Perfil de ejecución:** QA Lead define los estándares de aceptación, SA contribuye con la perspectiva de requisitos. En VTT: un agente QA puede generar acceptance criteria en Gherkin a partir de use cases y business rules — es uno de los deliverables más automatizables.

**Qué es:** Documento que define los estándares y criterios generales de aceptación del producto, más los criterios específicos por feature/story.

**Para qué sirve:** Define CUÁNDO algo está "terminado." Sin criterios de aceptación, la definición de "listo" es subjetiva.

**Inputs requeridos:**
- `2.1.1` SRS Document
- `2.3.4` Detailed Use Cases
- `2.5.1` Business Rules

**Dependencias (predecessors):**
- `2.1.1` SRS Document *(obligatorio)*
- `2.3.4` Detailed Use Cases *(obligatorio)*

**Habilita (successors):**
- `2.7.2`-`2.7.5` — criterios específicos
- `5.2.1` Test Cases — se derivan de los AC

**Criterio de completitud:**
- [ ] Criterios generales de calidad definidos
- [ ] Cada feature del MVP tiene AC específicos
- [ ] PO entiende y aprueba los criterios

**Template:** `_pm/templates/TEMPLATE_ACCEPTANCE_CRITERIA.md` *(pendiente)*

---

### 2.7.2 Criteria per Story

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.7 Acceptance Criteria |
| **Responsable** | QA Lead |
| **Ejecuta** | QA Lead + Product Manager |
| **Aprueba** | Product Owner |
| **Formato** | Gherkin |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Continuo (en refinement) |
| **Frecuencia** | Cada sprint |

**Perfil de ejecución:** QA Lead los escribe en formato Gherkin, PM valida que reflejan la intención del producto. En VTT: altamente automatizable — un agente puede generar Given/When/Then a partir de los use cases detallados.

**Qué es:** Acceptance criteria en formato Gherkin (Given/When/Then) para cada user story.

**Para qué sirve:** Hace testable cada story. El developer sabe cuándo terminó, el QA sabe qué validar.

**Inputs requeridos:**
- `2.4.2` User Stories
- `2.5.1` Business Rules
- `2.3.4` Detailed Use Cases

**Dependencias (predecessors):**
- `2.4.2` User Stories *(obligatorio)*

**Habilita (successors):** `2.7.5` Test Scenarios, `5.2.1` Test Cases

**Criterio de completitud:**
- [ ] Cada story tiene al menos 3 ACs
- [ ] Formato Given/When/Then consistente
- [ ] Cubren happy path Y edge cases
- [ ] PO aprueba

**Anti-patrones:**
- ❌ **ACs vagos:** "Debe funcionar correctamente" no es AC.
- ❌ **Solo happy path:** Los ACs de error son igual de importantes.

**Template:** Incluido dentro de user stories

---

### 2.7.3 Definition of Done

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.7 Acceptance Criteria |
| **Responsable** | QA Lead |
| **Ejecuta** | QA Lead + Tech Lead |
| **Aprueba** | Product Owner |
| **Formato** | Checklist |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Una vez + revisión trimestral |

**Perfil de ejecución:** QA Lead y TL la definen juntos. En VTT: un agente puede proponer un DoD estándar (code review aprobado, tests pasan, documentación actualizada, deploy a staging exitoso).

**Qué es:** Checklist global que define cuándo una story está verdaderamente "terminada" — no solo "código escrito" sino "lista para producción."

**Para qué sirve:** Estandariza la calidad. Sin DoD, "done" significa cosas diferentes para cada developer.

**Inputs requeridos:**
- Estándares de calidad del equipo
- `2.2.1` NFR Document — los NFRs informan el DoD

**Dependencias (predecessors):** Ninguna directa — es un estándar del equipo

**Habilita (successors):** Todo el desarrollo — cada story se valida contra el DoD

**Secciones esperadas:**
- [ ] Código escrito y compilable
- [ ] Unit tests escritos y pasando
- [ ] Code review aprobado
- [ ] Acceptance criteria validados
- [ ] Documentación actualizada (si aplica)
- [ ] Deploy a staging exitoso
- [ ] QA aprueba en staging
- [ ] No hay bugs P1/P2 abiertos

**Criterio de completitud:**
- [ ] Acordado por TODO el equipo (no impuesto por QA)
- [ ] Realista (no pedir 100% test coverage si no es práctico)
- [ ] Visible y referenciado en cada sprint

**Anti-patrones:**
- ❌ **DoD ignorado:** Si el equipo no lo sigue, no existe.
- ❌ **DoD imposible:** Si nunca se cumple al 100%, baja la barra o ajusta el DoD.

**Template:** Incluido dentro de `TEMPLATE_ACCEPTANCE_CRITERIA.md`

---

### 2.7.4 Definition of Ready

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.7 Acceptance Criteria |
| **Responsable** | QA Lead |
| **Ejecuta** | QA Lead + Product Manager |
| **Aprueba** | Product Owner |
| **Formato** | Checklist |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Una vez + revisión trimestral |

**Perfil de ejecución:** QA Lead y PM la definen. En VTT: un agente puede proponer un DoR estándar.

**Qué es:** Checklist que define cuándo una story está "lista para ser trabajada por desarrollo" — es decir, tiene toda la información necesaria para que un developer empiece sin preguntas.

**Para qué sirve:** Evita que stories incompletas entren al sprint, causando interrupciones y delays.

**Inputs requeridos:** Experiencia del equipo con stories mal definidas

**Dependencias (predecessors):** Ninguna directa

**Habilita (successors):** Sprint planning — solo stories "ready" entran al sprint

**Secciones esperadas:**
- [ ] Story escrita en formato estándar
- [ ] Acceptance criteria definidos
- [ ] Diseño (wireframe/mockup) disponible
- [ ] Dependencias técnicas resueltas
- [ ] Estimada en story points
- [ ] PO ha aprobado

**Criterio de completitud:**
- [ ] Acordado por PM, TL y QA Lead
- [ ] Usado como gate en sprint planning

**Template:** Incluido dentro de `TEMPLATE_ACCEPTANCE_CRITERIA.md`

---

### 2.7.5 Test Scenarios

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.7 Acceptance Criteria |
| **Responsable** | QA Lead |
| **Ejecuta** | QA Lead + QA Engineer |
| **Aprueba** | Product Owner |
| **Formato** | Gherkin |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Continuo |
| **Frecuencia** | Cada sprint |

**Perfil de ejecución:** QA Lead diseña los escenarios, QA Engineer los detalla. En VTT: altamente automatizable — un agente puede generar test scenarios en Gherkin a partir de los acceptance criteria por story.

**Qué es:** Escenarios de prueba en formato Gherkin que cubren los acceptance criteria: happy path, error paths, edge cases.

**Para qué sirve:** Puente entre los AC (qué validar) y los test cases (cómo validar). Cada scenario se convierte en uno o más test cases.

**Inputs requeridos:**
- `2.7.2` Criteria per Story
- `2.6.3` Error Flows
- `2.6.4` Edge Cases

**Dependencias (predecessors):** `2.7.2` Criteria per Story *(obligatorio)*

**Habilita (successors):** `5.2.1` Test Cases

**Criterio de completitud:**
- [ ] Cada AC tiene al menos 1 test scenario
- [ ] Cubren happy path, error paths y edge cases
- [ ] Formato Gherkin consistente

**Template:** Incluido dentro de `TEMPLATE_ACCEPTANCE_CRITERIA.md`

---

# 2.8 TRACEABILITY MATRIX

**Responsable:** Systems Analyst  
**Aprueba:** QA Lead  
**Objetivo de subfase:** Conectar requisitos con implementación y tests.

---

### 2.8.1 Traceability Matrix

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.8 Traceability Matrix |
| **Responsable** | Systems Analyst |
| **Ejecuta** | Systems Analyst |
| **Aprueba** | QA Lead |
| **Formato** | Excel/Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 2 días |
| **Frecuencia** | Continua (se actualiza con cada sprint) |

**Perfil de ejecución:** SA la produce y mantiene. En VTT: altamente automatizable — un agente puede cruzar los IDs de RF-XXX, UC-XXX, US-XXX, BR-XXX y TC-XXX para generar la matriz automáticamente si el naming convention es consistente.

**Qué es:** Matriz que conecta cada requisito funcional con sus use cases, user stories, business rules y test cases correspondientes. Responde: "¿Este requisito está implementado y testeado?"

**Para qué sirve:** Asegura cobertura completa — ningún requisito se pierde entre analysis y testing. Identifica requisitos sin implementación y tests sin requisito.

**Inputs requeridos:**
- `2.1.2` Requirements List
- `2.3.3` Use Case List
- `2.4.1` Product Backlog
- `2.5.2` Rules List
- `5.2.1` Test Cases (cuando existan)

**Dependencias (predecessors):**
- `2.1.2` Requirements List *(obligatorio)*
- `2.3.3` Use Case List *(obligatorio)*

**Habilita (successors):**
- `2.8.4` Coverage Report
- QA — verificar cobertura de testing

**Secciones esperadas:**

| RF-ID | UC-ID | US-ID | BR-IDs | TC-ID | Estado |
|-------|-------|-------|--------|-------|--------|
| RF-001 | UC-003 | US-012 | BR-005, BR-007 | TC-034 | ✅ Tested |

**Criterio de completitud:**
- [ ] Cada RF tiene al menos 1 UC, 1 US y 1 TC mapeados
- [ ] No hay RFs huérfanos (sin US)
- [ ] No hay TCs huérfanos (sin RF)

**Anti-patrones:**
- ❌ **Matriz estática:** Si no se actualiza por sprint, pierde valor rápidamente.
- ❌ **Solo se llena al final:** Debe construirse progresivamente.

**Template:** `_pm/templates/TEMPLATE_TRACEABILITY.md` *(pendiente)*

---

### 2.8.2 RF to US Mapping

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.8 Traceability Matrix |
| **Responsable** | Systems Analyst |
| **Ejecuta** | Systems Analyst |
| **Aprueba** | QA Lead |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Por sprint |

**Perfil de ejecución:** SA mapea. En VTT: automatizable si los IDs son consistentes en los documentos.

**Qué es:** Mapeo específico de cada requisito funcional a las user stories que lo implementan.

**Para qué sirve:** Verifica que cada requisito aprobado tiene al menos una story que lo implementa.

**Inputs requeridos:** `2.1.2` Requirements List, `2.4.1` Product Backlog

**Dependencias (predecessors):** `2.8.1` Traceability Matrix *(obligatorio)*

**Criterio de completitud:**
- [ ] Cada RF mapeado a al menos 1 US
- [ ] RFs sin US documentados como gaps

**Template:** Incluido dentro de `TEMPLATE_TRACEABILITY.md`

---

### 2.8.3 US to Test Mapping

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.8 Traceability Matrix |
| **Responsable** | Systems Analyst |
| **Ejecuta** | QA Lead + Systems Analyst |
| **Aprueba** | QA Lead |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Por sprint |

**Perfil de ejecución:** QA Lead mapea stories a tests, SA valida cobertura de requisitos. En VTT: automatizable.

**Qué es:** Mapeo de cada user story a los test cases que la validan.

**Para qué sirve:** Verifica que cada story implementada tiene tests que la cubren.

**Inputs requeridos:** `2.4.1` Product Backlog, `2.7.5` Test Scenarios

**Dependencias (predecessors):** `2.8.1` Traceability Matrix *(obligatorio)*

**Criterio de completitud:**
- [ ] Cada US mapeada a al menos 1 TC
- [ ] Stories sin TC documentadas como gaps de testing

**Template:** Incluido dentro de `TEMPLATE_TRACEABILITY.md`

---

### 2.8.4 Coverage Report

| Campo | Valor |
|-------|-------|
| **Fase** | 02-Analysis |
| **Subfase** | 2.8 Traceability Matrix |
| **Responsable** | Systems Analyst |
| **Ejecuta** | Systems Analyst |
| **Aprueba** | QA Lead |
| **Formato** | Report |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Por sprint / por release |

**Perfil de ejecución:** SA genera el reporte. En VTT: automatizable — un agente puede calcular % de cobertura desde la traceability matrix.

**Qué es:** Reporte que muestra el % de cobertura de requisitos: cuántos RFs tienen US, cuántas US tienen TCs, cuántos TCs han sido ejecutados.

**Para qué sirve:** Dashboard de calidad del análisis. Si la cobertura es baja, hay riesgo de entregar features incompletas o no testeadas.

**Inputs requeridos:** `2.8.1` Traceability Matrix completa

**Dependencias (predecessors):** `2.8.1` Traceability Matrix *(obligatorio)*

**Habilita (successors):** Decisión de go/no-go para release

**Secciones esperadas:**
- % RFs con US mapeadas
- % US con TCs mapeados
- % TCs ejecutados y pasando
- Lista de gaps (RFs sin cobertura)

**Criterio de completitud:**
- [ ] Métricas de cobertura calculadas
- [ ] Gaps identificados y comunicados
- [ ] Plan de acción para gaps críticos

**Template:** Incluido dentro de `TEMPLATE_TRACEABILITY.md`

---

# ÍNDICE DE DEPENDENCIAS — FASE 2

```
2.1.1 SRS Document
  └─► 2.1.2, 2.1.3, 2.2.1, 2.3.1, 2.5.1, 2.7.1, 3B.1.1, 5.1.1

2.1.2 Requirements List
  └─► 2.1.3, 2.8.1

2.1.3 Priority Matrix
  └─► 2.4.1, Sprint planning

2.1.4 Feature List
  └─► 2.1.5, 2.4.4

2.1.5 Functional Decomposition
  └─► 3B.1.1

2.1.6 Requirements Approval
  └─► Inicio de Fase 3, 2.4.1

2.2.1 NFR Document
  └─► 2.2.2-2.2.6, 3B.1.1, 5.3.1

2.3.1 Use Case Document
  └─► 2.3.2-2.3.6, 2.4.2, 2.7.2, 5.2.1

2.3.4 Detailed Use Cases
  └─► 2.4.2, 2.5.1, 2.6.1, 2.7.5

2.3.5 Actor Definitions
  └─► 2.3.2, 2.5.5

2.4.1 Product Backlog
  └─► 2.4.2-2.4.6, Sprint planning

2.4.2 User Stories
  └─► 2.4.5, 2.7.2, Development

2.4.5 Story Estimation
  └─► 2.4.6

2.5.1 Business Rules Document
  └─► 2.5.2-2.5.7, 2.4.2, Development

2.5.5 Authorization Rules
  └─► 2.2.3, 3B.1.1

2.6.1 User Flow Diagrams
  └─► 2.6.2-2.6.7, 3A.4.x

2.6.5 User Journey Maps
  └─► 2.4.3, 3A.4.x

2.7.1 Acceptance Criteria Doc
  └─► 2.7.2-2.7.5

2.7.2 Criteria per Story
  └─► 2.7.5, 5.2.1

2.7.3 Definition of Done
  └─► Development (global)

2.7.4 Definition of Ready
  └─► Sprint planning (gate)

2.8.1 Traceability Matrix
  └─► 2.8.2-2.8.4

2.8.4 Coverage Report
  └─► Go/no-go para release
```

---

# RESUMEN DE EJECUTORES — FASE 2

| Deliverable | Responsable | Ejecuta | Delegable a agente VTT |
|-------------|-------------|---------|------------------------|
| 2.1.1 SRS Document | SA | SA | ✅ Sí — draft completo desde MVP + use cases |
| 2.1.2 Requirements List | SA | SA | ✅ Sí — extracción automática |
| 2.1.3 Priority Matrix | SA | SA + PM | 🔶 Parcial — estructura sí, priorización no |
| 2.1.4 Feature List | SA | SA + PM | ✅ Sí — agrupar requisitos |
| 2.1.5 Functional Decomposition | SA | SA | ✅ Sí — diagrama Mermaid |
| 2.1.6 Requirements Approval | SA | PO | ❌ No — acto de aprobación humano |
| 2.2.1 NFR Document | SA | SA + Architect | 🔶 Parcial — estándares sí, targets específicos no |
| 2.2.2 Performance Requirements | SA | SA + TL | 🔶 Parcial — targets estándar sí |
| 2.2.3 Security Requirements | SA | SA + Security | 🔶 Parcial — OWASP sí, amenazas específicas no |
| 2.2.4 Scalability Requirements | SA | SA + Architect | ✅ Sí — calcular desde SOM |
| 2.2.5 Availability Requirements | SA | SA + DevOps | 🔶 Parcial — SLA estándar sí |
| 2.2.6 Usability Requirements | SA | UX + SA | ✅ Sí — WCAG estándar |
| 2.3.1 Use Case Document | SA | SA | ✅ Sí — altamente automatizable |
| 2.3.2 Use Case Diagram | SA | SA | ✅ Sí — Mermaid UML |
| 2.3.3 Use Case List | SA | SA | ✅ Sí — extracción automática |
| 2.3.4 Detailed Use Cases | SA | SA | ✅ Sí — mayor valor por volumen |
| 2.3.5 Actor Definitions | SA | SA | ✅ Sí — derivar de customer profile |
| 2.3.6 Use Case Relationships | SA | SA | ✅ Sí — diagrama automático |
| 2.4.1 Product Backlog | PM | PM | 🔶 Parcial — stories iniciales sí |
| 2.4.2 User Stories | PM | PM + SA | ✅ Sí — Gherkin desde use cases |
| 2.4.3 Story Map | PM | PM | 🔶 Parcial — estructura sí |
| 2.4.4 Epics | PM | PM | ✅ Sí — derivar de features |
| 2.4.5 Story Estimation | PM | TL + Devs | ❌ No — estimación del equipo |
| 2.4.6 Sprint Assignment | PM | PM + TL | 🔶 Parcial — proponer sí |
| 2.5.1 Business Rules Doc | SA | SA | ✅ Sí — extraer de use cases |
| 2.5.2 Rules List | SA | SA | ✅ Sí — extracción automática |
| 2.5.3 Validation Rules | SA | SA | ✅ Sí — por tipo de dato |
| 2.5.4 Calculation Rules | SA | SA | ✅ Sí — formalizar fórmulas |
| 2.5.5 Authorization Rules | SA | SA | ✅ Sí — matriz RBAC |
| 2.5.6 State Transition Rules | SA | SA | ✅ Sí — diagrama Mermaid |
| 2.5.7 Business Glossary | SA | SA | ✅ Sí — extraer términos |
| 2.6.1 User Flow Diagrams | UX | UX | ✅ Sí — desde use cases |
| 2.6.2 Happy Path Flows | UX | UX | ✅ Sí — flujo principal |
| 2.6.3 Error Flows | UX | UX | ✅ Sí — desde flujos alternativos |
| 2.6.4 Edge Cases | UX | UX + SA | ✅ Sí — edge cases comunes |
| 2.6.5 User Journey Maps | UX | UX | 🔶 Parcial — estructura sí, emociones no |
| 2.6.6 Task Flows | UX | UX | ✅ Sí — desde use cases |
| 2.6.7 Navigation Map | UX | UX | ✅ Sí — Mermaid |
| 2.7.1 Acceptance Criteria Doc | QA Lead | QA + SA | ✅ Sí — Gherkin automatizable |
| 2.7.2 Criteria per Story | QA Lead | QA + PM | ✅ Sí — Given/When/Then |
| 2.7.3 Definition of Done | QA Lead | QA + TL | 🔶 Parcial — DoD estándar sí |
| 2.7.4 Definition of Ready | QA Lead | QA + PM | 🔶 Parcial — DoR estándar sí |
| 2.7.5 Test Scenarios | QA Lead | QA + QA Eng | ✅ Sí — Gherkin desde ACs |
| 2.8.1 Traceability Matrix | SA | SA | ✅ Sí — cruce automático de IDs |
| 2.8.2 RF to US Mapping | SA | SA | ✅ Sí — automatizable |
| 2.8.3 US to Test Mapping | SA | QA + SA | ✅ Sí — automatizable |
| 2.8.4 Coverage Report | SA | SA | ✅ Sí — cálculo automático |

---

**Documento:** DICCIONARIO_FASE_02_ANALYSIS.md  
**Versión:** 1.1.0  
**Estado:** ✅ Listo para revisión  
**Siguiente:** DICCIONARIO_FASE_03A_DESIGN_UXUI.md
