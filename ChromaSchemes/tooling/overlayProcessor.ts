/**
 * OverlayProcessor – applies overlay transformations to colour vectors.
 *
 * Description:
 *   Adjusts hue, chroma, and luminance arrays according to the requested
 *   overlay operations.
 *
 * Inputs:
 *   - apply(hues, chromaValues, luminanceValues, overlays)
 *     * hues: base hue offsets.
 *     * chromaValues: base chroma values.
 *     * luminanceValues: base luminance values.
 *     * overlays: overlay descriptors and optional parameters.
 *
 * Outputs:
 *   A transformed hue/chroma/luminance bundle.
 *
 * Example:
 *   const processor = new OverlayProcessor();
 *   const next = processor.apply([0, 120], [0.2, 0.18], [0.8, 0.75], []);
 */
import { IOverlayProcessor } from './interfaces';

export class OverlayProcessor implements IOverlayProcessor {
  apply(
    hues: number[],
    chromaValues: number[],
    luminanceValues: number[],
    overlays: Array<{ type: string; params?: Record<string, unknown> }>,
  ) {
    let outHues = [...hues];
    let outChroma = [...chromaValues];
    let outLuminance = [...luminanceValues];

    for (const overlay of overlays) {
      if (['harmonic', 'rotational', 'rotation'].includes(overlay.type)) {
        const rotation = Number(overlay.params?.rotation ?? 0);
        outHues = outHues.map((h) => (h + rotation + 360) % 360);
      } else if (overlay.type === 'luminance_wheel') {
        const amplitude = Number(overlay.params?.amplitude ?? 0.12);
        outLuminance = outLuminance.map((l, i) => Math.min(0.95, Math.max(0.05, l + (amplitude * ((i % 4) - 1.5)) / 3)));
      } else if (overlay.type === 'chroma_spiral') {
        const step = Number(overlay.params?.step ?? 0.015);
        outChroma = outChroma.map((c, i) => Math.min(0.33, Math.max(0.01, c + i * step)));
      }
    }

    return { hues: outHues, chromaValues: outChroma, luminanceValues: outLuminance };
  }
}
