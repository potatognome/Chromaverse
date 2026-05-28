# ChromaGlyphs

ChromaGlyphs is a standalone TypeScript module that generates compact, human-readable
colour glyphs, encodes/decodes them, and exposes a stable API for ChromaTutor to render,
validate, and persist glyphs.

## Features

- **Generate** colour glyphs from any palette of hex colours
- **Encode / Decode** glyphs to a compact portable token (`CG1:<base64url>`)
- **Validate** glyphs against a strict JSON Schema
- **Render** glyphs as SVG swatches (PNG export via optional peer dependency)
- **TypeScript-first** – full type definitions included
- **JSON Schema** for language-agnostic integration

## Installation

```bash
npm install chromaglyphs
```

## Quick Start

```typescript
import { generateGlyph, encode, decode, renderSVG } from 'chromaglyphs';

// 1. Generate a glyph from a palette
const glyph = generateGlyph(['#FF6B6B', '#4ECDC4', '#45B7D1'], {
  author: 'ChromaTutor',
  tags: ['warm', 'cool'],
});

// 2. Encode to a portable token
const token = encode(glyph);
console.log(token);
// => "CG1:eyJ2IjoiY2cxIiwi..."

// 3. Decode back
const decoded = decode(token);

// 4. Render as SVG
const svg = renderSVG(glyph, { swatchSize: 48, layout: 'row' });
document.body.innerHTML = svg;
```

## API

### `generateGlyph(palette, meta?)`

Creates a new `Glyph` from an array of hex colour strings.

| Param   | Type                    | Description                        |
|---------|-------------------------|------------------------------------|
| palette | `HexColor[]`            | 1–16 hex colour strings            |
| meta    | `Partial<GlyphMeta>`    | Optional metadata overrides        |

Returns `Glyph`.

### `encode(glyph)`

Encodes a `Glyph` to a compact `GlyphToken` string (`CG1:<base64url>`).

### `decode(token)`

Decodes a `GlyphToken` back to a `Glyph`. Throws `ChromaGlyphError` on invalid input.

### `validate(glyph)`

Validates a `Glyph` against the JSON Schema.

Returns `ValidationResult { valid: boolean; errors: string[] }`.

### `renderSVG(glyph, options?)`

Renders a `Glyph` as an SVG string.

| Option      | Type                       | Default   | Description                    |
|-------------|----------------------------|-----------|--------------------------------|
| swatchSize  | `number`                   | `40`      | Width/height of each swatch    |
| layout      | `'row' \| 'grid'`          | `'row'`   | Swatch layout direction        |
| gap         | `number`                   | `4`       | Gap between swatches (px)      |
| showLabels  | `boolean`                  | `false`   | Render colour labels below     |
| gridColumns | `number`                   | `4`       | Columns when layout is 'grid'  |

Returns `string` (SVG markup).

### `renderPNG(glyph, options?)`

Renders a `Glyph` to a PNG `Buffer`. Requires the optional `sharp` peer dependency.

## Glyph Format

See [docs/glyph-format.md](./docs/glyph-format.md) for the full specification.

## Development

```bash
npm ci           # Install dependencies
npm run build    # Compile TypeScript
npm test         # Run Jest tests
npm run lint     # ESLint
npm run typecheck  # tsc --noEmit
```

## CI

GitHub Actions runs lint, type-check, and tests on every push and pull request.
See [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

## Integration with ChromaTutor

Import `chromaglyphs` as a dependency in the ChromaTutor frontend package.
Use `generateGlyph` → `encode` to persist glyphs, and `decode` → `renderSVG` to display them.
The exported JSON Schema (`src/schemas/glyph.schema.json`) can be used for server-side validation.

## License

MIT © potatognome
