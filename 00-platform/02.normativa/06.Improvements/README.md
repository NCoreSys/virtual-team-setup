# Mejoras propuestas — VTT Normativa

Carpeta de **mejoras pendientes de evaluación** detectadas durante la operación VTT.

Cada mejora se documenta con propósito, impacto, solución propuesta, riesgos, plan de implementación y decisión solicitada al PM.

---

## Índice

| ID | Título | Categoría | Prioridad | Estimación | Estado |
|---|---|---|---|---|---|
| [IMPROVE-001](IMPROVE-001_pool_transacciones_vtt.md) | Pool de Transacciones VTT | Infrastructure | 🟡 Media | 10 días | Propuesta |
| [IMPROVE-002](IMPROVE-002_bd_manifiestos_y_tis.md) | BD para Manifiestos y TrackableItems | Database / Reporting | 🟡 Media | 7 días | Propuesta |
| [IMPROVE-003](IMPROVE-003_platform_gaps_backend_vtt.md) | Platform Gaps del Backend VTT (5 fixes tácticos) | Backend / API | 🟡 Media (2) / 🟢 Baja (3) | 2 días | Propuesta |
| [IMPROVE-004](IMPROVE-004_rules_como_feature_vtt.md) | Rules como Feature VTT (Bloque 1 Autorización) | Backend / Authorization / Governance | 🟡 Media | 15 días | Propuesta |
| [IMPROVE-005](IMPROVE-005_extension_recursos_vtt_especificos.md) | Extensión modelo a recursos VTT-específicos | Backend / Authorization (depende IMPROVE-004) | 🟡 Media | 7 días | Propuesta |
| [IMPROVE-006](IMPROVE-006_gotchas_api_assignee_y_order_deliveries.md) | Gotchas API: `assigneeId` ignorado + `order` Deliveries sin validación | Backend / API / Documentation | 🟡 Media | 1h (docs) o 4h (fix BE) | Propuesta |

---

## Tipos de mejora

| Tipo | Característica | Ejemplos |
|---|---|---|
| **Estratégica** | Cambia arquitectura, mejora capacidades transversales | IMPROVE-001, IMPROVE-002 |
| **Táctica** | Fix puntual de endpoints o features ya documentadas | IMPROVE-003 |

---

## Relaciones entre mejoras

```
IMPROVE-001 (Pool de Transacciones)
       ↕ se complementan
IMPROVE-002 (BD de Manifiestos)

  Juntas habilitan:
    - Generación automática de delivery.dynamic_model_actions
    - Dashboards PM/TL con métricas en tiempo real
    - Auditoría completa de mutaciones VTT por tarea/sprint/agente

IMPROVE-003 (Platform Gaps)
   ↕ relacionado con:
   - IMPROVE-002 resuelve GAP-VTT-04 y GAP-VTT-05 al implementarse
   - GAP-VTT-01, 02, 03 son independientes (fixes puntuales)
```

### Estrategias de implementación

| Combinación | Razón |
|---|---|
| Solo IMPROVE-003 (2 días) | Quick wins — desbloquea workarounds operacionales actuales |
| IMPROVE-001 + IMPROVE-002 juntas (17 días) | Cambio arquitectónico mayor — diseñar considerándose mutuamente |
| IMPROVE-003 → luego IMPROVE-002 | Empezar por fixes; IMPROVE-002 hereda GAP-VTT-04 resuelto |

---

## Cómo agregar una mejora nueva

1. Crear archivo `IMPROVE-NNN_titulo_snake.md` (NNN = siguiente número secuencial)
2. Usar la plantilla mínima (ver IMPROVE-001 como referencia)
3. Secciones obligatorias:
   - Header con metadata (Código, Título, Categoría, Prioridad, Estimación, Estado, Autor, Fecha, Origen)
   - §Relación con otras mejoras (si aplica)
   - §1 Problema que resuelve
   - §2 Impacto / valor
   - §3 Concepto / Solución
   - §4-N detalles técnicos
   - §Riesgos / consideraciones
   - §Plan de implementación
   - §Decisión solicitada al PM
   - §Referencias
   - §Changelog
4. Actualizar este README con la nueva entrada

---

## Estados posibles

| Estado | Significado |
|---|---|
| **Propuesta** | Documentada, pendiente de evaluación del PM |
| **Aprobada** | PM aprobó — esperando programación |
| **En desarrollo** | Convertida en tarea VTT, en ejecución |
| **Implementada** | Completada y desplegada |
| **Rechazada** | PM rechazó — documentar razón |
| **Diferida** | Aprobada pero pospuesta a release futura |

---

**Última actualización:** 2026-05-16
