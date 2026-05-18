# DOC-SEC-01 — Modelo de Seguridad: Actores, Identidades y Scopes (Bloque 1)

**Proyecto:** VTT → HybridFlow  
**Versión:** 1.0  
**Estado:** Base para implementación  
**Objetivo:** Definir las entidades, actores, jerarquía de scopes y relaciones mínimas de seguridad que deben quedar cerradas antes de implementar autenticación, autorización y aprobaciones del Bloque 1.

---

## 1. Propósito del documento

Este documento define el **modelo base de seguridad** sobre el que se apoyará la implementación del Bloque 1. No describe todavía el detalle de middlewares o endpoints, sino la estructura conceptual y operativa que permite contestar, de forma consistente, las preguntas esenciales del sistema:

- ¿Quién actúa?
- ¿Con qué identidad entra?
- ¿Sobre qué recurso está actuando?
- ¿En qué organización y workspace existe ese recurso?
- ¿Qué alcance real tiene ese actor?
- ¿Qué diferencias existen entre humano y agente?
- ¿Qué acciones son críticas y no deben recaer en agentes?

La regla rectora es simple:

> **La seguridad no se modela desde rutas; se modela desde actores, recursos, scopes y políticas.**

---

## 2. Alcance de Bloque 1

Bloque 1 implementa la base operativa mínima de seguridad para soportar:

- autenticación profesional
- multitenant / organizations / workspaces
- RBAC activado con roles y capabilities
- restricciones contextuales mínimas
- sistema de aprobaciones y change requests
- preparación para compliance y auditoría posterior

Bloque 1 **no** implementa todavía el modelo enterprise completo de principals separados ni un policy engine sofisticado. Sin embargo, sí debe dejar el diseño listo para evolucionar hacia eso sin rehacer la arquitectura.

---

## 3. Principios de diseño

### 3.1 Seguridad por jerarquía de alcance

Toda autorización debe evaluarse siguiendo esta jerarquía:

**Platform → Organization → Workspace → Resource**

Ninguna acción debe aprobarse sin poder resolver explícitamente en qué organization y en qué workspace vive el recurso afectado.

### 3.2 Humano y agente no son equivalentes

Aunque en Bloque 1 ambos sigan representados por la entidad `User`, el sistema debe tratarlos como actores distintos a nivel de política.

- El humano es la autoridad de negocio.
- El agente es un operador delegado.
- El agente puede compartir scope operativo, pero no poder total.

### 3.3 RBAC no basta por sí solo

Roles y capabilities responden solo una parte del problema: qué puede hacer un actor en general. Las reglas reales del sistema también dependen de:

- el recurso concreto
- el workspace
- la asignación del trabajo
- el estado del recurso
- el tipo de actor
- la segregación de funciones

Por eso la implementación debe llevar, desde Bloque 1, una combinación de:

- autenticación
- RBAC
- ABAC mínimo / políticas contextuales

### 3.4 Aprobaciones y firmas son dominio crítico

Cualquier acción de aprobación, firma, cierre incompleto o cambio con impacto fuerte se considera **acción crítica**. Estas acciones deben estar más restringidas que una actualización operativa ordinaria.

---

## 4. Actores del sistema

## 4.1 Actor humano

Es la persona que opera el sistema desde frontend o cliente autenticado.

**Características:**
- entra por login humano
- usa sesión web/mobile
- puede tener una o más membresías organizacionales / de workspace
- puede ocupar roles operativos y/o de gobierno
- puede ser aprobador, firmante o owner organizacional

**Casos típicos:**
- Martin como `org_owner`
- PM humano
- TL humano
- QA humano
- aprobador de CR
- firmante electrónico

## 4.2 Actor agente

Es un actor no humano que ejecuta trabajo técnico u operativo dentro del sistema.

**Características:**
- entra por token de servicio
- no usa refresh flow
- opera server-to-server
- puede estar asociado a workspace/proyecto/tarea
- no debe heredar 1:1 el poder del humano
- tiene restricciones por tipo de actor

**Casos típicos:**
- TL-Agent
- Backend Specialist
- DB Engineer
- Integration Reviewer

## 4.3 Actor sistema / service account (objetivo futuro)

No se modela como tabla separada en Bloque 1, pero sí debe existir como categoría conceptual desde hoy.

**Uso esperado a futuro:**
- integraciones
- webhooks
- procesos internos de plataforma
- jobs automáticos con permisos acotados

## 4.4 Actor externo / auditor / guest (objetivo futuro)

Tampoco se modela completo en Bloque 1, pero el diseño no debe cerrarle el paso.

---

## 5. Entidades de seguridad

## 5.1 Identidad y autenticación

### `User`
Entidad actual base para humanos y agentes.

**Bloque 1:**
- sigue siendo el principal técnico actual
- distingue casos por claims y políticas
- contiene `platformRole` como capa superior temporal

### `RefreshToken`
Representa sesión revocable de usuario humano.

### `VerificationToken`
Soporta verificación de email y reset de password.

## 5.2 Scope organizacional

### `Organization`
Representa tenant lógico del sistema.

### `Workspace`
Representa unidad operativa o proyecto lógico bajo una organization.

### `WorkspaceMember`
Relaciona `User` con `Workspace` y le asigna un rol efectivo.

Es la entidad clave de pertenencia operativa.

## 5.3 Autorización base

### `Role`
Define el rol asignable.

### `Capability`
Define el permiso atómico.

### `RoleCapability`
Relaciona rol con capability.

### `platformRole` (en `User`)
Se considera una capa transitoria de autorización superior. En Bloque 1 se mantiene por compatibilidad, pero no debe convertirse en mecanismo dominante de seguridad ordinaria.

## 5.4 Gobierno, aprobación y cambio

### `ApprovalLevel`
### `ApprovalRole`
### `ApprovalLevelConfig`
### `ProjectApprover`
### `ApprovalFlowConfig`
### `ApprovalFlowSignatory`
### `ApprovalRequest`
### `ApprovalSignature`
### `ElectronicSignature`
### `ChangeRequest`
### `ChangeRequestTask`
### `ArchivedTaskReference`

Estas entidades forman el núcleo de gobierno y control del cambio.

## 5.5 Trazabilidad y lifecycle

### `ElementStatusHistory`
### `ElementMetrics`
### `AuditLog` / equivalente

Estas entidades soportan auditabilidad, seguimiento, agregación y control de lifecycle.

---

## 6. Recursos protegidos

En Bloque 1, los recursos protegidos mínimos son:

### Organizacionales
- Organization
- Workspace
- miembros de workspace
- usuarios

### Operativos
- Project
- Phase
- Task
- Delivery
- Issue
- Attachment
- TaskComment
- Plan / Lifecycle

### Gobierno
- ChangeRequest
- ApprovalRequest
- ApprovalSignature
- ProjectApprover
- ElectronicSignature

### Trazabilidad y control
- ElementStatusHistory
- ElementMetrics
- archivos archivados
- logs / evidencias / snapshots según aplique

Regla obligatoria:

> Todo recurso protegido debe poder resolverse hasta su `organizationId` y `workspaceId` efectivos.

---

## 7. Jerarquía de scopes

## 7.1 Scope de plataforma

Aplica a administración transversal y soporte de plataforma.

**Ejemplo:** `platform_super_admin`

Debe tratarse como excepción controlada, no como ruta normal de operación diaria.

## 7.2 Scope organizacional

Aplica a todos los workspaces dentro de una organización.

**Ejemplos:**
- `org_owner`
- `org_admin`

Este scope habilita gobierno amplio dentro de la org, pero no debe saltarse automáticamente reglas críticas de aprobación o segregación.

## 7.3 Scope de workspace

Aplica a recursos del workspace específico donde el actor es miembro.

**Ejemplos:**
- `ws_tech_lead`
- `ws_lead`
- `ws_developer`
- `ws_reviewer`
- `ws_analyst`
- `ws_observer`

## 7.4 Scope de recurso

Es el nivel más fino. Determina si una acción puede ejecutarse **sobre este recurso concreto**, no solo sobre el módulo.

**Ejemplos de atributos relevantes:**
- `workspaceId`
- `projectId`
- `assignedUserId`
- `completedBy`
- `requestedBy`
- `resourceOwnerId`
- `status`

---

## 8. Relación humano–agente

## 8.1 Regla general

El agente no debe modelarse como “el mismo usuario que la persona”.

En Bloque 1 todavía no existe una entidad `AgentIdentity` separada, pero el modelo base debe asumir desde ya lo siguiente:

- el humano es la autoridad de negocio
- el agente es un operador delegado
- el agente comparte contexto, no soberanía total

## 8.2 Regla de herencia

El agente **no hereda todo**. Solo hereda:

- el contexto permitido
- el scope operativo habilitado
- un subconjunto de capabilities

## 8.3 Fórmula de permisos efectivos del agente

**Permisos efectivos del agente =**  
permisos base del workspace o del actor que lo habilita  
∩ capabilities permitidas al tipo de agente  
∩ scope del proyecto/tarea  
∩ restricciones SoD / reglas críticas

## 8.4 Consecuencias prácticas

- si el humano no tiene acceso al proyecto, el agente tampoco
- si el humano sí tiene acceso, el agente puede operar solo dentro del alcance delegado
- aprobación, firma y cambios críticos siguen reservados salvo decisión explícita posterior

---

## 9. Roles funcionales, business roles y roles de seguridad

Uno de los errores más peligrosos es mezclar estos tres niveles.

### 9.1 Persona de negocio
Ejemplo:
- Program Manager
- QA/RA Manager
- VP Engineering

### 9.2 Rol funcional del producto
Ejemplo:
- PM
- TL
- Reviewer
- Analyst

### 9.3 Rol de autorización
Ejemplo:
- `org_owner`
- `ws_tech_lead`
- `ws_reviewer`
- capability específica

**Regla:**
Los títulos operativos o de negocio no deben usarse como sustituto directo del rol de seguridad.

---

## 10. Tokens y sesiones por tipo de actor

## 10.1 Humano

**Credenciales:**
- Access token (1h)
- Refresh token (30d)

**Propiedades:**
- sesión revocable
- refresh flow
- control de sesiones activas
- logout
- reset password invalida sesiones

## 10.2 Agente

**Credencial:**
- Service token de larga duración

**Propiedades:**
- sin refresh flow
- almacenado en variables de entorno
- autenticación server-to-server

## 10.3 Implicación de diseño

Aunque ambos hoy resuelvan a `User`, el modelo ya debe separar conceptualmente:

- sesión humana
- credencial de servicio

Porque el lifecycle de riesgo no es el mismo.

---

## 11. Acciones sensibles

Las acciones sensibles mínimas de Bloque 1 son:

- cambiar estados relevantes de lifecycle
- completar trabajo
- aprobar trabajo
- firmar electrónicamente
- crear y ejecutar change requests
- cancelar tareas/sprints/fases/proyectos
- mover o invalidar dependencias
- gestionar usuarios
- gestionar workspaces
- importar proyectos
- exportar o consultar artefactos sensibles cuando aplique

Estas acciones no pueden depender solo de una ruta protegida por capability genérica.

---

## 12. Acciones reservadas a humanos

Bloque 1 debe fijar expresamente que ciertas acciones son humanas por definición, salvo redefinición posterior:

- aprobar tarea
- aprobar/rechazar CR cuando aplique
- aprobar/rechazar firmas
- firmar electrónicamente
- ejercer rol `org_owner`
- ejecutar decisiones break-glass de seguridad

Regla complementaria:

> Ningún agente aprueba por defecto.

---

## 13. Segregación mínima de funciones (SoD)

Aunque Bloque 1 no implementa SoD enterprise completo, sí debe respetar estas reglas mínimas:

- quien ejecuta no aprueba
- el actor que completó una tarea no puede autoaprobarla
- el agente no puede actuar como aprobador humano
- PM-agente no equivale a `org_owner`
- la función de firma/aprobación debe quedar trazada y separada del operador que ejecutó el cambio

---

## 14. Gaps aceptados en Bloque 1

Estos vacíos se aceptan temporalmente, pero deben quedar documentados como deuda técnica controlada:

- no existe tabla separada de `AgentIdentity`
- no existe `ServiceAccount` formal como entidad propia
- no existe tabla explícita de delegación agente ↔ humano ↔ proyecto
- no existe todavía un policy engine generalizado
- no existe SoD horizontal enterprise completo

Bloque 1 implementa el núcleo. La expansión posterior deberá resolver estos puntos de manera estructural.

---

## 15. Conclusión

El modelo de seguridad de Bloque 1 no se limita a roles y rutas protegidas. La base correcta queda definida por:

- actores diferenciados
- recursos protegidos
- scopes jerárquicos
- sesión humana vs credencial de agente
- permisos base por rol
- restricciones contextuales por recurso
- acciones reservadas a humanos
- SoD mínimo para aprobaciones y control

Este documento sirve como base para los otros dos documentos de implementación:

1. **Políticas de permisos (RBAC + ABAC mínimo)**  
2. **Arquitectura de implementación y flujo por request**

