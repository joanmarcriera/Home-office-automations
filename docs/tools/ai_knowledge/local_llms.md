# Local LLMs (Ollama, MLX, llama.cpp)

## What it is
Tools and frameworks that allow running Large Language Models directly on your own hardware (Homelab, Workstation, Mac). As of May 2026, the local ecosystem is characterized by the rise of **Small Language Models (SLMs)** and **Local Multimodal** capabilities.

- **Ollama**: The industry standard for local LLM management with a simple CLI and API.
- **MLX**: Apple's high-performance AI framework optimized for Unified Memory on Apple Silicon.
- **llama.cpp**: The foundational C++ library enabling inference on almost any hardware via quantization.
- **LM Studio**: A premier GUI for discovering and running models with local server capabilities.

## What problem it solves
It provides **100% data sovereignty**, eliminates recurring token costs, and ensures availability during internet outages. It allows for the processing of sensitive personal or corporate data that cannot be sent to cloud providers due to privacy or compliance requirements.

## Where it fits in the stack
**LLM / Reasoning Engine (Self-hosted)**. It serves as the local intelligence layer in the [KnowledgeOps](../../architecture/README.md) stack, replacing or augmenting cloud providers like OpenAI or Anthropic.

## Architecture overview
Local inference relies on **Quantization** (typically GGUF or EXL2 formats) to compress model weights while maintaining performance.
- **CPU Inference**: Relies on system RAM and instruction sets (AVX, AMX).
- **GPU Inference**: Relies on VRAM and CUDA/ROCm/Metal kernels.
- **NPU Inference**: Leverages dedicated AI accelerators (Intel NPU, Qualcomm Hexagon, Apple Neural Engine).

## Typical use cases
- **Local Coding Assistance**: Running `Qwen-3.5-Coder` via [Continue](../development_ops/continue_dev.md) or `Aider`.
- **Private RAG**: Indexing personal documents into a local vector DB and querying them via `llama-3.2-3b-instruct`.
- **Local Vision Tasks**: Using `InternVL2` or `Llama-3.2-Vision` to describe local camera feeds or screenshots.
- **Agentic Pre-processing**: Using a small model (e.g., `Gemma-4-2b`) to classify and route tasks before escalating to a cloud model.
- **Offline Transcription**: Coordinating with [Whisper](../../services/whisper.md) for local voice-to-text workflows.

## Strengths
- **Privacy & Security**: No data ever leaves the local network boundary.
- **Cost Efficiency**: Zero cost per token; limited only by hardware power and initial cost.
- **Low Latency**: No network round-trips to remote data centers.
- **Infinite Customization**: Access to thousands of specialized fine-tunes on Hugging Face.

## Limitations
- **Reasoning Ceiling**: The largest local models (e.g., Llama-3-70B) still generally lag behind GPT-4o or Claude 3.5 Opus in complex reasoning.
- **Hardware Bottlenecks**: High-quality inference requires significant VRAM (24GB+) or Mac Unified Memory (64GB+).
- **Setup Complexity**: While Ollama is simple, optimizing performance for diverse hardware can be challenging.

## Recommended Models (May 2026)

| Category | Recommended Model | Notes |
| :--- | :--- | :--- |
| **All-rounder** | **Llama 3.2 (3B/8B/11B)** | Excellent balance of speed and reasoning; includes Vision. |
| **High Reasoning** | **Qwen 3.5 (72B)** | Competitive with top-tier cloud models for complex tasks. |
| **Small/Fast** | **Gemma 4 (2B)** | Perfect for mobile or edge devices; highly efficient. |
| **Coding** | **Qwen-3.5-Coder (32B)** | The current state-of-the-art for local coding assistance. |
| **Multimodal** | **InternVL2 (8B/26B)** | Superior performance for OCR and complex image analysis. |
| **Enterprise MoE** | **Nemotron-3 (120B)** | Massive Mixture-of-Experts model for diverse reasoning. |

## When to use it
- When processing PII (Personally Identifiable Information) or sensitive medical/legal data.
- For high-volume, low-complexity tasks (classification, formatting, summarization).
- When building "local-first" software that must work without an internet connection.
- For development and testing of agentic loops where API costs would be prohibitive.

## When not to use it
- When the highest possible reasoning performance is required for novel research or complex planning.
- If you lack a GPU with at least 8GB of VRAM or a Mac with 16GB+ of Unified Memory.
- When you need a massive context window (e.g., 2M tokens) that exceeds local RAM capacity.

## Getting started

### Ollama (The Standard)
1. **Install**: `curl -fsSL https://ollama.com/install.sh | sh`
2. **Run Model**: `ollama run llama3.2`
3. **API Access**: Ollama listens on `http://localhost:11434` with an OpenAI-compatible API.

### MLX (Apple Silicon)
1. **Install**: `pip install mlx-lm`
2. **Run Inference**:
```python
from mlx_lm import load, generate
model, tokenizer = load("mlx-community/Llama-3.2-3B-Instruct-4bit")
response = generate(model, tokenizer, prompt="Explain quantum entanglement", verbose=True)
```

## CLI examples

```bash
# Pull and run a specific model
ollama run qwen3.5-coder:32b

# List downloaded models and their sizes
ollama list

# Show detailed information about a running model
ollama ps

# Benchmark local inference speed (tokens/sec)
# Using a 100-token prompt
time ollama run llama3.2 "Write a 100 word essay on AI"
```

## API examples

### Python: OpenAI-Compatible Entry
Many local tools now support the OpenAI `/v1/chat/completions` standard.

```python
import openai

client = openai.OpenAI(
    base_url="http://localhost:11434/v1", # Ollama default
    api_key="ollama", # Required but ignored
)

response = client.chat.completions.create(
    model="llama3.2",
    messages=[{"role": "user", "content": "Hello local LLM!"}]
)
print(response.choices[0].message.content)
```

## Security considerations
- **Local API Binding**: By default, local servers bind to `127.0.0.1`. Do not change this to `0.0.0.0` unless you have a firewall or VPN in place.
- **Model Poisoning**: Only download models from verified publishers (e.g., `ollama`, `mlx-community`, `bartowski`).
- **Memory Privacy**: Local inference keeps data in RAM/VRAM. Ensure your machine is physically secure and uses disk encryption.

## Related tools / concepts
- [Ollama (Service)](../../services/ollama.md) — The backend engine.
- [LM Studio](https://lmstudio.ai/) — GUI for model management.
- [Open WebUI](../../services/open-webui.md) — The premier web interface for local LLMs.
- [LiteLLM](../../services/litellm.md) — Proxy for switching between local and cloud models.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — For giving local models tool access.
- [AnythingLLM](https://docs.useanything.com/introduction) — Full-stack local RAG solution.

## Backlog
- [x] Perform quarterly technical freshness audit. (Completed: 2026-06-03)

## Contribution Metadata
- Last reviewed: 2026-06-03
- Confidence: high

## Sources / References
- [AnythingLLM Documentation](https://docs.useanything.com/introduction)
- [Ollama Official Documentation](https://ollama.com/library)
- [MLX Examples Repository](https://github.com/ml-explore/mlx-examples)
- [llama.cpp GitHub](https://github.com/ggerganov/llama.cpp)
- [Llama 3.2 Technical Report](https://ai.meta.com/blog/llama-3-2-connect-2024-vision-edge-mobile-devices/)
