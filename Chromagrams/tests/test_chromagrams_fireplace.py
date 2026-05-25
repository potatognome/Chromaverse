from Dev.Chromagrams.src.Chromagrams.sequences.fireplace import FireplaceBurnSequence
from Dev.Chromaspace.src.Chromaspace.registry import (
    MODULE_TYPE_ANIMATION_SEQUENCE,
    get,
    metadata,
)


# ---------------------------------------------------------------------------
# Determinism
# ---------------------------------------------------------------------------

def test_fireplace_sequence_is_deterministic():
    sequence = FireplaceBurnSequence()
    first = sequence.generate_frames()
    second = sequence.generate_frames()
    assert first == second


# ---------------------------------------------------------------------------
# Frame count
# ---------------------------------------------------------------------------

def test_fireplace_sequence_default_frame_count():
    sequence = FireplaceBurnSequence()
    frames = sequence.generate_frames()
    # Default: 12 s × 60 fps = 720 frames
    assert len(frames) == 720


def test_fireplace_sequence_custom_frame_count():
    sequence = FireplaceBurnSequence()
    frames = sequence.generate_frames(frame_count=24)
    assert len(frames) == 24


def test_fireplace_sequence_duration_and_fps_control_frame_count():
    sequence = FireplaceBurnSequence()
    frames = sequence.generate_frames(duration=6.0, fps=30.0)
    assert len(frames) == 180


# ---------------------------------------------------------------------------
# Frame structure
# ---------------------------------------------------------------------------

def test_fireplace_sequence_frame_structure():
    sequence = FireplaceBurnSequence()
    frames = sequence.generate_frames(frame_count=8)
    required_keys = {"hue", "saturation", "brightness", "phase", "flicker_intensity"}
    for frame in frames:
        assert required_keys == set(frame.keys())


# ---------------------------------------------------------------------------
# Value ranges
# ---------------------------------------------------------------------------

def test_fireplace_sequence_values_in_range():
    sequence = FireplaceBurnSequence()
    frames = sequence.generate_frames(frame_count=120)
    for frame in frames:
        assert 0.0 <= frame["hue"] <= 1.0
        assert 0.0 <= frame["saturation"] <= 1.0
        assert 0.0 <= frame["brightness"] <= 1.0
        assert 0.0 <= frame["phase"] < 1.0
        assert 0.0 <= frame["flicker_intensity"] <= 1.0


# ---------------------------------------------------------------------------
# Warm palette constraint
# ---------------------------------------------------------------------------

def test_fireplace_sequence_warm_palette():
    sequence = FireplaceBurnSequence()
    frames = sequence.generate_frames(frame_count=720)
    for frame in frames:
        # Hue must stay within the warm ember-red → amber range [0.0, 0.083]
        assert frame["hue"] <= 0.083 + 1e-9, (
            f"Hue {frame['hue']!r} outside warm palette range"
        )


# ---------------------------------------------------------------------------
# Phase monotonicity (looping sequence — phase runs 0 → <1)
# ---------------------------------------------------------------------------

def test_fireplace_sequence_phase_monotonic():
    sequence = FireplaceBurnSequence()
    frames = sequence.generate_frames(frame_count=60)
    phases = [f["phase"] for f in frames]
    assert phases == sorted(phases)
    assert phases[0] == 0.0
    assert phases[-1] < 1.0


# ---------------------------------------------------------------------------
# Flicker speed scale parameter
# ---------------------------------------------------------------------------

def test_fireplace_sequence_flicker_speed_scale_changes_output():
    sequence = FireplaceBurnSequence()
    default_frames = sequence.generate_frames(frame_count=60)
    fast_frames = sequence.generate_frames(frame_count=60, flicker_speed_scale=1.0)
    # Different flicker speed must produce at least some different brightness values
    assert any(
        d["brightness"] != f["brightness"]
        for d, f in zip(default_frames, fast_frames)
    )


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

def test_fireplace_is_registered():
    factory = get(MODULE_TYPE_ANIMATION_SEQUENCE, "fireplace_burn")
    assert factory is FireplaceBurnSequence


def test_fireplace_registry_metadata():
    info = metadata(MODULE_TYPE_ANIMATION_SEQUENCE, "fireplace_burn")
    assert info.name == "fireplace_burn"
    assert "looping" in info.capabilities
    assert "warm_palette" in info.capabilities
    assert "flicker" in info.capabilities
    assert "ease_in_out" in info.capabilities
    assert "noise_modulated" in info.capabilities
