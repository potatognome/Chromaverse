# ChromaSchemes

ChromaSchemes is the deterministic colour-scheme engine for Chromaverse.

## Engine Layout

- `core/` — generation pipeline and deterministic orchestration
- `models/` — canonical input/output model helpers
- `geometry/` — pure geometry and overlay primitives
- `output/` — ChromaScheme output emission
- `tooling/` — required TypeScript interfaces and module primitives
- `samples/` — canonical sample outputs
- `docs/` — input/output schemas and engine notes

## Quick Start

```python
from pathlib import Path
from core import ChromaSchemesEngine

engine = ChromaSchemesEngine()
payload = {
    "baseColour": {"hex": "#FF78C8", "space": "rgb"},
    "geometryModel": "quadratic",
    "overlays": [{"type": "harmonic", "params": {"rotation": 45}}],
    "desiredColourCount": 8,
}
engine.emit(payload, Path("samples/generated.scheme.yaml"))
```
