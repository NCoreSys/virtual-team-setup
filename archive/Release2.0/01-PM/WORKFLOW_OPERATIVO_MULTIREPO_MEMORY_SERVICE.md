# WORKFLOW OPERATIVO MULTI-REPO — Memory Service

| Campo | Valor |
|-------|-------|
| **Documento** | WORKFLOW_OPERATIVO_MULTIREPO_MEMORY_SERVICE.md |
| **Versión** | 1.0 |
| **Fecha** | 2026-04-23 |
| **Autor** | PM (Martin Rivas) |
| **Propósito** | Cómo trabaja físicamente cada agente con la estrategia de 4 repos del ADR-001 |
| **Audiencia** | Todos los roles activos del proyecto |
| **Fuentes** | ADR-001 estrategia de repos · ESTRUCTURA_REPO v2.0 |
| **Estado** | ✅ Aprobado PM |

---

## 1. PROBLEMA QUE RESUELVE

Tras aprobar el ADR-001 (4 repos separados), surge la pregunta operativa:

> "¿Tengo que abrir 4 ventanas de VS Code? ¿Cómo se entera Claude Code de los OPERATIVOs si están en otro repo?"

Este documento define el **workflow estándar** para que cada agente trabaje en una sola sesión de VS Code, vea solo lo que le corresponde, y mantenga la barrera física de scope que el ADR-001 estableció.

---

## 2. CONCEPTOS CLAVE

### 2.1 Multi-root workspace de VS Code

VS Code soporta abrir varios repos en una sola ventana mediante un archivo `.code-workspace` (JSON). Cada agente abre **un solo workspace** que incluye:

- Los repos donde tiene **write** (puede commit y push)
- Los repos donde tiene **read-only** que necesita consultar (`api` para BE/FE)

### 2.2 Doble `.claude/` — sin conflicto

| Ubicación | Para qué |
|-----------|----------|
| `~/.claude/` (en home del agente, fuera del repo) | Configuración personal de Claude Code: settings, keybindings, MCP servers, modelo preferido |
| `memory-service-project/.claude/` (dentro del repo `memory-service-project`) | Configuración del proyecto: OPERATIVO por rol, rules del proyecto, datos de agentes |

**Claude Code lee ambas:** primero la global del usuario, después la del workspace donde está. Si se incluye `memory-service-project` en el workspace multi-root, Claude Code carga los OPERATIVOs del proyecto sin importar en qué otro repo del workspace esté trabajando.

### 2.3 Single source of truth de gobernanza

El repo `memory-service-project` es el **hub de gobernanza** del proyecto:

- OPERATIVOs por rol (`.claude/agents/`)
- PROJECT_RULES + Proyect_data (`.claude/rules/`)
- Devlogs cross-repo (`devlogs/`)
- ADRs (`Release2.0/01-PM/`)
- Knowledge base (`knowledge/agent-tasks/`)

**Regla:** todo agente activo incluye `memory-service-project` en su workspace. Sin excepción.

---

## 3. WORKSPACE POR ROL

### 3.1 Tabla maestra

| Rol | Repos en workspace | Write a | Read-only |
|-----|--------------------|---------|-----------|
| **PM** | 4 | project | api, backend, frontend |
| **PJM** | 4 | project | api, backend, frontend |
| **TL** | 4 | project, **api**, backend, frontend | (ninguno solo lectura) |
| **SA** | 1 | project | — |
| **AR** | 2 | project | api (review contratos) |
| **BE** | 3 | project (devlogs), backend | api |
| **DB** | 2 | project (devlogs), backend (prisma/) | — |
| **FE** | 3 | project (devlogs), frontend | api |
| **UX** | 1 | project | — |
| **DL** | 1 | project | — |
| **QA** | 4 | project (devlogs), backend (tests/), frontend (tests/) | api |
| **DO** | 4 | project (devlogs), backend (infra/, .github/), frontend (.github/) | api |

### 3.2 Archivos `.code-workspace`

Templates en `memory-service-project/scripts/workspaces/`:

- `pm.code-workspace`
- `pjm.code-workspace`
- `tl.code-workspace`
- `be.code-workspace`
- `fe.code-workspace`
- `db.code-workspace`
- `qa.code-workspace`
- `do.code-workspace`
- `sa-ar-ux-dl.code-workspace` (solo project)

Cada agente abre el suyo:

```bash
code <ruta>/memory-service-project/scripts/workspaces/be.code-workspace
```

---

## 4. SETUP INICIAL POR AGENTE

### 4.1 Bootstrap (1 vez por agente)

```bash
# 1. Configurar tu PAT segun tu rol (ver OPERATIVO_<ROL>.md)
export GITHUB_TOKEN="$PAT_MEM_<ROL>"
gh auth login --with-token <<< "$GITHUB_TOKEN"

# 2. Clonar los repos relevantes a tu rol
mkdir -p ~/memory-service-workspace
cd ~/memory-service-workspace

# Todos los agentes clonan project (es obligatorio)
gh repo clone prompt-ai-studio/memory-service-project

# Segun rol, clonar los demas (ejemplo BE)
gh repo clone prompt-ai-studio/memory-service-api      # read-only
gh repo clone prompt-ai-studio/memory-service-backend  # write

# 3. Configurar git user
cd memory-service-project
git config user.name "<<NombreAgente>>"
git config user.email "<<email@memory-service.vtt.ai>>"

# (Repetir git config en cada repo clonado)

# 4. Abrir workspace
code scripts/workspaces/be.code-workspace
```

### 4.2 Daily start (cada sesión)

```bash
# 1. Pull en todos los repos clonados
cd ~/memory-service-workspace
for d in memory-service-*; do (cd "$d" && git pull); done

# 2. Abrir workspace
code memory-service-project/scripts/workspaces/be.code-workspace
```

---

## 5. WORKFLOW DE TRABAJO COTIDIANO

### 5.1 Recibir asignación de tarea (al inicio de la sesión)

1. **Obtener token JWT** (ver tu `OPERATIVO_<ROL>.md` §Auth)
2. **Listar tus tareas asignadas en VTT:**
   ```bash
   curl -s "$API_URL/api/tasks?assigneeId=$TU_UUID&status=task_pending" \
     -H "Authorization: Bearer $TOKEN" | jq '.[] | {id, title}'
   ```
3. **Mover tu primera tarea a `task_in_progress`:**
   ```bash
   curl -s -X PATCH "$API_URL/api/tasks/{TASK_ID}/status" \
     -H "Authorization: Bearer $TOKEN" \
     -d "{\"statusId\":\"2a76888a-...\",\"changedBy\":\"$TU_UUID\"}"
   ```

### 5.2 Trabajar en el código (BE/FE/DB)

**Crear branch en TU repo de código:**

```bash
cd ~/memory-service-workspace/memory-service-backend
git checkout -b feature/MEM-053-import-endpoint
```

**Editar archivos en VS Code** (solo dentro de tu repo de write).

**Commit con formato del proyecto:**

```bash
git add src/routes/conversations.routes.ts src/services/importer.service.ts
git commit -m "feat [MEM-053]: implementar POST /import con 4 adapters

- Idempotencia por [sourceId, externalSessionId]
- Manejo P2002 -> ALREADY_INDEXED
- Catch delega cleanup (AMB-07)

Co-Authored-By: Claude <noreply@anthropic.com>
Refs: #MEM-053"
```

**Push:**

```bash
git push -u origin feature/MEM-053-import-endpoint
```

**Crear PR:**

```bash
gh pr create \
  --title "[MEM-053] POST /import con 4 adapters" \
  --body "Implementa el endpoint segun SPEC v1.9 §9.1. Ver devlog para detalles." \
  --base main
```

### 5.3 Crear devlog y code-logic

**Devlog (en `memory-service-project`):**

```bash
cd ~/memory-service-workspace/memory-service-project
git checkout -b devlog/MEM-053
# Crear archivo
mkdir -p devlogs
cat > devlogs/2026-04-23_MEM-053_import-endpoint.md << EOF
# Devlog MEM-053 — POST /import endpoint

**Fecha:** 2026-04-23
**Rol:** BE
**Tarea:** MEM-053
**Repo de código:** memory-service-backend
...
EOF

git add devlogs/2026-04-23_MEM-053_import-endpoint.md
git commit -m "docs [MEM-053]: devlog del endpoint /import

Co-Authored-By: Claude <noreply@anthropic.com>"
git push origin devlog/MEM-053
gh pr create --title "[MEM-053] devlog import endpoint" --body "Devlog de la tarea." --base main
```

**Code-logic (`.LOGIC.md` en `memory-service-backend/knowledge/code-logic/`):**

```bash
cd ~/memory-service-workspace/memory-service-backend
mkdir -p knowledge/code-logic/services
cat > knowledge/code-logic/services/importer.service.LOGIC.md << EOF
# importer.service.ts — LOGIC

## Propósito
Implementa el flujo de import de conversaciones desde 4 fuentes...

## Flujo
1. Validar payload con zod
2. Resolver sourceId desde cache
3. Verificar idempotencia
...
EOF
git add knowledge/code-logic/services/importer.service.LOGIC.md
git commit -m "docs [MEM-053]: code-logic de importer.service

Co-Authored-By: Claude <noreply@anthropic.com>"
git push
```

### 5.4 Mover a `task_in_review`

**Antes** de mover a review, **subir attachments a VTT** (devlog + code-logic + comentario de entrega):

```bash
# Subir devlog
curl -s -X POST "$API_URL/api/tasks/{TASK_ID}/attachments" \
  -F "file=@devlogs/2026-04-23_MEM-053_import-endpoint.md" \
  -F "fileType=devlog" \
  -F "uploadedById=$TU_UUID"

# Subir code-logic
curl -s -X POST "$API_URL/api/tasks/{TASK_ID}/attachments" \
  -F "file=@knowledge/code-logic/services/importer.service.LOGIC.md" \
  -F "fileType=code_logic" \
  -F "uploadedById=$TU_UUID"

# Comentario de entrega
curl -s -X POST "$API_URL/api/tasks/{TASK_ID}/comments" \
  -H "Content-Type: application/json" \
  -d "{\"message\":\"Entrega de MEM-053. PR backend: <url>. PR project (devlog): <url>.\",\"userId\":\"$TU_UUID\"}"

# Mover a review
curl -s -X PATCH "$API_URL/api/tasks/{TASK_ID}/status" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"statusId\":\"1ec975a5-...\",\"changedBy\":\"$TU_UUID\"}"
```

### 5.5 TL hace review

El TL abre `tl.code-workspace` (multi-root con los 4 repos), revisa los PRs en `backend` + `project`, y decide:

- **Aprobado** → mueve la tarea a `task_completed` (PATCH status)
- **Rechazado** → comentario con observaciones + PATCH a `task_rejected`

### 5.6 PM hace merge + sign-off

El PM (con write a los 4 repos) hace los merges:

1. Merge del PR de código (`memory-service-backend`)
2. Merge del PR de devlog (`memory-service-project`)
3. Mover tarea a `task_approved` (solo PM puede)

---

## 6. WORKFLOW CROSS-REPO (feature que toca contrato + BE + FE)

Ver ADR-001 §D. Aquí el resumen ejecutivo:

```
1. TL (en su workspace tl.code-workspace)
   └─ PR en memory-service-api: actualiza openapi.yaml
   └─ Merge → CI publica @prompt-ai-studio/memory-service-api-types@1.X.0

2. BE Agent (en be.code-workspace)
   └─ pnpm add @prompt-ai-studio/memory-service-api-types@^1.X.0
   └─ Implementa contra los types nuevos
   └─ PR en backend → review TL → merge

3. FE Agent (en fe.code-workspace, paralelo)
   └─ Renovate bumpea api-types automáticamente
   └─ Implementa Page consumiendo los types
   └─ PR en frontend → review TL → merge

4. PM hace merge unificado y deploy
```

---

## 7. RESUMEN VISUAL DE LA INTERACCIÓN

```
┌─────────────────────────────────────────────────────────────────────┐
│  Agente BE — sesión típica                                          │
└─────────────────────────────────────────────────────────────────────┘

     ~/memory-service-workspace/
     │
     ├── memory-service-project/        ← devlogs, OPERATIVO_BE.md, .claude/
     │     │
     │     └── (cuando Claude Code abre workspace, lee .claude/agents/OPERATIVO_BE.md)
     │
     ├── memory-service-api/            ← read-only (consume types)
     │     └── package: @prompt-ai-studio/memory-service-api-types
     │
     └── memory-service-backend/        ← write (código + tests + prisma)
           │
           ├── src/                     ← editar aquí
           ├── prisma/
           ├── tests/
           └── knowledge/code-logic/    ← .LOGIC.md espejo de src/

VS Code abierto con be.code-workspace muestra los 3 repos arriba.
Claude Code en VS Code lee:
  - ~/.claude/  (tu config personal)
  - memory-service-project/.claude/agents/OPERATIVO_BE.md  (instrucciones del proyecto)
```

---

## 8. RECONFIGURACIÓN DEL CHAT/SESIÓN ACTUAL DE PM

**Estado actual del coordinador (Martin):** está trabajando en el dir local
`c:\Users\Martin\Documents\virtual-teams\memory-service\` que tiene el remoto incorrecto a `twitter-react.git`.

**Acción recomendada:**

1. Renombrar el dir actual a `memory-service.legacy/` (preservar como referencia)
2. Hacer bootstrap en limpio:
   ```bash
   mkdir -p ~/memory-service-workspace
   cd ~/memory-service-workspace
   gh repo clone prompt-ai-studio/memory-service-project
   gh repo clone prompt-ai-studio/memory-service-api
   gh repo clone prompt-ai-studio/memory-service-backend
   gh repo clone prompt-ai-studio/memory-service-frontend
   ```
3. Migrar contenido del legacy según ADR-001 §3 Fase 3 (PM coordina)
4. Continuar trabajo desde `~/memory-service-workspace/` con `pm.code-workspace` abierto

---

## 9. REGLAS CRÍTICAS DEL WORKFLOW MULTI-REPO

| Regla | Razón |
|-------|-------|
| **Todo agente activo incluye `memory-service-project` en su workspace** | Claude Code necesita leer `.claude/agents/OPERATIVO_<ROL>.md` |
| **Devlogs SIEMPRE en `memory-service-project/devlogs/`** con prefijo `[BE]/[FE]/[DB]/...` | Cross-repo aggregator único |
| **Code-logic SIEMPRE junto al código** (`memory-service-backend/knowledge/code-logic/` o `memory-service-frontend/knowledge/code-logic/`) | Espejo de `src/` requiere proximidad |
| **Cada agente usa SU PAT, nunca el del coordinador** | Audit log granular y rotación segura |
| **PR de feature cross-repo se mergean en orden api → backend → frontend** | Drift de contratos cero |
| **Ningún agente tiene `Admin` en GitHub** — solo el coordinador (humano) | Branch protection no se puede bypassear |
| **Bootstrap con `bootstrap.sh`** (en `memory-service-project/scripts/`) | Garantiza estructura consistente del workspace local |

---

## 10. POST-SETUP — CÓMO ARRANCA EL PROYECTO

Una vez ejecutado el script `create_memory_service_vtt.py` (carga inicial VTT) **y los repos estén creados con sus PATs**, la ruta operativa es:

```
[Día 0] PM
  └─ Hace bootstrap.sh + pm.code-workspace
  └─ Emite HO_FASE_0_DISCOVERY al PJM y al equipo
  └─ Notifica a SA + PM (los 2 roles activos en Discovery)

[Día 1] PJM
  └─ Hace bootstrap.sh + pjm.code-workspace
  └─ Genera BRIEF_SA_MEM-006_problem-definition.md (en project/_pm/)
  └─ Asigna MEM-006 a SA en VTT (PATCH)
  └─ Notifica a SA con el mensaje del agente (formato del PROCESO_ASIGNACION_TAREAS)

[Día 1] SA
  └─ Hace bootstrap.sh + sa-ar-ux-dl.code-workspace
  └─ Lee OPERATIVO_SA.md, BRIEF, PROJECT_RULES, SPEC v1.9
  └─ Mueve MEM-006 a in_progress
  └─ Crea phases/00-discovery/deliverables/ + 4 docs (0.3.1 a 0.3.4)
  └─ Crea devlogs/2026-04-XX_MEM-006_problem-definition.md
  └─ Sube attachments a VTT
  └─ Mueve MEM-006 a in_review
  └─ Notifica al PM

[Día N] Cuando arranque Development (Sprint S01)
  └─ DB Agent hace bootstrap.sh + db.code-workspace
  └─ BE Agent hace bootstrap.sh + be.code-workspace
  └─ DO Agent hace bootstrap.sh + do.code-workspace
  └─ Trabajan en paralelo según dependencias
```

---

**Documento:** WORKFLOW_OPERATIVO_MULTIREPO_MEMORY_SERVICE.md
**Versión:** 1.0
**Estado:** ✅ Aprobado PM
**Fecha:** 2026-04-23
**Complementa:** ADR-001 + ESTRUCTURA_REPO v2.0
**Próximo paso:** generar los `.code-workspace` por rol en `scripts/workspaces/`

---

**PM — Martin Rivas**
