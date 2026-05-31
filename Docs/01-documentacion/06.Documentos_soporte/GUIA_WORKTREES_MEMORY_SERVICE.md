# Guía Worktrees Memory Service — Single Manual Control Surface

**Versión:** 2.2
**Fecha:** 2026-05-14
**Aplicable a:** **TODOS los roles** del proyecto (BE, DO, DB, QA, TL, PM, SA, AR, UX, DL, FE, SEC...)
**Cubre los 4 repos:** memory-service-backend, memory-service-project, memory-service-api, memory-service-frontend
**Reemplaza:** v1.0 (`GUIA_GIT_WORKTREES_TL_BACKEND.md` — nombre confuso, worktree por tarea)
**Origen:** `estrategia_worktrees_runtime_vtt_agentes.md` (Capa A — operación manual)

> **Reglas de ubicación de documentos:** ver
> `00-agent-setup/06.Documentos_soporte/REGLAS_UBICACION_DOCUMENTOS.md` v1.0
> Define qué documento vive en qué repo y quién escribe dónde.

---

## Decisión central

> Cada **rol** tiene un worktree fijo. La **tarea** define solo la branch dentro de ese worktree.
>
> Una ventana VSCode por rol. Una sola sesión de chat Claude Code por ventana.

Por qué: el incidente PROC-COORD-01 (MS-286) ocurrió porque 3 agentes compartían el mismo working tree. Cuando uno hacía `git checkout feature/MS-Y`, el otro perdía sus archivos. Con worktrees por rol cada agente tiene **directorio físico distinto** → imposibilidad técnica de pisarse.

---

## Estructura local

```
c:/Users/Martin/Documents/virtual-teams/memory-service/
│
├── memory-service-backend/             ← clon base (NO trabajar aquí)
├── memory-service-project/             ← clon base
├── memory-service-api/                 ← clon base
├── memory-service-frontend/            ← clon base
│
├── .vtt/                               ← infraestructura interna
│   ├── worktrees/                      ← UN worktree por rol activo
│   │   ├── backend-be/                 ← Backend Engineer trabaja AQUÍ
│   │   ├── backend-do/                 ← DevOps trabaja AQUÍ
│   │   ├── backend-db/                 ← DB Engineer
│   │   ├── backend-qa/                 ← QA Engineer
│   │   ├── project-tl/                 ← Tech Lead (review + coordinación)
│   │   ├── project-pm/                 ← Product Manager
│   │   └── project-sa/                 ← Systems Analyst
│   │
│   ├── workspaces/                     ← UN .code-workspace por rol
│   │   ├── backend-be.code-workspace   ← doble click → abre ventana VSCode del BE
│   │   ├── backend-do.code-workspace
│   │   ├── backend-db.code-workspace
│   │   ├── backend-qa.code-workspace
│   │   ├── project-tl.code-workspace
│   │   ├── project-pm.code-workspace
│   │   ├── project-sa.code-workspace
│   │   └── legacy/                     ← workspaces viejos (apuntaban a clon base)
│   │
│   ├── manifests/                      ← execution_manifest por tarea
│   │   ├── _template.execution.json
│   │   └── MS-XXX.execution.json
│   │
│   ├── reports/                        ← outputs operacionales (futuro Hook Manager)
│   ├── diffs/                          ← .patch files (futuro)
│   ├── agent-runs/                     ← logs (futuro)
│   ├── locks/                          ← file locks (futuro)
│   ├── memory/                         ← (preexistente)
│   ├── skills/                         ← (preexistente)
│   ├── manifest.yaml                   ← (preexistente)
│   └── teams.md                        ← (preexistente)
│
└── (carpetas pre-existentes intactas: 00-agent-setup/, Release2.0/, etc.)
```

---

## Reglas operativas (Capa A — manual)

### Regla 1 — Worktree FIJO por rol

Cada rol activo tiene **un solo worktree** que dura todo el proyecto. NO se crea uno por tarea.

| Rol | Worktree path | Repo principal | Branch idle |
|---|---|---|---|
| BE (Backend Engineer) | `.vtt/worktrees/backend-be/` | backend | `wt-backend-be` |
| DO (DevOps) | `.vtt/worktrees/backend-do/` | backend | `wt-backend-do` |
| DB (Database Engineer) | `.vtt/worktrees/backend-db/` | backend | `wt-backend-db` |
| QA (QA Engineer) | `.vtt/worktrees/backend-qa/` | backend | `wt-backend-qa` |
| TL (Tech Lead) | `.vtt/worktrees/project-tl/` | project | `wt-project-tl` |
| PM (Product Manager) | `.vtt/worktrees/project-pm/` | project | `wt-project-pm` |
| SA (Systems Analyst) | `.vtt/worktrees/project-sa/` | project | `wt-project-sa` |

**Cuándo se crea un worktree nuevo:** solo cuando un rol nuevo entra al proyecto (ej. SEC al llegar a Fase 3B.7 Security Plan, o FE al llegar a Fase 4.4 Frontend).

### Regla 2 — Una ventana VSCode por rol

```
backend-be.code-workspace   →  doble click  →  ventana "BE - Backend Engineer"
backend-do.code-workspace   →  doble click  →  ventana "DO - DevOps"
project-tl.code-workspace   →  doble click  →  ventana "TL - Tech Lead"
```

Cada ventana tiene:
- 1 folder (el worktree del rol)
- Título descriptivo en la barra de Windows
- 1 chat Claude Code adentro

`Alt+Tab` entre ventanas para cambiar de agente.

### Regla 3 — La branch sigue a la tarea, no al worktree

```
Tarea MS-293 al BE:
  cd .vtt/worktrees/backend-be/
  git checkout -b feature/MS-293 origin/main
  # trabajar, commit, push, PR

Tarea MS-310 al BE (después de cerrar MS-293):
  cd .vtt/worktrees/backend-be/    ← MISMO directorio
  git checkout main && git pull
  git checkout -b feature/MS-310 origin/main
  # trabajar...
```

El worktree del BE pasa por N branches a lo largo del proyecto. Pero el directorio físico es siempre el mismo.

### Regla 4 — Cada agente trabaja SOLO en su worktree

- NO hacer `cd` a otro worktree
- NO hacer `git checkout` en el clon base (`memory-service-backend/`, etc.)
- NO clonar de nuevo
- Trabajar siempre en `.vtt/worktrees/<repo>-<rol>/`

### Regla 5 — Execution manifest por tarea (TL lo crea)

Al asignar una tarea, el TL crea `.vtt/manifests/MS-XXX.execution.json` desde el template. Define:

- `agents[]` — quién trabaja la tarea, en qué repo, en qué branch
- `allowedPaths` — qué archivos puede tocar cada agente
- `deniedPaths` — qué archivos prohibidos (.env, secrets)
- `expectedOutputs` — qué entregables produce

El agente lee este manifest al arrancar la tarea (paso 0 de su workflow).

### Regla 6 — Integración solo por TL

- Agentes implementan → commit + push + crear PR
- NO mergear a `main` directamente
- TL revisa diffs + APR-TL comment + merge

### Regla 7 — Cada rol escribe en SU repo destino (no cruzar) — **NUEVA v2.2**

Cada worktree tiene un **repo destino fijo**:

| Worktree | Repo destino |
|---|---|
| `backend-be`, `backend-do`, `backend-db`, `backend-qa` | `memory-service-backend` |
| `api-be`, `api-qa` (cuando se creen) | `memory-service-api` |
| `frontend-fe`, `frontend-dl` (cuando se creen) | `memory-service-frontend` |
| `project-tl`, `project-pm`, `project-sa`, `project-ar`, `project-dl`, `project-ux`, `project-pjm`, `project-sec` | `memory-service-project` |

**Todo** lo que el agente produce (código + tests + code_logic + devlog) se commitea en **1 PR a SU repo destino**. NO mezclar repos.

`virtual-teams-setup` es **solo lectura** durante ejecución de tareas.

Ver `REGLAS_UBICACION_DOCUMENTOS.md` para la tabla maestra completa por artefacto y casos especiales.

---

## Operación: día a día

### Setup inicial (1 vez al proyecto)

Ya está hecho. Los 7 worktrees + 7 workspaces existen en `.vtt/`.

### Apertura de sesión (tú, cada mañana)

1. Doble click en los `.code-workspace` de los roles que vas a usar hoy
2. Cada uno abre una ventana VSCode con título identificable
3. Dentro de cada ventana: abrir chat Claude Code, se queda fijo todo el día
4. Pegar tareas a cada chat conforme las asignes

### Asignar tarea (TL)

1. Generar BRIEF + ASSIGNMENT en VTT (procesos existentes)
2. Crear execution_manifest: `cp .vtt/manifests/_template.execution.json .vtt/manifests/MS-XXX.execution.json` y editar
3. Generar mensaje: `python scripts/gen_mensaje.py MS-XXX --post`
4. El mensaje incluye automáticamente:
   - cwd del agente (`.vtt/worktrees/<repo>-<rol>/`)
   - Comando para crear branch de la tarea
   - Workspace VSCode a usar
   - Puerto npm asignado

### Agente arranca tarea (paso 0)

```bash
cd c:/Users/Martin/Documents/virtual-teams/memory-service/.vtt/worktrees/backend-be
git status                                  # debe estar limpio
git fetch origin
git checkout main && git pull origin main
git checkout -b feature/MS-XXX origin/main
```

A partir de aquí, el agente trabaja normal (workflow de 15 pasos del template).

### Cierre de tarea

1. Agente: commit + push + PR + status `task_in_review`
2. TL Reviewer: code review (FASE A + B + C), aprueba
3. Después del merge en GitHub, el TL hace cleanup local del worktree:
   ```bash
   cd .vtt/worktrees/backend-be
   git checkout main && git pull origin main
   git branch -d feature/MS-XXX        # borra branch local mergeada
   ```

El worktree queda listo para la siguiente tarea.

---

## Crear worktrees adicionales (cuando llegue un rol nuevo)

Cuando entra un rol que no tiene worktree (ej. FE al arrancar Fase 4.4):

```bash
cd c:/Users/Martin/Documents/virtual-teams/memory-service/memory-service-frontend
git fetch origin
git worktree add ../.vtt/worktrees/frontend-fe -b wt-frontend-fe origin/main
```

Y crear su workspace VSCode:

```bash
cat > .vtt/workspaces/frontend-fe.code-workspace << 'EOF'
{
  "folders": [
    { "name": "FE Frontend Engineer", "path": "../worktrees/frontend-fe" }
  ],
  "settings": {
    "window.title": "FE - Frontend Engineer | Memory Service",
    "terminal.integrated.cwd": "${workspaceFolder}"
  }
}
EOF
```

---

## Casos especiales

### Tarea toca múltiples repos (BE + project para docs)

Hoy: el agente trabaja primero en su worktree principal. Si necesita tocar otro repo (ej. devlog en `project`), aplica **Regla 7**: el devlog del BE va en `backend-be/knowledge/development-log/` y se commitea a `memory-service-backend`, NO a project.

Si el cambio realmente requiere tocar el repo project (ej. spec técnica de fase), el TL crea una **sub-tarea** para sí mismo o coordina el cambio.

### Tarea en branch base que NO es main

Si MS-310 depende de MS-309 que no está en main todavía:
```bash
cd .vtt/worktrees/backend-be
git fetch origin
git checkout -b feature/MS-310 origin/feature/MS-309
```

### Worktree con cambios sin commitear al cambiar de tarea

```bash
cd .vtt/worktrees/backend-be
git status   # muestra cambios

# Opción 1: commit WIP
git add -A && git commit -m "WIP: pause MS-XXX" && git push

# Opción 2: stash
git stash push -m "MS-XXX-pause"

# Luego puedes cambiar de branch sin perder nada
```

### El worktree quedó corrupto

```bash
cd memory-service-backend
git worktree remove --force ../.vtt/worktrees/backend-be
git worktree add ../.vtt/worktrees/backend-be -b wt-backend-be origin/main
```

---

## Lecciones aprendidas

### LL-WT-01 — El TL Reviewer también debe respetar su propio worktree (2026-05-14)

**Qué pasó:**
Durante la implementación de REGLAS_UBICACION_DOCUMENTOS v1.0, el TL Reviewer (Claude) trabajó inicialmente desde el clon base `memory-service-project/` en vez de su worktree `.vtt/worktrees/project-tl/`. Resultado:

1. Los cambios quedaron en el clon base, no en el worktree
2. Al hacer `git status` en el clon base se vieron cambios mezclados con trabajo del PM (archivos eliminados durante migración a vtt-setup)
3. Hubo que **copiar manualmente** los cambios desde el clon base al worktree TL
4. Hubo que hacer `git checkout --` archivo por archivo en el clon base para revertir sin pisar el trabajo del PM
5. El commit + PR finalmente se hizo desde el worktree TL (como debió ser desde el inicio)

**Por qué pasó:**
El TL operativo (chat de Claude) no validó al iniciar la sesión en qué cwd estaba. Saltó directo a editar archivos asumiendo que estaba en el lugar correcto.

**Cómo evitarlo:**

1. **Validación obligatoria al inicio de cada sesión del TL** (debe estar en el OPERATIVO_TL):
   ```bash
   pwd   # debe contener ".vtt/worktrees/project-tl"
   git branch --show-current   # debe ser wt-project-tl o branch chore/feature derivada
   ```

2. **Si pwd no es el worktree del TL:**
   ```bash
   cd c:/Users/Martin/Documents/virtual-teams/memory-service/.vtt/worktrees/project-tl
   ```

3. **NUNCA editar archivos en `memory-service-project/` directamente.**
   El clon base puede tener trabajo en progreso de otros (migraciones, eliminaciones, etc.).

4. **NUNCA `git checkout .` ciego en un clon base.**
   Solo restaurar archivos específicos con `git checkout -- <archivo>` si confirmas que son tuyos.

**Aplicabilidad:**
Esta lección aplica a TODOS los roles, no solo al TL. Cualquier agente que se descuide y termine en el clon base puede causar el mismo problema. Por eso la Regla 4 dice "NUNCA hacer `git checkout` en clones base".

**Evidencia:**
PR #64 (`chore/REGLAS-UBICACION-worktrees-v2`) y commits en branch del mismo nombre. El historial muestra que los archivos se commitearon desde el worktree TL, no desde el clon base.

---

## Lo que NO hace este enfoque (limitaciones honestas)

- **No previene** que dos agentes modifiquen el mismo `package.json` en sus respectivos worktrees → conflicto al merge. TL resuelve manualmente.
- **No previene** que un agente haga `cd` a otro worktree (técnicamente puede). Mitigación: prompt explícito "trabaja solo en tu cwd".
- **No tiene locks de archivos** (Capa B con Hook Manager los implementará).
- **No tiene logs centralizados** (Capa B los capturará en `.vtt/agent-runs/`).

---

## Mapeo con la estrategia futura (Capa B — Hook Manager)

Esta estructura es 100% compatible con el plan futuro del doc `estrategia_worktrees_runtime_vtt_agentes.md`:

| Hoy (Capa A — manual) | Futuro (Capa B — Hook Manager) |
|---|---|
| TL crea worktrees con `git worktree add` | Runtime los crea automáticamente |
| TL escribe execution_manifest manual | Runtime lo genera al asignar tarea |
| Agente lee mensaje con cwd y allowedPaths | Hook Manager sandboxea el cwd y enforza allowedPaths |
| Agente postea en VTT con curl manual | Runtime captura outputs automáticamente |
| TL revisa diffs leyendo PRs en GitHub | Runtime presenta diffs en UI VTT |

Cuando el Hook Manager esté listo, **migrar es trivial** porque la convención de paths, naming y manifest ya está alineada con el target.

---

## Cleanup de worktrees al final del proyecto

```bash
# Cerrar worktrees uno por uno
cd memory-service-backend
git worktree remove ../.vtt/worktrees/backend-be
git worktree remove ../.vtt/worktrees/backend-do
git worktree remove ../.vtt/worktrees/backend-db
git worktree remove ../.vtt/worktrees/backend-qa

cd ../memory-service-project
git worktree remove ../.vtt/worktrees/project-tl
git worktree remove ../.vtt/worktrees/project-pm
git worktree remove ../.vtt/worktrees/project-sa

# Borrar branches idle
cd ../memory-service-backend && git branch -D wt-backend-be wt-backend-do wt-backend-db wt-backend-qa
cd ../memory-service-project && git branch -D wt-project-tl wt-project-pm wt-project-sa
```

---

## Checklist de adopción (estado actual)

```
[x] Estructura .vtt/worktrees/ creada
[x] 7 worktrees iniciales creados (BE, DO, DB, QA, TL, PM, SA)
[x] 7 .code-workspace generados en .vtt/workspaces/
[x] Workspaces viejos archivados en .vtt/workspaces/legacy/
[x] _template.execution.json en .vtt/manifests/
[x] gen_mensaje.py actualizado para inyectar cwd por rol
[x] REGLAS_UBICACION_DOCUMENTOS v1.0 creado (Regla 7 → repo destino por rol)
[x] OPERATIVOs de 12 roles actualizados con §Working Directory + Repo destino
[ ] PR de los cambios (pendiente — siguiente paso)
[ ] Primera tarea asignada bajo este modelo (validación end-to-end)
[ ] Cerrar TI PROC-COORD-01 con [RESOLVED] una vez se valide la primera tarea
```

---

## Documentos relacionados

| Doc | Para qué |
|---|---|
| `REGLAS_UBICACION_DOCUMENTOS.md` (v1.0) | **Tabla maestra: qué documento vive en qué repo, quién escribe dónde** |
| `estrategia_worktrees_runtime_vtt_agentes.md` | Estrategia conceptual (Capa A + B) |
| `_template.execution.json` | Plantilla manifest por tarea |
| `gen_mensaje.py` | Genera mensaje al agente con cwd inyectado |
| `GUIA_ASIGNACION_TAREA_TL_EJECUTOR.md` | Guía operativa del TL al asignar |
| `GUIA_REVISION_TAREA_TL_REVIEWER.md` | Guía operativa del TL al revisar |
| `OPERATIVO_<rol>_MEMORY-SERVICE.md` | Operativo de cada rol (§Working Directory + Repo destino) |
| `PROC-COORD-01` (TI VTT) | Incidente origen — se cierra cuando esto esté validado |

---

## Changelog

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-05-14 | Versión inicial (worktree por tarea — enfoque incorrecto). Archivo se llamaba `GUIA_GIT_WORKTREES_TL_BACKEND.md`. |
| 2.0 | 2026-05-14 | Worktrees por rol (no por tarea). Single Manual Control Surface. |
| 2.1 | 2026-05-14 | Rename a `GUIA_WORKTREES_MEMORY_SERVICE.md`. Header indica TODOS los roles, 4 repos. |
| **2.2** | **2026-05-14** | **Regla 7 NUEVA: cada rol escribe en SU repo destino. Referencia a `REGLAS_UBICACION_DOCUMENTOS.md` v1.0. virtual-teams-setup solo lectura.** |
