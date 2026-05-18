# ASSIGNMENT: MS-121 / INIT-A-05 — Crear 15 dependencias críticas en VTT

```
Hola PJM,

Esta tarea es tuya. Las 15 dependencias inter-fase son el HITO crítico que
permite al Gantt mostrar el flujo secuencial correcto entre fases. Sin esto,
las fases aparecen en paralelo de forma incorrecta.

### TAREA ASIGNADA

MS-121: INIT-A-05 — Crear 15 dependencias críticas en VTT
- Estimacion: 3 horas
- Complejidad: MEDIUM
- Categoria: documentation
- Prioridad: HIGH
- Brief: knowledge/agent-tasks/briefs/phase1/BRIEF_INIT-A-05_crear-15-dependencias-criticas-en-vtt.md

---

### ANTES DE EMPEZAR

1. Este ASSIGNMENT completo
2. HO_INICIACION_MEMORY_SERVICE.md §A (tabla de 15 dependencias)
3. PROJECT_RULES.md §3 y §9

---

### CREDENCIALES

Agente PJM:
    userId:     0ff63a29-0bc0-465a-b9bd-5f71476bc91d
    serviceKey: hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d

API VTT:
    Base:    http://77.42.88.106:3000
    Auth:    POST /api/auth/service-token

Status UUIDs:
    task_in_progress: 2a76888a-e595-4cfc-ac4c-a3ae5087ef56
    task_in_review:   1ec975a5-7581-4a1a-ab8f-51b1a7ef868d

---

### LAS 15 DEPENDENCIAS A CREAR

Endpoint: POST /api/tasks/{taskId}/dependencies
Body: {"dependsOnTaskId": "<ID>", "type": "blocks"}

| # | From (bloquea) | To (bloqueado) | Razón |
|---|----------------|----------------|-------|
| 1  | MS-025 | MS-039 | Analysis completo antes de Design Technical |
| 2  | MS-039 | MS-048 | Design Technical antes de Development S01 |
| 3  | MS-048 | MS-053 | S01 completo antes de S02 |
| 4  | MS-053 | MS-058 | S02 completo antes de S03 |
| 5  | MS-058 | MS-063 | S03 completo antes de S04 |
| 6  | MS-063 | MS-069 | S04 completo antes de S05 |
| 7  | MS-069 | MS-075 | S05 completo antes de S06 |
| 8  | MS-038 | MS-081 | 🚨 HITO: Design Handoff Final bloquea primera tarea FE |
| 9  | MS-081 | MS-086 | UI-01 completo antes de UI-02 |
| 10 | MS-086 | MS-089 | UI-02 completo antes de UI-03 |
| 11 | MS-089 | MS-091 | UI-03 completo antes de UI-04 |
| 12 | MS-080 | MS-094 | Backend S06 + UI completos antes de Testing |
| 13 | MS-093 | MS-094 | UI-04 completo antes de Testing |
| 14 | MS-103 | MS-104 | Testing aprobado antes de Deploy |
| 15 | MS-110 | MS-111 | Deploy completo antes de Operations |

---

### ENTREGABLES OBLIGATORIOS

| # | Entregable | Aplica |
|---|------------|--------|
| 1 | Script Python ejecutado | SI |
| 2 | Development Log | SI |
| 3 | Code Logic | SI |
| 4 | Git (rama + commit) | SI |

---

### WORKFLOW (12 pasos)

Paso 0: Crear rama
    git checkout -b feature/MS-121

Paso 1: Mover a task_in_progress

Paso 2: Obtener JWT PJM

Paso 3: Verificar que las dependencias no existen ya
    GET /api/tasks/MS-048/dependencies
    # Verificar que no hay duplicados antes de crear

Paso 4: Crear script memory-service-project/Release2.0/scripts/create_15_deps_vtt.py
    con las 15 dependencias de la tabla

Paso 5: Ejecutar script
    python3 memory-service-project/Release2.0/scripts/create_15_deps_vtt.py
    # Resultado esperado: 15 OK, 0 errores

Paso 6: Verificar dependencia crítica MS-038 → MS-081
    GET /api/tasks/MS-081/dependencies
    # Debe mostrar MS-038 como bloqueante

Paso 7: Guardar reporte en /tmp/deps_results.json

Paso 8: Crear DevLog:
    devlogs/2026-04-24_MS-121_crear-15-dependencias-vtt.md

Paso 9: Crear Code Logic:
    knowledge/code-logic/phase1/MS-121_deps-script.LOGIC.md

Paso 10: Commit y push

Paso 11: Subir attachments a VTT (devlog, code_logic, script)

Paso 12: Mover a task_in_review

---

### CHECKLIST DE EXITO

- [ ] 15 dependencias POST exitoso (0 errores)
- [ ] MS-038 → MS-081 verificado con GET
- [ ] Cada dep tiene type="blocks"
- [ ] Reporte JSON guardado
- [ ] DevLog con resultado por dependencia

---

### FORMATO DE REPORTE

    ## Entrega: MS-121 - INIT-A-05: 15 dependencias VTT

    ### Resultado:
    - Creadas: [N]/15
    - Errores: [N]
    - Dependencia crítica MS-038→MS-081: [OK/ERROR]

    ### Development Log:
    devlogs/2026-04-24_MS-121_crear-15-dependencias-vtt.md

    ### Commit SHA: [hash]

---

Saludos,
PJM (auto-asignación)
```

---

## Metadata

- **Archivo**: `knowledge/agent-tasks/assignments/phase1/ASSIGNMENT_MS-121_crear-15-dependencias-vtt.md`
- **Fecha generacion**: 2026-04-24
- **Version**: 1.0
- **Estado**: Ready
