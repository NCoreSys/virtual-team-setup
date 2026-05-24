# VTT.WORKFLOW-WT-001.005 — Cleanup Final del Proyecto

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-WT-001.005` |
| **Pertenece a** | `VTT.PROTOCOL-WT-001` §5.5 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-05-18 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | TL principal con autorización del PM |
| **Tipo** | [PROCESO] sub-procedimiento — invocado por PROTOCOL-WT-001 §5.5 |
| **Frecuencia** | UNA VEZ al cerrar el proyecto |

---

## 1. Propósito

Cierre completo de la infraestructura `.vtt/` del proyecto: inventario y resolución de branches pendientes, remove de worktrees, delete de branches idle, archivo opcional de `.vtt/`. Garantiza cierre limpio sin dejar deuda silenciosa.

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `project_root` | path absoluto | Proyecto a cerrar | sí | Ej. `c:/.../memory-service` |
| `pm_authorization` | comment_id | PM aprobó cleanup en VTT | sí | Para audit trail |
| `decisiones_branches` | array de objetos | TL decide caso por caso | sí | Para cada branch `feature/*` o `fix/*` pendiente: acción A/B/C |
| `archivar_vtt` | bool | Decisión del TL | sí | Si `true`, generar tarball antes de borrar |

### Ejemplo de `decisiones_branches`

```json
[
  { "branch": "feature/MS-300", "task_status": "task_approved", "accion": "A", "motivo": "PR no mergeado por olvido" },
  { "branch": "feature/MS-301", "task_status": "task_rejected", "accion": "B", "motivo": "Decidió no implementarse" },
  { "branch": "fix/MS-302",     "task_status": "task_in_progress", "accion": "C", "motivo": "Deuda viva para R2 — preservar" }
]
```

---

## 3. Precondiciones

- PM autorizó cleanup final (`pm_authorization` registrado)
- NO hay tareas con status `task_in_review` activas (todas resueltas: approved, rejected definitivo, o cancelled)
- TL verificó §5.5.2 del Protocol (no hay activity reciente en VTT)
- Todos los Agentes han cerrado sus ventanas VSCode (`.vtt/workspaces/` no abierto)

---

## 4. Reglas del Workflow

- **R1:** Ninguna branch `feature/*` o `fix/*` se borra silenciosamente — cada una requiere decisión documentada
- **R2:** Branches preservadas (Acción C) NO se borran y se documentan en `_archive/branches_pending_phase2.md`
- **R3:** El archivo `.vtt/` se preserva como tarball SI `archivar_vtt=true`
- **R4:** El CLOSURE final del proyecto se postea en VTT como audit trail

---

## 5. Pasos

### Paso 1 — Verificar PM authorization

```bash
# Verificar que el comment_id existe y es del PM
curl -s "http://77.42.88.106:3000/api/comments/$PM_AUTH_COMMENT_ID" \
  -H "Authorization: Bearer $TOKEN"
# Esperado: comment del PM autorizando cleanup
```

Si no hay authorization → **STOP**. NO continuar.

### Paso 2 — Verificar que no hay tareas activas

```bash
# Por proyecto, contar tareas en task_in_review o task_in_progress
curl -s "http://77.42.88.106:3000/api/projects/<PROJECT_ID>/tasks?status=task_in_review" \
  -H "Authorization: Bearer $TOKEN" | jq '.data | length'
# Esperado: 0
```

Si hay tareas activas → **STOP** y notificar al PM.

### Paso 3 — Inventario de branches pendientes

Para cada repo del proyecto:

```bash
cd <project_root>/<repo_full_name>
git fetch origin --prune

# Branches pendientes (NO mergeadas a main)
git branch -a --no-merged origin/main | grep -E "(feature|fix)/" | sort -u
```

Output esperado:
```
feature/MS-300
feature/MS-301
fix/MS-302
...
```

Por cada branch, consultar su status en VTT:
```bash
TASK_ID=$(echo "$BRANCH" | sed 's|^.*[/-]||')
curl -s "http://77.42.88.106:3000/api/tasks/$TASK_ID" \
  -H "Authorization: Bearer $TOKEN" | jq '.data.statusCode'
```

### Paso 4 — Por cada branch, ejecutar acción A/B/C

Según `decisiones_branches`:

#### Acción A — Mergear

```bash
git checkout main
gh pr create --title "<branch> close" --base main --head <branch>
# PM aprueba PR — auto-merge si pasa CI
gh pr merge <PR_NUM> --merge
```

#### Acción B — Cerrar wontfix

```bash
# Postear comment en VTT cerrando la tarea
curl -s -X POST "http://77.42.88.106:3000/api/tasks/$TASK_ID/comments" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"message": "Tarea cerrada al final del proyecto. Motivo: <motivo>. Branch <branch> NO mergeada.", "type": "wontfix"}'

# Cerrar PR sin mergear
gh pr close <PR_NUM> --comment "Project closure — wontfix per TL decision."

# Borrar branch en remote
git push origin --delete <branch>
```

#### Acción C — Preservar para fase 2

```bash
# Solo agregar al registro — NO borrar
echo "- $BRANCH | task_status=$STATUS | motivo=$MOTIVO" \
  >> <project_root>/_archive/branches_pending_phase2.md
```

Generar el archivo de registro si no existe:

```markdown
# Branches preservadas para Fase 2 — <Proyecto>

Fecha de cierre del proyecto: <YYYY-MM-DD>
TL responsable: <nombre>
PM authorization: <comment_id>

## Branches

- branch | task_status | motivo
- ...

## Cómo continuar en fase 2

Cada branch listada arriba debe:
1. Rebase contra main al inicio de fase 2
2. Re-evaluar contra contexto actualizado
3. Crear nueva tarea VTT (no reutilizar TASK_ID viejo)
```

→ invoca **`VTT.SKILL-WT-001`** con (`action=close_branch_wontfix`) para Acción B
→ invoca **`VTT.SKILL-WT-001`** con (`action=archive_branch_for_phase2`) para Acción C

### Paso 5 — Cleanup masivo de worktrees

```bash
cd <project_root>

# Listar worktrees activos
git worktree list

# Por cada worktree (excepto clon base):
for WT in .vtt/worktrees/*/; do
    REPO=$(echo $WT | cut -d/ -f3 | cut -d- -f1)
    cd <project_root>/<repo_full_name_for_$REPO>
    git worktree remove ../.vtt/worktrees/$(basename $WT)
done
```

→ invoca **`VTT.SCRIPT-WT-003`** (`cleanup_worktrees.py`) para automatizar

### Paso 6 — Borrar branches idle

Por cada repo:

```bash
cd <project_root>/<repo_full_name>
git branch | grep "^  wt-" | while read BR; do
    git branch -D $BR
done
git push origin --delete wt-<repo>-<rol>  # también en remote (si fueron pusheadas)
```

### Paso 7 — Verificar cleanup completo

```bash
# Worktree list debe mostrar SOLO el clon base
cd <project_root>/<repo_full_name>
git worktree list
# Esperado: 1 línea (el clon base)

# No quedan branches idle
git branch | grep "^  wt-"
# Esperado: ninguna

# Branches pendientes — solo las de Acción C preservadas
git branch -a --no-merged origin/main | grep -E "(feature|fix)/"
# Esperado: solo las branches que decidiste preservar
```

### Paso 8 — Archivar `.vtt/` (opcional)

Si `archivar_vtt=true`:

```bash
cd <project_root>
FECHA=$(date +%Y%m%d)
tar czf .vtt-archive-$FECHA.tar.gz .vtt/
mv .vtt-archive-$FECHA.tar.gz _archive/
rm -rf .vtt/
```

Si `archivar_vtt=false`:

```bash
rm -rf <project_root>/.vtt/
```

### Paso 9 — Postear CLOSURE final en VTT

```bash
SUMMARY=$(cat <<EOF
# CLOSURE — <Proyecto>

Cleanup final ejecutado: $(date +%Y-%m-%d)
TL: <nombre>
PM authorization: $PM_AUTH_COMMENT_ID

## Worktrees removidos: N
## Branches procesadas: M total
- Acción A (mergeadas): X
- Acción B (wontfix): Y
- Acción C (preservadas para fase 2): Z

## Branches preservadas
Ver: _archive/branches_pending_phase2.md

## .vtt/ archivado
$([ "$ARCHIVAR_VTT" = "true" ] && echo "_archive/.vtt-archive-$FECHA.tar.gz" || echo "no archivado")

## Estado final
- ✅ git worktree list = clon base solamente
- ✅ Branches idle wt-* eliminadas
- ✅ Branches pendientes documentadas
- ✅ Proyecto en modo archived
EOF
)

curl -s -X POST "http://77.42.88.106:3000/api/projects/<PROJECT_ID>/comments" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"message\": $(echo "$SUMMARY" | jq -Rs .), \"type\": \"closure\"}"
```

### Paso 10 — Commit del `_archive/`

```bash
cd <project_root>/<repo_principal>
git checkout main
git pull
git add _archive/branches_pending_phase2.md
git add _archive/.vtt-archive-*.tar.gz  # si se archivó
git commit -m "[CLOSURE] <Proyecto> — cleanup final + archive

- N worktrees removidos
- M branches procesadas (A/B/C: X/Y/Z)
- .vtt/ archivado (si aplica)

PM authorization: $PM_AUTH_COMMENT_ID

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

git push origin main
```

> Esto sí es commit directo a main porque el cleanup final NO sigue el flujo normal de PR — es operación administrativa autorizada por el PM.

---

## 6. Outputs

| Nombre | Tipo | Destino | Descripción |
|---|---|---|---|
| Worktrees removidos | filesystem | local | Ninguno queda activo |
| Branches idle borradas | git | local + remote | Limpieza completa de `wt-*` |
| `_archive/branches_pending_phase2.md` | archivo md | repo | Registro de branches preservadas (Acción C) |
| `_archive/.vtt-archive-<fecha>.tar.gz` | tarball | repo (opcional) | Snapshot de `.vtt/` antes de borrar |
| CLOSURE comment en VTT | record VTT | proyecto | Audit trail del cierre |
| Commit en main | git | repo | Registra el cleanup |

---

## 7. Validación de salida

```bash
# Check 1: no quedan worktrees activos
cd <project_root>/<repo_principal>
git worktree list | wc -l
# Esperado: 1 (solo clon base)

# Check 2: no quedan branches idle
git branch -a | grep "wt-" | wc -l
# Esperado: 0

# Check 3: .vtt/ removido
ls -d <project_root>/.vtt/ 2>/dev/null
# Esperado: directorio no existe

# Check 4: archivo de Fase 2 existe si hay branches preservadas
ls <project_root>/_archive/branches_pending_phase2.md
# Esperado: existe (si Z > 0)

# Check 5: CLOSURE comment posteado
curl -s "http://77.42.88.106:3000/api/projects/<PROJECT_ID>/comments?type=closure" \
  -H "Authorization: Bearer $TOKEN" | jq '.data | length'
# Esperado: >= 1
```

- [ ] PM authorization verificada
- [ ] No hay tareas activas en VTT
- [ ] Inventario de branches generado
- [ ] Cada branch tiene acción A/B/C decidida y ejecutada
- [ ] Worktrees removidos
- [ ] Branches idle borradas (local + remote)
- [ ] `.vtt/` archivado o eliminado
- [ ] CLOSURE comment en VTT
- [ ] Commit del `_archive/` en main

---

## 8. Errores comunes

| Síntoma | Causa probable | Solución |
|---|---|---|
| `git worktree remove` falla "is locked" | Worktree tiene `locked` file | `rm <repo>/.git/worktrees/<wt>/locked` y reintentar |
| `git branch -D wt-X` falla "not fully merged" | Branch idle tiene commits que no van a main | OK — usar `-D` (forzado) ya que no se debe mergear |
| Branch idle no se puede borrar en remote | Nunca fue pusheada | OK — solo local. `git push origin --delete` retorna "remote ref does not exist" — ignorar |
| Tarball muy grande (>500MB) | `.vtt/manifests/` con muchos archivos viejos | Decidir si vale la pena archivar o solo borrar |
| PM authorization no encontrada | comment_id incorrecto | Solicitar al PM el comment_id explícito antes de ejecutar |
| Branch en Acción C no se documenta | TL olvidó §3 Acción C | Bloquear cleanup hasta documentar — sin registro no se preserva |

---

## 9. Skills invocadas

- `VTT.SKILL-WT-001` — `action=remove_worktree`, `action=close_branch_wontfix`, `action=archive_branch_for_phase2`
- `VTT.SKILL-AUTH-01` (legacy) — token para VTT API
- `VTT.SKILL-COMMENT-01` (legacy) — postear CLOSURE en VTT
- `VTT.SKILL-GIT-04` (legacy) — `gh pr create/merge/close`

---

## 10. Reglas Nivel 0 aplicables

| Regla | Razón |
|---|---|
| `RULE-WT-003` Cleanup post-aprobación | Esta es la versión "final" del cleanup — masivo en vez de por tarea |
| `RULE-WT-001` Worktree policy | Cleanup respeta el modelo (un worktree por rol) |

---

## 11. Changelog

| Versión | Fecha | Editor | Cambios |
|---|---|---|---|
| 1.0.0 | 2026-05-18 | PM Martin Rivas | Versión inicial. Refleja los §5.5.3-5.5.4 del Protocol (Fix #4): inventario de branches pendientes con 3 acciones (A/B/C). CLOSURE final + commit directo a main autorizado por PM (excepción a la regla "no commit directo"). |
