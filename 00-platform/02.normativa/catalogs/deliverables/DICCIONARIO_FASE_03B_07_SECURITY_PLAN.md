# DICCIONARIO DE DELIVERABLES — FASE 3B.7: SECURITY PLAN

**Versión:** 1.0  
**Fecha:** 2026-05-14  
**Fase:** 3B — Design Technical  
**Subfase:** 3B.7 — Security Plan  
**Total deliverables:** 11  
**Responsable de subfase:** Security Engineer  
**Aprueba:** Solution Architect

---

## Contexto de la subfase

Security Plan define la estrategia completa de seguridad del sistema: cómo se autentican los usuarios, cómo se autorizan las operaciones, cómo se protegen los datos en tránsito y en reposo, cómo se previenen las vulnerabilidades más comunes (OWASP Top 10), y cómo se responde a incidentes. La seguridad no es una feature — es un cross-cutting concern que permea toda la arquitectura.

**Prerequisitos de subfase:**
- Solution Architecture (3B.1) — superficie de ataque identificada
- API Design (3B.4) — auth/authz specs
- Database Design (3B.3) — datos sensibles identificados

**Entrega de subfase:**
- Plan de seguridad completo y accionable, listo para implementar en desarrollo

---

### 3B.7.1 Security Plan

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.7 Security Plan |
| **Responsable** | Security Engineer |
| **Ejecuta** | Security Engineer |
| **Aprueba** | Solution Architect |
| **Formato** | MD/PDF |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 2-3 días |
| **Frecuencia** | Una vez + actualizaciones por cambio arquitectónico |

**Perfil de ejecución:** Requiere experiencia en seguridad de aplicaciones: threat modeling, security architecture, compliance frameworks, y defense in depth.  
En VTT: un agente puede generar la estructura del plan de seguridad y compilar las secciones a partir de los deliverables 3B.7.2-3B.7.11. NO puede realizar threat modeling ni tomar decisiones de seguridad — esas requieren un Security Engineer. Necesita brief con: superficie de ataque, datos sensibles, compliance requirements, y decisiones de seguridad ya tomadas.

**Qué es:** Documento maestro de seguridad que consolida toda la estrategia: threat model, autenticación, autorización, protección de datos, encriptación, OWASP compliance, security headers, secrets management, input validation, security logging, e incident response. Es el documento que un auditor de seguridad revisaría.

**Para qué sirve:** Centraliza todas las consideraciones de seguridad en un solo lugar. Sin este documento, la seguridad se implementa ad-hoc: un developer agrega CORS, otro no; uno valida inputs, otro no; uno usa parameterized queries, otro concatena strings. El plan asegura que la seguridad es sistemática, no accidental.

**Inputs requeridos:**
- `3B.1.2` System Context Diagram — superficie de ataque
- `3B.1.6` Integration Points — puntos de exposición
- `3B.3.5` Data Dictionary — datos sensibles (PII, financieros)
- `3B.4.6` Authentication Spec — diseño de auth
- `3B.4.7` Authorization Spec — diseño de authz
- Requisitos de compliance (GDPR, CCPA, PCI-DSS, HIPAA si aplica)

**Dependencias (predecessors):**
- `3B.1.2` System Context Diagram *(obligatorio)* — superficie de ataque
- `3B.3.5` Data Dictionary *(obligatorio)* — datos sensibles identificados
- `3B.4.6` Authentication Spec *(obligatorio)*
- `3B.4.7` Authorization Spec *(obligatorio)*

**Habilita (successors):**
- `3B.7.2` a `3B.7.11` — secciones detalladas del plan
- `4.3.7` Middleware — security middleware
- `5.8.1` Security Testing — test plan de seguridad
- `6.3.1` Production Environment Setup — hardening de producción

**Audiencia:**
- **Security Engineer** — documento propio de referencia
- **Solution Architect** — validación de coherencia con la arquitectura
- **Tech Lead** — enforcement en code reviews
- **Compliance** — evidencia de controles de seguridad
- **Todo el equipo de desarrollo** — awareness de seguridad

**Secciones esperadas:**
1. Executive summary de seguridad
2. Threat model (actores maliciosos, vectores de ataque, assets a proteger)
3. Security architecture overview (defense in depth layers)
4. Autenticación (resumen — detalle en 3B.7.2)
5. Autorización (resumen — detalle en 3B.7.3)
6. Protección de datos (resumen — detalle en 3B.7.4)
7. Encriptación (resumen — detalle en 3B.7.5)
8. OWASP compliance (resumen — detalle en 3B.7.6)
9. Security headers (resumen — detalle en 3B.7.7)
10. Secrets management (resumen — detalle en 3B.7.8)
11. Input validation (resumen — detalle en 3B.7.9)
12. Security logging (resumen — detalle en 3B.7.10)
13. Incident response (resumen — detalle en 3B.7.11)
14. Compliance requirements y cómo se cumplen
15. Security testing strategy (pen testing, SAST, DAST)

**Criterio de completitud:**
- [ ] Threat model documentado
- [ ] Todas las áreas de seguridad cubiertas (auth, data, OWASP, etc.)
- [ ] Compliance requirements mapeados a controles
- [ ] Security testing strategy definida
- [ ] Revisado por Security Engineer
- [ ] Aprobado por Solution Architect

**Anti-patrones:**
- ❌ **"Security by obscurity":** Confiar en que "nadie va a descubrir nuestra API" — no es una estrategia de seguridad.
- ❌ **Security plan genérico:** Copiar un template de internet sin adaptarlo al proyecto — no cubre los riesgos específicos.
- ❌ **Sin threat model:** Plan de seguridad sin identificar amenazas — se protege contra amenazas imaginarias y se ignoran las reales.
- ❌ **Plan sin enforcement:** Documento de seguridad que nadie lee ni enforce en code reviews — teatro de seguridad.

**Template:** `phases/03B-design-technical/deliverables/security-plan.md` *(pendiente)*

---

### 3B.7.2 Authentication Design

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.7 Security Plan |
| **Responsable** | Security Engineer |
| **Ejecuta** | Security Engineer / Backend Developer |
| **Aprueba** | Solution Architect |
| **Formato** | Documento (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere conocimiento profundo de seguridad de autenticación: hash algorithms (bcrypt, Argon2), token security, session hijacking prevention, brute force protection.  
En VTT: un agente puede documentar el diseño de autenticación desde la perspectiva de seguridad. Es parcialmente delegable. Necesita brief con: auth method, password policy, token storage decisions, y MFA requirements.

**Qué es:** Diseño detallado de la seguridad de autenticación: password hashing algorithm, password policy (length, complexity, rotation), token security (signing algorithm, key rotation), session security (fixation prevention, concurrent sessions), brute force protection (account lockout, progressive delays), y MFA design.

**Para qué sirve:** Complementa la Authentication Spec (3B.4.6) con el ángulo de seguridad. La spec define el flujo; el Authentication Design define cómo hacerlo seguro. Sin esto, se usa MD5 para hashear passwords, tokens sin expiración, y sin protección contra brute force.

**Inputs requeridos:**
- `3B.4.6` Authentication Spec — flujo de auth
- Security best practices (OWASP Authentication Cheat Sheet)
- Compliance requirements

**Dependencias (predecessors):**
- `3B.4.6` Authentication Spec *(obligatorio)*
- `3B.7.1` Security Plan *(recomendado)* — contexto de seguridad general

**Habilita (successors):**
- `4.3.4` Authentication Implementation — implementación segura
- `5.8.1` Security Testing — test cases de auth security

**Audiencia:**
- **Backend Developer** — implementación segura de auth
- **Security Engineer** — validación
- **QA Engineer** — security test cases

**Secciones esperadas:**
1. Password hashing (algorithm: bcrypt/Argon2, cost factor, salt)
2. Password policy (min length, complexity, common password check, rotation)
3. Token security (signing algorithm RS256/HS256, key rotation schedule, claims validation)
4. Session security (fixation prevention, concurrent session policy, idle timeout)
5. Brute force protection (max attempts, lockout duration, progressive delays, CAPTCHA)
6. MFA design (TOTP, SMS, email — method, recovery codes)
7. Account recovery (password reset flow security, identity verification)
8. Credential storage (never plaintext, env variables, secrets manager)

**Criterio de completitud:**
- [ ] Password hashing algorithm definido (bcrypt o Argon2, nunca MD5/SHA)
- [ ] Password policy documentada
- [ ] Token signing algorithm y key rotation definidos
- [ ] Brute force protection diseñada
- [ ] Account lockout/recovery documentado
- [ ] MFA definido (si aplica)
- [ ] Validado contra OWASP Authentication Cheat Sheet

**Anti-patrones:**
- ❌ **MD5/SHA1 para passwords:** Algorithms rotos — usar bcrypt (cost 12+) o Argon2.
- ❌ **Sin rate limiting en login:** Permite brute force ilimitado.
- ❌ **Tokens sin expiración:** Acceso permanente si se compromete el token.
- ❌ **Password recovery vía security questions:** Fácilmente investigables en redes sociales.

**Template:** `phases/03B-design-technical/deliverables/authentication-design.md` *(pendiente)*

---

### 3B.7.3 Authorization Design

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.7 Security Plan |
| **Responsable** | Security Engineer |
| **Ejecuta** | Security Engineer / Backend Developer |
| **Aprueba** | Solution Architect |
| **Formato** | Documento (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Una vez + actualizaciones por nuevo rol/recurso |

**Perfil de ejecución:** Requiere entendimiento de modelos de autorización desde la perspectiva de seguridad: principle of least privilege, IDOR prevention, privilege escalation prevention.  
En VTT: un agente puede documentar el diseño de autorización con matrices de permisos y reglas de enforcement. Necesita brief con: modelo RBAC/ABAC, roles, permisos, y resources protegidos.

**Qué es:** Diseño detallado de la seguridad de autorización: modelo elegido (RBAC/ABAC), principle of least privilege, IDOR (Insecure Direct Object Reference) prevention, privilege escalation prevention, row-level security enforcement, y default deny policy. Complementa la Authorization Spec (3B.4.7) con controles de seguridad.

**Para qué sirve:** La Authorization Spec define qué roles pueden hacer qué. El Authorization Design define cómo prevenir que alguien haga lo que NO debe: acceder a datos de otro usuario (IDOR), escalar privilegios (user → admin), o bypasear controles (direct API call sin pasar por UI).

**Inputs requeridos:**
- `3B.4.7` Authorization Spec — modelo de permisos
- OWASP Access Control Cheat Sheet
- `3B.3.3` Table Specifications — resources a proteger

**Dependencias (predecessors):**
- `3B.4.7` Authorization Spec *(obligatorio)*
- `3B.7.1` Security Plan *(recomendado)*

**Habilita (successors):**
- `4.3.4` Authentication Implementation — guards/policies
- `5.8.1` Security Testing — authorization bypass tests

**Audiencia:**
- **Backend Developer** — implementación de controles
- **Security Engineer** — validación
- **QA Engineer** — test matrix de permisos

**Secciones esperadas:**
1. Principle of least privilege (default deny, explicit allow)
2. IDOR prevention (ownership validation en cada request)
3. Privilege escalation prevention (no self-promote, admin-only operations)
4. Row-level security enforcement (WHERE user_id = current_user)
5. API-level vs UI-level authorization (ambos necesarios)
6. Authorization caching (invalidation on role change)
7. Audit trail de authorization failures (logging de 403s)
8. Service-to-service authorization (si aplica)

**Criterio de completitud:**
- [ ] Principle of least privilege documentado y aplicado
- [ ] IDOR prevention strategy definida
- [ ] Privilege escalation scenarios identificados y mitigados
- [ ] Row-level security definida para multi-tenant resources
- [ ] Authorization logging configurado
- [ ] Default deny como regla base

**Anti-patrones:**
- ❌ **Authorization solo en frontend:** Ocultar botones en la UI pero no validar en el backend — bypass trivial con curl.
- ❌ **IDOR no prevenido:** `GET /users/123/orders` sin verificar que el user autenticado ES user 123.
- ❌ **Role check solo en controller:** Middleware de auth pero sin row-level security — acceso a datos de otros.
- ❌ **Self-promotion posible:** Endpoint `PUT /users/me` que permite cambiar el campo `role` a `admin`.

**Template:** `phases/03B-design-technical/deliverables/authorization-design.md` *(pendiente)*

---

### 3B.7.4 Data Protection Plan

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.7 Security Plan |
| **Responsable** | Security Engineer |
| **Ejecuta** | Security Engineer |
| **Aprueba** | Solution Architect |
| **Formato** | Documento (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere conocimiento de data protection regulations (GDPR, CCPA), clasificación de datos, y técnicas de protección (masking, anonymization, pseudonymization).  
En VTT: un agente puede generar el plan de protección de datos a partir del Data Dictionary y compliance requirements. Es bastante delegable. Necesita brief con: datos sensibles identificados, compliance requirements, y políticas de retención/eliminación.

**Qué es:** Plan que define cómo se protegen los datos en todas las etapas: clasificación de datos (public, internal, confidential, restricted), protección por clasificación, data minimization (no recolectar lo innecesario), retención y eliminación, right to be forgotten (GDPR), data masking en ambientes no-producción, y anonymization para analytics.

**Para qué sirve:** Compliance con GDPR/CCPA no es opcional — las multas son del 4% de revenue global. Más allá del compliance, la protección de datos previene data breaches que destruyen la confianza del usuario. El plan asegura que los datos se tratan con el nivel de protección que merecen.

**Inputs requeridos:**
- `3B.3.5` Data Dictionary — datos y su clasificación PII
- `3B.1.7` Data Flow Diagram — dónde fluyen datos sensibles
- Compliance requirements (GDPR, CCPA, PCI-DSS, HIPAA)
- Legal/DPO input sobre retención y derechos de usuario

**Dependencias (predecessors):**
- `3B.3.5` Data Dictionary *(obligatorio)* — campos PII identificados
- `3B.1.7` Data Flow Diagram *(obligatorio)* — flujo de datos sensibles

**Habilita (successors):**
- `3B.7.5` Encryption Strategy — encriptación de datos sensibles
- `4.3.2` Database Models — soft delete, anonymization
- `7.5.1` Data Retention Jobs — jobs de eliminación automática

**Audiencia:**
- **Security Engineer** — implementación de controles
- **Compliance / DPO** — evidencia de compliance
- **Backend Developer** — manejo correcto de datos sensibles
- **DevOps Lead** — masking en environments no-prod

**Secciones esperadas:**
1. Clasificación de datos (tabla: categoría, ejemplos, nivel de protección)
2. Data inventory (qué datos se recolectan, de quién, para qué)
3. Data minimization (qué datos NO recolectar)
4. Retención policy (cuánto tiempo se guardan por tipo de dato)
5. Eliminación / Right to be forgotten (proceso técnico)
6. Data masking en non-prod environments
7. Anonymization/pseudonymization para analytics
8. Cross-border data transfer (si aplica)
9. Third-party data sharing (con quién, qué datos, bajo qué acuerdos)
10. Breach notification plan (timeline, stakeholders)

**Criterio de completitud:**
- [ ] Todos los datos sensibles del Data Dictionary clasificados
- [ ] Retención policy definida por tipo de dato
- [ ] Right to be forgotten proceso técnico documentado
- [ ] Data masking para non-prod definido
- [ ] Compliance requirements mapeados a controles
- [ ] Breach notification plan incluido

**Anti-patrones:**
- ❌ **"No tenemos datos sensibles":** Todo sistema con usuarios tiene PII (email, nombre, IP) — la clasificación es necesaria.
- ❌ **Retención infinita:** Guardar datos forever "por si acaso" — violación de data minimization y storage innecesario.
- ❌ **Datos reales en staging:** BD de staging con copia de producción sin masking — data breach si staging es menos protegido.
- ❌ **Sin proceso de eliminación:** El usuario pide borrar su cuenta y el developer no sabe qué tablas limpiar.

**Template:** `phases/03B-design-technical/deliverables/data-protection-plan.md` *(pendiente)*

---

### 3B.7.5 Encryption Strategy

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.7 Security Plan |
| **Responsable** | Security Engineer |
| **Ejecuta** | Security Engineer / Backend Developer |
| **Aprueba** | Solution Architect |
| **Formato** | Documento (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5-1 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere conocimiento de criptografía aplicada: TLS, encryption at rest, encryption in transit, key management, y algorithms seguros.  
En VTT: un agente puede documentar la estrategia de encriptación basándose en best practices del stack y la clasificación de datos. Es bastante delegable. Necesita brief con: datos que requieren encriptación, plataforma de hosting (AWS KMS, GCP KMS), y TLS requirements.

**Qué es:** Definición de cómo se encriptan los datos en tránsito (TLS) y en reposo (AES-256): qué datos se encriptan, con qué algoritmos, cómo se gestionan las keys, y qué herramientas se usan (AWS KMS, HashiCorp Vault). Incluye TLS configuration, database encryption, file storage encryption, y field-level encryption para datos ultra-sensibles.

**Para qué sirve:** La encriptación es la última línea de defensa. Si un atacante obtiene acceso a la BD o intercepta tráfico, la encriptación asegura que los datos son ilegibles sin la key. TLS protege en tránsito; encryption at rest protege el almacenamiento.

**Inputs requeridos:**
- `3B.7.4` Data Protection Plan — datos que requieren encriptación
- `3B.1.5` Technology Stack — herramientas de encriptación disponibles
- `3B.8.1` Infrastructure Plan — plataforma cloud y servicios de KMS

**Dependencias (predecessors):**
- `3B.7.4` Data Protection Plan *(obligatorio)* — qué encriptar
- `3B.1.5` Technology Stack *(obligatorio)* — herramientas

**Habilita (successors):**
- `4.2.1` Database Setup — encryption at rest configurado
- `6.3.1` Production Environment Setup — TLS configurado

**Audiencia:**
- **DevOps Lead** — configuración de TLS y encryption at rest
- **Backend Developer** — field-level encryption
- **Security Engineer** — validación

**Secciones esperadas:**
1. Encryption in transit (TLS 1.3, certificate management, HSTS)
2. Encryption at rest (database: AES-256, storage: SSE-S3/SSE-KMS)
3. Field-level encryption (campos ultra-sensibles: SSN, credit card)
4. Key management (KMS, rotation schedule, access control)
5. Algorithms (tabla: propósito, algorithm, key size)
6. Certificate management (provider, renewal, monitoring expiry)
7. Backup encryption (backups encriptados)

**Criterio de completitud:**
- [ ] TLS 1.3 requerido para todo el tráfico
- [ ] Encryption at rest configurado para BD y file storage
- [ ] Key management strategy definida (KMS, rotation)
- [ ] Algorithms especificados y justificados
- [ ] Certificate management definido
- [ ] Backups encriptados

**Anti-patrones:**
- ❌ **HTTP en producción:** Sin TLS — datos en texto plano en la red.
- ❌ **Keys hardcoded:** Encryption keys en el código fuente — si el repo se filtra, la encriptación es inútil.
- ❌ **Sin key rotation:** Misma key por años — si se compromete, todo el historial es vulnerable.
- ❌ **Custom crypto:** Implementar algoritmos de encriptación propios — usar siempre libraries estándar probadas.

**Template:** `phases/03B-design-technical/deliverables/encryption-strategy.md` *(pendiente)*

---

### 3B.7.6 OWASP Checklist

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.7 Security Plan |
| **Responsable** | Security Engineer |
| **Ejecuta** | Security Engineer |
| **Aprueba** | Solution Architect |
| **Formato** | Checklist (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez + revisión por release |

**Perfil de ejecución:** Requiere conocimiento del OWASP Top 10 y cómo cada vulnerabilidad aplica al stack y arquitectura específicos del proyecto.  
En VTT: un agente puede generar el checklist OWASP contextualizado al proyecto con controles específicos por vulnerabilidad y cómo implementarlos en el stack elegido. Es altamente delegable. Necesita brief con: OWASP Top 10 actual, stack tecnológico, y controles ya planificados.

**Qué es:** Checklist que mapea cada vulnerabilidad del OWASP Top 10 a los controles implementados en el proyecto. Para cada vulnerabilidad: qué es, cómo aplica al proyecto, qué controles se implementan, quién es responsable de la implementación, y cómo se verifica.

**Para qué sirve:** OWASP Top 10 es el estándar de facto para seguridad de aplicaciones web. El checklist asegura que el equipo ha considerado cada vulnerabilidad y tiene controles planificados. Es también evidencia de due diligence para auditorías y compliance.

**Inputs requeridos:**
- OWASP Top 10 (versión vigente)
- `3B.1.5` Technology Stack — controles específicos por stack
- `3B.7.1` Security Plan — controles ya planificados

**Dependencias (predecessors):**
- `3B.7.1` Security Plan *(obligatorio)* — contexto de seguridad
- `3B.1.5` Technology Stack *(obligatorio)*

**Habilita (successors):**
- `5.8.1` Security Testing — test cases por vulnerabilidad OWASP
- Code reviews — checklist de seguridad

**Audiencia:**
- **Security Engineer** — verificación de cobertura
- **Backend Developer** — awareness de vulnerabilidades
- **QA Engineer** — security test cases
- **Auditors** — evidencia de compliance

**Secciones esperadas:**
1. Por cada OWASP Top 10 vulnerability:
   - Nombre y descripción
   - Cómo aplica al proyecto
   - Controles implementados
   - Responsable de implementación
   - Cómo se verifica (test, scan, code review)
   - Status (planned, implemented, verified)
2. Tabla resumen (vulnerability, control, status)
3. Fecha de última revisión

**Criterio de completitud:**
- [ ] Las 10 vulnerabilidades OWASP cubiertas
- [ ] Control específico para cada una (no genérico)
- [ ] Controles contextualizados al stack del proyecto
- [ ] Responsable asignado por control
- [ ] Método de verificación definido

**Anti-patrones:**
- ❌ **Checklist genérico sin contextualizar:** Copiar el OWASP Top 10 sin mapear al proyecto — no es accionable.
- ❌ **"No aplica" para todo:** Descartar vulnerabilidades sin análisis — probablemente aplican.
- ❌ **Checklist sin follow-up:** Llenarlo una vez y no volver a verificar — las vulnerabilidades cambian con el código.

**Template:** `phases/03B-design-technical/deliverables/owasp-checklist.md` *(pendiente)*

---

### 3B.7.7 Security Headers

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.7 Security Plan |
| **Responsable** | Security Engineer |
| **Ejecuta** | Backend Developer / DevOps Lead |
| **Aprueba** | Security Engineer |
| **Formato** | Lista (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere conocimiento de HTTP security headers y cómo configurarlos en el web server/framework.  
En VTT: un agente puede generar la lista completa de security headers con valores recomendados para el stack del proyecto. Es altamente delegable. Necesita brief con: framework backend, CDN/proxy, y CSP requirements.

**Qué es:** Lista de HTTP security headers que la aplicación debe incluir en todas las responses: Content-Security-Policy, Strict-Transport-Security, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy, etc. Para cada header: valor recomendado, justificación, y dónde configurarlo.

**Para qué sirve:** Los security headers son controles de seguridad "gratis" — se configuran una vez y previenen categorías enteras de ataques: XSS (CSP), clickjacking (X-Frame-Options), MIME sniffing (X-Content-Type-Options), protocol downgrade (HSTS). No tenerlos es negligencia.

**Inputs requeridos:**
- `3B.1.5` Technology Stack — framework y web server
- Requisitos de CSP (Content-Security-Policy) basados en recursos externos

**Dependencias (predecessors):**
- `3B.1.5` Technology Stack *(obligatorio)*
- `3B.7.1` Security Plan *(recomendado)*

**Habilita (successors):**
- `4.3.7` Middleware — headers configurados en middleware
- `5.8.1` Security Testing — verificación de headers

**Audiencia:**
- **Backend Developer** — configuración de headers
- **DevOps Lead** — configuración en CDN/reverse proxy
- **Security Engineer** — validación

**Secciones esperadas:**
1. Tabla de headers (header, valor, justificación)
2. Content-Security-Policy (CSP) detallado (directives)
3. Strict-Transport-Security (HSTS) con preload consideration
4. X-Content-Type-Options: nosniff
5. X-Frame-Options o frame-ancestors en CSP
6. Referrer-Policy
7. Permissions-Policy (camera, microphone, geolocation)
8. Dónde configurar (middleware, nginx, CDN)
9. Verificación (securityheaders.com, Mozilla Observatory)

**Criterio de completitud:**
- [ ] Todos los security headers principales incluidos
- [ ] CSP definida con directives específicas
- [ ] HSTS con max-age adecuado
- [ ] Dónde configurar documentado
- [ ] Verificable con herramienta online

**Anti-patrones:**
- ❌ **Sin CSP:** No tener Content-Security-Policy — XSS sin mitigación.
- ❌ **CSP demasiado permisiva:** `default-src *` — permite todo, inútil.
- ❌ **Sin HSTS:** Permite downgrade a HTTP — man-in-the-middle posible.
- ❌ **Headers solo en el backend:** CDN o reverse proxy no los propaga — headers nunca llegan al browser.

**Template:** `phases/03B-design-technical/deliverables/security-headers.md` *(pendiente)*

---

### 3B.7.8 Secrets Management

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.7 Security Plan |
| **Responsable** | Security Engineer |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Security Engineer |
| **Formato** | Documento (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5-1 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere experiencia con herramientas de secrets management (AWS Secrets Manager, HashiCorp Vault, Doppler) y secure deployment practices.  
En VTT: un agente puede documentar la estrategia de secrets management con inventario de secrets, herramienta elegida, y proceso de rotation. Es bastante delegable. Necesita brief con: herramienta elegida, lista de secrets (API keys, DB passwords, JWT signing keys), y policy de rotation.

**Qué es:** Documento que define cómo se gestionan los secretos (API keys, database passwords, JWT signing keys, encryption keys, third-party credentials): dónde se almacenan, cómo se acceden, cómo se rotan, quién tiene acceso, y cómo se previene que aparezcan en código o logs.

**Para qué sirve:** Un API key commiteado en GitHub es un data breach esperando a pasar. La gestión de secretos asegura que las credenciales nunca están en código, logs, ni ambientes no autorizados. También asegura que si una key se compromete, el proceso de rotación es rápido y documentado.

**Inputs requeridos:**
- `3B.1.6` Integration Points — credentials de cada integración
- `3B.1.5` Technology Stack — cloud provider y herramientas
- `3B.8.5` Environment Matrix — secrets por ambiente

**Dependencias (predecessors):**
- `3B.1.5` Technology Stack *(obligatorio)* — herramientas disponibles
- `3B.1.6` Integration Points *(obligatorio)* — inventario de credentials

**Habilita (successors):**
- `4.1.3` Project Scaffolding — .env setup y .gitignore
- `4.1.4` CI/CD Pipeline — secrets injection en pipeline
- `6.3.1` Production Environment Setup — secrets configurados

**Audiencia:**
- **DevOps Lead** — implementación
- **Backend Developer** — cómo acceder a secrets en código
- **Security Engineer** — validación
- **Tech Lead** — enforcement

**Secciones esperadas:**
1. Inventario de secrets (tabla: nombre, tipo, rotación, ambiente)
2. Herramienta de secrets management (AWS SM, Vault, Doppler)
3. Acceso a secrets en código (.env local, injected en CI/CD, SDK del vault)
4. Rotation policy (frecuencia por tipo de secret)
5. Access control (quién puede leer/escribir cada secret)
6. Prevention (pre-commit hooks para detectar secrets, .gitignore)
7. Incident response (qué hacer si un secret se filtra)
8. Secrets en CI/CD (cómo se inyectan en el pipeline)
9. Secrets per environment (dev, staging, prod — diferentes values)

**Criterio de completitud:**
- [ ] Todos los secrets inventariados
- [ ] Herramienta elegida y configurada
- [ ] Rotation policy definida
- [ ] Pre-commit hooks para detección de secrets configurados
- [ ] .gitignore incluye archivos de secrets
- [ ] Proceso de incident response para secret leaks definido

**Anti-patrones:**
- ❌ **Secrets en código:** API keys hardcoded en el source code — breach cuando el repo se filtra.
- ❌ **Secrets en .env commiteado:** `.env` con secrets en el repo — equivalente a hardcoded.
- ❌ **Mismos secrets en todos los ambientes:** La API key de prod igual a dev — si se filtra dev, prod comprometido.
- ❌ **Sin rotation:** Misma DB password por 3 años — si fue comprometida alguna vez, acceso permanente.
- ❌ **Secrets en logs:** Loggear requests con Authorization header — secrets en plain text en logs.

**Template:** `phases/03B-design-technical/deliverables/secrets-management.md` *(pendiente)*

---

### 3B.7.9 Input Validation Rules

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.7 Security Plan |
| **Responsable** | Security Engineer |
| **Ejecuta** | Backend Developer |
| **Aprueba** | Security Engineer |
| **Formato** | Documento (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez + adiciones por endpoint |

**Perfil de ejecución:** Requiere conocimiento de ataques basados en input (SQL injection, XSS, command injection, path traversal) y técnicas de validación y sanitización.  
En VTT: un agente puede generar las reglas de input validation a partir del OpenAPI spec y la lista de endpoints. Puede producir schemas de validación (Zod, Joi, class-validator). Es altamente delegable. Necesita brief con: endpoints list, request schemas, y validation library elegida.

**Qué es:** Documento que define las reglas de validación de inputs para cada endpoint y tipo de dato: qué se valida (type, format, length, range, pattern), cómo se valida (library: Zod, Joi, class-validator), dónde se valida (middleware, controller, service), y cómo se sanitiza (escape HTML, parameterized queries, strip dangerous chars).

**Para qué sirve:** Input validation es la primera línea de defensa contra inyección. SQL injection, XSS, y command injection se previenen validando y sanitizando inputs. "Never trust user input" es el principio — este documento lo operacionaliza con reglas concretas por campo.

**Inputs requeridos:**
- `3B.4.1` OpenAPI Spec — schemas de request
- `2.5.3` Validation Rules — reglas de negocio de validación
- `3B.4.5` Error Codes — error responses de validación

**Dependencias (predecessors):**
- `3B.4.1` OpenAPI Spec *(obligatorio)* — schemas a validar
- `2.5.3` Validation Rules *(obligatorio)* — reglas de negocio

**Habilita (successors):**
- `4.3.7` Middleware — validation middleware
- `4.3.3` API Routes — validation en cada route
- `5.3.1` API Tests — test cases de validation

**Audiencia:**
- **Backend Developer** — implementación de validaciones
- **Frontend Developer** — validaciones client-side alineadas
- **QA Engineer** — fuzzing y boundary testing

**Secciones esperadas:**
1. Principios (validate → sanitize → process, whitelist over blacklist)
2. Validation library elegida (Zod, Joi, class-validator)
3. Dónde se valida (middleware para formato, service para negocio)
4. Reglas por tipo de dato (string: maxLength, pattern; number: min, max; email: format; URL: protocol whitelist)
5. Sanitización (escape HTML entities, strip tags, parameterized queries)
6. File upload validation (type, size, malware scan)
7. Request size limits (max body size, max header size)
8. SQL injection prevention (parameterized queries always)
9. XSS prevention (output encoding, CSP)
10. Path traversal prevention (whitelist allowed paths)

**Criterio de completitud:**
- [ ] Validation library elegida y documentada
- [ ] Reglas por tipo de dato definidas
- [ ] Sanitización strategy definida
- [ ] SQL injection prevention: parameterized queries mandatorio
- [ ] XSS prevention: output encoding mandatorio
- [ ] File upload limits definidos
- [ ] Request size limits definidos

**Anti-patrones:**
- ❌ **Validación solo en frontend:** Client-side validation es UX, no seguridad — se bypasea con curl.
- ❌ **Blacklist en vez de whitelist:** Intentar bloquear caracteres peligrosos en vez de permitir solo los válidos.
- ❌ **String concatenation en queries:** `"SELECT * FROM users WHERE id = " + userId` — SQL injection 101.
- ❌ **Sin sanitización de output:** Datos del usuario renderizados sin escape — XSS stored.
- ❌ **Sin límite de file upload:** Permitir uploads de 1GB — DoS por storage.

**Template:** `phases/03B-design-technical/deliverables/input-validation-rules.md` *(pendiente)*

---

### 3B.7.10 Security Logging

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.7 Security Plan |
| **Responsable** | Security Engineer |
| **Ejecuta** | Backend Developer / DevOps Lead |
| **Aprueba** | Security Engineer |
| **Formato** | Documento (MD) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5-1 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere conocimiento de security monitoring: qué eventos loggear para detección de ataques, formato de logs de seguridad, y herramientas de SIEM.  
En VTT: un agente puede generar la estrategia de security logging con lista de eventos a loggear, formato, y alerting rules. Es bastante delegable. Necesita brief con: herramienta de logging, eventos de seguridad a monitorear, y thresholds de alerting.

**Qué es:** Definición de qué eventos de seguridad se loggean, en qué formato, y cómo se monitorean: login attempts (success/fail), authorization failures (403s), password changes, privilege escalations, suspicious patterns (rate limit hits, unusual access patterns), y data access logs (quién accedió a datos sensibles).

**Para qué sirve:** Sin security logging, un ataque en progreso es invisible. Los logs de seguridad permiten: detectar ataques en tiempo real (brute force, account takeover), investigar post-incident (¿qué datos se accedieron?), y cumplir compliance (audit trail). Son la "cámara de seguridad" del sistema.

**Inputs requeridos:**
- `3B.7.1` Security Plan — eventos de seguridad críticos
- `3B.8.11` Monitoring Strategy — herramienta de logging
- `3B.7.11` Incident Response Plan — qué logs se necesitan post-incident

**Dependencias (predecessors):**
- `3B.7.1` Security Plan *(obligatorio)*
- `3B.8.11` Monitoring Strategy *(recomendado)* — herramienta y formato

**Habilita (successors):**
- `4.3.7` Middleware — logging middleware
- `7.1.1` Monitoring Setup — dashboards de security events
- Incident investigation — logs como evidencia

**Audiencia:**
- **Security Engineer** — monitoring y alerting
- **DevOps Lead** — configuración de logging
- **Backend Developer** — implementación de log events

**Secciones esperadas:**
1. Eventos a loggear (tabla: evento, severity, datos a incluir, datos a EXCLUIR)
2. Authentication events (login success/fail, logout, token refresh, password change)
3. Authorization events (403 forbidden, privilege escalation attempt)
4. Data access events (PII access, bulk data export, admin operations)
5. Suspicious patterns (rate limit hit, multiple failed logins, unusual IP)
6. Log format (structured JSON, fields estándar: timestamp, event, userId, ip, userAgent)
7. Datos a NUNCA loggear (passwords, tokens, PII sin masking)
8. Retención de security logs (más larga que application logs)
9. Alerting rules (thresholds que disparan alertas)
10. SIEM integration (si aplica)

**Criterio de completitud:**
- [ ] Eventos de autenticación loggeados (success y failure)
- [ ] Eventos de autorización loggeados (403s)
- [ ] Datos sensibles EXCLUIDOS de logs (passwords, tokens)
- [ ] Formato structured JSON definido
- [ ] Alerting rules para eventos críticos
- [ ] Retención de logs definida

**Anti-patrones:**
- ❌ **Loggear passwords:** `log.info("Login attempt", { email, password })` — passwords en plain text en logs.
- ❌ **No loggear auth failures:** Login failures no loggeados — brute force invisible.
- ❌ **Logs sin estructura:** `console.log("Something happened")` — imposible de parsear y alertar.
- ❌ **Sin alerting:** Logs que nadie revisa — detectar un ataque 3 meses después no es detección.
- ❌ **Retención de 7 días:** Security logs borrados en una semana — si el ataque se detecta después, la evidencia ya no existe.

**Template:** `phases/03B-design-technical/deliverables/security-logging.md` *(pendiente)*

---

### 3B.7.11 Incident Response Plan

| Campo | Valor |
|-------|-------|
| **Fase** | 3B-Design Technical |
| **Subfase** | 3B.7 Security Plan |
| **Responsable** | Security Engineer |
| **Ejecuta** | Security Engineer / DevOps Lead |
| **Aprueba** | Solution Architect |
| **Formato** | Documento (MD/PDF) |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1 día |
| **Frecuencia** | Una vez + simulacros periódicos |

**Perfil de ejecución:** Requiere experiencia en incident management: clasificación de incidentes, escalation, communication, containment, eradication, y recovery.  
En VTT: un agente puede generar el plan de incident response basándose en frameworks estándar (NIST, SANS). Es bastante delegable. Necesita brief con: equipo de respuesta, canales de comunicación, herramientas, y clasificación de severidad del proyecto.

**Qué es:** Plan que define qué hacer cuando ocurre un incidente de seguridad: quién responde, cómo se clasifica la severidad, qué pasos seguir (identificación → contención → erradicación → recovery → lessons learned), cómo se comunica (interno, a usuarios, a reguladores), y timelines de respuesta.

**Para qué sirve:** Cuando hay un data breach a las 3AM no es momento de improvisar. El IRP asegura que el equipo sabe exactamente qué hacer, a quién llamar, y en qué orden. Reduce el tiempo de respuesta, minimiza el daño, y cumple con obligaciones legales de notificación (GDPR: 72 horas).

**Inputs requeridos:**
- `3B.7.1` Security Plan — contexto de seguridad
- `3B.7.10` Security Logging — logs como herramienta de investigación
- Contact list del equipo de respuesta
- Obligaciones legales de notificación

**Dependencias (predecessors):**
- `3B.7.1` Security Plan *(obligatorio)*
- `3B.7.10` Security Logging *(recomendado)*

**Habilita (successors):**
- `7.3.1` Incident Management — operación de incidents en producción
- Simulacros de seguridad — basados en el plan

**Audiencia:**
- **Security Engineer** — líder de respuesta
- **DevOps Lead** — contención técnica
- **Tech Lead** — coordinación del equipo
- **Management** — communication y escalation
- **Legal / DPO** — notificación regulatoria

**Secciones esperadas:**
1. Equipo de respuesta (roles, contactos, disponibilidad)
2. Clasificación de severidad (critical, high, medium, low con ejemplos)
3. Proceso de respuesta (Identification → Containment → Eradication → Recovery → Lessons Learned)
4. Containment procedures por tipo (data breach, DDoS, account compromise, malware)
5. Communication plan (interno, usuarios, reguladores, media)
6. Timelines de notificación (GDPR: 72h, interno: 1h, usuarios: depende)
7. Escalation matrix (quién se notifica según severidad)
8. Post-mortem template (blameless, timeline, root cause, actions)
9. Simulacros (frecuencia, scenarios, evaluación)
10. Herramientas de respuesta (war room, communication channel, runbooks)

**Criterio de completitud:**
- [ ] Equipo de respuesta definido con contactos
- [ ] Clasificación de severidad con criterios claros
- [ ] Proceso de respuesta step-by-step
- [ ] Communication plan por audiencia
- [ ] Timelines de notificación alineados a compliance
- [ ] Post-mortem template incluido
- [ ] Simulacros programados (al menos anual)

**Anti-patrones:**
- ❌ **Sin plan:** Improvisar durante un breach — caos, decisiones emocionales, comunicación inconsistente.
- ❌ **Plan que nadie conoce:** Plan guardado en un PDF que nadie sabe dónde está — inútil en crisis.
- ❌ **Sin simulacros:** Plan nunca probado — la primera vez que se usa es en una crisis real.
- ❌ **Blame-focused post-mortem:** Buscar culpables en vez de causas raíz — la próxima vez nadie reporta.
- ❌ **Sin communication plan:** El equipo técnico contiene el breach pero nadie notifica a usuarios ni reguladores — violación legal.

**Template:** `phases/03B-design-technical/deliverables/incident-response-plan.md` *(pendiente)*

---

## Tabla resumen de ejecutores — Fase 3B.7 Security Plan

| Deliverable | Responsable | Ejecuta | Delegable VTT |
|-------------|-------------|---------|---------------|
| 3B.7.1 Security Plan | Security Engineer | Security Engineer | 🔶 Parcial — puede compilar el plan, no puede hacer threat modeling |
| 3B.7.2 Authentication Design | Security Engineer | Security Engineer / Backend Dev | 🔶 Parcial — puede documentar, decisiones de seguridad requieren expertise |
| 3B.7.3 Authorization Design | Security Engineer | Security Engineer / Backend Dev | 🔶 Parcial — puede documentar matrices, diseño de seguridad requiere expertise |
| 3B.7.4 Data Protection Plan | Security Engineer | Security Engineer | ✅ — puede generar plan desde Data Dictionary y compliance requirements |
| 3B.7.5 Encryption Strategy | Security Engineer | Security Engineer / Backend Dev | ✅ — puede documentar estrategia basada en best practices del stack |
| 3B.7.6 OWASP Checklist | Security Engineer | Security Engineer | ✅ — puede generar checklist contextualizado al stack |
| 3B.7.7 Security Headers | Security Engineer | Backend Dev / DevOps Lead | ✅ — puede generar lista completa de headers con valores |
| 3B.7.8 Secrets Management | Security Engineer | DevOps Lead | ✅ — puede documentar estrategia con inventario y rotation policy |
| 3B.7.9 Input Validation Rules | Security Engineer | Backend Developer | ✅ — puede generar reglas y schemas de validación |
| 3B.7.10 Security Logging | Security Engineer | Backend Dev / DevOps Lead | ✅ — puede generar estrategia con eventos y alerting rules |
| 3B.7.11 Incident Response Plan | Security Engineer | Security Engineer / DevOps Lead | ✅ — puede generar plan basado en frameworks NIST/SANS |

---

## Siguiente archivo

**Próximo:** `DICCIONARIO_FASE_03B_08_INFRASTRUCTURE_PLAN.md` — 11 deliverables (3B.8.1 a 3B.8.11)
