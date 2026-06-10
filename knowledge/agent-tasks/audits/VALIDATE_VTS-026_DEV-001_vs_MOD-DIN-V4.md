# VALIDATE — VTS-026 PROTOCOL-DEV-001 vs Modelo Dinámico V4

| Campo | Valor |
|---|---|
| **Tarea VTT** | VTS-026 |
| **Tipo** | Reporte de validación (NO bumpea normativa) |
| **Branch** | `feature/VTS-026-validar-devlog-vs-mod-dinamico-v4` |
| **Fecha** | 2026-06-10 |
| **Autor** | TW-OPS (`fe1b589c-7cf2-4779-82d4-b7ae536536ce`) |
| **Lead asignador** | LEAD_NPL (`3c45e61c-b3fa-4291-b08e-3f29cfe9f8b7`) — instrucciones en BRIEF v2 (attachment `c1746c7d`) + dictamen PM (comment `9054851e`) |
| **Materializa bump** | NO — el bump del Protocol DEV-001 v1.0.0 → v1.1.0 lo ejecuta **VTS-051** (depende de este reporte) |
| **Hijas insumo** | VTS-027 (Workflows), VTS-028 (Skills), VTS-029 (Scripts), VTS-049 (CARDs). VTS-050 cancelada como duplicada de VTS-029 |
| **Reporte previo** | `AUDIT_VTS-007_DEV-001.md` (2026-06-02) — auditoría de cobertura del paquete, ya `task_approved` |

---

## 1. Contexto y delta con VTS-007

### 1.1 Por qué este reporte existe

El Módulo C "Devlog" del Modelo Dinámico V4 está declarado en `GUIA_FEATURES_MODELO_DINAMICO_V4.md` (2026-06-04) §4 con 4 features:

| Feature | Estado declarado por PM | Necesidad |
|---|---|---|
| Devlog Entries | ✅ documentada en FEATURE v1.1 + GUIA_DEVLOG_FINDINGS | Validar empíricamente |
| Resolución de Entries | ✅ documentada en FEATURE v1.1 §4 | Validar empíricamente |
| Diferir Entry a otra Fase | ✅ documentada (D-66) | Validar empíricamente |
| Crear Fix Task desde Entry | ⚠️ Reconciliar (legacy vs findings→issue / Sprint DEUDA) | Recomendación A/B/C |

VTS-026 es la tarea que cierra esa validación + reconciliación con dictamen técnico para 4 tareas hijas (VTS-027/028/029/049).

### 1.2 Delta vs VTS-007 (ya approved)

| Aspecto | VTS-007 (2026-06-02, approved) | VTS-026 (este, 2026-06-09/10) |
|---|---|---|
| Doc canónica de referencia | `FEATURE_DEVLOG_LIFECYCLE.md` **v1.0** (2026-05-21) | `FEATURE_DEVLOG_LIFECYCLE.md` **v1.1** (2026-06-04) + `GUIA_DEVLOG_FINDINGS.md` (2026-06-04) + `GUIA_FEATURES_MODELO_DINAMICO_V4.md` (2026-06-04) |
| Tipo de análisis | Auditoría de cobertura (qué falta) | Validación de conformidad (qué miente / qué cambió) |
| Output | Plan de FASE C con 4 commits (Workflows + CARDs + cross-link + INVENTARIO) — sin ejecutar | Dictamen técnico A/B/C + insumo concreto por tarea hija |
| Hallazgos clave | G1 (3 Workflows faltantes), G2 (Cards faltantes), G3 (cross-link DEV→ASG §5.4/§5.4.bis incompleto) | T2 (defer BY-DESIGN), T3 (fix-task endpoint inexistente), BUG-DEV-003 (status no se mueve), 12 vs 7 categorías, drift IP/SERVICE_KEY |
| Modifica normativa | Plan para sí (no ejecutado) | NO — solo reporte; bump efectivo en VTS-051 |

**Conclusión:** VTS-007 dijo *qué hace falta agregar*. VTS-026 dice *qué hace falta corregir*. Son complementarios, no solapados.

### 1.3 Cambio de scope durante ejecución (issue 600d2bde + dictamen PM)

Durante la FASE A, levanté issue `type=question` (`600d2bde`) reportando 8 inconsistencias del MSG inicial. LEAD_NPL respondió en 2 rondas (comments `a758a638` y `824d7a17`) y subió BRIEF v2 (attachment `c1746c7d`) que reemplaza el alcance original. Posteriormente PM (vía LEAD_NPL en comment `9054851e`) emitió dictamen agregando:

- **T2** — `resolution=null` en `deferred` es **BY-DESIGN** (no es bug del backend, línea 227 del service code lo hace explícito).
- **T3** — endpoint `create-fix-task` **NO existe** en prod (flujo manual de 3 pasos).
- VTS-050 cancelada como duplicada de VTS-029.
- VTS-026 NO modifica `DEV-001.md`; bump efectivo en VTS-051 nueva.

Issue `600d2bde` cerrado con `isResolved=true` antes de arrancar FASE B (PROTOCOL-ASG-001 §5.4.bis.6).

---

## 2. Validación de las 3 features ✅ del Módulo C

Cada feature se validó contra `api.vttagent.com` con `curl` real. Resultados completos en Anexo A.

### 2.1 Feature: Devlog Entries

**Documentación canónica:** `FEATURE_DEVLOG_LIFECYCLE` v1.1 §1-§3 + `VTT.PROTOCOL-DEV-001` v1.0.0 §5.1 + Skills `DEV-001` (decision), `DEV-002` (observation).

#### 2.1.1 Endpoints validados

| Test | Endpoint | Resultado |
|---|---|---|
| Crear 1 entry | `POST /api/tasks/:taskId/devlog` body objeto directo | ✅ HTTP 200 — entry creada con `status: pending` |
| Crear N entries batch | `POST /api/tasks/:taskId/devlog-entries` body `{entries:[]}` | ✅ HTTP 200 — `data.created: 3` + array de entries |
| Listar entries | `GET /api/tasks/:taskId/devlog` | ✅ HTTP 200 — array de entries con shape completo |
| Listar por fase | `GET /api/phases/:phaseId/devlog-summary` | ✅ HTTP 200 — `{phaseId, total, canProceed, byStatus, bySeverity, byCategory, blockers[]}` |
| `categoryCode` inválido | POST con `categoryCode:"xyz"` | ✅ HTTP 400 `INVALID_CATEGORY "Categoria 'xyz' no existe"` |

**Conclusión:** los endpoints funcionan exactamente como documenta el Protocol DEV-001 v1.0.0 §6.4 + Skills DEV-001/002.

#### 2.1.2 Hallazgos contra la documentación

**H-1 (alto)** — **Catálogo vivo tiene 12 categorías activas; Protocol/Skills documentan solo 7.**

`GET /api/catalogs/devlog-categories` retorna:

| code | severityLevels | Documentada en paquete DEV-001? |
|---|---|---|
| `issue` | critical/high/medium/low | ✅ Protocol §3.1 + Feature v1.1 §3 |
| `tech_debt` | critical/high/medium/low | ✅ ídem |
| `decision` | **`[]`** (sin severity) | ✅ ídem |
| `blocker` | critical/high/medium/low | ✅ ídem |
| `risk` | critical/high/medium/low | ✅ ídem |
| `testing_note` | critical/high/medium/low | ✅ ídem |
| `observation` | **`[]`** (sin severity) | ✅ ídem |
| `question` | high/medium/low | ❌ **No documentada** |
| `dependency` | high/medium | ❌ **No documentada** |
| `improvement` | medium/low | ❌ **No documentada** |
| `feedback` | high/medium/low | ❌ **No documentada** |
| `brand_issue` | critical/high/medium | ❌ **No documentada** |

Impacto: agentes que solo leen el paquete normativo no saben que existen `question`/`dependency`/`improvement`/`feedback`/`brand_issue` y pierden trazabilidad o las registran como `observation` genérica (anti-pattern).

Recomendación VTS-051 (bump): tabla completa de 12 codes con severityLevels permitidos + criterio "cuándo usar cada una" alineado con D-61 (devlog/finding/issue/TI).

**H-2 (medio)** — **`severity` en categorías con `severityLevels:[]` se normaliza silenciosamente a null.**

Test: POST con `categoryCode:"decision", severity:"high"` → respuesta `severity: null` (descartado). No retorna warning ni HTTP 400.

Skills DEV-001/002 dicen: *"severity enum no-null obligatorio. Default `low`."* — **incorrecto**. El catálogo declara `severityLevels:[]` para `decision` y `observation`, el backend ignora el valor enviado.

Impacto: agentes que confían en la doc Skill pueden creer que están marcando severidad pero el backend la descarta. Si combinado con un agente que registra `observation` con `severity:high` esperando que bloquee el review gate → **no bloquea** (`canProceedToReview:true` con high entries que figuran como `severity:null`).

Recomendación VTS-028 (bump Skills DEV-001/DEV-002): documentar que `severity` se ignora para `decision`/`observation`; omitir el campo en payload. Recomendación derivada para backend (eventualmente VTS-051 si toca): rechazar 400 si payload trae severity en categoría sin severityLevels.

### 2.2 Feature: Resolución de Entries (lifecycle)

**Documentación canónica:** `FEATURE_DEVLOG_LIFECYCLE` v1.1 §4 + `VTT.PROTOCOL-DEV-001` v1.0.0 §4 + Skill `DEV-004` (lifecycle) + Skill `DEV-003` (edit).

#### 2.2.1 Endpoints y enums validados

| Test | Endpoint | Resultado |
|---|---|---|
| Lifecycle estricto | `PATCH /api/tasks/:taskId/devlog/:entryId/status` con body `{status, resolution?, deferredToPhaseId?}` | ✅ Funciona — set completo `acknowledged/in_progress/resolved/wont_fix/deferred` |
| Edit body genérico | `PATCH /api/tasks/:taskId/devlog/:entryId` con campos sueltos | ✅ Funciona para `title/description/severity` |
| Edit body con `status:"acknowledged"` | `PATCH /api/tasks/:taskId/devlog/:entryId` | ✅ HTTP 400 `"Invalid enum value. Expected 'open' \| 'resolved' \| 'deferred'"` — confirma **set reducido DEV-003** |
| DELETE entry | `DELETE /api/tasks/:taskId/devlog/:entryId` | ✅ HTTP 204 sin body |

**Lifecycle 6 estados confirmados:** `pending → acknowledged → in_progress → resolved/wont_fix/deferred`. Estados terminales irreversibles (`ENTRY_ALREADY_FINAL` 400). Skill DEV-004 v1.0 alineada con el comportamiento real.

#### 2.2.2 Hallazgos contra la documentación

**H-3 (alto) — BUG-CONSISTENCIA en DEV-003 endpoint body al transicionar a `resolved`.**

Test empírico:
```
PATCH /api/tasks/VTS-026/devlog/71cbe36a-.../...
body: {"status":"resolved", "resolution":"TEST"}
```

Respuesta del backend: HTTP 200 con entry actualizada, donde:
- `status: "pending"` (NO se movió)
- `resolvedAt: "2026-06-10T04:49:15.480Z"` (sí se seteó)
- `resolvedBy: "fe1b589c-..."` (sí se seteó)
- `resolution: "TEST: ..."` (sí se persistió)

**El entry queda en estado inconsistente:** aparenta resuelta (`resolvedAt/resolvedBy/resolution` poblados) pero `status: pending` sigue activo. Esto puede engañar al review gate y al TL en code review.

Skill DEV-003 v1.0 §"Errores comunes" solo advierte que `resolvedAt` queda null si se usa DEV-003 en vez de DEV-004; no detecta este caso (donde `resolvedAt` SÍ se setea pero `status` no cambia).

Recomendación VTS-051 derivada:
- **Opción A (preferida)** — Backend rechaza 400 si body de DEV-003 trae `status: resolved` o `status: deferred`; forzar uso de PATCH `/status` (DEV-004) para cualquier transición de lifecycle.
- **Opción B** — Backend acepta pero también actualiza `status` consistentemente con `resolvedAt/resolvedBy` seteados.

Recomendación VTS-028 (bump Skill DEV-003): agregar **§Error CRÍTICO**: "Si pasás `status` en body, el `status` NO cambia pero `resolvedAt/resolvedBy/resolution` SÍ se setean → entry inconsistente. Usar SIEMPRE DEV-004 (PATCH /status) para lifecycle."

Recomendación VTS-051 (Protocol DEV-001 v1.1.0): nueva regla **R13** — "DEV-003 (PATCH body genérico) NUNCA para cambiar `status`. Para cualquier transición de lifecycle usar exclusivamente DEV-004 (PATCH /status)."

### 2.3 Feature: Diferir Entry a otra Fase (D-66)

**Documentación canónica:** `FEATURE_DEVLOG_LIFECYCLE` v1.1 §4.1 + `VTT.PROTOCOL-DEV-001` v1.0.0 R8 + Skill `DEV-004` Caso 5.

#### 2.3.1 Validación empírica T2

Test diseñado para confirmar dictamen PM (T2: `resolution=null` en `deferred` es BY-DESIGN):

**Request:**
```bash
PATCH /api/tasks/VTS-026/devlog/0e024547-.../status
body: {
  "status": "deferred",
  "resolution": "TEST: deberia ser limpiada a null por backend si T2 es BY-DESIGN",
  "deferredToPhaseId": "67045d1f-b0d7-4990-b96b-31cd8232cb32"
}
```

**Response del backend:**
```json
{
  "data": {
    "id": "0e024547-...",
    "status": "deferred",
    "resolution": null,
    "resolvedAt": null,
    "resolvedBy": null,
    "deferredToPhaseId": "67045d1f-...",
    "description": "Entry de prueba creada por TW-OPS..." // ← PRESERVADO
  }
}
```

✅ **T2 CONFIRMADO empíricamente:**
- Backend limpia `resolution` a `null` aunque se haya enviado contenido textual.
- Backend limpia `resolvedAt` y `resolvedBy` a `null`.
- Backend preserva `description` original del entry.
- Backend preserva `deferredToPhaseId` enviado.

Comportamiento coincide con Skill DEV-004 §"Comportamiento automático del backend" y FEATURE v1.1 §4.1 ("`deferred` ya NO significa pospuesto ambiguo. Significa TRANSFERIDO").

#### 2.3.2 Workaround documentado (dictamen PM)

Si se necesita preservar contexto del "a dónde fue transferido" (ej. "Elevado a TD-CORE-003"), las opciones son:

| Workaround | Cómo | Cuándo |
|---|---|---|
| 1. Usar `description` original | Al crear el entry, escribir el destino en el `description` ANTES de transicionar a deferred | Si el destino se conoce al crear |
| 2. Postear comment en la tarea | `POST /api/tasks/:id/comments` con referencia al destino + `entryId` | Si el destino se decide al diferir (caso típico) |
| 3. `fixTaskId` (campo) | Si el destino es una tarea, setear `fixTaskId` al diferir (campo se preserva) | Si destino es tarea concreta del backlog |

#### 2.3.3 Hallazgos contra la documentación

**H-4 (medio)** — **Protocol DEV-001 v1.0.0 R8 + Skill DEV-004 §"Comportamiento automático" lo dicen pero no explican el porqué semántico ni dan workaround**.

- Skill DEV-004 §"Caso 5" muestra que `deferred` limpia `resolution`/`resolvedAt`/`resolvedBy` pero no marca esto como hallazgo BY-DESIGN ni provee workaround.
- Protocol DEV-001 v1.0.0 R8 dice `deferredToPhaseId` obligatorio en `deferred`, pero no dice que `resolution` se limpia.
- FEATURE v1.1 §4.1 ya resignifica `deferred = TRANSFERIDO` y exige referencia obligatoria — pero como va a `resolution` que se limpia, la regla de la feature **es operativamente imposible** sin workaround.

Recomendación VTS-051 (Protocol DEV-001 v1.1.0): documentar T2 BY-DESIGN explícitamente + workaround de 3 opciones + regla **R14**: "Para preservar referencia al destino en `deferred`, usar `description` original o comment en la tarea — NUNCA confiar en `resolution` (se limpia BY-DESIGN)."

Recomendación VTS-028 (bump Skill DEV-004 §Caso 5): mismo agregado de workaround.

### 2.4 Resumen validación features ✅

| Feature | Status | Brechas críticas detectadas |
|---|---|---|
| Devlog Entries | ✅ Funciona | H-1 (12 vs 7 categorías), H-2 (severity ignorada silenciosamente) |
| Resolución de Entries | ✅ Funciona | H-3 (BUG-CONSISTENCIA DEV-003 endpoint body con status) |
| Diferir Entry a otra Fase | ✅ Funciona — T2 BY-DESIGN confirmado | H-4 (falta workaround documentado para FEATURE v1.1 §4.1) |

**Veredicto general de validación:** las 3 features ✅ están **operativamente correctas en el backend**. El paquete normativo DEV-001 v1.0.0 las cubre **mecánicamente** pero **NO refleja**: (a) la matriz de 4 entidades + D-61..D-66 de FEATURE v1.1, (b) las 5 categorías nuevas del catálogo vivo, (c) bugs/comportamientos no-obvios (H-2, H-3, H-4). Material para VTS-051 (bump Protocol) + VTS-028 (bump Skills).

---

## 3. Reconciliación: "Crear Fix Task desde Entry" (CA-2)

### 3.1 Estado actual

**En el paquete normativo DEV-001:**

- `VTT.PROTOCOL-DEV-001` v1.0.0 menciona `fixTaskId` como **campo del entry** (apunta a la tarea que cerró el devlog), NO como acción de **crear tarea correctiva**.
- Skills DEV-003 (§Campos editables) y DEV-004 (§Inputs, Caso 3) aceptan `fixTaskId` como input opcional/recomendado.
- **No existe Workflow, Skill ni Card que orqueste "crear tarea correctiva nueva desde un devlog entry".**

**En la doc del Modelo Dinámico V4:**

- `GUIA_FEATURES_MODELO_DINAMICO_V4` §4 marca esta feature como ⚠️ "Reconciliar: hoy se redirige a findings→issue (bug-de-scope) o finding→Sprint DEUDA. Decidir si este flujo legacy sobrevive o queda absorbido."
- `GUIA_DEVLOG_FINDINGS` §2.2 dictamen 1 dice: "AHORA — bug-de-scope mal clasificado: `resolved` 'Reclasificado como issue X' → POST /issues + correctiva en el sprint actual, tarea on-hold."

**En producción (confirmado T3 + tarea hermana VTS-029):**

- Endpoint `POST /api/tasks/:taskId/devlog/:entryId/create-fix-task` o equivalente **NO existe** (dictamen PM).
- VTS-029 ya tiene posteado blocker `high`: *"Endpoint POST /devlog/:id/fix-task no existe en producción — requiere decisión PM"* (verificado en `GET /api/phases/:id/devlog-summary` durante FASE B).

### 3.2 Hallazgo T3 confirmado: flujo manual de 3 pasos

Si se requiere asociar una tarea correctiva a un devlog entry, el flujo correcto es **manual**:

```
Paso 1: POST /api/phases/:phaseId/tasks
        body: { titulo, descripcion, ... }
        → respuesta: { data: { id: "VTS-XXX-nueva" } }

Paso 2: Capturar el taskId resultante (VTS-XXX / MS-XXX según proyecto)

Paso 3: PATCH /api/tasks/:taskIdPadre/devlog/:entryId/status
        body: {
          "status": "resolved",
          "fixTaskId": "VTS-XXX-nueva",
          "resolution": "Reclasificado como tarea correctiva <ID> — ver feed VTS-XXX-nueva"
        }
        → entry pasa a resolved con fixTaskId apuntando a la correctiva
```

**Este flujo NO tiene Workflow ni Skill propios hoy.** Si VTS-051 decide documentarlo, debe agregarlo como Workflow `VTT.WORKFLOW-DEV-001.004_crear_fix_task_desde_entry` o como sub-procedimiento en `VTT.WORKFLOW-DEV-001.002_editar_o_transicionar_entry`.

### 3.3 Distinción crítica (nota PM): trazabilidad vs bloqueo

Punto operativo más importante del dictamen PM:

| Necesidad | Mecanismo correcto | Resultado |
|---|---|---|
| **Solo trazabilidad post-hoc** (entry quedó cerrada, la tarea hija existe, queremos linkearlas) | Flujo manual T3 de 3 pasos (devlog `fixTaskId`) | Entry `resolved`, tarea padre sigue en `task_in_progress`/`task_in_review` sin cambios de status |
| **Bloqueo del padre con auto-resume** (padre debe pausar hasta que la correctiva cierre) | **Issue `type=bug` por ASG-001 §5.4** (NO devlog) | Padre → `task_on_hold`, hija con `sourceIssueId`, al cerrar hija → padre auto-resume a `previousStatus` |

**Nunca mezclar:**
- `fixTaskId` en devlog ≠ bloqueo. Es solo un link.
- `task_on_hold` ≠ devlog. Es Issue formal.

Esta distinción debe estar explícita en Protocol DEV-001 v1.1.0 (VTS-051) y en CARDs (VTS-049) — sin la distinción, agentes mezclan los dos flujos y rompen el modelo de bloqueo.

### 3.4 Recomendación A/B/C con justificación

| Opción | Significado | Recomendación |
|---|---|---|
| **A) Mantener flujo legacy** | Crear Workflow/Skill nuevo que orqueste el flujo T3 de 3 pasos como capacidad de primera clase | ❌ No |
| **B) Eliminar/absorber al flujo Issue de ASG-001** | Redirigir oficialmente: si bug-de-scope → Issue, si trazabilidad post-hoc → flujo manual T3 sin Workflow propio | ✅ **Recomendada** |
| **C) Híbrido** | Mantener flujo legacy para algunos casos + redirigir otros | ❌ No |

**Justificación de Opción B:**

1. **D-62 (registro único, prohibidos pares espejo)** — `FEATURE_DEVLOG_LIFECYCLE` v1.1 §0.2: "Cada cosa se registra UNA SOLA VEZ, en su entidad." Crear "Fix Task desde Entry" como capacidad propia duplicaría con Issue→correctiva de ASG-001 §5.4 (que YA existe y YA tiene Workflows/Skills).

2. **D-61 (matriz roles)** — `FEATURE_DEVLOG_LIFECYCLE` v1.1 §0.1: devlog = bitácora ("¿qué pasó?"); issue = bloqueo de scope ("¿qué impide cumplir los CAs?"). Una tarea correctiva nace de un bug-de-scope → es jurisdicción de Issue, no devlog. Mantener el flujo legacy en devlog viola la matriz.

3. **T3 confirmado** — endpoint dedicado no existe. Construir Workflow/Skill para un flujo manual de 3 pasos que ya tiene cobertura por Issue es duplicar esfuerzo y mantener doble fuente de verdad.

4. **`GUIA_DEVLOG_FINDINGS` §2.2 dictamen 1 ya documenta la redirección oficial:** "AHORA — bug-de-scope mal clasificado: `resolved` 'Reclasificado como issue X' → POST /issues + correctiva en el sprint actual, tarea on-hold."

5. **Caso "solo trazabilidad" sigue cubierto** — `fixTaskId` ya existe como campo opcional en DEV-003/DEV-004. Documentar en Protocol v1.1.0 cómo usarlo (flujo manual T3) **sin** crear Workflow propio. Es un patrón de uso, no una capacidad nueva.

**Acción concreta para VTS-051 (bump Protocol DEV-001 v1.1.0):**

a. Agregar §5.5 "Crear Fix Task desde Entry — distinción trazabilidad vs bloqueo" con:
   - Tabla §3.3 de este reporte (trazabilidad vs bloqueo).
   - Flujo manual T3 documentado como "patrón de uso" (no como Workflow).
   - Referencia explícita a ASG-001 §5.4 (Issue `type=bug`) para casos de bloqueo.

b. NO crear Workflow `DEV-001.004` ni Skill `DEV-006`/`DEV-007` para "crear fix task". El campo `fixTaskId` se setea con DEV-004 (existente).

c. Actualizar `GUIA_FEATURES_MODELO_DINAMICO_V4` §4 cambiando estado de "Crear Fix Task desde Entry" de ⚠️ a ✅ con nota "Absorbida — ver Protocol DEV-001 §5.5 + ASG-001 §5.4".

---

## 4. Insumo concreto para tareas hijas (CA-4)

> **VTS-050 cancelada** como duplicada de VTS-029 (comment trazabilidad `c7a5ab0d`, movida a `task_cancelled`). NO la considero en este §4.

### 4.1 VTS-027 — Workflows DEV-001.001/.002/.003

VTS-007 ya identificó los 3 Workflows faltantes. Mi reporte agrega contenido obligatorio para cada uno basado en hallazgos FASE B:

| Workflow | Cubre | Inputs específicos del reporte |
|---|---|---|
| `WORKFLOW-DEV-001.001_crear_devlog_entry` | FASE 1 — agente crea entry durante ejecución | Debe documentar las 12 categorías vivas (H-1) + matriz D-61 para elegir devlog vs finding vs issue + tabla "cuándo usar cada categoría" |
| `WORKFLOW-DEV-001.002_editar_o_transicionar_entry` | FASE 3 — TL/agente edita o transiciona | Debe documentar BUG-CONSISTENCIA DEV-003 (H-3) + regla "para status SIEMPRE DEV-004" + flujo manual T3 para `fixTaskId` |
| `WORKFLOW-DEV-001.003_cerrar_entries_terminal_pre_aprobacion` | FASE 4 — TL+PM cierre sprint | Debe documentar T2 BY-DESIGN (H-4) + 3 workarounds para preservar referencia en `deferred` |

> **Sub-pregunta residual (de AUDIT_VTS-007 Q5):** alcance del `.003` — ¿FASE 4 cierre sprint (TL+PM) o FASE 3 task review (TL solo)? **Mi recomendación:** FASE 4 cierre sprint, manteniendo `cerrar_entries_terminal_pre_aprobacion` reinterpretando "pre_aprobacion" como "antes de aprobar el sprint en reporte M". Si VTS-027 decide otra cosa, dejar el verbo `cerrar_entries_terminal_pre_aprobacion_sprint` para que sea inambiguo.

### 4.2 VTS-028 — Skills DEV (bump existentes + decidir si crear nuevas)

**Fixes obligatorios a las 5 Skills existentes:**

| Skill | Fix |
|---|---|
| DEV-001 (decision) | §Variables del entorno: cambiar `$VTT_BASE_URL=http://77.42.88.106:3000` → `$VTT_BASE_URL=https://api.vttagent.com` (RULE-SEC-001). §Notas técnicas: documentar H-2 (severity ignorada para decision/observation). |
| DEV-002 (observation) | Idem DEV-001 (mismo drift IP + mismo H-2). |
| DEV-003 (edit) | Idem drift IP. §Error CRÍTICO nuevo: H-3 (BUG-CONSISTENCIA al pasar status en body — usar SIEMPRE DEV-004). |
| DEV-004 (lifecycle) | Idem drift IP. §Caso 5: agregar 3 workarounds del PM para preservar referencia en `deferred` (H-4 / T2). |
| DEV-005 (delete) | Idem drift IP. Sin otros cambios. |

**Skills nuevas — recomendación:**

- ❌ **NO crear** Skills DEV-006..010 una por cada categoría nueva (`question`/`dependency`/`improvement`/`feedback`/`brand_issue`) — viola **anti-pattern 1 de GUIA_AUTOR** (Skill específica del contexto).
- ✅ **Refactorizar** DEV-001 y DEV-002 a una sola Skill genérica `DEV-001_crear_devlog_entry` con `categoryCode` parametrizable, o mantener DEV-001/DEV-002 y agregar tabla de "todas las categorías válidas" en sus respectivas §Cuándo usar. Decisión final del TL_NPL.

### 4.3 VTS-029 — Scripts DEV

**Recomendación:** ratificar la decisión Q3 de AUDIT_VTS-007 (NO crear `04.Scripts/dev/`).

Justificación:
- Las 4 operaciones DEV son curls ≤5 líneas a 4 endpoints REST (`POST /devlog`, `POST /devlog-entries`, `PATCH /devlog/:id`, `PATCH /devlog/:id/status`, `DELETE /devlog/:id`).
- `GUIA_AUTOR` §10 FAQ acepta Skills atómicas sin Script aparte ("Si la lógica es ≤5 líneas inline (curl simple). Si tiene >5 líneas o se invoca desde varias Skills, extraer a Script.").
- El blocker que VTS-029 tiene posteado (`endpoint create-fix-task no existe`) **queda resuelto** con la Opción B de §3.4 (NO se necesita Script para un endpoint que no debe existir).

VTS-029 puede cerrar como "scope = NO crear, decisión documentada".

### 4.4 VTS-049 — CARDs Nivel R

3 CARDs propuestas (1:1 con los 3 Workflows de VTS-027):

| CARD | Pertenece a | Tipo | Tokens estimados | Aplica cuando |
|---|---|---|---|---|
| `VTT.CARD-DEV-001_crear_devlog_entry` | WORKFLOW-DEV-001.001 | CARD-mini | ~400 | `agent.action == register_devlog` en `task.status == in_progress` |
| `VTT.CARD-DEV-002_editar_o_transicionar_entry` | WORKFLOW-DEV-001.002 | CARD-std | ~900 | `agent.action == update_devlog OR tl.action == process_entry_review`. **Debe incluir distinción crítica trazabilidad (fixTaskId) vs bloqueo (Issue ASG-001 §5.4)** |
| `VTT.CARD-DEV-003_cerrar_entries_terminal_pre_aprobacion` | WORKFLOW-DEV-001.003 | CARD-std | ~900 | `agent.role == tl AND sprint.action == close`. **Debe incluir T2 + workaround para `deferred`** |

Cada CARD genera entrada en `cards_catalog.json` con campos canónicos (`id, title, category:"dev", type, tokens_measured, tokens_measured_at, applies_when, requires_prior, consumer, trigger, output, status:"done", path, references`).

### 4.5 Resumen para el LEAD_NPL

| Hija | Estado post-VTS-026 | Bloquea? |
|---|---|---|
| VTS-027 (Workflows) | Lista con insumo concreto §4.1 | No — puede arrancar tras aprobar este reporte |
| VTS-028 (Skills) | Lista con fixes obligatorios §4.2 + decisión TL_NPL sobre Skills nuevas | No |
| VTS-029 (Scripts) | Recomendación: cerrar como "scope = no crear" §4.3 | No |
| VTS-049 (CARDs) | Lista con 3 CARDs propuestas §4.4 | Depende de VTS-027 (CARDs 1:1 con Workflows) |
| VTS-050 | **Cancelada** — no aplica | — |
| **VTS-051** (bump Protocol DEV-001 v1.1.0) | **Materializa los hallazgos T2/T3/H-1..H-4 + recomendación §3.4 Opción B + Workaround §2.3.2** | Depende de este reporte |

---

## 5. Ajustes propuestos al paquete (CA-3) → bump v1.1.0 (lo materializa VTS-051)

**Resumen para VTS-051** — lista priorizada de cambios al paquete DEV-001 que **NO ejecuto en este reporte** pero que el bump debe incorporar:

### 5.1 Cambios obligatorios al Protocol DEV-001 v1.0.0 → v1.1.0

| # | Cambio | Origen | Sección destino propuesta |
|---|---|---|---|
| C1 | Agregar §0 "Matriz de 4 entidades (D-61)" + regla registro único (D-62) | FEATURE v1.1 §0 + GUIA_DEVLOG_FINDINGS §0 | §0 nueva al principio |
| C2 | Tabla completa de 12 categoryCode + severityLevels permitidos por catálogo vivo | H-1 (§2.1.2 de este reporte) | §3.1 ampliar |
| C3 | Documentar T2 BY-DESIGN + 3 workarounds para preservar referencia en `deferred` | Dictamen PM + H-4 | §5.3 nuevo §5.3.5 + nueva regla R14 |
| C4 | Documentar §5.5 "Crear Fix Task desde Entry — distinción trazabilidad vs bloqueo" con flujo manual T3 + redirección a ASG-001 §5.4 para bloqueo | Dictamen PM + §3.4 Opción B de este reporte | §5.5 nuevo |
| C5 | Nueva regla R13: "DEV-003 NUNCA para cambiar status — usar SIEMPRE DEV-004" | H-3 (BUG-CONSISTENCIA) | §7 ampliar |
| C6 | Nueva regla R14: "Para preservar referencia en `deferred`: description original o comment, NUNCA `resolution`" | H-4 + T2 | §7 ampliar |
| C7 | Agregar D-63 (findings open high/critical bloquean `in_review → completed`) al mapa de gates §5.2 | FEATURE v1.1 §7 (mapa de gates) | §5.2 ampliar |
| C8 | Agregar D-64 (elevación a TI con referencia patrón Sprint DEUDA) | FEATURE v1.1 §10 | §4 ampliar (definición de `deferred`) |
| C9 | Agregar D-65 (mapa de gates por familia: devlog/findings/CAs/TIs) como tabla canónica | FEATURE v1.1 §7 | nuevo §5.X "Mapa de gates" |
| C10 | Bump versión v1.0.0 → **v1.1.0** + entry en §8 Historial | — | §8 ampliar |

### 5.2 Cambios obligatorios al paquete Skills DEV (VTS-028)

Listados en §4.2 de este reporte.

### 5.3 Cambios al INVENTARIO + cross-links

Standard de VTS-027/028/029/049: actualizar `INVENTARIO.md` + cross-links bidireccionales Protocol ↔ Workflows ↔ Skills ↔ CARDs.

---

## 6. Devlog del proceso

9 entries registrados en VTS-026 durante FASE B (excluye 3 entries de test borradas con SKL-DEV-005 + comment de trazabilidad previo):

| ID | Categoría | Severity | Status final | Qué documenta |
|---|---|---|---|---|
| `a62f4adf` | decision | null | pending | Arranque FASE B con scope BRIEF v2 (no modifico DEV-001.md) |
| `b5bd739c` | observation | null | pending | Drift SERVICE_KEY obsoleta en BRIEF v2 §7 + OPERATIVO §4 vs .env |
| `3b24f35c` | observation | null | pending | Drift IP hardcoded `http://77.42.88.106:3000` en 5 Skills DEV vs RULE-SEC-001 |
| `07fc738f` | decision | null | pending | Incorporo T2/T3 + cancelación VTS-050 + alcance reducido (no modifico DEV-001.md) al reporte |
| `f4221aa5` | observation | null (norm) | pending | BUG-CONSISTENCIA DEV-003: PATCH body acepta status=resolved + setea resolvedAt/By pero NO mueve status |
| `c75fe4a2` | observation | null (norm) | pending | Backend acepta severity en `decision`/`observation` y la normaliza a null sin warning |
| `3f3a82fe` | observation | null (norm) | pending | Catalog vivo tiene 12 categorías activas, paquete normativo documenta solo 7 |
| `b2f799ba` | decision | null | pending | (entry previa del LEAD_NPL probando endpoints — preservada) |
| `1f238279` | observation | null | wont_fix | (entry previa del LEAD_NPL probando endpoints — cerrada por él) |

> **Nota:** las 7 entries mías quedan `pending` en este punto porque la transición a `resolved` la hace el TL_NPL en code review (FASE 3 de ASG-001) — consistente con regla "agente NO transiciona entries propias a terminal sin revisión TL" (Protocol DEV-001 §3.1). Cuando VTS-026 cierre como `task_completed`, TL_NPL resolverá las entries con `resolution` apropiada por cada hallazgo.

**3 entries de test borradas con SKL-DEV-005** (comment de trazabilidad previo posteado en cada caso):

| ID borrado | Comment trazabilidad ID | Propósito del test |
|---|---|---|
| `0e024547` | `27b51398` | Validar T2 BY-DESIGN (deferred limpia resolution) — CONFIRMADO |
| `3d38123e` | (inline al DELETE batch) | Validar severity en decision se normaliza — CONFIRMADO |
| `71cbe36a` | (inline al DELETE batch) | Validar DEV-003 con status:resolved — DESCUBIERTO H-3 BUG-CONSISTENCIA |

---

## 7. Anexos

### Anexo A — Output curl real (request/response por endpoint validado)

#### A.1 GET catálogo vivo (H-1)

```
Request:  GET /api/catalogs/devlog-categories
Response: HTTP 200, total:12
  issue           severityLevels:[critical,high,medium,low]      active
  tech_debt       severityLevels:[critical,high,medium,low]      active
  decision        severityLevels:[]                              active
  blocker         severityLevels:[critical,high,medium,low]      active
  risk            severityLevels:[critical,high,medium,low]      active
  testing_note    severityLevels:[critical,high,medium,low]      active
  observation     severityLevels:[]                              active
  question        severityLevels:[high,medium,low]               active  ← NO documentada
  dependency      severityLevels:[high,medium]                   active  ← NO documentada
  improvement     severityLevels:[medium,low]                    active  ← NO documentada
  feedback        severityLevels:[high,medium,low]               active  ← NO documentada
  brand_issue     severityLevels:[critical,high,medium]          active  ← NO documentada
```

#### A.2 PATCH /status a deferred — confirmación T2

```
Request:  PATCH /api/tasks/VTS-026/devlog/0e024547-.../status
          body: {"status":"deferred","resolution":"TEST: deberia ser limpiada a null por backend si T2 es BY-DESIGN","deferredToPhaseId":"67045d1f-..."}

Response: HTTP 200
{
  "data": {
    "id": "0e024547-...",
    "status": "deferred",            ← OK
    "resolution": null,              ← T2 CONFIRMADO (limpiado)
    "resolvedAt": null,              ← T2 CONFIRMADO (limpiado)
    "resolvedBy": null,              ← T2 CONFIRMADO (limpiado)
    "deferredToPhaseId": "67045d1f-...",
    "description": "Entry de prueba creada por TW-OPS..." ← preservado
  }
}
```

#### A.3 PATCH body con status:acknowledged — confirmación set reducido DEV-003

```
Request:  PATCH /api/tasks/VTS-026/devlog/71cbe36a-...
          body: {"status":"acknowledged"}

Response: HTTP 400
{
  "code": "VALIDATION_FAILED",
  "details": [{
    "field": "status",
    "message": "Invalid enum value. Expected 'open' | 'resolved' | 'deferred', received 'acknowledged'"
  }]
}
```

#### A.4 PATCH body con status:resolved — BUG-CONSISTENCIA H-3

```
Request:  PATCH /api/tasks/VTS-026/devlog/71cbe36a-...
          body: {"status":"resolved","resolution":"TEST: DEV-003 endpoint body acepto resolved con resolution?"}

Response: HTTP 200
{
  "data": {
    "id": "71cbe36a-...",
    "status": "pending",              ← BUG: status NO se movió
    "resolvedBy": "fe1b589c-...",     ← inconsistente: seteado
    "resolvedAt": "2026-06-10T04:49:15.480Z", ← inconsistente: seteado
    "resolution": "TEST: DEV-003 endpoint body acepto resolved con resolution?", ← inconsistente: persistido
    ...
  }
}
```

#### A.5 POST con severity en decision — H-2

```
Request:  POST /api/tasks/VTS-026/devlog
          body: {"categoryCode":"decision","severity":"high","title":"TEST severity en decision","description":"...","reportedBy":"fe1b589c-..."}

Response: HTTP 200
{
  "data": {
    "id": "3d38123e-...",
    "categoryCode": "decision",
    "severity": null,                 ← severity:"high" enviado, backend normalizó a null sin warning
    ...
  }
}
```

#### A.6 GET phase-summary

```
Request:  GET /api/phases/67045d1f-.../devlog-summary

Response: HTTP 200
{
  "data": {
    "phaseId": "67045d1f-...",
    "total": 7,
    "canProceed": false,
    "byStatus": {"pending":6,"wont_fix":1},
    "bySeverity": {"high":1,"none":6},
    "byCategory": {"blocker":1,"decision":3,"observation":3},
    "blockers": [{
      "id": "e16109d8-...",
      "taskId": "VTS-029",
      "status": "pending",
      "severity": "high",
      "categoryCode": "blocker",
      "title": "[BLOCKER] Endpoint POST /devlog/:id/fix-task no existe en producción — requiere decisión PM",
      ...
    }]
  }
}
```

### Anexo B — Comparativa 12 categorías vivas vs 7 documentadas (resumen)

Ver tabla H-1 en §2.1.2.

### Anexo C — Drift colateral SERVICE_KEY + IP hardcoded

- SERVICE_KEY obsoleta `hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d` documentada en BRIEF v2 §7 + OPERATIVO_TW-OPS_VTT-SETUP §4. **Verificada como inválida** contra `/api/auth/service-token` (`INVALID_SERVICE_KEY`). La vigente vive en `00-platform/.env` como `VTT_SETUP_SERVICE_KEY=2c08e9cc756f6f862da265c61985fa9cc5e8db986fea3830a082c937fc2eb818`.
- IP hardcoded `http://77.42.88.106:3000` en `$VTT_BASE_URL` de las 5 Skills DEV-001..005 §"Variables del entorno". Viola RULE-SEC-001 (siempre dominio `https://api.vttagent.com`). Insumo obligatorio para VTS-028.

---

## 8. Referencias

| # | Documento / Comment | Propósito |
|---|---|---|
| 1 | `BRIEF_VTS-026_validar_devlog_v2.md` (attachment `c1746c7d`) | Alcance oficial de VTS-026 |
| 2 | Comment `9054851e` (dictamen PM, 2026-06-10T04:37) | T2/T3/VTS-050/VTS-051 dictamen |
| 3 | Comments `a758a638` + `824d7a17` (respuestas LEAD_NPL al issue 600d2bde) | Alineación de scope antes de FASE A |
| 4 | `AUDIT_VTS-007_DEV-001.md` (attachment de VTS-007 `c302de2d`) | Auditoría previa de cobertura del paquete |
| 5 | `VTT.PROTOCOL-DEV-001_ciclo_devlog_entry.md` v1.0.0 | Objeto validado |
| 6 | `VTT.SKILL-DEV-001..005` | Objeto validado |
| 7 | `FEATURE_DEVLOG_LIFECYCLE_v1.1.md` (2026-06-04) | Doc canónica del PM (referencia conceptual) |
| 8 | `GUIA_DEVLOG_FINDINGS.md` (2026-06-04) | Árbol P1-P5 + dictámenes finding |
| 9 | `GUIA_FEATURES_MODELO_DINAMICO_V4.md` (2026-06-04) | Fuente del alcance (Módulo C §4) |
| 10 | 7 devlog entries en VTS-026 + 3 borradas con trazabilidad | Trazabilidad del proceso FASE B |

---

**Autor:** TW-OPS (Technical Writer of Operational Processes)
**Branch:** `feature/VTS-026-validar-devlog-vs-mod-dinamico-v4`
**Estado del reporte:** Borrador FASE B + C — listo para que LEAD_NPL revise antes de mover VTS-026 a `task_in_review`
**Próximo paso:** subir como attachment `fileType=code_logic` (Review Gate L10) + reportar cumplimiento de 4 CAs + commit + push + PR a main + transición `task_in_progress → task_in_review`
**Materializa el bump:** VTS-051 nueva (depende de este reporte)
