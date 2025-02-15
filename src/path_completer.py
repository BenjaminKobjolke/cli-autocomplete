from pathlib import Path
from typing import List, Iterable
from prompt_toolkit.completion import Completer, Completion
from .config_manager import ConfigManager
from .logger import Logger

class PathCompleter(Completer):
    """Custom completer for paths from configured directories and current directory."""
    
    def __init__(self, config_manager: ConfigManager, current_dir: bool = False):
        """Initialize the path completer.
        
        Args:
            config_manager (ConfigManager): Instance of config manager
            current_dir (bool): Whether to complete from current directory
        """
        self.logger = Logger("PathCompleter")
        self.config_manager = config_manager
        self.current_dir = current_dir
        self.path_map = {}  # Maps display names to full paths
    
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
            current_path = Path('.')
            for item in current_path.glob('*'):
                name = str(item.name)
                if name.lower().startswith(word.lower()):
                    self.path_map[name] = str(item)
                    yield Completion(
                        name,
                        start_position=-len(word),
                        display=name
                    )
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
            for base_path in self.config_manager.get_paths():
                base_path = Path(base_path)
                if not base_path.exists():
                    continue
                    
                for item in base_path.glob('*'):
                    name = str(item.name)
                    if name.lower().startswith(word.lower()):
                        full_path = str(item)
                        self.path_map[name] = full_path
                        yield Completion(
                            name,
                            start_position=-len(word),
                            display=name
                        )
        except Exception as e:
            self.logger.error(f"Error completing configured paths: {e}")
    
    def get_first_completion(self, text: str) -> str | None:
        """Get the first matching completion for the given text.
        
        Args:
            text (str): Text to complete
            
        Returns:
            str | None: First matching completion or None if no matches found
        """
        class MockDocument:
            def get_word_before_cursor(self):
                return text
                
        completions = list(self.get_completions(MockDocument(), None))
        if not completions:
            return None
            
        completed_text = completions[0].text
        return self.path_map.get(completed_text)
