"""Handles hue angle computation and labelling."""

from .config import HUE_ANCHORS, HUE_VARIANTS, _bands


def get_hue_angle_step():
    """Return the spacing between hue anchors around the colour wheel."""
    return 360.0 / len(HUE_ANCHORS)


def get_hue_anchor_angles():
    """Return base hue angles for each anchor, with optional config override."""
    configured_angles = _bands.get("HUE_ANCHOR_BASE_ANGLES")
    if configured_angles:
        if isinstance(configured_angles, dict):
            return {
                anchor: float(configured_angles[anchor]) % 360
                for anchor in HUE_ANCHORS
            }
        return {
            anchor: float(configured_angles[i]) % 360
            for i, anchor in enumerate(HUE_ANCHORS)
        }

    step = get_hue_angle_step()
    start_angle = float(_bands.get("HUE_ANCHOR_START", 0.0))
    return {
        anchor: (start_angle + (i * step)) % 360
        for i, anchor in enumerate(HUE_ANCHORS)
    }


def _get_default_variant_offsets():
    """Space variants evenly and symmetrically around each anchor angle."""
    count = len(HUE_VARIANTS)
    if count == 1:
        return {HUE_VARIANTS[0]: 0.0}

    gap = get_hue_angle_step() / count
    centre = (count - 1) / 2.0
    return {
        variant: (index - centre) * gap
        for index, variant in enumerate(HUE_VARIANTS)
    }


def get_variant_offsets():
    """Return variant offsets, allowing per-config overrides."""
    configured_offsets = _bands.get("HUE_VARIANT_OFFSETS")
    if configured_offsets:
        if isinstance(configured_offsets, dict):
            return {
                variant: float(configured_offsets[variant])
                for variant in HUE_VARIANTS
            }
        return {
            variant: float(configured_offsets[i])
            for i, variant in enumerate(HUE_VARIANTS)
        }
    return _get_default_variant_offsets()


def get_hue_angle(anchor, variant, hue_offset=0):
    anchor_angles = get_hue_anchor_angles()
    variant_offsets = get_variant_offsets()
    base = anchor_angles[anchor]
    offset = variant_offsets[variant]
    return (base + offset + hue_offset) % 360


def get_sorted_hues():
    """Return (anchor, variant, angle) tuples sorted by hue angle."""
    tuples = [
        (anchor, variant, get_hue_angle(anchor, variant))
        for anchor in HUE_ANCHORS
        for variant in HUE_VARIANTS
    ]
    return sorted(tuples, key=lambda item: item[2])


def get_hue_label(anchor, variant):
    return f"{anchor}-{variant}"
