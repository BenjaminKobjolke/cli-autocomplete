import argparse
from pathlib import Path

from .app_logger import AppLogger
from .config_manager import ConfigManager


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

        # No arguments provided, enter interactive mode
        return args, True
