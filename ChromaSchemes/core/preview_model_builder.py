"""Build deterministic multi-pane preview models."""

from __future__ import annotations


class PreviewModelBuilder:
    """Generate a pure multi-pane fractal quadrant preview model."""

    def build(self, colour_set: list[dict], roles: dict) -> dict:
        refs = [entry["id"] for entry in colour_set]
        border_ref = roles.get("border_fg", {}).get("layers", {}).get("fg", {}).get("colourRef", refs[0])

        panes = []
        for idx in range(4):
            panes.append(
                {
                    "paneId": f"pane_{idx}",
                    "layout": "fractal_quadrant",
                    "roleUsageHints": {
                        "backgroundRole": ["primary_surface", "secondary_surface", "tertiary_surface", "accent_surface"][idx],
                        "interactiveRole": "interactive_bg",
                        "textRole": "menu_fg",
                    },
                    "border": {"colourRef": border_ref},
                    "fill": {"colourRef": refs[idx % len(refs)]},
                }
            )

        return {"model": "MultiPanePreviewModel", "panes": panes}
