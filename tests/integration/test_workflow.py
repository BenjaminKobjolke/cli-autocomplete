"""Integration tests: ConfigManager + CLIParser + PathCompleter wired together,
exercising the same flow the interactive tool uses (minus the prompt UI)."""

from pathlib import Path

from src.cli_parser import CLIParser
from src.config_manager import ConfigManager
from src.path_completer import PathCompleter


def test_add_list_complete_roundtrip(tmp_path: Path) -> None:
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    script = scripts / "deploy.bat"
    script.write_text("@echo off", encoding="utf-8")

    config_file = tmp_path / "config.json"
    manager = ConfigManager(config_file=config_file)
    parser = CLIParser(manager)

    # --add registers the path and does not enter interactive mode
    _, interactive = parser.parse_args(["--add", str(scripts)])
    assert interactive is False
    assert manager.get_paths() == [str(scripts.resolve())]

    # completion resolves the command exactly like the interactive flow
    completer = PathCompleter(manager, current_dir=False)
    completions = completer.get_completions_for("dep")
    assert [c.text for c in completions] == ["deploy.bat"]
    resolved = completer.path_map["deploy.bat"]
    assert Path(resolved) == script

    # --delete removes it again
    manager_reloaded = ConfigManager(config_file=config_file)
    parser_reloaded = CLIParser(manager_reloaded)
    _, interactive = parser_reloaded.parse_args(["--delete", str(scripts)])
    assert interactive is False
    assert manager_reloaded.get_paths() == []


def test_delete_by_index(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    first.mkdir()
    second.mkdir()

    manager = ConfigManager(config_file=tmp_path / "config.json")
    manager.add_path(str(first))
    manager.add_path(str(second))

    parser = CLIParser(manager)
    parser.parse_args(["--delete", "1"])

    assert manager.get_paths() == [str(second.resolve())]


def test_no_args_enters_interactive_mode(tmp_path: Path) -> None:
    manager = ConfigManager(config_file=tmp_path / "config.json")
    parser = CLIParser(manager)

    args, interactive = parser.parse_args([])

    assert interactive is True
    assert args.filter is None
