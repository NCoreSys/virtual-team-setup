# Cards categoría ISS — Sub-ciclo de Issue (FASE 3.5 PROTOCOL-ASG-001)

Activado SOLO cuando el agente detecta un bloqueante durante FASE 3. No es parte del flujo normal.

| CARD | Tipo | Tokens | Trigger | Quién |
|---|---|---|---|---|
| `CARD-ISS-001_crear_issue_vtt` | CARD-mini | ~690 | Bloqueante detectado | Agente |
| `CARD-ISS-002_solicitar_on_hold` | CARD-mini | ~580 | Issue creado, tarea debe pausarse | Agente |
| `CARD-ISS-003_analizar_issue_tl` | CARD-std | ~1,050 | TL recibe notificación | TL |
| `CARD-ISS-004_decidir_correctiva_o_inline` | CARD-std | ~1,350 | Análisis completo | TL |
| `CARD-ISS-005_retomar_post_resume` | CARD-std | ~900 | Sistema VTT auto-resume disparó | Agente |

**Total ISS:** ~4,570 tok

## Flujo end-to-end

```
Agente: bloqueante detectado
  ↓ CARD-ISS-001 (crear Issue con marker + devlog blocker enlazado)
  ↓ CARD-ISS-002 (solicitar on_hold via PUT dedicado)

TL notificado:
  ↓ CARD-ISS-003 (analizar + clasificar S1-S4)
  ↓ CARD-ISS-004 (decidir:
                  A correctiva (recursión PROTOCOL)
                  B inline (instrucciones al agente)
                  C workaround + tech_debt TI
                  D reject)

Sistema VTT: auto-resume (en B, C, D)

Agente: tarea vuelve a in_progress
  ↓ CARD-ISS-005 (retomar — stash pop + aplicar instrucciones TL + ack)
  ↓ Continúa CARD-EXE-004 desde donde se bloqueó
```

## Referencias

- Protocol padre: `PROTOCOL-ASG-001 §5.4`
- Workflows ISS: `WORKFLOW-ASG-001.011, .035, .036, .037, .038`
- Catálogo PB: `../cards_catalog.json`
