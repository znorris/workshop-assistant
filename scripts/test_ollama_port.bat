@echo off
echo === Quick Ollama Port Test ===
echo.

REM Default to localhost if OLLAMA_HOST not set
if defined OLLAMA_HOST (
    echo Testing: %OLLAMA_HOST%
    REM Extract host and port from OLLAMA_HOST
    for /f "tokens=2,3 delims=:/" %%a in ("%OLLAMA_HOST%") do (
        set HOST=%%a
        set PORT=%%b
    )
) else (
    echo Testing: http://localhost:11434 (default)
    set HOST=localhost
    set PORT=11434
)

echo.
echo Attempting to connect to %HOST%:%PORT%...
echo.

REM Use PowerShell for TCP connection test
powershell -Command "try { $tcp = New-Object System.Net.Sockets.TcpClient('%HOST%', %PORT%); if ($tcp.Connected) { Write-Host 'SUCCESS: Port %PORT% is open on %HOST%' -ForegroundColor Green; $tcp.Close(); exit 0 } } catch { Write-Host 'ERROR: Cannot connect to %HOST%:%PORT%' -ForegroundColor Red; Write-Host 'Make sure Ollama is running: ollama serve' -ForegroundColor Yellow; exit 1 }"

if errorlevel 1 (
    echo.
    echo Additional checks to try:
    echo   1. netstat -an ^| findstr :11434
    echo   2. Check Windows Firewall settings
    echo   3. Try: telnet %HOST% %PORT%
)

echo.
pause