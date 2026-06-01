"""Main CLI entry point for ChromaTutor instruction interpretation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .canvas_renderer import render_canvas
from .glyph_mapper import map_plan_to_glyphs
from .linter import lint_instructions
from .parser import parse_instructions
from .sequencer import sequence_instructions


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="chromatutor",
        description="ChromaTutor procedural interpreter and instructional canvas synthesizer",
    )
    parser.add_argument(
        "--input-file",
        help="Path to a text file containing step-by-step instructions.",
    )
    parser.add_argument(
        "--input-text",
        help="Inline instruction text. Use newline characters between steps.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="Emit pipeline output as JSON instead of formatted text.",
    )
    return parser


def _load_input(args: argparse.Namespace) -> tuple[str, str]:
    if args.input_text:
        return args.input_text, "inline"
    if args.input_file:
        path = Path(args.input_file)
        return path.read_text(encoding="utf-8"), str(path)
    default_text = """1. Read the procedure file
2. Parse each instruction line
3. Validate action wording
4. Sequence executable steps
5. Render the instructional canvas"""
    return default_text, "default-sample"


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    text, source_name = _load_input(args)
    parsed = parse_instructions(text, source_name=source_name)
    issues = lint_instructions(parsed)
    plan = sequence_instructions(parsed)
    glyphs = map_plan_to_glyphs(plan)
    canvas = render_canvas(glyphs)

    if args.as_json:
        payload = {
            "source": parsed.source_name,
            "steps": [
                {
                    "index": step.index,
                    "text": step.normalized_text,
                }
                for step in parsed.steps
            ],
            "lint_issues": [
                {
                    "step_index": issue.step_index,
                    "severity": issue.severity,
                    "code": issue.code,
                    "message": issue.message,
                }
                for issue in issues
            ],
            "plan": [
                {
                    "sequence_index": step.sequence_index,
                    "step_index": step.step_index,
                    "action": step.action,
                    "object": step.object_text,
                    "dependencies": step.dependencies,
                }
                for step in plan
            ],
            "glyphs": [
                {
                    "sequence_index": step.sequence_index,
                    "step_index": step.step_index,
                    "glyph": step.glyph,
                    "action": step.action,
                    "object": step.object_text,
                }
                for step in glyphs
            ],
            "canvas": canvas,
        }
        print(json.dumps(payload, indent=2))
        return

    print("ChromaTutor Procedural Interpretation")
    print(f"Source: {parsed.source_name}")
    print(f"Parsed steps: {len(parsed.steps)}")
    print(f"Lint issues: {len(issues)}")
    if issues:
        print("Lint details:")
        for issue in issues:
            print(f"  - Step {issue.step_index} [{issue.severity}] {issue.code}: {issue.message}")
    print()
    print(canvas)

if __name__ == "__main__":
    main()
