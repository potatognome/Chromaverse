from Dev.ChromaEmitters.src.chromaemitters.config_loader import load_emitter_config


def test_config_loading_has_tapo_settings():
    config = load_emitter_config()
    assert "emitters" in config
    assert "tapo_led" in config["emitters"]
