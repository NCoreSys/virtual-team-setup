# TEMPLATE — CLOSURE_S[N].md (Cierre de Sprint)

| Campo | Valor |
|---|---|
| **Código** | `VTT.TEMPLATE-CLO-001` |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-13 |
| **Aplica a** | Cualquier sprint de cualquier proyecto VTT |
| **Generado por** | PJM (durante SubFase 3C de SOP_GENERACION_SPRINT_DOCS) |
| **Consumido por** | PM (sign-off), TL/AR/DL/QA (firmas) |

---

## Notas de uso del template

- Reemplazar todos los `[PLACEHOLDER]` con valores reales del sprint
- Las **firmas** llevan comando API real, no solo checklist en papel
- Si el sprint **NO tiene FE** → eliminar §5 Firma DL y justificar en §0
- Si el sprint **NO tiene QA** → eliminar §6 Firma QA si aplica y justificar en §0
- Los **criterios GO/NO-GO** se copian del `3B.9.9 Capacity Plan §11` correspondiente al milestone
- **NO auto-completar firmas** — cada firma corresponde a un rol y debe ejecutar su comando API
- Reglas críticas del SOP_GENERACION_SPRINT_DOCS §7: R8 (APR-S[N] formal), R9 (firmas API), R11 (firma DL si FE)

---

```markdown
# CLOSURE_S[N] — [Nombre del Sprint]

| Campo | Valor |
|---|---|
| **Sprint** | S[N] — [nombre descriptivo] |
| **Release** | R[X] |
| **Fechas** | YYYY-MM-DD → YYYY-MM-DD |
| **Milestone** | M[N] — [nombre] |
| **Roles activos** | TL, BE, DB, DO, [FE, DL, QA según aplique] |
| **Firmas requeridas** | [N] (TL + AR + DL si FE + QA si aplica) |
| **Fecha cierre planificado** | YYYY-MM-DD |
| **Fecha cierre real** | YYYY-MM-DD |

---

## §0 Resumen ejecutivo (para el PM)

### Qué es este documento

Documento de evidencia del cierre de Sprint S[N]. Contiene:
- Verificación de deliverables completados
- Firmas API de cada rol responsable
- Métricas estimado vs real
- Gate final de aprobación PM

### Firmas requeridas en este sprint

- **TL** — Code Review (development stage)
- **AR** — Integration Audit (integration stage)
- [Si FE en sprint] **DL** — Visual Review (design stage)
- [Si QA en sprint] **QA** — Testing Validation (testing stage)

### Roles ausentes (justificación)

[Si no hay FE]: "Sprint sin Frontend — no requiere firma DL. Sprint enfocado en [BE/DB/DO]."
[Si no hay QA]: "Sprint sin Testing dedicado — validación QA cubierta por CAs verificables del TL."

### Condición de cierre

Todas las firmas requeridas registradas en VTT + APR-S[N] aprobada por PM → Sprint cerrado.

---

## §1 Resumen del Sprint

### Métricas esperadas (del Capacity Plan)

| Métrica | Valor |
|---|---|
| Horas estimadas | [N] h |
| SP estimados | [N] SP |
| Deliverables planificados | [N] |
| Tareas planificadas | [N] |
| Agentes activos | [N] |

### Deliveries en VTT

| Delivery | Rol | Tareas | Status |
|---|---|---|---|
| [DELIVERY-S[N]-BE] | BE | [N] | ⬜ |
| [DELIVERY-S[N]-DB] | DB | [N] | ⬜ |
| [DELIVERY-S[N]-DO] | DO | [N] | ⬜ |
| [DELIVERY-S[N]-REV] | Validación | [N] | ⬜ |

### Milestone gate

**M[N] — [nombre]** definido en `3B.9.9 §11`:
- Criterio GO 1: [criterio verificable]
- Criterio GO 2: [criterio verificable]
- Criterio GO 3: [criterio verificable]

---

## §2 Verificación de Deliverables

### Tabla por Delivery × CA

| Delivery | Tarea | CAs (met/total) | Devlog (resolved/total) | Manifest | Status |
|---|---|---|---|---|---|
| [DEL-BE] | [TASK-001] | ⬜ N/N | ⬜ N/N | ⬜ v1.5 | ⬜ |
| [DEL-BE] | [TASK-002] | ⬜ N/N | ⬜ N/N | ⬜ v1.5 | ⬜ |
| [DEL-DB] | [TASK-010] | ⬜ N/N | ⬜ N/N | ⬜ v1.5 | ⬜ |

**Regla:** Una tarea cuenta como completada solo si:
- Todas las CAs requeridas en `status=met` con evidencia
- Todos los devlog entries en `status=resolved`
- Manifest v1.5 (con `review.tl_review.verdict=approved`) subido
- PR(s) merged a main

---

## §3 Firma TL — Code Review (development stage)

### Criterios de la firma

- [ ] Todas las tareas BE/DB/DO del sprint en `task_completed`
- [ ] Code review aplicado según `CODE_REVIEW_GUIDE_V1.1.md`
- [ ] Modelo dinámico aplicado a cada cierre (TIs + evidencias + devlog resolved)
- [ ] Manifests v1.5 subidos para cada tarea
- [ ] Sin findings critical/high pendientes
- [ ] Hardcode Check ejecutado en todas las tareas con código

### Comando API de firma

```bash
TOKEN=$(curl -s -X POST $BASE/api/auth/service-token \
  -H "Content-Type: application/json" \
  -d "{\"userId\":\"$TL_UUID\",\"serviceKey\":\"$SERVICE_KEY\"}" \
  | python3 -c "import sys,json;print(json.load(sys.stdin)['data']['token'])")

curl -s -X POST "$BASE/api/sprints/$SPRINT_ID/stages/development/sign" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "signedBy": "<TL_UUID>",
    "comment": "Stage development firmado. Todas las tareas BE/DB/DO completadas con modelo dinámico aplicado."
  }'
```

### Firma

| Campo | Valor |
|---|---|
| Reviewer | TL — `<TL_UUID>` |
| Status | ⬜ Pendiente / ✅ Firmado |
| Fecha firma | YYYY-MM-DD HH:MM |
| Sign ID | (auto-generado por API) |

---

## §4 Firma AR — Integration Audit (integration stage)

### Criterios de la firma

- [ ] Integración entre módulos verificada (BE↔DB, BE↔Runtime, etc.)
- [ ] Audit checklist completo según `INTEGRATION_AUDIT_CHECKLIST_V1.1.md`
- [ ] Sin ADRs nuevos pendientes de aprobación
- [ ] Sin riesgos de integración escalados
- [ ] Endpoints respetan SLA NFR

### Comando API de firma

```bash
curl -s -X POST "$BASE/api/sprints/$SPRINT_ID/stages/integration/sign" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "signedBy": "<AR_UUID>",
    "comment": "Stage integration firmado. Audit checklist completo, sin findings críticos."
  }'
```

### Firma

| Campo | Valor |
|---|---|
| Reviewer | AR — `<AR_UUID>` |
| Status | ⬜ Pendiente / ✅ Firmado |
| Fecha firma | YYYY-MM-DD HH:MM |

---

## §5 Firma DL — Visual Review (design stage) — *Solo si hay FE en sprint*

### Criterios de la firma

- [ ] FE respetó design tokens del Design System
- [ ] Componentes implementados según specs UX
- [ ] Sin desviaciones visuales no aprobadas
- [ ] Visual QA ejecutado en navegadores objetivo

### Comando API de firma

```bash
curl -s -X POST "$BASE/api/sprints/$SPRINT_ID/stages/design/sign" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "signedBy": "<DL_UUID>",
    "comment": "Stage design firmado. FE alineado con Design System."
  }'
```

### Firma

| Campo | Valor |
|---|---|
| Reviewer | DL — `<DL_UUID>` |
| Status | ⬜ Pendiente / ✅ Firmado / N/A (sin FE) |
| Fecha firma | YYYY-MM-DD HH:MM |

---

## §6 Milestone M[N] — Verificación GO/NO-GO

### Criterios del milestone (del `3B.9.9 §11`)

| Criterio | Cómo verificar | Resultado |
|---|---|---|
| [Criterio 1 — ej: API endpoints responden <500ms] | [comando o test] | ⬜ GO / NO-GO |
| [Criterio 2] | [comando o test] | ⬜ GO / NO-GO |
| [Criterio 3] | [comando o test] | ⬜ GO / NO-GO |

### Decisión

- ⬜ **GO** — Milestone alcanzado, continuar con S[N+1]
- ⬜ **NO-GO** — Milestone NO alcanzado, ejecutar plan de contingencia §8

---

## §7 Métricas finales (estimado vs real)

| Métrica | Estimado | Real | Varianza |
|---|---|---|---|
| Horas totales | [N] | [N] | [+/- N%] |
| SP completados | [N] | [N] | [+/- N%] |
| Tareas completadas | [N]/[N] | [N]/[N] | [%] |
| Deliverables completados | [N]/[N] | [N]/[N] | [%] |
| Velocity del equipo | — | [SP/sprint] | calibra SOP-VEL-01 |
| Bugs encontrados en review | — | [N] | — |
| Tech debts diferidos a R2 | — | [N] | — |

### Notas de varianza

[Documentar si varianza >15% — razones, impacto en siguientes sprints]

---

## §8 Gate final — PM sign-off

### Checklist de condiciones para aprobación PM

- [ ] §3 Firma TL registrada en VTT
- [ ] §4 Firma AR registrada en VTT
- [ ] §5 Firma DL registrada en VTT (si FE en sprint) / Justificado si no aplica
- [ ] §6 Milestone GO confirmado
- [ ] §7 Métricas reportadas sin desviaciones críticas
- [ ] Plan de contingencia activo si hay NO-GO
- [ ] CONTEXTO_S[N].md generado con IDs VTT para sprint siguiente

### APR-S[N] — Aprobación PM (tarea formal en VTT)

```bash
# Mover tarea APR-S[N] a task_completed (firmado por PM)
curl -s -X PATCH "$BASE/api/tasks/APR-S[N]/status" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "statusId": "aa5ceb90-5209-42a2-b874-a8cbee597a97",
    "changedBy": "<PM_UUID>",
    "reason": "Sprint S[N] aprobado. Todas las firmas registradas, milestone GO."
  }'
```

---

## §9 Proceso de cierre (firmas secuenciales)

```
Tareas completadas (TL → task_completed)
      ↓
TL firma stage development (§3) ← API
      ↓
AR firma stage integration (§4) ← API
      ↓
[Si FE] DL firma stage design (§5) ← API
      ↓
TL verifica milestone GO/NO-GO (§6)
      ↓
PM revisa métricas (§7) + checklist gate (§8)
      ↓
PM aprueba APR-S[N] ← API
      ↓
Sprint S[N] CERRADO
      ↓
PJM inicia trío de documentos de S[N+1]
```

---

## §10 Firmas de cierre (tabla)

| Rol | Stage | Fecha | Sign ID | Comment |
|---|---|---|---|---|
| TL | development | YYYY-MM-DD | [auto] | [comment] |
| AR | integration | YYYY-MM-DD | [auto] | [comment] |
| DL | design | YYYY-MM-DD | [auto] | [comment] / N/A |
| QA | testing | YYYY-MM-DD | [auto] | [comment] / N/A |
| PM | approval (APR-S[N]) | YYYY-MM-DD | [auto] | [comment] |

---

## §11 Referencias

- `HANDOFF_TL_S[N].md` — handoff que originó el sprint
- `SETUP_S[N].md` — script de setup VTT
- `3B.9.9_capacity_plan.md` — milestone y criterios GO/NO-GO
- `CODE_REVIEW_GUIDE_V1.1.md` — criterios firma TL
- `INTEGRATION_AUDIT_CHECKLIST_V1.1.md` — criterios firma AR
- `METODOLOGIA_CIERRE_SPRINT_FASE.md` — metodología base
- `SOP_GENERACION_SPRINT_DOCS.md` §6 SubFase 3C — origen del template
- VTT API stage signing: `POST /api/sprints/:id/stages/:stage/sign`

---

**Documento generado por:** PJM
**Sprint:** S[N]
**Versión documento:** 1.0
**Fecha generación:** YYYY-MM-DD
```

---

## Changelog del template

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-05-13 | Versión inicial — extraído del SOP_GENERACION_SPRINT_DOCS §6 SubFase 3C |
