# TEMPLATE_CARD — Autoría de CARDs (Nivel R Runtime)

> Plantilla canónica para producir una CARD (Nivel R) del modelo normativo VTT.
>
> **Antes de usar este template:**
> 1. Leer `02.normativa/README.md` §2.4.bis (modelo conceptual del Nivel R) y §8.bis (estructura obligatoria)
> 2. Leer `02.normativa/GUIA_AUTOR.md` §2 (decisión nivel) + §4.5 (Checklist CARD) + §4.6 (Presupuesto tokens)
> 3. Verificar que existe el **Workflow padre** (las CARDs son 1:1 con su Workflow)
> 4. Decidir el `Tipo` aproximado según presupuesto esperado
>
> **Cómo usar este template:**
> 1. Copiar este archivo a la carpeta destino: `02.normativa/05.Cards/<categoria>/`
> 2. Renombrar a `VTT.CARD-<CAT>-<NNN>_<titulo_snake_case>.md`
> 3. Reemplazar TODOS los placeholders `<...>` con valores reales
> 4. Borrar este bloque "Cómo usar" antes de publicar
> 5. Medir tokens con `chars/4` y ajustar el `Tipo` si no encaja en el rango
> 6. Agregar entrada a `02.normativa/05.Cards/cards_catalog.json`
> 7. Actualizar `02.normativa/05.Cards/<categoria>/README.md`
> 8. Si la categoría es nueva → registrarla en `00_REGISTRO_ACRONIMOS.md` §3.1

---

# VTT.CARD-<CAT>-<NNN> — <Título corto (1 línea)>

| Campo | Valor |
|---|---|
| **Código** | `VTT.CARD-<CAT>-<NNN>` |
| **Tipo** | `CARD-mini` / `CARD-std` / `CARD-large` / `CARD-pack` |
| **Versión** | 1.0 |
| **Aplica cuando** | `<expresión lógica máquina-legible>` |
| **Requiere Cards previas** | `<CARD-XYZ-NNN, CARD-ABC-MMM>` o `ninguna` |
| **Pertenece a** | `WORKFLOW-<CAT>-<NNN>.<MMM>` |
| **Tokens estimados** | ~<NNN> (medidos con chars/4 el YYYY-MM-DD) |

---

## Qué hacer

<Happy path comprimido del workflow padre. Sin ramificaciones complejas. Solo el camino exitoso.>

<Comandos bash inline si aplica — los del happy path, NO exhaustivos.>

```bash
# Comando 1 del happy path
<comando>

# Comando 2
<comando>
```

## Si falla

| Síntoma | Acción inmediata |
|---|---|
| <error 1> | <acción 1> |
| <error 2> | <acción 2> |

## Output

<Estado consistente que la CARD deja al terminar. Qué información queda disponible para la siguiente CARD o paso.>

<Si encadenada: "Listo para `CARD-XYZ-NNN`">

---

<!--
=== INSTRUCCIONES PARA EL AUTOR — BORRAR ANTES DE PUBLICAR ===

GRAMÁTICA DEL CAMPO "Aplica cuando":

Operadores válidos: =, IN [...], AND, OR

Campos válidos:
  - task.phase ∈ {assignment, execution_start, execution, closing, review, approval}
  - agent.role ∈ {BE, DB, FE, DO, QA, DL, UX, AR, SA, TL, PM, PJM}
  - task.category ∈ {development, deployment, devops, documentation, testing, design, bugfix}

Ejemplos válidos:
  - task.phase = closing AND agent.role IN [BE,DB,FE,DO,QA,DL,UX,AR,SA]
  - task.phase = execution_start AND agent.role IN [BE,DB,FE]
  - task.phase = review AND agent.role = TL

PRESUPUESTO POR TIPO (chars/4 canónico):

| Tipo         | Target          | Hard cap |
|--------------|-----------------|----------|
| CARD-mini    | 200-500 tok     | 700      |
| CARD-std     | 500-1200 tok    | 1500     |
| CARD-large   | 1200-2500 tok   | 3000     |
| CARD-pack    | 2500-4500 tok   | 5000     |

REGLA ABSOLUTA: Si excedés el hard cap → upgrade al siguiente tipo
o partí en 2 CARDs encadenadas. NO se negocia el tope.

CÓMO MEDIR:
  python -c "print(open('VTT.CARD-<...>.md').read().__len__() // 4)"

VALIDACIÓN POST-MEDICIÓN:
  - Si tokens dentro del target → Tipo OK
  - Si tokens entre target y hard cap → Tipo OK pero considerar limpieza
  - Si tokens > hard cap → upgrade obligatorio o partir

ENTRADA EN cards_catalog.json (agregar al final del array "cards"):

{
  "id": "CARD-<CAT>-<NNN>",
  "title": "<título descriptivo>",
  "category": "<categoria lowercase>",
  "type": "CARD-<mini|std|large|pack>",
  "tokens_measured": <NNN>,
  "tokens_measured_at": "YYYY-MM-DD",
  "applies_when": "<expresión copiada del header>",
  "requires_prior": ["CARD-XYZ-NNN"],
  "consumer": "<agent|tl|pm|pjm>",
  "trigger": "<descripción del momento de activación>",
  "output": "<estado consistente al terminar>",
  "status": "done",
  "path": "05.Cards/<categoria>/VTT.CARD-<CAT>-<NNN>_<titulo>.md",
  "references": {
    "protocol": "PROTOCOL-<CAT>-<NNN> §X.Y",
    "workflow": "WORKFLOW-<CAT>-<NNN>.<MMM>",
    "skill": "SKILL-<CAT>-<NNN>",
    "script": "SCRIPT-<CAT>-<NNN>"
  }
}

ANTI-PATTERNS A EVITAR:

❌ Duplicar el contenido completo del Workflow — la CARD es SOLO happy path
❌ Incluir ramificaciones complejas tipo "si X entonces Y, sino Z, salvo W"
❌ Hardcodear UUIDs o paths específicos de un proyecto
❌ Falsear tokens_measured (siempre medir, nunca estimar a ojo)
❌ Invocar la CARD desde otro Workflow (las CARDs NO se invocan, se inyectan por PB)
❌ Crear una CARD para un Workflow que aún no existe (1:1 estricto)

CUERPO RECOMENDADO:

- 3 secciones mínimas: "Qué hacer", "Si falla", "Output"
- Comandos bash inline solo del happy path
- Tablas compactas para errores comunes
- Referencias a otras CARDs si hay encadenamiento

POST-PUBLICACIÓN:

1. Borrar este bloque <!-- ... -->
2. Borrar el bloque "Cómo usar este template" del header
3. Verificar que el archivo está en 05.Cards/<categoria>/
4. Confirmar entrada en cards_catalog.json
5. Confirmar README de la categoría actualizado
6. Si categoría nueva → ACRONIMOS actualizado

=== FIN INSTRUCCIONES ===
-->
