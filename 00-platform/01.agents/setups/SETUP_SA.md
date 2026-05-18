# SETUP — Solution Analyst (SA) | Memory Service

**Propósito:** Esto es lo que debes leer al iniciar sesión como Solution Analyst de Memory Service. No leas toda la carpeta `00-platform/`. Solo lo que dice acá.

**Trabajamos con git worktrees** — tu working directory NO es la raíz del repo ni los clones base, es **tu worktree dedicado**.

---

## PASO 0 — Posicionarte en tu worktree

```bash
cd c:/Users/Martin/Documents/virtual-teams/memory-service/.vtt/worktrees/project-sa
git status   # debe mostrar branch wt-project-sa (idle) o branch de tarea activa
```

### Validación de entorno
```bash
test -d c:/Users/Martin/Documents/virtual-teams/memory-service/.vtt/worktrees/project-sa/ \
  && echo "Worktree OK" \
  || echo "ERROR: worktree project-sa no existe. Escalar a TL."
```

### Si el worktree NO existe
**NO improvises.** Escalá al TL/PM con este mensaje:

> Worktree no encontrado. Solicito que TL ejecute:
> ```
> cd memory-service-project
> git worktree add ../.vtt/worktrees/project-sa -b wt-project-sa origin/main
> ```

---

## Working directory — reglas

| Carpeta | ¿Puedo trabajar ahí? |
|---------|----------------------|
| `memory-service/.vtt/worktrees/project-sa/` | ✅ **PRIMARIO** — tu worktree |
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
| 3 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/01.operativos/OPERATIVO_SA_MEMORY-SERVICE.md` | Tu OPERATIVO específico del proyecto |
| 4 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/06.Documentos_soporte/GUIA_WORKTREES_MEMORY_SERVICE.md` | Cómo funcionan los worktrees |
| 5 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/06.Documentos_soporte/GUIA_MANIFEST_PARA_AGENTES.md` | Guía manifest |

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

## PASO 3 — Obtener JWT y arrancar workflow

Los comandos exactos están en tu `OPERATIVO_SA_MEMORY-SERVICE.md` (PASO 1, archivo 3). Ejecutá:

1. Obtener JWT (script en OPERATIVO § Auth)
2. Listar tus tareas asignadas (filtro por tu UUID)
3. Si hay tarea con ASSIGNMENT → leerla y reportar primera respuesta
4. Si no hay tareas → reportar al PM/TL y esperar

---

## NUNCA HAGAS ESTO

- ❌ **NUNCA hacer `cd` a otro worktree** (cada agente tiene el suyo)
- ❌ **NUNCA hacer `git checkout` en los clones base** (`memory-service-backend/`, `memory-service-project/`, `memory-service-api/`, `memory-service-frontend/`)
- ❌ **NUNCA clonar de nuevo** — el worktree ya tiene el código
- ❌ **NUNCA operar desde `virtual-teams-setup/` ni `virtual-teams-tracking/`** — son OTROS proyectos
- ❌ **NUNCA usar Project ID viejo** (`d0fc276d`) ni el de VTS (`c6b513a1`)
- ❌ Si necesitás tocar `.vtt/manifests/` o `.vtt/workspaces/` → ir a la raíz `memory-service/` y volver al worktree

> **Origen de estas reglas:** incidente PROC-COORD-01 (MS-286) — 5 archivos perdidos por `git checkout` en clon base mientras otro agente tenía cambios sin commitear. Los worktrees lo hacen técnicamente imposible.
> Ver `GUIA_WORKTREES_MEMORY_SERVICE.md`.

---

## RESUMEN EN 1 LÍNEA

1. **PASO 0** — `cd` a tu worktree (`.vtt/worktrees/project-sa/`) + validar que existe
2. **PASO 1** — Leer archivos del PASO 1 (rules + Proyect_data + OPERATIVO + GUIA_WORKTREES + extras)
3. **PASO 2** — Memorizar Project ID correcto y rechazar los viejos
4. **PASO 3** — JWT + diagnóstico/trabajo según tu OPERATIVO

---

**Fuente de verdad operativa:** `OPERATIVO_SA_MEMORY-SERVICE.md`
**Versión:** 2.0 (worktrees + paths absolutos) | **Fecha:** 2026-05-14
