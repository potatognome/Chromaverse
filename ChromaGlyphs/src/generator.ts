/**
 * ChromaGlyphs – generator.
 *
 * Creates new `Glyph` objects from raw palette inputs, auto-assigning
 * UUIDs and timestamps so callers do not need to manage identity manually.
 */

import { Glyph, GlyphMeta, ColorEntry, HexColor, ChromaGlyphError } from './types';

const HEX_RE = /^#(?:[0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/;
const MAX_PALETTE_SIZE = 16;
const MIN_PALETTE_SIZE = 1;

/** Generates a UUID v4 using the built-in `crypto` module (Node ≥ 14.17). */
function uuidV4(): string {
  return crypto.randomUUID();
}

/** Returns the current UTC timestamp as an ISO-8601 string. */
function nowISO(): string {
  return new Date().toISOString();
}

/**
 * Creates a new `Glyph` from a palette of hex colour strings.
 *
 * @param palette  - Array of 1–16 hex colour strings (e.g. `"#FF6B6B"`).
 * @param meta     - Optional metadata overrides (id, author, tags, etc.).
 * @returns A fully-populated `Glyph` object.
 * @throws {ChromaGlyphError} If the palette is empty, too large, or contains invalid hex values.
 */
export function generateGlyph(
  palette: string[],
  meta?: Partial<Omit<GlyphMeta, 'version'>>,
): Glyph {
  if (!Array.isArray(palette) || palette.length < MIN_PALETTE_SIZE) {
    throw new ChromaGlyphError(
      `Palette must contain at least ${MIN_PALETTE_SIZE} colour(s).`,
    );
  }

  if (palette.length > MAX_PALETTE_SIZE) {
    throw new ChromaGlyphError(
      `Palette must not exceed ${MAX_PALETTE_SIZE} colours (got ${palette.length}).`,
    );
  }

  const entries: ColorEntry[] = palette.map((hex, idx) => {
    if (typeof hex !== 'string' || !HEX_RE.test(hex)) {
      throw new ChromaGlyphError(
        `palette[${idx}] is not a valid hex colour: "${hex}".`,
      );
    }
    return { hex: hex as HexColor };
  });

  const resolvedMeta: GlyphMeta = {
    id: meta?.id ?? uuidV4(),
    version: 'cg1',
    created: meta?.created ?? nowISO(),
    ...(meta?.author !== undefined ? { author: meta.author } : {}),
    ...(meta?.tags !== undefined ? { tags: meta.tags } : {}),
  };

  return {
    format: 'cg1',
    meta: resolvedMeta,
    palette: entries,
  };
}
