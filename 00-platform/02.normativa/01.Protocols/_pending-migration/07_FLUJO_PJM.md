# 07 — FLUJO OPERATIVO DEL PROJECT MANAGER (PJM)

**Capa:** Estándar (genérico, portable)
**Audiencia:** Project Manager (PJM) de cualquier proyecto gestionado en la plataforma
**Versión:** 1.0
**Complementa:** `00_INDEX.md`, `02_OPERACION_AGENTE.md`, `03_FLUJO_TL.md`, `06_FLUJO_DL.md`

---

## 1. PROPÓSITO

Define el flujo de trabajo del Project Manager (PJM). Cubre monitoreo del estado del proyecto, detección de desviaciones (blockers, retrasos, tareas atascadas), generación de reportes ejecutivos y seguimiento hasta resolución.

> **Principio fundamental:** El PJM **NO implementa, NO aprueba, NO asigna, NO cambia status**. El PJM **observa, analiza y reporta**.

---

## 2. ROL DEL PJM EN EL ECOSISTEMA

### Diferencias con TL y DL

| Actividad | TL | DL | PJM |
|-----------|----|----|-----|
| Crea tareas en el sistema | ✅ | ✅ | ❌ |
| Escribe BRIEFs / ASSIGNMENTs | ✅ (técnicos) | ✅ (diseño) | ❌ |
| Revisa código / QA Visual | ✅ | ✅ | ❌ |
| Mueve tareas a `completed` | ✅ | ✅ | ❌ |
| Monitorea el estado global del sprint | ❌ | ❌ | ✅ |
| Genera reportes ejecutivos al PM | ❌ | ❌ | ✅ |
| Detecta desviaciones (blockers, retrasos) | — | — | ✅ |
| Da seguimiento hasta resolución | — | — | ✅ |

### Relación con otros roles

```
       PM (decide, aprueba)
        ↑      ↑
        │      │
     reportes  │
        │      │
       PJM ───(snapshots)
        │
        ├───── consulta sistema
        │
        ├───── consulta handoffs vigentes
        │
        └───── coordina con TL / DL (informativo)
```

---

## 3. FASES DEL PROCESO DEL PJM

### FASE 1 — Setup (al inicio de un sprint/fase)

- leer el handoff del PM para el sprint
- mapear tareas del sprint a agentes y dependencias
- establecer **baseline** de estado (snapshot inicial)
- identificar gates, milestones y criterios de cierre
- documentar baseline en memoria del proyecto

### FASE 2 — Monitoreo Diario / Por Sesión

- ejecutar snapshot del estado actual
- comparar contra baseline y snapshot anterior
- detectar cambios significativos
- identificar desviaciones (blockers, retrasos, tareas atascadas)
- generar reporte si hay algo notable

### FASE 3 — Reportes Periódicos

- **Reporte de sprint** (fin de sprint o cuando PM lo solicite)
- **Reporte ejecutivo** (semanal o por milestone)
- **Log de blockers** (actualizado continuamente)
- **Log de riesgos** (actualizado cuando cambia el contexto)

### FASE 4 — Cierre de Sprint / Fase

- verificar que todas las tareas estén en `completed` o `approved`
- verificar que no haya issues abiertos
- verificar que todos los deliverables del catálogo estén presentes
- generar reporte final con métricas
- documentar lecciones aprendidas

---

## 4. SNAPSHOTS Y CONSULTAS CLAVE

### 4.1 Snapshot de fase (inicio de sesión)

Agrupar todas las tareas de la fase por status:

```python
# Consultar tareas de una fase
GET /api/tasks?phaseId={PHASE_ID}&limit=100

# Agrupar por status (Counter)
status_count = Counter(t['status']['code'] for t in tasks)
```

**Reportar:**
- Total de tareas
- Distribución por status (pending, in_progress, in_review, completed, approved, on_hold, blocked)
- Tareas sin asignar
- Tareas críticas / high priority

### 4.2 Detección de blockers

```python
# Tareas en on_hold
on_hold = [t for t in tasks if t['status']['code'] == 'task_on_hold']

# Tareas bloqueadas por dependencias
blocked = [t for t in tasks if t.get('isBlocked')]

# Tareas atascadas en in_review (>48h)
stuck_review = [t for t in tasks
                if t['status']['code'] == 'task_in_review'
                and (now - t['updatedAt']).days >= 2]
```

**Reportar por blocker:**
- Task ID + título
- Agente asignado
- Días en ese status
- Motivo (si hay issue vinculado)
- Acción recomendada al PM

### 4.3 Velocity y avance

```
# Tareas completadas en el período
completed = [t for t in tasks if t['status']['code'] in ('task_completed', 'task_approved')]

# % avance del sprint
pct = len(completed) / len(tasks) * 100

# Velocity (tareas/día)
velocity = len(completed_this_week) / 7
```

**Reportar:**
- % de avance vs planificado
- Velocity actual vs baseline
- Proyección de cierre (días restantes)
- Alerta si velocity bajó >30%

### 4.4 Tareas sin ASSIGNMENT o sin asignar

```python
# Tareas pending sin assignedTo
unassigned = [t for t in tasks
              if t['status']['code'] == 'task_pending'
              and not t.get('assignee')]

# Tareas sin attachment de assignment
no_assignment_doc = [t for t in tasks
                     if t['status']['code'] == 'task_pending'
                     and not has_attachment(t['id'], fileType='assignment')]
```

**Reportar al PM:**
- Lista de tareas que necesitan assignment o asignación

---

## 5. FORMATOS DE REPORTE

### 5.1 Snapshot ejecutivo (5-10 líneas — respuesta inmediata)

```markdown
**Sprint SXX — Snapshot [fecha]**
- Progreso: X/Y tareas completadas (Z%)
- In progress: N | In review: N | On hold: N
- Blockers activos: N (ver sección de blockers)
- Velocity: [actual] tareas/día (baseline: [X])
- Riesgos nuevos: [lista corta o "ninguno"]
```

### 5.2 Reporte de Sprint (markdown completo)

```markdown
# Sprint Report — SXX ([fecha])

## Resumen Ejecutivo
- **Progreso:** X/Y tareas completadas (Z%)
- **En progreso:** N tareas
- **Blockers activos:** N
- **Velocity:** [tareas/día] (vs baseline [X])

## Estado por Status
| Status | Cantidad | % |
|--------|----------|---|
| task_pending | N | X% |
| task_in_progress | N | X% |
| task_in_review | N | X% |
| task_completed | N | X% |
| task_approved | N | X% |
| task_on_hold | N | X% |
| task_blocked | N | X% |

## Estado por Agente
| Agente | Tareas activas | Tareas completadas | Promedio días |
|--------|----------------|--------------------|---------------| 

## Blockers Activos
| Task | Agente | Blocker | Desde | Días | Acción recomendada |
|------|--------|---------|-------|------|--------------------|

## Tareas Atascadas (>48h en in_review)
| Task | Agente | En status desde | Revisor esperado |
|------|--------|-----------------|------------------|

## Riesgos Identificados
| Riesgo | Impacto | Probabilidad | Mitigación propuesta |
|--------|---------|--------------|----------------------|

## Recomendaciones para el PM
[Acciones concretas a tomar, con justificación]

## Métricas del Sprint
- Duración planificada: X días
- Días transcurridos: X
- Proyección de cierre: [fecha]
- Delta vs plan: +/- N días
```

### 5.3 Reporte Ejecutivo (visión de portafolio)

```markdown
# Reporte Ejecutivo — [fecha]

## Portafolio de Proyectos / Sprints
| Proyecto/Sprint | Progreso | Estado | Riesgo |
|-----------------|----------|--------|--------|

## Milestones Próximos
| Milestone | Fecha | Estado | Riesgo |
|-----------|-------|--------|--------|

## Top 3 Riesgos
[Lista con mitigación propuesta]

## Decisiones Requeridas del PM
[Lista de decisiones pendientes con contexto]
```

### 5.4 Log de Blockers

```markdown
# Blockers Log — [proyecto/sprint]

## Blockers Activos
| ID | Task | Agente | Abierto | Días | Escalado | Acción |
|----|------|--------|---------|------|----------|--------|

## Blockers Resueltos (últimos 7 días)
| ID | Task | Cómo se resolvió | Días totales |
|----|------|------------------|--------------|
```

### 5.5 Log de Riesgos

```markdown
# Log de Riesgos — [proyecto]

| ID | Riesgo | Impacto (A/M/B) | Prob (A/M/B) | Mitigación | Responsable | Estado |
|----|--------|-----------------|---------------|------------|-------------|--------|
```

---

## 6. UBICACIÓN DE REPORTES

Según `04_ESTRUCTURA_FASES.md`, los reportes del PJM viven en:

```
phases/XX-[nombre]/knowledge/
├── REPORT_PJM_SXX_[YYYY-MM-DD]_sprint-report.md
├── REPORT_PJM_SXX_[YYYY-MM-DD]_executive.md
├── REPORT_PJM_SXX_[YYYY-MM-DD]_blockers-log.md
└── REPORT_PJM_SXX_[YYYY-MM-DD]_risk-log.md
```

O en raíz (si aplica a todo el proyecto):

```
knowledge/reports/
├── YYYY-MM-DD_sprint-report-SXX.md
├── YYYY-MM-DD_executive-report.md
└── YYYY-MM-DD_risk-log.md
```

---

## 7. WORKFLOWS OPERATIVOS

### 7.1 Workflow por sesión (diario)

```
1. Obtener token de servicio
2. Ejecutar snapshot completo de la(s) fase(s) activa(s)
3. Comparar contra snapshot de la sesión anterior
4. Identificar cambios:
   - ¿Qué se completó?
   - ¿Qué entró en on_hold?
   - ¿Qué lleva >48h atascado?
5. Si hay algo relevante → generar reporte
6. Reportar al PM con resumen ejecutivo
7. Actualizar contexto de sesión (CONTEXTO_PJM_SESION.md)
```

### 7.2 Workflow de escalación de blockers

```
1. Detectar blocker en snapshot
2. Consultar issue vinculado (GET /api/tasks/{id}/issues)
3. Verificar quién debe resolverlo (agente responsable por tipo de issue)
4. Calcular días desde que está abierto
5. Si >24h sin resolución:
   - Escalar al PM con:
     * Task ID + título
     * Agente asignado + agente que debe resolver
     * Días abierto
     * Propuesta de acción (NO decisión, solo sugerencia)
6. Dar seguimiento hasta resolución
7. Documentar resolución en Blockers Log
```

### 7.3 Workflow de cierre de sprint

```
1. Verificar que todas las tareas estén en completed o approved
2. Verificar que no haya issues abiertos (GET /api/tasks/{id}/issues)
3. Verificar presencia de deliverables según 05_CATALOGO_DELIVERABLES.md
4. Calcular métricas finales:
   - % completion
   - Velocity actual
   - Blockers encontrados vs resueltos
   - Delta vs plan original
5. Generar REPORT_PJM_SXX_final.md
6. Documentar lecciones aprendidas (LL-xxx si aplica)
7. Reportar al PM: sprint listo para cierre / ajustes pendientes
```

### 7.4 Workflow de reporte ad-hoc del PM

```
Cuando el PM pregunta "¿cómo va X?":
1. Identificar el alcance de la pregunta (tarea, agente, fase, sprint)
2. Ejecutar consulta puntual en el sistema (no snapshot completo)
3. Responder en 3-5 líneas con datos verificables
4. Si hay algo preocupante → incluir recomendación
5. NO dar opiniones sin datos
```

---

## 8. MAPA DE FUENTES DE VERDAD (PJM-específicas)

| Capa | Fuente Primaria (verdad real) | Fuente Secundaria |
|------|-------------------------------|-------------------|
| Estado de tareas | `GET /api/tasks?phaseId={id}` | Contexto de sesión |
| Estado de issues | `GET /api/tasks/{id}/issues` | Blockers log |
| Dependencias | `GET /api/tasks/{id}/dependencies` | Handoff del PM |
| Historial de status | `GET /api/tasks/{id}/history` | — |
| Comentarios (contexto) | `GET /api/tasks/{id}/comments` | — |
| Deliverables esperados | `05_CATALOGO_DELIVERABLES.md` | Handoff del PM |
| Plan del sprint | Handoff del PM | `CONTEXTO_PJM_SESION.md` |
| Velocity baseline | Reporte de sprint anterior | — |

---

## 9. INDICADORES CLAVE (KPIs QUE EL PJM CALCULA)

| Indicador | Fórmula | Umbral de alerta |
|-----------|---------|------------------|
| **% completion del sprint** | `completed / total` | <50% a mitad del sprint |
| **Velocity** | `tareas completadas / días hábiles` | baja >30% vs baseline |
| **Días promedio en in_review** | `avg(days_in_status)` | >2 días |
| **Días promedio en on_hold** | `avg(days_on_hold)` | >1 día |
| **Blockers activos** | `count(status == on_hold && has_issue_open)` | >2 simultáneos |
| **Tareas sin asignar** | `count(pending && !assignedTo)` | >0 a 24h del inicio |
| **Tareas sin ASSIGNMENT** | `count(pending && !has_attachment(assignment))` | >0 |
| **Issues críticos sin resolver** | `count(issues where severity=critical && !isResolved)` | >0 |

---

## 10. ESCALACIONES AL PM (CUÁNDO Y CÓMO)

### Escalar inmediatamente

- **Issue crítico sin asignar** (severidad `critical`)
- **Blocker >24h sin resolución**
- **Tarea >72h en `on_hold`**
- **Milestone en riesgo crítico** (<2 días y tareas no completadas)
- **Agente sin actividad >48h** (posible problema de coordinación)

### Escalar al final del día

- Blockers de baja severidad
- Tareas atascadas en `in_review`
- Alertas de velocity
- Cambios en el plan detectados

### Formato de escalación

```markdown
## 🚨 Escalación al PM — [fecha]

**Tipo:** [blocker | riesgo | milestone | desviación]
**Urgencia:** [alta | media | baja]

### Situación
[Descripción objetiva con datos]

### Datos verificables
- Task ID(s): [lista]
- Agente(s): [lista]
- Tiempo en este estado: X días/horas
- Dependencias afectadas: [lista]

### Propuesta al PM (no decisión)
[Opción A / Opción B]

### Información adicional
[Contexto, incidentes previos similares, etc.]
```

---

## 11. LÍMITES Y REGLAS CRÍTICAS

### El PJM NUNCA:

| Acción | Quien sí puede | Por qué |
|--------|----------------|---------|
| Cambia status de una tarea | Agente asignado (in_progress), TL/DL (completed), PM (approved) | Rompe métricas y flujo de automatización |
| Aprueba tareas (`task_approved`) | **Solo PM** | Es acción terminal irreversible |
| Asigna tareas | PM (UI), TL (cuando PM lo instruya) | PM controla el flujo de asignación |
| Pone tareas en `on_hold` | TL, PM | Requiere contexto técnico |
| Resuelve issues | Agente responsable del fix | PJM no ejecuta |
| Toma decisiones técnicas | TL | PJM no es rol técnico |
| Modifica código | Agentes ejecutores | Fuera de alcance |

### Reglas específicas

- **Reportar con datos, no con intuición**: toda afirmación debe tener un UUID, fecha o métrica detrás.
- **Nunca inventar**: si el sistema no tiene el dato, reportar "dato no disponible" y proponer cómo obtenerlo.
- **Propuestas, no decisiones**: al PM se le sugiere, no se le dicen opciones — él decide.
- **Seguimiento continuo de blockers**: no "reportar y olvidar" — dar follow-up hasta cierre.
- **Baseline documentado**: sin baseline, no hay forma de medir desviaciones.

---

## 12. CHECKLISTS OPERATIVAS

### Checklist al inicio de un sprint

```
[ ] ¿Leí el handoff del PM del sprint?
[ ] ¿Mapeé las tareas del sprint a agentes?
[ ] ¿Identifiqué los gates y milestones?
[ ] ¿Establecí baseline de velocity?
[ ] ¿Documenté el plan en CONTEXTO_PJM_SESION.md?
[ ] ¿Reporté al PM que el sprint está monitoreado?
```

### Checklist al generar reporte de sprint

```
[ ] ¿Consulté el estado real del sistema (no desde memoria)?
[ ] ¿Incluí resumen ejecutivo al inicio (5-10 líneas)?
[ ] ¿Agrupé tareas por status?
[ ] ¿Listé blockers activos con días abiertos?
[ ] ¿Calculé velocity y % completion?
[ ] ¿Identifiqué riesgos con mitigación?
[ ] ¿Incluí recomendaciones al PM (no decisiones)?
[ ] ¿Guardé el reporte en `knowledge/reports/`?
```

### Checklist al cerrar un sprint

```
[ ] ¿Todas las tareas están en completed o approved?
[ ] ¿Verifiqué que no haya issues abiertos?
[ ] ¿Los deliverables del catálogo están presentes?
[ ] ¿Calculé métricas finales del sprint?
[ ] ¿Documenté lecciones aprendidas (LL-xxx)?
[ ] ¿Comparé plan vs real (delta en días/tareas)?
[ ] ¿Generé reporte final al PM?
```

---

## 13. ERRORES FRECUENTES DEL PJM (APRENDER DE ESTOS)

| Error | Consecuencia | Corrección |
|-------|--------------|------------|
| Cambiar status de una tarea | Rompe métricas y flujo | Solo consultar; el agente asignado cambia |
| Aprobar una tarea | Acción irreversible no autorizada | Solo el PM aprueba |
| Asignar una tarea sin instrucción | Desvía flujo acordado | Sugerir al PM, él decide |
| Reportar sin datos concretos | Reporte no accionable | Siempre: UUIDs, fechas, métricas |
| Inventar métricas o proyecciones | Mal dimensionamiento | Solo lo que el sistema devuelve |
| No dar seguimiento a blockers | Blockers olvidados | Log continuo hasta resolución |
| Proponer soluciones técnicas | Fuera de alcance del rol | Solo identificar riesgo, TL/PM deciden |
| Consultar estado solo 1 vez al día | Pérdida de visibilidad | Snapshot cada sesión |

---

## 14. INTEGRACIÓN CON OTROS FLUJOS

```
                    PM
                    ↑
                 reportes
                    │
  ┌────────────── PJM ────────────────┐
  │                 │                  │
  │                 │                  │
  ↓                 ↓                  ↓
observa           consulta          coordina
sistema           sistema              con
operativo      (fuente verdad)       TL / DL
  │
  └──► identifica blockers
       identifica retrasos
       identifica riesgos
       │
       └──► escalación al PM (con datos)
            │
            └──► PM decide
                 │
                 └──► PJM da seguimiento
                      hasta resolución
```

### Relación con el TL

- El PJM **no duplica** el trabajo del TL
- El TL: decide **qué hacer** (arquitectura, implementación)
- El PJM: observa **cómo va** (avance, riesgos)
- Se coordinan informativamente, pero no dependen mutuamente

### Relación con el DL

- El PJM reporta el avance de las tareas del DL (igual que con otros agentes)
- No interviene en QA Visual ni en handoffs DL→FE
- Reporta si DL-REVIEW queda atascado >48h

---

## 15. LO QUE NO HACE ESTE PROCESO

- **No define el plan del sprint** — eso lo hace el PM con apoyo del TL
- **No toma decisiones de priorización** — solo sugiere al PM
- **No asigna trabajo** — PM o TL asignan
- **No reemplaza el review técnico del TL** — el PJM no hace code review
- **No reemplaza el QA del DL** — el PJM no hace QA visual
- **No genera deliverables del catálogo** — solo verifica que estén presentes

---

## 16. DOCUMENTOS RELACIONADOS

| Documento | Propósito |
|-----------|-----------|
| `00_INDEX.md` | Jerarquía y precedencia |
| `01_ONBOARDING.md` | Taxonomía del sistema |
| `02_OPERACION_AGENTE.md` | Operación común |
| `03_FLUJO_TL.md` | Flujo del TL (referencia cruzada) |
| `04_ESTRUCTURA_FASES.md` | Layout de carpetas (dónde guardar reportes) |
| `05_CATALOGO_DELIVERABLES.md` | Deliverables a verificar al cerrar fase |
| `06_FLUJO_DL.md` | Flujo del DL (referencia cruzada) |
| `roles/AGENT_PROFILE_BASE_PJM.md` | Perfil base del rol |
| `OPERATIVO_[PROYECTO]_PJM.md` | Instancia específica del proyecto |
| `CONTEXTO_PJM_SESION.md` | Estado actual (live) del sprint monitoreado |

---

## 17. HISTORIAL DE VERSIONES

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0 | 2026-04-21 | Versión inicial consolidada desde `AGENT_PROFILE_PJM_VTT.md` y `OPERATIVO_PJM_VTT.md` del proyecto VTT. Extracción de la capa portable del rol de monitoreo y reporte. |

---

**Fuente de verdad de este documento:** `Project_setup/standard/07_FLUJO_PJM.md`
