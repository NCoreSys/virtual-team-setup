# ADDENDUM — Bloque 0 Lite: Fundamentos Técnicos Memory Service R1

**Proyecto:** Memory Service
**Versión:** 1.0
**Fecha:** 2026-05-06
**Autor:** PM — Martin Rivas (`350831b2-e1ae-4dbe-b2eb-7e023ec2e103`)
**Estado:** BORRADOR PARA REVIEW SA
**Basado en:** SPEC_MANEJO_ERRORES_v1.1, SPEC_LOGS_OBSERVABILIDAD_v1.1, SPEC_SEGURIDAD_BASE_v1.1 (VTT/HybridFlow)

---

## 1. PROPÓSITO

Adaptar los 3 módulos fundacionales del Bloque 0 de VTT al contexto específico de Memory Service R1. Este addendum NO reemplaza las specs de VTT — las toma como base y define qué se implementa, qué se excluye y qué se adapta para un microservicio standalone de memoria de agentes.

### 1.1 Contexto de la decisión

Memory Service es un microservicio independiente (D-MEM-01) que será consumido por Runtime v1.1, Prompt Builder v1.3 y Hook Manager. Sus endpoints se dividen en dos grupos: service-to-service protegidos por SERVICE_KEY (import, context) y públicos consumidos por la UI (timeline, cost-report, dashboard). En R1 no tiene autenticación de usuarios, RBAC, ni Org/Workspace — esas capacidades se heredarán de VTT cuando estén disponibles.

Sin fundamentos técnicos, los 11 endpoints se implementarían con `console.log`, `catch(err) { res.status(500) }` y sin headers de seguridad. Este addendum evita eso con ~16h de esfuerzo.

### 1.2 Relación con las specs VTT

| Spec VTT | Horas VTT | Adaptación Memory Service | Horas MS |
|----------|:---------:|---------------------------|:--------:|
| SPEC_MANEJO_ERRORES_v1.1 | 12h | Sin circuit breaker ni retry service. Sin códigos AUTH/AUTHZ (no hay auth en R1). Taxonomía MEM-ERR-xxx específica. | 6h |
| SPEC_LOGS_OBSERVABILIDAD_v1.1 | 8h | Sin traceId, sin external API logger (no hay calls externos en R1). Winston + correlationId + request logger. | 5h |
| SPEC_SEGURIDAD_BASE_v1.1 | 14h | Sin cifrado AES/bcrypt (no hay passwords). Sin HTTPS/HSTS (VM interna). Helmet + rate limiting + CORS + Zod. | 5h |
| **Total** | **34h** | | **16h** |

### 1.3 Decisiones de alcance (5 preguntas críticas resueltas)

| # | Pregunta | Decisión | Justificación |
|:-:|----------|----------|---------------|
| 1 | ¿Org/Workspace propio? | **No.** Se hereda de VTT cuando RBAC esté listo. | D-MEM-01: standalone. No duplicar entidades de VTT. |
| 2 | ¿UI usa JWT propio? | **No.** Pública en R1 (SPEC §7.1). Adoptará JWT de VTT en R2. | Memory Service es consumidor de auth, no productor. |
| 3 | ¿Ingesta usa JWT o SERVICE_KEY? | **SERVICE_KEY** para system-to-system. Upload público en R1. | D-MEM-26: SERVICE_KEY pattern para R1. JWT en R2. |
| 4 | ¿Health visible para todos? | **Sí.** Público siempre. | Liveness probe estándar. No expone datos sensibles. |
| 5 | ¿CircuitBreaker en UI? | **No.** Es resiliencia interna. | La UI recibe errores estándar, no estado del breaker. |

---

## 2. MÓDULO 1 — ERROR HANDLING

### 2.1 Alcance Memory Service

| Incluido | Excluido (no aplica en R1) |
|----------|---------------------------|
| Taxonomía MEM-ERR-xxx | Circuit breaker (no hay APIs externas) |
| Clase AppError con isOperational | Retry service (cleanup job ya tiene su retry) |
| Error handler global | Códigos AUTH_*/AUTHZ_* (no hay auth en R1) |
| Mapper Prisma (P2002, P2025) | Graceful degradation |
| Mapper Zod | |
| Sanitización (no exponer stack traces) | |

### 2.2 Taxonomía de errores Memory Service

Las categorías se reducen a las que aplican en R1:

```typescript
// errors/types.ts
export type ErrorCategory =
  | 'VALIDATION'   // Datos de entrada inválidos
  | 'RESOURCE'     // No encontrado / conflicto
  | 'DOMAIN'       // Regla de negocio violada
  | 'EXTERNAL'     // Timeout de context (MEM-ERR-504)
  | 'INFRA'        // BD / storage / Redis
  | 'INTERNAL';    // Error inesperado

// AUTH y AUTHZ se agregan cuando VTT herede auth a Memory Service

export type ErrorSeverity = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

export interface ErrorDetail {
  field?: string;
  message: string;
  code?: string;
}

export interface ErrorResponse {
  error: string;
  code: string;
  details?: ErrorDetail[];
  correlationId: string;
  timestamp: string;
}
```

### 2.3 Catálogo de códigos MEM-ERR

Convención: `MEM_{CATEGORIA}_{DESCRIPCION}`

#### VALIDATION (400)

| Código | Descripción | Endpoint |
|--------|-------------|----------|
| `MEM_VALIDATION_FAILED` | Validación general falló | Todos |
| `MEM_VALIDATION_REQUIRED_FIELD` | Campo requerido faltante | POST /import, /upload |
| `MEM_VALIDATION_INVALID_FORMAT` | Formato de archivo inválido | POST /import, /upload |
| `MEM_VALIDATION_INVALID_SOURCE` | sourceCode no reconocido | POST /import |
| `MEM_VALIDATION_FILE_TOO_LARGE` | Archivo excede límite | POST /upload |

#### RESOURCE (404, 409)

| Código | HTTP | Descripción | Endpoint |
|--------|:----:|-------------|----------|
| `MEM_RESOURCE_NOT_FOUND` | 404 | Conversación/agente/proyecto no existe | GET /conversations/:id/*, GET /agents/:id/* |
| `MEM_RESOURCE_ALREADY_EXISTS` | 409 | Conversación ya importada (ALREADY_INDEXED) | POST /import |

#### DOMAIN (422)

| Código | Descripción | Endpoint |
|--------|-------------|----------|
| `MEM_DOMAIN_INVALID_CONVERSATION_TYPE` | Tipo de conversación no válido para este endpoint | POST /import vs /import-review |
| `MEM_DOMAIN_IMPORT_FAILED` | Import falló durante procesamiento | POST /import |
| `MEM_DOMAIN_CLASSIFICATION_FAILED` | Clasificación no pudo completarse | POST /import (no bloquea import) |

#### EXTERNAL (504)

| Código | HTTP | Descripción | Endpoint |
|--------|:----:|-------------|----------|
| `MEM_ERR_504` | 504 | Context generation timeout (<500ms) | GET /context |

**Nota:** `MEM-ERR-504` ya existe en SPEC v1.9 §11. Se integra en esta taxonomía.

#### INFRA (500, 503)

| Código | HTTP | Descripción | Cuándo |
|--------|:----:|-------------|--------|
| `MEM_INFRA_DATABASE_ERROR` | 500 | Error de PostgreSQL | Cualquier query fallida |
| `MEM_INFRA_DATABASE_UNAVAILABLE` | 503 | BD no disponible | Health check, startup |
| `MEM_INFRA_STORAGE_ERROR` | 500 | Error escribiendo/leyendo /storage/ | POST /import, GET /content |
| `MEM_INFRA_STORAGE_UNAVAILABLE` | 503 | Volumen /storage/ no accesible | Health check |
| `MEM_INFRA_REDIS_ERROR` | 500 | Error de Redis | Rate limiting, cache |

#### INTERNAL (500)

| Código | Descripción |
|--------|-------------|
| `MEM_INTERNAL_ERROR` | Error genérico inesperado |
| `MEM_INTERNAL_UNEXPECTED` | Bug, null pointer, etc. |

### 2.4 Clase AppError

```typescript
// errors/app-error.ts
import { ErrorCategory, ErrorSeverity, ErrorDetail } from './types';

export class AppError extends Error {
  public readonly code: string;
  public readonly httpStatus: number;
  public readonly category: ErrorCategory;
  public readonly severity: ErrorSeverity;
  public readonly isOperational: boolean;
  public readonly isRetryable: boolean;
  public readonly details?: ErrorDetail[];

  constructor(params: {
    message: string;
    code: string;
    httpStatus: number;
    category: ErrorCategory;
    severity?: ErrorSeverity;
    isOperational?: boolean;
    isRetryable?: boolean;
    details?: ErrorDetail[];
  }) {
    super(params.message);
    this.code = params.code;
    this.httpStatus = params.httpStatus;
    this.category = params.category;
    this.severity = params.severity || 'MEDIUM';
    this.isOperational = params.isOperational ?? true;
    this.isRetryable = params.isRetryable ?? false;
    this.details = params.details;
    Object.setPrototypeOf(this, AppError.prototype);
  }

  // Factory methods para Memory Service
  static validationFailed(details?: ErrorDetail[]) {
    return new AppError({
      message: 'Validation failed',
      code: 'MEM_VALIDATION_FAILED',
      httpStatus: 400,
      category: 'VALIDATION',
      severity: 'LOW',
      details,
    });
  }

  static notFound(resource: string) {
    return new AppError({
      message: `${resource} not found`,
      code: 'MEM_RESOURCE_NOT_FOUND',
      httpStatus: 404,
      category: 'RESOURCE',
      severity: 'LOW',
    });
  }

  static alreadyExists(resource: string) {
    return new AppError({
      message: `${resource} already exists`,
      code: 'MEM_RESOURCE_ALREADY_EXISTS',
      httpStatus: 409,
      category: 'RESOURCE',
      severity: 'LOW',
    });
  }

  static contextTimeout() {
    return new AppError({
      message: 'Context generation timeout',
      code: 'MEM_ERR_504',
      httpStatus: 504,
      category: 'EXTERNAL',
      severity: 'MEDIUM',
      isRetryable: true,
    });
  }

  static storageError(detail: string) {
    return new AppError({
      message: `Storage error: ${detail}`,
      code: 'MEM_INFRA_STORAGE_ERROR',
      httpStatus: 500,
      category: 'INFRA',
      severity: 'HIGH',
    });
  }

  static databaseError(detail: string) {
    return new AppError({
      message: `Database error: ${detail}`,
      code: 'MEM_INFRA_DATABASE_ERROR',
      httpStatus: 500,
      category: 'INFRA',
      severity: 'HIGH',
    });
  }
}
```

### 2.5 Error Handler Global

```typescript
// middleware/error-handler.middleware.ts
import { Request, Response, NextFunction } from 'express';
import { AppError } from '../errors/app-error';
import { logger } from '../services/logger.service';
import { Prisma } from '@prisma/client';
import { ZodError } from 'zod';

export function errorHandler(
  err: Error,
  req: Request,
  res: Response,
  _next: NextFunction
): void {
  const correlationId = req.correlationId || 'unknown';
  const timestamp = new Date().toISOString();

  // 1. AppError — operacional, controlado
  if (err instanceof AppError) {
    const logLevel = err.httpStatus >= 500 ? 'error' : 'warn';
    logger.log(logLevel, err.message, {
      correlationId,
      code: err.code,
      category: err.category,
      severity: err.severity,
      httpStatus: err.httpStatus,
    });

    res.status(err.httpStatus).json({
      error: err.message,
      code: err.code,
      details: err.details,
      correlationId,
      timestamp,
    });
    return;
  }

  // 2. Prisma errors — mapear a AppError
  if (err instanceof Prisma.PrismaClientKnownRequestError) {
    const mapped = mapPrismaError(err);
    logger.warn(mapped.message, {
      correlationId,
      code: mapped.code,
      prismaCode: err.code,
    });

    res.status(mapped.httpStatus).json({
      error: mapped.message,
      code: mapped.code,
      correlationId,
      timestamp,
    });
    return;
  }

  // 3. Zod errors — validación
  if (err instanceof ZodError) {
    const details = err.errors.map(e => ({
      field: e.path.join('.'),
      message: e.message,
    }));

    logger.warn('Validation failed', {
      correlationId,
      code: 'MEM_VALIDATION_FAILED',
      details,
    });

    res.status(400).json({
      error: 'Validation failed',
      code: 'MEM_VALIDATION_FAILED',
      details,
      correlationId,
      timestamp,
    });
    return;
  }

  // 4. Error no operacional — sanitizar
  logger.error('Unhandled error', {
    correlationId,
    code: 'MEM_INTERNAL_ERROR',
    stack: err.stack,
    message: err.message,
  });

  res.status(500).json({
    error: 'Internal server error',
    code: 'MEM_INTERNAL_ERROR',
    correlationId,
    timestamp,
  });
}

function mapPrismaError(err: Prisma.PrismaClientKnownRequestError): AppError {
  switch (err.code) {
    case 'P2002':
      return AppError.alreadyExists('Resource');
    case 'P2025':
      return AppError.notFound('Resource');
    default:
      return AppError.databaseError(`Prisma error ${err.code}`);
  }
}
```

### 2.6 Not Found Handler

```typescript
// middleware/not-found.middleware.ts
import { Request, Response } from 'express';

export function notFoundHandler(req: Request, res: Response): void {
  res.status(404).json({
    error: `Route ${req.method} ${req.path} not found`,
    code: 'MEM_RESOURCE_NOT_FOUND',
    correlationId: req.correlationId,
    timestamp: new Date().toISOString(),
  });
}
```

### 2.7 Async Handler Utility

```typescript
// utils/async-handler.ts
import { Request, Response, NextFunction, RequestHandler } from 'express';

export function asyncHandler(fn: RequestHandler): RequestHandler {
  return (req: Request, res: Response, next: NextFunction) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
}
```

---

## 3. MÓDULO 2 — LOGGING

### 3.1 Alcance Memory Service

| Incluido | Excluido (no aplica en R1) |
|----------|---------------------------|
| Winston logger con JSON estructurado | traceId / Runtime context fields |
| CorrelationId middleware | External API logger (no hay calls externos) |
| Request logger middleware | Loki/Grafana integration (infra de VTT) |
| Sanitización de datos sensibles | File transports (stdout es suficiente para Docker) |
| Niveles por ambiente | |

### 3.2 Logger Service

```typescript
// services/logger.service.ts
import winston from 'winston';

const { combine, timestamp, json, printf, colorize } = winston.format;

const isDev = process.env.NODE_ENV !== 'production';

const devFormat = combine(
  colorize(),
  timestamp({ format: 'HH:mm:ss' }),
  printf(({ timestamp, level, message, correlationId, ...meta }) => {
    const corrId = correlationId ? `[${correlationId}]` : '';
    const metaStr = Object.keys(meta).length ? JSON.stringify(meta) : '';
    return `${timestamp} ${level} ${corrId} ${message} ${metaStr}`;
  })
);

const prodFormat = combine(
  timestamp({ format: 'YYYY-MM-DDTHH:mm:ss.SSSZ' }),
  json()
);

export const logger = winston.createLogger({
  level: isDev ? 'debug' : 'info',
  format: isDev ? devFormat : prodFormat,
  defaultMeta: { service: 'memory-service' },
  transports: [
    new winston.transports.Console(),
  ],
});
```

### 3.3 CorrelationId Middleware

```typescript
// middleware/correlation-id.middleware.ts
import { Request, Response, NextFunction } from 'express';
import { randomUUID } from 'crypto';

declare global {
  namespace Express {
    interface Request {
      correlationId: string;
    }
  }
}

export function correlationIdMiddleware(
  req: Request,
  res: Response,
  next: NextFunction
): void {
  const correlationId =
    (req.headers['x-correlation-id'] as string) || randomUUID();

  req.correlationId = correlationId;
  res.setHeader('X-Correlation-ID', correlationId);

  next();
}
```

### 3.4 Request Logger Middleware

```typescript
// middleware/request-logger.middleware.ts
import { Request, Response, NextFunction } from 'express';
import { logger } from '../services/logger.service';

export function requestLoggerMiddleware(
  req: Request,
  res: Response,
  next: NextFunction
): void {
  const startTime = Date.now();

  // Log de entrada (solo en debug)
  logger.debug('Request received', {
    correlationId: req.correlationId,
    method: req.method,
    path: req.path,
    ip: req.ip,
  });

  // Log de salida
  res.on('finish', () => {
    const duration = Date.now() - startTime;
    const logLevel = res.statusCode >= 500 ? 'error'
                   : res.statusCode >= 400 ? 'warn'
                   : 'info';

    logger.log(logLevel, 'Request completed', {
      correlationId: req.correlationId,
      method: req.method,
      path: req.path,
      statusCode: res.statusCode,
      duration,
    });
  });

  next();
}
```

### 3.5 Log Sanitizer

```typescript
// utils/log-sanitizer.ts
const SENSITIVE_FIELDS = [
  'password', 'token', 'secret', 'apikey', 'api_key',
  'authorization', 'cookie', 'servicekey', 'service_key',
];

export function sanitizeForLogging(obj: any): any {
  if (!obj || typeof obj !== 'object') return obj;
  const sanitized = { ...obj };
  for (const key of Object.keys(sanitized)) {
    const lowerKey = key.toLowerCase();
    if (SENSITIVE_FIELDS.some(f => lowerKey.includes(f))) {
      sanitized[key] = '[REDACTED]';
    } else if (typeof sanitized[key] === 'object') {
      sanitized[key] = sanitizeForLogging(sanitized[key]);
    }
  }
  return sanitized;
}
```

---

## 4. MÓDULO 3 — SEGURIDAD BASE

### 4.1 Alcance Memory Service

| Incluido | Excluido (no aplica en R1) |
|----------|---------------------------|
| Helmet.js (headers de seguridad) | Cifrado AES-256 (no hay datos cifrados) |
| Rate limiting con Redis prefix `mem` | bcrypt (no hay passwords) |
| CORS por ambiente | HTTPS/HSTS (VM interna, acceso directo) |
| Validación Zod middleware | Secrets rotation (SERVICE_KEY es única) |
| Env validation | |

### 4.2 Helmet.js

```typescript
// middleware/helmet.middleware.ts
import helmet from 'helmet';

const isDev = process.env.NODE_ENV !== 'production';

export const helmetMiddleware = helmet({
  contentSecurityPolicy: isDev ? false : {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:"],
      connectSrc: ["'self'"],
      fontSrc: ["'self'"],
      objectSrc: ["'none'"],
      frameSrc: ["'none'"],
    },
  },
  crossOriginEmbedderPolicy: !isDev,
});
```

### 4.3 Rate Limiting

```typescript
// middleware/rate-limit.middleware.ts
import rateLimit from 'express-rate-limit';
// Usar Redis store cuando disponible, memory como fallback
// import RedisStore from 'rate-limit-redis';

// General: 100 requests / 15 min
export const generalRateLimit = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  standardHeaders: true,
  legacyHeaders: false,
  message: {
    error: 'Too many requests',
    code: 'MEM_RATE_LIMITED',
    message: 'Please retry after the window resets',
  },
});

// Import: más restrictivo (archivos pesados)
export const importRateLimit = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 30,
  standardHeaders: true,
  legacyHeaders: false,
  message: {
    error: 'Too many import requests',
    code: 'MEM_RATE_LIMITED',
    message: 'Import rate limit exceeded',
  },
});
```

### 4.4 CORS

```typescript
// middleware/cors.middleware.ts
import cors from 'cors';

const isDev = process.env.NODE_ENV !== 'production';

const allowedOrigins = isDev
  ? ['http://localhost:3003', 'http://localhost:3000']
  : [process.env.UI_ORIGIN || 'http://localhost:3003'];

export const corsMiddleware = cors({
  origin: allowedOrigins,
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Correlation-ID'],
  exposedHeaders: ['X-Correlation-ID'],
  credentials: false, // Sin cookies en R1
});
```

### 4.5 Validación Zod Middleware

```typescript
// middleware/validate.middleware.ts
import { Request, Response, NextFunction } from 'express';
import { AnyZodObject, ZodError } from 'zod';

export function validate(schema: AnyZodObject) {
  return (req: Request, _res: Response, next: NextFunction) => {
    try {
      schema.parse({
        body: req.body,
        query: req.query,
        params: req.params,
      });
      next();
    } catch (error) {
      // ZodError será capturado por el error handler global
      next(error);
    }
  };
}
```

### 4.6 Env Validation

```typescript
// config/env.ts
import { z } from 'zod';

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
  PORT: z.coerce.number().default(3002),
  DATABASE_URL: z.string().min(1),
  REDIS_URL: z.string().default('redis://shared-redis:6379'),
  REDIS_PREFIX: z.string().default('mem'),
  SERVICE_KEY: z.string().min(1),
  STORAGE_PATH: z.string().default('/storage'),
  UI_ORIGIN: z.string().optional(),
});

export const env = envSchema.parse(process.env);
```

---

## 5. INTEGRACIÓN EN APP.TS

```typescript
// app.ts — Orden de middleware con Bloque 0 Lite
import express from 'express';
import { initCatalogCache } from './services/catalog-cache.service';

// Bloque 0: Seguridad Base
import { helmetMiddleware } from './middleware/helmet.middleware';
import { corsMiddleware } from './middleware/cors.middleware';
import { generalRateLimit } from './middleware/rate-limit.middleware';

// Bloque 0: Logging
import { correlationIdMiddleware } from './middleware/correlation-id.middleware';
import { requestLoggerMiddleware } from './middleware/request-logger.middleware';

// Bloque 0: Error Handling
import { notFoundHandler } from './middleware/not-found.middleware';
import { errorHandler } from './middleware/error-handler.middleware';

// Auth existente (SPEC v1.9 §7.2)
import { requireServiceKey } from './middleware/auth';

const app = express();

async function bootstrap() {
  // 1. Catalog cache (SPEC v1.9 §3.3)
  await initCatalogCache();

  // 2. Seguridad Base
  app.use(helmetMiddleware);
  app.use(corsMiddleware);
  app.use(generalRateLimit);

  // 3. Parsing
  app.use(express.json({ limit: '10mb' }));

  // 4. Observabilidad
  app.use(correlationIdMiddleware);
  app.use(requestLoggerMiddleware);

  // 5. Rutas (SPEC v1.9 §8)
  // ... routes con requireServiceKey donde aplica

  // 6. Error Handling (siempre al final)
  app.use(notFoundHandler);
  app.use(errorHandler);

  app.listen(env.PORT, () => {
    logger.info(`Memory Service running on port ${env.PORT}`);
  });
}

bootstrap();
```

---

## 6. ESTRUCTURA DE ARCHIVOS

```
src/
├── config/
│   └── env.ts                          # Env validation con Zod
├── errors/
│   ├── types.ts                        # ErrorCategory, ErrorSeverity, interfaces
│   └── app-error.ts                    # AppError class + factory methods
├── middleware/
│   ├── helmet.middleware.ts             # Headers de seguridad
│   ├── cors.middleware.ts              # CORS por ambiente
│   ├── rate-limit.middleware.ts        # Rate limiting general + import
│   ├── validate.middleware.ts          # Zod validation
│   ├── correlation-id.middleware.ts    # CorrelationId
│   ├── request-logger.middleware.ts    # Request/response logging
│   ├── not-found.middleware.ts         # 404 handler
│   ├── error-handler.middleware.ts     # Global error handler
│   └── auth.ts                         # SERVICE_KEY (ya en SPEC v1.9)
├── services/
│   └── logger.service.ts              # Winston configurado
├── utils/
│   ├── async-handler.ts               # Promise wrapper para routes
│   └── log-sanitizer.ts              # Sanitización de datos sensibles
```

---

## 7. SPRINT S00 — FOUNDATION

### 7.1 Plan de implementación

| ID | Tarea | Horas | Dependencia |
|----|-------|:-----:|-------------|
| S00-01 | Env validation con Zod (`config/env.ts`) | 1h | — |
| S00-02 | Helmet.js + CORS middleware | 2h | S00-01 |
| S00-03 | Rate limiting (general + import) | 1h | S00-01 |
| S00-04 | Winston logger service | 1h | S00-01 |
| S00-05 | CorrelationId + request logger middleware | 2h | S00-04 |
| S00-06 | Error types + AppError class + factories | 2h | — |
| S00-07 | Error handler global + Prisma/Zod mappers | 2h | S00-04, S00-06 |
| S00-08 | Not found handler + async handler utility | 1h | S00-06 |
| S00-09 | Log sanitizer | 0.5h | S00-04 |
| S00-10 | Integración en app.ts (middleware chain) | 1.5h | Todos |
| S00-11 | Tests unitarios | 2h | Todos |
| | **Total** | **16h** | |

### 7.2 Gate de entrada

Design Technical specs aprobados (misma dependencia que S01).

### 7.3 Gate de salida

- [ ] Request sin errores devuelve 2xx con headers de seguridad (Helmet)
- [ ] X-Correlation-ID presente en todos los responses
- [ ] Request inválido devuelve 400 con envelope `{ error, code, correlationId, timestamp }`
- [ ] Ruta inexistente devuelve 404 con MEM_RESOURCE_NOT_FOUND
- [ ] Error interno devuelve 500 sanitizado (sin stack trace)
- [ ] Rate limit excedido devuelve 429 con MEM_RATE_LIMITED
- [ ] Logs en JSON estructurado en modo producción
- [ ] Logs legibles en modo desarrollo
- [ ] Env validation falla al startup si falta variable requerida
- [ ] SERVICE_KEY sigue funcionando como antes (no se toca)

### 7.4 Dependencias de paquetes nuevas

```bash
npm install winston helmet cors express-rate-limit
npm install @types/cors -D
```

**Nota:** `zod` y `multer` ya están en SPEC v1.9 §3.1.

---

## 8. IMPACTO EN EL PLAN

| Concepto | Antes | Después | Delta |
|----------|:-----:|:-------:|:-----:|
| Horas totales | 402h | 418h | +16h |
| Sprints Development | S01-S06 + UI-01..04 | S00 + S01-S06 + UI-01..04 | +1 sprint |
| Timeline | ~18 semanas | ~19 semanas | +1 semana |
| Decisiones cerradas (D-MEM) | 43 | 43 (sin cambios) | 0 |
| Endpoints | 11 | 11 (sin cambios) | 0 |
| Tablas BD | 19 + 10 catálogos | 19 + 10 catálogos (sin cambios) | 0 |

### 8.1 Lo que NO cambia

Los 43 D-MEM, los 11 endpoints, el modelo de datos, los flujos de import, el servicio de contexto, la clasificación, el storage, la UI, los wireframes, los criterios de aceptación funcionales — todo sigue exactamente igual.

### 8.2 Lo que SÍ cambia

Cada endpoint que se construya a partir de S01 usará `asyncHandler`, retornará errores con el envelope estándar, tendrá correlationId en logs, y estará protegido por rate limiting y headers de seguridad. En lugar de implementar esto ad-hoc en cada sprint, se implementa una vez en S00.

---

## 9. MIGRACIÓN FUTURA A VTT AUTH

Cuando VTT complete su Bloque 0+1 (Autenticación + RBAC), Memory Service adoptará:

| Componente VTT | Cómo lo adopta Memory Service |
|-----------------|-------------------------------|
| JWT validation | Nuevo middleware `requireJWT` que reemplaza/complementa `requireServiceKey` para endpoints de UI |
| RBAC capabilities | Policy middleware que evalúa capabilities del token JWT |
| Org/Workspace scope | Headers o claims JWT que filtran datos por organización/workspace |
| Audit logging | Extensión del logger con campos de audit (userId, action, resource) |
| Códigos AUTH/AUTHZ | Se agregan al catálogo MEM-ERR-xxx |

**Ninguno de estos cambios requiere reescribir el Bloque 0 Lite** — solo agregar middlewares adicionales a la cadena existente.

---

## Fuentes

| Documento | Uso |
|-----------|-----|
| SPEC_MANEJO_ERRORES_v1.1.md (VTT) | Base para §2 Error Handling |
| SPEC_LOGS_OBSERVABILIDAD_v1.1.md (VTT) | Base para §3 Logging |
| SPEC_SEGURIDAD_BASE_v1.1.md (VTT) | Base para §4 Seguridad Base |
| PLAN_IMPLEMENTACION_BLOQUE0_v1.0.md (VTT) | Estructura de sprints y orden de dependencias |
| SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md | §3.1 (deps), §3.3 (cache), §7 (auth), §11 (context timeout) |
| METODOLOGIA_MULTITENANT_RBAC_v1.2.md | §9 Migración futura (VTT hereda auth) |

---

**Documento:** ADDENDUM_BLOQUE0_LITE_MEMORY_SERVICE_v1.0.md
**Versión:** 1.0
**Estado:** Borrador para review SA
**Fecha:** 2026-05-06
