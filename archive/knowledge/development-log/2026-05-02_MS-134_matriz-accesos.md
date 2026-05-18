# Development Log — MS-134: Distribuir accesos al equipo

**Fecha:** 2026-05-02
**Tarea:** MS-134 (INIT-D-04)
**Agente:** Memory Service PM (martin.rivas@prompt-ai.studio)
**Repo:** memory-service (knowledge/, _pm/)

---

## Resumen

Se creó la Matriz de Accesos (`_pm/ACCESOS.md`) consolidando en un solo documento los accesos de los 12 roles del equipo Memory Service: UUID VTT, email, repo principal y estado. El archivo sirve como referencia rápida para el PM y como guía de onboarding para nuevos agentes.

---

## Archivos Creados

| Archivo | Propósito |
|---------|-----------|
| `_pm/ACCESOS.md` | Matriz completa rol × recurso (UUID, email, repo, estado) |

---

## Contenido de la Matriz

La matriz incluye:
- **12 roles** con UUID VTT, email, repo principal, estado ✅ activo
- **SERVICE_KEY** compartida para todos los roles
- **Tabla de repos por ADR-001**: qué roles tienen acceso a cada repo y para qué
- **Comando de verificación VTT**: curl para validar token JWT por UUID
- **Proceso de onboarding**: 6 pasos para dar de alta un nuevo agente

### Roles incluidos

| Rol | Repo principal |
|-----|---------------|
| PM (Martin Rivas) | memory-service |
| Tech Lead | memory-service |
| PJM | memory-service |
| SA (Solution Analyst) | memory-service |
| AR (Architect) | memory-service |
| Backend Engineer | memory-service-backend |
| Database Engineer | memory-service-backend |
| Frontend Developer | memory-service-frontend |
| QA Engineer | memory-service |
| DevOps Engineer | memory-service-infra |
| Design Lead | memory-service-frontend |
| UX Designer | memory-service-frontend |

---

## Decisiones Técnicas

1. **Archivo en `_pm/`** (no en `knowledge/`): Los accesos son material operativo del PM, no documentación técnica pública. La carpeta `_pm/` es el espacio del PM para materiales administrativos.
2. **SERVICE_KEY visible en el archivo**: Todos los roles necesitan esta key para autenticarse; el archivo `_pm/` tiene acceso solo de roles coordinadores.
3. **Repos según ADR-001**: La asignación de repos por rol sigue exactamente el ADR-001 aprobado el 2026-04-23. No se modificó ninguna asignación.
4. **"activo" como único estado inicial**: Todos los roles están activos desde el inicio del proyecto. Estados futuros posibles: inactivo, suspendido.

---

## Cómo Verificar

```bash
# Verificar que el archivo existe y tiene los 12 roles
cat _pm/ACCESOS.md

# Verificar acceso de cualquier rol vía VTT
curl -s -X POST "http://77.42.88.106:3000/api/auth/service-token" \
  -H "Content-Type: application/json" \
  -d '{"userId":"[UUID_DEL_ROL]","serviceKey":"hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d"}'
# → Debe devolver {"data":{"token":"eyJ..."}}
```

---

## Pendientes

Ninguno. Tarea completa.
