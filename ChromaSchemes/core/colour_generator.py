"""Deterministic colour generation from geometry expressions."""

from __future__ import annotations

from .chromaspace_adapter import ChromaSpaceAdapter


class ColourGenerator:
    """Generate RGB/OKLCH colours with stable IDs and origin metadata."""

    def __init__(self, adapter: ChromaSpaceAdapter | None = None) -> None:
        self._adapter = adapter or ChromaSpaceAdapter()

    def generate(
        self,
        base_hex: str,
        hue_offsets: list[float],
        chroma_values: list[float],
        luminance_values: list[float],
    ) -> list[dict]:
        base_rgb = self._adapter.hex_to_rgb(base_hex)
        base_h, _, _ = self._adapter.rgb_to_hsv(base_rgb)

        colours: list[dict] = []
        for index, offset in enumerate(hue_offsets):
            hue = (base_h + offset) % 360.0
            saturation = chroma_values[index]
            value = luminance_values[index]
            rgb = self._adapter.hsv_to_rgb(hue, saturation, value)
            oklch = self._adapter.hsv_to_oklch(hue, saturation, value)

            colours.append(
                {
                    "id": f"c{index}",
                    "origin": "base" if index < 4 else "derived",
                    "rgb": {"r": rgb[0], "g": rgb[1], "b": rgb[2]},
                    "oklch": {"l": oklch[0], "c": oklch[1], "h": oklch[2]},
                    "metadata": {"hueOffset": round(offset, 6)},
                }
            )

        return colours
