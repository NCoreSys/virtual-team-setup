# VTT.SKILL-PRECHECK-001 — Validar entorno antes de iniciar tarea

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-PRECHECK-001` |
| **Categoría** | PRECHECK (validación de entorno) |
| **Versión** | 1.1 |
| **Fecha** | 2026-05-31 |
| **Aplica a** | Todos los agentes ejecutores (BE, FE, DB, DO, QA, DL, UX, AR, SA) + TL (cuando ejecuta tareas) |
| **Tokens estimados** | ~280 |
| **Cuándo se usa** | **Paso 0 obligatorio** después de recibir el mensaje de asignación del TL y ANTES de tocar código |
| **Reglas aplicables** | `RULE-SCRIPT-001` (path canónico), `RULE-TEMPLATE-001` (lectura formal), `RULE-AGENT-001` (worktree dedicado) |

---

## 1. Propósito

Validar que el entorno del agente cumple las precondiciones operativas mínimas ANTES de iniciar la ejecución de cualquier tarea VTT. Si algo falla → **detener** y reportar al TL.

> **Origen:** drift visible MS-290 vs MS-333 + presencia de 5 copias locales de `gen_mensaje.py` en memory-service. Sin este pre-check, el agente puede ejecutar copias divergentes sin saberlo.

---

## 2. Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `task_id` | string (MS-XXX) | sí | ID de la tarea recibida |
| `role` | enum | sí | BE/FE/DB/DO/QA/DL/UX/AR/SA/TL |
| `expected_scripts` | array<string> | sí | Lista de scripts que la tarea referencia (extraída del mensaje del TL) |

---

## 3. Variables del entorno

```bash
$VTT_SETUP                # path al repo virtual-teams-setup/00-platform/
$TOKEN                    # JWT obtenido con SKILL-AUTH-001 (validar al final)
$AGENT_UUID               # UUID del agente
```

---

## 4. Los 5 checks obligatorios

### Check 1 — `$VTT_SETUP` está exportado y apunta a un directorio existente

```bash
if [ -z "$VTT_SETUP" ]; then
  echo "❌ ABORT: \$VTT_SETUP no está exportado. Configurar en init-message del rol."
  exit 2
fi

if [ ! -d "$VTT_SETUP" ]; then
  echo "❌ ABORT: \$VTT_SETUP=$VTT_SETUP no es un directorio existente."
  exit 2
fi

if [ ! -d "$VTT_SETUP/02.normativa" ]; then
  echo "❌ ABORT: \$VTT_SETUP no contiene 02.normativa/. ¿Apunta al repo correcto?"
  exit 2
fi
```

### Check 2 — Los scripts referenciados existen en `$VTT_SETUP`

Para cada script que el mensaje del TL mencione (típicamente `VTT.SCRIPT-MAN-001`, `VTT.SCRIPT-EXM-001`, `VTT.SCRIPT-MSG-001`):

```bash
EXPECTED_SCRIPTS=(
  "$VTT_SETUP/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py"
  "$VTT_SETUP/02.normativa/04.Scripts/manifest/VTT.SCRIPT-EXM-001_gen_execution_manifest.py"
  # ... otros que la tarea use
)

for script in "${EXPECTED_SCRIPTS[@]}"; do
  if [ ! -f "$script" ]; then
    echo "❌ ABORT: Script no existe en \$VTT_SETUP: $script"
    echo "         Si ves este error, el repo virtual-teams-setup/ no está actualizado."
    echo "         Hacer: cd \$VTT_SETUP/../.. && git pull origin main"
    echo "         NO continuar con la tarea hasta que el script aparezca en \$VTT_SETUP."
    exit 2
  fi
done
```

### Check 3 — NO existen copias locales INTRODUCIDAS POR ESTA BRANCH (RULE-SCRIPT-001) — v1.1

> **Cambio v1.1 (Brechas 1 + 4 — 2026-05-31):** este Check distinguía antes "copia local detectada = ABORT" sin importar el origen, lo que bloqueaba agentes por housekeeping de tareas anteriores que ellos no introdujeron. La v1.1 aplica heurística **preexistente vs introducido por esta branch**:
>
> - **Introducido por la branch de tarea actual** → ABORT (es responsabilidad del agente, viola RULE-SCRIPT-001 ahora)
> - **Preexistente en main / base ref** → WARN + listado al TL para limpieza separada (NO bloquea al agente)

```bash
# v1.1 — heurística "preexistente vs introducido por esta branch"

# Determinar el base ref para comparar
BASE_REF="${BASE_REF:-origin/main}"

# 1. Detectar TODAS las copias locales en el worktree
ALL_ROGUE=$(find . -type f \( -name "VTT.SCRIPT-MAN-*.py" -o -name "VTT.SCRIPT-EXM-*.py" -o -name "VTT.SCRIPT-MSG-*.py" \) 2>/dev/null | sed 's|^\./||')

if [ -z "$ALL_ROGUE" ]; then
  echo "✅ Check 3 — 0 copias locales detectadas en worktree"
else
  # 2. Para cada copia detectada, determinar si fue introducida por esta branch
  INTRODUCED_BY_BRANCH=""
  PREEXISTING=""

  for file in $ALL_ROGUE; do
    # ¿Existe el archivo en el base_ref?
    if git cat-file -e "$BASE_REF:$file" 2>/dev/null; then
      # Preexistente — estaba en main / base
      PREEXISTING="$PREEXISTING\n  - $file"
    else
      # No existía en base_ref → fue introducido por esta branch
      INTRODUCED_BY_BRANCH="$INTRODUCED_BY_BRANCH\n  - $file"
    fi
  done

  # 3. Si hay INTRODUCIDOS por esta branch → ABORT (responsabilidad del agente actual)
  if [ -n "$INTRODUCED_BY_BRANCH" ]; then
    echo "❌ ABORT (RULE-SCRIPT-001 violación): copias locales INTRODUCIDAS por esta branch:"
    echo -e "$INTRODUCED_BY_BRANCH"
    echo ""
    echo "Estas copias las introdujo la branch actual ($BRANCH_ACTUAL) — son tu responsabilidad."
    echo "Acción: borrar y usar los scripts desde \$VTT_SETUP/02.normativa/04.Scripts/."
    exit 2
  fi

  # 4. Si solo hay PREEXISTENTES → WARN (no bloquea, reporta al TL)
  if [ -n "$PREEXISTING" ]; then
    echo "⚠️  Check 3 — copias locales PREEXISTENTES detectadas (no introducidas por esta branch):"
    echo -e "$PREEXISTING"
    echo ""
    echo "Estas copias ya estaban en $BASE_REF antes de tu tarea. NO bloquean."
    echo "Acción recomendada: reportar al TL para que cree tarea de cleanup separada."
    echo "Tu tarea continúa normalmente — NO toques estos archivos a menos que tu ASSIGNMENT lo pida."
    # NOTA: NO se hace exit 2 — el agente sigue
  fi
fi
```

> **Excepción legítima preservada:** `scripts/gen_mensaje.py` (legacy, del TL) sigue vivo en `project-tl/scripts/` mientras dure la migración OLA 1 — no es violación porque aún no está promovido. Con la heurística v1.1, además, queda automáticamente clasificada como "preexistente" (ya está en main) → WARN, no ABORT.

> **Heurística inversa para el TL:** si el TL quiere ver QUÉ rogue files preexistentes hay en el worktree (sin necesidad de bloquear al agente), puede ejecutar este mismo Check 3 directamente — la lista PREEXISTING le sirve como input para crear la tarea de cleanup.

### Check 4 — Worktree del rol existe y el agente está en él (RULE-AGENT-001)

```bash
EXPECTED_WORKTREE=".vtt/worktrees/<repo>-${ROLE_LOWER}/"
CURRENT_DIR=$(pwd)

if [[ "$CURRENT_DIR" != *"/.vtt/worktrees/"*"-${ROLE_LOWER}/"* ]]; then
  echo "❌ ABORT: No estás en el worktree del rol $ROLE."
  echo "         cwd actual: $CURRENT_DIR"
  echo "         esperado:   .vtt/worktrees/<repo>-${ROLE_LOWER}/"
  exit 2
fi
```

### Check 5 — `$TOKEN` válido (responde 200 a un GET de prueba)

```bash
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer $TOKEN" \
  "$VTT_BASE_URL/api/auth/me")

if [ "$HTTP_CODE" != "200" ]; then
  echo "❌ ABORT: \$TOKEN no es válido (GET /auth/me retornó $HTTP_CODE)."
  echo "         Re-ejecutar VTT.SKILL-AUTH-001 para obtener nuevo JWT."
  exit 2
fi
```

---

## 5. Ejecución (Variante A — script único)

El agente ejecuta este script al inicio de cada tarea, ANTES de tocar código:

```bash
python $VTT_SETUP/02.normativa/04.Scripts/precheck/VTT.SCRIPT-PRECHECK-001_validate_environment.py \
  --task-id MS-XXX \
  --role $ROLE \
  --token-env TOKEN
```

> **Pendiente:** el script `VTT.SCRIPT-PRECHECK-001_validate_environment.py` aún no existe — ver §"Scripts invocados" abajo. Mientras tanto, el agente ejecuta los 5 checks manualmente con los bash de §4.

---

## 6. Output esperado (todos los checks OK)

```
✅ Check 1 — $VTT_SETUP definido y existe: c:/.../virtual-teams-setup/00-platform
✅ Check 2 — 2 scripts esperados encontrados en $VTT_SETUP
✅ Check 3 — 0 copias locales de scripts detectadas en worktree
✅ Check 4 — Worktree correcto: .vtt/worktrees/backend-be/
✅ Check 5 — $TOKEN válido (auth/me 200)

▶ Entorno OK. Procede a leer ASSIGNMENT y BRIEF de la tarea.
```

Si **cualquier** check falla → exit code **2** y mensaje claro. El agente NO continúa la tarea.

---

## 7. Validación

```bash
# El agente confirma que el pre-check pasó antes de mover la tarea a in_progress
echo $?  # esperado: 0
```

---

## 8. Errores comunes

| Error | Causa | Solución |
|---|---|---|
| `$VTT_SETUP no está exportado` | Init-message del rol no incluye `export VTT_SETUP=...` | Editar OPERATIVO_<ROL>_<PROYECTO>.md sección "Apertura de sesión" para agregar export |
| `Script no existe en $VTT_SETUP` | Repo `virtual-teams-setup/` desactualizado o el script todavía no está promovido | Hacer `git pull` en virtual-teams-setup/. Si el script no existe, escalar al TL/PM (puede ser una tarea de normativa pendiente) |
| `Copias locales detectadas` | Sesión previa copió scripts al worktree | Ejecutar CLEANUP_COPIAS_LOCALES_SCRIPTS_OLA1.md o borrar manualmente |
| `No estás en el worktree del rol` | Agente ejecuta desde clon base o desde worktree de otro rol | `cd .vtt/worktrees/<repo>-<rol>/` |
| `$TOKEN no es válido` | Token expirado (TTL 30 días) o nunca obtenido | Ejecutar SKILL-AUTH-001 |

---

## 9. Scripts invocados

- `VTT.SCRIPT-PRECHECK-001_validate_environment.py` (pendiente de crear) — versión automatizada de los 5 checks
- Mientras tanto: bash inline (Variante manual en §4)

---

## 10. Skills invocadas

- `VTT.SKILL-AUTH-001` (Check 5 — validar $TOKEN)

---

## 11. Skills que invocan ESTA

- **Toda skill/workflow que el agente ejecute al iniciar una tarea** debe invocar PRECHECK-001 como Paso 0
- `VTT.WORKFLOW-ASG-001.022` (Agente lee execution_manifest) — Paso 0 antes de leer
- Template `TEMPLATE_MENSAJE_ASIGNACION.md` v2.2 — sección "Paso 0 — Pre-check obligatorio"

---

## 12. Cuándo NO usar esta Skill

- **Re-ejecución dentro de la misma sesión** — si ya pasó el pre-check en la sesión actual, no es necesario re-ejecutar para la siguiente tarea del mismo worktree (con el mismo `$VTT_SETUP` y `$TOKEN`)
- **El TL operando sobre su propio worktree** para tareas de coordinación que NO modifican código — pre-check sigue siendo recomendado pero no obligatorio

---

## 13. Política de fail-fast

> **Si el pre-check falla, el agente DETIENE la ejecución y reporta al TL.**
>
> NO intenta "arreglarlo solo" (ej. copiar el script faltante desde otro lado, o re-exportar `$VTT_SETUP` apuntando a un path arbitrario). La razón: cada intervención silenciosa del agente para "compensar" un entorno roto **es la causa raíz del drift** que esta skill intenta detener.

Acción correcta cuando falla:
1. Capturar el output completo del pre-check
2. Postear comment en la tarea VTT al TL con el error
3. Dejar la tarea en `task_on_hold` (o `task_pending` si aún no se inició)
4. Esperar respuesta del TL antes de continuar

---

## 14. Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-22 | Versión inicial. 5 checks obligatorios (VTT_SETUP, scripts en setup, no copias locales, worktree, TOKEN). Aplica RULE-SCRIPT-001, RULE-TEMPLATE-001, RULE-AGENT-001. Origen: drift MS-290 vs MS-333 + ola 1 de cierre del sub-sistema MSG. |
| 1.1 | 2026-05-31 | **Brechas 1+4 (Sprint S00 VTT R2.0).** Check 3 rediseñado con heurística "preexistente vs introducido por esta branch". Antes: cualquier rogue file → ABORT (bloqueaba agentes por housekeeping ajeno de tareas anteriores). Ahora: solo abortar si la branch actual introdujo el rogue file (`git cat-file -e $BASE_REF:$file` para discriminar); preexistentes → WARN + reporte al TL sin bloquear. Origen: TL Reviewer VTT registró brechas en devlogs b428d19d y f9f976e3 de VTT-818. Severity de fix: high (sin esto cada agente del próximo sprint repite el bloqueo). |
