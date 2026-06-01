# ASSIGNMENT — VTS-001 — Fix regex VTT.SCRIPT-MAN-001 v1.4

| Campo | Valor |
|---|---|
| **Task ID** | VTS-001 |
| **Asignado a** | Coordinator (`51af43cf-8939-4a6f-99ee-31238cfd6894`) |
| **Worktree asignado** | N/A — el Coordinator opera directo en `virtual-teams-setup/` (sin worktree, igual que TL Reviewer por PROTOCOL-WT-001 v1.1) |
| **Branch** | `feature/VTS-001` |
| **Base ref** | `main` (al momento de crear branch) |
| **PR target** | `main` |
| **Estimación** | 1h |

---

## 1. Rol y agente asignado

**Rol:** Coordinator (vtt-setup) — `coord`
**Agente:** Process Coordinator & Reviewer
**Operativo de referencia:** N/A (rol nuevo, sin OPERATIVO formal aún)

> El Coordinator opera bajo el modelo de PROTOCOL-WT-001 v1.1 §2 — reviewers no usan worktrees. Operación directa en `virtual-teams-setup/`.

---

## 2. Scope

### 2.1 Qué SÍ hacer

- Modificar `parse_report_sections()` en `VTT.SCRIPT-MAN-001_gen_task_manifest.py` línea ~207
- Bumpear versión del script v1.3 → v1.4
- Agregar entrada changelog v1.4 en el header
- Crear CODE_LOGIC.md del script
- Crear Development Log
- Crear BRIEF + ASSIGNMENT
- Commit + push + PR a `main`
- Subir attachments a VTS-001 (BRIEF, ASSIGNMENT, devlog, code_logic)
- Reportar CAs cumplidos (PATCH /api/tasks/VTS-001/criteria/:cid)
- Postear SKL-REPORT-01 como comment + mover tarea a `task_in_review`

### 2.2 Qué NO hacer

- NO reprocesar manifests históricos (datos viejos quedan como están)
- NO refactorizar otras partes del script no relacionadas
- NO agregar tests unitarios formales (queda como deuda técnica derivada)
- NO modificar el lookahead de corte de las secciones
- NO subir archivos fuera de `00-platform/02.normativa/` y `knowledge/`
- NO commit directo a `main`
- NO postear datos sensibles en VTT (RULE-SEC-001)

---

## 3. Inputs (archivos a leer, paths exactos)

| Archivo | Por qué |
|---|---|
| `00-platform/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py` | El script a modificar |
| `Reportes/Edicion/edicion.md` (líneas que mencionen VTT-870) | Contexto del bug reportado por TL VTT (referencia opcional) |
| `00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-MAN-001_gobernanza_manifest.md` | Protocolo que rige el manifest — para validar que el fix no rompe gobernanza |

---

## 4. Outputs esperados (archivos a crear/modificar)

| Path | Acción | Versión |
|---|---|---|
| `00-platform/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py` | Modificar (regex + header + changelog) | v1.3 → v1.4 |
| `knowledge/code-logic/scripts/manifest/VTT.SCRIPT-MAN-001.LOGIC.md` | Crear | nuevo |
| `knowledge/development-log/2026-06-01_VTS-001_fix-regex-script-man-001.md` | Crear | nuevo |
| `knowledge/agent-tasks/briefs/BRIEF_VTS-001_fix-regex-script-man-001.md` | Crear | nuevo |
| `knowledge/agent-tasks/assignments/ASSIGNMENT_VTS-001_fix-regex-script-man-001.md` | Crear (este archivo) | nuevo |

---

## 5. Criterios de aceptación (criteriaIds del BRIEF cargados en VTT)

Ver §4 del BRIEF — 17 criterios:
- 12 DoD (compilación, tests, CODE_LOGIC, devlog, commit format, PR)
- 2 integración (cero regresión + 6 secciones extraen OK)
- 3 acceptance específicos del bug (regex `:?`, test inline, changelog v1.4)

---

## 6. Comandos (verificados contra entorno real)

### 6.1 Autenticación

```bash
TOKEN_RESP=$(curl -s -X POST https://api.vttagent.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"coordinator@vtt-setup.vtt.ai","password":"<COORD_PASSWORD>"}')
TOKEN=$(echo "$TOKEN_RESP" | python -c "import sys,json; print(json.load(sys.stdin)['data']['token'])")
```

> Password del Coordinator: ver chat privado con PM (no postear en VTT).

### 6.2 Mover tarea a in_progress

```bash
curl -s -X PATCH "https://api.vttagent.com/api/tasks/VTS-001/status" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"statusId":"2a76888a-e595-4cfc-ac4c-a3ae5087ef56","changedBy":"51af43cf-8939-4a6f-99ee-31238cfd6894"}'
```

### 6.3 Git (branch + commit + push + PR)

```bash
cd c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup
git checkout -b feature/VTS-001
# (cambios al script + creación de archivos LOGIC/devlog/BRIEF/ASSIGNMENT)
git add -A
git commit -m "<mensaje estructurado — ver §10 del devlog>"
git push -u origin feature/VTS-001
gh pr create --title "[VTS-001] Fix regex parse_report_sections acepta ':' final" --body "Ver devlog: knowledge/development-log/2026-06-01_VTS-001_*.md" --base main
```

### 6.4 Subir attachments a VTS-001

```bash
# BRIEF
curl -s -X POST "https://api.vttagent.com/api/tasks/VTS-001/attachments" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@knowledge/agent-tasks/briefs/BRIEF_VTS-001_fix-regex-script-man-001.md;type=text/markdown" \
  -F "fileType=brief" \
  -F "uploadedById=51af43cf-8939-4a6f-99ee-31238cfd6894"

# ASSIGNMENT
curl -s -X POST "https://api.vttagent.com/api/tasks/VTS-001/attachments" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@knowledge/agent-tasks/assignments/ASSIGNMENT_VTS-001_fix-regex-script-man-001.md;type=text/markdown" \
  -F "fileType=assignment" \
  -F "uploadedById=51af43cf-8939-4a6f-99ee-31238cfd6894"

# DEVLOG
curl -s -X POST "https://api.vttagent.com/api/tasks/VTS-001/attachments" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@knowledge/development-log/2026-06-01_VTS-001_fix-regex-script-man-001.md;type=text/markdown" \
  -F "fileType=devlog" \
  -F "uploadedById=51af43cf-8939-4a6f-99ee-31238cfd6894"

# CODE_LOGIC
curl -s -X POST "https://api.vttagent.com/api/tasks/VTS-001/attachments" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@knowledge/code-logic/scripts/manifest/VTT.SCRIPT-MAN-001.LOGIC.md;type=text/markdown" \
  -F "fileType=code_logic" \
  -F "uploadedById=51af43cf-8939-4a6f-99ee-31238cfd6894"
```

### 6.5 Mover a in_review

```bash
curl -s -X PATCH "https://api.vttagent.com/api/tasks/VTS-001/status" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"statusId":"1ec975a5-7581-4a1a-ab8f-51b1a7ef868d","changedBy":"51af43cf-8939-4a6f-99ee-31238cfd6894"}'
```

---

## 7. Fuentes de verdad

- **Script a modificar:** `00-platform/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py` (línea 207)
- **Origen del bug:** VTT-870 (proyecto VTT) reportado por TL Reviewer VTT
- **Protocolo del manifest:** `VTT.PROTOCOL-MAN-001_gobernanza_manifest.md`
- **Schema del manifest:** definido inline en el script (`build_v10` y `build_v15`)

---

## 8. Validación (cómo el TL VTT va a verificar al revisar)

1. **Review Gate verde** — `GET /api/tasks/VTS-001/review-gate` → `canProceedToReview: true`
2. **Criterios met** — 17/17 criterios en estado `met` con evidencia
3. **Attachments completos** — 4 attachments (brief + assignment + devlog + code_logic) subidos a VTS-001
4. **PR existe y mergeable** — `gh pr view <PR>` → `mergeable: MERGEABLE`, sin conflictos
5. **Validación inline del regex** — TL VTT puede correr el test Python del §5.1 del BRIEF y obtener `OK`
6. **Versionado correcto** — `grep "Version: 1.4"` en el script matchea + entrada changelog presente
7. **Sin datos sensibles** — devlog/BRIEF/ASSIGNMENT no contienen IPs prod, paths absolutos `/root/`, credenciales (RULE-SEC-001)
