# ZSE (Zero-Shot Engine)

## What it is
ZSE is an open-source LLM inference engine optimized for extreme performance, low overhead, and high deployment efficiency. It is recognized for serving open models with industry-leading cold start times (sub-3 seconds for 8B-parameter models), making it a key runtime for serverless AI architectures, dynamic agent orchestration, and edge deployment powered by SOTA models like Claude 5.6, GPT-5.6, and Gemini 4.0 Ultra.

## What problem it solves
It solves the latency bottleneck in on-demand LLM serving. Standard inference engines often take tens of seconds to load a model into VRAM; ZSE achieves cold start times under 3 seconds for 8B models (such as Llama 4 8B or Gemma 4 8B), enabling responsive serverless AI without the continuous cost of always-on GPUs. This drastically lowers operational overhead for homelab clusters and corporate serverless endpoints.

## Where it fits in the stack
**Infrastructure / Inference Engine**. It sits in the execution plane, serving models to agents, applications, and orchestration layers via an OpenAI-compatible API and native FastMCP 3.1 / MCP 3.1 protocol transport hooks.

```
┌──────────────────────────────────────────────┐
│           Agent & MCP Orchestration          │
│       (Claude 5.6, GPT-5.6, FastMCP 3.1)     │
├──────────────────────────────────────────────┤
│         ZSE ZERO-SHOT INFERENCE ENGINE       │ (Sub-3s Cold Starts, TTL Reclamation)
├──────────────────────────────────────────────┤
│     Hardware Acceleration (CUDA / Metal 3)   │
└──────────────────────────────────────────────┘
```

## Typical use cases
- **Serverless LLM APIs**: Providing on-demand model serving where pay-per-token or scale-to-zero compute models are required.
- **Dynamic Agentic Scaling**: Spawning new inference instances in seconds to handle sudden spikes in agentic task volume via FastMCP 3.1.
- **Edge Inference**: Running specialized models on edge servers where VRAM must be reclaimed immediately after use.
- **Development & Rapid Testing**: Iterating on prompts across different open checkpoints without waiting for long model reloading delays.

## Strengths
- **Ultra-Fast Cold Starts**: Optimized weight-streaming and kernel initialization (sub-3s for Llama 4 8B and Gemma 4).
- **FastMCP 3.1 & OpenAPI Native**: Direct support for MCP tool registries and OpenAI-compatible endpoint contracts.
- **Lightweight Architecture**: Minimal overhead compared to feature-heavy engines like vLLM or SGLang.
- **Hardware Agnostic**: Supports NVIDIA (CUDA 12.8+), Apple Silicon (Metal 3 / MPS), and emerging NPUs.
- **Optimized VRAM Reclamation**: Instantly purges inactive models from GPU memory according to configurable TTL policies.

## Limitations
- **Advanced Batching Features**: Focuses on single/low-concurrency cold-start speed rather than multi-LoRA throughput optimization found in vLLM or SGLang.
- **Model Coverage**: Support for 100B+ parameter architectures may require custom kernel bindings compared to mature engines.
- **Ecosystem Footprint**: Smaller plugin ecosystem than Ollama or Hugging Face TGI.

## When to use it
- When cold start latency is the primary bottleneck in your agent pipeline.
- When building a scale-to-zero local or homelab AI platform.
- When you need a lightweight, low-overhead inference runner for specialized local tasks.

## When not to use it
- For massive, steady-state production clusters where maximum sustained token throughput is prioritized over startup speed (use [vLLM](vllm.md) or [SGLang](sglang.md)).
- If you require the simplified UI and model-management suite of [Ollama](../../services/ollama.md).

## Getting started

### Installation
```bash
pip install zyora-zse
```

### Initializing a Model
```bash
zse init gemma-4-8b-instruct
```

### Simple Inference (Python)
```python
from zse import ZSE

# Initialize the engine
engine = ZSE(model="gemma-4-8b-instruct")

# Generate a response
response = engine.generate("Explain the 'cold start' problem in serverless computing.")
print(response)
```

## CLI examples

### Serving an API with MCP FastMCP 3.1 Support
Start an OpenAI-compatible and FastMCP-enabled server on a specific port:
```bash
zse serve --model gemma-4-8b-instruct --port 8080 --host 0.0.0.0 --enable-mcp
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
ZSE provides a REST control interface alongside its inference capabilities. Below is a Python example using **Pydantic v2** validation to programmatically configure, pre-warm, and interact with the ZSE server.

```python
from typing import Optional
from pydantic import BaseModel, Field, field_validator
import requests

# 1. Define strict configuration schema using Pydantic v2
class ZSEEngineConfig(BaseModel):
    model_name: str = Field(alias="model", default="gemma-4-8b-instruct")
    max_active_instances: int = Field(default=3, ge=1)
    vram_ttl_seconds: int = Field(default=300, ge=30)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=512, gt=0)

    @field_validator("model_name")
    @classmethod
    def validate_model(cls, v: str) -> str:
        if not v:
            raise ValueError("Model name cannot be empty.")
        return v

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
                return ZSEInstanceStatus.model_validate(response.json())
        except Exception as e:
            print(f"Failed status parsing: {e}")
        return None

# 3. Demonstration usage
if __name__ == "__main__":
    controller = ZSEController()
    payload = WarmupPayload(model="gemma-4-8b-instruct", prewarm_kv_cache=True)
    success = controller.warmup_instance(payload)
    print(f"Pre-warm Status: {success}")
```

## Related tools / concepts
- [Ollama](../../services/ollama.md) — Standard for local model management.
- [vLLM](vllm.md) — Benchmark for high-throughput production inference.
- [SGLang](sglang.md) — Structured generation and agent serving engine.
- [Local LLMs](../ai_knowledge/local_llms.md) — Broader local AI ecosystem patterns.
- [Aphrodite Engine](aphrodite-engine.md) — High-throughput local inference runner.
- [LiteLLM](../../services/litellm.md) — Unified API proxy for ZSE and external providers.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Protocol for agentic context and tool registries.
- [ExLlamaV3](exllamav3.md) — Multi-GPU local runtime optimized for low memory.
- [llama.cpp](llama-cpp.md) — Lightweight, cross-platform inference engine.

## Sources / references
- [ZSE GitHub Repository](https://github.com/Zyora-Dev/zse)
- [Serverless LLM Performance Benchmarks](https://zyora.dev/blog/zse-benchmarks)
- [Zyora Official Documentation](https://docs.zyora.dev/zse)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
