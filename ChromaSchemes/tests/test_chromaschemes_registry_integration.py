from Dev.Chromaspace.src.Chromaspace.registry import (
    MODULE_TYPE_SCHEME_GENERATOR,
    get,
    metadata,
)

from Dev.Chromaschemes.src.Chromaschemes.generators.orbit import OrbitSchemeGenerator


def test_orbit_is_registered_in_chromacore():
    factory = get(MODULE_TYPE_SCHEME_GENERATOR, "orbit")
    assert factory is OrbitSchemeGenerator

    info = metadata(MODULE_TYPE_SCHEME_GENERATOR, "orbit")
    assert info.name == "orbit"
    assert "rotational" in info.capabilities
