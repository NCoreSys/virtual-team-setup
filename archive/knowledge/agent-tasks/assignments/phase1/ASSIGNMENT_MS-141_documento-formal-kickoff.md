# ASSIGNMENT: MS-141 - Documento formal de Kickoff

**Task ID**: MS-141
**Brief ref**: INIT-G-01
**Titulo**: Documento formal de Kickoff
**Repositorio destino**: memory-service-project (NCoreSys/memory-service-project)
**Asignado a**: PM (Product Manager)
**Prioridad**: M (MEDIUM)
**Estimacion**: 2 horas
**Complejidad**: MEDIUM
**Categoria**: documentation
**Generado por**: TL
**Fecha asignacion**: 2026-05-02
**Dependencias**: MS-131 (Onboarding TL ✅), MS-134 (Onboarding equipo ✅), MS-135 (Onboarding por rol — en progreso)

---

## 1. Objetivo

Crear `KICKOFF_MEMORY_SERVICE.md` como documento formal de arranque del proyecto Memory Service R1. Este documento consolida visión, alcance, equipo, roadmap, riesgos y criterios de éxito en un solo artefacto que sirve como referencia durante todo el proyecto.

**Resultado esperado:** Documento completo, firmado por el PM, subido al repo `NCoreSys/memory-service-project` en `knowledge/kickoff/`.

---

## 2. Contexto

El proyecto Memory Service está en fase INIT (Phase 1). Las tareas de setup están completándose. Este documento marca formalmente el inicio del proyecto y sirve de input para el Kickoff Call (MS-142), que es el GATE para iniciar Fase 2 Discovery.

**Fuente de verdad funcional**: `Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` — leer antes de escribir el documento.

---

## 3. Archivos de Referencia (LEER ANTES DE EMPEZAR)

1. `Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` — Fuente de verdad: visión, objetivos, alcance R1
2. `memory-service-project/00-agent-setup/01.agent-setup/` — UUIDs y datos del equipo
3. `.claude/rules/Proyect_data.md` — UUIDs completos del equipo
4. `knowledge/agent-tasks/briefs/phase1/` — Estado actual de las tareas Phase 1

---

## 4. Estructura del Documento

El documento `KICKOFF_MEMORY_SERVICE.md` debe contener las siguientes secciones:

### 4.1. Header
```markdown
# Kickoff — Memory Service R1
**Fecha**: 2026-05-02
**Versión**: 1.0
**Estado**: Activo
**Firmado por**: [PM Name] — PM Memory Service
```

### 4.2. Visión del Producto
- Qué es Memory Service (1 párrafo)
- Problema que resuelve
- Propuesta de valor principal

### 4.3. Objetivos de Release 1 (R1)
- Lista de 5-7 objetivos concretos y medibles
- Fecha objetivo de completion de R1

### 4.4. Alcance R1

**IN SCOPE** (qué sí se hace en R1):
- Lista explícita de funcionalidades/módulos incluidos

**OUT OF SCOPE** (qué NO se hace en R1):
- Lista explícita de lo que queda para R2+

### 4.5. Equipo

| Rol | Nombre/Agente | UUID VTT | Email |
|-----|--------------|----------|-------|
| PM | Memory Service PM | `350831b2-e1ae-4dbe-b2eb-7e023ec2e103` | `pm@memory-service.vtt.ai` |
| Tech Lead | Memory Service TL | `92225290-6b6b-4c1f-a940-dcb4262507aa` | `memory-service.tl@vtt.ai` |
| Backend | Memory Service BE | `ebbe3cee-abed-4b3b-860d-0a81f632b08a` | `memory-service.be@vtt.ai` |
| Database | Memory Service DB | `6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7` | `memory-service.db@vtt.ai` |
| Frontend | Memory Service FE | `d23c9cd9-a156-433b-8900-94add5488eec` | `memory-service.fe@vtt.ai` |
| QA | Memory Service QA | `613c9538-658c-45fe-a6d7-c1ea9ff04b78` | `memory-service.qa@vtt.ai` |
| DevOps | Memory Service DO | `322e3745-9756-4a7c-af11-44b33edef44d` | `memory-service.devops@vtt.ai` |
| Design Lead | Memory Service DL | `b3a09269-cded-468c-a475-15a48f203cb0` | `memory-service.dl@vtt.ai` |
| AR | Memory Service AR | `e9403c25-c1f8-4b64-b2ef-f447d53115e2` | `ar@memory-service.vtt.ai` |
| SA | Memory Service SA | `0c128e3b-db3b-4e31-b107-0379b5791233` | `sa@memory-service.vtt.ai` |

### 4.6. Roadmap (Fechas por Fase)

| Fase | Nombre | Fecha inicio | Fecha fin | Estado |
|------|--------|-------------|-----------|--------|
| Phase 1 | INIT | 2026-04-XX | 2026-05-XX | 🔵 En progreso |
| Phase 2 | Discovery | TBD | TBD | ⏳ Pendiente |
| Phase 3 | Development | TBD | TBD | ⏳ Pendiente |
| Phase 4 | Testing | TBD | TBD | ⏳ Pendiente |
| Phase 5 | Release | TBD | TBD | ⏳ Pendiente |

> Completar fechas reales desde la SPEC v1.9 si están definidas.

### 4.7. Riesgos Identificados

| # | Riesgo | Probabilidad | Impacto | Mitigación |
|---|--------|-------------|---------|------------|
| R1 | [Riesgo técnico principal] | Alta/Media/Baja | Alto/Medio/Bajo | [Acción] |
| R2 | [Riesgo de alcance] | ... | ... | ... |
| R3 | [Riesgo de integración] | ... | ... | ... |

> Identificar al menos 3 riesgos reales desde la SPEC v1.9.

### 4.8. Criterios de Éxito R1

Lista de métricas/condiciones medibles que indican que R1 fue exitoso:
- [ ] [Criterio 1 medible]
- [ ] [Criterio 2 medible]
- [ ] [Criterio 3 medible]
- [ ] ...

### 4.9. Firma
```markdown
**Firmado**: [PM — Memory Service]
**Fecha**: 2026-05-02
**Versión**: 1.0
```

---

## 5. Implementación (via GitHub API)

```python
import urllib.request, json, base64

GH_TOKEN = "<tu-PAT-con-permisos-contents-write>"
REPO = "NCoreSys/memory-service-project"
BRANCH = "feature/MS-141"

# Contenido del KICKOFF_MEMORY_SERVICE.md (completar secciones)
KICKOFF_CONTENT = """# Kickoff — Memory Service R1
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

# 2. Create branch
gh("POST", f"/repos/{REPO}/git/refs", {
    "ref": f"refs/heads/{BRANCH}",
    "sha": main_sha
})

# 3. Commit kickoff doc
content = base64.b64encode(KICKOFF_CONTENT.encode()).decode()
gh("PUT", f"/repos/{REPO}/contents/knowledge/kickoff/KICKOFF_MEMORY_SERVICE.md", {
    "message": "docs [MS-141]: Documento formal de Kickoff Memory Service R1",
    "content": content,
    "branch": BRANCH
})

# 4. Create PR
gh("POST", f"/repos/{REPO}/pulls", {
    "title": "[MS-141] Documento formal de Kickoff Memory Service R1",
    "body": "Documento de kickoff con visión, alcance, equipo, roadmap, riesgos y criterios de éxito R1. Ver devlog para detalles.",
    "head": BRANCH,
    "base": "main"
})
```

---

## 6. Entregables Obligatorios (Modelo Dinámico V4)

| # | Entregable | Obligatorio |
|---|------------|-------------|
| 1 | `knowledge/kickoff/KICKOFF_MEMORY_SERVICE.md` | ✅ Sí |
| 2 | Development Log | ✅ Sí |
| 3 | Code Logic | N/A — documento de gestión |
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
| CA-1 | `3297d405-c098-447c-b211-906e30443739` | KICKOFF_MEMORY_SERVICE.md creado | Verificar en `knowledge/kickoff/` del repo |
| CA-2 | `f18223cb-44c7-43fc-b8f1-3dc3b03204f4` | Visión y objetivos R1 documentados | Secciones 4.2 y 4.3 presentes y completas |
| CA-3 | `a6a700a7-8772-40a5-9d18-0a637e796d87` | Alcance in/out definido | Sección 4.4 con lista IN y OUT explícitas |
| CA-4 | `4468935b-7aa8-4982-b7ad-f8e0f7f6f898` | Equipo con roles y UUIDs | Tabla 4.5 completa con todos los UUIDs |
| CA-5 | `6d1ca3c9-9d8b-48bb-8030-e2be59ae36f4` | Roadmap con fechas por fase | Tabla 4.6 presente con fechas reales o TBD justificado |
| CA-6 | `85110808-1c45-4d04-b9b2-319609c7865b` | Riesgos y criterios de éxito R1 | Secciones 4.7 y 4.8 con al menos 3 riesgos y 3 criterios |

```bash
curl -s -X POST "http://77.42.88.106:3000/api/tasks/MS-141/criteria/{criteriaId}/fulfill" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "met", "evidence": "descripción de evidencia"}'
```

---

## 8. Devlog Entries — Qué Registrar

```bash
POST http://77.42.88.106:3000/api/tasks/MS-141/devlog-entries
{"categoryCode": "decision", "severity": null, "title": "...", "reportedBy": "350831b2-e1ae-4dbe-b2eb-7e023ec2e103"}
```

| Cuándo | categoryCode | severity |
|--------|-------------|----------|
| Decisión sobre qué incluir en alcance R1 | `decision` | null |
| Riesgo no documentado en SPEC que se identifica | `risk` | high/medium |
| Si SPEC v1.9 tiene información incompleta | `observation` | null |
| Fecha de roadmap confirmada o asumida | `decision` | null |

---

## 9. Workflow (13 pasos)

**0.** Obtener JWT (ver mensaje del sistema en comentario de la tarea)

**1.** Mover MS-141 a in_progress en VTT

**2.** Leer `SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` completo

**3.** Leer datos del equipo desde `.claude/rules/Proyect_data.md`

**4.** Redactar `KICKOFF_MEMORY_SERVICE.md` siguiendo estructura de sección 4

**5.** Crear branch `feature/MS-141` via GitHub API

**6.** Commitear documento via GitHub API

**7.** Crear PR hacia main

**8.** Registrar devlog entries en VTT

**9.** Reportar CAs cumplidos en VTT

**10.** Crear Development Log

**11.** Verificar review gate

**12.** Mover a in_review

**13.** Enviar reporte (SKL-REPORT-01) como comentario

---

## 10. Notas

- El documento será presentado en MS-142 (Kickoff Call). Debe ser claro y ejecutivo, no técnico
- Si la SPEC v1.9 tiene fechas de roadmap, usarlas. Si no, poner TBD con nota de que se definirán en Discovery
- El documento se firma por el PM — incluir sección de firma con nombre y fecha
- MS-142 depende de este documento: no iniciar la call sin el documento aprobado

---

**Generado por**: TL (Martin Rivas)
**Fecha**: 2026-05-02
**Version**: 1.0
