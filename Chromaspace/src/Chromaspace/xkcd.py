"""Loads XKCD colours and computes nearest match."""
import json
import os
from math import sqrt

XKCD_PATH = os.path.join(os.path.dirname(__file__), '../../dict/xkcd_colors.json')

# Lazy load
_xkcd_colours = None

def load_xkcd_colours():
    """Load the XKCD colour lookup table on first use."""
    global _xkcd_colours
    if _xkcd_colours is None:
        with open(XKCD_PATH, 'r') as f:
            _xkcd_colours = json.load(f)
    return _xkcd_colours

def rgb_distance(rgb1, rgb2):
    """Return Euclidean distance between two RGB triples."""
    return sqrt(sum((a-b)**2 for a, b in zip(rgb1, rgb2)))

def nearest_xkcd_colour(rgb):
    """Return the nearest XKCD colour name and distance for an RGB triple."""
    colours = load_xkcd_colours()
    best = min(colours, key=lambda c: rgb_distance(rgb, colours[c]["rgb"]))
    return {"name": best, "distance": rgb_distance(rgb, colours[best]["rgb"])}
