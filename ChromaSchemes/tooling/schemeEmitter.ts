/**
 * ChromaSchemeEmitter – writes the final scheme payload to disk.
 *
 * Description:
 *   Serialises the assembled scheme payload and stores it at the target path.
 *
 * Inputs:
 *   - emit(payload, targetPath)
 *     * payload: final scheme object.
 *     * targetPath: output file path.
 *
 * Outputs:
 *   A promise resolving to the emitted file path.
 *
 * Example:
 *   const emitter = new ChromaSchemeEmitter();
 *   await emitter.emit(payload, 'out/scheme.json');
 */
import { promises as fs } from 'node:fs';

import { IChromaSchemeEmitter } from './interfaces';

export class ChromaSchemeEmitter implements IChromaSchemeEmitter {
  async emit(payload: Record<string, unknown>, targetPath: string): Promise<string> {
    await fs.writeFile(targetPath, JSON.stringify(payload, null, 2), 'utf-8');
    return targetPath;
  }
}
