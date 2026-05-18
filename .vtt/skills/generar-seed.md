---
name: generar-seed
description: Genera el TASK_INDEX_SEED completo para cargar un proyecto en VTT — con UUIDs de usuarios, fases, deliveries, tareas y dependencias — y el script Python de carga.
role: PM
vtt_version: "1.0"
---

# Skill: /generar-seed

## Propósito
Genera el `TASK_INDEX_SEED_[PROYECTO].md` v2.x con todas las tareas expandidas y el script `create_[proyecto]_vtt.py` listo para ejecutar contra la API de VTT.

## Cuándo usar
- Después de tener el CONSOLIDADO aprobado y el HO PJM firmado
- Equivale al PASO 7 del proceso PM estándar
- Prerequisito: FASES_APLICABLES y PRE_HANDOFFs completos

## Inputs requeridos
Antes de ejecutar, leer:
1. `CONSOLIDADO_[PROYECTO].md` — lista de tareas con roles asignados
2. `Proyect_data.md` (`.claude/rules/`) — UUIDs de usuarios del proyecto
3. `ADR-001` — estrategia de repos (para saber qué tareas van a qué repo)
4. `SPEC_[PROYECTO]` — para descripción de tareas

## Pasos de ejecución

### 1. Cargar UUIDs de usuarios
Leer `.claude/rules/Proyect_data.md` para obtener los UUIDs correctos del proyecto.

**CRÍTICO:** Usar SIEMPRE los UUIDs del archivo `Proyect_data.md` del proyecto actual.
NUNCA usar UUIDs de otros proyectos ni asumir que son los mismos.

```python
USERS = {
    "PM":  "[uuid-de-Proyect_data]",
    "TL":  "[uuid-de-Proyect_data]",
    "BE":  "[uuid-de-Proyect_data]",
    "DB":  "[uuid-de-Proyect_data]",
    "FE":  "[uuid-de-Proyect_data]",
    "QA":  "[uuid-de-Proyect_data]",
    "DO":  "[uuid-de-Proyect_data]",
    "DL":  "[uuid-de-Proyect_data]",
    "SA":  "[uuid-de-Proyect_data]",
    "AR":  "[uuid-de-Proyect_data]",
    "PJM": "[uuid-de-Proyect_data]",
}
```

### 2. Definir jerarquía de carga

El script carga en este orden (por dependencias de IDs):
1. POST proyecto → obtener `project_id`
2. POST fases (phases) → obtener `phase_id[]`
3. POST deliveries (deliverables agrupados) → obtener `delivery_id[]`
4. POST tareas → obtener `task_id[]`
5. POST asignaciones tarea → delivery (task_delivery)
6. POST dependencias entre tareas

### 3. Expandir tareas del CONSOLIDADO

Para cada tarea en el CONSOLIDADO, generar tupla:
```python
("TASK_ID", "Título", "Descripción detallada", "ROL", delivery_ref, priority)
```

**Regla de prioridades:**
- `critical` — tareas de setup inicial (INIT-A, INIT-B), tareas que desbloquean >3 tareas
- `high` — tareas de desarrollo core (endpoints, schema, auth)
- `medium` — tareas de features secundarias
- `low` — documentación, cleanup

### 4. Mapear dependencias críticas

Documentar las 15 dependencias mínimas que forman el camino crítico:
- Setup → Análisis → Diseño → Desarrollo → Testing → Deploy

Formato:
```python
DEPENDENCIES = [
    ("TASK_BLOCKING_ID", "TASK_BLOCKED_ID"),
    ...
]
```

### 5. Generar script Python

El script usa estas funciones helper:
```python
def auth_token() → str          # POST /api/auth/login → JWT
def post(path, payload) → dict  # POST con auth + error handling
def extract_id(response) → str  # extrae 'id' del response
```

Flujo principal: ejecutar los 6 pasos en secuencia, capturar IDs en variables,
usar esos IDs en pasos posteriores. Incluir logging de cada paso.

### 6. Validar seed antes de entregar
- Total de tareas generadas debe coincidir con CONSOLIDADO
- Cada tarea tiene delivery asignado
- Dependencias no crean ciclos
- Todos los roles tienen al menos 1 tarea

## Output generado
- `Release[X]/01-PM/TASK_INDEX_SEED_[PROYECTO].md`
- `Release[X]/scripts/create_[proyecto]_vtt.py`

## Lección aprendida (Memory Service)
La primera versión del seed usó UUIDs incorrectos (de otro proyecto).
El script fallaba silenciosamente al asignar usuarios.
**Siempre verificar UUIDs contra `Proyect_data.md` antes de ejecutar.**

## Referencia
- Caso Memory Service: 116 tareas, 65 deliveries, 15 dependencias
- Script referencia: `Release2.0/scripts/create_memory_service_vtt.py`
- Template base: `.vtt/templates/setup/pm/TEMPLATE_create_vtt_script_V1.0.py`
