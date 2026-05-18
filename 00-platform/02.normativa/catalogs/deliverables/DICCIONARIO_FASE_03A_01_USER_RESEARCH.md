# DICCIONARIO DE DELIVERABLES — FASE 3A.1: USER RESEARCH

**Versión:** 1.1  
**Fecha:** 2026-05-14  
**Fase:** 3A — Design UX/UI  
**Subfase:** 3A.1 — User Research  
**Total deliverables:** 9  
**Responsable de subfase:** UX Designer  
**Aprueba:** Design Lead

---

## Contexto de la subfase

User Research es la base empírica del diseño. Antes de diseñar una sola pantalla, hay que entender a los usuarios reales: quiénes son, qué necesitan, qué les frustra, cómo se comportan, y qué esperan del producto. Diseñar sin research es diseñar para uno mismo. User Research valida (o invalida) las assumptions del equipo con datos reales.

**Prerequisitos de subfase:**
- Problem Statement (0.3.1) y User Pain Points (0.3.2) — hipótesis a validar
- Target Customer Profile (0.4.4) — audiencia a investigar
- Use Cases (2.3) — funcionalidades planificadas como contexto

**Entrega de subfase:**
- Comprensión documentada de los usuarios reales que informa todo el diseño posterior

---

### 3A.1.1 User Research Plan

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.1 User Research |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Researcher / UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Documento (MD/PDF) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Una vez por ronda de research |

**Perfil de ejecución:** Requiere experiencia en métodos de investigación de usuarios: cualitativos (entrevistas, contextual inquiry) y cuantitativos (surveys, analytics). Debe saber elegir el método correcto según el objetivo de investigación.  
En VTT: un agente puede generar la estructura del plan de research a partir de los objetivos del proyecto y las preguntas de investigación. Puede redactar objetivos, metodología propuesta, y timeline. NO puede decidir el método óptimo sin contexto del UX Researcher. Necesita brief con: qué preguntas de investigación responder, audiencia target, budget/timeline, y restricciones (remoto vs presencial).

**Qué es:** Documento que define el plan completo de investigación de usuarios: objetivos del estudio, preguntas de investigación, metodología (entrevistas, surveys, contextual inquiry, diary studies), perfil de participantes, tamaño de muestra, timeline, herramientas, y presupuesto. Es el "proyecto" de la investigación.

**Para qué sirve:** Sin plan, la investigación es ad-hoc: "le pregunté a 3 amigos qué opinan". El plan asegura que el estudio es riguroso, tiene preguntas claras, usa métodos apropiados, y produce insights accionables. También permite al Design Lead validar la inversión antes de ejecutar.

**Inputs requeridos:**
- `0.3.1` Problem Statement — hipótesis a validar
- `0.3.2` User Pain Points — puntos de dolor a investigar
- `0.4.4` Target Customer Profile — audiencia a reclutar
- Preguntas de investigación del Product Owner

**Dependencias (predecessors):**
- `0.3.1` Problem Statement *(obligatorio)* — contexto del problema
- `0.4.4` Target Customer Profile *(obligatorio)* — audiencia target
- `0.3.2` User Pain Points *(recomendado)* — hipótesis a validar

**Habilita (successors):**
- `3A.1.2` User Research Report — resultados del plan ejecutado
- `3A.1.3` Interview Guide — guía derivada del plan
- `3A.1.5` Survey Results — survey derivada del plan

**Audiencia:**
- **UX Designer** — ejecutor del plan
- **Design Lead** — aprobación de metodología y budget
- **Product Owner** — validación de preguntas de investigación
- **Product Manager** — alineación con prioridades

**Secciones esperadas:**
1. Objetivos del estudio (qué queremos aprender)
2. Preguntas de investigación (3-7 preguntas específicas)
3. Metodología (cualitativa, cuantitativa, mixta — justificada)
4. Métodos específicos (entrevistas, surveys, contextual inquiry, analytics review)
5. Perfil de participantes (demographics, comportamiento, criterios)
6. Tamaño de muestra y justificación
7. Timeline (reclutamiento, ejecución, análisis, reporte)
8. Herramientas (Maze, Typeform, Zoom, Dovetail, etc.)
9. Presupuesto (incentivos, herramientas, reclutamiento)
10. Riesgos y mitigaciones del estudio
11. Entregables esperados (qué documentos producirá el estudio)

**Criterio de completitud:**
- [ ] Objetivos claros y alineados con preguntas de negocio
- [ ] Metodología definida y justificada
- [ ] Perfil de participantes con criterios de reclutamiento
- [ ] Tamaño de muestra definido (mínimo 5 para cualitativo, 30+ para cuantitativo)
- [ ] Timeline con fechas
- [ ] Budget estimado
- [ ] Aprobado por Design Lead

**Anti-patrones:**
- ❌ **Research sin plan:** "Vamos a hablar con unos usuarios y ver qué sale" — no produce insights estructurados.
- ❌ **Solo surveys:** Enviar un Google Form y declarar "hicimos research" — los surveys sin entrevistas no capturan el "por qué".
- ❌ **Plan demasiado ambicioso:** 50 entrevistas + 3 diary studies + eye tracking para un MVP — el plan debe ser proporcional al proyecto.
- ❌ **Preguntas de confirmación:** "¿No crees que nuestra solución es genial?" — sesgo de confirmación.

**Template:** `phases/03-design/deliverables/user-research-plan.md` *(pendiente)*

---

### 3A.1.2 User Research Report

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.1 User Research |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Researcher / UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | PDF/MD |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 2-3 días |
| **Frecuencia** | Una vez por ronda de research |

**Perfil de ejecución:** Requiere capacidad de síntesis: transformar horas de entrevistas y datos crudos en hallazgos accionables con recomendaciones para diseño.  
En VTT: un agente puede estructurar el reporte, organizar hallazgos por tema, y consolidar datos cuantitativos. NO puede observar sesiones ni interpretar lenguaje corporal o contexto emocional. Necesita brief con: transcripciones de entrevistas, resultados de surveys, notas de observación, y temas emergentes identificados por el researcher.

**Qué es:** Informe completo de la investigación de usuarios que consolida todos los hallazgos: resumen ejecutivo, metodología aplicada, perfil de participantes, hallazgos cualitativos (temas, patrones), datos cuantitativos (survey results), insights accionables, y recomendaciones para diseño. Es el documento final de la investigación.

**Para qué sirve:** Transforma datos crudos (transcripciones, respuestas de survey) en conocimiento accionable. Le dice al equipo de diseño: "esto es lo que descubrimos sobre los usuarios, y esto es lo que recomendamos hacer con esa información". Es la evidencia que fundamenta todas las decisiones de diseño posteriores.

**Inputs requeridos:**
- `3A.1.1` User Research Plan — plan ejecutado
- `3A.1.3` Interview Guide — guía utilizada
- `3A.1.4` Interview Transcripts — datos crudos cualitativos
- `3A.1.5` Survey Results — datos crudos cuantitativos

**Dependencias (predecessors):**
- `3A.1.1` User Research Plan *(obligatorio)* — plan que se ejecutó
- `3A.1.4` Interview Transcripts *(obligatorio)* — datos de entrevistas
- `3A.1.5` Survey Results *(recomendado)* — datos cuantitativos

**Habilita (successors):**
- `3A.1.6` User Insights — insights extraídos del reporte
- `3A.1.7` Pain Points — puntos de dolor validados
- `3A.1.8` User Needs — necesidades identificadas
- `3A.1.9` Behavioral Patterns — patrones de comportamiento
- `3A.2.1` Personas Document — personas basadas en research

**Audiencia:**
- **UX Designer** — base para diseño
- **UI Designer** — contexto de usuarios
- **Design Lead** — validación de hallazgos
- **Product Owner** — insights de negocio
- **Product Manager** — priorización informada
- **Stakeholders** — visibilidad de resultados

**Secciones esperadas:**
1. Resumen ejecutivo (3-5 hallazgos principales en 1 párrafo)
2. Metodología aplicada (qué se hizo, cuándo, con cuántos)
3. Perfil de participantes (demographics, anonimizado)
4. Hallazgos cualitativos agrupados por tema
5. Datos cuantitativos (survey results con gráficos)
6. Insights accionables (qué significan los hallazgos para el diseño)
7. Citas textuales relevantes (anonimizadas)
8. Recomendaciones de diseño derivadas de los hallazgos
9. Limitaciones del estudio
10. Próximos pasos

**Criterio de completitud:**
- [ ] Resumen ejecutivo conciso y accionable
- [ ] Metodología documentada
- [ ] Al menos 5 hallazgos principales documentados
- [ ] Datos cualitativos y cuantitativos incluidos
- [ ] Recomendaciones de diseño específicas
- [ ] Citas de participantes anonimizadas
- [ ] Limitaciones del estudio reconocidas

**Anti-patrones:**
- ❌ **Reporte de 80 páginas que nadie lee:** Demasiado detalle — el resumen ejecutivo debe bastar para el 80% de la audiencia.
- ❌ **Solo datos, sin insights:** Presentar transcripciones sin interpretación — datos sin análisis no son conocimiento.
- ❌ **Hallazgos sin recomendaciones:** "Los usuarios están frustrados con X" sin decir qué hacer al respecto.
- ❌ **Cherry-picking:** Seleccionar solo los datos que confirman las hipótesis del equipo.

**Template:** `phases/03-design/deliverables/user-research-report.md` *(pendiente)*

---

### 3A.1.3 Interview Guide

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.1 User Research |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Researcher / UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Documento (MD/PDF) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5-1 día |
| **Frecuencia** | Una vez por ronda de research |

**Perfil de ejecución:** Requiere experiencia en formular preguntas abiertas y no-sesgadas, y estructurar una conversación que fluya naturalmente.  
En VTT: un agente puede generar la interview guide completa a partir del research plan: intro, warm-up, preguntas por tema, probes/follow-ups, y cierre. Es bastante delegable. Necesita brief con: preguntas de investigación, perfil de participante, y contexto del producto.

**Qué es:** Guía semi-estructurada para las entrevistas de investigación: script de introducción, preguntas de warm-up (contexto del participante), preguntas principales agrupadas por tema de investigación, probes/follow-ups para profundizar, y preguntas de cierre. Es semi-estructurada: las preguntas guían pero permiten exploración.

**Para qué sirve:** Garantiza consistencia entre entrevistas (todos los participantes responden las mismas preguntas core) mientras permite flexibilidad para profundizar en temas emergentes. Sin guía, cada entrevista va en una dirección diferente y los datos no son comparables.

**Inputs requeridos:**
- `3A.1.1` User Research Plan — preguntas de investigación
- `0.4.4` Target Customer Profile — contexto del participante
- `0.3.2` User Pain Points — temas a explorar

**Dependencias (predecessors):**
- `3A.1.1` User Research Plan *(obligatorio)* — preguntas de investigación

**Habilita (successors):**
- `3A.1.4` Interview Transcripts — entrevistas ejecutadas con la guía
- `3A.1.2` User Research Report — datos producidos con la guía

**Audiencia:**
- **UX Designer / Moderador** — guía durante entrevistas
- **Observadores** — saben qué esperar
- **Design Lead** — revisión de calidad de preguntas

**Secciones esperadas:**
1. Script de introducción (presentación, consent, expectativas, duración)
2. Warm-up (3-5 preguntas de contexto: rol, experiencia, herramientas actuales)
3. Preguntas principales por tema de investigación (5-7 preguntas abiertas)
4. Probes/follow-ups sugeridos (por tema)
5. Preguntas de cierre (resumen, algo que no cubrimos, deseos)
6. Notas para el moderador (cuándo profundizar, cuándo avanzar)
7. Duración estimada por sección (total: 30-45 min)

**Criterio de completitud:**
- [ ] Intro con consent documentada
- [ ] Preguntas abiertas (no yes/no)
- [ ] Preguntas agrupadas por tema de investigación
- [ ] Probes para profundizar en cada tema
- [ ] Preguntas de cierre incluidas
- [ ] Duración total ≈ 30-45 min
- [ ] Revisada por alguien que no la escribió

**Anti-patrones:**
- ❌ **Preguntas cerradas:** "¿Usas apps de productividad?" (sí/no) vs "Cuéntame cómo organizas tu trabajo día a día" (abierta).
- ❌ **Leading questions:** "¿No te parece que X es un problema?" — sesga la respuesta.
- ❌ **Demasiadas preguntas:** 30 preguntas en 45 min — no hay tiempo para profundizar.
- ❌ **Sin warm-up:** Ir directo a preguntas difíciles sin romper el hielo — participante tenso, respuestas superficiales.

**Template:** `phases/03-design/deliverables/interview-guide.md` *(pendiente)*

---

### 3A.1.4 Interview Transcripts

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.1 User Research |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Researcher / Transcription service |
| **Aprueba** | UX Designer |
| **Formato** | Documentos (MD/PDF) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día por entrevista (o automático con herramienta) |
| **Frecuencia** | Una por participante |

**Perfil de ejecución:** Requiere capacidad de transcripción o uso de herramientas de AI transcription (Otter.ai, Rev, Fireflies). Debe asegurar anonimización de datos personales.  
En VTT: un agente puede limpiar y formatear transcripciones automáticas, anonimizar datos personales, y organizar por tema/pregunta. Es altamente delegable. Necesita brief con: grabaciones o transcripciones raw, convención de naming, y política de anonimización.

**Qué es:** Registro textual de cada entrevista de investigación: transcripción completa o notas detalladas de la conversación, con timestamps, identificador anonimizado del participante (P01, P02...), y marcas de temas/insights relevantes. Son los datos crudos del estudio cualitativo.

**Para qué sirve:** Las transcripciones son la evidencia primaria del estudio. Permiten: revisión posterior detallada, análisis temático (coding), extracción de citas textuales para el reporte, y auditoría del proceso. Sin transcripciones, los hallazgos dependen de la memoria del researcher — subjetiva y selectiva.

**Inputs requeridos:**
- `3A.1.3` Interview Guide — estructura de la conversación
- Grabaciones de entrevistas (audio/video)
- Consentimiento firmado de participantes

**Dependencias (predecessors):**
- `3A.1.3` Interview Guide *(obligatorio)* — guía usada en las entrevistas
- Entrevistas ejecutadas

**Habilita (successors):**
- `3A.1.2` User Research Report — análisis de transcripciones
- `3A.1.6` User Insights — insights extraídos
- `3A.1.9` Behavioral Patterns — patrones identificados en transcripciones

**Audiencia:**
- **UX Designer** — análisis temático
- **Design Lead** — verificación de hallazgos
- **Product Owner** — citas relevantes

**Secciones esperadas (por transcripción):**
1. Metadata (participante ID, fecha, duración, moderador)
2. Perfil del participante (anonimizado: demographics relevantes)
3. Transcripción completa o notas detalladas
4. Highlights/tags de temas relevantes
5. Observaciones del moderador (lenguaje corporal, emociones si presencial)

**Criterio de completitud:**
- [ ] Todas las entrevistas transcritas o documentadas con notas detalladas
- [ ] Participantes anonimizados (P01, P02... — sin nombres reales)
- [ ] Metadata registrada (fecha, duración)
- [ ] Datos personales eliminados de transcripciones
- [ ] Almacenadas en ubicación segura (datos de research son sensibles)

**Anti-patrones:**
- ❌ **Sin transcripción:** Solo notas mentales — los detalles se pierden en 24 horas.
- ❌ **Datos no anonimizados:** Nombres reales en transcripciones compartidas — violación de privacidad.
- ❌ **Transcripción sin revisión:** Transcripción automática con errores no corregidos — datos incorrectos.
- ❌ **Almacenamiento inseguro:** Transcripciones en Google Drive público — datos de participantes expuestos.

**Template:** `phases/03-design/deliverables/interview-transcript.md` *(pendiente)*

---

### 3A.1.5 Survey Results

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.1 User Research |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Researcher / UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Gráficos/Tablas |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días (análisis y visualización) |
| **Frecuencia** | Una vez por ronda de research |

**Perfil de ejecución:** Requiere capacidad de diseñar surveys válidos, analizar datos cuantitativos, y visualizar resultados de forma comprensible.  
En VTT: un agente puede analizar datos de surveys (agregaciones, cross-tabulations, visualizaciones), generar gráficos, y redactar el reporte de resultados. Es altamente delegable si los datos están en formato estructurado. Necesita brief con: CSV/export del survey, preguntas del survey, y preguntas de investigación a responder.

**Qué es:** Documento con los resultados analizados y visualizados del survey cuantitativo: tasa de respuesta, datos demográficos de respondents, resultados por pregunta (gráficos de barra, pie, escala), cross-tabulations relevantes, y insights derivados de los datos cuantitativos.

**Para qué sirve:** Los surveys complementan las entrevistas con datos a escala: mientras 5 entrevistas dan profundidad, un survey de 100+ respuestas da validez estadística. Los results confirman o contradicen los hallazgos cualitativos con números. Son evidencia fuerte para stakeholders que prefieren datos cuantitativos.

**Inputs requeridos:**
- `3A.1.1` User Research Plan — survey como parte del plan
- Survey diseñado y distribuido (Typeform, Google Forms, SurveyMonkey)
- Datos crudos exportados

**Dependencias (predecessors):**
- `3A.1.1` User Research Plan *(obligatorio)* — survey planificado

**Habilita (successors):**
- `3A.1.2` User Research Report — datos cuantitativos del reporte
- `3A.1.6` User Insights — insights cuantitativos
- `3A.1.7` Pain Points — puntos de dolor cuantificados

**Audiencia:**
- **UX Designer** — datos para informar diseño
- **Product Owner** — datos cuantitativos de usuarios
- **Product Manager** — priorización basada en datos
- **Stakeholders** — evidencia cuantitativa

**Secciones esperadas:**
1. Metodología del survey (plataforma, distribución, periodo, incentivo)
2. Tasa de respuesta y muestra
3. Perfil de respondents (demographics, segmentación)
4. Resultados por pregunta (gráfico + interpretación)
5. Cross-tabulations relevantes (resultados cruzados por segmento)
6. Preguntas abiertas (temas principales codificados)
7. Insights principales derivados de los datos
8. Limitaciones (sesgo de muestra, tasa de respuesta)

**Criterio de completitud:**
- [ ] Tasa de respuesta reportada
- [ ] Al menos 30 respuestas para significancia mínima
- [ ] Resultados por pregunta visualizados
- [ ] Insights derivados de los datos (no solo gráficos)
- [ ] Limitaciones reconocidas
- [ ] Datos crudos accesibles para re-análisis

**Anti-patrones:**
- ❌ **Survey de 40 preguntas:** Encuesta demasiado larga — abandono masivo, datos incompletos.
- ❌ **Solo gráficos sin interpretación:** Pie charts bonitos sin decir qué significan — datos sin insights.
- ❌ **10 respuestas como conclusiones:** Sample size insuficiente presentado como "dato definitivo".
- ❌ **Preguntas sesgadas en el survey:** "¿Qué tan excelente es nuestro producto?" — invalida los datos.

**Template:** `phases/03-design/deliverables/survey-results.md` *(pendiente)*

---

### 3A.1.6 User Insights

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.1 User Research |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Lista (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5-1 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere capacidad de síntesis: extraer los nuggets de conocimiento accionable de la masa de datos de research.  
En VTT: un agente puede compilar y organizar insights a partir del research report, categorizarlos por tema, y priorizarlos por impacto. Es bastante delegable. Necesita brief con: research report completo y categorías de organización deseadas.

**Qué es:** Lista destilada de los hallazgos clave de la investigación: afirmaciones concretas sobre los usuarios, respaldadas por evidencia, que informan decisiones de diseño. Cada insight es una "verdad" descubierta: "Los usuarios X hacen Y porque Z" — no opiniones ni especulaciones. Priorizados por impacto en el diseño.

**Para qué sirve:** El research report tiene 20 páginas. Los insights son la "cheat sheet" de 1 página que el equipo de diseño consulta diariamente. Son los puntos de referencia que guían cada decisión: "¿este diseño aborda el insight #3?". Son más consumibles y accionables que el reporte completo.

**Inputs requeridos:**
- `3A.1.2` User Research Report — fuente de insights

**Dependencias (predecessors):**
- `3A.1.2` User Research Report *(obligatorio)* — insights extraídos del reporte

**Habilita (successors):**
- `3A.2.1` Personas Document — insights informan personas
- `3A.3.1` Site Map — insights sobre mental models informan IA
- `3A.4.1` Wireframe Document — insights guían diseño de pantallas

**Audiencia:**
- **UX Designer** — referencia diaria durante diseño
- **UI Designer** — contexto de usuarios
- **Product Owner** — validación de comprensión del usuario
- **Todo el equipo** — "cheat sheet" de quién es el usuario

**Secciones esperadas:**
1. Lista de insights priorizados (5-15 insights clave)
2. Por cada insight: statement, evidencia que lo soporta, implicación para diseño
3. Categorización por tema (comportamiento, motivaciones, frustraciones, expectativas)
4. Priorización (impact: high/medium/low)

**Criterio de completitud:**
- [ ] Al menos 5 insights documentados
- [ ] Cada insight respaldado por evidencia (cita, dato, observación)
- [ ] Implicación para diseño explícita por insight
- [ ] Priorizados por impacto
- [ ] Lenguaje claro y accionable (no académico)

**Anti-patrones:**
- ❌ **Insights como opiniones:** "Creemos que los usuarios prefieren X" — un insight tiene evidencia, no es una creencia.
- ❌ **Insights vagos:** "Los usuarios quieren algo fácil de usar" — no es accionable, es una tautología.
- ❌ **Demasiados insights:** 50 insights — nadie los recuerda; priorizar a 10-15 máximo.
- ❌ **Insights sin implicación:** "Los usuarios usan el celular por la mañana" — ¿y qué hacemos con eso? Falta la implicación.

**Template:** `phases/03-design/deliverables/user-insights.md` *(pendiente)*

---

### 3A.1.7 Pain Points

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.1 User Research |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Lista (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere empatía para identificar y articular las frustraciones reales de los usuarios, diferenciando entre pain points validados por research y assumptions del equipo.  
En VTT: un agente puede compilar, categorizar y priorizar pain points a partir del research report y las transcripciones de entrevistas. Es altamente delegable. Necesita brief con: research report y criterios de priorización (frecuencia × severidad).

**Qué es:** Lista priorizada de los problemas, frustraciones y fricciones que los usuarios experimentan con las soluciones actuales (competidores, procesos manuales, herramientas existentes). Cada pain point es validado por research (no asumido), categorizado por severidad (blocker, major, minor), y cuantificado por frecuencia (cuántos usuarios lo mencionaron).

**Para qué sirve:** Los pain points son las "oportunidades de diseño". Cada pain point validado es un problema que el producto puede resolver. La priorización (frecuencia × severidad) indica qué resolver primero. Son el input directo para las Personas (3A.2) y para la definición de features del MVP.

**Inputs requeridos:**
- `3A.1.2` User Research Report — pain points identificados
- `3A.1.4` Interview Transcripts — evidencia específica
- `0.3.2` User Pain Points — hipótesis previas a comparar

**Dependencias (predecessors):**
- `3A.1.2` User Research Report *(obligatorio)* — fuente de pain points validados

**Habilita (successors):**
- `3A.2.1` Personas Document — pain points por persona
- `3A.2.8` Jobs to be Done — pain points informan JTBD
- `1.2.4` MVP Definition — features que resuelven top pain points

**Audiencia:**
- **UX Designer** — guía de qué problemas resolver en diseño
- **Product Owner** — priorización de features
- **Product Manager** — roadmap informado por dolor del usuario
- **Marketing** — messaging basado en problemas reales

**Secciones esperadas:**
1. Lista de pain points priorizados (tabla: #, pain point, severidad, frecuencia, evidencia)
2. Categorización (por flujo, por etapa del journey, por tipo: funcional/emocional/social)
3. Comparación con hipótesis previas (0.3.2) — ¿se confirmaron?
4. Pain points que el producto SÍ va a resolver (scope)
5. Pain points fuera de scope (diferidos o no abordables)

**Criterio de completitud:**
- [ ] Al menos 5 pain points validados por research
- [ ] Severidad asignada (blocker/major/minor)
- [ ] Frecuencia indicada (N de M participantes lo mencionaron)
- [ ] Evidencia por pain point (cita o dato)
- [ ] Priorización aplicada
- [ ] Comparación con hipótesis previas

**Anti-patrones:**
- ❌ **Pain points asumidos:** "Los usuarios odian X" sin haberlo investigado — es una hipótesis, no un hallazgo.
- ❌ **Sin priorización:** Lista de 20 pain points sin severidad ni frecuencia — todo parece igualmente importante.
- ❌ **Pain points del equipo, no del usuario:** "No me gusta cómo funciona el competidor" — eso es opinión interna, no del usuario.
- ❌ **Solo pain points funcionales:** Ignorar frustraciones emocionales y sociales — la experiencia es holística.

**Template:** `phases/03-design/deliverables/pain-points.md` *(pendiente)*

---

### 3A.1.8 User Needs

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.1 User Research |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Lista (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere capacidad de traducir lo que los usuarios dicen que quieren en lo que realmente necesitan (la necesidad subyacente detrás del pedido).  
En VTT: un agente puede compilar y categorizar user needs a partir del research report. Puede también mapearlos a features del producto. Es bastante delegable. Necesita brief con: research report, insights, y pain points para derivar necesidades.

**Qué es:** Lista de las necesidades reales de los usuarios identificadas a través de la investigación. Las necesidades son más profundas que los pedidos explícitos: el usuario dice "quiero un botón de exportar a Excel" — la necesidad real es "necesito compartir datos con mi jefe en un formato que él entienda". Las necesidades se categorizan en funcionales, emocionales, y sociales.

**Para qué sirve:** Las necesidades son el "por qué" detrás de las features. Diseñar para necesidades en lugar de pedidos explícitos produce mejores soluciones: el usuario pedía "exportar a Excel" pero quizás un link compartible resuelve mejor la necesidad subyacente. Las necesidades son input directo para JTBD y para la definición de features.

**Inputs requeridos:**
- `3A.1.2` User Research Report — necesidades extraídas
- `3A.1.6` User Insights — insights que revelan necesidades
- `3A.1.7` Pain Points — pain points cuyo reverso es una necesidad

**Dependencias (predecessors):**
- `3A.1.2` User Research Report *(obligatorio)*
- `3A.1.6` User Insights *(recomendado)*

**Habilita (successors):**
- `3A.2.8` Jobs to be Done — JTBD derivados de necesidades
- `3A.2.6` Scenarios — escenarios que satisfacen necesidades
- `2.4.1` Product Backlog — user stories que abordan necesidades

**Audiencia:**
- **UX Designer** — diseño orientado a necesidades
- **Product Owner** — feature definition basada en necesidades reales
- **Product Manager** — priorización

**Secciones esperadas:**
1. Lista de necesidades (tabla: #, necesidad, tipo, evidencia, prioridad)
2. Categorización (funcional, emocional, social)
3. Mapping necesidad → pedido explícito (lo que dicen vs lo que necesitan)
4. Mapping necesidad → feature propuesta
5. Necesidades no atendidas por soluciones actuales (oportunidad)

**Criterio de completitud:**
- [ ] Al menos 5 necesidades identificadas
- [ ] Necesidades diferenciadas de pedidos explícitos
- [ ] Categorización funcional/emocional/social
- [ ] Evidencia por necesidad
- [ ] Priorización aplicada

**Anti-patrones:**
- ❌ **Necesidades = features:** "El usuario necesita un dashboard" — eso es una solución, no una necesidad. La necesidad es "entender el estado de su negocio de un vistazo".
- ❌ **Solo necesidades funcionales:** Ignorar necesidades emocionales (seguridad, confianza) y sociales (impresionar al jefe, colaborar).
- ❌ **Necesidades del equipo disfrazadas:** "Los usuarios necesitan microservicios" — eso es una decisión técnica, no una necesidad de usuario.

**Template:** `phases/03-design/deliverables/user-needs.md` *(pendiente)*

---

### 3A.1.9 Behavioral Patterns

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.1 User Research |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Researcher / UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Report (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere capacidad de identificar patrones de comportamiento transversales a múltiples participantes: cómo toman decisiones, qué secuencia de acciones siguen, qué herramientas usan, cuándo y dónde usan el producto.  
En VTT: un agente puede analizar transcripciones y survey data para identificar patrones recurrentes de comportamiento. Es parcialmente delegable. Necesita brief con: transcripciones de entrevistas, observaciones de campo, y datos de analytics (si existen).

**Qué es:** Documento que identifica y documenta los patrones recurrentes de comportamiento de los usuarios: cómo realizan sus tareas actualmente (workflow actual), qué secuencia siguen, qué herramientas usan y cómo las combinan, cuándo y dónde interactúan con el dominio (contexto de uso), y cómo toman decisiones. Los patrones se identifican por repetición entre múltiples participantes.

**Para qué sirve:** Los patrones de comportamiento son el input más directo para el diseño de interacciones: si los usuarios siempre hacen A antes de B, el diseño debe facilitar esa secuencia, no forzar B antes de A. También informan la segmentación de personas: usuarios con patrones similares se agrupan en la misma persona.

**Inputs requeridos:**
- `3A.1.4` Interview Transcripts — comportamientos observados
- `3A.1.2` User Research Report — análisis de comportamiento
- Analytics de producto existente (si hay producto previo)
- Datos de contextual inquiry (si se realizó)

**Dependencias (predecessors):**
- `3A.1.2` User Research Report *(obligatorio)*
- `3A.1.4` Interview Transcripts *(obligatorio)*

**Habilita (successors):**
- `3A.2.1` Personas Document — personas basadas en patrones de comportamiento
- `3A.2.6` Scenarios — escenarios basados en comportamiento real
- `3A.3.2` Navigation Structure — navegación alineada a patrones
- `3A.4.8` Wireframe Flows — flujos basados en comportamiento real

**Audiencia:**
- **UX Designer** — diseño de interacciones basado en comportamiento real
- **UI Designer** — contexto de cómo se usa el producto
- **Product Manager** — priorización basada en frecuencia de comportamiento
- **Design Lead** — validación de comprensión del usuario

**Secciones esperadas:**
1. Patrones de workflow (cómo los usuarios realizan sus tareas principales)
2. Patrones de decisión (cómo eligen entre opciones, qué información buscan)
3. Patrones de herramientas (qué tools usan, cómo las combinan, switching patterns)
4. Patrones temporales (cuándo usan el producto: hora, día, frecuencia)
5. Patrones contextuales (dónde: oficina, mobile, remoto; con quién)
6. Patrones de colaboración (cómo comparten información, con quién)
7. Segmentación por comportamiento (clusters de usuarios con patrones similares)
8. Implicaciones para diseño (tabla: patrón → implicación)

**Criterio de completitud:**
- [ ] Al menos 3 categorías de patrones documentadas
- [ ] Patrones identificados por repetición (mínimo 3 de 5 participantes)
- [ ] Evidencia por patrón (fuente: entrevista, analytics, observación)
- [ ] Implicaciones para diseño documentadas
- [ ] Segmentación de comportamiento que informa personas

**Anti-patrones:**
- ❌ **Comportamiento de un participante como "patrón":** Un usuario que hace algo ≠ un patrón — necesita repetición entre participantes.
- ❌ **Patrones asumidos sin observación:** "Los millennials usan mobile" — estereotipo, no patrón observado.
- ❌ **Solo patrones del producto:** Patrones de uso del competidor sin investigar el comportamiento fuera del producto — pierde contexto.
- ❌ **Patrones sin implicación:** Documentar comportamiento sin decir cómo afecta al diseño — datos sin acción.

**Template:** `phases/03-design/deliverables/behavioral-patterns.md` *(pendiente)*

---

## Tabla resumen de ejecutores — Fase 3A.1 User Research

| Deliverable | Responsable | Ejecuta | Delegable VTT |
|-------------|-------------|---------|---------------|
| 3A.1.1 User Research Plan | UX Designer | UX Researcher / UX Designer | 🔶 Parcial — puede generar estructura, no puede elegir metodología óptima |
| 3A.1.2 User Research Report | UX Designer | UX Researcher / UX Designer | 🔶 Parcial — puede estructurar y analizar datos, no puede observar sesiones |
| 3A.1.3 Interview Guide | UX Designer | UX Researcher / UX Designer | ✅ — puede generar guía completa a partir del research plan |
| 3A.1.4 Interview Transcripts | UX Designer | Transcription service | ✅ — puede limpiar, formatear y anonimizar transcripciones |
| 3A.1.5 Survey Results | UX Designer | UX Researcher / UX Designer | ✅ — puede analizar datos, generar gráficos y redactar insights |
| 3A.1.6 User Insights | UX Designer | UX Designer | ✅ — puede compilar y priorizar insights del research report |
| 3A.1.7 Pain Points | UX Designer | UX Designer | ✅ — puede compilar, categorizar y priorizar pain points |
| 3A.1.8 User Needs | UX Designer | UX Designer | 🔶 Parcial — puede compilar, pero diferenciar pedido vs necesidad requiere juicio |
| 3A.1.9 Behavioral Patterns | UX Designer | UX Researcher / UX Designer | 🔶 Parcial — puede analizar transcripciones, pero identificar patrones requiere experiencia |

---

## Siguiente archivo

**Próximo:** `DICCIONARIO_FASE_03A_02_PERSONAS.md` — 8 deliverables (3A.2.1 a 3A.2.8)
