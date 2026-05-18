# Metodología: Setup del Plan de Proyecto en VTT
**Versión**: 1.0
**Fecha**: 2026-04-03
**Aplica a**: Inicio de cada fase/sprint en el sistema VTT

---

## 1. Objetivo

Definir el proceso estándar para configurar correctamente el plan de un sprint o fase en VTT, garantizando que el grafo de dependencias sea coherente, sin nodos huérfanos ni hojas abiertas.

---

## 2. Reglas Fundamentales del Grafo

Antes de crear una sola tarea, interiorizar estas reglas:

### 2.1 Todo nodo debe tener entrada Y salida

```
CORRECTO:   A → B → C → D
INCORRECTO: A → B     C → D   (C es huérfano, B es hoja)
```

- **Nodo huérfano** = tarea sin dependencias entrantes (ninguna tarea la precede)
- **Nodo hoja** = tarea sin dependencias salientes (ninguna tarea la sigue)
- **Excepción única**: el nodo ORIGEN (SETUP) no tiene entrada. El nodo CIERRE-FINAL no tiene salida.

### 2.2 Un solo nodo de inicio por fase

El nodo SETUP/ORIGEN es el punto de arranque absoluto. Solo él puede no tener dependencias entrantes.

### 2.3 Sprints secuenciales vs independientes

- **Sprints secuenciales** (ej. S09 → S10): S10 NO puede iniciar hasta que S09 esté cerrado.
- **Sprints independientes** (ej. S11 DL track): pueden arrancar desde el nodo ORIGEN en paralelo.

---

## 3. Estructura de Dependencias por Tipo de Tarea

### 3.1 Tareas de Base de Datos (DB)

```
ORIGEN → DB-01 → DB-02 → DB-03 → CIERRE-SPRINT
              ↓
           BE tasks (comienzan cuando DB está lista)
```

- La primera tarea DB arranca desde el nodo ORIGEN (o desde CIERRE del sprint anterior).
- Las DB posteriores dependen de la DB anterior.
- La última DB sin downstream conecta al **CIERRE del sprint**.

### 3.2 Tareas de Backend (BE)

```
DB-01 → BE-a (paralelo)
DB-02 → BE-b (paralelo)
DB-02 → BE-c (paralelo)
BE-a + BE-b → BE-d (consolidación)
BE-d → TL-Review
```

- Cada BE depende de la tarea DB que requiere.
- La tarea BE de consolidación (que jala a todas) es el punto de cierre del track BE.

### 3.3 Plan de Testing (QA-X-01)

```
❌ INCORRECTO: ORIGEN → QA-Test-Plan
❌ INCORRECTO: DB-01   → QA-Test-Plan

✅ CORRECTO:
BE-a + BE-b + BE-c (TODOS los BE completados) → QA-Test-Plan → QA-02, QA-03...
```

**Regla**: El Test Plan se escribe cuando el desarrollo está completo. No puede escribirse sobre código que no existe. El QA Test Plan habilita el inicio de las tareas de testing individual.

### 3.4 Tareas de QA individuales (QA-X-02, 03, ...)

```
BE-task  → QA-individual-test
FE-task  → QA-individual-test
QA-Test-Plan → QA-individual-test  ← el plan debe existir antes de testear

QA-individual-test → APR-QA-Sprint  ← toda prueba individual va a la aprobación QA
```

- Cada prueba individual conecta al nodo **APR-QA** de su sprint.
- APR-QA es el gate que aprueba que todo el QA del sprint pasó.

### 3.5 Tareas de Design Lead (DL)

```
ORIGEN → DL-S11-01 (inicio independiente)
           ↓
        DL-02, DL-03, DL-04 (paralelo, todos dependen de DL-01)
           ↓
        DL-05 (depende de DL-04)
        DL-06 (depende de DL-03)
           ↓
        APR-DL (depende de DL-06 + gate: CIERRE-BLOQUE anterior)
```

- Las tareas DL sin downstream conectan a **APR-DL**.
- APR-DL requiere también el cierre del bloque de desarrollo anterior (gate doble).

### 3.6 Tareas de Frontend (FE)

```
APR-DL → FE-01, FE-02 (arrancan cuando diseño aprobado)
FE-01  → FE-03, FE-04
FE-04  → FE-05 → FE-06
FE-01 + FE-04 + FE-05 + BE-b → FE-08

Todas las FE → TL-Review + DL-Review
```

- Toda tarea FE sin downstream conecta a **TL-Review** y a **DL-S11-REV**.

### 3.7 Nodos de Revisión y Cierre

```
BE-consolidación → TL-Review → AR-Review → CIERRE-SPRINT
DL-Review        → CIERRE-SPRINT
APR-QA           → CIERRE-SPRINT

CIERRE-S09 → primer tarea S10 (gate entre sprints secuenciales)
CIERRE-S10 + CIERRE-S09 → CIERRE-BLOQUE
CIERRE-BLOQUE → tareas S11 de desarrollo (BE-S11, FE-S11)
CIERRE-S11 + CIERRE-BLOQUE → CIERRE-FINAL
```

---

## 4. Proceso de Creación — Paso a Paso

### Paso 1: Crear el nodo ORIGEN
- Tarea tipo `setup` o `documentation`
- Sin dependencias entrantes
- Todos los "primeros" nodos de cada sprint dependen de esta tarea

### Paso 2: Crear todas las tareas
Para cada tarea verificar:
- [ ] Título claro con formato `ROL-SPRINT-NUM: Descripción`
- [ ] Categoría válida: `development | testing | review | documentation`
- [ ] Complejidad: `LOW | MEDIUM | HIGH`
- [ ] Horas estimadas (del handoff)
- [ ] Agente asignado (del handoff)

### Paso 3: Crear dependencias por sprint

Seguir el orden lógico del sprint:
1. DB chain (DB-01 → DB-02 → DB-03)
2. BE tasks (desde DB correspondiente)
3. QA individual tests (desde BE/FE correspondiente)
4. QA Test Plan (desde ÚLTIMOS BE + FE completados)
5. APR-QA (desde todos los QA individuales + Test Plan)
6. TL Review (desde BE consolidado + todas las FE)
7. AR Review (desde TL Review)
8. CIERRE-SPRINT (desde AR Review + APR-QA + DB sin downstream)

### Paso 4: Verificar el grafo — Script de auditoría

Ejecutar este script después de crear todas las dependencias:

```python
import urllib.request, json, time

API_BASE = "http://77.42.88.106:3000"

def get_token(user_id, service_key):
    d = json.dumps({"userId": user_id, "serviceKey": service_key}).encode()
    req = urllib.request.Request(f"{API_BASE}/api/auth/service-token", data=d,
        headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())["data"]["token"]

def get_deps(token, task_id):
    req = urllib.request.Request(f"{API_BASE}/api/tasks/{task_id}/dependencies",
        headers={"Authorization": f"Bearer {token}"}, method="GET")
    try:
        with urllib.request.urlopen(req) as r:
            raw = json.loads(r.read())
            return raw if isinstance(raw, list) else raw.get("data", raw.get("dependencies", []))
    except: return []

def audit_graph(token, task_ids, final_node, origin_node):
    depended_upon = set()
    has_incoming = set()

    for task_id in task_ids:
        deps = get_deps(token, task_id)
        for d in deps:
            dep_on = (d.get("dependsOnTaskId") or
                      d.get("dependsOnTask", {}).get("id") or
                      d.get("dependsOnTask", {}).get("vttId") or "")
            if dep_on:
                depended_upon.add(dep_on)
                has_incoming.add(task_id)
        time.sleep(0.05)

    # Leaves: nothing depends on them (except final node)
    leaves = [t for t in task_ids if t not in depended_upon and t != final_node]
    # Orphans: no incoming deps (except origin node and cancelled tasks)
    orphans = [t for t in task_ids if t not in has_incoming and t != origin_node]

    print(f"Leaf nodes (no outgoing): {len(leaves)}")
    for t in leaves: print(f"  LEAF: {t}")
    print(f"Orphan nodes (no incoming): {len(orphans)}")
    for t in orphans: print(f"  ORPHAN: {t}")

    if not leaves and not orphans:
        print("GRAPH OK - no leaves or orphans")
```

**Criterio de aceptación**: 0 hojas, 0 huérfanos (excepto nodos cancelados).

### Paso 5: Agregar tareas al snapshot del plan

```python
# POST /api/projects/{projectId}/plan/tasks
payload = {"taskIds": ["VTT-XXX", "VTT-YYY", ...], "force": False}
```

Solo ejecutar cuando el grafo esté validado (Paso 4 en verde).

---

## 5. Checklist de Validación Final

Antes de reportar el plan como listo:

- [ ] Todas las tareas tienen título, categoría, complejidad y horas
- [ ] Un único nodo ORIGEN sin dependencias entrantes
- [ ] Un único nodo CIERRE-FINAL sin dependencias salientes
- [ ] 0 nodos huérfanos (sin entrada)
- [ ] 0 nodos hoja (sin salida), excepto CIERRE-FINAL y tareas canceladas
- [ ] QA Test Plans dependen de desarrollo completo (BE + FE), NO del origen
- [ ] Cada tarea QA individual conecta al nodo APR-QA de su sprint
- [ ] Tareas DB sin downstream conectan al CIERRE de su sprint
- [ ] Tareas DL sin downstream conectan a APR-DL
- [ ] Tareas FE sin downstream conectan a TL-Review y DL-Review
- [ ] Plan snapshot actualizado vía `POST /plan/tasks`

---

## 6. Errores Comunes — No Repetir

| Error | Causa | Corrección |
|-------|-------|-----------|
| QA Test Plan desde el ORIGEN | "no tiene deps, lo pongo al inicio" | Siempre después de BE+FE completados |
| Tareas QA sin downstream | Olvidar conectar al APR-QA | Toda QA individual → APR-QA de su sprint |
| DB task sin downstream | Última DB no conecta al CIERRE | DB final → CIERRE-SPRINT |
| Múltiples nodos desde ORIGEN | Conectar test plans y tareas independientes al inicio | Solo nodos de inicio de sprint + tracks independientes parten del ORIGEN |
| FE tarea sin deps | "el spec dice sin deps" | Si es trabajo FE, siempre desde APR-DL como mínimo |

---

## 7. Referencia Rápida — Quién conecta con quién

```
ORIGEN
  ├── Sprint N inicio (DB-N-01)
  │     ├── BE tasks → TL-Review → AR-Review → CIERRE-N
  │     ├── QA Tests (desde BE) → APR-QA-N → CIERRE-N
  │     ├── QA Test Plan (desde TODOS los BE/FE) → habilita QA tests
  │     └── DB final → CIERRE-N
  │
  └── Track independiente (ej. DL-S11-01)
        └── DL tasks → APR-DL (gate: también espera CIERRE-BLOQUE)
              └── FE tasks → TL-Review + DL-Review → CIERRE-SPRINT-INDEPENDIENTE

CIERRE-SPRINT-N → inicio Sprint N+1 (si son secuenciales)
CIERRE-BLOQUE   → inicio desarrollo dependiente (BE/FE del sprint independiente)
CIERRE-FINAL    ← todos los CIERRE de sprint + CIERRE-BLOQUE
```
