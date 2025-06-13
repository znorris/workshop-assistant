#!/usr/bin/env python3

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e.stderr}")
        return None

def check_ollama():
    """Check if Ollama is running."""
    result = run_command("curl -s http://localhost:11434/api/tags", "Checking Ollama connection")
    return result is not None

def install_dependencies():
    """Install Python dependencies."""
    return run_command("pip install -r requirements.txt", "Installing Python dependencies")

def main():
    print("Setting up Workshop Assistant MCP Server...")
    
    # Install dependencies
    if not install_dependencies():
        print("Failed to install dependencies. Exiting.")
        sys.exit(1)
    
    # Check Ollama
    if not check_ollama():
        print("\nWarning: Ollama is not running or not accessible at localhost:11434")
        print("Please ensure Ollama is installed and running before using the MCP server.")
        print("Install Ollama: https://ollama.ai/download")
    else:
        print("✓ Ollama is running and accessible")
    
    print("\nSetup complete!")
    print("\nTo start the MCP server:")
    print("  python server.py")
    print("\nTo install in Claude Desktop, add this to your config:")
    print("  See claude_config.json for configuration details")

if __name__ == "__main__":
    main()