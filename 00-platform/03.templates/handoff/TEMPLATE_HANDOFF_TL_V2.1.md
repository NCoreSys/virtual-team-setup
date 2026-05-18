# HANDOFF TL: [PROYECTO] — Sprint [N]

**Documento:** HANDOFF_TL_SPRINT_[N].md  
**Versión:** 2.1  
**De:** PJM-Agent  
**Para:** TL (Tech Lead)  
**Fecha:** [YYYY-MM-DD]  
**Sprint:** [N] — [Nombre del Sprint]  
**Estado:** 📋 READY  
**Prerrequisitos:** [Lista de dependencias o "Ninguno"]

---

## 0. RESUMEN EJECUTIVO

[2-3 párrafos describiendo:]
- Objetivo del sprint
- Contexto del proyecto
- Por qué este sprint es importante ahora
- Qué se desbloquea al completarlo

**Duración total:** [X] horas  
**Distribución:** DB: [X]h | BE: [X]h | TL: [X]h

---

## 1. ARQUITECTURA DEL SPRINT

### 1.1 Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────────┐
│                    SPRINT [N]: [NOMBRE]                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [Diagrama ASCII de los módulos/componentes del sprint]         │
│                                                                  │
│  Ejemplo:                                                        │
│  ┌─────────┐     ┌─────────┐     ┌─────────┐                    │
│  │ Módulo  │────▶│ Módulo  │────▶│ Módulo  │                    │
│  │    A    │     │    B    │     │    C    │                    │
│  └─────────┘     └─────────┘     └─────────┘                    │
│      Xh              Yh              Zh                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 ADRs del Sprint

**ADRs nuevos de este sprint:**

| ADR | Decisión | Impacto |
|-----|----------|---------|
| ADR-[XXX] | [Título de la decisión] | [Qué afecta] |

> **Si no hay ADRs nuevos:** "Este sprint no introduce decisiones arquitectónicas nuevas."

**ADRs previos relevantes:**

| ADR | Decisión | Por qué aplica |
|-----|----------|----------------|
| ADR-[YYY] | [Título] | [Cómo afecta a este sprint] |

> **Si no hay ADRs previos relevantes:** "No hay ADRs previos que impacten este sprint."

### 1.3 Dependencias Externas

| Servicio | Usado para | Configuración |
|----------|-----------|---------------|
| [Redis] | [Cache/Sessions] | `REDIS_URL` en .env |
| [MinIO] | [Storage] | `MINIO_*` en .env |

---

## 2. ENDPOINTS A IMPLEMENTAR

### 2.1 Resumen de API

| Método | Path | Descripción | Auth | Permiso | Tarea |
|--------|------|-------------|------|---------|-------|
| GET | `/api/[recurso]` | [Descripción] | ✅ | `read:[recurso]` | BE-001 |
| POST | `/api/[recurso]` | [Descripción] | ✅ | `create:[recurso]` | BE-002 |
| PATCH | `/api/[recurso]/:id` | [Descripción] | ✅ | `update:[recurso]` | BE-003 |
| GET | `/api/public/[recurso]` | [Descripción] | ❌ | — | BE-004 |

### 2.2 Detalle por Endpoint

#### [METHOD] /api/[path] (BE-XXX)

**Auth:** ✅ Requerido  
**Permiso:** `[acción]:[recurso]`

**Request:**
```json
{
  "field1": "type",
  "field2": "type"
}
```

**Response 200:**
```json
{
  "data": {
    "id": "uuid",
    "field1": "value"
  }
}
```

**Validaciones:**
- `field1`: requerido, string, max 255
- `field2`: opcional, enum [A, B, C]

**Errores:**
- `400`: Validación fallida
- `401`: No autenticado
- `403`: Sin permiso
- `404`: Recurso no encontrado

---

## 3. BRIEFS PARA AGENTES

### 3.1 Brief DB Engineer

| Tarea | Descripción | Estimado |
|-------|-------------|----------|
| DB-001 | [Descripción de migración/tabla] | [X]h |
| DB-002 | [Descripción de índices/seeds] | [X]h |

**Schema esperado:**
```sql
-- Tabla: [nombre]
CREATE TABLE [nombre] (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  -- campos...
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_[nombre]_[campo] ON [nombre]([campo]);
```

**Criterios de Aceptación DB:**
- [ ] CA-DB-01: [Criterio específico]
- [ ] CA-DB-02: [Criterio específico]

### 3.2 Brief Backend Engineer

| Tarea | Descripción | Estimado | Depende de |
|-------|-------------|----------|-----------|
| BE-001 | [Service: descripción] | [X]h | DB-001 |
| BE-002 | [Endpoint: descripción] | [X]h | BE-001 |
| BE-003 | [Validador: descripción] | [X]h | — |

**Archivos a crear:**
```
src/
├── services/
│   └── [nombre].service.ts
├── routes/
│   └── [nombre].routes.ts
├── validators/
│   └── [nombre].validator.ts
└── types/
    └── [nombre].types.ts
```

**Criterios de Aceptación BE:**
- [ ] CA-BE-01: [Criterio específico]
- [ ] CA-BE-02: [Criterio específico]
- [ ] CA-BE-03: [Criterio específico]
- [ ] CA-BE-04: Archivo `.LOGIC.md` creado/actualizado por cada archivo de código creado o modificado

### 3.3 Brief DevOps Engineer (si aplica)

| Tarea | Descripción | Estimado |
|-------|-------------|----------|
| DO-001 | [Descripción de infra/config] | [X]h |
| DO-002 | [Descripción de deployment] | [X]h |

**Configuración requerida:**
- [ ] [Item de configuración 1]
- [ ] [Item de configuración 2]

**Criterios de Aceptación DO:**
- [ ] CA-DO-01: [Criterio específico]
- [ ] CA-DO-02: [Criterio específico]

> **Si no hay tareas DO en este sprint:** Eliminar esta sección.

### 3.4 Brief Frontend Engineer (⏳ Fase 2 — No incluir en handoff inicial)

> **Esta sección NO se entrega al inicio del sprint.**  
> Se redacta y asigna ÚNICAMENTE cuando se cumple el Gate FE (§11):
> - ✅ BE endpoints en `task_in_review`
> - ✅ APR-DL firmado (DL aprobó HTMLs)
>
> **TL crea las tareas FE en VTT y entrega el brief en ese momento.**

| Tarea | Descripción | Estimado | Depende de |
|-------|-------------|----------|-----------|
| FE-001 | [Pantalla/componente: descripción] | [X]h | APR-DL + BE-XXX |
| FE-002 | [Pantalla/componente: descripción] | [X]h | FE-001 |

**Archivos HTML de referencia (Design/specs/):**
- `[nombre-pantalla].html` — [qué cubre]

**Criterios de Aceptación FE:**
- [ ] CA-FE-01: [Criterio específico]
- [ ] CA-FE-02: [Criterio específico]
- [ ] CA-FE-03: Archivo `.LOGIC.md` creado/actualizado por cada componente creado o modificado

---

## 4. VARIABLES DE ENTORNO

| Variable | Descripción | Ejemplo | Requerida |
|----------|-------------|---------|-----------|
| `[VAR_NAME]` | [Para qué se usa] | `valor_ejemplo` | ✅/❌ |

**Agregar a `.env.example`:**
```bash
# Sprint [N] - [Nombre]
[VAR_NAME]=valor_default
```

---

## 5. RIESGOS Y MITIGACIONES

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| [Descripción del riesgo] | Alta/Media/Baja | Alto/Medio/Bajo | [Cómo mitigar] |

---

## 6. TAREAS DEL SPRINT

### Fase: Desarrollo (Días 1-X)

| ID | Tarea | Agente | Estimado | Complejidad | Categoría |
|----|-------|--------|----------|-------------|-----------|
| DB-001 | [Descripción] | DB | [X]h | HIGH/MEDIUM/LOW | development |
| BE-001 | [Descripción] | BE | [X]h | HIGH/MEDIUM/LOW | development |
| BE-002 | [Descripción] | BE | [X]h | HIGH/MEDIUM/LOW | development |
| TL-001 | Code Review PRs | TL | [X]h | MEDIUM | review |

### Fase: Validación (Días X-Y)

| ID | Tarea | Agente | Estimado | Complejidad | Categoría |
|----|-------|--------|----------|-------------|-----------|
| TL-002 | Technical Validation | TL | [X]h | MEDIUM | review |
| AR-001 | Integration Audit | AR | [X]h | MEDIUM | review |

---

## 7. DEPENDENCIAS ENTRE TAREAS

| Tarea | Depende de | Tipo | Nota |
|-------|-----------|------|------|
| BE-001 | DB-001 | FS | Necesita schema creado |
| BE-002 | BE-001 | FS | Necesita service |
| TL-001 | BE-002 | FS | Code Review post-implementación |
| AR-001 | TL-001 | FS | Integration Audit post-Code Review |

> **Tipo FS:** Finish-to-Start (la más común). La tarea bloqueada comienza cuando la bloqueante termina.

---

## 8. VTT PLANNING DATA

> Tabla para crear tareas en VTT. **TL crea las tareas de DB + BE + TL + AR** al inicio del sprint.  
> **Las tareas FE se crean en Fase 2**, cuando se cumple el Gate FE (§11): BE `in_review` + APR-DL firmado.

| Tarea | estimatedHours | complexity | category | dependsOn |
|-------|---------------|-----------|----------|-----------|
| DB-001 | [X] | [HIGH/MEDIUM/LOW] | development | — |
| BE-001 | [X] | [HIGH/MEDIUM/LOW] | development | DB-001 |
| BE-002 | [X] | [HIGH/MEDIUM/LOW] | development | BE-001 |
| TL-001 | [X] | MEDIUM | review | BE-002 |
| AR-001 | [X] | MEDIUM | review | TL-001 |

**Total TL scope:** [X]h

---

## 9. DOCUMENTOS DINÁMICOS A ACTUALIZAR

| Documento | Quién actualiza | Cuándo | Verificado en |
|-----------|----------------|--------|---------------|
| `API_CONTRACT.md` | BE | Al completar cada endpoint | Code Review (TL) |
| `*.LOGIC.md` | BE/DB | Al completar cada archivo | Code Review (TL) |
| `MODELO_DATOS.md` | DB | Al crear/modificar tablas | Code Review (TL) |
| `SCHEMA_REFERENCE.md` | TL | Post-merge | Integration Audit (AR) |

---

## 10. DoD — TL

### Coordinación:
- [ ] Todas las tareas DB asignadas y con dependencias configuradas
- [ ] Todas las tareas BE asignadas y con dependencias configuradas
- [ ] Todas las tareas DO asignadas (si aplica)
- [ ] Briefs entregados a DB, BE y DO
- [ ] Variables de entorno documentadas
- [ ] **FE bloqueado hasta que DL entregó HTMLs (APR-DL) y BE endpoints en `in_review`**

### Code Review:
- [ ] Todos los PRs revisados usando `CODE_REVIEW_GUIDE.md`
- [ ] Sin blockers pendientes
- [ ] Documentación dinámica actualizada

### Validación:
- [ ] Technical Validation completada (APR-TL)
- [ ] Integration Audit coordinada con AR
- [ ] 4 firmas recolectadas para cierre
- [ ] ⚠️ **NUNCA** mover ninguna tarea a `task_approved` — ese estado es del PM/Owner, es TERMINAL e irreversible

### Documentación:
- [ ] SCHEMA_REFERENCE actualizado
- [ ] API_CONTRACT actualizado
- [ ] DevLogs de agentes revisados

---

## 11. GATES DE APROBACIÓN

| Gate | Condición | Acción en VTT |
|------|-----------|---------------|
| DB puede arrancar | Sprint iniciado | TL notifica a DB |
| BE puede arrancar | DB-XXX completadas | Sistema desbloquea automático |
| FE puede arrancar | BE endpoints `in_review` + APR-DL aprobado | **TL crea y asigna tareas FE en VTT**, luego notifica a FE |
| DL-REVIEW puede arrancar | FE `in_review` | **TL crea tarea DL-REVIEW (3h MEDIUM)** y asigna a DL |
| QA puede arrancar | DL-REVIEW completado + FE aprobado | TL notifica a QA |
| Validación inicia | Desarrollo completo | TL notifica AR, QA, DL |
| Sprint cerrado | 4 firmas completas | TL crea APR-SPRINT para PM |

> **⚠️ Regla crítica:** FE NO puede empezar sin HTMLs aprobados (APR-DL). TL es responsable de verificar esta condición antes de crear las tareas FE en VTT y notificar al agente.

---

## 12. REFERENCIAS

| Documento | Ubicación | Para qué |
|-----------|-----------|----------|
| `CODE_REVIEW_GUIDE_V1.1.md` | `_project_manager/Templates/Handoff_proceso/` | Proceso de Code Review |
| `INTEGRATION_AUDIT_CHECKLIST_V1.1.md` | `_project_manager/Templates/Handoff_proceso/` | Referencia para AR |
| `TESTING_GUIDE_V1.1.md` | `_project_manager/Templates/Handoff_proceso/` | Referencia para QA |
| `METODOLOGIA_EJECUCION_SPRINTS_V1.1.md` | `_project_manager/Templates/Handoff_proceso/` | Proceso completo |
| `ADR_SPRINT_[N].md` | `_project_manager/Fases/Sprint [N]/` | Decisiones arquitectónicas |

---

## 13. HISTORIAL DE VERSIONES

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | [YYYY-MM-DD] | PJM-Agent | Versión inicial |
| 2.0 | 2026-03-30 | PJM-Agent | V2: ADRs previos, Brief DO, CAs por rol, Auth/Permisos en endpoints, check FE bloqueado, TL crea tareas FE |
| 2.1 | 2026-03-30 | PJM-Agent | CA .LOGIC.md en BE, §3.4 Brief FE deferred, nota Fase 2 en VTT Planning, warning task_approved, DL-REVIEW en gates, rutas corregidas |

---

**FIN DEL HANDOFF TL**
