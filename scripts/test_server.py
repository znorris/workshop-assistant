#!/usr/bin/env python3
"""Test script for the Workshop Assistant MCP Server."""

import json
import sys
import os

# Add parent directory to path to import server
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import mcp, get_ollama_models, get_ollama_base_url, list_available_models, chat_with_model

def test_connection():
    """Test connection to Ollama."""
    print(f"Testing connection to Ollama at: {get_ollama_base_url()}")
    models = get_ollama_models()
    if models:
        print(f"✓ Successfully connected! Found {len(models)} models:")
        for model in models[:3]:  # Show first 3 models
            print(f"  - {model['name']}")
        if len(models) > 3:
            print(f"  ... and {len(models) - 3} more")
    else:
        print("✗ Could not connect to Ollama. Please ensure:")
        print("  1. Ollama is installed")
        print("  2. Ollama service is running (ollama serve)")
        print("  3. If in WSL, Ollama is accessible from Windows host")
        return False
    return True

def test_list_models():
    """Test the list_available_models tool."""
    print("\nTesting list_available_models tool...")
    try:
        result = list_available_models()
        print(f"✓ Tool executed successfully!")
        print(f"  - Total models: {result['total_models']}")
        print(f"  - System specs: CPU={result['system_specs']['cpu_count']}, RAM={result['system_specs']['memory_gb']}GB")
        if result['models']:
            print(f"  - First model: {result['models'][0]['name']} ({result['models'][0]['size_gb']}GB)")
    except Exception as e:
        print(f"✗ Tool failed: {e}")
        return False
    return True

def test_chat():
    """Test the chat_with_model tool."""
    print("\nTesting chat_with_model tool...")
    
    # Get first available model
    models = get_ollama_models()
    if not models:
        print("✗ No models available for testing")
        return False
    
    model_name = models[0]['name']
    print(f"  Using model: {model_name}")
    
    try:
        result = chat_with_model(
            model_name=model_name,
            prompt="Hello! Please respond with a simple greeting.",
            system_prompt="You are a helpful assistant. Keep responses very brief."
        )
        
        if result['success']:
            print(f"✓ Chat successful!")
            print(f"  - Response: {result['response'][:100]}...")
            print(f"  - Eval count: {result['eval_count']} tokens")
        else:
            print(f"✗ Chat failed: {result.get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"✗ Tool failed: {e}")
        return False
    return True

def main():
    """Run all tests."""
    print("=== Workshop Assistant MCP Server Test ===\n")
    
    tests = [
        ("Connection", test_connection),
        ("List Models", test_list_models),
        ("Chat", test_chat)
    ]
    
    results = []
    for name, test_func in tests:
        if not results or results[-1]:  # Skip if previous test failed
            results.append(test_func())
        else:
            print(f"\nSkipping {name} test due to previous failure")
            results.append(False)
    
    print("\n=== Test Summary ===")
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✓ All tests passed! The MCP server is ready to use.")
    else:
        print("\n✗ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()