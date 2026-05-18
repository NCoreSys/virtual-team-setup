# DICCIONARIO DE DELIVERABLES — FASE 7 (PARTE 2): OPERATIONS — IMPROVEMENTS, SECURITY, SCALING

**Versión:** 1.1  
**Fecha:** 2026-05-14  
**Fase:** 7 — Operations  
**Subfases en este archivo:** 7.4, 7.5, 7.6  
**Deliverables en este archivo:** 12  
**Responsable de fase:** SRE  
**Aprueba:** Tech Lead

---

## 7.4 Incremental Improvements (4 deliverables)

**Responsable:** Tech Lead | **Aprueba:** Product Owner

---

### 7.4.1 Minor Releases

| Campo | Valor |
|-------|-------|
| **Fase** | 7-Operations |
| **Subfase** | 7.4 Incremental Improvements |
| **Responsable** | Tech Lead |
| **Ejecuta** | Developers |
| **Aprueba** | Product Owner |
| **Formato** | Code |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Por sprint |
| **Frecuencia** | Por sprint (cada 1-2 semanas) |

**Perfil de ejecución:** Requiere release management: versionado semántico, changelog, regression testing, y deploy coordinado.  
En VTT: un agente puede generar release notes, actualizar changelog, y ejecutar release scripts. Es bastante delegable. La decisión de qué incluir en cada release requiere Product Owner.

**Qué es:** Releases regulares con mejoras incrementales post-launch: nuevas features (minor version: v1.1.0, v1.2.0), mejoras de UX, bug fixes no-critical, y performance improvements. Cada release con: changelog, release notes, regression testing, y deploy vía CD pipeline. Cadencia regular (cada sprint o bi-weekly).

**Para qué sirve:** El producto no termina en v1.0 — mejora continuamente. Los minor releases mantienen el producto fresco, resuelven feedback de usuarios, y cierran la brecha entre "lo que lanzamos" y "lo que los usuarios necesitan". Una cadencia regular genera confianza: los usuarios saben que el producto mejora activamente.

**Inputs requeridos:**
- Sprint backlog (features, improvements, bug fixes del sprint)
- `4.7.8` Changelog — actualización
- `6.2.2` CD Pipeline — deploy
- `5.6.1` E2E Test Suite — regression

**Dependencias (predecessors):**
- Producto en producción
- CI/CD pipeline funcional (6.2)
- `7.4.4` Improvement Backlog — items a incluir

**Habilita (successors):**
- Producto mejorado continuamente
- User satisfaction creciente
- Feedback loop cerrado (user report → fix → release → user happy)

**Audiencia:**
- **Product Owner** — decide qué va en cada release
- **Developers** — implementan
- **Users** — beneficiarios
- **Marketing** — comunicación de mejoras

**Secciones esperadas:**
1. Release cadence (cada sprint, bi-weekly, monthly)
2. Release process (feature freeze → regression → release notes → deploy)
3. Versioning strategy (semver: major.minor.patch)
4. Changelog format y actualización
5. Release notes (user-facing, non-technical)
6. Regression testing pre-release
7. Deploy process (staging → smoke → prod)
8. Communication plan (cómo se notifica a usuarios)

**Criterio de completitud:**
- [ ] Cadencia de release definida y cumplida
- [ ] Cada release con changelog entry
- [ ] Release notes publicadas
- [ ] Regression testing ejecutado pre-release
- [ ] Deployed sin issues
- [ ] Comunicado a usuarios (si hay cambios visibles)
- [ ] Versioning semántico aplicado

**Anti-patrones:**
- ❌ **Releases sin cadencia:** "Releaseamos cuando hay algo listo" — impredecible, no genera confianza.
- ❌ **Release sin regression:** Nuevo feature rompe feature existente — usuarios pierden confianza.
- ❌ **Release sin release notes:** Los usuarios no saben qué cambió — oportunidad perdida.
- ❌ **Big bang releases:** Acumular 3 meses de cambios en un release — riesgo alto, debugging difícil.

**Template:** `phases/07-operations/deliverables/minor-releases.md` *(pendiente)*

---

### 7.4.2 Feature Flags

| Campo | Valor |
|-------|-------|
| **Fase** | 7-Operations |
| **Subfase** | 7.4 Incremental Improvements |
| **Responsable** | Tech Lead |
| **Ejecuta** | Developers |
| **Aprueba** | Tech Lead |
| **Formato** | Config |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día setup + por feature |
| **Frecuencia** | Una vez setup + por feature |

**Perfil de ejecución:** Requiere implementar sistema de feature flags y usarlo en cada feature nueva.  
En VTT: un agente puede configurar el sistema de feature flags y agregar flags a features. Es bastante delegable.

**Qué es:** Sistema de feature flags (LaunchDarkly, Unleash, Flagsmith, o custom con env vars/DB) configurado y en uso: cada feature nueva se wrappea en un flag que permite: gradual rollout (1% → 10% → 50% → 100%), kill switch (desactivar sin deploy), targeting (habilitada para beta users, enterprise plan, o specific users), y A/B testing (variante A vs B).

**Para qué sirve:** Feature flags desacoplan "deploy" de "release": el código se deploya pero la feature está oculta hasta que se activa el flag. Esto permite: deploy diario sin riesgo (feature oculta), rollout gradual (detectar problemas con pocos usuarios), y kill switch instantáneo (desactivar sin deploy si algo falla).

**Inputs requeridos:**
- `3B.1.5` Technology Stack — tool de feature flags
- Features a wrappear con flags

**Dependencias (predecessors):**
- Producto en producción
- Tool seleccionada e instalada

**Habilita (successors):**
- `7.4.3` A/B Tests — flags como mecanismo de A/B
- Gradual rollout de features
- Kill switch para features problemáticas

**Audiencia:**
- **Developers** — implementan flags en código
- **Tech Lead** — governance de flags
- **Product Owner** — controla activation de features

**Secciones esperadas:**
1. Tool seleccionada y configurada (LaunchDarkly, Unleash, custom)
2. SDK integrado en backend y frontend
3. Flag naming convention (feature.module.name)
4. Flag types (boolean, percentage rollout, user targeting)
5. Flag lifecycle (create → activate → rollout → permanent → cleanup)
6. Dashboard de flags (active, percentage, targeting)
7. Cleanup process (remover flags viejos del código)

**Criterio de completitud:**
- [ ] Tool configurada y accesible
- [ ] SDK integrado en backend y frontend
- [ ] Naming convention definida
- [ ] Al menos 1 feature usando flags
- [ ] Dashboard de flags accesible por PO
- [ ] Cleanup process documentado (no acumular flags muertos)

**Anti-patrones:**
- ❌ **Flags sin cleanup:** 200 flags en el código, 180 permanentemente ON — código lleno de `if (flag)` muertos.
- ❌ **Solo boolean flags:** Pierden el poder de gradual rollout y targeting.
- ❌ **Flags hardcoded:** `if (process.env.FEATURE_X === 'true')` — no permite cambio sin deploy.
- ❌ **Sin governance:** Cualquiera crea flags sin convención — caos de naming y lifecycle.

**Template:** `phases/07-operations/deliverables/feature-flags.md` *(pendiente)*

---

### 7.4.3 A/B Tests

| Campo | Valor |
|-------|-------|
| **Fase** | 7-Operations |
| **Subfase** | 7.4 Incremental Improvements |
| **Responsable** | Product Owner |
| **Ejecuta** | Developers |
| **Aprueba** | Product Owner |
| **Formato** | Config |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Variable (por experimento) |
| **Frecuencia** | Por experimento |

**Perfil de ejecución:** Requiere definir hipótesis, variantes, métricas, sample size, y duration para cada experimento.  
En VTT: un agente puede configurar A/B tests técnicamente (flags, analytics events). El diseño del experimento (hipótesis, métricas) requiere Product Owner. Es parcialmente delegable.

**Qué es:** Framework de A/B testing para validar mejoras con datos: cada experimento tiene hipótesis ("el nuevo onboarding aumenta completion rate"), variantes (A: actual, B: nuevo), métrica primaria (completion rate), sample size (mínimo 1000 por variante para significancia), duration (2-4 semanas), y análisis de resultados (statistical significance).

**Para qué sirve:** "¿El nuevo diseño es mejor?" sin A/B testing es una opinión. Con A/B testing es un dato: "variante B aumentó conversión 12% (p < 0.05)". Permite decisiones data-driven sobre qué cambios mantener y cuáles revertir.

**Inputs requeridos:**
- `7.4.2` Feature Flags — mecanismo de variantes
- Analytics tool (Mixpanel, Amplitude, GA4)
- Hipótesis del Product Owner

**Dependencias (predecessors):**
- `7.4.2` Feature Flags *(obligatorio)* — mecanismo de split
- Analytics configurados

**Habilita (successors):**
- Decisiones data-driven sobre features
- Producto optimizado por datos, no por opiniones

**Audiencia:**
- **Product Owner** — diseño del experimento y decisión
- **Developers** — implementación de variantes
- **Data Analyst** — análisis de resultados (si hay)
- **UX Designer** — diseño de variantes

**Secciones esperadas:**
1. Experiment template (hipótesis, variantes, métrica primaria, sample size, duration)
2. Technical setup (flags para variantes, analytics events)
3. Sample size calculator (para significancia estadística)
4. Analysis process (cuándo leer resultados, qué herramienta)
5. Decision framework (si significativo → keep winner, si no → keep control)
6. Experiment log (historial de experimentos y resultados)

**Criterio de completitud:**
- [ ] Framework de A/B testing documentado
- [ ] Template de experimento creado
- [ ] Technical infrastructure lista (flags + analytics)
- [ ] Al menos 1 experimento ejecutado como validación
- [ ] Analysis process definido
- [ ] Experiment log iniciado

**Anti-patrones:**
- ❌ **A/B sin statistical significance:** "Variante B tuvo 3 más clicks" en 50 usuarios — no es significativo. Minimum sample size.
- ❌ **Peeking:** Mirar resultados cada día y parar cuando "se ve bien" — introduce bias. Definir duration upfront.
- ❌ **A/B sin hipótesis:** "Probemos y veamos" — sin hipótesis no hay aprendizaje.
- ❌ **Múltiples cambios en una variante:** Cambiar color, texto, y layout — no se sabe qué causó el efecto.
- ❌ **Never ship:** Experimento concluye pero nadie implementa el winner — datos sin acción.

**Template:** `phases/07-operations/deliverables/ab-tests.md` *(pendiente)*

---

### 7.4.4 Improvement Backlog

| Campo | Valor |
|-------|-------|
| **Fase** | 7-Operations |
| **Subfase** | 7.4 Incremental Improvements |
| **Responsable** | Product Owner |
| **Ejecuta** | Product Owner |
| **Aprueba** | Product Owner |
| **Formato** | Lista (Jira/Linear) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Continuo |
| **Frecuencia** | Continua |

**Perfil de ejecución:** Requiere mantener un backlog priorizado de mejoras post-launch.  
En VTT: un agente puede organizar, categorizar, y priorizar el backlog. Es bastante delegable. Las decisiones de priorización requieren Product Owner.

**Qué es:** Backlog de mejoras post-launch alimentado por múltiples fuentes: feedback de usuarios (7.2.4 Support Metrics → top issues), performance improvements (7.1.2 → endpoints lentos), UX improvements (analytics → drop-off points), tech debt (4.8.3 Technical Debt Log), feature requests (de usuarios y stakeholders), y resultados de A/B tests. Priorizado por impact × effort.

**Para qué sirve:** Sin backlog, las mejoras son reactivas: "un usuario importante se quejó, hay que cambiar esto YA". Con backlog priorizado, las mejoras son estratégicas: "estos 3 cambios impactan al 80% de los usuarios con 2 días de esfuerzo — son los próximos".

**Inputs requeridos:**
- `7.2.4` Support Metrics — top issues de soporte
- `7.1.2` Performance Reports — endpoints a optimizar
- `4.8.3` Technical Debt Log — tech debt a pagar
- `5.10.4` User Feedback — feedback de UAT
- `7.4.3` A/B Tests — resultados de experimentos
- Analytics data — user behavior insights
- Feature requests de stakeholders

**Dependencias (predecessors):**
- Producto en producción con datos de uso

**Habilita (successors):**
- `7.4.1` Minor Releases — items del backlog se implementan en releases
- Sprint planning — backlog como source de work items

**Audiencia:**
- **Product Owner** — ownership y priorización
- **Tech Lead** — feasibility y estimation
- **Developers** — implementación
- **Stakeholders** — visibilidad de roadmap

**Secciones esperadas:**
1. Backlog items en ticket system (Jira/Linear)
2. Categorías (UX improvement, performance, feature request, tech debt, bug fix)
3. Priorización framework (impact × effort matrix, RICE, MoSCoW)
4. Source tracking (de dónde vino cada item: support, analytics, stakeholder)
5. Sprint allocation (qué % del sprint va a improvements vs new features)
6. Roadmap trimestral (top priorities para los próximos 3 meses)
7. Review cadence (revisión quincenal del backlog)

**Criterio de completitud:**
- [ ] Backlog activo en ticket system
- [ ] Items categorizados y priorizados
- [ ] Fuentes de items documentadas
- [ ] Sprint allocation definida (e.g., 70% features, 20% improvements, 10% tech debt)
- [ ] Roadmap trimestral de mejoras
- [ ] Review quincenal del backlog
- [ ] Stakeholders informados de prioridades

**Anti-patrones:**
- ❌ **Backlog de 500 items:** Lista infinita que nadie revisa — archivar lo que no se hará en 6 meses.
- ❌ **HIPPO prioritization:** "El jefe quiere X" override data-driven priorities — usar framework de priorización.
- ❌ **Sin sprint allocation:** "Mejoras cuando haya tiempo" — nunca hay tiempo si no se planifica.
- ❌ **Solo features, sin improvements:** Agregar features sin mejorar las existentes — UX se degrada.
- ❌ **Backlog sin review:** Items de hace 1 año que ya no son relevantes — limpiar regularmente.

**Template:** `phases/07-operations/deliverables/improvement-backlog.md` *(pendiente)*

---

## 7.5 Security Updates (4 deliverables)

**Responsable:** Security Engineer | **Aprueba:** Tech Lead

---

### 7.5.1 Security Patches

| Campo | Valor |
|-------|-------|
| **Fase** | 7-Operations |
| **Subfase** | 7.5 Security Updates |
| **Responsable** | Security Engineer |
| **Ejecuta** | Developers |
| **Aprueba** | Tech Lead |
| **Formato** | Code |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Variable (por vulnerabilidad) |
| **Frecuencia** | Por vulnerabilidad descubierta |

**Perfil de ejecución:** Requiere evaluar severidad de la vulnerabilidad, implementar fix, y deploy expedited si es critical.  
En VTT: un agente puede implementar fixes de vulnerabilidades conocidas (OWASP patterns, dependency updates). Vulnerabilidades de lógica requieren developer. Es parcialmente delegable.

**Qué es:** Parches de seguridad para vulnerabilidades descubiertas post-launch: vulnerabilidades en código propio (OWASP violations, auth bypass, injection), vulnerabilidades reportadas por security researchers, y vulnerabilidades descubiertas en auditorías periódicas. Cada patch: evaluado por severity, implementado con fix + test, y deployed con urgencia proporcional (critical: 24h, high: 1 semana, medium: next sprint).

**Para qué sirve:** Las vulnerabilidades descubiertas post-launch son una carrera contra el tiempo: si un atacante las descubre antes de que se parcheen, puede explotarlas. El proceso de patching asegura que cada vulnerabilidad se evalúa, prioriza, arregla, y verifica rápidamente.

**Inputs requeridos:**
- `7.5.4` Vulnerability Reports — vulnerabilidades detectadas
- `7.5.3` Security Audits — findings de auditorías
- Security researcher reports (si hay bug bounty program)
- `6.2.2` CD Pipeline — deploy expedited

**Dependencias (predecessors):**
- Vulnerabilidad identificada

**Habilita (successors):**
- Sistema seguro post-patch
- `7.5.4` Vulnerability Reports — vulnerabilidad cerrada

**Audiencia:**
- **Security Engineer** — evaluación y oversight
- **Developers** — implementación del fix
- **Tech Lead** — approval y priorización

**Secciones esperadas:**
1. Patching process (detect → assess severity → prioritize → fix → test → deploy → verify)
2. Severity-based timeline (critical: 24h, high: 1 week, medium: next sprint, low: backlog)
3. Fix requirements (security review del fix, regression test, no new vulnerabilities introduced)
4. Deploy process para security patches (expedited, como hotfix)
5. Verification post-patch (re-scan, pentest the fix)
6. Disclosure timeline (si aplica — cuándo comunicar públicamente)

**Criterio de completitud:**
- [ ] Vulnerability assessed y severity asignada
- [ ] Fix implementado y security-reviewed
- [ ] Regression test incluido
- [ ] Deployed en timeline según severity
- [ ] Re-scan post-patch confirma fix
- [ ] Vulnerability cerrada en tracking

**Anti-patrones:**
- ❌ **Critical sin timeline:** "Lo arreglamos cuando podamos" para un SQL injection — es urgente.
- ❌ **Patch sin test:** Fix de seguridad que introduce un nuevo bug — trading one problem for another.
- ❌ **Patch sin verification:** "Lo arreglé" sin re-scan — ¿realmente se arregló?
- ❌ **Patch solo en prod, no en código:** Fix directo en server sin PR — el próximo deploy lo sobrescribe.

**Template:** `phases/07-operations/deliverables/security-patches.md` *(pendiente)*

---

### 7.5.2 Dependency Updates

| Campo | Valor |
|-------|-------|
| **Fase** | 7-Operations |
| **Subfase** | 7.5 Security Updates |
| **Responsable** | Security Engineer |
| **Ejecuta** | Developers |
| **Aprueba** | Tech Lead |
| **Formato** | Code |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día/mes |
| **Frecuencia** | Mensual (minor/patch) + trimestral (major) |

**Perfil de ejecución:** Requiere actualizar dependencias evaluando changelogs, breaking changes, y CVEs.  
En VTT: un agente puede ejecutar Dependabot/Renovate, evaluar changelogs, y crear PRs de actualización. Es altamente delegable para minor/patch updates. Major updates requieren developer.

**Qué es:** Actualización regular de dependencias del proyecto (npm, pip, Go modules): minor/patch updates mensuales (automáticos con Dependabot/Renovate), major updates trimestrales (manuales con changelog review y testing). Cada update: changelog reviewed, tests passing, no breaking changes, y deployed.

**Para qué sirve:** Las dependencias acumulan CVEs con el tiempo — una dependencia de hace 2 años puede tener 20+ vulnerabilidades conocidas. Las actualizaciones regulares mantienen el sistema seguro y evitan el "dependency hell" de actualizar 100 dependencias de golpe después de años de no hacerlo.

**Inputs requeridos:**
- `7.5.4` Vulnerability Reports — CVEs en dependencias
- Dependabot/Renovate configurado
- Package.json / requirements.txt

**Dependencias (predecessors):**
- Producto en producción con dependencias

**Habilita (successors):**
- Sistema libre de CVEs conocidas en dependencias
- `7.5.4` Vulnerability Reports — CVEs cerradas

**Audiencia:**
- **Security Engineer** — oversight
- **Developers** — implementación
- **Tech Lead** — approval de major updates

**Secciones esperadas:**
1. Update cadence (minor/patch: mensual automático, major: trimestral manual)
2. Tool configurada (Dependabot, Renovate, Snyk)
3. Process per update type:
   - Patch: auto-merge si tests pasan
   - Minor: review changelog, merge si no breaking
   - Major: manual review, changelog, testing, staged rollout
4. CVE-driven updates (urgente si CVE critical en dependency)
5. Lock file management (package-lock.json committed)
6. Update log (qué se actualizó, cuándo, por qué)

**Criterio de completitud:**
- [ ] Dependabot/Renovate configurado y activo
- [ ] Minor/patch updates ejecutados mensualmente
- [ ] Major updates revisados trimestralmente
- [ ] 0 CVEs critical/high en dependencias (o con timeline de fix)
- [ ] Lock file actualizado y commiteado
- [ ] Update log mantenido

**Anti-patrones:**
- ❌ **Nunca actualizar:** 2 años sin updates → 50+ CVEs, incompatibilidades masivas.
- ❌ **Actualizar todo de golpe:** 100 updates en un PR → imposible debuggear si algo falla.
- ❌ **Auto-merge major:** Major update auto-mergeado sin review → breaking changes en producción.
- ❌ **Ignorar Dependabot PRs:** 50 PRs de Dependabot abiertos sin merge → security debt.

**Template:** `phases/07-operations/deliverables/dependency-updates.md` *(pendiente)*

---

### 7.5.3 Security Audits

| Campo | Valor |
|-------|-------|
| **Fase** | 7-Operations |
| **Subfase** | 7.5 Security Updates |
| **Responsable** | Security Engineer |
| **Ejecuta** | Security Engineer / External Pentester |
| **Aprueba** | Solution Architect |
| **Formato** | Report |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 3-5 días (por auditoría) |
| **Frecuencia** | Anual o bi-anual |

**Perfil de ejecución:** Requiere auditoría de seguridad comprensiva: pentest, code review, infrastructure audit, y access review.  
En VTT: un agente puede ejecutar scans automatizados (SAST, DAST, dependency scan) y compilar resultados. El pentest manual requiere pentester humano o servicio externo. Es parcialmente delegable.

**Qué es:** Auditoría de seguridad periódica (anual o bi-anual) del sistema en producción: penetration testing externo (diferente del pre-launch 5.8.2 — ahora con datos reales y tráfico real), code review de seguridad (nuevas features desde la última auditoría), infrastructure audit (configuraciones, accesos, compliance), y access review (quién tiene acceso a qué, revocar accesos innecesarios).

**Para qué sirve:** Las features nuevas introducen nuevas vulnerabilidades. La infraestructura cambia y los accesos se acumulan. La auditoría periódica es un "health check" de seguridad que detecta lo que el equipo interno no ve (bias de familiaridad). Muchos estándares de compliance (SOC2, ISO27001, PCI-DSS) requieren auditorías periódicas.

**Inputs requeridos:**
- `3B.7.1` Security Plan — baseline de seguridad
- `5.8.2` Penetration Test Results — auditoría anterior como baseline
- Pentest provider (externo, independiente)
- Infrastructure access logs

**Dependencias (predecessors):**
- Producto en producción con historial de cambios

**Habilita (successors):**
- `7.5.1` Security Patches — findings → patches
- `7.5.4` Vulnerability Reports — findings reportados
- Compliance evidence (SOC2, ISO27001)

**Audiencia:**
- **Security Engineer** — ownership
- **Solution Architect** — findings arquitectónicos
- **Tech Lead** — findings de código
- **Management** — compliance status
- **Compliance** — evidence de auditoría

**Secciones esperadas:**
1. Audit scope (qué se auditó: app, infra, access, compliance)
2. Methodology (pentest, SAST, DAST, manual review, access review)
3. Findings (vulnerability, severity, evidence, exploitability, recommendation)
4. Comparison vs auditoría anterior (qué mejoró, qué empeoró, qué es nuevo)
5. Access review results (quién tiene acceso, quién no debería, revocations)
6. Compliance status (vs SOC2/ISO27001/PCI-DSS requirements)
7. Remediation timeline (cuándo se arregla cada finding)
8. Executive summary (para management)

**Criterio de completitud:**
- [ ] Pentest ejecutado por auditor externo/independiente
- [ ] Findings documentados con severity y evidence
- [ ] Access review completado con revocations ejecutadas
- [ ] Comparison vs auditoría anterior
- [ ] Remediation timeline definido
- [ ] Executive summary para management
- [ ] Compliance status evaluado

**Anti-patrones:**
- ❌ **Nunca auditar:** "Ya hicimos pentest antes del launch" — el sistema cambió desde entonces.
- ❌ **Auditoría interna solamente:** El equipo interno tiene bias — auditor externo es esencial.
- ❌ **Auditoría sin remediación:** 20 findings y 0 arreglados — teatro de seguridad.
- ❌ **Access review skip:** 10 ex-empleados con acceso a producción — risk innecesario.

**Template:** `phases/07-operations/deliverables/security-audit.md` *(pendiente)*

---

### 7.5.4 Vulnerability Reports

| Campo | Valor |
|-------|-------|
| **Fase** | 7-Operations |
| **Subfase** | 7.5 Security Updates |
| **Responsable** | Security Engineer |
| **Ejecuta** | Security Engineer |
| **Aprueba** | Tech Lead |
| **Formato** | Report |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Automático + 0.25 día review |
| **Frecuencia** | Continua (automático) + semanal (review) |

**Perfil de ejecución:** Requiere monitorear CVEs y scans de vulnerabilidades continuamente.  
En VTT: un agente puede ejecutar scans, compilar resultados, y generar reportes de vulnerabilidades. Es altamente delegable.

**Qué es:** Dashboard y reportes de vulnerabilidades conocidas del sistema: CVEs en dependencias (Snyk/Dependabot alerts), vulnerabilidades en container images (Trivy scan), vulnerabilidades en infraestructura (AWS Inspector, SecurityHub), y findings de auditorías (7.5.3). Cada vulnerabilidad con: severity, affected component, status (open/in-progress/resolved), y aging (cuánto tiempo abierta).

**Para qué sirve:** Nuevas CVEs se publican diariamente. Sin monitoreo continuo, una dependencia que era segura ayer puede tener una CVE critical hoy. El vulnerability dashboard da visibilidad en tiempo real del security posture del sistema: "tenemos 0 critical, 2 high (en progreso), 8 medium (backlog)".

**Inputs requeridos:**
- Snyk/Dependabot — CVEs en dependencias
- Trivy — vulnerabilidades en container images
- AWS Inspector/SecurityHub — infra vulnerabilities
- `7.5.3` Security Audits — findings de auditorías

**Dependencias (predecessors):**
- Herramientas de scanning configuradas

**Habilita (successors):**
- `7.5.1` Security Patches — vulnerabilidades a parchear
- `7.5.2` Dependency Updates — dependencias a actualizar
- Compliance evidence

**Audiencia:**
- **Security Engineer** — monitoring diario
- **Tech Lead** — priorización
- **Management** — security posture
- **Compliance** — evidence

**Secciones esperadas:**
1. Vulnerability dashboard (open by severity, trend, aging)
2. Dependency CVEs (tabla: package, CVE, severity, affected version, fix version, status)
3. Container image vulnerabilities
4. Infrastructure vulnerabilities
5. Audit findings status (open/resolved)
6. Aging report (vulnerabilities open > 30 days by severity)
7. Weekly review summary (new, resolved, escalated)

**Criterio de completitud:**
- [ ] Scanning tools configurados y corriendo
- [ ] Dashboard accesible
- [ ] 0 critical open > 24h
- [ ] 0 high open > 7 days
- [ ] Weekly review ejecutado
- [ ] Aging tracked
- [ ] Trend tracked (improving/degrading)

**Anti-patrones:**
- ❌ **Scans sin review:** 200 alerts que nadie mira — security theater.
- ❌ **Solo dependency scan:** Container images y infra no scanned — blind spots.
- ❌ **Critical open for weeks:** CVE critical en una dependency sin parchear — breach risk.
- ❌ **"Accept risk" sin documentar:** Marcar vulnerability como "won't fix" sin justificación.

**Template:** `phases/07-operations/deliverables/vulnerability-reports.md` *(pendiente)*

---

## 7.6 Scaling (4 deliverables)

**Responsable:** DevOps Lead | **Aprueba:** Solution Architect

---

### 7.6.1 Scaling Reports

| Campo | Valor |
|-------|-------|
| **Fase** | 7-Operations |
| **Subfase** | 7.6 Scaling |
| **Responsable** | DevOps Lead |
| **Ejecuta** | SRE |
| **Aprueba** | Solution Architect |
| **Formato** | Report |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día/mes |
| **Frecuencia** | Mensual |

**Perfil de ejecución:** Requiere analizar uso de recursos, scaling events, y growth trends.  
En VTT: un agente puede generar reportes de scaling desde CloudWatch/Grafana. Es altamente delegable.

**Qué es:** Reporte mensual de uso de recursos y scaling: CPU/RAM utilization trends por servicio, auto-scaling events (scale up/down count, triggers), request volume growth (MoM), database size growth, storage usage, y connection pool utilization. Indica si el sistema está: under-provisioned (near limits), right-sized, o over-provisioned (desperdicio).

**Para qué sirve:** Sin scaling reports, la capacidad del sistema es un misterio: "¿estamos al 30% o al 90% de capacidad?". Los reports revelan: trends de crecimiento (para planificar), waste (over-provisioned resources), y risk (near-limit resources que pueden causar outage).

**Inputs requeridos:**
- `6.6.4` Metrics Collection — usage data
- `6.6.1` Monitoring Dashboard — resource metrics
- Auto-scaling logs

**Dependencias (predecessors):**
- `6.6.4` Metrics Collection *(obligatorio)*

**Habilita (successors):**
- `7.6.2` Capacity Planning — trends informan projections
- `7.6.4` Cost Optimization — over-provisioning identificado
- `7.6.3` Auto-scaling Config — tuning basado en datos reales

**Audiencia:**
- **DevOps Lead** — resource management
- **Solution Architect** — capacity decisions
- **SRE** — operational awareness
- **Finance** — cost implications

**Secciones esperadas:**
1. Resource utilization summary (tabla: resource, current %, trend, status)
2. CPU/RAM utilization by service (avg, peak, trend)
3. Auto-scaling events (count, triggers, effectiveness)
4. Request volume growth (MoM %)
5. Database size growth (GB, MoM %)
6. Storage usage (GB, % of limit)
7. Connection pool utilization
8. Status assessment: under/right/over-provisioned per resource
9. Recommendations

**Criterio de completitud:**
- [ ] Métricas de todos los recursos principales
- [ ] Trends incluidos (no solo snapshot actual)
- [ ] Auto-scaling events documentados
- [ ] Status assessment per resource
- [ ] Recommendations accionables
- [ ] Generado mensualmente

**Anti-patrones:**
- ❌ **Sin report:** "Parece que estamos bien" — sin datos no se sabe.
- ❌ **Solo snapshot actual:** "CPU es 45% ahora" — ¿y el trend? ¿sube o baja?
- ❌ **Report sin recommendations:** Datos sin acción — el DevOps Lead no sabe qué ajustar.

**Template:** `phases/07-operations/deliverables/scaling-report.md` *(pendiente)*

---

### 7.6.2 Capacity Planning

| Campo | Valor |
|-------|-------|
| **Fase** | 7-Operations |
| **Subfase** | 7.6 Scaling |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Solution Architect |
| **Formato** | Documento |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día/trimestre |
| **Frecuencia** | Trimestral |

**Perfil de ejecución:** Requiere proyectar crecimiento basándose en trends y planificar cuándo escalar.  
En VTT: un agente puede calcular proyecciones y generar capacity plans. Es bastante delegable. Decisiones de inversión requieren management.

**Qué es:** Planificación trimestral de capacidad: proyección de crecimiento basada en trends actuales (users MoM, traffic MoM, data growth MoM), cuándo se necesitará más capacidad (a este ritmo, la BD se llena en 6 meses), qué componentes escalar primero, y scenario planning (normal growth, viral growth, seasonal peaks). Incluye: cost projection por scenario.

**Para qué sirve:** Sin capacity planning, el sistema se queda corto cuando crece (downtime por saturación de DB connections, disk full) o se sobre-provisiona (pagando 3x lo necesario). El capacity plan anticipa necesidades: "en 3 meses necesitaremos upgrade de DB instance y agregar un app server".

**Inputs requeridos:**
- `7.6.1` Scaling Reports — trends actuales
- `7.1.2` Performance Reports — performance trends
- Business projections (expected user growth)
- `3B.8.9` Cost Estimate — baseline de costos

**Dependencias (predecessors):**
- `7.6.1` Scaling Reports *(obligatorio)* — data de trends

**Habilita (successors):**
- Budget requests para scaling
- Infra provisioning antes de que se necesite
- `7.6.3` Auto-scaling Config — adjustment basado en projections

**Audiencia:**
- **Solution Architect** — capacity decisions
- **DevOps Lead** — planning
- **Management/Finance** — budget implications
- **Product Owner** — growth expectations

**Secciones esperadas:**
1. Current state (resource utilization summary)
2. Growth trends (users, traffic, data — MoM %)
3. Projections (3, 6, 12 months based on trends)
4. Capacity limits (cuándo se alcanza cada límite)
5. Scenario planning:
   - Normal: steady growth at current rate
   - Optimistic: 2x growth (viral, marketing push)
   - Peak: seasonal/event spikes
6. Scaling plan (qué escalar, cuándo, cómo)
7. Cost projection per scenario
8. Recommendations y timeline

**Criterio de completitud:**
- [ ] Trends documentados con data
- [ ] Projections a 3, 6, 12 meses
- [ ] Capacity limits identificados con timeline
- [ ] At least 2 scenarios (normal + optimistic)
- [ ] Cost projection por scenario
- [ ] Recommendations con timeline
- [ ] Actualizado trimestralmente

**Anti-patrones:**
- ❌ **Sin projections:** "Estamos al 60%, todo bien" — ¿y en 6 meses?
- ❌ **Solo un scenario:** "Crecemos al 5% mensual" — ¿y si hay un viral moment o un seasonal peak?
- ❌ **Planning sin cost:** "Necesitamos 3x servers" — ¿cuánto cuesta? ¿hay budget?
- ❌ **Planning sin action:** Proyectar que la BD se llena en 4 meses y no hacer nada — surprised pikachu face.

**Template:** `phases/07-operations/deliverables/capacity-planning.md` *(pendiente)*

---

### 7.6.3 Auto-scaling Config

| Campo | Valor |
|-------|-------|
| **Fase** | 7-Operations |
| **Subfase** | 7.6 Scaling |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Solution Architect |
| **Formato** | Config |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez + tuning continuo |

**Perfil de ejecución:** Requiere configurar y tunar auto-scaling basándose en datos reales de producción.  
En VTT: un agente puede generar y ajustar auto-scaling configs. Es altamente delegable.

**Qué es:** Configuración de auto-scaling tuned con datos reales de producción: métricas de trigger (CPU > 70%, request count > threshold, custom metric), min/max instances, cooldown periods, scaling policies (step scaling, target tracking), y scheduled scaling (si hay patrones predecibles: más instancias lunes-viernes 9-18, menos el fin de semana). Ajustado basándose en scaling events reales y performance data.

**Para qué sirve:** El auto-scaling inicial (6.1.2) se configuró con estimates. Ahora con datos reales, se puede tunar: "scale up a CPU 65% en vez de 80% porque el 80% ya causa latency spikes", "min instances = 3 en vez de 2 porque el traffic mínimo requiere 3", "scheduled scaling a las 8AM porque el traffic sube abruptamente".

**Inputs requeridos:**
- `7.6.1` Scaling Reports — scaling events y patterns
- `6.1.2` Servers Provisioned — config actual
- `7.1.2` Performance Reports — correlación scaling ↔ performance

**Dependencias (predecessors):**
- `6.1.2` Servers Provisioned *(obligatorio)* — config base
- `7.6.1` Scaling Reports *(obligatorio)* — data para tuning

**Habilita (successors):**
- Sistema que escala automáticamente con la demanda
- Performance estable bajo carga variable

**Audiencia:**
- **DevOps Lead** — configuración
- **SRE** — monitoring de scaling events

**Secciones esperadas:**
1. Current config (métricas, thresholds, min/max, cooldown)
2. Scaling events analysis (cuándo scale up/down, triggers, effectiveness)
3. Tuning changes (qué se ajustó y por qué)
4. Scheduled scaling (si hay patrones predecibles)
5. Target tracking vs step scaling (cuál funciona mejor)
6. Performance validation (latency stays within SLO during scale events)

**Criterio de completitud:**
- [ ] Auto-scaling configurado y funcional
- [ ] Tuned con datos reales (no solo estimates)
- [ ] Scaling events no causan latency spikes
- [ ] Min instances suficientes para traffic mínimo
- [ ] Max instances con budget approval
- [ ] Cooldown periods no causan flapping
- [ ] Scheduled scaling si hay patrones claros

**Anti-patrones:**
- ❌ **Auto-scaling nunca tuned:** Config del día 1 sin ajustar con datos reales — subóptimo.
- ❌ **Scale up a 95% CPU:** Demasiado tarde — latency ya degradada. Scale up a 65-75%.
- ❌ **Min = 1 instance:** Single point of failure durante low traffic — min = 2 para HA.
- ❌ **No testeado con load test:** Auto-scaling configurado pero nunca verificado bajo carga real.
- ❌ **Flapping:** Scale up → cooldown → scale down → scale up loop — ajustar cooldown y thresholds.

**Template:** `phases/07-operations/deliverables/auto-scaling-config.md` *(pendiente)*

---

### 7.6.4 Cost Optimization

| Campo | Valor |
|-------|-------|
| **Fase** | 7-Operations |
| **Subfase** | 7.6 Scaling |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Solution Architect |
| **Formato** | Report |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día/mes |
| **Frecuencia** | Mensual |

**Perfil de ejecución:** Requiere analizar costos de cloud, identificar waste, y recomendar optimizaciones.  
En VTT: un agente puede analizar billing data, identificar idle resources, y recomendar reservations/rightsizing. Es altamente delegable.

**Qué es:** Reporte mensual de costos de infraestructura: actual vs budget, costo por servicio/componente, trend MoM, idle resources (instances corriendo al 5% CPU, unused EBS volumes, old snapshots), reservation opportunities (RI vs on-demand savings), rightsizing recommendations (instance type optimization), y action plan con estimated savings.

**Para qué sirve:** Los costos de cloud tienden a crecer sin control: un dev spins up un test instance y no lo apaga, un snapshot acumula storage, un oversized instance corre al 10% CPU. El cost optimization report identifica waste y propone savings — typical savings: 20-40% del spend con rightsizing y reservations.

**Inputs requeridos:**
- Cloud billing data (AWS Cost Explorer, GCP Billing)
- `7.6.1` Scaling Reports — resource utilization
- `3B.8.9` Cost Estimate — budget original
- Reserved Instance/Savings Plan data

**Dependencias (predecessors):**
- `7.6.1` Scaling Reports *(obligatorio)* — utilization data
- Cloud billing access *(obligatorio)*

**Habilita (successors):**
- Budget savings
- Efficient resource usage
- Budget request informado para scaling

**Audiencia:**
- **DevOps Lead** — optimization execution
- **Solution Architect** — architecture decisions (cost-driven)
- **Finance/Management** — cost visibility y savings
- **Tech Lead** — cost awareness

**Secciones esperadas:**
1. Monthly spend summary (total, by service, by component)
2. Actual vs budget (over/under by how much)
3. Trend MoM (growing? stable? shrinking?)
4. Top cost drivers (qué componentes cuestan más)
5. Waste identified:
   - Idle resources (low utilization instances, unused volumes)
   - Oversized resources (can downsize)
   - Old snapshots/backups (can delete)
   - Non-production resources running 24/7 (can schedule)
6. Optimization recommendations:
   - Rightsizing (current → recommended instance type, savings)
   - Reserved Instances / Savings Plans (on-demand → RI savings)
   - Spot instances (for non-critical workloads)
   - Scheduled scaling (dev/staging off at night/weekends)
7. Estimated savings (total potential savings)
8. Action plan (what to do this month)

**Criterio de completitud:**
- [ ] Monthly spend documented
- [ ] Actual vs budget comparison
- [ ] Waste identified with $ amount
- [ ] Optimization recommendations with estimated savings
- [ ] Action plan for this month
- [ ] Savings from previous month's actions documented (ROI)
- [ ] Report distributed to Finance/Management

**Anti-patrones:**
- ❌ **Sin cost review:** Costs grow 30% MoM without anyone noticing until the annual review — "¿cómo gastamos $50K más?".
- ❌ **Report sin action:** Identify $2K/month waste and do nothing — data sin acción.
- ❌ **Over-optimization:** Cut costs so aggressively that performance suffers — save $100/month, risk $10K outage.
- ❌ **Solo on-demand:** Never evaluate RIs — leaving 30-40% savings on the table.
- ❌ **Dev/staging 24/7:** Non-production environments running at night and weekends — unnecessary cost.

**Template:** `phases/07-operations/deliverables/cost-optimization.md` *(pendiente)*

---

## Tabla resumen — Fase 7 Parte 2

| Subfase | Deliverables | Responsable | Delegable VTT |
|---------|-------------|-------------|---------------|
| 7.4 Incremental Improvements | 4 | Tech Lead / Product Owner | 🔶 Release management delegable, A/B test design requiere PO |
| 7.5 Security Updates | 4 | Security Engineer | ✅ Scans y updates altamente delegables |
| 7.6 Scaling | 4 | DevOps Lead | ✅ Reportes y configs altamente delegables |

---

## 🏁 DICCIONARIO DE DELIVERABLES — RESUMEN FINAL COMPLETO

| Fase | Archivos | Deliverables | Status |
|------|----------|-------------|--------|
| 0 Discovery | (previo) | 22 | ✅ |
| 1 Planning | (previo) | 33 | ✅ |
| 2 Analysis | (previo) | 47 | ✅ |
| 3A Design UX/UI | 9 | 72 | ✅ |
| 3B Design Technical | 9 | 73 | ✅ |
| 4 Development | 8 | 78 | ✅ |
| 5 Testing | 11 | 52 | ✅ |
| 6 Deploy | 1 | 38 | ✅ |
| 7 Operations | 2 | 23 | ✅ |
| **TOTAL** | **40+ archivos** | **438** | **✅ COMPLETO** |
