# Wheel Modes: Saturation and Luminance Wheels

This document explains the two main wheel visualizations in the 36×5×5 colour system.

## Saturation Wheel (`build_sat_wheel(lum)`)
- **Purpose:** Visualizes all hues and saturation bands for a fixed luminance band.
- **Layout:**
  - Hue: Arranged circularly (36 anchors × 2 variants, 10° offset).
  - Saturation: Radial (washed → vivid).
  - Luminance: Fixed.
- **Cell Content:**
  - Colour swatch (inline CSS)
  - Hue label
  - Saturation band
  - HSV values

## Luminance Wheel (`build_lum_wheel(sat)`)
- **Purpose:** Visualizes all hues and luminance bands for a fixed saturation band.
- **Layout:**
  - Hue: Arranged circularly (36 anchors × 2 variants).
  - Luminance: Radial (deep → bright).
  - Saturation: Fixed.
- **Cell Content:**
  - Colour swatch (inline CSS)
  - Hue label
  - Luminance band
  - HSV values

## Usage
- Use the CLI in `scripts/render_wheels.py` to generate all wheels as HTML files.
- See also: `src/colour_system/visualization.py` for implementation details.
