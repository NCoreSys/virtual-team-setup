# IMPROVE-005 — Extensión del Modelo de Autorización a Recursos VTT-Específicos

| Campo | Valor |
|---|---|
| **Código** | `IMPROVE-005` |
| **Título** | Capabilities, Roles y Reglas para recursos nativos de VTT (TIs, Manifests, Devlogs, LDs, Evidencias) |
| **Categoría** | Backend / Authorization / VTT-Native Resources |
| **Prioridad** | 🟡 Media |
| **Estimación rough** | 5-7 días |
| **Estado** | Propuesta — pendiente de evaluación PM |
| **Autor** | PM Martin Rivas |
| **Fecha** | 2026-05-13 |
| **Origen** | Sesión de Normativa VTT — gap detectado en doc_sec_01..04 que no cubre recursos nativos VTT |
| **Depende de** | IMPROVE-004 (Rules Engine) |

---

## Relación con otras mejoras

- **IMPROVE-001 (Pool de Transacciones)**: complementaria — el pool valida estas nuevas capabilities/reglas antes de ejecutar operaciones.
- **IMPROVE-002 (BD de Manifiestos)**: complementaria directa — esta mejora protege el recurso `manifest` que IMPROVE-002 indexa.
- **IMPROVE-003 (Platform Gaps)**: independiente — esos son fixes API.
- **IMPROVE-004 (Rules Engine)**: **depende de**. Esta mejora extiende lo que el motor cubre. Sin Rules Engine no hay donde almacenar las nuevas capabilities/reglas.

---

## 1. Problema que resuelve

El Bloque 1 de autorización (`doc_sec_01..04`) define el modelo base con 30 capabilities + 9 roles, pero **solo cubre recursos genéricos del lifecycle de proyecto** (Task, Phase, Workspace, Delivery, Issue, Attachment, User, ChangeRequest, Signature).

**Faltan los recursos nativos de VTT** que en la práctica se usan a diario:

| Recurso VTT | ¿Está en doc_sec_01..04? | Status actual |
|---|---|---|
| **TrackableItem** (RFs, ADRs, NFRs, BR, AS, US, UC, tech_debt) | ❌ no | Operativo en MS pero sin RBAC formal |
| **TrackableItem Evidence** | ❌ no | Operativo, sin policy |
| **Devlog Entry** | ❌ no | Operativo, sin policy de quien resuelve |
| **Manifest** (v1.0, v1.5) | ❌ no | Operativo, sin policy de quien genera |
| **Living Document** | ❌ no | Solo en SOP-LD-01 (operativo, no RBAC) |
| **Document Impact** | ❌ no | Operativo, sin policy |
| **Hardcode Check Finding** | ❌ no | Operativo, sin policy |
| **Sprint** / **Release** | Parcial | Existen en VTT, no aparecen como recursos protegidos |
| **Deliverable** (catálogo SDLC — 438 items) | ❌ no | Solo en `deliverables_catalog.json` |
| **Rule** (este nuevo recurso introducido por IMPROVE-004) | ❌ no | Aplica a sí mismo |

### Consecuencias actuales

- Cualquier agente con `tasks.update` puede manipular TIs, evidencias, devlogs (no hay capability separada)
- No hay regla "solo TL puede generar manifest v1.5"
- No hay regla "evidencia debe tener marker `[TASK:MS-XXX]`" como policy enforceable
- No hay regla "Living Document modificado → declarar Document Impact"
- Difícil reportar "qué agentes están violando qué reglas en qué recursos"

## 2. Impacto / valor que aporta

### Cuantitativo
- **+25-30 capabilities nuevas** específicas de VTT (cubren los recursos faltantes)
- **+15-20 reglas operativas** que hoy viven solo en SOPs (modelo dinámico, LDs, etc.) se vuelven enforceable
- **0 violaciones silenciosas** de policies VTT-específicas

### Cualitativo
- **El modelo de Reglas (IMPROVE-004) tiene cobertura completa** sobre todos los recursos VTT
- **Auditoría** completa de quién hizo qué sobre cada recurso (no solo Task/Phase/Workspace)
- **Reportes** "% tareas con manifest v1.5 generado por TL correcto", "% TIs con evidencias con marker correcto", etc.

## 3. Solución propuesta

### 3.1 Nuevas capabilities (extensión del catálogo de 30 → ~55)

**Grupo nuevo: VTT-TRACKING** (TrackableItems)

```
trackable_items.read
trackable_items.create
trackable_items.update
trackable_items.delete
trackable_items.link_task        (vincular TI a tarea)
trackable_items.unlink_task
trackable_items.defer            (marcar [DEFER R2])
trackable_items.approve          (cambiar status a ti_approved)
evidence.create                  (POST /trackable-items/:id/evidence)
evidence.read
evidence.delete                  (cuando exista — ver GAP-VTT-03)
```

**Grupo nuevo: VTT-DEVLOG**

```
devlog.create
devlog.read
devlog.update
devlog.resolve                   (PATCH status=resolved con resolution)
devlog.defer                     (status=deferred)
```

**Grupo nuevo: VTT-MANIFEST**

```
manifest.generate_v1             (agente genera v1.0)
manifest.generate_v15            (TL genera v1.5)
manifest.read
manifest.update
```

**Grupo nuevo: VTT-DOCS** (Living Documents + Document Impacts)

```
living_documents.read
living_documents.update
living_documents.declare_no_change
document_impacts.create
document_impacts.read
```

**Grupo nuevo: VTT-FINDINGS** (Hardcode Check + otros)

```
findings.create
findings.read
findings.resolve
findings.justify_false_positive
```

**Grupo nuevo: VTT-SPRINT-RELEASE**

```
sprints.read
sprints.create
sprints.sign                     (firma de stage del sprint)
releases.read
releases.create
releases.sign
```

**Grupo nuevo: VTT-RULES** (meta-capabilities sobre el sistema de Rules)

```
rules.read
rules.create                     (PM crea reglas)
rules.update
rules.deactivate
rule_violations.read
```

### 3.2 Nuevas reglas operativas (extensión del catálogo de 43 → ~65)

Cubren los recursos nuevos. Ejemplos:

| Code | Title | Scope | Notas |
|---|---|---|---|
| RULE-TI-001 | Crear TI nuevo: requiere link a tarea o ADR | TASK | `trackable_items.create` |
| RULE-TI-002 | Marker `[DEFER R2]` obligatorio en TIs diferidos | TASK | mandatory |
| RULE-TI-003 | typeCode=process_improvement no válido en software (workaround `tech_debt`+marker) | PLATFORM | Workaround actual |
| RULE-EVD-001 | Evidence: marker `[TASK:MS-XXX] [SPRINT:SX]` obligatorio | PHASE 04 | auto_detect |
| RULE-EVD-002 | URL de evidencia debe ser PR específico (no URL base) | PHASE 04 | manual |
| RULE-DEV-001 | Resolver devlog: `resolution` obligatorio cuando status=resolved | PLATFORM | auto_detect |
| RULE-DEV-002 | Solo TL resuelve devlog del agente que entrega | ROLE | sod |
| RULE-MAN-001 | Manifest v1.0 = generado por agente al entregar | PHASE 04 | quien |
| RULE-MAN-002 | Manifest v1.5 = generado por TL al cerrar | PHASE 04 | quien |
| RULE-MAN-003 | Manifest generado AL FINAL (no antes de attachments + status) | PHASE 04 | PROC-MANIFEST-01 |
| RULE-LD-001 | Tarea que toca LD → declarar update o "sin cambios" | TASK | mandatory |
| RULE-LD-002 | LD-15 (server_specs) → solo DO actualiza | TASK | role-bound |
| RULE-FIND-001 | Hardcode Check critical/high pendiente bloquea Review Gate | TASK | blocks_review_gate |
| RULE-FIND-002 | False Positive de hardcode requiere justificación en devlog | TASK | mandatory |
| RULE-RULE-001 | Solo PM/TL crea reglas (rules.create) | ROLE | meta |
| RULE-RULE-002 | Regla con scope=PLATFORM requiere aprobación PM | PLATFORM | sensitive |

### 3.3 Nuevos campos en matriz RBAC

La matriz `role_capabilities` se extiende con las ~25 nuevas capabilities. Por defecto:

| Capability | Quién la tiene |
|---|---|
| `trackable_items.read` | Todos los workspace roles |
| `trackable_items.create` | ws_tech_lead + ws_lead |
| `trackable_items.approve` | org_owner (humano) |
| `evidence.create` | ws_tech_lead (al cerrar tarea) |
| `manifest.generate_v1` | ws_developer (en su tarea) |
| `manifest.generate_v15` | ws_tech_lead |
| `living_documents.update` | ws_tech_lead + role específico del LD |
| `findings.resolve` | ws_tech_lead + ws_reviewer |
| `findings.justify_false_positive` | ws_developer (con devlog) |
| `rules.create` | org_owner + ws_tech_lead (con restricciones por scope) |

### 3.4 Schema extensiones (sobre IMPROVE-004)

```sql
-- No requiere tablas nuevas, solo seed adicional
INSERT INTO capabilities (code, group_code, title, description, abac_required, ...) VALUES
  ('trackable_items.read', 'vtt_tracking', 'Leer TIs', '...', true, ...),
  ('trackable_items.create', 'vtt_tracking', 'Crear TIs', '...', true, ...),
  -- ... 25 capabilities más
;

INSERT INTO role_capabilities (role_code, capability_code, abac_marker) VALUES
  ('ws_tech_lead', 'trackable_items.create', NULL),
  ('ws_developer', 'manifest.generate_v1', '*'),  -- solo en su tarea
  -- ... matriz completa
;

INSERT INTO rules (code, title, rule_text, scope_level, ...) VALUES
  ('RULE-EVD-001', 'Evidencia con marker [TASK:MS-XXX]', '...', 'PHASE', ...),
  -- ... 20 reglas más
;
```

### 3.5 Resolución (sin cambios sobre IMPROVE-004)

El motor de IMPROVE-004 maneja estas capabilities/reglas exactamente igual. Solo el catálogo crece.

## 4. Plan de implementación

### Fase 1 — Catálogo de capabilities extendido (2 días)
- Definir las ~25 capabilities VTT-específicas
- Documentar grupos: VTT-TRACKING, VTT-DEVLOG, VTT-MANIFEST, VTT-DOCS, VTT-FINDINGS, VTT-SPRINT-RELEASE, VTT-RULES
- Validar contra catálogo actual de doc_sec_02 (no duplicar)

### Fase 2 — Matriz RBAC extendida (1 día)
- Asignar las ~25 capabilities a los 9 roles
- Documentar ABAC markers donde aplique

### Fase 3 — Reglas operativas VTT-específicas (2 días)
- Extraer reglas de:
  - `SOP-LD-01` (Living Documents)
  - `SOP-TRK-01/02` (TrackableItems)
  - `PROCESO_CIERRE_TAREA_v2` (modelo dinámico)
  - `TEMPLATE-APR-001`, `TEMPLATE-CFL-001`, `TEMPLATE-CLO-001`
  - Lecciones operativas (PROC-MANIFEST-01, PROC-COORD-01, etc.)

### Fase 4 — Seed + tests (2 días)
- Script seed que inserta capabilities/roles/rules nuevos
- Tests del motor de resolución con los nuevos casos
- Validar que `query_rules.py` los maneja sin cambios

**Total estimado:** 7 días

> **Implementación junto con IMPROVE-004:** la mejor estrategia. IMPROVE-005 es seed/datos sobre el schema de IMPROVE-004.

## 5. Riesgos / consideraciones

| Riesgo | Mitigación |
|---|---|
| Demasiadas capabilities → matriz inmanejable | Agrupación por dominio + UI con filtros |
| Conflicto entre reglas VTT-específicas y reglas Bloque 1 | Reglas VTT-específicas tienen scope más estrecho → tienen precedencia |
| Cambio de proceso operativo (ej. evolución de manifest a v2) | Versionado de reglas + grace period |
| Evolución del modelo de TI (typeCode=process_improvement futuro) | Agregar capability nueva sin romper existentes |
| Cobertura de los 438 deliverables del catálogo SDLC | Diferido a IMPROVE-006 (futuro) — esta mejora cubre solo recursos en uso activo |

## 6. Decisión solicitada al PM

1. **¿Aprobar como complemento de IMPROVE-004?** Recomendación: sí, implementar juntas.
2. **¿Las ~25 capabilities nuevas las acepto como propuesta inicial?** O quieres revisar/ajustar antes.
3. **¿Las ~20 reglas operativas nuevas las extraemos ahora** o esperamos a tener el motor en BD?
   - Recomendación: extraer ahora a JSON (extiende `rules_catalog.json`) para probar el modelo. Migrar a BD cuando IMPROVE-004 esté listo.
4. **¿Cobertura de los 438 deliverables del catálogo SDLC?** Posponer a IMPROVE-006 — escala muy grande para incluir aquí.

## 7. Recursos VTT cubiertos por esta mejora

```
✅ TrackableItem (todos los tipos: RF, ADR, NFR, BR, AS, US, UC, tech_debt, constraint, business_rule)
✅ TrackableItem Evidence
✅ Devlog Entry
✅ Manifest (v1.0 + v1.5)
✅ Living Document
✅ Document Impact
✅ Hardcode Check Finding
✅ Sprint (operaciones)
✅ Release (operaciones)
✅ Rule (meta-recurso)
✅ Rule Violation

⏳ Deliverable (438 items del catálogo SDLC) → diferido a IMPROVE-006
```

## 8. Referencias

- Documento padre: `IMPROVE-004_rules_como_feature_vtt.md`
- Fuentes de reglas operativas:
  - `00-platform/06.Documentos_soporte/SOP-LD-01_living_documents.md`
  - `00-platform/06.Documentos_soporte/SOP-TRK-01_trackable_items_workflow.md`
  - `00-platform/06.Documentos_soporte/SOP-TRK-02_dynamic_item_creation.md`
  - `memory-service-project/00-platform/06.Documentos_soporte/PROCESO_CIERRE_TAREA_v2.md`
  - `07.Normativa/06.Templates/VTT.TEMPLATE-APR-001_apr_tl_comment.md`
  - `07.Normativa/06.Templates/VTT.TEMPLATE-CFL-001_criteria_fulfillment.md`
  - `07.Normativa/06.Templates/VTT.TEMPLATE-CLO-001_closure_sprint.md`
  - Lecciones operativas: PROC-MANIFEST-01, PROC-COORD-01

## 9. Changelog

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-05-13 | Documento inicial — propuesta para evaluación PM |
