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

/** Bind generated colours into the semantic role map used by previews. */
export class RoleBinder implements IRoleBinder {
  /** Map each role to a colour ref by index, cycling through the set. */
  bind(colourSet: Array<Record<string, unknown>>) {
    return UNIVERSAL_ROLES.reduce<Record<string, unknown>>((acc, role, idx) => {
      const ref = String(colourSet[idx % colourSet.length]?.id ?? 'c0');
      const layer = role.endsWith('_fg') ? 'fg' : 'bg';
      acc[role] = { layers: { [layer]: { colourRef: ref } } };
      return acc;
    }, {});
  }
}
