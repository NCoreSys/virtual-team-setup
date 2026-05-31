# Manual: Registro de Trackable Items en VTT

**Versión:** 1.0  
**Fecha:** 2026-05-06  
**Autor:** SA Ejecutor (`0c128e3b-db3b-4e31-b107-0379b5791233`)  
**Aplica a:** Cualquier agente que deba registrar RF, RNF, ADR, AS, BR, etc. en VTT

---

## 1. Conceptos clave

| Concepto | Valor |
|----------|-------|
| Base URL | `http://77.42.88.106:3000` |
| Project ID | `d0fc276d-e764-4a83-96e9-d65f086ed803` |
| R1 Release ID | `92664a70-8812-4468-abc5-6b3f63d7ef54` |
| Service Key | `hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d` |

---

## 2. Obtener token JWT

```python
import urllib.request, json

def get_token(user_id, service_key):
    url = "http://77.42.88.106:3000/api/auth/service-token"
    body = json.dumps({"userId": user_id, "serviceKey": service_key}).encode()
    req = urllib.request.Request(url, data=body, method="POST", headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())["data"]["token"]
```

El token expira — regenerar si recibes 401.

---

## 3. typeCodes válidos para proyectos software

| typeCode | Semántica | Usar para |
|----------|-----------|-----------|
| `rf` | Requisito Funcional | RF-XXX |
| `rnf` | Requisito No Funcional | NFR-XXX |
| `adr` | Architecture Decision Record | ADR-XXX |
| `assumption` | Supuesto / Hipótesis | AS-XXX, HYP-XXX |
| `business_rule` | Regla de Negocio | BR-XXX |
| `user_story` | Historia de Usuario | US-XXX |
| `use_case` | Caso de Uso | UC-XXX |
| `bug` | Bug | BUG-XXX |
| `tech_debt` | Deuda técnica | TD-XXX |

**⚠️ NO válidos para software:** `hypothesis`, `kpi` — son de proyectos research/marketing.

---

## 4. Flujo completo: crear, linkear y deferir

### 4.1 Función helper de API

```python
import urllib.request, json

TOKEN = "<JWT aquí>"
BASE_URL = "http://77.42.88.106:3000"

def api_call(url, data=None, method="POST"):
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method, headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    })
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.read().decode()[:100]}"}
```

### 4.2 Crear un item

```python
PROJECT_ID = "d0fc276d-e764-4a83-96e9-d65f086ed803"

result = api_call(
    f"{BASE_URL}/api/projects/{PROJECT_ID}/trackable-items",
    {
        "code": "RF-001",           # código único del item
        "title": "Título corto",    # título descriptivo
        "description": "Descripción completa con decisiones y referencias.",
        "priority": "high",         # high | medium | low
        "typeCode": "rf"            # ver tabla sección 3
    }
)
item_id = result.get("data", {}).get("id")  # UUID del item creado
```

**Manejo de duplicados (409):** si el item ya existe, no es error — saltearlo y usar el ID existente si se necesita.

### 4.3 Linkear item a una tarea

```python
TASK_ID = "MS-019"  # ID de la tarea VTT

result = api_call(
    f"{BASE_URL}/api/trackable-items/{item_id}/tasks",
    {"taskId": TASK_ID}
)
# 409 = ya estaba linkeado, también es OK
```

### 4.4 Deferir un item (para items que no aplican en R1)

El item **debe estar en `ti_approved`** antes de poder deferir.

```python
R1_RELEASE_ID = "92664a70-8812-4468-abc5-6b3f63d7ef54"
SA_ID = "0c128e3b-db3b-4e31-b107-0379b5791233"

# Paso 1: aprobar
api_call(
    f"{BASE_URL}/api/trackable-items/{item_id}",
    {"statusCode": "ti_approved"},
    method="PATCH"
)

# Paso 2: deferir
api_call(
    f"{BASE_URL}/api/trackable-items/{item_id}/defer",
    {
        "targetType": "release",
        "targetReleaseId": R1_RELEASE_ID,  # usar R1 como placeholder si R2/R3 no existe
        "reason": "[Deferred to R2] Razón del diferimiento. Note: targetReleaseId references R1 as placeholder since R2 not yet created.",
        "deferredBy": SA_ID
    }
)
```

---

## 5. Script template completo

```python
import urllib.request, json

TOKEN = "<JWT>"
PROJECT_ID = "d0fc276d-e764-4a83-96e9-d65f086ed803"
BASE_URL = "http://77.42.88.106:3000"
TASK_ID = "MS-XXX"
SA_ID = "0c128e3b-db3b-4e31-b107-0379b5791233"
R1_RELEASE_ID = "92664a70-8812-4468-abc5-6b3f63d7ef54"

items = [
    # (code, title, description, priority, typeCode, defer_to_r2)
    ("RF-001", "Título", "Descripción completa.", "high", "rf", False),
    ("ADR-001", "Título ADR", "Descripción ADR.", "high", "adr", False),
    ("AS-001", "Supuesto", "Descripción supuesto.", "medium", "assumption", False),
    ("NFR-SEC-07", "NFR diferido", "Sin RBAC en R1 (LIM-05). Plan R2.", "low", "rnf", True),
]

def api_call(url, data=None, method="POST"):
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method, headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    })
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.read().decode()[:100]}"}

created = []
for code, title, desc, priority, type_code, defer in items:
    result = api_call(
        f"{BASE_URL}/api/projects/{PROJECT_ID}/trackable-items",
        {"code": code, "title": title, "description": desc, "priority": priority, "typeCode": type_code}
    )
    item = result.get("data", {})
    item_id = item.get("id")
    if item_id:
        created.append((code, item_id, defer))
        print(f"OK {code}: {item_id[:8]}")
    else:
        err = str(result.get("error", "?"))
        if "409" in err:
            print(f"SKIP {code}: ya existe")
        else:
            print(f"ERR {code}: {err[:80]}")

# Linkear a tarea
for code, item_id, defer in created:
    result = api_call(f"{BASE_URL}/api/trackable-items/{item_id}/tasks", {"taskId": TASK_ID})
    if "data" not in result:
        err = str(result.get("error", "?"))
        if "409" not in err:
            print(f"LINK ERR {code}: {err[:80]}")

# Deferir los marcados
for code, item_id, defer in created:
    if not defer:
        continue
    api_call(f"{BASE_URL}/api/trackable-items/{item_id}", {"statusCode": "ti_approved"}, method="PATCH")
    result = api_call(
        f"{BASE_URL}/api/trackable-items/{item_id}/defer",
        {
            "targetType": "release",
            "targetReleaseId": R1_RELEASE_ID,
            "reason": f"[Deferred to R2] {code} no aplica en R1. Ver limitaciones del proyecto.",
            "deferredBy": SA_ID
        }
    )
    print(f"DEFER {code}: {'OK' if 'data' in result else result.get('error','?')}")

print(f"\nTotal: {len(created)} items procesados")
```

---

## 6. Errores comunes y soluciones

| Error | Causa | Solución |
|-------|-------|----------|
| `HTTP 401` | Token expirado | Regenerar token con POST /api/auth/service-token |
| `HTTP 409` | Item ya existe | Ignorar — el item ya está registrado |
| `HTTP 400: Unrecognized key(s): typeCode, code` | PATCH no acepta estos campos | No se puede cambiar typeCode/code — eliminar y recrear |
| `HTTP 400: Type hypothesis not valid` | typeCode inválido para software | Usar `assumption` en su lugar |
| `Cannot defer item with status ti_draft` | Item no aprobado antes de deferir | PATCH statusCode=ti_approved primero |
| `HTTP 400` en defer sin mensaje claro | Schema incorrecto | Campos requeridos: targetType, targetReleaseId, reason, deferredBy |

---

## 7. IDs de roles del equipo

| Rol | Email | UUID |
|-----|-------|------|
| SA | sa@memory-service.vtt.ai | `0c128e3b-db3b-4e31-b107-0379b5791233` |
| AR | ar@memory-service.vtt.ai | `e9403c25-c1f8-4b64-b2ef-f447d53115e2` |
| TL | memory-service.tl@vtt.ai | `92225290-6b6b-4c1f-a940-dcb4262507aa` |
| BE | memory-service.be@vtt.ai | `ebbe3cee-abed-4b3b-860d-0a81f632b08a` |
| DB | memory-service.db@vtt.ai | `6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7` |
| FE | memory-service.fe@vtt.ai | `d23c9cd9-a156-433b-8900-94add5488eec` |
| QA | memory-service.qa@vtt.ai | `613c9538-658c-45fe-a6d7-c1ea9ff04b78` |
| DevOps | memory-service.devops@vtt.ai | `322e3745-9756-4a7c-af11-44b33edef44d` |
