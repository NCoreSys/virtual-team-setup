# Guía operativa — Git Worktrees para TL Backend

**Versión:** 1.0
**Fecha:** 2026-05-14
**Aplicable a:** TL Backend (y por extensión todos los TL/PJM que asignan tareas que tocan código)
**Origen:** PROC-COORD-01 (MS-286) — incidente de working tree perdido por checkout cross-agente

---

## El problema que resolvemos

Cuando dos agentes trabajan en el mismo clon del repo en branches distintas:

```
memory-service-backend/   (clon único)
  └── .git/
  └── src/...
```

Si el BE Engineer está en `feature/MS-293` con archivos sin commitear y el DO Engineer hace `git checkout feature/MS-286`, **el working tree del BE se descarta**. Archivos no commiteados se pierden.

**Incidente real:** MS-286 perdió 5 archivos por checkout cross-agente durante MS-293. Lección registrada como `PROC-COORD-01`.

---

## La solución: Git Worktrees

Cada agente trabaja en un **directorio físico distinto** pero comparten el mismo `.git/`. No hay checkouts cruzados posibles.

```
memory-service/
  ├── memory-service-backend/              ← clon base (TL, exploración, NO ejecutar tareas aquí)
  ├── memory-service-backend-MS-286/       ← worktree del DO (feature/MS-286)
  ├── memory-service-backend-MS-293/       ← worktree del BE (feature/MS-293)
  ├── memory-service-project/              ← clon base project
  ├── memory-service-project-MS-286/       ← worktree del DO
  └── memory-service-project-MS-293/       ← worktree del BE
```

Cada worktree:
- Tiene su propia branch checked out **simultáneamente** (no se bloquean)
- Tiene su propio `node_modules`, `.env`, archivos locales
- Comparte el `.git/` del clon base (no duplica historia)

---

## Reglas operativas

### Regla 1 — El TL crea el worktree al asignar

Cuando asignas una tarea (paso 8.5 del `PROCESO_ASIGNACION_TAREAS_v3.md`):

```bash
# Por cada repo que la tarea va a tocar (backend, project, o ambos)
cd /path/to/memory-service-backend
git fetch origin
git worktree add ../memory-service-backend-MS-XXX -b feature/MS-XXX origin/main
```

**Flags relevantes:**
- `-b feature/MS-XXX` — crea la branch nueva al instante
- `origin/main` — base actualizada
- Path relativo `../memory-service-backend-MS-XXX` — convención obligatoria

**Si la tarea depende de una branch upstream NO mergeada** (ej. MS-293 base feature/MS-292):
```bash
git worktree add ../memory-service-backend-MS-XXX -b feature/MS-XXX origin/feature/MS-292
```

### Regla 2 — El agente NUNCA trabaja en el clon base

El mensaje al agente (`gen_mensaje.py`) debe incluir la ruta del worktree:

```markdown
## Working directory

Tu worktree dedicado: `c:/Users/Martin/Documents/virtual-teams/memory-service/memory-service-backend-MS-XXX/`

⚠️ NO hagas `git checkout` en el clon base `memory-service-backend/`.
⚠️ NO claones de nuevo — el worktree ya está listo.

cd c:/Users/Martin/Documents/virtual-teams/memory-service/memory-service-backend-MS-XXX
```

### Regla 3 — Cada worktree tiene su propio entorno

```bash
cd memory-service-backend-MS-XXX
cp ../memory-service-backend/.env .env       # copiar config local
npm install                                    # instalar deps en este worktree
```

**Puertos para servicios locales** (npm run dev): convención por posición en sprint
- MS-283 → 3001
- MS-284 → 3002
- MS-285 → 3003
- MS-286 → 3004
- MS-287 → 3005
- MS-288 → 3006
- MS-293 → 3013

Documentar el puerto en el ASSIGNMENT §6 (workflow) y en el `.env` local del worktree:
```bash
PORT=3004 npm run dev
```

### Regla 4 — Cleanup al cerrar la tarea

El TL Reviewer al cerrar (paso 16 del cierre):

```bash
# Verificar que la branch ya está en task_completed o PR merged
# Luego:
cd /path/to/memory-service-backend
git worktree remove ../memory-service-backend-MS-XXX

# Si el worktree tiene cambios sin commitear (no debería):
git worktree remove --force ../memory-service-backend-MS-XXX
```

**NO borrar la branch local** todavía — esperar a que el PR esté mergeado:
```bash
git branch -d feature/MS-XXX   # solo después del merge
```

### Regla 5 — Auditoría de worktrees activos

Al iniciar sesión (apertura TL):

```bash
cd /path/to/memory-service-backend
git worktree list
```

Output esperado:
```
/path/memory-service-backend                  abc1234 [main]
/path/memory-service-backend-MS-286          def5678 [feature/MS-286]
/path/memory-service-backend-MS-293          ghi9012 [feature/MS-293]
```

Si ves worktrees de tareas ya cerradas → cleanup pendiente.

---

## Comandos rápidos

### Crear worktree para nueva tarea

```bash
TASK=MS-XXX
BASE_BRANCH=main                              # o feature/MS-YYY si depende

cd memory-service-backend
git fetch origin
git worktree add ../memory-service-backend-$TASK -b feature/$TASK origin/$BASE_BRANCH

cd memory-service-project
git fetch origin
git worktree add ../memory-service-project-$TASK -b feature/$TASK origin/$BASE_BRANCH
```

### Setup entorno en el worktree (lo hace el agente al arrancar)

```bash
TASK=MS-XXX
cd memory-service-backend-$TASK
cp ../memory-service-backend/.env .env 2>/dev/null || true
npm install
```

### Listar worktrees activos

```bash
git worktree list
```

### Remover worktree al cerrar

```bash
TASK=MS-XXX
cd memory-service-backend
git worktree remove ../memory-service-backend-$TASK

cd memory-service-project
git worktree remove ../memory-service-project-$TASK
```

### Cleanup forzado (si hay cambios sin commitear que ya no importan)

```bash
git worktree remove --force ../memory-service-backend-$TASK
```

---

## Casos especiales

### Caso 1 — Branch encadenada (upstream no mergeada)

Si MS-293 depende de MS-292 (que aún no está en main):

```bash
git fetch origin
git worktree add ../memory-service-backend-MS-293 -b feature/MS-293 origin/feature/MS-292
```

El agente luego rebasea sobre main cuando MS-292 caiga:
```bash
cd memory-service-backend-MS-293
git fetch origin
git rebase origin/main
```

### Caso 2 — Worktree existente con la misma branch

Si `feature/MS-XXX` ya tiene worktree creado:
```bash
git worktree list | grep MS-XXX
```

Si existe → el agente continúa en él, no se recrea.

### Caso 3 — Detenerse a mitad de tarea (task_on_hold)

NO remover el worktree. Queda como está hasta que se retome.

### Caso 4 — Agente perdió o corrompió el worktree

```bash
git worktree remove --force ../memory-service-backend-MS-XXX
git worktree add ../memory-service-backend-MS-XXX feature/MS-XXX
# Recuperar archivos sin commitear si los hay (probablemente perdidos)
```

### Caso 5 — Mover worktree a otro path

```bash
git worktree move ../memory-service-backend-MS-XXX /new/path/memory-service-backend-MS-XXX
```

### Caso 6 — Lock automático para evitar checkouts en el clon base

En el clon base, agregar a `.git/info/exclude` un hook que rechace `git checkout` si hay worktrees activos:

```bash
# .git/hooks/pre-checkout
#!/bin/sh
WORKTREES=$(git worktree list | wc -l)
if [ $WORKTREES -gt 1 ]; then
  echo "ERROR: Hay $WORKTREES worktrees activos."
  echo "El clon base NO debe cambiar de branch mientras existan worktrees."
  echo "Trabaja en tu worktree: git worktree list"
  exit 1
fi
```

(Opcional — git no tiene `pre-checkout` nativo, requiere hook custom.)

---

## Integración con el workflow

### En `PROCESO_ASIGNACION_TAREAS_v3.md` — agregar Paso 8.5

```markdown
### Paso 8.5 — Crear worktree(s) para el agente

Antes de generar el mensaje (Paso 9):

bash
TASK=MS-XXX
cd memory-service-backend && git worktree add ../memory-service-backend-$TASK -b feature/$TASK origin/main
cd memory-service-project && git worktree add ../memory-service-project-$TASK -b feature/$TASK origin/main


La ruta del worktree se incluye en el mensaje al agente (gen_mensaje.py la inyecta).
```

### En `gen_mensaje.py` — incluir ruta del worktree

```python
def get_worktree_paths(task_id):
    """Detecta worktrees creados para esta tarea."""
    repos = []
    for repo in ['memory-service-backend', 'memory-service-project']:
        worktree = f'/path/to/{repo}-{task_id}'
        if os.path.isdir(worktree):
            repos.append((repo, worktree))
    return repos

# En el mensaje:
worktrees = get_worktree_paths(task_id)
if worktrees:
    print("## Working directories")
    for repo, path in worktrees:
        print(f"- {repo}: `{path}`")
    print("\n⚠️ NO hagas `git checkout` en los clones base.")
```

### En `OPERATIVO_<rol>_MEMORY-SERVICE.md` — agregar §Working Directory

```markdown
## §X Working Directory

Cuando recibes una tarea, el TL ya creó tu worktree dedicado:

`memory-service-<repo>-MS-XXX/`

**Reglas:**
- Trabaja exclusivamente en tu worktree
- NO hagas `git checkout` en el clon base (`memory-service-<repo>/` sin sufijo)
- NO clones de nuevo — el worktree ya está listo
- Cada worktree tiene su propio `node_modules` y `.env`
```

### En `TEMPLATE_ASIGNACION_TAREARev.md` — agregar al Paso 0 del workflow del agente

```markdown
**0. Trabajar en el worktree dedicado (NO en el clon base):**
bash
cd /path/to/memory-service-backend-MS-XXX
git status                                 # confirma branch feature/MS-XXX
```

---

## Scripts pendientes de crear

Para automatizar, recomiendo agregar al repo `memory-service-project/scripts/`:

### `setup_worktree.py MS-XXX [--base feature/MS-YYY]`

```python
#!/usr/bin/env python
"""Crea worktrees para una tarea nueva.

Usage:
    python scripts/setup_worktree.py MS-XXX
    python scripts/setup_worktree.py MS-XXX --base feature/MS-YYY
    python scripts/setup_worktree.py MS-XXX --repos backend,project
"""
import argparse, os, subprocess, sys

def main():
    p = argparse.ArgumentParser()
    p.add_argument('task_id')
    p.add_argument('--base', default='main')
    p.add_argument('--repos', default='backend,project')
    args = p.parse_args()

    repos_map = {
        'backend': 'memory-service-backend',
        'project': 'memory-service-project',
    }
    repos = [repos_map[r] for r in args.repos.split(',')]

    for repo in repos:
        if not os.path.isdir(repo):
            print(f"SKIP {repo}: no existe")
            continue
        wt_path = f"../{repo}-{args.task_id}"
        if os.path.isdir(wt_path):
            print(f"SKIP {repo}: worktree ya existe en {wt_path}")
            continue
        subprocess.run(['git', '-C', repo, 'fetch', 'origin'], check=True)
        subprocess.run(['git', '-C', repo, 'worktree', 'add', wt_path,
                       '-b', f'feature/{args.task_id}',
                       f'origin/{args.base.replace("feature/","feature/")}' if not args.base.startswith('origin/') else args.base],
                      check=True)
        # Copiar .env si existe en el clon base
        src_env = f"{repo}/.env"
        dst_env = f"{wt_path}/.env"
        if os.path.isfile(src_env) and not os.path.isfile(dst_env):
            subprocess.run(['cp', src_env, dst_env], check=True)
            print(f"  .env copiado a {dst_env}")
        print(f"OK {repo}: worktree en {wt_path}")

if __name__ == '__main__':
    main()
```

### `cleanup_worktree.py MS-XXX [--force]`

```python
#!/usr/bin/env python
"""Remueve worktrees de una tarea cerrada.

Verifica que la tarea esté en task_completed o task_approved antes de borrar.
"""
import argparse, json, os, subprocess, sys, urllib.request

BASE_URL = "http://77.42.88.106:3000"

def get_task_status(task_id, token):
    req = urllib.request.Request(f'{BASE_URL}/api/tasks/{task_id}',
        headers={'Authorization': f'Bearer {token}'})
    return json.loads(urllib.request.urlopen(req).read())['data']['status']['code']

def main():
    p = argparse.ArgumentParser()
    p.add_argument('task_id')
    p.add_argument('--force', action='store_true')
    p.add_argument('--token-from-env', default='MEM_VTT_TOKEN')
    args = p.parse_args()

    if not args.force:
        token = os.environ.get(args.token_from_env)
        if not token:
            sys.exit(f"ERROR: $({args.token_from_env}) no definido. Usar --force para skip check.")
        status = get_task_status(args.task_id, token)
        if status not in ('task_completed', 'task_approved'):
            sys.exit(f"ERROR: {args.task_id} está en {status}. Esperado task_completed/task_approved. Usar --force para forzar.")

    for repo_base in ['memory-service-backend', 'memory-service-project']:
        wt_path = f"../{repo_base}-{args.task_id}"
        if not os.path.isdir(wt_path):
            print(f"SKIP {repo_base}: no hay worktree en {wt_path}")
            continue
        flag = ['--force'] if args.force else []
        try:
            subprocess.run(['git', '-C', repo_base, 'worktree', 'remove'] + flag + [wt_path], check=True)
            print(f"OK {repo_base}: worktree removido")
        except subprocess.CalledProcessError as e:
            print(f"ERR {repo_base}: {e}")

if __name__ == '__main__':
    main()
```

---

## Checklist de adopción

```
[ ] Validar que `git worktree` funciona en Windows (debe — git 2.5+)
[ ] Crear scripts/setup_worktree.py y scripts/cleanup_worktree.py
[ ] Actualizar gen_mensaje.py para inyectar ruta del worktree
[ ] Agregar Paso 8.5 al PROCESO_ASIGNACION_TAREAS_v3.md
[ ] Agregar Paso 16 cleanup al PROCESO_CIERRE_TAREA_v2.md
[ ] Actualizar TEMPLATE_ASIGNACION_TAREARev.md (Paso 0 del agente)
[ ] Actualizar OPERATIVOs de roles ejecutores (§Working Directory)
[ ] Migrar worktrees existentes:
    - MS-286, MS-288, MS-293 ya están cerradas → cleanup
    - Tareas activas → recrear como worktrees
[ ] Cerrar TI PROC-COORD-01 con [RESOLVED] cuando esto esté operativo
```

---

## Beneficios esperados

| Antes | Después |
|---|---|
| Checkouts cruzados pierden archivos | Imposibilidad técnica (working trees aislados) |
| Agentes esperan turno para usar el repo | Trabajo paralelo sin conflicto |
| Cleanup manual de branches sin merge | Convención clara con script |
| Mensaje al agente con "cuidado con el branch" | Mensaje con ruta exacta del worktree |
| Incidente PROC-COORD-01 (5 archivos perdidos) | Imposible repetir |

---

## Limitaciones conocidas

| Limitación | Mitigación |
|---|---|
| `node_modules` se duplica por worktree | Trade-off aceptable (~500MB c/u); o usar pnpm con store compartido |
| Si la branch ya existe en el clon base, no se puede recrear con worktree | Detectar y reusar branch existente |
| Cleanup olvidado deja worktrees huérfanos | `git worktree list` en apertura de sesión + `git worktree prune` |
| Puertos npm conflictivos | Convención de puertos por posición en sprint |
| Hooks de git (husky, pre-commit) corren en cada worktree | Esperado — comportamiento correcto |

---

## Documentos relacionados

| Doc | Para qué |
|---|---|
| `PROC-COORD-01` (TI en VTT) | Incidente de origen |
| `PROCESO_ASIGNACION_TAREAS_v3.md` | Donde se inserta Paso 8.5 |
| `PROCESO_CIERRE_TAREA_v2.md` | Donde se inserta Paso 16 cleanup |
| `TEMPLATE_ASIGNACION_TAREARev.md` v3.1 | Paso 0 del workflow del agente |
| `OPERATIVO_<rol>_MEMORY-SERVICE.md` | §Working Directory |
| `GUIA_ASIGNACION_TAREA_TL_EJECUTOR.md` | Guía operativa hermana |

---

## Cuando esté operativo

1. Cerrar TI `PROC-COORD-01` (UUID `4b54b2cc-cd96-47d4-bf64-7f0ebfbfe6b0`) marcándolo como resuelto en su descripción
2. Agregar evidencia a `PROC-COORD-01` con marker `[TASK:MS-XXX] [SPRINT:SX]` del PR que implementa los scripts
3. Actualizar `feedback_branches_encadenadas_pre_merge.md` (memoria) para reflejar que worktrees mitigan el problema de cadenas
