# Ollama

## What it is
Ollama allows you to get up and running with large language models locally. It provides a simple CLI and API for running models like **Llama 4**, **Mistral**, **DeepSeek-V4**, **Gemma 3**, and **Qwen 3.8** on your own hardware. As of **early January 2027**, it remains the premier choice for local inference, featuring full support for native tool-calling, multi-modal workloads, and the **FastMCP 3.1** / **MCP 3.1** Task Protocol.

## What problem it solves
It simplifies the complex setup usually required for running LLMs, handling model weights, configurations, and hardware acceleration (GPU/NPU) automatically. It enables private, offline AI interactions without relying on cloud providers.

## Where it fits in the stack
**Local Inference Engine**. It acts as the execution layer for models on your own hardware, serving as a backend for various WebUIs and agents.

## Typical use cases
- **Private Chat**: Interacting with LLMs without data leaving your local network.
- **Development & Testing**: Locally testing AI-integrated applications before deploying to cloud providers.
- **Autonomous Agents**: Serving as the local backend for agents like OpenHands and Roo Code.
- **Enterprise Prototyping**: Rapidly deploying specialized models for internal document analysis or coding assistance.
- **Codex App Integration**: Utilizing native local AI workflows and browser-integrated AI experiences.

## Strengths
- **Ease of Use**: One-line installation and simple model pulling (e.g., `ollama run llama4`).
- **Hardware Acceleration**: Automatic detection and utilization of NVIDIA RTX 50/40 series, AMD ROCm, Apple Silicon M-series, and NPU accelerators.
- **Large Model Library**: Easy access to Llama 4, Mistral, DeepSeek-V4, Qwen 3.8, and Gemma 3.
- **Zero Cost**: No per-token pricing; limited only by your hardware.
- **High Performance**:
    - **Apple M4 Pro / M5**: Llama 4 8B at ~75-85 t/s (Unified memory).
    - **NVIDIA RTX 4070 / 5070**: Llama 4 8B at ~95 t/s (FP16 inference).
    - **NVIDIA RTX 5090 / 4090**: Llama 4 32B at ~45 t/s (4-bit quantization).

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
    image: ollama/ollama:latest # v0.28+ (January 2027)
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

### Recommended Models (Early 2027)

| Category | Model | VRAM Required | Note |
| :--- | :--- | :--- | :--- |
| **All-Rounder** | `llama4:32b` | ~20GB | Superior balance of speed and intelligence. |
| **Reasoning & Code** | `deepseek-v4:local` | ~16GB | Optimized for local complex logic and refactoring tasks. |
| **Edge/Mobile** | `phi4:3b` / `qwen3.8:4b` | ~2.5GB | High performance on minimal hardware. |
| **Gemma** | `gemma3:8b` | ~6GB | State-of-the-art open model from Google. |

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

### Python: FastMCP 3.1 Inference & GPU Monitor with Pydantic v2
This production-grade script allows agents and developers to programmatically execute local prompts on Ollama while monitoring GPU/VRAM statistics. Inputs are strictly validated with Pydantic v2.

```python
import requests
import json
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("OllamaModelMonitor")

class OllamaQuerySchema(BaseModel):
    model_name: str = Field(default="llama4", description="The registered local model identifier to run")
    prompt: str = Field(description="The instructional query or context prompt")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Creativity temperature rating")

@mcp.tool()
def execute_local_inference(query_json: str) -> str:
    """
    Dispatches a synchronous generation request to the local Ollama daemon,
    verifying inputs via Pydantic v2 schemas and returning structural metrics.
    """
    try:
        data = json.loads(query_json)
        validated = OllamaQuerySchema(**data)

        url = "http://localhost:11434/api/generate"
        payload = {
            "model": validated.model_name,
            "prompt": validated.prompt,
            "options": {
                "temperature": validated.temperature
            },
            "stream": False
        }

        response = requests.post(url, json=payload, timeout=30)
        if response.status_code != 200:
            return json.dumps({"status": "error", "message": f"Ollama daemon returned status {response.status_code}"})

        result = response.json()
        return json.dumps({
            "status": "success",
            "model": validated.model_name,
            "response": result.get("response"),
            "eval_count": result.get("eval_count"),
            "total_duration_ms": result.get("total_duration", 0) // 1000000
        }, indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [Open WebUI](open-webui.md) — The recommended web frontend for Ollama.
- [LiteLLM](litellm.md) — For load balancing multiple Ollama instances and fallback to Claude 5.6 or GPT-5.6.
- [Local LLMs](../tools/ai_knowledge/local_llms.md) — Overview of the local model ecosystem.
- [TrueNAS SCALE](../architecture/infrastructure.md) — For hosting Ollama with GPU passthrough.
- [Docker](../tools/infrastructure/docker.md) — Containerization for Ollama.
- [Portracker](portracker.md) — For monitoring Ollama's API port (11434).
- [Nextcloud](nextcloud.md) — For integrating local AI models into the Nextcloud Assistant.
- [Model Context Protocol](https://modelcontextprotocol.io/) — For adding tools to Ollama-backed agents.
- [LM Studio](https://lmstudio.ai/) — Desktop alternative for GUI-based model experimentation.

## Sources / References
- [Ollama Official Website](https://ollama.com/)
- [Ollama GitHub](https://github.com/ollama/ollama)
- [Ollama Release Notes](https://github.com/ollama/ollama/releases)
- [Local Model Leaderboard](https://huggingface.co/spaces/lmsys/chatbot-arena-leaderboard)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
