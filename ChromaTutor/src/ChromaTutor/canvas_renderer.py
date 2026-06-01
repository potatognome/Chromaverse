"""ASCII canvas rendering for glyph-structured procedural plans."""

from __future__ import annotations

from typing import List

from .models import GlyphStep


def render_canvas(glyph_steps: List[GlyphStep]) -> str:
    """Render glyph steps into a deterministic ASCII instructional canvas."""
    if not glyph_steps:
        return "+-------------------------+\n| No steps to render.     |\n+-------------------------+"

    lines = [
        "+--------------------------------------------------------------------------------+",
        "| ChromaTutor Canvas                                                            |",
        "+--------------------------------------------------------------------------------+",
    ]

    for step in glyph_steps:
        summary = f"{step.sequence_index:02d} {step.glyph} {step.action.upper()} {step.object_text}".strip()
        clipped = summary[:78]
        lines.append(f"| {clipped:<78} |")

    lines.append("+--------------------------------------------------------------------------------+")
    return "\n".join(lines)
