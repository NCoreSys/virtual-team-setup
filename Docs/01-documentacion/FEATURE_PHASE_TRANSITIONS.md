# FEATURE: TRANSICIÓN Y CIERRE DE FASES

| Campo | Valor |
|-------|-------|
| **Feature** | Transición y Cierre de Fases |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-06 |
| **Detectado en** | Memory Service — Planning → Analysis |
| **Estado** | 📋 Gap documentado — pendiente decisión de implementación |

---

## 1. QUÉ ES

Define qué sucede después de que un sprint es firmado (`allApprovalsSigned: true`) y cómo se transiciona formalmente entre fases del proyecto (ej: Planning → Analysis).

---

## 2. GAP DETECTADO

Durante la sesión de SA Reviewer del proyecto Memory Service (2026-05-06), se detectó que el workflow no tiene definido el proceso post-firma de sprint:

| Pregunta | Respuesta actual |
|----------|-----------------|
| ¿Qué pasa después de firmar un sprint? | No definido |
| ¿Hay validación para iniciar la siguiente fase? | No definido |
| ¿Quién autoriza iniciar la siguiente fase? | No definido |
| ¿Es automático o requiere acción humana? | No definido |
| ¿Cómo se cierra formalmente una fase? | No definido |

---

## 3. CONTEXTO TÉCNICO

### 3.1 Mecanismos disponibles en la API

La API tiene dos mecanismos para el estado de una fase:

**Mecanismo A — Lifecycle (`PUT /api/lifecycle/phase/:id`)**
```
Ciclo: analysis → design → development → testing → deployment → completed
Restricción RN-007: solo permite avanzar ±1 paso
Body: { "newStage": "design", "changedBy": "UUID" }
```
> Este lifecycle representa la madurez de los entregables dentro de la fase, no el estado del proyecto.

**Mecanismo B — StatusId (`PUT /api/phases/:id`)**
```
Body: { "statusId": "UUID-de-phase_completed" }
Statuses disponibles: phase_pending, phase_completed (y otros del status_catalog)
```
> Requiere el UUID exacto del status `phase_completed` del catálogo.

### 3.2 Estado actual de las fases en Memory Service

| Fase | Estado actual | Debería estar |
|------|--------------|---------------|
| Project Setup | `phase_pending` | `phase_completed` |
| Discovery | `phase_pending` | `phase_completed` |
| Planning | `phase_pending` | `phase_completed` |
| Analysis | `phase_pending` | En curso |

Las 3 primeras fases completadas nunca fueron cerradas formalmente porque el proceso no estaba definido.

---

## 4. OPCIONES DE DISEÑO

### Opción A — Sin gate (recomendada para MVP)
Sprint firmado = fase lista. La siguiente fase puede iniciar directamente.

- ✅ Simple de implementar
- ✅ No bloquea el flujo de trabajo
- ✅ El sprint firmado ya es el registro formal de cierre
- ❌ No hay validación automática antes de iniciar la siguiente fase

### Opción B — Gate automático
Sprint firmado → Sistema valida checklist automático → Si OK, siguiente fase se habilita.

- ✅ Seguridad adicional
- ❌ Requiere definir qué valida el checklist
- ❌ Mayor complejidad de implementación

### Opción C — Gate manual (PM/TL autoriza)
Sprint firmado → PM o TL da "GO" explícito → Siguiente fase inicia.

- ✅ Control humano total
- ❌ Crea fricción y dependencia de disponibilidad del PM/TL
- ❌ No escala con múltiples proyectos paralelos

---

## 5. DECISIÓN

**Opción seleccionada:** `_______` (pendiente confirmación del PM)

**Recomendación SA:** Opción A para MVP. Sprint firmado = fase cerrada. Sin gate adicional.

---

## 6. IMPLEMENTACIÓN PROPUESTA (Opción A)

### 6.1 Regla de negocio
```
SI sprint.allApprovalsSigned = true
  → La fase asociada puede considerarse cerrada
  → La siguiente fase puede iniciar sin acción adicional
  → No se requiere un "gate review" explícito
```

### 6.2 Cierre formal de fase (opcional, para reporting)

Si se decide cerrar la fase formalmente en la BD:

```
PUT /api/phases/:id
Body: { "statusId": "UUID-phase_completed" }
```

> **Pendiente:** Obtener el UUID de `phase_completed` del status_catalog. No está expuesto en ningún endpoint público actual — requiere consulta directa a BD o que el equipo de desarrollo lo exponga via API.

### 6.3 Proceso del SA Reviewer post-sprint

Con Opción A, el proceso queda:

```
1. Sprint firmado (allApprovalsSigned: true)        ✅ Ya implementado
2. Sprint marcado como sprint_completed              ✅ Ya implementado
   PATCH /api/sprints/:id { "statusCode": "sprint_completed" }
3. Iniciar siguiente fase directamente               ← Nuevo: sin gate
   (asignar tareas, crear sprint, etc.)
```

---

## 7. FASES PENDIENTES DE CIERRE EN MEMORY SERVICE

Con Opción A, las siguientes fases se consideran cerradas por tener sprint firmado:

| Fase | Sprint | Estado sprint | Acción requerida |
|------|--------|--------------|-----------------|
| Planning | #1 Planning | `sprint_completed` + firmado | ✅ Cerrada — puede iniciar Analysis |
| Project Setup | Sin sprint | — | Cerrar manualmente cuando se defina el UUID |
| Discovery | Sin sprint | — | Cerrar manualmente cuando se defina el UUID |

---

## 8. PENDIENTES PARA EL EQUIPO DE DESARROLLO

| Pendiente | Prioridad | Descripción |
|-----------|-----------|-------------|
| Exponer UUID de `phase_completed` | Alta | Agregar al catálogo público o endpoint de statuses |
| Definir si el cierre de fase es automático | Media | Al firmar sprint → auto-cerrar fase asociada |
| Documentar en GUIA_AGENTES_MODELO_DINAMICO | Media | Agregar sección de transición entre fases |

---

## 9. FUENTES

- Sesión SA Reviewer Memory Service 2026-05-06
- `GET /api/lifecycle/phase/:id` — response con allowedTransitions
- Swagger `PUT /api/lifecycle/{entityType}/{entityId}` — RN-007
- Análisis PM: opciones A/B/C (2026-05-06)
