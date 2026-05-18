# FEATURE: TRACKABLE ITEMS

| Campo | Valor |
|-------|-------|
| **Feature** | Trackable Items |
| **Versión** | 1.0 |
| **Fecha** | 2026-04-12 |
| **Sprint origen** | S04, S04-B, S09 |
| **Estado** | ✅ Implementado (BE/DB) |

---

## 1. QUÉ ES

Items rastreables que necesitan seguimiento a lo largo del proyecto. Pueden ser requerimientos, decisiones arquitectónicas, KPIs, riesgos, o cualquier cosa que deba vincularse a tareas y evidenciarse.

---

## 2. PARA QUÉ SIRVE

- **Trazabilidad** — Rastrear desde requerimiento hasta implementación
- **Cobertura** — Ver qué items están implementados y cuáles faltan
- **Evidencia** — Documentar cómo se cumplió cada item
- **Auditoría** — Demostrar que los requerimientos se implementaron
- **Deferred scope** — Trackear lo que se pospone a futuras fases

---

## 3. PRECONDICIONES

### Para que la feature funcione, debe existir:

| Precondición | Tabla/Entidad | ¿Existe? |
|--------------|---------------|----------|
| Proyecto creado | `projects` | ✅ |
| Catálogo de tipos | `trackable_type_catalog` | ✅ (necesita seed) |
| Catálogo de link types | `link_type_catalog` | ✅ (necesita seed) |
| Tareas creadas | `tasks` | ✅ |

### Seeds necesarios:

**trackable_type_catalog:**

| code | name | Descripción |
|------|------|-------------|
| `rf` | Requerimiento Funcional | Comportamiento esperado del sistema |
| `rnf` | Requerimiento No Funcional | Requisitos de calidad (performance, seguridad) |
| `adr` | Architecture Decision Record | Decisión arquitectónica documentada |
| `kpi` | Key Performance Indicator | Métrica de éxito |
| `risk` | Riesgo | Riesgo identificado |
| `constraint` | Restricción | Limitación del proyecto |
| `assumption` | Supuesto | Supuesto asumido |
| `dependency` | Dependencia Externa | Dependencia de terceros |

**link_type_catalog:**

| code | name | Descripción |
|------|------|-------------|
| `implements` | Implements | Tarea implementa el item |
| `depends_on` | Depends On | Item depende de otro |
| `related_to` | Related To | Items relacionados |
| `blocks` | Blocks | Item bloquea a otro |
| `parent_of` | Parent Of | Item es padre de otro |
| `child_of` | Child Of | Item es hijo de otro |

---

## 4. CÓMO SE ACTIVA

### ¿Quién crea trackable items?

| Rol | ¿Puede crear? | Tipos típicos |
|-----|---------------|---------------|
| PM | ✅ Sí | RF, RNF, KPI |
| SA (Systems Analyst) | ✅ Sí | RF, RNF, Constraints |
| AR (Architect) | ✅ Sí | ADR, Constraints |
| TL | ✅ Sí | ADR, Risk |
| Agentes ejecutores | ❌ No (solo vincular) | — |

### ¿Cuándo se crean?

| Fase | Tipos típicos |
|------|---------------|
| Requirements | RF, RNF |
| Analysis | RF detallados, Constraints, Assumptions |
| Technical Design | ADR |
| Cualquier fase | Risk, Dependency |

### ¿Se pueden crear después?

**Sí.** Los trackable items pueden crearse en cualquier momento del proyecto. Es común que durante desarrollo se identifiquen nuevos ADRs o riesgos.

---

## 5. FLUJO OPERATIVO

### 5.1 CREAR TRACKABLE ITEM

#### Paso a paso

```
PASO 1: PM/SA/AR identifica algo que trackear
─────────────────────────────────────────────────
Ejemplo: "El sistema debe permitir registro con email"

PASO 2: Crear el item
─────────────────────────────────────────────────
POST /api/projects/:projectId/trackable-items

PASO 3: Item queda disponible para vincular
─────────────────────────────────────────────────
Aparece en lista de items del proyecto.
Se puede vincular a tareas.
```

#### Request

```
POST /api/projects/:projectId/trackable-items
```

```json
{
  "typeCode": "rf",
  "code": "RF-001",
  "title": "Registro de usuario con email",
  "description": "El sistema debe permitir que un usuario se registre proporcionando email y password. El email debe ser único.",
  "priority": "high",
  "status": "open"
}
```

#### Response

```json
{
  "id": "uuid",
  "projectId": "uuid-project",
  "typeCode": "rf",
  "code": "RF-001",
  "title": "Registro de usuario con email",
  "description": "El sistema debe permitir...",
  "priority": "high",
  "status": "open",
  "createdBy": "uuid-pm",
  "createdAt": "2026-04-12T10:00:00Z"
}
```

---

### 5.2 VINCULAR ITEM A TAREA

#### ¿Quién vincula?

| Rol | ¿Puede vincular? |
|-----|------------------|
| PM/SA/AR | ✅ Sí (al planificar) |
| TL | ✅ Sí (al asignar trabajo) |
| Agente ejecutor | ✅ Sí (durante ejecución) |

#### Paso a paso

```
PASO 1: Existe tarea y existe item
─────────────────────────────────────────────────
Tarea: VTT-423 "Implementar POST /users"
Item: RF-001 "Registro de usuario con email"

PASO 2: Vincular
─────────────────────────────────────────────────
POST /api/trackable-items/:itemId/tasks

PASO 3: Queda registrado el vínculo
─────────────────────────────────────────────────
La tarea ahora "implementa" el item RF-001.
```

#### Request

```
POST /api/trackable-items/:itemId/tasks
```

```json
{
  "taskId": "uuid-task-423",
  "linkType": "implements",
  "notes": "Esta tarea implementa el endpoint de registro"
}
```

#### Response

```json
{
  "id": "uuid-link",
  "trackableItemId": "uuid-rf-001",
  "taskId": "uuid-task-423",
  "linkType": "implements",
  "notes": "Esta tarea implementa el endpoint de registro",
  "createdBy": "uuid-user",
  "createdAt": "2026-04-12T10:30:00Z"
}
```

---

### 5.3 AGREGAR EVIDENCIA

#### ¿Qué es evidencia?

Documentación de que el item fue cumplido. Puede ser:

| Tipo | Ejemplo |
|------|---------|
| PR/Commit | "Implementado en PR #125" |
| Test | "Test case TC-001 pasó" |
| Documento | "Documentado en API Reference" |
| Screenshot | "Ver captura de pantalla adjunta" |
| URL | "Demo en https://staging.app.com/register" |

#### Paso a paso

```
PASO 1: Item está vinculado a tareas
─────────────────────────────────────────────────
RF-001 está vinculado a VTT-423.

PASO 2: Tarea se completa
─────────────────────────────────────────────────
VTT-423 pasa a "completed".

PASO 3: Agregar evidencia
─────────────────────────────────────────────────
POST /api/trackable-items/:itemId/evidences

PASO 4: Item puede marcarse como cumplido
─────────────────────────────────────────────────
PATCH /api/trackable-items/:itemId
{ "status": "completed" }
```

#### Request

```
POST /api/trackable-items/:itemId/evidences
```

```json
{
  "type": "pr",
  "title": "PR #125 - Implementar registro de usuario",
  "url": "https://github.com/org/repo/pull/125",
  "description": "Endpoint POST /users implementado con validación de email único"
}
```

---

### 5.4 VINCULAR ITEMS ENTRE SÍ

#### ¿Para qué?

- Mostrar dependencias entre requerimientos
- Vincular ADR con los RFs que lo originaron
- Relacionar riesgos con constraints

#### Tipos de link

| Link Type | Significado | Ejemplo |
|-----------|-------------|---------|
| `depends_on` | Este item necesita otro | RF-002 depends_on RF-001 |
| `related_to` | Items relacionados | RF-001 related_to RNF-001 |
| `blocks` | Este item bloquea otro | RISK-001 blocks RF-003 |
| `parent_of` | Este item es padre | RF-001 parent_of RF-001-A, RF-001-B |

#### Request

```
POST /api/trackable-items/:itemId/links
```

```json
{
  "targetItemId": "uuid-rf-002",
  "linkType": "related_to",
  "notes": "Ambos requerimientos afectan el módulo de usuarios"
}
```

---

### 5.5 DIFERIR ITEM (Deferred Scope)

#### ¿Qué es?

Cuando un item no se puede completar en el release/fase actual y se pospone.

#### Estados de deferral

| Status | Significado |
|--------|-------------|
| `deferral_pending` | Identificado como diferido, sin programar |
| `deferral_scheduled` | Programado para fase/release futuro |
| `deferral_completed` | Ya se implementó |
| `deferral_cancelled` | Se decidió no hacerlo |

#### Paso a paso

```
PASO 1: Durante análisis/desarrollo, se decide diferir
─────────────────────────────────────────────────
RF-005 "Exportar a PDF" no entra en MVP.

PASO 2: Registrar deferral
─────────────────────────────────────────────────
POST /api/trackable-items/:itemId/defer

PASO 3: Item queda marcado
─────────────────────────────────────────────────
Status cambia. Queda visible en backlog futuro.

PASO 4: En release futuro, se implementa
─────────────────────────────────────────────────
Se vincula a tareas del nuevo release.
Status cambia a deferral_completed.
```

#### Request

```
POST /api/trackable-items/:itemId/defer
```

```json
{
  "targetReleaseId": "uuid-release-v2",
  "targetPhaseId": "uuid-phase-dev",
  "reason": "No es crítico para MVP. Requiere librería externa.",
  "deferredBy": "uuid-pm"
}
```

---

### 5.6 VER MATRIZ DE TRAZABILIDAD

#### ¿Qué es?

Vista consolidada que muestra:
- Todos los items del proyecto
- Qué tareas los implementan
- Estado de cada uno
- Cobertura (% implementado)

#### Request

```
GET /api/projects/:projectId/traceability-report
```

#### Response

```json
{
  "projectId": "uuid",
  "generatedAt": "2026-04-12T12:00:00Z",
  "summary": {
    "totalItems": 25,
    "completed": 18,
    "inProgress": 5,
    "pending": 2,
    "deferred": 3,
    "coveragePercent": 72
  },
  "byType": {
    "rf": { "total": 15, "completed": 12 },
    "rnf": { "total": 5, "completed": 3 },
    "adr": { "total": 5, "completed": 3 }
  },
  "items": [
    {
      "id": "uuid",
      "code": "RF-001",
      "title": "Registro de usuario con email",
      "status": "completed",
      "tasks": [
        { "id": "uuid", "code": "VTT-423", "status": "completed" }
      ],
      "evidences": [
        { "type": "pr", "title": "PR #125" }
      ]
    }
  ]
}
```

---

## 6. CIERRE / COMPLETACIÓN

### ¿Cuándo se considera "completo" un item?

| Criterio | Obligatorio |
|----------|-------------|
| Al menos una tarea vinculada | ✅ Sí |
| Tarea(s) vinculada(s) completada(s) | ✅ Sí |
| Evidencia agregada | Recomendado |
| Status = "completed" | ✅ Sí |

### ¿Quién puede cerrar un item?

| Rol | ¿Puede cerrar? |
|-----|----------------|
| PM | ✅ Sí |
| SA | ✅ Sí |
| AR | ✅ Sí (solo ADRs) |
| TL | ✅ Sí |
| Agente ejecutor | ❌ No |

### Request para cerrar

```
PATCH /api/trackable-items/:itemId
```

```json
{
  "status": "completed",
  "completedBy": "uuid-pm",
  "completionNotes": "Implementado y verificado en PR #125"
}
```

---

## 7. ¿ES BLOQUEANTE?

### ¿Los trackable items bloquean el trabajo?

**NO por default.** Los items son para tracking, no para bloquear.

| Situación | ¿Bloquea? |
|-----------|-----------|
| Item sin tareas vinculadas | ❌ No |
| Item pendiente, tareas completadas | ❌ No |
| Item diferido | ❌ No |
| Querer cerrar release sin items completos | ❌ No (pero se reporta) |

### ¿Se puede configurar como bloqueante?

**Sí.** En la configuración del proyecto se puede definir:

```json
{
  "trackableItemsConfig": {
    "blockReleaseIfIncomplete": false,
    "requireEvidenceForCompletion": true,
    "requireTaskLinkForCompletion": true
  }
}
```

Si `blockReleaseIfIncomplete: true`, no se puede cerrar el release si hay items RF pendientes.

---

## 8. RESPONSABLES

| Acción | PM | SA | AR | TL | Agente |
|--------|----|----|----|----|--------|
| Crear item | ✅ | ✅ | ✅ | ✅ | ❌ |
| Editar item | ✅ | ✅ | ✅ | ✅ | ❌ |
| Vincular a tarea | ✅ | ✅ | ✅ | ✅ | ✅ |
| Agregar evidencia | ✅ | ✅ | ✅ | ✅ | ✅ |
| Cerrar item | ✅ | ✅ | ✅* | ✅ | ❌ |
| Diferir item | ✅ | ✅ | ❌ | ❌ | ❌ |
| Ver reporte trazabilidad | ✅ | ✅ | ✅ | ✅ | ✅ |

*AR solo puede cerrar ADRs.

---

## 9. ENDPOINTS

### CRUD de Items

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/projects/:projectId/trackable-items` | Listar items del proyecto |
| POST | `/api/projects/:projectId/trackable-items` | Crear item |
| GET | `/api/trackable-items/:id` | Ver detalle de item |
| PATCH | `/api/trackable-items/:id` | Actualizar item |
| DELETE | `/api/trackable-items/:id` | Eliminar item |

### Vínculos con Tareas

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/trackable-items/:id/tasks` | Ver tareas vinculadas |
| POST | `/api/trackable-items/:id/tasks` | Vincular tarea |
| DELETE | `/api/trackable-item-tasks/:linkId` | Desvincular tarea |

### Evidencias

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/trackable-items/:id/evidences` | Ver evidencias |
| POST | `/api/trackable-items/:id/evidences` | Agregar evidencia |
| DELETE | `/api/trackable-item-evidences/:id` | Eliminar evidencia |

### Links entre Items

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/trackable-items/:id/links` | Ver links |
| POST | `/api/trackable-items/:id/links` | Crear link |
| DELETE | `/api/trackable-item-links/:id` | Eliminar link |

### Deferred Scope

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/trackable-items/:id/defer` | Diferir item |
| PATCH | `/api/trackable-item-deferrals/:id` | Actualizar deferral |
| POST | `/api/trackable-item-deferrals/:id/schedule` | Programar para release |
| POST | `/api/trackable-item-deferrals/:id/cancel` | Cancelar deferral |

### Reportes

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/projects/:projectId/traceability-report` | Matriz de trazabilidad |
| GET | `/api/projects/:projectId/trackable-items/coverage` | Reporte de cobertura |
| GET | `/api/projects/:projectId/trackable-items/deferred` | Items diferidos |

---

## 10. EJEMPLO COMPLETO

### Escenario

Proyecto VTT, Release MVP. Tenemos 3 requerimientos funcionales.

### Flujo completo

```
FASE REQUIREMENTS
────────────────────────────────────────────────────────────

PM crea requerimientos:

POST /api/projects/vtt/trackable-items
{ "typeCode": "rf", "code": "RF-001", "title": "Registro con email" }
→ ✅ Creado

POST /api/projects/vtt/trackable-items
{ "typeCode": "rf", "code": "RF-002", "title": "Login con email" }
→ ✅ Creado

POST /api/projects/vtt/trackable-items
{ "typeCode": "rf", "code": "RF-003", "title": "Exportar a PDF" }
→ ✅ Creado

FASE ANALYSIS
────────────────────────────────────────────────────────────

SA analiza y crea vínculo entre RFs:

POST /api/trackable-items/rf-002/links
{ "targetItemId": "rf-001", "linkType": "depends_on" }
→ RF-002 depende de RF-001 (login depende de registro)

PM decide diferir RF-003:

POST /api/trackable-items/rf-003/defer
{ "targetReleaseId": "v2.0", "reason": "No crítico para MVP" }
→ RF-003 diferido a V2.0

FASE DEVELOPMENT
────────────────────────────────────────────────────────────

TL crea tareas y las vincula:

Tarea VTT-423: "Implementar POST /users"
POST /api/trackable-items/rf-001/tasks
{ "taskId": "vtt-423", "linkType": "implements" }
→ VTT-423 implementa RF-001

Tarea VTT-424: "Implementar POST /auth/login"
POST /api/trackable-items/rf-002/tasks
{ "taskId": "vtt-424", "linkType": "implements" }
→ VTT-424 implementa RF-002

EJECUCIÓN
────────────────────────────────────────────────────────────

BE-Agent completa VTT-423:

Agente agrega evidencia:
POST /api/trackable-items/rf-001/evidences
{ "type": "pr", "title": "PR #125", "url": "github.com/..." }

PM cierra RF-001:
PATCH /api/trackable-items/rf-001
{ "status": "completed" }

(Repetir para RF-002)

CIERRE DE RELEASE
────────────────────────────────────────────────────────────

PM genera reporte de trazabilidad:

GET /api/projects/vtt/traceability-report

Response:
{
  "summary": {
    "totalItems": 3,
    "completed": 2,
    "deferred": 1,
    "coveragePercent": 67
  },
  "items": [
    { "code": "RF-001", "status": "completed" },
    { "code": "RF-002", "status": "completed" },
    { "code": "RF-003", "status": "deferred", "deferredTo": "V2.0" }
  ]
}

Release puede cerrarse. RF-003 queda en backlog de V2.0.
```

---

## 11. TABLAS EN BASE DE DATOS

### trackable_type_catalog

```sql
CREATE TABLE trackable_type_catalog (
  code VARCHAR(50) PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  icon_type VARCHAR(100),
  is_active BOOLEAN DEFAULT true,
  "order" INT DEFAULT 0
);
```

### trackable_items

```sql
CREATE TABLE trackable_items (
  id TEXT PRIMARY KEY,
  project_id TEXT NOT NULL REFERENCES projects(id),
  type_code VARCHAR(50) NOT NULL REFERENCES trackable_type_catalog(code),
  code VARCHAR(50) NOT NULL,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  priority VARCHAR(50),
  status VARCHAR(50) DEFAULT 'open',
  created_by TEXT REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  completed_by TEXT REFERENCES users(id),
  completed_at TIMESTAMP,
  completion_notes TEXT,
  
  UNIQUE(project_id, code)
);
```

### trackable_item_tasks

```sql
CREATE TABLE trackable_item_tasks (
  id TEXT PRIMARY KEY,
  trackable_item_id TEXT NOT NULL REFERENCES trackable_items(id) ON DELETE CASCADE,
  task_id TEXT NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
  link_type VARCHAR(50) DEFAULT 'implements',
  notes TEXT,
  created_by TEXT REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW(),
  
  UNIQUE(trackable_item_id, task_id)
);
```

### trackable_item_evidences

```sql
CREATE TABLE trackable_item_evidences (
  id TEXT PRIMARY KEY,
  trackable_item_id TEXT NOT NULL REFERENCES trackable_items(id) ON DELETE CASCADE,
  type VARCHAR(50) NOT NULL,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  url TEXT,
  created_by TEXT REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW()
);
```

### trackable_item_links

```sql
CREATE TABLE trackable_item_links (
  id TEXT PRIMARY KEY,
  source_item_id TEXT NOT NULL REFERENCES trackable_items(id) ON DELETE CASCADE,
  target_item_id TEXT NOT NULL REFERENCES trackable_items(id) ON DELETE CASCADE,
  link_type_code VARCHAR(50) NOT NULL REFERENCES link_type_catalog(code),
  notes TEXT,
  created_by TEXT REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW(),
  
  UNIQUE(source_item_id, target_item_id, link_type_code)
);
```

### trackable_item_deferrals

```sql
CREATE TABLE trackable_item_deferrals (
  id TEXT PRIMARY KEY,
  trackable_item_id TEXT NOT NULL REFERENCES trackable_items(id) ON DELETE CASCADE,
  status VARCHAR(50) DEFAULT 'deferral_pending',
  target_release_id TEXT REFERENCES releases(id),
  target_phase_id TEXT REFERENCES phases(id),
  reason TEXT,
  deferred_by TEXT REFERENCES users(id),
  deferred_at TIMESTAMP DEFAULT NOW(),
  scheduled_by TEXT REFERENCES users(id),
  scheduled_at TIMESTAMP,
  completed_at TIMESTAMP,
  cancelled_at TIMESTAMP,
  cancellation_reason TEXT
);
```

---

## 12. ERRORES COMUNES

| Error | Causa | Solución |
|-------|-------|----------|
| "Item code already exists" | Código duplicado en proyecto | Usar código único (RF-001, RF-002) |
| "Cannot delete item with tasks" | Item tiene tareas vinculadas | Desvincular tareas primero |
| "Task already linked" | Tarea ya está vinculada al item | No se puede vincular dos veces |
| "Cannot complete without tasks" | Config requiere tareas | Vincular al menos una tarea |
| "Cannot complete without evidence" | Config requiere evidencia | Agregar evidencia primero |

---

## 13. FAQ

**¿Puedo crear items durante desarrollo?**
Sí. Es común identificar ADRs o riesgos durante desarrollo.

**¿Un item puede vincularse a múltiples tareas?**
Sí. Un RF grande puede requerir varias tareas para implementarse.

**¿Una tarea puede vincularse a múltiples items?**
Sí. Una tarea puede implementar varios RFs relacionados.

**¿Qué pasa con los items diferidos?**
Quedan en el backlog del release/fase destino. Aparecen en reportes de deferred scope.

**¿Puedo eliminar un item?**
Sí, pero solo si no tiene tareas vinculadas o evidencias.

**¿Los items bloquean el release?**
Por default no. Se puede configurar para que sí bloqueen.

---

## 14. CONFIGURACIÓN

### En wizard/settings del proyecto:

```json
{
  "trackableItemsConfig": {
    "enabled": true,
    "requiredTypes": ["rf"],
    "blockReleaseIfIncomplete": false,
    "requireEvidenceForCompletion": false,
    "requireTaskLinkForCompletion": true,
    "autoCreateFromPRD": false
  }
}
```

| Campo | Descripción | Default |
|-------|-------------|---------|
| `enabled` | Feature habilitada | `true` |
| `requiredTypes` | Tipos obligatorios para el proyecto | `["rf"]` |
| `blockReleaseIfIncomplete` | ¿Bloquear release si hay items incompletos? | `false` |
| `requireEvidenceForCompletion` | ¿Requerir evidencia para cerrar? | `false` |
| `requireTaskLinkForCompletion` | ¿Requerir tarea vinculada para cerrar? | `true` |
| `autoCreateFromPRD` | ¿Auto-crear items desde PRD? | `false` |

---

**Documento:** FEATURE_TRACKABLE_ITEMS.md  
**Versión:** 1.0  
**Fecha:** 2026-04-12
