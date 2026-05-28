/**
 * ChromaGlyphs – encoder.
 *
 * Serialises a `Glyph` object into a compact, URL-safe `GlyphToken` string
 * of the form `CG1:<base64url(JSON)>`.
 */

import { Glyph, GlyphToken, ChromaGlyphError } from './types';

/** Internal wire payload (compact field names to reduce token size). */
interface WirePayload {
  v: string;
  id: string;
  ts: string;
  au?: string;
  t?: string[];
  p: Array<{ h: string; l?: string; a?: string }>;
}

/**
 * Encodes a `Glyph` to a portable `GlyphToken`.
 *
 * @param glyph - The glyph to encode.
 * @returns A `GlyphToken` string (`CG1:<base64url>`).
 * @throws {ChromaGlyphError} If the glyph cannot be serialised.
 */
export function encode(glyph: Glyph): GlyphToken {
  try {
    const payload: WirePayload = {
      v: glyph.format,
      id: glyph.meta.id,
      ts: glyph.meta.created,
      p: glyph.palette.map((entry) => {
        const wire: { h: string; l?: string; a?: string } = { h: entry.hex };
        if (entry.label !== undefined) wire.l = entry.label;
        if (entry.annotation !== undefined) wire.a = entry.annotation;
        return wire;
      }),
    };

    if (glyph.meta.author !== undefined) payload.au = glyph.meta.author;
    if (glyph.meta.tags !== undefined && glyph.meta.tags.length > 0) {
      payload.t = glyph.meta.tags;
    }

    const json = JSON.stringify(payload);
    const b64 = Buffer.from(json, 'utf8').toString('base64url');
    return `CG1:${b64}` as GlyphToken;
  } catch (err) {
    throw new ChromaGlyphError(
      `Failed to encode glyph: ${err instanceof Error ? err.message : String(err)}`,
    );
  }
}
