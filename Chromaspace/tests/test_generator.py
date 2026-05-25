from Chromaspace.generator import generate_colour_entries
from Chromaspace.config import (
    HUE_ANCHORS,
    HUE_VARIANTS,
    LUM_BANDS,
    SAT_BANDS,
    SAT_BANDS_GREY,
    LUM_BANDS_GREY,
)


def _distinct_hue_angles(colours):
    angles = []
    seen = set()
    for entry in colours:
        if entry["hue_anchor"] == "grey":
            continue
        angle = round(entry["hsv"][0], 10)
        if angle not in seen:
            seen.add(angle)
            angles.append(angle)
    return angles


def _circular_differences(values):
    wrapped = values + [values[0] + 360.0]
    return [wrapped[i + 1] - wrapped[i] for i in range(len(values))]


def test_generate_colour_entries():
    colours = generate_colour_entries()
    active_sat_bands = sum(1 for _, sat_value in SAT_BANDS if sat_value != 0.0)
    regular_count = (
        len(HUE_ANCHORS) * len(HUE_VARIANTS) * active_sat_bands * len(LUM_BANDS)
    )
    grey_count = len(SAT_BANDS_GREY) * len(LUM_BANDS_GREY)
    assert len(colours) == regular_count + grey_count
    assert all('name' in c and 'hsv' in c and 'rgb' in c for c in colours)

    unique_hues = _distinct_hue_angles(colours)
    expected_unique = len(HUE_ANCHORS) * len(HUE_VARIANTS)
    assert len(unique_hues) == expected_unique
    assert unique_hues == sorted(unique_hues)

    diffs = _circular_differences(unique_hues)
    expected_step = 360.0 / expected_unique
    assert all(abs(diff - expected_step) < 1e-6 for diff in diffs)
