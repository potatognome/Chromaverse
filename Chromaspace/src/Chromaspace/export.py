#!/usr/bin/env python3
"""Writes JSON files and other structured outputs for Chromaspace."""
import json

try:
    from tUilKit import get_logger as _get_logger, get_file_system as _get_fs
    logger = _get_logger()
    file_system = _get_fs()
except Exception:
    logger = None
    file_system = None

try:
    from .config import app_config as _app_config
except Exception:
    _app_config = {}

LOG_FILES = _app_config.get(
    "LOG_FILES",
    {},
)


def export_to_json(colours, path):
    import os
    out_dir = os.path.dirname(path) or "."
    if file_system is not None:
        file_system.validate_and_create_folder(out_dir)
    else:
        os.makedirs(out_dir, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(colours, f, indent=2)
    if logger is not None:
        logger.colour_log(
            "!done", f"Exported {len(colours)} colours to", "!path", path,
            log_files=list(LOG_FILES.values())
        )
