"""Scheme interface contract."""

from __future__ import annotations

from abc import ABC, abstractmethod


class SchemeInterface(ABC):
    """Base contract for colour scheme generators."""

    @abstractmethod
    def generate(self, *args, **kwargs):
        """Generate deterministic scheme output."""
