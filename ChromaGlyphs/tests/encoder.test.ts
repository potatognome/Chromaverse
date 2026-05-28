import { encode } from '../src/encoder';
import { generateGlyph } from '../src/generator';
import { ChromaGlyphError } from '../src/types';

describe('encode', () => {
  const glyph = generateGlyph(['#FF6B6B', '#4ECDC4'], {
    id: 'test-id-001',
    author: 'test',
    tags: ['warm'],
  });

  it('returns a string beginning with "CG1:"', () => {
    const token = encode(glyph);
    expect(typeof token).toBe('string');
    expect(token.startsWith('CG1:')).toBe(true);
  });

  it('produces a valid base64url payload', () => {
    const token = encode(glyph);
    const b64 = token.slice(4);
    // base64url characters only
    expect(/^[A-Za-z0-9_-]+=*$/.test(b64)).toBe(true);
  });

  it('encodes palette colours', () => {
    const token = encode(glyph);
    const b64 = token.slice(4);
    const json = Buffer.from(b64, 'base64url').toString('utf8');
    const parsed = JSON.parse(json) as { p: Array<{ h: string }> };
    expect(parsed.p.map((e) => e.h)).toEqual(['#FF6B6B', '#4ECDC4']);
  });

  it('omits optional fields when absent', () => {
    const minimal = generateGlyph(['#AABBCC']);
    const token = encode(minimal);
    const b64 = token.slice(4);
    const parsed = JSON.parse(Buffer.from(b64, 'base64url').toString('utf8')) as Record<string, unknown>;
    expect(parsed).not.toHaveProperty('au');
    expect(parsed).not.toHaveProperty('t');
  });

  it('includes author when provided', () => {
    const token = encode(glyph);
    const b64 = token.slice(4);
    const parsed = JSON.parse(Buffer.from(b64, 'base64url').toString('utf8')) as { au?: string };
    expect(parsed.au).toBe('test');
  });

  it('throws ChromaGlyphError for invalid input', () => {
    expect(() => encode(null as unknown as ReturnType<typeof generateGlyph>)).toThrow(ChromaGlyphError);
  });
});
