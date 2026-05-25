

import argparse
import os
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from Chromaspace.config import _config
from Chromaspace.cli_utils import get_sat_bands, get_lum_bands, parse_band_arg, ensure_output_dir, load_json, save_json

# Load colour_system.json from config
colour_json_path = _config["PATHS"]["FILES"]["COLOUR_SYSTEM_JSON"]
colours = load_json(colour_json_path)

SAT_BANDS = get_sat_bands()
LUM_BANDS = get_lum_bands()

def parse_band_arg(arg, band_type=None):
    # Accept comma or space separated, e.g. "washed,soft" or "washed soft"
    if not arg:
        return []
    items = [x.strip() for x in arg.replace(',', ' ').split() if x.strip()]
    # Map numbers to band names if needed
    if band_type == 'sat':
        bands = SAT_BANDS
    elif band_type == 'lum':
        bands = LUM_BANDS
    else:
        bands = None
    if bands:
        mapped = []
        for item in items:
            if item.isdigit():
                idx = int(item) - 1
                if 0 <= idx < len(bands):
                    mapped.append(bands[idx])
            else:
                mapped.append(item)
        return mapped
    return items

def filter_colours(colours, only=None, except_=None, sats=None, lums=None):
    if only:
        sats, lums = only
    elif except_:
        sats_ex, lums_ex = except_
    filtered = []
    for c in colours:
        sat = c['sat_band']
        lum = c['lum_band']
        if only:
            if sat not in sats or lum not in lums:
                continue
        elif except_:
            if sat in sats_ex or lum in lums_ex:
                continue
        if sats and sat not in sats:
            continue
        if lums and lum not in lums:
            continue
        filtered.append(c)
    return filtered

def output_colours(colours, output_opts):
    results = []
    for c in colours:
        out = {}
        if 'name_rgb_only' in output_opts:
            results.append({'name': c['name'], 'rgb': c['rgb']})
            continue
        if 'no_descriptors' not in output_opts:
            out['name'] = c['name']
        if 'no_bands' not in output_opts:
            out['sat_band'] = c['sat_band']
            out['lum_band'] = c['lum_band']
        if 'no_hsv' not in output_opts:
            out['hsv'] = c['hsv']
        if 'no_rgb' not in output_opts:
            out['rgb'] = c['rgb']
        if 'no_xkcd' not in output_opts:
            out['xkcd_match'] = c['xkcd_match']
        results.append(out)
    return results


def main():
    parser = argparse.ArgumentParser(description='Filter colour_system.json by bands and output options.')
    parser.add_argument('--ONLY', nargs=2, metavar=('SAT','LUM'), help='Only include these SAT and LUM bands (comma, space, or number 1-5)')
    parser.add_argument('--EXCEPT', nargs=2, metavar=('SAT','LUM'), help='Exclude these SAT and LUM bands (comma, space, or number 1-5)')
    parser.add_argument('--SAT', nargs='+', help='Include only these SAT bands (by name or number 1-5)')
    parser.add_argument('--LUM', nargs='+', help='Include only these LUM bands (by name or number 1-5)')
    parser.add_argument('--OUTPUT', nargs='+', default=[], help='Output options: name_rgb_only, no_descriptors, no_bands, no_hsv, no_rgb, no_xkcd')
    parser.add_argument('--FILE', metavar='FILENAME', help='Write filtered set to output/FILENAME (JSON)')
    args = parser.parse_args()

    only = None
    except_ = None
    if args.ONLY:
        only = (parse_band_arg(args.ONLY[0], 'sat'), parse_band_arg(args.ONLY[1], 'lum'))
    elif args.EXCEPT:
        except_ = (parse_band_arg(args.EXCEPT[0], 'sat'), parse_band_arg(args.EXCEPT[1], 'lum'))
    sats = parse_band_arg(' '.join(args.SAT), 'sat') if args.SAT else None
    lums = parse_band_arg(' '.join(args.LUM), 'lum') if args.LUM else None
    output_opts = set(args.OUTPUT)

    filtered = filter_colours(colours, only=only, except_=except_, sats=sats, lums=lums)
    results = output_colours(filtered, output_opts)

    # Show record counts
    print(f"Original records: {len(colours)} | Filtered records: {len(filtered)}")

    if args.FILE:
        filename = args.FILE
        if not filename.lower().endswith('.json'):
            filename += '.json'
        out_path = os.path.join(os.path.dirname(__file__), '../output', filename)
        save_json(results, out_path)
        print(f"Filtered set written to {out_path}")
    else:
        for entry in results:
            from json import dumps
            print(dumps(entry, indent=2))

if __name__ == '__main__':
    main()
