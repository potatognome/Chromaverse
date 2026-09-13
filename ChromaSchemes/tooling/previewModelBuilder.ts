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
