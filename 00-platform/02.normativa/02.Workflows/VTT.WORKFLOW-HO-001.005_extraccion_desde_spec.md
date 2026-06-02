# VTT.WORKFLOW-HO-001.005 — Extracción desde SPEC (Pista A del Camino C)

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-HO-001.005` |
| **Pertenece a** | `VTT.PROTOCOL-HO-001` §5.2.0 (camino C pista A) |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-06-01 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | TL + agente generador |
| **Tipo** | [PROCESO] sub-procedimiento de FASE 2 — solo camino C |

---

## 1. Propósito

Generar documentos 3B sintéticos a partir de la SPEC consolidada, una sola vez al inicio del bloque. Estos documentos son inputs para el routing index y reemplazan la necesidad de que cada agente explore la SPEC entera por cada tarea. Aplica solo cuando el camino elegido es C (feature en sistema operando).

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `spec_path` | path | FASE 1 aprobada | sí | SPEC del bloque, versión aprobada |
| `metodologia_path` | path | FASE 1 aprobada | sí | METODOLOGIA del bloque |
| `decisiones_codigo` | string | parte de SPEC | sí | Prefijo de decisiones (ej. `D-MEM-`, `D-CR-`) |
| `output_dir` | path | configuración bloque | sí | Carpeta destino para los docs sintéticos |

---

## 3. Precondiciones

- SPEC + METODOLOGIA aprobadas por FASE 1 REVMA.
- Camino C confirmado en DECISION_BLOQUE.
- TL tiene visibilidad de la SPEC completa.

---

## 4. Reglas del Workflow

- **R1:** Los documentos generados son SINTÉTICOS — no reemplazan los 3B.X formales que se producen en §5.2.3. Son aceleradores de lectura.
- **R2:** Cada documento sintético cita explícitamente la sección de SPEC de origen.
- **R3:** NO se generan documentos sobre temas que la SPEC no cubre — si falta, se anota como gap a resolver en producción del 3B.X formal.
- **R4:** Los documentos sintéticos son inmutables — si la SPEC cambia (backfeed), se regeneran enteros, no se parchean.

---

## 5. Pasos

### Paso 1 — TL identifica qué documentos sintéticos producir

Según superficies de la feature:
- `3B.3_schema.md` — modelo de datos
- `3B.4_endpoints.md` — endpoints + contratos
- `3B.4_error_codes.md` — códigos de error
- `3B.4_auth.md` — RBAC/autorización
- `3B.2_structure.md` — estructura de archivos esperada
- `3B.5_flows.md` — lifecycle / flujos
- `3B.6_decisions.md` — decisiones cerradas D-XX-NN

### Paso 2 — Para cada documento sintético → producir

Por cada documento listado en Paso 1:

a) TL identifica las secciones de SPEC que contienen la información correspondiente.

b) TL (o agente asignado) extrae el contenido de la SPEC y lo reformula en formato sintético breve.

c) Se cita la sección de SPEC en cada bloque del documento sintético.

d) Se guarda en `output_dir/<nombre_doc>.md`.

### Paso 3 — TL valida coherencia entre documentos sintéticos

¿Los documentos sintéticos son coherentes entre sí? → **[DECISIÓN]**
- Ej. ¿el `3B.4_endpoints.md` consume tablas declaradas en `3B.3_schema.md`?
- Ej. ¿las decisiones de `3B.6_decisions.md` no contradicen al `3B.4_auth.md`?

Si hay inconsistencia → revisar SPEC, posiblemente activar backfeed a FASE 1.

### Paso 4 — TL registra documentos sintéticos en DECISION_BLOQUE

PM/TL anota en DECISION_BLOQUE qué documentos sintéticos se produjeron y qué secciones de SPEC alimentan a cada uno.

---

## 6. Outputs

| Output | Tipo | Destino |
|---|---|---|
| Documentos 3B sintéticos | archivos .md | `output_dir/` |
| Registro en DECISION_BLOQUE | sección actualizada | DECISION_BLOQUE |

---

## 7. Validación

- Los 7 documentos sintéticos típicos están en `output_dir/`.
- Cada uno cita SPEC con sección específica.
- No hay contradicciones cross-documento.
- Volumen total de los sintéticos es significativamente menor que la SPEC original (eso es el ahorro de tokens downstream).

---

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| Documento sintético contiene contenido que NO está en SPEC | Agente inventó | Eliminar contenido inventado, dejar solo lo que cita SPEC |
| Documento sintético es tan largo como la SPEC | No se sintetizó | Revisar criterio de compresión: solo lo esencial para que un agente ejecute su tarea |
| Documento sintético cita sección equivocada | Error de mapeo | Re-mapear con TL revisando cita por cita |
| Contradicción entre 2 documentos sintéticos | Inconsistencia en SPEC misma | Activar backfeed a FASE 1, revisar SPEC |

---

## 9. Skills invocadas

- `VTT.SKILL-ATTACH-001` (subir documentos al sistema)

---

**Documento:** `VTT.WORKFLOW-HO-001.005_extraccion_desde_spec.md`
**Versión:** 1.0.0
**Fecha:** 2026-06-01
