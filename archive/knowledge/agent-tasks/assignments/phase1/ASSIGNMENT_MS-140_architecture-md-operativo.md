# ASSIGNMENT: MS-140 - ARCHITECTURE.md operativo

**Task ID**: MS-140
**Brief ref**: INIT-F-02
**Titulo**: ARCHITECTURE.md operativo
**Repositorio destino**: memory-service (NCoreSys/memory-service)
**Asignado a**: TL (Tech Lead)
**Prioridad**: M (MEDIUM)
**Estimacion**: 1 hora
**Complejidad**: MEDIUM
**Categoria**: documentation
**Generado por**: TL
**Fecha asignacion**: 2026-05-04
**Dependencias**: Ninguna (tarea independiente de documentación)

---

## 1. Objetivo

Crear `docs/ARCHITECTURE.md` en el repo `NCoreSys/memory-service` como vista de alto nivel de la arquitectura del proyecto Memory Service R1.

**Resultado esperado:** `docs/ARCHITECTURE.md` committeado en `main` con resumen arquitectónico legible en 5 minutos, diagrama ASCII de componentes, y link a SPEC v1.9.

**REGLA CLAVE**: NO duplicar el SPEC. Solo vista de alto nivel para onboarding rápido.

---

## 2. Contexto

El repo `NCoreSys/memory-service` contiene la documentación central del proyecto. El archivo `docs/ARCHITECTURE.md` sirve como punto de entrada arquitectónico para cualquier agente nuevo o colaborador. La fuente de verdad funcional es `SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` — este documento solo la referencia, no la replica.

---

## 3. Archivos de Referencia (LEER ANTES DE EMPEZAR)

1. `Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` — fuente de verdad: arquitectura, componentes, integraciones
2. `.claude/rules/Proyect_data.md` — UUIDs del equipo
3. `memory-service-project/00-agent-setup/06.Documentos_soporte/PROCESO_ASIGNACION_TAREAS.md` — reglas del proyecto

---

## 4. Estructura del Documento

### `docs/ARCHITECTURE.md`

```markdown
# Architecture — Memory Service R1

**Versión**: 1.0
**Fecha**: 2026-05-04
**Fuente de verdad completa**: [SPEC v1.9](../Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md)

---

## 1. Visión General

[1 párrafo: qué es Memory Service, qué problema resuelve]

---

## 2. Componentes Principales

[Diagrama ASCII de la arquitectura, ejemplo:]

```
┌─────────────────────────────────────────────┐
│              Memory Service                  │
│                                             │
│  ┌──────────────┐    ┌──────────────────┐   │
│  │   API REST   │───▶│  Core Engine     │   │
│  │  (Express)   │    │  (Memory CRUD)   │   │
│  └──────────────┘    └────────┬─────────┘   │
│                               │             │
│                    ┌──────────▼─────────┐   │
│                    │   Database (PG)    │   │
│                    └────────────────────┘   │
└─────────────────────────────────────────────┘
```

---

## 3. Stack Tecnológico

| Capa | Tecnología | Versión |
|------|-----------|---------|
| Runtime | Node.js | 20.x |
| Framework | Express | [ver] |
| Lenguaje | TypeScript | [ver] |
| Base de datos | PostgreSQL | [ver] |
| ORM | [ver SPEC] | [ver] |

---

## 4. Repos del Proyecto

| Repo | Propósito |
|------|-----------|
| `NCoreSys/memory-service` | Documentación central |
| `NCoreSys/memory-service-backend` | API + Core Engine |
| `NCoreSys/memory-service-project` | Config agentes + setup |

---

## 5. Flujo Principal

[Descripción del flujo principal en 3-5 pasos, derivado de SPEC v1.9]

---

## 6. Documentación Completa

Ver [SPEC Memory Service v1.9](../Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md) para:
- Contrato técnico completo
- Endpoints y modelos de datos
- Reglas de negocio
- Roadmap por fases
```

---

## 5. Implementación (via GitHub API)

```python
import urllib.request, json, base64

GH_TOKEN = "<tu-PAT-con-permisos-contents-write>"
REPO = "NCoreSys/memory-service"
BRANCH = "feature/MS-140"

ARCH_CONTENT = """# Architecture — Memory Service R1
...(contenido completo)...
"""

def gh(method, path, body=None):
    url = "https://api.github.com" + path
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + GH_TOKEN)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("Content-Type", "application/json")
    return json.loads(urllib.request.urlopen(req).read())

# 1. Get main SHA
main_sha = gh("GET", f"/repos/{REPO}/git/refs/heads/main")["object"]["sha"]

# 2. Verificar si docs/ ya existe (puede que no exista la carpeta)
try:
    existing = gh("GET", f"/repos/{REPO}/contents/docs")
    # Si existe, solo agregar el archivo
except:
    pass  # La carpeta se crea automáticamente al crear el archivo

# 3. Create branch
gh("POST", f"/repos/{REPO}/git/refs", {
    "ref": f"refs/heads/{BRANCH}",
    "sha": main_sha
})

# 4. Commit ARCHITECTURE.md
content = base64.b64encode(ARCH_CONTENT.encode()).decode()
gh("PUT", f"/repos/{REPO}/contents/docs/ARCHITECTURE.md", {
    "message": "docs [MS-140]: ARCHITECTURE.md operativo — vista de alto nivel",
    "content": content,
    "branch": BRANCH
})

# 5. Create PR
gh("POST", f"/repos/{REPO}/pulls", {
    "title": "[MS-140] ARCHITECTURE.md operativo — Memory Service R1",
    "body": "Agrega docs/ARCHITECTURE.md con vista de alto nivel de la arquitectura. NO duplica SPEC v1.9, solo referencia. Ver devlog para detalles.",
    "head": BRANCH,
    "base": "main"
})
```

---

## 6. Entregables Obligatorios (Modelo Dinámico V4)

| # | Entregable | Obligatorio |
|---|------------|-------------|
| 1 | `docs/ARCHITECTURE.md` en repo memory-service | ✅ Sí |
| 2 | Development Log | ✅ Sí |
| 3 | Code Logic | N/A — documento de arquitectura |
| 4 | Commit + PR | ✅ Sí |
| 5 | Swagger Docs | N/A |
| 6 | Devlog entries en VTT | ✅ Sí |
| 7 | CAs reportados con fulfill | ✅ Sí |
| 8 | TrackableItems | N/A |
| 9 | Review gate limpio | ✅ Sí |

---

## 7. Criterios de Aceptación

| CA | criteriaId | Criterio | Cómo verificar |
|----|------------|----------|----------------|
| CA-1 | `389183a3-8d09-42b1-ab09-992c0f7ca49b` | ARCHITECTURE.md existe en `docs/` del repo memory-service | `gh api repos/NCoreSys/memory-service/contents/docs/ARCHITECTURE.md` |
| CA-2 | `cc160198-bc16-47bf-b40a-2b3799173b2e` | Incluye diagrama ASCII de componentes | Verificar sección 2 del documento |
| CA-3 | `64e75446-25b3-49f2-83cf-d095bf23a4d2` | Link funcional al SPEC v1.9 | Verificar sección de referencias |
| CA-4 | `72e0c7e0-5188-4c94-8240-7b1650fe6b10` | Legible en 5 minutos (máx 1 página) | Review visual del documento |
| CA-5 | `e91abab4-73f9-48b3-a2e7-7d409fcb100c` | NO duplica contenido del SPEC | Comparar con SPEC — solo resumen |

```bash
curl -s -X POST "http://77.42.88.106:3000/api/tasks/MS-140/criteria/{criteriaId}/fulfill" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "met", "evidence": "descripción de evidencia"}'
```

---

## 8. Devlog Entries — Qué Registrar

```bash
POST http://77.42.88.106:3000/api/tasks/MS-140/devlog-entries
{"entries": [{"categoryCode": "decision", "severity": null, "title": "...", "reportedBy": "92225290-6b6b-4c1f-a940-dcb4262507aa"}]}
```

| Cuándo | categoryCode | severity |
|--------|-------------|----------|
| Decisión sobre qué incluir/excluir del documento | `decision` | null |
| Si la carpeta `docs/` no existe en el repo | `observation` | null |
| Si SPEC v1.9 tiene secciones de arquitectura incompletas | `observation` | null |

---

## 9. Workflow (13 pasos)

**0.** Obtener JWT:
```python
import urllib.request, json, sys
req = urllib.request.Request(
    'http://77.42.88.106:3000/api/auth/service-token',
    data=json.dumps({'userId':'92225290-6b6b-4c1f-a940-dcb4262507aa','serviceKey':'hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d'}).encode(),
    headers={'Content-Type':'application/json'}, method='POST')
with urllib.request.urlopen(req) as r:
    sys.stdout.write(json.loads(r.read())['data']['token'])
```

**1.** Mover MS-140 a in_progress:
```bash
curl -s -X PATCH http://77.42.88.106:3000/api/tasks/MS-140/status \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"statusId":"2a76888a-e595-4cfc-ac4c-a3ae5087ef56","changedBy":"92225290-6b6b-4c1f-a940-dcb4262507aa"}'
```

**2.** Leer `SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` — secciones de arquitectura, componentes, stack

**3.** Verificar si `docs/` existe en `NCoreSys/memory-service`:
```bash
gh api repos/NCoreSys/memory-service/contents/docs --jq '[.[].name]' 2>/dev/null || echo "carpeta no existe"
```

**4.** Redactar `ARCHITECTURE.md` siguiendo estructura de sección 4

**5.** Crear branch `feature/MS-140` via GitHub API desde main

**6.** Commitear `docs/ARCHITECTURE.md` via GitHub API

**7.** Crear PR hacia main

**8.** Registrar devlog entries en VTT

**9.** Reportar CAs cumplidos en VTT

**10.** Crear Development Log

**11.** Verificar review gate:
```bash
curl -s "http://77.42.88.106:3000/api/tasks/MS-140/review-gate" -H "Authorization: Bearer $TOKEN"
```

**12.** Mover a in_review:
```bash
curl -s -X PATCH http://77.42.88.106:3000/api/tasks/MS-140/status \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"statusId":"1ec975a5-7581-4a1a-ab8f-51b1a7ef868d","changedBy":"92225290-6b6b-4c1f-a940-dcb4262507aa"}'
```

**13.** Enviar reporte de entrega (SKL-REPORT-01) como comentario en la tarea

---

## 10. Notas

- El repo destino es `NCoreSys/memory-service` (documentación), NO `memory-service-backend`
- Si la carpeta `docs/` no existe, se crea automáticamente al hacer PUT del archivo via GitHub API
- El documento debe ser autosuficiente para entender la arquitectura en 5 minutos — no un índice de links
- El TL tiene PAT con acceso a `NCoreSys/memory-service` para pushear via GitHub API
- UUIDs de status: in_progress=`2a76888a-e595-4cfc-ac4c-a3ae5087ef56` | in_review=`1ec975a5-7581-4a1a-ab8f-51b1a7ef868d`

---

**Generado por**: TL (Martin Rivas)
**Fecha**: 2026-05-04
**Version**: 1.0
