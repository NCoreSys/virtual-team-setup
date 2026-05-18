# ASSIGNMENT: MS-142 - Kickoff call del equipo (GATE)

**Task ID**: MS-142
**Brief ref**: INIT-G-02
**Titulo**: Kickoff call del equipo (GATE)
**Repositorio destino**: memory-service-project (NCoreSys/memory-service-project)
**Asignado a**: PM (Product Manager)
**Prioridad**: M (MEDIUM)
**Estimacion**: 2 horas
**Complejidad**: MEDIUM
**Categoria**: documentation
**Generado por**: TL
**Fecha asignacion**: 2026-05-02
**Dependencias**: MS-141 (Documento formal de Kickoff — debe estar APROBADO antes de iniciar esta tarea)

---

## 1. Objetivo

Realizar la sesión formal de kickoff con el equipo completo, revisar el documento KICKOFF_MEMORY_SERVICE.md, asignar compromisos por rol, y producir el acta firmada.

**Este es el GATE que habilita Fase 2 Discovery.** Sin esta tarea completada y aprobada, las tareas de Discovery no pueden iniciarse.

**Resultado esperado:** Acta `KICKOFF_ACTA_2026-05-02.md` subida al repo con compromisos y action items de cada rol, firmada por los participantes.

---

## 2. Contexto

Memory Service completó la fase INIT. El equipo tiene los repositorios configurados, las herramientas de calidad activas (linters, CI), y los documentos de onboarding disponibles. Este kickoff es el momento en que el equipo se alinea formalmente antes de iniciar el trabajo de Discovery y Development.

El PM conduce la sesión y produce el acta. En el contexto de agentes IA, "sesión" significa: el PM revisa el KICKOFF doc, genera los compromisos por rol basándose en la SPEC v1.9 y el estado actual, y produce el acta como entregable documental.

---

## 3. Archivos de Referencia (LEER ANTES DE EMPEZAR)

1. `knowledge/kickoff/KICKOFF_MEMORY_SERVICE.md` — Documento de MS-141 (debe estar aprobado)
2. `Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` — Alcance y objetivos R1
3. `.claude/rules/Proyect_data.md` — UUIDs del equipo
4. `knowledge/agent-tasks/assignments/phase1/` — Estado de tareas completadas

---

## 4. Entregable: KICKOFF_ACTA_2026-05-02.md

### Estructura del Acta

```markdown
# Acta de Kickoff — Memory Service R1

**Fecha**: 2026-05-02
**Conducida por**: PM Memory Service
**Participantes**: [Lista de roles presentes]

---

## 1. Resumen de la Sesión

[1-2 párrafos describiendo el propósito y resultado de la sesión]

---

## 2. Documentos Revisados

- `knowledge/kickoff/KICKOFF_MEMORY_SERVICE.md` v1.0 ✅
- `Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` ✅

---

## 3. Compromisos por Rol

### Tech Lead
- Commitment 1: [responsabilidad concreta]
- Commitment 2: ...

### Backend Engineer
- Commitment 1: ...

### Database Engineer
- Commitment 1: ...

### Frontend Developer
- Commitment 1: ...

### QA Engineer
- Commitment 1: ...

### DevOps Engineer
- Commitment 1: ...

### Design Lead
- Commitment 1: ...

---

## 4. Action Items

| # | Action Item | Responsable | Fecha límite | Estado |
|---|-------------|-------------|-------------|--------|
| AI-001 | [Descripción] | [Rol] | 2026-05-XX | ⏳ Pendiente |
| AI-002 | ... | ... | ... | ... |
| AI-003 | ... | ... | ... | ... |

---

## 5. Decisiones Tomadas

1. [Decisión 1 con contexto]
2. [Decisión 2]
3. ...

---

## 6. Próximos Pasos (Phase 2 Discovery)

- [ ] [Paso 1]
- [ ] [Paso 2]
- [ ] ...

---

## 7. Firmas

| Rol | Nombre | Fecha |
|-----|--------|-------|
| PM | Memory Service PM | 2026-05-02 |
| Tech Lead | Memory Service TL | 2026-05-02 |
| [Resto del equipo] | ... | ... |

---

**Acta generada por**: PM Memory Service
**Estado**: ✅ Aprobada
```

---

## 5. Implementación (via GitHub API)

```python
import urllib.request, json, base64

GH_TOKEN = "<tu-PAT-con-permisos-contents-write>"
REPO = "NCoreSys/memory-service-project"
BRANCH = "feature/MS-142"

ACTA_CONTENT = """# Acta de Kickoff — Memory Service R1
...(contenido completo del acta)...
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

# 3. Commit acta
content = base64.b64encode(ACTA_CONTENT.encode()).decode()
gh("PUT", f"/repos/{REPO}/contents/knowledge/kickoff/KICKOFF_ACTA_2026-05-02.md", {
    "message": "docs [MS-142]: Acta de Kickoff Memory Service R1 — GATE Fase 2",
    "content": content,
    "branch": BRANCH
})

# 4. Create PR
gh("POST", f"/repos/{REPO}/pulls", {
    "title": "[MS-142] Acta de Kickoff Memory Service R1 (GATE Fase 2)",
    "body": "Acta de kickoff con compromisos por rol y action items. GATE para iniciar Fase 2 Discovery. Ver devlog para detalles.",
    "head": BRANCH,
    "base": "main"
})
```

---

## 6. Entregables Obligatorios (Modelo Dinámico V4)

| # | Entregable | Obligatorio |
|---|------------|-------------|
| 1 | `knowledge/kickoff/KICKOFF_ACTA_2026-05-02.md` | ✅ Sí |
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
| CA-1 | `f9af031a-9e49-414d-878f-8600c57be0aa` | Kickoff call realizada con equipo completo | Acta lista con sección de participantes |
| CA-2 | `1cd35542-17f6-49aa-9a59-f6addaf09c66` | KICKOFF doc revisado en la call | Sección 2 del acta referencia KICKOFF_MEMORY_SERVICE.md |
| CA-3 | `beafbe36-8bcb-4afa-bd02-5d75b8784cb0` | Compromisos asignados por rol | Sección 3 del acta con compromisos para cada rol |
| CA-4 | `12a08989-50c0-40dd-9d10-83323379cfc6` | Action items con responsable y fecha | Tabla sección 4 con al menos 3 action items con fecha |
| CA-5 | `9e13f991-15d5-44df-ab5f-976f1a412e5b` | Acta creada y firmada | Archivo existe en `knowledge/kickoff/` con sección de firmas |

```bash
curl -s -X POST "http://77.42.88.106:3000/api/tasks/MS-142/criteria/{criteriaId}/fulfill" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "met", "evidence": "descripción de evidencia"}'
```

---

## 8. Devlog Entries — Qué Registrar

```bash
POST http://77.42.88.106:3000/api/tasks/MS-142/devlog-entries
{"categoryCode": "decision", "severity": null, "title": "...", "reportedBy": "350831b2-e1ae-4dbe-b2eb-7e023ec2e103"}
```

| Cuándo | categoryCode | severity |
|--------|-------------|----------|
| Decisión sobre compromisos de algún rol | `decision` | null |
| Riesgo identificado durante el kickoff | `risk` | high/medium |
| Si MS-141 no está aprobado al momento de iniciar | `blocker` | high |
| Action item crítico identificado | `observation` | null |

---

## 9. Workflow (13 pasos)

**0.** Obtener JWT (ver mensaje del sistema en comentario de la tarea)

**1.** Verificar que MS-141 está en estado `task_approved` antes de iniciar

**2.** Mover MS-142 a in_progress en VTT

**3.** Leer `KICKOFF_MEMORY_SERVICE.md` completo

**4.** Leer `SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` para definir compromisos reales

**5.** Redactar `KICKOFF_ACTA_2026-05-02.md` siguiendo estructura de sección 4

**6.** Crear branch `feature/MS-142` via GitHub API desde main actualizado

**7.** Commitear acta via GitHub API

**8.** Crear PR hacia main

**9.** Registrar devlog entries en VTT

**10.** Reportar CAs cumplidos en VTT

**11.** Crear Development Log

**12.** Verificar review gate:
```bash
curl -s "http://77.42.88.106:3000/api/tasks/MS-142/review-gate" -H "Authorization: Bearer $TOKEN"
```

**13.** Mover a in_review y enviar reporte (SKL-REPORT-01) como comentario

---

## 10. Notas Críticas

- **GATE**: Esta tarea es el gate que habilita Fase 2 Discovery. El TL/PM no deben marcar las tareas de Discovery como desbloqueadas hasta que esta tarea esté `task_approved`
- **Dependencia dura**: MS-141 debe estar `task_approved` antes de iniciar esta tarea. Si no está aprobada: registrar blocker en VTT, esperar
- **Compromisos por rol**: En el contexto de agentes IA, los compromisos deben ser concretos y derivados de la SPEC v1.9 (ej. "Backend: implementar endpoints de CRUD de memories en Phase 3"). No inventar compromisos genéricos
- **Action items**: Identificar al menos los action items de arranque de Phase 2: quién lee el SPEC, quién define el modelo de datos inicial, etc.

---

**Generado por**: TL (Martin Rivas)
**Fecha**: 2026-05-02
**Version**: 1.0
