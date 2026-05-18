# FEATURE: CATÁLOGOS BASE

| Campo | Valor |
|-------|-------|
| **Feature** | Catálogos Base |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-06 |
| **Sprint origen** | S01 |
| **Estado** | ✅ Implementado (BE/DB) |

---

## 1. QUÉ ES

Conjunto de catálogos globales que definen la configuración base del sistema. Son tablas de referencia que se comparten entre todos los proyectos y permiten la configuración dinámica.

---

## 2. PARA QUÉ SIRVE

- **Estandarización** — Todos los proyectos usan los mismos tipos, fases y deliverables
- **Configuración dinámica** — Sin hardcodear valores en el código
- **Extensibilidad** — Agregar nuevos tipos sin modificar código
- **Consistencia** — Nomenclatura uniforme en todo el sistema

---

## 3. CATÁLOGOS

### 3.1 Project Type Catalog

Define los tipos de proyecto disponibles.

| code | name | description | icon |
|------|------|-------------|------|
| `software` | Software Development | Desarrollo de software tradicional | `lucide:code` |
| `marketing` | Marketing Campaign | Campañas de marketing | `lucide:megaphone` |
| `research` | Research Project | Proyectos de investigación | `lucide:search` |
| `operations` | Operations | Proyectos operativos | `lucide:settings` |
| `custom` | Custom | Configuración personalizada | `lucide:sliders` |

### 3.2 Phase Catalog

Define las fases del ciclo de vida de proyectos.

| code | name | order | isRequired | defaultDuration | projectTypes |
|------|------|-------|------------|-----------------|--------------|
| `discovery` | Discovery | 1 | false | 5 | software |
| `requirements` | Requirements | 2 | true | 10 | software |
| `analysis` | Analysis | 3 | true | 15 | software |
| `design` | Design | 4 | true | 10 | software |
| `development` | Development | 5 | true | 30 | software |
| `testing` | Testing | 6 | true | 10 | software |
| `deployment` | Deployment | 7 | true | 5 | software |
| `maintenance` | Maintenance | 8 | false | 0 | software |

### 3.3 Deliverable Catalog

Define los tipos de entregables por fase.

| code | name | phaseCode | isRequired | description |
|------|------|-----------|------------|-------------|
| `problem_statement` | Problem Statement | discovery | false | Definición del problema |
| `value_proposition` | Value Proposition | discovery | false | Propuesta de valor |
| `requirements_list` | Requirements List | requirements | true | Lista de requerimientos |
| `use_cases` | Use Cases | analysis | true | Casos de uso |
| `user_stories` | User Stories | analysis | true | Historias de usuario |
| `acceptance_criteria` | Acceptance Criteria | analysis | true | Criterios de aceptación |
| `wireframes` | Wireframes | design | false | Wireframes UX |
| `mockups` | Mockups | design | false | Mockups UI |
| `architecture` | Architecture Doc | design | true | Documento de arquitectura |
| `spec` | Technical Spec | design | true | Especificación técnica |
| `source_code` | Source Code | development | true | Código fuente |
| `api_docs` | API Documentation | development | false | Documentación de API |
| `test_plan` | Test Plan | testing | true | Plan de pruebas |
| `test_results` | Test Results | testing | true | Resultados de pruebas |
| `deployment_guide` | Deployment Guide | deployment | true | Guía de despliegue |
| `release_notes` | Release Notes | deployment | true | Notas de versión |

### 3.4 Trackable Type Catalog

Define los tipos de items rastreables.

| code | name | description | icon |
|------|------|-------------|------|
| `rf` | Requerimiento Funcional | Comportamiento esperado del sistema | `lucide:check-circle` |
| `rnf` | Requerimiento No Funcional | Requisitos de calidad | `lucide:shield` |
| `adr` | Architecture Decision Record | Decisión arquitectónica | `lucide:git-branch` |
| `kpi` | Key Performance Indicator | Métrica de éxito | `lucide:bar-chart` |
| `risk` | Riesgo | Riesgo identificado | `lucide:alert-triangle` |
| `constraint` | Restricción | Limitación del proyecto | `lucide:lock` |
| `assumption` | Supuesto | Supuesto asumido | `lucide:help-circle` |
| `dependency` | Dependencia Externa | Dependencia de terceros | `lucide:external-link` |
| `bug` | Bug | Defecto encontrado | `lucide:bug` |

---

## 4. CARACTERÍSTICAS

### 4.1 Inmutabilidad desde proyectos

Los catálogos son **solo lectura** desde la perspectiva de los proyectos. Solo Admin VTT puede modificarlos.

```
Proyecto → Lee catálogos → Crea instancias locales
                ↓
        NO puede modificar catálogos
```

### 4.2 Herencia

Al crear un proyecto, se **copian** las configuraciones relevantes del catálogo. Los cambios posteriores al catálogo NO afectan proyectos existentes.

### 4.3 Filtrado por tipo de proyecto

Algunos elementos del catálogo solo aplican a ciertos tipos de proyecto.

```
GET /api/phases?projectTypeCode=software
→ Solo fases aplicables a software
```

---

## 5. FLUJO OPERATIVO

### 5.1 Consultar catálogos

```
GET /api/project-types
GET /api/phases
GET /api/deliverables
GET /api/trackable-types
```

### 5.2 Filtrar por tipo de proyecto

```
GET /api/phases?projectTypeCode=software
GET /api/deliverables?phaseCode=analysis
```

### 5.3 Crear proyecto usando catálogos

```
POST /api/projects
{
  "name": "Memory Service",
  "projectTypeCode": "software",
  "flowTemplateCode": "agile"
}

→ Sistema lee catálogos
→ Copia fases según flow template
→ Copia deliverables por fase
→ Proyecto creado con configuración inicial
```

---

## 6. ENDPOINTS

### Project Types

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/project-types` | Listar tipos de proyecto |
| GET | `/api/project-types/:code` | Ver tipo específico |

### Phases

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/phases` | Listar fases |
| GET | `/api/phases?projectTypeCode=X` | Filtrar por tipo de proyecto |
| GET | `/api/phases/:code` | Ver fase específica |

### Deliverables

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/deliverables` | Listar deliverables |
| GET | `/api/deliverables?phaseCode=X` | Filtrar por fase |
| GET | `/api/deliverables/:code` | Ver deliverable específico |

### Trackable Types

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/trackable-types` | Listar tipos rastreables |
| GET | `/api/trackable-types/:code` | Ver tipo específico |

---

## 7. TABLAS EN BASE DE DATOS

### project_type_catalog

```sql
CREATE TABLE project_type_catalog (
  code VARCHAR(50) PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  icon_url VARCHAR(255),
  icon_type VARCHAR(100),
  default_flow_template VARCHAR(50),
  is_active BOOLEAN DEFAULT true,
  sort_order INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### phase_catalog

```sql
CREATE TABLE phase_catalog (
  code VARCHAR(50) PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  "order" INT NOT NULL,
  is_required BOOLEAN DEFAULT true,
  default_duration_days INT,
  icon_url VARCHAR(255),
  icon_type VARCHAR(100),
  applicable_project_types TEXT[],
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_phase_order ON phase_catalog("order");
```

### deliverable_catalog

```sql
CREATE TABLE deliverable_catalog (
  code VARCHAR(50) PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  phase_code VARCHAR(50) NOT NULL REFERENCES phase_catalog(code),
  is_required BOOLEAN DEFAULT false,
  template_path VARCHAR(255),
  icon_url VARCHAR(255),
  icon_type VARCHAR(100),
  is_active BOOLEAN DEFAULT true,
  sort_order INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_deliverable_phase ON deliverable_catalog(phase_code);
```

### trackable_type_catalog

```sql
CREATE TABLE trackable_type_catalog (
  code VARCHAR(50) PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  icon_url VARCHAR(255),
  icon_type VARCHAR(100),
  is_active BOOLEAN DEFAULT true,
  sort_order INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 8. SEEDS

```sql
-- Project Types
INSERT INTO project_type_catalog (code, name, description, icon_type, sort_order) VALUES
('software', 'Software Development', 'Desarrollo de software tradicional', 'lucide:code', 1),
('marketing', 'Marketing Campaign', 'Campañas de marketing', 'lucide:megaphone', 2),
('research', 'Research Project', 'Proyectos de investigación', 'lucide:search', 3),
('operations', 'Operations', 'Proyectos operativos', 'lucide:settings', 4),
('custom', 'Custom', 'Configuración personalizada', 'lucide:sliders', 5);

-- Phases (software)
INSERT INTO phase_catalog (code, name, "order", is_required, default_duration_days, icon_type, applicable_project_types) VALUES
('discovery', 'Discovery', 1, false, 5, 'lucide:compass', ARRAY['software']),
('requirements', 'Requirements', 2, true, 10, 'lucide:clipboard-list', ARRAY['software']),
('analysis', 'Analysis', 3, true, 15, 'lucide:file-search', ARRAY['software']),
('design', 'Design', 4, true, 10, 'lucide:palette', ARRAY['software']),
('development', 'Development', 5, true, 30, 'lucide:code', ARRAY['software']),
('testing', 'Testing', 6, true, 10, 'lucide:test-tube', ARRAY['software']),
('deployment', 'Deployment', 7, true, 5, 'lucide:rocket', ARRAY['software']),
('maintenance', 'Maintenance', 8, false, 0, 'lucide:wrench', ARRAY['software']);

-- Deliverables
INSERT INTO deliverable_catalog (code, name, phase_code, is_required, icon_type, sort_order) VALUES
('problem_statement', 'Problem Statement', 'discovery', false, 'lucide:file-text', 1),
('value_proposition', 'Value Proposition', 'discovery', false, 'lucide:target', 2),
('requirements_list', 'Requirements List', 'requirements', true, 'lucide:list', 1),
('use_cases', 'Use Cases', 'analysis', true, 'lucide:users', 1),
('user_stories', 'User Stories', 'analysis', true, 'lucide:book-open', 2),
('acceptance_criteria', 'Acceptance Criteria', 'analysis', true, 'lucide:check-square', 3),
('wireframes', 'Wireframes', 'design', false, 'lucide:layout', 1),
('mockups', 'Mockups', 'design', false, 'lucide:image', 2),
('architecture', 'Architecture Doc', 'design', true, 'lucide:git-branch', 3),
('spec', 'Technical Spec', 'design', true, 'lucide:file-code', 4),
('source_code', 'Source Code', 'development', true, 'lucide:code', 1),
('api_docs', 'API Documentation', 'development', false, 'lucide:book', 2),
('test_plan', 'Test Plan', 'testing', true, 'lucide:clipboard-check', 1),
('test_results', 'Test Results', 'testing', true, 'lucide:check-circle', 2),
('deployment_guide', 'Deployment Guide', 'deployment', true, 'lucide:file-text', 1),
('release_notes', 'Release Notes', 'deployment', true, 'lucide:tag', 2);

-- Trackable Types (ya en SEED_CATALOGOS_VTT_V4.sql)
```

---

## 9. ¿ES BLOQUEANTE?

**No.** Los catálogos son informativos y configurativos.

| Situación | ¿Bloquea? |
|-----------|-----------|
| Catálogo vacío | ❌ No (pero wizard no funcionará) |
| Tipo de proyecto inactivo | ⚠️ No se puede seleccionar |
| Fase sin deliverables | ❌ No |

---

## 10. RESPONSABLES

| Acción | Admin VTT | PM | TL | Agente |
|--------|-----------|----|----|--------|
| Crear entrada en catálogo | ✅ | ❌ | ❌ | ❌ |
| Modificar catálogo | ✅ | ❌ | ❌ | ❌ |
| Desactivar entrada | ✅ | ❌ | ❌ | ❌ |
| Leer catálogos | ✅ | ✅ | ✅ | ✅ |

---

## 11. INTEGRACIÓN CON OTRAS FEATURES

| Feature | Integración |
|---------|-------------|
| **Flow Templates** | Usa phases y deliverables del catálogo |
| **Wizard** | Muestra opciones desde catálogos |
| **Trackable Items** | Usa trackable_type_catalog |
| **Releases/Sprints** | Heredan estructura de fases |

---

## 12. FAQ

**¿Puedo agregar mis propios tipos de proyecto?**
No desde la UI. Solo Admin VTT puede agregar al catálogo global.

**¿Qué pasa si desactivo una fase?**
Proyectos existentes no se afectan. Nuevos proyectos no la verán.

**¿Los deliverables son obligatorios?**
Depende del campo `isRequired`. El sistema advierte pero no bloquea.

**¿Puedo tener fases custom por proyecto?**
Sí, después de crear el proyecto puedes agregar/quitar fases en la instancia local.

---

**Documento:** FEATURE_CATALOGOS_BASE.md  
**Versión:** 1.0  
**Fecha:** 2026-05-06
