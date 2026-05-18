# ASSIGNMENT: MS-145 - Auto-merge workflow (Claude Code Review) en memory-service-backend

**Task ID**: MS-145
**Brief ref**: INIT-E-04
**Titulo**: Auto-merge workflow (Claude Code Review) en memory-service-backend
**Repositorio destino**: memory-service-backend (NCoreSys/memory-service-backend)
**Asignado a**: DO (DevOps Engineer)
**Prioridad**: H (HIGH)
**Estimacion**: 1 hora
**Complejidad**: LOW
**Categoria**: deployment
**Generado por**: PJM
**Fecha asignacion**: 2026-05-02

---

## 1. Objetivo

Replicar los 2 workflows de GitHub Actions de VTT en el repo `NCoreSys/memory-service-backend`:
- `.github/workflows/claude-code-review.yml` — idéntico al de VTT
- `.github/workflows/auto-merge.yml` — idéntico al de VTT

También configurar los 2 secrets requeridos en el repo.

**Resultado esperado:** Todo PR creado en `memory-service-backend` activa Claude Code Review automáticamente. Si el review pasa, el PR se mergea automáticamente.

---

## 2. Contexto

VTT ya tiene este pipeline funcionando. Memory Service Backend debe replicarlo para agilizar el workflow del equipo: el DO o cualquier agente crea un PR, Claude lo revisa, y si pasa se mergea solo sin intervención manual.

El repo ya está en NCoreSys (confirmado) y tiene branch protection activa en `main`. El pipeline funcionará correctamente.

---

## 3. Estado del Repo (Verificado por PJM — 2026-05-02)

- **Repo**: `NCoreSys/memory-service-backend` ✅ (NO necesita migración)
- **Branch protection**: Activa en `main` ✅
- **Workflows existentes**: Ninguno (carpeta `.github/workflows/` no existe aún)

---

## 4. Archivos a Crear

### 4.1. `.github/workflows/claude-code-review.yml`

```yaml
name: Claude Code Review

on:
  pull_request:
    types: [opened, synchronize, ready_for_review, reopened]

jobs:
  claude-review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: read
      issues: read
      id-token: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 1

      - name: Run Claude Code Review
        id: claude-review
        uses: anthropics/claude-code-action@v1
        with:
          claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
          plugin_marketplaces: 'https://github.com/anthropics/claude-code.git'
          plugins: 'code-review@claude-code-plugins'
          prompt: '/code-review:code-review ${{ github.repository }}/pull/${{ github.event.pull_request.number }}'
```

### 4.2. `.github/workflows/auto-merge.yml`

```yaml
name: Auto Merge PR

on:
  workflow_run:
    workflows: ["Claude Code Review"]
    types:
      - completed

jobs:
  auto-merge:
    name: Auto-merge after Claude review
    runs-on: ubuntu-latest
    if: >
      github.event.workflow_run.conclusion == 'success' &&
      github.event.workflow_run.event == 'pull_request'

    steps:
      - name: Merge PR
        uses: actions/github-script@v7
        with:
          github-token: ${{ secrets.GH_PATH }}
          script: |
            const pr_number = context.payload.workflow_run.pull_requests[0]?.number;
            if (!pr_number) {
              core.warning('No PR number in payload — skipping');
              return;
            }
            console.log(`Merging PR #${pr_number}`);

            const { data: pr } = await github.rest.pulls.get({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: pr_number,
            });

            if (pr.state !== 'open') {
              console.log(`PR #${pr_number} is ${pr.state} — skipping`);
              return;
            }

            await github.rest.pulls.merge({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: pr_number,
              merge_method: 'squash',
              commit_title: pr.title,
              commit_message: `Auto-merged after Claude Code Review\n\n${pr.body || ''}`.trim(),
            });

            console.log(`PR #${pr_number} merged successfully`);
```

---

## 5. Secrets a Configurar en el Repo

Ir a: **GitHub → NCoreSys/memory-service-backend → Settings → Secrets and variables → Actions**

| Secret | Valor | Origen |
|--------|-------|--------|
| `GH_PATH` | El mismo token que usa VTT | Coordinador Martin Rivas |
| `CLAUDE_CODE_OAUTH_TOKEN` | El mismo token OAuth de Claude Code que usa VTT | Coordinador Martin Rivas |

> **IMPORTANTE**: Estos valores NO se documentan en el repo. Pedirlos directamente al Coordinador.

---

## 6. Implementación

### Opción A — Via GitHub API (recomendada para evitar problema de mixed history)

```python
import urllib.request, json, base64

GH_TOKEN = "<tu-PAT-con-permisos-contents-write>"
REPO = "NCoreSys/memory-service-backend"
BRANCH = "feature/MS-145"

def gh(method, path, body=None):
    url = "https://api.github.com" + path
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + GH_TOKEN)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("Content-Type", "application/json")
    return json.loads(urllib.request.urlopen(req).read())

# 1. Get main SHA
main_ref = gh("GET", f"/repos/{REPO}/git/refs/heads/main")
main_sha = main_ref["object"]["sha"]

# 2. Create branch
gh("POST", f"/repos/{REPO}/git/refs", {
    "ref": f"refs/heads/{BRANCH}",
    "sha": main_sha
})

# 3. Commit claude-code-review.yml
review_content = base64.b64encode(REVIEW_YAML.encode()).decode()
gh("PUT", f"/repos/{REPO}/contents/.github/workflows/claude-code-review.yml", {
    "message": "chore [MS-145]: Add Claude Code Review workflow",
    "content": review_content,
    "branch": BRANCH
})

# 4. Commit auto-merge.yml
merge_content = base64.b64encode(MERGE_YAML.encode()).decode()
gh("PUT", f"/repos/{REPO}/contents/.github/workflows/auto-merge.yml", {
    "message": "chore [MS-145]: Add auto-merge workflow",
    "content": merge_content,
    "branch": BRANCH
})

# 5. Create PR
gh("POST", f"/repos/{REPO}/pulls", {
    "title": "[MS-145] Auto-merge workflow (Claude Code Review)",
    "body": "Replica workflows de VTT: claude-code-review + auto-merge. Ver devlog para detalles.",
    "head": BRANCH,
    "base": "main"
})
```

### Opción B — Via git local (si el remote está correctamente configurado)

```bash
git checkout -b feature/MS-145
mkdir -p .github/workflows
# Crear los 2 archivos yml (sección 4)
git add .github/workflows/
git commit -m "chore [MS-145]: Add Claude Code Review + auto-merge workflows

- .github/workflows/claude-code-review.yml
- .github/workflows/auto-merge.yml
Replica configuracion de VTT.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
Refs: #MS-145"
git push origin feature/MS-145
gh pr create --title "[MS-145] Auto-merge workflow (Claude Code Review)" \
  --body "Ver devlog para detalles." --base main
```

---

## 7. Configurar Secrets (MANUAL — requiere acceso de admin al repo)

```bash
# Con gh CLI y permisos de admin:
gh secret set GH_PATH --repo NCoreSys/memory-service-backend
gh secret set CLAUDE_CODE_OAUTH_TOKEN --repo NCoreSys/memory-service-backend
# (gh pedirá el valor interactivamente)
```

---

## 8. Verificación

### 8.1. Verificar que los workflows existen en main
```bash
gh api repos/NCoreSys/memory-service-backend/contents/.github/workflows --jq '[.[].name]'
# → ["auto-merge.yml","claude-code-review.yml"]
```

### 8.2. Verificar secrets configurados
```bash
gh api repos/NCoreSys/memory-service-backend/actions/secrets --jq '[.secrets[].name]'
# → ["CLAUDE_CODE_OAUTH_TOKEN","GH_PATH"]
```

### 8.3. Prueba end-to-end (crear PR de prueba)
```bash
# Crear branch de prueba con un cambio mínimo
git checkout -b test/workflow-check
echo "# workflow test" >> .workflow-test
git add .workflow-test
git commit -m "test: verificar workflow auto-merge"
git push origin test/workflow-check
gh pr create --title "test: verificar Claude Code Review + auto-merge" --base main
# Verificar en GitHub Actions que se dispara el workflow
# Si el review pasa → el PR debe mergearse automáticamente
```

---

## 9. Entregables Requeridos

| # | Entregable | Ubicación |
|---|-----------|-----------|
| 1 | `.github/workflows/claude-code-review.yml` | Repo `NCoreSys/memory-service-backend` |
| 2 | `.github/workflows/auto-merge.yml` | Repo `NCoreSys/memory-service-backend` |
| 3 | Secrets configurados | GitHub Settings → Secrets |
| 4 | Development Log | `knowledge/development-log/2026-05-XX_MS-145_auto-merge-workflow.md` (en `memory-service`) |
| 5 | Commit + PR | Branch `feature/MS-145`, PR a `main` de `memory-service-backend` |

---

## 10. Workflow VTT

```bash
# 1. Cambiar estado en VTT
curl -X PATCH "http://77.42.88.106:3000/api/tasks/MS-145/status" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"statusId":"<task_in_progress_uuid>","comment":"Creando workflows en memory-service-backend"}'

# 2. Implementar (sección 6)

# 3. Cambiar estado a in_review
curl -X PATCH "http://77.42.88.106:3000/api/tasks/MS-145/status" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"statusId":"<task_in_review_uuid>","comment":"Workflows creados y PR abierto"}'
```

---

## 11. Notas

- Los workflows son **idénticos a los de VTT** — no modificar la lógica, solo copiar
- El secret `GH_PATH` en el auto-merge.yml necesita permisos `repo` + `pull_requests:write`
- Si el `CLAUDE_CODE_OAUTH_TOKEN` no está configurado, el workflow `claude-code-review` fallará silenciosamente — verificar en Actions tab
- La verificación end-to-end (paso 8.3) es **obligatoria** antes de reportar como completada

---

**Generado por**: PJM (Martin Rivas)
**Fecha**: 2026-05-02
**Version**: 1.0
