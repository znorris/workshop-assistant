@echo off
echo === Ollama Workshop Assistant MCP Server Setup ===
echo.

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python:
    echo   1. Visit https://www.python.org/downloads/
    echo   2. Download Python 3.11 or later
    echo   3. During installation, CHECK "Add Python to PATH"
    echo   4. Restart this command prompt after installation
    echo.
    pause
    exit /b 1
)

echo Python found: 
python --version

REM Create virtual environment
echo.
echo Creating Python virtual environment...
if not exist "..\venv" (
    python -m venv ..\venv
)

REM Activate virtual environment and install dependencies
echo Installing dependencies...
call ..\venv\Scripts\activate.bat
pip install -r ..\requirements.txt

echo.
echo === Setup Complete ===
echo.
echo The MCP server is now ready to use!
echo.
echo To run the MCP server:
echo   ..\venv\Scripts\activate.bat
echo   python ..\server.py
echo.
echo To test the MCP server:
echo   scripts\test_windows.bat
echo.
echo To use with Claude Desktop:
echo   See instructions in ..\claude_config.json
echo.
pause