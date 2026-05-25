# src/colour_system/colour_engine.py

from . import colour_spaces  # noqa: F401
from .registry import MODULE_TYPE_COLOUR_SPACE, get

def to_rgb(h, s, lum_value, method="hsv"):
    """
    Convert semantic (hue, sat, lum) into RGB using the selected engine.
    """
    adapter_factory = get(MODULE_TYPE_COLOUR_SPACE, method)
    if adapter_factory is None:
        raise ValueError(f"Unknown colour method: {method}")

    adapter = adapter_factory() if isinstance(adapter_factory, type) else adapter_factory
    if not hasattr(adapter, "to_rgb"):
        raise TypeError(f"Registered adapter for {method} does not expose to_rgb")

    return list(adapter.to_rgb(h, s, lum_value))