# METODOLOGÍA: Cierre de Sprints y Fases

**Documento:** METODOLOGIA_CIERRE_SPRINT_FASE.md  
**Versión:** 1.0  
**Autor:** PJM-Agent  
**Fecha:** 2026-04-02  
**Audiencia:** TL, AR, QA, DL, PM  
**Propósito:** Definir el proceso formal de cierre de sprints y fases en VTT

---

## 1. PRINCIPIO FUNDAMENTAL

> **Toda actividad tiene inicio y fin.**

En un diagrama de flujo bien diseñado, cada proceso tiene un nodo de entrada y un nodo de salida. Los sprints y fases no son la excepción:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         FLUJO DE SPRINT                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────┐      │
│  │  INICIO  │───▶│  DESARROLLO  │───▶│  VALIDACIÓN  │───▶│  CIERRE  │      │
│  │  Sprint  │    │  (tareas)    │    │  (TL/AR/QA)  │    │  Sprint  │      │
│  └──────────┘    └──────────────┘    └──────────────┘    └──────────┘      │
│       │                                                        │            │
│       │              Sprint abierto                            │            │
│       └────────────────────────────────────────────────────────┘            │
│                                                                             │
│  Sin tarea de CIERRE → Sprint queda indefinidamente "en progreso"           │
│  Con tarea de CIERRE → Sprint tiene fin formal, puede auditarse             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. TIPOS DE CIERRE

### 2.1 Cierre de Sprint

| Aspecto | Descripción |
|---------|-------------|
| **Qué cierra** | Un sprint individual (S01, S09, S11, etc.) |
| **Quién firma** | TL + AR + QA (+ DL si hay FE) |
| **Documento guía** | CLOSURE_S[N].md |
| **Tarea en VTT** | `CIERRE-S[N]` |
| **Resultado** | Sprint completado, tareas no se pueden reabrir |

### 2.2 Cierre de Fase/Bloque

| Aspecto | Descripción |
|---------|-------------|
| **Qué cierra** | Un bloque completo (varios sprints) |
| **Quién firma** | AR (integración) + PM (autorización) |
| **Documento guía** | CLOSURE_BLOQUE_[N].md |
| **Tarea en VTT** | `CIERRE-BLOQUE-[N]` |
| **Resultado** | Fase cerrada, no se puede reabrir. Bugs van a Soporte. |

---

## 3. PROCESO DE CIERRE DE SPRINT

### 3.1 Diagrama de Flujo

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PROCESO: CIERRE DE SPRINT                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────┐                                   │
│  │ 1. TL verifica que todas las        │                                   │
│  │    tareas de desarrollo están       │                                   │
│  │    en task_completed                │                                   │
│  └──────────────┬──────────────────────┘                                   │
│                 │                                                           │
│                 ▼                                                           │
│  ┌─────────────────────────────────────┐                                   │
│  │ 2. TL crea tarea CIERRE-S[N]        │                                   │
│  │    usando CLOSURE_S[N].md           │                                   │
│  │    como plantilla                   │                                   │
│  └──────────────┬──────────────────────┘                                   │
│                 │                                                           │
│                 ▼                                                           │
│  ┌─────────────────────────────────────┐                                   │
│  │ 3. TL completa su sección           │                                   │
│  │    (Code Review) y firma            │                                   │
│  │    → Asigna a AR                    │                                   │
│  └──────────────┬──────────────────────┘                                   │
│                 │                                                           │
│                 ▼                                                           │
│  ┌─────────────────────────────────────┐                                   │
│  │ 4. AR completa su sección           │                                   │
│  │    (Integration Audit) y firma      │                                   │
│  │    → Asigna a QA                    │                                   │
│  └──────────────┬──────────────────────┘                                   │
│                 │                                                           │
│                 ▼                                                           │
│  ┌─────────────────────────────────────┐                                   │
│  │ 5. QA completa su sección           │                                   │
│  │    (Testing) y firma                │                                   │
│  │    → Asigna a DL (si hay FE)        │                                   │
│  │    → O asigna a TL (si solo BE)     │                                   │
│  └──────────────┬──────────────────────┘                                   │
│                 │                                                           │
│                 ▼                                                           │
│  ┌─────────────────────────────────────┐                                   │
│  │ 6. (Si FE) DL completa Visual       │                                   │
│  │    Review y firma                   │                                   │
│  │    → Asigna a TL                    │                                   │
│  └──────────────┬──────────────────────┘                                   │
│                 │                                                           │
│                 ▼                                                           │
│  ┌─────────────────────────────────────┐                                   │
│  │ 7. TL verifica todas las firmas     │                                   │
│  │    → Mueve tarea a task_completed   │                                   │
│  └──────────────┬──────────────────────┘                                   │
│                 │                                                           │
│                 ▼                                                           │
│  ┌─────────────────────────────────────┐                                   │
│  │ 8. SPRINT CERRADO                   │                                   │
│  │    • Tareas no se pueden reabrir    │                                   │
│  │    • Métricas finales registradas   │                                   │
│  │    • Listo para cierre de fase      │                                   │
│  └─────────────────────────────────────┘                                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Crear Tarea de Cierre en VTT

**Endpoint:** `POST /api/projects/:projectId/tasks`

```json
{
  "title": "CIERRE-S09: Cierre Sprint 9 — Catálogos + Trazabilidad Base",
  "description": "Tarea de cierre formal del Sprint S09. Requiere firmas de TL, AR, QA.",
  "phaseCode": "05-testing",
  "assignedToId": "[UUID del TL]",
  "estimatedHours": 2,
  "complexity": "MEDIUM",
  "category": "review",
  "dependsOn": ["[UUID última tarea de validación del sprint]"]
}
```

**Campos de la tarea:**

| Campo | Valor | Notas |
|-------|-------|-------|
| `title` | `CIERRE-S[N]: Cierre Sprint [N] — [Nombre]` | Formato estándar |
| `phaseCode` | `05-testing` o fase de validación | Donde viven las tareas de cierre |
| `assignedToId` | UUID del TL | TL inicia el proceso |
| `estimatedHours` | 2-3h | Depende de complejidad |
| `category` | `review` | Categoría de revisión |
| `dependsOn` | Última tarea de validación | No puede iniciar hasta que todo esté listo |

### 3.3 Checklist del TL para Cierre de Sprint

```markdown
## Antes de crear la tarea CIERRE-S[N]:

[ ] Todas las tareas de desarrollo están en `task_completed`
[ ] Todas las tareas de validación están en `task_completed`
[ ] Code Review completado sin blockers
[ ] PRs mergeados a rama principal
[ ] Documentación dinámica actualizada (.LOGIC.md, API_CONTRACT)
[ ] 0 bugs P0/P1 abiertos

## Al crear la tarea:

[ ] Usar CLOSURE_S[N].md como referencia
[ ] Asignarme como responsable inicial
[ ] Configurar dependencia con última tarea de validación
[ ] Notificar a AR y QA que el proceso de cierre inicia

## Durante el cierre:

[ ] Completar mi sección (§2 o §3 según documento)
[ ] Firmar con fecha
[ ] Reasignar a siguiente firmante
[ ] Monitorear progreso hasta completar
```

---

## 4. PROCESO DE CIERRE DE FASE/BLOQUE

### 4.1 Diagrama de Flujo

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PROCESO: CIERRE DE FASE/BLOQUE                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────┐                                   │
│  │ 1. TL verifica que todos los        │                                   │
│  │    sprints del bloque tienen        │                                   │
│  │    CIERRE-S[N] en task_completed    │                                   │
│  └──────────────┬──────────────────────┘                                   │
│                 │                                                           │
│                 ▼                                                           │
│  ┌─────────────────────────────────────┐                                   │
│  │ 2. TL crea tarea CIERRE-BLOQUE-[N]  │                                   │
│  │    usando CLOSURE_BLOQUE_[N].md     │                                   │
│  │    → Asigna a AR                    │                                   │
│  └──────────────┬──────────────────────┘                                   │
│                 │                                                           │
│                 ▼                                                           │
│  ┌─────────────────────────────────────┐                                   │
│  │ 3. AR ejecuta validación de         │                                   │
│  │    integración cross-sprint         │                                   │
│  │    (§3 del CLOSURE_BLOQUE)          │                                   │
│  └──────────────┬──────────────────────┘                                   │
│                 │                                                           │
│                 ▼                                                           │
│  ┌─────────────────────────────────────┐                                   │
│  │ 4. AR firma integración             │                                   │
│  │    → Asigna a PM                    │                                   │
│  └──────────────┬──────────────────────┘                                   │
│                 │                                                           │
│                 ▼                                                           │
│  ┌─────────────────────────────────────┐                                   │
│  │ 5. PM revisa:                       │                                   │
│  │    • Todos los sprints cerrados     │                                   │
│  │    • Métricas consolidadas          │                                   │
│  │    • 0 bugs P0/P1 abiertos          │                                   │
│  │    • AR firmó integración           │                                   │
│  └──────────────┬──────────────────────┘                                   │
│                 │                                                           │
│                 ▼                                                           │
│  ┌─────────────────────────────────────┐                                   │
│  │ 6. PM dice "APPROVED"               │                                   │
│  │    → Mueve tarea a task_completed   │                                   │
│  └──────────────┬──────────────────────┘                                   │
│                 │                                                           │
│                 ▼                                                           │
│  ┌─────────────────────────────────────┐                                   │
│  │ 7. FASE/BLOQUE CERRADO              │                                   │
│  │    • No se puede reabrir            │                                   │
│  │    • Bugs futuros → Soporte         │                                   │
│  │    • Habilitado inicio siguiente    │                                   │
│  │      bloque                         │                                   │
│  └─────────────────────────────────────┘                                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Crear Tarea de Cierre de Bloque en VTT

**Endpoint:** `POST /api/projects/:projectId/tasks`

```json
{
  "title": "CIERRE-BLOQUE-2: Cierre Fase Trazabilidad (S09 + S10)",
  "description": "Tarea de cierre formal del Bloque 2. Requiere validación AR y aprobación PM.",
  "phaseCode": "05-testing",
  "assignedToId": "[UUID del AR]",
  "estimatedHours": 3,
  "complexity": "HIGH",
  "category": "review",
  "dependsOn": ["[UUID CIERRE-S09]", "[UUID CIERRE-S10]"]
}
```

### 4.3 Qué hace el PM al aprobar

Cuando PM marca "APPROVED" en el CLOSURE_BLOQUE:

1. **Fase queda cerrada** — no se pueden agregar tareas, modificar sprints, o reabrir issues
2. **Bugs futuros van a Soporte** — si aparece un bug post-cierre, se crea ticket en área de Soporte, no se reabre el sprint
3. **Siguiente bloque habilitado** — las dependencias de fase se desbloquean
4. **Métricas congeladas** — horas, entregables, varianza quedan como registro histórico

---

## 5. ORDEN DE FIRMAS

### 5.1 Sprint sin FE (solo Backend)

```
TL (Code Review) → AR (Integration Audit) → QA (Testing) → TL (Cierre)
```

| Paso | Quién | Qué hace | Siguiente |
|------|-------|----------|-----------|
| 1 | TL | Completa Code Review, firma | Asigna a AR |
| 2 | AR | Completa Integration Audit, firma | Asigna a QA |
| 3 | QA | Completa Testing, firma | Asigna a TL |
| 4 | TL | Verifica 3 firmas, cierra tarea | `task_completed` |

### 5.2 Sprint con FE

```
TL (Code Review) → AR (Integration Audit) → QA (Testing) → DL (Visual Review) → TL (Cierre)
```

| Paso | Quién | Qué hace | Siguiente |
|------|-------|----------|-----------|
| 1 | TL | Completa Code Review BE+FE, firma | Asigna a AR |
| 2 | AR | Completa Integration Audit, firma | Asigna a QA |
| 3 | QA | Completa Testing E2E, firma | Asigna a DL |
| 4 | DL | Completa Visual Review, firma | Asigna a TL |
| 5 | TL | Verifica 4 firmas, cierra tarea | `task_completed` |

### 5.3 Cierre de Fase/Bloque

```
TL (Crea tarea) → AR (Integración) → PM (Aprobación)
```

| Paso | Quién | Qué hace | Siguiente |
|------|-------|----------|-----------|
| 1 | TL | Crea tarea, verifica sprints cerrados | Asigna a AR |
| 2 | AR | Valida integración cross-sprint, firma | Asigna a PM |
| 3 | PM | Revisa todo, dice "APPROVED" | `task_completed` |

---

## 6. ESTADOS DE LA TAREA DE CIERRE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ESTADOS DE TAREA CIERRE                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  task_draft ──▶ task_ready ──▶ task_in_progress ──▶ task_completed         │
│       │              │                │                    │                │
│       │              │                │                    │                │
│   TL crea        TL inicia       Firmas en           Sprint/Fase           │
│   la tarea       proceso         progreso             cerrado               │
│                                                                             │
│  ⚠️ NUNCA usar task_approved para tareas de cierre                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Estados válidos:**

| Estado | Cuándo |
|--------|--------|
| `task_draft` | TL acaba de crear la tarea |
| `task_ready` | TL inicia el proceso de firmas |
| `task_in_progress` | Firmas en progreso (TL→AR→QA→DL) |
| `task_completed` | Todas las firmas, sprint/fase cerrado |

**Estados NO válidos para cierre:**
- `task_approved` — NO usar, es para tareas de desarrollo
- `task_blocked` — Si hay blocker, resolver antes de iniciar cierre

---

## 7. QUÉ PASA SI HAY PROBLEMAS

### 7.1 Durante el Cierre de Sprint

| Problema | Acción |
|----------|--------|
| Bug P0 descubierto | Detener cierre, crear tarea de fix, resolver, reiniciar cierre |
| Firma rechazada | Documentar razón, resolver issue, volver a solicitar firma |
| Finding AR blocker | TL coordina corrección, AR re-verifica, continúa proceso |

### 7.2 Después del Cierre de Fase

| Problema | Acción |
|----------|--------|
| Bug descubierto post-cierre | Crear ticket en área de Soporte |
| Feature faltante | Agregar a backlog del siguiente release |
| Documentación incompleta | Crear tarea de documentación en siguiente sprint |

**Regla crítica:** Una vez que PM dice "APPROVED" en CLOSURE_BLOQUE, la fase NO se reabre. Todo lo que aparezca después se maneja como Soporte o siguiente release.

---

## 8. DOCUMENTOS RELACIONADOS

| Documento | Propósito |
|-----------|-----------|
| `CLOSURE_S[N].md` | Plantilla de cierre por sprint |
| `CLOSURE_BLOQUE_[N].md` | Plantilla de cierre por fase |
| `INTEGRATION_AUDIT_CHECKLIST_V4.md` | Checklist que AR usa en su firma |
| `CODE_REVIEW_GUIDELINES_V4.md` | Guía que TL usa en su firma |
| `FINAL_AUDIT_REPORT_V4.md` | Auditoría final de release |

---

## 9. IMPLEMENTACIÓN FUTURA

### 9.1 Fase Actual (Manual)

- TL crea tarea de cierre manualmente
- Firmas se registran en documento CLOSURE
- TL mueve tarea a `task_completed`

### 9.2 Fase Futura (Automatizado)

Cuando se implemente el módulo de firmas:

1. Sistema detecta que todas las tareas del sprint están `task_completed`
2. Sistema crea automáticamente tarea `CIERRE-S[N]`
3. Sistema notifica a TL para iniciar proceso
4. Firmas se registran en BD (tabla `approvals`)
5. Sistema valida firmas requeridas
6. Sistema marca sprint como cerrado automáticamente

---

## 10. RESUMEN EJECUTIVO

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         RESUMEN: CIERRE                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  SPRINT:                                                                    │
│  • TL crea tarea CIERRE-S[N]                                               │
│  • Firmas: TL → AR → QA (→ DL si FE)                                       │
│  • TL cierra cuando todas las firmas están                                 │
│                                                                             │
│  FASE/BLOQUE:                                                               │
│  • TL crea tarea CIERRE-BLOQUE-[N]                                         │
│  • Depende de todos los CIERRE-S[N] del bloque                             │
│  • AR valida integración                                                    │
│  • PM dice "APPROVED" → Fase cerrada, no se reabre                         │
│                                                                             │
│  POST-CIERRE:                                                               │
│  • Bugs → Soporte                                                          │
│  • Features → Siguiente release                                             │
│  • Métricas → Congeladas                                                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 11. HISTORIAL DE VERSIONES

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | 2026-04-02 | PJM-Agent | Versión inicial |

---

**FIN DEL DOCUMENTO METODOLÓGICO**
