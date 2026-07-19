import argparse
from pathlib import Path

from .app_logger import AppLogger
from .config_manager import ConfigManager
from .installer import install_launcher, writable_path_dirs

# argparse default for --install when the flag is absent; distinct from None (flag present,
# no folder given) so we can tell "not requested" from "requested interactively".
_INSTALL_NOT_REQUESTED = "__not_requested__"


class CLIParser:
    """Handles command line argument parsing and validation."""

    def __init__(self, config_manager: ConfigManager):
        """Initialize the CLI parser.

        Args:
            config_manager (ConfigManager): Shared config manager instance
        """
        self.logger = AppLogger("CLIParser")
        self.config_manager = config_manager
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create and configure the argument parser.

        Returns:
            argparse.ArgumentParser: Configured parser
        """
        parser = argparse.ArgumentParser(
            description="CLI tool for path autocompletion and command execution"
        )

        parser.add_argument("--list", action="store_true", help="List all configured paths")

        parser.add_argument(
            "--add", type=str, metavar="PATH", help="Add a new path to the configuration"
        )

        parser.add_argument(
            "--delete", type=str, metavar="PATH", help="Remove a path from the configuration"
        )

        parser.add_argument(
            "--install",
            nargs="?",
            const=None,
            default=_INSTALL_NOT_REQUESTED,
            metavar="FOLDER",
            help=(
                "Copy an 'auto.bat' launcher into a PATH folder so 'auto' works globally. "
                "Pass a folder to install there directly, or omit it to pick interactively."
            ),
        )

        parser.add_argument("filter", nargs="?", help="Initial filter for command completion")

        return parser

    def parse_args(self, argv: list[str] | None = None) -> tuple[argparse.Namespace, bool]:
        """Parse command line arguments.

        Args:
            argv (Optional[List[str]]): Arguments to parse; defaults to sys.argv

        Returns:
            Tuple[argparse.Namespace, bool]: Parsed arguments and whether to enter interactive mode
        """
        args = self.parser.parse_args(argv)

        # Handle --list argument
        if args.list:
            paths = self.config_manager.get_paths()
            if paths:
                self.logger.info("Configured paths:")
                for i, path in enumerate(paths, 1):
                    self.logger.info(f"  {i}. {path}")
            else:
                self.logger.info("No paths configured")
            return args, False

        # Handle --add argument
        if args.add:
            original_input = args.add
            add_target = Path(args.add).resolve()
            if not add_target.exists():
                self.logger.error(f"Path does not exist: {add_target}")
                return args, False

            if self.config_manager.add_path(str(add_target)):
                if original_input == ".":
                    self.logger.info(f"Added current directory: {add_target}")
                else:
                    self.logger.info(f"Added path: {add_target}")
            return args, False

        # Handle --delete argument
        if args.delete:
            paths = self.config_manager.get_paths()
            try:
                # Try to parse as number first
                index = int(args.delete)
                if 1 <= index <= len(paths):
                    path_to_remove = paths[index - 1]
                    if self.config_manager.remove_path(path_to_remove):
                        self.logger.info(f"Removed path: {path_to_remove}")
                else:
                    self.logger.error("Invalid path number. Use --list to see available paths.")
            except ValueError:
                # If not a number, try as path
                delete_target = Path(args.delete).resolve()
                if self.config_manager.remove_path(str(delete_target)):
                    self.logger.info(f"Removed path: {delete_target}")
            return args, False

        # Handle --install argument
        if args.install != _INSTALL_NOT_REQUESTED:
            self._handle_install(args.install)
            return args, False

        # No arguments provided, enter interactive mode
        return args, True

    def _handle_install(self, folder: str | None) -> None:
        """Install a global 'auto.bat' launcher into a PATH folder.

        Args:
            folder (Optional[str]): Target folder passed on the command line, or None to
                choose interactively (pick a number from PATH, or paste a path).
        """
        repo_dir = Path(__file__).parent.parent

        target = self._resolve_install_target(folder)
        if target is None:
            return

        if not target.is_dir():
            self.logger.error(f"Not a directory: {target}")
            return

        if target not in writable_path_dirs():
            self.logger.warning(
                f"'{target}' is not on your PATH. Add it to PATH, or pick a folder that "
                "already is, for 'auto' to work globally."
            )

        launcher = target / "auto.bat"
        if launcher.exists():
            self.logger.info(f"Overwriting existing launcher: {launcher}")

        try:
            written = install_launcher(target, repo_dir)
        except OSError as e:
            self.logger.error(f"Install failed: {e}")
            return

        self.logger.info(f"Installed launcher: {written}")
        self.logger.info("Restart your shell, then run 'auto' from anywhere.")

    def _resolve_install_target(self, folder: str | None) -> Path | None:
        """Resolve the install target from a CLI value or interactive selection.

        Returns:
            Optional[Path]: Chosen directory, or None if the user made no valid choice.
        """
        if folder is not None:
            return Path(folder).expanduser().resolve()

        dirs = writable_path_dirs()
        if dirs:
            self.logger.info("Writable folders on your PATH:")
            for i, path in enumerate(dirs, 1):
                self.logger.info(f"  {i}. {path}")
        else:
            self.logger.info("No writable PATH folders auto-detected; paste a folder path.")

        reply = input("Pick a number, or paste a folder path: ").strip()
        if not reply:
            self.logger.error("No folder selected.")
            return None

        # Mirror --delete: a bare number selects from the list, anything else is a path.
        if reply.isdigit():
            index = int(reply)
            if 1 <= index <= len(dirs):
                return dirs[index - 1]
            self.logger.error("Invalid number.")
            return None

        return Path(reply).expanduser().resolve()
