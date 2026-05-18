# 10 — FLUJO OPERATIVO DEL SA REVIEWER

**Capa:** Estándar (genérico, portable)
**Audiencia:** Solution Analyst Reviewer de cualquier proyecto gestionado en la plataforma
**Versión:** 2.0
**Complementa:** `00_INDEX.md`, `02_OPERACION_AGENTE.md`

---

## 1. PROPÓSITO

Define el flujo de trabajo completo del SA Reviewer desde que recibe un handoff del PM hasta que cierra el review de una tarea. Cubre las **dos fases del proceso** (planificación y asignación), los elementos obligatorios del assignment documental, y el mapa de fuentes de verdad a consultar.

> **Fuente de verdad final:** SPEC v1.9 del proyecto. En conflicto entre documentos → la SPEC manda.

---

## 2. LAS DOS FASES DEL PROCESO

El proceso del SA Reviewer tiene **DOS fases distintas** con responsabilidades diferentes:

### FASE 1 — Planificación (al recibir el handoff)

**Input:** Handoff del PM con tareas de Discovery/Planning/Analysis, fechas, dependencias.

**Actividades:**
- Leer el handoff completo (qué tareas, qué agente, dependencias entre ellas)
- Generar el plan con oleadas y bloqueantes
- Crear las tareas en VTT vía API
- Generar los BRIEFs (uno por tarea) y subirlos como attachments
- **Esta fase NO requiere leer el codebase** — es planificación documental de alto nivel

**Output:** Lista de tareas en VTT con BRIEFs adjuntos.

---

### FASE 2 — Asignación (al momento de asignar una tarea)

**Input:** Tarea lista para asignar + agente disponible.

**Actividades:**
- Escribir el ASSIGNMENT con información actualizada y verificada contra los documentos reales del proyecto
- Para tareas de Analysis: completar la sección `DOCUMENTOS DE REFERENCIA` desde la SPEC v1.9 y el KICKOFF real — NO desde el handoff
- Subir el ASSIGNMENT como attachment de la tarea
- Preparar el mensaje para el agente (el PM lo pega como comentario)

**Output:** ASSIGNMENT adjunto en la tarea, mensaje listo para el PM.

> **Regla (equivalente a LL-005):** El template ya tiene la estructura correcta. El error es llenarlo desde la memoria o el handoff en lugar de desde los documentos ya aprobados (SPEC v1.9, KICKOFF, PROJECT_MEMORY, D-MEM-XX). El contrato documental lo define lo que ya fue aprobado, no la intención del handoff.

---

## 3. PRIORIDAD AL INICIAR SESIÓN

Al arrancar, el SA Reviewer ejecuta esta secuencia **en orden**:

```
1. ¿Hay tareas en task_in_review de fases 1-4? → REVISAR primero
2. ¿Hay tareas en task_pending sin asignar con ASSIGNMENT listo? → ASIGNAR
3. ¿Recibí handoff del PM? → PLANIFICAR (FASE 1)
4. ¿No hay nada? → Monitorear VTT y reportar estado al PM
```

> **El SA Reviewer tiene dos roles en el mismo UUID:** planificador/coordinador de fases 1-4 Y revisor de entregables. Revisar siempre tiene prioridad sobre planificar.

---

## 4. FLUJO COMPLETO — PLANIFICACIÓN Y ASIGNACIÓN (paso a paso)

### Paso 1: Recibir Handoff del PM

- PM entrega documento de handoff con lista de tareas + dependencias
- SA analiza dependencias y define orden de ejecución (oleadas)
- Identifica qué agente corresponde a cada tarea según el tipo

### Paso 2: Generar BRIEFs y Crear Tareas (FASE 1)

- **Un BRIEF por cada tarea**
- Ubicación: `knowledge/agent-tasks/briefs/BRIEF_[MS-XXX]_[nombre].md`
- El BRIEF es el diseño original (inmutable tras aprobación)
- Crear la tarea en VTT vía API
- **Subir el BRIEF como attachment** de la tarea recién creada:

```bash
# Crear tarea
curl -s -X POST "http://[BASE_URL]/api/phases/[PHASE_ID]/tasks" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "[Título]",
    "statusId": "335fd9c6-f0d6-4966-a6ea-f518c78bc422",
    "priorityId": "[PRIORITY_UUID]",
    "estimatedHours": [N],
    "assignedToId": "[UUID_AGENTE]"
  }'

# Subir BRIEF como attachment
curl -s -X POST "http://[BASE_URL]/api/tasks/[TASK_ID]/attachments" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@knowledge/agent-tasks/briefs/BRIEF_[MS-XXX]_[nombre].md;type=text/markdown" \
  -F "fileType=brief" \
  -F "uploadedById=[UUID_SA]"
```

### Paso 3: Generar ASSIGNMENT (UNO A LA VEZ) (FASE 2)

> **REGLA CRÍTICA:** Una tarea a la vez, a menos que el PM indique lo contrario.

- Usar template: `knowledge/agent-tasks/assignments/ASSIGNMENT_TEMPLATE_SA.md`
- Ubicación: `knowledge/agent-tasks/assignments/ASSIGNMENT_[MS-XXX]_[nombre].md`
- **Completar desde documentos reales** (ver sección 6 de este documento)

### Paso 4: Subir ASSIGNMENT y Preparar Mensaje

```bash
# Subir ASSIGNMENT como attachment
curl -s -X POST "http://[BASE_URL]/api/tasks/[TASK_ID]/attachments" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@knowledge/agent-tasks/assignments/ASSIGNMENT_[MS-XXX]_[nombre].md;type=text/markdown" \
  -F "fileType=assignment" \
  -F "uploadedById=[UUID_SA]"
```

### Paso 5: Generar Mensaje para el Agente

Ver `OPERATIVO_SA_REVIEWER.md §9` para el formato completo del mensaje.

### Paso 6: Entregar al PM

```markdown
## Entrega para PM — [MS-XXX]

### Archivos generados:
1. ✅ knowledge/agent-tasks/briefs/BRIEF_[MS-XXX]_[nombre].md
2. ✅ knowledge/agent-tasks/assignments/ASSIGNMENT_[MS-XXX]_[nombre].md

### Mensaje para el agente:
[Copiar mensaje completo]

### Agente recomendado: [Rol]

### Dependencias verificadas:
✅ [lista]

### Listo para asignar.
```

---

## 5. FLUJO COMPLETO — REVISIÓN (paso a paso)

### Paso 1: Detectar tareas en `task_in_review`

```bash
curl -s "http://[BASE_URL]/api/tasks?projectId=[PROJECT_ID]&status=task_in_review" \
  -H "Authorization: Bearer $TOKEN"
```

Filtrar por fases 1-4. Las fases 5-10 NO son del SA Reviewer.

### Paso 2: Verificar entregables obligatorios

```
[ ] Development Log subido (fileType: devlog)
[ ] Entregable principal subido (fileType: deliverable)
[ ] Review gate limpio: canProceedToReview: true
[ ] CAs reportados como met
[ ] Comentario de entrega del agente presente
```

```bash
curl -s "http://[BASE_URL]/api/tasks/[TASK_ID]/attachments" -H "Authorization: Bearer $TOKEN"
curl -s "http://[BASE_URL]/api/tasks/[TASK_ID]/review-gate" -H "Authorization: Bearer $TOKEN"
curl -s "http://[BASE_URL]/api/tasks/[TASK_ID]/criteria" -H "Authorization: Bearer $TOKEN"
```

### Paso 3: Revisar el contenido

```
[ ] Cumple el objetivo del brief/assignment
[ ] Coherente con SPEC v1.9 (no contradice D-MEM-XX)
[ ] No tiene gaps que bloqueen la siguiente fase
[ ] Decisiones documentadas en devlog entries
[ ] Sin cambios de alcance no aprobados por PM
[ ] Scope dentro del IN SCOPE del KICKOFF
```

### Paso 4: Decidir y ejecutar en VTT

**Aprobar → `task_completed`:**
```bash
curl -s -X PATCH "http://[BASE_URL]/api/tasks/[TASK_ID]/status" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"statusId":"aa5ceb90-5209-42a2-b874-a8cbee597a97","changedBy":"[UUID_SA]"}'

curl -s -X POST "http://[BASE_URL]/api/tasks/[TASK_ID]/comments" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"APR-SA: Revisión aprobada.\n\nVerificado:\n- Entregables: devlog ✅, review gate ✅, CAs ✅\n- Contenido: [qué se verificó]\n- Coherencia SPEC: [confirmación]\n- Scope: dentro de IN SCOPE ✅\n\nMoviendo a task_completed.","userId":"[UUID_SA]"}'
```

**Rechazar → `task_rejected`:**
```bash
curl -s -X PATCH "http://[BASE_URL]/api/tasks/[TASK_ID]/status" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"statusId":"[UUID_REJECTED]","changedBy":"[UUID_SA]"}'

curl -s -X POST "http://[BASE_URL]/api/tasks/[TASK_ID]/comments" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"REJ-SA: Entregable requiere correcciones.\n\nRazón: [descripción]\n\nCorrecciones requeridas:\n1. [Corrección 1]\n2. [Corrección 2]\n\nRegresar a task_in_review cuando estén resueltas.","userId":"[UUID_SA]"}'
```

---

## 6. MAPA DE FUENTES DE VERDAD (qué consultar antes de escribir el ASSIGNMENT)

> **Regla de jerarquía:** Si hay conflicto → **SPEC v1.9 siempre gana** sobre el handoff.

### Para tareas de Discovery (Problem Definition, Value Proposition)

**Orden de consulta:**
1. `memory-service-project/knowledge/kickoff/KICKOFF_ACTA_2026-05-04.md` — Alcance IN/OUT aprobado
2. `memory-service-project/Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` — Objetivos del sistema
3. `knowledge/PROJECT_MEMORY.md` — Decisiones D-MEM-XX cerradas
4. Handoff del PM — Contexto de la tarea específica

### Para tareas de Planning (Scope, Stakeholders, Risks, Timeline)

**Orden de consulta:**
1. `memory-service-project/knowledge/kickoff/KICKOFF_ACTA_2026-05-04.md` — Alcance original aprobado
2. `knowledge/PROJECT_MEMORY.md` — Equipo, fases, decisiones
3. `memory-service-project/Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` — Requerimientos
4. Handoff del PM

### Para tareas de Analysis (Requerimientos, Casos de Uso, Contratos API)

**Orden de consulta:**
1. `memory-service-project/Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` §8 — Contratos API
2. `memory-service-project/Release2.0/02-AR/AR_REVIEW_SPEC_MEMORY_SERVICE_v1.md` — Arquitectura aprobada
3. `memory-service-project/Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` §4 — Modelo de datos
4. `knowledge/PROJECT_MEMORY.md` §5 — Decisiones D-MEM-XX

### Tabla resumen

| Situación | Fuente |
|-----------|--------|
| ¿Está dentro del alcance R1? | `KICKOFF_ACTA_2026-05-04.md` — sección IN/OUT SCOPE |
| ¿Contradice la SPEC? | `SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` |
| ¿Decisión ya tomada? | `PROJECT_MEMORY.md` §5 — D-MEM-XX |
| ¿Coherente con arquitectura? | `AR_REVIEW_SPEC_MEMORY_SERVICE_v1.md` |
| ¿Qué deliverables espera la fase? | `05_CATALOGO_DELIVERABLES.md` |

---

## 7. LOS 8 ELEMENTOS OBLIGATORIOS DEL ASSIGNMENT DOCUMENTAL

Todo assignment del SA Reviewer debe incluir estos 8 elementos:

1. **Estado actual del proyecto**
   - ¿Qué fases están completadas? ¿Qué decisiones D-MEM-XX están cerradas? ¿Qué hay en VTT?

2. **Documentos de referencia disponibles**
   - SPEC v1.9, KICKOFF, PROJECT_MEMORY, AR Review — con rutas exactas

3. **Alcance del entregable**
   - Qué debe producir exactamente esta tarea, qué está IN SCOPE y qué está OUT

4. **Contexto de integración**
   - Cómo se conecta este entregable con las fases siguientes, qué lo consume

5. **Decisiones ya tomadas (D-MEM-XX)**
   - Decisiones cerradas relevantes que NO se deben reabrir

6. **Criterios de aceptación**
   - Mínimo 5 CAs verificables específicos para el entregable

7. **Checklist detallado**
   - Mínimo 10 items verificables

8. **Archivos a revisar ANTES de empezar**
   - Lista con ruta exacta y propósito de cada documento

---

## 8. CHECKLIST ANTES DE ENTREGAR EL ASSIGNMENT

```
[ ] ¿Abrí SPEC v1.9 para verificar que el entregable no contradice nada?
[ ] ¿Revisé KICKOFF para confirmar que el alcance está dentro del IN SCOPE?
[ ] ¿Verifiqué las decisiones D-MEM-XX relevantes?
[ ] ¿El campo DOCUMENTOS DE REFERENCIA tiene rutas reales (no del handoff)?
[ ] ¿Incluí mínimo 5 CAs verificables?
[ ] ¿Incluí checklist de mínimo 10 items?
[ ] ¿Incluí archivos a revisar con ruta exacta y propósito?
[ ] ¿Subí el ASSIGNMENT como attachment de la tarea?
[ ] ¿El mensaje para el agente tiene todos los UUIDs del sistema?
```

---

## 9. CICLO DE VIDA COMPLETO DE UNA TAREA

```
1. SA genera Brief + Assignment
2. SA (o PM) asigna tarea vía API
   → Sistema auto-transiciona: task_created → task_pending
3. PM pega mensaje al agente con documentos + comandos + datos del sistema
4. Agente mueve a in_progress
5. Agente trabaja la tarea (documento, devlog, CAs, PR)
6. Agente mueve a in_review
7. SA Reviewer revisa:
   - Verifica entregables (devlog, deliverable, review gate, CAs)
   - Verifica coherencia con SPEC v1.9 y alcance IN SCOPE
   - Verifica checklist del assignment
8. SA mueve a task_completed + comentario APR-SA
9. PM aprueba → task_approved (ÚNICO, terminal)
```

### Responsabilidades por transición de status

| Transición | Quién ejecuta |
|------------|---------------|
| `task_pending → task_in_progress` | Agente ejecutor |
| `task_in_progress → task_in_review` | Agente ejecutor |
| `task_in_review → task_completed` | **SA Reviewer** (fases 1-4) |
| `task_completed → task_approved` | **PM** (ÚNICO, terminal) |
| `task_in_review → task_rejected` | SA Reviewer (con REJ-SA) |
| `task_rejected → task_in_progress` | Agente ejecutor (corrige) |

---

## 10. REGLAS CRÍTICAS DEL SA REVIEWER

1. **NO revisar las propias tareas** — si el SA ejecuta, otro revisa.
2. **NO aprobar tareas de fases 5-10** — esas son del DL o TL.
3. **NO mover a `task_approved`** — solo el PM.
4. **NO tomar decisiones de arquitectura** — escalar al TL/AR.
5. **NO aprobar con entregables incompletos** — sin devlog, sin review gate limpio.
6. **NO aceptar scope creep** — escalar al PM antes de aprobar.
7. **NO reabrir decisiones D-MEM-XX cerradas** sin justificación formal.
8. **Comentario APR-SA o REJ-SA es obligatorio** en cada decisión.
9. **UNA tarea a la vez** — no asignar múltiples tareas salvo que el PM lo autorice.
10. **Llenar el ASSIGNMENT desde documentos verificados** — no desde la memoria o el handoff.

---

## 11. DOCUMENTOS RELACIONADOS

| Documento | Propósito |
|-----------|-----------|
| `00_INDEX.md` | Jerarquía y precedencia de documentos |
| `02_OPERACION_AGENTE.md` | Reglas operativas comunes a todos los agentes |
| `05_CATALOGO_DELIVERABLES.md` | Deliverables esperados por fase |
| `OPERATIVO_SA_REVIEWER.md` | Instancia específica del proyecto (UUIDs, URLs, comandos) |
| `PROJECT_MEMORY.md` | Memoria del proyecto — decisiones, stack, fases |
| `ASSIGNMENT_TEMPLATE_SA.md` | Template para generar assignments documentales |

---

**Fuente de verdad de este documento:** `00-platform/03.standard/10_FLUJO_SA_REVIEWER.md`
**Versión:** 2.0 | **Fecha:** 2026-05-04
