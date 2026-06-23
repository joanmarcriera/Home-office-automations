# LM Studio

## What it is
LM Studio is a desktop application for discovering, downloading, running, and chatting with local models. It provides a user-friendly interface for managing GGUF and MLX models on local hardware, including a native inference server.

## What problem it solves
It lowers the barrier to local LLM experimentation by packaging model discovery, downloads, chat, and an OpenAI-compatible local server into one desktop workflow. It eliminates the need for complex CLI setups for users who want to quickly evaluate models or run private inference on their workstations.

## Where it fits in the stack
**AI & Knowledge / Local Model Workbench**. It is a practical bridge between end-user experimentation and local inference, sitting above the [Inference Engine](../infrastructure/index.md) layer.

## Typical use cases
- **Model Evaluation**: Testing local models (Llama 3.3, Qwen 3.5) without a CLI-heavy setup.
- **Local API Endpoint**: Running a local OpenAI-compatible endpoint for development of agentic applications.
- **Hardware Benchmarking**: Comparing performance of small and medium models on Apple Silicon or NVIDIA hardware.
- **Private Chat**: Interacting with LLMs locally to ensure data privacy for sensitive workflows.

## Strengths
- **Native Apple Silicon Support**: (June 2026) Fully optimized for M4/M5 unified memory architecture, allowing the M5 (48 GB) to host models up to 70B (Q4_K_M) with excellent performance.
- **Integrated Model Browser**: Direct access to Hugging Face GGUF models with one-click downloads.
- **Multi-Backend**: Supports both `llama.cpp` (GGUF) and native MLX backends (v0.3.6+).
- **Zero-Config Server**: Instantly spin up an OpenAI-compatible API server.
- **In-App Monitoring**: Real-time visualization of VRAM usage, token throughput, and system resource consumption.

## Limitations
- **Desktop-Centric**: Designed as a GUI application; not ideal for headless server-grade or multi-user production deployments.
- **Closed Source**: The application itself is proprietary, although it utilizes open-source backends.
- **Resource Competition**: Running the GUI consumes system resources that could otherwise be dedicated to inference.

## When to use it
- When you want the fastest path to trying local models on macOS, Windows, or Linux.
- When you need a simple, reliable local server for app development or evaluation.
- When you are utilizing Apple Silicon and want to leverage unified memory via the native MLX or Metal backends.

## When not to use it
- When you need a multi-user, production-ready inference cluster (use [vLLM](../infrastructure/vllm.md) or [SGLang](../infrastructure/sglang.md) instead).
- When you require a headless environment with zero GUI overhead (use [Ollama](../../services/ollama.md)).

## Getting started
1. **Download**: Install LM Studio from [lmstudio.ai](https://lmstudio.ai/).
2. **Search**: Use the "Search" tab to find a model (e.g., `Meta-Llama-3.3-70B-Instruct-GGUF`).
3. **Download**: Choose a quantization level (e.g., `Q4_K_M`) and click download.
4. **Load**: Go to the "AI Chat" tab, select the model from the top dropdown, and wait for it to load into VRAM/Unified Memory.
5. **Configure GPU**: In **Settings → GPU**, ensure **Apple Metal** or **NVIDIA CUDA** is selected for acceleration.

## CLI examples
The `lms` CLI (v0.4.x+) allows for headless management of the LM Studio backend.

```bash
# Check status and loaded models
lms status

# Search for and download a model
lms get meta-llama-3.3-70b

# Start the local OpenAI-compatible API server on a specific port
lms server start --port 1234 --gpu-layers auto

# List all downloaded models
lms ls
```

## API examples
LM Studio provides a local server that is a drop-in replacement for the OpenAI API.

```python
from openai import OpenAI

# Point to the local LM Studio endpoint
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lmstudio")

response = client.chat.completions.create(
    model="meta-llama-3.3-70b",
    messages=[{"role": "user", "content": "Explain the benefit of unified memory for LLMs."}]
)

print(response.choices[0].message.content)
```

## Related tools / concepts
- [Local LLMs (Ollama, MLX, llama.cpp)](../ai_knowledge/local_llms.md)
- [Ollama](../../services/ollama.md)
- [Jan.ai](jan-ai.md)
- [Msty](msty.md)
- [Claude Code](../development_ops/claude-code.md)
- [llama.cpp](../infrastructure/llama-cpp.md)
- [MLX](mlx.md)
- [vLLM](../infrastructure/vllm.md)
- [SGLang](../infrastructure/sglang.md)
- [Inference Engines](../infrastructure/index.md)

## Sources / References
- [Official Website](https://lmstudio.ai/)
- [LM Studio CLI Documentation](https://lmstudio.ai/docs/cli)
- [LM Studio v0.3.x Release Notes](https://lmstudio.ai/blog/v0.3.0)
- [Apple Silicon Unified Memory for LLMs](https://developer.apple.com/metal/tensorflow-plugin/)

## Contribution Metadata
- Last reviewed: 2026-06-23
- Confidence: high
