# 00.Rules — Sistema de Reglas VTT

| Campo | Valor |
|---|---|
| **Versión** | 1.0 |
| **Fecha** | 2026-05-13 |
| **Nivel en el modelo normativo** | Nivel 0 (transversal a Protocols/Workflows/Skills/Scripts) |
| **Mantenedor** | PM Martin Rivas |
| **Source of Truth** | `virtual-teams-setup/00-platform/07.Normativa/00.Rules/` |
| **Fuentes externas** | `00-platform/04.Process/01.authorizaton/doc_sec_01..04.md` |

---

## 1. Propósito

Definir el **modelo de Reglas VTT** que gobierna qué puede hacer cada actor (humano o agente) sobre cada recurso del sistema, en cada scope, bajo qué condiciones.

Las reglas son **transversales** — no son procedimientos (Protocols/Workflows) ni capacidades (Skills) ni comandos (Scripts). Son **restricciones/condiciones** que cualquier nivel operativo debe respetar.

## 2. Alineación con doc_sec_01..04

Este sistema **implementa** el modelo de autorización del Bloque 1 definido en:

- `doc_sec_01_modelo_seguridad_actores_scopes` — actores, recursos, jerarquía
- `doc_sec_02_politicas_permisos_rbac_abac` — RBAC + ABAC + reglas + acciones humanas
- `doc_sec_03_arquitectura_implementacion_autorizacion` — middleware + policies
- `doc_sec_04_matriz_autorizacion` — matriz capability × rol

**No reemplaza esos documentos.** Los operacionaliza convirtiéndolos en JSONs consultables + reglas catalogadas.

## 3. Componentes del sistema

| Archivo | Propósito |
|---|---|
| `README.md` | Este archivo — manifiesto del sistema |
| `rules_schema.json` | JSON Schema validador del catálogo de reglas |
| `rules_catalog.json` | Catálogo maestro de reglas (este es el "índice consultable") |
| `capabilities_catalog.json` | 30 capabilities base de doc_sec_02 §4 |
| `roles_catalog.json` | 9 roles + matriz RBAC de doc_sec_04 §4.3 |
| `query_rules.py` | Motor de filtros (resolución jerárquica) — prueba sin BD |
| `extract_rules_from_md.py` | Extractor para migrar reglas de .md a JSON |
| `sources/` | Copias .md de los archivos fuente (auditoría) |

## 4. Modelo de Reglas — 4 dimensiones

Cada regla se define en 4 dimensiones ortogonales:

### 4.1 Scope jerárquico (8 niveles)

```
1. PLATFORM       (toda la plataforma VTT)
2. ORGANIZATION   (tenant lógico)
3. WORKSPACE      (proyecto lógico bajo org)
4. PROJECT        (proyecto operativo en VTT)
5. PHASE          (fase del SDLC)
6. TASK           (tareas que cumplen criterios)
7. ROLE           (rol del actor: BE, FE, TL, etc.)
8. AGENT          (instancia específica por UUID)
```

> Los niveles 1-4 vienen de **doc_sec_01 §7** (jerarquía Platform → Org → Workspace → Resource).
> Los niveles 5-8 son extensiones VTT-específicas necesarias para reglas operativas.

### 4.2 Tipo de actor

Ortogonal al scope:

```
- HUMAN              (usuario humano)
- AGENT              (operador IA delegado)
- SERVICE_ACCOUNT    (futuro — doc_sec_01 §4.3)
- EXTERNAL           (futuro — doc_sec_01 §4.4)
```

### 4.3 Capabilities requeridas

La regla puede exigir que el actor tenga ciertas capabilities (del catálogo de 30 en `capabilities_catalog.json`).

Ejemplo: regla "solo aprobar si tiene `tasks.approve`" → `required_capabilities: ["tasks.approve"]`.

### 4.4 Markers (banderas operativas)

```
- mandatory          (bloquea si no se cumple)
- sensitive          (acción sensible — log obligatorio)
- human_only         (no aplica a agentes — doc_sec_01 §12)
- sod_enforcement    (Segregación de Funciones)
- blocks_review_gate (bloquea el Review Gate de la tarea)
- auto_detect        (el sistema puede detectar violación automáticamente)
```

## 5. Resolución de reglas aplicables

```python
def get_applicable_rules(context):
    """
    context = {
        "actor_type": "HUMAN" | "AGENT",
        "actor_role": "ws_developer" | "ws_tech_lead" | ...,
        "actor_id": "<uuid>",
        "actor_capabilities": ["tasks.read", "tasks.update", ...],
        "organization_id": "<uuid>",
        "workspace_id": "<uuid>",
        "project_id": "<uuid>",
        "phase_id": "<uuid>",
        "task": {
            "id": "MS-XXX",
            "category": "feature",
            "has_endpoints": True,
            ...
        }
    }
    """
    return [
        rule for rule in catalog
        if matches_scope(rule, context)
        and matches_actor_type(rule, context)
        and has_required_capabilities(rule, context)
    ]
```

Ver implementación en `query_rules.py`.

## 6. Cómo se usa el sistema

### 6.1 Hoy (sin BD — modo archivo)

```
1. Agente inicia sesión → llama a query_rules.py con su contexto
2. Script lee rules_catalog.json + capabilities_catalog.json
3. Aplica filtros de scope + actor + capabilities
4. Devuelve lista de reglas que el agente DEBE respetar
5. El prompt del agente incluye esa lista
6. El agente las respeta durante ejecución
```

### 6.2 Mañana (con feature VTT — ver IMPROVE-004)

```
1. Hook Manager intercepta inicio de sesión del agente
2. Consulta GET /api/rules/applicable?taskId=MS-XXX&agentId=<uuid>
3. Backend resuelve usando misma lógica de query_rules.py
4. Backend devuelve lista de reglas + capabilities efectivas
5. Hook inyecta al prompt del agente
6. Validación post-ejecución registra violaciones en tabla rule_violations
```

## 7. Cómo agregar una regla nueva

### 7.1 Manual (hoy)

```
1. Editar rules_catalog.json
2. Agregar objeto en array "rules" siguiendo rules_schema.json
3. Validar con: python query_rules.py --validate
4. Probar con: python query_rules.py --simulate <contexto>
5. Si la regla viene de un .md fuente, agregar copia en sources/
6. Actualizar summary del catalog
```

### 7.2 Futuro (con BD)

```
PM o TL via UI VTT:
  POST /api/rules
  {
    "code": "RULE-XXX-NN",
    "title": "...",
    "scope": {...},
    "actor_types": ["AGENT"],
    "markers": {...}
  }
  → Backend valida contra rules_schema
  → Inserta en tabla rules
  → Disponible para agentes en próxima sesión
```

## 8. Estructura de un Rule (resumen)

```json
{
  "id": "RULE-CODE-001",
  "title": "UN archivo .LOGIC.md por archivo de código",
  "rule_text": "Por cada archivo creado/modificado en /src...",
  "status": "active",
  "scope": {
    "level": "TASK",
    "task_criteria": {"has_code_files": true},
    "role_codes": ["ws_developer", "ws_tech_lead"]
  },
  "actor_types": ["AGENT", "HUMAN"],
  "required_capabilities": ["tasks.update"],
  "markers": {
    "mandatory": true,
    "sensitive": false,
    "human_only": false,
    "sod_enforcement": false,
    "blocks_review_gate": true,
    "auto_detect": true
  },
  "violation": {
    "severity": "high",
    "action": "block_review_gate",
    "auto_detect_query": "diff vs .LOGIC.md tree"
  },
  "source_origin": {
    "file": "03.standard/09.AGENT_RULES_Rev.md",
    "section": "§4 Reglas de Code Logic"
  },
  "examples": {
    "compliant": "src/controllers/userController.ts + knowledge/code-logic/controllers/userController.LOGIC.md",
    "violation": "src/controllers/userController.ts sin LOGIC.md correspondiente"
  },
  "tags": ["code-logic", "documentation"]
}
```

Ver schema completo en `rules_schema.json`.

## 9. Diferencia con otros niveles del modelo VTT

| Nivel | ¿Qué define? | Ejemplo |
|---|---|---|
| **Rule (Nivel 0)** | **Restricción/condición transversal** | "Tareas con código → code_logic obligatorio" |
| Protocol (Nivel 4) | Proceso de negocio end-to-end | "Ciclo de asignación y cierre de tarea" |
| Workflow (Nivel 3) | Pasos secuenciales | "Generar y subir BRIEFs" |
| Skill (Nivel 2) | Capacidad reusable | "Subir attachment a tarea" |
| Script (Nivel 1) | Comando atómico | "POST /attachments multipart" |

## 10. Referencias

### Documentos fuente

| Fuente | Ubicación | Contenido extraído |
|---|---|---|
| `doc_sec_01_modelo_seguridad_actores_scopes` | `04.Process/01.authorizaton/` | Niveles de scope (Platform→Org→Workspace→Resource), tipos de actor, recursos protegidos, SoD |
| `doc_sec_02_politicas_permisos_rbac_abac` | `04.Process/01.authorizaton/` | 30 capabilities, 9 roles, reglas ABAC (DEV-01..AG-03, CR-01..03), acciones humanas |
| `doc_sec_03_arquitectura_implementacion_autorizacion` | `04.Process/01.authorizaton/` | Middleware authenticate / resolveAuthorizationContext / requireCapability / requirePolicy |
| `doc_sec_04_matriz_autorizacion` | `04.Process/01.authorizaton/` | Matriz RBAC capability×rol completa |
| `AGENT_RULES_Rev.md` v1.3 | `03.standard/` | Reglas operativas de agentes (workflow, entregables, calidad código, commits, etc.) |

### Improvements relacionados

- `IMPROVE-004` — Rules como feature VTT (este sistema en BD con endpoints)
- `IMPROVE-005` — Extensión del modelo a recursos VTT-específicos (TIs, manifests, devlogs, LDs)

### Política de actualización

| Cambio | Acción |
|---|---|
| Nueva regla detectada | Agregar a `rules_catalog.json` + actualizar summary |
| Regla obsoleta | Cambiar `status` a `deprecated`, no borrar |
| Cambio en doc_sec_01..04 (fuente) | Re-sincronizar `capabilities_catalog.json` y `roles_catalog.json` |
| Cambio de schema | Bump versión + migrar reglas existentes |

---

## 11. Changelog

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-05-13 | Versión inicial. Modelo de 8 niveles + 4 tipos de actor + capabilities + markers. Alineado con doc_sec_01..04 del Bloque 1 de autorización. |
