# VTT.WORKFLOW-WT-001.002 — Apertura de Sesión Diaria

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-WT-001.002` |
| **Pertenece a** | `VTT.PROTOCOL-WT-001` §5.2 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-05-18 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | Coordinador humano (apertura) + cada agente (verificación dentro de su ventana) |
| **Tipo** | [PROCESO] sub-procedimiento — invocado por PROTOCOL-WT-001 §5.2 |
| **Frecuencia** | Diaria |

---

## 1. Propósito

Abrir las N ventanas VSCode necesarias para el trabajo del día, una por rol activo, con verificación de `git status` limpio en cada worktree antes de recibir asignaciones.

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `project_root` | path absoluto | Estructura del proyecto | sí | Ej. `c:/.../memory-service` |
| `roles_hoy` | array de roles | Plan del día del Coordinador | sí | Subset de los `roles_activos` del proyecto |

---

## 3. Precondiciones

- FASE 1 (Setup inicial — `WORKFLOW-WT-001.001`) ya ejecutada
- `.vtt/workspaces/<repo>-<rol>.code-workspace` existe para cada rol que se va a abrir
- Coordinador tiene VSCode instalado

---

## 4. Reglas del Workflow

- **R1:** Una ventana VSCode = un rol = una sesión Claude Code
- **R2:** El agente verifica `git status` ANTES de declarar el worktree listo
- **R3:** Si encuentra estado sucio o branch inesperada → ejecutar §5.2.4.bis del Protocol (3 casos)
- **R4:** Si encuentra worktree corrupto → escalar al TL (§5.4.4)

---

## 5. Pasos

### Paso 1 — Coordinador identifica roles del día

```
roles_hoy = [tl, be, do]      # ejemplo
```

### Paso 2 — Por cada rol, abrir ventana VSCode

Por cada rol en `roles_hoy`:

```bash
# Doble click en el archivo (o desde terminal):
code <project_root>/.vtt/workspaces/<repo>-<rol>.code-workspace
```

Resultado: ventana VSCode abierta con:
- Folder = worktree del rol
- Título de ventana = "<ROL_UPPER> - <Rol Descripción> | <Proyecto>"
- cwd del terminal integrado = worktree del rol

### Paso 3 — Por cada ventana, agente abre chat Claude Code

Acción manual del Coordinador:
- Abrir paleta de comandos (Ctrl+Shift+P)
- "Claude Code: Start Session" (o equivalente)
- Esperar a que cargue el chat

### Paso 4 — Agente verifica su worktree (DENTRO de su ventana)

```bash
cd .vtt/worktrees/<repo>-<rol>
pwd
git status
git branch --show-current
```

### Paso 5 — Decisión por estado del worktree (3 casos)

→ ver `PROTOCOL-WT-001 §5.2.4.bis` para detalle de cada caso

#### Caso A — Branch idle activa, working tree limpio

```
Branch: wt-<repo>-<rol>
Status: nothing to commit, working tree clean
```

**Acción:** ninguna. Worktree listo para recibir tarea. Reportar al Coordinador: "Agente <ROL> listo".

#### Caso B — Branch `feature/<TASK_ID>` de tarea YA mergeada

```
Branch: feature/MS-XXX
Status: working tree clean (pero la branch ya fue mergeada en remote)
```

**Acción — cleanup retroactivo:**

```bash
git fetch origin
git checkout main
git pull origin main
git branch -d feature/<TASK_ID>        # debe funcionar si está fully merged
git checkout wt-<repo>-<rol>
```

Si `git branch -d` falla:
- Verificar en GitHub que el PR sí fue mergeado
- Si sí: `git pull` (sync) y reintentar
- Si NO: la tarea no estaba mergeada — caso C

Reportar al TL: "Cleanup retroactivo de <TASK_ID> ejecutado por <ROL>".

#### Caso C — Branch `feature/<TASK_ID>` de tarea EN CURSO

```
Branch: feature/MS-YYY
Status: depende — puede ser limpio o sucio
```

¿Mi tarea de hoy es la misma `<TASK_ID>`? → **[DECISIÓN]**

- **Sí** → quedarse en esa branch, continuar el trabajo
- **No** → ANTES de cambiar branch, resolver cambios pendientes:
  ```
  # Si git status muestra cambios uncommitted, ver §5.4.3 del Protocol:
  # Opción A — commit WIP
  git add -A && git commit -m "WIP: pause <TASK_ID_actual>" && git push
  # Opción B — stash
  git stash push -m "<TASK_ID_actual>-pause"
  # Opción C — abandonar (cuidado, perdés cambios)
  git checkout -- .
  ```
  Después, ir al Caso A para arrancar limpio.

### Paso 6 — Reportar al Coordinador

Cada agente reporta estado:
```
[BE]  Worktree OK — branch wt-backend-be — ready
[DO]  Cleanup retroactivo de MS-XXX ejecutado — ready
[TL]  Caso C — quedó en feature/MS-YYY (tarea en review) — continúa
```

---

## 6. Outputs

| Nombre | Tipo | Destino | Descripción |
|---|---|---|---|
| N ventanas VSCode abiertas | UI | desktop del Coordinador | Una por rol activo del día |
| N sesiones Claude Code activas | UI | dentro de cada ventana | Una por ventana |
| Worktrees verificados | estado git | local | Cada uno en estado conocido (A/B/C) |
| Reporte de estado al Coordinador | mensaje texto | chat coordinador | "[ROL] estado" para cada agente |

---

## 7. Validación de salida

```bash
# Para cada rol activo del día:
for rol in roles_hoy:
    cd <project_root>/.vtt/worktrees/<repo>-$rol
    git status
    git branch --show-current
# Esperado: todos en Caso A, B (post-cleanup) o C (con tarea en curso explícita)
```

- [ ] N ventanas VSCode abiertas con títulos correctos
- [ ] N sesiones Claude activas
- [ ] Cada worktree en estado conocido
- [ ] Reporte de estado generado al Coordinador

---

## 8. Errores comunes

| Síntoma | Causa probable | Solución |
|---|---|---|
| Ventana VSCode no abre nada | `.code-workspace` con JSON mal formado | Validar JSON con `python -m json.tool < <archivo>.code-workspace` |
| Título de ventana genérico ("Untitled") | Falta `window.title` en `.code-workspace` | Regenerar con WORKFLOW-WT-001.001 Paso 5 |
| `git status` muestra archivos de OTRO worktree | Agente hizo `cd` fuera de su worktree | Volver a su worktree — escalar al TL si es recurrente |
| Caso B falla con "branch not fully merged" | Branch local desincronizada con remote | `git fetch origin --prune` + reintentar |
| Caso C — agente NO sabe cuál es su tarea de hoy | Falta asignación de VTT | Coordinador asigna primero, después abrir sesión |
| 2 ventanas para el mismo rol abiertas | Coordinador abrió dos veces | Cerrar una — viola R1 (una ventana por rol) |

---

## 9. Skills invocadas

- `VTT.SKILL-WT-001` — `action=verify_worktree_status` (Paso 4)
- `VTT.SKILL-AUTH-01` (legacy) — el agente puede necesitar JWT para verificar tarea en VTT (Caso C)

---

## 10. Reglas Nivel 0 aplicables

| Regla | Razón |
|---|---|
| `RULE-WT-001` Worktree policy | El agente verifica que está en su worktree correcto |
| `RULE-AGENT-001 v2.0` Worktree por rol | Una ventana = un rol |

---

## 11. Changelog

| Versión | Fecha | Editor | Cambios |
|---|---|---|---|
| 1.0.0 | 2026-05-18 | PM Martin Rivas | Versión inicial. Formaliza el proceso de "abrir el día" en proyectos multi-rol. Incluye los 3 casos de §5.2.4.bis del Protocol. |
