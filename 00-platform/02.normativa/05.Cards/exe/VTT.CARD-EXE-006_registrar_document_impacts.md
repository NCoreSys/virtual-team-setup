# VTT.CARD-EXE-006 — Registrar Document Impacts

| Campo | Valor |
|---|---|
| **Código** | `VTT.CARD-EXE-006` |
| **Tipo** | `CARD-mini` |
| **Versión** | 1.0 |
| **Aplica cuando** | `task.phase = execution AND agent.role IN [BE,DB,FE,DO,QA,DL,UX,AR,SA]` |
| **Requiere Cards previas** | `CARD-EXE-005` |
| **Pertenece a** | WORKFLOW-ASG-001.018 |
| **Tokens estimados** | ~640 |

---

## Qué hacer

Por cada documento canónico afectado (LDs modificados + `.LOGIC.md` nuevos + ADRs creados):

```bash
curl -X POST "$VTT_BASE_URL/api/tasks/<TASK_ID>/document-impacts" \
  -H "Authorization: Bearer $VTT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "documentSourceId": "<UUID del doc en VTT>",
    "impactType": "modified",
    "description": "Actualizada §X.Y — <qué cambió + por qué>"
  }'
```

## `impactType` (enum cerrado)

| Valor | Cuándo |
|---|---|
| `added` | Nuevo archivo creado |
| `modified` | Archivo existente cambió |
| `removed` | Archivo eliminado |
| `referenced` | Código nuevo menciona el doc sin modificarlo (ej. comentario `// see ADR-15`) |

## Fallback DEBT-INFRA-VTT-01

Si el endpoint devuelve 403/404 porque NO tenés acceso a `documentSourceId`:

```bash
curl -X POST "$VTT_BASE_URL/api/tasks/<TASK_ID>/devlog-entries" \
  -H "Authorization: Bearer $VTT_TOKEN" \
  -d '{"entries":[{
    "categoryCode":"observation",
    "severity":"low",
    "title":"Document Impacts (fallback DEBT-INFRA-VTT-01)",
    "description":"POST /document-impacts no accesible. Declaración manual:\n1. SPEC v1.9 (§4.2) — modified — <descripción>\n2. <archivo>.LOGIC.md — added — <descripción>\nReferencia: DEBT-INFRA-VTT-01",
    "reportedBy":"<AGENT_UUID>"
  }]}'
```

## Reglas

- **R1:** UN Document Impact por cada doc. NO agrupar (no se acepta "actualicé varios docs").
- **R4:** `description` concreta — qué cambió + por qué + sección §X.Y. NO descripciones vagas tipo "actualizado".
- **R5:** `referenced` cuando código NUEVO menciona el doc sin modificarlo.

## Si falla

| Síntoma | Acción |
|---|---|
| HTTP 403 (sin acceso a documentSourceId) | Fallback devlog observation (DEBT-INFRA-VTT-01) |
| HTTP 400 invalid impactType | Solo `added`/`modified`/`removed`/`referenced` |
| Olvidaste algún doc | Volver a CARD-EXE-005 + consolidar lista |

## Output

Lista de impacts registrados (endpoint o fallback). Próximo: **CARD-EXE-007** (Hardcode Check).
