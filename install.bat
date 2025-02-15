@echo off
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing requirements...
pip install -r requirements.txt

echo Installation complete!
echo.
echo Please add "%~dp0" to your Windows PATH to use 'auto' command from anywhere.
echo.
pause
