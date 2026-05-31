#!/usr/bin/env python3
import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple


PHASE_INDEX_ORDER = ["00", "01", "02", "3A", "3B", "04", "05", "06", "07"]
PHASE_LABELS = {
    "00": "00-Discovery",
    "01": "01-Planning",
    "02": "02-Analysis",
    "3A": "3A-Design UX/UI",
    "3B": "3B-Design Technical",
    "04": "04-Development",
    "05": "05-Testing",
    "06": "06-Deploy",
    "07": "07-Operations",
}


def load_catalog(path: Path) -> Dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def clean_text(value: str) -> str:
    return str(value).replace("\r\n", "\n").replace("\r", "\n").strip()


def md_escape(value: str) -> str:
    return clean_text(value).replace("|", r"\|").replace("\n", "<br>")


def path_basename(path_value: str) -> str:
    return Path(clean_text(path_value)).name if clean_text(path_value) else ""


def join_dependency_ids(deliverable: Dict[str, object]) -> str:
    values = []
    for item in deliverable.get("dependencies", []):
        dep_id = clean_text(item.get("id", ""))
        if dep_id:
            values.append(dep_id)
    return ", ".join(values)


def join_agent_docs(deliverable: Dict[str, object]) -> str:
    docs: List[str] = []
    source_doc = path_basename(deliverable.get("source_file_name", "") or deliverable.get("source_file", ""))
    if source_doc:
        docs.append(source_doc)
    template_path = clean_text(deliverable.get("template_path", ""))
    if template_path:
        docs.append(template_path)
    # Preserve order and deduplicate
    result = []
    seen = set()
    for item in docs:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return ", ".join(result)


def spec_source(deliverable: Dict[str, object]) -> str:
    return path_basename(deliverable.get("markdown_file", ""))


def section_label(deliverable: Dict[str, object]) -> str:
    return "completo"


def render_phase_block(phase_label: str, deliverables: List[Dict[str, object]]) -> List[str]:
    lines: List[str] = []
    lines.append(f"## {phase_label}")
    lines.append("")
    lines.append(
        "| Deliverable ID | Nombre | Responsable | Ejecuta | Spec Source | Sección | Horas | Complejidad | Dependencias | Docs para el agente |"
    )
    lines.append(
        "|:-:|---|---|---|---|---|---:|---|---|---|"
    )

    for item in sorted(deliverables, key=lambda row: clean_text(row.get("id", ""))):
        lines.append(
            f"| {md_escape(item.get('id', ''))} | "
            f"{md_escape(item.get('name', ''))} | "
            f"{md_escape(item.get('responsible_role', '') or '—')} | "
            f"{md_escape(item.get('executor_role', '') or '—')} | "
            f"{md_escape(spec_source(item))} | "
            f"{md_escape(section_label(item))} | "
            f"{md_escape(item.get('hours', '') or 'TBD')} | "
            f"{md_escape(item.get('complexity', '') or 'TBD')} | "
            f"{md_escape(join_dependency_ids(item) or '—')} | "
            f"{md_escape(join_agent_docs(item) or '—')} |"
        )
    lines.append("")
    return lines


def build_output(catalog: Dict[str, object]) -> str:
    deliverables = catalog.get("deliverables", [])
    grouped: Dict[str, List[Dict[str, object]]] = defaultdict(list)
    for item in deliverables:
        grouped[clean_text(item.get("phase_key", ""))].append(item)

    lines: List[str] = []
    lines.append("# Índice de Ruteo de Deliverables — Estructura de Proyecto")
    lines.append("")
    lines.append("Documento derivado del catálogo SDLC enriquecido para soportar generación de estructura de proyecto, setup de sprints y handoffs.")
    lines.append("")
    lines.append("## Columnas")
    lines.append("")
    lines.append("| Columna | Qué contiene |")
    lines.append("|---------|--------------|")
    lines.append("| **Responsable** | Rol dueño del resultado final |")
    lines.append("| **Ejecuta** | Rol o agente que hace el trabajo operativo |")
    lines.append("| **Spec Source** | El archivo markdown individual del deliverable, ya separado y enriquecido |")
    lines.append("| **Sección** | `completo`, porque cada deliverable ya vive en un archivo dedicado |")
    lines.append("| **Horas** | Horas derivadas desde `typical_effort` o `TBD` si requiere decisión manual |")
    lines.append("| **Complejidad** | `LOW`, `MEDIUM`, `HIGH` o `TBD` si requiere decisión manual |")
    lines.append("| **Dependencias** | IDs de deliverables predecesores |")
    lines.append("| **Docs para el agente** | Documento fuente del diccionario + template asociado |")
    lines.append("")

    for phase_key in PHASE_INDEX_ORDER:
        items = grouped.get(phase_key, [])
        if not items:
            continue
        lines.extend(render_phase_block(PHASE_LABELS.get(phase_key, phase_key), items))

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Genera una tabla de ruteo de deliverables similar a la solicitada por PM/TL."
    )
    parser.add_argument(
        "--input",
        default="00-platform/02.normativa/catalogs/deliverables/generated/deliverables_catalog_enriched.json",
        help="Ruta del catálogo enriquecido.",
    )
    parser.add_argument(
        "--output",
        default="00-platform/02.normativa/catalogs/deliverables/generated/INDICE_RUTEO_ESTRUCTURA_PROYECTO.md",
        help="Ruta del markdown de salida.",
    )
    args = parser.parse_args()

    catalog = load_catalog(Path(args.input))
    output = build_output(catalog)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output, encoding="utf-8-sig")
    print(f"Índice de ruteo generado: {output_path}")


if __name__ == "__main__":
    main()
