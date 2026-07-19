import os
from pathlib import Path

# The launcher name is the command users type (`auto`).
LAUNCHER_NAME = "auto.bat"

# Token in the repo's auto.bat that resolves to "its own folder". A copy placed in a
# different PATH folder must not rely on it, so we bake in the absolute repo path instead.
SELF_DIR_TOKEN = "%~dp0"


def writable_path_dirs() -> list[Path]:
    """Existing, writable directories currently on the user's PATH.

    Returns:
        list[Path]: PATH entries that exist, are directories, and are writable,
            deduplicated with first-seen order preserved.
    """
    seen: set[Path] = set()
    result: list[Path] = []
    for entry in os.environ.get("PATH", "").split(os.pathsep):
        if not entry:
            continue
        path = Path(entry)
        if path in seen:
            continue
        if path.is_dir() and os.access(path, os.W_OK):
            seen.add(path)
            result.append(path)
    return result


def install_launcher(target_dir: Path, repo_dir: Path) -> Path:
    """Write a global `auto.bat` launcher into ``target_dir``.

    The repo's own ``auto.bat`` is the single source of truth for the command line; we
    copy it and replace ``%~dp0`` with the absolute repo path so the launcher works from
    any folder. An existing launcher is overwritten.

    Args:
        target_dir (Path): Directory to write the launcher into (usually a PATH folder).
        repo_dir (Path): Directory containing the repo's auto.bat and clicomplete.py.

    Returns:
        Path: The written launcher file.

    Raises:
        FileNotFoundError: If the repo's auto.bat template is missing.
    """
    source = repo_dir / LAUNCHER_NAME
    if not source.is_file():
        raise FileNotFoundError(f"Launcher template not found: {source}")

    content = source.read_text(encoding="utf-8")
    launcher = content.replace(SELF_DIR_TOKEN, f"{repo_dir}{os.sep}")

    destination = target_dir / LAUNCHER_NAME
    destination.write_text(launcher, encoding="utf-8")
    return destination
