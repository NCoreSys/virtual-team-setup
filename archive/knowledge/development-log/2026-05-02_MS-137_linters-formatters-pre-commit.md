# Development Log — MS-137: Linters + formatters + pre-commit hooks

## Informacion General

| Campo | Valor |
|-------|-------|
| Fecha | 2026-05-02 |
| Tarea | MS-137 |
| Repo | NCoreSys/memory-service-backend |
| Branch | feature/MS-137 |
| PR | #4 — https://github.com/NCoreSys/memory-service-backend/pull/4 |
| Agente | DevOps Agent (DO) |
| Dependencia | MS-136 (base Node+TypeScript) completada |

---

## Resumen

Configuracion de ESLint, Prettier y Husky con lint-staged en `NCoreSys/memory-service-backend`.
Pre-commit hook activo que bloquea commits con errores de lint, formato incorrecto o fallos TypeScript.

Todos los archivos creados via GitHub API directamente en branch `feature/MS-137` (mismo patron
exitoso de MS-136, evita problema de path duality Windows/bash).

---

## Archivos Creados/Modificados

| Archivo | Tipo | SHA commit | Descripcion |
|---------|------|-----------|-------------|
| `.eslintrc.json` | Nuevo | `9da52e50` | ESLint TypeScript strict rules |
| `.prettierrc` | Nuevo | `f8216b62` | Prettier config del proyecto |
| `.prettierignore` | Nuevo | `34bedc64` | Excluye dist/, node_modules/, *.md |
| `.husky/pre-commit` | Nuevo | `a67a7f1e` | Hook que corre lint-staged |
| `package.json` | Modificado | `b75ee021` | Nuevos scripts + lint-staged config + 3 deps |

---

## Dependencias Agregadas

| Paquete | Version | Tipo | Proposito |
|---------|---------|------|-----------|
| `eslint-config-prettier` | 9.1.0 | dev | Desactiva reglas ESLint que Prettier cubre |
| `husky` | 9.0.11 | dev | Git hooks manager |
| `lint-staged` | 15.2.2 | dev | Corre linters solo en archivos staged |

> Nota: `eslint`, `@typescript-eslint/*` y `prettier` ya estaban instalados desde MS-136.

---

## Scripts Nuevos en package.json

| Script | Comando | Uso |
|--------|---------|-----|
| `lint:fix` | `eslint src --ext .ts --fix` | Corrige errores automaticamente |
| `format:check` | `prettier --check src/**/*.ts` | Verifica formato sin modificar |
| `type-check` | `tsc --noEmit` | Validacion TypeScript sin compilar |
| `prepare` | `husky` | Instala hooks automaticamente en `npm install` |

---

## Configuracion lint-staged

```json
"lint-staged": {
  "src/**/*.{ts,tsx}": [
    "eslint --fix",
    "prettier --write",
    "tsc --noEmit"
  ]
}
```

Cada commit en archivos TypeScript pasa por ESLint (con autofix), Prettier (con autoformat)
y TypeScript check. Si cualquiera falla, el commit se bloquea.

---

## Decisiones Tecnicas

1. **GitHub API directo**: Se uso la API REST para crear archivos en el branch, evitando
   el problema de path duality (Windows bash /tmp/ vs C:\tmp\) que causo issues en tareas previas.

2. **ESLint config `recommended-requiring-type-checking`**: Habilita reglas que requieren
   informacion de tipos (como `no-floating-promises`). Mas lento pero mas correcto.

3. **`no-console: warn` con allowlist**: Permite `console.warn`, `console.error`, `console.info`
   para logs del servidor. Bloquea `console.log` de debug accidental.

4. **`eslint-config-prettier` como ultima extension**: Desactiva conflictos entre ESLint y
   Prettier. Orden importa: debe ir al final del array `extends`.

5. **`tsc --noEmit` en lint-staged**: Puede ser lento en repos grandes; para esta fase
   del proyecto el repo es pequeño y el beneficio de type-safety supera el costo.

6. **`prepare` script**: Instala husky automaticamente cuando un nuevo colaborador corre
   `npm install`, sin pasos manuales adicionales.

---

## Verificacion (pendiente localmente — repo en GitHub API)

Los archivos estan en el branch. Para verificar localmente despues del merge:

```bash
# Clonar y verificar
git clone https://github.com/NCoreSys/memory-service-backend.git
cd memory-service-backend
npm install

# Lint
npm run lint
# Esperado: 0 errores en src/index.ts

# Format check
npm run format:check
# Esperado: Todo formateado correctamente

# Type check
npm run type-check
# Esperado: 0 errores TypeScript

# Pre-commit hook (test manual)
echo "const x = require('something')" >> src/test-lint.ts
git add src/test-lint.ts
git commit -m "test lint hook"
# Esperado: FALLA con error de ESLint
git checkout src/test-lint.ts  # restaurar
```

---

## Unblocks

- **MS-138** (CI smoke en GitHub Actions) — depende de scripts `lint` y `type-check` en package.json
