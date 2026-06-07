# SETUP — Backend Engineer (BE) | VTL (VTT Agent Landing)

**Versión:** 1.0 | **Fecha:** 2026-06-05
**Tropicalizado de:** `vtt/setups/SETUP_BE.md` v1.1

---

## PASO 0 — cd a tu worktree del equipo backend (en virtual-teams-tracking)

⚠️ **IMPORTANTE:** Tu worktree vive en `virtual-teams-tracking/.vtt/worktrees/vttl-team-backend/` porque el endpoint vive en el backend VTT existente (ADR-LAND-01). NO trabajás en `Virtual-teams-landing-page/`.

```bash
cd c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking/.vtt/worktrees/vttl-team-backend
git fetch origin
git checkout wt-vttl-team-backend   # branch idle del equipo
git pull origin main 2>/dev/null || true

# Crear branch para tu tarea
git checkout -b feature/BE-S0X-XX origin/main
```

> VTL SÍ usa worktrees por equipo (PROTOCOL-WT-001 v1.1.0). El equipo "backend" tiene 1 solo agente (vos). Si tu worktree no existe → escalá al TL VTL (él lo crea con `OPERATIVO_TL §16.2`).

> ⚠️ **CUIDADO:** El repo `virtual-teams-tracking/` también tiene otros worktrees del proyecto VTT principal (`vtt-espacio-1..5`) — esos NO son tuyos. Solo trabajás en `vttl-team-backend`.

---

## Working directory — reglas

| Carpeta | ¿Puedo trabajar ahí? |
|---------|----------------------|
| `virtual-teams-tracking/.vtt/worktrees/vttl-team-backend/` | ✅ **MI WORKTREE** (equipo backend VTL — solo yo) |
| `…/vttl-team-backend/backend/prisma/schema.prisma` | ✅ Agregar model `EarlyAccessLead` (NO modificar models existentes) |
| `…/vttl-team-backend/backend/prisma/migrations/` | ✅ Crear nueva migration |
| `…/vttl-team-backend/backend/src/routes/early-access.routes.ts` | ✅ Crear router nuevo |
| `…/vttl-team-backend/backend/src/services/early-access.service.ts` | ✅ Crear service nuevo |
| `…/vttl-team-backend/backend/src/validators/early-access.validator.ts` | ✅ Crear validador Zod |
| `…/vttl-team-backend/backend/src/index.ts` (registrar route) | ✅ Solo agregar `app.use('/api/early-access', earlyAccessRouter)` |
| `…/vttl-team-backend/backend/.env` (referencia para nuevas vars) | ⚠️ Solo leer (TURNSTILE_SECRET, RESEND_API_KEY) |
| `…/vttl-team-backend/backend/src/routes/*.ts` (otros existentes) | ❌ NUNCA modificar (no es tu tarea) |
| `…/vttl-team-backend/frontend/` | ❌ Es del FE |
| `…/vttl-team-backend/docker-compose.yml` / `nginx.conf` | ❌ Es del DO |
| `virtual-teams-tracking/.vtt/worktrees/vtt-espacio-*/` | ❌ **PROHIBIDO** — son del proyecto VTT principal, NO del proyecto VTL |
| `virtual-teams-tracking/` (clon padre) | ❌ NO trabajar — es del TL VTT principal |
| `Virtual-teams-landing-page/.vtt/worktrees/vttl-team-*/` | ❌ PROHIBIDO — son de los otros equipos VTL |
| `Virtual-teams-landing-page/docs/Specs/` (clon padre landing) | ✅ Solo lectura — spec del endpoint |

---

## PASO 1 — Lee al iniciar

### Normativa (paths absolutos)

| # | Archivo | Qué contiene |
|---|---------|--------------|
| 1 | `c:/Users/Martin/.claude/rules/rules_agents.instructions.md` | Reglas globales |
| 2 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/05.proyectos/vtl/Proyect_data.md` | Datos VTL |
| 3 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/05.proyectos/vtl/operativos-instancias/OPERATIVO_BE.md` | Tu OPERATIVO |
| 4 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-MAN-001_gobernanza_manifest.md` | Manifest §5.2 leer + §5.3 generar v1.0 |
| 4.bis | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-WT-001_gobernanza_worktrees.md` | **Worktrees v1.1.0** — sos AGENTE EJECUTOR, sí usás worktree. Equipo "backend" — solo vos, worktree en `virtual-teams-tracking/` |
| 5 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/03.Skills/precheck/VTT.SKILL-PRECHECK-001_validar_entorno_inicio_tarea.md` | Pre-check entorno |
| 6 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/03.Skills/manifest/VTT.SKILL-EXM-001_execution_manifest.md` | Leer execution_manifest |
| 7 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/03.Skills/manifest/VTT.SKILL-MAN-001_task_manifest.md` | Task manifest v1.0 |
| 8 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/03.Skills/report/VTT.SKILL-REPORT-001_entrega_tarea.md` | REPORT v1.1 |

### Operativa — Specs aprobadas (en repo landing)

| # | Archivo |
|---|---------|
| 9 | `c:/Users/Martin/Documents/virtual-teams/Virtual-teams-landing-page/docs/Specs/07_Landing_Technical_Spec_v1.md` §1.4 (formulario backend), §7 (form técnico) |
| 10 | `c:/Users/Martin/Documents/virtual-teams/Virtual-teams-landing-page/docs/Specs/08_Growth_SEO_Analytics_Brief_v1.md` §2.2 (events del form) |
| 11 | `c:/Users/Martin/Documents/virtual-teams/Virtual-teams-landing-page/docs/Sprints/HO_PJM_TL_LANDING.md` §6.6 (ADR-LAND-09) + §10 (SEC-L) |
| 12 | `c:/Users/Martin/Documents/virtual-teams/Virtual-teams-landing-page/docs/Sprints/HANDOFF_TL_S00.md` |
| 13 | Tu BRIEF + ASSIGNMENT (attachments en la tarea VTT) |

### Repo backend VTT (donde implementás)

| # | Archivo |
|---|---------|
| 14 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking/backend/prisma/schema.prisma` (read-only — verificar models existentes) |
| 15 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking/backend/src/routes/` (patrones de endpoints existentes para reusar) |
| 16 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking/backend/src/services/` (patrones de services existentes) |

> ⚠️ **NO leas el PROTOCOL-ASG-001 completo (47 pasos / 6 fases).** Ese es del TL.

---

## PASO 2 — Datos clave

| Campo | Valor |
|-------|-------|
| UUID #1 | `a2e44984-929c-4453-a8c2-01815d0a74be` |
| UUID #2 (backup) | `57da2365-bc11-422f-8915-6139a2957019` |
| Email | `backend.dev@vtt-landing.ai` |
| Role | `backend_dev` |
| Project ID VTL | `7e460b63-a3b0-4ce5-9d21-b88cf38748e1` |
| API URL VTT | `https://api.vttagent.com` |
| SERVICE_KEY | `VTT_TL_SERVICE_KEY` del `.env` (NUNCA hardcodear) |
| Swagger | `https://api.vttagent.com/api-docs` |

---

## PASO 3 — JWT + tareas asignadas

```bash
cd c:/Users/Martin/Documents/virtual-teams/Virtual-teams-landing-page
set -a && . ./.env && set +a  # carga VTT_TL_SERVICE_KEY

TOKEN=$(curl -s -X POST https://api.vttagent.com/api/auth/service-token \
  -H "Content-Type: application/json" \
  -d "{\"userId\":\"a2e44984-929c-4453-a8c2-01815d0a74be\",\"serviceKey\":\"$VTT_TL_SERVICE_KEY\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['token'])")

curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.vttagent.com/api/tasks?assigneeId=a2e44984-929c-4453-a8c2-01815d0a74be"
```

---

## PASO 4 — Diagnóstico repo backend VTT

```bash
cd c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking
git branch --show-current     # debe estar en main o feature/BE-S00-XX
git status                    # debe estar limpio antes de empezar
git stash list                # vacío
```

---

## PASO 5 — Workflow por tarea

### BE-S00-01: Modelo Prisma + migración (2h)

```bash
# 0. Branch (desde tu worktree del equipo backend VTL)
cd c:/Users/Martin/Documents/virtual-teams/virtual-teams-tracking/.vtt/worktrees/vttl-team-backend
git fetch origin
git checkout wt-vttl-team-backend
git pull origin main 2>/dev/null || true
git checkout -b feature/BE-S00-01 origin/main

# 1. PATCH in_progress
TOKEN=$(cat .vtl_jwt)  # JWT del BE
curl -s -X PATCH "https://api.vttagent.com/api/tasks/<TASK_ID>/status" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"statusId":"2a76888a-e595-4cfc-ac4c-a3ae5087ef56","changedBy":"a2e44984-929c-4453-a8c2-01815d0a74be"}'

# 2. Agregar model en schema.prisma (NO modificar models existentes)
# Editar backend/prisma/schema.prisma — al final del archivo:
cat >> backend/prisma/schema.prisma << 'PRISMA'

model EarlyAccessLead {
  id          String   @id @default(uuid())
  email       String   @unique  // único pero NO devolver 409 en duplicado (ADR-LAND-09 — upsert silencioso)
  teamSize    String   // enum: "1-5" | "6-15" | "16-30" | "31-100" | "100+"
  source      String?  // opcional — "landing", "demo", etc.
  tools       String?  // opcional paso 2 — comma-separated
  motivation  String?  // opcional paso 2 — free text
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  @@index([createdAt])
  @@index([teamSize])
}
PRISMA

# 3. Crear migration
cd backend
npx prisma migrate dev --name add_early_access_lead --create-only

# 4. Verificar el SQL generado
cat prisma/migrations/<timestamp>_add_early_access_lead/migration.sql

# 5. .LOGIC.md para schema.prisma
# (en knowledge/code-logic/prisma/schema.LOGIC.md — solo el segmento del nuevo model)

# 6. DevLog
# 7. Commit + push + PR a main
git add backend/prisma/schema.prisma backend/prisma/migrations/<timestamp>_add_early_access_lead
git commit -m "[BE-S00-01] Add EarlyAccessLead model + migration

- Model con email unique + upsert silencioso (ADR-LAND-09)
- Campos teamSize obligatorio, tools/motivation opcionales (paso 2)
- Indexes en createdAt y teamSize

Co-Authored-By: Claude (BE VTL) <backend.dev@vtt-landing.ai>
Refs: #BE-S00-01"
git push origin feature/BE-S00-01

# 8. Crear PR
gh pr create --base main --title "[BE-S00-01] EarlyAccessLead model + migration" \
  --body "Ver devlog para detalles. Migration NO se aplica en prod hasta INF-S05-02."

# 9. Subir attachments (devlog + code_logic) a VTT
curl -s -X POST "https://api.vttagent.com/api/tasks/<TASK_ID>/attachments" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@knowledge/development-log/<archivo>.md;type=text/markdown" \
  -F "fileType=devlog" \
  -F "uploadedById=a2e44984-929c-4453-a8c2-01815d0a74be"

# 10. Generar manifest v1.0
python3 "$VTT_SETUP/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py" \
  --task <TASK_ID> --version 1.0

# 11. PATCH in_review
curl -s -X PATCH "https://api.vttagent.com/api/tasks/<TASK_ID>/status" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"statusId":"1ec975a5-7581-4a1a-ab8f-51b1a7ef868d","changedBy":"a2e44984-929c-4453-a8c2-01815d0a74be"}'
```

### BE-S00-02: Endpoint POST /api/early-access (6h)

Estructura modular Router → Service → Validator:

```typescript
// backend/src/validators/early-access.validator.ts
import { z } from 'zod';

export const earlyAccessSchema = z.object({
  email: z.string().email().max(254),
  teamSize: z.enum(["1-5", "6-15", "16-30", "31-100", "100+"]),
  turnstileToken: z.string().min(10).max(4096),
  source: z.string().optional(),
  // paso 2 opcional
  tools: z.string().optional(),
  motivation: z.string().max(500).optional(),
});

// backend/src/services/early-access.service.ts
import { PrismaClient } from '@prisma/client';
import crypto from 'crypto';
const prisma = new PrismaClient();

export async function upsertLead(data: { email: string; teamSize: string; source?: string; tools?: string; motivation?: string }) {
  // Upsert silencioso (ADR-LAND-09 — sin info leak)
  await prisma.earlyAccessLead.upsert({
    where: { email: data.email },
    create: { email: data.email, teamSize: data.teamSize, source: data.source, tools: data.tools, motivation: data.motivation },
    update: { teamSize: data.teamSize, tools: data.tools, motivation: data.motivation, updatedAt: new Date() }
  });
  // NO devolver si era nuevo o duplicado
}

// SEC-L-06: NO loggear email completo — usar hash
export function anonymizeEmail(email: string): string {
  const [user, domain] = email.split('@');
  const userHash = crypto.createHash('sha256').update(user).digest('hex').slice(0, 8);
  return `${userHash}@${domain}`;
}

// backend/src/routes/early-access.routes.ts
import { Router } from 'express';
import rateLimit from 'express-rate-limit';
import { earlyAccessSchema } from '../validators/early-access.validator';
import { upsertLead, anonymizeEmail } from '../services/early-access.service';
import { validateTurnstile } from '../services/turnstile.service';
import { sendLeadNotification } from '../services/resend.service';

const router = Router();

// SEC-L-01: Rate limiting 5 req/min/IP
const limiter = rateLimit({
  windowMs: 60_000,
  max: 5,
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: { code: 'RATE_LIMIT', message: 'Too many requests' } }
});

/**
 * @swagger
 * /api/early-access:
 *   post:
 *     summary: Register early access lead
 *     description: Upsert silent (ADR-LAND-09) — devuelve 200 para nuevo Y duplicado (no info leak)
 *     tags: [Landing]
 *     security: []  # public endpoint (Turnstile valida)
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required: [email, teamSize, turnstileToken]
 *             properties:
 *               email: { type: string, format: email }
 *               teamSize: { type: string, enum: ["1-5", "6-15", "16-30", "31-100", "100+"] }
 *               turnstileToken: { type: string }
 *               source: { type: string }
 *               tools: { type: string }
 *               motivation: { type: string, maxLength: 500 }
 *     responses:
 *       200: { description: Lead registered (or already exists — no info leak) }
 *       400: { description: Validation error }
 *       403: { description: Turnstile invalid }
 *       429: { description: Rate limit exceeded }
 *       500: { description: Internal error }
 */
router.post('/', limiter, async (req, res) => {
  try {
    // SEC-L-04: Zod validation
    const parsed = earlyAccessSchema.safeParse(req.body);
    if (!parsed.success) {
      return res.status(400).json({ error: { code: 'VALIDATION', message: 'Invalid input', details: parsed.error.flatten() } });
    }
    const { email, teamSize, turnstileToken, source, tools, motivation } = parsed.data;

    // SEC-L-02: Turnstile server-side
    const turnstileOK = await validateTurnstile(turnstileToken, req.ip);
    if (!turnstileOK) {
      return res.status(403).json({ error: { code: 'TURNSTILE_INVALID', message: 'Verification failed' } });
    }

    // SEC-L-03 + ADR-LAND-09: upsert silencioso
    await upsertLead({ email, teamSize, source, tools, motivation });

    // Notificar al equipo (async, no bloquea response)
    sendLeadNotification({ email: anonymizeEmail(email), teamSize, source }).catch(() => {});

    // SEC-L-06: log anonimizado
    console.log(`[early-access] Lead upsert: ${anonymizeEmail(email)} teamSize=${teamSize}`);

    return res.status(200).json({ success: true });
  } catch (err) {
    console.error('[early-access] Error:', err);
    return res.status(500).json({ error: { code: 'INTERNAL', message: 'Internal server error' } });
  }
});

export default router;

// backend/src/index.ts (agregar):
// import earlyAccessRouter from './routes/early-access.routes';
// app.use('/api/early-access', earlyAccessRouter);
```

```
... (workflow standar — branch, commit, PR, attachments, manifest, in_review)
```

### BE-S00-03: Config Turnstile + Resend + CORS (2h)

```typescript
// backend/src/services/turnstile.service.ts
import fetch from 'node-fetch';
export async function validateTurnstile(token: string, ip: string): Promise<boolean> {
  const r = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ secret: process.env.TURNSTILE_SECRET_KEY, response: token, remoteip: ip }),
  });
  const data: any = await r.json();
  return data.success === true;
}

// backend/src/services/resend.service.ts
import { Resend } from 'resend';
const resend = new Resend(process.env.RESEND_API_KEY);
export async function sendLeadNotification({ email, teamSize, source }: { email: string; teamSize: string; source?: string }) {
  await resend.emails.send({
    from: 'leads@vttagent.com',
    to: ['martin.rivas.auge@gmail.com'],  // o lista del equipo
    subject: `[VTT Agent] New early access lead — ${teamSize}`,
    text: `Email (anon): ${email}\nTeam size: ${teamSize}\nSource: ${source ?? 'unknown'}`
  });
}

// backend/src/index.ts — agregar CORS específico para vttagent.com (SEC-L-05)
import cors from 'cors';
app.use('/api/early-access', cors({
  origin: ['https://vttagent.com', 'https://www.vttagent.com'],
  methods: ['POST'],
  allowedHeaders: ['Content-Type'],
  credentials: false
}));
```

Variables nuevas en `.env`:
```
TURNSTILE_SECRET_KEY=  # de Cloudflare Turnstile dashboard
RESEND_API_KEY=        # de Resend dashboard
```

Esas vars NO se commitean. Coordinar con DO/PM para setearlas en `.env` de prod.

---

## NUNCA HAGAS ESTO

- ❌ NUNCA trabajar fuera de tu worktree `vttl-team-backend` (en virtual-teams-tracking)
- ❌ NUNCA entrar a worktrees del proyecto VTT principal (`vtt-espacio-1..5`)
- ❌ NUNCA cambiar a otro worktree del equipo VTL (design, frontend, infra, qa)
- ❌ NUNCA crear/eliminar worktrees por tu cuenta — eso es del TL VTL
- ❌ NUNCA dejar trabajo local sin commit+push al cerrar (R-AGENTE-WT-01)
- ❌ NUNCA endpoint que devuelva 409 en duplicado (ADR-LAND-09 — siempre 200 upsert silencioso)
- ❌ NUNCA loggear email completo (SEC-L-06)
- ❌ NUNCA endpoint sin Zod validation (SEC-L-04)
- ❌ NUNCA endpoint sin rate limiting (SEC-L-01)
- ❌ NUNCA endpoint sin Turnstile validation (SEC-L-02)
- ❌ NUNCA CORS sin origin restrictivo (SEC-L-05)
- ❌ NUNCA modificar models existentes en schema.prisma (solo agregar EarlyAccessLead)
- ❌ NUNCA modificar otros endpoints del backend VTT
- ❌ NUNCA modificar docker-compose / nginx / .env (es del DO)
- ❌ NUNCA modificar frontend/ (es del FE)
- ❌ NUNCA inventar campos del schema — verificar contra schema.prisma
- ❌ NUNCA mockear datos — crear ISSUE
- ❌ NUNCA dejar console.log de debug
- ❌ NUNCA endpoint sin try-catch ni Swagger JSDoc inline
- ❌ NUNCA commit directo a main
- ❌ NUNCA PR a develop — siempre main
- ❌ NUNCA postear datos sensibles en VTT (RULE-SEC-001)

---

## R-AGENTE-WT-01 — Cleanup al cerrar

```bash
git status                  # commit + push pending
git stash list              # vacío
git log @{u}..HEAD          # vacío (todo pusheado)
git checkout main
git pull --ff-only origin main
```

---

## RESUMEN

1. cd a tu worktree `virtual-teams-tracking/.vtt/worktrees/vttl-team-backend/` + sync con main
2. Crear `feature/BE-S00-XX`
3. Lee specs (Technical §1.4/§7 + ADR-LAND-09 + SEC-L-01..06) + execution_manifest
4. JWT + tareas
5. Workflow por tarea (model+migration / endpoint / config integrations)
6. .LOGIC.md + DevLog + commit + PR
7. Attachments + manifest v1.0 + in_review + cleanup R-AGENTE-WT-01

**Fuente de verdad:** `OPERATIVO_BE.md`
**Versión:** 1.1 | **Fecha:** 2026-06-05 (reincorpora worktrees por equipo — PROTOCOL-WT-001 v1.1.0)
