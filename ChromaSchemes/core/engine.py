"""Top-level deterministic ChromaSchemes engine."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from geometry import GeometryInterpreter, OverlayProcessor
from output import ChromaSchemeEmitter

from .colour_generator import ColourGenerator
from .colour_set_builder import ColourSetBuilder
from .preview_model_builder import PreviewModelBuilder
from .role_binder import RoleBinder


class ChromaSchemesEngine:
    """Generate ChromaScheme output from canonical input."""

    def __init__(self) -> None:
        self.geometry_interpreter = GeometryInterpreter()
        self.overlay_processor = OverlayProcessor()
        self.colour_generator = ColourGenerator()
        self.colour_set_builder = ColourSetBuilder()
        self.role_binder = RoleBinder()
        self.preview_model_builder = PreviewModelBuilder()
        self.emitter = ChromaSchemeEmitter()

    def generate(self, payload: dict[str, Any]) -> dict[str, Any]:
        base_hex = payload["baseColour"]["hex"]
        geometry_model = payload["geometryModel"]
        overlays = payload.get("overlays", [])
        desired_count = int(payload.get("desiredColourCount", 8))

        hue_offsets = self.geometry_interpreter.interpret(geometry_model, desired_count, payload.get("geometryParams"))
        base_chroma = [0.18 for _ in range(desired_count)]
        base_luminance = [0.68 for _ in range(desired_count)]
        hues, chroma_values, luminance_values = self.overlay_processor.apply(
            hue_offsets,
            base_chroma,
            base_luminance,
            overlays,
        )

        generated = self.colour_generator.generate(base_hex, hues, chroma_values, luminance_values)
        colour_set = self.colour_set_builder.build(generated)
        roles = self.role_binder.bind(colour_set)
        preview = self.preview_model_builder.build(colour_set, roles)

        return {
            "colourSet": colour_set,
            "roles": roles,
            "geometry": {
                "baseGeometry": geometry_model,
                "overlays": overlays,
                "expressions": {"parageometric": True, "offsets": hues},
            },
            "preview": preview,
        }

    def emit(self, payload: dict[str, Any], target_path: Path) -> Path:
        return self.emitter.emit(self.generate(payload), target_path)
