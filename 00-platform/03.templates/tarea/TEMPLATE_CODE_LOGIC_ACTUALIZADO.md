# Code Logic: [NOMBRE_ARCHIVO]

**Archivo fuente:** `src/path/to/file.js`  
**Última actualización:** YYYY-MM-DD  
**Actualizado por:** [Backend Engineer / Frontend Engineer / etc]

---

## Tabla de Contenidos

1. [Propósito del Archivo](#1-propósito-del-archivo)
2. [Stack Tecnológico](#2-stack-tecnológico)
3. [Configuración y Variables de Entorno](#3-configuración-y-variables-de-entorno)
4. [Costos y Límites](#4-costos-y-límites) *(si aplica)*
5. [Performance Metrics](#5-performance-metrics)
6. [Dependencias](#6-dependencias)
7. [Exports / Lo que expone](#7-exports--lo-que-expone)
8. [Lógica Detallada](#8-lógica-detallada)
9. [Ejemplos de Uso](#9-ejemplos-de-uso)
10. [Relación con Otros Archivos](#10-relación-con-otros-archivos)
11. [Seguridad y Validación](#11-seguridad-y-validación)
12. [Troubleshooting](#12-troubleshooting)
13. [Integraciones](#13-integraciones)
14. [Métricas y Monitoreo](#14-métricas-y-monitoreo)
15. [Testing](#15-testing)
16. [Consideraciones Importantes](#16-consideraciones-importantes)
17. [Mejoras Futuras](#17-mejoras-futuras)
18. [Historial de Cambios](#18-historial-de-cambios)

---

## 1. Propósito del Archivo

**Descripción breve (1-2 líneas):**  
[QUÉ hace este archivo y POR QUÉ existe. Ejemplo: "Servicio que maneja la lógica de negocio de autenticación con Clerk, coordinando entre validación de tokens y sincronización con base de datos."]

**Responsabilidad principal:**  
[Una frase clara. Ejemplo: "Validar usuarios autenticados y adjuntar información del usuario a cada request."]

---

## 2. Stack Tecnológico

### Engine / Framework Principal

**Tecnología Primaria:**
- **Nombre:** [Express.js / React / Prisma / etc]
- **Versión:** [4.18.2]
- **Repositorio:** [https://github.com/...]
- **Licencia:** [MIT / Apache 2.0]
- **Propósito:** [Para qué se usa en este archivo]

### Alternativas y Fallbacks *(si aplica)*

| Opción | Tipo | Cuándo se usa | Ventajas | Desventajas |
|--------|------|---------------|----------|-------------|
| Opción A | Primaria | Por defecto | Rápido, gratis | Requiere setup |
| Opción B | Fallback | Si A falla | No requiere setup | Costo $X |

### Flujo de Selección *(si tiene lógica de fallback)*

```
Request
   ↓
¿Condición?
  ↓ Sí     ↓ No
Opción A  Opción B
  ↓          ↓
Resultado ← ←
```

### Dependencias de Sistema

**Hardware Requirements:**
- **Mínimo:**
  - CPU: [specs]
  - RAM: [amount]
  - Disco: [space]

- **Recomendado:**
  - CPU: [specs]
  - RAM: [amount]
  - GPU: [si aplica]

**Software Requirements:**
- Node.js: [versión]
- PostgreSQL: [versión]
- Otras dependencias de sistema

---

## 3. Configuración y Variables de Entorno

### Variables Requeridas

```bash
# Autenticación
CLERK_SECRET_KEY=sk_test_...
CLERK_PUBLISHABLE_KEY=pk_test_...

# Base de datos
DATABASE_URL=postgresql://user:pass@host:5432/db

# [Otras categorías]
VARIABLE_NAME=value
```

### Configuración por Defecto

```javascript
// Valores por defecto si no se especifican
const DEFAULT_CONFIG = {
  timeout: 5000,
  retries: 3,
  cacheEnabled: true,
};
```

### Ejemplo de Configuración Completa

```yaml
# docker-compose.yml (si aplica)
service-name:
  environment:
    VAR1: value1
    VAR2: value2
```

---

## 4. Costos y Límites

### Costos por Uso *(si aplica, ej: APIs externas)*

| Proveedor | Servicio | Costo | Unidad | Ejemplo |
|-----------|----------|-------|--------|---------|
| Clerk | Autenticación | $25 | por 1000 MAU | 10K usuarios = $250/mes |
| OpenAI | Claude API | $3 | por 1M tokens | 1M tokens = $3 |

### Ejemplos de Costos Reales

**Ejemplo 1: Aplicación pequeña (1000 usuarios/mes)**
- Clerk: $25/mes
- Claude API: ~$10/mes
- Total: ~$35/mes

**Ejemplo 2: Aplicación mediana (10,000 usuarios/mes)**
- Clerk: $250/mes
- Claude API: ~$100/mes
- Total: ~$350/mes

### Rate Limits

**Service A:**
- Requests por minuto: 100
- Requests por día: 10,000
- Timeout: 30 segundos

**Service B:**
- [Límites específicos]

### Límites Técnicos

**Input:**
- Longitud máxima: 4096 caracteres
- Tipos soportados: JSON, Form-data
- Tamaño máximo: 50MB

**Output:**
- Formato: JSON
- Campos opcionales: X, Y, Z

### Comparación de Costos *(si hay alternativas)*

| Opción | Setup | Mensual | Anual | Break-even |
|--------|-------|---------|-------|------------|
| Opción A | $0 | $50 | $600 | - |
| Opción B | $0 | $25 | $300 | Mes 1 |
| Opción C (self-host) | $100 | $5 | $160 | Mes 3 |

---

## 5. Performance Metrics

### Tiempos de Procesamiento

| Operación | Tamaño Input | Tiempo Promedio | Tiempo Máximo |
|-----------|--------------|-----------------|---------------|
| Validar token | N/A | ~50ms | ~200ms |
| Consultar BD | Simple | ~20ms | ~100ms |
| Consultar BD | Compleja | ~100ms | ~500ms |
| API externa | N/A | ~200ms | ~2s |

### Throughput

**Con 1 instancia:**
- Requests por segundo: ~100
- Usuarios concurrentes: ~500

**Con 3 instancias (escalado):**
- Requests por segundo: ~300
- Usuarios concurrentes: ~1500

### Latencia End-to-End

```
Request → Middleware → Service → Database → Response
  ~5ms      ~50ms       ~100ms     ~20ms      ~10ms

Total: ~185ms (promedio)
```

### Cache Performance *(si aplica)*

**Métricas de Cache:**
- Hit rate promedio: 60%
- Tiempo respuesta (HIT): <10ms
- Tiempo respuesta (MISS): ~100ms
- Ahorro de costo: 40-60%

---

## 6. Dependencias

### Internas (otros archivos del proyecto)

```javascript
import { prisma } from '../config/prisma';           // Cliente BD
import { logger } from '../utils/logger';             // Sistema de logs
import UserService from '../services/userService';    // Lógica de usuarios
```

**Descripción de cada dependencia:**
- `prisma` - ORM para consultas a PostgreSQL
- `logger` - Sistema centralizado de logs
- `UserService` - Servicio de lógica de negocio de usuarios

### Externas (librerías NPM)

```json
{
  "@clerk/clerk-sdk-node": "^4.13.0",
  "express": "^4.18.2",
  "joi": "^17.9.0"
}
```

**Propósito de cada una:**
- `@clerk/clerk-sdk-node` - Validación de JWT y gestión de usuarios
- `express` - Framework web para routing
- `joi` - Validación de schemas

---

## 7. Exports / Lo que expone

### Funciones Exportadas

```javascript
module.exports = {
  functionName,           // Descripción breve
  anotherFunction,        // Descripción breve
  HelperClass,            // Descripción breve
};
```

### Interfaces TypeScript *(si aplica)*

```typescript
export interface UserData {
  id: string;
  email: string;
  // ...
}

export type AuthResult = 'success' | 'failed' | 'expired';
```

---

## 8. Lógica Detallada

### Función Principal: `functionName(params)`

**Firma:**
```javascript
async function functionName(param1, param2, options = {})
```

**Propósito:**  
[QUÉ hace esta función - 1-2 líneas]

**Parámetros:**
| Nombre | Tipo | Requerido | Default | Descripción |
|--------|------|-----------|---------|-------------|
| param1 | string | Sí | - | ID del usuario |
| param2 | object | No | {} | Opciones adicionales |
| options.retry | boolean | No | true | Si reintentar en caso de error |

**Retorna:**  
`Promise<Object>` - Objeto con estructura:
```javascript
{
  success: boolean,
  data: {...},
  error?: string
}
```

**Throws:**  
- `ValidationError` - Si los parámetros son inválidos
- `NotFoundError` - Si el recurso no existe
- `UnauthorizedError` - Si no tiene permisos

**Flujo de Ejecución:**

```
1. Validar parámetros de entrada
   ↓
2. Verificar autenticación
   ↓
3. Consultar base de datos
   ↓
4. Procesar resultado
   ↓
5. Retornar respuesta
```

**Pseudocódigo:**

```javascript
async function functionName(param1, param2, options) {
  // 1. Validar inputs
  if (!param1) throw new ValidationError('param1 is required');
  
  // 2. Buscar en BD
  const record = await prisma.table.findUnique({
    where: { id: param1 }
  });
  
  // 3. Verificar existencia
  if (!record) throw new NotFoundError('Record not found');
  
  // 4. Procesar lógica de negocio
  const processed = await processData(record, param2);
  
  // 5. Retornar
  return {
    success: true,
    data: processed
  };
}
```

**Ejemplo de uso:**

```javascript
try {
  const result = await functionName('user-123', { option: 'value' });
  console.log(result.data);
} catch (error) {
  console.error(error.message);
}
```

---

### Función Secundaria: `helperFunction()`

[Repetir estructura anterior para cada función importante]

---

## 9. Ejemplos de Uso

### Caso de Uso 1: [Nombre del caso]

**Contexto:**  
[Descripción de la situación]

**Código:**
```javascript
// Ejemplo completo funcional
const result = await service.method({
  param1: 'value',
  param2: 123
});

if (result.success) {
  console.log('Éxito:', result.data);
}
```

**Input esperado:**
```json
{
  "param1": "value",
  "param2": 123
}
```

**Output esperado:**
```json
{
  "success": true,
  "data": {
    "id": "xyz",
    "result": "processed"
  }
}
```

---

### Caso de Uso 2: [Manejo de errores]

**Código:**
```javascript
try {
  await service.method({ invalid: 'data' });
} catch (error) {
  if (error instanceof ValidationError) {
    console.error('Datos inválidos:', error.message);
  }
}
```

---

## 10. Relación con Otros Archivos

### Componentes que USAN este archivo:

**1. `routes/users.js`**
- **Qué usa:** `functionName()`
- **Para qué:** Validar usuario en endpoint GET /users/:id
- **Flujo:** Route → Controller → **Este Service** → Database

**2. `middleware/auth.js`**
- **Qué usa:** `validateToken()`
- **Para qué:** Autenticar requests entrantes
- **Flujo:** Request → **Este Middleware** → Route Handler

### Componentes que este archivo USA:

**1. `services/userService.js`**
- **Qué consume:** `getUserById()`
- **Para qué:** Obtener datos completos del usuario
- **Dependencia:** Crítica (sin esto no funciona)

**2. `utils/logger.js`**
- **Qué consume:** `logger.info()`, `logger.error()`
- **Para qué:** Registrar eventos y errores
- **Dependencia:** Opcional (puede funcionar sin logs)

### Diagrama de Flujo:

```
┌──────────────┐
│   Routes     │
└──────┬───────┘
       │
       ↓
┌──────────────┐
│ Controller   │
└──────┬───────┘
       │
       ↓
┌──────────────┐
│ Este Archivo │  ← ← ← ← ← ← ← ← ← ←
└──────┬───────┘                      ↑
       │                              │
       ↓                              │
┌──────────────┐             ┌───────────────┐
│   Prisma     │             │ UserService   │
└──────────────┘             └───────────────┘
```

---

## 11. Seguridad y Validación

### Validaciones de Input

**Validación de parámetros:**
```javascript
const schema = Joi.object({
  email: Joi.string().email().required(),
  password: Joi.string().min(8).required(),
  role: Joi.string().valid('admin', 'member', 'viewer')
});

const { error, value } = schema.validate(input);
if (error) throw new ValidationError(error.message);
```

**Checklist de validación:**
- [ ] Email debe ser formato válido
- [ ] Password mínimo 8 caracteres
- [ ] Role debe ser uno de los permitidos
- [ ] UserID debe ser UUID válido
- [ ] No permitir SQL injection (usar Prisma)

### Validaciones de Estado

- [ ] Usuario debe existir en BD
- [ ] Usuario no debe estar desactivado
- [ ] Token no debe estar expirado
- [ ] Request debe tener permisos

### Validaciones de Permisos

```javascript
// Verificar que usuario es Admin
if (user.role !== 'admin') {
  throw new ForbiddenError('Admin role required');
}

// Verificar que usuario es miembro del proyecto
const membership = await prisma.projectMember.findFirst({
  where: {
    projectId: projectId,
    userId: user.id
  }
});

if (!membership) {
  throw new ForbiddenError('Not a project member');
}
```

### Sanitización de Datos

```javascript
// Limpiar HTML tags
const sanitized = input.replace(/<[^>]*>/g, '');

// Escapar caracteres especiales
const escaped = input.replace(/[&<>"']/g, (char) => {
  const entities = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
  };
  return entities[char];
});
```

### Secrets y Credenciales

**❌ NUNCA:**
```javascript
// NO HACER ESTO
const apiKey = 'sk-hardcoded-key-abc123';
```

**✅ SIEMPRE:**
```javascript
// Usar variables de entorno
const apiKey = process.env.API_KEY;
if (!apiKey) throw new Error('API_KEY not configured');
```

---

## 12. Troubleshooting

### Error 1: [Nombre del error]

**Síntoma:**
```
Error: Token validation failed
```

**Causa:**  
El token JWT ha expirado o la firma es inválida.

**Solución:**
1. Verificar que `CLERK_SECRET_KEY` está correctamente configurado
2. Verificar que el token no ha expirado (verificar timestamp)
3. Regenerar token desde el cliente

**Código para debuggear:**
```javascript
console.log('Token:', token);
console.log('Decoded:', jwt.decode(token));
console.log('Secret:', process.env.CLERK_SECRET_KEY?.substring(0, 10) + '...');
```

---

### Error 2: [Otro error común]

[Repetir estructura anterior]

---

### Errores Conocidos

| Error | Frecuencia | Severidad | Workaround |
|-------|------------|-----------|------------|
| Connection timeout | Alta | Media | Incrementar timeout a 10s |
| Rate limit exceeded | Media | Baja | Implementar backoff |
| Invalid schema | Baja | Alta | Validar antes de enviar |

---

## 13. Integraciones

### Integración 1: Clerk (Autenticación)

**Propósito:**  
Validar tokens JWT y obtener información del usuario.

**Configuración:**
```javascript
import { clerkClient } from '@clerk/clerk-sdk-node';

const clerk = clerkClient({
  secretKey: process.env.CLERK_SECRET_KEY
});
```

**Flujo:**
```
Request → Extract token → Verify with Clerk → Get user data → Continue
```

**Código de ejemplo:**
```javascript
async function verifyUser(token) {
  const session = await clerk.verifyToken(token);
  const user = await clerk.users.getUser(session.userId);
  return user;
}
```

**Manejo de errores:**
- Si token inválido → 401 Unauthorized
- Si usuario no existe → 404 Not Found
- Si API de Clerk falla → 503 Service Unavailable

---

### Integración 2: [Otra integración]

[Repetir estructura anterior]

---

## 14. Métricas y Monitoreo

### Logs Importantes

**Éxito:**
```javascript
logger.info('User authenticated', {
  userId: user.id,
  email: user.email,
  timestamp: new Date()
});
```

**Error:**
```javascript
logger.error('Authentication failed', {
  error: error.message,
  token: token.substring(0, 20) + '...',
  timestamp: new Date()
});
```

### Eventos a Monitorear

| Evento | Nivel | Cuándo loguear | Qué incluir |
|--------|-------|----------------|-------------|
| User login | INFO | Cada login exitoso | userId, timestamp |
| Auth failed | WARN | Cada intento fallido | reason, ip |
| Token expired | WARN | Token expirado | userId, expiredAt |
| API error | ERROR | Error externo | service, statusCode |

### Métricas Clave (KPIs)

**Performance:**
- Tiempo promedio de respuesta: <200ms
- P95 latency: <500ms
- P99 latency: <1s

**Reliability:**
- Success rate: >99.5%
- Error rate: <0.5%
- Uptime: >99.9%

**Business:**
- Logins por día: [objetivo]
- Active users: [objetivo]
- Failed logins: <1%

### Alertas

**Configurar alertas cuando:**
- Error rate > 1% durante 5 minutos
- Latencia P95 > 1s durante 10 minutos
- Failed logins > 10 en 1 minuto (posible ataque)

---

## 15. Testing

### Unit Tests

**Archivo de test:** `__tests__/filename.test.js`

```javascript
describe('functionName', () => {
  it('should return success when user exists', async () => {
    const result = await functionName('user-123');
    expect(result.success).toBe(true);
    expect(result.data).toHaveProperty('id');
  });

  it('should throw error when user not found', async () => {
    await expect(
      functionName('invalid-id')
    ).rejects.toThrow(NotFoundError);
  });

  it('should validate email format', async () => {
    await expect(
      functionName('not-an-email')
    ).rejects.toThrow(ValidationError);
  });
});
```

### Integration Tests

```javascript
describe('Integration: Auth Flow', () => {
  it('should authenticate user end-to-end', async () => {
    // 1. Register user
    const token = await register({ email, password });
    
    // 2. Verify token
    const verified = await verifyToken(token);
    expect(verified.success).toBe(true);
    
    // 3. Access protected resource
    const data = await getProtectedData(token);
    expect(data).toBeDefined();
  });
});
```

### Test Coverage

**Objetivo:** >80% coverage

**Comandos:**
```bash
npm test                    # Ejecutar todos los tests
npm test -- --coverage      # Con coverage report
npm test -- --watch         # Watch mode para desarrollo
```

### Logs Esperados (Éxito)

```
[INFO] User authenticated successfully
  userId: user-abc123
  email: test@example.com
  timestamp: 2026-01-15T10:30:00Z

[INFO] Database query completed
  query: SELECT * FROM users WHERE id = ?
  duration: 23ms

[INFO] Response sent
  statusCode: 200
  duration: 185ms
```

### Logs Esperados (Error)

```
[ERROR] Authentication failed
  reason: Invalid token
  token: eyJhbGciOiJIUzI1NiIs...
  timestamp: 2026-01-15T10:30:00Z

[ERROR] Database connection failed
  error: Connection timeout
  retries: 3
  duration: 5000ms
```

---

## 16. Consideraciones Importantes

### Decisiones de Diseño

**1. ¿Por qué usar Clerk en lugar de Auth0?**
- Mejor DX (Developer Experience)
- Más económico para nuestro caso de uso
- Mejor integración con React
- Webhook más simple

**2. ¿Por qué soft delete en lugar de hard delete?**
- Cumplimiento legal (GDPR, retención de datos)
- Posibilidad de recuperación
- Auditoría de cambios

### Limitaciones Conocidas

- ❌ No soporta autenticación multi-factor (MFA) - Pendiente para v2
- ❌ No tiene cache de usuarios - Cada request golpea la BD
- ⚠️ Rate limit de Clerk puede ser alcanzado en picos de tráfico

### Trade-offs

| Decisión | Ventaja | Desventaja | Por qué la elegimos |
|----------|---------|------------|---------------------|
| Usar Clerk | Fácil de implementar | Vendor lock-in | Velocidad de desarrollo |
| Soft delete | Auditoría | BD más grande | Compliance |
| Sync vs Async | Más simple | Menos escalable | MVP primero |

### Performance Considerations

- ⚡ Query de usuarios incluye JOIN con projects → Puede ser lento con muchos proyectos
- 💡 Considerar agregar índice en `user.clerk_id`
- 💡 Considerar implementar cache Redis para tokens validados

---

## 17. Mejoras Futuras

### Próximas Funcionalidades

- [ ] Implementar cache Redis para tokens (ETA: Sprint 3)
- [ ] Agregar soporte para MFA (ETA: Sprint 5)
- [ ] Implementar rate limiting por usuario (ETA: Sprint 4)
- [ ] Optimizar queries con índices adicionales (ETA: Sprint 3)

### Optimizaciones Pendientes

**Performance:**
- Implementar batching de consultas a BD
- Usar connection pooling
- Agregar CDN para assets estáticos

**Seguridad:**
- Implementar rotación automática de secrets
- Agregar detección de anomalías en logins
- Implementar IP whitelisting

**Monitoreo:**
- Integrar con Sentry para error tracking
- Agregar dashboard de métricas en Grafana
- Implementar alertas proactivas

---

## 18. Historial de Cambios

| Fecha | Versión | Cambio | Autor |
|-------|---------|--------|-------|
| 2026-01-15 | 1.0 | Creación inicial del archivo | Backend Engineer |
| 2026-01-16 | 1.1 | Agregada validación de email | Backend Engineer |
| 2026-01-17 | 1.2 | Refactor de error handling | Backend Engineer |
| 2026-01-20 | 2.0 | Migración a Clerk desde JWT manual | Backend Engineer |

### Cambios Detallados

**v2.0 (2026-01-20):**
- Migración completa a Clerk
- Removidas funciones de JWT manual
- Agregado webhook para sincronización
- Actualizada documentación

**v1.2 (2026-01-17):**
- Refactorizado manejo de errores para ser más consistente
- Agregadas clases de error personalizadas
- Mejorados mensajes de error para el usuario

**v1.1 (2026-01-16):**
- Agregada validación de formato de email
- Fix de bug donde emails con + causaban error
- Agregados tests unitarios para validación

---

## Documentación Relacionada

**Development Log:** `knowledge/development-log/2026-01-15_F1-AUTH-01_webhook.md`  
**API Documentation:** `/docs/specs/05_Especificacion_APIs_REST.md`  
**Architecture:** `/docs/context/ARCHITECTURE.md`  
**Project Context:** `/docs/context/PROJECT_CONTEXT.md`

---

**Documento Versión:** 2.0  
**Last Updated:** 2026-01-15  
**Author:** [Nombre del Engineer]  
**Status:** [Draft / In Review / Complete]  
**Total Secciones:** 18
