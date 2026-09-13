"""Deterministic, extensible geometry interpreter."""

from __future__ import annotations

from collections.abc import Callable


class GeometryInterpreter:
    """Resolve model names to deterministic hue offsets."""

    def __init__(self) -> None:
        self._models: dict[str, Callable[[int], list[float]]] = {
            "quadratic": self._quadratic,
            "triadic": self._triadic,
            "tetradic": self._tetradic,
            "split_complementary": self._split_complementary,
            "harmonic": self._harmonic,
            "custom": self._custom,
        }

    def register_model(self, name: str, builder: Callable[[int], list[float]]) -> None:
        self._models[name] = builder

    def interpret(self, model: str, desired_count: int, params: dict | None = None) -> list[float]:
        if desired_count < 1:
            raise ValueError("desired_count must be at least 1")
        builder = self._models.get(model)
        if builder is None:
            raise ValueError(f"Unsupported geometry model: {model}")
        if model == "custom":
            return self._custom(desired_count, params or {})
        offsets = builder(desired_count)
        return [round(float(v) % 360.0, 6) for v in offsets[:desired_count]]

    @staticmethod
    def _repeat_cycle(cycle: list[float], desired_count: int) -> list[float]:
        return [cycle[index % len(cycle)] for index in range(desired_count)]

    def _quadratic(self, desired_count: int) -> list[float]:
        cycle = [0.0, 90.0, 180.0, 270.0]
        return self._repeat_cycle(cycle, desired_count)

    def _triadic(self, desired_count: int) -> list[float]:
        cycle = [0.0, 120.0, 240.0]
        return self._repeat_cycle(cycle, desired_count)

    def _tetradic(self, desired_count: int) -> list[float]:
        cycle = [0.0, 60.0, 180.0, 240.0]
        return self._repeat_cycle(cycle, desired_count)

    def _split_complementary(self, desired_count: int) -> list[float]:
        cycle = [0.0, 150.0, 210.0]
        return self._repeat_cycle(cycle, desired_count)

    def _harmonic(self, desired_count: int) -> list[float]:
        # Parageometric harmonic wave projected into hue space.
        return [round((index * index * 29.0) % 360.0, 6) for index in range(desired_count)]

    def _custom(self, desired_count: int, params: dict) -> list[float]:
        values = params.get("offsets", [])
        if not isinstance(values, list) or not values:
            raise ValueError("Custom geometry requires non-empty 'offsets' list")
        cycle = [float(v) % 360.0 for v in values]
        return self._repeat_cycle(cycle, desired_count)
