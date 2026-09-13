# ChromaSchemes Engine

This rebuild replaces the prior ChromaSchemes structures with a deterministic geometry-driven engine.

## Design

- Geometry interpretation is pure and isolated in `geometry/`.
- Overlays are deterministic transforms over hue/chroma/luminance vectors.
- Colour generation uses ChromaSpace adapters for RGB/HSV/OKLCH conversion routes.
- Roles bind semantically to Prismata universal role keys.
- Emission and preview model generation are separated from geometry and role logic.
