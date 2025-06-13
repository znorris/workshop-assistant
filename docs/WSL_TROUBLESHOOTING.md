# WSL to Windows Ollama Connection Troubleshooting

## Common Issues and Solutions

### 1. Connection Timeout from WSL to Windows Ollama

If you're getting connection timeouts when trying to access Ollama running on Windows from WSL, try these solutions:

#### Solution A: Windows Firewall Configuration

1. **Allow Ollama through Windows Firewall:**
   - Open Windows Defender Firewall with Advanced Security
   - Create a new Inbound Rule:
     - Rule Type: Port
     - Protocol: TCP
     - Specific local ports: 11434
     - Action: Allow the connection
     - Profile: All (Domain, Private, Public)
     - Name: "Ollama API"

2. **Alternative: Allow the Ollama executable:**
   - Create an Inbound Rule for Program
   - Browse to Ollama executable (usually `C:\Users\<username>\AppData\Local\Ollama\ollama.exe`)
   - Allow all connections

#### Solution B: Configure Ollama to Listen on All Interfaces

1. **Set Ollama to listen on 0.0.0.0:**
   ```cmd
   set OLLAMA_HOST=0.0.0.0
   ollama serve
   ```

2. **Or use a config file:** Create `%USERPROFILE%\.ollama\config.json`:
   ```json
   {
     "host": "0.0.0.0"
   }
   ```

#### Solution C: Use Port Forwarding

1. **From Windows (PowerShell as Administrator):**
   ```powershell
   netsh interface portproxy add v4tov4 listenport=11434 listenaddress=0.0.0.0 connectport=11434 connectaddress=127.0.0.1
   ```

2. **To remove the port forwarding:**
   ```powershell
   netsh interface portproxy delete v4tov4 listenport=11434 listenaddress=0.0.0.0
   ```

### 2. Finding the Correct Windows Host IP

The Windows host IP from WSL can be found using:

```bash
# Microsoft recommended method for WSL2
ip route show | grep -i default | awk '{ print $3}'

# Alternative methods:
cat /etc/resolv.conf | grep nameserver | awk '{print $2}'

# Get WSL network info
hostname -I
```

### 3. Testing Connectivity

#### From WSL:
```bash
# Test if port is open
nc -zv $(ip route show | grep -i default | awk '{ print $3}') 11434

# Test with curl
curl -m 5 http://$(ip route show | grep -i default | awk '{ print $3}'):11434/api/tags

# Test with telnet
telnet $(ip route show | grep -i default | awk '{ print $3}') 11434
```

#### From Windows:
```powershell
# Test if Ollama is listening
netstat -an | findstr :11434

# Test API endpoint
Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -UseBasicParsing
```

### 4. Environment Variable Configuration

Set the `OLLAMA_HOST` environment variable in WSL:

```bash
# Temporary (current session)
export OLLAMA_HOST=http://$(ip route show | grep -i default | awk '{ print $3}'):11434

# Permanent (add to ~/.bashrc or ~/.zshrc)
echo 'export OLLAMA_HOST=http://$(ip route show | grep -i default | awk '{ print $3}'):11434' >> ~/.bashrc
```

### 5. Alternative: Run Ollama in WSL

If Windows firewall issues persist, consider running Ollama directly in WSL:

```bash
# Install Ollama in WSL
curl -fsSL https://ollama.ai/install.sh | sh

# Run Ollama in WSL
ollama serve

# Use localhost in MCP server
export OLLAMA_HOST=http://localhost:11434
```

### 6. Debugging Network Issues

1. **Check WSL version:**
   ```bash
   wsl --version
   ```

2. **Check WSL network mode:**
   ```powershell
   # From Windows PowerShell
   Get-Content "$env:USERPROFILE\.wslconfig"
   ```

3. **Check if WSL is using NAT or bridged mode:**
   - NAT mode (default): WSL has its own IP subnet
   - Bridged mode: WSL shares the host network

### 7. Known Issues

- **WSL1 vs WSL2:** WSL1 uses the same network as Windows (localhost works), WSL2 has its own network (requires host IP)
- **VPN Software:** Some VPN software can interfere with WSL networking
- **Docker Desktop:** Can change WSL network configuration
- **Windows Updates:** May reset firewall rules

### 8. Quick Test Script

Save as `test_ollama_wsl.sh`:

```bash
#!/bin/bash
echo "Testing Ollama connectivity from WSL..."

# Get Windows host IP
HOST_IP=$(ip route show | grep -i default | awk '{ print $3}')
echo "Windows host IP: $HOST_IP"

# Test connection
if curl -s -m 5 "http://$HOST_IP:11434/api/tags" > /dev/null 2>&1; then
    echo "✓ Successfully connected to Ollama!"
    echo "Set: export OLLAMA_HOST=http://$HOST_IP:11434"
else
    echo "✗ Cannot connect to Ollama on Windows"
    echo "Please check Windows Firewall and Ollama configuration"
fi
```

## Recommended Setup

For the most reliable WSL to Windows Ollama connection:

1. Configure Ollama to listen on `0.0.0.0`
2. Add Windows Firewall rule for port 11434
3. Set `OLLAMA_HOST` environment variable in WSL
4. Test with `check_ollama.py` script

If issues persist, running Ollama directly in WSL is often the simplest solution.