# Ollama

## What it is
Ollama allows you to get up and running with large language models locally. It provides a simple CLI and API for running models like Llama 4, Mistral, and others on your own hardware. As of **June 2026**, Ollama v0.25+ features native support for the **Model Context Protocol (MCP 3.0)** and multi-modal reasoning chains.

## What problem it solves
It simplifies the complex setup usually required for running LLMs, handling model weights, configurations, and hardware acceleration (GPU) automatically. It enables private, offline AI interactions without relying on cloud providers, ensuring data sovereignty for individuals and enterprises.

## Where it fits in the stack
**Local Inference Engine**. It acts as the execution layer for models on your own hardware, serving as a backend for various WebUIs, agents, and IDE extensions like **Cline** and **Roo Code**.

## Typical use cases
- **Private Chat**: Interacting with LLMs without data leaving your local network.
- **Development & Testing**: Locally testing AI-integrated applications before deploying to cloud providers.
- **Autonomous Agents**: Serving as the local backend for agents like Aider or OpenHands.
- **Enterprise Prototyping**: Rapidly deploying specialized models for internal document analysis or coding assistance.
- **Agentic Workflows**: Executing complex multi-step reasoning tasks via **Claude 4.8 Opus** orchestration.

## Strengths
- **Ease of Use**: One-line installation and simple model pulling (e.g., `ollama run llama4`).
- **Hardware Acceleration**: Automatic detection and utilization of NVIDIA, AMD, and Apple Silicon GPUs.
- **Large Model Library**: Easy access to Llama 4, Mistral, Qwen 3, and many more.
- **Zero Cost**: No per-token pricing; limited only by your hardware.
- **MCP 3.0 Native**: (v0.25+) Can act as both an MCP client and server for unified tool access.

## Limitations
- **Hardware Dependent**: Performance is strictly tied to local CPU/GPU/RAM.
- **Memory Requirements**: Larger models require significant VRAM (e.g., 70B+ models).

## When to use it
- For maximum privacy and data sovereignty.
- To eliminate per-token costs during development and testing.
- When working in offline or low-connectivity environments.
- As a local development backend for agentic frameworks.

## When not to use it
- If you lack dedicated GPU hardware and require low-latency responses for large models.
- For massive models (e.g., 400B+) that exceed consumer hardware capacity.
- If you require managed scaling and high availability without managing infrastructure.

## Licensing and cost
- **Open Source**: Yes (MIT License)
- **Cost**: Free
- **Self-hostable**: Yes

## Getting started

### Installation (Docker)
```yaml
services:
  ollama:
    volumes:
      - ./ollama:/root/.ollama
    container_name: ollama
    pull_policy: always
    tty: true
    restart: unless-stopped
    image: ollama/ollama:latest # v0.25+ (June 2026)
```

## Codex App & Tools
Ollama v0.24 introduced the **Codex App**, a native desktop experience for managing local AI workflows.
- **Launch**: Use `ollama launch codex-app` from the terminal.
- **Features**: Includes built-in browser support for loading local servers/sites directly within the AI interface and an MCP resource browser.

## Recommended Models (June 2026)
Avoid relying on the `:latest` tag. For June 2026, the following models are recommended:

| Category | Model | VRAM Required | Note |
| :--- | :--- | :--- | :--- |
| **All-Rounder** | `llama4:8b` | ~6GB | Industry standard for local intelligence. |
| **Pro Reasoning** | `qwen3:30b` | ~24GB | Best balance of speed and complex logic. |
| **Edge / Mobile** | `gemma4:2b` | ~1.6GB | Minimal RAM requirements, perfect for low-power. |
| **Coding** | `codestral:22b` | ~16GB | Optimized for development and logic tasks. |

## CLI examples

```bash
# Pull and run a model
ollama run llama4

# List all local models
ollama list

# Create a model from a Modelfile
ollama create my-model -f Modelfile

# Launch the Codex App (v0.24+)
ollama launch codex-app
```

## API examples

### Python (Standard)
```python
import requests

url = "http://localhost:11434/api/generate"
data = {
    "model": "llama4",
    "prompt": "Explain Quantum Entanglement."
}

response = requests.post(url, json=data)
print(response.json())
```

### Python (LiteLLM Wrapper)
Recommended for multi-model orchestration with **Claude 4.8 Opus**.
```python
import litellm

response = litellm.completion(
    model="ollama/llama4",
    messages=[{"role": "user", "content": "Write a python script to sort a list."}],
    api_base="http://localhost:11434"
)
print(response.choices[0].message.content)
```

## TrueNAS SCALE & GPU Setup
Running Ollama on [TrueNAS SCALE](../architecture/infrastructure.md) requires configuring GPU passthrough for optimal performance.

### GPU Passthrough (NVIDIA)
1. **Host Configuration**: Ensure the NVIDIA driver is active in TrueNAS SCALE (**System Settings > Advanced > Isolated GPU Device**).
2. **Docker/App Configuration**: In the application settings, allocate `1` (or more) GPU under the "Resource Reservation" section.
3. **Environment**: Ensure `NVIDIA_VISIBLE_DEVICES=all` and `NVIDIA_DRIVER_CAPABILITIES=compute,utility` are set in the container environment.

## Related tools / concepts
- [Open WebUI](open-webui.md) — The recommended web frontend for Ollama.
- [LiteLLM](litellm.md) — For load balancing multiple Ollama instances.
- [Local LLMs](../tools/ai_knowledge/local_llms.md) — Overview of the local model ecosystem.
- [LM Studio](https://lmstudio.ai/) — A desktop-first alternative for model experimentation.
- [Cline](../tools/agents/cline.md) — IDE agent that utilizes Ollama as a local backend.
- [Roo Code](../tools/agents/roo-code.md) — Advanced coding agent with Ollama support.
- [MCP 3.0](../knowledge_base/patterns/tool-calling-and-mcp.md) — Unified protocol for tool access in Ollama.

## Backlog
- [x] Perform quarterly technical freshness audit (June 2026).

## Sources / References
- [Ollama Official Website](https://ollama.com/)
- [Ollama GitHub Repository](https://github.com/ollama/ollama)
- [Ollama Releases & Changelog](https://github.com/ollama/ollama/releases)
- [Best Local Models 2026 Guide](https://aiopsschool.com/blog/the-best-ollama-models-in-2026-which-model-should-you-run-on-your-hardware/)

## Contribution Metadata
- Last reviewed: 2026-06-18
- Confidence: high
