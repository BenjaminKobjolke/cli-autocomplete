from pathlib import Path

import pytest

from src.config_manager import ConfigManager
from src.path_completer import PathCompleter


@pytest.fixture
def scripts_dir(tmp_path: Path) -> Path:
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    (scripts / "alpha.bat").write_text("@echo off", encoding="utf-8")
    (scripts / "album.bat").write_text("@echo off", encoding="utf-8")
    (scripts / "beta.bat").write_text("@echo off", encoding="utf-8")
    return scripts


@pytest.fixture
def config_manager(tmp_path: Path, scripts_dir: Path) -> ConfigManager:
    manager = ConfigManager(config_file=tmp_path / "config.json")
    manager.add_path(str(scripts_dir))
    return manager


def test_configured_paths_prefix_match(config_manager: ConfigManager, scripts_dir: Path) -> None:
    completer = PathCompleter(config_manager, current_dir=False)

    names = [c.text for c in completer.get_completions_for("al")]

    assert sorted(names) == ["album.bat", "alpha.bat"]
    assert completer.path_map["alpha.bat"] == str(scripts_dir / "alpha.bat")


def test_match_is_case_insensitive(config_manager: ConfigManager) -> None:
    completer = PathCompleter(config_manager, current_dir=False)
    names = [c.text for c in completer.get_completions_for("ALPHA")]
    assert names == ["alpha.bat"]


def test_no_match_returns_empty(config_manager: ConfigManager) -> None:
    completer = PathCompleter(config_manager, current_dir=False)
    assert completer.get_completions_for("zzz") == []


def test_missing_configured_path_is_skipped(tmp_path: Path) -> None:
    manager = ConfigManager(config_file=tmp_path / "config.json")
    gone = tmp_path / "gone"
    gone.mkdir()
    manager.add_path(str(gone))
    gone.rmdir()

    completer = PathCompleter(manager, current_dir=False)
    assert completer.get_completions_for("") == []


def test_current_dir_completions(
    config_manager: ConfigManager, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    workdir = tmp_path / "work"
    workdir.mkdir()
    (workdir / "input.txt").write_text("data", encoding="utf-8")
    monkeypatch.chdir(workdir)

    completer = PathCompleter(config_manager, current_dir=True)
    names = [c.text for c in completer.get_completions_for("in")]

    assert names == ["input.txt"]


def test_get_first_completion_resolves_full_path(
    config_manager: ConfigManager, scripts_dir: Path
) -> None:
    completer = PathCompleter(config_manager, current_dir=False)
    assert completer.get_first_completion("beta") == str(scripts_dir / "beta.bat")
    assert completer.get_first_completion("zzz") is None
