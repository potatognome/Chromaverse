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

/**
 * Re-export the public glyph generation, token, validation, and rendering API
 * from a single barrel entry point.
 */
export { ChromaGlyphError } from './types';
export { generateGlyph } from './generator';
export { encode } from './encoder';
export { decode } from './decoder';
export { validate } from './validator';
export { renderSVG, renderPNG } from './renderer';
