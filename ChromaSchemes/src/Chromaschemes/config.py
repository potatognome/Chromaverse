"""Configuration access for ChromaSchemes."""

from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_ROOT = PROJECT_ROOT / "config"
CONFIG_CANDIDATES = [
    CONFIG_ROOT / "ChromaSchemes_CONFIG.json",
    CONFIG_ROOT / "CHROMASCHEMES_CONFIG.json",
]
OVERRIDE_DIR = CONFIG_ROOT / "CHROMASCHEMES.d"


def _merge_dict(base: dict, patch: dict) -> dict:
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            base[key] = _merge_dict(base[key], value)
        else:
            base[key] = value
    return base


def load_config() -> dict:
    config_path = next((path for path in CONFIG_CANDIDATES if path.exists()), None)
    if config_path is None:
        print("[Chromaschemes.config] Warning: no config file found; returning empty config.")
        return {}

    with config_path.open("r", encoding="utf-8-sig") as handle:
        config = json.load(handle)

    if OVERRIDE_DIR.exists():
        for path in sorted(OVERRIDE_DIR.glob("*.json")):
            with path.open("r", encoding="utf-8-sig") as handle:
                override = json.load(handle)
            config = _merge_dict(config, override)

    return config


CONFIG = load_config()
