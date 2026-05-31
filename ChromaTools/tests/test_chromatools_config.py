from pathlib import Path
import sys
import unittest

SRC_ROOT = Path(__file__).resolve().parents[1] / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from ChromaTools.settings import CONFIG, load_config


class ConfigTests(unittest.TestCase):
    def test_config_loads_project_metadata(self) -> None:
        config = load_config()

        self.assertEqual(config["INFO"]["PROJECT_NAME"], "ChromaTools")
        self.assertIs(config["CLI_DEFAULTS"]["SHOW_DISABLED_APPS"], True)

    def test_config_defines_launchable_cli_apps(self) -> None:
        apps = CONFIG["APPS"]

        self.assertEqual(apps["chromaspace"]["launch_command"], ["chromaspace"])
        self.assertEqual(apps["chromatutor"]["launch_command"], ["chromatutor"])
