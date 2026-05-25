"""Deterministic math helpers used by geometry and generators."""

from __future__ import annotations


def clamp(value: float, low: float, high: float) -> float:
    """Clamp a value into an inclusive range."""
    if low > high:
        raise ValueError("low must be <= high")
    if value < low:
        return low
    if value > high:
        return high
    return value


def normalize_hue(angle: float) -> float:
    """Normalize a hue angle to the canonical [0, 360) range."""
    result = angle % 360.0
    if result == 360.0:
        return 0.0
    return result


def stable_round(value: float, digits: int = 10) -> float:
    """Round float values in one place to keep outputs stable."""
    return round(float(value), digits)
