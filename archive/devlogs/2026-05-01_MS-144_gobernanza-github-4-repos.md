# Development Log — MS-144 / INIT-E-01: Gobernanza GitHub 4 repos

## Informacion General

| Campo | Valor |
|-------|-------|
| Fecha | 2026-05-01 |
| Tarea | MS-144 / INIT-E-01 |
| Repo | NCoreSys/memory-service-project |
| Branch | feature/MS-144 |
| Agente | DevOps Agent (DO) |

---

## Resumen

Implementacion de gobernanza GitHub para los 4 repos del Memory Service en org NCoreSys.
Branch protection verificada activa en los 4 repos. Secret scanning y Dependabot activados.
PAT_INVENTORY.md creado — PATs pendientes de creacion manual por Coordinador.

Nota: el assignment menciona org `prompt-ai-studio` pero los repos ya fueron migrados a
`NCoreSys` en MS-122. Se trabajo sobre NCoreSys correctamente.

---

## Paso 3: Verificacion de ramas main

```
NCoreSys/memory-service-project: main OK
NCoreSys/memory-service-api:     main OK
NCoreSys/memory-service-backend: main OK
NCoreSys/memory-service-frontend: main OK
```

## Paso 5: Branch protection — verificacion

Output de `gh api repos/NCoreSys/<repo>/branches/main/protection`:

```json
{
  "enforce_admins": true,
  "required_reviews": 1,
  "allow_force_pushes": false,
  "allow_deletions": false,
  "dismiss_stale": true
}
```

Estado identico en los 4 repos. Branch protection ya estaba configurada desde MS-122.
Verificacion confirma que todos los campos del ADR-001 §D-ADR-001-B estan correctos.

## Paso 6: Security features activadas

```
NCoreSys/memory-service-project  vulnerability alerts: OK
NCoreSys/memory-service-api      vulnerability alerts: OK
NCoreSys/memory-service-backend  vulnerability alerts: OK
NCoreSys/memory-service-frontend vulnerability alerts: OK

NCoreSys/memory-service-project  secret scanning: enabled
NCoreSys/memory-service-api      secret scanning: enabled
NCoreSys/memory-service-backend  secret scanning: enabled
NCoreSys/memory-service-frontend secret scanning: enabled
```

## Paso 4: PATs (accion manual del Coordinador)

Los Fine-grained PATs NO se pueden crear via API — requieren creacion manual en github.com.
PAT_INVENTORY.md creado con metadata de los 5 PATs requeridos. Pendiente que el
Coordinador los cree siguiendo las instrucciones del inventario.

PATs requeridos:
- PAT_MEM_BE: Write en memory-service-backend
- PAT_MEM_FE: Write en memory-service-frontend
- PAT_MEM_DO: Write en memory-service-project, memory-service-api
- PAT_MEM_TL: Write en los 4 repos
- PAT_MEM_PM: Write en memory-service-project, Read en resto

---

## Archivos Creados

| Archivo | Descripcion |
|---------|-------------|
| `knowledge/pat-inventory/PAT_INVENTORY.md` | Inventario de PATs sin valores |
| `devlogs/2026-05-01_MS-144_gobernanza-github-4-repos.md` | Este DevLog |
| `knowledge/code-logic/phase1/MS-144_github-governance.LOGIC.md` | Code Logic |

---

## Decisiones Tecnicas

1. **Repos en NCoreSys, no prompt-ai-studio**: el assignment menciona prompt-ai-studio pero
   los repos fueron migrados a NCoreSys en MS-122 (org con Teams plan). Se trabajo sobre
   NCoreSys que es el estado real actual.

2. **Branch protection ya estaba configurada**: MS-122 la configuro al crear los repos.
   Esta tarea verifica y documenta el estado, y activa las security features adicionales.

3. **PATs pendientes**: los Fine-grained PATs requieren accion manual del Coordinador.
   Siguiendo PROJECT_RULES 15.3 (no mock), se documenta como pendiente.
