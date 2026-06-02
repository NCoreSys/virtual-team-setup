# VTT.WORKFLOW-HO-001.029 — Inyectar Tareas de Calidad por Sprint

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-HO-001.029` |
| **Pertenece a** | `VTT.PROTOCOL-HO-001` §5.6.7 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-06-01 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | PJM |
| **Tipo** | [PROCESO] sub-procedimiento de inyección por sprint |

---

## 1. Propósito

PJM inyecta tareas de calidad (Code Review + Testing + Integration Audit + Cierre) en cada sprint para que las 3 guías cross-sprint se ejecuten realmente, no queden como documentación sin enforcement.

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `sprint_id` | string | iterador | sí | Sprint actual |
| `roles_activos` | array | WORKFLOW-025 | sí | Determina qué tareas se inyectan |
| `setup_doc` | path | WORKFLOW-026 | sí | SETUP_S[N] donde se agregan las tareas |
| `code_review_guide` | path | guías | sí | CODE_REVIEW_GUIDE_V1.1 |
| `testing_guide` | path | guías | sí | TESTING_GUIDE_V1.1 |
| `integration_audit_checklist` | path | guías | sí | INTEGRATION_AUDIT_CHECKLIST_V1.1 |

---

## 3. Precondiciones

- WORKFLOW-026 (SETUP_S[N]) producido.
- Roles activos identificados.

---

## 4. Reglas del Workflow

- **R1:** Catálogo canónico de tareas inyectadas es fijo según familia, pero algunas son condicionales según rol activo.
- **R2:** Las tareas inyectadas se AGREGAN al SETUP_S[N] (no van en handoffs).
- **R3:** Cada tarea inyectada tiene assignee, estimación, complejidad, categoría según guía origen.
- **R4:** Tareas de cierre dependen formalmente de las de calidad (chain de aprobaciones).

---

## 5. Pasos

### Paso 1 — PJM identifica familias aplicables al sprint

| Familia | Aplica si... |
|---|---|
| Code Review | Sprint produce código (siempre) |
| Testing | Sprint produce código (siempre) |
| Integration Audit | Sprint produce código que se integra al sistema |
| Cierre | Siempre |

### Paso 2 — PJM inyecta familia Code Review

| Tarea | Assignee | Estimado | Complejidad | Categoría | Condición |
|---|---|---|---|---|---|
| TL-S[N]-BE-REVIEW | TL | 3h | MEDIUM | review | si hay BE en sprint |
| TL-S[N]-FE-REVIEW | TL | 3h | MEDIUM | review | si hay FE en sprint |
| TL-S[N]-DB-REVIEW | TL | 2h | MEDIUM | review | si hay DB en sprint |
| CR-S[N]-XXX | CR externo | 4h | MEDIUM | review | si hay PR >500 LOC esperado |
| AR-S[N]-ADR-REVIEW | AR | 2h | MEDIUM | review | si hay PR con ADR |

### Paso 3 — PJM inyecta familia Testing

| Tarea | Assignee | Estimado | Complejidad | Categoría | Condición |
|---|---|---|---|---|---|
| QA-001 | QA | 4h | MEDIUM | testing | siempre si QA activo |
| QA-002 (BE tests) | QA | 6h | MEDIUM | testing | si BE en sprint |
| QA-003 (FE tests) | QA | 6h | MEDIUM | testing | si FE en sprint |
| QA-004 (QA-FLOW E2E) | QA | 6h | HIGH | testing | si E2E aplicable |
| QA-005 (Regression) | QA | 4h | MEDIUM | testing | post-bug fixes |

### Paso 4 — PJM inyecta familia Integration Audit

| Tarea | Assignee | Estimado | Complejidad | Categoría | Condición |
|---|---|---|---|---|---|
| AR-S[N]-AUDIT | AR | 3h | MEDIUM | review | siempre (1 por sprint) |

### Paso 5 — PJM inyecta familia Cierre

| Tarea | Assignee | Estimado | Complejidad | Categoría |
|---|---|---|---|---|
| TL-S[N]-REV | TL | 2h | MEDIUM | review |
| AR-S[N] | AR | 2h | MEDIUM | review |
| QA-S[N] | QA | 2h | LOW | review |
| DL-S[N]-REV | DL | 3h | MEDIUM | review (si UI) |
| CIERRE-S[N] | TL | 2h | LOW | review |
| APR-S[N] | PM | 1h | LOW | review |

### Paso 6 — PJM configura cadena de dependencias

Cadena obligatoria al final del sprint:
```
Deliverables del rol → TL-S[N]-<ROL>-REVIEW → AR-S[N]-AUDIT
                                              ↓
                          QA-S[N] (después de QA-005)
                                              ↓
                                       DL-S[N]-REV (si UI)
                                              ↓
                                       CIERRE-S[N] → APR-S[N]
```

### Paso 7 — PJM agrega las tareas inyectadas al SETUP_S[N]

Agrega bloques de creación de tarea + dependencias al script Python del SETUP.

→ actualiza `SETUP_S[N].md` + `.json`.

### Paso 8 — PJM documenta inyecciones en INDEX

Agrega sección "Tareas de calidad inyectadas por sprint" al INDEX_PAQUETE_OPERATIVO_<BLOQUE> (cuando se produzca en WORKFLOW-030).

---

## 6. Outputs

| Output | Tipo | Destino |
|---|---|---|
| SETUP_S[N] actualizado con tareas de calidad | secciones agregadas | mismo SETUP_S[N].md |
| Cadena de dependencias actualizada | bloque agregado | mismo SETUP_S[N].md |

---

## 7. Validación

- Tareas Code Review presentes según roles activos.
- Tareas Testing presentes según roles activos.
- AR-S[N]-AUDIT siempre presente.
- Cadena de cierre completa: TL → AR → QA → (DL) → CIERRE → APR.
- APR-S[N] es tarea formal con dependencia a CIERRE-S[N].

---

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| Sprint sin AR-S[N]-AUDIT | Olvido | Inyectar siempre |
| QA-001 ausente con QA activo | Olvido | Inyectar Test Plan |
| Cadena de cierre rota | Mal mapeo | Reconfigurar dependencias |
| Tarea inyectada sin assignee | Falta UUID | Completar desde OPERATIVO |

---

## 9. Skills invocadas

(Ninguna directa — actualiza SETUP_S[N] producido por WORKFLOW-026)

---

**Documento:** `VTT.WORKFLOW-HO-001.029_inyectar_tareas_calidad.md`
**Versión:** 1.0.0
**Fecha:** 2026-06-01
