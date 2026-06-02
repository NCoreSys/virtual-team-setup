# VTT.PROTOCOL-WT-001 — Gobernanza de Worktrees por Equipo

| Campo | Valor |
|---|---|
| **Código** | `VTT.PROTOCOL-WT-001` |
| **Título** | Gobernanza de Worktrees por Equipo (antes: por Rol) |
| **Versión** | 1.1.0 |
| **Fecha** | 2026-06-02 |
| **Autor** | PM Martin Rivas (v1.0.x), PM_GOV (v1.1.0 — bajo dirección de Martin) |
| **Aplica a** | Coordinador humano (setup + apertura), TL/PM_GOV/Leads (asignación + revisión + coordinación de equipo), Agentes ejecutores (operación diaria) |
| **Estado** | Aprobado para uso |
| **Tipo** | Aplicable VTT — aplica a proyectos multi-agente con cambios concurrentes a archivos compartidos (memory-service, vtt-setup, futuros). Aplica también a proyectos de documentación/gobernanza con 2+ agentes concurrentes. Proyectos con un solo agente activo pueden omitir worktrees. |
| **Reglas aplicables (Nivel 0)** | `RULE-WT-001` Worktree policy, `RULE-WT-002` Execution manifest, `RULE-WT-003` Cleanup post-aprobación, `RULE-AGENT-001 v2.0` Worktree por equipo, `RULE-TL-001` Worktree TL/Lead |
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

Establecer el modelo normativo de **git worktrees por equipo** que garantiza que múltiples agentes puedan trabajar en paralelo sobre el mismo proyecto sin pisarse entre sí, **sea código o documentación**.

> **Problema que resuelve:** sin worktrees, agentes que comparten working tree compiten por la branch activa. Caso real PROC-COORD-01 (MS-286): tres agentes con un solo clone hicieron `git checkout feature/MS-Y` y el agente que tenía `feature/MS-X` perdió su working state. Caso real vtt-setup (2026-06-02): agente TW-OPS creó branch y empezó a trabajar; agente RA arrancó en paralelo y al hacer checkout deshizo el estado de TW-OPS. **El incidente confirmó que el riesgo NO es exclusivo de proyectos de código** — cualquier proyecto multi-agente con archivos compartidos lo sufre.
>
> Con worktrees **cada equipo tiene directorio físico distinto** → imposibilidad técnica de pisarse entre equipos.

**Decisión central (v1.1.0):**

> Cada **equipo activo** tiene un worktree fijo durante todo el proyecto. La **tarea** define solo la branch dentro de ese worktree. Una ventana VSCode por equipo. Una sesión Claude Code por agente del equipo (puede haber varios agentes en el mismo worktree de equipo, coordinados por su líder humano o agente coordinador del equipo).

### Modelo de equipos

Un **equipo** es un Lead/Coordinador + sus ejecutores que trabajan sobre el mismo conjunto de archivos. Ejemplos:

| Proyecto | Equipo | Lead | Ejecutores | Worktree |
|---|---|---|---|---|
| `vtt-setup` | Normativa | LEAD_NPL | TW-OPS | `.vtt/worktrees/vtt-setup-team-normativa/` |
| `vtt-setup` | Research | LEAD_RKL | RA | `.vtt/worktrees/vtt-setup-team-research/` |
| `vtt-setup` | Agentes & Plataforma | LEAD_APL | (futuros ejecutores de perfilería) | `.vtt/worktrees/vtt-setup-team-agents/` |
| `memory-service` | Backend | TL | BE, DB | `.vtt/worktrees/memory-service-team-backend/` (cuando se aplique modelo equipo) |
| `memory-service` | Frontend | TL | FE, UX | `.vtt/worktrees/memory-service-team-frontend/` (cuando se aplique modelo equipo) |

### Coordinación intra-equipo

Dentro de un worktree de equipo, **los agentes del equipo coordinan branches secuencialmente**, no en paralelo:
- El Lead asigna tarea a un solo agente por vez del equipo.
- Si dos agentes del mismo equipo necesitan trabajar en paralelo, el Lead crea worktrees auxiliares temporales (§5.4.5 nuevo) o secuencia las tareas.
- La coordinación humana/Lead resuelve el conflicto dentro del equipo; la separación física por equipo resuelve el conflicto entre equipos.

### Compatibilidad con modelo viejo (worktree por rol)

El modelo v1.0.x "worktree por rol" sigue siendo válido para proyectos donde cada rol ejecuta solo (memory-service hoy: BE, DB, FE, etc. cada uno en su worktree). El modelo v1.1.0 "worktree por equipo" es **superset**: un equipo de 1 rol = worktree por rol; un equipo de N roles = worktree compartido por el equipo con coordinación intra-equipo del Lead.

---

## 2. Campo de Aplicación

### Aplica a

- Proyectos VTT con **2+ agentes en paralelo** sobre el mismo repositorio, **sea código o documentación**
- Proyectos donde el TL/Lead necesita operar simultáneamente con agentes (review en vivo)
- Cualquier rol que necesite `.env` propio, `node_modules`, o cualquier estado local independiente del clon base
- **Proyectos de documentación/gobernanza multi-agente** (vtt-setup, futuros) — confirmado por incidente 2026-06-02 (TW-OPS+RA)

### NO aplica a

- Proyectos con un solo agente activo (clon directo es suficiente)
- Repos sin Git

> **Nota histórica:** v1.0.x excluía "proyectos sin ejecución de código (solo documentación)". Esa exclusión fue **invalidada en v1.1.0** por evidencia empírica: el incidente vtt-setup 2026-06-02 demostró que cualquier proyecto multi-agente con cambios concurrentes a archivos compartidos sufre el mismo problema, independientemente de si los archivos son código o docs. La regla real es **multi-agente paralelo**, no "código vs docs".

> **Nota sobre Workflows/Skills/Scripts:** este Protocol referencia 5 Workflows + 2 Skills + 3 Scripts derivados (ver §6). Al momento de publicar v1.0.0, esos artefactos están **pendientes de escribir**. Las referencias se mantienen para que cuando se escriban hagan match. Mientras tanto:
>
> - Cada paso del §5 que invoca un PROCESO incluye el **comando directo** que el Workflow encapsulará — el agente puede ejecutar el Protocol completo sin esperar los Workflows.
> - Cuando los Workflows estén escritos, este Protocol queda intacto — solo se quitan las notas "pendiente".

---

## 3. Responsabilidades

### 3.1 Coordinador humano (Martin)
- Ejecutar setup inicial del proyecto (FASE 1) — una vez por proyecto
- Apertura de sesión diaria (FASE 2) — abrir las N ventanas VSCode necesarias (una por equipo activo)

### 3.2 TL/PM_GOV/Leads (Coordinadores de equipo)
- Onboardear equipo nuevo cuando entra al proyecto (FASE 3) — bajo demanda
- Coordinar internamente los agentes del equipo (asignar tareas secuencialmente, evitar pisadas dentro del mismo worktree de equipo)
- Verificar disciplina de worktree del agente al cerrar tarea (`PROTOCOL-ASG-001 §5.5.5.b`)
- Crear worktrees auxiliares bajo demanda cuando agentes del mismo equipo necesitan paralelo real (`PROTOCOL-MAN-001 §5.1` + §5.4.5 de este Protocol)
- Ejecutar cleanup branch local post-aprobación (`PROTOCOL-ASG-001 §5.5.18`)

### 3.3 Agentes ejecutores (BE/DB/FE/DO/QA/DL/UX/AR/SA/TW-OPS/RA/futuros)
- Operar SIEMPRE en el worktree de su equipo (NUNCA en clon base ni en worktree de otro equipo)
- Coordinar branches con otros agentes del MISMO equipo a través del Lead (no checkout simultáneo sobre branches ajenas)
- Leer execution_manifest antes de empezar (`PROTOCOL-MAN-001 §5.2`)
- Verificar `git status` limpio antes de iniciar nueva tarea
- Reportar al Lead del equipo si el worktree quedó corrupto

### 3.4 PM (Product Manager)
- Cierre final del proyecto — disparar FASE 5 (Cleanup) cuando se cierra el repo

---

## 4. Definiciones

**Worktree:** directorio físico independiente del clon base que comparte `.git/` pero tiene su propia branch checked-out. Permite que múltiples branches coexistan simultáneamente en el filesystem sin conflicto.

**Worktree por equipo (v1.1.0):** estructura `.vtt/worktrees/<repo>-team-<area>/` donde `<area>` identifica el equipo (ej. `normativa`, `research`, `agents`, `backend`, `frontend`). Cada equipo tiene **un** worktree fijo durante todo el proyecto. El Lead del equipo coordina los agentes dentro del worktree.

**Worktree por rol (v1.0.x compat):** estructura `.vtt/worktrees/<repo>-<rol>/` donde `<rol>` ∈ {be, db, fe, do, qa, tl, pm, sa, etc.}. Forma legítima cuando un equipo es de un solo rol. Equivalente a "worktree por equipo de tamaño 1".

**Workspace VSCode dedicado:** archivo `.code-workspace` en `.vtt/workspaces/<repo>-team-<area>.code-workspace` (modelo equipo) o `.vtt/workspaces/<repo>-<rol>.code-workspace` (modelo rol legacy) que abre VSCode con título identificable y `cwd` apuntando al worktree.

**Branch idle:**
- Modelo equipo (v1.1.0): `wt-<repo>-team-<area>` — ej. `wt-vtt-setup-team-normativa`
- Modelo rol (v1.0.x compat): `wt-<repo>-<rol>` — ej. `wt-memory-service-be`
- NO se mergea a main. Sirve solo para que el worktree no quede en estado detached HEAD.

**Branch de tarea:**
- Ejecutores de código: `feature/<TASK_ID>` o `feature/<TASK_ID>-<desc>` — ej. `feature/MS-310`, `feature/VTS-018-mover-init`
- Coordinadores/Leads que suben documentación: `docs/<TASK_ID>-<scope>` — ej. `docs/VTS-019-protocolo-wt-multi-agente`
- Vive en el mismo worktree del equipo hasta que se mergee y se cleanee.

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

5.1.2 Identificar los equipos activos al inicio del proyecto → **[ACTIVIDAD]**
   - Proyecto de código (memory-service típico): equipo backend (TL+BE+DB), equipo frontend (FE+UX), equipo ops (DO+QA), equipo PM/SA
   - Proyecto de docs/gobernanza (vtt-setup): equipo normativa (LEAD_NPL+TW-OPS), equipo research (LEAD_RKL+RA), equipo agentes (LEAD_APL), reviewer PM_GOV (sin worktree — opera en clon base, §7.bis)
   - Equipos que entran más tarde: se onboardean en FASE 3 cuando lleguen

5.1.3 Crear estructura `.vtt/` → **[ACTIVIDAD]**
   ```
   mkdir -p <project_root>/.vtt/{worktrees,workspaces,manifests}
   ```

5.1.4 **Crear UN worktree por cada equipo activo** → **[PROCESO]** → ver `VTT.WORKFLOW-WT-001.001_setup_inicial` *(pendiente de escribir — mientras tanto usar el comando directo abajo)*
   - Invoca: `VTT.SKILL-WT-001` (`action=add_worktree`)
   - Por cada equipo: `git worktree add ../.vtt/worktrees/<repo>-team-<area> -b wt-<repo>-team-<area> origin/main`
   - Ejemplo vtt-setup: `git worktree add ../.vtt/worktrees/vtt-setup-team-normativa -b wt-vtt-setup-team-normativa origin/main`
   - Si el equipo es de un solo rol (modelo v1.0.x compat): `git worktree add ../.vtt/worktrees/<repo>-<rol> -b wt-<repo>-<rol> origin/main`

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

#### 5.4.5 Paralelo real dentro de un equipo (worktree auxiliar)

5.4.5.a Dos agentes del mismo equipo necesitan trabajar realmente en paralelo (no secuencial) → **[CONTEXTO]**
   - Ej. LEAD_NPL escribiendo PROTOCOL-DEP-001 mientras TW-OPS migra un SOP legacy distinto. Ambos en el equipo normativa, ambos tocando archivos en `02.normativa/` pero en sub-rutas diferentes.

5.4.5.b Lead decide si justifica worktree auxiliar → **[DECISIÓN]**
   - Si las branches tocan paths disjuntos → vale la pena. Continuar.
   - Si pueden colisionar → mejor secuenciar, no crear auxiliar.

5.4.5.c Lead crea worktree auxiliar del equipo → **[PROCESO]** → ver `VTT.WORKFLOW-WT-001.004 §5`
   ```
   cd <repo>
   git worktree add ../.vtt/worktrees/<repo>-team-<area>-aux-<NN> -b wt-<repo>-team-<area>-aux-<NN> origin/main
   ```
   - `<NN>` es secuencial (aux-01, aux-02). El Lead lleva el registro.

5.4.5.d Agente del equipo trabaja en el worktree auxiliar para esa tarea específica → **[ACTIVIDAD]**

5.4.5.e Al cerrar la tarea, Lead cleanea el worktree auxiliar → **[ACTIVIDAD]**
   ```
   git worktree remove ../.vtt/worktrees/<repo>-team-<area>-aux-<NN>
   ```

> **Regla:** los worktrees auxiliares son **temporales**. Si un equipo necesita ≥2 worktrees auxiliares permanentes, considerar si en realidad son 2 equipos distintos.

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

### 7.2 Un equipo = un worktree fijo (NO por tarea, NO por agente del equipo)

Si un agente termina MS-X y empieza MS-Y, **usa el MISMO worktree del equipo**, solo cambia branch:

```
✅ Correcto:
  cd .vtt/worktrees/vtt-setup-team-normativa   # MISMO worktree del equipo
  git checkout -b docs/VTS-Y-scope origin/main

❌ Incorrecto:
  git worktree add .vtt/worktrees/vtt-setup-team-normativa-VTS-Y  # NO crear nuevo por tarea
  git worktree add .vtt/worktrees/vtt-setup-tw-ops              # NO crear por agente individual del equipo
```

### 7.3 Una ventana VSCode = un equipo = N sesiones Claude (una por agente del equipo)

NO abrir 2 chats Claude del MISMO agente en la misma ventana. Pero SÍ pueden abrirse varias sesiones Claude **de distintos agentes del mismo equipo** apuntando al MISMO worktree de equipo, coordinadas por el Lead. Ejemplo: ventana `vtt-setup-team-normativa` puede tener sesión LEAD_NPL + sesión TW-OPS — pero el Lead coordina las branches para que no se pisen (asignación secuencial, no checkout concurrente).

Para evitar pisadas dentro de un equipo:
- Solo UN agente del equipo tiene `task_in_progress` por vez.
- El Lead asigna la siguiente tarea solo cuando la anterior está en `task_in_review` o terminada.
- Si dos tareas del mismo equipo deben hacerse en paralelo de verdad → §5.4.5 (worktree auxiliar del equipo).

### 7.4 Worktrees NO van a git

La carpeta `.vtt/` está en `.gitignore`. Es infraestructura local, no se commitea.

### 7.5 Branch idle del equipo NUNCA se mergea

`wt-<repo>-team-<area>` (modelo equipo) o `wt-<repo>-<rol>` (modelo rol legacy). Es solo para que el worktree no quede detached. Si alguien intenta hacer PR de `wt-vtt-setup-team-normativa` → rechazar.

### 7.bis Reviewers/PMs operan en clon base (NO en worktree)

PM_GOV, TL Reviewer y otros roles puramente de revisión **NO usan worktree** — operan directamente en el clon padre. Razones:
- No producen branches `feature/*` ni `docs/*` ellos mismos (revisan las branches de otros).
- Cuando excepcionalmente commitean (HOs, decisiones, releases), el cambio es a paths que no se solapan con worktrees de equipos.
- Tener su propio worktree multiplica overhead sin beneficio.

Excepción: si un Lead/Reviewer EJECUTA directo (no delega), entonces actúa como ejecutor del equipo correspondiente y opera en el worktree del equipo.

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
| 1.1.0 | 2026-06-02 | PM_GOV (bajo dirección de Martin) | **Minor bump — ampliación de scope y cambio de modelo.** Origen: incidente vtt-setup 2026-06-02 (agentes TW-OPS y RA se pisaron en proyecto de docs — exactamente el mismo patrón que PROC-COORD-01 que originó el Protocol, pero en docs). **Cambios:** (1) Título "por Rol" → "por Equipo" + propósito ampliado a cualquier proyecto multi-agente (código o docs). (2) §2 NUEVO: aplica explícitamente a proyectos de documentación/gobernanza multi-agente (vtt-setup, futuros). Eliminada exclusión "solo documentación" — invalidada por evidencia empírica. (3) §1 NUEVO bloque "Modelo de equipos" con tabla de mapeo equipo→Lead→ejecutores→worktree para memory-service y vtt-setup. (4) §1 NUEVO bloque "Coordinación intra-equipo" — el Lead asigna secuencialmente dentro del worktree del equipo. (5) §1 NUEVO bloque "Compatibilidad con modelo viejo" — v1.0.x "por rol" sigue válido como caso especial (equipo de 1 rol). (6) §3.2 ampliado a TL/PM_GOV/Leads como coordinadores de equipo. (7) §3.3 incluye TW-OPS/RA/futuros. (8) §4 NUEVO definición "Worktree por equipo" + branch idle `wt-<repo>-team-<area>` + branch tarea `docs/<TASK_ID>-<scope>` para coordinadores. (9) §5.1.2 ahora habla de "equipos activos" con ejemplos para proyectos de docs. (10) §5.1.4 comando actualizado a `team-<area>`. (11) §5.4.5 NUEVO: paralelo real dentro de un equipo con worktree auxiliar temporal `<area>-aux-<NN>`. (12) §7.2 actualizada al modelo equipo. (13) §7.3 amplía a "N sesiones Claude del MISMO equipo en el MISMO worktree" coordinadas por el Lead. (14) §7.5 actualizada al nuevo patrón de branch idle. (15) §7.bis NUEVO: reviewers/PMs operan en clon base, no en worktree. Aplicación inmediata: vtt-setup elimina `vtt-setup-tw-ops` y `vtt-setup-ra` y crea `vtt-setup-team-normativa` (NPL+TW-OPS) + `vtt-setup-team-research` (RKL+RA) + `vtt-setup-team-agents` (APL). |

---

**Fin del Protocol.** Para implementar, ver los 5 Workflows (`VTT.WORKFLOW-WT-001.001..005`), 2 Skills (`VTT.SKILL-WT-001`, `VTT.SKILL-WT-002`) y 3 Scripts (`VTT.SCRIPT-WT-001`, `VTT.SCRIPT-WT-002`, `VTT.SCRIPT-WT-003`).
