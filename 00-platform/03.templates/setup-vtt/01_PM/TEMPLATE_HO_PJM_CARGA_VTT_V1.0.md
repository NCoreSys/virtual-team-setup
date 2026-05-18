# TEMPLATE — HANDOFF PM → PJM · Carga Inicial a VTT

> **Cómo usar:**
> 1. Copiar a `01-PM/HO_PJM_CARGA_VTT_<<PROYECTO>>.md`
> 2. Reemplazar placeholders `<<...>>`
> 3. Validar que el script Python y el TASK_INDEX_SEED existan antes de emitir
> 4. Firmar como PM antes de entregar al PJM
> 5. Borrar este bloque antes de emitir

---

# HANDOFF PM → PJM — Carga Inicial a VTT · <<NOMBRE_PROYECTO>>

| Campo | Valor |
|-------|-------|
| **Documento** | HO_PJM_CARGA_VTT_<<PROYECTO>>.md |
| **Versión** | 1.0 |
| **Fecha** | <<YYYY-MM-DD>> |
| **De** | PM (<<Nombre>>) — `<<UUID_PM>>` |
| **Para** | PJM (Project Manager) — `<<UUID_PJM>>` |
| **Proyecto** | <<NOMBRE_PROYECTO>> |
| **Backend** | `<<API_URL>>` |
| **Estado** | ✅ APROBADO — Listo para ejecución |

---

## 1. OBJETIVO

Cargar desde cero en VTT toda la estructura del proyecto <<NOMBRE_PROYECTO>>:

- **1** Project
- **<<N>>** Phases
- **<<N>>** Deliveries
- **<<N>>** Tasks con metadata completa (assignee, priority, complexity, hours, category, description)
- **<<N>>** Task→Delivery assignments
- **<<N>>** Dependencies críticas

Todo en **una sola pasada** mediante script Python ejecutable.

---

## 2. CONTEXTO

Previo a este HO, el PM cerró la planificación:

| Docs PM cerrados | Versión | Estado |
|------------------|---------|--------|
| <<SPEC>> | <<vX.Y>> | ✅ Aprobado PM |
| <<Metodología>> | <<vX.Y>> | ✅ Vigente |
| <<Addendum(s)>> | <<vX.Y>> | ✅ Aprobado |
| FASES_APLICABLES_<<PROYECTO>>.md | X.0 | ✅ N deliverables aplicables |
| CONSOLIDADO_<<PROYECTO>>.md | X.0 | ✅ Plan maestro |
| CIERRE_PM_HANDOFF_PJM_<<PROYECTO>>.md | X.0 | ✅ HO operativo completo |
| TASK_INDEX_SEED_<<PROYECTO>>.md | X.0 | ✅ N tareas con todos los campos |

---

## 3. ENTREGABLE ADJUNTO

### 3.1 Script de ejecución

`<<PATH>>/scripts/create_<<proyecto>>_vtt.py`

**Qué hace:**

1. Autentica como PJM vía `POST /api/auth/service-token` → obtiene JWT.
2. `POST /api/projects` — crea el Project "<<NOMBRE>>" (sin wizard).
3. `POST /api/projects/{id}/phases` × **N** — crea las fases en orden.
4. `POST /api/deliveries` × **N** — crea los deliveries asociados a su fase.
5. `POST /api/phases/{phaseId}/tasks` × **N** — crea las tareas con metadata.
6. `POST /api/deliveries/{deliveryId}/tasks/{taskId}` × **N** — vincula task a delivery.
7. `POST /api/tasks/{id}/dependencies` × **N** — registra dependencias críticas.
8. Escribe `VTT_UUIDS_<<PROYECTO>>.json` con todos los UUIDs capturados.

---

## 4. PRERREQUISITOS ANTES DE EJECUTAR

### 4.1 Checklist

```
[ ] Python 3.8+ instalado en el entorno
[ ] Variable VTT_SERVICE_KEY exportada
[ ] Variable VTT_API_URL (default http://77.42.88.106:3000)
[ ] Conectividad al backend verificada (curl .../health)
[ ] Ningún proyecto previo "<<NOMBRE>>" en VTT
[ ] Los usuarios del proyecto ya existen (confirmar UUIDs)
[ ] Los catálogos Status y Priority tienen los UUIDs esperados
[ ] Rama git donde se ejecutará (para log)
```

### 4.2 Configuración del entorno

```bash
export VTT_SERVICE_KEY="<valor del PM>"
export VTT_API_URL="<<API_URL>>"

cd <<PATH>>/scripts/
python3 --version   # debe ser >= 3.8
```

---

## 5. PROCESO DE EJECUCIÓN

### 5.1 Ejecutar el script

```bash
cd <<PATH>>/scripts/
python3 create_<<proyecto>>_vtt.py | tee run_$(date +%Y%m%d_%H%M%S).log
```

### 5.2 Salida esperada

```
[HH:MM:SS] <<PROYECTO>> — VTT Creation Script
=== Paso 1: Crear Project ===
[HH:MM:SS] ✓ Project creado: <uuid>
=== Paso 2: Crear N Phases ===
... (N líneas)
=== Paso 3: Crear N Deliveries ===
... (N líneas)
=== Paso 4: Crear N Tasks ===
... (N líneas)
=== Paso 6: Crear N Dependencies ===
... (N líneas)
✅ Completado. UUIDs guardados en VTT_UUIDS_<<PROYECTO>>.json
```

### 5.3 Artefacto de salida

**`VTT_UUIDS_<<PROYECTO>>.json`** — source of truth post-creación:

```json
{
  "projectId": "<uuid>",
  "phases": { "<<Fase 1>>": "<uuid>", ... },
  "deliveries": { "<<Delivery 1>>": "<uuid>", ... },
  "tasks": { "<<MEM-001>>": "<uuid>", ... }
}
```

---

## 6. VERIFICACIÓN POST-EJECUCIÓN

### 6.1 Checks automáticos

```bash
# Verificar project existe
curl -s "<<API_URL>>/api/projects/$(jq -r .projectId VTT_UUIDS_<<PROYECTO>>.json)" \
  -H "Authorization: Bearer $TOKEN" | jq .data.name

# Contar tareas del proyecto (esperado: <<N>>)
curl -s "<<API_URL>>/api/tasks?projectId=$(jq -r .projectId VTT_UUIDS_<<PROYECTO>>.json)" \
  -H "Authorization: Bearer $TOKEN" | jq 'length'

# Contar fases (esperado: <<N>>)
curl -s "<<API_URL>>/api/projects/$(jq -r .projectId VTT_UUIDS_<<PROYECTO>>.json)/phases" \
  -H "Authorization: Bearer $TOKEN" | jq 'length'
```

### 6.2 Checklist manual

```
[ ] VTT_UUIDS_<<PROYECTO>>.json generado sin entradas vacías
[ ] GET project retorna nombre correcto
[ ] GET project/phases retorna N fases con orden 1..N
[ ] GET tasks retorna N tareas
[ ] Tareas críticas con priorityId correcto (ver §15 CIERRE_PM)
[ ] Dependencias críticas registradas (verificar con GET /api/tasks/{id}/dependencies)
[ ] Todas las tareas con description no vacía
[ ] Sin warnings de "⚠" en el log (o si los hay, documentar)
```

### 6.3 Si hay fallos

| Error | Diagnóstico | Acción |
|-------|-------------|--------|
| `401 UNAUTHORIZED` | SERVICE_KEY inválida | Confirmar con PM |
| `400 VALIDATION_ERROR` | Campo mal formateado | Revisar seed |
| `409 PHASE_ORDER_CONFLICT` | Fase con order duplicado | Revisar script |
| `409 delivery→task` | Task y delivery en fases distintas (RN-010) | Revisar agrupación |
| `404` en dependencia | Task referenciada no existe | Verificar orden de Paso 4 |

### 6.4 Rollback / Reintento

**Opción A — Completar manualmente:**
1. Revisar JSON parcial (si existe)
2. Ejecutar POSTs faltantes con curl
3. Completar JSON

**Opción B — Limpiar y reintentar (si falla al inicio):**
1. `DELETE /api/projects/{projectId}` (cascade)
2. Borrar JSON
3. Reejecutar script

**Opción C — Reanudar (si falla en Paso 4+):**
1. Comentar pasos ya completados en script
2. Cargar JSON parcial
3. Continuar desde el paso que falló

---

## 7. ACCIONES POST-CARGA

1. **Commit `VTT_UUIDS_<<PROYECTO>>.json` al repo**
2. **Notificar al PM** con log + JSON
3. **PM ejecuta kickoff call** y emite `HO_FASE_0_<<PROYECTO>>.md`
4. **PJM comunica a cada rol activo** sus tareas asignadas
5. **BRIEFs y ASSIGNMENTs** se generan en dinámica de cada fase

### 7.1 Dónde guardar los UUIDs capturados

- **Recomendado:** commit al repo + actualizar OPERATIVOs con UUIDs reales de Project/Phases

---

## 8. ESCALACIÓN

| Bloqueo | Escalar a |
|---------|-----------|
| Auth falla / SERVICE_KEY inválida | PM |
| Catálogo Status/Priority sin UUIDs esperados | DO + PM |
| Backend VTT caído / timeout recurrente | DO (Admin VM) |
| Validación Zod rechaza campos | TL + PM |
| Endpoint de dependencias no existe | PM (registrar manualmente en issue) |

---

## 9. CRITERIO DE ÉXITO

La carga se considera **COMPLETADA** cuando:

1. ✅ `VTT_UUIDS_<<PROYECTO>>.json` existe con todos los UUIDs
2. ✅ Log de ejecución sin errores críticos
3. ✅ Checklist manual del §6.2 completo
4. ✅ PM recibe notificación del PJM con resumen + log
5. ✅ PM aprueba sign-off (§10)

---

## 10. FIRMAS

| Rol | Nombre | Firma | Fecha |
|-----|--------|-------|-------|
| **PM (emite)** | <<Nombre>> | ✅ APROBADO | <<YYYY-MM-DD>> |
| **PJM (recibe y ejecuta)** | <<Nombre>> | ⬜ Pendiente | — |
| **PJM (reporta carga exitosa)** | <<Nombre>> | ⬜ Pendiente | — |
| **PM (sign-off post-carga)** | <<Nombre>> | ⬜ Pendiente | — |

---

## 11. REFERENCIAS

**Documentos de insumo:**
- `TASK_INDEX_SEED_<<PROYECTO>>.md` — fuente de datos del script
- `PROCESO_ASIGNACION_TAREAS.md` — definición de endpoints VTT
- `CIERRE_PM_HANDOFF_PJM_<<PROYECTO>>.md` — HO operativo general
- `.claude/rules/Proyect_data.md` — UUIDs reales de usuarios

**Script ejecutable:**
- `<<PATH>>/scripts/create_<<proyecto>>_vtt.py`

**Salida esperada:**
- `<<PATH>>/scripts/VTT_UUIDS_<<PROYECTO>>.json`
- `<<PATH>>/scripts/run_YYYYMMDD_HHMMSS.log`

---

**Documento:** HO_PJM_CARGA_VTT_<<PROYECTO>>.md
**Versión:** 1.0
**Estado:** ✅ APROBADO — Listo para ejecución PJM
**Fecha:** <<YYYY-MM-DD>>

---

**PM — <<Nombre>>**

---

**Template source:** `TEMPLATE_HO_PJM_CARGA_VTT_V1.0.md`
**Proceso asociado:** `09_PROCESO_CIERRE_PM_HANDOFF_PJM.md` (paso 9)
