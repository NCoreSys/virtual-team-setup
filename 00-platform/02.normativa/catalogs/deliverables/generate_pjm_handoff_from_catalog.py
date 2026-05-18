#!/usr/bin/env python3
import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


PHASE_ORDER = ["00", "01", "02", "3A", "3B", "04", "05", "06", "07"]


def md_escape(value: str) -> str:
    return value.replace("|", r"\|").replace("\n", "<br>")


def join_dependency_ids(deliverable: dict) -> str:
    ids = [item.get("id", "") for item in deliverable.get("dependencies", []) if item.get("id")]
    return ", ".join(ids) if ids else ""


def load_catalog(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_phase_summary(deliverables: list) -> list:
    grouped = defaultdict(list)
    for item in deliverables:
        grouped[item.get("phase_key", "")].append(item)

    rows = []
    for key in PHASE_ORDER:
        items = grouped.get(key, [])
        if not items:
            continue
        phase_name = items[0].get("phase", "")
        required = sum(1 for item in items if item.get("required") == "required")
        optional = sum(1 for item in items if item.get("required") == "optional")
        rows.append((key, phase_name, len(items), required, optional))
    return rows


def render_handoff(catalog: dict) -> str:
    deliverables = catalog.get("deliverables", [])
    project = catalog.get("project", {})
    summary = catalog.get("summary", {})
    generated_at = catalog.get("generated_at", "")

    grouped = defaultdict(list)
    for item in deliverables:
        grouped[item.get("phase_key", "")].append(item)

    lines = []
    lines.append("# HANDOFF — PJM: Catálogo SDLC para Configuración de Deliverables")
    lines.append("")
    lines.append("| Campo | Valor |")
    lines.append("|-------|-------|")
    lines.append("| **Documento** | HO_PJM_CONFIGURACION_DELIVERABLES_SDLC.md |")
    lines.append("| **Fecha de generación** | " + md_escape(generated_at) + " |")
    lines.append("| **Origen** | deliverables_catalog.json |")
    lines.append("| **Estado** | Borrador técnico generado desde diccionarios SDLC |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 1. Objetivo")
    lines.append("")
    lines.append("Entregar al PJM una fuente estructurada del catálogo SDLC para configurar deliverables, dependencias y trazabilidad en VTT a partir de los diccionarios de `configuracion_deliverables`.")
    lines.append("")
    lines.append("Este HO expone explícitamente los faltantes que siguen pendientes antes de una carga final en VTT:")
    lines.append("")
    lines.append(f"- `hours` vacíos: **{summary.get('missing_field_counts', {}).get('hours', 0)}**")
    lines.append(f"- `complexity` vacíos: **{summary.get('missing_field_counts', {}).get('complexity', 0)}**")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 2. Datos de Proyecto VTT")
    lines.append("")
    lines.append("| Campo | Valor |")
    lines.append("|-------|-------|")
    lines.append(f"| **Project ID VTT** | `{project.get('project_id_vtt', '')}` |")
    for phase_name, phase_id in project.get("phase_ids_vtt", {}).items():
        lines.append(f"| **Phase ID VTT — {md_escape(phase_name)}** | `{phase_id}` |")
    lines.append("")
    lines.append("### 2.1 UUIDs del equipo")
    lines.append("")
    lines.append("| Rol | UUID VTT |")
    lines.append("|-----|----------|")
    for role, uuid in project.get("team_uuids", {}).items():
        lines.append(f"| {md_escape(role)} | `{uuid}` |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 3. Resumen del Catálogo")
    lines.append("")
    lines.append("| Fase | Nombre | Deliverables | Obligatorios | Opcionales |")
    lines.append("|------|--------|--------------|--------------|------------|")
    for key, phase_name, total, required, optional in build_phase_summary(deliverables):
        lines.append(f"| {key} | {md_escape(phase_name)} | {total} | {required} | {optional} |")
    lines.append("")
    lines.append(f"**Total deliverables extraídos:** {summary.get('deliverables', 0)}")
    lines.append("")
    lines.append(f"**Total dependencias trazadas:** {len(catalog.get('dependency_edges', []))}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 4. Campos mínimos por Deliverable")
    lines.append("")
    lines.append("Cada deliverable quedó normalizado con estos campos:")
    lines.append("")
    lines.append("- `id`")
    lines.append("- `name`")
    lines.append("- `responsible_role`")
    lines.append("- `executor_role`")
    lines.append("- `required`")
    lines.append("- `typical_effort`")
    lines.append("- `hours`")
    lines.append("- `complexity`")
    lines.append("- `dependencies`")
    lines.append("")
    lines.append("Regla aplicada: cuando el documento no trae el campo, el JSON deja `\"\"` en texto y `[]` en listas.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 5. Deliverables por Fase")
    lines.append("")

    for phase_key in PHASE_ORDER:
        items = grouped.get(phase_key, [])
        if not items:
            continue
        phase_name = items[0].get("phase", "")
        lines.append(f"### {phase_key} — {phase_name}")
        lines.append("")
        lines.append("| ID | Deliverable | Responsable | Ejecuta | Obligatorio | Esfuerzo típico | Horas | Complejidad | Dependencias |")
        lines.append("|----|-------------|-------------|---------|-------------|-----------------|-------|-------------|--------------|")
        for item in sorted(items, key=lambda row: row.get("id", "")):
            lines.append(
                f"| {md_escape(item.get('id', ''))} | {md_escape(item.get('name', ''))} | {md_escape(item.get('responsible_role', ''))} | "
                f"{md_escape(item.get('executor_role', ''))} | {md_escape(item.get('required', ''))} | {md_escape(item.get('typical_effort', ''))} | "
                f"{md_escape(item.get('hours', ''))} | {md_escape(item.get('complexity', ''))} | {md_escape(join_dependency_ids(item))} |"
            )
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 6. Dependencias Trazadas")
    lines.append("")
    lines.append("| From | To | Requirement | Notes |")
    lines.append("|------|----|-------------|-------|")
    for edge in catalog.get("dependency_edges", []):
        lines.append(
            f"| {md_escape(edge.get('from', ''))} | {md_escape(edge.get('to', ''))} | {md_escape(edge.get('requirement', ''))} | {md_escape(edge.get('notes', ''))} |"
        )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 7. Próximo Paso Operativo")
    lines.append("")
    lines.append("Antes de usar este catálogo para carga final en VTT o para un Project Plan ejecutable del PJM, completar:")
    lines.append("")
    lines.append("1. `project_id_vtt`")
    lines.append("2. `phase_ids_vtt` por fase")
    lines.append("3. `team_uuids` por rol")
    lines.append("4. `hours` por deliverable")
    lines.append("5. `complexity` por deliverable")
    lines.append("")
    lines.append("Una vez completados esos campos, este catálogo ya puede servir como base directa para:")
    lines.append("")
    lines.append("- generación de seed de deliverables/tareas")
    lines.append("- HO operativo de carga VTT")
    lines.append("- trazabilidad de dependencias entre deliverables")
    lines.append("")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera un HO PJM a partir del catálogo JSON de deliverables.")
    parser.add_argument(
        "--input",
        default="00-platform/04.Process/configuracion_deliverables/deliverables_catalog.json",
        help="Ruta del JSON canónico.",
    )
    parser.add_argument(
        "--output",
        default="00-platform/04.Process/configuracion_deliverables/HO_PJM_CONFIGURACION_DELIVERABLES_SDLC.md",
        help="Ruta del markdown de salida.",
    )
    args = parser.parse_args()

    catalog = load_catalog(Path(args.input))
    markdown = render_handoff(catalog)
    output_path = Path(args.output)
    output_path.write_text(markdown, encoding="utf-8")
    print(f"HO generado: {output_path}")
    print(f"Fecha: {datetime.now(timezone.utc).isoformat()}")


if __name__ == "__main__":
    main()
