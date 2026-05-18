# Development Log — MS-122: INIT-B-01 Crear y verificar repo Git

## Información General

| Campo | Valor |
|-------|-------|
| **Fecha** | 2026-04-24 |
| **Tarea** | MS-122 / INIT-B-01 |
| **Agente** | DevOps Engineer (DO) |
| **Repos afectados** | NCoreSys/memory-service-project, memory-service-api, memory-service-backend, memory-service-frontend |

---

## Resumen

Se verificaron, inicializaron y configuraron los 4 repositorios del proyecto Memory Service
bajo la organización NCoreSys en GitHub. Se aplicó branch protection en `main` de los 4 repos.

---

## Pasos Ejecutados

| Paso | Acción | Resultado |
|------|--------|-----------|
| 0 | Crear rama `feature/MS-122` | ✅ |
| 1 | Verificar MS-122 en `task_in_progress` | ✅ (ya en in_progress) |
| 2 | Obtener JWT credenciales DO | ✅ |
| 3 | Verificar existencia 4 repos | ✅ (project + api tenían main; backend + frontend vacíos) |
| 4 | Corregir remote local | ✅ → NCoreSys/memory-service-project.git |
| 5 | Inicializar `main` en backend y frontend | ✅ commit inicial + push |
| 6 | Branch protection en `main` (4 repos) | ✅ aplicada en NCoreSys |
| 7 | Vulnerability alerts | ✅ activados en 4 repos |
| 8 | Verificar clone | ✅ clone funciona con URL NCoreSys |

---

## Decisiones Técnicas

### Cambio de org: prompt-ai-studio → NCoreSys

Los repos fueron creados inicialmente en la cuenta `prompt-ai-studio` (cuenta de usuario, plan Free).
Branch protection en repos privados requiere GitHub Pro (usuarios) o GitHub Team (organizaciones).

Al intentar aplicar branch protection en `prompt-ai-studio` se recibió:
```
HTTP 403: Upgrade to GitHub Pro or make this repository public
```

Se detectó que `prompt-ai-studio` tiene permisos de Owner en la org `NCoreSys` (que sí tiene
plan Team). Se recrearon los 4 repos bajo NCoreSys donde branch protection funcionó correctamente.

Los repos de `prompt-ai-studio` quedan pendientes de borrado manual por el PM (requiere scope
`delete_repo` no disponible en el token actual).

### Remote local corregido

El repo local en `C:\Users\Martin\Documents\virtual-teams\memory-service\` apuntaba a
`twitter-react.git` (KeepCodingWeb17). Corregido a `NCoreSys/memory-service-project.git`.

---

## Repos Finales

| Repo | URL | main | Branch Protection |
|------|-----|------|-------------------|
| memory-service-project | https://github.com/NCoreSys/memory-service-project | ✅ | ✅ |
| memory-service-api | https://github.com/NCoreSys/memory-service-api | ✅ | ✅ |
| memory-service-backend | https://github.com/NCoreSys/memory-service-backend | ✅ | ✅ |
| memory-service-frontend | https://github.com/NCoreSys/memory-service-frontend | ✅ | ✅ |

**Branch protection config aplicada:**
- required_approving_review_count: 1
- dismiss_stale_reviews: true
- enforce_admins: true
- allow_force_pushes: false
- allow_deletions: false

---

## Pendientes

- [ ] PM: borrar manualmente repos de `prompt-ai-studio` (4 repos, Settings → Danger Zone)
- [ ] Actualizar ADR-001 con nueva org (NCoreSys en lugar de prompt-ai-studio)

---

## Cómo verificar

```bash
# Verificar branch protection
gh api repos/NCoreSys/memory-service-project/branches/main/protection \
  --jq '{force_pushes: .allow_force_pushes.enabled, deletions: .allow_deletions.enabled, reviews: .required_pull_request_reviews.required_approving_review_count}'

# Verificar clone
git clone https://github.com/NCoreSys/memory-service-project.git
```
