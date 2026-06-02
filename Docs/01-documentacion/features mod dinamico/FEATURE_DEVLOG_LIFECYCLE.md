# FEATURE: DEVLOG ENTRY LIFECYCLE

| Campo | Valor |
|-------|-------|
| **Feature** | Devlog Entry Lifecycle |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-21 |
| **Sprint origen** | S2 — Core Backend (documentado post-implementación) |
| **Estado** | ✅ Implementado (BE) |
| **Protocol normativo** | `VTT.PROTOCOL-DEV-001` v1.1.0 — ver `00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-DEV-001_ciclo_devlog_entry.md` |
| **Workflows operativos** | `VTT.WORKFLOW-DEV-001.001` (crear), `.002` (editar/transicionar), `.003` (cerrar sprint) — `00-platform/02.normativa/02.Workflows/` |
| **Skills** | `VTT.SKILL-DEV-001..005` — `00-platform/02.normativa/03.Skills/dev/` |
| **Cards runtime (Nivel R)** | `VTT.CARD-DEV-001/002/003` — `00-platform/02.normativa/05.Cards/dev/` |
| **Frontera con bug/blocker/question** | escalación a `VTT.PROTOCOL-ASG-001` §5.4 (bug/blocker) / §5.4.bis (question) — ver Protocol DEV-001 §5.1.2.bis |

---

## 1. QUÉ ES

El lifecycle de devlog entries es el sistema de estados que permite transicionar una entrada de devlog desde su creación hasta su resolución. Cada entry creada durante la ejecución de una tarea nace en estado `pending` y debe avanzar explícitamente a través de los estados del ciclo hasta quedar `resolved`, `wont_fix` o `deferred`.

---

## 2. PARA QUÉ SIRVE

- **Trazabilidad** — Saber qué decisiones y observaciones fueron revisadas y por quién
- **Review Gate** — Los entries con severidad `critical` o `high` en estado `pending` bloquean el avance de la tarea
- **Auditoría** — Demostrar que cada hallazgo fue atendido, no ignorado
- **Cierre limpio** — Garantizar que al cerrar un sprint no quedan decisiones sin procesar
- **Visibilidad PM** — El PM puede ver qué entries quedan pendientes sin necesidad de leer todos los comentarios

---

## 3. PRECONDICIONES

### Para que el lifecycle funcione, debe existir:

| Precondición | Entidad | ¿Existe? |
|--------------|---------|----------|
| Tarea creada | `tasks` | ✅ |
| Devlog entry creada | `task_devlog_entries` | ✅ |
| Entry en estado `pending` | — | ✅ (estado inicial al crear) |

### Catálogo de categorías (`devlog_category_catalog`):

| code | name | ¿Usa severidad? | Cuándo usarla |
|------|------|-----------------|---------------|
| `decision` | Decision | ❌ No | Decisión técnica tomada durante la ejecución |
| `observation` | Observation | ❌ No | Observación de comportamiento o contexto |
| `blocker` | Blocker | ✅ Sí | Algo que impide avanzar |
| `tech_debt` | Tech Debt | ✅ Sí | Deuda técnica identificada para después |
| `testing_note` | Testing Note | ✅ Sí | Resultado de prueba o verificación |
| `risk` | Risk | ✅ Sí | Riesgo potencial identificado |
| `issue` | Issue | ✅ Sí | Observación o inconsistencia (no bugs) |

### Catálogo de severidades (para categorías que la usan):

| Severidad | Significado | ¿Bloquea Review Gate? |
|-----------|-------------|----------------------|
| `critical` | Impide que el sistema funcione | ✅ SÍ |
| `high` | Problema serio que debe resolverse | ✅ SÍ |
| `medium` | Debería resolverse, no urgente | ❌ NO |
| `low` | Nice to have | ❌ NO |

---

## 4. ESTADOS DEL LIFECYCLE

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  ESTADO: pending                                                    │
│     │  (estado inicial al crear la entry)                          │
│     │                                                               │
│     ▼  Agente o TL reconoce la entry                               │
│                                                                     │
│  ESTADO: acknowledged                                               │
│     │  (alguien tomó nota, está en proceso)                        │
│     │                                                               │
│     ▼  Opcionalmente, cuando se trabaja activamente en ella        │
│                                                                     │
│  ESTADO: in_progress                                                │
│     │  (hay trabajo activo asociado)                               │
│     │                                                               │
│     ├─► ESTADO: resolved                                            │
│     │   (se resolvió — decisión documentada / issue corregido)     │
│     │                                                               │
│     ├─► ESTADO: wont_fix                                            │
│     │   (se decidió conscientemente no resolver)                   │
│     │                                                               │
│     └─► ESTADO: deferred                                            │
│         (se pospone a una fase o sprint futuro)                    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Tabla de estados

| Estado | Significado | ¿Quién lo pone? | ¿Terminal? |
|--------|-------------|-----------------|-----------|
| `pending` | Creada, sin atender | Sistema (al crear) | ❌ |
| `acknowledged` | Vista y reconocida | Agente o TL | ❌ |
| `in_progress` | Hay trabajo activo | Agente o TL | ❌ |
| `resolved` | Resuelta o documentada | Agente o TL | ✅ |
| `wont_fix` | No se va a resolver (decisión consciente) | TL o PM | ✅ |
| `deferred` | Pospuesta a sprint/fase futura | TL o PM | ✅ |

> **IMPORTANTE:** Las transiciones son **irreversibles**. Una vez en estado terminal (`resolved`, `wont_fix`, `deferred`), no se puede volver atrás.

---

## 5. CÓMO SE ACTIVA

### ¿Quién puede transicionar estados?

| Rol | ¿Puede transicionar? | Notas |
|-----|----------------------|-------|
| Agente ejecutor | ✅ Sí | Sus propias entries mientras la tarea está activa |
| Tech Lead | ✅ Sí | Entries de cualquier tarea que esté revisando |
| PM | ✅ Sí | Especialmente para `wont_fix` y `deferred` |
| QA | ✅ Sí | Entries de tareas en revisión |

### ¿Cuándo se usa cada estado terminal?

| Si... | Usar estado |
|-------|-------------|
| La decisión fue tomada y documentada | `resolved` |
| El issue fue corregido | `resolved` |
| La observación fue verificada | `resolved` |
| Se decidió no resolver (con justificación) | `wont_fix` |
| Se pospone a S3, R2 u otro sprint | `deferred` |

---

## 6. FLUJO OPERATIVO

### 6.1 TRANSICIONAR UN ENTRY

#### Endpoint

```
PATCH /api/tasks/:taskId/devlog/:entryId/status
```

#### Request

```json
{
  "status": "acknowledged"
}
```

```json
{
  "status": "resolved",
  "resolution": "Decisión tomada: usar UUID v4 por consistencia con el resto del sistema."
}
```

```json
{
  "status": "deferred",
  "resolution": "Pospuesto a Sprint S3. Vinculado a tarea MS-323."
}
```

```json
{
  "status": "wont_fix",
  "resolution": "CleanupService no aplica en S2. Scope definido para S3 según roadmap."
}
```

#### Response (ejemplo `resolved`)

```json
{
  "id": "4ff4e0a1-0215-4a70-9ee6-dd525e0bec02",
  "taskId": "MS-316",
  "categoryCode": "decision",
  "severity": null,
  "title": "Decisión: usar UUID v4 para IDs",
  "description": "Por consistencia con el resto del sistema...",
  "status": "resolved",
  "resolvedBy": "92225290-6b6b-4c1f-a940-dcb4262507aa",
  "resolvedAt": "2026-05-21T17:38:55.422Z",
  "resolution": "Decisión tomada: usar UUID v4 por consistencia con el resto del sistema.",
  "updatedAt": "2026-05-21T17:38:55.422Z"
}
```

---

### 6.2 CONSULTAR DEVLOG DE UNA TAREA

#### Endpoint

```
GET /api/tasks/:taskId/devlog
```

#### Response

```json
{
  "data": [
    {
      "id": "uuid",
      "taskId": "MS-316",
      "categoryCode": "decision",
      "severity": null,
      "title": "Decisión: usar UUID v4",
      "description": "...",
      "status": "resolved",
      "resolvedAt": "2026-05-21T17:38:55.422Z",
      "resolution": "Documentado en reporte M2.",
      "category": { "code": "decision", "name": "Decision" }
    }
  ]
}
```

---

### 6.3 CREAR UNA ENTRY DE DEVLOG

#### Endpoint

```
POST /api/tasks/:taskId/devlog
```

#### Request (entry tipo `decision`, sin severidad)

```json
{
  "categoryCode": "decision",
  "title": "Usar lazyConnect: true en Redis",
  "description": "Redis no bloquea el startup si no está disponible al arrancar. Patrón de resiliencia para entornos de contenedores.",
  "reportedBy": "92225290-6b6b-4c1f-a940-dcb4262507aa"
}
```

#### Request (entry tipo `tech_debt`, con severidad)

```json
{
  "categoryCode": "tech_debt",
  "severity": "low",
  "title": "CleanupService no implementado en S2",
  "description": "CleanupService planificado pero fuera de scope S2. Solo existen 5 services. Deuda para S3.",
  "reportedBy": "92225290-6b6b-4c1f-a940-dcb4262507aa"
}
```

---

## 7. FLUJO COMPLETO — DESDE CREACIÓN HASTA CIERRE DE SPRINT

```
AGENTE durante ejecución de tarea
─────────────────────────────────────────────────────────
PASO 1: Agente identifica decisión / observación / issue
        │
        ▼
PASO 2: POST /api/tasks/:taskId/devlog
        Entry nace en status: pending
        │
        ▼
PASO 3: Agente continúa su trabajo
        (puede haber múltiples entries durante la tarea)
        │
        ▼
PASO 4: Agente mueve tarea a task_in_review
        El Review Gate verifica:
        - ¿Hay entries critical/high en pending? → BLOQUEA
        │
        ▼ (si no hay blockers)
        
TL durante code review
─────────────────────────────────────────────────────────
PASO 5: TL lee las entries de devlog de la tarea
        │
        ▼
PASO 6: TL procesa cada entry:
        PATCH /api/tasks/:taskId/devlog/:entryId/status
        
        → pending → acknowledged (reconocer)
        → acknowledged → resolved / wont_fix / deferred
        │
        ▼
PASO 7: Todos los entries en estado terminal
        TL puede proceder con PASS
        │
        ▼
PASO 8: TL mueve tarea a task_completed
```

---

## 8. RELACIÓN CON REVIEW GATE

El Review Gate verifica automáticamente los devlog entries antes de permitir avanzar:

| Condición | Resultado |
|-----------|-----------|
| Entries `critical` o `high` en `pending` | 🔴 BLOQUEADO — error 422 |
| Entries `critical` o `high` en `acknowledged` | 🔴 BLOQUEADO — error 422 |
| Entries `critical` o `high` en `in_progress` | 🔴 BLOQUEADO — error 422 |
| Entries `critical` o `high` en `resolved/wont_fix/deferred` | ✅ OK |
| Entries `medium` o `low` en cualquier estado | ✅ OK (no bloquean) |
| Entries sin severidad (`decision`, `observation`) en cualquier estado | ✅ OK (no bloquean) |

> **Nota:** Solo `critical` y `high` bloquean el Review Gate. Las entries `decision` y `observation` no tienen severidad y nunca bloquean — pero deben procesarse igualmente antes del cierre de sprint para mantener el historial limpio.

---

## 9. ERRORES COMUNES

| Error | Causa | Solución |
|-------|-------|---------|
| Usar `PATCH /api/tasks/:taskId/devlog/:entryId` con `{status: "resolved"}` | Endpoint incorrecto — ese endpoint edita el contenido, no el estado | Usar `PATCH /api/tasks/:taskId/devlog/:entryId/status` |
| Entry sigue en `pending` después del PATCH | Se usó el endpoint de edición en lugar del de lifecycle | Verificar con `GET /devlog` — si `status` no cambió, usar `/status` |
| Intentar volver a `pending` desde `resolved` | Las transiciones son irreversibles | No es posible — si hay error, crear nueva entry |
| Review Gate bloqueado con entries `decision` | `decision` no bloquea el gate | Verificar que el bloqueo es por entries con severidad `critical`/`high` |

---

## 10. INTEGRACIÓN CON CIERRE DE SPRINT

Al cerrar un sprint, el TL debe verificar que **todas las entries de todas las tareas del sprint** estén en estado terminal. El proceso recomendado:

```
1. GET /api/tasks/:taskId/devlog para cada tarea del sprint
2. Filtrar entries con status: pending | acknowledged | in_progress
3. Por cada entry pendiente:
   a. Evaluar si fue resuelta (resolved)
   b. Si no aplica resolvería → wont_fix con justificación
   c. Si va a otro sprint → deferred con referencia a tarea destino
4. Confirmar que 0 entries quedan en estados no terminales
5. Proceder con generación de reporte M (milestone)
```

---

## 11. EJEMPLOS POR CATEGORÍA

### Ejemplo: `decision` (sin severidad)

```
Título: multer movido de devDependencies a dependencies
Descripción: Es un middleware de runtime (manejo de uploads), no solo tipos.
             Si queda en devDeps no estará disponible en producción.
Resolución: Corrección de clasificación confirmada. PR #45 incluye el cambio.
Estado final: resolved
```

### Ejemplo: `tech_debt` (con severidad low)

```
Título: CleanupService no implementado en S2
Severidad: low
Descripción: CleanupService planificado en 3B.1.4 pero fuera de scope S2.
             Solo existen 5 services. Impacto: memoria puede crecer sin límite
             hasta que se implemente la limpieza automática.
Resolución: Deferred — asignado a MS-323 en Sprint S3.
Estado final: deferred
```

### Ejemplo: `blocker` (con severidad high)

```
Título: Endpoint POST /close no implementado en API VTT
Severidad: high
Descripción: closedAt permanece null. POST /close retorna 404.
             Sprint en sprint_completed operacionalmente cerrado pero
             sin fecha de cierre formal registrada.
Resolución: wont_fix en S2 — sprint ya está cerrado de facto.
            Implementar endpoint en backlog VTT infraestructura.
Estado final: wont_fix
```

---

**Documento:** FEATURE_DEVLOG_LIFECYCLE.md  
**Versión:** 1.0  
**Fecha:** 2026-05-21  
**Generado por:** Tech Lead — documentación post-aplicación S2
