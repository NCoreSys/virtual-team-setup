# CONTEXTO QA — Estado de Sesión Persistente

> **INSTRUCCIÓN:** Leer este archivo AL INICIO de cada sesión. Actualizar AL FINAL de cada sesión.

**Última actualización:** 2026-05-01

---

## Identidad

| Campo | Valor |
|-------|-------|
| Agente | QA Engineer |
| UUID | `613c9538-658c-45fe-a6d7-c1ea9ff04b78` |
| Email | `memory-service.qa@vtt.ai` |
| API VTT | `http://77.42.88.106:3000` |
| Proyecto ID | `d0fc276d-e764-4a83-96e9-d65f086ed803` |
| Project Key | MS |
| Repo principal | `memory-service` (ADR-001) |

---

## Estado del Proyecto

**Fase actual:** Project Setup (Phase 1).
**Mi trabajo arranca en:** Testing Phase 8 (MEM-094..103).
**Bloqueado por:** Development Phase 7 completa — no puedo testear sin backend.

---

## Mis Responsabilidades

- Diseñar y ejecutar plan de testing para Memory Service
- Testing de integración, performance (`GET /context` <500ms), idempotencia
- Testing de los 11 endpoints R1
- Reporte de bugs y verificación de fixes
- Testing Phase 8: 10 tareas, 60h

---

## Tareas Asignadas a Mí

| Tarea | Título | Estado |
|-------|--------|--------|
| *(consultar VTT al iniciar sesión)* | — | — |

```bash
curl -s "http://77.42.88.106:3000/api/tasks?projectId=d0fc276d-e764-4a83-96e9-d65f086ed803&assigneeId=613c9538-658c-45fe-a6d7-c1ea9ff04b78" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

---

## Próximos Pasos

1. Esperar que Development Phase 7 esté completa
2. Leer SPEC v1.9 §8 (contratos API) para preparar casos de prueba
3. Al iniciar Phase 8: obtener token y comenzar con MEM-094

---

## Contexto Técnico Relevante

| Recurso | Valor |
|---------|-------|
| API a testear | `http://[host]:3002` |
| SLA crítico | `GET /context` < 500ms (contractual) |
| Idempotencia | reimport del mismo session → `ALREADY_INDEXED`, no error |
| Fuentes a testear | 5 (CLAUDE_SDK, CLAUDE_CLI, CLAUDE_WEB, CHATGPT, VTT_CHANNEL) |

### Casos de prueba clave

| Caso | Endpoint | Criterio |
|------|----------|---------|
| Import idempotente | POST /import | Segundo import → ALREADY_INDEXED |
| SLA context | GET /context | Respuesta < 500ms siempre |
| Cleanup recovery | — | ERROR tras 3 retries del cleanup job |
| Multi-agent review | POST /import-review | primaryAgentId = NULL, participantes en join |

---

## Documentos Clave

1. `knowledge/PROJECT_MEMORY.md` — particularidades §7 (casos edge críticos)
2. `memory-service-project/Release2.0/01-PM/SPEC_MEMORY_SERVICE_v1.9_CONSOLIDADO.md` — §8 contratos, §7 SLAs
3. `.claude/rules/PROJECT_RULES.md` — workflow y entregables
4. `knowledge/GUIA_AGENTES_MODELO_DINAMICO_V4.md` — endpoints VTT V4

---

## Notas de Coordinación

- Coordinar con BE si se encuentran bugs — reportar como devlog entry `categoryCode: blocker`
- Los bugs críticos bloquean el review gate de las tareas de testing
- Verificar `GET /review-gate` antes de mover cada tarea a in_review

---

## Cómo Actualizar Este Archivo

Al terminar sesión: bugs encontrados, casos probados, próxima tarea, fecha.
