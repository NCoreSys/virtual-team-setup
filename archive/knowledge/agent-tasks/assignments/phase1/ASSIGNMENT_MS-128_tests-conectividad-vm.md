# ASSIGNMENT: MS-128 / INIT-C-02 — Tests de conectividad local a VM

```
Hola DO,

Esta tarea valida que desde desarrollo local se puede acceder a todos los servicios
en la VM Hetzner (77.42.88.106). Es prerequisito para que el equipo de desarrollo
pueda trabajar con la infra real antes de levantar el stack local.

### TAREA ASIGNADA

MS-128: INIT-C-02 — Tests de conectividad local a VM
- Estimacion: 1 hora
- Complejidad: MEDIUM
- Categoria: deployment
- Prioridad: MEDIUM
- Brief: knowledge/agent-tasks/briefs/phase1/BRIEF_INIT-C-02_tests-de-conectividad-local-a-vm.md

---

### ANTES DE EMPEZAR

1. Este ASSIGNMENT completo
2. MS-127 completada (infra Hetzner verificada)
3. knowledge/agent-tasks/assignments/phase1/ASSIGNMENT_MS-127_verificar-infraestructura-hetzner.md
4. PROJECT_RULES.md §10 (manejo de problemas)

---

### CREDENCIALES

Agente DO:
    userId:     322e3745-9756-4a7c-af11-44b33edef44d
    serviceKey: hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d
    email:      memory-service.devops@vtt.ai

VM Hetzner:
    IP:     77.42.88.106
    Puertos relevantes:
      3000  VTT (operativo)
      3002  Memory Service API
      3003  Memory Service UI
      5432  PostgreSQL (shared-postgres)
      6379  Redis (shared-redis)

API VTT:
    Base:    http://77.42.88.106:3000

Status UUIDs:
    task_in_progress: 2a76888a-e595-4cfc-ac4c-a3ae5087ef56
    task_in_review:   1ec975a5-7581-4a1a-ab8f-51b1a7ef868d

---

### TESTS A EJECUTAR

#### Test 1: PostgreSQL — Base de datos memory_service_db
```bash
# Desde local, via psql o conexión directa
psql -h 77.42.88.106 -U memory_service_user -d memory_service_db -c "SELECT 1;"
# Esperado: "1" como resultado
```

#### Test 2: Volumen de storage — Escritura en /root/memory-service-storage/
```bash
# Via SSH al servidor
ssh root@77.42.88.106 "echo 'test' > /root/memory-service-storage/test.txt && cat /root/memory-service-storage/test.txt && rm /root/memory-service-storage/test.txt"
# Esperado: "test" impreso, sin errores de permisos
```

#### Test 3: Redis — PING con prefix mem
```bash
# Via redis-cli
redis-cli -h 77.42.88.106 -p 6379 PING
# Esperado: PONG
redis-cli -h 77.42.88.106 -p 6379 SET mem:test "ok"
redis-cli -h 77.42.88.106 -p 6379 GET mem:test
# Esperado: "ok"
redis-cli -h 77.42.88.106 -p 6379 DEL mem:test
```

#### Test 4: Puerto 3002 (API Memory Service)
```bash
curl -s http://77.42.88.106:3002/health || echo "Puerto 3002 no responde (esperado si servicio aun no deployado)"
# Si el servicio no está deployado, documentar como "puerto disponible pero servicio pendiente"
```

#### Test 5: Puerto 3003 (UI Memory Service)
```bash
curl -s -o /dev/null -w "%{http_code}" http://77.42.88.106:3003 || echo "Puerto 3003 no responde (esperado si servicio aun no deployado)"
```

#### Test 6: Docker network shared-network
```bash
ssh root@77.42.88.106 "docker network ls | grep shared-network"
# Esperado: shared-network aparece en la lista
```

#### Test 7: Conectividad general — VTT operativo
```bash
curl -s http://77.42.88.106:3000/api/health | python3 -m json.tool
# Esperado: {"status": "ok"} o similar
```

---

### WORKFLOW (12 pasos)

Paso 0: Crear rama
    git checkout -b feature/MS-128

Paso 1: Mover MS-128 a task_in_progress con credenciales DO

Paso 2: Ejecutar Test 7 primero (VTT ya operativo — baseline)

Paso 3: Ejecutar Tests 1-6 en orden, documentar cada resultado

Paso 4: Para cada test FALLIDO — aplicar §15.3 de PROJECT_RULES:
    - Crear ISSUE si hay blocker real
    - Documentar en DevLog como pendiente
    - NO mockear resultados

Paso 5: Crear reporte de conectividad:
    knowledge/infra/CONNECTIVITY_REPORT_MS-128.md
    con tabla: Test | Resultado | Comando ejecutado | Output

Paso 6: Crear DevLog:
    devlogs/2026-04-24_MS-128_tests-conectividad-vm.md

Paso 7: Crear Code Logic placeholder:
    knowledge/code-logic/phase1/MS-128_connectivity-tests.LOGIC.md

Paso 8: Commit y push
    git add knowledge/infra/ devlogs/ knowledge/code-logic/
    git commit -m "docs [MS-128]: Reporte tests conectividad VM

    - 7 tests ejecutados contra 77.42.88.106
    - Resultado: [N]/7 OK
    - Ver CONNECTIVITY_REPORT_MS-128.md para detalle

    Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
    Refs: #MS-128"
    git push origin feature/MS-128

Paso 9: Subir attachments a VTT (devlog, code_logic, reporte connectivity)

Paso 10: Postear comentario de entrega en MS-128

Paso 11: Mover MS-128 a task_in_review

---

### CHECKLIST DE EXITO

- [ ] Test PostgreSQL memory_service_db: OK/FAIL documentado
- [ ] Test volumen /storage/: OK/FAIL documentado
- [ ] Test Redis PING con prefix mem: OK/FAIL documentado
- [ ] Test puerto 3002: OK/PENDIENTE documentado
- [ ] Test puerto 3003: OK/PENDIENTE documentado
- [ ] Test Docker shared-network: OK/FAIL documentado
- [ ] Test VTT :3000: OK (ya operativo)
- [ ] CONNECTIVITY_REPORT_MS-128.md creado
- [ ] DevLog con output de cada test
- [ ] Si algún test falla: ISSUE creado + tarea en task_on_hold

---

### NOTAS IMPORTANTES

- Los puertos 3002 y 3003 pueden no responder si Memory Service aún no está deployado.
  Esto NO es un error — documenta como "puerto disponible, servicio pendiente deploy".
- Si PostgreSQL no está accesible desde local (firewall), documentar como blocker
  y crear ISSUE para que el Coordinador abra el puerto.
- El output completo de cada comando debe estar en el CONNECTIVITY_REPORT.

---

### FORMATO DE REPORTE

    ## Entrega: MS-128 - INIT-C-02: Tests de conectividad VM

    ### Resultados:
    | Test | Componente | Resultado |
    |------|-----------|-----------|
    | 1 | PostgreSQL memory_service_db | OK/FAIL |
    | 2 | Volumen /storage/ escritura | OK/FAIL |
    | 3 | Redis PING prefix mem | OK/FAIL |
    | 4 | Puerto 3002 (API) | OK/PENDIENTE |
    | 5 | Puerto 3003 (UI) | OK/PENDIENTE |
    | 6 | Docker shared-network | OK/FAIL |
    | 7 | VTT :3000 baseline | OK |

    ### ISUEs creados: [N] (si hay blockers)

    ### Development Log:
    devlogs/2026-04-24_MS-128_tests-conectividad-vm.md

    ### Commit SHA: [hash]

---

Saludos,
PJM (coordinación Fase 1 Project Setup)
```

---

## Metadata

- **Archivo**: `knowledge/agent-tasks/assignments/phase1/ASSIGNMENT_MS-128_tests-conectividad-vm.md`
- **Fecha generacion**: 2026-04-24
- **Version**: 1.0
- **Estado**: Ready
