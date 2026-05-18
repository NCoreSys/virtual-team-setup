# DICCIONARIO DE DELIVERABLES — FASE 4.1: ENVIRONMENT SETUP

**Versión:** 1.0  
**Fecha:** 2026-05-14  
**Fase:** 4 — Development  
**Subfase:** 4.1 — Environment Setup  
**Total deliverables:** 10  
**Responsable de subfase:** DevOps Lead  
**Aprueba:** Tech Lead

---

## Contexto de la subfase

Environment Setup prepara todo lo necesario para que el equipo de desarrollo pueda empezar a escribir código productivamente: ambiente local reproducible, repositorio configurado, linting/formatting automático, pre-commit hooks, y documentación de setup. Un developer nuevo debería poder clonar el repo y estar productivo en menos de 30 minutos.

**Nota sobre Fase 4:** Los deliverables de esta fase son **código y configuración**, no documentos. El diccionario describe: qué artefacto se genera, qué archivos lo componen, su Criterio de completitud, y la documentación que lo acompaña.

**Prerequisitos de subfase:**
- Technology Stack definido (3B.1.5)
- Folder Structure definida (3B.2.1)
- Coding Standards definidos (3B.2.2)

**Entrega de subfase:**
- Repositorio configurado, ambiente local reproducible, developer experience optimizada desde el primer commit

---

### 4.1.1 Development Environment

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.1 Environment Setup |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Tech Lead |
| **Formato** | Docker Compose / Config files |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 1-2 días |
| **Frecuencia** | Una vez + mantenimiento |

**Perfil de ejecución:** Requiere experiencia con Docker, Docker Compose, y configuración de servicios locales.  
En VTT: un agente puede generar docker-compose.yml, Dockerfiles, y scripts de setup. Es altamente delegable. Necesita brief con: servicios requeridos (DB, cache, queue), versiones, puertos.

**Qué es:** Ambiente de desarrollo local containerizado con Docker Compose que incluye todos los servicios: base de datos, cache (Redis), message queue (si aplica), y la aplicación con hot reload. Con un solo `docker compose up` todo funciona.

**Para qué sirve:** Elimina "en mi máquina funciona". Todos los developers tienen exactamente el mismo ambiente. Reduce onboarding de 1 día a 30 minutos.

**Inputs requeridos:**
- `3B.1.5` Technology Stack — servicios y versiones
- `3B.8.5` Environment Matrix — configuración dev
- `3B.3.2` Schema Definition — BD a inicializar

**Dependencias (predecessors):**
- `3B.1.5` Technology Stack *(obligatorio)*
- `3B.8.5` Environment Matrix *(obligatorio)*

**Habilita (successors):**
- `4.1.2` Environment Setup Guide — documentación del setup
- `4.2.1` Initial Migration — BD local lista
- Todo el desarrollo del proyecto

**Audiencia:**
- **Todo el equipo de desarrollo** — ambiente diario

**Secciones esperadas:
- `docker-compose.yml` — orquestación de servicios
- `Dockerfile` / `Dockerfile.dev` — imagen de la app
- `.dockerignore` — exclusiones de build
- `scripts/setup.sh` — script de inicialización

**Criterio de completitud:
- [ ] `docker compose up` levanta todos los servicios sin errores
- [ ] BD accesible con credenciales del .env
- [ ] Hot reload funcional (cambios sin rebuild)
- [ ] Volúmenes persistentes (datos sobreviven restart)
- [ ] Funciona en macOS, Linux, y Windows (WSL2)
- [ ] Tiempo de setup < 5 minutos (excluyendo descarga de imágenes)

**Anti-patrones:**
- ❌ **"Instala todo local":** PostgreSQL, Redis, Node.js manual — cada developer tiene config diferente.
- ❌ **Docker sin hot reload:** Rebuild para cada cambio — productividad destruida.
- ❌ **Sin volúmenes persistentes:** `docker compose down` borra la BD.
- ❌ **Ports hardcoded:** Port 5432 fijo conflicta con PostgreSQL local.

**Template:** `phases/04-development/deliverables/docker-compose.yml` *(pendiente)*

---

### 4.1.2 Environment Setup Guide

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.1 Environment Setup |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Tech Lead |
| **Formato** | README.md |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez + actualizaciones |

**Perfil de ejecución:** Requiere escritura técnica clara y paso-a-paso.  
En VTT: un agente puede generar la guía completa. Es altamente delegable. Necesita brief con: prerrequisitos, pasos, y troubleshooting.

**Qué es:** Documentación paso-a-paso: prerrequisitos (Docker, Node.js, Git), clonación del repo, configuración de .env, Docker Compose up, migrations, seeds, y verificación. Incluye troubleshooting de problemas comunes.

**Para qué sirve:** Developer nuevo → lee guía → 30 min → productivo. Sin guía → 1 día de "pregúntale a alguien".

**Inputs requeridos:**
- `4.1.1` Development Environment — setup a documentar
- `4.1.3` Environment Variables — variables requeridas

**Dependencias (predecessors):**
- `4.1.1` Development Environment *(obligatorio)*

**Habilita (successors):**
- Onboarding de developers nuevos

**Secciones esperadas:
- `README.md` (sección Setup) o `docs/SETUP.md`

**Criterio de completitud:
- [ ] Developer nuevo puede seguir la guía sin ayuda externa
- [ ] Prerrequisitos con versiones listados
- [ ] Comandos copy-pasteable
- [ ] Verificación incluida ("cómo saber que funciona")
- [ ] Troubleshooting de 3+ problemas comunes
- [ ] Probado por alguien que NO la escribió

**Anti-patrones:**
- ❌ **Sin guía:** "Pregúntale a Juan cómo se configura" — Juan se va de vacaciones y nadie puede setear el proyecto.
- ❌ **Guía desactualizada:** Documentación de hace 6 meses que ya no funciona — peor que no tener guía.
- ❌ **Pasos implícitos:** "Configura el .env" sin decir qué variables ni qué valores.

**Template:** `phases/04-development/deliverables/setup-guide.md` *(pendiente)*

---

### 4.1.3 Environment Variables

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.1 Environment Setup |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Tech Lead |
| **Formato** | .env.example |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.25 día |
| **Frecuencia** | Una vez + adiciones por feature |

**Perfil de ejecución:** Requiere conocimiento de qué configuración debe externalizarse como variables de entorno.  
En VTT: un agente puede generar .env.example con todas las variables documentadas. Es altamente delegable. Necesita brief con: servicios, sus configs, y secrets inventariados.

**Qué es:** Archivo `.env.example` commiteado en el repo que documenta todas las variables de entorno necesarias: nombre, descripción, valor de ejemplo (no el real), si es requerida u opcional, y agrupación por servicio. El developer copia `.env.example` a `.env` y llena los valores reales.

**Para qué sirve:** Sin .env.example, cada developer descubre las variables necesarias por prueba y error o preguntando. El .env.example es la documentación viva de la configuración — siempre actualizado porque está en el repo.

**Inputs requeridos:**
- `3B.7.8` Secrets Management — inventario de secrets
- `3B.1.5` Technology Stack — servicios con configuración
- `3B.1.6` Integration Points — credentials de integraciones

**Dependencias (predecessors):**
- `3B.7.8` Secrets Management *(obligatorio)*
- `3B.1.5` Technology Stack *(obligatorio)*

**Habilita (successors):**
- `4.1.1` Development Environment — Docker Compose lee .env
- `4.1.4` Docker Compose — servicios configurados con env vars

**Secciones esperadas:
- `.env.example` — template con valores de ejemplo
- `.env` (gitignored) — valores reales locales

**Criterio de completitud:
- [ ] Todas las variables documentadas con descripción
- [ ] Valores de ejemplo realistas (no vacíos)
- [ ] Variables agrupadas por servicio (DB, Redis, Auth, APIs)
- [ ] Required vs optional marcado
- [ ] `.env` en `.gitignore` (nunca commiteado)
- [ ] `.env.example` en el repo (siempre commiteado)

**Anti-patrones:**
- ❌ **.env commiteado:** Secrets reales en el repo — data breach.
- ❌ **Sin .env.example:** "¿Qué variables necesito?" — descubrimiento por error.
- ❌ **Variables sin descripción:** `MAGIC_KEY=` — ¿qué es? ¿de dónde lo saco?
- ❌ **.env.example desactualizado:** Se agrega una variable nueva al código pero no al .env.example — deploy falla.

**Template:** `phases/04-development/deliverables/.env.example` *(pendiente)*

---

### 4.1.4 Docker Compose

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.1 Environment Setup |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Tech Lead |
| **Formato** | docker-compose.yml |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | Incluido en 4.1.1 |
| **Frecuencia** | Una vez + mantenimiento |

**Perfil de ejecución:** Requiere dominio de Docker Compose: services, volumes, networks, healthchecks, depends_on.  
En VTT: un agente puede generar el docker-compose.yml completo. Es altamente delegable. Necesita brief con: servicios, imágenes, ports, volumes, y dependencies.

**Qué es:** Archivo `docker-compose.yml` que define y orquesta todos los servicios del ambiente de desarrollo: app (con hot reload), database (PostgreSQL/MySQL), cache (Redis), queue (RabbitMQ/SQS local), mail (Mailhog para testing), y cualquier servicio auxiliar. Cada servicio con healthcheck, volumes, y networking correcto.

**Para qué sirve:** Un solo archivo que describe todo el ambiente. `docker compose up` → todo corre. `docker compose down` → todo se apaga. Reproducible, versionado, y compartido entre todo el equipo.

**Inputs requeridos:**
- `3B.1.5` Technology Stack — servicios y versiones
- `4.1.3` Environment Variables — configuración por servicio

**Dependencias (predecessors):**
- `3B.1.5` Technology Stack *(obligatorio)*
- `4.1.3` Environment Variables *(obligatorio)*

**Habilita (successors):**
- `4.1.1` Development Environment — orquestación del ambiente
- `4.2.1` Initial Migration — BD local lista

**Secciones esperadas:
- `docker-compose.yml`
- `docker-compose.override.yml` (overrides locales, gitignored)

**Criterio de completitud:
- [ ] Todos los servicios del stack definidos
- [ ] Healthchecks configurados en servicios críticos (DB, cache)
- [ ] `depends_on` con condition: service_healthy
- [ ] Volumes para persistencia de datos
- [ ] Hot reload del código de la app
- [ ] Ports configurable via .env

**Anti-patrones:**
- ❌ **Sin healthchecks:** La app arranca antes que la BD esté lista — crash al inicio.
- ❌ **Build largo en cada up:** Imagen que rebuilds desde cero cada vez — usar cache layers.
- ❌ **Servicios innecesarios:** Elasticsearch, Kibana, Grafana en el compose de desarrollo — RAM consumida sin necesidad.

**Template:** `phases/04-development/deliverables/docker-compose.yml` *(pendiente)*

---

### 4.1.5 Makefile / Scripts

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.1 Environment Setup |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Tech Lead |
| **Formato** | Makefile / shell scripts |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez + adiciones |

**Perfil de ejecución:** Requiere conocimiento de Make y/o shell scripting para crear shortcuts útiles.  
En VTT: un agente puede generar Makefile y scripts. Es altamente delegable. Necesita brief con: comandos frecuentes a automatizar.

**Qué es:** Makefile o colección de scripts que automatiza comandos frecuentes: `make setup` (primera vez), `make dev` (levantar ambiente), `make test` (correr tests), `make migrate` (correr migrations), `make seed` (sembrar datos), `make lint` (linting), `make build` (build de producción). Son shortcuts que el developer usa 50 veces al día.

**Para qué sirve:** En lugar de recordar `docker compose exec app npx prisma migrate dev --name=`, el developer escribe `make migrate`. Reduce errores de typos en comandos largos, estandariza el workflow, y documenta los comandos disponibles (`make help`).

**Inputs requeridos:**
- `4.1.1` Development Environment — comandos de Docker
- Workflow del proyecto (qué comandos se ejecutan frecuentemente)

**Dependencias (predecessors):**
- `4.1.1` Development Environment *(obligatorio)*

**Habilita (successors):**
- Productividad del equipo de desarrollo

**Secciones esperadas:
- `Makefile` o `scripts/` directory
- `make help` target documentado

**Criterio de completitud:
- [ ] Targets básicos: setup, dev, test, lint, build, migrate, seed
- [ ] `make help` muestra todos los targets disponibles con descripción
- [ ] Cada target funciona sin errores
- [ ] Documentado en README

**Anti-patrones:**
- ❌ **Comandos de 80 caracteres:** `docker compose exec -T app npx prisma migrate deploy --schema=./prisma/schema.prisma` de memoria — usar un alias.
- ❌ **Sin `make help`:** 20 targets pero nadie sabe cuáles existen.
- ❌ **Makefile con lógica compleja:** Make no es un lenguaje de programación — scripts complejos van en shell/Python.

**Template:** `phases/04-development/deliverables/Makefile` *(pendiente)*

---

### 4.1.6 IDE Configuration

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.1 Environment Setup |
| **Responsable** | DevOps Lead |
| **Ejecuta** | Tech Lead |
| **Aprueba** | Tech Lead |
| **Formato** | .vscode/ / .idea/ |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.25 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere conocimiento de VS Code settings, extensions recomendadas, y debug configurations.  
En VTT: un agente puede generar los archivos de configuración IDE. Es altamente delegable. Necesita brief con: IDE primario (VS Code), extensions necesarias, y debug configs.

**Qué es:** Archivos de configuración del IDE compartidos en el repo: VS Code settings (format on save, default formatter, tab size), extensiones recomendadas, snippets del proyecto, y debug configurations (attach to Node.js, debug tests). Se comparten vía `.vscode/` commiteado en el repo.

**Para qué sirve:** Cada developer tiene la misma experiencia de IDE: format on save funciona igual para todos, los mismos linters están activos, y debugging está pre-configurado. Sin config compartida, cada developer configura a su gusto y los pull requests tienen cambios de formatting mezclados con cambios de lógica.

**Inputs requeridos:**
- `3B.2.2` Coding Standards — estilo que el IDE debe enforcar
- `4.1.9` Linter Configuration — linter del proyecto
- `4.1.10` Formatter Configuration — formatter del proyecto

**Dependencias (predecessors):**
- `3B.2.2` Coding Standards *(obligatorio)*

**Habilita (successors):**
- Productividad y consistencia del equipo

**Secciones esperadas:
- `.vscode/settings.json` — settings del proyecto
- `.vscode/extensions.json` — extensiones recomendadas
- `.vscode/launch.json` — debug configurations
- `.editorconfig` — settings cross-IDE (tabs, line endings)

**Criterio de completitud:
- [ ] Format on save configurado con el formatter del proyecto
- [ ] Extensiones recomendadas listadas
- [ ] Debug configuration funcional (breakpoints en backend y frontend)
- [ ] EditorConfig para consistencia cross-IDE
- [ ] Settings no incluyen preferencias personales (solo de proyecto)

**Anti-patrones:**
- ❌ **Settings personales commiteados:** Font size 24, tema Monokai — esas son preferencias, no config de proyecto.
- ❌ **Sin debug config:** Cada developer configura debugging a su manera — o peor, usa `console.log`.
- ❌ **Sin extensiones recomendadas:** El developer no sabe que necesita ESLint, Prettier, Prisma extensions.

**Template:** `phases/04-development/deliverables/.vscode/` *(pendiente)*

---

### 4.1.7 Pre-commit Hooks

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.1 Environment Setup |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead / Tech Lead |
| **Aprueba** | Tech Lead |
| **Formato** | .pre-commit-config / husky |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.25 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere configuración de Husky + lint-staged o pre-commit framework.  
En VTT: un agente puede generar la configuración de pre-commit hooks. Es altamente delegable. Necesita brief con: qué checks ejecutar pre-commit (lint, format, type-check, test).

**Qué es:** Git hooks que se ejecutan automáticamente antes de cada commit: linting (ESLint), formatting (Prettier), type checking (tsc --noEmit), detección de secrets (detect-secrets), y opcionalmente tests afectados. Implementados con Husky + lint-staged (JS) o pre-commit framework (Python).

**Para qué sirve:** Es la última línea de defensa antes de que código mal formateado o con errores de lint llegue al repo. Sin pre-commit hooks, el CI falla después del push (loop de fix → push → fail → fix). Con hooks, se detecta antes del commit — feedback inmediato.

**Inputs requeridos:**
- `4.1.9` Linter Configuration — qué linter ejecutar
- `4.1.10` Formatter Configuration — qué formatter ejecutar
- `3B.7.8` Secrets Management — detección de secrets

**Dependencias (predecessors):**
- `4.1.9` Linter Configuration *(obligatorio)*
- `4.1.10` Formatter Configuration *(obligatorio)*

**Habilita (successors):**
- Calidad de código desde el primer commit

**Secciones esperadas:
- `.husky/pre-commit` — hook de pre-commit
- `.lintstagedrc` — configuración de lint-staged
- `package.json` scripts (prepare: husky)

**Criterio de completitud:
- [ ] Hook se ejecuta en cada commit automáticamente
- [ ] Lint solo de archivos staged (no todo el proyecto — lint-staged)
- [ ] Formatting automático de archivos staged
- [ ] Detección de secrets (API keys, passwords)
- [ ] Hook no toma más de 10 segundos (performance)
- [ ] Se puede bypassar con `--no-verify` (para emergencias documentadas)

**Anti-patrones:**
- ❌ **Sin hooks:** Código con errores de lint llega al repo — CI falla, loop de fix.
- ❌ **Hooks que lintean TODO el proyecto:** 5 minutos de espera en cada commit — el developer desactiva los hooks.
- ❌ **Hooks que corren tests:** Tests completos en pre-commit = 30 min wait — eso va en CI, no en pre-commit.
- ❌ **Hooks sin bypass:** Un bug crítico necesita hotfix y el hook bloquea — `--no-verify` para emergencias.

**Template:** `phases/04-development/deliverables/.husky/` *(pendiente)*

---

### 4.1.8 Git Configuration

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.1 Environment Setup |
| **Responsable** | DevOps Lead |
| **Ejecuta** | DevOps Lead |
| **Aprueba** | Tech Lead |
| **Formato** | .gitignore / .gitattributes |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.25 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere conocimiento de qué archivos excluir del repo y convenciones de Git.  
En VTT: un agente puede generar .gitignore completo por stack. Es altamente delegable. Necesita brief con: stack tecnológico y archivos sensibles.

**Qué es:** Configuración de Git del proyecto: `.gitignore` (archivos excluidos del repo: node_modules, .env, dist, coverage, logs), `.gitattributes` (line endings, binary files), branching strategy documentada, y commit message convention (Conventional Commits).

**Para qué sirve:** Previene que archivos no deseados lleguen al repo: node_modules (500MB), .env (secrets), dist (build output), coverage (reports). También estandariza line endings (LF en Linux/Mac, CRLF en Windows → conflictos) y commits (feat:, fix:, docs: → changelog automático).

**Inputs requeridos:**
- `3B.1.5` Technology Stack — qué ignorar por stack
- `3B.2.5` Naming Conventions — commit convention

**Dependencias (predecessors):**
- `3B.1.5` Technology Stack *(obligatorio)*

**Habilita (successors):**
- Repo limpio desde el primer commit

**Secciones esperadas:
- `.gitignore` — exclusiones
- `.gitattributes` — line endings, binary files
- `docs/BRANCHING.md` o sección en README — branching strategy

**Criterio de completitud:
- [ ] .gitignore cubre: node_modules, .env, dist, coverage, .DS_Store, logs, IDE files personales
- [ ] .gitattributes configura line endings (LF)
- [ ] Branching strategy documentada (trunk-based, git-flow, o GitHub flow)
- [ ] Commit convention documentada (Conventional Commits)

**Anti-patrones:**
- ❌ **node_modules commiteado:** 500MB de dependencias en el repo.
- ❌ **.env commiteado:** Secrets en el historial de Git — incluso si se borra después, persiste en el historial.
- ❌ **Sin .gitattributes:** Line endings inconsistentes — diffs fantasma en PRs.
- ❌ **Commits sin convención:** "fix stuff", "wip", "changes" — historial ilegible.

**Template:** `phases/04-development/deliverables/.gitignore` *(pendiente)*

---

### 4.1.9 Linter Configuration

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.1 Environment Setup |
| **Responsable** | DevOps Lead |
| **Ejecuta** | Tech Lead |
| **Aprueba** | Tech Lead |
| **Formato** | .eslintrc / ruff.toml |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.5 día |
| **Frecuencia** | Una vez + ajustes |

**Perfil de ejecución:** Requiere conocimiento del linter del ecosistema y configuración de rules.  
En VTT: un agente puede generar la configuración de linter basada en la guía de estilo elegida (Airbnb, Standard). Es altamente delegable. Necesita brief con: guía base, customizaciones, y plugins necesarios.

**Qué es:** Configuración del linter del proyecto: ESLint para JavaScript/TypeScript, Ruff/Flake8 para Python, RuboCop para Ruby. Incluye: rules (error, warn, off), plugins (TypeScript, React, import, accessibility), y overrides por tipo de archivo. Basada en la guía de estilo elegida (3B.2.2) con customizaciones del proyecto.

**Para qué sirve:** El linter detecta automáticamente: errores potenciales (unused variables, unreachable code), bad practices (eval, any), inconsistencias de estilo, y problemas de accesibilidad (jsx-a11y). Es la implementación automática de los Coding Standards — las reglas que se olvidan manualmente se enforcan automáticamente.

**Inputs requeridos:**
- `3B.2.2` Coding Standards — reglas a enforcar
- `3B.1.5` Technology Stack — linter del ecosistema

**Dependencias (predecessors):**
- `3B.2.2` Coding Standards *(obligatorio)*
- `3B.1.5` Technology Stack *(obligatorio)*

**Habilita (successors):**
- `4.1.7` Pre-commit Hooks — linting en pre-commit
- CI/CD pipeline — linting como step
- Calidad de código consistente

**Secciones esperadas:
- `.eslintrc.json` o `eslint.config.js` — reglas
- `.eslintignore` — archivos excluidos

**Criterio de completitud:
- [ ] Guía base configurada (Airbnb, Standard, o custom)
- [ ] TypeScript plugin configurado (si aplica)
- [ ] React plugin configurado (si aplica)
- [ ] A11y plugin configurado (si aplica)
- [ ] Import order plugin configurado
- [ ] Cero errores de lint en el codebase inicial
- [ ] Integrado en IDE (VS Code muestra errores inline)

**Anti-patrones:**
- ❌ **Sin linter:** Cada developer escribe con su propio estilo — inconsistencia total.
- ❌ **200 rules custom:** Sobre-configuración que genera fatiga — usar una guía estándar con mínimas customizaciones.
- ❌ **Todos los errores como "warn":** Warnings se ignoran — los errores reales deben ser "error".
- ❌ **`// eslint-disable` everywhere:** Desactivar reglas en vez de arreglar el código — derrota el propósito.

**Template:** `phases/04-development/deliverables/.eslintrc.json` *(pendiente)*

---

### 4.1.10 Formatter Configuration

| Campo | Valor |
|-------|-------|
| **Fase** | 4-Development |
| **Subfase** | 4.1 Environment Setup |
| **Responsable** | DevOps Lead |
| **Ejecuta** | Tech Lead |
| **Aprueba** | Tech Lead |
| **Formato** | .prettierrc / config |
| **Obligatorio** | ✅ |
| **Esfuerzo típico** | 0.25 día |
| **Frecuencia** | Una vez |

**Perfil de ejecución:** Requiere configuración básica del formatter — deliberadamente pocas opciones para evitar debates.  
En VTT: un agente puede generar la configuración del formatter. Es altamente delegable. Necesita brief con: decisiones de estilo (tabs/spaces, quotes, semicolons, print width).

**Qué es:** Configuración del formatter automático: Prettier para JS/TS/CSS/HTML, Black para Python, gofmt para Go. Define las pocas opciones configurables: tab width (2/4), quotes (single/double), semicolons (yes/no), trailing commas, print width (80/100/120). El formatter re-formatea el código automáticamente — no hay debates de estilo.

**Para qué sirve:** Elimina los debates de estilo más tediosos: "tabs o spaces?", "semicolons o no?", "comillas simples o dobles?". Se configura una vez y el formatter aplica automáticamente en cada save (IDE) y cada commit (pre-commit hook). Los PRs nunca tienen cambios de formatting mezclados con cambios de lógica.

**Inputs requeridos:**
- `3B.2.2` Coding Standards — decisiones de estilo

**Dependencias (predecessors):**
- `3B.2.2` Coding Standards *(obligatorio)*

**Habilita (successors):**
- `4.1.7` Pre-commit Hooks — formatting en pre-commit
- `4.1.6` IDE Configuration — format on save
- Código visualmente consistente en todo el proyecto

**Secciones esperadas:
- `.prettierrc` — configuración
- `.prettierignore` — archivos excluidos

**Criterio de completitud:
- [ ] Configuración de Prettier (o equivalente) commiteada
- [ ] Integrada con ESLint (eslint-config-prettier para evitar conflictos)
- [ ] Format on save funciona en VS Code
- [ ] Pre-commit hook formatea staged files
- [ ] Cero archivos sin formatear en el codebase

**Anti-patrones:**
- ❌ **Formatter vs Linter en conflicto:** ESLint dice semicolons, Prettier dice no semicolons — usar eslint-config-prettier.
- ❌ **Print width de 200:** Líneas que requieren scroll horizontal — 80-120 es legible.
- ❌ **Sin formatter:** Formatting manual = inconsistente = PRs con noise de whitespace.
- ❌ **Debates de configuración eternos:** Prettier tiene pocas opciones por diseño — elegir y seguir adelante.

**Template:** `phases/04-development/deliverables/.prettierrc` *(pendiente)*

---

## Tabla resumen de ejecutores — Fase 4.1 Environment Setup

| Deliverable | Responsable | Ejecuta | Delegable VTT |
|-------------|-------------|---------|---------------|
| 4.1.1 Development Environment | DevOps Lead | DevOps Lead | ✅ — puede generar Docker Compose y Dockerfiles |
| 4.1.2 Environment Setup Guide | DevOps Lead | DevOps Lead | ✅ — puede generar guía step-by-step |
| 4.1.3 Environment Variables | DevOps Lead | DevOps Lead | ✅ — puede generar .env.example documentado |
| 4.1.4 Docker Compose | DevOps Lead | DevOps Lead | ✅ — puede generar docker-compose.yml completo |
| 4.1.5 Makefile / Scripts | DevOps Lead | DevOps Lead | ✅ — puede generar Makefile con targets |
| 4.1.6 IDE Configuration | DevOps Lead | Tech Lead | ✅ — puede generar .vscode/ configs |
| 4.1.7 Pre-commit Hooks | DevOps Lead | DevOps Lead / Tech Lead | ✅ — puede generar config de Husky + lint-staged |
| 4.1.8 Git Configuration | DevOps Lead | DevOps Lead | ✅ — puede generar .gitignore y .gitattributes |
| 4.1.9 Linter Configuration | DevOps Lead | Tech Lead | ✅ — puede generar configuración de ESLint |
| 4.1.10 Formatter Configuration | DevOps Lead | Tech Lead | ✅ — puede generar configuración de Prettier |

---

## Siguiente archivo

**Próximo:** `DICCIONARIO_FASE_04_02_DATABASE_IMPLEMENTATION.md` — 10 deliverables (4.2.1 a 4.2.10)
