# Code Logic — MS-144: Gobernanza GitHub 4 repos

## Informacion General

| Campo | Valor |
|-------|-------|
| Tarea | MS-144 / INIT-E-01 |
| Tipo | Infrastructure / GitHub Governance |
| Fecha | 2026-05-01 |

---

## Proposito

Implementar ADR-001 Fases 1+2: Fine-grained PATs por rol y branch protection
en los 4 repos de NCoreSys para el Memory Service.

---

## Componentes Configurados

### Branch Protection (los 4 repos)

Reglas activas en `main` de cada repo:

| Regla | Valor | Razon |
|-------|-------|-------|
| enforce_admins | true | Aplica a todos, sin bypass |
| required_approving_review_count | 1 | Al menos 1 reviewer |
| dismiss_stale_reviews | true | Nuevo commit invalida aprobacion anterior |
| allow_force_pushes | false | Protege historial de main |
| allow_deletions | false | Protege rama main de borrado accidental |

### Security Features

- **Vulnerability alerts (Dependabot)**: activado via `PUT /repos/{org}/{repo}/vulnerability-alerts`
- **Secret scanning**: activado via `PATCH /repos/{org}/{repo}` con `security_and_analysis`

### PATs (Fine-grained, pendiente creacion manual)

| PAT | Scope | Repos |
|-----|-------|-------|
| PAT_MEM_BE | Contents + PRs Write | memory-service-backend |
| PAT_MEM_FE | Contents + PRs Write | memory-service-frontend |
| PAT_MEM_DO | Contents + PRs Write | memory-service-project, memory-service-api |
| PAT_MEM_TL | Contents + PRs Write | todos (4 repos) |
| PAT_MEM_PM | Write project, Read resto | memory-service-project (W) + 3 restantes (R) |

---

## Comandos gh CLI Usados

```bash
# Verificar branch protection
gh api repos/NCoreSys/<repo>/branches/main/protection

# Activar Dependabot
gh api repos/NCoreSys/<repo>/vulnerability-alerts --method PUT

# Activar secret scanning
gh api repos/NCoreSys/<repo> --method PATCH \
  -f "security_and_analysis[secret_scanning][status]=enabled"
```

---

## Referencias

- ADR-001 §D-ADR-001-A: PATs por rol
- ADR-001 §D-ADR-001-B: Branch protection rules
- Inventario PATs: `knowledge/pat-inventory/PAT_INVENTORY.md`

---

## Historial de Cambios

| Fecha | Cambio | Autor |
|-------|--------|-------|
| 2026-05-01 | Creacion — branch protection verificada, security activada, PAT inventory creado | DO Agent |
