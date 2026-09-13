import { IColourGenerator } from './interfaces';

export class ColourGenerator implements IColourGenerator {
  generate(baseHex: string, hueOffsets: number[], chromaValues: number[], luminanceValues: number[]) {
    const base = parseInt(baseHex.replace('#', ''), 16);
    const baseHue = ((base % 360) + 360) % 360;

    return hueOffsets.map((offset, idx) => ({
      id: `c${idx}`,
      origin: idx < 4 ? 'base' : 'derived',
      rgb: {
        r: Math.round(((baseHue + offset) % 360 / 360) * 255),
        g: Math.round(Math.min(255, chromaValues[idx] * 700)),
        b: Math.round(Math.min(255, luminanceValues[idx] * 255)),
      },
      oklch: {
        l: Number(luminanceValues[idx].toFixed(6)),
        c: Number(chromaValues[idx].toFixed(6)),
        h: Number((((baseHue + offset) % 360) + 360).toFixed(6)),
      },
    }));
  }
}
