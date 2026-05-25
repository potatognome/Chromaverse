"""Chromaschemes config loading with optional .d overrides."""

from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_ROOT = PROJECT_ROOT / "config"
BASE_CONFIG_PATH = CONFIG_ROOT / "CHROMASCHEMES_CONFIG.json"
OVERRIDE_DIR = CONFIG_ROOT / "CHROMASCHEMES.d"


def _merge_dict(base: dict, patch: dict) -> dict:
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            base[key] = _merge_dict(base[key], value)
        else:
            base[key] = value
    return base


def load_config() -> dict:
    with BASE_CONFIG_PATH.open("r", encoding="utf-8") as handle:
        config = json.load(handle)

    if OVERRIDE_DIR.exists():
        for path in sorted(OVERRIDE_DIR.glob("*.json")):
            with path.open("r", encoding="utf-8") as handle:
                override = json.load(handle)
            config = _merge_dict(config, override)

    return config


CONFIG = load_config()
