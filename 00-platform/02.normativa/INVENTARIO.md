# Inventario Maestro de Documentos VTT

| Campo | Valor |
|---|---|
| **Versión** | 1.2 |
| **Fecha** | 2026-05-31 |
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
| Catálogo de reglas | `02.normativa/00.Rules/rules_catalog.json` | 49 reglas activas (ABAC doc_sec_02 + AGENT_RULES + VTT-operacionales + 2 nuevas OLA 1 MSG: `RULE-SCRIPT-001` y `RULE-TEMPLATE-001`) | ✅ v1.0 — actualizado 2026-05-22 |
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
| Reglas activas | 49 |
| Niveles de scope | 8 (Platform/Org/Workspace/Project/Phase/Task/Role/Agent) |
| Tipos de actor | 4 (Human/Agent/Service_Account/External) |
| Markers operativos | 7 (mandatory, sensitive, human_only, sod_enforcement, blocks_review_gate, auto_detect, agent_default_forbidden) |
| Severidades | critical (11), high (23), medium (11), low (4) |
| Auto-detect habilitado | 24 reglas |

### Reglas destacadas — OLA 1 cierre sub-sistema MSG (2026-05-22)

| Regla | Scope | Severity | Propósito |
|---|---|---|---|
| `RULE-SCRIPT-001` | PLATFORM | high | Scripts de normativa SOLO se invocan desde `$VTT_SETUP/02.normativa/04.Scripts/` — prohibido copiar al worktree. Origen: drift `gen_mensaje.py` 5 copias |
| `RULE-TEMPLATE-001` | PLATFORM | high | Templates de `$VTT_SETUP/03.templates/` se leen formalmente desde disco — prohibido hardcodear formato en scripts (f-strings con markdown). Origen: drift MS-290 vs MS-333 |

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
| `VTT.PROTOCOL-GOV-002` | Gobierno editorial de `virtual-teams-setup` (Fase de Desarrollo) | `02.normativa/01.Protocols/VTT.PROTOCOL-GOV-002_gobierno_edicion_vtt_setup_fase_desarrollo.md` | ✅ Nuevo (2026-05-17) |
| `VTT.PROTOCOL-ASG-001` | Ciclo de asignación y cierre de tarea | `02.normativa/01.Protocols/VTT.PROTOCOL-ASG-001_ciclo_asignacion_tarea.md` | ✅ v1.5.0 (2026-05-22) — OLA 1 cierre MSG + §5.5.9 bifurca rechazo en feedback simple vs bug con tarea hija (invoca WORKFLOW-ASG-001.030) |
| `VTT.PROTOCOL-MAN-001` | Gobernanza del Manifest (Task + Execution) | `02.normativa/01.Protocols/VTT.PROTOCOL-MAN-001_gobernanza_manifest.md` | ✅ Nuevo (2026-05-17) |
| `VTT.PROTOCOL-WT-001` | Gobernanza de Worktrees por rol | `02.normativa/01.Protocols/VTT.PROTOCOL-WT-001_gobernanza_worktrees.md` | ✅ Nuevo (2026-05-18) v1.0.1 |
| `VTT.PROTOCOL-DEV-001` | **Ciclo de vida del Devlog Entry** (creación → Review Gate → review → cierre de sprint) | `02.normativa/01.Protocols/VTT.PROTOCOL-DEV-001_ciclo_devlog_entry.md` | ✅ v1.1.0 (2026-06-10) — bump por TW-OPS (VTS-051) sobre validación VTS-026: §0 matriz 4 entidades D-61/D-62, §3.1 ampliada a 12 categorías del catálogo vivo, T2 BY-DESIGN documentado + workaround §5.3.5, §5.5 nueva "Crear Fix Task — trazabilidad vs bloqueo" + flujo manual T3, R13 (DEV-003 nunca para status), R14 (preservar referencia en deferred), §5.6 mapa de gates D-65, D-63 findings bloquean gate, D-64 elevación a TI. Origen: feature DEVLOG_LIFECYCLE v1.1; orquesta DEV-001..005 |
| `VTT.PROTOCOL-REVMA-001` | **Ciclo de Revisión Multi-Agente.** Transversal — invocado por todos los Protocols del upstream. PM Revisor (modelo distinto) audita docs producidos por agentes generadores. Máx 3 vueltas por documento. Backfeed obligatorio si downstream rompe upstream. Política "corregir local vs devolver" con 5 criterios. | `02.normativa/01.Protocols/VTT.PROTOCOL-REVMA-001_ciclo_revision_multiagente.md` | ✅ Nuevo (2026-05-31) v1.0.0 — Por TW-OPS |
| `VTT.PROTOCOL-PT-001` | **Generación del Paquete Técnico Base** (3B.1..3B.8). Ownership único por doc, tabla maestra de producción con inputs/colaboradores/función, orden de dependencias (3B.1 raíz), paralelismo desde 3B.4 aprobado, cross-check de coherencia cruzada antes de entregar al TL para `IPL-001`. | `02.normativa/01.Protocols/VTT.PROTOCOL-PT-001_generacion_paquete_tecnico.md` | ✅ Nuevo (2026-05-31) v1.0.0 — Por TW-OPS |
| `VTT.PROTOCOL-OB-001` | **Onboarding de Feature en Sistema Operando.** Variante de `PT-001` para features dentro de repos con código vivo. 2 pistas paralelas: (A) diseño delta desde SPEC, (B) estado actual del repo citando archivos/líneas. Resolución de drift SPEC vs Repo. Inversión única amortizada en docs `*_actual_*`. | `02.normativa/01.Protocols/VTT.PROTOCOL-OB-001_onboarding_feature_sistema_operando.md` | ✅ Nuevo (2026-05-31) v1.0.0 — Por TW-OPS |
| `VTT.PROTOCOL-IPL-001` | **Consolidación del Implementation Plan** (3B.9 + Routing Index). 10 sub-docs: 3B.9.3 PIVOTE + 4 derivados directos + 4 derivados compuestos + 3B.9.1 síntesis final. Separación matemática de esfuerzos (5 categorías), trazabilidad obligatoria de ✅/⚪/❌, cobertura 100% del Routing Index. Modo modular y consolidado válidos. | `02.normativa/01.Protocols/VTT.PROTOCOL-IPL-001_consolidacion_implementation_plan.md` | ✅ Nuevo (2026-05-31) v1.0.0 — Por TW-OPS |
| `VTT.PROTOCOL-HOPJM-001` | **Generación del Handoff Maestro PM → PJM.** 7 fases con bucles, 16 secciones obligatorias del HO, modos modular/consolidado del paquete técnico, Routing Index obligatorio, separación matemática de esfuerzos, clasificación P0/GATE/DIFERIDO de insumos PM, ownership separado (owner primario + ejecutor + colaboradores), addendums con triage administrativo/técnico, DoD como resumen operativo no duplicado del Routing Index. | `02.normativa/01.Protocols/VTT.PROTOCOL-HOPJM-001_generacion_ho_pm_pjm_v2.0.1.md` | ✅ v2.0.1 (2026-05-30) — Por TW-OPS, aprobado por PM Revisor |
| `VTT.PROTOCOL-SPRINT-001` | **Generación del trío de documentos por sprint** (SETUP + HANDOFF_TL + CLOSURE). PJM produce por sprint. HANDOFF_TL §7 referencia Routing Index del paquete técnico (no duplica). Aplicabilidad declarada explícita en §0 (DL si FE, QA si QA), firmas condicionales correctas (TL/AR/QA/DL nivel sprint, PJM/PM/STAKEHOLDER nivel release). INDEX_PAQUETE_OPERATIVO obligatorio. | `02.normativa/01.Protocols/VTT.PROTOCOL-SPRINT-001_generacion_sprint_docs.md` | ✅ v2.0.0 (2026-05-30) — Por TW-OPS |
| `VTT.PROTOCOL-PRE-001` | **Preflight TL antes de Materializar.** Validación contractual del paquete operativo del PJM contra API real del backend antes de cualquier escritura en VTT. 5 secciones de validación obligatoria (Acceso/Topología, Contrato API, IDs/Catálogos, Seguridad/Prerrequisitos, Grafo, QA/Firmas). Dictamen: GO / GO local / NO-GO devolución / Suspensión. Política de corrección local con 6 criterios obligatorios. | `02.normativa/01.Protocols/VTT.PROTOCOL-PRE-001_preflight_tl.md` | ✅ Nuevo (2026-05-31) v1.0.0 — Por TW-OPS |
| `VTT.PROTOCOL-MAT-001` | **Materialización en VTT.** Pipeline de 8 scripts secuenciales (idempotentes y reanudables): Phase+Release+Sprints+Deliveries → Tasks → TIs → Vínculos → CAs → Dependencias → Auditoría grafo → Cierre SETUP. CONTEXTO poblado con UUIDs reales. REPORTE_MATERIALIZACION_TL para sign-off PM. Cierre formal del upstream — downstream (`ASG-001`) arranca tras aprobación PM. | `02.normativa/01.Protocols/VTT.PROTOCOL-MAT-001_materializacion_vtt.md` | ✅ Nuevo (2026-05-31) v1.0.0 — Por TW-OPS |
| `VTT.PROTOCOL-ISS-001` | Proceso de Issue y on_hold | `07.Normativa/01.Protocols/VTT.PROTOCOL-ISS-001_*.md` | ⚪ Pendiente |

### Meta-índices (gobernanza de nomenclatura + filesystem)

| Documento | Path canónico | Propósito | Estado |
|---|---|---|---|
| `00_REGISTRO_ACRONIMOS.md` | `02.normativa/00_REGISTRO_ACRONIMOS.md` | Source of Truth de acrónimos `<CAT>` + convenciones de branch Git §3.bis | ✅ Activo (2026-05-18) v1.2 |
| `00_CONVENCIONES_FILESYSTEM.md` | `02.normativa/00_CONVENCIONES_FILESYSTEM.md` | Estructura obligatoria de carpetas en todo proyecto VTT (`knowledge/agent-tasks/...`, `task-manifests/`, etc.) + variable `$VTT_SETUP` | ✅ Nuevo (2026-05-18) v1.0 |

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
| `VTT.WORKFLOW-ASG-001.014` | Actualizar manifest a v1.5 | DEPRECADO — reemplazado por `VTT.WORKFLOW-MAN-001.004` | 🟤 Deprecado (2026-05-17) |
| `VTT.WORKFLOW-ASG-001.015` | Firma de stage development | `07.Normativa/02.Workflows/` | ⚪ Pendiente — §5.6.2 |
| `VTT.WORKFLOW-ASG-001.016` | Cierre de sprint CLOSURE | `07.Normativa/02.Workflows/` | ⚪ Pendiente — §5.6.5 |
| `VTT.WORKFLOW-ASG-001.017` | Revisar Living Documents impactados | `07.Normativa/02.Workflows/` | ⚪ Pendiente — §5.3.5 |
| `VTT.WORKFLOW-ASG-001.018` | Registrar Document Impacts | `07.Normativa/02.Workflows/` | ⚪ Pendiente — §5.3.6 |
| `VTT.WORKFLOW-ASG-001.019` | Ejecutar Hardcode Check | `07.Normativa/02.Workflows/` | ⚪ Pendiente — §5.3.7 |
| `VTT.WORKFLOW-ASG-001.020` | Verificar worktree por rol del agente | `07.Normativa/02.Workflows/` | ⚪ Pendiente — §5.2.10 |
| `VTT.WORKFLOW-ASG-001.021` | Generar execution_manifest.json | DEPRECADO — reemplazado por `VTT.WORKFLOW-MAN-001.001` | 🟤 Deprecado (2026-05-17) |
| `VTT.WORKFLOW-ASG-001.022` | Agente lee execution_manifest y verifica allowedPaths | DEPRECADO — reemplazado por `VTT.WORKFLOW-MAN-001.002` | 🟤 Deprecado (2026-05-17) |
| `VTT.WORKFLOW-ASG-001.023` | Verificar disciplina de worktree (TL Reviewer Paso 4b) | `07.Normativa/02.Workflows/` | ⚪ Pendiente — §5.5.5.b |
| `VTT.WORKFLOW-ASG-001.024` | Cleanup branch local post-aprobación (Paso 9) | `07.Normativa/02.Workflows/` | ⚪ Pendiente — §5.5.18 |
| `VTT.WORKFLOW-ASG-001.030` | **Manejo de Bugs detectados en Code Review** — crear tarea hija + padre on_hold + ciclo bug-fix-release | `02.normativa/02.Workflows/VTT.WORKFLOW-ASG-001.030_manejo_bugs_en_review.md` | ✅ v1.0.0 (2026-05-22) — invocado por PROTOCOL-ASG-001 §5.5.9. Origen: `GUIA_MANEJO_BUGS_TL.md` legacy memory-service. Pendiente promover `crear_tarea_bug.py` → `VTT.SCRIPT-ASG-001` |

### Workflows de PROTOCOL-MAN-001 (Gobernanza del Manifest)

| Código | Título | Path canónico | Estado |
|---|---|---|---|
| `VTT.WORKFLOW-MAN-001.001` | Generar Execution Manifest (TL al asignar) | `02.normativa/02.Workflows/VTT.WORKFLOW-MAN-001.001_generar_execution_manifest.md` | ✅ Nuevo (2026-05-17) — invocado por PROTOCOL-MAN-001 §5.1.2 (y PROTOCOL-ASG-001 §5.2.11) |
| `VTT.WORKFLOW-MAN-001.002` | Leer Execution Manifest (agente al iniciar) | `02.normativa/02.Workflows/VTT.WORKFLOW-MAN-001.002_leer_execution_manifest.md` | ✅ Nuevo (2026-05-17) — invocado por PROTOCOL-MAN-001 §5.2.1 (y PROTOCOL-ASG-001 §5.3.2.b) |
| `VTT.WORKFLOW-MAN-001.003` | Generar Task Manifest v1.0 (agente al cerrar) | `02.normativa/02.Workflows/VTT.WORKFLOW-MAN-001.003_generar_task_manifest_v10.md` | ✅ Activo v1.1.0 (2026-05-18) — Paso 12 commit del manifest al PR. Invocado por PROTOCOL-MAN-001 §5.3.2 |
| `VTT.WORKFLOW-MAN-001.004` | Actualizar Task Manifest v1.5 (TL al cerrar review) | `02.normativa/02.Workflows/VTT.WORKFLOW-MAN-001.004_actualizar_task_manifest_v15.md` | ✅ Activo v1.1.0 (2026-05-18) — Pasos 12-14 branch TL + PR. Invocado por PROTOCOL-MAN-001 §5.4.3 |
| `VTT.WORKFLOW-MAN-001.005` | Actualizar Task Manifest v2.0 (PM aprobación terminal) | reservado | ⚪ Pendiente — PROTOCOL-MAN-001 §5.5 futuro |

### Workflows de PROTOCOL-WT-001 (Gobernanza de Worktrees)

| Código | Título | Path canónico | Estado |
|---|---|---|---|
| `VTT.WORKFLOW-WT-001.001` | Setup inicial (one-time) — N worktrees + workspaces | `02.normativa/02.Workflows/VTT.WORKFLOW-WT-001.001_setup_inicial.md` | ✅ Nuevo (2026-05-18) — invocado por PROTOCOL-WT-001 §5.1 |
| `VTT.WORKFLOW-WT-001.002` | Apertura de sesión diaria | `02.normativa/02.Workflows/VTT.WORKFLOW-WT-001.002_apertura_sesion_diaria.md` | ✅ Nuevo (2026-05-18) — invocado por PROTOCOL-WT-001 §5.2 |
| `VTT.WORKFLOW-WT-001.003` | Agregar worktree de rol nuevo (bajo demanda) | `02.normativa/02.Workflows/VTT.WORKFLOW-WT-001.003_agregar_rol.md` | ✅ Nuevo (2026-05-18) — invocado por PROTOCOL-WT-001 §5.3 |
| `VTT.WORKFLOW-WT-001.004` | Casos especiales (multi-repo / branch dependiente / pausar / recovery) | `02.normativa/02.Workflows/VTT.WORKFLOW-WT-001.004_casos_especiales.md` | ✅ Nuevo (2026-05-18) — invocado por PROTOCOL-WT-001 §5.4 |
| `VTT.WORKFLOW-WT-001.005` | Cleanup final del proyecto | `02.normativa/02.Workflows/VTT.WORKFLOW-WT-001.005_cleanup_final.md` | ✅ Nuevo (2026-05-18) — invocado por PROTOCOL-WT-001 §5.5 |

> **Nota:** los Workflows nacen cuando se genera su Protocol padre. No hay Workflows huérfanos.

---

## 5. Nivel 2 — Skills

> Modelo Operativo VTT — Nivel 2 (capacidades reusables parametrizadas).

### Path canónico de skills

```
$VTT_NORMATIVA/06.Skills/  (path actual — se moverá a 07.Normativa/03.Skills/ en migración)
```

### Catálogo completo

#### Categoría MAN (Manifest) — versionadas VTT.SKILL-*

| Código | Título | Path | Estado |
|---|---|---|---|
| `VTT.SKILL-MAN-001` | Task Manifest (generar/validar/subir) — v1.0 agente y v1.5 TL | `02.normativa/03.Skills/manifest/VTT.SKILL-MAN-001_task_manifest.md` | ✅ Nuevo (2026-05-17) |
| `VTT.SKILL-EXM-001` | Execution Manifest (generar/leer) | `02.normativa/03.Skills/manifest/VTT.SKILL-EXM-001_execution_manifest.md` | ✅ Nuevo (2026-05-17) |

#### Categoría WT (Worktree) — versionadas VTT.SKILL-*

| Código | Título | Path | Estado |
|---|---|---|---|
| `VTT.SKILL-WT-001` | Operaciones de worktree (add/remove/list/verify_status/close_branch/archive) | `02.normativa/03.Skills/worktree/VTT.SKILL-WT-001_operaciones_worktree.md` | ✅ Nuevo (2026-05-18) |
| `VTT.SKILL-WT-002` | Generar workspace VSCode | `02.normativa/03.Skills/worktree/VTT.SKILL-WT-002_workspace_vscode.md` | ✅ Nuevo (2026-05-18) |

#### Categoría AUTH

| Código | Título | Path | Estado |
|---|---|---|---|
| `VTT.SKILL-AUTH-001` | Obtener JWT de sesión | `02.normativa/03.Skills/auth/VTT.SKILL-AUTH-001_obtener_jwt.md` | ✅ Nuevo (2026-05-19) |

#### Categoría TASK (gestión de tareas)

| Código | Título | Path | Estado |
|---|---|---|---|
| `VTT.SKILL-TASK-001` | Crear tarea en VTT | `02.normativa/03.Skills/task/VTT.SKILL-TASK-001_crear_tarea.md` | ✅ Nuevo (2026-05-19) |
| `VTT.SKILL-TASK-002` | Generar ASSIGNMENT | `02.normativa/03.Skills/task/VTT.SKILL-TASK-002_generar_assignment.md` | ✅ Nuevo (2026-05-19) |
| `VTT.SKILL-TASK-003` | Asignar tarea a agente | `02.normativa/03.Skills/task/VTT.SKILL-TASK-003_asignar_tarea.md` | ✅ Nuevo (2026-05-19) |
| `VTT.SKILL-TASK-004` | Mensaje al agente | `02.normativa/03.Skills/task/VTT.SKILL-TASK-004_mensaje_agente.md` | ✅ Nuevo (2026-05-19) |
| `VTT.SKILL-TASK-005` | Review de tarea | `02.normativa/03.Skills/task/VTT.SKILL-TASK-005_review_tarea.md` | ✅ Nuevo (2026-05-19) |

#### Categoría STATUS (transiciones de estado)

| Código | Título | Path | Estado |
|---|---|---|---|
| `VTT.SKILL-STATUS-001` | Mover a `task_in_progress` | `02.normativa/03.Skills/status/VTT.SKILL-STATUS-001_task_in_progress.md` | ✅ Nuevo (2026-05-19) |
| `VTT.SKILL-STATUS-002` | Mover a `task_in_review` | `02.normativa/03.Skills/status/VTT.SKILL-STATUS-002_task_in_review.md` | ✅ Nuevo (2026-05-19) |
| `VTT.SKILL-STATUS-003` | Mover a `task_completed` (TL) | `02.normativa/03.Skills/status/VTT.SKILL-STATUS-003_task_completed.md` | ✅ Nuevo (2026-05-19) |
| `VTT.SKILL-STATUS-004` | Mover a `task_approved` (PM) | `02.normativa/03.Skills/status/VTT.SKILL-STATUS-004_task_approved.md` | ✅ Nuevo (2026-05-19) |
| `VTT.SKILL-STATUS-005` | Mover a `task_on_hold` (endpoint dedicado) | `02.normativa/03.Skills/status/VTT.SKILL-STATUS-005_task_on_hold.md` | ✅ Nuevo (2026-05-19) |
| `VTT.SKILL-STATUS-006` | Mover a `task_rejected` (PM) | `02.normativa/03.Skills/status/VTT.SKILL-STATUS-006_task_rejected.md` | ✅ Nuevo (2026-05-19) |

#### Categoría QUERY (consultas de lectura)

| Código | Título | Path | Estado |
|---|---|---|---|
| `VTT.SKILL-QUERY-001` | Mis tareas asignadas | `02.normativa/03.Skills/query/VTT.SKILL-QUERY-001_mis_tareas.md` | ✅ Nuevo (2026-05-19) |
| `VTT.SKILL-QUERY-002` | Tareas en revisión del proyecto | `02.normativa/03.Skills/query/VTT.SKILL-QUERY-002_tareas_en_revision.md` | ✅ Nuevo (2026-05-19) |
| `VTT.SKILL-QUERY-003` | Detalle completo de una tarea (6 sub-opciones) | `02.normativa/03.Skills/query/VTT.SKILL-QUERY-003_detalle_tarea.md` | ✅ Nuevo (2026-05-19) |
| `VTT.SKILL-QUERY-004` | Avance por fases del proyecto | `02.normativa/03.Skills/query/VTT.SKILL-QUERY-004_avance_fases.md` | ✅ Nuevo (2026-05-19) |
| `VTT.SKILL-QUERY-005` | Estado de fase: qué tareas son asignables | `02.normativa/03.Skills/query/VTT.SKILL-QUERY-005_estado_fase_asignable.md` | ✅ Nuevo (2026-05-19) |

#### Categoría COMMENT

| Código | Título | Path | Estado |
|---|---|---|---|
| `VTT.SKILL-COMMENT-001` | Postear comentario genérico | `02.normativa/03.Skills/comment/VTT.SKILL-COMMENT-001_comentario_generico.md` | ✅ Nuevo (2026-05-19) |
| `VTT.SKILL-COMMENT-002` | APR-PM (aprobación funcional) | `02.normativa/03.Skills/comment/VTT.SKILL-COMMENT-002_apr_pm.md` | ✅ Nuevo (2026-05-19) |
| `VTT.SKILL-COMMENT-003` | APR-TL (aprobación técnica) | `02.normativa/03.Skills/comment/VTT.SKILL-COMMENT-003_apr_tl.md` | ✅ Nuevo (2026-05-19) |

#### Categoría DEV (Devlog entries)

| Código | Título | Path | Estado |
|---|---|---|---|
| `VTT.SKILL-DEV-001` | Registrar decisión en devlog | `02.normativa/03.Skills/dev/VTT.SKILL-DEV-001_decision.md` | ✅ v1.1 (2026-05-22) — fixes BE: wrapper entries[], description obligatorio |
| `VTT.SKILL-DEV-002` | Registrar observación en devlog | `02.normativa/03.Skills/dev/VTT.SKILL-DEV-002_observacion.md` | ✅ v1.1 (2026-05-20) — mismo fix de wrapper |
| `VTT.SKILL-DEV-003` | **Editar campos genéricos de un devlog entry** (PATCH `/devlog/:entryId`) | `02.normativa/03.Skills/dev/VTT.SKILL-DEV-003_edit_devlog.md` | ✅ v1.0 (2026-05-22) — spec del BE |
| `VTT.SKILL-DEV-004` | **Lifecycle del devlog entry** (PATCH `/devlog/:entryId/status` — estados finales irreversibles) | `02.normativa/03.Skills/dev/VTT.SKILL-DEV-004_lifecycle_devlog.md` | ✅ v1.0 (2026-05-22) — spec del BE |
| `VTT.SKILL-DEV-005` | **Eliminar devlog entry** (DELETE `/devlog/:entryId` — destructivo, irreversible, sin soft-delete ni audit log) | `02.normativa/03.Skills/dev/VTT.SKILL-DEV-005_delete_devlog.md` | ✅ v1.0 (2026-05-22) — spec del BE; incluye receta batch |

#### Categoría ISS (Issues)

| Código | Título | Path | Estado |
|---|---|---|---|
| `VTT.SKILL-ISS-001` | Crear issue/blocker en tarea | `02.normativa/03.Skills/iss/VTT.SKILL-ISS-001_crear_issue.md` | ✅ Nuevo (2026-05-19) |

#### Categoría ATTACH

| Código | Título | Path | Estado |
|---|---|---|---|
| `VTT.SKILL-ATTACH-001` | Subir archivo (skill base de attachments) | `02.normativa/03.Skills/attach/VTT.SKILL-ATTACH-001_subir_archivo.md` | ✅ Nuevo (2026-05-19) |
| `VTT.SKILL-ATTACH-002` | Subir devlog del cierre | `02.normativa/03.Skills/attach/VTT.SKILL-ATTACH-002_subir_devlog.md` | ✅ Nuevo (2026-05-19) |

#### Categoría GIT

| Código | Título | Path | Estado |
|---|---|---|---|
| `VTT.SKILL-GIT-001` | Crear branch estructurado verificable contra patrón (gobernanza editorial) | `02.normativa/03.Skills/git/VTT.SKILL-GIT-001_crear_branch_estructurado.md` | ✅ Activo (2026-05-17) |
| `VTT.SKILL-GIT-002` | Commit estructurado verificable contra schema (gobernanza editorial) | `02.normativa/03.Skills/git/VTT.SKILL-GIT-002_commit_estructurado.md` | ✅ Activo (2026-05-17) |
| `VTT.SKILL-GIT-003` | Crear branch de tarea `feature/<TASK_ID>` (operación PROTOCOL-ASG) | `02.normativa/03.Skills/git/VTT.SKILL-GIT-003_crear_branch_tarea.md` | ✅ Nuevo (2026-05-19) |
| `VTT.SKILL-GIT-004` | Rebase con main antes de PR | `02.normativa/03.Skills/git/VTT.SKILL-GIT-004_rebase_main.md` | ✅ Nuevo (2026-05-19) |
| `VTT.SKILL-GIT-005` | Commit con formato del proyecto | `02.normativa/03.Skills/git/VTT.SKILL-GIT-005_commit_tarea.md` | ✅ Nuevo (2026-05-19) |
| `VTT.SKILL-GIT-006` | Crear PR con gh CLI | `02.normativa/03.Skills/git/VTT.SKILL-GIT-006_crear_pr.md` | ✅ Nuevo (2026-05-19) |

#### Categoría REPORT

| Código | Título | Path | Estado |
|---|---|---|---|
| `VTT.SKILL-REPORT-001` | Reporte de entrega de tarea (SKL-REPORT-01) | `02.normativa/03.Skills/report/VTT.SKILL-REPORT-001_entrega_tarea.md` | ✅ v1.1 (2026-05-22) — OLA 1 cierre MSG: R6 path nuevo `knowledge/task-manifests/` + R7 render obligatorio en pantalla (políticas I2/I3 del template v2.1) |
| `VTT.SKILL-PRECHECK-001` | **Validar entorno antes de iniciar tarea** (5 checks: $VTT_SETUP, scripts canónicos, NO copias locales, worktree, $TOKEN) | `02.normativa/03.Skills/precheck/VTT.SKILL-PRECHECK-001_validar_entorno_inicio_tarea.md` | ✅ v1.0 (2026-05-22) — invocada como Paso 0 obligatorio antes de tocar código |
| `VTT.SKILL-REPORT-002` | Reporte ejecutivo PJM al PM | `02.normativa/03.Skills/report/VTT.SKILL-REPORT-002_reporte_pjm.md` | ✅ Nuevo (2026-05-19) |

#### Categoría FILE

| Código | Título | Path | Estado |
|---|---|---|---|
| `VTT.SKILL-FILE-001` | Ubicar entregable en estructura del proyecto | `02.normativa/03.Skills/file/VTT.SKILL-FILE-001_ubicar_entregable.md` | ✅ Nuevo (2026-05-19) |

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
| `VTT.SCRIPT-GIT-001` | Validar branch y mensaje de commit contra config de gobernanza | `02.normativa/04.Scripts/git/VTT.SCRIPT-GIT-001_validate_branch_and_commit.py` | ✅ Nuevo (2026-05-17) |
| `VTT.SCRIPT-MAN-001` | `gen_task_manifest.py` — Task Manifest schema v1.2 (v1.0 agente y v1.5 TL) | `02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py` | ✅ v1.3 (2026-05-18) + enforcement RULE-SCRIPT-001 agregado 2026-05-22 (aborta si se ejecuta desde copia local) |
| `VTT.SCRIPT-MSG-001` | `gen_mensaje.py` refactorizado — Generador del mensaje de asignación, lee template formalmente, 3 modos (`--post` / `--output` / `--validate`) | `02.normativa/04.Scripts/msg/VTT.SCRIPT-MSG-001_gen_mensaje.py` | ✅ v1.0 (2026-05-22) — refactor MS-328. Aplica RULE-SCRIPT-001 (enforcement runtime) y RULE-TEMPLATE-001 (lectura formal). Fixes: regex non-greedy + FP B5 (PM 2026-05-22) |
| `VTT.SCRIPT-ASG-001` | `crear_tarea_bug.py` — Automatiza pasos 4a-4i del WORKFLOW-ASG-001.030 (crear tarea hija de bug + asignar agente + subir ASSIGNMENT + CAs + bug entry en padre + dependency + on_hold + mensaje) | `02.normativa/04.Scripts/asg/VTT.SCRIPT-ASG-001_crear_tarea_bug.py` | ✅ v1.0 (2026-05-22) — promovido desde memory-service worktree. Aplica RULE-SCRIPT-001 (enforcement runtime). Deuda pendiente: modo `--validate`, lectura formal TEMPLATE_ASSIGNMENT |
| `VTT.SCRIPT-EXM-001` | `gen_execution_manifest.py` — Execution Manifest v1.0 (generar/leer) | `02.normativa/04.Scripts/manifest/VTT.SCRIPT-EXM-001_gen_execution_manifest.py` | ✅ Nuevo (2026-05-17) |
| `VTT.SCRIPT-WT-001` | `setup_worktrees.py` — Setup inicial bulk (N worktrees + workspaces) | `02.normativa/04.Scripts/worktree/VTT.SCRIPT-WT-001_setup_worktrees.py` | ✅ Nuevo (2026-05-18) |
| `VTT.SCRIPT-WT-002` | `add_worktree.py` — Agregar UN worktree + workspace (rol nuevo o aux) | `02.normativa/04.Scripts/worktree/VTT.SCRIPT-WT-002_add_worktree.py` | ✅ Nuevo (2026-05-18) |
| `VTT.SCRIPT-WT-003` | `cleanup_worktrees.py` — Cleanup final con 3 acciones A/B/C | `02.normativa/04.Scripts/worktree/VTT.SCRIPT-WT-003_cleanup_worktrees.py` | ✅ Nuevo (2026-05-18) |

> Config asociada (GIT-001): `02.normativa/04.Scripts/git/vtt_governance.example.json` (template a copiar en `.git/hooks/vtt_governance.json` por cada clone — ver `VTT.PROTOCOL-GOV-002` §5.0).

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
| `TEMPLATE_MENSAJE_ASIGNACION.md` v2.2 | `03.templates/tarea/` | Mensaje del TL al agente — incluye **Paso 0-A Pre-check obligatorio** (`VTT.SKILL-PRECHECK-001`) + Paso 0-B git + Working Directory condicional + I1/I2/I3 entrega + fix endpoint devlog. Aplica `RULE-SCRIPT-001`, `RULE-TEMPLATE-001`, `RULE-AGENT-001` | ✅ v2.2 (2026-05-22) — OLA 1 cierre MSG |
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
| ~~`GUIA_WORKTREES_MEMORY_SERVICE.md`~~ | v2.1 (FANTASMA) | NO existe en disco | 🔴 **Referencia fantasma** — archivo nunca se creó. Reemplazada por `VTT.PROTOCOL-WT-001` v1.0.1 (Protocol normativo). 25 referencias originales actualizadas en 2026-05-18. |
| `GUIA_GIT_WORKTREES_TL_BACKEND.md` | v2.0 (LEGACY) | `04.docs-soporte/guias-operativas/` | 🟤 **Deprecada** (2026-05-18). Reemplazada por `VTT.PROTOCOL-WT-001` v1.0.1. Se conserva como referencia histórica del incidente PROC-COORD-01. |
| `GUIA_ASIGNACION_TAREA_TL_EJECUTOR.md` | v2.1 | `06.Documentos_soporte/` | Cheatsheet TL al asignar — Paso 8.5 (execution_manifest) |
| `GUIA_REVISION_TAREA_TL_REVIEWER.md` | v2.1 | `06.Documentos_soporte/` | Cheatsheet TL al cerrar — Paso 5b + Paso 16 |
| `PROCESO_CIERRE_TAREA_v2.md` | v2.1 (header dice v2.0) | `06.Documentos_soporte/` | Paso 4b (verificación worktree) + Paso 9 (cleanup) |
| `PROCESO_ASIGNACION_TAREAS_v3.md` | v3.1 | `06.Documentos_soporte/` | Paso 7b (execution_manifest) |
| `GUIA_MANIFEST_PARA_AGENTES.md` | v2.0 | `06.Documentos_soporte/` | Manifest v1.0 generado por agente |
| `CLEANUP_COPIAS_LOCALES_SCRIPTS_OLA1.md` | v1.0 | `04.docs-soporte/guias-operativas/` | ✅ Nuevo (2026-05-22) — checklist one-shot del TL para eliminar las 5 copias divergentes de `gen_mensaje.py` + copias locales de `VTT.SCRIPT-MAN-001`. Aplica `RULE-SCRIPT-001`. Origen: drift MS-290 vs MS-333 |

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
| 22 | Deprecar GUIA_GIT_WORKTREES_TL_BACKEND.md (v2.0 legacy) | — | ✅ Completado (2026-05-18) — reemplazada por VTT.PROTOCOL-WT-001 |
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
| 1.2 | 2026-05-17 | Sub-sistema MANIFEST completo: `00_REGISTRO_ACRONIMOS.md` v1.0, `VTT.PROTOCOL-MAN-001`, 4 Workflows `VTT.WORKFLOW-MAN-001.001..004`, 2 Skills `VTT.SKILL-MAN-001` + `VTT.SKILL-EXM-001`, 2 Scripts `VTT.SCRIPT-MAN-001` + `VTT.SCRIPT-EXM-001`. Workflows legacy `ASG-001.014/.021/.022` marcados como `🟤 Deprecado`. GUIA_AUTOR y _autoria/README ahora apuntan al registro maestro. |
| 1.3 | 2026-05-18 | **Convenciones operativas universales.** Nuevo `00_CONVENCIONES_FILESYSTEM.md` v1.0 (estructura obligatoria de `knowledge/agent-tasks/{briefs,assignments,messages,reports}/<phase>/<sprint>/` + variable `$VTT_SETUP`). `TEMPLATE_MENSAJE_ASIGNACION.md` bumpeado a v2.0 (única plantilla con sección Working Directory condicional WT/no-WT, apunta al setup, incluye Paso 12 commit del manifest). Origen: drift de paths detectado en VTT-718 + necesidad de soportar proyectos con/sin worktrees. Script `VTT.SCRIPT-MAN-001` actualizado a v1.3 (Fix #8: re-indexación de TIs evidenciados). Protocol `VTT.PROTOCOL-ASG-001` v1.3.0 con FASE 4.5 (Commit del TL post-aprobación). |
| 1.4 | 2026-05-18 | **Sub-sistema WT completo.** Nuevo `VTT.PROTOCOL-WT-001` v1.0.1 (Gobernanza de Worktrees por rol). 5 Workflows derivados (`WT-001.001..005`): setup inicial, apertura diaria, agregar rol, casos especiales, cleanup final. 2 Skills (`SKILL-WT-001` operaciones worktree con 6 acciones, `SKILL-WT-002` workspace VSCode). 3 Scripts (`SCRIPT-WT-001` setup_worktrees.py, `SCRIPT-WT-002` add_worktree.py, `SCRIPT-WT-003` cleanup_worktrees.py). Categoría `WT` registrada como Activa en `00_REGISTRO_ACRONIMOS.md` v1.3. `GUIA_GIT_WORKTREES_TL_BACKEND.md` v2.0 marcada Deprecada — reemplazada por el Protocol. Origen: incidente PROC-COORD-01 (MS-286). |
| 1.5 | 2026-05-19 | **Migración masiva de skills legacy.** 32 skills `SKL-*` legacy en `_pending-migration/` migradas a formato VTT.SKILL en 11 categorías: AUTH(1), TASK(5), STATUS(6), QUERY(5), COMMENT(3), DEV(2), ISS(1), ATTACH(2), GIT(4 — renumeradas a 003..006), REPORT(2), FILE(1). Categorías activadas en `00_REGISTRO_ACRONIMOS.md` v1.4: AUTH, TASK, STATUS, COMMENT, DEV, ISS, ATTACH, FILE. Nuevas categorías registradas: QUERY, REPORT. **Total skills VTT activas: 38** (32 migradas hoy + 6 que ya existían: GIT-001/002, MAN-001, EXM-001, WT-001, WT-002). Todas las 33 legacies marcadas `🟤 Deprecada` con puntero al reemplazo. Correcciones aplicadas durante migración: bug `categoryCode` vs `type` en devlog, bug `severity null` (debe ser enum), comportamiento de issues + on_hold ahora documentado correctamente (NO automático). |
