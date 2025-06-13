@echo off
echo === Starting Ollama Workshop Assistant MCP Server ===
echo.

REM Activate virtual environment
if exist "..\venv\Scripts\activate.bat" (
    call ..\venv\Scripts\activate.bat
) else (
    echo ERROR: Virtual environment not found. Run setup_windows.bat first.
    pause
    exit /b 1
)

REM Show current configuration
echo Configuration:
if defined OLLAMA_HOST (
    echo   OLLAMA_HOST=%OLLAMA_HOST%
) else (
    echo   OLLAMA_HOST=http://localhost:11434 (default)
)
echo.
echo Starting MCP server...
echo Press Ctrl+C to stop the server
echo.

REM Run the server
python ..\server.py