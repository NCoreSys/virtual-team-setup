# ASSIGNMENT: MS-137 - Linters + formatters + pre-commit hooks

**Task ID**: MS-137
**Brief ref**: INIT-E-02
**Titulo**: Linters + formatters + pre-commit hooks
**Repositorio destino**: memory-service-backend (NCoreSys/memory-service-backend)
**Asignado a**: DO (DevOps Engineer)
**Prioridad**: M (MEDIUM)
**Estimacion**: 1 hora
**Complejidad**: LOW
**Categoria**: deployment
**Generado por**: PJM
**Fecha asignacion**: 2026-05-02
**Dependencias**: MS-136 (Base Node + TypeScript ✅ completada)

---

## 1. Objetivo

Configurar ESLint, Prettier y Husky con lint-staged en el repo `NCoreSys/memory-service-backend`, sobre la base Node+TypeScript ya existente (MS-136).

**Resultado esperado:** Pre-commit hook activo que bloquea commits con errores de lint, formato incorrecto, o fallos de TypeScript.

---

## 2. Contexto

MS-136 dejó el repo con estructura Node 20 + TypeScript + Express corriendo en puerto 3002. Esta tarea agrega las herramientas de calidad de código que todo el equipo usará desde el primer commit real. Sin esto, el código del BE y DB puede entrar al repo sin pasar por ningún gate de calidad.

**Unblocks**: MS-138 (CI smoke en GitHub Actions) — depende de que los scripts de lint estén definidos en `package.json`.

---

## 3. Archivos de Referencia (LEER ANTES DE EMPEZAR)

1. `NCoreSys/memory-service-backend` — `package.json` actual (base de MS-136)
2. `NCoreSys/memory-service-backend` — `tsconfig.json` actual
3. `.claude/rules/PROJECT_RULES.md` — reglas del proyecto

---

## 4. Prerequisitos

- [ ] MS-136 completada (repo tiene Node 20 + TypeScript + Express) ✅
- [ ] Acceso de escritura a `NCoreSys/memory-service-backend`
- [ ] PAT con scope `contents:write` para el repo

---

## 5. Implementación

### 5.1. Instalar dependencias

```bash
# En el repo memory-service-backend
npm install --save-dev \
  eslint@^8.57.0 \
  @typescript-eslint/parser@^7.0.0 \
  @typescript-eslint/eslint-plugin@^7.0.0 \
  prettier@^3.2.0 \
  eslint-config-prettier@^9.1.0 \
  husky@^9.0.0 \
  lint-staged@^15.2.0
```

### 5.2. Archivo `.eslintrc.json`

```json
{
  "root": true,
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "project": "./tsconfig.json",
    "ecmaVersion": 2022,
    "sourceType": "module"
  },
  "plugins": ["@typescript-eslint"],
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:@typescript-eslint/recommended-requiring-type-checking",
    "prettier"
  ],
  "rules": {
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/explicit-function-return-type": "warn",
    "@typescript-eslint/no-unused-vars": ["error", { "argsIgnorePattern": "^_" }],
    "@typescript-eslint/no-floating-promises": "error",
    "no-console": ["warn", { "allow": ["warn", "error", "info"] }]
  },
  "ignorePatterns": ["dist/", "node_modules/", "*.js"]
}
```

### 5.3. Archivo `.prettierrc`

```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100,
  "arrowParens": "always"
}
```

### 5.4. Archivo `.prettierignore`

```
dist/
node_modules/
*.md
```

### 5.5. Configurar Husky + lint-staged

```bash
# Inicializar husky
npx husky init

# El archivo .husky/pre-commit debe contener:
echo "npx lint-staged" > .husky/pre-commit
chmod +x .husky/pre-commit
```

### 5.6. Configurar lint-staged en `package.json`

Agregar al `package.json` existente:

```json
{
  "lint-staged": {
    "src/**/*.{ts,tsx}": [
      "eslint --fix",
      "prettier --write",
      "tsc --noEmit"
    ]
  }
}
```

### 5.7. Scripts a agregar en `package.json`

```json
{
  "scripts": {
    "lint": "eslint src --ext .ts",
    "lint:fix": "eslint src --ext .ts --fix",
    "format": "prettier --write src/**/*.ts",
    "format:check": "prettier --check src/**/*.ts",
    "type-check": "tsc --noEmit",
    "prepare": "husky"
  }
}
```

> **Nota**: Mantener todos los scripts existentes de MS-136 (`build`, `start`, `dev`, `test`, etc.) — solo agregar los nuevos.

---

## 6. Verificación

### 6.1. Lint funciona
```bash
npm run lint
# → 0 errores en src/index.ts (código limpio de MS-136)
```

### 6.2. Prettier funciona
```bash
npm run format:check
# → Todo formateado correctamente
```

### 6.3. Type-check funciona
```bash
npm run type-check
# → 0 errores TypeScript
```

### 6.4. Pre-commit hook activo
```bash
# Hacer un cambio con error de lint intencional y tratar de commitear
echo "const x = require('something')" >> src/test-lint.ts
git add src/test-lint.ts
git commit -m "test lint hook"
# → Debe FALLAR y mostrar error de ESLint
git checkout src/test-lint.ts  # restaurar
```

### 6.5. Verificar scripts en package.json
```bash
cat package.json | grep -A 10 '"scripts"'
# → Debe incluir lint, lint:fix, format, format:check, type-check, prepare
```

---

## 7. Entregables Requeridos

| # | Entregable | Ubicación |
|---|-----------|-----------|
| 1 | `.eslintrc.json` | Raíz de `NCoreSys/memory-service-backend` |
| 2 | `.prettierrc` | Raíz de `NCoreSys/memory-service-backend` |
| 3 | `.prettierignore` | Raíz de `NCoreSys/memory-service-backend` |
| 4 | `.husky/pre-commit` | Raíz de `NCoreSys/memory-service-backend` |
| 5 | `package.json` actualizado | Con lint-staged config + nuevos scripts |
| 6 | Development Log | `knowledge/development-log/2026-05-XX_MS-137_linters-formatters.md` (en `memory-service`) |
| 7 | Commit + PR | Branch `feature/MS-137`, PR a `main` de `memory-service-backend` |

---

## 8. Workflow

```bash
# 1. Cambiar estado en VTT
curl -X PATCH "http://77.42.88.106:3000/api/tasks/MS-137/status" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"statusId":"<task_in_progress_uuid>","comment":"Configurando ESLint + Prettier + Husky en memory-service-backend"}'

# 2. Crear branch (via GitHub API — ver patrón de MS-136)
# Branch: feature/MS-137
# Base: main de NCoreSys/memory-service-backend

# 3. Instalar deps y crear archivos (sección 5)

# 4. Commit
git commit -m "chore [MS-137]: Linters + formatters + pre-commit hooks

- .eslintrc.json con TypeScript strict rules
- .prettierrc con config del proyecto
- Husky + lint-staged para pre-commit gate
- Scripts: lint, lint:fix, format, format:check, type-check

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
Refs: #MS-137"

# 5. Push + PR
git push origin feature/MS-137
gh pr create --title "[MS-137] Linters + formatters + pre-commit hooks" \
  --body "ESLint TypeScript strict + Prettier + Husky pre-commit gate. Unblocks MS-138 (CI smoke). Ver devlog para detalles." \
  --base main \
  --repo NCoreSys/memory-service-backend

# 6. Cambiar estado
curl -X PATCH "http://77.42.88.106:3000/api/tasks/MS-137/status" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"statusId":"<task_in_review_uuid>","comment":"Linters configurados, pre-commit hook activo, PR creado"}'
```

---

## 9. Notas

- Si hay conflictos entre ESLint y Prettier, `eslint-config-prettier` los resuelve desactivando las reglas de ESLint que Prettier cubre
- La regla `no-console: warn` permite `console.warn`, `console.error`, `console.info` — suficiente para logs del servidor
- El `tsc --noEmit` en lint-staged puede ser lento en repos grandes; si es un problema, moverlo a CI solamente
- El `prepare` script instala husky automáticamente en `npm install` para nuevos colaboradores
- **Problema de mixed history**: usar GitHub API para crear el branch y commitear archivos (mismo patrón que MS-136 usó exitosamente)

---

**Generado por**: PJM (Martin Rivas)
**Fecha**: 2026-05-02
**Version**: 1.0
