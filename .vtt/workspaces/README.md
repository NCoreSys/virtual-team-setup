# VS Code Workspaces — Memory Service

**Documento:** README.md
**Carpeta:** `.vtt/workspaces/` (también en `Release2.0/scripts/workspaces/` como referencia histórica)
**Propósito:** Archivos `.code-workspace` por rol. Modelo de 3 equipos operativos: BE, FE, QA/Testing/Integraciones.

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

## Modelo de 3 equipos operativos

| Equipo | Workspace(s) | Repos write | Repos read |
|--------|-------------|-------------|------------|
| **BE** | `be.code-workspace`, `db.code-workspace`, `do.code-workspace` | backend | api, project |
| **FE** | `fe.code-workspace`, `analyst.code-workspace` | frontend | api, project |
| **QA/Testing** | `qa.code-workspace` | backend (tests/), frontend (tests/) | api, project |
| Transversal | `tl.code-workspace`, `pm.code-workspace`, `pjm.code-workspace` | según rol | según rol |

## Workspaces disponibles

| Archivo | Rol | Repos write | Repos read |
|---------|-----|-------------|------------|
| `pm.code-workspace` | PM | project, api | — |
| `pjm.code-workspace` | PJM | project | — |
| `tl.code-workspace` | TL | todos | — |
| `be.code-workspace` | BE | backend, project (devlogs) | api |
| `db.code-workspace` | DB | backend (prisma/), project (devlogs) | api |
| `do.code-workspace` | DO | backend (infra/.github/), project (devlogs) | frontend (.github/) |
| `fe.code-workspace` | FE | frontend, project (devlogs) | api |
| `qa.code-workspace` | QA | backend (tests/), frontend (tests/), project (devlogs) | api |
| `analyst.code-workspace` | SA/AR/UX/DL | project | — |

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

**Última actualización:** 2026-04-27
**PM — Martin Rivas**
