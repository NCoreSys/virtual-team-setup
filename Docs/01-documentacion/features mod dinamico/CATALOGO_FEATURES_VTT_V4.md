# CATÁLOGO DE FEATURES VTT V4
## Qué puedes hacer con el sistema hoy

**Versión:** 1.0  
**Fecha:** 2026-04-12  
**Estado:** ✅ Implementado (BE/DB listo, FE pendiente integración)

---

## RESUMEN EJECUTIVO

| Categoría | Features | Estado BE | Estado FE |
|-----------|----------|-----------|-----------|
| Catálogos Base | 4 | ✅ | ⚠️ Admin pendiente |
| Trazabilidad | 4 | ✅ | ⚠️ Pendiente |
| Devlog | 3 | ✅ | ⚠️ Pendiente |
| Documentos | 3 | ✅ | ⚠️ Pendiente |
| Criterios | 2 | ✅ | ⚠️ Pendiente |
| **Total** | **16** | ✅ | ⚠️ |

**Los agentes pueden usar TODAS las features vía API hoy.**

---

## 1. CATÁLOGOS DISPONIBLES

### 1.1 Catálogos que NECESITAN seed

| Catálogo | Tabla | ¿Tiene datos? | Acción |
|----------|-------|---------------|--------|
| Tipos de Criterio | `criteria_type_catalog` | ❌ VACÍO | Seed requerido |
| Categorías Devlog | `devlog_category_catalog` | ❌ VACÍO | Seed requerido |
| Tipos de Link | `link_type_catalog` | ❌ VACÍO | Seed requerido |
| Fuentes Living Doc | `living_doc_source_catalog` | ❌ VACÍO | Seed requerido |

### 1.2 Catálogos que ya tienen datos

| Catálogo | Tabla | Estado |
|----------|-------|--------|
| Status | `status_catalog` | ✅ Tiene datos |
| Prioridades | `priority_catalog` | ✅ Tiene datos |
| Tipos de Entidad | `entity_type_catalog` | ✅ Tiene datos |
| Tipos de Documento | `document_type_catalog` | ✅ Tiene datos |
| Tipos de Archivo | `file_type_catalog` | ✅ Tiene datos |

---

## 2. FEATURES DE TRAZABILIDAD

### 2.1 Links entre Tasks (TrackableItemLink)

**Qué hace:** Vincular tareas entre sí con relación tipada.

**Tipos de link disponibles** (requiere seed):
- `implements` — tarea implementa otra
- `depends_on` — tarea depende de otra
- `related_to` — tareas relacionadas
- `blocks` — tarea bloquea otra

**API:**
```
POST /api/tasks/:parentId/links
{
  "childId": "uuid-tarea-hija",
  "linkTypeCode": "depends_on"
}

GET /api/tasks/:id/links
DELETE /api/task-links/:id
```

**Caso de uso:**
- Tarea "Implementar endpoint POST /users" `depends_on` "Crear modelo User"
- Tarea "QA Integration tests" `related_to` "Implementar endpoint GET /users"

---

### 2.2 Criterios de Aceptación (AcceptanceCriteria)

**Qué hace:** Definir criterios que una tarea debe cumplir.

**Tipos de criterio disponibles** (requiere seed):
- `functional` — comportamiento esperado
- `technical` — requisito técnico
- `ux` — experiencia de usuario
- `security` — seguridad
- `performance` — rendimiento

**API:**
```
POST /api/tasks/:id/criteria
{
  "criteriaTypeCode": "functional",
  "title": "Usuario puede registrarse con email",
  "description": "El endpoint POST /users acepta email válido"
}

GET /api/tasks/:id/criteria
PATCH /api/criteria/:id
DELETE /api/criteria/:id
```

---

### 2.3 Fulfillment de Criterios (TaskCriteriaFulfillment)

**Qué hace:** Marcar si un criterio se cumplió o no.

**Estados:**
- `pending` — no evaluado
- `met` — cumplido
- `not_met` — no cumplido

**API:**
```
POST /api/criteria/:id/fulfill
{
  "status": "met",
  "notes": "Verificado en PR #123",
  "reportedBy": "uuid-agente"
}

GET /api/tasks/:id/criteria-fulfillments
```

**Campos importantes:**
- `reportedBy` — quién reportó el cumplimiento (agente)
- `verifiedBy` — quién verificó (TL/QA)
- `fulfilledAt` — cuándo se marcó

---

### 2.4 Document Impacts (TaskDocumentImpact)

**Qué hace:** Registrar qué documentos impacta una tarea.

**Tipos de impacto:**
- `added` — documento nuevo
- `modified` — documento modificado
- `removed` — documento eliminado
- `referenced` — solo referenciado

**API:**
```
POST /api/tasks/:id/document-impacts
{
  "documentSourceId": "uuid-source",
  "impactType": "modified",
  "description": "Agregué nuevo endpoint al schema"
}

GET /api/tasks/:id/document-impacts
PATCH /api/document-impacts/:id/resolve
```

---

## 3. FEATURES DE DEVLOG

### 3.1 Entries de Devlog (TaskDevlogEntry)

**Qué hace:** Registrar observaciones, decisiones, blockers durante ejecución.

**Categorías disponibles** (requiere seed):
- `issue` — observación/inconsistencia (NO bugs)
- `tech_debt` — deuda técnica
- `decision` — decisión tomada
- `blocker` — algo bloquea avance
- `risk` — riesgo identificado
- `testing_note` — resultado de test

**Severidad:**
- `critical` — BLOQUEA cierre de tarea
- `high` — BLOQUEA cierre de tarea
- `medium` — no bloquea
- `low` — no bloquea

**API:**
```
POST /api/tasks/:id/devlog-entries
{
  "categoryCode": "decision",
  "severity": null,
  "title": "Usar UUID en lugar de auto-increment",
  "description": "Por consistencia con el resto del sistema",
  "reportedBy": "uuid-agente"
}

GET /api/tasks/:id/devlog-entries
```

---

### 3.2 Resolución de Entries

**Qué hace:** Marcar un entry como resuelto.

**API:**
```
PATCH /api/devlog-entries/:id/resolve
{
  "resolution": "Migración ejecutada por Admin",
  "resolvedBy": "uuid-usuario"
}
```

**Campos que se llenan automáticamente:**
- `resolvedAt` — timestamp
- `resolvedBy` — quién resolvió

---

### 3.3 Diferir Entry a otra Fase

**Qué hace:** Marcar que el entry se resolverá en otra fase.

**API:**
```
PATCH /api/devlog-entries/:id/defer
{
  "deferredToPhaseId": "uuid-fase-futura"
}
```

---

### 3.4 Crear Fix Task desde Entry

**Qué hace:** Crear una tarea nueva para resolver el entry.

**API:**
```
POST /api/devlog-entries/:id/create-fix-task
{
  "title": "Fix: Refactorizar TimeService",
  "assignedToId": "uuid-usuario"
}
```

El entry queda con `fixTaskId` apuntando a la nueva tarea.

---

## 4. FEATURES DE DOCUMENTOS DINÁMICOS

### 4.1 Living Documents (ProjectDocument + Sources)

**Qué hace:** Documentos que se auto-actualizan desde código.

**Fuentes disponibles** (requiere seed):
- `prisma_schema` — genera doc desde schema.prisma
- `swagger_openapi` — genera doc desde swagger/openapi.json

**API:**
```
POST /api/project-documents/:id/sources
{
  "sourceCode": "prisma_schema",
  "config": {
    "filePath": "prisma/schema.prisma"
  }
}

POST /api/project-documents/:id/sync
```

---

### 4.2 Document Sources (ProjectDocumentSource)

**Qué hace:** Configurar de dónde se alimenta un living document.

**Campos:**
- `sourceCode` — tipo de fuente
- `isEnabled` — activo/inactivo
- `config` — JSON con configuración específica
- `lastParsedAt` — última vez que se parseó

---

## 5. FEATURES DE CRITERIOS

### 5.1 Criterios por Tarea

**Qué hace:** Lista de criterios de aceptación por tarea.

**Workflow:**
1. PM/TL crea criterios → `POST /api/tasks/:id/criteria`
2. Agente trabaja en tarea
3. Agente reporta fulfillment → `POST /api/criteria/:id/fulfill`
4. TL verifica → `PATCH /api/criteria-fulfillments/:id { verifiedBy }`

---

### 5.2 Tipos de Criterio

**Configuración en catálogo** (requiere seed):

| code | name | Descripción |
|------|------|-------------|
| `functional` | Funcional | Comportamiento esperado |
| `technical` | Técnico | Requisito de implementación |
| `ux` | UX | Experiencia de usuario |
| `security` | Seguridad | Requisitos de seguridad |
| `performance` | Rendimiento | Requisitos de performance |

---

## 6. GATE DE REVISIÓN (Pendiente S12)

### ¿Qué va a hacer?

Verificar antes de que una tarea pase a `task_in_review`:
1. ¿Hay devlog entries con `severity=critical|high` en `status=pending`?
2. Si sí → **BLOQUEA** con 422

### API (cuando se implemente):

```
GET /api/tasks/:id/review-gate

Response:
{
  "canProceedToReview": false,
  "blockers": [...],
  "warnings": [...],
  "summary": {
    "total": 5,
    "pending": 2,
    "resolved": 3
  }
}
```

---

## 7. CÓMO USAR LAS FEATURES COMO AGENTE

### Al iniciar trabajo en una tarea:

```bash
# 1. Ver criterios que debo cumplir
GET /api/tasks/:id/criteria

# 2. Ver si hay blockers pendientes
GET /api/tasks/:id/devlog-entries?status=pending
```

### Durante ejecución:

```bash
# Registrar decisión
POST /api/tasks/:id/devlog-entries
{ "categoryCode": "decision", "title": "...", "reportedBy": "mi-uuid" }

# Registrar blocker
POST /api/tasks/:id/devlog-entries
{ "categoryCode": "blocker", "severity": "high", "title": "...", "reportedBy": "mi-uuid" }

# Registrar deuda técnica
POST /api/tasks/:id/devlog-entries
{ "categoryCode": "tech_debt", "severity": "medium", "title": "...", "reportedBy": "mi-uuid" }
```

### Al completar trabajo:

```bash
# 1. Reportar cumplimiento de criterios
POST /api/criteria/:criteriaId/fulfill
{ "status": "met", "notes": "Implementado en PR #123", "reportedBy": "mi-uuid" }

# 2. Registrar impactos en documentos
POST /api/tasks/:id/document-impacts
{ "documentSourceId": "uuid", "impactType": "modified", "description": "..." }

# 3. Verificar que no haya blockers pendientes
GET /api/tasks/:id/devlog-entries?severity=critical,high&status=pending
# Si hay → resolverlos antes de cerrar
```

---

## 8. CATÁLOGOS QUE NECESITAN SEED

### criteria_type_catalog

```sql
INSERT INTO criteria_type_catalog (code, name, description, is_active, "order") VALUES
('functional', 'Funcional', 'Comportamiento esperado del sistema', true, 1),
('technical', 'Técnico', 'Requisito de implementación', true, 2),
('ux', 'UX', 'Experiencia de usuario', true, 3),
('security', 'Seguridad', 'Requisitos de seguridad', true, 4),
('performance', 'Rendimiento', 'Requisitos de performance', true, 5);
```

### devlog_category_catalog

```sql
INSERT INTO devlog_category_catalog (code, name, description, severity_levels, is_active, "order") VALUES
('issue', 'Issue', 'Observación o inconsistencia detectada', '{"critical","high","medium","low"}', true, 1),
('tech_debt', 'Tech Debt', 'Deuda técnica identificada', '{"critical","high","medium","low"}', true, 2),
('decision', 'Decision', 'Decisión técnica tomada', '{}', true, 3),
('blocker', 'Blocker', 'Algo que bloquea el avance', '{"critical","high","medium","low"}', true, 4),
('risk', 'Risk', 'Riesgo identificado', '{"critical","high","medium","low"}', true, 5),
('testing_note', 'Testing Note', 'Resultado o nota de testing', '{"critical","high","medium","low"}', true, 6);
```

### link_type_catalog

```sql
INSERT INTO link_type_catalog (code, name, description, is_active, "order") VALUES
('implements', 'Implements', 'Tarea implementa a otra', true, 1),
('depends_on', 'Depends On', 'Tarea depende de otra', true, 2),
('related_to', 'Related To', 'Tareas relacionadas', true, 3),
('blocks', 'Blocks', 'Tarea bloquea a otra', true, 4);
```

### living_doc_source_catalog

```sql
INSERT INTO living_doc_source_catalog (code, name, description, generation_type, parser_service, source_file_path, is_active, "order") VALUES
('prisma_schema', 'Prisma Schema', 'Genera documentación desde schema.prisma', 'file', 'PrismaParserService', 'prisma/schema.prisma', true, 1),
('swagger_openapi', 'Swagger/OpenAPI', 'Genera documentación desde openapi.json', 'file', 'SwaggerParserService', 'swagger/openapi.json', true, 2);
```

---

## 9. CHECKLIST ANTES DE USAR

| Paso | Acción | Estado |
|------|--------|--------|
| 1 | Ejecutar seeds de catálogos | ⬜ Pendiente |
| 2 | Verificar endpoints funcionan | ⬜ Pendiente |
| 3 | Crear proyecto de prueba | ⬜ Pendiente |
| 4 | Probar flujo completo | ⬜ Pendiente |

---

**Documento:** CATALOGO_FEATURES_VTT_V4.md  
**Versión:** 1.0  
**Fecha:** 2026-04-12
