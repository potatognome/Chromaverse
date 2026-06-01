"""Tests for ChromaTutor instruction processing pipeline."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from ChromaTutor import (
    lint_instructions,
    map_plan_to_glyphs,
    parse_instructions,
    render_canvas,
    sequence_instructions,
)


def test_pipeline_parses_and_sequences_steps():
    text = """1. Read source instructions
2. Parse lines into steps
3. Render output canvas"""

    parsed = parse_instructions(text, source_name="test")
    issues = lint_instructions(parsed)
    plan = sequence_instructions(parsed)
    glyphs = map_plan_to_glyphs(plan)

    assert len(parsed.steps) == 3
    assert len(plan) == 3
    assert plan[1].dependencies == [1]
    assert glyphs[0].glyph == "[R]"
    assert len([issue for issue in issues if issue.severity == "error"]) == 0


def test_canvas_renderer_outputs_expected_header():
    parsed = parse_instructions("1. Render training panel", source_name="inline")
    plan = sequence_instructions(parsed)
    glyphs = map_plan_to_glyphs(plan)
    canvas = render_canvas(glyphs)

    assert "ChromaTutor Canvas" in canvas
    assert "01" in canvas
    assert "RENDER" in canvas
