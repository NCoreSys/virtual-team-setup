# VTT.SKILL-CFL-001 — Lectura formal de docs canónicos + fulfill CAs

| Campo | Valor |
|---|---|
| **Código** | `VTT.SKILL-CFL-001` |
| **Categoría** | CFL (Canonical File Loader) |
| **Versión** | 1.0 |
| **Fecha** | 2026-05-31 |
| **Aplica a** | Cualquier rol que lea docs canónicos (BRIEFs/ASSIGNMENTs/OPERATIVOs/SPECs) o reporte fulfill CAs |
| **Tokens estimados** | ~140 |
| **Cuándo se usa** | Lectura inicial de inputs (paso 2-3 del WORKFLOW-ASG-001.031) + fulfill final (paso 8 del .034 + paso 1 del .010) |

---

## Inputs (contractuales)

| Nombre | Tipo | Requerido | Descripción |
|---|---|---|---|
| `document_path` | path | sí (modo lectura) | Path absoluto al doc |
| `verify_sections` | array | opcional | Secciones obligatorias a validar |
| `task_id` | string | sí (modo fulfill) | TASK_ID |
| `criteria_id` | UUID | sí (modo fulfill) | criteriaId del CA |
| `status` | enum | sí (modo fulfill) | `met`/`not_met`/`na` |
| `evidence` | string | sí (modo fulfill) | Descripción concreta + path/url/SHA |
| `notes` | string | opcional | Notas opcionales |

## Precondición

- `$VTT_TOKEN` vigente
- Modo lectura: archivo existe en `document_path`

## Variables del entorno

- `$VTT_TOKEN`
- `$VTT_BASE_URL`

## Reglas

| # | Regla |
|---|---|
| R1 | Leer documento COMPLETO — sin saltos, sin filtros |
| R2 | Si `verify_sections` especificado, validar cada sección presente |
| R3 | Endpoint fulfill correcto: `PATCH /api/tasks/:id/criteria/:cid` (NO `POST /fulfill` — 404) |
| R4 | `evidence` concreta — path/url/SHA/comando |
| R5 | `status=na` requiere justificación en `notes` |

## Ejecución

### Modo lectura
```bash
cat "$DOCUMENT_PATH"
# Si verify_sections activo:
for s in "${VERIFY_SECTIONS[@]}"; do
  grep -q "## $s" "$DOCUMENT_PATH" || { echo "FALTA: $s"; exit 1; }
done
```

### Modo fulfill CA
```bash
curl -X PATCH "$VTT_BASE_URL/api/tasks/$TASK_ID/criteria/$CRITERIA_ID" \
  -H "Authorization: Bearer $VTT_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"status\":\"$STATUS\",\"evidence\":\"$EVIDENCE\",\"notes\":\"$NOTES\"}"
```

## Validación

### Modo lectura
HTTP exit 0 + secciones obligatorias presentes.

### Modo fulfill
HTTP 200 + criterio actualizado.

## Error común

- HTTP 404 con `POST /fulfill` → usar `PATCH /criteria/:cid`
- Archivo no existe → verificar path absoluto
- Sección obligatoria faltante → escalar al PM/TL

## Scripts invocados

- `SCRIPT-CFL-001_fulfill_ca.py` (modo fulfill)

## Changelog

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-05-31 | Versión inicial. Dual-mode: lectura formal + fulfill canónico. |
