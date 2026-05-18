Te bajo el problema y las opciones concretas.

El problema en sus términos

virtual-teams-setup (fuente de verdad)
       │
       ├──── consume Proyecto A (Memory Service) — N agentes
       ├──── consume Proyecto B — N agentes
       └──── consume Proyecto C — N agentes

Tres equipos editando en paralelo:
  - Equipo Perfiles → actualiza OPERATIVOs por rol
  - Equipo Worktrees → actualiza estructura .vtt/ + procesos
  - Tú/TL → actualiza Protocols/Workflows/Skills/Rules

Riesgo:
  1. Tres equipos editando lo mismo → conflictos / overwrites
  2. Si VTT-setup cambia → ¿cómo se entera Proyecto A, B, C?
  3. ¿Quién decide qué entra a la fuente de verdad?
Son dos problemas distintos que la conversación está mezclando. Lo crítico es separarlos antes de elegir solución.

Problema 1 — Quién puede modificar la fuente de verdad
Sin gobierno editorial → caos garantizado.

Necesitas reglas tipo:

Tipo de documento	Quién puede editar	Aprobación
OPERATIVOs por rol	Equipo Perfiles	Review del PM
Worktrees / procesos operativos	Equipo Worktrees	Review del PM
Protocols / Workflows / Rules	Tú/TL	Review del PM
Templates (BRIEF, ASSIGNMENT, etc.)	Cualquiera con aprobación	PR review
Solución base: branch protection en GitHub sobre virtual-teams-setup. Nadie commitea directo a main. Todos los cambios via PR + 1 aprobador (PM o TL). Es 30 min de setup y elimina el 80% del problema.

Problema 2 — Cómo se propaga el cambio a los proyectos consumidores
Aquí están las opciones del agente de Perfiles vs Worktrees vs lo que yo creo. Te las pongo lado a lado.

Opción A — Symlinks / shared filesystem (lo más simple)

virtual-teams-setup/      ← fuente única
       ↑ symlinks
memory-service/.vtt-normativa → ../../virtual-teams-setup/00-agent-setup/07.Normativa
designmine/.vtt-normativa   → ../../virtual-teams-setup/00-agent-setup/07.Normativa
Cómo se actualiza: PM hace git pull en virtual-teams-setup. Todos los proyectos ven el cambio automáticamente (symlink).

Pro	Contra
0 sincronización manual	Solo funciona si los repos viven en el mismo filesystem
Cambio instantáneo	Windows requiere admin para symlinks
Sin scripts	Si VTT-setup tiene bug, TODOS los proyectos lo heredan inmediatamente (no hay "versión estable")
Opción B — Git submodule (control de versión)

memory-service-project/
  └── .vtt-normativa/  ← submodule pinned a virtual-teams-setup @ commit abc123
Cómo se actualiza: En cada proyecto, el TL hace git submodule update --remote cuando quiere traer cambios de VTT-setup. Pin a versiones específicas.

Pro	Contra
Cada proyecto fija su versión (estable)	Submodules son confusos para nuevos integrantes
No hay "rotura silenciosa"	Hay que recordar actualizar submodule (no es automático)
Auditoría completa: cada commit del proyecto dice qué versión de normativa usa	Trabajo extra cada vez que el PM publica versión nueva
Opción C — Release versionado + script de sincronización (mi recomendación)

virtual-teams-setup/
  ├── releases/
  │   ├── v1.0.0/  (snapshot inmutable)
  │   ├── v1.1.0/
  │   └── v1.2.0/  (current — el PM declara cuál es current)
  └── scripts/
      └── sync_to_project.py [proyecto] [version]

memory-service-project/
  └── .vtt-normativa-sync/
      ├── VERSION              ← v1.2.0
      ├── synced_at.txt        ← 2026-05-14
      └── (copia local de archivos sincronizados)
Cómo se actualiza:


# En VTT-setup: PM publica nueva versión
cd virtual-teams-setup
python scripts/release_normativa.py --version v1.3.0
# → crea snapshot releases/v1.3.0/
# → opcional: tag git v1.3.0

# En cada proyecto consumidor: TL/agente sincroniza
cd memory-service-project
python ../../virtual-teams-setup/scripts/sync_to_project.py . --to-version v1.3.0
# → copia archivos relevantes a .vtt-normativa-sync/
# → registra VERSION + synced_at
Pro	Contra
Cada proyecto controla cuándo actualizar	Implementación inicial: 1 día de scripts
Versiones explícitas (auditable)	El proyecto puede quedarse desactualizado si nadie ejecuta sync
No requiere symlinks ni submodules	Mantenimiento del script de sync
Funciona cross-filesystem	—
Opción D — Hook Manager / Pull dinámico al arrancar agente (idea futura, IMPROVE)

Agente arranca su sesión
  → Hook consulta VTT-setup última versión
  → Hook valida que el proyecto está en versión compatible
  → Si NO compatible → warn al TL/PM
  → Inyecta normativa al prompt del agente
Es la versión "enterprise" pero requiere Hook Manager existente. La registramos como IMPROVE-006 y no la atacamos ahora.

Mi recomendación concreta
Combinación A + B + C según el tipo de archivo:

Tipo	Estrategia	Por qué
Protocols / Workflows / Rules (cambian poco)	Opción C — Release versionado	Estable, auditable, los proyectos controlan cuándo actualizan
OPERATIVOs de rol (cambian cuando hay cambio de proceso)	Opción C — Release versionado	Los agentes necesitan estabilidad — no quiero que un cambio en setup les rompa la sesión a mitad de tarea
Templates (BRIEF, ASSIGNMENT)	Opción C — Release versionado	Mismo argumento
Skills / Scripts (utilidades)	Opción C	Los agentes los cargan al arrancar — necesitan versión fija
gen_mensaje.py y otros scripts ejecutables	Opción C	Pinear versión
Y para el problema 1 (gobierno):

Branch protection en virtual-teams-setup/main
Todos los cambios via PR con 1 aprobador (PM)
CODEOWNERS file que dice quién aprueba qué carpeta:

/00-agent-setup/01.operativos/   @equipo-perfiles
/00-agent-setup/04.Process/      @equipo-worktrees
/00-agent-setup/07.Normativa/    @pm @tl
Lo que propongo concretamente para esta semana
Paso 1 — Definir el gobierno editorial (1 hora)
Documento GOBIERNO_VTT_SETUP.md con:

Quién puede modificar qué carpeta
CODEOWNERS de GitHub
Política de PRs (mínimo 1 aprobador del CODEOWNERS)
Branch protection: main protegida, todo va por PR
Paso 2 — Versionado de la normativa (2 horas)
Crear releases/ folder en virtual-teams-setup
Script release_normativa.py que:
Toma el state actual de 00-agent-setup/
Hace snapshot a releases/v1.2.0/ (carpeta + tag git)
Actualiza CURRENT_VERSION.txt en raíz
Documento RELEASES.md con cambios entre versiones
Paso 3 — Script de sincronización por proyecto (3 horas)
Script sync_normativa.py que cada proyecto ejecuta
Lee VERSION deseada del proyecto (en .vtt-normativa-sync/VERSION)
Copia desde releases/v[X.Y.Z]/ a .vtt-normativa-sync/
Verifica integridad (checksums)
Paso 4 — Migrar Memory Service como primer caso (1 hora)
Crear .vtt-normativa-sync/ en memory-service-project
Pin a v1.2.0
Sync inicial
Validar que agentes pueden leer desde ese path
Paso 5 — Documento IMPROVE-006_hook_manager_normativa.md (futuro)
Registrar la idea de Hook Manager para versión 2 cuando exista.

Antes de ejecutar — preguntas decisorias
¿Quién es el editor en jefe de virtual-teams-setup/main? El PM (Martin) o un comité.

Hay tres equipos editando: Perfiles, Worktrees, TL/Tú.
¿Cada uno trabaja en su carpeta o hay zonas grises donde se solapan?
Necesito saber para definir CODEOWNERS bien.

¿Los 3 proyectos están en el mismo filesystem que virtual-teams-setup?
Si sí → Opción A (symlinks) es viable también.
Si no → solo C funciona bien.

¿Cuándo "publican" una nueva versión?

Por sprint del proyecto VTT-setup
Cuando hay cambio mayor
Cuando un proyecto pide actualización Tú decides la política.
¿Tolerancia a desfase entre proyectos?
¿Está OK que Memory Service esté en v1.2.0 y DesignMine en v1.1.0? O todos deben estar siempre en current?
Mi opinión: tolerar desfase es más sano (cada proyecto migra cuando puede).

¿Empezamos por Paso 1 (Gobierno)?
Es lo más urgente porque sin gobierno, la fuente de verdad se ensucia rápido.

Una vez respondas estos 6 puntos, generamos:

GOBIERNO_VTT_SETUP.md
CODEOWNERS
RELEASES.md con v1.2.0 como primera versión
sync_normativa.py (esquema inicial)
IMPROVE-006_hook_manager_normativa.md
¿Vamos por ahí? ¿O algún ajuste antes?

Listo. ¿Quién puede modificar los documentos? Lo que pasa es que no había considerado todavía esa parte del proyecto. Solamente pueden modificar, más bien tendríamos que hacer toda la modificación de los documentos en Virtual Setup, ¿OK? Si hay una modificación que alguien, un agente de algún proyecto necesite, se tendría que, el proceso es, se levanta un ticket o se levanta una tarea dentro de VTT, que tendríamos que definir ese proceso y esa sería una mejora que se tendría que hacer en donde cualquier agente de algún proyecto si necesita alguna mejora o nosotros detectamos algún cambio, pues en ese momento se manda directamente a Virtual Setup y ahí se trabaja, ¿no? En teoría, pues ahí puede haber uno o n cantidad de agentes, pero la gobernanza dentro del repositorio tendría que ser la misma, ¿no? ¿Por qué está así ahorita? Porque en diferentes sesiones hemos ido trabajando en diferentes cosas. Por ejemplo, aquí comenzamos en Service Project a trabajar el el el el el proceso o el protocolo de de las tareas, porque aquí fue donde empezamos a a a a a revisar todo. El problema es que cuando yo detecto a un agente que puede trabajar o está trabajando bien un proceso, ya no lo puedo cambiar. Lo saco de la operación y con ese agente sigo trabajando. ¿Por qué? Porque lo que sucede es esos procesos van surgiendo conforme vayamos trabajando. Aquí comenzamos a trabajar incluso los protocolos y los workflows, porque surgió. Por eso es que tú ya no estás viendo nada de la parte operativa. La otra parte, el otro el otro agente comenzó a trabajar la parte operativa de de. Service projects y cuando empecé a ver los problemas de los workers, le comenté qué es lo que estaba sucediendo y empezamos a trabajar en la configuración. Entonces, ese agente se convirtió directamente en el agente que está trabajando los workers, ¿no? y así sucesivamente. Entonces el problema es que eso se ha ido generando conforme hemos ido obteniendo o hemos ido viendo, pues básicamente los problemas conforme van surgiendo, ¿no? En teoría todo esto debería de estar centrado en VTT, ya creé un proyecto dentro de VTT y ya está el repositorio, entonces nos vamos a tener que mudar poco a poco hacia allá. Pero mientras yo tenga que trabajar con ciertos agentes para terminar los procesos, lo voy a tener que seguir haciendo, ¿no? Entonces por eso es que se tiene este esta situación. La idea, como dices, es generar un documento que reine y que cubra la parte normativa de la organización. Si ahorita es una actualización a LOOM o si es una actualización de varios agentes o en un futuro con una parte de un manager, no necesariamente tiene que generar y hacer una mejor actualización que generar también, ¿no? Entonces, sí, lo primero es definir la gobernanza, pero más allá de quién puede modificar la carpeta, yo creo que también, como tenemos el proceso ahorita que estamos armando con un CTO, tendríamos que ver la manera de cómo podemos armar el proceso para poder hacer la actualización y bajar directamente todas las actualizaciones a todo el repositorio. Porque partes por el mismo es que también tú lo viste, tenemos varias versiones de documentos en toda la parte de de las de los diferentes proyectos por lo mismo. ahorita ya dijimos, yo te estoy a este parte más que la verdad y o sea, ya lo vemos de nuevo por lo mismo. Si vamos a definir el gobierno editorial, sí lo tenemos que definir, lo tenemos definido y relacionado. Entonces tendríamos que definirlo. Entonces, cómo se trabajaría eso y hacer la actualización a la sincronización con todas las cosas a todos los problemas, a todos los problemas que tenemos. En este caso, yo soy el que lo está determinando, pero podemos generar un PM dentro de este sector para que lo que tú me digas que lo haga, se lo mandemos a generado y él sea el que se está controlando todo el proceso, ¿no? Este, en el caso de los equipos, sí, son tres, pueden ser tres o más equipos los que están trabajando y cada quien está en su respecto, ¿no? Este, pues básicamente que son Memory Service, Memory Service Project, Memory Service Backend y Server, que son los que están trabajando, ¿no? Los tres proyectos están en el mismo sector. No, no, porque son repositorios separados. No sé si a eso te refieres con file system, pero sí todos tienen que estar dirigidos a un solo equipo que es la fuerte de la verdad. Cuando publican una versión como la próxima, ahorita lo estoy haciendo copy paste y yo estoy haciendo el copiado de todos los archivos en un en un repositorio que quiero que lo suban y ahorita es donde estamos. No tenemos el conocimiento para poder hacer la actualización. Sí, podemos tener un desfase. Sí, sí, podría ser, pero en algún momento se puede llegar a tener, pero también la idea sería tener todo actualizado, ¿no? Eso es básicamente lo que te puedo comentar. y ahorita trabajamos sobre la parte de los pads, que es donde estamos la actualización, que es donde nos quedamos atorados.
Bajado. Te bajo el plan ordenado.

Resumen de lo que me dijiste
Punto	Lo que entiendo
Editores VTT-setup	Solo se modifica AQUÍ. Los proyectos no editan normativa — levantan ticket si necesitan cambio.
Mientras tanto	Hay agentes activos en proyectos antiguos que siguen produciendo cosas que migran después (tú haces copy/paste manual hoy).
Modelo futuro	Un PM dedicado en VTT-setup recibe tickets de mejora y aplica cambios → propaga a proyectos.
Filesystem	Repos separados (memory-service-project, memory-service-backend, virtual-teams-setup) pero en la misma máquina, en mismo árbol de carpetas.
Política de versión	Tolerar desfase entre proyectos (no todos tienen que estar en current).
Bloqueo actual	Te quedaste atorado en los paths — cómo conectar VTT-setup con los proyectos consumidores.
Los 2 problemas separados (importante)
Problema A — Gobierno editorial (quién edita qué)
Tiene que quedar formalizado:

Branch protection en virtual-teams-setup
CODEOWNERS por carpeta
Política de PRs
Proceso de ticket de mejora (improvement_request)
Problema B — Propagación de cambios (cómo bajan a proyectos)
Aquí es donde te atoraste con los paths. Te baja al detalle abajo.

Solución concreta de paths
Lo bueno: están en el mismo árbol. Eso permite paths relativos sin scripts complejos.

Layout actual (lo que vi)

c:/Users/Martin/Documents/virtual-teams/
├── virtual-teams-setup/                      ← FUENTE ÚNICA
│   └── 00-agent-setup/...
├── memory-service/
│   ├── memory-service-project/
│   │   └── 00-agent-setup/...                ← copia manual hoy (drift)
│   ├── memory-service-backend/
│   └── .vtt/
│       ├── worktrees/
│       ├── workspaces/
│       └── manifests/
├── designmine/                               ← futuro proyecto
└── ...
Decisión clave de paths
Hay 3 formas de que un proyecto referencie la normativa. Las tres funcionan con tu setup actual (mismo árbol).

Opción 1 — Path relativo desde el proyecto

# Desde memory-service-project/scripts/gen_mensaje.py
NORMATIVA_PATH = "../../../virtual-teams-setup/00-agent-setup"
Pro: ya funciona sin nada nuevo. Contra: cada script hardcodea el path. Si cambias estructura → rompe todo.

Opción 2 — Variable de entorno + .env por proyecto

# memory-service-project/.env
VTT_NORMATIVA_PATH=/c/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-agent-setup

# Cualquier script
import os
NORMATIVA = os.environ["VTT_NORMATIVA_PATH"]
Pro: una variable controla todo. Contra: cada agente carga .env al arrancar, hay que mantener sincronizado entre máquinas.

Opción 3 — Symlink dentro del proyecto

# Una sola vez
cd memory-service-project
ln -s ../../virtual-teams-setup/00-agent-setup/07.Normativa .vtt-normativa

# Cualquier agente lee
cat .vtt-normativa/01.Protocols/VTT.PROTOCOL-ASG-001*.md
Pro: transparente. Los scripts no saben que es un symlink. Contra: Windows requiere admin o Developer Mode.

Mi recomendación — Combinación Opción 2 + Opción 3 fallback

# En memory-service-project/.env (versionado en git):
VTT_NORMATIVA=../../virtual-teams-setup/00-agent-setup/07.Normativa

# Si Windows permite symlinks, crear adicionalmente:
memory-service-project/.vtt-normativa → symlink al path

# Si NO, los scripts caen al env var
Funciona en cualquier máquina, cualquier OS. Cero scripts de sync. Si VTT-setup cambia, los proyectos lo ven al instante sin copy/paste.

Pero hay un problema con "ver al instante"
Si VTT-setup cambia mientras un agente está trabajando, le puede romper la sesión.

Para eso necesitamos versionado (el Paso 2 que te propuse antes).


virtual-teams-setup/
├── 00-agent-setup/              ← editing (puede cambiar cualquier día)
└── releases/
    ├── v1.2.0/                  ← snapshot estable
    └── CURRENT.txt              ← v1.2.0
Y el proyecto puede pinearse a una versión:


# memory-service-project/.env
VTT_NORMATIVA_VERSION=v1.2.0
VTT_NORMATIVA=../../virtual-teams-setup/releases/v1.2.0
O usar CURRENT (siempre la última estable):


VTT_NORMATIVA=../../virtual-teams-setup/00-agent-setup  # bleeding edge
# o
VTT_NORMATIVA=../../virtual-teams-setup/releases/v1.2.0  # pinned
Lo que propongo construir ahora (este chat)
Documento 1 — GOBIERNO_VTT_SETUP.md
Define:

Quién edita qué carpeta (CODEOWNERS)
Cómo se levanta ticket de mejora desde un proyecto
Política de PRs
Roles del PM editorial (que mencionas crear)
Política de versionado (semver — major / minor / patch)
Documento 2 — PROCESO_ACTUALIZACION_NORMATIVA.md
El flujo completo:


1. Detección de necesidad (agente en proyecto X o PM)
   ↓
2. Ticket de mejora en VTT (proyecto VTT-setup)
   ↓
3. PM editorial recibe + clasifica (major/minor/patch)
   ↓
4. Asigna a un agente que edite en VTT-setup
   ↓
5. PR con CODEOWNERS approval
   ↓
6. Merge a main de VTT-setup
   ↓
7. Si es major/minor → release nuevo (releases/vX.Y.0/)
   ↓
8. Notificar a TLs de proyectos consumidores
   ↓
9. Cada TL decide cuándo pinear su proyecto a la nueva versión
   ↓
10. TL ejecuta sync (actualiza .env del proyecto o regenera symlink)
Documento 3 — IMPROVE-006_actualizacion_en_cascada_normativa.md
La versión enterprise futura:

Pool de notificaciones cuando VTT-setup publica versión
Validador automático (proyecto incompatible con versión X)
Hook Manager que valida al arrancar agente
Dashboard de "qué proyecto está en qué versión"
Scripts mínimos (para ejecutar de inicio)
Script	Path	Función
release_normativa.py	virtual-teams-setup/scripts/	PM congela versión actual en releases/vX.Y.Z/
sync_project.py	virtual-teams-setup/scripts/	TL del proyecto actualiza su .env a nueva versión
verify_version.py	virtual-teams-setup/scripts/	Cualquier agente verifica versión actual del proyecto
CODEOWNERS propuesto

# virtual-teams-setup/CODEOWNERS

# Operativos por rol → Equipo Perfiles
/00-agent-setup/01.operativos/     @equipo-perfiles @martin

# Procesos operativos / worktrees → Equipo Worktrees
/00-agent-setup/04.Process/        @equipo-worktrees @martin
/00-agent-setup/06.Documentos_soporte/GUIA_WORKTREES_*.md   @equipo-worktrees @martin
/00-agent-setup/06.Documentos_soporte/PROCESO_*.md          @equipo-worktrees @martin

# Normativa (Protocols/Workflows/Rules) → TL + PM
/00-agent-setup/07.Normativa/      @tl @martin

# Templates / Skills → cualquiera con review del PM
/00-agent-setup/05.Templates/      @martin
/00-agent-setup/06.Skills/         @martin

# Resto → PM
*                                  @martin
Antes de generar los documentos — 5 preguntas decisorias
1. ¿Creas el PM editorial dedicado en VTT-setup o tú mantienes ese rol?
Si lo creas, podemos diseñar su OPERATIVO específico. Si no, tú asumes y documentamos el rol como "PM de Normativa" tuyo.

2. ¿Qué versión es la actual?
Después de todo lo que hicimos hoy (PROTOCOL-ASG-001 v1.2.0, Rules v47, etc.), ¿esto es v1.0.0 del release de normativa (primera versión "publicada") o seguimos en draft?

Mi recomendación: declarar v1.0.0 hoy como baseline. Todo lo que sigue será v1.1, v2.0, etc.

3. ¿Cómo se levanta ticket de mejora?
Tres opciones:

A. Tarea VTT en el proyecto VTT-setup con label improvement_request
B. GitHub Issue en el repo virtual-teams-setup
C. Comment en una tarea del proyecto que detectó la necesidad → PM lo escala
Mi recomendación: A (tarea VTT en proyecto VTT-setup). Mantiene todo en un solo sistema.

4. ¿Cuándo se publica una versión nueva?
Major (X.0.0) — cuando cambia estructura/contratos (ej. modelo de niveles)
Minor (1.X.0) — cuando agregamos features (ej. Worktrees por rol)
Patch (1.2.X) — fixes de typos, aclaraciones
Decisión tuya — confirmas o ajustamos.

5. ¿Qué tan urgente?
Si tienes 3 equipos activos editando hoy, esto es bloqueante. Te recomiendo:

Hoy/mañana:

Documentos 1 + 2 (gobierno + proceso actualización)
CODEOWNERS file
Declarar v1.0.0 baseline
Esta semana:

Scripts mínimos
Migrar Memory Service a usar VTT_NORMATIVA env var
Próxima semana:

IMPROVE-006 documentado
Onboarding de los otros equipos al proceso nuevo
¿Procedo?
Si confirmas las 5 preguntas, genero todo de una pasada:

GOBIERNO_VTT_SETUP.md
PROCESO_ACTUALIZACION_NORMATIVA.md
CODEOWNERS
releases/v1.0.0/ con snapshot inicial
scripts/release_normativa.py + sync_project.py + verify_version.py
IMPROVE-006_actualizacion_en_cascada_normativa.md
¿Cuál es tu respuesta a las 5?

Antes de generar los documentos, ¿puedes revisar dentro de las features del modelo dinámico a qué se refiere o cómo se maneja la parte de documentos? Porque hay un apartado que es específicamente para la documentación.
Reviso el modelo dinámico V4 para identificar el apartado de documentos antes de continuar.

Bash Find dynamic model docs
IN
find "c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup" -name "*MODELO_DINAMICO*" -o -name "*FEATURE*" 2>/dev/null | head -10

OUT
c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-agent-setup/03.standard/11_GUIA_AGENTES_MODELO_DINAMICO_V4.md
c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-agent-setup/06.Documentos_soporte/CIERRE_PM_HANDOFF_PJM_MODELO_DINAMICO_V4.2.md
c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/archive/memory-service-project/00-agent-setup/03.standard/11_GUIA_AGENTES_MODELO_DINAMICO_V4.md
c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/archive/memory-service-project/00-agent-setup/06.Documentos_soporte/CIERRE_PM_HANDOFF_PJM_MODELO_DINAMICO_V4.2.md
c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/archive/memory-service-project/Release2.0/Memory/BRIEF_PM_VTT_MODELO_DINAMICO_V3.md
c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/archive/Release2.0/Memory/BRIEF_PM_VTT_MODELO_DINAMICO_V3.md
c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/Docs/01-documentacion/FEATURE_FIRMAS.md
c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/Docs/01-documentacion/FEATURE_PHASE_TRANSITIONS.md
c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/Docs/01-documentacion/FEATURE_TRACKABLE_ITEMS.md
c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/Docs/01-documentacion/MANUAL_FEATURES_VTT_V4.md
Bash Inspect Docs folder + find document features
IN
ls "c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/Docs/01-documentacion/" 2>&1; echo "---grep docs feature---"; ls "c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/Docs/" 2>&1; echo "---busqueda DOCUMENT---"; find "c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup" -maxdepth 4 -name "*DOCUMENT*" -type f 2>/dev/null | head -10

OUT
DECISIONES_CRITERIA_SYSTEM_Q1-Q7.md
FEATURE_FIRMAS.md
FEATURE_PHASE_TRANSITIONS.md
FEATURE_TRACKABLE_ITEMS.md
LIVING_DOCUMENTS_MEMORY_SERVICE.md
MANUAL_FEATURES_VTT_V4.md
MANUAL_TRACKABLE_ITEMS_VTT.md
PROPUESTA_CRITERIA_TRAZABILIDAD_VTT.md
REFERENCE_ProjectPlan_Deliveries_Sprints.md
REFERENCE_Setup_Fase_Sprint_Delivery_Dependencies.md
SOP-EST-01_technical_estimates.md
SOP-RET-01_retrospective_analysis.md
SOP-TRK-01_trackable_items_workflow.md
SOP-TRK-02_dynamic_item_creation.md
SOP-VEL-01_velocity_methodology.md
SOP_GENERACION_HO_PJM.md
SOP_GENERACION_SPRINT_DOCS.md
TASK_CRITERIA_MS-024_ACCEPTANCE_CRITERIA.md
ejemplos
---grep docs feature---
01-documentacion
agent-kits
analysis
discovery
planning
soporte
tl-docs
---busqueda DOCUMENT---
c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-agent-setup/04.Process/configuracion_deliverables/DICCIONARIO_FASE_04_07_TECHNICAL_DOCUMENTATION.md
c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-agent-setup/06.Documentos_soporte/LIVING_DOCUMENTS_MEMORY_SERVICE.md
c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/00-agent-setup/07.Normativa/INVENTARIO_DOCUMENTOS_VTT.md
c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/archive/INDICE_MAESTRO_DOCUMENTOS.md
c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/archive/memory-service-project/INDICE_MAESTRO_DOCUMENTOS.md
c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/Docs/01-documentacion/LIVING_DOCUMENTS_MEMORY_SERVICE.md
c:/Users/Martin/Documents/virtual-teams/virtual-teams-setup/Docs/tl-docs/07_LIVING_DOCUMENTS_MEMORY_SERVICE.md
Grep "^##|^# |document|Document|DOCUMENT|ProjectDocument|DocumentImpact|document_impact" (in c:\Users\Martin\Documents\virtual-teams\virtual-teams-setup\Docs\01-documentacion\MANUAL_FEATURES_VTT_V4.md)
81 lines of output
Read c:\Users\Martin\Documents\virtual-teams\virtual-teams-setup\Docs\01-documentacion\MANUAL_FEATURES_VTT_V4.md (lines 206-325)
Hay también referencia a ProjectDocument que es donde subiste VTT_PLATFORM_GAPS. Reviso si hay endpoints documentados:

Grep "ProjectDocument|/api/projects/.*/documents|documentSource|DocumentSource" (in c:\Users\Martin\Documents\virtual-teams\virtual-teams-setup\Docs\01-documentacion)
1 line of output
Grep "document.*[Ss]ource|/api/projects/.*/documents|projectDocument|ProjectDocument" (in c:\Users\Martin\Documents\virtual-teams\virtual-teams-setup)
11 lines of output
Grep "ProjectDocument|documentType|/projects/.+/documents" (in c:\Users\Martin\Documents\virtual-teams\virtual-teams-setup\Reportes\conversaciones\2026-04-22_Product-Manager-Prt02\conversacion.md)
1 line of output
Grep "documentType|ProjectDocument|/projects/.+/documents" (in c:\Users\Martin\Documents\virtual-teams\virtual-teams-setup\Reportes\conversaciones\2026-04-22_Product-Manager-Prt02\conversacion.md)
1 line of output
Read c:\Users\Martin\Documents\virtual-teams\virtual-teams-setup\Reportes\conversaciones\2026-04-22_Product-Manager-Prt02\conversacion.md (lines 14601-14700)
Tengo el panorama. Te bajo lo que encontré:

Features de Documentación en el Modelo Dinámico V4
1. ProjectDocument (lo que ya usaste para VTT_PLATFORM_GAPS)
Endpoint: POST /api/projects/:projectId/documents

Campos clave:

title, description, documentType (enum: reference | methodology | architecture | attachment)
isLivingDocument (bool) — aunque la guía dice que se ignora en POST, requiere PATCH (que devolvió 404 — feature incompleta)
changeControl (fixed / otros)
uploadedById
2. Document Sources (vinculación con fuentes)
Endpoint: POST /api/project-documents/:id/sources

Permite registrar las fuentes que alimentan un documento living (qué archivos de código o procesos lo afectan).

3. Document Impacts (feature MANUAL_FEATURES_VTT_V4 §5)
Endpoint: POST /api/tasks/:id/document-impacts

Cuando una tarea afecta un documento:

documentSourceId (REQUERIDO — del catálogo de sources)
impactType (added / modified / removed / referenced)
description
⚠️ Gotcha conocido (GAP-VTT-04 / DEBT-INFRA-VTT-01): requiere documentSourceId que el DO no puede obtener fácilmente. Workaround actual: declarar via devlog observation.

4. Living Documents (MANUAL_FEATURES_VTT_V4 §7)
Documentos que se actualizan automáticamente desde el código:

Tipo	Fuente	Genera
Schema	prisma/schema.prisma	Documentación de modelos
API	swagger/openapi.json	Documentación de endpoints
Los LD-XX de Memory Service (LD-01 a LD-15) son manuales (manual_agent) — no se actualizan solos, pero están registrados como living para forzar declaración de impactos al cierre.

5. changeControl y isLivingDocument
changeControl: "fixed" — el documento NO cambia salvo decisión explícita
changeControl: "living" — sujeto a updates por código/agentes
isLivingDocument: true — habilita auto-tracking de cambios
⚠️ Solo se setean via UI o via PATCH /api/project-documents/:id (que no está expuesto en algunos proyectos).

Cómo conecta con tu problema de "fuente de verdad y sincronización"
Esto es exactamente el modelo que VTT ya tiene diseñado para resolver tu problema.

Aplicado a tu caso

ProjectDocument (en VTT proyecto "virtual-teams-setup")
   ├── PROTOCOL-ASG-001         documentType: methodology, isLiving: true
   ├── rules_catalog.json       documentType: reference, isLiving: true
   ├── GUIA_WORKTREES_v2.1      documentType: methodology, isLiving: true
   └── ...

Document Sources de cada doc:
   PROTOCOL-ASG-001 → sources:
     - virtual-teams-setup/00-agent-setup/07.Normativa/01.Protocols/VTT.PROTOCOL-ASG-001*.md
     - memory-service-project/.../PROCESO_CIERRE_TAREA_v2.md (lección que originó cambios)

Document Impacts (en cada tarea):
   Tarea "MS-501: actualizar BE para usar worktree por rol"
     → Document Impact: PROTOCOL-ASG-001 v1.1 → v1.2 (modified)
     → Document Impact: rules_catalog.json (modified — RULE-AGENT-001 v2.0)
Cuando cambias VTT-setup, el flujo es

1. PM edita PROTOCOL-ASG-001 (en VTT-setup)
2. PM registra Document Impact en la tarea VTT que originó el cambio
3. VTT notifica a TODOS los proyectos que consumen ese ProjectDocument
4. TLs de proyectos reciben notificación: "PROTOCOL-ASG-001 cambió a v1.2 — revisa si te afecta"
5. Cada TL decide si actualiza su versión consumida
Mi propuesta tras revisar las features
No necesitamos inventar un sistema de propagación nuevo. Ya existe en VTT como ProjectDocument + Document Sources + Document Impacts. Lo que falta es usarlo correctamente.

Plan ajustado
Cada documento normativo de VTT-setup se registra como ProjectDocument en VTT (proyecto virtual-teams-setup)
Cada ProjectDocument tiene Sources que apuntan al archivo .md real en disco
Los proyectos consumidores se vinculan al ProjectDocument (no a copias locales)
Cuando cambia el archivo fuente, el TL de VTT-setup registra Document Impact + bump de versión
Los TLs de proyectos reciben la notificación y actualizan su pin de versión
Lo que tengo que verificar antes de proponer la solución completa
¿La feature ProjectDocument está completamente implementada? Vimos que PATCH para isLivingDocument daba 404 → puede haber gaps backend.

¿Existe endpoint de "documentos consumidos por proyecto"? Para que un proyecto B se suscriba a un documento de VTT-setup.

¿Existe el catálogo de DocumentSource accesible para todos los roles? El gap GAP-VTT-04 dice que el DO no puede acceder.

¿Hay notificación cuando cambia un ProjectDocument? O hay que pollear.

Antes de seguir
¿Quieres que:

Opción A — Pruebe los endpoints de ProjectDocument + Document Sources contra VTT real para mapear qué funciona y qué no, antes de diseñar el sistema de propagación?

Opción B — Diseñe el sistema asumiendo que las features funcionan (siguiendo lo documentado en MANUAL_FEATURES_VTT_V4) y dejamos los gaps como tech debts a resolver?

Opción C — Me bases en IMPROVE-003 (Platform Gaps) y reportes adicionales sobre ProjectDocument que ya existen?

Mi recomendación: Opción A, 30 min de pruebas para validar antes de diseñar. Si la feature está rota, lo descubrimos antes de basar todo el gobierno en algo que no funciona.

¿Cuál?

si ya estan implementados  mira estas guias:
@C:\Users\Martin\Documents\virtual-teams\virtual-teams-setup\Docs\01-documentacion\features mod dinamico\FEATURE_PROJECT_FOLDERS.md
@C:\Users\Martin\Documents\virtual-teams\virtual-teams-setup\Docs\01-documentacion\features mod dinamico\FEATURE_PROJECT_DOCUMENTS.md.

Como podemos sguir
Reviso los dos documentos antes de proponer plan.

Read c:\Users\Martin\Documents\virtual-teams\virtual-teams-setup\Docs\01-documentacion\features mod dinamico\FEATURE_PROJECT_DOCUMENTS.md
Excelente, está mucho más completo de lo que pensaba. Ahora veo Folders:

Read c:\Users\Martin\Documents\virtual-teams\virtual-teams-setup\Docs\01-documentacion\features mod dinamico\FEATURE_PROJECT_FOLDERS.md
Excelente. Esto cambia el panorama completamente. Las features ya están implementadas BE/DB. Te bajo el plan basado en lo que descubrí.

Lo que tenemos disponible (ya implementado)
Project Folders
Jerarquía completa de carpetas por proyecto
Estructura default software que se auto-crea
CRUD completo, mover, renombrar, search
Project Documents — resuelve directamente tu problema
5 tipos:

Tipo	Caso de uso para fuente de verdad
static	SOPs estables que cambian poco
versioned	Tu caso ideal — historial completo + restore version
living	Para docs auto-generados (no aplica a normativa)
template	BRIEFs/ASSIGNMENTs templates
attachment	PDFs, imágenes
Endpoint clave para versionado

PATCH /api/documents/:id      → crea nueva versión automáticamente
GET   /api/documents/:id/versions → historial completo
POST  /api/documents/:id/restore → rollback a versión anterior
GET   /api/documents/:id/diff?v1=2&v2=3 → diff entre versiones
Vínculos cross-entidad

POST /api/tasks/:taskId/documents     → documento ref de tarea
POST /api/sprints/:sprintId/documents → documento del sprint
POST /api/releases/:releaseId/documents → documento del release
Cómo resuelve tu problema de fuente de verdad
Modelo propuesto (usando feature existente)

1. Crear proyecto VTT en VTT-API: "virtual-teams-setup"

2. Crear estructura de carpetas:
   /Normativa/
     /Protocols/
     /Workflows/
     /Skills/
     /Scripts/
     /Templates/
     /Rules/

3. Cada documento normativo se sube como ProjectDocument tipo `versioned`:
   - PROTOCOL-ASG-001 → documentType=versioned
   - rules_catalog.json → documentType=versioned
   - GUIA_WORKTREES → documentType=versioned

4. Cada cambio = PATCH → genera nueva versión automáticamente
   Sin scripts de release. Sin snapshots manuales. La DB lo hace.

5. Proyectos consumidores vinculan al ProjectDocument:
   POST /api/projects/memory-service/documents/{id}/link
   {
     "sourceDocumentId": "uuid-PROTOCOL-ASG-001",
     "version": 2,
     "linkType": "reference"
   }

   → Memory Service queda pineado a version 2 del PROTOCOL-ASG-001
   → Si VTT-setup sube version 3, Memory Service NO se rompe
   → TL de Memory Service decide cuándo actualizar pin
Comparación con plan anterior (Opción C con scripts release)
Aspecto	Opción C (scripts manuales)	Project Documents (feature existente)
Versionado	Carpetas releases/v1.2.0/	Automático en BD
Snapshots	Script release_normativa.py	PATCH genera version
Rollback	Manual checkout	POST /restore
Diff	git diff	GET /diff?v1=2&v2=3
Búsqueda	grep	GET /search?q=...
Tracking de uso	Manual	tabla task_documents
Auditoría	git log	document_versions con changeNote
Mantenimiento	Hay que mantener scripts	0 — feature core de VTT
Project Documents gana en todo.

Plan ajustado — usar lo que ya existe
Paso 1 — Crear proyecto VTT-setup en VTT

POST /api/projects
{
  "name": "Virtual Teams Setup",
  "code": "VTT-SETUP",
  "type": "infrastructure"
}
Paso 2 — Auto-crear estructura de carpetas (default software) + ajustar
Estructura específica para normativa:


/Normativa/
  /Protocols/
  /Workflows/
  /Skills/
  /Scripts/
  /Templates/
  /Rules/
  /Improvements/
/Procesos/
/Documentos_soporte/
/Standard/
Paso 3 — Migrar normativa actual como ProjectDocuments versionados
Script que recorre virtual-teams-setup/00-agent-setup/07.Normativa/ y por cada .md:

Lee contenido
POST /api/projects/VTT-SETUP/documents con documentType: versioned
Registra mapping file_path → document_id
Output: cada documento normativo ahora vive en VTT con UUID + version 1.

Paso 4 — Definir proceso de actualización

PM detecta cambio necesario
   ↓
Crea tarea en VTT-SETUP (proyecto)
   ↓
Asigna a agente editor (TL o quien corresponda según CODEOWNERS)
   ↓
Agente:
  - Edita archivo .md en virtual-teams-setup/ local
  - PR + merge a main (gobierno editorial - branch protection)
  - PATCH /api/documents/:id con contenido nuevo + changeNote
    → VTT crea version 2 automáticamente
   ↓
Cierra tarea
   ↓
TLs de proyectos consumidores reciben notificación (futuro Hook Manager)
Paso 5 — Vincular Memory Service como primer consumidor

POST /api/projects/memory-service/documents/link
{
  "sourceDocumentId": "uuid-PROTOCOL-ASG-001",
  "version": 2,                          ← pineado
  "linkType": "reference"
}
Cuando TL de Memory Service quiera actualizar:


PATCH /api/projects/memory-service/documents/{linkId}
{ "version": 3 }
Paso 6 — IMPROVE-006 — Hook Manager para notificaciones
Cuando VTT-SETUP publica versión nueva, hook notifica a TLs de proyectos consumidores. Diferido.

Validación previa necesaria
Te propongo 30 min de pruebas contra VTT antes de comprometernos con este plan:

Test	Qué validamos
Crear proyecto VTT-SETUP	¿Project creation funciona?
Crear folder Normativa	¿Folder API funciona?
Crear ProjectDocument versionado	¿documentType=versioned se respeta?
PATCH para generar v2	¿Auto-versionado funciona?
GET /versions	¿Historial accesible?
POST /restore	¿Rollback funciona?
Vincular document a tarea/sprint de otro proyecto	¿Cross-project link funciona?
Antes de seguir, decide
¿Test primero (30 min) o asumimos que funciona y diseñamos?

Recomendación: testear. La conversación de Product Manager Prt02 ya mostró que algunos endpoints (PATCH living-config) dieron 404.
¿Creamos el proyecto VTT-SETUP en VTT ahora?
Es el primer paso operativo. Necesita autorización tuya.

¿Quién es el editor de VTT-SETUP en VTT?

PM (tú) → tú haces todo
PM editorial dedicado → necesitamos crear el usuario
¿Mantenemos los .md en virtual-teams-setup/ Git como respaldo, o todo migra a VTT?

Recomendación: dual storage. Archivos .md en Git para edición local + ProjectDocuments en VTT para consumo cross-proyecto. PATCH sincroniza ambos.
¿Pruebas con un documento o con todos?

Recomendación: empieza con PROTOCOL-ASG-001 como primer caso. Si funciona bien, escalamos al resto.
¿Cuál es tu llamada en estos 5 puntos?

c:\Users\Martin\Documents\virtual-teams\memory-service\.vtt\worktrees\project-tl\00-agent-setup\06.Documentos_soporte\GUIA_MANIFEST_PARA_AGENTES.md
si, testea priemro para que compruebs que ya funcionan los endpoitns y todas las features
VTT setuo ya existe
c6b513a1-d8ae-4344-b684-96d73721bfbf
eso es lo que te iba a decir, necesitamos subir a git como respaldo

necesitmos hacer pruabs apra crear los folder y subri los versionados

loq eu debmos definir son als relgas de edicion, proque, proque ahrita cualquir agente de cualquier proeycto puede editar. y estamos editando de maenra directa en los archivos de vtt setup y eso no s esta causando discrepancias mira, estoy ttabajando con otro agente. y mira los errores que tenemos
El cambio de mentalidad
Lo que YO interpreté mal (y rompí en SKL-MANIFEST-01 v4.1):

"Mete skl_report_01_full completo en el JSON" → infla cada manifest a ~5K tokens de texto repetido
Lo que TÚ pediste:

El manifest contiene los 2 campos narrativos esenciales del report (lo que se hizo + qué código se tocó) + punteros a devlog/code-logic para lectura on-demand
Resto del report (CAs, devlog, ADRs, etc.) ya vive en sus tablas/campos estructurados del manifest — no se duplica
Campos que debe tener el manifest (corregido)

"delivery": {
  "summary": {
    "what_was_done": "Se regeneró la suite unitaria S06-FIX-A...",  // ~70 palabras max
    "code_touched": [
      { "path": "backend/src/services/__tests__/documentVersion.service.test.ts", "what": "suite principal con 5 describe blocks" },
      { "path": "...", "what": "..." }
    ]
  },
  "context_pointers": {
    "development_log": "knowledge/development-log/2026-05-17_VTT-718_tests-unitarios-s06.md",
    "code_logic": ["knowledge/code-logic/qa/VTT-718-tests-unitarios-s06.LOGIC.md"],
    "report_full": "knowledge/agent-tasks/reports/.../VTT-718_REPORT.md"  // puntero, NO contenido
  },
  // ... resto de campos estructurados (criteria_results, trackable_items, git, etc.) sin cambio
}
Lo que tengo que revertir/corregir
Archivo	Estado actual	Acción
SKL-REPORT-01 v2.0 (vtt-setup)	"Guardar report completo en archivo, postear extracto, manifest lee del archivo"	CORREGIR: el report en archivo sigue existiendo (es el "report completo" navegable por humanos), pero el manifest NO lo embebe. Manifest solo guarda el puntero al archivo.
SKL-MANIFEST-01 v4.1 (worktree TL)	Lee report_path y mete el contenido en skl_report_01_full	CORREGIR: NO leer el contenido. Solo guardar el path en context_pointers.report_full. Extraer del report las 2 secciones narrativas (what_was_done + code_touched) y meterlas en delivery.summary.
GUIA_MANIFEST_PARA_AGENTES v3.1	Schema con skl_report_01_full como string completo	CORREGIR: schema con delivery.summary (estructurado) + delivery.context_pointers (paths). Eliminar skl_report_01_full del schema.
IMPROVE-002 §queries	Algunas asumen leer skl_report_01_full	CORREGIR: las queries de "qué se hizo en S6" se hacen sobre delivery.summary.what_was_done (campo corto, indexable). El report completo solo se lee on-demand.
Cálculo de tu ejemplo
50 manifests × ~200 palabras de summary (what + code) = 10K palabras ≈ 12.5K tokens
Eso cabe en 6% del context window — perfectamente navegable
Vs. la versión rota: 50 × 5000 chars = ~60K tokens solo en reports duplicados → no escala
¿Procedo a corregir los 3 archivos (SKL-REPORT, SKL-MANIFEST, GUIA) con este modelo? Antes de mover un dedo: confirma si la estructura delivery.summary { what_was_done, code_touched } + delivery.context_pointers { development_log, code_logic, report_full } es lo que tienes en mente, o lo afino.

a que te refieres cone sto

Archivo	Estado actual	Acción
SKL-REPORT-01 v2.0 (vtt-setup)	"Guardar report completo en archivo, postear extracto, manifest lee del archivo"	CORREGIR: el report en archivo sigue existiendo (es el "report completo" navegable por humanos), pero el manifest NO lo embebe. Manifest solo guarda el puntero al archivo.

Y esot?


Archivo	Estado actual	Acción
SKL-REPORT-01 v2.0 (vtt-setup)	"Guardar report completo en archivo, postear extracto, manifest lee del archivo"	CORREGIR: el report en archivo sigue existiendo (es el "report completo" navegable por humanos), pero el manifest NO lo embebe. Manifest solo guarda el puntero al archivo.
SKL-MANIFEST-01 v4.1 (worktree TL)	Lee report_path y mete el contenido en skl_report_01_full	CORREGIR: NO leer el contenido. Solo guardar el path en context_pointers.report_full. Extraer del report las 2 secciones narrativas (what_was_done + code_touched) y meterlas en delivery.summary.

ahora ojo proque tu soloe tas trabajando en el worktree de BE y esoe st amal tienes aue dejar los arhcivos en set up vvTT porque asi vamos a perder la trazabildiad

despus sde actualizat en VTT setup actualzias en cascada
Te respondo cada pregunta y aclaro mi error de worktrees.

1. ¿A qué me refiero con "SKL-REPORT-01: el report en archivo sigue existiendo pero el manifest NO lo embebe"?
Hoy (lo que dejé mal en v2.0):

Agente guarda VTT-718_REPORT.md en disco ✓ (correcto, sigue así)
Agente postea extracto en VTT como comment ✓ (correcto, sigue así)
Manifest lee el archivo completo y lo mete en skl_report_01_full ❌ ← esto es la basura
Corrección:

Igual — guardar VTT-718_REPORT.md en disco
Igual — postear extracto en VTT
Manifest NO lee el contenido. Solo guarda context_pointers.report_full: "knowledge/agent-tasks/reports/.../VTT-718_REPORT.md" (un string con la ruta).
Adicionalmente, el manifest extrae 2 secciones del report (lo que se hizo + código tocado) y las mete en delivery.summary — son cortas, navegables.
Resultado: el report sigue siendo navegable por humanos (archivo en disco), pero el JSON no carga 5K chars de texto duplicado.

2. ¿A qué me refiero con "SKL-MANIFEST-01: extraer del report las 2 secciones narrativas"?
El report tiene ~15 secciones (Lo que se hizo, Código, Devlog, Code Logic, CAs, Devlog entries, Findings, ADRs, TIs, Items detectados, Tareas derivadas, Cómo verificar, Notas, Review gate, Commit, PR).

Las 2 narrativas (lo que se hizo + código tocado) → van a delivery.summary del manifest (texto corto, lo que el agente futuro lee de un vistazo)
El resto ya vive estructurado en otros campos del manifest (criteria_results, devlog_summary, trackable_items_actual, git, vtt_attachments, etc.) — no duplicar
El report completo en archivo → puntero en context_pointers.report_full por si alguien quiere leerlo entero
3. Mi error de worktrees — confirmado, sí estoy mal
Tienes razón. Hice esto mal:

Archivo	Dónde lo edité	Dónde DEBÍ editarlo
SKL-REPORT-01_entrega-tarea.md	✓ vtt-setup (correcto)	vtt-setup (fuente)
SKL-MANIFEST-01_generar-manifest.md	❌ worktree project-tl de memory-service	vtt-setup primero, luego cascadear
GUIA_MANIFEST_PARA_AGENTES.md	❌ worktree project-tl de memory-service	vtt-setup primero, luego cascadear
El flujo correcto que rompí:

Editar fuente en virtual-teams-setup (single source of truth)
Cascadear (copiar) a cada proyecto que la consume: memory-service, virtual-teams-tracking, etc.
Lo que hice fue editar la copia local del worktree directamente → se perdería la trazabilidad cuando otro proyecto lo necesite.

Propuesta de fix (espero tu OK antes de tocar)
Paso 1 — Reset: Revertir las ediciones que metí en el worktree de memory-service.

Paso 2 — Editar las 3 fuentes en vtt-setup:

virtual-teams-setup/00-agent-setup/06.Skills/report/SKL-REPORT-01_entrega-tarea.md → ya está en v2.0 pero hay que quitarle el bullet "manifest lee del archivo" y reemplazarlo por "manifest guarda puntero + extrae 2 secciones narrativas"
virtual-teams-setup/00-agent-setup/06.Skills/manifest/SKL-MANIFEST-01_generar-manifest.md → ¿existe en vtt-setup o solo en worktrees?
virtual-teams-setup/Docs/01-documentacion/GUIA_MANIFEST_PARA_AGENTES.md → ya está copiado ahí (lo copié hace un rato), aplicar la corrección
virtual-teams-setup/00-agent-setup/07.Normativa/IMPROVEMENTS/IMPROVE-002_bd_manifiestos_y_tis.md → ajustar §queries que mencionaban skl_report_01_full
Paso 3 — Cascadear desde vtt-setup hacia los proyectos que ya tenían copia local.

Antes de mover un dedo, dos preguntas:

¿Existe SKL-MANIFEST-01_generar-manifest.md en virtual-teams-setup o solo se creó en el worktree? Si no existe en vtt-setup, lo creo ahí primero.
¿La estructura delivery.summary { what_was_done, code_touched } + delivery.context_pointers { development_log, code_logic, report_full } es lo que tienes en mente o la afinamos antes?
no, esto sigue estando mal
2. ¿A qué me refiero con "SKL-MANIFEST-01: extraer del report las 2 secciones narrativas"?
El report tiene ~15 secciones (Lo que se hizo, Código, Devlog, Code Logic, CAs, Devlog entries, Findings, ADRs, TIs, Items detectados, Tareas derivadas, Cómo verificar, Notas, Review gate, Commit, PR).

Las 2 narrativas (lo que se hizo + código tocado) → van a delivery.summary del manifest (texto corto, lo que el agente futuro lee de un vistazo)
El resto ya vive estructurado en otros campos del manifest (criteria_results, devlog_summary, trackable_items_actual, git, vtt_attachments, etc.) — no duplicar
El report completo en archivo → puntero en context_pointers.report_full por si alguien quiere leerlo entero

cad campo del rporte debe esta en el manifiesto.
si tu colocas los dos campos en uno soloe stara contaminando la memoria

Al final al tenr todo en campo separados, yo peudo filtrar por archivos tocados. y ver que tareas son las que lo tocaron, ahcer un query y decirle para este mmodulo se hizo esto en estas tareas...  así el agente sabra que se hizo y hacer correcciones o modificaciones

Por eso es que cada cmapo lo necesitamos pro separado en el manifiesto

No reviertas anda en work tree, haces las modificaciones den setup y copais el archivo pum ya rapido
2 VTT setup ya tiene todos los archivos solod ebes de generar ahi las modificaciones y/o archivos neuvos.

por ultimo, la guía de manifiesto no debe ria de tenr etodo el cpodigo endebido.. proque eso lo ahce muy grande mas ebien deberia de describri las secciones o como genrarlo.. reglas, condiciojes, notas, CAs etc
Entendido, ahora sí. Corrijo:

Lo que entendí ahora
Cada sección del report = su propio campo en el manifest. NO consolidar en delivery.summary. Las 15 secciones se vuelven 15 campos estructurados → un agente futuro puede hacer queries tipo "todas las tareas que tocaron documentVersion.service.ts" y obtener lista exacta.

Ejemplo mental:


"delivery": {
  "what_was_done": "Se regeneró la suite unitaria S06-FIX-A...",
  "code_touched": [{ "path": "...", "what": "..." }],
  "development_log_path": "knowledge/development-log/...",
  "code_logic_paths": ["knowledge/code-logic/..."],
  "findings": "...",
  "adrs_taken": "...",
  "items_detected_for_tl": [...],
  "derived_tasks": "...",
  "how_to_verify": [...],
  "notes": "...",
  "review_gate": {...},
  "commit": {...},
  "pr_url": "...",
  // criteria_results, devlog, trackable_items, etc. ya estructurados como hoy
}
Sin consolidar narrativas en bloque único. Sin skl_report_01_full.

Errores que reconozco
No reviertas worktrees — solo edito en vtt-setup y copio. Entendido.
vtt-setup ya tiene todos los archivos — confirmo antes de tocar.
La guía no debe tener código embebido — debe describir secciones, reglas, condiciones, CAs, notas. Que sea documentación, no template de copy-paste con Python.
Antes de actuar — 3 preguntas
¿Existe ya SKL-MANIFEST-01_generar-manifest.md en vtt-setup? Verifico.
Para la GUIA sin código embebido: ¿la quieres como spec puro (qué secciones, qué reglas, qué validaciones, condiciones por categoría) y el código va aparte en el .py que el script ejecuta? ¿O describimos las secciones y dejamos referencia "ver script gen_manifest.py"?
El mapeo report → manifest: ¿lo construyo yo (1:1 cada sección del report a un campo) y te lo presento como tabla para validar antes de tocar archivos? Así evitamos meter campos que después tengas que reorganizar.
Bash Verificar archivos existentes en vtt-setup
IN
ls "C:\Users\Martin\Documents\virtual-teams\virtual-teams-setup\00-agent-setup\06.Skills\manifest\" 2>&1 && echo "---" && ls "C:\Users\Martin\Documents\virtual-teams\virtual-teams-setup\00-agent-setup\06.Skills\" 2>&1 && echo "---DOCS---" && ls "C:\Users\Martin\Documents\virtual-teams\virtual-teams-setup\Docs\01-documentacion\" | grep -i manifest

OUT
Exit code 2
/usr/bin/bash: eval: line 1: unexpected EOF while looking for matching `"'
Bash Verificar archivos existentes en vtt-setup
IN
ls 'C:\Users\Martin\Documents\virtual-teams\virtual-teams-setup\00-agent-setup\06.Skills\manifest' 2>&1; echo "---"; ls 'C:\Users\Martin\Documents\virtual-teams\virtual-teams-setup\00-agent-setup\06.Skills' 2>&1

OUT
ls: cannot access 'C:\Users\Martin\Documents\virtual-teams\virtual-teams-setup\00-agent-setup\06.Skills\manifest': No such file or directory
---
CATALOGO_SKILLS_MEMORY_SERVICE.md
auth
file-structure
git-ops
report
vtt-attach
vtt-task
Globpattern: "C:\Users\Martin\Documents\virtual-teams\virtual-teams-setup\**\SKL-MANIFEST*.md"
No files found
Globpattern: "C:\Users\Martin\Documents\virtual-teams\virtual-teams-setup\**\GUIA_MANIFEST*.md"
Found 2 files
Encontré inconsistencias en vtt-setup que necesito que confirmes antes de tocar nada:

Archivo	Estado en vtt-setup
SKL-MANIFEST-01_generar-manifest.md	NO EXISTE — no hay carpeta 06.Skills/manifest/ ni el archivo
GUIA_MANIFEST_PARA_AGENTES.md	EXISTE DUPLICADO en 2 lugares: 06.Documentos_soporte/ y Docs/01-documentacion/ (este último lo copié yo hace rato)
Decisiones que necesito de ti:

SKL-MANIFEST-01 en vtt-setup: ¿lo creo en 06.Skills/manifest/ (creando la carpeta)? La fuente única tiene que vivir ahí.
GUIA_MANIFEST duplicada: ¿cuál es la fuente oficial — 06.Documentos_soporte/ o Docs/01-documentacion/? Hay que borrar la otra (yo causé el duplicado).
Mapeo report → manifest: ¿armo la tabla 1:1 primero y me das visto bueno antes de tocar archivos?

mno me digas como corregirlo, queiro que analiss los errores proque aqui vamos acontinaur con la aprte del setup y definir como se hara la edicion
Te bajo el análisis de los errores observados en esa conversación. Sin proponer fixes, solo el patrón de fallas para que diseñemos las reglas de edición.

Errores reales que detectaste en esa sesión
Error 1 — Mala interpretación de un requisito → cambio destructivo
Lo que pasó:

Tú pediste: "el manifest debe tener los datos del report en campos estructurados separados"
El agente entendió: "mete el report completo como un string en skl_report_01_full"
Resultado: cada manifest infla a ~5K tokens de texto duplicado
Causa raíz:

No hubo validación del requisito antes de codificar
El agente asumió en lugar de preguntar
No hay un schema formal del manifest que el agente pueda contrastar con su interpretación
Error 2 — Edición en el lugar incorrecto (worktree en vez de fuente)
Lo que pasó:

El agente editó SKL-MANIFEST-01 y GUIA_MANIFEST_PARA_AGENTES directamente en memory-service/.vtt/worktrees/project-tl/
La fuente está en virtual-teams-setup/
Si otro proyecto consume esos docs, no se entera del cambio → drift
Causa raíz:

No hay regla técnica que impida editar en worktree de consumidor
El agente no tenía claro cuál era la fuente de verdad
No hay validación pre-edición
Error 3 — Duplicación silenciosa en la fuente
Lo que pasó:

GUIA_MANIFEST_PARA_AGENTES.md existe en dos ubicaciones dentro de virtual-teams-setup:
00-agent-setup/06.Documentos_soporte/
Docs/01-documentacion/ (creado por el agente en sesión anterior sin avisar)
Ahora hay dos "fuentes oficiales" y nadie sabe cuál es la buena
Causa raíz:

El agente copió un archivo a otra ubicación sin documentar por qué
No hay un único índice canónico que diga "este path es el oficial"
No hay validación de unicidad antes de crear archivos
Error 4 — Archivo crítico nunca tuvo fuente en VTT-setup
Lo que pasó:

SKL-MANIFEST-01 no existe en virtual-teams-setup/
Sí existe en memory-service-project/00-agent-setup/06.Skills/manifest/
Es decir: la "copia" del consumidor es realmente la única versión
Causa raíz:

Cuando se creó (en sesiones anteriores), nadie validó que naciera en VTT-setup primero
El catálogo INVENTARIO_DOCUMENTOS_VTT.md lo lista pero apunta a memory-service-project
No hay regla que diga "todo SKL debe vivir en VTT-setup como source"
Error 5 — Cambios en cascada sin coordinación
Lo que pasó:

El agente identifica que tiene que tocar 4 archivos:
SKL-REPORT-01 (vtt-setup)
SKL-MANIFEST-01 (no existe en vtt-setup)
GUIA_MANIFEST_PARA_AGENTES (duplicada)
IMPROVE-002 (vtt-setup)
Sin proceso definido, propone "edito y copio rápido"
Esto es exactamente el patrón que causa drift
Causa raíz:

No hay protocolo de "edición + propagación" definido
No hay registro de qué proyectos consumen qué documento
No se notifica a TLs de consumidores cuando algo cambia
Error 6 — Documentos operativos con código embebido
Lo que pasó:

GUIA_MANIFEST_PARA_AGENTES.md (y SKL-MANIFEST-01) tienen snippets Python completos embebidos
La guía mezcla 2 roles: documentación (qué hace) + implementación (cómo)
Resultado: archivos enormes, difíciles de mantener, se actualizan a medias
Causa raíz:

No hay separación entre "spec" (qué + por qué) y "implementación" (script)
Sin separación, cada cambio en el código exige editar la doc; cada cambio en la doc se queda desincronizado del código
Error 7 — Schema del manifest no es contractual
Lo que pasó:

Cada agente que toca el manifest interpreta los campos a su manera
Tú tienes una visión clara (campos atómicos para queries) pero esa visión no está formalizada como JSON Schema
Resultado: SKL-MANIFEST-01 v4.1 introduce skl_report_01_full rompiendo el modelo, sin que nada lo bloquee
Causa raíz:

El schema del manifest está descrito en prosa dentro de la GUIA, no como JSON Schema validable
No hay validador automático que rechace manifests con campos inventados
No hay versionado del schema mismo
Error 8 — Decisión de diseño tomada por el agente sin escalación
Lo que pasó:

El agente decidió consolidar summary { what_was_done, code_touched } + context_pointers { paths }
Esa estructura es invención del agente, no decisión tuya
Tú la rechazaste explícitamente — pero el agente ya había empezado a planear los cambios
Causa raíz:

No hay ritual de "validación de propuesta antes de codificar" en cambios estructurales
El agente confunde "proponer solución" con "asumir aprobación"
Patrones que se repiten
Si abstraigo los 8 errores:

Patrón	Frecuencia	Severidad
Asunción en lugar de pregunta	3 veces (errores 1, 8, parcialmente 7)	Alta — produce trabajo desechable
Edición fuera de la fuente	2 veces (errores 2, 4)	Crítica — rompe trazabilidad
Duplicación sin notificar	2 veces (errores 3, 4)	Alta — fuentes ambiguas
Sin validación pre-acción	4 veces (errores 1, 2, 5, 8)	Crítica — sin guardrails
Mezcla de niveles (spec + script + doc)	1 vez (error 6)	Media — mantenibilidad
Sin contratos formales (schema validable)	1 vez (error 7)	Crítica — todo se filtra
Causas raíz consolidadas
A. No hay regla técnica que diga dónde editar qué
El agente sabe que VTT-setup es "fuente de verdad" porque se lo dijiste, pero no hay nada que impida que edite en otro lado. Necesitamos un mecanismo (validación previa, lint, hook) que rechace ediciones en ubicación incorrecta.

B. No hay índice canónico de "dónde vive cada archivo"
El INVENTARIO_DOCUMENTOS_VTT.md lista archivos pero no marca cuál es la fuente oficial y cuáles son copias derivadas. Sin esta distinción explícita, cualquier copia se siente "oficial".

C. No hay schema contractual del manifest (ni de otros docs estructurados)
El manifest se describe en prosa. Un JSON Schema validable bloquearía agentes que inventan campos. Lo mismo aplicaría a rules_catalog.json, capabilities_catalog.json, etc.

D. No hay separación entre "spec" e "implementación"
Documentos como GUIA_MANIFEST_PARA_AGENTES mezclan:

Spec del manifest (qué secciones, qué reglas)
Implementación (script Python que genera el manifest)
Cualquier cambio en el script requiere editar la guía. Cualquier cambio en la spec puede dejar el script desactualizado.

E. No hay ritual de validación antes de cambios estructurales
El agente puede:

Modificar schemas
Crear archivos nuevos en ubicaciones nuevas
Decidir consolidaciones/separaciones de campos
…sin pedir aprobación. Necesitamos diferenciar cambios "menores" (typo, ejemplo) de "estructurales" (campo nuevo, archivo nuevo, ubicación nueva).

F. No hay registro de "quién consume qué"
Cuando se modifica SKL-MANIFEST-01, nadie sabe automáticamente que memory-service-project y designmine lo consumen. La cascada de actualización es manual y por memoria del PM.

G. No hay diferenciación entre tipos de cambio
Los 4 errores estructurales (1, 4, 5, 8) habrían sido evitables si distinguiéramos:

Cambio editorial (typo, ejemplo, aclaración) — agente puede aplicar directo
Cambio funcional (nuevo paso, regla nueva) — requiere review TL
Cambio estructural (campo nuevo en schema, ubicación nueva) — requiere aprobación PM
Cambio que rompe consumidores (rename, deprecación) — requiere migración planificada
Preguntas que sugieren las reglas de edición a definir
Las decisiones que necesitarías tomar (no las contesto, las dejo planteadas):

¿Cómo se garantiza técnicamente que un agente solo pueda editar en VTT-setup?

Permisos de filesystem por rol
Pre-commit hook que rechace edición fuera de su scope
Worktree del agente bloquea escritura sobre paths fuera de su rol
O simplemente "regla + auditoría reactiva"
¿Cuál es la definición operativa de "fuente de verdad" por archivo?

Path canónico explícito en el INVENTARIO
Header del archivo dice "FUENTE: virtual-teams-setup/... — copias en proyectos X, Y, Z"
Tag en frontmatter del .md (source: canonical | derived)
¿Quién aprueba cada tipo de cambio?

Cambio editorial → agente propone, TL aprueba
Cambio funcional → TL propone, PM aprueba
Cambio estructural → PM propone, va a discusión
Cambio que rompe consumidores → PM + TLs de cada proyecto consumidor
¿Cómo se notifica el cambio a los consumidores?

Manual (PM avisa)
Tarea VTT automática al editar
Hook que detecta git push a virtual-teams-setup y crea tareas
¿Cada archivo declara explícitamente quién es su "dueño editorial"?

SKL-MANIFEST → dueño: TL Memory Service (porque él lo creó)
O todos los SKL → dueño: PM/Editor Normativa
Esta decisión define quién recibe los tickets de cambio
¿Cuál es el flujo cuando un agente detecta necesidad de cambio?

Crea ticket en VTT (proyecto VTT-setup)
Para a esperar aprobación
NO toca nada hasta tener OK
Cuando tiene OK, edita SOLO en VTT-setup, no en su worktree
¿Cómo separamos spec de implementación?

Spec en 07.Normativa/ (qué + por qué + reglas)
Implementación en 04.Scripts/ o scripts/ del proyecto (cómo en código)
Guía referencia ambos pero no embebe código
¿Cuándo se rompe la regla "no tocar fuera del worktree de su rol"?

Si el agente está editando normativa VTT, su "rol" es editor de VTT-setup, no su rol de proyecto
Necesita un worktree adicional vtt-setup-editor/?
O cambio explícito de contexto: "ahora estoy editando normativa"
¿Qué validación automática agregamos?

JSON Schema validator para manifest, rules_catalog, capabilities_catalog
Lint que detecte ediciones fuera de fuente canónica
CI que valide unicidad de paths declarados como canónicos
¿Cómo trackeamos el drift entre VTT-setup y proyectos consumidores?

Script que compara hashes de archivos
Reporte semanal "estos N archivos divergen entre VTT-setup y memory-service-project"
Trigger de alerta cuando divergencia > umbral
Esos son los 8 errores reales + 7 causas raíz + 10 preguntas. ¿Por dónde quieres empezar a discutir? Mi sugerencia: causa raíz A + B + F son las más críticas — sin resolverlas, los otros 5 errores se van a repetir.

ok enteindo y me aprece excelente analisis como comenzamos
Te propongo arrancar por las 3 causas raíz más críticas (A, B, F). Cada una con una pregunta concreta para tomar decisión.

Orden propuesto

PRIMERO  → B (Índice canónico) — 1 hora — desbloquea las otras
SEGUNDO  → A (Regla de dónde editar) — 2 horas — sin esto los agentes siguen rompiendo
TERCERO  → F (Registro de consumidores) — 3 horas — sin esto la cascada es manual
Las otras 4 causas raíz (C, D, E, G) las atacamos después.

Causa raíz B — Índice canónico
Problema: El INVENTARIO lista archivos pero no marca cuál es la fuente oficial vs copia derivada. Sin esta marca, cualquier copia se siente oficial.

Mi propuesta:

Agregar 3 columnas al INVENTARIO actual:

Path canónico (único)	Tipo	Copias derivadas (donde están permitidas)
virtual-teams-setup/00-agent-setup/06.Skills/manifest/SKL-MANIFEST-01.md	CANONICAL	memory-service-project/00-agent-setup/06.Skills/manifest/SKL-MANIFEST-01.md (consumer copy)
Y un frontmatter mínimo en cada archivo:


---
source: canonical
canonical_path: virtual-teams-setup/00-agent-setup/06.Skills/manifest/SKL-MANIFEST-01.md
---
o en copias:


---
source: derived
canonical_path: virtual-teams-setup/00-agent-setup/06.Skills/manifest/SKL-MANIFEST-01.md
sync_status: synced | drift | unknown
last_synced: 2026-05-17
---
Beneficio inmediato: cualquier agente que abra un archivo sabe en 2 segundos si es la fuente o una copia. Si es copia y necesita editarla, sabe a dónde ir.

Pregunta decisoria para B
¿Aprobamos agregar frontmatter source: canonical | derived a todos los archivos normativos y completar el INVENTARIO con la columna "Copias derivadas"?

Implementación:

Script que recorre VTT-setup y agrega frontmatter canonical a todo lo que esté en 00-agent-setup/
Script que detecta los mismos archivos en proyectos consumidores y agrega frontmatter derived + path canónico
Actualizo INVENTARIO con la columna nueva
Tiempo total: 1 hora
¿Confirmas o ajustamos?

Causa raíz A — Regla técnica de dónde editar
Problema: El agente sabe que VTT-setup es fuente de verdad porque se lo dijiste, pero nada le impide editar en otro lado.

Te doy 3 niveles de enforcement ordenados de menos a más estricto. Tú decides cuál implementamos.

Nivel 1 — Convención + autocheck (más simple)
Regla documentada: "si el archivo tiene source: derived en frontmatter, NO se edita"
Pre-edit hook que el agente ejecuta antes de cualquier edición:

python scripts/check_can_edit.py <file_path>
# → OK si source: canonical
# → ABORT si source: derived (mensaje: "edita en <canonical_path>")
Agente desciplinado lo respeta. Agente que ignora regla → falla, queda en log.
Pro: rápido, sin infra. Contra: depende de disciplina del agente.

Nivel 2 — Worktree limitado por rol editorial
Cada agente recibe un worktree con permisos de escritura limitados:
Agente BE de memory-service → solo puede escribir en memory-service-backend/src/** y memory-service-project/knowledge/**
Si intenta editar memory-service-project/00-agent-setup/** → filesystem rechaza
Editor de normativa tiene su propio worktree apuntando a virtual-teams-setup/
Cambio de contexto = abrir otra ventana VSCode
Pro: imposible saltarse. Contra: complejidad inicial, requiere permisos de filesystem distintos por worktree.

Nivel 3 — CI/Pre-commit que bloquea PRs
Pre-commit hook en cada repo proyecto que detecta:

Si el commit modifica un archivo con frontmatter source: derived
  → ABORTA el commit
  → Mensaje: "Este archivo es copia. Edita en <canonical_path> y solicita re-sync"
GitHub Action que valida lo mismo en PRs
Pro: bloqueo final, no se puede ignorar. Contra: requiere instalar hooks en N repos.

Mi recomendación: Nivel 1 ahora, Nivel 3 después
Razón:

Nivel 1 lo implementamos en 30 min, valida la regla
Si Nivel 1 no es suficiente (agentes siguen rompiendo), saltamos a Nivel 3
Nivel 2 es overkill — los worktrees ya están funcionando, no rompamos eso
Pregunta decisoria para A
¿Nivel 1 (autocheck) o Nivel 3 (CI bloquea)? O combinamos.

Si Nivel 1:

Script check_can_edit.py (lee frontmatter, retorna OK/ABORT)
Regla documentada en los OPERATIVOs de cada rol: "ejecutar check antes de editar"
Time: 30 min
¿Cuál eliges?

Causa raíz F — Registro de consumidores
Problema: Cuando se modifica SKL-MANIFEST-01, nadie sabe automáticamente que memory-service-project lo consume. La cascada es manual + de memoria.

Mi propuesta: archivo consumers.json en VTT-setup.


{
  "virtual-teams-setup/00-agent-setup/06.Skills/manifest/SKL-MANIFEST-01.md": {
    "consumers": [
      {
        "project": "memory-service",
        "derived_path": "memory-service-project/00-agent-setup/06.Skills/manifest/SKL-MANIFEST-01.md",
        "last_synced": "2026-05-17",
        "sync_status": "drift",
        "tl_uuid": "92225290-..."
      },
      {
        "project": "designmine",
        "derived_path": "designmine/00-agent-setup/06.Skills/manifest/SKL-MANIFEST-01.md",
        "last_synced": "2026-05-10",
        "sync_status": "drift"
      }
    ]
  }
}
Cuando se edita un archivo canonical:


python scripts/notify_consumers.py SKL-MANIFEST-01.md
# → lee consumers.json
# → identifica N proyectos consumidores
# → crea tareas VTT en cada proyecto consumidor: "Re-sync SKL-MANIFEST-01 v3.X"
# → notifica a TLs
Cuando un proyecto hace sync:


python scripts/sync_from_canonical.py SKL-MANIFEST-01.md
# → copia desde canonical a derived
# → actualiza last_synced en consumers.json
# → cambia sync_status a "synced"
Pregunta decisoria para F
¿Aprobamos consumers.json + 2 scripts (notify_consumers, sync_from_canonical)?

Tiempo: 3 horas

Crear consumers.json poblándolo con los archivos compartidos que detectemos hoy (escaneo automático de duplicados entre VTT-setup y los proyectos)
notify_consumers.py — al editar canonical, lista consumers y opcionalmente crea tareas VTT
sync_from_canonical.py — TL del proyecto ejecuta para traer la versión canónica
Resumen para decidir
Causa	Pregunta clave	Tiempo
B — Índice canónico	¿Frontmatter `source: canonical	derived` + columna en INVENTARIO?
A — Regla técnica	¿Nivel 1 autocheck o Nivel 3 CI? (Mi rec: Nivel 1)	30 min - 3 horas
F — Registro de consumidores	¿consumers.json + 2 scripts?	3 horas
Total si haces los 3 hoy: ~4-5 horas trabajo mío.

Orden de ejecución dentro de cada uno (todos siguen el mismo patrón):

Te muestro el formato exacto del frontmatter / schema / script
Validas con un ejemplo concreto
Ejecuto al resto
Antes de empezar — confirma:
¿Empezamos por B (índice canónico)? Es el cimiento — sin marcar fuentes vs copias, A y F no pueden funcionar.

¿Frontmatter YAML es OK? O prefieres metadata fuera del archivo (un .meta.json paralelo, por ejemplo). El YAML va dentro del .md y es estándar — los Markdown viewers lo respetan.

¿Necesitas ver el formato exacto del frontmatter antes de aprobar, o vamos directo?

Una vez confirmes, ejecuto B sin interrumpir.

vamos con el el indice , lee estos docuemntos:
@C:\Users\Martin\Documents\virtual-teams\virtual-teams-setup\00-platform\INDEX.md
@C:\Users\Martin\Documents\virtual-teams\virtual-teams-setup\00-platform\README.md
Leídos. Tienes un repo muy bien estructurado — la reorganización a 5 entidades + INDEX exhaustivo es exactamente el cimiento que necesitamos para B (Índice canónico).

Lo que ya tienes resuelto
Componente B (índice canónico)	Estado
Inventario completo de archivos	✅ INDEX.md con 318 archivos catalogados
Estructura jerárquica clara	✅ 5 entidades + reglas de organización
Sección "Cuándo entrar aquí" por entidad	✅
Onramp por rol	✅ (5 roles)
Búsqueda rápida por concepto	✅ §6 con 24 entradas
Estadísticas + estado	✅ activos / pending-migration / legacy
Gobierno editorial documentado	✅ §6 — tabla "quién edita qué"
TODOs explícitos	✅ §7 con renombrado, gobierno, sync, drift
Lo que falta para cerrar B (índice canónico)
Tienes 90% del trabajo. Faltan 3 cosas concretas:

Falta 1 — Marker explícito "canonical vs derived"
El INDEX te dice dónde están los archivos, pero no marca cuáles son fuentes oficiales vs copias derivadas que viven en proyectos.

Ejemplo del problema actual:


SKL-MANIFEST-01.md
  → existe en virtual-teams-setup/02.normativa/03.Skills/_pending-migration/manifest/  (¿es canonical?)
  → existe en memory-service-project/00-agent-setup/06.Skills/manifest/                (¿es derived?)
Tu INDEX dice "está en _pending-migration" pero no responde "¿esta es la fuente o la copia?".

Falta 2 — Frontmatter en cada archivo
Cuando un agente abre un archivo aislado (no via INDEX), no sabe:

Si es canonical (puede editar) o derived (solo lectura)
Cuál es su path canonical (a dónde ir si quiere editar la fuente)
Cuándo fue la última sync
Falta 3 — Mapeo formal "canonical → derived" (el consumers.json que propuse)
INDEX lista archivos pero no dice "este SKL-MANIFEST-01 de VTT-setup tiene copia en memory-service-project en este path". Sin ese mapeo, no se puede automatizar la cascada.

Lo bueno: ya hay decisiones en el README que cierran preguntas que tenía pendientes
Mi pregunta anterior	Tu README responde
¿Quién edita qué?	§6 — tabla por carpeta con aprobación PM
¿Política de paths?	§5 — Opción C confirmada (canónico + fallback)
¿Cuál es la fuente de verdad?	Línea 16 — virtual-teams-setup/
¿Cuándo se mueven operativos-instancias?	TODO en §7 — diferido
Mi propuesta concreta para cerrar B
3 acciones, en orden:

Acción 1 — Agregar frontmatter source: canonical a archivos VTT-setup
Script que recorre 00-platform/ y agrega al inicio de cada .md:


---
source: canonical
canonical_path: 00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-ASG-001_*.md
last_modified: 2026-05-17
editors_allowed: [TL, PM]   # según tabla §6 del README
---
Excepciones que NO llevan frontmatter:

.json (no soporta frontmatter — los catalogamos en INDEX)
.py, .zip (no aplica)
Archivos en _pending-migration/ (pendientes — frontmatter source: legacy_pending)
Tiempo: 1 hora. Script idempotente.

Acción 2 — Generar consumers.json escaneando duplicados
Script que:

Lista todos los archivos en VTT-setup
Busca el mismo nombre en memory-service/memory-service-project/ y memory-service/memory-service-backend/
Para cada match → genera entrada en consumers.json
Calcula hash MD5 → marca sync_status: synced | drift
Output: 00-platform/CONSUMERS.json
Formato:


{
  "generated_at": "2026-05-17",
  "consumers": [
    {
      "canonical": "00-platform/02.normativa/03.Skills/_pending-migration/manifest/SKL-MANIFEST-01_generar-manifest.md",
      "derived_paths": [
        {
          "project": "memory-service-project",
          "path": "memory-service-project/00-agent-setup/06.Skills/manifest/SKL-MANIFEST-01_generar-manifest.md",
          "sync_status": "drift",
          "last_synced": null,
          "canonical_hash": "abc123",
          "derived_hash": "def456"
        }
      ]
    }
  ],
  "stats": {
    "total_canonical": 0,
    "total_with_consumers": 0,
    "total_derived": 0,
    "in_drift": 0
  }
}
Tiempo: 1 hora. Script idempotente.

Acción 3 — Agregar al INDEX.md una columna o sección "Consumers"
Para cada archivo canonical que tenga copias en proyectos, agregar nota en INDEX:


| `VTT.PROTOCOL-ASG-001_*.md` | Ciclo asignación tarea | v1.2.0 | 📌 1 consumer: memory-service-project |
O sección dedicada al final del INDEX:


## 11. Archivos con copias en proyectos consumidores

Ver `CONSUMERS.json` para detalle.

| Archivo canonical | Proyectos consumidores | Estado |
|---|---|---|
| `SKL-MANIFEST-01_*.md` | memory-service-project | 🔴 drift |
| `VTT.PROTOCOL-ASG-001_*.md` | memory-service-project | ✅ synced |
Tiempo: 30 min. Manual o script genera tabla desde CONSUMERS.json.

Total para cerrar B
~2.5 horas de trabajo. Output:


00-platform/
├── CONSUMERS.json                ← NUEVO — mapeo canonical → derived
├── INDEX.md                       ← actualizado con sección §11
├── 01.agents/**/*.md              ← cada archivo con frontmatter
├── 02.normativa/**/*.md           ← idem
├── 03.templates/**/*.md           ← idem
├── 04.docs-soporte/**/*.md        ← idem
└── 05.proyectos/**/*.md           ← idem

memory-service/memory-service-project/**/*.md   ← frontmatter source: derived
memory-service/memory-service-backend/**/*.md   ← idem
Antes de ejecutar — 3 confirmaciones
1. ¿Frontmatter YAML es OK en .md?
Frontmatter es la sintaxis de Jekyll/Hugo/Obsidian. Los editores Markdown lo respetan. No rompe nada.

Ejemplo:


---
source: canonical
canonical_path: 00-platform/02.normativa/01.Protocols/VTT.PROTOCOL-ASG-001_ciclo_asignacion_tarea.md
editors_allowed: [TL, PM]
last_modified: 2026-05-17
---

# VTT.PROTOCOL-ASG-001 — Ciclo de Asignación y Cierre de Tarea
...
¿OK?

2. ¿Aplicamos frontmatter también a archivos en _pending-migration/?
Mi recomendación: sí, con source: legacy_pending para marcarlos. Cuando se migren al modelo VTT, se cambia a source: canonical.

¿Confirmas?

3. Orden de ejecución
Te propongo:


1. Acción 2 PRIMERO (CONSUMERS.json) — sin tocar archivos, solo escaneo
   ↓ Te muestro el JSON resultante para validar el mapeo
   
2. Acción 1 DESPUÉS (frontmatter en todos los archivos)
   ↓ Script masivo, idempotente
   
3. Acción 3 AL FINAL (actualizar INDEX con sección §11)
   ↓ Lectura de CONSUMERS.json + tabla en INDEX
¿Vamos en este orden? El cambio mayor es Acción 1 (toca ~300 archivos). Si fallás algo, primero validamos con Acción 2 que el inventario está correcto.

Una vez confirmes los 3 puntos (frontmatter OK, pending-migration sí, orden 2→1→3), ejecuto sin interrumpir.

ttodo lo qeu es en repo es la fuetnete d ela verdad
lo unico que es derivado es lo que hay en 05.proyectos.
Asi e siple y sencillo todo lo que esta fuera de este repo no se considera como aprte de la doceumtnacion oficial

Ahora ojo proqeue so se va a subir al proeycto vtt setup  ahi es donde van a vivir dlos doceumtnso  de fuetne verdadera.

que faltaria para determianr como se editan los docuemntos
Bajado. Cierras el problema B con esa regla tan simple. Te bajo el análisis.

La regla queda simplificada

TODO lo que vive en virtual-teams-setup/  = CANONICAL
TODO lo que vive en 05.proyectos/           = DERIVED (instancias)
TODO lo que NO está en el repo              = NO existe oficialmente
Más adelante:


Cuando suba a VTT-setup project en VTT API    = FUENTE OPERATIVA (con versionado, search, links)
El repo virtual-teams-setup/                    = RESPALDO GIT + edición humana
Eso elimina necesidad de frontmatter por archivo. La ubicación dicta el tipo.

Lo que falta para definir cómo se editan los documentos
Te bajo los 7 puntos pendientes ordenados por urgencia. Son las decisiones que tienen que estar tomadas antes de que cualquier agente edite.

Punto 1 — Quién puede editar VTT-setup (autorización)
Pregunta: ¿Quién tiene permiso de modificar archivos en virtual-teams-setup/?

Opción A	Solo PM (tú) edita. Agentes proponen vía ticket
Opción B	PM + 1-2 agentes editores (TL Normativa, PM editorial)
Opción C	Cualquier agente con autorización por carpeta (CODEOWNERS)
El README §6 ya lo tiene mapeado por carpeta. Falta convertir esa tabla en regla técnica:

¿GitHub branch protection + CODEOWNERS?
¿O por convención + auditoría reactiva?
Punto 2 — Proceso de cambio (workflow desde idea hasta archivo editado)
Necesitas declarar el flujo completo:


Agente detecta necesidad de cambio
    ↓
¿Cómo lo propone?
    - Tarea VTT en proyecto VTT-setup
    - GitHub Issue
    - Mensaje al PM
    ↓
¿Quién aprueba?
    - PM siempre
    - Solo cambios "estructurales"
    ↓
¿Quién ejecuta el cambio?
    - El agente que propuso (autoriza la edición)
    - Un agente editor dedicado
    - El PM
    ↓
¿Dónde edita?
    - VTT-setup local (Git)
    - Solo después de tener aprobación
    ↓
¿Cómo se valida?
    - PR + review
    - Lint + tests automáticos
    - Solo merge manual
    ↓
¿Cuándo se publica?
    - Cada merge
    - Por release (v1.0, v1.1, etc.)
Punto 3 — Clasificación de cambios (severidad)
No todos los cambios son iguales. ¿Diferenciamos?

Tipo de cambio	Ejemplo	Quién autoriza
Editorial (typo, ejemplo, aclaración)	"Corregir typo en línea 42"	TL o auto-aprobado
Funcional (paso nuevo, regla nueva)	"Agregar paso 5.3.7 Hardcode Check"	TL → PM informa
Estructural (campo en schema, ubicación)	"Renombrar campo X en manifest"	PM aprueba
Breaking (rompe consumidores)	"Eliminar campo Y"	PM + migración planificada
Sin esto, todo cambio pasa por el mismo proceso (lento) o ninguno (caos).

Punto 4 — Cuándo se sincroniza con proyectos consumidores
Hoy lo haces copy/paste manual. Eso seguirá siendo así hasta que:

Suba a VTT-setup project en VTT API (con endpoints)
O implementes IMPROVE-004 (Hook Manager)
Mientras tanto necesitas:

¿Cada cambio en VTT-setup → notificar a TLs de proyectos consumidores?
¿Esperar al cierre de sprint para batch sync?
¿Los TLs deciden cuándo traer cambios?
Punto 5 — Validación pre-edición (guardrails)
Antes de aceptar un cambio:

¿Hay JSON Schema validable? (manifest, rules_catalog, capabilities_catalog)
¿Hay linter de estructura? (Protocol debe tener §1-§7, etc.)
¿Hay validación de unicidad de paths/códigos?
¿Hay verificación de referencias rotas? (si elimino archivo X, ¿qué otros lo referencian?)
Punto 6 — Trazabilidad del cambio
Cada edición debe registrar:

Quién editó (agente + usuario humano que autorizó)
Cuándo (timestamp)
Por qué (referencia al ticket/issue que originó)
Qué cambió (diff)
Versión (semver bump)
¿Cómo se registra?

Solo Git log (commit message estructurado)
Tabla VTT (cuando subamos a project)
Ambos
Punto 7 — Onboarding del proceso (cómo lo aprende un agente nuevo)
Cuando un agente nuevo entra al proyecto VTT-setup:

¿Lee un documento PROCESO_EDICION_VTT_SETUP.md?
¿Tiene un OPERATIVO específico de editor?
¿Hay un INIT_EDITOR.md?
Sin esto, cada agente nuevo va a romper convenciones por desconocimiento.

Cómo te propongo abordarlo
Te puedo proponer 2 caminos:

Camino corto (1-2 horas) — Documento mínimo viable
Genero un único PROCESO_EDICION_VTT_SETUP.md que responda los 7 puntos con decisiones simples:


Punto 1 — Solo PM edita por ahora
Punto 2 — Flujo: ticket → PM aprueba → PM edita → commit → notifica TLs
Punto 3 — 3 tipos: editorial / funcional / estructural
Punto 4 — Manual por ahora (PM copia a proyectos en batch al cierre de sprint)
Punto 5 — Validación: query_rules.py --validate para JSONs, ninguna para .md
Punto 6 — Git log + commit message estructurado
Punto 7 — Documento se referencia en README §6 + onboarding
Suficiente para arrancar. Iteramos cuando duela algo.

Camino completo (4-6 horas) — Sistema robusto
Implementamos:

GOBIERNO_VTT_SETUP.md (estructura formal)
PROCESO_EDICION_VTT_SETUP.md (workflow detallado)
CODEOWNERS (si está en git)
Script validate_change.py (lint + schemas + referencias)
Template IMPROVEMENT_REQUEST.md (formato del ticket)
Workflow VTT en proyecto VTT-setup para tickets
Onboarding INIT_EDITOR_VTT_SETUP.md
Antes de elegir camino — 3 preguntas decisorias
1. ¿Hoy hay agentes editando VTT-setup además de ti?
Si NO → camino corto. Tú eres único editor mientras tanto.
Si SÍ → camino completo. Necesitas reglas para todos.
2. ¿VTT-setup ya está como repo Git?
Si NO (carpeta local) → camino corto + agregar git init después
Si SÍ → camino completo con CODEOWNERS y PR
3. ¿Cuándo planeas subirlo al proyecto VTT-setup en VTT API?
Esta semana → camino completo (vale la pena hacerlo bien antes)
En 2-4 semanas → camino corto + iterar
Más adelante → camino corto
Mi recomendación rápida: camino corto ahora. Sales con PROCESO_EDICION_VTT_SETUP.md que responde los 7 puntos con decisiones simples. Cuando duela algo o entren más agentes editores, lo iteramos.

¿Cuál tomamos? Si camino corto, me das tus respuestas a los 7 puntos (o las propones tú) y genero el documento.

no, el repo aun no existe en git lo peudo crear, 
SIm cualquier agente oude modificar los arhcivos ahorita tengo a 6 agentes trabajando en difernetes areas porque ses que puden modificarlos

proque estmos en la fase de desarrollo

en un futuro nadie deberia modificar los cdocuemtnso, si dse requeire algun cambiom se modifica en ela rhcivo lcoal de cada repo ys e subiria al sistema apra que eela gente o yo reviselos el cambio que se propone y entocnes el agente y yo en el repo se revisen lso cambios se omodifique el doceumtnp y se apruebe como valido y se peuda replciar pata tods los  proeyctos.

pero por el moemnto nneceistamos un rpoceso que eprmita modificar los doceumtnso si n que detenga el trabajdo
Bajado. Te bajo el modelo completo en dos tiempos.

Modelo de gobierno editorial — dos fases
FASE ACTUAL (desarrollo — hoy)
Caos controlado. 6 agentes editan en paralelo. Reglas mínimas para no bloquearlos pero que evitemos el caos puro:


Agente edita VTT-setup directo
       ↓
Sin aprobación previa
       ↓
SOLO requisito: commit estructurado + branch propio
       ↓
PM revisa al cierre del día (audit reactiva)
FASE FUTURA (post-desarrollo — cuando se estabilice)
Gobierno con tickets. Nadie edita VTT-setup directo.


Agente en proyecto X detecta cambio necesario
       ↓
Modifica el archivo en SU repo local (memory-service-project/...)
       ↓
Crea ticket en sistema (VTT proyecto VTT-setup) con propuesta
       ↓
Ticket llega al PM (tú) + editor designado
       ↓
PM + editor revisan el diff
       ↓
Si aprueba → editor aplica cambio en VTT-setup
       ↓
Replica a todos los proyectos (vía sistema VTT)
Para la FASE ACTUAL (lo urgente)
Necesitamos un proceso mínimo de 4 reglas que evite el desastre sin frenar el trabajo:

Regla 1 — Branch propio por agente
Cada agente trabaja en su rama:


agent/<rol-o-nombre>/<descripción-corta>
   ej. agent/tl-normativa/protocol-asg-update
   ej. agent/equipo-perfiles/profile-be-v2
NO se commitea a main directo. Esto requiere git init y branch protection.

Regla 2 — Commit message estructurado
Cada commit indica qué se tocó, por qué, quién (qué agente/proyecto):


[agente:tl-normativa] [scope:02.normativa/01.Protocols] [type:functional]
PROTOCOL-ASG-001: agregar paso 5.3.7 Hardcode Check

- Motivo: lección de MS-285 — agentes no ejecutaban check antes de PR
- Origen: sesión 2026-05-17 con PM
- Consumidores afectados: memory-service-project
Sin esto, el log de cambios es ruido.

Regla 3 — Daily merge a main (con auditoría tuya)
Cada agente termina su día con su rama. Al final del día (o cada 24h máximo):

PM revisa los commits del día por rama
Aprueba o pide cambios
Merge a main
No bloquea trabajo. Audit reactiva en vez de bloqueo preventivo.

Regla 4 — Conflict resolution declarada
Si 2 agentes editan el mismo archivo:

Quien hace merge primero, gana
El segundo hace rebase + resuelve conflicts antes de su merge
PM se entera porque sale en el daily review
Lo que necesitas decidir HOY
Decisión 1 — Git init en VTT-setup
¿Lo convertimos a repo git ahora?

Sin git no hay branches, no hay commits con metadata, no hay diff revisable. La FASE ACTUAL no funciona sin esto.

Tiempo: 5 min:


cd virtual-teams-setup
git init
git add .
git commit -m "Initial — baseline VTT-setup v1.0.0"
git remote add origin <repo-github>
git push -u origin main
Decisión 2 — ¿Cómo se reparten los 6 agentes hoy?
Necesito saber para diseñar reglas que no choquen:

Agente	¿En qué carpeta edita?
Equipo Perfiles	01.agents/roles/ y setups/?
Equipo Worktrees	04.docs-soporte/guias-operativas/ y 02.normativa/01.Protocols/_pending-migration/PROCESO_*?
TL Normativa (tú/asistente)	02.normativa/?
Agente Setup	01.agents/setups/?
...	...
Si me dices quién toca qué, podemos:

Validar que NO hay overlap
Donde haya overlap → declarar regla específica (ej. "PROCESO_CIERRE_TAREA solo lo toca TL Normativa")
Decisión 3 — ¿Branch protection desde día 1 o después?
Opción A	Sin branch protection — todos pueden commitear a main. Audit reactiva	Más rápido, riesgo alto
Opción B	Branch protection desde día 1 — todos van por PR	Más lento al inicio, sin riesgo
Si son 6 agentes paralelos, Opción B. Si fueran 2, Opción A.

Decisión 4 — ¿Hay un editor dedicado por carpeta o todos editan donde sea?
Lo ideal según README §6:

01.agents/ → Equipo Perfiles edita
02.normativa/ → TL + PM edita
etc.
Si lo aplicamos hoy:

Cada agente tiene su carpeta asignada
No cruza a otras carpetas sin avisarte
Reduce conflicts dramáticamente
¿Lo aplicamos?

Decisión 5 — Daily review ¿quién lo hace y cuándo?
Tú (PM) revisas commits al final del día → 30-60 min
Asistente IA revisa y te resume → 10 min de tu tiempo
No hay review — solo merge automático con auditoría semanal
Mi propuesta para arrancar HOY
Si los 5 puntos los respondes así (aproximado), genero el documento:

Decisión	Respuesta sugerida
1. Git init	Sí, ahora (5 min)
2. Mapeo de agentes	Me lo das tú con nombres reales
3. Branch protection	Sí, desde día 1 (PR obligatorio)
4. Editor por carpeta	Sí, según §6 README
5. Daily review	PM revisa con asistente IA (yo te resumo, tú apruebas)
El documento que generaría
PROCESO_EDICION_VTT_SETUP_v1_DESARROLLO.md

Contenido:


1. Estado actual — fase desarrollo (hasta cuándo)
2. Las 4 reglas mínimas
3. Mapeo de agentes → carpetas
4. Git workflow (branch naming, commit format)
5. Conflict resolution
6. Daily review (qué revisa el PM)
7. Cómo evolucionará a fase futura (referencia al modelo de tickets)
8. Quién es responsable de qué
9. Qué pasa si un agente rompe la regla
Tamaño: ~150 líneas. Tiempo: 1 hora.

Después generamos el PROCESO_EDICION_VTT_SETUP_v2_PRODUCCION.md cuando se estabilice (modelo de tickets, validación, etc.).

Antes de ejecutar — confirmas
¿Git init ahora? Yo lo puedo hacer en 5 min si me autorizas.
¿Me das el mapeo de los 6 agentes? Para no inventar.
¿Las 5 decisiones que sugerí están OK?
¿Procedo con el documento de fase desarrollo?
Una vez confirmes, ejecuto.

Regla 1 — Branch propio por agente
ndefine las reglas o  una skill apra que se peuda implementar

Regla 2 — Commit message estructurado
define la refgla y desarrolla el skill apr que lso agente lo usen

Decisión 2 — ¿Cómo se reparten los 6 agentes hoy?

NO peudo definirlo es imposible
son 6 agenters en 3 proyctos diferentes comoforme voy trabajnado si detecto algun a cambio trabajo cone se agent y no lo suelto ahasta que haya terminado dde trabajar las mejroas o

Decisión 4 — ¿Hay un editor dedicado por carpeta o todos editan donde sea?
no y no s epeude aplciar
Decisión 5 — Daily review ¿quién lo hace y cuándo?

no y nos e peud epalciar
Bajado. Te bajo plan ajustado a tu realidad.

Lo que entiendo
Decisión	Tu realidad
1. Git init	Sí, requerido
2. Mapeo agentes	Imposible. 6 agentes en 3 proyectos. Asignación fluida según necesidad.
3. Branch protection	Pendiente decidir
4. Editor por carpeta	No aplica. Cualquier agente puede tocar cualquier carpeta.
5. Daily review	No aplica. Sin daily review.
Esto cambia el diseño. No podemos depender de "quién toca qué" ni de "review programado". Las reglas tienen que funcionar sin coordinación previa entre agentes.

Las 2 reglas que pediste — formalizadas
Regla 1 — Branch propio por agente
Patrón obligatorio:


agent/<rol>/<proyecto-origen>/<descripcion-corta-kebab-case>
Ejemplos:


agent/tl/memory-service/protocol-asg-update
agent/be/designmine/add-rule-be-coverage
agent/pjm/vtt-setup/profile-pjm-v2
Reglas:

<rol> = código corto del rol del agente (tl, be, pm, pjm, do, db, fe, qa, ux, dl, sa, ar, sec)
<proyecto-origen> = proyecto que originó el cambio (memory-service, designmine, vtt-setup)
<descripcion-corta-kebab-case> = máx 50 chars
NO se commitea directo a main
Una rama por edición — no acumular cambios no relacionados
La rama se borra después del merge
Por qué este formato: sin asignación fija de agentes, el branch name es el único registro de "quién hizo qué desde dónde". Sin esto, el git log es ruido.

Regla 2 — Commit message estructurado
Formato obligatorio:


[agente:<rol>] [proyecto:<origen>] [scope:<ruta>] [type:<tipo>]
<título corto — 60 chars max>

<descripción — qué cambió y por qué — 3-5 líneas>

Motivo: <razón del cambio>
Origen: <ticket / sesión / PR / lección — id o referencia>
Consumidores: <lista de proyectos afectados o "none">
Campos:

<rol> — tl, be, pm, pjm, etc.
<origen> — vtt-setup, memory-service, designmine, etc.
<scope> — ruta de carpeta(s) tocadas (02.normativa/01.Protocols o multiple)
<tipo> — editorial | functional | structural | breaking
Ejemplo real:


[agente:tl] [proyecto:memory-service] [scope:02.normativa/01.Protocols] [type:functional]
PROTOCOL-ASG-001: agregar paso 5.3.7 Hardcode Check

Agente debe ejecutar grep de patrones de secretos antes
de mover tarea a in_review. Findings critical/high bloquean
Review Gate. FPs requieren justificación en devlog.

Motivo: lección MS-285 — agentes saltaban este check
Origen: sesión 2026-05-17 con PM
Consumidores: memory-service-project
Por qué este formato:

[agente:X] permite filtrar git log por rol
[proyecto:Y] permite saber qué proyecto originó el cambio
[scope:Z] permite detectar qué carpetas se tocan
[type:W] permite priorizar reviews (breaking > structural > functional > editorial)
Cómo implementarlo sin coordinación
Componente 1 — Skill SKL-GIT-VTT-BRANCH-01 (crear rama)
Archivo: 00-platform/02.normativa/03.Skills/git-ops/SKL-GIT-VTT-BRANCH-01_crear_branch_vtt_setup.md

Inputs requeridos:

$AGENT_ROLE — del .env del agente (tl, be, pm, etc.)
$ORIGIN_PROJECT — proyecto donde el agente opera (memory-service, designmine, vtt-setup)
$BRANCH_DESCRIPTION — descripción kebab-case (input del usuario o derivado del ticket)
Validación previa (auto):


# 1. Validar formato del rol
[[ "$AGENT_ROLE" =~ ^(tl|be|pm|pjm|do|db|fe|qa|ux|dl|sa|ar|sec)$ ]] || ABORT "rol inválido"

# 2. Validar formato del proyecto
[[ "$ORIGIN_PROJECT" =~ ^(vtt-setup|memory-service|designmine|.*)$ ]] || ABORT

# 3. Validar descripción
[[ "$BRANCH_DESCRIPTION" =~ ^[a-z0-9-]{3,50}$ ]] || ABORT "descripción debe ser kebab-case 3-50 chars"

# 4. Verificar que NO estamos en main
git rev-parse --abbrev-ref HEAD | grep -v '^main$' || ABORT "no creates ramas desde main directamente — pull first"
Ejecución:


cd virtual-teams-setup
git fetch origin
git checkout main && git pull
BRANCH="agent/$AGENT_ROLE/$ORIGIN_PROJECT/$BRANCH_DESCRIPTION"
git checkout -b "$BRANCH"
echo "Branch creada: $BRANCH"
Validación posterior:

HEAD apunta al branch nuevo
Branch tiene el formato correcto
Error común: rol no en lista → editar roles.txt autorizado.

Componente 2 — Skill SKL-GIT-VTT-COMMIT-01 (commit estructurado)
Archivo: 00-platform/02.normativa/03.Skills/git-ops/SKL-GIT-VTT-COMMIT-01_commit_vtt_setup.md

Inputs requeridos:

$AGENT_ROLE, $ORIGIN_PROJECT (env)
$TITLE — título corto (máx 60 chars)
$DESCRIPTION — qué + por qué (3-5 líneas)
$MOTIVO — razón del cambio
$ORIGEN — ticket / sesión / lección
$CONSUMIDORES — lista de proyectos o "none"
$TYPE — editorial | functional | structural | breaking
Validación previa (auto):


# 1. Detectar scope automáticamente
SCOPE=$(git diff --cached --name-only | xargs -I{} dirname {} | sort -u | head -3 | paste -sd ',')
[ -z "$SCOPE" ] && ABORT "no hay nada staged"
[ "$(echo $SCOPE | tr ',' '\n' | wc -l)" -gt 1 ] && SCOPE="multiple"

# 2. Validar título
[ ${#TITLE} -gt 60 ] && ABORT "título excede 60 chars"

# 3. Validar tipo
[[ "$TYPE" =~ ^(editorial|functional|structural|breaking)$ ]] || ABORT

# 4. Bloquear commit a main
[ "$(git rev-parse --abbrev-ref HEAD)" = "main" ] && ABORT "no commitees a main directo"
Ejecución:


git commit -m "[agente:$AGENT_ROLE] [proyecto:$ORIGIN_PROJECT] [scope:$SCOPE] [type:$TYPE]
$TITLE

$DESCRIPTION

Motivo: $MOTIVO
Origen: $ORIGEN
Consumidores: $CONSUMIDORES
"
Validación posterior:

git log -1 --format=%B retorna el commit con todos los markers [agente:], [proyecto:], [scope:], [type:]
Componente 3 — Script atómico SCR-GIT-VTT-VALIDATE-01
Archivo: 00-platform/02.normativa/04.Scripts/SCR-GIT-VTT-VALIDATE-01_validate_commit.py

Hook que valida pre-commit y pre-push:

Branch tiene formato agent/<rol>/<proyecto>/<desc>
Commit message tiene los 4 markers obligatorios
No hay commits a main
Detecta conflictos potenciales (otro agente tocó el mismo archivo en main desde tu base)
Modo uso:


# Pre-commit hook
python 02.normativa/04.Scripts/SCR-GIT-VTT-VALIDATE-01.py --pre-commit

# Pre-push hook
python 02.normativa/04.Scripts/SCR-GIT-VTT-VALIDATE-01.py --pre-push

# Validación on-demand de un agente
python 02.normativa/04.Scripts/SCR-GIT-VTT-VALIDATE-01.py --check-current
Componente 4 — Documento PROCESO_EDICION_VTT_SETUP_FASE_DESARROLLO.md
Archivo: 00-platform/04.docs-soporte/guias-operativas/PROCESO_EDICION_VTT_SETUP_FASE_DESARROLLO.md

Contenido:


1. Fase actual y duración
2. Las 2 reglas (branch + commit)
3. Workflow del agente (paso a paso)
4. Cómo detectar conflictos
5. Qué hacer si rompes una regla
6. Cómo evoluciona a fase futura
Sin daily review, ¿cómo detectamos problemas?
Sin tu review tampoco hay nadie validando que no haya catástrofes. Te propongo 3 mecanismos automáticos que no requieren tu tiempo:

Mecanismo 1 — CI que valida cada PR
GitHub Action:

Valida formato de branch name
Valida formato de commit message
Rechaza si falta algún marker
Bloquea merge si falla
Tiempo de implementación: 30 min.

Mecanismo 2 — Bot de alertas (futuro IMPROVE)
Bot que detecta:

Commits a 02.normativa/01.Protocols/ con [type:breaking] → te notifica
Conflictos en mismo archivo por 2 agentes → notifica a ambos
Archivos editados >3 veces en un día → posible inestabilidad
Mecanismo 3 — Reporte semanal automático
Script que cada lunes genera resumen:

Cuántos commits por agente
Cuántos por tipo (editorial/functional/structural/breaking)
Top 10 archivos más editados
Conflictos resueltos
Output: archivo MD que tú lees en 5 min.

Plan de ejecución propuesto

HOY:
  1. Git init en virtual-teams-setup (5 min)
  2. .gitignore (5 min)
  3. Commit baseline v1.0.0 (5 min)
  4. Crear las 2 skills: BRANCH-01, COMMIT-01 (1 hora)
  5. Crear el script VALIDATE-01 (1 hora)
  6. Crear PROCESO_EDICION_VTT_SETUP_FASE_DESARROLLO.md (1 hora)
  7. Instalar pre-commit hooks (30 min)

MAÑANA O DESPUÉS:
  8. GitHub repo + branch protection (30 min)
  9. CI workflow (30 min)

CUANDO ESTABILICES:
  10. Sistema de tickets (fase futura — para después)
Decisiones pendientes para ejecutar HOY
Decisión 1 — ¿Git init ya?

cd virtual-teams-setup
git init
git add .
git commit -m "[agente:pm] [proyecto:vtt-setup] [scope:all] [type:structural]
Initial — baseline VTT-setup v1.0.0

Primer commit con la estructura reorganizada en 5 entidades.
318 archivos catalogados en INDEX.md.

Motivo: bootstrap del gobierno editorial
Origen: sesión 2026-05-17 con PM
Consumidores: memory-service-project, memory-service-backend"
¿Procedo?

Decisión 2 — ¿Branch protection sí o no?
Sí branch protection	No branch protection
Imposible commit a main directo	Posible commit accidental a main
PR obligatorio (más lento)	Más rápido
Audit reactiva via PR comments	Audit reactiva via git log
Mi recomendación: sí, branch protection desde día 1. Sin asignación de agentes ni daily review, esto es tu única defensa contra el caos.

Decisión 3 — ¿GitHub repo o solo local?
Solo local → no hay PRs, no hay CI, solo git log
GitHub → PRs + CI + colaboración real
Mi recomendación: GitHub ya que tienes 6 agentes en 3 proyectos. Sin servidor central no escala.

Decisión 4 — Lista autorizada de roles
Roles válidos en <rol> del branch name:


tl, be, pm, pjm, do, db, fe, qa, ux, dl, sa, ar, sec, setup
¿Falta alguno? ¿Cuál descartas?

Decisión 5 — Tipos válidos en commit [type:]

editorial   — typo, ejemplo, aclaración (sin cambio de proceso)
functional  — paso nuevo, regla nueva, mejora funcional
structural  — cambio en schema, nueva carpeta, nueva entidad
breaking    — elimina o rompe consumidores
¿Los 4 te sirven? ¿Agregar/quitar?

Si me confirmas las 5 decisiones, ejecuto en este orden:


1. Git init (5 min)
2. Generar SKL-GIT-VTT-BRANCH-01 (30 min)
3. Generar SKL-GIT-VTT-COMMIT-01 (30 min)
4. Generar SCR-GIT-VTT-VALIDATE-01 (1 hora)
5. Generar PROCESO_EDICION_VTT_SETUP_FASE_DESARROLLO.md (1 hora)
6. Instalar pre-commit hooks (30 min)
Total: 4 horas para tener todo operativo
Si dices "vamos", arranco con git init.

