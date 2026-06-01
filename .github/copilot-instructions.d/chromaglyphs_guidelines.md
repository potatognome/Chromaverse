# ChromaGlyphs Guidelines

ChromaGlyphs is the colour-glyph generation and encoding layer for ChromaTutor.
It provides a TypeScript SDK, a compact portable token format (cg1), an SVG renderer, and a JSON Schema.

## Project-Specific Rules

- All public API changes must update the TypeScript types in `src/types.ts` and the JSON Schema in `src/schemas/glyph.schema.json` together.
- The `cg1` token format is a public contract: backward-incompatible changes require a new format version (e.g., `cg2`).
- The `encode` / `decode` pair must always be a lossless round-trip.
- Glyph palettes are capped at 16 entries; this limit is enforced in both the generator and the validator.
- SVG output must be well-formed XML and safe for embedding in HTML without sanitisation.
- Keep `sharp` as an optional peer dependency for PNG export only.

## Building Exemplar Policy

The `examples/` folder must include supplementary scripts that run outside Jest and stress public APIs and edge cases.

Requirements:
- Exercise all public functions across normal and adversarial input scenarios.
- Deliberately stress edge cases (empty input, oversized palette, bad hex values, malformed tokens).
- Produce structured console output for human review.
- Keep scripts as living behaviour documentation.
- Maintain an `examples/exemplar.ts` mock application entry point.
