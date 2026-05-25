"""Simple terminal emitter for debugging output."""

from __future__ import annotations

from Dev.Chromaspace.src.Chromaspace.interfaces import EmitterInterface
from Dev.Chromaspace.src.Chromaspace.registry import register_emitter

from ..config_loader import CONFIG, get_emitter_settings


@register_emitter(
    name="terminal",
    version="1.0.0",
    capabilities=["rgb", "debug"],
    config_schema="schemas/terminal.yaml",
)
class TerminalEmitter(EmitterInterface):
    """Emit frames to stdout for local debugging."""

    def __init__(self, config=None):
        self.config = config or CONFIG
        settings = get_emitter_settings(self.config, "terminal")
        self.enabled = bool(settings.get("enabled", True))

    def render(self, frame):
        if not self.enabled:
            return {"emitted": False, "reason": "disabled"}
        return {"emitted": True, "frame": frame}
