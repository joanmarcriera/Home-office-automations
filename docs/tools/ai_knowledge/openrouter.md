# OpenRouter

## What it is
OpenRouter is a unified API gateway and intelligent "meta-provider" for Large Language Models (LLMs) and multimodal foundation models. It offers a single, OpenAI-compatible API to access hundreds of models from providers like OpenAI, Anthropic, Google, Meta, DeepSeek, Mistral, and Qwen. By early January 2027, OpenRouter features native **FastMCP 3.1 routing**, real-time reasoning/thinking token streaming, dynamic auto-fallbacks, and unified organization analytics.

## What problem it solves
It eliminates the complexity of managing multiple developer accounts, API keys, billing subscriptions, and client SDKs across different AI providers. It also mitigates API outages, rate limits, and regional restrictions through automated, zero-downtime model fallbacks and multi-region load balancing.

## Where it fits in the stack
**Provider / Routing Layer**. It sits between application/agent frameworks (such as [LangChain](langchain.md) or [Claude Code](../development_ops/claude-code.md)) and underlying LLM infrastructure endpoints, functioning as a smart proxy, load balancer, and intelligence router.

## Typical use cases
- **Multi-Model Agent Orchestration**: Seamlessly toggling between specialized models (e.g., Gemini 4.0 for long-context retrieval, Claude 5.1 for code synthesis, DeepSeek for high-volume reasoning) via a single endpoint.
- **Consolidated Spent & Credit Management**: Aggregating enterprise or team AI API usage across dozens of model families into one unified billing account.
- **Hosted Open-Weights Access**: Deploying models like Llama 4, Gemma 3, or Qwen 3.8 without local GPU hardware management or dedicated cloud infrastructure.
- **High-Availability Fallback Chains**: Configuring primary and fallback model arrays (e.g., GPT-5.5 -> Claude 5.1 -> Qwen 3.8) to maintain 99.99% system availability.

## Strengths
- **Vast Model Selection**: Instant access to 250+ model variations through a single API key.
- **Transparent Competitive Pricing**: Routes requests dynamically to the lowest-cost provider hosting open-weights models.
- **Standardized Drop-In API**: Completely OpenAI-compatible `chat/completions` and structured outputs interface.
- **Advanced Capabilities**: Native tool calling, structured outputs, prompt caching, thinking token streams, and FastMCP 3.1 routing.
- **Privacy Controls**: Optional "no-trace" configurations preventing third-party model providers from storing or training on prompt data.

## Limitations
- **Gateway Overhead**: Introduces a minor network proxy latency (typically < 10ms) relative to direct provider connections.
- **Intermediary Trust**: Requires trusting OpenRouter as a secure proxy in the data path.
- **Single Point of Dependency**: Disruption to OpenRouter's proxy layer temporarily affects access to all downstream routed models.

## When to use it
- During development and prototyping to quickly compare model accuracy, latency, and costs.
- For production agents that require multi-provider failover, model routing, and cost optimization.
- In team environments where centralized budget control and unified usage reporting are required.

## When not to use it
- For latency-critical edge applications where microsecond round-trips matter.
- When direct enterprise SLAs and reserved compute capacity with a specific provider (e.g., Azure OpenAI) are already established.
- When strict air-gapped data residency policies mandate local-only inference (prefer [Local LLMs](local_llms.md)).

## Getting started

### 1. API Key Setup
1. Create an account at [openrouter.ai](https://openrouter.ai/).
2. Navigate to Keys and generate a new secret API key.
3. Pre-fund your account balance or attach enterprise payment details.

### 2. Environment Setup
```bash
export OPENROUTER_API_KEY="your_openrouter_api_key"
```

## CLI examples

### Testing Endpoint with cURL
```bash
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -d '{
    "model": "google/gemma-3-27b-it",
    "messages": [{"role": "user", "content": "Explain FastMCP 3.1 protocol features."}]
  }'
```

### Listing Available Models and Pricing
```bash
curl -s https://openrouter.ai/api/v1/models | jq '.data[] | {id, pricing}' | head -n 20
```

## API examples

### Python: OpenAI Client with Fallback Chain & Pydantic v2
```python
from typing import List
from pydantic import BaseModel, Field
import openai

class RoutingBenchmark(BaseModel):
    chosen_model: str = Field(description="Name of the model used")
    response_summary: str = Field(description="Summary of the returned analysis")
    status: str = Field(description="Execution status")

client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="your_openrouter_api_key"
)

# OpenRouter accepts comma-separated model fallback priority lists
response = client.beta.chat.completions.parse(
    model="anthropic/claude-5.1-sonnet,openai/gpt-5.5,qwen/qwen-3.8-72b",
    messages=[
        {"role": "system", "content": "Analyze network telemetry and return summary."},
        {"role": "user", "content": "Analyze ping metrics for latency spikes."}
    ],
    response_format=RoutingBenchmark,
    extra_headers={
        "HTTP-Referer": "https://my-company-ops.internal",
        "X-Title": "KnowledgeOps Routing Agent"
    }
)

result: RoutingBenchmark = response.choices[0].message.parsed
print(f"Model Chosen: {result.chosen_model}")
print(f"Summary: {result.response_summary}")
```

## Related tools / concepts
- [OpenAI](openai.md) — Primary foundation model provider.
- [Claude](claude.md) — High-reasoning frontier models.
- [Gemini](gemini.md) — Long-context multimodal model series.
- [Local LLMs](local_llms.md) — Self-hosted open-weights models.
- [FastMCP 3.1](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Open protocol for agent tools.
- [LangChain](langchain.md) — Agent orchestration framework.

## Sources / references
- [OpenRouter Official Developer Documentation](https://openrouter.ai/docs)
- [OpenRouter API Reference and Model List](https://openrouter.ai/api/v1/models)
- [OpenRouter Rankings and Benchmarks](https://openrouter.ai/rankings)
- [Antling-30B-Flash on OpenRouter](https://www.reddit.com/r/LocalLLaMA/comments/1v4m5cr/antling30flash_is_now_live_on_openrouter_and_free/) — Antling-30B-Flash live on OpenRouter.

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
