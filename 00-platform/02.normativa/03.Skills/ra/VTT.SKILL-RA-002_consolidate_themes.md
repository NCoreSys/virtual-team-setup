# VTT.SKILL-RA-002 — Consolidate themes cross-extracts

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-RA-002` |
| **Categoría** | RA (Research Analyst) |
| **Versión** | 1.0 |
| **Fecha** | 2026-06-02 |
| **Aplica a** | Research Analyst (RA) |
| **Tokens estimados** | ~280 |
| **Cuándo se usa** | Paso 2 del pipeline RA — UNA invocación por feature (cruza los N EXTRACTs de esa feature) |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `extracts_paths` | array<path> | sí | Lista de N EXTRACTs ya generados (Paso 1) de la misma feature |
| `feature_name` | string (kebab-case) | sí | Nombre de la feature |
| `output_dir` | path | sí | Dónde escribir THEMES (típicamente la misma carpeta de los EXTRACTs) |
| `template_path` | path | sí | Path a `TEMPLATE_THEMES_CONSOLIDATED.md` |

---

## Precondición

- Los N EXTRACTs ya están generados (Paso 1 completo)
- Cada EXTRACT cumple `VTT.SKILL-RA-001` (8 marcadores + Impacto + citas literales)
- El template `template_path` existe
- El RA tiene en contexto los dominios típicos del cruce temático (ver §Ejecución)

> **Si falta algún EXTRACT del feature** (ej. 5 de 6) → ABORT y reportar al Coordinator. NO consolidar incompleto.

---

## Variables del entorno

```bash
$VTT_SETUP          # path al repo virtual-teams-setup/00-platform/
```

---

## Ejecución

### Lógica de consolidación temática (paso a paso)

1. **Leer los N EXTRACTs completos** — no escanear

2. **Construir índice temático inverso** — para cada recomendación de cada EXTRACT, identificar a qué dominio pertenece:

   | Dominio | Heurística (palabras clave + contexto) |
   |---|---|
   | Arquitectura | "patrón", "estructura", "modelo", "control plane", "diseño macro" |
   | Tecnología (stack) | nombres de tecnologías concretas (Restate, Temporal, Postgres, etc.) |
   | Migración | "paulatinamente", "primero X después Y", "fallback", "deprecación" |
   | Seguridad / Governance | "OWASP", "RBAC", "ABAC", "SoD", "auditoría", "compliance" |
   | Performance / Escalabilidad | throughput, latencia, p99, p95, throughput, IOPS |
   | Observabilidad / Monitoreo | "métricas", "logs", "tracing", "alertas", "dashboards" |
   | Human-in-the-loop | "approval", "HITL", "gate", "supervisión humana" |
   | Costos / Model Routing | "token cost", "model routing", "tier", "precio" |
   | Otros | si la heurística no clasifica, crear dominio nuevo en §2.9 |

3. **Detectar consensos cross-extracto** — recomendaciones que aparecen en **3+ EXTRACTs** de la misma feature. Son las señales más fuertes para el FEATURE_SPEC.

4. **Detectar conflictos cross-extracto** — recomendaciones donde 2+ EXTRACTs contradicen entre sí (un bloque dice A, otro dice B sobre el mismo tema). Diferenciar de las DIVERGENCIAS dentro de un EXTRACT (que están en §2.8 del template EXTRACT).

5. **Detectar dependencias cross-feature** — "para hacer X (bloque A) primero hay que resolver Y (bloque B)". Importante para el orden de implementación.

6. **Consolidar GAPs** — los `[GAP-DETECTADO]` que aparecen en 2+ EXTRACTs son problemas reales que VTT debe atender.

7. **Consolidar datos duros** — si dos EXTRACTs reportan el mismo dato con valores distintos → conflicto en §4 del THEMES.

8. **Generar §8 Decisiones pendientes PM** — resumen de conflictos + ambigüedades que requieren decisión humana.

9. **Rellenar las 10 secciones del TEMPLATE_THEMES_CONSOLIDATED.md**.

10. **Validar output**: dominios cubiertos, consensos detectados (≥3 ítems en proyectos típicos), conflictos listados, dependencias mapeadas.

### Comando (Bash)

```bash
# Variables
EXTRACTS_DIR="<output_dir del Paso 1>"
FEATURE="<feature_name>"
TEMPLATE="$VTT_SETUP/03.templates/research/TEMPLATE_THEMES_CONSOLIDATED.md"
OUTFILE="$EXTRACTS_DIR/THEMES_${FEATURE}.md"

# Validar precondición: deben existir todos los EXTRACTs del feature
ls "$EXTRACTS_DIR"/EXTRACT_${FEATURE}_*.md | wc -l
# Si el conteo NO coincide con N esperado → ABORT

# Setup
cp "$TEMPLATE" "$OUTFILE"

# Pasos 1-9: el agente RA cruza los EXTRACTs cognitivamente y rellena $OUTFILE

# Validación post-ejecución
grep -c "^### 2\." "$OUTFILE"   # subsecciones de dominio (deberían ser 8-9)
grep -c "## 3. Consensos cross-extracto" "$OUTFILE" && echo "§3 OK"
grep -c "## 4. Conflictos cross-extracto" "$OUTFILE" && echo "§4 OK"
```

---

## Validación

| Check | Cómo verificar |
|---|---|
| Todos los dominios cubiertos | §2 tiene 8+ subsecciones con contenido |
| Consensos detectados | §3 lista recomendaciones con `Aparece en: HM-XX, HM-YY, HM-ZZ` |
| Conflictos listados con posturas claras | §4 muestra "Postura A vs Postura B + extractos que sostienen cada una" |
| Dependencias cross-feature mapeadas | §5 con grafo o lista de orden |
| Decisiones PM consolidadas | §8 con tabla |
| Stats §9 coherentes con el contenido | Conteos cruzan |

---

## Error común

| Error | Causa | Solución |
|---|---|---|
| THEMES muy plano (sin consensos detectados) | El RA no cruzó realmente los EXTRACTs, solo los listó | Re-procesar mirando la misma recomendación en N archivos a la vez |
| Conflictos confundidos con divergencias | Diferencia: divergencia = dentro de 1 extracto (entre los 4 modelos); conflicto = entre EXTRACTs distintos | Releer definiciones en §3-§4 del template |
| Dominios inventados / duplicados | Usar los 8 estándar (§2.1 a §2.8); el 2.9 es para Otros | Auditar y consolidar |
| Subsecciones §2.X vacías | Decisión: si un dominio no tiene recomendaciones, dejar explícitamente "Sin recomendaciones en este dominio" | Honestidad — no inflar |

---

## Scripts invocados

Sin scripts externos — skill cognitiva. El bash de §Ejecución solo valida pre/post.

---

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-06-02 | Versión inicial. Cruce temático de N EXTRACTs → 1 THEMES siguiendo `TEMPLATE_THEMES_CONSOLIDATED.md`. 8 dominios estándar + dominios `Otros`. Consensos (3+ EXTRACTs coinciden) + conflictos cross-extracto + dependencias cross-feature + decisiones pendientes PM. Origen: pipeline RA paso 2. |
