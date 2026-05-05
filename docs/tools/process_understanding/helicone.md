# Helicone

## What it is
Helicone is an open-source LLM observability platform that acts as a proxy between your application and LLM providers (like OpenAI, Anthropic, or Groq). It records all requests, responses, and metadata, providing detailed analytics and debugging tools.

## What problem it solves
It solves the visibility gap in AI applications. Developers often don't know exactly what prompts are being sent, how much they cost in real-time, or where bottlenecks are occurring. Helicone provides a central dashboard for monitoring costs, latency, and model performance with minimal code changes.

## Where it fits in the stack
**Category**: Process & Understanding / LLM Gateway & Observability

## Typical use cases
- **Cost Monitoring**: Tracking spend across multiple models and environments (dev vs. prod).
- **Prompt Debugging**: Inspecting full request/response cycles to fix edge cases.
- **Performance Benchmarking**: Comparing latency between different providers or model versions.
- **Caching**: Reducing costs and latency by caching frequent LLM responses at the proxy level.

## Strengths
- **Low Friction**: Implementation usually requires just changing the `base_url` in your LLM client.
- **Open Source**: Can be self-hosted for maximum privacy and data control.
- **Real-time Analytics**: Dashboard provides instant feedback on throughput and error rates.
- **Feature Rich**: Includes tools for A/B testing, user-level tracking, and custom property logging.

## Limitations
- **Proxy Latency**: Adds a very small amount of network latency (though often offset by caching).
- **Dependency**: Your application's availability depends on the proxy being up (mitigated by Helicone's high availability).

## Getting started

### Basic Integration (OpenAI Python)
```python
import openai

client = openai.OpenAI(
  api_key="your-api-key",
  base_url="https://oai.helicone.ai/v1",
  default_headers={
    "Helicone-Auth": f"Bearer {HELICONE_API_KEY}"
  }
)

response = client.chat.completions.create(
  model="gpt-4o",
  messages=[{"role": "user", "content": "Hello!"}]
)
```

## CLI examples

### helm compose up
Deploys the complete Helicone stack using Helm Compose (for self-hosting):
```bash
helm compose up
```

### aws s3 ls
List backups or logs stored in S3 (standard infrastructure management for Helicone):
```bash
aws s3 ls s3://helicone-backups/
```

### curl (Manual Proxy Test)
Test the Helicone proxy connectivity directly via curl:
```bash
curl https://oai.helicone.ai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Helicone-Auth: Bearer $HELICONE_API_KEY" \
  -d '{"model": "gpt-4o", "messages": [{"role": "user", "content": "Hello"}]}'
```

## API examples

### Python (Logging Custom Properties)
```python
import openai

client = openai.OpenAI(
  api_key="OPENAI_API_KEY",
  base_url="https://oai.helicone.ai/v1",
  default_headers={
    "Helicone-Auth": f"Bearer {HELICONE_API_KEY}",
    "Helicone-Property-Session": "session_123",
    "Helicone-Property-App": "demo-app"
  }
)

# Properties are automatically tracked in the Helicone dashboard
response = client.chat.completions.create(
  model="gpt-4o",
  messages=[{"role": "user", "content": "Analyze this data."}]
)
```

## Related tools / concepts
- [Langfuse](langfuse.md)
- [AgentOps](agentops.md)
- [Portkey AI Gateway](../providers/portkey.md)
- [LiteLLM](../../services/litellm.md)
- [OpenRouter](../ai_knowledge/openrouter.md)

## Sources / references
- [Helicone Official Website](https://www.helicone.ai/)
- [Helicone Documentation](https://docs.helicone.ai/)

## Contribution Metadata
- Last reviewed: 2026-05-09
- Confidence: high
