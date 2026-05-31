from io import StringIO
from unittest.mock import patch

from ChromaTools.catalog import AppRecord
from ChromaTools.main import CONFIG, PROJECT_ROOT, launch_app, menu


def test_menu_quits_cleanly():
    outputs = StringIO()
    inputs = iter(["Q"])

    def _input(_: str) -> str:
        return next(inputs)

    menu(config=CONFIG, input_func=_input, output_func=lambda text: outputs.write(text + "\n"))

    assert "=== ChromaTools ===" in outputs.getvalue()


def test_launch_app_reports_missing_command():
    outputs = []
    app = AppRecord(
        key="chromagrams",
        name="Chromagrams",
        app_type="python-library",
        description="",
        entry_point="Chromagrams",
        project_path=PROJECT_ROOT,
        config_path=PROJECT_ROOT / "config" / "ChromaTools_CONFIG.json",
        launch_command=(),
    )

    launched = launch_app(app, outputs.append)

    assert launched is False
    assert outputs == ["Chromagrams has no launch command configured."]


def test_launch_app_runs_configured_command():
    outputs = []
    app = AppRecord(
        key="chromaspace",
        name="Chromaspace",
        app_type="python-cli",
        description="",
        entry_point="Chromaspace.main:main",
        project_path=PROJECT_ROOT,
        config_path=PROJECT_ROOT / "config" / "ChromaTools_CONFIG.json",
        launch_command=("chromaspace",),
    )

    with patch("ChromaTools.main.subprocess.run") as run_mock:
        run_mock.return_value.returncode = 0
        launched = launch_app(app, outputs.append)

    assert launched is True
    assert outputs[-1] == "Chromaspace finished successfully."
