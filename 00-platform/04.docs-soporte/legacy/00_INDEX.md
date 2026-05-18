# 00 — INDEX Y JERARQUÍA OPERATIVA

**Capa:** Estándar (genérico, portable)
**Propósito:** Definir qué documentos mandan, cuándo se leen y cómo resolver conflictos antes de ejecutar cualquier trabajo en proyectos gestionados con la plataforma Virtual Teams.
**Versión:** 1.0

---

## 1. PRINCIPIO RECTOR

- El **sistema de gestión (VTT)** y el **código real** son la verdad operativa final.
- La documentación define proceso, contexto, formatos y validaciones.
- Si un documento contradice al código implementado o al estado real en VTT, se debe **verificar y escalar** antes de actuar.

---

## 2. CAPAS DE PRECEDENCIA

### Nivel 0 — Onboarding conceptual

Se lee **UNA SOLA VEZ** al empezar a operar en la plataforma:

- `01_ONBOARDING.md` — Taxonomía del sistema (Proyecto → Release → Sprint → Fase → Delivery → Tarea)

### Nivel 1 — Núcleo obligatorio (estándar portable)

Se consultan siempre antes de ejecutar trabajo real:

1. `02_OPERACION_AGENTE.md` — Ciclo de vida de tareas, issues, on-hold, git flow, endpoints
2. `03_FLUJO_TL.md` — Flujo del Tech Lead (FASE 1 + FASE 2, 8 elementos del assignment)
3. `04_ESTRUCTURA_FASES.md` — Layout de carpetas por fase SDLC
4. `05_CATALOGO_DELIVERABLES.md` — 438 deliverables por fase (catálogo completo)

### Nivel 2 — Guías de validación y calidad

Aplican cuando la tarea entra a validación, review o testing:

1. `CODE_REVIEW_GUIDE_V1.1.md` (si existe en el proyecto)
2. `INTEGRATION_AUDIT_CHECKLIST_V1.1.md` (si existe en el proyecto)
3. `TESTING_GUIDE_V1.1.md` (si existe en el proyecto)

### Nivel 3 — Perfiles de rol

Se leen solo si el rol está activo en la tarea o fase:

- `roles/AGENT_PROFILE_BASE_TL.md` — perfil base del Tech Lead
- `roles/AGENT_PROFILE_BASE_[BE|FE|DB|DO|QA|DL|UX|PJM|AR|SA].md` — otros roles
- `OPERATIVO_[PROYECTO]_[ROL].md` — instancia específica del proyecto (UUIDs, URLs, comandos)

### Nivel 4 — Templates de artefactos

Se usan cuando toca producir un documento:

- `templates/MEMORY_TEMPLATE.md` — memoria del proyecto
- Handoff, Brief, Assignment, DevLog, Code Logic, UX Spec (templates del proyecto)

### Nivel 5 — Contexto y memoria

Sirven como apoyo, NO como fuente máxima:

- `PROJECT_MEMORY.md` del proyecto específico
- `CONTEXTO_[ROL]_SESION.md` — estado actual del sprint (live)
- Historiales, devlogs previos

### Nivel 6 — Sistema y código (verdad final)

Siempre validar contra:

- Estado real de tareas en el sistema de gestión
- Rutas, schemas y contratos reales del backend
- Router y componentes reales del frontend
- Esquema de datos real (Prisma)

---

## 3. REGLAS DE CONFLICTO

### Caso A — Documento viejo vs documento nuevo

- Gana el documento **más reciente y más específico**.
- Si ambos parecen vigentes, **escalar al PM/TL** antes de ejecutar.

### Caso B — Documento vs código

- Gana el **código implementado** para contratos técnicos.
- El desalineamiento debe registrarse como issue, fix o deuda.

### Caso C — Documento vs estado del sistema

- Gana **el sistema (VTT)** para status, ownership, dependencias y aprobaciones.

### Caso D — Memoria vs proceso formal

- La memoria ayuda a entender contexto, pero **NUNCA reemplaza** el proceso formal.
- Ante conflicto, el proceso formal (documentos de Nivel 1) gana.

---

## 4. SECUENCIA OBLIGATORIA ANTES DE ACTUAR

```
1. Identificar el tipo de solicitud:
   pregunta | análisis | setup | ejecución | review | cierre

2. Identificar el rol operativo que aplica.

3. Leer el núcleo obligatorio (Nivel 1) si aún no está en contexto.

4. Leer la guía del rol (Nivel 3), si aplica.

5. Leer el template del artefacto que se va a producir (Nivel 4).

6. Revisar memoria o contexto (Nivel 5) solo como apoyo.

7. Verificar VTT y código real (Nivel 6).

8. Ejecutar.
```

---

## 5. MAPA DE DOCUMENTOS DEL SISTEMA

### Documentos ESTÁNDAR (portables entre proyectos)

Ubicación: `Project_setup/standard/`

| # | Documento | Propósito | Cuándo leer |
|---|-----------|-----------|-------------|
| 00 | `00_INDEX.md` | Este documento — jerarquía y precedencia | Referencia ante dudas |
| 01 | `01_ONBOARDING.md` | Taxonomía conceptual | Una sola vez al empezar |
| 02 | `02_OPERACION_AGENTE.md` | Operación común a todos los agentes | Cada sesión como referencia |
| 03 | `03_FLUJO_TL.md` | Flujo del Tech Lead | Cada vez que el TL arma un assignment |
| 04 | `04_ESTRUCTURA_FASES.md` | Layout de carpetas por fase | Al crear archivos o estructura |
| 05 | `05_CATALOGO_DELIVERABLES.md` | 438 deliverables por fase SDLC | Al planificar una fase |

### Perfiles de rol (genéricos)

Ubicación: `Project_setup/standard/roles/`

| Documento | Para rol |
|-----------|----------|
| `AGENT_PROFILE_BASE_TL.md` | Tech Lead |
| `AGENT_PROFILE_BASE_[ROL].md` | Otros roles (a crear según necesidad) |

### Templates (se rellenan por proyecto)

Ubicación: `Project_setup/templates/`

| Documento | Propósito |
|-----------|-----------|
| `MEMORY_TEMPLATE.md` | Plantilla de memoria de proyecto |

### Documentos de proyecto (instancia específica)

Ubicación: `[repo-del-proyecto]/`

| Documento | Dónde vive | Propósito |
|-----------|------------|-----------|
| `PROJECT_MEMORY.md` | `knowledge/` | Instancia de MEMORY_TEMPLATE con datos reales |
| `OPERATIVO_[ROL].md` | `.claude/agents/` | Instancia del perfil de rol con UUIDs, URLs reales |
| `CONTEXTO_[ROL]_SESION.md` | `knowledge/agent-tasks/` | Estado actual del sprint (live) |

---

## 6. RESULTADO ESPERADO

Si esta jerarquía se sigue bien:

- **No se trabaja desde memoria informal**
- **No se usan documentos equivocados**
- **No se rompen gates ni fases**
- **El sistema se vuelve repetible entre proyectos**
- **Los prompts de agente se ensamblan consistentemente**

---

## 7. RELACIÓN CON EL PROMPT DEL AGENTE

Los prompts de los agentes se **ensamblan** leyendo secciones de varios documentos de esta jerarquía. No son archivos separados.

Ejemplo: el prompt del Tech Lead tiene 9 secciones que se componen así:

| Sección del prompt TL | Se arma leyendo |
|------------------------|------------------|
| 1. Identidad | `AGENT_PROFILE_BASE_TL` §1 + `OPERATIVO_TECH_LEAD` + `PROJECT_MEMORY` §5 |
| 2. Responsabilidades | `AGENT_PROFILE_BASE_TL` §3 |
| 3. Límites | `AGENT_PROFILE_BASE_TL` §7 + `OPERATIVO_TECH_LEAD` |
| 4. Reglas operativas | `02_OPERACION_AGENTE` §10 + `PROJECT_MEMORY` §17 |
| 5. SOP del rol | `03_FLUJO_TL` + `OPERATIVO_TECH_LEAD` §Proceso |
| 6. Fuentes de verdad | `03_FLUJO_TL` + `OPERATIVO_TECH_LEAD` + `PROJECT_MEMORY` §7 |
| 7. Contexto actual | `PROJECT_MEMORY` §3+§16 + `CONTEXTO_TL_SESION` |
| 8. Tarea específica | Runtime (inyectado por PM) |
| 9. Contrato de salida | `AGENT_PROFILE_BASE_TL` §4+§10 + `02_OPERACION_AGENTE` + `OPERATIVO_TECH_LEAD` |

---

## 8. HISTORIAL DE VERSIONES

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0 | 2026-04-20 | Versión inicial consolidada desde `JERARQUIA_OPERATIVA.md` del memory-service. Alineada con la arquitectura de 2 capas (estándar + proyecto) y el ensamblado del prompt de agente de 9 secciones. |

---

**Fuente de verdad de este documento:** `Project_setup/standard/00_INDEX.md`
