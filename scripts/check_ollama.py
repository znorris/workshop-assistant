#!/usr/bin/env python3
"""Simple script to check Ollama connectivity."""

import sys
import json

try:
    import requests
except ImportError:
    print("ERROR: requests module not installed")
    print("Run: pip install requests")
    sys.exit(1)

def check_ollama(url="http://localhost:11434"):
    """Check if Ollama is accessible."""
    try:
        response = requests.get(f"{url}/api/tags", timeout=2)
        if response.status_code == 200:
            data = response.json()
            models = data.get("models", [])
            print(f"SUCCESS: Ollama is running at {url}")
            print(f"Found {len(models)} models installed")
            if models:
                print("\nAvailable models:")
                for model in models[:5]:  # Show first 5
                    print(f"  - {model['name']}")
                if len(models) > 5:
                    print(f"  ... and {len(models) - 5} more")
            return True
        else:
            print(f"ERROR: Ollama returned status code {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"ERROR: Cannot connect to Ollama at {url}")
        print("Please ensure Ollama is running (ollama serve)")
        return False
    except requests.exceptions.Timeout:
        print(f"ERROR: Connection to Ollama timed out")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    import os
    url = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    success = check_ollama(url)
    sys.exit(0 if success else 1)