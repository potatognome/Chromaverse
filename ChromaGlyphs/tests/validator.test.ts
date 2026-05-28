import { validate } from '../src/validator';
import { generateGlyph } from '../src/generator';
import { Glyph } from '../src/types';

describe('validate', () => {
  it('returns valid for a well-formed glyph', () => {
    const glyph = generateGlyph(['#FF6B6B', '#4ECDC4']);
    const result = validate(glyph);
    expect(result.valid).toBe(true);
    expect(result.errors).toHaveLength(0);
  });

  it('accepts a 3-digit hex shorthand', () => {
    const glyph = generateGlyph(['#ABC']);
    const result = validate(glyph);
    expect(result.valid).toBe(true);
  });

  it('rejects a glyph with an invalid hex value', () => {
    const glyph = generateGlyph(['#FF6B6B']);
    // Force an invalid value bypassing the generator guard
    (glyph.palette[0] as { hex: string }).hex = 'notahex';
    const result = validate(glyph);
    expect(result.valid).toBe(false);
    expect(result.errors.some((e) => e.includes('notahex'))).toBe(true);
  });

  it('rejects a glyph with wrong format version', () => {
    const glyph = generateGlyph(['#FFFFFF']);
    (glyph as { format: string }).format = 'cg99';
    const result = validate(glyph);
    expect(result.valid).toBe(false);
    expect(result.errors.some((e) => e.includes('cg99'))).toBe(true);
  });

  it('rejects a palette exceeding 16 entries', () => {
    const palette = Array.from({ length: 17 }, (_, i) => `#${String(i).padStart(2, '0')}AABB`);
    // Construct directly to bypass generator guard
    const glyph: Glyph = {
      format: 'cg1',
      meta: { id: 'x', version: 'cg1', created: new Date().toISOString() },
      palette: palette.map((h) => ({ hex: h as import('../src/types').HexColor })),
    };
    const result = validate(glyph);
    expect(result.valid).toBe(false);
    expect(result.errors.some((e) => e.includes('16'))).toBe(true);
  });

  it('rejects an empty palette', () => {
    const glyph: Glyph = {
      format: 'cg1',
      meta: { id: 'y', version: 'cg1', created: new Date().toISOString() },
      palette: [],
    };
    const result = validate(glyph);
    expect(result.valid).toBe(false);
  });
});
