# DOC-SEC-03 — Arquitectura de Implementación de Autorización (Bloque 1)

**Proyecto:** VTT → HybridFlow  
**Versión:** 1.0  
**Estado:** Base para implementación  
**Objetivo:** Definir la arquitectura backend concreta para implementar autenticación, autorización, scopes, políticas contextuales y trazabilidad en Bloque 1, con flujo exacto por request y listado de componentes a desarrollar o ajustar.

---

## 1. Propósito del documento

Este documento convierte el modelo de seguridad y las políticas de permisos en una arquitectura de implementación operativa.

Su función es definir:

- qué componentes backend deben existir
- qué hace cada middleware
- en qué orden corre cada capa
- cómo se resuelve el scope real del recurso
- cómo se combinan auth, RBAC y ABAC
- qué endpoints críticos deben ajustarse
- qué parte pertenece realmente a Bloque 1 y qué parte queda preparada para evolución futura

---

## 2. Objetivo técnico de Bloque 1

Bloque 1 debe lograr que toda ruta crítica del sistema deje de depender de bypass y quede protegida por un flujo consistente de autorización.

El objetivo no es solamente “poner token” o “agregar requireCapability”. El objetivo real es este:

> **Todo request sensible debe validarse contra la identidad del actor, su scope organizacional, su rol efectivo, la capability requerida y la política contextual del recurso.**

---

## 3. Arquitectura objetivo de Bloque 1

La arquitectura ejecutable de Bloque 1 queda compuesta por cinco capas:

1. **Autenticación**
2. **Resolución de contexto de autorización**
3. **RBAC base**
4. **Policy / ABAC mínimo**
5. **Auditoría de decisiones sensibles**

Representación resumida:

```text
Request
  → authenticate
  → resolveAuthorizationContext
  → requireCapability
  → requirePolicy
  → controller
  → service
  → persistence / side effects
  → auditDecision
  → response
```

---

## 4. Componentes backend obligatorios

## 4.1 Middleware `authenticate`

### Responsabilidad
Validar el token recibido y convertirlo en una identidad técnica utilizable por el backend.

### Inputs esperados
- `Authorization: Bearer <access_token>`
- `Authorization: Bearer <service_token>`

### Tokens aceptados
- `type = access`
- `type = service`

### Tokens no válidos para rutas de negocio
- `type = refresh`

### Salida requerida en request

```ts
req.auth = {
  userId: string,
  tokenType: 'access' | 'service',
  email: string,
  role: string | null,
  platformRole: string | null,
  orgId: string | null
}
```

### Notas de implementación
- La verificación del JWT debe ser uniforme.
- El `tokenType` debe sobrevivir hasta la policy layer.
- No se debe asumir que un `service token` tiene el mismo comportamiento que un `access token`.

---

## 4.2 Middleware `resolveAuthorizationContext`

### Responsabilidad
Resolver el scope real del request.

Este middleware es la pieza que evita el Frankenstein. Sin él, la autorización queda amarrada a la ruta, no al recurso.

### Qué debe resolver
Según el endpoint, debe poblar:

```ts
req.authz = {
  organizationId: string | null,
  workspaceId: string | null,
  projectId: string | null,
  resourceType: string,
  resourceId: string | null,
  resourceOwnerId: string | null,
  assignedUserId: string | null,
  completedBy: string | null,
  requestedBy: string | null,
  status: string | null
}
```

### Regla técnica obligatoria
Toda ruta protegida debe poder resolver su recurso hasta `workspaceId` y `organizationId`.

### Ejemplos de resolución

#### `PATCH /tasks/:id`
- `taskId` → `Task`
- `Task.projectId` → `Project`
- `Project.workspaceId` → `Workspace`
- `Workspace.organizationId` → `Organization`

#### `POST /approval-signatures/:id/approve`
- `approvalSignatureId` → `ApprovalSignature`
- `ApprovalSignature.approvalRequestId` → `ApprovalRequest`
- `ApprovalRequest.changeRequestId` → `ChangeRequest`
- `ChangeRequest.projectId` → `Project`
- `Project.workspaceId` → `Workspace`
- `Workspace.organizationId` → `Organization`

#### `POST /change-requests/:id/submit`
- `changeRequestId` → `ChangeRequest`
- `ChangeRequest.projectId` → `Project`
- `Project.workspaceId` → `Workspace`
- `Workspace.organizationId` → `Organization`

### Nota de diseño
Este middleware puede ser genérico con resolvers por tipo de recurso, o puede exponerse como helpers específicos por módulo. Lo importante es que el resultado sea uniforme.

---

## 4.3 Servicio `permissions.service`

### Responsabilidad
Resolver autorización base por roles y capabilities.

### Entradas
- `userId`
- `capabilityCode`
- `organizationId`
- `workspaceId`

### Responsabilidad mínima
Debe evaluar, en este orden:

1. `platformRole` si aplica
2. privilegio organizacional (`org_owner`, `org_admin`)
3. membresía en workspace (`WorkspaceMember`)
4. `RoleCapability`

### Restricción importante
No debe devolver `true` solo porque el usuario tenga la capability en *algún* workspace. Debe evaluar contra el **workspace del recurso actual**.

### Ajuste requerido
El comportamiento descrito en el material previo recorre memberships y aprueba si encuentra la capability en cualquiera. Eso debe corregirse en Bloque 1.

---

## 4.4 Servicio `policy.service` o `contextual-permissions.service`

### Responsabilidad
Implementar ABAC mínimo y reglas de negocio.

### Policies mínimas requeridas

- `canReadWorkspaceResource()`
- `canUpdateTask()`
- `canTransitionTask()`
- `canApproveTask()`
- `canSubmitChangeRequest()`
- `canApproveSignature()`
- `canManageUsers()`
- `canExecuteImport()`

### Regla de arquitectura
Las reglas críticas de negocio **no** deben quedar escondidas dentro del controller ni distribuidas por servicios sin patrón. Deben vivir en una capa explícita de policy.

---

## 4.5 `auditDecision` / auditoría de seguridad

### Responsabilidad
Registrar decisiones sensibles de autorización.

### Qué eventos debe dejar
- actor
- tipo de token
- capability evaluada
- policy aplicada
- recurso
- resultado (`allowed` / `denied`)
- razón resumida
- timestamp

### Casos mínimos a auditar
- aprobaciones
- rechazos
- firmas
- denegaciones por policy crítica
- cambios de estado sensibles
- importaciones
- gestión de usuarios

---

## 5. Flujo exacto por request

## 5.1 Flujo general estándar

### Paso 1 — Autenticación
`authenticate`

Valida el JWT y genera `req.auth`.

### Paso 2 — Contexto
`resolveAuthorizationContext`

Resuelve el recurso y su scope real.

### Paso 3 — Capability
`requireCapability(capabilityCode)`

Valida permiso general RBAC.

### Paso 4 — Policy
`requirePolicy(policyName)`

Valida ABAC y reglas de negocio.

### Paso 5 — Controller
El controller solo orquesta input/output, no decide seguridad de negocio compleja.

### Paso 6 — Service
Ejecuta la operación de negocio.

### Paso 7 — Auditoría
Se registra la decisión o evento sensible.

---

## 5.2 Flujos concretos por endpoint crítico

## Caso A — Leer tarea

### Endpoint
`GET /api/tasks/:id`

### Cadena
1. `authenticate`
2. `resolveAuthorizationContext(task)`
3. `requireCapability('tasks.read')`
4. `requirePolicy('canReadWorkspaceResource')`
5. controller → service → DB

### Resultado esperado
Solo actores con lectura válida en el workspace del recurso.

---

## Caso B — Actualizar tarea

### Endpoint
`PATCH /api/tasks/:id`

### Cadena
1. `authenticate`
2. `resolveAuthorizationContext(task)`
3. `requireCapability('tasks.update')`
4. `requirePolicy('canUpdateTask')`
5. controller → service → DB

### Reglas mínimas de policy
- developer solo si está asignado
- reviewer solo si está dentro de su scope de revisión
- analyst / observer no actualiza

---

## Caso C — Cambiar estado de tarea

### Endpoint
`PATCH /api/tasks/:id/status`

### Cadena
1. `authenticate`
2. `resolveAuthorizationContext(task)`
3. selección dinámica de capability:
   - si `toStatus !== approved` → `tasks.status`
   - si `toStatus === approved` → `tasks.approve`
4. `requirePolicy('canTransitionTask')`
5. controller → lifecycle service → DB
6. audit

### Reglas mínimas
- developer puede mover solo estados operativos definidos
- reviewer puede mover a `completed` según regla vigente
- TL/Lead hasta `completed`
- `approved` solo humano con autorización válida
- no self-approval

---

## Caso D — Crear issue

### Endpoint
`POST /api/tasks/:taskId/issues`

### Cadena
1. `authenticate`
2. `resolveAuthorizationContext(task)`
3. `requireCapability('issues.create')`
4. `requirePolicy('canReadWorkspaceResource')`
5. controller → service → DB

### Nota
La creación de issue es operativa y no requiere approval, pero sí scope correcto.

---

## Caso E — Aprobar tarea

### Endpoint lógico
`PATCH /api/tasks/:id/status` con `toStatus = approved`

### Cadena
1. `authenticate`
2. `resolveAuthorizationContext(task)`
3. `requireCapability('tasks.approve')`
4. `requirePolicy('canApproveTask')`
5. controller → service → DB
6. audit

### Reglas mínimas
- humano
- `org_owner` o política equivalente válida
- actor no es `completedBy`
- agente nunca aprueba

---

## Caso F — Submit Change Request

### Endpoint
`POST /api/change-requests/:id/submit`

### Cadena
1. `authenticate`
2. `resolveAuthorizationContext(changeRequest)`
3. capability según diseño final del módulo (temporalmente capability operativa compatible)
4. `requirePolicy('canSubmitChangeRequest')`
5. controller → `ChangeRequestService.submit()`
6. crea `ApprovalRequest`
7. audit

### Regla importante
Un CR no debe poder ejecutarse ni aprobarse automáticamente solo por tener acceso a tareas.

---

## Caso G — Aprobar firma

### Endpoint
`POST /api/approval-signatures/:id/approve`

### Cadena
1. `authenticate`
2. `resolveAuthorizationContext(approvalSignature)`
3. capability de aprobación correspondiente
4. `requirePolicy('canApproveSignature')`
5. controller → `ApprovalService.approve()`
6. vincula `ElectronicSignature`
7. audit

### Reglas mínimas
- humano
- firmante asignado o delegado válido
- secuencia correcta si el flujo es secuencial
- sin autoaprobación si aplica

---

## 6. Organización del código recomendada

## 6.1 Estructura sugerida

```text
src/
  middleware/
    authenticate.ts
    requireCapability.ts
    requirePolicy.ts
    resolveAuthorizationContext.ts
  services/
    permissions.service.ts
    policy.service.ts
    authorization-context.service.ts
    audit-decision.service.ts
  policies/
    task.policy.ts
    approval.policy.ts
    change-request.policy.ts
    workspace.policy.ts
  controllers/
  routes/
  domain-services/
```

### Nota
Si no quieres crear carpeta `policies`, al menos agrupa las policies por dominio y evita dejar reglas críticas dispersas en controllers.

---

## 7. Cambios concretos sobre componentes existentes

## 7.1 `authenticate`

### Mantener
- validación JWT
- aceptación de `access` y `service`

### Ajustar
- poblar `req.auth` estructurado
- rechazar token type incorrecto para rutas de negocio

## 7.2 `permissions.service.ts`

### Mantener
- lógica general de roles y capabilities

### Ajustar
- evaluar contra el `workspaceId` del recurso actual
- no aprobar por membresía en workspace ajeno
- dejar preparada distinción por `tokenType`

## 7.3 `requireCapability`

### Mantener
- wrapper de capability por ruta

### Ajustar
- depender de `req.auth`
- opcionalmente recibir contexto o usar `req.authz`

## 7.4 `contextual-permissions.service.ts`

### Extender
No dejarlo en dos funciones aisladas. Debe ser la base del policy layer.

---

## 8. Endpoints que deben tocarse en Bloque 1

## 8.1 Críticos inmediatos
- `users.ts`
- `import.ts`
- `issues.ts`
- `attachments.ts`
- `taskComment.ts`

## 8.2 Ya usan capability pero deben corregirse
- `projects.ts`
- `phases.ts`
- `deliveries.ts`
- `plans.routes.ts`
- `lifecycle.routes.ts`

## 8.3 De evaluación adicional
- `conversations.ts`
- `time-entries.routes.ts`
- rutas de lectura y métricas

---

## 9. Orden de implementación técnica

## 9.1 Paso 1 — Auth listo
No rediseñar auth. Ya está decidido.

## 9.2 Paso 2 — Seed RBAC
Roles, capabilities, orgs, workspaces, memberships.

## 9.3 Paso 3 — Quitar bypass
Remover `platform_super_admin` temporal de agentes solo cuando el seed esté completo.

## 9.4 Paso 4 — Resolver contexto
Implementar `resolveAuthorizationContext`.

## 9.5 Paso 5 — Corregir RBAC por workspace real
Ajustar `permissions.service`.

## 9.6 Paso 6 — Implementar policy layer mínima
Tasks, approvals, CR, users, imports.

## 9.7 Paso 7 — Proteger rutas críticas
Aplicar cadena completa en endpoints priorizados.

## 9.8 Paso 8 — Auditoría y tests
Agregar trazabilidad de decisiones críticas y pruebas integrales.

---

## 10. Qué NO debe hacerse

- No proteger rutas solo con `requireCapability` sin `authenticate`.
- No depender del JWT como fuente completa de scope.
- No meter toda la lógica crítica dentro del controller.
- No usar `platform_super_admin` como solución operativa estable.
- No permitir que aprobación dependa únicamente de una capability sin policy contextual.

---

## 11. Criterios de aceptación técnicos

La arquitectura de autorización se considerará correctamente implementada cuando:

- toda ruta crítica use la cadena completa de validación
- ningún request sensible se autorice sin `workspaceId`/`organizationId` resueltos
- el RBAC evalúe sobre el workspace correcto
- las policies críticas de tareas y aprobaciones estén separadas del controller
- agentes operen sin bypass de super admin
- ninguna aprobación crítica pueda realizarse por agente
- existan logs/auditoría mínimos para decisiones sensibles

---

## 12. Deuda futura prevista

Quedan preparadas, pero no incluidas completas en Bloque 1:

- `AgentIdentity` como entidad propia
- `ServiceAccount` separado de `User`
- delegación formal humano ↔ agente
- elevation / JIT
- MFA condicional
- policy engine horizontal enterprise

---

## 13. Conclusión

La implementación correcta de autorización para Bloque 1 no consiste en “poner middleware” de forma aislada. Consiste en construir una cadena coherente de:

- identidad
- contexto del recurso
- permiso general por rol
- restricción contextual por política
- auditoría

Ese núcleo permite implementar Bloque 1 sin parches y además deja alineado el sistema con el modelo objetivo futuro.

