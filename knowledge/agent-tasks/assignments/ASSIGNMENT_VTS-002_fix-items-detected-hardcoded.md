# ASSIGNMENT — VTS-002 — Fix items_detected hardcoded

| Campo | Valor |
|---|---|
| **Task ID** | VTS-002 |
| **Asignado a** | Coordinator (`51af43cf-...`) |
| **Worktree** | N/A — Coordinator opera directo en `virtual-teams-setup/` |
| **Branch** | `feature/VTS-001-002-003` (consolidado con VTS-001 y VTS-003 — todos al mismo script) |
| **Base ref** | `main` |
| **PR target** | `main` |
| **Estimación** | 0.5h |

---

## 1. Rol y agente

Coordinator (`coord`). Mismo modelo operativo que VTS-001 (sin worktree, PROTOCOL-WT-001 v1.1 §2).

## 2. Scope

### SÍ

- Reemplazar `[]` hardcoded por llamada al helper `_extract_list_items(report_sections.get("items_detected"))` en línea ~509 de `build_v10()`
- El helper se crea en VTS-003 (mismo PR)
- Bumpear v1.4 → v1.5 (consolidado)
- Actualizar CODE_LOGIC con D-MAN-005
- Devlog + BRIEF + ASSIGNMENT
- Subir attachments a VTS-002
- Reportar CAs + SKL-REPORT-01 + mover a in_review

### NO

- No tocar otros campos hardcoded por diseño
- No refactorizar más allá del helper
- No regenerar manifests históricos
- No commit a main directo
- RULE-SEC-001 — no postear datos sensibles en VTT

## 3. Inputs

- `00-platform/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py` (script a modificar)
- BRIEF de VTS-002 (este archivo + el BRIEF)

## 4. Outputs

| Path | Acción |
|---|---|
| `VTT.SCRIPT-MAN-001_gen_task_manifest.py` | Modificar línea ~509 + header v1.5 + changelog |
| `knowledge/code-logic/scripts/manifest/VTT.SCRIPT-MAN-001.LOGIC.md` | Actualizar con D-MAN-005 |
| `knowledge/development-log/2026-06-01_VTS-002_*.md` | Crear |
| `knowledge/agent-tasks/briefs/BRIEF_VTS-002_*.md` | Crear |
| `knowledge/agent-tasks/assignments/ASSIGNMENT_VTS-002_*.md` | Crear (este archivo) |

## 5. Criterios

17 totales (12 DoD + 2 integración + 3 acceptance). Ver §4 del BRIEF.

## 6. Comandos

Mismo workflow que VTS-001 (auth → PATCH in_progress → branch → fix → entregables → commit → push → PR → attachments → SKL-REPORT-01 → in_review). Ver `ASSIGNMENT_VTS-001_*.md` §6 para detalle.

**Status UUIDs:**
- task_in_progress: `2a76888a-e595-4cfc-ac4c-a3ae5087ef56`
- task_in_review: `1ec975a5-7581-4a1a-ab8f-51b1a7ef868d`

## 7. Validación TL

1. Review Gate verde
2. Criterios met (17/17)
3. 4 attachments subidos
4. PR mergeable
5. Test inline del helper con `items_detected` devuelve items NO vacíos
6. Línea ~509 ya no contiene `: []` hardcoded
7. Sin datos sensibles (RULE-SEC-001)
