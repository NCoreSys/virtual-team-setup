# VTT.WORKFLOW-HO-001.015 — Ciclo Iterativo Task Breakdown v1.0 → v1.4

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-HO-001.015` |
| **Pertenece a** | `VTT.PROTOCOL-HO-001` §5.4.8 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-06-01 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | TL + PM (cruce) |
| **Tipo** | [PROCESO] sub-procedimiento iterativo de FASE 4 |

---

## 1. Propósito

Ejecutar el ciclo canónico de 5 versiones del Task Breakdown (v1.0 → v1.4) combinando algoritmo, cruce PM/TL y resolución de conflictos pendientes. La v1.4 es la versión emitible al HO Maestro.

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `task_breakdown_v1_0` | path (.md + .json) | WORKFLOW-014 | sí | Versión inicial |
| `paquete_3b` | array<path> | FASE 2+3 | sí | Para validación cruzada |
| `velocity_historica` | path | proyecto | no | Si existe |

---

## 3. Precondiciones

- v1.0 producida por WORKFLOW-014.
- REVMA inicial aprobado.

---

## 4. Reglas del Workflow

- **R1:** Cada vuelta produce una versión incrementada (.md + .json sincronizados).
- **R2:** Versiones intermedias se preservan en `Versiones deprecadas/`.
- **R3:** Métrica de salud del cruce: <20% conflictos pendientes al cierre de v1.4.
- **R4:** Si >20% → cruce falló, rehacer auditoría algorítmica (v1.3).
- **R5:** Conflictos pendientes NO se resuelven votando ni "por las dudas" — pregunta semántica concreta sobre contenido del entregable.

---

## 5. Pasos

### Paso 1 — v1.0 → v1.1: Reconciliación PM/TL de horas, gates y baseline

PM y TL revisan en conjunto:
- Total de horas suma correctamente.
- Gates `GATE-S0X` coinciden con plan de rollout (3B.8).
- Baseline funcional separado de DB interno / DevOps / etc.

Output: `3B.9.3_v1.1.md` + `.json`.

### Paso 2 — v1.1 → v1.2: Modelo de 4 dimensiones aplicado a todo el grafo

TL re-revisa el grafo completo bajo el modelo de 4 dimensiones:
- ¿Toda dep que estaba como dependencia se clasificó correctamente en `dep_technical` vs `dep_role`?
- ¿Hay frases tipo "S0X cerrado" que escaparon? → mover a `gate_release`.

Output: `3B.9.3_v1.2.md` + `.json`.

### Paso 3 — v1.2 → v1.3: TL Claude reaplica algoritmo §11 caso por caso

Auditoría fina algorítmica:
- Por cada `dep_technical` declarada en v1.2, el TL Claude aplica las 7 preguntas otra vez.
- Detecta patrones de gap: continuidad-rol disfrazada, omisión simétrica, dep transitiva sin declaración.
- Documenta sugerencias de cambio con justificación.

Output: `3B.9.3_v1.3.md` + `.json` + lista de cambios sugeridos.

### Paso 4 — v1.3 → v1.4: Cruce PM/TL del proyecto

PM media entre TL Claude (auditor algorítmico) y TL del proyecto (auditor de contexto):

Por cada cambio sugerido en v1.3:
- **Acuerdo** → aplicar en v1.4.
- **Discrepancia con evidencia clara** → aplicar con mejor justificación técnica.
- **Conflicto semántico** → NO aplicar todavía, documentar pregunta concreta para TL del proyecto.

Output: `3B.9.3_v1.4.md` + `.json` + lista de conflictos pendientes.

### Paso 5 — PM valida métrica de salud del cruce

Calcula: `conflictos_pendientes / total_items_revisados`.

- Si <20% → cruce válido, v1.4 aprobada.
- Si >20% → cruce falló, regresar a Paso 3 con más cuidado.

### Paso 6 — Resolución de conflictos pendientes (v1.5+ opcional)

Si quedan conflictos pendientes:
- TL del proyecto inspecciona archivo/seed/migración del entregable cuestionado.
- Si SÍ → aplicar dep en v1.5.
- Si NO → cerrar item sin dep.
- v1.5+ es puntual (no re-audita el resto).

### Paso 7 — Marcar v1.4 como versión "emitible"

`3B.9.3_v1.4.md` queda como input formal para WORKFLOW-016 (derivados) y WORKFLOW-017 (Routing Index).

Versiones v1.0, v1.1, v1.2, v1.3 se mueven a `Versiones deprecadas/`.

---

## 6. Outputs

| Output | Tipo | Destino |
|---|---|---|
| `3B.9.3_TASK_BREAKDOWN_v1.4.md` (final emitible) | archivo .md | `_project-management/Fases/<BLOQUE>/` |
| `3B.9.3_TASK_BREAKDOWN_v1.4.json` | archivo .json sincronizado | mismo lugar |
| `CONFLICTOS_PENDIENTES_TASK_BREAKDOWN_<BLOQUE>.md` | archivo .md | `_project-management/Fases/<BLOQUE>/` |
| Versiones v1.0..v1.3 | archivos | `Versiones deprecadas/` |

---

## 7. Validación

- v1.4 está firmada por PM + TL.
- Métrica de salud <20% conflictos pendientes.
- Versiones intermedias archivadas.
- .md y .json v1.4 sincronizados.
- Conflictos pendientes documentados con pregunta semántica concreta.

---

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| Métrica >20% conflictos | Algoritmo aplicado superficialmente en v1.3 | Rehacer v1.3 con más cuidado |
| Conflicto "se resuelve" votando | Violación R5 | NO. Identificar pregunta semántica, TL inspecciona archivo |
| Conflicto se agrega "por las dudas" | Conservadurismo mal aplicado | Bloquea agentes artificialmente. Eliminar |
| v1.4 emitida con conflictos abiertos sin documentar | Riesgo downstream | Documentar en CONFLICTOS_PENDIENTES |

---

## 9. Skills invocadas

- `VTT.WORKFLOW-HO-001.020` (emitir JSON sincronizado en cada vuelta)
- `VTT.SKILL-ATTACH-001`

---

**Documento:** `VTT.WORKFLOW-HO-001.015_ciclo_iterativo_task_breakdown.md`
**Versión:** 1.0.0
**Fecha:** 2026-06-01
