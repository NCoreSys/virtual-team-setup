# VTT.WORKFLOW-MAN-001.002 — Leer Execution Manifest

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-MAN-001.002` |
| **Pertenece a** | `VTT.PROTOCOL-MAN-001` §5.2 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-05-17 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | Agente ejecutor (BE/DB/FE/DO/QA/DL/UX/AR/SA) |
| **Tipo** | [PROCESO] sub-procedimiento — invocado por PROTOCOL-MAN-001 §5.2.1 (que a su vez corresponde a PROTOCOL-ASG-001 §5.3.2.b) |

---

## 1. Propósito

Que el agente ejecutor cargue, valide y memorice el contenido del `.vtt/manifests/<TASK_ID>.execution.json` antes de tocar código. Esto le dice al agente:

- En qué worktree debe operar
- Qué paths puede modificar (`allowedPaths`)
- Qué outputs se esperan al cerrar (`expectedOutputs`)
- Qué branch usar (`branchExpected`)

> Sin leer el manifest, el agente trabaja a ciegas y termina tocando archivos fuera del scope → `task_rejected` al cierre. Este Workflow elimina esa posibilidad.

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `task_id` | string | Mensaje del TL al agente | sí | ID externo de la tarea (MS-XXX) |
| `agent_uuid` | uuid | Operativo del agente | sí | UUID del propio agente para verificar identidad |
| `manifest_path` | path | Convención: `.vtt/manifests/<TASK_ID>.execution.json` | sí | Ruta absoluta al manifest local |
| `expected_role` | enum | Operativo del agente | sí | Rol esperado (debe coincidir con `agent.role` del manifest) |

---

## 3. Precondiciones

- El TL Asignador ya ejecutó `VTT.WORKFLOW-MAN-001.001` y dejó el manifest en disco
- El agente está en una shell con `pwd` que puede acceder a `.vtt/manifests/`
- El agente tiene su `agent_uuid` cargado en variable de entorno o conocido
- El mensaje de asignación recibido por el agente menciona el path del manifest

---

## 4. Reglas del Workflow

- **R1:** El agente NO toca código antes de completar este Workflow.
- **R2:** Si `agent.uuid` del manifest ≠ propio UUID del agente → STOP inmediato y notificar al TL. NO continuar.
- **R3:** El agente memoriza `allowedPaths` y los respeta durante TODA la ejecución. Cualquier archivo fuera → STOP y escalar.
- **R4:** Si el manifest tiene errores (JSON inválido, campos faltantes) → STOP y notificar al TL. NO inventar valores.
- **R5:** Cada vez que el agente abre una sesión nueva en el worktree, vuelve a verificar el manifest (no asumir contexto previo).

---

## 5. Pasos

### Paso 1 — Localizar el manifest

```
ls .vtt/manifests/<TASK_ID>.execution.json
```

¿Archivo existe? →
- **SÍ** → continuar
- **NO** → STOP y notificar al TL: "Execution Manifest no generado para <TASK_ID> — bloqueo asignación"

### Paso 2 — Validar que el JSON es parseable

```
jq '.' .vtt/manifests/<TASK_ID>.execution.json > /dev/null
```

¿Parsea sin error? →
- **SÍ** → continuar
- **NO** → STOP y notificar al TL: "Execution Manifest inválido (JSON malformed) — bloqueo asignación"

### Paso 3 — Verificar `agent.uuid` coincide

```
MANIFEST_AGENT_UUID=$(jq -r '.agent.uuid' .vtt/manifests/<TASK_ID>.execution.json)

if [ "$MANIFEST_AGENT_UUID" != "$AGENT_UUID" ]; then
  echo "ERROR: manifest asigna a $MANIFEST_AGENT_UUID, pero soy $AGENT_UUID"
  exit 1
fi
```

¿Coinciden? →
- **SÍ** → continuar
- **NO** → STOP y escalar al TL: "Manifest no es para mí — verificar asignación"

### Paso 4 — Verificar rol coincide

```
MANIFEST_ROLE=$(jq -r '.agent.role' .vtt/manifests/<TASK_ID>.execution.json)
```

¿`MANIFEST_ROLE` == `EXPECTED_ROLE`? →
- **SÍ** → continuar
- **NO** → STOP y escalar (probable error del TL)

### Paso 5 — Verificar worktree y branch

```
WT=$(jq -r '.worktreePath' .vtt/manifests/<TASK_ID>.execution.json)
BR=$(jq -r '.branchExpected' .vtt/manifests/<TASK_ID>.execution.json)

cd "$WT"
pwd                          # debe terminar en el worktreePath
git status                   # debe mostrar working tree limpio o branch activa
```

¿Estoy en el worktree correcto? →
- **SÍ** → continuar
- **NO** → `cd "$WT"` o STOP si el worktree no existe

¿Branch correcta o puedo crearla? →
```
git checkout -b "$BR" 2>/dev/null || git checkout "$BR"
```

### Paso 6 — Memorizar `allowedPaths`

```
jq -r '.allowedPaths[]' .vtt/manifests/<TASK_ID>.execution.json
```

Imprimir y memorizar la lista. El agente debe **revisitarla cada vez** que vaya a modificar un archivo.

Ejemplo de auto-check antes de cada edit (pseudo-código mental del agente):

```
¿Voy a tocar X? → ¿X está en allowedPaths? →
  SÍ → proceder
  NO → STOP, escalar al TL
```

### Paso 7 — Memorizar `expectedOutputs`

```
jq -r '.expectedOutputs[]' .vtt/manifests/<TASK_ID>.execution.json
```

Esta lista es la **checklist final** que el agente verificará en su Paso 14 antes de generar el Task Manifest v1.0.

### Paso 8 — Memorizar referencias

```
jq -r '.references.assignment_path, .references.brief_path' \
   .vtt/manifests/<TASK_ID>.execution.json
```

El agente debe abrir y leer:
- El ASSIGNMENT completo (workflow de 15 pasos + criterios de aceptación)
- El BRIEF completo (diseño original inmutable)

→ invoca **`VTT.SKILL-EXM-001`** con (`action=read_manifest`, `task_id=<TASK_ID>`)

### Paso 9 — Confirmar al TL (opcional pero recomendado)

Postear comment de inicio en VTT:

```
"Ejecutando <TASK_ID> desde worktree <WT>, branch <BR>. allowedPaths confirmados."
```

→ invoca **`VTT.SKILL-COMMENT-01`** (legacy)

### Paso 10 — Iniciar workflow del ASSIGNMENT

El agente cambia su tarea a `task_in_progress` y procede con los 15 pasos del ASSIGNMENT.

→ invoca **`VTT.SKILL-STATUS-01`** (legacy — mover a `task_in_progress`)

---

## 6. Outputs

| Nombre | Tipo | Destino | Descripción |
|---|---|---|---|
| Memoria operativa del agente | runtime | sesión del agente | `allowedPaths` y `expectedOutputs` cargados |
| Status `task_in_progress` | VTT API | tarea en VTT | Indica que el agente inició formalmente |
| Comment de inicio (opcional) | VTT API | tarea en VTT | Trazabilidad |

---

## 7. Validación de salida

```bash
# Check 1: estoy en el worktree correcto
pwd | grep -F "$(jq -r '.worktreePath' .vtt/manifests/<TASK_ID>.execution.json)"
# Esperado: match

# Check 2: estoy en la branch correcta
git branch --show-current
# Esperado: feature/<TASK_ID>

# Check 3: status en VTT
curl -s "$VTT_BASE_URL/api/tasks/<TASK_ID>" -H "Authorization: Bearer $TOKEN" | \
  jq '.data.statusCode'
# Esperado: "task_in_progress"
```

- [ ] Manifest cargado sin errores
- [ ] `agent.uuid` confirmado como propio
- [ ] Worktree correcto activo
- [ ] Branch correcta o creada
- [ ] `allowedPaths` y `expectedOutputs` memorizados
- [ ] Status en VTT cambió a `task_in_progress`

---

## 8. Errores comunes

| Síntoma | Causa probable | Solución |
|---|---|---|
| Manifest no existe | TL no ejecutó WORKFLOW-MAN-001.001 | Notificar al TL — NO empezar a trabajar |
| `agent.uuid` distinto al propio | Asignación cruzada (TL se confundió de agente) | STOP y solicitar corrección al TL |
| Worktree no existe en disco | Setup incompleto | Ejecutar setup de worktree del rol antes |
| Branch ya existe con cambios | Re-entrega de tarea rechazada | OK — continuar sobre la branch existente |
| `allowedPaths` muy estrecho — necesito tocar archivo X | El ASSIGNMENT mal definió scope | NO inventar — escalar al TL para extender `allowedPaths` formalmente |
| ASSIGNMENT referenciado no existe en disco | Path absoluto vs relativo | Verificar path desde la raíz del proyecto |
| `expectedOutputs` ambiguos | ASSIGNMENT mal formado | Pedir clarificación al TL antes de empezar |

---

## 9. Skills invocadas

- `VTT.SKILL-EXM-001` — Skill principal (`action=read_manifest`)
- `VTT.SKILL-STATUS-01` (legacy) — Mover a `task_in_progress`
- `VTT.SKILL-COMMENT-01` (legacy) — Postear comment de inicio (opcional)
- `VTT.SKILL-AUTH-01` (legacy) — Token para los GET/PATCH a VTT

---

## 10. Reglas Nivel 0 aplicables

| Regla | Razón |
|---|---|
| `RULE-WT-002` Execution manifest | Aplica directamente — esta es la lectura obligatoria definida por la regla |
| `RULE-AGENT-001 v2.0` Worktree por rol | El agente debe verificar que está en el worktree de su rol |
| `RULE-WT-001` Worktree policy | Granularidad por rol — el agente no crea worktrees nuevos por tarea |

---

## 11. Changelog

| Versión | Fecha | Editor | Cambios |
|---|---|---|---|
| 1.0.0 | 2026-05-17 | PM Martin Rivas | Versión inicial. Reemplaza la referencia legacy `VTT.WORKFLOW-ASG-001.022`. Ahora vive bajo PROTOCOL-MAN-001. |
