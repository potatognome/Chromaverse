/**
 * ColourSetBuilder – normalises generated colour records.
 *
 * Description:
 *   Shapes generator output into the colour-set structure consumed by later
 *   ChromaSchemes tooling stages.
 *
 * Inputs:
 *   - build(generatedColours)
 *     * generatedColours: array of raw colour records.
 *
 * Outputs:
 *   An array of colour-set entries with id, origin, rgb, and oklch fields.
 *
 * Example:
 *   const builder = new ColourSetBuilder();
 *   const colourSet = builder.build(colours);
 */
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
