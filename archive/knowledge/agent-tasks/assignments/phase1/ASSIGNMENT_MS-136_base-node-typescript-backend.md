# ASSIGNMENT: MS-136 - Base Node + TypeScript backend

**Task ID**: MS-136
**Brief ref**: INIT-E-01
**Titulo**: Base Node + TypeScript backend
**Repositorio destino**: memory-service-backend
**Asignado a**: DO (DevOps Engineer)
**Prioridad**: H (HIGH) — BLOQUEA Sprint S01 BE
**Estimacion**: 2 horas
**Complejidad**: MEDIUM
**Categoria**: deployment
**Generado por**: PJM
**Fecha asignacion**: 2026-05-01

---

## 1. Objetivo

Bootstrappear el proyecto backend con Node 20 + TypeScript + scripts base en el repo `memory-service-backend`.

**Resultado esperado:** `package.json` + `tsconfig.json` + `nodemon.json` + `.nvmrc` committeados. `npm install` y `npm run dev` funcionan sin errores.

---

## 2. Contexto del Proyecto

El Memory Service backend correrá en la VM `77.42.88.106` en el puerto `3002`.
La estrategia multi-repo (ADR-001) define que el backend vive en `memory-service-backend` (repo separado de infra, frontend, y contrato de API).
Sin este setup, los agentes BE no pueden empezar Sprint S01.

---

## 3. Archivos de Referencia (LEER ANTES DE EMPEZAR)

1. `.claude/rules/PROJECT_RULES.md` — reglas operativas v1.5
2. `memory-service-project/Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` — spec técnica (ver §3 Arquitectura)
3. `memory-service-project/Release2.0/01-PM/ADR-001_estrategia_repositorios.md` — estrategia multi-repo

---

## 4. Prerequisitos

- [ ] Acceso al repo `memory-service-backend` (via Fine-grained PAT del rol DO)
- [ ] Node 20 disponible en el entorno local (`nvm install 20`)
- [ ] Token VTT válido para actualizaciones de estado

---

## 5. Implementación — Archivos a Crear

### 5.1. `.nvmrc`

```
20
```

### 5.2. `package.json`

```json
{
  "name": "memory-service-backend",
  "version": "0.1.0",
  "description": "Memory Service — Backend API (Node 20 + TypeScript)",
  "main": "dist/index.js",
  "scripts": {
    "dev": "nodemon",
    "build": "tsc",
    "start": "node dist/index.js",
    "test": "jest",
    "lint": "eslint src --ext .ts",
    "format": "prettier --write src/**/*.ts",
    "migrate": "npx prisma migrate deploy",
    "seed": "npx ts-node prisma/seed.ts"
  },
  "engines": {
    "node": ">=20.0.0"
  },
  "dependencies": {
    "express": "4.18.2",
    "prisma": "5.13.0",
    "@prisma/client": "5.13.0",
    "ioredis": "5.3.2",
    "swagger-jsdoc": "6.2.8",
    "swagger-ui-express": "5.0.0",
    "dotenv": "16.4.5",
    "cors": "2.8.5",
    "helmet": "7.1.0",
    "morgan": "1.10.0"
  },
  "devDependencies": {
    "typescript": "5.4.5",
    "tsx": "4.7.3",
    "nodemon": "3.1.0",
    "@types/express": "4.17.21",
    "@types/cors": "2.8.17",
    "@types/morgan": "1.9.9",
    "@types/swagger-jsdoc": "6.0.4",
    "@types/swagger-ui-express": "4.1.6",
    "@types/node": "20.12.7",
    "jest": "29.7.0",
    "@types/jest": "29.5.12",
    "ts-jest": "29.1.2",
    "eslint": "8.57.0",
    "@typescript-eslint/eslint-plugin": "7.7.0",
    "@typescript-eslint/parser": "7.7.0",
    "prettier": "3.2.5"
  }
}
```

### 5.3. `tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

### 5.4. `nodemon.json`

```json
{
  "watch": ["src"],
  "ext": "ts,json",
  "ignore": ["src/**/*.test.ts"],
  "exec": "tsx src/index.ts"
}
```

### 5.5. `src/index.ts` (entry point mínimo)

```typescript
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';

const app = express();
const PORT = process.env.PORT || 3002;

app.use(helmet());
app.use(cors());
app.use(morgan('combined'));
app.use(express.json());

app.get('/health', (_req, res) => {
  res.json({ status: 'ok', service: 'memory-service-backend', port: PORT });
});

app.listen(PORT, () => {
  console.log(`Memory Service Backend running on port ${PORT}`);
});

export default app;
```

### 5.6. `.env.example`

```
NODE_ENV=development
PORT=3002
DATABASE_URL=postgresql://user:password@localhost:5432/memory_service
REDIS_URL=redis://localhost:6379
```

### 5.7. `.gitignore`

```
node_modules/
dist/
.env
*.log
```

---

## 6. Estructura de Carpetas a Crear

```
memory-service-backend/
├── src/
│   └── index.ts
├── prisma/
│   └── .gitkeep
├── .env.example
├── .gitignore
├── .nvmrc
├── nodemon.json
├── package.json
└── tsconfig.json
```

> **NO crear** `knowledge/`, `docs/` ni otras carpetas — esas las crean BE y DB en sus tareas.

---

## 7. Verificación (Criterios de Éxito)

```bash
nvm use
npm install
npm run dev
# → Debe mostrar: "Memory Service Backend running on port 3002"

curl http://localhost:3002/health
# → {"status":"ok","service":"memory-service-backend","port":3002}
```

- [ ] `npm install` sin errores
- [ ] `npm run dev` levanta en puerto 3002
- [ ] `GET /health` responde 200
- [ ] `npm run build` genera `dist/` sin errores TypeScript

---

## 8. Entregables Requeridos

| # | Entregable | Ubicación |
|---|-----------|-----------|
| 1 | Código + config | `memory-service-backend/` (raíz del repo) |
| 2 | Development Log | `knowledge/development-log/2026-05-XX_MS-136_base-node-typescript.md` |
| 3 | Code Logic | `knowledge/code-logic/src/index.LOGIC.md` |
| 4 | Commit + PR | Branch `feature/MS-136`, PR a `main` |

---

## 9. Workflow

```bash
# 1. Cambiar estado en VTT
curl -X PATCH "http://77.42.88.106:3000/api/tasks/[MS-136-UUID]/status" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"status":"task_in_progress","comment":"Iniciando setup Node 20 + TypeScript"}'

# 2. Crear branch
git checkout -b feature/MS-136

# 3. Implementar archivos (sección 5)

# 4. Commit
git add .
git commit -m "feat [MS-136]: Bootstrap Node 20 + TypeScript backend

- package.json con scripts: dev, build, start, test, lint, format, migrate, seed
- tsconfig.json strict mode
- nodemon.json para dev con tsx
- .nvmrc con Node 20
- src/index.ts entry point con health endpoint
- Dependencias: express, prisma, ioredis, swagger, dotenv

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
Refs: #MS-136"

# 5. Push + PR
git push origin feature/MS-136
gh pr create --title "[MS-136] Bootstrap Node 20 + TypeScript backend" --body "Ver devlog para detalles." --base main

# 6. Cambiar estado a task_in_review
curl -X PATCH "http://77.42.88.106:3000/api/tasks/[MS-136-UUID]/status" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"status":"task_in_review","comment":"PR creado, pendiente revisión TL"}'
```

---

## 10. Notas

- Puerto **3002** (API Memory Service) — no usar 3000 (VTT) ni 3001 (otro servicio)
- Las dependencias tienen versiones **fijas** — no usar `latest`
- `src/index.ts` es MÍNIMO — los agentes BE agregarán routers en sus tareas
- **No crear archivo `.env`** — solo `.env.example` va al repo

---

**Generado por**: PJM (Martin Rivas)
**Fecha**: 2026-05-01
**Version**: 1.0
