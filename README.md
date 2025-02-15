# CLI Autocomplete Tool

A Python-based command-line tool that provides autocompletion for executing commands from configured directories with arguments from the current directory.

## Features

- Autocomplete commands from configured paths
- Autocomplete arguments from current directory
- Interactive command selection
- Path configuration management
- Exact match validation with suggestions
- Support for interactive batch files

## Requirements

- Python 3.8 or higher
- Windows operating system

## Installation

1. Clone the repository:

```bash
git clone https://github.com/BenjaminKobjolke/cli-autocomplete.git
cd cli-autocomplete
```

2. Run the installation script:

```bash
install.bat
```

3. Add to Windows PATH:
   - Open System Properties (Win + R, type `sysdm.cpl`)
   - Click "Environment Variables"
   - Under "System Variables", find and select "Path"
   - Click "Edit"
   - Click "New"
   - Add the full path to the cli-autocomplete directory (the directory where you cloned the repository)
   - For example, if you cloned to `D:\Projects\cli-autocomplete`, add that path
   - Click "OK" on all windows
   - Restart any open command prompts

After adding to PATH, you can run the tool from anywhere by simply typing:

```bash
auto
```

## Usage

### Basic Usage

Run the tool using the provided batch file:

```bash
auto
```

Or using Python directly:

```bash
python clicomplete.py
```

### Interactive Mode

1. First prompt: Type and use TAB to autocomplete commands from configured paths
2. Second prompt: Type and use TAB to autocomplete files from current directory
3. The tool executes the selected command with arguments

Example:

```bash
auto
Enter command from configured paths: zip_folder.bat
Enter arguments from current directory: test.txt
Executing: zip_folder.bat test.txt
```

### Managing Paths

List configured paths:

```bash
auto --list
Configured paths:
  1. E:\Tools\Scripts
  2. C:\Utils\Commands
```

Add a new path:

```bash
auto --add "C:\Scripts"
```

Remove a path (by number or full path):

```bash
auto --delete 1
# or
auto --delete "C:\Scripts"
```

### Command Filtering

Start with a filter to show matching commands:

```bash
auto zip
Enter command from configured paths: zip[TAB]
zip_folder.bat    zip_files.bat    zip_archive.bat
```

## Features

- Exact match validation with suggestions for partial matches
- Support for interactive batch files (stdin/stdout)
- Numbered path management
- Command filtering
- Tab completion
- Error handling with helpful messages

## Project Structure

```
cli-autocomplete/
├── clicomplete.py (main script)
├── auto.bat (convenience wrapper)
├── config.json (path configuration)
├── requirements.txt (dependencies)
└── src/
    ├── __init__.py
    ├── logger.py (logging functionality)
    ├── config_manager.py (configuration management)
    ├── path_completer.py (autocompletion logic)
    └── cli_parser.py (argument parsing)
```

## Dependencies

- prompt_toolkit: For interactive command-line interface
- pathlib: For path handling
- Other standard Python libraries

## License

MIT License
