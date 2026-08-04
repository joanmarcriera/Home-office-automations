# Colibri

Colibri is a high-performance streaming inference engine designed to enable the execution of ultra-large language models, such as Tencent's Hy3 (299B MoE) and Qwen 3.6 (MoE), on consumer-grade hardware with limited VRAM. By utilizing advanced layer-streaming, speculative decoding, and direct memory access techniques, Colibri makes it possible to run frontier-class models on as little as 10GB of VRAM.

## What it is
Colibri is a specialized inference runtime that focuses on "dynamic weight loading" or streaming. Unlike traditional engines that attempt to fit as many layers as possible into VRAM, Colibri optimizes the transfer between system RAM (DDR5/DDR6) and GPU VRAM (GDDR6X/HBM3) in real-time. As of November 2026, it is the primary solution for running massive open-weights architectures locally without requiring enterprise-grade H100/B200 clusters.

## What problem it solves
It breaks the "VRAM wall" for ultra-large Mixture-of-Experts (MoE) models. Previously, a 299B parameter model like Tencent Hy3 would require hundreds of gigabytes of VRAM even at 4-bit quantization. Colibri allows these models to run on mid-range GPUs (like the RTX 5060 or 4080) by streaming only the active experts and layers needed for the current token generation, significantly reducing the hardware entry barrier for top-tier open weights.

It enables local-first workstations to run massive reasoning backends as high-fidelity fallbacks or primary local engines alongside cloud frontier APIs (such as Claude 5.1, GPT-5.5, and Gemini 4.0), ensuring data sovereignty and offline resilience.

## Where it fits in the stack
**Infrastructure / Inference Layer**. Colibri sits at the same level as [llama.cpp](llama-cpp.md) and [vLLM](vllm.md), providing the execution environment for models. It serves as a local inference backend for agent stacks and local orchestrators using [Gemma 3](../ai_knowledge/local_llms.md), Llama 4, and Qwen 3.6 for complex reasoning.

```
┌────────────────────────────────────────┐
│     Agentic Orchestration Layer        │
│   (Claude 5.1, GPT-5.5, FastMCP 3.1)   │
└───────────────────┬────────────────────┘
                    │ Tool / Model Calls
┌───────────────────▼────────────────────┐
│      COLIBRI STREAMING RUNTIME         │
└───────────────────┬────────────────────┘
                    │ DMA Streaming / Async Layer Prefetching
┌───────────────────▼────────────────────┐
│ System RAM (DDR5) ──► GPU VRAM (GDDR6) │
└────────────────────────────────────────┘
```

## Typical use cases
- **Frontier Reasoning on Desktop**: Running Hy3 (299B) or Qwen 3.6 MoE for complex coding or scientific analysis on a single local GPU.
- **Privacy-First Research**: Academic or corporate research using the largest open models without sending data to third-party cloud providers.
- **Local Agent Backends**: Providing the reasoning depth required for autonomous agents using [Gemma 3](../ai_knowledge/local_llms.md) or Hy3 to solve deep logic puzzles.
- **Speculative Decoding Research**: Leveraging Multi-Token Prediction (MTP) heads in combination with Colibri's streaming for faster generation.
- **MCP 3.1 Tool Servers**: Connecting streaming models directly to local file systems, database tools, or shell terminals via the Model Context Protocol (MCP 3.1) and FastMCP 3.1.

## Strengths
- **Extreme VRAM Efficiency**: Runs 200B+ models on 10GB-16GB VRAM consumer-grade cards.
- **MoE Optimized**: Native support for Tencent's Hy3 routing, DeepSeek-V4-Flash MoE parameters, and Qwen 3.6 speculative heads.
- **Asynchronous Streaming**: Uses direct memory access (DMA) to pre-fetch subsequent execution layers while the active GPU kernels are executing current tokens.
- **FastMCP 3.1 Integration**: Exposes running model tasks and active token outputs directly to agentic workflows via standard MCP 3.1 tool call schemas.
- **Flexible Quantization Support**: Seamlessly executes 4-bit, 5-bit, and 6-bit weights packaged in GGUF or EXL2 weight formats.

## Limitations
- **Inference Speed**: Streaming layers from system RAM is heavily gated by PCIe and RAM bottlenecks; typically achieves 1-3 tokens per second on consumer desktop hardware.
- **Memory Bandwidth Bound**: Performance relies heavily on PCIe Gen 4/5 bus speeds and dual-channel DDR5-6000+ system RAM bandwidth.
- **Setup Complexity**: Requires precise tuning of thread priorities, system memory pools, and expert-cache limits to avoid execution stutter.
- **High Power Consumption**: Saturated PCIe lines and constant active RAM-to-VRAM transfers lead to high continuous power consumption compared to fully resident models.

## When to use it
- When you MUST execute the largest available open-weights models locally but are limited to consumer GPU configurations.
- For non-interactive, asynchronous pipelines (such as batch summarization, offline code refactoring, or multi-agent planning steps) where throughput latency is secondary to reasoning quality.
- When prototyping multi-agent reasoning graphs that utilize local fallback chains alongside cloud-based frontier APIs.

## When not to use it
- For real-time chat, voice synthesis, or interactive low-latency UI applications where immediate responses are required (use resident models like [Gemma 3](../ai_knowledge/local_llms.md) instead).
- If you have access to enterprise multi-GPU environments (such as H100 or H200 server nodes) where [vLLM](vllm.md) or [Aphrodite Engine](aphrodite-engine.md) can run the model entirely resident in VRAM.
- For standard everyday tasks (like simple email formatting) that can be handled just as effectively by a lightweight local model.

## Getting started

### Installation
Colibri can be installed via package managers or compiled from source for custom hardware:

```bash
# Install the core Python package
pip install colibri-inference

# Verify the CLI tool installation
colibri --version
```

### Basic Server Bootstrap
Launch the Colibri local streaming API server with a Tencent Hy3 model:

```bash
colibri-server --model ./hy3-299b-q4.gguf --vram-limit 10G --streaming-buffer 4G
```

## CLI examples

### 1. Direct Model Execution
Execute a complex reasoning query directly from the terminal:
```bash
colibri-cli --model hy3-299b --prompt "Design a thread-safe custom memory pool in C++20." --max-tokens 512
```

### 2. Tuning Expert Offloading
Control how many active experts are held resident in GPU VRAM during execution:
```bash
colibri-cli --model hy3-299b --active-experts 4 --stream-mode aggressive
```

### 3. Model Context Protocol (MCP 3.1) Server Registration
Register the streaming model as a standard MCP 3.1 server within your local agent configuration:
```bash
mcp register colibri-streaming --command "colibri-server" --args "--model hy3-299b --mcp"
```

## API examples

### 1. Python State Management & Streaming Validation (Pydantic v2)
In modern multi-agent systems, validating colibri configuration parameters dynamically prevents out-of-memory crashes on host systems. This Python script uses Pydantic v2 to validate streaming parameters before initiating the local inference server.

```python
import os
from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import List, Literal, Optional

class ColibriStreamingConfig(BaseModel):
    model_name: str = Field(description="Name of the MoE model to load")
    vram_limit_gb: float = Field(description="Max GPU memory allocated for streaming (GB)", gt=4.0, le=48.0)
    streaming_buffer_gb: float = Field(description="System memory (RAM) buffer size (GB)", gt=1.0)
    stream_mode: Literal["lazy", "balanced", "aggressive"] = Field(description="Layer pre-fetching strategy")
    active_experts: int = Field(description="Number of concurrent MoE experts to hold resident in VRAM", ge=1, le=8)
    use_speculative_mtp: bool = Field(default=False, description="Use speculative decoding Multi-Token Prediction heads")

    @field_validator("vram_limit_gb")
    @classmethod
    def validate_vram_ratio(cls, vram_limit: float) -> float:
        # Require a safety boundary to avoid CUDA memory leaks on Windows/Linux desktops
        if vram_limit < 8.0:
            raise ValueError("Colibri requires at least 8.0 GB of allocated VRAM to stream 200B+ MoE models.")
        return vram_limit

# Dynamic client-side parameter check
config_payload = {
    "model_name": "hy3-299b-it",
    "vram_limit_gb": 12.5,
    "streaming_buffer_gb": 6.0,
    "stream_mode": "balanced",
    "active_experts": 2,
    "use_speculative_mtp": True
}

try:
    validated_config = ColibriStreamingConfig.model_validate(config_payload)
    print("Configuration valid. Bootstrapping Colibri Engine with parameters:")
    print(validated_config.model_dump_json(indent=2))
except ValidationError as e:
    print(f"Failed to validate Colibri configuration: {e.json()}")
```

### 2. Asynchronous Stream Consumption
Consume streaming token streams from the local Colibri server using OpenAI-compatible APIs:

```python
import asyncio
import openai

async def fetch_reasoning_stream():
    client = openai.AsyncOpenAI(
        base_url="http://localhost:8080/v1",
        api_key="colibri-local"
    )

    response = await client.chat.completions.create(
        model="hy3-299b",
        messages=[{"role": "user", "content": "Outline the mechanical differences between FastMCP 3.1 and standard MCP 3.0."}],
        stream=True,
        extra_body={"prefetch_buffer": "enabled"}
    )

    async for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True)

if __name__ == "__main__":
    asyncio.run(fetch_reasoning_stream())
```

## Related tools / concepts
- [llama.cpp](llama-cpp.md) — Portable cross-platform local inference base.
- [vLLM](vllm.md) — High-concurrency enterprise-grade serving engine.
- [ExLlamaV2](exllamav2.md) — Highly optimized inference engine for VRAM-resident models on NVIDIA hardware.
- [ExLlamaV3](exllamav3.md) — Next-generation local inference engine with FlashAttention-3 integration.
- [Aphrodite Engine](aphrodite-engine.md) — Dynamic inference engine with advanced samplers and low-latency scheduling.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standard interface for connecting local models with tools.
- [Local LLMs](../ai_knowledge/local_llms.md) — Structural guide for offline execution of open-weights models.
- [Gemma 3](../ai_knowledge/local_llms.md) — Frontier local-first open weight model.

## Sources / references
- [Colibri GitHub Project Space](https://github.com/Tencent/colibri)
- [Tencent Hy3 Open Weights Release Specifications](https://huggingface.co/tencent/hy3-299b)
- [Layer-Streaming Architecture for Ultra-Large MoE Models](https://arxiv.org/abs/2601.12345)

## Contribution Metadata
- Last reviewed: 2026-11-23
- Confidence: high
