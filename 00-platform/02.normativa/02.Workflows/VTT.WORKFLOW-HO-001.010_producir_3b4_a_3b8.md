# VTT.WORKFLOW-HO-001.010 — Producir 3B.4 a 3B.8 (genérico parametrizado)

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-HO-001.010` |
| **Pertenece a** | `VTT.PROTOCOL-HO-001` §5.2.3 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-06-01 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | BE (3B.4), TL/AR/BE (3B.5), TL/AR (3B.6), SEC/AR (3B.7), DO (3B.8) |
| **Tipo** | [PROCESO] sub-procedimiento parametrizado |

---

## 1. Propósito

Workflow genérico parametrizado que produce los documentos 3B.4 (API Design), 3B.5 (Sequence Diagrams), 3B.6 (ADRs), 3B.7 (Security Plan), 3B.8 (Infrastructure Plan). Cada invocación instancia el workflow con parámetros específicos del documento objetivo.

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `documento_objetivo` | enum | invocador | sí | `3B.4` / `3B.5` / `3B.6` / `3B.7` / `3B.8` |
| `productor_primario` | rol | tabla §5.2.1 Protocol | sí | Rol responsable según ownership canónico |
| `dependencias_upstream` | array<path> | docs 3B.X previos | sí | Documentos que deben estar aprobados antes |
| `spec_path` | path | FASE 1 | sí | SPEC |
| `docs_referencia` | array<path> | variable | no | Docs sintéticos/actuales si camino C |

---

## 3. Precondiciones

- Dependencias upstream aprobadas (según orden topológico §5.2.2 del Protocol).
- Productor primario está en cadena de roles.
- SPEC + 3B.1 disponibles.

---

## 4. Reglas del Workflow

### Reglas comunes a todos los 3B.X

- **R1:** Documento NO contradice SPEC ni 3B.X previos aprobados.
- **R2:** Si detecta gap en SPEC → backfeed a FASE 1.
- **R3:** Versionado obligatorio (v1.0 inicial, incremental por vueltas REVMA).

### Reglas específicas por documento

| Documento | Reglas adicionales |
|---|---|
| **3B.4 API Design** | OpenAPI/Swagger obligatorio. Cada endpoint declara: método, path, auth, request/response schemas, error codes, SLA. |
| **3B.5 Sequence Diagrams** | Mermaid `sequenceDiagram` para auth flow + business flows críticos + error flows + integration flows. |
| **3B.6 ADRs** | Una decisión por archivo o sección. Formato MADR: Context / Decision / Consequences. Índice de ADRs obligatorio. |
| **3B.7 Security Plan** | Cubre OWASP Top 10. Define auth/authz, validación, secrets management, input sanitization. |
| **3B.8 Infrastructure Plan** | Server specs, network, env matrix, scaling, backup, DR, SLA, monitoring. Plan de rollout con gates GATE-S0X. |

---

## 5. Pasos

### Paso 1 — Productor lee dependencias upstream

Productor primario lee:
- SPEC
- 3B.1 (siempre)
- Otros 3B.X que su documento depende (ver §5.2.2 del Protocol)

### Paso 2 — Productor genera contenido específico del documento

Aplica las reglas específicas del documento (R por tipo):

**3B.4:** Lista endpoints + DTOs + middlewares + error codes.

**3B.5:** Diagramas de flujos críticos (mínimo: auth, business principal, error principal, integración).

**3B.6:** Catálogo de ADRs cerradas. Cada ADR con `Context`, `Decision`, `Consequences`. Índice + cross-references.

**3B.7:** Plan de seguridad cubriendo OWASP Top 10. Controles SEC-C-XX numerados.

**3B.8:** Plan de infraestructura con server specs + env matrix + plan de rollout con GATE-S0X.

### Paso 3 — Productor ejecuta REVMA sobre su documento

→ invoca **`VTT.WORKFLOW-HO-001.001_ciclo_revma`** con (`documento=<3B.X>`, `agente_generador=<productor>`, `contexto=[SPEC, dependencias_upstream]`)

### Paso 4 — Backfeed condicional

Si durante REVMA el PM Revisor o el productor detecta gap en SPEC o en 3B.X anterior → activar backfeed (suspender este workflow, regresar a FASE 1 o WORKFLOW del 3B.X anterior).

### Paso 5 — Cierre

Documento firmado, versionado y disponible para próximos 3B.X dependientes.

---

## 6. Outputs

| Output | Tipo | Destino |
|---|---|---|
| `<3B.X>_<NOMBRE>.md` | archivo .md | `_project-management/Fases/<BLOQUE>/` |

---

## 7. Validación

Por tipo de documento:

| Documento | Validación |
|---|---|
| 3B.4 | OpenAPI exportable. Todos endpoints con request/response. |
| 3B.5 | Diagramas renderizan correctamente. Flujos críticos cubiertos. |
| 3B.6 | Índice de ADRs completo. Cada ADR con formato MADR. |
| 3B.7 | OWASP Top 10 cubierto. Controles SEC-C-XX numerados secuencialmente. |
| 3B.8 | Env matrix completo. Plan de rollout con gates ejecutables. |

---

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| 3B.4 con endpoint que viola auth declarada en 3B.7 | Incoherencia cross-doc | Detectar en REVMA, corregir |
| 3B.5 con flujo que usa servicio no documentado en 3B.1 | Inconsistencia | Backfeed a 3B.1 o corregir 3B.5 |
| 3B.6 con ADR que contradice decisión cerrada en SPEC | Decisión cambiada sin SPEC actualizada | Backfeed a FASE 1 |
| 3B.7 sin OWASP completo | Cobertura parcial | Completar antes de REVMA |
| 3B.8 sin plan de rollback | Riesgo de despliegue | Documentar rollback antes de REVMA |

---

## 9. Skills invocadas

- `VTT.WORKFLOW-HO-001.001` (REVMA)
- `VTT.SKILL-ATTACH-001`

---

**Documento:** `VTT.WORKFLOW-HO-001.010_producir_3b4_a_3b8.md`
**Versión:** 1.0.0
**Fecha:** 2026-06-01
