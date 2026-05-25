"""Chromagrams exemplar — living behaviour documentation for public APIs.

Run directly (outside pytest) to exercise normal and adversarial paths,
stress menu/UI edge cases, and produce colour-logged output for human review.

Usage
-----
    python examples/exemplar.py
"""

from __future__ import annotations

import json
import importlib.util
import math
import subprocess
import sys
from pathlib import Path

# Bootstrap paths from TESTS_CONFIG for policy alignment.
_HERE = Path(__file__).resolve()
_TESTS_CONFIG = _HERE.parent / "TESTS_CONFIG.py"
_TEST_PATHS = _HERE.parent / "test_paths.json"
if not _TEST_PATHS.exists():
    subprocess.run([sys.executable, str(_TESTS_CONFIG)], check=True)

_PATHS = json.loads(_TEST_PATHS.read_text(encoding="utf-8"))
_REPO_ROOT = Path(_PATHS["project_root"])
_SRC = _REPO_ROOT / "src"
_TUILKIT_SRC = _REPO_ROOT.parent / "tUilKit" / "src"
for _path in (_SRC, _TUILKIT_SRC):
    _path_s = str(_path)
    if _path.exists() and _path_s not in sys.path:
        sys.path.insert(0, _path_s)

# ---------------------------------------------------------------------------
# tUilKit factory imports (verbose mode where available)
# ---------------------------------------------------------------------------
from tUilKit.utils.config import ConfigLoader
from tUilKit.utils.output import ColourManager, Logger

# Initialize ConfigLoader with explicit tUilKit config path
_TUILKIT_CONFIG = Path(_PATHS.get("tuilkit_config_file", str(_REPO_ROOT.parent / "tUilKit" / "config" / "tUilKit_CONFIG.json")))
_config_loader = ConfigLoader(config_path=str(_TUILKIT_CONFIG))
_colour = ColourManager(_config_loader.load_colour_config())
_logger = Logger(_colour)
_HAS_TUILKIT = True

# ---------------------------------------------------------------------------
# Chromagrams config (loaded directly to avoid triggering the Dev namespace)
# ---------------------------------------------------------------------------
_config_spec = importlib.util.spec_from_file_location(
    "chromagrams_config", str(_SRC / "Chromagrams" / "config.py")
)
_config_mod = importlib.util.module_from_spec(_config_spec)
_config_spec.loader.exec_module(_config_mod)
CONFIG = _config_mod.CONFIG
BASE_CONFIG_PATH = _config_mod.BASE_CONFIG_PATH
OVERRIDE_DIR = _config_mod.OVERRIDE_DIR

# ---------------------------------------------------------------------------
# Sequence imports — gracefully degrade when Dev namespace is absent
# ---------------------------------------------------------------------------
try:
    from Chromagrams.sequences.fireplace import FireplaceBurnSequence
    from Chromagrams.sequences.pulse import PulseSequence
    _HAS_SEQUENCES = True
except ModuleNotFoundError:
    # Dev.Chromaspace not installed in this environment; exercise logic inline
    _HAS_SEQUENCES = False


# ---------------------------------------------------------------------------
# Minimal colour-log helper (falls back to plain print when tUilKit absent)
# ---------------------------------------------------------------------------

def _log(key: str, msg: str) -> None:
    if _HAS_TUILKIT:
        try:
            print(_colour.colour_str(key, msg))
            return
        except Exception:
            pass
    print(f"[{key}] {msg}")


# ---------------------------------------------------------------------------
# Inline fallback logic (mirrors fireplace.py without the registry decorator)
# ---------------------------------------------------------------------------

_NOISE_PHASE_OFFSET = 1.2345678


def _trig_noise(phase: float, harmonics: int) -> float:
    value = 0.0
    norm = 0.0
    for k in range(1, harmonics + 1):
        value += math.sin(k * phase + k * _NOISE_PHASE_OFFSET) / k
        norm += 1.0 / k
    return value / norm


def _make_fireplace_frames(
    count: int,
    flicker_speed: float | None = None,
    defaults: dict | None = None,
) -> list[dict]:
    d = defaults or CONFIG.get("FIREPLACE_DEFAULTS", {})
    hue_min = float(d.get("HUE_MIN", 0.0))
    hue_max = float(d.get("HUE_MAX", 0.083))
    sat_base = float(d.get("SATURATION_BASE", 0.85))
    sat_range = float(d.get("SATURATION_RANGE", 0.12))
    bri_base = float(d.get("BRIGHTNESS_BASE", 0.75))
    bri_range = float(d.get("BRIGHTNESS_RANGE", 0.20))
    flicker_range = float(d.get("FLICKER_RANGE", 0.15))
    harmonics = int(d.get("FLICKER_HARMONICS", 6))
    flicker_cycles = float(d.get("FLICKER_CYCLES", 8.0))
    fs = float(flicker_speed if flicker_speed is not None else d.get("FLICKER_SPEED_SCALE", 0.7))
    two_pi = 2.0 * math.pi
    frames = []
    for idx in range(count):
        phase = idx / count if count else 0.0
        smooth = (1.0 - math.cos(two_pi * phase)) / 2.0
        hue = hue_min + smooth * (hue_max - hue_min)
        bri_bf = bri_base + bri_range * math.sin(two_pi * phase)
        sat = sat_base + sat_range * math.sin(two_pi * phase + math.pi / 4.0)
        fp = phase * fs * two_pi * flicker_cycles
        noise = _trig_noise(fp, harmonics)
        fi = (noise + 1.0) / 2.0
        bri = bri_bf + flicker_range * noise
        frames.append({
            "hue": round(max(0.0, min(1.0, hue)), 6),
            "saturation": round(max(0.0, min(1.0, sat)), 6),
            "brightness": round(max(0.0, min(1.0, bri)), 6),
            "phase": round(phase, 6),
            "flicker_intensity": round(max(0.0, min(1.0, fi)), 6),
        })
    return frames


# ---------------------------------------------------------------------------
# Config section
# ---------------------------------------------------------------------------

def _section_config() -> None:
    _log("!info", "─── Config ─────────────────────────────────────────────")
    _log("!path", f"Base config  : {BASE_CONFIG_PATH}")
    _log("!path", f"Override dir : {OVERRIDE_DIR}")

    version = CONFIG.get("INFO", {}).get("VERSION", "?")
    _log("!data", f"Project version: {version}")

    root_modes = CONFIG.get("ROOT_MODES", {})
    _log("!info", f"ROOT_MODES loaded — {len(root_modes)} entries")

    log_files = CONFIG.get("LOG_FILES", {})
    _log("!info", f"LOG_FILES loaded — {len(log_files)} entries")
    for name, filename in log_files.items():
        _log("!file", f"  {name}: {filename}")

    fireplace_defaults = CONFIG.get("FIREPLACE_DEFAULTS", {})
    _log("!info", f"FIREPLACE_DEFAULTS — {len(fireplace_defaults)} keys")
    for key, val in fireplace_defaults.items():
        _log("!data", f"  {key}: {val}")


# ---------------------------------------------------------------------------
# FireplaceBurnSequence section
# ---------------------------------------------------------------------------

def _section_fireplace() -> None:
    _log("!info", "─── FireplaceBurnSequence ───────────────────────────────")

    if _HAS_SEQUENCES:
        seq: object = FireplaceBurnSequence()
        make = seq.generate_frames
    else:
        _log("!warn", "Dev.Chromaspace not found — exercising inline logic fallback")
        _fp_defaults = CONFIG.get("FIREPLACE_DEFAULTS", {})
        _default_count = round(
            _fp_defaults.get("DURATION", 12.0) * _fp_defaults.get("FPS", 60.0)
        )

        def make(frame_count: int | None = None, flicker_speed_scale: float | None = None, **_kw) -> list[dict]:
            return _make_fireplace_frames(
                frame_count if frame_count is not None else _default_count,
                flicker_speed=flicker_speed_scale,
            )

    # --- Normal paths ---
    frames = make(frame_count=12)
    _log("!proc", f"frame_count=12 → {len(frames)} frames")
    _log("!data", f"  First frame : {frames[0]}")
    _log("!data", f"  Last frame  : {frames[-1]}")

    frames2 = make(frame_count=12)
    _log(
        "!pass" if frames == frames2 else "!fail",
        "Determinism check",
    )

    long_frames = make(frame_count=720)
    _log("!proc", f"frame_count=720 → {len(long_frames)} frames")

    # flicker speed variations
    slow = make(frame_count=60, flicker_speed_scale=0.3)
    fast = make(frame_count=60, flicker_speed_scale=1.5)
    _log("!proc", f"flicker 0.3  sample brightness: {slow[10]['brightness']:.4f}")
    _log("!proc", f"flicker 1.5  sample brightness: {fast[10]['brightness']:.4f}")
    _log(
        "!pass" if any(s["brightness"] != f["brightness"] for s, f in zip(slow, fast)) else "!fail",
        "Flicker speed alters brightness",
    )

    # Range validation
    all_ok = all(0.0 <= f["hue"] <= 1.0 and 0.0 <= f["brightness"] <= 1.0 for f in long_frames)
    _log("!pass" if all_ok else "!fail", "All values in [0.0, 1.0]")

    palette_ok = all(f["hue"] <= 0.083 + 1e-9 for f in long_frames)
    _log("!pass" if palette_ok else "!fail", "Hue stays in warm palette [0.0, 0.083]")

    keys_ok = all(
        {"hue", "saturation", "brightness", "phase", "flicker_intensity"} == set(f.keys())
        for f in frames
    )
    _log("!pass" if keys_ok else "!fail", "Frame keys correct")

    # --- Adversarial / edge paths ---
    empty = make(frame_count=0)
    _log("!pass" if len(empty) == 0 else "!fail", f"frame_count=0 → {len(empty)} frames")

    single = make(frame_count=1)
    _log("!pass" if len(single) == 1 else "!fail", f"frame_count=1 → {single}")

    large = make(frame_count=10_000)
    _log("!pass" if len(large) == 10_000 else "!fail", f"frame_count=10000 → {len(large)} frames")

    zero_flicker = make(frame_count=8, flicker_speed_scale=0.0)
    _log("!pass" if len(zero_flicker) == 8 else "!fail", f"flicker_speed_scale=0.0 → {len(zero_flicker)} frames")


# ---------------------------------------------------------------------------
# PulseSequence section
# ---------------------------------------------------------------------------

def _section_pulse() -> None:
    _log("!info", "─── PulseSequence ───────────────────────────────────────")

    if not _HAS_SEQUENCES:
        _log("!warn", "Dev.Chromaspace not found — skipping PulseSequence section")
        return

    seq = PulseSequence()
    frames = seq.generate_frames()
    _log("!proc", f"Default generate_frames() → {len(frames)} frames")
    _log("!data", f"  Values: {frames}")
    _log(
        "!pass" if seq.generate_frames() == frames else "!fail",
        "PulseSequence determinism check",
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    _log("!info", "═══════════════════════════════════════════════════════")
    _log("!info", "  Chromagrams Exemplar")
    _log("!info", "═══════════════════════════════════════════════════════")

    _section_config()
    _section_fireplace()
    _section_pulse()

    _log("!done", "Exemplar complete.")


if __name__ == "__main__":
    main()

