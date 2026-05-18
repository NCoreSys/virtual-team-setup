# DICCIONARIO DE DELIVERABLES — FASE 1: PLANNING

**Versión:** 1.1.0  
**Fecha:** 2026-05-14  
**Total deliverables:** 33  
**Objetivo de fase:** Definir QUÉ se va a construir, PARA QUIÉN, CUÁNDO y CON QUÉ recursos.  
**Duración típica:** 1-2 semanas  
**Criterio de salida de fase:** Plan de proyecto aprobado por stakeholders.

---

## Roles involucrados en esta fase

| Rol | Nivel | Participa en |
|-----|-------|-------------|
| Product Owner (PO) | ●●● Principal | Todas las subfases |
| Product Manager (PM) | ●●● Principal | 1.1, 1.2 |
| Program Manager (PgM) | ●●● Principal | 1.3, 1.4, 1.5, 1.6 |
| Systems Analyst (SA) | ●● Activo | 1.2, 1.4 |
| Solution Architect | ● Participa | 1.4, 1.5 |
| Tech Lead (TL) | ●● Activo | 1.4, 1.5, 1.6 |
| Design Lead | ● Participa | 1.5 |

---

# 1.1 VISION & OBJECTIVES

**Responsable:** Product Owner  
**Aprueba:** Product Owner  
**Objetivo de subfase:** Establecer la visión del producto y los objetivos medibles.

---

### 1.1.1 Vision Statement

| Campo | Valor |
|-------|-------|
| **Fase** | 01-Planning |
| **Subfase** | 1.1 Vision & Objectives |
| **Responsable** | Product Owner |
| **Ejecuta** | Product Owner |
| **Aprueba** | Product Owner |
| **Formato** | 1-2 párrafos |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Una vez (raramente cambia) |

**Perfil de ejecución:** La visión es la declaración fundacional del PO — su apuesta de largo plazo. No es delegable porque refleja la dirección estratégica personal del PO. En VTT: un agente puede proponer opciones de redacción basado en el Problem Statement y el UVP, pero el PO selecciona y reescribe con su voz.

**Qué es:** Declaración aspiracional de lo que el producto será a largo plazo (3-5 años). No es lo que construyes hoy — es hacia dónde vas.

**Para qué sirve:** Alinea al equipo en una dirección compartida cuando hay que tomar decisiones de trade-off. "¿Esta decisión nos acerca a la visión?" es el filtro.

**Inputs requeridos:**
- `0.3.1` Problem Statement — el problema que se resuelve
- `0.4.2` UVP Statement — la propuesta de valor
- `0.3.4` Why Now — el contexto temporal
- Visión personal del PO sobre el futuro del dominio

**Dependencias (predecessors):**
- `0.3.1` Problem Statement *(obligatorio)*
- `0.4.2` UVP Statement *(obligatorio)*

**Habilita (successors):**
- `1.1.2` Mission Statement — la misión operacionaliza la visión
- `1.1.3` Product Goals — objetivos concretos derivados de la visión
- `1.2.1` Scope Statement — el alcance se define dentro de la visión

**Audiencia:**
- Todo el equipo — motivación y dirección
- Investors/stakeholders — alineamiento estratégico

**Secciones esperadas:**
1-2 párrafos que respondan: "¿En qué mundo vivimos cuando este producto triunfa?"

**Criterio de completitud:**
- [ ] Aspiracional pero creíble
- [ ] No describe features sino el resultado en el mundo
- [ ] Horizonte de 3-5 años
- [ ] Cualquier miembro del equipo puede parafrasearla

**Anti-patrones:**
- ❌ **Visión como feature list:** "Seremos una plataforma con IA, dashboard y analytics" — eso es un roadmap, no una visión.
- ❌ **Visión genérica:** "Transformar la educación" — aplica a miles de productos.
- ❌ **Visión inalcanzable:** "Eliminar el analfabetismo global" — aspira pero no guía decisiones.

**Template:** `_pm/templates/TEMPLATE_VISION_OBJECTIVES.md` *(pendiente)*

---

### 1.1.2 Mission Statement

| Campo | Valor |
|-------|-------|
| **Fase** | 01-Planning |
| **Subfase** | 1.1 Vision & Objectives |
| **Responsable** | Product Owner |
| **Ejecuta** | Product Owner |
| **Aprueba** | Product Owner |
| **Formato** | 1 párrafo |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Igual que la visión, es redacción personal del PO. En VTT: un agente puede generar opciones, pero la versión final es del PO.

**Qué es:** Declaración de lo que el producto hace HOY y para quién. Si la visión es el destino, la misión es el vehículo.

**Para qué sirve:** Define el alcance operativo actual del producto. Acota lo que el equipo construye AHORA vs lo que queda para el futuro.

**Inputs requeridos:**
- `1.1.1` Vision Statement
- `0.4.2` UVP Statement
- `0.1.5` Target Market

**Dependencias (predecessors):**
- `1.1.1` Vision Statement *(obligatorio)*

**Habilita (successors):**
- `1.1.3` Product Goals
- `1.2.1` Scope Statement

**Criterio de completitud:**
- [ ] Describe qué hace el producto (no qué será)
- [ ] Menciona para quién
- [ ] Diferenciable de la misión de un competidor

**Anti-patrones:**
- ❌ **Misión = Visión:** Si suenan igual, una de las dos está mal. La visión es futuro, la misión es presente.

**Template:** Incluido dentro de `TEMPLATE_VISION_OBJECTIVES.md`

---

### 1.1.3 Product Goals

| Campo | Valor |
|-------|-------|
| **Fase** | 01-Planning |
| **Subfase** | 1.1 Vision & Objectives |
| **Responsable** | Product Owner |
| **Ejecuta** | Product Manager |
| **Aprueba** | Product Owner |
| **Formato** | Lista |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez + revisión trimestral |

**Perfil de ejecución:** El PM traduce la visión y misión del PO en objetivos SMART concretos. Requiere capacidad de definir métricas y targets. En VTT: un agente puede proponer goals basado en la visión, misión y value hypothesis, pero el PM valida que sean realistas y el PO aprueba las prioridades.

**Qué es:** Lista de objetivos SMART (Specific, Measurable, Achievable, Relevant, Time-bound) del producto para el horizonte del proyecto.

**Para qué sirve:** Traduce la visión abstracta en metas concretas y medibles. Cada sprint y cada feature se justifica contra estos goals.

**Inputs requeridos:**
- `1.1.1` Vision Statement
- `1.1.2` Mission Statement
- `0.4.5` Value Hypothesis — las hipótesis implican goals
- `0.1.2` TAM/SAM/SOM — para dimensionar targets

**Dependencias (predecessors):**
- `1.1.1` Vision Statement *(obligatorio)*
- `1.1.2` Mission Statement *(obligatorio)*

**Habilita (successors):**
- `1.1.4` Success Metrics — métricas para medir los goals
- `1.1.6` OKRs — goals se convierten en OKRs
- `1.2.1` Scope Statement — el alcance se define para lograr los goals

**Criterio de completitud:**
- [ ] 3-7 goals definidos
- [ ] Cada uno cumple criterio SMART
- [ ] Priorizados
- [ ] Alineados con la visión (no goals "sueltos")

**Anti-patrones:**
- ❌ **Goals vagos:** "Crecer" no es SMART. "Alcanzar 500 usuarios activos en Q3 2026" sí.
- ❌ **Goals sin ownership:** Cada goal debe tener un responsable de lograrlo.
- ❌ **Demasiados goals:** Más de 7 diluye el foco.

**Template:** Incluido dentro de `TEMPLATE_VISION_OBJECTIVES.md`

---

### 1.1.4 Success Metrics (KPIs)

| Campo | Valor |
|-------|-------|
| **Fase** | 01-Planning |
| **Subfase** | 1.1 Vision & Objectives |
| **Responsable** | Product Owner |
| **Ejecuta** | Product Manager |
| **Aprueba** | Product Owner |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez + revisión mensual de valores |

**Perfil de ejecución:** El PM define las métricas, los targets y la frecuencia de medición. Requiere entender analytics y data. En VTT: un agente puede proponer KPIs estándar de la industria (churn rate, DAU, NPS, etc.) y el PM selecciona los relevantes y define targets.

**Qué es:** Tabla de métricas clave con target, frecuencia de medición y responsable de tracking. Cada KPI mapea a un Product Goal.

**Para qué sirve:** Sin métricas, no sabes si estás ganando o perdiendo. Los KPIs convierten los goals en números rastreables.

**Inputs requeridos:**
- `1.1.3` Product Goals — cada goal tiene al menos 1 KPI
- `0.4.5` Value Hypothesis — cada hipótesis tiene una métrica
- Benchmarks de industria para targets realistas

**Dependencias (predecessors):**
- `1.1.3` Product Goals *(obligatorio)*
- `0.4.5` Value Hypothesis *(recomendado)*

**Habilita (successors):**
- `1.1.5` North Star Metric — se selecciona de estos KPIs
- `1.1.6` OKRs — los Key Results son KPIs
- `6.6.1` Monitoring Dashboard — dashboard trackea estos KPIs

**Secciones esperadas:**

| KPI | Goal asociado | Target | Frecuencia | Responsable | Fuente de datos |
|-----|--------------|--------|------------|-------------|----------------|

**Criterio de completitud:**
- [ ] Cada Product Goal tiene al menos 1 KPI
- [ ] Cada KPI tiene target numérico
- [ ] Fuente de datos identificada (de dónde sale el número)
- [ ] Frecuencia de medición definida

**Anti-patrones:**
- ❌ **Vanity metrics:** Pageviews y downloads sin contexto de retención.
- ❌ **KPIs sin target:** "Medir NPS" sin decir qué NPS es aceptable.
- ❌ **KPIs no medibles:** Si no puedes obtener el dato, no es un KPI.

**Template:** Incluido dentro de `TEMPLATE_VISION_OBJECTIVES.md`

---

### 1.1.5 North Star Metric

| Campo | Valor |
|-------|-------|
| **Fase** | 01-Planning |
| **Subfase** | 1.1 Vision & Objectives |
| **Responsable** | Product Owner |
| **Ejecuta** | Product Owner |
| **Aprueba** | Product Owner |
| **Formato** | 1 métrica |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Una vez (raramente cambia) |

**Perfil de ejecución:** Decisión estratégica del PO — elegir LA métrica que mejor captura si el producto genera valor. No es delegable. En VTT: un agente puede listar candidatos de los KPIs, pero el PO elige cuál es la que importa más.

**Qué es:** La única métrica que, si sube, significa que el producto está cumpliendo su propósito. Es la brújula cuando hay conflicto entre KPIs.

**Para qué sirve:** Cuando dos features compiten por prioridad, la que mueve el North Star gana. Simplifica la toma de decisiones.

**Inputs requeridos:**
- `1.1.4` Success Metrics — candidatos
- `0.4.1` Value Proposition Canvas — la métrica debe reflejar el valor creado

**Dependencias (predecessors):**
- `1.1.4` Success Metrics *(obligatorio)*

**Habilita (successors):**
- Priorización de backlog y roadmap
- `6.6.1` Monitoring Dashboard — la métrica más prominente

**Criterio de completitud:**
- [ ] Es una sola métrica (no dos ni tres)
- [ ] Refleja valor entregado al usuario (no revenue ni vanity)
- [ ] Todo el equipo la conoce

**Anti-patrones:**
- ❌ **Revenue como North Star:** El revenue es resultado, no causa. La métrica debe capturar el valor (ej: "horas de transcripción procesadas" no "MRR").
- ❌ **Métrica que no mueve el equipo:** Si el desarrollador no puede conectar su trabajo con la North Star, no sirve.

**Template:** Incluido dentro de `TEMPLATE_VISION_OBJECTIVES.md`

---

### 1.1.6 OKRs

| Campo | Valor |
|-------|-------|
| **Fase** | 01-Planning |
| **Subfase** | 1.1 Vision & Objectives |
| **Responsable** | Product Owner |
| **Ejecuta** | Product Manager + Program Manager |
| **Aprueba** | Product Owner |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Trimestral |

**Perfil de ejecución:** PM y PgM traducen los goals y KPIs en formato OKR. El PM define los Objectives, el PgM contribuye los Key Results operativos. En VTT: un agente puede formatear OKRs a partir de los goals y KPIs ya definidos — es una tarea de estructuración más que de estrategia.

**Qué es:** Objectives & Key Results — framework que conecta objetivos cualitativos (Objectives) con resultados cuantitativos (Key Results). Típicamente 3-5 Objectives con 2-4 KRs cada uno.

**Para qué sirve:** Operacionaliza los goals en ciclos trimestrales. Permite tracking de progreso y ajuste de dirección.

**Inputs requeridos:**
- `1.1.3` Product Goals
- `1.1.4` Success Metrics
- `1.1.5` North Star Metric

**Dependencias (predecessors):**
- `1.1.3` Product Goals *(obligatorio)*
- `1.1.4` Success Metrics *(obligatorio)*

**Habilita (successors):**
- Sprint planning — los OKRs guían qué entra en cada sprint
- `1.5.1` Project Schedule — los OKRs informan el timeline

**Criterio de completitud:**
- [ ] 3-5 Objectives definidos
- [ ] Cada Objective tiene 2-4 Key Results medibles
- [ ] Key Results son numéricos (no binarios ni vagos)
- [ ] Horizonte trimestral definido

**Anti-patrones:**
- ❌ **OKRs como task list:** Los KRs son resultados, no tareas. "Lanzar feature X" es tarea; "50% de usuarios usan feature X" es resultado.
- ❌ **KRs al 100%:** Si alcanzas todos los KRs, estaban demasiado fáciles. El ideal es 70%.

**Template:** Incluido dentro de `TEMPLATE_VISION_OBJECTIVES.md`

---

# 1.2 SCOPE

**Responsable:** Product Manager  
**Aprueba:** Product Owner  
**Objetivo de subfase:** Definir qué incluye y qué NO incluye el proyecto.

---

### 1.2.1 Scope Statement

| Campo | Valor |
|-------|-------|
| **Fase** | 01-Planning |
| **Subfase** | 1.2 Scope |
| **Responsable** | Product Manager |
| **Ejecuta** | Product Manager |
| **Aprueba** | Product Owner |
| **Formato** | Documento |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez + revisión por cambio de alcance |

**Perfil de ejecución:** El PM lo redacta directamente porque es una decisión de producto. Requiere integrar la visión del PO con la realidad técnica (input del TL) y los recursos disponibles (input del PgM). En VTT: un agente puede generar un draft basado en los goals y el target market, pero el PM debe validar contra capacidad real.

**Qué es:** Declaración formal de lo que el proyecto incluye y lo que excluye explícitamente. Es el contrato de alcance del equipo.

**Para qué sirve:** Previene scope creep — la tendencia natural a agregar "una cosita más." Si algo no está en el scope, no se construye sin aprobación formal de cambio.

**Inputs requeridos:**
- `1.1.3` Product Goals — el scope debe lograr los goals
- `0.1.5` Target Market — el scope es para este mercado
- `0.3.1` Problem Statement — el scope resuelve este problema
- Input del TL sobre viabilidad técnica
- Input del PgM sobre recursos disponibles

**Dependencias (predecessors):**
- `1.1.3` Product Goals *(obligatorio)*
- `0.3.1` Problem Statement *(obligatorio)*
- `0.1.5` Target Market *(obligatorio)*

**Habilita (successors):**
- `1.2.2` In-Scope — detalle de lo incluido
- `1.2.3` Out-of-Scope — detalle de lo excluido
- `1.2.4` MVP Definition — MVP es un subconjunto del scope
- `2.1.1` Functional Requirements — requirements dentro del scope

**Criterio de completitud:**
- [ ] Define explícitamente qué SÍ incluye
- [ ] Define explícitamente qué NO incluye
- [ ] Aprobado por PO, PM y TL
- [ ] Referencia los goals que justifican el alcance

**Anti-patrones:**
- ❌ **Scope sin out-of-scope:** Si no dices qué excluyes, todo puede entrar.
- ❌ **Scope vago:** "Construir una plataforma educativa" no es un scope statement.
- ❌ **Scope sin validación técnica:** El TL debe confirmar viabilidad.

**Template:** `_pm/templates/TEMPLATE_SCOPE.md` *(pendiente)*

---

### 1.2.2 In-Scope

| Campo | Valor |
|-------|-------|
| **Fase** | 01-Planning |
| **Subfase** | 1.2 Scope |
| **Responsable** | Product Manager |
| **Ejecuta** | Product Manager + Systems Analyst |
| **Aprueba** | Product Owner |
| **Formato** | Lista |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Una vez + cambio controlado |

**Perfil de ejecución:** PM define las funcionalidades incluidas, SA las refina con detalle técnico. En VTT: un agente puede derivar la lista de in-scope a partir de los goals y la feature comparison, pero PM y SA validan.

**Qué es:** Lista detallada de funcionalidades, módulos y capacidades que SÍ están incluidas en el proyecto.

**Para qué sirve:** Referencia explícita para el equipo. Si alguien pregunta "¿vamos a hacer X?", la respuesta está aquí.

**Inputs requeridos:**
- `1.2.1` Scope Statement
- `0.2.3` Feature Comparison — table-stakes que deben entrar
- `0.4.3` Key Differentiators — diferenciadores que deben entrar

**Dependencias (predecessors):**
- `1.2.1` Scope Statement *(obligatorio)*

**Habilita (successors):**
- `1.2.4` MVP Definition
- `2.1.1` Functional Requirements

**Criterio de completitud:**
- [ ] Cada ítem es específico y verificable
- [ ] Cubre table-stakes + al menos 1 diferenciador
- [ ] No contradice el out-of-scope

**Anti-patrones:**
- ❌ **Lista genérica:** "Sistema de login" — ¿con OAuth? ¿con MFA? ¿con passwordless?
- ❌ **Todo incluido:** Si el in-scope tiene 50 ítems, no estás priorizando.

**Template:** Incluido dentro de `TEMPLATE_SCOPE.md`

---

### 1.2.3 Out-of-Scope

| Campo | Valor |
|-------|-------|
| **Fase** | 01-Planning |
| **Subfase** | 1.2 Scope |
| **Responsable** | Product Manager |
| **Ejecuta** | Product Manager |
| **Aprueba** | Product Owner |
| **Formato** | Lista |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Una vez + cambio controlado |

**Perfil de ejecución:** El PM lo define — es una decisión de priorización. En VTT: un agente puede sugerir ítems out-of-scope basado en el future phases roadmap, pero la decisión de excluir es del PM con aprobación del PO.

**Qué es:** Lista explícita de lo que NO se construye en esta fase del proyecto, con justificación breve.

**Para qué sirve:** El documento más importante para prevenir scope creep. Cuando un stakeholder pide algo, si está en esta lista, la conversación es diferente: "Eso está planeado para fase 2, no para MVP."

**Inputs requeridos:**
- `1.2.1` Scope Statement
- `1.2.5` Future Phases — lo excluido hoy puede estar planeado para después

**Dependencias (predecessors):**
- `1.2.1` Scope Statement *(obligatorio)*

**Habilita (successors):**
- `1.2.5` Future Phases — algunos excluidos se convierten en roadmap
- Gestión de cambios — referencia cuando pidan cambios

**Criterio de completitud:**
- [ ] Lista las funcionalidades más "tentadoras" que se excluyeron
- [ ] Cada exclusión tiene justificación breve
- [ ] PO ha aprobado (entiende qué se sacrifica)

**Anti-patrones:**
- ❌ **Out-of-scope vacío:** Si no excluyes nada, no estás priorizando.
- ❌ **Solo lo obvio:** "No hacemos hardware" no ayuda. Excluir lo que alguien podría razonablemente pedir.

**Template:** Incluido dentro de `TEMPLATE_SCOPE.md`

---

### 1.2.4 MVP Definition

| Campo | Valor |
|-------|-------|
| **Fase** | 01-Planning |
| **Subfase** | 1.2 Scope |
| **Responsable** | Product Manager |
| **Ejecuta** | Product Manager + Tech Lead |
| **Aprueba** | Product Owner |
| **Formato** | Documento |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 2 días |
| **Frecuencia** | Una vez + revisión post-validación |

**Perfil de ejecución:** PM define qué entra en el MVP desde la perspectiva de producto (qué hipótesis valida), TL valida la viabilidad técnica y estima esfuerzo. En VTT: un agente puede proponer un MVP basado en el cruce de value hypothesis + feature comparison (table-stakes + 1 diferenciador), pero PM y TL deben validar contra capacidad real del equipo.

**Qué es:** Definición del Minimum Viable Product — el subconjunto más pequeño del scope que valida las hipótesis de valor más riesgosas. No es "versión incompleta" — es la versión más pequeña que genera aprendizaje.

**Para qué sirve:** Fuerza al equipo a construir lo mínimo necesario para aprender si las hipótesis son correctas. Sin MVP definido, se construye todo y se aprende nada.

**Inputs requeridos:**
- `0.4.5` Value Hypothesis — el MVP valida estas hipótesis
- `0.4.3` Key Differentiators — el MVP incluye al menos 1
- `0.2.3` Feature Comparison — table-stakes obligatorias
- `1.2.2` In-Scope — el MVP es subconjunto
- Estimación del TL sobre esfuerzo por feature

**Dependencias (predecessors):**
- `0.4.5` Value Hypothesis *(obligatorio)*
- `1.2.2` In-Scope *(obligatorio)*
- `0.4.3` Key Differentiators *(obligatorio)*

**Habilita (successors):**
- `2.1.1` Functional Requirements — requirements del MVP
- `2.4.1` Product Backlog — stories del MVP
- `1.5.1` Project Schedule — timeline del MVP
- `3B.1.1` System Architecture — arquitectura para el MVP

**Audiencia:**
- Todo el equipo — define qué se construye primero

**Secciones esperadas:**
1. Hipótesis que el MVP valida
2. Features incluidas (con justificación por feature)
3. Features excluidas del MVP (con "cuándo" entran)
4. Criterios de éxito del MVP (cómo sabremos si funcionó)
5. Estimación de esfuerzo (alto nivel)

**Criterio de completitud:**
- [ ] Cada feature incluida se justifica contra una hipótesis o table-stake
- [ ] Al menos 1 diferenciador incluido
- [ ] Criterios de éxito medibles
- [ ] TL confirma que es construible en el timeline
- [ ] PO aprueba lo que se sacrifica

**Anti-patrones:**
- ❌ **MVP = v1 completa:** Si el MVP toma 6 meses, no es mínimo.
- ❌ **MVP sin diferenciador:** Si solo tiene table-stakes, no aprendes si tu propuesta de valor funciona.
- ❌ **MVP sin criterio de éxito:** Construir sin saber qué medirás es un proyecto, no un experimento.

**Template:** `_pm/templates/TEMPLATE_MVP_DEFINITION.md` *(pendiente)*

---

### 1.2.5 Future Phases

| Campo | Valor |
|-------|-------|
| **Fase** | 01-Planning |
| **Subfase** | 1.2 Scope |
| **Responsable** | Product Manager |
| **Ejecuta** | Product Manager |
| **Aprueba** | Product Owner |
| **Formato** | Lista |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Revisión trimestral |

**Perfil de ejecución:** El PM lo define como roadmap de alto nivel. En VTT: un agente puede proponer agrupaciones de features del out-of-scope en fases, pero la secuencia y priorización es decisión del PM.

**Qué es:** Roadmap de alto nivel de lo que se construirá DESPUÉS del MVP, organizado en fases con prioridad relativa.

**Para qué sirve:** Da visibilidad a stakeholders de que lo excluido no se ignora — tiene un lugar en el plan. Reduce ansiedad sobre el out-of-scope.

**Inputs requeridos:**
- `1.2.3` Out-of-Scope — lo excluido se convierte en roadmap
- `1.1.1` Vision Statement — las fases avanzan hacia la visión

**Dependencias (predecessors):**
- `1.2.3` Out-of-Scope *(obligatorio)*

**Habilita (successors):**
- Comunicación con stakeholders
- Planificación de recursos a mediano plazo

**Criterio de completitud:**
- [ ] Cada ítem del out-of-scope tiene un "cuándo" tentativo
- [ ] Fases secuenciadas con lógica (no arbitrariamente)
- [ ] PO aprueba la secuencia

**Anti-patrones:**
- ❌ **Roadmap como promesa:** Es un plan tentativo, no un compromiso. Debe decirlo explícitamente.

**Template:** Incluido dentro de `TEMPLATE_SCOPE.md`

---

### 1.2.6 Assumptions

| Campo | Valor |
|-------|-------|
| **Fase** | 01-Planning |
| **Subfase** | 1.2 Scope |
| **Responsable** | Product Manager |
| **Ejecuta** | Product Manager + Systems Analyst |
| **Aprueba** | Product Owner |
| **Formato** | Lista |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Revisión por sprint |

**Perfil de ejecución:** PM y SA listan los supuestos del proyecto. Cada miembro del equipo puede contribuir. En VTT: un agente puede extraer supuestos implícitos de los documentos anteriores (si el scope asume ciertas integraciones, si el timeline asume cierto equipo, etc.).

**Qué es:** Lista de supuestos sobre los que se basa el plan — cosas que asumimos como ciertas pero que no hemos verificado completamente.

**Para qué sirve:** Hacer explícito lo implícito. Si un supuesto resulta falso, el plan cambia. Mejor saberlo antes que descubrirlo en desarrollo.

**Inputs requeridos:**
- Todos los documentos anteriores — cada uno tiene supuestos implícitos
- Input de TL, PgM, SA sobre supuestos técnicos y de recursos

**Dependencias (predecessors):**
- `1.2.1` Scope Statement *(obligatorio)*

**Habilita (successors):**
- `1.4.1` Risk Register — cada supuesto es un riesgo potencial si falla
- Gestión de cambios — cuando un supuesto falla, se activa cambio

**Criterio de completitud:**
- [ ] Supuestos de mercado, técnicos, de recursos y de timeline listados
- [ ] Cada uno tiene impacto si resulta falso
- [ ] Revisado por TL y PgM (no solo PM)

**Anti-patrones:**
- ❌ **Supuestos obvios:** "Asumimos que habrá internet" no agrega valor.
- ❌ **Sin impacto:** Listar el supuesto sin decir qué pasa si falla.

**Template:** Incluido dentro de `TEMPLATE_SCOPE.md`

---

# 1.3 STAKEHOLDERS

**Responsable:** Program Manager  
**Aprueba:** Product Owner  
**Objetivo de subfase:** Identificar y mapear stakeholders.

---

### 1.3.1 Stakeholder Map

| Campo | Valor |
|-------|-------|
| **Fase** | 01-Planning |
| **Subfase** | 1.3 Stakeholders |
| **Responsable** | Program Manager |
| **Ejecuta** | Program Manager |
| **Aprueba** | Product Owner |
| **Formato** | Diagrama |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Una vez + por cambio organizacional |

**Perfil de ejecución:** El PgM lo produce directamente — requiere conocimiento organizacional. En VTT: un agente puede generar el template del mapa, pero el PgM lo llena con conocimiento real de la organización.

**Qué es:** Diagrama que visualiza a todos los stakeholders del proyecto posicionados por nivel de influencia y nivel de interés (matriz poder/interés).

**Para qué sirve:** Define a quién informar, a quién consultar y a quién mantener satisfecho. Evita sorpresas políticas.

**Inputs requeridos:**
- Conocimiento organizacional del PgM
- Input del PO sobre stakeholders de negocio

**Dependencias (predecessors):**
- Ninguna directa — depende de contexto organizacional

**Habilita (successors):**
- `1.3.2` Stakeholder Register — detalle de cada stakeholder
- `1.3.3` RACI Matrix — responsabilidades formales
- `1.3.4` Communication Plan — estrategia por stakeholder

**Criterio de completitud:**
- [ ] Todos los stakeholders relevantes incluidos
- [ ] Posicionados en matriz poder/interés
- [ ] Estrategia por cuadrante definida (gestionar, informar, satisfacer, monitorear)

**Anti-patrones:**
- ❌ **Solo los cercanos:** Incluir stakeholders de IT, legal, finanzas, no solo producto.
- ❌ **Sin estrategia:** El mapa sin la estrategia por cuadrante es un organigrama.

**Template:** `_pm/templates/TEMPLATE_STAKEHOLDERS.md` *(pendiente)*

---

### 1.3.2 Stakeholder Register

| Campo | Valor |
|-------|-------|
| **Fase** | 01-Planning |
| **Subfase** | 1.3 Stakeholders |
| **Responsable** | Program Manager |
| **Ejecuta** | Program Manager |
| **Aprueba** | Product Owner |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Actualización por cambio |

**Perfil de ejecución:** PgM lo produce y mantiene. En VTT: un agente puede generar el template de la tabla, PgM lo llena.

**Qué es:** Tabla con cada stakeholder: nombre, rol, intereses, nivel de influencia, expectativas y estrategia de gestión.

**Para qué sirve:** Referencia operativa del PgM para gestionar las relaciones del proyecto.

**Inputs requeridos:**
- `1.3.1` Stakeholder Map

**Dependencias (predecessors):**
- `1.3.1` Stakeholder Map *(obligatorio)*

**Habilita (successors):**
- `1.3.3` RACI Matrix
- `1.3.4` Communication Plan

**Criterio de completitud:**
- [ ] Cada stakeholder del mapa tiene entrada en el registro
- [ ] Expectativas documentadas por stakeholder
- [ ] Estrategia de gestión definida

**Template:** Incluido dentro de `TEMPLATE_STAKEHOLDERS.md`

---

### 1.3.3 RACI Matrix

| Campo | Valor |
|-------|-------|
| **Fase** | 01-Planning |
| **Subfase** | 1.3 Stakeholders |
| **Responsable** | Program Manager |
| **Ejecuta** | Program Manager + Product Manager |
| **Aprueba** | Product Owner |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez + por cambio de equipo |

**Perfil de ejecución:** PgM define la estructura, PM contribuye con las responsabilidades de producto. En VTT: un agente puede generar la matriz a partir de los roles definidos en `_pm/roles/` y las fases del SDLC — esto es altamente automatizable porque es cruce de roles × actividades.

**Qué es:** Matriz Responsible-Accountable-Consulted-Informed por actividad principal del proyecto.

**Para qué sirve:** Elimina ambigüedad sobre quién hace qué. Cuando hay conflicto de responsabilidad, la RACI resuelve.

**Inputs requeridos:**
- `1.3.2` Stakeholder Register — lista de personas/roles
- `1.2.2` In-Scope — actividades principales
- Perfiles de agentes VTT (`_pm/roles/`) si aplica

**Dependencias (predecessors):**
- `1.3.2` Stakeholder Register *(obligatorio)*

**Habilita (successors):**
- `1.3.4` Communication Plan
- Handoffs entre agentes en VTT

**Criterio de completitud:**
- [ ] Cada actividad principal tiene exactamente 1 Accountable
- [ ] Cada actividad tiene al menos 1 Responsible
- [ ] No hay actividades sin asignar
- [ ] Validada por todos los stakeholders listados

**Anti-patrones:**
- ❌ **Dos Accountables:** Si dos personas son accountable, nadie lo es.
- ❌ **Todos Consulted:** Si consultas a todos en todo, nada avanza.

**Template:** Incluido dentro de `TEMPLATE_STAKEHOLDERS.md`

---

### 1.3.4 Communication Plan

| Campo | Valor |
|-------|-------|
| **Fase** | 01-Planning |
| **Subfase** | 1.3 Stakeholders |
| **Responsable** | Program Manager |
| **Ejecuta** | Program Manager |
| **Aprueba** | Product Owner |
| **Formato** | Documento |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Una vez + ajuste por feedback |

**Perfil de ejecución:** PgM lo define basado en el stakeholder map y la RACI. En VTT: un agente puede proponer un plan estándar (daily standup, weekly report, sprint review, etc.) que el PgM ajusta al contexto.

**Qué es:** Plan que define qué se comunica, a quién, con qué frecuencia, por qué canal y quién lo envía.

**Para qué sirve:** Evita dos problemas: stakeholders que no saben lo que pasa (sub-comunicación) y stakeholders abrumados con información irrelevante (sobre-comunicación).

**Inputs requeridos:**
- `1.3.1` Stakeholder Map — quién necesita qué nivel de información
- `1.3.3` RACI Matrix — quién informa a quién
- `0.4.4` Target Customer Profile — cómo se comunica con el perfil del cliente

**Dependencias (predecessors):**
- `1.3.1` Stakeholder Map *(obligatorio)*
- `1.3.3` RACI Matrix *(obligatorio)*

**Habilita (successors):**
- Ejecución del proyecto — el plan se usa activamente
- `7.2.1` Support Process — base para comunicación con usuarios

**Criterio de completitud:**
- [ ] Cada stakeholder tiene canal y frecuencia definida
- [ ] Incluye comunicación regular y de emergencia
- [ ] Canales son realistas (no 5 reuniones diarias)

**Anti-patrones:**
- ❌ **Plan que nadie sigue:** Si el plan es demasiado elaborado, se ignora.
- ❌ **Solo comunicación interna:** Incluir comunicación con usuarios/clientes si aplica.

**Template:** Incluido dentro de `TEMPLATE_STAKEHOLDERS.md`

---

# 1.4 RISKS

**Responsable:** Program Manager  
**Aprueba:** Product Owner  
**Objetivo de subfase:** Identificar y planear mitigación de riesgos.

---

### 1.4.1 Risk Register

| Campo | Valor |
|-------|-------|
| **Fase** | 01-Planning |
| **Subfase** | 1.4 Risks |
| **Responsable** | Program Manager |
| **Ejecuta** | Program Manager + Tech Lead + Systems Analyst |
| **Aprueba** | Product Owner |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Revisión quincenal |

**Perfil de ejecución:** PgM lidera, TL aporta riesgos técnicos, SA aporta riesgos de requisitos. En VTT: un agente puede generar una lista de riesgos comunes para el tipo de proyecto (tech stack, integraciones, equipo) y el equipo los valida y prioriza.

**Qué es:** Tabla con todos los riesgos identificados, su probabilidad, impacto, responsable de monitoreo y estado.

**Para qué sirve:** No elimina riesgos — los hace visibles. Un riesgo conocido se gestiona; uno desconocido te golpea.

**Inputs requeridos:**
- `1.2.6` Assumptions — cada supuesto es un riesgo potencial
- `1.2.1` Scope Statement — riesgos de alcance
- Input del TL sobre riesgos técnicos
- Input del SA sobre riesgos de requisitos
- `1.5.1` Project Schedule — riesgos de timeline

**Dependencias (predecessors):**
- `1.2.6` Assumptions *(obligatorio)*
- `1.2.1` Scope Statement *(obligatorio)*

**Habilita (successors):**
- `1.4.2` Risk Assessment — evaluación formal
- `1.4.3` Mitigation Plan
- `1.4.4` Contingency Plan

**Secciones esperadas:**

| ID | Riesgo | Probabilidad | Impacto | Score | Owner | Estado | Mitigación |
|----|--------|-------------|---------|-------|-------|--------|-----------|

**Criterio de completitud:**
- [ ] Riesgos técnicos, de negocio, de equipo y de timeline incluidos
- [ ] Cada riesgo tiene probabilidad × impacto
- [ ] Cada riesgo tiene owner
- [ ] Se revisa quincenalmente

**Anti-patrones:**
- ❌ **Solo riesgos técnicos:** Los riesgos de personas, mercado y organización son igual de letales.
- ❌ **Register estático:** Si se llena una vez y se olvida, no sirve.

**Template:** `_pm/templates/TEMPLATE_RISK_MANAGEMENT.md` *(pendiente)*

---

### 1.4.2 Risk Assessment

| Campo | Valor |
|-------|-------|
| **Fase** | 01-Planning |
| **Subfase** | 1.4 Risks |
| **Responsable** | Program Manager |
| **Ejecuta** | Program Manager |
| **Aprueba** | Product Owner |
| **Formato** | Matriz |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Quincenal con el register |

**Perfil de ejecución:** PgM evalúa y visualiza los riesgos en una matriz de probabilidad/impacto. En VTT: automatizable — un agente puede generar la matriz a partir del risk register.

**Qué es:** Evaluación formal de cada riesgo en una matriz de probabilidad × impacto (heat map).

**Para qué sirve:** Prioriza visualmente qué riesgos necesitan atención inmediata vs cuáles monitorear.

**Inputs requeridos:**
- `1.4.1` Risk Register

**Dependencias (predecessors):**
- `1.4.1` Risk Register *(obligatorio)*

**Habilita (successors):**
- `1.4.3` Mitigation Plan — para los riesgos altos
- `1.4.4` Contingency Plan — para los riesgos críticos

**Criterio de completitud:**
- [ ] Todos los riesgos del register evaluados
- [ ] Riesgos altos (rojo) tienen acción inmediata
- [ ] Visualización tipo heat map disponible

**Template:** Incluido dentro de `TEMPLATE_RISK_MANAGEMENT.md`

---

### 1.4.3 Mitigation Plan

| Campo | Valor |
|-------|-------|
| **Fase** | 01-Planning |
| **Subfase** | 1.4 Risks |
| **Responsable** | Program Manager |
| **Ejecuta** | Risk Owners (según register) |
| **Aprueba** | Product Owner |
| **Formato** | Documento |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Actualización por cambio de riesgo |

**Perfil de ejecución:** Cada risk owner define su plan de mitigación, PgM consolida. En VTT: un agente puede proponer estrategias de mitigación estándar por tipo de riesgo (técnico→PrototypeFirst, equipo→CrossTraining, etc.), pero los owners validan.

**Qué es:** Plan de acciones proactivas para REDUCIR la probabilidad o impacto de cada riesgo alto/crítico.

**Para qué sirve:** Diferente del contingency — la mitigación actúa ANTES de que el riesgo se materialice.

**Inputs requeridos:**
- `1.4.2` Risk Assessment — riesgos altos/críticos

**Dependencias (predecessors):**
- `1.4.2` Risk Assessment *(obligatorio)*

**Habilita (successors):**
- Ejecución de acciones de mitigación
- `1.4.5` Risk Monitoring

**Criterio de completitud:**
- [ ] Cada riesgo alto/crítico tiene plan de mitigación
- [ ] Cada acción tiene responsable y deadline
- [ ] Costo de mitigación vs costo del riesgo evaluado

**Template:** Incluido dentro de `TEMPLATE_RISK_MANAGEMENT.md`

---

### 1.4.4 Contingency Plan

| Campo | Valor |
|-------|-------|
| **Fase** | 01-Planning |
| **Subfase** | 1.4 Risks |
| **Responsable** | Program Manager |
| **Ejecuta** | Program Manager + Tech Lead |
| **Aprueba** | Product Owner |
| **Formato** | Documento |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Actualización por cambio |

**Perfil de ejecución:** PgM y TL definen qué hacer SI el riesgo se materializa. En VTT: un agente puede proponer planes de contingencia estándar (rollback, feature flag, scale down scope), pero los planes específicos requieren juicio del PgM y TL.

**Qué es:** Plan de acciones reactivas para cuando un riesgo SE MATERIALIZA. El "Plan B."

**Para qué sirve:** Cuando algo sale mal, el equipo no improvisa — sigue un plan ya pensado en frío.

**Inputs requeridos:**
- `1.4.1` Risk Register
- `1.4.2` Risk Assessment — riesgos críticos

**Dependencias (predecessors):**
- `1.4.2` Risk Assessment *(obligatorio)*

**Habilita (successors):**
- `6.7.1` Rollback Plan — contingencia específica de deploy

**Criterio de completitud:**
- [ ] Riesgos críticos tienen plan de contingencia
- [ ] Cada plan tiene trigger (qué indica que el riesgo se materializó)
- [ ] Cada plan tiene acciones concretas y responsable

**Anti-patrones:**
- ❌ **Contingencia = "re-evaluar":** No es plan. Plan es: "Si X falla, hacemos Y en Z tiempo."
- ❌ **Sin trigger:** Si no defines cuándo activar el plan, nadie lo activa.

**Template:** Incluido dentro de `TEMPLATE_RISK_MANAGEMENT.md`

---

### 1.4.5 Risk Monitoring

| Campo | Valor |
|-------|-------|
| **Fase** | 01-Planning |
| **Subfase** | 1.4 Risks |
| **Responsable** | Program Manager |
| **Ejecuta** | Program Manager |
| **Aprueba** | Product Owner |
| **Formato** | Documento |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días (setup) |
| **Frecuencia** | Continua |

**Perfil de ejecución:** PgM define el proceso de monitoreo. En VTT: automatizable — un agente puede generar reportes periódicos de estado de riesgos a partir del register.

**Qué es:** Definición del proceso de monitoreo continuo de riesgos: frecuencia de revisión, indicadores early-warning, y proceso de escalamiento.

**Para qué sirve:** Sin monitoreo, el risk register se llena una vez y se olvida. El monitoreo lo mantiene vivo.

**Inputs requeridos:**
- `1.4.1` Risk Register
- `1.3.4` Communication Plan — integrar reporting de riesgos

**Dependencias (predecessors):**
- `1.4.1` Risk Register *(obligatorio)*

**Criterio de completitud:**
- [ ] Frecuencia de revisión definida
- [ ] Early-warning indicators para riesgos críticos
- [ ] Proceso de escalamiento definido
- [ ] Integrado en la rutina del equipo (no un proceso extra)

**Template:** Incluido dentro de `TEMPLATE_RISK_MANAGEMENT.md`

---

# 1.5 TIMELINE

**Responsable:** Program Manager  
**Aprueba:** Product Owner  
**Objetivo de subfase:** Definir cronograma del proyecto.

---

### 1.5.1 Project Schedule

| Campo | Valor |
|-------|-------|
| **Fase** | 01-Planning |
| **Subfase** | 1.5 Timeline |
| **Responsable** | Program Manager |
| **Ejecuta** | Program Manager + Tech Lead |
| **Aprueba** | Product Owner |
| **Formato** | Gantt |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 2 días |
| **Frecuencia** | Actualización semanal |

**Perfil de ejecución:** PgM estructura el cronograma, TL estima las duraciones técnicas. En VTT: un agente puede generar un timeline template basado en las fases del SDLC y el sprint calendar, pero las estimaciones de duración requieren input del TL.

**Qué es:** Cronograma completo del proyecto con fechas de inicio/fin por actividad, dependencias y recursos asignados.

**Para qué sirve:** Hace visible cuándo se entrega cada cosa y qué depende de qué. Permite detectar bottlenecks y conflictos de recursos.

**Inputs requeridos:**
- `1.2.4` MVP Definition — qué se construye
- `1.1.6` OKRs — timeline alineado a OKRs
- Estimaciones del TL por feature/módulo
- Disponibilidad de recursos del PgM

**Dependencias (predecessors):**
- `1.2.4` MVP Definition *(obligatorio)*
- `1.1.6` OKRs *(obligatorio)*

**Habilita (successors):**
- `1.5.2` Milestones
- `1.5.4` Sprint Calendar
- `1.5.5` Dependencies
- `1.5.6` Critical Path
- Todo el equipo usa el schedule para planear

**Criterio de completitud:**
- [ ] Todas las actividades del MVP incluidas
- [ ] Dependencias mapeadas
- [ ] Recursos asignados
- [ ] Buffer time incluido (ver 1.5.7)

**Anti-patrones:**
- ❌ **Schedule sin buffer:** Si no hay holgura, el primer delay rompe todo.
- ❌ **Schedule sin dependencias:** Sin dependencias, no puedes calcular ruta crítica.
- ❌ **Estimaciones del PM sin TL:** El PM no estima trabajo técnico.

**Template:** `_pm/templates/TEMPLATE_TIMELINE.md` *(pendiente)*

---

### 1.5.2 Milestones

| Campo | Valor |
|-------|-------|
| **Fase** | 01-Planning |
| **Subfase** | 1.5 Timeline |
| **Responsable** | Program Manager |
| **Ejecuta** | Program Manager |
| **Aprueba** | Product Owner |
| **Formato** | Lista |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Con el schedule |

**Perfil de ejecución:** PgM los define. En VTT: un agente puede extraer milestones lógicos del schedule (fin de cada fase, entregables clave, gates de aprobación).

**Qué es:** Lista de hitos principales del proyecto — puntos de verificación donde algo significativo se completa o se decide.

**Para qué sirve:** Puntos de control para reportar progreso. Cada milestone es un checkpoint de go/no-go.

**Inputs requeridos:**
- `1.5.1` Project Schedule

**Dependencias (predecessors):**
- `1.5.1` Project Schedule *(obligatorio)*

**Criterio de completitud:**
- [ ] 5-10 milestones para un proyecto típico
- [ ] Cada uno tiene fecha y criterio de completitud
- [ ] Incluye milestones de negocio (no solo técnicos)

**Template:** Incluido dentro de `TEMPLATE_TIMELINE.md`

---

### 1.5.3 Phase Breakdown

| Campo | Valor |
|-------|-------|
| **Fase** | 01-Planning |
| **Subfase** | 1.5 Timeline |
| **Responsable** | Program Manager |
| **Ejecuta** | Program Manager |
| **Aprueba** | Product Owner |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Con el schedule |

**Perfil de ejecución:** PgM lo produce. En VTT: altamente automatizable — un agente puede generar el breakdown a partir de la estructura de fases VTT (ESTRUCTURA_FASES_V3.1) y el schedule.

**Qué es:** Tabla que muestra la duración, fechas y recursos de cada fase del proyecto.

**Para qué sirve:** Vista de alto nivel del timeline — cada fase con su duración y recursos asignados.

**Inputs requeridos:**
- `1.5.1` Project Schedule

**Dependencias (predecessors):**
- `1.5.1` Project Schedule *(obligatorio)*

**Criterio de completitud:**
- [ ] Cada fase del SDLC incluida con duración
- [ ] Solapamiento entre fases documentado si existe

**Template:** Incluido dentro de `TEMPLATE_TIMELINE.md`

---

### 1.5.4 Sprint Calendar

| Campo | Valor |
|-------|-------|
| **Fase** | 01-Planning |
| **Subfase** | 1.5 Timeline |
| **Responsable** | Program Manager |
| **Ejecuta** | Program Manager |
| **Aprueba** | Product Owner |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Una vez + ajuste por sprint |

**Perfil de ejecución:** PgM lo define. En VTT: un agente genera el calendario automáticamente dado fecha de inicio, duración de sprint y número de sprints.

**Qué es:** Calendario con las fechas de inicio/fin de cada sprint, incluyendo ceremonias (planning, review, retro).

**Para qué sirve:** Referencia operativa para todo el equipo. Saben cuándo empieza y termina cada sprint.

**Inputs requeridos:**
- `1.5.1` Project Schedule
- Decisión de duración de sprint (1-4 semanas)

**Dependencias (predecessors):**
- `1.5.1` Project Schedule *(obligatorio)*

**Habilita (successors):**
- `2.4.6` Sprint Assignment — stories asignadas a sprints del calendario

**Criterio de completitud:**
- [ ] Todos los sprints del MVP con fechas
- [ ] Ceremonias incluidas (planning, review, retro)
- [ ] Feriados y vacaciones consideradas

**Template:** Incluido dentro de `TEMPLATE_TIMELINE.md`

---

### 1.5.5 Dependencies

| Campo | Valor |
|-------|-------|
| **Fase** | 01-Planning |
| **Subfase** | 1.5 Timeline |
| **Responsable** | Program Manager |
| **Ejecuta** | Program Manager + Tech Lead |
| **Aprueba** | Product Owner |
| **Formato** | Diagrama |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Con el schedule |

**Perfil de ejecución:** PgM mapea dependencias de proceso, TL mapea dependencias técnicas. En VTT: un agente puede generar un grafo de dependencias a partir del backlog y las relaciones entre features.

**Qué es:** Diagrama de dependencias entre tareas/features — qué debe completarse antes de qué.

**Para qué sirve:** Identifica dónde un delay en una tarea impacta en cascada a otras. Sin esto, los delays sorprenden.

**Inputs requeridos:**
- `1.5.1` Project Schedule
- `1.2.4` MVP Definition — dependencias entre features
- Input del TL sobre dependencias técnicas

**Dependencias (predecessors):**
- `1.5.1` Project Schedule *(obligatorio)*

**Habilita (successors):**
- `1.5.6` Critical Path — se calcula a partir de las dependencias

**Criterio de completitud:**
- [ ] Todas las dependencias técnicas y de proceso mapeadas
- [ ] Dependencias externas identificadas (APIs, servicios de terceros)
- [ ] Visualización clara (no solo texto)

**Template:** Incluido dentro de `TEMPLATE_TIMELINE.md`

---

### 1.5.6 Critical Path

| Campo | Valor |
|-------|-------|
| **Fase** | 01-Planning |
| **Subfase** | 1.5 Timeline |
| **Responsable** | Program Manager |
| **Ejecuta** | Program Manager |
| **Aprueba** | Product Owner |
| **Formato** | Diagrama |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Con el schedule |

**Perfil de ejecución:** PgM lo calcula a partir de las dependencias. En VTT: automatizable — un agente puede calcular la ruta crítica dado el grafo de dependencias y las duraciones.

**Qué es:** La secuencia más larga de tareas dependientes — cualquier delay en esta cadena retrasa el proyecto entero.

**Para qué sirve:** Identifica dónde poner la mayor atención. Las tareas en el critical path no tienen margen.

**Inputs requeridos:**
- `1.5.5` Dependencies
- `1.5.1` Project Schedule

**Dependencias (predecessors):**
- `1.5.5` Dependencies *(obligatorio)*

**Habilita (successors):**
- `1.5.7` Buffer Time — buffer en el critical path
- Gestión diaria — priorizar tareas del critical path

**Criterio de completitud:**
- [ ] Ruta crítica identificada y visualizada
- [ ] Tareas del critical path marcadas en el schedule
- [ ] Equipo sabe cuáles son las tareas críticas

**Template:** Incluido dentro de `TEMPLATE_TIMELINE.md`

---

### 1.5.7 Buffer Time

| Campo | Valor |
|-------|-------|
| **Fase** | 01-Planning |
| **Subfase** | 1.5 Timeline |
| **Responsable** | Program Manager |
| **Ejecuta** | Program Manager |
| **Aprueba** | Product Owner |
| **Formato** | Documento |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Con el schedule |

**Perfil de ejecución:** PgM define la estrategia de buffer. En VTT: un agente puede aplicar reglas estándar (15-20% de buffer sobre estimación total, buffer concentrado al final del critical path).

**Qué es:** Definición del tiempo de holgura incluido en el schedule — cuánto, dónde, y bajo qué condiciones se consume.

**Para qué sirve:** Los proyectos sin buffer fallan el 100% de las veces. El buffer absorbe imprevistos sin cambiar el deadline.

**Inputs requeridos:**
- `1.5.1` Project Schedule
- `1.5.6` Critical Path
- `1.4.1` Risk Register — riesgos que podrían consumir buffer

**Dependencias (predecessors):**
- `1.5.6` Critical Path *(obligatorio)*

**Criterio de completitud:**
- [ ] Buffer calculado (15-20% del total o por método PERT)
- [ ] Ubicación del buffer definida (al final, distribuido, en critical path)
- [ ] Reglas de consumo definidas (quién autoriza usar buffer)

**Anti-patrones:**
- ❌ **Buffer oculto:** Inflar estimaciones individuales en vez de buffer explícito. Pierde visibilidad.
- ❌ **Buffer al inicio:** El buffer se consume al final, no al principio.

**Template:** Incluido dentro de `TEMPLATE_TIMELINE.md`

---

# 1.6 BUDGET

**Responsable:** Program Manager  
**Aprueba:** Product Owner  
**Objetivo de subfase:** Definir presupuesto y ROI.

---

### 1.6.1 Budget Estimate

| Campo | Valor |
|-------|-------|
| **Fase** | 01-Planning |
| **Subfase** | 1.6 Budget |
| **Responsable** | Program Manager |
| **Ejecuta** | Program Manager + Tech Lead |
| **Aprueba** | Product Owner |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Una vez + revisión mensual |

**Perfil de ejecución:** PgM estructura el presupuesto, TL estima costos técnicos (infra, licencias, herramientas). En VTT: un agente puede generar un template de budget con categorías estándar (personal, infra, licencias, servicios, contingencia), pero las cifras las ponen PgM y TL.

**Qué es:** Estimación del presupuesto total del proyecto desglosado por categoría.

**Para qué sirve:** Define cuánto cuesta el proyecto y permite al PO decidir si la inversión se justifica contra el SOM.

**Inputs requeridos:**
- `1.5.1` Project Schedule — duración × costo de equipo
- `1.6.3` Resource Plan — costos de personal
- `0.1.2` TAM/SAM/SOM — para justificar la inversión
- Costos de infraestructura (cloud, licencias, herramientas)

**Dependencias (predecessors):**
- `1.5.1` Project Schedule *(obligatorio)*
- `1.6.3` Resource Plan *(obligatorio)*

**Habilita (successors):**
- `1.6.2` Cost Breakdown
- `1.6.4` ROI Analysis
- `1.6.5` Budget Tracking

**Criterio de completitud:**
- [ ] Costos de personal, infraestructura, licencias y contingencia incluidos
- [ ] Contingencia del 10-15% incluida
- [ ] PO aprueba el total

**Anti-patrones:**
- ❌ **Sin contingencia:** Si el budget es exacto, el primer imprevisto lo rompe.
- ❌ **Solo costos directos:** Incluir overhead (oficina, herramientas, capacitación).

**Template:** `_pm/templates/TEMPLATE_BUDGET.md` *(pendiente)*

---

### 1.6.2 Cost Breakdown

| Campo | Valor |
|-------|-------|
| **Fase** | 01-Planning |
| **Subfase** | 1.6 Budget |
| **Responsable** | Program Manager |
| **Ejecuta** | Program Manager |
| **Aprueba** | Product Owner |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Con el budget |

**Perfil de ejecución:** PgM desglosa el budget. En VTT: automatizable — un agente puede desglosar el budget estimate en categorías y subcategorías.

**Qué es:** Desglose detallado de costos por categoría, subcategoría y periodo.

**Para qué sirve:** Transparencia sobre dónde va cada peso. Permite optimizar donde el costo es alto relativo al valor.

**Inputs requeridos:**
- `1.6.1` Budget Estimate

**Dependencias (predecessors):**
- `1.6.1` Budget Estimate *(obligatorio)*

**Criterio de completitud:**
- [ ] Cada línea del budget tiene desglose
- [ ] Costos por mes/sprint si aplica

**Template:** Incluido dentro de `TEMPLATE_BUDGET.md`

---

### 1.6.3 Resource Plan

| Campo | Valor |
|-------|-------|
| **Fase** | 01-Planning |
| **Subfase** | 1.6 Budget |
| **Responsable** | Program Manager |
| **Ejecuta** | Program Manager |
| **Aprueba** | Product Owner |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Revisión mensual |

**Perfil de ejecución:** PgM lo define. En VTT: un agente puede proponer un resource plan basado en los roles definidos en `_pm/roles/` y el sprint calendar.

**Qué es:** Plan de recursos humanos: quién, cuándo, cuántas horas, en qué fase, con qué costo.

**Para qué sirve:** Asegura que hay personas disponibles cuando se necesitan. Identifica conflictos de asignación.

**Inputs requeridos:**
- `1.5.1` Project Schedule
- `1.3.3` RACI Matrix — quién hace qué
- Disponibilidad real del equipo

**Dependencias (predecessors):**
- `1.5.1` Project Schedule *(obligatorio)*
- `1.3.3` RACI Matrix *(obligatorio)*

**Habilita (successors):**
- `1.6.1` Budget Estimate — costos de personal

**Criterio de completitud:**
- [ ] Cada fase tiene recursos asignados
- [ ] No hay personas asignadas al 100% en múltiples tareas simultáneas
- [ ] Vacaciones y disponibilidad parcial consideradas

**Anti-patrones:**
- ❌ **Personas al 100%:** Nadie produce al 100%. 70-80% es realista.
- ❌ **Sin considerar ramp-up:** Nuevos miembros del equipo no producen al 100% desde el día 1.

**Template:** Incluido dentro de `TEMPLATE_BUDGET.md`

---

### 1.6.4 ROI Analysis

| Campo | Valor |
|-------|-------|
| **Fase** | 01-Planning |
| **Subfase** | 1.6 Budget |
| **Responsable** | Program Manager |
| **Ejecuta** | Program Manager + Product Manager |
| **Aprueba** | Product Owner |
| **Formato** | Documento |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez + revisión trimestral |

**Perfil de ejecución:** PgM calcula costos, PM proyecta revenue basado en el SOM y el pricing. En VTT: un agente puede generar un modelo de ROI básico dado los inputs de costo y revenue proyectado.

**Qué es:** Análisis de retorno de inversión — cuánto cuesta el proyecto vs cuánto generará en un horizonte definido.

**Para qué sirve:** Justifica la inversión con números. Si el ROI es negativo en un horizonte razonable, el proyecto se cuestiona.

**Inputs requeridos:**
- `1.6.1` Budget Estimate — costo total
- `0.1.2` TAM/SAM/SOM — revenue potencial
- `0.2.4` Pricing Comparison — modelo de pricing
- Proyecciones de adopción

**Dependencias (predecessors):**
- `1.6.1` Budget Estimate *(obligatorio)*
- `0.1.2` TAM/SAM/SOM *(obligatorio)*

**Habilita (successors):**
- Decisión de inversión del PO/Board
- `1.6.5` Budget Tracking — tracking contra lo proyectado

**Criterio de completitud:**
- [ ] Costo total del proyecto documentado
- [ ] Revenue proyectado con supuestos explícitos
- [ ] Break-even point identificado
- [ ] Escenarios optimista, realista y pesimista

**Anti-patrones:**
- ❌ **Solo escenario optimista:** Siempre incluir pesimista.
- ❌ **Revenue sin supuestos:** Las proyecciones de revenue deben explicar sus supuestos.

**Template:** Incluido dentro de `TEMPLATE_BUDGET.md`

---

### 1.6.5 Budget Tracking

| Campo | Valor |
|-------|-------|
| **Fase** | 01-Planning |
| **Subfase** | 1.6 Budget |
| **Responsable** | Program Manager |
| **Ejecuta** | Program Manager |
| **Aprueba** | Product Owner |
| **Formato** | Documento |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días (setup) |
| **Frecuencia** | Continua (mensual) |

**Perfil de ejecución:** PgM define el proceso de tracking. En VTT: un agente puede generar reportes mensuales de budget vs actual si tiene acceso a datos de gastos.

**Qué es:** Definición del proceso de seguimiento de presupuesto: frecuencia de revisión, formato de reporte, umbrales de alerta.

**Para qué sirve:** Sin tracking, el budget se gasta sin visibilidad. Cuando te das cuenta que te pasaste, ya es tarde.

**Inputs requeridos:**
- `1.6.1` Budget Estimate — baseline
- `1.6.2` Cost Breakdown — categorías a trackear

**Dependencias (predecessors):**
- `1.6.1` Budget Estimate *(obligatorio)*

**Criterio de completitud:**
- [ ] Proceso de tracking definido (herramienta, frecuencia, responsable)
- [ ] Umbrales de alerta (ej: alerta si gasto >80% del budget en <80% del timeline)
- [ ] Formato de reporte definido

**Anti-patrones:**
- ❌ **Tracking solo al final:** Revisar el budget al final del proyecto no es tracking, es autopsia.

**Template:** Incluido dentro de `TEMPLATE_BUDGET.md`

---

# ÍNDICE DE DEPENDENCIAS — FASE 1

```
1.1.1 Vision Statement
  └─► 1.1.2, 1.1.3, 1.2.1

1.1.2 Mission Statement
  └─► 1.1.3, 1.2.1

1.1.3 Product Goals
  └─► 1.1.4, 1.1.6, 1.2.1

1.1.4 Success Metrics
  └─► 1.1.5, 1.1.6, 6.6.1

1.1.5 North Star Metric
  └─► Priorización de backlog, 6.6.1

1.1.6 OKRs
  └─► Sprint planning, 1.5.1

1.2.1 Scope Statement
  └─► 1.2.2, 1.2.3, 1.2.4, 1.2.6, 2.1.1

1.2.2 In-Scope
  └─► 1.2.4, 2.1.1

1.2.3 Out-of-Scope
  └─► 1.2.5

1.2.4 MVP Definition
  └─► 2.1.1, 2.4.1, 1.5.1, 3B.1.1

1.2.5 Future Phases
  └─► Comunicación con stakeholders

1.2.6 Assumptions
  └─► 1.4.1

1.3.1 Stakeholder Map
  └─► 1.3.2, 1.3.3, 1.3.4

1.3.2 Stakeholder Register
  └─► 1.3.3, 1.3.4

1.3.3 RACI Matrix
  └─► 1.3.4, Handoffs VTT

1.3.4 Communication Plan
  └─► Ejecución del proyecto, 7.2.1

1.4.1 Risk Register
  └─► 1.4.2, 1.4.3, 1.4.4, 1.4.5

1.4.2 Risk Assessment
  └─► 1.4.3, 1.4.4

1.4.3 Mitigation Plan
  └─► Ejecución de mitigaciones

1.4.4 Contingency Plan
  └─► 6.7.1

1.4.5 Risk Monitoring
  └─► Proceso continuo

1.5.1 Project Schedule
  └─► 1.5.2, 1.5.3, 1.5.4, 1.5.5, 1.6.1

1.5.2 Milestones
  └─► Reporting de progreso

1.5.3 Phase Breakdown
  └─► Vista de alto nivel

1.5.4 Sprint Calendar
  └─► 2.4.6

1.5.5 Dependencies
  └─► 1.5.6

1.5.6 Critical Path
  └─► 1.5.7

1.5.7 Buffer Time
  └─► Schedule final

1.6.1 Budget Estimate
  └─► 1.6.2, 1.6.4, 1.6.5

1.6.2 Cost Breakdown
  └─► Tracking operativo

1.6.3 Resource Plan
  └─► 1.6.1

1.6.4 ROI Analysis
  └─► Decisión de inversión

1.6.5 Budget Tracking
  └─► Proceso continuo
```

---

# RESUMEN DE EJECUTORES — FASE 1

| Deliverable | Responsable | Ejecuta | Delegable a agente VTT |
|-------------|-------------|---------|------------------------|
| 1.1.1 Vision Statement | PO | PO | 🔶 Parcial — opciones sí, versión final no |
| 1.1.2 Mission Statement | PO | PO | 🔶 Parcial — opciones sí, versión final no |
| 1.1.3 Product Goals | PO | PM | ✅ Sí — draft de goals SMART |
| 1.1.4 Success Metrics | PO | PM | ✅ Sí — KPIs estándar de industria |
| 1.1.5 North Star Metric | PO | PO | ❌ No — decisión estratégica |
| 1.1.6 OKRs | PO | PM + PgM | ✅ Sí — estructuración de goals en OKRs |
| 1.2.1 Scope Statement | PM | PM | 🔶 Parcial — draft sí, validación técnica no |
| 1.2.2 In-Scope | PM | PM + SA | ✅ Sí — derivar de goals y features |
| 1.2.3 Out-of-Scope | PM | PM | 🔶 Parcial — sugerir sí, decidir no |
| 1.2.4 MVP Definition | PM | PM + TL | 🔶 Parcial — proponer sí, validar viabilidad no |
| 1.2.5 Future Phases | PM | PM | ✅ Sí — agrupar out-of-scope en fases |
| 1.2.6 Assumptions | PM | PM + SA | ✅ Sí — extraer supuestos de docs previos |
| 1.3.1 Stakeholder Map | PgM | PgM | ❌ No — requiere contexto organizacional |
| 1.3.2 Stakeholder Register | PgM | PgM | ❌ No — requiere conocimiento de personas |
| 1.3.3 RACI Matrix | PgM | PgM + PM | ✅ Sí — cruce roles × actividades |
| 1.3.4 Communication Plan | PgM | PgM | 🔶 Parcial — plan estándar sí, ajuste a contexto no |
| 1.4.1 Risk Register | PgM | PgM + TL + SA | ✅ Sí — riesgos estándar por tipo de proyecto |
| 1.4.2 Risk Assessment | PgM | PgM | ✅ Sí — matriz probabilidad × impacto |
| 1.4.3 Mitigation Plan | PgM | Risk Owners | 🔶 Parcial — estrategias estándar sí |
| 1.4.4 Contingency Plan | PgM | PgM + TL | 🔶 Parcial — planes genéricos sí |
| 1.4.5 Risk Monitoring | PgM | PgM | ✅ Sí — setup de proceso |
| 1.5.1 Project Schedule | PgM | PgM + TL | 🔶 Parcial — estructura sí, estimaciones no |
| 1.5.2 Milestones | PgM | PgM | ✅ Sí — extraer del schedule |
| 1.5.3 Phase Breakdown | PgM | PgM | ✅ Sí — derivar del schedule |
| 1.5.4 Sprint Calendar | PgM | PgM | ✅ Sí — generar automáticamente |
| 1.5.5 Dependencies | PgM | PgM + TL | 🔶 Parcial — técnicas no, proceso sí |
| 1.5.6 Critical Path | PgM | PgM | ✅ Sí — calcular del grafo |
| 1.5.7 Buffer Time | PgM | PgM | ✅ Sí — aplicar regla 15-20% |
| 1.6.1 Budget Estimate | PgM | PgM + TL | 🔶 Parcial — template sí, cifras no |
| 1.6.2 Cost Breakdown | PgM | PgM | ✅ Sí — desglosar budget |
| 1.6.3 Resource Plan | PgM | PgM | 🔶 Parcial — template sí, disponibilidad no |
| 1.6.4 ROI Analysis | PgM | PgM + PM | 🔶 Parcial — modelo sí, proyecciones no |
| 1.6.5 Budget Tracking | PgM | PgM | ✅ Sí — setup de proceso |

---

**Documento:** DICCIONARIO_FASE_01_PLANNING.md  
**Versión:** 1.1.0  
**Estado:** ✅ Listo para revisión  
**Siguiente:** DICCIONARIO_FASE_02_ANALYSIS.md
