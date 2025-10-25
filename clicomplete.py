#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path
from prompt_toolkit import prompt, PromptSession
from src.logger import Logger
from src.config_manager import ConfigManager
from src.cli_parser import CLIParser
from src.path_completer import PathCompleter

def main():
    """Main entry point for the CLI autocomplete tool."""
    logger = Logger("Main")
    config_manager = ConfigManager()
    cli_parser = CLIParser()
    
    # Clear any previous state
    command = None
    arguments = None
    
    # Parse command line arguments
    args, interactive_mode = cli_parser.parse_args()
    
    if not interactive_mode:
        return
    
    try:
        # Create prompt session
        session = PromptSession()
        
        # First prompt: complete from configured paths
        configured_completer = PathCompleter(config_manager, current_dir=False)
        while True:
            initial_text = args.filter or ""
            user_input = session.prompt(
                "Enter command from configured paths: ",
                completer=configured_completer,
                default=initial_text,
                complete_in_thread=True,
                complete_while_typing=True,
            ).strip()
            
            if not user_input:
                logger.error("No command entered")
                return
                
            # Get all possible completions
            class MockDocument:
                def get_word_before_cursor(self):
                    return user_input
            completions = list(configured_completer.get_completions(MockDocument(), None))
            
            # Only accept exact matches
            exact_match = next((c for c in completions if c.text == user_input), None)
            if exact_match is None:
                logger.error(f"Command not found: {user_input}")
                if completions:
                    logger.info("Did you mean one of these?")
                    for c in completions:
                        logger.info(f"  - {c.text}")
                continue
                
            command = configured_completer.path_map.get(user_input)
            if not Path(command).exists():
                logger.error(f"Command not found: {user_input}")
                continue
                
            break
        
        # Second prompt: complete from current directory
        current_completer = PathCompleter(config_manager, current_dir=True)
        while True:
            user_input = session.prompt(
                "Enter arguments from current directory: ",
                completer=current_completer,
                complete_in_thread=True,
                complete_while_typing=True
            ).strip()

            if not user_input:
                arguments = ""  # Explicitly set empty string for no arguments
                break

            # Check if user wants to use current directory
            if user_input in ['/', '.']:
                arguments = str(Path.cwd())
                logger.info(f"Using current directory: {arguments}")
                break

            # Get all possible completions for arguments
            class MockDocument:
                def get_word_before_cursor(self):
                    return user_input
            completions = list(current_completer.get_completions(MockDocument(), None))
            
            # Only accept exact matches
            exact_match = next((c for c in completions if c.text == user_input), None)
            if exact_match is None:
                logger.error(f"File not found: {user_input}")
                if completions:
                    logger.info("Did you mean one of these?")
                    for c in completions:
                        logger.info(f"  - {c.text}")
                continue
                
            arguments = current_completer.path_map.get(user_input)
            if not Path(arguments).exists():
                logger.error(f"File not found: {user_input}")
                continue
                
            break
        
        # Construct and execute the command
        display_command = f"{Path(command).name} {Path(arguments).name if arguments else ''}"
        full_command = f"{command} {arguments}" if arguments else command
        logger.info(f"Executing: {display_command}")
        logger.debug(f"Full command: {full_command}")
        
        try:
            result = subprocess.run(
                full_command,
                shell=True,
                check=True,
                stdin=None,
                stdout=None,
                stderr=None
            )
            logger.info("Command executed successfully")
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed with exit code {e.returncode}")
            
    except KeyboardInterrupt:
        logger.info("\nOperation cancelled by user")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
