# DISEÑO: Sistema Anti-Hardcode VTT

| Campo | Valor |
|-------|-------|
| **Documento** | DISENO_HARDCODE_CHECK_VTT.md |
| **Versión** | 1.0 |
| **Fecha** | 2026-04-12 |
| **Autor** | PM (Martin Rivas) |
| **Estado** | ✅ DECISIONES TOMADAS — LISTO PARA IMPLEMENTACIÓN |
| **Fuente** | ADDENDUM_FIRMAS_VALIDACION_CALIDAD_V4.3.2.md (S08) |

---

## 1. RESUMEN EJECUTIVO

### ¿Qué es?
Sistema para detectar datos "quemados" en código que deberían venir de configuración, catálogos o variables de entorno.

### ¿Qué está implementado?

| Componente | Estado | Descripción |
|------------|--------|-------------|
| Tabla `hardcode_patterns` | ✅ | Catálogo de patrones regex |
| Tabla `task_findings` | ✅ | Hallazgos por tarea |
| Endpoint `POST /tasks/:id/hardcode-check` | ✅ | Ejecutar análisis |
| Endpoint `GET /hardcode-patterns` | ✅ | Listar patrones |
| UI: Pantalla manual | ✅ | Textarea + botón ejecutar |
| **Integración automática** | ❌ | NO implementado |

### ¿Qué falta?

| Componente | Estado | Descripción |
|------------|--------|-------------|
| Webhook Git/PR | ❌ | Trigger automático en commit/PR |
| Scan de repositorio | ❌ | Leer archivos del repo |
| Integración CI/CD | ❌ | Ejecutar en pipeline |
| Bloqueo automático | ❌ | Bloquear task_completed si hay critical/high |

---

## 2. ARQUITECTURA DISEÑADA (Completa)

### 2.1 Flujo Automático (NO implementado)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     FLUJO HARDCODE CHECK                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────────────────┐ │
│  │   COMMIT    │ ───► │   WEBHOOK   │ ───► │  HARDCODE CHECK SERVICE │ │
│  │   (Git)     │      │   (VTT BE)  │      │                         │ │
│  └─────────────┘      └─────────────┘      │  1. Fetch archivos      │ │
│                                            │  2. Por cada archivo:   │ │
│                                            │     - Aplicar regex     │ │
│                                            │     - Detectar matches  │ │
│                                            │  3. Crear findings      │ │
│                                            │  4. Evaluar severidad   │ │
│                                            └───────────┬─────────────┘ │
│                                                        │                │
│                                                        ▼                │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │                         RESULTADOS                                  ││
│  │                                                                     ││
│  │  ┌─────────────┐   ┌──────────────┐   ┌───────────────────────────┐││
│  │  │  CRITICAL   │   │     HIGH     │   │    MEDIUM / LOW          │││
│  │  │  BLOQUEA    │   │   BLOQUEA    │   │    NO BLOQUEA            │││
│  │  │             │   │              │   │    Solo se registra      │││
│  │  └─────────────┘   └──────────────┘   └───────────────────────────┘││
│  │                                                                     ││
│  │  Si hay CRITICAL o HIGH:                                           ││
│  │  → Tarea NO puede avanzar a task_completed                         ││
│  │  → Agente recibe notificación                                      ││
│  │  → Opción: marcar como "falso positivo" con justificación          ││
│  │                                                                     ││
│  └─────────────────────────────────────────────────────────────────────┘│
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Flujo Manual (Implementado)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     FLUJO MANUAL ACTUAL                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────┐                                                │
│  │   USUARIO/AGENTE    │                                                │
│  │                     │                                                │
│  │  1. Abre pantalla   │                                                │
│  │     /tasks/:id/     │                                                │
│  │     hardcode-check  │                                                │
│  │                     │                                                │
│  │  2. Pega código     │                                                │
│  │     manualmente     │                                                │
│  │                     │                                                │
│  │  3. Click "Ejecutar │                                                │
│  │     análisis"       │                                                │
│  └──────────┬──────────┘                                                │
│             │                                                           │
│             ▼                                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │  POST /api/tasks/:id/hardcode-check                                 ││
│  │  Body: { content: "...código pegado..." }                           ││
│  └───────────────────────────────────┬─────────────────────────────────┘│
│                                      │                                  │
│                                      ▼                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │  HARDCODE CHECK SERVICE                                             ││
│  │  1. Cargar patrones activos de hardcode_patterns                    ││
│  │  2. Por cada patrón:                                                ││
│  │     - Aplicar regex contra content                                  ││
│  │     - Si match → registrar finding                                  ││
│  │  3. Retornar resultados                                             ││
│  └─────────────────────────────────────────────────────────────────────┘│
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. MODELO DE DATOS

### 3.1 Tabla: `hardcode_patterns` (Catálogo Global)

```prisma
model HardcodePattern {
  id                String    @id @default(uuid())
  
  // === PATRÓN ===
  code              String    @unique  // "MAGIC_NUMBER", "HARDCODED_ID"
  name              String
  description       String?
  
  // === DETECCIÓN ===
  regex             String    // Expresión regular
  fileExtensions    String[]  // [".ts", ".js", ".py"]
  severity          String    // "critical", "high", "medium", "low"
  
  // === EJEMPLO ===
  badExample        String?   @map("bad_example")
  goodExample       String?   @map("good_example")
  
  // === CONFIGURACIÓN ===
  isActive          Boolean   @default(true) @map("is_active")
  autoDetect        Boolean   @default(true) @map("auto_detect")
  
  // === METADATA ===
  createdAt         DateTime  @default(now()) @map("created_at")
  
  // === RELACIONES ===
  projectPatterns   ProjectHardcodePattern[]
  
  @@map("hardcode_patterns")
}
```

### 3.2 Tabla: `project_hardcode_patterns` (Por Proyecto - NUEVA)

```prisma
model ProjectHardcodePattern {
  id                String    @id @default(uuid())
  
  // === CONTEXTO ===
  projectId         String    @map("project_id")
  
  // === HERENCIA ===
  globalPatternId   String?   @map("global_pattern_id")  // Si viene de patrón global
  isCustom          Boolean   @default(false) @map("is_custom")  // true = creado por usuario
  
  // === PATRÓN (copia o custom) ===
  code              String
  name              String
  description       String?
  regex             String
  fileExtensions    String[]
  severity          String
  badExample        String?   @map("bad_example")
  goodExample       String?   @map("good_example")
  
  // === OVERRIDE ===
  isActive          Boolean   @default(true) @map("is_active")  // Usuario puede desactivar
  autoDetect        Boolean   @default(true) @map("auto_detect")
  
  // === METADATA ===
  createdAt         DateTime  @default(now()) @map("created_at")
  updatedAt         DateTime  @updatedAt @map("updated_at")
  
  // === RELACIONES ===
  project           Project   @relation(fields: [projectId], references: [id], onDelete: Cascade)
  globalPattern     HardcodePattern? @relation(fields: [globalPatternId], references: [id], onDelete: SetNull)
  
  @@unique([projectId, code])
  @@index([projectId])
  @@map("project_hardcode_patterns")
}
```

### 3.3 Tabla: `task_findings` (Hallazgos - Actualizada)

```prisma
model TaskFinding {
  id                String    @id @default(uuid())
  taskId            String    @map("task_id")
  
  // === TIPO DE HALLAZGO ===
  type              String    // "issue", "tech_debt", "decision", "adr_note", "testing_note", "hardcode"
  severity          String    // "critical", "high", "medium", "low"
  status            String    @default("open")  // "open", "resolved", "false_positive", "bug_created", "deferred"
  
  // === CONTENIDO ===
  title             String
  description       String?
  resolution        String?   // Cómo se resolvió o justificación falso positivo
  
  // === HARDCODE ESPECÍFICO ===
  patternCode       String?   @map("pattern_code")  // Código del patrón que matcheó
  filePath          String?   @map("file_path")     // Archivo donde se encontró
  lineNumber        Int?      @map("line_number")   // Línea
  matchedContent    String?   @map("matched_content") // Texto que matcheó
  
  // === INTEGRACIÓN CON BUGS ===
  bugId             String?   @map("bug_id")  // Si se creó bug
  
  // === VALIDACIÓN LEGACY ===
  hardcodeCheckPassed Boolean @default(false) @map("hardcode_check_passed")
  hardcodePatterns  Json?     @map("hardcode_patterns")  // Legacy, mantener por compatibilidad
  
  // === MÉTRICAS ===
  filesCreated      Int       @default(0) @map("files_created")
  filesModified     Int       @default(0) @map("files_modified")
  linesAdded        Int       @default(0) @map("lines_added")
  linesDeleted      Int       @default(0) @map("lines_deleted")
  
  // === METADATA ===
  reportedBy        String    @map("reported_by")
  reportedAt        DateTime  @default(now()) @map("reported_at")
  updatedAt         DateTime  @updatedAt @map("updated_at")
  resolvedBy        String?   @map("resolved_by")
  resolvedAt        DateTime? @map("resolved_at")
  
  // === RELACIONES ===
  task              Task      @relation(fields: [taskId], references: [id], onDelete: Cascade)
  
  @@index([taskId])
  @@index([status])
  @@index([type])
  @@map("task_findings")
}
```

### 3.4 Extensión a Task

```prisma
model Task {
  // ... campos existentes ...
  
  // === INTEGRACIÓN CON PR ===
  prNumber          Int?      @map("pr_number")  // Número del PR en GitHub
  prUrl             String?   @map("pr_url")     // URL completa del PR
  
  // ... relaciones existentes ...
}
```

---

## 4. PATRONES PREDEFINIDOS (SEED)

| Code | Name | Severity | Regex | Ejemplo Malo | Ejemplo Bueno |
|------|------|----------|-------|--------------|---------------|
| `HARDCODED_UUID` | UUID Hardcodeado | HIGH | `['"][0-9a-f]{8}-[0-9a-f]{4}...` | `const userId = "550e8400-..."` | `const userId = config.defaultUserId` |
| `MAGIC_NUMBER` | Magic Number | MEDIUM | `(?<![\\w.])(?:86400\|3600\|60000...)` | `setTimeout(fn, 86400000)` | `setTimeout(fn, MS_PER_DAY)` |
| `HARDCODED_STATUS` | Status Hardcodeado | HIGH | `status.*['"](?:active\|pending...)` | `status: "active"` | `status: StatusCatalog.ACTIVE` |
| `HARDCODED_ROLE` | Rol Hardcodeado | HIGH | `role.*['"](?:admin\|user...)` | `if (role === "admin")` | `if (role === Roles.ADMIN)` |
| `HARDCODED_URL` | URL Hardcodeada | CRITICAL | `https?://(?:localhost\|127...)` | `fetch("http://localhost:3000")` | `fetch(config.apiUrl)` |
| `INLINE_CREDENTIALS` | Credenciales Inline | CRITICAL | `(?:password\|apiKey\|token).*['"][^'"]{8,}` | `apiKey = "sk-abc123..."` | `apiKey = process.env.API_KEY` |
| `HARDCODED_EMAIL` | Email Hardcodeado | MEDIUM | `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+` | `sendEmail("admin@company.com")` | `sendEmail(config.adminEmail)` |
| `HARDCODED_PORT` | Puerto Hardcodeado | MEDIUM | `port.*(?:3000\|5432\|6379...)` | `const port = 3000` | `const port = process.env.PORT` |

---

## 5. REGLAS DE NEGOCIO

### 5.1 Severidad y Bloqueo

| Severidad | ¿Bloquea? | Comportamiento |
|-----------|-----------|----------------|
| `critical` | ✅ SÍ | Tarea NO puede avanzar a `task_completed` |
| `high` | ✅ SÍ | Tarea NO puede avanzar a `task_completed` |
| `medium` | ❌ NO | Se registra, visible en reporte de cierre |
| `low` | ❌ NO | Se registra, visible en reporte de cierre |

### 5.2 Falsos Positivos

| Regla | Descripción |
|-------|-------------|
| RN-HC-04 | Agente puede marcar como "falso positivo" con justificación |
| RN-HC-05 | Falsos positivos requieren revisión de AR o TL |
| RN-HC-05 | Se revisan en Integration Audit |

### 5.3 Checklist Manual (D-21)

El check automático NO cubre todo. Hay un checklist manual que valida:

| Item | Descripción |
|------|-------------|
| ☐ | ¿Se usan catálogos en lugar de strings hardcodeados? |
| ☐ | ¿No hay mocks en código de producción? |
| ☐ | ¿Los datos de negocio vienen de BD, no de código? |
| ☐ | ¿Las excepciones tienen justificación documentada? |

---

## 6. API ENDPOINTS

### 6.1 Implementados

| Método | Path | Descripción | Estado |
|--------|------|-------------|--------|
| `GET` | `/api/hardcode-patterns` | Listar patrones activos | ✅ |
| `POST` | `/api/hardcode-patterns` | Crear patrón (admin) | ✅ |
| `POST` | `/api/tasks/:id/hardcode-check` | Ejecutar check | ✅ |
| `GET` | `/api/tasks/:id/hardcode-check` | Ver último resultado | ✅ |
| `GET` | `/api/tasks/:id/findings` | Ver hallazgos | ✅ |

### 6.2 Por Implementar (Integración Automática)

| Método | Path | Descripción | Estado |
|--------|------|-------------|--------|
| `POST` | `/api/webhooks/git/push` | Webhook para commits | ❌ |
| `POST` | `/api/webhooks/git/pr` | Webhook para PRs | ❌ |
| `POST` | `/api/tasks/:id/hardcode-check/scan-repo` | Scan de archivos del repo | ❌ |
| `POST` | `/api/tasks/:id/hardcode-check/:patternId/false-positive` | Marcar falso positivo | ❌ |

---

## 7. REQUEST/RESPONSE

### 7.1 POST /api/tasks/:id/hardcode-check (Manual - Actual)

**Request:**
```json
{
  "content": "const userId = \"550e8400-e29b-41d4-a716-446655440000\";\nconst port = 3000;\nconst apiKey = \"sk-abc123xyz\";"
}
```

**Response:**
```json
{
  "taskId": "uuid",
  "hardcodeCheckPassed": false,
  "findings": [
    {
      "patternCode": "HARDCODED_UUID",
      "severity": "high",
      "line": 1,
      "match": "550e8400-e29b-41d4-a716-446655440000",
      "suggestion": "Usar config.defaultUserId o valor de BD"
    },
    {
      "patternCode": "HARDCODED_PORT",
      "severity": "medium",
      "line": 2,
      "match": "3000",
      "suggestion": "Usar process.env.PORT"
    },
    {
      "patternCode": "INLINE_CREDENTIALS",
      "severity": "critical",
      "line": 3,
      "match": "sk-abc123xyz",
      "suggestion": "Usar process.env.API_KEY"
    }
  ],
  "summary": {
    "critical": 1,
    "high": 1,
    "medium": 1,
    "low": 0,
    "total": 3
  },
  "canProceed": false
}
```

### 7.2 POST /api/tasks/:id/hardcode-check/scan-repo (Automático - Por Implementar)

**Request:**
```json
{
  "repositoryUrl": "https://github.com/NCoreSys/memory-service.git",
  "branch": "feature/user-endpoint",
  "commitHash": "abc123",
  "filePaths": [
    "src/services/user.service.ts",
    "src/controllers/user.controller.ts"
  ]
}
```

**Response:** Igual que el manual, pero con `file` en cada finding.

---

## 8. FLUJO DE GESTIÓN DE FINDINGS (Actualizado)

### 8.1 Flujo Completo

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     FLUJO HARDCODE CHECK COMPLETO                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  FASE 1 (Manual):                    FASE 3 (Automático):                  │
│  ┌─────────────────────┐             ┌─────────────────────┐               │
│  │ Usuario (TL/PM)     │             │ Webhook GitHub      │               │
│  │ click "Analizar"    │             │ en PR open/sync     │               │
│  └──────────┬──────────┘             └──────────┬──────────┘               │
│             │                                   │                           │
│             └─────────────┬─────────────────────┘                           │
│                           ▼                                                 │
│             ┌─────────────────────────────────────┐                         │
│             │  BE ejecuta `gh pr view --json`     │                         │
│             │  + `gh pr diff` para obtener        │                         │
│             │  archivos del PR                    │                         │
│             └──────────────┬──────────────────────┘                         │
│                            ▼                                                │
│             ┌─────────────────────────────────────┐                         │
│             │  Aplicar patrones (globales +       │                         │
│             │  proyecto) contra archivos          │                         │
│             └──────────────┬──────────────────────┘                         │
│                            ▼                                                │
│             ┌─────────────────────────────────────┐                         │
│             │  Crear findings en task_findings    │                         │
│             └──────────────┬──────────────────────┘                         │
│                            ▼                                                │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                    PANTALLA DE FINDINGS                              │  │
│  │                    /tasks/:id/hardcode-findings                      │  │
│  │                                                                      │  │
│  │  ┌────────────────────────────────────────────────────────────────┐  │  │
│  │  │ 🔴 CRITICAL | INLINE_CREDENTIALS                               │  │  │
│  │  │ Archivo: src/config/api.ts:15                                  │  │  │
│  │  │ Match: apiKey = "sk-abc123..."                                 │  │  │
│  │  │                                                                │  │  │
│  │  │ [Aprobar Falso Positivo] [Generar Bug]                        │  │  │
│  │  └────────────────────────────────────────────────────────────────┘  │  │
│  │                                                                      │  │
│  │  ┌────────────────────────────────────────────────────────────────┐  │  │
│  │  │ 🟠 HIGH | HARDCODED_UUID                                       │  │  │
│  │  │ Archivo: src/services/user.ts:42                               │  │  │
│  │  │ Match: "550e8400-e29b-41d4..."                                 │  │  │
│  │  │                                                                │  │  │
│  │  │ [Aprobar Falso Positivo] [Generar Bug]                        │  │  │
│  │  └────────────────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                            │                                                │
│              ┌─────────────┴─────────────┐                                  │
│              ▼                           ▼                                  │
│  ┌─────────────────────┐     ┌─────────────────────────────────────────┐   │
│  │ APROBAR FALSO       │     │ GENERAR BUG                             │   │
│  │ POSITIVO            │     │                                         │   │
│  │                     │     │ 1. Crea bug vinculado a tarea           │   │
│  │ - Usuario ingresa   │     │ 2. Tarea pasa a ON_HOLD                 │   │
│  │   justificación     │     │ 3. TL revisa bug                        │   │
│  │ - Finding status =  │     │ 4. TL crea fix task                     │   │
│  │   'false_positive'  │     │ 5. Fix task se completa                 │   │
│  │ - No bloquea        │     │ 6. Bug se resuelve                      │   │
│  │                     │     │ 7. Tarea original sale de ON_HOLD       │   │
│  └─────────────────────┘     └─────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 8.2 Integración con Sistema de Bugs Existente

```
Finding CRITICAL/HIGH detectado
        │
        ▼
Usuario click [Generar Bug]
        │
        ▼
┌─────────────────────────────────────┐
│ POST /api/findings/:id/create-bug   │
│                                     │
│ 1. Crea Bug en sistema existente    │
│    - title: "Hardcode: {pattern}"   │
│    - description: archivo + línea   │
│    - severity: del finding          │
│    - linkedTaskId: tarea actual     │
│                                     │
│ 2. Actualiza Task                   │
│    - status → ON_HOLD               │
│    - holdReason: "Bug #{bugId}"     │
│                                     │
│ 3. Actualiza Finding                │
│    - status → 'bug_created'         │
│    - bugId: referencia al bug       │
└─────────────────────────────────────┘
        │
        ▼
TL recibe notificación de bug
        │
        ▼
TL crea Fix Task desde bug
        │
        ▼
Fix Task completada → Bug resuelto
        │
        ▼
┌─────────────────────────────────────┐
│ Trigger automático:                 │
│                                     │
│ 1. Finding status → 'resolved'      │
│ 2. Task original status → anterior  │
│    (sale de ON_HOLD)                │
└─────────────────────────────────────┘
```

---

## 9. FASES DE IMPLEMENTACIÓN (Actualizado)

### 9.1 Fase 1: Scan de PR via GitHub CLI (Manual)

**Descripción:** Usuario (TL/PM) hace click en "Analizar código" en vista de tarea. Sistema usa `gh` CLI para obtener archivos del PR asociado y ejecuta scan.

| Tarea | Descripción | Horas |
|-------|-------------|-------|
| BE-HC-01 | Service para ejecutar `gh pr view --json files` y `gh pr diff` | 4h |
| BE-HC-02 | Parsear archivos y aplicar patrones | 4h |
| BE-HC-03 | Endpoint `POST /tasks/:id/hardcode-check/scan-pr` | 3h |
| BE-HC-04 | Vincular tarea con número de PR (campo `prNumber` en Task) | 2h |
| FE-HC-01 | Botón "Analizar código" en Task Detail | 2h |
| FE-HC-02 | Mostrar resultados inline | 3h |
| **Total** | | **18h** |

### 9.2 Fase 2: Pantalla de Gestión de Findings

**Descripción:** Pantalla dedicada donde usuario ve todos los findings de hardcode y puede aprobar (falso positivo) o generar bug.

| Tarea | Descripción | Horas |
|-------|-------------|-------|
| FE-HC-03 | Pantalla `/tasks/:id/hardcode-findings` | 6h |
| FE-HC-04 | Listado de findings con filtros (severidad, status) | 4h |
| FE-HC-05 | Acción "Aprobar como falso positivo" con justificación | 3h |
| FE-HC-06 | Acción "Generar Bug" → integración con sistema de bugs | 4h |
| BE-HC-05 | Endpoint `POST /findings/:id/approve-false-positive` | 2h |
| BE-HC-06 | Endpoint `POST /findings/:id/create-bug` → pone tarea ON_HOLD | 4h |
| **Total** | | **23h** |

### 9.3 Fase 3: Webhook Automático (GitHub Actions + Webhook)

**Descripción:** Scan automático al crear/actualizar PR. Usuario no hace nada.

| Tarea | Descripción | Horas |
|-------|-------------|-------|
| BE-HC-07 | Endpoint webhook `POST /webhooks/github/pr` | 4h |
| BE-HC-08 | GitHub Action que llama webhook en PR open/sync | 3h |
| BE-HC-09 | Mapear PR → tarea activa del agente (via branch name o commits) | 4h |
| BE-HC-10 | Ejecutar scan automático y crear findings | 3h |
| BE-HC-11 | Notificación al usuario si hay findings críticos | 2h |
| **Total** | | **16h** |

### 9.4 Fase 4: Patrones por Proyecto

**Descripción:** Al crear proyecto, copiar patrones globales. Usuario puede customizar.

| Tarea | Descripción | Horas |
|-------|-------------|-------|
| DB-HC-01 | Tabla `project_hardcode_patterns` (copia de globales + custom) | 2h |
| BE-HC-12 | Copiar patrones globales al crear proyecto | 2h |
| BE-HC-13 | CRUD de patrones por proyecto | 4h |
| FE-HC-07 | Pantalla admin de patrones por proyecto | 6h |
| **Total** | | **14h** |

### Resumen de Fases

| Fase | Descripción | Horas | Prioridad |
|------|-------------|-------|-----------|
| 1 | Scan PR manual via `gh` CLI | 18h | P0 |
| 2 | Pantalla gestión findings + integración bugs | 23h | P0 |
| 3 | Webhook automático | 16h | P1 |
| 4 | Patrones por proyecto | 14h | P2 |
| **Total** | | **71h** |

---

## 10. DECISIONES PM CONGELADAS

| # | Decisión | Estado |
|---|----------|--------|
| D-18 | `critical` y `high` **BLOQUEAN** cierre de tarea | ✅ FROZEN |
| D-21 | Check es **HÍBRIDO**: automático (regex) + manual (checklist) | ✅ FROZEN |

---

## 11. DECISIONES TOMADAS (PM + TL)

| # | Pregunta | Decisión |
|---|----------|----------|
| Q1 | ¿Implementamos Fase 1 (scan repo manual) primero? | ✅ **SÍ.** Fase 1: Usuario (TL/PM) ejecuta scan manual por tarea (archivos del PR/commit). Fase 2+: Automático via webhook, usuario no hace nada. |
| Q2 | ¿Qué servicio de Git usamos? | ✅ **GitHub CLI (`gh`).** Ya lo usan los agentes. Comandos: `gh pr view --json files,commits`, `gh pr diff`. No requiere nueva infraestructura. |
| Q3 | ¿Integramos con CI/CD o webhook? | ✅ **AMBOS.** GitHub Actions para integración con PR checks + Webhook directo a VTT para control interno. |
| Q4 | ¿Cómo se gestionan los findings? | ✅ **Pantalla dedicada.** Usuario ve findings → Aprueba (falso positivo) o Genera Bug → Bug pone tarea ON_HOLD → TL crea fix task → Bug resuelto → Tarea sale de ON_HOLD. |
| Q5 | ¿Patrones por proyecto? | ✅ **SÍ, con herencia.** Patrones globales se copian al proyecto al crearlo. Usuario puede agregar/modificar/desactivar localmente. |

---

## 12. ESTADO ACTUAL vs DISEÑO COMPLETO

```
DISEÑO COMPLETO                          IMPLEMENTADO
─────────────────────────────────────────────────────────────────
┌─────────────────────┐                  ┌─────────────────────┐
│ Patrones globales   │  ════════════>   │ ✅ hardcode_patterns│
│ en BD               │                  │                     │
└─────────────────────┘                  └─────────────────────┘

┌─────────────────────┐                  ┌─────────────────────┐
│ Findings por tarea  │  ════════════>   │ ✅ task_findings    │
└─────────────────────┘                  └─────────────────────┘

┌─────────────────────┐                  ┌─────────────────────┐
│ UI: Pegar código    │  ════════════>   │ ✅ Pantalla manual  │
└─────────────────────┘                  └─────────────────────┘

┌─────────────────────┐                  ┌─────────────────────┐
│ Scan PR via `gh`    │  ───────────X    │ ❌ Fase 1 (18h)     │
│ CLI                 │                  │                     │
└─────────────────────┘                  └─────────────────────┘

┌─────────────────────┐                  ┌─────────────────────┐
│ Pantalla gestión    │  ───────────X    │ ❌ Fase 2 (23h)     │
│ findings + bugs     │                  │                     │
└─────────────────────┘                  └─────────────────────┘

┌─────────────────────┐                  ┌─────────────────────┐
│ Webhook GitHub      │  ───────────X    │ ❌ Fase 3 (16h)     │
│ + Actions           │                  │                     │
└─────────────────────┘                  └─────────────────────┘

┌─────────────────────┐                  ┌─────────────────────┐
│ Patrones por        │  ───────────X    │ ❌ Fase 4 (14h)     │
│ proyecto            │                  │                     │
└─────────────────────┘                  └─────────────────────┘

TOTAL PENDIENTE: 71h (4 fases)
```

---

## 13. FIRMA

| Rol | Firma | Fecha |
|-----|-------|-------|
| PM | ✅ Aprobado | 2026-04-12 |
| TL | ✅ Decisiones confirmadas | 2026-04-12 |

---

**Documento:** DISENO_HARDCODE_CHECK_VTT.md  
**Versión:** 1.0  
**Fecha:** 2026-04-12
