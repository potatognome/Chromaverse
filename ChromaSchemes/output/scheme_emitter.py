"""Emit ChromaScheme output files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _to_yaml(data: Any, indent: int = 0) -> str:
    pad = " " * indent
    if isinstance(data, dict):
        lines: list[str] = []
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                lines.append(f"{pad}{key}:")
                lines.append(_to_yaml(value, indent + 2))
            else:
                lines.append(f"{pad}{key}: {json.dumps(value)}")
        return "\n".join(lines)
    if isinstance(data, list):
        lines = []
        for value in data:
            if isinstance(value, (dict, list)):
                lines.append(f"{pad}-")
                lines.append(_to_yaml(value, indent + 2))
            else:
                lines.append(f"{pad}- {json.dumps(value)}")
        return "\n".join(lines)
    return f"{pad}{json.dumps(data)}"


class ChromaSchemeEmitter:
    """Serialize scheme payloads as YAML files."""

    def emit(self, payload: dict, target_path: Path) -> Path:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(_to_yaml(payload) + "\n", encoding="utf-8")
        return target_path
