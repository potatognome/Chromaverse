/**
 * ChromaSchemes tooling interface contracts.
 *
 * Description:
 *   Declares the public TypeScript interfaces that connect the geometry,
 *   colour-generation, overlay, role-binding, preview, and emitter stages.
 *
 * Inputs:
 *   See each interface method signature for the accepted values.
 *
 * Outputs:
 *   The interfaces describe hue arrays, colour records, preview models,
 *   bindings, and emitted file paths.
 *
 * Example:
 *   class CustomGenerator implements IColourGenerator {
 *     generate(baseHex, hueOffsets, chromaValues, luminanceValues) { ... }
 *   }
 */
export interface IGeometryInterpreter {
  interpret(model: string, desiredCount: number, params?: Record<string, unknown>): number[];
}

export interface IOverlayProcessor {
  apply(
    hues: number[],
    chromaValues: number[],
    luminanceValues: number[],
    overlays: Array<{ type: string; params?: Record<string, unknown> }>,
  ): { hues: number[]; chromaValues: number[]; luminanceValues: number[] };
}

export interface IColourGenerator {
  generate(
    baseHex: string,
    hueOffsets: number[],
    chromaValues: number[],
    luminanceValues: number[],
  ): Array<Record<string, unknown>>;
}

export interface IColourSetBuilder {
  build(generatedColours: Array<Record<string, unknown>>): Array<Record<string, unknown>>;
}

export interface IRoleBinder {
  bind(colourSet: Array<Record<string, unknown>>): Record<string, unknown>;
}

export interface IChromaSchemeEmitter {
  emit(payload: Record<string, unknown>, targetPath: string): Promise<string>;
}

export interface IPreviewModelBuilder {
  build(colourSet: Array<Record<string, unknown>>, roles: Record<string, unknown>): Record<string, unknown>;
}
