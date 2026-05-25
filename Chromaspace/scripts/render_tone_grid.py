
import argparse
import os
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from Chromaspace.visualization import build_hue_square
from Chromaspace.cli_utils import get_hue_anchors, get_hue_variants, ensure_output_dir


def main():
    parser = argparse.ArgumentParser(description="Render all hue squares as HTML files.")
    parser.add_argument('--output', default=None, help='Output directory for HTML files')
    args = parser.parse_args()

    anchors = get_hue_anchors()
    variants = get_hue_variants()


    from Chromaspace.cli_utils import (
        append_suffix_to_filename,
        get_output_folder,
    )
    output_dir = args.output or get_output_folder(
        "HTML_OUTPUT", "../output/HTML", with_system_suffix=True
    )
    ensure_output_dir(output_dir)

    for anchor in anchors:
        for variant in variants:
            hue = f"{anchor}-{variant}"
            html = build_hue_square(hue)
            file_name = append_suffix_to_filename(f"tone_grid_{hue}.html")
            fname = os.path.join(output_dir, file_name)
            with open(fname, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"Wrote tone grid for {hue}")

if __name__ == "__main__":
    main()
