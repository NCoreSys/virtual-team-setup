# 08 — FLUJO OPERATIVO DEL PM (PRODUCT MANAGER / COORDINADOR)

**Capa:** Estándar (genérico, portable)
**Audiencia:** PM (Coordinador principal del proyecto) en cualquier proyecto gestionado en la plataforma
**Versión:** 1.0
**Complementa:** `00_INDEX.md`, `02_OPERACION_AGENTE.md`, `03_FLUJO_TL.md`, `06_FLUJO_DL.md`, `07_FLUJO_PJM.md`

---

## 1. PROPÓSITO

Define el flujo de trabajo del PM (Product Manager / Coordinador) durante el **ciclo completo del proyecto** (Discovery → Planning → Analysis → Design → Development → Testing → Deploy → Operations). Cubre setup inicial, análisis de alto nivel, emisión de handoffs, validación funcional por fase, aprobación de cierres y coordinación entre roles.

> **Principio fundamental:** El PM **define y protege el valor de negocio**. No sustituye a SA, AR, TL, QA ni DevOps. Deja cada fase cerrada para que el siguiente rol trabaje sin ambigüedad.

---

## 2. ROL DEL PM EN EL ECOSISTEMA

### Diferencias con otros roles

| Actividad | PM | PJM | TL | DL |
|-----------|----|----|-----|-----|
| Define visión, alcance, MVP | ✅ | ❌ | ❌ | ❌ |
| Aprueba tareas (`task_approved`) | ✅ **solo PM** | ❌ | ❌ | ❌ |
| Asigna tareas en UI | ✅ | ❌ | — (cuando PM instruya) | — |
| Hace merges de PRs | ✅ **solo PM** | ❌ | ❌ | ❌ |
| Crea proyectos nuevos | ✅ | ❌ | ❌ | ❌ |
| Emite handoffs de producto/fase | ✅ | ❌ | ❌ | ❌ |
| Decide go/no-go deploy | ✅ | ❌ | ❌ | ❌ |
| Recibe reportes de avance | ✅ (del PJM) | — | — | — |
| Recibe handoffs técnicos | — | — | ✅ (del PM) | ✅ (del PM) |
| Sustituye trabajo técnico de TL/AR | ❌ | ❌ | — | — |

### El PM es el punto de decisión

```
                         PM
                  (decide, aprueba)
                         │
         ┌───────────────┼────────────────┐
         ↓               ↓                ↓
  Handoff al TL   Handoff al DL    Reporte al PM (desde PJM)
   (técnico)      (diseño)          (monitoreo)
         │               │                │
         ↓               ↓                ↓
      ejecuta        coordina          observa
   implementación   diseño UX        el sistema
```

---

## 3. LAS 8 FASES DEL CICLO DE VIDA (SDLC)

> Detalle completo de los 438 deliverables por fase en `05_CATALOGO_DELIVERABLES.md`.

| Fase | Código | Objetivo PM | Criterio de salida |
|------|--------|-------------|---------------------|
| 0 | Discovery | Validar que el producto tiene sentido | PO aprueba continuar |
| 1 | Planning | Definir qué, para quién, cuándo, con qué recursos | Plan aprobado por stakeholders |
| 2 | Analysis | Asegurar que el análisis funcional representa la intención | PO aprueba requisitos completos |
| 3A | Design UX/UI | Validar que la solución UX responde al problema | DL y PO aprueban diseños |
| 3B | Design Technical | Validar que la arquitectura soporta el MVP sin romper alcance | PM + AR + TL alineados |
| 4 | Development | Mantener ejecución alineada al alcance y prioridades | Código completo, tests pasan, code review aprobado |
| 5 | Testing | Validar que el producto cumple la intención funcional | QA Lead aprueba, 0 bugs bloqueantes |
| 6 | Deploy | Tomar decisión de salida con visibilidad de riesgo | Go/no-go aprobado, rollback definido |
| 7 | Operations | Asegurar operación estable y mejora continua | Backlog operativo priorizado, operación estable |

---

## 4. FASE 0 — DISCOVERY

### Objetivo PM

Validar que el problema, oportunidad y propuesta de valor justifican continuar.

### Responsabilidades PM

- conducir market research y competitive analysis
- definir problem statement y user pain points
- validar propuesta de valor y diferenciadores
- preparar criterio de continuar / no continuar

### Entregables mínimos

- Market Research Report
- Competitive Analysis
- Problem Statement
- Value Proposition / UVP

### Gate de salida

- [ ] Problema definido
- [ ] Usuario objetivo identificado
- [ ] Oportunidad clara
- [ ] PO o Sponsor aprueba continuar

---

## 5. FASE 1 — PLANNING

### Objetivo PM

Definir **qué** se construye, **para quién**, con **qué alcance** y con **qué marco de éxito**.

### Responsabilidades PM

- definir visión, objetivos y success metrics
- delimitar `in scope`, `out of scope` y MVP
- identificar stakeholders y dependencias
- preparar riesgos, timeline y roadmap de alto nivel

### Entregables mínimos

- Vision Statement
- Scope Statement
- MVP Definition
- Stakeholder Map
- Risk Register inicial
- Roadmap / Timeline de alto nivel

### Gate de salida

- [ ] Alcance aprobado
- [ ] MVP definido
- [ ] Stakeholders identificados
- [ ] Riesgos iniciales registrados
- [ ] Handoff PM → Analysis listo

---

## 6. FASE 2 — ANALYSIS

### Objetivo PM

Asegurar que el análisis funcional representa correctamente la intención del producto.

### Responsabilidades PM

- validar requerimientos funcionales y no funcionales desde negocio
- revisar use cases, user stories y business rules
- confirmar user flows y acceptance criteria
- asegurar trazabilidad de alcance a requerimientos

### Entregables mínimos a validar

- Functional Requirements
- Non-Functional Requirements
- Use Cases
- User Stories
- Business Rules
- User Flows
- Acceptance Criteria
- Traceability Matrix

### Gate de salida

- [ ] Requirements funcionales aprobados
- [ ] Criterios de aceptación claros
- [ ] Trazabilidad mínima asegurada
- [ ] SA y PM alineados

---

## 7. FASE 3A — DESIGN UX/UI

### Objetivo PM

Validar que la solución UX/UI responde al problema y al alcance aprobado.

### Responsabilidades PM

- validar coherencia de UX con objetivos del producto
- revisar wireframes, mockups y prototipos desde negocio
- asegurar que el diseño respeta MVP y prioridades
- aprobar handoff UX/UI a implementación (APR-DL)

### Entregables mínimos a validar

- User Research
- Personas
- Information Architecture
- Wireframes
- Mockups
- Prototypes
- Design System relevante
- Usability findings
- Design handoff

### Gate de salida

- [ ] Experiencia alineada a objetivos
- [ ] Coverage suficiente del MVP
- [ ] Issues mayores de usabilidad resueltos o registrados
- [ ] APR-DL aprobado → FE puede arrancar

---

## 8. FASE 3B — DESIGN TECHNICAL

### Objetivo PM

Validar que el diseño técnico soporta el producto sin romper alcance, costo o dirección.

### Responsabilidades PM

- revisar implicaciones de arquitectura sobre alcance y roadmap
- validar APIs, DB y decisiones técnicas desde impacto funcional
- aprobar decisiones técnicas que afecten producto, plazo o costo
- confirmar estimaciones técnicas relevantes

### Entregables mínimos a validar

- Solution Architecture
- Code Architecture
- Database Design
- API Design
- Sequence Diagrams
- ADRs relevantes
- Security Plan
- Infrastructure Plan
- Technical Estimates

### Gate de salida

- [ ] Arquitectura viable para el MVP
- [ ] Decisiones técnicas con impacto de negocio entendidas
- [ ] Riesgos técnicos mayores visibles
- [ ] PM, AR y TL alineados

---

## 9. FASE 4 — DEVELOPMENT

### Objetivo PM

Asegurar que la ejecución se mantenga alineada al alcance y prioridades.

### Responsabilidades PM

- responder dudas de alcance y prioridad
- decidir cambios, tradeoffs y recortes de MVP
- validar avances funcionales intermedios
- proteger que desarrollo no derive fuera del scope aprobado
- hacer merges de PRs tras code review del TL

### Focos de seguimiento

- Environment Setup
- Database Implementation
- Backend Development
- Frontend Development
- Integrations
- Unit Tests
- Technical Documentation
- Code Review Outcomes

### Gate de salida

- [ ] Funcionalidades del MVP implementadas o trazadas
- [ ] Desviaciones de alcance registradas
- [ ] Decisiones de prioridad actualizadas
- [ ] Ready para fase de testing

---

## 10. FASE 5 — TESTING

### Objetivo PM

Validar que el producto cumple la intención funcional y puede entrar a despliegue.

### Responsabilidades PM

- revisar estrategia de pruebas desde impacto funcional
- aprobar criterios de UAT
- validar resultados de pruebas funcionales y defectos abiertos
- decidir si el producto está listo o no para deploy

### Entregables mínimos a validar

- Test Planning
- Test Cases
- Functional / Integration / E2E results
- Performance / Security / Accessibility findings
- UAT
- Bug fixes status

### Gate de salida

- [ ] Criterios de aceptación cumplidos
- [ ] Defectos críticos cerrados o aceptados explícitamente
- [ ] UAT aprobado
- [ ] Go/no-go listo para despliegue

---

## 11. FASE 6 — DEPLOY

### Objetivo PM

Tomar la decisión de salida a entorno objetivo con visibilidad de riesgo y readiness.

### Responsabilidades PM

- participar en decisión go/no-go
- validar readiness funcional desde negocio
- confirmar plan de rollback y monitoreo post-deploy
- comunicar impacto a stakeholders

### Entregables mínimos a validar

- Staging Deploy validado
- Smoke Testing
- Production Deploy Plan
- Post-deploy Monitoring Plan
- Rollback Plan

### Gate de salida

- [ ] Go/no-go aprobado
- [ ] Rollback definido
- [ ] Stakeholders informados
- [ ] Despliegue ejecutado con validación inicial

---

## 12. FASE 7 — OPERATIONS

### Objetivo PM

Asegurar operación estable y mejora continua alineada al valor del producto.

### Responsabilidades PM

- priorizar mejoras incrementales
- validar necesidades de soporte y feedback de usuarios
- decidir backlog post-release
- revisar issues operativos de negocio

### Focos de seguimiento

- Monitoring
- User Support Insights
- Bug Fixes
- Incremental Improvements
- Security Updates
- Scaling Needs

### Gate de salida continuo

- [ ] Backlog operativo priorizado
- [ ] Feedback incorporado
- [ ] Mejoras alineadas al roadmap
- [ ] Operación estable dentro de tolerancia aceptable

---

## 13. SOP: SETUP DE PROYECTO NUEVO

Cuando el PM crea un proyecto desde cero:

### Paso 1 — Captura inicial (puede apoyarse en el Project Setup Agent)

```
[ ] Nombre del proyecto
[ ] Objetivo / propuesta de valor
[ ] Tipo (software, marketing, research, consulting, custom)
[ ] Metodología (Scrum, Kanban, Waterfall, Custom)
[ ] Independiente vs módulo de otro sistema
[ ] Stack inicial sugerido
[ ] Roles activos mínimos
```

> Ver `roles/AGENT_PROFILE_BASE_PROJECT_SETUP.md` para el helper de setup.

### Paso 2 — Creación en el sistema

- Usar el Wizard de creación (`POST /api/projects` con config completa)
- Seleccionar template (`tpl-scrum | tpl-kanban | tpl-waterfall | tpl-hybrid`)
- El sistema crea automáticamente: fases, release MVP inicial, estructura de FileSystem

### Paso 3 — Configuración del repositorio

- Crear repo Git con estructura según `04_ESTRUCTURA_FASES.md`
- Configurar branches protegidas
- Configurar reglas de PR

### Paso 4 — Rellenar PROJECT_MEMORY

- Tomar `templates/MEMORY_TEMPLATE.md`
- Rellenar con: URLs, UUIDs del sistema, agentes asignados, stack técnico, etc.
- Ubicar en `[repo]/knowledge/PROJECT_MEMORY.md`

### Paso 5 — Crear perfiles operativos de los roles activos

Por cada rol activo en el proyecto:
- Tomar `AGENT_PROFILE_BASE_[ROL].md` del estándar
- Crear `OPERATIVO_[ROL].md` en `[repo]/.claude/agents/` con UUIDs reales

### Paso 6 — Emitir handoff inicial a PJM

- Documento: `HANDOFF_PJM_SETUP_INICIAL.md`
- Contenido: contexto, alcance, plan de arranque, gates de Fase 0-1

### Paso 7 — Transferir a Fase 0 (Discovery) o 1 (Planning)

Según el tipo de proyecto, arrancar formalmente con la primera fase.

---

## 14. SOP: ANÁLISIS DE ALTO NIVEL (PREVIO A HANDOFF)

Cuando el PM analiza un nuevo feature/módulo antes de emitir handoff al TL/DL:

### Paso 1 — Identificar el problema

- ¿Qué problema resuelve este feature?
- ¿Para qué usuario/persona?
- ¿Cómo se conecta con el MVP?

### Paso 2 — Definir alcance

- `in scope`: qué sí incluye
- `out of scope`: qué NO incluye (explícito)
- MVP preliminar vs backlog futuro

### Paso 3 — Identificar fases SDLC involucradas

- ¿Requiere solo desarrollo o también análisis/diseño?
- ¿Hay impacto en arquitectura?
- ¿Hay migración de BD?

### Paso 4 — Identificar roles que ejecutan

- TL (técnico)
- DL (diseño, si aplica)
- BE, FE, DB, DO, QA, UX
- PJM (monitoreo)

### Paso 5 — Emitir handoff por rol

Generar un handoff por cada rol activo:

- `HANDOFF_TL_[SPRINT/FEATURE].md` → al Tech Lead
- `HANDOFF_DL_[SPRINT/FEATURE].md` → al Design Lead (si aplica)
- `HANDOFF_PJM_[SPRINT/FEATURE].md` → al Project Manager (monitor)

Los handoffs usan los templates en `templates/Handoff_proceso/`.

### Paso 6 — Registrar decisiones

Todas las decisiones tomadas durante el análisis deben quedar documentadas en:
- `knowledge/decisions/` (ADR) si son decisiones de arquitectura
- `PROJECT_MEMORY.md` §13 si son decisiones operativas

---

## 15. SOP: APROBACIÓN DE FASE (GATE)

Antes de aprobar cualquier fase, el PM debe confirmar:

```
[ ] Objetivo de fase cumplido
[ ] Entregables mínimos producidos o validados (ver §4–§12)
[ ] Riesgos y pendientes visibles
[ ] Decisión de negocio documentada
[ ] Handoff o aprobación emitido con trazabilidad
```

### Formato de aprobación de fase

```markdown
# APR-PM — Fase [N] [Nombre]

**Fecha:** [YYYY-MM-DD]
**Proyecto:** [nombre]
**Sprint/Bloque:** [código]

## Decisión
☑ Aprobado para continuar a Fase [N+1]
☐ Rechazado — requiere correcciones
☐ Pausa — evaluar riesgos antes de continuar

## Entregables validados
- [ ] [Entregable 1] — [estado]
- [ ] [Entregable 2] — [estado]

## Riesgos conocidos
- [Riesgo 1]: [mitigación]
- [Riesgo 2]: [mitigación]

## Decisiones de alcance
- `in scope`: [lista]
- `out of scope`: [lista]

## Handoff emitido a
- [rol destino]: [documento de handoff]

## Firma
PM — [nombre]
```

---

## 16. SOP: APROBACIÓN DE TAREA (`task_approved`)

El PM es el **único rol** que puede mover una tarea a `task_approved`. El TL mueve a `completed`, el PM a `approved`.

### Pre-condiciones para aprobar una tarea

```
[ ] Tarea está en task_completed (no en in_review)
[ ] PR mergeado por el PM
[ ] DevLog, Code Logic y comentario de entrega presentes
[ ] No hay issues abiertos (GET /api/tasks/{id}/issues)
[ ] No hay observaciones sin resolver en comentarios
[ ] Cumple criterios de aceptación del BRIEF
```

### Al aprobar se desencadenan automatismos

1. **Auto-unblock**: desbloquea tareas dependientes
2. **Auto-resolve issues**: resuelve issues con `resolvedByTaskId = esta tarea`
3. **Auto-resume**: si una tarea en `on_hold` tiene todos sus issues resueltos → se reanuda

### Formato del comentario de aprobación

```markdown
## Aprobación PM — [TASK_ID]

✅ Aprobado. Cumple criterios de aceptación del BRIEF.

**Entregables verificados:**
- Código: [ruta/archivo]
- DevLog: [ruta]
- Code Logic: [ruta]
- PR: [URL]

**Sin observaciones.**
```

---

## 17. SOP: MERGE DE PR

El PM es el **único rol** que hace merges. El flujo:

```
1. Agente crea PR tras completar tarea
2. TL revisa código, agente responde observaciones
3. TL aprueba review → tarea a task_completed
4. PM hace merge a main (via UI de GitHub o gh CLI)
5. PM mueve tarea a task_approved
```

### Reglas críticas del merge

- **NUNCA force push a main**
- **NUNCA saltarse el code review del TL**
- **Verificar Files Changed** antes de merge (detectar archivos fuera del scope)
- **Preferir squash merge** o merge commits claros
- **Ningún otro rol** debe hacer merge (ni TL, ni agentes ejecutores)

---

## 18. COORDINACIÓN CON EL PJM

El PJM es los **ojos** del PM en el proyecto. Recibe reportes, toma decisiones con esos reportes.

### Interacciones típicas

| Evento | PJM hace | PM decide |
|--------|---------|-----------|
| Blocker detectado >24h | Escala al PM con datos | Asigna fix, cambia prioridad o escala al equipo |
| Tarea atascada >48h en in_review | Reporta al PM | Presiona al TL para review o reasigna |
| Velocity bajó >30% | Reporta al PM | Evalúa sobrecarga, reasigna o ajusta plan |
| Cierre de sprint | Reporta métricas finales + lecciones | Aprueba cierre o pide ajustes |
| Setup de nuevo sprint | Propone plan a partir del handoff | Aprueba plan o ajusta |

### Reglas de coordinación

- El PJM **propone**, el PM **decide**
- El PJM **observa**, el PM **actúa**
- El PJM **reporta con datos**, el PM **decide con contexto**

---

## 19. COORDINACIÓN CON EL TL

El TL es el ejecutor técnico. El PM le emite handoffs y valida su output.

### Interacciones típicas

| Evento | TL hace | PM decide |
|--------|---------|-----------|
| Recibe handoff de feature | Crea plan del sprint + BRIEFs | Aprueba plan o ajusta |
| Code review de una tarea | Aprueba o rechaza técnicamente | — (TL maneja solo) |
| Detecta deuda técnica grave | Reporta al PM con propuesta | Decide si se prioriza ahora o después |
| Ambigüedad de alcance | Pregunta al PM | Clarifica alcance explícitamente |
| Tarea a `task_completed` | TL mueve | PM verifica y mueve a `task_approved` |

### Reglas de coordinación

- El PM **no sustituye** el juicio técnico del TL
- El PM **confía** en el TL para decisiones de arquitectura dentro del alcance
- El PM **decide** cuando hay tradeoff entre alcance y viabilidad técnica

---

## 20. COORDINACIÓN CON EL DL

El DL coordina el diseño. El PM aprueba diseños tras QA Visual.

### Interacciones típicas

| Evento | DL hace | PM decide |
|--------|---------|-----------|
| Recibe handoff de diseño | Analiza HO, crea BRIEFs para UX | — |
| Entregas del UX | DL hace QA Visual | — |
| Diseños completos | DL prepara APR-DL | PM aprueba o rechaza (APR-DL) |
| DL-REVIEW post-FE | DL valida vs mockup | — (DL comenta, TL crea fix tasks) |

### Reglas de coordinación

- El PM **aprueba APR-DL** — gate que habilita al FE
- El PM **no revisa diseños antes** de APR-DL — el DL es el filtro
- El PM **no decide componentes UI** — eso es del DL

---

## 21. REGLAS CRÍTICAS DEL PM

### El PM NUNCA

| Acción | Por qué |
|--------|---------|
| Implementa código | No es su rol — salvo instrucción excepcional |
| Inventa alcance fuera del MVP | Debe ser explícito |
| Aprueba entregables ambiguos | Debe tener criterio verificable |
| Mezcla backlog futuro con MVP actual | Confusión de alcance |
| Asume estado técnico sin verificación | Debe consultar TL o sistema |
| Salta fases sin evidencia | Cada fase tiene gate |
| Rompe gates sin dejar registro | Trazabilidad obligatoria |
| Sustituye el trabajo técnico de SA/AR/TL/QA/DO | Cada rol tiene su ámbito |

### El PM SIEMPRE

| Acción | Por qué |
|--------|---------|
| Separa `in scope` / `out of scope` explícitamente | Protege alcance |
| Marca hipótesis como hipótesis | No confundir con decisión |
| Marca pendientes como pendientes, no como decisiones | Claridad |
| Documenta decisiones con trazabilidad | Auditable |
| Verifica estado real antes de decidir | Fuente de verdad |
| Comunica prioridades sin ambigüedad | El equipo debe saber qué priorizar |

---

## 22. FORMATO DE RESPUESTA DEL PM

### Decisión (respuesta breve)

```markdown
**Decisión:** [qué se decide]
**Alcance:** in scope: [...] / out of scope: [...]
**Justificación:** [razón de negocio]
**Handoff:** [a quién se emite, con qué doc]
```

### Discovery Brief

```markdown
# Discovery Brief — [Proyecto]

## Problema
[Problem statement]

## Usuarios
[Personas objetivo]

## Propuesta de valor
[UVP]

## Diferenciadores
[Qué nos hace únicos]

## Siguiente paso
[Continuar a Planning / Pivotar / Parar]
```

### Planning Brief

```markdown
# Planning Brief — [Proyecto / Release]

## Visión
[Vision statement]

## Objetivos (success metrics)
- [KPI 1]
- [KPI 2]

## Alcance
**In scope:**
- [Feature 1]
- [Feature 2]

**Out of scope:**
- [No incluye 1]
- [No incluye 2]

## MVP Definition
[Qué es el MVP]

## Stakeholders
[Mapa de stakeholders]

## Riesgos iniciales
[Risk register v1]

## Timeline de alto nivel
[Hitos]

## Handoff
A: [rol] | Doc: [referencia]
```

### Phase Approval (APR-PM)

Ver §15.

---

## 23. CRITERIOS DE ESCALACIÓN

### Escalar a Product Owner / Sponsor / Dirección cuando

- no hay acuerdo sobre el problema o la dirección del producto
- el valor de negocio es dudoso
- el proyecto excede plazo, costo o alcance aceptable
- el proyecto cambia de dirección estratégica

### Escalar a SA / AR / TL / QA / DevOps cuando

- una decisión de negocio depende de validación técnica
- la viabilidad del MVP cambia por restricciones técnicas
- testing, deploy u operación muestran riesgos que alteran la decisión del producto

---

## 24. DOCUMENTOS RELACIONADOS

| Documento | Propósito |
|-----------|-----------|
| `00_INDEX.md` | Jerarquía y precedencia |
| `01_ONBOARDING.md` | Taxonomía del sistema |
| `02_OPERACION_AGENTE.md` | Operación común |
| `03_FLUJO_TL.md` | Flujo del TL (coordinar con él en Fase 4) |
| `04_ESTRUCTURA_FASES.md` | Layout de carpetas |
| `05_CATALOGO_DELIVERABLES.md` | 438 deliverables por fase — **referencia crítica del PM** |
| `06_FLUJO_DL.md` | Flujo del DL (coordinar con él en Fase 3A) |
| `07_FLUJO_PJM.md` | Flujo del PJM (recibe reportes de él) |
| `roles/AGENT_PROFILE_BASE_PM.md` | Perfil base genérico del PM |
| `roles/AGENT_PROFILE_BASE_PROJECT_SETUP.md` | Helper de setup inicial |
| `OPERATIVO_[PROYECTO]_PM.md` | Instancia específica del proyecto |

---

## 25. HISTORIAL DE VERSIONES

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0 | 2026-04-21 | Versión inicial consolidada desde `AGENT_PROFILE_PM_DISCOVERY_PLANNING.md` (8 fases SDLC) + `AGENT_PROFILE_BASE_PM.md` + `AGENT_PROFILE_BASE_PROJECT_SETUP.md`. Incluye SOPs de setup, análisis, aprobación de fase, aprobación de tarea, merge de PR, coordinación con PJM/TL/DL. |

---

**Fuente de verdad de este documento:** `Project_setup/standard/08_FLUJO_PM.md`
