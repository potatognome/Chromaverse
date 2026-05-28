/**
 * ChromaGlyphs – SVG renderer.
 *
 * Converts a `Glyph` into an SVG string.  An optional PNG export helper
 * is provided as a thin wrapper that delegates to the `sharp` peer dependency
 * when it is available.
 */

import { Glyph, RenderOptions, ChromaGlyphError } from './types';

const DEFAULTS: Required<RenderOptions> = {
  swatchSize: 40,
  layout: 'row',
  gap: 4,
  showLabels: false,
  gridColumns: 4,
};

/**
 * Renders a `Glyph` as an SVG string.
 *
 * @param glyph   - The glyph to render.
 * @param options - Optional render configuration.
 * @returns SVG markup as a string.
 * @throws {ChromaGlyphError} If the glyph palette is empty.
 */
export function renderSVG(glyph: Glyph, options?: RenderOptions): string {
  const opts: Required<RenderOptions> = { ...DEFAULTS, ...options };

  if (!glyph.palette || glyph.palette.length === 0) {
    throw new ChromaGlyphError('Cannot render a glyph with an empty palette.');
  }

  const { swatchSize, layout, gap, showLabels, gridColumns } = opts;
  const labelHeight = showLabels ? 16 : 0;
  const cellH = swatchSize + labelHeight;
  const count = glyph.palette.length;

  let totalW: number;
  let totalH: number;
  let positions: Array<{ x: number; y: number }>;

  if (layout === 'grid') {
    const cols = Math.min(gridColumns, count);
    const rows = Math.ceil(count / cols);
    totalW = cols * swatchSize + (cols - 1) * gap;
    totalH = rows * cellH + (rows - 1) * gap;
    positions = glyph.palette.map((_, i) => ({
      x: (i % cols) * (swatchSize + gap),
      y: Math.floor(i / cols) * (cellH + gap),
    }));
  } else {
    totalW = count * swatchSize + (count - 1) * gap;
    totalH = cellH;
    positions = glyph.palette.map((_, i) => ({
      x: i * (swatchSize + gap),
      y: 0,
    }));
  }

  const swatches = glyph.palette
    .map((entry, i) => {
      const { x, y } = positions[i];
      const hex = entry.hex;
      const title = entry.label ?? hex;
      const rectTitle = `<title>${escapeXml(title)}</title>`;
      const rect = `<rect x="${x}" y="${y}" width="${swatchSize}" height="${swatchSize}" fill="${escapeXml(hex)}" rx="3" ry="3">${rectTitle}</rect>`;

      if (!showLabels) return rect;

      const labelY = y + swatchSize + 12;
      const label = `<text x="${x + swatchSize / 2}" y="${labelY}" text-anchor="middle" font-size="10" font-family="monospace" fill="#444">${escapeXml(hex)}</text>`;
      return rect + label;
    })
    .join('\n  ');

  const titleAttr = glyph.meta.id ? ` aria-label="ChromaGlyph ${escapeXml(glyph.meta.id)}"` : '';

  return [
    `<svg xmlns="http://www.w3.org/2000/svg" width="${totalW}" height="${totalH}" role="img"${titleAttr}>`,
    `  ${swatches}`,
    `</svg>`,
  ].join('\n');
}

/**
 * Renders a `Glyph` to a PNG `Buffer`.
 *
 * Requires the `sharp` package to be installed as a peer dependency.
 * Throws a `ChromaGlyphError` if `sharp` is not available.
 *
 * @param glyph   - The glyph to render.
 * @param options - Optional render configuration.
 * @returns A `Promise` resolving to a `Buffer` containing PNG data.
 * @throws {ChromaGlyphError} If `sharp` is not installed.
 */
export async function renderPNG(glyph: Glyph, options?: RenderOptions): Promise<Buffer> {
  // `sharp` is an optional peer dependency; import it dynamically at runtime.
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  let sharpFn: (input: Buffer) => { png(): { toBuffer(): Promise<Buffer> } };
  try {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const mod = await import('sharp' as string) as any;
    sharpFn = mod.default ?? mod;
  } catch {
    throw new ChromaGlyphError(
      'renderPNG requires the "sharp" package. Install it with: npm install sharp',
    );
  }

  const svg = renderSVG(glyph, options);
  return sharpFn(Buffer.from(svg)).png().toBuffer();
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function escapeXml(str: string): string {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}
