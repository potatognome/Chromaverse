"""Ensure emitter modules are imported so decorators register them."""

from __future__ import annotations

from Dev.Chromaspace.src.Chromaspace.registry import (
    MODULE_TYPE_EMITTER,
    get_all,
)


def ensure_emitters_registered() -> None:
    from ..tapo.tapo_emitter import TapoEmitter  # noqa: F401
    from ..terminal.terminal_emitter import TerminalEmitter  # noqa: F401


def get_registered_emitters():
    ensure_emitters_registered()
    return get_all(MODULE_TYPE_EMITTER)
