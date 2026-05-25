"""Colour-space adapters package.

Importing this package initializes decorator-driven registry registration.
"""

from .hsv import HSVColourSpace
from .lab import LabColourSpace
from .oklch import OklchColourSpace

__all__ = [
    "HSVColourSpace",
    "LabColourSpace",
    "OklchColourSpace",
]
