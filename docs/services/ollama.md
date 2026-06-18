# Ollama

## What it is
Ollama allows you to get up and running with large language models locally. It provides a simple CLI and API for running models like Llama 4, Mistral, and the O4 reasoning series on your own hardware.

## What problem it solves
It simplifies the complex setup usually required for running LLMs, handling model weights, configurations, and hardware acceleration (GPU) automatically. It enables private, offline AI interactions without relying on cloud providers.

## Where it fits in the stack
**Local Inference Engine**. It acts as the execution layer for models on your own hardware, serving as a backend for various WebUIs and agents.

## Typical use cases
- **Private Chat**: Interacting with LLMs without data leaving your local network.
- **Development & Testing**: Locally testing AI-integrated applications before deploying to cloud providers.
- **Autonomous Agents**: Serving as the local backend for agents like Aider or OpenHands.
- **Enterprise Prototyping**: Rapidly deploying specialized models for internal document analysis or coding assistance.
- **Codex App Integration**: Utilizing the native Codex App (v0.25+) for managed local AI workflows and browser-integrated AI experiences.

## Strengths
- **Ease of Use**: One-line installation and simple model pulling (e.g., `ollama run llama4`).
- **Hardware Acceleration**: Automatic detection and utilization of NVIDIA, AMD, and Apple Silicon GPUs.
- **Large Model Library**: Easy access to Llama 4, Mistral, Phi-4, and O4 reasoning models.
- **Zero Cost**: No per-token pricing; limited only by your hardware.

## Limitations
- **Hardware Dependent**: Performance is strictly tied to local CPU/GPU/RAM.
- **Memory Requirements**: Larger models (70B+) require significant VRAM (24GB+ for 4-bit quantization).

## When to use it
- For maximum privacy and data sovereignty.
- To eliminate per-token costs during development.
- When working in offline or low-connectivity environments.

## When not to use it
- If you lack dedicated GPU hardware and require low-latency responses for large models.
- For massive models that exceed consumer hardware capacity without extensive quantization.

## Getting started

### Installation (Docker)
```yaml
services:
  ollama:
    image: ollama/ollama:latest # v0.25+ (June 2026)
    container_name: ollama
    volumes:
      - ./ollama:/root/.ollama
    restart: unless-stopped
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

### Recommended Models (June 2026)

| Category | Model | VRAM Required | Note |
| :--- | :--- | :--- | :--- |
| **All-Rounder** | `llama4:32b` | ~20GB | Superior balance of speed and intelligence. |
| **Reasoning** | `o4-mini:local` | ~12GB | Optimized for local complex logic tasks. |
| **Edge/Mobile** | `phi4:3b` | ~2.5GB | High performance on minimal hardware. |

## CLI examples
The `ollama` CLI is the primary tool for model management.

```bash
# Pull and run a model
ollama run llama4

# List locally available models
ollama list

# Create a model from a Modelfile
ollama create my-custom-model -f Modelfile

# Remove a model
ollama rm gemma2
```

## API examples
Ollama provides an OpenAI-compatible API on port `11434`.

### Generate a Response (Curl)
```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama4",
  "prompt": "Explain Quantum Entanglement in one sentence."
}'
```

### Chat Completion (Python)
```python
import requests

def get_chat_response(prompt):
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": "llama4",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }
    response = requests.post(url, json=payload)
    return response.json()["message"]["content"]

print(get_chat_response("Hello, Ollama!"))
```

## Performance Benchmarking (June 2026)

| Hardware | Model | Eval Rate (t/s) | Note |
| :--- | :--- | :--- | :--- |
| **Apple M4 Pro** | Llama 4 8B | ~65 t/s | Unified memory performance. |
| **NVIDIA RTX 4070** | Llama 4 8B | ~85 t/s | FP16 inference. |
| **NVIDIA RTX 4090** | Llama 4 32B | ~35 t/s | 4-bit quantization. |

## Related tools / concepts
- [Open WebUI](open-webui.md) — The recommended web frontend for Ollama.
- [LiteLLM](litellm.md) — For load balancing multiple Ollama instances and fallback to Claude 4.8 Opus.
- [Local LLMs](../tools/ai_knowledge/local_llms.md) — Overview of the local model ecosystem.
- [Model Context Protocol](https://modelcontextprotocol.io/) — For adding tools to Ollama-backed agents.
- [TrueNAS SCALE](../architecture/infrastructure.md) — For hosting Ollama with GPU passthrough.
- [LM Studio](https://lmstudio.ai/) — Desktop alternative for GUI-based model experimentation.
- [Aider](https://aider.chat/) — AI pair programming tool that can use Ollama as a backend.

## Sources / References
- [Ollama Official Website](https://ollama.com/)
- [Ollama GitHub](https://github.com/ollama/ollama)
- [Ollama v0.25 Release Notes](https://github.com/ollama/ollama/releases)
- [Local Model Leaderboard (June 2026)](https://huggingface.co/spaces/lmsys/chatbot-arena-leaderboard)

## Contribution Metadata
- Last reviewed: 2026-06-19
- Confidence: high
