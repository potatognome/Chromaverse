"""Generates combined tone descriptors."""
from .config import SAT_BANDS, LUM_BANDS

def get_tone_label(sat, lum):
    return f"{sat}-{lum}"

def all_tone_labels():
    return [get_tone_label(sat, lum) for sat, _ in SAT_BANDS for lum, _ in LUM_BANDS]
