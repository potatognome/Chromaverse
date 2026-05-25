from Chromaspace.core import (
    clamp,
    normalize_hue,
    stable_round,
)


def test_clamp_basic_range():
    assert clamp(3, 0, 5) == 3
    assert clamp(-1, 0, 5) == 0
    assert clamp(8, 0, 5) == 5


def test_normalize_hue_wraps():
    assert normalize_hue(360) == 0
    assert normalize_hue(725) == 5
    assert normalize_hue(-15) == 345


def test_stable_round_is_deterministic():
    assert stable_round(1 / 3, 4) == 0.3333
