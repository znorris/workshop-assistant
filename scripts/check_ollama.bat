@echo off
echo === Checking Ollama Installation and Connection ===
echo.

REM Check if Ollama is installed
where ollama >nul 2>&1
if errorlevel 1 (
    echo ERROR: Ollama is not installed or not in PATH
    echo.
    echo To install Ollama:
    echo   1. Visit https://ollama.ai/download
    echo   2. Download and install Ollama for Windows
    echo   3. Restart this command prompt after installation
    echo.
    pause
    exit /b 1
)

echo Ollama found at:
where ollama
echo.

REM Check if Python is available for network test
python --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Python not found. Skipping network test.
    echo.
    goto :check_models
)

REM Check network connectivity to Ollama API
echo Checking Ollama API connectivity...
echo.

REM Determine which host to check
if defined OLLAMA_HOST (
    echo Testing connection to: %OLLAMA_HOST%
    python -c "import sys; sys.path.append('.'); from check_ollama import check_ollama; sys.exit(0 if check_ollama('%OLLAMA_HOST%') else 1)" 2>nul
) else (
    echo Testing connection to: http://localhost:11434 (default)
    python -c "import sys; sys.path.append('.'); from check_ollama import check_ollama; sys.exit(0 if check_ollama() else 1)" 2>nul
)

if errorlevel 1 (
    echo.
    echo ERROR: Cannot connect to Ollama API
    echo.
    echo Troubleshooting steps:
    echo   1. Make sure Ollama is running: ollama serve
    echo   2. Check if firewall is blocking port 11434
    echo   3. If Ollama is on another machine, set OLLAMA_HOST:
    echo      set OLLAMA_HOST=http://your-host:11434
    echo.
    echo For WSL users:
    echo   - Ollama on Windows might only accept localhost connections
    echo   - Try: set OLLAMA_HOST=http://localhost:11434
    echo.
    goto :end
)

:check_models
REM Try to list models using CLI (this will fail if service is not running)
echo.
echo Checking installed models...
ollama list >nul 2>&1
if errorlevel 1 (
    echo.
    echo WARNING: Cannot list models. Ollama service might not be running.
    echo To start Ollama: ollama serve
) else (
    echo.
    echo Installed models:
    ollama list
)

:end
echo.
pause