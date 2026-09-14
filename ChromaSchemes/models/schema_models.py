"""Typed model helpers for ChromaSchemes payloads."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ChromaSchemeInput:
    """Normalised input payload for ChromaSchemes generation."""

    base_hex: str
    geometry_model: str
    overlays: list[dict[str, Any]] = field(default_factory=list)
    desired_colour_count: int = 8


@dataclass(frozen=True)
class ChromaSchemeOutput:
    """Structured output payload returned by the scheme engine."""

    colourSet: list[dict[str, Any]]
    roles: dict[str, Any]
    geometry: dict[str, Any]
    preview: dict[str, Any]
