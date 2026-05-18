# Onboarding Agente Ejecutor - Proyecto Memory Service

**Fecha**: 2026-04-22
**Para**: Agentes ejecutores (BE, DO, DB, FE, QA, DL, UX, AR, SA, IR)
**De**: PM (Martin Rivas)

> Este documento es para los agentes que **EJECUTAN** tareas (escriben código, diseñan, testean, despliegan).
> Si eres TL, PM, PJM → usa tu propio onboarding, este no aplica.

---

## 1. Identifica tu rol y UUID

Busca tu rol en la tabla. Password común: `VttAgent2026`.

| Rol | UUID | Email |
|-----|------|-------|
| **SA** (Solution Analyst) | `0c128e3b-db3b-4e31-b107-0379b5791233` | sa@memory-service.vtt.ai |
| **AR** (Architect) | `e9403c25-c1f8-4b64-b2ef-f447d53115e2` | ar@memory-service.vtt.ai |
| **BE** (Backend) | `ebbe3cee-abed-4b3b-860d-0a81f632b08a` | be@memory-service.vtt.ai |
| **DB** (Database) | `6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7` | db@memory-service.vtt.ai |
| **FE** (Frontend) | `d23c9cd9-a156-433b-8900-94add5488eec` | fe@memory-service.vtt.ai |
| **UX** (UX Designer) | `a75a1dae-754a-4b6f-a3ff-db8d51f6a91b` | ux@memory-service.vtt.ai |
| **DL** (Design Lead) | `b3a09269-cded-468c-a475-15a48f203cb0` | dl@memory-service.vtt.ai |
| **QA** | `613c9538-658c-45fe-a6d7-c1ea9ff04b78` | qa@memory-service.vtt.ai |
| **DO** (DevOps) | `322e3745-9756-4a7c-af11-44b33edef44d` | do@memory-service.vtt.ai |
| **IR** (Integration Reviewer) | `f3e358f7-679f-400f-8dd7-df41517bca15` | integration-reviewer@memory-service.vtt.ai |

**Guarda tu UUID** como variable: `export MY_UUID="<tu-uuid>"`

---

## 2. Configuración Base

```
BASE_URL    = http://77.42.88.106:3000
SWAGGER     = http://77.42.88.106:3000/api-docs
SERVICE_KEY = hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d
```

### Obtener JWT (token de 30 días)

```python
python3 -c "
import urllib.request, json, os
data = json.dumps({
    'userId': os.environ['MY_UUID'],
    'serviceKey': 'hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d'
}).encode()
req = urllib.request.Request(
    'http://77.42.88.106:3000/api/auth/service-token',
    data=data,
    headers={'Content-Type': 'application/json'}
)
print(json.loads(urllib.request.urlopen(req).read())['token'])
"
```

Guarda el token: `export TOKEN="<token-obtenido>"`

---

## 3. Tu Flujo de Trabajo (los 12 pasos)

```
┌─ 0. Recibes asignación del TL ─┐
│                                │
│ 1. Leer BRIEF + ASSIGNMENT     │
│ 2. Verificar prerequisitos     │
│ 3. Crear branch Git            │
│ 4. Cambiar status → in_progress│
│ 5. Implementar                 │
│ 6. Crear LOGIC.md              │
│ 7. Crear Swagger (si endpoints)│
│ 8. Testing local               │
│ 9. Crear Dev Log               │
│ 10. Commit + Push              │
│ 11. Crear PR                   │
│ 12. Cambiar status → in_review │
└────────────────────────────────┘
```

---

## 4. PASO 1: Leer el BRIEF y ASSIGNMENT

Cuando el TL te asigna una tarea, lee **ambos documentos** antes de hacer nada:

```bash
# Buscar tu tarea asignada
curl -s "http://77.42.88.106:3000/api/tasks?assignedToId=$MY_UUID&statusCode=task_pending" \
  -H "Authorization: Bearer $TOKEN" | jq .

# Descargar attachments de la tarea
curl -s "http://77.42.88.106:3000/api/tasks/$TASK_ID/attachments" \
  -H "Authorization: Bearer $TOKEN" | jq .
```

### ¿Qué debes encontrar?

| Archivo | Qué contiene |
|---------|--------------|
| **BRIEF** | Alcance técnico, qué hacer, criterios de aceptación, referencias |
| **ASSIGNMENT** | Rama base, PRs previos, dependencias, archivos a leer, checklist |

### ⚠️ Excepción: DevOps

Si eres **DevOps**, NO hay BRIEF ni ASSIGNMENT formal. La **description de la tarea** es tu handoff. Debe incluir:
- Objetivo
- SQL/comandos a ejecutar
- Pre/post checks
- Plan de rollback

---

## 5. PASO 2: Verificar Prerequisitos

Antes de arrancar:

```bash
# 1. Verificar que el backend está vivo
curl -s http://77.42.88.106:3000/health

# 2. Leer comentarios previos de la tarea
curl -s "http://77.42.88.106:3000/api/tasks/$TASK_ID/comments" \
  -H "Authorization: Bearer $TOKEN" | jq .

# 3. Verificar dependencias (¿depende de otras tareas?)
curl -s "http://77.42.88.106:3000/api/tasks/$TASK_ID/dependencies" \
  -H "Authorization: Bearer $TOKEN" | jq .

# 4. Verificar que las tareas de las que dependes están aprobadas
```

**Si alguna dependencia NO está en `task_approved`** → crea issue + on_hold (ver sección 12).

---

## 6. PASO 3: Crear Branch Git

```bash
# Clonar repo (si aún no lo tienes)
git clone <URL_REPO>
cd <repo>

# Configurar user (obligatorio)
git config user.email "<tu-email>@memory-service.vtt.ai"
git config user.name "<tu-rol> Memory Service"

# Actualizar main
git checkout main
git pull origin main

# Crear tu branch
git checkout -b feature/MEM-XXX-descripcion-corta
```

**Convención de nombres:**
- `feature/MEM-123-auth-endpoint` — nueva funcionalidad
- `fix/MEM-124-bug-login` — bugfix
- `docs/MEM-125-readme-update` — solo documentación

---

## 7. PASO 4: Cambiar Status → `in_progress`

**IMPORTANTE**: Tu tarea DEBE tener assignee antes (debería ya tenerlo porque tú la recibiste).

```bash
curl -s -X PATCH http://77.42.88.106:3000/api/tasks/$TASK_ID/status \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "statusId": "2a76888a-e595-4cfc-ac4c-a3ae5087ef56",
    "changedBy": "'$MY_UUID'",
    "reason": "Arrancando implementación"
  }'
```

> **UUID `2a76888a-...`** = `task_in_progress`

### 🚨 REGLA CRÍTICA

**NUNCA cambies el status de una tarea asignada a OTRO agente.**
Solo tus propias tareas.

---

## 8. PASO 5: Implementar

Sigue el scope del BRIEF/ASSIGNMENT al pie de la letra. **NO agregues funcionalidad fuera de scope.**

### Reglas por rol

| Rol | Qué haces | Qué NO haces |
|-----|-----------|--------------|
| **BE** | Endpoints, servicios, lógica de negocio | NO tocas schema Prisma (eso es DB) |
| **DB** | Schema Prisma, migraciones SQL | NO aplicas migración en prod (eso es DO) |
| **FE** | Componentes, páginas, stores | NO tocas endpoints BE |
| **DO** | Docker, CI/CD, deploy, VM | NO tocas lógica de código |
| **QA** | Tests, escenarios, reports | NO modifica código de producción |
| **DL** | Design system, review de HTMLs | NO implementa código FE |
| **UX** | Mockups HTML renderizables | NO conecta APIs ni programa |
| **AR** | Auditorías arquitectónicas | NO implementa fixes |

### 🚨 Reglas absolutas durante implementación

1. **NUNCA mockear datos** — si faltan datos reales → crear issue + on_hold
2. **NUNCA tocar la VM directamente** — reportar al PM, crear BUG para DO
3. **NUNCA commit directo a `main`** — siempre en tu feature branch
4. **NUNCA modificar archivos fuera del scope** de la tarea
5. **NUNCA instalar deps sin documentarlas** en el Dev Log

---

## 9. PASO 6: Crear LOGIC.md (código)

**Regla**: 1 archivo de código = 1 archivo `.LOGIC.md`

```
src/services/memoryService.ts
           ↓
knowledge/code-logic/services/memoryService.LOGIC.md
```

### Contenido del .LOGIC.md

- **QUÉ** hace el archivo (propósito)
- **CÓMO** fluye la lógica (paso a paso)
- **Dependencias** importantes
- **Decisiones de diseño**
- ❌ NO incluir código fuente
- ❌ NO duplicar archivo si ya existe — actualizarlo

---

## 10. PASO 7: Swagger (solo BE si hay endpoints)

**Si creas un endpoint nuevo, agrega JSDoc Swagger inline:**

```javascript
/**
 * @swagger
 * /api/memory/context:
 *   get:
 *     summary: Obtener contexto del agente
 *     tags: [Memory]
 *     security: [{ bearerAuth: [] }]
 *     parameters:
 *       - in: query
 *         name: agentId
 *         required: true
 *         schema: { type: string }
 *     responses:
 *       200: { description: Contexto retornado }
 *       401: { description: No autenticado }
 *       404: { description: Agente no encontrado }
 */
router.get('/context', getContextHandler);
```

### Verificar que funciona

1. Levantar backend: `npm run dev`
2. Abrir: http://77.42.88.106:3000/api-docs
3. Tu endpoint debe aparecer
4. Probar "Try it out"

---

## 11. PASO 8: Testing Local

**Antes de commit, prueba:**

| Rol | Qué probar |
|-----|------------|
| BE | Endpoints con curl/Postman (happy path + errores) |
| DB | Migración local, rollback local, queries de verificación |
| FE | Componente visual + interacciones + estados (loading/error/empty) |
| DO | Script en staging antes de prod, rollback validado |
| QA | Todos los escenarios del test plan |

**Si algo falla**: arregla antes de commit. No subir código roto.

---

## 12. PASO 9: Crear Dev Log

**Ubicación**: `knowledge/development-log/YYYY-MM-DD_MEM-XXX_descripcion-corta.md`

### Contenido obligatorio

```markdown
# Dev Log: MEM-XXX - [Nombre de la tarea]

**Fecha**: 2026-04-22
**Agente**: [tu rol]
**Branch**: feature/MEM-XXX-...

## Qué hice
- [Cambio 1]
- [Cambio 2]

## Archivos creados/modificados
- src/...
- knowledge/code-logic/...

## Decisiones técnicas
- [Decisión 1 y por qué]

## Dependencias agregadas
- [paquete@version y por qué]

## Cómo probar
```bash
# comandos para validar
```

## Pendientes
- [si algo quedó fuera de scope]
```

---

## 13. PASO 10: Commit y Push

### Formato de commit OBLIGATORIO

```
[tipo](repo) [MEM-XXX]: Descripción breve

- Cambio 1
- Cambio 2

Co-Authored-By: Claude <noreply@anthropic.com>
Refs: #MEM-XXX
```

### Tipos

| Tipo | Uso |
|------|-----|
| `feat` | Nueva funcionalidad |
| `fix` | Bugfix |
| `docs` | Solo documentación |
| `refactor` | Refactor sin cambio funcional |
| `test` | Tests |
| `chore` | Setup, config, deps |

### Ejemplo real

```bash
git add .
git commit -m "$(cat <<'EOF'
feat(backend) [MEM-059]: GET /api/memory/context endpoint

- Crear memoryController.ts con getContext handler
- Agregar validación con Zod
- Swagger docs inline

Co-Authored-By: Claude <noreply@anthropic.com>
Refs: #MEM-059
EOF
)"

git push origin feature/MEM-059-context-endpoint
```

### 🚨 Regla absoluta

**Co-Authored-By es OBLIGATORIO en TODOS los commits.**

---

## 14. PASO 11: Crear PR

```bash
gh pr create \
  --title "[MEM-XXX] Descripción breve" \
  --body "$(cat <<'EOF'
## Summary
- Cambio 1
- Cambio 2

## Test plan
- [ ] Endpoint responde 200 con payload válido
- [ ] Endpoint responde 401 sin token
- [ ] Endpoint responde 400 con payload inválido

Ver Dev Log: knowledge/development-log/2026-04-22_MEM-XXX_...md
EOF
)" \
  --base main
```

---

## 15. PASO 12: Cambiar Status → `in_review`

```bash
curl -s -X PATCH http://77.42.88.106:3000/api/tasks/$TASK_ID/status \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "statusId": "1ec975a5-7581-4a1a-ab8f-51b1a7ef868d",
    "changedBy": "'$MY_UUID'",
    "reason": "PR creado, listo para review"
  }'
```

### Agregar comentario con el PR

```bash
curl -s -X POST http://77.42.88.106:3000/api/tasks/$TASK_ID/comments \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "PR #XXX creado: <URL del PR>\nDev Log: knowledge/development-log/...\nBranch: feature/MEM-XXX-...",
    "userId": "'$MY_UUID'"
  }'
```

**YA TERMINASTE tu trabajo.** Ahora espera al TL que hará el review.

---

## 16. 🚨 Cuando te BLOQUEAS (crear issue + on_hold)

### Si te faltan datos, hay un bug de plataforma, o una dependencia no está lista

**Paso A: Crear issue en la tarea**

```bash
curl -s -X POST http://77.42.88.106:3000/api/tasks/$TASK_ID/issues \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Falta catálogo de prioridades",
    "description": "Necesito que existan registros en la tabla priorities para continuar. La tarea depende de datos reales, no puedo mockear.",
    "type": "requirement",
    "severity": "high"
  }'
```

**Paso B: Poner tarea on_hold**

```bash
curl -s -X PUT http://77.42.88.106:3000/api/tasks/$TASK_ID/on-hold \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-user-id: $MY_UUID" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "dependency",
    "title": "Falta data real de prioridades",
    "description": "Ver issue creado. Necesito seeds de catálogo.",
    "priority": "high"
  }'
```

> **⚠️ ERR-004**: NUNCA uses `PATCH /status` para on_hold — rompe `previousStatus` y bloquea el resume.

**Paso C: Notificar al PM** (el TL verá el issue y escalará al PM)

Cuando el issue se resuelva, la tarea se reanuda automáticamente (auto-resume).

---

## 17. 🔄 Si el TL te regresa con NEEDS_FIXES

Si el TL encuentra problemas en tu PR, NO te reasigna ni te lo devuelve — solo agrega comentarios indicando qué falla y te deja en `in_review`.

### Qué haces tú

```bash
# 1. Lee los comentarios
curl -s "http://77.42.88.106:3000/api/tasks/$TASK_ID/comments" \
  -H "Authorization: Bearer $TOKEN" | jq .

# 2. Vuelve a tu branch
git checkout feature/MEM-XXX-...

# 3. Actualiza con main (por si pasó tiempo)
git fetch origin
git rebase origin/main

# 4. Aplica los fixes
# ... haces cambios ...

# 5. Commit + push
git add .
git commit -m "fix(repo) [MEM-XXX]: Aplicar correcciones del review

- Fix 1
- Fix 2

Co-Authored-By: Claude <noreply@anthropic.com>
Refs: #MEM-XXX"

git push origin feature/MEM-XXX-...

# 6. Comentar en la tarea
curl -s -X POST http://77.42.88.106:3000/api/tasks/$TASK_ID/comments \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Correcciones aplicadas en commit <SHA>. Listo para re-review.",
    "userId": "'$MY_UUID'"
  }'
```

---

## 18. 🚨 Reglas Críticas (NO VIOLAR)

1. **NUNCA commit directo a `main`** — siempre feature branch
2. **NUNCA aprobar tareas** (`task_approved`) — solo el PM
3. **NUNCA completar tareas** (`task_completed`) — solo el TL (tú solo llegas a `in_review`)
4. **NUNCA mockear datos** — crear issue + on_hold
5. **NUNCA tocar la VM directamente** — reportar al PM
6. **NUNCA cambiar status de tareas de OTRO agente** — solo tus propias
7. **NUNCA instalar deps sin documentarlas** en el Dev Log
8. **NUNCA hacer merge de tu propio PR** — eso es del PM
9. **NUNCA saltar el review** — si intentas mover a completed, será rechazado
10. **NUNCA ejecutar comandos con `!` en bash** — usar Python (ERR-010)
11. **NUNCA dejar `console.log` de debug** en el código
12. **NUNCA modificar `.env` o `docker-compose`** sin autorización del DO

---

## 19. ✅ Checklist Antes de mover a `in_review`

```
FUNCIONALIDAD:
[ ] El código compila sin errores
[ ] Probé localmente (happy path + errores)
[ ] Pasé todos los escenarios del BRIEF

CALIDAD:
[ ] Seguí la arquitectura existente
[ ] No hay console.log de debug
[ ] Manejo de errores con try-catch
[ ] Nombres consistentes con el proyecto

DOCUMENTACIÓN:
[ ] Creé/actualicé TODOS los archivos .LOGIC.md
[ ] Dev Log completo con decisiones técnicas
[ ] Swagger docs agregados (si hay endpoints)
[ ] Probé /api-docs "Try it out" (si hay endpoints)

GIT:
[ ] Rama `feature/MEM-XXX-...` creada
[ ] Commits con formato correcto + Co-Authored-By
[ ] Push a GitHub
[ ] PR creado con `gh pr create`

ESTADO VTT:
[ ] Status cambiado a `task_in_review`
[ ] Comentario con URL del PR agregado a la tarea
```

Si falta UNO → **NO reportes como listo**.

---

## 20. Referencia Rápida de Endpoints

| Acción | Método | Endpoint |
|--------|--------|----------|
| Obtener token | POST | `/api/auth/service-token` |
| Ver tus tareas | GET | `/api/tasks?assignedToId=$MY_UUID` |
| Ver tarea | GET | `/api/tasks/{id}` |
| Leer attachments | GET | `/api/tasks/{id}/attachments` |
| Leer comentarios | GET | `/api/tasks/{id}/comments` |
| Crear comentario | POST | `/api/tasks/{id}/comments` |
| Cambiar status | PATCH | `/api/tasks/{id}/status` |
| Ver dependencies | GET | `/api/tasks/{id}/dependencies` |
| Crear issue | POST | `/api/tasks/{taskId}/issues` |
| On-hold | PUT | `/api/tasks/{id}/on-hold` (header x-user-id) |
| Swagger | GET | `/api-docs` |

### UUIDs de Status (para PATCH /status)

| Status | UUID |
|--------|------|
| task_in_progress | `2a76888a-e595-4cfc-ac4c-a3ae5087ef56` |
| task_in_review | `1ec975a5-7581-4a1a-ab8f-51b1a7ef868d` |
| task_on_hold | `c62eb334-b7bc-4c9f-af85-a5666c262aaa` |

---

## 21. Documentos de Referencia

| Documento | Ubicación |
|-----------|-----------|
| Reglas globales | `C:\Users\Martin\.claude\rules\rules_agents.instructions.md` |
| Onboarding TL | `00-platform/ONBOARDING_TL_MEMORY_SERVICE.md` |
| Spec del producto | `memory-service-project/Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` |
| Metodología | `memory-service-project/Release2.0/01-PM/METODOLOGIA_MEMORY_SERVICE_v1.2.md` |
| Template Dev Log | `_project-management/templates/TEMPLATE_DEVELOPMENT_LOG.md` |
| Template LOGIC.md | `_project-management/templates/TEMPLATE_CODE_LOGIC.md` |
| Swagger API | http://77.42.88.106:3000/api-docs |

---

## 22. Primera Respuesta Esperada del Agente

Al recibir este onboarding, responde al TL/PM con:

1. "Leí el onboarding. Entendí mi rol: [tu rol]."
2. "Mi UUID es: [tu UUID]."
3. "Estoy listo para recibir tareas."
4. Si hay algo que NO te quedó claro → pregúntalo antes de arrancar.

---

**Creado por**: PM (Martin Rivas)
**Fecha**: 2026-04-22
**Versión**: 1.0
