# VTT.SKILL-AUTH-001 — Obtener JWT de Sesión

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-AUTH-001` |
| **Categoría** | AUTH (Authentication) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-19 |
| **Aplica a** | Todos los roles (TL, PM, PJM, SA, BE, DB, FE, DO, QA, DL, UX, AR) — humanos y agentes |
| **Tokens estimados** | ~150 |
| **Cuándo se usa** | **Primera skill en cualquier sesión.** Cualquier llamada a la API VTT requiere `$TOKEN` en el header `Authorization: Bearer $TOKEN`. |
| **Reemplaza** | `SKL-AUTH-01_obtener-jwt.md` (legacy en `_pending-migration/auth/`) |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `agent_uuid` | uuid | sí | UUID del agente/usuario en VTT (lo obtiene desde su OPERATIVO) |
| `service_key` | string | sí | Service key del proyecto (compartida entre todos los agentes — vive en `.env` o variable de entorno) |
| `base_url` | url | sí | Base URL del backend VTT (default `http://77.42.88.106:3000`) |

> **Política contractual:** los 3 inputs son fijos. No hay variantes de auth (login con email/password está deprecado para agentes — ese flow es solo para humanos vía UI).

---

## Precondición

- Existe el usuario en VTT con el `agent_uuid` provisto
- El `service_key` está vigente (no expirado)
- Conectividad al backend VTT (sin firewall bloqueando `:3000`)

---

## Variables del entorno

```bash
$VTT_BASE_URL       # default http://77.42.88.106:3000
$AGENT_UUID         # UUID del actor que invoca (cada agente tiene el suyo)
$SERVICE_KEY        # Service key del proyecto — NUNCA hardcodear en el código
```

> **Regla de seguridad:** la `$SERVICE_KEY` se carga desde `.env` del proyecto o variable de entorno del shell. **NO se commitea en git.**

---

## Ejecución

### Opción A — Inline Python (recomendado para agentes IA)

```python
import urllib.request
import json
import os

req = urllib.request.Request(
    f"{os.environ['VTT_BASE_URL']}/api/auth/service-token",
    data=json.dumps({
        'userId': os.environ['AGENT_UUID'],
        'serviceKey': os.environ['SERVICE_KEY']
    }).encode('utf-8'),
    headers={'Content-Type': 'application/json'},
    method='POST'
)

with urllib.request.urlopen(req) as response:
    body = json.loads(response.read())
    TOKEN = body['data']['token']

# Exportar para skills subsecuentes
os.environ['TOKEN'] = TOKEN
print(f"TOKEN obtenido ({len(TOKEN)} chars)")
```

### Opción B — Bash one-liner (para coordinador humano)

```bash
export TOKEN=$(curl -s -X POST "$VTT_BASE_URL/api/auth/service-token" \
  -H "Content-Type: application/json" \
  -d "{\"userId\": \"$AGENT_UUID\", \"serviceKey\": \"$SERVICE_KEY\"}" \
  | python -c "import sys, json; print(json.load(sys.stdin)['data']['token'])")
```

---

## Validación

```bash
# Token no vacío
[ -n "$TOKEN" ] && echo "OK: TOKEN cargado" || echo "ERROR: TOKEN vacío"

# Estructura JWT (empieza con 'eyJ')
[[ "$TOKEN" == eyJ* ]] && echo "OK: formato JWT válido" || echo "ERROR: no es JWT"

# Token funciona contra VTT
curl -s "$VTT_BASE_URL/api/users/me" -H "Authorization: Bearer $TOKEN" \
  | python -c "import sys, json; d=json.load(sys.stdin); print(f\"OK: user_id={d['data']['id']}\")"
```

**Esperado:** 3 líneas con `OK:` y el `user_id` matching el `$AGENT_UUID`.

---

## Vida útil del token

| Aspecto | Valor |
|---|---|
| Duración | 30 días (configurable en VTT backend) |
| Refresh automático | ❌ No implementado en el backend actual |
| Acción al expirar | Re-ejecutar esta skill — devuelve nuevo token |

> **Política operativa:** los agentes guardan el TOKEN en variable de entorno de la sesión. NO persistir en disco (token es credencial sensible).

---

## Error común

| Error | Causa probable | Solución |
|---|---|---|
| `HTTP 401 Unauthorized` | `SERVICE_KEY` incorrecto o expirado | Verificar en `.env` del proyecto. Si está expirado, solicitar nuevo al PM. |
| `HTTP 404 Not Found` | `AGENT_UUID` no existe en VTT | Verificar UUID contra `GET /api/users` con un token admin |
| `HTTP 500 Internal Server Error` | Backend caído | Verificar healthcheck `curl $VTT_BASE_URL/api/health` |
| `Connection refused` | Backend no accesible (firewall, IP cambió) | Confirmar `$VTT_BASE_URL` actual |
| `KeyError: 'data'` | Response shape cambió | Verificar con `curl ... | jq .` qué retorna el endpoint |
| Token vacío después de `urlopen` | Body JSON malformado | Imprimir `response.read()` para diagnóstico |

---

## Scripts invocados

Sin Scripts externos — lógica inline ≤30 líneas Python con `urllib.request` puro.

> Si en el futuro se requiere refresh automático o caching de tokens entre sesiones, generar `VTT.SCRIPT-AUTH-001_obtener_jwt.py` que cubra ambos casos.

---

## Skills invocadas

Ninguna. Esta es la skill **base** que todas las demás presuponen ya ejecutada.

---

## Cuándo NO usar esta Skill

- **Si ya tenés `$TOKEN` cargado en la sesión actual** — reusar. No hay penalidad por solicitar otro pero genera ruido en logs del backend.
- **Si vas a hacer auth de humano vía UI** — usar el login normal de la UI de VTT, no esta skill (que es para service tokens).

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-19 | Versión inicial. Migración formal de `SKL-AUTH-01_obtener-jwt.md` legacy al formato VTT.SKILL. Ampliación: separación inputs contractuales, 2 opciones de ejecución (Python inline / bash), tabla de errores comunes con 6 casos, política operativa del token (no persistir en disco). Contrato funcional **sin cambios** vs legacy. |
