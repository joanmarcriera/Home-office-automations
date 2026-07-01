# Fireworks AI

## What it is
Fireworks AI is a high-performance inference platform providing an ultra-fast API for running and fine-tuning open-source generative AI models (Llama 4, Gemma 3, Qwen 2.5). As of July 2026, it is recognized for its proprietary "FireAttention" optimization stack and full support for the **MCP 3.0 Task Protocol**, which allows for standardized, automated benchmarking of frontier open-weights models.

## What problem it solves
It provides reliable, low-latency, and cost-effective access to the latest open-source models, eliminating the performance overhead of standard GPU deployments and the complexity of managing private inference infrastructure. It solves the "speed-to-token" bottleneck for real-time agentic workflows.

## Where it fits in the stack
**Inference Provider**. Fireworks AI sits in the **Infrastructure** layer, providing the raw compute and model serving capability that powers higher-level agentic frameworks. It serves as a performance-optimized alternative to self-hosting via [vLLM](../infrastructure/vllm.md) or using general-purpose providers like [Together AI](together.md).

## Typical use cases
- **Automated Benchmarking**: Leveraging the **MCP 3.0 Task Protocol** to perform high-throughput evaluation of models like Gemma 3 and Llama 4.
- **High-Throughput Applications**: Production apps requiring many concurrent, low-latency LLM requests for real-time interaction.
- **Function Calling**: Using optimized models for reliable structured data extraction and autonomous tool use.
- **Custom Model Deployment**: Deploying specialized fine-tuned models on dedicated, scalable infrastructure via LoRA adapters.
- **Real-time Agents**: Powering agents that require immediate reasoning responses to maintain conversation flow.

## Strengths
- **Extreme Speed**: The FireAttention engine provides exceptionally high throughput and low time-to-first-token (TTFT).
- **Gemma 3 Optimization**: Native support and hardware-level optimizations for the Gemma 3 model family.
- **LoRA Support**: Native, first-class support for deploying and switching between custom LoRA adapters with zero cold-start latency.
- **MCP 3.0 Integration**: Standardized integration for automated task execution and monitoring via the [Model Context Protocol (MCP)](../automation_orchestration/mcp.md).
- **Developer Experience**: Fully OpenAI-compatible API ensures seamless migration from other providers.

## Limitations
- **Focus**: Prioritizes performance for a curated set of models rather than hosting every niche model available on Hugging Face.
- **Proprietary Optimizations**: While models are open-weights, the underlying FireAttention stack is proprietary.
- **Cloud-Only**: Does not offer a standalone local version for completely offline environments (see [vLLM](../infrastructure/vllm.md)).

## When to use it
- When you need the fastest possible inference for Llama 4, Gemma 3, or other top-tier open models.
- For high-volume production applications where reliability and consistent latency are critical.
- When you need to deploy and manage multiple fine-tuned LoRA adapters efficiently.
- When building real-time interactive agents using [Model Context Protocol (MCP)](../automation_orchestration/mcp.md).

## When not to use it
- If your application requires proprietary "frontier" models like `claude-4-8-opus-20260528`.
- For extremely niche or research models that are not included in their curated performance-optimized list.
- If strict data sovereignty requires 100% on-premises local hosting (see [TGI](../infrastructure/tgi.md)).

## Getting started
To start using Fireworks AI, install the official Python SDK:

```bash
pip install fireworks-ai
```

Initialize the client and run a basic chat completion:

```python
import fireworks.client
import os

fireworks.client.api_key = os.environ["FIREWORKS_API_KEY"]

response = fireworks.client.ChatCompletion.create(
    model="accounts/fireworks/models/gemma-3-27b-it",
    messages=[{"role": "user", "content": "Hello Fireworks! Tell me about Gemma 3."}]
)
print(response.choices[0].message.content)
```

## CLI examples
The Fireworks API is OpenAI-compatible and can be easily tested via `curl`.

### 1. Basic Chat Completion
```bash
curl https://api.fireworks.ai/inference/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $FIREWORKS_API_KEY" \
  -d '{
    "model": "accounts/fireworks/models/llama-v4-70b-instruct",
    "messages": [{"role": "user", "content": "Compare PagedAttention and FireAttention."}]
  }'
```

### 2. List Available Models
```bash
curl https://api.fireworks.ai/inference/v1/models \
  -H "Authorization: Bearer $FIREWORKS_API_KEY"
```

### 3. Embeddings Request
```bash
curl https://api.fireworks.ai/inference/v1/embeddings \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $FIREWORKS_API_KEY" \
  -d '{
    "model": "accounts/fireworks/models/nomic-embed-text-v1.5",
    "input": ["Indexing this for low-latency retrieval."]
  }'
```

## API examples

### Structured Output (Function Calling)
Fireworks supports function calling via Pydantic or JSON schemas for reliable data extraction.

```python
from pydantic import BaseModel
import fireworks.client
import os

fireworks.client.api_key = os.environ["FIREWORKS_API_KEY"]

class ToolOutput(BaseModel):
    action: str
    priority: int

response = fireworks.client.ChatCompletion.create(
    model="accounts/fireworks/models/gemma-3-27b-it",
    messages=[{"role": "user", "content": "Task: Update database, Priority: 1"}],
    response_format={"type": "json_object", "schema": ToolOutput.model_json_schema()}
)
print(response.choices[0].message.content)
```

### LoRA Adapter Usage
Deploying a custom adapter over a base model.

```python
import fireworks.client
import os

fireworks.client.api_key = os.environ["FIREWORKS_API_KEY"]

response = fireworks.client.ChatCompletion.create(
    model="accounts/your-account/models/your-base-model",
    extra_body={"lora_adapter": "accounts/your-account/models/your-adapter-id"},
    messages=[{"role": "user", "content": "Generate code in my specific style."}]
)
```

## Related tools / concepts
- [Groq](groq.md) — Low-latency LPU-based inference provider.
- [Together AI](together.md) — Comprehensive serverless inference platform.
- [Mistral](mistral.md) — High-performance model family often hosted on Fireworks.
- [vLLM](../infrastructure/vllm.md) — Open-source inference engine for self-hosting.
- [TGI](../infrastructure/tgi.md) — Hugging Face's production inference server.
- [SGLang](../infrastructure/sglang.md) — High-throughput runtime for LLMs.
- [OpenRouter](../ai_knowledge/openrouter.md) — Unified model access gateway.
- [LiteLLM](../../services/litellm.md) — Proxy for unified API calls.
- [Local LLMs](../ai_knowledge/local_llms.md) — Guide for running Llama 4 and Gemma 3 locally.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standardized agent communication protocol.

## Sources / references
- [Official Website](https://fireworks.ai/)
- [Fireworks AI Docs](https://docs.fireworks.ai/)
- [Model Directory](https://fireworks.ai/models)
- [FireAttention Benchmarks](https://fireworks.ai/blog/fireattention)
- [MCP 3.0 Task Protocol Specification](https://modelcontextprotocol.io/3.0/task-protocol)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
