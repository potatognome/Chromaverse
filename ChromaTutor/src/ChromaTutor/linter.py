"""Instruction lint checks for parsed procedural steps."""

from __future__ import annotations

from typing import List

from .models import LintIssue, ParsedInstructions


_COMMON_ACTIONS = {
    "add",
    "align",
    "apply",
    "attach",
    "check",
    "click",
    "configure",
    "connect",
    "create",
    "deploy",
    "enable",
    "enter",
    "install",
    "load",
    "open",
    "parse",
    "press",
    "read",
    "render",
    "replace",
    "run",
    "save",
    "select",
    "set",
    "start",
    "sync",
    "update",
    "validate",
    "verify",
    "write",
}


def lint_instructions(parsed: ParsedInstructions) -> List[LintIssue]:
    """Lint parsed instructions and return quality findings."""
    issues: List[LintIssue] = []

    if not parsed.steps:
        issues.append(
            LintIssue(
                step_index=0,
                severity="error",
                code="no_steps",
                message="No procedural steps were found in the input.",
            )
        )
        return issues

    for step in parsed.steps:
        text = step.normalized_text
        words = text.split()

        if len(words) < 2:
            issues.append(
                LintIssue(
                    step_index=step.index,
                    severity="warning",
                    code="too_short",
                    message="Step is very short and may be ambiguous.",
                )
            )
            continue

        first = words[0].lower()
        if first not in _COMMON_ACTIONS:
            issues.append(
                LintIssue(
                    step_index=step.index,
                    severity="warning",
                    code="unknown_action",
                    message=f"Step does not start with a recognized action verb: '{words[0]}'.",
                )
            )

        if "maybe" in text.lower() or "etc" in text.lower():
            issues.append(
                LintIssue(
                    step_index=step.index,
                    severity="warning",
                    code="ambiguous_language",
                    message="Step contains ambiguous language ('maybe' or 'etc').",
                )
            )

    return issues
