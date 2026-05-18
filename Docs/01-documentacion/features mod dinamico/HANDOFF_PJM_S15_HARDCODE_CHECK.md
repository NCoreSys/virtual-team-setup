# HANDOFF PJM — HARDCODE CHECK COMPLETO

| Campo | Valor |
|-------|-------|
| **Sprint** | S15 |
| **Documento** | HANDOFF_PJM_S15_HARDCODE_CHECK.md |
| **Versión** | 1.0 |
| **Fecha** | 2026-04-12 |
| **De** | PM (Martin Rivas) |
| **Para** | PJM |
| **Referencia** | DISENO_HARDCODE_CHECK_VTT.md |
| **Estado** | ✅ LISTO PARA EJECUCIÓN |

---

## 1. RESUMEN EJECUTIVO

| Métrica | Valor |
|---------|-------|
| Tablas nuevas | 1 (project_hardcode_patterns) |
| Tablas ALTER | 2 (task_findings, tasks) |
| Endpoints nuevos | 8 |
| Pantallas FE | 2 |
| Horas totales | 71h |
| Fases | 4 |

---

## 2. CONTEXTO

### Lo que ya existe:
- Tabla `hardcode_patterns` con patrones regex ✅
- Tabla `task_findings` para hallazgos ✅
- Pantalla manual donde se pega código ✅
- Endpoint `POST /tasks/:id/hardcode-check` ✅

### Lo que falta:
- Scan automático desde PR (sin pegar código)
- Pantalla para gestionar findings
- Integración con sistema de bugs
- Webhook para scan automático en PR
- Patrones personalizados por proyecto

---

## 3. DECISIONES PM CONGELADAS

| # | Decisión | Resolución |
|---|----------|------------|
| Q1 | ¿Quién ejecuta scan? | Fase 1: Usuario (TL/PM) manual. Fase 3: Automático via webhook. |
| Q2 | ¿Servicio Git? | GitHub CLI (`gh pr view --json`, `gh pr diff`) — ya lo usan agentes |
| Q3 | ¿CI/CD o webhook? | Ambos: GitHub Actions + Webhook directo a VTT |
| Q4 | ¿Gestión findings? | Pantalla dedicada → Usuario aprueba o genera bug → Bug pone tarea ON_HOLD |
| Q5 | ¿Patrones por proyecto? | Sí. Globales se copian al crear proyecto. Usuario customiza localmente. |

---

## 4. FASES DE IMPLEMENTACIÓN

### Fase 1: Scan PR via GitHub CLI (P0)

**Descripción:** Usuario hace click en "Analizar código" → Sistema usa `gh` CLI para obtener archivos del PR → Ejecuta scan.

**Horas:** 18h

| # | Tarea | Rol | Horas | Descripción |
|---|-------|-----|-------|-------------|
| BE-HC-01 | Service GitHub CLI | BE | 4h | Ejecutar `gh pr view --json files` y `gh pr diff` |
| BE-HC-02 | Parser de archivos | BE | 4h | Parsear archivos y aplicar patrones |
| BE-HC-03 | Endpoint scan-pr | BE | 3h | `POST /tasks/:id/hardcode-check/scan-pr` |
| BE-HC-04 | Campo prNumber en Task | DB/BE | 2h | ALTER tasks ADD pr_number, pr_url |
| FE-HC-01 | Botón "Analizar código" | FE | 2h | En Task Detail header |
| FE-HC-02 | Mostrar resultados | FE | 3h | Lista de findings inline |

**Entregables:**
- Endpoint `POST /tasks/:id/hardcode-check/scan-pr`
- UI con botón y resultados

---

### Fase 2: Pantalla Gestión de Findings (P0)

**Descripción:** Pantalla dedicada donde usuario ve findings y puede aprobar como falso positivo o generar bug.

**Horas:** 23h

| # | Tarea | Rol | Horas | Descripción |
|---|-------|-----|-------|-------------|
| FE-HC-03 | Pantalla findings | FE | 6h | `/tasks/:id/hardcode-findings` |
| FE-HC-04 | Lista con filtros | FE | 4h | Filtros por severidad, status |
| FE-HC-05 | Modal falso positivo | FE | 3h | Con campo justificación |
| FE-HC-06 | Modal generar bug | FE | 4h | Integración con sistema bugs |
| BE-HC-05 | Endpoint falso positivo | BE | 2h | `POST /findings/:id/approve-false-positive` |
| BE-HC-06 | Endpoint crear bug | BE | 4h | `POST /findings/:id/create-bug` → pone tarea ON_HOLD |

**Entregables:**
- Pantalla `/tasks/:id/hardcode-findings`
- Endpoints de gestión
- Integración con sistema de bugs

---

### Fase 3: Webhook Automático (P1)

**Descripción:** Scan automático al crear/actualizar PR. Usuario no hace nada.

**Horas:** 16h

| # | Tarea | Rol | Horas | Descripción |
|---|-------|-----|-------|-------------|
| BE-HC-07 | Endpoint webhook | BE | 4h | `POST /webhooks/github/pr` |
| BE-HC-08 | GitHub Action | DevOps | 3h | Action que llama webhook en PR open/sync |
| BE-HC-09 | Mapeo PR → Tarea | BE | 4h | Via branch name o commits |
| BE-HC-10 | Scan automático | BE | 3h | Ejecutar y crear findings |
| BE-HC-11 | Notificación | BE | 2h | Notificar si hay findings críticos |

**Entregables:**
- Webhook funcional
- GitHub Action template
- Scan automático en PRs

---

### Fase 4: Patrones por Proyecto (P2)

**Descripción:** Al crear proyecto, copiar patrones globales. Usuario puede customizar.

**Horas:** 14h

| # | Tarea | Rol | Horas | Descripción |
|---|-------|-----|-------|-------------|
| DB-HC-01 | Tabla project_hardcode_patterns | DB | 2h | CREATE TABLE |
| BE-HC-12 | Copiar al crear proyecto | BE | 2h | Hook en ProjectService.create() |
| BE-HC-13 | CRUD patrones proyecto | BE | 4h | Endpoints CRUD |
| FE-HC-07 | Pantalla admin patrones | FE | 6h | En settings de proyecto |

**Entregables:**
- Tabla `project_hardcode_patterns`
- Pantalla de administración

---

## 5. MODELO DE DATOS

### 5.1 Nueva Tabla: project_hardcode_patterns

```sql
CREATE TABLE project_hardcode_patterns (
  id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
  project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  global_pattern_id TEXT REFERENCES hardcode_patterns(id) ON DELETE SET NULL,
  is_custom BOOLEAN DEFAULT false,
  code VARCHAR(100) NOT NULL,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  regex TEXT NOT NULL,
  file_extensions TEXT[] NOT NULL,
  severity VARCHAR(50) NOT NULL,
  bad_example TEXT,
  good_example TEXT,
  is_active BOOLEAN DEFAULT true,
  auto_detect BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(project_id, code)
);

CREATE INDEX idx_project_hardcode_patterns_project ON project_hardcode_patterns(project_id);
```

### 5.2 ALTER: tasks

```sql
ALTER TABLE tasks 
ADD COLUMN pr_number INTEGER,
ADD COLUMN pr_url TEXT;
```

### 5.3 ALTER: task_findings

```sql
ALTER TABLE task_findings
ADD COLUMN pattern_code VARCHAR(100),
ADD COLUMN file_path TEXT,
ADD COLUMN line_number INTEGER,
ADD COLUMN matched_content TEXT,
ADD COLUMN bug_id TEXT,
ADD COLUMN resolved_by TEXT,
ADD COLUMN resolved_at TIMESTAMP;

-- Actualizar constraint unique (quitar si existe, ahora puede haber múltiples findings por tarea)
-- La constraint @@unique([taskId]) debe removerse
```

---

## 6. ENDPOINTS

### 6.1 Fase 1

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/tasks/:id/hardcode-check/scan-pr` | Scan archivos del PR asociado |

**Request:**
```json
{
  "prNumber": 680
}
```

**Response:**
```json
{
  "taskId": "uuid",
  "prNumber": 680,
  "filesScanned": 5,
  "findings": [
    {
      "id": "uuid",
      "patternCode": "HARDCODED_UUID",
      "severity": "high",
      "filePath": "src/services/user.ts",
      "lineNumber": 42,
      "matchedContent": "550e8400-e29b-41d4...",
      "suggestion": "Usar config o BD"
    }
  ],
  "summary": {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 0
  }
}
```

### 6.2 Fase 2

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/tasks/:id/hardcode-findings` | Listar findings de hardcode |
| POST | `/api/findings/:id/approve-false-positive` | Aprobar como falso positivo |
| POST | `/api/findings/:id/create-bug` | Crear bug y poner tarea ON_HOLD |

**POST /findings/:id/approve-false-positive:**
```json
{
  "justification": "Es un UUID de prueba en archivo de seeds"
}
```

**POST /findings/:id/create-bug:**
```json
{
  "title": "Fix: Remover UUID hardcodeado",
  "description": "Mover a configuración o BD",
  "assignedToId": "uuid-tl"
}
```

**Response:**
```json
{
  "findingId": "uuid",
  "bugId": "uuid",
  "taskStatus": "on_hold",
  "message": "Bug creado. Tarea en ON_HOLD hasta resolver."
}
```

### 6.3 Fase 3

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/webhooks/github/pr` | Webhook para eventos de PR |

**Payload (GitHub):**
```json
{
  "action": "opened",
  "pull_request": {
    "number": 680,
    "head": {
      "ref": "feature/VTT-423-user-endpoint"
    }
  }
}
```

### 6.4 Fase 4

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/projects/:id/hardcode-patterns` | Listar patrones del proyecto |
| POST | `/api/projects/:id/hardcode-patterns` | Crear patrón custom |
| PATCH | `/api/project-hardcode-patterns/:id` | Modificar patrón |
| DELETE | `/api/project-hardcode-patterns/:id` | Eliminar patrón custom |

---

## 7. PANTALLAS

### 7.1 Task Detail — Botón Analizar (Fase 1)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ VTT-423: Implementar endpoint POST /users           [Analizar Código 🔍]│
├─────────────────────────────────────────────────────────────────────────┤
│ PR: #680                                                                │
│ Status: In Progress                                                     │
│                                                                         │
│ [Click en "Analizar Código" ejecuta scan del PR #680]                  │
└─────────────────────────────────────────────────────────────────────────┘
```

### 7.2 Pantalla Hardcode Findings (Fase 2)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Hardcode Findings — VTT-423                                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│ [Filtros: Todos | Pendientes | Aprobados | Con Bug]  [Severidad ▼]     │
│                                                                         │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ 🔴 CRITICAL | INLINE_CREDENTIALS | PENDIENTE                        │ │
│ │ Archivo: src/config/api.ts:15                                       │ │
│ │ Match: apiKey = "sk-abc123..."                                      │ │
│ │ Sugerencia: Usar process.env.API_KEY                                │ │
│ │                                                                     │ │
│ │ [Aprobar Falso Positivo] [Generar Bug]                             │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ 🟠 HIGH | HARDCODED_UUID | PENDIENTE                                │ │
│ │ Archivo: src/services/user.ts:42                                    │ │
│ │ Match: "550e8400-e29b-41d4..."                                      │ │
│ │                                                                     │ │
│ │ [Aprobar Falso Positivo] [Generar Bug]                             │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ ✅ | MAGIC_NUMBER | FALSO POSITIVO                                  │ │
│ │ Archivo: src/constants.ts:10                                        │ │
│ │ Justificación: "Es constante de negocio documentada"               │ │
│ │ Aprobado por: TL • 2026-04-12                                       │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ RESUMEN: 3 findings | 2 pendientes | 1 aprobado                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 7.3 Modal Aprobar Falso Positivo

```
┌─────────────────────────────────────────────────────────────────────────┐
│ APROBAR COMO FALSO POSITIVO                                        [X] │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│ Finding: HARDCODED_UUID en src/services/user.ts:42                     │
│                                                                         │
│ Justificación *                                                         │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Es un UUID de prueba en archivo de seeds, no código de producción  │ │
│ │                                                                     │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ ⚠️ Esta acción se revisará en Integration Audit                        │
│                                                                         │
│                                                [Cancelar] [Aprobar]    │
└─────────────────────────────────────────────────────────────────────────┘
```

### 7.4 Modal Generar Bug

```
┌─────────────────────────────────────────────────────────────────────────┐
│ GENERAR BUG                                                        [X] │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│ Finding: INLINE_CREDENTIALS en src/config/api.ts:15                    │
│ Severidad: CRITICAL                                                     │
│                                                                         │
│ Título del Bug *                                                        │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Fix: Remover API key hardcodeada                                    │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ Descripción                                                             │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Mover apiKey a variable de entorno process.env.API_KEY             │ │
│ │ Archivo: src/config/api.ts línea 15                                 │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ Asignar a                                                               │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ [BE-Agent ▼]                                                        │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ ⚠️ La tarea VTT-423 pasará a ON_HOLD hasta que el bug se resuelva      │
│                                                                         │
│                                              [Cancelar] [Crear Bug]    │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 8. FLUJO COMPLETO

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     FLUJO HARDCODE CHECK                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  FASE 1 (Manual)              FASE 3 (Automático)                      │
│  ┌──────────────┐             ┌──────────────┐                         │
│  │ Usuario click│             │ PR opened    │                         │
│  │ "Analizar"   │             │ webhook      │                         │
│  └──────┬───────┘             └──────┬───────┘                         │
│         │                            │                                  │
│         └────────────┬───────────────┘                                  │
│                      ▼                                                  │
│         ┌────────────────────────┐                                      │
│         │ BE: gh pr view --json  │                                      │
│         │ + gh pr diff           │                                      │
│         └───────────┬────────────┘                                      │
│                     ▼                                                   │
│         ┌────────────────────────┐                                      │
│         │ Aplicar patrones       │                                      │
│         │ (globales + proyecto)  │                                      │
│         └───────────┬────────────┘                                      │
│                     ▼                                                   │
│         ┌────────────────────────┐                                      │
│         │ Crear findings         │                                      │
│         └───────────┬────────────┘                                      │
│                     ▼                                                   │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                PANTALLA FINDINGS (Fase 2)                        │  │
│  │                                                                  │  │
│  │   Por cada finding:                                              │  │
│  │   ┌─────────────────────────┬─────────────────────────────────┐  │  │
│  │   │ [Aprobar Falso Positivo]│ [Generar Bug]                   │  │  │
│  │   │                         │                                 │  │  │
│  │   │ → status='false_pos'    │ → Crea bug                      │  │  │
│  │   │ → No bloquea            │ → Tarea → ON_HOLD               │  │  │
│  │   │ → Se revisa en Audit    │ → TL crea fix task              │  │  │
│  │   │                         │ → Fix done → Bug resolved       │  │  │
│  │   │                         │ → Tarea sale de ON_HOLD         │  │  │
│  │   └─────────────────────────┴─────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 9. DEPENDENCIAS

### Previas (deben existir):

| Componente | Estado |
|------------|--------|
| Tabla `hardcode_patterns` | ✅ Existe |
| Tabla `task_findings` | ✅ Existe |
| Pantalla hardcode manual | ✅ Existe |
| Sistema de bugs | ✅ Existe |
| Status ON_HOLD en tareas | ✅ Existe |
| GitHub CLI (`gh`) en servidor | ⚠️ Verificar |

### Entre fases:

```
Fase 1 ──────────────────────────────────────►
        └── Fase 2 depende de findings de Fase 1
                   └── Fase 3 depende de BE de Fase 1-2
                              └── Fase 4 independiente (puede ir paralelo)
```

---

## 10. SECUENCIA DE EJECUCIÓN

```
SEMANA 1 (18h): FASE 1
├── DB: ALTER tasks (pr_number, pr_url)
├── BE: Service GitHub CLI + endpoint scan-pr
└── FE: Botón + resultados inline

SEMANA 2 (23h): FASE 2
├── DB: ALTER task_findings
├── BE: Endpoints falso positivo + crear bug
└── FE: Pantalla findings + modales

SEMANA 3 (16h): FASE 3
├── BE: Webhook endpoint
├── DevOps: GitHub Action
└── BE: Mapeo PR → Tarea + notificaciones

SEMANA 4 (14h): FASE 4
├── DB: CREATE project_hardcode_patterns
├── BE: CRUD + copiar al crear proyecto
└── FE: Pantalla admin patrones
```

---

## 11. CRITERIOS DE ACEPTACIÓN

| # | Criterio | Fase |
|---|----------|------|
| CA-01 | Usuario puede ejecutar scan desde Task Detail con botón | F1 |
| CA-02 | Scan usa `gh` CLI para obtener archivos del PR | F1 |
| CA-03 | Findings se crean en task_findings con pattern_code, file_path, line_number | F1 |
| CA-04 | Pantalla muestra findings con filtros | F2 |
| CA-05 | Usuario puede aprobar como falso positivo con justificación | F2 |
| CA-06 | Usuario puede generar bug desde finding | F2 |
| CA-07 | Al generar bug, tarea pasa a ON_HOLD | F2 |
| CA-08 | Al resolver bug, tarea sale de ON_HOLD | F2 |
| CA-09 | Webhook recibe eventos de PR y ejecuta scan | F3 |
| CA-10 | Scan automático crea findings sin intervención de usuario | F3 |
| CA-11 | Al crear proyecto, se copian patrones globales | F4 |
| CA-12 | Usuario puede agregar/modificar/desactivar patrones por proyecto | F4 |

---

## 12. RIESGOS

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| `gh` CLI no instalado en servidor | Media | Alto | Verificar antes de iniciar, instalar si falta |
| Rate limit de GitHub | Baja | Medio | Usar token con permisos adecuados |
| Falsos positivos saturan usuario | Media | Medio | Mecanismo de aprobación rápida + filtros |
| Webhook no recibe eventos | Media | Alto | Logs + retry + fallback a manual |

---

## 13. DOCUMENTOS DE REFERENCIA

| Documento | Path |
|-----------|------|
| Diseño completo | DISENO_HARDCODE_CHECK_VTT.md |
| Addendum S08 original | ADDENDUM_FIRMAS_VALIDACION_CALIDAD_V4.3.2.md |
| Catálogo features V4 | CATALOGO_FEATURES_VTT_V4.md |

---

## 14. FIRMA

| Rol | Firma | Fecha |
|-----|-------|-------|
| PM | ✅ Aprobado | 2026-04-12 |
| PJM | ⬜ Pendiente | |

---

**Documento:** HANDOFF_PJM_S15_HARDCODE_CHECK.md  
**Versión:** 1.0  
**Fecha:** 2026-04-12

---

**PM — Martin Rivas**  
CEO/Founder — Virtual Teams Tracking
