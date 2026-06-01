"""Instruction parser for procedural text sources."""

from __future__ import annotations

import re

from .models import InstructionStep, ParsedInstructions


_LEADING_MARKER_RE = re.compile(r"^\s*(?:[-*]|\d+[.)])\s+")
_MULTISPACE_RE = re.compile(r"\s+")


def _normalize_line(line: str) -> str:
    """Strip bullet/number markers and normalize whitespace."""
    stripped = _LEADING_MARKER_RE.sub("", line.strip())
    return _MULTISPACE_RE.sub(" ", stripped).strip()


def parse_instructions(text: str, source_name: str = "inline") -> ParsedInstructions:
    """Parse step-by-step instruction text into normalized steps.

    Empty lines are ignored. If no markers are used, each non-empty line is
    still treated as an individual procedural step.
    """
    parsed = ParsedInstructions(source_name=source_name)

    for raw_line in text.splitlines():
        if not raw_line.strip():
            continue
        normalized = _normalize_line(raw_line)
        if not normalized:
            continue
        parsed.steps.append(
            InstructionStep(
                index=len(parsed.steps) + 1,
                raw_text=raw_line.rstrip("\n"),
                normalized_text=normalized,
            )
        )

    return parsed
