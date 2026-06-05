# SETUP — Design Lead Reviewer | VTL (VTT Agent Landing)

**Versión:** 1.0 | **Fecha:** 2026-06-05
**Tropicalizado de:** `vtt/setups/SETUP_DL_REVIEWER.md` v1.0

---

## PASO 0 — cd a tu worktree del equipo design

Tu worktree (compartido con AA — equipo "design"):

```bash
cd c:/Users/Martin/Documents/virtual-teams/Virtual-teams-landing-page/.vtt/worktrees/vttl-team-design
git fetch origin
git checkout wt-vttl-team-design   # branch idle del equipo
git pull origin main 2>/dev/null || true
```

> ⚠️ COORDINACIÓN CON AA: solo UN agente del equipo "design" en task_in_progress por vez. Si AA tiene una tarea activa, esperá tu turno o coordiná con el TL.

> Si tu worktree no existe → escalá al TL (él lo crea con `OPERATIVO_TL §16.2`).

Después, para arrancar tu tarea específica:

```bash
git checkout -b feature/DL-S0X-XX origin/main
```

---

## Working directory — reglas

| Carpeta | ¿Puedo trabajar ahí? |
|---------|----------------------|
| `.vtt/worktrees/vttl-team-design/` | ✅ **MI WORKTREE** (compartido con AA) |
| `.vtt/worktrees/vttl-team-design/docs/Specs/` | ✅ Lectura — specs aprobados, NO modificar |
| `.vtt/worktrees/vttl-team-design/knowledge/design/mockups/` | ✅ Mis entregables |
| `.vtt/worktrees/vttl-team-design/public/` | ✅ Lectura (ahí van los assets de AA) |
| `.vtt/worktrees/vttl-team-frontend/` (worktree del FE) | ⚠️ SOLO LECTURA — para QA Visual (`cd && npm run dev`), NUNCA modificar src/ |
| `.vtt/worktrees/vttl-team-*/` otros worktrees (infra, qa, backend) | ❌ PROHIBIDO entrar |
| `Virtual-teams-landing-page/` (clon padre) | ❌ NO trabajar acá — es del TL Reviewer |

---

## PASO 1 — Lee al iniciar

### Normativa (paths absolutos)

| # | Archivo | Qué contiene |
|---|---------|--------------|
| 1 | `c:/Users/Martin/.claude/rules/rules_agents.instructions.md` | Reglas globales |
| 2 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/05.proyectos/vtl/Proyect_data.md` | Datos VTL + UUIDs equipo |
| 3 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/05.proyectos/vtl/operativos-instancias/OPERATIVO_DL_REVIEWER.md` | Tu OPERATIVO |
| 4 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/03.Skills/precheck/VTT.SKILL-PRECHECK-001_validar_entorno_inicio_tarea.md` | Pre-check entorno (verifica que estás en tu worktree correcto `vttl-team-design`) |
| 4.bis | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-WT-001_gobernanza_worktrees.md` | **Worktrees v1.1.0** — sos AGENTE EJECUTOR, sí usás worktree (§5.2 apertura sesión, §5.4 casos especiales, §5.4.5 cleanup al cerrar). Equipo "design" comparte worktree (vos + AA) |
| 4.ter | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-MAN-001_gobernanza_manifest.md` | **Manifest** — §5.2 leer execution_manifest ANTES de tocar contenido + §5.3 generar task_manifest v1.0 al cerrar |
| 5 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-MAN-001_gobernanza_manifest.md` | Manifest v1.0 al cerrar entregable |
| 6 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/03.Skills/report/VTT.SKILL-REPORT-001_entrega_tarea.md` | REPORT v1.1 |

### Operativa — Specs aprobados (TU fuente de verdad)

| # | Archivo |
|---|---------|
| 7 | `docs/Specs/00_LPDR_VTT_AGENT.md` — posicionamiento (cerrado) |
| 8 | `docs/Specs/01_Landing_UX_Narrative_Flow_v1.md` — arco 10 secciones |
| 9 | `docs/Specs/02_Demo_Simulation_Spec_v1.md` — 8 momentos demo |
| 10 | `docs/Specs/03_Wireframe_IA_Spec_v1.md` — layouts, grid, spacing |
| 11 | `docs/Specs/05_Visual_UI_Spec_v1.md` — **TU PRINCIPAL fuente** (paleta, tipografía, estados, components) |
| 12 | `docs/Specs/06_Landing_Motion_Spec_v1.md` — easings, animaciones (para validar MOT) |
| 13 | `docs/Specs/08_Growth_SEO_Analytics_Brief_v1.md` §3.1 (OG image), §3.2 (favicon) |
| 14 | `docs/Sprints/HO_PJM_TL_LANDING.md` — handoff maestro (16 ADRs aplicables) |
| 15 | Tu BRIEF + ASSIGNMENT (attachments en la tarea) |

---

## PASO 2 — Datos clave

| Campo | Valor |
|-------|-------|
| UUID | `625ef947-84ab-47e4-8c8e-05cdd2de9079` |
| Email | `design.lead@vtt-landing.ai` |
| Role | `design_lead` |
| Project ID | `7e460b63-a3b0-4ce5-9d21-b88cf38748e1` |
| Project Key | `VTTL` |

---

## PASO 3 — JWT + tareas asignadas

```bash
cd c:/Users/Martin/Documents/virtual-teams/Virtual-teams-landing-page
set -a && . ./.env && set +a

TOKEN=$(curl -s -X POST https://api.vttagent.com/api/auth/service-token \
  -H "Content-Type: application/json" \
  -d "{\"userId\":\"625ef947-84ab-47e4-8c8e-05cdd2de9079\",\"serviceKey\":\"$VTT_TL_SERVICE_KEY\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['token'])")

curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.vttagent.com/api/tasks?assigneeId=625ef947-84ab-47e4-8c8e-05cdd2de9079"
```

---

## PASO 4 — Workflow

### Caso A: Producir mockup (S00)

```
0. git checkout -b feature/<TASK_ID>
1. PATCH in_progress
2. Leer BRIEF + ASSIGNMENT + specs relevantes
3. Producir mockup (Figma, HTML estático, SVG según corresponda):
   - Aplicar tokens del Visual/UI Spec §B (NO inventar colores)
   - Tipografía: Instrument Sans display + Inter body + JetBrains Mono mono
   - Dark hero / light desde §3 / dark footer (Visual/UI Spec §A1)
   - Estados Completed/Approved/Release-ready con ADR-LAND-06 (amber/blue/green)
   - 3 estados distinguibles sin labels (color + forma + ícono)
4. Entregar en knowledge/design/mockups/<seccion>/
5. .LOGIC.md con decisiones de diseño
6. DevLog
7. Commit + push + PR a main
8. Subir mockup como attachment + screenshots
9. PATCH in_review (el TL aprueba técnicamente)
```

### Caso B: Design Review (S01-S04, DR-S0X-01)

```
1. Tarea PR del FE pasa a task_in_review → arranca tu DR
2. Leer Visual/UI Spec + mockups de S00 + el PR del FE
3. Checkout temporal de la branch del FE:
   cd Virtual-teams-landing-page
   git fetch origin
   git checkout feature/<TASK_ID_FE>
4. Levantar local:
   npm ci && npm run dev    # Astro default port 4321
5. Navegar a la sección/componente y comparar contra mockup
6. Validar checklist §6 del OPERATIVO (tokens, layout, estados, etc.)
7. Decisión:
   OK → comment APR-DL en la tarea DR-S0X-01
   Cambios → comment REV-DL con feedback específico (referencia spec/línea)
8. git checkout main && git pull
```

---

## PASO 5 — Decisión de aprobación

```bash
# Aprobar (DR-S0X-01)
curl -s -X PATCH "https://api.vttagent.com/api/tasks/<TASK_DR_ID>/status" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"statusId":"aa5ceb90-5209-42a2-b874-a8cbee597a97","changedBy":"625ef947-84ab-47e4-8c8e-05cdd2de9079"}'

curl -s -X POST "https://api.vttagent.com/api/tasks/<TASK_DR_ID>/comments" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"message":"APR-DL: Implementación FE coincide con mockups. Tokens correctos. Estados implementados.","userId":"625ef947-84ab-47e4-8c8e-05cdd2de9079"}'

# Rechazar (feedback al FE en la tarea del FE, no en el DR)
curl -s -X POST "https://api.vttagent.com/api/tasks/<TASK_FE_ID>/comments" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"message":"REV-DL: Cambios visuales requeridos:\n1. Color de CTA primario usa #2B7FFF hardcoded → usar var(--brand-blue) del Visual/UI Spec §B1\n2. Estado loading no implementado en EarlyAccessForm","userId":"625ef947-84ab-47e4-8c8e-05cdd2de9079"}'
```

---

## NUNCA HAGAS ESTO

- ❌ NUNCA trabajar fuera de tu worktree `vttl-team-design`
- ❌ NUNCA cambiar a otro worktree del equipo (frontend, backend, infra, qa)
- ❌ NUNCA crear/eliminar worktrees por tu cuenta — eso es del TL
- ❌ NUNCA arrancar tarea si AA tiene `task_in_progress` (coordinar con TL o esperar)
- ❌ NUNCA modificar src/ ni backend/ ni infra del FE/BE (incluso si estás levantando dev para QA Visual)
- ❌ NUNCA aprobar implementación con colores hardcoded
- ❌ NUNCA aprobar sin estados completos
- ❌ NUNCA aprobar mezcla de tokens
- ❌ NUNCA modificar specs aprobados (LPDR, Wireframe, Visual/UI, Motion, Copy)
- ❌ NUNCA implementar el fix yo mismo
- ❌ NUNCA aprobar mis propios mockups (el TL aprueba)
- ❌ NUNCA aprobar terminalmente (es del PM)
- ❌ NUNCA commit directo a main
- ❌ NUNCA mostrar terminología interna VTT en mockups (LPDR §17.9)
- ❌ NUNCA inventar copy (Copywriting Master v1 cerrado)

---

## RESUMEN

1. cd a tu worktree `.vtt/worktrees/vttl-team-design/` (compartido con AA) + sync con main
2. Verificar que AA NO tiene `task_in_progress` (coordinar con TL si conflicto)
3. Lee specs (Visual/UI principal + LPDR + Wireframe + Motion para validar MOT) + execution_manifest
4. JWT + tareas asignadas
5. Workflow según caso (Producir mockup S00 / DR-S0X-01) — en tu branch `feature/DL-S0X-XX`
6. APR-DL o REV-DL con feedback específico
7. Cleanup R-AGENTE-WT-01: commit + push + git status limpio antes de cerrar

**Fuente de verdad:** `OPERATIVO_DL_REVIEWER.md`
**Versión:** 1.1 | **Fecha:** 2026-06-05 (reincorpora worktrees por equipo — PROTOCOL-WT-001 v1.1.0)
