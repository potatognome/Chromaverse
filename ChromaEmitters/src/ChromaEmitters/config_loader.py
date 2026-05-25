"""Deterministic ChromaEmitters config loading with .d overrides."""

from __future__ import annotations

import json
from pathlib import Path

try:
    import yaml
except Exception:
    yaml = None

try:
    from tUilKit.utils.config import ConfigLoader as _ConfigLoader
except Exception:
    _ConfigLoader = None


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_ROOT = PROJECT_ROOT / "config"
BASE_CONFIG_PATH = CONFIG_ROOT / "ChromaEmitters_CONFIG.json"
OVERRIDE_DIR = CONFIG_ROOT / "emitters.d"


def _merge_dict(base: dict, patch: dict) -> dict:
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            base[key] = _merge_dict(base[key], value)
        else:
            base[key] = value
    return base


def _load_base_config() -> dict:
    if _ConfigLoader is not None:
        loader = _ConfigLoader(config_path=str(BASE_CONFIG_PATH))
        if isinstance(loader.global_config, dict) and loader.global_config:
            return dict(loader.global_config)

    with BASE_CONFIG_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _load_override(path: Path) -> dict:
    suffix = path.suffix.lower()
    if suffix == ".json":
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    if suffix in {".yaml", ".yml"}:
        if yaml is None:
            raise RuntimeError(
                f"YAML override requires PyYAML but it is unavailable: {path}"
            )
        with path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
        return data if isinstance(data, dict) else {}

    return {}


def load_emitter_config() -> dict:
    config = _load_base_config()

    if OVERRIDE_DIR.exists():
        patterns = ["*.json", "*.yaml", "*.yml"]
        override_files = []
        for pattern in patterns:
            override_files.extend(OVERRIDE_DIR.glob(pattern))

        for path in sorted(set(override_files), key=lambda item: item.name.lower()):
            override = _load_override(path)
            config = _merge_dict(config, override)

    return config


def get_emitter_settings(config: dict, emitter_name: str) -> dict:
    emitters = config.get("emitters", {})
    settings = emitters.get(emitter_name, {})
    return settings if isinstance(settings, dict) else {}


CONFIG = load_emitter_config()
