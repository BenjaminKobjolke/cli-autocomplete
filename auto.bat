@echo off
:: Keep cwd — the tool completes arguments from the current directory.
uv run --project "%~dp0." python "%~dp0clicomplete.py" %*
