/**
 * ChromaGlyphs – public API entry point.
 *
 * Re-exports all public types, functions, and the error class so that
 * consumers can import everything from a single `'chromaglyphs'` specifier.
 */

export type {
  HexColor,
  GlyphToken,
  ColorEntry,
  GlyphMeta,
  Glyph,
  ValidationResult,
  SwatchLayout,
  RenderOptions,
} from './types';

/** Re-export the shared ChromaGlyphs error type. */
export { ChromaGlyphError } from './types';
/** Re-export glyph generation, encoding, and decoding helpers. */
export { generateGlyph } from './generator';
/** Re-export glyph token encoding. */
export { encode } from './encoder';
/** Re-export glyph token decoding. */
export { decode } from './decoder';
/** Re-export validation and rendering helpers. */
export { validate } from './validator';
/** Re-export SVG and PNG renderers. */
export { renderSVG, renderPNG } from './renderer';
