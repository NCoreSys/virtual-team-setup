# Development Log — MS-145: Auto-merge workflow (Claude Code Review) en memory-service-backend

## Informacion General

| Campo | Valor |
|-------|-------|
| Fecha | 2026-05-02 |
| Tarea | MS-145 |
| Repo | NCoreSys/memory-service-backend |
| Branch | feature/MS-145 |
| PR | #2 — https://github.com/NCoreSys/memory-service-backend/pull/2 |
| Agente | DevOps Agent (DO) |

---

## Resumen

Creacion de los 2 workflows de GitHub Actions en `NCoreSys/memory-service-backend`, replicando
el pipeline existente en VTT:

1. **claude-code-review.yml** — dispara revision de Claude Code en cada PR
2. **auto-merge.yml** — mergea automaticamente si el review pasa

Los archivos fueron creados via GitHub API (Opcion A del brief) directamente en branch
`feature/MS-145` sin necesidad de clonar el repo localmente.

---

## Archivos Creados

| Archivo | SHA commit | Descripcion |
|---------|-----------|-------------|
| `.github/workflows/claude-code-review.yml` | `2e9e616d7ac1b70fe31d67de34f4a9875372de8b` | Workflow Claude Code Review |
| `.github/workflows/auto-merge.yml` | `ec5db2c5ec786d95ef5c84a6efdb5e0447700ef9` | Workflow auto-merge post-review |

---

## Estado de Secrets

| Secret | Estado | Accion requerida |
|--------|--------|-----------------|
| `GH_PATH` | ❌ NO configurado | Martin debe agregar via GitHub Settings |
| `CLAUDE_CODE_OAUTH_TOKEN` | ❌ NO configurado | Martin debe agregar via GitHub Settings |
| `MEMORY_SERVICE_KEY` | ✅ Ya existia | Configurado en sesion anterior (MS-129) |

### Para configurar los secrets faltantes

```bash
gh secret set GH_PATH --repo NCoreSys/memory-service-backend
gh secret set CLAUDE_CODE_OAUTH_TOKEN --repo NCoreSys/memory-service-backend
# (gh pedira el valor interactivamente)
```

O via GitHub UI: **Settings → Secrets and variables → Actions → New repository secret**

Los valores son los mismos que usa VTT — consultarlos con el Coordinador.

---

## Verificaciones

```bash
# Workflows en el branch
gh api repos/NCoreSys/memory-service-backend/contents/.github/workflows \
  --ref feature/MS-145 --jq '[.[].name]'
# → ["auto-merge.yml","claude-code-review.yml"]

# Secrets actuales (solo muestra nombres, no valores)
gh api repos/NCoreSys/memory-service-backend/actions/secrets --jq '[.secrets[].name]'
# → ["MEMORY_SERVICE_KEY"]  (GH_PATH y CLAUDE_CODE_OAUTH_TOKEN PENDIENTES)
```

---

## Decisiones Tecnicas

1. **GitHub API (Opcion A)**: Se uso la API REST directamente en vez de git local para evitar
   el problema de path duality (Windows bash /tmp/ vs C:\tmp\) presente en sesiones anteriores.
2. **Identicos a VTT**: Los workflows no fueron modificados — copia exacta del brief para
   garantizar paridad con el pipeline que ya funciona en produccion.
3. **merge_method: squash**: Mantiene historial limpio, igual que VTT.

---

## Pendientes

- [ ] Martin configura `GH_PATH` en GitHub Secrets del repo
- [ ] Martin configura `CLAUDE_CODE_OAUTH_TOKEN` en GitHub Secrets del repo
- [ ] Verificar end-to-end: crear PR de prueba y confirmar que Claude revisa y mergea

---

## Como Probar (despues de configurar secrets)

```bash
# 1. Crear branch de prueba
git checkout -b test/workflow-check
echo "# workflow test" >> .workflow-test
git add .workflow-test
git commit -m "test: verificar workflow auto-merge"
git push origin test/workflow-check

# 2. Crear PR
gh pr create --title "test: verificar Claude Code Review + auto-merge" \
  --base main --repo NCoreSys/memory-service-backend

# 3. Verificar en GitHub Actions tab que se dispara claude-code-review
# 4. Si review pasa -> auto-merge debe ejecutarse automaticamente
```
