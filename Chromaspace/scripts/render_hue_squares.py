import os
import argparse
import sys
import pathlib
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))
from Chromaspace.visualization import build_hue_square
from Chromaspace.config import (
    HUE_GLOBAL_OFFSET,
    SAT_GLOBAL_OFFSET,
    LUM_GLOBAL_OFFSET,
    _config,
)
from Chromaspace.cli_utils import (
    get_hue_anchors,
    get_hue_variants,
    get_sat_bands,
    get_lum_bands,
    parse_band_arg,
    ensure_output_dir,
)

def main():
    parser = argparse.ArgumentParser(description="Render configurable hue squares as HTML.")
    parser.add_argument('--hue_anchors', default=None, help='Comma-separated anchor names or indices (e.g. red,blue or 0,2)')
    parser.add_argument('--variant', default=None, help='Variant(s): cool, warm, or both (comma-separated)')
    parser.add_argument('--sat_bands', default=None, help='Comma-separated saturation band names or indices')
    parser.add_argument('--lum_bands', default=None, help='Comma-separated luminance band names or indices')
    parser.add_argument('--hsl_offsets', default=None, help='Global HSL offsets: int,float,float (e.g. 0,0.0,0.0)')
    parser.add_argument('--output', default=None, help='Output HTML file')
    args = parser.parse_args()

    anchors = parse_band_arg(args.hue_anchors, get_hue_anchors())
    variants = get_hue_variants()
    if args.variant:
        vlist = [v.strip() for v in args.variant.split(",") if v.strip() in variants]
        if vlist:
            variants = vlist
    sat_bands = parse_band_arg(args.sat_bands, get_sat_bands())
    lum_bands = parse_band_arg(args.lum_bands, get_lum_bands())

    # Parse global HSL offsets
    # Use HSL_OFFSETS from config if present, else fall back to HUE/SAT/LUM_GLOBAL_OFFSET
    hsl_offsets = _config.get("HSL_OFFSETS", None)
    if hsl_offsets and len(hsl_offsets) == 3:
        h_offset, s_offset, l_offset = hsl_offsets
    else:
        h_offset, s_offset, l_offset = HUE_GLOBAL_OFFSET, SAT_GLOBAL_OFFSET, LUM_GLOBAL_OFFSET

    if args.hsl_offsets:
        parts = args.hsl_offsets.split(",")
        if len(parts) == 3:
            try:
                h_offset = int(parts[0])
                s_offset = float(parts[1])
                l_offset = float(parts[2])
            except Exception:
                pass

    from Chromaspace.cli_utils import get_output_folder, get_output_file
    html_folder = get_output_folder(
        "HTML_OUTPUT", "../output/HTML", with_system_suffix=True
    )
    html_file = args.output or get_output_file(
        "HUE_SQUARES_HTML", "hue_squares.html", with_system_suffix=True
    )
    output_path = os.path.join(html_folder, html_file)
    ensure_output_dir(output_path)

    table_rows = []
    for anchor in anchors:
        row_cells = [f"<th class='anchor-label'>{anchor}</th>"]
        for variant in variants:
            hue = f"{anchor}-{variant}"
            grid_html = build_hue_square(hue, h_offset)
            row_cells.append(
                "<td class='variant-cell'>"
                f"<h2>{hue}</h2>"
                f"{grid_html}"
                "</td>"
            )
        table_rows.append("<tr>" + "".join(row_cells) + "</tr>")

    header_cells = ["<th>Anchor</th>"] + [f"<th>{variant}</th>" for variant in variants]
    big_table = (
        "<table class='mega-grid'>"
        "<thead><tr>" + "".join(header_cells) + "</tr></thead>"
        "<tbody>" + "".join(table_rows) + "</tbody>"
        "</table>"
    )

    html = f"""<!DOCTYPE html>
<html lang='en'>
<head>
<meta charset='UTF-8'>
<title>Hue Squares Preview</title>
<style>
body {{ font-family: sans-serif; }}
h2 {{ margin: 0 0 0.5em 0; font-size: 1rem; }}
.mega-grid {{ border-collapse: collapse; width: 100%; }}
.mega-grid th, .mega-grid td {{ border: 1px solid #ddd; padding: 10px; vertical-align: top; }}
.mega-grid thead th {{ background: #f5f5f5; position: sticky; top: 0; z-index: 1; }}
.anchor-label {{ white-space: nowrap; background: #fafafa; font-weight: 700; }}
.variant-cell table {{ margin: 0; }}
</style>
</head>
<body>
<h1>Preview: Configurable Hue Squares</h1>
<p>Each row is one hue anchor, with all variant tone grids shown side-by-side.</p>
<ul>
<li>HUE_ANCHORS: {', '.join(anchors)}</li>
<li>Variants: {', '.join(variants)}</li>
<li>SAT_BANDS: {', '.join(sat_bands)}</li>
<li>LUM_BANDS: {', '.join(lum_bands)}</li>
<li>Global HSL offsets: {h_offset}, {s_offset}, {l_offset}</li>
</ul>
<hr>
{big_table}
</body>
</html>"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Wrote {output_path}")

if __name__ == "__main__":
    main()
