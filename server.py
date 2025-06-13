#!/usr/bin/env python3

import os
import subprocess
import requests
import psutil
import logging
import argparse
from typing import List, Dict, Any
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

mcp = FastMCP("Workshop Assistant")


def get_ollama_base_url() -> str:
    """Get the appropriate Ollama base URL based on the environment."""
    # Check environment variable first
    env_url = os.environ.get('OLLAMA_HOST')
    if env_url:
        logger.info(f"Using OLLAMA_HOST from environment: {env_url}")
        return env_url
    
    # First try localhost
    localhost_url = "http://localhost:11434"
    try:
        response = requests.get(f"{localhost_url}/api/tags", timeout=1)
        if response.status_code == 200:
            logger.info(f"Connected to Ollama at {localhost_url}")
            return localhost_url
    except requests.exceptions.RequestException:
        logger.debug(f"Could not connect to {localhost_url}")
    
    # Check if running in WSL
    if os.path.exists("/proc/version"):
        with open("/proc/version", "r") as f:
            if "microsoft" in f.read().lower():
                # Running in WSL, get Windows host IP
                try:
                    # Use the Microsoft documented method for WSL2
                    result = subprocess.run(
                        ["sh", "-c", "ip route show | grep -i default | awk '{ print $3}'"],
                        capture_output=True,
                        text=True
                    )
                    if result.returncode == 0 and result.stdout.strip():
                        host_ip = result.stdout.strip()
                        wsl_url = f"http://{host_ip}:11434"
                        # Test if it works
                        try:
                            response = requests.get(f"{wsl_url}/api/tags", timeout=1)
                            if response.status_code == 200:
                                logger.info(f"Connected to Ollama at {wsl_url} (WSL host)")
                                return wsl_url
                        except requests.exceptions.RequestException:
                            logger.debug(f"Could not connect to {wsl_url}")
                except Exception:
                    pass
    
    # Default to localhost
    logger.warning("Could not connect to Ollama. Using default URL. Set OLLAMA_HOST environment variable if needed.")
    return "http://localhost:11434"


OLLAMA_BASE_URL = get_ollama_base_url()


def get_ollama_models() -> List[Dict[str, Any]]:
    """Get available models from Ollama API."""
    try:
        logger.debug(f"Fetching models from {OLLAMA_BASE_URL}/api/tags")
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        response.raise_for_status()
        models = response.json().get("models", [])
        
        enriched_models = []
        for model in models:
            model_info = {
                "name": model["name"],
                "size": model.get("size", 0),
                "modified_at": model.get("modified_at", ""),
                "digest": model.get("digest", ""),
                "details": model.get("details", {}),
            }
            enriched_models.append(model_info)
        
        logger.info(f"Found {len(enriched_models)} Ollama models")
        return enriched_models
    except requests.exceptions.RequestException as e:
        logger.error(f"Could not connect to Ollama at {OLLAMA_BASE_URL}: {e}")
        return []


def get_system_specs() -> Dict[str, Any]:
    """Get system hardware specifications."""
    return {
        "cpu_count": psutil.cpu_count(),
        "memory_gb": round(psutil.virtual_memory().total / (1024**3), 2),
        "gpu_available": check_gpu_availability(),
    }


def check_gpu_availability() -> bool:
    """Check if GPU is available for Ollama."""
    try:
        import subprocess
        result = subprocess.run(["nvidia-smi"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


@mcp.tool()
def list_available_models() -> Dict[str, Any]:
    """List all available Ollama models with their specifications and recommended use cases."""
    logger.info("Listing available models")
    models = get_ollama_models()
    system_specs = get_system_specs()
    
    model_recommendations = []
    for model in models:
        name = model["name"]
        size_gb = round(model["size"] / (1024**3), 2)
        
        # Add use case recommendations based on model name patterns
        recommendations = []
        if "code" in name.lower():
            recommendations.append("code generation")
            recommendations.append("code analysis")
        if "instruct" in name.lower():
            recommendations.append("instruction following")
            recommendations.append("task completion")
        if any(x in name.lower() for x in ["7b", "8b"]):
            recommendations.append("fast generation")
        if any(x in name.lower() for x in ["13b", "34b", "70b"]):
            recommendations.append("complex reasoning")
        
        model_info = {
            "name": name,
            "size_gb": size_gb,
            "recommended_uses": recommendations if recommendations else ["general chat"],
            "memory_requirement_gb": size_gb * 1.2,  # Rough estimate
        }
        model_recommendations.append(model_info)
    
    return {
        "models": model_recommendations,
        "system_specs": system_specs,
        "total_models": len(models),
    }


@mcp.tool()
def chat_with_model(model_name: str, prompt: str, system_prompt: str = "", verbose: bool = False) -> Dict[str, Any]:
    """Send a chat message to a specific Ollama model and return the response.
    
    Args:
        model_name: Name of the Ollama model to use
        prompt: The user prompt/message to send
        system_prompt: Optional system prompt to set context
        verbose: If True, return full JSON with metadata. If False, return only response text.
    """
    logger.info(f"Chat request to model '{model_name}' with prompt length: {len(prompt)}")
    try:
        payload = {
            "model": model_name,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }
        
        if system_prompt:
            payload["messages"].insert(0, {"role": "system", "content": system_prompt})
        
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json=payload,
            timeout=300
        )
        response.raise_for_status()
        
        result = response.json()
        response_content = result.get("message", {}).get("content", "")
        logger.info(f"Chat successful. Response length: {len(response_content)} chars")
        
        if verbose:
            return {
                "success": True,
                "model": model_name,
                "response": response_content,
                "total_duration": result.get("total_duration", 0),
                "load_duration": result.get("load_duration", 0),
                "prompt_eval_count": result.get("prompt_eval_count", 0),
                "eval_count": result.get("eval_count", 0),
            }
        else:
            return response_content
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Chat failed for model '{model_name}': {e}")
        return {
            "success": False,
            "error": f"Failed to communicate with Ollama: {str(e)}",
            "model": model_name,
            "ollama_url": OLLAMA_BASE_URL,
            "hint": "Ensure Ollama is running and accessible. You can set OLLAMA_HOST environment variable."
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Workshop Assistant MCP Server")
    parser.add_argument("--port", type=int, help="Run server on TCP port instead of stdio")
    parser.add_argument("--host", type=str, default="localhost", help="Host to bind to (default: localhost)")
    args = parser.parse_args()
    
    logger.info(f"Starting Workshop Assistant MCP Server")
    logger.info(f"Ollama URL: {OLLAMA_BASE_URL}")
    
    # Print server details
    logger.info(f"MCP Server Name: {mcp.name}")
    
    if args.port:
        logger.info(f"Server running on: TCP {args.host}:{args.port}")
        logger.info(f"Server ready with registered tools")
        mcp.run(transport="tcp", host=args.host, port=args.port)
    else:
        logger.info(f"Server running on: stdio transport")
        logger.info(f"Server ready with registered tools")
        mcp.run()