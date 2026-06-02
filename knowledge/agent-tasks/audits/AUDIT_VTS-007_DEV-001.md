# AUDIT — VTS-007 PROTOCOL-DEV-001 paquete normativo

| Campo | Valor |
|---|---|
| **Tarea VTT** | VTS-007 |
| **Branch** | `agent/tw-ops/vtt-setup/audit-protocol-dev-001` |
| **Fecha** | 2026-06-02 |
| **Autor** | TW-OPS (`fe1b589c-7cf2-4779-82d4-b7ae536536ce`) |
| **Estado** | Borrador FASE B — pendiente validación Coordinator antes de empezar FASE C |
| **Inputs auditados** | Protocol DEV-001 v1.0.0, FEATURE_DEVLOG_LIFECYCLE v1.0, 5 Skills DEV (001..005), Protocol ASG-001 v1.6.1, INVENTARIO, 00_REGISTRO_ACRONIMOS, cards_catalog.json, TEMPLATE_CARD |

---

## 1. Resumen ejecutivo

El paquete DEV-001 actual cubre el **Protocol + 5 Skills atómicas** con buena calidad — alineamiento alto con la FEATURE origen. Los **3 gaps reales confirmados** son:

| # | Gap | Severidad | Acción FASE C |
|---|---|---|---|
| **G1** | 3 Workflows DEV-001.001/.002/.003 mencionados en Protocol §6.1 + §5.1/§5.3/§5.4 pero NO existen en `02.Workflows/` | 🔴 Alta — Protocol invoca artefactos inexistentes | Crear los 3 con TEMPLATE_WORKFLOW |
| **G2** | `05.Cards/dev/` no existe (0 Cards Nivel R del lifecycle) | 🟡 Media — Prompt Builder no puede inyectar runtime al agente | Crear Cards aplicables + entradas en `cards_catalog.json` |
| **G3** | DEV-001 §6.3 menciona ASG-001 §5.5 pero NO la frontera §5.4/§5.4.bis (escalación `issue`→Issue formal bug/blocker/question) | 🟡 Media — cross-link unidireccional incompleto | Agregar tabla de escalación + entrada en §6.3 |

3 gaps **descartados** tras la auditoría:

| # | Gap descartado | Razón |
|---|---|---|
| **N1** | Skills DEV-006/007/008 "mencionadas pero faltan" | **No están mencionadas en ningún archivo del repo.** `grep -rn "DEV-00[6-8]"` devuelve 0 hits. El MSG_VTS-007 era preventivo — no hay referencias a limpiar ni Skills a crear |
| **N2** | Scripts DEV (`04.Scripts/dev/`) | Las 5 Skills DEV son curls ≤5 líneas a 4 endpoints REST (POST/PATCH-body/PATCH-status/DELETE). GUIA_AUTOR §10 FAQ acepta Skills atómicas sin Script aparte. **NO crear** (confirmado por Coord en Q3) |
| **N3** | DEV en `00_REGISTRO_ACRONIMOS.md` | Ya activo desde 2026-05-13, registrado por PM. **NO tocar** |

Resultado neto FASE C: **bump Protocol v1.0.0 → v1.1.0** + **3 Workflows nuevos** + **N Cards** (a definir tras inventario) + **fix cross-link DEV→ASG**. Coincide con el plan del Coord.

---

## 2. Inputs auditados

| # | Archivo | Versión | Estado |
|---|---|---|---|
| I1 | `Docs/01-documentacion/features mod dinamico/FEATURE_DEVLOG_LIFECYCLE.md` | v1.0 (2026-05-21) | ✅ leído completo |
| I2 | `00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-DEV-001_ciclo_devlog_entry.md` | v1.0.0 (2026-05-22) | ✅ leído completo |
| I3 | `00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-ASG-001_ciclo_asignacion_tarea.md` | v1.6.1 (2026-05-31) | ✅ grep §5.3/§5.4/§5.4.bis/§5.5/§5.6 |
| I4 | `00-platform/02.normativa/03.Skills/dev/VTT.SKILL-DEV-001..005.md` | v1.0–v1.1 (2026-05-20..22) | ✅ las 5 leídas |
| I5 | `00-platform/02.normativa/05.Cards/cards_catalog.json` + `TEMPLATE_CARD.md` | — | ✅ leídos |
| I6 | `00-platform/02.normativa/INVENTARIO.md` | — | ✅ grep DEV |
| I7 | `00-platform/02.normativa/00_REGISTRO_ACRONIMOS.md` | — | ✅ DEV activo desde v1.4 |

---

## 3. Cross-walk FEATURE → Protocol → Workflows → Skills

### 3.1 Cobertura por sección de la FEATURE

| FEATURE §X | Tema | Cubierto en Protocol DEV-001? | Cubierto en Skill? | Cubierto en Workflow? |
|---|---|---|---|---|
| §1–§3 QUÉ ES / PARA QUÉ / PRECONDICIONES | Definición + catálogos | ✅ §1, §2, §4 | N/A | N/A |
| §4 ESTADOS LIFECYCLE | 6 estados + irreversibilidad | ✅ §4 + tabla §3.3 + R3 | ✅ DEV-004 lifecycle | ❌ **G1 — DEV-001.002** |
| §5 CÓMO SE ACTIVA | Quién transiciona | ✅ §3 Responsabilidades | ✅ DEV-004 | ❌ G1 |
| §6.1 TRANSICIONAR ENTRY | PATCH /devlog/:id/status | ✅ §5.3 + §5.4 | ✅ DEV-004 | ❌ G1 |
| §6.2 CONSULTAR DEVLOG | GET /devlog | Implícito §5.3.1, §5.4.1 | ❌ Sin Skill QUERY-DEV (no hace falta — es GET trivial) | ❌ G1 |
| §6.3 CREAR ENTRY | POST /devlog | ✅ §5.1.3 | ✅ DEV-001 (decision), DEV-002 (observation) | ❌ **G1 — DEV-001.001** |
| §7 FLUJO COMPLETO (8 pasos) | E2E lifecycle | ✅ §5 (4 fases) | parcial | ❌ G1 |
| §8 RELACIÓN REVIEW GATE | Tabla bloqueo critical/high | ✅ §5.2 idéntica | N/A | N/A |
| §9 ERRORES COMUNES | Gotchas | ✅ §7 Reglas R1-R12 | ✅ Skills documentan errores propios | N/A |
| §10 INTEGRACIÓN CIERRE SPRINT | Iteración por tareas | ✅ §5.4 | N/A | ❌ **G1 — DEV-001.003** |
| §11 EJEMPLOS POR CATEGORÍA | 3 ejemplos | ⚠️ Faltan en Protocol (estaría bueno tenerlos) | Skills tienen ejemplos propios | N/A |

**Conclusión §3.1:** Protocol DEV-001 v1.0.0 tiene cobertura completa de la FEATURE. La única ausencia menor son los ejemplos por categoría — opcional, no bloqueante.

### 3.2 Cobertura de las 5 Skills

| Skill | Endpoint cubierto | Categoryque atiende | Estado |
|---|---|---|---|
| `DEV-001 decision` | `POST /devlog` | `decision` (sin severity) | ✅ v1.1 |
| `DEV-002 observacion` | `POST /devlog` | `observation` (sin severity) | ✅ v1.1 |
| `DEV-003 edit_devlog` | `PATCH /devlog/:id` (body) | Todas — corrección de campos | ✅ v1.0 |
| `DEV-004 lifecycle_devlog` | `PATCH /devlog/:id/status` | Todas — transiciones de estado | ✅ v1.0 |
| `DEV-005 delete_devlog` | `DELETE /devlog/:id` | Todas — borrado destructivo | ✅ v1.0 |

**Conclusión §3.2:** las 5 Skills cubren los 4 verbos REST + 7 categoryCode. No faltan Skills. **DEV-006/007/008 no se necesitan** (Coord confirma en Q2: "crear si invocada operativamente / eliminar si aspiracional" — al no estar invocadas, no se crean ni hay refs que limpiar).

### 3.3 Workflows mencionados pero ausentes (G1)

El Protocol DEV-001 referencia 3 Workflows en su §6.1 + en el cuerpo de §5:

| Workflow esperado | Mencionado en Protocol §X | Existe en `02.Workflows/`? |
|---|---|---|
| `VTT.WORKFLOW-DEV-001.001` "Crear devlog entries durante ejecución" | §5.1 + §6.1 | ❌ NO |
| `VTT.WORKFLOW-DEV-001.002` "Procesar devlog en code review" | §5.3 + §6.1 | ❌ NO |
| `VTT.WORKFLOW-DEV-001.003` "Cerrar devlog al cerrar sprint" | §5.4 + §6.1 | ❌ NO |

**Coord confirma en Q1 (con ajuste en .003):**

- `VTT.WORKFLOW-DEV-001.001_crear_devlog_entry.md`
- `VTT.WORKFLOW-DEV-001.002_editar_o_transicionar_entry.md`
- `VTT.WORKFLOW-DEV-001.003_cerrar_entries_terminal_pre_aprobacion.md` (renombrado — verbo explícito)

> Nota: el título del Workflow .003 en el Protocol actual es "Cerrar devlog al cerrar sprint" (FASE 4 del Protocol = cierre de sprint, PM+TL). El Coord renombró a `cerrar_entries_terminal_pre_aprobacion` que sugiere FASE 3 (pre-aprobación de tarea, TL). **Hay una pequeña ambigüedad de scope**: ¿el .003 cubre FASE 3 (por tarea) o FASE 4 (cierre sprint)? **Pendiente clarificación con Coord antes de FASE C** — propuesta: el .003 cubre **FASE 4** (cierre de sprint) y se mantiene el verbo `cerrar_entries_terminal_pre_aprobacion` reinterpretando "aprobación" como "aprobación del sprint" (no de tarea), o bien se crea un `.004` separado. Lo dejo como sub-pregunta en el reporte que paso al Coord.

---

## 4. Cross-link DEV-001 ↔ ASG-001 §5.4 / §5.4.bis (G3)

### 4.1 Estado actual

**DEV-001 §6.3** menciona ASG-001 sólo en su rol de "contenedor" del lifecycle:

> "El lifecycle del devlog ocurre **dentro** del ciclo de asignación. El review (FASE 3) coincide con el PASS del code review del PROTOCOL-ASG-001 §5.5."

**NO menciona §5.4 (bug/blocker) ni §5.4.bis (question)** que son los sub-ciclos donde una entry devlog escala a Issue formal. Cross-link unidireccional incompleto, igual que detectamos en la sesión.

**ASG-001 §4 (líneas 124-131)** SÍ tiene heurística clara para distinguir `bug`/`blocker` vs `question` — pero hay que enlazar desde DEV-001 hacia allá.

### 4.2 Fix propuesto en v1.1.0 (alcance confirmado por Coord en Q4.b)

1. En **DEV-001 §6.3** agregar entrada:

   | Código | Relación |
   |---|---|
   | `VTT.PROTOCOL-ASG-001 §5.4` | Sub-ciclo de Issue tipo `bug`/`blocker` — destino al que escala un entry `categoryCode: blocker` severity `high`/`critical`. La tarea pasa a `task_on_hold` |
   | `VTT.PROTOCOL-ASG-001 §5.4.bis` | Sub-ciclo de Issue tipo `question` — para consultas del agente al TL. La tarea NO pasa a `task_on_hold` |

2. En **DEV-001 §5.1.2** (decisión devlog/comment/issue) **reemplazar** la tabla de 3 filas por la tabla de 6 filas provista por el Coord:

   | Entry devlog (`categoryCode`) | Acción del agente | ¿Escala a Issue formal? |
   |---|---|---|
   | `decision` | registrar y seguir | no |
   | `observation` | registrar y seguir | no |
   | `tech_debt` | registrar + derivar tarea futura | no (queda en devlog) |
   | `issue` (no-bug, no-blocker) | registrar y seguir | no |
   | `issue` tipo `bug`/`blocker` | INVOCAR ASG-001 §5.4 | sí (`POST /issues` `type=bug`/`blocker`) |
   | `issue` tipo `question` | INVOCAR ASG-001 §5.4.bis | sí (`POST /issues` `type=question`) |

3. **NO tocar ASG-001** — sus §5.4 / §5.4.bis ya están correctos en v1.6.1.

---

## 5. Cards Nivel R del lifecycle (G2)

### 5.1 Estado actual

| Carpeta | Cards |
|---|---|
| `05.Cards/exe/` | 4 Cards (EXE-001..004) — pasos iniciales del agente |
| `05.Cards/iss/` | 1 Card |
| `05.Cards/dev/` | ❌ **NO EXISTE** |
| `cards_catalog.json` | 14 cards totales, 0 con `DEV` en categoría |

### 5.2 Cards DEV propuestas (a confirmar con Coord)

Aplicando GUIA_AUTOR §2 (CARD = vista runtime 1:1 con Workflow) y el principio de "happy path comprimido":

| CARD propuesta | Pertenece a Workflow | Aplica cuando | Tipo estimado | Tokens |
|---|---|---|---|---|
| `VTT.CARD-DEV-001` _crear_devlog_entry | DEV-001.001 | `agent.action == register_decision\|observation\|tech_debt\|risk\|testing_note\|issue` en `task.status == in_progress` | `CARD-mini` | ~400 |
| `VTT.CARD-DEV-002` _editar_o_transicionar | DEV-001.002 | `agent.action == update_devlog_entry` (edit body o status) | `CARD-std` | ~700 |
| `VTT.CARD-DEV-003` _cerrar_entries_terminal_pre_aprobacion | DEV-001.003 | `agent.role == tl AND sprint.action == close` (PM cierre) — Coord debe confirmar el rol consumidor | `CARD-std` | ~900 |

> **Sub-pregunta para el Coord**: ¿el ALCANCE de la CARD .003 es agente o TL+PM (cierre de sprint)? Si es PM+TL → es Card de TL, no de agente ejecutor. **Lo aclaro en el chat antes de empezar commit 4**.

Cada CARD requiere también entrada nueva en `cards_catalog.json` con campos: `id`, `title`, `category: "dev"`, `type`, `tokens_measured`, `tokens_measured_at`, `applies_when`, `requires_prior`, `consumer`, `trigger`, `output`, `status`, `path`, `references`.

---

## 6. Decisiones de scope (confirmadas con Coord, ver issue da7faa32)

| ID | Decisión | Confirmada por |
|---|---|---|
| Q1 | Títulos de los 3 Workflows + ajuste `.003` → `cerrar_entries_terminal_pre_aprobacion` | Coord comment `6876d7a0` |
| Q2 | Heurística "crear si invocada / eliminar si aspiracional" — resultado tras auditoría: **NO crear DEV-006/7/8** porque no están invocadas en ningún lado | Coord comment `6876d7a0` |
| Q3 | NO crear `04.Scripts/dev/` — justificación textual (Skills atómicas ≤5 líneas, GUIA_AUTOR §10 FAQ aplica) | Coord comment `6876d7a0` |
| Q4.a | 5 commits estructurados + orden estricto 1→2→3→4→5 + partir commit 3 en 3a/3b si mix | Coord comment `6876d7a0` |
| Q4.b | INCLUIR cross-link DEV-001→ASG-001 §5.4/§5.4.bis con tabla de 6 filas (provista) | Coord comment `6876d7a0` |

---

## 7. Plan de commits propuestos (FASE C)

Tras la auditoría, el plan se simplifica vs propuesta inicial (Q2 → no hay cleanup de DEV-006/7/8 porque no hay referencias):

| # | Commit | Type | Scope | Archivos esperados |
|---|---|---|---|---|
| 1 | Protocol DEV-001 v1.0.0 → v1.1.0 + cross-link ASG §5.4/§5.4.bis | `functional` | `02.normativa/01.Protocols` | 1 archivo modificado |
| 2 | 3 Workflows DEV-001.001/.002/.003 creados | `functional` | `02.normativa/02.Workflows` | 3 archivos nuevos |
| 3 | ~~Skills DEV-006/7/8~~ **OMITIDO** (sin referencias a crear ni a limpiar) | — | — | 0 |
| 4 | Cards DEV (3 mini/std) + entradas en `cards_catalog.json` | `functional` | `02.normativa/05.Cards` | 3 archivos nuevos + 1 modificado |
| 5 | Cross-links: INVENTARIO + FEATURE_DEVLOG_LIFECYCLE pointer + reporte de auditoría | `structural` | varios | 3+ archivos modificados |

**Total: 4 commits** (no 5 — uno menos porque G2 descartado tras auditar).

---

## 8. Acciones pendientes ANTES de empezar FASE C

1. ⏸️ **Coord debe validar este reporte** (Coord lo pidió en `6876d7a0` punto 4: "Antes de commit 1, pasame el output de FASE B…")
2. ⏸️ **Sub-preguntas residuales para Coord:**
   - **Q5** (nueva): el Workflow `.003` y su CARD: ¿alcance FASE 4 sprint-close (TL+PM) o FASE 3 task-review (TL)? La FEATURE+Protocol actuales dicen FASE 4 pero el nombre `cerrar_entries_terminal_pre_aprobacion` sugiere FASE 3. Propuesta: **FASE 4 cierre de sprint**, reinterpretando "pre_aprobacion" como "antes de aprobar el sprint en el reporte M".
   - **Q6** (nueva): N1 — el MSG_VTS-007 mencionaba "Skills DEV-006/007/008 mencionadas pero faltan" pero `grep` muestra 0 menciones reales. ¿El Coord las menciona en algún doc no auditable o fue preventivo? Asumo preventivo y las descarto.
3. ⏸️ **Coord también debe destrabar 3 gaps de plataforma reportados aparte** (capability `tracking.update_status`, endpoint resolve issue, falta `tw-ops` en `vtt_governance.example.json`) — son blockers para cerrar VTS-007 pero NO para empezar FASE C de commits.

---

## 9. Referencias

- Issue da7faa32: 4 decisiones de scope (resuelto por comment Coord `6876d7a0`)
- Comment `b863a39b`: reporte de 3 gaps API/regex
- MSG_VTS-007 attachment `7113ecd7`

---

**Autor:** TW-OPS Agent
**Versión reporte:** 1.0 (borrador FASE B)
**Próximo paso:** esperar validación del Coordinator antes de empezar commit 1
