from ChromaTools.config import CONFIG, load_config


def test_config_loads_project_metadata():
    config = load_config()

    assert config["INFO"]["PROJECT_NAME"] == "ChromaTools"
    assert config["CLI_DEFAULTS"]["SHOW_DISABLED_APPS"] is True


def test_config_defines_launchable_cli_apps():
    apps = CONFIG["APPS"]

    assert apps["chromaspace"]["launch_command"] == ["chromaspace"]
    assert apps["chromatutor"]["launch_command"] == ["chromatutor"]

