"""Minimal geometry primitives for colour-geometry operations."""

from __future__ import annotations

from dataclasses import dataclass
import math

from ..core import stable_round


@dataclass(frozen=True)
class Point2D:
    """Immutable 2D point with deterministic float serialization."""

    x: float
    y: float

    def as_tuple(self, digits: int = 10) -> tuple[float, float]:
        return (stable_round(self.x, digits), stable_round(self.y, digits))


def rotate_point(
    point: Point2D,
    angle_degrees: float,
    origin: Point2D | None = None,
    digits: int = 10,
) -> Point2D:
    """Rotate a point around an origin by a degree angle."""
    pivot = origin or Point2D(0.0, 0.0)
    radians = math.radians(angle_degrees)
    cos_a = math.cos(radians)
    sin_a = math.sin(radians)

    shifted_x = point.x - pivot.x
    shifted_y = point.y - pivot.y

    rot_x = (shifted_x * cos_a) - (shifted_y * sin_a)
    rot_y = (shifted_x * sin_a) + (shifted_y * cos_a)

    return Point2D(
        stable_round(rot_x + pivot.x, digits),
        stable_round(rot_y + pivot.y, digits),
    )
