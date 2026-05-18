# TEMPLATE: Mensaje de Asignacion de Tarea

**Usar este template para generar el mensaje que el PM pega al agente en la UI.**

---

```
**Asignado a:** [ROL_AGENTE]

Hola [NOMBRE_AGENTE],

[CONTEXTO: 1-2 lineas explicando por que esta tarea existe]

### TAREA ASIGNADA

**[ID_TAREA]: [TITULO]**
- Estimacion: [X]h
- Prioridad: P[0-3] - [CRITICO/ALTO/MEDIO/BAJO]
- Brief: `knowledge/agent-tasks/BRIEF_[ID_TAREA]_[Nombre].md`
- Branch: `feature/[ID_TAREA]-[nombre-corto]`

---

### DOCUMENTOS A LEER

| # | Archivo | Por que |
|---|---------|---------|
| 1 | `[RUTA_BRIEF]` | Brief completo |
| 2 | `knowledge/PROCEDIMIENTOS_OPERATIVOS_AGENTES.md` | Reglas operativas, APIs, git flow |
| 3 | `_project-management/templates/TEMPLATE_DEVELOPMENT_LOG.md` | Template para dev log (OBLIGATORIO) |
| 4 | `_project-management/templates/TEMPLATE_CODE_LOGIC.md` | Template para code logic (OBLIGATORIO) |
| 5 | `[RUTA_ARCHIVO_REFERENCIA_1]` | [RAZON] |
| 6 | `[RUTA_ARCHIVO_REFERENCIA_2]` | [RAZON] |

---

### COMANDOS DEL SISTEMA

**Cambiar estado a in_progress:**
```bash
curl -s -X PATCH http://77.42.88.106:3000/api/tasks/[ID_TAREA]/status \
  -H "Content-Type: application/json" \
  -d '{"statusId": "2a76888a-e595-4cfc-ac4c-a3ae5087ef56", "changedBy": "[USER_ID_AGENTE]"}'
```

**Cambiar estado a in_review (al terminar):**
```bash
curl -s -X PATCH http://77.42.88.106:3000/api/tasks/[ID_TAREA]/status \
  -H "Content-Type: application/json" \
  -d '{"statusId": "1ec975a5-7581-4a1a-ab8f-51b1a7ef868d", "changedBy": "[USER_ID_AGENTE]"}'
```

---

### DATOS DEL SISTEMA

- **Tu userId:** `[USER_ID_AGENTE]`
- **Proyecto VTT:** `d837bcd5-3f10-4e19-a418-344a1eef98ad`
- **Backend API:** `http://77.42.88.106:3000`
- **Git config:**
  ```bash
  git config user.name "Martin Rivas"
  git config user.email "martin.rivas@prompt-ai.studio"
  ```

---

### ENTREGABLES OBLIGATORIOS (5)

TODA tarea debe entregar estas 5 cosas. Si falta una, la entrega esta INCOMPLETA:

| # | Entregable | Ubicacion |
|---|------------|-----------|
| 1 | **Codigo** | `/backend/...` o `/frontend/...` |
| 2 | **Development Log** | `/devlogs/YYYY-MM-DD_[ID_TAREA]_[desc].md` |
| 3 | **Code Logic** | `/knowledge/code-logic/[espejo]/*.LOGIC.md` (1 por archivo) |
| 4 | **Git** (Rama + Commit + Push + PR) | GitHub |
| 5 | **Swagger Docs** (si hay endpoints) | JSDoc inline |

---

### CODE LOGIC - REGLA

> UN archivo .LOGIC.md por CADA archivo de codigo que crees o modifiques

**Ubicacion espejo:**
```
backend/src/services/auth.service.ts
         -> knowledge/code-logic/backend/src/services/auth.service.LOGIC.md

frontend/src/pages/Login.tsx
         -> knowledge/code-logic/frontend/src/pages/Login.LOGIC.md
```

- Si CREAS archivo nuevo -> Crear `.LOGIC.md` en ubicacion espejo
- Si MODIFICAS archivo existente -> Actualizar `.LOGIC.md` existente (o crearlo si no existe)
- Usar template: `_project-management/templates/TEMPLATE_CODE_LOGIC.md`

**Archivos para esta tarea (crear/actualizar .LOGIC.md):**
- `[RUTA_ARCHIVO_1]` -> `knowledge/code-logic/[espejo]/[archivo].LOGIC.md`
- `[RUTA_ARCHIVO_2]` -> `knowledge/code-logic/[espejo]/[archivo].LOGIC.md`

---

### QUE HACER

1. Lee el brief, procedimientos operativos y templates (dev log + code logic)
2. Cambia estado a in_progress
3. Crea rama `feature/[ID_TAREA]-[nombre-corto]` desde main
4. [PASO_ESPECIFICO_1]
5. [PASO_ESPECIFICO_2]
6. [PASO_ESPECIFICO_3]
7. Crea archivos .LOGIC.md (uno por archivo de codigo creado/modificado)
8. Crea Development Log en `/devlogs/`
9. Commit, push, PR hacia main
10. Cambia estado a in_review

---

### AL TERMINAR (verificar ANTES de reportar)

- [ ] PR creado hacia main
- [ ] [ENTREGABLE_1]
- [ ] [ENTREGABLE_2]
- [ ] Development Log creado en `/devlogs/`
- [ ] Code Logic creado/actualizado para CADA archivo de codigo
- [ ] Swagger docs (si hay endpoints)
- [ ] Estado cambiado a in_review

### REPORTE DE ENTREGA (OBLIGATORIO)

Al completar la tarea, genera un comentario con tu reporte de entrega para que el PM lo pegue en la tarea. Formato:

```
Reporte de Entrega [ID_TAREA]: [TITULO]

**Codigo:**
| # | Archivo | Estado |
|---|---------|--------|
| 1 | [archivo_1] | Creado/Modificado |
| 2 | [archivo_2] | Creado/Modificado |

**Development Log:**
- `devlogs/YYYY-MM-DD_[ID_TAREA]_[desc].md`

**Code Logic:**
- `knowledge/code-logic/[espejo]/[archivo_1].LOGIC.md`
- `knowledge/code-logic/[espejo]/[archivo_2].LOGIC.md`

**Resumen de cambios:**
- [Descripcion de lo que se hizo]

**Branch:** feature/[ID_TAREA]-[nombre-corto]
**PR:** #[numero]
**Archivos modificados:** [N] archivos

**Como probar:**
[Pasos para validar que funciona]
```

Este reporte se agrega como comentario en la tarea del sistema para que quede registro de que se entrego y que contiene.
```

---

## VARIABLES A REEMPLAZAR

| Variable | Descripcion | Ejemplo |
|----------|-------------|---------|
| `[ROL_AGENTE]` | Rol del agente | Frontend Dev #1, Backend API Specialist, Design Lead |
| `[NOMBRE_AGENTE]` | Nombre corto | Frontend Dev, Backend Dev, Design Lead |
| `[ID_TAREA]` | Codigo de tarea | VTT-070 |
| `[TITULO]` | Titulo de la tarea | Filtro de Proyecto en Vista de Tareas |
| `[USER_ID_AGENTE]` | UUID del agente en la BD | `84ad0fbe-996d-4aa7-abf6-57d64d4671de` |

## USER IDs POR ROL

| Rol | userId |
|-----|--------|
| Backend API Specialist | `8834830b-578f-46be-933b-0abcbbc5da99` |
| Frontend Dev #1 | `84ad0fbe-996d-4aa7-abf6-57d64d4671de` |
| Frontend Dev #2 | `9b8d927e-0013-4291-850d-bff968b37c84` |
| Design Lead | `ebf0f384-51ba-49f5-8e98-fa7569ce1d31` |
| Database Engineer | `a3a2ce62-28d8-419d-9888-44203a963894` |
| DevOps Engineer | `b2e00b9d-a657-4bdb-b982-3dcf1f5b5757` |
| Tech Lead | `abdff0db-ad0b-4a0c-99f5-c898d18bd2d8` |
| Martin Rivas (PM) | `07a07147-cf5a-4117-8fbd-2fd1ccb95d54` |

## STATUS IDs

| Status | statusId |
|--------|----------|
| in_progress | `2a76888a-e595-4cfc-ac4c-a3ae5087ef56` |
| in_review | `1ec975a5-7581-4a1a-ab8f-51b1a7ef868d` |
| completed | `aa5ceb90-5209-42a2-b874-a8cbee597a97` |
| pending | `335fd9c6-f0d6-4966-a6ea-f518c78bc422` |
| on_hold | `c62eb334-b7bc-4c9f-af85-a5666c262aaa` |
