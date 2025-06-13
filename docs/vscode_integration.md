# VSCode Integration Guide

## Overview

Integrate the Workshop Assistant MCP Server with VSCode for seamless local LLM assistance during development.

## Integration Methods

### Method 1: Continue Extension (Recommended)

The Continue extension provides the most mature MCP integration for VSCode.

#### Installation
1. Install Continue extension from VSCode marketplace
2. Open Continue configuration (Ctrl/Cmd + Shift + P → "Continue: Open Config")

#### Configuration

**Option A: Stdio Transport (Default)**
Add to your Continue config file (`~/.continue/config.json`):

```json
{
  "models": [
    {
      "title": "Local Ollama Models",
      "provider": "mcp",
      "model": "workshop-assistant",
      "serverConfig": {
        "command": "python",
        "args": ["/absolute/path/to/workshop-assistant/server.py"],
        "env": {}
      }
    }
  ]
}
```

**Option B: TCP Transport**
First start the server on TCP:
```bash
python server.py --port 8080
```

Then configure Continue:
```json
{
  "models": [
    {
      "title": "Local Ollama Models",
      "provider": "mcp",
      "model": "workshop-assistant",
      "serverConfig": {
        "transport": "tcp",
        "host": "localhost",
        "port": 8080
      }
    }
  ]
}
```

#### Usage
- **Chat**: Use Continue sidebar to chat with local models
- **Code Generation**: Highlight code and use Continue commands
- **Autocomplete**: Get suggestions as you type

### Method 2: Claude Code CLI in Terminal

Use Claude Code CLI directly within VSCode's integrated terminal.

#### Setup

**Option A: Stdio Transport**
```bash
# Configure MCP
mkdir -p ~/.config/claude-code
cat > ~/.config/claude-code/mcp.json << EOF
{
  "mcpServers": {
    "ollama-workshop-assistant": {
      "command": "python",
      "args": ["/absolute/path/to/workshop-assistant/server.py"],
      "env": {}
    }
  }
}
EOF

# Set environment variable
echo 'export CLAUDE_MCP_CONFIG=~/.config/claude-code/mcp.json' >> ~/.bashrc
source ~/.bashrc
```

**Option B: TCP Transport**
```bash
# Start server on TCP port
python server.py --port 8080 &

# Configure MCP for TCP
mkdir -p ~/.config/claude-code
cat > ~/.config/claude-code/mcp.json << EOF
{
  "mcpServers": {
    "ollama-workshop-assistant": {
      "transport": "tcp",
      "host": "localhost",
      "port": 8080
    }
  }
}
EOF

# Set environment variable
echo 'export CLAUDE_MCP_CONFIG=~/.config/claude-code/mcp.json' >> ~/.bashrc
source ~/.bashrc
```

#### Usage in VSCode Terminal
```bash
# Start Claude Code with MCP support
claude-code

# Now you can use Ollama models through Claude Code
# Example: "Use the local codellama model to implement this function"
```

### Method 3: Custom VSCode Extension

For advanced users who want deep integration.

#### Create Extension Skeleton
```bash
npm install -g yo generator-code
yo code  # Choose "New Extension (TypeScript)"
cd your-extension-name
```

#### Add MCP Dependencies
```json
// package.json
{
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.0.0",
    "vscode": "^1.74.0"
  }
}
```

#### Basic Extension Code
```typescript
// src/extension.ts
import * as vscode from 'vscode';
import { Client } from '@modelcontextprotocol/sdk/client/index.js';

export function activate(context: vscode.ExtensionContext) {
    // Initialize MCP client
    const client = new Client({
        name: "vscode-ollama-assistant",
        version: "1.0.0"
    });

    // Register commands
    const disposable = vscode.commands.registerCommand('ollama-assistant.chat', async () => {
        const input = await vscode.window.showInputBox({
            prompt: 'Enter your prompt for Ollama'
        });
        
        if (input) {
            // Call MCP server
            const result = await client.callTool('chat_with_model', {
                model_name: 'codellama:7b',
                prompt: input
            });
            
            // Show result
            vscode.window.showInformationMessage(result.response);
        }
    });

    context.subscriptions.push(disposable);
}
```

## Workflow Examples

### Code Generation Workflow

1. **Highlight code block** in VSCode
2. **Right-click** → "Continue: Edit with AI" (if using Continue)
3. **Specify task**: "Refactor this function to be more efficient"
4. **Model selection**: Continue automatically uses local Ollama model
5. **Review changes** in Continue's diff view

### Code Review Workflow

1. **Open Pull Request** in VSCode (GitHub PR extension)
2. **Terminal**: `claude-code` 
3. **Command**: "Review this PR using local models for syntax and architecture analysis"
4. **Claude Code**: Uses MCP to delegate specific review tasks to appropriate models
5. **Results**: Comprehensive review combining multiple model outputs

### Debugging Workflow

1. **Paste error message** in Continue chat
2. **Ask**: "Use the local debugging model to analyze this error"
3. **Continue**: Automatically routes to appropriate Ollama model
4. **Get**: Detailed analysis and fix suggestions
5. **Apply**: Suggested fixes directly in editor

## Server Startup Options

The MCP server supports both stdio and TCP transports:

```bash
# Default: stdio transport (for direct MCP client connections)
python server.py

# TCP transport: specify port
python server.py --port 8080

# TCP transport: specify host and port
python server.py --port 3000 --host 0.0.0.0

# Get help
python server.py --help
```

**Transport Comparison:**
- **Stdio**: Direct process communication, lower latency, auto-managed lifecycle
- **TCP**: Network-based, can be shared across applications, persistent server

## Configuration Tips

### Performance Optimization

```json
// Continue config optimizations
{
  "mcp": {
    "timeout": 300000,  // 5 minutes for large models
    "retries": 3,
    "cacheEnabled": true
  }
}
```

### Model Selection Strategy

```json
// Route different tasks to different models
{
  "models": [
    {
      "title": "Fast Code Gen",
      "provider": "mcp",
      "model": "codellama:7b",
      "description": "Quick code generation and simple fixes"
    },
    {
      "title": "Code Review", 
      "provider": "mcp",
      "model": "codellama:13b",
      "description": "Thorough code analysis and architecture review"
    }
  ]
}
```

### Workspace-Specific Settings

Create `.vscode/settings.json` in your project:

```json
{
  "continue.mcp.enabled": true,
  "continue.defaultModel": "ollama-workshop-assistant",
  "continue.contextLength": 8192
}
```

## Troubleshooting

### Common Issues

1. **MCP Server Not Found**
   ```bash
   # Verify server path is absolute
   which python  # Use full path
   ls /absolute/path/to/workshop-assistant/server.py  # Verify exists
   ```

2. **Permission Errors**
   ```bash
   # Make server executable
   chmod +x /path/to/workshop-assistant/server.py
   ```

3. **Ollama Not Running**
   ```bash
   # Check Ollama status
   curl http://localhost:11434/api/tags
   
   # Start if needed
   ollama serve
   ```

4. **Models Not Available**
   ```bash
   # Download required models
   ollama pull codellama:7b
   ollama pull llama3:8b
   ```

### Debug Mode

Enable verbose logging in Continue:

```json
{
  "logging": {
    "level": "debug",
    "file": "~/.continue/logs/debug.log"
  }
}
```

Monitor MCP communication:
```bash
# Watch server logs
python server.py --verbose

# Monitor Ollama
ollama logs
```

## Best Practices

1. **Start Small**: Begin with 7B models for testing
2. **Monitor Resources**: Use `ollama ps` to track memory usage
3. **Cache Models**: Keep frequently used models loaded
4. **Keyboard Shortcuts**: Set up VSCode shortcuts for common Continue commands
5. **Context Management**: Keep relevant files open for better AI context
6. **Model Switching**: Use different models for different task types

## Advanced Features

### Custom Prompts

Create workspace-specific prompts:

```json
// .vscode/continue/prompts.json
{
  "code-review": {
    "prompt": "Review this code for bugs, performance issues, and adherence to our team's coding standards",
    "model": "codellama:13b"
  },
  "unit-tests": {
    "prompt": "Generate comprehensive unit tests for this function",
    "model": "codellama:7b"
  }
}
```

### Team Configuration

Share MCP configuration across team:

```bash
# Add to project repository
mkdir .vscode
cat > .vscode/mcp-config.json << EOF
{
  "mcpServers": {
    "team-ollama-assistant": {
      "command": "python",
      "args": ["./tools/ollama-mcp-server/server.py"],
      "env": {}
    }
  }
}
EOF
```