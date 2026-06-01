# INDEX — Proyecto VTT (Virtual Teams Tracking)

| Campo | Valor |
|---|---|
| Proyecto | Virtual Teams Tracking (VTT) |
| Project UUID | `d837bcd5-3f10-4e19-a418-344a1eef98ad` |
| Backend | `http://77.42.88.106:3000` |
| PM | Martin Rivas (`pm@vtt.com`) |
| Versión | 1.0 |
| Fecha | 2026-05-29 |

> Índice navegable de los operativos del proyecto VTT. Inspirado en la estructura de `05.proyectos/memory-service/`.

---

## 1. Estructura del proyecto

```
05.proyectos/vtt/
├── Proyect_data.md             ← Datos maestros (UUIDs, emails, service key, status, tokens)
├── INDEX.md                    ← Este archivo
├── operativos-instancias/      ← OPERATIVOS por rol (18 archivos) — manual completo del rol
├── init-messages/              ← INIT por rol (18 archivos) — system prompt al iniciar agente
├── setups/                     ← SETUP por rol (18 archivos) — procedimiento de arranque
├── onboarding/                 ← (vacío — pendiente)
├── setup-proyecto/             ← (vacío — pendiente)
├── living-documents/           ← (vacío — pendiente)
└── templates-proyecto/         ← (vacío — opcional)
```

### Relación INIT → SETUP → OPERATIVO

```
1. INIT_<ROL>.md           ← System prompt corto al iniciar el agente (datos + reglas innegociables)
        ↓ apunta a
2. SETUP_<ROL>.md          ← Procedimiento de arranque (worktree, JWT, archivos a leer, diagnóstico)
        ↓ apunta a
3. OPERATIVO_<ROL>.md      ← Manual completo del rol (workflow, comandos, boundaries, reglas)
```

---

## 2. Archivos por rol (18 roles × 3 archivos = 54 archivos)

### 2.1 Coordinación (6 roles × 3 = 18 archivos)

| Rol | UUID | INIT | SETUP | OPERATIVO |
|-----|------|------|-------|-----------|
| PM Executor | `07a07147-...` | [INIT](init-messages/INIT_PM_EXECUTOR.md) | [SETUP](setups/SETUP_PM_EXECUTOR.md) | [OPERATIVO](operativos-instancias/OPERATIVO_PM_EXECUTOR.md) |
| PM Reviewer | `07a07147-...` | [INIT](init-messages/INIT_PM_REVIEWER.md) | [SETUP](setups/SETUP_PM_REVIEWER.md) | [OPERATIVO](operativos-instancias/OPERATIVO_PM_REVIEWER.md) |
| TL Executor | `abdff0db-...` | [INIT](init-messages/INIT_TL_EXECUTOR.md) | [SETUP](setups/SETUP_TL_EXECUTOR.md) | [OPERATIVO](operativos-instancias/OPERATIVO_TL_EXECUTOR.md) |
| TL Reviewer | `abdff0db-...` | [INIT](init-messages/INIT_TL_REVIEWER.md) | [SETUP](setups/SETUP_TL_REVIEWER.md) | [OPERATIVO](operativos-instancias/OPERATIVO_TL_REVIEWER.md) |
| PJM | `49937318-...` | [INIT](init-messages/INIT_PJM.md) | [SETUP](setups/SETUP_PJM.md) | [OPERATIVO](operativos-instancias/OPERATIVO_PJM.md) |
| PO | `4128b577-...` | [INIT](init-messages/INIT_PO.md) | [SETUP](setups/SETUP_PO.md) | [OPERATIVO](operativos-instancias/OPERATIVO_PO.md) |

### 2.2 Desarrollo (4 roles × 3 = 12 archivos)

| Rol | UUIDs | INIT | SETUP | OPERATIVO |
|-----|-------|------|-------|-----------|
| BE (#1 + #2) | `8834830b-...` / `008cacfc-...` | [INIT](init-messages/INIT_BE.md) | [SETUP](setups/SETUP_BE.md) | [OPERATIVO](operativos-instancias/OPERATIVO_BE.md) |
| DB | `a3a2ce62-...` | [INIT](init-messages/INIT_DB.md) | [SETUP](setups/SETUP_DB.md) | [OPERATIVO](operativos-instancias/OPERATIVO_DB.md) |
| DO | `b2e00b9d-...` | [INIT](init-messages/INIT_DO.md) | [SETUP](setups/SETUP_DO.md) | [OPERATIVO](operativos-instancias/OPERATIVO_DO.md) |
| FE (#1 + #2) | `84ad0fbe-...` / `9b8d927e-...` | [INIT](init-messages/INIT_FE.md) | [SETUP](setups/SETUP_FE.md) | [OPERATIVO](operativos-instancias/OPERATIVO_FE.md) |

### 2.3 Análisis y QA (5 roles × 3 = 15 archivos)

| Rol | UUID | INIT | SETUP | OPERATIVO |
|-----|------|------|-------|-----------|
| QA (#1 + #2) | `1d8eb958-...` / `40aea495-...` | [INIT](init-messages/INIT_QA.md) | [SETUP](setups/SETUP_QA.md) | [OPERATIVO](operativos-instancias/OPERATIVO_QA.md) |
| SA Executor | `becdf45a-...` | [INIT](init-messages/INIT_SA_EXECUTOR.md) | [SETUP](setups/SETUP_SA_EXECUTOR.md) | [OPERATIVO](operativos-instancias/OPERATIVO_SA_EXECUTOR.md) |
| SA Reviewer | `becdf45a-...` | [INIT](init-messages/INIT_SA_REVIEWER.md) | [SETUP](setups/SETUP_SA_REVIEWER.md) | [OPERATIVO](operativos-instancias/OPERATIVO_SA_REVIEWER.md) |
| AR (Architect) | `9cc9e322-...` | [INIT](init-messages/INIT_AR.md) | [SETUP](setups/SETUP_AR.md) | [OPERATIVO](operativos-instancias/OPERATIVO_AR.md) |
| IR (Integration Reviewer) | `fbef6ae6-...` | [INIT](init-messages/INIT_IR.md) | [SETUP](setups/SETUP_IR.md) | [OPERATIVO](operativos-instancias/OPERATIVO_IR.md) |

### 2.4 Diseño (3 roles × 3 = 9 archivos)

| Rol | UUID | INIT | SETUP | OPERATIVO |
|-----|------|------|-------|-----------|
| DL Executor | `ebf0f384-...` | [INIT](init-messages/INIT_DL_EXECUTOR.md) | [SETUP](setups/SETUP_DL_EXECUTOR.md) | [OPERATIVO](operativos-instancias/OPERATIVO_DL_EXECUTOR.md) |
| DL Reviewer | `ebf0f384-...` | [INIT](init-messages/INIT_DL_REVIEWER.md) | [SETUP](setups/SETUP_DL_REVIEWER.md) | [OPERATIVO](operativos-instancias/OPERATIVO_DL_REVIEWER.md) |
| UX | `ce8a2ace-...` | [INIT](init-messages/INIT_UX.md) | [SETUP](setups/SETUP_UX.md) | [OPERATIVO](operativos-instancias/OPERATIVO_UX.md) |

---

## 3. Modelo Ejecutor / Revisor — Aplicación en VTT

Roles con **doble perfil** (Ejecutor + Revisor) — mismo UUID, sesiones separadas:

| Rol | Ejecutor (hace) | Revisor (revisa) |
|-----|-----------------|-------------------|
| **TL** | Tareas técnicas asignadas a sigla TL | Coordinador completo (planifica + asigna + revisa + cierra) |
| **PM** | Define producto + mergea PRs + APR final | Revisa entregables funcionales |
| **SA** | Produce análisis funcional | Revisa análisis ajeno |
| **DL** | Produce specs UI/UX | Revisa entregables UX/FE + QA Visual |

> **Convención:** mismo UUID, dos archivos OPERATIVO_*_EXECUTOR.md y OPERATIVO_*_REVIEWER.md (excepto TL Reviewer que es el más extenso y se usa como entrypoint del rol).

Roles con **un solo perfil**:

- BE (#1 y #2 comparten perfil)
- DB
- DO
- FE (#1 y #2 comparten perfil)
- QA (#1 y #2 comparten perfil)
- AR
- IR
- UX
- PJM
- PO

---

## 4. Roles VTT vs Memory Service

### Roles que VTT TIENE y Memory Service NO

- **Product Owner (PO)** — `product.owner@vtt.ai`
- **Program Manager** — `program.manager@vtt.ai` (sin operativo creado todavía)
- **Product Manager separado** — `product.manager@vtt.ai` (sin operativo — Martin es el PM principal)
- **Integration Auditor** — `integration.auditor@vtt.ai` (sin operativo — duplica IR)
- **Recursos duplicados #2** (Backend, Frontend, QA) cubiertos en el mismo operativo

### Roles que Memory Service TIENE y VTT NO (gap)

Si VTT requiere alguno de estos roles, crear usuarios en el sistema y luego operativos:
- CIA (Competitive Intelligence Analyst)
- MRA (Market Research Analyst)
- PSA (Product Strategy Analyst)
- FA (Financial Analyst)
- SEC (Security Engineer)
- SRE (Site Reliability Engineer)
- TW (Technical Writer)
- QAA (QA Automation)
- PTE (Performance Test Engineer)
- UXR (UX Researcher)

---

## 5. Modelo de dos repos — Normativa vs Operativa

> **Regla:** El agente VTT consulta documentos de DOS repos según la naturaleza del documento.

### Repo `virtual-teams-setup/` — Normativa
> Cómo se hacen las cosas. Genérico y reutilizable entre proyectos.

| Tipo | Path canónico |
|------|---------------|
| Datos del equipo VTT | `00-platform/05.proyectos/vtt/Proyect_data.md` |
| Operativos por rol | `00-platform/05.proyectos/vtt/operativos-instancias/OPERATIVO_*.md` |
| Perfiles base genéricos | `00-platform/01.agents/roles/AGENT_PROFILE_BASE_*.md` |
| Setups por rol | `00-platform/01.agents/setups/SETUP_*.md` |
| Init messages | `00-platform/01.agents/init-messages/INIT_*.md` |
| Protocols (procesos) | `00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-*.md` |
| Reglas Nivel 0 | `00-platform/02.normativa/00.Rules/rules_catalog.json` |
| Skills | `00-platform/02.normativa/03.Skills/` |
| Scripts canónicos | `00-platform/02.normativa/04.Scripts/` |
| Templates (BRIEF, ASSIGNMENT, devlog, code_logic) | `00-platform/03.templates/tarea/` |
| Templates de handoff | `00-platform/03.templates/handoff/` |
| Templates de specs UI/UX | `00-platform/03.templates/specs-design/` |
| Guías operativas | `00-platform/04.docs-soporte/guias-operativas/` |

### Repo `virtual-teams-tracking/` — Operativa
> Qué se está haciendo en el proyecto VTT específicamente. Datos vivos del trabajo en curso.

| Tipo | Path |
|------|------|
| Estado del proyecto / sprint actual | `knowledge/tl-docs/CONTEXTO_TECH_LEAD_SESION.md` |
| Procedimientos operativos agentes (a migrar a 00-platform) | `knowledge/PROCEDIMIENTOS_OPERATIVOS_AGENTES.md` |
| BRIEFs de tareas | `knowledge/agent-tasks/briefs/` |
| ASSIGNMENTs de tareas | `knowledge/agent-tasks/assignments/` |
| Development logs | `knowledge/development-log/` |
| Code logic (espejo de src/) | `knowledge/code-logic/` |
| HTMLs del UX | `knowledge/design/screens/` |
| SPECs y handoffs del PM | `_project-management/` |
| Documentación del proyecto | `_project-management/Documentacion/` |
| Schema BD | `backend/prisma/schema.prisma` |
| Migrations | `backend/prisma/migrations/` |
| Routes BE | `backend/src/routes/` |
| Services BE | `backend/src/services/` |
| Router FE | `frontend/src/router/index.tsx` |
| Tokens App FE | `frontend/src/index.css` |
| Componentes FE | `frontend/src/components/` + `frontend/src/features/` |

### Documentos en migración (legacy → canónico)

| Path legacy (VTT) | Reemplazo canónico (setup) |
|---|---|
| `knowledge/tl-docs/PROCESO_ASIGNACION_TAREAS.md` | `00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-ASG-001_*.md` |
| `knowledge/tl-docs/PROCESO_ASIGNACION_TAREAS.md` (legacy v1.6) | `00-platform/02.normativa/01.Protocols/_pending-migration/PROCESO_ASIGNACION_TAREAS.md` |
| `knowledge/PROCEDIMIENTOS_OPERATIVOS_AGENTES.md` | **pendiente de migrar a `00-platform/02.normativa/`** |
| `_project-management/templates/` | `00-platform/03.templates/` |

---

## 6. Carga de contexto por agente (capas)

### Capa 1 — Auto-cargado en cada sesión
- `MEMORY.md` (auto-memory del proyecto VTT)
- `rules_agents.instructions.md` (reglas globales transversales)
- `OPERATIVO_<ROL>_VTT.md` (perfil del rol activo, en `.claude/agents/...`)

### Capa 2 — El agente lee manualmente al iniciar
- `knowledge/agent-tasks/CONTEXTO_<ROL>_SESION.md` (o `knowledge/tl-docs/` para el TL)
- `GET /api/tasks?assigneeId=<UUID_AGENTE>` — sus tareas asignadas
- `00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-ASG-001_*.md` — ciclo asignación
- `00-platform/05.proyectos/vtt/Proyect_data.md` — datos del equipo
- `00-platform/05.proyectos/vtt/operativos-instancias/OPERATIVO_<MI_ROL>.md` — mi operativo

### Capa 3 — Específico por tarea
- `BRIEF_VTT-XXX_*.md` (attachment de la tarea)
- `ASSIGNMENT_VTT-XXX_*.md` (attachment de la tarea)
- Mensaje del agente (comentario en la tarea con curls de status y datos)

---

## 7. Worktrees del proyecto VTT

VTT usa **4 worktrees genéricos** que el TL asigna por tarea (VTT.PROTOCOL-WT-001):

| Worktree | Path | Uso típico |
|----------|------|------------|
| `vtt-espacio-1` | `virtual-teams-tracking/.vtt/worktrees/vtt-espacio-1` | TL coordinación (default) |
| `vtt-espacio-2` | `virtual-teams-tracking/.vtt/worktrees/vtt-espacio-2` | Agente ejecutor |
| `vtt-espacio-3` | `virtual-teams-tracking/.vtt/worktrees/vtt-espacio-3` | Agente ejecutor |
| `vtt-espacio-4` | `virtual-teams-tracking/.vtt/worktrees/vtt-espacio-4` | Agente ejecutor |

> El TL asigna el worktree en el comentario/ASSIGNMENT de la tarea. Los agentes NO eligen worktree por su cuenta.

### Diagnóstico al abrir (6 estados — ver SETUP_TL_EXECUTOR.md §PASO 4.2)

- ✅ A — Branch idle limpio
- ✅ B — Branch feature mergeada limpia (cleanup automático)
- ✅ C — Tu propia branch en curso
- ⚠️ D — Archivos extraños → STOP + investigar
- 🛑 E — Branch de otra tarea → STOP + reportar al TL
- 🛑 F — Stash sin label → STOP + reportar

### Cleanup obligatorio al cerrar (R-AGENTE-WT-01)

**Regla de oro:** ante duda → commit + push (lo más seguro para el próximo agente).

```bash
git status                              # decidir por tipo (commit/discard/ignorar)
git stash list                          # vacío (excepción documentada en devlog)
git log @{u}..HEAD                      # vacío (todo pusheado)
git checkout wt-<vtt-espacio-N>         # branch idle
```

---

## 8. Pendientes (TODOs)

### Estructura
- [ ] Crear `onboarding/ONBOARDING_AGENTE_EJECUTOR_VTT.md`
- [ ] Crear `onboarding/ONBOARDING_TL_VTT.md`
- [ ] Crear `setup-proyecto/SETUP_VM_VTT.md`
- [ ] Crear `living-documents/LIVING_DOCUMENTS_VTT.md`

### Operativos faltantes (roles sin template genérico)
- [ ] OPERATIVO_PROGRAM_MANAGER (si se decide crear)
- [ ] OPERATIVO_PRODUCT_MANAGER (si se decide separar de PM principal)
- [ ] OPERATIVO_INTEGRATION_AUDITOR (si se decide separar de IR)

### Roles a crear en el sistema (si se necesitan)
- [ ] CIA, MRA, PSA, FA, SEC, SRE, TW, QAA, PTE, UXR

---

## 8. Cómo invocar este operativo desde el agente

### Opción A — Path canónico
```
00-platform/05.proyectos/vtt/operativos-instancias/OPERATIVO_<ROL>.md
```

### Opción B — Symlink a `.claude/agents/`
El sistema actual ya tiene `OPERATIVO_*` en `.claude/agents/` con formato similar. Cuando se migre formalmente, los archivos de `.claude/agents/` apuntarán a estos via symlink o copia controlada.

---

## 9. Convenciones del proyecto VTT

| Aspecto | Convención |
|---------|------------|
| Branch principal | `main` (NUNCA `develop` — LL-004) |
| Commit format | `[tipo](vtt-*) [TASK_ID]: descripción` + Co-Authored-By + Refs |
| PR | siempre a `main` |
| Auth | JWT obligatorio desde VTT-296 / LL-006 |
| Comentarios | campos `message` + `userId` (NO `content`/`authorId`) |
| On-hold | `PUT /on-hold` con `x-user-id` (NUNCA `PATCH /status` — ERR-006) |
| Sprint en tareas | vive en Delivery, NO en Task |
| Tech debt diferido | severity = medium/low (NUNCA high — bloquea gate D-41) |
| Issues correctivos | crear tarea con `sourceIssueId` (NUNCA PUT manual al issue) |

---

## 10. Validación

```bash
# Verificar que todos los UUIDs de operativos existen en el sistema
curl -s "http://77.42.88.106:3000/api/users" | \
  python3 -c "import sys,json; users=json.load(sys.stdin)['data']; \
              print('\n'.join(f\"{u['email']:40} {u['id']}\" for u in users \
                              if u['email'].endswith('@vtt.ai') or u['email'].endswith('@vtt.com')))"

# Comparar UUIDs del Proyect_data.md vs API
diff <(grep -oE '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}' Proyect_data.md | sort -u) \
     <(curl -s "http://77.42.88.106:3000/api/users" | python3 -c "import sys,json; print('\n'.join(u['id'] for u in json.load(sys.stdin)['data'] if u['email'].endswith('@vtt.ai') or u['email'].endswith('@vtt.com')))" | sort -u)
```

---

**Mantenedor:** TL VTT (Claude — `tech.lead@vtt.ai`)
**Cambios:** vía PR al repo `virtual-teams-setup/` cuando esté en git
**Versión:** 1.0 | **Fecha:** 2026-05-29
