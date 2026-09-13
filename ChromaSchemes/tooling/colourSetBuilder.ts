import { IColourSetBuilder } from './interfaces';

export class ColourSetBuilder implements IColourSetBuilder {
  build(generatedColours: Array<Record<string, unknown>>) {
    return generatedColours.map((entry) => ({
      id: entry.id,
      origin: entry.origin,
      rgb: entry.rgb,
      oklch: entry.oklch,
    }));
  }
}
