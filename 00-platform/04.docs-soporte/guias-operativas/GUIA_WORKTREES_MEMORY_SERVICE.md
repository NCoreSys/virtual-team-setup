# Guía Worktrees Memory Service — Single Manual Control Surface

**Versión:** 2.1
**Fecha:** 2026-05-14
**Aplicable a:** **TODOS los roles** del proyecto (BE, DO, DB, QA, TL, PM, SA, AR, UX, DL, FE, SEC...)
**Cubre los 4 repos:** memory-service-backend, memory-service-project, memory-service-api, memory-service-frontend
**Reemplaza:** v1.0 (`GUIA_GIT_WORKTREES_TL_BACKEND.md` — nombre confuso, worktree por tarea)
**Origen:** `estrategia_worktrees_runtime_vtt_agentes.md` (Capa A — operación manual)

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
│   │   ├── project-tl/                 ← Tech Lead (review)
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
│   ├── reports/                        ← outputs de agentes
│   │   └── MS-XXX_<AGENT>_report.md
│   │
│   ├── diffs/                          ← .patch files por (tarea, agente)
│   │   └── MS-XXX_<repo>_<agent>.patch
│   │
│   ├── agent-runs/                     ← logs (Hook Manager futuro)
│   ├── locks/                          ← file locks (futuro)
│   ├── memory/                         ← (preexistente)
│   ├── skills/                         ← (preexistente)
│   ├── manifest.yaml                   ← (preexistente)
│   └── teams.md                        ← (preexistente)
│
└── (carpetas pre-existentes intactas: 00-platform/, Release2.0/, etc.)
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

Hoy: el agente trabaja primero en su worktree principal. Si necesita tocar otro repo (ej. devlog en `project`), el TL le pasa el path del worktree del TL como working dir para la parte de docs, o el agente edita los devlogs en su worktree de backend si están duplicados.

Mejor opción: que TL cree un worktree adicional bajo demanda si es necesario:
```bash
cd memory-service-project
git worktree add ../.vtt/worktrees/project-be-aux -b wt-project-be-aux origin/main
```

Capa B (Hook Manager) automatizará esto.

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
[x] GUIA_GIT_WORKTREES (este doc) reescrita con enfoque correcto
[ ] PR de los cambios (pendiente — siguiente paso)
[ ] Primera tarea asignada bajo este modelo (validación end-to-end)
[ ] Cerrar TI PROC-COORD-01 con [RESOLVED] una vez se valide la primera tarea
```

---

## Documentos relacionados

| Doc | Para qué |
|---|---|
| `estrategia_worktrees_runtime_vtt_agentes.md` | Estrategia conceptual (Capa A + B) |
| `_template.execution.json` | Plantilla manifest por tarea |
| `gen_mensaje.py` | Genera mensaje al agente con cwd inyectado |
| `GUIA_ASIGNACION_TAREA_TL_EJECUTOR.md` | Workflow del TL al asignar |
| `GUIA_REVISION_TAREA_TL_REVIEWER.md` | Workflow del TL al revisar |
| `OPERATIVO_<rol>_MEMORY-SERVICE.md` | Operativo de cada rol (debe incluir §Working Directory) |
| `PROC-COORD-01` (TI VTT) | Incidente origen — se cierra cuando esto esté validado |
