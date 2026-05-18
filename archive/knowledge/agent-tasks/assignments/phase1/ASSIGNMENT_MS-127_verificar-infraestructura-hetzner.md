# ASSIGNMENT: MS-127 / INIT-C-01 — Verificar infraestructura provisionada en Hetzner

```
Hola DO,

El servidor Hetzner (77.42.88.106) esta corriendo VTT en puerto 3000. Tu tarea
es verificar que la infra base para Memory Service tambien esta provisionada
segun SPEC v1.9 §16.

### TAREA ASIGNADA

MS-127: INIT-C-01 — Verificar infraestructura provisionada en Hetzner
- Estimacion: 1 hora
- Complejidad: MEDIUM
- Categoria: deployment
- Prioridad: HIGH
- Brief: knowledge/agent-tasks/briefs/phase1/BRIEF_INIT-C-01_verificar-infraestructura-provisionada-e.md

---

### ANTES DE EMPEZAR - LEE ESTO PRIMERO

1. BRIEF adjunto (ver ruta arriba)
2. SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md §16 (infraestructura Docker)
3. PROJECT_RULES.md §3 y §9 (workflow, entrega)

Config Git:
    git config user.name "Martin Rivas"
    git config user.email "martin.rivas@prompt-ai.studio"

---

### CONTEXTO TECNICO

Servidor: 77.42.88.106 (Hetzner)
VTT ya corre en puerto 3000 en este servidor.

Lo que se debe verificar para Memory Service:
- BD: memory_service_db en shared-postgres (PostgreSQL)
- Volumen: /root/memory-service-storage/ con permisos escritura
- Redis: prefix "mem" en shared-redis
- Puertos: 3002 (API) y 3003 (UI) abiertos en firewall
- Red Docker: shared-network existe
- Config: SERVICE_KEY en .env del servidor

---

### CREDENCIALES

Agente DO:
    userId:     322e3745-9756-4a7c-af11-44b33edef44d
    serviceKey: hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d

API VTT:
    Base:    http://77.42.88.106:3000
    Auth:    POST /api/auth/service-token

Status UUIDs:
    task_in_progress: 2a76888a-e595-4cfc-ac4c-a3ae5087ef56
    task_in_review:   1ec975a5-7581-4a1a-ab8f-51b1a7ef868d

Acceso SSH al servidor: usar las credenciales configuradas en tu entorno.

---

### ENTREGABLES OBLIGATORIOS

| # | Entregable | Aplica |
|---|------------|--------|
| 1 | Codigo | NO |
| 2 | Development Log | SI |
| 3 | Code Logic placeholder | SI (gate VTT) |
| 4 | Git (rama + commit) | SI — solo para el DevLog |
| 5 | Swagger | NO |

Ademas crear: docs/INFRASTRUCTURE.md con checklist verificado.

---

### WORKFLOW (12 pasos)

Paso 0: Crear rama
    git checkout -b feature/MS-127

Paso 1: Mover a task_in_progress con tus credenciales DO

Paso 2: Obtener JWT DO
    python3 -c "
    import urllib.request, json
    req = urllib.request.Request(
        'http://77.42.88.106:3000/api/auth/service-token',
        data=json.dumps({
            'userId': '322e3745-9756-4a7c-af11-44b33edef44d',
            'serviceKey': 'hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d'
        }).encode(),
        headers={'Content-Type': 'application/json'}, method='POST')
    with urllib.request.urlopen(req) as r:
        print(json.loads(r.read())['data']['token'])
    " > /tmp/token_do.txt

Paso 3: Verificar BD memory_service_db
    ssh root@77.42.88.106 "docker exec shared-postgres psql -U postgres \
      -c '\l' | grep memory_service_db"
    # Esperado: memory_service_db en la lista

Paso 4: Verificar volumen de storage
    ssh root@77.42.88.106 "ls -la /root/memory-service-storage/ 2>/dev/null \
      || echo 'VOLUMEN NO EXISTE'"
    # Esperado: directorio con permisos rwx

Paso 5: Verificar Redis prefix
    ssh root@77.42.88.106 "docker exec shared-redis redis-cli PING"
    # Esperado: PONG

Paso 6: Verificar puertos 3002 y 3003
    nc -zv 77.42.88.106 3002 2>&1
    nc -zv 77.42.88.106 3003 2>&1
    # Si no hay respuesta: puertos cerrados → documentar como pendiente

Paso 7: Verificar shared-network Docker
    ssh root@77.42.88.106 "docker network ls | grep shared-network"
    # Esperado: shared-network en la lista

Paso 8: Verificar SERVICE_KEY en .env
    ssh root@77.42.88.106 "cat /root/memory-service/.env 2>/dev/null \
      | grep SERVICE_KEY || echo 'SERVICE_KEY no configurada'"

Paso 9: Crear docs/INFRASTRUCTURE.md con checklist (ver formato abajo)

Paso 10: Crear DevLog en:
    devlogs/2026-04-24_MS-127_verificar-infraestructura-hetzner.md

Paso 11: Crear Code Logic placeholder:
    knowledge/code-logic/phase1/MS-127_no-code.LOGIC.md

Paso 12: Subir attachments a VTT, postear comentario, mover a task_in_review

---

### FORMATO docs/INFRASTRUCTURE.md

    # Infrastructure Checklist — Memory Service

    **Fecha verificacion**: 2026-04-24
    **Servidor**: 77.42.88.106 (Hetzner)
    **Verificado por**: DO

    | Item | Estado | Detalle |
    |------|--------|---------|
    | memory_service_db (PostgreSQL) | [OK/PENDIENTE] | [detalle] |
    | /root/memory-service-storage/ | [OK/PENDIENTE] | [permisos] |
    | Redis prefix mem | [OK/PENDIENTE] | [respuesta PING] |
    | Puerto 3002 abierto | [OK/PENDIENTE] | [nc output] |
    | Puerto 3003 abierto | [OK/PENDIENTE] | [nc output] |
    | shared-network Docker | [OK/PENDIENTE] | [network ID] |
    | SERVICE_KEY en .env | [OK/PENDIENTE] | [si existe o no] |

---

### FORMATO DE REPORTE AL COMPLETAR

    ## Entrega: MS-127 - INIT-C-01: Verificar infraestructura Hetzner

    ### Checklist:
    - memory_service_db: [OK/PENDIENTE]
    - /root/memory-service-storage/: [OK/PENDIENTE]
    - Redis prefix mem: [OK/PENDIENTE]
    - Puerto 3002: [OK/PENDIENTE]
    - Puerto 3003: [OK/PENDIENTE]
    - shared-network: [OK/PENDIENTE]
    - SERVICE_KEY: [OK/PENDIENTE]

    ### Items pendientes de provisionamiento:
    - [lista o "ninguno"]

    ### Development Log:
    devlogs/2026-04-24_MS-127_verificar-infraestructura-hetzner.md

    ### Docs creados:
    docs/INFRASTRUCTURE.md

    ### Commit SHA: [hash]

---

Si algun item no esta provisionado, documentarlo como PENDIENTE en INFRASTRUCTURE.md
y notificarme para que el PM coordine el provisionamiento.

Saludos,
Tech Lead / PJM (coordinacion Fase 1 Project Setup)
```

---

## Metadata

- **Archivo**: `knowledge/agent-tasks/assignments/phase1/ASSIGNMENT_MS-127_verificar-infraestructura-hetzner.md`
- **Fecha generacion**: 2026-04-24
- **Version**: 1.0
- **Estado**: Ready
