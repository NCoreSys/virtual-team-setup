# FEATURE: DOCUMENTOS DE PROYECTO (Project Documents)

| Campo | Valor |
|-------|-------|
| **Feature** | Project Documents |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-06 |
| **Sprint origen** | S06 |
| **Estado** | ✅ Implementado (BE/DB) |

---

## 1. QUÉ ES

Sistema de gestión de documentos del proyecto. Incluye documentos estáticos (specs, guías), documentos versionados, y living documents que se auto-generan desde fuentes de datos.

---

## 2. PARA QUÉ SIRVE

- **Centralización** — Toda la documentación del proyecto en un lugar
- **Versionamiento** — Historial de cambios de documentos críticos
- **Auto-generación** — Living documents que se actualizan automáticamente
- **Indexación** — Búsqueda y navegación eficiente
- **Trazabilidad** — Vincular documentos a tareas, releases, sprints

---

## 3. PRECONDICIONES

| Precondición | Tabla/Entidad | ¿Existe? |
|--------------|---------------|----------|
| Proyecto creado | `projects` | ✅ |
| Carpeta destino (opcional) | `project_folders` | ✅ |
| Catálogo de fuentes living doc | `living_doc_source_catalog` | ✅ |

---

## 4. TIPOS DE DOCUMENTOS

| Tipo | Código | Descripción | Ejemplo |
|------|--------|-------------|---------|
| **Estático** | `static` | Documento manual, no cambia automáticamente | SPEC, README, Guías |
| **Versionado** | `versioned` | Documento con historial de versiones | Specs que evolucionan |
| **Living** | `living` | Auto-generado desde una fuente de datos | API docs desde Swagger |
| **Template** | `template` | Plantilla para generar otros documentos | Handoff template |
| **Attachment** | `attachment` | Archivo binario adjunto | Imágenes, PDFs |

---

## 5. FLUJO OPERATIVO

### 5.1 Crear documento estático

```
PASO 1: Usuario crea documento
─────────────────────────────────────────────────
POST /api/projects/:projectId/documents

PASO 2: Documento disponible
─────────────────────────────────────────────────
Aparece en la carpeta especificada.
Se puede editar, versionar, vincular.
```

#### Request

```
POST /api/projects/:projectId/documents
```

```json
{
  "title": "SPEC Memory Service v1.9",
  "slug": "spec-memory-service-v1.9",
  "folderId": "uuid-specs-folder",
  "documentType": "versioned",
  "contentType": "markdown",
  "content": "# Memory Service\n\n## 1. Introducción\n...",
  "tags": ["spec", "memory-service", "r1"],
  "metadata": {
    "version": "1.9",
    "status": "approved"
  }
}
```

#### Response

```json
{
  "id": "uuid-document",
  "projectId": "uuid-project",
  "folderId": "uuid-specs-folder",
  "title": "SPEC Memory Service v1.9",
  "slug": "spec-memory-service-v1.9",
  "path": "/docs/specs/spec-memory-service-v1.9",
  "documentType": "versioned",
  "contentType": "markdown",
  "content": "# Memory Service\n\n## 1. Introducción\n...",
  "version": 1,
  "tags": ["spec", "memory-service", "r1"],
  "metadata": {
    "version": "1.9",
    "status": "approved"
  },
  "createdBy": "uuid-user",
  "createdAt": "2026-05-06T10:00:00Z"
}
```

### 5.2 Actualizar documento (crear versión)

```
PATCH /api/documents/:documentId
```

```json
{
  "content": "# Memory Service\n\n## 1. Introducción (actualizada)\n...",
  "changeNote": "Actualizado sección de introducción con nuevos requisitos",
  "updatedBy": "uuid-user"
}
```

**Efecto para documentos `versioned`:**
- Se guarda la versión anterior en `document_versions`
- `version` se incrementa
- Se registra `changeNote` y `updatedBy`

### 5.3 Ver historial de versiones

```
GET /api/documents/:documentId/versions
```

#### Response

```json
{
  "documentId": "uuid-document",
  "currentVersion": 3,
  "versions": [
    {
      "version": 3,
      "content": "...",
      "changeNote": "Agregado sección de cleanup",
      "createdBy": "uuid-user",
      "createdAt": "2026-05-06T14:00:00Z"
    },
    {
      "version": 2,
      "content": "...",
      "changeNote": "Corregido endpoint de import",
      "createdBy": "uuid-user",
      "createdAt": "2026-05-05T10:00:00Z"
    },
    {
      "version": 1,
      "content": "...",
      "changeNote": "Versión inicial",
      "createdBy": "uuid-user",
      "createdAt": "2026-05-04T08:00:00Z"
    }
  ]
}
```

### 5.4 Restaurar versión anterior

```
POST /api/documents/:documentId/restore
```

```json
{
  "version": 2,
  "restoredBy": "uuid-user",
  "reason": "Versión 3 tenía errores"
}
```

**Efecto:** Crea una nueva versión (4) con el contenido de la versión 2.

### 5.5 Configurar Living Document

```
PASO 1: Crear documento tipo living
─────────────────────────────────────────────────
POST /api/projects/:projectId/documents
{
  "documentType": "living",
  "title": "API Reference",
  ...
}

PASO 2: Configurar fuente de datos
─────────────────────────────────────────────────
POST /api/documents/:documentId/living-config

PASO 3: Documento se auto-genera
─────────────────────────────────────────────────
Según trigger configurado (manual, schedule, on-change)
```

#### Request - Configurar living doc

```
POST /api/documents/:documentId/living-config
```

```json
{
  "sourceCode": "swagger_openapi",
  "sourceConfig": {
    "filePath": "swagger/openapi.json",
    "includeSchemas": true,
    "includeExamples": true
  },
  "triggerType": "on_change",
  "triggerConfig": {
    "watchPath": "swagger/openapi.json"
  },
  "templateId": "uuid-api-template"
}
```

### 5.6 Regenerar Living Document manualmente

```
POST /api/documents/:documentId/regenerate
```

**Efecto:** 
- Lee la fuente de datos
- Aplica el template
- Actualiza el contenido
- Crea nueva versión si cambió

---

## 6. ÍNDICE DE DOCUMENTOS

El sistema mantiene un índice para búsqueda rápida.

### 6.1 Buscar documentos

```
GET /api/projects/:projectId/documents/search?q=memory+service
```

#### Response

```json
{
  "query": "memory service",
  "results": [
    {
      "id": "uuid-1",
      "title": "SPEC Memory Service v1.9",
      "path": "/docs/specs/spec-memory-service-v1.9",
      "snippet": "...Memory Service es un microservicio independiente...",
      "score": 0.95,
      "tags": ["spec", "memory-service"]
    },
    {
      "id": "uuid-2",
      "title": "Handoff Memory Service S03",
      "path": "/handoffs/ms-r1-s03",
      "snippet": "...Sprint 3 del proyecto Memory Service...",
      "score": 0.82,
      "tags": ["handoff", "memory-service"]
    }
  ],
  "totalResults": 2
}
```

### 6.2 Reindexar documento

```
POST /api/documents/:documentId/reindex
```

**Cuándo usar:** Después de actualización masiva o si el índice está desactualizado.

---

## 7. VINCULAR DOCUMENTOS

### 7.1 Vincular a tarea

```
POST /api/tasks/:taskId/documents
```

```json
{
  "documentId": "uuid-document",
  "linkType": "reference",
  "notes": "SPEC principal del proyecto"
}
```

| linkType | Significado |
|----------|-------------|
| `reference` | Documento de referencia |
| `input` | Documento de entrada (brief, assignment) |
| `output` | Documento de salida (deliverable) |
| `devlog` | Devlog de la tarea |

### 7.2 Vincular a release/sprint

```
POST /api/releases/:releaseId/documents
POST /api/sprints/:sprintId/documents
```

---

## 8. FUENTES DE LIVING DOCUMENTS

| sourceCode | Fuente | Genera |
|------------|--------|--------|
| `prisma_schema` | `prisma/schema.prisma` | Documentación de modelo de datos |
| `swagger_openapi` | `swagger/openapi.json` | Documentación de API |
| `typescript_types` | `src/types/*.d.ts` | Documentación de tipos |
| `env_template` | `.env.example` | Documentación de variables de entorno |
| `package_json` | `package.json` | Documentación de dependencias |
| `db_query` | Query SQL configurable | Documentación desde BD |

---

## 9. ¿ES BLOQUEANTE?

**No por default.** Los documentos son informativos.

| Situación | ¿Bloquea? |
|-----------|-----------|
| Documento sin vincular | ❌ No |
| Living doc desactualizado | ❌ No (warning) |
| Documento en draft | ❌ No |

### Configuración bloqueante (opcional)

```json
{
  "documentsConfig": {
    "requireSpecForDevelopment": true,
    "requireHandoffForSprint": true
  }
}
```

Si `requireSpecForDevelopment: true`, no se puede iniciar fase Development sin SPEC aprobada.

---

## 10. RESPONSABLES

| Acción | PM | TL | SA | AR | Agente |
|--------|----|----|----|----|--------|
| Crear documento | ✅ | ✅ | ✅ | ✅ | ✅ |
| Editar documento | ✅ | ✅ | ✅ | ✅ | ✅ |
| Eliminar documento | ✅ | ✅ | ❌ | ❌ | ❌ |
| Configurar living doc | ✅ | ✅ | ✅ | ✅ | ❌ |
| Regenerar living doc | ✅ | ✅ | ✅ | ✅ | ✅ |
| Restaurar versión | ✅ | ✅ | ❌ | ❌ | ❌ |
| Vincular a tarea | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 11. ENDPOINTS

### CRUD de Documentos

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/projects/:projectId/documents` | Listar documentos |
| POST | `/api/projects/:projectId/documents` | Crear documento |
| GET | `/api/documents/:id` | Ver documento |
| PATCH | `/api/documents/:id` | Actualizar documento |
| DELETE | `/api/documents/:id` | Eliminar documento |
| PATCH | `/api/documents/:id/move` | Mover a otra carpeta |

### Versionamiento

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/documents/:id/versions` | Listar versiones |
| GET | `/api/documents/:id/versions/:version` | Ver versión específica |
| POST | `/api/documents/:id/restore` | Restaurar versión |
| GET | `/api/documents/:id/diff?v1=2&v2=3` | Comparar versiones |

### Living Documents

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/documents/:id/living-config` | Configurar living doc |
| PATCH | `/api/documents/:id/living-config` | Actualizar config |
| POST | `/api/documents/:id/regenerate` | Regenerar manualmente |
| GET | `/api/documents/:id/generation-log` | Ver log de generaciones |

### Índice y Búsqueda

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/projects/:projectId/documents/search` | Buscar documentos |
| POST | `/api/documents/:id/reindex` | Reindexar documento |
| POST | `/api/projects/:projectId/documents/reindex-all` | Reindexar todo |

### Vínculos

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/tasks/:taskId/documents` | Vincular a tarea |
| DELETE | `/api/task-documents/:linkId` | Desvincular |
| GET | `/api/documents/:id/linked-tasks` | Ver tareas vinculadas |

---

## 12. EJEMPLO COMPLETO

### Escenario

Crear SPEC, versionar, vincular a sprint.

```
CREAR SPEC
────────────────────────────────────────────────────────────

POST /api/projects/vtt/documents
{
  "title": "SPEC Memory Service v1.0",
  "folderId": "uuid-specs",
  "documentType": "versioned",
  "contentType": "markdown",
  "content": "# Memory Service\n\n## 1. Introducción\n..."
}
→ Documento creado, version=1

ACTUALIZAR SPEC
────────────────────────────────────────────────────────────

PATCH /api/documents/uuid-spec
{
  "content": "# Memory Service v1.5\n\n## 1. Introducción (actualizada)\n...",
  "changeNote": "Actualizado a v1.5 con nuevos endpoints"
}
→ version=2, versión anterior guardada

VER HISTORIAL
────────────────────────────────────────────────────────────

GET /api/documents/uuid-spec/versions
→ [v2 (actual), v1 (anterior)]

VINCULAR A SPRINT
────────────────────────────────────────────────────────────

POST /api/sprints/uuid-s03/documents
{
  "documentId": "uuid-spec",
  "linkType": "reference"
}
→ Sprint S03 tiene la SPEC como referencia

CONFIGURAR COMO LIVING DOC (API Reference)
────────────────────────────────────────────────────────────

POST /api/projects/vtt/documents
{
  "title": "API Reference",
  "documentType": "living",
  "folderId": "uuid-docs"
}

POST /api/documents/uuid-api-ref/living-config
{
  "sourceCode": "swagger_openapi",
  "sourceConfig": { "filePath": "swagger/openapi.json" },
  "triggerType": "on_change"
}
→ Se genera automáticamente cuando cambia openapi.json
```

---

## 13. TABLAS EN BASE DE DATOS

### project_documents

```sql
CREATE TABLE project_documents (
  id TEXT PRIMARY KEY,
  project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  folder_id TEXT REFERENCES project_folders(id),
  
  title VARCHAR(500) NOT NULL,
  slug VARCHAR(500) NOT NULL,
  path TEXT NOT NULL,
  
  document_type VARCHAR(50) NOT NULL,  -- static, versioned, living, template, attachment
  content_type VARCHAR(50) DEFAULT 'markdown',  -- markdown, html, json, binary
  content TEXT,
  
  version INT DEFAULT 1,
  tags TEXT[],
  metadata JSONB,
  
  -- Para attachments
  file_name VARCHAR(255),
  file_size INT,
  mime_type VARCHAR(100),
  storage_path TEXT,
  
  -- Auditoría
  created_by TEXT REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_by TEXT REFERENCES users(id),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  UNIQUE(project_id, path)
);

CREATE INDEX idx_documents_project ON project_documents(project_id);
CREATE INDEX idx_documents_folder ON project_documents(folder_id);
CREATE INDEX idx_documents_type ON project_documents(document_type);
CREATE INDEX idx_documents_tags ON project_documents USING GIN(tags);
```

### document_versions

```sql
CREATE TABLE document_versions (
  id TEXT PRIMARY KEY,
  document_id TEXT NOT NULL REFERENCES project_documents(id) ON DELETE CASCADE,
  version INT NOT NULL,
  content TEXT NOT NULL,
  change_note TEXT,
  created_by TEXT REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW(),
  
  UNIQUE(document_id, version)
);

CREATE INDEX idx_versions_document ON document_versions(document_id);
```

### document_index

```sql
CREATE TABLE document_index (
  id TEXT PRIMARY KEY,
  document_id TEXT NOT NULL REFERENCES project_documents(id) ON DELETE CASCADE,
  project_id TEXT NOT NULL REFERENCES projects(id),
  
  title_tokens TSVECTOR,
  content_tokens TSVECTOR,
  tags_tokens TSVECTOR,
  
  indexed_at TIMESTAMP DEFAULT NOW(),
  
  UNIQUE(document_id)
);

CREATE INDEX idx_index_title ON document_index USING GIN(title_tokens);
CREATE INDEX idx_index_content ON document_index USING GIN(content_tokens);
CREATE INDEX idx_index_project ON document_index(project_id);
```

### living_document_configs

```sql
CREATE TABLE living_document_configs (
  id TEXT PRIMARY KEY,
  document_id TEXT NOT NULL REFERENCES project_documents(id) ON DELETE CASCADE,
  
  source_code VARCHAR(50) NOT NULL REFERENCES living_doc_source_catalog(code),
  source_config JSONB,
  
  trigger_type VARCHAR(50) DEFAULT 'manual',  -- manual, schedule, on_change
  trigger_config JSONB,
  
  template_id TEXT REFERENCES project_documents(id),
  
  last_generated_at TIMESTAMP,
  last_generation_status VARCHAR(50),
  last_generation_error TEXT,
  
  is_active BOOLEAN DEFAULT true,
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  UNIQUE(document_id)
);
```

### task_documents

```sql
CREATE TABLE task_documents (
  id TEXT PRIMARY KEY,
  task_id TEXT NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
  document_id TEXT NOT NULL REFERENCES project_documents(id) ON DELETE CASCADE,
  
  link_type VARCHAR(50) DEFAULT 'reference',  -- reference, input, output, devlog
  notes TEXT,
  
  created_by TEXT REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW(),
  
  UNIQUE(task_id, document_id)
);
```

---

## 14. CONFIGURACIÓN

### Por proyecto

```json
{
  "documentsConfig": {
    "defaultContentType": "markdown",
    "enableVersioning": true,
    "maxVersionsToKeep": 50,
    "enableLivingDocs": true,
    "enableFullTextSearch": true,
    "requireSpecForDevelopment": false,
    "requireHandoffForSprint": false
  }
}
```

---

## 15. FAQ

**¿Cuántas versiones se guardan?**
Por default 50. Configurable en `maxVersionsToKeep`.

**¿Puedo convertir un documento estático a versionado?**
Sí. PATCH con `documentType: "versioned"`. La versión actual se convierte en v1.

**¿Qué pasa si la fuente de un living doc no existe?**
El documento queda en estado `error` con mensaje. No se borra el contenido anterior.

**¿Puedo tener varios living docs de la misma fuente?**
Sí. Pueden tener diferentes templates o configuraciones.

**¿Los attachments se versionan?**
No por default. Son archivos binarios que se sobreescriben.

---

## 16. INTEGRACIÓN CON OTRAS FEATURES

| Feature | Integración |
|---------|-------------|
| **Project Folders** | Documentos viven dentro de carpetas |
| **Tasks** | Documentos se vinculan como input/output/reference |
| **Handoffs** | Son documentos tipo template + output |
| **Devlogs** | Son documentos vinculados a tareas |
| **Living Documents** | Subsistema de auto-generación |
| **Document Impacts** | Feature que trackea qué docs afecta una tarea |

---

**Documento:** FEATURE_PROJECT_DOCUMENTS.md  
**Versión:** 1.0  
**Fecha:** 2026-05-06
