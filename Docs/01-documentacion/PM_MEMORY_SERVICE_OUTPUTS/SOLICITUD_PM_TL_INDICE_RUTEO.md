# SOLICITUD PM → TL: Índice de Ruteo de Deliverables

**De:** PM — Martin Rivas (`350831b2-e1ae-4dbe-b2eb-7e023ec2e103`)
**Para:** TL (`92225290-6b6b-4c1f-a940-dcb4262507aa`)
**Fecha:** 2026-05-12
**Prioridad:** ALTA — bloquea generación de HANDOFFs para S1-S8
**Estimado:** 3-4h

---

## Problema

El PJM no puede generar HANDOFFs con detalle técnico real porque el task breakdown (3B.9.3) no indica qué documento 3B es la fuente de cada deliverable. Sin esa información, el PJM inventa contenido o pone referencias genéricas. Ambas opciones son inaceptables.

## Lo que necesito

Un índice que mapee cada deliverable ✅ del task breakdown a su spec source. Formato:

| Deliverable ID | Nombre | Spec Source | Sección | D-MEM aplicables | Docs para el agente |
|:-:|---|---|---|---|---|
| 4.2.1 | Initial Migration | 3B.3.2_schema_prisma.md | completo | D-MEM-10, D-MEM-41 | 3B.3.1, 3B.3.2 |
| 4.2.3 | Seed Data | 3B.3.2_schema_prisma.md | §catálogos | D-MEM-14, D-MEM-20 | 3B.3.2 |
| 4.3.7 | Middlewares | 3B.4.3_middleware_specs.md | §auth, §validation, §rateLimit | D-MEM-26, D-MEM-09 | 3B.4.3, 3B.4.5, Addendum Bloque 0 Lite |
| 4.3.1 | API Endpoints | 3B.4.2_endpoints_list.md | completo | D-MEM-07, D-MEM-05 | 3B.4.2, 3B.5.1 |
| ... | ... | ... | ... | ... | ... |

## Columnas

| Columna | Qué poner | Ejemplo |
|---------|-----------|---------|
| **Spec Source** | El documento 3B donde está la spec técnica del deliverable | `3B.3.2_schema_prisma.md` |
| **Sección** | La sección específica dentro del doc (para que el agente no lea todo) | `§catálogos` o `completo` |
| **D-MEM aplicables** | Qué decisiones cerradas de la SPEC v1.9 debe respetar el agente | `D-MEM-14, D-MEM-20` |
| **Docs para el agente** | Lista de documentos que el agente debe leer antes de ejecutar la tarea | `3B.3.2, 3B.5.1` |

## Alcance

Los 174 deliverables ✅ de Fases 4-7 del task breakdown (3B.9.3). Si quieres empezar por lo urgente, los de S1 y S2 primero (22 deliverables).

## Por qué solo tú puedes hacerlo

Tú escribiste los documentos 3B. Tú sabes qué doc define cada deliverable. Ni el PM ni el PJM pueden inferir esa relación sin abrir cada 3B y mapear manualmente.

## Dónde entregarlo

Puede ser una tabla adicional en 3B.9.3, o un documento separado `3B.9.10_routing_index.md`. El formato es lo de menos mientras tenga las 5 columnas.

## Qué pasa con esta información

```
TL entrega índice de ruteo
    ↓
PM genera HO por sprint con referencias reales (no contenido inlineado)
    ↓
PJM genera HANDOFF por sprint para TL con ruteo incluido
    ↓
TL genera ASSIGNMENT por tarea abriendo el 3B referenciado
    ↓
Agente ejecuta con spec real, no con contenido inventado
```

---

**Entrega esperada:** `3B.9.10_routing_index.md` o columnas adicionales en `3B.9.3`
**Deadline:** Antes de que el PJM genere el HANDOFF de S1
