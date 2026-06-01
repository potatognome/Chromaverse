"""Core data models for ChromaTutor instruction processing."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class InstructionStep:
    """One parsed procedural step from an instruction source."""

    index: int
    raw_text: str
    normalized_text: str


@dataclass
class ParsedInstructions:
    """Parsed instruction document with normalized steps."""

    source_name: str
    steps: List[InstructionStep] = field(default_factory=list)


@dataclass
class LintIssue:
    """Lint finding for a parsed step."""

    step_index: int
    severity: str
    code: str
    message: str


@dataclass
class PlannedStep:
    """Sequenced instruction step with explicit dependencies."""

    sequence_index: int
    step_index: int
    action: str
    object_text: str
    dependencies: List[int] = field(default_factory=list)


@dataclass
class GlyphStep:
    """Symbolic representation of a planned step."""

    sequence_index: int
    step_index: int
    glyph: str
    action: str
    object_text: str
