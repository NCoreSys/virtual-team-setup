# HANDOFF PM → PJM — Carga Inicial a VTT · Memory Service

| Campo | Valor |
|-------|-------|
| **Documento** | HO_PJM_CARGA_VTT_MEMORY_SERVICE.md |
| **Versión** | 1.0 |
| **Fecha** | 2026-04-22 |
| **De** | PM (Martin Rivas) — `350831b2-e1ae-4dbe-b2eb-7e023ec2e103` |
| **Para** | PJM (Project Manager) — `0ff63a29-0bc0-465a-b9bd-5f71476bc91d` |
| **Proyecto** | Memory Service |
| **Backend** | `http://77.42.88.106:3000` |
| **Estado** | ✅ APROBADO — Listo para ejecución |

---

## 1. OBJETIVO

Cargar desde cero en VTT toda la estructura del proyecto Memory Service:

- **1** Project
- **10** Phases
- **65** Deliveries
- **116** Tasks con metadata completa (assignee, priority, complexity, hours, category, description)
- **116** Task→Delivery assignments
- **15** Dependencies críticas

Todo en **una sola pasada** mediante script Python ejecutable.

---

## 2. CONTEXTO

Este HO cierra la planificación PM y habilita el kickoff operativo. Previo a este momento:

| Docs PM cerrados | Versión | Estado |
|------------------|---------|--------|
| SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md | 1.9 | ✅ Aprobado PM |
| METODOLOGIA_MEMORY_SERVICE_v1.2.md | 1.1 | ✅ Vigente |
| ADDENDUM_INTEGRACION_MEMORY_SERVICE_v1.1.md | 1.1 | ✅ Aprobado |
| FASES_APLICABLES_MEMORY_SERVICE.md | 2.0 | ✅ 390 deliverables aplicables |
| CONSOLIDADO_MEMORY_SERVICE_R1.md | 1.0 | ✅ Plan maestro |
| CIERRE_PM_HANDOFF_PJM_MEMORY_SERVICE_R1.md | 1.0 | ✅ HO operativo completo |
| TASK_INDEX_SEED_MEMORY_SERVICE.md | 2.1 | ✅ 140 tareas con todos los campos |

---

## 3. ENTREGABLE ADJUNTO

### 3.1 Script de ejecución

`memory-service-project/Release2.0/scripts/create_memory_service_vtt.py`

**Qué hace:**

1. Autentica como PJM vía `POST /api/auth/service-token` → obtiene JWT.
2. `POST /api/projects` — crea el Project "Memory Service" (sin wizard).
3. `POST /api/projects/{id}/phases` × **10** — crea las fases en orden.
4. `POST /api/deliveries` × **65** — crea los deliveries asociados a su fase.
5. `POST /api/phases/{phaseId}/tasks` × **116** — crea las tareas con: `title`, `description`, `priorityId`, `statusId`, `assignedToId`, `assignedBy`, `category`, `complexity`, `estimatedHours`, `createdBy`.
6. `POST /api/deliveries/{deliveryId}/tasks/{taskId}` × **116** — vincula cada tarea a su delivery.
7. `POST /api/tasks/{id}/dependencies` × **15** — registra las dependencias críticas.
8. Escribe `VTT_UUIDS_MEMORY_SERVICE.json` con todos los UUIDs capturados.

**Origen de datos:** el script es la materialización directa de `TASK_INDEX_SEED_MEMORY_SERVICE.md v2.1` (§2 referencias y §4 índice de tareas).

---

## 4. PRERREQUISITOS ANTES DE EJECUTAR

### 4.1 Checklist

```
[ ] Python 3.8+ instalado en el entorno de ejecución
[ ] Variable de entorno VTT_SERVICE_KEY exportada
[ ] Variable de entorno VTT_API_URL definida (default http://77.42.88.106:3000)
[ ] Conectividad al backend verificada (`curl http://77.42.88.106:3000/health`)
[ ] Ningún proyecto previo "Memory Service" en VTT (validar con GET /api/projects)
[ ] Los 12 + 4 usuarios del proyecto ya existen (confirmado por PM el 2026-04-22)
[ ] Los catálogos globales Status y Priority tienen los UUIDs del §2 del seed
[ ] Rama git donde se ejecutará el script (para registro del log)
```

### 4.2 Configuración del entorno

```bash
export VTT_SERVICE_KEY="<valor provisto por PM>"
export VTT_API_URL="http://77.42.88.106:3000"

cd memory-service-project/Release2.0/scripts/
python3 --version   # debe ser >= 3.8
```

---

## 5. PROCESO DE EJECUCIÓN

### 5.1 Ejecutar el script

```bash
cd memory-service-project/Release2.0/scripts/
python3 create_memory_service_vtt.py | tee run_$(date +%Y%m%d_%H%M%S).log
```

El script imprime cada paso en consola con timestamp. Si algún POST falla, se imprime el código HTTP + detalle del error y se aborta (excepto las asignaciones task↔delivery y las dependencias, que solo imprimen warning).

### 5.2 Salida esperada (resumen)

```
[HH:MM:SS] Memory Service — VTT Creation Script
[HH:MM:SS] API: http://77.42.88.106:3000
[HH:MM:SS] Ejecutado por PJM: 0ff63a29-0bc0-465a-b9bd-5f71476bc91d
[HH:MM:SS] ✓ Token JWT obtenido

=== Paso 1: Crear Project ===
[HH:MM:SS] ✓ Project creado: <uuid> — 'Memory Service'

=== Paso 2: Crear 10 Phases ===
[HH:MM:SS]   ✓ Phase  1. Project Setup: <uuid>
[HH:MM:SS]   ✓ Phase  2. Discovery: <uuid>
... (10 líneas)

=== Paso 3: Crear 65 Deliveries ===
[HH:MM:SS]   ✓ [Project Setup] Project Foundation Ready: <uuid>
... (65 líneas)

=== Paso 4: Crear 116 Tasks ===
[HH:MM:SS]   ✓ MEM-001 [DO 4h MEDIUM] Infra Setup -> <uuid>
... (116 líneas)

=== Paso 6: Crear 15 Dependencies criticas ===
[HH:MM:SS]   ✓ MEM-006 depende de MEM-005 (Discovery despues de Kickoff)
... (15 líneas)

✅ Completado. UUIDs guardados en VTT_UUIDS_MEMORY_SERVICE.json
   Project:    1 creado
   Phases:     10 creadas
   Deliveries: 65 creados
   Tasks:      116 creadas
   Deps:       15 procesadas
```

### 5.3 Artefacto de salida

**`VTT_UUIDS_MEMORY_SERVICE.json`** — source of truth para todas las operaciones posteriores:

```json
{
  "projectId": "<uuid>",
  "phases": {
    "Project Setup": "<uuid>",
    "Discovery": "<uuid>",
    ...
  },
  "deliveries": {
    "Project Foundation Ready": "<uuid>",
    "Problem Definition": "<uuid>",
    ...
  },
  "tasks": {
    "MEM-001": "<uuid>",
    "MEM-002": "<uuid>",
    ...
  }
}
```

---

## 6. VERIFICACIÓN POST-EJECUCIÓN

### 6.1 Checks automáticos (ejecutar tras el script)

```bash
# Verificar project existe
curl -s "http://77.42.88.106:3000/api/projects/$(jq -r .projectId VTT_UUIDS_MEMORY_SERVICE.json)" \
  -H "Authorization: Bearer $TOKEN" | jq .data.name
# → "Memory Service"

# Contar tareas del proyecto
curl -s "http://77.42.88.106:3000/api/tasks?projectId=$(jq -r .projectId VTT_UUIDS_MEMORY_SERVICE.json)" \
  -H "Authorization: Bearer $TOKEN" | jq 'length'
# → 116

# Contar fases
curl -s "http://77.42.88.106:3000/api/projects/$(jq -r .projectId VTT_UUIDS_MEMORY_SERVICE.json)/phases" \
  -H "Authorization: Bearer $TOKEN" | jq 'length'
# → 10
```

### 6.2 Checklist manual

```
[ ] VTT_UUIDS_MEMORY_SERVICE.json generado sin entradas vacías
[ ] GET project retorna nombre "Memory Service" y código "MEM"
[ ] GET project/phases retorna 10 fases con orden 1..10
[ ] GET tasks?projectId=... retorna 116 tareas
[ ] Una tarea de muestra (MEM-038 Design Handoff Final) tiene priorityId = critical
[ ] Una tarea de muestra (MEM-059 GET /context) tiene priorityId = critical
[ ] Una tarea de muestra (MEM-005 Project Kickoff) tiene priorityId = high
[ ] MEM-081 depende de MEM-038 (verificar con GET /api/tasks/{id}/dependencies)
[ ] Todas las tareas tienen description no vacía (< 2000 chars por la restricción Zod)
[ ] No hay warnings de "⚠" en el log (o si los hay, registrar para resolver manualmente)
```

### 6.3 Si hay fallos

| Error | Diagnóstico | Acción |
|-------|-------------|--------|
| `401 UNAUTHORIZED` en auth | `VTT_SERVICE_KEY` inválida | Confirmar clave con PM |
| `400 VALIDATION_ERROR` en POST task | Campo mal formateado (ej. `complexity: "medium"` en vez de `"MEDIUM"`) | Revisar script — el seed ya usa MAYÚSCULAS |
| `409 PHASE_ORDER_CONFLICT` | Fase con order duplicado | No debería ocurrir — cada fase tiene order único 1..10 |
| `409 en delivery→task` | Task y delivery en fases distintas (RN-010) | No debería ocurrir — el script respeta agrupación |
| `404` en create dependency | El task referenciado no existe aún | Verificar que el POST de tasks se completó antes |
| Script se detiene a mitad | Parcialmente cargado | Ver §6.4 Rollback / Reintento |

### 6.4 Rollback / Reintento

**Si el script falla a mitad de la carga**, hay 3 opciones:

**Opción A — Completar manualmente:**
1. Revisar `VTT_UUIDS_MEMORY_SERVICE.json` parcial (si existe).
2. Ejecutar POSTs faltantes manualmente con `curl`.
3. Completar el JSON con los UUIDs obtenidos.

**Opción B — Limpiar y reintentar (recomendado si falla al inicio):**
1. Si el Project ya se creó: `DELETE /api/projects/{projectId}` (elimina cascade).
2. Borrar `VTT_UUIDS_MEMORY_SERVICE.json`.
3. Volver a ejecutar el script desde el principio.

**Opción C — Reanudar (si falla en Paso 4 o posterior):**
1. Modificar el script comentando los pasos ya completados.
2. Cargar el `VTT_UUIDS_MEMORY_SERVICE.json` parcial al inicio.
3. Continuar desde el paso que falló.

---

## 7. ACCIONES POST-CARGA

Una vez completada la carga exitosa:

1. **Commit `VTT_UUIDS_MEMORY_SERVICE.json` al repo** (o registrar UUIDs en doc separado — ver §7.1).
2. **Notificar al PM** con el log de ejecución y el JSON resultante.
3. **PM ejecuta kickoff call** y emite `HO_FASE_0_DISCOVERY_MEMORY_SERVICE.md` (primer HO de fase).
4. **PJM comunica a cada rol activo** de Fase 0 (SA, PM) sus tareas asignadas.
5. **Los BRIEFs y ASSIGNMENTs** se generan en la dinámica de cada fase (no al momento de la carga).

### 7.1 Dónde guardar los UUIDs capturados

Opciones aceptables:

- **Opción 1 (recomendada):** commit al repo en `memory-service-project/Release2.0/scripts/VTT_UUIDS_MEMORY_SERVICE.json`.
- **Opción 2:** actualizar `OPERATIVO_PM_MEMORY-SERVICE.md` y `OPERATIVO_TECH_LEAD.md` con los UUIDs reales de Project/Phases capturados.
- **Opción 3:** ambas (JSON + sincronizar OPERATIVOs).

PM recomienda **Opción 3** para trazabilidad.

---

## 8. ESCALACIÓN

Si el PJM encuentra un bloqueo durante la ejecución:

| Bloqueo | Escalar a |
|---------|-----------|
| Auth falla / SERVICE_KEY inválida | PM (Martin Rivas) |
| Catálogo Status o Priority no tiene los UUIDs esperados | DO + PM |
| Backend VTT caído / timeout recurrente | DO (Admin VM) |
| Validación Zod rechaza campos que el script envía | TL + PM (revisar script + seed) |
| Endpoint de dependencias no existe | PM (registrar dependencias manualmente en issue) |

---

## 9. CRITERIO DE ÉXITO

La carga se considera **COMPLETADA** cuando:

1. ✅ `VTT_UUIDS_MEMORY_SERVICE.json` existe con: 1 projectId + 10 phaseIds + 65 deliveryIds + 116 taskIds
2. ✅ Log de ejecución sin errores críticos (warnings en deps/delivery-task son aceptables si se documentan)
3. ✅ Checklist manual del §6.2 completo
4. ✅ PM recibe notificación del PJM con resumen + log
5. ✅ PM aprueba sign-off en este documento (§10)

---

## 10. FIRMAS

| Rol | Nombre | Firma | Fecha |
|-----|--------|-------|-------|
| **PM (emite)** | Martin Rivas | ✅ APROBADO | 2026-04-22 |
| **PJM (recibe y ejecuta)** | Project Manager | ⬜ Pendiente ejecución | — |
| **PJM (reporta carga exitosa)** | Project Manager | ⬜ Pendiente | — |
| **PM (sign-off post-carga)** | Martin Rivas | ⬜ Pendiente | — |

---

## 11. REFERENCIAS

**Documentos de insumo:**

- `TASK_INDEX_SEED_MEMORY_SERVICE.md` v2.1 — fuente de los datos del script
- `PROCESO_ASIGNACION_TAREAS.md` v1.6 — definición de endpoints + reglas (assignedToId, complexity MAYÚSCULAS, etc.)
- `CIERRE_PM_HANDOFF_PJM_MEMORY_SERVICE_R1.md` v1.0 — HO operativo general (contexto del proyecto)
- `.claude/rules/Proyect_data.md` — UUIDs reales de usuarios Memory Service

**Script ejecutable:**

- `memory-service-project/Release2.0/scripts/create_memory_service_vtt.py`

**Salida esperada:**

- `memory-service-project/Release2.0/scripts/VTT_UUIDS_MEMORY_SERVICE.json` (generado tras ejecución)
- `memory-service-project/Release2.0/scripts/run_YYYYMMDD_HHMMSS.log` (log de ejecución)

---

**Documento:** HO_PJM_CARGA_VTT_MEMORY_SERVICE.md  
**Versión:** 1.0  
**Estado:** ✅ APROBADO — Listo para ejecución PJM  
**Fecha:** 2026-04-22  

---

**PM — Martin Rivas**  
CEO/Founder — Virtual Teams Tracking
