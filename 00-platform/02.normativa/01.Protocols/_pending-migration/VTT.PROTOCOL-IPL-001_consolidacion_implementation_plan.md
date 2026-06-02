# VTT.PROTOCOL-IPL-001 — Consolidación del Implementation Plan (3B.9 + Routing Index)

| Campo | Valor |
|---|---|
| **Código** | `VTT.PROTOCOL-IPL-001` |
| **Título** | Consolidación del Implementation Plan — 3B.9 (10 sub-docs) + Routing Index |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-05-31 |
| **Autor** | TW-OPS |
| **Dueño** | PM Governance / Process Owner VTT |
| **Aplica a** | TL (ejecutor principal), PM Revisor (audita), Coordinador (orquesta), PM (recibe para HO) |
| **Estado** | Aprobado |
| **Tipo** | Genérico VTT — protocolo del upstream |
| **Reglas aplicables (Nivel 0)** | Ver `00.Rules/rules_catalog.json` |
| **Invoca** | `VTT.PROTOCOL-REVMA-001` (sobre el 3B.9 consolidado) |
| **Es invocado por** | TL al recibir notificación de cierre del `VTT.PROTOCOL-PT-001` |

---

## Tabla de Contenido

1. [Propósito](#1-propósito)
2. [Campo de Aplicación](#2-campo-de-aplicación)
3. [Trigger de Inicio y Condiciones de Fin](#3-trigger-de-inicio-y-condiciones-de-fin)
4. [Responsabilidades](#4-responsabilidades)
5. [Definiciones](#5-definiciones)
6. [Artefactos de Entrada y de Salida](#6-artefactos-de-entrada-y-de-salida)
7. [Estructura Interna de 3B.9](#7-estructura-interna-de-3b9)
8. [Procedimiento](#8-procedimiento)
9. [Reglas Críticas de Consolidación](#9-reglas-críticas-de-consolidación)
10. [Reglas de Aplicabilidad](#10-reglas-de-aplicabilidad)
11. [Referencias Cruzadas](#11-referencias-cruzadas)
12. [Resumen de Revisiones](#12-resumen-de-revisiones)
13. [Anexos](#anexos)

---

## 1. Propósito

Establecer el proceso normativo por el cual el TL consolida los 8 documentos del paquete técnico (3B.1..3B.8) en el **Implementation Plan consolidado 3B.9**, compuesto por 10 sub-docs que incluyen el **Routing Index** — la pieza crítica que conecta cada Task ID con su documento fuente, archivos afectados, ADRs, controles SEC y criterio de cierre.

El 3B.9 + Routing Index es la **bisagra** entre el upstream (paquete técnico) y el downstream (HO Maestro, paquete operativo PJM, asignación de tareas). Sin él, el PM no puede emitir HO, el PJM no puede generar handoffs, y los agentes ejecutores no saben dónde leer cada cosa.

> **Regla de oro:** sin Routing Index completo, no hay 3B.9 entregable. Sin 3B.9 entregable, no hay HO Maestro. Sin HO Maestro, no se puede arrancar el downstream.

---

## 2. Campo de Aplicación

**Aplica a:**

- Cualquier proyecto VTT que haya completado `VTT.PROTOCOL-PT-001` con los 8 docs del paquete técnico aprobados.
- Cualquier feature dentro de sistema operando que adicionalmente haya completado `VTT.PROTOCOL-OB-001` (pista "estado actual" incluida).
- Cualquier bloque/release que requiera Implementation Plan formal antes de emitir HO.

**No aplica a:**

- Generación del paquete técnico (cubierto por `VTT.PROTOCOL-PT-001`).
- Emisión del HO Maestro (cubierta por `VTT.PROTOCOL-HOPJM-001`).
- Materialización en VTT (cubierta por `VTT.PROTOCOL-MAT-001`).

---

## 3. Trigger de Inicio y Condiciones de Fin

### 3.1 Trigger de inicio

El Protocol arranca cuando se cumple **una** de estas condiciones:

1. Coordinador notifica al TL que `VTT.PROTOCOL-PT-001` cerró exitosamente y los 8 docs del paquete técnico están aprobados.
2. Backfeed desde HO o paquete operativo PJM detecta inconsistencia en 3B.9 que requiere regenerar uno o más sub-docs.
3. Addendum técnico aprobado modifica scope cuantificado y requiere regenerar 3B.9.

### 3.2 Condición de fin (éxito)

El Protocol termina exitosamente cuando se cumplen **todas** estas condiciones:

1. Los 10 sub-docs del 3B.9 están producidos.
2. El Routing Index (3B.9.10) cubre **el 100% de los Task IDs** declarados en el Task Breakdown (3B.9.3).
3. El 3B.9 consolidado pasó `VTT.PROTOCOL-REVMA-001` con dictamen APROBADO.
4. Separación matemática verificada (baseline funcional / distribución técnica interna / OPER / buffers / diferidos no se suman entre sí).
5. Coordinador notifica al PM que 3B.9 está listo para emitir HO Maestro.

### 3.3 Condición de fin (suspensión)

El Protocol se suspende sin completar si:

1. El Routing Index no logra cubrir el 100% de Task IDs (faltan filas o referencias inválidas) → escalación al PM Governance.
2. La separación matemática no cuadra y el TL no puede justificar la diferencia → revisión de cifras del paquete técnico (potencial backfeed a 3B.2 y/o 3B.3).
3. Excede 3 vueltas de `REVMA-001` sin aprobación → escalación al PM Governance.

---

## 4. Responsabilidades

### 4.1 TL (Tech Lead) — Ejecutor principal

- Recibir notificación del coordinador con el paquete técnico aprobado.
- Producir los 10 sub-docs de 3B.9 en el orden correcto (§7).
- Garantizar que el Routing Index (3B.9.10) tiene **una fila por cada Task ID** declarado en 3B.9.3.
- Verificar separación matemática (§9.1) antes de declarar el 3B.9 entregable.
- Documentar la decisión `✅ / ⚪ / ❌` por deliverable de forma **trazable** (no "de memoria") — la trazabilidad va en 3B.9.3 mismo o en doc complementario referenciado.
- Atender ciclo `REVMA-001` sobre el 3B.9 consolidado.
- Entregar al coordinador para que notifique al PM.

### 4.2 PM Revisor — Audita el 3B.9 consolidado

- Recibir el 3B.9 consolidado del coordinador.
- Aplicar `REVMA-001` sobre el documento completo (todos los 10 sub-docs + Routing Index).
- Verificar específicamente:
  - Routing Index cubre 100% Task IDs del Task Breakdown.
  - Separación matemática de esfuerzos respetada.
  - Trazabilidad de decisiones `✅ / ⚪ / ❌` documentada.
  - Coherencia con paquete técnico 3B.1..3B.8.
- Emitir dictamen.

### 4.3 Coordinador (PM Governance / Process Owner)

- Confirmar al TL que el paquete técnico está completo antes de arrancar.
- Disparar `REVMA-001` sobre el 3B.9 cuando el TL lo entregue.
- Mantener bitácora del ciclo.
- Notificar al PM cuando 3B.9 está aprobado.

### 4.4 PM — Consumidor downstream

- NO produce el 3B.9.
- Recibe notificación de cierre del Protocol y arranca `VTT.PROTOCOL-HOPJM-001`.

---

## 5. Definiciones

**Implementation Plan (3B.9):** documento consolidado compuesto por 10 sub-docs internos (3B.9.1 a 3B.9.10) que cuantifica el alcance del bloque/release en términos ejecutables: tareas, dependencias, capacidad, riesgos, ruteo a fuentes técnicas.

**Sub-doc de 3B.9:** cualquiera de los 10 documentos internos. Pueden entregarse en **modo modular** (10 archivos separados) o en **modo consolidado** (un único `3B.9_IMPLEMENTATION_PLAN_*.md` con las 10 secciones como sub-§). Ambos modos son válidos.

**Task Breakdown (3B.9.3):** **PIVOTE del 3B.9**. Lista TODOS los deliverables del catálogo SDLC para las fases en alcance, con decisión `✅ / ⚪ / ❌`, horas, SP, owner primario, rol ejecutor, colaboradores, complejidad, dependencias. **Si está mal, se propaga a los 9 derivados.**

**Routing Index (3B.9.10):** **BISAGRA del upstream→downstream**. Mapa Task ID → documento → sección → ADR → control SEC → archivo/carpeta → dependencia → evidencia → criterio de cierre. **Debe cubrir 100% de Task IDs.**

**Decisión ✅ / ⚪ / ❌ trazable:** decisión documentada con justificación verificable contra fuente. NO "de memoria del TL". Ejemplos válidos: "❌ porque ADR-XYZ §3 cierra esta opción", "⚪ porque SPEC §X no exige para R1", "✅ por defecto al estar en alcance".

**Separación matemática de esfuerzos:** regla por la cual:
- Baseline funcional = suma de horas de deliverables ✅.
- Distribución técnica interna (ej. DB 71h) está **dentro** del baseline, NO se suma adicionalmente.
- Esfuerzo operativo (DevOps/SRE) está **fuera** del baseline.
- Buffers de riesgo están **fuera** del baseline.
- Tareas diferidas NO se suman al baseline.
- Porcentajes funcionales por rol suman 100% **solo sobre baseline funcional**.

**Modo modular / consolidado:** elección de empaquetado del 3B.9. Modular = 10 archivos. Consolidado = 1 archivo con 10 sub-§. El HO Maestro acepta ambos (ver HOPJM-001).

**Derivado directo:** sub-doc que se genera **únicamente a partir de 3B.9.3**. Son 4: 3B.9.2 (Story Points), 3B.9.4 (Effort Matrix / Dependency Map), 3B.9.5 (Complexity Analysis), 3B.9.8 (Migration & Rollout).

**Derivado compuesto:** sub-doc que requiere 3B.9.3 + uno o más derivados directos. Son 4: 3B.9.6 (Risk-Adjusted Estimates), 3B.9.7 (Capacity Plan), 3B.9.9 (Scheduling Inputs PM), 3B.9.10 (Routing Index).

**Síntesis final:** 3B.9.1 (Scope Baseline / Estimates Doc) — se escribe AL FINAL una vez que los otros 9 están listos.

---

## 6. Artefactos de Entrada y de Salida

### 6.1 Artefactos de entrada

| # | Artefacto | Producido por | Obligatorio |
|---|---|---|---|
| 1 | 3B.1 Solution Architecture aprobado | AR vía `PT-001` | ✅ |
| 2 | 3B.2 Code Architecture aprobado | TL vía `PT-001` | ✅ |
| 3 | 3B.3 Database Design aprobado | DB vía `PT-001` | ✅ |
| 4 | 3B.4 API Design aprobado | BE vía `PT-001` | ✅ |
| 5 | 3B.5 Sequence Diagrams aprobado | AR vía `PT-001` | ✅ |
| 6 | 3B.6 ADRs aprobado | TL vía `PT-001` | ✅ |
| 7 | 3B.7 Security Plan aprobado | SEC vía `PT-001` | ✅ |
| 8 | 3B.8 Infrastructure Plan aprobado | DevOps vía `PT-001` | ✅ |
| 9 | METODOLOGIA + SPEC aprobadas | PM análisis | ✅ |
| 10 | Catálogo SDLC genérico (ANALISIS_FASES_COMPLETO o equivalente) | Referencia | ✅ (input crítico de 3B.9.3) |
| 11 | OPERATIVO del proyecto (UUIDs reales) | PM | ✅ |
| 12 | Docs 3B "estado actual" (si feature en sistema operando) | Pista paralela `OB-001` | ⚠️ Condicional |

### 6.2 Artefactos de salida

| # | Artefacto | Path canónico sugerido | Obligatorio |
|---|---|---|---|
| 1 | 3B.9.3 Task Breakdown | `phases/03-design/deliverables/estimates/3B.9.3_task_breakdown.md` | ✅ **PIVOTE** |
| 2 | 3B.9.2 Story Points (derivado directo) | `.../3B.9.2_story_points.md` | ✅ |
| 3 | 3B.9.4 Dependency Map (derivado directo) | `.../3B.9.4_dependency_map.md` | ✅ |
| 4 | 3B.9.5 Complexity Analysis (derivado directo) | `.../3B.9.5_complexity_analysis.md` | ✅ |
| 5 | 3B.9.8 Migration & Rollout Plan (derivado directo) | `.../3B.9.8_migration_rollout.md` | ⚠️ Condicional — solo si proyecto tiene migraciones técnicas |
| 6 | 3B.9.6 Risk-Adjusted Estimates (derivado compuesto) | `.../3B.9.6_risk_adjusted_estimates.md` | ✅ |
| 7 | 3B.9.7 Capacity Plan (derivado compuesto) | `.../3B.9.7_capacity_plan.md` | ✅ |
| 8 | 3B.9.9 Scheduling Inputs for PM (derivado compuesto) | `.../3B.9.9_scheduling_inputs.md` | ✅ |
| 9 | 3B.9.10 Routing Index (derivado compuesto) | `.../3B.9.10_routing_index.md` | ✅ **BISAGRA** |
| 10 | 3B.9.1 Scope Baseline / Estimates Doc (síntesis final) | `.../3B.9.1_estimates_doc.md` | ✅ |
| 11 | (Opcional) 3B.9 consolidado en un solo archivo | `.../3B.9_IMPLEMENTATION_PLAN_<bloque>_v<X.Y>.md` | Configurable — modo consolidado |
| 12 | Bitácora `REVMA` del 3B.9 | `_project-management/revma-log/3B.9_<bloque>.md` | ✅ |

---

## 7. Estructura Interna de 3B.9

### 7.1 Los 10 sub-docs y su clasificación

| ID | Sub-doc | Tipo | Inputs propios | Función |
|---|---|---|---|---|
| 3B.9.3 | Task Breakdown | **PIVOTE** | Catálogo SDLC + SPEC + ADRs (3B.6) + 3B.1..3B.8 + (Fase 2 docs si aplica) | Catálogo completo de deliverables con ✅/⚪/❌, horas, SP, owner primario, rol ejecutor, colaboradores, complejidad, dependencias. |
| 3B.9.2 | Story Points | Derivado directo | 3B.9.3 | Conversión horas → SP según escala del proyecto. |
| 3B.9.4 | Dependency Map | Derivado directo | 3B.9.3 | Dependencias entre tareas, critical path. |
| 3B.9.5 | Complexity Analysis | Derivado directo | 3B.9.3 + 3B.1 + 3B.4 | Justificación técnica de complejidades HIGH/VERY HIGH. |
| 3B.9.8 | Migration & Rollout | Derivado directo | 3B.9.3 + 3B.3 + 3B.8 | Plan ordenado de migraciones técnicas con backup, ventana, rollback. **Condicional.** |
| 3B.9.6 | Risk-Adjusted Estimates | Derivado compuesto | 3B.9.3 + 3B.9.5 + (Risk Register si aplica) | Buffer sobre estimaciones base según riesgos. Separado del baseline. |
| 3B.9.7 | Capacity Plan | Derivado compuesto | 3B.9.3 + 3B.9.4 + 3B.9.6 | Asignación de deliverables a sprints según capacidad de cada rol. |
| 3B.9.9 | Scheduling Inputs for PM | Derivado compuesto | 3B.9.3 + 3B.9.4 + 3B.9.7 | Secuencia de sprints, insumos PM pendientes, ventanas críticas. |
| 3B.9.10 | Routing Index | **BISAGRA** | 3B.9.3 + 3B.1..3B.8 | Mapa Task ID → doc → sección → ADR → SEC → archivos → dep → evidencia → criterio. |
| 3B.9.1 | Estimates Doc (síntesis) | Síntesis final | Todos los anteriores | Resumen ejecutivo. Último en escribirse. |

### 7.2 Orden de producción obligatorio

```
Paso 1 — PIVOTE:
   3B.9.3 Task Breakdown
        ↓
Paso 2 — Derivados directos (paralelizables):
   3B.9.2 Story Points
   3B.9.4 Dependency Map
   3B.9.5 Complexity Analysis
   3B.9.8 Migration & Rollout (si aplica)
        ↓
Paso 3 — Derivados compuestos (semi-paralelizables):
   3B.9.6 Risk-Adjusted   (necesita 3B.9.5)
   3B.9.7 Capacity Plan   (necesita 3B.9.4 + 3B.9.6)
   3B.9.9 Scheduling      (necesita 3B.9.7)
   3B.9.10 Routing Index  (necesita 3B.9.3 + 3B.1..3B.8)
        ↓
Paso 4 — Síntesis final:
   3B.9.1 Estimates Doc
```

### 7.3 Columnas obligatorias del Routing Index (3B.9.10)

Por cada Task ID del Task Breakdown:

| Columna | Origen | Obligatorio |
|---|---|---|
| Task ID | 3B.9.3 | ✅ |
| Sprint | 3B.9.7 | ✅ |
| Owner primario | 3B.9.3 | ✅ |
| Rol ejecutor principal | 3B.9.3 | ✅ |
| Roles colaboradores secundarios | 3B.9.3 | ✅ (puede ser vacía pero presente) |
| Deliverable / Nombre | 3B.9.3 | ✅ |
| Spec Source (doc principal) | 3B.1..3B.8 | ✅ |
| Documento (archivo exacto) | 3B.1..3B.8 | ✅ |
| Sección | 3B.1..3B.8 | ✅ |
| ADR / Decisión cerrada | 3B.6 | ⚠️ Si aplica |
| Control SEC | 3B.7 | ⚠️ Si aplica |
| Archivo / carpeta afectada | 3B.2 | ✅ |
| Dependencia (Task ID upstream) | 3B.9.4 | ⚠️ Si tiene |
| Evidencia mínima | 3B.7 / Test plan | ✅ |
| Criterio de cierre | 3B.9.3 + ADRs | ✅ |
| Migración aplicable | 3B.9.8 | ⚠️ Si aplica |

---

## 8. Procedimiento

### 8.1 FASE 1 — Recepción del paquete técnico

#### 8.1.1 TL recibe notificación del coordinador → **[ACTIVIDAD]**

Confirmación de cierre de `PT-001` con los 8 docs aprobados.

#### 8.1.2 TL verifica accesibilidad de inputs → **[DECISIÓN]**

- 8 docs del paquete técnico en sus paths canónicos.
- SPEC + METODOLOGIA accesibles.
- Catálogo SDLC accesible.
- OPERATIVO accesible.
- (Si feature en sistema operando) docs `3B.X_actual_*` accesibles.

Si falta cualquiera → notifica al coordinador y suspende hasta resolver.

### 8.2 FASE 2 — Producción del PIVOTE (3B.9.3 Task Breakdown)

#### 8.2.1 TL extrae deliverables del catálogo SDLC → **[ACTIVIDAD]**

Para las fases en alcance del bloque/release, lista TODOS los deliverables del catálogo (típicamente Fases 4-7 si es Development+).

#### 8.2.2 Para cada deliverable, TL decide ✅ / ⚪ / ❌ con trazabilidad → **[DECISIÓN]**

**Regla universal U-01 de IPL:** la decisión debe ser trazable contra fuente. No "de memoria".

Criterios:
- **✅** = aplica en R1, se estima y ejecuta. **Justificación:** referencia a SPEC §X o decisión cerrada que lo incluye, o "por defecto al estar en alcance del catálogo SDLC".
- **⚪** = opcional en R1, deseable no bloqueante. **Justificación:** referencia a SPEC §X o ADR que lo marca opcional.
- **❌** = NO aplica en R1. **Justificación obligatoria:** referencia explícita a ADR/decisión cerrada que lo excluye (ej. "ADR-XYZ §3 cierra esta opción").

La columna de justificación va en 3B.9.3 mismo o en doc complementario `3B.9.3.bis_scope_decisions.md`.

#### 8.2.3 Para cada deliverable ✅, TL asigna → **[ACTIVIDAD]**

- Horas estimadas (según escala de complejidad del proyecto).
- SP (conversión horas → SP).
- Owner primario.
- Rol ejecutor principal.
- Roles colaboradores secundarios.
- Complejidad.
- Dependencias (Task IDs upstream).

#### 8.2.4 TL verifica suma matemática del baseline funcional → **[DECISIÓN]**

Suma de horas de deliverables ✅ = baseline funcional declarado.

Si no cuadra → revisar estimaciones individuales o consultar al rol responsable.

### 8.3 FASE 3 — Producción de derivados directos (paralelizables)

#### 8.3.1 TL produce 3B.9.2 Story Points → **[ACTIVIDAD]**

Conversión horas → SP según escala.

#### 8.3.2 TL produce 3B.9.4 Dependency Map → **[ACTIVIDAD]**

Grafo de dependencias entre tareas + critical path.

#### 8.3.3 TL produce 3B.9.5 Complexity Analysis → **[ACTIVIDAD]**

Top 10-15 deliverables más complejos con justificación técnica (referencia a 3B.1, 3B.4).

#### 8.3.4 TL produce 3B.9.8 Migration & Rollout (si aplica) → **[ACTIVIDAD]**

Plan ordenado de migraciones técnicas con backup, ventana, rollback. Referencia 3B.3 y 3B.8.

### 8.4 FASE 4 — Producción de derivados compuestos

#### 8.4.1 TL produce 3B.9.6 Risk-Adjusted Estimates → **[ACTIVIDAD]**

Aplica buffer sobre 3B.9.3 según 3B.9.5 + Risk Register.

> **Regla U-02 de IPL:** Buffer se presenta SEPARADO del baseline funcional. NO se suma al baseline.

#### 8.4.2 TL produce 3B.9.7 Capacity Plan → **[ACTIVIDAD]**

Asignación de deliverables a sprints según capacidad de cada rol.

#### 8.4.3 TL produce 3B.9.9 Scheduling Inputs for PM → **[ACTIVIDAD]**

Secuencia de sprints, insumos PM pendientes (clasificación P0/GATE/DIFERIDO opcional aquí; obligatoria en HO Maestro vía HOPJM-001), ventanas críticas.

#### 8.4.4 TL produce 3B.9.10 Routing Index → **[ACTIVIDAD]**

**Una fila por cada Task ID** del Task Breakdown (✅ y ⚪).

> **Regla U-03 de IPL:** cobertura del Routing Index = 100% de Task IDs del 3B.9.3. Sin cobertura completa, NO se puede declarar 3B.9 entregable.

### 8.5 FASE 5 — Síntesis final (3B.9.1)

#### 8.5.1 TL produce 3B.9.1 Estimates Doc → **[ACTIVIDAD]**

Resumen ejecutivo: totales por escenario (best/expected/worst), métricas globales, conclusión. **Último en escribirse.**

### 8.6 FASE 6 — Verificación de coherencia interna

#### 8.6.1 TL ejecuta checklist de coherencia → **[DECISIÓN]**

- [ ] 3B.9.3 cubre todas las fases en alcance del catálogo SDLC.
- [ ] Cada deliverable ✅ tiene horas > 0.
- [ ] Cada deliverable ✅ tiene owner primario.
- [ ] Cada ❌ tiene justificación con referencia.
- [ ] Suma de horas ✅ = baseline funcional declarado.
- [ ] Distribución técnica interna NO se suma al baseline.
- [ ] OPER se valida por separado.
- [ ] Buffers se validan por separado.
- [ ] Diferidos NO se suman.
- [ ] % funcionales por rol suman 100% solo sobre baseline.
- [ ] Routing Index cubre 100% Task IDs del 3B.9.3.
- [ ] Cada fila del Routing Index tiene todas las columnas obligatorias (§7.3).
- [ ] Critical path en 3B.9.4 es explícito.
- [ ] Top complejidad en 3B.9.5 está justificada.

Si falta cualquiera → corregir antes de invocar `REVMA-001`.

#### 8.6.2 TL elige modo de empaquetado → **[DECISIÓN]**

- **Modo modular:** mantiene 10 archivos separados.
- **Modo consolidado:** genera archivo único `3B.9_IMPLEMENTATION_PLAN_<bloque>_v<X.Y>.md` con las 10 secciones internas.

Ambos modos son aceptados por HOPJM-001. La elección depende del proyecto.

### 8.7 FASE 7 — Ciclo REVMA sobre el 3B.9 consolidado

#### 8.7.1 TL entrega 3B.9 al coordinador → **[ACTIVIDAD]**

#### 8.7.2 Coordinador invoca `VTT.PROTOCOL-REVMA-001` → **[INVOCACIÓN]**

PM Revisor audita el 3B.9 completo (las 10 sub-§ + Routing Index). Hasta 3 vueltas.

#### 8.7.3 ¿3B.9 aprobado? → **[DECISIÓN]**

- **Sí:** continuar a FASE 8.
- **No (escalación REVMA):** suspender hasta resolver.

### 8.8 FASE 8 — Entrega al PM para HO Maestro

#### 8.8.1 Coordinador escribe bitácora del ciclo → **[ACTIVIDAD]**

#### 8.8.2 Coordinador notifica al PM → **[ACTIVIDAD]**

Mensaje:
- Path del 3B.9 (modo + archivo o carpeta).
- Path del Routing Index.
- Confirmación: "3B.9 aprobado, listo para emitir HO Maestro vía VTT.PROTOCOL-HOPJM-001".

#### 8.8.3 Fin del Protocol → **[ACTIVIDAD]**

El PM invoca `VTT.PROTOCOL-HOPJM-001`.

---

## 9. Reglas Críticas de Consolidación

### 9.1 Separación matemática de esfuerzos (regla universal)

| Concepto | Trato |
|---|---|
| Baseline funcional | Suma horas de ✅. Cifra inmutable. |
| Distribución técnica interna (ej. DB) | Desagregación DENTRO del baseline. NO se suma adicionalmente. |
| Esfuerzo operativo (DevOps/SRE) | FUERA del baseline. Validación separada. |
| Buffers de riesgo | FUERA del baseline. Indicativos. |
| Tareas diferidas (Bloque siguiente) | NO se suman. Van a §16 del HO. |
| % funcionales por rol | Suman 100% SOLO sobre baseline funcional. |

### 9.2 Trazabilidad de decisiones ✅/⚪/❌

Cada decisión documentada con justificación verificable. Sin esto, el 3B.9.3 es rechazado en `REVMA`.

### 9.3 Cobertura 100% del Routing Index

Sin esto, no hay 3B.9 entregable.

### 9.4 Pivote no se parchea

Si después del REVMA del 3B.9 se detecta que 3B.9.3 tiene error → regenerar 3B.9.3 + TODOS los derivados (no parche local en algún derivado).

---

## 10. Reglas de Aplicabilidad

### 10.1 Reglas UNIVERSALES

| # | Regla |
|---|---|
| U-01 | Decisión ✅/⚪/❌ debe ser trazable contra fuente. Nunca "de memoria". |
| U-02 | Buffer de riesgo SEPARADO del baseline. NO se suma. |
| U-03 | Routing Index cubre 100% de Task IDs del Task Breakdown. |
| U-04 | Separación matemática de esfuerzos (5 categorías) respetada. |
| U-05 | 3B.9.3 es PIVOTE: si está mal, se regenera + derivados, NO se parchea downstream. |
| U-06 | Ownership separado por deliverable (owner primario único + ejecutor + colaboradores 0..N). |
| U-07 | 3B.9.1 (síntesis) se escribe AL FINAL, no al inicio. |
| U-08 | Modo modular o consolidado: ambos válidos. El TL elige. |
| U-09 | `REVMA-001` obligatorio sobre el 3B.9 completo antes de entregar al PM. |

### 10.2 Reglas CONFIGURABLES

| # | Regla | Configuración por proyecto |
|---|---|---|
| C-01 | Escala de complejidad (LOW/MEDIUM/HIGH/VERY HIGH) y conversión a horas/SP | Por proyecto. Default: LOW=2-3h, MEDIUM=5h, HIGH=8h, VERY HIGH=13h. |
| C-02 | Modo del 3B.9 (modular vs consolidado) | Por proyecto. Default sugerido: consolidado si <100 Task IDs, modular si más. |
| C-03 | Ruta canónica de los sub-docs | Por proyecto. Default sugerido en §6.2. |
| C-04 | Buffer % aplicado por nivel de complejidad | Por proyecto. Default: 0% LOW, 15% MEDIUM, 25% HIGH, 40% VERY HIGH. |
| C-05 | Trazabilidad de decisiones en 3B.9.3 mismo vs doc complementario | Por proyecto. |

### 10.3 Reglas CONDICIONALES

| # | Regla | Condición |
|---|---|---|
| CD-01 | Pista paralela "estado actual" del repo | Feature dentro de sistema operando — `OB-001` activo. |
| CD-02 | 3B.9.8 Migration & Rollout obligatorio | Proyecto tiene migraciones técnicas (DB schema, infra, etc.). |
| CD-03 | Catálogo SDLC genérico como input | Default obligatorio. Excepción justificada: feature muy pequeña con scope explícito en SPEC. |
| CD-04 | Doc complementario `3B.9.3.bis_scope_decisions.md` | Proyecto exige trazabilidad fuera del 3B.9.3 principal. |
| CD-05 | Regeneración tras backfeed | HO o paquete operativo PJM detectó inconsistencia en 3B.9. |

### 10.4 Reglas RETIRADAS

- **R-01:** Decisión ✅/⚪/❌ "de memoria del TL" — RETIRADA. Aprendizaje de Memory Service v1: el TL admitió que decidió de memoria, no es trazable. Regla U-01 cierra esto.

---

## 11. Referencias Cruzadas

### Protocols relacionados

| Protocol | Relación | Estado |
|---|---|---|
| `VTT.PROTOCOL-PT-001` | **Upstream directo.** Provee los 8 docs del paquete técnico. | VIGENTE (1.0.0) |
| `VTT.PROTOCOL-OB-001` | **Paralelo en feature en sistema operando.** Provee docs "estado actual". | EN DESARROLLO |
| `VTT.PROTOCOL-REVMA-001` | **Invocado** sobre el 3B.9 consolidado. | VIGENTE (1.0.0) |
| `VTT.PROTOCOL-HOPJM-001` | **Downstream directo.** Consume 3B.9 + Routing Index para emitir HO. | VIGENTE (2.0.1) |
| `VTT.PROTOCOL-SPRINT-001` | Downstream indirecto. PJM usa 3B.9.10 al generar handoffs. | VIGENTE (2.0.0) |
| `VTT.PROTOCOL-ASG-001` | Downstream lejano. Agentes leen Routing Index al ejecutar. | VIGENTE (1.8.1) |

### Templates referenciados

| Template | Uso |
|---|---|
| Template del 3B.9 consolidado | Por proyecto. Si no existe, referenciar Memory Service `3B.9_IMPLEMENTATION_PLAN_BLOQUE1A_v1.1.md` como ejemplo. |
| Template del Routing Index | Por proyecto. Columnas obligatorias en §7.3. |

### Reglas Nivel 0 aplicables

| Regla | Aplica en |
|---|---|
| `RULE-WORKFLOW-*` | §8 todas las fases |
| `RULE-DOC-*` | §6 artefactos de salida |

---

## 12. Resumen de Revisiones

| Versión | Fecha | Editor | Cambios |
|---|---|---|---|
| 1.0.0 | 2026-05-31 | TW-OPS | **Versión inicial.** Formaliza la consolidación 3B.9 + Routing Index. Codifica: (1) 3B.9.3 PIVOTE / 3B.9.10 BISAGRA; (2) orden de producción obligatorio (PIVOTE → derivados directos → derivados compuestos → síntesis); (3) modos modular y consolidado; (4) separación matemática de esfuerzos en 5 categorías; (5) trazabilidad obligatoria de ✅/⚪/❌; (6) cobertura 100% del Routing Index; (7) ownership separado por deliverable (owner primario único + ejecutor + colaboradores); (8) columnas obligatorias del Routing Index (§7.3); (9) invocación de `REVMA-001` sobre el 3B.9 completo; (10) entrega formal al PM para activar `HOPJM-001`. |

---

## Anexos

### Anexo A — Diagrama de flujo end-to-end

```mermaid
flowchart TD
    START([🟢 PT-001 cerrado, 8 docs aprobados])

    F1[F1 Verificar accesibilidad de inputs]
    F2[F2 Producir PIVOTE 3B.9.3]
    F2_DEC{¿Suma baseline OK?}
    F2_FIX[Revisar estimaciones]

    F3a[3B.9.2 SP]
    F3b[3B.9.4 Deps]
    F3c[3B.9.5 Complexity]
    F3d[3B.9.8 Migration]

    F4a[3B.9.6 Risk-Adjusted]
    F4b[3B.9.7 Capacity]
    F4c[3B.9.9 Scheduling]
    F4d[3B.9.10 Routing Index]
    F4_DEC{¿Routing cubre 100%?}
    F4_FIX[Completar Routing Index]

    F5[F5 3B.9.1 Síntesis]

    F6[F6 Checklist coherencia]
    F6_DEC{¿Todo OK?}
    F6_FIX[Corregir]

    F7[F7 REVMA-001 sobre 3B.9]
    F7_DEC{¿Aprobado?}

    F8[F8 Notificar al PM]

    END_OK([🔵 PM inicia HOPJM-001])
    END_SUSP([🟠 Suspensión])

    START --> F1 --> F2 --> F2_DEC
    F2_DEC -->|No| F2_FIX --> F2
    F2_DEC -->|Sí| F3a
    F2_DEC -->|Sí| F3b
    F2_DEC -->|Sí| F3c
    F2_DEC -->|Sí| F3d

    F3a --> F4a
    F3b --> F4b
    F3c --> F4a
    F3d --> F4c

    F4a --> F4b --> F4c --> F4d --> F4_DEC
    F4_DEC -->|No| F4_FIX --> F4d
    F4_DEC -->|Sí| F5

    F5 --> F6 --> F6_DEC
    F6_DEC -->|No| F6_FIX --> F6
    F6_DEC -->|Sí| F7 --> F7_DEC

    F7_DEC -->|No (3 vueltas)| END_SUSP
    F7_DEC -->|Sí| F8 --> END_OK
```

### Anexo B — Checklist consolidado pre-REVMA

- [ ] 8 docs del paquete técnico (3B.1..3B.8) aprobados y accesibles.
- [ ] METODOLOGIA + SPEC aprobadas y accesibles.
- [ ] Catálogo SDLC accesible.
- [ ] OPERATIVO con UUIDs reales accesible.
- [ ] (Si feature en sistema operando) docs `3B.X_actual_*` accesibles.
- [ ] 3B.9.3 producido con TODAS las columnas obligatorias.
- [ ] Cada ✅ tiene horas > 0 y owner primario.
- [ ] Cada ❌ tiene justificación trazable.
- [ ] Suma de horas ✅ = baseline funcional declarado.
- [ ] Distribución técnica interna NO se suma.
- [ ] OPER se valida por separado.
- [ ] Buffers se validan por separado.
- [ ] Diferidos NO se suman.
- [ ] % funcionales por rol = 100% solo sobre baseline.
- [ ] 3B.9.2, 3B.9.4, 3B.9.5 producidos (derivados directos).
- [ ] 3B.9.8 producido si aplica.
- [ ] 3B.9.6, 3B.9.7, 3B.9.9 producidos (derivados compuestos).
- [ ] 3B.9.10 Routing Index cubre 100% Task IDs.
- [ ] Cada fila Routing Index tiene columnas obligatorias §7.3.
- [ ] 3B.9.1 síntesis producido al final.
- [ ] Critical path explícito en 3B.9.4.
- [ ] Top complejidad justificado en 3B.9.5.
- [ ] Modo elegido (modular / consolidado).

### Anexo C — Glosario operativo

| Término | Definición abreviada |
|---|---|
| PIVOTE | 3B.9.3 Task Breakdown — fuente de los 9 derivados |
| BISAGRA | 3B.9.10 Routing Index — conecta upstream con downstream |
| Derivado directo | Sub-doc que solo necesita 3B.9.3 |
| Derivado compuesto | Sub-doc que necesita 3B.9.3 + otros derivados |
| Síntesis | 3B.9.1 — último en escribirse |
| Separación matemática | 5 categorías de esfuerzo que no se suman entre sí |
| Trazabilidad de decisión | Justificación verificable de ✅/⚪/❌ |
| Cobertura Routing Index | 100% Task IDs del Task Breakdown deben tener fila |
| Modo modular | 10 archivos separados |
| Modo consolidado | 1 archivo con 10 sub-§ |

---

| Editor | Dueño | Última Actualización |
|---|---|---|
| TW-OPS (fe1b589c-7cf2-4779-82d4-b7ae536536ce) | PM Governance / Process Owner VTT | 2026-05-31 |

**Versión:** 1.0.0 — Consolidación 3B.9 con PIVOTE/BISAGRA, separación matemática y trazabilidad de decisiones.
**Estado:** Aprobado

*Versión más reciente en `virtual-teams-setup`. No controlada si se imprime.*
