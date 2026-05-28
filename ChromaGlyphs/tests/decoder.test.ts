import { encode } from '../src/encoder';
import { decode } from '../src/decoder';
import { generateGlyph } from '../src/generator';
import { ChromaGlyphError, GlyphToken } from '../src/types';

describe('decode', () => {
  const original = generateGlyph(['#FF6B6B', '#4ECDC4', '#45B7D1'], {
    id: 'decode-test-001',
    author: 'tester',
    tags: ['cool'],
  });

  it('round-trips a glyph through encode → decode', () => {
    const token = encode(original);
    const decoded = decode(token);
    expect(decoded.format).toBe('cg1');
    expect(decoded.meta.id).toBe('decode-test-001');
    expect(decoded.meta.author).toBe('tester');
    expect(decoded.meta.tags).toEqual(['cool']);
    expect(decoded.palette.map((e) => e.hex)).toEqual(['#FF6B6B', '#4ECDC4', '#45B7D1']);
  });

  it('preserves optional label and annotation fields', () => {
    const glyphWithLabels = generateGlyph(['#FF6B6B']);
    glyphWithLabels.palette[0].label = 'coral';
    glyphWithLabels.palette[0].annotation = 'warm primary';
    const token = encode(glyphWithLabels);
    const decoded = decode(token);
    expect(decoded.palette[0].label).toBe('coral');
    expect(decoded.palette[0].annotation).toBe('warm primary');
  });

  it('throws ChromaGlyphError for a token without the CG1: prefix', () => {
    expect(() => decode('INVALID' as GlyphToken)).toThrow(ChromaGlyphError);
  });

  it('throws ChromaGlyphError for a token with invalid base64url payload', () => {
    expect(() => decode('CG1:!!!' as GlyphToken)).toThrow(ChromaGlyphError);
  });

  it('throws ChromaGlyphError for an unsupported format version', () => {
    const badPayload = Buffer.from(JSON.stringify({ v: 'cg99', id: 'x', ts: new Date().toISOString(), p: [{ h: '#000' }] })).toString('base64url');
    expect(() => decode(`CG1:${badPayload}` as GlyphToken)).toThrow(ChromaGlyphError);
  });

  it('throws ChromaGlyphError for a payload with an empty palette', () => {
    const badPayload = Buffer.from(JSON.stringify({ v: 'cg1', id: 'x', ts: new Date().toISOString(), p: [] })).toString('base64url');
    expect(() => decode(`CG1:${badPayload}` as GlyphToken)).toThrow(ChromaGlyphError);
  });
});
