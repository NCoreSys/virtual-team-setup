# VTT.WORKFLOW-HO-001.011 — Emitir REVIEW_AR_CROSS_MODULE

| Campo | Valor |
|---|---|
| **Código** | `VTT.WORKFLOW-HO-001.011` |
| **Pertenece a** | `VTT.PROTOCOL-HO-001` §5.3.2 |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-06-01 |
| **Autor** | PM Martin Rivas |
| **Aplica a** | AR |
| **Tipo** | [PROCESO] sub-procedimiento de FASE 3 |

---

## 1. Propósito

AR emite review formal cross-módulo del paquete técnico 3B.1-3B.8 al cierre de FASE 2. Valida consistencia entre módulos, no calidad individual de cada 3B.X (eso lo hizo REVMA en FASE 2).

---

## 2. Inputs (estrictos)

| Nombre | Tipo | Origen | Requerido | Descripción |
|---|---|---|---|---|
| `paquete_3b` | array<path> | FASE 2 aprobada | sí | Los 8 documentos 3B.1-3B.8 |
| `spec_path` | path | FASE 1 | sí | SPEC del bloque |
| `template_review_ar` | path | templates | sí | Template canónico del REVIEW_AR |

---

## 3. Precondiciones

- Los 8 documentos 3B.1-3B.8 aprobados por REVMA.
- AR está en cadena de roles.

---

## 4. Reglas del Workflow

- **R1:** AR audita CONSISTENCIA cross-módulo, no calidad individual.
- **R2:** Si AR detecta gap en un 3B.X individual, escala para que ese 3B.X re-pase por REVMA — NO lo corrige él mismo.
- **R3:** AR firma sobre evidencia citable (referencias a sección/línea de cada 3B.X).
- **R4:** Severidad: bloqueante / mayor / menor. Bloqueantes paran FASE 3.

---

## 5. Pasos

### Paso 1 — AR valida boundaries entre módulos

Pregunta: ¿los módulos declarados en 3B.1 mantienen boundaries en 3B.2 (estructura de carpetas) y 3B.4 (endpoints)? 

Ejemplos de incoherencia:
- Módulo A accede a tablas declaradas como exclusivas del Módulo B en 3B.3.
- Módulo A importa servicios del Módulo B fuera de interfaz pública.

### Paso 2 — AR valida integraciones declaradas

Pregunta: ¿las integraciones de 3B.1 se reflejan en 3B.4 (endpoints expuestos) y 3B.8 (config externa)?

Ejemplos:
- 3B.1 declara integración con Redis. ¿3B.8 tiene Redis en infra plan? ¿3B.4 declara endpoint de health para Redis?
- 3B.1 declara webhook outbound. ¿3B.4 declara contrato del webhook? ¿3B.7 cubre auth del webhook?

### Paso 3 — AR valida coherencia ADRs vs implementación

Pregunta: ¿ADRs de 3B.6 no se contradicen con decisiones implícitas de 3B.2-3B.8?

Ejemplos:
- ADR declara "usar Promise.allSettled() para fallos parciales" pero 3B.4 declara endpoints con error code que requiere fallo total.
- ADR declara "no hay stored procedures" pero 3B.3 incluye stored procs.

### Paso 4 — AR valida cobertura Security vs superficie

Pregunta: ¿3B.7 (Security Plan) cubre TODAS las superficies expuestas en 3B.4 (endpoints)?

Ejemplos:
- 3B.4 expone endpoint público sin auth. ¿3B.7 justifica esa excepción?
- 3B.4 expone endpoint con role-based access. ¿3B.7 declara los roles?

### Paso 5 — AR valida cobertura Infra vs requerimientos

Pregunta: ¿3B.8 cubre los NFR de SPEC y los requisitos derivados de 3B.4?

Ejemplos:
- SPEC NFR-PERF-01 dice "SLA <500ms p95". ¿3B.8 tiene capacidad para sostenerlo?
- 3B.4 expone endpoint asíncrono. ¿3B.8 tiene worker/queue declarado?

### Paso 6 — AR redacta REVIEW_AR_CROSS_MODULE

Usa template canónico. Estructura:
- Resumen ejecutivo (PASA / PASA CON OBSERVACIONES / NO PASA)
- Sección por categoría auditada (boundaries, integraciones, ADRs, security, infra)
- Por cada hallazgo: descripción + cita + severidad
- Decisión final

### Paso 7 — AR firma el documento

Documento: `REVIEW_AR_<BLOQUE>_CROSS_MODULE_v1.0.md`

Si hay hallazgos bloqueantes → escala al PM, FASE 3 NO avanza hasta resolución.

---

## 6. Outputs

| Output | Tipo | Destino |
|---|---|---|
| `REVIEW_AR_<BLOQUE>_CROSS_MODULE_v1.0.md` | archivo .md | `_project-management/Fases/<BLOQUE>/` |

---

## 7. Validación

- Las 5 categorías están auditadas (boundaries, integraciones, ADRs, security, infra).
- Cada hallazgo cita evidencia.
- Decisión final clara (PASA / PASA CON OBSERVACIONES / NO PASA).
- Firma AR presente.

---

## 8. Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| Review pasa pero downstream hay inconsistencias | Auditoría superficial | Re-auditar con cita por cita |
| Hallazgos sin severidad | Olvido | Clasificar antes de firmar |
| AR corrige los 3B.X él mismo | Violación R2 | Devolver al productor del 3B.X |
| Hallazgo bloqueante ignorado | Pasa por alto | Forzar resolución antes de FASE 4 |

---

## 9. Skills invocadas

- `VTT.SKILL-ATTACH-001`

---

**Documento:** `VTT.WORKFLOW-HO-001.011_emitir_review_ar_cross_module.md`
**Versión:** 1.0.0
**Fecha:** 2026-06-01
