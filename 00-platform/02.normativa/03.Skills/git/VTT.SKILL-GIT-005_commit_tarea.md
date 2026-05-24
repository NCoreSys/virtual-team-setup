# VTT.SKILL-GIT-005 — Commit con formato del proyecto

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-GIT-005` |
| **Categoría** | GIT |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-19 |
| **Aplica a** | Todos los roles ejecutores |
| **Tokens estimados** | ~200 |
| **Cuándo se usa** | Paso 10 del workflow del agente — cuando hay cambios stageados listos para commitear |
| **Reemplaza** | `SKL-GIT-03_commit-formato.md` (legacy) |
| **Relacionada con** | `VTT.SKILL-GIT-002` (validar mensaje contra schema) — esta crea, GIT-002 valida |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `files_to_add` | array<path> | sí | Archivos específicos a stagear (evitar `git add .`) |
| `commit_type` | enum | sí | `feat` / `fix` / `docs` / `refactor` / `test` / `chore` |
| `task_id` | string (MS-XXX) | sí | ID de la tarea |
| `commit_description` | string ≤72 | sí | Descripción breve para el subject |
| `cambios` | array de strings | sí | Lista de cambios para el body |
| `agent_uuid` | uuid | sí/no | Para trazabilidad — agregado al footer si se especifica |

---

## Precondición

- Tu branch es `feature/<TASK_ID>` (verificable con `git branch --show-current`)
- Tenés cambios en working tree o stageados
- El working tree NO está en estado de rebase/merge en curso

---

## Variables del entorno

Ninguna específica.

---

## Formato del mensaje (estructura obligatoria)

```
<type> [<TASK_ID>]: <description>

- <cambio 1>
- <cambio 2>
- ...

Co-Authored-By: <Modelo> <noreply@anthropic.com>
Refs: #<TASK_ID>
```

### Reglas

| Regla | Detalle |
|---|---|
| **R1** | `Co-Authored-By` es **OBLIGATORIO** en todos los commits — preserva atribución del modelo |
| **R2** | `Refs: #<TASK_ID>` permite que VTT/GitHub vinculen commit ↔ tarea |
| **R3** | Subject ≤72 chars (límite git estándar) |
| **R4** | Body con bullets `- ` (uno por cambio) |
| **R5** | NO hacer `git add .` — usar lista específica de archivos |

---

## Ejecución

```bash
# 1. Stagear archivos específicos
git add <FILES_TO_ADD>

# 2. Commit con heredoc para mensaje multilínea
git commit -m "$(cat <<'EOF'
<TYPE> [<TASK_ID>]: <DESCRIPTION>

- <CAMBIO_1>
- <CAMBIO_2>

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
Refs: #<TASK_ID>
EOF
)"
```

### Ejemplo concreto

```bash
git add backend/src/services/foo.service.ts backend/src/tests/foo.test.ts
git commit -m "$(cat <<'EOF'
feat [MS-293]: Implementar error handling con AppError + MEM-ERR-xxx

- Crear src/errors/AppError.ts con factory + categorías
- Crear src/errors/errorCatalog.ts con MEM_ERR_001..019
- Middleware errorHandler en src/middleware/
- Tests con coverage >=80% en src/errors/

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
Refs: #MS-293
EOF
)"
```

---

## Validación

```bash
# Verificar el último commit
git log --oneline -1
# Esperado: <sha> <TYPE> [<TASK_ID>]: <DESCRIPTION>

# Verificar Co-Authored-By presente
git log -1 --pretty=format:"%b"
# Esperado: incluye "Co-Authored-By: ..."

# Verificar que solo se stageó lo deseado
git diff HEAD~1 --name-only
# Esperado: solo los files de $FILES_TO_ADD
```

---

## Error común

| Error | Causa | Solución |
|---|---|---|
| Commit sin `Co-Authored-By` | Olvido del footer | Amend: `git commit --amend` y agregar el footer |
| `git add .` agregó archivos no deseados | Falta de discipline | `git reset HEAD <file>` para unstage, luego commit limpio |
| Subject > 72 chars | Mensaje demasiado largo | Recortar el subject, mover detalle al body |
| Mensaje en una sola línea | Falta body | Re-commit con `--amend` agregando bullets |
| `Refs: #MS-XXX` mal escrito (sin #) | Sintaxis incorrecta | El `#` permite link automático en GitHub. Usar exactamente `Refs: #<TASK_ID>` |
| Heredoc con expansión de variables | Usar `EOF` sin comillas | Las comillas en `<<'EOF'` previenen expansión — variables las pongo en bash antes del heredoc o uso `<<EOF` (sin comillas) si querés expandirlas |

---

## Skills invocadas

Ninguna — solo git CLI.

---

## Skills que invocan ESTA

- Workflow del agente al cerrar tarea (Paso 10)
- `VTT.WORKFLOW-MAN-001.003 §Paso 12` — commit del manifest al PR del agente

---

## Cuándo NO usar esta Skill

- **Si vas a commitear cambios no relacionados con la tarea** — separar en commits distintos por tarea
- **Si solo cambiaste el manifest del agente** — usar el commit message específico de `VTT.WORKFLOW-MAN-001.003 §Paso 12`
- **Si es WIP (work-in-progress) por interrupción** — usar mensaje "WIP: pause <TASK_ID>" (ver `PROTOCOL-WT-001 §5.4.3 Opción A`)

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-19 | Versión inicial. Migración de `SKL-GIT-03_commit-formato.md` con renumeración a `GIT-005`. Ampliación: ejemplo concreto con MS-293, sección de reglas R1-R5 enumeradas, tabla de errores comunes con 6 casos incluido el bug del heredoc con expansión. |
