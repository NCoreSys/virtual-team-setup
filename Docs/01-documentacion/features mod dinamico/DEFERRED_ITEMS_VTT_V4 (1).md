x|# DEFERRED ITEMS — VTT V4

| Campo | Valor |
|-------|-------|
| **Documento** | DEFERRED_ITEMS_VTT_V4.md |
| **Versión** | 1.0 |
| **Fecha** | 2026-04-12 |
| **Estado** | 🔄 ACTIVO |

---

## PROPÓSITO

Este documento registra items diferidos identificados durante el análisis de features que no se implementarán inmediatamente pero deben ser trackeados para futuras iteraciones.

---

## DEFERRED ITEMS

### DI-001: Wizard V2 — Configuración de Features

| Campo | Valor |
|-------|-------|
| **ID** | DI-001 |
| **Título** | Wizard V2 — Paso de configuración de features |
| **Origen** | Análisis de Feature Firmas |
| **Fecha identificado** | 2026-04-12 |
| **Prioridad** | P1 |
| **Estimación** | Por definir |

**Descripción:**

Agregar un paso adicional al wizard de creación de proyecto donde el usuario configure las features disponibles:

- Firmas (niveles, firmantes por default)
- Hardcode check (habilitado/deshabilitado, tipos de tarea)
- Plan/Fechas (movimiento de fechas, recálculo automático)
- Otras features por identificar

**Razón del diferimiento:**

No modificar el wizard ahora porque hay más features que pueden requerir configuración. Mejor acumular todos los cambios y hacer una sola modificación.

**Dependencias:**

- Análisis completo de todas las features
- Identificación de qué features requieren configuración
- Diseño UX del nuevo paso del wizard

---

### DI-002: Settings — Configuración de Features Post-Creación

| Campo | Valor |
|-------|-------|
| **ID** | DI-002 |
| **Título** | Settings de proyecto — Edición de configuración de features |
| **Origen** | Análisis de Feature Firmas |
| **Fecha identificado** | 2026-04-12 |
| **Prioridad** | P1 |
| **Estimación** | Por definir |

**Descripción:**

Las mismas opciones del wizard (DI-001) deben estar disponibles en Settings del proyecto para que el usuario pueda modificar la configuración después de crear el proyecto.

**Restricciones:**

- Algunas configuraciones solo editables si no hay datos (ej: firmas si no hay firmas registradas)
- Solo usuario humano puede editar, no agentes

**Dependencias:**

- DI-001 (definir primero qué va en wizard)

---

### DI-003: Algoritmo de Firmantes por Nivel de Usuario

| Campo | Valor |
|-------|-------|
| **ID** | DI-003 |
| **Título** | Algoritmo para calcular firmantes según nivel de autoridad |
| **Origen** | Análisis de Feature Firmas |
| **Fecha identificado** | 2026-04-12 |
| **Prioridad** | P2 |
| **Estimación** | ~8h |

**Descripción:**

Crear algoritmo que determine automáticamente quiénes son los firmantes requeridos para cada nivel (tarea, entregable, sprint, fase, release) basado en:

1. Usuarios asignados al proyecto
2. Nivel de autoridad de cada usuario (ejecutor, revisor, aprobador)
3. Fase actual
4. Configuración del catálogo de fases

**Pseudo-algoritmo:**

```
function getRequiredSigners(level, context):
  users = getProjectUsers(context.projectId)
  phase = getPhase(context.phaseId)
  
  for each user in users:
    if user.authorityLevel >= level.requiredAuthority:
      if user.role in phase.defaultSigners:
        signers.add(user)
  
  return signers
```

**Dependencias:**

- Definir niveles de autoridad en modelo de usuarios
- Actualizar catálogo de fases con firmantes default

---

### DI-004: Firmantes en Handoff

| Campo | Valor |
|-------|-------|
| **ID** | DI-004 |
| **Título** | Sección de firmantes y flujo de aprobación en Handoff |
| **Origen** | Análisis de Feature Firmas |
| **Fecha identificado** | 2026-04-12 |
| **Prioridad** | P2 |
| **Estimación** | ~4h |

**Descripción:**

Agregar sección en el template de Handoff que defina explícitamente:

- Firmantes por nivel (stage, sprint, release)
- Niveles de autoridad
- Flujo de aprobaciones
- Override de firmantes default si es necesario

**Ejemplo de sección:**

```markdown
## FIRMANTES Y APROBACIONES

### Sprint S05
| Nivel | Firmantes | Obligatorio |
|-------|-----------|-------------|
| Stage Development | DB, BE, FE | Todos |
| Stage Testing | QA | Sí |
| Sprint | TL, AR, QA | Sí |

### Release MVP
| Firmante | Rol | Obligatorio |
|----------|-----|-------------|
| @pjm-agent | PJM | ✅ |
| @martin | PM | ✅ |
```

**Dependencias:**

- DI-003 (para calcular firmantes automáticamente)

---

### DI-005: Hardcode Check — Aplicabilidad por Tipo de Tarea

| Campo | Valor |
|-------|-------|
| **ID** | DI-005 |
| **Título** | Configurar cuándo aplica hardcode check según tipo de tarea/proyecto |
| **Origen** | Análisis de Feature Hardcode |
| **Fecha identificado** | 2026-04-12 |
| **Prioridad** | P2 |
| **Estimación** | ~6h |

**Descripción:**

El hardcode check no debe aplicar a todas las tareas ni a todos los proyectos. Necesita configuración:

**Por proyecto:**

| Tipo de proyecto | ¿Aplica hardcode? |
|------------------|-------------------|
| Software | ✅ Sí |
| Marketing | ❌ No |
| Research | ❌ No |
| Custom | Configurable |

**Por tipo de tarea:**

| Tipo de tarea | ¿Aplica hardcode? |
|---------------|-------------------|
| Development | ✅ Sí |
| Bugfix | ✅ Sí |
| Analysis | ❌ No |
| Documentation | ❌ No |
| Design | ❌ No |

**Por severidad de cambio:**

| Cambio | ¿Requiere hardcode check completo? |
|--------|-------------------------------------|
| Nueva feature | ✅ Sí |
| Bug crítico | ✅ Sí |
| Bug menor (cambio de color) | ❌ No, o check reducido |

**Dependencias:**

- DI-001 (configuración en wizard)
- DI-002 (editable en settings)

---

### DI-006: Catálogo de Tipos de Tarea

| Campo | Valor |
|-------|-------|
| **ID** | DI-006 |
| **Título** | Crear catálogo de tipos de tarea con configuración de features |
| **Origen** | Análisis de Features Firmas y Hardcode |
| **Fecha identificado** | 2026-04-12 |
| **Prioridad** | P2 |
| **Estimación** | ~4h |

**Descripción:**

Crear un catálogo `task_type_catalog` que permita configurar por tipo de tarea qué features aplican:

```prisma
model TaskTypeCatalog {
  code                String   @id
  name                String
  description         String?
  
  // Configuración de features
  requiresSignature   Boolean  @default(true)
  requiresHardcodeCheck Boolean @default(true)
  requiresCriteria    Boolean  @default(true)
  requiresDevlog      Boolean  @default(true)
  
  // Metadata
  isActive            Boolean  @default(true)
  order               Int      @default(0)
}
```

**Tipos iniciales:**

| code | name | signature | hardcode | criteria |
|------|------|-----------|----------|----------|
| `development` | Development | ✅ | ✅ | ✅ |
| `bugfix` | Bug Fix | ✅ | ✅ | ✅ |
| `analysis` | Analysis | ❌ | ❌ | ✅ |
| `documentation` | Documentation | ❌ | ❌ | ✅ |
| `design` | Design | ❌ | ❌ | ✅ |
| `research` | Research | ❌ | ❌ | ❌ |
| `meeting` | Meeting | ❌ | ❌ | ❌ |

---

### DI-007: Configuración de Plan y Fechas

| Campo | Valor |
|-------|-------|
| **ID** | DI-007 |
| **Título** | Configuración de manejo de plan y fechas del proyecto |
| **Origen** | Análisis de Feature Firmas (mención) |
| **Fecha identificado** | 2026-04-12 |
| **Prioridad** | P3 |
| **Estimación** | Por definir |

**Descripción:**

Configuración de cómo se maneja el plan del proyecto:

- ¿Se pueden mover fechas de tareas?
- ¿Se recalcula automáticamente el plan?
- ¿Hay fechas bloqueadas?
- ¿Cómo se manejan dependencias al mover fechas?

**Nota:** Este item está mencionado pero no analizado. Requiere análisis completo.

### DI-008: Gate Automático de Transición de Fases

| Campo | Valor |
|-------|-------|
| **ID** | DI-008 |
| **Título** | Gate automático para transición entre fases |
| **Origen** | Memory Service — Planning → Analysis (2026-05-06) |
| **Fecha identificado** | 2026-05-06 |
| **Prioridad** | P2 |
| **Estimación** | ~6h |
| **Documento relacionado** | FEATURE_PHASE_TRANSITIONS.md |

**Descripción:**

Definir qué sucede después de que un sprint es firmado y cómo se transiciona entre fases:

- MVP: Sprint firmado = fase cerrada, siguiente fase puede iniciar sin gate
- Futuro: Gate automático que valide checklist antes de habilitar siguiente fase

**Decisión PM:** Opción B (Gate automático) para implementación futura. MVP usa Opción A (sin gate).

**Pendientes técnicos:**

1. Exponer UUID de `phase_completed` del status_catalog
2. Definir si cierre de fase es automático al firmar sprint
3. Documentar proceso en guía de agentes

**Dependencias:**

- Feature Firmas completada
- Status catalog accesible via API

---

### DI-009: Tabla criteria_template para DoD/DoR

| Campo | Valor |
|-------|-------|
| **ID** | DI-009 |
| **Título** | Tabla criteria_template para templates de DoD/DoR |
| **Origen** | PROPUESTA_CRITERIA_TRAZABILIDAD_VTT.md (P1) |
| **Fecha identificado** | 2026-05-06 |
| **Prioridad** | P1 |
| **Estimación** | ~16h |

**Descripción:**

Crear tabla `criteria_template` con dos niveles de scope:
- Global: aplica a todos los proyectos de un `projectTypeCode`
- Proyecto: específico de un proyecto

Los templates se heredan automáticamente al crear tareas según su `taskTypeCode`.

**Modelo:**

```sql
CREATE TABLE criteria_template (
  id TEXT PRIMARY KEY,
  code VARCHAR(50) NOT NULL,
  name VARCHAR(255),
  description TEXT,
  criteria_type_code VARCHAR(50) REFERENCES criteria_type_catalog(code),
  scope VARCHAR(50) NOT NULL,  -- 'global' o 'project'
  project_type_code VARCHAR(50),
  project_id TEXT,
  task_type_code VARCHAR(50),
  is_required BOOLEAN DEFAULT true,
  is_active BOOLEAN DEFAULT true,
  sort_order INT DEFAULT 0
);
```

**Dependencias:**
- DI-010 (task_type_catalog)

---

### DI-010: Tabla task_type_catalog

| Campo | Valor |
|-------|-------|
| **ID** | DI-010 |
| **Título** | Catálogo de tipos de tarea (backend, frontend, docs, etc.) |
| **Origen** | PROPUESTA_CRITERIA_TRAZABILIDAD_VTT.md (P3) |
| **Fecha identificado** | 2026-05-06 |
| **Prioridad** | P1 |
| **Estimación** | ~6h |

**Descripción:**

Crear catálogo que clasifica tareas por tipo de trabajo. Determina qué DoD template se hereda.

**Tipos iniciales:** backend, frontend, database, documentation, testing, devops, design, research, meeting

**Modelo:**

```sql
CREATE TABLE task_type_catalog (
  code VARCHAR(50) PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  parent_category VARCHAR(50),
  project_type_code VARCHAR(50),
  dod_template_group VARCHAR(50),
  sort_order INT DEFAULT 0,
  is_active BOOLEAN DEFAULT true
);

ALTER TABLE tasks ADD COLUMN task_type_code VARCHAR(50) REFERENCES task_type_catalog(code);
```

**Dependencias:** Ninguna

---

### DI-011: Lógica de herencia de templates al crear tarea

| Campo | Valor |
|-------|-------|
| **ID** | DI-011 |
| **Título** | Hook de herencia de criteria templates al crear tarea |
| **Origen** | PROPUESTA_CRITERIA_TRAZABILIDAD_VTT.md (P1) |
| **Fecha identificado** | 2026-05-06 |
| **Prioridad** | P1 |
| **Estimación** | ~8h |

**Descripción:**

Al crear una tarea, el sistema debe:
1. Obtener `taskTypeCode` (inferido del rol o explícito)
2. Buscar templates globales + de proyecto
3. Combinar (proyecto override global)
4. Crear criteria automáticamente en la tarea

**Dependencias:**
- DI-009 (criteria_template)
- DI-010 (task_type_catalog)

---

### DI-012: DoR bloqueante con override

| Campo | Valor |
|-------|-------|
| **ID** | DI-012 |
| **Título** | Validación DoR bloqueante al iniciar tarea |
| **Origen** | PROPUESTA_CRITERIA_TRAZABILIDAD_VTT.md (P2) |
| **Fecha identificado** | 2026-05-06 |
| **Prioridad** | P1 |
| **Estimación** | ~8h |

**Descripción:**

Al intentar mover tarea a `in_progress`, validar que todos los criterios tipo `dor` estén cumplidos. Si no, bloquear con opción de override.

**Request extendido:**

```json
{
  "statusCode": "in_progress",
  "overrideReason": "string (requerido si hay DoR pendientes)"
}
```

**Dependencias:**
- DI-009 (templates para tener DoR)

---

### DI-013: Campos adicionales en acceptance_criteria

| Campo | Valor |
|-------|-------|
| **ID** | DI-013 |
| **Título** | Campos nuevos en acceptance_criteria (desactivación, deprecación, fulfillment dual, testing) |
| **Origen** | DECISIONES_CRITERIA_SYSTEM_Q1-Q7.md |
| **Fecha identificado** | 2026-05-06 |
| **Prioridad** | P1 |
| **Estimación** | ~6h |

**Descripción:**

Agregar campos para:
- Q1: `isApplicable`, `disabledReason`, `disabledBy`
- Q3: `acStatus`, `supersededBy`
- Q5: `fulfillmentStatus`, `reportedBy`, `reportedAt`, `verifiedBy`, `verifiedAt`, etc.
- Q6: `testResult`, `executedAt`, `evidence`, `defectId`

**Dependencias:** Ninguna (alter table)

---

### DI-014: Tipos dod y dor en criteria_type_catalog

| Campo | Valor |
|-------|-------|
| **ID** | DI-014 |
| **Título** | Agregar tipos dod y dor al catálogo de criterios |
| **Origen** | PROPUESTA_CRITERIA_TRAZABILIDAD_VTT.md |
| **Fecha identificado** | 2026-05-06 |
| **Prioridad** | P0 (seed) |
| **Estimación** | ~0.5h |

**Descripción:**

Agregar al seed de `criteria_type_catalog`:

```sql
INSERT INTO criteria_type_catalog (code, name, description) VALUES
  ('dod', 'Definition of Done', 'Criterio de completitud de tarea'),
  ('dor', 'Definition of Ready', 'Precondición para iniciar tarea');
```

**Dependencias:** Ninguna

---

## RESUMEN

| ID | Título | Prioridad | Dependencias |
|----|--------|-----------|--------------|
| DI-001 | Wizard V2 — Config de Features | P1 | — |
| DI-002 | Settings — Config de Features | P1 | DI-001 |
| DI-003 | Algoritmo de Firmantes | P2 | — |
| DI-004 | Firmantes en Handoff | P2 | DI-003 |
| DI-005 | Hardcode — Aplicabilidad | P2 | DI-001, DI-002 |
| DI-006 | Catálogo Tipos de Tarea | P2 | — |
| DI-007 | Config de Plan y Fechas | P3 | Por analizar |
| DI-008 | Gate Transición de Fases | P2 | Feature Firmas |
| DI-009 | Tabla criteria_template | P1 | DI-010 |
| DI-010 | Tabla task_type_catalog | P1 | — |
| DI-011 | Herencia de templates | P1 | DI-009, DI-010 |
| DI-012 | DoR bloqueante | P1 | DI-009 |
| DI-013 | Campos acceptance_criteria | P1 | — |
| DI-014 | Tipos dod/dor en catálogo | P0 | — |

### Orden de implementación recomendado

```
DI-014 (seed)
    │
    ▼
DI-010 (task_type_catalog)
    │
    ▼
DI-009 (criteria_template)
    │
    ├─► DI-011 (herencia)
    │
    └─► DI-012 (DoR bloqueante)
    
DI-013 (campos) — paralelo

DI-001..DI-008 — según necesidad
```

### Estimación total nuevos items (DI-009 a DI-014)

| Item | Horas |
|------|-------|
| DI-009 | 16h |
| DI-010 | 6h |
| DI-011 | 8h |
| DI-012 | 8h |
| DI-013 | 6h |
| DI-014 | 0.5h |
| **Total** | **44.5h** |

---

## CÓMO AGREGAR NUEVOS ITEMS

Al identificar un nuevo deferred item durante análisis de features:

1. Asignar ID secuencial (DI-XXX)
2. Documentar con el formato de este documento
3. Asignar prioridad inicial (P1/P2/P3)
4. Identificar dependencias
5. Agregar al resumen

---

**Documento:** DEFERRED_ITEMS_VTT_V4.md  
**Versión:** 1.0  
**Fecha:** 2026-04-12
