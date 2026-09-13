"""Bind generated colours to Prismata universal roles."""

from __future__ import annotations


UNIVERSAL_ROLES = [
    "primary_surface",
    "secondary_surface",
    "tertiary_surface",
    "accent_surface",
    "border_fg",
    "menu_fg",
    "menu_bg",
    "interactive_fg",
    "interactive_bg",
    "neutral_fg",
    "neutral_bg",
]


class RoleBinder:
    """Map colour IDs to semantic universal roles deterministically."""

    def bind(self, colour_set: list[dict]) -> dict:
        if not colour_set:
            raise ValueError("colour_set cannot be empty")

        refs = [entry["id"] for entry in colour_set]
        payload: dict[str, dict] = {}

        for index, role in enumerate(UNIVERSAL_ROLES):
            colour_ref = refs[index % len(refs)]
            channel = "fg" if role.endswith("_fg") else "bg"
            payload[role] = {"layers": {channel: {"colourRef": colour_ref}}}

        return payload
