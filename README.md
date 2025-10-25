# CLI Autocomplete Tool

A Python-based command-line tool that provides autocompletion for executing commands from configured directories with arguments from the current directory.

![CLI Autocomplete Tool Demo](media/demo.gif)

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
   - Enter a file/folder name from the current directory
   - Enter `/` or `.` to use the current directory path as the argument
   - Press Enter with no input to run the command without arguments
3. The tool executes the selected command with arguments

Example:

```bash
auto
Enter command from configured paths: zip_folder.bat
Enter arguments from current directory: test.txt
Executing: zip_folder.bat test.txt
```

Using current directory as argument:

```bash
auto
Enter command from configured paths: process_folder.bat
Enter arguments from current directory: /
Using current directory: D:\Projects\MyFolder
Executing: process_folder.bat D:\Projects\MyFolder
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

### Batch File Integration

You can place various batch (.bat) files in your configured source paths to extend functionality. These batch files can perform tasks like:

- Zipping files/folders
- Unzipping archives
- File conversions
- Text processing
- Any other command-line operations

Example batch files:

```bash
zip_folder.bat     # Compress a folder into a zip archive
unzip.bat         # Extract contents of a zip file
convert_pdf.bat   # Convert documents to PDF
rename_files.bat  # Batch rename files with patterns
```

You can find ready-to-use example scripts in the `example_scripts` folder of this repository. These scripts demonstrate common use cases and can serve as templates for creating your own batch files.

To make these example scripts available for autocompletion, add the example_scripts directory to your configured paths:

```bash
auto --add "path\to\cli-autocomplete\example_scripts"
```

For example, if you cloned the repository to `D:\Projects\cli-autocomplete`, you would run:

```bash
auto --add "D:\Projects\cli-autocomplete\example_scripts"
```

The tool will automatically detect and make these batch files available for autocompletion, allowing you to quickly access and execute them with files from your current directory.

#### Available Example Scripts

The repository includes several example scripts that demonstrate common use cases:

- `convert_h265_cpu.bat`: Converts video files to H.265 format using CPU encoding

  - Takes video files as input
  - Uses FFmpeg to convert to H.265 with good compression settings
  - Renames original file with \_h264 suffix
  - Creates new file with \_h265 suffix

- `copy_file_name.bat`: Utility for quick filename copying

  - Copies the input filename to the system clipboard
  - Useful for quick file renaming workflows

- `dummy_image.bat`: Downloads placeholder images for mockups/testing

  - Downloads a random 1920x1080 image from picsum.photos
  - Automatically numbers files (dummy_1.jpg, dummy_2.jpg, etc.)
  - Perfect for testing image processing features

- `echo.bat`: Simple echo utility for testing
  - Displays the input argument
  - Useful for testing command-line argument passing

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
