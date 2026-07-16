from collections.abc import Iterable
from pathlib import Path

from prompt_toolkit.completion import Completer, Completion

from .app_logger import AppLogger
from .config_manager import ConfigManager


class PathCompleter(Completer):
    """Custom completer for paths from configured directories and current directory."""

    def __init__(self, config_manager: ConfigManager, current_dir: bool = False):
        """Initialize the path completer.

        Args:
            config_manager (ConfigManager): Instance of config manager
            current_dir (bool): Whether to complete from current directory
        """
        self.logger = AppLogger("PathCompleter")
        self.config_manager = config_manager
        self.current_dir = current_dir
        self.path_map: dict[str, str] = {}  # Maps display names to full paths

    def get_completions(self, document, complete_event) -> Iterable[Completion]:
        """Get completions based on the current input.

        Args:
            document: The document to complete
            complete_event: The completion event

        Returns:
            Iterable[Completion]: List of possible completions
        """
        word = document.get_word_before_cursor()

        if self.current_dir:
            # Complete from current directory
            yield from self._get_current_dir_completions(word)
        else:
            # Complete from configured paths
            yield from self._get_configured_paths_completions(word)

    def _get_current_dir_completions(self, word: str) -> Iterable[Completion]:
        """Get completions from the current directory.

        Args:
            word (str): Current word to complete

        Returns:
            Iterable[Completion]: List of possible completions
        """
        try:
            current_path = Path(".")
            for item in current_path.glob("*"):
                name = str(item.name)
                if name.lower().startswith(word.lower()):
                    self.path_map[name] = str(item)
                    yield Completion(name, start_position=-len(word), display=name)
        except Exception as e:
            self.logger.error(f"Error completing current directory paths: {e}")

    def _get_configured_paths_completions(self, word: str) -> Iterable[Completion]:
        """Get completions from configured paths.

        Args:
            word (str): Current word to complete

        Returns:
            Iterable[Completion]: List of possible completions
        """
        try:
            for configured_path in self.config_manager.get_paths():
                base_path = Path(configured_path)
                if not base_path.exists():
                    continue

                for item in base_path.glob("*"):
                    name = str(item.name)
                    if name.lower().startswith(word.lower()):
                        full_path = str(item)
                        self.path_map[name] = full_path
                        yield Completion(name, start_position=-len(word), display=name)
        except Exception as e:
            self.logger.error(f"Error completing configured paths: {e}")

    def get_completions_for(self, text: str) -> list[Completion]:
        """Get all completions for a plain text string (outside a prompt session).

        Args:
            text (str): Text to complete

        Returns:
            List[Completion]: All matching completions
        """

        # Minimal document stand-in: matching treats the full text as the word.
        class _TextDocument:
            def get_word_before_cursor(self) -> str:
                return text

        return list(self.get_completions(_TextDocument(), None))

    def get_first_completion(self, text: str) -> str | None:
        """Get the first matching completion for the given text.

        Args:
            text (str): Text to complete

        Returns:
            str | None: First matching completion or None if no matches found
        """
        completions = self.get_completions_for(text)
        if not completions:
            return None

        completed_text = completions[0].text
        return self.path_map.get(completed_text)
