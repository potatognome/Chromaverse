"""Config loading for ChromaTools with optional override fragments."""

from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_ROOT = PROJECT_ROOT / "config"
BASE_CONFIG_PATH = CONFIG_ROOT / "ChromaTools_CONFIG.json"
OVERRIDE_DIR = CONFIG_ROOT / "CHROMATOOLS.d"


def _merge_dict(base: dict, patch: dict) -> dict:
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            base[key] = _merge_dict(base[key], value)
        else:
            base[key] = value
    return base


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    return data if isinstance(data, dict) else {}


def load_config() -> dict:
    config = _load_json(BASE_CONFIG_PATH)
    if OVERRIDE_DIR.exists():
        for path in sorted(OVERRIDE_DIR.glob("*.json")):
            config = _merge_dict(config, _load_json(path))
    return config


CONFIG = load_config()

