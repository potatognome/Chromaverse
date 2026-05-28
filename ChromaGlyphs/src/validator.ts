/**
 * ChromaGlyphs – validator.
 *
 * Validates a `Glyph` object against the JSON Schema and additional
 * semantic rules (palette size, hex format, etc.).
 */

import Ajv from 'ajv';
import addFormats from 'ajv-formats';
import { Glyph, ValidationResult } from './types';
import glyphSchema from './schemas/glyph.schema.json';

const ajv = new Ajv({ allErrors: true });
addFormats(ajv);
const validateSchema = ajv.compile(glyphSchema);

const HEX_RE = /^#(?:[0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/;
const MAX_PALETTE_SIZE = 16;
const MIN_PALETTE_SIZE = 1;

/**
 * Validates a `Glyph` against the JSON Schema and semantic rules.
 *
 * @param glyph - The glyph to validate.
 * @returns `ValidationResult` with `valid` flag and `errors` array.
 */
export function validate(glyph: Glyph): ValidationResult {
  const errors: string[] = [];

  // 1. JSON Schema check
  const schemaValid = validateSchema(glyph);
  if (!schemaValid && validateSchema.errors) {
    for (const e of validateSchema.errors) {
      errors.push(`Schema: ${e.instancePath || '/'} – ${e.message ?? 'unknown error'}`);
    }
  }

  // 2. Semantic rules
  const size = Array.isArray(glyph?.palette) ? glyph.palette.length : 0;
  if (size < MIN_PALETTE_SIZE) {
    errors.push(`Palette must contain at least ${MIN_PALETTE_SIZE} colour(s).`);
  }
  if (size > MAX_PALETTE_SIZE) {
    errors.push(`Palette must not exceed ${MAX_PALETTE_SIZE} colours (got ${size}).`);
  }

  if (Array.isArray(glyph?.palette)) {
    for (let i = 0; i < glyph.palette.length; i++) {
      const hex = glyph.palette[i]?.hex;
      if (typeof hex !== 'string' || !HEX_RE.test(hex)) {
        errors.push(`palette[${i}].hex is not a valid hex colour: "${hex}".`);
      }
    }
  }

  if (glyph?.format !== 'cg1') {
    errors.push(`Unsupported format version: "${glyph?.format}". Expected "cg1".`);
  }

  return { valid: errors.length === 0, errors };
}
