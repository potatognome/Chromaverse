#!/usr/bin/env python3
"""ChromaTools CLI entry point."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Callable, Iterable, Optional

from ChromaTools.catalog import AppRecord, load_app_catalog, resolve_app
from ChromaTools.config import CONFIG, PROJECT_ROOT

try:
    from tUilKit import get_logger as _get_logger
except Exception:
    _get_logger = None


class _FallbackLogger:
    @staticmethod
    def _format(parts: Iterable[object]) -> str:
        return " ".join(
            str(part)
            for part in parts
            if part not in {"!info", "!value", "!done", "!warning", "!error", "!path"}
        )

    def colour_log(self, *parts: object, **_: object) -> None:
        print(self._format(parts))

    def log_exception(self, message: str, exc: Exception, **_: object) -> None:
        print(f"{message}: {exc}", file=sys.stderr)


logger = _get_logger() if _get_logger is not None else _FallbackLogger()


def startup(config: Optional[dict] = None) -> dict:
    active_config = config or CONFIG
    clear_screen = bool(active_config.get("CLI_DEFAULTS", {}).get("CLEAR_SCREEN", True))
    if clear_screen:
        os.system("cls" if os.name == "nt" else "clear")
    logger.colour_log("!info", "ChromaTools ready")
    return active_config


def render_menu(output_func: Callable[[str], None]) -> None:
    output_func("\n=== ChromaTools ===")
    output_func("  [1] List Chroma apps")
    output_func("  [2] Inspect app details")
    output_func("  [3] Launch configured app")
    output_func("  [4] Show configuration summary")
    output_func("  [Q] Quit")


def list_apps(apps: Iterable[AppRecord], output_func: Callable[[str], None]) -> None:
    for index, app in enumerate(apps, start=1):
        command_state = "launchable" if app.launchable else "catalogue-only"
        output_func(f"{index}. {app.name} [{app.app_type}] - {command_state}")
        if app.description:
            output_func(f"   {app.description}")


def show_app_details(app: AppRecord, output_func: Callable[[str], None]) -> None:
    output_func(f"Name: {app.name}")
    output_func(f"Key: {app.key}")
    output_func(f"Type: {app.app_type}")
    output_func(f"Enabled: {'yes' if app.enabled else 'no'}")
    output_func(f"Entry point: {app.entry_point or '-'}")
    output_func(f"Project path: {app.project_path}")
    output_func(f"Config path: {app.config_path}")
    output_func(
        "Launch command: "
        + (" ".join(app.launch_command) if app.launch_command else "not configured")
    )


def show_config_summary(config: dict, apps: Iterable[AppRecord], output_func: Callable[[str], None]) -> None:
    info = config.get("INFO", {})
    output_func(f"Project: {info.get('PROJECT_NAME', 'ChromaTools')}")
    output_func(f"Version: {info.get('VERSION', '0.1.0')}")
    output_func(f"Description: {info.get('PROJECT_DESCRIPTION', '')}")
    output_func(f"Apps registered: {len(list(apps))}")
    for key, value in sorted(config.get("PATHS", {}).items()):
        output_func(f"PATHS.{key}: {value}")


def launch_app(app: AppRecord, output_func: Callable[[str], None]) -> bool:
    if not app.launch_command:
        output_func(f"{app.name} has no launch command configured.")
        return False

    output_func(f"Launching {app.name}...")
    try:
        completed = subprocess.run(
            list(app.launch_command),
            cwd=str(app.project_path),
            check=False,
        )
    except OSError as exc:
        logger.log_exception(f"Failed to launch {app.name}", exc)
        output_func(f"Failed to launch {app.name}: {exc}")
        return False

    if completed.returncode == 0:
        output_func(f"{app.name} finished successfully.")
        return True

    output_func(f"{app.name} exited with code {completed.returncode}.")
    return False


def _prompt_for_app(
    apps: list[AppRecord],
    input_func: Callable[[str], str],
    output_func: Callable[[str], None],
) -> Optional[AppRecord]:
    list_apps(apps, output_func)
    selection = input_func("\nSelect app by number or key: ")
    app = resolve_app(selection, apps)
    if app is None:
        output_func("Unknown app selection.")
    return app


def menu(
    config: Optional[dict] = None,
    input_func: Callable[[str], str] = input,
    output_func: Callable[[str], None] = print,
) -> int:
    active_config = config or CONFIG
    apps = load_app_catalog(active_config, PROJECT_ROOT)

    while True:
        render_menu(output_func)
        choice = input_func("\nSelect option: ").strip().upper()

        if choice == "1":
            list_apps(apps, output_func)
        elif choice == "2":
            app = _prompt_for_app(apps, input_func, output_func)
            if app is not None:
                show_app_details(app, output_func)
        elif choice == "3":
            app = _prompt_for_app(apps, input_func, output_func)
            if app is not None:
                launch_app(app, output_func)
        elif choice == "4":
            show_config_summary(active_config, apps, output_func)
        elif choice in {"Q", "QUIT", "EXIT"}:
            logger.colour_log("!done", "ChromaTools exited.")
            return 0
        else:
            logger.colour_log("!warning", "Unknown option:", "!value", choice)
            output_func("Unknown option.")


def main() -> int:
    config = startup()
    return menu(config=config)


if __name__ == "__main__":
    raise SystemExit(main())

