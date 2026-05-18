# SKL-AUTH-01: Obtener JWT de Sesión

**Categoría:** AUTH  
**Aplica a:** Todos los agentes  
**Tokens estimados:** ~80  
**Cuándo inyectar:** Siempre — primera skill en cualquier sesión

## Precondición

Variables de entorno disponibles:
- `VTT_BASE_URL=http://77.42.88.106:3000`
- `AGENT_UUID` — UUID del agente en VTT
- `SERVICE_KEY=hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d`

## Ejecución

```python
import urllib.request, json, os

req = urllib.request.Request(
    f"{os.getenv('VTT_BASE_URL')}/api/auth/service-token",
    data=json.dumps({
        'userId': os.getenv('AGENT_UUID'),
        'serviceKey': os.getenv('SERVICE_KEY')
    }).encode(),
    headers={'Content-Type': 'application/json'},
    method='POST'
)
response = json.loads(urllib.request.urlopen(req).read())
TOKEN = response['data']['token']
```

## Validación

`TOKEN` no vacío, empieza con `eyJ`

## Error común

401 → `SERVICE_KEY` incorrecto. Verificar en `.env`.
