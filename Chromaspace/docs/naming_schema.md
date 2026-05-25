# Naming Schema

- Primary name: `<hueanchor-variant> <satword-lumword>`
- Machine fields: `hue_anchor`, `hue_variant`, `sat_band`, `lum_band`
- Numeric band tag: `Sat_<low-high>_Lum_<low-high>`
- Each entry includes HSV, RGB, and nearest XKCD match

Example:
```json
{
  "name": "red-warm vivid-bright",
  "hue_anchor": "red",
  "hue_variant": "warm",
  "sat_band": "vivid",
  "lum_band": "bright",
  "bands": {"sat": 4, "lum": 4},
  "hsv": [350, 0.9, 0.9],
  "rgb": [230, 23, 23],
  "xkcd_match": {"name": "red", "distance": 5.2}
}
```
