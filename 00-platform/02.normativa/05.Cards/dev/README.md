# Cards categoría DEV — Devlog Lifecycle (PROTOCOL-DEV-001)

| CARD | Tipo | Tokens | Trigger | Quién |
|---|---|---|---|---|
| `CARD-DEV-001_crear_devlog_entry` | CARD-std | ~769 | Agente detecta evento a registrar (decisión, observación, blocker, tech_debt, testing_note, risk, issue) | Agente ejecutor |
| `CARD-DEV-002_editar_o_transicionar_entry` | CARD-std | ~1036 | Agente corrige typo / TL procesa entry en code review | Agente / TL |
| `CARD-DEV-003_cerrar_entries_terminal_pre_aprobacion` | CARD-std | ~1029 | PM/TL cierran sprint, validan 0 entries pending | TL + PM |

**Total DEV:** ~2,834 tok (suma de las 3 CARDs)

## Flujo end-to-end

```
Agente durante ejecución
  ↓ CARD-DEV-001 (crear entry — pending)
       │
       └─ si surgió bug/blocker/question formal → CARD-ISS-001 (escalación a ASG-001 §5.4/§5.4.bis)
  ↓ CARD-DEV-002 Vía A (editar contenido si typo) — opcional
       │
TL en code review (FASE 3)
  ↓ CARD-DEV-002 Vía B (transicionar a acknowledged → resolved/wont_fix/deferred)
       │
PM + TL al cierre de sprint (FASE 4)
  ↓ CARD-DEV-003 (auditar 0 pending + decisión PM + transiciones masivas + resumen reporte M)
```

## Referencias

- **Protocol padre:** `VTT.PROTOCOL-DEV-001` (Ciclo de vida del Devlog Entry)
- **Workflows hijos:** `VTT.WORKFLOW-DEV-001.001/.002/.003`
- **Skills invocadas:** `VTT.SKILL-DEV-001..005`
- **Feature origen:** `Docs/01-documentacion/features mod dinamico/FEATURE_DEVLOG_LIFECYCLE.md`
- **Cross-link bug/question:** `VTT.PROTOCOL-ASG-001` §5.4 (bug/blocker) / §5.4.bis (question)

## Notas de medición

Tokens medidos con `chars/4` (estimador canónico VTT — GUIA_AUTOR §4.6):

```bash
python -c "print(open('VTT.CARD-DEV-001_crear_devlog_entry.md').read().__len__() // 4)"
```

DEV-001 originalmente declarada `CARD-mini` (~480 tok proyectado), upgradeada a `CARD-std` tras medición real (769 tok > hard cap mini 700). Las otras 2 se mantienen en `CARD-std` (1036 y 1029 — dentro de target 500-1200 y hard cap 1500).
