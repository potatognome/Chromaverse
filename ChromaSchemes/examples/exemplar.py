#!/usr/bin/env python3
"""ChromaSchemes exemplar — menu-driven behaviour documentation."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Iterable

HERE = Path(__file__).resolve()
TEST_PATHS = HERE.parent / "test_paths.json"
if TEST_PATHS.exists():
    try:
        PATHS = json.loads(TEST_PATHS.read_text(encoding="utf-8"))
    except Exception:
        PATHS = {}
else:
    PATHS = {}

PROJECT_ROOT = Path(PATHS.get("project_root", HERE.parents[1])).resolve()
if not PROJECT_ROOT.exists():
    PROJECT_ROOT = HERE.parents[1].resolve()

WORKSPACE_ROOT = Path(PATHS.get("workspace_root", PROJECT_ROOT.parents[1])).resolve()
CONFIG_FILE = Path(PATHS.get("config_file", PROJECT_ROOT / "config" / "ChromaSchemes_CONFIG.json")).resolve()
if not CONFIG_FILE.exists():
    CONFIG_FILE = (PROJECT_ROOT / "config" / "ChromaSchemes_CONFIG.json").resolve()

SRC_ROOT = PROJECT_ROOT / "src"
REPO_ROOT = PROJECT_ROOT.parent
for p in (SRC_ROOT, REPO_ROOT):
    ps = str(p)
    if p.exists() and ps not in sys.path:
        sys.path.insert(0, ps)

try:
    # tUilKit factory imports in verbose mode where available.
    from tUilKit.utils.config import ConfigLoader
    from tUilKit.utils.output import ColourManager, Logger

    TUILKIT_CONFIG = Path(PATHS.get("tuilkit_config_file", str(WORKSPACE_ROOT / "tUilKit" / "config" / "tUilKit_CONFIG.json")))
    config_loader = ConfigLoader(config_path=str(TUILKIT_CONFIG))
    colour_manager = ColourManager(config_loader.load_colour_config())
    logger = Logger(colour_manager)
    HAS_TUILKIT = True
except Exception:
    config_loader = None
    colour_manager = None
    logger = None
    HAS_TUILKIT = False

from Chromaschemes import ChromaSchemesEngine  # noqa: E402


if config_loader is not None:
    try:
        CONFIG = config_loader.load_config(str(CONFIG_FILE))
    except Exception:
        try:
            CONFIG = json.loads(CONFIG_FILE.read_text(encoding="utf-8-sig"))
        except Exception:
            CONFIG = {}
else:
    try:
        CONFIG = json.loads(CONFIG_FILE.read_text(encoding="utf-8-sig"))
    except Exception:
        CONFIG = {}


def _log(key: str, message: str) -> None:
    if HAS_TUILKIT and colour_manager is not None:
        try:
            print(colour_manager.colour_str(key, message))
            return
        except Exception:
            pass
    print(f"[{key}] {message}")


def _pick(mapping: dict, keys: Iterable[str], default: str) -> str:
    for key in keys:
        value = mapping.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return default


def _resolve_any(mode_keys: Iterable[str], path_keys: Iterable[str], fallback: str) -> Path:
    modes = CONFIG.get("ROOT_MODES", {}) if isinstance(CONFIG.get("ROOT_MODES"), dict) else {}
    paths = CONFIG.get("PATHS", {}) if isinstance(CONFIG.get("PATHS"), dict) else {}
    mode = _pick(modes, mode_keys, "project").lower().strip()
    base = WORKSPACE_ROOT if mode == "workspace" else PROJECT_ROOT
    rel = _pick(paths, path_keys, fallback)
    return (base / rel).resolve()


def show_config_and_paths() -> None:
    _log("!proc", "Config and path inspection")
    _log("!path", f"Primary config file: {CONFIG_FILE}")

    root_modes = CONFIG.get("ROOT_MODES", {}) if isinstance(CONFIG.get("ROOT_MODES"), dict) else {}
    for key, value in root_modes.items():
        _log("!data", f"ROOT_MODE[{key}] = {value}")

    log_root = _resolve_any(("LOGS", "LOG_PATHS"), ("LOGS", "LOG_PATHS"), ".logs/ChromaSchemes/")
    cfg_root = _resolve_any(("CONFIG",), ("CONFIG",), "config/")
    input_root = _resolve_any(("INPUTS", "INPUT_DATA"), ("INPUTS", "INPUT_DATA"), ".projects_data/input_data/")

    _log("!path", f"Resolved logs path: {log_root}")
    _log("!path", f"Resolved config path: {cfg_root}")
    _log("!path", f"Resolved input path: {input_root}")

    log_files = CONFIG.get("LOG_FILES", {}) if isinstance(CONFIG.get("LOG_FILES"), dict) else {}
    for key, value in log_files.items():
        _log("!file", f"LOG_FILE[{key}] -> {log_root / str(value)}")


def _generate_payload(geometry_model: str, desired_colour_count: int) -> dict:
    return {
        "baseColour": {"hex": "#FF78C8", "space": "rgb"},
        "geometryModel": geometry_model,
        "overlays": [
            {"type": "harmonic", "params": {"rotation": 45}},
            {"type": "luminance_wheel", "params": {"amplitude": 0.08}},
            {"type": "chroma_spiral", "params": {"step": 0.01}},
        ],
        "desiredColourCount": desired_colour_count,
    }


def run_engine_demos() -> None:
    _log("!proc", "Engine demonstrations")
    engine = ChromaSchemesEngine()

    for model in ("quadratic", "triadic", "tetradic", "split_complementary", "harmonic"):
        payload = _generate_payload(model, 8)
        result = engine.generate(payload)
        _log("!done", f"{model} -> colourSet size {len(result['colourSet'])}, pane count {len(result['preview']['panes'])}")


def run_edge_cases() -> None:
    _log("!proc", "Edge-case stress checks")
    engine = ChromaSchemesEngine()

    checks = [
        ("empty-input", _generate_payload("quadratic", 1)),
        ("long-count", _generate_payload("quadratic", 24)),
        ("custom-geometry", {
            "baseColour": {"hex": "#112233", "space": "rgb"},
            "geometryModel": "custom",
            "geometryParams": {"offsets": [0, 33, 121, 202]},
            "desiredColourCount": 12,
        }),
    ]

    for name, payload in checks:
        result = engine.generate(payload)
        _log("!pass", f"{name}: generated {len(result['colourSet'])} colours")

    try:
        engine.generate({"baseColour": {"hex": "#XYZ123", "space": "rgb"}, "geometryModel": "quadratic"})
        _log("!fail", "Invalid hex unexpectedly accepted")
    except Exception as exc:
        _log("!pass", f"Invalid hex rejected: {exc}")


def emit_sample_file() -> None:
    _log("!proc", "Emit sample scheme output")
    engine = ChromaSchemesEngine()
    output_path = PROJECT_ROOT / "samples" / "generated.exemplar.scheme.yaml"
    emitted = engine.emit(_generate_payload("quadratic", 8), output_path)
    _log("!done", f"Wrote {emitted}")


def menu_loop() -> None:
    while True:
        _log("!list", "1. Config and path report")
        _log("!list", "2. Engine demos")
        _log("!list", "3. Edge-case stress checks")
        _log("!list", "4. Emit sample output")
        _log("!list", "5. Exit")
        choice = input("Select option (1-5): ").strip()

        if choice == "1":
            show_config_and_paths()
        elif choice == "2":
            run_engine_demos()
        elif choice == "3":
            run_edge_cases()
        elif choice == "4":
            emit_sample_file()
        elif choice == "5":
            _log("!done", "Exiting exemplar")
            return
        else:
            _log("!error", "Invalid choice")


def main() -> int:
    _log("!info", "═══════════════════════════════════════════════════════")
    _log("!info", " ChromaSchemes Exemplar")
    _log("!info", "═══════════════════════════════════════════════════════")
    if HAS_TUILKIT:
        _log("!done", "Loaded tUilKit factories in verbose exemplar mode")
    else:
        _log("!warn", "tUilKit unavailable; running fallback logging mode")
    menu_loop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
