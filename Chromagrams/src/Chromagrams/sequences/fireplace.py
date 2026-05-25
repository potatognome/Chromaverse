"""FireplaceBurnSequence — slow-burning fireplace animation with warm gradients and flicker."""

from __future__ import annotations

import math

from Dev.Chromaspace.src.Chromaspace.interfaces import AnimationInterface
from Dev.Chromaspace.src.Chromaspace.registry import register_animation

from ..config import CONFIG

_NOISE_PHASE_OFFSET = 1.2345678


def _trig_noise(phase: float, harmonics: int) -> float:
    """Deterministic noise-like value via trig harmonic series.

    Returns a value in [-1, 1].  The signal is fully reproducible for
    identical inputs — no random state is used.
    """
    value = 0.0
    norm = 0.0
    for k in range(1, harmonics + 1):
        value += math.sin(k * phase + k * _NOISE_PHASE_OFFSET) / k
        norm += 1.0 / k
    return value / norm


@register_animation(
    name="fireplace_burn",
    version="1.0.0",
    capabilities=["looping", "warm_palette", "flicker", "ease_in_out", "noise_modulated"],
    config_schema="schemas/fireplace.json",
)
class FireplaceBurnSequence(AnimationInterface):
    """Generate deterministic fireplace frames with warm gradients and organic flicker.

    Base motion
    -----------
    A smooth ease-in-out hue drift through ember-red → amber, with gentle
    brightness breathing, completing one cycle every ``duration`` seconds.

    Flicker transform
    -----------------
    A deterministic trig-harmonic noise signal applied on top of the base
    brightness.  Its frequency is scaled to ``flicker_speed_scale`` (default
    0.7 — i.e. 30 % slower than the raw harmonic rate) to keep the effect
    organic rather than strobe-like.

    Each frame is a ``dict`` with keys:
    ``hue``, ``saturation``, ``brightness``, ``phase``, ``flicker_intensity``.
    All values are in [0.0, 1.0].
    """

    def generate_frames(
        self,
        frame_count: int | None = None,
        duration: float | None = None,
        fps: float | None = None,
        flicker_speed_scale: float | None = None,
    ) -> list[dict]:
        defaults = CONFIG.get("FIREPLACE_DEFAULTS", {})

        _duration = float(duration if duration is not None else defaults.get("DURATION", 12.0))
        _fps = float(fps if fps is not None else defaults.get("FPS", 60.0))
        _flicker_speed = float(
            flicker_speed_scale
            if flicker_speed_scale is not None
            else defaults.get("FLICKER_SPEED_SCALE", 0.7)
        )
        harmonics = int(defaults.get("FLICKER_HARMONICS", 6))
        flicker_cycles = float(defaults.get("FLICKER_CYCLES", 8.0))

        count = int(frame_count if frame_count is not None else defaults.get("FRAME_COUNT", round(_duration * _fps)))

        hue_min = float(defaults.get("HUE_MIN", 0.0))
        hue_max = float(defaults.get("HUE_MAX", 0.083))
        sat_base = float(defaults.get("SATURATION_BASE", 0.85))
        sat_range = float(defaults.get("SATURATION_RANGE", 0.12))
        bri_base = float(defaults.get("BRIGHTNESS_BASE", 0.75))
        bri_range = float(defaults.get("BRIGHTNESS_RANGE", 0.20))
        flicker_range = float(defaults.get("FLICKER_RANGE", 0.15))

        two_pi = 2.0 * math.pi
        frames = []
        for idx in range(count):
            phase = idx / count  # [0.0, 1.0)

            # Base motion: ease-in-out hue drift (red → amber → red)
            smooth = (1.0 - math.cos(two_pi * phase)) / 2.0
            hue = hue_min + smooth * (hue_max - hue_min)

            # Brightness breathing
            bri_base_frame = bri_base + bri_range * math.sin(two_pi * phase)

            # Saturation pulse (quarter-phase offset for subtle variation)
            saturation = sat_base + sat_range * math.sin(two_pi * phase + math.pi / 4.0)

            # Flicker: noise at reduced speed layered on top of base brightness
            flicker_phase = phase * _flicker_speed * two_pi * flicker_cycles
            noise = _trig_noise(flicker_phase, harmonics)
            flicker_intensity = (noise + 1.0) / 2.0  # [0, 1]
            brightness = bri_base_frame + flicker_range * noise

            frames.append({
                "hue": round(max(0.0, min(1.0, hue)), 6),
                "saturation": round(max(0.0, min(1.0, saturation)), 6),
                "brightness": round(max(0.0, min(1.0, brightness)), 6),
                "phase": round(phase, 6),
                "flicker_intensity": round(max(0.0, min(1.0, flicker_intensity)), 6),
            })

        return frames
