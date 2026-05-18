# PROTOCOLO DE EJECUCIÓN Y REGISTRO PARA AGENTES VTT

| Campo | Valor |
|-------|-------|
| **Documento** | PROTOCOLO_EJECUCION_REGISTRO_AGENTES_VTT.md |
| **Versión** | 1.0 |
| **Fecha** | 2026-04-04 |
| **Autor** | PM (Martin Rivas) |
| **Aplica a** | Todos los agentes (SA, AR, TL, DB, BE, FE, QA, DL) |
| **Estado** | ✅ OBLIGATORIO |

---

## 1. OBJETIVO

Establecer el proceso **OBLIGATORIO** que todo agente debe seguir para registrar en BD:
- Criterios cumplidos/no cumplidos
- Bugs, blockers, gaps detectados
- Observaciones y decisiones
- Acciones requeridas para otros roles
- Evidencias de trabajo

**REGLA FUNDAMENTAL:**
```
╔═══════════════════════════════════════════════════════════════════════════╗
║ Una tarea NO puede marcarse como task_in_review o task_completed          ║
║ si no tiene TODOS los registros obligatorios en BD.                       ║
║                                                                           ║
║ El mensaje de entrega en chat NO sustituye el registro en BD.            ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

---

## 2. FLUJO DE EJECUCIÓN CON REGISTRO

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    FLUJO DE EJECUCIÓN DE TAREA                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. RECIBIR TAREA                                                       │
│     └── Verificar criterios asignados: GET /tasks/:id/criteria          │
│                                                                         │
│  2. EJECUTAR TRABAJO                                                    │
│     └── Durante ejecución, registrar en BD:                             │
│         ├── Decisiones tomadas → POST /tasks/:id/devlog-entries         │
│         ├── Issues encontrados → POST /tasks/:id/devlog-entries         │
│         ├── Gaps detectados → POST /tasks/:id/devlog-entries            │
│         └── Blockers → POST /tasks/:id/devlog-entries                   │
│                                                                         │
│  3. COMPLETAR TRABAJO                                                   │
│     └── Registrar en BD:                                                │
│         ├── Fulfillment por criterio → POST /tasks/:id/criteria/:id/fulfill
│         ├── Evidencias → POST /trackable-items/:id/evidences            │
│         └── Document impacts → POST /tasks/:id/document-impacts         │
│                                                                         │
│  4. AUTO-VERIFICAR                                                      │
│     └── Consultar: GET /tasks/:id/completion-check                      │
│         ├── ¿Todos los criterios tienen fulfillment? ✅/❌              │
│         ├── ¿Hay devlog entries critical/high sin resolver? ✅/❌       │
│         ├── ¿Document impacts completados? ✅/❌                        │
│         └── canComplete: true/false                                     │
│                                                                         │
│  5. ENTREGAR                                                            │
│     └── Solo si canComplete = true:                                     │
│         PATCH /tasks/:id { status: 'task_in_review' }                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. MAPEO: MENSAJE DE ENTREGA → REGISTRO EN BD

### 3.1 Criterios Cubiertos

**Antes (solo mensaje):**
```
Criterios cubiertos:
* ✅ CA-01: Tab General (campos, inmutabilidad código+tipo, save)
* ✅ CA-02: Tab Fases (drag, add/edit/delete, restricción tareas activas)
```

**Ahora (registro obligatorio en BD):**
```bash
# Por cada criterio cumplido
POST /api/tasks/{taskId}/criteria/{criteriaId}/fulfill
{
  "status": "met",
  "evidence": "Tab General implementado con campos nombre, descripción. Código y tipo son readonly. Botón save funcional."
}
```

---

### 3.2 Bugs Encontrados

**Antes (solo mensaje):**
```
Bugs encontrados:
* BUG-SRC-01: rutas POST/GET/DELETE /sources sin auth
* BUG-SRC-02: las sources se comparten por projectId
```

**Ahora (registro obligatorio en BD):**
```bash
POST /api/tasks/{taskId}/devlog-entries
{
  "entries": [
    {
      "categoryCode": "issue",
      "severity": "critical",
      "title": "BUG-SRC-01: Rutas /sources sin autenticación",
      "description": "Las rutas POST/GET/DELETE /sources no tienen middleware de auth. Cualquier usuario puede manipular sources.",
      "status": "pending"
    },
    {
      "categoryCode": "issue",
      "severity": "high",
      "title": "BUG-SRC-02: Sources compartidas por projectId",
      "description": "Las sources se filtran por projectId, no por documentId. Un documento vacío ve fuentes de otros documentos del mismo proyecto.",
      "status": "pending"
    }
  ]
}
```

---

### 3.3 Blockers

**Antes (solo mensaje):**
```
BLOCKED: BE-IMP-01, BE-IMP-04
BLOCKER-IMP-02: no existen TaskDocumentImpact reales
```

**Ahora (registro obligatorio en BD):**
```bash
POST /api/tasks/{taskId}/devlog-entries
{
  "entries": [
    {
      "categoryCode": "blocker",
      "severity": "critical",
      "title": "BLOCKER-IMP-02: No existen TaskDocumentImpact en producción",
      "description": "Muestreo de 120 tareas del proyecto VTT devolvió 0 impacts. No se pueden ejecutar escenarios BE-IMP-01 y BE-IMP-04.",
      "status": "pending"
    }
  ]
}
```

---

### 3.4 Observaciones

**Antes (solo mensaje):**
```
Observaciones clave:
* OBS-S10-01: Devlog usa /devlog (single entry), no /devlog-entries (batch)
* OBS-S10-02: Reports usan /phases/ no /sprints/
```

**Ahora (registro obligatorio en BD):**
```bash
POST /api/tasks/{taskId}/devlog-entries
{
  "entries": [
    {
      "categoryCode": "issue",
      "severity": "medium",
      "title": "OBS-S10-01: Endpoint devlog inconsistente con spec",
      "description": "Implementación usa /devlog (single entry). Spec dice /devlog-entries (batch). Actualizar spec o código.",
      "status": "pending"
    },
    {
      "categoryCode": "issue",
      "severity": "medium",
      "title": "OBS-S10-02: Reports usan /phases/ en lugar de /sprints/",
      "description": "Los endpoints de reports están bajo /phases/ pero spec indica /sprints/. Verificar cuál es correcto.",
      "status": "pending"
    }
  ]
}
```

---

### 3.5 Acciones Requeridas para Otros

**Antes (solo mensaje):**
```
Acción requerida (Admin VM — NO ejecutar SQL directo):
docker exec vtt-backend npx prisma migrate resolve --applied 20260315000001
```

**Ahora (registro obligatorio en BD):**
```bash
POST /api/tasks/{taskId}/devlog-entries
{
  "entries": [
    {
      "categoryCode": "dependency",
      "severity": "high",
      "title": "Acción requerida: Admin debe ejecutar migrate resolve",
      "description": "Admin VM debe ejecutar: docker exec vtt-backend npx prisma migrate resolve --applied 20260315000001_s09_traceability_catalogs. NO ejecutar SQL directo.",
      "status": "pending"
    }
  ]
}
```

---

### 3.6 Decisiones Tomadas

**Antes (solo mensaje):**
```
Se decidió usar /devlog en lugar de /devlog-entries por simplicidad
```

**Ahora (registro obligatorio en BD):**
```bash
POST /api/tasks/{taskId}/devlog-entries
{
  "entries": [
    {
      "categoryCode": "decision",
      "severity": "medium",
      "title": "Decisión: Usar /devlog en lugar de /devlog-entries",
      "description": "Se decidió implementar endpoint /devlog (single entry) en lugar de /devlog-entries (batch) por simplicidad en el MVP. Batch se puede agregar después.",
      "status": "acknowledged"
    }
  ]
}
```

---

### 3.7 Gaps/Deuda Técnica

**Antes (solo mensaje):**
```
Nota: Falta implementar validación de zona horaria en TimeService
```

**Ahora (registro obligatorio en BD):**
```bash
POST /api/tasks/{taskId}/devlog-entries
{
  "entries": [
    {
      "categoryCode": "tech_debt",
      "severity": "medium",
      "title": "GAP: Falta validación de zona horaria",
      "description": "TimeService no considera zona horaria del proyecto. Puede causar inconsistencias en cálculo overnight para proyectos multi-región.",
      "status": "pending"
    }
  ]
}
```

---

## 4. CATEGORÍAS Y SEVERIDADES

### 4.1 Categorías (devlog_category_catalog)

| categoryCode | Cuándo usar | Ejemplo |
|--------------|-------------|---------|
| `issue` | Bug o problema encontrado | BUG-SRC-01, OBS-S10-01 |
| `blocker` | Impide continuar trabajo | BLOCKER-IMP-02 |
| `tech_debt` | Deuda técnica identificada | Refactorizar TimeService |
| `decision` | Decisión técnica tomada | Usar /devlog vs /devlog-entries |
| `dependency` | Acción requerida de otro rol | Admin debe ejecutar migrate |
| `risk` | Riesgo identificado | Puede fallar en multi-región |
| `testing_note` | Nota de QA | Escenario no ejecutable |
| `improvement` | Mejora sugerida | Agregar batch endpoint |

### 4.2 Severidades

| severity | Cuándo usar | Bloquea cierre? |
|----------|-------------|-----------------|
| `critical` | Impide funcionamiento básico | ✅ SÍ |
| `high` | Afecta funcionalidad importante | ✅ SÍ |
| `medium` | Funciona pero con limitaciones | ❌ NO |
| `low` | Mejora menor / cosmético | ❌ NO |

### 4.3 Estados de Entry

| status | Significado | Quién cambia |
|--------|-------------|--------------|
| `pending` | Recién registrado | Agente |
| `acknowledged` | TL/PM vio el entry | TL |
| `in_progress` | Se está resolviendo | TL |
| `resolved` | Resuelto | TL |
| `deferred` | Diferido a otro sprint | TL |
| `wont_fix` | No se va a resolver | TL |

---

## 5. CHECKLIST OBLIGATORIO ANTES DE ENTREGAR

### 5.1 Para TODO agente

```
ANTES DE MARCAR task_in_review:

[ ] 1. CRITERIOS
    [ ] GET /tasks/:id/criteria → verificar criterios asignados
    [ ] Por cada criterio: POST fulfill con status y evidence
    [ ] Todos los criterios tienen fulfillment registrado

[ ] 2. DEVLOG ENTRIES
    [ ] Issues encontrados registrados (categoryCode: issue)
    [ ] Blockers registrados (categoryCode: blocker)
    [ ] Decisiones registradas (categoryCode: decision)
    [ ] Dependencias registradas (categoryCode: dependency)
    [ ] Tech debt registrada (categoryCode: tech_debt)

[ ] 3. DOCUMENT IMPACTS
    [ ] Si la tarea afecta documentos → registrar impacts
    [ ] Si se actualizó documento → completar impact

[ ] 4. EVIDENCIAS
    [ ] Links a PRs, commits, archivos subidos
    [ ] Screenshots si aplica

[ ] 5. AUTO-CHECK
    [ ] GET /tasks/:id/completion-check → canComplete: true
```

### 5.2 Para QA específicamente

```
CHECKLIST ADICIONAL QA:

[ ] Test cases ejecutados registrados como fulfillments
[ ] PASS/FAIL por escenario con evidence
[ ] Bugs encontrados como devlog entries (issue)
[ ] Blockers como devlog entries (blocker)
[ ] Observaciones como devlog entries (issue, severity: medium)
```

### 5.3 Para DB específicamente

```
CHECKLIST ADICIONAL DB:

[ ] Migración aplicada → evidence con hash de commit
[ ] Acciones para Admin → devlog entry (dependency)
[ ] Cambios de schema → document impact en SCHEMA_REF
```

---

## 6. GATE DE REVISIÓN AUTOMÁTICO

### 6.1 Qué valida el sistema

Antes de permitir `task_in_review`:

| Validación | Condición | Bloquea? |
|------------|-----------|----------|
| Criterios | Todos tienen fulfillment | ✅ SÍ |
| Critical entries | Ninguno con status=pending | ✅ SÍ |
| High entries | Ninguno con status=pending | ✅ SÍ |
| Document impacts | Todos completed (si hay) | ⚠️ Warning |

### 6.2 Qué valida el TL antes de aprobar

| Validación | Acción TL |
|------------|-----------|
| Entries critical/high | Resolver, diferir, o wont_fix |
| Evidencias suficientes | Verificar links/screenshots |
| Fulfillments correctos | Validar que evidence corresponde |

---

## 7. EJEMPLO COMPLETO: ENTREGA DE TAREA QA

### 7.1 Mensaje Actual (incompleto)

```
Entrega VTT-367 - QA Sources/Impacts S10

Document Sources:
* 7/11 PASS
* FAIL: BE-SRC-05, BE-SRC-07, BE-SRC-08, BE-SRC-11
* Bugs encontrados:
  * BUG-SRC-01: rutas sin auth
  * BUG-SRC-02: sources compartidas

Estado: task_on_hold por blocker
```

### 7.2 Registro Correcto en BD

**Paso 1: Registrar fulfillments por criterio**

```bash
# Criterios PASS
POST /api/tasks/VTT-367/criteria/BE-SRC-01/fulfill
{ "status": "met", "evidence": "Auth verificada, retorna 401 sin token" }

POST /api/tasks/VTT-367/criteria/BE-SRC-02/fulfill
{ "status": "met", "evidence": "CRUD completo funcional" }

# ... repetir para BE-SRC-03, 04, 06, 09, 10

# Criterios FAIL
POST /api/tasks/VTT-367/criteria/BE-SRC-05/fulfill
{ "status": "not_met", "evidence": "Falla por BUG-SRC-01, sin auth" }

POST /api/tasks/VTT-367/criteria/BE-SRC-07/fulfill
{ "status": "not_met", "evidence": "Falla por BUG-SRC-02, sources compartidas" }
```

**Paso 2: Registrar bugs como devlog entries**

```bash
POST /api/tasks/VTT-367/devlog-entries
{
  "entries": [
    {
      "categoryCode": "issue",
      "severity": "critical",
      "title": "BUG-SRC-01: Rutas /sources sin autenticación",
      "description": "POST/GET/DELETE /api/project-documents/:id/sources no tienen middleware authenticateOptional. Cualquier request sin token pasa.",
      "status": "pending"
    },
    {
      "categoryCode": "issue",
      "severity": "high",
      "title": "BUG-SRC-02: Sources compartidas por projectId",
      "description": "ProjectDocumentSource filtra por projectId, no por documentId. GET /documents/123/sources retorna sources de documento 456 si ambos son del mismo proyecto.",
      "status": "pending"
    },
    {
      "categoryCode": "blocker",
      "severity": "critical",
      "title": "BLOCKER-IMP-02: No existen TaskDocumentImpact en producción",
      "description": "Query de 120 tareas en proyecto VTT retorna 0 impacts. Escenarios BE-IMP-01 y BE-IMP-04 no ejecutables.",
      "status": "pending"
    }
  ]
}
```

**Paso 3: Verificar estado**

```bash
GET /api/tasks/VTT-367/completion-check

Response:
{
  "canComplete": false,
  "blockers": [
    { "type": "devlog_entry", "severity": "critical", "count": 2 },
    { "type": "criteria_not_met", "count": 4 }
  ],
  "warnings": [],
  "summary": {
    "criteriaTotal": 18,
    "criteriaMet": 10,
    "criteriaNotMet": 4,
    "criteriaPartial": 0,
    "criteriaPending": 4
  }
}
```

**Paso 4: Marcar estado correcto**

```bash
# Como hay blockers, la tarea debe quedar on_hold
PATCH /api/tasks/VTT-367
{ "status": "task_on_hold" }
```

**Paso 5: Mensaje de entrega (ahora es resumen, no la fuente)**

```
Entrega VTT-367 - QA Sources/Impacts S10

Registros en BD:
* Fulfillments: 10 met, 4 not_met, 4 pending
* Devlog entries: 2 issues critical, 1 blocker critical
* Ver detalles: GET /tasks/VTT-367/devlog-entries

Estado: task_on_hold (canComplete: false por blockers)

Acción requerida: BE debe resolver BUG-SRC-01 y BUG-SRC-02
```

---

## 8. ENDPOINTS DE VERIFICACIÓN

### 8.1 Ver estado de completitud

```bash
GET /api/tasks/:id/completion-check
```

### 8.2 Ver criterios y fulfillments

```bash
GET /api/tasks/:id/criteria?include=fulfillments
```

### 8.3 Ver devlog entries

```bash
GET /api/tasks/:id/devlog-entries
```

### 8.4 Ver gate del sprint

```bash
GET /api/sprints/:id/devlog-review
```

---

## 9. CONSECUENCIAS DE NO SEGUIR EL PROTOCOLO

| Situación | Consecuencia |
|-----------|--------------|
| Entregar sin registrar fulfillments | TL rechaza, regresa a development |
| No registrar bugs encontrados | Se detectan en integración, retrabajo |
| No registrar blockers | Sprint no puede avanzar, se pierde tiempo |
| No registrar decisiones | Se olvidan, inconsistencias futuras |
| Marcar task_in_review con pending criticals | Sistema bloquea (si gate implementado) |

---

## 10. IMPLEMENTACIÓN DEL GATE AUTOMÁTICO

### 10.1 Endpoint Propuesto

```typescript
// TaskService.canTransitionToReview(taskId)
async canTransitionToReview(taskId: string): Promise<CompletionCheck> {
  const criteria = await this.getCriteriaWithFulfillments(taskId);
  const devlogEntries = await this.getDevlogEntries(taskId);
  const documentImpacts = await this.getDocumentImpacts(taskId);
  
  const criticalPending = devlogEntries.filter(
    e => e.severity === 'critical' && e.status === 'pending'
  );
  const highPending = devlogEntries.filter(
    e => e.severity === 'high' && e.status === 'pending'
  );
  const criteriaWithoutFulfillment = criteria.filter(
    c => !c.fulfillment
  );
  
  return {
    canComplete: criticalPending.length === 0 
                 && highPending.length === 0 
                 && criteriaWithoutFulfillment.length === 0,
    blockers: [
      ...criticalPending.map(e => ({ type: 'devlog_critical', entry: e })),
      ...highPending.map(e => ({ type: 'devlog_high', entry: e })),
      ...criteriaWithoutFulfillment.map(c => ({ type: 'criteria_missing', criteria: c }))
    ],
    // ...
  };
}
```

### 10.2 Integración con Transición de Estado

```typescript
// TaskService.updateStatus(taskId, newStatus)
async updateStatus(taskId: string, newStatus: string) {
  if (newStatus === 'task_in_review') {
    const check = await this.canTransitionToReview(taskId);
    if (!check.canComplete) {
      throw new HttpException({
        message: 'Cannot transition to review',
        blockers: check.blockers
      }, 422);
    }
  }
  // ... continuar con update
}
```

---

## 11. FIRMA

| Rol | Firma | Fecha |
|-----|-------|-------|
| PM | ✅ Aprobado y OBLIGATORIO | 2026-04-04 |

---

**Documento:** PROTOCOLO_EJECUCION_REGISTRO_AGENTES_VTT.md  
**Versión:** 1.0  
**Estado:** ✅ OBLIGATORIO PARA TODOS LOS AGENTES  
**Fecha:** 2026-04-04

---

**PM — Martin Rivas**  
CEO/Founder — Virtual Teams Tracking
