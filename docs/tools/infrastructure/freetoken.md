# FreeToken

## What it is
FreeToken is an open-source high-performance local LLM inference engine and token-management sidecar daemon designed for zero-latency token recycling, prefix cache sharing, and dynamic GPU memory optimization. Released in mid-2026 and widely adopted in early 2027, FreeToken operates between agent orchestrators and local model runtimes (such as [vLLM](vllm.md), [llama.cpp](llama-cpp.md), or [Ollama](../../services/ollama.md)), dramatically accelerating multi-agent workflows and reducing TTFT (Time To First Token) for local execution environments.

## What problem it solves
In multi-agent architectures and iterative code-editing sessions, high context repetition across requests results in redundant key-value (KV) cache generation and heavy token processing latencies. FreeToken resolves this bottleneck by implementing cross-process shared KV-cache layers, immediate memory reclamation upon task completion, and token reuse algorithms that bypass redundant prefill phases across local model instances.

## Where it fits in the stack
**Infrastructure & Serving Layer**. FreeToken sits as a lightweight proxy and KV-cache management sidecar directly ahead of local LLM inference servers.

## Typical use cases
- **Multi-Agent Swarm Orchestration**: Accelerating parallel agents ([Claude 5.6](../ai_knowledge/claude.md), [Qwen 3.8](../ai_knowledge/qwen.md), or [Gemma 4](../ai_knowledge/gemma.md)) sharing common system prompts and MCP schemas.
- **Local Workstation Memory Optimization**: Dynamic VRAM offloading and instant KV-cache swapping between active models on single-GPU setups.
- **IDE Code-Assistant Sidecars**: Bypassing prefill computation during rapid, iterative code autocomplete and diff generation in [OmO](../development_ops/opencode.md) or VS Code.
- **FastMCP 3.1 Task Protocol Acceleration**: Caching tool definition schemas across thousands of subtask tool calls.

## Strengths
- **Zero-Prefill Token Recycling**: Eliminates re-computation for identical system prompts and context prefixes.
- **Cross-Engine Support**: Seamlessly bridges with vLLM, SGLang, ExLlamaV3, and llama.cpp runtimes.
- **Low VRAM Overhead**: Rust-based core engine with minimal memory footprint (<30MB RAM).
- **FastMCP 3.1 Native Protocol Integration**: Direct awareness of MCP tool definitions and context frames.

## Limitations
- **Local Network Proxy Hop**: Introduces a minor <1ms local loopback routing latency for non-cached tokens.
- **Cache Eviction Tuning**: Requires configuring eviction policies (LRU / LFU) based on workload memory limits.

## When to use it
- When running local swarms of AI agents on consumer or workstation GPUs.
- When developer workflows involve heavy context reuse (e.g. multi-file repository indexing or repetitive tool schemas).
- When seeking to reduce Time-To-First-Token (TTFT) for local interactive coding assistants.

## When not to use it
- When all LLM requests are routed exclusively to proprietary cloud APIs (e.g., Anthropic or OpenAI cloud endpoints) where server-side caching is handled remotely.
- When running single, non-interactive batch inference jobs with zero context overlap.

## Getting started
FreeToken can be installed via package manager or run via Docker container as an OpenAI-compatible proxy sidecar.

```bash
# Install FreeToken CLI and proxy daemon
cargo install freetoken-cli

# Start FreeToken proxy forwarding to local vLLM or Ollama instance
freetoken-daemon --backend http://localhost:11434 --port 8080 --cache-size-gb 4
```

## CLI examples

### 1. Launching FreeToken Sidecar with Automatic Memory Reclamation
```bash
# Launch daemon with maximum GPU memory bound and FastMCP 3.1 cache tracking
freetoken-daemon --port 8080 --target http://127.0.0.1:8000 --enable-mcp-cache
```

### 2. Monitoring Token Reuse and Cache Hit Ratio
```bash
# Display live token cache metrics and VRAM savings
freetoken-cli stats
```

### 3. Evicting Stale Context Prefixes
```bash
# Clear cached KV states for a specific agent session
freetoken-cli purge --session-id "agent-task-9921"
```

## API examples

### Python Integration with OpenAI Client Proxying
```python
import os
from openai import OpenAI

# Direct client to FreeToken proxy endpoint instead of raw inference server
client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="freetoken-local"
)

# Request will benefit from prefix cache token recycling
response = client.chat.completions.create(
    model="qwen3.8-27b",
    messages=[
        {"role": "system", "content": "Large system prompt with extensive MCP tool definitions..."},
        {"role": "user", "content": "Execute task decomposition step 1."}
    ]
)

print(response.choices[0].message.content)
```

### Programmatic Python Integration with Pydantic v2 Metrics Validation
The following script demonstrates querying FreeToken cache statistics and strictly validating response performance using **Pydantic v2** models.

```python
import sys
from typing import Optional
from pydantic import BaseModel, Field, ValidationError

class FreeTokenCacheMetrics(BaseModel):
    total_requests: int = Field(..., description="Total LLM requests routed through proxy")
    cache_hits: int = Field(..., description="Requests leveraging recycled prefix tokens")
    recycled_tokens: int = Field(..., description="Total tokens saved from prefill re-computation")
    saved_vram_mb: float = Field(..., description="VRAM footprint saved via shared KV-cache")
    hit_ratio: float = Field(..., description="Percentage of requests hitting KV cache")

class FreeTokenStatusResponse(BaseModel):
    status: str
    active_backend: str
    metrics: FreeTokenCacheMetrics

def parse_freetoken_status(data: dict) -> Optional[FreeTokenStatusResponse]:
    try:
        return FreeTokenStatusResponse.model_validate(data)
    except ValidationError as ve:
        print(f"Pydantic Validation Error for FreeToken status: {ve}", file=sys.stderr)
        return None

if __name__ == "__main__":
    print("Validating FreeToken runtime status and metrics...")

    mock_status_data = {
        "status": "healthy",
        "active_backend": "http://127.0.0.1:11434",
        "metrics": {
            "total_requests": 1420,
            "cache_hits": 1180,
            "recycled_tokens": 850400,
            "saved_vram_mb": 3450.5,
            "hit_ratio": 83.1
        }
    }

    validated = parse_freetoken_status(mock_status_data)
    if validated:
        print("FreeToken Metrics Validated Successfully:")
        print(f"  Backend: {validated.active_backend}")
        print(f"  Hit Ratio: {validated.metrics.hit_ratio}%")
        print(f"  Recycled Tokens: {validated.metrics.recycled_tokens:,}")
        print(f"  VRAM Saved: {validated.metrics.saved_vram_mb} MB")
    else:
        print("Validation failed.", file=sys.stderr)
```

## Related tools / concepts
- [vLLM](vllm.md) — High-throughput serving engine with PagedAttention.
- [SGLang](sglang.md) — Fast execution engine for structured outputs.
- [ExLlamaV3](exllamav3.md) — Next-gen GPU inference engine.
- [llama.cpp](llama-cpp.md) — C/C++ inference engine for local models.
- [ROCm](rocm.md) — AMD open software platform for GPU compute.

## Sources / references
- [InfoQ: FreeToken Local LLM Inference Release](https://www.infoq.com/news/2026/08/freetoken-local-inference/)
- [vLLM Shared KV-Cache Documentation](https://docs.vllm.ai/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
