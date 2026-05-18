# Code Logic — MS-124: Archivos Base del Repo

**Tarea:** MS-124 / INIT-B-03
**Fecha:** 2026-04-25
**Agente:** PJM-Agent

---

## Qué hace

Define la configuración base del repositorio `memory-service`: exclusiones de Git, normalización de line endings, indentación consistente, y documentación de entrada (README + CONTRIBUTING).

No hay código ejecutable — son archivos de configuración y documentación que **estandarizan cómo todos los agentes interactúan con el repo**.

---

## Cómo fluye la lógica

### .gitignore
Git lee este archivo en cada operación (`git status`, `git add`, etc.) y excluye los patterns listados. La precedencia: el más específico gana, y `!pattern` permite re-incluir excepciones.

### .gitattributes
Git lo aplica al hacer checkout/checkin para normalizar line endings. Con `* text=auto eol=lf`, Git convierte CRLF→LF al hacer commit y mantiene LF al hacer checkout, evitando los warnings "LF will be replaced by CRLF" en Windows.

### .editorconfig
Los IDEs/editores (VS Code, IntelliJ, vim) leen este archivo automáticamente al abrir un archivo y aplican las reglas de indent/charset/eol. Sin él, cada dev usa su configuración personal y se generan diffs falsos.

### README.md
Punto de entrada para cualquier persona que abre el repo. Contiene stack, setup local, endpoints, decisiones clave. Apunta al SPEC v1.9 para detalle.

### CONTRIBUTING.md
Manual operativo del flujo de trabajo. Replica las reglas de `PROJECT_RULES.md` y `AGENT_RULES_Rev.md` en una versión accesible desde la raíz.

---

## Dependencias Importantes

| Componente | Por qué |
|------------|---------|
| Git | Ejecuta `.gitignore` y `.gitattributes` |
| IDE/Editor | Aplica `.editorconfig` |
| `PROJECT_RULES.md` (`.claude/rules/`) | Fuente de verdad de las reglas — CONTRIBUTING refleja su contenido |
| `SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` | Fuente de verdad técnica — README apunta aquí |

---

## Decisiones de Diseño

- **`knowledge/` y `devlogs/` ignorados:** Son documentación local de agentes (development-log, code-logic). No deben ensuciar el historial de git del código.
- **Allowlist en `.vscode/`:** Permite compartir `extensions.json` y `settings.json.example` pero excluye preferencias personales.
- **`text=auto eol=lf` en `.gitattributes`:** Política unificada — todo el equipo trabaja con LF, evita divergencias entre Windows y Unix.
- **CONTRIBUTING como reflejo de PROJECT_RULES:** Mantener una sola fuente de verdad sería ideal, pero CONTRIBUTING.md en la raíz es convención GitHub que aparece automáticamente en PRs.

---

## Historial de Cambios

| Fecha | Cambio | Agente |
|-------|--------|--------|
| 2026-04-25 | Creación inicial — 5 archivos base + validación de exclusión .env | PJM-Agent |
