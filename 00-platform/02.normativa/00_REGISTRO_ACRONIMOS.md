# Registro Maestro de Acrónimos — VTT

| Campo | Valor |
|---|---|
| **Versión** | 1.7 |
| **Fecha** | 2026-05-31 |
| **Mantenedor** | PM Martin Rivas |
| **Audiencia** | Todo autor de normativa (PM/TL/SA) antes de crear Protocol/Workflow/Skill/Script |
| **Source of Truth** | Este archivo es la **única** fuente para acrónimos `<CAT>` de codings VTT |

---

## 1. Propósito

Catalogar **todos los acrónimos** que VTT usa como `<CAT>` en su nomenclatura `VTT.<NIVEL>-<CAT>-<NNN>` (Protocol/Workflow/Skill/Script) y en otros espacios de nombres operativos.

> **Por qué existe este archivo:** evitar colisiones silenciosas. Si un autor crea mañana `VTT.PROTOCOL-MAN-002` pensando que `MAN` es "Management" cuando ya está reservado para "Manifests", se rompe la convención y todo lo construido sobre ese acrónimo. Este registro **bloquea** esa posibilidad.

---

## 2. Reglas de asignación

1. **Antes de usar un `<CAT>` nuevo, agregarlo PRIMERO a este registro.** Sin entrada aquí → el coding no es válido y será rechazado en review.
2. **Una vez asignado, NO se reutiliza** aunque el dominio se deprecie. La fila pasa a estado `🟤 Deprecado` pero permanece para evitar colisión con documentos históricos.
3. **Longitud:** mínimo 2, máximo 8 letras. Mayúsculas sin guiones ni números.
4. **Si dos dominios compiten por el mismo acrónimo:** gana el primero registrado; el segundo elige variante (ej. `MAN` para Manifest → si alguien quiere Management, usa `MGMT`).
5. **No se permiten alias** (ej. `MFT` y `MANIFEST` para el mismo concepto). Un acrónimo, un dominio.
6. **Cambios al registro** quedan en §6 Changelog con fecha + autor + motivo.

---

## 3.0 Niveles operativos — `<NIVEL>` en `VTT.<NIVEL>-<CAT>-<NNN>`

> El modelo VTT actual tiene **4 niveles operativos jerárquicos + 1 nivel transversal + 1 nivel runtime**.

| Nivel | Código | Tipo | Cuándo aplica | Documento gobernanza |
|---|---|---|---|---|
| **0** | `RULE` | Transversal | Restricciones que aplican a TODOS los niveles operativos | `00.Rules/README.md` |
| **4** | `PROTOCOL` | Operativo | Proceso de negocio end-to-end multi-fase multi-rol | `README.md` (PROTOCOL-GOV-001) |
| **3** | `WORKFLOW` | Operativo | Sub-proceso atómico con pasos secuenciales | `README.md` (PROTOCOL-GOV-001) |
| **2** | `SKILL` | Operativo | Capacidad reusable parametrizada | `README.md` (PROTOCOL-GOV-001) |
| **1** | `SCRIPT` | Operativo | Comando atómico ejecutable | `README.md` (PROTOCOL-GOV-001) |
| **R** | `CARD` | **Runtime** | Comprimido happy-path de un Workflow para inyectar al prompt del agente. Activado por Prompt Builder según `Aplica cuando` | `05.Cards/README.md` |

### Sobre el Nivel R (CARD)

- **No es un nivel operativo** (no se "ejecuta" — se "lee")
- **No reemplaza** ningún nivel — el agente puede consultar Workflow/Skill si necesita más detalle
- **Es una vista comprimida**: condensa Protocol+Workflow+Skill+Script en 200-5000 tokens
- **Reducción medida**: ~83-91% vs Protocol+Workflow+Skill completos
- **4 tipos por presupuesto** (estimador canónico `chars/4`):
  - `CARD-mini` (200-500 tok, tope 700)
  - `CARD-std` (500-1200 tok, tope 1500)
  - `CARD-large` (1200-2500 tok, tope 3000)
  - `CARD-pack` (2500-4500 tok, tope 5000)
- **Header obligatorio** incluye `Aplica cuando` (expresión lógica sobre `task.phase` + `agent.role` + `task.category`) y `Requiere Cards previas`
- **Catálogo Prompt Builder**: `02.normativa/05.Cards/cards_catalog.json`
- **Template autoría**: `03.templates/normativa/_autoria/TEMPLATE_CARD.md`

---

## 3. Categorías de Normativa — `<CAT>` en `VTT.<NIVEL>-<CAT>-<NNN>`

> Usado en: `VTT.PROTOCOL-<CAT>-<NNN>`, `VTT.WORKFLOW-<CAT>-<NNN>.<MMM>`, `VTT.SKILL-<CAT>-<NNN>`, `VTT.SCRIPT-<CAT>-<NNN>`, `VTT.TEMPLATE-<CAT>-<NNN>`, `VTT.CARD-<CAT>-<NNN>`.

### 3.1 Categorías activas

| `<CAT>` | Nombre completo | Dominio cubierto | Reservado por | Fecha | Estado |
|---|---|---|---|---|---|
| `GOV` | Governance | Gobierno transversal (guías normativas, README de normativa, autorización general) | PM Martin Rivas | 2026-05-13 | ✅ Activo |
| `ASG` | Assignment | Ciclo end-to-end de asignación y cierre de tarea | PM Martin Rivas | 2026-05-13 | ✅ Activo |
| `MAN` | Manifest | Task Manifest (v1.0/v1.5) + Execution Manifest — gobernanza completa del manifest | PM Martin Rivas | 2026-05-17 | ✅ Activo |
| `WT` | Worktree | Git worktrees por rol + workspaces VSCode dedicados — setup, operación diaria, casos especiales, cleanup | PM Martin Rivas | 2026-05-18 | ✅ Activo |
| `ISS` | Issue | Issues, on_hold y sub-ciclo de bloqueantes | PM Martin Rivas | 2026-05-13 | ✅ Activo (2026-05-19 — migración SKL-ISSUE-01) |
| `TRK` | Trackable Items | TIs catalogados: RFs, ADRs, NFRs, BRs, US, UC, tech_debt, AS, PERS | — | 2026-05-13 | ⚪ Reservado |
| `LD` | Living Documents | Documentos vivos del proyecto (SPEC, ARCHITECTURE, etc.) | — | 2026-05-13 | ⚪ Reservado |
| `EVD` | Evidence | Evidencias vinculadas a Trackable Items | — | 2026-05-13 | ⚪ Reservado |
| `DEV` | Devlog | Devlog entries en VTT (decision/blocker/finding/observation/tech_debt) | PM Martin Rivas | 2026-05-13 | ✅ Activo (2026-05-19 — migración skills DEV) |
| `QUERY` | Query | Consultas de lectura sobre tareas VTT (mis-tareas, detalle, avance, etc.) | PM Martin Rivas | 2026-05-19 | ✅ Activo |
| `REPORT` | Report | Reportes generados por agentes (entrega, PJM ejecutivo) | PM Martin Rivas | 2026-05-19 | ✅ Activo |
| `EST` | Estimate | Estimaciones técnicas (SOP-EST-01) | — | 2026-05-13 | ⚪ Reservado |
| `VEL` | Velocity | Métrica de velocidad del equipo (SOP-VEL-01) | — | 2026-05-13 | ⚪ Reservado |
| `RET` | Retrospective | Retrospectivas de sprint (SOP-RET-01) | — | 2026-05-13 | ⚪ Reservado |
| `AUTH` | Authentication | Login, JWT, refresh tokens, service keys | PM Martin Rivas | 2026-05-13 | ✅ Activo (2026-05-19 — migración SKL-AUTH-01) |
| `TASK` | Task CRUD | CRUD de tareas a nivel Skill/Script (crear, asignar, leer) | PM Martin Rivas | 2026-05-13 | ✅ Activo (2026-05-19) |
| `ATTACH` | Attachment | Subir/descargar/listar attachments | PM Martin Rivas | 2026-05-13 | ✅ Activo (2026-05-19) |
| `STATUS` | Status transitions | Cambios de estado de tarea (in_progress, in_review, completed, etc.) | PM Martin Rivas | 2026-05-13 | ✅ Activo (2026-05-19) |
| `COMMENT` | Comment | Comentarios en tareas (APR-PM, APR-TL, genéricos) | PM Martin Rivas | 2026-05-13 | ✅ Activo (2026-05-19) |
| `PB` | Prompt Builder | Sub-sistema Prompt Builder (futuro) | — | 2026-05-13 | ⚪ Reservado |
| `QA` | Quality Assurance | Skills/Workflows de QA (testing, validación) | — | 2026-05-13 | ⚪ Reservado |
| `DB` | Database | Operaciones de base de datos (migrations, queries directas) | — | 2026-05-13 | ⚪ Reservado |
| `GIT` | Git / GitHub | Operaciones de Git, branches, PRs, GitHub API | PM Martin Rivas | 2026-05-13 | ✅ Activo |
| `FILE` | Filesystem | Operaciones de filesystem (copy, mv, glob, etc.) y ubicación de entregables | PM Martin Rivas | 2026-05-13 | ✅ Activo (2026-05-19 — migración SKL-STRUCTURE-01) |
| `HOPJM` | Handoff PJM | Generación de Handoff Maestro PM → PJM a partir del plan de implementación técnica (3B.9 modular o consolidado) | PM Martin Rivas | 2026-05-30 | ✅ Activo |
| `SPRINT` | Sprint Documentation | Generación del trío de documentos por sprint (SETUP + HANDOFF_TL + CLOSURE) por parte del PJM | PM Martin Rivas | 2026-05-30 | ✅ Activo |
| `REVMA` | Revisión Multi-Agente | Ciclo transversal de revisión: PM Revisor (modelo distinto) audita documentos producidos por agentes generadores, máx 3 vueltas, con backfeed obligatorio si downstream rompe upstream | PM Martin Rivas | 2026-05-31 | ✅ Activo |
| `PT` | Paquete Técnico | Generación del paquete técnico base 3B.1..3B.8 (Solution Architecture, Code Architecture, DB Design, API Design, Sequence Diagrams, ADRs, Security Plan, Infrastructure Plan) | PM Martin Rivas | 2026-05-31 | ✅ Activo |
| `OB` | Onboarding Feature | Onboarding de feature dentro de sistema operando — dos pistas paralelas (extracción desde SPEC + análisis del repo existente) | PM Martin Rivas | 2026-05-31 | ✅ Activo |
| `IPL` | Implementation Plan | Consolidación 3B.9 (10 sub-docs: Scope Baseline, WBS, Task Breakdown, Dependency Map, Complexity, Risk-Adjusted, Capacity, Migration & Rollout, Scheduling Inputs, Routing Index) | PM Martin Rivas | 2026-05-31 | ✅ Activo |
| `SEC` | Security / InfoSec | Seguridad de información: prohibición de exposición de datos sensibles (IPs prod, credenciales, paths absolutos, vulnerabilidades activas) en VTT comments/devlog/attachments. Sanitización de outputs. Rotación de credenciales expuestas. | PM Martin Rivas | 2026-05-30 | ✅ Activo (incidente RULE-SEC-001) |
| `RA` | Research Analyst | Pipeline de procesamiento de investigaciones consolidadas (4 agentes Claude/ChatGPT/Gemini/Perplexity → consolidados) hacia specs de features implementables. Extrae recomendaciones críticas con citas literales, marca convergencias/divergencias, agrupa por dominio, produce FEATURE_SPEC ejecutable. | PM Martin Rivas | 2026-06-02 | ✅ Activo (rol RA + skills SKILL-RA-001/002) |
| `PRE` | Preflight TL | Validación contractual de TL contra API real del backend antes de materializar el paquete operativo en VTT | PM Martin Rivas | 2026-05-31 | ✅ Activo |
| `MAT` | Materialización VTT | Ejecución de scripts reproducibles para materializar Release/Sprints/Deliveries/Tasks/TIs/CAs/dependencias en VTT + audit del grafo + reporte de materialización | PM Martin Rivas | 2026-05-31 | ✅ Activo |
| `HOTL` | Handoff TL | Validación PJM → TL del `HANDOFF_TL_S[N].md` al inicio del sprint (FASE 0 PROTOCOL-ASG-001 §5.0.2). Cubre Workflow `.001` + SKILL-HOTL-001 + SCRIPT-HOTL-001 + CARD-ASG-001 | PM Martin Rivas | 2026-05-30 | ✅ Activo |
| `EXE` | Execution (CARDs) | Categoría de CARDs runtime para la **FASE 3 de ejecución del agente** del PROTOCOL-ASG-001. Comprende CARD-EXE-001..009 (lee inputs, verifica worktree, mueve in_progress, ejecuta workflow ASSIGNMENT, LDs, document impacts, hardcode check, entrega, TL mantiene sprint status) | PM Martin Rivas | 2026-05-31 | ✅ Activo |
| `CARD` | CARD (transversal) | Categoría reservada para CARDs transversales sin sub-sistema específico. **Las CARDs operativas usan la categoría del workflow al que pertenecen** (MAN, ASG, EXE, ISS, etc.) | PM Martin Rivas | 2026-05-31 | ⚪ Reservado |
| `LD` | Living Documents | (Re-activado) Skill SKILL-LD-001 + Script SCRIPT-LD-001 para revisión de catálogo de LDs del proyecto antes del commit (PROTOCOL-ASG-001 §5.3.5) | PM Martin Rivas | 2026-05-31 | ✅ Activo (2026-05-31) |
| `DOCIMP` | Document Impacts | Skill SKILL-DOCIMP-001 + Script SCRIPT-DOCIMP-001 para registrar impactos a docs canónicos en VTT vía POST /document-impacts (con fallback DEBT-INFRA-VTT-01 a devlog observation) (PROTOCOL-ASG-001 §5.3.6) | PM Martin Rivas | 2026-05-31 | ✅ Activo |
| `HARDCODE` | Hardcode Security Check | Skill SKILL-HARDCODE-001 + Script SCRIPT-HARDCODE-001.sh para detectar secretos hardcodeados (9 patrones canónicos: passwords, api keys, tokens, service keys, JWT, DB strings, AWS, GCP keys). Bloquea Review Gate si findings reales > 0 (PROTOCOL-ASG-001 §5.3.7) | PM Martin Rivas | 2026-05-31 | ✅ Activo |
| `CODE` | Code Implementation | Skill SKILL-CODE-001 + Scripts SCRIPT-CODE-001 (.LOGIC.md espejo) + SCRIPT-CODE-002 (Development Log). Implementación del código + `.LOGIC.md` por archivo + devlog al cierre | PM Martin Rivas | 2026-05-31 | ✅ Activo |
| `PR` | Pull Request | Skill SKILL-PR-001 + Script SCRIPT-PR-001 para creación de PR canónico vía `gh pr create` con body estructurado (resumen + devlog + manifest + CAs + hardcode check) | PM Martin Rivas | 2026-05-31 | ✅ Activo |
| `RESUME` | Resume Task | Skill SKILL-RESUME-001 + Script SCRIPT-RESUME-001 para retoma del agente tras auto-resume del sistema VTT (post-resolución de Issue FASE 3.5). Detecta `resume_strategy` (`continue` vs `wait_corrective`) + busca stash (PROTOCOL-ASG-001 §5.4.7-8) | PM Martin Rivas | 2026-05-31 | ✅ Activo |
| `CFL` | Canonical File Loader | Skill SKILL-CFL-001 + Script SCRIPT-CFL-001 para lectura formal de documentos canónicos (BRIEFs, ASSIGNMENTs, OPERATIVOs, SPECs) + endpoint canónico de fulfill CAs (`PATCH /criteria/:cid` — NO `POST /fulfill` que devuelve 404) | PM Martin Rivas | 2026-05-31 | ✅ Activo |
| `HO` | Handoff Operativo (consolidado) | Generación end-to-end del Handoff Operativo: ciclo completo desde feature aprobada (METODOLOGIA + SPEC) hasta entrega del paquete operativo al TL. Absorbe el upstream técnico (REVMA + Paquete técnico 3B.1-3B.8 + Dictámenes cross-rol + Implementation Plan 3B.9 + HO Maestro + Paquete operativo PJM). NO incluye preflight ni materialización (eso pertenece al ciclo de tarea ASG-001) | PM Martin Rivas | 2026-06-01 | ✅ Activo |

### 3.2 Acrónimos bloqueados (no usar)

> Acrónimos cuya semántica común podría causar colisión con los activos. Quedan bloqueados de forma preventiva.

| Bloqueado | Por qué | Alternativa sugerida |
|---|---|---|
| `MGT`, `MGMT` | Demasiado cerca de `MAN` (Manifest) | Si se necesita "Management" → usar `MGMT` explícito |
| `STA` | Demasiado cerca de `STATUS` | Usar `STATUS` completo |
| `ATT` | Demasiado cerca de `ATTACH` | Usar `ATTACH` completo |
| `RT` | Ambiguo (Retrospective, Routing, Runtime) | Usar nombre completo del dominio |
| `MD` | Confunde con extensión markdown | Buscar nombre semántico |

### 3.3 Categorías deprecadas

> Categorías que se usaron en el pasado pero se retiraron. **Permanecen en el registro** para que nadie las re-asigne a otro dominio.

*(Vacío — sin deprecaciones aún)*

---

## 3.bis Convenciones de Branch Git

> Patterns obligatorios para los nombres de branches en cualquier repo VTT. Cada pattern corresponde a un actor + propósito específico. **No se permiten branches que no encajen en uno de estos patterns.**

| Pattern | Actor | Propósito | PR a | Cleanup tras merge |
|---|---|---|---|---|
| `feature/<TASK_ID>` | Agente ejecutor (BE/DB/FE/DO/QA/DL/UX/AR/SA) | Implementación de tarea + commit del manifest v1.0 | `main` | `git branch -d feature/<TASK_ID>` |
| `tl/<TASK_ID>-close` | TL Reviewer | Manifest v1.5 + archivos modificados por el TL durante el review (BRIEF/ASSIGNMENT corregidos, etc.) | `main` | `git branch -d tl/<TASK_ID>-close` |
| `fix/<TASK_ID>` | Agente ejecutor (en re-entrega tras `task_rejected`) | Correcciones derivadas de findings del TL | `main` | `git branch -d fix/<TASK_ID>` |
| `hotfix/<DESCRIPTOR>` | TL o agente con autorización del PM | Bug crítico de producción sin TASK_ID asignada aún | `main` | crear TASK_ID retroactivo + cleanup |
| `wt-<repo>-<rol>` | Setup de worktree (idle, no para PRs) | Branch base del worktree del rol; nunca se mergea | — | NO se borra (worktree persiste) |

### Reglas operativas

1. **NO se permite commit directo a main.** Toda branch va por PR.
2. **Una task → una branch `feature/`** (del agente) + **una branch `tl/...-close`** (del TL si modificó archivos).
3. **Naming case-sensitive.** El `<TASK_ID>` se respeta como aparece en VTT (ej. `MS-293`, `VTT-721`).
4. **No anidar slashes** dentro de `<TASK_ID>`. Si el TASK_ID tiene caracteres especiales — usar guion bajo.
5. **Si la tarea se rechaza y re-entrega** → seguir usando `feature/<TASK_ID>` (no crear nueva branch — es continuación).
6. **`tl/<TASK_ID>-close` puede tener múltiples commits** si el TL hace varios cambios durante el review, pero **un solo PR**.

### Patterns prohibidos

| Patrón | Por qué prohibido |
|---|---|
| `main-<TASK_ID>` | Sugiere fork de main; confusión con CI |
| `dev`, `develop` | No usar GitFlow histórico — VTT trabaja trunk-based |
| `<USERNAME>/...` | Personal branches no rastreables al ciclo VTT |
| `temp/`, `wip/` sin TASK_ID | Branches huérfanas sin trazabilidad |

---

## 4. Otros espacios de nombres

Estos espacios NO usan `<CAT>` de §3. Tienen sus propios catálogos canónicos. Los listo aquí para que el autor sepa **dónde NO mirar** cuando elige un acrónimo de normativa.

| Espacio | Pattern | Catálogo canónico | Notas |
|---|---|---|---|
| Categorías de Normativa | `VTT.<NIVEL>-<CAT>-<NNN>` | **Este archivo §3** | Lo que estás leyendo |
| Branches Git | `feature/<TASK_ID>`, `tl/<TASK_ID>-close`, etc. | **Este archivo §3.bis** | 4 patterns activos + patterns prohibidos |
| Capabilities (RBAC) | `<dominio>.<accion>` (ej. `task.create`, `comment.write`) | `02.normativa/00.Rules/capabilities_catalog.json` | 30 capabilities base (Bloque 1) + 25 propuestas (IMPROVE-005) |
| Rules (transversales) | `RULE-<DOMINIO>-<NNN>` (ej. `RULE-AGENT-001`, `RULE-WT-002`) | `02.normativa/00.Rules/rules_catalog.json` | 47 reglas activas |
| Roles | snake_case (ej. `ws_tech_lead`, `org_owner`) | `02.normativa/00.Rules/roles_catalog.json` | 9 roles del Bloque 1 |
| Markers operativos de reglas | snake_case (ej. `auto_detect`, `blocks_review_gate`) | `00.Rules/rules_catalog.json` §markers | 7 markers |
| Severidades de devlog | enum (`low|medium|high|critical`) | Schema VTT backend | — |
| Tipos de Trackable Item | snake_case (ej. `tech_debt`, `nfr_security`) | `02.normativa/catalogs/` | — |
| Status de tarea | snake_case (`task_pending`, `task_in_progress`, ...) | Schema VTT backend | — |
| Tipos de attachment | snake_case (`brief`, `assignment`, `devlog`, `code_logic`, `manifest`, `report`) | Schema VTT backend | — |

> **Si encuentras un acrónimo en código viejo que no está aquí ni en los catálogos:** repórtalo al PM. Probablemente es deuda de la migración legacy.

---

## 5. Cómo registrar un nuevo `<CAT>`

### Paso 1 — Confirmar que no existe

Buscar en §3.1, §3.2, §3.3. Si aparece — no se puede reutilizar.

### Paso 2 — Validar que NO colisione con §4

Si el acrónimo coincide con un nombre de capability/rule/role/marker → elegir otro. Aunque sean espacios distintos, la confusión cognitiva justifica evitar overlap.

### Paso 3 — Agregar fila a §3.1

```markdown
| `XXX` | Nombre completo | Dominio cubierto (1 línea) | Tu nombre + rol | YYYY-MM-DD | ⚪ Reservado |
```

Si vas a usarlo en el mismo commit donde lo registras, marcarlo `✅ Activo`.

### Paso 4 — Agregar entrada al Changelog §6

```markdown
| 1.X | YYYY-MM-DD | Agregado `XXX` por <tu nombre>. Motivo: <brief>. |
```

### Paso 5 — Bump de versión del registro

Patch (1.0 → 1.1) si solo agregás categoría. Minor (1.x → 2.0) si cambia regla operativa.

---

## 6. Changelog

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-05-17 | Versión inicial. Carga 21 categorías legacy de `02.normativa/README.md` §4.2 y `GUIA_AUTOR.md` §3. Marca `MAN` como `✅ Activo` (PROTOCOL-MAN-001 en construcción). Marca `GOV` y `ASG` como `✅ Activo` (Protocols existentes). Resto como `⚪ Reservado`. Establece §3.2 con 5 acrónimos bloqueados preventivamente. |
| 1.1 | 2026-05-17 | `GIT` pasa a `✅ Activo` por PM Martin Rivas. Motivo: registro de `VTT.SKILL-GIT-001` (crear branch), `VTT.SKILL-GIT-002` (commit estructurado) y `VTT.SCRIPT-GIT-001` (validar branch + commit) en el paquete de gobierno editorial del repo (PROTOCOL-GOV-002). |
| 1.2 | 2026-05-18 | **§3.bis nueva — Convenciones de Branch Git.** 5 patterns activos (`feature/<TASK_ID>`, `tl/<TASK_ID>-close`, `fix/<TASK_ID>`, `hotfix/<DESCRIPTOR>`, `wt-<repo>-<rol>`) + 4 patterns prohibidos. Refleja la nueva FASE 4.5 del PROTOCOL-ASG-001 v1.3.0 que introduce el branch del TL (`tl/<TASK_ID>-close`). Por PM Martin Rivas. |
| 1.3 | 2026-05-18 | `WT` registrado como `✅ Activo` por PM Martin Rivas. Motivo: arranque del sub-sistema `VTT.PROTOCOL-WT-001_gobernanza_worktrees` (worktrees por rol + workspaces VSCode + casos especiales + cleanup). Formaliza el acrónimo que ya se usaba informalmente en `RULE-WT-001/002/003` del rules_catalog. |
| 1.4 | 2026-05-19 | **Migración de skills legacy.** Activación de 10 categorías que estaban en estado `⚪ Reservado` por arranque de la migración de 33 skills `SKL-*` a `VTT.SKILL-*`. Activadas: `AUTH`, `TASK`, `STATUS`, `COMMENT`, `DEV`, `ISS`, `ATTACH`, `FILE`. Nuevas (no estaban en el registro): `QUERY` y `REPORT`. Por PM Martin Rivas. |
| 1.5 | 2026-05-30 | Registro de dos categorías nuevas `HOPJM` (Handoff PJM) y `SPRINT` (Sprint Documentation) por PM Martin Rivas. Motivo: arranque de los Protocols `VTT.PROTOCOL-HOPJM-001` y `VTT.PROTOCOL-SPRINT-001`, ambos preceden a `VTT.PROTOCOL-ASG-001` en el ciclo de planificación. |
| 1.6 | 2026-05-31 | **Tanda de 6 acrónimos nuevos del procedimiento upstream completo (feature dentro de sistema operando):** `REVMA` (revisión multiagente transversal), `PT` (paquete técnico 3B.1..3B.8), `OB` (onboarding feature en sistema operando, 2 pistas paralelas), `IPL` (Implementation Plan 3B.9 consolidado + Routing Index), `PRE` (preflight TL contra API real), `MAT` (materialización en VTT con scripts reproducibles). Por PM Martin Rivas / TW-OPS. Habilita los Protocols `VTT.PROTOCOL-REVMA-001`, `PT-001`, `OB-001`, `IPL-001`, `PRE-001`, `MAT-001`. |
| 1.7 | 2026-05-31 | **§3.0 NUEVA: Niveles operativos** (Nivel 0 RULE + 4-3-2-1 PROTOCOL/WORKFLOW/SKILL/SCRIPT + **Nivel R CARD runtime**). Documenta el Nivel R con sus 4 tipos por presupuesto (mini/std/large/pack), estimador canónico `chars/4`, header obligatorio (`Aplica cuando` + `Requiere Cards previas`), catálogo Prompt Builder, template autoría. **Tanda de 11 acrónimos nuevos por arranque del set FASE 3 + FASE 3.5 del PROTOCOL-ASG-001**: `HOTL` (handoff TL FASE 0), `EXE` (CARDs runtime ejecución agente, comprende EXE-001..009), `CARD` (categoría transversal reservada para CARDs sin sub-sistema), `LD` re-activado (Living Documents skill+script), `DOCIMP` (Document Impacts), `HARDCODE` (Hardcode Check 9 patrones), `CODE` (Code Implementation + `.LOGIC.md`), `PR` (Pull Request), `RESUME` (Resume Task post auto-resume), `CFL` (Canonical File Loader + fulfill CAs). Habilita: WORKFLOW-ASG-001.010/.017/.018/.019/.022/.028/.029/.030/.031/.032/.033/.034/.035/.036/.037/.038/.011 + 14 Skills nuevas + 14 CARDs (EXE-001..009 + ISS-001..005) + scripts canónicos. Por PM Martin Rivas. |
| 1.8 | 2026-06-01 | **`HO` registrado como ✅ Activo** por PM Martin Rivas. Motivo: arranque del Protocol consolidado `VTT.PROTOCOL-HO-001_generacion_handoff_operativo` que absorbe el upstream completo (REVMA-SPEC + Paquete técnico 3B.1-3B.8 + Dictámenes cross-rol + Implementation Plan 3B.9 + HO Maestro PM→PJM + Paquete operativo por sprint). Reemplaza al modelo previo de 7 Protocols separados (HOPJM/SPRINT/PT/OB/IPL/PRE/MAT) que será deprecado progresivamente. NO incluye preflight ni materialización VTT — esas fases pertenecen al ciclo de tarea `ASG-001`. |

---

## 7. Referencias

- `02.normativa/README.md` §4.2 — versión histórica de la lista (queda como puntero a este registro)
- `02.normativa/GUIA_AUTOR.md` §3 — guía narrativa de asignación de código (referencia este registro)
- `03.templates/normativa/_autoria/README.md` §2 Paso 2 — checklist del autor (referencia este registro)
- `02.normativa/INVENTARIO.md` — inventario maestro de documentos VTT
