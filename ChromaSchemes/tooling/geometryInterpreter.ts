import { IGeometryInterpreter } from './interfaces';

export class GeometryInterpreter implements IGeometryInterpreter {
  interpret(model: string, desiredCount: number): number[] {
    const cycles: Record<string, number[]> = {
      quadratic: [0, 90, 180, 270],
      triadic: [0, 120, 240],
      tetradic: [0, 60, 180, 240],
      split_complementary: [0, 150, 210],
      harmonic: Array.from({ length: Math.max(1, desiredCount) }, (_, i) => (i * i * 29) % 360),
      custom: [0],
    };

    const cycle = cycles[model] ?? cycles.quadratic;
    return Array.from({ length: Math.max(1, desiredCount) }, (_, i) => cycle[i % cycle.length]);
  }
}
