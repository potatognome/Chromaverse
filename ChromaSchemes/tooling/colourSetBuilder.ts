import { IColourSetBuilder } from './interfaces';

/** Normalise generated colour records for downstream scheme consumers. */
export class ColourSetBuilder implements IColourSetBuilder {
  /** Strip generated colour records down to id/origin/rgb/oklch fields. */
  build(generatedColours: Array<Record<string, unknown>>) {
    return generatedColours.map((entry) => ({
      id: entry.id,
      origin: entry.origin,
      rgb: entry.rgb,
      oklch: entry.oklch,
    }));
  }
}
