# DICCIONARIO DE DELIVERABLES — FASE 3B.9: TECHNICAL ESTIMATES

**Versión:** 1.0  
**Fecha:** 2026-05-14  
**Fase:** 3B — Design Technical  
**Subfase:** 3B.9 — Technical Estimates  
**Total deliverables:** 9  
**Responsable de subfase:** Tech Lead  
**Aprueba:** Solution Architect

---

## Contexto de la subfase

Technical Estimates traduce el diseño técnico en estimaciones de esfuerzo: cuánto toma construir cada parte del sistema. Es el puente entre el diseño (qué construir) y el planning (cuándo estará listo). Las estimaciones alimentan el sprint planning, el release planning, y las expectativas del negocio. Subestimar genera crunches y deuda técnica; sobreestimar desperdicia budget y confianza.

**Prerequisitos de subfase:**
- Solution Architecture (3B.1) — scope técnico definido
- API Design (3B.4) — endpoints a implementar
- Database Design (3B.3) — modelo de datos definido
- User Stories estimadas en story points (2.4.5)

**Entrega de subfase:**
- Estimaciones técnicas completas, ajustadas por riesgo, con dependencias mapeadas y capacidad planificada

---

### 3B.9.1 Technical Estimates

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.9 Technical Estimates |
| **Responsable** | Tech Lead |
| **Ejecuta** | Tech Lead / Development Team |
| **Aprueba** | Solution Architect |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 2-3 días |
| **Frecuencia** | Una vez + refinamiento por sprint |

**Perfil de ejecución:** Requiere experiencia en estimación de software: técnicas (Planning Poker, T-shirt sizing, three-point estimation), factores de ajuste (complejidad, incertidumbre, experiencia del equipo), y calibración histórica.  
En VTT: un agente puede generar la tabla de estimaciones base a partir del task breakdown y la complejidad assessment. NO puede estimar con precisión — las estimaciones requieren juicio del equipo que implementará. Puede facilitar el proceso generando templates y consolidando inputs. Necesita brief con: task breakdown, complexity assessment, y estimaciones del equipo de desarrollo.

**Qué es:** Tabla consolidada de estimaciones de esfuerzo para cada user story o componente técnico: story points, horas estimadas, complejidad, incertidumbre, y dependencias. Incluye estimaciones del equipo (no solo del Tech Lead) obtenidas mediante Planning Poker o técnica similar.

**Para qué sirve:** Las estimaciones son la base para todo planning: cuántos sprints necesitamos, cuándo estará lista cada feature, cuántos developers necesitamos. Sin estimaciones, el planning es ficción. Con estimaciones calibradas, las fechas de entrega son creíbles.

**Inputs requeridos:**
- `2.4.5` Story Estimation — story points por user story
- `3B.9.3` Task Breakdown — tareas por user story
- `3B.9.5` Complexity Assessment — complejidad por componente
- `3B.4.2` Endpoints List — endpoints a implementar
- `3B.3.1` ERD Complete — entidades a modelar

**Dependencias (predecessors):**
- `2.4.5` Story Estimation *(obligatorio)* — estimaciones iniciales
- `3B.9.3` Task Breakdown *(obligatorio)* — tareas identificadas
- `3B.9.5` Complexity Assessment *(obligatorio)* — factores de complejidad

**Habilita (successors):**
- `3B.9.4` Effort Matrix — resumen de esfuerzo por módulo
- `3B.9.6` Risk-adjusted Estimates — estimaciones con buffer
- `3B.9.9` Capacity Planning — planning de equipo
- `2.4.6` Sprint Assignment — asignación a sprints

**Audiencia:**
- **Tech Lead** — planning de sprints
- **Product Manager** — expectativas de entrega
- **Solution Architect** — validación de feasibility
- **Development Team** — compromisos de sprint

**Secciones esperadas:**
1. Metodología de estimación usada (Planning Poker, three-point, T-shirt)
2. Tabla de estimaciones (user story/task, story points, horas, complejidad, incertidumbre, estimador)
3. Assumptions de estimación
4. Factores de ajuste aplicados (new tech, unclear requirements, integration complexity)
5. Confidence level por estimación (high, medium, low)
6. Resumen por epic/módulo

**Criterio de completitud:**
- [ ] Todas las user stories del MVP estimadas
- [ ] Estimaciones del equipo (no solo del Tech Lead)
- [ ] Complejidad e incertidumbre documentadas
- [ ] Assumptions explícitas
- [ ] Confidence level por estimación
- [ ] Metodología documentada

**Anti-patrones:**
- ❌ **Estimaciones del jefe solo:** El Tech Lead estima sin consultar al equipo — compromete al equipo con algo que no validó.
- ❌ **Estimaciones sin incertidumbre:** "Son exactamente 3 días" — las estimaciones son rangos, no certezas.
- ❌ **Anchor bias:** La primera persona dice "5 puntos" y todos conforman — Planning Poker con reveal simultáneo evita esto.
- ❌ **Estimaciones de hace 3 meses:** El scope cambió pero las estimaciones son las originales — recalibrando nunca.

**Template:** `phases/03B-design-technical/deliverables/technical-estimates.md` *(pendiente)*

---

### 3B.9.2 Story Points

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.9 Technical Estimates |
| **Responsable** | Tech Lead |
| **Ejecuta** | Development Team |
| **Aprueba** | Tech Lead |
| **Formato** | En cada User Story |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día (sesión de estimación) |
| **Frecuencia** | Por sprint (refinement) |

**Perfil de ejecución:** Requiere entendimiento de la escala de story points (Fibonacci: 1, 2, 3, 5, 8, 13, 21) y qué representa cada nivel en términos de complejidad relativa.  
En VTT: un agente NO puede asignar story points — los asigna el equipo que implementa en sesiones colaborativas. Puede generar la referencia de calibración (qué user story es un "3" vs un "8") y facilitar la documentación de los resultados. Necesita brief con: resultados de la sesión de Planning Poker.

**Qué es:** Asignación de story points a cada user story usando la escala Fibonacci (1, 2, 3, 5, 8, 13, 21). Los story points miden complejidad relativa, no horas. Se asignan en sesiones de equipo (Planning Poker) comparando cada story con stories de referencia ya calibradas.

**Para qué sirve:** Story points permiten medir la velocity del equipo (cuántos puntos completa por sprint) y usar esa velocity para predecir cuándo se completará el backlog. Son más estables que horas porque miden complejidad relativa (no afectados por experiencia individual ni interrupciones).

**Inputs requeridos:**
- `2.4.1` Product Backlog — user stories a estimar
- `2.4.5` Story Estimation — estimaciones iniciales
- Reference stories calibradas (qué es un "1", qué es un "8")

**Dependencias (predecessors):**
- `2.4.1` Product Backlog *(obligatorio)* — stories a estimar
- `3B.9.5` Complexity Assessment *(recomendado)* — informa la estimación

**Habilita (successors):**
- `3B.9.1` Technical Estimates — consolidated view
- `3B.9.8` Velocity Baseline — velocity derivada de story points
- `2.4.6` Sprint Assignment — stories asignadas por capacity en puntos

**Audiencia:**
- **Development Team** — compromisos de sprint
- **Product Manager** — priorización informada
- **Tech Lead** — sprint capacity planning

**Secciones esperadas:**
1. Escala de story points (Fibonacci con descripción de cada nivel)
2. Reference stories (al menos 3 stories calibradas: small, medium, large)
3. Story points por user story (tabla o anotación en cada story)
4. Distribución (histograma de cuántas stories por tamaño)
5. Outliers (stories > 13 puntos que deben descomponerse)

**Criterio de completitud:**
- [ ] Todas las user stories del sprint/release estimadas
- [ ] Escala de referencia documentada
- [ ] Stories > 13 puntos descompuestas
- [ ] Estimaciones del equipo (no unilaterales)
- [ ] Reference stories definidas para calibración futura

**Anti-patrones:**
- ❌ **Story points = horas:** "1 punto = 1 día" — destruye el concepto de complejidad relativa.
- ❌ **Stories de 21+ puntos:** Demasiado grandes para estimar con confianza — deben descomponerse.
- ❌ **Un estimador:** Solo el Tech Lead estima — pierde la perspectiva del equipo.
- ❌ **Sin reference stories:** Cada sesión empieza de cero sin calibración — inconsistencia entre sprints.

**Template:** `phases/03B-design-technical/deliverables/story-points.md` *(pendiente)*

---

### 3B.9.3 Task Breakdown

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.9 Technical Estimates |
| **Responsable** | Tech Lead |
| **Ejecuta** | Tech Lead / Development Team |
| **Aprueba** | Tech Lead |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Por sprint (refinement) |

**Perfil de ejecución:** Requiere capacidad de descomponer user stories en tareas técnicas implementables (max 1 día por tarea) asignables a un developer.  
En VTT: un agente puede generar el task breakdown de user stories a partir de la arquitectura y el diseño técnico: identificar tasks de backend (API endpoint, service logic, DB migration), frontend (component, page, styling), testing, y docs. Es bastante delegable. Necesita brief con: user story, architecture doc, API endpoints involucrados, y definition of done.

**Qué es:** Descomposición de cada user story en tareas técnicas concretas e implementables. Cada tarea es una unidad de trabajo asignable a un developer, completable en máximo 1 día (4-8 horas), y verificable. Tipos típicos: DB migration, API endpoint, service logic, frontend component, test, documentation.

**Para qué sirve:** Una user story es "Como usuario quiero X" — es el qué. El task breakdown dice el cómo: "crear migration para tabla X, implementar endpoint POST /api/x, crear componente FormX, agregar tests". Permite tracking granular del progreso (no "estoy en la story" sino "terminé 4 de 7 tareas").

**Inputs requeridos:**
- `2.4.1` Product Backlog — user stories a descomponer
- `3B.4.2` Endpoints List — endpoints por story
- `3B.3.1` ERD Complete — tablas afectadas por story
- `3B.2.1` Folder Structure — dónde crear cada archivo

**Dependencias (predecessors):**
- `2.4.1` Product Backlog *(obligatorio)*
- `3B.4.2` Endpoints List *(recomendado)*
- `3B.3.1` ERD Complete *(recomendado)*

**Habilita (successors):**
- `3B.9.1` Technical Estimates — estimaciones por tarea
- `3B.9.7` Dependencies Map — dependencias entre tareas
- Sprint execution — tareas asignables en el sprint board

**Audiencia:**
- **Development Team** — tareas asignables
- **Tech Lead** — tracking de progreso
- **QA Engineer** — sabe qué se implementa para preparar tests

**Secciones esperadas:**
1. Tabla de tareas por user story (US, tarea, tipo, estimación, dependencias, assignee)
2. Tipos de tarea (backend, frontend, database, test, config, docs)
3. Definition of Done por tipo de tarea
4. Tareas de integración y testing
5. Tareas cross-cutting (linting, CI config, deploy)

**Criterio de completitud:**
- [ ] Todas las user stories del sprint descompuestas
- [ ] Cada tarea completable en máximo 1 día
- [ ] Tipo de tarea identificado (backend, frontend, DB, test)
- [ ] Dependencias entre tareas documentadas
- [ ] Definition of Done claro por tarea

**Anti-patrones:**
- ❌ **Tareas de 5 días:** "Implementar módulo de pagos" — demasiado grande, debe descomponerse más.
- ❌ **Solo tareas de código:** No incluir tasks de testing, documentation, ni deployment — se olvidan.
- ❌ **Tasks sin DoD:** "Hacer el login" — ¿incluye tests? ¿validation? ¿error handling? Ambiguo.
- ❌ **Breakdown solo del Tech Lead:** El developer que implementa puede tener mejor visibilidad de las tareas necesarias.

**Template:** `phases/03B-design-technical/deliverables/task-breakdown.md` *(pendiente)*

---

### 3B.9.4 Effort Matrix

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.9 Technical Estimates |
| **Responsable** | Tech Lead |
| **Ejecuta** | Tech Lead |
| **Aprueba** | Solution Architect |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez + actualización por sprint |

**Perfil de ejecución:** Requiere capacidad de agregar estimaciones individuales en una vista consolidada por módulo/epic.  
En VTT: un agente puede generar la effort matrix consolidando las estimaciones por módulo. Es altamente delegable. Necesita brief con: estimaciones técnicas, agrupación por módulo/epic, y categorización por tipo de trabajo.

**Qué es:** Vista consolidada del esfuerzo por módulo/epic: tabla cruzada que muestra story points o días por módulo y por tipo de trabajo (backend, frontend, DB, testing, DevOps). Permite ver de un vistazo dónde está la mayor concentración de esfuerzo y si la distribución entre frontend/backend es balanceada.

**Para qué sirve:** Identifica dónde está el "peso" del proyecto: si el 60% del esfuerzo es backend, se necesitan más backend developers. Si un módulo concentra el 40% del esfuerzo, es el critical path. La matrix informa decisiones de staffing y planificación.

**Inputs requeridos:**
- `3B.9.1` Technical Estimates — estimaciones individuales
- `2.4.4` Epics — agrupación de stories
- `3B.9.3` Task Breakdown — categorización por tipo

**Dependencias (predecessors):**
- `3B.9.1` Technical Estimates *(obligatorio)*
- `2.4.4` Epics *(obligatorio)*

**Habilita (successors):**
- `3B.9.9` Capacity Planning — distribución de trabajo por equipo
- Sprint planning — balance de carga por sprint

**Audiencia:**
- **Tech Lead** — staffing decisions
- **Product Manager** — priorización informada por esfuerzo
- **Solution Architect** — validación de distribución

**Secciones esperadas:**
1. Effort matrix (tabla: módulo/epic × tipo de trabajo = story points)
2. Totales por módulo y por tipo
3. Distribución porcentual (qué % es backend, frontend, testing)
4. Módulos de mayor esfuerzo identificados
5. Visualización (bar chart o heatmap)

**Criterio de completitud:**
- [ ] Todos los módulos/epics incluidos
- [ ] Esfuerzo desglosado por tipo de trabajo
- [ ] Totales calculados
- [ ] Módulos de mayor esfuerzo identificados
- [ ] Distribución frontend/backend visible

**Anti-patrones:**
- ❌ **Sin desglose por tipo:** Solo total por módulo sin saber cuánto es backend vs frontend — no informa staffing.
- ❌ **Testing no incluido:** Solo esfuerzo de desarrollo sin testing — subestimación del 30-40% del esfuerzo real.
- ❌ **Matrix estática:** No actualizarla con las estimaciones refinadas — se vuelve irrelevante.

**Template:** `phases/03B-design-technical/deliverables/effort-matrix.md` *(pendiente)*

---

### 3B.9.5 Complexity Assessment

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.9 Technical Estimates |
| **Responsable** | Tech Lead |
| **Ejecuta** | Tech Lead / Solution Architect |
| **Aprueba** | Solution Architect |
| **Formato** | Documento (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere capacidad de evaluar complejidad técnica desde múltiples dimensiones: algorítmica, de integración, de concurrencia, de datos, y de UX.  
En VTT: un agente puede evaluar complejidad basándose en criterios predefinidos y el diseño técnico. Es parcialmente delegable. Necesita brief con: módulos a evaluar, criterios de complejidad, y observaciones del Tech Lead.

**Qué es:** Evaluación de la complejidad técnica de cada módulo/componente del sistema en múltiples dimensiones: complejidad algorítmica (lógica de negocio), complejidad de integración (APIs externas), complejidad de datos (modelo, volumen, consistencia), complejidad de UX (interacciones complejas), y complejidad de infraestructura (escalado, deployment). Cada dimensión se puntúa (1-5) y se documenta la justificación.

**Para qué sirve:** La complejidad es el factor #1 de error en estimaciones. Un módulo "simple" con una integración compleja puede tomar 3x más de lo esperado. El assessment hace visible la complejidad oculta antes de estimar, permitiendo ajustar las estimaciones y asignar developers con la experiencia adecuada.

**Inputs requeridos:**
- `3B.1.4` Component Diagram — módulos a evaluar
- `3B.1.6` Integration Points — complejidad de integraciones
- `2.5.1` Business Rules Document — complejidad de lógica de negocio
- `3B.3.1` ERD Complete — complejidad del modelo de datos

**Dependencias (predecessors):**
- `3B.1.4` Component Diagram *(obligatorio)*
- `3B.1.6` Integration Points *(recomendado)*
- `2.5.1` Business Rules Document *(recomendado)*

**Habilita (successors):**
- `3B.9.1` Technical Estimates — complejidad informa estimaciones
- `3B.9.2` Story Points — complejidad informa puntos
- `3B.9.6` Risk-adjusted Estimates — riesgo correlaciona con complejidad

**Audiencia:**
- **Tech Lead** — asignación de developers apropiados
- **Solution Architect** — identificación de riesgos técnicos
- **Product Manager** — priorización informada

**Secciones esperadas:**
1. Criterios de complejidad (algorítmica, integración, datos, UX, infra — escala 1-5)
2. Tabla de assessment (módulo × dimensión = score)
3. Justificación por módulo de alta complejidad
4. Módulos de mayor riesgo (score total alto)
5. Mitigaciones recomendadas (spike, PoC, pair programming)
6. Mapping complejidad → developer assignment

**Criterio de completitud:**
- [ ] Todos los módulos principales evaluados
- [ ] Múltiples dimensiones de complejidad evaluadas
- [ ] Justificación para scores altos (≥4)
- [ ] Módulos de alto riesgo identificados
- [ ] Mitigaciones propuestas para módulos complejos

**Anti-patrones:**
- ❌ **"Todo es mediano":** Todos los módulos con complejidad 3/5 — assessment que no diferencia y no informa decisiones.
- ❌ **Solo complejidad algorítmica:** Ignorar complejidad de integración, datos, o UX — subestimación de módulos "simples" con integraciones difíciles.
- ❌ **Assessment sin consecuencias:** Identificar módulos complejos pero no ajustar estimaciones ni asignaciones.

**Template:** `phases/03B-design-technical/deliverables/complexity-assessment.md` *(pendiente)*

---

### 3B.9.6 Risk-adjusted Estimates

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.9 Technical Estimates |
| **Responsable** | Tech Lead |
| **Ejecuta** | Tech Lead |
| **Aprueba** | Solution Architect |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez + actualización por sprint |

**Perfil de ejecución:** Requiere experiencia en estimación bajo incertidumbre y técnicas de risk buffering.  
En VTT: un agente puede calcular estimaciones ajustadas aplicando factores de riesgo a las estimaciones base. Es altamente delegable. Necesita brief con: estimaciones base, complejidad, incertidumbre por tarea, y factor de buffer.

**Qué es:** Estimaciones que incluyen buffers por riesgo e incertidumbre: three-point estimation (optimista, probable, pesimista), risk multipliers por complejidad (complejidad alta = 1.5x), y contingency buffer global (10-20%). Produce rangos de estimación en lugar de números fijos.

**Para qué sirve:** Las estimaciones base son el "caso probable". Los risk-adjusted estimates dan el rango realista. Cuando el PM pregunta "¿cuándo estará listo?", la respuesta es un rango con confidence: "entre 8 y 12 semanas, con 80% de confidence en 10 semanas". Es más honesto y más útil que un solo número.

**Inputs requeridos:**
- `3B.9.1` Technical Estimates — estimaciones base
- `3B.9.5` Complexity Assessment — factores de riesgo
- `1.4.1` Risk Register — riesgos técnicos identificados

**Dependencias (predecessors):**
- `3B.9.1` Technical Estimates *(obligatorio)*
- `3B.9.5` Complexity Assessment *(obligatorio)*
- `1.4.1` Risk Register *(recomendado)*

**Habilita (successors):**
- `3B.9.9` Capacity Planning — planning con rangos
- `2.4.6` Sprint Assignment — capacity con buffer
- Release planning — fechas con confidence levels

**Audiencia:**
- **Product Manager** — expectativas realistas
- **Tech Lead** — planning con buffer
- **Management** — release dates con rangos

**Secciones esperadas:**
1. Metodología de ajuste (three-point, risk multiplier, contingency %)
2. Tabla ajustada (task, estimate base, optimista, probable, pesimista, adjusted)
3. Risk multipliers por complejidad (1.0x, 1.3x, 1.5x, 2.0x)
4. Contingency buffer global (% y justificación)
5. Rangos de entrega por epic (best case, expected, worst case)
6. Confidence levels (% de confidence en cada rango)

**Criterio de completitud:**
- [ ] Estimaciones base ajustadas con riesgo
- [ ] Three-point estimation para tareas de alta incertidumbre
- [ ] Contingency buffer documentado y justificado
- [ ] Rangos de entrega calculados
- [ ] Confidence levels asignados

**Anti-patrones:**
- ❌ **Estimaciones sin buffer:** Dar el caso optimista como fecha de entrega — falla garantizada.
- ❌ **Buffer demasiado grande:** 100% de buffer "por si acaso" — pierde credibilidad y el buffer se consume en Parkinson's Law.
- ❌ **Un solo número:** "Estará listo el 15 de julio" sin rango — falsa precisión.
- ❌ **Buffer oculto:** Cada developer agrega buffer secreto + el TL agrega más + el PM agrega más — estimaciones infladas x3.

**Template:** `phases/03B-design-technical/deliverables/risk-adjusted-estimates.md` *(pendiente)*

---

### 3B.9.7 Dependencies Map

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.9 Technical Estimates |
| **Responsable** | Tech Lead |
| **Ejecuta** | Tech Lead |
| **Aprueba** | Solution Architect |
| **Formato** | Diagrama |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5-1 día |
| **Frecuencia** | Una vez + actualizaciones por sprint |

**Perfil de ejecución:** Requiere capacidad de identificar dependencias entre tareas y definir el critical path.  
En VTT: un agente puede generar el mapa de dependencias en Mermaid (Gantt o graph) a partir del task breakdown. Es altamente delegable. Necesita brief con: task breakdown con dependencias, y orden de ejecución esperado.

**Qué es:** Diagrama que muestra las dependencias entre tareas de desarrollo: qué tareas deben completarse antes de que otras puedan empezar (finish-to-start), qué tareas pueden ejecutarse en paralelo, y cuál es el critical path (la secuencia más larga que determina la duración mínima del proyecto).

**Para qué sirve:** Sin mapa de dependencias, los developers empiezan tareas que dependen de otras no completadas — bloqueos, retrabajo, idle time. El mapa permite: secuenciar el trabajo correctamente, identificar el critical path (donde cualquier retraso retrasa todo), y maximizar paralelismo.

**Inputs requeridos:**
- `3B.9.3` Task Breakdown — tareas con dependencias
- `3B.2.4` Module Dependencies — dependencias entre módulos
- `3B.4.2` Endpoints List — dependencias de API

**Dependencias (predecessors):**
- `3B.9.3` Task Breakdown *(obligatorio)*
- `3B.2.4` Module Dependencies *(recomendado)*

**Habilita (successors):**
- `2.4.6` Sprint Assignment — sequencing de tareas
- `3B.9.9` Capacity Planning — paralelismo posible
- Sprint planning — asignación sin bloqueos

**Audiencia:**
- **Tech Lead** — sequencing y sprint planning
- **Development Team** — saber qué puede empezarse
- **Product Manager** — critical path visibility

**Secciones esperadas:**
1. Diagrama de dependencias (directed graph o Gantt)
2. Critical path identificado y resaltado
3. Tareas paralelizables identificadas
4. Dependencias externas (API de terceros, decisiones pendientes)
5. Bottlenecks (tareas de las que muchas otras dependen)
6. Sugerencias de secuenciación (qué empezar primero)

**Criterio de completitud:**
- [ ] Todas las tareas del task breakdown incluidas
- [ ] Dependencias finish-to-start documentadas
- [ ] Critical path identificado
- [ ] Tareas paralelizables identificadas
- [ ] Dependencias externas listadas
- [ ] Bottlenecks identificados

**Anti-patrones:**
- ❌ **Todo secuencial:** Ninguna tarea en paralelo — maximiza la duración del proyecto.
- ❌ **Sin dependencias:** Todas las tareas "independientes" — se descubren bloqueos durante el sprint.
- ❌ **Ignorar dependencias externas:** No contar con que la API de Stripe toma 5 días en aprobar la cuenta sandbox.

**Template:** `phases/03B-design-technical/deliverables/dependencies-map.mmd` *(pendiente)*

---

### 3B.9.8 Velocity Baseline

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.9 Technical Estimates |
| **Responsable** | Tech Lead |
| **Ejecuta** | Tech Lead |
| **Aprueba** | Tech Lead |
| **Formato** | Métrica |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.25 día (setup) + medición continua |
| **Frecuencia** | Por sprint (se calibra con cada sprint completado) |

**Perfil de ejecución:** Requiere entendimiento de velocity en Scrum y cómo usarla para forecasting sin caer en abusos (velocity como target, velocity como evaluación).  
En VTT: un agente puede calcular velocity baseline y forecasts a partir de datos de sprints completados. Es altamente delegable. Necesita brief con: story points comprometidos vs completados por sprint, y sprint length.

**Qué es:** Métrica que establece cuántos story points el equipo completa por sprint. Se calcula después de los primeros 2-3 sprints como promedio. Es la base para forecasting: si el equipo hace 30 puntos/sprint y quedan 150 puntos, faltan ~5 sprints.

**Para qué sirve:** La velocity transforma los story points en fechas. Sin velocity, los story points son números abstractos. Con velocity, el PM puede decir "a 30 puntos/sprint, el release de 150 puntos estará listo en 5 sprints ≈ 10 semanas". También detecta problemas: si la velocity baja, algo está bloqueando al equipo.

**Inputs requeridos:**
- `3B.9.2` Story Points — puntos por sprint
- Datos de sprints completados (comprometido vs completado)
- Sprint length (2 semanas típico)

**Dependencias (predecessors):**
- `3B.9.2` Story Points *(obligatorio)*
- Al menos 1 sprint completado (para datos reales; antes es estimación)

**Habilita (successors):**
- `3B.9.9` Capacity Planning — velocity informa capacity
- Release planning — forecasting de entrega
- Sprint planning — capacity por sprint

**Audiencia:**
- **Tech Lead** — sprint capacity
- **Product Manager** — forecasting de releases
- **Scrum Master** — health metrics del equipo

**Secciones esperadas:**
1. Velocity inicial estimada (antes del primer sprint — basada en experiencia)
2. Velocity observada por sprint (tabla: sprint, committed, completed, velocity)
3. Velocity promedio (rolling average de últimos 3 sprints)
4. Velocity range (min, avg, max — para forecasting con rangos)
5. Factores que afectan velocity (vacaciones, ramp-up, deuda técnica)
6. Forecasting con velocity (backlog restante / velocity = sprints restantes)

**Criterio de completitud:**
- [ ] Velocity inicial estimada (pre-sprint 1)
- [ ] Tracking configurado para medir automáticamente
- [ ] Metodología de cálculo documentada (average de últimos N sprints)
- [ ] Forecasting formula documentada
- [ ] Factores de ajuste identificados

**Anti-patrones:**
- ❌ **Velocity como target:** "Este sprint DEBEN hacer 40 puntos" — convierte la medición en presión, los developers inflan estimaciones.
- ❌ **Velocity como evaluación:** "Tu velocity es menor que la del otro equipo" — velocity no es comparable entre equipos.
- ❌ **Velocity del sprint 1 como baseline:** El primer sprint siempre es atípico (setup, learning) — esperar 2-3 sprints para calibrar.
- ❌ **Sin factores de ajuste:** Usar la misma velocity en un sprint con 3 feriados — forecasting irreal.

**Template:** `phases/03B-design-technical/deliverables/velocity-baseline.md` *(pendiente)*

---

### 3B.9.9 Capacity Planning

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.9 Technical Estimates |
| **Responsable** | Tech Lead |
| **Ejecuta** | Tech Lead / Program Manager |
| **Aprueba** | Solution Architect |
| **Formato** | Documento (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez + ajuste por sprint |

**Perfil de ejecución:** Requiere visión de staffing, skills del equipo, y capacity constraints (vacaciones, onboarding, meetings overhead).  
En VTT: un agente puede generar el capacity plan a partir de: equipo disponible, velocity, backlog, y calendar. Es bastante delegable. Necesita brief con: team roster con skills, availability por sprint, velocity baseline, y backlog estimado.

**Qué es:** Plan que alinea el esfuerzo estimado con la capacidad real del equipo: quién está disponible, cuántas horas efectivas por sprint (descontando meetings, vacaciones, on-call), qué skills tiene cada developer, y cómo se distribuye el trabajo para maximizar throughput sin sobrecargar a nadie.

**Para qué sirve:** Las estimaciones dicen cuánto trabajo hay. La capacidad dice cuánto trabajo puede hacerse. El capacity planning reconcilia ambos: si hay 200 puntos de trabajo y el equipo hace 30/sprint, se necesitan ~7 sprints o más developers. También identifica bottlenecks de skills: si solo 1 developer sabe DevOps y hay 40 puntos de infra, esa persona es cuello de botella.

**Inputs requeridos:**
- `3B.9.1` Technical Estimates — esfuerzo total
- `3B.9.4` Effort Matrix — distribución por tipo de trabajo
- `3B.9.8` Velocity Baseline — capacidad por sprint
- Team roster con skills y availability
- Calendar (vacaciones, feriados, training)

**Dependencias (predecessors):**
- `3B.9.1` Technical Estimates *(obligatorio)*
- `3B.9.4` Effort Matrix *(obligatorio)*
- `3B.9.8` Velocity Baseline *(recomendado)*

**Habilita (successors):**
- `2.4.6` Sprint Assignment — sprints planificados con capacity real
- Release planning — fechas realistas basadas en capacity
- Staffing decisions — contratar, subcontratar, o reducir scope

**Audiencia:**
- **Tech Lead** — distribución de trabajo
- **Program Manager** — resource planning
- **Product Manager** — expectativas de entrega
- **Management** — staffing decisions

**Secciones esperadas:**
1. Team roster (nombre, rol, skills, availability %)
2. Capacity por sprint (horas o puntos disponibles por persona)
3. Overhead factors (meetings 20%, code review 10%, on-call 5%, etc.)
4. Skills matrix (developer × skill = proficiency level)
5. Bottlenecks de skills (skills que solo 1-2 personas tienen)
6. Capacity vs demand (tabla: sprint, capacity disponible, demand estimada, gap)
7. Scenarios (a) current team, (b) +1 developer, (c) reduced scope
8. Recommendations (contratar, reducir scope, defer features, o adjustar timeline)

**Criterio de completitud:**
- [ ] Team roster con availability real (no 100% para nadie)
- [ ] Overhead factors aplicados (meetings, reviews, etc.)
- [ ] Skills matrix documentada
- [ ] Bottlenecks identificados
- [ ] Capacity vs demand calculado
- [ ] Al menos 2 scenarios evaluados
- [ ] Recommendation clara

**Anti-patrones:**
- ❌ **100% availability:** Asumir que cada developer produce 8h/día de código — irrealista (meetings, reviews, interrupciones, learning).
- ❌ **Sin skills matrix:** Asumir que todos los developers son fungibles — un frontend dev no reemplaza a un DBA.
- ❌ **Capacity planning sin buffer:** Sprint lleno al 100% de capacity — cero margen para sorpresas, el sprint falla.
- ❌ **Ignorar ramp-up:** Nuevo developer produce al 100% desde día 1 — realísticamente, 50% el primer sprint, 75% el segundo.

**Template:** `phases/03B-design-technical/deliverables/capacity-planning.md` *(pendiente)*

---

## Tabla resumen de ejecutores — Fase 3B.9 Technical Estimates

| Deliverable | Responsable | Ejecuta | Delegable VTT |
|-------------|-------------|---------|---------------|
| 3B.9.1 Technical Estimates | Tech Lead | Tech Lead / Dev Team | 🔶 Parcial — puede consolidar, pero estimar requiere el equipo |
| 3B.9.2 Story Points | Tech Lead | Development Team | ❌ — los asigna el equipo en sesión colaborativa |
| 3B.9.3 Task Breakdown | Tech Lead | Tech Lead / Dev Team | ✅ — puede generar breakdown desde arquitectura y endpoints |
| 3B.9.4 Effort Matrix | Tech Lead | Tech Lead | ✅ — puede consolidar estimaciones en matrix |
| 3B.9.5 Complexity Assessment | Tech Lead | Tech Lead / Sol. Architect | 🔶 Parcial — puede evaluar con criterios, pero juicio requiere experiencia |
| 3B.9.6 Risk-adjusted Estimates | Tech Lead | Tech Lead | ✅ — puede calcular ajustes aplicando factores y three-point |
| 3B.9.7 Dependencies Map | Tech Lead | Tech Lead | ✅ — puede generar mapa en Mermaid desde task breakdown |
| 3B.9.8 Velocity Baseline | Tech Lead | Tech Lead | ✅ — puede calcular y hacer forecasting desde datos de sprints |
| 3B.9.9 Capacity Planning | Tech Lead | Tech Lead / Program Mgr | 🔶 Parcial — puede generar plan, pero staffing decisions son humanas |

---

## Resumen de cierre — Fase 3B Design Technical completa

Con este archivo se completa la **Fase 3B: Design Technical** del diccionario de deliverables.

| Subfase | Archivo | Deliverables | Status |
|---------|---------|-------------|--------|
| 3B.1 Solution Architecture | `DICCIONARIO_FASE_03B_01_SOLUTION_ARCHITECTURE.md` | 7 | ✅ |
| 3B.2 Code Architecture | `DICCIONARIO_FASE_03B_02_CODE_ARCHITECTURE.md` | 6 | ✅ |
| 3B.3 Database Design | `DICCIONARIO_FASE_03B_03_DATABASE_DESIGN.md` | 8 | ✅ |
| 3B.4 API Design | `DICCIONARIO_FASE_03B_04_API_DESIGN.md` | 11 | ✅ |
| 3B.5 Sequence Diagrams | `DICCIONARIO_FASE_03B_05_SEQUENCE_DIAGRAMS.md` | 6 | ✅ |
| 3B.6 ADR | `DICCIONARIO_FASE_03B_06_ADR.md` | 4 | ✅ |
| 3B.7 Security Plan | `DICCIONARIO_FASE_03B_07_SECURITY_PLAN.md` | 11 | ✅ |
| 3B.8 Infrastructure Plan | `DICCIONARIO_FASE_03B_08_INFRASTRUCTURE_PLAN.md` | 11 | ✅ |
| 3B.9 Technical Estimates | `DICCIONARIO_FASE_03B_09_TECHNICAL_ESTIMATES.md` | 9 | ✅ |
| **TOTAL FASE 3B** | **9 archivos** | **73** | **✅ Completa** |

---

## Siguiente archivo

**Próximo:** `DICCIONARIO_FASE_04_01_ENVIRONMENT_SETUP.md` — Fase 4: Development  
**Nota:** Fase 4 tiene 78 deliverables en 8 subfases. Se dividirá en un archivo por subfase.  
**Primer archivo:** 4.1 Environment Setup
