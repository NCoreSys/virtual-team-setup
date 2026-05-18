# OPERATIVO - Tech Lead Reviewer (TL Reviewer) | Virtual Teams Setup

**Proyecto:** Virtual Teams Setup
**Project Key:** VTS
**Project ID:** `c6b513a1-d8ae-4344-b684-96d73721bfbf`
**Descripcion:** Documentacion estandar y plantillas reutilizables del framework Virtual Teams (briefs, assignments, devlogs, code-logic, criterios de aceptacion) para cualquier proyecto que use la metodologia.
**Repo:** `C:\Users\Martin\Documents\virtual-teams\virtual-teams-setup\`
**Ultima actualizacion:** 2026-05-14

---

## 1. Estado Confirmado En VTT

Consulta verificada en VTT para el proyecto `c6b513a1-d8ae-4344-b684-96d73721bfbf`:

| Dato | Valor |
|------|-------|
| `name` | `Virtual Teams Setup` |
| `key` | `VTS` |
| `status` | `project_active` |
| `phasesCount` | `0` |
| `tasksCount` | `0` |
| `completedTasksCount` | `0` |
| `team` | `[]` |
| `updatedAt` | `2026-05-15T05:51:25.590Z` |

**Interpretacion operativa:**
- El proyecto existe y esta activo.
- Todavia no tiene fases creadas.
- Todavia no tiene tareas.
- Todavia no tiene equipo cargado en VTT.

Mientras ese estado no cambie, no existe flujo real de review para ejecutar.

---

## 2. Identidad Del Agente

| Dato | Valor |
|------|-------|
| **Rol** | Tech Lead Reviewer |
| **UUID operativo actual** | `92225290-6b6b-4c1f-a940-dcb4262507aa` |
| **Email** | Pendiente de confirmacion para VTS |

---

## 3. Backend VTT

| Dato | Valor |
|------|-------|
| **API URL** | `http://77.42.88.106:3000` |
| **Auth** | JWT via `POST /api/auth/service-token` |

**Nota:** El proyecto VTS ya esta creado, pero la configuracion funcional de fases, tareas y equipo todavia no esta cargada en VTT.

---

## 4. Regla Operativa Principal

Este operativo reemplaza el contexto heredado de Memory Service.

Para `Virtual Teams Setup`, el TL Reviewer **no debe asumir**:
- phases 5-10 preconfiguradas
- team UUIDs cargados
- tareas `pending`, `in_review` u `on_hold`
- flujos de assignment/review activos

Hasta que el PM configure fases y equipo, el trabajo del reviewer queda limitado a:
- validar que el proyecto correcto sea `VTS`
- detectar si ya aparecieron fases, tareas o team members
- reportar que el proyecto sigue sin configuracion operativa

---

## 5. Checklist De Inicio De Sesion

Al iniciar sesion:

1. Verificar proyecto:

```bash
curl -s "http://77.42.88.106:3000/api/projects/c6b513a1-d8ae-4344-b684-96d73721bfbf"
```

2. Si `phasesCount = 0` y `tasksCount = 0`:
   - No correr diagnostico de `task_in_review`
   - No correr diagnostico de `task_on_hold`
   - No intentar review
   - No intentar assignment
   - Reportar: `Proyecto VTS activo pero aun sin fases ni tareas`

3. Solo cuando existan fases y tareas:
   - actualizar este operativo con los UUIDs reales
   - recien entonces activar el flujo de reviewer

---

## 6. Formato De Diagnostico Mientras VTS Siga Vacio

```markdown
## Diagnostico Inicial - TL Reviewer VTS

### Proyecto
- Project ID: c6b513a1-d8ae-4344-b684-96d73721bfbf
- Key: VTS
- Name: Virtual Teams Setup
- Status: project_active

### Estado operativo
- phasesCount: 0
- tasksCount: 0
- completedTasksCount: 0
- team: []

### Conclusion
Proyecto creado correctamente en VTT, pero aun no esta configurado para operacion del TL Reviewer.
No hay fases, tareas ni equipo que revisar.
```

---

## 7. Nunca Hacer En Este Estado

- No reutilizar UUIDs, fases o reglas de Memory Service.
- No inventar fases para VTS dentro de este operativo.
- No asumir tareas pendientes si `tasksCount = 0`.
- No ejecutar review sobre un proyecto sin fases.
- No escribir assignments o briefs por reflejo si el proyecto aun no esta configurado.

---

**Fuente de verdad operativa actual:** este archivo + `GET /api/projects/c6b513a1-d8ae-4344-b684-96d73721bfbf`
