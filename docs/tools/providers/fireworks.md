# Fireworks AI

## What it is
Fireworks AI is a high-performance inference platform providing an ultra-fast API for running and fine-tuning open-source generative AI models (Llama 4 Maverick, Gemma 4, Qwen 3.6 VL, DeepSeek-V4). As of early 2027, it is recognized for its proprietary "FireAttention" optimization stack and full support for the **FastMCP 3.1 Task Protocol**, which allows for standardized, automated benchmarking and seamless tool-calling of frontier open-weights models.

## What problem it solves
It provides reliable, low-latency, and cost-effective access to the latest open-source models, eliminating the performance overhead of standard GPU deployments and the complexity of managing private inference infrastructure. It solves the "speed-to-token" bottleneck for real-time agentic workflows.

## Architecture & FireAttention Execution Topology

```
+-----------------------------------------------------------------------------------+
|                           FastMCP 3.1 / OpenAI Client Ingress                     |
|   +-------------------+     +-------------------+     +-----------------------+   |
|   |  Claude Code CLI  |     | LangChain/Llama   |     | Agentic Tool Routers  |   |
|   +---------+---------+     +---------+---------+     +-----------+-----------+   |
|             |                         |                           |               |
|             +-------------------------+---------------------------+               |
|                                       |                                           |
|                                       v                                           |
|                     +-----------------------------------+                         |
|                     | Fireworks OpenAI-Compatible API   |                         |
|                     | (v1/chat/completions & MCP 3.1)   |                         |
|                     +-----------------+-----------------+                         |
+---------------------------------------|-------------------------------------------+
                                        |
                                        v
+-----------------------------------------------------------------------------------+
|                      FireAttention Optimized Runtime Engine                       |
|   +-------------------+     +-------------------+     +-----------------------+   |
|   | Continuous Batch  |     | Zero-Cold-Start   |     | Paged KV-Cache Engine |   |
|   |  Scheduler Engine |     | Multi-LoRA Router |     | (FP8/INT4 Quantization|   |
|   +---------+---------+     +---------+---------+     +-----------+-----------+   |
+---------------------------------------|-------------------------------------------+
                                        |
                   +--------------------+--------------------+
                   |                                         |
                   v                                         v
+------------------------------------+    +------------------------------------+
| Dedicated / Shared Tensor Core GPU |    | Multi-LoRA Custom Fine-Tune Store  |
| Cluster (H100/H200/B200 Accelerators)|  | (Dynamic NVMe Adapter Injection)   |
+------------------------------------+    +------------------------------------+
```

## Where it fits in the stack
**Inference Provider**. Fireworks AI sits in the **Infrastructure** layer, providing the raw compute and model serving capability that powers higher-level agentic frameworks. It serves as a performance-optimized alternative to self-hosting via [vLLM](../infrastructure/vllm.md) or using general-purpose providers like [Together AI](together.md).

## Feature & Performance Comparison Matrix

| Provider / Metric | Fireworks AI | Groq | Together AI | vLLM (Self-Hosted) | Anyscale / Ray |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Inference Engine** | FireAttention Core | LPU Hardware Engine | vLLM / FlashAttention | Open-Source vLLM | Ray Serve Core |
| **Multi-LoRA Serving** | Zero Cold-Start Native | N/A (Static Models) | Supported | Supported | Supported |
| **FastMCP 3.1 Native** | Full Support | Webhook Bridges | Community Drivers | Native FastMCP Wrapper | Ray MCP Adapter |
| **Time-To-First-Token** | 12ms – 25ms | 5ms – 15ms | 30ms – 60ms | Hardware Dependent | 25ms – 50ms |
| **Max Context Window** | 128k – 1M Tokens | 8k – 128k Tokens | 128k Tokens | Configurable | Configurable |
| **Custom Model Support**| Direct Fine-Tune Upload| Limited | Supported | Full Local Access | Full Cluster Access |

## Typical use cases
- **Automated Benchmarking**: Leveraging the **FastMCP 3.1 Task Protocol** to perform high-throughput evaluation of models like Gemma 4, Qwen 3.6 VL, DeepSeek-V4, and Llama 4 Maverick.
- **High-Throughput Applications**: Production apps requiring many concurrent, low-latency LLM requests for real-time interaction.
- **Function Calling**: Using optimized models for reliable structured data extraction and autonomous tool use.
- **Custom Model Deployment**: Deploying specialized fine-tuned models on dedicated, scalable infrastructure via LoRA adapters.
- **Real-time Agents**: Powering agents that require immediate reasoning responses to maintain conversation flow.

## Strengths
- **Extreme Speed**: The FireAttention engine provides exceptionally high throughput and low time-to-first-token (TTFT).
- **Gemma 4 & DeepSeek-V4 Optimization**: Native support and hardware-level optimizations for the Gemma 4 model family and DeepSeek-V4.
- **LoRA Support**: Native, first-class support for deploying and switching between custom LoRA adapters with zero cold-start latency.
- **FastMCP 3.1 Integration**: Standardized integration for automated task execution and monitoring via the [Model Context Protocol (MCP)](../automation_orchestration/mcp.md).
- **Developer Experience**: Fully OpenAI-compatible API ensures seamless migration from other providers.

## Limitations
- **Focus**: Prioritizes performance for a curated set of models rather than hosting every niche model available on Hugging Face.
- **Proprietary Optimizations**: While models are open-weights, the underlying FireAttention stack is proprietary.
- **Cloud-Only**: Does not offer a standalone local version for completely offline environments (see [vLLM](../infrastructure/vllm.md)).

## When to use it
- When you need the fastest possible inference for Llama 4 Maverick, Gemma 4, DeepSeek-V4, or other top-tier open models.
- For high-volume production applications where reliability and consistent latency are critical.
- When you need to deploy and manage multiple fine-tuned LoRA adapters efficiently.
- When building real-time interactive agents using [Model Context Protocol (MCP)](../automation_orchestration/mcp.md).

## When not to use it
- If your application requires proprietary "frontier" models like `claude-5-6-sonnet` or `gpt-5-6`.
- For extremely niche or research models that are not included in their curated performance-optimized list.
- If strict data sovereignty requires 100% on-premises local hosting (see [TGI](../infrastructure/tgi.md)).

## Getting started
To start using Fireworks AI, install the official Python SDK or use the OpenAI-compatible SDK:

```bash
pip install fireworks-ai pydantic openai fastmcp
```

Initialize the client and run a basic chat completion:

```python
import os
from openai import OpenAI

# Fireworks AI is fully OpenAI-compatible.
client = OpenAI(
    base_url="https://api.fireworks.ai/inference/v1",
    api_key=os.environ.get("FIREWORKS_API_KEY", "mock-key")
)

response = client.chat.completions.create(
    model="accounts/fireworks/models/gemma-4-31b-it",
    messages=[{"role": "user", "content": "Hello Fireworks! Tell me about Gemma 4."}]
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
    "model": "accounts/fireworks/models/llama-v4-maverick-70b-instruct",
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

### FastMCP 3.1 Inference Provider Server

```python
import os
from typing import List, Optional
from fastmcp import FastMCP
from pydantic import BaseModel, Field
from openai import OpenAI

mcp = FastMCP("Fireworks FastMCP Server", version="3.1.0")

class FireworksPromptInput(BaseModel):
    task_id: str = Field(..., description="FastMCP 3.1 Task Protocol correlation string")
    model: str = Field(default="accounts/fireworks/models/llama-v4-maverick-70b-instruct", description="Fireworks model path")
    prompt: str = Field(..., description="User prompt text")
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)

class FireworksPromptOutput(BaseModel):
    task_id: str
    model: str
    completion: str

@mcp.tool()
def generate_completion(params: FireworksPromptInput) -> FireworksPromptOutput:
    """Invokes Fireworks AI open-weights inference engine via FastMCP 3.1 tool call."""
    client = OpenAI(
        base_url="https://api.fireworks.ai/inference/v1",
        api_key=os.environ.get("FIREWORKS_API_KEY", "mock-key")
    )

    response = client.chat.completions.create(
        model=params.model,
        messages=[{"role": "user", "content": params.prompt}],
        temperature=params.temperature
    )

    return FireworksPromptOutput(
        task_id=params.task_id,
        model=params.model,
        completion=response.choices[0].message.content or ""
    )

if __name__ == "__main__":
    mcp.run()
```

### Structured Output (Function Calling)
Fireworks supports function calling via Pydantic or JSON schemas for reliable data extraction. This example demonstrates strict **Pydantic v2** validation.

```python
import os
from pydantic import BaseModel, Field, ValidationError
from openai import OpenAI

client = OpenAI(
    base_url="https://api.fireworks.ai/inference/v1",
    api_key=os.environ.get("FIREWORKS_API_KEY", "mock-key")
)

class ExecutionPlan(BaseModel):
    task_name: str = Field(description="Name of the execution task")
    priority: int = Field(default=1, ge=1, le=5, description="Priority level from 1 to 5")
    actions: List[str] = Field(default_factory=list, description="Sub-steps required to complete the task")

try:
    response = client.chat.completions.create(
        model="accounts/fireworks/models/qwen-36b-vl-instruct",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that responds ONLY with valid JSON matching the schema requested."},
            {"role": "user", "content": "Task: Upgrade database schema, Priority: 1. Actions: Stop app, Run migrations, Restart app."}
        ],
        response_format={
            "type": "json_object",
            "schema": ExecutionPlan.model_json_schema()
        }
    )

    raw_content = response.choices[0].message.content
    plan = ExecutionPlan.model_validate_json(raw_content)
    print(f"Validated Plan: {plan.task_name} (Priority {plan.priority})")
    print(f"Steps: {', '.join(plan.actions)}")

except ValidationError as e:
    print(f"Schema validation failed: {e}")
except Exception as e:
    print(f"API call failed: {e}")
```

### LoRA Adapter Usage
Deploying a custom adapter over a base model with zero cold-start delay.

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://api.fireworks.ai/inference/v1",
    api_key=os.environ.get("FIREWORKS_API_KEY", "mock-key")
)

response = client.chat.completions.create(
    model="accounts/your-account/models/your-base-model",
    extra_body={"lora_adapter": "accounts/your-account/models/your-adapter-id"},
    messages=[{"role": "user", "content": "Generate code in my specific style."}]
)
```

## Operational Best Practices & Troubleshooting

### Rate Limits & Provisioned Throughput
- **Shared Deployment**: Default rate limits depend on tier; use backoff retries with `tenacity` or `httpx` async handlers for high concurrency.
- **On-Demand On-Server LoRA**: Keep LoRA rank sizes <= 64 for optimal FireAttention swapping speeds.

## Related tools / concepts
- [Groq](groq.md) — Low-latency LPU-based inference provider.
- [Together AI](together.md) — Comprehensive serverless inference platform.
- [Mistral](mistral.md) — High-performance model family often hosted on Fireworks.
- [vLLM](../infrastructure/vllm.md) — Open-source inference engine for self-hosting.
- [TGI](../infrastructure/tgi.md) — Hugging Face's production inference server.
- [SGLang](../infrastructure/sglang.md) — High-throughput runtime for LLMs.
- [OpenRouter](../ai_knowledge/openrouter.md) — Unified model access gateway.
- [LiteLLM](../../services/litellm.md) — Proxy for unified API calls.
- [Local LLMs](../ai_knowledge/local_llms.md) — Guide for running Llama 4 Maverick and Gemma 4 locally.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standardized agent communication protocol.

## Sources / references
- [Official Website](https://fireworks.ai/)
- [Fireworks AI Docs](https://docs.fireworks.ai/)
- [Model Directory](https://fireworks.ai/models)
- [FireAttention Benchmarks](https://fireworks.ai/blog/fireattention)
- [FastMCP 3.1 Task Protocol Specification](https://modelcontextprotocol.io/3.1/task-protocol)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
