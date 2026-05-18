# TEMPLATE — CIERRE PM + HANDOFF OPERATIVO PJM

> **Cómo usar este template:**
> 1. Copiar a `01-PM/CIERRE_PM_HANDOFF_PJM_<PROYECTO>.md` (o equivalente)
> 2. Reemplazar todos los placeholders `<<...>>` con valores reales
> 3. Llenar tablas según tu proyecto
> 4. Validar gates del `09_PROCESO_CIERRE_PM_HANDOFF_PJM.md` §6 antes de firmar
> 5. Borrar este bloque `>` antes de emitir

---

# CIERRE PM + HANDOFF OPERATIVO PJM — <<NOMBRE_PROYECTO>>

| Campo | Valor |
|-------|-------|
| **Documento** | CIERRE_PM_HANDOFF_PJM_<<PROYECTO>>.md |
| **Versión** | 1.0.0 |
| **Fecha** | <<YYYY-MM-DD>> |
| **Fase SDLC** | 02-Analysis → Cierre · 04-Development → Handoff |
| **Autor** | PM (<<NOMBRE_PM>>) |
| **Destinatario** | PJM (Project Manager) |
| **Proyecto** | <<NOMBRE_PROYECTO>> (`<<PROJECT_UUID>>`, key <<PROJECT_CODE>>) |
| **Estado** | ✅ CERRADO — Listo para ejecución |

---

## PARTE I: CIERRE PM DEL ANÁLISIS

### 1. DOCUMENTOS CONSUMIDOS

| # | Documento | Versión | Autor | Estado |
|---|-----------|---------|-------|--------|
| 1 | <<SPEC principal>> | <<vX.Y>> | PM + SA | ✅ Aprobado PM <<fecha>> |
| 2 | <<Metodología>> | <<vX.Y>> | PM | ✅ Vigente |
| 3 | <<Addendum(s)>> | <<vX.Y>> | PM | ✅ Integrado al SPEC |
| 4 | FASES_APLICABLES_<<PROYECTO>>.md | X.0 | PM | ✅ N deliverables aplicables |
| 5 | CONSOLIDADO_<<PROYECTO>>.md | X.0 | PM | ✅ Plan maestro |
| 6 | <<Reviews técnicas AR/DB/TL>> | X.0 | AR/DB/TL | ✅ Integradas |
| ... | ... | ... | ... | ... |

---

### 2. DECISIONES PM FINALES (<<N>> FROZEN)

Todas las decisiones están **CONGELADAS**. No se reabren.

#### 2.1 Arquitectura R1 (D-<<PFX>>-01 a D-<<PFX>>-NN) — <<N>> decisiones

| ID | Decisión |
|----|----------|
| D-<<PFX>>-01 | <<decisión arquitectural principal>> |
| D-<<PFX>>-02 | <<decisión 2>> |
| ... | ... |

#### 2.2 Revisión AR (D-<<PFX>>-NN a D-<<PFX>>-NN) — <<N>> decisiones

| ID | Decisión |
|----|----------|
| ... | ... |

#### 2.3 Correcciones AR (si aplica) — <<N>> decisiones

#### 2.4 Revisión TL / DB (si aplica) — <<N>> decisiones

#### 2.5 Integración Cross-Service (D-INT-XX) — <<N>> decisiones

| ID | Decisión | Origen |
|----|----------|--------|
| D-INT-01 | <<decisión>> | <<sistema upstream>> |
| ... | ... | ... |

---

### 3. CORRECCIONES INCORPORADAS (<<N>>)

Todas integradas al SPEC v<<X.Y>>.

| Origen | Código | Corrección |
|--------|--------|------------|
| AR | AR-OBS-01 | <<descripción breve>> |
| DB | DB-OBS-01 | <<descripción>> |
| TL | TL-XX | <<descripción>> |
| PM | Punto N | <<descripción>> |
| ADDENDUM | INT-XX | <<descripción>> |
| ... | ... | ... |

---

### 4. LIMITACIONES R1 DOCUMENTADAS

| # | Limitación | Fase resolución |
|---|------------|-----------------|
| LIM-01 | <<limitación 1>> | R2 / R3 / R1 aceptado |
| LIM-02 | <<limitación 2>> | <<fase>> |
| ... | ... | ... |

---

### 5. REASSIGNMENTS APROBADOS (si aplica)

| Task | Título | Fase | Plan original | Aprobado PM | Razón |
|------|--------|------|---------------|-------------|-------|
| <<MEM-XXX>> | <<título>> | <<fase>> | <<rol original>> | ✅ <<rol nuevo>> | <<razón>> |

---

### 6. VEREDICTO PM

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║   ✅ ANÁLISIS CERRADO — APROBADO PARA EJECUCIÓN                          ║
║                                                                           ║
║   <<N>> decisiones PM congeladas                                         ║
║   <<N>> correcciones incorporadas al SPEC                                ║
║   <<N>> limitaciones R1 documentadas                                     ║
║   <<N>> reassignments aprobados                                          ║
║   0  bloqueos pendientes                                                  ║
║   0  inconsistencias abiertas                                             ║
║                                                                           ║
║   Alcance R1:                                                             ║
║   · <<N>> tablas principales + <<N>> catálogos                           ║
║   · <<N>> endpoints API R1                                               ║
║   · <<N>> pantallas UI (si aplica)                                       ║
║   · <<N>> fuentes/integraciones                                          ║
║                                                                           ║
║   Plan maestro:                                                           ║
║   · Iniciación (pre-SDLC): <<N>> tareas · <<N>>h                         ║
║   · Fases SDLC 0-7:        <<N>> tareas · <<N>>h                         ║
║   · <<N>> deliveries  ·  <<N>> deliverables aplicables                   ║
║   · TOTAL: <<N>> tareas · <<N>>h                                         ║
║                                                                           ║
║   El paquete está listo para ejecución operativa vía PJM.                ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

---

## PARTE II: HANDOFF OPERATIVO PARA PJM

### 7. ALCANCE FINAL R1

#### 7.1 Tablas principales + catálogos

**Tablas principales:** <<listar>>

**Catálogos:** <<listar>>

#### 7.2 Endpoints R1 (<<N>>)

| # | Método | Ruta | Auth | Consumidor |
|---|--------|------|------|------------|
| 1 | <<VERB>> | <<ruta>> | <<auth>> | <<consumidor>> |
| ... | ... | ... | ... | ... |

#### 7.3 UI Standalone (si aplica)

| Prioridad | Pantalla | Ruta |
|-----------|----------|------|
| P0 | <<pantalla>> | <<ruta>> |
| ... | ... | ... |

#### 7.4 Infraestructura

| Recurso | Valor |
|---------|-------|
| VM | `<<IP>>` |
| Puertos | API <<port>> · UI <<port>> |
| BD | `<<nombre>>` |
| Cache/Redis | <<config>> |
| Storage | `<<path>>` |
| Red Docker | `<<network>>` |

#### 7.5 Integraciones cross-service

| Consumidor | Endpoint consumido | Cuándo |
|------------|-------------------|--------|
| <<sistema>> | <<endpoint>> | <<trigger>> |
| ... | ... | ... |

#### 7.6 Diferido a R2+

Ver §4 (LIM-XX).

---

### 8. FASE DE INICIACIÓN DEL PROYECTO (pre-SDLC)

**<<N>> tareas · <<N>>h** antes de arrancar Phase 0.

#### 8.1 Resumen por categoría

| Categoría | Tareas | Horas | MEM original |
|-----------|-------:|------:|--------------|
| A. VTT Setup | <<N>> | <<N>>h | <<MEM-XXX>> |
| B. Repository Setup | <<N>> | <<N>>h | <<MEM-XXX>> |
| C. VM Configuration | <<N>> | <<N>>h | <<MEM-XXX>> |
| D. Agent Team Setup | <<N>> | <<N>>h | <<MEM-XXX>> |
| E. Tooling Setup | <<N>> | <<N>>h | <<MEM-XXX>> |
| F. Documentation | <<N>> | <<N>>h | <<MEM-XXX>> |
| G. Kickoff | <<N>> | <<N>>h | <<MEM-XXX>> |

Ver detalle en `PRE_HANDOFF_INICIACION_<<PROYECTO>>.md`.

#### 8.2 Estado actual (bloqueos pre-arranque)

| Item | Estado | Acción |
|------|--------|--------|
| <<item>> | ✅ / 🟡 / 🔴 | <<acción>> |

---

### 9. SECUENCIA DE FASES SDLC

```
╔════════════════════════════════════════════════════════════════════════╗
║ FASE 0: INICIACIÓN (pre-SDLC)  ·  <<N>> tareas  ·  <<N>>h              ║
╠════════════════════════════════════════════════════════════════════════╣
║ FASE A: FUNDACIÓN (Discovery → Planning → Analysis)                    ║
╠════════════════════════════════════════════════════════════════════════╣
║  Discovery · <<N>> tareas · <<N>>h                                      ║
║  Planning  · <<N>> tareas · <<N>>h                                      ║
║  Analysis  · <<N>> tareas · <<N>>h                                      ║
╠════════════════════════════════════════════════════════════════════════╣
║ FASE B: DISEÑO (paralelo UX/UI ↔ Technical)                            ║
║  Design UX/UI     · <<N>> tareas · <<N>>h · 🚨 <<hito>>                 ║
║  Design Technical · <<N>> tareas · <<N>>h                               ║
╠════════════════════════════════════════════════════════════════════════╣
║ FASE C: DESARROLLO (secuencial S01 → SNN)                              ║
║  <<detalle de sprints>>                                                 ║
╠════════════════════════════════════════════════════════════════════════╣
║ FASE D: DESARROLLO FRONTEND (si aplica, desbloqueado por hito DL)     ║
╠════════════════════════════════════════════════════════════════════════╣
║ FASE E: VALIDACIÓN · Testing · <<N>>h                                   ║
╠════════════════════════════════════════════════════════════════════════╣
║ FASE F: LANZAMIENTO · Deploy <<N>>h · Operations <<N>>h                 ║
╚════════════════════════════════════════════════════════════════════════╝

TOTAL: <<N>> tareas · <<N>>h · <<N>> fases
```

**Paralelismo permitido:** <<describir>>

---

### 10. PLAN COMPLETO DE TAREAS POR FASE (con mapeo tarea → deliverables)

> **Nota metodológica crítica:** Cada tarea VTT puede producir **varios deliverables SDLC**. La columna "Produce" hace explícito ese mapeo para evitar ambigüedad.

#### 10.1 Fase 0 · Discovery (<<N>> tareas · <<N>>h · <<N>> deliverables)

| Task | Título | Delivery | Rol | Horas | Complexity | Produce (deliverables SDLC) |
|------|--------|----------|-----|------:|------------|------------------------------|
| <<MEM-XXX>> | <<título>> | <<delivery>> | <<rol>> | <<h>> | <<cmplx>> | <<0.X.Y, 0.X.Z, ...>> |

#### 10.2 Fase 1 · Planning (<<N>> tareas · <<N>>h · <<N>> deliverables)

<<tabla igual>>

#### 10.3 Fase 2 · Analysis

#### 10.4 Fase 3A · Design UX/UI

#### 10.5 Fase 3B · Design Technical

#### 10.6 Fase 4 · Development

##### S01 / S02 / ... UI-01 / ... (subsprints)

#### 10.7 Fase 5 · Testing

#### 10.8 Fase 6 · Deploy

#### 10.9 Fase 7 · Operations

#### 10.10 Resumen consolidado por rol

| Rol | Tareas VTT | Tareas INIT | Total | Horas VTT | Horas INIT | Total h |
|-----|-----------:|------------:|------:|----------:|-----------:|--------:|
| PM | <<N>> | <<N>> | <<N>> | <<N>> | <<N>> | <<N>> |
| ... | ... | ... | ... | ... | ... | ... |

---

### 11. DEPENDENCIAS POR ROL

#### 11.1 DO (DevOps)

| Prerequisito | Momento | Responsable |
|--------------|---------|-------------|
| <<prerequisito>> | <<antes de tarea>> | DO coordina |

#### 11.2 / 11.3 / ... por rol (DB, BE, DL, FE, QA, AR)

---

### 12. DEPENDENCIAS CRÍTICAS (<<N>>)

| From | To | Razón | Impacto |
|------|-----|-------|---------|
| INICIACION | <<task>> | <<razón>> | 🚨 CRÍTICO |
| <<task>> | <<task>> | <<razón>> | Alto / Medio |

---

### 13. RIESGOS Y MITIGACIONES

| # | Riesgo | Prob. | Impacto | Mitigación |
|---|--------|-------|---------|------------|
| R1 | <<riesgo>> | Baja/Media/Alta | Bajo/Medio/Alto | <<mitigación>> |

---

### 14. CHECKLIST PJM ANTES DE INICIAR

```
INICIACIÓN (pre-arranque):
[ ] PM ejecuta PATCH MEM-001..005 con horas actualizadas
[ ] PM aplica reassignments si aplica
[ ] PM ejecuta PATCH N tareas con metadata
[ ] PJM confirma distribución temporal

INFRAESTRUCTURA:
[ ] BD accesible desde contenedor
[ ] Redis accesible
[ ] Network Docker con DNS
[ ] Storage con permisos
[ ] SERVICE_KEY distribuida

VALIDACIÓN DE CONTRATO:
[ ] TL confirma lectura SPEC
[ ] AR confirma arquitectura sin bloqueos
[ ] DB confirma schema aplicable
[ ] BE confirma contrato de endpoints

ASIGNACIÓN EN VTT:
[ ] N tareas con metadata completa
[ ] Dependencias críticas registradas
[ ] Deliveries vinculados
[ ] Hitos marcados

DOCUMENTOS DE REFERENCIA:
[ ] <<listar docs de §1>>
```

---

### 15. CRITERIO DE ÉXITO

<<PROYECTO>> R1 se considera **COMPLETADO** cuando:

1. ✅ <<criterio verificable 1>>
2. ✅ <<criterio verificable 2>>
3. ✅ <<criterio verificable 3>>
...
N. ✅ <<criterio verificable N>>

---

### 16. HANDOFFS DOWNSTREAM (el PJM genera)

**Regla:** Los HOs se generan para el **líder de área** o para **roles con responsabilidad de decisión**.

| Líder del área | Cubre |
|---------------|-------|
| TL | BE, DB, DO, FE (todo lo de código) |
| DL | UX (todo lo de diseño) |
| PM / PJM / SA / AR / QA | Cada uno por separado |

**Estructura: <<N>> HOs secuenciales, uno por fase.**

| # | HO | Fase | Seguimiento | Tareas | Horas |
|---:|----|------|-------------|-------:|------:|
| 1 | HO_INICIACION_<<PROYECTO>>.md | Pre-SDLC | PJM | <<N>> | <<N>>h |
| 2 | HO_FASE_0_DISCOVERY_<<PROYECTO>>.md | Fase 0 | PM | <<N>> | <<N>>h |
| 3 | HO_FASE_1_PLANNING_<<PROYECTO>>.md | Fase 1 | PM+PJM | <<N>> | <<N>>h |
| ... | ... | ... | ... | <<N>> | <<N>>h |

### 16.1 INDEX / SEED de tareas

Para la carga masiva a VTT sin retrabajo, existe:

`TASK_INDEX_SEED_<<PROYECTO>>.md` — 116+ tareas con todos los campos del sistema VTT.

---

### 17. FIRMAS

| Rol | Nombre | Firma | Fecha |
|-----|--------|-------|-------|
| **PM** | <<Nombre>> | **✅ APROBADO** | <<fecha>> |
| PJM | (pendiente) | ⬜ | — |
| TL | (pendiente) | ⬜ | — |
| ... | ... | ⬜ | — |

---

**Documento:** CIERRE_PM_HANDOFF_PJM_<<PROYECTO>>.md
**Versión:** 1.0.0
**Estado:** ✅ CERRADO — Listo para ejecución
**Fecha:** <<YYYY-MM-DD>>

**Consolida:**
- PRE_HANDOFF_INICIACION_<<PROYECTO>>.md
- FASES_APLICABLES_<<PROYECTO>>.md
- CONSOLIDADO_<<PROYECTO>>.md

**Referencias técnicas:**
- <<SPEC>>
- <<Metodología>>
- <<Addendum>>

---

**PM — <<Nombre>>**
<<Organización>>

---

**Template source:** `TEMPLATE_CIERRE_PM_HANDOFF_PJM_V1.0.md`
**Proceso asociado:** `09_PROCESO_CIERRE_PM_HANDOFF_PJM.md` (paso 6)
