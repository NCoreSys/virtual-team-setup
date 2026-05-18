# DICCIONARIO DE DELIVERABLES — FASE 5.5: INTEGRATION TESTING

**Versión:** 1.1  
**Fecha:** 2026-05-14  
**Fase:** 5 — Testing  
**Subfase:** 5.5 — Integration Testing  
**Total deliverables:** 4  
**Responsable de subfase:** QA Automation  
**Aprueba:** QA Lead

---

## Contexto de la subfase

Integration Testing verifica que los componentes del sistema funcionan correctamente juntos: frontend → API → BD, y sistema → servicios externos. Complementa los unit tests (piezas aisladas) y los E2E tests (flujos completos de usuario) verificando las "costuras" entre componentes.

---

### 5.5.1 Integration Test Suite

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.5 Integration Testing |
| **Responsable** | QA Automation |
| **Ejecuta** | QA Automation |
| **Aprueba** | QA Lead |
| **Formato** | Jest |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 3-5 días |
| **Frecuencia** | Por sprint |

**Perfil de ejecución:** Requiere automatización de tests API y de integración entre componentes.  
En VTT: un agente puede generar integration tests desde OpenAPI spec y request/response examples. Es altamente delegable.

**Qué es:** Suite automatizada de tests que verifican la integración entre componentes: API tests end-to-end (HTTP request → controller → service → repository → DB → response), integración frontend-backend (API client → endpoints), e integración con servicios externos (usando mocks/stubs). Complementa los integration tests del developer (4.3.10) con perspectiva de QA.

**Para qué sirve:** Un service puede pasar unit tests pero fallar cuando el controller le pasa datos en formato inesperado, o cuando la query del repository no incluye un JOIN necesario. Los integration tests detectan estos problemas de "costura" entre capas.

**Inputs requeridos:**
- `3B.4.1` OpenAPI Spec — contratos a verificar
- `4.3.10` Integration Tests — tests del developer como base
- `5.3.1` Test Environment — ambiente de ejecución
- `3B.4.3` Request/Response Examples — fixtures

**Dependencias (predecessors):**
- `4.3.10` Integration Tests *(obligatorio)* — base existente
- `5.3.1` Test Environment *(obligatorio)*

**Habilita (successors):**
- `5.5.2` Integration Test Results — resultados de ejecución
- `5.5.4` Integration Coverage — medición de coverage
- CI/CD gate — integration tests como check

**Audiencia:**
- **QA Automation** — mantenimiento de suite
- **Tech Lead** — coverage de integración
- **Backend Developer** — debugging de failures

**Secciones esperadas:**
1. Test files organizados por módulo/feature
2. API integration tests (CRUD por resource)
3. Cross-layer tests (controller → service → repository → DB)
4. External service tests (con mocks)
5. Test data setup/teardown
6. CI configuration para ejecución automática

**Criterio de completitud:**
- [ ] Tests para todos los endpoints principales (CRUD)
- [ ] Happy path y error paths cubiertos
- [ ] Auth tests (con/sin token, expirado, forbidden)
- [ ] Validation tests (inputs inválidos → 400)
- [ ] Tests pasan en CI consistentemente (no flaky)
- [ ] External services mockeados en CI
- [ ] Execution time < 5 minutos
- [ ] Tests aislados (no dependen de orden)

**Anti-patrones:**
- ❌ **Tests lentos:** Suite de 30 min — se ignora o solo corre antes de release.
- ❌ **Tests flaky:** Fallan aleatoriamente — equipo pierde confianza y los ignora.
- ❌ **Depender de servicios externos en CI:** Test falla porque sandbox de Stripe caído — usar mocks.
- ❌ **Tests que dependen de orden:** Test B falla si test A no corrió — cada test debe ser independiente.
- ❌ **Test DB compartida sin cleanup:** Data de un test contamina otro — false positives/negatives.

**Template:** `phases/05-testing/deliverables/integration-test-suite/` *(pendiente)*

---

### 5.5.2 Integration Test Results

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.5 Integration Testing |
| **Responsable** | QA Automation |
| **Ejecuta** | QA Automation |
| **Aprueba** | QA Lead |
| **Formato** | Report |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Automático |
| **Frecuencia** | Por CI run |

**Perfil de ejecución:** Requiere configurar reporting automático de test results en CI.  
En VTT: un agente puede configurar Jest reporters y CI artifacts. Es altamente delegable.

**Qué es:** Reporte automático de resultados de la integration test suite: pass/fail por test con duración, errores con stack trace y request/response context, y trend de resultados over time. Generado automáticamente en CI como artifact descargable.

**Para qué sirve:** Visibilidad inmediata de si las integraciones funcionan después de cada push/merge. Cuando un test falla, el reporte muestra exactamente qué request se envió, qué response se recibió, y dónde falló la assertion — debugging rápido.

**Inputs requeridos:**
- `5.5.1` Integration Test Suite — ejecutada en CI

**Dependencias (predecessors):**
- `5.5.1` Integration Test Suite *(obligatorio)*

**Habilita (successors):**
- Go/no-go para merge/deploy
- `5.5.4` Integration Coverage — data de coverage

**Audiencia:**
- **Todo el equipo técnico** — CI results
- **Tech Lead** — overview de health de integraciones

**Secciones esperadas:**
1. Pass/fail summary (total, passed, failed, skipped)
2. Failed tests con error details (assertion, expected vs actual)
3. Request/response context en failures (qué se envió, qué se recibió)
4. Duration por test y total
5. Trend vs CI run anterior

**Criterio de completitud:**
- [ ] Report generado automáticamente en cada CI run
- [ ] Failed tests incluyen error details con contexto
- [ ] Accesible como CI artifact
- [ ] Trend tracking configurado (si CI lo soporta)
- [ ] Formato parseable (JUnit XML para integraciones)

**Anti-patrones:**
- ❌ **Results solo en console log:** Nadie scrollea 500 líneas de log — generar report artifact.
- ❌ **Failures sin contexto:** "AssertionError: expected 400 to equal 200" sin mostrar qué request lo causó.
- ❌ **Report no accesible:** Solo visible para quien ejecutó el pipeline — debe ser artifact público.

**Template:** N/A — generado por CI/Jest reporter

---

### 5.5.3 API Contract Tests

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.5 Integration Testing |
| **Responsable** | QA Automation |
| **Ejecuta** | QA Automation |
| **Aprueba** | QA Lead |
| **Formato** | Jest |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Una vez + por endpoint nuevo |

**Perfil de ejecución:** Requiere implementar contract testing que verifica que la API cumple el OpenAPI spec exactamente.  
En VTT: un agente puede generar contract tests desde OpenAPI spec usando jest-openapi o schemathesis. Es altamente delegable.

**Qué es:** Tests que verifican que la API implementada cumple exactamente con el OpenAPI spec: response schemas match (todos los campos presentes, tipos correctos, campos extra no permitidos), status codes correctos por caso (200 para success, 404 para not found, 422 para validation), y headers requeridos presentes (Content-Type, pagination headers).

**Para qué sirve:** Detecta drift entre el spec y la implementación. Si el spec dice `GET /users` retorna `{ name: string }` pero la implementación retorna `{ userName: string }`, el contract test falla. El frontend confía en el contrato — si la API no lo cumple, el frontend se rompe.

**Inputs requeridos:**
- `3B.4.1` OpenAPI Spec — contrato a verificar
- `4.3.1` API Endpoints — implementación a testear
- Library: jest-openapi, schemathesis, o Pact

**Dependencias (predecessors):**
- `3B.4.1` OpenAPI Spec *(obligatorio)* — el contrato
- `4.3.1` API Endpoints *(obligatorio)* — la implementación

**Habilita (successors):**
- Confianza en que API matches spec
- Frontend puede desarrollar contra el contrato con confianza

**Audiencia:**
- **QA Automation** — mantenimiento
- **Frontend Developer** — confianza en contrato
- **Backend Developer** — detección de drift

**Secciones esperadas:**
1. Contract tests por endpoint (request → verify response schema)
2. Schema validation (response body matches OpenAPI schema exactly)
3. Status code validation (cada caso retorna el status correcto)
4. Header validation (Content-Type, pagination)
5. Negative contract tests (invalid input → error response schema)

**Criterio de completitud:**
- [ ] Todos los endpoints del OpenAPI spec tienen contract test
- [ ] Response schemas validados (campos, tipos, required)
- [ ] Status codes validados por caso
- [ ] Error response schema validado
- [ ] Tests pasan en CI
- [ ] Spec version referenciado en tests

**Anti-patrones:**
- ❌ **Spec y código divergen sin detección:** Sin contract tests, la divergencia se descubre cuando el frontend se rompe en producción.
- ❌ **Contract test que no valida schema:** Solo verificar status 200 sin validar el body — no es contract testing.
- ❌ **Spec desactualizado:** Contract tests pasan pero el spec no refleja la realidad — actualizar spec primero.

**Template:** `phases/05-testing/deliverables/contract-tests/` *(pendiente)*

---

### 5.5.4 Integration Coverage

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.5 Integration Testing |
| **Responsable** | QA Automation |
| **Ejecuta** | QA Automation |
| **Aprueba** | QA Lead |
| **Formato** | Métrica |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.25 día |
| **Frecuencia** | Por sprint |

**Perfil de ejecución:** Requiere medir qué % de endpoints y flujos de integración están cubiertos por tests automatizados.  
En VTT: un agente puede calcular coverage comparando endpoints testeados vs endpoints totales. Es altamente delegable.

**Qué es:** Métrica que indica la cobertura de integration tests: endpoints testeados vs total de endpoints del OpenAPI spec (tabla con ✅/❌ por endpoint), flujos de integración cubiertos vs total, y gap analysis con plan para cerrar gaps.

**Para qué sirve:** Sin esta métrica, "tenemos integration tests" es vago. 10 tests para 100 endpoints = 10% coverage — insuficiente. La métrica identifica exactamente qué endpoints no están cubiertos y prioriza cuáles cubrir primero (por criticidad).

**Inputs requeridos:**
- `5.5.1` Integration Test Suite — tests existentes
- `3B.4.2` Endpoints List — total de endpoints

**Dependencias (predecessors):**
- `5.5.1` Integration Test Suite *(obligatorio)*
- `3B.4.2` Endpoints List *(obligatorio)*

**Habilita (successors):**
- Plan para cerrar gaps de coverage
- Sprint planning — items de testing

**Audiencia:**
- **QA Lead** — oversight de coverage
- **Tech Lead** — gaps de riesgo

**Secciones esperadas:**
1. Coverage summary (endpoints cubiertos / total = %)
2. Coverage por módulo (tabla: módulo, endpoints, cubiertos, %)
3. Endpoint-level detail (tabla: endpoint, method, testeado ✅/❌)
4. Gap analysis (endpoints no cubiertos, prioridad)
5. Plan para cerrar gaps (cuáles cubrir en el próximo sprint)

**Criterio de completitud:**
- [ ] Coverage calculado y documentado
- [ ] Gaps identificados con prioridad
- [ ] Target definido (e.g., ≥80% de endpoints)
- [ ] Plan de mejora si < target
- [ ] Actualizado por sprint

**Anti-patrones:**
- ❌ **Coverage desconocido:** "Tenemos tests" sin saber cuánto cubren — ceguera.
- ❌ **Coverage sin priorización:** 80% coverage pero el endpoint de pagos no está cubierto — la priorización importa más que el número.
- ❌ **Coverage metric sin acción:** Reportar 60% y no hacer nada al respecto.

**Template:** `phases/05-testing/deliverables/integration-coverage.md` *(pendiente)*

---

## Tabla resumen — Fase 5.5

| Deliverable | Responsable | Delegable VTT |
|-------------|-------------|---------------|
| 5.5.1 Integration Test Suite | QA Automation | ✅ — generables desde OpenAPI spec |
| 5.5.2 Integration Test Results | QA Automation | ✅ — auto-generado por CI |
| 5.5.3 API Contract Tests | QA Automation | ✅ — generables desde OpenAPI spec |
| 5.5.4 Integration Coverage | QA Automation | ✅ — calculable automáticamente |
