# ESTRATEGIA DE GENERACIÓN DE TEMPLATES — DICCIONARIO DE DELIVERABLES SDLC

**Versión:** 1.0  
**Fecha:** 2026-05-14  
**Propósito:** Guía completa para generar los 438 templates de deliverables del SDLC usando un agente VTT  
**Autor:** PM  
**Estado:** Listo para ejecución

---

## 1. OBJETIVO

Generar un template estandarizado por cada deliverable del diccionario SDLC (438 total). Cada template será usado por un agente VTT para producir el deliverable real de un proyecto específico, garantizando consistencia de formato, completitud de contenido, y calidad homogénea.

---

## 2. CLASIFICACIÓN DE DELIVERABLES POR TIPO DE TEMPLATE

No todos los 438 deliverables necesitan el mismo tipo de template. Se clasifican en 7 tipos:

### Tipo A — Documento de Análisis/Diseño (~150 deliverables)

**Descripción:** Documentos que describen, analizan, o diseñan algo: planes, estrategias, specs, reports de research, personas, architecture docs.  
**Ejemplos:** Test Plan, Security Plan, User Research Plan, Architecture Document, Personas Document.  
**Formato del template:** Markdown con secciones, instrucciones por sección, y ejemplo de output.  
**Fases:** 0, 1, 2, 3A, 3B, 5 (parcial), 7 (parcial).

### Tipo B — Reporte de Resultados (~60 deliverables)

**Descripción:** Documentos que reportan resultados de una actividad: test results, performance reports, audit results, deploy logs.  
**Ejemplos:** Functional Test Results, Performance Report, Post-Deploy Report, Uptime Report.  
**Formato del template:** Markdown con tablas de datos, métricas, gráficos placeholder, y assessment.  
**Fases:** 5, 6, 7.

### Tipo C — Checklist / Sign-off (~25 deliverables)

**Descripción:** Documentos de verificación con items ✅/❌ y aprobación formal.  
**Ejemplos:** Smoke Test Sign-off, UAT Sign-off, Security Sign-off, Critical Paths Verified.  
**Formato del template:** Markdown con tabla de checklist, sección de decisión, y campo de firma.  
**Fases:** 5, 6.

### Tipo D — Código / Configuración (~120 deliverables)

**Descripción:** Archivos de código o configuración que el agente puede generar como starter.  
**Ejemplos:** docker-compose.yml, .eslintrc, CI pipeline YAML, Makefile, seed scripts.  
**Formato del template:** Archivo del tipo correspondiente (.yml, .json, .ts, .sh) con comentarios explicativos.  
**Fases:** 4, 6.

### Tipo E — Proceso / Guía (~25 deliverables)

**Descripción:** Documentos que definen un proceso step-by-step o una guía operativa.  
**Ejemplos:** Hotfix Process, Support Process, Contributing Guide, Migration Guide, Rollback Runbook.  
**Formato del template:** Markdown con pasos numerados, decisiones, y diagrams de flujo.  
**Fases:** 4, 6, 7.

### Tipo F — Lista / Backlog (~18 deliverables)

**Descripción:** Listas trackeadas de items con clasificación, priorización, y aging.  
**Ejemplos:** Bug Tracking, Improvement Backlog, Technical Debt Log, Defects Found.  
**Formato del template:** Markdown con tabla estructurada, campos por item, y reglas de clasificación.  
**Fases:** 4, 5, 7.

### Tipo G — Auto-generado / No necesita template (~40 deliverables)

**Descripción:** Artefactos que se generan automáticamente por herramientas o que son simplemente valores (URLs, métricas, logs automáticos).  
**Ejemplos:** Production URL, Staging URL, SSL Active, Coverage ≥80%, Test Coverage Report (auto), Deployment Log (auto).  
**Formato del template:** N/A — se documenta solo la verificación (checklist de que existe y cumple criterios).  
**Acción:** Generar solo un mini-checklist de verificación, no un template completo.

---

## 3. ESTRUCTURA DEL TEMPLATE (META-TEMPLATE)

Cada template sigue esta estructura estándar. El agente VTT recibe este template y lo llena con datos del proyecto.

```markdown
# {{DELIVERABLE_ID}} — {{DELIVERABLE_NAME}}

## Metadata

| Campo | Valor |
|-------|-------|
| **Proyecto** | {{PROJECT_NAME}} |
| **Fase** | {{PHASE}} |
| **Subfase** | {{SUBPHASE}} |
| **Versión** | 1.0 |
| **Fecha** | {{DATE}} |
| **Autor** | {{AUTHOR}} |
| **Revisor** | {{REVIEWER}} |
| **Aprobador** | {{APPROVER}} |
| **Estado** | Borrador / En revisión / Aprobado |

## Control de versiones

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | {{DATE}} | {{AUTHOR}} | Versión inicial |

---

## 1. {{SECTION_1_TITLE}}

<!-- INSTRUCCIÓN PARA EL AGENTE:
{{SECTION_1_INSTRUCTION}}
-->

{{SECTION_1_CONTENT}}

## 2. {{SECTION_2_TITLE}}

<!-- INSTRUCCIÓN PARA EL AGENTE:
{{SECTION_2_INSTRUCTION}}
-->

{{SECTION_2_CONTENT}}

[... N secciones según "Secciones esperadas" del diccionario ...]

---

## Aprobación

| Rol | Nombre | Fecha | Firma |
|-----|--------|-------|-------|
| {{ROLE_AUTHOR}} | | | |
| {{ROLE_APPROVER}} | | | |

---

## Referencias

- Deliverables de input: {{INPUT_DELIVERABLES}}
- Deliverables que habilita: {{OUTPUT_DELIVERABLES}}
```

---

## 4. VARIABLES DEL SISTEMA

Estas variables se inyectan en cada template. El agente las recibe como contexto.

### Variables globales (iguales para todo el proyecto)

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `{{PROJECT_NAME}}` | Nombre del proyecto | "HO Registrar" |
| `{{PROJECT_CODE}}` | Código del proyecto | "HO-REG" |
| `{{COMPANY_NAME}}` | Nombre de la empresa | "HO Corp" |
| `{{DATE}}` | Fecha de generación | "2026-05-14" |
| `{{SDLC_VERSION}}` | Versión del SDLC | "3.1" |

### Variables por deliverable (extraídas del diccionario)

| Variable | Fuente en el diccionario |
|----------|------------------------|
| `{{DELIVERABLE_ID}}` | Número del deliverable (e.g., "5.1.1") |
| `{{DELIVERABLE_NAME}}` | Nombre (e.g., "Test Plan") |
| `{{PHASE}}` | Fase (e.g., "5-Testing") |
| `{{SUBPHASE}}` | Subfase (e.g., "5.1 Test Planning") |
| `{{AUTHOR}}` | Campo "Ejecuta" de la tabla de metadatos |
| `{{REVIEWER}}` | Campo "Responsable" de la tabla de metadatos |
| `{{APPROVER}}` | Campo "Aprueba" de la tabla de metadatos |
| `{{SECTION_N_TITLE}}` | Ítem N de "Secciones esperadas" |
| `{{SECTION_N_INSTRUCTION}}` | Derivada de "Qué es" + "Para qué sirve" + "Criterio de completitud" |
| `{{INPUT_DELIVERABLES}}` | Campo "Inputs requeridos" |
| `{{OUTPUT_DELIVERABLES}}` | Campo "Habilita (successors)" |

### Variables de contexto del proyecto (el agente las necesita para llenar)

| Variable | Descripción | Quién la provee |
|----------|-------------|-----------------|
| `{{TECH_STACK}}` | Stack tecnológico del proyecto | Architect / Tech Lead |
| `{{USE_CASES}}` | Lista de use cases del proyecto | Business Analyst |
| `{{PERSONAS}}` | Personas definidas | UX Designer |
| `{{BUSINESS_RULES}}` | Reglas de negocio | Business Analyst |
| `{{NFRS}}` | Requerimientos no-funcionales | Architect |
| `{{DOMAIN_CONTEXT}}` | Contexto del dominio de negocio | Product Owner |

---

## 5. PROMPT PARA EL AGENTE GENERADOR DE TEMPLATES

Este es el prompt que se usa para generar cada template. Se ejecuta una vez por deliverable.

```
CONTEXTO:
Eres un agente especializado en generar templates estandarizados para 
deliverables de un SDLC de 8 fases. Cada template será usado posteriormente 
por otro agente VTT para producir el deliverable real de un proyecto específico.

ENTRADA:
Te voy a dar la entrada del DICCIONARIO DE DELIVERABLES para un deliverable 
específico. La entrada contiene:
- Tabla de metadatos (9 campos)
- Perfil de ejecución (incluyendo delegabilidad VTT)
- Qué es (descripción del deliverable)
- Para qué sirve (propósito y valor)
- Inputs requeridos (deliverables previos necesarios)
- Dependencias (predecessors)
- Habilita (successors)
- Audiencia (quién lo consume)
- Secciones esperadas (estructura del documento)
- Criterio de completitud (checklist de done)
- Anti-patrones (errores a evitar)

TAREA:
Genera el TEMPLATE MARKDOWN completo para este deliverable siguiendo 
estas reglas:

1. ESTRUCTURA:
   - Header con metadata del proyecto (campos como variables {{VARIABLE}})
   - Control de versiones (tabla)
   - Una sección H2 por cada ítem de "Secciones esperadas"
   - Sección de Aprobación al final
   - Sección de Referencias al final

2. POR CADA SECCIÓN:
   - Título H2 con el nombre de la sección
   - Bloque de instrucción para el agente (en comentario HTML) que explique:
     a. Qué debe contener esta sección
     b. Qué formato usar (prosa, tabla, lista, diagrama)
     c. Qué nivel de detalle se espera
     d. Qué inputs necesita para llenarla
     e. Qué errores evitar (derivados de Anti-patrones)
   - Placeholder de contenido que muestre la estructura esperada:
     - Si es tabla: tabla con headers y 1-2 filas de ejemplo con {{VARIABLES}}
     - Si es lista: 3-5 bullets de ejemplo con {{VARIABLES}}
     - Si es prosa: 1 párrafo de ejemplo con {{VARIABLES}}
     - Si es diagrama: indicación de qué tipo de diagrama y qué elementos

3. INSTRUCCIONES PARA EL AGENTE:
   - Las instrucciones van en comentarios HTML <!-- -->
   - Deben ser específicas y accionables (no "describe el sistema")
   - Deben referenciar los inputs necesarios
   - Deben incluir constraints de calidad del "Criterio de completitud"
   - Deben advertir sobre los anti-patrones

4. CONSTRAINTS:
   - El template debe ser auto-contenido (el agente que lo use no necesita 
     consultar el diccionario)
   - Las instrucciones deben ser suficientes para que un agente sin contexto 
     previo genere un output de calidad
   - El formato debe ser consistente entre todos los templates
   - Usar {{VARIABLES}} para todo lo que es project-specific

5. TIPO DE TEMPLATE:
   Según la clasificación del deliverable:
   - Tipo A (Documento): Secciones con prosa + tablas
   - Tipo B (Reporte): Tablas de datos + métricas + assessment
   - Tipo C (Checklist): Tabla ✅/❌ + decisión + firma
   - Tipo D (Código): Archivo con comentarios explicativos
   - Tipo E (Proceso): Pasos numerados + decisiones + diagrama
   - Tipo F (Lista): Tabla con campos por item + reglas

SALIDA:
El template completo en Markdown, listo para ser usado por un agente VTT.
No incluyas explicaciones fuera del template — solo el template.

ENTRADA DEL DICCIONARIO:
[PEGAR AQUÍ LA ENTRADA DEL DELIVERABLE DEL DICCIONARIO]
```

---

## 6. PROMPT PARA EL AGENTE QUE LLENA EL TEMPLATE (USO POSTERIOR)

Este prompt se usa cuando un agente VTT necesita producir un deliverable real para un proyecto.

```
CONTEXTO:
Eres un {{ROLE}} trabajando en el proyecto {{PROJECT_NAME}}. 
Necesitas producir el deliverable {{DELIVERABLE_ID}} — {{DELIVERABLE_NAME}}.

TEMPLATE:
[Se inyecta el template generado en el paso anterior]

INPUTS DEL PROYECTO:
[Se inyectan los deliverables previos que este deliverable necesita como input]

CONTEXTO DEL PROYECTO:
- Proyecto: {{PROJECT_NAME}}
- Dominio: {{DOMAIN_CONTEXT}}
- Stack: {{TECH_STACK}}
- [Otros contextos relevantes]

TAREA:
Llena el template con información real del proyecto. Sigue las instrucciones 
en los comentarios HTML de cada sección. Reemplaza todas las {{VARIABLES}} 
con valores reales. Elimina los comentarios HTML de instrucciones del output 
final.

CONSTRAINTS DE CALIDAD:
- Cada sección debe cumplir los criterios de completitud listados
- Evitar los anti-patrones documentados
- El documento debe ser auto-contenido (legible sin contexto adicional)
- Usar datos reales del proyecto, no placeholders genéricos

SALIDA:
El deliverable completo en Markdown, listo para revisión por {{APPROVER}}.
```

---

## 7. PLAN DE EJECUCIÓN

### Fase de generación de templates

| Lote | Fase SDLC | Deliverables | Templates a generar | Sesiones estimadas |
|------|-----------|-------------|--------------------|--------------------|
| 1 | 4 Development | 78 | ~70 (8 auto-gen) | 4-5 |
| 2 | 3B Technical Design | 73 | ~70 (3 auto-gen) | 4-5 |
| 3 | 3A UX/UI Design | 72 | ~65 (7 auto-gen) | 4-5 |
| 4 | 5 Testing | 52 | ~45 (7 auto-gen) | 3 |
| 5 | 2 Analysis | 47 | ~45 (2 auto-gen) | 3 |
| 6 | 6 Deploy | 38 | ~30 (8 auto-gen) | 2 |
| 7 | 1 Planning | 33 | ~32 (1 auto-gen) | 2 |
| 8 | 7 Operations | 23 | ~20 (3 auto-gen) | 1-2 |
| 9 | 0 Discovery | 22 | ~22 | 1-2 |
| **TOTAL** | | **438** | **~400** | **~25 sesiones** |

### Ritmo sugerido

- **Agresivo:** 2 sesiones/día × 15 templates/sesión = 13 días laborales (~2.5 semanas)
- **Normal:** 1 sesión/día × 15 templates/sesión = 25 días laborales (~5 semanas)
- **Conservador:** 1 sesión cada 2 días × 10 templates/sesión = 40 días (~8 semanas)

### Proceso por sesión

1. El PM selecciona los N deliverables del lote
2. Por cada deliverable:
   a. Copia la entrada del diccionario
   b. Ejecuta el prompt de generación de template (Sección 5)
   c. El agente genera el template
   d. El PM revisa y aprueba (o pide ajustes)
3. Templates aprobados se guardan en la estructura de carpetas (Sección 8)
4. Se actualiza el tracking de progreso

---

## 8. NAMING CONVENTION Y ESTRUCTURA DE CARPETAS

### Estructura de carpetas

```
templates/
├── fase-00-discovery/
│   ├── 0.3.1_problem-statement.md
│   ├── 0.3.2_user-pain-points.md
│   └── ...
├── fase-01-planning/
│   ├── 1.1.1_vision-statement.md
│   └── ...
├── fase-02-analysis/
│   ├── 2.3.1_use-case-document.md
│   └── ...
├── fase-03a-design-ux/
│   ├── 3A.1.1_user-research-plan.md
│   └── ...
├── fase-03b-design-technical/
│   ├── 3B.1.1_architecture-document.md
│   └── ...
├── fase-04-development/
│   ├── documents/
│   │   ├── 4.1.2_environment-setup-guide.md
│   │   └── ...
│   └── code/
│       ├── 4.1.1_docker-compose.yml
│       ├── 4.1.3_env-example
│       ├── 4.1.5_makefile
│       └── ...
├── fase-05-testing/
│   ├── 5.1.1_test-plan.md
│   └── ...
├── fase-06-deploy/
│   ├── documents/
│   │   ├── 6.2.6_pipeline-documentation.md
│   │   └── ...
│   └── code/
│       ├── 6.2.1_ci-pipeline.yml
│       └── ...
├── fase-07-operations/
│   ├── 7.1.1_uptime-report.md
│   └── ...
└── _master-templates/
    ├── TIPO-A_documento.md
    ├── TIPO-B_reporte.md
    ├── TIPO-C_checklist-signoff.md
    ├── TIPO-D_codigo-config.md
    ├── TIPO-E_proceso-guia.md
    ├── TIPO-F_lista-backlog.md
    └── TIPO-G_verificacion.md
```

### Naming convention de archivos

```
{{DELIVERABLE_ID}}_{{deliverable-name-kebab-case}}.{{extension}}
```

Ejemplos:
- `5.1.1_test-plan.md`
- `4.1.1_docker-compose.yml`
- `6.4.3_smoke-test-signoff.md`
- `3A.2.1_personas-document.md`

---

## 9. EJEMPLO COMPLETO: TEMPLATE GENERADO

A continuación un ejemplo de cómo se ve un template generado para el deliverable **5.1.1 Test Plan** (Tipo A — Documento).

```markdown
# 5.1.1 — Test Plan

## Metadata

| Campo | Valor |
|-------|-------|
| **Proyecto** | {{PROJECT_NAME}} |
| **Fase** | 5-Testing |
| **Subfase** | 5.1 Test Planning |
| **Versión** | 1.0 |
| **Fecha** | {{DATE}} |
| **Autor** | {{QA_LEAD_NAME}} |
| **Revisor** | {{TECH_LEAD_NAME}} |
| **Aprobador** | {{TECH_LEAD_NAME}} |
| **Estado** | Borrador |

## Control de versiones

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | {{DATE}} | {{QA_LEAD_NAME}} | Versión inicial |

---

## 1. Objetivos de testing

<!-- INSTRUCCIÓN PARA EL AGENTE:
Describe los objetivos principales del testing para este proyecto.
- Formato: 3-5 bullets concisos
- Cada objetivo debe ser específico y medible
- Derivar de: use cases (2.3.4), business rules (2.5.1), y NFRs
- NO escribir "verificar que todo funciona" — ser específico
- Ejemplo: "Verificar que los 12 use cases principales funcionan 
  según los acceptance criteria definidos"
-->

- Verificar que {{USE_CASE_COUNT}} use cases principales funcionan según acceptance criteria
- Validar que las {{BUSINESS_RULE_COUNT}} business rules se aplican correctamente
- Confirmar que los NFRs de performance se cumplen (latencia p95 < {{LATENCY_TARGET}}ms)
- Verificar integración con {{INTEGRATION_COUNT}} servicios externos
- Validar accesibilidad WCAG 2.1 AA

## 2. Scope

<!-- INSTRUCCIÓN PARA EL AGENTE:
Define qué está dentro y fuera del alcance de testing.
- Formato: dos sub-secciones (In-scope / Out-of-scope)
- In-scope: listar módulos, features, plataformas, browsers
- Out-of-scope: listar qué NO se testea y por qué
- Derivar de: test scope (5.1.3), sitemap (3A.3.1)
- Incluir browser/device matrix
- NO asumir que se testea todo — priorizar por riesgo
-->

### In-scope

| Módulo | Features | Prioridad |
|--------|----------|-----------|
| {{MODULE_1}} | {{FEATURES_1}} | Alta |
| {{MODULE_2}} | {{FEATURES_2}} | Alta |
| {{MODULE_3}} | {{FEATURES_3}} | Media |

### Browser/device matrix

| Browser | Desktop | Mobile |
|---------|---------|--------|
| Chrome (latest) | ✅ | ✅ |
| Safari (latest) | ✅ | ✅ (iOS) |
| Firefox (latest) | ✅ | ❌ |
| Edge (latest) | ✅ | ❌ |

### Out-of-scope

- {{OUT_OF_SCOPE_1}} — Razón: {{REASON_1}}
- {{OUT_OF_SCOPE_2}} — Razón: {{REASON_2}}

## 3. Tipos de testing

<!-- INSTRUCCIÓN PARA EL AGENTE:
Lista los tipos de testing que se ejecutarán con descripción breve de cada uno.
- Formato: tabla (tipo, descripción, herramienta, responsable, obligatorio)
- Tipos mínimos: functional, integration, E2E, performance, security, 
  accessibility, UAT
- Derivar herramientas de: technology stack (3B.1.5)
- NO omitir security ni accessibility — son obligatorios
-->

| Tipo | Descripción | Herramienta | Responsable | Obligatorio |
|------|-------------|-------------|-------------|-------------|
| Functional | Verificar cada feature funciona | Manual + {{TEST_TOOL}} | QA Engineer | ✅ |
| Integration | Verificar integración entre componentes | Jest + Supertest | QA Automation | ✅ |
| E2E | Verificar flujos completos | Playwright | QA Automation | ✅ |
| Performance | Verificar latencia y throughput bajo carga | k6 | QA Automation | ✅ |
| Security | Verificar OWASP Top 10, auth, data protection | OWASP ZAP + manual | Security Engineer | ✅ |
| Accessibility | Verificar WCAG 2.1 AA | axe-core + VoiceOver | QA Engineer | ✅ |
| UAT | Validación por usuarios de negocio | Manual | Product Owner | ✅ |

[... secciones 4-10 continúan con el mismo patrón ...]

---

## Aprobación

| Rol | Nombre | Fecha | Firma |
|-----|--------|-------|-------|
| QA Lead (autor) | {{QA_LEAD_NAME}} | | |
| Tech Lead (aprobador) | {{TECH_LEAD_NAME}} | | |

---

## Referencias

- **Inputs:** Use Cases (2.3.4), Business Rules (2.5.1), OpenAPI Spec (3B.4.1)
- **Habilita:** Test Scope (5.1.3), Test Cases (5.2.1), todos los tipos de testing (5.4-5.10)
```

---

## 10. CRITERIOS DE CALIDAD DE UN TEMPLATE

Cada template generado se evalúa contra estos criterios:

### Must-have (obligatorio)

- [ ] Metadata completa con variables {{}}
- [ ] Control de versiones
- [ ] Todas las secciones del diccionario presentes como H2
- [ ] Instrucciones HTML por cada sección
- [ ] Placeholders con estructura visible (tablas, listas, prosa)
- [ ] Variables {{}} para todo lo project-specific
- [ ] Sección de aprobación
- [ ] Sección de referencias con inputs y successors

### Should-have (recomendado)

- [ ] Ejemplo de contenido real (no solo headers vacíos)
- [ ] Constraints derivados de anti-patrones
- [ ] Formato sugerido por sección (tabla vs prosa vs lista)
- [ ] Nivel de detalle esperado por sección

### Nice-to-have (deseable)

- [ ] Mini-ejemplo de una sección completamente llena con datos ficticios
- [ ] Tips específicos para el agente basados en el "Perfil de ejecución"
- [ ] Referencia a deliverables anteriores que el agente debe consultar

---

## 11. DELIVERABLES QUE NO NECESITAN TEMPLATE COMPLETO (TIPO G)

Estos ~40 deliverables son auto-generados o son valores/verificaciones simples. Solo necesitan un mini-checklist:

| Deliverable | Razón | Acción |
|-------------|-------|--------|
| 4.6.4 Coverage ≥80% | Métrica, no documento | Checklist de verificación |
| 5.5.2 Integration Test Results | Auto-generado por CI | Checklist de verificación |
| 5.5.4 Integration Coverage | Métrica calculada | Checklist de verificación |
| 5.6.2 E2E Test Results | Auto-generado por Playwright | Checklist de verificación |
| 5.6.3 Critical Path Coverage | Métrica calculada | Checklist de verificación |
| 6.3.1 Staging Deploy | Log automático de CD | Checklist de verificación |
| 6.3.2 Staging URL | URL, no documento | Checklist de verificación |
| 6.3.3 Migration Run | Log automático | Checklist de verificación |
| 6.5.1 Production Deploy | Log automático de CD | Checklist de verificación |
| 6.5.2 Production URL | URL, no documento | Checklist de verificación |
| 6.5.3 DNS Configured | Config, verificación | Checklist de verificación |
| 6.5.4 SSL Active | Verificación | Checklist de verificación |
| 6.5.6 Deployment Log | Log automático | Checklist de verificación |
| 5.2.2 Test Case IDs | Convención, no documento | Incluido en 5.2.1 |
| 5.2.4 Expected Results | Incluido en cada TC | Incluido en 5.2.1 |
| ... | ... | ... |

**Template mini-checklist para Tipo G:**

```markdown
# {{DELIVERABLE_ID}} — {{DELIVERABLE_NAME}} (Verificación)

## Metadata
| Campo | Valor |
|-------|-------|
| **Proyecto** | {{PROJECT_NAME}} |
| **Fecha verificación** | {{DATE}} |
| **Verificado por** | {{VERIFIER}} |

## Checklist de verificación

- [ ] {{CRITERION_1}}
- [ ] {{CRITERION_2}}
- [ ] {{CRITERION_3}}

## Evidencia

| Criterio | Status | Evidencia/Link |
|----------|--------|----------------|
| {{CRITERION_1}} | ✅/❌ | {{LINK}} |
| {{CRITERION_2}} | ✅/❌ | {{LINK}} |

## Resultado: ✅ VERIFICADO / ❌ NO CUMPLE
```

---

## 12. INSTRUCCIONES PARA INICIAR LA PRIMERA SESIÓN

### Preparación

1. Tener abierto el archivo del diccionario de la fase que vas a procesar
2. Tener este documento de estrategia como referencia
3. Elegir los primeros 10-15 deliverables del lote

### Prompt de inicio de sesión

```
Vamos a generar templates de deliverables para el SDLC. 

CONTEXTO:
- Tengo un diccionario de deliverables con 438 entradas
- Cada entrada tiene: metadatos, qué es, para qué sirve, inputs, 
  dependencias, secciones esperadas, criterios de completitud, y anti-patrones
- Necesito generar un template MD por deliverable para uso de agentes VTT
- El template debe seguir el formato del documento de estrategia 
  [adjuntar este documento o el meta-template de la sección 3]

TAREA DE HOY:
Generar templates para los deliverables {{LISTA DE IDs}}.
Te voy a pasar la entrada del diccionario de cada uno.

FORMATO DE OUTPUT:
Un archivo .md por template, guardado en /mnt/user-data/outputs/ 
con naming: {{ID}}_{{name-kebab}}.md

¿Listo? Te paso el primero.
```

### Después del primer template

1. Revisar que cumple los criterios de calidad (Sección 10)
2. Si está bien → aprobar y continuar con el siguiente
3. Si necesita ajustes → dar feedback específico y re-generar
4. Una vez aprobado el formato del primero, los siguientes van más rápido (el agente ya entendió el patrón)

---

## 13. TRACKING DE PROGRESO

Mantener una tabla de tracking actualizada por sesión:

| Fase | Total | Generados | Pendientes | % Completado | Última sesión |
|------|-------|-----------|------------|-------------|---------------|
| 0 Discovery | 22 | 0 | 22 | 0% | — |
| 1 Planning | 33 | 0 | 33 | 0% | — |
| 2 Analysis | 47 | 0 | 47 | 0% | — |
| 3A Design UX | 72 | 0 | 72 | 0% | — |
| 3B Design Tech | 73 | 0 | 73 | 0% | — |
| 4 Development | 78 | 0 | 78 | 0% | — |
| 5 Testing | 52 | 0 | 52 | 0% | — |
| 6 Deploy | 38 | 0 | 38 | 0% | — |
| 7 Operations | 23 | 0 | 23 | 0% | — |
| **TOTAL** | **438** | **0** | **438** | **0%** | — |
