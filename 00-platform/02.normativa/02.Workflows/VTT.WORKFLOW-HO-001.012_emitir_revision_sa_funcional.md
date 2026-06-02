# VTT.WORKFLOW-HO-001.012 — Emitir REVISION_SA_FUNCIONAL

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-HO-001.012` |
| **Pertenece a** | `VTT.PROTOCOL-HO-001` §5.3.3 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-06-01 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | SA |
| **Tipo** | [PROCESO] sub-procedimiento de FASE 3 — opcional según cadena |

---

## 1. Propósito

SA emite revisión funcional del paquete técnico contra la SPEC base. Verifica que ningún 3B.X haya derivado en algo que SPEC no aprueba y que el paquete cubre todos los RF/NFR declarados.

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `paquete_3b` | array<path> | FASE 2 | sí | Los 8 documentos 3B.X |
| `spec_path` | path | FASE 1 | sí | SPEC aprobada |
| `metodologia_path` | path | FASE 1 | sí | METODOLOGIA aprobada |
| `template_revision_sa` | path | templates | sí | Template canónico |

---

## 3. Precondiciones

- SA está en cadena de roles (paso opcional, PM decide en FASE 0).
- Los 8 documentos 3B.X aprobados.

---

## 4. Reglas del Workflow

- **R1:** SA valida FUNCIONALMENTE, no técnicamente. No revisa código ni patrones.
- **R2:** Cada RF de SPEC debe estar cubierto por al menos un 3B.X.
- **R3:** Cada NFR de SPEC debe estar cubierto en 3B.7 o 3B.8.
- **R4:** Si SPEC quedó vaga en algo, SA verifica que el paquete técnico NO lo resolvió arbitrariamente.
- **R5:** Severidad bloqueante / mayor / menor.

---

## 5. Pasos

### Paso 1 — SA construye matriz RF ↔ 3B.X

Por cada RF declarado en SPEC:
- ¿Qué 3B.X lo cubre?
- ¿Está cubierto por API (3B.4)? ¿Por schema (3B.3)? ¿Por flujo (3B.5)?

Si un RF no aparece en ningún 3B.X → gap funcional.

### Paso 2 — SA construye matriz NFR ↔ 3B.X

Por cada NFR de SPEC:
- ¿Está cubierto en 3B.7 (security NFRs) o 3B.8 (performance/availability/scalability)?

### Paso 3 — SA valida que no hay derivas de scope

Pregunta: ¿algún 3B.X incluye funcionalidad que SPEC NO declara?

Ejemplos:
- 3B.4 declara endpoint que SPEC no menciona.
- 3B.3 incluye tabla para feature futura no aprobada.

Si hay derivas → escalar al PM.

### Paso 4 — SA valida resolución de ambigüedades

Pregunta: ¿hay puntos donde SPEC quedó vaga? ¿el paquete técnico los resolvió arbitrariamente?

Ejemplos:
- SPEC dice "el sistema permite búsqueda" sin definir parámetros. 3B.4 declara `GET /search?q=&type=&limit=` — eso es invención de scope.
- Si hay, escalar al PM para ratificación (decisión documentada en SPEC actualizada o aceptada como decisión técnica con `D-XX-NN`).

### Paso 5 — SA redacta REVISION_SA_FUNCIONAL

Estructura del documento:
- Matriz RF ↔ 3B.X (Paso 1)
- Matriz NFR ↔ 3B.X (Paso 2)
- Lista de derivas detectadas (Paso 3)
- Lista de ambigüedades resueltas arbitrariamente (Paso 4)
- Decisión final (APROBADO / APROBADO CON OBSERVACIONES / NO APROBADO)

### Paso 6 — SA firma el documento

Documento: `REVISION_SA_FUNCIONAL_<BLOQUE>_v1.0.md`

---

## 6. Outputs

| Output | Tipo | Destino |
|---|---|---|
| `REVISION_SA_FUNCIONAL_<BLOQUE>_v1.0.md` | archivo .md | `_project-management/Fases/<BLOQUE>/` |

---

## 7. Validación

- Matriz RF completa (cada RF mapeado).
- Matriz NFR completa.
- Derivas listadas (incluso si lista vacía).
- Ambigüedades listadas (incluso si lista vacía).
- Decisión final firmada.

---

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| RF no mapeado a ningún 3B.X | Gap funcional real | Backfeed a FASE 2 para que productor del 3B.X cubra |
| Deriva detectada → PM la acepta sin actualizar SPEC | Riesgo de drift entre SPEC y entregable | PM debe actualizar SPEC o aceptar como ADR |
| SA revisa código del 3B.X | Violación R1 | Re-encuadrar revisión a funcional |

---

## 9. Skills invocadas

- `VTT.SKILL-ATTACH-001`

---

**Documento:** `VTT.WORKFLOW-HO-001.012_emitir_revision_sa_funcional.md`
**Versión:** 1.0.0
**Fecha:** 2026-06-01
