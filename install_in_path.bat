@echo off
:: Copy an 'auto.bat' launcher into a PATH folder so 'auto' works globally.
uv run --project "%~dp0." python "%~dp0clicomplete.py" --install %*
