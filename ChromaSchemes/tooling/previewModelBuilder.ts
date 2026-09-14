/**
 * PreviewModelBuilder – builds preview-ready model payloads.
 *
 * Description:
 *   Converts colour-set and role-binding data into the preview model consumed
 *   by the UI renderer.
 *
 * Inputs:
 *   - build(colourSet, roles)
 *     * colourSet: normalised colour entries.
 *     * roles: resolved role-binding map.
 *
 * Outputs:
 *   A preview model object with pane definitions and colour references.
 *
 * Example:
 *   const builder = new PreviewModelBuilder();
 *   const preview = builder.build(colourSet, roles);
 */
import { IPreviewModelBuilder } from './interfaces';

export class PreviewModelBuilder implements IPreviewModelBuilder {
  build(colourSet: Array<Record<string, unknown>>, roles: Record<string, unknown>) {
    const borderRef =
      (roles.border_fg as { layers?: { fg?: { colourRef?: string } } } | undefined)?.layers?.fg?.colourRef ?? 'c0';

    return {
      model: 'MultiPanePreviewModel',
      panes: Array.from({ length: 4 }, (_, idx) => ({
        paneId: `pane_${idx}`,
        layout: 'fractal_quadrant',
        border: { colourRef: borderRef },
        fill: { colourRef: String(colourSet[idx % colourSet.length]?.id ?? 'c0') },
      })),
    };
  }
}
