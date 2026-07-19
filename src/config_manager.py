import json
from pathlib import Path

from .app_logger import AppLogger


class ConfigManager:
    """Manages the configuration file for storing and retrieving paths."""

    def __init__(self, config_file: Path | None = None):
        """Initialize the config manager.

        Args:
            config_file (Optional[Path]): Config file location; defaults to
                config.json next to the application entry point.
        """
        self.logger = AppLogger("ConfigManager")
        script_dir = Path(__file__).parent.parent
        self.config_file = config_file or script_dir / "config.json"
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """Load the configuration from the JSON file.

        Returns:
            dict: Configuration data
        """
        if not self.config_file.exists():
            self.logger.info("Config file not found. Creating new one.")
            default_config: dict = {"paths": []}
            self._save_config(default_config)
            return default_config

        try:
            with open(self.config_file) as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            self.logger.error(f"Error reading config file: {e}")
            return {"paths": []}

    def _save_config(self, config: dict) -> None:
        """Save the configuration to the JSON file.

        Args:
            config (dict): Configuration data to save
        """
        try:
            with open(self.config_file, "w") as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving config file: {e}")

    def get_paths(self) -> list[str]:
        """Get the list of configured paths.

        Returns:
            List[str]: List of configured paths
        """
        return self.config.get("paths", [])

    def add_path(self, path: str) -> bool:
        """Add a new path to the configuration.

        Args:
            path (str): Path to add

        Returns:
            bool: True if path was added successfully
        """
        path = str(Path(path).resolve())
        paths = self.get_paths()

        if path in paths:
            self.logger.warning(f"Path already exists: {path}")
            return False

        paths.append(path)
        self.config["paths"] = paths
        self._save_config(self.config)
        return True

    def remove_path(self, path: str) -> bool:
        """Remove a path from the configuration.

        Args:
            path (str): Path to remove

        Returns:
            bool: True if path was removed successfully
        """
        path = str(Path(path).resolve())
        paths = self.get_paths()

        if path not in paths:
            self.logger.warning(f"Path not found: {path}")
            return False

        paths.remove(path)
        self.config["paths"] = paths
        self._save_config(self.config)
        return True
