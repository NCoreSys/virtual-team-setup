# DICCIONARIO DE DELIVERABLES — FASE 5.1: TEST PLANNING

**Versión:** 1.0  
**Fecha:** 2026-05-14  
**Fase:** 5 — Testing  
**Subfase:** 5.1 — Test Planning  
**Total deliverables:** 5  
**Responsable de subfase:** QA Lead  
**Aprueba:** Tech Lead

---

## Contexto de la subfase

Test Planning define la estrategia, alcance, cronograma, y recursos de testing antes de ejecutar un solo test. Es el equivalente al "plan de batalla" de QA: qué se testea, cómo, con qué herramientas, quién lo hace, y cuándo está listo. Sin plan, el testing es ad-hoc y reactivo — "probamos lo que podemos antes del release".

**Prerequisitos de subfase:**
- Development en progreso o completado (Fase 4)
- Requirements y Use Cases (Fase 2) — qué testear
- NFRs definidos — performance, security targets

**Entrega de subfase:**
- Plan de testing completo, estrategia definida, y recursos asignados

---

### 5.1.1 Test Plan

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.1 Test Planning |
| **Responsable** | QA Lead |
| **Ejecuta** | QA Lead |
| **Aprueba** | Tech Lead |
| **Formato** | MD/PDF |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Una vez + refinamiento por sprint |

**Perfil de ejecución:** Requiere experiencia en test management y conocimiento del producto para definir un plan de testing integral.  
En VTT: un agente puede generar la estructura del test plan completa. Es bastante delegable. Necesita brief con: scope del producto, tipos de testing requeridos, herramientas, y equipo disponible.

**Qué es:** Documento maestro de testing que consolida: qué se testea (scope), cómo se testea (estrategia), con qué herramientas (tools), quién testea (recursos), cuándo se testea (schedule), y cuándo se considera "suficiente" (exit criteria). Es el plan que el QA Lead ejecuta y que el Tech Lead aprueba.

**Para qué sirve:** Sin plan, el testing es caótico: QA testea lo que se acuerda, en el orden que quiere, con los datos que tiene. El plan asegura cobertura sistemática, priorización por riesgo, y criterios de exit claros.

**Inputs requeridos:**
- `2.3.4` Detailed Use Cases — qué funcionalidades testear
- `2.5.1` Business Rules Document — reglas a validar
- `3B.4.1` OpenAPI Spec — API contracts a testear
- NFRs — targets de performance, security

**Dependencias (predecessors):**
- `2.3.4` Detailed Use Cases *(obligatorio)*
- `5.1.2` Test Strategy *(co-dependencia)* — estrategia informa el plan

**Habilita (successors):**
- `5.1.3` Test Scope — scope detallado
- `5.2.1` Test Cases Document — test cases basados en el plan
- `5.4.1` Functional Test Results — ejecución del plan
- Todos los tipos de testing (5.4 - 5.10)

**Audiencia:**
- **QA Team** — guía de ejecución
- **Tech Lead** — aprobación
- **Product Manager** — visibilidad de coverage
- **Management** — timeline de testing

**Secciones esperadas:**
1. Objetivos de testing
2. Scope (in/out — qué se testea, qué no)
3. Tipos de testing (functional, integration, E2E, performance, security, accessibility, UAT)
4. Herramientas por tipo (Jest, Playwright, k6, OWASP ZAP)
5. Entry criteria (cuándo empezar testing)
6. Exit criteria (cuándo se considera "suficiente")
7. Risk-based prioritization (qué testear primero)
8. Defect management process (cómo se reportan, clasifican, y resuelven bugs)
9. Schedule
10. Resources

**Criterio de completitud:**
- [ ] Todos los tipos de testing definidos
- [ ] Entry y exit criteria claros
- [ ] Herramientas seleccionadas
- [ ] Risk-based prioritization aplicada
- [ ] Schedule con milestones
- [ ] Defect management process definido
- [ ] Aprobado por Tech Lead

**Anti-patrones:**
- ❌ **"Probamos todo":** Sin priorización por riesgo — se gasta tiempo igual en features críticas y cosméticas.
- ❌ **Sin exit criteria:** "Testeamos hasta que se acabe el tiempo" — no hay definición de "suficiente".
- ❌ **Plan sin schedule:** "Testeamos cuando esté el código" — sin timeline, QA siempre queda último y con poco tiempo.
- ❌ **Solo functional testing:** Ignorar performance, security, y accessibility — bugs que explotan en producción.

**Template:** `phases/05-testing/deliverables/test-plan.md` *(pendiente)*

---

### 5.1.2 Test Strategy

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.1 Test Planning |
| **Responsable** | QA Lead |
| **Ejecuta** | QA Lead |
| **Aprueba** | Tech Lead |
| **Formato** | Documento |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere definir el approach de testing: test pyramid, automation strategy, y manual vs automated balance.  
En VTT: un agente puede generar la estrategia. Es bastante delegable.

**Qué es:** Definición del approach de testing del proyecto: test pyramid (muchos unit tests, menos integration, pocos E2E), automation strategy (qué automatizar, qué queda manual), manual vs automated balance (80% automated / 20% manual), regression strategy (qué re-testear en cada sprint), y environments strategy (dónde se ejecuta cada tipo de test).

**Para qué sirve:** Define el "cómo" del testing a nivel estratégico. Sin estrategia, QA hace todo manual (no escala) o todo automated (costoso de mantener para UI volátil). La estrategia balancea costo, cobertura, y velocidad.

**Inputs requeridos:**
- `3B.1.5` Technology Stack — herramientas de testing
- Complejidad del producto
- Tamaño del equipo de QA

**Dependencias (predecessors):**
- `3B.1.5` Technology Stack *(obligatorio)*

**Habilita (successors):**
- `5.1.1` Test Plan — estrategia informa el plan
- Todos los tipos de testing

**Audiencia:**
- **QA Team** — guía estratégica
- **Tech Lead** — alineación técnica

**Secciones esperadas:**
1. Test pyramid (unit → integration → E2E — ratio)
2. Automation strategy (qué automatizar: API tests, critical paths, regression)
3. Manual testing (qué queda manual: exploratory, UAT, visual)
4. Regression strategy (qué re-testear en cada release)
5. Shift-left approach (testing temprano en el ciclo)
6. Defect prevention vs detection

**Criterio de completitud:**
- [ ] Test pyramid definida con ratios
- [ ] Automation vs manual balance definido
- [ ] Regression strategy documentada
- [ ] Herramientas por tipo de test
- [ ] Alineada con capacidad del equipo

**Anti-patrones:**
- ❌ **Todo manual:** No escala — cada release requiere más tiempo de testing.
- ❌ **Inverted pyramid:** Más E2E que unit tests — frágil, lento, costoso de mantener.
- ❌ **Automatizar UI volátil:** Automatizar una UI que cambia cada sprint — tests rotos constantemente.

**Template:** `phases/05-testing/deliverables/test-strategy.md` *(pendiente)*

---

### 5.1.3 Test Scope

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.1 Test Planning |
| **Responsable** | QA Lead |
| **Ejecuta** | QA Lead |
| **Aprueba** | Tech Lead |
| **Formato** | Documento |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Por sprint/release |

**Perfil de ejecución:** Requiere definir qué se testea y qué no, con justificación.  
En VTT: un agente puede generar el scope desde use cases y risk assessment. Es altamente delegable.

**Qué es:** Definición explícita del alcance de testing: qué funcionalidades se testean (in-scope), qué no se testea y por qué (out-of-scope), qué plataformas/browsers (Chrome, Safari, mobile), y qué versiones. El scope se ajusta por sprint basándose en qué cambió.

**Para qué sirve:** Sin scope, QA intenta testear todo — imposible en el tiempo disponible. El scope prioriza: features nuevas, features modificadas, y regression de áreas de riesgo. Lo que está fuera de scope se documenta (no se "olvida").

**Inputs requeridos:**
- `2.3.3` Use Case List — funcionalidades
- `5.1.1` Test Plan — contexto
- Sprint scope (qué features son nuevas/modificadas)

**Dependencias (predecessors):**
- `5.1.1` Test Plan *(obligatorio)*

**Habilita (successors):**
- `5.2.1` Test Cases Document — test cases dentro del scope

**Audiencia:**
- **QA Team** — qué testear
- **Product Owner** — qué está cubierto y qué no

**Secciones esperadas:**
1. In-scope (funcionalidades, plataformas, browsers)
2. Out-of-scope (con justificación)
3. Browser/device matrix (qué combinaciones se testean)
4. Scope por sprint (qué cambió, qué re-testear)

**Criterio de completitud:**
- [ ] In-scope documentado por módulo/feature
- [ ] Out-of-scope con justificación
- [ ] Browser/device matrix definida
- [ ] Aprobado por Product Owner

**Anti-patrones:**
- ❌ **Scope = "todo":** Imposible de cumplir — priorizar por riesgo.
- ❌ **Out-of-scope no documentado:** Features no testeadas sin que nadie sepa.
- ❌ **Sin browser matrix:** "Testeamos en Chrome" — ¿y Safari? ¿y mobile?

**Template:** `phases/05-testing/deliverables/test-scope.md` *(pendiente)*

---

### 5.1.4 Test Schedule

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.1 Test Planning |
| **Responsable** | QA Lead |
| **Ejecuta** | QA Lead |
| **Aprueba** | Tech Lead |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.25 día |
| **Frecuencia** | Por sprint |

**Perfil de ejecución:** Requiere planificar el timeline de testing alineado al sprint.  
En VTT: un agente puede generar el schedule. Es altamente delegable.

**Qué es:** Cronograma de testing por sprint/release: cuándo se escriben test cases, cuándo se ejecutan tests manuales, cuándo corren automation suites, cuándo se hace regression, y cuándo es el deadline de bug fixes. Alineado con el sprint calendar.

**Para qué sirve:** Sin schedule, testing se comprime al último día del sprint. Con schedule, el tiempo de testing está protegido y el equipo sabe cuándo entregar código "testeable" a QA.

**Inputs requeridos:**
- Sprint calendar
- `5.1.3` Test Scope — qué testear en este sprint

**Dependencias (predecessors):**
- `5.1.1` Test Plan *(obligatorio)*

**Habilita (successors):**
- Ejecución ordenada del testing

**Audiencia:**
- **QA Team** — timeline
- **Development Team** — deadlines de entrega a QA

**Secciones esperadas:**
1. Timeline por sprint (test case creation → execution → regression → sign-off)
2. Dependencies (cuándo necesita QA el código)
3. Milestones de testing
4. Buffer para bug fixes y re-test

**Criterio de completitud:**
- [ ] Timeline con fechas por actividad de testing
- [ ] Dependencies con development documentadas
- [ ] Buffer para bug fixes incluido
- [ ] Alineado con sprint calendar

**Anti-patrones:**
- ❌ **Testing el último día:** Sprint de 10 días, testing en el día 10 — sin tiempo para bugs.
- ❌ **Sin buffer de bug fixes:** Se encuentran bugs pero no hay tiempo para arreglar y re-testear.

**Template:** `phases/05-testing/deliverables/test-schedule.md` *(pendiente)*

---

### 5.1.5 Resource Allocation

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.1 Test Planning |
| **Responsable** | QA Lead |
| **Ejecuta** | QA Lead |
| **Aprueba** | Tech Lead |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.25 día |
| **Frecuencia** | Por sprint |

**Perfil de ejecución:** Requiere asignar QA resources a tipos de testing y módulos.  
En VTT: un agente puede generar la asignación. Es altamente delegable.

**Qué es:** Asignación de recursos de QA a actividades de testing: quién hace qué tipo de test, quién es responsible de qué módulo, y cómo se distribuye el tiempo entre manual y automation. Incluye: skills matrix del QA team y assignment por competencia.

**Para qué sirve:** Sin asignación, todos testean "lo que pueden" y nadie es responsible de nada en particular. La asignación asegura cobertura: "María es responsible de API testing, Juan de E2E, Pedro de UAT coordination".

**Inputs requeridos:**
- QA team roster con skills
- `5.1.4` Test Schedule — timeline
- `5.1.3` Test Scope — qué testear

**Dependencias (predecessors):**
- `5.1.4` Test Schedule *(obligatorio)*

**Habilita (successors):**
- QA team sabe qué hacer

**Audiencia:**
- **QA Team** — assignment
- **QA Lead** — resource management

**Secciones esperadas:**
1. QA team roster (nombre, rol, skills, availability)
2. Assignment por tipo de testing (functional, API, E2E, performance)
3. Assignment por módulo/feature
4. Backup assignments (si alguien no está disponible)

**Criterio de completitud:**
- [ ] Cada tipo de testing tiene assignee
- [ ] Cada módulo tiene QA responsible
- [ ] Backup plan documentado
- [ ] Alineado con skills del equipo

**Anti-patrones:**
- ❌ **Un QA para todo:** Bottleneck garantizado.
- ❌ **Sin skills match:** QA junior asignado a security testing — no tiene la experiencia.

**Template:** `phases/05-testing/deliverables/resource-allocation.md` *(pendiente)*

---

## Tabla resumen de ejecutores — Fase 5.1 Test Planning

| Deliverable | Responsable | Ejecuta | Delegable VTT |
|-------------|-------------|---------|---------------|
| 5.1.1 Test Plan | QA Lead | QA Lead | ✅ — puede generar plan completo |
| 5.1.2 Test Strategy | QA Lead | QA Lead | ✅ — puede generar estrategia |
| 5.1.3 Test Scope | QA Lead | QA Lead | ✅ — puede generar scope desde use cases |
| 5.1.4 Test Schedule | QA Lead | QA Lead | ✅ — puede generar schedule |
| 5.1.5 Resource Allocation | QA Lead | QA Lead | 🔶 Parcial — puede generar asignación, staffing decisions son humanas |

---

## Siguiente archivo

**Próximo:** `DICCIONARIO_FASE_05_02_TEST_CASES.md` — 4 deliverables (5.2.1 a 5.2.4)
