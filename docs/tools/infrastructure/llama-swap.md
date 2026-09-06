# llama-swap

## What it is
`llama-swap` is a lightweight, low-overhead model hot-swapping proxy and launcher for local LLM inference engines like [llama.cpp](llama-cpp.md). It presents a unified, OpenAI-compatible API endpoint while dynamically loading, unloading, and swapping GGUF models on demand according to incoming API request model parameters.

## What problem it solves
Self-hosters and home-lab operators running local LLMs on VRAM-constrained hardware (e.g., single NVIDIA GPUs or Apple Silicon Macs) often need access to multiple specialized models (e.g., coding, general chat, summarization, embedding models). Keeping all models resident in VRAM simultaneously causes out-of-memory (OOM) errors or heavy memory paging. `llama-swap` eliminates manual model loading and dedicated multi-port server instances by managing the lifecycle of underlying inference processes automatically, loading requested models into VRAM on demand and un-loading idle models after configurable timeout periods.

## Where it fits in the stack
**Infrastructure / Model Routing & Local Serving**. It sits between client applications (e.g., Open WebUI, FastMCP 3.1 agents, auto-routing API gateways) and local inference engines such as `llama.cpp` or `ollama`.

## Typical use cases
- **Multi-Model Home-Lab Gateways**: Exposing a single OpenAI-compatible `/v1/chat/completions` endpoint for diverse local workloads without locking VRAM permanently.
- **Agentic Workflows**: Allowing local agents (e.g., FastMCP 3.1 task runners) to switch between small fast models for routing and larger reasoning models for execution.
- **Resource-Constrained Server Hosting**: Running multiple LLMs efficiently on single-GPU hardware like RTX 4060/4090 or Mac Studio unified memory setups.

## Strengths
- **Transparent OpenAI API Proxying**: Fully compatible with OpenAI client SDKs and agent frameworks.
- **Dynamic On-Demand Swapping**: Automatically spawns background server instances (like `llama-server`) for requested models and terminates idle ones after TTL timeouts.
- **Zero Idle VRAM Usage**: Evicts models when inactive, leaving VRAM free for other workloads (e.g., image generation, embedding models).
- **Simple Configuration**: Declarative YAML configuration specifying model paths, startup arguments, ports, and idle timeouts.

## Limitations
- **Model Swapping Latency**: Initial request to an unloaded model incurs a cold-start delay while the model weights are loaded into VRAM.
- **Single-Active Concurrency Tradeoff**: Optimized for sequential or low-concurrency multi-model switching on a single GPU rather than high-throughput concurrent batching across multiple models simultaneously.

## When to use it
- When you want to serve 5+ different local GGUF models on a single workstation or server without keeping them all in VRAM.
- When client apps expect a single static server endpoint (e.g., `http://localhost:8080/v1`) but need access to multiple underlying models.

## When not to use it
- High-concurrency production deployments with multi-GPU clusters where models are permanently resident in VRAM — use [vLLM](vllm.md) or [TGI](tgi.md).
- Single-model single-purpose dedicated serving setups.

## Getting started

### Installation
```bash
# Clone and build from source or install pre-built binaries
git clone https://github.com/michaelfeil/llama-swap.git
cd llama-swap
go build -o llama-swap main.go
```

### Example Configuration (`config.yaml`)
```yaml
port: 8080
models:
  llama-4-8b:
    cmd: "llama-server -m /models/llama-4-8b-Q4_K_M.gguf --port 8081 -c 8192 -gqa"
    port: 8081
    ttl: 300
  qwen-3-8:
    cmd: "llama-server -m /models/qwen-3.8-27b-Q4_K_M.gguf --port 8082 -c 8192"
    port: 8082
    ttl: 300
```

## CLI examples

### Starting llama-swap with custom config
```bash
./llama-swap --config config.yaml --port 8080
```

## API examples

### Querying Swappable Endpoint via OpenAI SDK
```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8080/v1", api_key="not-needed")

# Request automatically loads llama-4-8b
response = client.chat.completions.create(
    model="llama-4-8b",
    messages=[{"role": "user", "content": "Explain local GGUF model hot-swapping."}]
)
print(response.choices[0].message.content)
```

## Related tools / concepts
- [llama.cpp](llama-cpp.md) — Fast C++ GGUF inference engine used as backend.
- [Ollama](../../services/ollama.md) — Local model serving runtime with built-in model management.
- [vLLM](vllm.md) — High-throughput GPU inference engine.
- [Text Generation WebUI](text-generation-webui.md) — Gradio web interface supporting multiple inference backends.

## Sources / references
- [llama-swap GitHub Repository](https://github.com/michaelfeil/llama-swap)
- [llama.cpp GitHub Repository](https://github.com/ggerganov/llama.cpp)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
