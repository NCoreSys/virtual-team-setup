# DICCIONARIO DE DELIVERABLES — FASE 5.6: E2E TESTING

**Versión:** 1.1  
**Fecha:** 2026-05-14  
**Fase:** 5 — Testing  
**Subfase:** 5.6 — E2E Testing  
**Total deliverables:** 5  
**Responsable de subfase:** QA Automation  
**Aprueba:** QA Lead

---

## Contexto de la subfase

E2E Testing simula al usuario real en un browser: navega, llena formularios, clickea botones, y verifica resultados. Cubre flujos completos de inicio a fin (registro → login → crear proyecto → completar tarea → logout). Es la validación más cercana a la experiencia real del usuario.

---

### 5.6.1 E2E Test Suite

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.6 E2E Testing |
| **Responsable** | QA Automation |
| **Ejecuta** | QA Automation |
| **Aprueba** | QA Lead |
| **Formato** | Playwright |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 5-8 días |
| **Frecuencia** | Por sprint |

**Perfil de ejecución:** Requiere dominio de Playwright/Cypress para automatizar flujos browser-based con Page Object Model.  
En VTT: un agente puede generar E2E tests desde user flows y test cases. Es bastante delegable para flujos estándar. Flujos con lógica condicional compleja requieren developer.

**Qué es:** Suite de tests E2E con Playwright que simulan al usuario: abrir browser, navegar a URL, llenar formularios, click buttons, verificar resultados en pantalla y en BD. Cubren los flujos críticos del producto de inicio a fin. Organizados con Page Object Model (POM) para mantenibilidad.

**Para qué sirve:** Los E2E tests verifican que TODO funciona junto: frontend + backend + BD + integraciones. Si el E2E pasa, el usuario puede completar el flujo. Detectan bugs que solo aparecen cuando todas las capas interactúan (CSS que oculta un botón, race condition entre frontend y API).

**Inputs requeridos:**
- `2.6.2` Happy Path Flows — flujos a automatizar
- `5.2.1` Test Cases Document — test cases de flujos críticos
- `5.3.1` Test Environment — ambiente de ejecución

**Dependencias (predecessors):**
- `5.3.1` Test Environment *(obligatorio)*
- `2.6.2` Happy Path Flows *(obligatorio)*
- Frontend y Backend deployed *(obligatorio)*

**Habilita (successors):**
- `5.6.2` E2E Test Results — resultados
- `5.6.3` Critical Path Coverage — medición
- `5.6.4` Visual Regression — screenshots de referencia
- CI/CD gate

**Audiencia:**
- **QA Automation** — mantenimiento de suite
- **QA Lead** — coverage de flujos críticos
- **Product Owner** — confianza en flujos principales

**Secciones esperadas:**
1. Test files por flujo (auth.spec.ts, orders.spec.ts, settings.spec.ts)
2. Page Object Model (POM) por página (LoginPage, DashboardPage, OrderPage)
3. Test data fixtures (users, entities para tests)
4. CI configuration (headless, parallelism, retries)
5. Screenshot/video on failure configurado
6. Test cleanup (data created during tests)

**Criterio de completitud:**
- [ ] Flujos críticos (3-5) automatizados de inicio a fin
- [ ] Page Object Model implementado (selectors centralizados)
- [ ] Tests pasan en CI (headless browser)
- [ ] Screenshot/video on failure configurado
- [ ] Execution time < 10 minutos
- [ ] No flaky tests (reliability > 95%)
- [ ] Cada test es independiente (no depende de orden)

**Anti-patrones:**
- ❌ **E2E para todo:** 200 E2E = 2 horas de ejecución — solo flujos críticos, el resto con unit/integration.
- ❌ **Sin Page Objects:** Selectors duplicados en cada test — cuando la UI cambia, rompe 50 tests.
- ❌ **Flaky tests:** Tests que fallan 20% del tiempo — el equipo los ignora y pierden valor.
- ❌ **Tests sin cleanup:** Test A crea un usuario que hace fallar test B.
- ❌ **Hardcoded waits:** `sleep(5000)` en vez de `waitForSelector` — frágil y lento.

**Template:** `phases/05-testing/deliverables/e2e-test-suite/` *(pendiente)*

---

### 5.6.2 E2E Test Results

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.6 E2E Testing |
| **Responsable** | QA Automation |
| **Ejecuta** | QA Automation |
| **Aprueba** | QA Lead |
| **Formato** | Report |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Automático |
| **Frecuencia** | Por CI run |

**Perfil de ejecución:** Requiere configurar Playwright HTML reporter y CI artifacts.  
En VTT: un agente puede configurar reporting. Es altamente delegable.

**Qué es:** Reporte automático de E2E test execution generado por Playwright: pass/fail por flujo y por step, screenshots de cada paso (para debugging), videos de ejecución completa (opcional), traces para debugging detallado (DOM snapshots, network requests, console logs), y duración por test.

**Para qué sirve:** Cuando un E2E falla, el reporte muestra exactamente qué paso falló con screenshot del estado de la UI, el trace permite inspeccionar el DOM y network requests en ese momento — debugging sin necesidad de reproducir manualmente.

**Inputs requeridos:**
- `5.6.1` E2E Test Suite — ejecutada en CI
- Playwright reporter configurado

**Dependencias (predecessors):**
- `5.6.1` E2E Test Suite *(obligatorio)*

**Habilita (successors):**
- Debugging rápido de E2E failures
- Go/no-go para deploy

**Audiencia:**
- **QA Automation** — debugging de failures
- **Frontend Developer** — debugging de UI issues
- **Tech Lead** — CI results overview

**Secciones esperadas:**
1. Pass/fail summary por flujo
2. Screenshots de cada step (success y failure)
3. Video recordings (opcional, para flujos que fallan)
4. Playwright traces para debugging detallado
5. Duration por test y total
6. Retry results (si retry está configurado)

**Criterio de completitud:**
- [ ] Report generado automáticamente en CI
- [ ] Screenshots on failure capturados
- [ ] Traces accesibles para debugging
- [ ] Accesible como CI artifact (URL compartible)
- [ ] Report parseable (JUnit XML para integraciones)

**Anti-patrones:**
- ❌ **Solo "FAIL" sin contexto:** Sin screenshot ni trace — debugging a ciegas requiere reproducir manualmente.
- ❌ **Traces no guardados:** El report dice "failed" pero no hay trace para investigar.
- ❌ **Reports solo locales:** Solo visibles en la máquina que corrió el pipeline.

**Template:** N/A — generado por Playwright reporter

---

### 5.6.3 Critical Path Coverage

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.6 E2E Testing |
| **Responsable** | QA Automation |
| **Ejecuta** | QA Automation |
| **Aprueba** | QA Lead |
| **Formato** | Métrica |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.25 día |
| **Frecuencia** | Por sprint |

**Perfil de ejecución:** Requiere mapear flujos críticos del producto a E2E tests existentes.  
En VTT: un agente puede calcular coverage comparando flujos vs tests. Es altamente delegable.

**Qué es:** Métrica que indica qué porcentaje de los flujos críticos del producto están cubiertos por E2E tests automatizados: tabla de flujos críticos con status (automatizado ✅ / no automatizado ❌), gap analysis, y plan para cubrir los faltantes. Target: 100% de flujos críticos cubiertos.

**Para qué sirve:** Asegura que los flujos que generan revenue o que si fallan causan mayor impacto están protegidos. Si el flujo de pago no tiene E2E, un CSS change puede romperlo sin que nadie lo detecte hasta que un usuario intenta pagar.

**Inputs requeridos:**
- `2.6.2` Happy Path Flows — flujos críticos definidos
- `5.6.1` E2E Test Suite — tests existentes

**Dependencias (predecessors):**
- `5.6.1` E2E Test Suite *(obligatorio)*
- `2.6.2` Happy Path Flows *(obligatorio)*

**Habilita (successors):**
- Plan para cubrir flujos faltantes
- Decisión de qué automatizar en el próximo sprint

**Audiencia:**
- **QA Lead** — oversight de coverage
- **Product Owner** — flujos críticos protegidos

**Secciones esperadas:**
1. Lista de flujos críticos (del Product Owner / Happy Path Flows)
2. Coverage table (flujo, automatizado ✅/❌, test file, notas)
3. Coverage % (automatizados / total)
4. Gap analysis (flujos no cubiertos con justificación)
5. Plan para cerrar gaps (prioridad, sprint, esfuerzo)

**Criterio de completitud:**
- [ ] 100% de flujos críticos listados
- [ ] Coverage % calculado
- [ ] Gaps identificados con prioridad
- [ ] Plan de mejora para gaps
- [ ] Actualizado por sprint

**Anti-patrones:**
- ❌ **Flujo de pago sin E2E:** El flujo que genera revenue no está protegido — riesgo inaceptable.
- ❌ **Coverage metric sin acción:** "70% coverage" sin plan para el 30% restante.
- ❌ **"Todo es critical":** 50 flujos marcados como critical — priorizar los realmente críticos (3-5).

**Template:** `phases/05-testing/deliverables/critical-path-coverage.md` *(pendiente)*

---

### 5.6.4 Visual Regression

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.6 E2E Testing |
| **Responsable** | QA Automation |
| **Ejecuta** | QA Automation |
| **Aprueba** | QA Lead |
| **Formato** | Screenshots |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días setup |
| **Frecuencia** | Por CI run |

**Perfil de ejecución:** Requiere configurar visual comparison (Playwright toMatchSnapshot, Chromatic, Percy).  
En VTT: un agente puede configurar visual regression testing. Es bastante delegable.

**Qué es:** Tests que comparan screenshots de la UI actual vs screenshots de referencia (baseline) pixel-by-pixel: detectan cambios visuales no intencionados que un test funcional no detecta (CSS change que rompe layout de otra página, spacing changes, font changes, color changes). Cada comparison genera un diff visual (baseline vs actual vs difference highlighted).

**Para qué sirve:** Un CSS change en un componente compartido puede romper visualmente 10 páginas que lo usan. Sin visual regression, estos cambios pasan desapercibidos en code review (el reviewer no ve las 10 páginas afectadas). Con visual regression, cualquier cambio visual genera un diff visible que alguien debe aprobar o rechazar.

**Inputs requeridos:**
- `5.6.1` E2E Test Suite — screenshots capturados durante E2E runs
- Baseline screenshots (referencia aprobada)
- `4.4.12` Storybook — Chromatic para component-level regression (si aplica)

**Dependencias (predecessors):**
- `5.6.1` E2E Test Suite *(obligatorio)* — captura screenshots
- Baselines generados y aprobados

**Habilita (successors):**
- Detección automática de regresiones visuales
- UI quality gate en CI

**Audiencia:**
- **QA Automation** — review de diffs
- **UI Designer** — validación de que la UI no cambió inesperadamente
- **Frontend Developer** — impacto visual de sus cambios

**Secciones esperadas:**
1. Tool configurada (Playwright toMatchSnapshot, Chromatic, Percy)
2. Baseline screenshots generados (páginas principales, estados clave)
3. Diff threshold configurado (% de píxeles diferentes aceptable)
4. Review process (quién aprueba/rechaza diffs)
5. Update baselines process (cómo actualizar cuando el cambio es intencional)
6. CI integration (fail si diff > threshold sin aprobación)

**Criterio de completitud:**
- [ ] Baselines generados para páginas principales
- [ ] Comparison automática en CI
- [ ] Diff threshold configurado (típico: 0.1-0.5%)
- [ ] Review process definido (quién aprueba diffs)
- [ ] Update baselines process documentado
- [ ] Anti-aliasing y font rendering differences manejados

**Anti-patrones:**
- ❌ **Threshold 0%:** Cualquier diferencia sub-pixel falla — demasiados false positives por anti-aliasing.
- ❌ **Sin review process:** Diffs auto-aprobados — pierde el propósito de detección.
- ❌ **Baselines nunca actualizados:** Cambios intencionales generan diffs permanentes que se ignoran.
- ❌ **Solo desktop:** Sin screenshots mobile — regresiones mobile no detectadas.

**Template:** `phases/05-testing/deliverables/visual-regression/` *(pendiente)*

---

### 5.6.5 E2E Documentation

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.6 E2E Testing |
| **Responsable** | QA Automation |
| **Ejecuta** | QA Automation |
| **Aprueba** | QA Lead |
| **Formato** | MD |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez + actualizaciones |

**Perfil de ejecución:** Requiere documentar cómo escribir, correr, y debuggear E2E tests.  
En VTT: un agente puede generar la documentación completa. Es altamente delegable.

**Qué es:** Guía de E2E testing del proyecto: cómo instalar dependencias, cómo correr E2E localmente (headed y headless), cómo agregar un nuevo test (con Page Object Model), cómo debuggear tests fallidos (traces, headed mode, slowMo, pause), cómo actualizar baselines de visual regression, y convenciones del proyecto.

**Para qué sirve:** Un developer nuevo puede escribir y correr E2E tests siguiendo esta guía sin ayuda de QA. Sin docs, solo QA Automation sabe cómo funcionan — bus factor de 1.

**Inputs requeridos:**
- `5.6.1` E2E Test Suite — tests a documentar
- Playwright configuration

**Dependencias (predecessors):**
- `5.6.1` E2E Test Suite *(obligatorio)*

**Habilita (successors):**
- Todo el equipo puede contribuir E2E tests
- Onboarding de QA nuevos

**Audiencia:**
- **Todo el equipo técnico** — autonomía para E2E
- **New QA Engineers** — onboarding

**Secciones esperadas:**
1. Setup (instalar, configurar, prerequisitos)
2. Correr tests (npm test:e2e, headed vs headless, single test)
3. Agregar nuevo test (step-by-step con POM)
4. Page Object Model conventions (cómo crear un Page Object)
5. Debugging (traces, headed mode, slowMo, pause(), Playwright Inspector)
6. Visual regression (cómo actualizar baselines)
7. CI (cómo interpretar CI results, dónde ver artifacts)
8. Troubleshooting (problemas comunes y soluciones)

**Criterio de completitud:**
- [ ] Setup reproducible sin ayuda
- [ ] How-to para correr, agregar, y debuggear
- [ ] POM conventions documentadas con ejemplo
- [ ] Troubleshooting de 3+ problemas comunes
- [ ] Probado por developer que no escribió la guía

**Anti-patrones:**
- ❌ **Sin docs:** Solo QA Automation sabe correr E2E — si se va, nadie puede.
- ❌ **Docs desactualizadas:** Comandos que ya no funcionan — peor que no tener docs.
- ❌ **Sin debugging guide:** Developer ve "test failed" y no sabe cómo investigar.

**Template:** `phases/05-testing/deliverables/e2e-docs.md` *(pendiente)*

---

## Tabla resumen — Fase 5.6

| Deliverable | Responsable | Delegable VTT |
|-------------|-------------|---------------|
| 5.6.1 E2E Test Suite | QA Automation | 🔶 Parcial — scaffolding sí, flujos complejos requieren juicio |
| 5.6.2 E2E Test Results | QA Automation | ✅ — auto-generado por Playwright |
| 5.6.3 Critical Path Coverage | QA Automation | ✅ — calculable |
| 5.6.4 Visual Regression | QA Automation | ✅ — configuración delegable |
| 5.6.5 E2E Documentation | QA Automation | ✅ — documentación delegable |
