# SETUP — Design Lead (DL) | Memory Service

**Rol:** Design Lead
**Proyecto:** Memory Service
**Fecha:** 2026-05-05

---

## Mensaje de arranque

Pega este mensaje al iniciar la sesión del DL:

```
Eres el Design Lead (DL) del proyecto Memory Service.

Lee primero tu OPERATIVO completo:
→ `.claude/agents/OPERATIVO_DL_MEMORY-SERVICE.md`

Luego ejecuta tu rutina de apertura (§5 del OPERATIVO):
1. Obtener token JWT
2. Leer `knowledge/PROJECT_MEMORY.md`
3. Verificar tareas en `task_in_review` de fases 5-6
4. Verificar estado de tareas asignadas al UX (tu equipo)

Todas tus tareas están actualmente en `task_blocked` — se desbloquean
cuando la fase Analysis (4) esté completa. Mientras tanto, familiarízate
con el SPEC v1.9 §8 (contratos API) y los User Flows de MS-023 (UX) para
preparar la producción del Design System (MS-028).
```

---

## Archivos incluidos en este kit

| Archivo | Para qué |
|---------|---------|
| `OPERATIVO_DL_MEMORY-SERVICE.md` | Identidad, comandos, SOP revisión, 11 tareas asignadas |
| `PROJECT_MEMORY.md` | Contexto persistente del proyecto |
| `SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` | Fuente de verdad — §8 contratos API, modelo de datos |
| `SKL-STRUCTURE-01_ubicar-entregable.md` | Dónde depositar entregables por fase |
| `11_GUIA_AGENTES_MODELO_DINAMICO_V4.md` | API VTT completa — referencia de comandos |

---

## Credenciales

| Campo | Valor |
|-------|-------|
| **UUID** | `b3a09269-cded-468c-a475-15a48f203cb0` |
| **Email** | `memory-service.dl@vtt.ai` |
| **SERVICE_KEY** | `hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d` |
| **API URL** | `http://77.42.88.106:3000` |
| **Project ID** | `d0fc276d-e764-4a83-96e9-d65f086ed803` |

---

## Tus 11 tareas (todas bloqueadas por Analysis)

| Task ID | Título | Status |
|---------|--------|--------|
| MS-028 | Design System | `task_blocked` |
| MS-029 | Wireframes - Dashboard | `task_blocked` |
| MS-030 | Wireframes - Timeline | `task_blocked` |
| MS-031 | Wireframes - Viewer | `task_blocked` |
| MS-032 | Wireframes - Cost Report | `task_blocked` |
| MS-033 | Wireframes - Lista Convs | `task_blocked` |
| MS-034 | Wireframes - Import Manual | `task_blocked` |
| MS-035 | Wireframes - Health | `task_blocked` |
| MS-036 | Wireframes - Extras | `task_blocked` |
| MS-037 | Design Handoff - Assets | `task_blocked` |
| MS-038 | Design Handoff - Final | `task_blocked` |

> MS-028 (Design System) será la primera en desbloquearse. Es el prerequisito de todos los wireframes.

---

## Tu equipo (UX Designer)

| Rol | UUID | Tareas asignadas |
|-----|------|-----------------|
| UX Designer | `a75a1dae-754a-4b6f-a3ff-db8d51f6a91b` | MS-023 (activa), MS-026, MS-027 |

---

**Repo local:** `c:\Users\Martin\Documents\virtual-teams\memory-service\`
