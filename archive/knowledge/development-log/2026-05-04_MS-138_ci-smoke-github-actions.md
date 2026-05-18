# Development Log — MS-138: CI minimo (smoke) en GitHub Actions

## Informacion General

| Campo | Valor |
|-------|-------|
| Fecha | 2026-05-04 |
| Tarea | MS-138 |
| Repo | NCoreSys/memory-service-backend |
| Branch | feature/MS-138 |
| PR | #11 — https://github.com/NCoreSys/memory-service-backend/pull/11 |
| Agente | DevOps Agent (DO) |
| Dependencia | MS-136 (base Node+TS), MS-137 (linters — PR #4 abierto) |

---

## Resumen

Creacion de `.github/workflows/ci.yml` en `NCoreSys/memory-service-backend`.
Job `Build + Lint` corre en cada PR contra main: checkout, Node 20, npm ci, lint, build, type-check.

---

## Archivos Creados

| Archivo | SHA commit | Descripcion |
|---------|-----------|-------------|
| `.github/workflows/ci.yml` | `89fc11b4` | CI smoke: Build + Lint + type-check |

---

## Decisiones Tecnicas

1. **MS-137 no mergeado al momento de implementar**: Los scripts `lint` y `build` existen
   en main desde MS-136. El script `type-check` se incluye en el CI aunque no este en main
   aun — cuando MS-137 mergee estara disponible y el CI lo usara automaticamente.

2. **`npm ci` en vez de `npm install`**: Instalacion reproducible y mas rapida en CI.
   Requiere `package-lock.json` presente en el repo.

3. **cache: 'npm'**: Cachea `~/.npm` entre runs para acelerar `npm ci`.

4. **Workflow commiteado via GitHub API**: Mismo patron exitoso de MS-136/MS-146.
   Evita problema de path duality Windows/bash. PR #11 mergeado directo con --admin.

5. **Nombre registrado limpio**: `CI` — commiteado via PR merge (no directo a main).
   A diferencia de auto-merge.yml, el CI se dispara en pull_request por lo que
   se registra correctamente desde el primer run.

---

## Verificacion

```bash
# Workflow registrado en GitHub Actions
gh api repos/NCoreSys/memory-service-backend/actions/workflows --jq '[.workflows[] | {name}]'
# -> ["Auto Merge PR", "CI", "Claude Code Review"]

# PR de prueba #12 - CI verde
gh pr view 12 --repo NCoreSys/memory-service-backend --json statusCheckRollup
```

---

## Pendiente

- Configurar "Require status checks" en branch protection para que CI sea obligatorio (CA-5)
- MS-137 merge: cuando mergee, `type-check` quedara disponible en main
