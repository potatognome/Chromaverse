"""Adapter that routes colour conversions through ChromaSpace."""

from __future__ import annotations

import colorsys
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[2]
CHROMASPACE_SRC = REPO_ROOT / "Chromaspace" / "src"
if CHROMASPACE_SRC.exists() and str(CHROMASPACE_SRC) not in sys.path:
    sys.path.insert(0, str(CHROMASPACE_SRC))

try:
    from Chromaspace.colour_spaces.hsv import hsv_to_rgb  # type: ignore  # noqa: E402
    from Chromaspace.colour_spaces.oklch import to_rgb as oklch_to_rgb  # type: ignore  # noqa: E402
except Exception:
    hsv_to_rgb = None
    oklch_to_rgb = None


class ChromaSpaceAdapter:
    """Colour space conversions for deterministic ChromaSchemes generation."""

    @staticmethod
    def hex_to_rgb(hex_colour: str) -> tuple[int, int, int]:
        text = hex_colour.strip().lstrip("#")
        if len(text) != 6:
            raise ValueError("baseColour.hex must be a 6-digit RGB hex value")
        return int(text[0:2], 16), int(text[2:4], 16), int(text[4:6], 16)

    @staticmethod
    def rgb_to_hsv(rgb: tuple[int, int, int]) -> tuple[float, float, float]:
        r, g, b = rgb
        h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
        return (h * 360.0, s, v)

    @staticmethod
    def hsv_to_rgb(h: float, s: float, v: float) -> tuple[int, int, int]:
        h_norm = h % 360.0
        s_norm = min(1.0, max(0.0, s))
        v_norm = min(1.0, max(0.0, v))
        if hsv_to_rgb is not None:
            out = hsv_to_rgb(h_norm, s_norm, v_norm)
            return int(out[0]), int(out[1]), int(out[2])
        r, g, b = colorsys.hsv_to_rgb(h_norm / 360.0, s_norm, v_norm)
        return int(round(r * 255)), int(round(g * 255)), int(round(b * 255))

    @staticmethod
    def hsv_to_oklch(h: float, s: float, v: float) -> tuple[float, float, float]:
        # Deterministic projection used by the generator for role and metadata output.
        return (round(min(1.0, max(0.0, v)), 6), round(min(0.4, max(0.0, s * 0.32)), 6), round(h % 360.0, 6))

    @staticmethod
    def oklch_to_rgb(L: float, C: float, H: float) -> tuple[int, int, int]:
        if oklch_to_rgb is not None:
            rgb = oklch_to_rgb(L, C, H)
            return int(rgb[0]), int(rgb[1]), int(rgb[2])
        return ChromaSpaceAdapter.hsv_to_rgb(H, C, L)
