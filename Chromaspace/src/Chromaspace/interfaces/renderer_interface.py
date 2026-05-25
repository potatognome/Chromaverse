"""Renderer interface contract."""

from __future__ import annotations

from abc import ABC, abstractmethod


class RendererInterface(ABC):
    """Base contract for renderer modules."""

    @abstractmethod
    def render(self, *args, **kwargs):
        """Render output from colour/animation inputs."""
