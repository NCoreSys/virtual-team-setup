# CONTEXTO DO — Sesión de trabajo

**Última actualización:** 2026-04-24
**DO:** `322e3745-9756-4a7c-af11-44b33edef44d`
**Email:** memory-service.devops@vtt.ai
**Proyecto:** Memory Service (`d0fc276d-e764-4a83-96e9-d65f086ed803`) — Project Key: MS

---

## 1. ESTADO ACTUAL DEL PROYECTO

| Aspecto | Estado |
|---------|--------|
| **Estructura** | 10 fases, 116 tareas, 381h |
| **Fase actual** | Fase 1 — Project Setup (INIT-* tasks en ejecución) |
| **Multi-repo** | ✅ Decidido — ADR-001 aprobado 2026-04-23 |
| **Repos GitHub** | ✅ 4 repos creados en org `NCoreSys` |
| **Branch protection** | ⏳ Pendiente — tu tarea MS-144 |
| **Código escrito** | 0 líneas — Sprint S01 aún no arranca |
| **Infra Hetzner** | Provisionada (77.42.88.106) — pendiente verificar MS-127 |

---

## 2. LO QUE YA ESTÁ HECHO

| Fecha | Hito | Owner |
|-------|------|-------|
| 2026-04-22 | 116 tareas creadas en VTT (MS-001..MS-116) | PJM |
| 2026-04-23 | ADR-001 aprobado — polirrepo 4 repos en NCoreSys | PM |
| 2026-04-23 | PROJECT_RULES.md v1.5 publicado | TL |
| 2026-04-24 | MS-117..MS-120 completadas (verificación VTT + PATCH metadata) | PJM |
| 2026-04-24 | Assignments MS-122, MS-127, MS-144 subidos a VTT | PJM |

---

## 3. TUS TAREAS ASIGNADAS (Fase 1)

| Task ID | Título | Status | Assignment |
|---------|--------|--------|------------|
| **MS-122** | INIT-B-01: Crear y verificar repo Git | task_pending | ✅ En VTT |
| **MS-127** | INIT-C-01: Verificar infraestructura Hetzner | task_pending | ✅ En VTT |
| **MS-144** | INIT-E-01: Configurar gobernanza GitHub 4 repos | task_pending | ✅ En VTT |

**Orden recomendado:** MS-127 → MS-122 → MS-144

---

## 4. LOS 4 REPOS GITHUB (ADR-001)

| Repo | Propósito | URL |
|------|-----------|-----|
| `memory-service-project` | Docs, ADRs, devlogs, knowledge | https://github.com/NCoreSys/memory-service-project |
| `memory-service-api` | Contrato OpenAPI + types | https://github.com/NCoreSys/memory-service-api |
| `memory-service-backend` | Node.js + Express + Prisma | https://github.com/NCoreSys/memory-service-backend |
| `memory-service-frontend` | React + Vite + Tailwind | https://github.com/NCoreSys/memory-service-frontend |

**Tu repo de escritura principal:** `memory-service-project` (devlogs, infra docs)
**También escribes en:** `memory-service-backend` (infra/, .github/)

**Estado actual:** los 4 repos existen pero sin rama `main` inicializada ni branch protection.

---

## 5. INFRA HETZNER (lo que debes verificar en MS-127)

| Componente | Esperado | Estado |
|------------|----------|--------|
| PostgreSQL `memory_service_db` | En shared-postgres | Por verificar |
| Volumen `/root/memory-service-storage/` | Con permisos escritura | Por verificar |
| Redis prefix `mem` | En shared-redis | Por verificar |
| Puerto 3002 (API) | Abierto en firewall | Por verificar |
| Puerto 3003 (UI) | Abierto en firewall | Por verificar |
| Docker `shared-network` | Existe | Por verificar |
| `SERVICE_KEY` en `.env` | Configurada | Por verificar |

Servidor: `77.42.88.106` — VTT corre en puerto 3000 (ya operativo).

---

## 6. BRANCH PROTECTION REQUERIDA (MS-144 — ADR-001 §D-ADR-001-B)

Aplicar en `main` de los 4 repos:
- Require pull request before merging (1 approval mínimo)
- Dismiss stale approvals on new commits
- Do not allow bypassing ← CRÍTICO
- Prevent force pushes
- Allow deletions: NO

PATs requeridos (los crea el Coordinador Martin Rivas en github.com):

| PAT | Repos de escritura |
|-----|--------------------|
| PAT_MEM_BE | memory-service-backend |
| PAT_MEM_FE | memory-service-frontend |
| PAT_MEM_DO | memory-service-project, memory-service-api |
| PAT_MEM_TL | todos (4 repos) |
| PAT_MEM_PM | memory-service-project |

**IMPORTANTE:** Los valores de PATs son secretos — NUNCA commitear. Solo el inventario de metadata.

---

## 7. CREDENCIALES Y API

```
userId (DO):  322e3745-9756-4a7c-af11-44b33edef44d
serviceKey:   hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d
email:        memory-service.devops@vtt.ai

API VTT:      http://77.42.88.106:3000
Auth:         POST /api/auth/service-token
              body: {"userId": "<DO_UUID>", "serviceKey": "<SERVICE_KEY>"}

Status IDs:
  task_in_progress: 2a76888a-e595-4cfc-ac4c-a3ae5087ef56
  task_in_review:   1ec975a5-7581-4a1a-ab8f-51b1a7ef868d
  task_completed:   aa5ceb90-5209-42a2-b874-a8cbee597a97

GitHub CLI: gh (autenticado como NCoreSys)
```

---

## 8. MEMORY SERVICE API — ACCESO Y SERVICE_KEY

### ¿Qué es la SERVICE_KEY del Memory Service?
Es la clave que protege el acceso al Memory Service API (puerto 3002). Cualquier servicio
que quiera llamar al Memory Service debe incluirla en el header `X-Service-Key`.

### ¿Dónde está configurada?
- **En la VM:** `/root/memory-service/.env` → `SERVICE_KEY=<valor>`
- **En GitHub (los 4 repos):** GitHub Actions Secret `MEMORY_SERVICE_KEY`
  - NCoreSys/memory-service-api ✅
  - NCoreSys/memory-service-backend ✅
  - NCoreSys/memory-service-frontend ✅
  - NCoreSys/memory-service-project ✅

### Cómo leer la key (como agente DO en una tarea):
```bash
# Opción 1: leer del .env en la VM
ssh root@77.42.88.106 "grep SERVICE_KEY /root/memory-service/.env"
# Output: SERVICE_KEY=<valor> — usar en memoria, nunca commitear

# Opción 2: en un GitHub Actions workflow
env:
  MEMORY_SERVICE_KEY: ${{ secrets.MEMORY_SERVICE_KEY }}
```

### Cómo usarla para llamar al Memory Service API:
```bash
# Test de conectividad
curl -H "X-Service-Key: <valor>" http://77.42.88.106:3002/api/health

# En código (Node.js)
headers: { 'X-Service-Key': process.env.MEMORY_SERVICE_KEY }
```

### Regla de seguridad:
- **NUNCA** commitear el valor de la key
- **NUNCA** incluirla en devlogs, LOGIC.md, ni comentarios de VTT
- Inventario de distribución: `knowledge/infra/SERVICE_KEY_DISTRIBUTION.md`

---

## 9. REGLAS CRÍTICAS PARA TI (DO)

1. **NUNCA muevas tareas de otros agentes** — solo mueves las tuyas (MS-122, MS-127, MS-144)
2. **NUNCA commits directos a main** — siempre rama `feature/[TASK_ID]` + PR
3. **Siempre mueve a in_progress con tus credenciales DO** antes de empezar
4. **3 attachments en VTT antes de in_review:** devlog + code_logic + comentario
5. **PAT values = secretos absolutos** — solo commitear metadata (PAT_INVENTORY.md)

Ver: `.claude/rules/PROJECT_RULES.md` — reglas completas del proyecto.

---

## 10. RUTINA DE APERTURA DE SESIÓN

1. Obtener JWT: `POST /api/auth/service-token` con tus credenciales DO
2. Ver tus tareas pendientes: `GET /api/tasks?assigneeId=322e3745-9756-4a7c-af11-44b33edef44d`
3. Leer assignment de la tarea que vas a trabajar (adjunto en VTT)
4. Mover a `task_in_progress`
5. Empezar

---

## 11. NOTAS DE SESIÓN

### 2026-04-24 — Onboarding DO

**Estado al arrancar:**
- ADR-001 aprobado, repos creados en NCoreSys pero sin main ni branch protection
- 3 tareas asignadas: MS-122, MS-127, MS-144 con assignments en VTT
- Infra Hetzner provisionada pero pendiente verificación formal

**Próxima sesión DO:**
- Ejecutar MS-127 primero (verificar infra — 1h)
- Luego MS-122 (corregir remote + verificar repos — 1h)
- Luego MS-144 (branch protection + PATs — 6h, coordinar con Coordinador para PAT creation)

---

**Regla:** actualizar §10 al inicio y cierre de cada sesión DO.
