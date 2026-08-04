# ZSE (Zero-Shot Engine)

## What it is
ZSE is an open-source LLM inference engine optimized for extreme performance and deployment efficiency. As of late 2026, it is recognized for its ability to serve models with industry-leading "cold start" times, making it a favorite for serverless AI architectures, dynamic agent orchestration, and edge deployment.

## What problem it solves
It solves the latency bottleneck in on-demand LLM serving. Standard inference engines often take tens of seconds to load a model into VRAM; ZSE achieves cold start times as low as 3.9 seconds for 8B-parameter models, enabling truly responsive serverless AI without the cost of "always-on" GPUs. This drastically lowers operational overhead for homelab clusters and corporate serverless endpoints, especially when utilizing lightweight models like [Gemma 3](../ai_knowledge/local_llms.md) and Qwen 3.6.

## Where it fits in the stack
**Infrastructure / Inference Engine**. It sits in the execution plane, serving models to agents, applications, and orchestration layers via an OpenAI-compatible API.

## Typical use cases
- **Serverless LLM APIs**: Providing on-demand model serving where pay-per-token or pay-per-request models are required.
- **Dynamic Agentic Scaling**: Spawning new inference instances in seconds to handle spikes in agentic task volume.
- **Edge Inference**: Running specialized models on edge servers where resources must be reclaimed immediately after use.
- **Development & Testing**: Rapidly iterating on prompts across different models without waiting for long load times.

## Strengths
- **Ultra-Fast Cold Starts**: Optimized weights-loading and kernel initialization (3.9s for Llama 4 8B and Gemma 3).
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
ZSE provides a powerful REST control interface alongside its inference capabilities. Below is a robust Python example using **Pydantic v2** validation to programmatically configure, warm up, and interact with the ZSE server.

```python
from typing import Optional, Dict
from pydantic import BaseModel, Field, confloat, conint
import requests

# 1. Define strict configuration schema using Pydantic v2
class ZSEEngineConfig(BaseModel):
    model_name: str = Field(alias="model", default="gemma-3-8b-instruct")
    max_active_instances: int = Field(default=3, ge=1)
    vram_ttl_seconds: int = Field(default=300, ge=30)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=512, gt=0)

class WarmupPayload(BaseModel):
    model: str
    prewarm_kv_cache: bool = True
    concurrency_limit: Optional[int] = None

class ZSEInstanceStatus(BaseModel):
    instance_id: str
    status: str
    vram_allocated_mb: int
    loaded_at: float

# 2. Programmatic Controller class to interact with ZSE APIs
class ZSEController:
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url

    def warmup_instance(self, payload: WarmupPayload) -> bool:
        # Validate input schema
        validated_payload = payload.model_dump()
        try:
            response = requests.post(
                f"{self.base_url}/control/warmup",
                json=validated_payload,
                timeout=10
            )
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with ZSE engine: {e}")
            return False

    def query_status(self, instance_id: str) -> Optional[ZSEInstanceStatus]:
        try:
            response = requests.get(f"{self.base_url}/control/status/{instance_id}", timeout=5)
            if response.status_code == 200:
                # Validate output schema via Pydantic v2
                return ZSEInstanceStatus.model_validate(response.json())
        except Exception as e:
            print(f"Failed status parsing: {e}")
        return None

# 3. Demonstration usage
if __name__ == "__main__":
    controller = ZSEController()
    payload = WarmupPayload(model="gemma-3-8b-instruct", prewarm_kv_cache=True)
    success = controller.warmup_instance(payload)
    print(f"Pre-warm Status: {success}")
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
- Last reviewed: 2026-11-23
- Confidence: high
