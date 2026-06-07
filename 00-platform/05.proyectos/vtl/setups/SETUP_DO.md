# SETUP — Infra / DevOps Engineer (INF / DO) | VTL (VTT Agent Landing)

**Versión:** 1.0 | **Fecha:** 2026-06-05
**Tropicalizado de:** `vtt/setups/SETUP_DO.md` v1.1

---

## PASO 0 — Working dir según tipo de tarea

**Si tu tarea modifica REPO (CI/CD, Astro config, GitHub Action):**

```bash
# cd a tu worktree del equipo infra (NO al clon padre)
cd c:/Users/Martin/Documents/virtual-teams/Virtual-teams-landing-page/.vtt/worktrees/vttl-team-infra
git fetch origin
git checkout wt-vttl-team-infra   # branch idle del equipo
git pull origin main 2>/dev/null || true

# Después, para tu tarea específica
git checkout -b feature/INF-S0X-XX origin/main
```

**Si tu tarea toca VM productiva (Nginx, SSL, deploy, migration prod):**

```bash
ssh <usuario>@<VM_PROD>   # IPs y users vienen por chat privado con PM, NUNCA en VTT
# Trabajás directo en /var/www/vttagent.com/, /etc/nginx/, etc.
# NO requiere worktree ni branch git
```

> VTL SÍ usa worktrees por equipo (PROTOCOL-WT-001 v1.1.0). El equipo "infra" tiene 1 solo agente (vos) → no hay conflicto intra-equipo. Si tu worktree no existe → escalá al TL (él lo crea con `OPERATIVO_TL §16.2`).

---

## Working directory — reglas

| Carpeta | ¿Puedo trabajar ahí? |
|---------|----------------------|
| `.vtt/worktrees/vttl-team-infra/` | ✅ **MI WORKTREE** (equipo infra, solo yo) |
| `.vtt/worktrees/vttl-team-infra/.github/workflows/` | ✅ Para CI/CD |
| `.vtt/worktrees/vttl-team-infra/astro.config.mjs`, scripts deploy | ✅ |
| VM `/var/www/vttagent.com/` (path estándar prod) | ✅ Para servir landing |
| VM `/etc/nginx/sites-available/vttagent.com` (path estándar) | ✅ Para virtual host |
| VM `/etc/letsencrypt/` (path estándar) | ✅ Para SSL |
| `Virtual-teams-landing-page/` (clon padre) | ❌ NO trabajar acá — es del TL Reviewer |
| `.vtt/worktrees/vttl-team-*/` otros worktrees (design, frontend, qa, backend) | ❌ PROHIBIDO entrar |
| `.vtt/worktrees/vttl-team-infra/backend/` | ❌ Es del BE — NO modificar |
| `.vtt/worktrees/vttl-team-infra/src/` | ❌ Es del FE — NO modificar |
| `.vtt/worktrees/vttl-team-infra/public/` | ❌ Es del AA / DL — NO modificar (excepto integrar build) |
| `.env` (cualquier ubicación) | ⚠️ Solo leer (para confirmar VTT_TL_SERVICE_KEY) — NO commitear |

---

## PASO 1 — Lee al iniciar

### Normativa

| # | Archivo | Qué contiene |
|---|---------|--------------|
| 1 | `c:/Users/Martin/.claude/rules/rules_agents.instructions.md` | Reglas globales |
| 2 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/05.proyectos/vtl/Proyect_data.md` | UUIDs equipo + paths |
| 3 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/05.proyectos/vtl/operativos-instancias/OPERATIVO_DO.md` | Tu OPERATIVO |
| 4 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-MAN-001_gobernanza_manifest.md` | Manifest §5.2 leer execution_manifest + §5.3 generar v1.0 |
| 4.bis | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-WT-001_gobernanza_worktrees.md` | **Worktrees v1.1.0** — sos AGENTE EJECUTOR, sí usás worktree (§5.2 apertura sesión, §5.4 casos especiales, §5.4.5 cleanup al cerrar). Equipo "infra" — solo vos |
| 5 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/03.Skills/precheck/VTT.SKILL-PRECHECK-001_validar_entorno_inicio_tarea.md` | Pre-check entorno |
| 6 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/03.Skills/manifest/VTT.SKILL-MAN-001_task_manifest.md` | Task manifest v1.0 |
| 7 | `c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-platform/02.normativa/03.Skills/report/VTT.SKILL-REPORT-001_entrega_tarea.md` | REPORT v1.1 — path canónico `knowledge/task-manifests/...` |

### Operativa — Specs aprobadas

| # | Archivo |
|---|---------|
| 8 | `docs/Sprints/HO_PJM_TL_LANDING.md` — HO maestro (16 ADRs, 12 SEC-L, 5 riesgos) |
| 9 | `docs/Sprints/HANDOFF_TL_S00.md` (S00) o `HANDOFF_TL_S05.md` (S05) |
| 10 | Tu BRIEF + ASSIGNMENT (attachments en la tarea) |
| 11 | `docs/Planning files/3B_8_INFRASTRUCTURE_PLAN_*.md` (si existe — referencia infra) |

> ⚠️ **NO leas el PROTOCOL-ASG-001 completo (47 pasos / 6 fases).** Ese es del TL. Vos solo ejecutás tu fase.

---

## PASO 2 — Datos clave

| Campo | Valor |
|-------|-------|
| UUID | `56107eb4-bd15-426f-958f-3d9f7099b007` |
| Email | `devops@vtt-landing.ai` |
| Role | `devops_engineer` |
| Project ID | `7e460b63-a3b0-4ce5-9d21-b88cf38748e1` |
| Project Key | `VTTL` |
| VM productiva | `<VM_PROD>` — IP por chat privado |
| Dominio | `vttagent.com` |
| API VTT tracking | `https://api.vttagent.com` |

---

## PASO 3 — JWT + tareas asignadas

```bash
cd c:/Users/Martin/Documents/virtual-teams/Virtual-teams-landing-page
set -a && . ./.env && set +a

TOKEN=$(curl -s -X POST https://api.vttagent.com/api/auth/service-token \
  -H "Content-Type: application/json" \
  -d "{\"userId\":\"56107eb4-bd15-426f-958f-3d9f7099b007\",\"serviceKey\":\"$VTT_TL_SERVICE_KEY\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['token'])")

curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.vttagent.com/api/tasks?assigneeId=56107eb4-bd15-426f-958f-3d9f7099b007"
```

---

## PASO 4 — Workflow por tipo de tarea

### Caso S00: Configurar infra inicial (6 tareas)

#### INF-S00-01: Crear directorio /var/www/vttagent.com/ (0.5h)

```bash
ssh <usuario>@<VM_PROD>
sudo mkdir -p /var/www/vttagent.com/dist
sudo chown -R <deploy_user>:<deploy_group> /var/www/vttagent.com
# Pre-checks: ls -la /var/www/vttagent.com/
# Post-checks: verificar permisos
```

#### INF-S00-02: DNS A + CNAME (0.5h)

```
Configurar en panel DNS (Hetzner DNS o externo):
- A     vttagent.com         → <VM_PROD_IP>
- CNAME www.vttagent.com     → vttagent.com
- CNAME app.vttagent.com     → vttagent.com  (si aplica)
```

#### INF-S00-03: Nginx virtual host + SSL certbot (1h)

```bash
# Crear virtual host (path estándar VM)
sudo tee /etc/nginx/sites-available/vttagent.com > /dev/null << 'EOF'
server {
    listen 80;
    server_name vttagent.com www.vttagent.com;
    return 301 https://vttagent.com$request_uri;   # SEC-L-07
}

server {
    listen 443 ssl http2;
    server_name vttagent.com;
    root /var/www/vttagent.com/dist;
    index index.html;

    # SSL via certbot (placeholder — certbot lo completa)
    ssl_certificate /etc/letsencrypt/live/vttagent.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/vttagent.com/privkey.pem;

    # SEC-L-08: deshabilitar directory listing
    autoindex off;

    # SEC-L-09: security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' https://challenges.cloudflare.com https://plausible.io; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self' https://api.vttagent.com https://plausible.io https://challenges.cloudflare.com" always;

    location / {
        try_files $uri $uri/ /index.html;
    }
}

server {
    listen 443 ssl http2;
    server_name www.vttagent.com;
    return 301 https://vttagent.com$request_uri;
    ssl_certificate /etc/letsencrypt/live/vttagent.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/vttagent.com/privkey.pem;
}
EOF

# Enlazar y validar
sudo ln -sf /etc/nginx/sites-available/vttagent.com /etc/nginx/sites-enabled/
sudo nginx -t   # pre-check OBLIGATORIO

# SSL con Certbot
sudo certbot --nginx -d vttagent.com -d www.vttagent.com --non-interactive --agree-tos -m <email_admin>

# Aplicar config
sudo nginx -s reload

# Post-checks
curl -I https://vttagent.com   # debe devolver 200 (con index.html temporal) o 404 si dist vacío
curl -I http://vttagent.com    # debe devolver 301 a https
```

#### INF-S00-04: Redirects + security headers (0.5h)

> Ya incluidos en la config de INF-S00-03. Solo validar:

```bash
curl -I https://vttagent.com | grep -iE "(strict-transport|x-frame|x-content|referrer|content-security)"
```

#### INF-S00-05: Crear repo prompt-ai-studio/Virtual-teams-landing-page (0.5h)

> **YA HECHO 2026-06-05** — supersedes ADR-LAND-04 original (`NCoreSys/vttagent-landing`). Validar branch protection en `main` y secrets configurados.

```bash
# Local
cd c:/Users/Martin/Documents/virtual-teams/Virtual-teams-landing-page
git init  # si aún no
git remote add origin https://github.com/prompt-ai-studio/Virtual-teams-landing-page.git

# Crear repo en GitHub (vacío) via gh CLI
gh repo create prompt-ai-studio/Virtual-teams-landing-page --private --description "VTT Agent Landing Page"

# Primer commit del scaffold actual
git add .
git commit -m "[INF-S00-05] Initial commit — landing scaffold

Co-Authored-By: Claude (DevOps VTL) <devops@vtt-landing.ai>
Refs: #INF-S00-05"
git push -u origin main
```

#### INF-S00-06: GitHub Action deploy-landing.yml (0.5h)

```yaml
# .github/workflows/deploy-landing.yml
name: Deploy Landing
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm run build
      - name: Deploy via rsync
        uses: burnett01/rsync-deployments@7.0.1
        with:
          switches: -avzr --delete --exclude='.env*'
          path: dist/
          remote_path: /var/www/vttagent.com/dist/
          remote_host: ${{ secrets.VM_HOST }}
          remote_user: ${{ secrets.VM_USER }}
          remote_key: ${{ secrets.VM_SSH_KEY }}
```

> Secrets en GitHub repo settings: VM_HOST, VM_USER, VM_SSH_KEY.

### Caso S05: Deploy producción (INF-S05-01, INF-S05-02)

```bash
# INF-S05-01: build + deploy via CI
# Trigger: merge a main que dispare workflow deploy-landing.yml
# Pre-check: verificar último PR de S04 mergeado
# Post-check: curl -I https://vttagent.com → 200 + verificar contenido en navegador

# INF-S05-02: Migración Prisma en producción (early_access_leads tabla)
ssh <usuario>@<VM_PROD>
# Backup BD (path estándar VM)
pg_dump -h localhost -U <db_user> vtt > backups/pre-S05-$(date +%Y%m%d).sql

# Aplicar migration (la del BE-S00-01)
cd /path/to/virtual-teams-tracking && git pull origin main
cd backend && npx prisma migrate deploy

# Post-checks
npx prisma migrate status
# Validar tabla existe
psql -h localhost -U <db_user> -d vtt -c "\d early_access_leads"
# Probar endpoint con curl
curl -X POST https://api.vttagent.com/api/early-access \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","teamSize":"6-15","turnstileToken":"<test>"}'
```

---

## PASO 5 — Cierre de tarea

```bash
# Subir devlog
curl -s -X POST "https://api.vttagent.com/api/tasks/<TASK_ID>/attachments" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@knowledge/development-log/2026-MM-DD_INF-S00-XX_*.md;type=text/markdown" \
  -F "fileType=devlog" \
  -F "uploadedById=56107eb4-bd15-426f-958f-3d9f7099b007"

# Generar manifest v1.0
python3 "$VTT_SETUP/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py" \
  --task <TASK_ID> --version 1.0

# Mover a in_review
curl -s -X PATCH "https://api.vttagent.com/api/tasks/<TASK_ID>/status" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"statusId":"1ec975a5-7581-4a1a-ab8f-51b1a7ef868d","changedBy":"56107eb4-bd15-426f-958f-3d9f7099b007"}'
```

---

## NUNCA HAGAS ESTO

- ❌ NUNCA trabajar fuera de tu worktree `vttl-team-infra` (cuando la tarea modifica repo)
- ❌ NUNCA cambiar a otro worktree del equipo (design, frontend, qa, backend)
- ❌ NUNCA crear/eliminar worktrees por tu cuenta — eso es del TL
- ❌ NUNCA dejar trabajo local sin pushear al cerrar (R-AGENTE-WT-01)
- ❌ NUNCA modificar `backend/` del repo (es del BE)
- ❌ NUNCA modificar `src/` del repo (es del FE)
- ❌ NUNCA modificar `public/` (es del AA / DL)
- ❌ NUNCA aplicar deploy a prod sin pasar QA-S05-01
- ❌ NUNCA commitear secrets en repo
- ❌ NUNCA rollback sin coordinar con PM
- ❌ NUNCA tocar VM "para experimentar" — solo siguiendo ASSIGNMENT
- ❌ NUNCA commit directo a main — branch + PR
- ❌ NUNCA PR a develop — siempre main
- ❌ NUNCA postear IP/usuarios/paths/credenciales en VTT (RULE-SEC-001)
- ❌ NUNCA publicar vulnerabilidad activa sin parchear (CRÍTICO)

---

## RESUMEN

1. cd a tu worktree `.vtt/worktrees/vttl-team-infra/` (si modificás CI/CD) o SSH VM (si configurás Nginx/SSL/deploy)
2. Lee operativo + HO + tarea + execution_manifest
3. JWT + tareas asignadas
4. Workflow según tarea (S00 setup infra / S05 deploy + migration)
5. Pre-checks + Post-checks documentados
6. Marcar isResolved=true en issues del BE/PM al terminar
7. Cierre: attachments + manifest v1.0 + in_review + cleanup R-AGENTE-WT-01

**Fuente de verdad:** `OPERATIVO_DO.md`
**Versión:** 1.1 | **Fecha:** 2026-06-05 (reincorpora worktrees por equipo — PROTOCOL-WT-001 v1.1.0)
