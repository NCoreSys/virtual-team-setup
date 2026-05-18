# FEATURE: FLOW TEMPLATES

| Campo | Valor |
|-------|-------|
| **Feature** | Flow Templates |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-06 |
| **Sprint origen** | S02 |
| **Estado** | ✅ Implementado (BE/DB) |

---

## 1. QUÉ ES

Plantillas predefinidas de flujo de trabajo que determinan qué fases y deliverables se incluyen al crear un proyecto. Permiten configurar rápidamente un proyecto según la metodología elegida.

---

## 2. PARA QUÉ SIRVE

- **Configuración rápida** — Seleccionar Agile y tener toda la estructura lista
- **Estandarización** — Equipos usan la misma estructura
- **Flexibilidad** — Múltiples templates para diferentes metodologías
- **Personalización** — Después de clonar, el proyecto puede modificarse

---

## 3. TEMPLATES DISPONIBLES

### 3.1 Agile (Default para software)

```
📋 Agile Flow Template
├── 📁 Discovery (opcional)
├── 📁 Requirements
├── 📁 Analysis
├── 📁 Design
├── 📁 Development
├── 📁 Testing
└── 📁 Deployment
```

| Fase | Duración | Sprints | Deliverables |
|------|----------|---------|--------------|
| Discovery | 1 semana | 0.5 | Problem Statement, Value Prop |
| Requirements | 1 semana | 0.5 | Requirements List |
| Analysis | 2 semanas | 1 | Use Cases, User Stories, AC |
| Design | 2 semanas | 1 | Wireframes, Architecture, Spec |
| Development | Variable | N | Source Code, API Docs |
| Testing | 1 semana | 0.5 | Test Plan, Test Results |
| Deployment | 3 días | 0.25 | Deployment Guide, Release Notes |

### 3.2 Waterfall

```
📋 Waterfall Flow Template
├── 📁 Requirements (Gate 1)
├── 📁 Analysis (Gate 2)
├── 📁 Design (Gate 3)
├── 📁 Development (Gate 4)
├── 📁 Testing (Gate 5)
└── 📁 Deployment (Gate 6)
```

| Fase | Duración | Gate | Deliverables requeridos |
|------|----------|------|------------------------|
| Requirements | 3 semanas | Aprobación formal | Requirements Sign-off |
| Analysis | 4 semanas | Aprobación formal | Analysis Sign-off |
| Design | 4 semanas | Aprobación formal | Design Sign-off |
| Development | 8 semanas | Code Complete | Código entregado |
| Testing | 4 semanas | QA Sign-off | Test Sign-off |
| Deployment | 2 semanas | Go-Live | Deployment Complete |

### 3.3 Kanban

```
📋 Kanban Flow Template
├── 📁 Backlog
├── 📁 In Progress
├── 📁 Review
└── 📁 Done
```

Sin fases SDLC tradicionales. Flujo continuo basado en WIP limits.

### 3.4 Custom

```
📋 Custom Flow Template
└── (vacío - configuración manual)
```

El usuario define todas las fases y deliverables manualmente.

---

## 4. ESTRUCTURA DE DATOS

### 4.1 Flow Template

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `code` | String | Código único (agile, waterfall, kanban, custom) |
| `name` | String | Nombre del template |
| `description` | Text | Descripción de la metodología |
| `projectTypeCode` | String | Tipo de proyecto aplicable |
| `isDefault` | Boolean | Si es el default para el tipo |

### 4.2 Flow Phase Config

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `flowTemplateCode` | String | FK al template |
| `phaseCode` | String | FK a la fase del catálogo |
| `order` | Int | Orden en el template |
| `isRequired` | Boolean | Si es obligatoria |
| `defaultDuration` | Int | Duración default en días |

### 4.3 Phase Deliverable Config

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `flowPhaseConfigId` | UUID | FK a la config de fase |
| `deliverableCode` | String | FK al deliverable del catálogo |
| `isRequired` | Boolean | Si es obligatorio |
| `order` | Int | Orden dentro de la fase |

---

## 5. FLUJO OPERATIVO

### 5.1 Listar templates disponibles

```
GET /api/flow-templates?projectTypeCode=software
```

```json
{
  "templates": [
    {
      "code": "agile",
      "name": "Agile",
      "description": "Metodología ágil con sprints",
      "isDefault": true,
      "phasesCount": 7,
      "deliverablesCount": 16
    },
    {
      "code": "waterfall",
      "name": "Waterfall",
      "description": "Metodología secuencial con gates",
      "isDefault": false,
      "phasesCount": 6,
      "deliverablesCount": 12
    },
    {
      "code": "custom",
      "name": "Custom",
      "description": "Configuración manual",
      "isDefault": false,
      "phasesCount": 0,
      "deliverablesCount": 0
    }
  ]
}
```

### 5.2 Ver detalle de template

```
GET /api/flow-templates/agile
```

```json
{
  "code": "agile",
  "name": "Agile",
  "description": "Metodología ágil con sprints de 2 semanas",
  "projectTypeCode": "software",
  "isDefault": true,
  "phases": [
    {
      "phaseCode": "discovery",
      "name": "Discovery",
      "order": 1,
      "isRequired": false,
      "defaultDuration": 5,
      "deliverables": [
        { "code": "problem_statement", "name": "Problem Statement", "isRequired": false },
        { "code": "value_proposition", "name": "Value Proposition", "isRequired": false }
      ]
    },
    {
      "phaseCode": "analysis",
      "name": "Analysis",
      "order": 3,
      "isRequired": true,
      "defaultDuration": 15,
      "deliverables": [
        { "code": "use_cases", "name": "Use Cases", "isRequired": true },
        { "code": "user_stories", "name": "User Stories", "isRequired": true },
        { "code": "acceptance_criteria", "name": "Acceptance Criteria", "isRequired": true }
      ]
    }
  ]
}
```

### 5.3 Aplicar template al crear proyecto

```
POST /api/projects
{
  "name": "Memory Service",
  "projectTypeCode": "software",
  "flowTemplateCode": "agile"
}
```

**Efecto:**
1. Sistema lee el template "agile"
2. Copia las fases configuradas → `project_phases`
3. Copia los deliverables por fase → `project_deliverables`
4. Proyecto creado con estructura completa

### 5.4 Preview de template antes de crear

```
GET /api/flow-templates/agile/preview
```

Retorna la estructura completa que se aplicará al proyecto.

---

## 6. HERENCIA Y CLONACIÓN

### 6.1 Principio de clonación

```
Template (Global, inmutable)
        │
        │ clone al crear proyecto
        ▼
Proyecto (Local, editable)
```

### 6.2 Cambios post-creación

Una vez creado el proyecto:
- ✅ Puedes agregar/quitar fases
- ✅ Puedes reordenar fases
- ✅ Puedes agregar/quitar deliverables
- ❌ NO afecta al template original
- ❌ NO afecta a otros proyectos

### 6.3 Cambios al template

Si Admin VTT modifica el template:
- ✅ Nuevos proyectos usan el template actualizado
- ❌ Proyectos existentes NO se afectan

---

## 7. ENDPOINTS

### Flow Templates

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/flow-templates` | Listar todos los templates |
| GET | `/api/flow-templates?projectTypeCode=X` | Filtrar por tipo de proyecto |
| GET | `/api/flow-templates/:code` | Ver template con fases y deliverables |
| GET | `/api/flow-templates/:code/preview` | Preview de estructura |

### Admin (solo Admin VTT)

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/flow-templates` | Crear template |
| PATCH | `/api/flow-templates/:code` | Actualizar template |
| DELETE | `/api/flow-templates/:code` | Eliminar template |
| POST | `/api/flow-templates/:code/phases` | Agregar fase |
| DELETE | `/api/flow-templates/:code/phases/:phaseCode` | Quitar fase |

---

## 8. TABLAS EN BASE DE DATOS

### flow_template_catalog

```sql
CREATE TABLE flow_template_catalog (
  code VARCHAR(50) PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  project_type_code VARCHAR(50) REFERENCES project_type_catalog(code),
  is_default BOOLEAN DEFAULT false,
  is_active BOOLEAN DEFAULT true,
  icon_url VARCHAR(255),
  icon_type VARCHAR(100),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_flow_template_project_type ON flow_template_catalog(project_type_code);
```

### flow_phase_config

```sql
CREATE TABLE flow_phase_config (
  id TEXT PRIMARY KEY,
  flow_template_code VARCHAR(50) NOT NULL REFERENCES flow_template_catalog(code) ON DELETE CASCADE,
  phase_code VARCHAR(50) NOT NULL REFERENCES phase_catalog(code),
  "order" INT NOT NULL,
  is_required BOOLEAN DEFAULT true,
  default_duration_days INT,
  
  UNIQUE(flow_template_code, phase_code)
);

CREATE INDEX idx_flow_phase_template ON flow_phase_config(flow_template_code);
```

### phase_deliverable_config

```sql
CREATE TABLE phase_deliverable_config (
  id TEXT PRIMARY KEY,
  flow_phase_config_id TEXT NOT NULL REFERENCES flow_phase_config(id) ON DELETE CASCADE,
  deliverable_code VARCHAR(50) NOT NULL REFERENCES deliverable_catalog(code),
  is_required BOOLEAN DEFAULT false,
  "order" INT DEFAULT 0,
  
  UNIQUE(flow_phase_config_id, deliverable_code)
);

CREATE INDEX idx_phase_deliverable_config ON phase_deliverable_config(flow_phase_config_id);
```

---

## 9. SEEDS

```sql
-- Flow Templates
INSERT INTO flow_template_catalog (code, name, description, project_type_code, is_default, icon_type) VALUES
('agile', 'Agile', 'Metodología ágil con sprints de 2 semanas', 'software', true, 'lucide:zap'),
('waterfall', 'Waterfall', 'Metodología secuencial con gates formales', 'software', false, 'lucide:git-commit'),
('kanban', 'Kanban', 'Flujo continuo basado en WIP limits', 'software', false, 'lucide:columns'),
('custom', 'Custom', 'Configuración completamente manual', 'software', false, 'lucide:sliders');

-- Flow Phase Config (Agile)
INSERT INTO flow_phase_config (id, flow_template_code, phase_code, "order", is_required, default_duration_days) VALUES
('fpc-agile-discovery', 'agile', 'discovery', 1, false, 5),
('fpc-agile-requirements', 'agile', 'requirements', 2, true, 7),
('fpc-agile-analysis', 'agile', 'analysis', 3, true, 14),
('fpc-agile-design', 'agile', 'design', 4, true, 14),
('fpc-agile-development', 'agile', 'development', 5, true, 28),
('fpc-agile-testing', 'agile', 'testing', 6, true, 7),
('fpc-agile-deployment', 'agile', 'deployment', 7, true, 3);

-- Phase Deliverable Config (Agile - Analysis)
INSERT INTO phase_deliverable_config (id, flow_phase_config_id, deliverable_code, is_required, "order") VALUES
('pdc-agile-analysis-uc', 'fpc-agile-analysis', 'use_cases', true, 1),
('pdc-agile-analysis-us', 'fpc-agile-analysis', 'user_stories', true, 2),
('pdc-agile-analysis-ac', 'fpc-agile-analysis', 'acceptance_criteria', true, 3);

-- (continuar para otras fases...)
```

---

## 10. ¿ES BLOQUEANTE?

**No.** Los templates son sugerencias de configuración.

| Situación | ¿Bloquea? |
|-----------|-----------|
| Crear proyecto sin template | ⚠️ Debe ser "custom" |
| Template sin fases | ❌ No (proyecto vacío) |
| Cambiar template después de crear | ❌ No es posible (ya clonado) |

---

## 11. RESPONSABLES

| Acción | Admin VTT | PM | TL | Agente |
|--------|-----------|----|----|--------|
| Crear template | ✅ | ❌ | ❌ | ❌ |
| Modificar template | ✅ | ❌ | ❌ | ❌ |
| Ver templates | ✅ | ✅ | ✅ | ✅ |
| Seleccionar template al crear proyecto | ✅ | ✅ | ❌ | ❌ |

---

## 12. INTEGRACIÓN CON OTRAS FEATURES

| Feature | Integración |
|---------|-------------|
| **Catálogos Base** | Usa phases y deliverables del catálogo |
| **UX Wizard** | Paso 2 selecciona template |
| **Project Folders** | Crea carpetas según fases del template |
| **Releases/Sprints** | Hereda estructura de fases |

---

## 13. FAQ

**¿Puedo crear mis propios templates?**
No desde la UI. Solo Admin VTT puede crear templates globales.

**¿Qué pasa si elijo Custom?**
El proyecto se crea sin fases ni deliverables. Debes configurar todo manualmente.

**¿Puedo cambiar de template después de crear el proyecto?**
No. El template se clona al crear. Después solo puedes modificar la configuración local del proyecto.

**¿Los templates afectan los sprints?**
No directamente. Los sprints son independientes de las fases del template.

---

**Documento:** FEATURE_FLOW_TEMPLATES.md  
**Versión:** 1.0  
**Fecha:** 2026-05-06
