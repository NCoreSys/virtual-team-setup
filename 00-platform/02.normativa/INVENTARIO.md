# Inventario Maestro de Documentos VTT

| Campo | Valor |
|---|---|
| **Versión** | 1.0 |
| **Fecha** | 2026-05-13 |
| **Mantenedor** | PM Martin Rivas |
| **Frecuencia de revisión** | Al cierre de cada sprint o cuando se agregue/depreque documento |
| **Source of Truth** | `virtual-teams-setup/00-platform/` |
| **Proyectos espejo** | `memory-service/memory-service-project/00-platform/`, `memory-service/memory-service-backend/` |

---

## ⚠️ AVISO DE REORGANIZACIÓN (2026-05-17)

El repo `00-platform/` fue **reorganizado en 5 entidades**:

```
00-platform/
├── 01.agents/                    (roles, setups, onboarding, init-messages, kits, operativos-templates)
├── 02.normativa/                 (Rules, Protocols, Workflows, Skills, Scripts, Improvements, catalogs)
├── 03.templates/                 (tarea, handoff, normativa, memoria, contexto, specs-design, setup-vtt)
├── 04.docs-soporte/              (guias-operativas, lecciones, legacy)
└── 05.proyectos/memory-service/  (instancias específicas Memory Service)
```

**Las referencias en el cuerpo de este inventario usan paths LEGACY**. Equivalencias:

| Path legacy | Path actual |
|---|---|
| `07.Normativa/` | `02.normativa/` |
| `07.Normativa/00.Rules/` | `02.normativa/00.Rules/` |
| `07.Normativa/01.Protocols/` | `02.normativa/01.Protocols/` |
| `07.Normativa/IMPROVEMENTS/` | `02.normativa/06.Improvements/` |
| `07.Normativa/06.Templates/` | `03.templates/normativa/` |
| `06.Documentos_soporte/GUIA_*` | `04.docs-soporte/guias-operativas/` |
| `06.Documentos_soporte/SOP-*`, `PROCESO_*` | `02.normativa/01.Protocols/_pending-migration/` |
| `06.Documentos_soporte/LIVING_DOCUMENTS_MEMORY_SERVICE.md` | `05.proyectos/memory-service/living-documents/` |
| `06.Skills/` | `02.normativa/03.Skills/_pending-migration/` |
| `05.Templates/02.Operativos/` | `01.agents/operativos-templates/` |
| `05.Templates/05.Proyecto/02.Genericos/` | `03.templates/tarea/` |
| `05.Templates/05.Proyecto/03.Handoff/` | `03.templates/handoff/` |
| `05.Templates/05.Proyecto/04.Specs_Design/` | `03.templates/specs-design/` |
| `05.Templates/03.Memory/` | `03.templates/memoria/` |
| `05.Templates/04.contexto/` | `03.templates/contexto/` |
| `05.Templates/01.SETUP/` | `03.templates/setup-vtt/` |
| `01.agent-setup/` | `01.agents/setups/` |
| `01.operativos/` | `05.proyectos/memory-service/operativos-instancias/` |
| `02.roles/` | `01.agents/roles/` |
| `07.init-messages/` | `01.agents/init-messages/` |
| `09.kits/` | `01.agents/kits/` |
| `03.standard/01_ONBOARDING.md`, `02_OPERACION_AGENTE.md` | `01.agents/onboarding/` |
| `03.standard/03_FLUJO_*`, `06_*`, `07_*`, `08_*`, `10_*`, `11_*` | `02.normativa/01.Protocols/_pending-migration/` |
| `03.standard/04_ESTRUCTURA_FASES.md`, `05_CATALOGO_DELIVERABLES.md` | `02.normativa/catalogs/` |
| `03.standard/09.AGENT_RULES_Rev.md` | `02.normativa/00.Rules/sources/` |
| `04.Process/01.authorizaton/doc_sec_*.md` | `02.normativa/00.Rules/sources/` |
| `04.Process/configuracion_deliverables/` | `02.normativa/catalogs/deliverables/` |
| `04.Process/01_PM_PROCESO_*`, `02.PJM_PROCESO_*`, `SETUP_PROCESS_PM.md` | `02.normativa/01.Protocols/_pending-migration/` |

Ver README maestro de `00-platform/` para navegación completa.

---

## 1. Propósito

Inventario centralizado de **todos los documentos operativos** de VTT (Protocols, Workflows, Skills, Scripts, Templates, Metodologías) con su ubicación canónica, estado y referencias cruzadas.

Reemplaza al catálogo legacy `CATALOGO_SKILLS_MEMORY_SERVICE.md` (que solo cubría skills).

## 2. Convención de paths

### Path canónico (Source of Truth)

```
$VTT_NORMATIVA = virtual-teams-setup/00-platform/
```

Todos los documentos normativos viven aquí. Los proyectos referencian este path.

### Path legacy (durante migración progresiva)

Los proyectos pueden mantener copias temporales en su propia `00-platform/`. Estas copias se marcan como **LEGACY** y se eliminarán al completarse la migración.

### Aplicación de Opción C (paths con fallback)

Los operativos y scripts referencian:
```
1. Path canónico: $VTT_NORMATIVA/...
2. Fallback legacy: ./00-platform/...  (relativo al proyecto)
```

---

## 2.bis Nivel 0 — Rules (transversal)

> Modelo Operativo VTT — Nivel 0 (restringe transversalmente a Protocols/Workflows/Skills/Scripts).

### Sistema de Rules VTT

| Archivo | Path canónico | Propósito | Estado |
|---|---|---|---|
| README del sistema | `07.Normativa/00.Rules/README.md` | Manifiesto + modelo de 8 niveles + alineación doc_sec | ✅ Activo (v1.0) |
| Schema validador | `07.Normativa/00.Rules/rules_schema.json` | JSON Schema para validar `rules_catalog.json` | ✅ Activo (v1.0) |
| Catálogo de reglas | `07.Normativa/00.Rules/rules_catalog.json` | 43 reglas iniciales (ABAC doc_sec_02 + AGENT_RULES + VTT-operacionales) | ✅ Activo (v1.0) |
| Catálogo de capabilities | `07.Normativa/00.Rules/capabilities_catalog.json` | 30 capabilities base de doc_sec_02 | ✅ Activo |
| Catálogo de roles | `07.Normativa/00.Rules/roles_catalog.json` | 9 roles + matriz RBAC completa de doc_sec_04 §4.3 | ✅ Activo |
| Motor de filtros | `07.Normativa/00.Rules/query_rules.py` | Resolución jerárquica (sin BD aún) — `--validate`, `--list`, `--simulate-task`, `--context-json` | ✅ Funcional |

### Documentos fuente del Bloque 1 de Autorización

| Documento | Path | Contenido |
|---|---|---|
| `doc_sec_01_modelo_seguridad_actores_scopes_bloque_1` | `04.Process/01.authorizaton/` | Actores, recursos, jerarquía Platform→Org→Workspace→Resource |
| `doc_sec_02_politicas_permisos_rbac_abac_bloque_1` | `04.Process/01.authorizaton/` | 30 capabilities, 9 roles, reglas ABAC, acciones humanas |
| `doc_sec_03_arquitectura_implementacion_autorizacion_bloque_1` | `04.Process/01.authorizaton/` | Middleware authenticate/resolveAuthorizationContext/requireCapability/requirePolicy |
| `doc_sec_04_matriz_autorizacion_bloque_1` | `04.Process/01.authorizaton/` | Matriz RBAC capability×rol completa |

### Resumen del catálogo de Rules

| Métrica | Valor |
|---|---|
| Reglas activas | 43 |
| Niveles de scope | 8 (Platform/Org/Workspace/Project/Phase/Task/Role/Agent) |
| Tipos de actor | 4 (Human/Agent/Service_Account/External) |
| Markers operativos | 7 (mandatory, sensitive, human_only, sod_enforcement, blocks_review_gate, auto_detect, agent_default_forbidden) |
| Severidades | critical (12), high (18), medium (11), low (0) |
| Auto-detect habilitado | 19 reglas |

### Mejoras propuestas relacionadas

| Mejora | Propósito |
|---|---|
| `IMPROVE-004_rules_como_feature_vtt` | Implementar Rules en BD + API + Hook Manager |
| `IMPROVE-005_extension_recursos_vtt_especificos` | Agregar ~25 capabilities + ~20 reglas VTT-nativas (TIs, manifests, devlogs, LDs) |

---

## 3. Nivel 1 — Protocols (SOPs genéricos VTT)

> Modelo Operativo VTT — Nivel 4 (gobierna el proceso completo).

| Código | Título | Path canónico | Estado |
|---|---|---|---|
| `VTT.PROTOCOL-GOV-001` | Guía Normativa VTT (4 niveles) | `07.Normativa/00_GUIA_NORMATIVA_VTT.md` | ✅ Activo |
| `VTT.PROTOCOL-ASG-001` | Ciclo de asignación y cierre de tarea | `07.Normativa/01.Protocols/VTT.PROTOCOL-ASG-001_ciclo_asignacion_tarea.md` | ✅ Activo (2026-05-13) |
| `VTT.PROTOCOL-ISS-001` | Proceso de Issue y on_hold | `07.Normativa/01.Protocols/VTT.PROTOCOL-ISS-001_*.md` | ⚪ Pendiente |

### Documentos pre-VTT.PROTOCOL (legacy con función de Protocol)

| Documento legacy | Path actual | Equivalencia VTT | Plan |
|---|---|---|---|
| `SOP-LD-01_living_documents.md` | `06.Documentos_soporte/` | `VTT.PROTOCOL-LD-001` | Migrar al editar |
| `SOP-TRK-01_trackable_items_workflow.md` | `06.Documentos_soporte/` | `VTT.PROTOCOL-TRK-001` | Migrar al editar |
| `SOP-TRK-02_dynamic_item_creation.md` | `06.Documentos_soporte/` | `VTT.PROTOCOL-TRK-002` | Migrar al editar |
| `SOP-EST-01_technical_estimates.md` | `06.Documentos_soporte/` (memory-service-project) | `VTT.PROTOCOL-EST-001` | Migrar al editar |
| `SOP-VEL-01_velocity_methodology.md` | `06.Documentos_soporte/` (memory-service-project) | `VTT.PROTOCOL-VEL-001` | Migrar al editar |
| `SOP-RET-01_retrospective_analysis.md` | `06.Documentos_soporte/` (memory-service-project) | `VTT.PROTOCOL-RET-001` | Migrar al editar |
| `SOP_GENERACION_HO_PJM.md` | `memory-service-project/docs/` | `VTT.PROTOCOL-HO-001` | Migrar al editar |
| `SOP_GENERACION_SPRINT_DOCS.md` | `memory-service-project/docs/` | `VTT.PROTOCOL-SPR-001` | Migrar al editar |

---

## 4. Nivel 3 — Workflows (WIs)

> Modelo Operativo VTT — Nivel 3 (guía pasos secuenciales sin decisiones de negocio).

| Código | Título | Path canónico | Estado |
|---|---|---|---|
| `VTT.WORKFLOW-ASG-001.001` | Validar inputs del handoff | `07.Normativa/02.Workflows/` | ⚪ Pendiente — invocado por PROTOCOL-ASG-001 §5.0.2 |
| `VTT.WORKFLOW-ASG-001.002` | Analizar handoff y extraer scope | `07.Normativa/02.Workflows/` | ⚪ Pendiente — §5.1.1 |
| `VTT.WORKFLOW-ASG-001.003` | Determinar datos de tareas | `07.Normativa/02.Workflows/` | ⚪ Pendiente — §5.1.2 |
| `VTT.WORKFLOW-ASG-001.004` | Setup inicial estructura VTT | `07.Normativa/02.Workflows/` | ⚪ Pendiente — §5.1.4 |
| `VTT.WORKFLOW-ASG-001.005` | Mapear dependencias del sprint | `07.Normativa/02.Workflows/` | ⚪ Pendiente — §5.1.6 |
| `VTT.WORKFLOW-ASG-001.006` | Crear tareas del sprint | `07.Normativa/02.Workflows/` | ⚪ Pendiente — §5.1.7 |
| `VTT.WORKFLOW-ASG-001.007` | Generar y subir BRIEFs | `07.Normativa/02.Workflows/` | ⚪ Pendiente — §5.1.9 |
| `VTT.WORKFLOW-ASG-001.008` | Analizar dependencias de datos | `07.Normativa/02.Workflows/` | ⚪ Pendiente — §5.2.3 |
| `VTT.WORKFLOW-ASG-001.009` | Generar ASSIGNMENT desde código | `07.Normativa/02.Workflows/` | ⚪ Pendiente — §5.2.5 |
| `VTT.WORKFLOW-ASG-001.010` | Entrega del agente (ref) | `07.Normativa/02.Workflows/` | ⚪ Pendiente — §5.3.5 |
| `VTT.WORKFLOW-ASG-001.011` | Analizar Issue y decidir acción | `07.Normativa/02.Workflows/` | ⚪ Pendiente — §5.4.3 |
| `VTT.WORKFLOW-ASG-001.012` | Code review técnico | `07.Normativa/02.Workflows/` | ⚪ Pendiente — §5.5.6 |
| `VTT.WORKFLOW-ASG-001.013` | Aplicar Modelo Dinámico al cierre | `07.Normativa/02.Workflows/` | ⚪ Pendiente — §5.5.8 |
| `VTT.WORKFLOW-ASG-001.014` | Actualizar manifest a v1.5 | `07.Normativa/02.Workflows/` | ⚪ Pendiente — §5.5.11 |
| `VTT.WORKFLOW-ASG-001.015` | Firma de stage development | `07.Normativa/02.Workflows/` | ⚪ Pendiente — §5.6.2 |
| `VTT.WORKFLOW-ASG-001.016` | Cierre de sprint CLOSURE | `07.Normativa/02.Workflows/` | ⚪ Pendiente — §5.6.5 |
| `VTT.WORKFLOW-ASG-001.017` | Revisar Living Documents impactados | `07.Normativa/02.Workflows/` | ⚪ Pendiente — §5.3.5 |
| `VTT.WORKFLOW-ASG-001.018` | Registrar Document Impacts | `07.Normativa/02.Workflows/` | ⚪ Pendiente — §5.3.6 |
| `VTT.WORKFLOW-ASG-001.019` | Ejecutar Hardcode Check | `07.Normativa/02.Workflows/` | ⚪ Pendiente — §5.3.7 |
| `VTT.WORKFLOW-ASG-001.020` | Verificar worktree por rol del agente | `07.Normativa/02.Workflows/` | ⚪ Pendiente — §5.2.10 |
| `VTT.WORKFLOW-ASG-001.021` | Generar execution_manifest.json | `07.Normativa/02.Workflows/` | ⚪ Pendiente — §5.2.11 |
| `VTT.WORKFLOW-ASG-001.022` | Agente lee execution_manifest y verifica allowedPaths | `07.Normativa/02.Workflows/` | ⚪ Pendiente — §5.3.2.b |
| `VTT.WORKFLOW-ASG-001.023` | Verificar disciplina de worktree (TL Reviewer Paso 4b) | `07.Normativa/02.Workflows/` | ⚪ Pendiente — §5.5.5.b |
| `VTT.WORKFLOW-ASG-001.024` | Cleanup branch local post-aprobación (Paso 9) | `07.Normativa/02.Workflows/` | ⚪ Pendiente — §5.5.18 |

> **Nota:** los Workflows nacen cuando se genera su Protocol padre. No hay Workflows huérfanos.

---

## 5. Nivel 2 — Skills

> Modelo Operativo VTT — Nivel 2 (capacidades reusables parametrizadas).

### Path canónico de skills

```
$VTT_NORMATIVA/06.Skills/  (path actual — se moverá a 07.Normativa/03.Skills/ en migración)
```

### Catálogo completo

#### Categoría AUTH

| Código | Título | Path | Estado |
|---|---|---|---|
| `SKL-AUTH-01` | Obtener JWT Token | `06.Skills/auth/SKL-AUTH-01_obtener-jwt.md` | ✅ Activo |

#### Categoría VTT-TASK (gestión de tareas)

| Código | Título | Path | Estado |
|---|---|---|---|
| `SKL-TASK-01` | Crear tarea en VTT | `06.Skills/vtt-task/SKL-TASK-01_crear-tarea.md` | ✅ Activo |
| `SKL-TASK-02` | Generar ASSIGNMENT | `06.Skills/vtt-task/SKL-TASK-02_generar-assignment.md` | ✅ Activo |
| `SKL-TASK-03` | Asignar tarea a agente | `06.Skills/vtt-task/SKL-TASK-03_asignar-tarea.md` | ✅ Activo |
| `SKL-TASK-04` | Mensaje al agente | `06.Skills/vtt-task/SKL-TASK-04_mensaje-agente.md` | ✅ Activo |
| `SKL-TASK-05` | Review de tarea | `06.Skills/vtt-task/SKL-TASK-05_review-tarea.md` | ✅ Activo |

#### Categoría VTT-STATUS

| Código | Título | Path | Estado |
|---|---|---|---|
| `SKL-STATUS-01` | Mover a task_in_progress | `06.Skills/vtt-task/SKL-STATUS-01_task-in-progress.md` | ✅ Activo |
| `SKL-STATUS-02` | Mover a task_in_review | `06.Skills/vtt-task/SKL-STATUS-02_task-in-review.md` | ✅ Activo |
| `SKL-STATUS-03` | Mover a task_completed (TL) | `06.Skills/vtt-task/SKL-STATUS-03_task-completed-tl.md` | ✅ Activo |
| `SKL-STATUS-04` | Mover a task_approved (PM) | `06.Skills/vtt-task/SKL-STATUS-04_task-approved-pm.md` | ✅ Activo |
| `SKL-STATUS-05` | Mover a task_on_hold | `06.Skills/vtt-task/SKL-STATUS-05_task-on-hold.md` | ✅ Activo |
| `SKL-STATUS-06` | Mover a task_rejected | `06.Skills/vtt-task/SKL-STATUS-06_task-rejected-pm.md` | ✅ Activo |

#### Categoría VTT-QUERY

| Código | Título | Path | Estado |
|---|---|---|---|
| `SKL-QUERY-01` | Mis tareas asignadas | `06.Skills/vtt-task/SKL-QUERY-01_mis-tareas.md` | ✅ Activo |
| `SKL-QUERY-02` | Tareas en revisión | `06.Skills/vtt-task/SKL-QUERY-02_tareas-en-revision.md` | ✅ Activo |
| `SKL-QUERY-03` | Detalle de tarea | `06.Skills/vtt-task/SKL-QUERY-03_detalle-tarea.md` | ✅ Activo |
| `SKL-QUERY-04` | Avance de fases | `06.Skills/vtt-task/SKL-QUERY-04_avance-fases.md` | ✅ Activo |
| `SKL-QUERY-05` | Estado de fase asignable | `06.Skills/vtt-task/SKL-QUERY-05_estado-fase-asignable.md` | ✅ Activo |

#### Categoría VTT-COMMENT

| Código | Título | Path | Estado |
|---|---|---|---|
| `SKL-COMMENT-01` | Comment genérico | `06.Skills/vtt-task/SKL-COMMENT-01_comentario-generico.md` | ✅ Activo |
| `SKL-COMMENT-02` | APR-PM | `06.Skills/vtt-task/SKL-COMMENT-02_apr-pm.md` | ✅ Activo |
| `SKL-COMMENT-03` | APR-TL | `06.Skills/vtt-task/SKL-COMMENT-03_apr-tl.md` | ✅ Activo |

#### Categoría VTT-DEVLOG

| Código | Título | Path | Estado |
|---|---|---|---|
| `SKL-DEVLOG-01` | Registrar decision | `06.Skills/vtt-task/SKL-DEVLOG-01_decision.md` | ✅ Activo |
| `SKL-DEVLOG-02` | Registrar observación | `06.Skills/vtt-task/SKL-DEVLOG-02_observacion.md` | ✅ Activo |

#### Categoría VTT-ISSUE

| Código | Título | Path | Estado |
|---|---|---|---|
| `SKL-ISSUE-01` | Crear issue | `06.Skills/vtt-task/SKL-ISSUE-01_crear-issue.md` | ✅ Activo |

#### Categoría VTT-ATTACH

| Código | Título | Path | Estado |
|---|---|---|---|
| `SKL-ATTACH-01` | Subir archivo | `06.Skills/vtt-attach/SKL-ATTACH-01_subir-archivo.md` | ✅ Activo |
| `SKL-ATTACH-02` | Subir devlog | `06.Skills/vtt-attach/SKL-ATTACH-02_subir-devlog.md` | ✅ Activo |

#### Categoría GIT (formato VTT — genéricas, parametrizables)

| Código | Título | Path canónico | Estado |
|---|---|---|---|
| `VTT.SKILL-GIT-001` | Crear branch estructurado verificable contra un patrón | `02.normativa/03.Skills/git/VTT.SKILL-GIT-001_crear_branch_estructurado.md` | ✅ Nuevo (2026-05-17) |
| `VTT.SKILL-GIT-002` | Commit estructurado verificable contra un schema de mensaje | `02.normativa/03.Skills/git/VTT.SKILL-GIT-002_commit_estructurado.md` | ✅ Nuevo (2026-05-17) |

#### Categoría GIT-OPS (legacy Memory Service — pending migration)

| Código | Título | Path | Estado |
|---|---|---|---|
| `SKL-GIT-01` | Crear branch | `06.Skills/git-ops/SKL-GIT-01_crear-branch.md` | ✅ Activo (legacy) |
| `SKL-GIT-02` | Rebase main | `06.Skills/git-ops/SKL-GIT-02_rebase-main.md` | ✅ Activo (legacy) |
| `SKL-GIT-03` | Commit formato | `06.Skills/git-ops/SKL-GIT-03_commit-formato.md` | ✅ Activo (legacy — superseded por `VTT.SKILL-GIT-002`) |
| `SKL-GIT-04` | Crear PR | `06.Skills/git-ops/SKL-GIT-04_crear-pr.md` | ✅ Activo (legacy) |

#### Categoría REPORT

| Código | Título | Path | Estado |
|---|---|---|---|
| `SKL-REPORT-01` | Reporte de entrega | `06.Skills/report/SKL-REPORT-01_entrega-tarea.md` | ✅ Activo |
| `SKL-REPORT-02` | Reporte ejecutivo PJM | `06.Skills/report/SKL-REPORT-02_reporte-pjm.md` | ✅ Activo |

#### Categoría FILE-STRUCTURE

| Código | Título | Path | Estado |
|---|---|---|---|
| `SKL-STRUCTURE-01` | Ubicar entregable | `06.Skills/file-structure/SKL-STRUCTURE-01_ubicar-entregable.md` | ✅ Activo |

### Skills nuevas (solo en memory-service-project — pendientes de migrar a VTT setup)

| Código | Título | Path actual | Plan |
|---|---|---|---|
| `SKL-DYNAMIC-MODEL-01` | Cierre con modelo dinámico | `memory-service-project/00-platform/06.Skills/dynamic-model/` | Migrar a VTT setup |
| `SKL-MANIFEST-01` | Generar/actualizar manifest | `memory-service-project/00-platform/06.Skills/manifest/` | Migrar a VTT setup |
| `SKL-MESSAGE-01` | Generar mensaje agente (auto) | `memory-service-project/00-platform/06.Skills/message/` | Migrar a VTT setup |

### Catálogo legacy

| Documento | Estado | Reemplazo |
|---|---|---|
| `CATALOGO_SKILLS_MEMORY_SERVICE.md` v1.3 | 🟡 Activo pero obsoleto conceptualmente | Este `INVENTARIO_DOCUMENTOS_VTT.md` lo absorbe — deprecar al cerrar SOP-ASG-001 |

---

## 6. Nivel 1 — Scripts

> Modelo Operativo VTT — Nivel 1 (comandos atómicos ejecutables).

| Código | Título | Path canónico | Estado |
|---|---|---|---|
| `VTT.SCRIPT-*` | Scripts ejecutables | `07.Normativa/04.Scripts/` | ⚪ Carpeta vacía — pendiente de generar al ejecutar Protocols |

### Scripts existentes (sin nomenclatura VTT aún)

| Script | Path actual | Propósito | Plan |
|---|---|---|---|
| `add_phase1_deps_vtt.py` | `memory-service-project/Release2.0/scripts/` | Agregar deps Phase 1 | Refactorizar a SCRIPT genérico |
| `create_memory_service_vtt.py` | `memory-service-project/Release2.0/scripts/` | Setup proyecto en VTT | Refactorizar |
| `fix_dev_deps_vtt.py` | `memory-service-project/Release2.0/scripts/` | Fix dependencias dev | Refactorizar |
| `generate_and_upload_briefs_phase1.py` | `memory-service-project/Release2.0/scripts/` | Generar y subir BRIEFs | Refactorizar |
| `patch_116_tasks_metadata.py` | `memory-service-project/Release2.0/scripts/` | Patch metadata bulk | Refactorizar |
| `restructure_phase1_vtt.py` | `memory-service-project/Release2.0/scripts/` | Restructurar Phase 1 | Histórico, mantener |
| `resume_tasks_vtt.py` | `memory-service-project/Release2.0/scripts/` | Resume de tareas | Refactorizar |
| `gen_mensaje.py` | **NO existe en disco** — referenciado en SKL-MESSAGE-01 | Generar mensaje agente | **Pendiente de crear** |

---

## 7. Templates

> Plantillas instanciables para artefactos del proyecto.

### Templates activos en VTT setup (Source of Truth)

| Código | Título | Path canónico | Estado |
|---|---|---|---|
| `VTT.TEMPLATE-CLO-001` | CLOSURE_S[N] (cierre de sprint) | `03.templates/normativa/VTT.TEMPLATE-CLO-001_closure_sprint.md` | ✅ Nuevo (2026-05-13) |
| `VTT.TEMPLATE-CFL-001` | Criteria Fulfillment (agente reporta CAs) | `03.templates/normativa/VTT.TEMPLATE-CFL-001_criteria_fulfillment.md` | ✅ Nuevo (2026-05-13) |
| `VTT.TEMPLATE-APR-001` | APR-TL Comment | `03.templates/normativa/VTT.TEMPLATE-APR-001_apr_tl_comment.md` | ✅ Nuevo (2026-05-13) |

### Templates de autoría (moldes para crear normativa)

> Carpeta `03.templates/normativa/_autoria/` — usados por autores (PM/TL) cuando crean nuevos Protocols/Workflows/Skills/Scripts.

| Template | Para crear | Path canónico | Estado |
|---|---|---|---|
| `TEMPLATE_PROTOCOL.md` | Protocol nuevo (Nivel 4) | `03.templates/normativa/_autoria/TEMPLATE_PROTOCOL.md` | ✅ Nuevo (2026-05-17) |
| `TEMPLATE_WORKFLOW.md` | Workflow nuevo (Nivel 3) | `03.templates/normativa/_autoria/TEMPLATE_WORKFLOW.md` | ✅ Nuevo (2026-05-17) |
| `TEMPLATE_SKILL.md` | Skill nueva (Nivel 2) | `03.templates/normativa/_autoria/TEMPLATE_SKILL.md` | ✅ Nuevo (2026-05-17) |
| `TEMPLATE_SCRIPT.py` | Script nuevo (Nivel 1) | `03.templates/normativa/_autoria/TEMPLATE_SCRIPT.py` | ✅ Nuevo (2026-05-17) |
| `README.md` | Guía de uso de los 4 templates | `03.templates/normativa/_autoria/README.md` | ✅ Nuevo (2026-05-17) |

### Guía de autor (narrativa con anti-patterns)

| Documento | Path canónico | Propósito | Estado |
|---|---|---|---|
| `GUIA_AUTOR.md` | `02.normativa/GUIA_AUTOR.md` | Guía narrativa de 12 secciones: checklist previo, decisión de nivel, asignación de código, checklists por nivel, 8 anti-patterns con ejemplos, workflow del autor (10 pasos), Reglas Nivel 0, versionado, FAQ | ✅ Nuevo (2026-05-17) |

### Templates pre-VTT (legacy en `05.Templates/`)

#### 05.Templates/01.SETUP/01_PM/

| Template | Path | Propósito | Estado |
|---|---|---|---|
| `TEMPLATE_CIERRE_PM_HANDOFF_PJM_V1.0.md` | `05.Templates/01.SETUP/01_PM/` | HO PM → PJM | ✅ Activo |
| `TEMPLATE_CONSOLIDADO_V1.0.md` | `05.Templates/01.SETUP/01_PM/` | Doc consolidado fase | ✅ Activo |
| `TEMPLATE_FASES_APLICABLES_V1.0.md` | `05.Templates/01.SETUP/01_PM/` | Fases aplicables a proyecto | ✅ Activo |
| `TEMPLATE_HO_PJM_CARGA_VTT_V1.0.md` | `05.Templates/01.SETUP/01_PM/` | HO PJM carga VTT | ✅ Activo |
| `TEMPLATE_PRE_HANDOFF_INICIACION_V1.0.md` | `05.Templates/01.SETUP/01_PM/` | Pre-HO iniciación | ✅ Activo |
| `TEMPLATE_TASK_INDEX_SEED_V1.0.md` | `05.Templates/01.SETUP/01_PM/` | Task index seed | ✅ Activo |
| `TEMPLATE_create_vtt_script_V1.0.py` | `05.Templates/01.SETUP/01_PM/` | Script template setup VTT | ✅ Activo |

#### 05.Templates/02.Operativos/ (plantillas operativos por rol)

| Template | Path | Rol | Estado |
|---|---|---|---|
| `OPERATIVO_AR_TEMPLATE.md` | `05.Templates/02.Operativos/` | AR | ✅ Activo |
| `OPERATIVO_BE_TEMPLATE.md` | `05.Templates/02.Operativos/` | BE | ✅ Activo |
| `OPERATIVO_DB_TEMPLATE.md` | `05.Templates/02.Operativos/` | DB | ✅ Activo |
| `OPERATIVO_DL_TEMPLATE.md` | `05.Templates/02.Operativos/` | DL | ✅ Activo |
| `OPERATIVO_DO_TEMPLATE.md` | `05.Templates/02.Operativos/` | DO | ✅ Activo |
| `OPERATIVO_FE_TEMPLATE.md` | `05.Templates/02.Operativos/` | FE | ✅ Activo |
| `OPERATIVO_PJM_TEMPLATE.md` | `05.Templates/02.Operativos/` | PJM | ✅ Activo |
| `OPERATIVO_PM_TEMPLATE.md` | `05.Templates/02.Operativos/` | PM | ✅ Activo |
| `OPERATIVO_PM_REVISOR_TEMPLATE.md` | `05.Templates/02.Operativos/` | PM Revisor | ✅ Activo |
| `OPERATIVO_QA_TEMPLATE.md` | `05.Templates/02.Operativos/` | QA | ✅ Activo |
| `OPERATIVO_SA_TEMPLATE.md` | `05.Templates/02.Operativos/` | SA | ✅ Activo |
| `OPERATIVO_TL_TEMPLATE.md` | `05.Templates/02.Operativos/` | TL | ✅ Activo |
| `OPERATIVO_UX_TEMPLATE.md` | `05.Templates/02.Operativos/` | UX | ✅ Activo |

#### 05.Templates/03.Memory/

| Template | Path | Propósito |
|---|---|---|
| `MEMORY_TEMPLATE.md` | `05.Templates/03.Memory/` | Memoria de agente |

#### 05.Templates/04.contexto/

| Template | Path | Propósito |
|---|---|---|
| `CONTEXTO_DL_SESION_TEMPLATE.md` | `05.Templates/04.contexto/` | Contexto sesión DL |
| `CONTEXTO_PJM_SESION_TEMPLATE.md` | `05.Templates/04.contexto/` | Contexto sesión PJM |
| `CONTEXTO_PM_SESION_TEMPLATE.md` | `05.Templates/04.contexto/` | Contexto sesión PM |
| `CONTEXTO_TL_SESION_TEMPLATE.md` | `05.Templates/04.contexto/` | Contexto sesión TL |

#### 05.Templates/05.Proyecto/02.Genericos/

| Template | Path | Propósito | Estado |
|---|---|---|---|
| `TEMPLATE_BRIEF_LARGE.md` | `05.Templates/05.Proyecto/02.Genericos/` | BRIEF de tarea | ✅ Activo |
| `TEMPLATE_ASIGNACION_TAREARev.md` v3.1 | `05.Templates/05.Proyecto/02.Genericos/` | ASSIGNMENT de tarea | ✅ Activo (recientemente actualizado) |
| `TEMPLATE_DEVELOPMENT_LOG.md` | `05.Templates/05.Proyecto/02.Genericos/` | Devlog archivo markdown | ✅ Activo |
| `TEMPLATE_DEVLOG.md` | `05.Templates/05.Proyecto/02.Genericos/` | Devlog entries VTT | ✅ Activo |
| `TEMPLATE_CODE_LOGIC_ACTUALIZADO.md` | `05.Templates/05.Proyecto/02.Genericos/` | `.LOGIC.md` por archivo | ✅ Activo |
| `TEMPLATE_HANDOFF.md` | `05.Templates/05.Proyecto/02.Genericos/` | HO genérico | 🟡 Revisar — posible obsoleto |
| `TEMPLATE_ISSUE.md` | `05.Templates/05.Proyecto/02.Genericos/` | Issue en VTT | ✅ Activo |
| `TEMPLATE_MENSAJE_ASIGNACION.md` | `05.Templates/05.Proyecto/02.Genericos/` | Mensaje al agente | 🟡 Reemplazo por `gen_mensaje.py` |
| `GUIA_USO_TEMPLATES.md` | `05.Templates/05.Proyecto/02.Genericos/` | Manual de uso | ✅ Activo |
| `METODOLOGIA_EJECUCION_SPRINTS_V1.md` | `05.Templates/05.Proyecto/02.Genericos/` | Metodología base | ✅ Activo |

#### 05.Templates/05.Proyecto/03.Handoff/

| Template | Path | Propósito | Estado |
|---|---|---|---|
| `TEMPLATE_HANDOFF_TL_V2.1.md` | `05.Templates/05.Proyecto/03.Handoff/` | HO PJM → TL | ✅ Activo |
| `TEMPLATE_HANDOFF_FE_V1.1.md` | `05.Templates/05.Proyecto/03.Handoff/` | HO TL → FE | 🔴 Obsoleto (proceso corto) |
| `TEMPLATE_HANDOFF_DL_V1.1.md` | `05.Templates/05.Proyecto/03.Handoff/` | HO TL → DL | 🔴 Obsoleto (proceso corto) |
| `TEMPLATE_HANDOFF_QA_V1.1.md` | `05.Templates/05.Proyecto/03.Handoff/` | HO TL → QA | 🔴 Obsoleto (proceso corto) |
| `TEMPLATE_DEVLOG_V1.1.md` | `05.Templates/05.Proyecto/03.Handoff/` | Devlog v1.1 | ✅ Activo (más reciente que el de 02.Genericos) |
| `METODOLOGIA_SETUP_FASE.md` | `05.Templates/05.Proyecto/03.Handoff/` | Setup de fase | ✅ Activo |
| `METODOLOGIA_SETUP_PROYECTOS_VTT.md` | `05.Templates/05.Proyecto/03.Handoff/` | Setup proyecto VTT | ✅ Activo |
| `METODOLOGIA_SETUP_PLAN_VTT.md` | `05.Templates/05.Proyecto/03.Handoff/` | Planificación VTT | ✅ Activo |
| `METODOLOGIA_EJECUCION_SPRINTS_V1.1.md` | `05.Templates/05.Proyecto/03.Handoff/` | Ejecución sprints v1.1 | ✅ Activo |
| `METODOLOGIA_CIERRE_SPRINT_FASE.md` | `05.Templates/05.Proyecto/03.Handoff/` | Cierre sprint/fase | ✅ Activo |
| `CODE_REVIEW_GUIDE_V1.1.md` | `05.Templates/05.Proyecto/03.Handoff/` | Guía code review TL | ✅ Activo |
| `INTEGRATION_AUDIT_CHECKLIST_V1.1.md` | `05.Templates/05.Proyecto/03.Handoff/` | Checklist integración AR | ✅ Activo |
| `TESTING_GUIDE_V1.1.md` | `05.Templates/05.Proyecto/03.Handoff/` | Guía testing QA | ✅ Activo |

#### 05.Templates/05.Proyecto/04.Specs_Design/

12+ templates de specs UI/UX (Landing, DataGrid, Form, Modal, etc.). Listados en `catalogo_maestro_templates_specs_uiux_v2.md`.

| Template | Path | Estado |
|---|---|---|
| `catalogo_maestro_templates_specs_uiux_v2.md` | `04.Specs_Design/` | ✅ Activo (índice) |
| `index_templates_specs_v2.md` | `04.Specs_Design/` | ✅ Activo |
| `README_base_conocimiento_templates_specs_v2.md` | `04.Specs_Design/` | ✅ Activo |
| `GUIA_Design_Tokens_Checklist.md` | `04.Specs_Design/` | ✅ Activo |
| `template_base_especificacion_funcional_uiux.md` | `04.Specs_Design/` | ✅ Activo |
| `TEMPLATE_BASE_Spec_*.md` (12+ archivos) | `04.Specs_Design/` | ✅ Activos (uno por tipo de pantalla) |

---

## 8. Documentos estándar (no normativos pero estructurales)

### 03.standard/

Documentos transversales que definen el modelo operativo VTT general.

| Documento | Path | Propósito |
|---|---|---|
| `00_INDEX.md` | `03.standard/` | Índice general |
| `01_ONBOARDING.md` | `03.standard/` | Onboarding de agentes |
| `02_OPERACION_AGENTE.md` | `03.standard/` | Cómo opera un agente |
| `03_FLUJO_TL.md` | `03.standard/` | Flujo del Tech Lead |
| `04_ESTRUCTURA_FASES.md` | `03.standard/` | Estructura de fases SDLC |
| `05_CATALOGO_DELIVERABLES.md` | `03.standard/` | Catálogo deliverables |
| `06_FLUJO_DL.md` | `03.standard/` | Flujo del Design Lead |
| `07_FLUJO_PJM.md` | `03.standard/` | Flujo del PJM |
| `08_FLUJO_PM.md` | `03.standard/` | Flujo del PM |
| `09.AGENT_RULES_Rev.md` | `03.standard/` | Reglas de agentes |
| `10_FLUJO_SA_REVIEWER.md` | `03.standard/` | Flujo del SA Reviewer |
| `11_GUIA_AGENTES_MODELO_DINAMICO_V4.md` | `03.standard/` | Guía Modelo Dinámico V4 |

---

## 9. Operativos por rol (instancias del proyecto)

### Plantillas (en VTT setup)

Ver §7 `05.Templates/02.Operativos/`.

### Instancias del proyecto Memory Service

| Operativo | Path (memory-service-project) | Path (memory-service-backend) | Rol |
|---|---|---|---|
| `OPERATIVO_TL_MEMORY-SERVICE.md` | `.claude/agents/` | — | Tech Lead |
| `OPERATIVO_BE_MEMORY-SERVICE.md` | `01.operativos/` | `.claude/agents/` | Backend |
| `OPERATIVO_DB_MEMORY-SERVICE.md` | `01.operativos/` | `.claude/agents/` | Database |
| `OPERATIVO_DO_MEMORY-SERVICE.md` | `.claude/agents/` y `01.operativos/` | `.claude/agents/` | DevOps |
| `OPERATIVO_FE_MEMORY-SERVICE.md` | `01.operativos/` | — | Frontend |
| `OPERATIVO_QA_MEMORY-SERVICE.md` | `01.operativos/` | — | QA |
| `OPERATIVO_DL_MEMORY-SERVICE.md` | `01.operativos/` | — | Design Lead |
| `OPERATIVO_UX_MEMORY-SERVICE.md` | `01.operativos/` | — | UX |
| `OPERATIVO_AR_MEMORY-SERVICE.md` | `01.operativos/` | — | Architect |
| `OPERATIVO_SA_MEMORY-SERVICE.md` | `01.operativos/` | — | Solution Analyst |
| `OPERATIVO_PJM_MEMORY-SERVICE.md` | `01.operativos/` (2 archivos similares — revisar) | — | Project Manager |
| `OPERATIVO_PM_MEMORY-SERVICE.md` | `01.operativos/` | — | Product Manager |

**Notas:**
- Hay un `OPERATIVO_TECH_LEAD.md` legacy en VTT setup `01.operativos/` que no aplica a Memory Service — revisar.
- Hay un `OPERATIVO_SA_REVIEWER.md` separado del `OPERATIVO_SA` — verificar si se fusiona o se mantiene.
- Hay duplicados `OPERATIVO_PJM_MEMORY-SERVICE.md` y `OPERATIVO_PJM_MEMORY_SERVICE.md` (diff: guión vs underscore) — consolidar.

---

## 10. Procesos legacy (Process/)

### 04.Process/

| Documento | Path | Propósito | Estado |
|---|---|---|---|
| `01_PM_PROCESO_ANALISIS_INICIAL.md` | `04.Process/` | Proceso análisis inicial PM | ✅ Activo |
| `02.PJM_PROCESO_SETUP_PROYECTO_VTT.md` | `04.Process/` | Setup proyecto VTT PJM | ✅ Activo |
| `SETUP_PROCESS_PM.md` | `04.Process/` | Proceso setup PM | ✅ Activo |

---

## 11. Mejoras (IMPROVEMENTS/)

| Código | Título | Path | Estado |
|---|---|---|---|
| `IMPROVE-001` | Pool de Transacciones VTT | `07.Normativa/IMPROVEMENTS/IMPROVE-001_*.md` | Propuesta |
| `IMPROVE-002` | BD para Manifiestos y TIs | `07.Normativa/IMPROVEMENTS/IMPROVE-002_*.md` | Propuesta |
| `IMPROVE-003` | Platform Gaps Backend VTT | `07.Normativa/IMPROVEMENTS/IMPROVE-003_*.md` | Propuesta |
| `IMPROVE-004` | Rules como Feature VTT (Bloque 1 Autorización) | `07.Normativa/IMPROVEMENTS/IMPROVE-004_*.md` | Propuesta |
| `IMPROVE-005` | Extensión modelo a recursos VTT-específicos | `07.Normativa/IMPROVEMENTS/IMPROVE-005_*.md` | Propuesta |

---

## 11.bis Guías operativas v2.x — Modelo de Worktrees por rol

> Implementación operativa del PROTOCOL-ASG-001 v1.2.0 (worktrees por rol + execution_manifest + N ventanas VSCode).

### Guías sincronizadas en virtual-teams-setup

| Documento | Versión | Path canónico | Cubre |
|---|---|---|---|
| `GUIA_WORKTREES_MEMORY_SERVICE.md` | v2.1 | `06.Documentos_soporte/` | Setup de worktrees por rol + 7 workspaces VSCode + reglas operativas |
| `GUIA_GIT_WORKTREES_TL_BACKEND.md` | v2.0 (LEGACY) | `06.Documentos_soporte/` | Reemplazado por v2.1 — pendiente deprecar |
| `GUIA_ASIGNACION_TAREA_TL_EJECUTOR.md` | v2.1 | `06.Documentos_soporte/` | Cheatsheet TL al asignar — Paso 8.5 (execution_manifest) |
| `GUIA_REVISION_TAREA_TL_REVIEWER.md` | v2.1 | `06.Documentos_soporte/` | Cheatsheet TL al cerrar — Paso 5b + Paso 16 |
| `PROCESO_CIERRE_TAREA_v2.md` | v2.1 (header dice v2.0) | `06.Documentos_soporte/` | Paso 4b (verificación worktree) + Paso 9 (cleanup) |
| `PROCESO_ASIGNACION_TAREAS_v3.md` | v3.1 | `06.Documentos_soporte/` | Paso 7b (execution_manifest) |
| `GUIA_MANIFEST_PARA_AGENTES.md` | v2.0 | `06.Documentos_soporte/` | Manifest v1.0 generado por agente |

### Infraestructura `.vtt/` (NO commiteada — vive en raíz del proyecto)

> En memory-service: `c:/Users/Martin/Documents/virtual-teams/memory-service/.vtt/`

| Componente | Ubicación | Estado |
|---|---|---|
| Worktrees por rol | `.vtt/worktrees/<repo>-<rol>/` (7 actuales: backend-be/do/db/qa + project-tl/pm/sa) | ✅ Creados |
| Workspaces VSCode | `.vtt/workspaces/<repo>-<rol>.code-workspace` (7 actuales) | ✅ Creados |
| Workspaces legacy | `.vtt/workspaces/legacy/` | ✅ Archivados |
| Template manifest ejecución | `.vtt/manifests/_template.execution.json` | ✅ Creado |
| Execution manifests por tarea | `.vtt/manifests/<TASK_ID>.execution.json` | Generados por TL al asignar |
| Archivo de manifests cerrados | `.vtt/manifests/archived/` | Tras task_approved |

### Scripts relacionados

| Script | Path | Propósito | Estado |
|---|---|---|---|
| `gen_mensaje.py` | `memory-service-project/scripts/` | Genera mensaje al agente (cwd por rol + fix S0-unknown) | ✅ Activo v2.1 |
| `setup_worktree.py` | `memory-service-project/scripts/` | LEGACY (era por tarea) | 🟡 Conservar por compat, no usar |
| `cleanup_worktree.py` | `memory-service-project/scripts/` | LEGACY (era por tarea) | 🟡 Conservar por compat, no usar |

### Nuevas reglas (rules_catalog v1.1)

| Rule | Categoría | Origen |
|---|---|---|
| `RULE-AGENT-001` v2.0 | Worktree | Actualizada — worktree por rol (antes era por tarea) |
| `RULE-TL-001` | Worktree TL | Nueva — TL opera en project-tl, no en clon base |
| `RULE-WT-001` | Worktree policy | Nueva — granularidad por rol, no por tarea |
| `RULE-WT-002` | Execution manifest | Nueva — agente lee manifest antes de empezar |
| `RULE-WT-003` | Cleanup | Nueva — borrar branch local post-aprobación |

---

## 12. Documentos de Soporte (memory-service-project)

> Documentos legacy que mezclan SOPs + conceptos + referencia.

| Documento | Path | Estado | Plan |
|---|---|---|---|
| `ANALISIS_FASES_COMPLETO_PARA_PM.md` | `06.Documentos_soporte/` | ✅ Activo | Mantener — input del PM |
| `CIERRE_PM_HANDOFF_PJM_MODELO_DINAMICO_V4.2.md` | `06.Documentos_soporte/` | ✅ Activo | Migrar a Protocol |
| `ESTRUCTURA_FASES_DESARROLLO_PROYECTOS_V3.1.md` | `06.Documentos_soporte/` | ✅ Activo | Mantener referencia |
| `HANDOFF_PJM_ADDENDUM_V4.5.md` | `06.Documentos_soporte/` | ✅ Activo | Mantener |
| `LIVING_DOCUMENTS_MEMORY_SERVICE.md` | `06.Documentos_soporte/` | ✅ Activo | Instancia proyecto, mantener |
| `METODOLOGIA_TRABAJO_PM_VTT.md` | `06.Documentos_soporte/` | ✅ Activo | Mantener |
| `ONBOARDING_TECHLEAD_DESIGN_MINE.md` | `06.Documentos_soporte/` | 🟡 Específico DesignMine | Revisar relevancia |
| `PROCESO_ASIGNACION_TAREAS.md` v1.6 | `06.Documentos_soporte/` | 🟡 Legacy | Reemplazo: `PROCESO_ASIGNACION_TAREAS_v3.md` en memory-service-project |
| `PROCESO_CIERRE_TAREA_v2.md` | `memory-service-project/00-platform/06.Documentos_soporte/` | ✅ Nuevo | Migrar a Protocol |
| `PROCESO_ANALISIS_DEPENDENCIAS_ASSIGNMENT.md` | `memory-service-project/.claude/rules/` | ✅ Activo | Mantener |
| `MAPA_DEPENDENCIAS_ENTREGABLES.md` | `memory-service-project/.claude/rules/` | ✅ Activo | Mantener |
| `ADDON_PASO0_ADR_REPOS_LECCION_APRENDIDA.md` | `06.Documentos_soporte/` | ✅ Activo | Mantener (lección) |

---

## 13. Reglas / Rules

### Reglas globales (usuario)

| Archivo | Path | Propósito |
|---|---|---|
| `rules_agents.instructions.md` | `~/.claude/rules/` | Reglas globales de agentes |

### Reglas por proyecto

| Archivo | Path | Propósito |
|---|---|---|
| `Proyect_data.md` | `memory-service-project/.claude/rules/` | UUIDs y datos del equipo Memory Service |
| `MAPA_DEPENDENCIAS_ENTREGABLES.md` | `memory-service-project/.claude/rules/` | Mapa dependencias |
| `PROCESO_ANALISIS_DEPENDENCIAS_ASSIGNMENT.md` | `memory-service-project/.claude/rules/` | Proceso análisis deps |

---

## 14. Artefactos del proyecto (NO normativos)

> Por completitud — estos NO son normativa, son entregables/outputs de los procesos.

### memory-service-project

```
knowledge/
├── agent-tasks/
│   ├── briefs/[fase]/[sprint]/         ← BRIEFs por tarea
│   ├── assignments/[fase]/[sprint]/    ← ASSIGNMENTs por tarea
│   └── messages/[fase]/[sprint]/       ← Mensajes generados a agentes
├── task-manifests/[fase]/[sprint]/     ← Manifests v1.5
├── development-log/                    ← Devlogs archivo MD
├── code-logic/                         ← .LOGIC.md por archivo de código
├── platform-feedback/                  ← VTT gaps, mejoras
└── kickoff/                            ← Kickoffs de proyecto
```

### memory-service-backend

```
docs/
├── SECRETS.md                          ← Política de secretos
├── SETUP.md                            ← Guía de setup
└── TROUBLESHOOTING.md                  ← Troubleshooting
```

---

## 15. Estado de salud del inventario

| Categoría | Total | Activos | Obsoletos | En migración |
|---|---|---|---|---|
| Rules (Nivel 0) | 47 catalogadas | 47 | 0 | 0 |
| Capabilities (catalog) | 30 (Bloque 1) + 25 propuestas (IMPROVE-005) | 30 documentadas | 0 | 25 propuestas |
| Roles (catalog) | 9 (Bloque 1) | 9 documentados | 0 | 0 |
| Protocols VTT | 2 | 2 (GUIA + ASG-001) | 0 | 1 en construcción (ISS-001) |
| Workflows VTT | 24 catalogados | 0 escritos | 0 | 24 pendientes (todos del ASG-001 v1.2) |
| Skills | 31 | 31 | 0 | 3 nuevas a migrar |
| Scripts | 7 visibles | 7 | 0 | Pendiente refactor |
| Templates (VTT.) operativos | 3 | 3 | 0 | — |
| Templates de autoría (`_autoria/`) | 4 + README | 4 + README | 0 | — |
| Guía de autor | 1 | 1 (GUIA_AUTOR.md) | 0 | — |
| Templates legacy | 50+ | 47 | 3 (HANDOFF_FE/DL/QA) | Migración progresiva |
| Metodologías | 6 | 6 | 0 | — |
| Operativos plantilla | 13 | 13 | 0 | — |
| Operativos instancia MS | 13 | 13 | 0 | — |
| SOPs legacy | 8 | 8 | 0 | Migrar a Protocol al editar |
| Standards (03.standard) | 12 | 12 | 0 | — |
| Documentos de soporte | 13 | 11 | 0 | 2 en revisión |
| Mejoras propuestas | 3 | 3 | 0 | — |

---

## 16. Política de mantenimiento

### Cuándo actualizar este inventario

1. Cuando se cree un documento nuevo en cualquier nivel
2. Cuando se deprecie un documento (mover a sección de obsoletos)
3. Cuando se mueva un documento entre repos
4. Al cierre de cada sprint (revisión global)

### Quién actualiza

- **PM**: revisión global y aprobación de cambios estructurales
- **TL**: actualización tras crear/editar Protocols, Workflows, Skills
- **Agentes**: notifican al TL si necesitan crear documento nuevo

### Cómo deprecar

1. Cambiar estado a 🔴 Obsoleto en este inventario
2. Mover archivo a `99.Deprecated/` con README explicando razón y fecha
3. Si tiene reemplazo, agregar referencia al reemplazo
4. Mantener en el inventario como referencia histórica

---

## 17. Cambios pendientes (TODO)

| # | Acción | Cuándo | Estado |
|---|---|---|---|
| 1 | Crear los Workflows del PROTOCOL-ASG-001 (16) | Cuando se implemente el Protocol en producción | ⚪ Pendiente |
| 2 | Crear el Protocol VTT.PROTOCOL-ASG-001 | — | ✅ Completado (2026-05-13) |
| 3 | Migrar SKL-DYNAMIC-MODEL-01 a VTT setup | Al implementar Workflows del ASG-001 | ⚪ Pendiente |
| 4 | Migrar SKL-MANIFEST-01 a VTT setup | Al implementar Workflows del ASG-001 | ⚪ Pendiente |
| 5 | Crear SKL-MESSAGE-01 + script gen_mensaje.py | Próximo trabajo | ⚪ Pendiente |
| 6 | Deprecar HANDOFF_FE/DL/QA legacy | Al cerrar ciclo completo | ⚪ Pendiente |
| 7 | Deprecar CATALOGO_SKILLS_MEMORY_SERVICE | Cuando inventario sea adoptado | ⚪ Pendiente |
| 8 | Consolidar operativos duplicados (PJM guión vs underscore) | Próxima limpieza | ⚪ Pendiente |
| 9 | Refactorizar scripts a VTT.SCRIPT-* | Migración progresiva | ⚪ Pendiente |
| 10 | README pointers en 2 repos Memory Service | — | ✅ Completado (2026-05-13) |
| 11 | Crear PROTOCOL-ISS-001 (Proceso de Issue) | Después del ASG-001 implementado | ⚪ Pendiente |
| 12 | Sistema de Rules Nivel 0 + catálogo inicial 43 reglas | — | ✅ Completado (2026-05-13) |
| 13 | Catálogos de Capabilities (30) y Roles (9) JSON | — | ✅ Completado (2026-05-13) |
| 14 | Motor query_rules.py funcional sin BD | — | ✅ Completado (2026-05-13) |
| 15 | IMPROVE-004 Rules como Feature VTT | — | ✅ Documentado (2026-05-13) |
| 16 | IMPROVE-005 Extensión a recursos VTT-específicos | — | ✅ Documentado (2026-05-13) |
| 17 | Migrar 25 capabilities + 20 reglas VTT-específicas a catálogos | Cuando IMPROVE-005 se apruebe | ⚪ Pendiente |
| 18 | Migrar reglas de los 438 deliverables del SDLC | Oleada 2 (IMPROVE-006 futuro) | ⚪ Pendiente |
| 19 | Actualizar PROTOCOL-ASG-001 a v1.2.0 (worktrees por rol + execution_manifest) | — | ✅ Completado (2026-05-14) |
| 20 | Sincronizar Guías v2.x/v3.1 a virtual-teams-setup | — | ✅ Completado por usuario (2026-05-14) |
| 21 | Migrar 5 nuevas reglas (TL-001, WT-001/002/003) + actualizar AGENT-001 | — | ✅ Completado (2026-05-14) |
| 22 | Deprecar GUIA_GIT_WORKTREES_TL_BACKEND.md (v2.0 legacy) | Próxima sesión | ⚪ Pendiente |
| 23 | Deprecar PROCESO_ASIGNACION_TAREAS.md v1.6 (reemplazado por v3.1) | Próxima sesión | ⚪ Pendiente |
| 24 | Crear 4 templates de autoría (_autoria/ + README) | — | ✅ Completado (2026-05-17) |
| 25 | Crear GUIA_AUTOR.md (narrativa con 8 anti-patterns + FAQ) | — | ✅ Completado (2026-05-17) |

---

## 18. Referencias

- Guía normativa: `00_GUIA_NORMATIVA_VTT.md` (define los 4 niveles)
- Mejoras propuestas: `IMPROVEMENTS/README.md`
- Proceso de cierre: `PROCESO_CIERRE_TAREA_v2.md` (memory-service-project — migrará)

---

## 19. Changelog

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-05-13 | Versión inicial — escaneo de los 3 repos (virtual-teams-setup + memory-service-project + memory-service-backend). 80+ documentos catalogados. |
| 1.1 | 2026-05-17 | Registro de templates de autoría (`_autoria/`) + `GUIA_AUTOR.md`. Actualización de paths VTT.TEMPLATE-* a `03.templates/normativa/` (post-reorganización). |
