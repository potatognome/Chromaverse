from pathlib import Path
import sys
from io import StringIO
import unittest
from unittest.mock import patch

SRC_ROOT = Path(__file__).resolve().parents[1] / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from ChromaTools.catalog import AppRecord
from ChromaTools.main import CONFIG, PROJECT_ROOT, launch_app, menu


class MainTests(unittest.TestCase):
    def test_menu_quits_cleanly(self) -> None:
        outputs = StringIO()
        inputs = iter(["Q"])

        def _input(_: str) -> str:
            return next(inputs)

        menu(
            config=CONFIG,
            input_func=_input,
            output_func=lambda text: outputs.write(text + "\n"),
        )

        self.assertIn("=== ChromaTools ===", outputs.getvalue())

    def test_launch_app_reports_missing_command(self) -> None:
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

        self.assertFalse(launched)
        self.assertEqual(outputs, ["Chromagrams has no launch command configured."])

    def test_launch_app_runs_configured_command(self) -> None:
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

        self.assertTrue(launched)
        self.assertEqual(outputs[-1], "Chromaspace finished successfully.")
