# Workshop Assistant MCP Server

A Model Context Protocol (MCP) server that integrates with Ollama to provide local LLM capabilities to Claude and other MCP-compatible clients.

## Overview

This MCP server acts as a bridge between Claude and your local Ollama installation. It exposes Ollama's models as tools that Claude can use to delegate specific tasks to appropriate local models.

**Architecture:**
```
Claude (via Claude Desktop/CLI) <--> MCP Server (this project) <--> Ollama <--> Local LLMs
```

The MCP server provides two main tools to Claude:
- **list_available_models**: Discover what models Ollama has installed
- **chat_with_model**: Send prompts to specific Ollama models and get responses

## Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai/download) installed and running
- At least one Ollama model downloaded

## Ollama Setup

### 1. Install Ollama

Download and install from [ollama.ai/download](https://ollama.ai/download)

**Linux/WSL:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**macOS:**
```bash
brew install ollama
```

**Windows:**
Download the installer from the website.

**Important for WSL Users:**
If running the MCP server in WSL while Ollama runs on Windows:
- Ollama on Windows may only accept localhost connections by default
- You may need to set `OLLAMA_HOST=http://localhost:11434` in WSL
- Or configure Ollama to accept connections from all interfaces

### 2. Start Ollama Service

```bash
# Start Ollama (runs on localhost:11434 by default)
ollama serve
```

### 3. Download Recommended Models

**For Code Tasks:**
```bash
# Fast code generation (3.8GB)
ollama pull codellama:7b

# Better code quality (7.3GB) 
ollama pull codellama:13b

# Efficient coding model (3.8GB)
ollama pull deepseek-coder:6.7b
```

**For General Tasks:**
```bash
# Fast general model (4.7GB)
ollama pull llama3:8b

# High-quality reasoning (requires 40GB+ VRAM)
ollama pull llama3:70b
```

### 4. Verify Installation

**Linux/macOS/WSL:**
```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# Test a model
ollama run codellama:7b "Write a hello world function in Python"
```

**Windows (Command Prompt):**
```cmd
REM Check Ollama is installed
where ollama

REM Check Ollama is running (after installation)
ollama list

REM Test a model
ollama run codellama:7b "Write a hello world function in Python"
```

### 5. Hardware Acceleration Configuration

#### GPU Acceleration (Recommended)

**NVIDIA GPU:**
```bash
# Ollama automatically detects CUDA
# Ensure NVIDIA drivers and CUDA are installed
nvidia-smi  # Verify GPU is detected
```

**AMD GPU:**
```bash
# Use ROCm-enabled Ollama
docker run -d --device /dev/kfd --device /dev/dri -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama:rocm
```

**Apple Silicon:**
- Metal acceleration is automatic - no configuration needed

#### CPU-Only Mode

Force CPU-only execution (useful for testing or when GPU is unavailable):

```bash
# Force CPU-only mode
export CUDA_VISIBLE_DEVICES=-1
ollama serve

# Alternative: Use CPU-optimized models
ollama pull steamdj/llama3.1-cpu-only
```

#### NPU Support (Currently Limited)

**Status:** NPU support is not yet available in Ollama
- **Intel NPU**: Feature request open, no current support
- **AMD Ryzen NPU**: Feature request open, no current support
- **Workaround**: Use CPU or GPU acceleration instead

**Performance Environment Variables:**
```bash
# Memory optimization
export OLLAMA_FLASH_ATTENTION=1        # Reduce memory usage
export OLLAMA_KEEP_ALIVE=5m           # Keep models loaded longer
export OLLAMA_MAX_LOADED_MODELS=2     # Limit concurrent models

# CPU optimization
export OLLAMA_NUM_PARALLEL=1          # Reduce parallel requests for CPU
export OLLAMA_MAX_QUEUE=10            # Adjust request queue size

# Start Ollama with settings
ollama serve
```

## MCP Server Installation

### Option 1: Windows Installation

1. Clone the repository:
```cmd
git clone <repository-url>
cd workshop-assistant
```

2. Set up the MCP server:
```cmd
setup_windows.bat
```

3. (In a separate terminal) Check Ollama:
```cmd
REM Option 1: Batch file (basic check)
check_ollama.bat

REM Option 2: PowerShell (detailed network diagnostics)
powershell -ExecutionPolicy Bypass -File check_ollama.ps1
```

4. Test the MCP server:
```cmd
test_windows.bat
```

5. Run the MCP server:
```cmd
run_server.bat
```

### Option 2: Linux/macOS/WSL Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd workshop-assistant
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Verify Ollama connection:
```bash
curl http://localhost:11434/api/tags
```

5. Test the server:
```bash
python test_server.py
```

### Environment Configuration

If Ollama is running on a different host or port:
```bash
# Linux/macOS/WSL
export OLLAMA_HOST=http://your-ollama-host:11434

# Windows
set OLLAMA_HOST=http://your-ollama-host:11434

# WSL connecting to Windows Ollama (common setup)
export OLLAMA_HOST=http://$(ip route show | grep -i default | awk '{ print $3}'):11434
```

**Note for WSL Users:** If running the MCP server in WSL while Ollama runs on Windows, see `docs/WSL_TROUBLESHOOTING.md` for detailed setup instructions including firewall configuration and port forwarding.

## Usage

### Prerequisites

1. **Ollama Service**: Must be running separately
   - Windows: `ollama serve`
   - Linux/macOS: `ollama serve`
   - The service runs on `http://localhost:11434` by default

2. **Ollama Models**: At least one model must be installed
   - Check installed models: `ollama list`
   - Install a model: `ollama pull codellama:7b`

### Starting the MCP Server

**Windows:**
```cmd
run_server.bat
```

**Linux/macOS/WSL:**
```bash
source venv/bin/activate  # or your virtual environment
python server.py
```

The MCP server will connect to Ollama and expose tools to Claude.

### Integration Options

#### Claude Desktop Integration

1. Open Claude Desktop configuration file:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

2. Add the server configuration:
```json
{
  "mcpServers": {
    "workshop-assistant": {
      "command": "python",
      "args": ["/absolute/path/to/workshop-assistant/server.py"],
      "env": {}
    }
  }
}
```

3. Restart Claude Desktop

#### Claude Code CLI Integration

**Option 1: Add Server via CLI (Recommended)**

```bash
# Add the MCP server to Claude Code
# This configures Claude to start our Python MCP server when needed
claude mcp add ollama-workshop /absolute/path/to/workshop-assistant/server.py

# If using virtual environment, specify the venv's Python interpreter
claude mcp add ollama-workshop /path/to/venv/bin/python /absolute/path/to/workshop-assistant/server.py

# Add with environment variables (e.g., for WSL users where Ollama runs on Windows)
# The MCP server will use OLLAMA_HOST to find Ollama
claude mcp add ollama-workshop /path/to/python /path/to/server.py -e OLLAMA_HOST=http://172.23.240.1:11434

# List configured MCP servers
claude mcp list

# Get details about our MCP server
claude mcp get ollama-workshop
```

**Option 2: Project Configuration (.mcp.json)**

Create a `.mcp.json` file in your project root:
```json
{
  "mcpServers": {
    "ollama-workshop": {
      "command": "python",
      "args": ["/absolute/path/to/workshop-assistant/server.py"],
      "env": {
        "OLLAMA_HOST": "http://localhost:11434"
      }
    }
  }
}
```

**Option 3: Import from Claude Desktop**

If you've already configured the server in Claude Desktop:
```bash
# Import servers from Claude Desktop
claude mcp import-from-desktop
```

**Server Scopes:**
- `local` (default): Project-specific user settings
- `project`: Shared via `.mcp.json` file
- `user`: Available across all projects

```bash
# Add server globally (user scope)
claude mcp add ollama-workshop /path/to/server.py --scope user

# Add to project (creates .mcp.json)
claude mcp add ollama-workshop /path/to/server.py --scope project
```

#### VSCode Integration

**Option 1: Continue Extension (Recommended)**
1. Install the Continue extension from VSCode marketplace
2. Configure Continue to use MCP servers:
```json
// settings.json or Continue config
{
  "continue.mcp": {
    "servers": {
      "workshop-assistant": {
        "command": "python",
        "args": ["/absolute/path/to/workshop-assistant/server.py"]
      }
    }
  }
}
```

**Option 2: Direct Integration (Advanced)**
Create a VSCode extension that connects to the MCP server:
```bash
# Generate extension template
npm install -g yo generator-code
yo code

# Add MCP client dependencies to package.json
npm install @modelcontextprotocol/sdk
```

**Option 3: Terminal Integration**
Use Claude Code CLI within VSCode terminal:
```bash
# In VSCode terminal
export CLAUDE_MCP_CONFIG=~/.config/claude-code/mcp.json
claude-code
```

### Quick Start with Claude Code CLI

```bash
# 1. Install the MCP server (if not already done)
git clone <repository-url>
cd workshop-assistant
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Add the MCP server to Claude Code (adjust paths as needed)
# This tells Claude Code how to start our MCP server
claude mcp add ollama-workshop $(which python) $(pwd)/server.py

# 3. For WSL users (if Ollama is running on Windows)
# The MCP server needs to know where Ollama is
claude mcp add ollama-workshop $(which python) $(pwd)/server.py \
  -e OLLAMA_HOST="http://$(ip route show | grep -i default | awk '{ print $3}'):11434"

# 4. Verify the MCP server is configured
claude mcp list
claude mcp get ollama-workshop

# 5. Start using Claude Code
# Claude will now have access to the MCP tools:
# - list_available_models() - See what Ollama models are available
# - chat_with_model() - Send prompts to specific Ollama models
```

### Available Tools

#### `list_available_models()`
Returns all available Ollama models with their specifications and recommended use cases.

**Response:**
```json
{
  "models": [
    {
      "name": "codellama:7b",
      "size_gb": 3.8,
      "recommended_uses": ["code generation", "code analysis", "fast generation"],
      "memory_requirement_gb": 4.56
    }
  ],
  "system_specs": {
    "cpu_count": 8,
    "memory_gb": 32.0,
    "gpu_available": true
  },
  "total_models": 1
}
```

#### `chat_with_model(model_name, prompt, system_prompt="")`
Send a chat message to a specific Ollama model.

**Parameters:**
- `model_name`: Name of the Ollama model to use
- `prompt`: The user message to send
- `system_prompt`: Optional system prompt to set context

**Response:**
```json
{
  "success": true,
  "model": "codellama:7b",
  "response": "Generated response from the model",
  "total_duration": 1500000000,
  "load_duration": 100000000,
  "prompt_eval_count": 25,
  "eval_count": 150
}
```

## Development

### Project Structure

```
workshop-assistant/
├── server.py              # Main MCP server implementation
├── requirements.txt       # Python dependencies
├── setup.py              # Installation and setup script
├── claude_config.json    # Claude Desktop configuration template
├── docs/                 # Documentation files
│   ├── DEVELOPMENT_PLAN.md   # Development progress tracking
│   └── ...              # Other documentation
├── scripts/             # Setup and utility scripts
└── README.md            # This file
```

### Testing

Start the server in development mode:

```bash
python server.py
```

Test with MCP client or use the development tools provided by the MCP Python SDK.

### Model Performance Guide

**Hardware Requirements:**
- **8GB RAM**: Can run 7b models comfortably
- **16GB RAM**: Can run 13b models
- **32GB+ RAM**: Can run larger models like 70b (CPU only)
- **8GB+ VRAM**: GPU acceleration for faster inference
- **24GB+ VRAM**: Can run 70b models on GPU

**Model Selection:**
```bash
# Minimum setup (recommended starting point)
ollama pull codellama:7b    # 3.8GB - Fast code generation
ollama pull llama3:8b       # 4.7GB - General tasks

# Enhanced setup (if you have 16GB+ RAM)
ollama pull codellama:13b   # 7.3GB - Higher quality code
ollama pull deepseek-coder:6.7b  # 3.8GB - Efficient coding

# Power user setup (32GB+ RAM or 24GB+ VRAM)  
ollama pull llama3:70b      # 40GB - Best reasoning quality
```

**Performance Tips:**
- **GPU vs CPU**: GPU acceleration provides 5-10x speed improvement
- **CPU Performance**: Expect ~10 tokens/second on powerful CPUs (i7+ with 32GB RAM)
- **Memory Caching**: Models load faster on subsequent runs (cached in memory)
- **Model Size**: For CPU-only, stick to 7B models unless you have 32GB+ RAM
- **Context Management**: Larger context windows prevent slow reprocessing
- **Monitoring**: Use `ollama ps` to see running models and memory usage

**CPU-Only Performance Expectations:**
- **7B models**: Usable performance (~10 tokens/sec on good hardware)
- **13B models**: Requires 16GB+ RAM, slower generation
- **70B models**: Requires 32GB+ RAM, very slow (CPU only)
- **Startup Time**: Initial model load can take 30+ seconds on CPU

## Workflow Examples

### Example: Test-Driven Development

**Orchestrator Prompt:**
```
You have access to local Ollama models through MCP tools. Use them to accelerate development.

Available approach:
1. Write unit tests yourself (you're best at understanding requirements)
2. Delegate implementation to appropriate local model
3. Iterate until tests pass

Task: Create a Python class for managing a shopping cart with add/remove/total functionality.
```

**Workflow:**
1. **Claude** writes comprehensive unit tests
2. **Claude** calls `list_available_models()` to assess options
3. **Claude** calls `chat_with_model("codellama:7b", "Implement this ShoppingCart class to pass these tests: [test code]")`
4. **Local model** generates implementation
5. **Claude** runs tests, identifies failures
6. **Claude** iterates with local model until all tests pass

### Example: Code Review Pipeline

**Orchestrator Prompt:**
```
Review this pull request using local models for different aspects:
- Use fast model for syntax/style checks
- Use larger model for architecture review
- Generate summary and recommendations
```

**Workflow:**
1. **Claude** calls `chat_with_model("codellama:7b", "Check this code for syntax errors and style issues: [code]")`
2. **Claude** calls `chat_with_model("llama3:70b", "Provide architectural review of this implementation: [code]")`
3. **Claude** synthesizes feedback into comprehensive review

### Task Delegation Strategy

- **Code Generation**: `codellama:7b/13b` for speed vs quality trade-off
- **Code Review**: `llama3:70b` for thorough analysis
- **Documentation**: `llama3:8b` for balanced speed/quality
- **Refactoring**: `codellama:13b` for code understanding
- **Bug Analysis**: Larger models for complex debugging

## Troubleshooting

### Common Issues

1. **Ollama not found**: Ensure Ollama is installed and running on port 11434
2. **Model not available**: Download required models with `ollama pull`
3. **Memory issues**: Monitor system memory and adjust model selection
4. **Connection refused**: Check firewall settings and Ollama service status

### Debugging

Enable verbose logging by modifying `server.py` to include debug output:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Additional Documentation

This repository includes several specialized guides for advanced usage:

### Performance & Optimization
- **[WORKSHOP_ASSISTANT_ANALYSIS.md](docs/WORKSHOP_ASSISTANT_ANALYSIS.md)** - Comprehensive technical analysis with performance benchmarks, system prompt testing results, and detailed usage insights from systematic testing
- **[OPTIMIZATION_GUIDE.md](docs/OPTIMIZATION_GUIDE.md)** - Practical guide with performance-tested prompts, workflows, and quick reference for maximizing workshop-assistant effectiveness

### Setup & Integration
- **[hardware_optimization.md](docs/hardware_optimization.md)** - Hardware acceleration setup for NVIDIA (CUDA), AMD (ROCm), Apple Silicon (Metal), and CPU optimization
- **[vscode_integration.md](docs/vscode_integration.md)** - VSCode integration methods including Continue extension setup and Claude Code CLI integration
- **[WSL_TROUBLESHOOTING.md](docs/WSL_TROUBLESHOOTING.md)** - Windows Subsystem for Linux networking configuration and troubleshooting

### Development
- **[orchestrator_prompts.md](docs/orchestrator_prompts.md)** - Example system prompts and workflow patterns for Claude Desktop integration
- **[DEVELOPMENT_PLAN.md](docs/DEVELOPMENT_PLAN.md)** - Project development history, completed tasks, and testing results

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes following the existing code style
4. Update `DEVELOPMENT_PLAN.md` with progress
5. Submit a pull request

## License

MIT License - see LICENSE file for details