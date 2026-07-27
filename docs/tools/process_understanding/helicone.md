# Helicone

## What it is
Helicone is an open-source AI Gateway and LLM observability platform that acts as a proxy between your application and various LLM providers (such as OpenAI, Anthropic, Gemini, and Groq). In late July 2026, it has expanded to support the **Model Context Protocol (MCP 3.1)**, allowing agents to query observability data and session telemetry directly within their execution context.

## What problem it solves
Developing LLM applications often lacks transparency regarding what is happening "under the hood." Helicone addresses several critical pain points:
- **Visibility Gap**: Developers can see exactly what prompts were sent, what responses were received, and the associated metadata.
- **Cost and Latency Tracking**: Provides real-time metrics on token usage, financial spend, and performance bottlenecks across different models.
- **Reliability Issues**: Offers intelligent routing, retries, and automatic fallbacks to ensure application uptime even when a specific provider is down.
- **Prompt Iteration**: Decouples prompts from code with a centralized management system and version control.
- **Agentic Debugging**: Solves the difficulty of tracing multi-step reasoning loops in models like **Claude 5.1** and **GPT-5.5**.

## Where it fits in the stack
Helicone sits in the **AI Gateway and Observability** layer. It is positioned between the application code and the inference providers, acting as an intelligent intermediary that manages telemetry and request flow.

## Typical use cases
- **Production Monitoring**: Tracking real-time throughput, error rates, and costs for live AI features.
- **Agent Tracing**: Inspecting complex multi-step sessions to identify where an agentic loop failed or became inefficient.
- **Prompt Engineering**: Testing and versioning prompts in a UI-based playground using production data.
- **Fine-tuning Preparation**: Tagging and exporting specific request/response pairs to fine-tuning partners like OpenPipe.
- **Caching**: Implementing proxy-level caching to reduce costs and latency for repetitive LLM queries.
- **MCP Integration**: Using an MCP 3.1 server to allow **Llama 4 Maverick** to self-audit its own performance logs.

## Strengths
- **Low-Friction Integration**: Usually requires changing only the `baseURL` and adding a Helicone API key header.
- **Open Source and Self-hostable**: Offers a Docker-based deployment for teams requiring complete data sovereignty.
- **Unified Provider Access**: Access 100+ models through a single, OpenAI-compatible API interface.
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
pip install openai pydantic
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

### Completion with Custom Properties (Pydantic v2 Validation)
You can add custom properties to your requests to enable advanced filtering and analytics in the Helicone dashboard:

```python
from pydantic import BaseModel, Field

class SummarizationRequest(BaseModel):
    document_id: str = Field(..., description="The unique ID of the document")
    user_plan: str = Field("free", description="Subscribed plan tier of the user")

# Setup query payload
request_meta = SummarizationRequest(document_id="doc-9941", user_plan="premium")

response = client.chat.completions.create(
  model="gpt-5.5-preview",
  messages=[{"role": "user", "content": f"Summarize document: {request_meta.document_id}"}],
  extra_headers={
    "Helicone-Property-User-Plan": request_meta.user_plan,
    "Helicone-Property-Source": "mobile-app"
  }
)

print(response.choices[0].message.content)
```

### Async Integration (Python)
Helicone supports asynchronous requests natively via the standard OpenAI async client.

```python
import asyncio
import os
from openai import AsyncOpenAI

async def main():
    client = AsyncOpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        base_url="https://gateway.helicone.ai/v1",
        default_headers={
            "Helicone-Auth": f"Bearer {os.environ.get('HELICONE_API_KEY')}"
        }
    )
    # ... execution logic
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
- Last reviewed: 2026-07-27
- Confidence: high
