# DICCIONARIO DE DELIVERABLES — FASE 3A.8: USABILITY TESTING

**Versión:** 1.0  
**Fecha:** 2026-05-14  
**Fase:** 3A — Design UX/UI  
**Subfase:** 3A.8 — Usability Testing  
**Total deliverables:** 7  
**Responsable de subfase:** UX Designer  
**Aprueba:** Design Lead

---

## Contexto de la subfase

Usability Testing es la validación empírica de los diseños con usuarios reales (o representativos). No se trata de preguntar "¿te gusta?" sino de observar si el usuario puede completar tareas clave sin fricción. Es la última oportunidad de detectar problemas de UX antes de invertir en desarrollo. Cada bug de usabilidad encontrado aquí cuesta 10x menos de arreglar que si se descubre post-desarrollo.

**Prerequisitos de subfase:**
- Prototipo interactivo (3A.6.1) funcional y navegable
- Personas definidas (3A.2) para reclutar participantes representativos
- Flujos principales identificados (2.6)

**Entrega de subfase:**
- Diseños validados con usuarios, iterados según hallazgos, y aprobados para handoff

---

### 3A.8.1 Usability Test Plan

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.8 Usability Testing |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Researcher / UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Documento (MD/PDF) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Una vez por ronda de testing |

**Perfil de ejecución:** Requiere experiencia en metodologías de usability testing (moderated vs unmoderated, remote vs presencial, think-aloud, task-based). Debe saber diseñar estudios válidos con métricas medibles.  
En VTT: un agente puede generar la estructura del test plan a partir de: objetivos de negocio, flujos a testear, y personas definidas. Puede redactar objetivos, métricas propuestas, y timeline. NO puede decidir la metodología óptima ni el número de participantes sin juicio del UX Researcher. Necesita brief con: qué flujos testear, qué preguntas de investigación responder, budget/timeline disponible, y si es remoto o presencial.

**Qué es:** Documento que define el plan completo de pruebas de usabilidad: objetivos del estudio, preguntas de investigación, metodología, métricas a recoger, perfil de participantes, número de sesiones, duración, herramientas, timeline, y roles del equipo de testing. Es el "proyecto" del estudio antes de ejecutarlo.

**Para qué sirve:** Sin plan, el testing se convierte en "le enseño el prototipo a alguien y le pregunto qué opina" — lo cual no es usability testing. El plan asegura que el estudio sea riguroso, replicable, y que responda preguntas específicas de UX. También permite al Design Lead validar la inversión de tiempo antes de ejecutar.

**Inputs requeridos:**
- `3A.6.1` Interactive Prototype — lo que se va a testear
- `3A.2.1` Personas Document — perfil de usuarios a reclutar
- `2.6.1` User Flow Diagrams — flujos que se van a testear
- `2.6.2` Happy Path Flows — flujos principales como base de tareas
- Preguntas de investigación del Product Owner / Product Manager

**Dependencias (predecessors):**
- `3A.6.1` Interactive Prototype *(obligatorio)* — sin prototipo no hay qué testear
- `3A.2.1` Personas Document *(obligatorio)* — criterios de reclutamiento
- `2.6.1` User Flow Diagrams *(obligatorio)* — flujos a evaluar
- `2.6.2` Happy Path Flows *(recomendado)* — base para definir tareas

**Habilita (successors):**
- `3A.8.2` Test Script — guión basado en el plan
- `3A.8.3` Participant Criteria — criterios derivados del plan
- `3A.8.4` Test Results — resultados del estudio planificado

**Audiencia:**
- **UX Designer** — ejecutor del plan
- **Design Lead** — aprobación de metodología e inversión de tiempo
- **Product Owner** — validación de que se testean los flujos correctos
- **Product Manager** — alineación con prioridades de producto

**Secciones esperadas:**
1. Objetivos del estudio (qué queremos aprender)
2. Preguntas de investigación (3-5 preguntas específicas)
3. Metodología (moderated/unmoderated, remote/presencial, think-aloud)
4. Métricas a recoger (task success rate, time on task, error rate, SUS score)
5. Perfil de participantes (criterios de inclusión/exclusión)
6. Número de participantes y justificación
7. Tareas a evaluar (lista con descripción y flujo esperado)
8. Herramientas (Maze, Lookback, UserTesting, Zoom, etc.)
9. Timeline (reclutamiento, sesiones, análisis, reporte)
10. Roles del equipo (moderador, observador, note-taker)
11. Riesgos y mitigaciones del estudio

**Criterio de completitud:**
- [ ] Objetivos del estudio claros y alineados con preguntas de negocio
- [ ] Metodología definida y justificada
- [ ] Al menos 3 métricas cuantificables definidas
- [ ] Perfil de participantes con criterios de inclusión/exclusión
- [ ] Al menos 5 tareas de testing definidas con descripción
- [ ] Timeline con fechas de inicio y fin
- [ ] Herramientas de testing seleccionadas
- [ ] Plan aprobado por Design Lead

**Anti-patrones:**
- ❌ **Testing sin plan:** "Vamos a enseñarle el prototipo a 3 personas y ver qué pasa" — no es un estudio, es una demo informal.
- ❌ **Preguntas de opinión en vez de tareas:** "¿Te gusta este diseño?" no es usability testing — las tareas deben ser accionables ("Registra una cuenta nueva").
- ❌ **Un solo participante:** Los hallazgos de 1 persona no son generalizables — mínimo 5 participantes por perfil (Nielsen).
- ❌ **Sin métricas definidas:** Si no defines qué mides antes, cualquier resultado "confirma" el diseño — sesgo de confirmación.

**Template:** `phases/03-design/deliverables/usability-test-plan.md` *(pendiente)*

---

### 3A.8.2 Test Script

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.8 Usability Testing |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Researcher / UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Documento (MD/PDF) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez por ronda de testing |

**Perfil de ejecución:** Requiere experiencia en moderación de sesiones de usability testing. Debe saber formular tareas sin sesgo (sin dar pistas), escribir preguntas follow-up neutrales, y estructurar la sesión para que fluya naturalmente.  
En VTT: un agente puede generar un borrador del test script a partir del test plan: intro, consent, warm-up questions, task descriptions, post-task questions, y debrief. Es bastante delegable si el plan está bien definido. NO puede juzgar si las tareas están formuladas sin sesgo ni ajustar el tono para diferentes tipos de participantes. Necesita brief con: test plan completo, prototipo URL, y contexto del moderador.

**Qué es:** Guión detallado que sigue el moderador durante cada sesión de usability testing. Incluye: script de introducción (explicar el estudio, consent), preguntas de warm-up, las tareas a realizar (con redacción exacta sin sesgos), preguntas post-tarea (difficulty rating, follow-up), y preguntas de cierre/debrief. Asegura que todas las sesiones sean consistentes.

**Para qué sirve:** Garantiza que cada sesión se ejecute de forma idéntica, haciendo los resultados comparables entre participantes. Sin script, cada sesión es diferente: el moderador da pistas en una, omite una tarea en otra, formula las preguntas de forma distinta. El script es la estandarización del estudio.

**Inputs requeridos:**
- `3A.8.1` Usability Test Plan — objetivos, tareas y metodología
- `3A.6.1` Interactive Prototype — prototipo que se va a testear
- `3A.6.5` Prototype Links — URLs compartibles del prototipo

**Dependencias (predecessors):**
- `3A.8.1` Usability Test Plan *(obligatorio)* — tareas y metodología definen el script
- `3A.6.1` Interactive Prototype *(obligatorio)* — el script referencia pantallas del prototipo
- `3A.6.5` Prototype Links *(obligatorio)* — links para que el participante acceda

**Habilita (successors):**
- `3A.8.4` Test Results — el script se ejecuta para producir resultados
- `3A.8.5` Findings & Recommendations — hallazgos derivados de la ejecución del script

**Audiencia:**
- **UX Designer / Moderador** — guión a seguir durante cada sesión
- **Observadores** — saben qué esperar en cada momento de la sesión
- **Design Lead** — revisión de que las tareas son neutrales y relevantes

**Secciones esperadas:**
1. Script de introducción (presentación, explicar el estudio, setting expectations)
2. Consentimiento informado (grabación, privacidad, derecho a retirarse)
3. Preguntas de warm-up (background, experiencia previa con productos similares)
4. Tareas con redacción exacta (scenario + task, sin pistas sobre la solución)
5. Post-task questions por tarea (SEQ — Single Ease Question, follow-up abierto)
6. Cuestionario post-estudio (SUS, NPS, o similar)
7. Preguntas de debrief / cierre
8. Notas para el moderador (qué hacer si el participante se atasca, cuándo intervenir)
9. Checklist de sesión (setup, grabación, agradecimiento, incentivo)

**Criterio de completitud:**
- [ ] Intro con consent y expectativas documentada
- [ ] Todas las tareas del test plan incluidas con redacción neutral
- [ ] Post-task questions definidas para cada tarea
- [ ] Cuestionario post-estudio incluido (SUS o equivalente)
- [ ] Notas para el moderador sobre manejo de situaciones difíciles
- [ ] Duración estimada por sección (total ≈ 45-60 min)
- [ ] Script revisado por al menos una persona que no lo escribió

**Anti-patrones:**
- ❌ **Tareas con pistas:** "Haz click en el botón azul de arriba a la derecha para registrarte" — eso NO es una tarea, es una instrucción.
- ❌ **Preguntas sesgadas:** "¿No crees que este diseño es fácil de usar?" — leading question que invalida el dato.
- ❌ **Sin scenario context:** "Registra una cuenta" vs "Imagina que un amigo te recomendó esta app y quieres probarla. ¿Cómo empezarías?" — el contexto cambia el comportamiento.
- ❌ **Script rígido sin flexibility:** No tener indicaciones de cuándo improvisar follow-ups — se pierden insights valiosos.

**Template:** `phases/03-design/deliverables/usability-test-script.md` *(pendiente)*

---

### 3A.8.3 Participant Criteria

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.8 Usability Testing |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Researcher / UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Documento (MD/PDF) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 días |
| **Frecuencia** | Una vez por ronda de testing |

**Perfil de ejecución:** Requiere entender la diferencia entre segmentación de mercado y criterios de reclutamiento para usability testing. Debe poder traducir personas en screener questions accionables.  
En VTT: un agente puede generar los criterios de participantes y un screener questionnaire a partir de las personas definidas. Es altamente delegable. NO puede decidir cuántos participantes por segmento ni hacer trade-offs entre representatividad y budget. Necesita brief con: personas del proyecto, número de participantes target, budget para incentivos, y canal de reclutamiento (interno, panel, guerrilla).

**Qué es:** Documento que define quién debe participar en las pruebas de usabilidad: criterios de inclusión (demographics, experiencia técnica, relación con el dominio), criterios de exclusión (empleados, UX professionals, usuarios del producto anterior), número de participantes por segmento, y screener questionnaire para filtrar candidatos.

**Para qué sirve:** Si reclutas a las personas equivocadas, los resultados no representan a tu audiencia real. Un test con 5 developers no valida la usabilidad para usuarios no-técnicos. Los criterios aseguran que los participantes son representativos de las personas del producto.

**Inputs requeridos:**
- `3A.8.1` Usability Test Plan — contexto del estudio
- `3A.2.1` Personas Document — perfiles de usuario a representar
- `3A.2.3` Primary Persona — foco principal de reclutamiento
- `3A.2.4` Secondary Personas — segmentos adicionales

**Dependencias (predecessors):**
- `3A.8.1` Usability Test Plan *(obligatorio)* — número de participantes y segmentos
- `3A.2.1` Personas Document *(obligatorio)* — base para criterios demográficos
- `3A.2.3` Primary Persona *(obligatorio)* — perfil prioritario

**Habilita (successors):**
- `3A.8.4` Test Results — participantes reclutados según criterios producen resultados válidos

**Audiencia:**
- **UX Designer** — referencia para reclutamiento
- **Recruiter / Panel provider** — criterios para filtrar candidatos
- **Design Lead** — validación de representatividad

**Secciones esperadas:**
1. Resumen de perfiles buscados (alineado a personas)
2. Criterios de inclusión (demographics, experiencia, comportamiento)
3. Criterios de exclusión (conflictos de interés, expertise)
4. Distribución por segmento (cuántos de cada perfil)
5. Screener questionnaire (preguntas de filtro)
6. Incentivo definido (monto, forma de pago)
7. Canal de reclutamiento (panel, redes sociales, base de datos interna)
8. Timeline de reclutamiento

**Criterio de completitud:**
- [ ] Criterios de inclusión documentados y alineados a personas
- [ ] Criterios de exclusión explícitos
- [ ] Screener questionnaire con preguntas de filtro
- [ ] Número de participantes por segmento definido (mínimo 5 total)
- [ ] Incentivo definido
- [ ] Canal de reclutamiento identificado

**Anti-patrones:**
- ❌ **Reclutar convenience sample:** Testear con compañeros de oficina o amigos — no representan a la audiencia real.
- ❌ **Sin exclusiones:** No excluir UX professionals o empleados — sus respuestas están contaminadas por expertise.
- ❌ **Un solo segmento:** Solo testear con el perfil "más fácil" de reclutar — ignora segmentos clave.
- ❌ **Screener demasiado largo:** 25 preguntas de screener — los candidatos abandonan antes de terminar.

**Template:** `phases/03-design/deliverables/participant-criteria.md` *(pendiente)*

---

### 3A.8.4 Test Results

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.8 Usability Testing |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Researcher / UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Report (MD/PDF) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 2-3 días |
| **Frecuencia** | Una vez por ronda de testing |

**Perfil de ejecución:** Requiere capacidad analítica para sintetizar observaciones cualitativas y datos cuantitativos. Debe saber diferenciar entre hallazgos individuales y patrones, y evitar sobreinterpretar datos de muestras pequeñas.  
En VTT: un agente puede estructurar el reporte de resultados, calcular métricas cuantitativas (task success rate, promedio SUS), y organizar observaciones por tarea/theme. NO puede observar sesiones ni interpretar comportamiento no-verbal. Necesita brief con: notas de sesión raw, scores post-task, resultados del cuestionario SUS, y grabaciones transcritas (si disponibles).

**Qué es:** Reporte factual con los datos recopilados durante las sesiones de testing. Incluye: métricas cuantitativas por tarea (success rate, time on task, error count, difficulty ratings), observaciones cualitativas (dónde se atascaron, qué confundió, qué verbalizaron), scores del cuestionario (SUS, NPS), y datos demográficos de participantes. Es el "qué pasó" sin interpretación.

**Para qué sirve:** Documenta objetivamente lo que ocurrió en las sesiones. Separa los hechos de las interpretaciones (que van en Findings & Recommendations). Permite que otros stakeholders vean los datos raw y saquen sus propias conclusiones. Sirve como evidencia para justificar cambios de diseño ante stakeholders resistentes.

**Inputs requeridos:**
- `3A.8.1` Usability Test Plan — métricas definidas
- `3A.8.2` Test Script — tareas ejecutadas
- Notas de sesiones de testing
- Grabaciones de sesiones (si aplica)
- Scores de cuestionarios (SUS, SEQ, post-task)

**Dependencias (predecessors):**
- `3A.8.1` Usability Test Plan *(obligatorio)* — define qué se mide
- `3A.8.2` Test Script *(obligatorio)* — se ejecutó para producir datos
- `3A.8.3` Participant Criteria *(obligatorio)* — participantes reclutados según criterios

**Habilita (successors):**
- `3A.8.5` Findings & Recommendations — interpretación de los resultados
- `3A.8.6` Iteration Log — iteraciones basadas en resultados

**Audiencia:**
- **UX Designer** — datos para análisis e iteración
- **Design Lead** — visibilidad de resultados del estudio
- **Product Owner** — evidencia de problemas de usabilidad
- **Product Manager** — datos para priorización de fixes

**Secciones esperadas:**
1. Resumen ejecutivo (número de sesiones, participantes, fechas)
2. Perfil de participantes (demographics table, anonimizada)
3. Resultados por tarea (tabla: tarea, success rate, avg time, error count, avg difficulty)
4. Observaciones por tarea (observaciones cualitativas agrupadas)
5. Métricas globales (SUS score, NPS, task completion rate global)
6. Citas textuales relevantes de participantes (anonimizadas)
7. Heatmaps / click maps (si la herramienta lo produce)
8. Tabla de issues detectados (issue, severidad, frecuencia, tarea afectada)
9. Datos raw en anexo (si aplica)

**Criterio de completitud:**
- [ ] Todas las tareas del test plan tienen resultados documentados
- [ ] Métricas cuantitativas calculadas (success rate, time, errors, SUS)
- [ ] Observaciones cualitativas documentadas por tarea
- [ ] Al menos 5 participantes con datos completos
- [ ] Issues detectados listados con severidad
- [ ] Datos de participantes anonimizados
- [ ] Reporte distingue hechos de interpretaciones

**Anti-patrones:**
- ❌ **Mezclar datos con recomendaciones:** El reporte de resultados debe ser factual — las interpretaciones van en 3A.8.5 Findings.
- ❌ **Cherry-picking datos:** Reportar solo los datos que confirman que el diseño "funciona" — omitir problemas es peor que no testear.
- ❌ **Sin métricas cuantitativas:** Solo observaciones cualitativas sin numbers — pierde poder de persuasión ante stakeholders.
- ❌ **Datos no anonimizados:** Incluir nombres de participantes — violación de privacidad y consent.

**Template:** `phases/03-design/deliverables/usability-test-results.md` *(pendiente)*

---

### 3A.8.5 Findings & Recommendations

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.8 Usability Testing |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Researcher / UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Report (MD/PDF) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 2-3 días |
| **Frecuencia** | Una vez por ronda de testing |

**Perfil de ejecución:** Requiere capacidad de síntesis, pensamiento de diseño, y habilidad de traducir problemas observados en soluciones accionables. Debe poder priorizar hallazgos por impacto y esfuerzo.  
En VTT: un agente puede agrupar issues por themes, categorizar por severidad (crítico/mayor/menor/cosmético), y proponer priorización basada en frecuencia × severidad. Puede sugerir soluciones de diseño genéricas basadas en UX best practices. NO puede proponer soluciones de diseño contextualizadas al producto sin juicio del UX Designer. Necesita brief con: test results completos, contexto del producto, y restricciones técnicas conocidas.

**Qué es:** Análisis interpretativo de los resultados del testing. Agrupa los issues detectados en temas (themes), clasifica por severidad (crítico, mayor, menor, cosmético), identifica patrones transversales, y propone recomendaciones accionables con prioridad. Es el "qué significa" y "qué hacemos" derivado de los datos.

**Para qué sirve:** Los datos raw (3A.8.4) son hechos; este documento los convierte en acciones. Le dice al equipo: "estos son los 3 problemas más graves, así recomendamos arreglarlos, y esta es la prioridad". Es el input directo para las iteraciones de diseño. También sirve como herramienta de comunicación con stakeholders para justificar cambios.

**Inputs requeridos:**
- `3A.8.4` Test Results — datos factuales del estudio
- `3A.8.1` Usability Test Plan — preguntas de investigación originales
- Conocimiento de UX best practices para proponer soluciones

**Dependencias (predecessors):**
- `3A.8.4` Test Results *(obligatorio)* — datos que se interpretan
- `3A.8.1` Usability Test Plan *(recomendado)* — contexto de las preguntas de investigación

**Habilita (successors):**
- `3A.8.6` Iteration Log — iteraciones basadas en recomendaciones
- `3A.8.7` Final Validation — validación post-iteración
- `3A.5.1` UI Mockups Complete — mockups actualizados según recomendaciones
- `3A.6.1` Interactive Prototype — prototipo actualizado

**Audiencia:**
- **UX Designer** — guía para iterar los diseños
- **UI Designer** — cambios visuales recomendados
- **Design Lead** — decisiones de priorización
- **Product Owner** — entender qué problemas tiene el producto
- **Product Manager** — priorización de fixes en el backlog

**Secciones esperadas:**
1. Resumen ejecutivo (3-5 hallazgos principales en 1 párrafo)
2. Respuesta a preguntas de investigación (del test plan)
3. Hallazgos agrupados por tema (cada hallazgo: descripción, evidencia, severidad)
4. Clasificación de severidad (tabla: critical, major, minor, cosmetic con definiciones)
5. Recomendaciones accionables (por hallazgo: qué cambiar, cómo, prioridad)
6. Matriz de priorización (impacto vs esfuerzo)
7. Quick wins (cambios de alto impacto y bajo esfuerzo)
8. Hallazgos positivos (qué funcionó bien — no solo problemas)
9. Próximos pasos (qué iterar, si se necesita otra ronda de testing)

**Criterio de completitud:**
- [ ] Todos los issues del test results interpretados y agrupados
- [ ] Severidad asignada a cada hallazgo (critical/major/minor/cosmetic)
- [ ] Recomendación accionable por cada hallazgo
- [ ] Matriz de priorización incluida
- [ ] Quick wins identificados
- [ ] Hallazgos positivos documentados (no solo problemas)
- [ ] Preguntas de investigación del plan respondidas
- [ ] Próximos pasos definidos

**Anti-patrones:**
- ❌ **Solo problemas, nunca lo positivo:** Reportar únicamente lo malo desmoraliza al equipo y pierde la oportunidad de reforzar lo que funciona.
- ❌ **Recomendaciones vagas:** "Mejorar la navegación" no es accionable — "Agregar breadcrumbs en la sección de settings" sí lo es.
- ❌ **Sin priorización:** Lista de 30 issues sin prioridad — el equipo no sabe por dónde empezar.
- ❌ **Confundir opinión con hallazgo:** "A mí no me gusta el color del botón" no es un hallazgo — "3 de 5 participantes no vieron el CTA" sí lo es.

**Template:** `phases/03-design/deliverables/usability-findings-recommendations.md` *(pendiente)*

---

### 3A.8.6 Iteration Log

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.8 Usability Testing |
| **Responsable** | UX Designer |
| **Ejecuta** | UI Designer / UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Documento (MD/Tabla) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días (paralelo a iteraciones) |
| **Frecuencia** | Continua durante iteraciones |

**Perfil de ejecución:** Requiere disciplina de documentación. Cada iteración de diseño debe registrarse con el hallazgo que la motivó, qué se cambió, y si se validó.  
En VTT: un agente puede mantener el log actualizado recibiendo inputs del UX/UI Designer sobre cada cambio realizado. Puede generar la tabla de tracking y hacer cross-reference con los hallazgos originales. Es altamente delegable como tarea de documentación. Necesita brief con: lista de hallazgos del 3A.8.5, y updates del diseñador sobre cada cambio realizado.

**Qué es:** Registro cronológico de todas las iteraciones de diseño realizadas como resultado del usability testing. Para cada iteración: qué hallazgo la motivó (referencia a 3A.8.5), qué se cambió (antes/después), quién lo cambió, cuándo, y si el cambio fue validado (en una ronda subsecuente de testing o por el Design Lead).

**Para qué sirve:** Crea trazabilidad entre hallazgo → cambio → validación. Sin este log, después de 10 iteraciones nadie recuerda por qué se cambió algo, si realmente respondía a un hallazgo, o si el cambio fue validado. Es la "cadena de custodia" de las decisiones de diseño basadas en evidencia.

**Inputs requeridos:**
- `3A.8.5` Findings & Recommendations — hallazgos que motivan iteraciones
- Screenshots/diffs de diseños antes y después de cada cambio
- Decisiones del Design Lead sobre qué iterar

**Dependencias (predecessors):**
- `3A.8.5` Findings & Recommendations *(obligatorio)* — hallazgos que disparan las iteraciones
- `3A.5.1` UI Mockups Complete *(obligatorio)* — diseños que se iteran

**Habilita (successors):**
- `3A.8.7` Final Validation — registro de iteraciones previo a validación final
- `3A.9.1` Handoff Document — historial de decisiones de diseño para contexto del developer

**Audiencia:**
- **UX Designer** — tracking de su propio trabajo de iteración
- **UI Designer** — referencia de qué cambios implementar
- **Design Lead** — supervisión de que los hallazgos se abordan
- **Product Manager** — visibilidad del progreso de iteración

**Secciones esperadas:**
1. Tabla de iteraciones (columnas: #, fecha, hallazgo ref, componente/pantalla afectada, descripción del cambio, responsable, estado de validación)
2. Capturas antes/después por iteración significativa
3. Decisiones de "no cambiar" documentadas (hallazgos descartados y justificación)
4. Resumen de iteraciones por ronda
5. Status de cada hallazgo (resuelto, en progreso, descartado, diferido)

**Criterio de completitud:**
- [ ] Cada hallazgo de 3A.8.5 tiene un status (resuelto/descartado/diferido)
- [ ] Cada iteración registrada con fecha, hallazgo ref, y descripción del cambio
- [ ] Decisiones de "no cambiar" justificadas
- [ ] Capturas antes/después para cambios significativos
- [ ] Log actualizado al momento de la validación final

**Anti-patrones:**
- ❌ **Iterar sin registrar:** Hacer cambios sin documentar qué motivó el cambio — pierde trazabilidad.
- ❌ **Solo registrar lo resuelto:** No documentar hallazgos diferidos o descartados — se pierde el por qué de decisiones de diseño.
- ❌ **Sin antes/después:** Registrar "cambié el formulario de registro" sin mostrar qué cambió — inútil para referencia futura.
- ❌ **Actualizar al final:** Llenar el log después de hacer todas las iteraciones de memoria — impreciso e incompleto.

**Template:** `phases/03-design/deliverables/iteration-log.md` *(pendiente)*

---

### 3A.8.7 Final Validation

| Campo | Valor |
|-------|-------|
| **Fase** | 3A-Design UX/UI |
| **Subfase** | 3A.8 Usability Testing |
| **Responsable** | UX Designer |
| **Ejecuta** | UX Designer |
| **Aprueba** | Design Lead |
| **Formato** | Sign-off (MD/PDF) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5-1 día |
| **Frecuencia** | Una vez (gate de salida de subfase) |

**Perfil de ejecución:** Requiere autoridad para declarar que los diseños están "listos para desarrollo". Debe poder evaluar si los hallazgos críticos fueron resueltos y si la calidad UX es suficiente para pasar a handoff.  
En VTT: un agente puede generar el documento de validación compilando: status de hallazgos, métricas de rondas de testing, y checklist de criterios. NO puede tomar la decisión de go/no-go — esa es del Design Lead. Necesita brief con: iteration log actualizado, métricas de la ronda final de testing (si hubo), y criterios de aceptación del Design Lead.

**Qué es:** Documento formal de sign-off que confirma que los diseños han sido validados con usuarios, los hallazgos críticos han sido resueltos (o diferidos con justificación), y los diseños están aprobados para pasar a handoff y desarrollo. Incluye el checklist de criterios de validación, las firmas de aprobación, y cualquier caveat o hallazgo diferido.

**Para qué sirve:** Es el gate de salida de la subfase de usability testing y, por extensión, de toda la fase de diseño UX/UI. Sin este sign-off, los diseños no deberían entrar a handoff (3A.9). Protege contra el riesgo de desarrollar diseños no validados que requerirán retrabajo costoso.

**Inputs requeridos:**
- `3A.8.5` Findings & Recommendations — hallazgos y su resolución
- `3A.8.6` Iteration Log — registro de iteraciones completadas
- `3A.8.4` Test Results — métricas finales
- Diseños iterados (mockups y prototipo actualizados)

**Dependencias (predecessors):**
- `3A.8.4` Test Results *(obligatorio)* — evidencia del testing
- `3A.8.5` Findings & Recommendations *(obligatorio)* — hallazgos resueltos
- `3A.8.6` Iteration Log *(obligatorio)* — iteraciones completadas

**Habilita (successors):**
- `3A.9.1` Handoff Document — gate de entrada a design handoff
- `3A.9.2` Specs Export — diseños validados listos para exportar specs
- `3A.9.3` Asset Export — assets de diseños validados

**Audiencia:**
- **Design Lead** — firma de aprobación
- **Product Owner** — confirmación de que el diseño cumple expectativas
- **Tech Lead** — señal de que puede iniciar handoff y planning técnico
- **Product Manager** — milestone de proyecto completado

**Secciones esperadas:**
1. Resumen del proceso de validación (rondas de testing, participantes, fechas)
2. Métricas finales (SUS score, task success rate global, improvement vs primera ronda)
3. Status de hallazgos críticos (todos resueltos o diferidos con justificación)
4. Status de hallazgos mayores (resueltos, diferidos, o aceptados)
5. Hallazgos diferidos con justificación y plan de abordaje futuro
6. Checklist de validación final
7. Declaración de aprobación
8. Firmas: UX Designer, Design Lead, Product Owner
9. Condiciones o caveats (si aplica)

**Criterio de completitud:**
- [ ] Todos los hallazgos críticos resueltos o diferidos con justificación escrita
- [ ] SUS score ≥ 68 (above average) o mejora documentada vs ronda anterior
- [ ] Task success rate ≥ 80% en flujos principales
- [ ] Checklist de validación completado
- [ ] Firma de Design Lead obtenida
- [ ] Firma de Product Owner obtenida
- [ ] Hallazgos diferidos documentados con plan futuro
- [ ] Diseños actualizados (mockups + prototipo reflejan iteraciones)

**Anti-patrones:**
- ❌ **Sign-off sin testing:** Aprobar diseños porque "se ven bien" sin haberlos testeado — teatro de UX.
- ❌ **Ignorar hallazgos críticos:** Sign-off con hallazgos críticos sin resolver ni diferir formalmente — deuda de UX oculta.
- ❌ **Sign-off sin métricas:** "Los usuarios dijeron que les gustó" sin datos cuantificables — no es evidencia.
- ❌ **Diferir todo:** Marcar todos los hallazgos como "diferidos" para avanzar — acumula deuda que se paga en desarrollo.

**Template:** `phases/03-design/deliverables/final-validation-signoff.md` *(pendiente)*

---

## Tabla resumen de ejecutores — Fase 3A.8 Usability Testing

| Deliverable | Responsable | Ejecuta | Delegable VTT |
|-------------|-------------|---------|---------------|
| 3A.8.1 Usability Test Plan | UX Designer | UX Researcher / UX Designer | 🔶 Parcial — puede generar estructura y métricas, no puede elegir metodología óptima |
| 3A.8.2 Test Script | UX Designer | UX Researcher / UX Designer | ✅ — puede generar borrador completo del script a partir del test plan |
| 3A.8.3 Participant Criteria | UX Designer | UX Researcher / UX Designer | ✅ — puede generar criterios y screener a partir de personas |
| 3A.8.4 Test Results | UX Designer | UX Researcher / UX Designer | 🔶 Parcial — puede estructurar reporte y calcular métricas, no puede observar sesiones |
| 3A.8.5 Findings & Recommendations | UX Designer | UX Researcher / UX Designer | 🔶 Parcial — puede agrupar y priorizar, no puede proponer soluciones UX contextualizadas |
| 3A.8.6 Iteration Log | UX Designer | UI Designer / UX Designer | ✅ — puede mantener log actualizado recibiendo inputs del diseñador |
| 3A.8.7 Final Validation | UX Designer | UX Designer | ❌ — decisión de go/no-go requiere juicio humano del Design Lead |

---

## Siguiente archivo

**Próximo:** `DICCIONARIO_FASE_03A_09_DESIGN_HANDOFF.md` — 5 deliverables (3A.9.1 a 3A.9.5)
