# DICCIONARIO DE DELIVERABLES — FASE 7 (PARTE 1): OPERATIONS — MONITORING, USER SUPPORT, BUG FIXES

**Versión:** 1.1  
**Fecha:** 2026-05-14  
**Fase:** 7 — Operations  
**Subfases en este archivo:** 7.1, 7.2, 7.3  
**Deliverables en este archivo:** 11  
**Responsable de fase:** SRE  
**Aprueba:** Tech Lead

---

## Contexto de la fase

Operations es la fase continua post-lanzamiento: mantener el producto funcionando, monitorear performance, dar soporte a usuarios, corregir bugs en producción, mejorar incrementalmente, actualizar seguridad, y escalar según demanda. Es la fase más larga — dura mientras el producto viva.

---

## 7.1 Monitoring (4 deliverables)

**Responsable:** SRE | **Aprueba:** Tech Lead

---

### 7.1.1 Uptime Reports

| Campo | Valor |
|-------|-------|
| **Fase** | 7-Operations |
| **Subfase** | 7.1 Monitoring |
| **Responsable** | SRE |
| **Ejecuta** | SRE |
| **Aprueba** | Tech Lead |
| **Formato** | Report |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Automático + 0.25 día review |
| **Frecuencia** | Mensual |

**Perfil de ejecución:** Requiere interpretar métricas de uptime y generar reportes accionables con SLO compliance.  
En VTT: un agente puede generar reportes automáticos desde Grafana/Datadog, calcular SLO compliance, y resaltar anomalías. Es altamente delegable.

**Qué es:** Reporte mensual de disponibilidad del sistema: uptime % (target vs actual), downtime incidents con duración y causa, SLO compliance, trend mensual, y comparación con meses anteriores. Ejemplo: "El sistema estuvo disponible 99.95% del mes, con 22 minutos de downtime por el incidente INC-047".

**Para qué sirve:** Documenta si el sistema cumple sus compromisos de disponibilidad (SLO). Un trend de uptime decreciente señala problemas antes de que se conviertan en crisis. Es evidencia para stakeholders y clientes de la confiabilidad del sistema.

**Inputs requeridos:**
- `6.6.1` Monitoring Dashboard — métricas de uptime
- `3B.8.10` SLA Definition — targets de uptime
- Incident log — incidents del mes

**Dependencias (predecessors):**
- `6.6.1` Monitoring Dashboard *(obligatorio)*
- `3B.8.10` SLA Definition *(obligatorio)*

**Habilita (successors):**
- `7.1.4` Weekly Reports — data de uptime
- Decisiones de inversión en reliability

**Audiencia:**
- **Tech Lead** — health del sistema
- **Product Owner** — quality del producto
- **Management** — SLO compliance
- **Clientes** — SLA evidence (si contractual)

**Secciones esperadas:**
1. Uptime % del mes (actual vs target SLO)
2. Downtime incidents (tabla: fecha, duración, causa, resolución)
3. SLO compliance (dentro/fuera de error budget)
4. Trend mensual (últimos 3-6 meses)
5. Top causas de downtime
6. Action items para mejorar uptime

**Criterio de completitud:**
- [ ] Uptime % calculado con precisión
- [ ] Todos los incidents del mes documentados
- [ ] SLO compliance evaluado
- [ ] Trend incluido
- [ ] Action items si SLO no cumplido
- [ ] Distribuido a stakeholders

**Anti-patrones:**
- ❌ **"99.9% uptime" sin definición:** ¿Qué cuenta como downtime? Definir claramente.
- ❌ **Reporte sin action items:** Solo datos sin plan para mejorar — decorativo.
- ❌ **Excluir maintenance windows:** Si el usuario no puede acceder, es downtime — no importa que sea "planificado".

**Template:** `phases/07-operations/deliverables/uptime-report.md` *(pendiente)*

---

### 7.1.2 Performance Reports

| Campo | Valor |
|-------|-------|
| **Fase** | 7-Operations |
| **Subfase** | 7.1 Monitoring |
| **Responsable** | SRE |
| **Ejecuta** | SRE |
| **Aprueba** | Tech Lead |
| **Formato** | Report |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Automático + 0.25 día review |
| **Frecuencia** | Mensual |

**Perfil de ejecución:** Requiere analizar métricas de performance y detectar degradación temprana.  
En VTT: un agente puede generar reportes desde dashboards de performance. Es altamente delegable.

**Qué es:** Reporte mensual de performance: latencia p50/p95/p99 por endpoint, throughput (requests/second), error rate por tipo, y comparación vs SLO targets. Identifica endpoints con degradación de performance, trends preocupantes, y correlación con cambios (deploys, traffic spikes, data growth).

**Para qué sirve:** Performance se degrada gradualmente — un endpoint que respondía en 100ms hace 3 meses ahora responde en 300ms porque la tabla creció. El reporte detecta esta degradación antes de que se convierta en un outage o en una queja masiva de usuarios.

**Inputs requeridos:**
- `6.6.1` Monitoring Dashboard — métricas de performance
- `6.6.4` Metrics Collection — datos de latency, throughput
- `3B.8.10` SLA Definition — targets de performance

**Dependencias (predecessors):**
- `6.6.1` Monitoring Dashboard *(obligatorio)*
- `6.6.4` Metrics Collection *(obligatorio)*

**Habilita (successors):**
- `7.1.4` Weekly Reports — data de performance
- Optimización de endpoints degradados
- `7.6.2` Capacity Planning — trends informan capacity

**Audiencia:**
- **Tech Lead** — performance decisions
- **Backend Developer** — endpoints a optimizar
- **SRE** — operational awareness
- **DevOps Lead** — capacity implications

**Secciones esperadas:**
1. Latency summary (p50, p95, p99 — global y por endpoint)
2. Throughput (requests/second — global y por endpoint)
3. Error rate (% por tipo: 4xx, 5xx)
4. Comparison vs SLO targets (pass/fail)
5. Trend vs mes anterior (mejora/empeora)
6. Top 5 endpoints más lentos
7. Top 5 endpoints con más errores
8. Correlación con eventos (deploys, traffic spikes)
9. Recommendations (qué optimizar)

**Criterio de completitud:**
- [ ] Latency metrics incluidas (p50, p95, p99)
- [ ] Comparison vs SLO targets
- [ ] Trend vs periodo anterior
- [ ] Top endpoints problemáticos identificados
- [ ] Recommendations accionables
- [ ] Gráficos incluidos

**Anti-patrones:**
- ❌ **Solo promedios:** p50 = 100ms pero p99 = 5000ms — promedios ocultan outliers, reportar percentiles.
- ❌ **Sin trend:** "p95 es 200ms" — ¿subió? ¿bajó? ¿estable? Sin contexto no es accionable.
- ❌ **Reporte sin recommendations:** Datos sin acción — el Tech Lead no sabe qué priorizar.

**Template:** `phases/07-operations/deliverables/performance-report.md` *(pendiente)*

---

### 7.1.3 Error Reports

| Campo | Valor |
|-------|-------|
| **Fase** | 7-Operations |
| **Subfase** | 7.1 Monitoring |
| **Responsable** | SRE |
| **Ejecuta** | SRE |
| **Aprueba** | Tech Lead |
| **Formato** | Report |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Automático + 0.25 día review |
| **Frecuencia** | Semanal |

**Perfil de ejecución:** Requiere analizar errores de Sentry/logs y priorizar por impacto.  
En VTT: un agente puede generar error reports desde Sentry y logs. Es altamente delegable.

**Qué es:** Reporte semanal de errores en producción: nuevos errores detectados (Sentry), top errores por frecuencia e impacto (usuarios afectados), error rate trend, errores resueltos vs abiertos, y distribución por módulo. Prioriza qué bugs de producción arreglar primero basándose en impacto real.

**Para qué sirve:** Sin error report, los errores de producción se acumulan silenciosamente. Un error que afecta a 1000 usuarios/día se pierde entre 500 errores de log. El reporte prioriza: "este error afecta al 5% de los usuarios — es el #1 a resolver".

**Inputs requeridos:**
- `6.6.5` Error Tracking — datos de Sentry
- `6.6.3` Log Aggregation — error logs
- `7.3.3` Bug Tracking — status de bugs conocidos

**Dependencias (predecessors):**
- `6.6.5` Error Tracking *(obligatorio)*

**Habilita (successors):**
- `7.3.1` Hotfix Process — errores críticos disparan hotfixes
- `7.3.3` Bug Tracking — nuevos bugs identificados
- Sprint planning — bugs como backlog items

**Audiencia:**
- **Tech Lead** — priorización de bugs
- **Developers** — bugs a resolver
- **QA Lead** — error trends
- **Product Owner** — impacto en usuarios

**Secciones esperadas:**
1. New errors this week (tabla: error, count, users affected, first seen)
2. Top errors by frequency (recurrentes)
3. Top errors by impact (usuarios afectados)
4. Error rate trend (semanal, últimas 4 semanas)
5. Errors resolved this week
6. Open errors by severity
7. Distribution by module/service
8. Action items (top 3 errores a resolver esta semana)

**Criterio de completitud:**
- [ ] Nuevos errores identificados
- [ ] Top errores por frecuencia e impacto
- [ ] Error rate trend incluido
- [ ] Errores resueltos vs abiertos
- [ ] Action items con top 3 prioridades
- [ ] Distribuido a Tech Lead y developers

**Anti-patrones:**
- ❌ **Lista de 500 errores sin priorización:** Nadie sabe por dónde empezar — priorizar por impacto.
- ❌ **Solo count sin impact:** "Error X ocurrió 1000 veces" — ¿cuántos usuarios afectó? Count ≠ impact.
- ❌ **Errores ignorados semana tras semana:** Error en el reporte 10 semanas seguidas sin resolverse — debt acumulada.

**Template:** `phases/07-operations/deliverables/error-report.md` *(pendiente)*

---

### 7.1.4 Weekly Reports

| Campo | Valor |
|-------|-------|
| **Fase** | 7-Operations |
| **Subfase** | 7.1 Monitoring |
| **Responsable** | SRE |
| **Ejecuta** | SRE |
| **Aprueba** | Tech Lead |
| **Formato** | Report |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Semanal |

**Perfil de ejecución:** Requiere consolidar métricas operacionales en un reporte ejecutivo semanal.  
En VTT: un agente puede generar el weekly report consolidando datos de múltiples fuentes. Es altamente delegable.

**Qué es:** Reporte semanal consolidado para stakeholders: uptime de la semana, performance highlights, top errores, tickets de soporte (count, themes, resolution time), deploys realizados, incidents (si hubo), y upcoming work (maintenance, deploys planificados). Es el "pulse check" semanal del producto en producción.

**Para qué sirve:** El weekly report es el canal de comunicación entre Operations y el resto del equipo/management. En 1 página, todos saben: "el producto está healthy" o "hay un trend preocupante en latencia que necesita atención". Evita el silencio de Operations donde nadie sabe cómo va hasta que algo se rompe.

**Inputs requeridos:**
- `7.1.1` Uptime Reports — datos de uptime
- `7.1.2` Performance Reports — datos de performance
- `7.1.3` Error Reports — datos de errores
- `7.2.4` Support Metrics — datos de soporte
- Deploy log de la semana

**Dependencias (predecessors):**
- `7.1.1` a `7.1.3` *(obligatorio)* — data sources

**Habilita (successors):**
- Management visibility
- Sprint planning informado por operational data
- Trend detection temprana

**Audiencia:**
- **Tech Lead** — operational overview
- **Product Owner** — product health
- **Management** — executive summary
- **SRE** — compilador del reporte

**Secciones esperadas:**
1. Executive summary (3-5 bullets: lo más importante de la semana)
2. Uptime summary (% de la semana, incidents)
3. Performance summary (latency trend, throughput)
4. Error summary (nuevos, resueltos, top 3)
5. Support summary (tickets abiertos/cerrados, avg resolution time, themes)
6. Deploys de la semana (versiones, issues)
7. Incidents de la semana (si hubo, con post-mortem link)
8. Upcoming (maintenance windows, planned deploys)
9. Action items / asks (si Operations necesita algo del equipo)

**Criterio de completitud:**
- [ ] Todas las secciones completadas
- [ ] Executive summary conciso (1 párrafo)
- [ ] Datos actualizados de la semana (no del mes pasado)
- [ ] Action items si hay issues
- [ ] Distribuido a stakeholders el lunes (o viernes)
- [ ] Formato consistente semana a semana

**Anti-patrones:**
- ❌ **Reporte de 10 páginas:** Nadie lo lee — máximo 1-2 páginas con executive summary.
- ❌ **Solo datos sin contexto:** "p95 = 320ms" — ¿es bueno? ¿malo? Comparar con target y trend.
- ❌ **Reporte inconsistente:** Cada semana con formato diferente — difícil comparar trends.
- ❌ **Reporte que nadie lee:** Generar y enviar sin audience — verificar que alguien lo consume.

**Template:** `phases/07-operations/deliverables/weekly-report.md` *(pendiente)*

---

## 7.2 User Support (4 deliverables)

**Responsable:** Tech Lead | **Aprueba:** Product Owner

---

### 7.2.1 Support Process

| Campo | Valor |
|-------|-------|
| **Fase** | 7-Operations |
| **Subfase** | 7.2 User Support |
| **Responsable** | Tech Lead |
| **Ejecuta** | Tech Lead |
| **Aprueba** | Product Owner |
| **Formato** | Documento |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez + refinamientos |

**Perfil de ejecución:** Requiere definir el proceso end-to-end de soporte: canales, triage, escalation, y resolución.  
En VTT: un agente puede generar la documentación completa del proceso de soporte. Es altamente delegable.

**Qué es:** Definición del proceso de soporte técnico: cómo reportan los usuarios issues (email, in-app widget, chat), cómo se clasifican (bug, feature request, question, account issue), workflow de resolución (triage → assign → investigate → resolve → close → follow-up), escalation path (L1 → L2 → L3), y on-call rotation.

**Para qué sirve:** Sin proceso, los usuarios reportan por cualquier canal (Slack DM, email personal, Twitter), los issues se pierden, y nadie sabe quién es responsable de resolverlos. El proceso centraliza, prioriza, y asegura que cada issue tiene owner y SLA.

**Inputs requeridos:**
- Canales de comunicación con usuarios
- Equipo de soporte (o developers que hacen soporte)
- `3B.8.10` SLA Definition — SLAs como base para support SLAs

**Dependencias (predecessors):**
- Producto en producción (Fase 6)

**Habilita (successors):**
- `7.2.2` Ticket System — sistema configurado según el proceso
- `7.2.3` SLA Definitions — SLAs de soporte
- `7.3.1` Hotfix Process — bugs de soporte que necesitan hotfix

**Audiencia:**
- **Tech Lead** — ownership de soporte
- **Developers** — resuelven tickets escalados
- **Product Owner** — visibilidad de issues
- **Users** — saben cómo reportar

**Secciones esperadas:**
1. Canales de soporte (in-app widget, email, chat — cuáles están activos)
2. Clasificación de tickets (bug, feature request, question, account)
3. Workflow (triage → assign → investigate → resolve → close → follow-up)
4. Escalation path (L1: FAQ/self-service → L2: support team → L3: engineering)
5. On-call rotation (quién está disponible fuera de horario)
6. Communication templates (auto-responses, resolution messages)
7. Métricas de éxito (first response time, resolution time, CSAT)

**Criterio de completitud:**
- [ ] Canales definidos y configurados
- [ ] Clasificación de tickets documentada
- [ ] Workflow step-by-step
- [ ] Escalation path claro
- [ ] On-call rotation definida
- [ ] Comunicado al equipo y a los usuarios (cómo reportar)

**Anti-patrones:**
- ❌ **Soporte via Slack DMs:** Issues se pierden, no son trackeables, no tienen SLA.
- ❌ **Sin escalation path:** Todo llega a L3 (engineering) — developers hacen soporte L1.
- ❌ **Sin on-call:** Nadie responsable fuera de horario — critical bugs esperan al lunes.
- ❌ **Proceso documentado pero no seguido:** Existe en un doc pero nadie lo usa.

**Template:** `phases/07-operations/deliverables/support-process.md` *(pendiente)*

---

### 7.2.2 Ticket System

| Campo | Valor |
|-------|-------|
| **Fase** | 7-Operations |
| **Subfase** | 7.2 User Support |
| **Responsable** | Tech Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Product Owner |
| **Formato** | Config |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere configurar sistema de tickets con categorías, automations, y SLA tracking.  
En VTT: un agente puede configurar el ticket system y crear templates. Es altamente delegable.

**Qué es:** Sistema de tickets configurado (Jira Service Desk, Zendesk, Linear, Intercom, o GitHub Issues): categorías de ticket (bug, feature request, question, account), prioridades (critical/high/medium/low), automations (auto-assign por categoría, auto-label, SLA reminders), templates de ticket para usuarios, y SLA tracking integrado.

**Para qué sirve:** El ticket system es la "single source of truth" de soporte: cada issue tiene un ticket, un owner, un status, y un SLA. Sin ticket system, los issues viven en emails, Slack, y la memoria del equipo — se pierden.

**Inputs requeridos:**
- `7.2.1` Support Process — proceso a implementar en el sistema
- Tool seleccionada (Jira, Zendesk, Linear)

**Dependencias (predecessors):**
- `7.2.1` Support Process *(obligatorio)* — proceso que el sistema implementa

**Habilita (successors):**
- `7.2.4` Support Metrics — métricas del ticket system
- `7.3.3` Bug Tracking — bugs como tickets

**Audiencia:**
- **Support team** — herramienta de trabajo diario
- **Users** — donde reportan issues
- **Tech Lead** — oversight

**Secciones esperadas:**
1. Tool configurada (plataforma, plan, access)
2. Categorías y subcategorías de tickets
3. Prioridades con definición
4. Automations (auto-assign, auto-label, escalation triggers)
5. Templates de ticket para usuarios (bug report, feature request)
6. SLA tracking configurado
7. Integrations (Slack notifications, email inbound)

**Criterio de completitud:**
- [ ] Tool configurada y accesible
- [ ] Categorías y prioridades definidas
- [ ] Automations funcionales
- [ ] Templates de ticket creados
- [ ] SLA tracking activo
- [ ] Integrations configuradas (Slack, email)
- [ ] Users saben cómo crear tickets

**Anti-patrones:**
- ❌ **Tool sin automations:** Todo manual — triage toma horas.
- ❌ **Sin SLA tracking:** "¿Cuánto tardamos en responder?" — nadie sabe.
- ❌ **Ticket system que nadie usa:** Configurado pero los issues siguen llegando por Slack.

**Template:** `phases/07-operations/deliverables/ticket-system-config.md` *(pendiente)*

---

### 7.2.3 SLA Definitions

| Campo | Valor |
|-------|-------|
| **Fase** | 7-Operations |
| **Subfase** | 7.2 User Support |
| **Responsable** | Tech Lead |
| **Ejecuta** | Tech Lead |
| **Aprueba** | Product Owner |
| **Formato** | Documento |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez + revisiones anuales |

**Perfil de ejecución:** Requiere definir SLAs de soporte realistas y medibles.  
En VTT: un agente puede generar SLA definitions. Es altamente delegable.

**Qué es:** Definición de SLAs de soporte por prioridad: tiempo de primera respuesta (critical: 1h, high: 4h, medium: 1 business day, low: 3 business days), tiempo de resolución (critical: 4h, high: 1 day, medium: 3 days, low: 1 week), y escalation triggers (si SLA se acerca al límite, escalar automáticamente).

**Para qué sirve:** Sin SLAs, "respondemos cuando podemos" — el usuario espera indefinidamente. Los SLAs son un compromiso medible: el usuario sabe cuándo esperar respuesta, y el equipo tiene targets claros.

**Inputs requeridos:**
- `7.2.1` Support Process — proceso de soporte
- `3B.8.10` SLA Definition — SLAs del sistema como base
- Expectativas de usuarios / mercado

**Dependencias (predecessors):**
- `7.2.1` Support Process *(obligatorio)*

**Habilita (successors):**
- `7.2.2` Ticket System — SLA tracking configurado
- `7.2.4` Support Metrics — SLA compliance como métrica

**Audiencia:**
- **Tech Lead** — ownership
- **Product Owner** — compromiso con usuarios
- **Support team** — targets
- **Users** — expectativas (si se publican)

**Secciones esperadas:**
1. SLAs por prioridad (tabla: priority, first response, resolution, escalation)
2. Definición de cada prioridad (cuándo es critical vs high)
3. Business hours definition (24/7 o L-V 9-18)
4. Escalation triggers (SLA at 80% → notify, SLA at 100% → escalate)
5. SLA exceptions (maintenance windows, force majeure)
6. Review cadence (revisión anual de SLAs)

**Criterio de completitud:**
- [ ] SLAs por prioridad definidos
- [ ] Prioridades con definición clara
- [ ] Business hours definidos
- [ ] Escalation triggers configurados
- [ ] Aprobado por Product Owner
- [ ] Comunicado al equipo

**Anti-patrones:**
- ❌ **SLAs imposibles:** Critical response en 5 min con un equipo de 2 personas — no realista.
- ❌ **SLAs sin tracking:** Definidos pero nunca medidos — nadie sabe si se cumplen.
- ❌ **SLAs sin escalation:** Se vence el SLA y nadie se entera — sin consecuencia.
- ❌ **Todo es "critical":** Si todo es urgente, nada es urgente — definir claramente cada nivel.

**Template:** `phases/07-operations/deliverables/sla-definitions.md` *(pendiente)*

---

### 7.2.4 Support Metrics

| Campo | Valor |
|-------|-------|
| **Fase** | 7-Operations |
| **Subfase** | 7.2 User Support |
| **Responsable** | Tech Lead |
| **Ejecuta** | SRE |
| **Aprueba** | Product Owner |
| **Formato** | Dashboard |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día setup + automático |
| **Frecuencia** | Continua (dashboard) + semanal (review) |

**Perfil de ejecución:** Requiere configurar dashboard de métricas de soporte.  
En VTT: un agente puede configurar dashboards de support metrics. Es altamente delegable.

**Qué es:** Dashboard de métricas de soporte en tiempo real: tickets abiertos/cerrados (daily, weekly, monthly), average first response time, average resolution time, SLA compliance %, top issues (categorías más frecuentes), customer satisfaction (CSAT si se mide), y backlog de tickets abiertos.

**Para qué sirve:** Sin métricas, "el soporte va bien" es una opinión. Con métricas, es un dato: "first response promedio = 2.3h (SLA: 4h) ✅, resolution promedio = 18h (SLA: 24h) ✅, CSAT = 4.2/5". Las métricas revelan si el equipo de soporte está cumpliendo, si necesita más recursos, o si un tipo de issue es demasiado frecuente (señal de un bug o UX problem).

**Inputs requeridos:**
- `7.2.2` Ticket System — data source
- `7.2.3` SLA Definitions — targets para comparar

**Dependencias (predecessors):**
- `7.2.2` Ticket System *(obligatorio)* — data source
- `7.2.3` SLA Definitions *(obligatorio)* — targets

**Habilita (successors):**
- `7.1.4` Weekly Reports — support data
- Decisiones de staffing de soporte
- Product improvements (top issues → product backlog)

**Audiencia:**
- **Tech Lead** — oversight de soporte
- **Product Owner** — quality de soporte y top issues
- **Management** — SLA compliance

**Secciones esperadas:**
1. Ticket volume (daily/weekly/monthly, trend)
2. First response time (avg, vs SLA target)
3. Resolution time (avg, vs SLA target)
4. SLA compliance % (per priority)
5. Top issues by category (bug, feature request, question)
6. Backlog (open tickets by priority and age)
7. CSAT score (if measured)
8. Trend vs previous period

**Criterio de completitud:**
- [ ] Dashboard configurado y accesible
- [ ] Métricas clave visibles (volume, response time, resolution time)
- [ ] SLA compliance tracked
- [ ] Top issues identificados
- [ ] Dashboard reviewed semanalmente
- [ ] Auto-refresh configurado

**Anti-patrones:**
- ❌ **Métricas que nadie revisa:** Dashboard creado pero nunca consultado — desperdicio.
- ❌ **Sin SLA tracking:** "Respondemos rápido" sin dato que lo confirme.
- ❌ **Top issues ignorados:** El mismo issue reportado 50 veces sin fix — el soporte trata síntomas en vez de causas.

**Template:** `phases/07-operations/deliverables/support-metrics-dashboard.md` *(pendiente)*

---

## 7.3 Bug Fixes (3 deliverables)

**Responsable:** Developers | **Aprueba:** Tech Lead

---

### 7.3.1 Hotfix Process

| Campo | Valor |
|-------|-------|
| **Fase** | 7-Operations |
| **Subfase** | 7.3 Bug Fixes |
| **Responsable** | Tech Lead |
| **Ejecuta** | Tech Lead |
| **Aprueba** | Tech Lead |
| **Formato** | Documento |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere definir un "fast lane" para bugs críticos en producción, diferente del proceso normal de sprint.  
En VTT: un agente puede generar la documentación del proceso. Es altamente delegable.

**Qué es:** Proceso de cómo se manejan bugs críticos en producción: detección (Sentry alert, user report, monitoring) → triage (¿es crítico? ¿cuántos usuarios afecta?) → hotfix branch (hotfix/BUG-xxx from main) → fix implementation → expedited review (1 reviewer, fast-track) → deploy to staging → verify → deploy to production → verify → close ticket. Diferente del proceso normal: no espera al sprint, review más rápido, deploy directo.

**Para qué sirve:** Los bugs en producción afectan usuarios reales ahora — no pueden esperar al próximo sprint (2 semanas). El hotfix process define cómo resolver bugs críticos rápidamente pero de forma controlada (con review, tests, y verificación — no un push directo a main sin review).

**Inputs requeridos:**
- `4.7.7` Contributing Guide — branching strategy base
- `6.2.2` CD Pipeline — deploy pipeline
- `6.7.4` Rollback Runbook — si el hotfix falla

**Dependencias (predecessors):**
- Producto en producción
- CI/CD pipeline funcional (6.2)

**Habilita (successors):**
- `7.3.2` Hotfix Releases — releases ejecutadas con este proceso
- Resolución rápida de bugs críticos

**Audiencia:**
- **Developers** — ejecutan hotfixes
- **Tech Lead** — triage y approval
- **QA Lead** — verification
- **On-call team** — ejecución fuera de horario

**Secciones esperadas:**
1. Detection (cómo se detecta un bug que necesita hotfix: Sentry, alert, user report)
2. Triage criteria (cuándo es hotfix vs next sprint: critical = hotfix, medium = sprint)
3. Branching (hotfix/BUG-xxx from main)
4. Fix implementation (developer asignado, timeline: 4h para critical)
5. Expedited review (1 reviewer, 1h turnaround)
6. Deploy process (staging → verify → prod → verify)
7. Post-hotfix (regression test added, ticket closed, post-mortem si fue serio)
8. Communication (quién notifica a quién durante el proceso)

**Criterio de completitud:**
- [ ] Proceso documentado step-by-step
- [ ] Triage criteria claros (cuándo hotfix vs sprint)
- [ ] Branching strategy para hotfixes
- [ ] Expedited review process definido
- [ ] Deploy process para hotfixes
- [ ] Communication plan durante hotfix
- [ ] Conocido por todo el equipo

**Anti-patrones:**
- ❌ **Hotfix = push directo a main:** Sin PR, sin review, sin tests — introduce más bugs.
- ❌ **Todo es hotfix:** Features disfrazadas de hotfix — abuso del fast lane que degrada code quality.
- ❌ **Hotfix sin regression test:** Bug arreglado pero sin test — reaparece en el próximo refactor.
- ❌ **Sin post-mortem:** Hotfix tras hotfix sin entender root cause — Groundhog Day.

**Template:** `phases/07-operations/deliverables/hotfix-process.md` *(pendiente)*

---

### 7.3.2 Hotfix Releases

| Campo | Valor |
|-------|-------|
| **Fase** | 7-Operations |
| **Subfase** | 7.3 Bug Fixes |
| **Responsable** | Developers |
| **Ejecuta** | Developer asignado |
| **Aprueba** | Tech Lead |
| **Formato** | Code |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Variable (por bug) |
| **Frecuencia** | Por bug crítico |

**Perfil de ejecución:** Requiere implementar el fix, regression test, y deploy expedited siguiendo el hotfix process.  
En VTT: un agente puede generar fixes simples y regression tests. Bugs complejos requieren developer. Es parcialmente delegable.

**Qué es:** Releases de emergencia que corrigen bugs críticos en producción: versionadas (v1.0.1, v1.0.2 — patch version increment), con fix específico, regression test incluido, code review aprobado, y deployed a producción vía el CD pipeline. Cada hotfix release tiene: PR con root cause, fix, y test; changelog entry; y deploy log.

**Para qué sirve:** Convierte un bug crítico en producción en un fix deployed y verificado. Sin hotfix releases formales, los fixes son ad-hoc: "modifiqué el archivo en el server" — sin version control, sin test, sin rollback capability.

**Inputs requeridos:**
- `7.3.1` Hotfix Process — proceso a seguir
- Bug report con reproducción
- `6.2.2` CD Pipeline — deploy

**Dependencias (predecessors):**
- `7.3.1` Hotfix Process *(obligatorio)*
- Bug reportado y triaged como critical

**Habilita (successors):**
- Bug resuelto en producción
- Regression test permanente en la suite

**Audiencia:**
- **Developer** — implementa
- **Tech Lead** — review y approval
- **QA** — verification en prod
- **Users** — bug resuelto

**Secciones esperadas:**
1. PR con: root cause analysis, fix, regression test
2. Changelog entry (fix: description)
3. Version bump (patch: v1.0.x)
4. Deploy log (staging → verify → prod → verify)
5. Ticket closed con resolution notes

**Criterio de completitud:**
- [ ] Fix implementado y code-reviewed
- [ ] Regression test incluido
- [ ] Deployed a producción y verificado
- [ ] Changelog actualizado
- [ ] Ticket cerrado con resolution
- [ ] Post-mortem si el bug fue serio (afectó datos o downtime)

**Anti-patrones:**
- ❌ **Fix sin review:** "Es urgente, lo pusheo directo" — introduce más bugs.
- ❌ **Fix sin regression test:** El bug vuelve en 2 sprints.
- ❌ **Fix en el server sin PR:** No hay record del cambio — el próximo deploy lo sobrescribe.
- ❌ **Hotfix que cambia funcionalidad:** Aprovechar el hotfix para agregar features — scope creep peligroso.

**Template:** N/A — PRs en Git

---

### 7.3.3 Bug Tracking

| Campo | Valor |
|-------|-------|
| **Fase** | 7-Operations |
| **Subfase** | 7.3 Bug Fixes |
| **Responsable** | QA Lead |
| **Ejecuta** | QA Lead |
| **Aprueba** | Tech Lead |
| **Formato** | Jira/GitHub Issues |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Continuo |
| **Frecuencia** | Continua |

**Perfil de ejecución:** Requiere tracking continuo de bugs con clasificación, aging, y trend analysis.  
En VTT: un agente puede mantener el tracking, generar reportes de aging, y clasificar bugs. Es altamente delegable.

**Qué es:** Tracking continuo de todos los bugs en producción: cada bug en el ticket system con clasificación (severity: critical/high/medium/low, type: functional/performance/security/UX), aging (cuánto tiempo abierto), trend (creciendo o disminuyendo), y categorización por módulo. Incluye: triage meeting semanal para priorizar el backlog de bugs.

**Para qué sirve:** Sin tracking, los bugs se olvidan, se duplican, o se priorizan por "quién grita más fuerte". Con tracking, hay visibilidad: "tenemos 12 bugs open, 3 critical, el más viejo tiene 45 días". Informa sprint planning: "este sprint dedicamos 20% a bug fixes, priorizando los 3 critical".

**Inputs requeridos:**
- `7.1.3` Error Reports — bugs detectados por monitoring
- `7.2.2` Ticket System — bugs reportados por usuarios
- `6.6.5` Error Tracking — bugs de Sentry

**Dependencias (predecessors):**
- `7.2.2` Ticket System *(obligatorio)* — donde viven los bugs

**Habilita (successors):**
- Sprint planning — bugs como backlog items
- `7.3.1` Hotfix Process — critical bugs → hotfix

**Audiencia:**
- **QA Lead** — ownership del bug backlog
- **Tech Lead** — priorización
- **Developers** — bugs asignados
- **Product Owner** — visibilidad de deuda de calidad

**Secciones esperadas:**
1. Bug backlog en ticket system (todas las categorías y severities)
2. Triage meeting semanal (agenda, participants, output)
3. Bug aging report (tabla: severity, count, avg age, oldest)
4. Bug trend (new vs resolved per week)
5. Bug distribution by module
6. Sprint allocation recommendation (% de sprint para bugs)

**Criterio de completitud:**
- [ ] Todos los bugs conocidos en el ticket system
- [ ] Clasificados por severity y módulo
- [ ] Triage meeting semanal ejecutándose
- [ ] Aging report generado semanalmente
- [ ] Trend tracked (new vs resolved)
- [ ] Sprint planning incluye bug fix allocation

**Anti-patrones:**
- ❌ **Bugs fuera del tracker:** "Lo sé pero no lo registré" — bugs invisibles para el equipo.
- ❌ **Sin triage:** 100 bugs sin priorizar — developers no saben qué resolver primero.
- ❌ **Bug backlog que solo crece:** Más new que resolved cada semana — debt acumulándose.
- ❌ **Bugs sin severity:** Lista plana sin prioridad — critical se pierde entre los low.

**Template:** `phases/07-operations/deliverables/bug-tracking.md` *(pendiente)*

---

## Tabla resumen — Fase 7 Parte 1

| Subfase | Deliverables | Responsable | Delegable VTT |
|---------|-------------|-------------|---------------|
| 7.1 Monitoring | 4 | SRE | ✅ Reportes automáticos altamente delegables |
| 7.2 User Support | 4 | Tech Lead | ✅ Proceso, SLAs, y dashboard delegables |
| 7.3 Bug Fixes | 3 | Developers | 🔶 Proceso delegable, fixes complejos no |

---

## Siguiente archivo

**Próximo:** `DICCIONARIO_FASE_07_PARTE2_IMPROVEMENTS_SECURITY_SCALING.md` — 12 deliverables (7.4, 7.5, 7.6)
