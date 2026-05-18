# FEATURE: COMPLIANCE CHECKS

| Campo | Valor |
|-------|-------|
| **Feature** | Compliance Checks |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-06 |
| **Sprint origen** | S07 |
| **Estado** | ✅ Diseñado — Pendiente implementación |

---

## 1. QUÉ ES

Sistema de verificaciones automáticas y manuales que validan el cumplimiento de estándares, reglas de negocio y buenas prácticas en tareas, sprints y releases.

---

## 2. PARA QUÉ SIRVE

- **Calidad** — Verificar estándares antes de cerrar tareas
- **Automatización** — Checks automáticos sin intervención manual
- **Auditoría** — Registro de qué se verificó y cuándo
- **Gates** — Bloquear avance si hay checks críticos fallidos
- **Personalización** — Configurar checks por proyecto

---

## 3. TIPOS DE CHECKS

| Tipo | Código | Descripción | Ejecución |
|------|--------|-------------|-----------|
| **Automático** | `auto` | Se ejecuta sin intervención | Sistema |
| **Manual** | `manual` | Requiere verificación humana | TL/QA |
| **Híbrido** | `hybrid` | Auto + confirmación manual | Sistema + TL |

---

## 4. CATEGORÍAS DE CHECKS

### 4.1 Code Quality

| Check | Tipo | Severidad | Descripción |
|-------|------|-----------|-------------|
| `no_console_log` | auto | medium | Sin console.log en código |
| `no_todo_comments` | auto | low | Sin TODOs sin resolver |
| `typescript_strict` | auto | high | Código compila sin errores TS |
| `lint_passed` | auto | medium | ESLint sin errores |
| `no_hardcoded_values` | hybrid | high | Sin valores hardcodeados |

### 4.2 Documentation

| Check | Tipo | Severidad | Descripción |
|-------|------|-----------|-------------|
| `devlog_created` | auto | medium | Devlog de tarea existe |
| `code_logic_exists` | auto | medium | Archivo .LOGIC.md existe |
| `swagger_updated` | manual | medium | Swagger actualizado |
| `readme_updated` | manual | low | README actualizado |

### 4.3 Testing

| Check | Tipo | Severidad | Descripción |
|-------|------|-----------|-------------|
| `unit_tests_pass` | auto | critical | Tests unitarios pasan |
| `coverage_minimum` | auto | high | Cobertura mínima 80% |
| `integration_tests` | auto | high | Tests de integración pasan |
| `manual_qa_approved` | manual | critical | QA aprueba manualmente |

### 4.4 Security

| Check | Tipo | Severidad | Descripción |
|-------|------|-----------|-------------|
| `no_secrets_exposed` | auto | critical | Sin secrets en código |
| `auth_implemented` | manual | critical | Autenticación implementada |
| `input_validation` | manual | high | Validación de inputs |

### 4.5 Process

| Check | Tipo | Severidad | Descripción |
|-------|------|-----------|-------------|
| `pr_created` | auto | medium | PR creado en GitHub |
| `pr_approved` | auto | high | PR aprobado por reviewer |
| `criteria_met` | auto | critical | DoD cumplidos |
| `no_blockers` | auto | critical | Sin devlog blockers pendientes |

---

## 5. SEVERIDADES

| Severidad | Código | Efecto en gate | Color |
|-----------|--------|----------------|-------|
| **Critical** | `critical` | Bloquea avance | 🔴 Rojo |
| **High** | `high` | Bloquea avance | 🟠 Naranja |
| **Medium** | `medium` | Warning, no bloquea | 🟡 Amarillo |
| **Low** | `low` | Info, no bloquea | 🔵 Azul |

---

## 6. FLUJO OPERATIVO

### 6.1 Ejecutar checks en tarea

```
POST /api/tasks/:taskId/run-compliance
```

```json
{
  "checksToRun": ["all"],  // o lista específica
  "runBy": "uuid-tl"
}
```

#### Response

```json
{
  "taskId": "uuid-task",
  "executedAt": "2026-05-06T10:00:00Z",
  "summary": {
    "total": 12,
    "passed": 10,
    "failed": 1,
    "skipped": 1,
    "canProceed": false
  },
  "results": [
    {
      "checkCode": "typescript_strict",
      "status": "passed",
      "severity": "high",
      "message": "TypeScript compilation successful",
      "executedAt": "2026-05-06T10:00:01Z"
    },
    {
      "checkCode": "no_hardcoded_values",
      "status": "failed",
      "severity": "high",
      "message": "Found 3 hardcoded values in src/config.ts",
      "details": {
        "file": "src/config.ts",
        "lines": [15, 23, 45],
        "values": ["localhost:5432", "secret123", "admin@test.com"]
      },
      "executedAt": "2026-05-06T10:00:02Z"
    },
    {
      "checkCode": "manual_qa_approved",
      "status": "skipped",
      "severity": "critical",
      "message": "Requires manual verification",
      "requiresManualAction": true
    }
  ],
  "blockers": [
    {
      "checkCode": "no_hardcoded_values",
      "severity": "high",
      "resolution": "Remove hardcoded values and use environment variables"
    }
  ]
}
```

### 6.2 Resolver check manual

```
POST /api/compliance-results/:resultId/resolve
```

```json
{
  "status": "passed",
  "verifiedBy": "uuid-qa",
  "notes": "Verificado manualmente. Funcionalidad correcta."
}
```

### 6.3 Ver resumen de compliance del sprint

```
GET /api/sprints/:sprintId/compliance-summary
```

```json
{
  "sprintId": "uuid-sprint",
  "tasks": {
    "total": 15,
    "compliant": 12,
    "nonCompliant": 2,
    "pending": 1
  },
  "checks": {
    "total": 180,
    "passed": 165,
    "failed": 10,
    "skipped": 5
  },
  "criticalBlockers": [
    {
      "taskId": "uuid-task-1",
      "taskCode": "VTT-123",
      "checkCode": "unit_tests_pass",
      "message": "3 tests failing"
    }
  ],
  "canCloseSprin": false
}
```

### 6.4 Override de check fallido

```
POST /api/compliance-results/:resultId/override
```

```json
{
  "overrideBy": "uuid-pm",
  "reason": "Falso positivo - el valor es configurable en runtime",
  "approvedBy": "uuid-tl"
}
```

**Requiere:** PM o TL para override. Se registra en auditoría.

---

## 7. CONFIGURACIÓN DE CHECKS

### 7.1 Checks por proyecto

```
GET /api/projects/:projectId/compliance-config
```

```json
{
  "projectId": "uuid",
  "checks": [
    {
      "checkCode": "typescript_strict",
      "enabled": true,
      "severity": "high",
      "config": {}
    },
    {
      "checkCode": "coverage_minimum",
      "enabled": true,
      "severity": "high",
      "config": {
        "minimumPercent": 80
      }
    },
    {
      "checkCode": "no_hardcoded_values",
      "enabled": true,
      "severity": "high",
      "config": {
        "patterns": ["localhost", "127.0.0.1", "password", "secret"],
        "excludePaths": ["*.test.ts", "*.spec.ts"]
      }
    }
  ],
  "gates": {
    "blockTaskCompletion": ["critical", "high"],
    "blockSprintClose": ["critical"],
    "blockReleaseClose": ["critical"]
  }
}
```

### 7.2 Actualizar configuración

```
PATCH /api/projects/:projectId/compliance-config
```

```json
{
  "checks": [
    {
      "checkCode": "coverage_minimum",
      "config": {
        "minimumPercent": 70
      }
    }
  ]
}
```

---

## 8. INTEGRACIÓN CON CI/CD

### 8.1 Webhook desde GitHub Actions

```
POST /api/webhooks/compliance
```

```json
{
  "source": "github_actions",
  "taskCode": "VTT-123",
  "prNumber": 125,
  "checks": [
    {
      "checkCode": "unit_tests_pass",
      "status": "passed",
      "details": { "testsRun": 45, "testsPassed": 45 }
    },
    {
      "checkCode": "lint_passed",
      "status": "passed"
    }
  ]
}
```

### 8.2 Trigger automático

Los checks automáticos se ejecutan cuando:
- Tarea pasa a `in_review`
- PR se crea/actualiza
- Sprint intenta cerrarse
- Release intenta cerrarse

---

## 9. ¿ES BLOQUEANTE?

| Situación | Severidad | ¿Bloquea? |
|-----------|-----------|-----------|
| Check critical fallido | critical | ✅ Sí |
| Check high fallido | high | ⚠️ Configurable |
| Check medium fallido | medium | ❌ No (warning) |
| Check low fallido | low | ❌ No (info) |

### Gates configurables

```json
{
  "gates": {
    "blockTaskCompletion": ["critical", "high"],
    "blockSprintClose": ["critical"],
    "blockReleaseClose": ["critical"]
  }
}
```

---

## 10. RESPONSABLES

| Acción | PM | TL | QA | Agente |
|--------|----|----|----|----|
| Configurar checks del proyecto | ✅ | ✅ | ❌ | ❌ |
| Ejecutar checks | ✅ | ✅ | ✅ | ✅ |
| Resolver check manual | ❌ | ✅ | ✅ | ❌ |
| Override de check | ✅ | ✅ | ❌ | ❌ |
| Ver resultados | ✅ | ✅ | ✅ | ✅ |

---

## 11. ENDPOINTS

### Ejecución

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/tasks/:taskId/run-compliance` | Ejecutar checks en tarea |
| GET | `/api/tasks/:taskId/compliance-results` | Ver resultados de tarea |
| GET | `/api/sprints/:sprintId/compliance-summary` | Resumen del sprint |
| GET | `/api/releases/:releaseId/compliance-summary` | Resumen del release |

### Resolución

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/compliance-results/:id/resolve` | Resolver check manual |
| POST | `/api/compliance-results/:id/override` | Override con justificación |

### Configuración

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/compliance-checks` | Listar checks disponibles |
| GET | `/api/projects/:projectId/compliance-config` | Ver config del proyecto |
| PATCH | `/api/projects/:projectId/compliance-config` | Actualizar config |

### Webhooks

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/webhooks/compliance` | Recibir resultados de CI/CD |

---

## 12. TABLAS EN BASE DE DATOS

### compliance_checks

```sql
CREATE TABLE compliance_checks (
  code VARCHAR(50) PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  category VARCHAR(50) NOT NULL,  -- code_quality, documentation, testing, security, process
  check_type VARCHAR(50) NOT NULL,  -- auto, manual, hybrid
  default_severity VARCHAR(50) DEFAULT 'medium',
  validation_rule JSONB,  -- Config para checks automáticos
  is_active BOOLEAN DEFAULT true,
  sort_order INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_compliance_category ON compliance_checks(category);
```

### project_compliance_config

```sql
CREATE TABLE project_compliance_config (
  id TEXT PRIMARY KEY,
  project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  check_code VARCHAR(50) NOT NULL REFERENCES compliance_checks(code),
  
  enabled BOOLEAN DEFAULT true,
  severity VARCHAR(50),  -- Override de default
  config JSONB,  -- Config específica del proyecto
  
  UNIQUE(project_id, check_code)
);

CREATE INDEX idx_project_compliance ON project_compliance_config(project_id);
```

### compliance_results

```sql
CREATE TABLE compliance_results (
  id TEXT PRIMARY KEY,
  task_id TEXT NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
  check_code VARCHAR(50) NOT NULL REFERENCES compliance_checks(code),
  
  status VARCHAR(50) NOT NULL,  -- passed, failed, skipped, overridden
  severity VARCHAR(50) NOT NULL,
  message TEXT,
  details JSONB,
  
  executed_at TIMESTAMP DEFAULT NOW(),
  executed_by TEXT REFERENCES users(id),
  
  -- Para resolución manual
  resolved_at TIMESTAMP,
  resolved_by TEXT REFERENCES users(id),
  resolution_notes TEXT,
  
  -- Para override
  overridden_at TIMESTAMP,
  overridden_by TEXT REFERENCES users(id),
  override_reason TEXT,
  override_approved_by TEXT REFERENCES users(id)
);

CREATE INDEX idx_compliance_results_task ON compliance_results(task_id);
CREATE INDEX idx_compliance_results_status ON compliance_results(status);
```

---

## 13. SEEDS

```sql
INSERT INTO compliance_checks (code, name, description, category, check_type, default_severity, sort_order) VALUES
-- Code Quality
('typescript_strict', 'TypeScript Strict', 'Código compila sin errores TypeScript', 'code_quality', 'auto', 'high', 1),
('no_console_log', 'No Console.log', 'Sin console.log en código de producción', 'code_quality', 'auto', 'medium', 2),
('no_todo_comments', 'No TODO Comments', 'Sin TODOs sin resolver', 'code_quality', 'auto', 'low', 3),
('lint_passed', 'Lint Passed', 'ESLint sin errores', 'code_quality', 'auto', 'medium', 4),
('no_hardcoded_values', 'No Hardcoded Values', 'Sin valores hardcodeados', 'code_quality', 'hybrid', 'high', 5),

-- Documentation
('devlog_created', 'Devlog Created', 'Devlog de tarea existe', 'documentation', 'auto', 'medium', 1),
('code_logic_exists', 'Code Logic Exists', 'Archivo .LOGIC.md existe', 'documentation', 'auto', 'medium', 2),
('swagger_updated', 'Swagger Updated', 'Swagger actualizado para endpoints', 'documentation', 'manual', 'medium', 3),

-- Testing
('unit_tests_pass', 'Unit Tests Pass', 'Todos los tests unitarios pasan', 'testing', 'auto', 'critical', 1),
('coverage_minimum', 'Coverage Minimum', 'Cobertura mínima alcanzada', 'testing', 'auto', 'high', 2),
('manual_qa_approved', 'Manual QA Approved', 'QA aprueba manualmente', 'testing', 'manual', 'critical', 3),

-- Security
('no_secrets_exposed', 'No Secrets Exposed', 'Sin secrets en código', 'security', 'auto', 'critical', 1),
('input_validation', 'Input Validation', 'Validación de inputs implementada', 'security', 'manual', 'high', 2),

-- Process
('pr_created', 'PR Created', 'Pull Request creado', 'process', 'auto', 'medium', 1),
('pr_approved', 'PR Approved', 'Pull Request aprobado', 'process', 'auto', 'high', 2),
('criteria_met', 'Criteria Met', 'DoD cumplidos', 'process', 'auto', 'critical', 3),
('no_blockers', 'No Blockers', 'Sin devlog blockers pendientes', 'process', 'auto', 'critical', 4);
```

---

## 14. FAQ

**¿Los checks se ejecutan automáticamente?**
Los de tipo `auto` sí, cuando la tarea pasa a `in_review`. Los `manual` requieren intervención.

**¿Puedo desactivar un check para mi proyecto?**
Sí. En la configuración del proyecto puedes desactivar checks específicos.

**¿Qué pasa si un check critical falla?**
Por default, bloquea el avance de la tarea. Se puede hacer override con justificación.

**¿Los checks se guardan en historial?**
Sí. Cada ejecución queda registrada con timestamp y resultados.

---

## 15. INTEGRACIÓN CON OTRAS FEATURES

| Feature | Integración |
|---------|-------------|
| **Firmas** | Checks critical deben pasar para firmar |
| **Criterios** | Check `criteria_met` valida DoD |
| **Devlog** | Check `no_blockers` valida devlog |
| **Hardcode Check** | Es un compliance check específico |
| **Tasks** | Checks se ejecutan en transiciones |

---

**Documento:** FEATURE_COMPLIANCE_CHECKS.md  
**Versión:** 1.0  
**Fecha:** 2026-05-06
