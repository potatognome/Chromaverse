# Tone Grid: 5×5 Hue Squares

This document explains the 5×5 tone grid visualization for a single hue in the 36×5×5 colour system.

## Hue Square (`build_hue_square(hue)`)
- **Purpose:** Visualizes all 25 tone descriptors (saturation × luminance) for a single hue.
- **Layout:**
  - Rows: Saturation bands (washed → vivid)
  - Columns: Luminance bands (deep → bright)
- **Cell Content:**
  - Colour swatch (inline CSS)
  - Sat-lum descriptor
  - HSV values

## Usage
- Use the CLI in `scripts/render_tone_grid.py` to generate all hue squares as HTML files.
- See also: `src/colour_system/visualization.py` for implementation details.
