# src/colour_system/colour_methods/lab.py

import math

from ..interfaces import ColourSpaceInterface
from ..registry import register_colour_space

def lab_to_xyz(L, a, b):
    # D65 reference white
    Xn, Yn, Zn = 95.047, 100.000, 108.883

    fy = (L + 16) / 116
    fx = fy + (a / 500)
    fz = fy - (b / 200)

    def f_inv(t):
        if t ** 3 > 0.008856:
            return t ** 3
        return (t - 16/116) / 7.787

    X = Xn * f_inv(fx)
    Y = Yn * f_inv(fy)
    Z = Zn * f_inv(fz)

    return X, Y, Z

def xyz_to_rgb(X, Y, Z):
    X /= 100
    Y /= 100
    Z /= 100

    r = X * 3.2406 + Y * -1.5372 + Z * -0.4986
    g = X * -0.9689 + Y * 1.8758 + Z * 0.0415
    b = X * 0.0557 + Y * -0.2040 + Z * 1.0570

    def gamma(x):
        if x <= 0.0031308:
            return 12.92 * x
        return 1.055 * (x ** (1/2.4)) - 0.055

    return (
        int(max(0, min(1, gamma(r))) * 255),
        int(max(0, min(1, gamma(g))) * 255),
        int(max(0, min(1, gamma(b))) * 255),
    )

def to_rgb(h, c, l):
    """
    h: hue angle 0–360
    c: chroma band value
    l: lightness band value
    """
    L = l * 100
    a = math.cos(math.radians(h)) * c * 100
    b = math.sin(math.radians(h)) * c * 100

    X, Y, Z = lab_to_xyz(L, a, b)
    return xyz_to_rgb(X, Y, Z)


@register_colour_space(
    name="lab",
    version="1.0.0",
    capabilities=["lab", "rgb", "deterministic"],
    config_schema="schemas/colour_spaces/lab.json",
)
class LabColourSpace(ColourSpaceInterface):
    """Registry-backed CIE Lab adapter."""

    def to_rgb(self, h, s, l):
        return to_rgb(h, s, l)