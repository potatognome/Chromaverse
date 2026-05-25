from Chromaspace.hue import (
    get_hue_angle,
    get_hue_label,
    get_sorted_hues,
)


def _circular_differences(values):
    wrapped = values + [values[0] + 360.0]
    return [wrapped[i + 1] - wrapped[i] for i in range(len(values))]


def test_hue_spacing_is_uniform():
    hues = get_sorted_hues()
    angles = [angle for _, _, angle in hues]
    diffs = _circular_differences(angles)
    expected = 360.0 / len(hues)
    assert all(abs(diff - expected) < 1e-9 for diff in diffs)


def test_hue_angles_are_sorted():
    hues = get_sorted_hues()
    angles = [angle for _, _, angle in hues]
    assert angles == sorted(angles)


def test_hue_label_and_angle_access():
    anchor, variant, angle = get_sorted_hues()[0]
    assert get_hue_angle(anchor, variant) == angle
    assert get_hue_label(anchor, variant) == f"{anchor}-{variant}"
