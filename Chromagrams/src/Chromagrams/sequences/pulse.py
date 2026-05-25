"""Pulse animation sequence registered with Chromacore."""

from __future__ import annotations

import math

from Dev.Chromaspace.src.Chromaspace.interfaces import AnimationInterface
from Dev.Chromaspace.src.Chromaspace.registry import register_animation

from ..config import CONFIG


@register_animation(
    name="pulse",
    version="1.0.0",
    capabilities=["looping", "amplitude"],
    config_schema="schemas/pulse.json",
)
class PulseSequence(AnimationInterface):
    """Generate deterministic pulse frames in [0, 1]."""

    def generate_frames(
        self,
        frame_count: int | None = None,
        amplitude: float | None = None,
    ) -> list[float]:
        defaults = CONFIG.get("ANIMATION_DEFAULTS", {})
        count = int(frame_count if frame_count is not None else defaults.get("FRAME_COUNT", 8))
        amp = float(amplitude if amplitude is not None else defaults.get("AMPLITUDE", 0.5))

        frames = []
        for idx in range(count):
            phase = (2 * math.pi * idx) / count
            value = 0.5 + (math.sin(phase) * amp)
            frames.append(round(max(0.0, min(1.0, value)), 6))
        return frames
