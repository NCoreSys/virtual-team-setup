# DOC-SEC-04 — Matriz de Autorización Operativa (Bloque 1)

**Proyecto:** VTT → HybridFlow  
**Versión:** 1.0  
**Estado:** Base para implementación  
**Objetivo:** Consolidar en formato matricial las decisiones de autorización de Bloque 1 para que DB, BE, QA y TL tengan una referencia única y ejecutable.

---

## 1. Propósito del documento

Este documento aterriza el modelo de seguridad a matrices de implementación.

No reemplaza los otros documentos del paquete de seguridad. Los complementa.

Su función es dejar explícito:

- qué tipo de actor existe
- con qué credencial entra
- qué rol puede tener
- qué capability recibe
- qué acciones sobre cada recurso son permitidas
- qué policies contextuales deben correr
- qué acciones quedan reservadas a humanos

La matriz aquí definida debe tomarse como la **referencia operativa de Bloque 1**.

---

## 2. Estructura de la autorización en Bloque 1

La autorización se resuelve en este orden:

1. **Identidad autenticada**
2. **Scope real del recurso**
3. **Capability por RBAC**
4. **Policy contextual (ABAC mínimo)**
5. **Restricción por tipo de actor / SoD**

Por lo tanto, ninguna fila de esta matriz debe leerse como “si tiene capability, ya puede”. La capability habilita, pero la policy decide si el caso concreto procede.

---

## 3. Matriz A — Actores × Credenciales × Restricciones base

| Actor | Entidad técnica actual | Credencial | Token type | Refresh flow | Puede aprobar | Puede firmar | Puede gestionar usuarios | Observaciones |
|---|---|---|---|---|---|---|---|---|
| Humano | `User` | Access + Refresh | `access` / `refresh` | Sí | Sí, si rol/policy lo permite | Sí, si flujo/policy lo permite | Sí, si rol/capability lo permite | Fuente de autoridad de negocio |
| Agente | `User` | Service Token | `service` | No | **No por defecto** | **No por defecto** | No por defecto | Operador delegado, no equivalente al humano |
| Sistema / Service Account futuro | No separado aún | Service Token / API credential | futuro | No | No por defecto | No | Solo por policy futura | Preparar diseño, no implementar completo en B1 |
| Externo / Guest futuro | No separado aún | TBD | futuro | TBD | No | No | No | Modelo futuro, no entra completo en B1 |

---

## 4. Matriz B — Roles × Capabilities (base de Bloque 1)

## 4.1 Roles

- `platform_super_admin`
- `org_owner`
- `org_admin`
- `ws_tech_lead`
- `ws_lead`
- `ws_developer`
- `ws_reviewer`
- `ws_analyst`
- `ws_observer`

## 4.2 Capabilities

- `tasks.read`
- `tasks.create`
- `tasks.update`
- `tasks.delete`
- `tasks.status`
- `tasks.assign`
- `tasks.approve`
- `phases.read`
- `phases.create`
- `phases.update`
- `phases.delete`
- `workspaces.read`
- `workspaces.create`
- `workspaces.update`
- `workspaces.delete`
- `deliveries.read`
- `deliveries.create`
- `deliveries.update`
- `deliveries.delete`
- `tracking.view_all`
- `tracking.manage_workflows`
- `lifecycle.read`
- `lifecycle.update`
- `issues.create`
- `issues.update`
- `users.read`
- `users.manage`
- `catalogs.read`
- `attachments.manage`
- `import.execute`

## 4.3 Matriz consolidada

| Capability | platform_super_admin | org_owner | org_admin | ws_tech_lead | ws_lead | ws_developer | ws_reviewer | ws_analyst | ws_observer |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| tasks.read | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| tasks.create | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| tasks.update | ✅ | ✅ | ✅ | ✅ | ✅ | ✅* | ✅** | ❌ | ❌ |
| tasks.delete | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| tasks.status | ✅ | ✅ | ✅ | ✅*** | ✅*** | ✅**** | ✅***** | ❌ | ❌ |
| tasks.assign | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| tasks.approve | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| phases.read | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| phases.create | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| phases.update | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| phases.delete | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| workspaces.read | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| workspaces.create | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| workspaces.update | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| workspaces.delete | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| deliveries.read | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| deliveries.create | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| deliveries.update | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| deliveries.delete | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| tracking.view_all | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| tracking.manage_workflows | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| lifecycle.read | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| lifecycle.update | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| issues.create | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| issues.update | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| users.read | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| users.manage | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| catalogs.read | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| attachments.manage | ✅ | ✅ | ✅ | ✅ | ✅ | ✅* | ✅** | ❌ | ❌ |
| import.execute | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

### Notas obligatorias de esta matriz

- `*` Developer: solo en tareas asignadas a él.
- `**` Reviewer: solo en tareas dentro de su scope de revisión.
- `***` Tech Lead / Lead: puede mover hasta `completed`, nunca `approved`.
- `****` Developer: solo transiciones operativas autorizadas y en tareas asignadas.
- `*****` Reviewer: solo transiciones de revisión autorizadas.

La matriz anterior es **RBAC base**, no permiso final. Todo `✅` con nota requiere policy adicional.

---

## 5. Matriz C — Recursos × Acciones × Capability × Policy

Esta es la matriz más importante para backend.

| Recurso | Acción | Capability base | Policy contextual obligatoria | Actores no permitidos por defecto |
|---|---|---|---|---|
| Workspace | leer | `workspaces.read` | `canReadWorkspaceResource` | ninguno con membership válida |
| Workspace | crear | `workspaces.create` | `canManageWorkspace` | developer, reviewer, analyst, observer, agentes no autorizados |
| Workspace | actualizar | `workspaces.update` | `canManageWorkspace` | developer, reviewer, analyst, observer |
| Workspace | eliminar | `workspaces.delete` | `canDeleteWorkspace` | todos salvo privilegio organizacional válido |
| User | leer | `users.read` | `canReadUsersInScope` | actores fuera de org/workspace |
| User | gestionar | `users.manage` | `canManageUsers` | developer, reviewer, analyst, observer, agentes por defecto |
| Task | leer | `tasks.read` | `canReadWorkspaceResource` | actores fuera de scope |
| Task | crear | `tasks.create` | `canCreateTask` | developer, reviewer, analyst, observer |
| Task | actualizar | `tasks.update` | `canUpdateTask` | actor fuera de scope o developer no asignado |
| Task | eliminar | `tasks.delete` | `canDeleteTask` | todos salvo owner/admin válidos según regla final |
| Task | asignar | `tasks.assign` | `canAssignTask` | developer, reviewer, analyst, observer |
| Task | cambiar estado operativo | `tasks.status` | `canTransitionTask` | actores fuera de transición permitida |
| Task | aprobar | `tasks.approve` | `canApproveTask` | agentes, actor que completó, roles no humanos |
| Phase | leer | `phases.read` | `canReadWorkspaceResource` | fuera de scope |
| Phase | crear | `phases.create` | `canManagePhaseStructure` | workspace roles operativos bajos |
| Phase | actualizar | `phases.update` | `canManagePhaseStructure` | developer, reviewer, analyst, observer |
| Phase | eliminar | `phases.delete` | `canDeletePhase` | developer, reviewer, analyst, observer |
| Delivery | leer | `deliveries.read` | `canReadWorkspaceResource` | fuera de scope |
| Delivery | crear | `deliveries.create` | `canCreateDelivery` | analyst, observer |
| Delivery | actualizar | `deliveries.update` | `canUpdateDelivery` | developer salvo política específica |
| Delivery | eliminar | `deliveries.delete` | `canDeleteDelivery` | workspace roles bajos |
| Issue | crear | `issues.create` | `canCreateIssue` | analyst, observer |
| Issue | actualizar | `issues.update` | `canUpdateIssue` | actor sin ownership o privilegio de liderazgo |
| Attachment | gestionar | `attachments.manage` | `canManageAttachment` | analyst, observer |
| Comment | crear | `tasks.update` | `canCommentTask` | actor fuera de scope |
| ChangeRequest | crear | capability operativa definida por módulo | `canCreateChangeRequest` | observer, agente fuera de scope |
| ChangeRequest | submit | capability operativa definida por módulo | `canSubmitChangeRequest` | actor fuera de workspace, agente sin permiso |
| ChangeRequest | cancelar | capability operativa/gobierno | `canCancelChangeRequest` | actor sin ownership o liderazgo |
| ChangeRequest | ejecutar | capability de flujo | `canExecuteApprovedChangeRequest` | cualquiera mientras no esté aprobado |
| ApprovalRequest | consultar | capability de aprobación / lectura | `canReadApprovalFlow` | actor fuera del flujo |
| ApprovalSignature | aprobar | capability de aprobación | `canApproveSignature` | agentes, actor no asignado, actor fuera de secuencia |
| ApprovalSignature | rechazar | capability de aprobación | `canRejectSignature` | agentes, actor no asignado |
| ApprovalSignature | delegar | capability de aprobación | `canDelegateSignature` | agentes, actor no autorizable |
| ElectronicSignature | firmar | capability de aprobación/firma | `canSignElectronically` | agentes |
| Import | ejecutar | `import.execute` | `canExecuteImport` | workspace roles bajos, agentes por defecto |
| Catalog | leer | `catalogs.read` o público según decisión final | `canReadCatalogs` | depende de decisión final |

---

## 6. Matriz D — Transiciones de estado de Task por rol

| Transición | org_owner | org_admin | ws_tech_lead | ws_lead | ws_developer | ws_reviewer | ws_analyst | ws_observer | agente |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `pending → in_progress` | ✅ | ✅ | ✅ | ✅ | ✅* | ❌ | ❌ | ❌ | ✅* |
| `in_progress → in_review` | ✅ | ✅ | ✅ | ❌/según regla final | ✅* | ❌ | ❌ | ❌ | ✅* |
| `in_progress → on_hold` | ✅ | ✅ | ✅ | ✅ | ✅* | ❌ | ❌ | ❌ | ✅* |
| `on_hold → in_progress` | ✅ | ✅ | ✅ | ✅ | ✅* | ❌ | ❌ | ❌ | ✅* |
| `in_review → in_progress` | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | según política de agente revisor |
| `in_review → completed` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | según tipo de agente revisor |
| `completed → approved` | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | **❌** |
| `any → cancelled` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

**Nota:** `*` solo sobre tareas asignadas al actor.

---

## 7. Matriz E — Aprobaciones y firmas

| Acción | Humano org_owner | Humano org_admin | ws_tech_lead | ws_lead | ws_developer | ws_reviewer | Agente | Condición obligatoria |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| Aprobar Task | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | actor distinto de `completedBy` |
| Aprobar CR | ✅** | ⚠️* | ⚠️* | ❌ | ❌ | ❌ | ❌ | depende de flujo y nivel configurado |
| Rechazar firma | ✅** | ⚠️* | ⚠️* | ❌ | ❌ | ❌ | ❌ | actor asignado / delegado válido |
| Firmar electrónicamente | ✅ | ⚠️* | ⚠️* | ❌ | ❌ | ❌ | ❌ | humano + asignación + secuencia |
| Delegar firma | ✅ | ⚠️* | ⚠️* | ❌ | ❌ | ❌ | ❌ | política de flujo lo permite |

**Notas:**
- `*` solo si el flujo de aprobación lo configuró como firmante válido.
- `**` rol más naturalmente dueño del flujo en Bloque 1.

---

## 8. Matriz F — Acciones reservadas solo para humanos

| Acción | Humano | Agente | Comentario |
|---|:---:|:---:|---|
| Aprobar tarea | ✅ | ❌ | `tasks.approve` humana |
| Aprobar firma | ✅ | ❌ | no delegar a agentes |
| Rechazar firma | ✅ | ❌ | control crítico |
| Firmar electrónicamente | ✅ | ❌ | compliance |
| Ejercer `org_owner` | ✅ | ❌ | el PM-agente no equivale al owner |
| Gestión crítica de seguridad | ✅ | ❌ | break-glass / gobierno |
| Revocar sesiones humanas | ✅ | ❌ | administración / seguridad |

---

## 9. Matriz G — Policies mínimas obligatorias a implementar

| Policy | Aplica a | Qué valida |
|---|---|---|
| `canReadWorkspaceResource` | lectura de recursos | resource → workspace → org + membership válida |
| `canUpdateTask` | update task | assignment / scope / actor type |
| `canTransitionTask` | status task | transición permitida por rol + actor |
| `canApproveTask` | approve task | humano + `tasks.approve` + no self-approval |
| `canCreateIssue` | issue create | scope correcto |
| `canUpdateIssue` | issue update | ownership o liderazgo válido |
| `canManageAttachment` | attachments | scope + permiso de edición real |
| `canCreateChangeRequest` | CR create | actor dentro del proyecto/workspace |
| `canSubmitChangeRequest` | CR submit | estado, ownership/scope, completitud mínima |
| `canApproveSignature` | firma approve | actor asignado/delegado + secuencia + humano |
| `canRejectSignature` | firma reject | actor asignado/delegado + humano |
| `canDelegateSignature` | firma delegate | actor válido + policy del flujo |
| `canManageUsers` | users manage | organization/workspace correcto + privilegio superior |
| `canExecuteImport` | import | permiso admin + scope válido |

---

## 10. Matriz H — Scopes por tipo de recurso

| Recurso | Scope mínimo a resolver | Fuente de verdad esperada |
|---|---|---|
| Organization | `organizationId` | recurso directo |
| Workspace | `organizationId`, `workspaceId` | recurso directo |
| Project | `organizationId`, `workspaceId`, `projectId` | `Project.workspaceId` |
| Phase | `organizationId`, `workspaceId`, `projectId` | `Phase -> Project` |
| Task | `organizationId`, `workspaceId`, `projectId` | `Task -> Project` |
| Delivery | `organizationId`, `workspaceId`, `projectId` | `Delivery -> Phase/Project` |
| Issue | `organizationId`, `workspaceId`, `projectId`, `taskId` | `Issue -> Task -> Project` |
| Attachment | `organizationId`, `workspaceId`, `projectId`, `taskId` | `Attachment -> Task -> Project` |
| ChangeRequest | `organizationId`, `workspaceId`, `projectId` | `CR -> Project` |
| ApprovalRequest | `organizationId`, `workspaceId`, `projectId`, `changeRequestId` | `ApprovalRequest -> CR -> Project` |
| ApprovalSignature | `organizationId`, `workspaceId`, `projectId`, `approvalRequestId` | `ApprovalSignature -> ApprovalRequest` |
| ElectronicSignature | scope del flujo que firma | relación con `ApprovalSignature` |

---

## 11. Reglas de lectura de esta matriz

1. **La capability nunca es suficiente por sí sola.**  
2. Todo `✅` de RBAC puede quedar denegado por policy contextual.  
3. Todo flujo de aprobación y firma debe revisar también SoD.  
4. Agente y humano no se tratan igual aunque ambos hoy cuelguen de `User`.  
5. Si un recurso no puede resolverse a `workspaceId` y `organizationId`, la autorización está incompleta.

---

## 12. Criterios de aceptación de la matriz

La matriz se considera lista para implementación cuando:

- DB puede sembrar roles, capabilities y memberships sin ambigüedad
- BE puede mapear cada endpoint crítico a capability + policy
- QA puede derivar casos positivos y negativos por rol y por actor
- TL puede revisar que ninguna acción crítica depende solo de una capability
- el equipo acepta que aprobación y firma son acciones humanas críticas por defecto

---

## 13. Conclusión

La matriz de Bloque 1 no es solo “roles × capabilities”. La referencia operativa correcta está compuesta por:

- matriz de actores y credenciales
- matriz RBAC base
- matriz recurso × acción × capability × policy
- matriz de transiciones de estado
- matriz de aprobaciones y acciones reservadas a humanos
- matriz de scopes por recurso

Este documento completa el paquete de seguridad de Bloque 1 y debe leerse junto con:

1. **DOC-SEC-01 — Modelo de Seguridad: Actores, Identidades y Scopes**  
2. **DOC-SEC-02 — Políticas de Permisos: RBAC + ABAC mínimo**  
3. **DOC-SEC-03 — Arquitectura de Implementación de Autorización**

