# TEMPLATE_WORKFLOW — Molde para crear un Workflow nuevo (Nivel 3)

> **Cómo usar:** copia este archivo a `02.normativa/02.Workflows/` con nombre `VTT.WORKFLOW-<CAT>-<NNN>.<MMM>_<titulo_snake>.md`. Reemplaza los placeholders `<...>`. Borra esta sección de instrucciones antes de publicar.
>
> **Antes de empezar:** verifica que es realmente un Workflow (Nivel 3 — sub-proceso con pasos secuenciales fijos, sin decisiones de negocio mayores). Si tiene decisiones de negocio multi-rol → es un Protocol. Si es una capacidad reusable parametrizada → es una Skill.
>
> **Pertenencia:** un Workflow SIEMPRE pertenece a un Protocol padre. El `<MMM>` se asigna según el orden dentro del Protocol (`.001`, `.002`, etc.).
>
> **Referencias:**
> - `02.normativa/README.md` §3 — Tabla decisoria (Workflow vs Skill)
> - `02.normativa/README.md` §6 — Estructura obligatoria del Workflow
> - `02.normativa/GUIA_AUTOR.md` — Anti-patterns
> - Ejemplos reales: cuando existan en `02.normativa/02.Workflows/`

---

# VTT.WORKFLOW-<CAT>-<NNN>.<MMM> — <Título descriptivo>

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-<CAT>-<NNN>.<MMM>` |
| **Pertenece a** | `VTT.PROTOCOL-<CAT>-<NNN>` §<X.Y> |
| **Versión** | 1.0.0 |
| **Fecha** | YYYY-MM-DD |
| **Autor** | <Nombre + rol> |
| **Aplica a** | <rol que ejecuta> |
| **Tipo** | [PROCESO] sub-procedimiento — invocado por Protocol padre |

---

## 1. Propósito

<1-2 líneas. Qué hace este Workflow y por qué se invoca.>

> **Ejemplo:** "Validar que el handoff recibido del PJM tiene todos los inputs requeridos (briefs por agente, dependencias, CAs verificables, gates) antes de iniciar la planificación del sprint."

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `<input_1>` | <string / uuid / path / json> | <paso del Protocol que lo provee> | sí | <qué contiene> |
| `<input_2>` | <tipo> | <origen> | sí/no | <...> |

> **Tip:** sé estricto. Si un input es opcional, marcarlo "no" y documentar el comportamiento default.

---

## 3. Precondiciones

Condiciones que deben ser verdaderas ANTES de ejecutar este Workflow:

- <Condición 1 — ej. "Existe `HANDOFF_TL_S[N].md` en el repo">
- <Condición 2 — ej. "TL tiene JWT válido (`SKL-AUTH-01` ya ejecutado)">
- <Condición 3 — ej. "Sprint anterior está en `task_approved`">

> **Si una precondición falla:** documentar en §8 Errores comunes el comportamiento esperado.

---

## 4. Reglas del Workflow

Reglas operativas que aplican durante la ejecución de este Workflow (distintas a las Reglas Nivel 0):

- **Regla 1:** <ej. "El BRIEF es inmutable — no se edita después de crearlo">
- **Regla 2:** <ej. "Usar template `TEMPLATE_BRIEF_LARGE.md`">
- **Convenciones:** <paths, naming, formato>

---

## 5. Pasos

### Paso 1 — <Acción concisa>

<Descripción del paso (1-3 líneas).>

<Decisiones intermedias del paso, si las hay.>

→ invoca **`VTT.SKILL-<CAT>-<NNN>`** con (`param1=valor`, `param2=valor`)

### Paso 2 — <Acción>

<...>

¿<Pregunta de decisión>? →
- **SÍ** → Paso 3
- **NO** → Paso 5 (saltar la validación)

### Paso 3 — <Acción>

<...>

### Paso N — <Acción final>

<...>

> **Convención:**
> - Pasos numerados secuencialmente (1, 2, 3...).
> - Cada paso ≤ 1 párrafo. Si necesita más, probablemente debería ser su propio Workflow.
> - Si un paso requiere lógica de decisión compleja, documentarlo como `¿pregunta? → SÍ/NO`.
> - Cada paso que invoca acción externa cita la Skill (`→ invoca VTT.SKILL-XXX-NNN`).

---

## 6. Outputs

| Nombre | Tipo | Destino | Descripción |
|---|---|---|---|
| `<output_1>` | <archivo / record VTT / variable> | <dónde queda> | <qué contiene> |
| `<output_2>` | <...> | <...> | <...> |

---

## 7. Validación de salida

Comandos o checks que confirman que el Workflow terminó correctamente:

```bash
# Check 1: <descripción>
<comando o query>
# Esperado: <resultado>

# Check 2: <descripción>
<...>
```

O lista verificable:

- [ ] <Output 1 existe en <destino>>
- [ ] <Status en VTT cambió a <X>>
- [ ] <Archivo tiene formato correcto>

---

## 8. Errores comunes

| Síntoma | Causa probable | Solución |
|---|---|---|
| <error A> | <causa> | <fix> |
| <error B> | <causa> | <fix> |

---

## 9. Skills invocadas

Lista de skills que este Workflow invoca:

- `VTT.SKILL-<CAT>-<NNN>` — <para qué se usa en este Workflow>
- `VTT.SKILL-<CAT>-<NNN>` — <...>

> Si una skill no existe aún, registrarla como pendiente en `02.normativa/03.Skills/_pending-migration/` o crear nueva siguiendo `TEMPLATE_SKILL.md`.

---

## 10. Reglas Nivel 0 aplicables

Reglas del catálogo `rules_catalog.json` que aplican específicamente cuando se ejecuta este Workflow:

| Regla | Razón |
|---|---|
| `RULE-XXX-NNN` <título> | <por qué aplica aquí> |

> Para descubrir reglas aplicables: `python 00.Rules/query_rules.py --context-json '{...}'` con el contexto del Workflow.

---

## 11. Changelog

| Versión | Fecha | Editor | Cambios |
|---|---|---|---|
| 1.0.0 | YYYY-MM-DD | <Nombre> | Versión inicial. <Resumen>. |
