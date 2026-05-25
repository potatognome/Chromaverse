#!/usr/bin/env python3
"""
examples/TESTS_CONFIG.py
Resolve example-suite paths for Chromagrams and emit test_paths.json.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict


HERE = Path(__file__).resolve()
PROJECT_ROOT = next((p for p in HERE.parents if (p / "pyproject.toml").exists()), HERE.parents[1])
WORKSPACE_ROOT = PROJECT_ROOT.parents[1]

SRC_ROOT = PROJECT_ROOT / "src"
TUILKIT_SRC = WORKSPACE_ROOT / "Core" / "tUilKit" / "src"
for _path in (SRC_ROOT, TUILKIT_SRC):
    _path_s = str(_path)
    if _path.exists() and _path_s not in sys.path:
        sys.path.insert(0, _path_s)


def _load_config() -> Dict:
    try:
        from tUilKit import get_config_loader

        loader = get_config_loader()
        return loader.load_config(str(PROJECT_ROOT / "config" / "Chromagrams_CONFIG.json"))
    except Exception:
        raw = (PROJECT_ROOT / "config" / "Chromagrams_CONFIG.json").read_text(encoding="utf-8")
        return json.loads(raw)


def _resolve(cfg: Dict, mode_key: str, path_key: str, fallback: str) -> Path:
    mode = str(cfg.get("ROOT_MODES", {}).get(mode_key, "project")).lower()
    base = WORKSPACE_ROOT if mode == "workspace" else PROJECT_ROOT
    rel = str(cfg.get("PATHS", {}).get(path_key, fallback))
    return (base / rel).resolve()


def main() -> int:
    cfg = _load_config()

    # Calculate tUilKit config path
    tuilkit_config_path = WORKSPACE_ROOT / "Core" / "tUilKit" / "config" / "tUilKit_CONFIG.json"

    payload = {
        "tuilkit_config_file": str(tuilkit_config_path.resolve()),
        "project_name": cfg.get("INFO", {}).get("PROJECT_NAME", "Chromagrams"),
        "config_file": str((PROJECT_ROOT / "config" / "Chromagrams_CONFIG.json").resolve()),
        "project_root": str(PROJECT_ROOT.resolve()),
        "workspace_root": str(WORKSPACE_ROOT.resolve()),
        "config_folder": str(_resolve(cfg, "CONFIG", "CONFIG", "config/")),
        "test_logs_folder": str(_resolve(cfg, "TESTS_LOGS", "TESTS_LOGS", ".tests_logs/Chromagrams/")),
        "logs_folder": str(_resolve(cfg, "LOG_PATHS", "LOG_PATHS", ".logs/Chromagrams/")),
        "tests_inputs_folder": str(_resolve(cfg, "TESTS_INPUTS", "TESTS_INPUTS", ".tests_data/")),
        "tests_outputs_folder": str(_resolve(cfg, "TESTS_OUTPUTS", "TESTS_OUTPUTS", ".tests_data/output/")),
    }

    for key in ("test_logs_folder", "tests_inputs_folder", "tests_outputs_folder"):
        Path(payload[key]).mkdir(parents=True, exist_ok=True)

    out_path = HERE.parent / "test_paths.json"
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"[TESTS_CONFIG] Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
