# IMPROVE-001 — Pool de Transacciones VTT

| Campo | Valor |
|---|---|
| **Código** | `IMPROVE-001` |
| **Título** | Pool de Transacciones VTT |
| **Categoría** | Infrastructure / Architecture |
| **Prioridad** | 🟡 Media |
| **Estimación rough** | 3-5 días (MVP) |
| **Estado** | Propuesta — pendiente de evaluación PM |
| **Autor** | PM Martin Rivas |
| **Fecha** | 2026-05-13 |
| **Origen** | Sesión TL Memory Service — discusión sobre ahorro de tokens y duplicación de scripts |

---

## 1. Problema que resuelve

Hoy cada agente que necesita mutar datos en VTT (crear tareas, subir attachments, agregar evidencias, resolver devlog, etc.) **regenera el script desde cero** dentro de su conversación:

```
Agente recibe instrucción → escribe curl/python → ejecuta → reporta
```

Esto causa:

| Problema | Impacto observado en MS-283..MS-285 |
|---|---|
| **Costo de tokens repetitivo** | El mismo POST attachment se regenera ~20 veces por sprint |
| **Inconsistencia entre agentes** | Cada agente formatea el JSON ligeramente distinto |
| **Sin dedup automático** | Riesgo de crear TIs/evidencias duplicadas (vimos esto al estandarizar evidencias) |
| **Sin auditoría central** | No hay forma de saber quién hizo qué mutación VTT, cuándo, desde qué tarea |
| **Sin rollback** | Si una operación falla a mitad de un batch, no hay forma estándar de revertir |
| **Sin validación previa** | Errores 400 (uploadedById faltante, criteriaTypeCode mal, etc.) se descubren en ejecución |

## 2. Impacto / valor que aporta

### Cuantitativo
- **Ahorro estimado de tokens**: 30-40% por agente en tareas con muchas mutaciones VTT
- **Reducción de errores 400/422**: validación previa en el pool elimina errores recurrentes
- **Auditoría completa**: 100% de mutaciones VTT pasan por un único punto

### Cualitativo
- Los agentes se enfocan en **decisiones de negocio**, no en construir HTTP requests
- Las **skills** se vuelven más reutilizables (mismo input → mismo output independientemente del agente)
- **Migración VTT** simplificada: si el backend cambia un endpoint, solo se actualiza el pool

## 3. Concepto / Solución propuesta

### Flujo actual (sin pool)

```
Agente IA → genera script → ejecuta curl/python → backend VTT
            ↑ tokens caros           ↑ sin validación
```

### Flujo propuesto (con pool)

```
Agente IA → emite JSON de operación → POOL DE TRANSACCIONES → backend VTT
            ↑ ~50 tokens             ↑ valida, dedupa,
                                       ordena, ejecuta,
                                       audita, retorna
```

### Componentes del pool

```
┌─────────────────────────────────────────────────────────────┐
│ POOL DE TRANSACCIONES VTT                                    │
│                                                              │
│  1. API de entrada                                           │
│     POST /pool/transactions                                  │
│     Body: { operations: [ {type, params}, ... ] }            │
│                                                              │
│  2. Validador                                                │
│     - Valida schema de cada operation                        │
│     - Verifica precondiciones (auth, IDs existen)            │
│                                                              │
│  3. Deduplicador                                             │
│     - Detecta operaciones idénticas en N segundos            │
│     - Detecta duplicados semánticos (mismo content_hash)     │
│                                                              │
│  4. Ordenador                                                │
│     - Resuelve dependencias entre operations                 │
│     - Ej: vincular TI a tarea requiere que TI exista primero │
│                                                              │
│  5. Ejecutor                                                 │
│     - Corre cada operation (HTTP a VTT)                      │
│     - Maneja errores y reintentos                            │
│                                                              │
│  6. Auditor                                                  │
│     - Registra cada operation en tabla pool_transactions     │
│     - Vincula a task_id, agent_id, timestamp                 │
│                                                              │
│  7. API de respuesta                                         │
│     - Retorna resultado por operation (success/error)        │
│     - Si rollback es posible, lo intenta en errores parciales│
└─────────────────────────────────────────────────────────────┘
```

### Schema de operación (input)

```json
{
  "agent_id": "ebbe3cee-abed-4b3b-860d-0a81f632b08a",
  "task_id": "MS-285",
  "correlation_id": "uuid-de-sesion",
  "operations": [
    {
      "id": "op-1",
      "type": "create_trackable_item",
      "params": {
        "project_id": "d0fc276d-...",
        "code": "DEBT-INFRA-VTT-02",
        "title": "[DEFER R2] ...",
        "type_code": "tech_debt",
        "status_code": "ti_draft"
      }
    },
    {
      "id": "op-2",
      "type": "link_trackable_item_to_task",
      "depends_on": ["op-1"],
      "params": {
        "trackable_item_id": "${op-1.result.id}",
        "task_id": "MS-285",
        "link_type": "related_to"
      }
    },
    {
      "id": "op-3",
      "type": "add_evidence",
      "depends_on": ["op-1"],
      "params": {
        "trackable_item_id": "${op-1.result.id}",
        "type": "link",
        "title": "[MS-285] [S1] PR #15",
        "url": "https://github.com/.../pull/15",
        "description": "[TASK:MS-285] [SPRINT:S1] ..."
      }
    }
  ]
}
```

### Schema de respuesta (output)

```json
{
  "correlation_id": "uuid-de-sesion",
  "status": "success | partial | failed",
  "results": [
    {
      "id": "op-1",
      "status": "success",
      "data": { "id": "uuid-creado" },
      "duration_ms": 120
    },
    { "id": "op-2", "status": "success", "data": { ... } },
    { "id": "op-3", "status": "skipped", "reason": "duplicate" }
  ],
  "audit_id": "uuid-pool-transaction"
}
```

## 4. Tipos de operaciones a soportar (catálogo inicial)

Basadas en lo que vimos en MS-283..MS-285:

| Tipo | Mapea a VTT |
|---|---|
| `create_task` | POST /api/phases/:phaseId/tasks |
| `update_task_status` | PATCH /api/tasks/:id/status |
| `add_attachment` | POST /api/tasks/:id/attachments |
| `add_comment` | POST /api/tasks/:id/comments |
| `create_acceptance_criterion` | POST /api/tasks/:id/criteria |
| `fulfill_acceptance_criterion` | PATCH /api/tasks/:id/criteria/:cid |
| `create_devlog_entry` | POST /api/tasks/:id/devlog-entries |
| `resolve_devlog_entry` | PATCH /api/tasks/:id/devlog/:eid/status |
| `create_trackable_item` | POST /api/projects/:id/trackable-items |
| `link_trackable_item_to_task` | POST /api/trackable-items/:id/tasks |
| `add_evidence` | POST /api/trackable-items/:id/evidence |
| `create_issue` | POST /api/tasks/:id/issues |
| `move_task_on_hold` | PUT /api/tasks/:id/on-hold |

## 5. Beneficios secundarios

### Para skills/scripts (Modelo Normativo VTT)

- Las **Skills** quedan más simples: solo emiten JSON al pool en vez de orquestar curls
- Los **Scripts** se reducen drásticamente (uno por tipo de operación, no por skill)
- El **Modelo Normativo VTT** (Protocol → Workflow → Skill → Script) gana coherencia: Script = "envío operación al pool"

### Para auditoría

- Reporte: "¿qué operaciones VTT hizo el agente BE durante MS-293?" → query a `pool_transactions` con filtro
- Reporte: "¿cuáles fueron las operaciones más usadas en S1?" → métricas de uso
- Detección de patrones erróneos: "el agente X falla 30% de sus `add_evidence` por marker mal formado"

### Para el modelo dinámico

- El bloque `delivery.dynamic_model_actions` del manifest se puede generar **automáticamente** desde el pool consultando `pool_transactions WHERE task_id = 'MS-XXX'`

## 6. Riesgos / consideraciones

| Riesgo | Mitigación |
|---|---|
| El pool se vuelve un cuello de botella | Diseñar stateless + horizontalmente escalable |
| Latencia adicional vs llamada directa | Aceptable si batch operations compensa (1 round-trip vs N) |
| Lock-in al backend pool | Mantener compatibilidad con llamadas directas (opcional usarlo) |
| Curva de aprendizaje agentes | Skills/Scripts existentes siguen funcionando; migración gradual |
| Mantenimiento del catálogo de operaciones | Una operación nueva = un endpoint nuevo en el pool. Versionar contratos. |

## 7. Plan de implementación sugerido (MVP)

### Fase 1 — MVP (3 días)
- Tabla `pool_transactions` (id, agent_id, task_id, correlation_id, operations_json, results_json, status, created_at)
- Endpoint `POST /pool/transactions` con validación de schema básico
- Soporte para 3 operaciones más comunes: `add_attachment`, `add_comment`, `update_task_status`
- Test con 1 tarea real (ej. cierre de MS-286)

### Fase 2 — Catálogo completo (2 días)
- Agregar las 13 operaciones del §4
- Soporte para `depends_on` entre operations (DAG resolution)
- Variable substitution `${op-X.result.id}` en parámetros

### Fase 3 — Dedup y auditoría (2 días)
- Detección de duplicados por content_hash + ventana temporal
- Dashboard simple de transacciones (vista `pool_transactions_summary`)
- Reporte por task_id

### Fase 4 — Integración con agentes (3 días)
- Actualizar SKL-MESSAGE-01 para invocar pool
- Actualizar skills de cierre para emitir batch operations
- Documentar en GUIA_NORMATIVA_VTT.md el nuevo paradigma

**Total estimado:** 10 días (2 semanas de un dev backend dedicado)

## 8. Decisión solicitada al PM

1. ¿Aprobar como **tarea VTT** del proyecto VTT (no de Memory Service)?
2. ¿Incluir en R2 del proyecto Memory Service o esperar a un release específico de plataforma VTT?
3. ¿Quién implementa? — Backend Engineer del equipo VTT o contrato externo
4. Si se aprueba: ¿prioridad sobre los gaps del VTT_PLATFORM_GAPS_2026-05-13 (defer, evidence DELETE, taskId en evidence)?

## 9. Referencias

- Sesión origen: TL Memory Service 2026-05-13 (cierre MS-285 con modelo dinámico)
- Documentos relacionados:
  - `00_GUIA_NORMATIVA_VTT.md` §2 (Modelo de 4 niveles — script como nivel 1)
  - `knowledge/platform-feedback/VTT_PLATFORM_GAPS_2026-05-13.md` (gaps backend)
  - `IMPROVE-002_bd_manifiestos_y_tis.md` (mejora relacionada)
- Conceptos análogos:
  - Pool de transacciones SAP (el ejemplo original del PM)
  - Outbox pattern (microservicios)
  - Event sourcing (CQRS)

## 10. Changelog

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-05-13 | Documento inicial — propuesta para evaluación PM |
