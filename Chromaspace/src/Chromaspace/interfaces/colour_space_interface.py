"""Colour-space interface contract."""

from __future__ import annotations

from abc import ABC, abstractmethod


class ColourSpaceInterface(ABC):
    """Base contract for colour-space adapters."""

    @abstractmethod
    def to_rgb(self, h, s, l):
        """Convert semantic colour values to RGB."""
