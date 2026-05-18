#!/usr/bin/env python3
"""
Memory Service R1 — Generate + Upload 26 BRIEFs (Phase 1 Project Setup)
========================================================================
1. Genera un BRIEF por cada tarea INIT-A..G (26 archivos .md)
2. Los guarda en knowledge/agent-tasks/briefs/phase1/
3. Los sube como attachments a cada tarea VTT via POST multipart

Requiere:
  VTT_UUIDS_PHASE1_RESTRUCTURED.json (generado por restructure_phase1_vtt.py)
  VTT_SERVICE_KEY en el entorno
"""

import os, sys, json, time, uuid, mimetypes, urllib.request, urllib.error
from pathlib import Path

API_URL     = os.environ.get("VTT_API_URL", "http://77.42.88.106:3000")
SERVICE_KEY = os.environ.get("VTT_SERVICE_KEY")
if not SERVICE_KEY:
    sys.exit("ERROR: Define VTT_SERVICE_KEY antes de ejecutar.")

PJM_UUID = "0ff63a29-0bc0-465a-b9bd-5f71476bc91d"
UUIDS_FILE = "VTT_UUIDS_PHASE1_RESTRUCTURED.json"
BRIEFS_DIR = Path(__file__).resolve().parents[3] / "knowledge" / "agent-tasks" / "briefs" / "phase1"
BRIEFS_DIR.mkdir(parents=True, exist_ok=True)

# ── Detalle completo por tarea para generar BRIEFs ──────────────────────────
# (code, titulo, rol, horas, complex, status, prioridad, objetivo, contexto, entregable, criterios, como_probar)
BRIEFS_DATA = [
    # ══════════════════════════ A. VTT Setup ═════════════════════════════════
    ("INIT-A-01", "Verificar proyecto en VTT", "PJM", 1, "LOW", "completed", "M",
     "Confirmar que el Project 'Memory Service R1' existe en VTT con los metadatos correctos (key MEM, owner PM).",
     "Es la primera verificacion del entorno VTT antes de crear cualquier fase/tarea. El proyecto fue creado por el script `create_memory_service_vtt.py` durante la carga inicial.",
     "Evidencia de que el proyecto existe con projectId `d0fc276d-e764-4a83-96e9-d65f086ed803`, nombre 'Memory Service R1' y owner PM.",
     ["Proyecto visible en GET /api/projects/{id}", "key = 'MEM'", "ownerId = PM UUID", "statusId valido"],
     "curl -H 'Authorization: Bearer $TOKEN' http://77.42.88.106:3000/api/projects/d0fc276d-e764-4a83-96e9-d65f086ed803"),

    ("INIT-A-02", "Verificar 10 fases en VTT", "PJM", 1, "LOW", "completed", "M",
     "Validar que las 10 fases del proyecto (Project Setup ... Operations) estan creadas con order y status correctos.",
     "Las fases fueron creadas por el script de carga inicial. Validar estructura antes de crear deliveries/tareas.",
     "Listado completo de 10 fases con sus UUIDs registrado en PROJECT_MEMORY §6.",
     ["10 fases en orden correcto (1-10)", "Nombres coinciden con el plan (Project Setup, Discovery, Planning, Analysis, Design UX/UI, Design Technical, Development, Testing, Deploy, Operations)", "Status phase_pending"],
     "curl -H 'Authorization: Bearer $TOKEN' http://77.42.88.106:3000/api/projects/{id}/phases"),

    ("INIT-A-03", "Verificar 65 deliveries en VTT", "PJM", 1, "LOW", "completed", "M",
     "Validar que los 65 deliveries distribuidos por fase estan creados correctamente.",
     "Los deliveries agrupan tareas dentro de cada fase. Se cargaron en el script inicial.",
     "Lista de 65 deliveries con UUIDs guardada en VTT_UUIDS_MEMORY_SERVICE.json.",
     ["65 deliveries totales", "Cada uno vinculado a su phaseId correcto", "Nombres coinciden con el plan maestro"],
     "Recorrer las 10 fases con GET /api/phases/{id}/deliveries y contar. Suma debe ser 65."),

    ("INIT-A-04", "PATCH 116 tareas en VTT con metadata completa", "PJM", 2, "MEDIUM", "pending", "H",
     "Validar que las 116 tareas originales tienen metadata correcta: assigneeId, complexity MAYUSCULAS, category valida, estimatedHours, priorityId.",
     "Las tareas fueron creadas en la carga inicial. Hay reassignments pendientes (MEM-022 pasa de TL a SA, MEM-039 pasa de TL a AR) documentados en el CIERRE_PM.",
     "Reporte de validacion con las 116 tareas y sus campos. Reassignments aplicados.",
     ["116 tareas validadas", "Todos con assignedToId (no NULL)", "complexity en MAYUSCULAS", "category en lista valida", "estimatedHours > 0", "priorityId valido", "MEM-022 → SA", "MEM-039 → AR"],
     "Script de validacion: recorrer tareas y verificar campos. PATCH las que tengan errores."),

    ("INIT-A-05", "Crear 15 dependencias criticas en VTT", "PJM", 3, "MEDIUM", "pending", "H",
     "Registrar las 15 dependencias criticas inter-fase para que el Gantt refleje el orden correcto.",
     "Incluye el HITO CRITICO: MEM-038 (Design Handoff Final) → MEM-081 (primera tarea FE). Sin esto, el Gantt muestra fases en paralelo incorrectamente.",
     "15 dependencias registradas en VTT via POST /api/tasks/{id}/dependencies. Gantt muestra flujo secuencial entre fases.",
     ["15 dependencias POSTeadas sin errores", "MEM-038 → MEM-081 visible", "Cada dep tiene razon documentada", "Gantt valida el orden"],
     "Script `create_memory_service_vtt.py` ya incluye el bloque. Validar con GET /api/tasks/{id}/dependencies."),

    # ══════════════════════════ B. Repository Setup ══════════════════════════
    ("INIT-B-01", "Crear y verificar repo Git", "DO", 1, "MEDIUM", "blocked", "H",
     "Crear repo Git oficial del Memory Service en GitHub con la URL correcta (actual apunta por error a twitter-react.git).",
     "🔴 BLOQUEADO: requiere que el PM defina el esquema multi-repo (PROJECT_RULES §8). Sin decision, toda la categoria B (INIT-B-02..B-05) no puede avanzar.",
     "Repo en GitHub accesible con la URL correcta. README inicial. Rama main protegida.",
     ["Repo creado en GitHub con URL correcta", "Rama main por default", "Acceso configurado para el equipo", "Clone funciona localmente"],
     "git clone <URL>; git remote -v debe mostrar la URL correcta."),

    ("INIT-B-02", "Inicializar estructura de carpetas V3.1", "PJM", 1, "LOW", "pending", "M",
     "Crear la estructura de carpetas V3.1 definida en PROJECT_RULES: phases/00-discovery a phases/07-operations, _pm/, docs/, archive/, .claude/agents/.",
     "La estructura V3.1 es el estandar de VTT para proyectos. Permite que agentes encuentren docs de forma consistente.",
     "Estructura de carpetas committeada. README.md explica cada carpeta.",
     ["phases/00-discovery a phases/07-operations existen", "_pm/ existe", "docs/ existe", "archive/ existe", ".claude/agents/ existe", "README explica cada una"],
     "ls -la debe mostrar las 4 carpetas base + phases/. git log muestra el commit."),

    ("INIT-B-03", "Configurar archivos base del repo", "PJM", 1, "LOW", "pending", "M",
     ".gitignore (node_modules, dist, .env, storage/), .gitattributes (LF line endings), .editorconfig (2 spaces TS, LF), README.md inicial, CONTRIBUTING.md con flujo.",
     "Archivos base que todo repo debe tener para que el equipo trabaje con configuracion consistente.",
     "5 archivos committeados con contenido estandar.",
     [".gitignore excluye node_modules, dist, .env", ".gitattributes fuerza LF", ".editorconfig 2 spaces + LF", "README describe el proyecto", "CONTRIBUTING describe workflow de PRs"],
     "Crear un archivo .env local y verificar que no aparece en git status."),

    ("INIT-B-04", "Branch protection + CODEOWNERS + PR template", "DO", 1, "MEDIUM", "pending", "M",
     "Activar branch protection en main y configurar CODEOWNERS + template de PR.",
     "Sin branch protection, los agentes pueden hacer merge directo. CODEOWNERS define revisores automaticos. PR template asegura que cada PR lleve info minima.",
     "Protecciones visibles en GitHub Settings > Branches. CODEOWNERS reconocido. Template aparece al abrir un PR.",
     ["main requiere PR", "main requiere 1 aprobacion", "main requiere status checks (CI)", "CODEOWNERS define PM + TL como owners globales", "PR template obliga a linkear TASK_ID"],
     "Intentar push directo a main (debe fallar). Abrir PR de prueba y verificar template."),

    ("INIT-B-05", "Git user config + commit conventions", "PJM", 1, "LOW", "pending", "M",
     "Configurar git user.name y user.email locales + documentar convention de commits.",
     "Sin convention de commits, el changelog es caotico. El formato [tipo] [TASK_ID]: descripcion + Co-Authored-By permite trackear quien hizo que.",
     "Git config verificado con los datos del PM. Convention documentada en CONTRIBUTING.",
     ["git config user.name = 'Martin Rivas'", "git config user.email = 'martin.rivas@prompt-ai.studio'", "CONTRIBUTING documenta el formato", "Co-Authored-By obligatorio"],
     "git config --get user.name y user.email debe devolver los valores correctos."),

    # ══════════════════════════ C. VM Configuration ══════════════════════════
    ("INIT-C-01", "Verificar infraestructura provisionada en Hetzner", "DO", 1, "MEDIUM", "completed", "H",
     "Validar que la infra base en Hetzner (77.42.88.106) esta lista para hostear Memory Service.",
     "El Admin VM provisiono los recursos segun SPEC v1.9 §16. Validar antes de correr el resto.",
     "Checklist de 6 items verificados y documentados en docs/INFRASTRUCTURE.md.",
     ["BD memory_service_db accesible en shared-postgres", "Volumen /root/memory-service-storage/ con permisos", "Redis prefix mem OK", "Puertos 3002 y 3003 abiertos en firewall", "shared-network Docker existe", "SERVICE_KEY generada en .env del server"],
     "psql al memory_service_db, ls en el volumen, redis-cli PING con prefix, nc -zv 77.42.88.106 3002."),

    ("INIT-C-02", "Tests de conectividad local a VM", "DO", 1, "MEDIUM", "pending", "M",
     "Validar que desde la maquina local (desarrollo) se puede acceder a todos los servicios de la VM.",
     "Sin conectividad local, los desarrolladores no pueden probar features antes de deploy.",
     "Reporte de tests en INFRASTRUCTURE.md mostrando cada conexion OK.",
     ["Prisma puede conectar al memory_service_db", "Escritura en /storage/ desde container Docker OK", "Redis PING OK con prefix mem", "curl a http://77.42.88.106:3002/health responde 200"],
     "Ejecutar cada test y adjuntar output al INFRASTRUCTURE.md."),

    ("INIT-C-03", "Distribuir SERVICE_KEY a consumidores", "DO", 1, "MEDIUM", "pending", "H",
     "Entregar el SERVICE_KEY del Memory Service a los 4 servicios que van a consumirlo.",
     "Sin SERVICE_KEY, los consumidores no pueden autenticarse al Memory Service. Son 4: Runtime v1.1, Prompt Builder v1.3, Hook Manager, FE.",
     "Confirmacion escrita de que los 4 consumidores recibieron y probaron la key.",
     ["Runtime v1.1 recibio SERVICE_KEY y autentica OK", "Prompt Builder v1.3 recibio y autentica OK", "Hook Manager recibio y autentica OK", "FE recibio como variable env y autentica OK"],
     "Pedir a cada consumidor un curl de prueba con su nueva key."),

    ("INIT-C-04", "Documentar configuracion VM en repo", "DO", 1, "LOW", "pending", "M",
     "Escribir docs/INFRASTRUCTURE.md con toda la info operativa de la VM.",
     "Cuando haya que rebuild o escalar, este doc es la fuente de verdad. Sin el, hay que reinventar.",
     "docs/INFRASTRUCTURE.md committeado con secciones minimas.",
     ["IP servidor (77.42.88.106)", "Puertos (3002 API, 3003 UI)", "Paths (/root/memory-service-storage/)", "Schema de backups + retencion", "Procedimiento de escalacion al Admin VM", "Variables env esperadas"],
     "Abrir docs/INFRASTRUCTURE.md y revisar que cubre las 6 secciones."),

    # ══════════════════════════ D. Agent Team Setup ══════════════════════════
    ("INIT-D-01", "Crear OPERATIVO por cada rol activo", "PM", 3, "MEDIUM", "in_progress", "H",
     "Crear .claude/agents/OPERATIVO_<ROL>.md para cada uno de los 12 roles del proyecto.",
     "Cada OPERATIVO define: funciones del rol, tokens, endpoints VTT, referencias a reglas. Sin esto, los agentes no saben que pueden/no pueden hacer. Hechos: PM, TL (2/12). Pendientes: 10. Prioridad: BE + DB + DO antes de S01.",
     "12 archivos OPERATIVO_<ROL>.md en .claude/agents/.",
     ["OPERATIVO_PM.md ✅", "OPERATIVO_TL.md ✅", "OPERATIVO_PJM.md", "OPERATIVO_SA.md", "OPERATIVO_AR.md", "OPERATIVO_BE.md (prio)", "OPERATIVO_DB.md (prio)", "OPERATIVO_DO.md (prio)", "OPERATIVO_FE.md", "OPERATIVO_UX.md", "OPERATIVO_DL.md", "OPERATIVO_QA.md"],
     "ls .claude/agents/ | wc -l debe dar 12."),

    ("INIT-D-02", "Consolidar PROJECT_MEMORY.md", "PM", 1, "LOW", "completed", "M",
     "Consolidar PROJECT_MEMORY.md con toda la info persistente del proyecto.",
     "PROJECT_MEMORY es la memoria que todo agente lee al inicio de sesion. Evita tener que re-explicar el contexto.",
     "PROJECT_MEMORY.md en el repo con secciones minimas.",
     ["Stack tecnologico", "Fases + horas", "Decisiones D-XX aprobadas", "UUIDs del equipo", "Referencias a SPEC v1.9"],
     "cat PROJECT_MEMORY.md debe tener al menos 5 secciones."),

    ("INIT-D-03", "CONTEXTO de sesion por rol", "PJM", 1, "LOW", "in_progress", "M",
     "Crear knowledge/agent-tasks/CONTEXTO_<ROL>_SESION.md para los 8 roles principales.",
     "El CONTEXTO es el resumen que el rol lee al retomar sesion. Diferente del OPERATIVO (que es permanente). Hecho: PM (1/8). Pendientes: 7.",
     "8 archivos CONTEXTO en knowledge/agent-tasks/.",
     ["CONTEXTO_PM ✅", "CONTEXTO_TL", "CONTEXTO_PJM", "CONTEXTO_BE", "CONTEXTO_FE", "CONTEXTO_DB", "CONTEXTO_DO", "CONTEXTO_QA"],
     "ls knowledge/agent-tasks/CONTEXTO_*.md debe dar 8 archivos."),

    ("INIT-D-04", "Distribuir accesos al equipo", "PJM", 1, "LOW", "pending", "M",
     "Verificar que cada rol activo tiene los accesos necesarios: repo Git, UUID VTT, SERVICE_KEY.",
     "Sin accesos, el rol no puede empezar a trabajar. Matriz de accesos evita olvidos.",
     "Matriz de accesos rol × recurso documentada.",
     ["Cada rol confirmado con acceso al repo", "Cada rol confirmado con UUID VTT", "Cada rol confirmado con SERVICE_KEY", "Matriz actualizada en _pm/ACCESOS.md"],
     "Enviar mensaje a cada rol pidiendo confirmacion de acceso."),

    ("INIT-D-05", "Reuniones de onboarding por rol", "PM", 3, "MEDIUM", "pending", "M",
     "Sesion de kickoff 1:1 con cada rol activo donde se revisa el contexto del proyecto.",
     "El onboarding personal permite resolver dudas que la lectura del doc no cubre. Sin el, los roles arrancan con interpretaciones distintas.",
     "Actas de onboarding por rol archivadas.",
     ["Sesion con BE realizada + acta", "Sesion con DB realizada + acta", "Sesion con DO realizada + acta", "Sesion con FE realizada + acta", "Sesion con QA realizada + acta", "Sesion con TL realizada + acta", "Sesion con SA realizada + acta", "Sesion con AR realizada + acta"],
     "Agendar en calendario. Tomar nota en _pm/onboarding/<ROL>.md."),

    # ══════════════════════════ E. Tooling Setup ═════════════════════════════
    ("INIT-E-01", "Base Node + TypeScript backend", "DO", 2, "MEDIUM", "pending", "H",
     "Bootstrappear el proyecto backend con Node 20 + TypeScript + scripts base.",
     "Sin esto, los agentes BE no pueden empezar a codificar. Debe estar listo ANTES del sprint S01.",
     "package.json + tsconfig + nodemon + .nvmrc committeados. npm install funciona.",
     ["package.json con scripts: dev, build, start, test, lint, format, migrate, seed", "tsconfig.json estricto (strict:true)", ".nvmrc con 20", "nodemon.json para dev mode", "Dependencias: express, typescript, tsx, prisma, redis, swagger-jsdoc, swagger-ui-express"],
     "nvm use; npm install; npm run dev debe levantar el server."),

    ("INIT-E-02", "Linters + formatters + pre-commit hooks", "DO", 1, "LOW", "pending", "M",
     "Configurar ESLint + Prettier + Husky + lint-staged para bloquear commits invalidos.",
     "Sin pre-commit hooks, se cuela codigo sin lint al repo. Los PRs tardan mas por ida y vuelta de estilo.",
     "Husky instalado. Pre-commit ejecuta lint + prettier + type-check.",
     [".eslintrc.json con reglas TS estrictas", ".prettierrc con config del proyecto", "Husky configurado en package.json", "lint-staged configurado", "Commit con error de lint falla el hook"],
     "Intentar commit con error de lint - debe fallar."),

    ("INIT-E-03", "CI minimo (smoke) en GitHub Actions", "DO", 1, "MEDIUM", "pending", "M",
     "Crear workflow de CI que corra build + lint + test en cada PR.",
     "Sin CI, no hay forma automatica de validar que el PR no rompe nada. El CI completo de deploy va en MEM-105.",
     ".github/workflows/ci.yml committeado y corriendo en PRs.",
     ["ci.yml trigger on pull_request", "Node 20 con cache de npm", "Steps: install, lint, type-check, test, build", "Falla el CI bloquea el merge", "PR de prueba pasa CI en verde"],
     "Abrir un PR vacio; CI debe correr y terminar OK."),

    # ══════════════════════════ F. Documentation ═════════════════════════════
    ("INIT-F-01", "README + CONTRIBUTING del repo", "PM", 1, "LOW", "pending", "M",
     "README.md con vista general del proyecto y CONTRIBUTING.md con workflow para el equipo.",
     "El README es lo primero que ve alguien nuevo. CONTRIBUTING evita que cada agente invente su propio flow.",
     "2 archivos committeados en la raiz del repo.",
     ["README: descripcion + stack + setup local + links a SPEC y PROJECT_RULES", "CONTRIBUTING: branches, commits, PRs, reviews, conventions"],
     "Leer el README y poder hacer setup local sin preguntar."),

    ("INIT-F-02", "ARCHITECTURE.md operativo", "TL", 1, "MEDIUM", "pending", "M",
     "docs/ARCHITECTURE.md con resumen arquitectonico breve + link a SPEC v1.9.",
     "ARCHITECTURE es vista de alto nivel para onboarding rapido. NO duplica SPEC (que es el contrato completo).",
     "docs/ARCHITECTURE.md committeado.",
     ["Resumen en 1 pagina de la arquitectura", "Diagrama de componentes (ASCII u otro)", "Link al SPEC v1.9 consolidado", "No duplica el SPEC"],
     "Leer ARCHITECTURE en 5 min y entender como estan conectadas las piezas."),

    # ══════════════════════════ G. Kickoff ═══════════════════════════════════
    ("INIT-G-01", "Documento formal de Kickoff", "PM", 2, "MEDIUM", "pending", "H",
     "KICKOFF_MEMORY_SERVICE.md con vision + alcance + equipo + roadmap + riesgos.",
     "Es el documento oficial de arranque. Firma el PM y se usa como referencia durante todo el proyecto.",
     "KICKOFF_MEMORY_SERVICE.md firmado por el PM.",
     ["Vision del producto", "Objetivos R1 medibles", "Alcance in/out (LIM-XX)", "Equipo + roles + UUIDs", "Roadmap con fechas por fase", "Riesgos principales", "Criterios de exito R1"],
     "Revisar el doc en plenario. Firmar en caja ASCII."),

    ("INIT-G-02", "Kickoff call del equipo (GATE)", "PM", 1, "HIGH", "pending", "C",
     "🚨 HITO: sesion de arranque con el equipo completo. Es el GATE que habilita Fase 2 Discovery.",
     "Sin este kickoff, la Fase 2 no puede empezar. Es el cierre formal de la Fase 1 Project Setup.",
     "Acta de kickoff con compromisos por rol + action items + siguiente fase iniciada.",
     ["Todos los roles activos presentes o acuse asincrono", "Revision del KICKOFF doc", "Compromisos escritos por rol", "Action items con owner y deadline", "PJM confirma que Fase 2 arranca formalmente"],
     "Leer el acta y poder identificar quien hace que en los proximos 2 sprints."),
]


# ── Helpers ──────────────────────────────────────────────────────────────────

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def auth_token():
    req = urllib.request.Request(
        f"{API_URL}/api/auth/service-token",
        data=json.dumps({"userId": PJM_UUID, "serviceKey": SERVICE_KEY}).encode(),
        headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())["data"]["token"]


def render_brief(data):
    (code, title, role, hours, complex_, status, prio,
     objetivo, contexto, entregable, criterios, como_probar) = data

    lines = [
        f"# BRIEF: {code} - {title}",
        "",
        f"**Tarea**: {code}",
        f"**Titulo**: {title}",
        f"**Repositorio**: memory-service",
        f"**Asignado a**: {role}",
        f"**Prioridad**: {prio} ({'CRITICAL' if prio=='C' else 'HIGH' if prio=='H' else 'MEDIUM' if prio=='M' else 'LOW'})",
        f"**Estimacion**: {hours} horas",
        f"**Complejidad**: {complex_}",
        f"**Categoria**: {'documentation' if role in ('PM','PJM','TL') else 'deployment'}",
        f"**Estado inicial**: {status}",
        f"**Creado por**: PJM (Martin Rivas)",
        f"**Fecha de creacion**: 2026-04-22",
        "",
        "---",
        "",
        "## 1. Objetivo",
        "",
        objetivo,
        "",
        "**Resultado esperado:** " + entregable,
        "",
        "---",
        "",
        "## 2. Contexto",
        "",
        contexto,
        "",
        "---",
        "",
        "## 3. Campos del Sistema VTT",
        "",
        "Valores con los que se creo la tarea en VTT:",
        "",
        "| Campo API | Valor |",
        "|-----------|-------|",
        f"| `title` | {code}: {title} |",
        f"| `estimatedHours` | {hours} |",
        f"| `complexity` | {complex_} |",
        f"| `category` | {'documentation' if role in ('PM','PJM','TL') else 'deployment'} |",
        f"| `priorityId` | (UUID correspondiente a {prio}) |",
        f"| `statusId` | (UUID correspondiente a {status}) |",
        f"| `assignedToId` | UUID del agente rol {role} |",
        "",
        "---",
        "",
        "## 4. Dependencias",
        "",
        "### Prerrequisitos (deben estar OK antes de arrancar)",
        "",
        "- Ambiente VTT accesible (http://77.42.88.106:3000)",
        "- SERVICE_KEY del agente asignado entregada",
        "- Token JWT valido (30 dias de validez)",
        "",
        "### Documentos a leer",
        "",
        "- `memory-service-project/01-project-management/00-setup/HO_INICIACION_MEMORY_SERVICE.md` (seccion correspondiente a la categoria)",
        "- `memory-service-project/Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` (si aplica)",
        "- `PROJECT_RULES.md` (reglas de commits, branches, code logic)",
        "",
        "---",
        "",
        "## 5. Criterios de Exito",
        "",
    ]
    for crit in criterios:
        lines.append(f"- [ ] {crit}")

    lines += [
        "",
        "### No Funcionales",
        "",
        "- [ ] Sigue convenciones del proyecto",
        "- [ ] Sin codigo/config hardcodeado que deba ser variable",
        "- [ ] Manejo de errores apropiado",
        "",
        "### Documentacion",
        "",
        "- [ ] Development Log completo",
        "- [ ] Code Logic (.LOGIC.md) si se creo/modifico codigo",
        "- [ ] Referencias cruzadas a otros docs del proyecto",
        "",
        "---",
        "",
        "## 6. Como Probar",
        "",
        como_probar,
        "",
        "---",
        "",
        "## 7. Referencias",
        "",
        "### Documentacion Interna",
        "",
        "- `HO_INICIACION_MEMORY_SERVICE.md` - Handoff PM->PJM con desglose completo de INIT-*",
        "- `SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` - Contrato tecnico",
        "- `PROJECT_RULES.md` v1.4 - Reglas operativas del proyecto",
        "- `PROCESO_ASIGNACION_TAREAS.md` - Proceso para que TL genere ASSIGNMENTs",
        "",
        "### UUIDs y Endpoints Utiles",
        "",
        "- API Base: `http://77.42.88.106:3000`",
        "- Swagger: `http://77.42.88.106:3000/api-docs`",
        "- Auth: `POST /api/auth/service-token`",
        "- Task status update: `PATCH /api/tasks/{id}/status`",
        "",
        "---",
        "",
        "## 8. Notas Importantes",
        "",
        "- Este BRIEF describe **QUE** hay que hacer. Cuando se asigne la tarea, el TL generara un **ASSIGNMENT** con el CUANDO/COMO especifico (archivos reales, endpoints confirmados, decisiones tecnicas).",
        "- Antes de mover la tarea a `task_in_review`, el agente debe subir 3 entregables: DevLog, Code Logic (si hubo codigo), y un comentario con el reporte de entrega.",
        "- Las tareas umbrella MEM-001..005 fueron canceladas (estado `task_cancelled`) por ser demasiado alto nivel. Esta tarea INIT-* las reemplaza.",
        "",
        "---",
        "",
        "## 9. Dependencias de Esta Tarea",
        "",
        "### Tareas Desbloqueadas al Completar",
        "",
        "- (Ver HO_INICIACION §5 ORDEN DE EJECUCION para el detalle)",
        "",
        "---",
        "",
        "## 10. Contacto",
        "",
        "**PM / Coordinador**: Martin Rivas (martin.rivas@prompt-ai.studio)",
        "**Preguntas**: Via comment en VTT o mensaje directo al PM/PJM",
        "",
        "---",
        "",
        "**Ultima actualizacion:** 2026-04-22",
        "**Version:** 1.0",
        "**Estado del BRIEF:** Ready",
        "",
    ]

    return "\n".join(lines)


def build_multipart(fields, files):
    """Construye body multipart/form-data sin dependencias externas."""
    boundary = "----MemoryServiceBrief" + uuid.uuid4().hex
    body = b""
    for key, value in fields.items():
        body += f"--{boundary}\r\n".encode()
        body += f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode()
        body += f"{value}\r\n".encode()
    for key, (filename, content, content_type) in files.items():
        body += f"--{boundary}\r\n".encode()
        body += f'Content-Disposition: form-data; name="{key}"; filename="{filename}"\r\n'.encode()
        body += f"Content-Type: {content_type}\r\n\r\n".encode()
        body += content
        body += b"\r\n"
    body += f"--{boundary}--\r\n".encode()
    return body, f"multipart/form-data; boundary={boundary}"


def upload_brief(task_id_or_uuid, file_path, token):
    with open(file_path, "rb") as f:
        file_content = f.read()

    fields = {"fileType": "brief", "uploadedById": PJM_UUID}
    files = {"file": (file_path.name, file_content, "text/markdown")}
    body, content_type = build_multipart(fields, files)

    req = urllib.request.Request(
        f"{API_URL}/api/tasks/{task_id_or_uuid}/attachments",
        data=body,
        headers={"Content-Type": content_type, "Authorization": f"Bearer {token}"},
        method="POST")

    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read()), None
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="ignore")
        return None, f"{e.code} - {detail[:300]}"


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    log("=" * 70)
    log("Memory Service R1 - Generate + Upload 26 BRIEFs")
    log("=" * 70)

    if not os.path.exists(UUIDS_FILE):
        sys.exit(f"ERROR: falta {UUIDS_FILE}. Ejecutar primero restructure_phase1_vtt.py.")

    with open(UUIDS_FILE, encoding="utf-8") as f:
        uuids = json.load(f)

    token = auth_token()
    log("Token OK\n")

    generated, uploaded, errors = 0, 0, 0

    for data in BRIEFS_DATA:
        code = data[0]
        info = uuids["tasks"].get(code)
        if not info:
            log(f"  ERROR {code}: no esta en VTT_UUIDS_PHASE1_RESTRUCTURED.json")
            errors += 1
            continue

        # 1. Generar archivo BRIEF
        filename = f"BRIEF_{code}_{data[1].lower().replace(' ', '-').replace(',', '').replace('.', '')[:40]}.md"
        brief_path = BRIEFS_DIR / filename
        brief_content = render_brief(data)
        brief_path.write_text(brief_content, encoding="utf-8")
        generated += 1

        # 2. Subir como attachment
        task_uuid = info["uuid"]
        resp, err = upload_brief(task_uuid, brief_path, token)
        if err:
            log(f"  WARN {code}: upload fallo ({err})")
            errors += 1
        else:
            uploaded += 1
            log(f"  OK   {code} [{info['vttCode']}] - brief generado + subido")

    log("")
    log("=" * 70)
    log("RESUMEN")
    log("=" * 70)
    log(f"BRIEFs generados localmente: {generated} / 26")
    log(f"BRIEFs subidos a VTT:        {uploaded} / 26")
    log(f"Errores:                     {errors}")
    log(f"Carpeta local:               {BRIEFS_DIR}")
    log("=" * 70)


if __name__ == "__main__":
    main()
