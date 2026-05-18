# ASSIGNMENT: MS-143 — ISS-25b344aa: Resolver discrepancia naming proyecto VTT (name + key)

```
Hola PM,

Contexto: La verificacion de MS-117 (INIT-A-01) detecto que el proyecto en VTT
se llama "Memory Service" con key "MS", pero la documentacion HO_INICIACION y
PROJECT_MEMORY asumen "Memory Service R1" y key "MEM". MS-117 esta en
task_on_hold esperando tu decision. Esta tarea (MS-143) es para que resuelvas
el ISSUE y liberes MS-117.

Te asigno la siguiente tarea:

### TAREA ASIGNADA

MS-143: ISS-25b344aa — Resolver discrepancia naming proyecto VTT (name + key)
- Estimacion: 1 hora
- Complejidad: LOW
- Categoria: documentation
- Prioridad: Medium
- Brief: knowledge/agent-tasks/briefs/phase1/BRIEF_MS-143_resolver-discrepancia-naming-proyecto-vtt.md
- sourceIssueId: 25b344aa-4ab7-4edd-ae5b-9f6856f3a1c0
- Tarea bloqueada por este issue: MS-117 (INIT-A-01)

---

### ANTES DE EMPEZAR — LEE ESTO PRIMERO

1. BRIEF ya adjunto en VTT (fileType="brief")
2. Este ASSIGNMENT completo
3. ISSUE 25b344aa (GET /api/issues/25b344aa-4ab7-4edd-ae5b-9f6856f3a1c0)
4. DevLog de MS-117 donde se detecto la discrepancia:
   devlogs/2026-04-22_INIT-A-01_verificar-proyecto-vtt.md

---

### ENTREGABLES OBLIGATORIOS

Por tipo de tarea (decision + docs o PATCH al proyecto):

| # | Entregable | Aplica |
|---|------------|--------|
| 1 | Codigo | Depende: Opcion A = script PATCH; Opcion B = cambios en docs |
| 2 | Development Log | SI (siempre) |
| 3 | Code Logic | NO (no hay archivo de codigo persistente tipo .js o .ts) |
| 4 | Git (rama + commit + PR) | SI para Opcion B (cambios en docs); opcional para A |
| 5 | Swagger docs | NO |

Antes de in_review el sistema VTT exige 3 attachments:
- DevLog (fileType="devlog")
- Code Logic minimo (fileType="code_logic") — placeholder similar al de MS-117
- Comentario/reporte en la tarea

---

### RESUMEN DE OPCIONES (del BRIEF)

| Opcion | Accion | Impacto |
|--------|--------|---------|
| **A** | PATCH proyecto VTT a name="Memory Service R1" + key="MEM" | Afecta task codes actuales MS-* (142 en uso). Pueden quedar mezclados MS-* viejos + MEM-* nuevos. |
| **B** | Actualizar docs (HO, PROJECT_MEMORY, 26 BRIEFs, 1 ASSIGNMENT) a "Memory Service" + "MS" | Mas seguro. No toca task codes. |
| **C** | Divergencia intencional con glosario "alias MEM = key MS" | No recomendado. |

Recomendacion PJM: **Opcion B** (menor riesgo operativo).

---

### API / RECURSOS DISPONIBLES

YA FUNCIONAN:

Auth:
  POST http://77.42.88.106:3000/api/auth/service-token
       body: {"userId": "350831b2-e1ae-4dbe-b2eb-7e023ec2e103",
              "serviceKey": "<SERVICE_KEY_PM>"}
       response: {"success": true, "data": {"token": "<JWT>"}}

Lectura del proyecto:
  GET  http://77.42.88.106:3000/api/projects/d0fc276d-e764-4a83-96e9-d65f086ed803
       headers: Authorization: Bearer <JWT>

Para Opcion A — PATCH del proyecto:
  PATCH http://77.42.88.106:3000/api/projects/d0fc276d-e764-4a83-96e9-d65f086ed803
        headers: Authorization: Bearer <JWT>
        body: {"name": "Memory Service R1", "key": "MEM"}
  NOTA: confirmar primero con PATCH en un proyecto de prueba que el cambio de
  `key` no rompe los task codes existentes. Si falla, caer a Opcion B.

Para Opcion B — no requiere API. Solo actualizacion de archivos:
  grep -rn "Memory Service R1" memory-service-project/ knowledge/
  grep -rn "key.*MEM\|\\\"MEM\\\"" knowledge/ memory-service-project/

Issue para resolver:
  GET  /api/issues/25b344aa-4ab7-4edd-ae5b-9f6856f3a1c0  (inspeccionar)
  El sistema auto-marca isResolved=true al mover MS-143 a task_completed.
  No hace falta PUT manual al issue si se completa la tarea normalmente.

---

### WORKFLOW (12 pasos adaptado)

0. Obten tu JWT (PM):
   python3 -c "
   import urllib.request, json, sys
   req = urllib.request.Request(
       'http://77.42.88.106:3000/api/auth/service-token',
       data=json.dumps({'userId': '350831b2-e1ae-4dbe-b2eb-7e023ec2e103',
                        'serviceKey': '<TU_SERVICE_KEY>'}).encode(),
       headers={'Content-Type': 'application/json'}, method='POST')
   with urllib.request.urlopen(req) as r:
       sys.stdout.write(json.loads(r.read())['data']['token'])
   " > /tmp/token.txt

1. Mueve la tarea MS-143 a task_in_progress:
   TOKEN=$(cat /tmp/token.txt)
   curl -s -X PATCH \
     http://77.42.88.106:3000/api/tasks/MS-143/status \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"statusId": "2a76888a-e595-4cfc-ac4c-a3ae5087ef56",
          "changedBy": "350831b2-e1ae-4dbe-b2eb-7e023ec2e103",
          "reason": "Resolviendo decision de naming del proyecto"}'

2. Lee BRIEF adjunto y el DevLog de MS-117.

3. Decide Opcion A, B o C. Documenta la razon.

4. (Opcional si A) Crea rama feature/MS-143 para el PATCH script o el grep/update.
   git checkout -b feature/MS-143

5. Ejecuta la accion:
   - Opcion A: PATCH al proyecto VTT con name y key nuevos.
   - Opcion B: actualizar los ~28 archivos (HO, PROJECT_MEMORY, 26 BRIEFs,
     1 ASSIGNMENT). Un script `sed` o busqueda/reemplazo con editor sirve.
   - Opcion C: crear/actualizar seccion "Naming" en PROJECT_MEMORY.md con
     glosario.

6. Verifica:
   - Opcion A: GET al proyecto muestra los valores nuevos.
   - Opcion B: grep no devuelve mas referencias "Memory Service R1" ni "MEM"
     (excepto en el DevLog que documenta la decision).
   - Opcion C: seccion glosario visible en PROJECT_MEMORY.

7. Escribe Development Log:
   devlogs/YYYY-MM-DD_MS-143_resolver-naming-proyecto.md
   Contenido minimo:
     - Opcion elegida (A, B o C) + razon
     - Comandos ejecutados o archivos modificados
     - Resultado de verificacion
     - Impacto en MS-117 y otras tareas futuras

8. Crea Code Logic minimo (placeholder si no hubo codigo):
   knowledge/code-logic/phase1/MS-143_no-code.LOGIC.md

9. Sube DevLog como attachment a MS-143:
   curl -s -X POST \
     "http://77.42.88.106:3000/api/tasks/MS-143/attachments" \
     -F "file=@devlogs/YYYY-MM-DD_MS-143_resolver-naming-proyecto.md" \
     -F "fileType=devlog" \
     -F "uploadedById=350831b2-e1ae-4dbe-b2eb-7e023ec2e103"

10. Sube Code Logic como attachment a MS-143:
    curl -s -X POST \
      "http://77.42.88.106:3000/api/tasks/MS-143/attachments" \
      -F "file=@knowledge/code-logic/phase1/MS-143_no-code.LOGIC.md" \
      -F "fileType=code_logic" \
      -F "uploadedById=350831b2-e1ae-4dbe-b2eb-7e023ec2e103"

11. Sube comentario/reporte a la tarea:
    curl -s -X POST \
      http://77.42.88.106:3000/api/tasks/MS-143/comments \
      -H "Content-Type: application/json" \
      -d '{"message": "<REPORTE>", "userId": "350831b2-e1ae-4dbe-b2eb-7e023ec2e103"}'

12. Mueve MS-143 a task_in_review:
    curl -s -X PATCH \
      http://77.42.88.106:3000/api/tasks/MS-143/status \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"statusId": "1ec975a5-7581-4a1a-ab8f-51b1a7ef868d",
           "changedBy": "350831b2-e1ae-4dbe-b2eb-7e023ec2e103",
           "reason": "Decision tomada y aplicada"}'

IMPORTANTE: al completar MS-143 (task_completed por el TL), el sistema
automaticamente:
  a) Marca el issue 25b344aa como isResolved=true
  b) Auto-resume MS-117 (sale de task_on_hold y vuelve a task_in_progress)

---

### CHECKLIST DE ENTREGA

Funcional:
- [ ] Opcion elegida (A, B o C) y razon documentada
- [ ] Accion ejecutada (PATCH proyecto, o update de docs, o glosario)
- [ ] Verificacion post-accion: sin divergencias restantes
- [ ] Issue 25b344aa quedara resuelto al mover a completed (automatico)
- [ ] MS-117 se desbloqueara al resolverse el issue (automatico)

Calidad:
- [ ] DevLog completo con decision + comandos + verificacion
- [ ] Code Logic minimo subido
- [ ] Comentario/reporte subido con formato del BRIEF

Estado:
- [ ] MS-143 en task_in_review (tu accion)
- [ ] Espera revision del TL para mover a completed

---

### ARCHIVOS A CREAR/MODIFICAR

**Siempre:**
- devlogs/YYYY-MM-DD_MS-143_resolver-naming-proyecto.md (nuevo)
- knowledge/code-logic/phase1/MS-143_no-code.LOGIC.md (nuevo — placeholder)

**Si Opcion A** (PATCH VTT):
- scripts/patch_project_naming.py (opcional — script con el PATCH)

**Si Opcion B** (docs):
- memory-service-project/01-project-management/00-setup/HO_INICIACION_MEMORY_SERVICE.md
- PROJECT_MEMORY.md (si existe en el repo)
- knowledge/agent-tasks/briefs/phase1/BRIEF_INIT-A-01..G-02.md (26 archivos)
- knowledge/agent-tasks/assignments/phase1/ASSIGNMENT_INIT-A-01_verificar-proyecto-en-vtt.md

**Si Opcion C:**
- PROJECT_MEMORY.md — agregar seccion "Naming"

---

### FORMATO DE REPORTE AL COMPLETAR

Pegar en el comentario de la tarea:

    ## Entrega: MS-143 - Resolver discrepancia naming proyecto VTT

    ### Opcion elegida: [A / B / C]
    ### Razon: [por que esa opcion]

    ### Accion ejecutada:
    - [describir que se hizo: PATCH o cambios en docs]

    ### Verificacion:
    - [resultado de GET del proyecto o grep post-actualizacion]

    ### Archivos modificados:
    - [lista]

    ### Development Log:
    devlogs/YYYY-MM-DD_MS-143_resolver-naming-proyecto.md

    ### Impacto:
    - Issue 25b344aa sera auto-resuelto al completar esta tarea
    - MS-117 saldra automaticamente de task_on_hold

---

Empieza leyendo el BRIEF y este ASSIGNMENT. Tomas la decision, ejecutas y me
avisas cuando este en task_in_review para que el TL (yo) revise y cierre.

Al cerrar MS-143 como task_completed, MS-117 se libera automaticamente.

Saludos,
PJM (en coordinacion con TL)
```

---

## Metadata

- **Archivo**: `knowledge/agent-tasks/assignments/phase1/ASSIGNMENT_MS-143_resolver-discrepancia-naming-proyecto-vtt.md`
- **Tarea**: MS-143
- **Asignada a**: Memory Service PM (`350831b2-e1ae-4dbe-b2eb-7e023ec2e103`, `pm@memory-service.vtt.ai`)
- **Version**: 1.0
- **Estado**: Ready para ejecucion

## Datos reales verificados para este ASSIGNMENT

- Token PM confirmado funcional (obtenido via service-token)
- Endpoint PATCH /api/projects/{id} existe (aunque no se probo aun el cambio de key)
- Issue 25b344aa estado: isResolved=false, resolvedByTaskId=MS-143 (vinculado)
- MS-117 estado: task_on_hold con onHoldIssueId apuntando a 25b344aa
