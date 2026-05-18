# DICCIONARIO DE DELIVERABLES — FASE 3A.2: PERSONAS

**Versión:** 1.1  
**Fecha:** 2026-05-14  
**Fase:** 3A — Design UX/UI  
**Subfase:** 3A.2 — Personas  
**Total deliverables:** 8  
**Responsable de subfase:** UX Designer  
**Aprueba:** Design Lead

---

## Contexto de la subfase

Personas transforma los datos de User Research en arquetipos de usuario vividos y memorables. No es "el usuario promedio" — es un personaje concreto con nombre, cara, motivaciones, frustraciones y contexto. Las personas sirven como proxy del usuario real en cada decisión de diseño: "¿María entendería este flujo?" es más poderoso que "¿el usuario entendería esto?".

**Prerequisitos de subfase:**
- User Research completado (3A.1) — datos empíricos de usuarios reales
- Behavioral Patterns (3A.1.9) — clusters de comportamiento para segmentar personas

**Entrega de subfase:**
- 3-5 personas documentadas que representan a los segmentos principales de usuarios

---

### 3A.2.1 Personas Document

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.2 Personas |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | PDF/MD |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 2-3 días |
| **Frecuencia** | Una vez + refinamientos |

**Perfil de ejecución:** Requiere capacidad de síntesis de research data en personajes creíbles, y habilidad narrativa para que las personas sean memorables y empáticas.  
En VTT: un agente puede generar el documento de personas completo a partir de los datos de research: demographics, motivaciones, frustraciones, goals, y escenarios. Es bastante delegable. Necesita brief con: research report, behavioral patterns, segmentos identificados, y nivel de detalle deseado.

**Qué es:** Documento consolidado que presenta todas las personas del proyecto: persona primaria, secundarias, y anti-personas. Para cada una: nombre, foto/avatar, demographics, background, goals, frustrations, motivaciones, tech savviness, quote representativa, y escenario de uso. Es la referencia canónica de "para quién diseñamos".

**Para qué sirve:** Humaniza los datos de research. En lugar de diseñar para "segmento A, 25-34 años, nivel socio-económico medio", diseñamos para "María García, 29 años, project manager en startup que lidia con 5 herramientas diferentes para coordinar a su equipo". Las personas generan empatía y permiten tomar decisiones de diseño consistentes.

**Inputs requeridos:**
- `3A.1.2` User Research Report — datos empíricos
- `3A.1.9` Behavioral Patterns — segmentación por comportamiento
- `3A.1.7` Pain Points — frustraciones por segmento
- `3A.1.8` User Needs — necesidades por segmento
- `0.4.4` Target Customer Profile — perfil de audiencia target

**Dependencias (predecessors):**
- `3A.1.2` User Research Report *(obligatorio)* — base empírica
- `3A.1.9` Behavioral Patterns *(obligatorio)* — segmentación
- `3A.1.7` Pain Points *(obligatorio)* — frustraciones

**Habilita (successors):**
- `3A.2.2` Persona Cards — cards visuales derivadas
- `3A.2.3` Primary Persona — persona principal seleccionada
- `3A.2.6` Scenarios — escenarios por persona
- `3A.2.7` Empathy Maps — mapas de empatía
- `3A.2.8` Jobs to be Done — JTBD por persona
- `3A.3.1` Site Map — IA diseñada para la persona primaria
- `3A.8.3` Participant Criteria — criterios de reclutamiento para testing

**Audiencia:**
- **Todo el equipo de producto** — referencia compartida del usuario
- **UX/UI Designer** — guía para cada decisión de diseño
- **Product Owner** — validación de segmentación
- **Marketing** — messaging por persona
- **New team members** — onboarding rápido de "para quién construimos"

**Secciones esperadas:**
1. Overview del proceso (cómo se crearon las personas — basadas en research, no inventadas)
2. Resumen de personas (tabla: nombre, tipo, segmento, goal principal)
3. Persona primaria (completa — ver 3A.2.3)
4. Personas secundarias (completas — ver 3A.2.4)
5. Anti-personas (ver 3A.2.5)
6. Mapping personas ↔ features (qué features abordan qué persona)
7. Guía de uso (cómo usar las personas en el día a día)

**Criterio de completitud:**
- [ ] 3-5 personas creadas (1 primaria, 1-3 secundarias, 1 anti-persona)
- [ ] Basadas en research real (no inventadas)
- [ ] Cada persona tiene: demographics, goals, frustrations, context
- [ ] Persona primaria claramente identificada
- [ ] Guía de uso incluida
- [ ] Aprobadas por Design Lead y Product Owner

**Anti-patrones:**
- ❌ **Personas sin research:** Inventar personas basadas en assumptions del equipo — ficción, no diseño centrado en el usuario.
- ❌ **Demasiadas personas:** 8 personas — el equipo no recuerda ninguna. 3-5 es el sweet spot.
- ❌ **Personas estereotipadas:** "María es millennial y le gusta Instagram" — cliché sin profundidad.
- ❌ **Personas que nadie usa:** Documento hermoso que se archiva y nunca se consulta — las personas deben estar visibles y ser referenciadas activamente.

**Template:** `phases/03-design/deliverables/personas-document.md` *(pendiente)*

---

### 3A.2.2 Persona Cards

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.2 Personas |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Designer / UI Designer |
| **Aprueba** | Design Lead |
| **Formato** | Template visual (Figma/PDF) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5-1 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere habilidad de diseño visual para crear cards atractivas y fáciles de consumir.  
En VTT: un agente puede generar el contenido de las persona cards en formato markdown o HTML. NO puede diseñarlas visualmente en Figma. Necesita brief con: datos de cada persona y layout deseado.

**Qué es:** Tarjetas visuales de 1 página por persona que condensan la información clave en un formato rápido de consumir: nombre, foto/avatar, quote, demographics en un vistazo, goals (3-4 bullets), frustrations (3-4 bullets), tech savviness, y contexto de uso. Son la "versión poster" de cada persona para pegar en la pared del equipo o tener en el escritorio.

**Para qué sirve:** El Personas Document de 15 páginas es la referencia detallada. Las Persona Cards son la referencia rápida que el equipo ve todos los días. Son el recordatorio visual constante de para quién diseñamos. Funcionan mejor impresas/pegadas en la oficina o como fondo de pantalla del equipo.

**Inputs requeridos:**
- `3A.2.1` Personas Document — contenido de cada persona

**Dependencias (predecessors):**
- `3A.2.1` Personas Document *(obligatorio)*

**Habilita (successors):**
- Referencia visual diaria para el equipo
- Presentaciones a stakeholders

**Audiencia:**
- **Todo el equipo** — referencia visual rápida

**Secciones esperadas (por card):**
1. Nombre y foto/avatar
2. Quote representativa
3. Demographics (edad, rol, ubicación, tech level)
4. Goals (3-4 bullets)
5. Frustrations (3-4 bullets)
6. Motivaciones clave
7. Contexto de uso (dispositivo, momento, lugar)
8. Tipo de persona (primary/secondary/anti)

**Criterio de completitud:**
- [ ] Una card por persona (3-5 cards)
- [ ] Diseño visual atractivo y consumible en 30 segundos
- [ ] Información clave sin recortar (goals, frustrations, context)
- [ ] Consistencia visual entre cards
- [ ] Formato imprimible

**Anti-patrones:**
- ❌ **Cards con demasiado texto:** Si no cabe en 1 página o se lee en 30 seg, tiene demasiado.
- ❌ **Cards feas:** Si no son visualmente atractivas, nadie las pone en su escritorio.
- ❌ **Cards sin quote:** La quote es lo más memorable — la frase que encapsula a la persona.

**Template:** `phases/03-design/deliverables/persona-card.figma` *(pendiente)*

---

### 3A.2.3 Primary Persona

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.2 Personas |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Card (Figma/PDF) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere juicio para elegir cuál de las personas es la primaria: la que representa al segmento de mayor valor/volumen y para la que se optimiza el diseño cuando hay trade-offs.  
En VTT: un agente puede documentar la primary persona con todos sus detalles. NO puede decidir cuál persona es la primaria — esa es una decisión estratégica del UX Designer + Product Owner. Necesita brief con: persona elegida como primaria y justificación.

**Qué es:** La persona principal del proyecto: el usuario para el que se optimiza el diseño. Cuando hay un trade-off de diseño ("¿hacemos esto más fácil para usuarios novatos o para expertos?"), la primary persona resuelve el conflicto. Es la representación más detallada: incluye un "Day in the Life" narrativo, journey map simplificado, y contexto completo.

**Para qué sirve:** En un proyecto con 3 personas, no se puede optimizar igualmente para todas — hay trade-offs. La primary persona es la prioridad: si un diseño funciona para ella pero no para la persona secundaria, se acepta. Si no funciona para la primaria, se itera. Es la brújula de diseño.

**Inputs requeridos:**
- `3A.2.1` Personas Document — personas creadas
- `3A.1.9` Behavioral Patterns — segmento más importante
- Decisión del Product Owner sobre segmento prioritario

**Dependencias (predecessors):**
- `3A.2.1` Personas Document *(obligatorio)*

**Habilita (successors):**
- `3A.3.1` Site Map — IA optimizada para la primaria
- `3A.4.1` Wireframe Document — wireframes diseñados para la primaria
- `3A.8.3` Participant Criteria — reclutamiento prioriza perfil de la primaria

**Audiencia:**
- **Todo el equipo de producto** — "para quién diseñamos primero"

**Secciones esperadas:**
1. Toda la información de la Persona Card (3A.2.2)
2. Day in the Life (narrativa de un día típico)
3. Journey map simplificado (etapas de interacción con el dominio)
4. Herramientas que usa actualmente (con frustraciones específicas)
5. Goals detallados (corto, mediano, largo plazo)
6. Métricas de éxito de la persona (cómo mide si logró su goal)
7. Justificación de por qué es la primaria

**Criterio de completitud:**
- [ ] Nivel de detalle superior a las personas secundarias
- [ ] Day in the Life narrativo incluido
- [ ] Justificación de selección como primaria documentada
- [ ] Aprobada por Product Owner
- [ ] El equipo sabe quién es la primary persona

**Anti-patrones:**
- ❌ **Primary persona = el CEO:** Diseñar para el stakeholder que paga en vez de para el usuario final.
- ❌ **Primary sin justificación:** "Es la primaria porque sí" — debe estar basada en datos (volumen, revenue, strategic importance).
- ❌ **Cambiar la primaria cada sprint:** Indica que no se ha definido bien — la primaria es estable.

**Template:** `phases/03-design/deliverables/primary-persona.md` *(pendiente)*

---

### 3A.2.4 Secondary Personas

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.2 Personas |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Cards (Figma/PDF) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5-1 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere capacidad de diferenciar claramente cada persona secundaria de la primaria y entre sí.  
En VTT: un agente puede documentar las personas secundarias con el mismo nivel de detalle. Es bastante delegable. Necesita brief con: datos de cada persona secundaria y su diferenciador clave vs la primaria.

**Qué es:** Las 1-3 personas que representan segmentos de usuarios adicionales al primario. Tienen el mismo formato que la primaria pero con menor nivel de detalle. Cada secundaria tiene un diferenciador claro: diferente rol, diferente nivel de experiencia, diferente contexto de uso, o diferente objetivo principal.

**Para qué sirve:** Aseguran que el diseño no ignora completamente a otros segmentos. Cuando se diseña un feature, se verifica: "funciona para la primaria ✅, ¿funciona razonablemente para las secundarias?". No se optimiza para ellas, pero tampoco se las excluye.

**Inputs requeridos:**
- `3A.2.1` Personas Document — personas definidas
- `3A.1.9` Behavioral Patterns — segmentos secundarios

**Dependencias (predecessors):**
- `3A.2.1` Personas Document *(obligatorio)*
- `3A.2.3` Primary Persona *(obligatorio)* — definida primero para diferenciar

**Habilita (successors):**
- `3A.2.6` Scenarios — escenarios específicos por persona secundaria
- `3A.2.7` Empathy Maps — mapas por persona

**Audiencia:**
- **UX/UI Designer** — verificación de diseño para múltiples segmentos
- **Product Manager** — features por segmento

**Secciones esperadas (por persona):**
1. Persona Card completa (mismos campos que 3A.2.2)
2. Diferenciador clave vs primary persona
3. Cómo su experiencia difiere (qué features le importan más/menos)
4. Trade-offs aceptables (qué puede ser subóptimo para esta persona)

**Criterio de completitud:**
- [ ] 1-3 personas secundarias definidas
- [ ] Diferenciador claro vs primaria documentado
- [ ] Trade-offs aceptables documentados
- [ ] Mismo formato que la primaria (consistencia)

**Anti-patrones:**
- ❌ **Secundarias idénticas a la primaria:** Si no hay diferencia significativa, no es otra persona — es la misma.
- ❌ **Secundarias sin uso:** Crearlas pero nunca verificar los diseños contra ellas — esfuerzo desperdiciado.
- ❌ **Demasiadas secundarias:** 5 secundarias — nadie las diferencia. 1-3 es suficiente.

**Template:** `phases/03-design/deliverables/secondary-personas.md` *(pendiente)*

---

### 3A.2.5 Anti-Personas

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.2 Personas |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Card (Figma/PDF) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.25 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere claridad sobre quién NO es el usuario target y por qué excluirlo del diseño.  
En VTT: un agente puede documentar anti-personas a partir de la definición de scope y target customer. Es altamente delegable. Necesita brief con: quién NO es el usuario, por qué, y qué implicaciones tiene para el diseño.

**Qué es:** Definición explícita de quién NO es usuario del producto: personas para las que deliberadamente NO diseñamos. La anti-persona tiene: perfil, por qué no es target, y qué decisiones de diseño implica excluirla. Ejemplos: "no diseñamos para usuarios que nunca han usado una computadora", "no diseñamos para empresas de 500+ empleados".

**Para qué sirve:** Poner boundaries al diseño. Sin anti-personas, el scope se expande infinitamente: "¿y si un usuario de 80 años quiere usarlo? ¿y si es ciego? ¿y si no tiene internet?". Las anti-personas dicen explícitamente "estos casos están fuera de scope" para que el equipo no intente diseñar para todos.

**Inputs requeridos:**
- `3A.2.1` Personas Document — contexto de personas definidas
- `0.4.4` Target Customer Profile — quién SÍ es target
- `1.2.3` Out of Scope — qué está fuera de scope

**Dependencias (predecessors):**
- `3A.2.1` Personas Document *(obligatorio)*
- `0.4.4` Target Customer Profile *(recomendado)*

**Habilita (successors):**
- Decisiones de scope de diseño
- `3A.8.3` Participant Criteria — exclusión en reclutamiento

**Audiencia:**
- **UX/UI Designer** — saber para quién NO optimizar
- **Product Owner** — validación de exclusiones

**Secciones esperadas:**
1. Anti-persona card (nombre, perfil breve)
2. Por qué NO es target (justificación de negocio/producto)
3. Qué implica para el diseño (qué NO hacer para acomodarla)
4. Riesgo de incluirla (qué complejidad agregaría)

**Criterio de completitud:**
- [ ] Al menos 1 anti-persona definida
- [ ] Justificación de exclusión documentada
- [ ] Implicaciones para diseño explícitas
- [ ] Aprobada por Product Owner

**Anti-patrones:**
- ❌ **Anti-persona discriminatoria:** Excluir por demographics irrelevantes — las exclusiones deben ser por comportamiento o necesidades, no por edad/género/raza.
- ❌ **Sin anti-personas:** Intentar diseñar para todos = no optimizar para nadie.
- ❌ **Anti-persona secreta:** Exclusiones no documentadas que se aplican inconsistentemente.

**Template:** `phases/03-design/deliverables/anti-personas.md` *(pendiente)*

---

### 3A.2.6 Scenarios

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.2 Personas |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Narrativas (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez + nuevos por feature |

**Perfil de ejecución:** Requiere habilidad narrativa para escribir escenarios que sean realistas, específicos, y contextualizados en la vida de cada persona.  
En VTT: un agente puede generar escenarios narrativos a partir de las personas, user needs, y use cases del producto. Es altamente delegable. Necesita brief con: personas, use cases principales, y contexto situacional.

**Qué es:** Narrativas cortas (1-2 párrafos cada una) que describen cómo cada persona usa el producto en una situación realista: el contexto (dónde está, qué está haciendo, qué necesita), el trigger (qué dispara la interacción), la interacción esperada (qué hace con el producto), y el outcome deseado (qué logra). Son "historias" del uso del producto en contexto real.

**Para qué sirve:** Los use cases son funcionales ("el usuario puede crear un proyecto"). Los scenarios son contextuals ("María está en el metro camino a la oficina, recuerda que tiene reunión en 30 min, abre la app para revisar el status de su proyecto y preparar 3 talking points rápidamente"). Los scenarios dan el contexto emocional y situacional que los use cases no tienen.

**Inputs requeridos:**
- `3A.2.1` Personas Document — personas
- `3A.1.8` User Needs — necesidades a resolver
- `2.3.4` Detailed Use Cases — funcionalidades del producto

**Dependencias (predecessors):**
- `3A.2.1` Personas Document *(obligatorio)*
- `3A.1.8` User Needs *(obligatorio)*

**Habilita (successors):**
- `3A.4.8` Wireframe Flows — flujos diseñados para escenarios
- `3A.8.2` Test Script — escenarios como base de tareas de testing
- `2.4.2` User Stories — escenarios informan stories

**Audiencia:**
- **UX Designer** — contexto para diseño de flujos
- **UI Designer** — contexto situacional (mobile? prisa? distracción?)
- **QA Engineer** — escenarios de testing realistas

**Secciones esperadas:**
1. Escenarios por persona (2-3 por persona)
2. Por escenario: contexto, trigger, interacción, outcome
3. Escenarios positivos (la persona logra su goal)
4. Escenarios de frustración (la persona no logra su goal con soluciones actuales)
5. Mapping escenario → use case (cross-reference)

**Criterio de completitud:**
- [ ] Al menos 2 escenarios por persona principal
- [ ] Contexto situacional incluido (dónde, cuándo, con qué dispositivo)
- [ ] Trigger realista (no "el usuario abre la app")
- [ ] Outcome claro (qué logra la persona)
- [ ] Mapping a use cases

**Anti-patrones:**
- ❌ **Escenarios genéricos:** "El usuario abre la app y crea un proyecto" — sin contexto, sin emoción, sin valor agregado sobre el use case.
- ❌ **Escenarios irrealistas:** Situaciones que nunca ocurrirían — no informan el diseño.
- ❌ **Solo escenarios positivos:** No mostrar escenarios de frustración — pierde la oportunidad de diseñar para el "momento difícil".

**Template:** `phases/03-design/deliverables/scenarios.md` *(pendiente)*

---

### 3A.2.7 Empathy Maps

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.2 Personas |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Diagrama (Figma/Miro) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere empatía y capacidad de sintetizar research en los 4 cuadrantes del empathy map.  
En VTT: un agente puede generar el contenido de empathy maps a partir del research report y las personas. Es bastante delegable como texto; el diseño visual requiere Figma. Necesita brief con: persona, research data, y contexto de uso del producto.

**Qué es:** Diagrama visual de 4 cuadrantes (Says, Thinks, Does, Feels) por persona, centrado en la interacción con el dominio del producto. Captura: qué dice la persona (citas textuales), qué piensa (preocupaciones internas), qué hace (acciones observables), y qué siente (emociones). Es una herramienta de empatía, no de funcionalidad.

**Para qué sirve:** El empathy map captura la dimensión emocional que las persona cards no profundizan. Revela la tensión entre lo que la persona dice ("no necesito ayuda") y lo que piensa/siente ("estoy perdida y frustrada"). Esa tensión informa diseños más empáticos y soluciones que abordan necesidades no expresadas.

**Inputs requeridos:**
- `3A.2.1` Personas Document — personas
- `3A.1.4` Interview Transcripts — citas para "Says"
- `3A.1.9` Behavioral Patterns — acciones para "Does"
- `3A.1.7` Pain Points — frustraciones para "Feels"

**Dependencias (predecessors):**
- `3A.2.1` Personas Document *(obligatorio)*
- `3A.1.2` User Research Report *(obligatorio)* — datos empíricos

**Habilita (successors):**
- `3A.4.1` Wireframe Document — diseño empático
- Workshops de diseño — herramienta de alineación de equipo

**Audiencia:**
- **UX/UI Designer** — dimensión emocional del usuario
- **Product Owner** — empatía con el usuario
- **Todo el equipo** — alineación en "cómo se siente el usuario"

**Secciones esperadas (por empathy map):**
1. Persona referenciada
2. Says (citas textuales de entrevistas — 4-6 bullets)
3. Thinks (pensamientos internos inferidos — 4-6 bullets)
4. Does (acciones observables y comportamientos — 4-6 bullets)
5. Feels (emociones identificadas — 4-6 bullets)
6. Pain & Gain summary (derivado de los 4 cuadrantes)

**Criterio de completitud:**
- [ ] Un empathy map por persona principal (al menos primary + 1 secondary)
- [ ] Los 4 cuadrantes completados con datos de research
- [ ] "Says" con citas reales (no inventadas)
- [ ] Tensiones entre cuadrantes identificadas (dice vs piensa)
- [ ] Formato visual claro

**Anti-patrones:**
- ❌ **Empathy map inventado:** Llenar los cuadrantes con suposiciones sin research — ficción disfrazada de empatía.
- ❌ **Cuadrantes repetitivos:** "Says" y "Thinks" idénticos — la tensión entre ambos es lo valioso.
- ❌ **Empathy map como ejercicio único:** Hacerlo en un workshop y no volver a consultarlo — pierde valor.

**Template:** `phases/03-design/deliverables/empathy-map.figma` *(pendiente)*

---

### 3A.2.8 Jobs to be Done

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.2 Personas |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Lista (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5-1 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere entendimiento del framework JTBD (Christensen/Ulwick): formular jobs en el formato "Cuando [situación], quiero [motivación], para poder [resultado esperado]".  
En VTT: un agente puede formular JTBD statements a partir de las personas, user needs, y scenarios. Es altamente delegable. Necesita brief con: personas, needs, scenarios, y contexto del producto.

**Qué es:** Lista de Jobs to be Done por persona: statements en formato "Cuando [situación], quiero [motivación], para poder [resultado esperado]". Capturan qué "trabajo" el usuario está tratando de lograr con el producto (no qué features usa). Los JTBD se categorizan en: funcionales, emocionales, y sociales. Se priorizan por importancia e insatisfacción actual.

**Para qué sirve:** Los JTBD son la mejor guía para decidir features: el producto existe para ayudar al usuario a completar un "trabajo". "Contrato" Netflix no para ver películas, sino para "cuando llego cansado del trabajo, quiero desconectarme fácilmente, para poder relajarme sin tener que pensar qué hacer". Los JTBD revelan competidores inesperados (TV, libro, siesta — todos compiten por el mismo job).

**Inputs requeridos:**
- `3A.2.1` Personas Document — personas
- `3A.1.8` User Needs — necesidades como base de jobs
- `3A.2.6` Scenarios — situaciones que contextualizan los jobs
- `3A.1.7` Pain Points — insatisfacción actual

**Dependencias (predecessors):**
- `3A.2.1` Personas Document *(obligatorio)*
- `3A.1.8` User Needs *(obligatorio)*
- `3A.2.6` Scenarios *(recomendado)*

**Habilita (successors):**
- `2.4.2` User Stories — stories derivadas de JTBD
- `1.2.4` MVP Definition — features que resuelven top jobs
- Feature prioritization — priorizar por importancia × insatisfacción

**Audiencia:**
- **Product Owner** — feature prioritization basada en jobs
- **UX Designer** — diseño orientado al job, no a features
- **Product Manager** — competitive landscape por job
- **Marketing** — messaging basado en jobs

**Secciones esperadas:**
1. Lista de JTBD por persona (formato: "Cuando [situación], quiero [motivación], para poder [resultado]")
2. Categorización (funcional, emocional, social)
3. Priorización por importancia × insatisfacción (opportunity score)
4. Mapping JTBD → features del producto
5. Competidores por job (qué soluciones actuales "contratan" los usuarios para cada job)
6. Underserved jobs (alta importancia, alta insatisfacción — oportunidad)

**Criterio de completitud:**
- [ ] Al menos 5 JTBD documentados para la persona primaria
- [ ] Formato correcto (Cuando/Quiero/Para poder)
- [ ] Categorización funcional/emocional/social
- [ ] Priorización aplicada
- [ ] Mapping a features del producto
- [ ] Competidores por job identificados

**Anti-patrones:**
- ❌ **JTBD = features:** "Quiero un botón de exportar" — eso es una solución, no un job. El job es "quiero compartir resultados con mi equipo".
- ❌ **Solo funcionales:** Ignorar jobs emocionales ("sentirme en control") y sociales ("impresionar a mi jefe") — pierden las motivaciones profundas.
- ❌ **JTBD sin priorización:** Lista de 20 jobs sin importancia ni insatisfacción — no guía decisiones.
- ❌ **JTBD sin competidores:** No identificar cómo resuelven el job actualmente — no se entiende contra qué se compite.

**Template:** `phases/03-design/deliverables/jobs-to-be-done.md` *(pendiente)*

---

## Tabla resumen de ejecutores — Fase 3A.2 Personas

| Deliverable | Responsable | Ejecuta | Delegable VTT |
|-------------|-------------|---------|---------------|
| 3A.2.1 Personas Document | UX Designer | UX Designer | ✅ — puede generar documento completo de personas desde research data |
| 3A.2.2 Persona Cards | UX Designer | UX Designer / UI Designer | 🔶 Parcial — puede generar contenido, diseño visual requiere Figma |
| 3A.2.3 Primary Persona | UX Designer | UX Designer | 🔶 Parcial — puede documentar, pero selección de primaria requiere juicio |
| 3A.2.4 Secondary Personas | UX Designer | UX Designer | ✅ — puede documentar personas secundarias |
| 3A.2.5 Anti-Personas | UX Designer | UX Designer | ✅ — puede documentar anti-personas desde scope y target |
| 3A.2.6 Scenarios | UX Designer | UX Designer | ✅ — puede generar escenarios narrativos desde personas y use cases |
| 3A.2.7 Empathy Maps | UX Designer | UX Designer | ✅ — puede generar contenido de los 4 cuadrantes desde research |
| 3A.2.8 Jobs to be Done | UX Designer | UX Designer | ✅ — puede formular JTBD statements desde needs y scenarios |

---

## Siguiente archivo

**Próximo:** `DICCIONARIO_FASE_03A_03_INFORMATION_ARCHITECTURE.md` — 8 deliverables (3A.3.1 a 3A.3.8)
