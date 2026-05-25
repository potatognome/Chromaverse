# src/colour_system/colour_methods/oklch.py

import math

from ..interfaces import ColourSpaceInterface
from ..registry import register_colour_space

def oklch_to_oklab(L, C, H):
    a = C * math.cos(math.radians(H))
    b = C * math.sin(math.radians(H))
    return L, a, b

def oklab_to_linear_srgb(L, a, b):
    # OKLab → linear RGB matrix
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b

    l = l_ ** 3
    m = m_ ** 3
    s = s_ ** 3

    r = (+4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s)
    g = (-1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s)
    b = (-0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)

    return r, g, b

def linear_to_srgb(x):
    if x <= 0.0031308:
        return 12.92 * x
    return 1.055 * (x ** (1/2.4)) - 0.055

def to_rgb(h, c, l):
    """
    h: hue angle 0–360
    c: chroma band value (0–1)
    l: lightness band value (0–1)
    """
    L = l
    C = c
    H = h

    L, a, b = oklch_to_oklab(L, C, H)
    r_lin, g_lin, b_lin = oklab_to_linear_srgb(L, a, b)

    r = linear_to_srgb(r_lin)
    g = linear_to_srgb(g_lin)
    b = linear_to_srgb(b_lin)

    return (
        int(max(0, min(1, r)) * 255),
        int(max(0, min(1, g)) * 255),
        int(max(0, min(1, b)) * 255),
    )


@register_colour_space(
    name="oklch",
    version="1.0.0",
    capabilities=["oklch", "rgb", "deterministic"],
    config_schema="schemas/colour_spaces/oklch.json",
)
class OklchColourSpace(ColourSpaceInterface):
    """Registry-backed OKLCh adapter."""

    def to_rgb(self, h, s, l):
        return to_rgb(h, s, l)