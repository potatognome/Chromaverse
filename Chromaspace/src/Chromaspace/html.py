"""HTML helpers for colour system visualizations."""

def _format_xkcd_match(xkcd_match):
    """Render XKCD match as a compact value string."""
    if not xkcd_match:
        return ""
    if isinstance(xkcd_match, dict):
        name = xkcd_match.get("name", "")
        distance = xkcd_match.get("distance")
        if distance is None:
            return str(name)
        return f"{name} ({float(distance):.1f})"
    return str(xkcd_match)

def swatch_cell(rgb, label, hsv, xkcd_match=None, extra=None):
    style = (
        "background: rgb({0}, {1}, {2}); width: 88px; min-width: 88px; "
        "height: 32px; text-align: center; border: 1px solid #ccc;"
    ).format(rgb[0], rgb[1], rgb[2])
    hsv_str = f"HSV: {hsv}"
    rgb_str = f"RGB: {rgb}"
    extra_str = f"<br>{extra}" if extra else ""
    xkcd_value = _format_xkcd_match(xkcd_match)
    xkcd_str = f"<br>XKCD: {xkcd_value}" if xkcd_value else ""
    return (
        f"<td style='{style}' title='{label}'>"
        f"<div style='font-size:10px; min-width: 140px'>{label}{extra_str}"
        f"{xkcd_str}<br>{hsv_str}<br>{rgb_str}</div></td>"
    )

def build_html_table(rows, header=None, row_labels=None, title=None):
    html = (
        "<table style='border-collapse:collapse; margin:1em 0;'>"
        "<style>th, td { min-width: 140px; padding: 6px 10px; }</style>"
    )
    if title:
        html += f"<caption style='font-weight:bold; font-size:1.2em; margin-bottom:0.5em'>{title}</caption>"
    if header:
        html += "<tr>"
        if row_labels:
            html += "<th></th>"
        for h in header:
            html += f"<th>{h}</th>"
        html += "</tr>"
    for i, row in enumerate(rows):
        html += "<tr>"
        if row_labels:
            html += f"<th>{row_labels[i]}</th>"
        for cell in row:
            html += cell
        html += "</tr>"
    html += "</table>"
    return html
