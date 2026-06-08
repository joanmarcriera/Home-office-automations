# LM Studio

## What it is
LM Studio is a desktop application for discovering, downloading, running, and chatting with local models.

## What problem it solves
It lowers the barrier to local LLM experimentation by packaging model discovery, downloads, chat, and an OpenAI-compatible local server into one desktop workflow.

## Where it fits in the stack
**AI & Knowledge / Local Model Workbench**. It is a practical bridge between end-user experimentation and local inference.

## Typical use cases
- Testing local models without a CLI-heavy setup
- Running a local OpenAI-compatible endpoint for development
- Comparing small and medium models on a laptop or workstation

## Strengths
- Easy local-model onboarding
- Friendly UI for experimentation
- Useful stepping stone before deeper infrastructure choices

## Limitations
- Less flexible than lower-level inference stacks for production
- Desktop-first workflow is not ideal for multi-user deployment

## Apple Silicon / Metal backend

LM Studio v0.3.0+ ships with a native Metal inference backend for Apple Silicon, using llama.cpp under the hood. All 48 GB of the M5's unified memory is addressable by Metal — there is no separate VRAM pool. This makes the M5 MacBook a better local LLM host than any single consumer NVIDIA GPU for models in the 30-40B range.

**M5 48 GB model ceiling:**

| Model | Quantization | Approx. RAM | Notes |
|---|---|---|---|
| Llama 3.3 70B | Q4_K_M | ~40 GB | Fits, leaves ~8 GB headroom |
| Qwen3.5 32B | Q5_K_M | ~22 GB | Comfortable, excellent quality |
| Llama 3.2 11B | Q8_0 | ~12 GB | Near full precision |
| Llama 3.2 3B | Q8_0 | ~3.5 GB | Fast; good for local agents |

**CLI launch with Metal:**
```bash
lms server start --port 1234 --gpu-layers auto
```
The `auto` flag lets LM Studio calculate the optimal number of layers to offload to Metal based on available unified memory.

In the **Settings → GPU** panel, ensure the **Apple Metal** or **llama.cpp Metal** backend is selected. Use the GGUF model filter when browsing — MLX-format models require the separate MLX backend available in LM Studio 0.3.6+.

## When to use it
- When you want the fastest path to trying local models
- When you need a simple local server for app development or evaluation

## When not to use it
- When you need multi-user, server-grade inference
- When you already operate [Ollama](../../services/ollama.md) or [vLLM](../infrastructure/vllm.md) successfully

## Getting started
1. Download and install LM Studio from [lmstudio.ai](https://lmstudio.ai/).
2. Open the app and search for a model (e.g., `Meta-Llama-3-8B-Instruct-GGUF`).
3. Click "Download" on the desired version.
4. Go to the "AI Chat" tab to interact with the model immediately, or the "Local Server" tab to start an API.

## CLI examples
The `lms` CLI is bundled with the desktop application (requires version 0.4.0+).

```bash
# Check status and loaded models
lms status

# Search for and download a model
lms get meta-llama-3-8b

# Start the local OpenAI-compatible API server
lms server start --port 1234
```

## API examples
LM Studio provides an OpenAI-compatible local server.

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lmstudio")

response = client.chat.completions.create(
    model="meta-llama-3-8b",
    messages=[{"role": "user", "content": "Explain quantum entanglement."}]
)
print(response.choices[0].message.content)
```

## Licensing and cost
- **Open Source**: No
- **Cost**: Free desktop app
- **Self-hostable**: Local desktop runtime only

## Related tools / concepts
- [Local LLMs (Ollama, MLX, llama.cpp)](../ai_knowledge/local_llms.md)
- [Ollama](../../services/ollama.md)
- [Jan.ai](jan-ai.md)
- [Msty](msty.md)
- [Claude Code](../development_ops/claude-code.md)
- [llama.cpp](../infrastructure/llama-cpp.md)
- [MLX](mlx.md) — Lower-level Apple Silicon inference framework that LM Studio wraps

## Sources / References
- [Official Website](https://lmstudio.ai/)
- [LM Studio CLI Documentation](https://lmstudio.ai/docs/cli)

## Contribution Metadata
- Last reviewed: 2026-06-03
- Confidence: high
