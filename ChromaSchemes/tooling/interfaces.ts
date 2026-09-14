/**
 * Shared TypeScript interface contracts for the ChromaSchemes tooling layer.
 */

export interface IGeometryInterpreter {
  /** Convert a geometry model into hue offsets. */
  interpret(model: string, desiredCount: number, params?: Record<string, unknown>): number[];
}

/** Overlay processor contract for hue and band adjustments. */
export interface IOverlayProcessor {
  /** Apply overlay adjustments to hue, chroma, and luminance values. */
  apply(
    hues: number[],
    chromaValues: number[],
    luminanceValues: number[],
    overlays: Array<{ type: string; params?: Record<string, unknown> }>,
  ): { hues: number[]; chromaValues: number[]; luminanceValues: number[] };
}

/** Colour-generator contract for semantic-to-RGB expansion. */
export interface IColourGenerator {
  /** Produce colour records from a base hex and band values. */
  generate(
    baseHex: string,
    hueOffsets: number[],
    chromaValues: number[],
    luminanceValues: number[],
  ): Array<Record<string, unknown>>;
}

/** Colour-set builder contract for normalising generated records. */
export interface IColourSetBuilder {
  /** Normalize generated colour records into a colour set. */
  build(generatedColours: Array<Record<string, unknown>>): Array<Record<string, unknown>>;
}

/** Role-binder contract for mapping colours to semantics. */
export interface IRoleBinder {
  /** Bind colour-set entries to universal semantic roles. */
  bind(colourSet: Array<Record<string, unknown>>): Record<string, unknown>;
}

/** Scheme emitter contract for persisting generated payloads. */
export interface IChromaSchemeEmitter {
  /** Emit a payload to the requested target path. */
  emit(payload: Record<string, unknown>, targetPath: string): Promise<string>;
}

/** Preview-model builder contract for downstream renderers. */
export interface IPreviewModelBuilder {
  /** Build the preview model consumed by downstream renderers. */
  build(colourSet: Array<Record<string, unknown>>, roles: Record<string, unknown>): Record<string, unknown>;
}
