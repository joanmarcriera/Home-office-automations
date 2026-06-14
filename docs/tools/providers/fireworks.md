# Fireworks AI

## What it is
Fireworks AI is a high-performance inference platform providing an ultra-fast API for running and fine-tuning open-source generative AI models (Llama, Mixtral, Qwen). As of June 2026, it is recognized for its proprietary "FireAttention" optimization stack, which consistently delivers industry-leading tokens-per-second (TPS) for frontier open-weights models.

## What problem it solves
It provides reliable, low-latency, and cost-effective access to the latest open-source models, eliminating the performance overhead of standard GPU deployments and the complexity of managing private inference infrastructure.

## Where it fits in the stack
**Inference Provider**. Fireworks AI sits in the **Infrastructure** layer, providing the raw compute and model serving capability that powers higher-level agentic frameworks. It serves as a performance-optimized alternative to self-hosting via vLLM or using general-purpose providers like Together AI.

## Typical use cases
- **High-Throughput Applications**: Production apps requiring many concurrent, low-latency LLM requests for real-time interaction.
- **Function Calling**: Using their optimized models (e.g., Llama 4 family) for reliable structured data extraction and autonomous tool use.
- **Custom Model Deployment**: Deploying specialized fine-tuned models on dedicated, scalable infrastructure via LoRA adapters.
- **Real-time Agents**: Powering agents that require immediate reasoning responses to maintain conversation flow.

## Strengths
- **Extreme Speed**: The FireAttention engine provides exceptionally high throughput and low time-to-first-token (TTFT).
- **LoRA Support**: Native, first-class support for deploying and switching between custom LoRA adapters with zero cold-start latency.
- **Developer Experience**: Fully OpenAI-compatible API ensures seamless migration from other providers.
- **Cost-Efficiency**: Competitive serverless pricing that is often significantly lower than proprietary frontier models like GPT-5.5.
- **Model Variety**: Curated selection of the best-performing open models, including Llama, Mistral, and Qwen architectures.

## Limitations
- **Focus**: Prioritizes performance for a curated set of models rather than hosting every niche model available on Hugging Face.
- **Proprietary Optimizations**: While models are open-weights, the underlying FireAttention stack is proprietary.
- **Cloud-Only**: Does not offer a standalone local version for completely offline environments.

## When to use it
- When you need the fastest possible inference for Llama 3/4 or other top-tier open models.
- For high-volume production applications where reliability and consistent latency are critical.
- When you need to deploy and manage multiple fine-tuned LoRA adapters efficiently.
- When building real-time interactive agents.

## When not to use it
- If your application requires proprietary "frontier" models like `claude-4-8-opus-20260528`.
- For extremely niche or research models that are not included in their curated performance-optimized list.
- If strict data sovereignty requires 100% on-premises local hosting (see [vLLM](../infrastructure/vllm.md)).

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
    model="accounts/fireworks/models/llama-v3-70b-instruct",
    messages=[{"role": "user", "content": "Hello Fireworks!"}]
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
    "model": "accounts/fireworks/models/llama-v3-70b-instruct",
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
    model="accounts/fireworks/models/llama-v3-70b-instruct",
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
- [Llama 4](../ai_knowledge/llama.md) — The frontier open-weights family optimized for Fireworks.

## Sources / references
- [Official Website](https://fireworks.ai/)
- [Fireworks AI Docs](https://docs.fireworks.ai/)
- [Model Directory](https://fireworks.ai/models)
- [FireAttention Benchmarks](https://fireworks.ai/blog/fireattention)

## Contribution Metadata
- Last reviewed: 2026-06-12
- Confidence: high
