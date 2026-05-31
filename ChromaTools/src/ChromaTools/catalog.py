"""Config-backed application catalogue for ChromaTools."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional


@dataclass(frozen=True)
class AppRecord:
    key: str
    name: str
    app_type: str
    description: str
    entry_point: str
    project_path: Path
    config_path: Path
    launch_command: tuple[str, ...]
    enabled: bool = True

    @property
    def launchable(self) -> bool:
        return self.enabled and bool(self.launch_command)


def _resolve_path(project_root: Path, raw_path: str) -> Path:
    candidate = Path(raw_path)
    if candidate.is_absolute():
        return candidate
    return (project_root / candidate).resolve()


def load_app_catalog(config: dict, project_root: Path) -> list[AppRecord]:
    apps = []
    for key, data in sorted(config.get("APPS", {}).items()):
        apps.append(
            AppRecord(
                key=key,
                name=str(data.get("name", key)),
                app_type=str(data.get("type", "unknown")),
                description=str(data.get("description", "")).strip(),
                entry_point=str(data.get("entry_point", "")),
                project_path=_resolve_path(project_root, str(data.get("project_path", "."))),
                config_path=_resolve_path(project_root, str(data.get("config_path", "config/ChromaTools_CONFIG.json"))),
                launch_command=tuple(str(item) for item in data.get("launch_command", []) if str(item).strip()),
                enabled=bool(data.get("enabled", True)),
            )
        )
    return apps


def resolve_app(selection: str, apps: Iterable[AppRecord]) -> Optional[AppRecord]:
    choices = list(apps)
    value = selection.strip()
    if not value:
        return None

    if value.isdigit():
        index = int(value) - 1
        if 0 <= index < len(choices):
            return choices[index]

    lowered = value.lower()
    for app in choices:
        if lowered in {app.key.lower(), app.name.lower()}:
            return app
    return None

