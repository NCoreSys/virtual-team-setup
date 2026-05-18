# DOC-SEC-02 — Políticas de Permisos: RBAC + ABAC mínimo (Bloque 1)

**Proyecto:** VTT → HybridFlow  
**Versión:** 1.0  
**Estado:** Base para implementación  
**Objetivo:** Traducir el modelo de seguridad de Bloque 1 a un sistema de permisos ejecutable, separando claramente qué resuelve RBAC, qué resuelve ABAC y qué acciones quedan reservadas a actores humanos.

---

## 1. Propósito del documento

Este documento define las políticas operativas de autorización de Bloque 1.

Su función es responder, con precisión:

- qué capabilities existen y para qué sirven
- qué roles reciben esas capabilities
- qué restricciones contextuales aplican encima del rol
- qué acciones están prohibidas para agentes
- qué validaciones de segregación de funciones se aplican desde el inicio

La regla principal es:

> **RBAC da permiso general. ABAC decide si ese permiso puede ejercerse en este recurso, en este contexto y por este actor.**

---

## 2. Estructura de autorización de Bloque 1

Bloque 1 implementa tres capas reales de autorización:

### 2.1 Capa 1 — Identidad autenticada

Primero se valida si el request viene firmado por un actor válido.

Tipos de identidad aceptados:
- humano con access token
- agente con service token

La identidad autenticada todavía no implica permiso.

### 2.2 Capa 2 — RBAC

RBAC responde:

**¿este actor, por su rol, tiene esta capability en general?**

Aquí entran:
- `Role`
- `Capability`
- `RoleCapability`
- `platformRole`
- membresías en workspace

### 2.3 Capa 3 — ABAC / policy

ABAC responde:

**aunque el rol tenga esa capability, en este recurso concreto y bajo estas condiciones, ¿se permite la acción?**

Aquí entran:
- pertenencia real al workspace
- ownership o assignment
- transición de estado válida
- tipo de actor (humano/agente)
- separación entre quien ejecuta y quien aprueba
- restricciones por status del recurso

---

## 3. Catálogo de roles operativos de Bloque 1

El sistema usará el siguiente catálogo operativo base.

### 3.1 Nivel plataforma
- `platform_super_admin`

### 3.2 Nivel organización
- `org_owner`
- `org_admin`

### 3.3 Nivel workspace
- `ws_tech_lead`
- `ws_lead`
- `ws_developer`
- `ws_reviewer`
- `ws_analyst`
- `ws_observer`

---

## 4. Catálogo de capabilities base

Bloque 1 parte del catálogo operativo de 30 capabilities. Para implementación, se agrupan así:

### 4.1 Contenido y ejecución
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
- `deliveries.read`
- `deliveries.create`
- `deliveries.update`
- `deliveries.delete`
- `issues.create`
- `issues.update`
- `attachments.manage`

### 4.2 Workspace / proyecto
- `workspaces.read`
- `workspaces.create`
- `workspaces.update`
- `workspaces.delete`

### 4.3 Tracking / lifecycle
- `tracking.view_all`
- `tracking.manage_workflows`
- `lifecycle.read`
- `lifecycle.update`

### 4.4 Administración
- `users.read`
- `users.manage`
- `import.execute`

### 4.5 Sistema / referencia
- `catalogs.read`

---

## 5. Qué resuelve RBAC y qué no resuelve

## 5.1 Qué sí resuelve RBAC

RBAC decide si un rol puede realizar una acción en abstracto.

Ejemplos:
- `org_owner` puede aprobar
- `ws_developer` puede actualizar tareas
- `ws_reviewer` puede actualizar issues
- `org_admin` puede gestionar usuarios
- `ws_analyst` puede leer contenido

## 5.2 Qué NO resuelve RBAC

RBAC no sabe:
- si la tarea está asignada al usuario
- si el recurso pertenece al workspace correcto
- si el actor es humano o agente
- si la transición de estado está permitida
- si hay autoaprobación
- si falta evidencia para cerrar

Eso debe ir a políticas ABAC.

---

## 6. Matriz de permisos base por rol

Este documento no reproduce la matriz entera en formato extensivo, pero establece la política oficial de implementación por grupo.

## 6.1 `platform_super_admin`

**Uso esperado:** solo infraestructura / emergencia.

**Política:**
- bypass de plataforma
- no debe ser el modo normal de operación
- no debe usarse como sustituto de roles organizacionales o de workspace

## 6.2 `org_owner`

**Política:**
- acceso total funcional dentro de su organización
- puede aprobar tareas y flujos críticos
- puede gestionar usuarios y workspaces de su org
- sigue sujeto a restricciones críticas de integridad del negocio cuando aplique

## 6.3 `org_admin`

**Política:**
- administra org y workspaces
- no aprueba por defecto si la política del flujo lo reserva a `org_owner`
- no sustituye al owner humano en decisiones críticas

## 6.4 `ws_tech_lead`

**Política:**
- lectura completa operativa del workspace
- puede asignar
- puede cambiar estados hasta `completed`
- no puede pasar a `approved`
- puede operar sobre tareas y entregables del workspace

## 6.5 `ws_lead`

**Política:**
- liderazgo funcional de área
- puede mover estados hasta `completed`
- puede crear o coordinar trabajo según capability asignada
- no aprueba

## 6.6 `ws_developer`

**Política:**
- ejecuta trabajo operativo
- actualiza tareas dentro de su scope
- puede crear/actualizar issues según reglas
- no crea tareas salvo decisión explícita diferente en feature posterior
- no aprueba

## 6.7 `ws_reviewer`

**Política:**
- revisa trabajo
n- puede crear y actualizar issues
- puede participar en transición hacia `completed` según reglas
- no aprueba

## 6.8 `ws_analyst`

**Política:**
- lectura y análisis
- sin ejecución operativa de cambios en tareas ni aprobación

## 6.9 `ws_observer`

**Política:**
- solo lectura

---

## 7. Reglas ABAC mínimas obligatorias

Las siguientes políticas deben existir en Bloque 1. No son opcionales.

## 7.1 Scope por organization

Toda acción sobre recurso debe validar que el recurso pertenece a la misma organization que el actor está autorizado a operar.

## 7.2 Scope por workspace

Toda acción sobre recurso debe validar:

- el recurso pertenece al workspace esperado
- el actor es miembro del workspace o tiene privilegio superior organizacional válido

## 7.3 Restricción por asignación de tarea

### Regla DEV-01
Un `ws_developer` solo puede actualizar una tarea si la tarea está asignada a él.

### Regla DEV-02
Un `ws_developer` solo puede ejecutar las transiciones permitidas para developer.

## 7.4 Restricción por rol de revisión

### Regla REV-01
Un `ws_reviewer` solo puede modificar el estado o revisión de tareas dentro de su scope de revisión.

### Regla REV-02
El reviewer no aprueba.

## 7.5 Restricción por transición de estado

### Regla ST-01
`ws_tech_lead` y `ws_lead` pueden llevar el trabajo hasta `completed`.

### Regla ST-02
`approved` requiere capability separada `tasks.approve`.

### Regla ST-03
`tasks.approve` solo puede ejercerse por actor humano autorizado.

## 7.6 Restricción de autoaprobación

### Regla AP-01
El actor que completó una tarea no puede autoaprobarla.

### Regla AP-02
El actor asignado como firmante no puede saltarse secuencia si el flujo es secuencial.

## 7.7 Restricción por tipo de actor

### Regla AG-01
Un agente nunca aprueba por defecto.

### Regla AG-02
Un agente nunca sustituye al `org_owner` humano.

### Regla AG-03
Un agente puede ejecutar trabajo, actualizar estados operativos y producir evidencia dentro de su scope, pero no ejercer poder de gobierno reservado.

## 7.8 Restricción por recurso de aprobación

### Regla CR-01
Un Change Request no se ejecuta mientras no esté aprobado.

### Regla CR-02
Una firma no se puede resolver si el actor no es el asignado o delegado válido.

### Regla CR-03
Las firmas electrónicas requieren actor humano y vínculo correcto con el flujo.

---

## 8. Acciones reservadas solo para humanos

Las siguientes acciones quedan restringidas a humanos en Bloque 1:

- `tasks.approve`
- aprobar o rechazar firmas
- aprobar o rechazar flujos de Change Request cuando corresponda
- firmar electrónicamente
- ejercer `org_owner`
- ejecutar decisiones críticas de seguridad o gobierno organizacional

Esta lista puede crecer, pero no reducirse sin decisión explícita.

---

## 9. Reglas SoD mínimas

## 9.1 Separación ejecución vs aprobación

Quien ejecuta el trabajo no debe ser quien lo aprueba.

## 9.2 Separación agente vs owner

El PM-agente, TL-agent o cualquier agente técnico no reemplaza al owner humano.

## 9.3 Separación revisión vs firma crítica

Una revisión operativa no equivale automáticamente a una firma de aprobación formal.

## 9.4 Inmutabilidad de auditoría

No debe existir capacidad normal de negocio para borrar la traza de aprobación, firma o cambio crítico.

---

## 10. Policies concretas para implementar

El backend debe implementar, como mínimo, estas policies ejecutables.

### 10.1 `canReadWorkspaceResource`
Valida pertenencia y scope del recurso.

### 10.2 `canUpdateTask`
Valida:
- capability `tasks.update`
- actor en workspace correcto
- si developer: task asignada a él
- si reviewer: scope de revisión válido

### 10.3 `canTransitionTask`
Valida:
- capability de status o approve según destino
- transición permitida para el rol
- actor humano si destino es `approved`
- no autoaprobación

### 10.4 `canApproveTask`
Valida:
- humano
- capability `tasks.approve`
- rol efectivo compatible (`org_owner`)
- `completedBy != actor`

### 10.5 `canSubmitChangeRequest`
Valida:
- actor dentro del proyecto/workspace
- estado actual del CR
- completitud mínima requerida

### 10.6 `canApproveSignature`
Valida:
- actor asignado o delegado
- humano
- secuencia correcta
- privilegio de firma válido

### 10.7 `canManageUsers`
Valida:
- capability `users.manage`
- alcance organizacional o superior

### 10.8 `canExecuteImport`
Valida:
- capability `import.execute`
- actor permitido por org/workspace según política final de importación

---

## 11. Mapa de decisiones por tipo de recurso

## 11.1 Recursos operativos

**Task / Issue / Comment / Attachment / Delivery**
- RBAC decide acceso base
- ABAC decide ownership, asignación y scope

## 11.2 Recursos de estructura

**Workspace / Project / Phase / Plan / Lifecycle**
- RBAC domina en lectura/gestión general
- ABAC valida organization/workspace real del recurso

## 11.3 Recursos de gobierno

**ChangeRequest / ApprovalRequest / ApprovalSignature / ElectronicSignature**
- RBAC habilita solo a roles adecuados
- ABAC y SoD dominan la decisión final

---

## 12. Política específica para agentes

### 12.1 Regla de base

El agente es operador delegado, no autoridad final.

### 12.2 Permisos permitidos en Bloque 1

El agente puede:
- leer tareas y contexto si su rol lo permite
- actualizar progreso y estados operativos dentro de su scope
- crear issues si la capability lo permite
- generar artefactos operativos y evidencia si se le habilita

### 12.3 Permisos prohibidos por defecto

El agente no puede:
- aprobar tareas
- ejercer `org_owner`
- firmar electrónicamente
- cerrar flujos críticos como autoridad humana
- gestionar seguridad de tenant/organization

---

## 13. Qué queda para evolución futura

Este documento define el núcleo ejecutable de Bloque 1. A futuro se podrá extender con:

- principals separados (`HumanUser`, `AgentIdentity`, `ServiceAccount`)
- delegación formal por entidad
- JIT / elevation
- políticas MFA / device trust
- SoD enterprise más amplio
- scopes API diferenciados por clase de token

---

## 14. Criterios de aceptación de política

El modelo de permisos se considerará correctamente implementado cuando:

- una capability nunca sea suficiente por sí sola para operar fuera del scope del recurso
- ningún agente pueda aprobar por defecto
- ningún developer pueda modificar tareas ajenas sin regla explícita
- `approved` exija validación humana y capability separada
- el flujo de aprobación respete secuencia, asignación y anti-autoaprobación
- todas las rutas críticas combinen identidad + RBAC + policy contextual

---

## 15. Conclusión

La autorización de Bloque 1 no se reduce a matriz de roles. La matriz RBAC es solo una capa. El sistema completo se compone de:

- identidad válida
- rol y capability
- scope real del recurso
- políticas contextuales
- separación mínima de funciones
- reservas explícitas para acciones humanas críticas

Este documento debe usarse junto con:

1. **Modelo de seguridad: actores, identidades y scopes**  
2. **Arquitectura de implementación y flujo exacto por request**

