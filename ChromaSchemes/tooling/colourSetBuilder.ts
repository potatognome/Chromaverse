import { IColourSetBuilder } from './interfaces';

/** Normalize generated colour records into a stable colour-set shape. */
export class ColourSetBuilder implements IColourSetBuilder {
  /** Strip generated colour records down to the canonical colour-set shape. */
  build(generatedColours: Array<Record<string, unknown>>) {
    return generatedColours.map((entry) => ({
      id: entry.id,
      origin: entry.origin,
      rgb: entry.rgb,
      oklch: entry.oklch,
    }));
  }
}
