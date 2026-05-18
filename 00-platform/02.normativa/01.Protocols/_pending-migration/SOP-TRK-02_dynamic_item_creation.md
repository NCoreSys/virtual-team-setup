# SOP-TRK-02 — Creación Dinámica de Trackable Items durante la Ejecución

**Versión:** 1.0  
**Fecha:** 2026-05-12  
**Autor:** TL Memory Service — `92225290-6b6b-4c1f-a940-dcb4262507aa`  
**Aplica a:** TL (decisor), Agentes BE/DO/DB/QA (detectores), PM (gatillo externo)  
**Propósito:** Definir el proceso para crear y gestionar Trackable Items que emergen DURANTE la ejecución del proyecto — no en el análisis inicial — distinguiendo entre los que requieren retroactividad y los que solo aplican hacia adelante.

---

## 1. El problema que resuelve este SOP

El análisis inicial (Fases 0–3B) capturó ~210 Trackable Items. Pero durante la Fase 4 (Development) aparecen nuevas necesidades:

- El agente BE detecta que un endpoint necesita un comportamiento de caché no documentado → sugiere un NFR nuevo
- El PM decide que se necesita una funcionalidad adicional no contemplada en R1 → nuevo RF
- El agente DO encuentra que la configuración de Docker necesita una decisión formal → nuevo ADR
- El QA detecta que una regla de negocio no está documentada pero está siendo implementada → BR no registrado

Estos items tienen naturalezas distintas y requieren tratamiento diferente.

---

## 2. Clasificación: dos tipos de items dinámicos

### Tipo A — Items con retroactividad (requieren revisión del pasado)

**Cuándo aplica:** El item describe algo que potencialmente YA fue implementado (o debería haber sido implementado) en tareas anteriores.

**Tipos de Trackable Item que normalmente caen aquí:**
- `rf` — Requerimiento Funcional nuevo o gap detectado
- `rnf` — No funcional nuevo (SLA, seguridad, disponibilidad)
- `business_rule` — Regla que ya opera en el sistema pero no estaba registrada
- `use_case` — Flujo de usuario no documentado pero ya implementado

**Preguntas de retroactividad:**
1. ¿Ya hay tareas `task_approved` que implementan esto sin saberlo?
2. ¿Hay tareas en curso que deberían incorporar este requisito?
3. ¿El item ya existe en VTT con otro nombre/código? (verificar primero)

**Proceso:** Ver §4.

---

### Tipo B — Items solo hacia adelante (sin retroactividad)

**Cuándo aplica:** El item es una directriz, decisión o criterio que aplica a partir de ahora. Lo pasado, pasado está.

**Tipos de Trackable Item que normalmente caen aquí:**
- `adr` — Decisión arquitectónica tomada durante la ejecución
- `assumption` — Supuesto que se formalizó durante el desarrollo
- `constraint` — Restricción identificada durante la ejecución
- `tech_debt` — Deuda técnica identificada (se trackea para R2, no retroactiva)
- Acceptance Criteria — Solo aplican a tareas futuras o en curso, no a tareas ya aprobadas

**Proceso:** Ver §5.

---

## 3. Dos gatillos: quién inicia la creación

### Gatillo 1 — El PM o usuario externo detecta la necesidad

El PM o un stakeholder decide en cualquier momento que se necesita agregar, modificar o eliminar un requerimiento.

**Flujo:**

```
PM / Usuario detecta necesidad de nuevo item
        │
        ▼
PM agrega el item en VTT (o le pide al TL que lo haga)
  POST /api/projects/{project_id}/trackable-items
        │
        ▼
VTT crea notificación / PM comenta en tarea activa o en canal del TL:
  "NUEVO-TI: Se agregó [código] [título]. Revisar aplicabilidad y cobertura."
        │
        ▼
TL recibe el aviso → ejecuta proceso según Tipo A o Tipo B (§4 o §5)
```

**Template de mensaje del PM al TL:**

```
NUEVO-TI: [código] — [título]
Tipo: rf | rnf | adr | business_rule | ...
Descripción: [breve descripción]
Motivo: [por qué se agrega ahora]
Acción requerida del TL: revisar retroactividad y linkear a tareas
```

---

### Gatillo 2 — El agente detecta algo durante la ejecución

El agente, en su formato de entrega (comentario de `task_in_review`), señala que identificó algo que debería trackearse. Esto está dentro del formato estándar de SKL-REPORT-01.

**Sección específica en el reporte de entrega del agente:**

```markdown
### Items detectados para trackeo (TL revisar):

| Tipo sugerido | Código sugerido | Descripción | Urgencia |
|--------------|-----------------|-------------|----------|
| rnf | NFR-PERF-07 | El batch de embeddings tarda >2s cuando son >50 items simultáneos. Sugerencia: agregar NFR de límite de batch. | Alta |
| adr | ADR-SA-007 | Se usó Promise.allSettled() en vez de Promise.all() para el vector search — decisión que afecta el comportamiento bajo fallo parcial. | Media |
| business_rule | BR-024 | El sistema silencia errores de embedding y retorna memoria sin vector cuando falla el servicio externo. Esta regla no estaba documentada. | Alta |
```

**El TL, al revisar la tarea (SKL-TASK-05), tiene un paso adicional:**

```
Paso 5.5 — Procesar items detectados por el agente:
  → Leer sección "Items detectados para trackeo" del reporte del agente
  → Para cada item: clasificar como Tipo A o Tipo B
  → Ejecutar proceso correspondiente (§4 o §5)
  → Registrar decisión en comentario APR-TL:
    "Items detectados procesados: ADR-SA-007 creado, BR-024 creado y linkeado retroactivamente a MS-052 y MS-054, NFR-PERF-07 pendiente de decisión del PM."
```

---

## 4. Proceso para Tipo A — Con retroactividad

```
1. VERIFICAR: ¿ya existe en VTT?
   GET /api/projects/{project_id}/trackable-items?limit=200
   → Buscar por título o descripción similar
   → Si ya existe con otro código → NO crear duplicado, usar el existente
   → Si no existe → continuar

2. CREAR el item en VTT
   POST /api/projects/{project_id}/trackable-items
   {"code": "RF-033", "title": "...", "description": "...", "priority": "high", "typeCode": "rf"}

3. REVISAR tareas ya aprobadas (retroactividad)
   → Consultar tareas en task_approved del proyecto
   GET /api/tasks?projectId={id}&status=task_approved
   → Para cada tarea aprobada: ¿esta tarea implementó este nuevo item?
   → Si SÍ: linkear retroactivamente
     POST /api/trackable-items/{item_id}/tasks {"taskId": "MS-052"}
   → Si NO: continuar

4. REVISAR tareas en curso (task_in_progress, task_in_review)
   → Para cada tarea en curso: ¿debería cubrir este item?
   → Si SÍ: notificar al agente responsable + agregar CA a esa tarea
     POST /api/tasks/{task_id}/criteria {"title": "...", "required": true}

5. REVISAR tareas futuras (task_pending, task_assigned)
   → Para tareas aún no iniciadas: ¿cuáles deberían implementar este item?
   → El TL lo incorpora en el ASSIGNMENT de esas tareas cuando las asigne
   → Agregar nota en el item: "Pendiente de linkear a MS-060, MS-065"

6. DETERMINAR si el item queda:
   a. Completamente cubierto por tareas ya aprobadas → ti_approved
   b. Parcialmente cubierto → linkear las que lo cubren + tareas pendientes lo completan
   c. No cubierto aún → crear tarea nueva si es necesario (notificar al PM)

7. REGISTRAR decisión
   Comentario en la tarea que disparó el item (o en el sprint):
   "RF-033 creado. Retroactividad: ya cubierto por MS-052 (POST /memories) y MS-054 (Services).
    Linkeado. Estado: ti_approved."
```

### 4.1 Escenario concreto: RF nuevo detectado por agente

El agente BE en MS-060 (implementando GET /memories/search) detecta que no hay RF que describa la búsqueda semántica por texto libre — solo hay RF para búsqueda por agentId.

```
TL recibe en APR-TL el item detectado:
  Tipo sugerido: rf
  Descripción: "Búsqueda semántica de memorias por texto libre"
  Urgencia: Alta (ya se está implementando)

TL ejecuta Tipo A:
  1. Busca en VTT → RF-001..032 — ninguno cubre búsqueda semántica → no hay duplicado
  2. Crea RF-033: "El sistema permite buscar memorias por similitud semántica de texto"
  3. Revisa tareas aprobadas: MS-054 (Services) tenía lógica de vector search → linkea RF-033 a MS-054
  4. Tarea en curso MS-060 → agrega CA: "La búsqueda retorna top-K resultados ordenados por score"
  5. Tareas futuras MS-070 (Search UI) → incorporar RF-033 en su assignment
  6. Item queda: parcialmente cubierto (MS-054 linkeado, MS-060 en curso, MS-070 pendiente)
```

---

## 5. Proceso para Tipo B — Solo hacia adelante

```
1. VERIFICAR: ¿ya existe en VTT?
   → Misma verificación que Tipo A para evitar duplicados

2. CREAR el item en VTT
   POST /api/projects/{project_id}/trackable-items
   {"code": "ADR-SA-007", "title": "...", "description": "...", "priority": "medium", "typeCode": "adr"}

3. NO revisar tareas pasadas
   → Lo que se hizo antes fue sin esta directriz → no se penaliza retroactivamente
   → Excepción: si el ADR CONTRADICE algo ya implementado → crear devlog entry risk en las tareas afectadas

4. LINKEAR a tareas en curso y futuras que apliquen
   → Tareas en in_progress: notificar al agente que este ADR existe y debe considerarlo
   → Tareas en pending: incorporar en el ASSIGNMENT

5. REGISTRAR fecha de vigencia en la descripción del item
   "Vigente desde 2026-05-12 (sprint S02). No aplica retroactivamente a tareas anteriores a esta fecha."

6. Para tech_debt: marcar como Deferred Scope hacia R2
   POST /api/trackable-items/{item_id}/defer
   {"targetType": "release", "targetReleaseId": "...", "reason": "Identificado en S02. Plan R2."}
```

### 5.1 Escenario concreto: ADR técnico detectado por agente

El agente BE detecta que usó Promise.allSettled() para el vector search y esta decisión afecta cómo el sistema se comporta bajo fallo parcial.

```
TL recibe el item detectado:
  Tipo sugerido: adr
  Descripción: "Promise.allSettled() en vector search para tolerancia a fallos parciales"
  Urgencia: Media

TL ejecuta Tipo B:
  1. Busca en VTT → ADR-SA-001..006 — ninguno cubre esto
  2. Crea ADR-SA-007: "Usar Promise.allSettled() para operaciones de vector search"
     Descripción incluye: "Vigente desde 2026-05-12 (MS-060). No aplica retroactivamente."
  3. NO revisa tareas aprobadas (el código ya está ahí, ese ADR describe lo que se hizo)
  4. Linkea ADR-SA-007 a MS-060 (la tarea donde se tomó la decisión)
  5. Para tareas futuras que implementen vector operations → TL lo incluye en sus assignments
```

---

## 6. Tabla de decisión rápida para el TL

| Item detectado | Tipo | ¿Retroactividad? | ¿Crear tarea nueva? | Urgencia típica |
|----------------|------|-----------------|--------------------|-----------------| 
| RF nuevo no contemplado | A | ✅ Sí | Solo si no hay tarea que lo cubra | Alta |
| NFR nuevo (SLA, límite) | A | ✅ Sí — verificar si ya se cumple | Solo si no hay tarea de testing | Alta |
| BR no documentada pero implementada | A | ✅ Sí — linkear a donde se implementó | No — ya existe | Media |
| UC no documentado | A | ✅ Sí | Depende del alcance | Media |
| ADR técnico (decisión ya tomada) | B | ❌ No | No | Media |
| ADR de proceso | B | ❌ No | No | Baja |
| Assumption nueva | B | ❌ No | No | Baja |
| Constraint identificado | B | ❌ No | No | Media |
| Tech debt | B | ❌ No — aplaza a R2 | Crear como deferred scope | Baja |
| CA adicional para tareas futuras | B | ❌ No | No | Alta (si es seguridad) |

---

## 7. Integración con el formato de entrega del agente (SKL-REPORT-01)

El formato estándar de entrega del agente DEBE incluir la sección de items detectados. Se agrega al template:

```markdown
## Entrega: $TASK_ID — $TASK_NAME

### Código:
[...]

### Development Log:
[...]

### Items detectados para trackeo (TL revisar):
<!-- Si no hay items, escribir: "Sin items detectados." -->

| Tipo sugerido | Código sugerido | Descripción | Retroactividad | Urgencia |
|--------------|-----------------|-------------|----------------|----------|
| rnf | NFR-PERF-07 | Batch >50 embeddings tarda >2s | Sí — verificar tareas de performance | Alta |
| adr | ADR-SA-007 | Promise.allSettled() en vector search | No — decisión tomada ahora | Media |
| business_rule | BR-024 | Sistema silencia errores de embedding | Sí — verificar MS-052, MS-054 | Alta |

<!-- Clasificar cada uno como Tipo A (retroactividad) o Tipo B (solo hacia adelante) -->
<!-- El TL decide si crear, si ya existe, y cómo proceder -->

### Commit SHA:
[...]
```

---

## 8. Integración con SKL-TASK-05 (review del TL)

Se agrega el Paso 5.5 al flujo de review del TL:

```
PASO 5.5 — Procesar items detectados por el agente

1. Leer sección "Items detectados para trackeo" del comentario de entrega
2. Para cada item:
   a. Buscar en VTT si ya existe → GET /api/projects/{id}/trackable-items
   b. Clasificar: ¿Tipo A (retroactividad) o Tipo B (solo adelante)?
   c. Ejecutar proceso §4 o §5 según corresponda
   d. Registrar decisión: creado / ya existe con código X / rechazado (motivo)

3. Incluir resultado en el comentario APR-TL:
   "Items detectados procesados:
    - ADR-SA-007: CREADO. No retroactivo. Linkeado a MS-060.
    - BR-024: CREADO. Retroactivo: linkeado a MS-052 y MS-054. Estado: ti_approved.
    - NFR-PERF-07: PENDIENTE decisión PM — requiere nueva tarea de load testing."

4. Si hay items que requieren acción del PM → notificar al PM con formato NUEVO-TI
```

---

## 9. Límites del proceso: qué NO hace este SOP

- ❌ No aplica retroactividad a CAs ya cerrados — un CA `met` en una tarea `task_approved` no se reabre
- ❌ No genera tareas nuevas automáticamente — el TL evalúa si se necesita tarea y lo propone al PM
- ❌ No cambia el estado de tareas ya aprobadas — solo agrega links retroactivos
- ❌ No resuelve gaps que requieren código nuevo sin coordinación del PM — eso es scope change

---

## 10. Referencia de API calls para este proceso

```python
# 1. Verificar si item ya existe
GET /api/projects/{PROJECT_ID}/trackable-items?limit=200
# → Filtrar por title/code manualmente

# 2. Crear item nuevo
POST /api/projects/{PROJECT_ID}/trackable-items
{"code": "RF-033", "title": "...", "description": "...", "priority": "high", "typeCode": "rf"}

# 3. Linkear a tarea (retroactiva o futura)
POST /api/trackable-items/{item_id}/tasks
{"taskId": "MS-052"}

# 4. Agregar CA a tarea en curso
POST /api/tasks/{task_id}/criteria
{"title": "...", "description": "...", "type": "functional", "required": true}

# 5. Deferir item (tech_debt a R2)
POST /api/trackable-items/{item_id}/defer
{"targetType": "release", "targetReleaseId": "92664a70-...", "reason": "[Deferred to R2] ...", "deferredBy": "92225290-..."}

# 6. Cerrar item si ya está completamente cubierto
PATCH /api/trackable-items/{item_id}
{"statusCode": "ti_approved"}
```

---

**Documento:** SOP-TRK-02_dynamic_item_creation.md | **Versión:** 1.0 | **Fecha:** 2026-05-12  
**Relacionado con:** SOP-TRK-01 (flujo base), SKL-TASK-05 (review TL), SKL-REPORT-01 (formato entrega agente)  
**Complementa:** MANUAL_FEATURES_VTT_V4.md §8 (Trackable Items), §1 (Acceptance Criteria)
