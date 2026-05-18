# TEMPLATE — Reporte de Cumplimiento de CAs por el Agente

| Campo | Valor |
|---|---|
| **Código** | `VTT.TEMPLATE-CFL-001` |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-13 |
| **Aplica a** | Cualquier agente ejecutor (BE, DB, FE, DO, QA, DL, UX) |
| **Cuándo se usa** | Al cerrar la tarea, ANTES de mover a `task_in_review` |
| **Endpoint API** | `PATCH /api/tasks/:taskId/criteria/:cid` |

---

## Notas de uso del template

- Una llamada `PATCH` por cada CA — no se pueden agrupar
- Si una CA **no se cumple**, marcar `status="not_met"` y documentar razón en `evidence` (no omitir)
- `evidence` debe ser **concreta y verificable** — no aceptar "funciona" sino "comando X retorna Y"
- `notes` es opcional, sirve para contexto adicional
- El endpoint reemplaza al obsoleto `POST /criteria/:cid/fulfill` que devuelve 404
- Reglas críticas:
  - **R1**: Toda CA marcada `met` debe tener URL al PR o comando verificable en `evidence`
  - **R2**: `not_met` requiere descripción del bloqueante en `evidence`
  - **R3**: No marcar todas las CAs de golpe — el TL revisa cada una individualmente

---

## Patrón básico

```bash
# Obtener token del agente
TOKEN=$(curl -s -X POST $BASE/api/auth/service-token \
  -H "Content-Type: application/json" \
  -d "{\"userId\":\"$AGENT_UUID\",\"serviceKey\":\"$SERVICE_KEY\"}" \
  | python3 -c "import sys,json;print(json.load(sys.stdin)['data']['token'])")

# Reportar cada CA
curl -s -X PATCH "$BASE/api/tasks/$TASK_ID/criteria/$CRITERIA_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "met",
    "evidence": "<descripción concreta + URL al PR/comando>",
    "notes": "<contexto adicional opcional>"
  }'
```

---

## Status válidos del campo `status`

| Status | Cuándo usar | Requiere evidence | Bloquea Review Gate |
|---|---|---|---|
| `pending` | CA creada, aún no trabajada | No | Sí (si es required) |
| `met` | CA cumplida — entregable verificable | **Sí** | No |
| `not_met` | CA no se pudo cumplir — bloqueante o decisión técnica | **Sí (razón)** | Sí |
| `partial` | CA cumplida parcialmente | **Sí** | Sí (si es required) |
| `deferred` | CA diferida a sprint/release futuro | Sí + referencia al destino | No (si justificada) |

---

## Formato de `evidence` por tipo de CA

### CA de implementación de endpoint

```json
{
  "status": "met",
  "evidence": "PR #15 implementa POST /api/users (memory-service-backend/src/controllers/userController.ts:42-89). Verificado con: curl -X POST http://localhost:3001/api/users -d '{\"email\":\"test@test.com\"}' → 201 + UUID en response.body.data.id",
  "notes": "Validación email con Zod schema. Tests passing 100%."
}
```

### CA de cobertura de tests

```json
{
  "status": "met",
  "evidence": "npm run test:coverage → Lines: 87.3% (target ≥80%). Reporte: memory-service-backend/coverage/lcov-report/index.html. PR #15 (commit abc1234).",
  "notes": "Coverage por encima del threshold 80% requerido."
}
```

### CA de documentación

```json
{
  "status": "met",
  "evidence": "docs/SECRETS.md (336 líneas, 10 secciones). PR #15 línea 1-336. Incluye: inventario 19 variables, procedimiento rotación 90d, tabla de acceso, manejo de incidentes.",
  "notes": "Validado contra estructura del brief §6.2."
}
```

### CA con verificación funcional

```json
{
  "status": "met",
  "evidence": "Ejecutado curl -X GET http://77.42.88.106:3000/api/tasks/MS-285/review-gate → response.data.canProceedToReview=true, blockers=[], warnings=[1 low no-bloqueante]. Captura: knowledge/screenshots/MS-285_review_gate.png",
  "notes": null
}
```

### CA con dependencia bloqueada (status=not_met)

```json
{
  "status": "not_met",
  "evidence": "CA bloqueada por falta de migration de DB. Issue VTT creado: ISS-042 'Falta migration users.password'. Tarea en task_on_hold vinculada al issue. Resolución estimada: cuando DB Engineer entregue MS-049.",
  "notes": "Bloqueante reportado al PM. Sin workaround viable sin la migration."
}
```

### CA diferida a sprint/release futuro (status=deferred)

```json
{
  "status": "deferred",
  "evidence": "CA diferida a R2 por decisión técnica. ADR registrado: ADR-MS-024 'Diferir OAuth2 a R2 — R1 solo soporta API Key'. TI creado: DEBT-AUTH-01 (related_to MS-285). Marker [DEFER R2] aplicado.",
  "notes": "Aprobado por PM en handoff R1."
}
```

---

## Workflow del agente — reportar todas las CAs

```bash
# 1. Listar CAs de la tarea
curl -s "$BASE/api/tasks/$TASK_ID/criteria" \
  -H "Authorization: Bearer $TOKEN" | jq '.data[] | {id, title, status}'

# 2. Por cada CA → PATCH
for CRITERIA_ID in $(curl -s "$BASE/api/tasks/$TASK_ID/criteria" \
  -H "Authorization: Bearer $TOKEN" | jq -r '.data[].id'); do
  echo "Reportando $CRITERIA_ID..."
  # Llenar evidence específica para cada CA
  # PATCH individual
done

# 3. Verificar Review Gate antes de mover a in_review
curl -s "$BASE/api/tasks/$TASK_ID/review-gate" \
  -H "Authorization: Bearer $TOKEN" | jq '.data.canProceedToReview'
# Esperado: true
```

---

## Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| 404 al usar `/fulfill` | Endpoint legacy obsoleto | Usar `PATCH /criteria/:cid` (sin `/fulfill`) |
| 400 "status invalid" | Status fuera del enum | Usar uno de: pending\|met\|not_met\|partial\|deferred |
| 400 "evidence required" | CA marcada `met` sin `evidence` | Agregar descripción concreta |
| Review Gate sigue bloqueado | Alguna CA requerida en `pending` | Verificar `GET /criteria` y reportar las faltantes |
| 401 Unauthorized | TOKEN expirado | Renovar con SKL-AUTH-01 |

---

## Validación final

Antes de pasar a `task_in_review`, el agente verifica:

```bash
# Todas las CAs marcadas
curl -s "$BASE/api/tasks/$TASK_ID/criteria" -H "Authorization: Bearer $TOKEN" | \
  jq '.data | map(select(.status == "pending")) | length'
# Esperado: 0

# Ninguna requerida en not_met sin justificación
curl -s "$BASE/api/tasks/$TASK_ID/criteria" -H "Authorization: Bearer $TOKEN" | \
  jq '.data | map(select(.status == "not_met" and .required == true and (.evidence | length) < 50))'
# Esperado: array vacío

# Review Gate
curl -s "$BASE/api/tasks/$TASK_ID/review-gate" -H "Authorization: Bearer $TOKEN" | \
  jq '.data.canProceedToReview'
# Esperado: true
```

---

## Snippet Python — Reporte de todas las CAs

```python
import urllib.request, json, os, sys

BASE_URL = os.environ["VTT_BASE_URL"]
TASK_ID = sys.argv[1]
AGENT_UUID = os.environ["AGENT_UUID"]
SK = os.environ["SERVICE_KEY"]

# Token
req = urllib.request.Request(f'{BASE_URL}/api/auth/service-token',
    data=json.dumps({'userId':AGENT_UUID,'serviceKey':SK}).encode(),
    headers={'Content-Type':'application/json'}, method='POST')
TOKEN = json.loads(urllib.request.urlopen(req).read())['data']['token']

# CAs de la tarea
req = urllib.request.Request(f'{BASE_URL}/api/tasks/{TASK_ID}/criteria',
    headers={'Authorization': f'Bearer {TOKEN}'})
criteria = json.loads(urllib.request.urlopen(req).read()).get('data', [])

# Plantilla de evidence por CA (el agente la llena)
fulfillments = {
    # "criteria-id-001": {"status": "met", "evidence": "...", "notes": None},
}

for ca in criteria:
    cid = ca['id']
    if cid not in fulfillments:
        print(f"⚠️ Falta llenar {cid}: {ca['title']}")
        continue
    f = fulfillments[cid]
    body = json.dumps(f).encode()
    req = urllib.request.Request(
        f'{BASE_URL}/api/tasks/{TASK_ID}/criteria/{cid}',
        data=body,
        headers={'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'},
        method='PATCH'
    )
    try:
        urllib.request.urlopen(req)
        print(f"✅ {cid}: {ca['title'][:50]} → {f['status']}")
    except Exception as e:
        print(f"❌ {cid}: {e}")
```

---

## Referencias

- Endpoint VTT: `PATCH /api/tasks/:taskId/criteria/:cid`
- Documento legacy obsoleto: `POST /criteria/:cid/fulfill` (404)
- Skill relacionada: `SKL-TRACK-03_fulfillment-criterion.md`
- SOP relacionado: `VTT.PROTOCOL-ASG-001` (FASE 3 — Ejecución del agente)
- Workflow del agente: paso 14 del `TEMPLATE_ASIGNACION_TAREARev.md` v3.1

---

## Changelog

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-05-13 | Versión inicial — patrón observado en MS-283/284/285 |
