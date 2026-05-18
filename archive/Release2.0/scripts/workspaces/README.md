# VS Code Workspaces — Memory Service Multi-Repo

**Documento:** README.md
**Carpeta:** `memory-service-project/Release2.0/scripts/workspaces/`
**Propósito:** Archivos `.code-workspace` por rol para abrir VS Code multi-root con los repos correctos del proyecto.

---

## Cómo usar

1. **Bootstrap previo:** clonar los 4 repos (ver `WORKFLOW_OPERATIVO_MULTIREPO_MEMORY_SERVICE.md §4`):

   ```bash
   mkdir -p ~/memory-service-workspace
   cd ~/memory-service-workspace
   gh repo clone prompt-ai-studio/memory-service-project
   gh repo clone prompt-ai-studio/memory-service-api
   gh repo clone prompt-ai-studio/memory-service-backend
   gh repo clone prompt-ai-studio/memory-service-frontend
   ```

2. **Abrir el workspace de tu rol:**

   ```bash
   code memory-service-project/Release2.0/scripts/workspaces/<rol>.code-workspace
   ```

   Por ejemplo, BE Agent:

   ```bash
   code memory-service-project/Release2.0/scripts/workspaces/be.code-workspace
   ```

---

## Workspaces disponibles

| Archivo | Rol | Repos visibles | Write a |
|---------|-----|-----------------|---------|
| `pm.code-workspace` | PM (Coordinador) | 4 repos | project |
| `pjm.code-workspace` | PJM | 4 repos | project |
| `tl.code-workspace` | Tech Lead | 4 repos | TODOS |
| `be.code-workspace` | Backend Engineer | 3 (project, api, backend) | project, backend |
| `db.code-workspace` | Database Engineer | 2 (project, backend) | project, backend (prisma/) |
| `fe.code-workspace` | Frontend Engineer | 3 (project, api, frontend) | project, frontend |
| `qa.code-workspace` | QA Engineer | 4 repos | project, backend (tests/), frontend (tests/) |
| `do.code-workspace` | DevOps | 4 repos | project, backend (infra/, .github/), frontend (.github/) |
| `analyst.code-workspace` | SA, AR, UX, DL | 1 (project) + opcional api (AR) | project |

---

## Estructura esperada del directorio padre

Todos los workspaces asumen que los 4 repos están **al mismo nivel** en un directorio padre:

```
~/memory-service-workspace/
├── memory-service-project/
├── memory-service-api/
├── memory-service-backend/
└── memory-service-frontend/
```

Si tu directorio padre tiene otro nombre, abre el `.code-workspace` con tu editor y ajusta los `path` (son relativos al `.code-workspace`).

---

## Por qué multi-root y no 4 ventanas

1. **Claude Code puede leer `.claude/agents/OPERATIVO_<ROL>.md`** del repo `memory-service-project` aunque estés trabajando en otro repo del workspace.
2. Búsqueda y navegación cross-repo funcionan (Cmd/Ctrl + P, Cmd/Ctrl + Shift + F).
3. Una sola sesión de terminal por workspace (multiplexada con paneles).
4. Git status panel muestra todos los repos juntos.

**Nota de seguridad:** la barrera física del ADR-001 NO se rompe por multi-root. Si intentas push a un repo donde tu PAT no tiene write, GitHub retorna `403 Forbidden`. El multi-root solo facilita la lectura/edición local.

---

## Convenciones de los archivos

Todos los `.code-workspace` siguen esta plantilla mínima:

```jsonc
{
  "folders": [
    { "name": "project (write)", "path": "../../../../memory-service-project" },
    { "name": "backend (write)", "path": "../../../../memory-service-backend" },
    { "name": "api (read-only)", "path": "../../../../memory-service-api" }
  ],
  "settings": {
    "files.exclude": {
      "**/node_modules": true,
      "**/dist": true,
      "**/.git": true
    },
    "search.exclude": {
      "**/node_modules": true,
      "**/dist": true
    }
  }
}
```

Las rutas usan `../../../../` para subir 4 niveles desde el archivo `.code-workspace` hasta el directorio padre que contiene los 4 repos.

> **Si tu workspace local NO tiene esa profundidad** (ej: clonaste todo en `~/work/`), abre el `.code-workspace` y reemplaza `../../../../` por una ruta absoluta o relativa correcta.

---

**Última actualización:** 2026-04-23
**PM — Martin Rivas**
