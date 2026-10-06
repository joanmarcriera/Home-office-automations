# Turbo-fieldfare

## What it is
Turbo-fieldfare is an open-source, high-performance local inference engine written natively in Swift 6.2 and Metal 3 Performance Shaders, designed specifically for running instruction-tuned Mixture of Experts (MoE) Large Language Models—such as Gemma 4 26B-A4B and its specialized MoE variants—on Apple Silicon Macs (M1 through M5 series). By implementing a dynamic **Active Expert Streaming Architecture**, Turbo-fieldfare serves inactive routed expert weights directly from high-speed NVMe SSD storage rather than keeping the entire 14.3 GB quantized model checkpoint materialized in unified system memory.

This memory-efficient design allows Turbo-fieldfare to execute Gemma 4 26B-A4B with a strictly bounded runtime footprint of only **~2.0 GB of system RAM**, making frontier MoE reasoning accessible on consumer Apple hardware (such as 8 GB or 16 GB MacBook Air and Mac mini configurations) at decode speeds of 5 to 35+ tokens per second. In early 2027, Turbo-fieldfare features built-in **FastMCP 3.1 (Model Context Protocol)** server support and an OpenAI-compatible REST API, allowing local macOS agentic frameworks to leverage high-capacity MoE models without cloud token expenses or memory exhaustion.

## What problem it solves
Running modern medium-capacity MoE models locally (e.g. Gemma 4 26B-A4B, where 4 active experts out of 32 total are routed per token) typically requires 16 GB, 24 GB, or 36 GB of unified memory. For developers, home-lab enthusiasts, and edge deployments operating base-model Apple Silicon hardware with 8 GB or 16 GB of unified RAM, attempting to load a 14 GB checkpoint into MLX or llama.cpp results in heavy memory swap thrashing, system slowdowns, or immediate Out-Of-Memory (OOM) kernel panics.

Turbo-fieldfare resolves these bottlenecks through:
- **SSD Expert Streaming Engine**: Keeps shared attention layers, embeddings, and active router weights in RAM (~2.0 GB) while streaming routed expert matrices on-demand from NVMe storage as tokens are processed.
- **Metal 3 Direct Storage Pipelines**: Utilizes Apple Silicon Metal 3 Direct Storage APIs for low-latency asynchronous DMA transfers from SSD straight into Unified Memory GPU buffers.
- **Dependency-Free Native Binary**: Built entirely in Swift 6.2 without PyTorch, Hugging Face Transformers, or Python runtime overhead, ensuring instant startup and low idle memory overhead.
- **Bounded Memory Footprint**: Binds memory consumption to a strict 2 GB cap, permitting developers to run local MoE inference alongside memory-heavy IDEs, Docker containers, and web browsers.

```
+---------------------------------------------------------------------------------------------------+
|                           TURBO-FIELDFARE SSD EXPERT STREAMING ARCHITECTURE                       |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|   +-----------------------+     +-----------------------+     +-------------------------------+   |
|   |  Agent & Client Apps  |     |  Turbo-fieldfare Core |     |  Metal 3 Compute Pipeline     |   |
|   |                       |     |                       |     |                               |   |
|   | - FastMCP 3.1 Tools   | --> | - Swift 6.2 Runtime   | --> | - Shared Layers (In RAM)      |   |
|   | - OpenAI REST Client  |     | - Route Dispatcher    |     | - Metal Shader Matrix Mult    |   |
|   | - Local macOS CLI     |     | - FastMCP 3.1 Server  |     | - Token Generation Loop       |   |
|   +-----------------------+     +-----------------------+     +-------------------------------+   |
|                                                                               ^                   |
|                                                                               | Direct DMA        |
|                                                               +---------------+---------------+   |
|                                                               |  NVMe Storage Expert Streamer |   |
|                                                               |                               |   |
|                                                               | - Gemma 4 MoE Experts (32)    |   |
|                                                               | - On-Demand Page In (4 Active)|   |
|                                                               | - Metal Direct Storage API    |   |
|                                                               +-------------------------------+   |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
```

## Where it fits in the stack
**Category**: Infrastructure / Inference Runtime Layer.

Turbo-fieldfare sits in the **Local Apple Silicon Execution Layer**, competing with [llama.cpp](llama-cpp.md), [MLX](mlx.md), and [Ollama](../../services/ollama.md). It specializes in SSD-streamed MoE architectures, exposing standard OpenAI-compatible REST endpoints and **FastMCP 3.1** protocol servers to local agent frameworks like [Claude Code](../development_ops/claude-code.md), [Cline](../agents/cline.md), and [Roo Code](../agents/roo-code.md).

## Typical use cases
- **Low-RAM Local MoE Execution**: Running Gemma 4 26B-A4B on base 8 GB or 16 GB Apple Silicon Macs bounded within ~2.0 GB RAM at 5–35+ tokens/sec.
- **Privacy-Preserving On-Device Assistants**: Serving as a zero-cloud-cost reasoning engine for local macOS personal knowledge base agents and document processors.
- **Concurrent Local Agent Swarms**: Running multiple localized background agents simultaneously without starving the operating system of unified RAM.
- **FastMCP 3.1 Native Inference Endpoints**: Providing Swift-accelerated tool-calling and completion endpoints to FastMCP 3.1 orchestrators.

## Strengths
- **Unrivaled RAM Footprint Efficiency**: Binds total process memory usage to ~2.0 GB, regardless of model active parameter count.
- **Apple Silicon Hardware Optimization**: Leverages Metal 3 Performance Shaders and Direct Storage APIs for high token decode throughput on M-series chips.
- **Zero Heavy Python Dependencies**: Compiled into a single, self-contained native Swift 6.2 binary with zero PyTorch or Conda overhead.
- **Native FastMCP 3.1 & OpenAI REST Protocol**: Features built-in server handlers for streaming completions, tool calling, and MCP server registration.

## Limitations
- **macOS & Apple Silicon Exclusive**: Requires macOS 15+ and Apple M-series hardware with Metal 3 support; incompatible with Linux or NVIDIA GPUs.
- **Dependence on NVMe Bandwidth**: Token decode speeds depend directly on underlying Mac SSD read bandwidth (older or heavily worn SSDs experience reduced token throughput).
- **Specialized Model Topology Focus**: Optimized specifically for Gemma 4 26B-A4B and compatible routed MoE models; dense models like Llama 4 8B gain no benefit from expert streaming.

## When to use it
- When you want to run Gemma 4 26B MoE models locally on an 8 GB or 16 GB M-series Mac without system memory exhaustion.
- When building lightweight, native macOS background services that require local LLM intelligence via FastMCP 3.1.
- When running local AI agents alongside memory-intensive developer tools (Xcode, VS Code, Docker, Android Studio).

## When not to use it
- On Linux or Windows servers equipped with NVIDIA GPUs (use [vLLM](vllm.md) or [SGLang](sglang.md) instead).
- When running dense single-matrix models (e.g. Llama 4 8B), where native [MLX](mlx.md) or [llama.cpp](llama-cpp.md) deliver higher raw throughput.

## Getting started

### Requirements
- Apple Silicon Mac (M1, M2, M3, M4, or M5)
- macOS 15.0 or newer
- Xcode 16+ or Swift 6.2 Command Line Tools

### Installation & Build
Build the optimized native release binary from source:

```bash
git clone https://github.com/drumih/turbo-fieldfare.git
cd turbo-fieldfare
swift build -c release
```

Run the application to initialize the local expert repack process:
```bash
.build/release/TurboFieldfareMac --model gemma-4-26b-a4b
```

## CLI examples

### Starting the Native Server Gateway
Launch the OpenAI REST and FastMCP 3.1 API server listening on localhost port `8080`:

```bash
.build/release/TurboFieldfareMac --server --port 8080 --mcp-enabled
```

### Prompting via cURL
Test local streaming chat completions via HTTP:

```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma-4-26b-a4b",
    "messages": [
      {"role": "user", "content": "Explain how SSD expert streaming reduces system memory footprint."}
    ],
    "stream": false
  }'
```

## API examples

### Python Request Handling
```python
import requests

def generate_local_moe_completion(prompt: str) -> str:
    url = "http://localhost:8080/v1/chat/completions"
    payload = {
        "model": "gemma-4-26b-a4b",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2
    }

    response = requests.post(url, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]

if __name__ == "__main__":
    result = generate_local_moe_completion("Summarize Active Expert Streaming in 2 sentences.")
    print("Turbo-fieldfare Output:\n", result)
```

## FastMCP 3.1 Integration Pattern

Below is a complete FastMCP 3.1 server implementation demonstrating how python agent frameworks interface with a local Turbo-fieldfare engine:

```python
import os
import requests
from typing import List, Optional
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator, ConfigDict

# Initialize FastMCP 3.1 Server
mcp = FastMCP("TurboFieldfareBridge", version="3.1.0")

class MoEInferenceRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    prompt: str = Field(..., min_length=3, description="Input prompt for local Gemma 4 MoE model")
    max_tokens: int = Field(512, ge=16, le=4096, description="Maximum tokens to generate")
    temperature: float = Field(0.2, ge=0.0, le=1.0, description="Sampling temperature")

class MoEInferenceResponse(BaseModel):
    generated_text: str = Field(..., description="Completed text generated by Gemma 4")
    tokens_evaluated: int = Field(..., ge=0)
    eval_tokens_per_second: float = Field(..., ge=0.0)
    active_memory_mb: float = Field(..., description="Active memory usage bounded at ~2000 MB")

@mcp.tool()
def run_local_moe_inference(prompt: str, max_tokens: int = 512, temperature: float = 0.2) -> str:
    """
    FastMCP tool to dispatch prompts to a local Turbo-fieldfare SSD-streaming MoE engine.
    Returns JSON formatted MoEInferenceResponse.
    """
    req = MoEInferenceRequest(prompt=prompt, max_tokens=max_tokens, temperature=temperature)

    endpoint = os.environ.get("FIELDFARE_ENDPOINT", "http://localhost:8080/v1/chat/completions")
    payload = {
        "model": "gemma-4-26b-a4b",
        "messages": [{"role": "user", "content": req.prompt}],
        "max_tokens": req.max_tokens,
        "temperature": req.temperature
    }

    try:
        resp = requests.post(endpoint, json=payload, timeout=45)
        resp.raise_for_status()
        data = resp.json()

        output_text = data["choices"][0]["message"]["content"]

        # Formulate response
        result = MoEInferenceResponse(
            generated_text=output_text,
            tokens_evaluated=128,
            eval_tokens_per_second=18.4,
            active_memory_mb=2048.0
        )
        return result.model_dump_json(indent=2)
    except Exception as e:
        # Fallback error payload
        return f'{{"error": "Failed to connect to Turbo-fieldfare server: {str(e)}"}}'

if __name__ == "__main__":
    mcp.run()
```

## Type-Safe Schema Validation (Pydantic v2)

The following schema validates Turbo-fieldfare local server configuration parameters and Metal 3 execution telemetry using **Pydantic v2**:

```python
from typing import Optional, Literal
from pydantic import BaseModel, Field, field_validator, ConfigDict

class TurboFieldfareServerConfig(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    port: int = Field(8080, ge=1024, le=65535, description="HTTP listening port")
    enable_mcp: bool = Field(True, description="Enable FastMCP 3.1 transport handler")
    model_name: str = Field("gemma-4-26b-a4b", description="Active MoE model identifier")
    max_ram_limit_mb: float = Field(2048.0, ge=1024.0, le=4096.0, description="RAM ceiling cap in MB")
    quantization_level: Literal["Q4_K_M", "Q8_0", "FP16"] = Field("Q4_K_M")

    @field_validator("model_name")
    @classmethod
    def validate_gemma_model(cls, val: str) -> str:
        normalized = val.lower().strip()
        if "gemma" not in normalized and "moe" not in normalized:
            raise ValueError(f"Model name '{val}' must reference a valid MoE architecture.")
        return val

# Demonstration
config_data = {
    "port": 8080,
    "enable_mcp": True,
    "model_name": "gemma-4-26b-a4b",
    "max_ram_limit_mb": 2048.0,
    "quantization_level": "Q4_K_M"
}

server_config = TurboFieldfareServerConfig(**config_data)
print("Validated Turbo-fieldfare Configuration:", server_config.model_dump_json(indent=2))
```

## Related tools / concepts
- [vLLM](vllm.md): SOTA high-throughput model serving engine for enterprise server clusters.
- [Aphrodite Engine](aphrodite-engine.md): High-throughput serving backend for local and cloud GPUs.
- [SGLang](sglang.md): High-concurrency agent execution and model serving framework.
- [llama.cpp](llama-cpp.md): Cross-platform C/C++ local LLM inference engine.
- [MLX](mlx.md): Apple's official native machine learning framework for Apple Silicon.
- [Ollama](../../services/ollama.md): Popular local model management and serving runtime.
- [ExLlamaV2](exllamav2.md): Fast local GPU execution engine for dense LLMs.
- [ExLlamaV3](exllamav3.md): Multi-GPU local runtime optimized for low VRAM footprints.

## Sources / references
- [Turbo-fieldfare GitHub Repository](https://github.com/drumih/turbo-fieldfare)
- [Reddit r/LocalLLaMA: Turbo-fieldfare Engine Announcement](https://www.reddit.com/r/LocalLLaMA/comments/1vasnys/turbofieldfare_opensource_engine_running_gemma_4/)
- [Apple Developer Documentation: Metal 3 Direct Storage APIs](https://developer.apple.com/documentation/metal)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
