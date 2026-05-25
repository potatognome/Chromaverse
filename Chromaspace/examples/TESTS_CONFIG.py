#!/usr/bin/env python3
"""
examples/TESTS_CONFIG.py
Resolve Chromaspace example-suite paths from project config.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable


HERE = Path(__file__).resolve()
PROJECT_ROOT = next((p for p in HERE.parents if (p / "pyproject.toml").exists()), HERE.parents[1])
WORKSPACE_ROOT = PROJECT_ROOT.parents[1]
CONFIG_DIR = PROJECT_ROOT / "config"

SRC_ROOT = PROJECT_ROOT / "src"
TUILKIT_SRC = WORKSPACE_ROOT / "Core" / "tUilKit" / "src"
for _path in (SRC_ROOT, TUILKIT_SRC):
    _path_s = str(_path)
    if _path.exists() and _path_s not in sys.path:
        sys.path.insert(0, _path_s)


def _find_primary_config(config_dir: Path) -> Path:
    files = sorted(config_dir.glob("*_CONFIG.json"))
    non_secondary = [p for p in files if "SECONDARY" not in p.name.upper()]
    if non_secondary:
        return non_secondary[0]
    if files:
        return files[0]
    raise FileNotFoundError(f"No *_CONFIG.json found in {config_dir}")


def _load_config(config_path: Path) -> Dict[str, Any]:
    try:
        from tUilKit import get_config_loader

        loader = get_config_loader()
        return loader.load_config(str(config_path))
    except Exception:
        return json.loads(config_path.read_text(encoding="utf-8"))


def _pick(d: Dict[str, Any], keys: Iterable[str], default: str = "") -> str:
    for key in keys:
        value = d.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return default


def _resolve(cfg: Dict[str, Any], mode_key: str, path_keys: Iterable[str], fallback: str) -> Path:
    modes = cfg.get("ROOT_MODES", {}) if isinstance(cfg.get("ROOT_MODES", {}), dict) else {}
    paths = cfg.get("PATHS", {}) if isinstance(cfg.get("PATHS", {}), dict) else {}

    mode = str(modes.get(mode_key, "project")).lower().strip()
    base = WORKSPACE_ROOT if mode == "workspace" else PROJECT_ROOT
    rel = _pick(paths, path_keys, fallback)
    return (base / rel).resolve()


def main() -> int:
    config_file = _find_primary_config(CONFIG_DIR)
    cfg = _load_config(config_file)

    # Calculate tUilKit config path
    tuilkit_config_path = WORKSPACE_ROOT / "Core" / "tUilKit" / "config" / "tUilKit_CONFIG.json"

    payload = {
        "tuilkit_config_file": str(tuilkit_config_path.resolve()),
        "project_name": str(cfg.get("INFO", {}).get("PROJECT_NAME", PROJECT_ROOT.name)),
        "config_file": str(config_file.resolve()),
        "project_root": str(PROJECT_ROOT.resolve()),
        "workspace_root": str(WORKSPACE_ROOT.resolve()),
        "config_folder": str(_resolve(cfg, "CONFIG", ("CONFIG",), "config/")),
        "test_logs_folder": str(_resolve(cfg, "TESTS_LOGS", ("TESTS_LOGS", "TEST_LOGS"), ".tests_logs/Chromaspace/")),
        "logs_folder": str(_resolve(cfg, "LOG_PATHS", ("LOG_PATHS", "LOGS"), ".logs/Chromaspace/")),
        "tests_inputs_folder": str(_resolve(cfg, "TESTS_INPUTS", ("TESTS_INPUTS",), ".tests_data/inputs/")),
        "tests_outputs_folder": str(_resolve(cfg, "TESTS_OUTPUTS", ("TESTS_OUTPUTS",), ".tests_data/output/")),
    }

    for key in ("test_logs_folder", "tests_inputs_folder", "tests_outputs_folder"):
        Path(payload[key]).mkdir(parents=True, exist_ok=True)

    out = HERE.parent / "test_paths.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"[TESTS_CONFIG] Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
