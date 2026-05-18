# BUG REPORT: VTT API no permite reordenar fases existentes

**De:** PM / PJM Memory Service
**Para:** Backend Team VTT
**Fecha:** 2026-04-20
**Prioridad:** P1 (bloquea reorganizacion de fases SDLC en proyectos existentes)
**Ambiente:** http://77.42.88.106:3000
**Proyecto afectado:** Memory Service (a56a76e6-29bf-401e-a8ec-091882e383f7)

---

## 1. RESUMEN EJECUTIVO

El API de VTT **no permite cambiar el campo `order` de una fase despues de creada**. Los endpoints `PUT /api/phases/{id}` y `PATCH /api/projects/{id}/phases/{id}` responden **200 OK pero silenciosamente ignoran el cambio**, devolviendo el `order` original sin actualizarlo. No existe endpoint dedicado para reordenar (`/phases/reorder` retorna 404).

Esto impide insertar una fase nueva en cualquier posicion distinta de la ultima, y obliga a un workaround de colision de `order` (dos fases con el mismo numero) o rollback manual.

---

## 2. CONTEXTO DE USO

El proyecto Memory Service ya tiene 9 fases SDLC creadas (Discovery → Operations, order 1 a 9) con 68 deliverables asociados.

Se identifico la necesidad de agregar una fase **"Project Setup"** al inicio (order=1) para registrar tareas de bootstrap del repositorio (estructura de carpetas, TASK_TRACKING, templates, docker-compose base).

La operacion logica seria:
1. Shift de las 9 fases existentes +1 posicion (Discovery 1→2, Planning 2→3, ..., Operations 9→10)
2. Crear "Project Setup" con order=1

El paso 1 **no es posible** con la API actual.

---

## 3. EVIDENCIA — PRUEBAS DE API REALIZADAS

### 3.1 PUT con cambio de order — devuelve 200 pero NO actualiza

Request:
```
PUT /api/phases/e4e85063-4574-402f-8a93-9fca395b3133   (Operations, order actual=9)
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Operations",
  "description": "",
  "order": 10
}
```

Response: `200 OK`
```json
{
  "success": true,
  "data": {
    "id": "e4e85063-4574-402f-8a93-9fca395b3133",
    "name": "Operations",
    "order": 9,    // <-- NO actualizado
    ...
  }
}
```

**Re-GET confirma:** `order` sigue en 9.

Se repitio con las 9 fases del proyecto, todas respondieron 200 pero ninguna cambio su order.

### 3.2 PATCH /api/phases/{id} — 404

```
PATCH /api/phases/{id}     -> 404 NOT_FOUND
```

### 3.3 PATCH /api/projects/{projectId}/phases/{id} — mismo problema que PUT

```
PATCH /api/projects/a56.../phases/e4e8...
{ "order": 11 }

Response: 200 OK, pero order en respuesta = 9 (sin cambio)
```

### 3.4 Endpoints de reorder probados — todos 404

| Metodo | Path | Status |
|--------|------|--------|
| POST | /api/phases/reorder | 404 |
| PUT  | /api/phases/reorder | 400 (ruteado como `/api/phases/{id}` con id=`reorder`) |
| POST | /api/projects/{id}/reorder-phases | 404 |
| PUT  | /api/projects/{id}/phases | 404 |
| POST | /api/projects/{id}/phases/order | 404 |
| POST | /api/projects/{id}/phases/{id}/move | 404 |
| POST | /api/phases/{id}/move | 404 |
| POST | /api/phases/{id}/reorder | 404 |

### 3.5 POST /api/projects/{id}/phases con order=0 — rechazado

```json
{
  "error": "Validation error",
  "details": [{
    "code": "too_small",
    "minimum": 0,
    "inclusive": false,
    "message": "Order must be a positive integer"
  }]
}
```

El `order` debe ser entero positivo (>= 1). No se puede insertar "al inicio" usando order=0.

### 3.6 POST /api/projects/{id}/phases con order=1 — SI permite duplicados

```
POST /api/projects/a56.../phases
{ "name": "Project Setup", "order": 1 }

Response: 201 Created
```

**La API acepta crear una fase con el mismo `order` que otra fase existente**, dejando dos fases en order=1 sin validacion de unicidad.

---

## 4. ESTADO RESULTANTE EN EL PROYECTO

Tras la prueba quedaron en el proyecto Memory Service dos fases en order=1:

| order | Fase | ID |
|-------|------|-----|
| 1 | Discovery | bc86125e-7957-40e2-97e5-39dfff941088 |
| 1 | **Project Setup (NUEVA)** | 8b290c8e-896b-4f24-be27-31c1613fd2ea |
| 2 | Planning | c37881ba-6c05-42c4-b674-9512f5e9d493 |
| 3 | Analysis | 48bdc798-e1f2-4e02-8267-2ab073bf79ca |
| 4 | Design UX/UI | 340df4ef-24ae-4d65-96ce-45ccaea1e042 |
| 5 | Design Technical | 4e10b5bd-8021-49ab-ad78-e1763ee791de |
| 6 | Development | 7e003478-cd98-4953-ae79-676e864fb1f8 |
| 7 | Testing | 2b619b6b-f017-4194-858c-55806074881f |
| 8 | Deploy | cce5eaf6-58d6-4168-bded-336316ea2faa |
| 9 | Operations | e4e85063-4574-402f-8a93-9fca395b3133 |

Bajo Project Setup hay 5 deliverables creados (MEM-069 a MEM-073) que tambien quedan huerfanos si se borra la fase.

---

## 5. IMPACTO

- **Funcional:** cualquier proyecto que requiera insertar fases intermedias o iniciales queda bloqueado
- **UX VTT:** la UI debera decidir arbitrariamente como ordenar fases con el mismo `order` (alfabetico, fecha de creacion, random)
- **Integridad SDLC:** no se puede hacer el shift estandar cuando se agrega una fase nueva, provocando colisiones
- **Data:** actualmente hay 2 fases colisionadas en Memory Service, imposible resolver sin endpoint o sin borrar una

---

## 6. SOLUCION SOLICITADA

Necesitamos **una** de las siguientes opciones (en orden de preferencia):

### Opcion A (preferida): endpoint de reordenamiento batch

```
PUT /api/projects/{projectId}/phases/reorder
Authorization: Bearer {token}
Content-Type: application/json

{
  "phases": [
    { "id": "uuid-1", "order": 1 },
    { "id": "uuid-2", "order": 2 },
    ...
  ]
}
```

- Valida que todos los `id` pertenezcan al proyecto
- Valida que los `order` sean unicos en el conjunto
- Ejecuta la actualizacion en transaccion atomica
- Retorna lista actualizada ordenada

### Opcion B: permitir cambio de order via PUT/PATCH

Hacer que `PUT /api/phases/{id}` y/o `PATCH /api/projects/{id}/phases/{id}` **si acepten** el campo `order` y lo persistan.
- Opcional: al recibir un order duplicado, shiftear automaticamente las demas fases (comportamiento tipo "drag and drop")

### Opcion C: validar unicidad de order al crear

Como minimo, `POST /api/projects/{id}/phases` debe validar que el `order` no exista ya en el proyecto, y rechazar con 409 CONFLICT. Asi evitamos crear colisiones silenciosas.

---

## 7. CLEANUP REQUERIDO EN MEMORY SERVICE

Mientras se resuelve el bug, necesitamos que el backend (o la via administrativa) ejecute UNA de estas acciones sobre el proyecto `a56a76e6-29bf-401e-a8ec-091882e383f7`:

**Accion A (preferida):** shift manual via SQL/consola
```sql
UPDATE phases SET "order" = "order" + 1
WHERE "projectId" = 'a56a76e6-29bf-401e-a8ec-091882e383f7'
  AND id != '8b290c8e-896b-4f24-be27-31c1613fd2ea';
-- resultado: Discovery=2, Planning=3, ..., Operations=10, Project Setup=1
```

**Accion B (rollback):** eliminar Project Setup y sus tareas
```sql
DELETE FROM tasks WHERE "phaseId" = '8b290c8e-896b-4f24-be27-31c1613fd2ea';
DELETE FROM phases WHERE id = '8b290c8e-896b-4f24-be27-31c1613fd2ea';
```

Si no hay acceso admin disponible rapido, procedemos con Accion B via API (DELETE de las 5 tareas + DELETE de la fase) y movemos las 5 tareas bootstrap a Phase 1 Planning.

---

## 8. INFORMACION DE SOPORTE

- **Scripts de reproduccion:** `memory-service/validate_phase_reorder.py`, `debug_put_phase.py`, `try_reorder_endpoints.py`
- **Credenciales de prueba:** PJM userId `0ff63a29-0bc0-465a-b9bd-5f71476bc91d` + serviceKey
- **Project ID afectado:** a56a76e6-29bf-401e-a8ec-091882e383f7
- **Fase nueva problematica:** 8b290c8e-896b-4f24-be27-31c1613fd2ea
- **Contacto:** Martin Rivas — martin.rivas@prompt-ai.studio

---

**Estado:** Esperando decision de backend VTT
**Accion en espera:** cleanup de fases colisionadas + implementacion de reorder endpoint
