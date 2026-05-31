#!/usr/bin/env python3
import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple


MANUAL_KEYWORDS = (
    "continuo",
    "variable",
    "incluido",
    "automático",
    "automatico",
    "por sprint",
    "por integración",
    "por integracion",
    "día/trimestre",
    "dias/trimestre",
    "día por",
    "dias por",
    "+",
)

INVALID_FILENAME_CHARS = '<>:"/\\|?*'
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
PHASE_INDEX_ORDER = ["00", "01", "02", "3A", "3B", "04", "05", "06", "07"]


def load_catalog(path: Path) -> Dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def clean_text(value: str) -> str:
    return value.replace("\r\n", "\n").replace("\r", "\n").strip()


def markdown_escape(value: str) -> str:
    return clean_text(value).replace("|", r"\|")


def sanitize_filename(value: str) -> str:
    sanitized = value
    for char in INVALID_FILENAME_CHARS:
        sanitized = sanitized.replace(char, " ")
    sanitized = re.sub(r"\s+", " ", sanitized).strip()
    return sanitized


def derive_hours_from_effort(typical_effort: str) -> Tuple[Optional[float], str]:
    raw = clean_text(typical_effort)
    lowered = raw.lower()

    if not raw:
        return None, "Esfuerzo típico vacío"

    if any(keyword in lowered for keyword in MANUAL_KEYWORDS):
        return None, f"Requiere decisión manual TL/PM por patrón contextual: {raw}"

    normalized = re.sub(r"\([^)]*\)", "", lowered)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    normalized = normalized.replace("días", "día").replace("dias", "día")

    range_match = re.fullmatch(r"(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*día", normalized)
    if range_match:
        start = float(range_match.group(1))
        end = float(range_match.group(2))
        midpoint_days = (start + end) / 2
        return midpoint_days * 8, f"Promedio de rango {start:g}-{end:g} días"

    single_day_match = re.fullmatch(r"(\d+(?:\.\d+)?)\s*día", normalized)
    if single_day_match:
        days = float(single_day_match.group(1))
        return days * 8, f"Conversión directa de {days:g} día(s)"

    hour_match = re.fullmatch(r"(\d+(?:\.\d+)?)\s*h", normalized)
    if hour_match:
        hours = float(hour_match.group(1))
        return hours, f"Conversión directa de {hours:g}h"

    return None, f"No se pudo derivar automáticamente desde: {raw}"


def derive_complexity_from_hours(hours: Optional[float]) -> Optional[str]:
    if hours is None:
        return None
    if hours <= 4:
        return "LOW"
    if hours <= 16:
        return "MEDIUM"
    return "HIGH"


def format_hours(hours: Optional[float]) -> str:
    if hours is None:
        return "TBD por TL/PM"
    if abs(hours - round(hours)) < 1e-9:
        return f"{int(round(hours))}h"
    return f"{hours:.1f}h"


def render_bullet_section(title: str, values: List[str]) -> List[str]:
    lines = [f"**{title}:**"]
    if values:
        for value in values:
            lines.append(f"- {value}")
    else:
        lines.append("- N/A")
    lines.append("")
    return lines


def render_dependency_lines(items: List[Dict[str, str]], include_requirement: bool) -> List[str]:
    rendered: List[str] = []
    for item in items:
        raw = clean_text(item.get("raw", ""))
        if raw:
            rendered.append(raw)
            continue

        identifier = clean_text(item.get("id", ""))
        name = clean_text(item.get("name", ""))
        notes = clean_text(item.get("notes", ""))
        requirement = clean_text(item.get("requirement", ""))

        base = f"`{identifier}` {name}".strip() if identifier else name
        if include_requirement and requirement:
            base += f" *({requirement})*"
        if notes:
            base += f" — {notes}"
        rendered.append(base.strip())
    return rendered


def render_audience_lines(items: List[Dict[str, str]]) -> List[str]:
    rendered: List[str] = []
    for item in items:
        raw = clean_text(item.get("raw", ""))
        if raw:
            rendered.append(raw)
            continue
        role = clean_text(item.get("role", ""))
        usage = clean_text(item.get("usage", ""))
        if role and usage:
            rendered.append(f"**{role}** — {usage}")
        elif role:
            rendered.append(f"**{role}**")
        elif usage:
            rendered.append(usage)
    return rendered


def render_anti_pattern_lines(items: List[Dict[str, str]]) -> List[str]:
    rendered: List[str] = []
    for item in items:
        raw = clean_text(item.get("raw", ""))
        if raw:
            rendered.append(raw)
            continue
        name = clean_text(item.get("name", ""))
        description = clean_text(item.get("description", ""))
        if name and description:
            rendered.append(f"❌ **{name}:** {description}")
        elif description:
            rendered.append(description)
    return rendered


def render_deliverable_markdown(deliverable: Dict[str, object]) -> str:
    hours_value = deliverable.get("hours_derived")
    hours_display = clean_text(str(deliverable.get("hours", ""))) or "TBD por TL/PM"
    complexity = clean_text(str(deliverable.get("complexity", ""))) or "TBD por TL/PM"
    estimation_status = deliverable.get("estimation_status", "")
    estimation_note = clean_text(str(deliverable.get("estimation_note", "")))

    lines: List[str] = []
    lines.append(f"### {deliverable['id']} {deliverable['name']}")
    lines.append("")
    lines.append("| Campo | Valor |")
    lines.append("|-------|-------|")
    lines.append(f"| **Fase** | {markdown_escape(str(deliverable.get('phase', '')))} |")
    lines.append(f"| **Subfase** | {markdown_escape(str(deliverable.get('subphase', '')))} |")
    lines.append(f"| **Responsable** | {markdown_escape(str(deliverable.get('responsible_role', '')))} |")
    lines.append(f"| **Ejecuta** | {markdown_escape(str(deliverable.get('executor_role', '')))} |")
    lines.append(f"| **Aprueba** | {markdown_escape(str(deliverable.get('approver_role', '')))} |")
    lines.append(f"| **Formato** | {markdown_escape(str(deliverable.get('format', '')))} |")
    lines.append(f"| **Obligatorio** | {markdown_escape(str(deliverable.get('required_raw', '')))} |")
    lines.append(f"| **Esfuerzo típico** | {markdown_escape(str(deliverable.get('typical_effort', '')))} |")
    lines.append(f"| **Horas** | {hours_display} |")
    lines.append(f"| **Complejidad** | {complexity} |")
    lines.append(f"| **Frecuencia** | {markdown_escape(str(deliverable.get('frequency', '')))} |")
    lines.append("")

    lines.append(f"**Perfil de ejecución:** {clean_text(str(deliverable.get('execution_profile', 'N/A')))}")
    lines.append("")
    lines.append(f"**Qué es:** {clean_text(str(deliverable.get('what_is', 'N/A')))}")
    lines.append("")
    lines.append(f"**Para qué sirve:** {clean_text(str(deliverable.get('purpose', 'N/A')))}")
    lines.append("")

    lines.extend(render_bullet_section("Inputs requeridos", [clean_text(value) for value in deliverable.get("inputs_required", [])]))
    lines.extend(render_bullet_section("Dependencias (predecessors)", render_dependency_lines(deliverable.get("dependencies", []), include_requirement=True)))
    lines.extend(render_bullet_section("Habilita (successors)", render_dependency_lines(deliverable.get("successors", []), include_requirement=False)))

    audience_lines = render_audience_lines(deliverable.get("audience", []))
    if audience_lines:
        lines.extend(render_bullet_section("Audiencia", audience_lines))

    expected_sections = [clean_text(value) for value in deliverable.get("expected_sections", [])]
    if expected_sections:
        lines.append("**Secciones esperadas:**")
        for index, value in enumerate(expected_sections, start=1):
            lines.append(f"{index}. {value}")
        lines.append("")

    completion = [clean_text(value) for value in deliverable.get("completion_criteria", [])]
    lines.append("**Criterio de completitud:**")
    if completion:
        for value in completion:
            lines.append(f"- [ ] {value}")
    else:
        lines.append("- [ ] N/A")
    lines.append("")

    anti_patterns = render_anti_pattern_lines(deliverable.get("anti_patterns", []))
    lines.extend(render_bullet_section("Anti-patrones", anti_patterns))

    template_path = clean_text(str(deliverable.get("template_path", ""))) or "pendiente"
    lines.append(f"**Template:** `{template_path}`")
    lines.append("")

    lines.append("**Metadata de estimación:**")
    lines.append(f"- Estado: `{estimation_status}`")
    if estimation_note:
        lines.append(f"- Nota: {estimation_note}")
    lines.append("")

    if estimation_status != "derived":
        lines.append("**Pendiente TL/PM:**")
        lines.append("- Confirmar horas reales para este entregable.")
        lines.append("- Confirmar complejidad final a usar en VTT.")
        lines.append("")

    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def build_filename(deliverable: Dict[str, object]) -> str:
    title = sanitize_filename(str(deliverable["name"]))
    identifier = sanitize_filename(str(deliverable["id"]))
    return f"{identifier} - {title}.md"


def enrich_deliverable(deliverable: Dict[str, object], markdown_dir: Path) -> Dict[str, object]:
    enriched = dict(deliverable)
    enriched["hours_original"] = deliverable.get("hours", "")
    enriched["complexity_original"] = deliverable.get("complexity", "")
    hours, note = derive_hours_from_effort(str(deliverable.get("typical_effort", "")))
    complexity = derive_complexity_from_hours(hours)
    enriched["hours_derived"] = hours
    enriched["hours_derived_display"] = format_hours(hours)
    enriched["complexity_derived"] = complexity
    enriched["complexity_vtt"] = complexity
    enriched["hours"] = format_hours(hours) if hours is not None else ""
    enriched["complexity"] = complexity or ""
    enriched["estimation_note"] = note
    enriched["estimation_status"] = "derived" if hours is not None else "pending_tl"
    enriched["markdown_file"] = str(markdown_dir / build_filename(enriched))
    return enriched


def write_markdown_files(deliverables: List[Dict[str, object]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for deliverable in deliverables:
        target = output_dir / build_filename(deliverable)
        target.write_text(render_deliverable_markdown(deliverable), encoding="utf-8-sig")


def write_index_file(deliverables: List[Dict[str, object]], output_dir: Path) -> Path:
    grouped = defaultdict(lambda: defaultdict(list))
    for deliverable in deliverables:
        phase_key = clean_text(str(deliverable.get("phase_key", "")))
        phase = PHASE_LABELS.get(phase_key, clean_text(str(deliverable.get("phase", ""))) or "Sin fase")
        subphase = clean_text(str(deliverable.get("subphase", ""))) or "Sin subfase"
        grouped[phase][subphase].append(deliverable)

    def phase_sort_key(name: str) -> Tuple[str, str]:
        reverse = {label: key for key, label in PHASE_LABELS.items()}
        key = reverse.get(name, "ZZ")
        try:
            order_index = PHASE_INDEX_ORDER.index(key)
        except ValueError:
            order_index = 999
        return (f"{order_index:03d}", name)

    lines: List[str] = []
    lines.append("# Índice de Deliverables SDLC")
    lines.append("")
    lines.append(f"- Total de entregables: **{len(deliverables)}**")
    lines.append(f"- Generado: `{datetime.now(timezone.utc).isoformat()}`")
    lines.append("")
    lines.append("## Fases")
    lines.append("")
    for phase in sorted(grouped.keys(), key=phase_sort_key):
        total_phase = sum(len(items) for items in grouped[phase].values())
        anchor = re.sub(r"[^a-z0-9]+", "-", phase.lower()).strip("-")
        lines.append(f"- [{phase}](#{anchor}) ({total_phase})")
    lines.append("")

    for phase in sorted(grouped.keys(), key=phase_sort_key):
        total_phase = sum(len(items) for items in grouped[phase].values())
        lines.append(f"## {phase}")
        lines.append("")
        lines.append(f"Total: **{total_phase}**")
        lines.append("")
        for subphase in sorted(grouped[phase].keys()):
            items = sorted(grouped[phase][subphase], key=lambda item: str(item.get("id", "")))
            lines.append(f"### {subphase}")
            lines.append("")
            for deliverable in items:
                filename = build_filename(deliverable)
                lines.append(
                    f"- [{deliverable['id']} {deliverable['name']}](./{filename})"
                )
            lines.append("")

    index_path = output_dir / "index.md"
    index_path.write_text("\n".join(lines), encoding="utf-8-sig")
    return index_path


def build_summary(deliverables: List[Dict[str, object]]) -> Dict[str, object]:
    status_counter = Counter(str(item.get("estimation_status", "")) for item in deliverables)
    phase_counter = Counter(str(item.get("phase_key", "")) for item in deliverables)
    return {
        "deliverables": len(deliverables),
        "by_phase_key": dict(sorted(phase_counter.items())),
        "estimation_status": dict(sorted(status_counter.items())),
        "derived_hours_count": sum(1 for item in deliverables if item.get("hours_derived") is not None),
        "pending_tl_count": sum(1 for item in deliverables if item.get("estimation_status") != "derived"),
    }


def export_catalog(input_path: Path, json_output: Path, markdown_dir: Path) -> None:
    catalog = load_catalog(input_path)
    deliverables = [
        enrich_deliverable(item, markdown_dir) for item in catalog.get("deliverables", [])
    ]

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_catalog": str(input_path),
        "summary": build_summary(deliverables),
        "project": catalog.get("project", {}),
        "source_files": catalog.get("source_files", []),
        "dependency_edges": catalog.get("dependency_edges", []),
        "deliverables": deliverables,
    }

    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8-sig")
    write_markdown_files(deliverables, markdown_dir)
    index_path = write_index_file(deliverables, markdown_dir)

    print(f"JSON generado: {json_output}")
    print(f"Archivos markdown generados: {len(deliverables)} en {markdown_dir}")
    print(f"Índice generado: {index_path}")
    print(f"Entregables con horas derivadas: {payload['summary']['derived_hours_count']}")
    print(f"Entregables pendientes TL/PM: {payload['summary']['pending_tl_count']}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Genera 438 archivos markdown individuales y un JSON enriquecido desde deliverables_catalog.json."
    )
    parser.add_argument(
        "--input",
        default="00-platform/02.normativa/catalogs/deliverables/deliverables_catalog.json",
        help="Ruta del catálogo JSON base.",
    )
    parser.add_argument(
        "--json-output",
        default="00-platform/02.normativa/catalogs/deliverables/generated/deliverables_catalog_enriched.json",
        help="Ruta del JSON enriquecido de salida.",
    )
    parser.add_argument(
        "--markdown-dir",
        default="00-platform/02.normativa/catalogs/deliverables/generated/individual_md",
        help="Carpeta donde se escribirán los markdown individuales.",
    )
    args = parser.parse_args()

    export_catalog(
        input_path=Path(args.input),
        json_output=Path(args.json_output),
        markdown_dir=Path(args.markdown_dir),
    )


if __name__ == "__main__":
    main()
