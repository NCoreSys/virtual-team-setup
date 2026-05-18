# GUÍA DE INTEGRATION AUDIT

**Documento:** INTEGRATION_AUDIT_CHECKLIST.md  
**Versión:** 1.1  
**Fecha:** 2026-03-30  
**Autor:** PJM-Agent  
**Aplica a:** Todos los proyectos con equipo de agentes  
**Estado:** 📋 ESTÁNDAR OBLIGATORIO

---

## 0. PROPÓSITO

Esta guía define el proceso estándar de Integration Audit para equipos de agentes virtuales. Es un documento **cross-sprint** que explica **cómo** hacer la auditoría — los handoffs de cada sprint definen **qué** auditar específicamente.

> **Regla fundamental:** La auditoría de integración verifica que la **implementación coincide con el plan**. Se ejecuta en Fase 3 (Validación), después del Code Review.

---

## 1. ¿QUÉ ES LA INTEGRATION AUDIT?

### 1.1 Definición

La Integration Audit es la validación formal de que:
- El código implementado respeta las decisiones arquitectónicas (ADRs)
- El schema de base de datos coincide con el modelo diseñado
- Los endpoints implementados coinciden con los contratos de API
- Los boundaries de módulos se respetan
- Las integraciones funcionan correctamente

### 1.2 Diferencia con Code Review

| Aspecto | Code Review | Integration Audit |
|---------|-------------|-------------------|
| **Enfoque** | Calidad del código | Coherencia con diseño |
| **Quién** | TL + Code Reviewer | AR (Architect) |
| **Cuándo** | Por cada PR | Al final del sprint |
| **Contra qué valida** | Patrones, tests, seguridad | ADRs, MODELO_DATOS, API_CONTRACT |
| **Granularidad** | Archivo/función | Sistema/módulo |

### 1.3 Responsable

El **AR (Architect)** es responsable de la Integration Audit. Si no hay AR asignado, el TL puede ejecutarla como fallback — pero en proyectos con AR formal (tarea AR-001 en VTT), la separación TL/AR es obligatoria. TL = calidad técnica; AR = coherencia arquitectónica.

---

## 2. PROCESO DE AUDITORÍA

### 2.1 Flujo Completo

```
Code Review completado (todos los PRs mergeados)
        │
        ▼
AR recibe notificación de TL
        │
        ▼
AR ejecuta Integration Audit usando checklists §3-§6
        │
        ├── Sin issues → AR firma APR-AR en VTT
        │
        └── Con issues:
                │
                ├── S1/S2 → Crea issues en VTT → NO firma hasta fix
                │
                └── S3/S4 → Documenta → Firma con observaciones
        │
        ▼
AR entrega reporte de auditoría
```

### 2.2 Timing

| Fase | Día típico | Duración |
|------|-----------|----------|
| Integration Audit | Día 7-8 del sprint | 2-4 horas |

### 2.3 Prerrequisitos

Antes de iniciar la auditoría, verificar:

```
[ ] Todos los PRs del sprint están mergeados
[ ] Code Review completado por TL
[ ] Tests pasando en CI
[ ] Documentación dinámica actualizada (.LOGIC.md, API_CONTRACT.md)
```

---

## 3. CHECKLIST: VALIDACIÓN DE ADRs

### 3.1 Template de Verificación

Para cada ADR del sprint, usar este template:

```markdown
## Verificación [ADR-XXX]

### Decisión Documentada
[Copiar resumen de la decisión del ADR]

### Items a Verificar
- [ ] Item 1 según ADR
- [ ] Item 2 según ADR
- [ ] Item 3 según ADR

### Evidencia
- [ ] [Tipo de evidencia requerida]

### Resultado
- [ ] ✅ CUMPLE
- [ ] ⚠️ CUMPLE PARCIALMENTE — [Observaciones]
- [ ] ❌ NO CUMPLE — [Issue ID]
```

### 3.2 Ejemplo de Verificación

```markdown
## Verificación ADR-AUTH-01

### Decisión Documentada
"Toda autenticación usa JWT con refresh tokens. Access token expira en 15 min, refresh en 7 días."

### Items a Verificar
- [ ] Middleware de auth usa JWT
- [ ] Access token TTL = 15 min
- [ ] Refresh token TTL = 7 días
- [ ] Endpoints protegidos requieren token válido

### Evidencia
- [ ] Screenshot de config con TTLs
- [ ] Curl de endpoint protegido sin token → 401
- [ ] Curl de endpoint protegido con token → 200

### Resultado
- [x] ✅ CUMPLE
```

---

## 4. CHECKLIST: MODELO DE DATOS

### 4.1 Verificación de Schema

```markdown
## Verificación Modelo de Datos

### Tablas Nuevas
Para cada tabla nueva del sprint:

| Tabla | En MODELO_DATOS | En DB real | Columnas match | Constraints match |
|-------|-----------------|------------|----------------|-------------------|
| [nombre] | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |

### Verificación Detallada por Tabla

#### Tabla: [nombre_tabla]

**Columnas:**
- [ ] Todas las columnas del diseño existen
- [ ] Tipos de datos correctos
- [ ] Nullability correcta
- [ ] Defaults correctos

**Constraints:**
- [ ] Primary Key correcto
- [ ] Foreign Keys implementadas
- [ ] UNIQUE constraints implementados
- [ ] CHECK constraints implementados

**Índices:**
- [ ] Índices de búsqueda frecuente creados
- [ ] Índices documentados en MODELO_DATOS

**Evidencia:**
```sql
\d nombre_tabla
```

[Pegar output aquí]
```

### 4.2 Verificación de Relaciones

```markdown
## Relaciones Entre Tablas

| Tabla origen | FK | Tabla destino | Implementada | ON DELETE |
|--------------|-------|---------------|--------------|-----------|
| [tabla_a] | [fk_col] | [tabla_b] | ✅/❌ | CASCADE/SET NULL/RESTRICT |

### Test de Integridad Referencial
- [ ] INSERT con FK inválida → Error
- [ ] DELETE de padre con hijos → Comportamiento esperado según ON DELETE
```

---

## 5. CHECKLIST: API ENDPOINTS

### 5.1 Verificación de Contratos

```markdown
## Verificación API

### Endpoints del Sprint

| Método | Path | En API_CONTRACT | Implementado | Response Schema |
|--------|------|-----------------|--------------|-----------------|
| GET | /api/[recurso] | ✅/❌ | ✅/❌ | ✅/❌ |
| POST | /api/[recurso] | ✅/❌ | ✅/❌ | ✅/❌ |

### Verificación Detallada por Endpoint

#### [METHOD] /api/[path]

**Request:**
- [ ] Body schema coincide con documentación
- [ ] Parámetros de query documentados
- [ ] Headers requeridos documentados

**Response:**
- [ ] Status codes correctos (200, 201, 400, 401, 404, 500)
- [ ] Response body coincide con schema documentado
- [ ] Errores siguen formato estándar

**Auth:**
- [ ] Requiere autenticación (si aplica)
- [ ] Permisos correctos (si aplica)

**Evidencia:**
```bash
curl -X [METHOD] [URL] -H "Authorization: Bearer [token]" -d '[body]'
```

[Pegar response aquí]
```

### 5.2 Verificación de Swagger/OpenAPI

```markdown
## Swagger/OpenAPI

- [ ] Swagger UI accesible
- [ ] Todos los endpoints del sprint documentados
- [ ] Schemas de request/response completos
- [ ] Ejemplos presentes

**Evidencia:**
- Screenshot de Swagger UI mostrando endpoints del sprint
```

---

## 6. CHECKLIST: BOUNDARIES E INTEGRACIONES

### 6.1 Verificación de Boundaries

```markdown
## Boundaries de Módulos

### Arquitectura Esperada
[Diagrama o descripción de la arquitectura de módulos]

### Verificación
- [ ] Módulo A no accede directamente a tablas de Módulo B
- [ ] Comunicación entre módulos via interfaces definidas
- [ ] No hay imports cruzados prohibidos
- [ ] Services respetan single responsibility

### Violaciones Encontradas
| Archivo | Violación | Severidad |
|---------|-----------|-----------|
| [path] | [descripción] | S1/S2/S3/S4 |
```

### 6.2 Verificación de Integraciones Externas

```markdown
## Integraciones Externas

### Servicios Integrados
| Servicio | Configurado | Conectividad | Fallback |
|----------|-------------|--------------|----------|
| [Redis] | ✅/❌ | ✅/❌ | ✅/❌ |
| [S3/MinIO] | ✅/❌ | ✅/❌ | ✅/❌ |
| [API Externa] | ✅/❌ | ✅/❌ | ✅/❌ |

### Tests de Conectividad
- [ ] Conexión a [servicio] funciona
- [ ] Timeout configurado correctamente
- [ ] Fallback funciona cuando servicio no disponible
- [ ] Errores de conexión no rompen la aplicación

### Evidencia
- [ ] Log de conexión exitosa
- [ ] Test de fallback con servicio caído
```

---

## 7. SEVERIDAD DE ISSUES

### 7.1 Clasificación

| Severidad | Definición | Ejemplos | Acción |
|-----------|------------|----------|--------|
| **S1 - Blocker** | Funcionalidad core rota | ADR violado que causa bugs, FK faltante causa data corruption | Fix inmediato, bloquea release |
| **S2 - Critical** | Feature importante no funciona | Endpoint retorna schema incorrecto, índice faltante causa timeout | Fix antes de release |
| **S3 - Major** | Feature secundaria afectada | Documentación desactualizada, naming inconsistente | Fix en sprint actual o siguiente |
| **S4 - Minor** | Cosmético, no afecta funcionalidad | Typo en comentario, orden de columnas diferente | Backlog |

### 7.2 Reglas de Firma

| Severidad encontrada | ¿AR puede firmar? |
|---------------------|-------------------|
| Sin issues | ✅ Sí |
| Solo S4 | ✅ Sí (documentar) |
| Solo S3 | ✅ Sí (documentar) |
| S2 presente | ❌ No hasta fix |
| S1 presente | ❌ No hasta fix |

---

## 8. FORMATO DE REPORTE

### 8.1 Template de Reporte

```markdown
# Reporte de Integration Audit — Sprint [N]

**Fecha:** YYYY-MM-DD  
**Auditor:** [Nombre]  
**Rol:** AR / TL  
**Proyecto:** [Nombre proyecto]

---

## 0. Resumen Ejecutivo

| Categoría | Items | Passed | Failed | % |
|-----------|-------|--------|--------|---|
| ADRs | X | X | X | X% |
| Modelo Datos | X | X | X | X% |
| API Endpoints | X | X | X | X% |
| Boundaries | X | X | X | X% |
| Integraciones | X | X | X | X% |
| **TOTAL** | **X** | **X** | **X** | **X%** |

---

## 1. ADRs Verificados

### ADR-XXX: [Título]
- **Estado:** ✅ CUMPLE / ⚠️ PARCIAL / ❌ NO CUMPLE
- **Observaciones:** [Si aplica]
- **Evidencia:** [Referencia a screenshots/logs]

[Repetir para cada ADR]

---

## 2. Modelo de Datos

### Tablas Verificadas
| Tabla | Estado | Observaciones |
|-------|--------|---------------|
| [nombre] | ✅/⚠️/❌ | [obs] |

### Issues Encontrados
[Lista de issues o "Ninguno"]

---

## 3. API Endpoints

### Endpoints Verificados
| Endpoint | Estado | Observaciones |
|----------|--------|---------------|
| [METHOD /path] | ✅/⚠️/❌ | [obs] |

### Issues Encontrados
[Lista de issues o "Ninguno"]

---

## 4. Boundaries e Integraciones

### Boundaries
- **Estado:** ✅ Sin violaciones / ❌ Violaciones encontradas
- **Detalle:** [Si aplica]

### Integraciones
| Servicio | Estado |
|----------|--------|
| [nombre] | ✅/❌ |

---

## 5. Issues Encontrados

| ID | Categoría | Descripción | Severidad | Asignado a |
|----|-----------|-------------|-----------|------------|
| IA-001 | [cat] | [desc] | S1/S2/S3/S4 | [agente] |

---

## 6. Observaciones Adicionales

[Notas, recomendaciones, deuda técnica identificada]

---

## 7. Decisión

- [ ] ✅ APROBADO — Sprint listo para release
- [ ] ⚠️ APROBADO CON CONDICIONES — Fix items S3/S4 post-release
- [ ] ❌ RECHAZADO — Fix items S1/S2 antes de release

**Firma AR:** _______________  
**Fecha:** _______________
```

---

## 9. INTEGRACIÓN CON VTT

### 9.1 Tarea de Integration Audit

| Campo | Valor típico |
|-------|--------------|
| ID | AR-XXX |
| Título | Integration Audit Sprint [N] |
| Agente | AR |
| Estimado | 2-4h |
| Complejidad | MEDIUM/HIGH |
| Categoría | review |
| Depende de | TL-XXX (Code Review) |

### 9.2 Estados

```
AR-XXX: Integration Audit
        │
        ├── task_in_progress (AR ejecutando auditoría)
        │
        ├── Sin issues S1/S2:
        │       │
        │       └── task_completed → AR firma APR-AR
        │
        └── Con issues S1/S2:
                │
                ├── POST /api/tasks/{taskId}/issues → tarea origen va a task_on_hold auto
                │
                ├── AR-XXX permanece en task_in_progress (AR espera fixes)
                │
                ├── TL crea FIX tasks → agentes resuelven → PUT /api/issues/{id}
                │
                └── Fixes confirmados → task_completed → AR firma APR-AR
```

### 9.3 Creación de Issues

Cuando se encuentra un issue:

```
POST /api/tasks/{taskId}/issues
{
    "title": "[IA-XXX] [Descripción corta]",
    "description": "[Descripción detallada]",
    "priorityId": "[UUID según severidad]",
    "category": "integration_audit"
}
```

> **Nota:** El campo `severity` es semántico para el reporte. Al crear el issue en VTT, usar `priorityId`:
> - S1 (Blocker) → Critical: `90ec3df2-fac4-40fa-b2ce-29daf0f4956e`
> - S2 (Critical) → High: `1a617554-6319-4c56-826f-8ef49a0ff9cc`
> - S3 (Major) → Medium: `d0b619ef-...`
> - S4 (Minor) → Low: `95f2e731-...`

---

## 10. AUTOMATIZACIÓN (OPCIONAL)

### 10.1 Scripts de Verificación

```bash
#!/bin/bash
# verify-schema.sh
# Compara schema real con MODELO_DATOS.md

echo "=== Verificando Schema ==="

# Extraer tablas del modelo
grep "### Tabla:" MODELO_DATOS.md | cut -d: -f2 | tr -d ' ' > expected_tables.txt

# Extraer tablas reales
psql -c "\dt" | grep "public" | awk '{print $3}' > actual_tables.txt

# Comparar
diff expected_tables.txt actual_tables.txt
```

```bash
#!/bin/bash
# verify-endpoints.sh
# Verifica que todos los endpoints documentados responden

echo "=== Verificando Endpoints ==="

# Extraer endpoints del contrato
grep -E "^(GET|POST|PUT|PATCH|DELETE)" API_CONTRACT.md > endpoints.txt

# Probar cada uno
while read line; do
    method=$(echo $line | awk '{print $1}')
    path=$(echo $line | awk '{print $2}')
    
    response=$(curl -s -o /dev/null -w "%{http_code}" -X $method "http://localhost:3000$path")
    
    if [ "$response" == "000" ]; then
        echo "❌ $method $path - No response"
    else
        echo "✅ $method $path - $response"
    fi
done < endpoints.txt
```

### 10.2 CI/CD Gate

```yaml
# .github/workflows/integration-audit-gate.yml

name: Integration Audit Gate

on:
  workflow_dispatch:
    inputs:
      sprint:
        description: 'Sprint number'
        required: true

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Verify DB schema
        run: ./scripts/verify-schema.sh
      
      - name: Verify API endpoints
        run: ./scripts/verify-endpoints.sh
      
      - name: Generate audit report
        run: ./scripts/generate-audit-report.sh > audit-report.md
      
      - name: Upload report
        uses: actions/upload-artifact@v3
        with:
          name: integration-audit-report
          path: audit-report.md
```

---

## 11. APÉNDICE: CHECKLIST RÁPIDO

### Pre-Auditoría

```
[ ] Todos los PRs mergeados
[ ] Code Review completado
[ ] CI verde
[ ] Documentación actualizada
[ ] ADRs del sprint identificados
```

### Durante Auditoría

```
[ ] ADRs verificados (§3)
[ ] Modelo de datos verificado (§4)
[ ] Endpoints verificados (§5)
[ ] Boundaries verificados (§6)
[ ] Issues clasificados por severidad
```

### Post-Auditoría

```
[ ] Reporte generado
[ ] Issues S1/S2 creados en VTT (si aplica)
[ ] Todos los issues S1/S2 resueltos y PUT /api/issues/{id} ejecutado
[ ] Tareas en on_hold volvieron a su previousStatus
[ ] APR-AR firmado (si aplica)
[ ] TL notificado del resultado
```

---

## 12. HISTORIAL DE VERSIONES

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | 2026-03-30 | PJM-Agent | Versión inicial estandarizada |
| 1.1 | 2026-03-30 | PJM-Agent | Correcciones: diagrama §9.2 con task_on_hold, priorityId en §9.3, pasos resolución on_hold en §11, fallback TL clarificado en §1.3 |

---

**FIN DEL DOCUMENTO**
