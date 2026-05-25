"""Visualization functions for the 36×5×5 colour system."""
from .config import HUE_ANCHORS, HUE_VARIANTS, SAT_BANDS, LUM_BANDS, _bands
from .colour_engine import to_rgb
from .hue import get_hue_angle, get_sorted_hues
from .html import build_html_table, swatch_cell


COLOUR_METHOD = _bands.get("COLOUR_METHOD", "hsv")




def build_sat_wheel(lum):
    """Generate a saturation-gradient wheel for a fixed luminance band as an HTML table."""
    band_names = [name for name, value in LUM_BANDS]
    assert lum in band_names, f"Invalid luminance band: {lum}"
    lum_idx = band_names.index(lum)
    rows = []
    for anchor, variant, h in get_sorted_hues():
        row = []
        for si, (sat, s) in enumerate(SAT_BANDS):
            v = LUM_BANDS[lum_idx][1]
            rgb = to_rgb(h, s, v, method=COLOUR_METHOD)
            hsv = [round(h,2), round(s,2), round(v,2)]
            label = f"{anchor}-{variant} / {sat}"
            xkcd_match = None
            try:
                from .xkcd import nearest_xkcd_colour
                xkcd_match = nearest_xkcd_colour(rgb)
            except Exception:
                pass
            cell = swatch_cell(
                rgb, label, hsv, xkcd_match=xkcd_match, extra=f"{sat}"
            )
            row.append(cell)
        rows.append(row)
    return build_html_table(rows, header=[name for name, value in SAT_BANDS], title=f"Saturation Wheel for {lum}")

def build_lum_wheel(sat):
    """Generate a luminance-gradient wheel for a fixed saturation band as an HTML table."""
    band_names = [name for name, value in SAT_BANDS]
    assert sat in band_names, f"Invalid saturation band: {sat}"
    sat_idx = band_names.index(sat)
    rows = []
    for anchor, variant, h in get_sorted_hues():
        row = []
        for li, (lum, v) in enumerate(LUM_BANDS):
            s = SAT_BANDS[sat_idx][1]
            rgb = to_rgb(h, s, v, method=COLOUR_METHOD)
            hsv = [round(h,2), round(s,2), round(v,2)]
            label = f"{anchor}-{variant} / {lum}"
            xkcd_match = None
            try:
                from .xkcd import nearest_xkcd_colour
                xkcd_match = nearest_xkcd_colour(rgb)
            except Exception:
                pass
            cell = swatch_cell(
                rgb, label, hsv, xkcd_match=xkcd_match, extra=f"{lum}"
            )
            row.append(cell)
        rows.append(row)
    return build_html_table(rows, header=[name for name, value in LUM_BANDS], title=f"Luminance Wheel for {sat}")

def build_hue_square(hue, hue_offset=0):
    """Generate a 5×5 tone square for a single hue as an HTML table."""
    # hue is anchor-variant (anchor may contain hyphens)
    anchor, variant = hue.rsplit("-", 1)
    h = get_hue_angle(anchor, variant, hue_offset)
    rows = []
    colour_name_format = _bands.get("COLOUR_NAME_FORMAT", "{lum} {sat} {variant} {hue}")
    for si, (sat, s) in enumerate(SAT_BANDS):
        row = []
        for li, (lum, v) in enumerate(LUM_BANDS):
            rgb = to_rgb(h, s, v, method=COLOUR_METHOD)
            hsv = [round(h,2), round(s,2), round(v,2)]
            label = colour_name_format.format(
                lum=lum,
                sat=sat,
                variant=variant,
                hue=anchor
            )
            xkcd_match = None
            try:
                from .xkcd import nearest_xkcd_colour
                xkcd_match = nearest_xkcd_colour(rgb)
            except Exception:
                pass
            cell = swatch_cell(rgb, label, hsv, xkcd_match=xkcd_match)
            row.append(cell)
        rows.append(row)
    return build_html_table(rows, header=[name for name, value in LUM_BANDS], row_labels=[name for name, value in SAT_BANDS], title=f"Tone Grid for {hue}")
