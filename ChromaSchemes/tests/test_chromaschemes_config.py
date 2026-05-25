from Dev.Chromaschemes.src.Chromaschemes.config import CONFIG


def test_config_loads_defaults():
    defaults = CONFIG.get("SCHEME_DEFAULTS", {})
    assert defaults.get("BASE_ROTATION_DEGREES") == 30
    assert defaults.get("STEPS") == 4
