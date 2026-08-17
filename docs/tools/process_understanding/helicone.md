# Helicone

## What it is
Helicone is an open-source AI Gateway and LLM observability platform that acts as a high-performance proxy between your application and various LLM providers (such as OpenAI, Anthropic, Gemini, Groq, and Cohere). In early January 2027, it fully supports **FastMCP 3.1**, allowing agents like Claude 5.1, GPT-5.5, Gemini 4.0 Pro, and Llama 4 to dynamically query observability telemetry, tracing logs, and cost analytics directly within their JSON-RPC tool context.

## What problem it solves
Developing robust LLM applications often suffers from opaque prompt-response cycles, unpredictable latency, and unmonitored costs. Helicone solves these challenges by:
- **Visibility Gap**: Developers can see exactly what prompts were sent, what responses were received, and the associated metadata in real-time event graphs.
- **Cost and Latency Tracking**: Providing real-time metrics on token usage, financial spend, and performance bottlenecks across diverse model configurations.
- **Reliability Issues**: Offering intelligent routing, automatic retries, custom rate-limiting, and automatic fallbacks to ensure application uptime.
- **Prompt Iteration**: Decoupling prompts from application code with a centralized management system and semantic version control.
- **Agentic Debugging**: Enabling deep nesting trace visualizations for multi-step reasoning loops in models like **Claude 5.1** and **GPT-5.5**.

## Where it fits in the stack
Helicone sits in the **AI Gateway and Observability** layer. It is positioned between the application code and the inference providers, acting as an intelligent intermediary that manages telemetry, caching, routing, and request flow.

## Typical use cases
- **Production Monitoring**: Tracking real-time throughput, error rates, and costs for live AI features.
- **Agent Tracing**: Inspecting complex multi-step sessions to identify where an agentic loop failed or became inefficient.
- **Prompt Engineering**: Testing and versioning prompts in a UI-based playground using production data.
- **Fine-tuning Preparation**: Tagging and exporting specific request/response pairs to fine-tuning partners like OpenPipe.
- **Caching**: Implementing proxy-level semantic caching to reduce costs and latency for repetitive LLM queries.
- **MCP Integration**: Using an MCP 3.1 server to allow **Llama 4** to self-audit its own performance logs and correct errors.

## Strengths
- **Low-Friction Integration**: Usually requires changing only the `baseURL` and adding a Helicone API key header.
- **FastMCP 3.1 & Open Source**: Full FastMCP 3.1 integration alongside self-hostable Docker deployments for privacy-first homelabs.
- **Unified Provider Access**: Access 100+ models (including Claude 5.1, GPT-5.5, Gemini 4.0 Pro, Llama 4, Gemma 3, and Qwen 3.8) through a single interface.
- **Rich Feature Set**: Includes A/B testing, user-level tracking, custom property logging, and PostHog integration.
- **Real-time Performance**: Optimized for minimal overhead even when handling high-concurrency agent swarms.

## Limitations
- **Proxy Dependency**: If the proxy is unavailable, the application's LLM features may fail (mitigated by self-hosting or using Helicone's high-availability cloud).
- **Network Latency**: Adds a marginal amount of latency for the proxy hop, though this is often offset by the platform's caching capabilities.
- **Provider-Specific Features**: Some very new or niche features of specific LLM providers might take a short time to be fully supported through the gateway.
- **Storage Costs**: High-volume tracing can lead to significant database growth if using the self-hosted version without a retention policy.

## When to use it
- When you need a unified gateway to manage multiple LLM providers with automatic failover and routing.
- When you want "zero-instrumentation" observability for OpenAI-compatible SDKs.
- When you require a self-hosted observability solution due to data privacy or compliance requirements.
- When you need to systematically track LLM costs and latency across different teams or environments.

## When not to use it
- For extremely simple applications where basic local logging is sufficient and a proxy adds unnecessary complexity.
- If you are already using a comprehensive agent framework (like [AgentOps](agentops.md)) that provides its own integrated observability.
- If your application has extremely strict latency requirements that cannot tolerate even a marginal proxy hop (and caching is not applicable).

## Getting started

### Installation
To use Helicone with the OpenAI Python SDK, no special installation is required beyond the standard SDK.

```bash
pip install openai
```

### Basic Integration
Updating an existing OpenAI integration to use Helicone is straightforward:

```python
import os
from openai import OpenAI

# Configure the client to point to the Helicone gateway
client = OpenAI(
  api_key=os.environ.get("OPENAI_API_KEY"),
  base_url="https://gateway.helicone.ai/v1",
  default_headers={
    "Helicone-Auth": f"Bearer {os.environ.get('HELICONE_API_KEY')}"
  }
)
```

## CLI examples

### Self-Hosting with Docker
To start the Helicone stack locally:
```bash
git clone https://github.com/Helicone/helicone.git
cd helicone/docker
./helicone-compose.sh helicone up
```

### Manual Proxy Test (curl)
```bash
curl https://gateway.helicone.ai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Helicone-Auth: Bearer $HELICONE_API_KEY" \
  -d '{
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## API examples

### Completion with Custom Properties & Pydantic v2 Validation (Async Python)
You can configure Helicone headers and request parameters using Pydantic v2 validation schemas:

```python
import asyncio
import os
from pydantic import BaseModel, Field, field_validator
from openai import AsyncOpenAI

class HeliconeRequestConfig(BaseModel):
    user_plan: str = Field(default="premium", description="User tier for telemetry tagging")
    source: str = Field(default="home-office-agent", description="Request source identifier")
    enable_cache: bool = Field(default=True, description="Enable Helicone semantic proxy caching")
    model_name: str = Field(default="gpt-5.5", description="Target frontier model")

    @field_validator("user_plan")
    @classmethod
    def validate_plan(cls, v: str) -> str:
        allowed = {"free", "pro", "premium", "enterprise"}
        if v.lower() not in allowed:
            raise ValueError(f"user_plan must be one of {allowed}")
        return v.lower()

async def main():
    config = HeliconeRequestConfig(
        user_plan="premium",
        source="mcp-agent-loop",
        model_name="gpt-5.5"
    )

    client = AsyncOpenAI(
        api_key=os.environ.get("OPENAI_API_KEY", "sk-dummy"),
        base_url="https://gateway.helicone.ai/v1",
        default_headers={
            "Helicone-Auth": f"Bearer {os.environ.get('HELICONE_API_KEY', 'sk-helicone-dummy')}"
        }
    )

    extra_headers = {
        "Helicone-Property-User-Plan": config.user_plan,
        "Helicone-Property-Source": config.source,
        "Helicone-Cache": "true" if config.enable_cache else "false"
    }

    print("Sending request with validated Helicone config:", config.model_dump())
    # Example execution (will perform call if live keys exist)
    try:
        response = await client.chat.completions.create(
            model=config.model_name,
            messages=[{"role": "user", "content": "Verify Helicone FastMCP 3.1 telemetry integration."}],
            extra_headers=extra_headers
        )
        print("Response:", response.choices[0].message.content)
    except Exception as e:
        print("Helicone proxy call execution skipped or failed:", e)

if __name__ == "__main__":
    asyncio.run(main())
```

## Related tools / concepts
- [Langfuse](langfuse.md) - Open-source LLM engineering platform with strong evaluation tools.
- [AgentOps](agentops.md) - Specialized observability for autonomous agent workflows.
- [Portkey AI Gateway](../providers/portkey.md) - Enterprise-grade AI gateway and observability.
- [LiteLLM](../../services/litellm.md) - Lightweight LLM proxy that can also export to Helicone.
- [OpenRouter](../ai_knowledge/openrouter.md) - Aggregator that provides its own unified API and logging.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) - Protocol for connecting agents to data/tools.
- [Claude](../ai_knowledge/claude.md) - Primary frontier model for agentic workflows.
- [GPT-5.5 Optimization](../ai_knowledge/openai.md) - Reference for OpenAI model performance tuning.
- [Llama 4 Maverick](../ai_knowledge/local_llms.md) - Frontier-grade open model for local deployments.

## Sources / references
- [Helicone Official Website](https://www.helicone.ai/)
- [Helicone Documentation](https://docs.helicone.ai/)
- [Helicone GitHub Repository](https://github.com/Helicone/helicone)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
