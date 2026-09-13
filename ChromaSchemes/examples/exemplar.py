#!/usr/bin/env python3
"""examples/exemplar.py - ChromaSchemes exemplar mock entry point."""

from __future__ import annotations

import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve()
PROJECT_ROOT = HERE.parents[1]
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

from Chromaschemes import ChromaSchemesEngine  # noqa: E402


def main() -> int:
    engine = ChromaSchemesEngine()
    payload = {
        "baseColour": {"hex": "#FF78C8", "space": "rgb"},
        "geometryModel": "quadratic",
        "overlays": [{"type": "harmonic", "params": {"rotation": 45}}, {"type": "chroma_spiral", "params": {"step": 0.01}}],
        "desiredColourCount": 8,
    }

    output_path = PROJECT_ROOT / "samples" / "generated.exemplar.scheme.yaml"
    emitted = engine.emit(payload, output_path)

    print("ChromaSchemes exemplar output:")
    print(json.dumps(engine.generate(payload), indent=2))
    print(f"Wrote {emitted}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
