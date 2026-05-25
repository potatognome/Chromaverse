import json
import argparse
import os
import math
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Colour Preview</title>
    <style>
        body {{ font-family: sans-serif; }}
        .swatch {{ width: 60px; height: 30px; display: inline-block; margin: 2px; border: 1px solid #ccc; }}
        table {{ border-collapse: collapse; margin-bottom: 2em; }}
        th, td {{ padding: 6px 10px; text-align: center; min-width: 120px; }}
        .wheel-container {{ text-align: center; margin: 2em 0; }}
    </style>
</head>
<body>
    <h1>Colour Preview</h1>
    <div class="wheel-container">
        <svg width="420" height="420" viewBox="0 0 420 420">
            <g>
                {wheel_svg}
            </g>
        </svg>
    </div>
    <h2>Colour Table</h2>
    <table border="1">
        <tr>
            <th>Swatch</th>
            <th>Name</th>
            <th>RGB</th>
            <th>HSV</th>
            <th>SAT</th>
            <th>LUM</th>
            <th>XKCD</th>
        </tr>
        {rows}
    </table>
</body>
</html>
'''

def rgb_str(rgb):
    return f"rgb({rgb[0]}, {rgb[1]}, {rgb[2]})"


def format_xkcd_value(xkcd_match):
    if not xkcd_match:
        return ""
    if isinstance(xkcd_match, dict):
        name = xkcd_match.get('name', '')
        distance = xkcd_match.get('distance')
        if distance is None:
            return str(name)
        return f"{name} ({float(distance):.1f})"
    return str(xkcd_match)

def make_table_rows(colours):
    rows = []
    for c in colours:
        rgb = c['rgb']
        hsv = c.get('hsv', ['-', '-', '-'])
        xkcd_value = format_xkcd_value(c.get('xkcd_match', ''))
        row = f"""
        <tr>
            <td><span class='swatch' style='background:{rgb_str(rgb)}'></span></td>
            <td>{c['name']}</td>
            <td>{rgb}</td>
            <td>{[round(x,2) for x in hsv]}</td>
            <td>{c.get('sat_band','')}</td>
            <td>{c.get('lum_band','')}</td>
            <td>{xkcd_value}</td>
        </tr>"""
        rows.append(row)
    return '\n'.join(rows)

def make_wheel_svg(colours):
    # Place each colour on a wheel by its hue (if available), else just spread evenly
    cx, cy, r = 210, 210, 180
    points = []
    for c in colours:
        hsv = c.get('hsv')
        if hsv:
            h = hsv[0]  # 0-1
            angle = h * 2 * math.pi
        else:
            angle = (len(points) / max(1, len(colours))) * 2 * math.pi
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        rgb = c['rgb']
        points.append(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='18' fill='{rgb_str(rgb)}' stroke='#333' stroke-width='1'><title>{c['name']}</title></circle>")
    return '\n'.join(points)

def main():
    parser = argparse.ArgumentParser(description='Preview a set of colours as HTML table and wheel.')
    parser.add_argument('input', nargs='?', default=None, help='Input JSON file (filtered set)')
    parser.add_argument('--output', default=None, help='Output HTML file (default: config or same as input, .html)')
    args = parser.parse_args()

    from Chromaspace.config import _config
    from Chromaspace.cli_utils import ensure_output_dir
    input_path = args.input or _config["PATHS"]["FILES"]["COLOUR_SYSTEM_JSON"]
    output_path = (
        args.output
        or _config["PATHS"]["FILES"].get("PREVIEW_HTML")
        or os.path.splitext(input_path)[0] + '.html'
    )
    ensure_output_dir(output_path)
    with open(input_path, 'r', encoding='utf-8') as f:
        colours = json.load(f)

    rows = make_table_rows(colours)
    wheel_svg = make_wheel_svg(colours)
    html = HTML_TEMPLATE.format(rows=rows, wheel_svg=wheel_svg)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"HTML preview written to {output_path}")

if __name__ == '__main__':
    main()
