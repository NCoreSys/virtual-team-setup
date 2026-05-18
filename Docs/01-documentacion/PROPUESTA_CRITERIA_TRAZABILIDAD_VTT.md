# PROPUESTA — Mejoras al Sistema de Criteria y Trazabilidad VTT
## Para evaluación de TL y AR

**Solicitado por:** PM Memory Service (`350831b2-e1ae-4dbe-b2eb-7e023ec2e103`)
**Elaborado por:** SA Ejecutor (`0c128e3b-db3b-4e31-b107-0379b5791233`)
**Fecha:** 2026-05-06
**Origen:** Análisis de MS-024 (Acceptance Criteria) reveló gaps en el modelo VTT V4 para gestionar 144 criterios de aceptación, DoD y DoR de forma escalable.

---

## 1. PROBLEMA

Durante el análisis de Memory Service R1, el SA produjo 144 criterios (49 Gherkin AC, 35 DoD, 14 DoR, 46 Test Scenarios) que deben registrarse en VTT y vincularse a las tareas correspondientes. El modelo actual tiene el catálogo de `criteria_types` (14 tipos) pero carece de:

- Mecanismo de templates reutilizables para DoD/DoR
- Vinculación automática de DoD al tipo de tarea
- Validación bloqueante de DoR al mover tareas
- Clasificación de tareas por tipo (backend, frontend, docs, testing)
- Registro masivo de criterios desde documentos de análisis

Estos gaps afectan a todos los proyectos VTT, no solo a Memory Service.

---

## 2. PROPUESTA 1 — Criteria Templates (DoD/DoR)

### 2.1 Concepto

Un criteria template es un conjunto predefinido de criterios que se aplica automáticamente a las tareas según su contexto (tipo de proyecto, tipo de tarea). Dos niveles de scope:

| Nivel | Scope | Ejemplo | Quién lo gestiona |
|-------|-------|---------|-------------------|
| **Global** | Todos los proyectos de un `projectTypeCode` | "Código compila TypeScript" para todo proyecto `software` | Admin VTT |
| **Proyecto** | Un proyecto específico | "Idempotencia verificada" solo para Memory Service | PM del proyecto |

### 2.2 Modelo de datos propuesto

```
criteria_template
├── id: UUID (PK)
├── code: String (unique) — ej: "DOD-BE-01"
├── name: String — ej: "Código compila TypeScript"
├── description: String
├── criteriaTypeCode: String (FK → criteria_type_catalog) — ej: "dod", "dor"
├── scope: Enum("global", "project")
├── projectTypeCode: String? (FK → project_type_catalog) — para scope=global
├── projectId: UUID? (FK → projects) — para scope=project
├── taskTypeCode: String? (FK → task_type_catalog) — a qué tipo de tarea aplica
├── isActive: Boolean (default: true)
├── sortOrder: Int
├── createdAt: DateTime
└── updatedAt: DateTime
```

### 2.3 Herencia

Al crear una tarea en un proyecto `software` con `taskTypeCode=backend`:

```
1. Sistema busca templates globales con:
   - scope=global AND projectTypeCode=software AND taskTypeCode=backend
   
2. Sistema busca templates de proyecto con:
   - scope=project AND projectId={projectId} AND taskTypeCode=backend

3. Combina ambos sets (proyecto override global si mismo code)

4. Crea criteria en la tarea automáticamente
```

### 2.4 Ejemplo concreto

Templates globales para `software` + `backend`:

| code | description | scope |
|------|-------------|-------|
| DOD-BE-01 | Código compila sin errores TypeScript | global |
| DOD-BE-02 | Validación Zod implementada | global |
| DOD-BE-03 | Tests unitarios pasan | global |
| DOD-BE-09 | Development Log creado | global |

Templates de proyecto Memory Service + `backend`:

| code | description | scope |
|------|-------------|-------|
| DOD-BE-06 | Máquina de estados respetada (2.5.6) | project |
| DOD-BE-07 | Idempotencia verificada | project |

Al crear una tarea BE en Memory Service → recibe los 6 criterios automáticamente.

### 2.5 API propuesta

```
# CRUD de templates
GET    /api/criteria-templates?scope=global&projectTypeCode=software
POST   /api/criteria-templates
PATCH  /api/criteria-templates/:id
DELETE /api/criteria-templates/:id

# Preview: qué criteria recibiría una tarea
GET    /api/criteria-templates/preview?projectId={pid}&taskTypeCode=backend

# Aplicar templates a una tarea existente (si se creó antes del template)
POST   /api/tasks/:taskId/criteria/apply-templates
```

### 2.6 Impacto estimado

| Componente | Cambio |
|-----------|--------|
| BD | 1 tabla nueva (`criteria_template`) |
| API | 4 endpoints nuevos |
| Lógica | Hook en creación de tarea para aplicar templates |
| Migration | Seed de templates globales |

---

## 3. PROPUESTA 2 — DoR Bloqueante con Override

### 3.1 Concepto

El DoR (Definition of Ready) se valida al intentar mover una tarea a `task_in_progress`. Si hay criterios DoR sin cumplir, la transición se bloquea salvo override explícito con justificación.

### 3.2 Flujo

```
Agente llama: PATCH /api/tasks/:id/status { statusId: "in_progress" }

  ┌─ Sistema verifica criteria tipo "dor" de la tarea
  │
  ├─ Todos met → transición OK
  │
  └─ Alguno pendiente:
     │
     ├─ Sin overrideReason → HTTP 422
     │  {
     │    "error": "DOR_NOT_MET",
     │    "pendingCriteria": ["DOR-05", "DOR-12"],
     │    "message": "2 DoR criteria pending. Provide overrideReason to proceed."
     │  }
     │
     └─ Con overrideReason → transición OK + registro
        {
          "statusId": "in_progress",
          "overrideReason": "BD no disponible aún, pero puedo avanzar con lógica pura",
          "changedBy": "uuid-agente"
        }
        
        → Se registra en task_status_history:
          - dorOverride: true
          - overrideReason: "..."
          - pendingCriteria: ["DOR-05", "DOR-12"]
          - overriddenBy: "uuid-agente"
```

### 3.3 Impacto en el endpoint existente

```
PATCH /api/tasks/:id/status

Body actual:
{
  "statusId": "uuid",
  "changedBy": "uuid"
}

Body extendido:
{
  "statusId": "uuid",
  "changedBy": "uuid",
  "overrideReason": "string (opcional, requerido si hay DoR pendientes)"
}
```

### 3.4 Configuración

| Config | Valor | Dónde |
|--------|-------|-------|
| `dorBlockingEnabled` | `true/false` | Por proyecto (settings) |
| `dorBlockingDefault` | `true` | Global (system settings) |

Esto permite que proyectos nuevos arranquen con DoR bloqueante pero proyectos legacy puedan desactivarlo temporalmente durante migración.

### 3.5 Impacto estimado

| Componente | Cambio |
|-----------|--------|
| BD | Campo `overrideReason` y `dorOverride` en `task_status_history` |
| API | Validación adicional en `PATCH /status`, campo opcional en body |
| Lógica | Query de criteria tipo `dor` antes de transición |
| Config | Campo `dorBlockingEnabled` en project settings |

---

## 4. PROPUESTA 3 — Task Type Catalog

### 4.1 Concepto

Un catálogo que clasifica las tareas por tipo de trabajo. Determina qué DoD template aplica y permite reportes de velocidad por tipo.

### 4.2 Catálogo propuesto

```sql
CREATE TABLE task_type_catalog (
  code VARCHAR(50) PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  "projectTypeCode" VARCHAR(50) REFERENCES project_type_catalog(code),
  "dodTemplateGroup" VARCHAR(50), -- qué grupo de DoD hereda
  "sortOrder" INT DEFAULT 0,
  "isActive" BOOLEAN DEFAULT true
);

INSERT INTO task_type_catalog (code, name, description, "projectTypeCode", "dodTemplateGroup", "sortOrder") VALUES
('backend',       'Backend Development',     'Endpoints, servicios, lógica de negocio', 'software', 'DOD-BE',  1),
('frontend',      'Frontend Development',    'Componentes UI, vistas, interacción',     'software', 'DOD-FE',  2),
('database',      'Database',                'Schema, migrations, seeds, índices',       'software', 'DOD-BE',  3),
('documentation', 'Documentation / Analysis','Documentos SDLC, análisis, specs',        'software', 'DOD-DOC', 4),
('testing',       'QA Testing',              'Tests, validación, certificación',         'software', 'DOD-QA',  5),
('devops',        'Infrastructure / DevOps', 'Docker, CI/CD, monitoreo, deployment',    'software', 'DOD-BE',  6),
('design',        'Design',                  'Wireframes, design system, specs UX',      'software', NULL,      7);
```

### 4.3 Vinculación con tasks

```sql
ALTER TABLE tasks ADD COLUMN "taskTypeCode" VARCHAR(50) 
  REFERENCES task_type_catalog(code);
```

### 4.4 Asignación automática vs manual

| Opción | Cómo funciona | Pros | Contras |
|--------|--------------|------|---------|
| **Manual** | El PM o TL asigna taskTypeCode al crear la tarea | Simple, sin lógica | Requiere disciplina |
| **Por rol** | Se infiere del `assigneeRole`: BE→backend, FE→frontend, SA→documentation | Automático | No siempre es 1:1 (BE puede hacer docs) |
| **Híbrido** | Se infiere por rol pero editable | Mejor de ambos | Más lógica |

**Recomendación:** Híbrido. Se infiere del rol del asignado al crear la tarea, pero el PM/TL puede cambiarlo.

### 4.5 Impacto estimado

| Componente | Cambio |
|-----------|--------|
| BD | 1 tabla nueva + 1 FK en tasks |
| API | Campo `taskTypeCode` en create/update task |
| Lógica | Inferencia por rol (opcional) |
| Migration | Seed del catálogo + backfill de tareas existentes |

---

## 5. PROPUESTA 4 — Registro Masivo de Criteria

### 5.1 Problema

El SA produce documentos de análisis con tablas estructuradas de criterios. Hoy, registrar cada criterio requiere una llamada individual a `POST /api/tasks/:taskId/criteria`. Para 144 criterios = 144 llamadas HTTP.

### 5.2 Solución: Tres niveles incrementales

#### Nivel 1 — JSON normalizado (inmediato, sin cambios en VTT)

El SA genera un archivo `.criteria.json` junto con cada entrega de análisis. Un script del agente ejecutor lo lee y hace los POST en batch.

```json
{
  "projectId": "d0fc276d-...",
  "source": "MS-024",
  "criteria": [
    {
      "code": "AC-US-001-1",
      "criteriaTypeCode": "functional",
      "description": "Import exitoso CLAUDE_SDK: HTTP 201, IMPORTED...",
      "targetUS": "US-001",
      "targetSprint": "S02"
    }
  ],
  "dodTemplates": [
    {
      "code": "DOD-BE-01",
      "criteriaTypeCode": "dod",
      "description": "Código compila sin errores TypeScript",
      "taskTypeCode": "backend"
    }
  ],
  "dorTemplates": [
    {
      "code": "DOR-01",
      "criteriaTypeCode": "dor",
      "description": "ASSIGNMENT leído completamente"
    }
  ]
}
```

**Script del agente:**

```javascript
const data = JSON.parse(fs.readFileSync('MS-024.criteria.json'));

// 1. Resolver taskId de cada US
for (const c of data.criteria) {
  const task = await findTaskByUS(c.targetUS, c.targetSprint);
  await api.post(`/tasks/${task.id}/criteria`, {
    criteriaTypeCode: c.criteriaTypeCode,
    description: c.description,
    code: c.code
  });
}

// 2. Registrar DoD/DoR templates (si endpoint existe)
for (const t of data.dodTemplates) {
  await api.post('/criteria-templates', t);
}
```

#### Nivel 2 — Endpoint bulk (cambio menor en VTT)

```
POST /api/tasks/:taskId/criteria/bulk

Body:
{
  "criteria": [
    { "code": "AC-US-001-1", "criteriaTypeCode": "functional", "description": "..." },
    { "code": "AC-US-001-2", "criteriaTypeCode": "functional", "description": "..." }
  ]
}

Response:
{
  "created": 2,
  "errors": []
}
```

Reduce 144 llamadas a ~30 (una por tarea con múltiples criterios).

#### Nivel 3 — Import desde documento (R2)

```
POST /api/projects/:projectId/criteria/import

Body:
{
  "sourceFile": "MS-024.criteria.json",
  "autoResolveUS": true  // resuelve US→taskId automáticamente
}
```

El sistema parsea el JSON, resuelve los taskIds y registra todo en una operación.

### 5.3 Recomendación

| Nivel | Cuándo | Esfuerzo VTT |
|-------|--------|-------------|
| **Nivel 1** | Ahora (Memory Service R1) | Cero — solo el SA genera el JSON |
| **Nivel 2** | Si más proyectos lo necesitan | 1 endpoint nuevo (~4h BE) |
| **Nivel 3** | R2 de VTT | Feature completa (~16h BE) |

---

## 6. RESUMEN DE CAMBIOS PROPUESTOS

| # | Propuesta | Tabla/Endpoint nuevo | Esfuerzo | Prioridad |
|---|-----------|---------------------|----------|-----------|
| P1 | Criteria Templates (DoD/DoR) | `criteria_template` + 4 endpoints + hook | ~16h | Alta |
| P2 | DoR Bloqueante | Campos en `task_status_history` + validación | ~8h | Alta |
| P3 | Task Type Catalog | `task_type_catalog` + FK en tasks | ~6h | Media |
| P4 | Registro masivo criteria | JSON del SA (0h) + bulk endpoint (~4h) | 0-4h | Alta |
| **Total** | | | **30-34h** | |

### Dependencias entre propuestas

```
P3 (Task Type) ──► P1 (Templates) ──► P2 (DoR bloqueante)
                                  └──► P4 (Bulk registra templates)
```

P3 es prerequisito de P1 (los templates necesitan saber el taskType para aplicarse). P1 es prerequisito de P2 (DoR bloqueante necesita criteria tipo `dor` existentes). P4 es independiente pero se beneficia de P1.

### Orden de implementación recomendado

1. **P4 Nivel 1** (inmediato, 0h VTT) — el SA genera JSON, script lo registra
2. **P3** (6h) — catálogo de task types
3. **P1** (16h) — templates con herencia
4. **P2** (8h) — DoR bloqueante con override

---

## 7. DECISIONES QUE NECESITAMOS DEL PM Y AR

| # | Decisión | Opciones | Impacto |
|---|----------|----------|---------|
| D-01 | ¿Templates global + proyecto o solo proyecto? | A: Dos niveles / B: Solo proyecto | A requiere más lógica pero escala mejor |
| D-02 | ¿DoR bloqueante desde R1 o R2? | A: R1 / B: R2 | A requiere P2 antes del desarrollo de Memory Service |
| D-03 | ¿Task type como catálogo o como tags? | A: Catálogo / B: Tags | A es determinístico, B es flexible |
| D-04 | ¿Bulk endpoint en R1 o solo JSON+script? | A: Bulk / B: JSON+script | A requiere 4h BE, B es cero costo |
| D-05 | ¿Backfill de tareas existentes con taskType? | A: Sí / B: Solo nuevas | A requiere script de migración |

---

**Documento:** PROPUESTA_CRITERIA_TRAZABILIDAD_VTT.md
**Versión:** 1.0
**Fecha:** 2026-05-06
**Para:** TL (`92225290-6b6b-4c1f-a940-dcb4262507aa`), AR (`e9403c25-c1f8-4b64-b2ef-f447d53115e2`)
**CC:** PM (`350831b2-e1ae-4dbe-b2eb-7e023ec2e103`)
