from Chromaspace.colour_engine import to_rgb
from Chromaspace.registry import (
    MODULE_TYPE_COLOUR_SPACE,
    find,
    get,
    metadata,
)


def test_colour_spaces_are_registered():
    for name in ["hsv", "oklch", "lab"]:
        factory = get(MODULE_TYPE_COLOUR_SPACE, name)
        assert factory is not None
        info = metadata(MODULE_TYPE_COLOUR_SPACE, name)
        assert info.name == name
        assert "deterministic" in info.capabilities


def test_colour_engine_uses_registry_adapters():
    rgb = to_rgb(0, 1.0, 1.0, method="hsv")
    assert rgb == [255, 0, 0]


def test_find_by_capability_returns_registered_adapters():
    adapters = find(MODULE_TYPE_COLOUR_SPACE, "rgb")
    assert len(adapters) >= 3
