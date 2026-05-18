Emails memory-service actualizados
Rol	Email (nuevo)	UUID
Tech Lead	memory-service.tl@vtt.ai	92225290-6b6b-4c1f-a940-dcb4262507aa
Backend Engineer	memory-service.be@vtt.ai	ebbe3cee-abed-4b3b-860d-0a81f632b08a
Database Engineer	memory-service.db@vtt.ai	6fae26f0-fc87-42d3-9a9e-eb6b1dbe6dd7
Frontend Developer	memory-service.fe@vtt.ai	d23c9cd9-a156-433b-8900-94add5488eec
QA Engineer	memory-service.qa@vtt.ai	613c9538-658c-45fe-a6d7-c1ea9ff04b78
DevOps Engineer	memory-service.devops@vtt.ai	322e3745-9756-4a7c-af11-44b33edef44d
Design Lead	memory-service.dl@vtt.ai	b3a09269-cded-468c-a475-15a48f203cb0
UX Designer	memory-service.ux@vtt.ai	a75a1dae-754a-4b6f-a3ff-db8d51f6a91b
Product Strategy Analyst	product-strategy@memory-service.vtt.ai	a43f6bd0-3452-46ea-85ae-78589c071a3e	✅ creado
Competitive Intelligence Analyst	competitive-intel@memory-service.vtt.ai	4ccfe002-ddd3-4df7-bf31-825dcebd576e	✅ creado
Market Research Analyst	market-research@memory-service.vtt.ai	44e7bfb3-2aca-4ac1-820e-0836e95cd718	✅ creado
Integration Reviewer	integration-reviewer@memory-service.vtt.ai	f3e358f7-679f-400f-8dd7-df41517bca15	✅ creado
SA (Solution Analyst)	sa@memory-service.vtt.ai	0c128e3b-db3b-4e31-b107-0379b5791233	✅ ya existía
AR (Architect)	ar@memory-service.vtt.ai	e9403c25-c1f8-4b64-b2ef-f447d53115e2	✅ ya existía


service key

hBCGEKm41BijI6jJ-s91KTMfv4pZ4a06d4a06d

-------- proceso

Capa 1 — Auto-cargado en cada sesión:

MEMORY.md (auto-memory del proyecto — se inyecta automáticamente al contexto)
rules_agents.instructions.md (reglas globales de todos los agentes)
OPERATIVO_TECH_LEAD.md (.claude/agents/OPERATIVO_TECH_LEAD.md) — este es el archivo central del TL
Capa 2 — El TL lee manualmente al iniciar (rutina de apertura en el OPERATIVO):

knowledge/agent-tasks/CONTEXTO_TECH_LEAD_SESION.md — estado actual del sprint
GET /api/tasks?assigneeId=abdff0db... — sus tareas asignadas en VTT
Project_setup/standard/03_FLUJO_TL.md — SOP genérico del rol
Para Bloque 1 específicamente, además:
4. HANDOFF_TL_S01.md (ya en VTT como ProjectDocument)
5. Los BRIEFs de VTT-507..510 (los de las tareas desbloqueadas)

Entonces para setear un nuevo TL solo necesitas:

Configurar el agente con .claude/agents/OPERATIVO_TECH_LEAD.md como instrucciones de sistema
El MEMORY.md se auto-inyecta solo (ya está configurado)
El TL arranca y él mismo sabe qué leer en su rutina de apertura
