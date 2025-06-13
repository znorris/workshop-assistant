# Ollama Connection Checker for PowerShell
Write-Host "=== Checking Ollama Installation and Connection ===" -ForegroundColor Cyan
Write-Host ""

# Check if Ollama is installed
$ollamaPath = Get-Command ollama -ErrorAction SilentlyContinue
if (-not $ollamaPath) {
    Write-Host "ERROR: Ollama is not installed or not in PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "To install Ollama:"
    Write-Host "  1. Visit https://ollama.ai/download"
    Write-Host "  2. Download and install Ollama for Windows"
    Write-Host "  3. Restart PowerShell after installation"
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Ollama found at:" -ForegroundColor Green
Write-Host "  $($ollamaPath.Path)"
Write-Host ""

# Determine Ollama host
$ollamaHost = if ($env:OLLAMA_HOST) { $env:OLLAMA_HOST } else { "http://localhost:11434" }
Write-Host "Testing connection to: $ollamaHost" -ForegroundColor Yellow

# Test network connectivity to Ollama API
try {
    $response = Invoke-WebRequest -Uri "$ollamaHost/api/tags" -Method Get -TimeoutSec 5 -ErrorAction Stop
    $models = ($response.Content | ConvertFrom-Json).models
    
    Write-Host "SUCCESS: Connected to Ollama API!" -ForegroundColor Green
    Write-Host ""
    
    if ($models.Count -eq 0) {
        Write-Host "WARNING: No models installed" -ForegroundColor Yellow
        Write-Host "Install a model with: ollama pull codellama:7b"
    } else {
        Write-Host "Found $($models.Count) installed models:" -ForegroundColor Green
        foreach ($model in $models) {
            $sizeGB = [math]::Round($model.size / 1GB, 2)
            Write-Host "  - $($model.name) (${sizeGB}GB)"
        }
    }
} catch {
    Write-Host "ERROR: Cannot connect to Ollama API at $ollamaHost" -ForegroundColor Red
    Write-Host ""
    Write-Host "Error details: $_" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Troubleshooting steps:" -ForegroundColor Yellow
    Write-Host "  1. Make sure Ollama is running: ollama serve"
    Write-Host "  2. Check if Windows Firewall is blocking port 11434"
    Write-Host "  3. For remote Ollama, set OLLAMA_HOST environment variable:"
    Write-Host "     `$env:OLLAMA_HOST = 'http://your-host:11434'"
    Write-Host ""
    Write-Host "For WSL users:" -ForegroundColor Yellow
    Write-Host "  - Ollama on Windows might only accept localhost connections"
    Write-Host "  - Try: `$env:OLLAMA_HOST = 'http://localhost:11434'"
    
    # Additional network diagnostics
    Write-Host ""
    Write-Host "Network diagnostics:" -ForegroundColor Yellow
    
    # Extract host and port from URL
    if ($ollamaHost -match 'http://([^:]+):(\d+)') {
        $host = $matches[1]
        $port = $matches[2]
        
        # Test if port is open
        try {
            $tcpClient = New-Object System.Net.Sockets.TcpClient
            $tcpClient.Connect($host, $port)
            if ($tcpClient.Connected) {
                Write-Host "  - Port $port is open on $host" -ForegroundColor Green
                Write-Host "  - Service might be running but not responding to API calls"
                $tcpClient.Close()
            }
        } catch {
            Write-Host "  - Port $port is not reachable on $host" -ForegroundColor Red
            Write-Host "  - Ollama service is likely not running"
        }
    }
}

Write-Host ""
Read-Host "Press Enter to exit"