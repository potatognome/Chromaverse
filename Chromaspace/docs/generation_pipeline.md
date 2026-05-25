# Generation Pipeline

1. Iterate all hue anchors and variants
2. For each, iterate all saturation and luminance bands
3. Compute HSV, convert to RGB
4. Find nearest XKCD colour
5. Output as JSON object

See `src/colour_system/generator.py` for implementation.