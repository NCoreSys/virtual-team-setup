# DICCIONARIO DE DELIVERABLES — FASE 5.4: FUNCTIONAL TESTING

**Versión:** 1.0  
**Fecha:** 2026-05-14  
**Fase:** 5 — Testing  
**Subfase:** 5.4 — Functional Testing  
**Total deliverables:** 5  
**Responsable de subfase:** QA Engineer  
**Aprueba:** QA Lead

---

## Contexto de la subfase

Functional Testing verifica que cada funcionalidad del producto funciona según los requisitos: cada use case, cada business rule, cada flujo. Es el testing más extenso y tradicional — ejecutar test cases manualmente o con automation, registrar resultados, reportar defectos, y generar evidencia.

**Prerequisitos de subfase:**
- Test Cases (5.2) — qué testear
- Test Environment (5.3) — dónde testear
- Código deployed en test environment

**Entrega de subfase:**
- Resultados de testing funcional, defectos encontrados, y evidencia

---

### 5.4.1 Functional Test Results

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.4 Functional Testing |
| **Responsable** | QA Engineer |
| **Ejecuta** | QA Engineer |
| **Aprueba** | QA Lead |
| **Formato** | Report |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 3-5 días por sprint |
| **Frecuencia** | Por sprint |

**Perfil de ejecución:** Requiere ejecutar test cases sistemáticamente y documentar resultados con precisión.  
En VTT: un agente NO puede ejecutar tests funcionales manuales (requiere interactuar con la UI real). Puede consolidar resultados en reportes y calcular métricas. Necesita brief con: resultados raw de ejecución.

**Qué es:** Reporte con los resultados de la ejecución de test cases funcionales: por cada test case ejecutado, el resultado (PASS/FAIL/BLOCKED/SKIPPED), la fecha de ejecución, el tester, y notas/observaciones. Incluye métricas agregadas: total executed, pass rate, fail rate, blocked rate.

**Para qué sirve:** Documenta objetivamente el estado de calidad del producto: "de 200 test cases, 180 pasaron (90%), 15 fallaron (7.5%), y 5 están bloqueados (2.5%)". Permite al QA Lead y al Product Owner decidir si el producto está listo para release.

**Inputs requeridos:**
- `5.2.1` Test Cases Document — test cases a ejecutar
- `5.3.1` Test Environment — ambiente donde ejecutar
- Código deployed en test environment

**Dependencias (predecessors):**
- `5.2.1` Test Cases Document *(obligatorio)*
- `5.3.1` Test Environment *(obligatorio)*

**Habilita (successors):**
- `5.4.3` Defects Found — bugs detectados
- `5.4.4` Pass/Fail Summary — resumen de resultados
- `5.11.1` Bug Fixes Implemented — bugs a corregir

**Audiencia:**
- **QA Lead** — overview de calidad
- **Tech Lead** — bugs a priorizar
- **Product Owner** — readiness para release

**Secciones esperadas:**
1. Resumen ejecutivo (total TCs, pass rate, fail rate, blocked)
2. Resultados por módulo/feature
3. Detalle por test case (ID, resultado, fecha, tester, notas)
4. Test cases fallidos con descripción del defecto
5. Test cases bloqueados con razón de bloqueo
6. Métricas y gráficos (pass/fail trend por sprint)

**Criterio de completitud:**
- [ ] Todos los test cases in-scope ejecutados
- [ ] Resultado documentado por TC (PASS/FAIL/BLOCKED/SKIPPED)
- [ ] TCs fallidos tienen defecto referenciado
- [ ] Métricas calculadas (pass rate, fail rate)
- [ ] Reporte generado y compartido con stakeholders

**Anti-patrones:**
- ❌ **"Todo pasa":** 100% pass rate sospechoso — probablemente no se testearon edge cases.
- ❌ **Sin detalles en FAILs:** "TC-015: FAIL" sin explicar qué falló — inútil para el developer.
- ❌ **Testing superficial:** Ejecutar los pasos pero no verificar el expected result con rigor.

**Template:** `phases/05-testing/deliverables/functional-test-results.md` *(pendiente)*

---

### 5.4.2 Test Execution Log

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.4 Functional Testing |
| **Responsable** | QA Engineer |
| **Ejecuta** | QA Engineer |
| **Aprueba** | QA Lead |
| **Formato** | Documento |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Continuo (durante ejecución) |
| **Frecuencia** | Por sesión de testing |

**Perfil de ejecución:** Requiere disciplina de registro durante la ejecución de tests.  
En VTT: un agente puede generar el template del log. NO puede registrar ejecución real. Es parcialmente delegable.

**Qué es:** Registro cronológico de la ejecución de tests: fecha/hora, tester, test cases ejecutados, ambiente/versión, build number, observaciones generales, y issues encontrados durante la sesión (no solo bugs funcionales sino también issues de ambiente, performance, o UX).

**Para qué sirve:** Trazabilidad de cuándo se ejecutó qué, por quién, en qué versión. Si un bug aparece en producción, el log permite verificar: "¿se testeó esta funcionalidad? ¿en qué versión? ¿cuándo?".

**Inputs requeridos:**
- Sesiones de testing ejecutadas
- Build/version deployed

**Dependencias (predecessors):**
- `5.4.1` Functional Test Results *(co-dependencia)*

**Habilita (successors):**
- Trazabilidad de testing
- Auditoría de coverage

**Audiencia:**
- **QA Lead** — oversight de ejecución
- **Tech Lead** — qué versión se testeó

**Secciones esperadas:**
1. Log entries (fecha, hora, tester, build, TCs ejecutados, resultado summary, notas)
2. Issues de ambiente detectados
3. Observaciones generales de la sesión

**Criterio de completitud:**
- [ ] Cada sesión de testing registrada
- [ ] Build/version documentado
- [ ] TCs ejecutados listados
- [ ] Issues de ambiente reportados

**Anti-patrones:**
- ❌ **Sin log:** "Testeé ayer" — ¿qué? ¿en qué versión? No hay registro.
- ❌ **Log post-facto:** Registrar de memoria al final del día — impreciso.

**Template:** `phases/05-testing/deliverables/test-execution-log.md` *(pendiente)*

---

### 5.4.3 Defects Found

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.4 Functional Testing |
| **Responsable** | QA Engineer |
| **Ejecuta** | QA Engineer |
| **Aprueba** | QA Lead |
| **Formato** | Lista (Jira/GitHub Issues) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Continuo |
| **Frecuencia** | Por defecto encontrado |

**Perfil de ejecución:** Requiere redactar bug reports claros, reproducibles, y con evidencia.  
En VTT: un agente puede formatear bug reports y agregar contexto técnico. Es parcialmente delegable.

**Qué es:** Lista de todos los defectos encontrados durante testing funcional, reportados en el bug tracker (Jira, GitHub Issues, Linear): cada bug tiene ID, título descriptivo, severidad (critical/high/medium/low), prioridad, pasos de reproducción, resultado actual vs esperado, evidencia (screenshot/video), ambiente/versión, y test case referenciado.

**Para qué sirve:** Un bug report bien escrito se arregla en 30 minutos. Un bug report mal escrito ("no funciona") toma 2 horas de ida y vuelta entre QA y dev para entender qué falla. Los bug reports son la comunicación formal entre QA y Development.

**Inputs requeridos:**
- `5.4.1` Functional Test Results — TCs fallidos
- `5.4.5` Screenshots/Evidence — evidencia visual

**Dependencias (predecessors):**
- `5.4.1` Functional Test Results *(obligatorio)* — tests ejecutados

**Habilita (successors):**
- `5.11.1` Bug Fixes Implemented — bugs a corregir
- `5.11.3` Bug Resolution Report — tracking de resolución
- `5.4.4` Pass/Fail Summary — conteo de defectos

**Audiencia:**
- **Backend/Frontend Developer** — reproduce y arregla el bug
- **Tech Lead** — priorización
- **QA Lead** — overview de defectos
- **Product Owner** — impacto en release

**Secciones esperadas:**
1. Bug report template (ID, título, severidad, prioridad, steps, actual vs expected, evidence, env, TC ref)
2. Clasificación de severidad (critical: bloquea uso, high: funcionalidad rota, medium: workaround existe, low: cosmético)
3. Lista de defectos abiertos
4. Distribución por severidad y por módulo

**Criterio de completitud:**
- [ ] Cada TC fallido tiene bug report correspondiente
- [ ] Steps de reproducción claros y verificados
- [ ] Severidad y prioridad asignadas
- [ ] Screenshot o video como evidencia
- [ ] Ambiente y versión documentados
- [ ] TC referenciado

**Anti-patrones:**
- ❌ **"No funciona":** Sin steps de reproducción — el developer no puede reproducir.
- ❌ **Sin severidad:** Todos los bugs parecen iguales — imposible priorizar.
- ❌ **Sin evidencia:** "El botón no hace nada" — ¿cuál botón? ¿en qué pantalla? Screenshot resuelve.
- ❌ **Bugs duplicados:** No buscar si ya existe un report similar — noise en el backlog.

**Template:** `phases/05-testing/deliverables/bug-report-template.md` *(pendiente)*

---

### 5.4.4 Pass/Fail Summary

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.4 Functional Testing |
| **Responsable** | QA Engineer |
| **Ejecuta** | QA Engineer |
| **Aprueba** | QA Lead |
| **Formato** | Tabla |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.25 día |
| **Frecuencia** | Por sprint |

**Perfil de ejecución:** Requiere agregar resultados en un resumen ejecutivo.  
En VTT: un agente puede generar el summary desde los resultados. Es altamente delegable.

**Qué es:** Tabla resumen de resultados de testing: total test cases, PASS count/%, FAIL count/%, BLOCKED count/%, SKIPPED count/%, desglosado por módulo. Es el "dashboard" de testing que se presenta en sprint review o release meeting.

**Para qué sirve:** El Product Owner no lee 200 test cases — lee el summary: "90% pass, 5% fail (8 bugs, 2 critical), 3% blocked, 2% skipped". En 10 segundos sabe el estado de calidad y si puede dar go/no-go para release.

**Inputs requeridos:**
- `5.4.1` Functional Test Results — datos raw

**Dependencias (predecessors):**
- `5.4.1` Functional Test Results *(obligatorio)*

**Habilita (successors):**
- Go/no-go decision para release
- Sprint review reporting

**Audiencia:**
- **Product Owner** — go/no-go
- **QA Lead** — overview
- **Management** — quality status

**Secciones esperadas:**
1. Summary table (total, pass, fail, blocked, skipped — count y %)
2. Breakdown por módulo
3. Breakdown por severidad de defectos
4. Trend vs sprint anterior
5. Go/no-go recommendation

**Criterio de completitud:**
- [ ] Totales calculados
- [ ] Breakdown por módulo
- [ ] Defectos por severidad
- [ ] Recommendation de QA (go/no-go/conditional)

**Anti-patrones:**
- ❌ **Solo números sin contexto:** "15 fails" — ¿de qué severidad? 15 cosméticos ≠ 15 critical.
- ❌ **Summary sin recommendation:** Datos sin opinión de QA — el PO no sabe qué decidir.

**Template:** `phases/05-testing/deliverables/pass-fail-summary.md` *(pendiente)*

---

### 5.4.5 Screenshots/Evidence

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.4 Functional Testing |
| **Responsable** | QA Engineer |
| **Ejecuta** | QA Engineer |
| **Aprueba** | QA Lead |
| **Formato** | Images / Videos |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Continuo (durante testing) |
| **Frecuencia** | Por defecto / por TC crítico |

**Perfil de ejecución:** Requiere capturar evidencia visual durante testing.  
En VTT: un agente NO puede capturar screenshots de testing manual. Puede organizar y nombrar evidencia. Es parcialmente delegable.

**Qué es:** Capturas de pantalla y videos que documentan: bugs encontrados (screenshot del error, video de reproducción), test cases críticos ejecutados (evidencia de PASS), y comparación visual vs mockup (implementación matches diseño). Organizados por TC ID y nombrados consistentemente.

**Para qué sirve:** "Una imagen vale más que mil palabras" — un screenshot del bug es la mejor evidencia. Un video de reproducción elimina el "no puedo reproducirlo". La evidencia de PASS en TCs críticos es prueba de que se testeó (para auditoría/compliance).

**Inputs requeridos:**
- Ejecución de testing en progreso
- Herramienta de captura (Loom, screenshot tool)

**Dependencias (predecessors):**
- `5.4.1` Functional Test Results *(co-dependencia)* — evidence durante ejecución

**Habilita (successors):**
- `5.4.3` Defects Found — evidence en bug reports
- Auditoría de testing

**Audiencia:**
- **Developer** — reproduce bug desde evidence
- **QA Lead** — verificación de testing

**Secciones esperadas:**
1. Screenshots de bugs (nombrados: BUG-XXX-description.png)
2. Videos de reproducción (para bugs complejos)
3. Screenshots de TCs críticos PASS (evidence de testing)
4. Comparación visual (implementación vs mockup)
5. Naming convention de archivos

**Criterio de completitud:**
- [ ] Cada bug report tiene screenshot o video
- [ ] TCs críticos tienen evidence de PASS
- [ ] Naming convention consistente
- [ ] Organizados por sprint/TC
- [ ] Accesibles por el equipo (no en el desktop del QA)

**Anti-patrones:**
- ❌ **Bugs sin screenshot:** "El botón no funciona" — ¿cuál botón? ¿qué pantalla?
- ❌ **Screenshots sin contexto:** Imagen sin TC reference ni descripción — ¿qué muestra?
- ❌ **Evidence solo local:** En el desktop del QA — inaccesible para developers.

**Template:** `phases/05-testing/deliverables/evidence/` *(pendiente)*

---

## Tabla resumen de ejecutores — Fase 5.4 Functional Testing

| Deliverable | Responsable | Ejecuta | Delegable VTT |
|-------------|-------------|---------|---------------|
| 5.4.1 Functional Test Results | QA Engineer | QA Engineer | 🔶 Parcial — puede consolidar resultados, no ejecutar tests manuales |
| 5.4.2 Test Execution Log | QA Engineer | QA Engineer | 🔶 Parcial — puede generar template, no registrar ejecución real |
| 5.4.3 Defects Found | QA Engineer | QA Engineer | 🔶 Parcial — puede formatear bug reports, no encontrar bugs |
| 5.4.4 Pass/Fail Summary | QA Engineer | QA Engineer | ✅ — puede generar summary desde resultados |
| 5.4.5 Screenshots/Evidence | QA Engineer | QA Engineer | ❌ — requiere captura manual durante testing |

---

## Siguiente archivo

**Próximo:** `DICCIONARIO_FASE_05_05_INTEGRATION_TESTING.md` — 4 deliverables (5.5.1 a 5.5.4)
