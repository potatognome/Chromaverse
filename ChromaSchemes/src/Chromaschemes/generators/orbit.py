"""Orbit scheme generator registered with Chromacore."""

from __future__ import annotations

from Dev.Chromaspace.src.Chromaspace.interfaces import SchemeInterface
from Dev.Chromaspace.src.Chromaspace.registry import register_scheme

from ..config import CONFIG


@register_scheme(
    name="orbit",
    version="1.0.0",
    capabilities=["circular", "rotational"],
    config_schema="schemas/orbit.json",
)
class OrbitSchemeGenerator(SchemeInterface):
    """Generate deterministic circular hue progressions."""

    def generate(self, base_hue: float, steps: int | None = None) -> list[float]:
        defaults = CONFIG.get("SCHEME_DEFAULTS", {})
        count = int(steps if steps is not None else defaults.get("STEPS", 4))
        rotation = float(defaults.get("BASE_ROTATION_DEGREES", 30))
        return [((base_hue + (rotation * idx)) % 360) for idx in range(count)]
