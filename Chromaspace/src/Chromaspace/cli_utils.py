# Shared JSON file helpers
import json
def load_json(path, encoding='utf-8'):
    with open(path, 'r', encoding=encoding) as f:
        return json.load(f)

def save_json(obj, path, encoding='utf-8', **kwargs):
    with open(path, 'w', encoding=encoding) as f:
        json.dump(obj, f, indent=2, ensure_ascii=False, **kwargs)
"""Shared CLI utilities for colour_system scripts."""
import os
from .config import _config, COLOUR_SYSTEM_SUFFIX

# Band/variant parsing helpers
def parse_band_arg(arg, all_bands):
    if not arg:
        return all_bands
    items = [x.strip() for x in arg.split(",") if x.strip()]
    result = []
    for item in items:
        if item.isdigit():
            idx = int(item)
            if 0 <= idx < len(all_bands):
                result.append(all_bands[idx])
        elif item in all_bands:
            result.append(item)
    return result


def ensure_output_dir(path):
    """Ensure the output directory exists for a file or directory path."""
    # If path is a directory, create it. If it's a file, create its parent.
    if path is None:
        return
    dir_path = path
    if not os.path.splitext(path)[1]:  # No file extension, treat as folder
        dir_path = path
    else:
        dir_path = os.path.dirname(path)
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)

# Config-driven output folder and file helpers
def append_suffix_to_filename(filename, suffix=COLOUR_SYSTEM_SUFFIX):
    """Append colour-system suffix to a filename if not already present."""
    if not filename or not suffix:
        return filename
    base, ext = os.path.splitext(filename)
    if base.endswith(suffix):
        return filename
    return f"{base}{suffix}{ext}"


def append_suffix_to_folder(folder, suffix=COLOUR_SYSTEM_SUFFIX):
    """Append colour-system suffix to a folder name if not already present."""
    if not folder or not suffix:
        return folder
    norm_folder = os.path.normpath(folder)
    parent = os.path.dirname(norm_folder)
    leaf = os.path.basename(norm_folder)
    if leaf.endswith(suffix):
        return folder
    suffixed_leaf = f"{leaf}{suffix}"
    if parent:
        return os.path.join(parent, suffixed_leaf)
    return suffixed_leaf


def get_output_folder(key, default=None, with_system_suffix=False):
    folder = _config["PATHS"]["FOLDERS"].get(key, default)
    if with_system_suffix:
        return append_suffix_to_folder(folder)
    return folder


def get_output_file(key, default=None, with_system_suffix=False):
    filename = _config["PATHS"]["FILES"].get(key, default)
    if with_system_suffix:
        return append_suffix_to_filename(filename)
    return filename

# Config-driven band/variant access
def get_hue_anchors():
    return _config["HUE_ANCHORS"]

def get_hue_variants():
    return _config["HUE_VARIANTS"]

def get_sat_bands():
    return [name for name, value in _config["SAT_BANDS"]]

def get_lum_bands():
    return [name for name, value in _config["LUM_BANDS"]]
