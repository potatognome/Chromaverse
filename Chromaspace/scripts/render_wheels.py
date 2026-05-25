
import argparse
import os
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from Chromaspace.visualization import build_sat_wheel, build_lum_wheel
from Chromaspace.cli_utils import get_sat_bands, get_lum_bands, ensure_output_dir


def main():
    parser = argparse.ArgumentParser(description="Render all sat/lum wheels as HTML files.")
    parser.add_argument('--output', default=None, help='Output directory for HTML files')
    args = parser.parse_args()

    sat_bands = get_sat_bands()
    lum_bands = get_lum_bands()

    # Use config-driven default if not provided

    from Chromaspace.cli_utils import (
        append_suffix_to_filename,
        get_output_folder,
    )
    output_dir = args.output or get_output_folder(
        "HTML_OUTPUT", "../output/HTML", with_system_suffix=True
    )
    ensure_output_dir(output_dir)

    for lum in lum_bands:
        html = build_sat_wheel(lum)
        sat_file = append_suffix_to_filename(f"sat_wheel_{lum}.html")
        with open(os.path.join(output_dir, sat_file), "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Wrote sat wheel for {lum}")

    for sat in sat_bands:
        html = build_lum_wheel(sat)
        lum_file = append_suffix_to_filename(f"lum_wheel_{sat}.html")
        with open(os.path.join(output_dir, lum_file), "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Wrote lum wheel for {sat}")

if __name__ == "__main__":
    main()
