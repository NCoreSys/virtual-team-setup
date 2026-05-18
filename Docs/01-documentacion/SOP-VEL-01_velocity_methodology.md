# SOP-VEL-01 — Metodología de Velocity para Equipos de Agentes IA

**Versión:** 1.0  
**Fecha:** 2026-05-12  
**Autor:** TL Memory Service — `92225290-6b6b-4c1f-a940-dcb4262507aa`  
**Aplica a:** PM, TL, PJM — para cualquier proyecto que use agentes IA como equipo de desarrollo  
**Propósito:** Definir cómo se mide, calcula, actualiza y consume la velocity del equipo en VTT.

---

## 1. Qué es velocity en este contexto

**Velocity** = la cantidad de trabajo real (horas o SP) que el equipo de agentes completa por sprint, medido a partir de datos históricos de ejecución.

En un equipo de agentes IA, velocity tiene propiedades distintas a un equipo humano:

| Característica | Equipo humano | Equipo de agentes IA |
|----------------|---------------|----------------------|
| Curva de aprendizaje | Alta al inicio, baja con experiencia | Casi plana — cada sesión parte desde contexto |
| Variabilidad inter-sprint | Alta (vacaciones, carga) | Baja — consistente si los prompts son buenos |
| Variabilidad intra-tarea | Baja | Media — depende de calidad del assignment |
| Overhead de coordinación | 15-25% | 5-10% (solo TL review) |
| Factor de documentación | Variable | Alto — devlogs, code logic obligatorios |

---

## 2. Unidades de medida

### 2.1 Story Points (SP)
- Escala Fibonacci: 1, 2, 3, 5, 8, 13
- **1 SP = 1 hora de agente** (para este equipo)
- Medir en SP permite comparar entre proyectos aunque las horas varíen

### 2.2 Horas de sesión de agente
- Medida más granular
- Fuente: devlogs (cuando el agente registra duración) o diferencia de timestamps VTT
- Cuando VTT no tiene transición completa: usar longitud del output como proxy (ver §4)

### 2.3 Factor de velocity (FV)
```
FV = Horas reales / Horas estimadas
```
- FV < 1.0 → el equipo es más rápido que lo estimado (subestimamos)
- FV > 1.0 → el equipo es más lento que lo estimado (sobreestimamos)
- FV ideal: 0.85–1.10 (estimaciones calibradas)

---

## 3. Granularidades de velocity

VTT puede calcular velocity en 4 niveles:

### Nivel 1 — Por deliverable (más granular)
```
FV(deliverable) = horas reales del deliverable / horas estimadas del deliverable
```
- Ejemplo: `4.3.1 API Endpoints` estimado 8h, tomó 6.5h → FV = 0.81
- Útil para: calibrar estimaciones del catálogo estándar por tipo de deliverable

### Nivel 2 — Por subfase
```
FV(subfase) = Σ horas reales de la subfase / Σ horas estimadas de la subfase
```
- Ejemplo: subfase 4.3 Backend Development estimada 95h, tomó 78h → FV = 0.82
- Útil para: estimar subfases completas en proyectos futuros

### Nivel 3 — Por fase
```
FV(fase) = Σ horas reales de la fase / Σ horas estimadas de la fase
```
- Ejemplo: Fase 4 estimada 370h, tomó 310h → FV = 0.84
- Útil para: planificación de alto nivel de fases completas

### Nivel 4 — Por proyecto (más agregado)
```
FV(proyecto) = Σ horas reales del proyecto / Σ horas estimadas del proyecto
```
- Útil para: comparar proyectos entre sí y detectar si los agentes mejoran con el tiempo

---

## 4. Fuentes de datos para calcular horas reales

En orden de confiabilidad:

| Fuente | Confiabilidad | Cómo extraer |
|--------|---------------|--------------|
| VTT: timestamp `in_progress` → `completed` | ⭐⭐⭐⭐ | `GET /api/tasks/:id` → `statusHistory` |
| Devlog: "Sesión de X horas" explícito | ⭐⭐⭐⭐ | Leer campo "Duración" o "Sesión" en devlog |
| Devlog: timestamps de inicio y fin implícitos | ⭐⭐⭐ | Metadata del archivo (created + modified) |
| Proxy por longitud de output | ⭐⭐ | Líneas de código + docs / velocidad promedio del agente |
| Estimación del TL post-hoc | ⭐ | Solo si no hay otra fuente |

### 4.1 Cálculo del proxy por longitud (cuando VTT no tiene transición completa)

Para el 20% de tareas sin transición completa (situación actual en Memory Service con ~80% de datos completos):

```
Horas estimadas por proxy = (líneas de código generadas / 200) + (líneas de docs generadas / 100)
```

Calibración basada en observaciones del equipo:
- Un agente escribe ~200 líneas de código TypeScript/hora
- Un agente escribe ~100 líneas de markdown estructurado/hora

Marcar siempre los valores proxy con `(*)` en los reportes.

### 4.2 Tratamiento de datos incompletos

Cuando una tarea no tiene datos suficientes:
1. Usar el proxy de longitud si hay archivos creados
2. Si ni eso: usar la estimación original con FV = 1.0 (neutro)
3. Documentar como "sin datos" en el reporte de velocity
4. No excluir la tarea — distorsionaría los totales

---

## 5. Proceso de actualización de velocity

### 5.1 Cuándo actualizar

| Evento | Acción |
|--------|--------|
| Al cerrar cada sprint | Calcular FV del sprint y actualizar rolling average |
| Al cerrar cada fase | Calcular FV de la fase y actualizar histórico de fases |
| Al cerrar un proyecto | Calcular FV total y agregar al histórico inter-proyectos |

### 5.2 Rolling average de velocity

No usar el FV de un solo sprint — usar promedio móvil de los últimos 3 sprints:

```
FV_rolling = (FV_sprint_N + FV_sprint_N-1 + FV_sprint_N-2) / 3
```

Este valor es el que se usa para ajustar estimaciones en el siguiente sprint.

### 5.3 Archivo de velocity histórica

```
knowledge/retrospectives/VELOCITY_HISTORICA_[proyecto].md
```

Estructura:

```markdown
# Velocity Histórica — [Proyecto]

## Por Sprint (Fase 4)
| Sprint | SP Planif. | SP Real | FV Sprint | FV Rolling |
|--------|-----------|---------|-----------|------------|
| S1 | 74 | 58 | 0.78 | — |
| S2 | 67 | 71 | 1.06 | 0.92 |
| S3 | 70 | 65 | 0.93 | 0.92 |

## Por Fase
| Fase | Horas Est. | Horas Reales | FV Fase | Datos completos |
|------|-----------|--------------|---------|-----------------|
| 3B | 6h (TL) | 5.5h | 0.92 | 100% |
| 4 | 370h | — | — | 0% (en progreso) |

## Por Tipo de Deliverable (acumulado)
| Tipo | Horas est. promedio | Horas reales promedio | FV tipo | N muestras |
|------|--------------------|-----------------------|---------|-----------|
| README / Guías | 2h | 1.5h | 0.75 | 12 |
| Endpoint REST MEDIUM | 5h | 4.2h | 0.84 | 8 |
| Endpoint REST HIGH | 8h | 7.8h | 0.98 | 3 |
| Migración DB | 8h | 9.5h | 1.19 | 4 |
```

---

## 6. Cómo VTT puede calcular velocity automáticamente

### 6.1 Datos que VTT ya tiene (actualmente)

- Timestamps de cambio de estado por tarea (cuando la transición está completa)
- SP estimados por tarea (si se registran al crear la tarea)
- Asignado (rol del agente)
- Fase y subfase de la tarea

### 6.2 Datos que VTT necesitaría agregar

| Dato | Dónde añadirlo | Tipo |
|------|---------------|------|
| SP reales al completar | Campo en `PATCH /tasks/:id/status` cuando pasa a `completed` | Number |
| Horas reales al completar | Campo en `PATCH /tasks/:id/status` | Number |
| ID de deliverable del catálogo | Campo en task (ej: `catalogId: "4.3.1"`) | String |
| Flag "datos completos" | Calculado: ¿tiene timestamps de todos los estados? | Boolean |

### 6.3 Algoritmo de cálculo propuesto para VTT

```
Para cada proyecto:
  Para cada tarea con datos completos:
    duracion_real = timestamp_completed - timestamp_in_progress (en horas)
    sp_real = sp_estimados * (duracion_real / horas_estimadas)  // si no se registran SP reales
    
    fv_tarea = duracion_real / horas_estimadas
    
  Por fase:
    fv_fase = Σ(duracion_real de tareas de la fase) / Σ(horas_estimadas de la fase)
    
  Por tipo de deliverable (catalogId prefix):
    fv_tipo = promedio de fv_tarea donde catalogId empieza con "X.Y"
    
  Por proyecto:
    fv_proyecto = Σ(duracion_real) / Σ(horas_estimadas)
    cobertura = tareas_con_datos_completos / total_tareas
```

### 6.4 Granularidades calculables en VTT

| Granularidad | ¿VTT puede calcular hoy? | Qué falta |
|-------------|--------------------------|-----------|
| Por proyecto | ⚠️ Parcial (80% datos) | Completar algoritmo de transiciones |
| Por fase | ⚠️ Parcial | Etiquetado de fase en tareas |
| Por subfase | ❌ No | Campo `catalogId` en tareas |
| Por deliverable | ❌ No | Campo `catalogId` + SP reales al completar |
| Por tipo de deliverable | ❌ No | `catalogId` + categorización |
| Por rol | ✅ Sí | Ya tiene asignado por tarea |

### 6.5 Roadmap de implementación sugerido

**Iteración 1 (ya en curso según datos del proyecto):**
- Completar el algoritmo de transiciones para cubrir el 20% de tareas sin datos
- Resultado: velocity por proyecto con 95%+ cobertura

**Iteración 2:**
- Agregar campo `catalogId` al crear tareas (ej: `4.3.1`)
- Agregar campo `horasReales` al mover tarea a `completed`
- Resultado: velocity por subfase y tipo de deliverable

**Iteración 3:**
- Dashboard de velocity en VTT: FV por proyecto, fase, tipo
- Alertas cuando FV > 1.3 en un sprint (el equipo está más lento de lo esperado)
- Resultado: velocity como métrica operativa en tiempo real

---

## 7. Cómo usar velocity para mejorar estimaciones futuras

### 7.1 Ajuste de estimaciones

Si el FV histórico de un tipo de deliverable es 0.80 (el equipo es 20% más rápido):

```
Horas ajustadas = Horas del catálogo × FV_tipo
```

Ejemplo: catálogo dice 5h para un endpoint MEDIUM, FV_tipo = 0.80 → usar 4h en la próxima estimación.

### 7.2 Cuándo NO ajustar

- Si hay menos de 5 muestras del tipo → insuficiente para ser estadísticamente significativo
- Si el proyecto tiene características muy diferentes (stack distinto, dominio distinto)
- Si la mejora se debe a un assignment excepcionalmente bueno (no replicable)

### 7.3 Velocity inter-proyectos

Cuando hay múltiples proyectos en VTT usando el mismo catálogo estándar:

```
FV_global_tipo = promedio ponderado de FV_tipo por proyecto
                 ponderado por número de muestras
```

Este valor es el más confiable para estimar proyectos nuevos.

---

## 8. Velocity por fase vs velocity de desarrollo

Es importante no mezclar:

| Tipo | Qué mide | Para qué sirve |
|------|----------|----------------|
| Velocity de Fase 4 (Development) | SP completados por sprint | Planificación de sprints de desarrollo |
| Velocity de Fase 3B (Design Technical) | Horas por deliverable de arquitectura | Estimar duración de fase de diseño |
| Velocity de Fase 2 (Analysis) | Horas por deliverable de análisis | Estimar fase de análisis en nuevos proyectos |
| Velocity por tipo de deliverable | FV por tipo (README, Endpoint, Migration...) | Calibrar el catálogo estándar |

Un proyecto nuevo se beneficia de todos estos niveles:
- "¿Cuánto tarda la Fase 3B?" → usar FV de Fase 3B de proyectos similares
- "¿Cuántas horas para implementar un endpoint HIGH?" → usar FV de tipo "Endpoint REST HIGH"
- "¿Cuántos sprints de desarrollo?" → usar FV de Fase 4 del equipo

---

## 9. Preguntas frecuentes

**¿La velocity de agentes IA mejora con el tiempo?**  
No de la misma forma que un equipo humano. Lo que mejora es la calidad de los assignments y los SOPs. Mejorar el SOP-EST-01 reduce el rework. Mejorar los prompts del SOP-RET-01 reduce el tiempo de retrospectiva. La velocity del agente individual es constante; la del sistema mejora.

**¿Se puede comparar velocity entre proyectos de dominios diferentes?**  
Solo al nivel de tipo de deliverable genérico (README, Endpoint MEDIUM, Migración DB). La velocity de "Import Service con idempotencia" es específica de ese proyecto.

**¿Qué hacer si el FV es muy alto (>1.5) en un sprint?**  
Investigar si: (a) el assignment fue deficiente y requirió muchas iteraciones, (b) hay un riesgo que se materializó, o (c) el deliverable era más complejo de lo estimado. No ajustar velocity global por un outlier — registrar la causa en el devlog del sprint.

**¿Con qué frecuencia actualizar el archivo VELOCITY_HISTORICA?**  
Al final de cada sprint durante Fase 4. Al cerrar cada fase para Fases 0–3, 5, 6, 7.

---

**Documento:** SOP-VEL-01_velocity_methodology.md | **Versión:** 1.0 | **Fecha:** 2026-05-12  
**Relacionado con:** SOP-EST-01 (estimación), SOP-RET-01 (retrospectiva), VTT velocity feature (roadmap)
