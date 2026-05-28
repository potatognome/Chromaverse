import { renderSVG } from '../src/renderer';
import { generateGlyph } from '../src/generator';
import { ChromaGlyphError, Glyph } from '../src/types';

describe('renderSVG', () => {
  const glyph = generateGlyph(['#FF6B6B', '#4ECDC4', '#45B7D1']);

  it('returns a string', () => {
    expect(typeof renderSVG(glyph)).toBe('string');
  });

  it('opens with <svg and closes with </svg>', () => {
    const svg = renderSVG(glyph);
    expect(svg.trimStart().startsWith('<svg')).toBe(true);
    expect(svg.trimEnd().endsWith('</svg>')).toBe(true);
  });

  it('includes a <rect> for each palette entry', () => {
    const svg = renderSVG(glyph);
    const matches = svg.match(/<rect/g);
    expect(matches).toHaveLength(glyph.palette.length);
  });

  it('embeds the fill colour of each palette entry', () => {
    const svg = renderSVG(glyph);
    for (const entry of glyph.palette) {
      expect(svg).toContain(`fill="${entry.hex}"`);
    }
  });

  it('applies default swatchSize of 40', () => {
    const svg = renderSVG(glyph);
    expect(svg).toContain('width="40"');
    expect(svg).toContain('height="40"');
  });

  it('respects a custom swatchSize', () => {
    const svg = renderSVG(glyph, { swatchSize: 64 });
    expect(svg).toContain('width="64"');
  });

  it('renders labels when showLabels is true', () => {
    const svg = renderSVG(glyph, { showLabels: true });
    const textTags = svg.match(/<text/g);
    expect(textTags).toHaveLength(glyph.palette.length);
  });

  it('does not render labels by default', () => {
    const svg = renderSVG(glyph);
    expect(svg).not.toContain('<text');
  });

  it('renders grid layout with correct columns', () => {
    const svg = renderSVG(glyph, { layout: 'grid', gridColumns: 2 });
    // Second swatch in 2-column grid should start at x = swatchSize + gap = 44
    expect(svg).toContain('x="44"');
  });

  it('throws ChromaGlyphError for an empty palette', () => {
    const empty: Glyph = {
      format: 'cg1',
      meta: { id: 'z', version: 'cg1', created: new Date().toISOString() },
      palette: [],
    };
    expect(() => renderSVG(empty)).toThrow(ChromaGlyphError);
  });

  it('escapes XML special characters in hex values', () => {
    const glyphWithAmpersand = generateGlyph(['#AABBCC']);
    // Force a special character to test escaping
    (glyphWithAmpersand.palette[0] as { hex: string }).hex = '#AA&BB';
    const svg = renderSVG(glyphWithAmpersand);
    expect(svg).toContain('&amp;');
    expect(svg).not.toContain('&#');
  });
});
