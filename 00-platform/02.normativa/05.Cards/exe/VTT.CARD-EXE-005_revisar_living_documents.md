# VTT.CARD-EXE-005 — Revisar Living Documents impactados

| Campo | Valor |
|---|---|
| **Código** | `VTT.CARD-EXE-005` |
| **Tipo** | `CARD-std` |
| **Versión** | 1.0 |
| **Aplica cuando** | `task.phase = execution AND agent.role IN [BE,DB,FE,DO,QA,DL,UX,AR,SA]` |
| **Requiere Cards previas** | `CARD-EXE-004` |
| **Pertenece a** | WORKFLOW-ASG-001.017 |
| **Tokens estimados** | ~950 |

---

## Qué hacer

ANTES del commit final, revisar el **catálogo completo de LDs del proyecto** y declarar explícitamente cuáles modificaste y cuáles no.

```bash
# 1. Localizar el catálogo
LD_CATALOG="knowledge/LIVING_DOCUMENTS_<PROYECTO>.md"
# Variantes válidas: docs/LIVING_DOCUMENTS_<PROYECTO>.md, knowledge/living-documents/CATALOG.md

[ -f "$LD_CATALOG" ] || { echo "Catálogo no existe — escalar al PM"; exit 1; }
```

## Por cada LD del catálogo

Responder: **¿Esta tarea modifica algo que afecta este LD?**

### Tipos típicos de LD

- SPEC del sistema
- ERD / Schema DB
- API Contract / Swagger
- Diagrama de Arquitectura
- Catálogo de Endpoints / Componentes FE
- ADRs
- Catálogo de TIs

### Análisis típico por tipo de tarea

| Tipo tarea | LDs típicamente impactados |
|---|---|
| BE — nuevo endpoint | API Contract, Catálogo de Endpoints |
| BE — lógica de negocio | SPEC, ADRs si hay decisión |
| DB — migration | ERD, Schema, SPEC §Schema |
| FE — nueva pantalla | Catálogo Componentes FE, Site Map, Wireframes |
| DO — infra | Arquitectura, Infrastructure Plan |
| QA — suite nueva | Test Strategy, KPIs calidad |
| DL — componente Design | Design System |

## Si NO se modifica un LD — declarar explícito (NO implícito)

```bash
curl -X POST "$VTT_BASE_URL/api/tasks/<TASK_ID>/devlog-entries" \
  -H "Authorization: Bearer $VTT_TOKEN" \
  -d '{"entries":[{
    "categoryCode":"observation",
    "severity":"low",
    "title":"LD-XX (<nombre>): sin cambios",
    "description":"Tarea no afecta este LD porque <justificación específica>",
    "reportedBy":"<AGENT_UUID>"
  }]}'
```

## Si SÍ se modifica un LD

1. Actualizar el LD físicamente (editar archivo)
2. Registrar devlog `decision` con cambios + sección §X.Y modificada
3. Invocar **CARD-EXE-006** (registrar Document Impact en VTT)

## Inconsistencias menores → tech_debt

Si después de actualizar quedan inconsistencias con código legacy:
- Registrar devlog `tech_debt` severity=`medium`
- Crear TI tipo `tech_debt` vinculado al sprint próximo (paso 9 del .034)

## Checklist final

```
[ ] Total LDs revisados = Total del catálogo (sin excepción)
[ ] Cada LD tiene su devlog (sin cambios O actualizado)
[ ] LDs modificados están físicamente actualizados en el repo
[ ] Document Impacts registrados via CARD-EXE-006 para cada LD modificado
[ ] Inconsistencias menores registradas como tech_debt + TI
```

## Si falla

| Síntoma | Acción |
|---|---|
| Catálogo de LDs no existe | Escalar al PM — proyecto sin formalización LDs |
| LD físico no existe (path desactualizado) | Actualizar catálogo + escalar al PM |
| Total revisado < total catálogo | Volver a iterar — completar revisión |

## Bloqueo

**Sin revisión → bloquea Review Gate.**

## Output

Lista de LDs modificados + lista de LDs sin cambios (todos declarados como devlog entries). Próximo: **CARD-EXE-006** (registrar Document Impacts).
