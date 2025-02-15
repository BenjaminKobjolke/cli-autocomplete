import logging
from pathlib import Path

class Logger:
    """Custom logger class for the application."""
    
    def __init__(self, name: str = "CLIComplete"):
        """Initialize logger with name and configuration.
        
        Args:
            name (str): Name of the logger instance
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Create logs directory in script directory
        script_dir = Path(__file__).parent.parent
        log_dir = script_dir / "logs"
        log_dir.mkdir(exist_ok=True)
        
        # File handler
        file_handler = logging.FileHandler(log_dir / "cli_complete.log")
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(message)s')
        console_handler.setFormatter(console_formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message: str) -> None:
        """Log info level message.
        
        Args:
            message (str): Message to log
        """
        self.logger.info(message)
    
    def error(self, message: str) -> None:
        """Log error level message.
        
        Args:
            message (str): Message to log
        """
        self.logger.error(message)
    
    def debug(self, message: str) -> None:
        """Log debug level message.
        
        Args:
            message (str): Message to log
        """
        self.logger.debug(message)
    
    def warning(self, message: str) -> None:
        """Log warning level message.
        
        Args:
            message (str): Message to log
        """
        self.logger.warning(message)
