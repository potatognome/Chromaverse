from ChromaTools.catalog import load_app_catalog, resolve_app
from ChromaTools.config import CONFIG, PROJECT_ROOT


def test_catalog_includes_chroma_projects():
    apps = load_app_catalog(CONFIG, PROJECT_ROOT)
    keys = {app.key for app in apps}

    assert {
        "chromaspace",
        "chromagrams",
        "chromaglyphs",
        "chromatutor",
        "chromaemitters",
        "chromaschemes",
    }.issubset(keys)


def test_resolve_app_supports_numeric_and_key_selection():
    apps = load_app_catalog(CONFIG, PROJECT_ROOT)

    assert resolve_app("1", apps) == apps[0]
    assert resolve_app("chromaspace", apps).name == "Chromaspace"
    assert resolve_app("ChromaGlyphs", apps).key == "chromaglyphs"

