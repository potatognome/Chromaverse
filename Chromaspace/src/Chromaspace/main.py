#!/usr/bin/env python3
"""
main.py
Chromaspace CLI entry point. Menu-driven interface for generating and
exporting colour system data.
"""

import os
import sys
from datetime import datetime
from tUilKit import get_logger, get_config_loader, get_file_system

logger = get_logger()
config_loader = get_config_loader()
file_system = get_file_system()

LOG_FILES = {
    "SESSION": "logFiles/chromaspace_SESSION.log",
    "MASTER":  "logFiles/chromaspace_MASTER.log",
}


def startup():
    """Print startup banner and load configuration."""
    os.system("cls" if os.name == "nt" else "clear")
    start_time = datetime.now()
    global_config = config_loader.global_config
    log_cfg = global_config.get("LOG_FILES", {})
    if log_cfg:
        LOG_FILES.update({k: v for k, v in log_cfg.items()})
    logger.colour_log(
        "!info", "Chromaspace started at",
        "!value", start_time.strftime("%Y-%m-%d %H:%M:%S"),
        log_files=list(LOG_FILES.values()),
    )
    return global_config


def menu(global_config):
    """Main CLI menu."""
    while True:
        print("\n=== Chromaspace ===")
        print("  [1] Generate colour JSON")
        print("  [2] Render hue squares (HTML)")
        print("  [3] Render colour wheels (HTML)")
        print("  [4] Preview full colour table (HTML)")
        print("  [Q] Quit")
        choice = input("\nSelect option: ").strip().upper()

        if choice == "1":
            _run_generate_json(global_config)
        elif choice == "2":
            _run_script("render_hue_squares.py")
        elif choice == "3":
            _run_script("render_wheels.py")
        elif choice == "4":
            _run_script("preview_colours.py")
        elif choice == "Q":
            logger.colour_log(
                "!done", "Chromaspace exited.",
                log_files=list(LOG_FILES.values()),
            )
            break
        else:
            logger.colour_log("!warning", "Unknown option:", "!value", choice)


def _run_generate_json(global_config):
    """Run the JSON generation pipeline."""
    try:
        from Chromaspace.generator import generate_colour_entries
        from Chromaspace.export import export_to_json
        from Chromaspace.cli_utils import get_output_file, ensure_output_dir

        colours = generate_colour_entries()
        out_path = get_output_file(
            "COLOUR_SYSTEM_JSON", "../output/chromaspace.json",
            with_system_suffix=True,
        )
        ensure_output_dir(out_path)
        export_to_json(colours, out_path)
        logger.colour_log(
            "!done", f"Generated {len(colours)} colours →",
            "!path", out_path,
            log_files=list(LOG_FILES.values()),
        )
    except Exception as exc:
        logger.log_exception("JSON generation failed", exc,
                             log_files=list(LOG_FILES.values()))


def _run_script(script_name):
    """Launch a script from the scripts/ folder."""
    import subprocess
    scripts_dir = os.path.join(os.path.dirname(__file__), "..", "..", "scripts")
    script_path = os.path.normpath(os.path.join(scripts_dir, script_name))
    if not os.path.isfile(script_path):
        logger.colour_log("!error", "Script not found:", "!path", script_path)
        return
    subprocess.run([sys.executable, script_path], check=False)


def main():
    global_config = startup()
    menu(global_config)


if __name__ == "__main__":
    main()
