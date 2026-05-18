# ESTRUCTURA DE REPOSITORIOS — Memory Service

| Campo | Valor |
|-------|-------|
| **Documento** | ESTRUCTURA_REPO_MEMORY_SERVICE.md |
| **Versión** | 2.0 |
| **Fecha** | 2026-04-23 |
| **Autor** | PM (Martin Rivas) |
| **Propósito** | Blueprint exacto de carpetas/archivos para los **4 repositorios** del proyecto. **Deliverable concreto de INIT-B-02**. |
| **Audiencia** | DO (ejecuta creación) · PJM (verifica) · TL (review) |
| **Fuentes** | **ADR-001** estrategia 4 repos · V3.1 estándar · FASES_APLICABLES v2.0 |
| **Estado** | ✅ Aprobado PM |

---

## CHANGELOG

| Versión | Cambios |
|---------|---------|
| 1.0 (2026-04-22) | ❌ **OBSOLETA** — Asumía monorepo único, no respetaba ADR-001 |
| **2.0 (2026-04-23)** | Alineada a **ADR-001**: 4 repos separados. Code-logic se mueve a los repos de código. `phases/` queda solo en `memory-service-project`. |

---

## 1. CÓMO SE DETERMINÓ LA ESTRUCTURA

### 1.1 Decisión de gobernanza: ADR-001 (4 repos)

**Fuente principal:** [ADR-001_estrategia_repositorios.md](./ADR-001_estrategia_repositorios.md) — aprobado por PM 2026-04-23.

Razón principal: scope leak físico de agentes IA. Cada agente tiene PAT con scope al repo de su rol; el push a otro repo retorna `403`.

### 1.2 Los 4 repos (ya creados en `prompt-ai-studio`)

| # | Repo | URL | Función |
|---|------|-----|---------|
| 1 | `memory-service-project` | https://github.com/prompt-ai-studio/memory-service-project | Docs PM/PJM, ADRs, handoffs, devlogs, knowledge, scripts ops |
| 2 | `memory-service-api` | https://github.com/prompt-ai-studio/memory-service-api | Contrato OpenAPI + types compartidos (single source of truth) |
| 3 | `memory-service-backend` | https://github.com/prompt-ai-studio/memory-service-backend | Implementación Node + Express + Prisma + tests BE + infra |
| 4 | `memory-service-frontend` | https://github.com/prompt-ai-studio/memory-service-frontend | Implementación React + Vite + tests FE + assets |

### 1.3 Reglas de distribución (ADR-001 §E)

| Tipo de artefacto | Repo |
|-------------------|------|
| ADRs, handoffs, SPEC, METODOLOGIA, FASES_APLICABLES, CONSOLIDADO | `memory-service-project` |
| Devlogs por tarea + agent-tasks | `memory-service-project/devlogs/` |
| OPERATIVOs de agentes + reglas | `memory-service-project/.claude/` |
| OpenAPI spec + contract tests + types generados | `memory-service-api` |
| Código BE + tests BE + prisma + migraciones | `memory-service-backend` |
| Código FE + tests FE + assets | `memory-service-frontend` |
| Code Logic por archivo (`.LOGIC.md`) | repo del código correspondiente, en `knowledge/code-logic/` |
| docker-compose.yml | `memory-service-backend/infra/` |

### 1.4 Filtro de fases SDLC aplicables

De `FASES_APLICABLES_MEMORY_SERVICE.md v2.0` — las 9 fases SDLC aplican. Los **deliverables** (docs) viven en `memory-service-project/phases/`. El **código** vive distribuido en los 3 repos técnicos.

---

## 2. ESTRUCTURA POR REPO

### 2.1 Repo 1 — `memory-service-project` (governance + docs)

```
memory-service-project/
│
├── README.md                              ← Resumen del proyecto + links a otros 3 repos
├── CONTRIBUTING.md                        ← Workflow cross-repo (BE → API → FE)
├── CODEOWNERS                             ← PM + TL como reviewers
├── LICENSE
├── .gitignore
├── .gitattributes
├── .editorconfig
├── .github/
│   ├── workflows/
│   │   └── docs-lint.yml                  ← Markdown lint en docs
│   └── PULL_REQUEST_TEMPLATE.md
│
├── .claude/                               ← Configuración agentes IA
│   ├── agents/
│   │   ├── OPERATIVO_PM.md
│   │   ├── OPERATIVO_PJM.md
│   │   ├── OPERATIVO_TL.md
│   │   ├── OPERATIVO_SA.md
│   │   ├── OPERATIVO_AR.md
│   │   ├── OPERATIVO_BE.md
│   │   ├── OPERATIVO_DB.md
│   │   ├── OPERATIVO_FE.md
│   │   ├── OPERATIVO_UX.md
│   │   ├── OPERATIVO_DL.md
│   │   ├── OPERATIVO_QA.md
│   │   └── OPERATIVO_DO.md
│   └── rules/
│       ├── PROJECT_RULES.md               ← v1.5 (sin "multi-repo pendiente", ya resuelto)
│       └── Proyect_data.md                ← UUIDs reales agentes
│
├── _pm/                                   ← Governance global del proyecto
│   ├── roles/                             ← Perfiles base por rol
│   ├── templates/                         ← Templates de docs (ver Handoff_proceso/)
│   └── operativos/                        ← OPERATIVO_*, PROCESO_*, MEMO_*
│
├── phases/                                ← Las 9 fases SDLC (SOLO DOCS — el código vive en los repos técnicos)
│   ├── 00-discovery/
│   │   ├── deliverables/                  ← 10 docs (Problem Definition, Value Proposition)
│   │   ├── _pm/                           ← Handoffs Discovery
│   │   └── knowledge/                     ← Devlogs Discovery
│   │
│   ├── 01-planning/
│   │   ├── deliverables/                  ← 33 docs (Vision, Scope, Stakeholders, Risks, Timeline, Budget)
│   │   ├── _pm/
│   │   └── knowledge/
│   │
│   ├── 02-analysis/
│   │   ├── deliverables/                  ← 47 docs (FR, NFR, Use Cases, User Stories, etc.)
│   │   ├── _pm/
│   │   │   └── analisis/                  ← Flujo PM→SA→AR→TL→PJM por sprint
│   │   │       └── S01/
│   │   │           ├── 01-PM/
│   │   │           ├── 02-SA/
│   │   │           ├── 03-AR/
│   │   │           ├── 04-TL/
│   │   │           └── 05-PJM/
│   │   └── knowledge/
│   │
│   ├── 03a-design-uxui/
│   │   ├── deliverables/                  ← 40 docs
│   │   │   ├── personas/
│   │   │   ├── information-architecture/
│   │   │   ├── design-system/
│   │   │   ├── wireframes/
│   │   │   ├── mockups/
│   │   │   └── handoff/
│   │   ├── _pm/
│   │   └── knowledge/
│   │
│   ├── 03b-design-technical/
│   │   ├── deliverables/                  ← 73 docs
│   │   │   ├── solution-architecture/
│   │   │   ├── code-architecture/
│   │   │   ├── database-design/
│   │   │   ├── api-design/                ← Spec funcional (impl en memory-service-api)
│   │   │   ├── sequence-diagrams/
│   │   │   ├── adrs/                      ← ADRs del proyecto (incl. ADR-001)
│   │   │   ├── security-plan/
│   │   │   ├── infrastructure-plan/
│   │   │   └── technical-estimates/
│   │   ├── _pm/
│   │   └── knowledge/
│   │
│   ├── 04-development/
│   │   ├── deliverables/                  ← Swagger ref, READMEs cross-repo
│   │   ├── _pm/                           ← HANDOFF_<DISC>_S<NN>_*, BRIEFs, ASSIGNMENTs
│   │   └── knowledge/                     ← Devlogs por tarea (NO code-logic — vive en repos de código)
│   │
│   ├── 05-testing/
│   │   ├── deliverables/                  ← Test plans, test cases consolidados, reports finales
│   │   ├── _pm/
│   │   └── knowledge/                     ← QA reports, bug reports
│   │
│   ├── 06-deploy/
│   │   ├── deliverables/                  ← Deployment guide, release notes, runbook
│   │   ├── _pm/
│   │   └── knowledge/
│   │
│   └── 07-operations/
│       ├── deliverables/                  ← Monitoring config, support process, scaling plan
│       ├── _pm/
│       └── knowledge/
│
├── docs/                                  ← Referencia técnica viva (cross-repo)
│   ├── ARCHITECTURE.md                    ← Vista general (link a SPEC v1.9)
│   ├── ENVIRONMENT.md                     ← Variables de entorno cross-repo
│   ├── INFRASTRUCTURE.md                  ← Hetzner config, Admin VM contact
│   ├── REPOSITORIES.md                    ← Mapa de los 4 repos + workflow cross-repo
│   └── ONBOARDING.md                      ← Cómo arrancar como nuevo agente (clona los 4)
│
├── devlogs/                               ← Devlogs cross-repo aggregator
│   └── (devlogs por tarea con prefix [BE], [FE], [DB], etc.)
│
├── knowledge/                             ← Knowledge base general
│   └── agent-tasks/                       ← CONTEXTO_<ROL>_SESION.md
│
├── archive/                               ← Histórico (preserva ruta original)
│
├── scripts/                               ← Scripts operativos
│   ├── create_memory_service_vtt.py       ← Carga inicial VTT
│   ├── bootstrap.sh                       ← Clona los 4 repos en estructura esperada
│   ├── rotate_pats.sh                     ← Rotación trimestral de PATs
│   └── VTT_UUIDS_MEMORY_SERVICE.json      ← Generado tras carga
│
└── memory-service-project/                ← (este folder, contenido del PM)
    └── Release2.0/
        ├── 01-PM/
        ├── 02-AR/
        ├── 03-DB/
        ├── 04-TL/
        ├── 05-SA/
        ├── PJM/
        ├── Analisis/
        └── Memory/
```

**PATs con write a este repo:** TODOS los roles (escriben sus devlogs y deliverables de su fase).

---

### 2.2 Repo 2 — `memory-service-api` (contrato)

```
memory-service-api/
│
├── README.md                              ← Cómo se usa el package, versionado SemVer
├── CONTRIBUTING.md                        ← Solo TL puede modificar el contrato
├── CODEOWNERS                             ← @TL (único reviewer)
├── LICENSE
├── .gitignore
├── .editorconfig
│
├── .github/
│   ├── workflows/
│   │   ├── validate.yml                   ← Valida openapi.yaml en cada PR
│   │   ├── codegen.yml                    ← Genera types en cada merge a main
│   │   └── publish.yml                    ← Publica @prompt-ai-studio/memory-service-api-types
│   └── PULL_REQUEST_TEMPLATE.md
│
├── openapi.yaml                           ← SINGLE SOURCE OF TRUTH del contrato
│
├── schemas/                               ← Esquemas JSON Schema reutilizables
│   ├── conversation.json
│   ├── turn.json
│   └── ...
│
├── types/                                 ← Generado automáticamente desde openapi.yaml
│   └── index.d.ts                         ← (no editar manual; codegen sobreescribe)
│
├── contract-tests/                        ← Tests del contrato (request/response shape)
│   ├── import.spec.ts
│   ├── context.spec.ts
│   └── ...
│
├── examples/                              ← Request/Response examples por endpoint
│   ├── import-cli.json
│   ├── import-sdk.json
│   └── ...
│
├── package.json                           ← Publica @prompt-ai-studio/memory-service-api-types
├── tsconfig.json
└── .nvmrc
```

**PATs con write a este repo:** **SOLO TL**. BE/FE solo lectura.

**Versionado del package:** SemVer (1.0.0, 1.1.0, 2.0.0). Major bumps requieren ADR.

---

### 2.3 Repo 3 — `memory-service-backend` (implementación BE)

```
memory-service-backend/
│
├── README.md                              ← Setup local, comandos, links cross-repo
├── CONTRIBUTING.md
├── CODEOWNERS                             ← @TL + @BE_lead
├── LICENSE
├── .gitignore
├── .editorconfig
├── .nvmrc                                 ← `20`
├── .env.example                           ← DATABASE_URL, REDIS_URL, SERVICE_KEY, etc.
│
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                         ← lint + type-check + test + build
│   │   ├── contract-test.yml              ← Valida contra @memory-service-api-types
│   │   └── deploy.yml                     ← Deploy a staging/prod
│   ├── CODEOWNERS
│   └── PULL_REQUEST_TEMPLATE.md
│
├── package.json                           ← Consume @prompt-ai-studio/memory-service-api-types
├── package-lock.json (o pnpm-lock.yaml)
├── tsconfig.json
├── .eslintrc.json
├── .prettierrc
├── .npmrc                                 ← Auth GitHub Packages
│
├── src/
│   ├── app.ts
│   ├── index.ts
│   ├── config/
│   │   └── env.ts
│   ├── routes/
│   │   ├── conversations.routes.ts
│   │   ├── agents.routes.ts
│   │   ├── projects.routes.ts
│   │   ├── context.routes.ts
│   │   ├── dashboard.routes.ts
│   │   └── health.routes.ts
│   ├── controllers/
│   ├── services/
│   │   ├── importer.service.ts
│   │   ├── storage.service.ts
│   │   ├── classifier.service.ts
│   │   ├── context.service.ts
│   │   ├── cleanup.service.ts
│   │   ├── catalog-cache.service.ts
│   │   └── adapters/
│   │       ├── cli.adapter.ts
│   │       ├── web.adapter.ts
│   │       ├── sdk.adapter.ts
│   │       ├── chatgpt.adapter.ts
│   │       └── vtt-channel.adapter.ts
│   ├── middleware/
│   │   ├── error-handler.ts
│   │   ├── validate.ts
│   │   └── auth.ts
│   ├── jobs/
│   │   └── cleanup.job.ts
│   ├── schemas/                           ← Zod validators
│   └── utils/
│
├── prisma/
│   ├── schema.prisma                      ← 19 tablas + 10 catálogos
│   ├── seed.ts                            ← Seed de catálogos
│   └── migrations/
│       └── manual/
│           └── partial_indexes.sql        ← Partial indexes + GIN index
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   ├── performance/                       ← <500ms test
│   └── fixtures/                          ← JSONL de las 5 fuentes
│
├── infra/                                 ← Docker para BE
│   ├── docker-compose.yml                 ← Compose unificado (referencia)
│   ├── Dockerfile                         ← Multi-stage Node 20 Alpine
│   └── .dockerignore
│
└── knowledge/
    └── code-logic/                        ← Espejo de src/ — .LOGIC.md por cada archivo
        ├── routes/
        ├── controllers/
        ├── services/
        │   └── adapters/
        ├── middleware/
        ├── jobs/
        └── README.md                      ← Cómo navegar code-logic
```

**PATs con write a este repo:** TL, BE, DB (prisma/), DO (infra/, .github/), QA (tests/).

---

### 2.4 Repo 4 — `memory-service-frontend` (implementación FE)

```
memory-service-frontend/
│
├── README.md                              ← Setup local, comandos, links cross-repo
├── CONTRIBUTING.md
├── CODEOWNERS                             ← @TL + @FE_lead
├── LICENSE
├── .gitignore
├── .editorconfig
├── .nvmrc                                 ← `20`
├── .env.example                           ← VITE_API_URL, VITE_SERVICE_KEY (para dev only)
│
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                         ← lint + type-check + test + build
│   │   ├── contract-test.yml              ← Valida types contra @memory-service-api-types
│   │   ├── deploy.yml
│   │   └── renovate.yml                   ← Bump automático del paquete de api-types
│   ├── CODEOWNERS
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── renovate.json
│
├── package.json                           ← Consume @prompt-ai-studio/memory-service-api-types
├── package-lock.json (o pnpm-lock.yaml)
├── tsconfig.json
├── tsconfig.node.json
├── vite.config.ts
├── tailwind.config.js
├── postcss.config.js
├── .eslintrc.json
├── .prettierrc
├── .npmrc
├── index.html
│
├── public/                                ← Assets estáticos
│   ├── favicon.svg
│   └── ...
│
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── routes/
│   ├── pages/
│   │   ├── Dashboard.tsx
│   │   ├── AgentTimeline.tsx
│   │   ├── ConversationsList.tsx
│   │   ├── ConversationViewer.tsx
│   │   ├── CostReportProject.tsx
│   │   ├── CostReportAgent.tsx
│   │   ├── ImportManual.tsx
│   │   └── Health.tsx
│   ├── components/
│   │   ├── ConversationViewerTask.tsx
│   │   ├── ConversationViewerReview.tsx
│   │   └── ...
│   ├── hooks/
│   ├── services/                          ← API client (consume types del package)
│   │   ├── api-client.ts
│   │   └── auth-context.tsx
│   ├── types/
│   ├── utils/
│   └── styles/
│
├── tests/
│   ├── unit/
│   ├── component/                         ← Testing Library
│   ├── e2e/                               ← Playwright
│   └── fixtures/
│
├── Dockerfile                             ← Build estático servido con nginx
│
└── knowledge/
    └── code-logic/                        ← Espejo de src/
        ├── pages/
        ├── components/
        ├── hooks/
        └── services/
```

**PATs con write a este repo:** TL, FE, QA (tests/), DO (.github/).

---

## 3. SCRIPT DE BOOTSTRAP — Clonar los 4 repos

`memory-service-project/scripts/bootstrap.sh`:

```bash
#!/bin/bash
# Bootstrap: clona los 4 repos de Memory Service en estructura esperada
set -e

ORG="prompt-ai-studio"
ROOT="${1:-$HOME/memory-service-workspace}"

mkdir -p "$ROOT"
cd "$ROOT"

REPOS=(
  "memory-service-project"
  "memory-service-api"
  "memory-service-backend"
  "memory-service-frontend"
)

for repo in "${REPOS[@]}"; do
  if [ -d "$repo" ]; then
    echo "Skipping $repo (ya existe)"
  else
    echo "Cloning $repo..."
    gh repo clone "$ORG/$repo"
  fi
done

echo ""
echo "✅ Workspace listo en $ROOT"
echo ""
echo "Estructura:"
ls -1 "$ROOT"
echo ""
echo "Siguiente paso: configurar tu PAT segun OPERATIVO_<ROL>.md"
```

Tras ejecutar el bootstrap, el workspace local del agente queda:

```
$HOME/memory-service-workspace/
├── memory-service-project/      ← clone con write
├── memory-service-api/          ← clone read-only para BE/FE, write para TL
├── memory-service-backend/      ← clone con write para BE/DB/DO/QA
└── memory-service-frontend/     ← clone con write para FE/QA/DO
```

---

## 4. SCRIPT DE CREACIÓN DE ESTRUCTURA INTERNA POR REPO

### 4.1 Para `memory-service-project`

```bash
#!/bin/bash
# scripts/init_structure_project.sh
# Inicializa estructura V3.1 dentro de memory-service-project
set -e

# Raíz
mkdir -p .claude/{agents,rules}
mkdir -p .github/workflows
mkdir -p _pm/{roles,templates,operativos}
mkdir -p docs archive scripts devlogs
mkdir -p knowledge/agent-tasks

# 9 fases con 3 subcarpetas estándar
for phase in 00-discovery 01-planning 02-analysis 03a-design-uxui 03b-design-technical 04-development 05-testing 06-deploy 07-operations; do
  mkdir -p "phases/$phase"/{deliverables,_pm,knowledge}
done

# Flujo análisis Fase 2
mkdir -p phases/02-analysis/_pm/analisis/S01/{01-PM,02-SA,03-AR,04-TL,05-PJM}

# Subdivisión deliverables Fase 3A
mkdir -p phases/03a-design-uxui/deliverables/{personas,information-architecture,design-system,wireframes,mockups,handoff}

# Subdivisión deliverables Fase 3B
mkdir -p phases/03b-design-technical/deliverables/{solution-architecture,code-architecture,database-design,api-design,sequence-diagrams,adrs,security-plan,infrastructure-plan,technical-estimates}

echo "✓ Estructura memory-service-project creada"
echo "Total carpetas: $(find . -type d | grep -v '\.git' | wc -l)"
```

### 4.2 Para `memory-service-api`

```bash
#!/bin/bash
# scripts/init_structure_api.sh
set -e

mkdir -p .github/workflows
mkdir -p schemas types contract-tests examples

touch openapi.yaml
echo "node_modules/\ntypes/*.js\n.env" > .gitignore

echo "✓ Estructura memory-service-api creada"
```

### 4.3 Para `memory-service-backend`

```bash
#!/bin/bash
# scripts/init_structure_backend.sh
set -e

mkdir -p .github/workflows
mkdir -p src/{config,routes,controllers,middleware,jobs,schemas,utils}
mkdir -p src/services/adapters
mkdir -p prisma/migrations/manual
mkdir -p tests/{unit,integration,e2e,performance,fixtures}
mkdir -p infra
mkdir -p knowledge/code-logic/{routes,controllers,services,middleware,jobs}
mkdir -p knowledge/code-logic/services/adapters

echo "✓ Estructura memory-service-backend creada"
```

### 4.4 Para `memory-service-frontend`

```bash
#!/bin/bash
# scripts/init_structure_frontend.sh
set -e

mkdir -p .github/workflows
mkdir -p src/{routes,pages,components,hooks,services,types,utils,styles}
mkdir -p public
mkdir -p tests/{unit,component,e2e,fixtures}
mkdir -p knowledge/code-logic/{pages,components,hooks,services}

echo "✓ Estructura memory-service-frontend creada"
```

---

## 5. WORKFLOW CROSS-REPO (ADR-001 §D)

Para una feature que toca contrato + BE + FE:

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Sprint S03 ejemplo: Endpoint GET /context con FE consumiéndolo          │
└─────────────────────────────────────────────────────────────────────────┘

1. TL (en memory-service-api)
   └─ PR: actualiza openapi.yaml con GET /context
   └─ CI valida + merge → publica @prompt-ai-studio/memory-service-api-types@1.3.0

2. BE Agent (en memory-service-backend)
   └─ pnpm add @prompt-ai-studio/memory-service-api-types@^1.3.0
   └─ Implementa controller + service usando types del package
   └─ Contract test pasa
   └─ PR a TL → review → merge

3. FE Agent (en memory-service-frontend) — paralelo o secuencial
   └─ Renovate bumpea api-types automáticamente (PR auto)
   └─ Implementa Page + hook usando types del package
   └─ PR a TL → review → merge

4. PM (cross-repo)
   └─ Mergea ambos en orden BE → FE
   └─ Deploy unitario (mismo docker-compose levanta los 2 containers)
```

---

## 6. CARPETAS VS ARCHIVOS — Reglas V3.1 respetadas

| Regla V3.1 | Cómo se respeta en multi-repo |
|------------|-------------------------------|
| Máximo 4 niveles | Cada repo tiene su propia profundidad — code-logic es excepción declarada |
| 3 subcarpetas por fase | Solo aplica en `memory-service-project/phases/*` |
| Sprint y disciplina en nombre | `DEVLOG_BE_S01_VTT-001_*.md` en `memory-service-project/devlogs/` |
| Crear carpetas solo cuando hay archivos | Aplicar al inicializar (placeholder con .gitkeep cuando se requiera commit del esqueleto) |
| Versionado en subcarpeta solo si >1 versión | `arquitectura/v1/`, `arquitectura/v2/` en `memory-service-project/phases/03b-design-technical/deliverables/` |
| Code-logic como excepción (5 niveles) | Vive en `memory-service-backend/knowledge/code-logic/` y `memory-service-frontend/knowledge/code-logic/` |

---

## 7. CHECKLIST DE VERIFICACIÓN (post-INIT-B-02)

```
REPO 1: memory-service-project
[ ] Existe `.claude/agents/` para 12 OPERATIVOs
[ ] Existe `.claude/rules/` con PROJECT_RULES + Proyect_data
[ ] Existe `_pm/{roles,templates,operativos}/`
[ ] Existen las 9 fases en `phases/`
[ ] Cada fase tiene `deliverables/, _pm/, knowledge/`
[ ] Existe `phases/02-analysis/_pm/analisis/S01/` con 5 sub-roles
[ ] Existe `phases/03a-design-uxui/deliverables/` con 6 subcarpetas
[ ] Existe `phases/03b-design-technical/deliverables/` con 9 subcarpetas (incl. adrs/)
[ ] Existe `docs/`, `archive/`, `scripts/`, `devlogs/`, `knowledge/agent-tasks/`
[ ] Branch protection en main configurado
[ ] CODEOWNERS con PM + TL como reviewers
[ ] PAT_MEM_PM con write configurado

REPO 2: memory-service-api
[ ] Existe `openapi.yaml` (puede vacío inicial)
[ ] Existe `schemas/, types/, contract-tests/, examples/`
[ ] CODEOWNERS solo TL
[ ] Workflow `validate.yml` + `codegen.yml` configurados
[ ] Branch protection en main
[ ] PAT_MEM_TL con write
[ ] PAT_MEM_BE / PAT_MEM_FE con read

REPO 3: memory-service-backend
[ ] Existe `src/` con estructura SPEC §3.2
[ ] Existe `prisma/migrations/manual/`
[ ] Existe `tests/{unit,integration,e2e,performance,fixtures}/`
[ ] Existe `infra/` para docker-compose + Dockerfile
[ ] Existe `knowledge/code-logic/` espejo de src/
[ ] CODEOWNERS con TL + BE_lead
[ ] Branch protection en main
[ ] PATs configurados (TL, BE, DB, DO, QA con write segmentado)

REPO 4: memory-service-frontend
[ ] Existe `src/{pages,components,hooks,services,types,utils,styles}/`
[ ] Existe `public/`
[ ] Existe `tests/{unit,component,e2e,fixtures}/`
[ ] Existe `knowledge/code-logic/`
[ ] CODEOWNERS con TL + FE_lead
[ ] Renovate configurado para bump del api-types package
[ ] Branch protection en main
[ ] PATs (TL, FE, QA, DO con write segmentado)

CROSS-REPO
[ ] `bootstrap.sh` en `memory-service-project/scripts/` clona los 4 repos
[ ] `docs/REPOSITORIES.md` documenta el mapa de los 4 repos
[ ] `docs/ONBOARDING.md` explica cómo arrancar como nuevo agente
[ ] OPERATIVO_<ROL>.md actualizado con `GITHUB_TOKEN_VAR=PAT_MEM_<ROL>`
```

---

## 8. NOTAS DE V3.1 — DESVIACIONES FORMALIZADAS

V3.1 fue diseñado para monorepo. La estrategia de 4 repos requiere estas adaptaciones:

| Aspecto V3.1 | Adaptación 4 repos | Justificación |
|--------------|--------------------|---------------|
| Una carpeta `phases/` con todo | `phases/` solo en `memory-service-project` | Docs son cross-repo; el código no |
| Code-logic en `phases/04-development/knowledge/code-logic/` | Code-logic en `memory-service-backend/knowledge/code-logic/` y `memory-service-frontend/knowledge/code-logic/` | Code Logic vive con el código por referencia local |
| Devlogs en `phases/04-development/knowledge/` | Devlogs en `memory-service-project/devlogs/` con prefijo `[BE]/[FE]/[DB]` | Devlogs cross-repo necesitan home único |
| `docker-compose.yml` en raíz | `docker-compose.yml` en `memory-service-backend/infra/` | ADR-001 §E |
| `.claude/` en raíz | `.claude/` solo en `memory-service-project` | Agentes consumen reglas desde un solo lugar |

---

## 9. RELACIÓN CON TAREAS VTT (revisada)

| Task | Acción | Output | Repo target |
|------|--------|--------|-------------|
| **MEM-001** Infra Setup | Coordinar Admin VM | `/root/memory-service-storage/` | (VM, no repo) |
| **MEM-002** Repo Structure | Ejecutar 4 scripts de init + bootstrap | 4 repos con estructura V3.1 adaptada | TODOS |
| **MEM-003** Team Onboarding | OPERATIVOs + accesos PATs | 12 OPERATIVOs configurados | `memory-service-project` |
| **MEM-004** Tooling Setup | package.json/tsconfig/eslint en BE+FE+API | Tooling listo | `api`, `backend`, `frontend` |
| **MEM-075** Docker | `docker-compose.yml` + Dockerfiles | Container config | `memory-service-backend/infra/` (compose + Dockerfile BE) + `memory-service-frontend/Dockerfile` |
| **MEM-042** API Design | OpenAPI spec inicial | `openapi.yaml` | `memory-service-api` |
| **MEM-048** DB Schema | `schema.prisma` | Schema implementado | `memory-service-backend/prisma/` |
| **MEM-053..080** Backend impl | Código BE | Código + tests + code-logic | `memory-service-backend` |
| **MEM-081..093** UI | Código FE | Código + tests + code-logic | `memory-service-frontend` |

---

## 10. MIGRACIÓN DEL REPO LOCAL ACTUAL

Estado actual: `c:\Users\Martin\Documents\virtual-teams\memory-service\` con remoto a `twitter-react.git` (incorrecto).

**Acciones pendientes (ADR-001 Fase 3):**

1. Renombrar el dir local a `memory-service.legacy/`
2. Clonar los 4 repos nuevos en un workspace limpio (`bootstrap.sh`)
3. Migrar contenido por destinos:

| Origen local actual | Destino |
|---------------------|---------|
| `memory-service-project/` (este folder) | `memory-service-project/` (raíz del repo) |
| `knowledge/agent-tasks/` | `memory-service-project/knowledge/agent-tasks/` |
| `.claude/agents/`, `.claude/rules/` | `memory-service-project/.claude/` |
| `devlogs/` | `memory-service-project/devlogs/` |
| (pendiente) código backend | `memory-service-backend/src/` (Sprint 2) |
| (pendiente) código frontend | `memory-service-frontend/src/` (post Design Handoff MEM-038) |
| (pendiente) OpenAPI spec | `memory-service-api/openapi.yaml` (cuando arranque MEM-042) |

---

**Documento:** ESTRUCTURA_REPO_MEMORY_SERVICE.md
**Versión:** 2.0
**Estado:** ✅ Aprobado PM
**Fecha:** 2026-04-23
**Deliverable de:** INIT-B-02 (sub-tarea de MEM-002 Repo Structure)
**Supersede:** v1.0 (asumía monorepo)

---

**PM — Martin Rivas**
