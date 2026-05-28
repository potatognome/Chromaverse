/**
 * ChromaGlyphs – decoder.
 *
 * Parses a `GlyphToken` back into a fully-resolved `Glyph` object.
 * Throws `ChromaGlyphError` for any malformed or unsupported token.
 */

import { Glyph, GlyphToken, HexColor, ChromaGlyphError } from './types';

const TOKEN_PREFIX = 'CG1:';

/** Internal wire payload (mirrors encoder.ts WirePayload). */
interface WirePayload {
  v: string;
  id: string;
  ts: string;
  au?: string;
  t?: string[];
  p: Array<{ h: string; l?: string; a?: string }>;
}

/**
 * Decodes a `GlyphToken` into a `Glyph`.
 *
 * @param token - A token produced by `encode()`.
 * @returns The decoded `Glyph`.
 * @throws {ChromaGlyphError} If the token is malformed, unsupported, or fails structural checks.
 */
export function decode(token: GlyphToken): Glyph {
  if (typeof token !== 'string' || !token.startsWith(TOKEN_PREFIX)) {
    throw new ChromaGlyphError(
      `Invalid token: must start with "${TOKEN_PREFIX}". Got: ${String(token).slice(0, 32)}`,
    );
  }

  const b64 = token.slice(TOKEN_PREFIX.length);

  let raw: unknown;
  try {
    const json = Buffer.from(b64, 'base64url').toString('utf8');
    raw = JSON.parse(json);
  } catch {
    throw new ChromaGlyphError('Token payload is not valid base64url-encoded JSON.');
  }

  const wire = raw as WirePayload;

  if (wire.v !== 'cg1') {
    throw new ChromaGlyphError(`Unsupported glyph format version: "${wire.v}".`);
  }

  if (typeof wire.id !== 'string' || wire.id.trim() === '') {
    throw new ChromaGlyphError('Token payload is missing a valid "id" field.');
  }

  if (typeof wire.ts !== 'string' || wire.ts.trim() === '') {
    throw new ChromaGlyphError('Token payload is missing a valid "ts" (timestamp) field.');
  }

  if (!Array.isArray(wire.p) || wire.p.length === 0) {
    throw new ChromaGlyphError('Token payload palette ("p") must be a non-empty array.');
  }

  const glyph: Glyph = {
    format: 'cg1',
    meta: {
      id: wire.id,
      version: wire.v,
      created: wire.ts,
      ...(wire.au !== undefined ? { author: wire.au } : {}),
      ...(Array.isArray(wire.t) ? { tags: wire.t } : {}),
    },
    palette: wire.p.map((entry, idx) => {
      if (typeof entry.h !== 'string' || entry.h.trim() === '') {
        throw new ChromaGlyphError(`Palette entry at index ${idx} is missing a hex colour ("h").`);
      }
      return {
        hex: entry.h as HexColor,
        ...(typeof entry.l === 'string' ? { label: entry.l } : {}),
        ...(typeof entry.a === 'string' ? { annotation: entry.a } : {}),
      };
    }),
  };

  return glyph;
}
