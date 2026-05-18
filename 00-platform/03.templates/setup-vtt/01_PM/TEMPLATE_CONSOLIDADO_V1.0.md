# TEMPLATE — CONSOLIDADO del Proyecto (Plan Maestro)

> **Cómo usar:**
> 1. Copiar a `01-PM/CONSOLIDADO_<<PROYECTO>>.md`
> 2. Consolidar: INICIACION + FASES_APLICABLES + PRE_HANDOFF_IMPLEMENTACION
> 3. Para fases de docs (0-3B) mantener deliverables
> 4. Para fases de código (4-7) reemplazar deliverables por tareas
> 5. Borrar este bloque antes de emitir

---

# CONSOLIDADO <<NOMBRE_PROYECTO>> — Plan Maestro

| Campo | Valor |
|-------|-------|
| **Documento** | CONSOLIDADO_<<PROYECTO>>.md |
| **Versión** | 1.0 |
| **Fecha** | <<YYYY-MM-DD>> |
| **Autor** | PM (<<Nombre>>) |
| **Proyecto** | <<NOMBRE_PROYECTO>> |
| **Propósito** | Plan maestro: iniciación + fases SDLC aplicables + tareas reemplazando deliverables en fases 4-7 |
| **Consolida** | PRE_HANDOFF_INICIACION · FASES_APLICABLES · PRE_HANDOFF_IMPLEMENTACION |
| **Estado** | ✅ Listo para revisión PM |

---

## ÍNDICE

1. Jerarquía y contexto
2. Fase de Iniciación (pre-SDLC)
3. Fases SDLC aplicables
4. Resumen ejecutivo
5. Siguiente paso

---

## 1. JERARQUÍA Y CONTEXTO

### 1.1 Jerarquía (Modelo Dinámico V3)

```
<<PROYECTO>> (Project)
  └── R1 (Release)
        └── Iniciación (pre-SDLC) + N Fases SDLC
              └── Deliverables / Tareas
                    └── Artefactos (docs, código, tests, deploy)
```

### 1.2 Contexto del proyecto

| Aspecto | Valor |
|---------|-------|
| Tipo | <<descripción breve del tipo>> |
| Stack | <<stack tecnológico>> |
| Infra | <<infraestructura>> |
| Integraciones | <<sistemas upstream/downstream>> |
| SLA crítico | <<si aplica>> |

### 1.3 Totales maestros

| Bloque | Unidades | Horas | Fuente |
|--------|---------:|------:|--------|
| Iniciación (pre-SDLC) | <<N>> tareas | <<N>>h | §2 |
| Fases 0-3B (docs/design) | <<N>> deliverables + <<N>> tareas | <<N>>h | §3 |
| Fases 4-7 (implementación) | <<N>> tareas | <<N>>h | §3 |
| **TOTAL proyecto** | **<<N>> tareas + <<N>> deliverables** | **<<N>>h** | |

---

## 2. FASE DE INICIACIÓN DEL PROYECTO (pre-SDLC)

**<<N>> tareas · <<N>>h** antes de arrancar Phase 0 Discovery.

### 2.1 Resumen por categoría

| Categoría | Tareas | Horas |
|-----------|-------:|------:|
| A. VTT Setup | <<N>> | <<N>>h |
| B. Repository Setup | <<N>> | <<N>>h |
| C. VM Configuration | <<N>> | <<N>>h |
| D. Agent Team Setup | <<N>> | <<N>>h |
| E. Tooling Setup | <<N>> | <<N>>h |
| F. Documentation | <<N>> | <<N>>h |
| G. Kickoff | <<N>> | <<N>>h |

### 2.2 Detalles por categoría

<<Copiar tablas del PRE_HANDOFF_INICIACION>>

### 2.3 Mapeo INIT → MEM

<<tabla de mapeo>>

---

## 3. FASES SDLC APLICABLES

### 3.1 FASE 0 · DISCOVERY

**Entregables aplicables:** <<N>> de 22 · **Tareas VTT:** <<N>> · **Horas:** <<N>>h

#### 3.1.1 Deliverables

<<listar deliverables por subfase>>

#### 3.1.2 Tareas VTT

| Task | Título | Delivery | Rol | Horas | Produce |
|------|--------|----------|-----|------:|---------|
| <<MEM-XXX>> | <<título>> | <<delivery>> | <<rol>> | <<N>> | <<deliverables>> |

### 3.2 FASE 1 · PLANNING

<<estructura igual>>

### 3.3 FASE 2 · ANALYSIS

### 3.4 FASE 3A · DESIGN UX/UI

### 3.5 FASE 3B · DESIGN TECHNICAL

### 3.6 FASE 4 · DEVELOPMENT

> **Deliverables reemplazados por tareas de implementación.** Los <<N>> deliverables aplicables son producidos por las <<N>> tareas abajo detalladas.

#### 3.6.1 S01 · <<nombre>>

<<tabla de tareas>>

#### 3.6.2 S02 · <<nombre>>

<<tabla>>

... (repetir para cada sub-sprint)

#### 3.6.N Mapeo Tareas → Deliverables SDLC Fase 4

| Subfase SDLC | Deliverables aplicables | Tareas VTT que los producen |
|--------------|-------------------------|------------------------------|
| 4.X <<nombre>> | <<items>> | <<MEM-XXX..MEM-YYY>> |

### 3.7 FASE 5 · TESTING

> **Deliverables reemplazados por tareas.**

<<tabla de tareas>>

### 3.8 FASE 6 · DEPLOY

> **Deliverables reemplazados por tareas.**

<<tabla de tareas>>

### 3.9 FASE 7 · OPERATIONS

<<tabla de tareas (mix docs + implementación)>>

---

## 4. RESUMEN EJECUTIVO

### 4.1 Totales maestros

| Bloque | Tareas | Horas | Deliverables |
|--------|-------:|------:|-------------:|
| Iniciación (pre-SDLC) | <<N>> | <<N>> | — |
| Fase 0 Discovery | <<N>> | <<N>> | <<N>> |
| Fase 1 Planning | <<N>> | <<N>> | <<N>> |
| Fase 2 Analysis | <<N>> | <<N>> | <<N>> |
| Fase 3A Design UX/UI | <<N>> | <<N>> | <<N>> |
| Fase 3B Design Technical | <<N>> | <<N>> | <<N>> |
| Fase 4 Development | <<N>> | <<N>> | <<N>> (producidos por tareas) |
| Fase 5 Testing | <<N>> | <<N>> | <<N>> (producidos por tareas) |
| Fase 6 Deploy | <<N>> | <<N>> | <<N>> (producidos por tareas) |
| Fase 7 Operations | <<N>> | <<N>> | <<N>> (producidos por tareas) |
| **TOTAL** | **<<N>> tareas** | **<<N>>h** | **<<N>> deliverables** |

### 4.2 Resumen por rol

| Rol | Tareas | Horas |
|-----|-------:|------:|
| PM | <<N>> | <<N>>h |
| PJM | <<N>> | <<N>>h |
| TL | <<N>> | <<N>>h |
| SA | <<N>> | <<N>>h |
| AR | <<N>> | <<N>>h |
| DB | <<N>> | <<N>>h |
| BE | <<N>> | <<N>>h |
| DL | <<N>> | <<N>>h |
| UX | <<N>> | <<N>>h |
| FE | <<N>> | <<N>>h |
| QA | <<N>> | <<N>>h |
| DO | <<N>> | <<N>>h |
| **TOTAL** | **<<N>>** | **<<N>>h** |

### 4.3 Hitos críticos

| Hito | Bloquea | Fase |
|------|---------|------|
| Iniciación completa | Phase 0 Discovery | pre-SDLC |
| <<hito DL>> | <<FE arranque>> | 3A → 4 |
| <<hito S01>> | <<backend posterior>> | 4 |
| <<Testing aprobado>> | Deploy | 5 → 6 |
| <<Deploy en prod>> | Operations | 6 → 7 |

### 4.4 Bloqueos activos (pre-arranque)

| # | Bloqueo | Resolver antes de |
|---|---------|-------------------|
| 1 | <<bloqueo>> | <<fase>> |

---

## 5. SIGUIENTE PASO

Con este consolidado:

1. **PM revisa y aprueba** el plan completo
2. **PM ejecuta PATCH en VTT** (actualizar horas + reassignments + metadata)
3. **PM emite HO formal al PJM** con este consolidado + pre-handoffs como anexos
4. **PJM genera BRIEFs downstream** por rol/sprint
5. **Kickoff call** una vez iniciación esté en ≥80%

---

**Documento:** CONSOLIDADO_<<PROYECTO>>.md
**Versión:** 1.0
**Estado:** ✅ Listo para revisión PM
**Fecha:** <<YYYY-MM-DD>>

---

**PM — <<Nombre>>**

---

**Template source:** `TEMPLATE_CONSOLIDADO_V1.0.md`
**Proceso asociado:** `09_PROCESO_CIERRE_PM_HANDOFF_PJM.md` (paso 5)
