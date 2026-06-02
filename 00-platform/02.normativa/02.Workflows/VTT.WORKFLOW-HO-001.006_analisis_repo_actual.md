# VTT.WORKFLOW-HO-001.006 — Análisis del Repo Actual (Pista B del Camino C)

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-HO-001.006` |
| **Pertenece a** | `VTT.PROTOCOL-HO-001` §5.2.0 (camino C pista B) |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-06-01 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | TL + agente analista de repo |
| **Tipo** | [PROCESO] sub-procedimiento de FASE 2 — solo camino C |

---

## 1. Propósito

Generar documentos `3B.X_actual_*` que capturan el estado actual del repo en aquellos puntos donde la feature va a aterrizar. Es la contraparte del WORKFLOW-005 (extracción desde SPEC). Aplica solo en camino C.

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `repo_path` | path | configuración bloque | sí | Root del repositorio existente |
| `superficies` | array<string> | DECISION_BLOQUE | sí | Qué partes del repo analizar (services, routes, schema, etc.) |
| `output_dir` | path | configuración bloque | sí | Carpeta destino para los docs `actual_*` |

---

## 3. Precondiciones

- Repo existe y es accesible (clonado localmente o vía worktree).
- Camino C confirmado.
- TL tiene visibilidad de qué áreas del repo toca la feature.

---

## 4. Reglas del Workflow

- **R1:** Los documentos `actual_*` describen estado ACTUAL del código, no estado deseado.
- **R2:** Si el repo no tiene algo (ej. no hay tabla X), el documento `actual_*` lo declara explícitamente — NO inventa.
- **R3:** Los documentos `actual_*` no juzgan la calidad del código actual, solo lo describen.
- **R4:** Si la feature requiere modificar archivo existente, el documento `actual_*` debe contener referencia exacta al path y líneas relevantes.

---

## 5. Pasos

### Paso 1 — TL define documentos `actual_*` a producir

Típicamente:
- `3B.2_actual_structure.md` — estructura de carpetas y archivos relevantes
- `3B.3_actual_schema.md` — schema de BD actual (tablas existentes)
- `3B.4_actual_endpoints.md` — endpoints ya implementados
- `3B.2_actual_patterns.md` — patrones de código del repo (AppError, logger, middleware chain)

### Paso 2 — Por cada documento → analizar repo

Por cada documento `actual_*`:

a) Agente analista navega las superficies relevantes del repo.

b) Extrae estructura/schema/endpoints/patrones actuales.

c) Documenta con referencias exactas a paths y líneas.

d) Guarda en `output_dir/<nombre_doc>.md`.

### Paso 3 — TL valida cobertura

¿Los documentos `actual_*` cubren las áreas donde aterrizará la feature? → **[DECISIÓN]**
- Si la feature toca un servicio cuya estructura no quedó documentada → ampliar análisis.
- Si la feature requiere FK a tabla cuyo schema no quedó capturado → ampliar análisis.

### Paso 4 — TL identifica gaps SPEC vs repo

Comparando docs sintéticos de WORKFLOW-005 (qué pide la SPEC) vs docs `actual_*` (qué hay):
- Lista delta: qué hay que crear, qué modificar, qué reusar.

Esta lista delta es input para el Task Breakdown en FASE 4.

### Paso 5 — TL registra en DECISION_BLOQUE

PM/TL anota qué documentos `actual_*` se produjeron y qué delta SPEC-vs-repo se identificó.

---

## 6. Outputs

| Output | Tipo | Destino |
|---|---|---|
| Documentos `3B.X_actual_*` | archivos .md | `output_dir/` |
| Lista delta SPEC vs repo | sección en DECISION_BLOQUE | DECISION_BLOQUE |

---

## 7. Validación

- Los 4 documentos `actual_*` típicos están en `output_dir/`.
- Cada uno cita paths reales del repo.
- Lista delta SPEC-vs-repo está identificada.
- No hay contenido inventado (todo es verificable contra el repo).

---

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| Documento `actual_*` describe algo que no existe en repo | Agente alucinó | Verificar paths citados, eliminar inventados |
| No se analizó superficie relevante para la feature | Mapeo incompleto | Ampliar análisis con superficies adicionales |
| Documento `actual_*` está obsoleto cuando se ejecuta FASE 4 | El repo cambió entre Paso 1 y Paso 4 | Re-ejecutar Paso 2 con HEAD actualizado |

---

## 9. Skills invocadas

- `VTT.SKILL-ATTACH-001`

---

**Documento:** `VTT.WORKFLOW-HO-001.006_analisis_repo_actual.md`
**Versión:** 1.0.0
**Fecha:** 2026-06-01
