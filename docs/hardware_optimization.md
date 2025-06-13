# Hardware Optimization Guide for Ollama

## Current Hardware Support Status

### ✅ Fully Supported
- **NVIDIA GPUs**: CUDA acceleration (automatic)
- **AMD GPUs**: ROCm acceleration (requires Docker container)
- **Apple Silicon**: Metal acceleration (automatic)
- **CPU**: All x86_64 and ARM64 processors

### ⚠️ Limited/Experimental Support
- **Intel Arc GPUs**: Community solutions available (IPEX-LLM)
- **Intel iGPUs**: Not officially supported by Ollama

### ❌ Not Yet Supported
- **Intel NPUs**: Feature request open ([#5747](https://github.com/ollama/ollama/issues/5747))
- **AMD Ryzen NPUs**: Feature request open ([#5186](https://github.com/ollama/ollama/issues/5186))

## Configuration by Hardware Type

### NVIDIA GPU Setup
```bash
# Verify CUDA installation
nvidia-smi

# Ollama automatically detects and uses NVIDIA GPUs
ollama serve
```

### AMD GPU Setup (Linux/Windows)
```bash
# Use ROCm container
docker run -d \
  --device /dev/kfd \
  --device /dev/dri \
  -v ollama:/root/.ollama \
  -p 11434:11434 \
  --name ollama \
  ollama/ollama:rocm

# Alternative: Install ROCm drivers and use native Ollama
```

### Intel Arc GPU (Community Solution)
```bash
# Install IPEX-LLM for Intel GPU acceleration
pip install ipex-llm[xpu]

# Configure environment
export USE_XETLA=OFF
export SYCL_PI_LEVEL_ZERO_USE_IMMEDIATE_COMMANDLISTS=1

# Note: Requires manual configuration, not plug-and-play
```

### CPU-Only Optimization
```bash
# Force CPU-only mode
export CUDA_VISIBLE_DEVICES=-1

# Performance optimization
export OLLAMA_FLASH_ATTENTION=1
export OLLAMA_NUM_PARALLEL=1
export OLLAMA_KEEP_ALIVE=10m

# Use CPU-optimized models when available
ollama pull steamdj/llama3.1-cpu-only
```

## Performance Optimization by Hardware

### High-End GPU (24GB+ VRAM)
```bash
# Optimal settings for large GPU
export OLLAMA_MAX_LOADED_MODELS=3
export OLLAMA_NUM_PARALLEL=4
export OLLAMA_KEEP_ALIVE=1h

# Can run large models efficiently
ollama pull llama3:70b
ollama pull codellama:34b
```

### Mid-Range GPU (8-16GB VRAM)
```bash
# Balanced settings
export OLLAMA_MAX_LOADED_MODELS=2
export OLLAMA_NUM_PARALLEL=2
export OLLAMA_KEEP_ALIVE=30m

# Stick to medium models
ollama pull codellama:13b
ollama pull llama3:8b
```

### CPU-Only (32GB+ RAM)
```bash
# Conservative settings for CPU
export OLLAMA_MAX_LOADED_MODELS=1
export OLLAMA_NUM_PARALLEL=1
export OLLAMA_KEEP_ALIVE=5m
export OLLAMA_FLASH_ATTENTION=1

# Use smaller models
ollama pull codellama:7b
ollama pull llama3:8b
```

### CPU-Only (16GB RAM)
```bash
# Minimal settings
export OLLAMA_MAX_LOADED_MODELS=1
export OLLAMA_NUM_PARALLEL=1
export OLLAMA_KEEP_ALIVE=2m

# Only small models
ollama pull codellama:7b
```

## NPU Future Considerations

While NPUs aren't supported yet, they represent the future of efficient AI computation:

### NPU Advantages (When Available)
- **Power Efficiency**: 10-100x more efficient than CPU for AI tasks
- **Always-On**: Low power consumption for continuous AI workloads
- **Parallel Processing**: Specialized for transformer architectures
- **Local Processing**: No cloud dependency

### Current Workarounds
1. **Intel NPU Users**: Use CPU mode with optimized settings
2. **AMD Ryzen NPU Users**: Use integrated GPU if available, otherwise CPU
3. **Monitor Issues**: Track GitHub issues for NPU support updates

### Preparing for NPU Support
```bash
# When NPU support arrives, likely configuration:
# export OLLAMA_DEVICE=npu
# export OLLAMA_NPU_DEVICE=0
# ollama serve
```

## Monitoring and Troubleshooting

### Check Current Hardware Usage
```bash
# See loaded models and memory usage
ollama ps

# Monitor GPU usage (NVIDIA)
nvidia-smi -l 1

# Monitor CPU usage
htop

# Monitor AMD GPU usage
radeontop
```

### Performance Benchmarking
```bash
# Time model responses
time ollama run codellama:7b "Write a hello world function"

# Monitor token generation speed
ollama run --verbose codellama:7b "Explain sorting algorithms"
```

### Common Issues
1. **Out of Memory**: Reduce model size or increase swap
2. **Slow Performance**: Check if GPU acceleration is working
3. **Model Loading Errors**: Verify sufficient RAM/VRAM
4. **Connection Issues**: Check firewall and port accessibility

## Hardware Recommendations

### For Development Workflows
- **Minimum**: 16GB RAM, modern CPU, 7B models
- **Recommended**: 16GB RAM + 8GB VRAM GPU, 7B-13B models  
- **Optimal**: 32GB RAM + 16GB VRAM GPU, all model sizes

### For Production Use
- **Small Team**: 32GB RAM + RTX 4090 (24GB VRAM)
- **Large Team**: Multiple GPUs or cloud GPU instances
- **Enterprise**: Dedicated GPU servers with 40GB+ VRAM cards