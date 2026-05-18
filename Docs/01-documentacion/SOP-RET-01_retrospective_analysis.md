# SOP-RET-01 — Análisis Retrospectivo por Fase (con Prompts para Agentes)

**Versión:** 1.0  
**Fecha:** 2026-05-12  
**Autor:** TL Memory Service — `92225290-6b6b-4c1f-a940-dcb4262507aa`  
**Aplica a:** PM, SA, DL, TL — al cierre de cada fase del SDLC  
**Propósito:** Documentar qué se hizo realmente vs qué estaba planificado, y generar los datos de velocity histórica del equipo de agentes.

---

## 1. Por qué hacer el análisis retrospectivo

El catálogo ANALISIS_FASES_COMPLETO_PARA_PM.md define los deliverables estándar de cada fase. El análisis retrospectivo responde:

1. ¿Qué deliverables del catálogo se ejecutaron realmente?
2. ¿Cuánto tiempo tomó cada uno (horas reales de sesión de agente)?
3. ¿Qué se omitió y por qué?
4. ¿Qué se añadió que no estaba en el catálogo?
5. ¿Cuál es la velocity real del equipo en este tipo de deliverable?

Esos datos calibran las estimaciones futuras y alimentan el SOP-VEL-01 de velocity.

---

## 2. Cuándo ejecutar por fase

| Fase | Quién lo ejecuta | Cuándo |
|------|-----------------|--------|
| 0 — Discovery | PM | Al aprobar todos los deliverables de Fase 0 |
| 1 — Planning | PM + Program Manager | Al aprobar todos los deliverables de Fase 1 |
| 2 — Analysis | SA (Solution Analyst) | Al aprobar todos los deliverables de Fase 2 |
| 3A — Design UX/UI | Design Lead | Al aprobar todos los deliverables de Fase 3A |
| 3B — Design Technical | Tech Lead | Al aprobar todos los deliverables de Fase 3B |
| 4 — Development | TL + BE + FE + DB | Al finalizar cada sprint y al cerrar la fase |
| 5 — Testing | QA Lead | Al aprobar la fase de testing |
| 6 — Deploy | DevOps Lead | Post-deploy exitoso a producción |
| 7 — Operations | SRE / TL | Cada trimestre |

---

## 3. Inputs necesarios (generales)

Antes de ejecutar el análisis, el agente debe localizar:

| Input | Dónde encontrarlo | Qué extraer |
|-------|------------------|-------------|
| Catálogo de deliverables de la fase | `ANALISIS_FASES_COMPLETO_PARA_PM.md` §Fase X | Lista de IDs esperados (X.Y.Z) |
| Devlogs de la fase | `knowledge/development-log/` filtrado por fecha de la fase | Horas de sesión, decisiones, archivos creados |
| Tareas VTT de la fase | `GET /api/tasks?phase=X` o búsqueda por prefijo de tarea | Fechas de transición de estado, asignados |
| Archivos entregados | `phases/0X-*/deliverables/` | Existencia real de cada deliverable |
| Assignments ejecutados | `knowledge/agent-tasks/assignments/` | Scope real de cada tarea |

**Regla de datos parciales:** Si una tarea en VTT no tiene transición completa (estado inicial → in_progress → completed), estimar el tiempo desde el devlog (fecha de creación del archivo + longitud del documento como proxy). Anotar como "estimado" en el output.

---

## 4. Output esperado

Un archivo markdown por fase:

```
knowledge/retrospectives/RETRO_FASE_[X]_[proyecto]_[fecha].md
```

Estructura:
1. Resumen ejecutivo (deliverables ejecutados / omitidos / añadidos)
2. Tabla de deliverables con horas reales
3. Comparativa estimado vs real (si hubo estimación previa)
4. Velocity calculada por tipo de deliverable
5. Hallazgos y recomendaciones

---

## 5. Prompts por rol

---

### 5.1 PM — Fases 0 y 1

**Cuándo usar:** Al cerrar Fase 0 (Discovery) o Fase 1 (Planning).

**Inputs que el PM debe reunir antes de dar el prompt:**
- Ruta a `ANALISIS_FASES_COMPLETO_PARA_PM.md`
- Ruta a `knowledge/development-log/` del proyecto
- Rango de fechas de la fase
- Ruta a `phases/00-discovery/deliverables/` y `phases/01-planning/deliverables/`
- IDs de las tareas VTT de la fase (ej: MS-001..MS-010)

**Prompt para el agente:**

```
Eres un agente de análisis retrospectivo. Tu tarea es documentar qué se hizo realmente en la [Fase 0 / Fase 1] del proyecto [NOMBRE_PROYECTO].

## Inputs a leer (en este orden)

1. `[RUTA]/ANALISIS_FASES_COMPLETO_PARA_PM.md` — secciones FASE 0 y/o FASE 1
   → Extrae la lista de deliverables esperados con sus IDs (0.1.1, 0.1.2... / 1.1.1, 1.1.2...)

2. `[RUTA]/phases/00-discovery/deliverables/` y/o `[RUTA]/phases/01-planning/deliverables/`
   → Lista los archivos que realmente existen

3. `[RUTA]/knowledge/development-log/` — filtrar archivos con fecha entre [FECHA_INICIO] y [FECHA_FIN]
   → Por cada devlog: extraer tarea ID, fecha, archivos creados, horas estimadas (si las menciona)

4. `[RUTA]/knowledge/agent-tasks/assignments/` — assignments de las tareas de esta fase
   → Extraer scope real ejecutado por cada agente

## Qué producir

Crea el archivo `[RUTA]/knowledge/retrospectives/RETRO_FASE_0_[proyecto]_[fecha].md` con:

### Sección 1 — Resumen ejecutivo
- Total deliverables esperados según catálogo
- Total deliverables ejecutados (archivo existe en repo)
- Total deliverables omitidos (justificación)
- Total deliverables añadidos fuera del catálogo

### Sección 2 — Tabla de deliverables
Para cada ID del catálogo (0.1.1, 0.1.2...):
| ID | Deliverable | Ejecutado | Archivo en repo | Horas reales | Fuente tiempo | Notas |
|----|-------------|-----------|-----------------|--------------|---------------|-------|
| 0.1.1 | Market Research Report | ✅ | phases/00.../market_research.md | 3h | devlog MS-001 | — |
| 0.1.2 | TAM/SAM/SOM | ❌ No ejecutado | — | — | — | No aplicó al ser herramienta interna |

### Sección 3 — Velocity observada
Agrupa por complejidad estimada (LOW/MEDIUM/HIGH) y calcula:
- Horas promedio por deliverable LOW
- Horas promedio por deliverable MEDIUM
- Horas promedio por deliverable HIGH
- Factor de velocity = horas reales / horas estimadas (si hay estimación previa)

### Sección 4 — Hallazgos
Lista máximo 5 hallazgos concretos: qué fue más rápido de lo esperado, qué tomó más tiempo, qué faltó en el catálogo.

### Sección 5 — Recomendaciones para próximos proyectos
Ajustes concretos al catálogo o al proceso basados en lo observado.

## Reglas
- No inventar datos. Si no hay devlog para un deliverable, marcar como "sin registro"
- Horas estimadas desde devlog: usar tiempo de sesión si está mencionado; si no, marcar como "estimado por longitud"
- Marcar con asterisco (*) todos los datos estimados vs medidos
```

---

### 5.2 SA — Fase 2 (Analysis)

**Cuándo usar:** Al cerrar Fase 2.

**Inputs que el SA debe reunir:**
- Ruta a `ANALISIS_FASES_COMPLETO_PARA_PM.md` sección FASE 2
- Ruta a `phases/02-analysis/deliverables/`
- Devlogs de las tareas MS-018..MS-025 (o equivalentes)
- Assignments de esas tareas

**Prompt para el agente:**

```
Eres un agente de análisis retrospectivo para la Fase 2 — Analysis del proyecto [NOMBRE_PROYECTO].

## Inputs a leer

1. `[RUTA]/ANALISIS_FASES_COMPLETO_PARA_PM.md` sección FASE 2 (subfases 2.1..2.8)
   → Lista de 47 deliverables esperados (2.1.1..2.8.4)

2. `[RUTA]/phases/02-analysis/deliverables/` — todos los subdirectorios
   → Lista real de archivos existentes

3. Devlogs de tareas de Fase 2: `[RUTA]/knowledge/development-log/` filtrar por [MS-018..MS-025 o equivalente]
   → Extraer: tarea, fecha, archivos creados, horas de sesión

4. `[RUTA]/knowledge/agent-tasks/assignments/ASSIGNMENT_[TAREA]_*.md`
   → Scope real: qué se pidió al agente, cuántos entregables por tarea

## Qué producir

`[RUTA]/knowledge/retrospectives/RETRO_FASE_2_[proyecto]_[fecha].md`

Estructura igual que en §5.1 pero para la Fase 2:
- Sección 1: resumen (de 47 esperados, cuántos ejecutados/omitidos/añadidos)
- Sección 2: tabla con los 47 IDs del catálogo (2.1.1..2.8.4)
- Sección 3: velocity por tipo de deliverable de análisis (SRS, Use Cases, User Stories, Business Rules...)
- Sección 4: hallazgos (¿qué deliverables de análisis agregaron más valor? ¿cuáles fueron redundantes?)
- Sección 5: recomendaciones para ajustar el catálogo en proyectos similares

## Consideración especial para Fase 2
Los deliverables de análisis tienen alto valor documental pero bajo impacto en velocity de desarrollo.
Identificar cuáles fueron realmente consultados por los agentes de Fase 3B y cuáles quedaron como documentación sin uso.
Esto informa si el catálogo de Fase 2 debe simplificarse para proyectos similares.
```

---

### 5.3 DL — Fase 3A (Design UX/UI)

**Cuándo usar:** Al cerrar Fase 3A.

**Inputs que el DL debe reunir:**
- Ruta a `ANALISIS_FASES_COMPLETO_PARA_PM.md` sección FASE 3A
- Ruta a `phases/03-design/deliverables/` (subcarpetas de 3A)
- Devlogs de tareas MS-026..MS-038 (o equivalentes)
- Nota: Fase 3A tiene 72 deliverables en el catálogo estándar — muchos son Figma/visual, no archivos MD

**Prompt para el agente:**

```
Eres un agente de análisis retrospectivo para la Fase 3A — Design UX/UI del proyecto [NOMBRE_PROYECTO].

## Inputs a leer

1. `[RUTA]/ANALISIS_FASES_COMPLETO_PARA_PM.md` sección FASE 3A (subfases 3A.1..3A.9)
   → Lista de 72 deliverables esperados

2. `[RUTA]/phases/03-design/deliverables/` — subcarpetas: personas/, wireframes/, design-system/, handoff/, etc.
   → Lista real de archivos existentes

3. Devlogs de tareas de Fase 3A: filtrar `knowledge/development-log/` por rango de fechas de la fase

4. Assignments de las tareas de diseño

## Consideración especial para Fase 3A
Muchos deliverables del catálogo (Figma, prototipos, assets visuales) no son archivos markdown.
Para estos, marcar como:
- ✅ Ejecutado (fuera de repo) — si el devlog confirma que se creó aunque sea en Figma/tool externa
- 📄 En repo (MD) — si existe como archivo markdown equivalente
- ❌ No ejecutado — si no hay evidencia en devlog ni en repo

El análisis debe separar deliverables "en repo" de "en herramienta externa" en la tabla.

## Qué producir

`[RUTA]/knowledge/retrospectives/RETRO_FASE_3A_[proyecto]_[fecha].md`

Estructura igual a §5.1 + sección adicional:
- Sección 6 — Formato de entrega: ¿qué porcentaje de deliverables terminó en markdown vs herramienta visual?
  Esto informa si el equipo de agentes puede ejecutar Fase 3A completamente o necesita un Design Lead humano.
```

---

### 5.4 TL — Fase 3B (Design Technical)

**Cuándo usar:** Al cerrar Fase 3B (ya ejecutado parcialmente en MS-047).

**Prompt para el agente:**

```
Eres el Tech Lead. Ejecuta el análisis retrospectivo de la Fase 3B — Design Technical del proyecto [NOMBRE_PROYECTO].

## Inputs a leer

1. `[RUTA]/ANALISIS_FASES_COMPLETO_PARA_PM.md` sección FASE 3B (subfases 3B.1..3B.9)
   → 73 deliverables esperados

2. `[RUTA]/phases/03-design/deliverables/` — todas las subcarpetas de 3B
   → Lista real de archivos existentes por subcarpeta

3. Devlogs de tareas MS-039..MS-047:
   `[RUTA]/knowledge/development-log/` filtrado por esas tareas

4. Assignments de MS-039..MS-047:
   `[RUTA]/knowledge/agent-tasks/assignments/ASSIGNMENT_MS-03*.md` y `ASSIGNMENT_MS-04*.md`

## Qué producir

`[RUTA]/knowledge/retrospectives/RETRO_FASE_3B_[proyecto]_[fecha].md`

Sección especial para 3B: mapear cada deliverable real contra su ID del catálogo.
Nota: los entregables de 3B a veces tienen numeración propia (3B.1.1, 3B.1.4...) que no coincide exactamente
con el catálogo (3B.1.1, 3B.1.2...). El agente debe hacer el mapeo explícito:

| ID catálogo | Nombre catálogo | ID real en repo | Archivo en repo | Ejecutado |
|-------------|-----------------|-----------------|-----------------|-----------|
| 3B.1.1 | Architecture Document | 3B.1.1 | solution-architecture/3B.1.1_architecture_document.md | ✅ |
| 3B.1.2 | System Context Diagram | 3B.1.2 | solution-architecture/3B.1.2_context_diagram_c4_l1.md | ✅ |
```

---

### 5.5 TL + BE + DO — Fase 4 (Development) — Por Sprint

**Cuándo usar:** Al finalizar cada sprint durante Fase 4.

**Prompt para el agente (ejecutar al final de cada sprint):**

```
Eres el Tech Lead. Ejecuta el análisis retrospectivo del Sprint [N] de la Fase 4 — Development
del proyecto [NOMBRE_PROYECTO].

## Inputs a leer

1. `[RUTA]/phases/03-design/deliverables/estimates/3B.9.9_capacity_plan.md`
   → Plan del sprint [N]: qué deliverables estaban planificados, con qué horas estimadas

2. Devlogs del sprint [N]: `[RUTA]/knowledge/development-log/` filtrar por fechas [INICIO..FIN del sprint]
   → Por cada tarea: ID, horas reales de sesión, deliverables completados

3. Tareas VTT del sprint [N]: IDs de las tareas, fechas de transición in_progress → completed

4. `[RUTA]/phases/03-design/deliverables/estimates/3B.9.3_task_breakdown.md`
   → Estimación original de cada deliverable ejecutado en el sprint

## Qué producir

`[RUTA]/knowledge/retrospectives/RETRO_SPRINT_[N]_FASE4_[proyecto]_[fecha].md`

### Sección 1 — Comparativa Sprint Plan vs Real
| Deliverable ID | Planificado | Horas est. | Horas reales | Delta | Estado |
|----------------|-------------|------------|--------------|-------|--------|
| 4.1.1 | ✅ | 3h | 2.5h | -0.5h | ✅ Completado |
| 4.2.1 | ✅ | 8h | 11h | +3h | ✅ Completado |
| 4.3.7 | ✅ | 8h | — | — | ⚠️ Movido a S[N+1] |

### Sección 2 — Velocity del sprint
- SP completados / SP planificados = % de cumplimiento
- Horas reales totales del sprint
- Factor de ajuste: horas reales / horas estimadas

### Sección 3 — Blockers encontrados
Lista de blockers que surgieron, cuánto tiempo consumieron, cómo se resolvieron.

### Sección 4 — Ajuste para siguiente sprint
Basado en la velocity real de este sprint, ¿hay deliverables que deben moverse o reestimarse?
```

---

## 6. Estructura de carpetas para retrospectivas

```
knowledge/
└── retrospectives/
    ├── RETRO_FASE_0_[proyecto]_[fecha].md
    ├── RETRO_FASE_1_[proyecto]_[fecha].md
    ├── RETRO_FASE_2_[proyecto]_[fecha].md
    ├── RETRO_FASE_3A_[proyecto]_[fecha].md
    ├── RETRO_FASE_3B_[proyecto]_[fecha].md
    ├── RETRO_SPRINT_01_FASE4_[proyecto]_[fecha].md
    ├── RETRO_SPRINT_02_FASE4_[proyecto]_[fecha].md
    ├── ...
    ├── RETRO_FASE_5_[proyecto]_[fecha].md
    ├── RETRO_FASE_6_[proyecto]_[fecha].md
    └── VELOCITY_HISTORICA_[proyecto].md  ← alimentado por SOP-VEL-01
```

---

## 7. Qué hacer con los datos retrospectivos

Una vez generados los archivos de retrospectiva:

1. **El PM extrae la velocity por tipo de deliverable** → actualiza `VELOCITY_HISTORICA_[proyecto].md`
2. **El TL ajusta las estimaciones futuras** → si el factor de velocity es consistentemente 0.7x, bajar horas base
3. **El SA propone ajustes al catálogo** → si deliverables fueron sistemáticamente omitidos o añadidos fuera del catálogo
4. **VTT recibe los datos** → ver SOP-VEL-01 para el proceso de ingesta en VTT

---

**Documento:** SOP-RET-01_retrospective_analysis.md | **Versión:** 1.0 | **Fecha:** 2026-05-12
