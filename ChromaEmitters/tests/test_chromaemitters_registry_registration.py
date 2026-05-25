from Dev.Chromaspace.src.Chromaspace.registry import MODULE_TYPE_EMITTER, get, metadata

from Dev.ChromaEmitters.src.chromaemitters.integration.registry_registration import (
    ensure_emitters_registered,
)


def test_emitters_register_in_chromacore_registry():
    ensure_emitters_registered()

    tapo_factory = get(MODULE_TYPE_EMITTER, "tapo_led")
    terminal_factory = get(MODULE_TYPE_EMITTER, "terminal")

    assert tapo_factory is not None
    assert terminal_factory is not None

    info = metadata(MODULE_TYPE_EMITTER, "tapo_led")
    assert "tapo" in info.capabilities
