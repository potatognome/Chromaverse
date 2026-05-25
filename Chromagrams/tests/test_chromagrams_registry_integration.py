from Dev.Chromaspace.src.Chromaspace.registry import (
    MODULE_TYPE_ANIMATION_SEQUENCE,
    get,
    metadata,
)

from Dev.Chromagrams.src.Chromagrams.sequences.pulse import PulseSequence


def test_pulse_is_registered_in_chromacore():
    factory = get(MODULE_TYPE_ANIMATION_SEQUENCE, "pulse")
    assert factory is PulseSequence

    info = metadata(MODULE_TYPE_ANIMATION_SEQUENCE, "pulse")
    assert info.name == "pulse"
    assert "looping" in info.capabilities
