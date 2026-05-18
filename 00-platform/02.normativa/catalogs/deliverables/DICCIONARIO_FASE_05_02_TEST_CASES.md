# DICCIONARIO DE DELIVERABLES — FASE 5.2: TEST CASES

**Versión:** 1.0  
**Fecha:** 2026-05-14  
**Fase:** 5 — Testing  
**Subfase:** 5.2 — Test Cases  
**Total deliverables:** 4  
**Responsable de subfase:** QA Engineer  
**Aprueba:** QA Lead

---

## Contexto de la subfase

Test Cases documenta qué se testea y cómo: cada caso de prueba tiene pasos reproducibles, datos de entrada, y resultado esperado. Son la especificación ejecutable del testing — si un test case pasa, la funcionalidad funciona como fue diseñada.

**Prerequisitos de subfase:**
- Test Plan (5.1.1) — qué testear
- Use Cases (2.3.4) — funcionalidades a cubrir
- API Spec (3B.4.1) — contratos de API

**Entrega de subfase:**
- Test cases documentados, identificados, con datos y resultados esperados

---

### 5.2.1 Test Cases Document

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.2 Test Cases |
| **Responsable** | QA Engineer |
| **Ejecuta** | QA Engineer |
| **Aprueba** | QA Lead |
| **Formato** | MD/Excel |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 3-5 días |
| **Frecuencia** | Por sprint (nuevos test cases por feature) |

**Perfil de ejecución:** Requiere traducir use cases y user stories en test cases con pasos, datos, y expected results.  
En VTT: un agente puede generar test cases desde use cases, API specs, y business rules. Es altamente delegable. Necesita brief con: use cases, acceptance criteria, y business rules.

**Qué es:** Documento con todos los test cases del proyecto, organizados por módulo/feature. Cada test case tiene: ID, título, precondiciones, pasos step-by-step, datos de entrada, resultado esperado, prioridad (critical/high/medium/low), y tipo (positive/negative/boundary/edge case). Cubre happy paths, error paths, y edge cases.

**Para qué sirve:** Los test cases son la definición operativa de "funciona". Si todos los test cases pasan, la funcionalidad cumple los requisitos. Son reproducibles (cualquier QA puede ejecutarlos), trazables (cada TC se relaciona a un use case), y reutilizables (regression testing).

**Inputs requeridos:**
- `2.3.4` Detailed Use Cases — funcionalidad a cubrir
- `2.5.1` Business Rules Document — reglas a validar
- `2.5.3` Validation Rules — validaciones a testear
- `3B.4.3` Request/Response Examples — API test cases
- Acceptance criteria de user stories

**Dependencias (predecessors):**
- `2.3.4` Detailed Use Cases *(obligatorio)*
- `5.1.3` Test Scope *(obligatorio)* — qué está in-scope

**Habilita (successors):**
- `5.4.1` Functional Test Results — ejecución de test cases
- `5.6.1` E2E Test Suite — E2E tests basados en test cases
- `5.10.2` UAT Test Cases — subset para UAT

**Audiencia:**
- **QA Engineer** — ejecución de tests
- **QA Lead** — review de coverage
- **Product Owner** — validación de que se testea lo correcto

**Secciones esperadas:**
1. Índice de test cases por módulo/feature
2. Por test case: ID, título, precondiciones, pasos, datos, expected result, prioridad, tipo
3. Positive test cases (happy path)
4. Negative test cases (invalid inputs, unauthorized access)
5. Boundary test cases (min, max, empty, overflow)
6. Edge cases (concurrent operations, network failure)
7. Cross-reference a use cases (TC → UC mapping)

**Criterio de completitud:**
- [ ] Cada use case tiene al menos 1 positive y 1 negative test case
- [ ] Business rules críticas tienen test cases específicos
- [ ] Boundary values testeados para inputs numéricos y strings
- [ ] Pasos reproducibles (cualquier QA puede ejecutar sin ambigüedad)
- [ ] Expected results claros y verificables
- [ ] Priorizados (critical > high > medium > low)
- [ ] Cross-reference a use cases documentada

**Anti-patrones:**
- ❌ **Solo happy path:** 100% positive tests — no se detectan errores de validación, auth, ni edge cases.
- ❌ **Pasos ambiguos:** "Verificar que funciona" — ¿qué significa "funciona"?
- ❌ **Sin datos de test:** "Ingresar un email" — ¿cuál email? El dato importa.
- ❌ **Test cases sin expected result:** Se ejecuta pero no se sabe qué verificar.
- ❌ **Copy-paste de use cases:** El test case repite el use case textualmente — no agrega valor.

**Template:** `phases/05-testing/deliverables/test-cases.md` *(pendiente)*

---

### 5.2.2 Test Case IDs

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.2 Test Cases |
| **Responsable** | QA Engineer |
| **Ejecuta** | QA Engineer |
| **Aprueba** | QA Lead |
| **Formato** | TC-XXX |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Incluido en 5.2.1 |
| **Frecuencia** | Automático |

**Perfil de ejecución:** Requiere una convención de IDs única y trazable.  
En VTT: un agente puede generar IDs automáticamente. Es altamente delegable.

**Qué es:** Sistema de identificadores únicos para cada test case: convención de naming (TC-AUTH-001, TC-ORD-001), secuencia auto-incrementable, y mapping a módulo/feature. Cada ID es único, estable (no cambia), y trazable (se puede buscar en reportes y bug tickets).

**Para qué sirve:** Cuando un bug report dice "falla TC-ORD-015", todos saben exactamente qué test case, qué funcionalidad, y qué pasos reproducir. Sin IDs, los bugs dicen "el formulario no funciona" — ambiguo.

**Inputs requeridos:**
- `5.2.1` Test Cases Document — test cases a identificar
- Convención de naming

**Dependencias (predecessors):**
- `5.2.1` Test Cases Document *(obligatorio)*

**Habilita (successors):**
- Trazabilidad en bug reports y test execution logs

**Audiencia:**
- **QA Team** — referencia en reports

**Secciones esperadas:**
1. Convención de naming (formato: TC-[MODULE]-[SEQ])
2. Módulos y sus prefijos
3. Tabla de IDs asignados

**Criterio de completitud:**
- [ ] Convención de naming definida
- [ ] Cada test case tiene ID único
- [ ] IDs estables (no cambian entre sprints)
- [ ] Prefijo por módulo

**Anti-patrones:**
- ❌ **IDs secuenciales sin módulo:** TC-001 a TC-500 — imposible saber de qué módulo.
- ❌ **IDs que cambian:** Re-numerar test cases cada sprint — rompe referencias en bug reports.

**Template:** N/A — convención aplicada en 5.2.1

---

### 5.2.3 Test Data

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.2 Test Cases |
| **Responsable** | QA Engineer |
| **Ejecuta** | QA Engineer |
| **Aprueba** | QA Lead |
| **Formato** | JSON/Excel |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Por sprint |

**Perfil de ejecución:** Requiere crear datos de test que cubran: valid data, invalid data, boundary values, y edge cases.  
En VTT: un agente puede generar test data sets. Es altamente delegable.

**Qué es:** Conjuntos de datos específicos para ejecutar test cases: datos válidos para happy path (email correcto, campos completos), datos inválidos para negative testing (email sin @, campos vacíos, strings de 10000 caracteres), datos de boundary (min, max, exacto en el límite), y datos de edge case (caracteres especiales, emojis, Unicode, SQL injection strings).

**Para qué sirve:** El test case dice "ingresar un email" — el test data dice exactamente cuál email para cada escenario: `valid@email.com` para positive, `invalidemail` para negative, `a@b.c` para boundary. Los datos específicos hacen los tests reproducibles y exhaustivos.

**Inputs requeridos:**
- `5.2.1` Test Cases Document — test cases que necesitan datos
- `2.5.3` Validation Rules — constraints a testear
- `3B.3.5` Data Dictionary — tipos y rangos de datos

**Dependencias (predecessors):**
- `5.2.1` Test Cases Document *(obligatorio)*

**Habilita (successors):**
- `5.4.1` Functional Test Results — tests ejecutados con datos

**Audiencia:**
- **QA Engineer** — datos para test execution

**Secciones esperadas:**
1. Valid data sets (happy path por feature)
2. Invalid data sets (negative testing)
3. Boundary data sets (min, max, limit)
4. Edge case data sets (special chars, Unicode, long strings, empty)
5. Security test data (SQL injection, XSS payloads)

**Criterio de completitud:**
- [ ] Datos valid/invalid para cada input field principal
- [ ] Boundary values para campos numéricos y strings
- [ ] Edge cases (empty, null, special chars, very long)
- [ ] Security payloads (SQL injection, XSS) para inputs de texto
- [ ] Datos organizados por test case o feature

**Anti-patrones:**
- ❌ **Datos genéricos:** "test" y "123" para todo — no detecta boundary issues.
- ❌ **Sin negative data:** Solo datos válidos — no se testea error handling.
- ❌ **Datos reales de producción:** PII de usuarios reales en test data — violación de privacidad.

**Template:** `phases/05-testing/deliverables/test-data.json` *(pendiente)*

---

### 5.2.4 Expected Results

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.2 Test Cases |
| **Responsable** | QA Engineer |
| **Ejecuta** | QA Engineer |
| **Aprueba** | QA Lead |
| **Formato** | En cada TC |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Incluido en 5.2.1 |
| **Frecuencia** | Por test case |

**Perfil de ejecución:** Requiere definir resultados verificables y específicos para cada test case.  
En VTT: un agente puede generar expected results desde use cases y API specs. Es altamente delegable.

**Qué es:** Resultado esperado específico y verificable para cada test case: qué debe pasar (UI response, API response, DB state, notification enviada), qué NO debe pasar (error, data corruption, side effects), y cómo verificarlo (visual check, API response code, DB query). Cada expected result es binario: PASS o FAIL, sin ambigüedad.

**Para qué sirve:** Un test case sin expected result es como un examen sin respuestas correctas — no se puede calificar. El expected result es la definición de "correcto" que permite a cualquier QA (o automation) determinar si el test pasó o falló.

**Inputs requeridos:**
- `5.2.1` Test Cases Document — test cases
- `2.3.4` Detailed Use Cases — behavior esperado
- `3B.4.3` Request/Response Examples — responses esperados

**Dependencias (predecessors):**
- `5.2.1` Test Cases Document *(obligatorio)*

**Habilita (successors):**
- `5.4.1` Functional Test Results — pass/fail determination

**Audiencia:**
- **QA Engineer** — criterio de pass/fail

**Secciones esperadas:**
1. Expected result por test case (incluido en el TC document)
2. Verificación method (visual, API response, DB query, log check)
3. Expected UI behavior (qué se muestra, qué cambia)
4. Expected API response (status code, body structure)
5. Expected side effects (email sent, notification created, log entry)

**Criterio de completitud:**
- [ ] Cada test case tiene expected result específico
- [ ] Expected results son verificables (no "funciona correctamente")
- [ ] Método de verificación documentado
- [ ] Side effects esperados documentados
- [ ] Binario: se puede determinar PASS/FAIL sin ambigüedad

**Anti-patrones:**
- ❌ **"Funciona correctamente":** Ambiguo — ¿qué significa "correctamente"? Especificar.
- ❌ **Sin lado negativo:** Decir qué debe pasar pero no qué NO debe pasar — side effects no detectados.
- ❌ **Expected result solo UI:** Verificar que la UI muestra "éxito" pero no que la BD se actualizó.

**Template:** N/A — incluido en cada test case de 5.2.1

---

## Tabla resumen de ejecutores — Fase 5.2 Test Cases

| Deliverable | Responsable | Ejecuta | Delegable VTT |
|-------------|-------------|---------|---------------|
| 5.2.1 Test Cases Document | QA Engineer | QA Engineer | ✅ — puede generar test cases desde use cases y business rules |
| 5.2.2 Test Case IDs | QA Engineer | QA Engineer | ✅ — puede generar IDs automáticamente |
| 5.2.3 Test Data | QA Engineer | QA Engineer | ✅ — puede generar data sets completos |
| 5.2.4 Expected Results | QA Engineer | QA Engineer | ✅ — puede generar expected results desde specs |

---

## Siguiente archivo

**Próximo:** `DICCIONARIO_FASE_05_03_TEST_ENVIRONMENT.md` — 4 deliverables (5.3.1 a 5.3.4)
