# Mellum2

Mellum2 is a high-efficiency open-weights large language model (LLM) that leverages Multi-Token Prediction (MTP) architecture to significantly accelerate inference and improve reasoning coherence. As of July 2026, Mellum2 is recognized for its ability to generate high-quality code and text with a substantially lower latency compared to traditional next-token prediction models.

## What it is
Mellum2 is the second-generation model from the Mellum series, specifically optimized for speed without sacrificing intelligence. Its core innovation, Multi-Token Prediction, allows the model to predict multiple future tokens in parallel during a single inference pass. This architecture, coupled with native support for the [Model Context Protocol (MCP) 3.0](../automation_orchestration/mcp.md), makes it a powerful engine for real-time agentic workflows.

## What problem it solves
It addresses the "inference bottleneck" in local LLM deployments. Standard autoregressive models predict tokens one-by-one, which can be slow on consumer hardware. Mellum2's MTP approach increases tokens-per-second (TPS) throughput and improves the model's "lookahead" capabilities, leading to better structural consistency in complex outputs like JSON or long-form code.

## Where it fits in the stack
**Reasoning & Execution Layer**. Mellum2 acts as a primary reasoning engine for local-first AI agents. It is typically hosted via [vLLM](../infrastructure/vllm.md) or [llama.cpp](../infrastructure/llama-cpp.md) and serves requests from orchestration frameworks like [LangGraph](../frameworks/langgraph.md) or [Smolagents](../frameworks/smolagents.md).

## Typical use cases
- **Low-Latency Chat**: Real-time conversational assistants where response time is critical.
- **Agentic Tool Use**: Fast reasoning for agents that need to call multiple MCP tools in sequence.
- **Local Code Generation**: Autocompletion and refactoring tasks in [VS Code](../development_ops/vscode.md) using [Continue.dev](../development_ops/continue_dev.md).
- **Embedded Reasoning**: Running sophisticated logic on high-end edge devices (e.g., Mac Studio, NVIDIA RTX 50-series).

## Strengths
- **High Throughput**: MTP architecture delivers up to 2x faster inference speeds than equivalent single-token prediction models.
- **Better Planning**: Multi-token lookahead reduces the likelihood of the model "painting itself into a corner" during complex reasoning.
- **MCP 3.0 Native**: Built-in support for the latest Task Protocol, allowing for seamless integration with modern MCP servers.
- **Quantization Friendly**: Maintains high accuracy even at 4-bit and 6-bit quantization levels (GGUF/EXL2).

## Limitations
- **Hardware Requirements**: While efficient, the MTP architecture benefits significantly from high memory bandwidth (VRAM).
- **Niche Architecture**: Some legacy inference engines may require specific patches to fully exploit the multi-token prediction heads.
- **Context Window**: While generous (128k), it is currently surpassed by frontier models like [Claude 5.1](claude.md) in ultra-long document analysis.

## When to use it
- When you require the fastest possible response times for a local LLM.
- For coding tasks where structural correctness and speed are paramount.
- When building agents that rely on frequent, small reasoning steps.
- As a local alternative to [Gemma 3](local_llms.md) for specialized low-latency tasks.

## When not to use it
- If you have extremely limited VRAM (e.g., < 8GB), smaller 1B-3B models may be more appropriate.
- For massive-scale document summarization exceeding 128k tokens.
- If your inference stack does not yet support the specialized MTP heads for acceleration.

## Getting started

### Installation via Ollama
As of July 2026, Mellum2 is available in the official Ollama library.

```bash
ollama run mellum2
```

### Local Hosting with vLLM
To leverage full MTP acceleration, vLLM is recommended:

```bash
python -m vllm.entrypoints.openai.api_server \
    --model mellum-ai/mellum2-8b \
    --enable-mtp \
    --tensor-parallel-size 1
```

## CLI examples
Using the Mellum CLI (included with the `mellum-tools` package).

```bash
# Basic query
mellum chat "Explain quantum entanglement in one sentence."

# Generate code and save to file
mellum code "Write a Python script to monitor CPU usage" > monitor.py

# Check model info and MTP status
mellum info --model mellum2
```

## API examples

### Python (OpenAI-compatible)
Mellum2 supports standard OpenAI-compatible API calls.

```python
import openai

client = openai.OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="not-needed"
)

response = client.chat.completions.create(
    model="mellum2",
    messages=[{"role": "user", "content": "How does MTP work?"}],
    extra_body={"use_mtp": True} # Enable MTP acceleration
)

print(response.choices[0].message.content)
```

### FastMCP Integration
Integrating Mellum2 as a reasoning engine for an MCP server.

```python
from fastmcp import FastMCP

mcp = FastMCP("MellumHelper")

@mcp.tool()
def summarize_fast(text: str) -> str:
    """Summarizes text using Mellum2's low-latency engine."""
    # Logic to call Mellum2 locally
    return "Summary generated by Mellum2..."
```

## Related tools / concepts
- [Multi-Token Prediction (MTP)](../../knowledge_base/model_classes.md) — The underlying architecture.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Orchestration protocol.
- [Gemma 3](local_llms.md) — Complementary open-weights model.
- [vLLM](../infrastructure/vllm.md) — Recommended high-performance inference engine.
- [LlamaIndex](llamaindex.md) — For RAG implementations.

## Sources / references
- [Mellum2 Announcement on Reddit](https://www.reddit.com/r/LocalLLaMA/comments/1uv4y2n/mellum2_with_mtp/)
- [Mellum AI Official Repository](https://github.com/mellum-ai/mellum2)
- [Understanding Multi-Token Prediction (Research Paper)](https://arxiv.org/abs/2404.19737)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
