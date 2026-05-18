# FEATURE: CARPETAS DE PROYECTO (Project Folders)

| Campo | Valor |
|-------|-------|
| **Feature** | Project Folders |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-06 |
| **Sprint origen** | S05 |
| **Estado** | ✅ Implementado (BE/DB) |

---

## 1. QUÉ ES

Sistema de organización jerárquica de documentos dentro de un proyecto. Permite crear carpetas y subcarpetas para estructurar la documentación del proyecto de manera lógica.

---

## 2. PARA QUÉ SIRVE

- **Organización** — Agrupar documentos relacionados (specs, análisis, diseño, etc.)
- **Navegación** — Facilitar la búsqueda de documentos por estructura
- **Convención** — Establecer estructura estándar de documentación
- **Contexto** — Los agentes saben dónde buscar y dónde guardar documentos

---

## 3. PRECONDICIONES

| Precondición | Tabla/Entidad | ¿Existe? |
|--------------|---------------|----------|
| Proyecto creado | `projects` | ✅ |

---

## 4. ESTRUCTURA DE CARPETAS

### 4.1 Estructura por defecto (proyectos software)

Al crear un proyecto tipo `software`, se genera automáticamente:

```
📁 {proyecto}/
├── 📁 docs/
│   ├── 📁 discovery/
│   │   ├── 📁 problem/
│   │   └── 📁 value/
│   ├── 📁 analysis/
│   │   ├── 📁 requirements/
│   │   ├── 📁 use-cases/
│   │   ├── 📁 user-stories/
│   │   ├── 📁 rules/
│   │   └── 📁 acceptance-criteria/
│   ├── 📁 design/
│   │   ├── 📁 ux/
│   │   ├── 📁 ui/
│   │   └── 📁 architecture/
│   ├── 📁 specs/
│   └── 📁 guides/
├── 📁 releases/
│   └── 📁 {release-code}/
│       └── 📁 sprints/
│           └── 📁 {sprint-code}/
├── 📁 handoffs/
├── 📁 devlogs/
└── 📁 attachments/
```

### 4.2 Carpetas por fase SDLC

| Fase | Carpeta | Contenido típico |
|------|---------|------------------|
| Discovery | `docs/discovery/` | Problem statement, value proposition, personas |
| Analysis | `docs/analysis/` | RFs, UCs, US, BRs, ACs |
| Design | `docs/design/` | Wireframes, mockups, architecture |
| Development | `releases/{release}/sprints/{sprint}/` | Handoffs, briefs, assignments |
| Testing | `releases/{release}/sprints/{sprint}/qa/` | Test plans, results |
| Deployment | `docs/guides/` | Guías de instalación, deployment |

---

## 5. FLUJO OPERATIVO

### 5.1 Crear carpeta

```
PASO 1: Usuario necesita nueva carpeta
─────────────────────────────────────────────────
Ejemplo: Crear carpeta para un nuevo módulo

PASO 2: Crear carpeta
─────────────────────────────────────────────────
POST /api/projects/:projectId/folders

PASO 3: Carpeta disponible para documentos
─────────────────────────────────────────────────
Aparece en el árbol de navegación.
Se pueden crear documentos dentro.
```

#### Request

```
POST /api/projects/:projectId/folders
```

```json
{
  "name": "memory-service",
  "parentId": "uuid-parent-folder",
  "description": "Documentación del módulo Memory Service",
  "icon": "lucide:database"
}
```

#### Response

```json
{
  "id": "uuid-folder",
  "projectId": "uuid-project",
  "name": "memory-service",
  "slug": "memory-service",
  "parentId": "uuid-parent-folder",
  "path": "/docs/specs/memory-service",
  "depth": 3,
  "description": "Documentación del módulo Memory Service",
  "icon": "lucide:database",
  "documentCount": 0,
  "createdBy": "uuid-user",
  "createdAt": "2026-05-06T10:00:00Z"
}
```

### 5.2 Obtener árbol de carpetas

```
GET /api/projects/:projectId/folders/tree
```

#### Response

```json
{
  "projectId": "uuid-project",
  "root": {
    "id": "root",
    "name": "Proyecto VTT",
    "children": [
      {
        "id": "uuid-docs",
        "name": "docs",
        "path": "/docs",
        "children": [
          {
            "id": "uuid-analysis",
            "name": "analysis",
            "path": "/docs/analysis",
            "documentCount": 15,
            "children": [...]
          }
        ]
      },
      {
        "id": "uuid-releases",
        "name": "releases",
        "path": "/releases",
        "children": [...]
      }
    ]
  }
}
```

### 5.3 Mover carpeta

```
PATCH /api/folders/:folderId/move
```

```json
{
  "newParentId": "uuid-new-parent",
  "movedBy": "uuid-user"
}
```

**Reglas:**
- No se puede mover una carpeta dentro de sí misma
- No se puede mover a un descendiente
- Se actualizan los paths de todos los documentos dentro

### 5.4 Renombrar carpeta

```
PATCH /api/folders/:folderId
```

```json
{
  "name": "nuevo-nombre"
}
```

**Efecto:** Se actualiza el `path` de la carpeta y todos sus documentos.

### 5.5 Eliminar carpeta

```
DELETE /api/folders/:folderId
```

**Reglas:**
- Solo se puede eliminar si está vacía (sin documentos ni subcarpetas)
- Para eliminar con contenido, usar `?force=true` (mueve contenido a padre)

---

## 6. CARPETAS ESPECIALES

Algunas carpetas tienen comportamiento especial:

| Carpeta | Comportamiento especial |
|---------|------------------------|
| `handoffs/` | Auto-crea subcarpeta por sprint al generar handoff |
| `devlogs/` | Auto-organiza por fecha (YYYY-MM/) |
| `attachments/` | Archivos binarios adjuntos a tareas/documentos |
| `releases/{code}/` | Se crea automáticamente al crear un release |
| `sprints/{code}/` | Se crea automáticamente al crear un sprint |

---

## 7. ¿ES BLOQUEANTE?

**No.** Las carpetas son organizativas. No bloquean ningún flujo.

| Situación | ¿Bloquea? |
|-----------|-----------|
| Documento sin carpeta | ❌ No (va a raíz) |
| Carpeta vacía | ❌ No |
| Carpeta eliminada con docs | ❌ No (docs se mueven) |

---

## 8. RESPONSABLES

| Acción | PM | TL | SA | Agente |
|--------|----|----|----|----|
| Crear carpeta | ✅ | ✅ | ✅ | ✅ |
| Renombrar carpeta | ✅ | ✅ | ✅ | ❌ |
| Mover carpeta | ✅ | ✅ | ❌ | ❌ |
| Eliminar carpeta | ✅ | ✅ | ❌ | ❌ |
| Ver árbol | ✅ | ✅ | ✅ | ✅ |

---

## 9. ENDPOINTS

### CRUD de Carpetas

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/projects/:projectId/folders` | Listar carpetas (flat) |
| GET | `/api/projects/:projectId/folders/tree` | Árbol jerárquico |
| POST | `/api/projects/:projectId/folders` | Crear carpeta |
| GET | `/api/folders/:id` | Detalle de carpeta |
| PATCH | `/api/folders/:id` | Actualizar carpeta |
| DELETE | `/api/folders/:id` | Eliminar carpeta |
| PATCH | `/api/folders/:id/move` | Mover carpeta |

### Documentos en carpeta

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/folders/:id/documents` | Listar documentos de la carpeta |
| POST | `/api/folders/:id/documents` | Crear documento en carpeta |

---

## 10. EJEMPLO COMPLETO

### Escenario

Crear estructura para Memory Service dentro de un proyecto existente.

```
POST /api/projects/vtt/folders
{
  "name": "memory-service",
  "parentId": "uuid-docs-specs",
  "description": "Especificaciones Memory Service R1"
}
→ Carpeta creada: /docs/specs/memory-service/

POST /api/projects/vtt/folders
{
  "name": "analysis",
  "parentId": "uuid-memory-service"
}
→ Carpeta creada: /docs/specs/memory-service/analysis/

POST /api/projects/vtt/folders
{
  "name": "design",
  "parentId": "uuid-memory-service"
}
→ Carpeta creada: /docs/specs/memory-service/design/

Resultado:
📁 docs/specs/memory-service/
├── 📁 analysis/
└── 📁 design/
```

---

## 11. TABLAS EN BASE DE DATOS

### project_folders

```sql
CREATE TABLE project_folders (
  id TEXT PRIMARY KEY,
  project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  parent_id TEXT REFERENCES project_folders(id),
  
  name VARCHAR(255) NOT NULL,
  slug VARCHAR(255) NOT NULL,
  path TEXT NOT NULL,
  depth INT DEFAULT 0,
  
  description TEXT,
  icon VARCHAR(100),
  
  -- Metadata
  document_count INT DEFAULT 0,
  is_system BOOLEAN DEFAULT false,  -- Carpetas auto-generadas
  
  created_by TEXT REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  UNIQUE(project_id, path),
  UNIQUE(project_id, parent_id, slug)
);

CREATE INDEX idx_folders_project ON project_folders(project_id);
CREATE INDEX idx_folders_parent ON project_folders(parent_id);
CREATE INDEX idx_folders_path ON project_folders(path);
```

---

## 12. CONFIGURACIÓN

### Por proyecto

```json
{
  "foldersConfig": {
    "autoCreateStructure": true,
    "defaultStructure": "software",
    "maxDepth": 10,
    "allowAgentCreate": true,
    "allowAgentMove": false
  }
}
```

| Campo | Descripción | Default |
|-------|-------------|---------|
| `autoCreateStructure` | Crear estructura al crear proyecto | `true` |
| `defaultStructure` | Template de estructura (`software`, `marketing`, `custom`) | `software` |
| `maxDepth` | Profundidad máxima de anidación | `10` |
| `allowAgentCreate` | Agentes pueden crear carpetas | `true` |
| `allowAgentMove` | Agentes pueden mover carpetas | `false` |

---

## 13. FAQ

**¿Puedo crear carpetas fuera de la estructura default?**
Sí. La estructura default es sugerencia, no obligatoria.

**¿Qué pasa si elimino una carpeta con documentos?**
Con `force=true`, los documentos se mueven a la carpeta padre. Sin `force`, error.

**¿Puedo tener dos carpetas con el mismo nombre?**
Sí, si están en diferentes padres. El `path` completo debe ser único.

**¿Los agentes pueden crear carpetas?**
Por default sí. Se puede desactivar en configuración.

**¿Se puede cambiar la estructura después de crear el proyecto?**
Sí. Las carpetas son completamente editables.

---

## 14. INTEGRACIÓN CON OTRAS FEATURES

| Feature | Integración |
|---------|-------------|
| **Project Documents** | Documentos viven dentro de carpetas |
| **Living Documents** | Se generan en carpeta específica |
| **Handoffs** | Auto-crean subcarpeta por sprint |
| **Devlogs** | Se organizan por fecha en `/devlogs/` |

---

**Documento:** FEATURE_PROJECT_FOLDERS.md  
**Versión:** 1.0  
**Fecha:** 2026-05-06
