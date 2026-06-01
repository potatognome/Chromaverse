"""Instruction sequencer for converting text steps into planned actions."""

from __future__ import annotations

from typing import List

from .models import ParsedInstructions, PlannedStep


def sequence_instructions(parsed: ParsedInstructions) -> List[PlannedStep]:
    """Create an explicit ordered plan from parsed instruction steps."""
    plan: List[PlannedStep] = []

    for position, step in enumerate(parsed.steps, start=1):
        words = step.normalized_text.split(maxsplit=1)
        action = words[0].lower() if words else "unknown"
        object_text = words[1] if len(words) > 1 else ""
        dependencies = [position - 1] if position > 1 else []

        plan.append(
            PlannedStep(
                sequence_index=position,
                step_index=step.index,
                action=action,
                object_text=object_text,
                dependencies=dependencies,
            )
        )

    return plan
