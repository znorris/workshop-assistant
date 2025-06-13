@echo off
echo === Testing Ollama Workshop Assistant MCP Server ===
echo.
echo This test will check:
echo   1. Connection to Ollama service
echo   2. MCP tool functionality
echo   3. Model listing and chat capabilities
echo.

REM Activate virtual environment
if exist "..\venv\Scripts\activate.bat" (
    call ..\venv\Scripts\activate.bat
) else (
    echo ERROR: Virtual environment not found. Run setup_windows.bat first.
    pause
    exit /b 1
)

REM Show current Ollama configuration
echo Current configuration:
if defined OLLAMA_HOST (
    echo   OLLAMA_HOST=%OLLAMA_HOST%
) else (
    echo   OLLAMA_HOST=http://localhost:11434 (default)
)
echo.
echo If Ollama is running on a different address, set OLLAMA_HOST:
echo   set OLLAMA_HOST=http://your-host:11434
echo.

REM Run the test
python test_server.py

echo.
echo === Test Complete ===
echo.
echo If the test failed:
echo   1. Make sure Ollama is running: ollama serve
echo   2. Check if you have models installed: ollama list
echo   3. If using WSL/remote, set OLLAMA_HOST environment variable
echo.
pause