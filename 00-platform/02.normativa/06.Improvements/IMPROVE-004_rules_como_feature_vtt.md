# IMPROVE-004 — Rules como Feature VTT (basado en doc_sec_01..04)

| Campo | Valor |
|---|---|
| **Código** | `IMPROVE-004` |
| **Título** | Sistema de Reglas como Feature VTT — Bloque 1 Autorización + Reglas Operativas |
| **Categoría** | Backend / Authorization / Governance |
| **Prioridad** | 🟡 Media |
| **Estimación rough** | 12-15 días (MVP) |
| **Estado** | Propuesta — pendiente de evaluación PM |
| **Autor** | PM Martin Rivas |
| **Fecha** | 2026-05-13 |
| **Origen** | Sesión de Normativa VTT — implementación operativa de doc_sec_01..04 |

---

## Relación con otras mejoras

- **IMPROVE-001 (Pool de Transacciones)**: independiente. El Pool valida reglas antes de ejecutar operaciones (lookup rápido de capabilities + ABAC).
- **IMPROVE-002 (BD de Manifiestos)**: complementaria. Las violaciones de reglas se registran en audit log accesible via reportes.
- **IMPROVE-003 (Platform Gaps)**: independiente. Los gaps son fixes API, este es nueva feature.
- **IMPROVE-005 (Recursos VTT-específicos)**: **complementaria directa**. IMPROVE-004 implementa el motor; IMPROVE-005 extiende los recursos protegidos (TIs, manifests, devlogs, LDs).

---

## 1. Problema que resuelve

El sistema VTT actual no tiene mecanismo formal para:

| Necesidad operativa | Estado actual |
|---|---|
| Verificar qué puede hacer un actor en un recurso | Implícito en código de cada endpoint |
| Validar separación de funciones (SoD) | Lógica dispersa, sin enforcement central |
| Distinguir humano vs agente en acciones críticas | No implementado — agente puede aprobar |
| Aplicar reglas por scope (project/phase/task/role) | Imposible — reglas viven en archivos .md |
| Reportar violaciones de reglas | No existe audit |
| Cambiar políticas sin redeploy | Requiere editar código |
| Reglas operativas (modelo dinámico, manifest al final, etc.) | En archivos .md — agentes pueden no leerlos |

**Documentación existente que ya define el modelo (no implementado):**

- `doc_sec_01_modelo_seguridad_actores_scopes` — actores, recursos, jerarquía
- `doc_sec_02_politicas_permisos_rbac_abac` — 30 capabilities + 9 roles + reglas ABAC
- `doc_sec_03_arquitectura_implementacion_autorizacion` — middleware
- `doc_sec_04_matriz_autorizacion` — matriz capability × rol

**Lo que ya tenemos en disco (sin BD):**

```
07.Normativa/00.Rules/
├── README.md
├── rules_schema.json
├── rules_catalog.json      ← 43 reglas
├── capabilities_catalog.json  ← 30 capabilities
├── roles_catalog.json      ← 9 roles + matriz RBAC
└── query_rules.py          ← motor de filtros funcional
```

**Lo que falta:** convertir esto en **feature operativa de VTT** consultable via API y vinculada con el motor de autorización del backend.

## 2. Impacto / valor que aporta

### Cuantitativo
- **0 violaciones de SoD** (hoy: agentes pueden aprobar tareas en teoría)
- **100% auditabilidad** de operaciones sensibles (hoy: sin audit log estandarizado)
- **Reducción de incidentes** tipo PROC-COORD-01 (perder código por checkout cruzado)
- **Time-to-policy-change**: de "editar archivo + reiniciar agentes" a "cambiar row en BD"

### Cualitativo
- **Compliance** facilitado (auditoría externa puede ver matriz RBAC + log de violaciones)
- **Onboarding** de agentes nuevos automatizado (reglas inyectadas via Hook Manager)
- **Evolución del modelo** sin tocar código (PM define regla nueva por API)
- **Escalabilidad**: agregar nuevo proyecto = reusar reglas Platform/Org

## 3. Solución propuesta

### 3.1 Componentes a implementar

```
┌─────────────────────────────────────────────────────────────────┐
│ RULES ENGINE VTT                                                 │
│                                                                  │
│  1. Database (Postgres)                                          │
│     - rules                                                      │
│     - capabilities                                               │
│     - roles                                                      │
│     - rule_violations (audit log)                                │
│                                                                  │
│  2. REST API                                                     │
│     - GET /api/rules?level=X&actor_type=Y&...                    │
│     - GET /api/rules/applicable?taskId=X&agentId=Y               │
│     - POST /api/rules (PM crea regla)                            │
│     - PATCH /api/rules/:id (PM modifica)                         │
│     - DELETE /api/rules/:id (PM desactiva)                       │
│     - GET /api/capabilities                                      │
│     - GET /api/roles                                             │
│     - POST /api/rule-violations (registrar violación)            │
│     - GET /api/rule-violations?taskId=X (reportes)               │
│                                                                  │
│  3. Authorization Middleware (doc_sec_03)                        │
│     - authenticate                                               │
│     - resolveAuthorizationContext                                │
│     - requireCapability                                          │
│     - requirePolicy (consulta Rules Engine)                      │
│     - auditDecision                                              │
│                                                                  │
│  4. Hook Manager integration                                     │
│     - Al iniciar sesión de agente:                               │
│       1. Llama a /api/rules/applicable                           │
│       2. Inyecta lista de reglas al prompt del agente            │
│     - Al fin de sesión:                                          │
│       1. Detecta violaciones automáticas (auto_detect=true)      │
│       2. Registra en /api/rule-violations                        │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Schema SQL

```sql
-- 30 capabilities base
CREATE TABLE capabilities (
  code VARCHAR(64) PRIMARY KEY,
  group_code VARCHAR(32) NOT NULL,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  abac_required BOOLEAN DEFAULT TRUE,
  abac_rule_codes TEXT[],
  human_only BOOLEAN DEFAULT FALSE,
  sensitive BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 9 roles + futuros
CREATE TABLE roles (
  code VARCHAR(64) PRIMARY KEY,
  scope_level VARCHAR(32) NOT NULL,  -- PLATFORM | ORGANIZATION | WORKSPACE
  title VARCHAR(255) NOT NULL,
  description TEXT,
  policy TEXT,
  actor_types VARCHAR(32)[] NOT NULL,
  human_only BOOLEAN DEFAULT FALSE,
  can_approve BOOLEAN DEFAULT FALSE,
  sensitive BOOLEAN DEFAULT FALSE
);

-- Matriz RBAC role × capability
CREATE TABLE role_capabilities (
  role_code VARCHAR(64) REFERENCES roles(code),
  capability_code VARCHAR(64) REFERENCES capabilities(code),
  abac_marker VARCHAR(8),  -- NULL | * | ** | *** | **** | *****
  notes TEXT,
  PRIMARY KEY (role_code, capability_code)
);

-- Reglas
CREATE TABLE rules (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  code VARCHAR(64) UNIQUE NOT NULL,        -- RULE-XXX-NNN
  title VARCHAR(255) NOT NULL,
  rule_text TEXT NOT NULL,
  status VARCHAR(16) NOT NULL DEFAULT 'active',
  version VARCHAR(16) DEFAULT '1.0',

  -- Scope (jerarquía)
  scope_level VARCHAR(32) NOT NULL,        -- PLATFORM | ... | AGENT
  organization_id UUID REFERENCES organizations(id),
  workspace_id UUID REFERENCES workspaces(id),
  project_id UUID REFERENCES projects(id),
  phase_id UUID REFERENCES phases(id),
  phase_key VARCHAR(16),                   -- alias '04-Development'
  task_criteria JSONB,                     -- {category: 'feature', has_endpoints: true}
  role_codes VARCHAR(64)[],                -- ['ws_developer']
  agent_id UUID,                           -- scope=AGENT

  -- Actor
  actor_types VARCHAR(32)[] NOT NULL,

  -- Requisitos
  required_capabilities VARCHAR(64)[],
  required_role_codes VARCHAR(64)[],

  -- Markers
  mandatory BOOLEAN DEFAULT TRUE,
  sensitive BOOLEAN DEFAULT FALSE,
  human_only BOOLEAN DEFAULT FALSE,
  sod_enforcement BOOLEAN DEFAULT FALSE,
  blocks_review_gate BOOLEAN DEFAULT FALSE,
  auto_detect BOOLEAN DEFAULT FALSE,
  agent_default_forbidden BOOLEAN DEFAULT FALSE,

  -- Violation
  violation_severity VARCHAR(16),          -- critical | high | medium | low
  violation_action VARCHAR(64),            -- block | warn | block_and_escalate | log_only
  auto_detect_query TEXT,
  escalate_to_role VARCHAR(64),

  -- Origin
  source_file VARCHAR(512),
  source_section VARCHAR(255),
  source_rule_label VARCHAR(64),

  -- Metadata
  tags VARCHAR(64)[],
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  created_by UUID
);

CREATE INDEX idx_rules_scope ON rules(scope_level, status);
CREATE INDEX idx_rules_phase ON rules(phase_key) WHERE status = 'active';
CREATE INDEX idx_rules_jsonb ON rules USING GIN (task_criteria);

-- Audit log de violaciones
CREATE TABLE rule_violations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  rule_id UUID REFERENCES rules(id),
  rule_code VARCHAR(64),
  actor_id UUID,
  actor_type VARCHAR(32),
  actor_role VARCHAR(64),
  task_id VARCHAR(64),
  resource_type VARCHAR(64),
  resource_id UUID,
  severity VARCHAR(16),
  action_taken VARCHAR(64),         -- blocked | warned | escalated
  detection_method VARCHAR(32),     -- auto | manual
  context_snapshot JSONB,
  resolution TEXT,
  detected_at TIMESTAMPTZ DEFAULT NOW(),
  resolved_at TIMESTAMPTZ
);

CREATE INDEX idx_violations_task ON rule_violations(task_id);
CREATE INDEX idx_violations_actor ON rule_violations(actor_id);
CREATE INDEX idx_violations_unresolved ON rule_violations(resolved_at) WHERE resolved_at IS NULL;
```

### 3.3 Endpoint clave: `/api/rules/applicable`

```http
GET /api/rules/applicable?taskId=MS-285&agentId=<uuid>
```

Response:

```json
{
  "data": {
    "context": {
      "task_id": "MS-285",
      "actor_type": "AGENT",
      "actor_role": "ws_developer",
      "phase_key": "04",
      "task_attributes": {
        "category": "feature",
        "has_endpoints": true,
        "has_code_files": true
      }
    },
    "applicable_rules": [
      {
        "code": "RULE-CODE-001",
        "title": "UN archivo .LOGIC.md por archivo de código",
        "severity": "high",
        "markers": ["mandatory", "blocks_review_gate", "auto_detect"]
      }
    ],
    "summary": {
      "total": 31,
      "mandatory": 31,
      "blocks_review_gate": 5,
      "human_only": 0,
      "sod_enforcement": 4
    }
  }
}
```

### 3.4 Integración con Hook Manager

```
1. Hook intercepta SessionStart de agente
2. Hook llama: GET /api/rules/applicable?agentId=<uuid>&taskId=<id>
3. Hook formatea reglas como prompt:
   "REGLAS APLICABLES A ESTA SESIÓN:
   - [RULE-CODE-001] UN archivo .LOGIC.md por archivo de código
   - [RULE-GIT-004] PROHIBIDO commit directo a main
   - ..."
4. Hook inyecta al system prompt del agente
5. Agente las respeta durante ejecución
6. Al fin de sesión, hook ejecuta auto-detect:
   - Para cada regla con auto_detect=true, evalúa la query
   - Si detecta violación, POST /api/rule-violations
7. PM/TL ven dashboard de violaciones
```

### 3.5 Caso de uso: PM define regla nueva sin código

```
Usuario al PM:
   "Quiero que todos los endpoints nuevos tengan rate limiting"

PM define vía UI VTT:
   POST /api/rules
   {
     "code": "RULE-API-002",
     "title": "Rate limiting obligatorio en endpoints",
     "rule_text": "...",
     "scope": {
       "level": "TASK",
       "task_criteria": {"has_endpoints": true}
     },
     "actor_types": ["AGENT", "HUMAN"],
     "required_role_codes": ["ws_developer", "ws_tech_lead"],
     "markers": {
       "mandatory": true,
       "blocks_review_gate": true,
       "auto_detect": true
     },
     "violation": {
       "severity": "high",
       "action": "block_review_gate",
       "auto_detect_query": "grep 'rateLimit' on new routes"
     }
   }

→ A partir de ese momento, cualquier tarea con has_endpoints=true
   recibe esta regla automáticamente en el prompt del agente.
→ Hook detecta automáticamente si el agente la cumplió.
```

## 4. Plan de implementación (MVP)

### Fase 1 — Schema + Seeding (3 días)
- Crear tablas: capabilities, roles, role_capabilities, rules, rule_violations
- Seed inicial desde JSONs en 07.Normativa/00.Rules/:
  - 30 capabilities
  - 9 roles + matriz RBAC
  - 43 reglas iniciales
- Validar contra schema actual de VTT

### Fase 2 — Read API (2 días)
- `GET /api/rules?level=...&status=active`
- `GET /api/rules/:id`
- `GET /api/capabilities`
- `GET /api/roles`
- `GET /api/role-capabilities?role=...`

### Fase 3 — Write API (2 días)
- `POST /api/rules` (con validación contra rules_schema.json)
- `PATCH /api/rules/:id`
- `DELETE /api/rules/:id` (soft delete → status=deprecated)

### Fase 4 — Resolution Engine (3 días)
- `GET /api/rules/applicable?taskId=X&agentId=Y`
- Implementa lógica de query_rules.py en backend
- Resuelve context: task → project → phase → role → capabilities
- Cache de capabilities por rol

### Fase 5 — Authorization Middleware (3 días)
- Middleware `requirePolicy` integrado con Rules Engine
- Para cada request sensible: consulta reglas aplicables + valida
- Audit log automático
- Integración con doc_sec_03 (authenticate + resolveAuthorizationContext + requireCapability)

### Fase 6 — Hook Manager integration (2 días)
- SessionStart hook → consulta /rules/applicable → inyecta al prompt
- SessionEnd hook → ejecuta auto-detect → registra violaciones
- Dashboard básico de violaciones en VTT UI

**Total estimado:** 15 días (~3 semanas)

## 5. Riesgos / consideraciones

| Riesgo | Mitigación |
|---|---|
| Performance: cada request consulta reglas | Cache agresivo (Redis) + denormalización por scope |
| Cambio de reglas rompe agentes corriendo | Versionado de reglas + grace period |
| Auto-detect genera falsos positivos | `auto_detect_query` se prueba contra catálogo antes de activar |
| Migración de reglas .md a BD | Script idempotente que lee JSONs actuales |
| Conflictos entre reglas (una permite, otra bloquea) | Reglas con `severity=critical` ganan; documentar precedencia |
| Reglas obsoletas se acumulan | `status=deprecated` + reporte mensual de limpieza |

## 6. Decisión solicitada al PM

1. **¿Aprobar esta mejora?** Es la base operativa de doc_sec_01..04.
2. **¿Implementar antes, después o junto con IMPROVE-005 (recursos VTT-específicos)?** Recomendación: junto — comparten schema y endpoints.
3. **¿Implementar como tarea VTT del proyecto VTT?** O contratar dev externo.
4. **¿Cache layer (Redis)?** O empezar sin cache y agregar después si performance lo exige.
5. **¿Hook Manager existe ya o se construye en paralelo?** Si no existe, IMPROVE-004 puede entregarse sin Hook (reglas consultables vía API + reportes manuales).

## 7. Referencias

- Documentos fuente:
  - `04.Process/01.authorizaton/doc_sec_01..04.md` (Bloque 1 autorización)
  - `03.standard/09.AGENT_RULES_Rev.md` (reglas operativas de agentes)
- Implementación piloto:
  - `07.Normativa/00.Rules/rules_catalog.json` (43 reglas)
  - `07.Normativa/00.Rules/capabilities_catalog.json` (30 capabilities)
  - `07.Normativa/00.Rules/roles_catalog.json` (9 roles)
  - `07.Normativa/00.Rules/query_rules.py` (motor de filtros funcional)
- Mejoras relacionadas:
  - `IMPROVE-001` (Pool de Transacciones)
  - `IMPROVE-002` (BD de Manifiestos)
  - `IMPROVE-005` (Recursos VTT-específicos — extensión del modelo)

## 8. Changelog

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-05-13 | Documento inicial — propuesta para evaluación PM |
