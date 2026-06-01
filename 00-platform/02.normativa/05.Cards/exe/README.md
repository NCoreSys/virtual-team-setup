# Cards categoría EXE — Ejecución del agente (FASE 3 PROTOCOL-ASG-001)

| CARD | Tipo | Tokens | Trigger | Quién |
|---|---|---|---|---|
| `CARD-EXE-001_agente_lee_inputs_iniciales` | CARD-mini | ~520 | Notificación de asignación recibida | Agente |
| `CARD-EXE-002_agente_verifica_worktree` | CARD-mini | ~580 | Inputs leídos, va a entrar al worktree | Agente |
| `CARD-EXE-003_agente_mueve_in_progress` | CARD-mini | ~430 | Worktree + manifest OK | Agente |
| `CARD-EXE-004_agente_ejecuta_workflow_assignment` | CARD-large | ~2,100 | task_in_progress, listo para implementar | Agente |
| `CARD-EXE-005_revisar_living_documents` | CARD-std | ~950 | Pre-commit final | Agente |
| `CARD-EXE-006_registrar_document_impacts` | CARD-mini | ~640 | LDs modificados detectados | Agente |
| `CARD-EXE-007_ejecutar_hardcode_check` | CARD-std | ~1,000 | Pre-commit final | Agente |
| `CARD-EXE-008_entrega_agente` | CARD-std | ~1,250 | Sub-workflows OK, listo para cierre | Agente |
| `CARD-EXE-009_mantener_sprint_status_tl` | CARD-std | ~950 | Cualquier trigger_event del sprint | TL |

**Total EXE:** ~8,420 tok (suma de los 9 CARDs)
**Reducción ~85% vs Protocol+Workflows+Skills+Scripts completos**

## Flujo end-to-end

```
Agente recibe asignación
  ↓ CARD-EXE-001 (lee inputs)
  ↓ CARD-EXE-002 (verifica worktree)
  ↓ CARD-MAN-004 (lee execution_manifest)
  ↓ CARD-EXE-003 (mueve in_progress)
  ↓ CARD-EXE-004 (ejecuta 13 pasos del ASSIGNMENT)
       │
       └─→ Si bloqueante → CARD-ISS-001..005 (FASE 3.5)
       │
  ↓ CARD-EXE-005 (revisar Living Docs) — pre-commit
  ↓ CARD-EXE-006 (Document Impacts) — pre-commit
  ↓ CARD-EXE-007 (Hardcode Check) — pre-commit
  ↓ Commit + push
  ↓ CARD-EXE-008 (entrega + manifest v1.0 AL FINAL)
  ↓ PR creado, tarea en task_in_review

TL (paralelo, durante toda FASE 3):
  CARD-EXE-009 (mantener SPRINT_STATUS_SX.md vivo)
```

## Referencias

- Protocol padre: `PROTOCOL-ASG-001 §5.3`
- Workflows EXE: `WORKFLOW-ASG-001.010, .017, .018, .019, .022, .028, .029, .030, .031, .032, .033, .034`
- Catálogo PB: `../cards_catalog.json`
