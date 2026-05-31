# VTT.SKILL-GIT-002 — Commit estructurado verificable contra un schema de mensaje

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-GIT-002` |
| **Categoría** | GIT |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-17 |
| **Aplica a** | Todos los roles que editen cualquier repo gobernado por VTT |
| **Tokens estimados** | ~190 |
| **Cuándo se usa** | Después de stagear cambios, ANTES de hacer commit. Garantiza que el mensaje cumple el schema que la gobernanza del repo exige. |

---

## Inputs (contractuales)

Parámetros que la Skill recibe SIEMPRE de igual forma, independiente del repo o del contexto:

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `commit_message` | string (multiline) | sí | El mensaje completo del commit, ya formateado por el invocador. |
| `header_regex` | string (regex) | sí | Regex que la primera línea del mensaje debe cumplir. Definido por gobernanza del repo. |
| `required_trailers` | json array de strings | sí | Lista de prefijos de campos obligatorios al final del mensaje. Ej: `["Motivo:", "Origen:", "Consumidores:"]`. Vacío `[]` si el repo no exige trailers. |
| `block_branches` | json array de strings | no (default `["main"]`) | Lista de branches en los que el commit debe ser rechazado. |
| `repo_path` | path | no (default `.`) | Path al repo donde se hace el commit. |

> **Regla contractual:** la Skill NO contiene el formato del mensaje. El invocador (Workflow / hook / documento de gobernanza) construye el mensaje y la Skill solo valida + ejecuta el commit. Esto permite que una misma Skill sirva a múltiples repos con schemas distintos.

---

## Precondición

Condiciones que deben ser verdaderas ANTES de ejecutar esta Skill:

- El directorio `repo_path` es un repo Git válido (`.git/` existe)
- Hay al menos un archivo en el index (`git diff --cached --name-only` retorna ≥1 línea)
- El branch actual NO está en `block_branches`
- `commit_message` no está vacío
- `commit_message` cumple `header_regex` en su primera línea
- `commit_message` contiene todos los prefijos de `required_trailers`
- Identidad git configurada (`git config user.name` y `user.email`)

---

## Variables del entorno

```bash
$GIT_AUTHOR_NAME       # Configurado vía git config (no se setea aquí)
$GIT_AUTHOR_EMAIL      # Configurado vía git config (no se setea aquí)
```

> **Política:** esta Skill NO usa variables específicas de proyecto. Todo se recibe como input contractual.

---

## Ejecución

La Skill valida que `commit_message` cumple `header_regex` y contiene todos los `required_trailers`, verifica que no se está commiteando a `block_branches`, y ejecuta el commit pasando el mensaje vía stdin para preservar el formato multilinea.

### Comando(s)

```bash
# Inputs (ejemplo)
HEADER_REGEX='^\[agente:[a-z]+\] \[proyecto:[a-z0-9-]+\] \[scope:[^]]+\] \[type:(editorial|functional|structural|breaking)\]'
REQUIRED_TRAILERS='["Motivo:", "Origen:", "Consumidores:"]'
BLOCK_BRANCHES='["main"]'
REPO_PATH="."

# commit_message viene de un archivo temporal o stdin para preservar multiline
COMMIT_MSG_FILE="/tmp/vtt_commit_msg.txt"

cd "$REPO_PATH"

# 1. Validar que hay algo staged
COUNT_STAGED=$(git diff --cached --name-only | wc -l)
[ "$COUNT_STAGED" -lt 1 ] && { echo "ABORT: no hay archivos staged"; exit 1; }

# 2. Validar que el branch actual no está bloqueado
CURRENT=$(git rev-parse --abbrev-ref HEAD)
echo "$BLOCK_BRANCHES" | python -c "import sys,json; \
  blocked=json.load(sys.stdin); \
  sys.exit(1 if '$CURRENT' in blocked else 0)" \
  || { echo "ABORT: commit a '$CURRENT' bloqueado por gobernanza"; exit 1; }

# 3. Validar que la primera línea cumple header_regex
HEADER=$(head -1 "$COMMIT_MSG_FILE")
echo "$HEADER" | grep -qE "$HEADER_REGEX" \
  || { echo "ABORT: header del commit no cumple header_regex"; exit 1; }

# 4. Validar que todos los required_trailers están presentes
echo "$REQUIRED_TRAILERS" | python -c "
import sys, json
trailers = json.load(sys.stdin)
msg = open('$COMMIT_MSG_FILE').read()
missing = [t for t in trailers if t not in msg]
if missing:
    print(f'ABORT: faltan trailers: {missing}')
    sys.exit(1)
" || exit 1

# 5. Ejecutar commit con el mensaje desde archivo (preserva formato)
git commit -F "$COMMIT_MSG_FILE"
```

> **Política:** lógica ~30 líneas, sin Script externo. Si en el futuro se requiere lógica más sofisticada (validación de Co-Authored-By, parsing de scope automático), se extrae a `VTT.SCRIPT-GIT-003_validate_commit_message.py`.

---

## Validación

Cómo saber si la Skill funcionó:

- `git log -1 --format=%H` retorna un SHA nuevo
- `git log -1 --format=%B` retorna exactamente el `commit_message` enviado
- La primera línea del último commit cumple `header_regex`
- Todos los `required_trailers` están presentes en el último commit

```bash
# Comando de validación post-ejecución
SHA=$(git log -1 --format=%H)
[ -n "$SHA" ] || { echo "FAIL: no se creo commit"; exit 1; }

MSG=$(git log -1 --format=%B)
echo "$MSG" | head -1 | grep -qE "$HEADER_REGEX" \
  || { echo "FAIL: header no cumple regex"; exit 1; }

echo "$REQUIRED_TRAILERS" | python -c "
import sys, json
trailers = json.load(sys.stdin)
msg = '''$MSG'''
missing = [t for t in trailers if t not in msg]
if missing:
    print(f'FAIL: faltan trailers: {missing}')
    sys.exit(1)
print('OK trailers')
"
echo "OK — commit $SHA valido en $(git rev-parse --abbrev-ref HEAD)"
```

---

## Error común

| Error | Causa probable | Solución |
|---|---|---|
| `ABORT: no hay archivos staged` | Olvidaste `git add` | Stagear archivos antes de invocar la Skill |
| `ABORT: commit a 'main' bloqueado` | Estás en main directo | Crear branch con `VTT.SKILL-GIT-001` y volver a invocar |
| `ABORT: header no cumple header_regex` | Faltó un marker, mayúsculas, o tipo inválido | Revisar `commit_message` y ajustar al regex del repo |
| `ABORT: faltan trailers` | Falta `Motivo:`, `Origen:` o `Consumidores:` | Agregar los campos al `commit_message` |
| Commit hecho pero formato perdido (todo en una línea) | No se usó `-F file` o HEREDOC | Pasar el mensaje vía archivo (`commit -F`) o HEREDOC con `cat <<EOF` |

---

## Scripts invocados

Sin Scripts externos — lógica inline en sección Ejecución.

> Cuando el catálogo `04.Scripts/` esté poblado, esta Skill podrá refactorizarse para invocar `VTT.SCRIPT-GIT-003_validate_commit_message.py` (validación de header + trailers en un solo paso, devolviendo JSON).

---

## Ejemplo de uso — gobierno editorial de virtual-teams-setup

Para el repo `virtual-teams-setup` durante la Fase de Desarrollo, el schema del mensaje exigido por la gobernanza es:

```
[agente:<rol>] [proyecto:<origen>] [scope:<ruta>] [type:<tipo>]
<titulo-corto-max-60-chars>

<descripcion-3-a-5-lineas>

Motivo: <razon-del-cambio>
Origen: <ticket-sesion-PR-leccion>
Consumidores: <lista-proyectos-afectados-o-none>

Co-Authored-By: Claude <modelo> <noreply@anthropic.com>
```

Inputs a la Skill:

```bash
HEADER_REGEX='^\[agente:(tl|pm|pjm|be|db|fe|do|qa|ux|dl|sa|ar|sec|setup)\] \[proyecto:[a-z0-9-]+\] \[scope:[^]]+\] \[type:(editorial|functional|structural|breaking)\]'
REQUIRED_TRAILERS='["Motivo:", "Origen:", "Consumidores:"]'
BLOCK_BRANCHES='["main"]'
```

Tipos válidos en `[type:...]`:

| Tipo | Cuándo usarlo |
|---|---|
| `editorial` | Typo, ejemplo, aclaración. NO cambia proceso ni schema |
| `functional` | Paso nuevo, regla nueva, mejora de procedimiento |
| `structural` | Cambio de schema, nueva carpeta, nueva entidad, renombre |
| `breaking` | Rompe consumidores (elimina campo, renombra path canónico) |

> Este ejemplo es **instancia** de la Skill, no la Skill misma. Otro repo (ej. memory-service-backend) puede usar otro schema (`feat(scope): description` de Conventional Commits) y la misma Skill funciona pasando otro `header_regex` y otros `required_trailers`.

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-17 | Versión inicial. Skill genérica para hacer commit verificado contra un regex de header y una lista de trailers obligatorios. Inputs contractuales: `commit_message`, `header_regex`, `required_trailers`, `block_branches`, `repo_path`. |

> **Política de versionado** (Incremental):
> - **v1, v2, v3...** — incremento por cambio de contrato (inputs/outputs) o de comportamiento mayor.
> - Mejoras internas que no cambian el contrato → misma versión, actualizar fecha.
