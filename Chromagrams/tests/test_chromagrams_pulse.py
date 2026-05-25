from Dev.Chromagrams.src.Chromagrams.sequences.pulse import PulseSequence


def test_pulse_sequence_is_deterministic():
    sequence = PulseSequence()
    first = sequence.generate_frames()
    second = sequence.generate_frames()
    assert first == second
    assert len(first) == 8
    assert all(0.0 <= value <= 1.0 for value in first)
