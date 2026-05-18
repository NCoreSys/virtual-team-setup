# DICCIONARIO DE DELIVERABLES — FASE 5.8: SECURITY TESTING

**Versión:** 1.1  
**Fecha:** 2026-05-14  
**Fase:** 5 — Testing  
**Subfase:** 5.8 — Security Testing  
**Total deliverables:** 7  
**Responsable de subfase:** Security Engineer  
**Aprueba:** Solution Architect

---

### 5.8.1 Security Test Plan

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.8 Security Testing |
| **Responsable** | Security Engineer |
| **Ejecuta** | Security Engineer |
| **Aprueba** | Solution Architect |
| **Formato** | Documento |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere experiencia en security testing: OWASP methodology, SAST, DAST, pentesting.  
En VTT: un agente puede generar el plan basándose en el Security Plan y OWASP checklist. Es bastante delegable.

**Qué es:** Plan de pruebas de seguridad: qué se testea (OWASP Top 10, auth/authz, data protection, input validation, rate limiting, CORS, CSRF, file upload), cómo (SAST con SonarQube, DAST con OWASP ZAP, manual pentesting), con qué herramientas, y scope (endpoints, flujos de auth, datos sensibles, admin panel).

**Para qué sirve:** Define el approach sistemático — no solo "escanear con ZAP y ver qué sale". Cubre las categorías de vulnerabilidades relevantes para este proyecto específico basándose en su arquitectura y datos.

**Inputs requeridos:**
- `3B.7.1` Security Plan — controles a verificar
- `3B.7.6` OWASP Checklist — vulnerabilidades a testear
- `3B.4.1` OpenAPI Spec — endpoints a testear
- `3B.7.3` Auth Flow — autenticación a verificar

**Dependencias (predecessors):**
- `3B.7.1` Security Plan *(obligatorio)*
- `3B.7.6` OWASP Checklist *(obligatorio)*

**Habilita (successors):**
- `5.8.2` a `5.8.7` — ejecución del plan

**Audiencia:**
- **Security Engineer** — guía de ejecución
- **Tech Lead** — validación de scope
- **Solution Architect** — aprobación

**Secciones esperadas:**
1. Scope de security testing (qué se testea, qué no)
2. Metodología por tipo (SAST, DAST, manual pentest)
3. OWASP Top 10 test cases (por cada categoría)
4. Auth/authz test scenarios (login, logout, token expiry, RBAC, IDOR)
5. Data protection tests (encryption at rest/transit, PII handling)
6. Input validation tests (injection, XSS, file upload)
7. Rate limiting y abuse prevention tests
8. Herramientas y configuración
9. Schedule de ejecución

**Criterio de completitud:**
- [ ] OWASP Top 10 cubierto con test cases específicos
- [ ] Auth/authz scenarios definidos
- [ ] Data protection scenarios definidos
- [ ] Herramientas seleccionadas y configuradas
- [ ] Schedule definido
- [ ] Aprobado por Solution Architect

**Anti-patrones:**
- ❌ **Solo DAST scan:** Un scan automatizado no reemplaza testing manual de lógica de auth (IDOR, privilege escalation).
- ❌ **Security testing al final del proyecto:** Demasiado tarde para arreglar issues arquitectónicos.
- ❌ **Plan genérico:** "Testear OWASP Top 10" sin test cases específicos para este proyecto.

**Template:** `phases/05-testing/deliverables/security-test-plan.md` *(pendiente)*

---

### 5.8.2 Penetration Test Results

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.8 Security Testing |
| **Responsable** | Security Engineer |
| **Ejecuta** | Security Engineer / External pentester |
| **Aprueba** | Solution Architect |
| **Formato** | Report |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 3-5 días |
| **Frecuencia** | Pre-release + anual |

**Perfil de ejecución:** Requiere pentesting manual: intentar explotar vulnerabilidades como un atacante real.  
En VTT: un agente NO puede hacer pentesting real (requiere interacción con la app live). Puede formatear resultados y generar reportes. Necesita pentester humano o servicio externo.

**Qué es:** Resultados de pruebas de penetración: por cada técnica intentada (SQL injection, XSS, CSRF, IDOR, auth bypass, privilege escalation, path traversal, SSRF), el resultado (vulnerable/no vulnerable), severity si vulnerable (critical/high/medium/low), evidence (screenshot, request/response), y recommendation de fix.

**Para qué sirve:** El pentesting encuentra lo que los scanners no: lógica de negocio explotable ("puedo cambiar el precio de un producto editando el request"), auth bypass via flujo inesperado ("resetear password de otro usuario cambiando el userId en la URL"), y IDOR que requiere razonamiento ("acceder a las facturas de otro usuario cambiando el ID en la API").

**Inputs requeridos:**
- `5.8.1` Security Test Plan — scope y metodología
- Aplicación deployed en test environment
- Credenciales de test (roles diferentes para probar authz)

**Dependencias (predecessors):**
- `5.8.1` Security Test Plan *(obligatorio)*
- `5.3.1` Test Environment *(obligatorio)*

**Habilita (successors):**
- `5.8.5` Security Findings — findings consolidados
- `5.8.6` Remediation Plan — plan de corrección

**Audiencia:**
- **Security Engineer** — análisis
- **Solution Architect** — architecture findings
- **Tech Lead** — code findings
- **Backend Developer** — fixes

**Secciones esperadas:**
1. Methodology (herramientas, approach, tiempo invertido)
2. Scope testeado (endpoints, flujos, roles)
3. Findings (tabla: ID, vulnerability, severity, evidence, exploitability, recommendation)
4. Passed tests (qué se probó y NO es vulnerable — evidencia de testing)
5. OWASP coverage (qué categorías se cubrieron)
6. Risk rating (overall security posture)

**Criterio de completitud:**
- [ ] OWASP Top 10 testeado
- [ ] Auth/authz testeado (IDOR, privilege escalation, token manipulation)
- [ ] Evidence per finding (request/response, screenshot)
- [ ] Severity clasificada (CVSS o Critical/High/Medium/Low/Info)
- [ ] Recommendation per finding
- [ ] Passed tests documentados (no solo lo que falló)

**Anti-patrones:**
- ❌ **Solo automated scan:** No reemplaza razonamiento humano para IDOR y business logic.
- ❌ **Pentest en producción sin autorización:** Legal y operational risk.
- ❌ **Findings sin evidence:** "SQL injection posible" sin demostrar cómo — no verificable.
- ❌ **Sin severity:** Todos los findings parecen iguales — imposible priorizar.

**Template:** `phases/05-testing/deliverables/pentest-results.md` *(pendiente)*

---

### 5.8.3 Vulnerability Scan

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.8 Security Testing |
| **Responsable** | Security Engineer |
| **Ejecuta** | Security Engineer |
| **Aprueba** | Solution Architect |
| **Formato** | Report |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Pre-release + periódico |

**Perfil de ejecución:** Requiere ejecutar herramientas de scanning automatizado y analizar resultados.  
En VTT: un agente puede ejecutar OWASP ZAP, Snyk, Trivy, y compilar resultados. Es altamente delegable.

**Qué es:** Resultado de escaneos automatizados de seguridad en 3 niveles: SAST (código fuente — SonarQube security rules, Semgrep), DAST (aplicación corriendo — OWASP ZAP active scan), y dependencias (Snyk, npm audit, Trivy para container images). Cada finding con: severity, CVE ID (si aplica), affected component/file, y fix recommendation.

**Para qué sirve:** Los scans automatizados detectan vulnerabilidades conocidas a escala: un humano no puede revisar 500 dependencias manualmente, pero Snyk sí. Detectan: CVEs en dependencias, patrones inseguros en código (eval(), SQL string concatenation), y vulnerabilidades en la app corriendo (headers faltantes, CORS mal configurado).

**Inputs requeridos:**
- Código fuente (para SAST)
- Aplicación deployed (para DAST)
- `5.8.1` Security Test Plan — herramientas configuradas
- Container images (para Trivy)

**Dependencias (predecessors):**
- `5.8.1` Security Test Plan *(obligatorio)*
- Código y app deployed *(obligatorio)*

**Habilita (successors):**
- `5.8.5` Security Findings — findings consolidados
- `5.8.6` Remediation Plan — CVEs a remediar

**Audiencia:**
- **Security Engineer** — análisis de resultados
- **Backend Developer** — código a corregir
- **DevOps Lead** — container/infra findings

**Secciones esperadas:**
1. SAST results (SonarQube/Semgrep — código inseguro)
2. DAST results (OWASP ZAP — vulnerabilidades en app corriendo)
3. Dependency scan results (Snyk/npm audit — CVEs en dependencias)
4. Container scan results (Trivy — vulnerabilidades en images)
5. Por finding: severity, CVE, component, description, fix
6. Summary (total by severity, new vs known)

**Criterio de completitud:**
- [ ] SAST ejecutado en todo el código
- [ ] DAST ejecutado contra la app corriendo
- [ ] Dependency scan ejecutado
- [ ] Container scan ejecutado (si usa containers)
- [ ] Findings clasificados por severity
- [ ] False positives marcados y justificados

**Anti-patrones:**
- ❌ **Scan sin análisis:** 200 findings sin revisar — muchos son false positives.
- ❌ **Solo dependency scan:** Ignora vulnerabilidades en código propio y en la app corriendo.
- ❌ **Scan sin remediación:** Encontrar 50 CVEs y no arreglar ninguno — scan sin valor.

**Template:** `phases/05-testing/deliverables/vulnerability-scan.md` *(pendiente)*

---

### 5.8.4 OWASP Compliance

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.8 Security Testing |
| **Responsable** | Security Engineer |
| **Ejecuta** | Security Engineer |
| **Aprueba** | Solution Architect |
| **Formato** | Checklist |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Pre-release |

**Perfil de ejecución:** Requiere evaluar cada categoría del OWASP Top 10 con evidence de testing.  
En VTT: un agente puede compilar resultados de pentest y scans contra la checklist OWASP. Es bastante delegable.

**Qué es:** Actualización del OWASP Checklist (3B.7.6) post-testing: cada vulnerabilidad del OWASP Top 10 marcada como PASS/FAIL/PARTIAL con evidence de cómo se verificó. Es la "auditoría" de que los controles de seguridad planificados en fase de design realmente funcionan en la implementación.

**Para qué sirve:** El OWASP Checklist del design (3B.7.6) dice "implementaremos protección contra SQL injection". El OWASP Compliance post-testing verifica: "sí, se implementó, y lo verificamos con pentest y SAST — PASS" o "no, encontramos SQL injection en el endpoint X — FAIL".

**Inputs requeridos:**
- `3B.7.6` OWASP Checklist — checklist original
- `5.8.2` Penetration Test Results — evidence manual
- `5.8.3` Vulnerability Scan — evidence automatizada

**Dependencias (predecessors):**
- `3B.7.6` OWASP Checklist *(obligatorio)*
- `5.8.2` Penetration Test Results *(obligatorio)*
- `5.8.3` Vulnerability Scan *(obligatorio)*

**Habilita (successors):**
- `5.8.5` Security Findings — findings de OWASP violations
- `5.8.7` Security Sign-off — evidence de compliance

**Audiencia:**
- **Security Engineer** — evaluación
- **Solution Architect** — compliance review
- **Compliance** — evidence de adherencia a OWASP

**Secciones esperadas:**
1. OWASP Top 10 compliance table (categoría, control, status PASS/FAIL/PARTIAL, evidence, notes)
2. A01:2021 Broken Access Control — status + evidence
3. A02:2021 Cryptographic Failures — status + evidence
4. A03:2021 Injection — status + evidence
5. A04:2021 Insecure Design — status + evidence
6. A05:2021 Security Misconfiguration — status + evidence
7. A06:2021 Vulnerable Components — status + evidence
8. A07:2021 Auth Failures — status + evidence
9. A08:2021 Software/Data Integrity — status + evidence
10. A09:2021 Logging/Monitoring Failures — status + evidence
11. A10:2021 SSRF — status + evidence
12. Overall OWASP compliance score

**Criterio de completitud:**
- [ ] Las 10 categorías evaluadas con evidence
- [ ] Cada categoría tiene status claro (PASS/FAIL/PARTIAL)
- [ ] FAILs tienen finding referenciado
- [ ] Evidence documentada por categoría
- [ ] Overall score calculado

**Anti-patrones:**
- ❌ **"Todo PASS" sin evidence:** Self-certification sin pruebas — no es compliance real.
- ❌ **OWASP checklist sin actualizar post-testing:** La checklist de design no refleja la realidad post-testing.
- ❌ **PARTIAL sin plan:** "Partially compliant" sin explicar qué falta y cuándo se completa.

**Template:** `phases/05-testing/deliverables/owasp-compliance.md` *(pendiente)*

---

### 5.8.5 Security Findings

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.8 Security Testing |
| **Responsable** | Security Engineer |
| **Ejecuta** | Security Engineer |
| **Aprueba** | Solution Architect |
| **Formato** | Lista |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Post-testing |

**Perfil de ejecución:** Requiere consolidar todos los hallazgos de todas las fuentes de security testing.  
En VTT: un agente puede consolidar findings de múltiples fuentes y priorizar. Es altamente delegable.

**Qué es:** Lista consolidada de TODOS los hallazgos de seguridad de todas las fuentes: pentest manual (5.8.2), vulnerability scans (5.8.3), y OWASP audit (5.8.4). Cada finding con: ID único, severity (CVSS o Critical/High/Medium/Low), description, affected component, evidence, exploitability (easy/medium/hard), y recommendation. Priorizada por risk score (severity × exploitability).

**Para qué sirve:** Sin consolidación, los findings están dispersos en 3 reportes diferentes. La lista consolidada permite: ver el panorama completo de seguridad, priorizar por risk (un high que es fácil de explotar es más urgente que un critical difícil de explotar), y trackear remediación.

**Inputs requeridos:**
- `5.8.2` Penetration Test Results — findings manuales
- `5.8.3` Vulnerability Scan — findings automatizados
- `5.8.4` OWASP Compliance — OWASP violations

**Dependencias (predecessors):**
- `5.8.2` Penetration Test Results *(obligatorio)*
- `5.8.3` Vulnerability Scan *(obligatorio)*
- `5.8.4` OWASP Compliance *(obligatorio)*

**Habilita (successors):**
- `5.8.6` Remediation Plan — findings a remediar
- `5.8.7` Security Sign-off — input para decisión

**Audiencia:**
- **Security Engineer** — ownership
- **Solution Architect** — review
- **Tech Lead** — priorización de fixes
- **Management** — security posture overview

**Secciones esperadas:**
1. Findings summary (total by severity, by source, by exploitability)
2. Consolidated findings table (ID, severity, source, description, component, exploitability, risk score)
3. Top 5 findings by risk (detailed description + recommendation)
4. Findings by category (auth, injection, config, dependencies, etc.)
5. False positives documented (finding, why false positive, evidence)
6. Comparison vs previous assessment (if exists)

**Criterio de completitud:**
- [ ] Findings de todas las fuentes consolidados
- [ ] Cada finding tiene severity + exploitability = risk score
- [ ] Priorizado por risk score
- [ ] Duplicates merged (mismo issue de pentest y scan)
- [ ] False positives marcados con justificación
- [ ] Top 5 findings con detalle y recommendation

**Anti-patrones:**
- ❌ **Findings sin priorización:** Lista plana de 30 findings sin risk score — ¿cuál resolver primero?
- ❌ **Findings duplicados:** Mismo issue reportado por scan y pentest como 2 findings separados — merge.
- ❌ **Sin exploitability:** Severity sin exploitability — un critical difícil de explotar puede ser menos urgente que un high fácil.

**Template:** `phases/05-testing/deliverables/security-findings.md` *(pendiente)*

---

### 5.8.6 Remediation Plan

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.8 Security Testing |
| **Responsable** | Security Engineer |
| **Ejecuta** | Backend Developer / DevOps Lead |
| **Aprueba** | Solution Architect |
| **Formato** | Documento |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5-1 día |
| **Frecuencia** | Post-testing |

**Perfil de ejecución:** Requiere crear plan de remediación por finding con timeline, assignee, y verification method.  
En VTT: un agente puede generar el plan con recommendations. Es bastante delegable.

**Qué es:** Plan para remediar cada security finding: fix description (qué hacer técnicamente), assignee (quién lo arregla), deadline (cuándo — basado en severity: critical pre-release, high 1 semana, medium next sprint), effort estimate, y verification method (cómo confirmar que se arregló: re-scan, re-test, code review).

**Para qué sirve:** Sin plan, los findings se archivan y nadie los arregla. El plan traduce "50 vulnerabilidades encontradas" en "3 critical arreglamos antes del release, 8 high en sprint 1 post-launch, 15 medium en backlog".

**Inputs requeridos:**
- `5.8.5` Security Findings — findings a remediar

**Dependencias (predecessors):**
- `5.8.5` Security Findings *(obligatorio)*

**Habilita (successors):**
- `5.8.7` Security Sign-off — critical remediados para sign-off
- Remediation execution

**Audiencia:**
- **Tech Lead** — priorización y assignment
- **Backend Developer** — fixes a implementar
- **DevOps Lead** — infra/config fixes
- **Security Engineer** — verification

**Secciones esperadas:**
1. Remediation table (finding ID, severity, fix description, assignee, deadline, effort, verification method, status)
2. Pre-release remediations (critical — must fix before launch)
3. Post-release remediations (high/medium — timeline documentado)
4. Accepted risks (findings que no se arreglan con justificación)
5. Verification schedule (cuándo se re-testea cada fix)

**Criterio de completitud:**
- [ ] Cada finding tiene remediation plan
- [ ] Critical findings con deadline pre-release
- [ ] Assignees definidos para cada fix
- [ ] Verification method por fix
- [ ] Accepted risks justificados y aprobados por Solution Architect
- [ ] Timeline realista

**Anti-patrones:**
- ❌ **"Lo arreglamos después del launch":** Critical findings diferidos — breach risk.
- ❌ **Plan sin assignee:** "Hay que arreglar X" — ¿quién?
- ❌ **Plan sin verification:** "Arreglado" sin re-testear — ¿realmente se arregló?
- ❌ **Accept risk sin justificación:** Cerrar findings como "won't fix" sin explicar por qué.

**Template:** `phases/05-testing/deliverables/remediation-plan.md` *(pendiente)*

---

### 5.8.7 Security Sign-off

| Campo | Valor |
|-------|-------|
| **Fase** | 5-Testing |
| **Subfase** | 5.8 Security Testing |
| **Responsable** | Security Engineer |
| **Ejecuta** | Security Engineer |
| **Aprueba** | Solution Architect |
| **Formato** | Sign-off |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.25 día |
| **Frecuencia** | Pre-release |

**Perfil de ejecución:** Requiere autoridad para declarar "el sistema es suficientemente seguro para release".  
En VTT: un agente puede compilar el sign-off document con datos de findings y remediación. NO puede tomar la decisión. Es parcialmente delegable.

**Qué es:** Aprobación formal de seguridad para release: confirma que critical findings están remediados y verificados, high findings tienen plan con deadline, OWASP compliance es aceptable, riesgo residual está documentado y es aceptable, y el sistema cumple los requisitos mínimos de seguridad para producción. Firmado por Security Engineer y Solution Architect.

**Para qué sirve:** Gate de seguridad antes de producción. Sin sign-off, el sistema se deploya con vulnerabilidades conocidas sin evaluación formal de riesgo. El sign-off documenta: "evaluamos la seguridad, estos son los riesgos residuales, y decidimos que son aceptables para launch".

**Inputs requeridos:**
- `5.8.5` Security Findings — estado actual de findings
- `5.8.6` Remediation Plan — critical remediados
- `5.8.4` OWASP Compliance — compliance status

**Dependencias (predecessors):**
- `5.8.6` Remediation Plan *(obligatorio)* — critical remediados

**Habilita (successors):**
- `6.5.1` Production Deploy — gate de entrada

**Audiencia:**
- **Solution Architect** — aprobador
- **Security Engineer** — evaluador
- **Tech Lead** — coordinación
- **Management** — risk acceptance

**Secciones esperadas:**
1. Security testing summary (qué se hizo: pentest, scans, OWASP audit)
2. Findings summary (total, by severity, remediated, open, accepted)
3. Critical findings: all remediated ✅ (con evidence)
4. High findings: plan with deadline ✅
5. OWASP compliance status
6. Residual risk assessment (qué riesgos quedan y por qué son aceptables)
7. Conditions (if any: "approved with condition that X is fixed by date Y")
8. Go/No-go decision
9. Signatures (Security Engineer + Solution Architect)

**Criterio de completitud:**
- [ ] Critical findings: 0 open (todos remediados y verificados)
- [ ] High findings: todos con plan y deadline
- [ ] OWASP compliance evaluado
- [ ] Residual risk documentado y aceptado
- [ ] Decision documentada (go/no-go/conditional)
- [ ] Firmado por Security Engineer y Solution Architect

**Anti-patrones:**
- ❌ **Sign-off sin remediation:** Aprobar con critical findings abiertos.
- ❌ **Sign-off sin pentest:** Basarse solo en scans automatizados — incompleto.
- ❌ **Sign-off sin residual risk:** "Todo está bien" — siempre hay riesgo residual, documentarlo.
- ❌ **Forced sign-off:** "Tenemos deadline" — Security Engineer debe poder decir no-go.

**Template:** `phases/05-testing/deliverables/security-signoff.md` *(pendiente)*

---

## Tabla resumen — Fase 5.8

| Deliverable | Responsable | Delegable VTT |
|-------------|-------------|---------------|
| 5.8.1 Security Test Plan | Security Engineer | ✅ |
| 5.8.2 Penetration Test Results | Security Engineer / External | ❌ — requiere pentester humano |
| 5.8.3 Vulnerability Scan | Security Engineer | ✅ — ejecutar herramientas y reportar |
| 5.8.4 OWASP Compliance | Security Engineer | 🔶 — compilar sí, evaluar requiere juicio |
| 5.8.5 Security Findings | Security Engineer | ✅ — consolidar findings |
| 5.8.6 Remediation Plan | Security Engineer | ✅ — generar plan |
| 5.8.7 Security Sign-off | Security Engineer | ❌ — decisión humana |
