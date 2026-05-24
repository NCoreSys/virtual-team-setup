# VTT.PROTOCOL-WT-001 — Gobernanza de Worktrees por Rol

| Campo | Valor |
|---|---|
| **Código** | `VTT.PROTOCOL-WT-001` |
| **Título** | Gobernanza de Worktrees por Rol |
| **Versión** | 1.0.1 |
| **Fecha** | 2026-05-18 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | Coordinador humano (setup + apertura), TL (asignación + revisión), Agentes ejecutores (operación diaria) |
| **Estado** | Aprobado para uso |
| **Tipo** | Opcional VTT — aplica solo a proyectos multi-rol con ejecución paralela (memory-service). Proyectos simples (un solo agente activo) pueden omitir worktrees. |
| **Reglas aplicables (Nivel 0)** | `RULE-WT-001` Worktree policy, `RULE-WT-002` Execution manifest, `RULE-WT-003` Cleanup post-aprobación, `RULE-AGENT-001 v2.0` Worktree por rol, `RULE-TL-001` Worktree TL |
| **Reemplaza** | `04.docs-soporte/guias-operativas/GUIA_GIT_WORKTREES_TL_BACKEND.md` v2.0 (legacy descriptiva) |

---

## Tabla de Contenido

1. [Propósito](#1-propósito)
2. [Campo de Aplicación](#2-campo-de-aplicación)
3. [Responsabilidades](#3-responsabilidades)
4. [Definiciones](#4-definiciones)
5. [Procedimiento](#5-procedimiento)
   - 5.1 [FASE 1 — Setup inicial del proyecto (one-time)](#51-fase-1--setup-inicial-del-proyecto)
   - 5.2 [FASE 2 — Apertura de sesión diaria](#52-fase-2--apertura-de-sesión-diaria)
   - 5.3 [FASE 3 — Onboarding de rol nuevo (bajo demanda)](#53-fase-3--onboarding-de-rol-nuevo)
   - 5.4 [FASE 4 — Casos especiales](#54-fase-4--casos-especiales)
   - 5.5 [FASE 5 — Cleanup final del proyecto](#55-fase-5--cleanup-final-del-proyecto)
6. [Referencias Cruzadas](#6-referencias-cruzadas)
7. [Reglas críticas](#7-reglas-críticas)
8. [Resumen de Revisiones](#8-resumen-de-revisiones)

---

## 1. Propósito

Establecer el modelo normativo de **git worktrees por rol** que garantiza que múltiples agentes (BE, DB, FE, QA, DO, TL, PM, SA) puedan trabajar en paralelo sobre el mismo proyecto sin pisarse entre sí.

> **Problema que resuelve:** sin worktrees, agentes que comparten working tree compiten por la branch activa. Caso real PROC-COORD-01 (MS-286): tres agentes con un solo clone hicieron `git checkout feature/MS-Y` y el agente que tenía `feature/MS-X` perdió su working state. Con worktrees por rol **cada agente tiene directorio físico distinto** → imposibilidad técnica de pisarse.

**Decisión central:**

> Cada **rol activo** tiene un worktree fijo durante todo el proyecto. La **tarea** define solo la branch dentro de ese worktree. Una ventana VSCode por rol. Una sesión Claude Code por ventana.

---

## 2. Campo de Aplicación

### Aplica a

- Proyectos VTT con **2+ agentes ejecutores en paralelo** sobre el mismo repositorio
- Proyectos donde el TL necesita operar simultáneamente con agentes (review en vivo)
- Cualquier rol que necesite `.env` propio o `node_modules` independiente del clon base

### NO aplica a

- Proyectos con un solo agente activo (clon directo es suficiente)
- Proyectos sin ejecución de código (solo documentación)
- Repos sin Git

> **Nota sobre Workflows/Skills/Scripts:** este Protocol referencia 5 Workflows + 2 Skills + 3 Scripts derivados (ver §6). Al momento de publicar v1.0.0, esos artefactos están **pendientes de escribir**. Las referencias se mantienen para que cuando se escriban hagan match. Mientras tanto:
>
> - Cada paso del §5 que invoca un PROCESO incluye el **comando directo** que el Workflow encapsulará — el agente puede ejecutar el Protocol completo sin esperar los Workflows.
> - Cuando los Workflows estén escritos, este Protocol queda intacto — solo se quitan las notas "pendiente".

---

## 3. Responsabilidades

### 3.1 Coordinador humano (Martin)
- Ejecutar setup inicial del proyecto (FASE 1) — una vez por proyecto
- Apertura de sesión diaria (FASE 2) — abrir las N ventanas VSCode necesarias

### 3.2 TL (Tech Lead)
- Onboardear rol nuevo cuando entra al proyecto (FASE 3) — bajo demanda
- Verificar disciplina de worktree del agente al cerrar tarea (`PROTOCOL-ASG-001 §5.5.5.b`)
- Crear worktrees auxiliares bajo demanda (`PROTOCOL-MAN-001 §5.1`)
- Ejecutar cleanup branch local post-aprobación (`PROTOCOL-ASG-001 §5.5.18`)

### 3.3 Agentes ejecutores (BE/DB/FE/DO/QA/DL/UX/AR/SA)
- Operar SIEMPRE en su worktree dedicado (NUNCA en clon base ni en otro worktree)
- Leer execution_manifest antes de empezar (`PROTOCOL-MAN-001 §5.2`)
- Verificar `git status` limpio antes de iniciar nueva tarea
- Reportar al TL si el worktree quedó corrupto

### 3.4 PM (Product Manager)
- Cierre final del proyecto — disparar FASE 5 (Cleanup) cuando se cierra el repo

---

## 4. Definiciones

**Worktree:** directorio físico independiente del clon base que comparte `.git/` pero tiene su propia branch checked-out. Permite que múltiples branches coexistan simultáneamente en el filesystem sin conflicto.

**Worktree por rol:** estructura `.vtt/worktrees/<repo>-<rol>/` donde `<rol>` ∈ {be, db, fe, do, qa, tl, pm, sa, etc.}. Cada rol tiene **un** worktree fijo durante todo el proyecto.

**Workspace VSCode dedicado:** archivo `.code-workspace` en `.vtt/workspaces/<repo>-<rol>.code-workspace` que abre VSCode con título identificable y `cwd` apuntando al worktree del rol.

**Branch idle (`wt-<repo>-<rol>`):** branch base del worktree cuando no hay tarea activa. NO se mergea a main. Sirve solo para que el worktree no quede en estado detached HEAD.

**Branch de tarea (`feature/<TASK_ID>`):** branch creada dentro del worktree del agente para una tarea específica. Vive en el mismo worktree hasta que se mergee y se cleanee.

**Execution manifest:** instructivo local del TL al agente — define `allowedPaths`, `branchExpected`, `worktreePath`. Vive en `.vtt/manifests/<TASK_ID>.execution.json`. Ver `VTT.PROTOCOL-MAN-001 §5.1` para detalle.

**Clon base:** repositorio clonado originalmente (`<project_root>/<repo>/`). **NO se trabaja directamente aquí** — solo sirve como anchor para los worktrees.

**PROC-COORD-01:** incidente fuente que originó este Protocol — 3 agentes pisaron archivos al compartir working tree.

---

## 5. Procedimiento

### 5.1 FASE 1 — Setup inicial del proyecto

> **Trigger:** proyecto recién clonado, antes de iniciar el primer sprint.
> **Quién ejecuta:** Coordinador humano (Martin) o TL principal.
> **Frecuencia:** UNA VEZ por proyecto.

5.1.1 Verificar que existen los clones base de los repos del proyecto → **[ACTIVIDAD]**
   ```
   ls <project_root>/<repo>-backend/
   ls <project_root>/<repo>-project/
   # etc — todos los repos del proyecto
   ```

5.1.2 Identificar los roles activos al inicio del proyecto → **[ACTIVIDAD]**
   - Típicamente: TL, BE, DB, DO, QA, PM, SA
   - Roles que entran más tarde (FE, UX, DL): se onboardean en FASE 3 cuando lleguen

5.1.3 Crear estructura `.vtt/` → **[ACTIVIDAD]**
   ```
   mkdir -p <project_root>/.vtt/{worktrees,workspaces,manifests}
   ```

5.1.4 **Crear UN worktree por cada rol activo** → **[PROCESO]** → ver `VTT.WORKFLOW-WT-001.001_setup_inicial` *(pendiente de escribir — mientras tanto usar el comando directo abajo)*
   - Invoca: `VTT.SKILL-WT-001` (`action=add_worktree`)
   - Por cada rol: `git worktree add ../.vtt/worktrees/<repo>-<rol> -b wt-<repo>-<rol> origin/main`

5.1.5 Generar workspace VSCode por cada worktree → **[PROCESO]** → ver `VTT.WORKFLOW-WT-001.001` *(pendiente)*
   - Invoca: `VTT.SKILL-WT-002` (`action=generate_workspace`) *(pendiente)*
   - Output: `<project_root>/.vtt/workspaces/<repo>-<rol>.code-workspace` por cada rol

5.1.6 Verificar que cada worktree tiene su branch idle activa → **[ACTIVIDAD]**
   ```
   git worktree list
   # Esperado: lista los N worktrees, cada uno en su wt-<repo>-<rol>
   ```

5.1.7 Crear archivo template del execution_manifest → **[ACTIVIDAD]**
   ```
   cp $VTT_SETUP/03.templates/normativa/_template.execution.json \
      .vtt/manifests/_template.execution.json
   ```

5.1.8 **Fin de FASE 1.** El proyecto queda listo para asignar tareas a agentes.

---

### 5.2 FASE 2 — Apertura de sesión diaria

> **Trigger:** Coordinador inicia día de trabajo del proyecto.
> **Quién ejecuta:** Coordinador humano (apertura) + cada agente (en su ventana).
> **Frecuencia:** Diaria.

5.2.1 Coordinador identifica qué roles trabajarán hoy → **[ACTIVIDAD]**
   - Típicamente: TL + 2-3 agentes ejecutores activos

5.2.2 Por cada rol activo, doble click en su workspace VSCode → **[ACTIVIDAD]**
   ```
   .vtt/workspaces/<repo>-<rol>.code-workspace
   ```
   - Abre ventana VSCode con título identificable (ej. "BE - Backend Engineer | <Proyecto>")
   - cwd ya apunta a su worktree

5.2.3 Dentro de cada ventana, abrir chat Claude Code → **[ACTIVIDAD]**
   - Una sesión por ventana — NO compartir Claude entre roles

5.2.4 Cada agente verifica `git status` de su worktree → **[ACTIVIDAD]**
   ```
   cd .vtt/worktrees/<repo>-<rol>
   git status
   git branch --show-current
   ```

5.2.4.bis ¿Qué branch está activa? → **[DECISIÓN — 3 casos]**
   - **Caso A:** branch idle `wt-<repo>-<rol>` → estado esperado, todo limpio → continuar a 5.2.5
   - **Caso B:** branch `feature/<TASK_ID>` de tarea YA aprobada y mergeada a main → el cleanup post-aprobación no se ejecutó. Acción:
     ```
     git fetch origin
     git checkout main
     git pull origin main
     git branch -d feature/<TASK_ID>        # borrar branch local mergeada
     git checkout wt-<repo>-<rol>           # volver a idle
     ```
     Si `git branch -d` falla con "not fully merged" → confirmar primero que el PR mergeó (mirar GitHub). Si sí mergeó pero git local no lo refleja → `git pull` antes.
   - **Caso C:** branch `feature/<TASK_ID>` de tarea **NO mergeada todavía** (in_progress, in_review, on_hold, rejected) → tarea en curso. Acción:
     - Si la tarea de hoy es la misma `<TASK_ID>` → quedarse en esa branch y continuar
     - Si la tarea de hoy es OTRA → ver §5.4.3 (Worktree con cambios sin commitear al cambiar de tarea) ANTES de cambiar branch

5.2.5 Si `git status` está sucio (modificaciones sin commitear) → **[DECISIÓN]**
- **Sí** → ver §5.4.3 para resolver (commit WIP, stash o abandonar)
- **NO** → continuar — agente listo para recibir asignación

5.2.6 **Fin de FASE 2.** Las N ventanas VSCode quedan abiertas todo el día. `Alt+Tab` para cambiar entre agentes.

---

### 5.3 FASE 3 — Onboarding de rol nuevo (bajo demanda)

> **Trigger:** un nuevo rol entra al proyecto (ej. FE al llegar a Fase 4.4 Frontend; SEC al llegar a 3B.7 Security Plan).
> **Quién ejecuta:** TL principal del proyecto.
> **Frecuencia:** Bajo demanda — cuando entra un rol nuevo.

5.3.1 TL identifica el rol nuevo + repo donde operará → **[ACTIVIDAD]**
   - Ej. FE → repo `<proyecto>-frontend`

5.3.2 TL agrega worktree para el rol → **[PROCESO]** → ver `VTT.WORKFLOW-WT-001.003_agregar_rol`
   - Invoca: `VTT.SKILL-WT-001` (`action=add_worktree`)
   - Output: `.vtt/worktrees/<repo>-<rol_nuevo>/`

5.3.3 TL genera workspace VSCode del rol nuevo → **[PROCESO]** → ver `VTT.WORKFLOW-WT-001.003`
   - Invoca: `VTT.SKILL-WT-002` (`action=generate_workspace`)
   - Output: `.vtt/workspaces/<repo>-<rol_nuevo>.code-workspace`

5.3.4 TL verifica setup → **[ACTIVIDAD]**
   ```
   git worktree list
   # Esperado: incluye el worktree nuevo
   ls .vtt/workspaces/<repo>-<rol_nuevo>.code-workspace
   # Esperado: archivo existe
   ```

5.3.5 TL notifica al Coordinador para que abra la ventana cuando empiece a usarse → **[ACTIVIDAD]**

5.3.6 **Fin de FASE 3.** El rol nuevo está listo para recibir tareas.

---

### 5.4 FASE 4 — Casos especiales

> **Trigger:** se presenta uno de los 4 sub-casos.
> **Quién ejecuta:** Agente ejecutor o TL según el caso.

#### 5.4.1 Tarea toca múltiples repos (BE + project)

5.4.1.a Agente identifica que necesita tocar un repo fuera de su worktree principal → **[ACTIVIDAD]**

5.4.1.b ¿Necesita escribir o solo leer? → **[DECISIÓN]**
- **Solo leer** → puede leer directo del clon base (no toca branch)
- **Escribir** → continuar al .c

5.4.1.c TL crea worktree auxiliar temporal bajo demanda → **[PROCESO]** → ver `VTT.WORKFLOW-WT-001.004_casos_especiales` §1
   ```
   cd <project_root>/<otro_repo>
   git worktree add ../.vtt/worktrees/<otro_repo>-<rol>-aux -b wt-<otro_repo>-<rol>-aux origin/main
   ```

5.4.1.d Agente trabaja en el worktree auxiliar para esa parte específica → **[ACTIVIDAD]**

5.4.1.e Al cerrar la tarea, TL cleanea el worktree auxiliar → **[ACTIVIDAD]**
   ```
   git worktree remove ../.vtt/worktrees/<otro_repo>-<rol>-aux
   ```

#### 5.4.2 Branch base de la tarea NO es main

5.4.2.a Tarea MS-310 depende de MS-309 que aún NO está en main → **[CONTEXTO]**

5.4.2.b Agente crea branch desde la branch padre → **[PROCESO]** → ver `VTT.WORKFLOW-WT-001.004 §2`
   ```
   cd .vtt/worktrees/<repo>-<rol>
   git fetch origin
   git checkout -b feature/MS-310 origin/feature/MS-309
   ```

5.4.2.c Cuando MS-309 mergea a main, agente rebase MS-310 → **[ACTIVIDAD]**
   ```
   git rebase origin/main
   ```

5.4.2.d PR de MS-310 target `main` (NO `feature/MS-309`) → **[REGLA]**

#### 5.4.3 Worktree con cambios sin commitear al cambiar de tarea

5.4.3.a Agente tiene cambios pendientes y necesita cambiar de tarea → **[CONTEXTO]**
   ```
   cd .vtt/worktrees/<repo>-<rol>
   git status
   # Muestra cambios uncommitted
   ```

5.4.3.b Elegir estrategia → **[DECISIÓN]** → ver `VTT.WORKFLOW-WT-001.004 §3`
- **Opción A — Commit WIP** (recomendado si vas a volver):
  ```
  git add -A && git commit -m "WIP: pause <TASK_ID>" && git push
  ```
- **Opción B — Stash** (si es muy temporal):
  ```
  git stash push -m "<TASK_ID>-pause"
  ```
- **Opción C — Abandonar** (si los cambios no sirven):
  ```
  git checkout -- .
  ```

5.4.3.c Continuar con la nueva tarea → **[ACTIVIDAD]**

#### 5.4.4 Worktree corrupto

5.4.4.a Agente detecta error inusual (HEAD detached, branch missing, etc.) → **[CONTEXTO]**

5.4.4.b Diagnóstico → **[ACTIVIDAD]** → ver `VTT.WORKFLOW-WT-001.004 §4`
   ```
   git worktree list
   ls -la .git/worktrees/
   ```

5.4.4.c Recuperar trabajo no committeado si lo hay → **[ACTIVIDAD]**
   ```
   # Stash o commit WIP antes de recrear
   ```

5.4.4.d TL recrea el worktree → **[PROCESO]** → ver `VTT.WORKFLOW-WT-001.004 §4`
   ```
   cd <repo>
   git worktree remove --force ../.vtt/worktrees/<repo>-<rol>
   git worktree add ../.vtt/worktrees/<repo>-<rol> -b wt-<repo>-<rol> origin/main
   ```

5.4.4.e Agente verifica que el worktree funciona y restaura su trabajo → **[ACTIVIDAD]**

---

### 5.5 FASE 5 — Cleanup final del proyecto

> **Trigger:** proyecto completo termina, repo se archiva o se entra a modo mantenimiento.
> **Quién ejecuta:** TL principal con autorización del PM.
> **Frecuencia:** UNA VEZ al cerrar el proyecto.

5.5.1 PM autoriza cleanup final → **[ACTIVIDAD]**

5.5.2 TL verifica que NO hay tareas activas en VTT → **[ACTIVIDAD]**

5.5.3 **TL inventaria branches `feature/*` y `fix/*` pendientes** (NO mergeadas a main) → **[ACTIVIDAD]**
   ```
   # En cada repo del proyecto:
   cd <repo>
   git fetch origin --prune
   git branch -a | grep -E "(feature|fix)/" | grep -v "merged"
   ```
   - Listar las branches resultantes con su `<TASK_ID>` y estado en VTT (`task_pending` / `task_rejected` / `task_on_hold` / etc.)

5.5.4 Por cada branch `feature/` o `fix/` pendiente → **[DECISIÓN — 3 acciones]**
   - **Acción A — Mergear** si la tarea está en `task_completed` o `task_approved` pero el PR no se mergeó. Crear PR (si no existe) + aprobar + mergear.
   - **Acción B — Cerrar como wontfix** si la tarea está abandonada (`task_rejected` permanente, `task_cancelled`). Postear comment en VTT, cerrar PR sin mergear, borrar branch en remote.
   - **Acción C — Preservar para fase 2 del proyecto** si la tarea es deuda viva para roadmap futuro. **NO borrar la branch.** Documentar en `_archive/branches_pending_phase2.md` qué branches quedan y por qué.

   > **Regla:** ninguna branch `feature/` o `fix/` se elimina silenciosamente. Cada una requiere decisión explícita y registro.

5.5.5 TL ejecuta cleanup masivo de worktrees → **[PROCESO]** → ver `VTT.WORKFLOW-WT-001.005_cleanup_final` *(pendiente)*
   - Invoca: `VTT.SCRIPT-WT-003` (`cleanup_worktrees.py`) *(pendiente)*
   - Por cada worktree:
     ```
     git worktree remove ../.vtt/worktrees/<repo>-<rol>
     ```
   - Borra branches idle: `git branch -D wt-<repo>-<rol>` por cada rol
   - **NO toca branches `feature/*` ni `fix/*`** — esas se manejaron en §5.5.4

5.5.6 TL verifica → **[ACTIVIDAD]**
   ```
   git worktree list
   # Esperado: solo el clon base

   git branch -a | grep -E "(feature|fix)/"
   # Esperado: solo las branches que decidiste preservar (Acción C de §5.5.4)
   ```

5.5.7 TL archiva la estructura `.vtt/` si se desea preservar → **[ACTIVIDAD]**
   ```
   tar czf .vtt-archive-<fecha>.tar.gz .vtt/
   rm -rf .vtt/
   ```

5.5.8 TL postea CLOSURE final del proyecto en VTT con resumen de §5.5.4 → **[ACTIVIDAD]**
   - Cuántas branches se mergearon (Acción A)
   - Cuántas se cerraron sin mergear (Acción B)
   - Cuántas se preservaron para fase 2 (Acción C) — link al archivo de registro

5.5.9 **Fin de FASE 5.** El proyecto queda en estado "archived" sin worktrees activos. Branches pendientes (si las hay) documentadas explícitamente.

---

## 6. Referencias Cruzadas

### 6.1 Workflows (Nivel 3) de este Protocol

| Código | Título | Invocado en |
|---|---|---|
| `VTT.WORKFLOW-WT-001.001` | Setup inicial (one-time) — crea N worktrees + workspaces | §5.1.4 / §5.1.5 |
| `VTT.WORKFLOW-WT-001.002` | Apertura de sesión diaria | §5.2 (referencia) |
| `VTT.WORKFLOW-WT-001.003` | Agregar worktree de rol nuevo (bajo demanda) | §5.3.2 / §5.3.3 |
| `VTT.WORKFLOW-WT-001.004` | Casos especiales (4 sub-procedimientos) | §5.4 |
| `VTT.WORKFLOW-WT-001.005` | Cleanup final del proyecto | §5.5.3 |

### 6.2 Skills (Nivel 2) invocadas

| Código | Título | Invocada por |
|---|---|---|
| `VTT.SKILL-WT-001` | Operaciones de worktree (add/remove/list/move) | WORKFLOW-WT-001.001, .003, .004, .005 |
| `VTT.SKILL-WT-002` | Generar workspace VSCode desde template | WORKFLOW-WT-001.001, .003 |

### 6.3 Scripts (Nivel 1) ejecutados

| Código | Título | Invocado por |
|---|---|---|
| `VTT.SCRIPT-WT-001` | `setup_worktrees.py` — idempotente, crea N worktrees iniciales | SKILL-WT-001 (FASE 1) |
| `VTT.SCRIPT-WT-002` | `add_worktree.py` — agrega 1 worktree para rol nuevo | SKILL-WT-001 (FASE 3) |
| `VTT.SCRIPT-WT-003` | `cleanup_worktrees.py` — remove masivo + delete branches al cerrar proyecto | SKILL-WT-001 (FASE 5) |

### 6.4 Protocols relacionados

- `VTT.PROTOCOL-ASG-001` v1.3.1 — invoca este Protocol en §5.2.10 (TL verifica worktree del agente) y §5.5.bis (Commit del TL post-aprobación usa worktree TL)
- `VTT.PROTOCOL-MAN-001` v1.1.1 — Execution Manifest define el worktree donde opera el agente

### 6.5 Reglas Nivel 0 aplicables

| Regla | Razón |
|---|---|
| `RULE-WT-001` Worktree policy | Granularidad por rol — base de este Protocol |
| `RULE-WT-002` Execution manifest | El agente lee el manifest antes de operar (FASE 2 §5.2.4) |
| `RULE-WT-003` Cleanup post-aprobación | Cleanup branch local (PROTOCOL-ASG-001 §5.5.18) |
| `RULE-AGENT-001 v2.0` Worktree por rol | Cada rol opera SIEMPRE en su worktree (FASE 2 §5.2.4) |
| `RULE-TL-001` Worktree TL | TL no opera en clon base — usa `.vtt/worktrees/<repo>-tl/` |

### 6.6 Convenciones operativas (meta-índices)

| Documento | Path canónico | Uso en este Protocol |
|---|---|---|
| Convenciones de filesystem | `02.normativa/00_CONVENCIONES_FILESYSTEM.md` v1.0 | Estructura `.vtt/worktrees/`, `.vtt/workspaces/`, `.vtt/manifests/` documentada como opcional para proyectos multi-rol |
| Registro de acrónimos + branches Git | `02.normativa/00_REGISTRO_ACRONIMOS.md` §3.bis v1.3 | Pattern `wt-<repo>-<rol>` (branch idle) registrado. Categoría `WT` activa. |

### 6.7 Documentos relacionados

- `04.docs-soporte/guias-operativas/GUIA_GIT_WORKTREES_TL_BACKEND.md` v2.0 (legacy) — guía descriptiva original que originó este Protocol. **Deprecada** al activar este Protocol. Se mantiene como referencia histórica del incidente PROC-COORD-01.
- ~~`04.docs-soporte/guias-operativas/GUIA_WORKTREES_MEMORY_SERVICE.md` v2.1~~ — referencia histórica (archivo NO existe en el setup; era una propuesta de guía específica para Memory Service que nunca se materializó). Este Protocol cubre todo el alcance que tendría esa guía.
- `00.Rules/rules_catalog.json` — catálogo de reglas Nivel 0

---

## 7. Reglas críticas

### 7.1 NUNCA trabajar en el clon base

El clon base (`<project_root>/<repo>/`) es **solo anchor** para los worktrees. Si un agente hace `cd <repo>` y `git checkout feature/X`, rompe el modelo.

> **Excepción:** lectura. Un agente puede leer archivos del clon base (no afecta branch).

### 7.2 Un rol = un worktree fijo (NO por tarea)

Si un agente termina MS-X y empieza MS-Y, **usa el MISMO worktree**, solo cambia branch:

```
✅ Correcto:
  cd .vtt/worktrees/backend-be   # MISMO
  git checkout -b feature/MS-Y origin/main

❌ Incorrecto:
  git worktree add .vtt/worktrees/backend-be-MS-Y  # NO crear nuevo por tarea
```

### 7.3 Una ventana VSCode = un rol = una sesión Claude

NO abrir 2 chats Claude en la misma ventana. NO usar 2 ventanas para el mismo rol. Cada rol tiene **su** workspace dedicado.

### 7.4 Worktrees NO van a git

La carpeta `.vtt/` está en `.gitignore`. Es infraestructura local, no se commitea.

### 7.5 Branch idle `wt-<repo>-<rol>` NUNCA se mergea

Es solo para que el worktree no quede detached. Si alguien intenta hacer PR de `wt-backend-be` → rechazar.

### 7.6 El agente verifica execution_manifest ANTES de tocar código

Al iniciar tarea, el agente DEBE leer su `.vtt/manifests/<TASK_ID>.execution.json`. Sin esto, opera ciegamente y puede tocar archivos fuera de `allowedPaths` → `task_rejected` al cierre.

**Dependencia con PROTOCOL-MAN-001:** la gobernanza completa del execution_manifest vive en `VTT.PROTOCOL-MAN-001_gobernanza_manifest.md` §5.2 (FASE 2 — Lectura del Execution Manifest), que invoca `VTT.WORKFLOW-MAN-001.002_leer_execution_manifest`.

| Quién | Hace | Cuándo |
|---|---|---|
| TL Asignador | Genera el execution_manifest en `.vtt/manifests/<TASK_ID>.execution.json` | `PROTOCOL-MAN-001 §5.1` (al asignar tarea) |
| Agente ejecutor | Lo lee ANTES de tocar código en su worktree | `PROTOCOL-MAN-001 §5.2` (este Protocol §7.6) |
| TL Reviewer | Valida disciplina (diff vs `allowedPaths`) al cerrar | `PROTOCOL-ASG-001 §5.5.5.b` |

Este Protocol (WT) provee el **worktree donde el agente opera**. El manifest (MAN) provee las **instrucciones de qué puede tocar**. Los dos sub-sistemas son ortogonales pero acoplados — el `worktreePath` del manifest siempre apunta a un worktree creado por este Protocol WT.

### 7.7 Cleanup branch local post-aprobación es obligatorio

Después de cada `task_approved`, el TL ejecuta `git branch -d feature/<TASK_ID>` en el worktree del agente. Sin esto, branches se acumulan localmente. Ver `PROTOCOL-ASG-001 §5.5.18`.

---

## 8. Resumen de Revisiones

| Versión | Fecha | Editor | Cambios |
|---|---|---|---|
| 1.0.0 | 2026-05-18 | PM Martin Rivas | Versión inicial. Formaliza el modelo de worktrees por rol que estaba documentado solo en `GUIA_GIT_WORKTREES_TL_BACKEND.md` v2.0 (legacy descriptiva). Origen: incidente PROC-COORD-01 (MS-286). Define 5 FASEs operativas, 5 Workflows derivados, 2 Skills, 3 Scripts. Cross-ref con PROTOCOL-MAN-001 (execution manifest) y PROTOCOL-ASG-001 (verificación de disciplina + cleanup). Categoría `WT` registrada en `00_REGISTRO_ACRONIMOS.md §3.1` v1.3. |
| 1.0.1 | 2026-05-18 | PM Martin Rivas | **4 fixes de review.** (1) §2 nota explícita sobre Workflows/Skills/Scripts pendientes — el Protocol es ejecutable desde hoy con comandos directos en cada paso. (2) §7.6 amplía la dependencia con PROTOCOL-MAN-001 con tabla de ortogonalidad (WT = worktree, MAN = qué tocar — sub-sistemas acoplados pero independientes). (3) §5.2.4.bis nuevo: decisión por 3 casos al abrir sesión (branch idle / branch mergeada sin cleanup / branch en curso). (4) §5.5.3-5.5.4 nuevos: inventario de branches `feature/*` y `fix/*` pendientes al cierre del proyecto con 3 acciones (mergear / cerrar wontfix / preservar para fase 2). §5.5.8 nuevo: CLOSURE final con resumen. |

---

**Fin del Protocol.** Para implementar, ver los 5 Workflows (`VTT.WORKFLOW-WT-001.001..005`), 2 Skills (`VTT.SKILL-WT-001`, `VTT.SKILL-WT-002`) y 3 Scripts (`VTT.SCRIPT-WT-001`, `VTT.SCRIPT-WT-002`, `VTT.SCRIPT-WT-003`).
