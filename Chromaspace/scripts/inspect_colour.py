"""CLI tool to classify a given RGB/HSV into the system."""
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from Chromaspace.hsv import hsv_to_rgb
from Chromaspace.xkcd import nearest_xkcd_colour

if __name__ == "__main__":
    if len(sys.argv) == 4:
        raw_values = sys.argv[1:4]
        # Use HSV mode when any argument is fractional; otherwise treat as RGB.
        if any("." in value for value in raw_values):
            h, s, v = map(float, raw_values)
            rgb = hsv_to_rgb(h, s, v)
            print(f"RGB: {rgb}")
            print(f"Nearest XKCD: {nearest_xkcd_colour(rgb)}")
        else:
            r, g, b = map(int, raw_values)
            print(f"Nearest XKCD: {nearest_xkcd_colour([r, g, b])}")
    else:
        print("Usage: inspect_colour.py H S V | R G B")
