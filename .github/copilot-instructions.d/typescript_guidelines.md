# TypeScript Guidelines

## What is a `.ts` File?

A `.ts` file is a **TypeScript source file**. TypeScript is a statically-typed superset of
JavaScript that compiles to plain JavaScript. Every `.ts` file in this workspace contains
TypeScript code — types, interfaces, classes, and functions — that is compiled by the
TypeScript compiler (`tsc`) before it runs.

Within Chromaverse, `.ts` files live in the **ChromaGlyphs** module (`ChromaGlyphs/src/`
and `ChromaGlyphs/tests/`). They are compiled to JavaScript in `ChromaGlyphs/dist/` and
are never executed directly in production.

---

## ChromaGlyphs File Layout

```
ChromaGlyphs/
├── src/
│   ├── index.ts        # Public API entry point — re-exports everything consumers need
│   ├── types.ts        # All shared interfaces, branded types, and the error class
│   ├── generator.ts    # generateGlyph() implementation
│   ├── encoder.ts      # encode() implementation
│   ├── decoder.ts      # decode() implementation
│   ├── validator.ts    # validate() implementation
│   ├── renderer.ts     # renderSVG() / renderPNG() implementation
│   └── schemas/        # JSON Schema files used for validation
├── tests/
│   ├── encoder.test.ts
│   ├── decoder.test.ts
│   ├── validator.test.ts
│   └── renderer.test.ts
├── tsconfig.json       # Compiler options (target ES2019, strict mode)
└── eslint.config.mjs   # Lint rules (@typescript-eslint)
```

---

## Key Conventions

### Types first
All shared types, interfaces, and branded primitives belong in `src/types.ts`.
Implementation files import from `types.ts` and must not re-declare types locally.

### Strict mode
`tsconfig.json` enables `"strict": true`. Every function must have explicit parameter
and return types. `any` is discouraged; use `unknown` and narrow where necessary.

### Branded primitives
Opaque string types (e.g. `HexColor`, `GlyphToken`) use the TypeScript brand pattern:

```typescript
type HexColor = string & { readonly __brand: 'HexColor' };
```

Cast using `as HexColor` only at validated entry points (e.g. after a regex check).

### One responsibility per file
Each `src/*.ts` module exports exactly one public function (or a closely-related pair).
Keep files short and focused; cross-file dependencies go through `src/index.ts`.

### Error handling
Throw `ChromaGlyphError` (exported from `src/types.ts`) for all domain errors.
Never throw plain `Error` from ChromaGlyphs public API functions.

### Tests
Test files live in `tests/` and follow the Jest naming convention `*.test.ts`.
The `tsconfig.json` excludes `tests/` from compilation; Jest uses `ts-jest` directly.

---

## Build and Lint Commands

```bash
cd ChromaGlyphs
npm ci               # Install dependencies
npm run build        # tsc — compiles src/ → dist/
npm test             # Jest with ts-jest
npm run lint         # ESLint (@typescript-eslint rules)
npm run typecheck    # tsc --noEmit (type-check without emitting files)
```

---

## References

- [ChromaGlyphs README](../../ChromaGlyphs/README.md)
- [Glyph Format Specification](../../ChromaGlyphs/docs/glyph-format.md)
- [TypeScript compiler options](../../ChromaGlyphs/tsconfig.json)
- [ESLint config](../../ChromaGlyphs/eslint.config.mjs)
