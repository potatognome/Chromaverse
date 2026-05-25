"""Animation interface contract."""

from __future__ import annotations

from abc import ABC, abstractmethod


class AnimationInterface(ABC):
    """Base contract for animation sequence modules."""

    @abstractmethod
    def generate_frames(self, *args, **kwargs):
        """Generate deterministic frame sequences."""
