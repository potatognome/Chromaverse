# src/colour_system/colour_methods/hsv.py
"""HSV to RGB conversion."""
import colorsys

from ..interfaces import ColourSpaceInterface
from ..registry import register_colour_space

def hsv_to_rgb(h, s, v):
    """h: 0-360, s/v: 0-1.0. Returns (r, g, b) 0-255."""
    r, g, b = colorsys.hsv_to_rgb(h/360, s, v)
    return [int(round(x * 255)) for x in (r, g, b)]

def to_rgb(h, s, v):
    """
    h: hue angle 0–360
    s: 0–1 saturation band value
    v: 0–1 luminance/value band value
    """
    r, g, b = colorsys.hsv_to_rgb(h/360, s, v)
    return int(r*255), int(g*255), int(b*255)


@register_colour_space(
    name="hsv",
    version="1.0.0",
    capabilities=["hsv", "rgb", "deterministic"],
    config_schema="schemas/colour_spaces/hsv.json",
)
class HSVColourSpace(ColourSpaceInterface):
    """Registry-backed HSV adapter."""

    def to_rgb(self, h, s, l):
        return to_rgb(h, s, l)