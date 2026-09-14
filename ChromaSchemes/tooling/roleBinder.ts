/**
 * RoleBinder – maps colour-set entries onto universal scheme roles.
 *
 * Description:
 *   Binds palette entries to the shared role vocabulary used by the preview
 *   and emitter stages.
 *
 * Inputs:
 *   - bind(colourSet)
 *     * colourSet: array of normalised colour-set entries.
 *
 * Outputs:
 *   A role map keyed by role name with foreground/background layer refs.
 *
 * Example:
 *   const binder = new RoleBinder();
 *   const roles = binder.bind(colourSet);
 */
import { IRoleBinder } from './interfaces';

const UNIVERSAL_ROLES = [
  'primary_surface',
  'secondary_surface',
  'tertiary_surface',
  'accent_surface',
  'border_fg',
  'menu_fg',
  'menu_bg',
  'interactive_fg',
  'interactive_bg',
  'neutral_fg',
  'neutral_bg',
];

export class RoleBinder implements IRoleBinder {
  bind(colourSet: Array<Record<string, unknown>>) {
    return UNIVERSAL_ROLES.reduce<Record<string, unknown>>((acc, role, idx) => {
      const ref = String(colourSet[idx % colourSet.length]?.id ?? 'c0');
      const layer = role.endsWith('_fg') ? 'fg' : 'bg';
      acc[role] = { layers: { [layer]: { colourRef: ref } } };
      return acc;
    }, {});
  }
}
