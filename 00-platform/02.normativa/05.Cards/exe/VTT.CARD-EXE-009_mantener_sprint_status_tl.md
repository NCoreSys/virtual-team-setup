# VTT.CARD-EXE-009 — TL mantiene SPRINT_STATUS_SX.md

| Campo | Valor |
|---|---|
| **Código** | `VTT.CARD-EXE-009` |
| **Tipo** | `CARD-std` |
| **Versión** | 1.0 |
| **Aplica cuando** | `task.phase IN [execution, review, closing] AND agent.role = TL` |
| **Requiere Cards previas** | ninguna |
| **Pertenece a** | WORKFLOW-ASG-001.028 |
| **Tokens estimados** | ~950 |

---

## Qué hacer (TL)

Mantener `knowledge/sprints/<sprint>/SPRINT_STATUS_<sprint>.md` actualizado **durante todo el sprint** — al MOMENTO del evento, NO batchear al final del día.

## Trigger events

| Evento | Cuándo |
|---|---|
| `task_in_progress_started` | Agente movió a in_progress |
| `task_in_review_received` | Agente entregó (FASE 3 → 4) |
| `task_approved` | TL aprobó en FASE 4 |
| `task_on_hold_authorized` | TL autorizó on_hold (FASE 3.5) |
| `issue_created` | Issue creado |
| `blocker_detected` | Blocker cross-tarea detectado |
| `daily_sync` | 1/día al iniciar sesión |
| `manual_update` | Ajuste manual |

## Ejecución

```bash
python $VTT_SETUP/02.normativa/04.Scripts/status/SCRIPT-STATUS-003_update_sprint_status.py \
  --sprint "$SPRINT" \
  --status-path "$SPRINT_STATUS_PATH" \
  --trigger-event "$TRIGGER_EVENT" \
  --sprint-id "$SPRINT_ID" \
  --tl-name "<nombre>"
```

El script consulta VTT y regenera §1-§5 desde datos reales. **Preserva §6** (próximos pasos del TL — solo manual).

## Estructura obligatoria (7 secciones)

1. **Resumen** — sprint, fechas, progreso, última actualización
2. **Tareas por estado** — 🟢 approved / 🟤 in_review / 🔵 in_progress / 🟠 on_hold / 🟡 pending / 🔴 blocked
3. **Blockers activos** — tabla con tarea + tipo + descripción + acción TL + fecha
4. **Issues abiertos** — tabla con issue + severidad + tipo + asignado
5. **KPIs** — tasa aprobación, tiempo P50 review, issues abiertos, hardcode findings reales (debe ser 0 al cierre)
6. **Próximos pasos del TL** — checklist editable manualmente (NO sobrescribe)
7. **Historial de cambios** — append-only

## Después de cada actualización

```bash
git add $SPRINT_STATUS
git commit -m "chore(sprint): SPRINT_STATUS_<sprint>.md — <trigger_event>

- Tarea(s) afectada(s): <lista>

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"

git push origin <branch_tl>
```

## Reglas

- **R1:** Actualizar al MOMENTO del evento, NO batchear.
- **R3:** NO duplicar info de VTT — referenciar links.
- **R6:** SPRINT_STATUS es fuente del sprint actual; TASK_TRACKING es agregada multi-sprint.
- **NO se firma** — es operativo del TL, no entregable del sprint.
- **NO bloquea cierre** del sprint si no está actualizado al 100%.

## Diferencia con CIERRE_S<N>.md

| | SPRINT_STATUS | CIERRE_S<N> |
|---|---|---|
| Cuándo | Vivo (durante sprint) | Final del sprint |
| Firma | NO | SÍ |
| Update | Múltiples por día | 1 vez |
| Bloquea | NO | SÍ cierre formal |

## Si falla

| Síntoma | Acción |
|---|---|
| Conflicto en git push | `git pull --rebase` + reintentar |
| Discrepancia con TASK_TRACKING | SPRINT_STATUS es fuente del sprint actual (R6) |
| Markdown inválido | Validar con `markdownlint` antes de commit |
| Sección §6 perdida | El script preserva §6 — verificar versión del script |

## Output

Dashboard actualizado + commit. **Cualquier TL que retome el sprint tiene contexto completo sin perder horas de re-investigación.**

Lección Memory Service S1-S2: TL perdía contexto del sprint en sesiones largas → este dashboard resuelve eso.
