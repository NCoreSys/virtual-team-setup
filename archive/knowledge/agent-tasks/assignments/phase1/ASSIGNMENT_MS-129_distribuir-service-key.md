# ASSIGNMENT: MS-129 / INIT-C-03 — Distribuir SERVICE_KEY a consumidores

```
Hola DO,

El Memory Service tiene una SERVICE_KEY que deben usar los 4 servicios que lo consumen.
Tu tarea es coordinar la distribución segura de esa key y confirmar que cada consumidor
puede autenticarse correctamente.

### TAREA ASIGNADA

MS-129: INIT-C-03 — Distribuir SERVICE_KEY a consumidores
- Estimacion: 1 hora
- Complejidad: MEDIUM
- Categoria: deployment
- Prioridad: HIGH
- Brief: knowledge/agent-tasks/briefs/phase1/BRIEF_INIT-C-03_distribuir-service_key-a-consumidores.md

---

### ANTES DE EMPEZAR

1. Este ASSIGNMENT completo
2. MS-127 completada (infra verificada — SERVICE_KEY en .env confirmada)
3. PROJECT_RULES.md §15.3 (nunca hardcodear, no mockear datos)
4. CONTEXTO_DO_SESION.md §5 (credenciales de infra)

---

### CREDENCIALES

Agente DO:
    userId:     322e3745-9756-4a7c-af11-44b33edef44d
    serviceKey: hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d
    email:      memory-service.devops@vtt.ai

VM Hetzner:
    IP: 77.42.88.106

API VTT:
    Base:    http://77.42.88.106:3000

Status UUIDs:
    task_in_progress: 2a76888a-e595-4cfc-ac4c-a3ae5087ef56
    task_in_review:   1ec975a5-7581-4a1a-ab8f-51b1a7ef868d

---

### CONTEXTO: LOS 4 CONSUMIDORES

| Servicio | Descripción | Cómo usa la key |
|---------|-------------|-----------------|
| Runtime v1.1 | Motor de agentes VTT | Header X-Service-Key o env MEMORY_SERVICE_KEY |
| Prompt Builder v1.3 | Editor de prompts | Env MEMORY_SERVICE_KEY |
| Hook Manager | Webhook processor | Env MEMORY_SERVICE_KEY |
| FE (Memory Service UI) | Frontend React | Env variable en .env |

---

### REGLA CRÍTICA: SEGURIDAD DE LA KEY

- La SERVICE_KEY NO se commitea a ningún repo
- Se distribuye via GitHub Secrets, variables de entorno en servidor, o mensaje directo seguro
- El inventario (este doc + PAT_INVENTORY) registra QUIÉN recibió la key, NO el valor

---

### PROCESO DE DISTRIBUCIÓN

#### Paso A: Obtener la SERVICE_KEY del Memory Service
```bash
# Verificar que está en el .env del servidor
ssh root@77.42.88.106 "grep SERVICE_KEY /path/to/memory-service/.env"
# El valor lo conoce el DO — NO lo compartas en documentos
```

#### Paso B: Distribuir a cada consumidor

Para cada servicio, el método de distribución es:

**GitHub Actions Secrets** (recomendado para servicios con CI):
```bash
gh secret set MEMORY_SERVICE_KEY --repo NCoreSys/<repo-consumidor> --body "<valor>"
```

**Variable de entorno en servidor** (para servicios ya deployados):
```bash
ssh root@77.42.88.106 "echo 'MEMORY_SERVICE_KEY=<valor>' >> /path/to/<servicio>/.env"
```

#### Paso C: Verificar autenticación desde cada consumidor
```bash
# Test básico desde cada servicio
curl -H "X-Service-Key: <MEMORY_SERVICE_KEY>" http://77.42.88.106:3002/api/health
# Esperado: 200 OK (cuando el servicio esté deployado)
# Si servicio no deployado aún: documentar como "key configurada, verificación pendiente deploy"
```

---

### WORKFLOW (12 pasos)

Paso 0: Crear rama
    git checkout -b feature/MS-129

Paso 1: Mover MS-129 a task_in_progress con credenciales DO

Paso 2: Obtener SERVICE_KEY del servidor (verificar .env Memory Service)

Paso 3: Distribuir a Runtime v1.1 (via GitHub Secret o .env del servidor)

Paso 4: Distribuir a Prompt Builder v1.3

Paso 5: Distribuir a Hook Manager

Paso 6: Distribuir a FE Memory Service

Paso 7: Verificar autenticación de cada consumidor (o documentar como pendiente si no deployado)

Paso 8: Crear inventario de distribución:
    knowledge/infra/SERVICE_KEY_DISTRIBUTION.md
    (sin el valor de la key — solo: servicio, método, fecha, estado)

Paso 9: Crear DevLog:
    devlogs/2026-04-24_MS-129_distribuir-service-key.md

Paso 10: Crear Code Logic placeholder:
    knowledge/code-logic/phase1/MS-129_service-key-distribution.LOGIC.md

Paso 11: Commit y push (SIN el valor de la key)
    git add knowledge/infra/SERVICE_KEY_DISTRIBUTION.md devlogs/ knowledge/code-logic/
    git commit -m "docs [MS-129]: Inventario distribución SERVICE_KEY consumidores

    - 4 consumidores: Runtime, Prompt Builder, Hook Manager, FE
    - Sin valores de key — solo metadata de distribución

    Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
    Refs: #MS-129"
    git push origin feature/MS-129

Paso 12: Subir attachments a VTT + mover a task_in_review

---

### CHECKLIST DE EXITO

- [ ] SERVICE_KEY obtenida del servidor (no commiteada)
- [ ] Runtime v1.1: key distribuida
- [ ] Prompt Builder v1.3: key distribuida
- [ ] Hook Manager: key distribuida
- [ ] FE Memory Service: key distribuida
- [ ] SERVICE_KEY_DISTRIBUTION.md creado (sin valores)
- [ ] Verificación de auth: OK o "pendiente deploy del servicio"
- [ ] NINGÚN valor de key en ningún archivo commiteado

---

### FORMATO DE REPORTE

    ## Entrega: MS-129 - INIT-C-03: Distribución SERVICE_KEY

    ### Estado por consumidor:
    | Consumidor | Key distribuida | Auth verificada |
    |-----------|----------------|-----------------|
    | Runtime v1.1 | SI/NO | OK/PENDIENTE |
    | Prompt Builder v1.3 | SI/NO | OK/PENDIENTE |
    | Hook Manager | SI/NO | OK/PENDIENTE |
    | FE Memory Service | SI/NO | OK/PENDIENTE |

    ### Inventario:
    knowledge/infra/SERVICE_KEY_DISTRIBUTION.md ✅

    ### Development Log:
    devlogs/2026-04-24_MS-129_distribuir-service-key.md

    ### Commit SHA: [hash]

---

IMPORTANTE: Si algún consumidor no tiene repo activo todavía, documentar como
"pendiente — servicio en desarrollo" y dejar esa parte como task_on_hold parcial.

Saludos,
PJM (coordinación Fase 1 Project Setup)
```

---

## Metadata

- **Archivo**: `knowledge/agent-tasks/assignments/phase1/ASSIGNMENT_MS-129_distribuir-service-key.md`
- **Fecha generacion**: 2026-04-24
- **Version**: 1.0
- **Estado**: Ready
