# ASSIGNMENT — VTS-003 — Fix how_to_verify parser limitado

| Campo | Valor |
|---|---|
| **Task ID** | VTS-003 |
| **Asignado a** | Coordinator (`51af43cf-...`) |
| **Worktree** | N/A |
| **Branch** | `feature/VTS-001-002-003` (consolidado) |
| **Base ref** | `main` |
| **PR target** | `main` |
| **Estimación** | 1h |

---

## 1. Rol y agente

Coordinator (`coord`). Mismo modelo operativo que VTS-001.

## 2. Scope

### SÍ

- Crear helper `_extract_list_items(section_text)` que acepta bullets + numerados + párrafos
- Reemplazar lógica inline de `how_to_verify` (línea ~511) por llamada al helper
- Compartir helper con VTS-002 (`items_detected`)
- Bumpear script v1.4 → v1.5 (consolidado)
- Actualizar CODE_LOGIC con §2.2.bis + D-MAN-006, D-MAN-007
- 13 tests del helper
- Devlog + BRIEF + ASSIGNMENT
- Subir attachments a VTS-003
- Reportar CAs + SKL-REPORT-01 + mover a in_review

### NO

- No refactorizar `findings`, `adrs`, `derived_tasks` al helper aún
- No regenerar manifests históricos
- No commit a main directo
- RULE-SEC-001 — no postear datos sensibles

## 3. Inputs

- `00-platform/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py`
- BRIEF de VTS-003

## 4. Outputs

| Path | Acción |
|---|---|
| `VTT.SCRIPT-MAN-001_gen_task_manifest.py` | Helper nuevo + línea ~511 modificada + header v1.5 + changelog |
| `knowledge/code-logic/scripts/manifest/VTT.SCRIPT-MAN-001.LOGIC.md` | §2.2.bis nuevo + D-MAN-006, D-MAN-007 |
| `knowledge/development-log/2026-06-01_VTS-003_*.md` | Crear |
| `knowledge/agent-tasks/briefs/BRIEF_VTS-003_*.md` | Crear |
| `knowledge/agent-tasks/assignments/ASSIGNMENT_VTS-003_*.md` | Crear (este archivo) |

## 5. Criterios

18 totales (12 DoD + 2 integración + 4 acceptance). Ver §4 del BRIEF.

## 6. Comandos

Mismo workflow que VTS-001. Ver `ASSIGNMENT_VTS-001_*.md` §6.

## 7. Validación TL

1. Review Gate verde
2. Criterios met (18/18)
3. 4 attachments subidos
4. PR mergeable
5. Helper `_extract_list_items` existe y pasa 13 tests
6. Cero regresión con bullets v1.4
7. Pasos numerados y párrafos del REPORT ahora aparecen en `how_to_verify`
8. Sin datos sensibles
