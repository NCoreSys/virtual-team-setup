# LIVING DOCUMENTS — Memory Service R1

**Versión:** 1.0  
**Fecha:** 2026-05-12  
**Autor:** TL Memory Service — `92225290-6b6b-4c1f-a940-dcb4262507aa`  
**Aplica a:** TL, BE, DB, DO — todos los que ejecutan tareas en Fase 4+  
**Propósito:** Definir qué documentos deben mantenerse actualizados durante la ejecución (no son entregables estáticos), quién los actualiza, y cuándo.

---

## 1. Qué es un Living Document en este proyecto

Un Living Document es un documento que:
1. Fue creado en Fase 3B como especificación inicial
2. **Se modifica durante la Fase 4+ cuando la implementación difiere del diseño** o cuando se toman decisiones que extienden/cambian lo especificado
3. Debe estar siempre sincronizado con el estado real del sistema — no con el diseño original

**Problema que resuelve:** "El esquema de BD está documentado... hace tres semanas." El Living Document obliga a que la actualización sea parte del cierre de cada tarea, no una actividad separada que nunca ocurre.

---

## 2. Catálogo de Living Documents — Memory Service R1

### Nivel 1 — Alta frecuencia de cambio (actualizar en cada sprint)

Estos documentos cambian casi garantizado cuando hay tareas de BE o DB activas:

| ID | Archivo | Quién actualiza | Gatillo de actualización |
|----|---------|-----------------|--------------------------|
| LD-01 | `phases/03-design/deliverables/database/3B.3.2_schema_prisma.md` | **DB** al ejecutar migración | Cada vez que se crea o modifica una migración de BD |
| LD-02 | `phases/03-design/deliverables/database/3B.3.1_erd.md` | **DB** al ejecutar migración | Cada vez que se agrega, modifica o elimina una entidad/relación |
| LD-03 | `phases/03-design/deliverables/api-design/3B.4.1_openapi_spec.md` | **BE** al implementar endpoint | Cada vez que se implementa, modifica o elimina un endpoint |
| LD-04 | `phases/03-design/deliverables/api-design/3B.4.2_endpoints_list.md` | **BE** al implementar endpoint | Cada vez que cambia el contrato de un endpoint (parámetros, responses, SLA) |
| LD-05 | `phases/03-design/deliverables/api-design/3B.4.5_error_codes.md` | **BE** al agregar errores | Cada vez que se implementa un nuevo AppError / MEM-ERR-XXX |

### Nivel 2 — Frecuencia media (actualizar cuando la tarea lo toca)

Estos documentos cambian cuando la tarea específicamente modifica algo en esa área:

| ID | Archivo | Quién actualiza | Gatillo de actualización |
|----|---------|-----------------|--------------------------|
| LD-06 | `phases/03-design/deliverables/database/3B.3.4_index_strategy.md` | **DB** | Cuando se agrega o modifica un índice de performance |
| LD-07 | `phases/03-design/deliverables/database/3B.3.5_data_dictionary.md` | **DB** | Cuando se agrega una columna o tabla nueva |
| LD-08 | `phases/03-design/deliverables/api-design/3B.4.3_request_response_examples.md` | **BE** | Cuando un endpoint cambia su estructura de request/response |
| LD-09 | `phases/03-design/deliverables/api-design/3B.4.6_auth_spec.md` | **BE** | Si cambia la estrategia de autenticación (poco probable en R1) |
| LD-10 | `phases/03-design/deliverables/solution-architecture/3B.1.4_component_diagram_c4_l3.md` | **TL** | Cuando se agrega o elimina un componente del sistema |
| LD-11 | `phases/03-design/deliverables/solution-architecture/3B.1.6_integration_points.md` | **TL** | Cuando cambia un contrato de integración externa |
| LD-12 | `phases/03-design/deliverables/infrastructure/3B.8.5_env_matrix.md` | **DO** | Cuando se agrega o modifica una variable de entorno |
| LD-13 | `phases/03-design/deliverables/adrs/3B.6.4_decision_log.md` | **TL** | Cuando se crea un nuevo ADR durante la ejecución |

### Nivel 3 — Baja frecuencia (solo si hay cambio de alcance significativo)

Estos documentos no deberían cambiar en R1 a menos que haya una decisión mayor:

| ID | Archivo | Quién actualiza | Gatillo de actualización |
|----|---------|-----------------|--------------------------|
| LD-14 | `phases/03-design/deliverables/code-architecture/3B.2.1_folder_structure.md` | **TL** | Si se agrega una carpeta nueva al proyecto |
| LD-15 | `phases/03-design/deliverables/infrastructure/3B.8.3_server_specs.md` | **DO** | Si cambia la configuración del servidor |
| LD-16 | `phases/03-design/deliverables/security/3B.7.1_security_plan.md` | **TL** | Si hay un cambio en la postura de seguridad |

---

## 3. Documentos que NO son Living Documents

Estos documentos se crearon en Fase 3B y **no se modifican durante Fase 4+**. Si hay algo nuevo, se crea un documento adicional o se gestiona como Deferred Scope:

| Archivo | Razón de no modificar |
|---------|----------------------|
| `3B.9.3_task_breakdown.md` (estimaciones) | Las estimaciones son históricas — los cambios van en velocity |
| `3B.6.3_adr_documents/ADR-*.md` (ADRs individuales) | Un ADR es inmutable una vez firmado. Si hay cambio → nuevo ADR que lo supersede |
| `3B.5.x_sequence_diagrams.md` | Son artefactos de diseño — los cambios en implementación se documentan en devlogs |
| Wireframes y mockups (`3A.5.x`) | Son artefactos de diseño — no se modifican post-entrega |
| Personas, Site Map, Design System | Documentos estáticos de UX |
| Análisis Fase 2 (SRS, Use Cases, User Stories) | Documentos de análisis — inmutables post-aprobación |

---

## 4. Proceso de actualización: quién hace qué

### 4.1 El agente lo detecta → lo actualiza él mismo

**Cuándo:** La tarea que está ejecutando el agente modifica directamente un Living Document.

Ejemplos:
- DB ejecuta migración → actualiza LD-01 (schema_prisma.md) y LD-02 (erd.md)
- BE implementa endpoint → actualiza LD-03 (openapi_spec.md) y LD-04 (endpoints_list.md)
- BE agrega error code → actualiza LD-05 (error_codes.md)

**Proceso del agente:**
```
1. Implementar el código de la tarea
2. Actualizar el Living Document correspondiente (ver tabla §2)
3. Incluir la actualización en el mismo commit de la tarea
4. Registrar en SKL-REPORT-01 sección "Document Impacts":
   Tipo: modified
   Documento: 3B.3.2_schema_prisma.md
   Cambio: Agregada entidad MemoryEmbedding con campos vector y dimensions
5. El CA de la tarea incluye: "Living Document LD-01 actualizado" (required: true)
```

### 4.2 El TL lo detecta → lo delega o lo hace él

**Cuándo:** El agente completó la tarea pero no actualizó el Living Document, o la actualización es de nivel arquitectónico (LD-10, LD-13, LD-14).

**Proceso del TL:**
```
En SKL-TASK-05 (review), verificar:
- ¿La tarea tocó algún Living Document de Nivel 1 o 2?
- ¿El agente lo actualizó? (ver section "Document Impacts" del reporte)
- Si NO fue actualizado → rechazar tarea con feedback específico:
  "REVIEW-TL: falta actualización de LD-03 (openapi_spec.md) — el endpoint POST /memories 
   fue implementado pero la spec no fue actualizada."
```

### 4.3 Regla de ownership por tipo de tarea

| Tipo de tarea | Living Documents que DEBE actualizar el agente |
|---------------|-----------------------------------------------|
| Tarea DB (4.2.x — migraciones, índices) | LD-01, LD-02, LD-06, LD-07 (según lo que toque) |
| Tarea BE (4.3.x — endpoints, services) | LD-03, LD-04, LD-05, LD-08 (según lo que toque) |
| Tarea DO (4.1.x, 6.x — infra, deploy) | LD-12, LD-15 (según lo que toque) |
| Tarea TL (coordinación, arquitectura) | LD-10, LD-11, LD-13, LD-14 |

---

## 5. Checklist de Living Documents por tarea (para incluir en assignments)

El TL agrega esta sección al ASSIGNMENT según el tipo de tarea:

### Para tareas de DB (4.2.x):
```markdown
## Living Documents a actualizar (obligatorio)

Al completar esta tarea, actualizar los siguientes documentos ANTES de mover a task_in_review:

- [ ] **LD-01** `phases/03-design/deliverables/database/3B.3.2_schema_prisma.md`
      Reflejar los cambios del schema de Prisma aplicados en esta migración.
      
- [ ] **LD-02** `phases/03-design/deliverables/database/3B.3.1_erd.md`
      Agregar/modificar entidades y relaciones según la migración.
      
- [ ] **LD-06** `phases/03-design/deliverables/database/3B.3.4_index_strategy.md` (si aplica)
      Documentar índices nuevos y su justificación de performance.

Incluir en SKL-REPORT-01 sección "Document Impacts" qué cambió en cada documento.
```

### Para tareas de BE (4.3.x):
```markdown
## Living Documents a actualizar (obligatorio)

- [ ] **LD-03** `phases/03-design/deliverables/api-design/3B.4.1_openapi_spec.md`
      Actualizar spec del endpoint implementado (parámetros, responses, ejemplos).
      
- [ ] **LD-04** `phases/03-design/deliverables/api-design/3B.4.2_endpoints_list.md`
      Confirmar o corregir: URL, método, auth, SLA real vs estimado.
      
- [ ] **LD-05** `phases/03-design/deliverables/api-design/3B.4.5_error_codes.md` (si aplica)
      Agregar errores nuevos con su código MEM-ERR-XXX y descripción.

Incluir en SKL-REPORT-01 sección "Document Impacts" qué cambió en cada documento.
```

### Para tareas de DO (4.1.x, 6.x):
```markdown
## Living Documents a actualizar (obligatorio)

- [ ] **LD-12** `phases/03-design/deliverables/infrastructure/3B.8.5_env_matrix.md` (si aplica)
      Documentar variables de entorno nuevas o modificadas por entorno.
      
- [ ] **LD-15** `phases/03-design/deliverables/infrastructure/3B.8.3_server_specs.md` (si aplica)
      Actualizar si hay cambios en la configuración del servidor.

Incluir en SKL-REPORT-01 sección "Document Impacts" qué cambió en cada documento.
```

---

## 6. Integración con el review del TL (SKL-TASK-05)

Se agrega al Paso 3 de SKL-TASK-05 la verificación de Living Documents:

```
PASO 3.5 — Verificar Living Documents

Según el tipo de tarea, verificar que el agente actualizó los Living Documents correspondientes:

1. Leer sección "Document Impacts" del reporte del agente
2. Comparar contra la tabla de §4.3 — ¿actualizó los que debía?
3. Si hay Living Document no actualizado que debía actualizarse:
   → RECHAZAR tarea con feedback: "Falta actualizar LD-XX [nombre del archivo]"
4. Si el agente actualizó correctamente:
   → Incluir en APR-TL: "Living Documents verificados: LD-01 ✅, LD-02 ✅"
```

---

## 7. Cómo registrar el impacto en VTT

Cuando el agente actualiza un Living Document, lo registra en VTT como Document Impact:

```bash
# Registrar que la tarea modificó un documento
POST /api/tasks/{TASK_ID}/impacts
{
  "type": "modified",
  "description": "3B.3.2_schema_prisma.md: agregado modelo MemoryEmbedding con campos vector[] y dimensions. Actualizado para reflejar migración 0003_add_embeddings."
}
```

Y en el devlog si el cambio al documento fue significativo:

```bash
POST /api/tasks/{TASK_ID}/devlog
{
  "category": "decision",
  "title": "Schema Prisma actualizado — entidad MemoryEmbedding",
  "description": "El diseño original en 3B.3.1 contemplaba el vector como campo JSON. Se cambió a vector[] (pgvector) por performance. LD-01 y LD-02 actualizados para reflejar esto."
}
```

---

## 8. Nota sobre el Hardcode Check

El Hardcode Check en VTT actualmente es manual (el agente pega código y ejecuta el análisis). La dirección es automatizarlo para que todo código generado por agentes pase por la revisión automáticamente.

**Estado actual (R1):**
- El agente ejecuta el Hardcode Check manualmente antes de mover a `task_in_review`
- Findings CRITICAL/HIGH deben resolverse o el PM aprueba explícitamente que se dejen (con justificación registrada en devlog)
- Findings MEDIUM/LOW se registran como tech_debt Trackable Items → Deferred Scope R2

**Dirección futura (R2):**
- Integración automática con CI/CD: cada PR pasa por el scanner
- Findings críticos bloquean el merge sin aprobación explícita del PM
- El log de aprobaciones queda en el audit trail de VTT

Para R1, el proceso manual del agente es suficiente y el TL verifica en el review que se ejecutó.

---

**Documento:** LIVING_DOCUMENTS_MEMORY_SERVICE.md | **Versión:** 1.0 | **Fecha:** 2026-05-12  
**Tipo:** Regla permanente — leer en cada apertura de sesión del TL (está en el ASSIGNMENT)  
**Relacionado con:** SOP-TRK-01 (Trackable Items), SOP-TRK-02 (items dinámicos), SKL-TASK-05 (review TL)  
**Ruta canónica:** `00-platform/06.Documentos_soporte/LIVING_DOCUMENTS_MEMORY_SERVICE.md`
