"""Emitter interface contract."""

from __future__ import annotations

from abc import ABC, abstractmethod


class EmitterInterface(ABC):
    """Base contract for output emitters."""

    @abstractmethod
    def render(self, frame):
        """Emit a single frame to the destination device."""
