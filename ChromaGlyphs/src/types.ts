/**
 * ChromaGlyphs – core TypeScript types.
 *
 * All public interfaces and branded types live here so that consumers can
 * import them without pulling in implementation code.
 */

// ---------------------------------------------------------------------------
// Branded primitives
// ---------------------------------------------------------------------------

/** A CSS-style hex colour string, e.g. `"#FF6B6B"` or `"#abc"`. */
export type HexColor = string & { readonly __brand: 'HexColor' };

/** An opaque encoded glyph token of the form `"CG1:<base64url>"`. */
export type GlyphToken = string & { readonly __brand: 'GlyphToken' };

// ---------------------------------------------------------------------------
// Palette
// ---------------------------------------------------------------------------

/** A single colour entry within a glyph palette. */
export interface ColorEntry {
  /** Hex colour value, e.g. `"#FF6B6B"`. */
  hex: HexColor;
  /** Human-readable label for the colour. */
  label?: string;
  /** Freeform annotation (usage note, mood tag, etc.). */
  annotation?: string;
}

// ---------------------------------------------------------------------------
// Metadata
// ---------------------------------------------------------------------------

/** Glyph metadata block. */
export interface GlyphMeta {
  /** Unique glyph identifier (UUID v4). */
  id: string;
  /** Format version string – always `"cg1"` for this release. */
  version: string;
  /** ISO-8601 creation timestamp. */
  created: string;
  /** Optional author name or identifier. */
  author?: string;
  /** Optional free-form tags for search and categorisation. */
  tags?: string[];
}

// ---------------------------------------------------------------------------
// Glyph
// ---------------------------------------------------------------------------

/** A fully-resolved ChromaGlyph object. */
export interface Glyph {
  /** Format version – always `"cg1"`. */
  format: 'cg1';
  /** Glyph metadata. */
  meta: GlyphMeta;
  /** Ordered colour palette (1–16 entries). */
  palette: ColorEntry[];
}

// ---------------------------------------------------------------------------
// Validation
// ---------------------------------------------------------------------------

/** Result returned by `validate()`. */
export interface ValidationResult {
  /** Whether the glyph passed all validation rules. */
  valid: boolean;
  /** Human-readable error messages when `valid` is `false`. */
  errors: string[];
}

// ---------------------------------------------------------------------------
// Rendering
// ---------------------------------------------------------------------------

/** Layout direction for SVG swatch rendering. */
export type SwatchLayout = 'row' | 'grid';

/** Options accepted by `renderSVG()` and `renderPNG()`. */
export interface RenderOptions {
  /** Width/height of each colour swatch in pixels. Default: `40`. */
  swatchSize?: number;
  /** Layout direction. Default: `'row'`. */
  layout?: SwatchLayout;
  /** Gap between swatches in pixels. Default: `4`. */
  gap?: number;
  /** Render hex labels below each swatch. Default: `false`. */
  showLabels?: boolean;
  /** Number of columns when `layout` is `'grid'`. Default: `4`. */
  gridColumns?: number;
}

// ---------------------------------------------------------------------------
// Errors
// ---------------------------------------------------------------------------

/** Base error class for ChromaGlyphs operations. */
export class ChromaGlyphError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'ChromaGlyphError';
  }
}
