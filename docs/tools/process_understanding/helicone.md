# Helicone

## What it is
Helicone is an open-source AI Gateway and LLM observability platform that acts as a proxy between your application and various LLM providers (such as OpenAI, Anthropic, Gemini, and Groq). It provides a unified API for accessing 100+ models while recording all requests, responses, and metadata for detailed analytics and debugging.

## What problem it solves
Developing LLM applications often lacks transparency regarding what is happening "under the hood." Helicone addresses several critical pain points:
- **Visibility Gap**: Developers can see exactly what prompts were sent, what responses were received, and the associated metadata.
- **Cost and Latency Tracking**: Provides real-time metrics on token usage, financial spend, and performance bottlenecks across different models.
- **Reliability Issues**: Offers intelligent routing, retries, and automatic fallbacks to ensure application uptime even when a specific provider is down.
- **Prompt Iteration**: Decouples prompts from code with a centralized management system and version control.

## Where it fits in the stack
Helicone sits in the **AI Gateway and Observability** layer. It is positioned between the application code and the inference providers, acting as an intelligent intermediary that manages telemetry and request flow.

## Typical use cases
- **Production Monitoring**: Tracking real-time throughput, error rates, and costs for live AI features.
- **Agent Tracing**: Inspecting complex multi-step sessions to identify where an agentic loop failed or became inefficient.
- **Prompt Engineering**: Testing and versioning prompts in a UI-based playground using production data.
- **Fine-tuning Preparation**: Tagging and exporting specific request/response pairs to fine-tuning partners like OpenPipe.
- **Caching**: Implementing proxy-level caching to reduce costs and latency for repetitive LLM queries.

## Strengths
- **Low-Friction Integration**: Usually requires changing only the `baseURL` and adding a Helicone API key header.
- **Open Source and Self-hostable**: Offers a Docker-based deployment for teams requiring complete data sovereignty.
- **Unified Provider Access**: Access 100+ models through a single, OpenAI-compatible API interface.
- **Rich Feature Set**: Includes A/B testing, user-level tracking, custom property logging, and PostHog integration.

## Limitations
- **Proxy Dependency**: If the proxy is unavailable, the application's LLM features may fail (mitigated by self-hosting or using Helicone's high-availability cloud).
- **Network Latency**: Adds a marginal amount of latency for the proxy hop, though this is often offset by the platform's caching capabilities.
- **Provider-Specific Features**: Some very new or niche features of specific LLM providers might take a short time to be fully supported through the gateway.

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

### Basic Integration (OpenAI Python)
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

response = client.chat.completions.create(
  model="gpt-4o",
  messages=[{"role": "user", "content": "Explain quantum entanglement in one sentence."}]
)

print(response.choices[0].message.content)
```

### Logging Custom Properties
You can add custom properties to your requests to enable advanced filtering and analytics in the Helicone dashboard:

```python
response = client.chat.completions.create(
  model="gpt-4o",
  messages=[{"role": "user", "content": "Summarize this document."}],
  extra_headers={
    "Helicone-Property-User-Plan": "premium",
    "Helicone-Property-Source": "mobile-app"
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

## Related tools / concepts
- [Langfuse](langfuse.md) - Open-source LLM engineering platform with strong evaluation tools.
- [AgentOps](agentops.md) - Specialized observability for autonomous agent workflows.
- [Portkey AI Gateway](../providers/portkey.md) - Enterprise-grade AI gateway and observability.
- [LiteLLM](../../services/litellm.md) - Lightweight LLM proxy that can also export to Helicone.
- [OpenRouter](../ai_knowledge/openrouter.md) - Aggregator that provides its own unified API and logging.
- [Arize AI](arize-ai.md) - ML observability platform that supports LLM tracing.
- [Braintrust](braintrust.md) - Software for building and evaluating AI applications.
- [PostHog](posthog.md) - Product analytics platform that Helicone can export data to.

## Sources / references
- [Helicone Official Website](https://www.helicone.ai/)
- [Helicone Documentation](https://docs.helicone.ai/)
- [Helicone GitHub Repository](https://github.com/Helicone/helicone)

## Contribution Metadata
- Last reviewed: 2026-05-11
- Confidence: high
