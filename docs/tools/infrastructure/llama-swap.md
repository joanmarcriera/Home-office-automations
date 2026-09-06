# llama-swap

## What it is
llama-swap is an open-source, lightweight model proxy and routing engine designed to hot-swap local GGUF models on demand behind a single OpenAI-compatible API endpoint. Built primarily for resource-constrained home labs and edge deployments running `llama.cpp`, it automatically loads and unloads models based on incoming API requests.

## What problem it solves
Running multiple local LLMs concurrently requires significant VRAM or RAM, which quickly exhausts hardware capacity on consumer GPUs or single-board computers. Manually starting and stopping different model server instances creates friction and breaks agent workflows expecting an always-on endpoint. llama-swap solves this by transparently intercepting API calls, unloading inactive models, and spinning up requested models dynamically without requiring manual server reconfiguration.

## Where it fits in the stack
**Infrastructure / Model Routing & Serving**. llama-swap sits between AI clients/agents and underlying `llama.cpp` server backends, acting as a dynamic, VRAM-conscious proxy layer.

## Typical use cases
- **Multi-Model Home Lab Serving**: Hosting code-completion, reasoning, and chat models on a single GPU without VRAM overflow.
- **OpenAI API Proxying**: Intercepting requests from tools like Open WebUI, LiteLLM, or Cursor to dynamically load target models.
- **Automated Memory Reclamation**: Automatically unloading idle models after a configurable TTL timeout to free system resources.

## Strengths
- **VRAM Optimization**: Maximizes efficiency by ensuring only active models reside in VRAM.
- **Drop-in OpenAI Compatibility**: Works seamlessly with standard OpenAI client SDKs and agent frameworks.
- **Zero-Downtime Configuration**: Allows dynamic model registry updates without restarting the proxy.

## Limitations
- **Load Latency Penalty**: Switching models introduces initial startup latency while loading GGUF weights into memory.
- **Single-User / Low-Concurrency Focus**: Optimized for individual home labs or small teams rather than multi-tenant high-throughput production clusters.

## When to use it
- When operating home lab hardware with limited VRAM (e.g., 8GB–24GB GPUs) that cannot hold multiple models simultaneously.
- When agent workflows require access to specialized models (e.g., Qwen-Coder vs Llama-3) on demand.
- When requiring automatic idle model unloading to conserve power and VRAM.

## When not to use it
- When running enterprise inference clusters where all models must remain warm with zero load latency.
- When using high-concurrency model servers like vLLM or TGI that manage batching across shared GPUs.

## Getting started
To set up llama-swap on a home lab server:

```bash
# Install llama-swap CLI / binary
go install github.com/sammcj/llama-swap@latest

# Start llama-swap with a configuration file
llama-swap --config config.yaml
```

Example `config.yaml`:
```yaml
port: 8080
models:
  llama-3:
    cmd: "llama-server -m /models/llama-3-8b.gguf --port 8081"
    port: 8081
  qwen-coder:
    cmd: "llama-server -m /models/qwen2.5-coder-7b.gguf --port 8082"
    port: 8082
ttl: 300 # Unload model after 5 minutes of inactivity
```

## CLI examples

```bash
# Check running llama-swap status
llama-swap status

# Pre-warm a specific model endpoint
curl -X POST http://localhost:8080/v1/models/llama-3/load
```

## API examples

### 1. Pydantic v2 Schema for llama-swap Configuration
```python
from typing import Dict, Optional
from pydantic import BaseModel, ConfigDict, Field

class ModelEndpointConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    cmd: str = Field(..., description="Execution command for launching backend llama-server instance")
    port: int = Field(..., ge=1024, le=65535, description="Local port for the backend instance")

class LlamaSwapConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    port: int = Field(default=8080, ge=1024, le=65535, description="Proxy listening port")
    ttl_seconds: int = Field(default=300, ge=0, description="Idle timeout before unloading model")
    models: Dict[str, ModelEndpointConfig] = Field(..., description="Registry of available models")

if __name__ == "__main__":
    cfg = LlamaSwapConfig(
        port=8080,
        ttl_seconds=300,
        models={
            "qwen-coder": ModelEndpointConfig(
                cmd="llama-server -m /models/qwen2.5-coder.gguf --port 8081",
                port=8081
            )
        }
    )
    print(f"llama-swap configured on port {cfg.port} with {len(cfg.models)} model(s).")
```

### 2. FastMCP 3.1 Task Protocol Integration
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("llama-swap-manager")

@mcp.tool()
def swap_model(model_name: str, target_port: int = 8080) -> dict:
    """Hot-swaps target GGUF model via llama-swap proxy endpoint."""
    return {"status": "swapping", "requested_model": model_name, "proxy_port": target_port}
```

## Related tools / concepts
- [llama.cpp](llama-cpp.md) — Core backend execution engine for GGUF models.
- [Ollama](ollama.md) — Alternative local model runner with built-in model management.
- [Model Routing Guide](../../knowledge_base/model_routing_guide.md) — Architectural patterns for local model routing.

## Sources / references
- [llama-swap GitHub Repository](https://github.com/sammcj/llama-swap)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
