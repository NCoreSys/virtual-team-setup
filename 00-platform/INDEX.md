# 00-platform — Índice de archivos

| Campo | Valor |
|---|---|
| **Versión** | 1.0 |
| **Fecha** | 2026-05-17 |
| **Total archivos** | 317 (.md/.json/.py/.zip) |
| **Propósito** | Catálogo navegable de todos los archivos de la plataforma — qué es cada uno y dónde está |

> **Cómo usar este índice:** busca por Ctrl+F el nombre del archivo o concepto que buscas. La estructura conceptual (qué es cada entidad) está en `README.md`.

---

## 1. `01.agents/` — Todo sobre agentes (97 archivos)

### 1.1 `01.agents/roles/` — Perfiles base por rol (57 archivos)

#### Perfiles individuales (25 archivos)

| Archivo | Rol | Función |
|---|---|---|
| `AGENT_PROFILE_BASE_AR.md` | Architect | Perfil base del rol Solution Architect |
| `AGENT_PROFILE_BASE_BE.md` | Backend Engineer | Perfil base del rol BE |
| `AGENT_PROFILE_BASE_CIA.md` | Competitive Intelligence Analyst | Perfil base CIA |
| `AGENT_PROFILE_BASE_DB.md` | Database Engineer | Perfil base DB |
| `AGENT_PROFILE_BASE_DL.md` | Design Lead | Perfil base DL |
| `AGENT_PROFILE_BASE_DO.md` | DevOps | Perfil base DO |
| `AGENT_PROFILE_BASE_FA.md` | Functional Analyst | Perfil base FA |
| `AGENT_PROFILE_BASE_FE.md` | Frontend Developer | Perfil base FE |
| `AGENT_PROFILE_BASE_MRA.md` | Market Research Analyst | Perfil base MRA |
| `AGENT_PROFILE_BASE_PJM.md` | Project Manager | Perfil base PJM |
| `AGENT_PROFILE_BASE_PM.md` | Product Manager | Perfil base PM |
| `AGENT_PROFILE_BASE_PM_REVISOR.md` | PM Revisor | Variante PM para revisión |
| `AGENT_PROFILE_BASE_PROJECT_SETUP.md` | Project Setup Agent | Especialista en setup inicial |
| `AGENT_PROFILE_BASE_PSA.md` | Product Strategy Analyst | Perfil base PSA |
| `AGENT_PROFILE_BASE_PTE.md` | Penetration Tester | Perfil base PTE (security) |
| `AGENT_PROFILE_BASE_QA.md` | QA Engineer | Perfil base QA |
| `AGENT_PROFILE_BASE_QAA.md` | QA Automation | Variante QA automation |
| `AGENT_PROFILE_BASE_QAE.md` | QA Engineer (variant) | Variante QA |
| `AGENT_PROFILE_BASE_SA.md` | Systems Analyst | Perfil base SA |
| `AGENT_PROFILE_BASE_SA_REVIEWER.md` | SA Revisor | SA para revisión |
| `AGENT_PROFILE_BASE_SEC.md` | Security Engineer | Perfil base SEC |
| `AGENT_PROFILE_BASE_SRE.md` | SRE | Site Reliability Engineer |
| `AGENT_PROFILE_BASE_TL.md` | Tech Lead | Perfil base TL |
| `AGENT_PROFILE_BASE_TW.md` | Technical Writer | Perfil base TW |
| `AGENT_PROFILE_BASE_UI.md` | UI Designer | Perfil base UI |
| `AGENT_PROFILE_BASE_UX.md` | UX Designer | Perfil base UX |
| `AGENT_PROFILE_BASE_UXR.md` | UX Researcher | Perfil base UXR |
| `AGENTES_MEMORY_SERVICE.md` | — | Catálogo de UUIDs y emails del equipo Memory Service |

#### `01.agents/roles/templates/` — Templates base por rol (29 archivos)

| Archivo | Función |
|---|---|
| `TEMPLATE_BASE_AR.md` | Template base perfil AR |
| `TEMPLATE_BASE_BE.md` | Template base perfil BE |
| `TEMPLATE_BASE_DB.md` | Template base perfil DB |
| `TEMPLATE_BASE_DL_EJECUTOR.md` | Template DL (modo ejecutor) |
| `TEMPLATE_BASE_DL_REVISOR.md` | Template DL (modo revisor) |
| `TEMPLATE_BASE_DO.md` | Template base perfil DO |
| `TEMPLATE_BASE_FE.md` | Template base perfil FE |
| `TEMPLATE_BASE_PJM.md` | Template base perfil PJM |
| `TEMPLATE_BASE_PJM_PM_SETUP.md` | Template PJM/PM combinado para setup |
| `TEMPLATE_BASE_PM.md` | Template base perfil PM |
| `TEMPLATE_BASE_PM_REVISOR.md` | Template PM (modo revisor) |
| `TEMPLATE_BASE_PROJECT_SETUP.md` | Template setup de proyecto |
| `TEMPLATE_BASE_QA.md` | Template base perfil QA |
| `TEMPLATE_BASE_SA.md` | Template base perfil SA |
| `TEMPLATE_BASE_TL_EJECUTOR.md` | Template TL (modo ejecutor) |
| `TEMPLATE_BASE_TL_GENERICO.md` | Template TL genérico (ejecutor + revisor) |
| `TEMPLATE_BASE_TL_REVISOR.md` | Template TL (modo revisor) |
| `TEMPLATE_BASE_UX.md` | Template base perfil UX |
| `_old_OPERATIVO_*_TEMPLATE.md` (11) | Templates legacy de OPERATIVOS por rol (AR, BE, DB, DL, DO, FE, PJM, PM, QA, SA, UX) — uso descontinuado |

### 1.2 `01.agents/setups/` — Configs iniciales por rol (11 archivos)

| Archivo | Rol |
|---|---|
| `SETUP_BE.md` | Backend Engineer |
| `SETUP_DB.md` | Database Engineer |
| `SETUP_DL.md` | Design Lead |
| `SETUP_DO.md` | DevOps |
| `SETUP_PJM.md` | Project Manager |
| `SETUP_PM.md` | Product Manager |
| `SETUP_SA.md` | Systems Analyst |
| `SETUP_SA_REVIEWER.md` | SA Revisor |
| `SETUP_SETUP.md` | Setup Agent (meta) |
| `SETUP_TL.md` | Tech Lead |
| `SETUP_TL_REVIEWER.md` | Tech Lead Revisor |

### 1.3 `01.agents/onboarding/` — Cómo arranca un agente (2 archivos)

| Archivo | Función |
|---|---|
| `01_ONBOARDING.md` | Guía de onboarding general para cualquier agente nuevo |
| `02_OPERACION_AGENTE.md` | Operación día a día del agente |

### 1.4 `01.agents/operativos-templates/` — Plantillas operativos (0 archivos)

Vacía. Los templates `OPERATIVO_*_TEMPLATE.md` antiguos están en `roles/templates/_old_*`.

### 1.5 `01.agents/init-messages/` — Mensajes iniciales por rol (15 archivos)

| Archivo | Rol |
|---|---|
| `INIT_AR.md` | Architect |
| `INIT_BE.md` | Backend Engineer |
| `INIT_DB.md` | Database Engineer |
| `INIT_DL.md` | Design Lead |
| `INIT_DO.md` | DevOps |
| `INIT_FE.md` | Frontend Developer |
| `INIT_PJM.md` | Project Manager |
| `INIT_PM.md` | Product Manager |
| `INIT_QA.md` | QA Engineer |
| `INIT_SA.md` | Systems Analyst |
| `INIT_SA_REVIEWER.md` | SA Revisor |
| `INIT_SETUP.md` | Setup Agent |
| `INIT_TL_EXECUTOR.md` | TL Ejecutor |
| `INIT_TL_REVIEWER.md` | TL Revisor |
| `INIT_UX.md` | UX Designer |

### 1.6 `01.agents/kits/` — Kits empaquetados por rol (12 archivos)

| Archivo | Tipo | Contenido |
|---|---|---|
| `KIT_AR.zip` | ZIP | Kit completo Architect |
| `KIT_DL.zip` | ZIP | Kit completo Design Lead |
| `KIT_PJM.zip` | ZIP | Kit completo PJM |
| `KIT_PM.zip` | ZIP | Kit completo PM |
| `KIT_SA_EJECUTOR.zip` | ZIP | Kit SA ejecutor |
| `KIT_SA_REVIEWER.zip` | ZIP | Kit SA revisor |
| `KIT_SETUP.zip` | ZIP | Kit Setup Agent |
| `KIT_TL_REVIEWER.zip` | ZIP | Kit TL revisor |
| `KIT_UX.zip` | ZIP | Kit UX |
| `SETUP_AR.md` | MD | Instrucciones setup AR (auxiliar de KIT) |
| `SETUP_DL.md` | MD | Instrucciones setup DL |
| `SETUP_UX.md` | MD | Instrucciones setup UX |

---

## 2. `02.normativa/` — Normativa operativa (130 archivos)

### 2.1 Raíz de normativa (2 archivos)

| Archivo | Función |
|---|---|
| `README.md` | **GUÍA NORMATIVA VTT** — Modelo de 4 niveles + Nivel 0 Rules. Documento conceptual maestro |
| `INVENTARIO.md` | Inventario maestro con tabla de equivalencias legacy → paths actuales |

### 2.2 `02.normativa/00.Rules/` — Nivel 0 (11 archivos)

| Archivo | Tipo | Función |
|---|---|---|
| `README.md` | MD | Sistema de Reglas VTT — modelo 8 niveles scope + 4 actor types + 7 markers |
| `rules_catalog.json` | JSON | **47 reglas activas** validadas — el catálogo maestro |
| `capabilities_catalog.json` | JSON | 30 capabilities de doc_sec_02 (RBAC base) |
| `roles_catalog.json` | JSON | 9 roles + matriz RBAC completa |
| `rules_schema.json` | JSON | JSON Schema validador de rules_catalog |
| `query_rules.py` | Python | Motor de filtros: `--validate`, `--list`, `--simulate-task`, `--context-json` |

#### `02.normativa/00.Rules/sources/` — Fuentes originales (5 archivos)

| Archivo | Origen | Reglas extraídas |
|---|---|---|
| `AGENT_RULES_Rev.md` | `03.standard/09.AGENT_RULES_Rev.md` | 15 reglas operativas (RULE-WORKFLOW, RULE-CODE, RULE-DOC, RULE-API, RULE-GIT, RULE-DATA, RULE-FORBID) |
| `doc_sec_01_modelo_seguridad_actores_scopes.md` | RCBA | Actores, recursos, jerarquía Platform→Org→Workspace→Resource |
| `doc_sec_02_politicas_permisos_rbac_abac.md` | RCBA | 17 reglas ABAC + SoD (DEV-01..AG-03, CR-01..03) |
| `doc_sec_03_arquitectura_implementacion_autorizacion.md` | RCBA | Middleware authenticate/resolveAuthorizationContext/requireCapability/requirePolicy |
| `doc_sec_04_matriz_autorizacion.md` | RCBA | Matriz RBAC capability×rol completa |

### 2.3 `02.normativa/01.Protocols/` — Nivel 4 (22 archivos)

#### Protocols VTT migrados (1 archivo)

| Archivo | Función | Versión |
|---|---|---|
| `VTT.PROTOCOL-ASG-001_ciclo_asignacion_tarea.md` | Ciclo completo de asignación y cierre de tarea (16 pasos, 24 Workflows derivados) | v1.2.0 |

#### `_pending-migration/` — Protocols legacy pendientes de convertir (21 archivos)

| Archivo | Origen / Tipo | Migración propuesta |
|---|---|---|
| `01_PM_PROCESO_ANALISIS_INICIAL.md` | PM | `VTT.PROTOCOL-ANL-001` |
| `02.PJM_PROCESO_SETUP_PROYECTO_VTT.md` | PJM | `VTT.PROTOCOL-SETUP-001` |
| `03_FLUJO_TL.md` | TL | `VTT.PROTOCOL-FLUJO-TL-001` |
| `06_FLUJO_DL.md` | DL | `VTT.PROTOCOL-FLUJO-DL-001` |
| `07_FLUJO_PJM.md` | PJM | `VTT.PROTOCOL-FLUJO-PJM-001` |
| `08_FLUJO_PM.md` | PM | `VTT.PROTOCOL-FLUJO-PM-001` |
| `10_FLUJO_SA_REVIEWER.md` | SA Reviewer | `VTT.PROTOCOL-FLUJO-SA-001` |
| `11_GUIA_AGENTES_MODELO_DINAMICO_V4.md` | Modelo Dinámico V4 | `VTT.PROTOCOL-MODDIN-001` |
| `CIERRE_PM_HANDOFF_PJM_MODELO_DINAMICO_V4.2.md` | Cierre PM → PJM | `VTT.PROTOCOL-HO-001` |
| `HANDOFF_PJM_ADDENDUM_V4.5.md` | Addendum HO PJM | Anexo del HO-001 |
| `METODOLOGIA_TRABAJO_PM_VTT.md` | PM methodology | `VTT.PROTOCOL-PM-METH-001` |
| `PROCESO_ASIGNACION_TAREAS.md` | v1.6 legacy | reemplazado por v3 (también pending) |
| `PROCESO_ASIGNACION_TAREAS_v3.md` v3.1 | Asignación TL | `VTT.PROTOCOL-ASG-001` (✅ migrado) |
| `PROCESO_CIERRE_TAREA_v2.md` v2.1 | Cierre TL Reviewer | `VTT.PROTOCOL-ASG-001` (✅ migrado) |
| `SETUP_PROCESS_PM.md` | Setup PM | `VTT.PROTOCOL-SETUP-PM-001` |
| `SOP-EST-01_technical_estimates.md` | Estimación técnica | `VTT.PROTOCOL-EST-001` |
| `SOP-LD-01_living_documents.md` | Living Documents | `VTT.PROTOCOL-LD-001` |
| `SOP-RET-01_retrospective_analysis.md` | Retrospectiva | `VTT.PROTOCOL-RET-001` |
| `SOP-TRK-01_trackable_items_workflow.md` | TIs workflow | `VTT.PROTOCOL-TRK-001` |
| `SOP-TRK-02_dynamic_item_creation.md` | TIs dinámicos | `VTT.PROTOCOL-TRK-002` |
| `SOP-VEL-01_velocity_methodology.md` | Velocity | `VTT.PROTOCOL-VEL-001` |

### 2.4 `02.normativa/02.Workflows/` — Nivel 3 (vacía)

Pendiente: escribir los 24 Workflows derivados del PROTOCOL-ASG-001 v1.2.0 (WF-ASG-001.001 a WF-ASG-001.024).

### 2.5 `02.normativa/03.Skills/` — Nivel 2 (34 archivos en `_pending-migration/`)

#### `_pending-migration/` — Skills legacy del catálogo Memory Service

| Archivo | Categoría | Función |
|---|---|---|
| `CATALOGO_SKILLS_MEMORY_SERVICE.md` | Catálogo legacy | Reemplazado por sistema de niveles VTT |
| `auth/SKL-AUTH-01_obtener-jwt.md` | AUTH | Obtener JWT VTT |
| `file-structure/SKL-STRUCTURE-01_ubicar-entregable.md` | FILES | Ubicar entregable en repo |
| `git-ops/SKL-GIT-01_crear-branch.md` | GIT | Crear branch feature/ |
| `git-ops/SKL-GIT-02_rebase-main.md` | GIT | Rebase con main |
| `git-ops/SKL-GIT-03_commit-formato.md` | GIT | Formato commits + Co-Authored-By |
| `git-ops/SKL-GIT-04_crear-pr.md` | GIT | Crear PR con gh |
| `manifest/SKL-MANIFEST-01_generar-manifest.md` | MANIFEST | Generar manifest v1.0 (agente) y v1.5 (TL) |
| `report/SKL-REPORT-01_entrega-tarea.md` | REPORT | Reporte de entrega del agente |
| `report/SKL-REPORT-02_reporte-pjm.md` | REPORT | Reporte ejecutivo PJM |
| `vtt-attach/SKL-ATTACH-01_subir-archivo.md` | VTT | Subir archivo a tarea |
| `vtt-attach/SKL-ATTACH-02_subir-devlog.md` | VTT | Subir devlog como attachment |
| `vtt-task/SKL-TASK-01_crear-tarea.md` | VTT | Crear tarea VTT |
| `vtt-task/SKL-TASK-02_generar-assignment.md` | VTT | Generar ASSIGNMENT |
| `vtt-task/SKL-TASK-03_asignar-tarea.md` | VTT | Asignar tarea a agente |
| `vtt-task/SKL-TASK-04_mensaje-agente.md` | VTT | Mensaje al agente |
| `vtt-task/SKL-TASK-05_review-tarea.md` | VTT | Review de tarea |
| `vtt-task/SKL-STATUS-01..06_*.md` | VTT | 6 transitions de status |
| `vtt-task/SKL-QUERY-01..05_*.md` | VTT | 5 queries (mis tareas, en review, detalle, avance, asignable) |
| `vtt-task/SKL-COMMENT-01..03_*.md` | VTT | Comments (genérico, APR-PM, APR-TL) |
| `vtt-task/SKL-DEVLOG-01..02_*.md` | VTT | Devlog (decision, observación) |
| `vtt-task/SKL-ISSUE-01_crear-issue.md` | VTT | Crear issue |

### 2.6 `02.normativa/04.Scripts/` — Nivel 1 (vacía)

Pendiente: extraer scripts atómicos referenciados por Skills (`POST /attachments`, `PATCH /status`, etc.).

### 2.7 `02.normativa/05.Flowcharts/` — Diagramas (vacía)

Pendiente: diagramas mermaid de los Protocols.

### 2.8 `02.normativa/06.Improvements/` — Mejoras propuestas (7 archivos)

| Archivo | Categoría | Estimación | Estado |
|---|---|---|---|
| `README.md` | — | — | Índice de mejoras |
| `IMPROVE-001_pool_transacciones_vtt.md` | Infrastructure | 10 días | Propuesta |
| `IMPROVE-002_bd_manifiestos_y_tis.md` | Database/Reporting | 6-8 días | Propuesta |
| `IMPROVE-003_platform_gaps_backend_vtt.md` | Backend gaps | 2 días | Propuesta |
| `IMPROVE-004_rules_como_feature_vtt.md` | Authorization | 15 días | Propuesta |
| `IMPROVE-005_extension_recursos_vtt_especificos.md` | Authorization | 7 días | Propuesta (depende 004) |
| `IMPROVE-006_gotchas_api_assignee_y_order_deliveries.md` | API gotchas | — | Propuesta |

### 2.9 `02.normativa/catalogs/` — Datos de referencia (54 archivos)

#### Catalogs raíz (4 archivos)

| Archivo | Función |
|---|---|
| `04_ESTRUCTURA_FASES.md` | Estructura de fases del SDLC VTT |
| `05_CATALOGO_DELIVERABLES.md` | Catálogo de deliverables del SDLC |
| `ANALISIS_FASES_COMPLETO_PARA_PM.md` | Análisis de fases para el PM (438 deliverables) |
| `ESTRUCTURA_FASES_DESARROLLO_PROYECTOS_V3.1.md` | Estructura de fases v3.1 |

#### `catalogs/deliverables/` — Diccionarios SDLC (50 archivos)

50 diccionarios `DICCIONARIO_FASE_*.md` cubriendo las 9 fases del SDLC (00 Discovery a 07 Operations) + utilidades:

| Tipo | Conteo | Detalle |
|---|---|---|
| Diccionarios por subfase | 43 | DICCIONARIO_FASE_00 a 07 (todos los deliverables del SDLC) |
| `deliverables_catalog.json` | 1 | Catálogo JSON con 438 deliverables estructurados |
| `extract_deliverables_to_json.py` | 1 | Script de extracción .md → JSON |
| `generate_pjm_handoff_from_catalog.py` | 1 | Script de generación HO PJM |
| `ESTRATEGIA_GENERACION_TEMPLATES_SDLC.md` | 1 | Estrategia de templates |
| `HO_PJM_CONFIGURACION_DELIVERABLES_SDLC.md` | 1 | Configuración deliverables HO PJM |
| `PROMPT_CONTINUACION_DICCIONARIO.md` | 1 | Prompt template |
| `SOP_GENERACION_TEMPLATES_SDLC.md` | 1 | SOP generación de templates |

---

## 3. `03.templates/` — Templates genéricos (58 archivos)

### 3.1 `03.templates/tarea/` — Templates de tarea (10 archivos)

| Archivo | Función |
|---|---|
| `TEMPLATE_BRIEF_LARGE.md` | Plantilla BRIEF — diseño original de tarea |
| `TEMPLATE_ASIGNACION_TAREARev.md` v3.1 | Plantilla ASSIGNMENT — instrucciones al agente |
| `TEMPLATE_DEVELOPMENT_LOG.md` | Plantilla devlog en .md (archivo en `knowledge/development-log/`) |
| `TEMPLATE_DEVLOG.md` | Plantilla devlog entries en VTT (otro formato) |
| `TEMPLATE_CODE_LOGIC_ACTUALIZADO.md` | Plantilla `.LOGIC.md` por archivo de código |
| `TEMPLATE_HANDOFF.md` | Plantilla HO genérico |
| `TEMPLATE_ISSUE.md` | Plantilla de issue en VTT |
| `TEMPLATE_MENSAJE_ASIGNACION.md` | Plantilla mensaje al agente (legacy — uso `gen_mensaje.py`) |
| `GUIA_USO_TEMPLATES.md` | Manual de uso de templates |
| `METODOLOGIA_EJECUCION_SPRINTS_V1.md` | Metodología de ejecución de sprints |

### 3.2 `03.templates/handoff/` — Handoffs y metodologías (13 archivos)

| Archivo | Función |
|---|---|
| `TEMPLATE_HANDOFF_TL_V2.1.md` | HO PJM → TL (v2.1) — el principal |
| `TEMPLATE_HANDOFF_DL_V1.1.md` | HO TL → DL (legacy — proceso corto) |
| `TEMPLATE_HANDOFF_FE_V1.1.md` | HO TL → FE (legacy) |
| `TEMPLATE_HANDOFF_QA_V1.1.md` | HO TL → QA (legacy) |
| `TEMPLATE_DEVLOG_V1.1.md` | Devlog v1.1 |
| `METODOLOGIA_SETUP_FASE.md` | Setup de fase |
| `METODOLOGIA_SETUP_PLAN_VTT.md` | Planificación VTT (grafo dependencias) |
| `METODOLOGIA_SETUP_PROYECTOS_VTT.md` | Setup de proyectos VTT |
| `METODOLOGIA_EJECUCION_SPRINTS_V1.1.md` | Ejecución de sprints v1.1 |
| `METODOLOGIA_CIERRE_SPRINT_FASE.md` | Cierre de sprint/fase |
| `CODE_REVIEW_GUIDE_V1.1.md` | Guía code review TL |
| `INTEGRATION_AUDIT_CHECKLIST_V1.1.md` | Checklist integración AR |
| `TESTING_GUIDE_V1.1.md` | Guía testing QA |

### 3.3 `03.templates/normativa/` — Templates de salidas operativas (3 archivos)

| Archivo | Función |
|---|---|
| `VTT.TEMPLATE-CLO-001_closure_sprint.md` | Template de CLOSURE de sprint con firmas API |
| `VTT.TEMPLATE-CFL-001_criteria_fulfillment.md` | Template de cumplimiento de CAs por el agente |
| `VTT.TEMPLATE-APR-001_apr_tl_comment.md` | Template APR-TL comment al cerrar tarea |

### 3.4 `03.templates/memoria/` — Memoria del agente (1 archivo)

| Archivo | Función |
|---|---|
| `MEMORY_TEMPLATE.md` | Template para memoria persistente del agente |

### 3.5 `03.templates/contexto/` — Contexto de sesión (4 archivos)

| Archivo | Rol |
|---|---|
| `CONTEXTO_DL_SESION_TEMPLATE.md` | Design Lead |
| `CONTEXTO_PJM_SESION_TEMPLATE.md` | Project Manager |
| `CONTEXTO_PM_SESION_TEMPLATE.md` | Product Manager |
| `CONTEXTO_TL_SESION_TEMPLATE.md` | Tech Lead |

### 3.6 `03.templates/specs-design/` — Specs UI/UX (19 archivos)

12 templates de spec por tipo de pantalla + 5 auxiliares + 2 guías:

| Tipo | Archivos |
|---|---|
| Specs por tipo de pantalla | `TEMPLATE_BASE_Spec_*` (12): AdminRBAC, AppScreen, Checkout, ContentSEO, DashboardKPI, DataGrid, EntityDetail, Form, Landing, ModalOverlay, Notification, SemanticSearch, UXStates, Wizard |
| Catálogo + índice | `catalogo_maestro_templates_specs_uiux_v2.md`, `index_templates_specs_v2.md`, `README_base_conocimiento_templates_specs_v2.md` |
| Spec base | `template_base_especificacion_funcional_uiux.md` |
| Tokens | `GUIA_Design_Tokens_Checklist.md` |

### 3.7 `03.templates/setup-vtt/01_PM/` — Setup de proyecto VTT (8 archivos)

| Archivo | Función |
|---|---|
| `INDEX_TEMPLATES_CIERRE_PM_HANDOFF_PJM.md` | Índice de templates de cierre |
| `TEMPLATE_CIERRE_PM_HANDOFF_PJM_V1.0.md` | Cierre PM → PJM |
| `TEMPLATE_CONSOLIDADO_V1.0.md` | Doc consolidado de fase |
| `TEMPLATE_FASES_APLICABLES_V1.0.md` | Fases aplicables al proyecto |
| `TEMPLATE_HO_PJM_CARGA_VTT_V1.0.md` | HO PJM con carga VTT |
| `TEMPLATE_PRE_HANDOFF_INICIACION_V1.0.md` | Pre-HO de iniciación |
| `TEMPLATE_TASK_INDEX_SEED_V1.0.md` | Seed inicial de tareas |
| `TEMPLATE_create_vtt_script_V1.0.py` | Script template para crear setup VTT |

---

## 4. `04.docs-soporte/` — Documentación complementaria (8 archivos)

### 4.1 `04.docs-soporte/guias-operativas/` — Guías operativas (5 archivos)

| Archivo | Versión | Función |
|---|---|---|
| `GUIA_WORKTREES_MEMORY_SERVICE.md` | v2.1 | Worktrees por rol (modelo actual) — TODOS los roles |
| `GUIA_GIT_WORKTREES_TL_BACKEND.md` | v2.0 (LEGACY) | Worktrees por tarea — reemplazado por v2.1 |
| `GUIA_ASIGNACION_TAREA_TL_EJECUTOR.md` | v2.1 | Cheatsheet del TL al asignar — Paso 8.5 (execution_manifest) |
| `GUIA_REVISION_TAREA_TL_REVIEWER.md` | v2.1 | Cheatsheet del TL al cerrar — Paso 5b + Paso 16 |
| `GUIA_MANIFEST_PARA_AGENTES.md` | v2.0 | Manifest v1.0 generado por agente |

### 4.2 `04.docs-soporte/lecciones/` — Lecciones aprendidas (1 archivo)

| Archivo | Función |
|---|---|
| `ADDON_PASO0_ADR_REPOS_LECCION_APRENDIDA.md` | Lección: ADR sobre estructura de repos (multi-repo) |

### 4.3 `04.docs-soporte/legacy/` — Docs viejos (2 archivos)

| Archivo | Función |
|---|---|
| `00_INDEX.md` | Índice viejo del repo (de `03.standard/00_INDEX.md`) |
| `ONBOARDING_TECHLEAD_DESIGN_MINE.md` | Onboarding TL específico DesignMine (cuando entre el proyecto) |

---

## 5. `05.proyectos/memory-service/` — Instancias Memory Service (23 archivos)

### 5.1 Raíz (1 archivo)

| Archivo | Función |
|---|---|
| `Proyect_data.md` | UUIDs y emails del equipo Memory Service (TL, BE, DB, DO, etc.) |

### 5.2 `05.proyectos/memory-service/onboarding/` — Onboarding específico (2 archivos)

| Archivo | Para |
|---|---|
| `ONBOARDING_AGENTE_EJECUTOR_MEMORY_SERVICE.md` | Agente ejecutor (BE/DB/DO/FE/QA) |
| `ONBOARDING_TL_MEMORY_SERVICE.md` | TL del Memory Service |

### 5.3 `05.proyectos/memory-service/operativos-instancias/` — Operativos por rol con UUIDs reales (18 archivos)

| Archivo | Rol | UUID asignado |
|---|---|---|
| `OPERATIVO_AR_MEMORY-SERVICE.md` | Architect | (en archivo) |
| `OPERATIVO_BE_MEMORY-SERVICE.md` | Backend Engineer | `ebbe3cee-…` |
| `OPERATIVO_DB_MEMORY-SERVICE.md` | Database Engineer | `6fae26f0-…` |
| `OPERATIVO_DL_MEMORY-SERVICE.md` | Design Lead | `b3a09269-…` |
| `OPERATIVO_DO_MEMORY-SERVICE.md` | DevOps | `322e3745-…` |
| `OPERATIVO_FE_MEMORY-SERVICE.md` | Frontend Developer | `d23c9cd9-…` |
| `OPERATIVO_PJM_MEMORY-SERVICE.md` | Project Manager (variante 1) | (en archivo) |
| `OPERATIVO_PJM_MEMORY_SERVICE.md` | PJM (variante 2 con underscore) | DUPLICADO — consolidar |
| `OPERATIVO_PM_MEMORY-SERVICE.md` | Product Manager | (en archivo) |
| `OPERATIVO_QA_MEMORY-SERVICE.md` | QA Engineer | `613c9538-…` |
| `OPERATIVO_SA_MEMORY-SERVICE.md` | Solution Analyst | `0c128e3b-…` |
| `OPERATIVO_SA_REVIEWER.md` | SA Revisor | (en archivo) |
| `OPERATIVO_SETUP_MEMORY-SERVICE.md` | Setup Agent | (en archivo) |
| `OPERATIVO_TECH_LEAD.md` | TL legacy | DUPLICADO con TL_MEMORY-SERVICE |
| `OPERATIVO_TL_EXECUTOR.md` | TL Ejecutor | (separado de revisor) |
| `OPERATIVO_TL_MEMORY-SERVICE.md` | TL (unificado) | `92225290-…` |
| `OPERATIVO_TL_REVIEWER.md` | TL Revisor | (separado de ejecutor) |
| `OPERATIVO_UX_MEMORY-SERVICE.md` | UX Designer | `a75a1dae-…` |

> **TODOs detectados:** consolidar `OPERATIVO_PJM_MEMORY-SERVICE.md` vs `OPERATIVO_PJM_MEMORY_SERVICE.md` (diff: `-` vs `_`). Resolver `OPERATIVO_TECH_LEAD.md` vs `OPERATIVO_TL_MEMORY-SERVICE.md`.

### 5.4 `05.proyectos/memory-service/templates-proyecto/` — Templates específicos (0 archivos)

Vacía. Si Memory Service necesita templates propios (ej. variantes de BRIEF con campos específicos), van aquí.

### 5.5 `05.proyectos/memory-service/living-documents/` — Living Documents (1 archivo)

| Archivo | Función |
|---|---|
| `LIVING_DOCUMENTS_MEMORY_SERVICE.md` | Catálogo de Living Documents del proyecto (LD-01 a LD-15) |

### 5.6 `05.proyectos/memory-service/setup-proyecto/` — Setup específico (1 archivo)

| Archivo | Función |
|---|---|
| `SETUP_HETZNER_COMPARTIDO.md` | Setup del servidor compartido Hetzner |

---

## 6. Búsqueda rápida — Por concepto

| Si buscas... | Ve a... |
|---|---|
| Reglas que aplican a una tarea | `02.normativa/00.Rules/` → `query_rules.py --simulate-task <ID>` |
| Cómo se asigna y cierra una tarea | `02.normativa/01.Protocols/VTT.PROTOCOL-ASG-001_*.md` |
| Modelo Dinámico V4 (devlog, evidencias, manifests) | `02.normativa/01.Protocols/_pending-migration/11_GUIA_AGENTES_MODELO_DINAMICO_V4.md` |
| Living Documents (concepto general) | `02.normativa/01.Protocols/_pending-migration/SOP-LD-01_*.md` |
| Living Documents (catálogo Memory Service) | `05.proyectos/memory-service/living-documents/` |
| TrackableItems (workflow) | `02.normativa/01.Protocols/_pending-migration/SOP-TRK-01_*.md` |
| Estimación técnica de tareas | `02.normativa/01.Protocols/_pending-migration/SOP-EST-01_*.md` |
| Velocity del equipo | `02.normativa/01.Protocols/_pending-migration/SOP-VEL-01_*.md` |
| Retrospectiva de fase/sprint | `02.normativa/01.Protocols/_pending-migration/SOP-RET-01_*.md` |
| Worktrees por rol (operación día a día) | `04.docs-soporte/guias-operativas/GUIA_WORKTREES_MEMORY_SERVICE.md` |
| Generar HO PJM → TL | `03.templates/handoff/TEMPLATE_HANDOFF_TL_V2.1.md` |
| Generar BRIEF de tarea | `03.templates/tarea/TEMPLATE_BRIEF_LARGE.md` |
| Generar ASSIGNMENT de tarea | `03.templates/tarea/TEMPLATE_ASIGNACION_TAREARev.md` |
| Generar `.LOGIC.md` | `03.templates/tarea/TEMPLATE_CODE_LOGIC_ACTUALIZADO.md` |
| Onboarding agente nuevo | `01.agents/onboarding/01_ONBOARDING.md` + perfil base + setup |
| UUIDs del equipo Memory Service | `05.proyectos/memory-service/Proyect_data.md` o `01.agents/roles/AGENTES_MEMORY_SERVICE.md` |
| Catálogo de 438 deliverables SDLC | `02.normativa/catalogs/deliverables/deliverables_catalog.json` |
| Diccionario de una fase específica | `02.normativa/catalogs/deliverables/DICCIONARIO_FASE_<NN>_*.md` |
| Proponer mejora a la plataforma | `02.normativa/06.Improvements/` |
| Setup de proyecto VTT (cuando entra cliente nuevo) | `03.templates/setup-vtt/01_PM/` |
| Spec de UI/UX para nueva pantalla | `03.templates/specs-design/` |
| Code review (criterios TL) | `03.templates/handoff/CODE_REVIEW_GUIDE_V1.1.md` |
| Integration audit (criterios AR) | `03.templates/handoff/INTEGRATION_AUDIT_CHECKLIST_V1.1.md` |
| Testing guide (criterios QA) | `03.templates/handoff/TESTING_GUIDE_V1.1.md` |

---

## 7. Estadísticas

| Entidad | Archivos | % |
|---|---|---|
| `01.agents/` | 97 | 31% |
| `02.normativa/` | 130 | 41% |
| `03.templates/` | 58 | 18% |
| `04.docs-soporte/` | 8 | 3% |
| `05.proyectos/` | 23 | 7% |
| **Total** | **316** + README + INDEX = **318** | 100% |

### Por tipo de archivo

| Tipo | Conteo |
|---|---|
| `.md` | 296 |
| `.json` | 6 |
| `.py` | 3 |
| `.zip` | 9 |
| **Total** | **314** + INDEX/README = **316** |

### Por estado

| Estado | Conteo | Detalle |
|---|---|---|
| Activos | 247 | Documentos en uso operativo |
| `_pending-migration/` | 55 | 21 SOPs + 34 Skills legacy pendientes de convertir a formato VTT |
| Legacy útiles | 2 | `00_INDEX.md`, `ONBOARDING_TECHLEAD_DESIGN_MINE.md` |
| Legacy obsoletos en `roles/templates/_old_*` | 11 | OPERATIVO_*_TEMPLATE.md viejos |

---

## 8. Changelog

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-05-17 | Versión inicial del INDEX. Refleja la reorganización en 5 entidades + renombre a `00-platform/`. 317 archivos catalogados con descripción individual. |
