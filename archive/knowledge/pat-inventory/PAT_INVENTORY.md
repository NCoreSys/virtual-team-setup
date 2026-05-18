# PAT Inventory — Memory Service GitHub Governance

**Proyecto**: Memory Service
**Org GitHub**: NCoreSys
**Fecha**: 2026-05-01
**Tarea**: MS-144 / INIT-E-01

> SEGURIDAD: Este archivo registra METADATA de PATs solamente.
> Los valores de tokens NUNCA se documentan aqui.

---

## PATs Requeridos (ADR-001 §D-ADR-001-A)

| PAT | Rol | Repos con Write | Repos con Read | Estado |
|-----|-----|----------------|----------------|--------|
| PAT_MEM_BE | Backend Developer | memory-service-backend | — | Pendiente creacion por Coordinador |
| PAT_MEM_FE | Frontend Developer | memory-service-frontend | — | Pendiente creacion por Coordinador |
| PAT_MEM_DO | DevOps Engineer | memory-service-project, memory-service-api | — | Pendiente creacion por Coordinador |
| PAT_MEM_TL | Tech Lead | memory-service-project, memory-service-api, memory-service-backend, memory-service-frontend | — | Pendiente creacion por Coordinador |
| PAT_MEM_PM | Project Manager | memory-service-project | memory-service-api, memory-service-backend, memory-service-frontend | Pendiente creacion por Coordinador |

---

## Como Crear los PATs (Instrucciones para Coordinador)

1. Ir a: github.com → Settings → Developer settings → Personal access tokens → Fine-grained tokens
2. Crear nuevo token con:
   - **Token name**: `PAT_MEM_BE` (o el nombre del PAT)
   - **Expiration**: 90 dias (recomendado)
   - **Resource owner**: NCoreSys
   - **Repository access**: Solo los repos listados arriba
   - **Permissions**: Contents → Read and write, Pull requests → Read and write
3. Guardar el valor en un gestor de passwords (NO en este repo)
4. Actualizar columna "Estado" en este archivo a "Activo - YYYY-MM-DD"

---

## Estado de Creacion

| PAT | Creado por Coordinador | Fecha | Expiracion |
|-----|----------------------|-------|-----------|
| PAT_MEM_BE | Pendiente | — | — |
| PAT_MEM_FE | Pendiente | — | — |
| PAT_MEM_DO | Pendiente | — | — |
| PAT_MEM_TL | Pendiente | — | — |
| PAT_MEM_PM | Pendiente | — | — |

---

## Politica de Rotacion

- Rotar cada 90 dias
- Notificar al agente correspondiente 7 dias antes de expiracion
- Responsable de rotacion: Martin Rivas (Coordinador)

---

**Ultima actualizacion**: 2026-05-01
**Referencia**: ADR-001 §D-ADR-001-A
