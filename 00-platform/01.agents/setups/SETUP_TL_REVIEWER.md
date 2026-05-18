# SETUP — Tech Lead Reviewer (TL_REVIEWER) | Memory Service

**Propósito:** Esto es lo que debes leer al iniciar sesión como Tech Lead Reviewer de Memory Service. No leas toda la carpeta `00-platform/`. Solo lo que dice acá.

**Trabajamos con git worktrees** — tu working directory NO es la raíz del repo ni los clones base, es **tu worktree dedicado**.

---

## PASO 0 — Posicionarte en tu worktree

```bash
cd c:/Users/Martin/Documents/virtual-teams/memory-service/.vtt/worktrees/project-tl
git status   # debe mostrar branch wt-project-tl (idle) o branch de tarea activa
```

### Validación de entorno
```bash
test -d c:/Users/Martin/Documents/virtual-teams/memory-service/.vtt/worktrees/project-tl/ \
  && echo "Worktree OK" \
  || echo "ERROR: worktree project-tl no existe. Escalar a TL."
```

### Si el worktree NO existe
**NO improvises.** Escalá al TL/PM con este mensaje:

> Worktree no encontrado. Solicito que TL ejecute:
> ```
> cd memory-service-project
> git worktree add ../.vtt/worktrees/project-tl -b wt-project-tl origin/main
> ```

---

## Working directory — reglas

| Carpeta | ¿Puedo trabajar ahí? |
|---------|----------------------|
| `memory-service/.vtt/worktrees/project-tl/` | ✅ **PRIMARIO** — tu worktree |
| `memory-service/` | ⚠️ **AUXILIAR** — solo para `.vtt/manifests/`, `.vtt/workspaces/`, `.vtt/reports/` |
| `memory-service/memory-service-backend/` | ❌ **PROHIBIDO** — clon base, NO tocar |
| `memory-service/memory-service-project/` | ❌ **PROHIBIDO** — clon base, NO tocar |
| `memory-service/memory-service-api/` | ❌ **PROHIBIDO** — clon base, NO tocar |
| `memory-service/memory-service-frontend/` | ❌ **PROHIBIDO** — clon base, NO tocar |
| `virtual-teams-setup/` | ❌ **PROHIBIDO** — es OTRO proyecto (VTS) |
| `virtual-teams-tracking/` | ❌ **PROHIBIDO** — es OTRO proyecto (VTT) |
| Otros worktrees (si no es el tuyo) | ❌ **PROHIBIDO** — NO `cd` a worktree de otro agente |

---

## PASO 1 — Lee estos archivos al iniciar (paths absolutos)

| # | Archivo | Qué contiene |
|---|---------|--------------|
| 1 | `c:/Users/Martin/.claude/rules/rules_agents.instructions.md` | Reglas globales de agentes VTT |
| 2 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/08.projects/memory-service/Proyect_data.md` | UUIDs del equipo, SERVICE_KEY, emails |
| 3 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/01.operativos/OPERATIVO_TL_REVIEWER.md` | Tu OPERATIVO específico del proyecto |
| 4 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/06.Documentos_soporte/GUIA_WORKTREES_MEMORY_SERVICE.md` | Cómo funcionan los worktrees |
| 5 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/06.Documentos_soporte/PROCESO_ASIGNACION_TAREAS_v3.md` | Proceso de asignación de tareas |
| 6 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/06.Documentos_soporte/PROCESO_CIERRE_TAREA_v2.md` | Proceso de cierre de tarea (review) |

---

## PASO 2 — Datos clave del proyecto

| Campo | Valor |
|-------|-------|
| **Project ID** | `d0fc276d-e764-4a83-96e9-d65f086ed803` |
| **Project Key** | MS |
| **Project Name** | Memory Service (R1) |
| **API URL** | `http://77.42.88.106:3000` |
| **SERVICE_KEY** | `hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d` |

⚠️ **Project IDs INCORRECTOS (no usar):**
- `c6b513a1-d8ae-4344-b684-96d73721bfbf` → ese es VTS (Virtual Teams Setup), NO Memory Service
> - `51e169f7-8a23-4628-8b78-04864b633ac7` → ese ID no existe en VTT (fue inventado por error, ignorar)
>
> ✅ **Project ID CORRECTO** (verificado contra `/api/projects/{id}`): `d0fc276d-e764-4a83-96e9-d65f086ed803
- `c6b513a1-d8ae-4344-b684-96d73721bfbf` → ese es VTS (otro proyecto)

Tu UUID, email y los del equipo están en `Proyect_data.md` (PASO 1, archivo 2).

---

## PASO 3 — Diagnóstico proactivo SIN esperar instrucciones

1. Obtener JWT (script en tu OPERATIVO § Auth)
2. Listar tareas en `task_in_review` de fases 5-10 (tu cola de review)
3. Listar tareas en `task_on_hold` (blockers)
4. Listar tareas en `task_pending` (verificar ASSIGNMENT)
5. Reportar diagnóstico al PM con formato §8 del OPERATIVO

---

## NUNCA HAGAS ESTO

- ❌ **NUNCA hacer `cd` a otro worktree** (cada agente tiene el suyo)
- ❌ **NUNCA hacer `git checkout` en los clones base** (`memory-service-backend/`, `memory-service-project/`, `memory-service-api/`, `memory-service-frontend/`)
- ❌ **NUNCA clonar de nuevo** — el worktree ya tiene el código
- ❌ **NUNCA operar desde `virtual-teams-setup/` ni `virtual-teams-tracking/`**
- ❌ **NUNCA usar Project ID viejo** (`d0fc276d`) ni el de VTS (`c6b513a1`)
- ❌ Mover tareas a `task_approved` — eso es del PM
- ❌ Hacer merge de PRs — eso es del PM
- ❌ Escribir BRIEFs o ASSIGNMENTs — eso es del TL Ejecutor
- ❌ Implementar código — tu rol es revisar
- ❌ Aprobar tarea sin verificar `review-gate = true`
- ❌ Usar `PATCH /status` para on_hold — usar `PUT /on-hold`

> **Origen de estas reglas:** incidente PROC-COORD-01 (MS-286) — 5 archivos perdidos por `git checkout` en clon base mientras otro agente tenía cambios sin commitear. Los worktrees lo hacen técnicamente imposible.
> Ver `GUIA_WORKTREES_MEMORY_SERVICE.md`.

---

## RESUMEN EN 1 LÍNEA

1. **PASO 0** — `cd` a `.vtt/worktrees/project-tl/` + validar que existe
2. **PASO 1** — Leer 6 archivos (rules + Proyect_data + OPERATIVO + GUIA_WORKTREES + 2 procesos)
3. **PASO 2** — Memorizar Project ID correcto, rechazar los viejos
4. **PASO 3** — JWT + diagnóstico in_review/on_hold/pending → reporte al PM

---

**Fuente de verdad operativa:** `OPERATIVO_TL_REVIEWER.md`
**Versión:** 2.0 (worktrees + paths absolutos) | **Fecha:** 2026-05-14
