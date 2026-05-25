from pathlib import Path
import sys


SRC_PATH = Path(__file__).resolve().parents[1] / "src"
TUILKIT_SRC = Path(__file__).resolve().parents[3] / "Core" / "tUilKit" / "src"
for path in [SRC_PATH, TUILKIT_SRC]:
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

from Chromaspace.config import resolve_app_config_path


def test_resolve_app_config_path_prefers_workspace_override(tmp_path):
    workspace_config = tmp_path / ".projects_config" / "CHROMASPACE_CONFIG.json"
    project_config = tmp_path / "Core" / "Chromaspace" / "config" / "CHROMASPACE_CONFIG.json"

    workspace_config.parent.mkdir(parents=True)
    project_config.parent.mkdir(parents=True)
    workspace_config.write_text("{}", encoding="utf-8")
    project_config.write_text("{}", encoding="utf-8")

    resolved = resolve_app_config_path(
        project_path=str(project_config),
        workspace_path=str(workspace_config),
    )

    assert resolved == str(workspace_config)


def test_resolve_app_config_path_falls_back_to_project_config(tmp_path):
    project_config = tmp_path / "Core" / "Chromaspace" / "config" / "CHROMASPACE_CONFIG.json"
    project_config.parent.mkdir(parents=True)
    project_config.write_text("{}", encoding="utf-8")

    resolved = resolve_app_config_path(
        project_path=str(project_config),
        workspace_path=str(tmp_path / ".projects_config" / "CHROMASPACE_CONFIG.json"),
    )

    assert resolved == str(project_config)
