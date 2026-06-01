# 05.Cards — Nivel R Runtime del modelo VTT

> **Tarjetas runtime** comprimidas del happy path de un Workflow, para inyección al prompt del agente por el Prompt Builder (futuro) o por el TL (hoy, vía lazy-loading desde el ASSIGNMENT).

| Campo | Valor |
|---|---|
| **Nivel** | R (Runtime) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-31 |
| **Mantenedor** | PM Martin Rivas |
| **Referencia conceptual** | `02.normativa/README.md` §2.4.bis y §8.bis |
| **Referencia autoría** | `02.normativa/GUIA_AUTOR.md` §4.5 y §4.6 |
| **Template autoría** | `03.templates/normativa/_autoria/TEMPLATE_CARD.md` |

---

## 1. Qué es Nivel R

Una **CARD** es una **vista comprimida runtime** del happy path de **UN Workflow** (1:1). NO reemplaza Protocol/Workflow/Skill/Script — el agente puede consultar Workflow/Skill si necesita más detalle.

**Reducción medida:** ~83-91% vs cargar Protocol+Workflow+Skill+Script completos para el mismo proceso.

## 2. 4 tipos por presupuesto (chars/4 canónico)

| Tipo | Target | Hard cap |
|---|---|---|
| `CARD-mini` | 200-500 tok | 700 |
| `CARD-std` | 500-1200 tok | 1500 |
| `CARD-large` | 1200-2500 tok | 3000 |
| `CARD-pack` | 2500-4500 tok | 5000 |

**Si excede hard cap** → upgrade al siguiente tipo o partir en 2 CARDs. NO se negocia el tope.

## 3. Estructura del directorio

```
05.Cards/
├── README.md                    (este archivo)
├── cards_catalog.json           (catálogo Prompt Builder)
├── asg/                         CARDs categoría ASG (Asignación)
│   └── README.md
├── manifest/                    CARDs categoría MAN (Manifests)
│   └── README.md
├── exe/                         CARDs categoría EXE (Ejecución FASE 3)
│   └── README.md
└── iss/                         CARDs categoría ISS (Sub-ciclo Issue FASE 3.5)
    └── README.md
```

## 4. Inventario actual por categoría

| Categoría | CARDs | Descripción |
|---|---|---|
| `asg/` | CARD-ASG-001 | FASE 0 PROTOCOL-ASG-001: validar HANDOFF_TL_S[N].md |
| `manifest/` | CARD-MAN-001..004 | Manifests v1.0/v1.5 + execution_manifest (gen+lee) |
| `exe/` | CARD-EXE-001..009 | FASE 3 PROTOCOL-ASG-001: ciclo completo ejecución del agente + TL sprint dashboard |
| `iss/` | CARD-ISS-001..005 | FASE 3.5 PROTOCOL-ASG-001: sub-ciclo de Issue (crear, on_hold, analizar, decidir, retomar) |

**Total: 19 CARDs activas.**

## 5. Cómo se usa una CARD

### Hoy (lazy-loading vía TL)

El TL referencia las CARDs aplicables en el ASSIGNMENT:

```markdown
### CARDs runtime aplicables a esta tarea

- `05.Cards/exe/VTT.CARD-EXE-001_agente_lee_inputs_iniciales.md`
- `05.Cards/exe/VTT.CARD-EXE-002_agente_verifica_worktree.md`
- ...
```

El agente carga cada CARD desde filesystem cuando entra a cada fase de su ejecución.

### Mañana (Prompt Builder activo)

El Prompt Builder consulta `cards_catalog.json` y activa CARDs automáticamente según contexto:

```python
# Pseudocódigo
for card in catalog.cards:
    if card.applies_when.evaluate(task.phase, agent.role, task.category):
        if all(prior in active_cards for prior in card.requires_prior):
            inject(card)
```

## 6. Catálogo Prompt Builder

`cards_catalog.json` es la fuente machine-readable. Estructura:

```json
{
  "schema_version": "1.0",
  "estimator": "chars/4",
  "consumer": "Prompt Builder (futuro) + TL Reviewer al escribir ASSIGNMENT (hoy)",
  "applies_when_grammar": {
    "fields": {
      "task.phase": ["assignment","execution_start","execution","closing","review","approval"],
      "agent.role": ["BE","DB","FE","DO","QA","DL","UX","AR","SA","TL","PM","PJM"],
      "task.category": ["development","deployment","devops","documentation","testing","design","bugfix"]
    },
    "operators": ["=","IN [...]","AND","OR"]
  },
  "cards": [
    { "id": "CARD-XYZ-NNN", "title": "...", "type": "CARD-std",
      "tokens_measured": 1234, "applies_when": "...",
      "requires_prior": ["CARD-ABC-MMM"], "consumer": "agent",
      "path": "05.Cards/categoria/VTT.CARD-XYZ-NNN_...md",
      "references": {"workflow": "...", "skill": "...", "script": "..."}
    }
  ]
}
```

## 7. Cómo producir una CARD nueva

1. Verificar que existe el **Workflow padre** (1:1 estricto)
2. Copiar `03.templates/normativa/_autoria/TEMPLATE_CARD.md` a `05.Cards/<categoria>/`
3. Renombrar a `VTT.CARD-<CAT>-<NNN>_<titulo_snake_case>.md`
4. Completar header obligatorio (Tipo + Aplica cuando + Requiere Cards previas + Pertenece a + Tokens)
5. Comprimir SOLO el happy path del Workflow
6. Medir tokens con `chars/4` → ajustar Tipo si excede target
7. Agregar entrada a `cards_catalog.json`
8. Actualizar `<categoria>/README.md`
9. Si categoría nueva → registrar en `00_REGISTRO_ACRONIMOS.md` §3.1

Ver checklist completo en `GUIA_AUTOR.md` §4.5.

## 8. Reglas operativas

| # | Regla |
|---|---|
| R1 | **1:1 con Workflow padre.** Una CARD por workflow, no consolidar packs cruzados (Opción A confirmada PM 2026-05-30). |
| R2 | **Tokens medidos**, no estimados. Estimador `chars/4` canónico. |
| R3 | **Hard cap del tipo no se negocia.** Excedés → upgrade o partir. |
| R4 | **NO invocación inversa.** Workflow/Skill no invocan CARDs. Activación al revés: Prompt Builder → CARD. |
| R5 | **Solo happy path.** Ramificaciones complejas viven en el Workflow padre. |
| R6 | **Sincronizar catálogo.** Toda CARD creada/actualizada → entrada en `cards_catalog.json` con `tokens_measured` real. |

## 9. Changelog

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-05-31 | Estructura inicial del Nivel R. Categorías `asg/`, `manifest/`, `exe/`, `iss/` creadas. 19 CARDs iniciales registradas en `cards_catalog.json`. README maestro + READMEs por categoría. |
