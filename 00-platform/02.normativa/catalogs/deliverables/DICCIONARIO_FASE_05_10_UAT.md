# DICCIONARIO DE DELIVERABLES — FASE 5.10: UAT (USER ACCEPTANCE TESTING)

**Versión:** 1.1  
**Fecha:** 2026-05-14  
**Fase:** 5 — Testing  
**Subfase:** 5.10 — UAT  
**Total deliverables:** 5  
**Responsable de subfase:** Product Owner  
**Aprueba:** Product Owner

---

### 5.10.1 UAT Plan

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.10 UAT |
| **Responsable** | Product Owner |
| **Ejecuta** | Product Owner / Business Users |
| **Aprueba** | Product Owner |
| **Formato** | Documento |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Pre-release |

**Perfil de ejecución:** Requiere definir qué usuarios de negocio testean, qué flujos, criterios de aceptación, y logistics.  
En VTT: un agente puede generar el plan de UAT completo desde use cases y acceptance criteria. Es bastante delegable.

**Qué es:** Plan de User Acceptance Testing: quién testea (business users, stakeholders — NO developers ni QA), qué testean (flujos de negocio principales desde perspectiva de usuario, en lenguaje no-técnico), criterios de aceptación por flujo, timeline (cuántos días de UAT, cuándo empieza/termina), y logistics (ambiente de UAT, acceso, credenciales, soporte disponible durante UAT, cómo reportar issues).

**Para qué sirve:** QA verifica que funciona técnicamente. UAT verifica que funciona para el negocio: "¿este sistema resuelve mi problema?", "¿puedo hacer mi trabajo diario con esto?". Es la última validación humana antes de producción.

**Inputs requeridos:**
- `2.3.4` Detailed Use Cases — flujos a validar
- Acceptance criteria de user stories
- `5.3.1` Test Environment — ambiente para UAT
- Lista de UAT participants

**Dependencias (predecessors):**
- `5.4.4` Pass/Fail Summary *(obligatorio)* — QA pass antes de UAT
- `5.3.1` Test Environment *(obligatorio)*

**Habilita (successors):**
- `5.10.2` UAT Test Cases — test cases para UAT
- `5.10.3` UAT Results — resultados
- `5.10.5` UAT Sign-off — decisión final

**Audiencia:**
- **Product Owner** — organiza y lidera UAT
- **Business Users** — participants
- **QA Lead** — coordinación técnica

**Secciones esperadas:**
1. UAT participants (tabla: nombre, rol, departamento, availability)
2. Flujos a testear (en lenguaje de negocio, no técnico)
3. Acceptance criteria por flujo (qué define "funciona")
4. Timeline (fecha inicio, fecha fin, horas por día)
5. Ambiente y acceso (URL, credenciales de test, datos de test)
6. Soporte durante UAT (quién ayuda si algo falla, canal de comunicación)
7. Cómo reportar issues (formulario, canal, qué incluir)
8. Feedback collection method (encuesta, entrevista, formulario)
9. Go/no-go criteria (qué porcentaje de acceptance criteria debe pasar)

**Criterio de completitud:**
- [ ] Participants identificados y confirmados
- [ ] Flujos de negocio principales cubiertos (en lenguaje no-técnico)
- [ ] Acceptance criteria claros y verificables por flujo
- [ ] Timeline definido y comunicado
- [ ] Ambiente accesible y con datos de test
- [ ] Soporte disponible durante UAT
- [ ] Método de reporte de issues definido

**Anti-patrones:**
- ❌ **Developers hacen UAT:** No es acceptance testing si lo hace el equipo que lo construyó — bias confirmatorio.
- ❌ **UAT sin acceptance criteria:** "Pruébalo y dinos qué opinas" — sin criterios no hay pass/fail objetivo.
- ❌ **UAT como formalidad:** PO firma sin que nadie testee realmente — teatro de aceptación.
- ❌ **UAT sin soporte:** Business users encuentran un bug y no saben qué hacer ni a quién reportar.
- ❌ **1 día de UAT para 20 flujos:** Tiempo insuficiente — los users no alcanzan a testear todo.

**Template:** `phases/05-testing/deliverables/uat-plan.md` *(pendiente)*

---

### 5.10.2 UAT Test Cases

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.10 UAT |
| **Responsable** | Product Owner |
| **Ejecuta** | Product Owner / Business Users |
| **Aprueba** | Product Owner |
| **Formato** | Documento |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Pre-UAT |

**Perfil de ejecución:** Requiere traducir test cases técnicos a lenguaje de negocio comprensible por usuarios no-técnicos.  
En VTT: un agente puede generar UAT test cases en lenguaje de negocio desde use cases y user stories. Es altamente delegable.

**Qué es:** Casos de prueba para UAT escritos en lenguaje de negocio (NO técnico): "Como gerente de ventas, puedo generar el reporte mensual por región y exportarlo a Excel". Cada test case tiene: descripción del flujo (en palabras del usuario), pasos simples (sin jerga: "Click en Reportes", no "Navigate to /reports"), resultado esperado (en términos de negocio: "El reporte muestra ventas por región del mes actual"), y datos de test a usar.

**Para qué sirve:** Los test cases de QA (5.2.1) son técnicos ("Verify GET /api/reports returns 200 with correct schema"). Los UAT test cases son de negocio ("Puedo generar mi reporte mensual"). El business user no entiende ni necesita la jerga técnica — necesita steps en su lenguaje.

**Inputs requeridos:**
- `2.3.4` Detailed Use Cases — flujos fuente
- `5.2.1` Test Cases Document — test cases técnicos como referencia
- `5.10.1` UAT Plan — flujos seleccionados para UAT

**Dependencias (predecessors):**
- `5.10.1` UAT Plan *(obligatorio)*

**Habilita (successors):**
- `5.10.3` UAT Results — test cases a ejecutar
- Business users preparados para UAT

**Audiencia:**
- **Business Users** — ejecutan estos test cases
- **Product Owner** — valida que cubren los flujos críticos

**Secciones esperadas:**
1. Instrucciones generales para el UAT participant (cómo usar los test cases)
2. Test cases por flujo de negocio:
   - TC-UAT-001: Título descriptivo en lenguaje de negocio
   - Descripción: qué se verifica
   - Pre-condiciones: qué debe estar listo antes de empezar
   - Pasos: 1, 2, 3... en lenguaje simple
   - Resultado esperado: qué debería pasar
   - Datos de test: qué usuario/datos usar
3. Espacio para resultado (PASS/FAIL) y notas del tester

**Criterio de completitud:**
- [ ] Test cases para cada flujo del UAT Plan
- [ ] Lenguaje no-técnico verificado (un business user lo entiende)
- [ ] Pasos concretos y reproducibles
- [ ] Resultado esperado claro
- [ ] Datos de test proporcionados
- [ ] Probado por al menos 1 business user antes del UAT (dry run)

**Anti-patrones:**
- ❌ **Test cases técnicos en UAT:** "Verificar que el endpoint retorna 200" — el business user no entiende.
- ❌ **Pasos vagos:** "Generar el reporte" — ¿cómo? ¿dónde? ¿qué reporte? Ser específico.
- ❌ **Sin datos de test:** "Usar un cliente existente" — ¿cuál? Proveer username/password/datos específicos.
- ❌ **50 test cases para UAT:** Demasiados — los business users tienen 2-3 horas, no 2 días. Priorizar 10-15 flujos críticos.

**Template:** `phases/05-testing/deliverables/uat-test-cases.md` *(pendiente)*

---

### 5.10.3 UAT Results

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.10 UAT |
| **Responsable** | Product Owner |
| **Ejecuta** | Business Users |
| **Aprueba** | Product Owner |
| **Formato** | Report |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días (durante UAT) |
| **Frecuencia** | Post-UAT |

**Perfil de ejecución:** Requiere compilar resultados de la ejecución de UAT por los business users.  
En VTT: un agente puede compilar y estructurar los resultados recopilados. Es parcialmente delegable. Los resultados vienen de los business users (humanos).

**Qué es:** Resultados de la ejecución de UAT: cada test case con PASS/FAIL, feedback del usuario (notas, confusiones, sugerencias), issues encontrados (bugs o UX problems desde perspectiva de negocio), acceptance criteria cumplidos/no cumplidos, y overall assessment de cada participant ("puedo hacer mi trabajo con este sistema" / "falta X para que funcione").

**Para qué sirve:** Los resultados de UAT son la voz del usuario final — no del QA ni del developer. Si el business user dice "no puedo completar mi flujo diario porque falta la opción de exportar a Excel", eso es un blocker real que QA no habría detectado (la funcionalidad "funciona técnicamente" pero no cumple la necesidad de negocio).

**Inputs requeridos:**
- `5.10.2` UAT Test Cases — test cases ejecutados
- Feedback de participants (formularios, notas, entrevistas)

**Dependencias (predecessors):**
- `5.10.2` UAT Test Cases *(obligatorio)*
- UAT ejecutado por business users *(obligatorio)*

**Habilita (successors):**
- `5.10.4` User Feedback — feedback cualitativo
- `5.10.5` UAT Sign-off — decisión
- Bug fixes para issues encontrados

**Audiencia:**
- **Product Owner** — go/no-go decision input
- **Tech Lead** — bugs a arreglar
- **Developers** — issues reportados
- **QA Lead** — issues no detectados por QA

**Secciones esperadas:**
1. Execution summary (cuántos participants, cuántas horas, cuántos TCs ejecutados)
2. Results table (TC ID, title, tester, result PASS/FAIL, notes, issues found)
3. Pass rate (% de TCs que pasaron)
4. Issues found (tabla: issue, severity, reported by, description, expected vs actual)
5. Acceptance criteria compliance (tabla: criterion, met/not met, evidence)
6. Per-participant assessment (participant, overall impression, can they do their job? yes/no/partially)
7. Blockers (issues que impiden el uso del sistema)
8. Recommendations (proceed / fix and re-test / not ready)

**Criterio de completitud:**
- [ ] Todos los TCs ejecutados con resultado PASS/FAIL
- [ ] Issues encontrados documentados con descripción
- [ ] Acceptance criteria evaluados (met/not met)
- [ ] Assessment de cada participant recopilado
- [ ] Blockers identificados
- [ ] Recommendation incluida

**Anti-patrones:**
- ❌ **Resultados sin notas del usuario:** Solo PASS/FAIL sin contexto — se pierde el feedback valioso.
- ❌ **Issues sin severity:** Todos los issues parecen iguales — priorizar blockers vs nice-to-have.
- ❌ **Results compilados por QA sin input real de business users:** QA interpreta lo que el user "quiso decir" — distorsión.
- ❌ **UAT con 1 participant:** Una opinión no es validación — mínimo 3 users de diferentes roles.

**Template:** `phases/05-testing/deliverables/uat-results.md` *(pendiente)*

---

### 5.10.4 User Feedback

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.10 UAT |
| **Responsable** | Product Owner |
| **Ejecuta** | Business Users |
| **Aprueba** | Product Owner |
| **Formato** | Lista |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Incluido en UAT |
| **Frecuencia** | Post-UAT |

**Perfil de ejecución:** Requiere recopilar y categorizar feedback cualitativo de los participants.  
En VTT: un agente puede categorizar y priorizar feedback recopilado. Es parcialmente delegable. La recopilación requiere humano.

**Qué es:** Feedback cualitativo de los participants de UAT más allá de pass/fail: sugerencias de mejora ("sería útil poder filtrar por fecha también"), frustraciones ("el flujo de aprobación tiene demasiados pasos"), features faltantes percibidas ("esperaba poder exportar a PDF"), comparación con la solución actual ("en el sistema viejo esto era más rápido"), y elogios ("la búsqueda es excelente, mucho mejor que antes"). Categorizado por tipo y prioridad.

**Para qué sirve:** El feedback de UAT es oro puro — son usuarios reales diciendo qué necesitan. Informa el roadmap post-launch: las sugerencias más frecuentes se convierten en features del próximo sprint. Las frustraciones se convierten en UX improvements. Los elogios confirman qué se hizo bien.

**Inputs requeridos:**
- `5.10.3` UAT Results — feedback capturado durante ejecución
- Entrevistas post-UAT con participants (opcional)
- Encuesta de satisfacción (opcional)

**Dependencias (predecessors):**
- `5.10.3` UAT Results *(obligatorio)*

**Habilita (successors):**
- `7.4.4` Improvement Backlog — feedback como input de mejoras
- Post-launch roadmap — features pedidos por usuarios
- Product decisions informadas por usuarios reales

**Audiencia:**
- **Product Owner** — roadmap input
- **UX Designer** — UX improvements
- **Developers** — awareness de necesidades
- **Management** — user satisfaction

**Secciones esperadas:**
1. Feedback collection method (formulario, entrevista, survey, notas)
2. Feedback categorizado:
   - Mejoras sugeridas (feature requests, UX improvements)
   - Frustraciones reportadas (pain points, confusiones)
   - Features faltantes percibidas (qué esperaban y no encontraron)
   - Comparación con solución actual (mejor/peor/igual)
   - Elogios (qué se hizo bien — mantener)
3. Frequency analysis (qué feedback se repitió más — prioridad alta)
4. Priority matrix (impact × frequency)
5. Action items (qué feedback se actuará en el próximo sprint)

**Criterio de completitud:**
- [ ] Feedback de todos los participants recopilado
- [ ] Categorizado por tipo (mejora, frustración, faltante, elogio)
- [ ] Frequency analysis (qué se repite más)
- [ ] Priority matrix aplicada
- [ ] Top 5 action items identificados
- [ ] Feedback comunicado al equipo de producto

**Anti-patrones:**
- ❌ **Feedback ignorado:** Recopilar y archivar sin actuar — los users no participan en la próxima UAT.
- ❌ **Solo feedback negativo:** Documentar solo problemas — los elogios informan qué mantener y motivan al equipo.
- ❌ **Feedback sin priorización:** Lista plana de 50 sugerencias — ¿cuáles importan más? Frequency analysis.
- ❌ **Un solo participant domina:** La opinión más vocal no es la más representativa — buscar patrones entre múltiples users.

**Template:** `phases/05-testing/deliverables/user-feedback.md` *(pendiente)*

---

### 5.10.5 UAT Sign-off

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.10 UAT |
| **Responsable** | Product Owner |
| **Ejecuta** | Product Owner |
| **Aprueba** | Product Owner |
| **Formato** | Sign-off |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.25 día |
| **Frecuencia** | Pre-release |

**Perfil de ejecución:** Requiere autoridad del Product Owner para dar go/no-go desde perspectiva de negocio.  
En VTT: un agente puede compilar el sign-off document con datos de UAT results. NO puede tomar la decisión. Es parcialmente delegable.

**Qué es:** Aprobación formal del Product Owner de que el producto cumple los requisitos de negocio y está listo para producción. Incluye: acceptance criteria cumplidos/no cumplidos con evidencia, issues conocidos aceptados (con justificación), condiciones (si aplica: "aprobado con la condición de que X se arregle en sprint 1 post-launch"), y firma del PO (y opcionalmente de stakeholders clave).

**Para qué sirve:** Es el ÚLTIMO gate antes de deploy a producción. Sin sign-off del PO, el producto no se lanza — incluso si QA aprobó. El PO representa al negocio y al usuario; su aprobación confirma: "este producto resuelve el problema de negocio suficientemente bien para lanzar".

**Inputs requeridos:**
- `5.10.3` UAT Results — resultados
- `5.10.4` User Feedback — feedback de participants
- `5.4.4` Pass/Fail Summary — QA results

**Dependencias (predecessors):**
- `5.10.3` UAT Results *(obligatorio)*
- `5.4.4` Pass/Fail Summary *(obligatorio)*

**Habilita (successors):**
- `6.5.1` Production Deploy — gate de entrada (sin UAT sign-off, no deploy)

**Audiencia:**
- **Product Owner** — decisor
- **Tech Lead** — go/no-go coordinación
- **Management** — launch visibility
- **Stakeholders** — confirmación

**Secciones esperadas:**
1. UAT results summary (TCs ejecutados, pass rate, participants)
2. Acceptance criteria compliance (tabla: criterion, status met/not met, evidence)
3. Issues conocidos y aceptados (tabla: issue, severity, justificación de acceptance)
4. User feedback summary (top themes)
5. Conditions (if any: "aprobado con condición de que X se arregle antes de fecha Y")
6. Blockers assessment (0 blockers = go, blockers = no-go)
7. Go/No-go decision (con justificación)
8. Signatures (Product Owner + stakeholders clave)

**Criterio de completitud:**
- [ ] UAT completado por business users
- [ ] Acceptance criteria evaluados con evidence
- [ ] Known issues documentados y aceptados (o no)
- [ ] Decision documentada (go / no-go / conditional)
- [ ] Conditions con deadline (si conditional)
- [ ] Firma del Product Owner
- [ ] Stakeholders informados de la decisión

**Anti-patrones:**
- ❌ **Sign-off sin UAT:** PO firma sin que business users hayan testeado — theatre.
- ❌ **PO presionado a aprobar:** "Tenemos deadline" — el PO debe poder decir no-go sin consecuencias.
- ❌ **Sign-off condicional sin follow-up:** "Aprobado si arreglan X" pero nadie trackea si X se arregla.
- ❌ **Sign-off sin acceptance criteria:** "Se ve bien, aprobado" — sin criterios medibles no es acceptance formal.
- ❌ **Solo PO firma sin consultar users:** Los participants tienen feedback — el PO debe incorporarlo en la decisión.

**Template:** `phases/05-testing/deliverables/uat-signoff.md` *(pendiente)*

---

## Tabla resumen — Fase 5.10

| Deliverable | Responsable | Delegable VTT |
|-------------|-------------|---------------|
| 5.10.1 UAT Plan | Product Owner | ✅ — plan generables desde use cases |
| 5.10.2 UAT Test Cases | Product Owner | ✅ — TCs en lenguaje de negocio generables |
| 5.10.3 UAT Results | Product Owner | 🔶 — compilar resultados sí, ejecutar UAT no |
| 5.10.4 User Feedback | Product Owner | 🔶 — categorizar sí, recopilar no |
| 5.10.5 UAT Sign-off | Product Owner | ❌ — decisión humana |
