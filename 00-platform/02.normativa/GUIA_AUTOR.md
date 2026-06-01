# GUIA_AUTOR — Cómo escribir documentos normativos VTT

| Campo | Valor |
|---|---|
| **Versión** | 1.1 |
| **Fecha** | 2026-05-31 |
| **Audiencia** | PM, TL, o cualquier autor que vaya a crear Protocols / Workflows / Skills / Scripts / **CARDs** |
| **Complementa a** | `README.md` (modelo conceptual) + `_autoria/` (templates concretos) |
| **Objetivo** | Resolver dudas del autor: ¿qué nivel uso? ¿cómo elijo el código? ¿qué evitar? |

> **v1.1 (2026-05-31):** Agregado tratamiento del Nivel R CARD: §2 árbol de decisión ampliado, §4.5 nueva Checklist CARD, §4.6 nueva Presupuesto tokens canónico (chars/4), anti-patterns CARD-específicos. Ver referencia completa del Nivel R en `README.md` §2.4.bis y §8.bis.

---

## Tabla de Contenido

1. [Antes de empezar — checklist previo](#1-antes-de-empezar--checklist-previo)
2. [Cómo decidir el nivel correcto](#2-cómo-decidir-el-nivel-correcto)
3. [Asignación de código](#3-asignación-de-código)
4. [Checklists por nivel](#4-checklists-por-nivel)
5. [Anti-patterns con ejemplos](#5-anti-patterns-con-ejemplos)
6. [Workflow del autor — del borrador a la publicación](#6-workflow-del-autor)
7. [Reglas Nivel 0 — cómo identificar las aplicables](#7-reglas-nivel-0--cómo-identificar-las-aplicables)
8. [Versionado](#8-versionado)
9. [Después de publicar](#9-después-de-publicar)
10. [FAQ](#10-faq)

---

## 1. Antes de empezar — checklist previo

Antes de copiar un template, completa estos 5 checks:

```
[ ] 1. ¿Es realmente necesario un documento nuevo? (busca primero en INVENTARIO.md)
[ ] 2. ¿En qué nivel del modelo encaja? (Protocol/Workflow/Skill/Script)
[ ] 3. ¿Qué categoría (CAT) le corresponde? (ASG, ISS, TRK, LD, AUTH, etc.)
[ ] 4. ¿Cuál es el siguiente NNN disponible? (consulta carpeta destino)
[ ] 5. ¿Identifiqué las Reglas Nivel 0 que aplican?
```

Si fallas alguno de estos checks, **detente y resuélvelo antes de escribir**. Documentos creados sin estos pasos generan drift y duplicación.

### Búsqueda previa — ¿ya existe algo similar?

```bash
cd 00-platform/02.normativa

# Buscar por palabra clave en INVENTARIO
grep -i "<keyword>" INVENTARIO.md

# Buscar archivos con nombre similar
find . -iname "*<keyword>*"

# Buscar en pending-migration (puede ya existir como SOP legacy)
ls 01.Protocols/_pending-migration/ | grep -i "<keyword>"
ls 03.Skills/_pending-migration/ -R | grep -i "<keyword>"
```

Si **ya existe algo parecido**, considera estas 3 opciones antes de crear nuevo:

| Situación | Acción |
|---|---|
| Existe pero está en `_pending-migration/` | Migra ese documento al formato VTT (no crees uno nuevo) |
| Existe pero está incompleto/obsoleto | Bump versión + actualiza (no dupliques) |
| Existe pero cubre el 80% del caso | Considera agregar sección al existente |
| No existe nada similar | Crea nuevo |

---

## 2. Cómo decidir el nivel correcto

La pregunta más frecuente del autor es: **¿esto es Protocol, Workflow, Skill o Script?**

### Árbol de decisión rápido

```
¿Es un proceso de negocio end-to-end con varias fases y múltiples roles?
│
├── SÍ → PROTOCOL (Nivel 4)
│   Ej: "Ciclo de asignación y cierre de tarea"
│   Tamaño esperado: 400-1000 líneas, 5-20 referencias cruzadas
│
└── NO → ¿Es una secuencia de pasos guiados (sin decisiones de negocio)?
    │
    ├── SÍ → WORKFLOW (Nivel 3)
    │   Ej: "Generar y subir BRIEFs", "Validar inputs del handoff"
    │   Tamaño esperado: 100-300 líneas, invoca varias Skills
    │
    └── NO → ¿Es una capacidad reusable con inputs/outputs contractuales?
        │
        ├── SÍ → SKILL (Nivel 2)
        │   Ej: "Subir attachment", "Crear TrackableItem"
        │   Tamaño esperado: 50-150 líneas, orquesta 1-N Scripts
        │
        └── NO → ¿Es un comando atómico ejecutable?
            │
            └── SÍ → SCRIPT (Nivel 1)
                Ej: "POST /api/tasks/:id/attachments multipart"
                Tamaño esperado: 50-200 líneas Python con argparse

CASO ESPECIAL → CARD (Nivel R Runtime)
─────────────────────────────────────────
¿Necesitas producir una versión comprimida del happy path de
UN Workflow para inyectar al prompt del agente?
   │
   └── SÍ → CARD (1:1 con su Workflow)
       Ej: "VTT.CARD-EXE-001 — Agente lee inputs iniciales"
       Tamaño esperado: 200-5000 tokens según tipo (chars/4)
       Header obligatorio: Aplica cuando + Requiere Cards previas + Tipo
       Path: 02.normativa/05.Cards/<categoria>/
       Registrar también en cards_catalog.json
```

> **Importante sobre CARD:** Una CARD NO es un quinto nivel paralelo a Protocol/Workflow/Skill/Script. Es una **vista runtime comprimida** del Workflow al que pertenece (1:1). El Workflow tiene el camino completo con ramificaciones y errores; la CARD condensa solo el happy path para el prompt.

### Tabla decisoria (criterios objetivos)

| Pregunta | Protocol | Workflow | Skill | Script |
|---|---|---|---|---|
| ¿Cubre proceso de negocio? | Sí (E2E) | Sí (sub-proceso) | No | No |
| ¿Tiene varias fases? | Sí (3+) | No (1 actividad) | No | No |
| ¿Involucra varios roles? | Sí | A veces | No (1 actor) | No |
| ¿Tiene decisiones de negocio? | Sí (mayores) | Sí (intermedias) | No | No |
| ¿Es atómico? | No | No | Parcial | Sí |
| ¿Reusable entre contextos? | Sí | Sí | **Siempre** | Siempre |
| ¿Tiene inputs contractuales fijos? | No | Sí | **Sí (estrictos)** | Sí (CLI args) |
| ¿Idempotente? | N/A | N/A | Cuando es posible | **Sí (obligatorio)** |
| Tamaño típico | 400-1000 líneas | 100-300 líneas | 50-150 líneas | 50-200 líneas |

### Casos límite frecuentes

#### Caso 1: "Es secuencial pero tiene decisiones"

Si el documento tiene **secuencia + decisiones internas pequeñas** ("si X entonces Y, si no Z") → es **Workflow**. Las decisiones "de negocio mayores" (involucran roles distintos, cambios de scope) son las que indican Protocol.

#### Caso 2: "Es reusable pero también tiene fases"

Si una Skill empieza a tener "fase A / fase B" → probablemente está creciendo a Workflow. **Las Skills no tienen fases**, son atómicas conceptualmente (aunque orquesten varios scripts).

#### Caso 3: "Es solo 1 curl"

Si es 1 curl o llamada HTTP y se invoca desde 1 solo lugar → considera inline en la Skill que lo necesita (sin crear Script aparte). Si se invoca desde 2+ Skills → vale la pena el Script separado.

---

## 3. Asignación de código

### Pattern de naming

```
VTT.<NIVEL>-<CAT>-<NNN>[.<MMM>]_<titulo_snake_case>.<ext>
```

| Componente | Reglas |
|---|---|
| `VTT` | Prefijo fijo |
| `<NIVEL>` | PROTOCOL / WORKFLOW / SKILL / SCRIPT (todo mayúsculas) |
| `<CAT>` | Categoría temática (ver §3.2) |
| `<NNN>` | 3 dígitos secuenciales (001, 002, ...) |
| `<MMM>` | 3 dígitos sub-id (solo Workflows que pertenecen a un Protocol) |
| `<titulo_snake_case>` | Descriptivo, minúsculas, separado por `_` |
| `<ext>` | `.md` (todos) o `.py` (Scripts) |

### Categorías estándar

> **Source of Truth:** `02.normativa/00_REGISTRO_ACRONIMOS.md` §3.

Ver la lista completa de categorías con descripción, dominio, reservado por y estado en el registro maestro. La tabla histórica que aquí aparecía se reemplazó por el registro centralizado para evitar drift entre múltiples archivos.

**Resumen rápido de categorías activas** (a 2026-05-17):

| `<CAT>` | Tema | Estado |
|---|---|---|
| `GOV` | Gobierno transversal | ✅ Activo |
| `ASG` | Asignación de tareas | ✅ Activo |
| `MAN` | Manifests (Task + Execution) | ✅ Activo |
| `ISS`, `TRK`, `LD`, `EVD`, `DEV`, `EST`, `VEL`, `RET`, `AUTH`, `TASK`, `ATTACH`, `STATUS`, `COMMENT`, `PB`, `QA`, `DB`, `GIT`, `FILE` | varios | ⚪ Reservado |

> **Si necesitas categoría nueva:**
> 1. Buscar primero en `00_REGISTRO_ACRONIMOS.md` §3.1 (activas) y §3.2 (bloqueadas).
> 2. Si no existe y no choca con nada → seguir el procedimiento de §5 del registro para agregarla.
> 3. **NO inventes** un acrónimo sin registrarlo — bloqueará el review.

### Cómo encontrar el `<NNN>` siguiente disponible

```bash
# Para Protocols
cd 00-platform/02.normativa/01.Protocols
ls VTT.PROTOCOL-<CAT>-*.md 2>/dev/null | sort
# Ejemplo: si existe VTT.PROTOCOL-ASG-001, el siguiente es 002

# Para Workflows derivados de un Protocol
ls VTT.WORKFLOW-ASG-001.*.md 2>/dev/null | sort
# Ejemplo: si existe .015, el siguiente es .016

# Para Skills
ls 00-platform/02.normativa/03.Skills/<categoria>/VTT.SKILL-<CAT>-*.md 2>/dev/null | sort

# Para Scripts
ls 00-platform/02.normativa/04.Scripts/<categoria>/VTT.SCRIPT-<CAT>-*.py 2>/dev/null | sort
```

### Ejemplos de naming válido

```
VTT.PROTOCOL-ASG-001_ciclo_asignacion_tarea.md
VTT.PROTOCOL-LD-001_living_documents.md
VTT.WORKFLOW-ASG-001.003_generar_y_subir_briefs.md
VTT.WORKFLOW-ASG-001.018_registrar_document_impacts.md
VTT.SKILL-ATTACH-001_subir_attachment_a_tarea.md
VTT.SKILL-TRK-002_vincular_trackable_item_a_tarea.md
VTT.SCRIPT-ATTACH-001_post_attachment_multipart.py
VTT.SCRIPT-AUTH-001_obtener_jwt_service_token.py
```

### Ejemplos de naming inválido

```
❌ vtt.protocol-asg-001.md           (debe ser mayúsculas en VTT y NIVEL)
❌ VTT.PROTOCOL-ASG-1_*.md            (NNN debe tener 3 dígitos: 001)
❌ VTT.PROTOCOL-001_*.md              (falta CAT)
❌ VTT.PROTOCOL-NUEVO-001_*.md        (CAT debe ser categoría estándar)
❌ VTT_PROTOCOL-ASG-001_*.md          (debe ser punto, no underscore después de VTT)
❌ VTT.WORKFLOW-ASG-001_*.md          (Workflow requiere .MMM)
❌ VTT.SKILL-ATTACH-001.001_*.md      (Skills NO llevan .MMM, son standalone)
```

---

## 4. Checklists por nivel

### 4.1 Checklist Protocol

Antes de publicar un Protocol nuevo, verifica todos estos puntos:

**Estructura:**
- [ ] Header con todos los campos (Código, Título, Versión, Fecha, Autor, Aplica a, Estado)
- [ ] §1 Propósito (1-2 párrafos respondiendo qué/por qué/output)
- [ ] §2 Campo de Aplicación (aplica a / no aplica a)
- [ ] §3 Responsabilidades por rol (no por persona)
- [ ] §4 Definiciones de términos clave
- [ ] §5 Procedimiento subdividido en fases con sub-pasos
- [ ] §6 Referencias Cruzadas (Workflows, Skills, Reglas, Templates)
- [ ] §7 Resumen de Revisiones con versión inicial
- [ ] Anexos (al menos diagrama mermaid recomendado)

**Calidad:**
- [ ] Cada paso marcado con `[ACTIVIDAD]`, `[PROCESO]` o `[DECISIÓN]`
- [ ] Pasos `[PROCESO]` referencian Workflow específico
- [ ] Pasos `[ACTIVIDAD]` referencian Skill específica
- [ ] Decisiones documentan ambos casos (SÍ / NO)
- [ ] Reglas Nivel 0 listadas en §6
- [ ] No mezcla niveles (todo es macro-procedimiento, sin instrucciones atómicas)

**Documental:**
- [ ] Borraste el bloque "Cómo usar" del template
- [ ] Placeholders `<...>` todos reemplazados (búscalos con grep)
- [ ] Footer con editor/dueño/fecha

### 4.2 Checklist Workflow

**Estructura:**
- [ ] Header indica `Pertenece a` (Protocol padre + §X.Y exacta)
- [ ] §1 Propósito (1-2 líneas)
- [ ] §2 Inputs con tabla (nombre + tipo + origen + requerido)
- [ ] §3 Precondiciones listadas
- [ ] §4 Reglas operativas del Workflow (distintas a las Reglas Nivel 0)
- [ ] §5 Pasos numerados (con decisiones intermedias si aplica)
- [ ] §6 Outputs con tabla (nombre + tipo + destino)
- [ ] §7 Validación de salida (comandos o checklist)
- [ ] §8 Errores comunes (tabla síntoma/causa/solución)
- [ ] §9 Skills invocadas listadas
- [ ] §10 Reglas Nivel 0 aplicables

**Calidad:**
- [ ] Cada paso que ejecuta acción invoca una Skill (no lógica inline)
- [ ] No hay decisiones de negocio mayores (esas van en Protocol padre)
- [ ] Inputs son contractuales (mismo formato siempre)
- [ ] Outputs son verificables

### 4.3 Checklist Skill

**Estructura:**
- [ ] Header con categoría + aplica a + tokens + cuándo
- [ ] Inputs contractuales (tabla con tipo + requerido)
- [ ] Precondición clara
- [ ] Variables del entorno listadas
- [ ] Ejecución (referencia a Script o lógica inline ≤5 líneas)
- [ ] Validación con códigos HTTP esperados
- [ ] Error común documentado
- [ ] Scripts invocados listados
- [ ] Changelog

**Calidad:**
- [ ] NO es específica del contexto (es reusable)
- [ ] Inputs NO cambian según contexto (son contractuales)
- [ ] Tokens estimados ≤ 200
- [ ] Si hay lógica >5 líneas, está extraída a Script aparte

### 4.4 Checklist Script

**Estructura:**
- [ ] Header docstring completo (Propósito + Idempotencia + Inputs + Outputs + Exit codes)
- [ ] argparse (no hardcode de inputs)
- [ ] Idempotencia documentada (Sí / No / Parcial + razón)
- [ ] Stdout en formato JSON
- [ ] Exit codes 0/1/2/3 documentados y usados
- [ ] Manejo de HTTPError + URLError + Exception genérico
- [ ] Encoding UTF-8 en Windows

**Calidad:**
- [ ] Sin secrets hardcoded (todo via env vars)
- [ ] Sin lógica de negocio (solo 1 acción atómica)
- [ ] Probado con al menos 1 caso real
- [ ] Manejo de errores no leak información sensible

### 4.5 Checklist CARD (Nivel R)

**Estructura:**
- [ ] Código `VTT.CARD-<CAT>-<NNN>` siguiendo pattern (CAT del workflow padre típicamente)
- [ ] Header con `Tipo` (CARD-mini/std/large/pack) declarado y consistente con tokens
- [ ] Header con `Aplica cuando` máquina-legible (`task.phase`/`agent.role`/`task.category` + operadores)
- [ ] Header con `Requiere Cards previas` (lista de CARD IDs o `ninguna`)
- [ ] Header con `Pertenece a` apuntando al Workflow padre (1:1)
- [ ] Header con `Tokens estimados` medidos con chars/4 (no estimados a ojo)
- [ ] Cuerpo: solo happy path comprimido (sin ramificaciones complejas — esas viven en el Workflow)
- [ ] Sección "Si falla" con tabla compacta de errores comunes + acción inmediata
- [ ] Sección "Output" indica estado consistente al terminar + CARD siguiente si encadenada

**Calidad:**
- [ ] Tokens medidos dentro del rango del tipo declarado (ver §4.6)
- [ ] Si supera hard cap → upgrade al siguiente tipo o partir en 2 CARDs (NO se negocia el tope)
- [ ] Apunta al Workflow padre como referencia documental (no como invocación)
- [ ] Encadenamiento explícito si aplica ("Listo para `CARD-XYZ-NNN`")
- [ ] Bash/comandos inline son los del happy path, no exhaustivos

**Catálogo:**
- [ ] Entrada agregada a `02.normativa/05.Cards/cards_catalog.json` con:
  - `id`, `title`, `category`, `type`, `tokens_measured`, `tokens_measured_at`
  - `applies_when`, `requires_prior`, `consumer` (agent/tl/pm/pjm)
  - `trigger`, `output`, `status: "done"`, `path`
  - `references` (protocol/workflow/skill/script)
- [ ] README de la categoría (`05.Cards/<categoria>/README.md`) actualizado
- [ ] Si categoría es nueva → registrada en `00_REGISTRO_ACRONIMOS.md` §3.1

### 4.6 Presupuesto de tokens canónico (chars/4)

**Estimador canónico VTT:** `chars/4` (conservador). Aplica a CARDs y a budget runtime del Prompt Builder.

> Auxiliar `words×1.33` solo de referencia, NO para decisiones de budget.

**Cómo medir:**

```bash
# Tokens estimados de un archivo
python -c "print(open('VTT.CARD-EXE-001_...md').read().__len__() // 4)"
```

**Tabla de tipos:**

| Tipo | Target | Hard cap | Cuándo usar |
|---|---|---|---|
| `CARD-mini` | 200-500 tok | **700** | Pasos atómicos, validaciones simples, transiciones de status |
| `CARD-std` | 500-1200 tok | **1500** | Procesos con varias decisiones simples (ej. revisar LDs, registrar Document Impacts) |
| `CARD-large` | 1200-2500 tok | **3000** | Procesos con sub-pasos múltiples (ej. ejecutar workflow del ASSIGNMENT con 13 pasos) |
| `CARD-pack` | 2500-4500 tok | **5000** | Solo si NO se puede partir; típicamente nunca |

**Reglas:**

1. **Si excede el hard cap del tipo declarado** → upgrade al siguiente tipo (NO se negocia).
2. **Si excede el hard cap del `CARD-pack`** → partir en 2 CARDs encadenadas (ej. `CARD-EXE-004a` ejecución + `CARD-EXE-004b` entrega).
3. **El campo `tokens_measured` en `cards_catalog.json`** debe coincidir con el medido. Si la CARD se actualiza y cambian los tokens → re-medir + actualizar `tokens_measured_at`.
4. **Opción A (1:1 CARD por workflow)** confirmada por PM (2026-05-30). NO consolidar packs cruzados de varios workflows.

---

## 5. Anti-patterns con ejemplos

### Anti-pattern 1 — Skill específica del contexto

**❌ Mal:** crear una Skill por cada tipo de archivo a subir.

```
SKILL-BRIEF-UPLOAD-001         "Subir BRIEF a tarea"
SKILL-ASSIGNMENT-UPLOAD-001    "Subir ASSIGNMENT a tarea"
SKILL-DEVLOG-UPLOAD-001        "Subir devlog a tarea"
SKILL-MANIFEST-UPLOAD-001      "Subir manifest a tarea"
SKILL-CODELOGIC-UPLOAD-001     "Subir code logic a tarea"
```

Resultado: **5 Skills haciendo casi lo mismo**.

**✅ Bien:** una Skill genérica con parámetro `file_type`.

```
SKILL-ATTACH-001 "Subir attachment a tarea"
   Inputs: task_id, file_path, file_type, uploaded_by
   → 1 Skill reusable; el Workflow le pasa file_type='brief' / 'assignment' / 'devlog' / ...
```

**Regla:** Si te tienta crear `SKILL-XXX-UPLOAD` específica de algo, la lógica del "qué subir" pertenece al **Workflow** que la invoca, no a una Skill nueva.

### Anti-pattern 2 — Mezclar niveles

**❌ Mal:** documento llamado "Protocol" pero que solo tiene pasos secuenciales sin decisiones de negocio.

```
# VTT.PROTOCOL-BRIEF-001 — Generar BRIEF

§5 Procedimiento
  5.1 Lee el handoff
  5.2 Identifica la tarea
  5.3 Llena template
  5.4 Sube como attachment
```

Esto **no es un Protocol** — no tiene fases, no hay decisiones de negocio, no involucra múltiples roles. Es un **Workflow**.

**✅ Bien:** moverlo a Workflow del Protocol padre.

```
# VTT.WORKFLOW-ASG-001.003 — Generar y subir BRIEFs
Pertenece a: VTT.PROTOCOL-ASG-001 §5.1.9
```

### Anti-pattern 3 — Script con lógica de negocio

**❌ Mal:** un Script de 200 líneas que decide qué endpoint llamar según el contexto.

```python
# VTT.SCRIPT-TASK-FANCY.py
if task.category == 'feature' and task.has_endpoints:
    # POST /api/tasks/:id/criteria con CA de Swagger
    ...
elif task.category == 'documentation':
    # No requiere CAs especiales
    ...
elif task.assignee == 'BE':
    # Crear Delivery específico
    ...
```

**✅ Bien:** Script atómico de 50 líneas que hace 1 cosa.

```python
# VTT.SCRIPT-CRITERIA-001.py
# POST /api/tasks/:id/criteria con el body recibido como argumento
```

La lógica de "qué CAs crear según contexto" vive en el **Workflow** que orquesta varias llamadas al Script.

### Anti-pattern 4 — Workflow sin inputs/outputs claros

**❌ Mal:** Workflow con pasos vagos.

```
Paso 1: configurar el entorno
Paso 2: ejecutar la tarea
Paso 3: revisar resultados
```

Imposible ejecutarlo determinísticamente. No hay inputs, no hay outputs, no se sabe qué Skill invocar.

**✅ Bien:** Workflow con pasos accionables.

```
§2 Inputs
   task_id (string): ej. "MS-285"
   agent_uuid (UUID): del agente que ejecutará

§5 Pasos
Paso 1 — Obtener TOKEN
   → invoca SKL-AUTH-001 con (agent_uuid=$agent_uuid)
Paso 2 — Crear branch
   → invoca SKL-GIT-001 con (task_id=$task_id, base="origin/main")
Paso 3 — Verificar worktree del rol
   → invoca SKL-WT-001 con (role=$agent_role)
```

### Anti-pattern 5 — Copiar template sin borrar instrucciones del autor

**❌ Mal:** El documento publicado mantiene el bloque inicial del template.

```markdown
# TEMPLATE_PROTOCOL — Molde para crear un Protocol nuevo (Nivel 4)

> Cómo usar: copia este archivo a 02.normativa/01.Protocols/ con nombre...

# VTT.PROTOCOL-XXX-001 — Mi protocol nuevo
...
```

El bloque `> Cómo usar...` debe **borrarse** al publicar. El documento final empieza directamente con el header del Protocol.

**✅ Bien:** documento limpio, sin metadata del template.

### Anti-pattern 6 — Versiones sin changelog

**❌ Mal:** Documento que llegó a v3.5 pero el `Resumen de Revisiones` solo dice "Versión inicial".

**✅ Bien:** Cada bump de versión deja una entrada en §7 con fecha, editor y resumen del cambio.

```
| Versión | Fecha | Editor | Cambios |
|---|---|---|---|
| 1.0.0 | 2026-05-13 | PM | Versión inicial |
| 1.1.0 | 2026-05-13 | PM | Agregadas 7 features faltantes... |
| 1.2.0 | 2026-05-14 | PM | Cambio modelo worktrees: por tarea → por rol... |
```

### Anti-pattern 7 — Documentos sin referencias cruzadas

**❌ Mal:** Crear un Workflow sin actualizar la tabla §6 del Protocol padre.

Resultado: el documento existe pero **nadie lo encuentra** porque no se referencia desde ningún lado.

**✅ Bien:** al crear un Workflow nuevo:
1. Crear el archivo
2. Actualizar §6 del Protocol padre con su entrada
3. Actualizar INVENTARIO.md

### Anti-pattern 8 — Reglas Nivel 0 ignoradas

**❌ Mal:** Escribir un Protocol/Workflow que viola reglas existentes del catálogo (`rules_catalog.json`).

Ejemplo: un Workflow que dice "el TL hace commit directo a main" — viola `RULE-GIT-004` (Prohibido commit directo a main).

**✅ Bien:** antes de escribir, ejecutar:

```bash
python 00.Rules/query_rules.py --simulate-task <ejemplo>
```

Y asegurar que el procedimiento respeta las reglas aplicables.

---

## 6. Workflow del autor

Del borrador a la publicación, 10 pasos:

```
[1] Identificar necesidad de documento nuevo
    → ¿Resuelve un gap real? ¿Ya existe algo similar?

[2] Decidir nivel (Protocol / Workflow / Skill / Script)
    → Usar §2 árbol de decisión

[3] Asignar código (CAT + NNN siguiente)
    → Usar §3 + buscar en carpeta destino

[4] Copiar template desde _autoria/
    cp 03.templates/normativa/_autoria/TEMPLATE_<NIVEL>.md \
       02.normativa/<carpeta>/VTT.<NIVEL>-<CAT>-<NNN>_<titulo>.md

[5] Rellenar placeholders <...>
    → Mantener convención de marcado [ACTIVIDAD]/[PROCESO]/[DECISIÓN] en Protocols/Workflows

[6] Borrar bloque "Cómo usar" del template
    → El documento publicado empieza con el header

[7] Validar contra checklist del nivel (§4 de esta guía)

[8] Identificar Reglas Nivel 0 aplicables
    → query_rules.py --simulate-task <contexto>
    → Listar en §6/§10 del documento

[9] Actualizar referencias cruzadas
    → INVENTARIO.md
    → §6 del Protocol padre (si es Workflow)
    → Documento que invoca (si es Skill/Script)

[10] Notificar
    → PM si es Protocol nuevo
    → TL si es Workflow/Skill/Script
```

---

## 7. Reglas Nivel 0 — cómo identificar las aplicables

Cada documento normativo opera bajo restricciones del Nivel 0. **Identifícalas antes de escribir**, no después.

### Cómo descubrir reglas aplicables

```bash
cd 00-platform/02.normativa/00.Rules

# Listar todas las reglas
python query_rules.py --list

# Simular reglas aplicables a una tarea típica
python query_rules.py --simulate-task MS-285

# Probar con contexto custom (JSON inline)
python query_rules.py --context-json '{
    "actor_type": "AGENT",
    "actor_role": "ws_developer",
    "actor_capabilities": ["tasks.read", "tasks.update"],
    "project_id": "memory-service",
    "phase_id": "04-Development",
    "phase_key": "04",
    "task": {
        "id": "MS-XXX",
        "has_code_files": true,
        "has_endpoints": false,
        "creates_assignment": false
    }
}'
```

### Reglas críticas que SIEMPRE consideres

Estas reglas aplican a casi cualquier Protocol/Workflow:

| Regla | Aplica cuando |
|---|---|
| `RULE-AGENT-001` Worktree por rol | Cualquier acción del agente en código |
| `RULE-GIT-004` Prohibido commit a main | Cualquier modificación de código |
| `RULE-DATA-001` Prohibido mockear datos | Tareas con dependencias de datos reales |
| `RULE-ABAC-007` `tasks.approve` solo HUMAN | Cualquier flow de aprobación |
| `RULE-ABAC-009` Agente nunca aprueba | Cualquier acción de agente sobre task_approved |
| `RULE-VTT-004` Manifest AL FINAL | Cualquier proceso de cierre de tarea |

### Cómo documentar las reglas en tu documento

En el **Protocol**: tabla en §6 "Reglas Nivel 0 aplicables".

En el **Workflow**: tabla en §10 con "Razón" (por qué aplica aquí).

En la **Skill**: si la skill ejerce una capability sensible, mencionar regla en `Precondición`.

En el **Script**: si tiene comportamiento idempotente o de auditoría, mencionar la regla en docstring.

---

## 8. Versionado

### Esquemas por nivel

| Nivel | Esquema | Cuándo bumpear |
|---|---|---|
| Protocol | SemVer (X.Y.Z) | Cambio de proceso |
| Workflow | SemVer (X.Y.Z) | Cambio de pasos o contratos |
| Skill | Incremental (v1, v2) | Cambio de inputs/outputs contractuales |
| Script | Incremental (v1, v2) | Cambio de comportamiento (no de refactor interno) |

### SemVer (Protocol / Workflow)

| Cambio | Tipo | Ejemplo |
|---|---|---|
| Major (X.0.0) | Cambio incompatible | Agregar fase obligatoria nueva, cambiar contratos de inputs |
| Minor (1.X.0) | Funcionalidad nueva compatible | Paso opcional adicional, anexo nuevo |
| Patch (1.0.X) | Aclaración o fix | Corregir typo, ejemplo nuevo, link roto |

### Incremental (Skill / Script)

| Cambio | Acción |
|---|---|
| Cambia contrato (inputs/outputs) | Nueva versión: `SKILL-XXX-001_v2` |
| Mejora interna sin romper | Mismo número, actualizar fecha en changelog |
| Bug fix | Mismo número, entrada en changelog |

### Política de retrocompatibilidad

**Protocols y Workflows con cambio major:**
- Mantener versión anterior accesible durante 1 sprint (no borrar)
- Marcar como `Deprecated` en el header
- Mover a `_pending-migration/_archived/` solo cuando confirmar que nadie la usa

**Skills y Scripts con nueva versión:**
- Coexisten v1 y v2 hasta que todas las invocaciones migren
- Documentar en el changelog qué Workflows aún usan v1

---

## 9. Después de publicar

### 9.1 Checklist post-publicación

```
[ ] Documento subido a la carpeta correcta
[ ] INVENTARIO.md actualizado con entrada nueva
[ ] §6 del Protocol padre actualizado (si es Workflow)
[ ] Si crea categoría nueva → agregada a README.md §4.2
[ ] Si introduce regla nueva → agregada a rules_catalog.json
[ ] PM notificado (si es Protocol)
[ ] TL notificado (si es Workflow/Skill/Script de un Protocol)
```

### 9.2 Mantenimiento ongoing

| Frecuencia | Acción |
|---|---|
| Cuando lo edites | Bump versión + entrada en changelog |
| Al cerrar sprint | Revisar si tu documento necesita ajustes por lecciones del sprint |
| Cuando se deprecia | Cambiar `Estado: Deprecated` + mover a `_pending-migration/_archived/` |

### 9.3 Notificación a equipos consumidores

Si el documento es consumido por agentes activos (ej. cambia un Workflow del Protocol ASG):

1. Comentar en el canal del equipo
2. Si el cambio es **breaking** (major), pausar las tareas en progreso hasta validar
3. Si el cambio es **menor**, los agentes lo recogerán en su próxima sesión

---

## 10. FAQ

### ¿Puedo crear un documento sin código aún (solo descripción)?

Sí. Marca `Estado: Borrador` en el header. Cuando esté listo, cambia a `Aprobado`.

### Mi Workflow es muy corto (3 pasos). ¿Vale la pena crearlo?

Si es **reusable desde varios Protocols** o tiene **inputs/outputs contractuales claros**, sí. Si solo se usa una vez y no tiene contrato → considera inline en el Protocol.

### ¿Puedo tener Skills sin Scripts?

Sí, si la lógica es ≤5 líneas inline (curl simple). Si tiene >5 líneas o se invoca desde varias Skills, extraer a Script.

### ¿Cuándo creo categoría nueva (`<CAT>`)?

Cuando ningún `<CAT>` existente captura semánticamente el tema. Antes de crear, verifica que **no caiga** en una existente. Documentarla primero en `README.md` §4.2.

### Mi Protocol depende de otro Protocol. ¿Cómo lo documento?

En §6 Referencias Cruzadas tabla "Protocols relacionados". Especifica la relación: `upstream / downstream / paralelo`.

### ¿Las Skills/Scripts también necesitan reglas Nivel 0?

Las Skills sí (mencionar en `Precondición` si ejerce capability sensible). Los Scripts solo si tienen comportamiento auditable (idempotencia, side effects sensibles).

### ¿Qué hago con los SOPs legacy de `_pending-migration/`?

Cuando vayas a usar uno, **migra primero**:
1. Copia el contenido al template adecuado (Protocol / Workflow / Skill)
2. Rellena estructura VTT
3. Asigna código `VTT.<NIVEL>-<CAT>-<NNN>`
4. Mueve el legacy a `_pending-migration/_archived/` (no borrar)
5. Actualiza INVENTARIO

### ¿Hay un template que falte?

Hoy tenemos: TEMPLATE_PROTOCOL, TEMPLATE_WORKFLOW, TEMPLATE_SKILL, TEMPLATE_SCRIPT. Si necesitas otro tipo (ej. TEMPLATE_RULE para definir reglas Nivel 0), avisar al PM.

### ¿Puedo modificar un template?

Sí, pero coordina con el PM. Cambios al template afectan a TODOS los autores futuros.

### ¿Dónde reporto problemas con esta guía?

Por ahora: directo al PM. Cuando exista un sistema de tickets de mejora → ahí.

---

## 11. Recursos relacionados

| Documento | Función |
|---|---|
| `02.normativa/README.md` | Modelo conceptual de 4 niveles + Nivel 0 |
| `02.normativa/INVENTARIO.md` | Qué documentos existen y dónde |
| `03.templates/normativa/_autoria/` | Los 4 templates concretos (Protocol/Workflow/Skill/Script) |
| `03.templates/normativa/_autoria/README.md` | Cómo usar cada template (5 pasos) |
| `00.Rules/README.md` | Sistema de Reglas Nivel 0 |
| `00.Rules/query_rules.py` | Motor de consulta de reglas aplicables |
| Ejemplo Protocol real | `01.Protocols/VTT.PROTOCOL-ASG-001_*.md` |

---

## 12. Changelog

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-05-17 | Versión inicial — checklist por nivel + 8 anti-patterns + workflow del autor + FAQ |
| 1.1 | 2026-05-31 | **Tratamiento del Nivel R CARD agregado.** §2 árbol de decisión ampliado con CASO ESPECIAL CARD (no es 5to nivel paralelo, es vista runtime 1:1 con Workflow). §4.5 NUEVA: Checklist CARD (estructura + calidad + catálogo + ACRONIMOS). §4.6 NUEVA: Presupuesto de tokens canónico chars/4 con tabla de 4 tipos + reglas de hard cap + Opción A 1:1 confirmada por PM. Referencias cruzadas a `README.md` §2.4.bis (modelo conceptual CARD) y §8.bis (estructura obligatoria CARD). Por PM Martin Rivas. |
