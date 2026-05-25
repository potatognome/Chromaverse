from Dev.Chromagrams.src.Chromagrams.config import CONFIG


def test_config_loads_defaults():
    defaults = CONFIG.get("ANIMATION_DEFAULTS", {})
    assert defaults.get("FRAME_COUNT") == 8
    assert defaults.get("AMPLITUDE") == 0.5
