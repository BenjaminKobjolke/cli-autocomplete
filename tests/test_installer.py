from pathlib import Path

import pytest

from src.installer import install_launcher, writable_path_dirs

AUTO_BAT = (
    "@echo off\n"
    ":: Keep cwd — the tool completes arguments from the current directory.\n"
    'uv run --project "%~dp0." python "%~dp0clicomplete.py" %*\n'
)


def make_repo(tmp_path: Path) -> Path:
    """A fake repo dir holding an auto.bat that uses %~dp0."""
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "auto.bat").write_text(AUTO_BAT, encoding="utf-8")
    return repo


def test_install_launcher_bakes_absolute_repo_path(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    target = tmp_path / "path_dir"
    target.mkdir()

    written = install_launcher(target, repo)

    assert written == target / "auto.bat"
    content = written.read_text(encoding="utf-8")
    assert "%~dp0" not in content
    assert str(repo) in content
    # The command still points at the repo's clicomplete.py.
    assert f"{repo}\\clicomplete.py" in content


def test_install_launcher_overwrites_existing(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    target = tmp_path / "path_dir"
    target.mkdir()
    (target / "auto.bat").write_text("old", encoding="utf-8")

    install_launcher(target, repo)

    assert "old" not in (target / "auto.bat").read_text(encoding="utf-8")


def test_install_launcher_missing_source_raises(tmp_path: Path) -> None:
    repo = tmp_path / "empty_repo"
    repo.mkdir()
    target = tmp_path / "path_dir"
    target.mkdir()

    with pytest.raises(FileNotFoundError):
        install_launcher(target, repo)


def test_writable_path_dirs_filters_bogus_entries(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    real = tmp_path / "real"
    real.mkdir()
    bogus = tmp_path / "does_not_exist"
    entries = [str(real), str(bogus), ""]
    monkeypatch.setenv("PATH", ";".join(entries))

    result = writable_path_dirs()

    assert real in result
    assert bogus not in result


def test_writable_path_dirs_dedups_preserving_order(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    a = tmp_path / "a"
    a.mkdir()
    b = tmp_path / "b"
    b.mkdir()
    monkeypatch.setenv("PATH", ";".join([str(a), str(b), str(a)]))

    result = writable_path_dirs()

    assert result == [a, b]
