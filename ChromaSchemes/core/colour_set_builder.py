"""Extensible colourSet construction."""

from __future__ import annotations


class ColourSetBuilder:
    """Normalize generated colours into Prismata-compatible colourSet arrays."""

    def build(self, generated_colours: list[dict]) -> list[dict]:
        out: list[dict] = []
        for entry in generated_colours:
            out.append(
                {
                    "id": entry["id"],
                    "origin": entry["origin"],
                    "rgb": entry["rgb"],
                    "oklch": entry["oklch"],
                    "originMetadata": entry.get("metadata", {}),
                }
            )
        return out
