# PROCESO — Setup de Sprint y Generación de BRIEFs

**Versión:** 1.5  
**Fecha:** 2026-05-20  
**Autor:** TL (Martin Rivas)  
**Complementa:** `PROCESO_ASIGNACION_TAREAS_v3.md` (Fase 1)  
**Motivo:** Refinado durante setup de Sprint S2 — Memory Service.

---

## PROPÓSITO

Define el proceso completo desde que el TL recibe el documento de entrada de un sprint hasta que todos los BRIEFs están en VTT y el sprint está configurado para operar. Es la **Fase 1 del ciclo TL** antes de cualquier asignación.

---

## REGLA FUNDAMENTAL

> Todo lo que se registra en VTT viene de fuentes verificadas.  
> El TL NO inventa información — usa el documento de entrada y los documentos fuente que este referencia.  
> El ASSIGNMENT se genera AL MOMENTO de asignar — nunca durante la planificación.

---

## DATOS DEL SISTEMA (Memory Service)

```
BASE_URL  = http://77.42.88.106:3000
PROJECT_ID = d0fc276d-e764-4a83-96e9-d65f086ed803
PROJECT_KEY = MS
TL_UUID   = 92225290-6b6b-4c1f-a940-dcb4262507aa
SERVICE_KEY = $MEM_VTT_SERVICE_KEY
```

**Autenticación (requerida para todos los pasos):**
```bash
TOKEN=$(curl -s -X POST "$BASE/api/auth/service-token" \
  -H "Content-Type: application/json" \
  -d "{\"userId\":\"$TL_UUID\",\"serviceKey\":\"$SERVICE_KEY\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['token'])")
```

---

## MODELO DE DATOS VTT — Jerarquía

```
Project
  └── Release          (ej: MVP, R1)
        └── Sprint     (ej: S1, S2, S3)
              └── Delivery   (agrupador de tareas dentro del sprint, ej: DB-S2, BE-S2)
                    └── Task (unidad de trabajo, código MS-XXX)
```

**Relaciones y cómo se crean:**

| Relación | Endpoint | Método |
|----------|----------|--------|
| Sprint pertenece a Release | `POST /api/releases/{releaseId}/sprints` | Al crear el sprint |
| Delivery pertenece a Phase | `POST /api/deliveries` con `phaseId` | Al crear el delivery |
| Delivery vinculado a Sprint | `POST /api/deliveries` con `sprintId` incluido en el body | Al momento de crear — PATCH no existe, usar PUT para actualizar |
| Delivery reordenado | `PUT /api/deliveries/{deliveryId}` con `{"order": N}` | Cuando se necesita cambiar el orden |
| Task pertenece a Phase | `POST /api/phases/{phaseId}/tasks` | Al crear la tarea |
| Task vinculada a Delivery | `POST /api/deliveries/{deliveryId}/tasks/{taskId}` | Paso posterior a la creación |
| Task con dependencia | `POST /api/tasks/{taskId}/dependencies` con `{"dependsOnTaskId": "..."}` | Paso posterior |

> Los Deliveries deben incluir `sprintId` al crearse — no existe endpoint de actualización posterior.  
> Las Tasks se vinculan a su delivery en un paso posterior a la creación.

### Nomenclatura estándar de Deliveries

```
{SX}-{ROL}: {Descripción corta}
```

| Patrón | Ejemplo | Order |
|--------|---------|:-----:|
| `SX-SETUP: Setup Sprint X` | `S3-SETUP: Setup Sprint 3` | **1 — siempre primero** |
| `SX-DB: {descripción}` | `S2-DB: Seeds + Indexes + Migration Docs` | 2+ |
| `SX-BE: {descripción}` | `S3-BE: Endpoints + Integrations + Worker` | 2+ |
| `SX-FE: {descripción}` | `S3-FE: Foundation (Components + Hooks + State)` | 2+ |
| `SX-TL: {descripción}` | `S3-TL: Reviews + SLA Check` | penúltimo |
| `SX-REV: {descripción}` | `S3-REV: Validación + Cierre` | último |

> La descripción viene del HO — resume el contenido del delivery en ≤6 palabras.

---

## SECCIÓN 1 — DOCUMENTOS DE ENTRADA

Un sprint típicamente llega con **tres documentos** generados por el PJM:

| Documento | Cuándo | Qué contiene | Quién lo usa |
|-----------|--------|--------------|--------------|
| **HO / TE (Handoff o Technical Estimate)** | Al inicio — define el trabajo | Tareas, horas, dependencias, CAs, decisiones D-MEM-xx, pseudocódigo | TL — para generar BRIEFs |
| **SETUP_SX.md** | Al inicio — instrucciones de configuración VTT | Scripts Python listos, IDs constantes (RELEASE_ID, PHASE_ID, UUIDs agentes, prioridades), pasos numerados para crear sprint + deliveries + tareas + dependencias | TL — para ejecutar el setup en VTT |
| **CLOSURE_SX.md** | Al cierre — plantilla de cierre | Criterios por delivery (DB, BE), milestone verification, métricas finales, gate PM, proceso de firmas con scripts API, tabla de firmas TL + AR + PM | TL + AR — para cerrar el sprint |

> **El SETUP_SX ya tiene los scripts Python listos.** El TL los ejecuta directamente — no los re-inventa con curl.  
> **El CLOSURE_SX define exactamente qué verificar y cómo firmar.** El TL lo sigue al pie de la letra al cerrar.

> 🚨 **REGLA ANTI-DUPLICACIÓN:** El SETUP_SX.md del PJM y los PASOS 2-6 de este proceso hacen lo mismo. El TL ejecuta UNO de los dos — no ambos. Si ejecutó el script del PJM, los PASOS 2-6 son solo de verificación. Si no hay script del PJM, ejecutar los PASOS 2-6 de este proceso. Nunca crear tareas sin verificar primero si ya existen en VTT.

**Verificación antes de comenzar:**
```
[ ] HO/TE disponible en knowledge/handoffs/ o como attachment en VTT (versión ≥ 2.0)
[ ] SETUP_SX.md disponible (tiene RELEASE_ID y todos los UUIDs necesarios)
[ ] CLOSURE_SX.md disponible (define criterios de cierre del sprint)
```

> ⚠️ **El SETUP del sprint nuevo NO requiere que el sprint anterior esté cerrado.**  
> La configuración VTT (crear sprint, deliveries, tareas, dependencias) puede hacerse en paralelo al cierre del sprint anterior.  
> Lo que bloquea a los **agentes para trabajar** es la dependencia `SETUP-SX → CIERRE-S(X-1)` registrada en VTT — el TL puede configurar todo antes de que esa dependencia se resuelva.

Si el HO solo tiene títulos/horas (v1.0) → solicitar v2.0 al PJM antes de continuar.  
Si falta SETUP_SX o CLOSURE_SX → solicitar al PJM antes de continuar.

---

## SECCIÓN 2 — QUÉ DATOS NECESITA CADA ARTEFACTO

### Para CREAR TAREA EN VTT:
| Dato | Fuente |
|------|--------|
| ID, título, descripción | Documento de entrada |
| Horas, complejidad, categoría, prioridad | Documento de entrada |
| **taskTypeCode** | Documento de entrada o criterio TL — determina DoD/DoR automáticos |
| Agente asignado (UUID) | Documento de entrada + `Proyect_data.md` |
| Sprint, delivery, phase (UUIDs) | Documento de entrada + configuración VTT |
| Dependencias (task IDs) | Documento de entrada § Dependencias |

### Para el BRIEF (diseño original — inmutable):
| Dato | Fuente |
|------|--------|
| Qué producir (outputs, entregables) | Documento de entrada § Briefs |
| AC (Acceptance Criteria) CA-xx | Documento de entrada — CAs por tarea |
| DoD/DoR | VTT automático por taskTypeCode |
| Decisiones D-MEM-xx aplicables | Documento de entrada § Decisiones |
| Inputs obligatorios (dependencias técnicas) | Documento de entrada § Dependencias |
| Variables de entorno | Documento de entrada § Variables |
| Pseudocódigo / lógica | Documento de entrada v2.0 + docs fuente referenciados |
| Trackable Items vinculados | RF, RNF, ADR, BR del documento o de Analysis |
| Riesgos | Documento de entrada o criterio TL |

> El TL NO investiga qué documentos adicionales leer — § Referencias del documento lo dice.

### Para el ASSIGNMENT (AL MOMENTO de asignar — no antes):
| Dato | Fuente |
|------|--------|
| Estado actual del repo | Leer worktree del agente en disco |
| Archivos existentes vs. a crear | `ls src/`, `git log` reales |
| Dependencias de librerías | `package.json` real |
| Comandos del sistema | UUIDs, endpoints — `Proyect_data.md` |
| Script manifest verificado | `ls <worktree>/scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py` |

---

## SECCIÓN 3 — MODELO DINÁMICO POR TAREA

Cada tarea en VTT tiene un modelo dinámico completo. Responsabilidades y endpoints:

| Elemento | Quién lo configura | Cuándo | Automático o manual |
|----------|-------|--------|---------------------|
| **DoR** (Definition of Ready) | VTT | Al crear tarea | ✅ Automático por taskTypeCode |
| **DoD** (Definition of Done) | VTT | Al crear tarea | ✅ Automático por taskTypeCode |
| **AC** específicos de la tarea | TL | Al planificar (PASO 8) | Manual — endpoint API |
| **Trackable Items** vinculados | TL | Al planificar (PASO 8) | Manual — endpoint API |
| **Devlog entries** | Agente | Durante ejecución | Manual — agente via API |
| **Review Gate** | VTT | Automático al cambiar a in_review | ✅ Automático — bloquea si hay blockers |
| **Fulfillment de criterios** | Agente reporta / TL verifica | Al completar / revisar | Manual — cada criterio |
| **Document Impacts** | Agente | Al completar | Manual — agente via API |
| **Hardcode Check** | TL/Agente | Antes de in_review | Manual — en VTT UI |
| **Deferred Scope** | TL | Si se decide posponer scope | Manual — según necesidad |
| **Living Documents** | Agente | Al completar | Declarar en ASSIGNMENT §5 |

### Endpoints del TL en Planificación

**Crear AC específicos de la tarea:**
```bash
curl -s -X POST "$BASE/api/tasks/<TASK_ID>/criteria" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{
    "title": "CA-BE-01: ...",
    "description": "...",
    "criteriaTypeCode": "acceptance",
    "required": true
  }'
# Gotcha: campo es criteriaTypeCode — NO type. Endpoint /criteria — NO /acceptance-criteria
```

**Vincular Trackable Items existentes a la tarea:**
```bash
curl -s -X POST "$BASE/api/trackable-items/<TI_UUID>/tasks" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"taskId": "<TASK_ID>", "linkType": "implements"}'
# linkType: "implements" | "related_to"
```

**Crear TI nuevo (si no existe en VTT):**
```bash
curl -s -X POST "$BASE/api/projects/$PROJECT_ID/trackable-items" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{
    "code": "RF-XXX",
    "title": "Título del requerimiento",
    "description": "...",
    "typeCode": "functional_requirement",
    "statusCode": "ti_draft",
    "createdById": "'$TL_UUID'"
  }'
```

### Endpoints del TL en Cierre (Fase 3)

**Verificar Review Gate antes de aprobar:**
```bash
curl -s "$BASE/api/tasks/<TASK_ID>/review-gate" -H "Authorization: Bearer $TOKEN"
# Esperado: canProceedToReview: true, blockers: []
```

**Verificar criterios — todos deben estar met:**
```bash
curl -s "$BASE/api/tasks/<TASK_ID>/criteria" -H "Authorization: Bearer $TOKEN" | \
  python3 -c "import sys,json; [print(c['title'], c['status']) for c in json.load(sys.stdin)['data']]"
```

**Revisar devlog entries del agente:**
```bash
curl -s "$BASE/api/tasks/<TASK_ID>/devlog" -H "Authorization: Bearer $TOKEN" | \
  python3 -c "import sys,json; [print(e['severity'], e['title']) for e in json.load(sys.stdin)['data']]"
```

### Lo que el Agente configura (referencia para el ASSIGNMENT)

El ASSIGNMENT debe indicar al agente qué debe hacer con el modelo dinámico:
- **§3 AC**: reportar fulfillment por cada CA con evidencia (PR#, línea de código, output)
- **§5 Living Documents**: declarar documentos impactados (BRIEF, LOGIC.md, devlog, API spec)
- **§7 Hardcode Check**: ejecutar antes de mover a in_review
- **§8 Tech debts**: listar items detectados durante ejecución para que TL los cree en VTT

---

## PASO 0 — Consultar VTT y obtener CONTEXTO del sprint anterior

Antes de ejecutar cualquier script, el TL obtiene el CONTEXTO_S(X-1) desde la tarea SETUP del sprint anterior en VTT — es la fuente oficial de IDs cross-sprint:

```python
# 1. Obtener attachments de la tarea SETUP-S(X-1)
req = urllib.request.Request(
    f'{BASE_URL}/api/tasks/{SETUP_S_ANTERIOR}/attachments',
    headers=HEADERS)
attachments = json.loads(urllib.request.urlopen(req).read())['data']
contexto = next((a for a in attachments if a.get('fileType') == 'brief' and 'CONTEXTO' in (a.get('originalName') or '')), None)
print("CONTEXTO:", contexto['fileName'] if contexto else "NO ENCONTRADO")

# 2. Descargar y leer el CONTEXTO_S(X-1).md
# Usar los IDs que provee: RELEASE_ID, SPRINT_S(X-1), PHASE_DEV,
# CIERRE_S(X-1), última tarea operativa, etc.
```

> **Regla:** El agente NUNCA asume IDs cross-sprint — los obtiene del attachment `fileType=brief` (nombre: `CONTEXTO_S(X-1).md`) de la tarea SETUP del sprint anterior. Si no existe → detener y notificar al TL.  
> **Gotcha:** `fileType=context` no existe en VTT. El CONTEXTO se sube y se busca como `fileType=brief`.

A continuación, verificar qué sprints existen en VTT:

```python
# Autenticar
req = urllib.request.Request(f'{BASE_URL}/api/auth/service-token',
    data=json.dumps({'userId': TL, 'serviceKey': SERVICE_KEY}).encode(),
    headers={'Content-Type': 'application/json'}, method='POST')
TOKEN = json.loads(urllib.request.urlopen(req).read())['data']['token']
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

# Consultar sprints existentes
req = urllib.request.Request(f'{BASE_URL}/api/releases/{RELEASE_ID}/sprints', headers=HEADERS)
sprints = json.loads(urllib.request.urlopen(req).read())['data']
for s in sprints:
    print(s['id'], '|', s['name'], '|', s.get('status',{}).get('code','?'))
```

**Mapeo HO → sprint real en VTT:**

El PJM genera el HO con nombres genéricos (S1, S2, S3...) sin saber cuántos sprints existen en VTT. El TL debe resolver el mapeo antes de cualquier acción:

```
HO dice "S4"  →  consultar VTT  →  identificar el sprint_planned vacío que corresponde  →  ese es el sprint real
```

| Situación | Acción |
|-----------|--------|
| El sprint del HO **no existe en VTT** | Crearlo en PASO 2 con el número consecutivo real de VTT |
| El sprint **existe por nombre y está vacío** | Tomar su ID, saltar PASO 2, continuar desde PASO 3 |
| El sprint **existe y ya tiene tareas** | NO recrear — verificar qué falta y completar solo eso |
| Hay sprints duplicados o "implementacion" | NO usar esos — identificar el sprint_planned correcto por nombre/contenido del HO |
| Estado inesperado o ambiguo | Reportar al PJM antes de continuar |

> ⚠️ **El número del HO NO es el número de VTT.** El TL identifica el sprint correcto por nombre y contenido — no por número. El nombre en VTT debe coincidir con el tema del HO.

> ⚠️ **TEMA PENDIENTE CON PJM — Consecutivo de sprints:** No está definido si los sprints son globales para todo el proyecto (un solo consecutivo) o se resetean por fase (Deploy S1-S5, Test S1-S3, etc.). Hasta que el PJM lo defina, el TL consulta VTT, identifica el sprint por nombre/tema, y si hay ambigüedad **detiene y consulta al PJM antes de crear nada**.

---

## PASO 1 — Leer el HO y evaluar fuentes

### 1.1 Extraer del HO:

| Qué extraer | Dónde está |
|-------------|------------|
| Lista de tareas: IDs, horas, complejidad, rol | Tabla de tareas |
| Deliveries del sprint y su agrupación | § Estructura / Deliveries |
| Dependencias entre tareas | § Dependencias |
| Variables de entorno | § Variables de Entorno |
| Decisiones D-MEM-xx | § Arquitectura / Decisiones |
| Documentos fuente a leer | § Referencias |
| CAs por tarea | § Briefs para agentes |
| Trackable Items vinculables | § Requerimientos |

### 1.2 Evaluar si el HO v2.0 es suficiente para generar BRIEFs:

**Suficiente** — tiene por tarea: pseudocódigo/lógica, valores exactos, CAs verificables, decisiones D-MEM-xx.

**Insuficiente** — solo títulos/horas → solicitar v2.0 al PJM antes de continuar.

**Necesita docs adicionales** — § Referencias indica exactamente cuáles. El TL NO investiga por su cuenta.

| Tipo de tarea | Docs fuente típicos (si § Referencias los lista) |
|---------------|--------------------------------------------------|
| DB | `3B.3.2_schema_prisma.md`, `3B.3.4_index_strategy.md`, `3B.3.7_seed_plan.md` |
| BE | `3B.4.2_endpoints_list.md`, `3B.4.5_error_codes.md`, `3B.1.4_component_diagram_c4_l3.md` |
| FE | Wireframes aprobados, `3B.4.2_endpoints_list.md`, Design System |

---

## PASO 2 — Crear el Sprint (si no existe)

```python
body = {
    "number": X,
    "name": "SX — [Nombre del HO]",
    "goal": "[Goal del HO]",
    "startDate": "YYYY-MM-DDTHH:MM:SSZ",
    "endDate": "YYYY-MM-DDTHH:MM:SSZ"
}
req = urllib.request.Request(f'{BASE_URL}/api/releases/{RELEASE_ID}/sprints',
    data=json.dumps(body).encode(), headers=HEADERS, method='POST')
SPRINT_SX_ID = json.loads(urllib.request.urlopen(req).read())['data']['id']
print(f"SPRINT_SX_ID: {SPRINT_SX_ID}")
```

> Si el sprint ya existe → tomar su ID del PASO 0 y continuar.

---

## PASO 3 — Crear Deliveries

El **primer delivery siempre es `SX-SETUP`**. Los demás los define el HO. El `sprintId` va en el body al crear — no existe endpoint de actualización posterior.

```python
def create_delivery(name, order):
    body = {
        "phaseId": PHASE_DEV,
        "name": name,
        "order": order,
        "sprintId": SPRINT_SX_ID,  # OBLIGATORIO al crear
        "createdBy": TL
    }
    req = urllib.request.Request(f'{BASE_URL}/api/deliveries',
        data=json.dumps(body).encode(), headers=HEADERS, method='POST')
    did = json.loads(urllib.request.urlopen(req).read())['data']['id']
    print(f"{name}: {did}")
    return did

DEL_SETUP_SX = create_delivery("SX-SETUP: Setup Sprint X", 1)  # siempre order=1
DEL_BE_SX    = create_delivery("SX-BE: ...", 2)                 # según HO
DEL_FE_SX    = create_delivery("SX-FE: ...", 3)
DEL_TL_SX    = create_delivery("SX-TL: Reviews + ...", 4)
DEL_REV_SX   = create_delivery("SX-REV: Validación + Cierre", 5)  # siempre último
```

> **Gotcha:** `PATCH /api/deliveries/{id}` devuelve 404. Para reordenar usar `PUT /api/deliveries/{id}` con `{"order": N}`.

> **REGLA DE NUMERACIÓN:** Si el SETUP_SX del PJM asigna `order=1` a un delivery que no es SETUP (ej: `DEL_FE_S4 = create_delivery("FE-S4: ...", 1)`), **ignorarlo**. El TL siempre crea `SX-SETUP` con `order=1` y renumera los demás deliveries del HO a partir de `2`. La numeración del PJM es orientativa — la regla del proceso es la que aplica.

---

## PASO 4 — Crear tarea SETUP-SX

> 🚨 **REGLA CRÍTICA:** Inmediatamente después de crear la tarea SETUP-SX, moverla a `in_progress`. No continuar con PASO 5 hasta que el status sea `in_progress`. Esto registra el inicio formal del trabajo del TL en VTT.

> ⚠️ **VERIFICAR ANTES DE EJECUTAR:** Si el SETUP_SX.md del PJM ya incluía un script para crear la tarea SETUP-SX y lo ejecutaste, esta tarea YA EXISTE. Buscarla en VTT antes de crearla:
> ```python
> # Verificar si SETUP-SX ya existe
> req = urllib.request.Request(f'{BASE_URL}/api/phases/{PHASE_DEV}/tasks', headers=HEADERS)
> tasks = json.loads(urllib.request.urlopen(req).read())['data']
> existing = [t for t in tasks if 'SETUP' in t.get('title','') and f'S{X}' in t.get('title','')]
> if existing:
>     print("SETUP-SX ya existe:", existing[0]['id'], "— NO crear otra")
>     SETUP_SX = existing[0]['id']
> # Solo crear si no existe
> ```
> Crear la tarea de setup duplicada bloquea el proyecto — dos tareas con el mismo propósito generan confusión en dependencias.

```python
body = {
    "title": "SETUP-SX: Setup Sprint X — [Nombre]",
    "description": "Configuración del Sprint SX en VTT. Rol: TL.",
    "assignedToId": TL,
    "estimatedHours": 1,
    "priorityId": PRI_MED,
    "complexity": "LOW",
    "category": "management"
}
req = urllib.request.Request(f'{BASE_URL}/api/phases/{PHASE_DEV}/tasks',
    data=json.dumps(body).encode(), headers=HEADERS, method='POST')
SETUP_SX = json.loads(urllib.request.urlopen(req).read())['data']['taskId']

# Dependencia: solo aplica para S2 en adelante — SETUP-S1 no tiene dependencia previa
if SPRINT_NUMBER > 1:
    body_dep = {"dependsOnTaskId": SETUP_S1}  # SETUP_S1 viene del CONTEXTO_S1.md
    req_dep = urllib.request.Request(f'{BASE_URL}/api/tasks/{SETUP_SX}/dependencies',
        data=json.dumps(body_dep).encode(), headers=HEADERS, method='POST')
    urllib.request.urlopen(req_dep)
else:
    print("SETUP-S1: sin dependencia previa — es el primer setup del proyecto")

# IMPORTANTE: mover SETUP-SX a in_progress INMEDIATAMENTE después de crearla
# Razón: el tiempo de desarrollo debe empezar a contar desde que el TL inicia el trabajo
body_status = {"statusId": "2a76888a-e595-4cfc-ac4c-a3ae5087ef56", "changedBy": TL,
               "reason": "TL inicia configuración del sprint"}
req_status = urllib.request.Request(f'{BASE_URL}/api/tasks/{SETUP_SX}/status',
    data=json.dumps(body_status).encode(), headers=HEADERS, method='PATCH')
urllib.request.urlopen(req_status)
print(f"SETUP_SX {SETUP_SX} → in_progress")
```

**Cadena de dependencias del sprint:**
```
SETUP-SX              → depende de → SETUP-S1                    ← anchor fijo: primer setup del proyecto
PRIMERA_TAREA_OP_SX   → depende de → SETUP-SX                    ← sprint configurado antes de arrancar
PRIMERA_TAREA_OP_SX   → depende de → ULTIMA_TAREA_OP_S(X-1)      ← sprint anterior terminado antes de arrancar
Demás tareas sin dep  → depende de → SETUP-SX                    ← ningún agente arranca antes
Tareas con dep téc.   → depende de → su tarea bloqueante técnica  ← cadena técnica la controla
```

> **Regla SETUP-SX:** `SETUP-S1` no tiene dependencia previa — es el anchor fijo del proyecto. `SETUP-S2` en adelante dependen de `SETUP-S1`. ID de SETUP-S1 viene del `CONTEXTO_S1.md`.

> **Regla primera tarea operativa:** La primera tarea operativa del sprint (la de menor orden según el HO) tiene **dos dependencias**: `SETUP-SX` (para garantizar que el sprint esté configurado) y la última tarea operativa del sprint anterior (para garantizar que los agentes del sprint previo terminaron antes de arrancar el nuevo). La "última tarea operativa" del sprint anterior viene del `CONTEXTO_S(X-1).md` — NO es el CIERRE ni el APR.

---

## PASO 5 — Crear tareas operativas (todas las del HO — DB, BE, FE, DevOps, QA, etc.)

> ⚠️ **VERIFICAR ANTES DE EJECUTAR:** Si el SETUP_SX.md del PJM ya creó tareas operativas, NO recrearlas. Consultar primero las tareas existentes en la phase y cruzar contra la lista del HO. Solo crear las que faltan.

Por cada tarea del HO:

```python
body = {
    "title": "[4.X.Y] Nombre de la tarea",
    "description": "...",
    "assignedToId": UUID_AGENTE,   # gotcha: NO assigneeId
    "estimatedHours": N,
    "priorityId": PRI_HIGH,        # o PRI_MED
    "complexity": "HIGH",          # LOW | MEDIUM | HIGH
    "category": "development"
}
req = urllib.request.Request(f'{BASE_URL}/api/phases/{PHASE_DEV}/tasks',
    data=json.dumps(body).encode(), headers=HEADERS, method='POST')
TASK_ID = json.loads(urllib.request.urlopen(req).read())['data']['taskId']
```

> **Gotcha:** Campo es `assignedToId` — NO `assigneeId`. El backend ignora `assigneeId` silenciosamente.

**UUIDs de status:**
| Status | UUID |
|--------|------|
| task_pending | `335fd9c6-f0d6-4966-a6ea-f518c78bc422` |
| task_in_progress | `2a76888a-e595-4cfc-ac4c-a3ae5087ef56` |
| task_in_review | `1ec975a5-7581-4a1a-ab8f-51b1a7ef868d` |
| task_completed | `aa5ceb90-5209-42a2-b874-a8cbee597a97` |

---

## PASO 6 — Crear tareas de cierre

Las tareas de cierre son fijas en todo sprint: TL-REV, AR-SX, CIERRE-SX, APR-SX.

```python
# TL Review
body = {"title": "TL-SX-REV: Reviews + Coordinación Sprint X", "assignedToId": TL,
        "estimatedHours": 4, "priorityId": PRI_MED, "complexity": "MEDIUM", "category": "review"}
req = urllib.request.Request(f'{BASE_URL}/api/phases/{PHASE_DEV}/tasks',
    data=json.dumps(body).encode(), headers=HEADERS, method='POST')
TL_SX_REV = json.loads(urllib.request.urlopen(req).read())['data']['taskId']

# AR Audit
body = {"title": "AR-SX: Integration Audit Sprint X", "assignedToId": AR,
        "estimatedHours": 3, "priorityId": PRI_MED, "complexity": "MEDIUM", "category": "review"}
req = urllib.request.Request(f'{BASE_URL}/api/phases/{PHASE_DEV}/tasks',
    data=json.dumps(body).encode(), headers=HEADERS, method='POST')
AR_SX = json.loads(urllib.request.urlopen(req).read())['data']['taskId']

# CIERRE-SX
body = {"title": "CIERRE-SX: Cierre Sprint X — [Nombre]", "assignedToId": TL,
        "estimatedHours": 2, "priorityId": PRI_HIGH, "complexity": "MEDIUM", "category": "review"}
req = urllib.request.Request(f'{BASE_URL}/api/phases/{PHASE_DEV}/tasks',
    data=json.dumps(body).encode(), headers=HEADERS, method='POST')
CIERRE_SX = json.loads(urllib.request.urlopen(req).read())['data']['taskId']

# APR-SX
body = {"title": "APR-SX: Aprobación final Sprint X", "assignedToId": PM_ID,
        "estimatedHours": 1, "priorityId": PRI_HIGH, "complexity": "LOW", "category": "review"}
req = urllib.request.Request(f'{BASE_URL}/api/phases/{PHASE_DEV}/tasks',
    data=json.dumps(body).encode(), headers=HEADERS, method='POST')
APR_SX = json.loads(urllib.request.urlopen(req).read())['data']['taskId']
```

---

## PASO 7 — Asociar tareas a sus deliveries

```python
def assign_to_delivery(delivery_id, task_id):
    body = {"assignedBy": TL}
    req = urllib.request.Request(
        f'{BASE_URL}/api/deliveries/{delivery_id}/tasks/{task_id}',
        data=json.dumps(body).encode(), headers=HEADERS, method='POST')
    urllib.request.urlopen(req)

# SETUP en DEL_SETUP_SX
assign_to_delivery(DEL_SETUP_SX, SETUP_SX)

# Tareas operativas en sus deliveries según el HO
assign_to_delivery(DEL_BE_SX, T_BE_1)
# ...

# Tareas de cierre en DEL_TL_SX y DEL_REV_SX
assign_to_delivery(DEL_TL_SX, TL_SX_REV)
assign_to_delivery(DEL_REV_SX, AR_SX)
assign_to_delivery(DEL_REV_SX, CIERRE_SX)
assign_to_delivery(DEL_REV_SX, APR_SX)
```

---

## PASO 8 — Registrar dependencias entre tareas

```python
def add_dep(task_id, depends_on_id):
    body = {"dependsOnTaskId": depends_on_id}
    req = urllib.request.Request(f'{BASE_URL}/api/tasks/{task_id}/dependencies',
        data=json.dumps(body).encode(), headers=HEADERS, method='POST')
    urllib.request.urlopen(req)

# Gate de proyecto: SETUP-SX siempre depende de SETUP-S1 (anchor fijo)
add_dep(SETUP_SX, SETUP_S1)

# Primera tarea operativa: dos dependencias
# 1. SETUP-SX → el sprint esté configurado antes de arrancar
# 2. Última tarea operativa del sprint anterior → agentes del sprint previo terminaron
add_dep(PRIMERA_TAREA_OP_SX, SETUP_SX)
add_dep(PRIMERA_TAREA_OP_SX, ULTIMA_TAREA_OP_S_ANTERIOR)  # viene del CONTEXTO_S(X-1).md

# Demás tareas sin dep técnica → SETUP-SX
add_dep(T_SIN_DEP, SETUP_SX)

# Tareas con dep técnica → su tarea bloqueante (del HO § Dependencias)
add_dep(T_CON_DEP, T_BLOQUEANTE)

# Cierre chain
add_dep(TL_SX_REV, ULTIMA_TAREA_OPERATIVA)
add_dep(AR_SX, TL_SX_REV)
add_dep(CIERRE_SX, AR_SX)
add_dep(APR_SX, CIERRE_SX)
```

---

## PASO 9 — Generar BRIEFs

**Template:** `00-agent-setup/05.Templates/05.Proyecto/02.Genericos/TEMPLATE_BRIEF_LARGE.md`  
**Ubicación:** `knowledge/agent-tasks/briefs/BRIEF_[TASK_ID]_[nombre-corto].md`

| Sección | Fuente |
|---------|--------|
| Header (tarea, horas, complejidad, rol) | HO |
| Objetivo + resultado esperado | HO § Briefs |
| Contexto (situación actual → deseada) | HO + docs fuente |
| Dependencias | HO § Dependencias |
| Archivos a crear (rutas exactas + pseudocódigo) | HO v2.0 + docs fuente |
| AC / CAs verificables con comandos | HO — CAs por tarea |
| Cómo Probar | TL genera desde los CAs |
| Referencias (rutas exactas) | HO § Referencias |
| Notas (D-MEM-xx, qué evitar, desbloquea) | HO § Decisiones |

**Regla de calidad:**
- ✅ El agente puede ejecutar SIN consultar al TL
- ✅ Rutas de archivos exactas, CAs verificables con comandos
- ❌ No inventar — todo viene del HO o sus fuentes referenciadas

---

## PASO 10 — Subir BRIEFs a VTT + crear AC

```python
# Subir BRIEF
import subprocess
subprocess.run(['curl', '-s', '-X', 'POST', f'{BASE_URL}/api/tasks/{TASK_ID}/attachments',
    '-H', f'Authorization: Bearer {TOKEN}',
    '-F', f'file=@knowledge/agent-tasks/briefs/BRIEF_{TASK_ID}_nombre.md',
    '-F', 'fileType=brief', '-F', f'uploadedById={TL}'])

# Crear AC por cada CA del BRIEF
body = {
    "title": "CA-BE-01: ...",
    "description": "...",
    "criteriaTypeCode": "acceptance",  # NO "type"
    "required": True
}
req = urllib.request.Request(f'{BASE_URL}/api/tasks/{TASK_ID}/criteria',
    data=json.dumps(body).encode(), headers=HEADERS, method='POST')
urllib.request.urlopen(req)
```

---

## PASO 10.1 — Vincular Trackable Items a cada tarea (OBLIGATORIO)

> 🚨 **El HO/BRIEF NO contiene la lista completa de Trackable Items que aplican a cada tarea.** El TL debe consultar VTT, leer todos los TIs del proyecto, y mapearlos a cada tarea por dominio. Sin este paso las tareas quedan sin trazabilidad a requerimientos, ADRs, BRs, US, UC.

### 10.1.1 Obtener TODOS los Trackable Items del proyecto

```python
req = urllib.request.Request(
    f'{BASE_URL}/api/projects/{PROJECT_ID}/trackable-items?limit=500',
    headers=HEADERS)
all_tis = json.loads(urllib.request.urlopen(req).read())['data']
print(f"Total TIs en el proyecto: {len(all_tis)}")
# Tipos esperados: rf, rnf, user_story, adr, business_rule, use_case,
#                  assumption, tech_debt, constraint
```

> **No hay paginación** — el endpoint devuelve todos los TIs en una sola llamada. Si la respuesta supera 500, aumentar el limit.

### 10.1.2 Mapeo TI → Tarea por dominio

Para cada tarea operativa, el TL revisa los 223 TIs y selecciona los relevantes según el dominio de la tarea:

| Dominio de tarea | Tipos de TI a considerar |
|------------------|--------------------------|
| **Endpoints / API** | RF (funcionales), RNF (perf, security), BR, US, UC, ADR-SA, NFR-PERF, NFR-SEC |
| **Workers / Cleanup** | RF cleanup, BR (frecuencias), US del worker, NFR-AVAIL, NFR-PERF, ADR del job |
| **Integrations / Webhooks** | RF (imports), BR (canales), US (imports), UC (importar), ADR-SA, NFR-SEC |
| **Components FE** | ADR-UX (pantallas), CON-UX (límites), NFR-USE, DEF-UX (deferidos) |
| **Hooks / API Client FE** | RF (datos que consume), US (qué muestra), NFR-PERF, ADR-SA-006 |
| **State / Layouts** | ADR-UX (estructura), CON-UX, NFR-USE |
| **Styles / Types** | ADR-UX (visual), CON-UX (restricciones), RNF (tipos), NFR-SEC |

**Criterio de inclusión:** un TI se vincula si la tarea lo **implementa**, **cubre** o **valida**. Si solo lo referencia indirectamente, no vincular.

### 10.1.3 Vincular en VTT

```python
def link_ti_to_task(ti_uuid, task_id):
    body = {"taskId": task_id, "linkType": "implements"}
    req = urllib.request.Request(
        f'{BASE_URL}/api/trackable-items/{ti_uuid}/tasks',
        data=json.dumps(body).encode(), headers=HEADERS, method='POST')
    try:
        urllib.request.urlopen(req)
        return True
    except urllib.error.HTTPError as e:
        if e.code == 409:  # ya vinculado
            return None
        raise

# Por cada tarea, vincular los TIs mapeados
for task_id, ti_codes in mapping.items():
    linked = 0
    for code in ti_codes:
        ti = next((t for t in all_tis if t['code'] == code), None)
        if ti and link_ti_to_task(ti['id'], task_id):
            linked += 1
    print(f"{task_id}: {linked} TIs vinculados")
```

### 10.1.4 Reglas

- **No saturar:** una tarea no debe tener todos los TIs del dominio. Vincular solo los que realmente implementa (criterio del TL).
- **linkType `implements`** para tareas que producen el TI; `related_to` para referencias indirectas.
- **Si ya está vinculado** (HTTP 409) → ignorar y continuar.
- **Reportar al final** cuántos vínculos se crearon por tarea para verificación.

---

## PASO 11 — Generar CONTEXTO_SX.md y subirlo a la tarea SETUP-SX

**Ubicación local:** `knowledge/agent-tasks/CONTEXTO_SX.md` ← path estándar, generado por el agente TL  
**Obligatorio para cerrar SETUP-SX** — sin él la tarea no se completa.

Una vez generado, subirlo como attachment a la tarea SETUP-SX en VTT:

```python
subprocess.run(['curl', '-s', '-X', 'POST',
    f'{BASE_URL}/api/tasks/{SETUP_SX}/attachments',
    '-H', f'Authorization: Bearer {TOKEN}',
    '-F', f'file=@knowledge/agent-tasks/CONTEXTO_SX.md',
    '-F', 'fileType=brief',
    '-F', f'uploadedById={TL}'])
```

> **Regla:** El CONTEXTO_SX siempre vive adjunto a su tarea SETUP-SX en VTT. Es la fuente oficial que el siguiente sprint consultará — no el worktree local.

```markdown
# CONTEXTO: Sprint SX — [Nombre]

## 1. Estructura VTT
| Entidad   | ID |
|-----------|----|
| Release   | `UUID` |
| Sprint SX | `UUID` |
| Phase Dev | `UUID` |

## 2. Tareas cross-sprint para S(X+1)
| Código VTT | Título | Estado |
|------------|--------|--------|
| `MS-XXX`   | CIERRE-SX | ⬜ |
| `MS-XXX`   | APR-SX | ⬜ |
| `MS-XXX`   | [tarea técnica que S(X+1) necesita] | ⬜ |

## 3. Todas las tareas SX
| Código VTT | Título | Rol | Horas | Delivery |
|------------|--------|:---:|:-----:|----------|
| `MS-XXX`   | ... | BE | Xh | SX-BE |

## 4. Constantes para SETUP_S(X+1)
RELEASE_ID  = "UUID"
SPRINT_SX   = "UUID"
PHASE_DEV   = "UUID"
CIERRE_SX   = "MS-XXX"
APR_SX      = "MS-XXX"
T_XXXX_SX   = "MS-XXX"   # tareas técnicas que S(X+1) puede necesitar
```

> IDs consultados de VTT — no inventados.

---

## PASO 11.1 — Cerrar tarea SETUP-SX

Una vez que el CONTEXTO_SX.md está subido como attachment, el TL cierra la tarea en tres pasos:

```python
# 1. Subir devlog (requerido por Review Gate)
subprocess.run(['curl', '-s', '-X', 'POST',
    f'{BASE_URL}/api/tasks/{SETUP_SX}/attachments',
    '-H', f'Authorization: Bearer {TOKEN}',
    '-F', f'file=@knowledge/development-log/YYYY-MM-DD_{SETUP_SX}_setup-sX.md',
    '-F', 'fileType=devlog', '-F', f'uploadedById={TL}'])

# 2. Subir code_logic (requerido por Review Gate)
subprocess.run(['curl', '-s', '-X', 'POST',
    f'{BASE_URL}/api/tasks/{SETUP_SX}/attachments',
    '-H', f'Authorization: Bearer {TOKEN}',
    '-F', f'file=@knowledge/code-logic/agent-tasks/SETUP_SX.LOGIC.md',
    '-F', 'fileType=code_logic', '-F', f'uploadedById={TL}'])

# 3. Subir comentario/reporte (requerido por Review Gate)
body_comment = {"userId": TL, "message": "SETUP-SX completado. [resumen de lo ejecutado]"}
req = urllib.request.Request(f'{BASE_URL}/api/tasks/{SETUP_SX}/comments',
    data=json.dumps(body_comment).encode(), headers=HEADERS, method='POST')
urllib.request.urlopen(req)

# 4. Mover a in_review
body_status = {"statusId": "1ec975a5-7581-4a1a-ab8f-51b1a7ef868d", "changedBy": TL,
               "reason": "Entregables completos"}
req = urllib.request.Request(f'{BASE_URL}/api/tasks/{SETUP_SX}/status',
    data=json.dumps(body_status).encode(), headers=HEADERS, method='PATCH')
urllib.request.urlopen(req)

# 5. Mover a task_completed (desbloquea las tareas dependientes)
body_status = {"statusId": "aa5ceb90-5209-42a2-b874-a8cbee597a97", "changedBy": TL,
               "reason": "SETUP-SX completo — sprint listo para operar"}
req = urllib.request.Request(f'{BASE_URL}/api/tasks/{SETUP_SX}/status',
    data=json.dumps(body_status).encode(), headers=HEADERS, method='PATCH')
urllib.request.urlopen(req)
print(f"SETUP_SX {SETUP_SX} → task_completed. Tareas del sprint desbloqueadas.")
```

> **Por qué este orden:** `in_review` requiere devlog + code_logic + comentario subidos. Sin esos tres el Review Gate bloquea la transición.  
> `task_completed` desde `in_review` desbloquea automáticamente todas las tareas que dependen de SETUP-SX.

---

## PASO 12 — Checklist final antes de pasar a ASSIGNMENT

```
[ ] Sprint existe en VTT con sprintId correcto en todos los deliveries
[ ] Delivery SX-SETUP creado con order=1
[ ] Tarea SETUP-SX creada, en DEL_SETUP_SX, con dep → SETUP-S1 (anchor fijo del proyecto)
[ ] SETUP-SX movida a in_progress inmediatamente al crearla (PASO 4)
[ ] Tareas operativas creadas y vinculadas a sus deliveries
[ ] Tareas de cierre creadas (TL-REV, AR-SX, CIERRE-SX, APR-SX) en DEL_TL + DEL_REV
[ ] Todas las dependencias configuradas en VTT
[ ] Primera tarea operativa tiene dep → SETUP-SX + última tarea op. del sprint anterior
[ ] BRIEF generado por cada tarea operativa
[ ] AC registrados en VTT por cada tarea
[ ] **Trackable Items vinculados** — TL consultó los 223 TIs del proyecto y mapeó los relevantes a cada tarea (PASO 10.1), no solo los que venían en el HO
[ ] BRIEFs subidos como attachments (fileType=brief)
[ ] CONTEXTO_SX.md generado con IDs reales de VTT
[ ] CONTEXTO_SX.md subido como attachment (fileType=brief) a la tarea SETUP-SX en VTT
[ ] Devlog subido a SETUP-SX (fileType=devlog)
[ ] Code Logic subido a SETUP-SX (fileType=code_logic)
[ ] Comentario/reporte subido a SETUP-SX
[ ] SETUP-SX movida a in_review → task_completed (desbloquea tareas del sprint)
[ ] Script manifest verificado en worktrees de cada agente
```

Solo después de este checklist → pasar a ASSIGNMENT cuando el TL decida activar una tarea.

---

## SECCIÓN 4 — AL MOMENTO DE ASIGNAR (Fase 2)

### Pre-requisito: verificar script manifest

```bash
ls <worktree>/scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py
# Si NO existe:
mkdir -p <worktree>/scripts/manifest/
cp $VTT_SETUP/02.normativa/04.Scripts/manifest/VTT.SCRIPT-MAN-001_gen_task_manifest.py \
   <worktree>/scripts/manifest/
```

### Generar ASSIGNMENT con estado real del repo:

Leer el worktree → verificar qué existe → generar `knowledge/agent-tasks/assignments/ASSIGNMENT_<TASK_ID>_nombre.md` → subir:

```bash
curl -s -X POST "$BASE/api/tasks/<TASK_ID>/attachments" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@knowledge/agent-tasks/assignments/ASSIGNMENT_<TASK_ID>_nombre.md" \
  -F "fileType=assignment" \
  -F "uploadedById=$TL_UUID"
```

### Cambiar status a in_progress y notificar al agente:

```bash
# Status → in_progress
curl -s -X PATCH "$BASE/api/tasks/<TASK_ID>/status" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{
    "statusId": "2a76888a-e595-4cfc-ac4c-a3ae5087ef56",
    "changedBy": "'$TL_UUID'",
    "reason": "Asignando a <agente> — ASSIGNMENT subido"
  }'

# Generar mensaje de activación
python scripts/gen_mensaje.py <TASK_ID> --post
```

---

## SECCIÓN 5 — CIERRE DEL SPRINT (usando CLOSURE_SX)

El CLOSURE_SX es la guía oficial de cierre. El TL lo sigue en orden:

### Estructura del CLOSURE_SX

| Sección | Contenido | Quién completa |
|---------|-----------|----------------|
| §1 Resumen | Métricas del sprint (tareas, horas, deliveries) | Referencia |
| §2 Verificación de deliverables | Criterios DB + BE con evidencia | TL verifica |
| §3 Firma TL — Code Review | Checklist PRs mergeados, LOGIC.md, N+1, etc. + script API firma | TL completa y firma |
| §4 Firma AR — Integration Audit | Checklist diseño + decisiones + integridad + script API firma | AR completa y firma |
| §5 Milestone verification | Criterios del milestone del sprint (M2, M3, etc.) | TL + AR verifican |
| §6 Métricas finales | Horas estimadas vs reales, PRs, LOGIC.md, issues | TL llena |
| §7 Gate final PM | Checklist completo para que PM apruebe APR-SX | TL prepara |
| §8 Proceso de firmas | Secuencia: TL → AR → TL verifica → PM aprueba | Guía de pasos |
| §9 Firmas físicas | Tabla con firma + fecha de cada rol | Todos |

### Proceso de cierre paso a paso

```
1. TL completa §2 + §3 → ejecuta script API de firma stage development
2. TL asigna CLOSURE_SX a AR
3. AR completa §4 → ejecuta script API de firma stage integration
4. AR devuelve a TL
5. TL verifica 2 firmas → completa §5 métricas → mueve CIERRE-SX a task_completed
6. PM revisa §7 gate → mueve APR-SX a task_completed → Sprint cerrado
```

### Scripts de firma (del CLOSURE_SX — ejecutar tal cual)

```python
# TL firma stage development
body = {"userId": TL, "role": "tech_lead", "comment": "Code Review SX completado. [resumen]"}
req = urllib.request.Request(
    f'{BASE_URL}/api/sprints/{SPRINT_SX_ID}/stages/development/sign',
    data=json.dumps(body).encode(), headers=HEADERS, method='POST')
urllib.request.urlopen(req)

# AR firma stage integration
body = {"userId": AR, "role": "architect", "comment": "Integration Audit SX completado. [resumen]"}
req = urllib.request.Request(
    f'{BASE_URL}/api/sprints/{SPRINT_SX_ID}/stages/integration/sign',
    data=json.dumps(body).encode(), headers=HEADERS, method='POST')
urllib.request.urlopen(req)

# PM aprueba APR-SX (cierre final)
body = {"statusId": "aa5ceb90-5209-42a2-b874-a8cbee597a97"}  # task_completed
req = urllib.request.Request(
    f'{BASE_URL}/api/tasks/{APR_SX}/status',
    data=json.dumps(body).encode(), headers=HEADERS, method='PATCH')
urllib.request.urlopen(req)
```

> Los IDs (`SPRINT_SX_ID`, `APR_SX`) vienen del CONTEXTO_SX.md generado en el SETUP.  
> El CLOSURE define qué roles firman en cada sprint — S2 solo TL + AR (sin QA ni DL).

---

## DIFERENCIA ENTRE BRIEF Y ASSIGNMENT

| | BRIEF | ASSIGNMENT |
|--|-------|------------|
| **Cuándo** | Al planificar el sprint | Al momento de asignar (no antes) |
| **Fuente** | Documento de entrada + docs de diseño | Código real verificado en worktree |
| **Inmutabilidad** | Inmutable tras aprobación | Actualizable si el código cambia |
| **Propósito** | Diseño original de la tarea | Instrucciones exactas verificadas al agente |
| **Sube como** | `fileType=brief` | `fileType=assignment` |

---

## LECCIONES APRENDIDAS

| Lección | Descripción |
|---------|-------------|
| **Input no siempre es un HO** | Puede ser TE u otro. Identificar el tipo antes de procesar. |
| **taskTypeCode determina DoD/DoR** | Asignarlo mal deja la tarea sin criterios automáticos. |
| **sprintId obligatorio al crear delivery** | Si se omite queda null — las tareas no aparecen en el sprint en el FE. |
| **Tarea SETUP como dependencia inicial** | Sin ella, agentes podrían arrancar antes de que el sprint esté configurado. |
| **PUT no PATCH para deliveries** | PATCH no funciona para campos como sprintId/order. |
| **assignedToId no assigneeId** | Backend ignora assigneeId silenciosamente. |
| **criteriaTypeCode no type** | Para CAs; endpoint /criteria no /acceptance-criteria. |
| **No inventar fuentes** | § Referencias del documento dice exactamente qué leer. |
| **ASSIGNMENT al momento de asignar** | Generarlo antes es inútil — el estado del repo puede cambiar. |
| **Script manifest es responsabilidad del TL** | Verificar antes de generar el mensaje de activación. |
| **Documento v1.0 insuficiente** | Solo títulos/horas no alcanza para BRIEFs de calidad. Solicitar v2.0. |
| **fileType=context no válido** | VTT rechaza `context` — subir CONTEXTO_SX como `fileType=brief`. |
| **categoryCode de devlog** | Valores válidos: `decision`, `testing_note`, `tech_debt` (y similares). No `development`, `setup`, `management`. |
| **Comentario: campos userId + message** | No `authorId`/`content` — el endpoint usa `userId` y `message`. |
| **Flujo de estados obligatorio** | `in_progress → in_review → task_completed`. No se puede saltar directo a completed. |
| **in_review requiere 3 attachments** | Antes de mover a in_review: subir devlog (`fileType=devlog`), code_logic (`fileType=code_logic`), y agregar comentario. |

---

## SECCIÓN 6 — ANÁLISIS DE DEPENDENCIAS REALES ENTRE SPRINTS

Al leer el HO, el TL clasifica cada tarea según su dependencia real — esto determina qué dependencias se registran en VTT.

### 6.1 Clasificación de tareas

| Tipo | Criterio | Dependencia en VTT |
|------|----------|--------------------|
| **Independiente** | No necesita outputs del sprint anterior — solo que el sprint esté configurado | `SETUP-SX` |
| **Dependiente cross-sprint** | Necesita código, schema, endpoints, o artifacts reales del sprint anterior | `SETUP-SX` + `ULTIMA_TAREA_OP_S(X-1)` |
| **Dependiente intra-sprint** | Depende de otra tarea del mismo sprint | Su tarea bloqueante según el HO |

**Criterio de decisión:**

```
¿La tarea puede arrancar el día 1 del sprint si SETUP-SX está completo?
  → SÍ: solo depende de SETUP-SX
  → NO (necesita output real del sprint anterior): depende de SETUP-SX + ULTIMA_TAREA_OP_S(X-1)
```

Ejemplos:
- `[4.3.5] DTOs/Schemas` — puede arrancar apenas el sprint esté configurado → solo `SETUP-SX`
- `[4.3.1] API Endpoints` — necesita las migrations y models del sprint anterior → `SETUP-SX` + `ULTIMA_TAREA_OP_S(X-1)`

> El TL hace este análisis leyendo el HO § Dependencias. Si el HO no lo especifica, revisar qué archivos/outputs consume la tarea.

### 6.2 Tabla de resolución HO → UUIDs reales

Antes del PASO 8, el TL construye esta tabla cruzando el HO con el CONTEXTO_S(X-1):

| Referencia en HO | Código VTT | UUID real (del CONTEXTO) |
|------------------|------------|--------------------------|
| "depende de Services S2" | MS-312 | `<uuid>` |
| "depende de Middlewares S2" | MS-308 | `<uuid>` |
| "última tarea op. S(X-1)" | MS-XXX | `<uuid>` |

> Sin esta tabla el TL registraría dependencias con códigos lógicos — VTT necesita UUIDs reales.  
> Los UUIDs vienen del CONTEXTO_S(X-1).md (attachment de la tarea SETUP-S(X-1) en VTT).

---

## SECCIÓN 7 — ARCHIVO DE SEGUIMIENTO OPERATIVO

Durante la ejecución del sprint el TL mantiene un archivo de tracking activo — diferente al CLOSURE que es solo para el cierre formal.

**Ubicación:** `knowledge/agent-tasks/SPRINT_STATUS_SX.md`

**Estructura:**

```markdown
# SPRINT STATUS — SX [Nombre]

**Última actualización:** YYYY-MM-DD
**Estado general:** 🟢 On track / 🟡 En riesgo / 🔴 Bloqueado

## Tareas

| Código | Título | Agente | Estado | Blocker | PR |
|--------|--------|--------|--------|---------|-----|
| MS-XXX | [4.3.1] API Endpoints | BE | 🔵 in_progress | — | #42 |
| MS-XXX | [4.3.5] DTOs/Schemas | BE | 🟡 pending | — | — |
| MS-XXX | [4.2.3] Seed Data | DB | 🔴 blocked | Falta schema final | — |

## Blockers activos

| # | Descripción | Tarea afectada | Acción TL | Desde |
|---|-------------|----------------|-----------|-------|
| 1 | Schema no finalizado | MS-XXX | Escalado al AR | 2026-05-20 |

## PRs pendientes de review

| PR | Tarea | Agente | Desde |
|----|-------|--------|-------|
| #42 | MS-XXX | BE | 2026-05-20 |

## Métricas parciales

| Métrica | Valor |
|---------|-------|
| Tareas completadas | X / N |
| Horas ejecutadas | Xh / Nh estimadas |
| PRs mergeados | X |
| Blockers resueltos | X |
```

> **Frecuencia de actualización:** El TL actualiza este archivo cada vez que revisa una tarea, resuelve un blocker, o aprueba un PR.  
> **No reemplaza al CLOSURE** — es el dashboard operativo del TL durante la ejecución.  
> **Al cerrar el sprint** — las métricas finales de este archivo alimentan el §6 del CLOSURE_SX.

---

## RELACIÓN CON OTROS DOCUMENTOS

| Documento | Relación |
|-----------|----------|
| `PROCESO_ASIGNACION_TAREAS_v3.md` | Ciclo completo de 16 pasos — este proceso es la Fase 1 expandida |
| `PROCESO_ANALISIS_DEPENDENCIAS_ASSIGNMENT.md` | Proceso para el ASSIGNMENT (Fase 2) |
| `MAPA_DEPENDENCIAS_ENTREGABLES.md` | Inputs obligatorios por fase/tarea |
| `MANUAL_FEATURES_VTT_V4.md` | Modelo dinámico: AC, DoD, DoR, Trackable Items, firmas |
| `03_FLUJO_TL.md` | Flujo genérico del TL |

---

**Archivo:** PROCESO_ANALISIS_HO_GENERACION_BRIEFS.md  
**Versión:** 1.5 | **Fecha:** 2026-05-20  
**Aplicable a:** TL al inicio de cada sprint
