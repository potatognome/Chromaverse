#!/usr/bin/env python3
"""
config.py
Loads Chromaspace app config via tUilKit (explicit path), then loads the
active colour-system JSON config via the pointer file.
"""
import json
import os


def _existing_path(candidates):
    for path in candidates:
        if path and os.path.exists(path):
            return path
    return None


def _load_json(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def resolve_app_config_path(project_path=None, workspace_path=None):
    """Resolve the primary Chromaspace config, preferring workspace override."""
    project_candidate = project_path or _CHROMASPACE_CONFIG_PATH
    workspace_candidate = workspace_path or _WORKSPACE_CHROMASPACE_CONFIG_PATH

    def _case_variants(path):
        folder, name = os.path.split(path)
        lower_name = name.lower()
        if lower_name != "chromaspace_config.json":
            return [path]
        return [
            path,
            os.path.join(folder, "Chromaspace_CONFIG.json"),
            os.path.join(folder, "CHROMASPACE_CONFIG.json"),
        ]

    candidates = []
    for candidate in [workspace_candidate, project_candidate]:
        for variant in _case_variants(candidate):
            if variant not in candidates:
                candidates.append(variant)

    return _existing_path(
        candidates
    )

# ---------------------------------------------------------------------------
# App-level config via tUilKit (CHROMASPACE_CONFIG.json)
# Using ConfigLoader with an explicit path so discovery works regardless of
# the working directory (tests run from workspace root, CLI from project dir).
# ---------------------------------------------------------------------------
_CHROMASPACE_CONFIG_PATH = os.path.normpath(
    os.path.join(os.path.dirname(__file__), '../../config/Chromaspace_CONFIG.json')
)

_CHROMASPACE_CONFIG_PATH_LEGACY = os.path.normpath(
    os.path.join(os.path.dirname(__file__), '../../config/CHROMASPACE_CONFIG.json')
)

_WORKSPACE_CHROMASPACE_CONFIG_PATH = os.path.normpath(
    os.path.join(
        os.path.dirname(__file__),
        '../../../../.projects_config/Chromaspace_CONFIG.json',
    )
)

_WORKSPACE_CHROMASPACE_CONFIG_PATH_LEGACY = os.path.normpath(
    os.path.join(
        os.path.dirname(__file__),
        '../../../../.projects_config/CHROMASPACE_CONFIG.json',
    )
)

try:
    from tUilKit.utils.config import ConfigLoader as _ConfigLoader
    _resolved_app_config_path = resolve_app_config_path()
    if _resolved_app_config_path is None:
        raise FileNotFoundError("No Chromaspace app config was found")

    _app_loader = _ConfigLoader(config_path=_resolved_app_config_path)
    app_config = _app_loader.global_config
except Exception:
    _resolved_app_config_path = resolve_app_config_path()
    if _resolved_app_config_path and os.path.exists(_resolved_app_config_path):
        try:
            app_config = _load_json(_resolved_app_config_path)
        except Exception:
            app_config = {}
    else:
        app_config = {}

LOG_FILES = app_config.get("LOG_FILES", {
    "SESSION": "logFiles/chromaspace_SESSION.log",
    "MASTER":  "logFiles/chromaspace_MASTER.log",
})

# ---------------------------------------------------------------------------
# Colour-system pointer → active colour config
# ---------------------------------------------------------------------------
_PROJECT_CONFIG_DIR = os.path.normpath(
    os.path.join(os.path.dirname(__file__), '../../config')
)
_WORKSPACE_ROOT = app_config.get("ROOTS", {}).get(
    "WORKSPACE",
    os.path.normpath(os.path.join(os.path.dirname(__file__), '../../../../')),
)
_WORKSPACE_CONFIG_DIR = os.path.normpath(
    os.path.join(_WORKSPACE_ROOT, '.projects_config')
)


def _resolve_secondary_config_path():
    secondary_ref = (
        app_config.get("SECONDARY", {}).get("FILE")
        or "CHROMASPACE.d/Chromaspace_SECONDARY.json"
    )
    secondary_name = os.path.basename(secondary_ref)
    return _existing_path(
        [
            os.path.join(_PROJECT_CONFIG_DIR, secondary_ref),
            os.path.join(_PROJECT_CONFIG_DIR, "CHROMASPACE.d", secondary_name),
            os.path.join(_PROJECT_CONFIG_DIR, secondary_name),
            os.path.join(_WORKSPACE_CONFIG_DIR, secondary_ref),
            os.path.join(_WORKSPACE_CONFIG_DIR, "CHROMASPACE.d", secondary_name),
            os.path.join(_WORKSPACE_CONFIG_DIR, secondary_name),
        ]
    )


SECONDARY_CONFIG_PATH = _resolve_secondary_config_path()
SECONDARY_CONFIG = {}
if SECONDARY_CONFIG_PATH is not None:
    try:
        SECONDARY_CONFIG = _load_json(SECONDARY_CONFIG_PATH)
    except Exception:
        SECONDARY_CONFIG = {}

pointer = SECONDARY_CONFIG.get("COLOUR_SYSTEM_POINTER", {})
if not pointer:
    # Backward-compatible fallback to legacy pointer file.
    POINTER_PATH = _existing_path(
        [
            os.path.join(_PROJECT_CONFIG_DIR, 'CHROMASPACE.d', '_COLOUR_SYSTEM_POINTER.json'),
            os.path.join(_PROJECT_CONFIG_DIR, '_COLOUR_SYSTEM_POINTER.json'),
            os.path.join(_WORKSPACE_CONFIG_DIR, 'CHROMASPACE.d', '_COLOUR_SYSTEM_POINTER.json'),
            os.path.join(_WORKSPACE_CONFIG_DIR, '_COLOUR_SYSTEM_POINTER.json'),
        ]
    )
    if POINTER_PATH is None:
        raise FileNotFoundError(
            "No Chromaspace colour-system pointer was found in secondary or legacy pointer file"
        )
    pointer = _load_json(POINTER_PATH)

COLOUR_SYSTEM_NAME = pointer.get("COLOUR_SYSTEM_NAME", "")
COLOUR_SYSTEM_SUFFIX = (
    f"_{COLOUR_SYSTEM_NAME}" if COLOUR_SYSTEM_NAME else ""
)

_spec_filename = pointer["CONFIG_PATH"]
CONFIG_PATH = _existing_path(
    [
        os.path.join(_PROJECT_CONFIG_DIR, 'CHROMASPACE_SPEC', _spec_filename),
        os.path.join(_PROJECT_CONFIG_DIR, _spec_filename),
        os.path.join(_WORKSPACE_CONFIG_DIR, 'CHROMASPACE_SPEC', _spec_filename),
        os.path.join(_WORKSPACE_CONFIG_DIR, _spec_filename),
    ]
)
if CONFIG_PATH is None:
    raise FileNotFoundError(
        f"No Chromaspace colour-system config file was found for {_spec_filename}"
    )

_config = _load_json(CONFIG_PATH)

# Enforce policy: colour-system specs are value-only and must not define PATHS.
# Any legacy/accidental PATHS block in a spec is ignored in favour of
# root-mode-resolved paths derived from primary + secondary app config.
SPEC_CONTAINED_PATHS = "PATHS" in _config
if SPEC_CONTAINED_PATHS:
    _config.pop("PATHS", None)


def _derive_paths_from_secondary():
    path_config = SECONDARY_CONFIG.get("PATHS", {})
    folders = dict(path_config.get("FOLDERS", {}))
    file_templates = dict(path_config.get("FILE_TEMPLATES", {}))

    roots = app_config.get("ROOTS", {})
    root_modes = app_config.get("ROOT_MODES", {})
    app_paths = app_config.get("PATHS", {})

    def _resolve_by_root_mode(path_key, default_relative, mode_key=None):
        selected_mode_key = mode_key or path_key
        mode_value = str(root_modes.get(selected_mode_key, "project")).lower()
        root_key = "WORKSPACE" if mode_value == "workspace" else "PROJECT"

        project_root_default = os.path.normpath(
            os.path.join(_PROJECT_CONFIG_DIR, os.pardir)
        )
        root_value = roots.get(root_key, project_root_default)
        relative_value = app_paths.get(path_key, default_relative)
        return os.path.normpath(os.path.join(root_value, relative_value))

    output_root = _resolve_by_root_mode("OUTPUTS", "output/")
    project_root = roots.get(
        "PROJECT",
        os.path.normpath(os.path.join(_PROJECT_CONFIG_DIR, os.pardir)),
    )

    folders.setdefault("HTML_OUTPUT", "HTML")
    folders.setdefault("JSON_OUTPUT", "JSON")
    folders.setdefault("DICT_OUTPUT", "dict")

    def _resolve_subfolder(base_folder, folder_value):
        if os.path.isabs(folder_value):
            return os.path.normpath(folder_value)
        return os.path.normpath(os.path.join(base_folder, folder_value))

    resolved_html_output = _resolve_subfolder(output_root, folders["HTML_OUTPUT"])
    resolved_json_output = _resolve_subfolder(output_root, folders["JSON_OUTPUT"])
    resolved_dict_output = _resolve_subfolder(project_root, folders["DICT_OUTPUT"])

    file_templates.setdefault(
        "COLOUR_SYSTEM_JSON",
        "colour_system.json",
    )
    file_templates.setdefault("XKCD_JSON", "xkcd_colors.json")
    file_templates.setdefault(
        "PREVIEW_HTML",
        "preview.html",
    )
    file_templates.setdefault(
        "HUE_SQUARES_HTML",
        "hue_squares.html",
    )
    file_templates.setdefault(
        "HUE_WHEEL_HTML",
        "hue_wheel.html",
    )

    colour_system_token = COLOUR_SYSTEM_NAME or "default"

    def _fmt(template):
        return str(template).format(COLOUR_SYSTEM_NAME=colour_system_token)

    files = {
        "COLOUR_SYSTEM_JSON": os.path.join(
            resolved_json_output,
            _fmt(file_templates["COLOUR_SYSTEM_JSON"]),
        ),
        "XKCD_JSON": os.path.join(
            resolved_dict_output,
            _fmt(file_templates["XKCD_JSON"]),
        ),
        "PREVIEW_HTML": os.path.join(
            resolved_html_output,
            _fmt(file_templates["PREVIEW_HTML"]),
        ),
        # Keep wheel/square file names as leaf names because scripts combine
        # them with HTML_OUTPUT at runtime.
        "HUE_SQUARES_HTML": _fmt(file_templates["HUE_SQUARES_HTML"]),
        "HUE_WHEEL_HTML": _fmt(file_templates["HUE_WHEEL_HTML"]),
    }

    return {
        "FOLDERS": {
            "HTML_OUTPUT": resolved_html_output,
            "JSON_OUTPUT": resolved_json_output,
            "DICT_OUTPUT": resolved_dict_output,
        },
        "FILES": files,
    }


_config.setdefault("PATHS", {})
_config["PATHS"] = _derive_paths_from_secondary()

_bands = _config

HUE_ANCHORS = _bands["HUE_ANCHORS"]
HUE_VARIANTS = _bands["HUE_VARIANTS"]
SAT_BANDS = _bands["SAT_BANDS"]  # list of (name, value)
LUM_BANDS = _bands["LUM_BANDS"]  # list of (name, value)
SAT_BANDS_GREY = _bands["SAT_BANDS_GREY"]  # list of (name, value)
LUM_BANDS_GREY = _bands["LUM_BANDS_GREY"]  # list of (name, value)

# Global offsets for special tables
HUE_GLOBAL_OFFSET = _bands.get("HUE_GLOBAL_OFFSET", 0)
SAT_GLOBAL_OFFSET = _bands.get("SAT_GLOBAL_OFFSET", 0)
LUM_GLOBAL_OFFSET = _bands.get("LUM_GLOBAL_OFFSET", 0)

# Per-band offsets for special tables
HUE_OFFSETS = _bands.get("HUE_OFFSETS", [0]*len(HUE_ANCHORS))
SAT_OFFSETS = _bands.get("SAT_OFFSETS", [0]*len(SAT_BANDS))
LUM_OFFSETS = _bands.get("LUM_OFFSETS", [0]*len(LUM_BANDS))

from .hue import get_sorted_hues

# Combined tuples for easier table generation
HUE_TUPLES = get_sorted_hues()
SAT_TUPLES = [(i, name, value) for i, (name, value) in enumerate(SAT_BANDS)]
LUM_TUPLES = [(i, name, value) for i, (name, value) in enumerate(LUM_BANDS)]
GREY_TUPLES = [(i, name, value, LUM_BANDS_GREY[i][1])
               for i, (name, value) in enumerate(SAT_BANDS_GREY)]

__all__ = [
    "_config", "app_config", "LOG_FILES",
    "HUE_ANCHORS", "HUE_VARIANTS", "SAT_BANDS", "LUM_BANDS",
    "HUE_TUPLES", "SAT_TUPLES", "LUM_TUPLES", "GREY_TUPLES",
    "HUE_OFFSETS", "SAT_OFFSETS", "LUM_OFFSETS",
    "HUE_GLOBAL_OFFSET", "SAT_GLOBAL_OFFSET", "LUM_GLOBAL_OFFSET",
    "COLOUR_SYSTEM_NAME", "COLOUR_SYSTEM_SUFFIX",
    "SECONDARY_CONFIG", "SECONDARY_CONFIG_PATH", "SPEC_CONTAINED_PATHS"
]
