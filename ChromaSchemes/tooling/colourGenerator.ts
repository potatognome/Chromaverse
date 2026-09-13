import { IColourGenerator } from './interfaces';

export class ColourGenerator implements IColourGenerator {
  private hsvToRgb(h: number, s: number, v: number): { r: number; g: number; b: number } {
    const hue = ((h % 360) + 360) % 360;
    const sat = Math.max(0, Math.min(1, s));
    const val = Math.max(0, Math.min(1, v));
    const c = val * sat;
    const x = c * (1 - Math.abs(((hue / 60) % 2) - 1));
    const m = val - c;

    let rp = 0;
    let gp = 0;
    let bp = 0;
    if (hue < 60) [rp, gp, bp] = [c, x, 0];
    else if (hue < 120) [rp, gp, bp] = [x, c, 0];
    else if (hue < 180) [rp, gp, bp] = [0, c, x];
    else if (hue < 240) [rp, gp, bp] = [0, x, c];
    else if (hue < 300) [rp, gp, bp] = [x, 0, c];
    else [rp, gp, bp] = [c, 0, x];

    return {
      r: Math.round((rp + m) * 255),
      g: Math.round((gp + m) * 255),
      b: Math.round((bp + m) * 255),
    };
  }

  generate(baseHex: string, hueOffsets: number[], chromaValues: number[], luminanceValues: number[]) {
    const base = parseInt(baseHex.replace('#', ''), 16);
    const baseHue = ((base % 360) + 360) % 360;

    return hueOffsets.map((offset, idx) => {
      const hue = (baseHue + offset) % 360;
      const rgb = this.hsvToRgb(hue, chromaValues[idx], luminanceValues[idx]);
      return {
        id: `c${idx}`,
        origin: idx < 4 ? 'base' : 'derived',
        rgb,
        oklch: {
          l: Number(luminanceValues[idx].toFixed(6)),
          c: Number(chromaValues[idx].toFixed(6)),
          h: Number(hue.toFixed(6)),
        },
      };
    });
  }
}
