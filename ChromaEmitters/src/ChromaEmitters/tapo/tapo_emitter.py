"""Registry-discoverable Tapo emitter implementation."""

from __future__ import annotations

try:
    from tUilKit import get_logger as _get_logger

    _LOGGER = _get_logger()
except Exception:
    _LOGGER = None

from Dev.Chromaspace.src.Chromaspace.interfaces import EmitterInterface
from Dev.Chromaspace.src.Chromaspace.registry import register_emitter

from ..config_loader import CONFIG, get_emitter_settings
from .tapo_device import TapoLedDevice


@register_emitter(
    name="tapo_led",
    version="1.0.0",
    capabilities=["rgb", "wifi", "tapo"],
    config_schema="schemas/tapo.yaml",
)
class TapoEmitter(EmitterInterface):
    """Emit Chromagrams frames to a Tapo LED device."""

    def __init__(self, config=None, device=None):
        self.config = config or CONFIG
        self.settings = get_emitter_settings(self.config, "tapo_led")
        self.enabled = bool(self.settings.get("enabled", False))
        self.transition_ms = int(self.settings.get("transition_ms", 50))

        self.device = device
        if self.device is None and self.enabled:
            self.device = TapoLedDevice(
                device_ip=self.settings.get("device_ip", ""),
                auth_token=self.settings.get("auth_token", ""),
            )

    def _log(self, level: str, message: str):
        if _LOGGER is None:
            return
        try:
            token = "!info" if level == "info" else "!error"
            _LOGGER.colour_log(token, message)
        except Exception:
            return

    def render(self, frame):
        if not self.enabled:
            self._log("info", "tapo_led emitter is disabled")
            return {"emitted": False, "reason": "disabled"}

        if self.device is None:
            raise RuntimeError("tapo_led emitter has no device instance")

        rgb = frame.get("rgb") if isinstance(frame, dict) else None
        if not isinstance(rgb, (list, tuple)) or len(rgb) != 3:
            raise ValueError("frame must contain rgb as a 3-value list or tuple")

        result = self.device.set_rgb(rgb=rgb, transition_ms=self.transition_ms)
        self._log("info", f"tapo_led emitted rgb={rgb}")
        return {"emitted": True, "result": result}
