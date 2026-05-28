# Building Examples Policy – ChromaGlyphs

The `examples/` folder holds scripts that run outside Jest and serve as living behaviour documentation.

## Requirements

- `examples/exemplar.ts` is the primary entry point, runnable via `npx ts-node examples/exemplar.ts`.
- Each exemplar must exercise all public API functions.
- Include adversarial / edge-case scenarios: empty palette, oversized palette, invalid hex values, malformed tokens, unsupported format versions.
- Produce structured, labelled console output so a human reviewer can verify correct behaviour at a glance.
- Scripts must not depend on test infrastructure (Jest, ts-jest) – they run standalone.
- Keep examples in sync with the README usage section.
