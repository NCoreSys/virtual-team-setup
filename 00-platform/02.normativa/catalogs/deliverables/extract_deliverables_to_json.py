#!/usr/bin/env python3
import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


DELIVERABLE_HEADING_RE = re.compile(r"^###\s+([0-9A-Z][0-9A-Za-z.\-]*)\s+(.+?)\s*$", re.MULTILINE)
TABLE_ROW_RE = re.compile(r"^\|\s*\*\*(.+?)\*\*\s*\|\s*(.*?)\s*\|\s*$", re.MULTILINE)
PHASE_HEADER_RE = re.compile(r"^#\s+DICCIONARIO DE DELIVERABLES.+FASE\s+(.+?)\s*$", re.MULTILINE)
TOTAL_DELIVERABLES_RE = re.compile(r"^\*\*Total deliverables:\*\*\s*(\d+)", re.MULTILINE)
SUBPHASE_HEADER_RE = re.compile(r"^##\s+([0-9A-Z.]+)\s+(.+?)\s*$", re.MULTILINE)
PROJECT_PLACEHOLDER_PHASES = [
    ("00", "Discovery"),
    ("01", "Planning"),
    ("02", "Analysis"),
    ("3A", "Design UX/UI"),
    ("3B", "Design Technical"),
    ("04", "Development"),
    ("05", "Testing"),
    ("06", "Deploy"),
    ("07", "Operations"),
]
PROJECT_PLACEHOLDER_PHASE_MAP = {key: f"{key}-{name}" for key, name in PROJECT_PLACEHOLDER_PHASES}


@dataclass
class SourceFileSummary:
    path: str
    phase_header: str
    deliverable_count: int
    declared_deliverables: str


def clean_text(value: str) -> str:
    value = value.replace("\r\n", "\n").replace("\r", "\n")
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def normalize_required(value: str) -> Tuple[str, bool]:
    text = clean_text(value)
    if "✅" in text:
        return "required", True
    if "⚪" in text or "opcional" in text.lower():
        return "optional", False
    return "", False


def normalize_role(value: str) -> str:
    return clean_text(value).replace(" / ", " / ")


def derive_phase_key(phase_value: str) -> str:
    match = re.match(r"^(03A|03B|[0-9]A|[0-9]B|[0-9]{2}|[0-9])", phase_value, re.IGNORECASE)
    if not match:
        return ""
    raw = match.group(1).upper()
    if raw == "03A":
        return "3A"
    if raw == "03B":
        return "3B"
    if len(raw) == 1 and raw.isdigit():
        return raw.zfill(2)
    return raw


def split_roles(value: str) -> List[str]:
    if not value:
        return []
    parts = re.split(r"\s*/\s*|\s*\+\s*|\s*,\s*|\s+y\s+", value)
    return [clean_text(part) for part in parts if clean_text(part)]


def derive_subphase_key(subphase_value: str) -> str:
    match = re.match(r"^([0-9]+(?:[AB])?(?:\.[0-9]+)?)", subphase_value)
    return match.group(1) if match else ""


def extract_labeled_sections(section_text: str) -> Dict[str, str]:
    labels = [
        "Perfil de ejecución",
        "Qué es",
        "Para qué sirve",
        "Inputs requeridos",
        "Dependencias (predecessors)",
        "Habilita (successors)",
        "Audiencia",
        "Secciones esperadas",
        "Criterio de completitud",
        "Anti-patrones",
        "Template",
    ]
    positions: List[Tuple[str, int, int]] = []
    for label in labels:
        pattern = re.compile(rf"\*\*{re.escape(label)}:\*\*")
        match = pattern.search(section_text)
        if match:
            positions.append((label, match.start(), match.end()))
    positions.sort(key=lambda item: item[1])

    extracted: Dict[str, str] = {label: "" for label in labels}
    for index, (label, start, end) in enumerate(positions):
        next_start = positions[index + 1][1] if index + 1 < len(positions) else len(section_text)
        extracted[label] = clean_text(section_text[end:next_start])
    return extracted


def parse_bullet_list(raw_text: str) -> List[str]:
    items: List[str] = []
    for line in raw_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            items.append(clean_text(stripped[2:]))
    return items


def parse_numbered_list(raw_text: str) -> List[str]:
    items: List[str] = []
    for line in raw_text.splitlines():
        stripped = line.strip()
        match = re.match(r"^\d+\.\s+(.+)$", stripped)
        if match:
            items.append(clean_text(match.group(1)))
    return items


def parse_checklist(raw_text: str) -> List[str]:
    items: List[str] = []
    for line in raw_text.splitlines():
        stripped = line.strip()
        match = re.match(r"^- \[[ xX]\]\s+(.+)$", stripped)
        if match:
            items.append(clean_text(match.group(1)))
    return items


def parse_dependencies(raw_text: str) -> List[Dict[str, str]]:
    dependencies: List[Dict[str, str]] = []
    for item in parse_bullet_list(raw_text):
        if clean_text(item).lower().startswith("ninguna"):
            continue
        dep_id = ""
        dep_name = item
        requirement = ""
        notes = ""

        id_match = re.search(r"`([^`]+)`", item)
        if id_match:
            dep_id = clean_text(id_match.group(1))
            dep_name = clean_text(re.sub(r"`[^`]+`", "", item, count=1))
        requirement_match = re.search(r"\*\(([^)]+)\)\*", item)
        if requirement_match:
            requirement = clean_text(requirement_match.group(1))
            dep_name = clean_text(re.sub(r"\*\([^)]+\)\*", "", dep_name))

        if "—" in dep_name:
            name_part, notes_part = dep_name.split("—", 1)
            dep_name = clean_text(name_part)
            notes = clean_text(notes_part)
        elif " - " in dep_name:
            name_part, notes_part = dep_name.split(" - ", 1)
            dep_name = clean_text(name_part)
            notes = clean_text(notes_part)

        dependencies.append(
            {
                "id": dep_id,
                "name": dep_name,
                "requirement": requirement,
                "notes": notes,
                "raw": item,
            }
        )
    return dependencies


def parse_successors(raw_text: str) -> List[Dict[str, str]]:
    successors: List[Dict[str, str]] = []
    for item in parse_bullet_list(raw_text):
        if clean_text(item).lower().startswith("ninguna"):
            continue
        succ_id = ""
        succ_name = item
        notes = ""

        id_match = re.search(r"`([^`]+)`", item)
        if id_match:
            succ_id = clean_text(id_match.group(1))
            succ_name = clean_text(re.sub(r"`[^`]+`", "", item, count=1))

        if "—" in succ_name:
            name_part, notes_part = succ_name.split("—", 1)
            succ_name = clean_text(name_part)
            notes = clean_text(notes_part)
        elif " - " in succ_name:
            name_part, notes_part = succ_name.split(" - ", 1)
            succ_name = clean_text(name_part)
            notes = clean_text(notes_part)

        successors.append(
            {
                "id": succ_id,
                "name": succ_name,
                "notes": notes,
                "raw": item,
            }
        )
    return successors


def parse_audience(raw_text: str) -> List[Dict[str, str]]:
    audience: List[Dict[str, str]] = []
    for item in parse_bullet_list(raw_text):
        role = ""
        usage = item
        match = re.match(r"^\*\*(.+?)\*\*\s+[—-]\s+(.+)$", item)
        if match:
            role = clean_text(match.group(1))
            usage = clean_text(match.group(2))
        audience.append({"role": role, "usage": usage, "raw": item})
    return audience


def parse_anti_patterns(raw_text: str) -> List[Dict[str, str]]:
    anti_patterns: List[Dict[str, str]] = []
    for item in parse_bullet_list(raw_text):
        name = ""
        description = item
        match = re.match(r"^❌\s+\*\*(.+?)\*\*:\s+(.+)$", item)
        if match:
            name = clean_text(match.group(1))
            description = clean_text(match.group(2))
        anti_patterns.append({"name": name, "description": description, "raw": item})
    return anti_patterns


def parse_template(raw_text: str) -> str:
    match = re.search(r"`([^`]+)`", raw_text)
    return clean_text(match.group(1)) if match else clean_text(raw_text)


def extract_phase_header(text: str) -> str:
    match = PHASE_HEADER_RE.search(text)
    return clean_text(match.group(1)) if match else ""


def extract_declared_deliverables(text: str) -> str:
    match = TOTAL_DELIVERABLES_RE.search(text)
    return match.group(1) if match else ""


def infer_hours(metadata: Dict[str, str]) -> str:
    effort = metadata.get("Esfuerzo típico", "")
    if not effort:
        return ""
    only_hours = re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*h\s*", effort, re.IGNORECASE)
    return only_hours.group(1) if only_hours else ""


def parse_markdown_file(path: Path) -> Tuple[SourceFileSummary, List[Dict[str, object]]]:
    text = path.read_text(encoding="utf-8")
    matches = list(DELIVERABLE_HEADING_RE.finditer(text))
    phase_header = extract_phase_header(text)
    declared_deliverables = extract_declared_deliverables(text)
    deliverables: List[Dict[str, object]] = []

    for index, match in enumerate(matches):
        section_start = match.start()
        section_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        section_text = text[section_start:section_end]

        metadata = {clean_text(key): clean_text(value) for key, value in TABLE_ROW_RE.findall(section_text)}
        labeled = extract_labeled_sections(section_text)
        deliverable_id = clean_text(match.group(1))
        deliverable_name = clean_text(match.group(2))
        phase_value = metadata.get("Fase", phase_header)
        subphase_value = metadata.get("Subfase", "")
        required_label, required_bool = normalize_required(metadata.get("Obligatorio", ""))

        deliverable = {
            "id": deliverable_id,
            "name": deliverable_name,
            "phase": phase_value,
            "phase_key": derive_phase_key(phase_value),
            "subphase": subphase_value,
            "subphase_key": derive_subphase_key(subphase_value),
            "responsible_role": normalize_role(metadata.get("Responsable", "")),
            "executor_role": normalize_role(metadata.get("Ejecuta", "")),
            "approver_role": normalize_role(metadata.get("Aprueba", "")),
            "format": metadata.get("Formato", ""),
            "required": required_label,
            "required_bool": required_bool,
            "required_raw": metadata.get("Obligatorio", ""),
            "typical_effort": metadata.get("Esfuerzo típico", ""),
            "hours": infer_hours(metadata),
            "complexity": "",
            "frequency": metadata.get("Frecuencia", ""),
            "execution_profile": labeled.get("Perfil de ejecución", ""),
            "what_is": labeled.get("Qué es", ""),
            "purpose": labeled.get("Para qué sirve", ""),
            "inputs_required": parse_bullet_list(labeled.get("Inputs requeridos", "")),
            "dependencies": parse_dependencies(labeled.get("Dependencias (predecessors)", "")),
            "successors": parse_successors(labeled.get("Habilita (successors)", "")),
            "audience": parse_audience(labeled.get("Audiencia", "")),
            "expected_sections": parse_numbered_list(labeled.get("Secciones esperadas", "")),
            "completion_criteria": parse_checklist(labeled.get("Criterio de completitud", "")),
            "anti_patterns": parse_anti_patterns(labeled.get("Anti-patrones", "")),
            "template_path": parse_template(labeled.get("Template", "")),
            "project_id_vtt": "",
            "phase_id_vtt": "",
            "source_file": str(path),
            "source_file_name": path.name,
            "raw_metadata": metadata,
            "missing_fields": [],
        }

        required_fields = [
            "id",
            "name",
            "phase",
            "subphase",
            "responsible_role",
            "executor_role",
            "approver_role",
            "format",
            "required",
            "typical_effort",
            "frequency",
            "hours",
            "complexity",
        ]
        deliverable["missing_fields"] = [field for field in required_fields if not deliverable.get(field)]
        deliverables.append(deliverable)

    summary = SourceFileSummary(
        path=str(path),
        phase_header=phase_header,
        deliverable_count=len(deliverables),
        declared_deliverables=declared_deliverables,
    )
    return summary, deliverables


def build_team_uuid_placeholders(deliverables: List[Dict[str, object]]) -> Dict[str, str]:
    roles = set()
    for deliverable in deliverables:
        for key in ("responsible_role", "executor_role", "approver_role"):
            value = str(deliverable.get(key, ""))
            for part in split_roles(value):
                if part:
                    roles.add(part)
    return {role: "" for role in sorted(roles)}


def build_phase_uuid_placeholders(deliverables: List[Dict[str, object]]) -> Dict[str, str]:
    return {label: "" for label in PROJECT_PLACEHOLDER_PHASE_MAP.values()}


def build_dependency_edges(deliverables: List[Dict[str, object]]) -> List[Dict[str, str]]:
    edges: Dict[Tuple[str, str, str], Dict[str, str]] = {}
    for deliverable in deliverables:
        target_id = str(deliverable["id"])
        for dependency in deliverable.get("dependencies", []):
            source_id = dependency.get("id", "")
            if not source_id:
                continue
            key = (source_id, target_id, dependency.get("requirement", ""))
            edges[key] = {
                "from": source_id,
                "to": target_id,
                "requirement": dependency.get("requirement", ""),
                "notes": dependency.get("notes", ""),
                "source": "predecessor",
            }
        for successor in deliverable.get("successors", []):
            target = successor.get("id", "")
            if not target:
                continue
            key = (target_id, target, "")
            edges.setdefault(
                key,
                {
                    "from": target_id,
                    "to": target,
                    "requirement": "",
                    "notes": successor.get("notes", ""),
                    "source": "successor",
                },
            )
    return sorted(edges.values(), key=lambda edge: (edge["from"], edge["to"]))


def build_summary(deliverables: List[Dict[str, object]], files: List[SourceFileSummary]) -> Dict[str, object]:
    required_counter = Counter(str(item.get("required", "")) for item in deliverables)
    phase_counter = Counter(str(item.get("phase_key", "")) for item in deliverables)
    missing_counter = Counter()
    for item in deliverables:
        missing_counter.update(item.get("missing_fields", []))

    return {
        "source_files": len(files),
        "deliverables": len(deliverables),
        "by_phase_key": dict(sorted(phase_counter.items())),
        "required": required_counter.get("required", 0),
        "optional": required_counter.get("optional", 0),
        "missing_field_counts": dict(sorted(missing_counter.items())),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Extrae deliverables SDLC a JSON normalizado.")
    parser.add_argument(
        "--source-dir",
        default="00-platform/04.Process/configuracion_deliverables",
        help="Carpeta con los diccionarios markdown.",
    )
    parser.add_argument(
        "--output",
        default="00-platform/04.Process/configuracion_deliverables/deliverables_catalog.json",
        help="Ruta del JSON de salida.",
    )
    args = parser.parse_args()

    source_dir = Path(args.source_dir)
    output_path = Path(args.output)
    files = sorted(source_dir.glob("DICCIONARIO_*.md"))

    file_summaries: List[SourceFileSummary] = []
    deliverables: List[Dict[str, object]] = []

    for file_path in files:
        summary, parsed_deliverables = parse_markdown_file(file_path)
        file_summaries.append(summary)
        deliverables.extend(parsed_deliverables)

    team_uuids = build_team_uuid_placeholders(deliverables)
    phase_ids_vtt = build_phase_uuid_placeholders(deliverables)
    dependency_edges = build_dependency_edges(deliverables)

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_dir": str(source_dir),
        "project": {
            "project_id_vtt": "",
            "phase_ids_vtt": phase_ids_vtt,
            "team_uuids": team_uuids,
        },
        "summary": build_summary(deliverables, file_summaries),
        "source_files": [summary.__dict__ for summary in file_summaries],
        "deliverables": deliverables,
        "dependency_edges": dependency_edges,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"JSON generado: {output_path}")
    print(f"Archivos procesados: {len(file_summaries)}")
    print(f"Deliverables extraídos: {len(deliverables)}")
    print(f"Dependencias trazadas: {len(dependency_edges)}")


if __name__ == "__main__":
    main()
