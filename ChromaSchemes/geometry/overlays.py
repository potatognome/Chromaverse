"""Pure deterministic overlay processor."""

from __future__ import annotations


class OverlayProcessor:
    """Apply deterministic overlay transforms to hue/chroma/luminance tracks."""

    def apply(
        self,
        hues: list[float],
        chroma_values: list[float],
        luminance_values: list[float],
        overlays: list[dict],
    ) -> tuple[list[float], list[float], list[float]]:
        out_hues = list(hues)
        out_chroma = list(chroma_values)
        out_luminance = list(luminance_values)

        for overlay in overlays:
            overlay_type = str(overlay.get("type", "")).strip().lower()
            params = overlay.get("params", {}) if isinstance(overlay.get("params", {}), dict) else {}

            if overlay_type in {"harmonic", "rotational", "rotation"}:
                angle = float(params.get("rotation", 0.0))
                out_hues = [round((h + angle) % 360.0, 6) for h in out_hues]
            elif overlay_type in {"luminance_wheel", "luminance-wheel"}:
                amplitude = float(params.get("amplitude", 0.12))
                out_luminance = [
                    min(0.95, max(0.05, round(l + (amplitude * ((idx % 4) - 1.5) / 3.0), 6)))
                    for idx, l in enumerate(out_luminance)
                ]
            elif overlay_type in {"chroma_spiral", "chroma-spiral"}:
                step = float(params.get("step", 0.015))
                out_chroma = [
                    min(0.33, max(0.01, round(c + (idx * step), 6)))
                    for idx, c in enumerate(out_chroma)
                ]

        return out_hues, out_chroma, out_luminance
