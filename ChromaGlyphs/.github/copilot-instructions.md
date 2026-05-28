# Copilot Instructions - ChromaGlyphs

## Purpose
ChromaGlyphs is the colour-glyph generation and encoding layer for ChromaTutor.
It provides a TypeScript SDK, a compact portable token format (cg1), an SVG renderer, and a JSON Schema.
This file is minimal by design. All general rules, agent edit policies, and centralized log/config options are defined in the modular copilot-instructions files.

Refer to:
- [Modular copilot-instructions](./copilot-instructions.d/*.md) for extensions to the general rules in this file.

## Shared Policies Propagated from dev_local/.github
- Treat this repository as its own root. Do not depend on parent dev_local paths existing on another machine.
- Keep all config, logs, tests, and output locations config-driven. Respect ROOT_MODES, PATHS, LOG_FILES, and any `.d` override directories.
- Never hardcode machine-specific absolute paths.
- Use semantic colour/log keys such as `!info`, `!proc`, `!done`, `!warn`, `!error`, `!path`, `!file`, `!data`, `!test`, `!pass`, `!fail`, and `!date`.
- Keep tests deterministic.
- Update `README.md`, `CHANGELOG.md`, `package.json`, and config version fields together when behavior or releases change.
- Keep changelog dates in `YYYY-MM-DD` format and place substantive docs under `docs/`.

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
