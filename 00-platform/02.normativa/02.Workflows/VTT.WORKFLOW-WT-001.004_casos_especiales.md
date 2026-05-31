# VTT.WORKFLOW-WT-001.004 — Casos Especiales de Worktrees

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-WT-001.004` |
| **Pertenece a** | `VTT.PROTOCOL-WT-001` §5.4 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-05-18 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | Agente ejecutor (sub-procedimientos §1, §2, §3); TL (sub-procedimientos §1.c, §4) |
| **Tipo** | [PROCESO] sub-procedimiento — invocado por PROTOCOL-WT-001 §5.4 |
| **Frecuencia** | Bajo demanda — cuando se presenta uno de los 4 casos |

---

## 1. Propósito

Cubrir los 4 casos especiales que NO encajan en la operación normal (FASE 2 del Protocol):

1. **Tarea toca múltiples repos** — agente necesita escribir en repo distinto al suyo
2. **Branch base NO es main** — tarea depende de otra branch aún no mergeada
3. **Cambios sin commitear al cambiar de tarea** — pausar trabajo en curso
4. **Worktree corrupto** — recuperación

Cada sub-procedimiento es independiente. NO se invocan juntos.

---

## 2. Inputs (estrictos)

Varían por sub-procedimiento. Cada §X lista los suyos.

---

## 3. Precondiciones generales

- WORKFLOW-WT-001.001 ejecutado (existe `.vtt/worktrees/<repo>-<rol>/`)
- Agente conoce su rol y worktree principal

---

## 4. Reglas del Workflow

- **R1:** NO inventar workflows nuevos para casos que ya estén aquí
- **R2:** Documentar el caso en devlog si tiene impacto en el cierre de la tarea
- **R3:** Casos §1.c, §4 requieren acción del TL — agente NO los ejecuta solo

---

## 5. Sub-procedimientos

### §1. Tarea toca múltiples repos

**Quién:** agente (lectura), TL (escritura — Paso .c).

**Contexto típico:** BE Engineer trabajando en `feature/MS-XXX` en su worktree `backend-be`, pero la tarea le pide tocar también un devlog que vive en otro repo (`project`).

#### Paso §1.a — Identificar repo destino

```
Repo principal del agente: backend (worktree backend-be)
Repo adicional necesario: project
```

#### Paso §1.b — Decisión: ¿necesita escribir o solo leer?

→ **[DECISIÓN]**

- **Solo leer** (consultar archivo, ver código) → leer directo del clon base sin checkout, NO afecta branch. Saltar al Paso §1.e.
- **Escribir** (modificar archivo, commitear) → continuar a §1.c

#### Paso §1.c — TL crea worktree auxiliar temporal

→ Acción del TL (no del agente)

```bash
cd <project_root>/<otro_repo_full_name>
git fetch origin
git worktree add ../.vtt/worktrees/<otro_repo>-<rol>-aux -b wt-<otro_repo>-<rol>-aux origin/main
```

Nota del naming: sufijo `-aux` distingue del worktree principal del rol (si lo hubiera).

→ invoca **`VTT.SKILL-WT-001`** con (`action=add_worktree`, `repo=<otro_repo>`, `rol=<rol>-aux`)

#### Paso §1.d — Agente trabaja en worktree auxiliar para esa parte

```bash
cd <project_root>/.vtt/worktrees/<otro_repo>-<rol>-aux
git checkout -b feature/<TASK_ID>-aux origin/main
# Hacer los cambios en este worktree
git add . && git commit -m "[<TASK_ID>] cambios en <otro_repo>"
git push origin feature/<TASK_ID>-aux
gh pr create --base main
```

El agente termina con DOS PRs por la misma tarea: uno en su repo principal + uno en el auxiliar.

#### Paso §1.e — Al cerrar tarea, TL cleanea worktree auxiliar

```bash
cd <project_root>/<otro_repo_full_name>
git worktree remove ../.vtt/worktrees/<otro_repo>-<rol>-aux
git branch -D wt-<otro_repo>-<rol>-aux
```

→ invoca **`VTT.SKILL-WT-001`** con (`action=remove_worktree`, `worktree_path=...`)

#### Paso §1.f — Documentar en devlog del agente

Devlog entry tipo `decision`:
```
"Tarea tocó múltiples repos. Worktree auxiliar creado en <otro_repo>-<rol>-aux.
PRs: #X (repo principal) + #Y (repo auxiliar). Worktree aux limpiado al cerrar."
```

---

### §2. Branch base de la tarea NO es main

**Quién:** agente ejecutor.

**Contexto típico:** MS-310 depende de MS-309 que aún está en `task_in_review` (no mergeada a main).

#### Paso §2.a — Verificar que la branch base existe en remote

```bash
cd <project_root>/.vtt/worktrees/<repo>-<rol>
git fetch origin
git ls-remote --heads origin feature/MS-309
# Debe retornar un SHA
```

Si NO existe → escalar al TL: branch padre no está pusheada.

#### Paso §2.b — Crear branch desde la branch padre

```bash
git checkout -b feature/MS-310 origin/feature/MS-309
git status
# Working tree limpio basado en MS-309
```

#### Paso §2.c — Trabajar normalmente

Commits, push, etc. La branch incluirá el código de MS-309 hasta que MS-309 mergee.

#### Paso §2.d — Cuando MS-309 mergee a main, rebase

```bash
git fetch origin
git rebase origin/main
# Resolver conflictos si los hay
git push origin feature/MS-310 --force-with-lease
```

Esto deja `feature/MS-310` rebased sobre main, sin el commit de MS-309 (ya parte de main).

#### Paso §2.e — PR target main (NO feature/MS-309)

```bash
gh pr create --base main --head feature/MS-310
```

> **Regla:** el PR siempre apunta a `main`. Si lo apuntas a `feature/MS-309` y esa branch desaparece, el PR queda huérfano.

#### Paso §2.f — Documentar en devlog

```
"Tarea creada desde feature/MS-309 (aún no mergeada). Rebase ejecutado tras
merge de MS-309 a main. PR target: main."
```

---

### §3. Cambios sin commitear al cambiar de tarea

**Quién:** agente ejecutor.

**Contexto típico:** agente está trabajando en MS-X, le piden urgente que arranque MS-Y, MS-X tiene código sin commitear.

#### Paso §3.a — Verificar estado

```bash
cd <project_root>/.vtt/worktrees/<repo>-<rol>
git status
# Esperado: muestra modified files
```

#### Paso §3.b — Elegir estrategia → **[DECISIÓN]**

| Estrategia | Cuándo usar | Comando |
|---|---|---|
| **A — Commit WIP** | Vas a volver a MS-X pronto, querés preservar progreso en remote | Ver §3.c |
| **B — Stash** | Es muy temporal (1-2 horas), no querés ensuciar git log | Ver §3.d |
| **C — Abandonar** | Los cambios eran exploratorios, no sirven | Ver §3.e |

#### Paso §3.c — Opción A: Commit WIP

```bash
git add -A
git commit -m "WIP: pause MS-X — switching to MS-Y

No estaba listo para entrega. Trabajo pendiente:
- [pendiente] X
- [pendiente] Y

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
git push origin feature/MS-X
```

Después:
```bash
git checkout main
git pull
git checkout -b feature/MS-Y origin/main
```

Al volver a MS-X:
```bash
git checkout feature/MS-X
git pull origin feature/MS-X
git reset HEAD~1     # opcional — deshace el WIP commit pero mantiene los archivos
# o continuar desde el WIP commit y commitear encima
```

#### Paso §3.d — Opción B: Stash

```bash
git stash push -m "MS-X pause for MS-Y"
git checkout main && git pull
git checkout -b feature/MS-Y origin/main
```

Al volver a MS-X:
```bash
git checkout feature/MS-X
git stash list
# stash@{0}: On feature/MS-X: MS-X pause for MS-Y
git stash pop
```

#### Paso §3.e — Opción C: Abandonar

```bash
# Cuidado — pierde cambios irreversiblemente
git checkout -- .       # descarta cambios en tracked files
git clean -fd           # borra untracked files (incluyendo directorios)
git checkout main && git pull
git checkout -b feature/MS-Y origin/main
```

#### Paso §3.f — Documentar en devlog (de MS-X)

```
"Trabajo en MS-X pausado por urgencia de MS-Y. Estrategia: [A/B/C]. <detalle>."
```

---

### §4. Worktree corrupto

**Quién:** TL (con asistencia del agente para preservar trabajo).

**Contexto típico:** agente reporta error inusual al hacer `git status` o `git checkout` — HEAD detached, branch missing, working tree inaccesible.

#### Paso §4.a — Diagnóstico

```bash
cd <project_root>/.vtt/worktrees/<repo>-<rol>
git worktree list             # ¿aparece este worktree?
git status                    # ¿qué dice exactamente?
ls -la .git/                  # ¿hay archivo .git con path al worktree real?
ls -la <project_root>/<repo>/.git/worktrees/
# El último comando lista los metadatos de TODOS los worktrees del repo
```

#### Paso §4.b — Preservar trabajo no committeado

Si el agente tenía trabajo en curso:

```bash
# Intentar stash primero
cd <project_root>/.vtt/worktrees/<repo>-<rol>
git stash push -m "Pre-corruption-recovery"

# Si stash falla, copiar archivos manualmente a /tmp
mkdir -p /tmp/<rol>-recovery
cp -r .  /tmp/<rol>-recovery/         # incluye los cambios
```

#### Paso §4.c — Identificar branches que vivían en el worktree

```bash
cd <project_root>/<repo_full_name>
git branch -a | grep "<repo>-<rol>"
# Listado de branches del rol
```

Anotar las branches que necesitan preservarse (típicamente: feature/<TASK_ID_actual>).

#### Paso §4.d — Remover worktree corrupto (forzado)

```bash
cd <project_root>/<repo_full_name>
git worktree remove --force ../.vtt/worktrees/<repo>-<rol>
# Si falla, manual:
git worktree prune
rm -rf <project_root>/.vtt/worktrees/<repo>-<rol>
```

#### Paso §4.e — Recrear worktree

```bash
cd <project_root>/<repo_full_name>
git fetch origin

# Si la branch idle wt-<repo>-<rol> ya existe, reusar
if git rev-parse --verify wt-<repo>-<rol> >/dev/null 2>&1; then
    git worktree add ../.vtt/worktrees/<repo>-<rol> wt-<repo>-<rol>
else
    git worktree add ../.vtt/worktrees/<repo>-<rol> -b wt-<repo>-<rol> origin/main
fi
```

→ invoca **`VTT.SKILL-WT-001`** con (`action=add_worktree`, ...)

#### Paso §4.f — Agente restaura su trabajo

```bash
cd <project_root>/.vtt/worktrees/<repo>-<rol>

# Si tenía branch de tarea en curso, restaurar
git checkout feature/<TASK_ID_actual>

# Aplicar el stash o copiar de /tmp/<rol>-recovery
git stash pop
# o
cp -r /tmp/<rol>-recovery/* .
git status
# Confirmar que los cambios reaparecieron
```

#### Paso §4.g — Limpiar /tmp si se usó

```bash
rm -rf /tmp/<rol>-recovery
```

#### Paso §4.h — Documentar incidente

Devlog del proyecto (no de tarea específica):
```
"Worktree <repo>-<rol> corrupto. Recreado por TL. Trabajo restaurado vía
[stash/copy]. Causa probable: <hipótesis>."
```

Si el caso se repite → reportar en `knowledge/platform-feedback/`.

---

## 6. Outputs

Varían por sub-procedimiento:

| Sub-procedimiento | Output principal |
|---|---|
| §1 Múltiples repos | Worktree auxiliar temporal + PR adicional + cleanup post-tarea |
| §2 Branch base no-main | Branch `feature/<TASK_ID>` basada en parent + PR a main + devlog explicativo |
| §3 Pausar tarea | Estado preservado (commit WIP / stash / abandono) + devlog |
| §4 Recovery | Worktree recreado + trabajo restaurado + devlog del incidente |

---

## 7. Validación de salida

Por sub-procedimiento:

### §1
- [ ] Worktree auxiliar removido tras cerrar tarea
- [ ] Ambos PRs (principal + auxiliar) mergeados
- [ ] Devlog documentado

### §2
- [ ] PR target = main (NO la branch padre)
- [ ] Rebase ejecutado tras merge del parent
- [ ] Devlog documentado

### §3
- [ ] Estrategia ejecutada exitosamente (commit WIP / stash / abandono)
- [ ] Branch nueva de la tarea siguiente creada desde main limpio
- [ ] Al volver a la pausada, trabajo restaurado

### §4
- [ ] Worktree recreado y accesible
- [ ] Trabajo restaurado verificable (`git status` muestra los cambios)
- [ ] Devlog del incidente registrado

---

## 8. Errores comunes

| Síntoma | Causa probable | Solución |
|---|---|---|
| §1.c — `git worktree add` falla por path ya existente | Cleanup previo falló | `git worktree prune` antes de retry |
| §2.d — `rebase` con muchos conflictos | Parent branch divergió mucho | Considerar `merge` en vez de `rebase`. Coordinar con TL. |
| §3.d — `stash pop` con conflicto | El stash y la branch nueva tocan mismos archivos | Resolver manualmente o `git stash drop` si los cambios ya no sirven |
| §4.b — `cp -r .` sobre directorio destino existente | Archivos duplicados o conflictos | Cleanup destino primero o usar `rsync` |
| §4.d — `git worktree remove` falla con "is locked" | El worktree tiene lock file | `rm <project_root>/<repo>/.git/worktrees/<wt>/locked` |
| Cualquier — el agente NO documenta en devlog | Olvido | TL recuerda en review |

---

## 9. Skills invocadas

- `VTT.SKILL-WT-001` — `action=add_worktree` (§1.c, §4.e), `action=remove_worktree` (§1.e, §4.d)
- `VTT.SKILL-AUTH-01` (legacy) — si los pasos requieren VTT API

---

## 10. Reglas Nivel 0 aplicables

| Regla | Razón |
|---|---|
| `RULE-WT-001` Worktree policy | Mantenida en todos los sub-procedimientos |
| `RULE-AGENT-001 v2.0` Worktree por rol | §1 crea worktree `aux` separado, no rompe la regla |

---

## 11. Changelog

| Versión | Fecha | Editor | Cambios |
|---|---|---|---|
| 1.0.0 | 2026-05-18 | PM Martin Rivas | Versión inicial. Consolida los 4 casos especiales del Protocol §5.4 en un solo Workflow (decisión validada con PM: ratio de tokens vs Workflows separados). |
