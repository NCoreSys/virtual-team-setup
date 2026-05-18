# 📚 ÍNDICE MAESTRO DE DOCUMENTOS — Memory Service

| Campo | Valor |
|-------|-------|
| **Documento** | INDICE_MAESTRO_DOCUMENTOS.md |
| **Versión** | 1.1 |
| **Fecha** | 2026-05-04 |
| **Autor** | PM (Martin Rivas) |
| **Propósito** | Índice navegable de **todos los documentos del proyecto**: qué es cada uno, para qué sirve, cuándo se usa, quién lo necesita. |
| **Audiencia** | Cualquiera que llegue al proyecto y necesite entender la documentación. |

---

## 🎯 CÓMO LEER ESTE ÍNDICE

Cada documento responde 4 preguntas:

| Pregunta | Significa |
|----------|-----------|
| **¿Qué es?** | Tipo de artefacto (HO, ADR, template, script, etc.) |
| **¿Para qué sirve?** | Qué problema resuelve / qué decisión documenta |
| **¿Cuándo se usa?** | Momento del proyecto en que se necesita |
| **¿Quién lo lee?** | Roles que lo consultan |

Los documentos están agrupados por **caso de uso**, no por carpeta. Si solo quieres trabajar, ve a la sección **"Quick start por rol"**.

---

## 🚦 QUICK START POR ROL — "Voy a empezar a trabajar, ¿qué leo?"

### Si eres PM
1. [`OPERATIVO_PM_MEMORY-SERVICE.md`](.claude/agents/OPERATIVO_PM_MEMORY-SERVICE.md) — qué hago como PM
2. [`CONTEXTO_PM_SESION.md`](knowledge/agent-tasks/CONTEXTO_PM_SESION.md) — estado actual de mi trabajo
3. Abrir [`pm.code-workspace`](memory-service-project/Release2.0/scripts/workspaces/pm.code-workspace) en VS Code

### Si eres PJM
1. Leer [`HO_PJM_CARGA_VTT_MEMORY_SERVICE.md`](memory-service-project/Release2.0/01-PM/HO_PJM_CARGA_VTT_MEMORY_SERVICE.md) — instrucciones de carga inicial
2. Leer [`CIERRE_PM_HANDOFF_PJM_MEMORY_SERVICE_R1.md`](memory-service-project/Release2.0/01-PM/CIERRE_PM_HANDOFF_PJM_MEMORY_SERVICE_R1.md) — plan completo del proyecto
3. Abrir [`pjm.code-workspace`](memory-service-project/Release2.0/scripts/workspaces/pjm.code-workspace)

### Si eres SA Reviewer
1. [`OPERATIVO_SA_REVIEWER.md`](.claude/agents/OPERATIVO_SA_REVIEWER.md) — procedimiento operativo completo (UUIDs, comandos, SOPs)
2. [`CONTEXTO_SA_REVIEWER_SESION.md`](memory-service-project/knowledge/agent-tasks/CONTEXTO_SA_REVIEWER_SESION.md) — estado actual de fases y tareas
3. HOs de entrada por fase activa (ver CASO 8)

### Si eres SA (ejecutor)
1. [`OPERATIVO_SA_MEMORY-SERVICE.md`](.claude/agents/OPERATIVO_SA_MEMORY-SERVICE.md) — procedimiento operativo
2. Tu ASSIGNMENT en `knowledge/agent-tasks/assignments/`

### Si eres TL / BE / DB / FE / QA / DO / AR / UX / DL
1. Leer [`WORKFLOW_OPERATIVO_MULTIREPO_MEMORY_SERVICE.md`](memory-service-project/Release2.0/01-PM/WORKFLOW_OPERATIVO_MULTIREPO_MEMORY_SERVICE.md) — cómo trabajo con 4 repos
2. Hacer bootstrap: clonar los repos relevantes
3. Abrir el `.code-workspace` correspondiente a tu rol (ver [`workspaces/README.md`](memory-service-project/Release2.0/scripts/workspaces/README.md))
4. Leer tu `OPERATIVO_<ROL>.md` (en `.claude/agents/`)

### Si llegaste al proyecto y no entiendes nada
1. Leer este índice (estás aquí ✅)
2. Leer [`PROJECT_MEMORY.md`](knowledge/PROJECT_MEMORY.md) — qué es Memory Service
3. Leer [`SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md`](memory-service-project/Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md) — el contrato técnico

---

## 📁 ÍNDICE POR CASO DE USO

### CASO 1 — Entender qué construye el proyecto

| Doc | ¿Qué es? | ¿Para qué? | ¿Cuándo? | ¿Quién? |
|-----|----------|-----------|----------|---------|
| [`PROJECT_MEMORY.md`](knowledge/PROJECT_MEMORY.md) | Memoria del proyecto | Resumen de stack, fases, decisiones, contexto general | Al onboarding · cada vez que arranca sesión | Todos |
| [`SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md`](memory-service-project/Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md) | Contrato técnico final | Definir CADA detalle: schema BD, 11 endpoints, flujos import, classifier, etc. | Antes de implementar código · referencia continua | TL, BE, DB, FE, QA, AR |
| [`METODOLOGIA_MEMORY_SERVICE_v1.2.md`](memory-service-project/Release2.0/01-PM/METODOLOGIA_MEMORY_SERVICE_v1.2.md) | Doc funcional | Explicar las 5 fuentes, 3 tipos de conversación, qué hace cada componente | Onboarding técnico | Todos los técnicos |
| [`ADDENDUM_INTEGRACION_MEMORY_SERVICE_v1.1.md`](memory-service-project/Release2.0/01-PM/ADDENDUM_INTEGRACION_MEMORY_SERVICE_v1.1.md) | Addendum integraciones | Cómo Memory se integra con Runtime v1.1 y Prompt Builder v1.3 | Cuando se trabaje con integraciones (S06) | TL, BE, AR |
| [`MEMORY_SERVICE_METODOLOGICO_v1.1.md`](memory-service-project/Release2.0/01-PM/MEMORY_SERVICE_METODOLOGICO_v1.1.md) | 🔴 OBSOLETO | Histórico — reemplazado por v1.2 | Solo referencia histórica | — |

### CASO 2 — Saber qué tareas hacer y en qué orden

| Doc | ¿Qué es? | ¿Para qué? | ¿Cuándo? | ¿Quién? |
|-----|----------|-----------|----------|---------|
| [`FASES_APLICABLES_MEMORY_SERVICE.md`](memory-service-project/Release2.0/01-PM/FASES_APLICABLES_MEMORY_SERVICE.md) | Filtro de deliverables | De los 438 deliverables del catálogo SDLC, cuáles aplican (390) y cuáles no (48) y por qué | Para entender el alcance documental | PM, PJM, TL |
| [`PRE_HANDOFF_INICIACION_MEMORY_SERVICE.md`](memory-service-project/Release2.0/01-PM/PRE_HANDOFF_INICIACION_MEMORY_SERVICE.md) | Tareas pre-SDLC | 24 sub-tareas operativas para iniciar el proyecto (VTT, repo, VM, team, tooling, kickoff) | Antes de Fase 0 Discovery | PM, PJM, DO |
| [`PRE_HANDOFF_IMPLEMENTACION_MEMORY_SERVICE.md`](memory-service-project/Release2.0/01-PM/PRE_HANDOFF_IMPLEMENTACION_MEMORY_SERVICE.md) | Tareas de código | 66 tareas de código/tests/deploy (desarrollo, testing, deploy, ops) | Cuando arranque Fase 4 Development | TL, BE, DB, FE, DO, QA |
| [`CONSOLIDADO_MEMORY_SERVICE_R1.md`](memory-service-project/Release2.0/01-PM/CONSOLIDADO_MEMORY_SERVICE_R1.md) | Plan maestro | Une iniciación + 9 fases SDLC + tareas con mapeo deliverable-tarea | Vista general del proyecto completo | PM, PJM, TL |
| [`PLAN_116_TAREAS.md`](knowledge/agent-tasks/PLAN_116_TAREAS.md) | Plan TL | Vista del Tech Lead: 116 tareas con horas, complexity, reassignments | Planificación operativa | TL, PJM |

### CASO 3 — Cargar el proyecto a VTT (carga inicial)

| Doc | ¿Qué es? | ¿Para qué? | ¿Cuándo? | ¿Quién? |
|-----|----------|-----------|----------|---------|
| [`CIERRE_PM_HANDOFF_PJM_MEMORY_SERVICE_R1.md`](memory-service-project/Release2.0/01-PM/CIERRE_PM_HANDOFF_PJM_MEMORY_SERVICE_R1.md) | ⭐ HO formal PM→PJM | Cierre del análisis PM + plan operativo completo (decisiones FROZEN, criterios de éxito, firmas) | Al cerrar la planeación, antes del kickoff | PJM (recibe), todos los líderes (firman) |
| [`TASK_INDEX_SEED_MEMORY_SERVICE.md`](memory-service-project/Release2.0/01-PM/TASK_INDEX_SEED_MEMORY_SERVICE.md) | Seed con UUIDs | Datos completos para que VTT cree todo (UUIDs, descripciones, metadata) | Insumo del script Python | PJM, TL |
| [`create_memory_service_vtt.py`](memory-service-project/Release2.0/scripts/create_memory_service_vtt.py) | Script ejecutable Python | Crear 1 Project + 10 Phases + 65 Deliveries + 116 Tasks + 15 Deps en VTT | Una sola vez al arrancar | PJM (ejecuta) |
| [`HO_PJM_CARGA_VTT_MEMORY_SERVICE.md`](memory-service-project/Release2.0/01-PM/HO_PJM_CARGA_VTT_MEMORY_SERVICE.md) | HO de ejecución | Instrucciones paso-a-paso para que el PJM ejecute el script (prerrequisitos, verificación, rollback) | Al ejecutar el script | PJM |
| [`HO_ACTUALIZAR_TAREAS_VTT.md`](memory-service-project/Release2.0/PJM/HO_ACTUALIZAR_TAREAS_VTT.md) | HO PJM v2.1 | Versión PJM con UUIDs de deliveries y mapeo a tareas | Referencia operativa | PJM |

### CASO 4 — Entender cómo trabajar (multi-repo, workspaces, VS Code)

| Doc | ¿Qué es? | ¿Para qué? | ¿Cuándo? | ¿Quién? |
|-----|----------|-----------|----------|---------|
| [`ADR-001_estrategia_repositorios.md`](memory-service-project/Release2.0/01-PM/ADR-001_estrategia_repositorios.md) | ADR de gobernanza | DECISIÓN: por qué 4 repos y no monorepo. Define PATs, branch protection, contratos cross-repo | Antes de configurar repos · referencia eterna | Todos (entender la decisión) |
| [`ESTRUCTURA_REPO_MEMORY_SERVICE.md`](memory-service-project/Release2.0/01-PM/ESTRUCTURA_REPO_MEMORY_SERVICE.md) | Blueprint físico | Qué carpetas crear en CADA uno de los 4 repos. Scripts bash de inicialización | Al ejecutar INIT-B-02 (estructura V3.1) | DO, PJM |
| [`WORKFLOW_OPERATIVO_MULTIREPO_MEMORY_SERVICE.md`](memory-service-project/Release2.0/01-PM/WORKFLOW_OPERATIVO_MULTIREPO_MEMORY_SERVICE.md) | Workflow operativo | CÓMO trabaja cada agente: qué clona, qué workspace abre, cómo commitea, cómo reporta | Al onboarding de cada agente | Todos los agentes activos |
| [`workspaces/README.md`](memory-service-project/Release2.0/scripts/workspaces/README.md) | Guía workspaces | Explica los 9 archivos `.code-workspace` y cómo usarlos | Una vez al setup local | Cualquier agente |
| [`workspaces/*.code-workspace`](memory-service-project/Release2.0/scripts/workspaces/) | Archivos VS Code | **Configuración multi-root**: cuando los abres con VS Code, ves los repos correctos para tu rol con sus permisos. **No son docs — son configuración de editor.** | Cada vez que abres VS Code para trabajar | Cada rol (1 archivo cada uno) |

### CASO 5 — Reproducir este proceso en otro proyecto (templates)

| Doc | ¿Qué es? | ¿Para qué? | ¿Cuándo? | ¿Quién? |
|-----|----------|-----------|----------|---------|
| [`INDEX_TEMPLATES_CIERRE_PM_HANDOFF_PJM.md`](memory-service-project/00-agent-setup/05.Templates/01.SETUP/01_PM/INDEX_TEMPLATES_CIERRE_PM_HANDOFF_PJM.md) | 📋 Índice de templates | Mapeo proceso ↔ templates: qué template usar en cada paso | Al iniciar otro proyecto | PM (de cualquier proyecto) |
| [`TEMPLATE_FASES_APLICABLES_V1.0.md`](memory-service-project/00-agent-setup/05.Templates/01.SETUP/01_PM/TEMPLATE_FASES_APLICABLES_V1.0.md) | Template filtro | Cómo escribir el filtro de deliverables aplicables | Paso 3 del proceso | PM |
| [`TEMPLATE_PRE_HANDOFF_INICIACION_V1.0.md`](memory-service-project/00-agent-setup/05.Templates/01.SETUP/01_PM/TEMPLATE_PRE_HANDOFF_INICIACION_V1.0.md) | Template iniciación | Cómo desglosar las 24 tareas de pre-SDLC | Paso 4 del proceso | PM |
| [`TEMPLATE_CONSOLIDADO_V1.0.md`](memory-service-project/00-agent-setup/05.Templates/01.SETUP/01_PM/TEMPLATE_CONSOLIDADO_V1.0.md) | Template plan maestro | Cómo unir iniciación + fases + tareas | Paso 5 del proceso | PM |
| [`TEMPLATE_CIERRE_PM_HANDOFF_PJM_V1.0.md`](memory-service-project/00-agent-setup/05.Templates/01.SETUP/01_PM/TEMPLATE_CIERRE_PM_HANDOFF_PJM_V1.0.md) | ⭐ Template HO principal | Estructura V4.2 del HO formal al PJM | Paso 6 del proceso | PM |
| [`TEMPLATE_TASK_INDEX_SEED_V1.0.md`](memory-service-project/00-agent-setup/05.Templates/01.SETUP/01_PM/TEMPLATE_TASK_INDEX_SEED_V1.0.md) | Template seed | Estructura del seed con UUIDs y campos VTT | Paso 7 del proceso | PM |
| [`TEMPLATE_create_vtt_script_V1.0.py`](memory-service-project/00-agent-setup/05.Templates/01.SETUP/01_PM/TEMPLATE_create_vtt_script_V1.0.py) | Template script Python | Esqueleto del script de creación | Paso 8 del proceso | PM |
| [`TEMPLATE_HO_PJM_CARGA_VTT_V1.0.md`](memory-service-project/00-agent-setup/05.Templates/01.SETUP/01_PM/TEMPLATE_HO_PJM_CARGA_VTT_V1.0.md) | Template HO ejecución | Estructura del HO de ejecución al PJM | Paso 9 del proceso | PM |
| [`ADDON_PASO0_ADR_REPOS_LECCION_APRENDIDA.md`](memory-service-project/00-agent-setup/06.Documentos_soporte/ADDON_PASO0_ADR_REPOS_LECCION_APRENDIDA.md) | Lección aprendida | PASO 0 del proceso: ADR de repos antes de cualquier estructura | Antes del PASO 1 | PM |

### CASO 6 — Configurar agentes IA y reglas

| Doc | ¿Qué es? | ¿Para qué? | ¿Cuándo? | ¿Quién? |
|-----|----------|-----------|----------|---------|
| [`OPERATIVO_PM_MEMORY-SERVICE.md`](.claude/agents/OPERATIVO_PM_MEMORY-SERVICE.md) | Procedimiento operativo PM | Identidad, UUIDs, comandos, SOPs del PM | Sesión del PM | Agente PM |
| [`OPERATIVO_PJM_MEMORY_SERVICE.md`](.claude/agents/OPERATIVO_PJM_MEMORY_SERVICE.md) | Procedimiento operativo PJM | Identidad, UUIDs, comandos del PJM | Sesión del PJM | Agente PJM |
| [`OPERATIVO_TECH_LEAD.md`](.claude/agents/OPERATIVO_TECH_LEAD.md) | Procedimiento operativo TL | Identidad, UUIDs, comandos del TL | Sesión del TL | Agente TL |
| [`OPERATIVO_SA_REVIEWER.md`](.claude/agents/OPERATIVO_SA_REVIEWER.md) | Procedimiento operativo SA Reviewer | Identidad, UUIDs, comandos, FASE 1 planificación + FASE 2 asignación + SOP revisión | Sesión del SA Reviewer | Agente SA Reviewer |
| [`OPERATIVO_SA_MEMORY-SERVICE.md`](.claude/agents/OPERATIVO_SA_MEMORY-SERVICE.md) | Procedimiento operativo SA ejecutor | Identidad, UUIDs, comandos del SA ejecutor | Sesión del SA | Agente SA |
| [`OPERATIVO_DL_MEMORY-SERVICE.md`](.claude/agents/OPERATIVO_DL_MEMORY-SERVICE.md) | Procedimiento operativo DL | Identidad, UUIDs, comandos del Design Lead | Sesión del DL | Agente DL |
| [`PROJECT_RULES.md`](.claude/rules/PROJECT_RULES.md) | Reglas del proyecto | Reglas obligatorias para todo agente del proyecto | Onboarding · cada sesión | Todos los agentes |
| [`Proyect_data.md`](.claude/rules/Proyect_data.md) | Datos del proyecto | UUIDs reales, emails, passwords de los agentes IA | Setup · referencia | PJM, DO |
| [`CONTEXTO_PM_SESION.md`](knowledge/agent-tasks/CONTEXTO_PM_SESION.md) | Contexto de sesión PM | Estado actual: qué tareas pendientes, decisiones, escalaciones | Cada sesión del PM | Agente PM |
| [`CONTEXTO_SA_REVIEWER_SESION.md`](memory-service-project/knowledge/agent-tasks/CONTEXTO_SA_REVIEWER_SESION.md) | Contexto de sesión SA Reviewer | Estado de fases 1-4: tareas en review, pending, blockers | Cada sesión del SA Reviewer | Agente SA Reviewer |

### CASO 8 — Handoffs operativos del PJM por fase (input del SA Reviewer)

> Estos HOs son el input que el SA Reviewer usa para generar BRIEFs y ASSIGNMENTs. Un HO por fase del SDLC.

| Doc | ¿Qué es? | ¿Para qué? | ¿Cuándo? | ¿Quién? |
|-----|----------|-----------|----------|---------|
| [`HO_FASE_0_DISCOVERY_MEMORY_SERVICE.md`](memory-service-project/Release2.0/PJM/HO_FASE_0_DISCOVERY_MEMORY_SERVICE.md) | HO PJM → SA Reviewer | Tareas, agentes y dependencias de Fase 0 Discovery | Al iniciar Discovery | SA Reviewer |
| [`HO_FASE_1_PLANNING_MEMORY_SERVICE.md`](memory-service-project/Release2.0/PJM/HO_FASE_1_PLANNING_MEMORY_SERVICE.md) | HO PJM → SA Reviewer | Tareas, agentes y dependencias de Fase 1 Planning | Al iniciar Planning | SA Reviewer |
| [`HO_FASE_2_ANALYSIS_MEMORY_SERVICE.md`](memory-service-project/Release2.0/PJM/HO_FASE_2_ANALYSIS_MEMORY_SERVICE.md) | HO PJM → SA Reviewer | Tareas, agentes y dependencias de Fase 2 Analysis | Al iniciar Analysis | SA Reviewer |
| [`HO_FASE_3A_DESIGN_UXUI_MEMORY_SERVICE.md`](memory-service-project/Release2.0/PJM/HO_FASE_3A_DESIGN_UXUI_MEMORY_SERVICE.md) | HO PJM → DL | Tareas de UX/UI Design | Al iniciar Design UX | DL, SA Reviewer |
| [`HO_FASE_3B_DESIGN_TECH_MEMORY_SERVICE.md`](memory-service-project/Release2.0/PJM/HO_FASE_3B_DESIGN_TECH_MEMORY_SERVICE.md) | HO PJM → TL | Tareas de diseño técnico/arquitectura | Al iniciar Design Tech | TL |
| [`HO_FASE_4_DEVELOPMENT_MEMORY_SERVICE.md`](memory-service-project/Release2.0/PJM/HO_FASE_4_DEVELOPMENT_MEMORY_SERVICE.md) | HO PJM → TL | Tareas de desarrollo | Al iniciar Development | TL |
| [`HO_FASE_5_TESTING_MEMORY_SERVICE.md`](memory-service-project/Release2.0/PJM/HO_FASE_5_TESTING_MEMORY_SERVICE.md) | HO PJM → TL/QA | Tareas de testing | Al iniciar Testing | TL, QA |
| [`HO_FASE_6_DEPLOY_MEMORY_SERVICE.md`](memory-service-project/Release2.0/PJM/HO_FASE_6_DEPLOY_MEMORY_SERVICE.md) | HO PJM → TL/DO | Tareas de deploy | Al iniciar Deploy | TL, DO |
| [`HO_FASE_7_OPERATIONS_MEMORY_SERVICE.md`](memory-service-project/Release2.0/PJM/HO_FASE_7_OPERATIONS_MEMORY_SERVICE.md) | HO PJM → DO | Tareas de operaciones | Al iniciar Operations | DO |

### CASO 7 — API VTT y estándares genéricos de plataforma

| Doc | ¿Qué es? | ¿Para qué? | ¿Cuándo? | ¿Quién? |
|-----|----------|-----------|----------|---------|
| [`11_GUIA_AGENTES_MODELO_DINAMICO_V4.md`](memory-service-project/00-agent-setup/03.standard/11_GUIA_AGENTES_MODELO_DINAMICO_V4.md) | ⭐ **Guía API VTT V4** | Referencia completa de endpoints, catálogos, living docs, devlog gate, trazabilidad, firmas — todo lo que un agente necesita para usar la API VTT | Siempre que se use la API VTT | **Todos los agentes** |
| [`METODOLOGIA_TRABAJO_PM_VTT.md`](memory-service-project/Release2.0/Analisis/METODOLOGIA_TRABAJO_PM_VTT.md) | Metodología PM VTT | Cómo trabaja un PM en cualquier proyecto VTT (filosofía + flujo) | Onboarding del PM | Cualquier PM |
| [`ANALISIS_FASES_COMPLETO_PARA_PM.md`](memory-service-project/Release2.0/Analisis/ANALISIS_FASES_COMPLETO_PARA_PM.md) | Catálogo SDLC | 438 deliverables del estándar VTT por fase | Insumo para FASES_APLICABLES | PM |
| [`ESTRUCTURA_FASES_DESARROLLO_PROYECTOS_V3.1.md`](memory-service-project/Release2.0/Analisis/ESTRUCTURA_FASES_DESARROLLO_PROYECTOS_V3.1.md) | Estándar de carpetas V3.1 | Cómo organizar carpetas en cualquier proyecto VTT | Setup de cualquier proyecto | PM, DO |
| [`PROCESO_ASIGNACION_TAREAS.md`](memory-service-project/Release2.0/Analisis/PROCESO_ASIGNACION_TAREAS.md) | Proceso TL VTT | Endpoints VTT, UUIDs globales, flujo de asignación | Operativa diaria | TL, PJM, DO |

---

## 🗂️ ÍNDICE POR TIPO DE DOCUMENTO

### Tipos y qué significan

| Tipo | Convención de nombre | Qué contiene |
|------|---------------------|--------------|
| **SPEC** | `SPEC_<NOMBRE>_v<X.Y>.md` | Contrato técnico — schema, endpoints, flujos |
| **METODOLOGIA** | `METODOLOGIA_<NOMBRE>_v<X.Y>.md` | Explicación funcional |
| **ADDENDUM** | `ADDENDUM_<TEMA>_v<X.Y>.md` | Anexo a un SPEC |
| **ADR** | `ADR-XXX_<tema>.md` | Architecture Decision Record (decisión arquitectural) |
| **HO** (Handoff) | `HO_<DESTINO>_<TEMA>.md` o `CIERRE_PM_HANDOFF_PJM_*.md` | Entrega formal entre roles |
| **PRE_HANDOFF** | `PRE_HANDOFF_<TEMA>_<PROYECTO>.md` | Insumo previo al HO formal |
| **CONSOLIDADO** | `CONSOLIDADO_<PROYECTO>_<RX>.md` | Plan maestro |
| **TASK_INDEX_SEED** | `TASK_INDEX_SEED_<PROYECTO>.md` | Datos para carga inicial VTT |
| **PLAN** | `PLAN_<TEMA>.md` | Vista de planificación operativa |
| **FASES_APLICABLES** | `FASES_APLICABLES_<PROYECTO>.md` | Filtro del catálogo SDLC |
| **WORKFLOW** | `WORKFLOW_<TEMA>_<PROYECTO>.md` | Cómo trabajar paso a paso |
| **ESTRUCTURA_REPO** | `ESTRUCTURA_REPO_<PROYECTO>.md` | Blueprint físico de carpetas |
| **OPERATIVO** | `OPERATIVO_<ROL>_<PROYECTO>.md` | Procedimiento operativo del rol |
| **CONTEXTO_*_SESION** | `CONTEXTO_<ROL>_SESION.md` | Estado live de sesión |
| **TEMPLATE** | `TEMPLATE_<TEMA>_V<X.Y>.md` | Plantilla reutilizable |
| **DEVLOG** | `YYYY-MM-DD_<TASK_ID>_<desc>.md` | Bitácora por tarea |
| **CODE_LOGIC** | `<archivo>.LOGIC.md` | Documenta la lógica de un archivo de código |
| **BRIEF** | `BRIEF_<DISC>_<SPRINT>_<TASK>_*.md` | Encargo a un agente |
| **ASSIGNMENT** | `ASSIGNMENT_<DISC>_<SPRINT>_<TASK>.md` | Asignación con detalle técnico |
| **.code-workspace** | `<rol>.code-workspace` | Configuración VS Code multi-root (NO es doc, es config) |
| **Script Python** | `*.py` | Ejecutable de carga / ops |
| **Script Bash** | `*.sh` | Ejecutable de setup |

### Ciclo de vida típico de un documento

```
BORRADOR (en proceso de redacción)
   ↓
LISTO PARA REVISIÓN (PM lo entrega)
   ↓
APROBADO (PM firma)
   ↓
FROZEN / CERRADO (no se reabre)
   ↓
OBSOLETO (reemplazado por nueva versión)
   ↓
ARCHIVADO (solo referencia histórica)
```

---

## 📍 UBICACIONES POR CARPETA

### `.claude/` (raíz del repo, configuración Claude Code)

| Carpeta | Qué contiene |
|---------|--------------|
| `agents/` | OPERATIVOs por rol — instrucciones operativas que Claude Code lee |
| `rules/` | Reglas del proyecto + datos (UUIDs reales, passwords) |

### `knowledge/` (documentación viva del proyecto)

| Carpeta | Qué contiene |
|---------|--------------|
| `agent-tasks/` | CONTEXTOs de sesión + planes operativos |
| `code-logic/` | `.LOGIC.md` por cada archivo de código (cuando arranque dev) |
| `development-log/` | Devlogs por tarea (cuando arranque dev) |

### `memory-service-project/Release2.0/01-PM/` (entregables del PM)

Documentos formales del PM: SPEC, METODOLOGIA, ADDENDUM, FASES_APLICABLES, PRE_HANDOFFs, CONSOLIDADO, CIERRE+HO, ADR, WORKFLOW, ESTRUCTURA_REPO.

### `memory-service-project/Release2.0/scripts/` (ejecutables)

| Subcarpeta | Qué contiene |
|------------|--------------|
| (raíz) | Scripts Python ejecutables (`create_memory_service_vtt.py`) + JSON output |
| `workspaces/` | 9 archivos `.code-workspace` por rol + README |

### `memory-service-project/Release2.0/Analisis/` (referencias estándar VTT)

Documentos genéricos del estándar VTT (no específicos del proyecto): metodologías, catálogos, procesos.

### `memory-service-project/Release2.0/PJM/` (entregables del PJM)

Documentos del PJM: HOs operativos, planes de sprint.

### `memory-service-project/00-agent-setup/` (estandarización del proyecto)

| Subcarpeta | Qué contiene |
|------------|--------------|
| `01.agent-setup/` | Setup inicial de agentes |
| `02.roles/` | Perfiles base de cada rol |
| `03.standard/` | Procesos estándar genéricos VTT (FLUJO_PM, FLUJO_PJM, etc.) |
| `04.Process/` | Procesos del proyecto (PM ANALISIS_INICIAL, PJM SETUP_PROYECTO, etc.) |
| `05.Templates/` | Templates reutilizables (con subcarpetas por tipo) |
| `06.Documentos_soporte/` | Lecciones aprendidas, add-ons |

---

## 🤔 PREGUNTAS FRECUENTES

### ¿Para qué creaste los archivos `.code-workspace`?

**No son documentos. Son configuración de VS Code.** Cuando abres uno con `code be.code-workspace`, VS Code abre una ventana con varios repos juntos en el mismo workspace, con permisos de write/read según tu rol.

**Sin ellos:** tendrías que abrir 4 carpetas manualmente cada vez. Y Claude Code no encontraría los OPERATIVOs porque viven en otro repo.

**Con ellos:** un comando, un workspace listo.

### ¿Cuál es la diferencia entre los `PRE_HANDOFF_*` y el `CIERRE_PM_HANDOFF_PJM`?

- **PRE_HANDOFF**: borradores temáticos. PRE_HANDOFF_INICIACION (24 tareas pre-SDLC) y PRE_HANDOFF_IMPLEMENTACION (66 tareas de código). **Son insumos** del PM para construir el HO final.
- **CIERRE_PM_HANDOFF_PJM**: el HO formal y consolidado. **Lo que recibe el PJM oficialmente**.

### ¿Cuál es la diferencia entre `CONSOLIDADO` y `CIERRE_PM_HANDOFF_PJM`?

- **CONSOLIDADO**: doc interno del PM, vista completa del plan (iniciación + fases + tareas). No tiene firmas ni gates de aprobación.
- **CIERRE_PM_HANDOFF_PJM**: doc formal con decisiones FROZEN, firmas, criterios de éxito. Es el "veredicto" del PM.

El CIERRE *consolida* el CONSOLIDADO con las partes formales agregadas.

### ¿Por qué hay `MEMORY_SERVICE_METODOLOGICO_v1.1` si está obsoleto?

Para **trazabilidad histórica**. Marcado como 🔴 OBSOLETO con aviso explícito. No se borra para que cualquiera entienda la evolución del análisis.

### ¿Cuál es la diferencia entre `OPERATIVO_<ROL>` y `CONTEXTO_<ROL>_SESION`?

- **OPERATIVO**: instrucciones permanentes — qué hago, comandos, SOPs. Casi nunca cambia.
- **CONTEXTO_SESION**: estado actual — qué tareas pendientes, decisiones recientes, escalaciones. Se actualiza al final de cada sesión.

### ¿Por qué tantos templates en `05.Templates/`?

Para **reproducir este proceso en cualquier proyecto futuro**. Memory Service es el caso piloto. Los 7 templates + INDEX significan que cualquier PM (humano o agente) puede arrancar otro proyecto siguiendo los mismos pasos sin reinventar la metodología.

### ¿Para qué sirve el `ADR-001`?

Es la **decisión arquitectural** de usar 4 repos en lugar de monorepo. Un ADR captura: contexto del problema, opciones consideradas, decisión, razones, consecuencias. **Sin ADR, las decisiones se olvidan** y el equipo termina cuestionando "¿por qué tenemos 4 repos?" en 3 meses.

### ¿Cuándo uso un BRIEF vs un ASSIGNMENT?

(Nota: aún no se generan en este proyecto, pero te respondo el patrón VTT)

- **BRIEF**: encargo conceptual de una tarea (qué hay que hacer, alcance). Lo crea el TL al planear el sprint.
- **ASSIGNMENT**: detalle técnico para que el agente ejecute (qué archivos tocar, qué APIs consumir, checklist). Lo crea el TL al asignar la tarea al agente.

---

## 🔄 FLUJO RECOMENDADO DE LECTURA SI ERES NUEVO

**Lectura mínima para entender el proyecto en 30 minutos:**

1. ⏱️ 5 min — Este índice (estás aquí)
2. ⏱️ 5 min — [`PROJECT_MEMORY.md`](knowledge/PROJECT_MEMORY.md)
3. ⏱️ 10 min — [`CIERRE_PM_HANDOFF_PJM_MEMORY_SERVICE_R1.md`](memory-service-project/Release2.0/01-PM/CIERRE_PM_HANDOFF_PJM_MEMORY_SERVICE_R1.md) (skim — tablas de §6 y §15)
4. ⏱️ 5 min — [`ADR-001_estrategia_repositorios.md`](memory-service-project/Release2.0/01-PM/ADR-001_estrategia_repositorios.md) (entender por qué 4 repos)
5. ⏱️ 5 min — [`WORKFLOW_OPERATIVO_MULTIREPO_MEMORY_SERVICE.md`](memory-service-project/Release2.0/01-PM/WORKFLOW_OPERATIVO_MULTIREPO_MEMORY_SERVICE.md) (cómo trabajar)

**Lectura profunda según tu rol:**

- **Vas a programar (BE/DB/FE):** → leer `SPEC_v1.9` completo
- **Vas a coordinar (PJM):** → leer `HO_PJM_CARGA_VTT` + `TASK_INDEX_SEED`
- **Vas a hacer Discovery o Planning (SA, PM):** → leer `FASES_APLICABLES` + `CONSOLIDADO §3.1-3.3`
- **Vas a hacer Diseño (DL, UX):** → leer `CONSOLIDADO §3.4` + cuando exista, los wireframes de MEM-029..038

---

## 🆘 SI TODAVÍA ESTÁS PERDIDO

1. Identifica **qué necesitas hacer** (ej: "voy a programar el endpoint /import")
2. Busca el **caso de uso** en este índice (ej: CASO 1 + 2)
3. Lee los 2-3 docs sugeridos
4. Si necesitas algo más, **pregúntale al PM**

---

**Documento:** INDICE_MAESTRO_DOCUMENTOS.md
**Versión:** 1.0
**Estado:** ✅ Vivo — actualizar cuando se agreguen docs nuevos

---

**PM — Martin Rivas**
