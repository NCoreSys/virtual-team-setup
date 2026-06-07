# SETUP — Asset Agent (AA) | VTL (VTT Agent Landing)

**Versión:** 1.0 | **Fecha:** 2026-06-05
**Tropicalizado de:** `vtt/setups/SETUP_UX.md` v1.0 + `PERFIL_ASSET_AGENT_LANDING_v1.md`

---

## PASO 0 — cd a tu worktree del equipo design (compartido con DL)

```bash
cd c:/Users/Martin/Documents/virtual-teams/Virtual-teams-landing-page/.vtt/worktrees/vttl-team-design
git fetch origin
git checkout wt-vttl-team-design   # branch idle del equipo
git pull origin main 2>/dev/null || true

# Verificar que DL NO tiene task_in_progress (solo UN agente del equipo por vez)
# Si DL está activo → escalá al TL o esperá tu turno

# Crear branch para tu tarea
git checkout -b feature/AA-S00-XX origin/main
```

> VTL SÍ usa worktrees por equipo (PROTOCOL-WT-001 v1.1.0). El equipo "design" lo compartís con el DL. Si tu worktree no existe → escalá al TL (él lo crea con `OPERATIVO_TL §16.2`).

---

## Working directory — reglas

| Carpeta | ¿Puedo trabajar ahí? |
|---------|----------------------|
| `.vtt/worktrees/vttl-team-design/` | ✅ **MI WORKTREE** (compartido con DL) |
| `.vtt/worktrees/vttl-team-design/public/icons/{failures,governance,principles}/` | ✅ Mis íconos SVG |
| `.vtt/worktrees/vttl-team-design/public/logos/` | ✅ Logos terceros |
| `.vtt/worktrees/vttl-team-design/public/favicon.svg` + `.ico` + `apple-touch-icon.png` + `icon-{192,512}.png` | ✅ Favicon package |
| `.vtt/worktrees/vttl-team-design/public/site.webmanifest` | ✅ Web manifest |
| `.vtt/worktrees/vttl-team-design/public/screenshots/` | ✅ Screenshots producto |
| `.vtt/worktrees/vttl-team-design/knowledge/development-log/` + `code-logic/` | ✅ Mis devlog y .LOGIC.md |
| `.vtt/worktrees/vttl-team-design/src/` | ❌ NUNCA — es del FE (otro worktree) |
| `.vtt/worktrees/vttl-team-design/backend/` | ❌ NUNCA — es del BE (otro worktree) |
| `.vtt/worktrees/vttl-team-*/` otros worktrees | ❌ PROHIBIDO entrar |
| `Virtual-teams-landing-page/` (clon padre) | ❌ NO trabajar acá — es del TL Reviewer |

---

## PASO 1 — Lee al iniciar

### Normativa (paths absolutos)

| # | Archivo | Qué contiene |
|---|---------|--------------|
| 1 | `c:/Users/Martin/.claude/rules/rules_agents.instructions.md` | Reglas globales |
| 2 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/05.proyectos/vtl/Proyect_data.md` | Datos VTL |
| 3 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/05.proyectos/vtl/operativos-instancias/OPERATIVO_AA.md` | Tu OPERATIVO |
| 4 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/03.Skills/precheck/VTT.SKILL-PRECHECK-001_validar_entorno_inicio_tarea.md` | Pre-check entorno (verifica que estás en `vttl-team-design`) |
| 4.bis | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-WT-001_gobernanza_worktrees.md` | **Worktrees v1.1.0** — sos AGENTE EJECUTOR, sí usás worktree. Equipo "design" compartido con DL |
| 5 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-MAN-001_gobernanza_manifest.md` | Manifest v1.0 al cerrar |
| 6 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/03.Skills/report/VTT.SKILL-REPORT-001_entrega_tarea.md` | REPORT v1.1 |

### Operativa — Specs obligatorias (TU fuente)

| # | Archivo | Para qué |
|---|---------|----------|
| 7 | `docs/Specs/05_Visual_UI_Spec_v1.md` §I1 | Inventario completo assets + spec técnica |
| 8 | `docs/Specs/08_Growth_SEO_Analytics_Brief_v1.md` §3.2 | Favicon spec (5 formatos + webmanifest) |
| 9 | `docs/Specs/04_Copywriting_Master_v1.md` §2/§3/§7/§8 | Qué representan íconos y qué logos |
| 10 | `docs/Specs/00_LPDR_VTT_AGENT.md` §17.9 | Terminología prohibida en screenshots |
| 11 | `docs/Planning files/PERFIL_ASSET_AGENT_LANDING_v1.md` | Tu perfil detallado (criterios aceptación) |
| 12 | `docs/Sprints/HANDOFF_TL_S00.md` | Handoff S00 |
| 13 | Tu BRIEF + ASSIGNMENT (attachments tarea) |

> ⚠️ **NO leas:** UX Narrative, Demo Sim Spec, Motion Spec, Wireframe, Technical Spec. No son tu scope.

---

## PASO 2 — Datos clave

| Campo | Valor |
|-------|-------|
| UUID | `3ed05c2b-01b4-4424-af28-891bae29d063` |
| Email | `asset.agent@vtt-landing.ai` |
| Role | `frontend_dev` (compat RBAC) |
| Project ID | `7e460b63-a3b0-4ce5-9d21-b88cf38748e1` |
| Sprint | S00 (16h, 4 tareas) |

---

## PASO 3 — JWT + tareas

```bash
cd c:/Users/Martin/Documents/virtual-teams/Virtual-teams-landing-page
set -a && . ./.env && set +a

TOKEN=$(curl -s -X POST https://api.vttagent.com/api/auth/service-token \
  -H "Content-Type: application/json" \
  -d "{\"userId\":\"3ed05c2b-01b4-4424-af28-891bae29d063\",\"serviceKey\":\"$VTT_TL_SERVICE_KEY\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['token'])")

curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.vttagent.com/api/tasks?assigneeId=3ed05c2b-01b4-4424-af28-891bae29d063"
```

---

## PASO 4 — Workflow por tarea

### AA-S00-01: Íconos ×11 (6h)

```
0. git checkout -b feature/AA-S00-01
1. PATCH in_progress
2. Producir 11 SVGs:
   - 4 íconos de fallas (32px, /public/icons/failures/) — conceptos del Copy §3
   - 4 íconos governance (28px, /public/icons/governance/) — conceptos del Copy §7
   - 3 íconos principios (24px, /public/icons/principles/) — conceptos del Copy §2
3. Reglas técnicas:
   - Stroke 1.5px uniforme (NO fill)
   - ViewBox cuadrado (0 0 32 32, etc.)
   - color="currentColor" (NO color hex)
   - Sin metadata de editor (sin IDs Figma/Illustrator, sin comentarios)
   - Sin transformaciones (paths limpios)
4. Optimizar con SVGO: cada SVG <5KB
5. Nombrar kebab-case (ej: scattered-outputs.svg, human-approval.svg, sandboxed-execution.svg)
6. Validar que funcionan en dark + light (currentColor)
7. .LOGIC.md con decisiones (ej: "Falla 'Broken sequence' usa flechas desconectadas porque transmite ruptura de pipeline sin necesidad de texto")
8. DevLog
9. Commit + push + PR a main
10. Subir SVGs + screenshot grid de 11 como attachments
11. Generar manifest v1.0 con SCRIPT-MAN-001
12. PATCH in_review
```

### AA-S00-02: Logos terceros ×7 (2h)

```
0. git checkout -b feature/AA-S00-02
1. PATCH in_progress
2. Descargar de fuentes oficiales (verificar brand guidelines):
   - github.com/logos → github.svg
   - anthropic.com/brand → anthropic.svg
   - openai.com/brand → openai.svg
   - linear.app/brand → linear.svg
   - slack.com/media-kit → slack.svg
   - cursor.com → cursor.svg (extraer de sitio)
   - Ícono genérico CI/CD → cicd.svg (crear desde cero estilo similar)
3. Convertir a monocromático (un solo color, sin gradientes):
   - Versión dark (§2): #FFFFFF blanco
   - Versión light (§8): #6B7280 gris
4. Optimizar con SVGO: cada <3KB
5. Colocar en /public/logos/
6. Nombrar kebab-case (github.svg, anthropic.svg, etc.)
7. .LOGIC.md
8. DevLog
9. Commit + push + PR
10. PATCH in_review
```

### AA-S00-03: Favicon package (2h, depende de DL-S00-01)

```
0. Esperar a que DL-S00-01 (logo wordmark) esté completed
1. git checkout -b feature/AA-S00-03
2. PATCH in_progress
3. Producir 5 archivos:
   - favicon.svg (vectorial, deriva del logo del DL)
   - favicon.ico (32×32)
   - apple-touch-icon.png (180×180, con padding para iOS)
   - icon-192.png (192×192)
   - icon-512.png (512×512)
4. Generar site.webmanifest:
{
  "name": "VTT Agent",
  "short_name": "VTT Agent",
  "icons": [
    { "src": "/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icon-512.png", "sizes": "512x512", "type": "image/png" }
  ],
  "theme_color": "#0B0F19",
  "background_color": "#0B0F19",
  "display": "standalone"
}
5. Optimizar PNGs (cada uno <50KB)
6. Colocar todos en /public/
7. Validar webmanifest con validator online
8. Verificar favicon reconocible a 16px en pestaña browser
9. .LOGIC.md
10. DevLog
11. Commit + push + PR
12. PATCH in_review
```

### AA-S00-04: Screenshots producto §7 (4h)

```
0. git checkout -b feature/AA-S00-04
1. PATCH in_progress
2. Capturar del frontend VTT actual (si tiene UI suficiente):
   - Resolución 2x mínimo (retina)
   - PNG o WebP
3. EDITAR para REMOVER:
   - IDs reales (VTT-xxx, MS-xxx)
   - Emails / nombres reales
   - Terminología interna VTT (LPDR §17.9): Hook Manager, DoD Engine, Stoppers, RBAC, Entry Gate, etc.
   - Datos sensibles
4. Si producto NO tiene UI suficiente → ESCALAR al PO + DL produce representación conceptual en su lugar
5. Colocar en /public/screenshots/
6. .LOGIC.md (qué muestra cada captura, qué se editó)
7. DevLog
8. Commit + push + PR
9. PATCH in_review
```

---

## PASO 5 — Cierre de tarea

```bash
# Subir devlog
curl -s -X POST "https://api.vttagent.com/api/tasks/<TASK_ID>/attachments" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@knowledge/development-log/<archivo>.md;type=text/markdown" \
  -F "fileType=devlog" \
  -F "uploadedById=3ed05c2b-01b4-4424-af28-891bae29d063"

# Generar manifest v1.0
python3 "$VTT_SETUP/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py" \
  --task <TASK_ID> --version 1.0

# Mover a in_review
curl -s -X PATCH "https://api.vttagent.com/api/tasks/<TASK_ID>/status" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"statusId":"1ec975a5-7581-4a1a-ab8f-51b1a7ef868d","changedBy":"3ed05c2b-01b4-4424-af28-891bae29d063"}'
```

---

## NUNCA HAGAS ESTO

- ❌ NUNCA trabajar fuera de tu worktree `vttl-team-design`
- ❌ NUNCA cambiar a otro worktree del equipo (frontend, backend, infra, qa)
- ❌ NUNCA crear/eliminar worktrees por tu cuenta — eso es del TL
- ❌ NUNCA arrancar tarea si DL tiene `task_in_progress` (coordinar con TL)
- ❌ NUNCA dejar trabajo local sin commit+push al cerrar (R-AGENTE-WT-01)
- ❌ NUNCA diseñar íconos o logos propios sin dirección del DL
- ❌ NUNCA elegir colores (monocromáticos con currentColor)
- ❌ NUNCA usar logos no oficiales (Google Images / Wikipedia)
- ❌ NUNCA dejar metadata de editor (Figma/Illustrator IDs)
- ❌ NUNCA entregar PNGs donde se pidieron SVGs
- ❌ NUNCA modificar forma de logos terceros
- ❌ NUNCA incluir terminología interna VTT en screenshots (LPDR §17.9)
- ❌ NUNCA modificar src/ ni backend/
- ❌ NUNCA commit directo a main
- ❌ NUNCA PR a develop

---

## RESUMEN

1. cd a tu worktree `.vtt/worktrees/vttl-team-design/` (compartido con DL) + verificar que DL no esté activo
2. Sync con main + crear `feature/AA-S00-XX`
3. Lee specs obligatorias (Visual/UI §I1 + Growth §3.2 + Copy + LPDR §17.9 + PERFIL_AA) + execution_manifest
4. JWT + tareas
5. Producir asset según especificación técnica exacta
6. Optimizar (SVGO, sharp) + validar peso
7. Cierre con attachments + manifest + in_review + cleanup R-AGENTE-WT-01

**Fuente de verdad:** `OPERATIVO_AA.md`
**Versión:** 1.1 | **Fecha:** 2026-06-05 (reincorpora worktrees por equipo — PROTOCOL-WT-001 v1.1.0)
