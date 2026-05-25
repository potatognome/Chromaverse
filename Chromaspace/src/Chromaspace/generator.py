#!/usr/bin/env python3
"""Generates all colour entries in the selected Chromaspace colour system."""
# src/Chromaspace/generator.py

try:
    from tUilKit import get_logger as _get_logger
    logger = _get_logger()
except Exception:
    logger = None

from .colour_engine import to_rgb

from .config import SAT_BANDS, LUM_BANDS, SAT_BANDS_GREY, LUM_BANDS_GREY
from .config import _bands
from .hue import get_sorted_hues
from .xkcd import nearest_xkcd_colour

LOG_FILES = {
    "SESSION": "logFiles/chromaspace_SESSION.log",
    "MASTER":  "logFiles/chromaspace_MASTER.log",
}

# Load tupled bands/values from config
GREY_BAND = _bands["GREY_BAND"]
GREY_VARIANT = _bands["GREY_VARIANT"]
COLOUR_METHOD = _bands.get("COLOUR_METHOD", "hsv")

def generate_colour(h, s, lum_value, method):
    rgb = to_rgb(h, s, lum_value, method=method)
    return {
        "hue": h,
        "sat": s,
        "lum": lum_value,
        "rgb": rgb,
    }

def generate_colour_entries():
    colours = []
    # Regular hues (skip sat=0 to avoid duplicate greys)
    for anchor, variant, h in get_sorted_hues():
        for si, (sat, s) in enumerate(SAT_BANDS):
            if s == 0.0:
                continue  # skip greys in hue loop
            for li, (lum, v) in enumerate(LUM_BANDS):
                name = f"{lum}-{sat} {variant}-{anchor}"
                rgb = to_rgb(h, s, v, method=COLOUR_METHOD)
                xkcd = nearest_xkcd_colour(rgb)
                entry = {
                    "name": name,
                    "hue_anchor": anchor,
                    "hue_variant": variant,
                    "sat_band": sat,
                    "lum_band": lum,
                    "bands": {"sat": si, "lum": li},
                    "hsv": [h, s, v],
                    "rgb": rgb,
                    "xkcd_match": xkcd
                }
                colours.append(entry)
    # Greys band (sat=0, single hue/variant)
    for anchor in GREY_BAND:
        for variant in GREY_VARIANT:
            h = 0  # hue is irrelevant for greys
            for si, (sat, s) in enumerate(SAT_BANDS_GREY):
                for li, (lum, v) in enumerate(LUM_BANDS_GREY):
                    name = f"{lum}-{sat} {variant}-{anchor}"
                    rgb = to_rgb(h, s, v, method=COLOUR_METHOD)
                    xkcd = nearest_xkcd_colour(rgb)
                    entry = {
                        "name": name,
                        "hue_anchor": anchor,
                        "hue_variant": variant,
                        "sat_band": sat,
                        "lum_band": lum,
                        "bands": {"sat": si, "lum": li},
                        "hsv": [h, s, v],
                        "rgb": rgb,
                        "xkcd_match": xkcd
                    }
                    colours.append(entry)
    return colours
