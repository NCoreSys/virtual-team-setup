# 🛡️ TEMPLATE BASE — SPEC ADMIN + RBAC (Roles/Permisos/Auditoría)

> **Versión:** 2.0 (Estandarizada para agentes)  
> **Tipo:** P2 — Enterprise/Scale  
> **Última actualización:** {{FECHA_ACTUALIZACION}}

---

## 🔖 GUÍA DE USO DEL TEMPLATE

### Marcadores de obligatoriedad

| Marcador | Significado | Regla |
|----------|-------------|-------|
| `[OBL]` | **Obligatorio** | Siempre debe completarse |
| `[OPC]` | **Opcional** | Completar si aplica al proyecto |
| `[COND]` | **Condicional** | Completar solo si se cumple la condición indicada |

### Cuándo usar este template

- ✅ Panel de **administración de usuarios**
- ✅ Sistema con **roles y permisos** (RBAC)
- ✅ Aplicaciones **multi-tenant**
- ✅ Requisitos de **auditoría y compliance**
- ✅ **Acciones críticas** que requieren aprobación
- ❌ App simple sin roles complejos → documentar RBAC dentro de AppScreen

---

# ESPECIFICACIÓN ADMIN + RBAC

---

## 0) Metadatos del documento [OBL]

> **Activación:** Siempre obligatorio.

| Campo | Valor |
|-------|-------|
| **Nombre del documento** | Spec_AdminRBAC_{{NOMBRE_AREA}}_{{VERSION}} |
| **Proyecto** | {{NOMBRE_PROYECTO}} |
| **Módulo / Feature** | {{NOMBRE_MODULO}} (ej: Admin, Seguridad, Config Tenant) |
| **Pantalla/Área** | {{NOMBRE_AREA}} |
| **ID técnico** | `admin-{{NUM}}-{{SLUG}}` (ej: `admin-01-user-management`) |
| **Ruta** | `{{RUTA}}` (ej: `/admin/users`) |
| **Contexto** | [Elegir: Admin Panel / Enterprise App / SaaS Config] |
| **Versión** | {{VERSION}} |
| **Estado** | [Elegir: Draft / Review / Approved / Deprecated] |
| **Prioridad** | [Elegir: Crítica / Alta / Media / Baja] |
| **Fecha** | {{FECHA_YYYY-MM-DD}} |
| **Owner (PM/PO)** | {{NOMBRE_OWNER}} |
| **Security Owner** | {{NOMBRE_SECURITY}} |
| **UX/UI Owner** | {{NOMBRE_UX}} |
| **Tech Lead** | {{NOMBRE_TECH}} |
| **QA Owner** | {{NOMBRE_QA}} |

---

## 1) Propósito del área Admin [OBL]

> **Activación:** Siempre obligatorio.

### 1.1 Descripción general [OBL]

Este módulo permite administrar **{{RECURSOS}}** (usuarios, roles, permisos, configuración, auditoría).

| Campo | Valor |
|-------|-------|
| **Recursos administrados** | {{RECURSOS}} |
| **Nivel de riesgo** | [Elegir: Alto / Medio / Bajo] |
| **Compliance requerido** | {{COMPLIANCE}} (ej: SOC2, GDPR, HIPAA, ninguno) |

### 1.2 Objetivo de negocio [OBL]

1. {{OBJETIVO_1}} (ej: Control de acceso granular)
2. {{OBJETIVO_2}} (ej: Administración multi-tenant)
3. {{OBJETIVO_3}} (ej: Cumplimiento y auditoría)
4. {{OBJETIVO_4}} (ej: Reducir riesgos operativos)

### 1.3 Objetivo UX [OBL]

- Claridad de permisos (quién puede hacer qué)
- Prevenir cambios peligrosos (confirmaciones)
- Minimizar errores de configuración
- Permitir soporte eficiente

---

## 2) Alcance (Scope) [OBL]

> **Activación:** Siempre obligatorio.

### 2.1 Incluye (In Scope) [OBL]

- {{INCLUYE_1}} (ej: Gestión de usuarios)
- {{INCLUYE_2}} (ej: Roles y permisos)
- {{INCLUYE_3}} (ej: Asignación de roles a usuarios)
- {{INCLUYE_4}} (ej: Scopes - tenant/site/region)
- {{INCLUYE_5}} (ej: Audit log)
- {{INCLUYE_6}} (ej: Controles de riesgo)

### 2.2 No incluye (Out of Scope) [OBL]

- {{EXCLUYE_1}}
- {{EXCLUYE_2}}

### 2.3 Dependencias [OBL]

| Tipo | Dependencia | Estado | Owner |
|------|-------------|--------|-------|
| Identity Provider | {{IDP}} (ej: Auth0, Okta, interno) | [Pendiente/Listo] | {{OWNER}} |
| Directory/SCIM | {{SISTEMA}} | [Pendiente/Listo] | {{OWNER}} |
| Audit/Observability | {{SISTEMA}} | [Pendiente/Listo] | {{OWNER}} |
| Feature Flags | {{SISTEMA}} | [Pendiente/Listo] | {{OWNER}} |

---

## 3) Modelo de seguridad [OBL]

> **Activación:** Siempre obligatorio.

### 3.1 Conceptos clave [OBL]

| Concepto | Definición | Ejemplo |
|----------|------------|---------|
| **Subject** | Quién realiza la acción | Usuario, Grupo, Service Account |
| **Role** | Conjunto de permisos | Admin, Editor, Viewer |
| **Permission** | Acción sobre recurso | `user.write`, `order.delete` |
| **Resource** | Entidad/área afectada | User, Order, Settings |
| **Scope** | Alcance del permiso | Tenant, Site, Region, Project |

### 3.2 Políticas de seguridad [OBL]

| Política | Implementación |
|----------|----------------|
| **Default Deny** | Sin permiso explícito = denegado |
| **Least Privilege** | Mínimos permisos necesarios |
| **Separation of Duties (SoD)** | Roles críticos separados |
| **Audit Everything** | Toda acción admin se registra |

### 3.3 Modelo RBAC [OBL]

| Tipo | Descripción | Seleccionado |
|------|-------------|--------------|
| **RBAC básico** | User → Role → Permissions | ☐ |
| **RBAC jerárquico** | Roles heredan de otros roles | ☐ |
| **RBAC con scopes** | Permisos limitados por scope | ☐ |
| **ABAC** | Atributos adicionales (hora, IP, etc.) | ☐ |

---

## 4) Roles (Role Catalog) [OBL] — **SECCIÓN NÚCLEO**

> **Activación:** Siempre obligatorio.

### 4.1 Catálogo de roles [OBL]

| Role ID | Nombre | Descripción | Nivel riesgo | Asignable por | Scopes válidos | Sistema/Custom |
|---------|--------|-------------|--------------|---------------|----------------|----------------|
| `role-viewer` | Viewer | Solo lectura | Bajo | Admin | Tenant, Site | Sistema |
| `role-editor` | Editor | Crear y editar recursos | Medio | Admin | Tenant, Site | Sistema |
| `role-admin` | Admin | Administración completa | Alto | Super Admin | Tenant | Sistema |
| `role-super-admin` | Super Admin | Control total | Crítico | — (manual) | Global | Sistema |
| `role-{{ID}}` | {{NOMBRE}} | {{DESCRIPCION}} | {{NIVEL}} | {{ASIGNADOR}} | {{SCOPES}} | {{TIPO}} |

### 4.2 Roles del sistema vs custom [OBL]

| Tipo | Descripción | Editable | Eliminable |
|------|-------------|----------|------------|
| **Sistema** | Roles predefinidos | No | No |
| **Custom** | Creados por admin | Sí | Sí |

### 4.3 Reglas de asignación [OBL]

| Regla | Implementación |
|-------|----------------|
| Quién puede asignar roles | {{REGLA}} (ej: Solo Admin o superior) |
| Self-assignment | [Permitido / Prohibido] |
| Approval requerido | [Sí: para roles {{NIVEL}} / No] |
| Máximo roles por usuario | {{NUM}} o ilimitado |
| Roles mutuamente excluyentes | {{ROLES}} (ej: Approver ≠ Requester) |

### 4.4 Detalle por rol crítico [OBL]

> Repetir para roles de alto riesgo.

#### Rol: {{NOMBRE_ROL}}

| Campo | Valor |
|-------|-------|
| **Role ID** | `role-{{ID}}` |
| **Nombre** | {{NOMBRE}} |
| **Descripción** | {{DESCRIPCION}} |
| **Nivel de riesgo** | [Bajo/Medio/Alto/Crítico] |
| **Permisos incluidos** | {{PERMISOS}} |
| **Scopes válidos** | {{SCOPES}} |
| **Asignación requiere** | {{REQUISITOS}} (ej: Aprobación de Security) |
| **SoD conflicts** | {{ROLES_CONFLICTO}} |

---

## 5) Permisos (Permission Catalog) [OBL] — **SECCIÓN NÚCLEO**

> **Activación:** Siempre obligatorio.

### 5.1 Catálogo de permisos [OBL]

| Permission ID | Recurso | Acción | Descripción | Riesgo | Audit | Scope-able |
|---------------|---------|--------|-------------|--------|-------|------------|
| `user.read` | User | read | Ver usuarios | Bajo | No | Sí |
| `user.write` | User | write | Crear/editar usuarios | Medio | Sí | Sí |
| `user.delete` | User | delete | Eliminar usuarios | Alto | Sí | Sí |
| `role.read` | Role | read | Ver roles | Bajo | No | No |
| `role.assign` | Role | assign | Asignar roles | Alto | Sí | Sí |
| `config.read` | Config | read | Ver configuración | Bajo | No | Sí |
| `config.write` | Config | write | Cambiar configuración | Alto | Sí | Sí |
| `audit.read` | Audit | read | Ver audit log | Medio | No | Sí |
| `audit.export` | Audit | export | Exportar audit log | Medio | Sí | Sí |
| `{{PERM_ID}}` | {{RECURSO}} | {{ACCION}} | {{DESCRIPCION}} | {{RIESGO}} | Sí/No | Sí/No |

### 5.2 Convención de naming [OBL]

```
{resource}.{action}

Recursos: user, role, permission, config, audit, order, product, etc.
Acciones: read, write, create, update, delete, assign, approve, export
```

### 5.3 Permisos de alto riesgo [OBL]

| Permission ID | Por qué es alto riesgo | Controles adicionales |
|---------------|------------------------|----------------------|
| `role.assign` | Escalación de privilegios | Approval, Audit |
| `user.delete` | Pérdida de datos | Confirm modal, Audit |
| `config.write` | Afecta todo el tenant | Dual approval |
| `{{PERM}}` | {{RAZON}} | {{CONTROLES}} |

---

## 6) Matriz Role × Permission (RBAC Matrix) [OBL] — **SECCIÓN NÚCLEO**

> **Activación:** Siempre obligatorio.

### 6.1 Matriz de permisos [OBL]

| Role ↓ \ Permission → | `user.read` | `user.write` | `user.delete` | `role.read` | `role.assign` | `config.read` | `config.write` | `audit.read` | `audit.export` |
|------------------------|:-----------:|:------------:|:-------------:|:-----------:|:-------------:|:-------------:|:--------------:|:------------:|:--------------:|
| **Viewer** | ✅ | ❌ | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ |
| **Editor** | ✅ | ✅ | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ |
| **Admin** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Super Admin** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **{{ROL}}** | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |

### 6.2 Permisos con scope [OBL]

| Permission | Global | Tenant | Site | Region | Project |
|------------|:------:|:------:|:----:|:------:|:-------:|
| `user.read` | ❌ | ✅ | ✅ | ❌ | ❌ |
| `user.write` | ❌ | ✅ | ✅ | ❌ | ❌ |
| `config.write` | ❌ | ✅ | ❌ | ❌ | ❌ |
| `{{PERM}}` | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |

### 6.3 Herencia de roles [COND]

> **Activación:** Incluir si hay roles jerárquicos.

| Rol hijo | Hereda de | Permisos adicionales |
|----------|-----------|---------------------|
| Editor | Viewer | `user.write` |
| Admin | Editor | `user.delete`, `role.assign`, `config.write`, `audit.*` |
| {{ROL}} | {{PADRE}} | {{PERMISOS}} |

---

## 7) Áreas Admin (Admin Surface Inventory) [OBL]

> **Activación:** Siempre obligatorio.

### 7.1 Tabla de áreas [OBL]

| Área | Ruta | Objetivo | Componentes | Rol mínimo | Riesgo |
|------|------|----------|-------------|------------|--------|
| Users | `/admin/users` | Gestionar usuarios | DataGrid + Modals | Admin | Alto |
| Roles | `/admin/roles` | Gestionar roles | DataGrid + Matrix | Admin | Alto |
| Permissions | `/admin/permissions` | Ver permisos | DataGrid (read-only) | Admin | Medio |
| Audit Log | `/admin/audit` | Trazabilidad | DataGrid + Filters | Admin | Medio |
| Settings | `/admin/settings` | Config tenant | Forms | Admin | Alto |
| {{AREA}} | {{RUTA}} | {{OBJETIVO}} | {{COMPONENTES}} | {{ROL}} | {{RIESGO}} |

### 7.2 Navegación admin [OBL]

```
/admin
├── /users          → User Management
│   ├── /users/:id  → User Detail
│   └── /users/invite → Invite User
├── /roles          → Role Management
│   └── /roles/:id  → Role Detail + Permissions
├── /audit          → Audit Log
└── /settings       → Tenant Settings
```

---

## 8) Flujos críticos (Critical Flows) [OBL]

> **Activación:** Siempre obligatorio.

### 8.1 Gestión de usuarios [OBL]

#### Crear/Invitar usuario

```
1. Admin navega a Users
2. Click "Invitar usuario"
3. Ingresa email + rol inicial + scope
4. Sistema valida (email único, rol permitido)
5. Sistema envía invitación
6. Audit log: user_invited
7. Usuario acepta → cuenta activa
```

#### Desactivar usuario

```
1. Admin selecciona usuario
2. Click "Desactivar"
3. Sistema muestra confirmación (high-risk)
4. Admin confirma
5. Sistema desactiva (no elimina)
6. Audit log: user_deactivated
7. Sesiones activas terminadas
```

### 8.2 Asignación de roles [OBL]

```
1. Admin navega a usuario o rol
2. Click "Asignar rol"
3. Selecciona rol + scope
4. Sistema valida:
   - Admin tiene permiso role.assign
   - No hay conflictos SoD
   - Scope es válido
5. [Si requiere approval] → Workflow de aprobación
6. Sistema asigna rol
7. Audit log: role_assigned
8. Notificación al usuario (opcional)
```

### 8.3 Cambios de configuración [COND]

> **Activación:** Incluir si hay settings de tenant.

```
1. Admin navega a Settings
2. Edita configuración
3. Sistema muestra preview de cambio
4. Admin confirma (con warning si es crítico)
5. [Si requiere approval] → Workflow
6. Sistema aplica cambio
7. Audit log: config_changed (before/after)
8. [Si falla] → Rollback automático
```

---

## 9) Controles de riesgo (Safety Controls) [OBL]

> **Activación:** Siempre obligatorio.

### 9.1 Confirmaciones [OBL]

| Nivel de riesgo | Control requerido |
|-----------------|-------------------|
| Bajo | Ninguno |
| Medio | Confirm modal |
| Alto | Confirm modal + mensaje de advertencia |
| Crítico | Confirm modal + typing confirmation |

#### Ejemplo de typing confirmation:
```
Para eliminar este usuario, escribe "ELIMINAR" para confirmar:
[____________]
```

### 9.2 Aprobaciones (Dual Control) [COND]

> **Activación:** Incluir si hay workflow de aprobación.

| Acción | Requiere aprobación | Aprobador | SLA |
|--------|---------------------|-----------|-----|
| Asignar rol Admin | Sí | Super Admin | 24h |
| Cambiar config crítica | Sí | Security Owner | 4h |
| {{ACCION}} | Sí/No | {{ROL}} | {{SLA}} |

### 9.3 Prevención de lockout [OBL]

| Escenario | Prevención |
|-----------|------------|
| Último admin se desactiva | Bloquear acción + warning |
| Admin se quita rol a sí mismo | Warning + confirmación extra |
| Todos los super admins desactivados | Proceso manual de recovery |

### 9.4 Auditoría [OBL]

| Campo | Descripción | Requerido |
|-------|-------------|-----------|
| `actor_id` | Quién realizó la acción | Sí |
| `actor_role` | Rol del actor | Sí |
| `action` | Qué acción | Sí |
| `resource_type` | Tipo de recurso | Sí |
| `resource_id` | ID del recurso | Sí |
| `before` | Estado anterior (JSON) | Para updates |
| `after` | Estado nuevo (JSON) | Para updates |
| `timestamp` | Cuándo | Sí |
| `ip_address` | Desde dónde | Sí |
| `user_agent` | Con qué cliente | Opcional |

### 9.5 Retención de audit log [OBL]

| Configuración | Valor |
|---------------|-------|
| Retención mínima | {{PERIODO}} (ej: 1 año) |
| Retención máxima | {{PERIODO}} |
| Inmutabilidad | Sí (no editable, no eliminable) |
| Export disponible | Sí (CSV, JSON) |

---

*Continúa en Parte 2 (Secciones 10-18)...*
---

*...Continuación de Parte 1 (Secciones 0-9)*

---

## 10) UI Specs (Patrones) [OBL]

> **Activación:** Siempre obligatorio.

### 10.1 Componentes por área [OBL]

| Área | Componente principal | Template de referencia |
|------|---------------------|----------------------|
| User List | DataGrid | TEMPLATE_BASE_Spec_DataGrid |
| User Create/Edit | Modal + Form | TEMPLATE_BASE_Spec_ModalOverlay + Form |
| Role List | DataGrid | TEMPLATE_BASE_Spec_DataGrid |
| Role Matrix | Custom Matrix | — |
| Audit Log | DataGrid (read-only) | TEMPLATE_BASE_Spec_DataGrid |
| Settings | Forms | TEMPLATE_BASE_Spec_Form |

### 10.2 Patrones de UI admin [OBL]

| Patrón | Uso | Implementación |
|--------|-----|----------------|
| Confirmación destructiva | Delete, Deactivate | Modal con warning + CTA danger |
| Typing confirmation | Acciones críticas | Input que requiere texto exacto |
| Inline status | Estado de usuario/rol | Badge con color |
| Action menu | Acciones por fila | Dropdown o icon buttons |
| Bulk actions | Acciones masivas | Toolbar sobre grid |
| Diff view | Audit changes | Before/After side-by-side |

### 10.3 Vista de matriz RBAC [COND]

> **Activación:** Incluir si hay UI para editar permisos.

| Elemento | Implementación |
|----------|----------------|
| Filas | Roles |
| Columnas | Permisos (agrupados por recurso) |
| Celdas | Checkbox o toggle |
| Indicadores | Heredado vs directo |
| Acciones | Guardar cambios, Reset |

---

## 11) Datos, APIs e integraciones [OBL]

> **Activación:** Siempre obligatorio.

### 11.1 Endpoints [OBL]

| Endpoint | Método | Uso | Auth | Rol mínimo |
|----------|--------|-----|------|------------|
| `GET /api/admin/users` | GET | Listar usuarios | Bearer | Admin |
| `POST /api/admin/users/invite` | POST | Invitar usuario | Bearer | Admin |
| `GET /api/admin/users/:id` | GET | Detalle usuario | Bearer | Admin |
| `PATCH /api/admin/users/:id` | PATCH | Editar usuario | Bearer | Admin |
| `POST /api/admin/users/:id/deactivate` | POST | Desactivar | Bearer | Admin |
| `GET /api/admin/roles` | GET | Listar roles | Bearer | Admin |
| `POST /api/admin/roles` | POST | Crear rol custom | Bearer | Super Admin |
| `POST /api/admin/roles/assign` | POST | Asignar rol | Bearer | Admin |
| `DELETE /api/admin/roles/assign` | DELETE | Quitar rol | Bearer | Admin |
| `GET /api/admin/permissions` | GET | Listar permisos | Bearer | Admin |
| `GET /api/admin/audit` | GET | Audit log | Bearer | Admin |
| `POST /api/admin/audit/export` | POST | Exportar audit | Bearer | Admin |
| `GET /api/admin/settings` | GET | Config tenant | Bearer | Admin |
| `PATCH /api/admin/settings` | PATCH | Actualizar config | Bearer | Admin |

### 11.2 Payloads de ejemplo [OBL]

#### Invite User
```json
{
  "email": "user@example.com",
  "roles": [
    { "role_id": "role-editor", "scope": { "tenant_id": "tenant-123" } }
  ],
  "send_invite": true
}
```

#### Assign Role
```json
{
  "user_id": "user-456",
  "role_id": "role-admin",
  "scope": { "tenant_id": "tenant-123" }
}
```

### 11.3 Error handling [OBL]

| Código | Significado | UI |
|--------|-------------|-----|
| 400 | Validación fallida | Toast error + detalles |
| 401 | No autenticado | Redirect a login |
| 403 | Sin permisos | Error "No tienes acceso" |
| 404 | Recurso no encontrado | Error page |
| 409 | Conflicto (ej: email duplicado) | Toast error |
| 422 | Regla de negocio violada | Toast con explicación |
| 500 | Error servidor | Error state + retry |

### 11.4 Integraciones externas [COND]

> **Activación:** Incluir si hay integraciones de identidad.

| Integración | Tipo | Uso | Estado |
|-------------|------|-----|--------|
| SSO/SAML | Identity | Login enterprise | [Pendiente/Activo] |
| OIDC | Identity | Login OAuth | [Pendiente/Activo] |
| SCIM | Directory | Sync usuarios | [Pendiente/Activo] |
| SIEM | Observability | Export audit | [Pendiente/Activo] |

---

## 12) Estados (UX States) [OBL]

> **Activación:** Siempre obligatorio. Referencia: `UXStates_Pack_{{PROYECTO}}`

### 12.1 Estados por área [OBL]

| Área | Loading | Empty | Error | Partial Error |
|------|---------|-------|-------|---------------|
| User List | Skeleton grid | "No hay usuarios" | Error + retry | — |
| Role List | Skeleton grid | "No hay roles custom" | Error + retry | — |
| Audit Log | Skeleton grid | "Sin actividad" | Error + retry | — |
| Settings | Skeleton form | — | Error + retry | Sección falla |

### 12.2 Estados de acciones [OBL]

| Acción | Loading | Success | Error |
|--------|---------|---------|-------|
| Invite User | Spinner en botón | Toast + redirect | Toast error |
| Assign Role | Spinner | Toast success | Toast error |
| Deactivate | Spinner | Toast + update list | Toast error |
| Save Settings | Spinner | Toast success | Toast + rollback visual |

---

## 13) Accesibilidad (A11Y) [OBL]

> **Activación:** Siempre obligatorio.

### 13.1 DataGrids admin [OBL]

| Requisito | Implementación |
|-----------|----------------|
| Navegación | Keyboard arrows |
| Headers | `scope="col"` |
| Actions | Buttons con labels claros |
| Status | No solo color (usar texto/iconos) |

### 13.2 Modales de confirmación [OBL]

| Requisito | Implementación |
|-----------|----------------|
| Focus trap | Sí |
| Focus inicial | En CTA primario o cancel |
| Escape | Cierra modal |
| Anuncio | `role="alertdialog"` para destructivas |

### 13.3 Matriz RBAC [COND]

| Requisito | Implementación |
|-----------|----------------|
| Navegación | Arrow keys entre celdas |
| Toggle | Space para cambiar |
| Headers | Legibles por screen reader |
| Estado | Anunciar checked/unchecked |

---

## 14) Analytics / Instrumentación [OBL]

> **Activación:** Siempre obligatorio.

### 14.1 Eventos [OBL]

| Evento | Trigger | Payload |
|--------|---------|---------|
| `admin_view` | Vista de área admin | `area, actor_id, actor_role` |
| `user_invited` | Usuario invitado | `actor_id, target_email, roles` |
| `user_activated` | Usuario acepta invite | `user_id` |
| `user_deactivated` | Usuario desactivado | `actor_id, target_id, reason` |
| `user_deleted` | Usuario eliminado | `actor_id, target_id` |
| `role_created` | Rol custom creado | `actor_id, role_id, permissions` |
| `role_assigned` | Rol asignado | `actor_id, user_id, role_id, scope` |
| `role_removed` | Rol quitado | `actor_id, user_id, role_id` |
| `permission_changed` | Permiso de rol cambiado | `actor_id, role_id, permission, action` |
| `config_changed` | Configuración cambiada | `actor_id, setting, before, after` |
| `audit_viewed` | Audit log visto | `actor_id, filters` |
| `audit_exported` | Audit exportado | `actor_id, format, date_range, row_count` |

### 14.2 Métricas de seguridad [OBL]

| Métrica | Cálculo | Alerta si |
|---------|---------|-----------|
| Role assignments / día | Count por día | > {{UMBRAL}} |
| Failed permission checks | 403 count | > {{UMBRAL}}/hora |
| Admin actions / admin | Actions per actor | Desviación significativa |
| Privilege escalation attempts | Assign role > own level | Cualquiera |

---

## 15) QA / Casos de prueba [OBL]

> **Activación:** Siempre obligatorio.

### 15.1 Casos de RBAC [OBL]

| ID | Caso | Resultado esperado | Prioridad |
|----|------|-------------------|-----------|
| TR-01 | Viewer intenta editar usuario | 403 Forbidden | Crítica |
| TR-02 | Editor intenta asignar rol | 403 Forbidden | Crítica |
| TR-03 | Admin asigna rol dentro de scope | Éxito | Crítica |
| TR-04 | Admin asigna rol fuera de scope | 403 Forbidden | Crítica |
| TR-05 | Escalación de privilegios | Bloqueado | Crítica |

### 15.2 Casos de lockout prevention [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TL-01 | Desactivar último admin | Bloqueado + warning |
| TL-02 | Admin se quita rol a sí mismo (único) | Warning + confirmación extra |
| TL-03 | Eliminar rol con usuarios asignados | Warning + listar afectados |

### 15.3 Casos de audit [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TA-01 | Toda acción admin genera log | Log con todos los campos |
| TA-02 | Audit log inmutable | No se puede editar/eliminar |
| TA-03 | Export de audit | Archivo con todos los eventos |

### 15.4 Casos de acciones high-risk [OBL]

| ID | Caso | Resultado esperado |
|----|------|-------------------|
| TH-01 | Delete requiere confirmación | Modal con warning |
| TH-02 | Config crítica requiere typing | Input de confirmación |
| TH-03 | Acción con approval pendiente | Estado "pending approval" |

---

## 16) Riesgos, supuestos y decisiones [OBL]

> **Activación:** Siempre obligatorio.

### 16.1 Riesgos identificados [OBL]

| ID | Riesgo | Probabilidad | Impacto | Mitigación |
|----|--------|--------------|---------|------------|
| R-01 | Escalación de privilegios | [Alta/Media/Baja] | Crítico | Validación server-side, audit |
| R-02 | Lockout de admins | Baja | Alto | Prevención + recovery manual |
| R-03 | Audit log incompleto | Media | Alto | Tests, validación automática |
| R-04 | {{RIESGO}} | {{PROB}} | {{IMPACTO}} | {{MITIGACION}} |

### 16.2 Supuestos [OBL]

| ID | Supuesto | Validado |
|----|----------|----------|
| S-01 | Identity provider disponible | Sí/No |
| S-02 | Roles iniciales definidos | Sí/No |
| S-03 | Compliance requirements claros | Sí/No |
| S-04 | {{SUPUESTO}} | Sí/No |

### 16.3 Decisiones pendientes [OBL]

| ID | Tema | Decisión | Responsable | Fecha |
|----|------|----------|-------------|-------|
| D-01 | Catálogo final de roles | {{DECISION}} | Security + PM | {{FECHA}} |
| D-02 | Workflow de aprobación | {{DECISION}} | Security | {{FECHA}} |
| D-03 | Retención de audit | {{DECISION}} | Legal + Security | {{FECHA}} |
| D-04 | Scopes soportados | {{DECISION}} | Tech Lead | {{FECHA}} |

---

## 17) Checklist de aprobación [OBL]

> **Activación:** Siempre obligatorio.

### 17.1 Modelo de seguridad [OBL]

- [ ] Role Catalog completo (§4)
- [ ] Permission Catalog completo (§5)
- [ ] RBAC Matrix definida (§6)
- [ ] Scopes documentados
- [ ] SoD conflicts identificados

### 17.2 Controles [OBL]

- [ ] Confirmaciones por nivel de riesgo
- [ ] Lockout prevention implementado
- [ ] Audit log especificado
- [ ] Retención definida

### 17.3 UX/Técnica [OBL]

- [ ] Áreas admin mapeadas
- [ ] APIs documentadas
- [ ] Estados definidos
- [ ] Accesibilidad validada

### 17.4 QA/Compliance [OBL]

- [ ] Casos RBAC documentados
- [ ] Casos de escalación documentados
- [ ] Analytics instrumentado
- [ ] Compliance requirements mapeados

### 17.5 Firmas de aprobación [OBL]

| Rol | Nombre | Fecha | Status |
|-----|--------|-------|--------|
| PM/PO | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| Security Owner | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| UX/UI | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| Tech Lead | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |
| QA | {{NOMBRE}} | {{FECHA}} | [Pendiente/Aprobado] |

---

## 18) Particularidades del proyecto [OPC]

> **Activación:** Usar para configuraciones específicas.

### 18.1 Roles específicos del proyecto

| Role ID | Nombre | Particularidad |
|---------|--------|----------------|
| `role-{{ID}}` | {{NOMBRE}} | {{PARTICULARIDAD}} |

### 18.2 Excepciones al estándar

| Sección | Excepción | Justificación | Aprobado por |
|---------|-----------|---------------|--------------|
| {{SECCION}} | {{EXCEPCION}} | {{JUSTIFICACION}} | {{APROBADOR}} |

### 18.3 Notas adicionales

{{NOTAS}}

---

## 📋 ANEXOS RELACIONADOS

> Marcar los anexos que aplican:

- [ ] **DataGrid** → Para listas de usuarios/roles/audit
- [ ] **Form** → Para settings y creación
- [ ] **ModalOverlay** → Para confirmaciones y edición
- [ ] **Wizard** → Para onboarding de usuarios
- [ ] **UXStates** → Referencia a estándar global

---

## 🔁 GUÍA OPERATIVA PARA AGENTES

### Cómo usar este template:

1. **Copiar** el template
2. **Completar las 3 secciones núcleo primero:**
   - §4 Role Catalog
   - §5 Permission Catalog
   - §6 RBAC Matrix
3. **Validar con Security Owner**
4. **Reemplazar** placeholders `{{...}}`
5. **Validar** con checklist (§17)

### Secciones núcleo (mínimo viable):

- §0 Metadatos
- §3 Modelo de seguridad
- §4 **Role Catalog** ← CRÍTICO
- §5 **Permission Catalog** ← CRÍTICO
- §6 **RBAC Matrix** ← CRÍTICO
- §8 Flujos críticos
- §9 Controles de riesgo
- §11 APIs
- §14 Analytics (audit)
- §17 Checklist

### Validación cruzada:

- Cada rol en §4 debe tener fila en §6 (matriz)
- Cada permiso en §5 debe tener columna en §6 (matriz)
- Cada acción high-risk debe tener control en §9
- Cada acción admin debe tener evento en §14
- Cada área en §7 debe tener componente en §10

### Red flags a evitar:

- ❌ RBAC sin Role Catalog
- ❌ Permisos sin nivel de riesgo
- ❌ Acciones destructivas sin confirmación
- ❌ Sin prevención de lockout
- ❌ Audit log incompleto
- ❌ Sin validación server-side de permisos
- ❌ Self-assignment de roles sin control

---

> **Fin del template**  
> **Versión:** 2.0  
> **Última actualización:** {{FECHA_ACTUALIZACION}}
