/**
 * GeometryInterpreter – converts scheme geometry models into hue offsets.
 *
 * Description:
 *   Implements the geometry contract for translating named models into
 *   deterministic hue sequences.
 *
 * Inputs:
 *   - interpret(model, desiredCount, params?)
 *     * model: geometry model name.
 *     * desiredCount: number of requested offsets.
 *     * params: optional geometry parameters such as custom offsets.
 *
 * Outputs:
 *   A numeric hue-offset array.
 *
 * Example:
 *   const interpreter = new GeometryInterpreter();
 *   const offsets = interpreter.interpret('quadratic', 4);
 */
import { IGeometryInterpreter } from './interfaces';

export class GeometryInterpreter implements IGeometryInterpreter {
  interpret(model: string, desiredCount: number, params: Record<string, unknown> = {}): number[] {
    if (model === 'custom') {
      const offsets = params.offsets;
      if (!Array.isArray(offsets) || offsets.length === 0) {
        throw new Error("Custom geometry requires a non-empty 'offsets' array");
      }
      return Array.from(
        { length: Math.max(1, desiredCount) },
        (_, i) => Number(offsets[i % offsets.length]) % 360,
      );
    }

    const cycles: Record<string, number[]> = {
      quadratic: [0, 90, 180, 270],
      triadic: [0, 120, 240],
      tetradic: [0, 60, 180, 240],
      split_complementary: [0, 150, 210],
      harmonic: Array.from({ length: Math.max(1, desiredCount) }, (_, i) => (i * i * 29) % 360),
    };

    const cycle = cycles[model] ?? cycles.quadratic;
    return Array.from({ length: Math.max(1, desiredCount) }, (_, i) => cycle[i % cycle.length]);
  }
}
