# LocalAI

## What it is
LocalAI is a self-hosted, OpenAI-compatible inference platform for running local models without depending on proprietary cloud APIs. It acts as a multi-modal proxy that can serve LLMs, image generation, audio-to-text, and text-to-audio. In January 2027, it has expanded to support [FastMCP 3.1 Task Protocol](../../knowledge_base/patterns/tool-calling-and-mcp.md) natively, enabling local frontier models (like Gemma 4, DeepSeek-V4, Qwen 3.6 VL) to call tools natively and interact with stateful servers.

## What problem it solves
It gives teams a local or self-hosted way to serve models behind a familiar API surface, which reduces vendor dependence and ensures data privacy. It unifies disparate local inference backends (llama.cpp, diffusers, whisper.cpp) under a single, standard API, solving the fragmentation problem in the local AI ecosystem.

## Where it fits in the stack
**Infrastructure / Local Inference Platform**. It is the primary serving layer for private model access, sitting between your hardware and your agentic applications (like [Claude Code](../development_ops/claude-code.md) or [Windsurf](../development_ops/codeium.md)).

## Typical use cases
- **Privacy-First AI APIs**: Serving models to internal applications where data must remain on-premise.
- **Hybrid Cloud/Local Stacks**: Using LocalAI as a fallback or for low-risk tasks alongside cloud providers like [OpenRouter](../ai_knowledge/openrouter.md).
- **Multi-Modal Agents**: Powering agents that need vision, speech, and text capabilities from a single endpoint.
- **Homelab Automation**: Integrating LLMs into [Home Assistant](../../services/home-assistant.md) or [n8n](../../services/n8n.md) workflows locally.

## Strengths
- **Standardized API**: Drop-in replacement for OpenAI, making it easy to use with any existing SDK or tool.
- **Multi-Backend Support**: Can run GGUF, EXL3, Diffusers, and more.
- **Hardware Agnostic**: Supports CPU-only, NVIDIA CUDA 12.8, Intel OneAPI, and AMD ROCm 6.3.
- **Feature Rich**: Supports image generation (Stable Diffusion), speech (Whisper/Piper), and vector embeddings out of the box.
- **Agentic Ready**: Native tool-calling support and [FastMCP 3.1 Task Protocol](../../knowledge_base/patterns/tool-calling-and-mcp.md) integration, including secure sandboxed tool execution.

## Limitations
- **Complexity**: Can be more difficult to configure than [Ollama](../../services/ollama.md) due to its extensive feature set and manual model management options.
- **Resource Intensive**: Multi-modal "All-In-One" (AIO) images are very large (40GB+) and require significant RAM/VRAM.
- **Update Frequency**: The rapid evolution of backends sometimes leads to temporary incompatibilities with the latest GGUF versions.

## When to use it
- When you need a single API for multiple types of AI tasks (text, image, audio).
- When data locality, cost control, or self-hosting is a requirement for enterprise compliance.
- When you want to use existing OpenAI-native tools with local models.

## When not to use it
- When you only need simple text inference (Ollama may be simpler).
- When you are not prepared to manage model files and configuration YAMLs for fine-grained control.

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
      - MCP_SERVERS_CONFIG=/models/mcp_servers.json
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

### 2. Model Installation
LocalAI can automatically download models via the API or by placing YAML files in the `/models` directory.
```bash
# Download a model via API
curl http://localhost:8080/models/apply -H "Content-Type: application/json" -d '{
  "id": "gemma-4-9b-instruct"
}'
```

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
### Python with Tool-calling and FastMCP 3.1 Task Protocol
LocalAI is a drop-in replacement for OpenAI's API, and natively handles tool extraction and execution behind the scenes when connected to a FastMCP server. Here is an example leveraging Pydantic v2 schemas:

```python
import os
from openai import OpenAI
from pydantic import BaseModel, Field

client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="sk-no-key-required"
)

# Define a structured tool schema using Pydantic v2
class FileListRequest(BaseModel):
    path: str = Field(default=".", description="The repository path to list files from")

# Call completion with local tools managed by LocalAI
response = client.chat.completions.create(
    model="gemma-4-9b-instruct",
    messages=[{"role": "user", "content": "What files are in the repository?"}],
    tools=[
        {
            "type": "function",
            "function": {
                "name": "list_files",
                "description": "Lists all files in the current repository path",
                "parameters": FileListRequest.model_json_schema()
            }
        }
    ]
)

print(response.choices[0].message.tool_calls)
```

## Related tools / concepts
- [Ollama](../../services/ollama.md)
- [LM Studio](lm-studio.md)
- [llmfit](../development_ops/llmfit.md)
- [llama.cpp](llama-cpp.md)
- [vLLM](vllm.md)
- [LiteLLM](../../services/litellm.md)
- [Home Assistant](../../services/home-assistant.md)
- [n8n](../../services/n8n.md)
- [Open WebUI](../../services/open-webui.md)
- [Model Serving Patterns](../../knowledge_base/model_routing_guide.md)
- [FastMCP 3.1 Task Protocol](../../knowledge_base/patterns/tool-calling-and-mcp.md)

## Sources / References
- [LocalAI Documentation](https://localai.io/)
- [LocalAI GitHub Repository](https://github.com/mudler/LocalAI)
- [Model Gallery](https://localai.io/models/)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
