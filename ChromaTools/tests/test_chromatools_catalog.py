from pathlib import Path
import sys
import unittest

SRC_ROOT = Path(__file__).resolve().parents[1] / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from ChromaTools.catalog import load_app_catalog, resolve_app
from ChromaTools.settings import CONFIG, PROJECT_ROOT


class CatalogTests(unittest.TestCase):
    def test_catalog_includes_chroma_projects(self) -> None:
        apps = load_app_catalog(CONFIG, PROJECT_ROOT)
        keys = {app.key for app in apps}

        self.assertTrue(
            {
                "chromaspace",
                "chromagrams",
                "chromaglyphs",
                "chromatutor",
                "chromaemitters",
                "chromaschemes",
            }.issubset(keys)
        )

    def test_resolve_app_supports_numeric_and_key_selection(self) -> None:
        apps = load_app_catalog(CONFIG, PROJECT_ROOT)

        self.assertEqual(resolve_app("1", apps), apps[0])
        self.assertEqual(resolve_app("chromaspace", apps).name, "Chromaspace")
        self.assertEqual(resolve_app("ChromaGlyphs", apps).key, "chromaglyphs")
