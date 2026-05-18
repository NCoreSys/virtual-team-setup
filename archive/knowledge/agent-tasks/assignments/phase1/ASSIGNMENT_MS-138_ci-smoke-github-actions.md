# ASSIGNMENT: MS-138 - CI mínimo (smoke) en GitHub Actions

**Task ID**: MS-138
**Brief ref**: INIT-E-03
**Titulo**: CI mínimo (smoke) en GitHub Actions
**Repositorio destino**: memory-service-backend (NCoreSys/memory-service-backend)
**Asignado a**: DO (DevOps Engineer)
**Prioridad**: M (MEDIUM)
**Estimacion**: 1 hora
**Complejidad**: LOW
**Categoria**: deployment
**Generado por**: TL
**Fecha asignacion**: 2026-05-02
**Dependencias**: MS-137 (Linters + formatters ✅ en progreso — scripts lint/build deben existir en package.json)

---

## 1. Objetivo

Crear `.github/workflows/ci.yml` en `NCoreSys/memory-service-backend` con un job que ejecuta **build + lint** en cada PR contra `main`. Los fallos deben bloquear el merge.

**Resultado esperado:** Cada PR creado contra `main` dispara automáticamente el CI. Un PR de prueba muestra el check verde en GitHub Actions.

---

## 2. Contexto

MS-136 instaló Node 20 + TypeScript + Express. MS-137 está configurando ESLint + Prettier + scripts de lint. Este CI smoke valida que el código que entra al repo compile y pase lint antes de hacer merge.

**NO confundir con el CI de deploy** — ese va en una tarea posterior. Este CI solo valida calidad de código.

**Dependencia crítica**: MS-137 debe estar completada (o al menos el PR mergeado) antes de que este CI tenga los scripts `lint` y `build` disponibles en `package.json`. Si MS-137 no está mergeado, el CI fallará al llamar `npm run lint`.

---

## 3. Estado del Repo (al momento de asignación)

- **Repo**: `NCoreSys/memory-service-backend` ✅
- **Branch protection**: Activa en `main` ✅
- **Scripts disponibles tras MS-137**: `build`, `lint`, `lint:fix`, `format:check`, `type-check`
- **Carpeta .github/workflows/**: Puede existir ya (MS-145 podría haberla creado)

> **Antes de crear el branch**, verificar si `.github/workflows/` ya existe:
> ```bash
> gh api repos/NCoreSys/memory-service-backend/contents/.github/workflows --jq '[.[].name]'
> ```
> Si existe → solo agregar `ci.yml`. Si no existe → crear la carpeta con el archivo.

---

## 4. Archivo a Crear

### `.github/workflows/ci.yml`

```yaml
name: CI

on:
  pull_request:
    branches: [main]

jobs:
  build-and-lint:
    name: Build + Lint
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run lint
        run: npm run lint

      - name: Run build
        run: npm run build

      - name: Run type check
        run: npm run type-check
```

---

## 5. Implementación (via GitHub API — método obligatorio)

```python
import urllib.request, json, base64

GH_TOKEN = "<tu-PAT-con-permisos-contents-write>"
REPO = "NCoreSys/memory-service-backend"
BRANCH = "feature/MS-138"

CI_YAML = """name: CI

on:
  pull_request:
    branches: [main]

jobs:
  build-and-lint:
    name: Build + Lint
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run lint
        run: npm run lint

      - name: Run build
        run: npm run build

      - name: Run type check
        run: npm run type-check
"""

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

# 3. Commit ci.yml
ci_content = base64.b64encode(CI_YAML.encode()).decode()
gh("PUT", f"/repos/{REPO}/contents/.github/workflows/ci.yml", {
    "message": "chore [MS-138]: Add CI smoke workflow (build + lint)",
    "content": ci_content,
    "branch": BRANCH
})

# 4. Create PR
gh("POST", f"/repos/{REPO}/pulls", {
    "title": "[MS-138] CI mínimo (smoke) en GitHub Actions",
    "body": "Agrega .github/workflows/ci.yml con job build+lint+type-check. Depende de scripts de MS-137. Ver devlog para detalles.",
    "head": BRANCH,
    "base": "main"
})
```

---

## 6. Verificación

### 6.1. Workflow existe en el repo
```bash
gh api repos/NCoreSys/memory-service-backend/contents/.github/workflows --jq '[.[].name]'
# → incluye "ci.yml"
```

### 6.2. CI se dispara en PR de prueba
```bash
# Crear branch de prueba con cambio mínimo
# (via GitHub API — no clonar)
python3 -c "
import urllib.request, json, base64
GH_TOKEN = '<PAT>'
REPO = 'NCoreSys/memory-service-backend'
BRANCH = 'test/ci-check'

def gh(method, path, body=None):
    url = 'https://api.github.com' + path
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header('Authorization', 'Bearer ' + GH_TOKEN)
    req.add_header('Accept', 'application/vnd.github+json')
    req.add_header('Content-Type', 'application/json')
    return json.loads(urllib.request.urlopen(req).read())

main_sha = gh('GET', f'/repos/{REPO}/git/refs/heads/main')['object']['sha']
gh('POST', f'/repos/{REPO}/git/refs', {'ref': f'refs/heads/{BRANCH}', 'sha': main_sha})

content = base64.b64encode(b'# CI test\n').decode()
gh('PUT', f'/repos/{REPO}/contents/.ci-test', {
    'message': 'test: verify CI workflow',
    'content': content,
    'branch': BRANCH
})
gh('POST', f'/repos/{REPO}/pulls', {
    'title': 'test: verificar CI smoke',
    'body': 'PR de prueba para verificar que el CI se dispara.',
    'head': BRANCH,
    'base': 'main'
})
"
# Verificar en GitHub Actions tab que el CI se dispara y pasa
```

### 6.3. Verificar check verde en PR
- Ir a GitHub → NCoreSys/memory-service-backend → Pull Requests
- El PR de prueba debe mostrar ✅ CI / Build + Lint

---

## 7. Entregables Requeridos

| # | Entregable | Ubicación |
|---|-----------|-----------|
| 1 | `.github/workflows/ci.yml` | Repo `NCoreSys/memory-service-backend` |
| 2 | Development Log | `knowledge/development-log/2026-05-XX_MS-138_ci-smoke.md` (en `memory-service`) |
| 3 | Commit + PR | Branch `feature/MS-138`, PR a `main` de `memory-service-backend` |

> **Nota**: No hay archivos `.LOGIC.md` — este workflow es YAML de infraestructura, no código de aplicación.

---

## 8. Entregables Obligatorios (Modelo Dinámico V4)

| # | Entregable | Obligatorio |
|---|------------|-------------|
| 1 | `.github/workflows/ci.yml` | ✅ Sí |
| 2 | Development Log | ✅ Sí |
| 3 | Code Logic | N/A — infraestructura YAML |
| 4 | Commit + PR | ✅ Sí |
| 5 | Swagger Docs | N/A |
| 6 | Devlog entries en VTT | ✅ Sí |
| 7 | CAs reportados con fulfill | ✅ Sí |
| 8 | TrackableItems | N/A |
| 9 | Review gate limpio | ✅ Sí |

---

## 9. Criterios de Aceptación

| CA | criteriaId | Criterio | Cómo verificar |
|----|------------|----------|----------------|
| CA-1 | `2206ccc5-9e42-4842-b913-1308a7afc095` | ci.yml existe en el repo | `gh api repos/NCoreSys/memory-service-backend/contents/.github/workflows` |
| CA-2 | `5055c67b-d444-4b88-9255-9172491280bd` | Job ejecuta lint + build sin errores | Revisar Actions tab en GitHub — job verde |
| CA-3 | `35773cf9-595e-4568-b058-d039ce2e1e72` | CI se dispara en cada PR | Crear PR de prueba y verificar que el check aparece |
| CA-4 | `b0b845fb-c1aa-48ad-b0d1-d2fe1c8e0524` | CI verde en PR de prueba | PR de prueba muestra ✅ en GitHub |
| CA-5 | `c0c255cd-344d-44ee-b6da-aede72231f23` | Fallos bloquean el merge | Verificar en Settings → Branches que CI es required check |

```bash
# Reportar cada CA cumplido:
curl -s -X POST "http://77.42.88.106:3000/api/tasks/MS-138/criteria/{criteriaId}/fulfill" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "met", "evidence": "descripción de evidencia"}'
```

---

## 10. Devlog Entries — Qué Registrar

```bash
POST http://77.42.88.106:3000/api/tasks/MS-138/devlog-entries
{"categoryCode": "decision", "severity": null, "title": "...", "reportedBy": "322e3745-9756-4a7c-af11-44b33edef44d"}
```

| Cuándo | categoryCode | severity |
|--------|-------------|----------|
| Decisión sobre qué steps incluir en el CI | `decision` | null |
| Si MS-137 no está mergeado y los scripts no existen | `blocker` | high |
| Si branch protection no permite requerir el check | `risk` | high |
| Resultado del PR de prueba | `testing_note` | null |

---

## 11. Workflow (13 pasos)

**0.** Obtener JWT (ver mensaje del sistema en comentario de la tarea)

**1.** Mover MS-138 a in_progress:
```bash
curl -s -X PATCH http://77.42.88.106:3000/api/tasks/MS-138/status \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"statusId":"2a76888a-e595-4cfc-ac4c-a3ae5087ef56","changedBy":"322e3745-9756-4a7c-af11-44b33edef44d"}'
```

**2.** Verificar que MS-137 está mergeado en main (scripts lint/build disponibles)

**3.** Verificar si `.github/workflows/` ya existe en el repo

**4.** Crear branch `feature/MS-138` desde main SHA via GitHub API

**5.** Crear `.github/workflows/ci.yml` via GitHub API (sección 5)

**6.** Crear PR hacia main

**7.** Registrar devlog entries durante la implementación

**8.** Crear PR de prueba para verificar que el CI se dispara y es verde (sección 6.2)

**9.** Reportar CAs cumplidos en VTT

**10.** Crear Development Log

**11.** Verificar review gate:
```bash
curl -s "http://77.42.88.106:3000/api/tasks/MS-138/review-gate" -H "Authorization: Bearer $TOKEN"
```

**12.** Mover a in_review:
```bash
curl -s -X PATCH http://77.42.88.106:3000/api/tasks/MS-138/status \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"statusId":"1ec975a5-7581-4a1a-ab8f-51b1a7ef868d","changedBy":"322e3745-9756-4a7c-af11-44b33edef44d"}'
```

**13.** Enviar reporte de entrega (SKL-REPORT-01) como comentario en la tarea

---

## 12. Notas

- El CI smoke **no incluye tests** — el proyecto aún no los tiene. El step de lint + build es suficiente para esta fase
- Si MS-137 no está mergeado, `npm run lint` fallará porque el script no existe en `package.json`. En ese caso: registrar devlog blocker, esperar merge de MS-137, luego continuar
- Para que los fallos bloqueen el merge: en GitHub → Settings → Branches → main → Edit → "Require status checks to pass" → agregar `Build + Lint`
- Este CI es distinto al auto-merge (MS-145): el auto-merge usa Claude Code Review. El CI smoke valida build/lint. Ambos conviven

---

**Generado por**: TL (Martin Rivas)
**Fecha**: 2026-05-02
**Version**: 1.0
