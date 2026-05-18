# SETUP — Architect (AR) | Memory Service

**Rol:** Solution Architect  
**Proyecto:** Memory Service  
**Fecha:** 2026-05-05

---

## Mensaje de arranque

Pega este mensaje al iniciar la sesión del AR:

```
Eres el Solution Architect (AR) del proyecto Memory Service.

Lee primero tu OPERATIVO completo:
→ `.claude/agents/OPERATIVO_AR_MEMORY-SERVICE.md`

Luego ejecuta tu rutina de apertura (§5 del OPERATIVO):
1. Obtener token JWT
2. Leer `knowledge/PROJECT_MEMORY.md`
3. Consultar tus tareas asignadas en VTT
4. Identificar tarea activa y empezar

Tu tarea inmediata desbloqueada es MS-019 (Non-Functional Requirements).
Lee el ASSIGNMENT en: `memory-service-project/knowledge/agent-tasks/assignments/ASSIGNMENT_MS-019_non-functional-requirements.md`
```

---

## Archivos incluidos en este kit

| Archivo | Para qué |
|---------|---------|
| `OPERATIVO_AR_MEMORY-SERVICE.md` | Identidad, comandos, flujo de trabajo — leer al iniciar |
| `ASSIGNMENT_MS-019_non-functional-requirements.md` | Tarea inmediata a ejecutar |
| `PROJECT_MEMORY.md` | Contexto persistente del proyecto |
| `SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` | Fuente de verdad técnica — D-MEM-01..43 |
| `AR_REVIEW_SPEC_MEMORY_SERVICE_v1.md` | Review propio previo — Q-01..Q-05, AR-OBS-01..02 |
| `ADDENDUM_INTEGRACION_MEMORY_SERVICE_v1.1.md` | SLAs cross-service Runtime + Prompt Builder |
| `SKL-STRUCTURE-01_ubicar-entregable.md` | Dónde depositar entregables por fase |
| `11_GUIA_AGENTES_MODELO_DINAMICO_V4.md` | API VTT completa — referencia de comandos |

---

## Credenciales

| Campo | Valor |
|-------|-------|
| **UUID** | `e9403c25-c1f8-4b64-b2ef-f447d53115e2` |
| **Email** | `ar@memory-service.vtt.ai` |
| **SERVICE_KEY** | `hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d` |
| **API URL** | `http://77.42.88.106:3000` |
| **Project ID** | `d0fc276d-e764-4a83-96e9-d65f086ed803` |

---

## Tarea inmediata: MS-019

- **Título:** Non-Functional Requirements
- **Fase:** Analysis (Phase 4)
- **Status actual:** `task_blocked` → se desbloqueará cuando MS-018 esté `task_completed`
- **Entregables:** 6 documentos NFR en `phases/02-analysis/deliverables/non-functional-requirements/`
- **Horas estimadas:** 4h
- **Reviewer:** SA Reviewer

---

**Repo local:** `c:\Users\Martin\Documents\virtual-teams\memory-service\`
