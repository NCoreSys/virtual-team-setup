# SOP-EST-01 — Proceso de Estimación Técnica (Technical Estimates)

**Versión:** 1.0  
**Fecha:** 2026-05-12  
**Autor:** TL Memory Service — `92225290-6b6b-4c1f-a940-dcb4262507aa`  
**Aplica a:** Tech Lead de cualquier proyecto que use el catálogo SDLC estándar  
**Tarea origen:** MS-047 (Technical Estimates — Memory Service R1)

---

## 1. Propósito

Este SOP documenta exactamente cómo el Tech Lead ejecuta el análisis de estimación técnica (entregable 3B.9) que cierra la Fase 3B (Design Technical) y habilita al PJM a crear las tareas de ejecución en VTT.

El output principal es **3B.9.3_task_breakdown.md** — la tabla maestra que mapea cada deliverable del catálogo estándar contra el proyecto real, con horas, SP, rol y decisión de aplicabilidad.

---

## 2. Cuándo ejecutar este SOP

| Condición | Acción |
|-----------|--------|
| Todos los entregables de Fases 3B.1..3B.8 están en `task_completed` o `task_approved` | ✅ Ejecutar este SOP |
| Algún entregable de 3B está pendiente | ⛔ Esperar — las estimaciones dependen de la arquitectura real |
| Proyecto nuevo sin 3B | ⛔ No ejecutar — no hay base técnica para estimar |

---

## 3. Documentos de entrada obligatorios

Leer en este orden antes de escribir cualquier número:

| # | Documento | Qué extraer |
|---|-----------|-------------|
| 1 | `ANALISIS_FASES_COMPLETO_PARA_PM.md` | Lista completa de deliverables 4.x.x..7.x.x con formato de tabla |
| 2 | `3B.1.4_component_diagram_c4_l3.md` | Componentes reales del sistema (controllers, services, middleware) |
| 3 | `3B.1.5_technology_stack.md` | Stack tecnológico — informa curva de aprendizaje y complejidad |
| 4 | `3B.2.1_folder_structure.md` | Número de archivos a crear — calibra estimaciones BE/FE |
| 5 | `3B.3.1_erd.md` | Número de entidades — calibra estimaciones DB |
| 6 | `3B.4.2_endpoints_list.md` | Endpoints reales con SLAs — informa complejidad BE |
| 7 | `3B.7.1_security_plan.md` | Controles de seguridad — agrega horas a endpoints y deploy |
| 8 | `3B.8.1_infrastructure_plan.md` | Entornos y herramientas — informa estimaciones DO |
| 9 | ADRs relevantes (`3B.6.2_adr_index.md`) | Decisiones que eliminan deliverables (ej: OAuth → ❌) |

**Regla:** No escribir ningún número antes de leer los 9 documentos. Los números sin base técnica generan rework.

---

## 4. Proceso paso a paso

### Paso 1 — Clasificar cada deliverable del catálogo

Para cada deliverable de las Fases 4, 5, 6, 7 del catálogo estándar, determinar:

| Decisión | Símbolo | Criterio |
|----------|---------|----------|
| Aplica en R1 | ✅ | El deliverable es necesario para el alcance del release actual |
| Opcional | ⚪ | Deseable pero no bloqueante para R1; incluir con flag |
| No aplica en R1 | ❌ | El proyecto tomó una decisión técnica que lo excluye explícitamente |

**Reglas de clasificación:**

- Un deliverable marcado ❌ debe tener justificación explícita referenciando un ADR o decisión de arquitectura
- Un deliverable marcado ⚪ debe indicar cuándo se activaría (ej: "R2", "si hay presupuesto")
- Los ❌ NO se omiten de la tabla — se listan con justificación para que el PJM sepa que fue evaluado

### Paso 2 — Estimar horas y SP para los ✅

**Escala de referencia (1 SP ≈ 1h para equipo de agentes IA):**

| Complejidad | SP | Horas | Criterio |
|-------------|-----|-------|----------|
| LOW | 2–3 | 2–3h | Tarea mecánica, sin decisiones de diseño, template aplicable |
| MEDIUM | 5 | 5h | Requiere lectura de contexto + implementación estándar |
| HIGH | 8 | 8h | Múltiples componentes, lógica de negocio no trivial, integración |
| VERY HIGH | 13 | 13h | SLA crítico, múltiples integraciones, riesgo técnico identificado |

**Criterios de complejidad por tipo de deliverable:**

| Tipo | Complejidad base | Factores que la aumentan |
|------|-----------------|--------------------------|
| README / Guías | LOW | — |
| Configuración (linters, .env) | LOW-MEDIUM | Muchos servicios |
| Migración DB simple | MEDIUM | +1 si >10 tablas, +1 si GIN/partial indexes |
| Endpoint REST simple | MEDIUM | +1 si tiene SLA <300ms, +1 si lógica de negocio compleja |
| Endpoint con SLA crítico | HIGH-VERY HIGH | GET /context <500ms = VERY HIGH por Promise.race |
| Service de orquestación | HIGH | Múltiples repos, idempotencia, state machine |
| Test suite completa | HIGH | Integración + performance + E2E combinados |
| CI/CD pipeline | HIGH | 4+ repos, múltiples entornos |
| Security testing | HIGH | OWASP + penetration + vulnerability scan |
| Deploy producción | MEDIUM | Aumenta si hay rollback complejo |

### Paso 3 — Asignar rol responsable

| Rol | Código | Deliverables típicos |
|-----|--------|----------------------|
| Backend Developer | BE | 4.3.x, 4.5.x, 5.5.x |
| Frontend Developer | FE | 4.4.x |
| Database Engineer | DB | 4.2.x |
| DevOps Lead | DO | 4.1.x, 6.1.x, 6.2.x, 6.3.x, 6.5.x |
| QA Engineer | QA | 4.6.x, 5.1.x–5.11.x, 6.4.x |
| Tech Lead | TL | 4.7.x, 4.8.x, reviews, coordinación |

### Paso 4 — Mapear dependencias

Para cada deliverable ✅, identificar su(s) prerequisito(s) en formato `X.Y.Z`:

- Las dependencias son siempre hacia atrás (un deliverable depende de otro anterior)
- Priorizar dependencias de bloqueo total sobre dependencias de contexto
- El diagrama Mermaid en 3B.9.7 muestra el critical path resultante

### Paso 5 — Agregar risk buffers

Identificar los 10–15 riesgos técnicos principales y cuantificar:

```
Horas adicionales = Probabilidad (0.0–1.0) × Impacto (horas)
```

Factores de riesgo comunes:
- SLA crítico no cumplido en staging → prob 0.35–0.45, impacto 12–20h
- Cambio en contrato de integración externa → prob 0.20–0.30, impacto 16–20h
- TypeScript strict + Prisma curva de aprendizaje → prob 0.30–0.40, impacto 6–10h
- CI/CD falla en primer deploy → prob 0.30–0.40, impacto 6–8h
- Tests E2E inestables (flaky) → prob 0.35–0.45, impacto 6–8h

**Fórmula de escenarios:**
```
Base = Σ horas de deliverables ✅
Expected = Base + Σ(prob × impacto)
Best case = Base × 0.80
Worst case = Expected + Σ(impacto máximo de top 5 riesgos)
```

### Paso 6 — Construir capacity plan

Distribuir los deliverables en sprints de 2 semanas:

1. Ordenar por dependencias (los bloqueantes van primero)
2. Asignar respetando paralelismo por rol (BE + DB simultáneos en S1)
3. Verificar que ningún sprint supere 85h sin paralelismo
4. Definir un milestone de GO/NO-GO al final de cada sprint

---

## 5. Estructura de salida (9 archivos)

| Archivo | Contenido | Fuente de datos |
|---------|-----------|-----------------|
| `3B.9.3_task_breakdown.md` | Tabla maestra ~191 filas | Catálogo + decisiones |
| `3B.9.1_estimates_doc.md` | Resumen ejecutivo | Totales de 3B.9.3 |
| `3B.9.2_story_points.md` | SP por módulo y rol | Totales de 3B.9.3 |
| `3B.9.4_effort_matrix.md` | Matriz rol × fase | Agrupación de 3B.9.3 |
| `3B.9.5_complexity_analysis.md` | Top 10 más complejos | 3B.9.3 ordenado por SP desc |
| `3B.9.6_risk_adjusted_estimates.md` | Riesgos + buffers | Análisis propio |
| `3B.9.7_dependencies_map.md` | Critical path + Mermaid | Columna dependencias de 3B.9.3 |
| `3B.9.8_velocity_assumptions.md` | Supuestos del equipo | Caracterización del equipo |
| `3B.9.9_capacity_plan.md` | Sprints + milestones | Ordenación de 3B.9.3 |

**Orden de escritura:** 3B.9.3 primero. Los otros 8 derivan de sus totales.

---

## 6. Checklist de calidad antes de entregar

```
[ ] ¿Leí los 9 documentos de entrada?
[ ] ¿Cada ❌ tiene justificación con referencia a ADR o decisión técnica?
[ ] ¿Los IDs son exactos del catálogo (4.1.1, 4.1.2... no inventados)?
[ ] ¿La suma de horas en 3B.9.4 coincide con el total de 3B.9.1?
[ ] ¿El 3B.9.3 incluye los ❌ (no los omitió)?
[ ] ¿Los riesgos de 3B.9.6 están cuantificados (prob × impacto)?
[ ] ¿El diagrama Mermaid en 3B.9.7 refleja las dependencias de 3B.9.3?
[ ] ¿El capacity plan no tiene sprint que supere 85h sin paralelismo?
[ ] ¿Los 3 escenarios (best/expected/worst) son matemáticamente consistentes?
```

---

## 7. Lecciones aprendidas (MS-047)

| Problema | Causa | Prevención |
|----------|-------|------------|
| v1.0 estimó solo desarrollo (402h) y omitió Testing, Deploy, Ops | No se usó el catálogo estándar como fuente | Siempre partir del catálogo ANALISIS_FASES antes de escribir cualquier número |
| Los ❌ no estaban justificados con ADRs | Se asumió que eran obvios | Cada ❌ requiere cita explícita al ADR o decisión |
| Los números de horas eran inconsistentes entre documentos | Se escribieron en paralelo sin fuente única | 3B.9.3 es la fuente. Los otros 8 derivan de ella, nunca al revés |

---

**Documento:** SOP-EST-01_technical_estimates.md | **Versión:** 1.0 | **Fecha:** 2026-05-12  
**Próxima revisión:** Después de completar Fase 4 (comparar estimado vs real)
