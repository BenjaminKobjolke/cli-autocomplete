from pathlib import Path

from src.config_manager import ConfigManager


def make_manager(tmp_path: Path) -> ConfigManager:
    return ConfigManager(config_file=tmp_path / "config.json")


def test_creates_default_config(tmp_path: Path) -> None:
    manager = make_manager(tmp_path)
    assert manager.get_paths() == []
    assert (tmp_path / "config.json").exists()


def test_add_and_get_paths(tmp_path: Path) -> None:
    manager = make_manager(tmp_path)
    target = tmp_path / "scripts"
    target.mkdir()

    assert manager.add_path(str(target)) is True
    assert manager.get_paths() == [str(target.resolve())]


def test_add_duplicate_path_rejected(tmp_path: Path) -> None:
    manager = make_manager(tmp_path)
    target = tmp_path / "scripts"
    target.mkdir()

    manager.add_path(str(target))
    assert manager.add_path(str(target)) is False
    assert len(manager.get_paths()) == 1


def test_remove_path(tmp_path: Path) -> None:
    manager = make_manager(tmp_path)
    target = tmp_path / "scripts"
    target.mkdir()
    manager.add_path(str(target))

    assert manager.remove_path(str(target)) is True
    assert manager.get_paths() == []


def test_remove_missing_path_rejected(tmp_path: Path) -> None:
    manager = make_manager(tmp_path)
    assert manager.remove_path(str(tmp_path / "nope")) is False


def test_corrupt_config_falls_back_to_empty(tmp_path: Path) -> None:
    config_file = tmp_path / "config.json"
    config_file.write_text("{not json", encoding="utf-8")

    manager = ConfigManager(config_file=config_file)
    assert manager.get_paths() == []


def test_config_persists_across_instances(tmp_path: Path) -> None:
    target = tmp_path / "scripts"
    target.mkdir()

    make_manager(tmp_path).add_path(str(target))
    assert make_manager(tmp_path).get_paths() == [str(target.resolve())]
