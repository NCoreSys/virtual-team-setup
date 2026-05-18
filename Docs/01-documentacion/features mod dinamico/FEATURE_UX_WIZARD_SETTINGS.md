# FEATURE: UX WIZARD Y SETTINGS

| Campo | Valor |
|-------|-------|
| **Feature** | UX Wizard y Settings de Proyecto |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-06 |
| **Sprint origen** | S11 |
| **Estado** | ✅ Diseñado — FE pendiente |

---

## 1. QUÉ ES

Interfaz de usuario para crear y configurar proyectos. Incluye:
- **Wizard** — Asistente de 7 pasos para crear proyectos
- **Settings** — Pantallas de configuración post-creación

---

## 2. PARA QUÉ SIRVE

- **Onboarding** — Guiar al usuario en la creación de proyectos
- **Configuración** — Personalizar fases, deliverables, sprints
- **Flexibilidad** — Modificar configuración después de crear
- **UX** — Experiencia guiada y clara

---

## 3. WIZARD DE CREACIÓN (7 PASOS)

### 3.1 Flujo completo

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           WIZARD DE CREACIÓN                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [1]        [2]          [3]         [4]          [5]         [6]    [7]   │
│  Tipo  →  Metodología → Sprints → Fases → Deliverables → Resumen → Crear  │
│                                                                             │
│  ════════════════════════════════════════════════════════════════════════  │
│                                                                             │
│  P1: ¿Qué tipo de proyecto es?                                             │
│      ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐                       │
│      │ 💻      │ │ 📢      │ │ 🔬      │ │ ⚙️      │                       │
│      │Software │ │Marketing│ │Research │ │Custom   │                       │
│      └─────────┘ └─────────┘ └─────────┘ └─────────┘                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Paso 1: Tipo de Proyecto

**Pantalla:** `ProjectTypeSelector`

| Elemento | Descripción |
|----------|-------------|
| Cards | Una card por tipo de proyecto del catálogo |
| Icono | Icono del tipo |
| Nombre | Nombre del tipo |
| Descripción | Descripción breve |
| Selección | Click selecciona, solo uno activo |

**Datos:** `GET /api/project-types`

### 3.3 Paso 2: Metodología

**Pantalla:** `FlowTemplateSelector`

| Elemento | Descripción |
|----------|-------------|
| Cards | Templates disponibles para el tipo seleccionado |
| Preview | Muestra fases incluidas al hover |
| Default | El template marcado como default viene preseleccionado |
| Custom | Opción para configuración manual |

**Datos:** `GET /api/flow-templates?projectTypeCode={type}`

### 3.4 Paso 3: Configuración de Sprints

**Pantalla:** `SprintConfigPanel`

| Elemento | Descripción |
|----------|-------------|
| Toggle | ¿Usar sprints? Sí/No |
| Duración | Slider o input: 1-4 semanas |
| Velocidad | Story points default por sprint |
| Info | Explicación de qué son los sprints |

**Comportamiento:**
- Si No → Proyecto sin estructura de sprints (trabajo continuo)
- Si Sí → Se habilitan releases y sprints

### 3.5 Paso 4: Configuración de Fases

**Pantalla:** `PhaseListEditor`

| Elemento | Descripción |
|----------|-------------|
| Lista | Fases del template seleccionado |
| Drag & Drop | Reordenar fases |
| Toggle | Habilitar/deshabilitar fase |
| Required | Indicador si es obligatoria |
| Agregar | Botón para agregar fase del catálogo |

**Componentes:**
- `PhaseItem` — Cada fase con controles
- `PhaseCatalogPicker` — Modal para agregar fases

### 3.6 Paso 5: Configuración de Deliverables

**Pantalla:** `DeliverableAccordion`

| Elemento | Descripción |
|----------|-------------|
| Acordeón | Una sección por fase |
| Checkboxes | Deliverables de la fase |
| Required | Indicador si es obligatorio |
| Agregar | Botón para agregar del catálogo |

**Componentes:**
- `DeliverableCheckbox` — Cada deliverable
- `DeliverableCatalogPicker` — Modal para agregar

### 3.7 Paso 6: Resumen

**Pantalla:** `ProjectSummaryCard`

| Sección | Contenido |
|---------|-----------|
| General | Nombre, tipo, metodología |
| Sprints | Configuración de sprints |
| Fases | Lista de fases seleccionadas |
| Deliverables | Conteo por fase |
| Warnings | Alertas si falta algo |

**Acciones:**
- Editar nombre del proyecto
- Agregar descripción
- Volver a cualquier paso

### 3.8 Paso 7: Confirmación

**Pantalla:** `CreateProjectConfirmation`

| Elemento | Descripción |
|----------|-------------|
| Botón | "Crear Proyecto" |
| Loading | Spinner mientras se crea |
| Success | Redirect al proyecto creado |
| Error | Mensaje de error si falla |

**Request:**
```json
POST /api/projects
{
  "name": "Memory Service",
  "description": "Microservicio de memoria para VTT",
  "projectTypeCode": "software",
  "flowTemplateCode": "agile",
  "config": {
    "sprintsEnabled": true,
    "sprintDuration": 14,
    "defaultVelocity": 21,
    "phases": [...],
    "deliverables": [...]
  }
}
```

---

## 4. NAVEGACIÓN DEL WIZARD

### 4.1 Componente WizardStepper

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  ● ──────── ● ──────── ○ ──────── ○ ──────── ○ ──────── ○ ──────── ○       │
│  Tipo    Metodología  Sprints   Fases   Deliverables  Resumen    Crear    │
│  ✓           ✓          →                                                   │
│                                                                             │
│  [← Anterior]                                            [Siguiente →]      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Estados de paso

| Estado | Icono | Color | Significado |
|--------|-------|-------|-------------|
| Completado | ✓ | Verde | Paso finalizado |
| Actual | → | Azul | Paso activo |
| Pendiente | ○ | Gris | No visitado |
| Error | ⚠ | Rojo | Requiere atención |

### 4.3 Validaciones por paso

| Paso | Validación | Mensaje si falla |
|------|------------|------------------|
| 1 | Tipo seleccionado | "Selecciona un tipo de proyecto" |
| 2 | Template seleccionado | "Selecciona una metodología" |
| 3 | — | (Opcional) |
| 4 | Al menos 1 fase | "Selecciona al menos una fase" |
| 5 | — | (Opcional) |
| 6 | Nombre no vacío | "Ingresa un nombre para el proyecto" |
| 7 | — | (Submit) |

---

## 5. SETTINGS POST-CREACIÓN

### 5.1 Estructura de tabs

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Settings del Proyecto                                              [×]    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [General]  [Fases]  [Deliverables]  [Sprints]  [Features]                 │
│  ─────────                                                                  │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                     │   │
│  │  Nombre del proyecto                                                │   │
│  │  ┌─────────────────────────────────────────────────────────────┐   │   │
│  │  │ Memory Service                                              │   │   │
│  │  └─────────────────────────────────────────────────────────────┘   │   │
│  │                                                                     │   │
│  │  Descripción                                                        │   │
│  │  ┌─────────────────────────────────────────────────────────────┐   │   │
│  │  │ Microservicio de memoria para agentes AI                   │   │   │
│  │  └─────────────────────────────────────────────────────────────┘   │   │
│  │                                                                     │   │
│  │  Tipo de proyecto                                                   │   │
│  │  [Software Development    ▼]  (no editable post-creación)         │   │
│  │                                                                     │   │
│  │  Metodología                                                        │   │
│  │  [Agile                   ▼]  (no editable post-creación)         │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  [Cancelar]                                              [Guardar Cambios] │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Tab: General

| Campo | Editable | Descripción |
|-------|----------|-------------|
| Nombre | ✅ | Nombre del proyecto |
| Descripción | ✅ | Descripción larga |
| Tipo | ❌ | Solo lectura post-creación |
| Metodología | ❌ | Solo lectura post-creación |
| Código | ❌ | Auto-generado |
| Fecha creación | ❌ | Solo lectura |

### 5.3 Tab: Fases

| Acción | Descripción |
|--------|-------------|
| Ver fases | Lista de fases del proyecto |
| Reordenar | Drag & drop |
| Agregar | Desde catálogo |
| Quitar | Solo si no tiene tareas |
| Editar duración | Por fase |

### 5.4 Tab: Deliverables

| Acción | Descripción |
|--------|-------------|
| Ver por fase | Acordeón |
| Agregar | Desde catálogo |
| Quitar | Solo si no tiene documentos |
| Marcar requerido | Toggle |

### 5.5 Tab: Sprints

| Campo | Editable | Descripción |
|-------|----------|-------------|
| Sprints habilitados | ✅ | Toggle |
| Duración default | ✅ | Días |
| Velocidad default | ✅ | Story points |
| Auto-crear carpetas | ✅ | Toggle |

### 5.6 Tab: Features

| Feature | Toggle | Configuración |
|---------|--------|---------------|
| Firmas | ✅ | Niveles requeridos |
| Criterios | ✅ | DoD/DoR bloqueantes |
| Compliance | ✅ | Checks habilitados |
| Trackable Items | ✅ | Tipos habilitados |
| Living Documents | ✅ | Fuentes habilitadas |

---

## 6. COMPONENTES UI

### 6.1 Lista de componentes

| # | Componente | Ubicación | Props principales |
|---|------------|-----------|-------------------|
| C1 | `ProjectTypeSelector` | Wizard P1 | `types`, `selected`, `onSelect` |
| C2 | `FlowTemplateSelector` | Wizard P2 | `templates`, `selected`, `onSelect` |
| C3 | `SprintConfigPanel` | Wizard P3, Settings | `config`, `onChange` |
| C4 | `PhaseListEditor` | Wizard P4, Settings | `phases`, `onReorder`, `onToggle` |
| C5 | `PhaseItem` | Dentro de C4 | `phase`, `onToggle`, `onRemove` |
| C6 | `DeliverableAccordion` | Wizard P5, Settings | `phases`, `deliverables`, `onChange` |
| C7 | `DeliverableCheckbox` | Dentro de C6 | `deliverable`, `checked`, `onChange` |
| C8 | `ProjectSummaryCard` | Wizard P6 | `project`, `onEdit` |
| C9 | `WizardStepper` | Wizard nav | `steps`, `current`, `onStepClick` |
| C10 | `PhaseCatalogPicker` | Modal | `catalog`, `onSelect` |
| C11 | `DeliverableCatalogPicker` | Modal | `catalog`, `phaseCode`, `onSelect` |

### 6.2 Estados de componentes

```typescript
// Estado del wizard
interface WizardState {
  currentStep: number;
  projectType: string | null;
  flowTemplate: string | null;
  sprintConfig: {
    enabled: boolean;
    duration: number;
    velocity: number;
  };
  phases: ProjectPhase[];
  deliverables: ProjectDeliverable[];
  projectName: string;
  projectDescription: string;
}

// Validación por paso
interface StepValidation {
  isValid: boolean;
  errors: string[];
}
```

---

## 7. REGLA CRÍTICA: FRONTERA DE PERSISTENCIA

### 7.1 Catálogos vs Instancias

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        FRONTERA DE PERSISTENCIA                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  CATÁLOGOS (Globales)              │   PROYECTO (Instancia)                │
│  ─────────────────────             │   ────────────────────                │
│                                    │                                        │
│  project_type_catalog    ────────► │   projects.projectTypeCode            │
│  phase_catalog           ──clone─► │   project_phases                      │
│  deliverable_catalog     ──clone─► │   project_deliverables                │
│  flow_template_catalog   ────────► │   (referencia, no copia)              │
│                                    │                                        │
│  ⚠️ INMUTABLES desde proyecto      │   ✅ EDITABLES                         │
│                                    │                                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 7.2 Reglas

| Regla | Descripción |
|-------|-------------|
| R1 | El wizard NUNCA modifica catálogos |
| R2 | Al crear proyecto, se CLONAN fases y deliverables |
| R3 | Cambios al proyecto NO afectan catálogos |
| R4 | Cambios a catálogos NO afectan proyectos existentes |
| R5 | Tipo y metodología NO son editables post-creación |

---

## 8. ENDPOINTS

### Wizard

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/projects` | Crear proyecto con wizard |
| GET | `/api/projects/wizard/preview` | Preview antes de crear |

### Settings

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/projects/:id/configuration` | Ver configuración |
| PATCH | `/api/projects/:id/configuration` | Actualizar configuración |
| POST | `/api/projects/:id/phases` | Agregar fase |
| DELETE | `/api/projects/:id/phases/:phaseId` | Quitar fase |
| PATCH | `/api/projects/:id/phases/reorder` | Reordenar fases |
| POST | `/api/projects/:id/deliverables` | Agregar deliverable |
| DELETE | `/api/projects/:id/deliverables/:id` | Quitar deliverable |

---

## 9. EJEMPLO COMPLETO

### Flujo de creación

```
PASO 1: Usuario abre wizard
────────────────────────────────────────────────────────────
Click en "Nuevo Proyecto"
→ Wizard se abre en paso 1

PASO 2: Selecciona tipo
────────────────────────────────────────────────────────────
Click en card "Software Development"
→ Tipo seleccionado, botón "Siguiente" habilitado

PASO 3: Selecciona metodología
────────────────────────────────────────────────────────────
Click en card "Agile"
→ Preview muestra 7 fases

PASO 4: Configura sprints
────────────────────────────────────────────────────────────
Toggle "Usar sprints" = ON
Duración = 2 semanas
Velocidad = 21 SP

PASO 5: Revisa fases
────────────────────────────────────────────────────────────
- Discovery (deshabilitada por usuario)
- Requirements ✓
- Analysis ✓
- Design ✓
- Development ✓
- Testing ✓
- Deployment ✓

PASO 6: Revisa deliverables
────────────────────────────────────────────────────────────
Analysis:
  ✓ Use Cases
  ✓ User Stories
  ✓ Acceptance Criteria
Design:
  ✓ Architecture
  ✓ Technical Spec
  ☐ Wireframes (deshabilitado)

PASO 7: Resumen
────────────────────────────────────────────────────────────
Nombre: "Memory Service"
Tipo: Software Development
Metodología: Agile
Sprints: Sí (2 semanas, 21 SP)
Fases: 6
Deliverables: 12

PASO 8: Crear
────────────────────────────────────────────────────────────
Click "Crear Proyecto"
→ POST /api/projects
→ Redirect a /projects/memory-service
```

---

## 10. FAQ

**¿Puedo volver a pasos anteriores?**
Sí. El stepper permite navegar a cualquier paso completado.

**¿Se guarda el progreso si cierro el wizard?**
No. El wizard es stateless. Si cierras, pierdes el progreso.

**¿Puedo cambiar el tipo de proyecto después?**
No. Tipo y metodología son inmutables post-creación.

**¿Las fases del proyecto son independientes del catálogo?**
Sí. Se clonan al crear. Cambios al catálogo no afectan proyectos existentes.

**¿Puedo agregar fases que no están en el catálogo?**
No. Solo puedes agregar fases del catálogo global.

---

## 11. INTEGRACIÓN CON OTRAS FEATURES

| Feature | Integración |
|---------|-------------|
| **Catálogos Base** | Lee tipos, fases, deliverables |
| **Flow Templates** | Lee templates disponibles |
| **Project Folders** | Crea carpetas según fases |
| **Releases/Sprints** | Configura si habilitar sprints |
| **Features Config** | Tab para configurar features |

---

**Documento:** FEATURE_UX_WIZARD_SETTINGS.md  
**Versión:** 1.0  
**Fecha:** 2026-05-06
