# ASSIGNMENT: MS-130 - Documentar configuración VM en repo

**Task ID**: MS-130
**Brief ref**: INIT-C-04
**Titulo**: Documentar configuración VM en repo
**Repositorio destino**: memory-service (este repo)
**Asignado a**: DO (DevOps Engineer)
**Prioridad**: M (MEDIUM)
**Estimacion**: 1 hora
**Complejidad**: LOW
**Categoria**: deployment
**Generado por**: PJM
**Fecha asignacion**: 2026-05-01

---

## 1. Objetivo

Crear `docs/INFRASTRUCTURE.md` con toda la información operativa de la VM de producción.

**Resultado esperado:** `docs/INFRASTRUCTURE.md` committeado con las 6 secciones mínimas requeridas.

---

## 2. Contexto

La VM `77.42.88.106` es el servidor de producción para Memory Service. Sin este documento, ante un incidente o rebuild hay que reinventar toda la configuración desde cero. Es la fuente de verdad de infraestructura.

---

## 3. Archivos de Referencia (LEER ANTES DE EMPEZAR)

1. `.claude/rules/PROJECT_RULES.md` — reglas operativas v1.5
2. `.claude/rules/Proyect_data.md` — datos del proyecto (emails, UUIDs, service keys)
3. `memory-service-project/Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` — spec técnica (§4 Deployment)

---

## 4. Prerequisitos

- [ ] Acceso a información real de la VM (IP, paths, puertos confirmados)
- [ ] Acceso al repo `memory-service`
- [ ] Token VTT válido

---

## 5. Implementación — Archivo a Crear

**Ruta**: `docs/INFRASTRUCTURE.md`

### Secciones mínimas requeridas:

```markdown
# Infrastructure — Memory Service

## 1. Servidor de Producción

| Campo | Valor |
|-------|-------|
| IP | 77.42.88.106 |
| OS | [completar: Ubuntu 22.04 / etc.] |
| Usuario root | root |
| Acceso | SSH vía clave privada del DO |

## 2. Puertos

| Servicio | Puerto | Descripción |
|---------|--------|-------------|
| Memory Service API | 3002 | Backend Node.js |
| Memory Service UI | 3003 | Frontend |
| VTT Backend | 3000 | Virtual Teams Tracking API |

## 3. Paths del Servidor

| Path | Contenido |
|------|-----------|
| `/root/memory-service-storage/` | Almacenamiento principal del servicio |
| `/root/memory-service-backend/` | [completar: código del backend si aplica] |
| [otros paths relevantes] | [descripción] |

## 4. Variables de Entorno Esperadas

```env
NODE_ENV=production
PORT=3002
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
```

> Las variables reales están en `.env` en el servidor (NO commitear valores reales).

## 5. Schema de Backups y Retención

| Tipo | Frecuencia | Retención | Ubicación |
|------|-----------|-----------|-----------|
| Base de datos | [completar] | [completar] | [completar] |
| Archivos storage | [completar] | [completar] | [completar] |

**Procedimiento de backup manual**:
```bash
# [completar con comandos reales]
```

## 6. Procedimiento de Escalación al Admin VM

**Cuándo escalar**: fallo de servidor, pérdida de acceso SSH, problemas de red, disco lleno.

**Contacto Admin VM**:
- **Nombre**: Martin Rivas
- **Email**: martin.rivas@prompt-ai.studio
- **Urgente**: [canal de comunicación urgente]

**Información a proveer al escalar**:
1. Descripción del problema
2. Timestamp del primer síntoma
3. Logs relevantes (`journalctl -u memory-service --since "1 hour ago"`)
4. Acciones ya intentadas

## 7. Comandos Útiles

```bash
# Ver logs del servicio
journalctl -u memory-service -f

# Reiniciar servicio
systemctl restart memory-service

# Ver estado
systemctl status memory-service

# Conectar a la VM
ssh root@77.42.88.106
```

## 8. Historial de Cambios

| Fecha | Cambio | Autor |
|-------|--------|-------|
| 2026-05-XX | Documento inicial creado | DO |
```

---

## 6. Verificación

Abrir `docs/INFRASTRUCTURE.md` y verificar que cubre las 6 secciones:
- [ ] IP del servidor
- [ ] Puertos (3002 API, 3003 UI)
- [ ] Paths (`/root/memory-service-storage/`)
- [ ] Schema de backups + retención
- [ ] Procedimiento de escalación al Admin VM
- [ ] Variables de entorno esperadas

---

## 7. Entregables Requeridos

| # | Entregable | Ubicación |
|---|-----------|-----------|
| 1 | `docs/INFRASTRUCTURE.md` | `docs/` en repo `memory-service` |
| 2 | Development Log | `knowledge/development-log/2026-05-XX_MS-130_infrastructure-doc.md` |
| 3 | Code Logic | No aplica (documento, no código) |
| 4 | Commit + PR | Branch `feature/MS-130`, PR a `main` |

---

## 8. Workflow

```bash
# 1. Cambiar estado en VTT
curl -X PATCH "http://77.42.88.106:3000/api/tasks/[MS-130-UUID]/status" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"status":"task_in_progress","comment":"Creando docs/INFRASTRUCTURE.md"}'

# 2. Crear branch
git checkout -b feature/MS-130

# 3. Crear docs/INFRASTRUCTURE.md (sección 5)

# 4. Commit
git add docs/INFRASTRUCTURE.md
git commit -m "docs [MS-130]: Documentar configuración VM en docs/INFRASTRUCTURE.md

- IP servidor: 77.42.88.106
- Puertos: 3002 (API), 3003 (UI)
- Paths: /root/memory-service-storage/
- Schema de backups y retención
- Procedimiento de escalación al Admin VM
- Variables de entorno esperadas

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
Refs: #MS-130"

# 5. Push + PR
git push origin feature/MS-130
gh pr create --title "[MS-130] Documentar configuración VM" --body "Ver devlog para detalles." --base main

# 6. Cambiar estado
curl -X PATCH "http://77.42.88.106:3000/api/tasks/[MS-130-UUID]/status" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"status":"task_in_review","comment":"PR creado, pendiente revisión"}'
```

---

## 9. Notas

- Completar los campos marcados con `[completar]` con información real de la VM
- Si no tienes acceso SSH a la VM para verificar paths, coordinar con Martin Rivas
- **NO commitear credenciales reales** — solo estructura y nombres de variables

---

**Generado por**: PJM (Martin Rivas)
**Fecha**: 2026-05-01
**Version**: 1.0
