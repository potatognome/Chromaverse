import { promises as fs } from 'node:fs';

import { IChromaSchemeEmitter } from './interfaces';

/** Serialise scheme payloads to disk. */
export class ChromaSchemeEmitter implements IChromaSchemeEmitter {
  /** Serialise a scheme payload to disk as formatted JSON. */
  async emit(payload: Record<string, unknown>, targetPath: string): Promise<string> {
    await fs.writeFile(targetPath, JSON.stringify(payload, null, 2), 'utf-8');
    return targetPath;
  }
}
