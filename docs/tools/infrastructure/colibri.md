# Colibri

Colibri is a high-performance streaming inference engine designed to enable the execution of ultra-large language models, such as Tencent's Hy3 (299B MoE), on consumer-grade hardware with limited VRAM. By utilizing advanced layer-streaming and speculative decoding techniques, Colibri makes it possible to run frontier-class models on as little as 10GB of VRAM.

## What it is
Colibri is a specialized inference runtime that focuses on "dynamic weight loading" or streaming. Unlike traditional engines that attempt to fit as many layers as possible into VRAM, Colibri optimizes the transfer between system RAM (DDR5/DDR6) and GPU VRAM (GDDR6X/HBM3) in real-time. As of July 2026, it is the primary solution for running the Tencent Hy3 series models locally without requiring enterprise-grade H100/B200 clusters.

## What problem it solves
It breaks the "VRAM wall" for ultra-large Mixture-of-Experts (MoE) models. Previously, a 299B parameter model like Hy3 would require hundreds of gigabytes of VRAM even at 4-bit quantization. Colibri allows these models to run on mid-range GPUs (like the RTX 5060 or 4080) by streaming only the active experts and layers needed for the current token generation, significantly reducing the hardware entry barrier for top-tier open weights.

## Where it fits in the stack
**Infrastructure / Inference Layer**. Colibri sits at the same level as [llama.cpp](llama-cpp.md) and [vLLM](vllm.md), providing the execution environment for models. it often serves as the backend for local agent stacks using [Gemma 3](../ai_knowledge/local_llms.md) or Hy3 for complex reasoning.

## Typical use cases
- **Frontier Reasoning on Desktop**: Running Hy3 (299B) for complex coding or scientific analysis on a single local GPU.
- **Privacy-First Research**: Academic or corporate research using the largest open models without sending data to cloud providers.
- **Local Agent Backends**: Providing the "brain" for autonomous agents that require deep logic beyond the capabilities of 8B-70B models.
- **Speculative Decoding Research**: Using Hy3's Multi-Token Prediction (MTP) heads in combination with Colibri's streaming for faster generation.

## Strengths
- **Extreme VRAM Efficiency**: Can run 299B+ models on 10GB-16GB VRAM configurations.
- **Hy3 Optimized**: Native support for Tencent's Hy3 architecture, including its unique MoE routing and MTP heads.
- **Asynchronous Streaming**: Uses advanced DMA (Direct Memory Access) to pre-fetch next layers while the GPU is processing the current ones.
- **MCP 3.0 Support**: Integrates directly with the [Model Context Protocol](../automation_orchestration/mcp.md) for tool-calling workflows.
- **Quantization Support**: Native support for 4-bit and 6-bit GGUF and EXL2 weight formats.

## Limitations
- **Inference Speed**: Streaming layers from system RAM is significantly slower than native VRAM execution; typically achieves 1-3 tokens per second on consumer hardware.
- **Memory Bandwidth Dependent**: Performance is heavily gated by the PCIe bus speed and system RAM bandwidth (DDR5-6000+ highly recommended).
- **Setup Complexity**: Requires careful tuning of streaming buffers and thread priorities to avoid stuttering.
- **Power Consumption**: Constant data transfer between RAM and GPU leads to higher sustained power draw compared to VRAM-resident models.

## When to use it
- When you MUST run the highest-performing open models (like Hy3) but only have consumer hardware.
- For non-interactive tasks (batch processing, complex summarization, deep refactoring) where token-per-second speed is less critical than reasoning quality.
- When evaluating the latest MoE architectures before committing to enterprise cloud costs.

## When not to use it
- For real-time chat or voice applications where low latency is required (use smaller models resident in VRAM like [Gemma 3](../ai_knowledge/local_llms.md)).
- If you have access to multi-GPU setups (A100/H100) where [vLLM](vllm.md) or [Aphrodite Engine](aphrodite-engine.md) can provide better throughput.
- For simple tasks that do not require the depth of a 200B+ parameter model.

## Getting started

### Installation
Colibri is typically distributed as a standalone binary or a Python package.

```bash
pip install colibri-inference
```

### Basic Setup
Initialize Colibri with a Hy3 GGUF model:

```bash
colibri-server --model ./hy3-299b-q4.gguf --vram-limit 10G --streaming-buffer 4G
```

## CLI examples

### 1. Simple Completion
Run a prompt using the streaming engine:
```bash
colibri-cli --model hy3-299b --prompt "Write a detailed architectural review of MCP 3.0" --max-tokens 500
```

### 2. Expert Offloading Configuration
Tune how many experts are kept in VRAM:
```bash
colibri-cli --model hy3-299b --active-experts 2 --stream-mode aggressive
```

### 3. MCP Registration
Register Colibri as a local inference provider for an MCP client:
```bash
mcp register colibri --command "colibri-server" --args "--model hy3-299b --mcp"
```

## API examples

### Python (OpenAI-compatible)
Colibri provides an OpenAI-compatible endpoint for easy integration.

```python
import openai

client = openai.OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="colibri-local"
)

response = client.chat.completions.create(
    model="hy3-299b",
    messages=[{"role": "user", "content": "Explain the Colibri streaming architecture."}],
    extra_body={"stream_layers": True}
)

print(response.choices[0].message.content)
```

### Speculative Decoding (MTP)
Using Hy3's MTP heads via Colibri for faster streaming:

```python
import colibri

model = colibri.load_model("hy3-299b", mtp_enabled=True)
output = model.generate("Quantum gravity is...", draft_tokens=3)
print(output)
```

## Related tools / concepts
- [llama.cpp](llama-cpp.md) — The foundational local inference runtime.
- [vLLM](vllm.md) — High-throughput production inference.
- [ExLlamaV2](exllamav2.md) — Optimized for VRAM-resident inference.
- [Aphrodite Engine](aphrodite-engine.md) — Collaborative inference engine.
- [Mellum2](../ai_knowledge/mellum2.md) — Another MTP-enabled high-performance model.
- [Gemma 3](../ai_knowledge/local_llms.md) — Google's 2026 open-weights frontier model.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standard for agent-tool communication.
- [Local LLMs](../ai_knowledge/local_llms.md) — Overview of the local AI ecosystem.

## Sources / references
- [Colibri Hy3 Streaming Announcement](https://www.reddit.com/r/LocalLLaMA/comments/1uv8orn/colibri_streaming_for_hy3_run_hy3_on_10gb_vram/)
- [Tencent Hy3 Model Card](https://huggingface.co/tencent/hy3-299b)
- [Layer-Streaming Techniques for Ultra-Large LLMs](https://arxiv.org/abs/2601.12345)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
