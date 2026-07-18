# ZSE (Zero-Shot Engine)

## What it is
ZSE is an open-source LLM inference engine optimized for extreme performance and deployment efficiency. As of July 2026, it is recognized for its ability to serve models with industry-leading "cold start" times, making it a favorite for serverless AI architectures, dynamic agent orchestration, and edge deployment.

## What problem it solves
It solves the latency bottleneck in on-demand LLM serving. Standard inference engines often take tens of seconds to load a model into VRAM; ZSE achieves cold start times as low as 3.9 seconds for 8B-parameter models, enabling truly responsive serverless AI without the cost of "always-on" GPUs. This drastically lowers operational overhead for homelab clusters and corporate serverless endpoints.

## Where it fits in the stack
**Infrastructure / Inference Engine**. It sits in the execution plane, serving models to agents, applications, and orchestration layers via an OpenAI-compatible API.

## Typical use cases
- **Serverless LLM APIs**: Providing on-demand model serving where pay-per-token or pay-per-request models are required.
- **Dynamic Agentic Scaling**: Spawning new inference instances in seconds to handle spikes in agentic task volume.
- **Edge Inference**: Running specialized models on edge servers where resources must be reclaimed immediately after use.
- **Development & Testing**: Rapidly iterating on prompts across different models without waiting for long load times.

## Strengths
- **Ultra-Fast Cold Starts**: Optimized weights-loading and kernel initialization (3.9s for Llama-3-8B and Gemma 3).
- **Lightweight Architecture**: Minimal overhead compared to feature-heavy engines like vLLM.
- **Open-Source Freedom**: Fully self-hostable with no licensing fees for standard deployment.
- **Hardware Agnostic**: Supports NVIDIA (CUDA), Apple Silicon (MPS), and emerging NPUs.
- **Optimized VRAM Reclamation**: Instantly purges inactive models from VRAM according to configurable TTL policies.

## Limitations
- **Feature Set**: Lacks some of the complex speculative decoding and multi-LoRA features found in vLLM or SGLang.
- **Model Coverage**: While growing, support for very large models (100B+) or exotic architectures may lag behind established frameworks.
- **Community**: Smaller ecosystem of plugins and integrations compared to Ollama or Hugging Face.

## When to use it
- When cold start latency is the primary bottleneck in your application.
- When building a "scale-to-zero" AI platform.
- When you need a lightweight, no-frills inference runner for specialized local tasks.

## When not to use it
- For massive, steady-state production clusters where absolute throughput (tokens/sec) is more important than startup speed (use [vLLM](vllm.md)).
- If you require the extensive UI and model-management features of [Ollama](../../services/ollama.md).
- For research requiring cutting-edge speculative decoding or complex batching strategies.

## Getting started

### Installation
```bash
pip install zyora-zse
```

### Initializing a Model
```bash
zse init gemma-3-8b-instruct
```

### Simple Inference (Python)
```python
from zse import ZSE

# Initialize the engine
engine = ZSE(model="gemma-3-8b-instruct")

# Generate a response
response = engine.generate("Explain the 'cold start' problem in serverless computing.")
print(response)
```

## CLI examples

### Serving an API
Start an OpenAI-compatible server on a specific port:
```bash
zse serve --model gemma-3-8b-instruct --port 8080 --host 0.0.0.0
```

### Monitoring Instances
List all active and suspended model instances:
```bash
zse ps --all
```

### Cleaning Up
Reclaim VRAM by stopping and purging an instance:
```bash
zse stop <instance_id>
zse purge
```

## API examples

### OpenAI-Compatible Completion
Interact with the ZSE server using standard tools like `curl`.

```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma-3-8b-instruct",
    "messages": [{"role": "user", "content": "What makes ZSE unique?"}]
  }'
```

### Programmatic State Management
ZSE allows agents to manage the inference lifecycle via its control API.

```python
import requests

# Instruct ZSE to pre-warm a model for an upcoming task
requests.post("http://localhost:8080/control/warmup", json={"model": "mistral-7b-v0.3"})
```

## Related tools / concepts
- [Ollama](../../services/ollama.md) — The standard for local model management.
- [vLLM](vllm.md) — The benchmark for high-throughput production inference.
- [SGLang](sglang.md) — Structured generation engine.
- [Local LLMs](../ai_knowledge/local_llms.md) — The broader local AI ecosystem.
- [Aphrodite Engine](aphrodite-engine.md) — High-throughput local alternative.
- [LiteLLM](../../services/litellm.md) — Unified API proxy for ZSE and other engines.
- [Model Routing Guide](../../knowledge_base/model_routing_guide.md) — Strategy for selecting the right engine.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Protocol for agentic context and tool registries.
- [ExLlamaV2](exllamav2.md) — Highly optimized inference engine for NVIDIA GPUs.
- [llama.cpp](llama-cpp.md) — Lightweight, cross-platform inference engine.

## Sources / references
- [ZSE GitHub Repository](https://github.com/Zyora-Dev/zse)
- [Serverless LLM Performance Benchmarks (2026)](https://zyora.dev/blog/zse-benchmarks)
- [Zyora Official Documentation](https://docs.zyora.dev/zse)
- [Model Serving Patterns](../../knowledge_base/model_routing_guide.md)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
