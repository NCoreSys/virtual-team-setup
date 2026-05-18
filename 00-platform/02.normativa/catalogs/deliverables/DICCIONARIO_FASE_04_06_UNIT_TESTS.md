# DICCIONARIO DE DELIVERABLES — FASE 4.6: UNIT TESTS

**Versión:** 1.0  
**Fecha:** 2026-05-14  
**Fase:** 4 — Development  
**Subfase:** 4.6 — Unit Tests  
**Total deliverables:** 7  
**Responsable de subfase:** QA Automation  
**Aprueba:** QA Lead

---

## Contexto de la subfase

Unit Tests consolida y complementa los tests escritos durante desarrollo (4.3.9, 4.3.10, 4.4.10, 4.4.11) con una visión de QA: coverage reports, mock factories reutilizables, fixtures estandarizados, y utilidades de testing compartidas. Mientras los developers escriben tests por feature, QA asegura que el coverage total es adecuado y las prácticas de testing son consistentes.

**Prerequisitos de subfase:**
- Backend Development (4.3) — código backend testeable
- Frontend Development (4.4) — código frontend testeable

**Entrega de subfase:**
- Coverage ≥80%, factories y fixtures reutilizables, y test infrastructure sólida

---

### 4.6.1 Unit Tests BE

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.6 Unit Tests |
| **Responsable** | QA Automation |
| **Ejecuta** | QA Automation / Backend Developer |
| **Aprueba** | QA Lead |
| **Formato** | Jest |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Continuo |
| **Frecuencia** | Por sprint |

**Perfil de ejecución:** Requiere experiencia en testing backend: mocking de repositories, testing de business logic, y assertion patterns.  
En VTT: un agente puede generar tests adicionales para cubrir gaps de coverage. Es bastante delegable para tests de CRUD y validation.

**Qué es:** Complemento a los tests escritos por developers (4.3.9): QA Automation revisa el coverage, identifica gaps (branches no cubiertas, edge cases no testeados), y agrega tests para alcanzar ≥80% coverage. Foco en: business rules complejas, edge cases, boundary values, y error paths que los developers no cubrieron.

**Para qué sirve:** Los developers testean lo que construyeron — QA testea lo que podría romperse. QA tiene una perspectiva diferente: "¿qué pasa si el input es null?", "¿qué pasa si hay 0 resultados?", "¿qué pasa si se llama 2 veces?". Esta perspectiva complementaria cierra gaps de coverage.

**Inputs requeridos:**
- `4.3.9` Unit Tests BE — tests existentes del developer
- `4.6.3` Test Coverage Report — gaps identificados
- `2.5.3` Validation Rules — edge cases de validación

**Dependencias (predecessors):**
- `4.3.9` Unit Tests BE *(obligatorio)* — tests existentes
- `4.6.3` Test Coverage Report *(obligatorio)* — gaps a cubrir

**Habilita (successors):**
- `4.6.4` Coverage ≥80% — target alcanzado

**Audiencia:**
- **QA Automation** — escribe tests complementarios
- **Backend Developer** — mantiene tests
- **Tech Lead** — verifica coverage

**Secciones esperadas:**
1. Tests complementarios por service (edge cases, boundary values)
2. Tests de error paths no cubiertos
3. Tests de concurrencia (si aplica)
4. Tests de validación boundary (min, max, empty, null, overflow)

**Criterio de completitud:**
- [ ] Gaps de coverage identificados y cubiertos
- [ ] Edge cases principales testeados
- [ ] Boundary values testeados (min, max, empty, null)
- [ ] Error paths testeados
- [ ] Coverage backend ≥80%

**Anti-patrones:**
- ❌ **Tests solo para subir coverage:** Tests sin assertions significativas — falsa seguridad.
- ❌ **Duplicar tests del developer:** QA re-testea lo que el dev ya testeó en vez de cubrir gaps.
- ❌ **Tests frágiles:** Tests que fallan con cualquier refactor — testean implementación, no comportamiento.

**Template:** `phases/04-development/deliverables/unit-tests-be-qa/` *(pendiente)*

---

### 4.6.2 Unit Tests FE

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.6 Unit Tests |
| **Responsable** | QA Automation |
| **Ejecuta** | QA Automation / Frontend Developer |
| **Aprueba** | QA Lead |
| **Formato** | Jest / Vitest |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Continuo |
| **Frecuencia** | Por sprint |

**Perfil de ejecución:** Requiere testing de React: Testing Library, user events, async behavior.  
En VTT: un agente puede generar tests de componentes para cubrir gaps. Es bastante delegable.

**Qué es:** Complemento a los tests frontend del developer (4.4.10, 4.4.11): QA agrega tests para cubrir gaps de coverage en hooks, utils, componentes, y pages. Foco en: edge cases de UI (texto largo, listas vacías, errores de red), accesibilidad (keyboard navigation funciona), y responsive behavior.

**Para qué sirve:** Misma lógica que 4.6.1 pero para frontend: QA complementa la perspectiva del developer con tests de edge cases, accesibilidad, y escenarios que el developer no anticipó.

**Inputs requeridos:**
- `4.4.10` Unit Tests FE — tests existentes
- `4.4.11` Component Tests — tests existentes
- `4.6.3` Test Coverage Report — gaps

**Dependencias (predecessors):**
- `4.4.10` Unit Tests FE *(obligatorio)*
- `4.6.3` Test Coverage Report *(obligatorio)*

**Habilita (successors):**
- `4.6.4` Coverage ≥80%

**Audiencia:**
- **QA Automation** — escribe tests
- **Frontend Developer** — mantiene tests

**Secciones esperadas:**
1. Tests de componentes con edge cases (texto largo, listas vacías)
2. Tests de accesibilidad (keyboard nav, ARIA)
3. Tests de hooks con edge cases
4. Tests de error states y loading states

**Criterio de completitud:**
- [ ] Gaps de coverage cubiertos
- [ ] Edge cases de UI testeados
- [ ] Coverage frontend ≥80%

**Anti-patrones:**
- ❌ **Snapshot tests masivos:** 100 snapshots que se auto-aprueban — no testean nada.
- ❌ **Tests de implementación:** Verificar que se llamó `useState` — no es behavior testing.

**Template:** `phases/04-development/deliverables/unit-tests-fe-qa/` *(pendiente)*

---

### 4.6.3 Test Coverage Report

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.6 Unit Tests |
| **Responsable** | QA Automation |
| **Ejecuta** | QA Automation |
| **Aprueba** | QA Lead |
| **Formato** | HTML |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Automático (configuración 0.25 día) |
| **Frecuencia** | Por CI run (automático) |

**Perfil de ejecución:** Requiere configurar coverage reporting en Jest/Vitest con thresholds.  
En VTT: un agente puede configurar coverage reporting y thresholds. Es altamente delegable.

**Qué es:** Reporte de cobertura de tests generado automáticamente por Jest/Vitest: porcentaje de líneas, branches, funciones, y statements cubiertos por tests. Incluye: reporte HTML navegable (qué líneas están cubiertas, cuáles no), resumen por archivo, y trend over time. Configurado como step del CI pipeline.

**Para qué sirve:** Sin coverage report, nadie sabe si los tests cubren el 20% o el 90% del código. El reporte identifica: archivos sin tests, branches no cubiertas (if/else donde solo se testea el if), y funciones nunca ejecutadas en tests. Es la guía para saber dónde agregar tests.

**Inputs requeridos:**
- Tests existentes (4.3.9, 4.4.10, 4.4.11, 4.6.1, 4.6.2)
- Jest/Vitest configuration

**Dependencias (predecessors):**
- Tests existentes *(obligatorio)*

**Habilita (successors):**
- `4.6.1` y `4.6.2` — identifica gaps a cubrir
- `4.6.4` Coverage ≥80% — medición del target

**Audiencia:**
- **QA Automation** — identifica gaps
- **Tech Lead** — oversight de calidad
- **Backend/Frontend Developer** — saber qué cubrir

**Secciones esperadas:**
1. Coverage summary (lines, branches, functions, statements — %)
2. Per-file coverage breakdown
3. Uncovered lines highlighted
4. Trend over time (si CI lo soporta)
5. Thresholds configurados (fail CI si < 80%)

**Criterio de completitud:**
- [ ] Coverage report generado automáticamente en CI
- [ ] Reporte HTML accesible (artifact del CI o deployed)
- [ ] Thresholds configurados (CI falla si < target)
- [ ] Per-file breakdown disponible
- [ ] Configurado para backend Y frontend

**Anti-patrones:**
- ❌ **Coverage sin thresholds:** El reporte existe pero nadie lo mira — no enforce el target.
- ❌ **Coverage solo de líneas:** 80% de líneas pero 40% de branches — los if/else no se testean.
- ❌ **Coverage report solo local:** Cada developer corre coverage localmente pero no hay visibilidad en CI.

**Template:** `phases/04-development/deliverables/coverage-config.js` *(pendiente)*

---

### 4.6.4 Coverage ≥80%

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.6 Unit Tests |
| **Responsable** | QA Automation |
| **Ejecuta** | Todo el equipo de desarrollo |
| **Aprueba** | QA Lead |
| **Formato** | Métrica |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Continuo |
| **Frecuencia** | Continua |

**Perfil de ejecución:** Requiere disciplina de equipo para mantener coverage sobre el threshold.  
En VTT: un agente puede generar tests para subir coverage. Es bastante delegable para código CRUD.

**Qué es:** Target de cobertura mínima del 80% de líneas y branches en backend Y frontend. No es un deliverable "de una vez" — es un gate que se verifica en cada CI run. Si un PR baja el coverage debajo de 80%, el CI falla y el PR no se puede mergear.

**Para qué sirve:** 80% es el sweet spot: suficiente para tener confianza en refactoring y detección de regresiones, sin la inversión exponencial de llegar a 95%+ (donde cada % adicional cuesta 10x más esfuerzo). El gate en CI asegura que el coverage nunca baja — solo sube.

**Inputs requeridos:**
- `4.6.3` Test Coverage Report — medición actual

**Dependencias (predecessors):**
- `4.6.3` Test Coverage Report *(obligatorio)*

**Habilita (successors):**
- Confianza en refactoring
- CI gate funcional

**Audiencia:**
- **Todo el equipo de desarrollo** — responsabilidad compartida

**Secciones esperadas:**
1. N/A — es una métrica, no un documento
2. Threshold configurado en CI (jest.config: coverageThreshold)
3. Baseline actual documentado
4. Plan para alcanzar 80% si actualmente es menor

**Criterio de completitud:**
- [ ] Coverage de líneas ≥80% en backend
- [ ] Coverage de líneas ≥80% en frontend
- [ ] Coverage de branches ≥70% (branches es más difícil)
- [ ] CI gate configurado (falla si < threshold)
- [ ] Coverage no decrece sprint a sprint

**Anti-patrones:**
- ❌ **Coverage gaming:** Tests sin assertions para subir % — el número sube pero la calidad no.
- ❌ **100% como target:** Testear getters, setters, y código trivial para llegar a 100% — ROI negativo.
- ❌ **Excluir archivos difíciles:** Excluir los archivos complejos del coverage para "llegar a 80%" — lo más importante sin testear.
- ❌ **Coverage baja sin consecuencia:** Threshold configurado pero CI no falla — el threshold es decorativo.

**Template:** N/A — es una configuración en `jest.config.js`

---

### 4.6.5 Mock Factories

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.6 Unit Tests |
| **Responsable** | QA Automation |
| **Ejecuta** | QA Automation / Backend Developer |
| **Aprueba** | QA Lead |
| **Formato** | TypeScript |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez + por entidad nueva |

**Perfil de ejecución:** Requiere crear factories que generan datos de test coherentes y tipados.  
En VTT: un agente puede generar mock factories completas desde los models. Es altamente delegable.

**Qué es:** Funciones factory que generan objetos de test para cada entidad del dominio: `createMockUser()`, `createMockOrder({ status: 'completed' })`. Cada factory: genera datos realistas (Faker), permite overrides parciales (cambiar solo los campos que importan al test), y mantiene relaciones coherentes (un order siempre tiene un user válido).

**Para qué sirve:** Sin factories, cada test crea sus datos manualmente: `{ id: 1, name: "Test", email: "test@test.com", ... }` — 10 líneas de setup por test, duplicadas en 50 tests. Las factories reducen el setup a `const user = createMockUser()` — una línea, datos realistas, tipado, coherente.

**Inputs requeridos:**
- `4.3.3` Models — entidades a mockear
- `3B.3.3` Table Specifications — campos y constraints
- Faker.js para datos realistas

**Dependencias (predecessors):**
- `4.3.3` Models *(obligatorio)* — estructura de entidades

**Habilita (successors):**
- `4.6.1` Unit Tests BE — factories usadas en tests
- `4.6.2` Unit Tests FE — factories usadas en tests
- `4.3.9` Unit Tests BE — factories usadas por developers
- `4.6.6` Test Fixtures — fixtures generados con factories

**Audiencia:**
- **Todo el equipo de desarrollo** — uso en tests

**Secciones esperadas:**
1. Factory por entidad (createMockUser, createMockOrder, createMockProduct)
2. Overrides parciales (createMockUser({ role: 'admin' }))
3. Relaciones (createMockOrder genera un user válido automáticamente)
4. Sequences (IDs incrementales para evitar conflictos)
5. Faker integration para datos realistas

**Criterio de completitud:**
- [ ] Factory por entidad principal
- [ ] Overrides parciales soportados
- [ ] Relaciones entre entidades coherentes
- [ ] TypeScript tipado (factory retorna el tipo correcto)
- [ ] Datos realistas (Faker)
- [ ] Documentadas con ejemplos de uso

**Anti-patrones:**
- ❌ **Datos hardcoded en tests:** `{ id: 1, name: "John" }` en 50 tests — frágil, repetitivo.
- ❌ **Factories sin overrides:** No poder cambiar un campo — tests inflexibles.
- ❌ **Factories con relaciones rotas:** MockOrder con userId que no existe — FK errors en integration tests.

**Template:** `phases/04-development/deliverables/mock-factories/` *(pendiente)*

---

### 4.6.6 Test Fixtures

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.6 Unit Tests |
| **Responsable** | QA Automation |
| **Ejecuta** | QA Automation |
| **Aprueba** | QA Lead |
| **Formato** | TypeScript / JSON |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez + adiciones |

**Perfil de ejecución:** Requiere definir conjuntos de datos fijos para tests que necesitan datos predecibles.  
En VTT: un agente puede generar fixtures desde schemas y examples. Es altamente delegable.

**Qué es:** Conjuntos de datos fijos (no generados aleatoriamente como factories) para tests que requieren datos predecibles: API request/response examples, error responses, paginated responses, y datos de escenarios específicos. Las fixtures son deterministas — siempre devuelven los mismos datos.

**Para qué sirve:** Las factories generan datos aleatorios (buenos para variety testing). Las fixtures son datos fijos (buenos para snapshot testing, integration testing, y tests que verifican valores exactos). Complementan a las factories para cubrir diferentes necesidades de testing.

**Inputs requeridos:**
- `3B.4.3` Request/Response Examples — API fixtures
- `3B.4.5` Error Codes — error fixtures
- `4.6.5` Mock Factories — factories como base

**Dependencias (predecessors):**
- `3B.4.3` Request/Response Examples *(recomendado)*

**Habilita (successors):**
- Tests que requieren datos predecibles

**Audiencia:**
- **Todo el equipo de desarrollo** — uso en tests

**Secciones esperadas:**
1. API request fixtures (valid request bodies)
2. API response fixtures (success, error, paginated)
3. Entity fixtures (user fixture, order fixture con datos conocidos)
4. Error fixtures (validation error, not found, unauthorized)

**Criterio de completitud:**
- [ ] Fixtures para API requests/responses principales
- [ ] Fixtures para error responses estándar
- [ ] Fixtures tipados (TypeScript)
- [ ] Organizados por entidad/contexto
- [ ] Documentados con uso esperado

**Anti-patrones:**
- ❌ **Fixtures enormes:** Archivos JSON de 500 líneas — difícil de mantener.
- ❌ **Fixtures duplicadas:** Mismos datos en 5 archivos — una sola fuente.
- ❌ **Fixtures desactualizadas:** Schema cambió pero fixtures no — tests pasan con datos incorrectos.

**Template:** `phases/04-development/deliverables/test-fixtures/` *(pendiente)*

---

### 4.6.7 Test Utils

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.6 Unit Tests |
| **Responsable** | QA Automation |
| **Ejecuta** | QA Automation |
| **Aprueba** | QA Lead |
| **Formato** | TypeScript |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez + adiciones |

**Perfil de ejecución:** Requiere crear utilidades que simplifiquen el setup y assertions de tests.  
En VTT: un agente puede generar test utils. Es altamente delegable.

**Qué es:** Utilidades compartidas para testing: helpers de setup (createTestApp, createTestDB, authenticateTestUser), custom assertions (expectApiError, expectPaginatedResponse), wrappers de Testing Library (renderWithProviders — render con store, router, theme provider), y cleanup utilities.

**Para qué sirve:** Sin test utils, cada test repite el mismo boilerplate: crear la app de test, autenticar un usuario, wrappear en providers. Las test utils reducen el setup de 20 líneas a 1: `const { api } = await createTestContext()`.

**Inputs requeridos:**
- Testing framework (Jest, Vitest)
- App configuration para test context
- `4.4.5` State Management — providers para wrapper

**Dependencias (predecessors):**
- Tests existentes que revelan la necesidad de utils

**Habilita (successors):**
- Todos los tests los consumen — menor boilerplate

**Audiencia:**
- **Todo el equipo de desarrollo** — uso en tests

**Secciones esperadas:**
1. Setup utils (createTestApp, createTestDB, seedTestDB)
2. Auth utils (authenticateTestUser, createTestToken)
3. Render utils (renderWithProviders — React con store/router/theme)
4. Assertion utils (expectApiError, expectPaginated, expectSorted)
5. Cleanup utils (clearTestDB, resetMocks)

**Criterio de completitud:**
- [ ] Setup de test context en 1-2 líneas (no 20)
- [ ] Auth helper para tests que requieren usuario autenticado
- [ ] Render wrapper con providers para React tests
- [ ] Custom assertions para patterns frecuentes
- [ ] Documentados con ejemplos de uso

**Anti-patrones:**
- ❌ **20 líneas de setup en cada test:** Boilerplate repetido — extraer a utils.
- ❌ **Test utils con side effects ocultos:** Utils que modifican estado global sin documentar.
- ❌ **Over-abstraction:** Utils tan abstractos que nadie entiende qué hacen.

**Template:** `phases/04-development/deliverables/test-utils/` *(pendiente)*

---

## Tabla resumen de ejecutores — Fase 4.6 Unit Tests

| Deliverable | Responsable | Ejecuta | Delegable VTT |
|-------------|-------------|---------|---------------|
| 4.6.1 Unit Tests BE | QA Automation | QA Automation / Backend Dev | 🔶 Parcial — puede generar tests de gaps, edge cases complejos requieren juicio |
| 4.6.2 Unit Tests FE | QA Automation | QA Automation / Frontend Dev | 🔶 Parcial — puede generar tests de gaps |
| 4.6.3 Test Coverage Report | QA Automation | QA Automation | ✅ — puede configurar coverage reporting |
| 4.6.4 Coverage ≥80% | QA Automation | Todo el equipo | 🔶 Parcial — puede generar tests para subir coverage, target es del equipo |
| 4.6.5 Mock Factories | QA Automation | QA Automation / Backend Dev | ✅ — puede generar factories desde models |
| 4.6.6 Test Fixtures | QA Automation | QA Automation | ✅ — puede generar fixtures desde schemas |
| 4.6.7 Test Utils | QA Automation | QA Automation | ✅ — puede generar test utilities |

---

## Siguiente archivo

**Próximo:** `DICCIONARIO_FASE_04_07_TECHNICAL_DOCUMENTATION.md` — 8 deliverables (4.7.1 a 4.7.8)
