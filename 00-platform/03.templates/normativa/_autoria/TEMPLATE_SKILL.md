# TEMPLATE_SKILL — Molde para crear una Skill nueva (Nivel 2)

> **Cómo usar:** copia este archivo a `02.normativa/03.Skills/<categoria>/` con nombre `VTT.SKILL-<CAT>-<NNN>_<titulo_snake>.md`. Reemplaza los placeholders `<...>`. Borra esta sección de instrucciones antes de publicar.
>
> **Antes de empezar:** verifica que es realmente una Skill (Nivel 2 — capacidad reusable con inputs/outputs contractuales). Si es 1 comando atómico → es un Script. Si tiene decisiones de negocio → es un Workflow.
>
> **Regla de reutilización:** las Skills NO son específicas del contexto. Si te tienta crear `SKL-BRIEF-UPLOAD`, esa lógica pertenece al Workflow. Crea `SKL-ATTACH-01` (genérico) y deja que el Workflow le pase el parámetro específico.
>
> **Referencias:**
> - `02.normativa/README.md` §3 — Tabla decisoria
> - `02.normativa/README.md` §7 — Estructura obligatoria del Skill
> - `02.normativa/GUIA_AUTOR.md` — Anti-pattern de skill específica del contexto
> - Ejemplos reales: `02.normativa/03.Skills/_pending-migration/`

---

# VTT.SKILL-<CAT>-<NNN> — <Título descriptivo>

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-<CAT>-<NNN>` |
| **Categoría** | <AUTH / TASK / STATUS / QUERY / COMMENT / DEVLOG / ATTACH / TRACK / GIT / REPORT / MANIFEST / DYNAMIC-MODEL / FILE / STRUCTURE / MESSAGE> |
| **Versión** | 1.0 |
| **Fecha** | YYYY-MM-DD |
| **Aplica a** | <rol específico o "Todos"> |
| **Tokens estimados** | ~XXX |
| **Cuándo se usa** | <una línea — momento específico de invocación> |

---

## Inputs (contractuales)

Parámetros que la Skill recibe SIEMPRE de igual forma, independiente de quién la invoque:

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `<input_1>` | <string / uuid / path / json / enum> | sí | <qué contiene + formato> |
| `<input_2>` | <tipo> | sí/no | <...> |

> **Regla contractual:** estos inputs son fijos. Si una Skill necesita más parámetros para "ajustarse al contexto", probablemente está mal diseñada — la lógica de contexto debe vivir en el Workflow que la invoca.

---

## Precondición

Condiciones que deben ser verdaderas ANTES de ejecutar esta Skill:

- <Condición 1 — ej. "JWT válido obtenido (`SKL-AUTH-01`)">
- <Condición 2 — ej. "El recurso destino existe en VTT">
- <Condición 3 — ej. "El input `<X>` cumple el formato esperado">

---

## Variables del entorno

Variables que la Skill lee de `os.environ` o configuración local:

```bash
$TOKEN              # JWT de la sesión actual
$VTT_BASE_URL       # Base URL del backend VTT
$AGENT_UUID         # UUID del actor que invoca
$PROJECT_ID         # UUID del proyecto (si aplica)
$SERVICE_KEY        # Service key (solo para AUTH-01)
```

> **Política:** las skills referencian env vars genéricas. Los UUIDs específicos del proyecto (TaskID, DeliveryID) son **inputs**, no env vars.

---

## Ejecución

<Descripción breve (1-3 líneas) de lo que hace la Skill orquestando Scripts.>

### Comando(s)

```bash
# Llamada principal
python <path>/VTT.SCRIPT-<CAT>-<NNN>.py \
  --param1="$<input_1>" \
  --param2="$<input_2>"
```

O en Python si la Skill ejecuta lógica directamente:

```python
import urllib.request, json, os

req = urllib.request.Request(
    f"{os.environ['VTT_BASE_URL']}/api/<endpoint>",
    data=json.dumps({
        '<field_1>': '<input_1>',
        '<field_2>': '<input_2>'
    }).encode(),
    headers={'Authorization': f"Bearer {os.environ['TOKEN']}",
             'Content-Type': 'application/json'},
    method='POST'
)
response = json.loads(urllib.request.urlopen(req).read())
```

> **Política:** Skills con curl ≤5 líneas pueden ser inline. Skills con lógica compleja deben invocar un Script (Nivel 1) para mantener el código atómico y reusable.

---

## Validación

Cómo saber si la Skill funcionó:

- HTTP <código esperado> (ej. `201` para POST, `200` para GET, `204` para DELETE)
- Response tiene campo `<X>` (ej. `data.id` es UUID válido)
- Side effect verificable (ej. `GET /api/.../verificar` retorna el resultado)

```bash
# Comando de validación post-ejecución
curl -s "$VTT_BASE_URL/api/<endpoint>" -H "Authorization: Bearer $TOKEN" | jq '.data.id'
```

---

## Error común

| Error | Causa probable | Solución |
|---|---|---|
| HTTP 400 `<mensaje>` | <causa> | <fix> |
| HTTP 401 Unauthorized | TOKEN expirado | Renovar con `SKL-AUTH-01` |
| HTTP 404 Not Found | Endpoint o recurso inexistente | Verificar `<X>` + path correcto |
| Validation error: `<campo>` requerido | Input faltante | Asegurar que el Workflow padre pase todos los inputs contractuales |

---

## Scripts invocados

Scripts atómicos que esta Skill orquesta:

- `VTT.SCRIPT-<CAT>-<NNN>` — <para qué>
- `VTT.SCRIPT-<CAT>-<NNN>` — <...>

> Si la Skill tiene lógica inline (sin Scripts), documentar aquí: "Sin Scripts externos — lógica inline en sección Ejecución".

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | YYYY-MM-DD | Versión inicial. <Resumen>. |

> **Política de versionado** (Incremental):
> - **v1, v2, v3...** — incremento por cambio de contrato (inputs/outputs) o de comportamiento mayor.
> - Mejoras internas que no cambian el contrato → misma versión, actualizar fecha.
