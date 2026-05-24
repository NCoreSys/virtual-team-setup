# Registro Maestro de Acrónimos — VTT

| Campo | Valor |
|---|---|
| **Versión** | 1.4 |
| **Fecha** | 2026-05-19 |
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

## 3. Categorías de Normativa — `<CAT>` en `VTT.<NIVEL>-<CAT>-<NNN>`

> Usado en: `VTT.PROTOCOL-<CAT>-<NNN>`, `VTT.WORKFLOW-<CAT>-<NNN>.<MMM>`, `VTT.SKILL-<CAT>-<NNN>`, `VTT.SCRIPT-<CAT>-<NNN>`, `VTT.TEMPLATE-<CAT>-<NNN>`.

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

---

## 7. Referencias

- `02.normativa/README.md` §4.2 — versión histórica de la lista (queda como puntero a este registro)
- `02.normativa/GUIA_AUTOR.md` §3 — guía narrativa de asignación de código (referencia este registro)
- `03.templates/normativa/_autoria/README.md` §2 Paso 2 — checklist del autor (referencia este registro)
- `02.normativa/INVENTARIO.md` — inventario maestro de documentos VTT
