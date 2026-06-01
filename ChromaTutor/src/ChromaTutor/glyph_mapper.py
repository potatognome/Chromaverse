"""Symbolic mapping from planned actions to ChromaTutor glyphs."""

from __future__ import annotations

from typing import Dict, List

from .models import GlyphStep, PlannedStep


_ACTION_GLYPH_MAP: Dict[str, str] = {
    "read": "[R]",
    "parse": "[P]",
    "lint": "[L]",
    "validate": "[V]",
    "verify": "[V]",
    "sequence": "[S]",
    "render": "[C]",
    "write": "[W]",
    "save": "[W]",
    "sync": "[Y]",
    "run": "[>]",
}


def map_plan_to_glyphs(plan: List[PlannedStep]) -> List[GlyphStep]:
    """Map planned steps to symbolic glyph steps for canvas rendering."""
    glyphs: List[GlyphStep] = []

    for step in plan:
        glyph = _ACTION_GLYPH_MAP.get(step.action, "[?]")
        glyphs.append(
            GlyphStep(
                sequence_index=step.sequence_index,
                step_index=step.step_index,
                glyph=glyph,
                action=step.action,
                object_text=step.object_text,
            )
        )

    return glyphs
