"""Tapo LED device adapter with injectable transport for tests."""

from __future__ import annotations

from typing import Callable, Optional


class TapoLedDevice:
    """Device adapter that emits deterministic payloads for Tapo LEDs."""

    def __init__(
        self,
        device_ip: str,
        auth_token: str = "",
        transport: Optional[Callable[[str, dict], object]] = None,
    ) -> None:
        if not device_ip:
            raise ValueError("device_ip is required")
        self.device_ip = device_ip
        self.auth_token = auth_token
        self._transport = transport

    def _build_payload(self, rgb, transition_ms: int) -> dict:
        return {
            "rgb": [int(rgb[0]), int(rgb[1]), int(rgb[2])],
            "transition_ms": int(transition_ms),
            "auth_token": self.auth_token,
        }

    def set_rgb(self, rgb, transition_ms: int = 50):
        payload = self._build_payload(rgb=rgb, transition_ms=transition_ms)
        endpoint = f"http://{self.device_ip}/chromaemitters/tapo/rgb"
        if self._transport is None:
            return {"endpoint": endpoint, "payload": payload, "sent": False}

        response = self._transport(endpoint, payload)
        return {"endpoint": endpoint, "payload": payload, "sent": True, "response": response}
