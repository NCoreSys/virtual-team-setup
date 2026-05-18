# DICCIONARIO DE DELIVERABLES — FASE 5.7: PERFORMANCE TESTING

**Versión:** 1.1  
**Fecha:** 2026-05-14  
**Fase:** 5 — Testing  
**Subfase:** 5.7 — Performance Testing  
**Total deliverables:** 6  
**Responsable de subfase:** QA Automation  
**Aprueba:** Tech Lead

---

## Contexto de la subfase

Performance Testing verifica que el sistema cumple los NFRs de rendimiento bajo carga: latencia aceptable, throughput suficiente, y estabilidad bajo estrés. Incluye load testing (carga esperada), stress testing (más allá de lo esperado), y análisis de bottlenecks con recomendaciones de optimización.

---

### 5.7.1 Load Test Plan

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.7 Performance Testing |
| **Responsable** | QA Automation |
| **Ejecuta** | QA Automation |
| **Aprueba** | Tech Lead |
| **Formato** | Documento |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere definir escenarios de carga realistas basados en proyecciones de uso y NFRs.  
En VTT: un agente puede generar el plan completo con escenarios y scripts k6. Es bastante delegable.

**Qué es:** Plan que define la estrategia de performance testing: qué endpoints testear (priorizados por criticidad y uso), escenarios de carga (normal: 100 concurrent, pico: 500, estrés: 1000), ramp-up profiles, métricas a medir (latencia p50/p95/p99, throughput, error rate), targets de NFRs, herramienta (k6, Artillery, JMeter), y ambiente de ejecución.

**Para qué sirve:** Sin plan, el performance testing es ad-hoc ("mandé 1000 requests y no se cayó"). El plan define escenarios realistas que simulan uso real con targets claros de pass/fail.

**Inputs requeridos:**
- NFRs de performance (latencia target, throughput target)
- `3B.8.6` Scaling Strategy — capacidad esperada
- `3B.4.2` Endpoints List — endpoints a testear
- Analytics de uso (si hay producto previo)

**Dependencias (predecessors):**
- NFRs *(obligatorio)*
- `3B.4.2` Endpoints List *(obligatorio)*
- `5.3.1` Test Environment *(obligatorio)*

**Habilita (successors):**
- `5.7.2` Load Test Results — ejecución del plan
- `5.7.3` Stress Test Results — ejecución del plan

**Audiencia:**
- **QA Automation** — ejecutor
- **Tech Lead** — aprobación de targets
- **DevOps Lead** — capacity del ambiente de test

**Secciones esperadas:**
1. Endpoints a testear (tabla: endpoint, method, criticidad, uso estimado)
2. Escenarios de carga (normal, pico, estrés — con números de usuarios)
3. Ramp-up profiles (gradual: 0 → 100 en 2 min, step: 50 → 100 → 200)
4. Métricas y targets (tabla: métrica, target, critical threshold)
5. Herramienta seleccionada y justificación
6. Ambiente de ejecución (staging con sizing similar a prod)
7. Data preparation (datos en BD para simular volumen realista)
8. Schedule de ejecución

**Criterio de completitud:**
- [ ] Endpoints críticos identificados y priorizados
- [ ] Al menos 3 escenarios definidos (normal, pico, estrés)
- [ ] Targets de performance definidos con números (p95 < 200ms)
- [ ] Herramienta seleccionada
- [ ] Ambiente definido (NO producción)
- [ ] Ramp-up profiles definidos

**Anti-patrones:**
- ❌ **Load test en producción:** Tumbar el sistema real con tráfico artificial — usar staging con sizing similar.
- ❌ **Sin targets:** "Veamos cuánto aguanta" — sin target no hay pass/fail.
- ❌ **Un solo endpoint:** Testear solo GET /health — no representa uso real.
- ❌ **Sin ramp-up:** 1000 usuarios simultáneos de golpe — no es realista.

**Template:** `phases/05-testing/deliverables/load-test-plan.md` *(pendiente)*

---

### 5.7.2 Load Test Results

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.7 Performance Testing |
| **Responsable** | QA Automation |
| **Ejecuta** | QA Automation |
| **Aprueba** | Tech Lead |
| **Formato** | Report |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Pre-release |

**Perfil de ejecución:** Requiere ejecutar load tests y analizar resultados contra targets.  
En VTT: un agente puede generar scripts k6, ejecutarlos, y analizar resultados. Es bastante delegable.

**Qué es:** Resultados de testing bajo carga normal y pico esperado: latencia por endpoint (p50, p95, p99), throughput (requests/second), error rate, resource utilization (CPU, RAM, DB connections), y pass/fail vs targets de NFRs. Incluye gráficos de latencia y throughput over time durante el test.

**Para qué sirve:** Verifica que el sistema cumple los NFRs bajo la carga esperada. Si p95 target es 200ms y el resultado es 180ms → PASS. Si es 350ms → FAIL, y se necesita optimización antes del release.

**Inputs requeridos:**
- `5.7.1` Load Test Plan — escenarios y targets
- `5.3.1` Test Environment — ambiente de ejecución
- k6/Artillery scripts

**Dependencias (predecessors):**
- `5.7.1` Load Test Plan *(obligatorio)*
- `5.3.1` Test Environment *(obligatorio)*

**Habilita (successors):**
- `5.7.4` Performance Metrics — métricas consolidadas
- `5.7.5` Bottleneck Analysis — si hay failures
- Go/no-go para release (performance cumple NFRs)

**Audiencia:**
- **Tech Lead** — pass/fail vs NFRs
- **DevOps Lead** — resource utilization
- **Backend Developer** — endpoints a optimizar

**Secciones esperadas:**
1. Test configuration (escenario, usuarios, duración, ramp-up)
2. Latency results (tabla: endpoint, p50, p95, p99, target, pass/fail)
3. Throughput (req/s global y por endpoint)
4. Error rate (% por tipo: timeout, 5xx, 4xx)
5. Resource utilization (CPU, RAM, DB connections — peak values)
6. Gráficos de latency y throughput over time
7. Pass/fail summary vs NFR targets
8. Observations y anomalías detectadas

**Criterio de completitud:**
- [ ] Tests ejecutados según todos los escenarios del plan
- [ ] Latency p50/p95/p99 reportado por endpoint
- [ ] Throughput reportado
- [ ] Error rate reportado
- [ ] Resource utilization reportado
- [ ] Pass/fail vs targets documentado
- [ ] Gráficos incluidos

**Anti-patrones:**
- ❌ **Solo promedios:** p50 = 100ms pero p99 = 5000ms — los promedios ocultan outliers.
- ❌ **Sin gráficos:** Solo números — los gráficos muestran spikes y trends que los números no.
- ❌ **Test con BD vacía:** 100ms con 10 rows ≠ 100ms con 1M rows — usar datos representativos.
- ❌ **Sin resource metrics:** Latency OK pero CPU al 95% — está al límite, cualquier spike lo tumba.

**Template:** `phases/05-testing/deliverables/load-test-results.md` *(pendiente)*

---

### 5.7.3 Stress Test Results

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.7 Performance Testing |
| **Responsable** | QA Automation |
| **Ejecuta** | QA Automation |
| **Aprueba** | Tech Lead |
| **Formato** | Report |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Pre-release |

**Perfil de ejecución:** Requiere ejecutar tests más allá de la carga esperada para encontrar el breaking point.  
En VTT: un agente puede ejecutar stress tests con ramp-up progresivo y analizar resultados. Es bastante delegable.

**Qué es:** Resultados de testing más allá de la carga esperada: ramp-up progresivo (100 → 200 → 500 → 1000 → hasta que se degrada) para encontrar el breaking point. Documenta: a cuántos usuarios concurrentes empieza la degradación (latency spike), a cuántos se vuelve inutilizable (error rate > 10%), cuál es el bottleneck (DB connections, CPU, memory, network), y cómo se recupera cuando la carga baja.

**Para qué sirve:** Conocer el breaking point permite: saber cuánto margen hay (si el pico esperado es 500 y el breaking point es 800, hay 60% de margen), identificar qué se rompe primero (DB connections se agotan antes que la CPU), y planificar scaling proactivo.

**Inputs requeridos:**
- `5.7.1` Load Test Plan — escenario de estrés
- `5.3.1` Test Environment — ambiente de ejecución

**Dependencias (predecessors):**
- `5.7.1` Load Test Plan *(obligatorio)*
- `5.7.2` Load Test Results *(recomendado)* — baseline antes de stress

**Habilita (successors):**
- `5.7.5` Bottleneck Analysis — qué se saturó
- `5.7.6` Optimization Recommendations — qué mejorar
- `7.6.2` Capacity Planning — breaking point como input

**Audiencia:**
- **Tech Lead** — capacity decisions
- **DevOps Lead** — scaling planning
- **Solution Architect** — architecture bottlenecks

**Secciones esperadas:**
1. Test configuration (ramp-up progresivo, max usuarios, duración por step)
2. Degradation point (a cuántos usuarios empieza la degradación — latency > 2x normal)
3. Breaking point (a cuántos usuarios el sistema falla — error rate > 10%)
4. Bottleneck identificado (qué componente se saturó primero)
5. Resource utilization at breaking point (CPU, RAM, DB connections, disk I/O)
6. Recovery behavior (cuánto tarda en recuperarse cuando la carga baja)
7. Gráficos: latency vs users, throughput vs users, error rate vs users
8. Margin analysis (pico esperado vs breaking point = % de margen)

**Criterio de completitud:**
- [ ] Breaking point identificado con número de usuarios
- [ ] Bottleneck identificado (qué componente se saturó)
- [ ] Degradation point documentado (antes del breaking point)
- [ ] Recovery behavior verificado
- [ ] Margin calculado (pico esperado vs breaking point)
- [ ] Gráficos incluidos
- [ ] Resource utilization at breaking point documentado

**Anti-patrones:**
- ❌ **Stress test hasta crash sin análisis:** "Se cayó a 500 users" — ¿por qué? ¿qué se saturó? Sin análisis no es útil.
- ❌ **Sin recovery test:** El sistema se cayó — ¿se recupera solo o necesita restart manual?
- ❌ **Stress test = load test con más usuarios:** Stress test busca el breaking point, no solo "funciona con más carga".
- ❌ **Sin margin calculation:** Saber el breaking point sin comparar con pico esperado — no contextualiza el riesgo.

**Template:** `phases/05-testing/deliverables/stress-test-results.md` *(pendiente)*

---

### 5.7.4 Performance Metrics

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.7 Performance Testing |
| **Responsable** | QA Automation |
| **Ejecuta** | QA Automation |
| **Aprueba** | Tech Lead |
| **Formato** | Dashboard |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Por test run |

**Perfil de ejecución:** Requiere consolidar métricas de performance en un dashboard accesible.  
En VTT: un agente puede crear dashboards y consolidar métricas. Es altamente delegable.

**Qué es:** Dashboard consolidado con métricas de performance: latencia por endpoint (p50/p95/p99), throughput, error rate, Apdex score, comparación vs NFR targets (pass/fail visual), y trend entre test runs. Puede estar en Grafana, k6 Cloud, o como reporte estático con gráficos.

**Para qué sirve:** Vista rápida del performance: el Tech Lead ve en 10 segundos si el sistema cumple NFRs. Sin dashboard, hay que leer reportes de 20 páginas para entender el estado.

**Inputs requeridos:**
- `5.7.2` Load Test Results — datos
- `5.7.3` Stress Test Results — datos
- NFR targets para comparación

**Dependencias (predecessors):**
- `5.7.2` Load Test Results *(obligatorio)*

**Habilita (successors):**
- Performance decisions rápidas
- Trend tracking entre releases

**Audiencia:**
- **Tech Lead** — overview rápido
- **DevOps Lead** — capacity view

**Secciones esperadas:**
1. Latency dashboard (p50, p95, p99 por endpoint vs target)
2. Throughput dashboard (req/s vs capacity)
3. Error rate dashboard (% vs threshold)
4. Apdex score (si se calcula)
5. NFR compliance (pass/fail visual por métrica)
6. Trend vs test run anterior

**Criterio de completitud:**
- [ ] Métricas principales visualizadas
- [ ] NFR targets marcados en dashboard
- [ ] Pass/fail visual claro
- [ ] Trend vs run anterior
- [ ] Accesible por stakeholders

**Anti-patrones:**
- ❌ **Solo promedios en dashboard:** Ocultan outliers — incluir percentiles.
- ❌ **Dashboard sin targets:** Números sin contexto — ¿200ms es bueno o malo?
- ❌ **Dashboard inaccesible:** Solo el QA puede verlo — debe ser compartible.

**Template:** N/A — dashboard en Grafana o k6 Cloud

---

### 5.7.5 Bottleneck Analysis

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.7 Performance Testing |
| **Responsable** | QA Automation |
| **Ejecuta** | QA Automation / Tech Lead |
| **Aprueba** | Tech Lead |
| **Formato** | Report |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Por test run con issues |

**Perfil de ejecución:** Requiere analizar dónde están los cuellos de botella usando APM, DB profiling, y resource metrics.  
En VTT: un agente puede analizar métricas y sugerir bottlenecks. Es parcialmente delegable. Diagnóstico profundo de queries o memory leaks requiere developer/DBA.

**Qué es:** Análisis de dónde están los cuellos de botella cuando los tests fallan o se acercan a los limits: slow queries (EXPLAIN ANALYZE), memory leaks (heap growth over time), connection pool exhaustion (max connections reached), CPU-bound operations (blocking event loop), network latency (slow external service calls), y serialization overhead.

**Para qué sirve:** "El sistema es lento" no es accionable. "GET /orders es lento porque la query hace full table scan en orders (1M rows) sin índice en status, y el p95 es 1200ms" es accionable — agregar un índice lo resuelve.

**Inputs requeridos:**
- `5.7.2` y `5.7.3` — test results con issues
- APM data (New Relic, Datadog traces)
- DB slow query log
- Resource metrics (CPU, RAM, connections)

**Dependencias (predecessors):**
- `5.7.2` Load Test Results *(obligatorio)*
- `5.7.3` Stress Test Results *(recomendado)*

**Habilita (successors):**
- `5.7.6` Optimization Recommendations — soluciones

**Audiencia:**
- **Tech Lead** — decisions de optimización
- **Backend Developer** — código a optimizar
- **Database Engineer** — queries a optimizar
- **DevOps Lead** — infra a escalar

**Secciones esperadas:**
1. Bottleneck(s) identificados (tabla: componente, endpoint, root cause, evidence)
2. Evidence por bottleneck (EXPLAIN ANALYZE, APM trace, metrics screenshot)
3. Root cause analysis (por qué es lento, no solo qué es lento)
4. Impact cuantificado (cuántos ms agrega, cuántos usuarios afecta)
5. Component ranking (qué limita más el throughput — ley de Amdahl)

**Criterio de completitud:**
- [ ] Al menos 1 bottleneck identificado con evidence
- [ ] Root cause documentada (no solo "la BD es lenta")
- [ ] Impact cuantificado
- [ ] Evidence incluida (queries, traces, metrics)
- [ ] Component ranking (qué resolver primero)

**Anti-patrones:**
- ❌ **"La BD es lenta":** Sin especificar qué query, qué tabla, por qué — no accionable.
- ❌ **Asumir sin datos:** "Probablemente es la BD" — usar APM traces como evidence.
- ❌ **Optimizar todo:** Resolver 10 bottlenecks a la vez — resolver el #1 primero (ley de Amdahl).

**Template:** `phases/05-testing/deliverables/bottleneck-analysis.md` *(pendiente)*

---

### 5.7.6 Optimization Recommendations

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.7 Performance Testing |
| **Responsable** | QA Automation |
| **Ejecuta** | Tech Lead |
| **Aprueba** | Solution Architect |
| **Formato** | Documento |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Por análisis de bottleneck |

**Perfil de ejecución:** Requiere proponer soluciones técnicas a los bottlenecks identificados.  
En VTT: un agente puede sugerir optimizaciones basadas en best practices. Es parcialmente delegable. Soluciones específicas al contexto del proyecto requieren Tech Lead.

**Qué es:** Recomendaciones accionables para resolver los bottlenecks: agregar índice, implementar cache (Redis), optimizar query (rewrite JOIN, add pagination), agregar connection pooling, horizontal scaling, code refactoring (async processing), o CDN para static assets. Cada recomendación con: effort estimate, expected impact, y priority.

**Para qué sirve:** Traduce bottlenecks en acciones priorizadas. "Quick wins" primero (agregar índice = 30 min de trabajo, 10x improvement), "medium-term" después (implementar cache = 2 días, 5x improvement), "long-term" en roadmap (re-architecture = 2 semanas).

**Inputs requeridos:**
- `5.7.5` Bottleneck Analysis — problemas a resolver

**Dependencias (predecessors):**
- `5.7.5` Bottleneck Analysis *(obligatorio)*

**Habilita (successors):**
- Sprint backlog con items de optimización
- Performance improvement medible

**Audiencia:**
- **Tech Lead** — priorización
- **Backend Developer** — implementación
- **DevOps Lead** — infra changes

**Secciones esperadas:**
1. Quick wins (bajo esfuerzo, alto impacto — implementar esta semana)
2. Medium-term (esfuerzo moderado, impacto significativo — próximo sprint)
3. Long-term (esfuerzo alto, impacto estructural — roadmap)
4. Por recomendación: description, effort, expected impact, priority, assignee
5. Expected results (p95 esperado después de implementar top 3 recommendations)

**Criterio de completitud:**
- [ ] Recomendación por cada bottleneck identificado
- [ ] Effort y expected impact estimados
- [ ] Quick wins identificados (resolver primero)
- [ ] Priorización aplicada
- [ ] Expected improvement cuantificado

**Anti-patrones:**
- ❌ **"Optimizar todo":** Sin priorización — resolver bottleneck #1 primero.
- ❌ **Premature optimization:** Optimizar endpoints que no son bottleneck — desperdicio.
- ❌ **Recommendations sin effort:** "Implementar cache" — ¿cuánto toma? ¿quién lo hace?
- ❌ **Solo recomendaciones de infra:** "Agregar más servers" — a veces un índice en la BD es más efectivo y barato.

**Template:** `phases/05-testing/deliverables/optimization-recommendations.md` *(pendiente)*

---

## Tabla resumen — Fase 5.7

| Deliverable | Responsable | Delegable VTT |
|-------------|-------------|---------------|
| 5.7.1 Load Test Plan | QA Automation | ✅ |
| 5.7.2 Load Test Results | QA Automation | ✅ — scripts k6 generables |
| 5.7.3 Stress Test Results | QA Automation | ✅ — scripts k6 generables |
| 5.7.4 Performance Metrics | QA Automation | ✅ — dashboard configurable |
| 5.7.5 Bottleneck Analysis | QA Automation / Tech Lead | 🔶 — análisis profundo requiere expertise |
| 5.7.6 Optimization Recommendations | Tech Lead | 🔶 — soluciones específicas requieren contexto |
