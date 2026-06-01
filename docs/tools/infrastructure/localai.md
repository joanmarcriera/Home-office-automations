# LocalAI

## What it is
LocalAI is a self-hosted, OpenAI-compatible inference platform for running local models without depending on proprietary cloud APIs. It acts as a multi-modal proxy that can serve LLMs, image generation, audio-to-text, and text-to-audio.

## What problem it solves
It gives teams a local or self-hosted way to serve models behind a familiar API surface, which reduces vendor dependence and ensures data privacy. It unifies disparate local inference backends (llama.cpp, diffusers, whisper.cpp) under a single, standard API.

## Where it fits in the stack
**Infrastructure / Local Inference Platform**. It is the primary serving layer for private model access, sitting between your hardware and your agentic applications.

## Typical use cases
- **Privacy-First AI APIs**: Serving models to internal applications where data must remain on-premise.
- **Hybrid Cloud/Local Stacks**: Using LocalAI as a fallback or for low-risk tasks alongside cloud providers.
- **Multi-Modal Agents**: Powering agents that need vision, speech, and text capabilities from a single endpoint.
- **Homelab Automation**: Integrating LLMs into [Home Assistant](../../services/home-assistant.md) or [n8n](../../services/n8n.md) workflows locally.

## Strengths
- **Standardized API**: Drop-in replacement for OpenAI, making it easy to use with any existing SDK or tool.
- **Multi-Backend Support**: Can run GGUF, EXL2, Diffusers, and more.
- **Hardware Agnostic**: Supports CPU-only, NVIDIA CUDA, Intel OneAPI, and AMD ROCm.
- **Feature Rich**: Supports image generation (Stable Diffusion), speech (Whisper/Piper), and vector embeddings.

## Limitations
- **Complexity**: Can be more difficult to configure than [Ollama](../../services/ollama.md) due to its extensive feature set and manual model management options.
- **Resource Intensive**: Multi-modal "All-In-One" (AIO) images are very large and require significant RAM/VRAM.

## When to use it
- When you need a single API for multiple types of AI tasks (text, image, audio).
- When data locality, cost control, or self-hosting is a requirement.
- When you want to use existing OpenAI-native tools with local models.

## When not to use it
- When you only need simple text inference (Ollama may be simpler).
- When you are not prepared to manage model files and configuration YAMLs.

## Getting started

### 1. Docker Compose Setup (Recommended)
Create a `docker-compose.yml` to run LocalAI with CUDA support:

```yaml
services:
  local-ai:
    image: localai/localai:latest-aio-gpu-nvidia-cuda-12
    container_name: local-ai
    ports:
      - 8080:8080
    environment:
      - DEBUG=true
      - MODELS_PATH=/models
    volumes:
      - ./models:/models
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

### 2. Hardware Acceleration
- **NVIDIA**: Set `image` to a `-cuda` variant and ensure `nvidia-container-toolkit` is installed.
- **Intel**: Use `-openvino` or `-oneapi` variants.
- **CPU Only**: Use `-cpu` variants.

## CLI examples

### List Available Models
```bash
curl http://localhost:8080/v1/models
```

### Image Generation (Stable Diffusion)
```bash
curl http://localhost:8080/v1/images/generations \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A futuristic city in the style of cyberpunk",
    "size": "512x512"
  }'
```

### Audio Transcription (Whisper)
```bash
curl http://localhost:8080/v1/audio/transcriptions \
  -H "Content-Type: multipart/form-data" \
  -F file="@audio.mp3" \
  -F model="whisper-1"
```

## API examples

### Python (OpenAI SDK)
LocalAI is a drop-in replacement for OpenAI's API.

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="sk-no-key-required"
)

response = client.chat.completions.create(
    model="gpt-4", # Or your local model name
    messages=[{"role": "user", "content": "Explain RAG in one sentence."}]
)

print(response.choices[0].message.content)
```

## Related tools / concepts
- [Ollama](../../services/ollama.md)
- [LM Studio](../ai_knowledge/lm-studio.md)
- [llmfit](../development_ops/llmfit.md)
- [llama.cpp](llama-cpp.md)
- [vLLM](vllm.md)
- [LiteLLM](../../services/litellm.md)
- [Home Assistant](../../services/home-assistant.md)
- [n8n](../../services/n8n.md)
- [Open WebUI](../../services/open-webui.md)
- [Model Serving Patterns](../../knowledge_base/patterns/model_routing_guide.md)

## Sources / References
- [LocalAI Documentation](https://localai.io/)
- [LocalAI GitHub Repository](https://github.com/mudler/LocalAI)
- [Model Gallery](https://localai.io/models/)

## Contribution Metadata
- Last reviewed: 2026-06-01
- Confidence: high
