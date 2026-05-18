# DICCIONARIO DE DELIVERABLES — FASE 4.8: CODE REVIEW

**Versión:** 1.0  
**Fecha:** 2026-05-14  
**Fase:** 4 — Development  
**Subfase:** 4.8 — Code Review  
**Total deliverables:** 4  
**Responsable de subfase:** Tech Lead  
**Aprueba:** Solution Architect

---

## Contexto de la subfase

Code Review es el proceso de calidad que asegura que cada línea de código que entra al codebase ha sido revisada por al menos otra persona. No es solo buscar bugs — es compartir conocimiento, mantener estándares, detectar deuda técnica, y mentorear al equipo. Los deliverables de esta subfase son procesos y artefactos de tracking, no código.

**Prerequisitos de subfase:**
- Código en desarrollo (4.3, 4.4, 4.5)
- Coding Standards (3B.2.2) — criterios de review
- Contributing Guide (4.7.7) — PR process

**Entrega de subfase:**
- Proceso de code review funcional, reportes de calidad, y tracking de deuda técnica

---

### 4.8.1 PR Reviews

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.8 Code Review |
| **Responsable** | Tech Lead |
| **Ejecuta** | Todo el equipo de desarrollo |
| **Aprueba** | Tech Lead |
| **Formato** | GitHub / GitLab |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Continuo (20-30% del tiempo de dev) |
| **Frecuencia** | Por PR |

**Perfil de ejecución:** Requiere experiencia técnica para evaluar: correctitud, mantenibilidad, performance, seguridad, y adherencia a estándares.  
En VTT: un agente puede hacer pre-review automatizado: linting, formatting, type checking, test coverage, y detección de patterns problemáticos. NO puede hacer el review humano de lógica, diseño, y naming. Necesita brief con: coding standards, review checklist, y PR diff.

**Qué es:** Proceso de revisión de cada Pull Request antes de mergear a main: al menos 1 reviewer (2 para código crítico), review de: correctitud de lógica, adherencia a coding standards, tests incluidos, documentación actualizada, y no-introducción de bugs/vulnerabilidades. Incluye: PR template, review checklist, y turnaround time expectations.

**Para qué sirve:** Code review es el control de calidad más efectivo del desarrollo: detecta bugs que los tests no cubren, mantiene la consistencia del codebase, comparte conocimiento entre el equipo (el reviewer aprende el código del author y viceversa), y previene que deuda técnica se acumule silenciosamente.

**Inputs requeridos:**
- `3B.2.2` Coding Standards — criterios de review
- `4.7.7` Contributing Guide — PR process
- PR template configurado en el repo
- Review checklist

**Dependencias (predecessors):**
- `3B.2.2` Coding Standards *(obligatorio)* — qué evaluar
- `4.7.7` Contributing Guide *(obligatorio)* — proceso de PR

**Habilita (successors):**
- `4.8.2` Code Quality Report — data de reviews
- Código de calidad en main branch

**Audiencia:**
- **Todo el equipo de desarrollo** — participan como author y reviewer

**Secciones esperadas:**
1. PR template (descripción, tipo de cambio, checklist, screenshots)
2. Review checklist (correctitud, tests, docs, security, performance)
3. Review assignment (quién revisa qué — round robin, CODEOWNERS)
4. Turnaround time (max 24h para primer review)
5. Merge requirements (min approvals, CI green, no conflicts)
6. Review etiquette (constructivo, específico, con sugerencias)

**Criterio de completitud:**
- [ ] PR template configurado en el repo
- [ ] Review checklist documentada
- [ ] CODEOWNERS configurado (o assignment policy)
- [ ] Turnaround time acordado (max 24h)
- [ ] Branch protection rules (min 1 approval, CI green)
- [ ] Todo el equipo entiende y sigue el proceso

**Anti-patrones:**
- ❌ **LGTM sin leer:** Aprobar sin revisar para "no bloquear" — derrota el propósito.
- ❌ **Nitpicking:** 20 comentarios sobre naming preferences — enfocarse en correctitud y diseño.
- ❌ **Reviews de 500+ líneas:** PRs enormes que nadie revisa bien — hacer PRs pequeños (<300 líneas).
- ❌ **Solo el Tech Lead revisa:** Un reviewer para todo — bottleneck y sin knowledge sharing.
- ❌ **Reviews destructivos:** "Esto está mal" sin explicar por qué ni sugerir alternativa — desmotiva.

**Template:** `phases/04-development/deliverables/pr-template.md` *(pendiente)*

---

### 4.8.2 Code Quality Report

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.8 Code Review |
| **Responsable** | Tech Lead |
| **Ejecuta** | Tech Lead / QA Lead |
| **Aprueba** | Solution Architect |
| **Formato** | Report |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día por sprint |
| **Frecuencia** | Por sprint |

**Perfil de ejecución:** Requiere agregar métricas de calidad del código y presentarlas de forma accionable.  
En VTT: un agente puede generar el reporte agregando datos de: SonarQube, coverage reports, linting stats, y PR metrics. Es altamente delegable.

**Qué es:** Reporte periódico (por sprint) de la calidad del código: coverage %, lint errors/warnings trend, code complexity metrics (cyclomatic), duplication %, PR metrics (time to review, size, comments), y technical debt trend. Puede generarse desde SonarQube, CodeClimate, o manualmente.

**Para qué sirve:** Sin métricas, "la calidad del código es buena" es una opinión. Con métricas, es un dato: "coverage subió de 72% a 81%, complejidad ciclomática promedio bajó de 15 a 11, y el tiempo promedio de review es 4 horas". Las métricas permiten detectar tendencias negativas antes de que se conviertan en problemas.

**Inputs requeridos:**
- `4.6.3` Test Coverage Report — coverage data
- Linting results de CI
- PR metrics de GitHub/GitLab
- SonarQube / CodeClimate (si configurado)

**Dependencias (predecessors):**
- `4.6.3` Test Coverage Report *(obligatorio)*
- CI pipeline con métricas *(obligatorio)*

**Habilita (successors):**
- `4.8.4` Refactoring Plan — áreas a refactorizar basadas en métricas
- Sprint retrospective — data para discusión de calidad

**Audiencia:**
- **Tech Lead** — oversight de calidad
- **Solution Architect** — tendencias de calidad
- **QA Lead** — coverage y defects
- **Management** — health del codebase (si lo requieren)

**Secciones esperadas:**
1. Coverage % (backend, frontend, total) — trend vs sprint anterior
2. Lint errors/warnings count — trend
3. Code complexity (cyclomatic complexity promedio y max)
4. Duplication % — trend
5. PR metrics (avg size, avg time to review, avg comments)
6. Technical debt score (si SonarQube/CodeClimate)
7. Top issues (archivos/módulos más problemáticos)
8. Actions (qué mejorar en el próximo sprint)

**Criterio de completitud:**
- [ ] Métricas de coverage incluidas con trend
- [ ] Métricas de lint incluidas
- [ ] PR metrics incluidas
- [ ] Trend vs sprint anterior (mejora/empeora)
- [ ] Actions derivadas de las métricas
- [ ] Generado cada sprint

**Anti-patrones:**
- ❌ **Métricas sin acción:** Reportar "coverage es 65%" sin plan para subirlo — datos decorativos.
- ❌ **Solo coverage:** Coverage es una métrica; calidad incluye complexity, duplication, y review metrics.
- ❌ **Reporte que nadie lee:** 20 páginas de gráficos — resumir en 1 página con top 3 actions.
- ❌ **Métricas como castigo:** "Tu archivo tiene complejidad 25, arréglalo" — usar métricas para mejorar, no para culpar.

**Template:** `phases/04-development/deliverables/code-quality-report.md` *(pendiente)*

---

### 4.8.3 Technical Debt Log

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.8 Code Review |
| **Responsable** | Tech Lead |
| **Ejecuta** | Tech Lead / Todo el equipo |
| **Aprueba** | Solution Architect |
| **Formato** | Documento |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Continuo (actualización por sprint) |
| **Frecuencia** | Continua |

**Perfil de ejecución:** Requiere identificar y clasificar deuda técnica: accidental (bugs, shortcuts) vs deliberada (trade-offs conscientes).  
En VTT: un agente puede mantener el log actualizado recibiendo inputs del equipo y detectando TODOs/FIXMEs en el código. Es bastante delegable.

**Qué es:** Registro de toda la deuda técnica conocida del proyecto: shortcuts tomados conscientemente ("usamos polling en vez de WebSocket por deadline — refactorizar en sprint 5"), TODO/FIXMEs del código, código que funciona pero no es óptimo, tests faltantes, y áreas que necesitan refactoring. Cada entrada tiene: descripción, impacto, esfuerzo de fix, y prioridad.

**Para qué sirve:** Toda deuda técnica es invisible hasta que explota. El log la hace visible: el equipo sabe exactamente cuánta deuda tiene, cuál es la más riesgosa, y cuánto costaría pagarla. Permite al Product Manager priorizar tech debt paydown vs features nuevas con información real.

**Inputs requeridos:**
- Code reviews (deuda detectada en reviews)
- TODO/FIXME scan del codebase
- `4.8.2` Code Quality Report — áreas problemáticas
- Decisiones de shortcuts durante sprints

**Dependencias (predecessors):**
- Código en desarrollo (4.3, 4.4, 4.5) — fuente de deuda

**Habilita (successors):**
- `4.8.4` Refactoring Plan — plan para pagar la deuda
- Sprint planning — tech debt como work items

**Audiencia:**
- **Tech Lead** — priorización técnica
- **Product Manager** — balance feature vs tech debt
- **Solution Architect** — riesgo técnico
- **Todo el equipo** — awareness de deuda

**Secciones esperadas:**
1. Tabla de deuda técnica (ID, descripción, tipo, impacto, esfuerzo, prioridad, sprint detectado)
2. Clasificación por tipo (code quality, architecture, testing, infrastructure, documentation)
3. Clasificación por impacto (high: afecta performance/security, medium: afecta mantenibilidad, low: cosmético)
4. Esfuerzo estimado por item (horas/story points)
5. Items resueltos (historial de deuda pagada)
6. Total debt score (suma de esfuerzo pendiente)

**Criterio de completitud:**
- [ ] Toda deuda conocida registrada
- [ ] Impacto y esfuerzo estimado por item
- [ ] Priorización aplicada
- [ ] Actualizado cada sprint
- [ ] TODOs/FIXMEs del código incluidos
- [ ] Items resueltos removidos a historial

**Anti-patrones:**
- ❌ **Deuda invisible:** "El código está bien" — todo proyecto tiene deuda; si no la ves, no la estás buscando.
- ❌ **Log sin priorización:** 50 items sin prioridad — el equipo no sabe por dónde empezar.
- ❌ **Nunca pagar deuda:** Registrar deuda y nunca asignar tiempo para resolverla — la deuda crece exponencialmente.
- ❌ **TODO sin tracking:** 200 TODOs en el código sin log — nadie los revisa.

**Template:** `phases/04-development/deliverables/tech-debt-log.md` *(pendiente)*

---

### 4.8.4 Refactoring Plan

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.8 Code Review |
| **Responsable** | Tech Lead |
| **Ejecuta** | Tech Lead |
| **Aprueba** | Solution Architect |
| **Formato** | Documento |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día por sprint |
| **Frecuencia** | Por sprint / por milestone |

**Perfil de ejecución:** Requiere planificar refactoring como trabajo estimado y priorizado, no como "lo hacemos cuando podamos".  
En VTT: un agente puede generar el plan de refactoring a partir del tech debt log. Es bastante delegable.

**Qué es:** Plan para pagar la deuda técnica de forma controlada: qué items del Technical Debt Log se van a refactorizar, en qué sprint, quién los hace, y cómo se valida (tests que deben pasar). Incluye: priorización por riesgo × esfuerzo, allocation de tiempo (regla 80/20: 80% features, 20% tech debt), y success criteria por refactoring.

**Para qué sirve:** Sin plan, el refactoring es: (a) "nunca" — la deuda crece hasta que el sistema es inmantenible, o (b) "big rewrite" — un proyecto de 3 meses para reescribir todo desde cero que siempre falla. El plan propone refactoring incremental: pequeños cambios cada sprint que mantienen la deuda bajo control.

**Inputs requeridos:**
- `4.8.3` Technical Debt Log — deuda a planificar
- `4.8.2` Code Quality Report — áreas más problemáticas
- Sprint capacity — tiempo disponible para tech debt

**Dependencias (predecessors):**
- `4.8.3` Technical Debt Log *(obligatorio)* — items a planificar
- `4.8.2` Code Quality Report *(recomendado)* — priorización data-driven

**Habilita (successors):**
- Sprints con tech debt allocation
- Codebase mantenible a largo plazo

**Audiencia:**
- **Tech Lead** — planificación
- **Product Manager** — negociación de tiempo para tech debt
- **Solution Architect** — riesgo mitigado
- **Development Team** — items asignados

**Secciones esperadas:**
1. Items priorizados del debt log para próximo sprint/milestone
2. Allocation de tiempo (e.g., 20% del sprint = X story points para tech debt)
3. Por item: descripción, esfuerzo, assignee, sprint, success criteria
4. Regla de no-new-debt (no agregar deuda en sprints de paydown)
5. Métricas de mejora esperada (coverage sube de X a Y, complexity baja de X a Y)
6. Refactoring completados (historial)

**Criterio de completitud:**
- [ ] Top 3-5 items de deuda priorizados para próximo sprint
- [ ] Tiempo asignado (no "si sobra tiempo" — tiempo planificado)
- [ ] Success criteria por refactoring (qué tests pasan, qué métrica mejora)
- [ ] Assignee por item
- [ ] Aprobado por Product Manager (balance feature vs debt)

**Anti-patrones:**
- ❌ **"Lo hacemos cuando podamos":** Nunca hay tiempo — tech debt debe estar en el sprint como work item.
- ❌ **Big rewrite:** "Vamos a reescribir todo el backend" — casi siempre falla. Refactoring incremental es más seguro.
- ❌ **Refactoring sin tests:** Refactorizar sin safety net de tests — introducir bugs nuevos.
- ❌ **Plan sin buy-in del PM:** El tech lead planea 50% tech debt y el PM no sabe — conflicto garantizado.
- ❌ **Refactoring sin success criteria:** "Mejorar el módulo de pagos" — ¿cómo sabemos que "mejoró"?

**Template:** `phases/04-development/deliverables/refactoring-plan.md` *(pendiente)*

---

## Tabla resumen de ejecutores — Fase 4.8 Code Review

| Deliverable | Responsable | Ejecuta | Delegable VTT |
|-------------|-------------|---------|---------------|
| 4.8.1 PR Reviews | Tech Lead | Todo el equipo | 🔶 Parcial — pre-review automatizado sí, review humano de lógica no |
| 4.8.2 Code Quality Report | Tech Lead | Tech Lead / QA Lead | ✅ — puede agregar métricas y generar reporte |
| 4.8.3 Technical Debt Log | Tech Lead | Tech Lead / Todo el equipo | ✅ — puede mantener log y scan TODOs/FIXMEs |
| 4.8.4 Refactoring Plan | Tech Lead | Tech Lead | 🔶 Parcial — puede generar plan, priorización requiere juicio humano |

---

## Resumen de cierre — Fase 4 Development completa

Con este archivo se completa la **Fase 4: Development** del diccionario de deliverables.

| Subfase | Archivo | Deliverables | Status |
|---------|---------|-------------|--------|
| 4.1 Environment Setup | `DICCIONARIO_FASE_04_01_ENVIRONMENT_SETUP.md` | 10 | ✅ |
| 4.2 Database Implementation | `DICCIONARIO_FASE_04_02_DATABASE_IMPLEMENTATION.md` | 10 | ✅ |
| 4.3 Backend Development | `DICCIONARIO_FASE_04_03_BACKEND_DEVELOPMENT.md` | 15 | ✅ |
| 4.4 Frontend Development | `DICCIONARIO_FASE_04_04_FRONTEND_DEVELOPMENT.md` | 15 | ✅ |
| 4.5 Integrations | `DICCIONARIO_FASE_04_05_INTEGRATIONS.md` | 9 | ✅ |
| 4.6 Unit Tests | `DICCIONARIO_FASE_04_06_UNIT_TESTS.md` | 7 | ✅ |
| 4.7 Technical Documentation | `DICCIONARIO_FASE_04_07_TECHNICAL_DOCUMENTATION.md` | 8 | ✅ |
| 4.8 Code Review | `DICCIONARIO_FASE_04_08_CODE_REVIEW.md` | 4 | ✅ |
| **TOTAL FASE 4** | **8 archivos** | **78** | **✅ Completa** |

---

## Siguiente archivo

**Próximo:** Fase 5: Testing (52 deliverables en 11 subfases)  
**Nota:** Fase 5 tiene >50 deliverables, se divide por subfase.  
**Primer archivo:** `DICCIONARIO_FASE_05_01_TEST_PLANNING.md`
